# CONJECTURES — open, currently UNPROVEN (do not treat as fact)

1. **Near-max-trace j=0 family is structurally special but NOT easy.**
   t = p+1-l = 131005 lies within ~65 below the supersingular boundary 2√p. All known
   results say ordinary curves in this slab still need √N for DLP; the slab is under-
   explored *algebraically* (degenerate CM ring). Conjecture: no sub-sqrt DLP exists in
   this slab. STATUS: open, consistent with all data; no route to a proof here.

2. **Shared-G amortization is the only "free lunch" the bench offers.**
   The多久 the lab reuses one base point, batch-BSGS amortization is available; beyond
   that the instance family is generic. STATUS: supported by E2 and reproduction, but
   only at the constant level.

3. **Alpha is 0.5 for every black-box solver on this family.**
   Supported by bsgs α=0.494 R²=0.9997 and by rho/kanga failing to go below. This is the
   generic model; treating it as a universal law for this family is a conjecture, not a
   theorem we proved in this session.

4. **Any new sub-sqrt method must break genericity (not speed up BSGS).**
   Either exploit something not yet seen (units of the CM order beyond the cube root,
   twist structure, specific lucky representation) or be a hallucinated claim. All today's
   probes found nothing at depth ≤ 1 endomorphism.