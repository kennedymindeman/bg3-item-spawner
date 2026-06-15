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
    ("Aid", "S", "All-day, no-concentration +5 (and more on upcast) to MAX HP for the whole party AND every summon within range — multiplies the value of fragile summons and gives huge party-wide survivability; cast it from a camp follower for free."),
    ("Cloud of Daggers", "S", "No-save, no-roll 4d4 slashing both on cast and at the start of each enemy turn (~8d4 before they act) in a decent AOE — guaranteed damage that just wins fights, great single-target or AOE; pairs with anything that traps enemies in it."),
    ("Darkness", "S", "An AOE blind that also blocks ranged attacks across it; the core of the broken Darkness + Devil's Sight strategy (your party advantage/ranged-immunity, enemies disadvantage), and it solves any fight with ranged attackers on its own."),
    ("Hold Person", "S", "Wisdom-save paralysis — the most debilitating condition, granting AUTO-CRITS to every attack within 10ft; locks down humanoids and is THE burst-damage setup, near-unbeatable with high save DC (Arcane Acuity / Band of the Mystic Scoundrel)."),
    ("Misty Step", "S", "A bonus-action 60ft teleport with no opportunity attacks — top-five spell in the game; escape, reposition, reach squishy enemies, dodge AOE. Every honour-mode character should have access (spell or item)."),
    ("Shadow Blade", "S", "Bonus action, an all-day finesse weapon doing 2d8-4d8 psychic with auto-advantage in dim light — more damage than any early weapon, free 4d8 upcast on warlocks, and absolutely broken with the psychic-vulnerability Resonant Stone."),
    ("Spike Growth", "S", "A huge (40ft across) non-flammable difficult-terrain zone dealing 2d4 per 5ft moved — single-handedly wins most melee Act 1 encounters (put Cloud of Daggers on top), and casters with Land's Stride walk through it freely."),
    ("Spiritual Weapon", "S", "Bonus-action, no-concentration summon — best understood as free crowd control: it baits attacks (resists all damage), blocks doorways, and chips in damage every turn at almost no opportunity cost. Great early and late."),
    ("Flaming Sphere", "A", "A durable (resists physical) summon that deals guaranteed fire each turn, soaks several attacks, blocks movement, and rams enemies as a bonus action — tons of accrued value over a fight; excellent until enemies can one-shot it."),
    ("Heat Metal", "A", "No-save 2d8 fire plus disadvantage-on-attacks or disarm vs any metal-armed/armoured enemy (most dangerous foes), repeatable each turn — very strong despite being buggy (and you can even drop concentration and keep the debuff)."),
    ("Invisibility", "A", "Concentration buff for scouting/positioning, a panic button to save an ally (or the whole party on upcast), and free traversal of hostile areas — doesn't win fights alone but is useful in countless situations; conserves invisibility potions."),
    ("Magic Weapon", "A", "All-day +1 to +3 (on upcast) attack and damage on a weapon — small but always-relevant, and excellent specifically for characters with nothing else to concentrate on (Eldritch Knight, paladin, arcane trickster, a wizard-dip sword bard)."),
    ("Moonbeam", "A", "The highest average level-2 damage — 2d10 radiant (con save) on cast and each enemy turn, and you can move it to chase enemies; efficient, though radiant-orb/Cull-the-Weak riders don't trigger (it counts as a summon)."),
    ("Scorching Ray", "A", "Three fire beams (2d6 each, attack rolls) splittable across targets — strong non-concentration damage that doubles under Hold Person and is THE engine for fire Arcane Acuity stacking and upcast Scorching Ray builds."),
    ("Silence", "A", "Ritual (free) 20ft no-cast zone — start a fight by dropping it on enemy casters (and it blocks some honour-mode boss legendary actions); fight-winning when you can keep them inside it, just combine with something that stops movement."),
    ("Blindness", "B", "A rare non-concentration, 10-turn, ranged debuff (con save) — solid and easy to apply, and it targets Constitution so it works on high-wisdom or incapacitation-immune enemies; only docked because Fog Cloud/Darkness blind with no save."),
    ("Blur", "B", "Self-only concentration disadvantage-on-attacks-against-you — wizards prefer Mirror Image, but it makes melee Hexblades and (cheap-concentration) Eldritch Knights extremely hard to kill."),
    ("Calm Emotions", "B", "A big-AOE charm/fear/rage immunity that 'solves' specific puzzle fights (harpies, charmers) and, despite the tooltip, shuts off ANY enemy rage — including some honour-mode boss legendary actions; situational but great where relevant."),
    ("Crown of Madness", "B", "Unreliable (the tooltip lies — it just applies the chaotic 'madness' AI and marks the target hostile to its allies), but when you isolate line-of-sight you can turn a boss's adds against it or make AOE enemies blow each other up."),
    ("Detect Thoughts", "B", "Mediocre in dialogue, but it's a free (ritual) all-day concentration spell — the best way to hold a concentration for Strange Conduit / to fuel the Concentrated Blast illithid power without giving up a real spell."),
    ("Enhance Ability", "B", "Advantage on a chosen ability's skill checks — mostly redundant with Friends/Gloves of Thieving, but invaluable (and reassuring to have prepared) for the high-value Act 3 checks that are otherwise hard to boost."),
    ("Lesser Restoration", "B", "Removes paralysis/poison/blind/disease — a panic button against Hold Person (action-neutral, since the paralysed ally wasn't acting anyway) and it clears some all-day debuffs; you'll rarely cast it, but it's clutch when you do."),
    ("Mirror Image", "B", "Pre-castable +9 AC (shedding 3 per enemy miss) — strong on its own, but doubly good because the AI won't target high-AC characters, so it protects a concentration-holder or makes an already-armoured character untouchable."),
    ("Warding Bond", "B", "Splits an ally's damage with the caster (+1 AC/saves) and stacks with damage-reduction/resistance to actually lower total damage taken — strong on an Oath of the Crown paladin or a tanky front-liner (and broken via camp-casting)."),
    ("Web", "B", "Entangle for sorcerers/wizards — a 10-turn AOE root with a bigger radius and, helpfully, a Dexterity save (better vs the strength-based melee you most want to stop); same flammable downside."),
    ("Arcane Lock", "C", "Permanently locks a door — niche, but luring half an encounter through a doorway and locking it buys turns (enemies now break it down rather than bugging out), and it cheeses a few story events."),
    ("Enlarge/Reduce", "C", "A medium damage buff (Enlarge) or shrink enemies to throw them off cliffs / lower their strength saves, plus weight tricks for jump-down owlbear builds — a creative, situational toolbox spell."),
    ("Knock", "C", "Opens any lock, but almost every party already has a Sleight of Hand character and the game is winnable without opening anything — a costly backup for lockless parties."),
    ("Pass Without Trace", "C", "+10 stealth to the whole party — useless for most parties (you rarely roll stealth), but mandatory for the game-breaking greater-invisibility / stealth-archer strategy."),
    ("Protection from Poison", "C", "All-day, no-concentration poison resistance + advantage vs the poisoned condition — only matters in the handful of poison-heavy fights (some Act 2 encounters), but very relevant there."),
    ("Ray of Enfeeblement", "C", "Halves a strength-based attacker's weapon damage (con save to end), but it's a concentration debuff you'd rather spend on Hold Person and it whiffs on archers/finesse enemies — niche use is on debuff-immune bosses."),
    ("Shatter", "C", "Low, con-save AOE thunder (no better than Chromatic Orb's thunder) — mainly useful to one-shot Scrying Eyes (they have disadvantage and thunder vulnerability) and for Tempest clerics to maximise."),
    ("Barkskin", "D", "Sets AC to 16 (does nothing if you're already there) at the cost of concentration AND a slot — too weak and too expensive; just don't."),
    ("Branding Smite", "D", "Half the damage of a same-slot Divine Smite, plus wasted concentration/bonus action for a useless anti-invisibility rider — the worst level-2 smite."),
    ("Darkvision", "D", "See in (non-magical) dark out to 40ft — but most arenas are lit, many races have it innately, and you can just use a light source or a scroll. Don't spend a slot."),
    ("Enthrall", "D", "Forces a creature to stare at you with essentially no mechanical effect — Fog Cloud and Minor Illusion do the steal-distraction job far better."),
    ("Flame Blade", "D", "A 3d6 fire sword for a slot that doesn't add your modifier and can't be buffed — usually less than just swinging a real weapon, and druids only get one attack."),
    ("Gust of Wind", "D", "A ranged line-push (and cloud-dispel) that's outclassed by free bonus-action shoves and is too short (40ft) to knock archers off high ground — cool, rarely useful."),
    ("Melf's Acid Arrow", "D", "~15 single-target acid damage — pathetic for a level-2 slot (less than Cloud of Daggers, with an attack roll); a damage spell that does no damage."),
    ("Phantasmal Force", "D", "Butchered in translation — 1d6/turn (less than a cantrip) on an Intelligence save with repeated saves to escape, after losing its real tabletop effect entirely. Skip."),
    ("Prayer of Healing", "D", "Efficient OUT-of-combat group healing — which BG3 never needs, since you can rest or chug potions freely. No use case outside a no-rest challenge."),
    ("See Invisibility", "D", "Reveals invisible enemies on a dex save, but splashing water reveals them with no save, the game gives free See Invisibility and a pile of scrolls — don't spend a slot."),
]

entry = {
    "key": "spells_level_2",
    "subject": "Spells — Level 2",
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
