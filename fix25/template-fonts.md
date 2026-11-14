# Fix #25 §4(b) — template-fonts self-host (worker D)

## What was wrong

`new-skills/pitch-deck-video/template/src/fonts.ts` loaded Hanken Grotesk /
Instrument Serif / JetBrains Mono via `@remotion/google-fonts`, which fetches
woff2 files from `fonts.gstatic.com` at render time. In sandbox Chrome that
fetch fails (`net::ERR_SSL_PROTOCOL_ERROR`, see
`fix24/dryrun39/qa-run.log`), and `@remotion/google-fonts`' loader cancels
the render on fetch failure — the long-standing dry-run Leg 3 environmental
FAIL. `template/package.json` carried `"@remotion/google-fonts": "4.0.526"`.

## Edits (staged sources only; built tree NOT touched)

All under `new-skills/pitch-deck-video/template/`:

1. **New files** — `public/fonts/` (3 files, 86,112 bytes total):
   - `HankenGrotesk.woff2` — 34,704 B, md5 `c501f578bf3fc800c20056df516ed9f2`
   - `InstrumentSerif.woff2` — 21,032 B, md5 `9b8dd1ecf641700bf1caa9d17da6374e`
   - `JetBrainsMono.woff2` — 30,376 B, md5 `3c6529ccf6d0b95f879202e8da9fd08a`
2. **`src/fonts.ts` (rewritten)** — now uses `@remotion/fonts` `loadFont`
   (the Remotion-documented local-font pattern, remotion.dev/docs/fonts)
   with `staticFile('fonts/….woff2')` URLs. Same family names the components
   use via `shots.json → theme.fonts`, so **no component changed**. Weights:
   Hanken `'100 900'`, Instrument `'400'`, JetBrains `'400 500'`.
   `loadFont` delays the render until each face loads and cancels the render
   (fail-closed) if a local file cannot be fetched — same fail-closed shape
   as the old loader. A header comment records the why + the provenance.
3. **`package.json`** — removed `"@remotion/google-fonts": "4.0.526"`, added
   `"@remotion/fonts": "4.0.526"` (same pinned version as the rest of
   Remotion, kept alphabetical). No other dependency changed.
4. **No template doc edit was needed**: no template doc described the font
   loading mechanism. Checked: `SKILL.md` (only the Bang-upstream note at
   :225, which is about upstream Bang Motion, not the template, and the
   self-hosted-static stance at :253, which is now true of the template too),
   `references/shots-reference.md`, `references/troubleshooting.md`,
   `commands/demo.md` — none mentions the template's font loading.
   `build.sh` needs no change: line 230 copies the whole template dir with
   `cp -r`, so `public/fonts/` flows into the built tree on the next build.
   No prior verifier asserts `@remotion/google-fonts` (grepped
   `fix22/verify22.py`, `fix23/verify23.py`, `fix24/verify24.py` and the
   dry-run scripts — the only "Instrument Serif" hit is an unrelated slop
   label in verify22.py).

## Where the fonts came from

Downloaded 2026-11-13 from Google Fonts (curl from this sandbox —
`fonts.googleapis.com` and `fonts.gstatic.com` both reachable via curl;
only sandbox *Chrome* fails them with `ERR_SSL_PROTOCOL_ERROR`):

- css2 API (Chrome UA, to get woff2 URLs), latin subset only:
  - `https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600;700&display=swap`
  - `https://fonts.googleapis.com/css2?family=Instrument+Serif&display=swap`
  - `https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap`
- Files fetched from `fonts.gstatic.com`:
  - Hanken: `https://fonts.gstatic.com/s/hankengrotesk/v12/ieVn2YZDLWuGJpnzaiwFXS9tYtpd59A.woff2`
  - Instrument: `https://fonts.gstatic.com/s/instrumentserif/v5/jizBRFtNs2ka5fXjeivQ4LroWlx-6zUTjg.woff2`
  - JetBrains: `https://fonts.gstatic.com/l/font?kit=tDbv2o-flEEny0FZhsfKu5WU4zr3E_BX0PnT8RD8yKwBNntkaToggR7BYaTNPxDcwg&skey=48ad01c60053c2ae&v=v24`
  (Note: these are the *same* URLs the old loader fetched — cf. the failing
  URLs in `fix24/dryrun39/qa-run.log` — now vendored instead of fetched.)
- Verified with `fontTools` 4.46.0: all three are genuine woff2 (`wOF2`
  magic). **Variable-font finding:** Google serves Hanken Grotesk and
  JetBrains Mono as variable fonts — one file covers the whole weight range
  (Hanken `wght` 100–900, JetBrains `wght` 400–500; all requested weights
  returned byte-identical files, same md5). Instrument Serif is static 400
  only. So 3 files cover the 7 weight slots the old code requested
  (Hanken 400/500/600/700, Instrument 400, JetBrains 400/500).
- No usable local source existed first: searched the plugin tree and system
  fonts — no Hanken / Instrument / JetBrains font files anywhere
  (`~/.fonts/` holds only Fraunces + Inter; the only `jetbrains*` hit in the
  tree is an unrelated SVG icon).
- `@remotion/fonts` API was verified from the published 4.0.526 tarball
  before use: `loadFont({family, url, weight?, …}) => Promise<void>`,
  calls `delayRender` synchronously, `fetch`es the URL, builds a `FontFace`
  with the given descriptors, `font.load()`, registers it in Remotion's
  internal font registry, `continueRender`; on error `cancelRender`.

## Proof (in `fix25/scratch/`, proof copy deleted after, logs + stills kept)

Setup (exact dry-run Leg 3 replica): fresh copy of the edited staged
template + the dry-run #37/38/39 fixture `shots.json` and
`src/vo-durations.json` from `fix24/dryrun39/demo-sample-video/`
(12 beats, narration `none`, `musicBed` false, runtime 84.1s). `npm install`
exit 0, 257 packages; `@remotion/fonts` present in `node_modules`,
`@remotion/google-fonts` absent. `TMPDIR` redirected to the scratch dir
(Chrome shared-memory needs it; `/tmp` hygiene per fix #24).

1. **`node scripts/qa.mjs`** — the exact command that failed in dry-run #39
   (`qa-proof.log`, 265s):
   - **12/12 stills rendered** (`out/qa/00111_problem.png` …
     `02408_close.png`) + 2 ffmpeg contact sheets — the `remotion still`
     step that died on the Google Fonts fetch in dry-run #39 now succeeds.
   - `grep -ci "fonts.googleapis|fonts.gstatic" qa-proof.log` → **0**.
   - `qa.mjs` exit code is **1, but NOT for fonts**: the only failures are
     6 fix-#18 coverage BLOCKINGs ("feature → beat produced no footage")
     because this proof copy has no recording — the fixture's
     `capture/marks.json` is empty (0 marks), same state as the dry-run
     fixture. No `remotion still` invocation failed. I am NOT claiming
     `qa.mjs` exit 0; that needs the record step + the dry-run worker's
     Leg 3 verdict.
2. **Visual check** (seed theme fonts swapped into the fixture `shots.json`
   in the scratch copy only, `theme.fonts` =
   `"Hanken Grotesk" / "Instrument Serif" / "JetBrains Mono"`):
   - `remotion still --frame=2227` (arch card) exit 0, `--frame=2408`
     (close card) exit 0; both logs 0 Google-font mentions.
   - Viewed both PNGs (`fix25/scratch/arch-2227.png`,
     `close-2408.png`): Instrument Serif display type ("How it works",
     "Pantry Pal" — its distinctive high-contrast face, not a Georgia
     fallback), JetBrains Mono labels ("INPUT / CODE / OUTPUT",
     "static HTML — no runtime code"), Hanken Grotesk body + the bold
     caption bar ("The whole app is static pages served locally —",
     weight 700 interpolated from the variable font). All three families
     visibly paint.
3. **Negative control** (`neg-control.log`): with `public/fonts/` moved
   aside, the same still render exits 1 with
   `[http://localhost:3000/public/fonts/HankenGrotesk.woff2] Failed to load
   resource: 404` (same for the other two) and
   `Error: Failed to load font "/public/fonts/HankenGrotesk.woff2": 404 Not
   Found`. This proves the render fetches the fonts from the **local**
   Remotion static server (`localhost:3000`), not from Google, and that the
   loader fails closed. Fonts restored afterwards; `shots.json` restored to
   the fixture version.

## What this does / does not claim

- DOES show: the template renders with no Google Fonts request, in the same
  sandbox Chrome that failed the old fetch; the Leg 3 environmental FAIL's
  cause is removed at the template level.
- Does NOT claim the dry-run Leg 3 clear (59/59) — that verdict belongs to
  the dry-run worker running the full Leg 3 on the rebuilt plugin.
- Does NOT claim the live smoke test — a live film + live `qa.mjs` exit 0 in
  Anish's Cursor is still owed by the smoke test, as before.

## Still owed / notes for the coordinator

- The **built tree** (`hackathon-ecc/skills/pitch-deck-video/template/`)
  still carries the old `fonts.ts` + `@remotion/google-fonts` dep — by rule
  it is never edited directly; it picks this up when `build.sh` re-stages
  (line 230 `cp -r`). Verify25 / the audit should confirm the staged copy
  lands there (and that no stale `@remotion/google-fonts` remains in the
  built tree afterwards).
- The /demo contract is untouched: no change to runtime, filming (local
  only), budget cap, or the voice fallback chain — only the font loading
  mechanism changed. `src/Video.tsx`, `src/theme.ts`, all scenes/parts, all
  scripts, and `shots.json` are byte-identical to before except the two
  files above.
- Scratch cleaned: proof copy (`demo-proof/`, incl. its `node_modules`) and
  the `@remotion/fonts` tarball extract deleted; kept in
  `fix25/scratch/`: `fonts/` (downloaded css + woff2, provenance),
  `qa-proof.log`, `visual-arch.log`, `visual-close.log`,
  `neg-control.log`, `npm-install.log`, `arch-2227.png`,
  `close-2408.png`, `sheet_01.png`.
