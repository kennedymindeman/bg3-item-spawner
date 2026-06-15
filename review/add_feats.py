import json, collections

PATH = "src/data/tierlists.json"

feats = {
    "key": "feats",
    "subject": "Feats",
    "context": "Baldur's Gate 3 build guide",
    "is_gameplay_only": True,
    "tier_definitions": {
        "S+": "Breaks D&D's balance range — part of the most broken builds",
        "S": "Extremely powerful mainstays taken very frequently",
        "A": "Strong, narrower alternatives to S-tier for specific builds",
        "B": "Viable niche strategies; good leftover 3rd/4th feat picks",
        "C": "Very niche; usually weaker than the alternatives",
        "D": "Very weak — little real effect or easily duplicated; avoid",
    },
    "ratings": {
        "Alert": "S+",
        "Tavern Brawler": "S+",
        "Ability Score Improvement": "S",
        "Athlete": "S",
        "Great Weapon Master": "S",
        "Savage Attacker": "S",
        "Sharpshooter": "S",
        "Actor": "A",
        "Dual Wielder": "A",
        "Heavy Armor Master": "A",
        "Mobile": "A",
        "Moderately Armored": "A",
        "Polearm Master": "A",
        "Resilient": "A",
        "Sentinel": "A",
        "War Caster": "A",
        "Defensive Duelist": "B",
        "Elemental Adept": "B",
        "Lucky": "B",
        "Mage Slayer": "B",
        "Magic Initiate": "B",
        "Spell Sniper": "B",
        "Durable": "C",
        "Heavily Armored": "C",
        "Martial Adept": "C",
        "Tough": "C",
        "Charger": "D",
        "Crossbow Expert": "D",
        "Dungeon Delver": "D",
        "Lightly Armored": "D",
        "Medium Armor Master": "D",
        "Performer": "D",
        "Ritual Caster": "D",
        "Shield Master": "D",
        "Skilled": "D",
        "Weapon Master": "D",
    },
    "notes": {
        "Alert": "Copied from 5e unchanged, but BG3 rolls initiative on a d4 instead of a d20, so its +5 is larger than the entire random range — a near-guaranteed win of initiative, which lets you kill enemies before they ever act. Aim to get it as your first or second feat on almost any Honour Mode character.",
        "Tavern Brawler": "A BG3 house rule that adds DOUBLE your Strength modifier to both hit and damage on unarmed and thrown attacks, breaking 5e's bounded-accuracy rule — worth roughly five ASIs of hit chance and free for monks/throwers (especially with Strength elixirs).",
        "Ability Score Improvement": "+2 to your main stat is a +1 to nearly every roll across the whole game, and small linear bonuses get proportionally stronger the better you already are — almost every optimal build takes two of these to hit 20.",
        "Athlete": "A half-ASI (even out a 17) that also grants +50% jump distance, giving a melee character cheap bonus-action mobility to actually reach combat and set up high ground — often just a better ASI.",
        "Great Weapon Master": "Toggle -5 to hit for +10 damage per two-handed attack, plus a bonus-action attack on a kill or crit; massively raises average AND maximum damage so you drop enemies before they act. Leave it on in most situations.",
        "Savage Attacker": "Roll melee damage dice twice and keep the higher — a ~25-30% average damage boost that scales with how many dice you roll, so it's S-tier on smite/sneak-attack/shadowblade builds but much weaker on flat-bonus hitters.",
        "Sharpshooter": "The ranged Great Weapon Master (-5/+10) plus ignoring the high-ground penalty; even better than GWM because ranged attacks land more often and the penalty is easy to offset with Archery style, high ground, and stealth advantage.",
        "Actor": "+1 Charisma (uncapped, unlike most feats) plus expertise in Deception and Performance without needing proficiency — nearly free on a Charisma build that started on an odd score.",
        "Dual Wielder": "Weak for actual dual-wielding, but lets casters wield two staves (or Phalar Aluve + a staff) at once for stacked passive spellcasting buffs — a core piece of some of the most broken magic-missile/fire-sorcerer builds.",
        "Heavy Armor Master": "+1 Strength and -3 to all incoming bludgeoning/piercing/slashing damage in heavy armor; stacks with armor damage reduction and resistances to slash effective damage dramatically. Often a free ASI swap on heavy-armor characters.",
        "Mobile": "+10 movement that stacks with everything, ignore difficult terrain while dashing, and no opportunity attacks after a melee hit — a strong fourth feat that opens late-game tactical options, especially on monoclass rogues.",
        "Moderately Armored": "Grants medium armor AND shield proficiency while bumping Strength or Dexterity, letting a Dex character (e.g. monoclass rogue) wear BG3's excellent medium armors and a shield at near-zero cost.",
        "Polearm Master": "A bonus-action butt-end attack and an opportunity attack when enemies enter your extended reach; the basis of the Polearm Master + Sentinel lockdown combo and great on its own because more attacks is always good.",
        "Resilient": "+1 to any attribute plus proficiency in its save; mainly taken for Constitution-save proficiency (better concentration) or to restore a save lost to multiclassing — nearly free when it evens out an odd score.",
        "Sentinel": "Opportunity attacks stop the target's movement, you get advantage on them, and you can punish enemies attacking your allies — pairs with Polearm Master to lock melee enemies out of range indefinitely.",
        "War Caster": "Advantage on Constitution saves to hold concentration (plus cast spells as opportunity attacks); a strong safety net if your casters lose concentration often, though Resilient is usually better when you lack con-save proficiency.",
        "Defensive Duelist": "Spend a reaction to add your proficiency bonus to AC when hit in melee with a finesse weapon — like half of Shield for free each turn, solid on Dex melee characters such as swashbuckler rogues.",
        "Elemental Adept": "Your chosen damage type ignores resistance and can't roll 1s; realistically only worth it for fire (lots of fire-resistant enemies), and even then you can often just cast a different element instead.",
        "Lucky": "Three luck points per long rest for advantage or to force an enemy to reroll an attack; good defensively and consistency-boosting if you rest often, but expensive — more of a third/fourth feat.",
        "Mage Slayer": "Advantage on saves vs adjacent casters, a reaction attack when they cast, and disadvantage on their concentration; a 'win-more' lockdown tool that shines mainly in mixed melee/caster boss fights.",
        "Magic Initiate": "Two cantrips and a 1st-level spell; a bad feat saved almost entirely by Patch 8's Booming Blade, which adds so much damage that some melee builds take Magic Initiate just to learn it.",
        "Spell Sniper": "Learn an attack cantrip (usually Eldritch Blast, cast with YOUR stat) and reduce your crit threshold by 1 on all spells; solid on attack-spam casters like Great Old One warlocks and fire sorcerers.",
        "Durable": "+1 Constitution and full HP on a short rest; out-of-combat healing is already nearly free in BG3, so it's a minor, rarely-relevant pick that's only fine when it evens out an odd con score.",
        "Heavily Armored": "+1 Strength and heavy armor proficiency, but Strength characters usually already have it, BG3's medium armors are better, and a 1-level cleric/fighter dip grants it more efficiently.",
        "Martial Adept": "Two maneuvers and one superiority die — a terrible return for most, but okay specifically on a Battle Master who wants one extra (and larger) superiority die per short rest.",
        "Tough": "+2 HP per level (up to +24); not nothing on a squishy character, but a purely defensive feat is hard to justify over options that improve your game plan.",
        "Charger": "Action + bonus action to move 30ft and attack (+5 damage) or shove; most characters get this mobility for free by jumping/dashing, and the wide charge path constantly whiffs on terrain and allies.",
        "Crossbow Expert": "Negates melee disadvantage on crossbow attacks, but BG3 crossbows are weak and free weapon-set swapping lets archers just hit with melee weapons instead — the feat is duplicated by base mechanics.",
        "Dungeon Delver": "Advantage to spot traps and half damage from them — so minimal it did literally nothing for six patches and nobody noticed; the lowest-impact feat in the game.",
        "Lightly Armored": "+1 Strength or Dexterity and light armor proficiency with no other bonus; almost no character that lacks light armor proficiency wants to boost those stats, and robes outclass light armor anyway.",
        "Medium Armor Master": "Removes medium-armor stealth disadvantage and raises the Dex cap to +3, but BG3's best medium armors are already uncapped and this feat actually OVERWRITES that, lowering AC on the high-Dex characters who'd want it.",
        "Performer": "+1 Charisma and instrument proficiency that does essentially nothing mechanically; Actor is a strictly better way to get the Charisma point.",
        "Ritual Caster": "Two ritual spells (Longstrider, Speak with Dead, etc.) that you can get from items or a 1-level dip; far too little value for a whole feat.",
        "Shield Master": "+2 Dex saves with a shield and a Rogue-evasion-like reaction, but the half-damage half is bugged to do nothing on a fail, and Resilient gives a bigger Dex-save bonus anyway.",
        "Skilled": "Three skill proficiencies — a huge opportunity cost for little benefit, since you can get skills from background/race and most BG3 skills aren't very impactful. Take only for flavor.",
        "Weapon Master": "+1 Strength or Dexterity and four weapon proficiencies, but any character who wants a weapon type already has proficiency in it; almost never worth a feat even as a half-feat.",
    },
}

data = json.load(open(PATH))
assert not any(x["key"] == "feats" for x in data), "feats already present"
# every rated item must have a note
missing = [k for k in feats["ratings"] if k not in feats["notes"]]
assert not missing, f"missing notes: {missing}"
# tiers valid
valid = {"S+", "S", "A", "B", "C", "D", "F"}
assert all(v in valid for v in feats["ratings"].values())
data.append(feats)
with open(PATH, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print("feats added:", len(feats["ratings"]), "items; total lists:", len(data))
print("tier spread:", dict(collections.Counter(feats["ratings"].values())))
