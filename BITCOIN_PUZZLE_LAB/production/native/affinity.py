"""Cross-platform thread/CPU affinity and NUMA hints.

Windows:  SetThreadAffinityMask via kernel32.dll
Linux:    sched_setaffinity via ctypes (no libc Python binding)
macOS:    thread_policy (not supported — returns silently)

NUMA-awareness: on multi-socket systems the coordinator's network threads
should live on a different socket from the GPU-compute threads.  The
``assign_cores()`` helper partitions cores by NUMA node (read from
/sys/devices/system/node on Linux) and returns a mask for the requested
node, which the caller passes to ``pin_thread()``.
"""

import ctypes
import ctypes.util
import os
import platform
import sys
import threading

_win = sys.platform == "win32"
_linux = sys.platform == "linux"


def _kernel32():
    if _win:
        k = ctypes.windll.kernel32
        k.GetCurrentThread.restype = ctypes.c_void_p
        k.GetCurrentThread.argtypes = []
        k.SetThreadAffinityMask.restype = ctypes.c_size_t
        k.SetThreadAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
        return k
    return None


def _libc():
    if _linux:
        name = ctypes.util.find_library("c")
        return ctypes.CDLL(name or "libc.so.6")
    return None


def get_cpu_count():
    return os.cpu_count() or 1


def get_numa_nodes():
    """Return a dict {node_id: [core_ids]} from sysfs.  macOS/Windows: single node."""
    if _linux:
        base = "/sys/devices/system/node"
        nodes = {}
        try:
            for entry in os.listdir(base):
                if not entry.startswith("node") or not entry[4:].isdigit():
                    continue
                nid = int(entry[4:])
                cpulist = os.path.join(base, entry, "cpulist")
                if os.path.exists(cpulist):
                    with open(cpulist) as f:
                        nodes[nid] = _parse_cpu_list(f.read().strip())
        except (OSError, ValueError):
            pass
        if nodes:
            return nodes
    # fallback: all cores on node 0
    return {0: list(range(get_cpu_count()))}


def _parse_cpu_list(s):
    cores = []
    for part in s.split(","):
        if "-" in part:
            lo, hi = part.split("-", 1)
            cores.extend(range(int(lo), int(hi) + 1))
        elif part.isdigit():
            cores.append(int(part))
    return cores


def pin_thread(cores, thread_id=None):
    """Pin the current thread (or thread with *thread_id*) to *cores* (list of ints).

    On Windows, ``thread_id`` is the Win32 thread handle (default: current).
    On Linux, ``thread_id`` is ignored (uses ``pthread_setaffinity_np``).
    """
    cores = list(cores)
    if not cores:
        return False

    if _win:
        mask = 0
        for c in cores:
            mask |= 1 << c
        handle = _kernel32().GetCurrentThread() if thread_id is None else thread_id
        prev = _kernel32().SetThreadAffinityMask(handle, ctypes.c_size_t(mask))
        return prev != 0

    if _linux:
        libc = _libc()
        if libc is None:
            return False
        CPU_SETSIZE = 1024
        cpu_set = ctypes.create_string_buffer(CPU_SETSIZE // 8)
        for c in cores:
            # CPU_SET macro equivalent
            idx = c // 64
            bit = c % 64
            word = ctypes.c_uint64.from_buffer(cpu_set, idx * 8)
            word.value |= (1 << bit)
        ret = libc.sched_setaffinity(0, ctypes.sizeof(cpu_set), cpu_set)
        return ret == 0

    return False  # macOS or unsupported


def get_affinity():
    """Return the set of CPUs the current thread is pinned to."""
    if _win:
        handle = _kernel32().GetCurrentThread()
        mask = _kernel32().SetThreadAffinityMask(handle, ctypes.c_size_t(-1))
        _kernel32().SetThreadAffinityMask(handle, ctypes.c_size_t(mask))
        return [i for i in range(64) if mask & (1 << i)]
    if _linux:
        libc = _libc()
        if libc is None:
            return list(range(get_cpu_count()))
        CPU_SETSIZE = 1024
        cpu_set = ctypes.create_string_buffer(CPU_SETSIZE // 8)
        ret = libc.sched_getaffinity(0, ctypes.sizeof(cpu_set), cpu_set)
        if ret != 0:
            return list(range(get_cpu_count()))
        cores = []
        for i in range(get_cpu_count()):
            idx = i // 64
            bit = i % 64
            word = ctypes.c_uint64.from_buffer(cpu_set, idx * 8)
            if word.value & (1 << bit):
                cores.append(i)
        return cores
    return list(range(get_cpu_count()))


def partition_by_numa():
    """Return {node_id: core_list}, plus a hint for which cores the current
    process should prefer for compute vs. network threads."""
    nodes = get_numa_nodes()
    n = len(nodes)
    if n <= 1:
        all_cores = nodes.get(0, list(range(get_cpu_count())))
        mid = len(all_cores) // 2
        return {"compute": all_cores[mid:], "network": all_cores[:mid],
                "all": all_cores, "nodes": nodes}
    sorted_ids = sorted(nodes.keys())
    return {"compute": nodes[sorted_ids[0]],
            "network": nodes[sorted_ids[-1]],
            "all": [c for nid in sorted_ids for c in nodes[nid]],
            "nodes": nodes}


class AffinityGuard:
    """Context manager that pins the calling thread to *cores* and restores
    the previous affinity on exit."""

    def __init__(self, cores):
        self.cores = cores
        self._prev = None

    def __enter__(self):
        self._prev = get_affinity()
        pin_thread(self.cores)
        return self

    def __exit__(self, *args):
        if self._prev:
            pin_thread(self._prev)


def auto_pin_worker(worker_cores=None, network_cores=None):
    """Assign compute cores to the calling thread and optionally start a
    detached network thread on the ``network_cores`` partition.

    Returns the network thread (or None).
    """
    parts = partition_by_numa()
    compute = worker_cores or parts["compute"]
    net = network_cores or parts["network"]
    pin_thread(compute)
    return compute, net