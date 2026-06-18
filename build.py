#!/usr/bin/env python3
"""Inline the split data back into a single self-contained HTML file.

    uv run build.py            # -> bg3_console.html (repo root)

Source lives in src/:
    src/index.html          the app (CSS + markup + logic) with @DATA markers
    src/data/items.json     spawnable item database
    src/data/tierlists.json tier ratings (regenerated from transcripts)

The single-file bg3_console.html at the repo root is GENERATED. Edit
src/, then re-run this script; don't hand-edit the root file.

The two markers in src/index.html:
    const ITEMS=/*@DATA:items*/[];
    const TIERLISTS=/*@DATA:tierlists*/[];
are replaced with the minified JSON so the shipped file stays portable
(open directly / paste-and-go, no server, no fetch).
"""

import json
from pathlib import Path

SRC = Path("src")
OUT = Path("bg3_console.html")

# marker -> json file
DATA = {
    "items": SRC / "data" / "items.json",
    "tierlists": SRC / "data" / "tierlists.json",
    "builds": SRC / "data" / "builds.json",
    "breakpoints": SRC / "data" / "breakpoints.json",
    "spellicons": SRC / "data" / "spell_icons.json",
}


def main() -> int:
    html = (SRC / "index.html").read_text(encoding="utf-8")

    for key, path in DATA.items():
        data = json.loads(path.read_text(encoding="utf-8"))  # validates JSON
        minified = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
        marker = f"/*@DATA:{key}*/[]"
        if marker not in html:
            raise SystemExit(f"marker {marker!r} not found in src/index.html")
        html = html.replace(marker, minified)
        print(f"inlined {key}: {len(data)} entries")

    OUT.write_text(html, encoding="utf-8")
    # Also emit index.html so the root URL works on any static host (GitHub Pages, etc.)
    Path("index.html").write_text(html, encoding="utf-8")
    print(f"\nwrote {OUT} and index.html ({OUT.stat().st_size:,} bytes)")

    # Spell-rune icons are vendored into icons/ (sidecar, lazy-loaded) so the app
    # doesn't hit bg3.wiki at runtime (it rate-limits -> blank glyphs). Warn if any
    # referenced icon is missing; run `uv run fetch_icons.py` to fetch them.
    from urllib.parse import unquote
    icons = json.loads((SRC / "data" / "spell_icons.json").read_text(encoding="utf-8"))
    # Decode %27 etc. so the check matches the on-disk filenames (Tasha's_..., not
    # Tasha%27s_...), same as fetch_icons.py basename_for and the app's img.src.
    wanted = {unquote(url.rstrip("/").split("/")[-1]) for url in icons.values()}
    have = {p.name for p in Path("icons").glob("*")} if Path("icons").is_dir() else set()
    missing = wanted - have
    if missing:
        print(f"WARNING: {len(missing)}/{len(wanted)} spell icons missing from icons/ "
              f"(runes fall back to letters). Run: uv run fetch_icons.py")
    else:
        print(f"icons: all {len(wanted)} spell-rune icons present in icons/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
