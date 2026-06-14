# BG3 Item Spawner / Script Extender Console

A single-file HTML reference for Baldur's Gate 3: item spawner, console commands,
and tier lists. Tier ratings come from Cephalopocalypse's Honour Mode YouTube guides.

## Layout

- `bg3_console.html` — **GENERATED. Do not hand-edit.** Built from `src/`.
- `src/index.html` — the app (CSS + markup + logic) with `@DATA` injection markers.
- `src/data/items.json` — 3,310 spawnable items (`{n,u,c,d}`), one per line.
- `src/data/tierlists.json` — 27 tier lists (`{key, subject, tier_definitions, ratings}`).
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

## ⬜ PENDING WORK — per-item reasoning ("why") for tier lists

**Goal:** every tier-list item card should show *why* it got its tier (the app
currently stores only `name → tier`, so descriptions render blank — e.g. the
Arrow of Darkness card). The reasoning lives in the `transcripts/`.

**How it surfaces in the app:** the render already supports it — `renderTierlist`
in `src/index.html` shows `tl.notes[name]` as a `.detail-note` in each item's
expanded card. **No JS or schema change is needed.** Just add a `"notes": {item:
why}` object to a tier list in `tierlists.json` (see the `arrows` entry as the
template) and rebuild.

**Status:** 1 of 27 lists done.
- ✅ `arrows` — verified, and the 21 `why` strings are merged into the `arrows`
  entry's `notes` in `tierlists.json` and rendering live (e.g. Arrow of Darkness).
  Source of the prose: `review/arrows_verified.json`.
- ⬜ The other 26 lists — not started.

**Recipe per list** (do NOT trust `extract_ratings.py`'s tiers — read the source):
1. Look up the list's source transcript number(s) in the `SOURCES` map in
   `extract_ratings.py` (e.g. `potions` → `028`, `gloves` → `043,044,045`).
2. Read those transcript(s) and, for each rated item, confirm the spoken tier and
   write a one-sentence `why`.
3. Save as `review/<key>_verified.json`, same shape as `review/arrows_verified.json`.
4. Merge the `why` strings into that list's `notes` object in `tierlists.json`
   (mirror the small Python snippet used for arrows), then `uv run build.py`.
5. Steps 1-3 can be fanned out across sub-agents (one list per agent).
