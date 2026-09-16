"""Tests for the production pipeline modules.

Run from the lab root:  python -m pytest production/tests -q
"""

import os

import pytest

from production import registry, keyspace, strategy, validator, runner, checkpoint


# ---------------------------------------------------------------- registry

def test_registry_shape():
    assert registry.summary()["total"] == 160
    assert registry.summary()["solved"] == 83
    assert registry.summary()["unsolved"] == 77
    r1, r2 = registry.unsolved_by_regime()
    assert len(r1) == 72
    assert len(r2) == 5


def test_registry_rejects_arbitrary_address():
    with pytest.raises(registry.RegistryError):
        registry.get_by_address("1BitcoinEaterAddressDontSendf59kuE")


def test_registry_rejects_unknown_number():
    with pytest.raises(registry.RegistryError):
        registry.resolve_target(number=999)


def test_next_targets():
    assert registry.get_by_number(71).regime == "R1"
    assert registry.get_by_number(71).address == "1PWo3JeB9jrGwfHDNpdGK54CRas7fsVzXU"
    assert registry.get_by_number(140).regime == "R2"
    assert registry.get_by_number(140).pubkey


# ---------------------------------------------------------------- keyspace

def test_split_equal_exhausts_interval():
    p = registry.get_by_number(71)
    shares = keyspace.split_equal(p, 8)
    assert shares[0][1] == p.lo_hex
    assert shares[-1][2] == p.hi_hex
    total_width = sum(int(e, 16) - int(s, 16) + 1 for _, s, e in shares)
    assert total_width == p.width


def test_subrange_must_stay_inside():
    p = registry.get_by_number(71)
    with pytest.raises(registry.RegistryError):
        keyspace.validate_subrange(p, "0", p.hi_hex)


# ---------------------------------------------------------------- strategy

def test_plan_sorted_and_sane():
    plans = strategy.plan(registry.unsolved(), gpu_count=4)
    assert len(plans) == 77
    assert plans[0]["n"] == 140          # cheapest by est. seconds
    times = [p["seconds"] for p in plans]
    assert times == sorted(times)


def test_feasibility_honest():
    p = registry.get_by_number(71)
    est = strategy.estimate(p)
    assert est["engine"] == "bitcrack"
    assert est["gpu_years"] > 1000        # no false night-and-day promise


# ---------------------------------------------------------------- validator

def test_verify_published_solved_keys():
    # Puzzle #1  : key = 1
    a1 = registry.get_by_number(1)
    v1 = validator.verify_candidate("1", a1.address)
    assert v1["privkey_hex"] == "01".rjust(64, "0")
    assert v1["matched_form"] == "compressed"
    # Puzzle #2  : key = 3
    v2 = validator.verify_candidate("3", registry.get_by_number(2).address)
    assert v2["privkey_hex"].endswith("03")
    # Puzzle #66 : published key
    v66 = validator.verify_candidate(
        "2832ed74f2b5e35ee",
        registry.get_by_number(66).address)
    assert v66["matched_form"] in ("compressed", "uncompressed")


def test_validator_rejects_wrong_key():
    p = registry.get_by_number(71)
    with pytest.raises(validator.ValidationError):
        validator.verify_candidate("0000000000000000000000000000000000000000000000000000000000000001",
                                   p.address)


def test_wif_well_formed():
    v = validator.verify_candidate("1", registry.get_by_number(1).address)
    assert v["wif_compressed"][0] == "K" or v["wif_compressed"][0] == "L"
    assert v["wif_uncompressed"][0] == "5"


# ---------------------------------------------------------------- runner

def test_bitcrack_cmd_shape():
    p = registry.get_by_number(71)
    share = {"start_hex": "400000000000000000", "end_hex": "400000000000000001"}
    cmd = runner.build_bitcrack_cmd("cuBitCrack", p, share, 0, "c.kc",
                                    "t.txt", None)
    assert "--keyspace" in cmd and "400000000000000000:400000000000000001" in cmd
    assert "--continue" in cmd and "-d" in cmd


def test_kangaroo_input_r2_only():
    p = registry.get_by_number(140)
    share = {"start_hex": "0000", "end_hex": "ffff", "share_idx": 0}
    path = runner.write_kangaroo_input(p, share)
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    assert lines[2] == p.pubkey
    os.remove(path)


# ---------------------------------------------------------------- checkpoint

def test_checkpoint_claim_touch(tmp_path):
    ck = checkpoint.Checkpoint(os.path.join(str(tmp_path), "ledger.json"))
    rec = ck.claim(71, 0, 1, "a", "b", "bitcrack")
    assert rec["status"] == "claimed"
    ck.touch(rec, status="running")
    assert ck.returns("bitcrack", 71, 0)["status"] == "running"
    assert len(ck.unresolved()) == 1


def test_bitcrack_continue_parse(tmp_path):
    f = os.path.join(str(tmp_path), "x.kc")
    with open(f, "w", encoding="utf-8") as fh:
        fh.write("==PROGRESS==\nStart key : 0x400000000000000000\n"
                 "End key   : 0x4fffffffffffffffff\n"
                 "Next key  : 0x410000000000000000\n")
    info = checkpoint.read_bitcrack_continue(f)
    assert info["start"] == "0x400000000000000000"
    assert info["next"] == "0x410000000000000000"