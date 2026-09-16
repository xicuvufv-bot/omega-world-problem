"""Shared fixtures for the Bitcoin Puzzle Lab test suite."""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from algorithms.curve import scalar_mult, to_affine, compressed, Gx, Gy, P, N
from algorithms.hash import hash160

import pytest

KNOWN_VECTORS = [
    (1, Gx, Gy),
    (3, 0xf9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f9,
          0x388f7b0f632de8140fe337e62a37f3566500a99934c2231b6cb9fd7584b8e672),
    (6, 0xff206757a898362124a45645c7b6c53b237730de1ee1800aa322ce93890d6e01,
          0xf12375498a58c167648784028305a5c2a4892df46f03ceabf2a9d797a6b50f1e),
]


@pytest.fixture
def secp256k1():
    return dict(p=P, n=N, Gx=Gx, Gy=Gy)
