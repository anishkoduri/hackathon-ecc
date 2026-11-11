# Single-executor sweep #13i — REPORT

## Verdict: CLEAN — 0 blocking, 0 minor

Rule swept: `browser-qa` is the SOLE executor of pass/fail VERDICTS on rendered
screens; everything else is design guidance / candidate evidence / static
checks, worded as such, never as a verdict. Read-only sweep; no files edited,
no fix round started.

## Build identity (verified first)

- `~/workspace/hackathon-plugin/build.sh`: **23,117 lines**, md5
  `cb12ab81c3334dba68054ba18c1d4f15` — matches the fix #13i manifest.
- Built-tree manifests `fix13i/manifest1.txt` and `manifest2.txt` are identical
  (same md5); manifest `eecb5315311c70d9675951db4b37ff7f`; two clean builds,
  diff = 0.
- Built tree `~/workspace/hackathon-plugin/hackathon-ecc/`: **169 skills /
  72 agents / 123 rules / 96 commands / 15 hooks, 57 MB** — matches.
  (Hooks dir lists 17 entries = 15 hook `.js` files + `adapter.js` +
  `hooks.json`.)
- Note: `build.sh` lives at `~/workspace/hackathon-plugin/build.sh`, not inside
  `hackathon-ecc/`; the built tree is `hackathon-ecc/`. All citations below are
  against the built tree.

## Method

Greps over `skills/` (`.md`/`.mdc`/`.mjs`), `rules/`, `commands/` in the built
tree, excluding the `browser-qa` skill itself, for: `verdict`, `PASS`/`FAIL`,
`pass/fail`, `ship it`, `redesign needed/indicated`, `REFLEX`, `FAIL`, `is a
template`, `reads as a template`, `generic template`, `machine-made`,
`generated look`, `ship`, `rebuild`, `judge`, `first word`, `recapture`.
Raw hit counts: verdict 202, PASS/FAIL 3,081, ship/rebuild 215, REFLEX 116,
template-family 35, judge 348, ship-it/redesign-needed 5. Every hit in a
design context was triaged by reading the cited file at the cited line; the
bulk of the PASS/FAIL and judge hits are code/test contexts (test failures,
ownership, hackathon judges as humans) with no rendered-screen verdict
content. A final targeted PASS/FAIL pass over all design-critical files
(Taste, ui-ux-pro-max, orchestrate, orch-build-mvp, polish-pass incl.
scoring/craft-floor/critique, design-system, gan-style-harness,
hackathon-scope, less-flat-ui, make-interfaces-feel-better, frontend-slides,
web-design-quality.mdc, hallmark-floor, redesign, review-hero/finish,
gan-build, gan-design) surfaced nothing beyond what is listed below.

## Fix #13i areas — verified clean

- **First-word vocabulary (definitions + all four consumers + gates :245).**
  Definitions: `review-finish.md:5` — first line one of `recapture` /
  `findings` / `no-findings`; "The first word is a craft status, not a
  ship/fix/rebuild verdict". `review-hero.md:5` — first line `findings` or
  `no-findings`; "The word is a craft status, not a ship/fix verdict".
  Consumers: `orchestrate/SKILL.md:195` ("Act on its first word
  (`recapture` / `findings` / `no-findings`)"), `orch-build-mvp/SKILL.md:49`
  (same triple), `design-taste-frontend/SKILL.md:314` ("Act on its first word
  (`no-findings` / `findings`)"), `gates.md:245` ("Act on its first word.
  `recapture` means the screenshots were wrong… Send the recaptures back for
  one scoring round only when a finding names a first-viewport wholesale
  failure or a Floor gate; scoring is not a second review. Record the outcome
  in the stamp, hero first: `hero-review: findings · 4 findings · 4
  resolved`"). No `ship` / `fix` / `rebuild` first-word value survives
  anywhere: backticked-`` `ship` `` / `` `fix` `` / `` `rebuild` `` grep over
  the Hallmark/orchestrate/standalone/polish-pass dirs returns 0 hits, and
  the `recapture` consumer grep finds no other consumer.
- **gates.md §5 clauses incl. gate 68.** Gate 68 (`gates.md:225`) ends "The
  wireframe read is candidate evidence of a generated look, for `browser-qa`
  to weigh at a glance." Neighbours likewise routed: 23 (`:199`, "not a
  template verdict"), 80–82 (`:233`), 83 (`:235`), 85 (`:239`), 6b (`:189`),
  8/32 (`:191`), 9 (`:193`) — all candidate evidence for `browser-qa`. §3
  pre-emit critique (`:38–40`) is "a design input, not a distinctiveness
  verdict"; Specificity under 3 goes to candidate evidence only.
- **sloplint-render scope guards.** `sloplint-render.mjs:2` header: "Its
  FAIL/REFLEX/WARN grades are render-check grades, not pass/fail verdicts on
  rendered screens… Template gates (80, 81, 82, 83, 85) never issue REFLEX
  verdicts here: on landing pages they emit NOTE candidate evidence for
  `browser-qa`; on app screens they are skipped (mirroring sloplint.mjs
  APP_SKIP)." `:741–748` implements it (`templateEvidence` pushes NOTE on
  landing, skips outright in app scope). `sloplint.mjs:2` header carries the
  matching static-grade disclaimer; `:798–799` `APP_SKIP` set confirmed
  present; `:2961` gate-38iii scope note present ("its FAIL/REFLEX grade is
  not a pass/fail verdict on a rendered screen").
- **Taste hero bar.** `design-taste-frontend/SKILL.md:53`: hero bar is
  candidate evidence for `browser-qa`, "whose visual-loop verdict alone
  decides whether the hero passes the distinctiveness bar". `:314` hero
  review routes template observations to candidate evidence, "never
  fix-batch verdicts". `:283`: "Every `check.mjs` finding fails the page on
  layout-correctness grounds… a layout finding is not a distinctiveness
  verdict — that is `browser-qa`'s alone."
- **Craft floor / gloss / critique bands / Harmony / scoring.**
  `craft-floor.md:5,111,168` and `impeccable-craft-floor.md:30,34,35`: bans are
  static/code-level checks and candidate evidence, never a rewrite on the
  check alone for template patterns. `polish.md:39,49` (incl. the
  `icon-tile-stack` carve-out, "never rewrite a template pattern on the
  detector's say-so alone") and `polish-pass/SKILL.md:92` (gloss: "the
  stricter ban wins — except page-level template patterns, which are
  candidate evidence for `browser-qa`, never a rewrite decided here").
  Critique bands `impeccable-critique.md:595` ("informs candidate evidence,
  never a ship verdict"), `:599` ("Redesign indicated, not decided; …
  record as candidate evidence for `browser-qa`"), `:601` ("The bands inform
  candidate evidence for `browser-qa`; only `browser-qa`'s verdict
  establishes a finding"); "ship it" / "Redesign needed" / "Major UX
  overhaul required" are 0 hits in the file. `:142` bars a generic-template
  Priority fix without a `browser-qa` verdict. Harmony
  (`polish-pass/SKILL.md:22,96`, `polish.md:24`): consistency-only, "does NOT
  judge whether a screen reads as a default template — that is the
  distinctiveness bar: pass/fail verdicts on rendered screens, executed by
  `browser-qa` ONLY". Scoring (`scoring.md:43,54,55,56,59`): Level/Score are
  internal anchors, "not a pass/fail verdict on a rendered screen"; the
  template-look cap at 6 applies "only on `browser-qa`'s generic-template
  verdict, never on the tell count alone".
- **Fix #13i blocking item (B1, spot-checked).** Snapshot exclusion present
  in both engines (orchestrate 5b / standalone 6b: "copy the whole tree,
  except `.hackathon/` and `.hallmark/candidate-evidence.md`"); the
  `fresh-verdict rounds used: 0/2` creation line is present once in each
  engine; the duplicated "after the run, the orchestrator records
  `fresh-verdict rounds used: N/2`" sentence is 0 hits in both engines.
- **GAN harness.** `gan-style-harness/SKILL.md:118`: "Screen distinctiveness
  is NOT scored here… judged ONLY by `browser-qa`… A screen that reads as a
  default template is a browser-qa finding, not a rubric deduction." Both
  `gan-build.md` and `gan-design.md` require the scoping note at the top of
  every rubric and repair it before scoring. `gan-build.md:84` "**Result:**
  PASS/FAIL" in the build-report template is a weighted-score loop outcome
  (score vs `--pass-threshold`, with failing tests capping below threshold),
  not a rendered-screen distinctiveness verdict — same class as the
  adjudicated loop/code-review acceptance verdicts.

## Other areas verified clean

- **Distinctiveness bar wording (both engines).** `orchestrate:193,195`,
  `orch-build-mvp:40,49`, `orch-change-feature:36`, `orch-fix-defect:36`,
  `orch-refine-code:35`: every "reads as a default template" failure is
  expressly "on `browser-qa`'s verdict", with the reviewer checking only the
  recorded direction. `browser-qa/SKILL.md:68` confirms it is the sole
  executor and reads `.hallmark/candidate-evidence.md` as candidate evidence,
  "never as a verdict".
- **"Is a template / reads as a template" declaratives.** Zero bare
  declarations that a page IS a template. Every hit routes to candidate
  evidence (orchestrate :193/:195, standalone :49, Taste :314, review-hero
  :11, review-finish :9/:13/:15, polish.md :49, scoring.md :56, critique
  :142, design-system :56, web-design-quality.mdc :19) or is unrelated
  (email draft template, MCP config template).
- **Design-system slop scope** (`design-system/SKILL.md:56`): "pattern
  evidence, not a distinctiveness verdict… judged ONLY by `browser-qa`".
- **ui-ux-pro-max bars** (`:14` captivating bar, `:91` anti-generic bar):
  both headed "(design guidance, not a screen verdict)"; "Only
  `browser-qa`'s pass/fail verdict on the rendered screen decides… this
  skill never states a screen pass/fail."
- **redesign.md:40**: "so the linter does not write the verdict"; `:56,81`
  "Floor 14 FAIL · Reflex 9" are example sloplint counts in a redesign
  record, not verdicts. `hallmark-floor.md:63,67`: Specificity scoped as
  candidate evidence; `:72` "would pass the gates" is a craft-axis
  (Execution) score descriptor, not a screen verdict.
- **frontend-slides** (`SKILL.md:26`): "avoid generic purple-gradient,
  Inter-on-white, template-looking decks" — design guidance only.
- **rules/**: no verdict wording beyond `web-design-quality.mdc:17–19`
  ("Design guidance, not a ship verdict… This rule never decides whether a
  surface ships… only `browser-qa`'s pass/fail verdict on the rendered
  screen decides template-ness"). All other `rules/` grep hits are false
  positives from substrings (`password`, `bypass`).
- **commands/**: `quality-gate.md` is a formatter check only (no screen
  verdict). `checkpoint.md` "Build: [PASS/FAIL]" and `code-review.md`
  "Record pass/fail for each" are build/code-check statuses. `astra-review`,
  `learn-eval`, `santa-loop`, `flutter-review` verdicts are code/doc review
  gates, not rendered-screen distinctiveness verdicts.
- **"ship"/"rebuild" in design contexts**: `gate.mjs --done` "ship it as it
  is" is the user's words, not a verdict (Taste :296, gate.md :94).
  Rebuild-a-surface rules route verification to `browser-qa`'s visual loop.
  `review-finish.md:5` explicitly "not a ship/fix/rebuild verdict".
  `production-audit` ship/block recommendation is an app-readiness audit
  (adjudicated class), not a screen-distinctiveness verdict.
- **"judge" in design contexts**: "judge stop and stare" is the
  hackathon-scope wow-test metaphor; Taste :301 "A FAIL you judge false is
  waived" is a checker-grade waiver decision (adjudicated sloplint-grade
  class); `hackathon-scope` "judges" are the human hackathon judges.
- **Scripts**: `consistency.mjs` / `perf.mjs` / `photos.mjs` PASS/FAIL/WARN
  values are mechanical layout/perf check grades, scoped by Taste :283 and
  `perf.md:10` ("WebGL off is a proxy, not a verdict") as non-distinctiveness
  checks. `gate.mjs:789` "// the verdict" is the section that prints the
  `GATE:` line — part of the adjudicated Taste gate below.

## Checked and deliberately NOT flagged (adjudicated design)

- **gates.md §6 ship rule** (`gates.md:18` grades "FAIL (Floor, nothing
  ships)" and `:247` "**Nothing ships with an open `FAIL` or an open
  `REFLEX`.**"). Adjudicated: sloplint check grades, static/render grades
  not verdicts, with the "Nothing ships with an open FAIL/REFLEX" pattern.
  **Literal-reading note (as instructed):** read literally, a rule that
  conditions shipping on non-`browser-qa` FAIL/REFLEX grades is a ship
  verdict issued by something other than `browser-qa`, and would be up for
  re-adjudication if the adjudication were reopened. Not flagged; left as
  adjudicated.
- **Taste gate** (`design-taste-frontend/SKILL.md:287–316`,
  `references/gate.md:3,66–97,116–130`, `scripts/gate.mjs` incl. `:789`).
  The finish gate runs the checker in a real browser (1440/390, 320
  overflow walk, copy-lint) and renders `GATE: PASS` / `GATE: FAIL <n>` /
  `GATE: OPEN`, with FAILs blocking finish ("A build is not finished while
  the checker still finds a FAIL it could fix", "Fix what it lists and run
  it again until its last line is `GATE: PASS`"). Adjudicated — not flagged.
  **Literal-reading note:** read literally, this is a pass/fail verdict on a
  rendered screen issued by a checker other than `browser-qa` (layout,
  copy, overflow, tap-size FAILs block the build), and would be up for
  re-adjudication if the adjudication were reopened. The gate's own scope
  notes (Taste :283: layout findings "fail the page on layout-correctness
  grounds", "not a distinctiveness verdict") keep it inside the adjudicated
  reading: it verdicts layout/copy correctness, not distinctiveness.
- **Loop/code-review acceptance verdicts**: `loop-design-check`,
  `production-audit` (ship/block bands), `santa-method` / `santa-loop`
  (PASS/FAIL → NICE/NAUGHTY), `verification-loop`, `click-path-audit`
  (VERDICT: BUG), `delivery-gate`, orch-pipeline verification bullet,
  `council` verdicts, `skill-stocktake` Keep verdicts, `rules-distill`
  verdicts, `feature-expansion` proposal verdicts, `repo-scan` four-level
  verdicts — all code/process/doc acceptance, not rendered-screen
  distinctiveness verdicts. Not flagged.
- **gates.md §5 descriptive clauses** (38iii, 63, 65, 67): describe a
  pattern class in general terms ("the most common machine-made head", "the
  punctuation of generated pages", "the most recognised generated look")
  rather than declaring this page IS a template. Not flagged.
- **polish.md Step 5.9 independent re-score gate** (`polish.md:56`): the
  Score is explicitly an internal anchor (`scoring.md:43,54,59`), not a
  pass/fail verdict. Not flagged.
- **OpenMontage `runtime-fetch.md` unpinned clone**: documented opt-in, out
  of scope per task. Not checked, not flagged.

## What remains

Nothing. No blocking findings, no minor findings. The sweep loop is clean
after fix #13i; no further fix round is indicated by this sweep. The only
open items are the two adjudicated literal-reading notes above (gates.md §6
ship rule, Taste gate), which are recorded here for the parent's awareness
and are NOT findings unless the parent reopens those adjudications.
