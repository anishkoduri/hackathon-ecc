# Fix #19 — SPEC: font identity, forced font choice, Anthropic body font, thought-out decisions

## 0. Goal

Back-port the Campus Eats font repair (Nov 11 evening) and Anish's two
follow-up directives into the package as enforceable rules, so a future
build cannot ship fonts that render differently per platform, cannot fall
back to a system font, cannot pick a generic font, cannot set body text in
anything but the Anthropic font (or its recorded stand-in), and cannot make
a UI decision without a thought-out, full-experience reason recorded for it.

Gate (verified before writing this SPEC): `fix18/MANIFEST.md` exists;
`build.sh` is 23,276 lines, md5 `5cdd22787dfd56aed0b360e49dae60f2`
(post-fix18). Checker numbers entering fix #19: Audit #59 CLEAN (0/0),
dry-run #29 PASS, sweep #22 CLEAN; verify15 43/43, verify17 59/59,
verify18 72/72. Counts 166 skills / 72 agents / 123 rules / 87 commands /
15 hooks.

## 1. Evidence — the render

Anish opened the Campus Eats cold-start render on his iPhone (looked nice)
and on Windows (looked bad). Root cause found by the artifact repair:

- The body font was a SINGLE VARIABLE font file whose interpolated weights
  render differently under iOS vs Windows, PLUS a system-ui fallback
  (SF Pro on iPhone, Segoe UI on Windows) — so the two platforms literally
  showed different fonts.
- The repair's verified solution: self-hosted, preloaded STATIC font files
  (the same bytes on every platform) — Fraunces static woff2 instances
  (400/500/600/700/800, latin + latin-ext, opsz 24, WONK off), generated
  from the OFL Fraunces variable font with fontTools instancer/subsetter,
  confirmed static (no fvar) with correct usWeightClass; the variable
  Sofia Sans files were deleted; zero remaining 'Sofia' or 'system-ui'
  references; zero generic sans-serif fallbacks; preloads for the four
  first-paint faces; font-synthesis:none; text-size-adjust:100%; inline
  SVG text stacks updated. Display type stays Bowlby One SC.

Anthropic font identity (grounded in web research by the repair):
Claude's reading text is Tiempos (Klim, paid, NOT bundleable); Fraunces
is the recorded free stand-in, set at Claude's 1.55 reading line-height.

Two honest caveats (state them, do not hide them):

- The workspace copy of the Campus Eats artifact
  (`~/workspace/cold-start-render/campus-eats/docs/design-tokens.md`) is
  v1-era and STALE: it still records `--font-body: "Sofia Sans",
  ui-sans-serif, system-ui, sans-serif;` and pre-repair typography lines.
  It does NOT reflect the repair and must not be cited as evidence of the
  repair. The repair evidence is the repair's verified solution (brief
  §1 above), not the workspace file. The dry-run uses the stale file only
  as a NEGATIVE demonstration (§6).
- Baseline counts in the built tree (measured Nov 11, pre-fix19):
  `system-ui` 139 occurrences (nearly all in reference/demo assets under
  `skills/design-taste-frontend/assets/` — demo HTML/CSS, not shipped
  pages — plus one rule-text conflict, see §5); `Sofia` in the font
  catalogues (`skills/ui-ux-pro-max/data/google-fonts.csv`,
  `google-font-licenses.json`), the Hallmark theme files
  (`sticker.md`, `darkroom.md`, `studio.md`, `index.json`), and demo
  assets; `Fraunces` 23 occurrences; `Tiempos` 0. The fix19 verify
  script must inventory `system-ui` by file class (§7) — a blanket
  tree-wide zero is WRONG (demo assets are not shipped pages).

## 2. Rules

### F2 — Fonts render identically on iPhone and web (extends fix #15 C2)

F2_RULE = """**Fonts render identically on iPhone and web — static bundled files only (fix #19 F2 — extends fix #15 C2).** The shipped font files are STATIC instances — one file per weight (e.g. 400/500/600/700/800), generated from a variable font with fontTools instancer/subsetter where the source is variable, with the optical size baked in (opsz) and no fvar table. A variable font file is NEVER the shipped delivery format: its interpolated weights render differently under iOS vs Windows, which is exactly the bug this rule fixes — a variable font may be the generation source, never a shipped file. NO system-ui / system fallback anywhere as a live path: no `system-ui` in any font stack, no bare generic `sans-serif`/`serif` as a live path — the stack names bundled faces only, and a bundled face that fails to load is a visible failure (a finding), never silently papered over by a system font. `font-synthesis: none` (no browser-synthesised bold/italic — the synthesised weights are the ones that diverge) and `text-size-adjust: 100%` (no platform text scaling). Preload the first-paint faces. The D1 screenshot QA (desktop + mobile) confirms the SAME faces render on both widths — compare the rendered faces, not just layout; a rendered face that is not a declared bundled face (a system font, a synthesised weight, a fallback sans) is a finding, the way the v1 audit caught Bowlby falling back to a plain sans. Where the stack's default font loading serves a variable font (e.g. next/font), the build instances it to static files before shipping. Recorded in `docs/design-tokens.md`'s Type list: each face → its static files (weight → file), source, and preloads. A Type-list row naming a variable file, a `system-ui` fallback, a bare generic fallback, or no preload is an incomplete build — a static check item in step 6, never a screen verdict."""

### F3 — Font choice is unique and interesting, forced (extends fix #15 C1, fix #17 F1)

F3_RULE = """**Font choice is unique and interesting — forced, never a default (fix #19 F3 — extends fix #15 C1, fix #17 F1).** No generic/system font as a display or body face. The pairing must be distinctive: a one-off display face with character plus a characterful body face — the pairing itself is a design decision, made THROUGH the design skills (the dealt pairing in Taste step 4a / the ui-ux-pro-max type scale) and recorded in `docs/design-tokens.md`'s Type list with a Source cell naming the exact skill text (fix #17 F1), never inherited from a framework default, a browser default, or a template. A pairing that is a framework default, a system stack, or a template's stock pairing is an incomplete build — a static check item in step 6, never a screen verdict. The display face is self-hosted (bundled static instances + `@font-face`, fix #19 F2); the body face likewise."""

### F4 — Plain/body text uses the Anthropic font

F4_RULE = """**Plain/body text uses the Anthropic font (fix #19 F4).** Body and plain text use Tiempos — the font Claude's reading text is set in (Klim, paid, NOT bundleable). The canonical free stand-in is Fraunces, set at Claude's 1.55 reading line-height. Wherever the stand-in is used, record it explicitly as the stand-in in the Type list (face → 'Fraunces (stand-in for Tiempos)') — never present Fraunces as Tiempos. Tiempos itself is never shipped from this plugin (no paid licence); if the project holds a Tiempos licence, the licensed files replace the stand-in and the record says so. A dealt theme that names a different body face keeps it ONLY as a scoped, recorded exception in `docs/design-tokens.md` with a fix #19 D19 reason (job / considered-and-rejected / theme-fit across the six full-experience dimensions) — the exception is about the FACE, never about the delivery format (fix #19 F2 still binds: static instances, no system fallback). A theme body face delivered as a variable file or with a system fallback is a bug to fix, not an exception to record."""

### D19 — Every UI decision carries a thought-out reason across the FULL experience

D19_RULE = """**Every UI decision carries a thought-out reason across the FULL experience (fix #19 D19).** No silent defaults, no arbitrary picks. Each UI decision run through the skills — font, color, layout, element, treatment, motion, component, spacing — carries an explicit recorded reason in the decision record (`docs/design-tokens.md` / the decision record / `design-system/<project-slug>/MASTER.md` on app surfaces; the run ledger for the smallest flows): (1) what job it serves, (2) what was considered and rejected, (3) how it matches the theme. The reasoning must consider the FULL experience, not just the UI: every decision's recorded reason addresses SIX dimensions, one line each — **Motion** (what moves, what entrance/hover/loop it carries, or `none — <reason>`); **Theme** (how it fits the dealt theme — material, tokens, palette balance, do-nots); **Texture** (the not-flat-UI texture layer — what less-flat-ui treatment it carries, or `none — <reason>`); **Visuals** (imagery, iconography, visual treatment, what it looks like); **Techniques** (the other design techniques brought to bear — element kinds and skill techniques beyond the decision's own kind, e.g. a dealt moment, a diagram, an effect, a type moment, a craft-floor rule); **Colors** (palette tokens used, balance, contrast). A dimension that genuinely does not apply records `none — <reason>` — an explicit none, never a missing line. A decision whose recorded reasoning covers only layout/structure — the UI alone — does NOT satisfy this rule. A UI decision with no recorded reason, a missing dimension, or a layout-only reason is an incomplete build — a static check item in step 6, never a screen verdict. The audit/dry-run loop CHECKS the reasoning is present: the static checks verify every decision-record entry carries all six dimension lines, and the blind reviewer on UI diffs flags a missing dimension as a finding (minor at least). The check verifies the reasoning is PRESENT and addresses the dimensions — the quality of the reasoning itself is browser-qa's and the reviewer's judgment, not a static check."""

The decision record is the Type list, the Unique list, the Motion list,
and the element applications in `docs/design-tokens.md` (and the MASTER.md
equivalents on app surfaces). D19 governs all of them: every entry in
those lists carries the six dimension lines (or the entry IS the decision
recorded with its reason). The motion skills need no direct edit — their
Motion-list entries are covered by this record-level check.

### Fix #19 static checks (consolidated paragraph, mirrors fix #17 STATIC_CHECKS)

STATIC19 = """**Fix #19 static checks (all static checks, never screen verdicts).** (F2) The Type list names, per face, its static files (weight → file) with source and preloads; a row naming a variable file, a `system-ui` fallback, a bare generic fallback, or no preload is an incomplete build. (F3) The pairing is recorded with a Source cell naming the exact skill text; a pairing that is a framework default, a system stack, or a template's stock pairing is an incomplete build. (F4) Body/plain text is Tiempos or the recorded stand-in 'Fraunces (stand-in for Tiempos)' at 1.55 line-height; a theme body face kept without a scoped, recorded exception is an incomplete build. (D1 face check) The D1 screenshot pass (desktop + mobile) confirms the same faces render on both widths — a rendered face that is not a declared bundled face (a system font, a synthesised weight, a fallback sans) is a finding. (D19) Every decision-record entry carries all six dimension lines (Motion / Theme / Texture / Visuals / Techniques / Colors), each a reason or an explicit `none — <reason>`; an entry missing a dimension, or a reason covering only layout/structure, is an incomplete build."""

## 3. Placement (fix #15 / fix #17 pattern)

The canonical variety + theme-match block is NOT modified (verify15.py's
verbatim check must keep passing — the block stays verbatim ×1 in all 11
files). The fix19 rules are placed as new bold rules adjacent to it in the
files where they apply, mirroring fix17's placement. One source of truth;
build.sh patches where the built tree needs them.

### Staged sources (edited directly; build.sh copies them verbatim)

| # | File | Change |
|---|---|---|
| 1 | `new-skills/design-taste-frontend/SKILL.md` (step 4a) | C2 REPLACEMENT: replace the C2 sentence in the giant step-4a line (old: "Display faces are self-hosted (bundled woff2 + `@font-face` in the built page) whenever the face's character matters — the closest installed font is a failure, not a fallback; body faces name their source (self-hosted or link) and fallback stack in `docs/design-tokens.md` (fix #15 C2).") with C2_NEW (below). |
| 2 | Taste step 4a | Append F2 + F3 + F4 + D19 as four new bold lines after the E1 rule. Anchor (count==1 in this file): "Distinctiveness itself is browser-qa's verdict alone." |
| 3 | Taste step 6 | Append STATIC19 as a new paragraph after the fix17 static-checks paragraph. Anchor: the STATIC_CHECKS ending "...or the failure recorded as a finding; a floor/ban break blocks." (verify count==1 in this file; it must NOT match the step-4a E1 ending, which is followed by "Distinctiveness itself…"). |
| 4 | `new-skills/orchestrate/SKILL.md` (design-package rule) | Append F2 + F3 + F4 + D19 after the E1 rule. Anchor: "Distinctiveness itself is browser-qa's verdict alone." (count==1 in this file). |
| 5 | orchestrate routing line (:100) | REPLACEMENT: extend "Record each decision (direction, components used, tokens) in `docs/design-tokens.md` / the decision record, and Verify checks the record exists and matches what was built." with the D19 reason requirement (D19_ROUTING, below). |
| 6 | orchestrate blind-reviewer check (:195) | REPLACEMENT: extend "a missing record is a finding, minor at least." with the D19 dimension check (D19_REVIEWER, below). |
| 7 | orchestrate Verify 5a | Append STATIC19 after the fix17 static-checks paragraph. Anchor: "a floor/ban break blocks.\n   - **5b. Final polish**". |
| 8 | `round2-skills/polish-pass/SKILL.md` (harmony) | Append POLISH_F19 (below) after the fix17 F1/T1 verification. Anchor: "It also verifies the T1 fill ratios recorded per Type-list row (glyph box ≥ 60% of the container's inner size) — consistency only, never a verdict." |
| 9 | `round2-skills/polish-pass/reference/lenses/typeset.md` | REPLACEMENT (conflict — see §5): replace the system-ui-legitimising sentence (line ~5) with TYPESET_F19 (below); update the variable-font checkbox (below). |
| 10 | `~/workspace/cursor-skills/less-flat-ui/SKILL.md` (record section) | Append LF_D19 (below) after the fix17 U1 record note. Anchor: "Handmade surface treatments (tape, perforation, washi, hand-drawn ink marks) record the same way and count toward the two-distinct-kinds check." |

C2_NEW (replaces the C2 sentence in Taste step 4a — F2 folded into C2's home):
"Display faces are self-hosted as STATIC instances (one bundled woff2 file per weight + `@font-face` in the built page) whenever the face's character matters — a variable font file is never the shipped format, and the closest installed font is a failure, not a fallback; body faces are likewise static instances, and name their source (self-hosted static files + preloads) in `docs/design-tokens.md` (fix #19 F2, extending fix #15 C2). No `system-ui` or bare generic fallback anywhere as a live path; `font-synthesis: none` and `text-size-adjust: 100%`."

D19_ROUTING (orchestrate :100, appended to the routing sentence):
" Each decision carries its fix #19 D19 reason — job served, considered-and-rejected, theme-fit — across all six full-experience dimensions (Motion / Theme / Texture / Visuals / Techniques / Colors), recorded in the decision record; Verify checks the record exists, matches what was built, AND that every decision carries all six dimension lines."

D19_REVIEWER (orchestrate :195, appended to the reviewer sentence):
" The reviewer also checks each UI decision's recorded reason covers all six fix #19 D19 dimensions (Motion / Theme / Texture / Visuals / Techniques / Colors) — a missing dimension, or a reason covering only layout/structure, is a finding, minor at least."

POLISH_F19 (polish-pass harmony append):
" The harmony check also verifies the Type list's font-identity fields (fix #19 F2): each face names its static files (weight → file) with source and preloads, and no row names a variable file, a `system-ui` fallback, or a bare generic fallback — a row that does is a harmony divergence, recorded as candidate evidence, never a verdict. It also verifies the decision-record reasons (fix #19 D19): every decision-record entry carries all six dimension lines (Motion / Theme / Texture / Visuals / Techniques / Colors), each a reason or an explicit `none — <reason>` — consistency only, never a verdict."

TYPESET_F19 (typeset lens replacement for the system-ui sentence):
"The system font stack (`system-ui`) is NOT a legitimate live path for a built page (fix #19 F2): a system font is a failure, not a fallback — the stack names bundled static faces only. A custom face needs a reason (brand voice, a job system fonts can't do); shipped files are static instances (one per weight, opsz baked in) — a variable font is the generation source only, never a shipped file. Set `font-optical-sizing: auto` on the static instances where the face ships an opsz axis."

TYPESET_CHECKBOX (typeset lens checkbox update):
Old: "- [ ] A custom typeface has a stated reason; variable fonts use `font-optical-sizing: auto`."
New: "- [ ] A custom typeface has a stated reason; shipped font files are static instances (one per weight, opsz baked in) — no variable file is shipped, no `system-ui` fallback (fix #19 F2)."

LF_D19 (less-flat-ui record append):
" Treatment choices are UI decisions under fix #19 D19: each recorded treatment carries the six dimension lines (Motion / Theme / Texture / Visuals / Techniques / Colors), each a reason or an explicit `none — <reason>`; a treatment recorded with only a layout/structure reason does not satisfy the rule."

### build.sh patch block (upstream, no staged source)

| # | File (built) | Change |
|---|---|---|
| 11 | `skills/ui-ux-pro-max/SKILL.md` | Append F2_APP + F3_APP + F4_APP + D19_APP (app mirrors, below) after the anti-generic bar (fix17 anchor). Extend the C1 sentence with the F2/F3/F4 app note (anchor: the C1 sentence fix17 used). |
| 12 | `skills/orch-build-mvp/SKILL.md` | Append D19_APP after the E1 rule in step 4 (anchor: the E1 ending in that file); append STATIC19 in step 6 after the fix17 static-checks paragraph (anchor: the STATIC_CHECKS ending in that file). |

F2_APP / F3_APP / F4_APP / D19_APP (app mirrors — same rules, app homes
`design-system/<project-slug>/MASTER.md` instead of `docs/design-tokens.md`):

F2_APP = """**Fonts render identically on iPhone and web — static bundled files only (fix #19 F2, app surfaces).** App surfaces ship static font instances only (one file per weight); a variable font file is never the shipped format; no `system-ui` or bare generic fallback as a live path; `font-synthesis: none`, `text-size-adjust: 100%`; preload the first-paint faces. The D1 screenshot pass (desktop + mobile) confirms the same faces render on both widths. Recorded in `design-system/<project-slug>/MASTER.md` (face → static files, source, preloads). The full F2 rule lives in `design-taste-frontend` step 4a."""

F3_APP = """**Font choice is unique and interesting — forced (fix #19 F3, app surfaces).** No generic/system font as a display or body face on app surfaces; the pairing is distinctive, made through this skill's type scale, and recorded in MASTER.md with a Source cell. A framework-default, system-stack, or template-stock pairing is an incomplete build. The full F3 rule lives in `design-taste-frontend` step 4a."""

F4_APP = """**Plain/body text uses the Anthropic font (fix #19 F4, app surfaces).** Body and plain text use Tiempos, or the recorded stand-in 'Fraunces (stand-in for Tiempos)' at 1.55 line-height; a theme body face kept without a scoped, recorded exception is an incomplete build. The full F4 rule lives in `design-taste-frontend` step 4a."""

D19_APP = """**Every UI decision carries a thought-out reason across the FULL experience (fix #19 D19, app surfaces).** Each app-surface UI decision carries its recorded reason in MASTER.md — job served, considered-and-rejected, theme-fit — across all six dimensions (Motion / Theme / Texture / Visuals / Techniques / Colors), each a reason or an explicit `none — <reason>`; a layout-only reason does not satisfy the rule. The full D19 rule lives in `design-taste-frontend` step 4a."""

## 4. What the canonical block does NOT get

The canonical variety + theme-match block stays verbatim ×1 in all 11
files (verify15.py must keep passing 43/43). Do not append the fix19
rules INTO the block. The motion-* skills, make-interfaces-feel-better,
and hallmark-floor.md get no direct fix19 edit: their entries are covered
by the record-level D19 check (the decision record comprises the Type
list, Unique list, Motion list, and element applications), and they do
not decide fonts. If the audit finds a motion skill deciding a font, that
is a finding for the audit, not a new edit in this fix.

## 5. Conflicts resolved in this SPEC

- **typeset.md:5 legitimises system-ui.** The polish-pass typeset lens
  says "The system font stack (`system-ui`) is a legitimate default with
  good optical sizing…" — that DIRECTLY contradicts F2. Fix19 REPLACES
  that sentence (TYPESET_F19, placement #9). The lens's variable-font
  checkbox is updated the same way.
- **nextjs.csv recommends variable fonts.** `skills/ui-ux-pro-max/data/
  stacks/nextjs.csv:24` ("Use variable fonts… Single variable font file")
  is upstream stack data for next/font, not a design rule. NOT edited.
  F2 governs the shipped format: where the stack's default serves a
  variable font, the build instances it to static files before shipping
  (stated in F2_RULE). Recorded as a documented tension in the manifest,
  not a defect.
- **Font catalogues name Sofia.** `skills/ui-ux-pro-max/data/google-fonts.csv`,
  `google-font-licenses.json` list Sofia Sans as an available font, and
  the Hallmark theme files (`sticker.md`, `darkroom.md`, `studio.md`,
  `index.json`) name it in their type voice. NOT edited: catalogues and
  theme voices are not delivery instructions. F4's exception mechanism
  governs per-build body-face choices; F2 governs delivery. The
  `sticker.md` Sofia body voice stays — a build using it records the
  scoped exception with a D19 reason, or (as the Campus Eats repair did)
  replaces it with Fraunces.
- **Demo assets contain system-ui.** The 139 `system-ui` occurrences are
  nearly all in reference/demo assets (`skills/design-taste-frontend/assets/`
  — demo HTML/CSS). Those are not shipped pages. The verify script
  inventories `system-ui` by file class (§7); the rule bans it as a live
  font path in BUILT PAGES. If the inventory finds a template that ships
  into built pages carrying a system-ui font stack, that template is in
  scope for this fix (replace the stack with the bundled faces) and the
  manifest records it.

## 6. Dry-run — dry-run #30

The dry-run is a font-identity + decision-record check, not an element
recount. PASS requires all of:

1. **Rule presence:** verify19.py passes (see §7).
2. **Criteria coverage:** every failure-mode token from the repair —
   variable font file as shipped format, `system-ui` in the stack, bare
   generic fallback as a live path, synthesised weight, missing preload,
   missing `font-synthesis: none` — is named as a finding trigger in the
   STATIC19 / D1-face-check text.
3. **Repair compliance (repair-reported, not re-verified):** the repaired
   Campus Eats artifact complies with F2/F3/F4 per the repair's verified
   solution (§1). The workspace tokens file is v1-era/stale and is NOT
   evidence of the repair — the report says so explicitly.
4. **Negative demonstration (font):** the v1 tokens file's font setup
   (single variable Sofia file + `system-ui` fallback, line 29 of the
   workspace `design-tokens.md`) FAILS the F2 criteria — proving the
   check fires on exactly the bug that was found.
5. **Negative demonstration (decision):** the v1 tokens file's decisions
   (typography lines 44–46, colours, layout — stated choices with NO
   recorded reason) FAIL the D19 check; and a fixture entry with a
   layout-only reason ("chosen for a clean grid") FAILS the six-dimension
   check — proving the check fires on a missing dimension and on a
   layout-only reason.
6. **Criteria coverage (D19):** all six dimensions (Motion / Theme /
   Texture / Visuals / Techniques / Colors) are named in the D19 check
   text, and the `none — <reason>` form is named as the only valid
   non-application.

The dry-run report (`fix19/dryrun30-report.md`) records the stale-workspace
caveat and the repair-reported status explicitly. No count target: the
re-trace is the check above, not an element recount.

## 7. Verify script — fix19/verify19.py

Follows the fix15/verify15.py and fix17/verify17.py pattern (read-only,
against the BUILT tree; imports rule constants from fix15, fix17, fix18,
fix19). Checks:

1. F2/F3/F4/D19 anchors present in Taste (built), ui-ux-pro-max (built),
   orchestrate (built).
2. C2_NEW present in Taste + the F2/F3/F4 app note in ui-ux-pro-max.
3. STATIC19 present ×3 (Taste step 6, orchestrate Verify 5a,
   orch-build-mvp step 6).
4. POLISH_F19 present in polish-pass; TYPESET_F19 present and the old
   system-ui-legitimising sentence GONE from the typeset lens;
   LF_D19 present in less-flat-ui.
5. D19_ROUTING + D19_REVIEWER present in orchestrate.
6. Canonical block still verbatim ×1 in all 11 files; D1 rule still
   present in Taste/orchestrate/polish-pass/orch-build-mvp.
7. `system-ui` inventory by file class: zero in built-tree `*.md` rule
   files (SKILL.md, references/*.md, lenses); the assets/ occurrences
   recorded with their baseline count (139 at fix19 start, minus any
   template fixed under §5) and classed as reference/demo-only — with an
   explicit fail if any inventoried occurrence sits in a template that
   ships into built pages.
8. Counts unchanged post-fix18: 166/72/123/87/15.
9. No banned terms (fix #16 scrub) in the built skill tree (excl.
   node_modules).
10. build.sh is the post-fix19 file (lines + recorded md5) and still
    contains the fix15 + fix17 + fix18 + fix19 blocks intact.
11. verify15.py 43/43, verify17.py 59/59, verify18.py 72/72 (run as
    subprocesses, exit 0 required).

## 8. Checkers

- Audit #60, dry-run #30, sweep #23 (following fix #18's #59 / #29 / #22).
- Build twice (exit 0, diff 0) before the checkers; the fix-up round
  pattern from fix #17/#18 applies (re-audit + re-sweep after any fix-up;
  the bound holds: a bound-holding diff triggers no re-run).
- Backup: `build.sh.before-fix19` (first pre-fix19 copy, kept).

## 9. Untouched / non-goals

- Fix #16 Grok pins and the Claude/Codex scrub (banned terms stay 0).
- Fix #15 anchors (43/43), fix #17 anchors (59/59), fix #18 anchors
  (72/72).
- The 11-file canonical block (verbatim).
- The Campus Eats artifact (read-only reference; do not touch).
- `fix11/fix11-stage.py` (never re-run).
- No commit, no bundle, no GitHub touch.
- No new inventory: no new less-flat-ui catalogue entries, no new
  Hallmark themes, no new font catalogue entries. Fraunces and Tiempos
  are named in rule text, not added as catalogue items.
