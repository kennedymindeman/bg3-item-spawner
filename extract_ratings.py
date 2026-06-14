#!/usr/bin/env python3
"""Heuristic transcript -> tier-rating extractor / reviewer.

    uv run extract_ratings.py

For each tier list in src/data/tierlists.json, this finds the source
Cephalopocalypse transcript(s), searches them for each rated item name,
and looks for a spoken tier declaration ("... that's S tier", "... s plus")
near the mention. It then diffs the detected tier against the tier we
currently store, and writes:

    review/tier_review.md     human-readable report (grouped by subject)
    review/tier_review.json   same data, machine-readable

IMPORTANT: the transcripts are auto-generated captions (lowercase, no
punctuation, frequent mishears), so this is a TRIAGE tool, not ground
truth. Every CONFLICT / detected value should be eyeballed against the
snippet before changing tierlists.json. Precision is favoured over
recall: we only trust the explicit "<letter> tier" / "s plus" phrasing.
"""

import json
import re
from pathlib import Path
from collections import Counter

TRANSCRIPTS = Path("transcripts")
TIERLISTS = Path("src/data/tierlists.json")
OUT_DIR = Path("review")

# tier-list key -> transcript number prefix(es) that cover it
SOURCES: dict[str, list[str]] = {
    "arrows": ["030"],
    "barrels": ["032"],
    "boots": ["046"],
    "cantrips": ["078", "003"],
    "cloaks": ["042"],
    "cloth_armor": ["036"],
    "elixirs": ["027"],
    "finesse_weapons": ["060", "061"],
    "gloves": ["043", "044", "045"],
    "grenades": ["029"],
    "helmets": ["047", "048", "049"],
    "light_armor": ["037"],
    "medium_armor": ["038"],
    "one_handed_weapons": ["066"],
    "poisons_oils": ["031"],
    "polearms": ["064"],
    "potions": ["028"],
    "ranged_weapons": ["059"],
    "rings": ["053", "054", "055"],
    "shields": ["041"],
    "simple_weapons": ["063"],
    "skills": ["001"],
    "staves": ["062"],
    "two_handed_weapons": ["065"],
    "versatile_weapons": ["067", "068"],
    "amulets": ["050", "051", "052"],
    "heavy_armor": ["039"],
}

# A spoken tier declaration is attributed to the single closest item
# mention within this many characters; declarations further than this
# from any rated item are ignored.
MAX_ATTRIB_DIST = 90


def norm(s: str) -> str:
    """Lowercase, strip punctuation, collapse whitespace - matches the
    shape of the auto-caption text so item names line up."""
    s = s.lower().replace("&", " and ")
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def load_transcript(prefixes: list[str]) -> str:
    parts = []
    for p in prefixes:
        hits = sorted(TRANSCRIPTS.glob(f"{p}-*.txt"))
        for h in hits:
            parts.append(h.read_text(encoding="utf-8"))
    return norm(" ".join(parts))


def find_tiers(text: str) -> list[tuple[int, str]]:
    """Positions of explicit spoken tier declarations."""
    out = []
    for m in re.finditer(r"\b([sabcdf]) tier\b", text):
        out.append((m.start(), m.group(1).upper()))
    for m in re.finditer(r"\bs plus\b", text):
        out.append((m.start(), "S+"))
    return sorted(out)


def mentions(needle: str, text: str) -> list[int]:
    out, start = [], 0
    while True:
        i = text.find(needle, start)
        if i < 0:
            return out
        out.append(i)
        start = i + len(needle)


def attribute(items: list[str], text: str, tiers: list[tuple[int, str]]):
    """Assign each spoken tier declaration to the single nearest item
    mention. Returns {item: (tier, snippet)} for items that won a
    declaration. Distance is measured to the *end* of a preceding name or
    the *start* of a following name, so the verdict latches onto whichever
    item name it sits closest to - which de-duplicates the 'previous
    item's verdict' problem."""
    spans = {it: [(p, p + len(norm(it))) for p in mentions(norm(it), text)]
             for it in items if norm(it)}
    won: dict[str, tuple[str, str]] = {}
    best_dist: dict[str, int] = {}
    for pos, tier in tiers:
        # His verdict trails the item ("the X arrow is s tier"), so prefer
        # the nearest item whose name *ends before* this declaration; only
        # fall back to a following item name if none precede it in range.
        prev = None   # (dist, item, mention_start)
        fwd = None
        for it, occ in spans.items():
            for a, b in occ:
                if b <= pos:
                    d = pos - b
                    if prev is None or d < prev[0]:
                        prev = (d, it, a)
                elif a >= pos:
                    d = a - pos
                    if fwd is None or d < fwd[0]:
                        fwd = (d, it, a)
        pick = prev if (prev and prev[0] <= MAX_ATTRIB_DIST) else fwd
        if pick is None or pick[0] > MAX_ATTRIB_DIST:
            continue
        owner_dist, owner, owner_pos = pick
        if owner not in best_dist or owner_dist < best_dist[owner]:
            best_dist[owner] = owner_dist
            snip = text[max(0, owner_pos - 30): owner_pos + len(norm(owner)) + 110].strip()
            won[owner] = (tier, snip)
    return won, spans


def main() -> int:
    tierlists = json.load(open(TIERLISTS, encoding="utf-8"))
    by_key = {t["key"]: t for t in tierlists}

    report = []
    totals = Counter()

    for key, prefixes in SOURCES.items():
        tl = by_key.get(key)
        if not tl:
            continue
        text = load_transcript(prefixes)
        tiers = find_tiers(text)
        won, spans = attribute(list(tl["ratings"]), text, tiers)
        rows = []
        for item, current in sorted(tl["ratings"].items()):
            detected, snip = won.get(item, (None, None))
            if detected is None:
                status = "no_tier_found" if spans.get(item) else "not_mentioned"
            elif detected == current:
                status = "match"
            else:
                status = "conflict"
            totals[status] += 1
            rows.append({
                "item": item, "current": current, "detected": detected,
                "status": status, "snippet": snip,
            })
        report.append({
            "key": key, "subject": tl["subject"],
            "sources": prefixes, "rows": rows,
        })

    OUT_DIR.mkdir(exist_ok=True)
    json.dump(report, open(OUT_DIR / "tier_review.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    # ---- markdown ----
    md = ["# Transcript tier-rating review\n",
          "Heuristic diff of stored ratings vs. tiers spoken in the source "
          "transcripts. **Auto-captions are noisy — verify every row before "
          "editing `tierlists.json`.**\n",
          f"**Totals:** " + ", ".join(f"{k}={v}" for k, v in totals.items()) + "\n"]
    for sec in report:
        c = Counter(r["status"] for r in sec["rows"])
        md.append(f"\n## {sec['subject']}  "
                  f"<sub>({', '.join('#'+s for s in sec['sources'])})</sub>")
        md.append(f"<sub>match={c['match']} · conflict={c['conflict']} · "
                  f"no_tier={c['no_tier_found']} · missing={c['not_mentioned']}"
                  f" · {len(sec['rows'])} rated</sub>\n")
        # lead with the rows that need attention
        order = {"conflict": 0, "no_tier_found": 1, "not_mentioned": 2, "match": 3}
        for r in sorted(sec["rows"], key=lambda r: (order[r["status"]], r["item"])):
            mark = {"match": "✅", "conflict": "❗", "no_tier_found": "🔍",
                    "not_mentioned": "—"}[r["status"]]
            det = r["detected"] or "?"
            snip = (r["snippet"] or "")[:130]
            md.append(f"- {mark} **{r['item']}** — stored `{r['current']}` / "
                      f"heard `{det}`" + (f"  \n  > …{snip}…" if snip else ""))
    (OUT_DIR / "tier_review.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print("totals:", dict(totals))
    print(f"wrote {OUT_DIR}/tier_review.md and tier_review.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
