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
    ("Counterspell", "S", "Reaction that deletes an enemy spell as it's cast — one of the five best spells in the game; trade your reaction for a boss's whole turn and a high-level slot. Use a slot of equal level to auto-counter (low slots become a die roll); no scrolls exist, so learn it. Every party wants 1-2 casters."),
    ("Glyph of Warding", "S", "Cast it directly ON an enemy and it detonates like Fireball, but with six damage types (double vs wet) OR a no-concentration AOE sleep on a dex save — non-concentration, spammable, the Swiss-army damage/control spell; also feeds Abjuration wards and is the bard's best direct damage."),
    ("Haste", "S", "Concentration buff granting +2 AC, advantage on dex saves, +30 move, and an EXTRA action each turn (one extra attack, or a full second spell on tactician) — the most direct way to win the action-economy game; twin it on a sorcerer for two. Mind the lethargic stun when it drops."),
    ("Hunger of Hadar", "S", "A huge no-save blind + difficult-terrain + cold-damage zone enemies can't jump out of (blinded) — drop it on top of another control spell (Plant Growth) and shove escapees back in to lock down an entire encounter; with Counterspell, the top Magical Secrets pick."),
    ("Spirit Guardians", "S", "A radiant/necrotic damage aura (3d8, upcasts to 6d8) that hits every nearby enemy each turn for just your MOVEMENT — near-free damage that pairs perfectly with Command/Glyph and stacks radiating orbs instantly; the gold standard cleric spell, now also on Crown paladins."),
    ("Animate Dead", "A", "Flexible all-day summons — skeleton archers for steady party damage, zombies to convert whole weak encounters, ghouls to paralyse; a 4th-level cast for three skeletons is the default, and necromancer wizards get an extra each. Summons are always strong."),
    ("Call Lightning", "A", "3d10 lightning (dex save half) in a decent AOE that you re-cast each turn for one slot — very efficient over long fights, doubles vs wet, and a Tempest cleric can maximise it to guaranteed 30; cast it again with hasted actions for more."),
    ("Fear", "A", "A 30ft-cone wisdom-save disable — failed enemies drop their weapon and flee for two turns, completely shutting down melee; the strongest of the AOE control spells when its cone can reach, one of the fear/hypnotic-pattern/sleet-storm trio you pick between per fight."),
    ("Hypnotic Pattern", "A", "A massive (60ft across) wisdom-save incapacitate for two turns with no repeat save — wins any fight where you catch the whole group (wake them one at a time by killing them); the go-to when you can hit the entire encounter."),
    ("Lightning Bolt", "A", "Fireball's damage (8d6) as a long 100ft line, but lightning (doubles vs wet, far fewer resistances) — the better go-to burst spell, especially when enemies advance toward you in a line; synergises with reverberation."),
    ("Mass Healing Word", "A", "A bonus-action AOE heal — mostly the best way to re-apply buff-on-heal items (Hellrider's Pride / Whispering Promise) to the whole party, plus reviving multiple downed allies; mandatory for any dedicated-healer party."),
    ("Sleet Storm", "A", "A giant (60ft) ice surface that forces concentration AND prone saves — wrecks enemy casters, and the ice prone-stuns half the enemies each turn for 10 turns; less reliable than Hypnotic Pattern but works even on part of an encounter and at long range."),
    ("Bestow Curse", "B", "A melee debuff that, crucially, doesn't start combat — set up the +1d8 damage rider (great with Scorching Ray) or the skip-a-turn 'dread' lockdown (bypasses many incapacitation immunities) on a neutral enemy for free before the fight; never cast it mid-combat."),
    ("Blinding Smite", "B", "A level-3 smite doing 3d8 radiant (no concentration) that can also blind on a con save — give up 1d8 vs Divine Smite for a debuff, or stack both on one attack for big burst plus a blind; a nice back-pocket option."),
    ("Elemental Weapon", "B", "All-day +1/+1d4 (up to +2/+2d4) elemental damage on a weapon — great specifically on a Hexblade (auto-upcasts) or cast on an archer ally for snow-burst-ring / reverberation / wet synergies; paladins rarely want it over a smite."),
    ("Fireball", "B", "8d6 fire AOE (dex save half) — still a big burst, but BG3 shrank its radius to 13ft, fire is widely resisted, and the dex save is forgiving, so it's a 'group them up and nuke weak enemies' tool rather than the tabletop encounter-ender."),
    ("Plant Growth", "B", "A non-concentration zone that cuts movement to a quarter — completely shuts down melee enemies that can't jump, and layers perfectly under Hunger of Hadar; incredible in the right fight, but flammable and useless vs ranged enemies."),
    ("Slow", "B", "Targets six creatures (wisdom save) for half move, -2 AC/dex saves, one action and no reactions/extra attacks — your reliable second-choice control: works when allies are clustered with enemies and on many incapacitation-immune bosses."),
    ("Blink", "C", "A 50% chance each turn to phase out and become untargetable — too unreliable for party play (it just redirects aggro to allies anyway, and Mirror Image does it cheaper), but genuinely strong defence in SOLO runs."),
    ("Crusader's Mantle", "C", "+1d4 radiant on every ally's weapon attack — usually worse than a smite, but excellent specifically for summon-heavy parties (multiply it across skeleton archers); a war cleric gets it early, and a cloak casts it."),
    ("Daylight", "C", "A big light source — mostly redundant with the free Light cantrip, but useful to light a whole arena for an archer and, crucially, to hurt the Act 3 vampires who are vulnerable to it."),
    ("Gaseous Form", "C", "Turns an ally into a damage-resistant, flying, tiny mist — a strong EXPLORATION tool (pass through grates/over lava) but useless in combat; the potion version is usually the better way to get it."),
    ("Protection from Energy", "C", "All-day concentration resistance to one element — powerful in single-element fights, but expensive (concentration + slot, single target) and easily duplicated by resistance elixirs and gear, except for hard-to-resist types like thunder."),
    ("Remove Curse", "C", "Removes curses — the textbook situational spell: swap it in for the few story-event curses that survive a long rest, otherwise never cast it. The hard part is remembering it exists."),
    ("Speak with Dead", "C", "A ritual (free) to chat with corpses — fun and occasionally helpful for quests, but the mechanical benefits are minor and you'll usually have an item/story way to do it."),
    ("Stinking Cloud", "C", "A big AOE nauseate (no-act) that's let down by the worst save (Constitution) AND poison immunity — and roughly half of BG3's threatening enemies (undead, constructs, fiends) are immune; great in the few fights it works in, dead weight elsewhere."),
    ("Warden of Vitality", "C", "A 10-turn bonus-action 2d6 heal — a waste of a slot for a paladin, but the centrepiece of a dedicated lore-bard healer build (extra bonus actions via Helmet of Grit / Thief plus healing gear make it pour out healing)."),
    ("Beacon of Hope", "D", "Maximises healing (plus minor wisdom/death-save advantage) — but healing is already a weak strategy, and the boost is tiny; it does nothing on its own and costs a slot plus concentration."),
    ("Conjure Barrage", "D", "A weapon-based cone (2d8, dex save) that takes your whole action, doesn't work with Extra Attack, and applies no on-hit effects — just shoot enemies instead."),
    ("Feign Death", "D", "Incapacitates an ally with damage resistance — pointless on a party member (you don't want them out of the fight), and the merchant/NPC tricks were patched out (allies only now)."),
    ("Fly", "D", "Concentration flight that's really just hopping (BG3 has no true flight) — duplicated by Enhanced Leap jumping and Misty Step, so the slot + concentration cost rarely justifies it; use a potion if you ever need it."),
    ("Lightning Arrow", "D", "A wisdom-attack ranger nuke that's both inaccurate (low ranger save DC/attack) and low damage — just shoot your bow; casting it does less, less reliably, for a slot."),
    ("Revivify", "D", "Brings a dead ally back at 1 HP — a fine effect, but every character starts with a scroll and vendors/loot drown you in more (and Withers revives out of combat), so you'll never need to spend a slot."),
    ("Vampiric Touch", "D", "~10 melee necrotic with half as healing, re-castable each turn — the numbers are simply terrible for a level-3 slot; do damage and drink a potion instead."),
]

entry = {
    "key": "spells_level_3",
    "subject": "Spells — Level 3",
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
