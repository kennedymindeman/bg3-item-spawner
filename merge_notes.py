"""Merge a review/<key>_verified.json file's `why` strings into that tier
list's `notes` object in src/data/tierlists.json.

Usage: uv run merge_notes.py <key> [<key> ...]

Verifies every rated item has a why and that every verified tier matches the
stored tier before writing. Run `uv run build.py` afterwards.
"""
import json
import sys

TL_PATH = "src/data/tierlists.json"


def merge(key: str) -> int:
    data = json.load(open(TL_PATH))
    ver = json.load(open(f"review/{key}_verified.json"))
    notes = {k: v["why"] for k, v in ver["ratings"].items()}
    tl = next((t for t in data if t["key"] == key), None)
    if tl is None:
        raise SystemExit(f"no tier list with key {key!r}")
    missing = [k for k in tl["ratings"] if k not in notes]
    mismatch = [k for k in tl["ratings"]
                if ver["ratings"].get(k, {}).get("tier") != tl["ratings"][k]]
    if missing:
        raise SystemExit(f"{key}: rated items missing a why: {missing}")
    if mismatch:
        raise SystemExit(f"{key}: verified tier != stored tier: {mismatch}")
    extra = [k for k in notes if k not in tl["ratings"]]
    if extra:
        raise SystemExit(f"{key}: verified items not in tier list: {extra}")
    tl["notes"] = notes
    json.dump(data, open(TL_PATH, "w"), ensure_ascii=False, indent=2)
    return len(notes)


if __name__ == "__main__":
    for key in sys.argv[1:]:
        print(f"merged {key}: {merge(key)} notes")
