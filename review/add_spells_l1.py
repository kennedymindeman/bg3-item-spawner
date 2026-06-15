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
    ("Bless", "S", "+1d4 to attacks AND saves for up to 3 allies (10 turns, pre-castable, upcasts) — a massive game-long accuracy boost that offsets Great Weapon Master/Sharpshooter penalties; the spell still beats the Whispering Promise ring because it lasts the whole fight."),
    ("Chromatic Orb", "S", "Non-concentration damage plus a chosen surface — ice for prone-stun control, acid for -2 AC, fire/lightning to finish low-HP enemies; 3d8 thunder or 2d8 elemental, doubled vs wet. Huge damage and versatility."),
    ("Command", "S", "A wisdom-save 'Grovel' drops an enemy prone and skips its turn (or 'Drop' to disarm), no concentration, upcasts to hit more — pure action-economy theft and the core of many builds (Band of the Mystic Scoundrel, Extend, fiend warlock)."),
    ("Create or Destroy Water", "S", "Applies the broken Wet condition (double cold/lightning damage) and makes water for ice/electrified surfaces — a level-1 way to halve fights, and it saves your scarce honour-mode water bottles."),
    ("Dissonant Whispers", "S", "3d6 psychic (wisdom save for half) that also frightens for 2 turns with no concentration — effectively stuns a melee enemy AND gives bards/GOO warlocks real damage; lands reliably on low-wisdom melee."),
    ("Enhanced Leap", "S", "Ritual (free) that triples jump distance for 10 turns — a free bonus-action 'teleport' and big effective move-speed boost for the whole party. Mobility is king."),
    ("Healing Word", "S", "Bonus-action ranged heal — the best panic button to revive a downed ally, the way to re-apply buff-on-heal items (Whispering Promise / Hellrider's Pride) mid-fight, and a turn-saver. Belongs in every party."),
    ("Hex", "S", "Bonus action, +1d6 necrotic on every attack roll vs a target all day (re-applies free on kill) — absurd cumulative damage, especially with multi-hit Eldritch Blast; a level-1 spell worth hundreds of damage."),
    ("Hunter's Mark", "S", "The ranger Hex — +1d6 weapon-damage-type on every weapon attack all day, re-applies on kill; mechanically the same enormous value, so every ranger takes it."),
    ("Longstrider", "S", "Ritual (free), all-day +10 move speed castable on the whole party and summons — mobility for free; basically an S+ pick."),
    ("Magic Missile", "S", "Three auto-hit force missiles (no save, ignores line of sight) that split across low-HP targets and stack per-missile riders (Callous Glow, lightning charges) — guaranteed damage is the least-random thing in the game."),
    ("Sanctuary", "S", "Bonus-action, no-concentration — enemies can't directly target the warded ally, so your healer / haste-bot / concentration-holder becomes untouchable; one of the most versatile and powerful spells in the game."),
    ("Shield", "S", "Reaction +5 AC (prompted only when it turns a hit into a miss) that also nullifies Magic Missile — negates an enemy attack (often a whole turn) for free; worth dipping a class just to get it."),
    ("Armor of Agathys", "A", "Temp HP plus cold retaliation that upcasts well (and doubles vs wet) and lasts until depleted — solid on warlocks and the centrepiece of the broken Abjuration-wizard retaliation build."),
    ("Disguise Self", "A", "Ritual (free) for crime cover, racial dialogue/merchant bonuses, AND using race-locked items (Githyanki swords, Dwarven Thrower) or shapeshift-keyed gear at full power; gets stronger as you learn the game."),
    ("Ensnaring Strike", "A", "Cast on a weapon hit (bonus action) to root a melee enemy for 10 turns at no damage cost; very reliable with the ranger's Bounty Hunter giving disadvantage on the save."),
    ("Find Familiar", "A", "Ritual summon (Raven blinds) for scouting, pressure plates, soaking a hit, and triggering sneak attack — value limited mostly by your patience; near-S if you love micromanaging."),
    ("Fog Cloud", "A", "No-save AOE blind/obscure — wins fights when you keep enemies inside it (great on immobile bosses), and otherwise just hands your party advantage; also a guaranteed hiding spot for stealing."),
    ("Grease", "A", "Non-concentration AOE prone-stun on YOUR save DC (better than grease bottles), great for repeated stuns and breaking caster concentration — only docked from S because it's flammable."),
    ("Ice Knife", "A", "Like a cold Chromatic Orb — 1d10 + 2d6 cold AOE leaving an ice surface; redundant for wizards/sorcerers but a mainstay damage-and-control spell for druids, who lack Chromatic Orb."),
    ("Mage Armor", "A", "All-day base AC 13 (+ Dex) for unarmored casters — skip it early, but near-mandatory late once you want to wear powerful robes."),
    ("Tasha's Hideous Laughter", "A", "Wisdom-save full disable (10 turns) that, unusually, many incapacitation-immune bosses can still suffer — unreliable early but a fight-winner once your save DC is high."),
    ("Thunderous Smite", "A", "A smite that knocks prone + 10ft back (breaks concentration, cliffs) for damage comparable to Divine Smite — and you can stack both on one attack for huge burst; most paladins take it."),
    ("Bane", "B", "A tiny -1d4 to enemy attacks/saves, but uniquely useful late: it targets the often-weak Charisma save, few bosses are immune, and it softens a target up for a bigger spell — only worth it in long late-game fights."),
    ("Entangle", "B", "A big 10-turn AOE root (strength save) granting advantage on attacks — strong control, but flammable and partly superseded by the druid's free spider webs."),
    ("Feather Fall", "B", "Ritual (free) AOE no-fall-damage — mostly traversal/trap-skipping, but pairs with Enhanced Leap to use height safely in combat arenas; the quintessential handy B-tier spell."),
    ("Guiding Bolt", "B", "4d6 radiant plus advantage on the next attack; a solid cleric filler (and radiant for orb-stacking), but cantrips like Toll the Dead now cover ranged damage, so it's rarely a go-to."),
    ("Inflict Wounds", "B", "3d10 melee necrotic — the highest single-target level-1 damage (a cleric 'smite'), upcasts well and extends with sorcerer, but it puts the cleric in melee, so it's situational."),
    ("Shield of Faith", "B", "All-day +2 AC (any armour), but costs concentration that clerics/paladins usually want elsewhere — best on one-level cleric dips that have nothing else to concentrate on."),
    ("Sleep", "B", "A no-save full disable based on enemy HP totals — an all-star for the first ~3 levels, then it falls off a cliff as HP outscales it; you'll swap it out."),
    ("Thunderwave", "B", "2d8 thunder in a square that flings enemies ~27ft (con save half) — a decent panic/repositioning button into cliffs/hazards, but the con save lets the melee enemies you most want to push resist."),
    ("Wrathful Smite", "B", "A smite with a good rider — frightens for 2 turns (disadvantage + can't move), pinning a fleeing enemy next to your paladin/hexblade; lower damage than Thunderous Smite."),
    ("Burning Hands", "C", "3d6 fire cone on a bad (dexterity) save at close range — weak, but light clerics get it free and use it to finish low-HP enemies."),
    ("Cure Wounds", "C", "A touch heal whose numbers can't keep up with incoming damage (potions / Healing Word are better) — only notable now as a way to trigger a Star Druid's Chalice healing with your action."),
    ("Divine Favor", "C", "+1d4 radiant on attacks for 3 turns, but a paladin would rather smite; only worth it on a war-cleric-dip weapon build doing radiant-orb / reverberation."),
    ("Expeditious Retreat", "C", "All-day bonus-action dash, but it costs concentration and is mostly superseded by Misty Step / Enhanced Leap — niche for dash-trigger and concentration-trigger item builds."),
    ("Faerie Fire", "C", "A big-radius advantage-granting / invisibility-revealing debuff (dex save), but Fog Cloud / Command / Entangle grant advantage too while doing more, so it's usually outclassed."),
    ("Hellish Rebuke", "C", "2d10 fire reaction — poor damage ratio, but useful for retaliation builds (Armor of Agathys), it works while raging, and a bug can delete multi-hit enemy attacks."),
    ("Heroism", "C", "Fear immunity + 5 temp HP/turn (upcasts to the whole party) — a pet pick that shines in a narrow set of long fights or as pre-Heroes'-Feast fear immunity, but needs many conditions to be good."),
    ("Protection from Evil and Good", "C", "A concentration buff giving disadvantage to aberrations/undead/fiends/etc (common in BG3) plus fear immunity — decent in those fights, but you usually want to concentrate on something proactive."),
    ("Speak with Animals", "C", "A ritual that bypasses some skill checks (and is fun), but the game floods you with animal-speaking potions, making the spell mostly redundant."),
    ("Witch Bolt", "C", "An embarrassing 1d12/turn normally — useless except as the single best spell for the one-shot Lightning Lord build (upcast + maximised + wet + auto-crit)."),
    ("Animal Friendship", "D", "The weakest crowd control — charm-only, on a wisdom save, and it only works in the game's few easy animal fights; just use Command instead."),
    ("Arms of Hadar", "D", "2d6 necrotic (strength save half) around a squishy caster that scales terribly on upcast — far too little damage to be worth a slot."),
    ("Charm Person", "D", "A marginal charm on a wisdom save (enemies have advantage) that's superseded by Friends in dialogue and useless in combat."),
    ("Color Spray", "D", "A no-save blind capped by enemy HP — it fails on the dangerous high-HP enemies, and Fog Cloud blinds with no HP cap while doing far more."),
    ("Compelled Duel", "D", "In BG3 it only gives disadvantage on attacks vs others (the 'must attack me' effect isn't implemented) — a bad trade for a paladin's bonus action, slot, and concentration."),
    ("False Life", "D", "7 temp HP that doesn't progress your game plan and blocks better temp-HP sources — a waste of a slot."),
    ("Goodberry", "D", "Summons four weak (1d4) healing berries in a game drowning in better potions; only relevant for infinite-long-rest camp-supply abuse."),
    ("Hail of Thorns", "D", "A bonus-action 1d10 AOE on a hit — negligible damage, a terrible ratio."),
    ("Ray of Sickness", "D", "2d8 of the game's worst damage type (poison) on a bad (con) save with a weak debuff — skip it."),
    ("Searing Smite", "D", "The worst smite — less up-front damage than Divine Smite and delayed; only ever used free by Zariel tieflings."),
]

entry = {
    "key": "spells_level_1",
    "subject": "Spells — Level 1",
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
