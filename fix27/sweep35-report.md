# Sweep #35 — Fix #27, weaving-coherence sweep — CHECK-ONLY report

**SWEEP #35: NOT CLEAN — 0 blocking, 1 minor, weaving-coherence CLEAN**

Scope: staged sources (`new-skills/`, `round2-skills/`, `rewritten-skills/`,
`new-rules/`), the build-time patcher `fix27/fix27.py`, the built tree
`~/workspace/hackathon-plugin/hackathon-ecc/` (build run 7, exit 0;
node_modules excluded everywhere), `build.sh`, and the fix #27 working
files. Check-only: no plugin file edited, no `build.sh` run, no fix/apply/
verify script edited, no bundle, commit, push, or message sent, no
fix11/fix11-stage.py re-run, no subagents.

Read first, in full: `fix27/SPEC.md` (§0–§8), `fix26/sweep34-report.md`
(the model for this report), `fix27/audit74-report.md`,
`fix27/audit75-report.md`, `fix27/audit76-report.md`,
`fix27/fix27-patch-log.md`, `fix27/staged-patch-log.md`,
`fix27/fix27-round2-patch-log.md`, `fix27/fix27-round3-patch-log.md`.
Every number below was re-derived by this sweeper's own greps/commands
listed in §9; nothing was copied from the fix notes without re-running.

## 1. Build fingerprint + counts (re-derived)

| Item | Re-derived value | Expected | Result |
|---|---|---|---|
| `build.sh` lines | 24,100 (`wc -l`) | > 24,088 (fix #26) | PASS — +12, exactly the fix27 invocation block (`build.sh:24079-24090`: header + 9 comment lines + `python3 … fix27.py` + blank); the MotionSites loop edit at `build.sh:217` is a same-line change, 0 net lines |
| `build.sh` md5 | `ff7fe0015210b3583f69afb4f5a40816` | — (new) | Recorded |
| skills / agents / rules / commands | 67 / 45 / 123 / 55 (directory counts) | 67/45/123/55 | PASS |
| hooks | 15 (`hooks.json` hooks dict) | 15 | PASS |
| trigger keys | 49 (`skill-triggers@1.json` triggers object; `coverage.skills` 67) | 49 | PASS |
| call-map header counts | 67/45/123/55/15/49 | same | PASS |
| build log run 7 | `fix27: 102 change(s)`, `fix27: 13 OWED item(s) recorded`, `fix27: OK`, then STEP 5 counts 67/45/123/55, `build complete` | 102 changes, 0 errors | PASS — matches `fix27-patch-log.md` (`## Changes (102)`, `## Errors (0)`) |
| verify27.py re-run by this sweeper | **79/79, exit 0** | 79/79 | PASS — matches `fix27/verify27-run5.log` (`79/79 checks pass`) |

## 2. Anchor-token census — all 20 `_F27` tokens, staged vs built

Counts are occurrences (`grep -o`), staged = `new-skills/` +
`round2-skills/` + `rewritten-skills/` + `new-rules/`, built =
`hackathon-ecc/` (node_modules excluded).

| Token | Staged | Built | Delta, explained |
|---|---|---|---|
| DESIGNPKG-AUTO_F27 | 4 | 4 | — |
| CEILING_F27 | 5 | 5 | — |
| DELRISK_F27 | 5 | 5 | — |
| CHECKSRC_F27 | 3 | 4 | +1 built: `hackathon-pitch/SKILL.md:49`, the fix27.py build-time patch (MIT-origin file, SPEC §5(c)) |
| AUDITGUIDE_F27 | 3 | 4 | +1 built: same `hackathon-pitch/SKILL.md:49` patch |
| NOCOAUTHOR_F27 | 1 | 2 | +1 built: `rules/common-git-workflow.mdc:16`, the fix27.py build-time patch (ECC-origin file, SPEC §5(e)); staged 1 is orchestrate step 6 (:104) |
| THEME-START_F27 | 12 | 16 | +4 built: `orch-build-mvp/SKILL.md:43` ×2 and `ui-ux-pro-max/SKILL.md:274` ×2, the fix27.py build-time E1 patches (B2) |
| ALWAYSLEAD_F27 | 6 | 6 | — |
| IMPL46_F27 | 2 | 2 | — |
| GRILLHDR_F27 | 5 | 5 | — |
| CAPTURE1_F27 | 0 | 1 | +1 built: `browser-qa/SKILL.md`, the fix27.py build-time patch (ECC-origin, SPEC §4(c)); 0 staged by design |
| TESTNOTBQA_F27 | 0 | 1 | +1 built: `verification-before-completion/SKILL.md`, the fix27.py build-time patch (marketplace-origin, SPEC §5(d)); 0 staged by design |
| DEFER3_F27 | 1 | 3 | +2 built: orchestrate `:8` and the trigger-manifest notes, both fix27.py patches; staged 1 is hackathon-mode `:22` |
| W2_F27 | 7 | 7 | — |
| W3_F27 | 9 | 9 | — |
| W4_F27 | 2 | 2 | — |
| TESTPASS_F27 | 1 | 1 | — |
| REROUTE_F27 | 19 | 29 | +10 built: orch-add-feature `:33`, orch-build-mvp `:41`, orch-change-feature `:36`, orch-fix-defect `:36`, orch-refine-code `:35`, integration `:21/:46/:60/:122`, ui-ux-pro-max `:363` — all fix27.py build-time re-routes (B1/B9) |
| MOTIONSITES_F27 | 4 | 4 | — |
| PALETTE-FIRST_F27 | 3 | 3 | — |
| **Total** | **92** | **113** | **+21, all build-time patches, no staged token missing from the built tree** |

No staged token is absent from the built tree; no built token lacks a
staged or fix27.py origin. Every delta is a documented build-time patch,
not a staged edit lost in the build.

Per-token built locations (file:line, one occurrence per line unless
noted): DESIGNPKG-AUTO orchestrate :35/:65/:92, hackathon-mode :44;
CEILING orchestrate :73/:99/:106/:385, hackathon-scope :69; DELRISK
orchestrate :61/:108/:386, hackathon-mode :60/:68; CHECKSRC orchestrate
:110/:387, hackathon-scope :73, hackathon-pitch :49; AUDITGUIDE
orchestrate :112/:387, hackathon-scope :77, hackathon-pitch :49;
NOCOAUTHOR orchestrate :104, common-git-workflow :16; THEME-START
orchestrate :35/:138/:148 (×2 on :148), design-taste-frontend
:258/:264/:425 (×2 on :425), feature-expansion :152/:196,
slop-checklist :27, hackathon-mode :44, orch-build-mvp :43 (×2),
ui-ux-pro-max :274 (×2); ALWAYSLEAD orchestrate :14/:59/:61/:120,
hackathon-mode :12/:48; IMPL46 orchestrate :29/:92; GRILLHDR orchestrate
:57, grill-me :39, hackathon-scope :9, hackathon-mode :60/:62; CAPTURE1
browser-qa (1 occurrence); TESTNOTBQA verification-before-completion (1);
DEFER3 orchestrate :8, hackathon-mode :22, trigger notes :7; W2
orchestrate :18/:128/:289/:293/:295/:326, patterns :28; W3 orchestrate
:73/:99/:272/:275/:283 (6 occurrences across 5 lines — one line carries
two), feature-expansion :32, design-taste-frontend :539, polish-pass
:112; W4 orchestrate :69/:71; TESTPASS orchestrate :281; REROUTE 29
locations as tabulated above plus feature-expansion ×10, orchestrate
:3/:65/:136/:138, dispatch-prompt :24, hackathon-mode :46/:48/:53/:55;
MOTIONSITES orchestrate :35, hackathon-mode :44,
motionsites-web-builder SKILL.md :6/:69; PALETTE-FIRST orchestrate :35,
hackathon-mode :44, design-taste-frontend :224.

## 3. Staged-edited files: staged vs built

md5 comparison for the 10 staged-edited files named in the brief, plus
the call map and hackathon-scope:

| File (staged → built) | Result |
|---|---|
| orchestrate/SKILL.md | DIFFERS — 7 lines only: `:8` (DEFER3 six→three), `:99` + `:272` + `:279` (fix16 agent-link expansions: bare `` `code-reviewer` `` → `` `code-reviewer` agent (`agents/ecc-code-reviewer.md`) ``, same for `security-reviewer`), `:104` (`conventional-commit-review` → `git-workflow`), `:114` + `:381` (DEFER3 six→three). All fix27.py or fix16 build-time patches; line count 403 = 403. |
| hackathon-mode.mdc | DIFFERS — 1 line only: `:38`, the fix16 rewrite of the upstream `` `claude -p` `` wording to "CLI-subprocess" (staged-patch-log appendix: the staged reword was attempted then reverted so fix16.py:3807's hard anchor stays intact). Line count 73 = 73. |
| design-taste-frontend/SKILL.md | DIFFERS — 1 region only: `:9-13` (5 lines) → `:9-14` (6 lines), the build.sh STEP 3 scope split: "Use ONLY for a full company or landing-page build from scratch…" / "Do NOT use for dashboards, apps, components, or fixes to existing UI — those belong to ui-ux-pro-max … and polish-pass". Pre-existing build-time patch, not a fix27 edit; no `_F27` token on any differing line. Line count 639 → 640 (+1). |
| feature-expansion/SKILL.md | DIFFERS — 11 lines: `:3`, `:12`, `:33-34` (build.sh STEP 3 "ECC process applies" / "Review while building" insertions), `:49`, `:137`, `:160`, `:192`, `:194-195`, `:213` (fix16 agent-link expansions, e.g. `` `code-explorer` `` → `` `code-explorer` agent (`agents/ecc-code-explorer.md`) ``). The REROUTE_F27 token on :192 is preserved verbatim. Line count 214 = 214. |
| grill-me/SKILL.md | IDENTICAL — md5 `7209a946e8964bca4daa86f83f717de1` |
| polish-pass/SKILL.md | DIFFERS — 5 lines: `:3`, `:15`, `:27`, `:34`, `:98-99`, the build.sh STEP 3 polish-pass patch naming design-taste-frontend ("… `ui-ux-pro-max`, `less-flat-ui`, and `design-taste-frontend` for design direction…"). Pre-existing build-time patch, not a fix27 edit. Line count 127 = 127. |
| orchestrate/references/dispatch-prompt.md | IDENTICAL — md5 `1944a1c5458c3157b843d980f0d34bc9` |
| orchestrate/references/patterns.md | IDENTICAL — md5 `36f587ec1a8e98ca19eeca7fc8393b06` |
| polish-pass/reference/slop-checklist.md | IDENTICAL — md5 `4ab221cef719470006ce3f49c3f32a6a` |
| motionsites-web-builder/SKILL.md | IDENTICAL — md5 `4220fb98d58fcb2c9a5d284e23754c08` (matches Audit #76); step-2 ignore-upsell line at built `:26`, directly under the fetch URL at `:25` |
| orchestrate/references/call-map.md | IDENTICAL — md5 `d82aec31bd98831533afd850f2861927` (matches Audit #76); counts table 67/45/123/55/15/49; B6 DOCUMENTATION-ONLY note intact (:38); `motionsites-web-builder` row at :104 with STRONG invokers; zero rows for the 5 cut commands (grep for `learn-eval` / `project-init` / `/projects` / `promote` / `prune` returns 0) |
| hackathon-scope/SKILL.md | IDENTICAL — md5 `59b2890babc000a6c2438064a541f212` |

No staged edit was lost in the build: every differing line is a
documented build-time-only rewrite (fix27.py §6/§7 patches, fix16
agent-link expansions, or build.sh STEP 3 patches), and every
`_F27`-bearing staged line is present at the same line in the built
copy except the two noted +1 shifts (design-taste-frontend E1
:424 staged → :425 built; PALETTE-FIRST :223 staged → :224 built).

## 4. Weaving coherence (a–f) — all six agree

### (a) DESIGNPKG-AUTO — VERIFIED

- `skills/orchestrate/SKILL.md:35` and `rules/hackathon-mode.mdc:44`
  are **byte-identical** (modulo the leading `- ` list marker):
  the same 10-skill list (design-taste-frontend / ui-ux-pro-max /
  less-flat-ui / polish-pass / motion-foundations / motion-patterns /
  motion-advanced / make-interfaces-feel-better / design-system /
  motionsites-web-builder), the same
  "`motionsites-web-builder` — cinematic components, motion patterns,
  hero treatments and media (free sample only; consulted, never a
  template)" gloss, the same "design decision with no package skill
  named … is off-skill improvisation and fails the audit" sentence,
  and the same "theme deal is the starting point, not the cage"
  close. Step-3 (:65) and step-4 (:92) extend it identically in
  orchestrate: "Design package in every brief that contains a design
  decision".
- The design-taste-frontend flow carries the same package: its
  palette paragraph (:224) names `motionsites-web-builder` with the
  same gloss ("free sample only … consulted, never a template") and
  the design package by name; Taste is itself the package lead, and
  orchestrate row 10 / orch-build-mvp's design-package rule route
  every UI slice through the package components. No design decision
  in the plugin's own artifacts is routed outside the package.

### (b) PALETTE-FIRST — VERIFIED

- The inventory-first ordering is stated identically in all three
  files: design-taste-frontend `:224` ("inventory the available
  components BEFORE the direction is finalized … Before any deal in
  this step — before the Hallmark theme deal and before the palette
  deal below"), orchestrate `:35` and hackathon-mode `:44`
  (byte-identical paragraphs: "inventories the available component
  palette FIRST, before the design direction is finalized, and bases
  the direction on it"). Ordering in Taste: palette step :224 →
  deal commands :226+ → Hallmark theme deal :258 → step-4a freeze
  :413. The audit hook is identical in all three: "The audit checks
  the design-direction record names the palette components used
  (sources + components + tailoring); a direction with no palette
  attribution is a finding."
- Palette contents agree: MotionSites + the design package
  (ui-ux-pro-max, less-flat-ui, motion-foundations, motion-patterns,
  motion-advanced, make-interfaces-feel-better, design-system) +
  the dealt Hallmark theme — the same set in orchestrate:35 /
  hackathon-mode:44 (enumerated) and taste:224 (grouped as "the
  design package (…)" plus motionsites-web-builder plus the dealt
  theme; design-taste-frontend itself and polish-pass are not palette
  sources — the lead contributes no components, polish-pass fixes
  existing UI — a grouping difference, not a content difference).
  **Animaster: 0 hits** in all three files, and 0 hits across the
  staged sources, the built tree, and `build.sh`.

### (c) THEME-START — VERIFIED across all FOUR E1 copies

All four E1 blocks are verbatim identical on the two operative
points (each block carries the token twice on one long line):

| Copy | Bound (2) | New-theme clause | Inversion sentence |
|---|---|---|---|
| orchestrate:148 | "… **or a recorded departure from it** (D19 reason required)" | deleted; "NOT within reason: a new palette" only | "Inventing a theme direction is a recorded D19 decision, not a forbidden move" |
| design-taste-frontend:425 (staged :424; brief's :423 is the pre-palette-insert anchor) | same | same | same |
| orch-build-mvp:43 | same | same | same |
| ui-ux-pro-max:274 | same | same | same |

Zero "a new theme (re-deal" hits remain in any of the four files.
The departure allowance also agrees in the slop-checklist header
(`:27`: "A D19-recorded departure satisfies the fit criterion") and
in taste `:258`/`:264` and orchestrate `:138` (dashboard hero-moment
line). The theme cage is lifted identically everywhere it appears.

### (d) B14 — VERIFIED: hackathon-mode §7:60/:62 vs orchestrate:57 agree

Read in full, both texts say the same thing:

- orchestrate:57: "If the check finds no record and no explicit
  skip, that is itself a finding (GRILLHDR_F27): state in the first
  reply that grill-me did not run and why (no trigger / no record),
  and ask the user whether to grill now (one prompt) or proceed —
  the one-question exception to §7. Do not silently proceed on a raw
  prompt."
- hackathon-mode:60: "… do not silently proceed on the raw prompt:
  state in the first reply that grill-me did not run and why (no
  trigger / no record), and ask the user whether to grill now (one
  prompt) or proceed — the one-question grill-now-or-proceed ask, the
  second one-question exception to §7 alongside the
  deliverable-at-risk flag (GRILLHDR_F27). Do not re-run `grill-me`
  unasked." The same paragraph's "do not ask the user anything" now
  reads "(except the one-question grill-now-or-proceed ask above)".
- hackathon-mode:62 (override): "§7 overrides any ask/stop/wait
  instruction … — except the one-question grill-now-or-proceed ask
  above (GRILLHDR_F27)."

No silent proceed; state grill-me-missed in the first reply; one
grill-now-or-proceed question; that question is carved out of §7's
override in both files. The Audit #74 contradiction is resolved and
stays resolved. (Observation O1, §7, notes a loose first sentence
inside orchestrate:57 itself; it does not contradict
hackathon-mode:60.)

### (e) DEFER3 — VERIFIED

The three kept deferred checks agree across orchestrate (`:8` with
the DEFER3_F27 token, `:114`, `:381`), orch-build-mvp (`:86`),
hackathon-mode (`:22`, token), and the trigger-manifest notes
(`skill-triggers@1.json:7`, token): every copy names exactly
`verification-loop`, `production-audit`, `delivery-gate` and nothing
else. Zero "six deferred" hits in the built tree's three files;
zero `codehealth-mcp` / `santa-method` / `security-scan` hits in
orchestrate, orch-build-mvp, or hackathon-mode at all. (SPEC §1(b)'s
"(:8, :103, :370)" are pre-edit line numbers; the built lines are
:8, :114, :381 — content identical.) Trigger notes read verbatim:
"Deferred: verification-loop, production-audit, delivery-gate.
(DEFER3_F27)".

### (f) Check-12 allow-list consistency — VERIFIED

Parsed `verify27.py`'s `ALLOW_LIST` / `ALLOW_NAMES` literals with
`ast`: **82 whole-line entries across 43 files + 1 name-scoped line
(`rules/hackathon-mode.mdc:46`, 2 names) = 83 allow-listed lines** —
exactly OWED-13's count and exactly verify27.py's own sweep report
("0 un-allow-listed, 83 allow-listed, 293 generic bare-word noise
lines") on this sweeper's re-run. Spot-checked 12 entries in context,
all matching their justifications:

- orchestrate:136 — prose-history "`ecc-recipes` was cut" (B3) ✓
- delivery-gate:13 — "former `agent-self-evaluation` skill — cut in
  fix #27" (M4) ✓
- feature-expansion:100 — "`product-lens` was cut" REROUTE note ✓
- integration:46 — routes to kept `documentation-lookup`; the CUT
  name is inside the "(… `skill-scout` was cut)" note ✓
- ecc-spec-miner:201 — negative ("does not require
  `codebase-onboarding`") ✓
- learn.md:2 — negative (distinguishes itself from CLv2) ✓
- react-patterns.mdc:194 — pointer-style ("For accessibility see
  `skills/accessibility/SKILL.md`", M7/OWED-11 class, carried) ✓
- hackathon-mode:37/:38 — negatives ("is not used", "deliberately
  NOT wired") ✓; :46 name-scoped — only `product-lens` /
  `intent-driven-development` allowed, `brainstorming` on the same
  line is NOT allowed ✓
- ui-ux-pro-max/scripts/core.py:232 — data (icon/search keyword
  `"accessibility"`) ✓
- rust-patterns.mdc:168 — pointer-style ("See skill:
  `rust-patterns`…", M7 class) ✓

Vercel entries are gone: zero `vercel-checklist` mentions anywhere
in `verify27.py` (the 11 entries removed by the coordinator
addition). `agents/ecc-typescript-reviewer.md` has no allow-list
entry at all (its only `verify27.py` mentions are the KEPT_AGENTS
list at :181 and the check-12b comment at :936 recounting B-new-1);
built `:119` now routes to the kept stack only
("`typescript-patterns` … plus `frontend-patterns` or
`backend-patterns`"), verified by reading the line.

### (g) OWED-13 record (M-new-7 fix) — VERIFIED, with independent re-derivation

- `fix27/fix27.py:1086` and the regenerated
  `fix27/fix27-patch-log.md:157` are **byte-identical** on OWED-13
  (4,204 chars each, compared by script): both say "accessibility
  **131**" (not 132), enumerate vercel-checklist **:93** alongside
  the 11 re-pointed citations, and carry the M-new-7 parenthetical
  ("the census counted 132 including vercel-checklist.md:93, a
  bare-word routing reference the staged worker also re-pointed to
  frontend-a11y, so the live count is 131").
- Independent re-derivation (own script replicating check 12's
  sweep over `skills/`, `agents/`, `commands/`, `rules/`, excluding
  the call map): **293 noise lines total**; per generic name —
  accessibility **131**, projects 156, promote 4, brainstorming 3,
  evolve 1, prune 1 (sum 296; 3 lines carry two generic names, so
  293 lines). Exactly OWED-13's numbers. Vercel-checklist now has
  **zero** `accessibility` hits; `:93` reads "named skill
  (frontend-a11y, motion-*, `ui-ux-pro-max`, the dealt theme)".
  Staged and built vercel-checklist md5s are identical
  (`edb22b15076db97f4be0a04ba771fad7`).

## 5. Kept-essentials spot-check — VERIFIED

- **gan-style-harness + agents/commands present and called:**
  `skills/gan-style-harness/` present; agents
  `ecc-gan-evaluator` / `ecc-gan-generator` / `ecc-gan-planner`
  present; commands `gan-build` / `gan-design` present.
  orch-build-mvp drives `/gan-build` at :62/:95 ("the orch-build-mvp
  step 4 GAN loop"); the call map's `gan-style-harness` row (:91)
  lists the three gan agents + gan-build as STRONG invokers, and
  `/gan-build` (:334) / `/gan-design` (:335) rows list the agents.
- **growth-log present** (`skills/growth-log/`); the harness-audit
  `memory-learning-skill` check points at it (verify27 check 10b
  passes on re-run).
- **The 9 design-package skills present:** design-taste-frontend,
  ui-ux-pro-max, less-flat-ui, polish-pass, motion-foundations,
  motion-patterns, motion-advanced, make-interfaces-feel-better,
  design-system — all 9 dirs exist.
- **learn KEPT:** `commands/learn.md` present (user-invoked
  session-review tool; its description distinguishes itself from the
  removed CLv2 system).
- **The 5 cut commands absent:** `learn-eval`, `project-init`,
  `projects`, `promote`, `prune` — all absent from `commands/` and
  from the call map (0 hits).
- **pi-core.json pruned (counted directly):** `skills.include` **30**
  entries, `commands.include` **18** entries (the `.md`-suffixed
  command names); **0 CUT skills** in `skills.include`, **0 dropped
  commands** in `commands.include` (checked against verify27.py's
  CUT_SKILLS / DROPPED_COMMANDS lists); every remaining entry exists
  in the built tree; `learn-eval.md` / `project-init.md` sit in
  `commands.exclude`, not `include`; the description's claim
  ("skills.include lists the shipped subset only") is true again.
- **Banned terms:** exactly 3 hits in the built tree, all the
  allow-listed MotionSites lines (SKILL.md:25, :38; LICENSE:1) —
  nothing else. **Grok pins:** `grok-4.7-high` ×56,
  `cursor-grok-4.6-high-fast` ×74, bare `grok-4.6-high-fast` ×0 —
  exactly the Audit #75/#76 numbers.
- **Animaster:** 0 hits across staged sources, the built tree, and
  `build.sh` (leave-out holds).

## 6. Findings

### MINOR 1 — Round-1 counts (66 skills / 60 commands / 27 dropped commands) still live in three files' prose

The round-2 count moves (66 → 67 skills via the vendored
motionsites-web-builder; 60 → 55 commands via the 5 further cuts:
learn-eval, project-init, projects, promote, prune) were never
propagated to the prose that describes what fix27 does. The checks
themselves assert the right numbers (verify27 checks 1/5/6/7 pass on
67/45/123/55; the patch log records 32 dropped commands), but three
live descriptions still state the round-1 figures:

- `build.sh:24081-24082` (the fix27 invocation-block comment):
  "removes 100 CUT skills, 27 companion agents, **27 CUT-only
  commands**; prunes 15 trigger keys (64 -> 49); updates README
  counts to **66/45/123/60**". Actual: 32 commands dropped
  (patch log: "commands dropped: 32 files"), README counts
  67/45/123/55 (built `README.md:13`).
- `fix27/fix27.py:256` (section header): "# 3. drop the **27
  CUT-only commands**" — the loop directly below iterates
  `DROPPED_COMMANDS`, which has 32 entries (verified by parsing the
  literal). The module docstring at `:16` also still quotes SPEC §1's
  "166 -> 66 skills".
- `fix27/verify27.py:8-10` (module docstring): "debloat 166 -> **66
  skills** (100 CUT), 27 companion agents removed (72 -> 45), **27
  CUT-only commands dropped (87 -> 60)**". Actual: 166 -> 67 skills,
  32 commands dropped (87 -> 55).

This is stale prose / record inaccuracy only: no shipped rule, no
dispatch, and no verifier check reads these lines. It is the same
class as Sweep #34's MINOR 1 (a stale comment contradicting a
recorded disposition). Note the irony the fix should also address:
verify27.py check 6 *fails the built tree* on the tokens "66
skills" / "60 commands" (fix27.py:1065-1066, verify27.py:344-345)
while its own docstring still carries them.

**Fix:** in the three spots, "27 CUT-only commands" → "32 CUT-only
commands", "66/45/123/60" → "67/45/123/55", "166 -> 66 skills" →
"166 -> 67 skills", "(87 -> 60)" → "(87 -> 55)". One-line edits;
no behavior change; re-run verify27.py afterwards (expected still
79/79 — the docstring is not asserted on).

## 7. Observations (not findings)

**O1 — Orchestrate:57's first sentence is looser than its own second
sentence.** ":57" opens "If neither holds, do not proceed without a
check: run the check …, and once that check is done, proceed on the
raw user prompt with a stated assumption" — read alone, that licenses
proceeding after merely running the check. The next sentence in the
same paragraph disambiguates it ("If the check finds no record and
no explicit skip, that is itself a finding: state … and ask … Do not
silently proceed"), and hackathon-mode:60's "Once the check passes,
the first build runs fully autonomously" presupposes the same
branching. The operative rule agrees everywhere (§4(d)); the first
sentence is a leftover of the pre-fix27 wording. A one-clause
tightening ("once that check finds a record or an explicit skip,
proceed…") would remove the misreading, but it is not a
contradiction as written.

**O2 — Taste's theme-deal / palette-deal file order vs execution
order.** The palette/css deal commands print at
design-taste-frontend `:226-228`, *before* the theme-deal paragraph
at `:258` ("Before the palette deal above, run the Hallmark theme
deal"). The palette-first paragraph at `:224` says the same deal is
"the palette deal below". Both are spatially correct from their own
lines (the css deal sits between them), and both state the same
execution order (inventory :224 → theme deal :258 → palette/css
deal). A reader following the file top-to-bottom must still read
:258's ordering instruction rather than executing the commands in
print order. Pre-existing layout, not a fix27 regression; Audit #75
already passed the ordering.

## 8. Open items (carried, explicitly — not findings this round)

1. **Fix MINOR 1** (§6): update the three stale round-1 count
   mentions (build.sh:24081-24082, fix27.py:256 (+:16), verify27.py
   docstring :8-10) to 67/55/32.
2. **fix27/MANIFEST.md does not exist yet** (checked: no
   `fix27/MANIFEST.md`, no dry-run #42 file). SPEC §7 requires the
   manifest (disposition table, anchor tokens, open parent
   adjudications), Sweep #35, and Dry-run #42. The prior-verifier
   retirements (verify26.py / verify25.py crash on the reduced tree
   — Audit #76 M-new-3, still unrecorded anywhere except the audit
   reports and the round-3 log's Un-done #1) and the OWED-13
   M-new-7 correction belong in the manifest when written.
3. **Rules (123) NOT cut** — per SPEC §1(d), the per-language rule
   families for cut languages remain a follow-up debloat candidate;
   their dangling skill pointers are M7/OWED-11 (record verified
   accurate; allow-listed as pointers in check 12).
4. **Install manifests left unpruned by decision** —
   `install-modules.json` (100 CUT skill paths of 166) and
   `install-components.json` (5 CUT skill components + 1
   continuous-learning-v2 mention) remain upstream-catalog artifacts
   per the recorded M-new-4 decision (fix27.py §8c, patch log); pi-core.json
   is the pruned one. A coherent prune would need a modules +
   components + profiles change with installer test coverage.
5. **Carried prior open items (unchanged):** Netlify row touch-up
   due after Dec 4, 2026; live smoke test still the gate before
   GitHub publish; D-6, C-5, C-6, D-9, E-7 carried items from
   fix25/MANIFEST.md §5.

## 9. Commands run (method)

All run read-only from `~/workspace/hackathon-plugin` (built-tree
greps from `hackathon-ecc/`; node_modules excluded everywhere; the
only file written is this report; one scratch script `/tmp/noise.py`,
not part of the repo):

- `wc -l build.sh && md5sum build.sh`; directory counts per built
  directory; `hooks.json` hooks dict (15); skill-triggers key count
  (49) + coverage.skills (67); `sed` of `build.sh:24078-24090` (fix27
  block = +12 lines) and `:217` (motionsites loop line)
- `python3 fix27/verify27.py` (re-run: 79/79, exit 0); `tail` of
  `fix27/verify27-run5.log` (79/79, matches)
- Per-token census loop for all 20 `_F27` tokens (staged and built,
  `grep -o` counts + per-file/per-line locations via
  `grep -rn … | cut -d: -f1-2`); python cross-check census (same
  totals: staged 92, built 113)
- md5 + `diff` staged vs built for orchestrate, hackathon-mode,
  design-taste-frontend, feature-expansion, grill-me, polish-pass
  (SKILL.md + slop-checklist), dispatch-prompt, patterns,
  motionsites-web-builder, call-map, hackathon-scope, vercel-checklist
  (md5 `edb22b15076db97f4be0a04ba771fad7` both copies)
- Full-line reads of orchestrate:35/:57/:65/:92, hackathon-mode
  :44/:60/:62, design-taste-frontend :224/:258/:264/:425,
  orch-build-mvp :43, ui-ux-pro-max :274; python byte-identity check
  orchestrate:35 vs hackathon-mode:44 (identical modulo leading
  `- `); palette-source presence checks in all three files;
  `grep -rni animaster` staged + built + build.sh (0)
- DEFER3: reads of orchestrate :8/:114/:381, orch-build-mvp :86,
  hackathon-mode :22, trigger notes; `grep` for "six deferred" /
  codehealth-mcp / santa-method / security-scan in the three files (0)
- Allow-list: `ast` parse of verify27.py `ALLOW_LIST`/`ALLOW_NAMES`
  literals (82 + 1 = 83 across 43 files); 12 entries read in context
  at their built lines; `grep vercel-checklist` over verify27.py (0);
  `grep ecc-typescript-reviewer` over verify27.py (only :181
  KEPT_AGENTS + :936 comment); read of built
  agents/ecc-typescript-reviewer.md:119
- OWED-13: python comparison fix27.py:1086 vs patch-log:157
  (byte-identical, 4,204 chars); `/tmp/noise.py` replication of the
  check-12 sweep (293 noise lines; accessibility 131, projects 156,
  promote 4, brainstorming 3, evolve 1, prune 1); `grep -n
  accessibility` over vercel-checklist (0); read of :93
- Kept essentials: presence checks for the 9 design-package skills,
  gan-style-harness + 3 gan agents + gan-build/gan-design,
  growth-log, learn; absence checks for the 5 cut commands; pi-core
  counts + CUT/dropped overlap via `ast` (30/18, 0/0, all entries
  exist); banned-term grep over the built tree (3 hits, all
  MotionSites); Grok-pin counts (56/74/0); call-map grep for the 5
  cut commands (0) and the motionsites row (:104)

## Verdict

**SWEEP #35: NOT CLEAN — 0 BLOCKING, 1 MINOR, weaving-coherence CLEAN.**

The fix #27 weaving holds: DESIGNPKG-AUTO is byte-identical in
orchestrate:35 and hackathon-mode:44 with the same skill list and
gloss, and the design-taste-frontend flow carries the same package;
PALETTE-FIRST orders the inventory before every direction-finalizing
step in all three files with agreeing palette contents and no
Animaster anywhere; THEME-START's E1 bound-(2) relaxation and
new-theme inversion are verbatim identical across all four copies;
B14's grill-me-missed question agrees between orchestrate:57 and
hackathon-mode §7:60/:62, including the §7 carve-out; DEFER3 names
exactly the three kept checks in orchestrate, orch-build-mvp,
hackathon-mode, and the trigger-manifest notes; the check-12
allow-list is exactly 82 whole-line + 1 name-scoped = 83, with the
vercel entries gone and orchestrate:136 present; and OWED-13 now
states "accessibility 131" with vercel-checklist :93 enumerated, in
both fix27.py and the regenerated patch log, confirmed by an
independent re-derivation of the noise count (293 lines; 131/156/4/3/1/1).
Counts (67/45/123/55, hooks 15, triggers 49), the call map, the
20-token census (92 staged / 113 built, every delta a documented
build-time patch), verify27.py 79/79 on re-run, banned terms (3
allow-listed MotionSites lines), Grok pins (56/74/0), and the kept
essentials (GAN harness called, growth-log, 9 design-package skills,
learn kept, 5 cut commands absent, pi-core 30/18 with 0 CUT/dropped)
all verify clean. The single minor finding is stale prose: the
round-1 counts (66 skills / 60 commands / 27 dropped commands) still
sit in the build.sh fix27 comment, a fix27.py section header, and
the verify27.py docstring, while the tree ships 67/55/32. Fixing it
is three one-line prose edits; nothing in the weaving needs to change.
