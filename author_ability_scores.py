#!/usr/bin/env python3
"""Add concrete starting ability-score arrays to each build (replacing the prose
`abilities` field in the UI). Per the user's rule: prefer EVEN numbers (odd points
are wasted on the modifier) and put the odd / elixir / Ethel's-Hair variant in the
note. Post-racial-bonus values. Swords Bard + EK Thrower arrays are transcript-
sourced (015 / 016); the rest are the standard honour-mode spreads.

Idempotent. `uv run author_ability_scores.py`
"""
import json
from pathlib import Path

SRC = Path("src") / "data" / "builds.json"

def A(STR, DEX, CON, INT, WIS, CHA, primary, note=""):
    d = {"STR": STR, "DEX": DEX, "CON": CON, "INT": INT, "WIS": WIS, "CHA": CHA,
         "primary": primary}
    if note:
        d["note"] = note
    return d

SCORES = {
    1: A(8, 16, 14, 8, 12, 16, ["DEX", "CHA"],
         "Want more durability? Drop CHA to 14 and run CON 16. With Gloves of "
         "Dexterity (sets DEX to 18) you can dump DEX to 8 and move those points "
         "into CON 16 / WIS 14."),
    2: A(8, 16, 16, 10, 14, 8, ["CON", "DEX"],
         "Elixir build: drink Hill/Cloud Giant Strength daily (it sets STR to "
         "23/27), so STR is dumped to 8. Min-max spread runs DEX 17 / CON 15 / "
         "INT 12 and evens them out with later feats. No elixir? Max STR instead."),
    3: A(8, 16, 14, 8, 16, 10, ["DEX", "WIS"],
         "The Strength elixir is effectively required — it sets STR, so dump it "
         "and run DEX 16 / WIS 16. Without the elixir the build is too ability-"
         "hungry to function."),
    4: A(8, 14, 16, 8, 12, 8, ["CON", "STR"],
         "Strength elixir (Hill/Cloud Giant) is required for this split — it sets "
         "STR, so dump it to 8 and pump CON 16. Tavern Brawler then adds the elixir "
         "STR to thrown attacks twice over."),
    5: A(8, 14, 16, 16, 10, 8, ["INT"],
         "One Sorcerer level is taken first for CON-save proficiency. With a +1 "
         "INT item or Auntie Ethel's Hair, start INT 17 to reach 18."),
    6: A(8, 14, 16, 8, 10, 16, ["CHA"],
         "Sorcerer is taken first for CON-save proficiency (concentration on "
         "Haste). +1 CHA item / Ethel's Hair → start CHA 17 for an eventual 18."),
    7: A(8, 14, 16, 8, 16, 10, ["WIS"],
         "Heavy-armour cleric, so DEX can stay low. +1 WIS item / Ethel's Hair → "
         "start WIS 17 to reach 18."),
    8: A(8, 14, 14, 8, 10, 16, ["CHA"],
         "Pure Sorcerer already grants CON-save proficiency. +1 CHA item / Ethel's "
         "Hair → start CHA 17 (move a point off CON if needed) to reach 18."),
    9: A(8, 16, 14, 8, 14, 8, ["DEX"],
         "Ranger wants some WIS for perception and spell saves. With Gloves of "
         "Dexterity (sets DEX 18), dump DEX and put the points into CON 16 / WIS 14."),
    10: A(8, 14, 16, 8, 16, 8, ["WIS"],
         "Wild-shape forms use their own stats, so only your WIS (spell DC) and CON "
         "(concentration + the bonus HP) matter — dump everything else."),
    11: A(8, 14, 16, 8, 10, 16, ["CHA"],
         "Every attack and smite scales off Charisma via Pact of the Blade. +1 CHA "
         "item / Ethel's Hair → start CHA 17 for an 18."),
}


def main() -> int:
    builds = json.loads(SRC.read_text(encoding="utf-8"))
    n = 0
    for b in builds:
        s = SCORES.get(b.get("rank"))
        if s:
            b["abilityScores"] = s
            n += 1
    SRC.write_text(json.dumps(builds, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"added ability-score arrays to {n} builds")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
