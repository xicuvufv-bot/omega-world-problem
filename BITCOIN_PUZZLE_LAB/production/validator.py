"""Offline key verification: found privkey -> pubkey -> address comparison.

Every candidate key found by BitCrack/Kangaroo MUST pass this check before it
is written anywhere. Nothing here touches the network; all math is local
stdlib (reuses the lab's ``algorithms.curve`` / ``algorithms.hash``).

Also builds WIF (compressed + uncompressed) so the winner can spend with any
standard wallet tooling. Spending/broadcasting itself is intentionally NOT
implemented here.
"""

import hashlib
import os
import sys

try:
    from algorithms.curve import scalar_mult, compressed, to_affine, P
    from algorithms.hash import hash160
except ImportError:  # allow running from inside production/ regardless of cwd
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from algorithms.curve import scalar_mult, compressed, to_affine, P
    from algorithms.hash import hash160


class ValidationError(ValueError):
    pass


# ---- base58 (Bitcoin alphabet) ------------------------------------------

_B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def _b58encode(b):
    n = int.from_bytes(b, "big")
    out = ""
    while n:
        n, r = divmod(n, 58)
        out = _B58[r] + out
    pad = 0
    for byte in b:
        if byte == 0:
            pad += 1
        else:
            break
    return "1" * pad + (out or "")


def _b58check(payload):
    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    return _b58encode(payload + checksum)


# ---- private-key -> artifacts --------------------------------------------

def privkey_bytes_from_hex(hexkey):
    """Accept any unpadded hex int; normalize to 32 bytes."""
    try:
        k = int(hexkey, 16)
    except ValueError:
        raise ValidationError("candidate is not hex: %r" % hexkey)
    if not 1 <= k < P:
        raise ValidationError("candidate out of secp256k1 range: %s" % hexkey)
    return k


def uncompressed_pubkey_hex(k):
    x, y = to_affine(scalar_mult(k))
    return "04" + "%064x" % x + "%064x" % y


def derive_points(k):
    jac = scalar_mult(k)
    comp = compressed(jac)
    uncomp = bytes([4]) + jac[0].to_bytes(32, "big") + jac[1].to_bytes(32, "big")
    return comp, uncomp


def hash_from_pub(pub_bytes):
    return hash160(pub_bytes)


def address_from_hash(h):
    return _b58check(b"\x00" + h)


def wif_from_key(k, compressed_flag):
    payload = b"\x80" + k.to_bytes(32, "big")
    if compressed_flag:
        payload += b"\x01"
    return _b58check(payload)


# ---- full verification ---------------------------------------------------

def verify_candidate(hexkey, target_address):
    """Return a dict of artifacts for a key whose hash160 matches target.

    Raises ValidationError if the key does NOT derive the target address
    (union over compressed + uncompressed), or if it is out of range.
    """
    k = privkey_bytes_from_hex(hexkey)
    comp, uncomp = derive_points(k)
    hc, hu = hash_from_pub(comp), hash_from_pub(uncomp)
    ac, au = address_from_hash(hc), address_from_hash(hu)

    matched = "compressed" if ac == target_address else (
        "uncompressed" if au == target_address else None)
    if matched is None:
        raise ValidationError(
            "candidate 0x%064x does NOT derive %s (comp=%s uncomp=%s)"
            % (k, target_address, ac, au))

    privhex = "%064x" % k
    return {
        "privkey_hex": privhex,
        "privkey_int": k,
        "puzzle_address": target_address,
        "matched_form": matched,
        "compressed_address": ac,
        "uncompressed_address": au,
        "compressed_pubkey": comp.hex(),
        "uncompressed_pubkey": uncomp.hex(),
        "wif_compressed": wif_from_key(k, True),
        "wif_uncompressed": wif_from_key(k, False),
    }


def verify_found_file(path, target_address):
    lines = []
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line and not line.startswith("#"):
                lines.append(line)
    results = []
    for line in lines:
        tok = line.split()
        hexkey = tok[-1] if tok else ""
        try:
            results.append(verify_candidate(hexkey, target_address))
        except ValidationError as e:
            results.append({"error": str(e)})
    return results