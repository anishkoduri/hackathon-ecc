# Dry-run #30 — Fix #19 font-identity + decision-record check

- **Date:** 2026-11-11, evening CST. Worker: dry-run worker (fix #19), check-only.
- **Scope kept:** no plugin file edited, `build.sh` not run, Campus Eats artifact not touched (read-only). One file written: this report.
- **What this dry-run is:** a font-identity + decision-record check, NOT an element recount (SPEC §6). No count target; the re-trace is the six checks below.
- **Verdict: PASS.** All six SPEC §6 items pass (see §1–§6).

## 0. Source limitations — read this first

1. **The workspace Campus Eats artifact is v1-era and STALE.** `~/workspace/cold-start-render/campus-eats/docs/design-tokens.md` still records `--font-body: "Sofia Sans", ui-sans-serif, system-ui, sans-serif;` and pre-repair typography lines. It does NOT reflect the Nov 11 evening font repair. Per SPEC §1, it is used in this dry-run ONLY as a NEGATIVE demonstration (§4, §5); it must not be cited as evidence of the repair. There is no `index.html`, no assets directory, no built CSS in this workspace to inspect the repaired artifact.
2. **Repair compliance (§3) is REPAIR-REPORTED, NOT re-verified.** The statement that the repaired artifact complies with F2/F3/F4 rests on the repair's verified solution as recorded in SPEC §1, not on any source this worker could inspect. **This worker did NOT re-verify the repair from this VM — the live artifact source does not exist in this workspace.** If the parent wants independent verification, it needs the live repaired artifact source.
3. The built-tree evidence (§1, §2, §6) IS independently verified: greps and `verify19.py` were run against `~/workspace/hackathon-plugin/hackathon-ecc/skills/` this session.

## 1. Rule presence — verify19.py re-run by this worker: PASS (75/75)

Re-ran `python3 fix19/verify19.py` from `~/workspace/hackathon-plugin/` this session (exit 0). Full output tail confirms, among others:

- `PASS system-ui zero in all 30 theme files (Tokens blocks stripped)`
- `PASS system-ui zero in start.mjs (stack fallback)` / `old start.mjs stack GONE`
- `PASS system-ui zero in theme.mjs CUSTOM_TOKENS` / `old theme.mjs font line GONE`
- `PASS system-ui zero in pitch-deck-video shots.json` / `shots.example.json`
- `PASS assets/ demo occurrences recorded at the 129 baseline`
- `PASS dev/QA tooling occurrences recorded at 12`
- `PASS detector occurrences kept at 3 (sloplint/consistency name the ban)`
- `PASS reference-data occurrences recorded at 3 (styles.csv)`
- `PASS *.md rule-text mentions of system-ui number exactly 14`
- `PASS total remaining system-ui is 161 (129 + 12 + 3 + 3 + 14 rule-text mentions)`
- `PASS less-flat-ui treatments still number 1..23 exactly`
- `PASS counts 166/72/123/87/15 (unchanged)`
- `PASS banned terms 0 in built tree (skills/agents/commands/rules/hooks/README)`
- `PASS build.sh is 23314 lines, md5 a8d3d3c6f6d32344d0168c5323d9364b (post-fix19)`
- `PASS build.sh contains the fix19 block marker` / `still contains the fix17 block marker` / `still contains the fix15 block marker`
- `PASS fix15 verifier still passes (43/43 checks pass)` / `fix17 verifier still passes (59/59 checks pass)` / `fix18 verifier still passes (72/72 checks pass)`

Final line: **75/75 checks pass.**

Note the two documented deviations from SPEC §7, both recorded in `fix19/MANIFEST.md` §3 and accepted by the verifier rather than hidden: (a) the SPEC §1 baseline of 139 `system-ui` occurrences is wrong — the measured pre-fix19 baseline is **191 in 121 files** (see `fix19/inventory.md`); (b) SPEC §7 check 7 ("zero in built-tree `*.md` rule files") cannot be literal, because the fix19 rule texts themselves name `system-ui` as the banned token — verify19 asserts zero AFTER subtracting the placed rule texts (14 rule-text mentions, as asserted above). The theme files are a literal zero.

**Item 1: PASS.**

## 2. Criteria coverage (font) — every failure-mode token named as a finding trigger: PASS

The STATIC19 paragraph and the D1 face check are present verbatim ×3 in the built tree — `design-taste-frontend/SKILL.md:312`, `orchestrate/SKILL.md:61`, `orch-build-mvp/SKILL.md:57`. The full paragraph (quoted from `design-taste-frontend/SKILL.md:312`):

> "**Fix #19 static checks (all static checks, never screen verdicts).** (F2) The Type list names, per face, its static files (weight → file) with source and preloads; a row naming a variable file, a `system-ui` fallback, a bare generic fallback, or no preload is an incomplete build. (F3) The pairing is recorded with a Source cell naming the exact skill text; a pairing that is a framework default, a system stack, or a template's stock pairing is an incomplete build. (F4) Body/plain text is Tiempos or the recorded stand-in 'Fraunces (stand-in for Tiempos)' at 1.55 line-height; a theme body face kept without a scoped, recorded exception is an incomplete build. (D1 face check) The D1 screenshot pass (desktop + mobile) confirms the same faces render on both widths — a rendered face that is not a declared bundled face (a system font, a synthesised weight, a fallback sans) is a finding. (D19) Every decision-record entry carries all six dimension lines (Motion / Theme / Texture / Visuals / Techniques / Colors), each a reason or an explicit `none — <reason>`; an entry missing a dimension, or a reason covering only layout/structure, is an incomplete build."

Token-by-token coverage against the STATIC19 paragraph, with the F2 rule text (`design-taste-frontend/SKILL.md:256`, identical in `orchestrate/SKILL.md:96`) as the co-located trigger text:

| # | Failure-mode token (from the repair) | Covered? | Covering text (built tree) |
|---|---|---|---|
| 2a | Variable font file as shipped format | YES | STATIC19 (all three files): "a row naming a variable file … is an incomplete build". F2 rule, `design-taste-frontend/SKILL.md:256`: "A variable font file is NEVER the shipped delivery format" and "A Type-list row naming a variable file … is an incomplete build". |
| 2b | `system-ui` in the stack | YES | STATIC19: "a row naming … a `system-ui` fallback … is an incomplete build". F2 rule, same lines: "no `system-ui` in any font stack". |
| 2c | Bare generic fallback as a live path | YES | STATIC19: "a row naming … a bare generic fallback … is an incomplete build". F2 rule: "no bare generic `sans-serif`/`serif` as a live path". |
| 2d | Synthesised weight | YES | STATIC19 (D1 face check): "a rendered face that is not a declared bundled face (a system font, a synthesised weight, a fallback sans) is a finding". F2 rule: "`font-synthesis: none` (no browser-synthesised bold/italic — the synthesised weights are the ones that diverge)". |
| 2e | Missing preload | YES | STATIC19: "a row naming … no preload is an incomplete build". F2 rule: "Preload the first-paint faces" and "each face → its static files (weight → file), source, and preloads". |
| 2f | Missing `font-synthesis: none` | YES | F2 rule, `design-taste-frontend/SKILL.md:256`: "`font-synthesis: none` (no browser-synthesised bold/italic — the synthesised weights are the ones that diverge)". C2_NEW, `design-taste-frontend/SKILL.md:246`: "No `system-ui` or bare generic fallback anywhere as a live path; `font-synthesis: none` and `text-size-adjust: 100%`." The D1 face check fires on the consequence (a synthesised weight rendered on screen is a finding, token 2d). |

One honest gap in coverage, noted rather than hidden: the STATIC19 paragraph itself does not literally spell out "`font-synthesis: none`" — the token is named in the co-located F2 rule text (step 4a, same skill file, two lines up in Taste: line 256 vs line 312) and its observable consequence (a synthesised weight) IS named in the D1 face check inside STATIC19 itself. The check therefore fires on the bug through the D1 clause; the rule text supplies the literal prescription. This is coverage by the check text as a whole, not by the STATIC19 paragraph alone — recorded here so the parent can decide whether the literal string belongs in STATIC19 too.

**Item 2: PASS** (6/6 tokens named as finding triggers in the STATIC19 / D1-face-check / F2 text, with the 2f note above).

## 3. Repair compliance (F2/F3/F4) — REPAIR-REPORTED, NOT re-verified: PASS as reported

**Status, stated explicitly: this is the repair's verified solution as recorded in SPEC §1. This worker did NOT re-verify it from this VM — the live artifact source does not exist in this workspace (see §0).** What SPEC §1 records as the repair's verified solution:

- Self-hosted, preloaded STATIC font files — Fraunces static woff2 instances (400/500/600/700/800, latin + latin-ext, opsz 24, WONK off), generated from the OFL Fraunces variable font with fontTools instancer/subsetter, confirmed static (no fvar) with correct usWeightClass.
- The variable Sofia Sans files were deleted.
- Zero remaining 'Sofia' or 'system-ui' references; zero generic sans-serif fallbacks.
- Preloads for the four first-paint faces; `font-synthesis: none`; `text-size-adjust: 100%`; inline SVG text stacks updated.
- Display type stays Bowlby One SC.

Compliance of that reported solution against the fix19 rules:

| Rule | Reported repair fact | Complies? |
|---|---|---|
| F2 — static bundled files only; no `system-ui`/bare-generic live path; `font-synthesis: none`; preloads; same faces on both widths | Static Fraunces woff2 instances (no fvar), variable Sofia files deleted, zero remaining 'Sofia'/'system-ui' references, zero generic sans fallbacks, four first-paint preloads, `font-synthesis: none`, `text-size-adjust: 100%` | **YES, as reported.** Every F2 element has a matching reported repair fact. The same-faces-on-both-widths confirmation is the D1 pass the repair performed (iPhone vs Windows), per SPEC §1's "looked nice on iPhone / looked bad on Windows" before-and-after. |
| F3 — unique/interesting forced pairing, no generic/system face | Display stays Bowlby One SC (a one-off display face with character) + Fraunces body (a characterful body face); no generic/system face remains in the stack (zero 'system-ui'/generic fallbacks) | **YES, as reported.** The pairing is distinctive and contains no generic/system face. Caveat: the repair record does not state the pairing's Source cell (which skill text dealt it); F3's recording requirement is a build-record matter, not a repair fact — the parent should not read this as evidence the record exists. |
| F4 — body text is Tiempos or the recorded stand-in Fraunces at 1.55 line-height | Body is Fraunces, the recorded free stand-in for Tiempos (Klim, paid, not bundleable), set at the 1.55 reading line-height per SPEC §1 | **YES, as reported.** |

**Item 3: PASS as repair-reported.** The compliance claim depends entirely on the repair's own verification; no independent check was possible from this VM.

## 4. Negative demonstration (font) — the stale v1 tokens file FAILS F2: PASS

The workspace file `~/workspace/cold-start-render/campus-eats/docs/design-tokens.md` is v1-era (SPEC §1 caveat). Its font setup, line 29 (inside the `:root` Tokens block):

> `--font-display: "Bowlby One SC", "Arial Black", sans-serif; --font-body: "Sofia Sans", ui-sans-serif, system-ui, sans-serif;`

Evaluated against the F2 criteria (F2 rule, `design-taste-frontend/SKILL.md:256`):

| F2 criterion | Tokens-file fact | Result |
|---|---|---|
| Static instances, one file per weight; no variable file shipped | Line 29 names a single face, "Sofia Sans", with **no static weight→file rows anywhere in the file**. A grep of the whole file for `preload`, `font-synthesis`, `woff2`, `static`, `variable`, `fvar` returns **zero matches**. SPEC §1 records the v1 body font as "a SINGLE VARIABLE font file" — the file records the face name only, which is exactly the under-specified form the F2 Type-list requirement forbids. | **FAIL** — a Type-list row naming a variable file (here: a single face with no static instances) is an incomplete build. |
| No `system-ui` in any font stack | Line 29: `… system-ui, sans-serif` — `system-ui` is literally in the body stack. | **FAIL** — quoted directly. |
| No bare generic fallback as a live path | Line 29 ends the body stack with a bare `sans-serif` (and the display stack with a bare `sans-serif` too); the body stack also carries `ui-sans-serif`, another generic. | **FAIL** — quoted directly ("a bare generic fallback" is a STATIC19 trigger). |
| `font-synthesis: none` | No `font-synthesis` anywhere in the file (grep: zero matches). | **FAIL** — the rule's prescription is entirely absent. |
| Preload the first-paint faces | No `preload` anywhere in the file (grep: zero matches). | **FAIL** — STATIC19: "a row naming … no preload is an incomplete build". |
| Same faces on both widths (D1 face check) | The stack as written *guarantees* divergence: `system-ui` resolves to SF Pro on iPhone and Segoe UI on Windows — two different rendered faces from one stack. That is the exact bug the D1 face check exists to catch ("a rendered face that is not a declared bundled face … is a finding"). | **FAIL** — the stack's live path is a system font on both platforms. |

Additional F4 note (not required for the F2 demonstration, but on the record): the file's body line-height is 1.5 (line 45: "Sofia Sans 400/600 body, line-height 1.5"), not the F4-required 1.55, and the body face is Sofia Sans, not Tiempos or its recorded stand-in Fraunces — so the same file would fail F4 too. That is consistent with it being pre-repair.

**Item 4: PASS** — the stale file fails F2 on at least five distinct criteria, including the exact bug found (single variable file + `system-ui` fallback). The check fires on exactly the failure it was built for.

## 5. Negative demonstration (decision) — the v1 decisions FAIL D19: PASS

### 5a. The v1 tokens file's decisions carry no recorded reason

The "Frozen system (Taste step 4a)" section of the same stale file records decisions as bare stated choices, with no reason anywhere. Grep of the whole file for `reason`, `because`, `job it serves` returns **zero matches**. Examples (quoted):

- **Typography, lines 44–46:** "Typography: Bowlby One SC 400 capitals only, h1 max 4.5rem, section heads 3.25rem, line-height 1.02; Sofia Sans 400/600 body, line-height 1.5, tabular-nums; labels Sofia Sans 700, sentence case, muted." — the faces, sizes, and weights are stated; there is no (1) job served, no (2) considered-and-rejected, no (3) theme-fit, and no six-dimension lines.
- **Colour / semantic tokens, lines 47–49:** "--color-accent (pink) = the primary action + prices; --color-accent-2 (lime) = tags, counts, highlights, growth; --color-ink = type, rules, shadows; --color-paper = ground; --color-muted = secondary text on paper. No raw hex in components." — token meanings stated, no reason recorded.
- **Spacing/layout, lines 49–51:** "one section per screen; equal left/right edges on one .wrap; hero alone on screen one; Bento grid for facts; radius-card 18px, photos 22px, pills on controls/tags; dashed --rule-bar dividers." — layout choices stated, no reason recorded.
- **Motion, lines 63–66:** "hero enters once on load; hover lifts a clickable raised surface 2px and turns it a degree; press pushes it onto its shadow; one authored moment (letters-assemble on the ink-band statement); nothing on scroll otherwise; reduced motion rests everything." — motion stated, no reason recorded.

Against the D19 rule (`design-taste-frontend/SKILL.md:262`): "A UI decision with no recorded reason, a missing dimension, or a layout-only reason is an incomplete build." Each of these entries has **no recorded reason at all** — they fail D19 before the dimension check even starts.

**5a: the v1 decisions FAIL D19 (no recorded reason).**

### 5b. Fixture: a layout-only reason fails the six-dimension check

Constructed fixture entry (per the task brief — a colour decision reasoned only as "chosen for a clean grid"):

> **Decision:** --color-accent (pink) = primary action + prices. **Reason recorded:** "chosen for a clean grid."

Evaluated against the six dimensions the D19 rule requires, one line each (`design-taste-frontend/SKILL.md:262`):

| Dimension | Present in the fixture reason? | Verdict |
|---|---|---|
| **Motion** (what moves, what entrance/hover/loop it carries, or `none — <reason>`) | Absent — the reason says nothing about motion, and does not record `none — <reason>`. | **MISSING** |
| **Theme** (how it fits the dealt theme — material, tokens, palette balance, do-nots) | Absent — "a clean grid" is a layout claim, not a theme-fit claim; no material, token, palette-balance, or do-not reference. | **MISSING** |
| **Texture** (the not-flat-UI texture layer — what less-flat-ui treatment it carries, or `none — <reason>`) | Absent — nothing about texture, no explicit none. | **MISSING** |
| **Visuals** (imagery, iconography, visual treatment, what it looks like) | Absent — nothing about what the colour looks like or its visual treatment. | **MISSING** |
| **Techniques** (the other design techniques brought to bear — element kinds and skill techniques beyond the decision's own kind) | Absent — no technique beyond the decision itself. | **MISSING** |
| **Colors** (palette tokens used, balance, contrast) | **Partially present at most** — the decision names the pink token, but the reason ("chosen for a clean grid") says nothing about palette balance or contrast. Even the one dimension whose subject the decision names is not actually reasoned. | **NOT REASONED** |

The D19 rule states explicitly: "A decision whose recorded reasoning covers only layout/structure — the UI alone — does NOT satisfy this rule." The fixture reason covers only layout ("a clean grid") and is therefore a textbook layout-only reason: **it fails on all six dimensions** (five missing outright, the sixth unreasoned). The static check ("every decision-record entry carries all six dimension lines") would flag it as an incomplete build, and the blind reviewer "flags a missing dimension as a finding (minor at least)".

**Item 5: PASS** — the check fires on (a) a decision with no recorded reason at all (the v1 file) and (b) a layout-only reason (the fixture, failing all six dimensions).

## 6. Criteria coverage (D19) — all six dimensions + the `none — <reason>` form: PASS

The D19 rule text is present in the built tree in `design-taste-frontend/SKILL.md:262` and identically in `orchestrate/SKILL.md:102`, with app-surface mirrors in `ui-ux-pro-max/SKILL.md:101` and `orch-build-mvp/SKILL.md:44`. Quoted from `design-taste-frontend/SKILL.md:262` (the dimension definitions):

> "…every decision's recorded reason addresses SIX dimensions, one line each — **Motion** (what moves, what entrance/hover/loop it carries, or `none — <reason>`); **Theme** (how it fits the dealt theme — material, tokens, palette balance, do-nots); **Texture** (the not-flat-UI texture layer — what less-flat-ui treatment it carries, or `none — <reason>`); **Visuals** (imagery, iconography, visual treatment, what it looks like); **Techniques** (the other design techniques brought to bear — element kinds and skill techniques beyond the decision's own kind, e.g. a dealt moment, a diagram, an effect, a type moment, a craft-floor rule); **Colors** (palette tokens used, balance, contrast). A dimension that genuinely does not apply records `none — <reason>` — an explicit none, never a missing line. A decision whose recorded reasoning covers only layout/structure — the UI alone — does NOT satisfy this rule."

Coverage table:

| D19 element | Named in the built-tree D19 check text? | Covering quote (file:line) |
|---|---|---|
| Motion | YES | `design-taste-frontend/SKILL.md:262`: "**Motion** (what moves, what entrance/hover/loop it carries, or `none — <reason>`)". |
| Theme | YES | Same line: "**Theme** (how it fits the dealt theme — material, tokens, palette balance, do-nots)". |
| Texture | YES | Same line: "**Texture** (the not-flat-UI texture layer — what less-flat-ui treatment it carries, or `none — <reason>`)". |
| Visuals | YES | Same line: "**Visuals** (imagery, iconography, visual treatment, what it looks like)". |
| Techniques | YES | Same line: "**Techniques** (the other design techniques brought to bear — element kinds and skill techniques beyond the decision's own kind, e.g. a dealt moment, a diagram, an effect, a type moment, a craft-floor rule)". |
| Colors | YES | Same line: "**Colors** (palette tokens used, balance, contrast)". |
| `none — <reason>` as the only valid non-application | YES | Same line: "A dimension that genuinely does not apply records `none — <reason>` — an explicit none, never a missing line." Also in STATIC19 (all three files, e.g. `design-taste-frontend/SKILL.md:312`): "each a reason or an explicit `none — <reason>`". |

All six dimensions are named, each with its definition, and the `none — <reason>` form is named twice over — once inside the Motion and Texture definitions, and once as the standalone rule that a non-applying dimension records an explicit none, never a missing line. No bare omission is a valid non-application anywhere in the text.

**Item 6: PASS.**

## Verdict summary

| # | SPEC §6 item | Result |
|---|---|---|
| 1 | Rule presence — verify19.py passes | **PASS** — re-run by this worker, 75/75, exit 0 |
| 2 | Criteria coverage (font) — all six failure-mode tokens named as finding triggers | **PASS** — 6/6 (see the 2f note in §2: "`font-synthesis: none`" is literal in the F2 rule text and fires via the D1 synthesised-weight clause, not literally inside the STATIC19 paragraph) |
| 3 | Repair compliance (F2/F3/F4) | **PASS as repair-reported** — NOT re-verified from this VM; the live artifact source does not exist in this workspace |
| 4 | Negative demonstration (font) — stale v1 tokens file fails F2 | **PASS** — fails on five criteria, including the exact bug found |
| 5 | Negative demonstration (decision) — v1 decisions fail D19; layout-only fixture fails the six-dimension check | **PASS** — no recorded reason at all in the v1 file; fixture fails all six dimensions |
| 6 | Criteria coverage (D19) — all six dimensions + `none — <reason>` | **PASS** — all six named with definitions; explicit-none rule stated twice |

**Overall: PASS.**

## Notes for the parent / audit worker

1. **The 2f wording call (§2).** STATIC19's D1 clause names "a synthesised weight" as a finding; the literal prescription "`font-synthesis: none`" lives in the F2 rule text in the same skill file. If the audit wants every token literal inside STATIC19 itself, that is a one-line wording addition, not a rule gap — the check fires on the bug either way.
2. **F3's recording requirement (§3).** The repair record confirms the pairing (Bowlby One SC + Fraunces) and the absence of generic/system faces, but does not state the pairing's Source cell (which skill text dealt it). That is a build-record matter for a future build, not a defect in the repair.
3. **SPEC §1 baseline (139) vs measured (191).** Already recorded in `fix19/MANIFEST.md` §3 and `fix19/inventory.md`; verify19 asserts against the measured numbers. No action needed — flagged here only so the audit does not re-litigate it.
4. **`start.mjs` loader (MANIFEST §5 open item).** The Google Fonts `css2` loader still can serve variable fonts as the generation source; F2 governs the shipped format by rule, but the script does not yet enforce instantiation. That is an audit item, not a dry-run finding: this dry-run's scope is the check text and the demonstrations above.

## Files / evidence used (read-only)

- `~/workspace/hackathon-plugin/fix19/SPEC.md` (§1 evidence, §2 rules, §6 dry-run definition, §7 verify script)
- `~/workspace/hackathon-plugin/fix19/MANIFEST.md` (build.sh 23,314 lines, md5 `a8d3d3c6f6d32344d0168c5323d9364b`; deviations §3; open items §5)
- `~/workspace/hackathon-plugin/fix19/inventory.md` (191 baseline; 161 remaining; class breakdown)
- `~/workspace/hackathon-plugin/fix19/verify19.py` (re-run this session: **75/75**, exit 0)
- Built tree (read-only greps this session): `~/workspace/hackathon-plugin/hackathon-ecc/skills/design-taste-frontend/SKILL.md:246, 256, 262, 312`; `orchestrate/SKILL.md:61, 96, 102`; `ui-ux-pro-max/SKILL.md:95, 101`; `orch-build-mvp/SKILL.md:44, 57`
- Artifact (read-only, stale v1): `~/workspace/cold-start-render/campus-eats/docs/design-tokens.md` — lines 29 (font stacks), 44–46 (typography), 47–51 (colour, spacing/layout), 63–66 (motion); greps for `preload|font-synthesis|woff2|static|variable|fvar` (zero matches) and `reason|because|job it serves` (zero matches)
