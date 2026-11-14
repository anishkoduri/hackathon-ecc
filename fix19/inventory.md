# Fix #19 — `system-ui` inventory (built tree, pre-fix19, Nov 11 2026)

Measured with `grep -r -o system-ui` over `hackathon-ecc/` (excl.
`node_modules`). **Total: 191 occurrences in 121 files.**

DEVIATION from SPEC §1: the SPEC's baseline says 139. The measured
baseline is 191. The SPEC's count is stale/wrong; the numbers below are
the measured ones and verify19.py asserts against them.

## By file class

| Class | Occurrences | Files | Disposition |
|---|---|---|---|
| `skills/design-taste-frontend/assets/` demo HTML/CSS | 129 | 76 | Reference/demo-only per SPEC §5 — NOT touched |
| `*.md` rule files | 40 | 31 | Fixed in this fix (must be 0 after) |
| Other (scripts / templates / data) | 22 | 14 | Split below |

## `*.md` rule files (40)

- 30 Hallmark theme files (`references/hallmark/references/themes/*.md`):
  39 occurrences — every one sits in the theme's Tokens block
  (`--font-display` / `--font-body` / `--font-outlier` / `--font-code`
  lines, e.g. `"Geologica", ui-sans-serif, system-ui, sans-serif`).
  The Tokens block IS the built page's `:root` (Taste step 4: "The
  theme's Tokens block is the page's `:root` tokens"), so these are
  shipping templates in scope under SPEC §5. Fixed: the
  `system-ui` + bare-generic tails are stripped from the `--font-*`
  lines; the named faces (the theme's type voice, cf. SPEC §5's Sofia
  precedent — Georgia, Impact, Arial Black, Futura, Iowan Old Style,
  and the named second faces) are RETAINED.
- `skills/polish-pass/reference/lenses/typeset.md`: 1 — the
  system-ui-legitimising sentence (line 55), replaced by TYPESET_F19.

## Other (22)

### Shipping templates — FIXED in this fix (4 occurrences)

| File | N | Why it ships |
|---|---|---|
| `skills/design-taste-frontend/scripts/start.mjs:291` | 1 | `stack()` builds the `font-family` emitted into built-page CSS |
| `skills/design-taste-frontend/references/hallmark/scripts/theme.mjs:470` | 1 | `CUSTOM_TOKENS` scaffold template (`--font-body` with a `system-ui` tail); Taste forbids `draw`/`scaffold`, but the template still generates pages, so the tail is stripped anyway |
| `skills/pitch-deck-video/template/shots.json:33` | 1 | `theme.fonts.sans` is rendered as `fontFamily` in the video template (`theme.ts` → `Captions.tsx` / `Arch.tsx`); Hanken Grotesk is loaded by `fonts.ts`, so the stack is now the bundled face alone |
| `skills/pitch-deck-video/template/shots.example.json:33` | 1 | Same seed, example copy |

### Dev/QA tooling pages — RECORDED, not fixed (12)

| File | N | Why out of scope |
|---|---|---|
| `skills/design-taste-frontend/scripts/fx-gallery.template.html` | 2 | Renders the fx-gallery lab tool page, not a client build |
| `skills/design-taste-frontend/scripts/fx-lab.template.html` | 1 | Renders the fx-lab tool page, not a client build |
| `skills/design-taste-frontend/scripts/moments.mjs` | 3 | Generates QA moment-shot index pages, not client builds |
| `skills/design-taste-frontend/references/hallmark/scripts/sloplint-render.mjs` | 1 | Renders the sloplint QA report page |
| `scripts/lib/control-pane/control-plane-view-ui.js` | 2 | Dev-harness control-plane UI |
| `scripts/lib/control-pane/proximity-viz.js` | 2 | Dev-harness control-plane UI |
| `scripts/lib/control-pane/ui.js` | 1 | Dev-harness control-plane UI |

### Detectors — MUST KEEP (3)

| File | N | Why kept |
|---|---|---|
| `skills/design-taste-frontend/references/hallmark/scripts/sloplint.mjs` | 2 | Names `system-ui` in its generic-family set and its banned-family set — the checker that DETECTS the problem |
| `skills/design-taste-frontend/scripts/consistency.mjs` | 1 | `SYS` regex naming `system-ui` as a system font — a detector |

### Reference data — RECORDED, not fixed (3)

| File | N | Why out of scope |
|---|---|---|
| `skills/ui-ux-pro-max/data/styles.csv` | 3 | Style-catalogue rows (Brutalism row, Apple Native row) describing styles; reference data like the font catalogues in SPEC §5, not delivery instructions |

## Expected post-fix19 totals

- `*.md` rule files: **0**
- Shipping templates (`start.mjs`, `theme.mjs`, `shots.json`,
  `shots.example.json`): **0**
- Remaining `system-ui` in the built tree: **161**
  (129 assets/demo + 12 dev/QA tooling + 3 detectors + 3 reference data
  + 14 fix19 rule-text mentions naming `system-ui` as the banned token:
  Taste 5, orchestrate 4, typeset lens 2, orch-build-mvp 1, polish-pass 1,
  ui-ux-pro-max 1)
- verify19.py asserts the 0s above and records the 147 with its class
  breakdown; it FAILS if any occurrence sits in a template that ships
  into built pages.

## Post-fix-up (Nov 11 2026 — audit #60 MINOR-1/2, sweep #23 MINOR-1)

Engine: `fix19/fix19_fixup.py`. The fix-up did not move the `system-ui`
total: it stays **161** with the same class breakdown (129 assets/demo
+ 12 dev/QA tooling + 3 detectors + 3 reference data + 14 rule-text
mentions), re-verified in the built tree post-fix-up.

- Theme Tokens blocks: the strip now covers ALL 51 theme files (the
  fix19 skip gate is dropped). Fix-up removed 92 bare-generic / `ui-*`
  tail instances from 31 `--font-*` lines in the 20 files that had
  never been stripped (arcade, blueprint, broadside, darkroom, dose,
  editorial, formwork, halftone, hum, newsprint, overprint, pasteup,
  piste, riso, solstice, sport, terminal, terrazzo, vellum, wayfind).
  Post-fix-up state: **0 `--font-*` lines in any of the 51 theme files
  carry a generic/system tail** (verified in the built tree); every
  declaration still names a face (or a `var()`).
- `shots.json` / `shots.example.json`: the serif/mono stacks lost
  their generic tails too (F2 governs — the video template is a
  shipped surface; see `fix19/MANIFEST.md` §6). No `system-ui` was
  involved in either change.
- No fix-up text adds a literal `system-ui` (verify19 still asserts
  the *.md mention count at exactly 14 and the total at 161).
- Verifiers post-fix-up: verify19 75/75, verify15 43/43, verify17
  59/59, verify18 72/72. `build.sh` unchanged: 23,314 lines, md5
  `a8d3d3c6f6d32344d0168c5323d9364b`.
