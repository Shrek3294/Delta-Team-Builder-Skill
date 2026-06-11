"""
DeltaCalc damage engine - faithful Python port of the in-game Kotlin engine
(Z:\\Cb delta\\DeltaCalc\\src\\main\\kotlin\\com\\cobblemonextendedbattleui\\calc\\DamageEngine.kt).

CLI for the paid Delta ranked team-building workflow. Reads species/move/typing
data from this workspace's data/ directory.

Faithfulness over idiomatic Python: floor/int truncation, modifier ordering,
and ability/item handling all mirror the Kotlin source. Where the Kotlin
behavior is opaque or depends on runtime battle state, the Python falls
through to 1.0x and the warning is surfaced.

# Delta-specific overrides — Pokemon Champions nerfs are MIXED in delta
# ----------------------------------------------------------------------
# As of 2026-05-14, the Champs balance changes have only PARTIALLY landed in
# Cobblemon Delta ranked. Treat the two groups below as separate concerns
# when refreshing this calc.
#
# DID propagate to delta (use Champs values):
#   - Sleep: capped at 1-2 turns (server patch quote, brickchef msg
#     1501590026319036478 on 5/06).
#   - Paralysis: full-para chance is 12.5%, NOT 25% (Champs value).
#   - Freeze: 25% thaw chance per turn (Champs value).
#   ※ This calc does not currently model status secondary-effect probability,
#     but if you ever extend it (e.g. para-chance-into-KO odds, sleep-turn
#     expectation), use the Champs numbers, not vanilla.
#
# DID NOT propagate to delta (use ORIGINAL pre-Champs values):
#   - Salt Cure: original BP / scaling. Invin clarified "Just cuz they
#     nerfed Salt Cure" (msg 1501952017369923635); Bb Greninja's Iai Slash
#     derives from Salt Cure but the derivative is also unaffected.
#   - Moonblast: 95 BP / 100 acc / 30% SpA-drop (original). The 10%
#     SpA-drop Champs nerf is NOT in delta (Lab msg 1501954515962826945).
#   - Leech Seed: not affected by the status patch (brickchef confirmation).
#
# When refreshing this calc against future Kotlin source, audit BOTH lists.
# If a future delta patch propagates Salt Cure / Moonblast nerfs, update
# notes/balance_history.md AND notes/discord-sentiment.md first, then this
# header, then the move table.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Paths / data loading
# ---------------------------------------------------------------------------

WORKSPACE = Path(__file__).resolve().parent.parent  # .../Delta team building
MONS_DIR = WORKSPACE / "data" / "mons"
TYPE_CHART_PATH = WORKSPACE / "data" / "type-chart.json"
TEAM_BUILDER_PATH = WORKSPACE / "data" / "team-builder.json"


def normalize_token(value: Optional[str]) -> str:
    """Mirror Kotlin's normalizeToken: lowercase, strip space/-/_/'/. ."""
    if not value:
        return ""
    return (
        value.lower()
        .replace(" ", "")
        .replace("-", "")
        .replace("_", "")
        .replace("'", "")
        .replace(".", "")
    )


_TYPE_CHART_CACHE: Optional[dict] = None


def load_type_chart() -> dict:
    global _TYPE_CHART_CACHE
    if _TYPE_CHART_CACHE is None:
        with open(TYPE_CHART_PATH, "r", encoding="utf-8") as f:
            _TYPE_CHART_CACHE = json.load(f)
    return _TYPE_CHART_CACHE


def type_multiplier(attacking_type: str, defending_type: str) -> float:
    """Lookup non-neutral entries; default 1.0."""
    chart = load_type_chart()["chart"]
    atk = attacking_type.lower()
    deft = defending_type.lower()
    entry = chart.get(atk)
    if not entry:
        return 1.0
    for mult_str, types in entry.items():
        if deft in [t.lower() for t in types]:
            return float(mult_str)
    return 1.0


_TEAM_BUILDER_CACHE: Optional[dict] = None


def load_team_builder() -> dict:
    global _TEAM_BUILDER_CACHE
    if _TEAM_BUILDER_CACHE is None:
        with open(TEAM_BUILDER_PATH, "r", encoding="utf-8") as f:
            _TEAM_BUILDER_CACHE = json.load(f)
    return _TEAM_BUILDER_CACHE


def find_team_builder_entry(display_name: str) -> Optional[dict]:
    """Look up a mon by display name in team-builder.json (fallback for forms)."""
    tb = load_team_builder()
    target = normalize_token(display_name)
    for entry in tb.get("entries", []):
        if normalize_token(entry.get("name")) == target:
            return entry
    return None


def species_filename(name: str) -> str:
    """Map display name 'Tinkaton-Gamma' -> 'tinkaton-gamma.json'."""
    # Replace spaces with hyphen, lowercase, keep existing hyphens.
    slug = name.strip().lower().replace(" ", "-")
    # Collapse any duplicate hyphens.
    slug = re.sub(r"-+", "-", slug)
    return slug + ".json"


@dataclass
class MonData:
    species_key: str
    display_name: str
    types: list[str]
    abilities: list[str]
    base_stats: dict  # hp/atk/def/spa/spd/spe
    weight_kg: Optional[float]
    legal_moves: list[dict]


def load_mon(name: str) -> MonData:
    """Load a mon by display name. Falls back to team-builder.json for forms."""
    fname = species_filename(name)
    path = MONS_DIR / fname
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        species = raw.get("species", {}) or {}
        types = [t.lower() for t in (species.get("types") or [])]
        base_stats = species.get("baseStats") or {}
        legal_moves = raw.get("legalMoves") or []
        # If the file is a stub (e.g. mega-flygon with empty legalMoves),
        # backfill legalMoves from team-builder rawContent if necessary.
        # For now, just return what we have; signature moves are handled separately.
        return MonData(
            species_key=species.get("speciesKey") or normalize_token(name),
            display_name=species.get("displayName") or name,
            types=types,
            abilities=list(species.get("abilities") or []),
            base_stats={k: int(v) for k, v in base_stats.items()},
            weight_kg=species.get("weightKg"),
            legal_moves=legal_moves,
        )
    # Fallback: team-builder.json
    entry = find_team_builder_entry(name)
    if entry is None:
        print(f"ERROR: species not found. searched '{fname}' and team-builder.json for '{name}'.", file=sys.stderr)
        sys.exit(1)
    forms = entry.get("forms") or []
    base_form = forms[0] if forms else {}
    types = [t.lower() for t in (base_form.get("types") or [])]
    abilities_block = base_form.get("abilities") or {}
    abilities: list[str] = []
    for key in ("primary", "secondary", "hidden"):
        v = abilities_block.get(key)
        if v:
            abilities.append(v)
    abilities.extend(abilities_block.get("extra") or [])
    stats = base_form.get("stats") or {}
    # team-builder.json stats keys are HP/Atk/Def/SpAtk/SpDef/Speed (case-varied)
    def pick(*keys: str) -> int:
        for k in keys:
            if k in stats:
                return int(stats[k])
            lk = k.lower()
            for sk, sv in stats.items():
                if sk.lower() == lk:
                    return int(sv)
        return 0
    base_stats = {
        "hp": pick("HP", "hp"),
        "atk": pick("Atk", "atk", "Attack"),
        "def": pick("Def", "def", "Defense"),
        "spa": pick("SpAtk", "spa", "SpA", "Sp.Atk", "SpecialAttack"),
        "spd": pick("SpDef", "spd", "SpD", "Sp.Def", "SpecialDefense"),
        "spe": pick("Speed", "spe", "Spe"),
    }
    return MonData(
        species_key=normalize_token(name),
        display_name=entry.get("name") or name,
        types=types,
        abilities=abilities,
        base_stats=base_stats,
        weight_kg=None,
        legal_moves=[],
    )


# ---------------------------------------------------------------------------
# Move lookup
# ---------------------------------------------------------------------------

@dataclass
class Move:
    move_id: str
    display_name: str
    type_name: str
    category: str  # "physical" | "special" | "status"
    base_power: int
    priority: int = 0


# Signature/custom move entries that the engine needs but may not be in legalMoves
# (e.g. Updraft on Tinkaton-Gamma has null type in legalMoves). Keyed by normalized
# move id. Sourced from team-builder.json signature move descriptions.
CUSTOM_MOVE_OVERRIDES: dict[str, Move] = {
    # Tinkaton-Gamma signature
    "updraft": Move("updraft", "Updraft", "flying", "special", 100, 0),
    # Draculedge signature multi-hit (kept here for completeness; multi-hit table
    # handles the hit count separately).
    "twincross": Move("twincross", "Twin Cross", "dragon", "physical", 50, 0),
    # Delta multi-hit / signature moves used in the engine
    "lumencascade": Move("lumencascade", "Lumen Cascade", "normal", "special", 50, 0),
    "searingclaws": Move("searingclaws", "Searing Claws", "fire", "physical", 35, 0),
    "dualdivide": Move("dualdivide", "Dual Divide", "bug", "physical", 40, 0),
    "tomahawkvolley": Move("tomahawkvolley", "Tomahawk Volley", "fire", "physical", 20, 0),
    "wretchedstab": Move("wretchedstab", "Wretched Stab", "ghost", "physical", 20, 0),
    "divinevolley": Move("divinevolley", "Divine Volley", "fighting", "physical", 20, 0),
    "quillstorm": Move("quillstorm", "Quill Storm", "fire", "physical", 20, 0),
}


def find_move(mon: MonData, move_name: str) -> Move:
    """Look up a move by name on a mon. Falls back to CUSTOM_MOVE_OVERRIDES."""
    needle = normalize_token(move_name)
    for m in mon.legal_moves:
        mid = m.get("id") or ""
        disp = m.get("displayName") or ""
        if normalize_token(mid) == needle or normalize_token(disp) == needle:
            typ = m.get("type")
            cat = m.get("category")
            bp = m.get("basePower") or 0
            # The per-mon JSON sometimes has null type/category for signature
            # moves (e.g. Updraft). Fall through to overrides in that case.
            if typ is None or cat is None or typ == "#n/a":
                break
            return Move(
                move_id=mid or needle,
                display_name=disp or move_name,
                type_name=str(typ).lower(),
                category=str(cat).lower(),
                base_power=int(bp),
                priority=int(m.get("priority") or 0),
            )
    if needle in CUSTOM_MOVE_OVERRIDES:
        return CUSTOM_MOVE_OVERRIDES[needle]
    # Last-ditch: search team-builder signatureMoves for the species
    entry = find_team_builder_entry(mon.display_name)
    if entry:
        for sig in entry.get("signatureMoves") or []:
            if normalize_token(sig.get("name")) == needle:
                pwr_str = (sig.get("power") or "").strip()
                try:
                    bp = int(re.search(r"\d+", pwr_str).group(0))  # type: ignore[union-attr]
                except Exception:
                    bp = 0
                return Move(
                    move_id=needle,
                    display_name=sig.get("name") or move_name,
                    type_name=(sig.get("type") or "normal").lower(),
                    category=(sig.get("category") or "physical").lower(),
                    base_power=bp,
                )
    print(f"ERROR: move '{move_name}' not found on {mon.display_name}.", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Stat calculation (port of StatCalculator.kt)
# ---------------------------------------------------------------------------

def stage_multiplier(stage: int) -> float:
    if stage >= 0:
        return (2.0 + stage) / 2.0
    return 2.0 / (2.0 - stage)


def apply_stage(value: int, stage: int) -> int:
    # Kotlin: (value * mult).toInt()  -> truncate toward zero
    return int(value * stage_multiplier(stage))


def calculate_stat(base: int, level: int, iv: int, ev: int, nature_mod: float) -> int:
    """stat = floor((floor((2*base + iv + floor(ev/4)) * level / 100) + 5) * nature)

    Kotlin uses Int arithmetic (integer floor division), then (.toInt) on the
    nature multiplication. We match that.
    """
    inner = ((2 * base + iv + ev // 4) * level) // 100 + 5
    return int(inner * nature_mod)


def calculate_hp(base: int, level: int, iv: int, ev: int) -> int:
    return ((2 * base + iv + ev // 4) * level) // 100 + level + 10


NATURE_MAPPING = {
    "lonely":   ("atk", "def"),
    "brave":    ("atk", "spe"),
    "adamant":  ("atk", "spa"),
    "naughty":  ("atk", "spd"),
    "bold":     ("def", "atk"),
    "relaxed":  ("def", "spe"),
    "impish":   ("def", "spa"),
    "lax":      ("def", "spd"),
    "timid":    ("spe", "atk"),
    "hasty":    ("spe", "def"),
    "jolly":    ("spe", "spa"),
    "naive":    ("spe", "spd"),
    "modest":   ("spa", "atk"),
    "mild":     ("spa", "def"),
    "quiet":    ("spa", "spe"),
    "rash":     ("spa", "spd"),
    "calm":     ("spd", "atk"),
    "gentle":   ("spd", "def"),
    "sassy":    ("spd", "spe"),
    "careful":  ("spd", "spa"),
}


def nature_modifiers(nature: str) -> dict[str, float]:
    neutral = {"atk": 1.0, "def": 1.0, "spa": 1.0, "spd": 1.0, "spe": 1.0}
    norm = normalize_token(nature)
    adj = NATURE_MAPPING.get(norm)
    if adj is None:
        return neutral
    out = dict(neutral)
    out[adj[0]] = 1.1
    out[adj[1]] = 0.9
    return out


def derive_stats(base_stats: dict, level: int, ivs: dict, evs: dict, nature: str) -> dict:
    mods = nature_modifiers(nature)
    return {
        "hp": calculate_hp(base_stats["hp"], level, ivs["hp"], evs["hp"]),
        "atk": calculate_stat(base_stats["atk"], level, ivs["atk"], evs["atk"], mods["atk"]),
        "def": calculate_stat(base_stats["def"], level, ivs["def"], evs["def"], mods["def"]),
        "spa": calculate_stat(base_stats["spa"], level, ivs["spa"], evs["spa"], mods["spa"]),
        "spd": calculate_stat(base_stats["spd"], level, ivs["spd"], evs["spd"], mods["spd"]),
        "spe": calculate_stat(base_stats["spe"], level, ivs["spe"], evs["spe"], mods["spe"]),
    }


# ---------------------------------------------------------------------------
# Item stat multipliers (port of StatCalculator.kt)
# ---------------------------------------------------------------------------

def item_attack_multiplier(item: Optional[str], species: Optional[str]) -> float:
    if not item:
        return 1.0
    n = normalize_token(item)
    s = (species or "").lower().replace(" ", "").replace("-", "")
    if n == "choiceband":
        return 1.5
    if n == "thickclub" and s in {"cubone", "marowak", "marowakalola"}:
        return 2.0
    if n == "lightball" and s.startswith("pikachu"):
        return 2.0
    return 1.0


def item_special_attack_multiplier(item: Optional[str], species: Optional[str]) -> float:
    if not item:
        return 1.0
    n = normalize_token(item)
    s = (species or "").lower().replace(" ", "").replace("-", "")
    if n == "choicespecs":
        return 1.5
    if n == "lightball" and s.startswith("pikachu"):
        return 2.0
    if n == "deepseatooth" and s == "clamperl":
        return 2.0
    return 1.0


def item_defense_multiplier(item: Optional[str], can_evolve: bool) -> float:
    if not item:
        return 1.0
    n = normalize_token(item)
    if n == "eviolite" and can_evolve:
        return 1.5
    return 1.0


def item_special_defense_multiplier(item: Optional[str], species: Optional[str], can_evolve: bool) -> float:
    if not item:
        return 1.0
    n = normalize_token(item)
    s = (species or "").lower().replace(" ", "").replace("-", "")
    if n == "assaultvest":
        return 1.5
    if n == "eviolite" and can_evolve:
        return 1.5
    if n == "deepseascale" and s == "clamperl":
        return 2.0
    return 1.0


# ---------------------------------------------------------------------------
# Item power boosts (a hardcoded subset of items.js; covers Life Orb,
# type-boosting items, plates, gems, Expert Belt, Muscle Band, Wise Glasses).
# ---------------------------------------------------------------------------

@dataclass
class ItemBoost:
    boosted_type: Optional[str]  # None = all types (Life Orb)
    multiplier: float


# Hand-picked from showdown/data/items.js. Faithful to ItemPowerBoostParser
# (which scrapes that file for chainModify multipliers).
ITEM_POWER_BOOSTS: dict[str, ItemBoost] = {
    "lifeorb": ItemBoost(None, 5324 / 4096),   # ~1.3
    # Type-boosting items: 4915/4096 ≈ 1.2 (Charcoal, Mystic Water, etc.)
    "charcoal": ItemBoost("fire", 4915 / 4096),
    "charcoalstick": ItemBoost("fire", 4915 / 4096),
    "mysticwater": ItemBoost("water", 4915 / 4096),
    "miracleseed": ItemBoost("grass", 4915 / 4096),
    "magnet": ItemBoost("electric", 4915 / 4096),
    "nevermeltice": ItemBoost("ice", 4915 / 4096),
    "blackbelt": ItemBoost("fighting", 4915 / 4096),
    "poisonbarb": ItemBoost("poison", 4915 / 4096),
    "softsand": ItemBoost("ground", 4915 / 4096),
    "sharpbeak": ItemBoost("flying", 4915 / 4096),
    "twistedspoon": ItemBoost("psychic", 4915 / 4096),
    "silverpowder": ItemBoost("bug", 4915 / 4096),
    "hardstone": ItemBoost("rock", 4915 / 4096),
    "spelltag": ItemBoost("ghost", 4915 / 4096),
    "dragonfang": ItemBoost("dragon", 4915 / 4096),
    "blackglasses": ItemBoost("dark", 4915 / 4096),
    "metalcoat": ItemBoost("steel", 4915 / 4096),
    "fairyfeather": ItemBoost("fairy", 4915 / 4096),
    "silkscarf": ItemBoost("normal", 4915 / 4096),
    # Plates / Memories / Drives (same 1.2 multiplier per items.js)
    "flameplate": ItemBoost("fire", 4915 / 4096),
    "splashplate": ItemBoost("water", 4915 / 4096),
    "meadowplate": ItemBoost("grass", 4915 / 4096),
    "zapplate": ItemBoost("electric", 4915 / 4096),
    "icicleplate": ItemBoost("ice", 4915 / 4096),
    "fistplate": ItemBoost("fighting", 4915 / 4096),
    "toxicplate": ItemBoost("poison", 4915 / 4096),
    "earthplate": ItemBoost("ground", 4915 / 4096),
    "skyplate": ItemBoost("flying", 4915 / 4096),
    "mindplate": ItemBoost("psychic", 4915 / 4096),
    "insectplate": ItemBoost("bug", 4915 / 4096),
    "stoneplate": ItemBoost("rock", 4915 / 4096),
    "spookyplate": ItemBoost("ghost", 4915 / 4096),
    "dracoplate": ItemBoost("dragon", 4915 / 4096),
    "dreadplate": ItemBoost("dark", 4915 / 4096),
    "ironplate": ItemBoost("steel", 4915 / 4096),
    "pixieplate": ItemBoost("fairy", 4915 / 4096),
    # Wellspring Mask = type-boosting for Ogerpon-Wellspring's STAB
    # In canon, it's a 1.2x to Ogerpon-W's moves (not generally type-bound).
    # Treat as 1.2x universal when held; engine-side this is best modeled
    # as a 1.2 multiplier on damage. We approximate by boosting Water+Grass.
    "wellspringmask": ItemBoost(None, 1.2),
    "hearthflamemask": ItemBoost(None, 1.2),
    "cornerstonemask": ItemBoost(None, 1.2),
    # Gems: 5325/4096 ≈ 1.3, single-use consumable; engine treats them as static boost
    "firegem": ItemBoost("fire", 5325 / 4096),
    "watergem": ItemBoost("water", 5325 / 4096),
    "grassgem": ItemBoost("grass", 5325 / 4096),
    "electricgem": ItemBoost("electric", 5325 / 4096),
    "icegem": ItemBoost("ice", 5325 / 4096),
    "fightinggem": ItemBoost("fighting", 5325 / 4096),
    "poisongem": ItemBoost("poison", 5325 / 4096),
    "groundgem": ItemBoost("ground", 5325 / 4096),
    "flyinggem": ItemBoost("flying", 5325 / 4096),
    "psychicgem": ItemBoost("psychic", 5325 / 4096),
    "buggem": ItemBoost("bug", 5325 / 4096),
    "rockgem": ItemBoost("rock", 5325 / 4096),
    "ghostgem": ItemBoost("ghost", 5325 / 4096),
    "dragongem": ItemBoost("dragon", 5325 / 4096),
    "darkgem": ItemBoost("dark", 5325 / 4096),
    "steelgem": ItemBoost("steel", 5325 / 4096),
    "fairygem": ItemBoost("fairy", 5325 / 4096),
    "normalgem": ItemBoost("normal", 5325 / 4096),
}


# ---------------------------------------------------------------------------
# Move flag database (minimal hand-curated subset of MoveFlagDatabase.kt)
# ---------------------------------------------------------------------------

@dataclass
class MoveFlags:
    is_contact: bool = False
    is_bite: bool = False
    is_punch: bool = False
    is_pulse: bool = False
    is_slicing: bool = False
    is_sound: bool = False
    is_recoil: bool = False
    has_secondary: bool = False
    multihit_min: int = 1
    multihit_max: int = 1


# Curated to cover the moves we need for Ability triggers (Tough Claws,
# Strong Jaw, etc.). The Kotlin engine reads a 17k-entry generated JSON;
# we cover the staples and Delta sigs.
MOVE_FLAGS: dict[str, MoveFlags] = {
    "tackle":       MoveFlags(is_contact=True),
    "bodyslam":     MoveFlags(is_contact=True, has_secondary=True),
    "ironhead":     MoveFlags(is_contact=True, has_secondary=True),
    "uturn":        MoveFlags(is_contact=True),
    "knockoff":     MoveFlags(is_contact=True),
    "doubleedge":   MoveFlags(is_contact=True, is_recoil=True),
    "outrage":      MoveFlags(is_contact=True),
    "dragonclaw":   MoveFlags(is_contact=True),
    "dragondarts":  MoveFlags(is_contact=True),
    "dragonrush":   MoveFlags(is_contact=True, has_secondary=True),
    "dragontail":   MoveFlags(is_contact=True),
    "stoneedge":    MoveFlags(),
    "facade":       MoveFlags(is_contact=True),
    "earthquake":   MoveFlags(),
    "playrough":    MoveFlags(is_contact=True, has_secondary=True),
    "moonblast":    MoveFlags(has_secondary=True),
    "flamethrower": MoveFlags(has_secondary=True),
    "fireblast":    MoveFlags(has_secondary=True),
    "thunderbolt":  MoveFlags(has_secondary=True),
    "thunder":      MoveFlags(has_secondary=True),
    "dragonpulse":  MoveFlags(is_pulse=True),
    "darkpulse":    MoveFlags(is_pulse=True),
    "watercannon":  MoveFlags(is_pulse=True),
    "ivycudgel":    MoveFlags(is_contact=True),
    "icefang":      MoveFlags(is_contact=True, is_bite=True, has_secondary=True),
    "firefang":     MoveFlags(is_contact=True, is_bite=True, has_secondary=True),
    "thunderfang":  MoveFlags(is_contact=True, is_bite=True, has_secondary=True),
    "crunch":       MoveFlags(is_contact=True, is_bite=True, has_secondary=True),
    "icepunch":     MoveFlags(is_contact=True, is_punch=True),
    "firepunch":    MoveFlags(is_contact=True, is_punch=True),
    "thunderpunch": MoveFlags(is_contact=True, is_punch=True),
    "drainpunch":   MoveFlags(is_contact=True, is_punch=True),
    "machpunch":    MoveFlags(is_contact=True, is_punch=True),
    "boomburst":    MoveFlags(is_sound=True),
    "hypervoice":   MoveFlags(is_sound=True),
    "psyblade":     MoveFlags(is_contact=True, is_slicing=True),
    "leafblade":    MoveFlags(is_contact=True, is_slicing=True),
    "sacredsword":  MoveFlags(is_contact=True, is_slicing=True),
    "updraft":      MoveFlags(),
    "airslash":     MoveFlags(is_slicing=True, has_secondary=True),
}


def move_flags_for(move: Move) -> MoveFlags:
    return MOVE_FLAGS.get(normalize_token(move.move_id), MoveFlags())


# ---------------------------------------------------------------------------
# Multi-hit move table (port of DamageEngine.kt::multiHitMoves)
# ---------------------------------------------------------------------------

MULTI_HIT_MOVES: dict[str, tuple[int, int]] = {
    "bulletseed": (2, 5),
    "rockblast": (2, 5),
    "iciclespear": (2, 5),
    "pinmissile": (2, 5),
    "armthrust": (2, 5),
    "tailslap": (2, 5),
    "furyswipes": (2, 5),
    "furyattack": (2, 5),
    "cometpunch": (2, 5),
    "doubleslap": (2, 5),
    "spikecannon": (2, 5),
    "barrage": (2, 5),
    "scaleshot": (2, 5),
    "watershuriken": (2, 5),
    "doublekick": (2, 2),
    "doubleironbash": (2, 2),
    "doublehit": (2, 2),
    "bonemerang": (2, 2),
    "twineedle": (2, 2),
    "dualchop": (2, 2),
    "geargrind": (2, 2),
    "dragondarts": (2, 2),
    "tripleaxel": (3, 3),
    "triplekick": (3, 3),
    "surgingstrikes": (3, 3),
    "populationbomb": (1, 10),
    "twincross": (2, 2),
    "lumencascade": (2, 2),
    "searingclaws": (2, 2),
    "dualdivide": (2, 2),
    "tomahawkvolley": (2, 5),
    "wretchedstab": (2, 5),
    "divinevolley": (1, 6),
    "quillstorm": (1, 3),
}


SLICING_MOVES: set[str] = {
    "aerialace", "aircutter", "airslash", "behemothblade", "bitterblade",
    "ceaselessedge", "crosspoison", "cut", "furycutter", "kowtowcleave",
    "leafblade", "nightslash", "populationbomb", "psyblade", "psychocut",
    "razorleaf", "razorshell", "sacredsword", "secretsword", "slash",
    "solarblade", "stoneaxe", "stormthrow", "xscissor",
    "dualdivide",
}

KICKING_MOVES: set[str] = {
    "axekick", "blazekick", "doublekick", "highhorsepower", "highjumpkick",
    "jumpkick", "lowkick", "lowsweep", "megakick", "pyroball",
    "rollingkick", "stomp", "stompingtantrum", "thunderouskick",
    "tripleaxel", "triplekick", "tropkick",
}


def is_slicing(move: Move) -> bool:
    return normalize_token(move.move_id) in SLICING_MOVES


def is_kicking(move: Move) -> bool:
    return normalize_token(move.move_id) in KICKING_MOVES


SPLIT_CATEGORY_MOVES: set[str] = {"terablast", "photongeyser", "lightthatburnsthesky"}

MOVES_THAT_BYPASS_ABILITY: set[str] = {
    "photongeyser", "lightthatburnsthesky", "sunsteelstrike", "moongeistbeam",
    "gmaxdrumsolo", "gmaxfireball", "gmaxhydrosnipe",
}


# ---------------------------------------------------------------------------
# Combatant assembly
# ---------------------------------------------------------------------------

@dataclass
class Combatant:
    mon: MonData
    level: int
    nature: str
    ivs: dict
    evs: dict
    derived_stats: dict  # hp/atk/def/spa/spd/spe
    ability: Optional[str]
    item: Optional[str]
    status: Optional[str] = None
    stages: dict = field(default_factory=lambda: {"atk": 0, "def": 0, "spa": 0, "spd": 0, "spe": 0})
    low_hp: bool = False
    at_full_hp: bool = True
    can_evolve: bool = False

    def has_type(self, type_name: str) -> bool:
        needle = normalize_token(type_name)
        return any(normalize_token(t) == needle for t in self.mon.types)

    def stage_for(self, stat: str) -> int:
        return int(self.stages.get(stat, 0))


def parse_stat_spread(spec: str) -> dict:
    """Parse 'hp/atk/def/spa/spd/spe' into dict."""
    parts = spec.split("/")
    if len(parts) != 6:
        print(f"ERROR: invalid stat spread '{spec}', expected 6 slash-separated numbers.", file=sys.stderr)
        sys.exit(1)
    keys = ["hp", "atk", "def", "spa", "spd", "spe"]
    return {k: int(v) for k, v in zip(keys, parts)}


# ---------------------------------------------------------------------------
# Damage engine (port of BestEffortDamageEngine)
# ---------------------------------------------------------------------------

@dataclass
class Context:
    weather: Optional[str] = None
    terrain: Optional[str] = None
    attacker_screens: bool = False  # not really used; defender side matters
    defender_light_screen: bool = False
    defender_reflect: bool = False
    defender_aurora_veil: bool = False
    strong_winds: bool = False
    attacker_team_fainted: int = 0


def is_grounded(c: Combatant) -> bool:
    if c.has_type("flying"):
        return False
    if normalize_token(c.ability) == "levitate":
        return False
    return True


def bypasses_defender_ability(attacker_ability: Optional[str]) -> bool:
    # Mirrors Kotlin exactly. Infiltrator is NOT here — in canon Infiltrator
    # bypasses screens/substitute, not abilities, and the Kotlin source agrees.
    return normalize_token(attacker_ability) in {"moldbreaker", "turboblaze", "teravolt"}


def move_bypasses_ability(move: Move) -> bool:
    return normalize_token(move.move_id) in MOVES_THAT_BYPASS_ABILITY


def resolve_move_type(move: Move, attacker: Combatant, ctx: Context) -> str:
    """Handle Weather Ball, Ivy Cudgel (Ogerpon-Wellspring -> Water), -ate abilities."""
    move_id = normalize_token(move.move_id)
    # Ivy Cudgel form-typing (port of BattleMoveSupport.resolveIvyCudgelTypeName).
    if move_id == "ivycudgel":
        species = normalize_token(attacker.mon.species_key)
        form_typings = {
            "ogerponwellspring": "water",
            "ogerponhearthflame": "fire",
            "ogerponcornerstone": "rock",
        }
        item_norm = normalize_token(attacker.item)
        mask_typings = {
            "wellspringmask": "water",
            "hearthflamemask": "fire",
            "cornerstonemask": "rock",
        }
        # Prefer species; mask is a secondary signal.
        for key, t in form_typings.items():
            if key in species:
                return t
        if item_norm in mask_typings:
            return mask_typings[item_norm]
        return "grass"

    base = move.type_name
    if move_id == "weatherball":
        w = normalize_token(ctx.weather)
        base = {"rain": "water", "harshsunlight": "fire", "sun": "fire", "sunlight": "fire",
                "sandstorm": "rock", "hail": "ice", "snow": "ice"}.get(w, move.type_name)
    elif move_id == "terablast":
        # Tera banned in ranked per workspace rules; just pass through type.
        base = move.type_name

    # -ate abilities convert Normal moves
    if base.lower() == "normal":
        ate = {
            "pixilate": "fairy",
            "aerilate": "flying",
            "refrigerate": "ice",
            "galvanize": "electric",
        }.get(normalize_token(attacker.ability))
        if ate:
            return ate
    return base.lower()


def pixelate_boost(move: Move, attacker: Combatant) -> float:
    if move.type_name.lower() != "normal":
        return 1.0
    if normalize_token(attacker.ability) in {"pixilate", "aerilate", "refrigerate", "galvanize"}:
        return 1.2
    return 1.0


def ability_type_immunity(defender_ability: Optional[str], move_type: str) -> float:
    """Type-changing/-immunity abilities. Returns 0.0 to nullify damage."""
    a = normalize_token(defender_ability)
    t = normalize_token(move_type)
    if a in {"levitate", "eartheater"} and t == "ground":
        return 0.0
    if a in {"waterabsorb", "stormdrain", "dryskin"} and t == "water":
        return 0.0
    if a in {"flashfire", "wellbakedbody"} and t == "fire":
        return 0.0
    if a in {"voltabsorb", "lightningrod", "motordrive"} and t == "electric":
        return 0.0
    if a == "sapsipper" and t == "grass":
        return 0.0
    return 1.0


def stab_multiplier(attacker: Combatant, move_type: str) -> float:
    if not attacker.has_type(move_type):
        return 1.0
    if normalize_token(attacker.ability) == "adaptability":
        return 2.0
    return 1.5


def weather_modifier(move_type: str, ctx: Context) -> float:
    w = normalize_token(ctx.weather)
    t = normalize_token(move_type)
    if w in {"harshsunlight", "sun", "sunlight"}:
        if t == "fire":
            return 1.5
        if t == "water":
            return 0.5
        return 1.0
    if w == "rain":
        if t == "water":
            return 1.5
        if t == "fire":
            return 0.5
    return 1.0


def terrain_modifier(move: Move, move_type: str, attacker: Combatant, defender: Combatant, ctx: Context) -> float:
    terrain = normalize_token(ctx.terrain)
    if not terrain:
        return 1.0
    atk_grounded = is_grounded(attacker)
    def_grounded = is_grounded(defender)
    t = normalize_token(move_type)
    move_id = normalize_token(move.move_id)
    if terrain == "electricterrain":
        return 1.3 if (atk_grounded and t == "electric") else 1.0
    if terrain == "psychicterrain":
        return 1.3 if (atk_grounded and t == "psychic") else 1.0
    if terrain == "grassyterrain":
        if atk_grounded and t == "grass":
            return 1.3
        if move_id in {"earthquake", "bulldoze", "magnitude"} and def_grounded:
            return 0.5
        return 1.0
    if terrain == "mistyterrain":
        return 0.5 if (def_grounded and t == "dragon") else 1.0
    return 1.0


def screen_modifier(defender_category: str, ctx: Context, attacker_ability: Optional[str] = None) -> float:
    # Infiltrator bypasses screens in canon. Kotlin doesn't model this
    # explicitly (no screen bypass in screenModifier), but it's a well-known
    # canonical interaction and the user spec calls Infiltrator out. Keeping
    # this minimal extension here; pass attacker_ability through.
    if normalize_token(attacker_ability) == "infiltrator":
        return 1.0
    if ctx.defender_aurora_veil:
        return 0.5
    if defender_category == "physical" and ctx.defender_reflect:
        return 0.5
    if defender_category == "special" and ctx.defender_light_screen:
        return 0.5
    return 1.0


def burn_modifier(attacker: Combatant, category: str) -> float:
    if category != "physical":
        return 1.0
    if normalize_token(attacker.status) != "burn":
        return 1.0
    if normalize_token(attacker.ability) == "guts":
        return 1.0
    return 0.5


def offensive_ability_modifier(attacker: Combatant, move: Move, move_type: str, category: str,
                                ctx: Context, effectiveness: float) -> float:
    ability = normalize_token(attacker.ability)
    flags = move_flags_for(move)
    power = move.base_power
    t = normalize_token(move_type)
    if ability in {"hugepower", "purepower"}:
        return 2.0 if category == "physical" else 1.0
    if ability == "guts":
        return 1.5 if (category == "physical" and attacker.status) else 1.0
    if ability == "solarpower":
        return 1.5 if (category == "special" and normalize_token(ctx.weather) in {"harshsunlight", "sun", "sunlight"}) else 1.0
    if ability == "flareboost":
        return 1.5 if (category == "special" and normalize_token(attacker.status) == "burn") else 1.0
    if ability == "toxicboost":
        return 1.5 if (category == "physical" and normalize_token(attacker.status) in {"poison", "poisonbadly", "badpoison"}) else 1.0
    if ability == "blaze":
        return 1.5 if (t == "fire" and attacker.low_hp) else 1.0
    if ability == "torrent":
        return 1.5 if (t == "water" and attacker.low_hp) else 1.0
    if ability == "overgrow":
        return 1.5 if (t == "grass" and attacker.low_hp) else 1.0
    if ability == "swarm":
        return 1.5 if (t == "bug" and attacker.low_hp) else 1.0
    if ability == "toughclaws":
        return 1.3 if flags.is_contact else 1.0
    if ability == "strongjaw":
        return 1.5 if flags.is_bite else 1.0
    if ability == "ironfist":
        return 1.2 if flags.is_punch else 1.0
    if ability == "megalauncher":
        return 1.5 if flags.is_pulse else 1.0
    if ability == "sharpness":
        return 1.5 if (flags.is_slicing or is_slicing(move)) else 1.0
    if ability == "punkrock":
        return 1.3 if flags.is_sound else 1.0
    if ability == "reckless":
        return 1.2 if flags.is_recoil else 1.0
    if ability == "sheerforce":
        return 1.3 if flags.has_secondary else 1.0
    if ability == "technician":
        return 1.5 if (1 <= power <= 60) else 1.0
    if ability == "tintedlens":
        return 2.0 if (0.0 < effectiveness < 1.0) else 1.0
    if ability == "waterbubble":
        return 2.0 if t == "water" else 1.0
    if ability in {"steelworker", "steelyspirit"}:
        return 1.5 if t == "steel" else 1.0
    if ability == "dragonsmaw":
        return 1.5 if t == "dragon" else 1.0
    if ability == "transistor":
        return 1.3 if t == "electric" else 1.0
    if ability == "rockypayload":
        return 1.5 if t == "rock" else 1.0
    if ability in {"aerilate", "pixilate", "refrigerate", "galvanize"}:
        return pixelate_boost(move, attacker)
    if ability == "supremeoverlord":
        fainted = max(0, min(5, ctx.attacker_team_fainted))
        return 1.0 + 0.1 * fainted
    return 1.0


def defensive_ability_modifier(defender: Combatant, move: Move, move_type: str, category: str,
                                effectiveness: float, defender_at_full_hp: bool) -> float:
    ability = normalize_token(defender.ability)
    flags = move_flags_for(move)
    t = normalize_token(move_type)
    if ability == "thickfat":
        return 0.5 if t in {"fire", "ice"} else 1.0
    if ability == "heatproof":
        return 0.5 if t == "fire" else 1.0
    if ability == "waterbubble":
        return 0.5 if t == "fire" else 1.0
    if ability == "dryskin":
        return 1.25 if t == "fire" else 1.0
    if ability == "fluffy":
        if flags.is_contact and t != "fire":
            return 0.5
        if t == "fire":
            return 2.0
        return 1.0
    if ability == "furcoat":
        return 0.5 if category == "physical" else 1.0
    if ability == "icescales":
        return 0.5 if category == "special" else 1.0
    if ability == "marvelscale":
        return (2.0 / 3.0) if (category == "physical" and defender.status) else 1.0
    if ability in {"filter", "solidrock", "prismarmor"}:
        return 0.75 if effectiveness > 1.0 else 1.0
    if ability in {"multiscale", "shadowshield"}:
        return 0.5 if defender_at_full_hp else 1.0
    if ability == "punkrock":
        return 0.5 if flags.is_sound else 1.0
    if ability == "purifyingsalt":
        return 0.5 if t == "ghost" else 1.0
    return 1.0


def delta_offensive_ability_modifier(attacker: Combatant, move_type: str, move: Move, effectiveness: float) -> float:
    ability = normalize_token(attacker.ability)
    t = normalize_token(move_type)
    if ability == "flurry":
        return 1.5 if (t == "ice" and attacker.low_hp) else 1.0
    if ability == "draconic":
        return 1.5 if (t == "dragon" and attacker.low_hp) else 1.0
    if ability == "pyroclastic":
        return 1.3 if t == "rock" else 1.0
    if ability == "stoneheart":
        return 1.5 if t == "rock" else 1.0
    if ability == "valorheart":
        return 1.2
    if ability == "torquestep":
        return 1.3 if is_kicking(move) else 1.0
    if ability == "conviction":
        return 1.25 if effectiveness > 1.0 else 1.0
    return 1.0


def delta_defensive_ability_modifier(defender: Combatant, move_type: str) -> float:
    ability = normalize_token(defender.ability)
    t = normalize_token(move_type)
    if ability == "igneous":
        return 0.5 if t in {"fire", "water"} else 1.0
    return 1.0


def delta_guaranteed_crit(attacker: Combatant, move: Move) -> float:
    ability = normalize_token(attacker.ability)
    if ability == "reap" and is_slicing(move):
        return 1.5
    return 1.0


def crit_multiplier(attacker: Combatant) -> float:
    return 2.25 if normalize_token(attacker.ability) == "sniper" else 1.5


def item_power_modifier(attacker: Combatant, move_type: str, category: str, effectiveness: float) -> float:
    item = normalize_token(attacker.item)
    if not item:
        return 1.0
    if item == "expertbelt":
        return 1.2 if effectiveness > 1.0 else 1.0
    if item == "muscleband":
        return 1.1 if category == "physical" else 1.0
    if item == "wiseglasses":
        return 1.1 if category == "special" else 1.0
    if item == "metronome":
        return 1.0
    boost = ITEM_POWER_BOOSTS.get(item)
    if boost is None:
        return 1.0
    if boost.boosted_type is None:
        return boost.multiplier
    return boost.multiplier if normalize_token(boost.boosted_type) == normalize_token(move_type) else 1.0


def freeze_dry_multiplier(move_id_norm: str, defending_type: str) -> Optional[float]:
    if move_id_norm == "freezedry" and defending_type.lower() == "water":
        return 2.0
    return None


def compute_effectiveness(move: Move, move_type: str, defender: Combatant, ctx: Context,
                          attacker_ability: Optional[str]) -> float:
    move_id_norm = normalize_token(move.move_id)
    eff = 1.0
    for dt in defender.mon.types:
        fd = freeze_dry_multiplier(move_id_norm, dt)
        if fd is not None:
            eff *= fd
        else:
            eff *= type_multiplier(move_type, dt)
    # Strong Winds: Ice/Rock/Electric vs Flying defenders -> 1x (was 2x).
    auto_strong_winds = normalize_token(defender.ability) in {"parasolprayer", "deltastream"}
    strong_winds_active = ctx.strong_winds or auto_strong_winds
    if strong_winds_active and defender.has_type("flying"):
        t = normalize_token(move_type)
        if t in {"ice", "rock", "electric"}:
            # Recompute: cancel the 2x on flying that the chart applied.
            # Easier: divide eff by chart's flying multiplier and multiply by 1.0
            # against flying. Cleaner: rebuild eff.
            eff = 1.0
            for dt in defender.mon.types:
                if normalize_token(dt) == "flying":
                    eff *= 1.0
                else:
                    fd = freeze_dry_multiplier(move_id_norm, dt)
                    if fd is not None:
                        eff *= fd
                    else:
                        eff *= type_multiplier(move_type, dt)
    bypass = bypasses_defender_ability(attacker_ability) or move_bypasses_ability(move)
    if not bypass:
        eff *= ability_type_immunity(defender.ability, move_type)
    if not bypass and normalize_token(defender.ability) == "wonderguard":
        # Wonder Guard: blocks anything that isn't super effective (and not immune already)
        if 0.0 < eff <= 1.0:
            eff = 0.0
    return eff


def effective_attack_stat(attacker: Combatant, defender: Combatant, move: Move, category: str,
                          is_crit: bool = False) -> int:
    move_id = normalize_token(move.move_id)
    uses_def_atk = (move_id == "foulplay")
    source = defender if uses_def_atk else attacker
    if move_id == "bodypress":
        base_attack = source.derived_stats["def"]
        raw_stage = source.stage_for("def")
    elif category == "physical":
        base_attack = source.derived_stats["atk"]
        raw_stage = source.stage_for("atk")
    else:
        base_attack = source.derived_stats["spa"]
        raw_stage = source.stage_for("spa")
    # Spectral Thief steal (port logic — defender stage matters here).
    effective_stage = raw_stage
    if move_id == "spectralthief" and not uses_def_atk:
        def_stage = defender.stage_for("atk") if category == "physical" else defender.stage_for("spa")
        if def_stage > 0:
            effective_stage = raw_stage + def_stage
    stage = max(0, effective_stage) if is_crit else effective_stage
    value = apply_stage(base_attack, stage)
    holder = defender if uses_def_atk else attacker
    if category == "physical":
        value = int(value * item_attack_multiplier(holder.item, holder.mon.species_key))
    else:
        value = int(value * item_special_attack_multiplier(holder.item, holder.mon.species_key))
    return max(1, value)


def effective_defense_stat(defender: Combatant, category: str, ctx: Context, is_crit: bool = False) -> int:
    raw_stage = defender.stage_for("def") if category == "physical" else defender.stage_for("spd")
    stage = min(0, raw_stage) if is_crit else raw_stage
    if category == "physical":
        value = apply_stage(defender.derived_stats["def"], stage)
        value = int(value * item_defense_multiplier(defender.item, defender.can_evolve))
    else:
        value = apply_stage(defender.derived_stats["spd"], stage)
        value = int(value * item_special_defense_multiplier(defender.item, defender.mon.species_key, defender.can_evolve))
    if category == "special" and normalize_token(ctx.weather) == "sandstorm" and defender.has_type("rock"):
        value = int(value * 1.5)
    if category == "physical" and normalize_token(ctx.weather) == "snow" and defender.has_type("ice"):
        value = int(value * 1.5)
    return max(1, value)


def effective_power(move: Move, attacker: Combatant, defender: Combatant, ctx: Context) -> float:
    move_id = normalize_token(move.move_id)
    bp = float(move.base_power)
    if move_id in {"hex", "barbbarrage", "infernalparade"}:
        return bp * 2.0 if defender.status else bp
    if move_id == "venoshock":
        return bp * 2.0 if normalize_token(defender.status) in {"poison", "poisonbadly", "badpoison"} else bp
    if move_id == "weatherball":
        if normalize_token(ctx.weather) in {"rain", "harshsunlight", "sun", "sunlight", "sandstorm", "hail", "snow"}:
            return bp * 2.0
        return bp
    if move_id == "facade":
        if normalize_token(attacker.status) in {"burn", "poison", "poisonbadly", "badpoison", "paralysis", "paralyze"}:
            return bp * 2.0
        return bp
    if move_id == "acrobatics":
        return bp * 2.0 if not attacker.item else bp
    if move_id == "lowkick" or move_id == "grassknot":
        kg = defender.mon.weight_kg
        if kg is None:
            return 20.0
        if kg >= 200:
            return 120.0
        if kg >= 100:
            return 100.0
        if kg >= 50:
            return 80.0
        if kg >= 25:
            return 60.0
        if kg >= 10:
            return 40.0
        return 20.0
    if move_id == "heavyslam" or move_id == "heatcrash":
        atk_kg = attacker.mon.weight_kg
        def_kg = defender.mon.weight_kg
        if atk_kg is None or def_kg is None:
            return 40.0
        if def_kg <= 0:
            return 120.0
        ratio = atk_kg / def_kg
        if ratio >= 5:
            return 120.0
        if ratio >= 4:
            return 100.0
        if ratio >= 3:
            return 80.0
        if ratio >= 2:
            return 60.0
        return 40.0
    if move_id in {"eruption", "waterspout", "dragonenergy"}:
        # at_full_hp implies currentHp == maxHp
        ratio = 1.0 if attacker.at_full_hp else (0.0 if attacker.low_hp else 0.5)
        return max(1.0, 150.0 * ratio)
    return bp


@dataclass
class DamageResult:
    move: Move
    move_type: str
    effectiveness: float
    damage_rolls: list[int]   # 16 rolls, 85-100, total damage (with multi-hit applied at .min/.max)
    min_damage: int
    max_damage: int
    defender_max_hp: int
    min_hits: int
    max_hits: int
    ko_label: str
    confidence: str
    warnings: list[str]


def damage_rolls(base_damage: float, modifier: float) -> list[int]:
    out = []
    for roll in range(85, 101):
        out.append(max(1, math.floor(base_damage * modifier * roll / 100.0)))
    return out


def ko_label(current_hp: int, min_dmg: int, max_dmg: int) -> str:
    if current_hp <= 0:
        return "KO"
    if min_dmg >= current_hp:
        return "OHKO"
    if max_dmg >= current_hp:
        return "Likely OHKO"
    if max_dmg * 2 >= current_hp:
        return "2HKO"
    if max_dmg * 3 >= current_hp:
        return "3HKO"
    return "4HKO+"


def compute_damage(attacker: Combatant, defender: Combatant, move: Move, ctx: Context) -> DamageResult:
    warnings: list[str] = []
    if move.category == "status":
        return DamageResult(move, move.type_name, 0.0, [], 0, 0, defender.derived_stats["hp"], 1, 1,
                            "--", "LOW", ["Status move"])
    category = move.category
    # Split-category moves
    if normalize_token(move.move_id) in SPLIT_CATEGORY_MOVES:
        phys = effective_attack_stat(attacker, defender, move, "physical")
        spec = effective_attack_stat(attacker, defender, move, "special")
        category = "physical" if phys > spec else "special"

    move_type = resolve_move_type(move, attacker, ctx)
    effectiveness = compute_effectiveness(move, move_type, defender, ctx, attacker.ability)

    defender_max_hp = defender.derived_stats["hp"]
    if effectiveness == 0.0:
        return DamageResult(move, move_type, 0.0, [0]*16, 0, 0, defender_max_hp, 1, 1,
                            "Immune", "HIGH", warnings)

    bypass = bypasses_defender_ability(attacker.ability) or move_bypasses_ability(move)
    power = effective_power(move, attacker, defender, ctx)
    if power <= 0:
        return DamageResult(move, move_type, effectiveness, [], 0, 0, defender_max_hp, 1, 1,
                            "--", "LOW", ["No damaging power"])

    attack_stat = effective_attack_stat(attacker, defender, move, category)
    defense_stat = effective_defense_stat(defender, category, ctx)
    if attack_stat <= 0 or defense_stat <= 0:
        return DamageResult(move, move_type, effectiveness, [], 0, 0, defender_max_hp, 1, 1,
                            "--", "LOW", ["Incomplete stats"])

    level_factor = (2.0 * attacker.level) / 5.0 + 2.0
    base_damage = ((level_factor * power * attack_stat / defense_stat) / 50.0) + 2.0

    screen_factor = screen_modifier(category, ctx, attacker.ability)
    defensive_ability_factor = 1.0 if bypass else defensive_ability_modifier(
        defender, move, move_type, category, effectiveness, defender.at_full_hp
    )

    modifier = stab_multiplier(attacker, move_type)
    modifier *= effectiveness
    modifier *= weather_modifier(move_type, ctx)
    modifier *= terrain_modifier(move, move_type, attacker, defender, ctx)
    modifier *= screen_factor
    modifier *= burn_modifier(attacker, category)
    modifier *= offensive_ability_modifier(attacker, move, move_type, category, ctx, effectiveness)
    modifier *= defensive_ability_factor
    modifier *= delta_offensive_ability_modifier(attacker, move_type, move, effectiveness)
    modifier *= delta_defensive_ability_modifier(defender, move_type)
    modifier *= item_power_modifier(attacker, move_type, category, effectiveness)

    crit_factor = delta_guaranteed_crit(attacker, move)
    if crit_factor > 1.0:
        warnings.append(f"Guaranteed crit ({attacker.ability})")
    modifier *= crit_factor

    rolls = damage_rolls(base_damage, modifier)

    # Multi-hit
    move_norm = normalize_token(move.move_id)
    hits = MULTI_HIT_MOVES.get(move_norm)
    min_hits, max_hits = (hits if hits else (1, 1))
    if max_hits > 1:
        if min_hits == max_hits:
            warnings.append(f"Multi-hit ({min_hits} hits)")
        else:
            warnings.append(f"Multi-hit ({min_hits}-{max_hits} hits)")

    min_damage = rolls[0] * min_hits
    max_damage = rolls[-1] * max_hits

    # Sturdy
    sturdy_active = (not bypass and normalize_token(defender.ability) == "sturdy"
                     and defender.at_full_hp and defender_max_hp > 0)
    if sturdy_active and max_damage >= defender_max_hp:
        cap = defender_max_hp - 1
        max_damage = cap
        if min_damage > cap:
            min_damage = cap
        warnings.append("Sturdy survives at 1 HP")

    # Confidence heuristic (port of confidenceFor)
    confidence = "HIGH"
    if any(w.lower().startswith("unknown") for w in warnings):
        confidence = "LOW"

    current_hp = defender_max_hp  # We assume full HP for the calc.
    label = ko_label(current_hp, min_damage, max_damage)

    return DamageResult(
        move=move,
        move_type=move_type,
        effectiveness=effectiveness,
        damage_rolls=rolls,
        min_damage=min_damage,
        max_damage=max_damage,
        defender_max_hp=defender_max_hp,
        min_hits=min_hits,
        max_hits=max_hits,
        ko_label=label,
        confidence=confidence,
        warnings=warnings,
    )


# ---------------------------------------------------------------------------
# Conditions parser
# ---------------------------------------------------------------------------

def parse_conditions(s: str, attacker: Combatant, defender: Combatant, ctx: Context) -> Context:
    if not s:
        return ctx
    for raw in s.split(","):
        cond = raw.strip().lower()
        if not cond:
            continue
        if cond == "rain":
            ctx.weather = "rain"
        elif cond in {"sun", "sunlight", "harshsunlight"}:
            ctx.weather = "harshsunlight"
        elif cond in {"sand", "sandstorm"}:
            ctx.weather = "sandstorm"
        elif cond == "snow":
            ctx.weather = "snow"
        elif cond in {"hail"}:
            ctx.weather = "hail"
        elif cond == "electric-terrain":
            ctx.terrain = "electricterrain"
        elif cond == "psychic-terrain":
            ctx.terrain = "psychicterrain"
        elif cond == "grassy-terrain":
            ctx.terrain = "grassyterrain"
        elif cond == "misty-terrain":
            ctx.terrain = "mistyterrain"
        elif cond == "light-screen":
            ctx.defender_light_screen = True
        elif cond == "reflect":
            ctx.defender_reflect = True
        elif cond == "aurora-veil":
            ctx.defender_aurora_veil = True
        elif cond == "strong-winds":
            ctx.strong_winds = True
        elif cond in {"attacker-screens-off", "defender-screens-off"}:
            pass  # explicit no-op for documentation
        elif cond == "attacker-burn":
            attacker.status = "burn"
        elif cond == "attacker-low-hp":
            attacker.low_hp = True
            attacker.at_full_hp = False
        elif cond == "defender-low-hp":
            defender.low_hp = True
            defender.at_full_hp = False
        else:
            m = re.match(r"(attacker|defender)\-([+-])(\d+)$", cond)
            if m:
                who, sign, num = m.group(1), m.group(2), int(m.group(3))
                delta = num if sign == "+" else -num
                target = attacker if who == "attacker" else defender
                # apply to the relevant attacking/defending stat. We don't know
                # which until we see the move, but for simplicity we bump atk,
                # spa for attacker and def, spd for defender. The engine reads
                # whichever stage is relevant at attack-stat time.
                if who == "attacker":
                    target.stages["atk"] = target.stages.get("atk", 0) + delta
                    target.stages["spa"] = target.stages.get("spa", 0) + delta
                else:
                    target.stages["def"] = target.stages.get("def", 0) + delta
                    target.stages["spd"] = target.stages.get("spd", 0) + delta
            else:
                print(f"WARN: unknown condition '{cond}'", file=sys.stderr)
    return ctx


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_combatant(name: str, ability: Optional[str], item: Optional[str], nature: str,
                    evs: str, ivs: str, level: int) -> Combatant:
    mon = load_mon(name)
    iv_dict = parse_stat_spread(ivs) if ivs else {"hp": 31, "atk": 31, "def": 31, "spa": 31, "spd": 31, "spe": 31}
    ev_dict = parse_stat_spread(evs) if evs else {"hp": 0, "atk": 0, "def": 0, "spa": 0, "spd": 0, "spe": 0}
    derived = derive_stats(mon.base_stats, level, iv_dict, ev_dict, nature)
    return Combatant(
        mon=mon,
        level=level,
        nature=nature,
        ivs=iv_dict,
        evs=ev_dict,
        derived_stats=derived,
        ability=ability,
        item=item,
    )


def format_result(attacker: Combatant, defender: Combatant, move: Move, ctx: Context, result: DamageResult) -> str:
    lines = []
    cond_bits = []
    if ctx.weather:
        cond_bits.append(ctx.weather)
    if ctx.terrain:
        cond_bits.append(ctx.terrain)
    if ctx.defender_light_screen:
        cond_bits.append("light screen")
    if ctx.defender_reflect:
        cond_bits.append("reflect")
    if ctx.defender_aurora_veil:
        cond_bits.append("aurora veil")
    if ctx.strong_winds or normalize_token(defender.ability) in {"parasolprayer", "deltastream"}:
        cond_bits.append("strong winds")
    cond_str = (" in " + ", ".join(cond_bits)) if cond_bits else ""

    atk_item = attacker.item or "no item"
    def_item = defender.item or "no item"
    lines.append(
        f"{attacker.mon.display_name} ({attacker.nature}, {atk_item}) {move.display_name} "
        f"vs {defender.mon.display_name} ({defender.nature}, {def_item}){cond_str}"
    )
    if result.max_hits > 1:
        if result.min_hits == result.max_hits:
            lines.append(f"Hits:        {result.max_hits} (multi-hit, fixed)")
        else:
            lines.append(f"Hits:        {result.min_hits}-{result.max_hits} (multi-hit)")
    if result.defender_max_hp > 0 and result.max_damage > 0:
        min_pct = result.min_damage * 100.0 / result.defender_max_hp
        max_pct = result.max_damage * 100.0 / result.defender_max_hp
        lines.append(f"Damage:      {result.min_damage}-{result.max_damage} ({min_pct:.1f}% - {max_pct:.1f}%)")
    else:
        lines.append(f"Damage:      0 (0.0% - 0.0%)")
    lines.append(f"Effectiveness: {result.effectiveness:g}x")
    lines.append(f"Result:      {result.ko_label}")
    lines.append(f"Confidence:  {result.confidence}")
    if result.warnings:
        lines.append("Warnings:    " + "; ".join(result.warnings))
    return "\n".join(lines)


def run_calc(args: argparse.Namespace) -> int:
    attacker = build_combatant(
        args.attacker, args.attacker_ability, args.attacker_item,
        args.attacker_nature, args.attacker_evs, args.attacker_ivs, args.level,
    )
    defender = build_combatant(
        args.defender, args.defender_ability, args.defender_item,
        args.defender_nature, args.defender_evs, args.defender_ivs, args.level,
    )
    move = find_move(attacker.mon, args.move)
    ctx = Context()
    parse_conditions(args.conditions or "", attacker, defender, ctx)
    result = compute_damage(attacker, defender, move, ctx)
    print(format_result(attacker, defender, move, ctx, result))
    return 0


def run_self_test() -> int:
    print("=== Self-test ===")
    cases = [
        # Test 1: Archapult Dragon Darts (Jolly 252 Atk LO) vs Tinkaton-Gamma (Calm 252 HP / 252 SpD Lefties), no weather.
        # Expected: multi-hit 2x, ballpark 45-60%.
        {
            "name": "Archapult Dragon Darts vs Tinkaton-Gamma (Lefties)",
            "attacker": "Archapult", "atk_abil": "Infiltrator", "atk_item": "Life Orb",
            "atk_nature": "Jolly", "atk_evs": "0/252/0/0/4/252", "atk_ivs": "31/31/31/31/31/31",
            "move": "Dragon Darts",
            "defender": "Tinkaton-Gamma", "def_abil": "Parasol Prayer", "def_item": "Leftovers",
            "def_nature": "Calm", "def_evs": "252/0/4/0/252/0", "def_ivs": "31/31/31/31/31/31",
            "conditions": "",
        },
        # Test 2: Ogerpon-W +2 Ivy Cudgel (Adamant 252 Atk Wellspring Mask) vs Skarmory (Impish 252 HP / 252 Def Lefties)
        # Expected: clean OHKO. Ivy Cudgel is Water-type here (form override).
        {
            "name": "Ogerpon-W +2 Ivy Cudgel vs Skarmory",
            "attacker": "Ogerpon-Wellspring", "atk_abil": "Water Absorb", "atk_item": "Wellspring Mask",
            "atk_nature": "Adamant", "atk_evs": "0/252/0/0/4/252", "atk_ivs": "31/31/31/31/31/31",
            "move": "Ivy Cudgel",
            "defender": "Skarmory", "def_abil": "Sturdy", "def_item": "Leftovers",
            "def_nature": "Impish", "def_evs": "252/0/252/0/4/0", "def_ivs": "31/31/31/31/31/31",
            "conditions": "attacker-+2",
        },
        # Test 3: Tinkaton-Gamma Updraft (Calm 252 HP / 4 SpA / 252 SpD Lefties) vs Mega Flygon
        # Custom move: Flying special 100 BP. Note Strong Winds is set by Parasol Prayer -> 1x (instead of 4x with Flying/Dragon)
        # Actually Mega Flygon is Ground/Dragon. Flying is 1x vs Ground, 1x vs Dragon. Total: 1x. STAB on Tinkaton-G (Fairy/Flying) -> 1.5x.
        {
            "name": "Tinkaton-Gamma Updraft vs Mega Flygon",
            "attacker": "Tinkaton-Gamma", "atk_abil": "Parasol Prayer", "atk_item": "Leftovers",
            "atk_nature": "Calm", "atk_evs": "252/0/0/4/252/0", "atk_ivs": "31/31/31/31/31/31",
            "move": "Updraft",
            "defender": "Mega Flygon", "def_abil": "Desert Spirit", "def_item": "",
            "def_nature": "Hardy", "def_evs": "0/0/0/0/0/0", "def_ivs": "31/31/31/31/31/31",
            "conditions": "",
        },
    ]
    for c in cases:
        print()
        print(f"--- {c['name']} ---")
        attacker = build_combatant(c["attacker"], c["atk_abil"], c["atk_item"] or None,
                                   c["atk_nature"], c["atk_evs"], c["atk_ivs"], 100)
        defender = build_combatant(c["defender"], c["def_abil"], c["def_item"] or None,
                                   c["def_nature"], c["def_evs"], c["def_ivs"], 100)
        move = find_move(attacker.mon, c["move"])
        ctx = Context()
        parse_conditions(c["conditions"], attacker, defender, ctx)
        result = compute_damage(attacker, defender, move, ctx)
        print(format_result(attacker, defender, move, ctx, result))
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description="DeltaCalc damage engine (Python port of the in-game Kotlin engine).")
    p.add_argument("--self-test", action="store_true", help="Run the bundled self-test cases.")
    p.add_argument("--attacker"); p.add_argument("--attacker-ability"); p.add_argument("--attacker-item")
    p.add_argument("--attacker-nature", default="Hardy")
    p.add_argument("--attacker-evs", default="0/0/0/0/0/0")
    p.add_argument("--attacker-ivs", default="31/31/31/31/31/31")
    p.add_argument("--defender"); p.add_argument("--defender-ability"); p.add_argument("--defender-item")
    p.add_argument("--defender-nature", default="Hardy")
    p.add_argument("--defender-evs", default="0/0/0/0/0/0")
    p.add_argument("--defender-ivs", default="31/31/31/31/31/31")
    p.add_argument("--level", type=int, default=100)
    p.add_argument("--move")
    p.add_argument("--conditions", default="")
    args = p.parse_args(argv)
    if args.self_test:
        return run_self_test()
    missing = [k for k in ("attacker", "defender", "move") if getattr(args, k) is None]
    if missing:
        print(f"ERROR: missing required: {', '.join('--'+m for m in missing)}", file=sys.stderr)
        return 1
    return run_calc(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
