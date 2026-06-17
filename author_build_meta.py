#!/usr/bin/env python3
"""Merge the redesign metadata into src/data/builds.json:

  - per-build `tag`   : compact list-row differentiator (class shorthand + 2nd role)
  - per-build `respecNote` : one-line respec guidance where the lead class is flexible
  - per-entry `spike` : {type: combat|utility|defensive, note} on real power-spike levels
  - per-entry `dipMin`: min TOTAL level at which a flexible dip pick is worth assigning
                        in a respec (the app skips it below that level, so the lead class
                        changes with respec level — the "different starting class" case)

Idempotent: re-running overwrites these fields. Keyed by build rank and entry level.
Sourced from build_transcripts/ + the existing leveling[] content; not fabricated.

    uv run author_build_meta.py
"""

import json
from pathlib import Path

SRC = Path("src") / "data" / "builds.json"

TAGS = {
    1:  "Bard · +face/control",
    2:  "Fighter · thrown nova",
    3:  "Monk · melee burst",
    4:  "Barb/Rogue · thrown",
    5:  "Wizard · tanky control",
    6:  "Sorc/Cleric · lightning nuke",
    7:  "Cleric · support/blast",
    8:  "Sorcerer · fire blaster",
    9:  "Ranger/Rogue · burst archer",
    10: "Druid · tanky shapeshifter",
    11: "Pally/Lock · CHA smite",
}

RESPEC_NOTES = {
    1: "The 2-level Fighter dip (Archery style + Action Surge) comes after Bard 6 — "
       "respeccing below level 7, stay pure Bard.",
    2: "Respeccing? Start with Fighter for the 19–20 base-AC chassis. The War Cleric "
       "dip (bonus-action thrown attacks) is optional — slot it once you're level 5+, "
       "or skip it entirely for a third attribute feat.",
}

# spike[rank][level] = (type, note)
SPIKES = {
    1: {
        1:  ("utility",  "Expertise + Bardic Inspiration — best dialogue/skills in the party from turn one."),
        3:  ("combat",   "Slashing Flourish (College of Swords) — two ranged attacks per action, the build's core."),
        4:  ("combat",   "Sharpshooter — the flat damage multiplier on every hit."),
        6:  ("combat",   "Extra Attack — Slashing Flourish now lands four ranged hits per action."),
        8:  ("combat",   "Action Surge (Fighter 2) — a full second volley; opening-turn nova."),
        12: ("utility",  "Magical Secrets (Bard 10) — Counterspell and other top-tier non-bard spells."),
    },
    2: {
        1:  ("defensive","Fighter chassis — ~20 base AC and strong from level one; no 'wait for it to come online'."),
        3:  ("combat",   "Action Surge (Fighter 2) — an extra full action of thrown attacks."),
        4:  ("combat",   "Eldritch Knight (Fighter 3) — bind your thrown weapon so it returns; War Magic bonus action."),
        6:  ("combat",   "Extra Attack (Fighter 5) — doubles your thrown attacks."),
        12: ("combat",   "Improved Extra Attack (Fighter 11) — three attacks; with the bonus-action throw + Action Surge, a massive thrown nova."),
    },
    3: {
        3:  ("combat",   "Way of the Open Hand (Monk 3) — Flurry of Blows riders: knock prone, push, or deny reactions."),
        5:  ("combat",   "Extra Attack + Stunning Strike (Monk 5) — lock down bosses for the party."),
        8:  ("combat",   "Thief (Rogue 3) — a second bonus action = an extra Flurry of Blows; the unarmed-DPS spike."),
    },
    4: {
        1:  ("defensive","Rage — resistance to physical damage; a durable frontliner immediately."),
        3:  ("combat",   "Berserker (Barb 3) — Frenzy grants a bonus-action thrown attack every turn."),
        4:  ("combat",   "Tavern Brawler — Strength counted twice on thrown attacks; the damage engine."),
        8:  ("combat",   "Thief (Rogue 3) — extra bonus-action throw stacks more attacks."),
    },
    5: {
        1:  ("defensive","Armour of Agathys + Shield from the Sorcerer-1 dip — early durability."),
        3:  ("defensive","Abjuration (Wizard 2) — Arcane Ward soaks damage and refreshes on every abjuration; near-unkillable."),
        6:  ("combat",   "Counterspell + Glyph of Warding — shut down enemy casters and pre-place burst."),
        12: ("combat",   "Level-6 spells (Chain Lightning) — your scaling control/damage online."),
    },
    6: {
        1:  ("utility",  "Create Water — sets up Wet to double your lightning/cold damage."),
        2:  ("combat",   "Destructive Wrath (Tempest Cleric 2) — max-roll the damage of a lightning/thunder spell."),
        7:  ("combat",   "Lightning Bolt + Haste, with Quicken/Twin metamagic — the nuke turns begin."),
        12: ("combat",   "Divination Wizard 2 — Portent dice + scribe Chain Lightning; Heightened max-damage nukes."),
    },
    7: {
        1:  ("utility",  "Full support online — Bless, healing, Sacred Flame, Guidance."),
        5:  ("combat",   "Spirit Guardians (Cleric 5) — the cleric damage + control engine."),
        11: ("utility",  "Heroes' Feast + Heal (Cleric 11) — party-wide buffs and big single-target healing."),
    },
    8: {
        3:  ("combat",   "Scorching Ray (Sorc 3) — strong multi-hit single-target early."),
        5:  ("combat",   "Fireball + Haste, with Twin/Quicken metamagic — the blaster turns begin."),
        11: ("combat",   "Level-6 spells + max sorcery points — double-Fireball / Quickened nova."),
    },
    9: {
        4:  ("combat",   "Sharpshooter — the flat damage multiplier on every shot."),
        5:  ("combat",   "Gloomstalker (Ranger 5) — Dread Ambusher: an extra first-turn attack + invisibility in the dark."),
        8:  ("combat",   "Assassin (Rogue 3) — auto-crit on the surprised/first turn; a huge alpha strike."),
        10: ("combat",   "Action Surge (Fighter 2) — doubles the opening burst."),
    },
    10: {
        1:  ("defensive","Wildshape HP pool — a disposable second health bar; tanky from level one."),
        4:  ("combat",   "Tavern Brawler + early beast forms — reliable wildshape damage."),
        5:  ("combat",   "Call Lightning + stronger forms (Owlbear) — your damage spikes hard."),
        11: ("combat",   "Sunbeam + Myrmidon/elemental forms — late-game powerhouse."),
    },
    11: {
        1:  ("combat",   "Eldritch Blast + Hex (Hexblade) — ranged pressure and a CHA-scaling chassis."),
        5:  ("combat",   "Pact of the Blade + Thirsting Blade (Warlock 5) — extra attack with short-rest slots to fuel smites."),
        8:  ("combat",   "Divine Smite (Paladin 3) — dump warlock spell slots into burst smites."),
    },
}

# dipMin[rank][level] = min total level to assign this flexible dip pick in a respec.
DIPMIN = {
    1: {7: 7, 8: 8},   # Swords Bard: the Fighter dip is post-Bard-6
    2: {1: 5},         # EK Thrower: the War Cleric dip is optional; lead with Fighter below level 5
}


def main() -> int:
    builds = json.loads(SRC.read_text(encoding="utf-8"))
    for b in builds:
        rank = b.get("rank")
        if rank in TAGS:
            b["tag"] = TAGS[rank]
        if rank in RESPEC_NOTES:
            b["respecNote"] = RESPEC_NOTES[rank]
        else:
            b.pop("respecNote", None)
        spikes = SPIKES.get(rank, {})
        dipmin = DIPMIN.get(rank, {})
        for st in b.get("leveling", []):
            lv = st["level"]
            # clear stale fields so re-runs are clean
            st.pop("spike", None)
            st.pop("dipMin", None)
            if lv in spikes:
                t, note = spikes[lv]
                st["spike"] = {"type": t, "note": note}
            if lv in dipmin:
                st["dipMin"] = dipmin[lv]
    SRC.write_text(json.dumps(builds, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    n_spikes = sum(len(v) for v in SPIKES.values())
    print(f"tagged {len(TAGS)} builds, {len(RESPEC_NOTES)} respec notes, "
          f"{n_spikes} spikes, {sum(len(v) for v in DIPMIN.values())} dipMin flags")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
