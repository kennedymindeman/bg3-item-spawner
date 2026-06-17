#!/usr/bin/env python3
"""Download every transcript in a YouTube playlist as clean plain text.

Usage:
    uv run get_transcripts.py "<playlist or video+list URL>" [output_dir]

    output_dir defaults to transcripts/. Pass a different dir (e.g.
    build_transcripts) to index a separate playlist with the same
    <index>-<title>.txt scheme without colliding with the tier-list set.

Steps:
  1. yt-dlp downloads English subtitles (manual, falling back to auto) as VTT.
  2. Each VTT is parsed into deduplicated plain text and written to <out>/<index>-<title>.txt
  3. The intermediate .vtt files are removed.
"""

import re
import sys
import subprocess
from pathlib import Path


def download_subs(playlist_url: str, vtt_dir: Path) -> None:
    vtt_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        "yt-dlp",
        "--skip-download",
        "--write-subs",
        "--write-auto-subs",
        "--sub-langs", "en.*",          # en, en-US, en-orig, etc.
        "--sub-format", "vtt",
        "--sleep-requests", "1",        # be polite / avoid rate limiting
        "--ignore-errors",              # skip videos with no captions
        "-o", str(vtt_dir / "%(playlist_index)03d-%(title)s.%(ext)s"),
        playlist_url,
    ]
    subprocess.run(cmd, check=False)


def vtt_to_text(vtt_path: Path) -> str:
    lines: list[str] = []
    last = None
    for raw in vtt_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith(("WEBVTT", "Kind:", "Language:", "NOTE")):
            continue
        if "-->" in line:               # timestamp cue line
            continue
        if line.isdigit():              # numeric cue index
            continue
        # strip inline timing/formatting tags like <00:00:01.000> and <c>
        line = re.sub(r"<[^>]+>", "", line)
        line = line.strip()
        if not line or line == last:    # collapse the heavy auto-caption duplication
            continue
        lines.append(line)
        last = line
    return "\n".join(lines)


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: uv run get_transcripts.py <playlist_url> [output_dir]", file=sys.stderr)
        return 1
    playlist_url = sys.argv[1]
    out_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("transcripts")
    vtt_dir = out_dir / "_vtt"

    download_subs(playlist_url, vtt_dir)

    vtts = sorted(vtt_dir.glob("*.vtt"))
    if not vtts:
        print("No subtitle files were downloaded.", file=sys.stderr)
        return 1

    seen_base: set[str] = set()
    for vtt in vtts:
        # filename: 001-Some Title.en.vtt  ->  base 001-Some Title
        base = vtt.name.rsplit(".", 2)[0]
        if base in seen_base:           # keep only one lang variant per video
            continue
        seen_base.add(base)
        text = vtt_to_text(vtt)
        out = out_dir / f"{base}.txt"
        out.write_text(text + "\n", encoding="utf-8")
        print(f"ok  {out}")

    # clean up intermediate vtt files
    for vtt in vtt_dir.glob("*.vtt"):
        vtt.unlink()
    vtt_dir.rmdir()

    print(f"\nDone. {len(seen_base)} transcripts in {out_dir}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
