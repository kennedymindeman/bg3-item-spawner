#!/usr/bin/env python3
"""Download the spell-rune icons referenced by src/data/spell_icons.json into
icons/ so the app loads them locally instead of hammering bg3.wiki at runtime
(which rate-limits with HTTP 429 -> blank glyphs).

    uv run fetch_icons.py            # fetch any missing icons into icons/

Polite: sequential, with a delay between requests and exponential backoff on
429/5xx. Re-running only fetches files that are missing or zero-length, so it's
resumable. The app references icons/<basename> via a relative path; the basename
is taken from the Special:FilePath URL (e.g. .../Aid_Icon.webp -> Aid_Icon.webp).
"""

import json
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

ICONS = Path("icons")
SRC = Path("src") / "data" / "spell_icons.json"
UA = "bg3-item-spawner-icon-fetch/1.0 (local reference build; one-time vendor)"
DELAY = 20.0         # seconds between requests: stay UNDER bg3.wiki's rate limit
                     # so we never trip the sticky 429 penalty box in the first place
MAX_RETRIES = 5
COOLDOWN = 150       # quiet seconds before the first request (clears penalty box)


def basename_for(url: str) -> str:
    # https://bg3.wiki/wiki/Special:FilePath/Aid_Icon.webp -> Aid_Icon.webp
    return url.rstrip("/").split("/")[-1]


def fetch(url: str, dest: Path) -> bool:
    backoff = 12.0
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                data = r.read()
            if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
                dest.write_bytes(data)
                return True
            # Sometimes FilePath redirects to PNG; accept any image-ish payload.
            if data[:8] == b"\x89PNG\r\n\x1a\n" or data[:3] == b"\xff\xd8\xff":
                dest.write_bytes(data)
                return True
            print(f"  ! unexpected payload ({len(data)}B) for {url}", file=sys.stderr)
            return False
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < MAX_RETRIES:
                wait = backoff * attempt
                print(f"  {e.code} on {dest.name}; backing off {wait:.0f}s "
                      f"(attempt {attempt}/{MAX_RETRIES})")
                time.sleep(wait)
                continue
            print(f"  ! HTTP {e.code} for {url}", file=sys.stderr)
            return False
        except (urllib.error.URLError, TimeoutError) as e:
            if attempt < MAX_RETRIES:
                time.sleep(backoff * attempt)
                continue
            print(f"  ! {e} for {url}", file=sys.stderr)
            return False
    return False


def main() -> int:
    ICONS.mkdir(exist_ok=True)
    icons = json.loads(SRC.read_text(encoding="utf-8"))
    total = len(icons)
    ok = skipped = failed = 0
    # Cooldown lead-in: bg3.wiki throttles bursts with a sticky 429 penalty box;
    # a quiet pause before resuming gives it time to clear. Skip if already done.
    pending = [u for u in icons.values()
               if not (ICONS / basename_for(u)).exists()]
    if pending and COOLDOWN:
        print(f"{len(pending)} icons to fetch; cooling down {COOLDOWN}s first "
              f"to clear any rate-limit penalty...", flush=True)
        time.sleep(COOLDOWN)
    for i, (name, url) in enumerate(sorted(icons.items()), 1):
        dest = ICONS / basename_for(url)
        if dest.exists() and dest.stat().st_size > 0:
            skipped += 1
            continue
        print(f"[{i}/{total}] {name} -> {dest.name}")
        if fetch(url, dest):
            ok += 1
        else:
            failed += 1
        time.sleep(DELAY)
    print(f"\ndone: {ok} fetched, {skipped} already present, {failed} failed "
          f"({total} total)")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
