"""Set a `video` (source-video title) on every tier list so the app can render
a discrete YouTube link. Titles are the source guide names; the app links to a
YouTube search for `Cephalopocalypse <title>` (exact video IDs weren't captured
by get_transcripts.py)."""
import json

PATH = "src/data/tierlists.json"

SOURCES = {
    "arrows": "Arrows Tier List - BG3 Honour Mode Guide",
    "barrels": "Barrels, Satchels and Fireworks Tier List - BG3 Honour Mode Guide",
    "boots": "The BEST Boots in Baldur's Gate 3 - Tier List and Guide",
    "cantrips": "BG3 Cantrips Tier List [Updated] - Patch 8 Honour Mode Guide",
    "cloaks": "The COOLEST Items in BG3 - Complete Cloak Tier List and Guide",
    "cloth_armor": "Armor Tier List - Robes, Clothes and Cloth - BG3 Honour Mode Guide",
    "elixirs": "Elixir Tier List - BG3 Honour Mode Guide",
    "finesse_weapons": "The BEST Stabbing / Rogue Weapons in BG3 - Tier List and Guide",
    "gloves": "Gloves Tier List and Guide - BG3 (Acts 1-3)",
    "grenades": "Grenades Tier List - Throwables Ranked - BG3 Honour Mode Guide",
    "helmets": "Helmets Tier List and Guide - BG3 (Acts 1-3)",
    "light_armor": "Light Armour Tier List - BG3 Honour Mode Guide",
    "medium_armor": "BG3's BEST Armor - Medium Armor Tier List - Honour Mode Guide",
    "one_handed_weapons": "The BEST One Handed Weapons in BG3 - Tier List and Guide",
    "poisons_oils": "Poisons, Oils and Coatings Tier List - BG3 Honour Mode Guide",
    "polearms": "The BEST Polearms in Baldur's Gate 3 - Tier List and Guide",
    "potions": "Potions Tier List - BG3 Honour Mode Guide",
    "ranged_weapons": "The BEST Bows in Baldur's Gate 3 - Tier List and Guide",
    "rings": "Rings Tier List and Guide - BG3 (Acts 1-3)",
    "shields": "The BEST Shields in Baldur's Gate 3 - Tier List and Guide",
    "simple_weapons": "The BEST Simple Weapons in BG3 - Tier List and Guide",
    "skills": "Skills Tier List - BG3 Build Guide",
    "staves": "The BEST Staves in Baldur's Gate 3 - Tier List and Guide",
    "two_handed_weapons": "The BEST Two Handed Weapons in BG3 - Tier List and Guide",
    "versatile_weapons": "Versatile Weapons Tier List - BG3 (Acts 1-3)",
    "amulets": "The BEST Amulets in Baldur's Gate 3 - Tier List (Acts 1-3)",
    "heavy_armor": "BG3's STRONGEST Armor - Heavy Armor Tier List - Honour Mode Guide",
    "feats": "Feats Tier List [Updated] - BG3 Honour Mode Guide",
    "classes": "Class Tier List - Single Class Characters - BG3 Honour Mode Guide",
    "subclasses": "Subclass Tier List - Single Class Characters - BG3 (+ Patch 8 New Subclasses)",
    "illithid_powers": "Illithid Powers Tier List - BG3 Honour Mode Guide (Part 1 & 2)",
    "multiclasses": "New Subclass Multiclass Tier List - BG3 Honour Mode Guide",
    "spells_level_1": "BG3 Spells Tier List - Level 1 [Updated] - Honour Mode Guide",
    "spells_level_2": "BG3 Spells Tier List - Level 2 [Updated] - Honour Mode Guide",
    "spells_level_3": "BG3 Spells Tier List - Level 3 [Updated] - Honour Mode Guide",
    "spells_level_4": "BG3 Spells Tier List - Level 4 [Updated] - Honour Mode Guide",
    "spells_level_5": "BG3 Spells Tier List - Level 5 [Updated] - Honour Mode Guide",
    "spells_level_6": "BG3 Spells Tier List - Level 6 [Updated] - Honour Mode Guide",
}

data = json.load(open(PATH))
missing = [x["key"] for x in data if x["key"] not in SOURCES]
assert not missing, f"no source title for: {missing}"
for x in data:
    x["video"] = SOURCES[x["key"]]
with open(PATH, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print("set video source on", len(data), "lists")
