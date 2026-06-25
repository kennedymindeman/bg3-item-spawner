# BG3 Item Spawner / Script Extender Console

A single-file HTML reference for Baldur's Gate 3: item spawner, console commands,
and Honour Mode tier lists.

## Open the website

**Live site: https://kennedymindeman.github.io/bg3-item-spawner/**

Or open it locally: double-click **`bg3_console.html`** (or `index.html`, an
identical copy) — it opens in any browser, no server or install needed.
Everything is inlined.

To copy a spawn command, find an item and click it; paste the command into the
Script Extender console in-game.

## Editing

`bg3_console.html` / `index.html` are **generated — don't hand-edit.** Change the
sources in `src/`, then rebuild:

```
uv run build.py
```

See `CLAUDE.md` for the data model and project layout.
