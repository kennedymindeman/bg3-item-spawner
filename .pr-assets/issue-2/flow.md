# Flow: search, copy and empty states (issue #2 design pass)

Script: `~/inbox/design-pass-2026-11-03/after/bg3-item-spawner/flow.py` (uv single-file Playwright script).
Output: `~/inbox/design-pass-2026-11-03/after/bg3-item-spawner/flow.txt` (ALL PASS).

The script serves the built `index.html` from the worktree over `http://127.0.0.1` (a secure context, like GitHub Pages) in headless Chromium. It reads the real clipboard after each copy.

Steps:
1. Load the page at 1440px. Builds is the selected tab. ArrowRight moves to Breakpoints and a focus ring shows. ArrowLeft goes back.
2. Press `/`, which focuses build search. Type `zzqx`: the empty state shows the query. Click "Clear search and filter": all builds come back.
3. Open the first build, then press Esc to close it.
4. Go to Item Spawner, press `/`, type `boots of speed`, then press ArrowDown right away. Focus lands on the Copy button for Boots of Speed. Press Enter: the clipboard holds `TemplateAddTo("8b22d15a-…", GetHostCharacter(), 1)`, the button shows "Copied" in green, and the live region says "Copied to clipboard". The label reverts after about 1.6s.
5. Set quantity to 3 and copy again: the command ends `, 3)`.
6. Click a tier badge: the tier filter switches to that tier.
7. Search `zzqxv`: the empty state shows the query. Clear resets the search and the tier filter.
8. Commands: search `gold`, which leaves one card. Copy puts `AddGold(GetHostCharacter(), 1000)` on the clipboard. A no-match search, then Clear, brings back all 14 cards.
9. Tier lists: search `boots`, open the first pill, and copy its spawn command.
10. Check for page errors: none.
11. At 390px, switch through every tab and open a build's detail. `document.documentElement.scrollWidth` is at most 390 everywhere.

Final screenshot: `~/inbox/design-pass-2026-11-03/after/bg3-item-spawner/state-items-copied-1440.png`. The full-page screenshots are `1440.png` and `390.png` in the same folder.

Tested commit: the PR head commit, the one that adds this file. The worktree had no other uncommitted changes when the flow ran.
Data: live. This is the repo's own bundled `items.json`, `tierlists.json` and `builds.json`; nothing synthetic.
