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
    ("Globe of Invulnerability", "S", "A 10ft zone of total damage immunity — since most fights are damage races, it simply WINS them, including most hard boss fights; three turns of acting freely while enemies can't hurt you ends any encounter. Get a caster or scrolls in every honour party."),
    ("Heroes' Feast", "S", "All-day, no-concentration party (and summon) buff: +12 max HP (stacks with Aid), advantage on wisdom saves, and immunity to fear/disease/poison conditions — removes most late-game run-killers at once; the priority 6th-level cast (and great from a camp caster)."),
    ("Chain Lightning", "A", "10d8 lightning to a target that arcs to three more (doubles vs wet) — ~360 average damage on a wet group, ending many encounters; just shy of S because it's pure damage, but absurd cast from Markoheshkir (twinnable, short-rest)."),
    ("Otto's Irresistible Dance", "A", "NO-save single-target lockdown that bypasses legendary resistance and many incapacitation immunities — costs the target at least one turn (often the whole fight); the best tool for the one dangerous enemy in a boss fight, and Enchantment wizards can double it."),
    ("Planar Ally", "A", "A cleric summon worth a whole extra party member all day — the Djinni (crowd-control tank, at-will Misty Step) or the Deva (136 HP / 21 AC damage tank); the best cleric 6th-level cast after Heroes' Feast. (Avoid the Cambion.)"),
    ("Wall of Ice", "A", "10d6 cold + prone along a wall — but cast it and immediately CANCEL concentration to hit enemies with three instances of 10d6 (initial + cloud + start-of-turn), doubled vs wet: the highest theoretical damage in the game. Fiddly and its save DCs are bugged, else S."),
    ("Create Undead", "B", "Summons a 93 HP mummy brawler — weaker than the other 6th-level summons and can't be healed (undead), so it lasts a fight or two; still good value as a warlock Mystic Arcanum or from the Crypt Lord's Ring."),
    ("Eyebite", "B", "A recastable (10-turn) wisdom-save disable — the 'panicked' mode applies Fear's flee-and-can't-act condition for a full 10 turns (no reduced duration); hasted, you lock down two enemies a turn and can end fights, though it competes with stronger options."),
    ("Otiluke's Freezing Sphere", "B", "10d6 cold AOE + ice surface — best made as a throwable 'grenade' and handed to a multi-attacker with high spell DC (sword bard, Hexblade, Bladesinger) so a 6th-level spell costs only part of a turn; also reverse-pickpocketable for a delayed nuke."),
    ("Sunbeam", "B", "A recastable 6d8 radiant line (con save, one-turn blind that BG3's timing makes useless on enemy turns) — inefficient raw, but good when hasted (double-cast) and/or wearing radiating orbs; usually best from Blood of Lathander or scrolls."),
    ("Summon Deva (Sigil of the Celestials)", "B", "A secret spell that summons only the Deva (a strong 136 HP / 21 AC damage tank) — a fine summon, but a wizard's 6th slot is contested by Conjure Elemental myrmidons, Globe of Invulnerability, Chain Lightning and Wall of Ice, so it's a third priority."),
    ("Wall of Thorns", "B", "A druid 'three-in-one' (Wall of Fire + Plant Growth + Entangle): 7d8 piercing (doubles with Bloodthirst/Ballista) that double-dips and can trap enemies — held back by bugged DCs (damage save DC 3) and only half-speed terrain, but still useful layered with other AOE."),
    ("Arcane Gate", "C", "Links two points for free movement — mostly redundant with party mobility by this level, but it moves NPCs across an arena (a couple of encounters), can lure/trap enemies, and enables some exploits; a very low C."),
    ("Blade Barrier", "D", "A 6d10 wall — but its save DC is bugged to a FIXED 15 then 3, so enemies basically always halve it, and even unbugged it's too little damage and too hard to place for a precious cleric 6th slot."),
    ("Circle of Death", "D", "Fireball damage (8d6) in a big radius for a 6th-level slot on the worst save (Constitution) — a 'villain wipes a village' spell that simply doesn't do enough damage to be worth casting."),
    ("Disintegrate", "D", "10d6+40 force (~75) but a dex save NEGATES it entirely at only 30ft — a single-target spell that can do literal nothing; even when it lands, Chain Lightning does more to more enemies. Scrolls are okay vs low-dex foes."),
    ("Flesh to Stone", "D", "A multi-turn petrify that starts as a level-1 Entangle and needs four failed con saves to kill one enemy — a 6th slot to do what cheaper spells do better; funny, not good."),
    ("Harm", "D", "14d6 necrotic (con save) that, incredibly, CANNOT reduce an enemy below 1 HP — a damage spell that can't kill, with low damage and a bad save and damage type. An embarrassment."),
    ("Heal", "D", "Restores 70 HP — a lot, but purely reactive in a game where preventing/disabling beats healing, and you're swimming in high-level potions; never worth a 6th slot, even on a dedicated healer."),
    ("Wind Walk", "D", "Gaseous Form on the whole party — a 6th slot for the benefits of an already-marginal level-3 spell; just don't."),
]

entry = {
    "key": "spells_level_6",
    "subject": "Spells — Level 6",
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
