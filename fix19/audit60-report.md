# Audit #60 — fix #19 audit (font identity, forced font choice, Tiempos body font, thought-out decisions)

**Date:** Nov 11, 2026 (~20:14 CST)
**Auditor:** audit #60 worker (check only — no plugin file edited, build.sh not run,
Campus Eats artifact not touched)
**Built tree:** `~/workspace/hackathon-plugin/hackathon-ecc/`
**Build state:** build.sh 23,314 lines, md5 `a8d3d3c6f6d32344d0168c5323d9364b`
(post-fix19). Builds 1 and 2: manifest sha256
`096b8ca3227c8b7d90db5ddb15b71faf701d83d0457badefe349af8b80090727` on both,
file lists identical, diff 0 (per `fix19/MANIFEST.md`; not re-built here —
read-only audit).
**Verifiers re-run by this audit:** `fix19/verify19.py` 75/75 PASS;
`fix15/verify15.py` 43/43 PASS; `fix17/verify17.py` 59/59 PASS;
`fix18/verify18.py` 72/72 PASS (each run directly, not only as verify19
subprocesses).

## Verdict: NOT CLEAN — 0 BLOCKING, 2 MINOR

Fix #19 is implemented exactly as the SPEC places it, all prior anchors
hold, and the tail-strip did its job on the 30 files it ran on. But the
tree still ships two live font paths that contradict the new F2 rule's own
letter: bare-generic/system tails in 20 Hallmark theme Tokens blocks
(MINOR-1), and the `start.mjs` Google Fonts variable-font link that goes
into the built page's head (MINOR-2). Both are pre-existing conditions the
fix scoped around rather than fixed, and both are caught downstream by the
STATIC19 Type-list check / D1 face check — which is why both are minor,
not blocking. Both fix-ups are small and named below.

## Findings

### MINOR-1 — 20 Hallmark theme files still ship bare-generic / system tails in their Tokens blocks, contradicting F2

F2 (Taste `:256`) bans "no bare generic `sans-serif`/`serif` as a live path"
and "NO system-ui / system fallback anywhere as a live path — the stack
names bundled faces only". The theme Tokens block IS the built page's
`:root` (Taste `:242`), so these stacks ship into built pages. 31
`--font-*` lines in 20 of the 51 theme files still carry generic tails:

- `arcade.md:29`, `blueprint.md:28-29`, `broadside.md:27-28`,
  `darkroom.md:27`, `dose.md:31-32`, `editorial.md:27`, `formwork.md:30-31`,
  `halftone.md:28`, `hum.md:32-33`, `newsprint.md:27-28`, `overprint.md:30-31`,
  `pasteup.md:27`, `piste.md:28`, `riso.md:27`, `solstice.md:28-29`,
  `sport.md:28-29`, `terminal.md:30`, `terrazzo.md:28-29`, `vellum.md:28-29`,
  `wayfind.md:27`
- e.g. `darkroom.md:27`: `--font-display: "Sofia Sans Extra Condensed", ui-sans-serif, sans-serif; --font-body: "Barlow", ui-sans-serif, sans-serif;`
- e.g. `editorial.md:27`: `--font-body: "Source Serif 4", ui-serif, Georgia, serif;`
- e.g. `hum.md:32`: `--font-display: "Chillax", ui-rounded, ui-sans-serif, sans-serif;`
- `ui-sans-serif` / `ui-serif` / `ui-monospace` are system-font keywords, not
  named faces; the bare `sans-serif` / `serif` / `monospace` tails are
  exactly the fallback F2 bans. A build dealing `darkroom` records those
  values into `docs/design-tokens.md`, and if Barlow fails to load the page
  silently falls back to a system sans — the failure mode F2 exists to kill
  ("a bundled face that fails to load is a visible failure, never silently
  papered over by a system font").

Root cause: `fix19/fix19.py` step 2 only runs the strip on files that contain
`system-ui` (`if not before: continue`, `fix19.py:397-400`). The 21 theme
files with no `system-ui` were never stripped, and 20 of them carry these
tails. The manifest's §1.3 wording ("`system-ui` + bare-generic tails
removed from `--font-*` lines") is true only for the 30 files the strip ran
on — it overstates the strip. Verified by re-running the strip function over
the built tree: it is a no-op on 31 files (the 30 stripped + 1 that never
had any tail) and would still change exactly these 20.

Why minor, not blocking: the condition is pre-existing (fix19 did not
introduce it), the SPEC §5 inventory scope was `system-ui` only and fix19
met it (0 `system-ui` in all theme files), and the new checks catch it
downstream — a build using one of these themes records the tail in its Type
list, and STATIC19 flags "a row naming … a bare generic fallback" as an
incomplete build. Fix-up: drop the `if not before: continue` gate so the
strip runs over all 51 theme files, rebuild, re-run verify19 (expect 0 tail
lines; `system-ui` total stays 161, since these files contain none).

### MINOR-2 — `start.mjs` still emits a Google Fonts variable-font `<link>` into the built page's head (OPEN ITEM — determination: shipped-page font path, not dev-time-only)

Determination, with evidence: this is a **shipped-page font path**.

- `skills/design-taste-frontend/scripts/start.mjs:257-288` — `fontLink(t)`
  builds `https://fonts.googleapis.com/css2?...&display=swap`. `axisVal`
  (`:258`) emits `r[0] + '..' + r[1]` ranges, and `e.variable = true`
  (`:268`) whenever the pairing defines a weight range `f.w` — i.e. the URL
  requests VARIABLE axes (`family=…:wght@400..700`-style), the exact
  delivery format F2 bans ("a variable font file is NEVER the shipped
  delivery format").
- `start.mjs:305-307` — `FONT_TAGS` emits `<link rel="preconnect"
  href="https://fonts.googleapis.com">`, `<link rel="preconnect"
  href="https://fonts.gstatic.com" crossorigin>`, and `<link href="${link}"
  rel="stylesheet">`.
- `start.mjs:309-326` — `block()` returns the FONT_TAGS plus the six local
  stylesheet links plus the `:root` block: the built page's `<head>`.
- The skill consumes that block as the built page's head: Taste
  `SKILL.md:206-207` instructs `node …/start.mjs css …`, `:230` says
  "Keep the `:root` block as printed", and `references/layout-v4.md:252`
  says "`:root` block as start.mjs prints it". "As printed" includes the
  Google Fonts `<link>` tags — a runtime CDN variable-font load, not a
  bundled static file.
- Same emitted block, second sub-point: `start.mjs:301` — the mono stack is
  `"JetBrains Mono", ui-monospace, "SFMono-Regular", Menlo, Consolas, monospace`
  — a live system-fallback chain (`ui-monospace` + named system fonts +
  bare `monospace`) that fix19's `stack()` change (`:291`, display/text
  only) did not touch. It is emitted only when `monoOf(t)` applies (tech
  pages or `--mono`).

Why minor, not blocking: the manifest already records this as an open item
("the rule text governs it, the script does not yet enforce it"); F2's own
text anticipates the path ("Where the stack's default font loading serves a
variable font (e.g. next/font), the build instances it to static files
before shipping"); and STATIC19 + the D1 face check catch a build that ships
the CDN variable font as-is (Type-list row naming a variable file is an
incomplete build; a rendered non-bundled face is a finding). The real gap is
procedural: no step tells the builder HOW to do the instancing, and "keep
the block as printed" points the other way — the rule and the procedure
disagree. Fix-up: either have the `css` path emit instancing guidance /
static-file output instead of the CDN link, or add the instancing step to
the Taste step-4a procedure that consumes this block; the mono stack should
be narrowed to the bundled mono face at the same time.

## What was checked and passed

### Fix #19 rules — present at assigned placements, verbatim, x1 each
- **C2_NEW** Taste `skills/design-taste-frontend/SKILL.md:246` (STATIC
  instances, variable file never shipped, no `system-ui` / bare generic
  fallback, `font-synthesis: none`, `text-size-adjust: 100%`). Old C2
  sentence GONE: 0 hits for "body faces name their source (self-hosted or
  link)" in the built tree (the 1 hit for "the closest installed font is a
  failure" is C2_NEW's own wording).
- **F2** Taste `:256`, **F3** `:258`, **F4** `:260`, **D19** `:262` — full
  rule texts as specified (F4 reworded per manifest §2: title "Plain/body
  text uses Tiempos", no attribution clause; see banned-terms section).
  All four sit after the E1 rule, before the step-6 checks.
- **STATIC19** x3 — Taste `:312`, orchestrate `:61`, orch-build-mvp `:57`
  (verbatim, identical in all three).
- **Orchestrate** — F2/F3/F4/D19 after the E1 rule; **D19_ROUTING** `:108`
  ("Each decision carries its fix #19 D19 reason … across all six
  full-experience dimensions … Verify checks … AND that every decision
  carries all six dimension lines"); **D19_REVIEWER** `:203` ("The reviewer
  also checks each UI decision's recorded reason covers all six fix #19 D19
  dimensions … a missing dimension, or a reason covering only
  layout/structure, is a finding, minor at least").
- **ui-ux-pro-max app mirrors** — F2_APP `:95`, F3_APP `:97`, F4_APP `:99`,
  D19_APP `:101`, each x1 with the "(fix #19 F2/F3/F4/D19, app surfaces)"
  titles and the "The full F2/F3/F4/D19 rule lives in
  `design-taste-frontend` step 4a" pointers; **C1 note** `:89` ("On app
  surfaces, the font-identity rules apply as in fix #19 F2/F3/F4 … see the
  F2/F3/F4 app mirrors in this skill"). **orch-build-mvp** D19_APP `:44`.
- **POLISH_F19** polish-pass `SKILL.md:22` (Type-list font-identity fields
  + decision-record six-dimension check, both "consistency only, never a
  verdict", after the fix17 F1/T1 verification).
- **TYPESET_F19** typeset lens `:55` (replaces the system-ui-legitimising
  sentence; old sentence 0 hits for "legitimate default with"); checkbox
  `:74` updated to the static-instances wording. Reads coherently in
  context (lines 48-60: pairing rule + loading rule both consistent with
  F2; the "metric-matched fallback" in rule 10 is a `font-display: swap`
  metric match, not a system-font stack — no contradiction).
- **LF_D19** less-flat-ui `SKILL.md:530` (after the fix17 U1 record note).
- **D19 six dimensions** named in every placement (Motion / Theme / Texture
  / Visuals / Techniques / Colors, plus the `none — <reason>` form) —
  spot-checked in Taste `:262`, orchestrate `:108`/`:203`, ui-ux-pro-max
  `:101`, orch-build-mvp `:44`, polish-pass `:22`, less-flat-ui `:530`.
- Every fix19 rule is a static check / candidate evidence / consistency
  check, never a screen verdict: F2/F3/F4/D19 end "a static check item in
  step 6, never a screen verdict"; STATIC19's header says "all static
  checks, never screen verdicts"; POLISH_F19 says "consistency only, never
  a verdict" twice; the D1 face check is a finding, not a verdict. Distinctiveness
  stays browser-qa's alone (E1 anchor intact — see fix17 section).

### Banned terms — 0, including in the new rule texts
- Tree-wide grep (case-insensitive, excl. `node_modules`) for
  `claude|codex|anthropic|opus|sonnet|haiku|composer-2.5`: 0 hits. No
  "Anthropic"/"Claude" token appears in any fix19 rule text: F4's title is
  "Plain/body text uses Tiempos", the body keeps Tiempos / Klim / paid /
  NOT bundleable / Fraunces stand-in / 1.55 line-height with the
  attribution clause dropped, per manifest §2. (Note: the word "Anthropic"
  does still appear in SPEC.md/MANIFEST.md/fix19.py under `fix19/` — those
  are fix documentation, not built-tree rule text, and the verifier's
  built-tree scan correctly excludes them.)

### Prior anchors — no regression
- **fix15 (43/43), fix17 (59/59), fix18 (72/72)** — all re-run directly by
  this audit, all PASS (verify19 also runs them as subprocesses).
- Canonical variety + theme-match block still verbatim x1 in all 11 files
  (this audit's independent count: 11 files, 11 occurrences of "Every
  element application is recorded").
- **D1** present in Taste / orchestrate / polish-pass / orch-build-mvp
  ("screenshot QA" mentions: Taste 2, orchestrate 3, polish-pass 1,
  orch-build-mvp 2; verify15 covers the rule itself).
- fix #15 R1 Taste `:244`, R4 `:276`, R5 `:246`, C1/C2 `:246`, C3 `:298`
  (unchanged line positions — the F2/F3/F4/D19 appends went after E1
  without disturbing them); sticker exceptions A+B intact (verify17);
  less-flat-ui treatments still exactly 1..23 (verify19).
- **Grok pins unchanged from fix16:** `grok-4.7-high` 52 occurrences,
  `cursor-grok-4.6-high-fast` 100; zero bare `grok-4.6-high-fast`
  (negative lookbehind grep, 0 hits); zero bracket syntax on slugs
  (0 hits) — same counts as audit #57.
- **Counts unchanged:** 166 skills / 72 agents / 123 rules / 87 commands /
  15 hooks (hooks.json declares 15; the `hooks/` directory holds 17 files
  because `adapter.js` + `hooks.json` are not hook entries — same as
  audit #57).

### build.sh integrity
- 23,314 lines, md5 `a8d3d3c6f6d32344d0168c5323d9364b` — matches the recorded
  post-fix19 values. Markers intact: fix15 block `:23147`, fix17 block
  `:23212`, fix19 block `:23267` ("# --- fix19: font identity, forced font
  choice, Tiempos body font, thought-out decisions (F2/F3/F4/D19) ---").
- **fix18 has no build.sh block** — only comment mentions (`:23273`,
  `:23276`, "fix18 made…"). That is manifest deviation 6 (fix18 edited
  staged sources only, per verify18 check 14), not a regression; verify19
  check 10 correctly asserts the fix15 + fix17 + fix19 markers.

### `system-ui` inventory — matches the measured baseline
- Total remaining in the built tree: **161** (independent recount),
  matching manifest §4: 129 demo assets + 12 dev/QA tooling pages + 3
  detectors (sloplint/consistency name the ban — must keep) + 3 reference
  data (`styles.csv`) + 14 rule-text mentions (the fix19 rules themselves
  naming `system-ui` as the banned token: Taste 5, orchestrate 4, typeset
  lens 2, orch-build-mvp 1, polish-pass 1, ui-ux-pro-max 1). `*.md` rule
  files: exactly those 14 mentions, 0 font-stack occurrences.
- 0 `system-ui` in all 30 stripped theme files, in `start.mjs`, in
  `theme.mjs`, and in both `shots.json` files (verify19 + independent grep).

### Fix19's own edits — correctness, not just presence
- **Theme tail-strip, on its scope:** the 30 stripped files' `--font-*`
  lines form valid CSS stacks with named faces only. Sample:
  `sticker.md:28` `--font-display: "Bowlby One SC", "Arial Black";
  --font-body: "Sofia Sans";`, `studio.md:28` `--font-display: "Hedvig
  Letters Serif", Georgia; --font-body: "Geist";` — no empty declarations,
  no orphaned commas, named second faces (Georgia, Impact, Arial Black,
  Arial Narrow, Futura, Iowan Old Style) retained per SPEC §5's Sofia
  precedent. Staged-vs-built theme directories are identical (`diff -rq`,
  no differences). See MINOR-1 for what the strip's scope missed.
- **`start.mjs:291`** — `stack()` now returns `"${f.family}"` plus only
  `, Georgia` on the serif branch: display/text stacks are named-face
  only, as the manifest claims. (The `:301` mono stack was not changed —
  see MINOR-2.)
- **`theme.mjs:470`** — CUSTOM_TOKENS font lines are now `--font-display:
  "FILL ME"; --font-body: "FILL ME"; --font-outlier: var(--font-body);` —
  no system-ui / generic tail, as the manifest claims. The surrounding
  BASE CSS (`body { … font-family: var(--font-body); … }`,
  `h1, h2, h3 { … font-synthesis: none; … }`) is consistent with F2.
- **`shots.json:33` + `shots.example.json:33`** — `"sans": "\"Hanken
  Grotesk\""` alone, as the manifest claims; `template/src/fonts.ts:1,6`
  loads Hanken Grotesk (`loadHanken('normal', { weights: ['400','500',
  '600','700'], subsets: ['latin'] })`), so the named face is the loaded
  face. (The `serif` and `mono` stacks in the same files still carry
  generic tails — see Observations.)
- **Typeset lens replacement** — reads coherently in context (see above).

### Remaining rule text — no other contradiction with F2
- `variable font` in `*.md` rule files outside the fix19 texts: 0 hits.
- `nextjs.csv:24` ("Use variable fonts… Single variable font file") is
  still there — the documented tension from SPEC §5. Not re-flagged: it is
  upstream stack data for next/font, not a design rule, and F2 governs the
  shipped format ("Where the stack's default font loading serves a variable
  font (e.g. next/font), the build instances it to static files before
  shipping"). Same treatment as MINOR-2's conversion burden — the tension
  is real but documented and governed, and the downstream checks fire if a
  build ships the variable file.

## Observations (not findings)

- **`shots.json` serif/mono stacks still carry generic tails** —
  `skills/pitch-deck-video/template/shots.json:34-35` (and
  `shots.example.json:34-35`): `"serif": "\"Instrument Serif\", Georgia,
  serif"`, `"mono": "\"JetBrains Mono\", ui-monospace, monospace"`. The
  manifest scoped the shots.json fix to the `sans` stack only, and the
  video template is not a built web page, so F2's "built pages" language
  does not clearly cover it. Flagging for the coordinator to scope-decide;
  if the /demo render counts as a shipped surface, these two stacks want
  the same treatment the `sans` stack got.
- **Manifest §1.3 wording overstates the strip** (see MINOR-1): "system-ui
  + bare-generic tails removed from `--font-*` lines" should read "removed
  from the `--font-*` lines of the 30 files that contained system-ui".
- **SPEC §1 baseline was wrong, manifest corrected it:** the SPEC's 139
  baseline is stale; the measured baseline is 191 (manifest deviation 1,
  `fix19/inventory.md`). Verify19 asserts against the measured numbers —
  correct behaviour, no finding.

## Not checked
- Live behaviour (no browser run in this audit): whether a cold-start build
  actually instances fonts to static files, whether the D1 face check
  fires on a CDN variable font, and whether the six-dimension D19 record
  check fires in practice — for the dry-run / re-trace, not this tree audit.
- The Campus Eats artifact itself (out of scope; must not be touched) — the
  stale-workspace-tokens caveat (SPEC §1) stands: the workspace
  `design-tokens.md` is v1-era and is NOT evidence of the repair.
- Dry-run #30 / sweep #23 (separate workers).
- `build.sh.before-fix19` backup exists (confirmed present).
