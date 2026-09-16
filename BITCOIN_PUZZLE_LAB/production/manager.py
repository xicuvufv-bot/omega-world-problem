"""Production pipeline CLI.

Commands
  status                  verify puzzle status (live tracker + chain spot)
  plan                    feasibility rank of unsolved puzzles
  audit   [--number|--address]
                          full dossier of one target (method, keyspace, est)
  gpus                    enumerate CUDA devices
  bench   --puzzle N [--bits B]
                          measure real keys/s with BitCrack on a small window
  scan    --puzzle N [--engine auto] [--gpus N] [--extra "..."] [--dry-run]
  resume  --puzzle N      relaunch claimed/paused shares from native checkpoints
  found                   list every verified key file

Engine binaries are resolved as:
  1) $BITCRACK / $KANGAROO env vars
  2) production/bin/cuBitCrack / cuBitCrack.exe
  3) production/bin/kangaroo / kangaroo.exe
"""

import argparse
import glob
import os
import subprocess
import sys
import threading
import time

from . import checkpoint as ckpt
from . import gpu as gpu_mod
from . import keyspace as ks
from . import registry
from . import runner
from . import status as status_mod
from . import strategy

BIN_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin")
os.makedirs(BIN_DIR, exist_ok=True)


def find_binary(name, env):
    env_path = os.environ.get(env)
    if env_path:
        return env_path
    candidates = glob.glob(os.path.join(BIN_DIR, name + ".*"))
    if candidates:
        return candidates[0]
    return None


def need_binary(name, env, hint):
    path = find_binary(name, env)
    if not path:
        sys.exit("engine not found: %s (expected at production/bin/%s.* or %s env). "
                 "Run build/build_windows.ps1 or build/build_linux.sh. %s"
                 % (name, name, env, hint))
    return path


# ---------------------------------------------------------------- commands

def cmd_status(args):
    report = status_mod.refresh(chain_check=args.chain, timeout=args.timeout)
    print("tracker:", report["attempts"].get("tracker"))
    for e in report["errors"]:
        print("WARN:", e)
    print("registry:", report["registry"])
    if report["live"]:
        print("live   :", report["live"])
    if report["diffs"]:
        print("DIFFS (changed since frozen registry):")
        for d in report["diffs"]:
            print("  ", d)
    else:
        print("no diffs: state matches the published tracker (unsolved untouched).")
    if report["chain_spot"]:
        for n, c in sorted(report["chain_spot"].items()):
            print("  #%d balance: %.8f BTC" % (n, c["sats"] / 1e8))
    print("wrote", status_mod.STATUS_JSON, "and", status_mod.STATUS_MD)


def cmd_plan(args):
    gpus = args.gpus or max(1, gpu_mod.summary()["count"])
    measured = None
    if args.measured:
        measured = float(args.measured)
    plans = strategy.plan(registry.unsolved(), gpu_count=gpus, measured_kps=measured)
    print("%-4s %-8s %-10s %-8s %s" % ("#", "regime", "engine", "GPU-years", "address"))
    for p in plans[: (args.limit or 20)]:
        print("%-4d %-8s %-10s %-8s %s"
              % (p["n"], p["regime"], p["engine"],
                 ks.human_seconds(p["seconds"]).rjust(8), p["address"]))
    print("\nRate model:", ("user-supplied %.0f keys/s" % measured) if measured
          else "R1=%.0e / R2=%.0e single-GPU defaults"
          % (strategy.FULL_R1_RATE, strategy.FULL_R2_RATE))
    print("Reality: all remaining puzzles are multi-thousand-GPU-year projects.")


def cmd_audit(args):
    p = registry.resolve_target(address=args.address, number=args.number)
    est = strategy.estimate(p, gpu_count=args.gpus or 1)
    print("Puzzle #%d  [%s]" % (p.n, p.regime))
    print("  address :", p.address)
    print("  range   : [0x%s, 0x%s]  width=2^%d" % (p.lo_hex, p.hi_hex, p.bits - 1))
    print("  pubkey  :", p.pubkey or "(not exposed)")
    print("  solved  :", p.solved)
    if est:
        print("  engine  :", est["engine"])
        print("  why     :", est["why"])
        print("  est.    :", ks.human_seconds(est["seconds"]),
              "on", est["gpu_count"], "GPU(s)")


def cmd_gpus(args):
    s = gpu_mod.summary()
    if not s["present"]:
        print("no nvidia-smi found; assume a single CPU/device and pass --gpus 1")
        return
    print("CUDA GPUs:", s["count"])
    for d in s["devices"]:
        print("  [%d] %-40s %.1f GB" % (d["id"], d["name"], d["memory_gb"]))


def cmd_bench(args):
    p = registry.resolve_target(address=args.address, number=args.number)
    if p.solved:
        sys.exit("refusing to benchmark a solved puzzle")
    bc = need_binary("cuBitCrack", "BITCRACK",
                     "(compile V1 fork; NVIDIA CUDA toolkit required)")
    bits = args.bits
    size = 1 << (bits - 1)
    share = {"share_idx": 0, "total_shares": 1,
             "start_hex": "%x" % p.lo,
             "end_hex": "%x" % (p.lo + size - 1),
             "start": p.lo, "end": p.lo + size - 1}
    t0 = time.monotonic()
    print("benchmarking %d keys on %s ..." % (size, p.address))
    res = runner.run_worker(bc, p, "bitcrack", share, extra=args.extra)
    elapsed = time.monotonic() - t0
    if res == "error":
        sys.exit("benchmark failed")
    kps = size / max(elapsed, 1e-9)
    print("elapsed=%.1fs  =>  %.2f Mkeys/s" % (elapsed, kps / 1e6))
    return kps


def cmd_scan(args):
    p = registry.resolve_target(address=args.address, number=args.number)
    if p.solved:
        sys.exit("puzzle #%d is SOLVED; nothing to scan" % p.n)

    engine = args.engine or "auto"
    if engine == "auto":
        engine = "kangaroo" if p.regime == "R2" else "bitcrack"
    if engine == "kangaroo" and p.regime != "R2":
        sys.exit("kangaroo needs an exposed pubkey; #%d is R1 (use 'bitcrack')" % p.n)

    # sub-range (optional, must stay inside the official interval)
    start_hex, end_hex = None, None
    if args.start or args.end:
        start_hex, end_hex = ks.validate_subrange(p,
                                                  args.start or p.lo_hex,
                                                  args.end or p.hi_hex)
        start_hex, end_hex = "%x" % start_hex, "%x" % end_hex

    n_gpus = args.gpus or max(1, gpu_mod.summary()["count"])
    if not args.gpus and engine == "bitcrack" and not gpu_mod.summary()["present"]:
        sys.exit("no CUDA devices found; BitCrack needs a GPU (add --gpus 1 to test)")

    binary = None
    if not args.dry_run:
        binary = (need_binary("kangaroo", "KANGAROO", "(compile JeanLucPons/Kangaroo)")
                  if engine == "kangaroo" else
                  need_binary("cuBitCrack", "BITCRACK",
                              "(compile brichard19/BitCrack CUDA)"))

    # Kangaroo can NOT be sharded into independent per-GPU sub-intervals:
    # that would lose the shared DP table (work grows ~sqrt(K)).  Instead it
    # runs ONE process over the whole (sub)range, fanning herds to all GPUs.
    if engine == "kangaroo":
        lo, hi = int(start_hex or p.lo_hex, 16), int(end_hex or p.hi_hex, 16)
        if args.dry_run:
            print("# engine=%s puzzle=%d devices=%d shares=1 (full-interval)"
                  % (engine, p.n, n_gpus))
            share = {"share_idx": 0, "total_shares": 1,
                     "start_hex": "%x" % lo, "end_hex": "%x" % hi}
            runner.run_worker(binary or "kangaroo", p, engine, share,
                              device=[d["id"] for d in gpu_mod.devices()][:n_gpus],
                              extra=args.extra, dry_run=True)
            return
        devices = [d["id"] for d in gpu_mod.devices()][:n_gpus] or [None]
        share = {"share_idx": 0, "total_shares": 1,
                 "start_hex": "%x" % lo, "end_hex": "%x" % hi}
        stop = threading.Event()
        print("scanning #%d [0x%x:0x%x] with kangaroo on %d device(s) (single shared interval)"
              % (p.n, lo, hi, len([d for d in devices if d is not None])))
        res = runner.run_worker(binary, p, "kangaroo", share, device=devices,
                                stop_event=stop, extra=args.extra)
        print("  result -> %s" % res)
        return

    if start_hex is None:
        shares = ks.split_equal(p, n_gpus)
        start_hex, end_hex = shares[0][1], shares[-1][2]
    else:
        lo, hi = int(start_hex, 16), int(end_hex, 16)
        width = hi - lo + 1
        base, rem = width // n_gpus, width % n_gpus
        shares = []
        cur = lo
        for i in range(n_gpus):
            size = base + (1 if i < rem else 0)
            if size <= 0:
                break
            shares.append((i, "%x" % cur, "%x" % (cur + size - 1)))
            cur += size

    if args.dry_run:
        print("# engine=%s puzzle=%d devices=%d shares=%d"
              % (engine, p.n, n_gpus, len(shares)))
        for i, s_lo, s_hi in shares:
            share = {"share_idx": i, "total_shares": len(shares),
                     "start_hex": s_lo, "end_hex": s_hi}
            runner.run_worker(engine, p, engine, share, device=None,
                              extra=args.extra, dry_run=True)
        return

    devices = [d["id"] for d in gpu_mod.devices()][:n_gpus] or [None] * n_gpus
    stop = threading.Event()
    print("scanning #%d [%s:%s] with %s on %d device(s) ..."
          % (p.n, start_hex, end_hex, engine, len(devices)))
    results = runner.scan_parallel(
        binary, p, engine,
        [{"share_idx": i, "total_shares": len(shares),
          "start_hex": s_lo, "end_hex": s_hi}
         for i, s_lo, s_hi in shares],
        stop_event=stop, devices=devices, extra=args.extra)
    for dev, idx, res in results:
        print("  device %-4s share %-3d -> %s" % (dev, idx, res))


def cmd_resume(args):
    p = registry.resolve_target(address=args.address, number=args.number)
    ck = ckpt.Checkpoint()
    recs = ck.returns_all(p.n)
    pend = ck.unresolved()
    pend_n = [r for r in pend if r.get("n") == p.n]
    if not pend_n:
        print("puzzle #%d has no unfinished shares." % p.n)
        return
    for r in pend_n:
        print("#%d share %d/%d status=%s engine=%s ckpt=%s"
              % (p.n, r.get("share_idx"), r.get("total_shares"),
                 r.get("status"), r.get("engine"), r.get("engine_ckpt")))
    print("\nnative checkpoint files (resume with the engine flags below):")
    for f in sorted(glob.glob(os.path.join(ckpt.SCAN_DIR, "%d_*.kc" % p.n))):
        print("  - %s" % f)
        print("    bitcrack: --continue %s" % os.path.abspath(f))
    for f in sorted(glob.glob(os.path.join(ckpt.WORK_DIR, "%d_*.work" % p.n))):
        print("  - %s" % os.path.abspath(f))
        in_path = os.path.join(ckpt.WORK_DIR, "in_%d_%s.txt"
                               % (p.n, os.path.basename(f).split("_")[1]))
        print("    kangaroo: -w %s -i %s"
              % (os.path.abspath(f), os.path.abspath(in_path)))


def cmd_found(args):
    files = sorted(glob.glob(os.path.join(ckpt.FOUND_DIR, "puzzle_*.txt")))
    if not files:
        print("no found keys yet.")
        return
    for f in files:
        print("=" * 60)
        with open(f, "r", encoding="utf-8") as fh:
            print(fh.read().strip())


def cmd_serve(args):
    from .cluster import protocol as cprotocol, scheduler as cscheduler
    from .cluster.manager import Coordinator
    from . import keyspace as ks_local
    from .telemetry import TelemetryStore
    p = registry.resolve_target(number=args.number)
    if p.solved:
        sys.exit("puzzle #%d is SOLVED; nothing to serve" % p.n)
    engine = args.engine or "auto"
    if engine == "auto":
        engine = "kangaroo" if p.regime == "R2" else "bitcrack"
    if engine == "kangaroo" and p.regime != "R2":
        sys.exit("kangaroo needs an exposed pubkey; #%d is R1 (use 'bitcrack')" % p.n)
    if engine == "bitcrack" and p.regime == "R2":
        print("WARN: %d has a pubkey but you chose bitcrack; kangaroo is better" % p.n,
              file=sys.stderr)
    if engine == "kangaroo":
        units = [cscheduler.Unit("%d:0" % p.n, p.n, engine,
                                p.lo_hex, p.hi_hex,
                                int(p.hi_hex, 16) - int(p.lo_hex, 16) + 1)]
    else:
        slices = ks_local.split_equal(p, args.units)
        units = cscheduler.build_units(p, engine, slices)
    scheduler = cscheduler.Scheduler(units, lease_ms=args.lease_ms)
    telemetry = TelemetryStore()
    telem_file = os.path.join(ckpt.STATE_DIR, "cluster_metrics.json")
    os.makedirs(ckpt.STATE_DIR, exist_ok=True)
    coord = Coordinator(args.token, scheduler, telemetry,
                        lease_ms=args.lease_ms)
    if args.extra:
        log.info("extra args %s available to node executors", args.extra)
    print("serving puzzle #%d [%s:%s] engine=%s units=%d on %s:%d ..."
          % (p.n, p.lo_hex, p.hi_hex, engine, len(units),
             args.host, args.port))
    coord.serve(host=args.host, port=args.port,
                certfile=args.tls_cert, keyfile=args.tls_key)


def cmd_node(args):
    from .cluster.node import WorkerNode, EngineExecutor
    slots = args.slots
    executor = EngineExecutor(args.engine, bin_dir=args.bin_dir,
                              extra=args.extra)
    node = WorkerNode(args.host, args.port, args.token,
                      name=args.name, slots=slots, executor=executor,
                      tls=args.tls)
    print("connecting to %s:%d as %s (%d slot(s)) ..."
          % (args.host, args.port, args.name, slots))
    node.run()


def cmd_dashboard(args):
    import json as _json
    try:
        import curses
    except ImportError:
        curses = None
    from .telemetry import render_dashboard
    path = os.path.join(ckpt.STATE_DIR, "cluster_metrics.json")
    if not os.path.exists(path):
        sys.exit("no metrics yet — run 'serve' first")
    last_snapshot = None
    while True:
        try:
            with open(path, "r", encoding="utf-8") as fh:
                snap = _json.load(fh)
            if curses and sys.stdout.isatty():
                os.system("cls" if os.name == "nt" else "clear")
                print(render_dashboard(snap))
            else:
                if snap != last_snapshot:
                    print(render_dashboard(snap))
                    last_snapshot = snap
            time.sleep(1)
        except KeyboardInterrupt:
            return


def cmd_cluster_status(args):
    import json as _json
    from .telemetry import render_dashboard
    path = os.path.join(ckpt.STATE_DIR, "cluster_metrics.json")
    if not os.path.exists(path):
        sys.exit("no metrics yet — run 'serve' first")
    with open(path, "r", encoding="utf-8") as fh:
        print(render_dashboard(_json.load(fh)))


def cmd_cluster_keygen(args):
    import secrets as _secrets
    import subprocess as _sp
    token = _secrets.token_urlsafe(32)
    print("CLUSTER_TOKEN=%s" % token)
    if args.tls:
        d = os.path.abspath(args.cert_dir)
        os.makedirs(d, exist_ok=True)
        key = os.path.join(d, "cluster-key.pem")
        cert = os.path.join(d, "cluster-cert.pem")
        if os.name == "nt" and not _which_openssl():
            sys.exit("openssl not found in PATH; install openssl first, or set --cert-dir "
                     "and run: openssl req -x509 -newkey rsa:2048 -nodes "
                     "-keyout %s -out %s -days 365 -subj '/CN=cluster'" % (key, cert))
        else:
            _sp.run(["openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes",
                      "-keyout", key, "-out", cert, "-days", "365",
                      "-subj", "/CN=cluster"], check=True)
            print("written: %s  %s" % (cert, key))


def _which_openssl():
    import shutil
    return shutil.which("openssl") is not None


# ------------------------------------------------------------------ entry

def build_parser():
    ap = argparse.ArgumentParser(prog="production.manager",
                                 description="Bitcoin-Puzzle production pipeline")
    sub = ap.add_subparsers(dest="cmd")

    s = sub.add_parser("status", help="verify puzzle status")
    s.add_argument("--chain", action="store_true",
                   help="also spot-check on-chain balances via mempool.space")
    s.add_argument("--timeout", type=int, default=20)
    s.set_defaults(fn=cmd_status)

    s = sub.add_parser("plan", help="rank unsolved puzzles by expected work")
    s.add_argument("--gpus", type=int)
    s.add_argument("--measured", type=float, help="measured keys/s to override defaults")
    s.add_argument("--limit", type=int)
    s.set_defaults(fn=cmd_plan)

    s = sub.add_parser("audit", help="dossier of one puzzle")
    s.add_argument("--address")
    s.add_argument("--number", type=int)
    s.add_argument("--gpus", type=int)
    s.set_defaults(fn=cmd_audit)

    s = sub.add_parser("gpus", help="list CUDA devices")
    s.set_defaults(fn=cmd_gpus)

    s = sub.add_parser("bench", help="measure real keys/s on a small window")
    s.add_argument("--address")
    s.add_argument("--number", type=int, default=71)
    s.add_argument("--bits", type=int, default=26)
    s.add_argument("--extra")
    s.set_defaults(fn=cmd_bench)

    s = sub.add_parser("scan", help="scan a puzzle across devices")
    s.add_argument("--address")
    s.add_argument("--number", type=int)
    s.add_argument("--engine", choices=["auto", "bitcrack", "kangaroo"], default="auto")
    s.add_argument("--gpus", type=int)
    s.add_argument("--start")
    s.add_argument("--end")
    s.add_argument("--extra")
    s.add_argument("--dry-run", action="store_true")
    s.set_defaults(fn=cmd_scan)

    s = sub.add_parser("resume", help="list/resume unfinished shares")
    s.add_argument("--address")
    s.add_argument("--number", type=int)
    s.set_defaults(fn=cmd_resume)

    s = sub.add_parser("found", help="show verified found keys")
    s.set_defaults(fn=cmd_found)

    # ---- cluster commands ----
    s = sub.add_parser("serve", help="start coordinator for remote GPU nodes")
    s.add_argument("--host", default="0.0.0.0")
    s.add_argument("--port", type=int, default=25200)
    s.add_argument("--token", required=True)
    s.add_argument("--number", type=int, required=True, help="puzzle to distribute")
    s.add_argument("--engine", choices=["auto", "bitcrack", "kangaroo"], default="auto")
    s.add_argument("--units", type=int, default=8, help="R1 slice count (ignored for R2)")
    s.add_argument("--lease-ms", type=int, default=60000)
    s.add_argument("--tls-cert")
    s.add_argument("--tls-key")
    s.add_argument("--extra")
    s.set_defaults(fn=cmd_serve)

    s = sub.add_parser("node", help="start GPU worker node (connects to serve)")
    s.add_argument("--host", required=True, help="coordinator address")
    s.add_argument("--port", type=int, default=25200)
    s.add_argument("--token", required=True)
    s.add_argument("--name", default="worker")
    s.add_argument("--slots", type=int, default=1)
    s.add_argument("--engine", choices=["auto", "bitcrack", "kangaroo"], default="auto")
    s.add_argument("--bin-dir")
    s.add_argument("--tls", action="store_true")
    s.add_argument("--extra")
    s.set_defaults(fn=cmd_node)

    s = sub.add_parser("dashboard", help="live cluster dashboard (refreshing)")
    s.set_defaults(fn=cmd_dashboard)

    s = sub.add_parser("cluster-status", help="one-shot cluster metrics from state/")
    s.set_defaults(fn=cmd_cluster_status)

    s = sub.add_parser("cluster-keygen", help="generate cluster auth token + optional TLS cert")
    s.add_argument("--tls", action="store_true", help="generate self-signed cert via openssl")
    s.add_argument("--cert-dir", default=".", help="output directory for key/cert files")
    s.set_defaults(fn=cmd_cluster_keygen)

    return ap


def main(argv=None):
    args = build_parser().parse_args(argv)
    if not getattr(args, "cmd", None):
        build_parser().print_help()
        return 1
    args.fn(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())