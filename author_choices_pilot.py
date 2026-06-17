#!/usr/bin/env python3
"""PILOT: author granular Must-take / Recommended pick guidance (`choices`) for
the Swords Bard Archer (rank 1) only, as a format check before rolling out to
the other builds. Each choice = {kind, req, items, note}; req is 'must' or 'rec'.
Sourced from build_transcripts/015 + the existing leveling data.

Idempotent. Re-run after editing. `uv run author_choices_pilot.py`
"""
import json
from pathlib import Path

SRC = Path("src") / "data" / "builds.json"

def C(kind, req, items, note=""):
    c = {"kind": kind, "req": req, "items": items}
    if note:
        c["note"] = note
    return c

# choices[level] = [C(...), ...]
CHOICES = {
    1: [
        C("skill", "must", ["Sleight of Hand", "Persuasion", "Deception"], "face skills + lockpicking on your high DEX"),
        C("skill", "rec", ["Stealth"], "enables stealth-archery openers later"),
        C("cantrip", "must", ["Minor Illusion"], "near-universal utility, basically required on everyone"),
        C("cantrip", "rec", ["Friends"], "consequence-free dialogue advantage"),
        C("spell", "must", ["Healing Word", "Dissonant Whispers", "Longstrider"], "bonus-action heal · 2-turn lockdown · party-wide speed (ritual)"),
        C("spell", "rec", ["Disguise Self"], "merchant prices / dialogue — or Speak with Animals"),
    ],
    2: [
        C("cantrip", "must", ["Vicious Mockery"], "enchantment cantrip → free bonus-action cast with Band of the Mystic Scoundrel"),
        C("spell", "rec", ["Tasha's Hideous Laughter"], "an enchantment to bonus-action later; swappable"),
    ],
    3: [
        C("subclass", "must", ["College of Swords"], "Slashing Flourish — two ranged attacks per action, the build's engine"),
        C("expertise", "must", ["Sleight of Hand", "Persuasion"], "double proficiency on your key skills"),
        C("style", "rec", ["Archery"], "+2 to hit ranged — or Two-Weapon Fighting if you'll melee flourish"),
        C("spell", "rec", ["Cloud of Daggers"], "or another control spell"),
    ],
    4: [
        C("spell", "must", ["Hold Person"], "enchantment lockdown — auto-fail saves, bonus-action via Mystic Scoundrel"),
    ],
    5: [
        C("spell", "must", ["Hypnotic Pattern"], "the best AOE control in the game; bonus-action it after an attack"),
        C("spell", "rec", ["Glyph of Warding"], "pre-placed burst, or hold for Counterspell later"),
    ],
    6: [
        C("spell", "rec", ["Enhance Ability"], "advantage/utility — or Slow / Glyph; nothing forced here"),
    ],
    7: [
        C("style", "must", ["Archery"], "+2 to hit with every ranged attack — the whole point of the Fighter dip"),
    ],
    9: [
        C("spell", "must", ["Confusion"], "AOE enchantment; bonus-action via Mystic Scoundrel to shut down a fight"),
        C("spell", "rec", ["Greater Invisibility"], "if you like stealth-archery; otherwise skip"),
    ],
    10: [
        C("spell", "rec", ["Freedom of Movement"], "anti-control insurance — or swap for utility"),
    ],
    11: [
        C("spell", "must", ["Hold Monster"], "single-target lockdown on bosses immune to Hold Person"),
    ],
    12: [
        C("spell", "must", ["Counterspell"], "Magical Secrets — the best reaction in the game"),
        C("spell", "rec", ["Banishing Smite"], "burst finisher — or Globe of Invulnerability / another AOE"),
    ],
}


def main() -> int:
    builds = json.loads(SRC.read_text(encoding="utf-8"))
    b = next(x for x in builds if x.get("rank") == 1)
    for st in b.get("leveling", []):
        st.pop("choices", None)
        if st["level"] in CHOICES:
            st["choices"] = CHOICES[st["level"]]
    SRC.write_text(json.dumps(builds, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"authored choices for {b['name']}: "
          f"{sum(len(v) for v in CHOICES.values())} picks across {len(CHOICES)} levels")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
