# BG3 Item Spawner / Script Extender Console

A single-file HTML reference for Baldur's Gate 3: item spawner, console commands,
and tier lists. Tier ratings come from Cephalopocalypse's Honour Mode YouTube guides.

## Layout

- `bg3_console.html` — **GENERATED. Do not hand-edit.** Built from `src/`.
- `src/index.html` — the app (CSS + markup + logic) with `@DATA` injection markers.
- `src/data/items.json` — 3,310 spawnable items (`{n,u,c,d}`) as a JSON array.
  It's a curated subset of bg3.wiki, so many real items (and all generic `+N`
  variants) aren't in it; `u` is the RootTemplate UUID used by `TemplateAddTo`.
- `src/data/tierlists.json` — 27 tier lists (`{key, subject, tier_definitions,
  ratings}`, plus optional `notes`, `acts`, `uuids`, `wnames`). `uuids[name]`
  overrides name-matching to give an explicit spawn UUID; `wnames[name]` is the
  bg3.wiki page title for the wiki link.
- `fetch_uuids.py` / `fetch_uuids2.py` — scrape bg3.wiki for UUIDs of tier-list
  items not in `items.json` (writes `review/wiki_uuids.json`).
- `build.py` — inlines the JSON back into `bg3_console.html`. Run after editing `src/`.
- `get_transcripts.py` — downloads a YouTube playlist's transcripts (yt-dlp).
- `transcripts/` — 93 plain-text transcripts of the source guides.
- `extract_ratings.py` — heuristic transcript→rating diff. **Triage only, not ground
  truth** (auto-captions are too noisy to attribute reliably — see review notes).
- `review/` — extractor output + hand-verified per-list data.

## Build / run

```
uv run build.py        # regenerate bg3_console.html from src/
```
Then open `bg3_console.html` directly (no server needed).

---

## ⬜ PENDING WORK — backlog (raised by user; not yet started)

1. **Missing spawn commands.** ✅ Mostly done — 149 of 163 recovered, 0 fabricated UUIDs.
   - ✅ **58 recovered** by a loose-match fallback added to `resolveEntry` in
     `src/index.html` (`looseKey`/`LOOSE_INDEX`): handles `+N` prefix↔suffix and a
     dropped `Armour` noun, collision-guarded so it never resolves ambiguously.
   - ✅ **91 scraped from bg3.wiki** (`fetch_uuids.py` + `fetch_uuids2.py`, output
     in `review/wiki_uuids.json`) and merged as `uuids`/`wnames` into the relevant
     lists in `tierlists.json`. The wiki infobox `| uuid =` (first one) matches the
     `TemplateAddTo` UUID — validated against items.json. Wrong search matches were
     hand-rejected (e.g. Voss the NPC, Worg Fang the ingredient, Sussur≠Redcap).
   - ⬜ **14 still unresolved** (see `review/wiki_uuids.json` statuses):
     5 generic "non-magical X"/family placeholders (Ring, Shield, Hat, Amulet
     (non-magical), Resistance elixir — not single items); 4 whose wiki page has an
     EMPTY uuid field (Worgfang, Redcap Sickle, Box of Fireworks, Box of Oddfire
     Fireworks); plus Spacehunt Boots, Coldsnap, Salty Scimitar (RRR),
     Mattis's Rings, Voss's Silver Sword (Act 3). Need another source or a decision.
2. **Filterable tags** (e.g. crit immunity, full Dex bonus, reverberation,
   radiating orb, initiative). Needs a schema + UI filter; much tag content is
   already in the `review/*.json` `why` strings.
3. **Per-item act ("first appears in").** Render already supports `tl.acts[name]`
   → "Found in Act X" (amulets/heavy_armor populate it). User asked to use the
   wiki, but the **source transcripts already state act-of-acquisition** (guides
   rate by act) — derive from transcripts, spot-verify on bg3.wiki.

**Tier lists NOT on the site** (all are *non-item* character-building lists):
Feats (transcript 002), Spells by level (004–013), Classes (015),
Subclasses (016–018), Multiclasses (019–023), Illithid Powers (034–035).
The site covers every *item/equipment/consumable* list plus skills & cantrips
(reference-only). Decide whether non-item lists belong in an item spawner.

## ✅ DONE — per-item reasoning ("why") for tier lists

**Goal:** every tier-list item card should show *why* it got its tier (the app
currently stores only `name → tier`, so descriptions render blank — e.g. the
Arrow of Darkness card). The reasoning lives in the `transcripts/`.

**How it surfaces in the app:** the render already supports it — `renderTierlist`
in `src/index.html` shows `tl.notes[name]` as a `.detail-note` in each item's
expanded card. **No JS or schema change is needed.** Just add a `"notes": {item:
why}` object to a tier list in `tierlists.json` (see the `arrows` entry as the
template) and rebuild.

**Status: COMPLETE — all 27 lists have `notes` for every rated item (verified: 0
missing).** Each list's prose is saved in `review/<key>_verified.json`. Merge helper:
`uv run merge_notes.py <key>` pulls `why` strings from `review/<key>_verified.json`
into `tierlists.json` (with tier-match sanity checks). Five stored tiers were
corrected to match the spoken guides: skills Persuasion S→A & Insight B→C,
cantrips Mage Hand S→A, versatile_weapons Voss's Silver Sword A→S & (Act 3) S→A.

- ✅ `arrows` — verified; `notes` merged & live. Source: `review/arrows_verified.json`.
- ✅ `elixirs` — transcript 027; merged & live. `review/elixirs_verified.json`.
- ✅ `potions` — transcript 028; merged & live. `review/potions_verified.json`.
- ✅ `grenades` — transcript 029; merged & live. `review/grenades_verified.json`.
- ✅ `poisons_oils` — transcript 031; merged & live. `review/poisons_oils_verified.json`.
- ✅ `barrels` — transcript 032; merged & live. `review/barrels_verified.json`.
- ✅ `skills` — transcript 001; merged & live. `review/skills_verified.json`.
  **Corrected 2 stored tiers** to match the spoken guide: Persuasion S→A, Insight B→C.
- ✅ `light_armor` — transcript 037; merged & live. `review/light_armor_verified.json`.
- ✅ `cloaks` — transcript 042; merged & live. `review/cloaks_verified.json`.
- ✅ `shields` — transcript 041; merged & live. `review/shields_verified.json`.
- ✅ `medium_armor` — transcript 038; merged & live. `review/medium_armor_verified.json`.
- ✅ `cloth_armor` — transcript 036; merged & live. `review/cloth_armor_verified.json`.
- ✅ `boots` — transcript 046; merged & live. `review/boots_verified.json`.
- ✅ `staves` — transcript 062; merged & live. `review/staves_verified.json`.
- ✅ `ranged_weapons` — transcript 059; merged & live. `review/ranged_weapons_verified.json`.
- ✅ `polearms` — transcript 064; merged & live. `review/polearms_verified.json`.
- ✅ `two_handed_weapons` — transcript 065; merged & live. `review/two_handed_weapons_verified.json`.
- ✅ `one_handed_weapons` — transcript 066; merged & live. `review/one_handed_weapons_verified.json`.
- ✅ `simple_weapons` — transcript 063; merged & live. `review/simple_weapons_verified.json`.
- ✅ `cantrips` — transcript 003; merged & live. `review/cantrips_verified.json`.
  **Corrected 1 stored tier**: Mage Hand S→A (guide says "the strong tier").
- ✅ `finesse_weapons` — transcripts 060+061; merged & live. `review/finesse_weapons_verified.json`.
- ✅ `versatile_weapons` — transcripts 067+068; merged & live. `review/versatile_weapons_verified.json`.
  **Corrected 2 stored tiers** (swapped): Voss's Silver Sword A→S, Voss's Silver Sword (Act 3) S→A.
- ✅ `gloves` — transcripts 043+044+045; merged & live. `review/gloves_verified.json`.
- ✅ `helmets` — transcripts 047+048+049; merged & live. `review/helmets_verified.json`.
- ✅ `rings` — transcripts 053+054+055; merged & live. `review/rings_verified.json`.
- (Pre-existing: `amulets`, `heavy_armor` shipped notes in the original split commit.)

**Recipe per list** (do NOT trust `extract_ratings.py`'s tiers — read the source):
1. Look up the list's source transcript number(s) in the `SOURCES` map in
   `extract_ratings.py` (e.g. `potions` → `028`, `gloves` → `043,044,045`).
2. Read those transcript(s) and, for each rated item, confirm the spoken tier and
   write a one-sentence `why`.
3. Save as `review/<key>_verified.json`, same shape as `review/arrows_verified.json`.
4. Merge the `why` strings into that list's `notes` object in `tierlists.json`
   (mirror the small Python snippet used for arrows), then `uv run build.py`.
5. Steps 1-3 can be fanned out across sub-agents (one list per agent).
