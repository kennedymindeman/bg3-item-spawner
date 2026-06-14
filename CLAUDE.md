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

**Status:** 1 of 27 lists done.
- ✅ `arrows` — verified in `review/arrows_verified.json` (all 21 tiers confirmed
  correct; reasoning written). **Not yet merged into `tierlists.json` or rendered.**
- ⬜ The other 26 lists — not started.

**Recipe per list** (do NOT trust `extract_ratings.py`'s tiers — read the source):
1. Look up the list's source transcript number(s) in the `SOURCES` map in
   `extract_ratings.py` (e.g. `potions` → `028`, `gloves` → `043,044,045`).
2. Read those transcript(s) and, for each rated item, confirm the spoken tier and
   write a one-sentence `why`.
3. Save as `review/<key>_verified.json`, same shape as `review/arrows_verified.json`.
4. This can be fanned out across sub-agents (one list per agent).

**Then wire it into the app (one-time, do after a few lists exist):**
1. Schema: change each `ratings` value in `tierlists.json` from `"S+"` to
   `{"t":"S+","why":"…"}`. Merge the verified `why` text in. Keep it
   backward-compatible OR update all 27 lists at once.
2. Render: update the tier-list / item-card rendering in `src/index.html` to show
   `why` under the tier badge when present, blank when absent.
3. `uv run build.py` and confirm e.g. the Arrow of Darkness card now shows text.
