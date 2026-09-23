# -*- coding: utf-8 -*-
"""probe_sig.py — print inspect.signature for every public solver fn actually
imported by the engine pickup (research root solvers) so verify_engine smoke
calls match the real API."""
import io, os, sys
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
sys.path[:0] = [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]  # research root
import inspect
import solvers, gen, fit, classify
for mod in (solvers, gen, fit, classify):
    print("##", getattr(mod, "__file__", "?"))
    for name in dir(mod):
        if name.startswith("_"):
            continue
        obj = getattr(mod, name)
        if callable(obj) and getattr(obj, "__module__", "") == mod.__name__:
            try:
                sig = inspect.signature(obj)
            except Exception as e:
                sig = "<sig err %s>" % e
            try:
                firstdoc = (obj.__doc__ or "").strip().splitlines()
                d1 = firstdoc[0][:70] if firstdoc else ""
            except Exception:
                d1 = ""
            print("   %-10s %s   %s" % (name, sig, d1))
print("SMOKE CONSTANTS gen:", getattr(gen, "TOY_P", "?"), getattr(gen, "TOY_L", "?"), getattr(gen, "TOY_G", "?"))
