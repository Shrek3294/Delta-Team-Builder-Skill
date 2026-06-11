"""Tests for tools/lint_team.py. Run: python -m pytest tools/tests/ -q

Covers: clean pass, one poisoned team per HARD check, alias-map + ban-alias
resolution against live data, and the hash-bound verifier sidecar gate.
"""
import os
import sys
import hashlib

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import tools.lint_team as L  # noqa: E402

DATA = L.Data()

HEADER = "| Pokemon | Item | Ability | Moves | Role |\n|---|---|---|---|---|\n"


def team(*rows):
    """Build a deliverable with a team table + minimal identity section."""
    body = HEADER + "".join(rows)
    return "## Team identity\n\nA test team.\n\n" + body


def row(pokemon, item, ability, moves, role="glue"):
    return "| %s | %s | %s | %s | %s |\n" % (pokemon, item, ability, moves, role)


# Known-legal Tinkaton-Gamma set (verified against data/mons/tinkaton-gamma.json).
CLEAN_ROW = row("Tinkaton-Gamma", "Heavy-Duty Boots", "Parasol Prayer",
                "Double-Edge, Fly, Play Rough, Facade")


# ---------- clean ----------

def test_clean_team_passes():
    res = L.lint_text(team(CLEAN_ROW), data=DATA)
    assert res.ok, res.report()


def test_real_delivered_team_passes():
    path = os.path.join(L.ROOT, "teams", "azelf-eterrain-offense.md")
    if not os.path.exists(path):
        pytest.skip("sample team not present")
    res = L.lint_file(path, require_verify=False, data=DATA)
    assert res.ok, res.report()


# ---------- one poisoned team per HARD check ----------

def test_illegal_move_fails():
    res = L.lint_text(team(row("Tinkaton-Gamma", "Heavy-Duty Boots", "Parasol Prayer",
                               "Hydro Pump, Fly, Play Rough, Facade")), data=DATA)
    assert any("illegal move" in h and "Hydro Pump" in h for h in res.hard), res.report()


def test_illegal_ability_fails():
    res = L.lint_text(team(row("Tinkaton-Gamma", "Heavy-Duty Boots", "Levitate",
                               "Double-Edge, Fly, Play Rough, Facade")), data=DATA)
    assert any("illegal ability" in h for h in res.hard), res.report()


def test_banned_mon_fails():
    res = L.lint_text(team(row("Gholdengo", "Choice Scarf", "Good as Gold",
                               "Make It Rain, Shadow Ball, Thunderbolt, Trick")), data=DATA)
    assert any("banned mon" in h for h in res.hard), res.report()


def test_legal_sibling_of_banned_mon_passes_ban_check():
    # Gholdengo-Delta is legal even though Gholdengo is banned.
    assert DATA.is_banned("Gholdengo", DATA.resolve("Gholdengo")) is True
    assert DATA.is_banned("Gholdengo-Delta", DATA.resolve("Gholdengo-Delta")) is False


def test_tera_line_fails():
    t = team(CLEAN_ROW) + "\n\nTera Type: Fairy\n"
    res = L.lint_text(t, data=DATA)
    assert any("Tera" in h for h in res.hard), res.report()


def test_terapagos_does_not_trip_tera():
    # 'Terapagos-ATOM' in prose must not be read as a Tera line.
    t = team(CLEAN_ROW) + "\n\nTerapagos-ATOM is a strong pick.\n"
    res = L.lint_text(t, data=DATA)
    assert not any("Tera line" in h for h in res.hard), res.report()


def test_em_dash_fails():
    t = team(CLEAN_ROW) + "\n\nThis team is fast — very fast.\n"
    res = L.lint_text(t, data=DATA)
    assert any("dash" in h for h in res.hard), res.report()


def test_customer_language_fails():
    t = team(CLEAN_ROW) + "\n\nAs requested, here is your team.\n"
    res = L.lint_text(t, data=DATA)
    assert any("customer" in h.lower() for h in res.hard), res.report()


def test_unresolvable_species_fails():
    res = L.lint_text(team(row("Notamon-Fake", "Leftovers", "Levitate",
                               "Tackle, Tackle, Tackle, Tackle")), data=DATA)
    assert any("unresolvable species" in h for h in res.hard), res.report()


def test_item_lock_mismatch_fails():
    # Deltatyphlosium Z is locked to Typhlosion-Delta.
    res = L.lint_text(team(row("Tinkaton-Gamma", "Deltatyphlosium Z", "Parasol Prayer",
                               "Double-Edge, Fly, Play Rough, Facade")), data=DATA)
    assert any("item lock" in h for h in res.hard), res.report()


def test_data_gap_move_allowed():
    # Corviknight Roost/Defog are missing from JSON but allowlisted.
    res = L.lint_text(team(row("Corviknight", "Leftovers", "Pressure",
                               "Roost, Defog, U-turn, Body Press", "wall")), data=DATA)
    assert res.ok, res.report()


# ---------- alias map + ban alias ----------

@pytest.mark.parametrize("name,stem", [
    ("Mega Flygon", "mega-flygon"),      # mega- prefix file
    ("Gengar-Mega", "gengar-mega"),      # -mega suffix file
    ("Mega Gengar", "gengar-mega"),      # token-set order independence
    ("Mega Scizor", "scizor-mega"),
    ("Tinkaton-Gamma", "tinkaton-gamma"),
    ("Terapagos-ATOM", "terapagos-atom"),
])
def test_alias_resolution(name, stem):
    assert DATA.resolve(name) == stem


@pytest.mark.parametrize("name,banned", [
    ("Mega Raichu-Y", True),     # banlist says 'Raichu-Mega-Y'
    ("Mega Alakazam", True),     # banlist says 'Alakazam-Mega'
    ("Flutter Mane", True),
    ("Urshifu-Single-Strike", True),
    ("Urshifu-Rapid-Strike", False),
    ("Tinkaton-Gamma", False),
])
def test_ban_alias(name, banned):
    assert DATA.is_banned(name, DATA.resolve(name)) is banned


def test_no_alias_collisions():
    assert DATA.alias_collisions == [], DATA.alias_collisions


def test_banlist_parser_nonempty():
    assert len(DATA.ban_collapsed) > 20


# ---------- verifier sidecar (hash-bound) ----------

def _write(tmp_path, text):
    p = tmp_path / "team.md"
    p.write_text(text, encoding="utf-8")
    return str(p)


def _sidecar(tmp_path, content):
    s = tmp_path / "team.verify.md"
    s.write_text(content, encoding="utf-8")
    return str(s)


def test_sidecar_missing_fails(tmp_path):
    p = _write(tmp_path, team(CLEAN_ROW))
    res = L.lint_file(p, require_verify=True, data=DATA)
    assert any("sidecar missing" in h for h in res.hard), res.report()


def test_sidecar_empty_fails(tmp_path):
    p = _write(tmp_path, team(CLEAN_ROW))
    _sidecar(tmp_path, "   \n")
    res = L.lint_file(p, require_verify=True, data=DATA)
    assert any("empty" in h for h in res.hard), res.report()


def test_sidecar_stale_hash_fails(tmp_path):
    p = _write(tmp_path, team(CLEAN_ROW))
    wrong = hashlib.sha256(b"different content").hexdigest()
    _sidecar(tmp_path, "source-sha256: %s\n\nfindings: none\n" % wrong)
    res = L.lint_file(p, require_verify=True, data=DATA)
    assert any("stale" in h for h in res.hard), res.report()


def test_sidecar_matching_hash_passes(tmp_path):
    text = team(CLEAN_ROW)
    p = _write(tmp_path, text)
    good = hashlib.sha256(open(p, "rb").read()).hexdigest()
    _sidecar(tmp_path, "source-sha256: %s\n\nfindings: none, all verified\n" % good)
    res = L.lint_file(p, require_verify=True, data=DATA)
    assert res.ok, res.report()
