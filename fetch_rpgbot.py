#!/usr/bin/env python3
"""Scrape rpgbot.net BG3 class handbooks for build-relevant data.

SECONDARY SOURCE — keep separate from the Cephalopocalypse builds and tag it
distinctly (see CLAUDE.md). Per class we pull only what fills a gap in our
builds: rpgbot's race shortlist (rated per class) and its ability-priority
one-liner, plus the guide URL. Writes review/rpgbot_class_data.json.

Only the 9 classes rpgbot has published are available; Monk, Ranger and Druid
have no handbook yet, so builds led by those classes get no rpgbot block.

Usage: uv run fetch_rpgbot.py
"""

import json
import re
import time
import urllib.request
from pathlib import Path

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")
BASE = "https://rpgbot.net/video-games/baldurs-gate-3/classes/"
CLASSES = ["bard", "fighter", "barbarian", "wizard", "sorcerer",
           "cleric", "paladin", "warlock", "rogue"]


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def strip_tags(s: str) -> str:
    import html
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def section(label: str, doc: str) -> str | None:
    m = re.search(r"<h2[^>]*>\s*" + re.escape(label), doc, re.I)
    if not m:
        return None
    rest = doc[m.end():]
    nxt = re.search(r"<h2", rest, re.I)
    return rest[:nxt.start()] if nxt else rest[:6000]


def dedup(seq):
    seen, out = set(), []
    for x in seq:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def parse_races(races: str):
    """Top (blue) and good (green) races, each subrace qualified by its parent
    race (the enclosing <h3>) since rpgbot ratings sit on bare subrace names."""
    heads = list(re.finditer(r"<h3[^>]*>(.*?)</h3>", races, flags=re.S | re.I))
    segs = []
    if heads:
        segs.append((None, races[:heads[0].start()]))
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(races)
        segs.append((strip_tags(m.group(1)), races[m.end():end]))
    top, good = [], []
    for parent, body in segs:
        for color, name in re.findall(
                r'<span class="rating-(red|orange|green|blue)">([^<]+)</span>', body):
            nm = strip_tags(name)
            if nm.lower() in ("red", "orange", "green", "blue"):
                continue                       # the rating legend, not a race
            if parent and parent.lower() not in nm.lower():
                nm = f"{nm} {parent}"          # "Deep" under Gnome -> "Deep Gnome"
            (top if color == "blue" else good).append(nm)
    return dedup(top), dedup(good)[:6]


def parse(cls: str, doc: str) -> dict:
    cap = cls.capitalize()
    # Only the reliable, non-duplicative signal: rpgbot's top (blue-rated) race
    # picks for the class, plus the guide URL. The green list is generic across
    # classes and the ability spread is already covered by the primary builds.
    top, _ = parse_races(section(cap + " Races", doc) or "")
    return {"url": BASE + cls + "/", "races_top": top}


def main() -> int:
    out = {}
    for cls in CLASSES:
        try:
            doc = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", fetch(BASE + cls + "/"),
                         flags=re.S | re.I)
            out[cls] = parse(cls, doc)
            print(f"ok  {cls}: top races={out[cls]['races_top']}")
        except Exception as e:
            print(f"skip {cls}: {e}")
        time.sleep(1)
    dest = Path("review/rpgbot_class_data.json")
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\nwrote {dest} ({len(out)} classes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
