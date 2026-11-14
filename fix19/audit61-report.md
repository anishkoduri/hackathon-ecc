# Audit #61 — fix #19 re-audit after the fix-up round (MINOR-1 / MINOR-2)

**Date:** Nov 11, 2026 (~20:30 CST)
**Auditor:** audit #61 worker (check only — no plugin file edited, build.sh not run,
Campus Eats artifact not touched)
**Built tree:** `~/workspace/hackathon-plugin/hackathon-ecc/`
**Build state:** build.sh 23,314 lines, md5 `a8d3d3c6f6d32344d0168c5323d9364b`
(post-fix19; UNCHANGED by the fix-up, re-verified here). Fix-up rebuilds per
`fix19/MANIFEST.md` §6: builds 1 + 2 exit 0, third build identical tree manifest
(diff 0); changed files vs the pre-fix-up built tree: exactly the 25 fix-up
files (Taste SKILL.md, layout-v4.md, start.mjs, shots.json ×2, 20 theme files).
**Verifiers re-run by this audit:** `fix19/verify19.py` 75/75 PASS;
`fix15/verify15.py` 43/43 PASS; `fix17/verify17.py` 59/59 PASS;
`fix18/verify18.py` 72/72 PASS (each run directly, not only as verify19
subprocesses).

## Verdict: CLEAN — 0 BLOCKING, 0 MINOR

Both audit #60 minors are fixed, verified by re-derivation and by live
execution of the loader (not just by reading the strings): all 51 Hallmark
theme files carry named faces only on every `--font-*` line (0 tail lines,
0 `system-ui`), and `start.mjs` now emits explicit static weights only —
0 `..` ranges across all six pages' `types` output, and the live `css`
blocks confirm it for both a place pairing (Fraunces) and a tech pairing
(mono face). The F2 rule text is unchanged, all prior anchors hold, no
regression was found, and the three left-open items from the fix-up are
judged documented limitations, with reasons, in §4. The shots.json scoping
decision (F2 governs the serif/mono stacks) is sound — agreed, with evidence.

## Findings

None.

## 1. MINOR-1 (audit #60 / sweep #23) — FIXED

All 51 Hallmark theme files' Tokens-block `--font-*` lines carry named
faces only. Verified two ways:

- **Full count (built tree):** re-ran the tail check (same `THEME_TAILS`
  list as `fix19.py`) over all 51 files in
  `hackathon-ecc/skills/design-taste-frontend/references/hallmark/references/themes/`:
  **0 files with a tail line, 0 tail lines, 0 `system-ui`** in any theme file.
- **Sample (all 20 previously-affected files, read in full):** every
  `--font-*` declaration line is named faces only, with no empty
  declarations and no orphaned commas. Examples:
  - `darkroom.md:27` (the audit #60 example): `--font-display: "Sofia Sans Extra Condensed"; --font-body: "Barlow";`
  - `arcade.md:29`: `--font-display: "Bungee", "Impact"; --font-body: "Chivo"; --font-outlier: "Silkscreen";`
  - `hum.md:32-33`: `--font-display: "Chillax"; --font-body: var(--font-display);` / `--font-outlier: "Geist Mono";`
  - `editorial.md:27`: `--font-display: "Bricolage Grotesque"; --font-body: "Source Serif 4", Georgia;`
  - `terminal.md:30`: `--font-display: "Martian Mono"; --font-body: var(--font-display); --font-outlier: var(--font-display);`
  - `sport.md:28-29`: `--font-display: "Saira Condensed"; --font-body: "Albert Sans";` / `--font-outlier: "JetBrains Mono";`
  - `wayfind.md:27`: `--font-display: "Chivo Mono"; --font-body: var(--font-display); --font-outlier: var(--font-body);`
  - `blueprint.md`, `broadside.md`, `dose.md`, `formwork.md`, `halftone.md`,
    `newsprint.md`, `overprint.md`, `pasteup.md`, `piste.md`, `riso.md`,
    `solstice.md`, `terrazzo.md`, `vellum.md` — all likewise named faces
    only (named second faces Georgia / Impact / Arial Narrow retained per
    SPEC §5's Sofia precedent).
- Staged-vs-built theme directories are identical (`diff -rq`, 0 mismatches
  across all 51 files). The manifest §1.3 wording is now accurate: the strip
  covers all 51 files.
- One non-declaration line worth noting, not a tail: `editorial.md:27` also
  carries `font-variation-settings: "opsz" 12;` in a `small, figcaption, th,
  nav, label, .btn, .tag` usage rule — a rendering declaration on a named
  face, not a `--font-*` stack, so it is outside MINOR-1's scope and outside
  the strip's. (It is the same class of residual as §4(a): a variable-axis
  setting that is inert on the prescribed static delivery.)

## 2. MINOR-2 (audit #60) — FIXED

### 2a. `fontLink()` no longer emits variable axis ranges — verified live, not just by string

Built `skills/design-taste-frontend/scripts/start.mjs`:

- `axisVal` / `axisOrder` / `isLower` / `e.variable`: all **0 hits** (deleted).
- `expandWeights` present (`:261-267`); the `f.w` branch stores statics
  (`e.statics.add(x)`, `:281`); the URL builder emits
  `wght@` with a numerically-sorted `;`-joined list only (`:287`).
- **Live check 1 — `types` over all 6 pages** (`node scripts/start.mjs types
  --page place|product|service|software|tech|gaming`, 384 lines):
  **0 `..` ranges**, 225 `wght@` occurrences, all explicit lists, e.g.
  `family=Bricolage+Grotesk:wght@400;500;600&family=Figtree:wght@400;500;600`,
  `family=Geist:wght@400;500;600;700`, `family=Instrument+Sans:wght@400;500;600;700`.
  (The fix-up worker's "128 `..` ranges → 0" claim is consistent with this:
  the pre-fix-up code emitted `r[0] + '..' + r[1]` for every weight range;
  no range survives in any page's output.)
- **Live check 2 — `css` for the Fraunces place pairing**
  (`--page place --palette white-link-blue --type fraunces`):
  link `family=Fraunces:wght@400;500;600&family=Figtree:wght@400;500;600&display=swap`
  — explicit static weights, no `..`; `:root` carries
  `--font-display: "Fraunces", Georgia; --font-text: "Figtree";`.
- **Live check 3 — `css` for a tech pairing**
  (`--page software --palette white-link-blue --type instrument`):
  link `family=Instrument+Sans:wght@400;500;600;700&family=DM+Mono:wght@400;500&display=swap`;
  `:root` carries `--font-mono: "DM Mono";` — the mono stack is a named
  bundled face only, and the loader requests it at explicit weights 400;500
  (matching `DEFAULT_MONO w: [400, 500]`).
- `node --check` on the edited `start.mjs` passes (re-run by this audit's
  live invocations above, which executed the file successfully).

### 2b. Mono stack, carve-outs, instancing step — all present, ×1 each

- Mono stack (`start.mjs:305`): `mono: monoOf(t) ? `"${monoOf(t).family}"` : ''`
  — `ui-monospace`, `SFMono-Regular`, `Menlo`, bare `monospace`: all 0 hits
  in the file.
- Carve-outs (each ×1, exact text as in `fix19_fixup.py`):
  Taste `SKILL.md` (`Keep the `:root` block as printed, except the font
  delivery: …`); `references/layout-v4.md:252` (same carve-out on "keep the
  `:root` block as start.mjs prints it."); `start.mjs:43` (loader header
  comment, same carve-out).
- Instancing step: Taste built `SKILL.md:258`, ×1, immediately after the F2
  rule — the five-step method (download OFL variable font → fontTools
  instancer per weight with opsz baked in and wdth/SOFT/WONK fixed at dealt
  values → subsetter latin + latin-ext → verify no fvar + correct
  usWeightClass → bundle static woff2 + `@font-face` + preloads), ending in
  the static-check sentence, never a screen verdict.
- **F2 rule text unchanged:** `F2_RULE` imported from `fix19/fix19.py`
  counts exactly 1 in built Taste, and `verify19.py` (which imports the same
  constant) passes 75/75 with no update — the fix-up added a procedural step
  after the rule, it did not edit the rule. `fix19.py` itself was not edited
  by the fix-up (its preflight + self-checks assert the F2 anchor).

## 3. shots.json scoping decision — F2 GOVERNS the serif/mono stacks — AGREED

Both `skills/pitch-deck-video/template/shots.json` and
`shots.example.json` parse as valid JSON, and both now read
`"sans": "\"Hanken Grotesk\""`, `"serif": "\"Instrument Serif\""`,
`"mono": "\"JetBrains Mono\""` — faces only, no generic tails.
The decision is sound, for the same reason fix19 already treated the `sans`
stack as in scope (MANIFEST §3 deviation 5): the video template is a shipped
surface. Verified independently:

- `template/src/theme.ts:6`: `export const FONT = shots.theme.fonts;` — the
  stacks flow straight into the render (the manifest's Brand/Captions/Arch/
  Close `fontFamily` claim follows from this export).
- `template/src/fonts.ts`: loads exactly the three named faces with explicit
  weights — Hanken Grotesk 400/500/600/700, Instrument Serif 400,
  JetBrains Mono 400/500 — via `@remotion/google-fonts`. The stacks now name
  exactly the faces that are loaded, so there is no longer a stack/loader
  mismatch on any of the three stacks.
- Leaving serif/mono with system tails while `sans` was fixed on the same
  reasoning would have been an internal contradiction; fixing them the same
  way removes it. No other file in the pitch-deck-video template carries a
  font stack with a generic tail (the `sans`/`serif`/`mono` trio is the
  whole `theme.fonts` object).

## 4. Left-open items from the fix-up — judged

### (a) `start.mjs` still emits `--display-axes` — DOCUMENTED LIMITATION, not a finding

Confirmed live: `css --page place --type fraunces` emits
`--display-axes: 'SOFT' 30, 'WONK' 0;` (start.mjs:322, only when the pairing
defines `ty.axes`). `library/type.json` has exactly **one** pairing with
`display.axes` — `fraunces` (`'SOFT' 30, 'WONK' 0`, w [400,600]) — matching
the manifest's claim. The variable is consumed by
`assets/layout/layout.css:44`:
`h1, h2, h3, .ly-display { … font-variation-settings: var(--display-axes, normal); }`.

Why limitation, not finding: on the prescribed delivery the setting is
inert. A static font file has no SOFT/WONK axes, and per the CSS Fonts
specification a `font-variation-settings` value naming axes the font does
not have is ignored — headings render from the static instances, and the
emitted link no longer requests those axes at all (§2a). The instancing step
also fixes SOFT/WONK at their dealt values when instancing, so the emitted
`'SOFT' 30, 'WONK' 0` is the baked-in value, not a contradiction. The var
only becomes live if a build ships the CDN variable font against the
procedure — which STATIC19 (Type-list row naming a variable file) and the D1
face check (rendered face not a declared bundled face) both catch. Related
residue, same class: the demo HTML files (`assets/layout/hero-place.html:24`,
`hero-split.html:22`, `assets/moments/_demo/in-page*.html:26`) hardcode
`--display-axes: 'SOFT' 70, 'WONK' 0;` — demo assets, out of scope per
SPEC §5, and note the value differs (70 vs the dealt 30), which is demo
copy, not a rule. Removing the var would require a type.json / layout.css
change beyond this fix-up's scope; the honest record is that it is emitted,
inert on static delivery, and downstream-checked.

### (b) `assets/layout/deal.mjs:128` "keep its :root lines as printed" left as-is — DOCUMENTED LIMITATION, not a finding

Confirmed present: `deal.mjs:128` reads
`type: the pairing start.mjs dealt (VI-02); keep its :root lines as printed (headlines 400; 400 to 500 on tech).${axis}` — inside a deal-brief
template string, where `${axis}` (line 118) is the sentence "This hero needs
a face with a wght or wdth axis." for word/editorial heroes.

Why limitation, not finding: this is a demo-asset file (`assets/`, the
demo-only class per SPEC §5 — the same class as the 129 remaining
`system-ui` occurrences that are explicitly out of scope), and the line is
generated deal-brief copy about headline weights, not a delivery instruction
— it never mentions a font link or a CDN, and the weights it names (400;
400–500) are delivered as static instances under the new procedure. The
governing shipping procedure is Taste `SKILL.md` step 4, which now carries
the carve-out (§2b), and `layout-v4.md` likewise. A builder following the
deal brief for weights and the skill for delivery gets the F2-compliant
result. It is, however, the only remaining uncarved "keep as printed" in
the font-delivery sense in the tree (tree-wide grep for "as printed":
the other hits are icon paths, `photos.mjs` `--out` paths, and photo-markup
comments — none font-related), so it is recorded here rather than silently
dropped. Editing it would mean editing demo-asset output copy for a phrase
that does not instruct a delivery; that is a coordinator call, not a defect.

### (c) verify19 check-7's name is stale — DOCUMENTED LIMITATION, not a finding

Confirmed: `fix19/verify19.py:219` names the check
`"system-ui zero in all 30 theme files (Tokens blocks stripped)"`, while the
check itself (lines 215–218) globs **all** `*.md` files in the themes
directory — all 51 — and asserts 0 `system-ui` across them. The name is
stale (30 was the pre-fix-up count); the check is correct and passes. The
manifest already records this as out of scope ("verify19 is updated only
when a rule text changes"), and I agree: renaming a check string is a doc
change, not a rule change, and no verifier behaviour depends on the name.
Recorded for the next verify19 touch, not a finding.

## 5. Prior anchors intact — no regression

- **Verifiers, re-run directly by this audit:** verify15 43/43, verify17
  59/59, verify18 72/72, verify19 75/75 — all PASS.
- **Canonical variety + theme-match block:** verbatim ×1 in all 11 files
  (independent count; md5 as in sweep #23).
- **Grok pins unchanged from fix16:** `grok-4.7-high` 52 occurrences,
  `cursor-grok-4.6-high-fast` 100; zero bare `grok-4.6-high-fast`
  (negative lookbehind grep, 0 hits); zero bracket syntax on slugs
  (0 hits) — same counts as audits #57/#60.
- **Banned terms:** 0 in the built tree (case-insensitive grep for
  `claude|codex|anthropic|opus|sonnet|haiku|composer-2.5`, excl.
  `node_modules`, over skills/agents/commands/rules/hooks/README.md).
- **Counts unchanged:** 166 skills / 72 agents / 123 rules / 87 commands /
  15 hooks.
- **`system-ui` total:** 161 in the built tree (independent recount),
  matching manifest §4 — the fix-up moved none of it (the 20 newly stripped
  theme files contain no `system-ui`; the shots.json serif/mono stacks
  contain none; no fix-up text adds a literal `system-ui` — verify19 pins
  the `*.md` mention count at 14 and passes).
- **build.sh:** 23,314 lines, md5 `a8d3d3c6f6d32344d0168c5323d9364b` —
  unchanged by the fix-up, as claimed.

## 6. Regression check — the fix-up introduced none

- **Staged-vs-built (the 25 fix-up files):** `layout-v4.md`, `start.mjs`,
  `shots.json`, `shots.example.json` — IDENTICAL staged vs built; all 51
  theme files IDENTICAL; Taste `SKILL.md` differs only by the pre-existing
  frontmatter hunk (lines 9–13, the `replace_text("design-taste-frontend", …)`
  "Use ONLY for a full company or landing-page build…" replacement at
  build.sh:606–614 — documented in sweep #23 §11, predates fix19, and the
  fix19-relevant regions match).
- **No rule text changed:** F2/F3/F4/D19/STATIC19 constants are untouched
  (verify19 passes 75/75 with no update; F2_RULE counts 1 in Taste — §2b).
  The fix-up's additions are a procedural step and three carve-outs, all
  outside the rule constants.
- **The two extra carve-outs are in scope and correct:** `layout-v4.md:254`
  (the "Load from Google Fonts with `display=swap`" sentence, same paragraph
  as the `:root` carve-out) and `start.mjs:43` (the loader's own header
  comment) carry the same delivery instruction as the two named `:root`
  lines, so leaving them uncarved would have left the procedure
  contradicting the rule in the same way MINOR-2 did. Both wordings are
  accurate: the link "requests static instances only" (verified live, §2a)
  and "is the generation source only". The layout-v4 sentence's retained
  tail — "A fallback face never shows (`font-load` warns a family that never
  loaded)" — is consistent with F2 (a failed load is a visible failure,
  never silently papered over), not a contradiction.
- **Font loading not broken:** `start.mjs` executes cleanly (live `types`
  and `css` runs above); every emitted link requests only weights that exist
  for the face (Fraunces 400/500/600 from w [400,600]; Geist 400–700;
  mono faces at 400;500). One behaviour change to note, not a regression:
  non-weight axes (wdth/opsz/SOFT/WONK) are now dropped from the link
  entirely — previously a `..` range for them was requested. That is the
  intended F2 trade (the instancing step bakes those axes in at their dealt
  values); a face whose character depends on a non-weight axis at runtime
  (e.g. a `wdth` letters moment) loses that live axis, and the D1 face check
  is the backstop if the rendered result differs.
- **Fix-up script's own honest notes verified:** the script as it now stands
  is the corrected version (its `'..'` self-check is scoped to the
  `fontLink` body, per the manifest's note that `'..'` is legitimate in
  `path.join(here, '..', 'library', …)`); the shots.json trailing-comma
  defect it caught is gone — both files parse as valid JSON (§3). The
  script was not re-run here (read-only audit); its claims were checked
  against the tree and the live loader instead.

## Observations (not findings)

- **Manifest §1.3 is now accurate** (see §1): the strip covers all 51
  files; the audit #60 observation about its wording is closed.
- **SPEC §1 baseline** remains as corrected (191, not 139 — manifest
  deviation 1); the fix-up did not change any inventory number.
- **`--display-axes` in demo HTML vs dealt value:** demo files hardcode
  `'SOFT' 70` while the dealt fraunces pairing is `'SOFT' 30` (§4a). Demo
  copy, not a rule — recorded only so a future reader does not mistake the
  demo value for the dealt one.

## Not checked

- Live behaviour beyond the loader's own output (no browser run in this
  audit): whether a cold-start build actually instances fonts to static
  files, whether the D1 face check fires on a CDN variable font, and
  whether the six-dimension D19 record check fires in practice — for the
  dry-run / re-trace, not this tree audit.
- The Campus Eats artifact itself (out of scope; must not be touched) — the
  stale-workspace-tokens caveat (SPEC §1) stands.
- Dry-run #30 / sweep #24 (separate workers).
- `build.sh` was not rebuilt here (read-only audit); the fix-up's build
  claims (builds 1 + 2 exit 0, third build diff 0, exactly 25 files changed)
  were not independently re-derived beyond the staged-vs-built diffs and the
  unchanged build.sh md5/line count.
