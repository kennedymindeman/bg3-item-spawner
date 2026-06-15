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
    ("Conjure Woodland Being", "S", "Several spells in one — a dryad that grants party difficult-terrain/paralysis/restraint immunity and poison resistance, casts Entangle and Spike Growth at will, and summons a regenerating Woad tank each short rest; basically a free extra party member, and the reason druids spike so hard at level 7."),
    ("Conjure Minor Elemental", "A", "All-day summons — usually the two flying Myrmidons for strong cold damage + a free ice surface every attack, or detonate both for a cold 'fireball' (double vs wet); like every summon, constant value across the whole day."),
    ("Greater Invisibility", "A", "Like Invisibility but it persists through attacks (on a rising stealth check) — a strong upfront-damage + surprise-round spell for any party, and absolutely broken if you build for stealth (Pass Without Trace + expertise) to end fights before they start."),
    ("Ice Storm", "A", "Mediocre damage (2d8 + 4d6 cold, doubles vs wet), but it lays a big 20ft ice surface WITHOUT concentration — the perfect follow-up to a concentration control spell (drop it on Spike Growth / Hunger of Hadar) to prone-stun a whole group each turn."),
    ("Wall of Fire", "A", "5d8 fire (dex save half) along a line that re-burns enemies each turn — single-handedly wins act-2 encounters where weak melee charge at you, devastating down a corridor, and excellent sustained damage on anything held in place; evocation wizards can stand in their own."),
    ("Banishment", "B", "Removes an enemy for two turns (then they skip a turn) on a CHARISMA save — far less control than Hold Person, but it lands far more reliably (many dangerous bosses have terrible charisma saves), and you can set traps where they'll reappear."),
    ("Confusion", "B", "An enemies-only AOE (so usable when your party is mixed in) that 50/50 stuns or triggers the chaotic 'madness' AI — strong when you isolate them (shut the door and let them blow each other up), but unreliable, so usually a second choice to Fear/Hypnotic Pattern."),
    ("Evard's Black Tentacles", "B", "A bigger (20ft), non-flammable Entangle that chips 3d6/turn — usually not worth a level-4 slot over Web/Entangle, but great on Great Old One warlocks (who pay no premium) and for layering Wall of Fire on top. (BG3's repeated saves make it weaker than tabletop.)"),
    ("Freedom of Movement", "B", "All-day paralysis/restraint immunity that ALSO breaks a stun on cast (including the haste-drop lethargic stun) — a powerful, action-neutral panic button; usually you avoid spending real slots on it, but a Tempest cleric gets it free, and it's vital solo."),
    ("Guardian of Faith", "B", "A no-concentration 60 HP / 20 AC summon that zaps nearby enemies (and is big enough to wall off a doorway) — strong board control that runs alongside Spirit Guardians/Spiritual Weapon; needs the right battlefield and party to shine."),
    ("Staggering Smite", "B", "A Hexblade smite (4d6 psychic, wisdom save to also stagger — disadvantage + no reactions) — costly on warlock concentration, but great burst on a weapon-attacking Hexblade, especially doubled by the Resonant Stone; mostly valuable just to have available."),
    ("Blight", "C", "8d8 single-target necrotic on the worst save (Constitution) and the worst damage type (necrotic, widely resisted) at short range — almost always worse than upcast Inflict Wounds; only okay for a death cleric vs the act-2 plants or a Staff of Cherish Necromancy build."),
    ("Dimension Door", "C", "Teleport yourself + an adjacent ally a long way, but it costs your whole action (unlike Misty Step) — only worth preparing for the few (mostly act-3, timed) encounters that demand crossing a big distance fast, or dragging an NPC along."),
    ("Fire Shield", "C", "Elemental resistance + melee retaliation (2d8) — but it mostly just redirects enemy aggro elsewhere, so it only pays off on builds that WANT to be hit (Abjuration wizard, barbarian) or as part of an Armor of Agathys retaliation stack; expensive otherwise."),
    ("Grasping Vine", "C", "A bonus-action, no-concentration summon that lays an Entangle surface and pulls enemies into it — neat for dragging foes into Hunger of Hadar, but a level-4 slot competes with Conjure Woodland Being / Ice Storm / Wall of Fire, so rarely cast."),
    ("Otiluke's Resilient Sphere", "C", "A no-save 'banishment' you cast on an ALLY to bubble them out of danger for three turns — mainly to keep a suicidal NPC ally alive in a couple of act-2 fights; as an offensive (dex-save) version of Banishment it's worse and can't hit big enemies."),
    ("Phantasmal Killer", "C", "Single-target root + 4d10 psychic that needs the enemy to fail TWO wisdom saves to do anything — too unreliable for a wizard's level-4 slot; only mildly interesting on a high-DC Hexblade (free upcast, psychic synergy with Resonant Stone)."),
    ("Polymorph", "C", "Turns an enemy into a 3 HP sheep for five turns (full disable), but ANY damage reverts them — BG3 cripples it vs tabletop; its real use is moving normally-immovable enemies (a sheep can be thrown/shoved off a cliff for an instant kill)."),
    ("Death Ward", "D", "Prevents one drop to 0 HP — but it's purely reactive, costs a level-4 slot, and frequently fails against multi-instance damage; better to spend a camp-caster slot on Freedom of Movement (outside the infinite-action bug)."),
    ("Dominate Beast", "D", "Mind-control a beast (wisdom save, repeated saves on damage) — a fine effect with almost no targets, since you've cleared every dangerous beast fight long before you get the spell."),
    ("Stoneskin", "D", "Concentration resistance to NON-magical physical damage — but most level-4-era damage is magical, it doesn't stack with the free Blade Ward, and chaining the right fights to use it isn't worth the effort."),
]

entry = {
    "key": "spells_level_4",
    "subject": "Spells — Level 4",
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
