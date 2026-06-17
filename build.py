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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
