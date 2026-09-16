"""Native-engine worker: builds the BitCrack/Kangaroo command line, runs it,
watches output, and fires the on-found hook (offline verify -> write found/).

Design notes
  * a worker owns exactly ONE engine share on ONE device (no overbooking);
  * first verified hit globally wins: a threading.Event is set and every
    other running worker is terminated (the dangerous duplicate-claim race);
  * engine checkpoints stay in place on terminate, so ``resume`` continues
    from the native progress file;
  * stdout of each engine is tee'd to logs/<n>_<share>.log AND scanned for
    the known privkey-line shapes of both engines.
"""

import os
import re
import subprocess
import sys
import threading

from . import validator
from . import checkpoint as ckpt

# Line shapes that can carry a found key (BitCrack + Kangaroo + forks):
#   Key found privkey <hex>
#   KEY FOUND! Privkey: <hex>
#   Key: 0x<hex>
#   privkey = <hex>
_KEY_RE = re.compile(
    r"(?:privkey|Privkey|PRIVKEY|Key)\s*[:= ]+\s*"
    r"(?:0x)?([0-9a-fA-F]{2,64})\b")

_EO_BANNER = re.compile(r"(solved|Key found|KEY FOUND|found)", re.IGNORECASE)


def pid_and_report(exe, args):
    return [exe] + [str(a) for a in args]


def build_bitcrack_cmd(binary, puzzle, share, device, continue_path,
                       target_path, extra, compression="both"):
    cmd = [binary, "--keyspace", "%s:%s" % (share["start_hex"], share["end_hex"]),
           "--continue", continue_path]
    if device is not None:
        cmd += ["-d", str(device)]
    cmd += ["--compression", compression]
    if extra:
        cmd += extra.split()
    cmd += ["-i", target_path]
    return cmd


def build_kangaroo_cmd(binary, puzzle, work_path, in_path, save_interval="60",
                       devices=None, extra=None):
    """JeanLucPons Kangaroo: ONE process owns the WHOLE interval and fans out
    kangaroo herds to every listed GPU (`-gpuId` per device).  GPUs share the
    same DP table, so adding devices is ~linear, NOT sqrt(K)-penalized like
    naively splitting into K per-GPU sub-intervals."""
    cmd = [binary, "-gpu"]
    devs = [int(d) for d in (devices or []) if d is not None]
    if not devs:
        devs = [0]
    for d in devs:
        cmd += ["-gpuId", str(d)]
    cmd += ["-w", work_path, "-wi", save_interval, "-ws"]
    if extra:
        cmd += extra.split()
    cmd += ["-o", in_path + ".found", in_path]
    return cmd


def write_kangaroo_input(puzzle, share):
    """Kangaroo input file: START, END, PUBKEY."""
    if not puzzle.pubkey:
        raise ValueError("kangaroo requires an exposed pubkey (R2 only)")
    path = os.path.join(ckpt.WORK_DIR, "in_%d_%d.txt" % (puzzle.n, share["share_idx"]))
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(share["start_hex"] + "\n")
        fh.write(share["end_hex"] + "\n")
        fh.write(puzzle.pubkey + "\n")
    return path


def write_target_file(puzzle):
    path = os.path.join(ckpt.STATE_DIR, "targets_%d.txt" % puzzle.n)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(puzzle.address + "\n")
    return path


class StopScan(Exception):
    pass


def _save_found(puzzle, artifacts):
    os.makedirs(ckpt.FOUND_DIR, exist_ok=True)
    path = os.path.join(ckpt.FOUND_DIR, "puzzle_%d_%s.txt" % (puzzle.n, puzzle.address))
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("# Puzzle #%d  %s\n" % (puzzle.n, puzzle.address))
        fh.write("privkey_hex=%s\n" % artifacts["privkey_hex"])
        fh.write("compressed_address=%s\n" % artifacts["compressed_address"])
        fh.write("uncompressed_address=%s\n" % artifacts["uncompressed_address"])
        fh.write("wif_compressed=%s\n" % artifacts["wif_compressed"])
        fh.write("wif_uncompressed=%s\n" % artifacts["wif_uncompressed"])
        fh.write("matched_form=%s\n" % artifacts["matched_form"])
    return path


def run_worker(binary, puzzle, engine, share, device=None, extra=None,
               stop_event=None, dry_run=False,
               on_found_artifacts=None, on_progress=None):
    """Run one engine share. Returns 'found' / 'error' / 'exited' / 'skipped'.

    ``on_found_artifacts(artifacts)`` is fired the instant a key verifies
    offline (before it is even written to disk), enabling the cluster
    coordinator to confirm before trusting a node's claim.
    ``on_progress(kps_or_None)`` streams per-line engine rate when the engine
    prints a keys/s figure (for live telemetry)."""
    ck = ckpt.Checkpoint()
    rec = ck.claim(puzzle.n, share["share_idx"], share["total_shares"],
                   share["start_hex"], share["end_hex"], engine, device=device)

    if engine == "bitcrack":
        cont_path = os.path.join(ckpt.SCAN_DIR, "%d_%d.kc" % (puzzle.n, share["share_idx"]))
        # resume: engine keeps scanning from its own native 'next key'
        target_path = write_target_file(puzzle)
        cmd = build_bitcrack_cmd(binary, puzzle, share, device, cont_path,
                                 target_path, extra)
    elif engine == "kangaroo":
        work_path = os.path.join(ckpt.WORK_DIR, "%d_%d.work" % (puzzle.n, share["share_idx"]))
        in_path = write_kangaroo_input(puzzle, share)
        # a worker may be handed several GPUs (devices=[...]): kangaroo fans
        # one interval out to all of them sharing one DP table.
        devs = device if isinstance(device, (list, tuple)) else ([device] if device is not None else None)
        cmd = build_kangaroo_cmd(binary, puzzle, work_path, in_path,
                                 devices=devs, extra=extra)
    else:
        raise ValueError("unknown engine: %s" % engine)

    if dry_run:
        print(" ".join(map(str, cmd)) if os.name == "posix"
              else subprocess.list2cmdline(cmd))
        return "skipped"

    log_path = os.path.join(ckpt.LOG_DIR, "%d_%d.log" % (puzzle.n, share["share_idx"]))
    logf = open(log_path, "a", encoding="utf-8", errors="replace")
    logf.write("\n# %s\n" % " ".join(subprocess.list2cmdline(cmd)))
    logf.flush()

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, errors="replace", bufsize=1,
        )
    except OSError as e:
        logf.close()
        ck.touch(rec, status="error", note=str(e))
        print("worker error: %s" % e)
        return "error"

    ck.touch(rec, status="running", engine_ckpt=cont_path if engine == "bitcrack"
             else work_path)

    def pump(stream, logf, rec):
        for line in stream:
            if stop_event is not None and stop_event.is_set():
                proc.terminate()
                break
            logf.write(line)
            logf.flush()
            # optional: feed live keys/s metric (e.g. "1234.56 MKey/s")
            if on_progress is not None:
                _km = re.search(r"([\d.]+)\s*[Mm][Kk]ey/", line)
                if _km:
                    on_progress(float(_km.group(1)) * 1_000_000)
            m = _KEY_RE.search(line)
            if not m:
                continue
            try:
                artifacts = validator.verify_candidate(m.group(1), puzzle.address)
            except validator.ValidationError:
                continue  # false positive banner or wrong key form
            if on_found_artifacts is not None:
                try:
                    on_found_artifacts(artifacts)
                except Exception:                        # noqa: BLE001
                    pass
            found_path = _save_found(puzzle, artifacts)
            ck.mark_found(rec, found_path)
            if stop_event is not None:
                stop_event.set()
            print("[FOUND] %s" % artifacts["privkey_hex"])
            return True
        return False

    found = pump(proc.stdout, logf, rec)
    if not found:
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.terminate()
    logf.close()
    if found:
        ck.touch(rec, status="found")
        return "found"
    if stop_event is not None and stop_event.is_set():
        ck.touch(rec, status="paused")
        return "exited"
    ck.touch(rec, status="finished")
    return "exited"


def scan_parallel(binary, puzzle, engine, shares, stop_event=None,
                  devices=None, extra=None, dry_run=False):
    """Run shares across devices in parallel; first verified hit stops all."""
    results = []
    lock = threading.Lock()

    def one(dev, share):
        r = run_worker(binary, puzzle, engine, share, device=dev,
                       extra=extra, stop_event=stop_event, dry_run=dry_run)
        with lock:
            results.append((dev, share["share_idx"], r))

    threads = []
    if devices is None:
        devices = [None] * len(shares)
    for dev, share in zip(devices, shares):
        t = threading.Thread(target=one, args=(dev, share))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    return results