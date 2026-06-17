#!/usr/bin/env python3
"""Build src/data/spell_icons.json: a {spell name -> bg3.wiki icon URL} map for
every spell named in builds.json, so the Builds tab can show each pick's in-game
icon "rune" (name on hover), matching how the level-up GUI displays spells.

BG3 wiki serves each spell's icon as `<Spell Name>_Icon.webp` via Special:FilePath
(verified against the live wiki for the spells used here). By default we generate
those URLs by convention with NO network calls — the browser loads them at
runtime and the UI falls back to a lettered tile on any 404 (img onerror).

    uv run fetch_spell_icons.py            # offline, by convention (default)
    uv run fetch_spell_icons.py --verify   # also HTTP-check each URL (paced; can hit wiki rate limits)
"""
import json
import sys
import urllib.parse
from pathlib import Path

FILEPATH = "https://bg3.wiki/wiki/Special:FilePath/"
BUILDS = Path("src/data/builds.json")
OUT = Path("src/data/spell_icons.json")

# Spells whose icon file deviates from the "<Name>_Icon.webp" convention.
OVERRIDES = {
    "Conjure Woodland Beings": "Conjure_Woodland_Being_Icon.webp",
}


def spell_names() -> list[str]:
    data = json.loads(BUILDS.read_text(encoding="utf-8"))
    names = set()
    for b in data:
        for lvl in b.get("leveling", []):
            names.update(lvl.get("spells", []) or [])
    return sorted(names)


def icon_file(name: str) -> str:
    return OVERRIDES.get(name, name.replace(" ", "_") + "_Icon.webp")


def verify(url: str) -> bool:
    import urllib.request
    req = urllib.request.Request(url, headers={"User-Agent": "bg3-item-spawner spell-icon fetch"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.headers.get("Content-Type", "").startswith("image/")
    except Exception:
        return False


def main() -> int:
    do_verify = "--verify" in sys.argv
    names = spell_names()
    out, bad = {}, []
    for name in names:
        url = FILEPATH + urllib.parse.quote(icon_file(name))
        if do_verify:
            import time
            ok = verify(url)
            time.sleep(0.8)
            if not ok:
                bad.append(name)
                print(f"??  {name}: {url} did not resolve")
                continue
            print(f"ok  {name}")
        out[name] = url
    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\nWrote {len(out)} spell icon URLs -> {OUT}" + (" (verified)" if do_verify else " (by convention)"))
    if bad:
        print("Did not resolve:", ", ".join(bad))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
