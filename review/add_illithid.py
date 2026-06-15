import json, collections

PATH = "src/data/tierlists.json"

entry = {
    "key": "illithid_powers",
    "subject": "Illithid Powers",
    "context": "Baldur's Gate 3 honour mode guide — rated mostly assuming the Zaith'isk bonus-action upgrade",
    "is_gameplay_only": True,
    "tier_definitions": {
        "S": "Extremely powerful mainstays — prioritise unlocking these",
        "A": "Strong abilities regularly, or very powerful occasionally",
        "B": "Solidly useful throughout the entire game",
        "C": "More situational — comes up, but not every encounter",
        "D": "Generally weak, but no illithid power is truly useless",
    },
    "ratings": {
        # Central / middle ring (Acts 1-2)
        "Psionic Overload": "S",
        "Favourable Beginnings": "S",
        "Cull the Weak": "S",
        "Shield of Thralls": "S",
        "Ability Drain": "A",
        "Luck of the Far Realms": "A",
        "Psionic Backlash": "A",
        "Illithid Persuasion": "B",
        "Force Tunnel": "B",
        "Stage Fright": "C",
        "Repulsor": "C",
        "Concentrated Blast": "C",
        "Transfuse Health": "D",
        "Charm": "D",
        "Displace": "D",
        "Perilous Stakes": "D",
        # Outer ring / elite (astral tadpole, Act 3)
        "Illithid Expertise": "S",
        "Black Hole": "S",
        "Fly": "S",
        "Psionic Dominance": "A",
        "Mind Blast": "A",
        "Freecast": "A",
        "Absorb Intellect": "B",
        "Displacer Beast Shape": "B",
        "Survival Instinct": "D",
        "Fracture Psyche": "D",
        "Mind Sanctuary": "D",
    },
    "notes": {
        "Psionic Overload": "A self-buff adding 1d4 psychic to EVERY attack you roll (multiplying across extra attacks, multi-hit spells, and crits) for a trivial 1d4 self-damage; not worth a full action, but as a bonus action via the Zaith'isk it's a huge damage spike on any attack-spam build.",
        "Favourable Beginnings": "A free passive that adds your proficiency bonus AGAIN to the first attack or ability check against each creature — lands the most important attack of every fight and turns the party face into a near-guaranteed dialogue passer, at zero action cost. Unlock it first.",
        "Cull the Weak": "Passive: any enemy you drop below your number of unlocked powers dies INSTANTLY (bypassing death-prevention and resistances) and explodes for AOE psychic; effectively adds ~5-20 damage to your attacks and only scales as you unlock more powers — thousands of effective damage over a run.",
        "Shield of Thralls": "Pre-castable 10 temp HP that, when broken, stuns every enemy within 30ft on a failed DC15 Intelligence save — a free, pre-combat AOE stun on a save enemies routinely fail, and an AOE one-turn stun wins fights.",
        "Ability Drain": "Free passive: each hit permanently shaves 1 off the stat you attacked with (Dexterity from finesse/ranged is best — lowers their AC and accuracy), with no save; marginal per stack but free, stackable across the party, and it applies a condition for reverberation/radiant-orb engines.",
        "Luck of the Far Realms": "Reaction to turn any hit into a guaranteed critical, once per long rest — S-tier on crit-hungry single-big-hit builds (Paladin smites, Rogue sneak attack, lightning builds); only the once-per-day limit keeps it out of S overall.",
        "Psionic Backlash": "Reaction dealing 1d4 psychic per spell level to a casting enemy (can break concentration), with no cooldown; re-rated up to A because it gives martials/archers a valuable use for an otherwise-idle reaction, useful in the hardest (caster) fights and it combos with Cull the Weak.",
        "Illithid Persuasion": "Replaces certain dialogue checks with a trivial DC2 Wisdom check (auto-pass after five uses); you start with it and never choose it, but it quietly smooths over checks and can hand you allies in a couple of fights.",
        "Force Tunnel": "Move 30ft in a line as a combined dash + disengage that knocks everything back 13ft with NO save, regardless of enemy size — weak as an action, but as a Zaith'isk bonus action it's a great reposition-plus-punt (off cliffs, into hazards) once per short rest.",
        "Stage Fright": "Large-AOE bonus-action debuff (Wisdom save) giving enemies disadvantage on attacks and 2d6 psychic on a miss; only worth it as a bonus action, and landing it depends on your often-low illithid save DC, so it's a minor but party-wide damage reducer.",
        "Repulsor": "A bigger Thunderwave (30ft around you, Strength save, 2d6 force + 20ft knockback, half on save), but it hits allies so you must be 30ft from your party, and Strength is a poor save to target for knockback — situational; Force Tunnel does no-save knockback more reliably.",
        "Concentrated Blast": "End your concentration to deal 3d6 no-save psychic (and heal if the target was concentrating); re-rated up to C because cheap concentration cantrips/ritual spells let you fire it off as a free bonus-action finisher, even if you shouldn't build around it.",
        "Transfuse Health": "Spend half your current HP to heal an ally that much (resistances/temp HP can cheat the cost); some cute tricks exist, but out-of-combat healing is essentially free in BG3, so it rarely matters.",
        "Charm": "A defensive reaction that only triggers AFTER an enemy's first attack, lets them retarget your allies anyway, and uses a Wisdom save enemies make with advantage — far weaker than Shield/Warding Flare; only free value if your reaction is otherwise idle.",
        "Displace": "Passive adding 1d8 psychic when YOUR actions cause falling damage; tiny, very situational, hard to trigger more than once per fight, and frequently bugged into doing nothing.",
        "Perilous Stakes": "On Honour Mode it can only target allies, granting damage vulnerability (lethal) for 2d8 heal-on-attack; its real (broken) enemy-vulnerability use is disabled here, leaving it as decent but unnecessary out-of-combat self-healing.",
        "Illithid Expertise": "Passive granting expertise in Persuasion, Deception, and Intimidation without needing the skills (like a free, no-cost Actor feat) — turns any character into a dominant Act 3 dialogue passer.",
        "Black Hole": "Short-rest AOE (Intelligence save) that pulls most of an encounter to one point and Slows them without using concentration — then recasts five more times as a bonus action; groups enemies for AOE nukes and traps them on hazard surfaces. The reason to dive the outer ring.",
        "Fly": "Free passive (no tadpole) granting flight that effectively doubles movement and ignores terrain at no action cost — the best mobility tool in the game, and you can give it to the whole party. Positioning is king.",
        "Psionic Dominance": "Effectively a free 4th-level Counterspell once per long rest against spells targeting you (auto-counters spells up to your proficiency bonus, ability check above that); A rather than S only because dedicated Counterspell is more flexible.",
        "Mind Blast": "Once-per-long-rest 47ft cone (Intelligence save) for 4d8+mod psychic and a full-turn STUN; the damage is modest by Act 3 but an AOE stun wins encounters outright — A only because it fires once a day and competes with Black Hole.",
        "Freecast": "Long-rest toggle that removes ALL costs of your next spell/ability (slot, sorcery points, dice) — roughly an extra 6th-level slot per day, best on sorcerers (also refunds metamagic points); pure adventuring-day longevity, near S-tier if you rest rarely.",
        "Absorb Intellect": "Cast on a creature for escalating Intelligence drain and 15d8 of healing over five turns (Intelligence save once); a solid heal and a safe way to assassinate low-Int enemies like Steel Watchers, but usually your bonus action is better spent on Black Hole/Mind Blast.",
        "Displacer Beast Shape": "Once-per-long-rest wild-shape into an 85 HP / 16 AC displacer beast with a guaranteed-teleport and triple attack; a competent but not top-tier combat form — best as a big bonus-action shield to tank one hit or fight when out of resources.",
        "Survival Instinct": "Pre-cast buff that heals an ally 3d4 instead of dropping to 0 (for three turns); preventing a death is nice, but it must be cast in advance on a target you predict will be hit, so it's rarely the best use of a bonus action.",
        "Fracture Psyche": "Short-rest single-target debuff (Intelligence save) lowering AC and saves by 1 (2 on a chain after a kill) for five turns — basically a weaker single-target Bane; occasionally used to set up an important spell, but low priority for your bonus action.",
        "Mind Sanctuary": "On Honour Mode it's simply AOE Haste (no stacking), which is fine but redundant by Act 3 — and it's badly bugged into sometimes eating a character's entire turn, which can lose an Honour run, so it's best avoided until fixed.",
    },
}

data = json.load(open(PATH))
assert not any(x["key"] == entry["key"] for x in data), f"{entry['key']} already present"
missing = [k for k in entry["ratings"] if k not in entry["notes"]]
assert not missing, f"missing notes: {missing}"
valid = {"S+", "S", "A", "B", "C", "D", "F"}
assert all(v in valid for v in entry["ratings"].values())
data.append(entry)
with open(PATH, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print(entry["key"], "added:", len(entry["ratings"]), "items; total lists:", len(data))
print("tier spread:", dict(collections.Counter(entry["ratings"].values())))
