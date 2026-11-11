# Hallmark — provenance (staged, scoped)

Source: **Nutlope/hallmark**, by Hassan El Mghari (nutlope) / Together AI,
MIT license. Version **2.0.0**, pinned HEAD commit
`7e213cb6feb4ef82733bd66a0600b2e54ca0994c` (2026-11-10 18:01 UTC; verified by `git rev-parse HEAD`
on the sparse checkout before staging). The repo has **no GitHub
releases and no tags** — the SHA is the pin.

## What was staged (text only, no binaries, no images)

- `references/themes/` — the 50-theme material catalog: 50 `.md` files +
  `index.json` + `README.md` (~424 KB text). The 50 `.jpg` pictures were
  NOT staged: the deal/pick step degrades to header + material
  description (the theme file's `material` line + feel paragraph) instead
  of the picture. The `.jpg`s total 5.0 MB and remain available upstream.
- `scripts/theme.mjs` — `deal` (3 themes, pick 1), `draw`, `photos`,
  `log`, `index`, `validate`, `check`, `scaffold`. Only `deal` (+ `log`,
  `photos`, `check`, `index`, `validate`) is wired in this plugin; `draw`
  and `scaffold` are NOT used — Taste owns shape + scaffold.
- `scripts/sloplint.mjs` — the mechanical gate checker (zero dependencies,
  Node 18+). `scripts/sloplint-render.mjs` — the render tier (needs
  `puppeteer-core@25.17.0` + Chrome; static tier runs without them).
- `scripts/photos.json` — 755 Wikimedia photo URLs + metadata only, no
  image bytes (needed by `theme.mjs photos`).
- `references/gates.md` — the full gate list: 90 clauses, 71 numbers
  (14 retired), tiers 39 Floor / 50 Reflex / 1 Ledger, + 26 Finish
  checks F1-F26. (Older write-ups say "57 gates" — that count does not
  match v2.0.0.)
- `references/review-hero.md`, `references/review-finish.md` — the
  fresh-context reviewer prompts (hero review, finish review).
- `references/redesign.md` — the redesign flow (keeps content + wiring).
- `references/hallmark-floor.md` — condensed Floor + 6-axis critique,
  written for this plugin from upstream SKILL.md + gates.md §3.

## What was NOT staged (and why)

- `skills/hallmark/SKILL.md` — Hallmark is NOT a separate skill in this
  plugin and has no `/hallmark` command; Taste leads landing builds and
  deals from this catalog. No `study` verb exists in v2.0.0 (verbs are
  build / redesign / audit only).
- The 50 `.jpg` theme pictures (see above).
- `references/layout.md`, `anatomy.md`, `craft.md`, `direction.md`,
  `imagery.md`, `patterns.md`, `flow.md`, `genres/`, `macrostructures/`,
  `texture.md`, etc. — Hallmark's build playbook; Taste owns the build.
- `scripts/capture.mjs`, `scripts/picture.mjs` — covered by polish-pass
  `capture.mjs` + browser-qa.
- `scripts/install.mjs`, `scripts/install-hook.mjs`,
  `scripts/lint-hook.mjs` — no Cursor edit-time hook exists upstream;
  this plugin has its own hooks.
- `scripts/imagegen.mjs` — Together AI FLUX image generation (needs
  `TOGETHER_API_KEY`). Never wired; the plugin never generates images.
- `scripts/refcheck.mjs` — upstream CI consistency gate, not runtime.
- `site/` (usehallmark.com demo pages, ~228 MB repo bulk) and `eval/` —
  never checked out.

## Windows notes (primary platform)

- `sloplint-render.mjs` resolves Chrome via `CHROME_PATH` first, then a
  hardcoded list that includes only the 64-bit path
  `C:\Program Files\Google\Chrome\Application\chrome.exe` (32-bit and
  per-user `%LOCALAPPDATA%` installs are NOT listed). If Chrome is not
  found, set `CHROME_PATH` (PowerShell:
  `$env:CHROME_PATH = 'C:\Program Files\Google\Chrome\Application\chrome.exe'`;
  Git Bash: `CHROME_PATH='C:/Program Files/Google/Chrome/Application/chrome.exe'`).
- All skill shell commands are `node <script> …` (shell-agnostic); no
  `.sh`/`.bat`/`.ps1`, no curl/wget/pipe-to-shell, no chmod.
- `theme.mjs log --entry '<json>'` examples use single quotes (Git Bash
  syntax); in PowerShell use double quotes with inner-quote escaping.
- Render tier needs `puppeteer-core@25.17.0` (pinned; `npm i -g
  puppeteer-core@25.17.0` when it is missing). It cannot reuse the
  plugin's Playwright 1.65.0 as a drop-in: `sloplint-render.mjs` is written
  directly against the Puppeteer API. The browser binary itself is shared
  (system Chrome), so no second browser download.
