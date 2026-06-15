import json, collections

PATH = "src/data/tierlists.json"

rows = [
    ("Hexblade (Warlock)", "S+", "One level is now the best single level in the game — Charisma to weapon attacks, medium armour/shields/martial weapons, Eldritch Blast, Shield, and bonus-action Hex's Curse (+proficiency to every damage instance); a 1-2 level dip improves essentially any attacking build."),
    ("Death Domain (Cleric)", "S", "It's a cleric, so a one-level dip alone is elite (armour, Guidance, Bless, Shield, Healing Word) — and it adds double-targeted necromancy cantrips (great on a Bone Chill caster like Spore Druid), a Smite-sized Touch of Death, and necrotic-resistance ignoring; tons of break points."),
    ("Circle of the Stars (Druid)", "S", "An unusually multiclass-friendly druid — at just level 2 you get free Star forms (bonus-action damage/healing) and Dragon form's reliable-talent concentration, so a 1-sorcerer / 2-star splash makes almost any concentration build (Spirit Guardians, Haste) nearly un-droppable."),
    ("Oath of the Crown (Paladin)", "S", "Now the best paladin to dip — level-1 Righteous Clarity gives the party a +proficiency bonus to attacks (it offsets Great Weapon Master's penalty), plus level-2 smites, Warding Bond, and level-9 Charisma Spirit Guardians for radiant-orb melee; superb 2/5/11 break points."),
    ("Bladesinging (Wizard)", "S", "Two levels give full wizard casting plus survivability/concentration AC, and level 6 grants Extra Attack on a full caster — absurd with Paladin smites or Hexblade, and you can ignore Bladesong entirely to run a heavy-armour wizard with Extra Attack and Counterspell."),
    ("Path of the Giant (Barbarian)", "A", "Signpost abilities arrive late (level 5-6), so it's the core of a build rather than a dip, but Giant's Rage + Elemental Cleaver make any-weapon throwers devastating, with great 8/4 and 10/2 splits (Thief for double Boots of the Giants, Fighter for Action Surge)."),
    ("Arcane Archer (Fighter)", "A", "A fighter, so it multiclasses superbly; Arcane Shots add a 12/day level-4 Banish, can't-miss shots, and crowd control to any archery build, customisable like Battle Master — common 3/5/6 break points (archery only)."),
    ("Swarm Keeper (Ranger)", "A", "Competes with Gloomstalker at the level-3 dip but does something different — a resource-free per-turn blind (convertible to damage or a teleport) that works off ANY attack, including wild-shape forms, making a 3-ranger / 2-druid spider a strong early controller."),
    ("Swashbuckler (Rogue)", "A", "The level-3 kit (free disengage on melee, scaling initiative, ally-free sneak attack) is a sidegrade to Thief/Assassin, but its real draw is the level-4 Flick of the Wrist / Sand Toss — a bonus-action near-Extra-Attack that makes a 4/8 split great on almost any martial."),
    ("College of Glamour (Bard)", "B", "Strong but greedy — it needs ~6 levels before Mantle of Inspiration scales and bonus-action Command (Mantle of Majesty) comes online, so multiclassing is mostly small dips INTO it (Fighter/Warlock/Paladin) rather than a dip out; usually you just go 12."),
    ("Shadow Magic (Sorcerer)", "B", "A great monoclass but an awkward dip — a 3-level splash buys see-in-magical-darkness without the warlock caster-level tax, but limited sorcery points plus the Eversight Ring and Darkness items make the investment hard to justify; you'd rather just take more shadow-sorcerer levels."),
    ("Drunken Master (Monk)", "C", "Still little reason to take it — a 3-level investment buys only Drunken Technique (worse than Open Hand's flurries or Thief's second bonus action), and only the level-6 Redirect Attack enables a single niche retaliation build; in need of a rework."),
]

entry = {
    "key": "multiclasses",
    "subject": "Multiclassing (Patch 8 subclasses)",
    "context": "Baldur's Gate 3 honour mode guide — how well each Patch 8 subclass multiclasses (break points, synergies)",
    "is_gameplay_only": True,
    "tier_definitions": {
        "S+": "Gives way too much for minimal investment — improves almost any build",
        "S": "Both incredibly powerful and incredibly versatile across many splits",
        "A": "Multiclasses very well, mostly for new options/lateral shifts",
        "B": "A few strong multiclass builds, but usually better single-classed",
        "C": "Weak/situational early abilities — rarely worth a multiclass split",
    },
    "ratings": {name: tier for name, tier, _ in rows},
    "notes": {name: note for name, _, note in rows},
}

data = json.load(open(PATH))
assert not any(x["key"] == entry["key"] for x in data), f"{entry['key']} already present"
assert len(entry["ratings"]) == len(rows), "duplicate name!"
valid = {"S+", "S", "A", "B", "C", "D", "F"}
assert all(v in valid for v in entry["ratings"].values())
data.append(entry)
with open(PATH, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print(entry["key"], "added:", len(entry["ratings"]), "entries; total lists:", len(data))
print("tier spread:", dict(collections.Counter(entry["ratings"].values())))
