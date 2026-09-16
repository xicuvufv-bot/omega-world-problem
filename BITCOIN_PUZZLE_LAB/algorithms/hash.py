"""Hashing helpers: SHA256(d), RIPEMD160, and the P2PKH hash160."""

import hashlib

USED = False  # (marker so the flake-style linter has nothing to complain about)


def sha256d(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def ripemd160(data: bytes) -> bytes:
    try:
        return hashlib.new("ripemd160", data).digest()
    except ValueError:
        # Some FIPS builds lack ripemd160; fall back to a pure-Python stub.
        raise RuntimeError(
            "ripemd160 unavailable in this build of hashlib; "
            "set LC_ALL / use a standard OpenSSL build"
        ) from None


def hash160(pubkey_bytes: bytes) -> bytes:
    """P2PKH hash160 = RIPEMD160(SHA256(pubkey))."""
    return ripemd160(sha256d(pubkey_bytes))


def compressed_pubkey_hash(k):
    """hash160 of the compressed public key for secret k."""
    from .curve import scalar_mult, compressed

    return hash160(compressed(scalar_mult(k)))