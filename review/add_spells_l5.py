import json, collections

PATH = "src/data/tierlists.json"

SPELL_TIER_DEFS = {
    "S": "Critical — take it whenever available and cast it constantly",
    "A": "Great workhorse spells; mainstays of your strategy",
    "B": "Very useful — high impact in the right situations",
    "C": "Marginal — for specific builds or narrow encounters",
    "D": "Weak — usually safe to skip",
}

rows = [
    ("Conjure Elemental", "S", "The best high-level summon — all eight elemental/myrmidon options are viable, each basically a whole extra party member for the day; the best use of your 5th slot, and usually beats every actual 6th-level spell when upcast."),
    ("Curriculum of Strategy: Artistry of War", "S", "A secret-spell super Magic Missile — six auto-hit, no-save bolts (2d6+6 each, ~72 total, minimum 48) that split across targets and trigger per-hit riders (Hex, Phalar Aluve) six times; once per short rest, hugely reliable, and broken in a magic-missile build."),
    ("Destructive Wave", "A", "A cleric-only 30ft AOE (10d6 thunder/radiant, con save) that also knocks enemies prone, no concentration, enemies-only — relevant damage types for itemisation and great prone-stacking under Spirit Guardians; Tempest/Light clerics always have it."),
    ("Hold Monster", "A", "Hold Person for (almost) any creature — paralysis with auto-crits, the game's most devastating condition; very expensive (5th slot, caps at two targets) so you prefer Hold Person when it works, but a fight-winner when it doesn't. Great with Band of the Mystic Scoundrel."),
    ("Banishing Smite", "B", "A smite adding 5d10 force that BANISHES anything dropped below 50 HP (no save) — effectively ~75-100 bonus damage to one target with a guaranteed crit; mainly a Hexblade pick (or a bard's Magical Secrets), used when you really want something dead."),
    ("Cone of Cold", "B", "8d8 cold (con save, doubles vs wet) in a 30ft cone — mediocre solo, but DOUBLE cone of cold (two casters / a scroll) on a wet, grouped pack is ~144 AOE damage plus an ice surface that ends encounters; also the Hexblade's best AOE burst."),
    ("Telekinesis", "B", "Pick up and throw an object or enemy each turn (no weight limit, 60ft, any direction) — reposition foes into hazards, yank them off high ground, or hurl normally-immovable enemies off cliffs; cast on an object first to dodge the save-cancels-it bug."),
    ("Cloudkill", "C", "A big movable poison cloud (5d8, con save, double-dips) — solid sustained damage when it works, but the worst save (Constitution) plus widespread poison immunity make it useless in many fights; great where it lands, and your party can stand in it with Heroes' Feast."),
    ("Contagion", "C", "A no-combat melee debuff (like Bestow Curse) — hit a neutral enemy pre-fight and, if they fail three con saves, inflict Flesh Rot (damage vulnerability) or Slimy Doom (stun on any damage) to instantly win; but it's a 5th slot vs Bestow Curse's 2nd, and poison/disease immunity is common."),
    ("Flame Strike", "C", "10d6 radiant/fire AOE (dex save) — basically a smaller upcast Fireball for a 5th slot, only notable because non-Tempest/Light/Death clerics lack other AOE burst; usually just do Spirit Guardians damage instead."),
    ("Dethrone", "D", "A secret-spell single-target nuke (10d6+20 necrotic) crippled by a bugged fixed DC 18 con save, the worst save, widely-resisted necrotic, and a once-per-LONG-rest cooldown — unreliable and not even better than upcast Inflict Wounds."),
    ("Dispel Good and Evil", "D", "A buggier, self-only, 10-turn version of the 1st-level Protection from Evil and Good for a 5th slot — one of the very worst spells in the game; never cast it."),
    ("Dominate Person", "D", "Mind-control one humanoid (wisdom save, repeated saves on damage, no real action control) — a 5th slot to swap a single enemy when you could just disable the whole encounter; items/scrolls cover the rare story uses."),
    ("Greater Restoration", "D", "Removes charm/petrify/stun/curse — but Freedom of Movement breaks stuns for a cheaper slot with an all-day buff, Remove Curse handles curses, and petrification basically never happens; no real use case."),
    ("Insect Plague", "D", "4d10/turn piercing (con save), but it damages at END of turn (no double-dip) and is barely more than a level-2 Cloud of Daggers — far too little damage for a 5th slot."),
    ("Mass Cure Wounds", "D", "AOE ~3d8 heal — healing can't keep up with incoming damage, and Mass Healing Word applies the buff-on-heal items for a bonus action and a 3rd slot; conceptually weak and the numbers don't back it up."),
    ("Planar Binding", "D", "Dominate Person for celestials/elementals/fey/fiends — same unreliability, and most such enemies are outright immune to domination; Hold Monster does the lockdown job better."),
    ("Seeming", "D", "Disguise Self on the whole party for a 5th slot — pointless, since only one character can be in a conversation and Disguise Self is a free level-1 ritual anyway; a contender for worst spell in the game."),
    ("Wall of Stone", "D", "A blocking wall, but each 30 HP segment dies in a hit or two (the AI smashes through), it costs concentration + a 5th slot, and BG3's fiddly wall targeting often spawns it with holes — too tricky to be reliable, however cool it is."),
]

entry = {
    "key": "spells_level_5",
    "subject": "Spells — Level 5",
    "context": "Baldur's Gate 3 honour mode guide (Patch 8 updated spell tier list)",
    "is_gameplay_only": True,
    "tier_definitions": SPELL_TIER_DEFS,
    "ratings": {name: tier for name, tier, _ in rows},
    "notes": {name: note for name, _, note in rows},
}

data = json.load(open(PATH))
assert not any(x["key"] == entry["key"] for x in data), f"{entry['key']} already present"
assert len(entry["ratings"]) == len(rows), "duplicate spell name!"
valid = {"S+", "S", "A", "B", "C", "D", "F"}
assert all(v in valid for v in entry["ratings"].values())
data.append(entry)
with open(PATH, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print(entry["key"], "added:", len(entry["ratings"]), "spells; total lists:", len(data))
print("tier spread:", dict(collections.Counter(entry["ratings"].values())))
