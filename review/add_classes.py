import json, collections

PATH = "src/data/tierlists.json"

entry = {
    "key": "classes",
    "subject": "Classes (single-class)",
    "context": "Baldur's Gate 3 honour mode build guide — monoclass, level 12",
    "is_gameplay_only": True,
    "tier_definitions": {
        "S": "Phenomenally powerful AND versatile — slots into any party",
        "A": "Either supremely versatile or extremely powerful, but not both",
        "B": "More build-constrained; lacks A-tier power but still excellent",
        "C": "Constrained to one/two roles and not the best at them",
        "D": "Empty on purpose — there are no non-viable classes in BG3",
    },
    "ratings": {
        "Bard": "S",
        "Cleric": "S",
        "Sorcerer": "S",
        "Druid": "A",
        "Fighter": "A",
        "Paladin": "A",
        "Ranger": "A",
        "Warlock": "A",
        "Wizard": "A",
        "Barbarian": "B",
        "Monk": "B",
        "Rogue": "C",
    },
    "notes": {
        "Bard": "The most versatile class in the game — every skill plus easy expertise (best party face), Song of Rest sustain, and Magical Secrets to grab the best spells of any class; also among the highest ranged/melee damage and the easiest access to the broken Arcane Acuity / Band of the Mystic Scoundrel combos. Fills every role except summoning.",
        "Cleric": "Misjudged as pure support — domains let it tank, deal damage, control, or heal, all backed by broken mechanics it gets out of the box (radiant-orb stacking, Spirit Guardians, heal-on-buff Blade Ward/Bless items) plus Guidance, Bless, and Command. Doesn't compete for party items; only cost is heavier long-rest reliance.",
        "Sorcerer": "Quicken + Twin Spell let it cast multiple leveled spells per turn — impossible in tabletop — effectively taking two turns to everyone else's one with the game's best spell list and Charisma face access. The class most likely to become broken entirely by accident.",
        "Druid": "A full spellcaster with extra health bars (wild shape / Spore shield) and the best summon access (Woodland Being, Conjure Elemental); supremely versatile and its late-game spell list is superb, but it comes online slowly and wild-shape melee falls off — slightly lower raw power than the S-tier casters.",
        "Fighter": "The most versatile martial: any role via its huge feat access, plus Action Surge (a whole extra turn), three attacks at level 11, and Indomitable saves. Eldritch Knight is the single easiest honour-mode character to pilot — but all it does is hit things, and that damage caps below dedicated damage dealers.",
        "Paladin": "Smite attacks trade spell slots for the highest burst damage in the game, devastating on the easily-guaranteed crits, alongside Charisma face access, party-wide defensive auras, and Lay on Hands healing. Misses S only because there's one build path and it's the most long-rest-hungry, resource-greedy class.",
        "Ranger": "The archer build stacks Archery style + Sharpshooter + early extra attacks (Gloomstalker at level 3) for huge, reliable ranged damage from safety; tanky with elemental resistances, great perception/stealth, and no item conflicts. Held back only by a mid-game dead zone before its strong level-11 capstones.",
        "Warlock": "Eldritch Blast + Agonizing Blast IS the damage-dealer baseline; short-rest control (Hunger of Hadar), the Darkness + Devil's Sight immunity combo, and Charisma face access round it out. Low end of A — it mostly does one thing per fight, but that thing is excellent.",
        "Wizard": "The widest spell access in the game (scribe nearly any scroll) means it almost always has the perfect spell for the encounter, plus the strongest subclass variance (Abjuration's ward, Divination), Arcane Recovery, and good summons. Versatility over raw power, and squishy — you must build the party to protect it.",
        "Barbarian": "Highest HP plus Rage (extra damage + physical resistance), Reckless Attack (free advantage that also baits enemy aggro onto your tank), fast movement, and Feral Instinct's ~3/5 of Alert. Very high power but essentially one role (melee bruiser) and it competes hard for the contested uncapped medium armors and strength elixirs.",
        "Monk": "Moves fast, hits hard (Flurry of Blows + the broken Tavern Brawler giving ~99% accuracy), and stuns — the strongest linear strategy in the game. But it's extremely multi-attribute dependent (STR/DEX/CON/WIS), squishy, and a monoclass monk lacks the Thief bonus action, so one bad positioning turn can end an honour-mode run.",
        "Rogue": "Level-1 skill expertise and sneak-attack burst are great, but no Extra Attack and the once-per-turn sneak-attack cap limit its damage, and a monoclass rogue gains almost nothing after level 3 (just a d6 every two levels). It falls steadily behind as a damage dealer while still demanding party resources and protection.",
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
