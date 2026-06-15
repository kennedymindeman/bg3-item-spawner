import json, collections

PATH = "src/data/tierlists.json"

# (subclass display name, tier, note)
rows = [
    # Barbarian
    ("Berserker (Barbarian)", "A", "Frenzy's bonus-action throw (no frenzied-strain penalty) makes it a top-tier Tavern Brawler thrower, plus Mindless Rage immunity to fear/charm — but a monoclass Eldritch Knight throws more often, so it lands at A rather than S."),
    ("Wild Heart (Barbarian)", "A", "Five excellent rage aspects (Bear's resistance, Tiger's GWM-friendly AOE, Elk's party move-speed aura) make it the most reliable bruiser in the game — the author's benchmark for good game balance."),
    ("Wild Magic (Barbarian)", "C", "No negative surges (unlike the sorcerer) and it can restore allies' spell slots, but the random rage effects are minor and you must rage 20ft from allies, which hampers party positioning."),
    ("Path of the Giant (Barbarian)", "A", "Giant's Rage and Elemental Cleaver stack huge bonus damage onto every (any-weapon) throw, becoming the best thrown-weapon barbarian by the late game — pure damage and nothing else."),
    # Bard
    ("College of Lore (Bard)", "S", "Cutting Words (a castable-on-anyone Shield), the earliest Magical Secrets for the best spells in the game, and extra skill proficiencies — the default, no-downside caster bard."),
    ("College of Swords (Bard)", "S+", "Ranged Slashing Flourish gives four attacks per round on top of full bard casting and medium armour, with the easiest access to the broken Arcane Acuity / Band of the Mystic Scoundrel combo — out of scale with the game's balance."),
    ("College of Valour (Bard)", "A", "Combat Inspiration and extra attack are fine, but it does everything Swords Bard does, worse — outclassed within the class, though still a strong bard."),
    ("College of Glamour (Bard)", "A", "A misunderstood support bard — Mantle of Inspiration's no-save charm-on-hit disrupts enemy turns for free and Mantle of Majesty wins a fight per day with bonus-action Command; brings everything but damage."),
    # Cleric
    ("Knowledge Domain (Cleric)", "A", "Knowledge of the Ages grants full skill proficiency in an ability on demand, fixing cleric's poor skill access (party face, lockpicker, perception), plus a few control spells."),
    ("Life Domain (Cleric)", "A", "The best solo applier of buff-on-heal items via an AOE Channel Divinity and self+ally healing, but a one-dimensional healer that gains no new spells — a great dip, merely A as monoclass."),
    ("Light Domain (Cleric)", "S", "Warding Flare (a party-wide Shield-like reaction), the big Radiance of the Dawn AOE nuke (and best radiant-orb access), plus a full fire/damage spell list that patches cleric's lack of direct damage."),
    ("Nature Domain (Cleric)", "S", "Shillelagh makes the early game playable in melee, plus an elite added spell list (Spike Growth, Sleet Storm, Plant Growth) and Dampen Elements — superb control access."),
    ("Tempest Domain (Cleric)", "S", "The best added spell list (Call Lightning, Sleet/Ice Storm, Fog Cloud) plus Destructive Wrath to maximise lightning damage and reaction knockback that ping-pongs enemies across electrified water."),
    ("Trickery Domain (Cleric)", "A", "Really only adds the spell Fear; Invoke Duplicity is a famously underwhelming concentration action, so it's outclassed by domains with better AOE control — still a fine cleric."),
    ("War Domain (Cleric)", "A", "Heavy armour, martial weapons, and a reaction to add +10 to an ally's attack (turning a miss into a hit); the bonus-action attacks don't keep up on a monoclass caster, but a solid domain."),
    ("Death Domain (Cleric)", "S", "Reaper double-targets necrotic cantrips (Toll the Dead/Bone Chill) for strong early damage and Touch of Death is a Smite-sized burst — patches cleric's only weakness (early damage) while keeping every cleric strength."),
    # Druid
    ("Circle of the Land (Druid)", "A", "The default caster druid — Circle spells add the best low-level picks (Misty Step, Haste, Hypnotic Pattern) plus difficult-terrain and poison immunity; falls off slightly late but a great class."),
    ("Circle of the Moon (Druid)", "S", "Bonus-action wild shape (cast-then-shift in one turn) plus strong forms (Owlbear, Myrmidons) that abuse Tavern Brawler for big sustained melee damage on top of full druid casting."),
    ("Circle of Spores (Druid)", "A", "Symbiotic Entity adds temp HP and +1d6 to every attack plus a proactive reaction, Bone Chill smooths the cantrip gap, and free Animate Dead enables a summon army — but it's MAD with no extra attack."),
    ("Circle of the Stars (Druid)", "S", "Star forms give spammable free damage (Archer/Dragon) or healing (Chalice) plus Dragon-form reliable concentration, free Guiding Bolts, and Cosmic Omen (a mini Cutting Words) — 'Druid but more', obsoleting Land Druid."),
    # Fighter
    ("Battle Master (Fighter)", "A", "Maneuvers add control while dealing full damage (Precision/Trip/Pushing), but burn through only five superiority dice fast — the author's benchmark for good balance, and three attacks make it great regardless."),
    ("Champion (Fighter)", "B", "Improved Critical works out to under +1 damage per attack — far less than Battle Master's maneuvers and dice, with no other meaningful options, so it's outclassed within the class."),
    ("Eldritch Knight (Fighter)", "S", "Best played as a tanky Tavern Brawler thrower with Shield/Misty Step utility — the most forgiving character and the easiest way to win Honour Mode, near-unmissable and hard to kill."),
    ("Arcane Archer (Fighter)", "A", "Arcane Shots add can't-miss attacks (Seeking/Piercing) and removal-from-combat (Banishing Arrow vs the often-weak Charisma save) on top of a normal strong fighter — lower damage, higher control than Battle Master."),
    # Monk
    ("Way of the Four Elements (Monk)", "B", "Mostly spends key points on worse copies of other classes' spells; the unique ranged punches and ice block add a little dimension, but it gives little the base monk doesn't already do."),
    ("Way of the Open Hand (Monk)", "S", "Free crowd control on Flurry of Blows (effective extra stuns), +1d4+Wis (radiant for orb-stacking) on every attack, and Wholeness of Body key recovery — the best Tavern Brawler abuser and highest sustained monk damage."),
    ("Way of Shadow (Monk)", "B", "Thematic and fun, but Shadow Step's bonus-action teleport is something monks already do by jumping, and its tricks (Darkness/Silence) are cheaper from other classes — little unique value monoclass."),
    ("Drunken Master (Monk)", "C", "A playtest subclass whose key abilities are situational or literally blank-text and self-defeating (you spend key points for marginal stacks that vanish the moment you act); outclassed by every other monk and badly in need of a rework."),
    # Paladin
    ("Oath of the Ancients (Paladin)", "S", "Healing Radiance double-applies buff-on-heal items, and its aura grants spell-damage resistance — combined with Paladin saves, that's party-wide quarter damage from spells, letting healing actually outpace incoming damage; great spells (Misty Step, Plant Growth) too."),
    ("Oath of Devotion (Paladin)", "A", "Sacred Weapon adds Charisma to attack rolls, but Vengeance's Vow of Enmity does the accuracy job better and the rest of the kit is weak — outclassed, though still a fine smiting paladin."),
    ("Oath of Vengeance (Paladin)", "S", "The best paladin spell list (Misty Step, Haste, Hold Person) plus Vow of Enmity advantage (currently bugged to apply to all your attacks) and Inquisitor's Might — excels at dropping priority targets fast."),
    ("Oathbreaker (Paladin)", "A", "Saves the oath-restoration tax and adds an AOE fear and Animate Dead, but its signature Aura of Hate doesn't work on any summonable undead, so it's just a worse Vengeance — outclassed."),
    ("Oath of the Crown (Paladin)", "S", "Righteous Clarity buffs the whole party's accuracy, Champion Challenge controls aggro, and Charisma-based Spirit Guardians at level 9 makes it the best radiant-orb melee paladin — damage plus cleric-like support."),
    # Ranger
    ("Beast Master (Ranger)", "A", "A continuously-scaling companion (the Raven's free AOE Darkness/blind is unmatched late utility) adds extra actions and Hunter's Mark damage on top of a Sharpshooter archer; the beast's fragility keeps it at A."),
    ("Gloomstalker (Ranger)", "A", "Dread Ambusher's free opening attack (~25 burst with Sharpshooter), out-of-combat invisibility for perfect positioning, Wisdom-save proficiency, and Misty Step — an incredibly safe, strong archer."),
    ("Hunter (Ranger)", "B", "Heavily back-loaded — Colossus Slayer is weak and the level-7 picks minor, but the level-11 Volley capstone is S-tier; rated B across a full 1-12 playthrough (S if you respec into it at 11)."),
    ("Swarm Keeper (Ranger)", "B", "A strong level-3 spike (2d6 plus a per-turn blind, later blind+slow at 11) but roughly eight dead levels in between — a happy-to-have B-tier with a soft mid-game."),
    # Rogue
    ("Arcane Trickster (Rogue)", "B", "Wizard utility spells (Shield, Misty Step, disguise/charm for a party face) plus Magical Ambush disadvantage to reliably land Hold Person; nearly unkillable but adds little damage — the best monoclass rogue."),
    ("Assassin (Rogue)", "C", "Huge opening burst (restored actions + auto-crits on the surprised) that falls off hard after level 3 and forces you to always initiate with the rogue, often costing more party damage than it gains."),
    ("Thief (Rogue)", "C", "The extra bonus action gives superb positioning and reliable sneak-attack landing, but a monoclass thief still lacks Extra Attack, so its damage lags every dedicated damage dealer — great in multiclass, weak solo."),
    ("Swashbuckler (Rogue)", "B", "Sneak attacks without allies, a scaling initiative bonus, and bonus-action blind/disarm (Flick of the Wrist is a near-second attack) make a safe hit-and-run rogue — but still lower damage than other damage subclasses."),
    # Sorcerer
    ("Draconic (Sorcerer)", "S", "Elemental Affinity adds Charisma to every damage spell of your type (broken with leveled Scorching Ray or wet cold/lightning), plus extra HP and free Mage Armour — a powerful sorcerer with a great damage feature."),
    ("Storm (Sorcerer)", "S", "Tempestuous Magic gives bonus-action flight with no opportunity attacks from level one (huge early-game safety), plus Heart of the Storm AOE rider damage and a flexible added spell list."),
    ("Wild Magic (Sorcerer)", "C", "Tides of Chaos and Bend Luck are powerful, but the random surges (including a hostile cambion) force restrictive positioning and can snowball a bad fight — rated C for the constraint, though one of the most fun playthroughs."),
    ("Shadow Magic (Sorcerer)", "S", "A sorcerer that gets Darkness plus see-in-magical-darkness without a warlock dip (one of the game's best strategies), plus the Hound of Ill Omen summon and a later teleport — high-end S."),
    # Warlock
    ("The Archfey (Warlock)", "A", "Underrated — Fey Presence is an AOE fear/charm disable from level one, Misty Escape gives an invisibility-plus-teleport escape, and Plant Growth pairs with Hunger of Hadar."),
    ("The Fiend (Warlock)", "A", "The best added spell list (auto-scaling Command, resource-free Wall of Fire), kill-based temp HP for sustain, Dark One's Own Luck (+d10 to a check), and changeable damage resistance — very hard to kill."),
    ("The Great Old One (Warlock)", "A", "Mortal Reminder spreads free fear on your frequent Eldritch Blast crits, plus a spell list that lets a warlock cheaply cast situational spells (Slow, Telekinesis) and Entropic Ward — the generically strongest warlock."),
    ("Hexblade (Warlock)", "S+", "Ties weapon and spell attacks to Charisma with medium armour/shields at level one, Hex's Curse adds proficiency to every damage instance (huge with Eldritch Blast), and Cone of Cold/Banishing Smite later remove its only weakness — too much in one character."),
    # Wizard
    ("Abjuration (Wizard)", "S+", "Arcane Ward is flat damage reduction (up to 2x level) refreshed by cheap Glyph of Warding and stacked with resistances/healing — effectively thousands of hit points; literally unkillable and game-breaking."),
    ("Conjuration (Wizard)", "A", "Almost nothing until Focus Conjuration at level 10 (concentration unbreakable by damage), which Abjuration does better — outclassed, but Wizard's base chassis keeps it strong."),
    ("Divination (Wizard)", "S", "Portent dice let you replace any attack or save you see with a pre-rolled value (force enemy fails, guarantee crits), regaining more via prophecies — removing randomness at key moments is nonsensically strong."),
    ("Enchantment (Wizard)", "A", "Little until level 10, but Split Enchantment double-casts single-target enchantments (double Hold Person / Otto's Irresistible Dance) — the best wizard at late-game disables."),
    ("Evocation (Wizard)", "A", "Sculpt Spells makes allies immune to your AOE (drop Fireball in a melee, stand in your own Wall of Fire), and late Int-to-damage makes Magic Missile/Acid Splash reliable finishers — the easiest, most forgiving wizard."),
    ("Illusion (Wizard)", "A", "Improved Minor Illusion barely matters and Illusory Self (turn a hit into a miss at level 10) is duplicated better by Divination's portent dice — outclassed, though still a strong wizard chassis."),
    ("Necromancy (Wizard)", "A", "The summoner wizard — free Animate Dead plus an extra corpse per cast and big HP/damage buffs to your minions; little else, but summon armies are very strong."),
    ("Transmutation (Wizard)", "A", "Usually a camp follower, but as an active member the Transmuter's Stone grants Constitution-save (concentration) proficiency so it rarely loses spells, plus extra potions — enough for an A on the strong wizard base."),
    ("Bladesinging (Wizard)", "A", "Bladesong adds AC, Con saves, and move speed for survivability plus a bonus-action burst of damage/healing (Bladesong Climax); the melee is secondary, but a wizard needs little from its subclass to be A."),
]

entry = {
    "key": "subclasses",
    "subject": "Subclasses (single-class)",
    "context": "Baldur's Gate 3 honour mode build guide — monoclass, level 12 (includes the Patch 8 subclasses)",
    "is_gameplay_only": True,
    "tier_definitions": {
        "S+": "Out of scale — breaks the game's intended balance",
        "S": "Both extremely powerful and extremely versatile",
        "A": "Either extremely powerful or extremely versatile, not both",
        "B": "A bit less powerful/versatile than A, but still great",
        "C": "Restricts your strategy via a drawback you must play around",
    },
    "ratings": {name: tier for name, tier, _ in rows},
    "notes": {name: note for name, _, note in rows},
}

data = json.load(open(PATH))
assert not any(x["key"] == entry["key"] for x in data), f"{entry['key']} already present"
assert len(entry["ratings"]) == len(rows), "duplicate subclass name!"
valid = {"S+", "S", "A", "B", "C", "D", "F"}
assert all(v in valid for v in entry["ratings"].values())
data.append(entry)
with open(PATH, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print(entry["key"], "added:", len(entry["ratings"]), "subclasses; total lists:", len(data))
print("tier spread:", dict(collections.Counter(entry["ratings"].values())))
