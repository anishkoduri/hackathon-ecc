# Fix round #13e — Spec B (worker B)

Scope: Item 2 (BLOCKING — GAN rubric rows + rubric validation on every path) and
Item 11 (minor — `claude -p` residue). All targets are upstream ECC files with no
staged source; every spec below is a **build.sh patch** against the built-tree file.
No spec adds a gate, wait point, user question, or new skill/agent/rule/command.
Weights (Design 0.3 / Originality 0.2 / Craft 0.3 / Functionality 0.2) and the 7.0
PASS/FAIL threshold are unchanged throughout.

Reframing applied to every NEW text: browser-qa is the SOLE executor of pass/fail
verdicts on rendered screens. Everything else scores the recorded direction and its
code-level application only, or is worded as candidate evidence / design guidance.

Anchor verification: every OLD block below was counted with `python3 str.count()`
against its target file before writing; each occurs exactly once (count = 1).

---

## 2a — Rubric rows rewritten to score direction + code only — hackathon-ecc/skills/gan-style-harness/SKILL.md [build.sh patch]

Re-trace: `skills/gan-style-harness/SKILL.md:120-130` confirmed. Parent citations
correct: `:121` reads `- 1-3: Generic, template-like, "AI slop" aesthetics` and
`:127` reads `- 1-3: Default colors, stock layouts, no personality`. The scoping
note at `:118` already exists, but the 1-3 rows contradict it by scoring screen
genericness directly. Decision: REWRITE the rows (not append a deferral) — see
Decisions at the end. All 8 Design Quality / Originality rows are rewritten so
each scores only whether a direction is recorded and how it is applied in code.

Anchor check: old text occurs exactly 1 time in the target file.

OLD (verbatim, in a code fence):
```
### Design Quality (weight: 0.3)
- 1-3: Generic, template-like, "AI slop" aesthetics
- 4-6: Competent but unremarkable, follows conventions
- 7-8: Distinctive, cohesive visual identity in the recorded direction and its code-level application — screen distinctiveness itself is judged ONLY by browser-qa, never here
- 9-10: Could pass for a professional designer's work

### Originality (weight: 0.2)
- 1-3: Default colors, stock layouts, no personality
- 4-6: Some custom choices, mostly standard patterns
- 7-8: Clear creative vision, unique approach in the recorded direction — screen distinctiveness itself is judged ONLY by browser-qa, never here
- 9-10: Surprising, delightful, genuinely novel
```

NEW (verbatim, in a code fence):
```
### Design Quality (weight: 0.3)
- 1-3: No named direction recorded, or tokens, type, and spacing in the code do not trace to any recorded direction
- 4-6: A direction is recorded but only partly applied in code — some tokens, type, or spacing trace to it, the rest do not
- 7-8: Direction recorded and applied in code — tokens, type, and spacing trace to it coherently across the app
- 9-10: Direction recorded and applied with professional-level craft in code — tokens, type, and spacing trace to it consistently, including edge states

### Originality (weight: 0.2)
- 1-3: Code-level choices do not trace to the recorded direction — defaults throughout, no direction-specific decisions in code
- 4-6: Some code-level choices trace to the recorded direction, most do not
- 7-8: Clear creative direction recorded and applied in code — direction-specific choices in tokens, type, and spacing throughout
- 9-10: Direction recorded and applied in code in a surprising, inventive way — direction-specific choices throughout, including details and edge states
```

---

## 2b — Evaluator key behaviors: template-ness wording removed — hackathon-ecc/skills/gan-style-harness/SKILL.md [build.sh patch]

Re-trace: `skills/gan-style-harness/SKILL.md:102-103` confirmed. `:103`
(`Originality — Custom decisions vs. template/AI patterns?`) scores template-ness
in the evaluator's key behaviors, outside the rubric rows. `:102` is reworded
with it so the pair reads as one code-level criterion.

Anchor check: old text occurs exactly 1 time in the target file.

OLD (verbatim, in a code fence):
```
  1. **Design Quality** — Does it feel like a coherent whole?
  2. **Originality** — Custom decisions vs. template/AI patterns?
```

NEW (verbatim, in a code fence):
```
  1. **Design Quality** — Is the recorded direction applied coherently in code (tokens, type, and spacing trace to it)?
  2. **Originality** — Do the code-level choices trace to the recorded direction rather than defaults?
```

---

## 2c — Anti-pattern #1: penalties scoped to code-level only — hackathon-ecc/skills/gan-style-harness/SKILL.md [build.sh patch]

Re-trace: `skills/gan-style-harness/SKILL.md:251` confirmed:
`1. **Evaluator too lenient** — If the evaluator passes everything on iteration 1,
your rubric is too generous. Tighten scoring criteria and add explicit penalties
for common AI patterns.` The "explicit penalties for common AI patterns" instruction
would otherwise re-admit screen-genericness penalties through the back door.

Anchor check: old text occurs exactly 1 time in the target file.

OLD (verbatim, in a code fence):
```
1. **Evaluator too lenient** — If the evaluator passes everything on iteration 1, your rubric is too generous. Tighten scoring criteria and add explicit penalties for common AI patterns.
```

NEW (verbatim, in a code fence):
```
1. **Evaluator too lenient** — If the evaluator passes everything on iteration 1, your rubric is too generous. Tighten scoring criteria and add explicit penalties for common AI patterns (code-level direction-application failures only — never screen distinctiveness, which is judged ONLY by `browser-qa`).
```

---

## 2d — Planner agent: validate the rubric it writes before handoff — hackathon-ecc/agents/ecc-gan-planner.md [build.sh patch]

Re-trace: `agents/ecc-gan-planner.md:107` (Process step 4) confirmed. #13d
verification: this writer DOES carry the deferral requirement — the sentence
already requires the scoping note at the top of `eval-rubric.md`. What is missing
is the validation step: the planner never re-reads what it wrote. This spec adds
the re-read-and-repair check at the writer, before handoff.

Anchor check: old text occurs exactly 1 time in the target file.

OLD (verbatim, in a code fence):
```
4. Also write a concise `gan-harness/eval-rubric.md` with the evaluation criteria in a format the Evaluator can consume directly — and include the screen-distinctiveness scoping note at its top (copy it from `gan-style-harness` SKILL.md's rubric: screen distinctiveness is NOT scored here; it is judged ONLY by `browser-qa` in the visual loop). Every rubric this agent writes must carry that deferral.
```

NEW (verbatim, in a code fence):
```
4. Also write a concise `gan-harness/eval-rubric.md` with the evaluation criteria in a format the Evaluator can consume directly — and include the screen-distinctiveness scoping note at its top (copy it from `gan-style-harness` SKILL.md's rubric: screen distinctiveness is NOT scored here; it is judged ONLY by `browser-qa` in the visual loop). Every rubric this agent writes must carry that deferral. Before handing off, re-read `gan-harness/eval-rubric.md` and confirm the scoping note is at its top; if it is missing, prepend it — never hand off a rubric without it.
```

---

## 2e — orch-build-mvp step 4: validate the rubric it writes before driving the loop — hackathon-ecc/skills/orch-build-mvp/SKILL.md [build.sh patch]

Re-trace: `skills/orch-build-mvp/SKILL.md:38-39` confirmed. Parent citation `:38`
is the translate-into-`spec.md` + `eval-rubric.md` bullet; the deferral
requirement itself is on `:39`. #13d verification: this writer DOES carry the
deferral requirement. Missing: the validation step before the loop starts. This
spec adds it to the same sentence (anchor is the deferral sentence on `:39`).

Anchor check: old text occurs exactly 1 time in the target file.

OLD (verbatim, in a code fence):
```
The `eval-rubric.md` you write must carry the screen-distinctiveness scoping note at its top (copy it from `gan-style-harness` SKILL.md's rubric — screen distinctiveness is NOT scored here; it is judged ONLY by `browser-qa` in the visual loop) — every rubric written on any path must carry that deferral.
```

NEW (verbatim, in a code fence):
```
The `eval-rubric.md` you write must carry the screen-distinctiveness scoping note at its top (copy it from `gan-style-harness` SKILL.md's rubric — screen distinctiveness is NOT scored here; it is judged ONLY by `browser-qa` in the visual loop) — every rubric written on any path must carry that deferral. Before driving `/gan-build`, re-read `gan-harness/eval-rubric.md` and confirm the scoping note is at its top; if it is missing, prepend it — never start the loop on a rubric without it.
```

---

## 2f — gan-build Phase 2: evaluator validates the rubric before scoring (covers --skip-planner) — hackathon-ecc/commands/gan-build.md [build.sh patch]

Re-trace: `commands/gan-build.md:45-50` confirmed. Parent citation `:45` is the
evaluator launch; `:46` reads `- Read eval-rubric.md and spec.md` and `:49` reads
`- Score against rubric` — the evaluator reads the rubric as-is with no
validation. This is the unguarded `--skip-planner` / stale / hand-written rubric
path on the Cursor side: Phase 1 is skipped, so no writer runs. The validation
bullet is inserted between reading the rubric and testing the app, so it runs on
every iteration of every path that reaches Phase 2 (including gan-design, which
reuses Phase 2).

Anchor check: old text occurs exactly 1 time in the target file.

OLD (verbatim, in a code fence):
```
    - Read eval-rubric.md and spec.md
    - Test the live application (mode: playwright/screenshot/code-only)
```

NEW (verbatim, in a code fence):
```
    - Read eval-rubric.md and spec.md
    - Validate `gan-harness/eval-rubric.md` before scoring: confirm the screen-distinctiveness scoping note is at its top; if it is missing, prepend the note (copied from the `gan-style-harness` SKILL.md rubric) to the rubric file, record the repair in the feedback file, and score the Design Quality / Originality rows on the recorded direction and its code-level application only — never score screen distinctiveness.
    - Test the live application (mode: playwright/screenshot/code-only)
```

---

## 2g — gan-build Phase 1: name the --skip-planner rubric gap explicitly — hackathon-ecc/commands/gan-build.md [build.sh patch]

Re-trace: `commands/gan-build.md:22-23` confirmed. Parent citations `:9`
(`--skip-planner` — skip planner, assume spec.md already exists) and `:23-25`
(Phase 1 runs only unless `--skip-planner` is set; step 2 waits for the planner
to produce `spec.md` and `eval-rubric.md`) are correct. With `--skip-planner` no
rubric is written on this path at all — this spec states that on the Phase 1
header so the Phase 2 validation in spec 2f is the named guard for that path.

Anchor check: old text occurs exactly 1 time in the target file.

OLD (verbatim, in a code fence):
```
### Phase 1: Planning (Planner Agent)
Unless `--skip-planner` is set:
```

NEW (verbatim, in a code fence):
```
### Phase 1: Planning (Planner Agent)
Unless `--skip-planner` is set (with `--skip-planner`, no rubric is written here — the existing `gan-harness/eval-rubric.md` is used as-is and is validated in Phase 2 before any scoring):
```

---

## 2h — gan-harness.sh planner prompt: add the deferral requirement (fourth writer, missing it) — hackathon-ecc/scripts/gan-harness.sh [build.sh patch]

Re-trace: `scripts/gan-harness.sh:209-218` confirmed. #13d verification finding:
this rubric writer does NOT carry the deferral in its own text. The planner
prompt at `:214-216` says only `2. gan-harness/eval-rubric.md — Evaluation
criteria for the Evaluator`; it inherits the requirement only indirectly via
`:210` (`Read the agent definition in agents/ecc-gan-planner.md for your full
instructions`), which points at the planner agent file that does carry it
(spec 2d). That indirect inheritance is the gap — the prompt itself must state
it. This spec makes the deferral explicit in the prompt.

Anchor check: old text occurs exactly 1 time in the target file.

OLD (verbatim, in a code fence):
```
2. gan-harness/eval-rubric.md — Evaluation criteria for the Evaluator
```

NEW (verbatim, in a code fence):
```
2. gan-harness/eval-rubric.md — Evaluation criteria for the Evaluator. Put the screen-distinctiveness scoping note at the top of eval-rubric.md (copy it from the gan-style-harness skill's rubric: screen distinctiveness is NOT scored here; it is judged ONLY by browser-qa in the visual loop) — every rubric written on any path must carry that deferral.
```

---

## 2i — gan-harness.sh Phase 1: validate the rubric on the --skip-planner path — hackathon-ecc/scripts/gan-harness.sh [build.sh patch]

Re-trace: `scripts/gan-harness.sh:203-204` confirmed. Parent citation correct:
`:203` is `if [ "$SKIP_PLANNER" = "true" ] && [ -f "${HARNESS_DIR}/spec.md" ]; then`
and `:204` is `phase "PHASE 1: Planning — SKIPPED (spec.md exists)"`. Nothing
here checks `eval-rubric.md` at all. This spec adds the shell-side validation:
if the rubric file exists but lacks the scoping note, prepend the note and log
the repair; if no rubric file exists, warn (no gate, no halt — the run proceeds
and the evaluator prompt validation in spec 2j is the second guard).

Anchor check: old text occurs exactly 1 time in the target file.

OLD (verbatim, in a code fence):
```
if [ "$SKIP_PLANNER" = "true" ] && [ -f "${HARNESS_DIR}/spec.md" ]; then
  phase "PHASE 1: Planning — SKIPPED (spec.md exists)"
```

NEW (verbatim, in a code fence):
```
if [ "$SKIP_PLANNER" = "true" ] && [ -f "${HARNESS_DIR}/spec.md" ]; then
  phase "PHASE 1: Planning — SKIPPED (spec.md exists)"
  # Rubric validation (screen-distinctiveness deferral): a skipped planner means
  # the rubric on disk may be stale or hand-written. If it does not carry the
  # scoping note, prepend it and log the repair — the evaluator never scores
  # screen distinctiveness.
  if [ ! -f "${HARNESS_DIR}/eval-rubric.md" ]; then
    warn "No gan-harness/eval-rubric.md found — nothing to validate; the evaluator will score only against the criteria in its own prompt."
  elif ! grep -q "Screen distinctiveness is NOT scored here" "${HARNESS_DIR}/eval-rubric.md"; then
    { printf '%s\n\n' "**Screen distinctiveness is NOT scored here.** Whether a named direction is recorded AND visibly applied on the rendered screens is judged ONLY by \`browser-qa\` in the visual loop — never by this evaluator. The Design Quality and Originality rows below score the recorded direction and its code-level application only."; cat "${HARNESS_DIR}/eval-rubric.md"; } > "${HARNESS_DIR}/eval-rubric.md.tmp" && mv "${HARNESS_DIR}/eval-rubric.md.tmp" "${HARNESS_DIR}/eval-rubric.md"
    warn "eval-rubric.md lacked the screen-distinctiveness scoping note — prepended it before scoring."
  fi
```

---

## 2j — gan-harness.sh evaluator prompt: validate the rubric before scoring — hackathon-ecc/scripts/gan-harness.sh [build.sh patch]

Re-trace: `scripts/gan-harness.sh:272-288` confirmed. The evaluator invocation
at `:272` (`claude -p --model "$EVALUATOR_MODEL"`) tells the evaluator at `:280`
to `Read gan-harness/eval-rubric.md for scoring criteria` and at `:284` to
`Score against the rubric (1-10 per criterion)` — with no validation between
reading and scoring. This spec inserts the validation as step 1a, numbered so
the existing steps 2–6 need no renumbering. This is the shell-path enforcement
point, mirroring spec 2f on the Cursor path.

Anchor check: old text occurs exactly 1 time in the target file.

OLD (verbatim, in a code fence):
```
1. Read gan-harness/eval-rubric.md for scoring criteria
2. Read gan-harness/spec.md for feature requirements
```

NEW (verbatim, in a code fence):
```
1. Read gan-harness/eval-rubric.md for scoring criteria
1a. Validate the rubric before scoring: confirm gan-harness/eval-rubric.md carries the screen-distinctiveness scoping note at its top ("Screen distinctiveness is NOT scored here" — judged ONLY by browser-qa); if it does not, prepend that note to the rubric file, note the repair in your feedback file, and score the Design Quality / Originality rows on the recorded direction and its code-level application only — never score screen distinctiveness.
2. Read gan-harness/spec.md for feature requirements
```

---

## 2k — Evaluator agent Step 1: validate the rubric before scoring (enforcement point on every path) — hackathon-ecc/agents/ecc-gan-evaluator.md [build.sh patch]

Re-trace: `agents/ecc-gan-evaluator.md:43-48` confirmed (Step 1: Read the Rubric).
Parent citation note: `commands/gan-build.md` has only 104 lines, so the `:112`
cited in the task is this file's `:112` — `Score each criterion on a 1-10 scale.
Use the rubric in `gan-harness/eval-rubric.md`.` — not a line in gan-build.md.
The evaluator is the actual scorer on every path (Cursor subagent via gan-build
and gan-design, and the shell prompt in gan-harness.sh), so its Step 1 is the
single enforcement point that covers all paths including any direct launch. This
spec adds the validation there, in addition to (not instead of) the three
path-level validations in specs 2d/2e/2f/2i/2j.

Anchor check: old text occurs exactly 1 time in the target file.

OLD (verbatim, in a code fence):
````
### Step 1: Read the Rubric
```
Read gan-harness/eval-rubric.md for project-specific criteria
Read gan-harness/spec.md for feature requirements
Read gan-harness/generator-state.md for what was built
```
````

NEW (verbatim, in a code fence):
````
### Step 1: Read the Rubric
```
Read gan-harness/eval-rubric.md for project-specific criteria
Read gan-harness/spec.md for feature requirements
Read gan-harness/generator-state.md for what was built
Validate gan-harness/eval-rubric.md before scoring: confirm it carries the screen-distinctiveness scoping note at its top; if it does not, prepend the note (copied from the gan-style-harness skill's rubric) to the rubric file, record the repair in your feedback file, and score the Design Quality / Originality rows on the recorded direction and its code-level application only — never score screen distinctiveness.
```
````

---

## 2l — gan-design :36: correct the false assertion — hackathon-ecc/commands/gan-design.md [build.sh patch]

Re-trace: `commands/gan-design.md:36` confirmed, verbatim as the parent cited:
the loop bullet claims `the evaluator scores against `eval-rubric.md`, which
carries that deferral`. That assertion was false on the gan-design path itself
(no validation existed between writing the rubric at Setup step 3 and scoring)
and false for any stale/hand-written rubric. Decision: REWORD the assertion to
be true (conditional on the Setup step-3 validation in spec 2m) rather than
deleting it — see Decisions at the end.

Anchor check: old text occurs exactly 1 time in the target file.

OLD (verbatim, in a code fence):
```
- Evaluator prompt emphasizes "would this win a design award?" over "do all features work?" — but screen distinctiveness is NOT judged here: whether a named direction is recorded AND visibly applied is judged ONLY by `browser-qa` in the visual loop; the evaluator scores against `eval-rubric.md`, which carries that deferral.
```

NEW (verbatim, in a code fence):
```
- Evaluator prompt emphasizes "would this win a design award?" over "do all features work?" — but screen distinctiveness is NOT judged here: whether a named direction is recorded AND visibly applied is judged ONLY by `browser-qa` in the visual loop; the evaluator scores against `eval-rubric.md` only after the Setup step-3 validation confirms it carries that deferral (a rubric without the deferral is repaired before scoring — see Setup step 3).
```

---

## 2m — gan-design Setup step 3: validate the rubric before the loop starts — hackathon-ecc/commands/gan-design.md [build.sh patch]

Re-trace: `commands/gan-design.md:19` (Setup step 3) confirmed. #13d verification:
this writer DOES carry the deferral requirement (the rubric must include the
scoping note at its top). Missing: the validation step — the loop starts
immediately after Setup with no re-read. This spec adds the validation, which is
what makes the reworded `:36` assertion in spec 2l true.

Anchor check: old text occurs exactly 1 time in the target file.

OLD (verbatim, in a code fence):
```
3. Write a design-focused `gan-harness/eval-rubric.md` with extra weight on Design Quality and Originality — and include the screen-distinctiveness scoping note at its top (copy it from `gan-style-harness` SKILL.md's rubric: screen distinctiveness is NOT scored here; it is judged ONLY by `browser-qa` in the visual loop). Every rubric written on any path must carry that deferral.
```

NEW (verbatim, in a code fence):
```
3. Write a design-focused `gan-harness/eval-rubric.md` with extra weight on Design Quality and Originality — and include the screen-distinctiveness scoping note at its top (copy it from `gan-style-harness` SKILL.md's rubric: screen distinctiveness is NOT scored here; it is judged ONLY by `browser-qa` in the visual loop). Every rubric written on any path must carry that deferral. Validate it before the loop starts: re-read `gan-harness/eval-rubric.md` and confirm the scoping note is at its top; if it is missing, prepend it — never start the loop on a rubric without it.
```

---

## 11a — :30 "When NOT to Use" line: scope the claude -p reference — hackathon-ecc/skills/gan-style-harness/SKILL.md [build.sh patch]

Re-trace: `skills/gan-style-harness/SKILL.md:30` confirmed, verbatim as the
parent cited: `- Quick single-file fixes (use standard `claude -p`)` — unscoped,
unlike the `Via Claude Code (Manual)` section note at `:181`. Truth per #13d:
the GAN loop runs in Cursor; only the upstream `claude -p` CLI path does not
run in Cursor.

Anchor check: old text occurs exactly 1 time in the target file.

OLD (verbatim, in a code fence):
```
- Quick single-file fixes (use standard `claude -p`)
```

NEW (verbatim, in a code fence):
```
- Quick single-file fixes (Claude Code only — use standard `claude -p` there; in this plugin use the Cursor agent loop, never `claude -p`)
```

---

## 11b — Manual section heading: scope it in the heading itself — hackathon-ecc/skills/gan-style-harness/SKILL.md [build.sh patch]

Re-trace: `skills/gan-style-harness/SKILL.md:179` confirmed: `### Via Claude Code
(Manual)`. The `:181` note already scopes the section, but the heading itself
does not — a reader skimming headings can miss the note. This spec scopes the
heading to match the `:181` note.

Anchor check: old text occurs exactly 1 time in the target file.

OLD (verbatim, in a code fence):
```
### Via Claude Code (Manual)
```

NEW (verbatim, in a code fence):
```
### Via Claude Code (Manual — Claude Code only, never executed in this plugin)
```

---

## 11c — Manual section commands: scope each claude -p command in place — hackathon-ecc/skills/gan-style-harness/SKILL.md [build.sh patch]

Re-trace: `skills/gan-style-harness/SKILL.md:183-196` confirmed. Parent citations
correct: runnable `claude -p --model sonnet …` commands at `:185` (Planner),
`:188` (Generator), `:191` (Evaluator), `:194` (Generator). The `:181` note
already says these commands are NOT executed in this plugin, but the commands
themselves carry no scope marker. This spec adds a scope comment directly above
each command (commands kept verbatim — upstream documentation, not deleted).

Anchor check: old text occurs exactly 1 time in the target file.

OLD (verbatim, in a code fence):
```
```bash
# Step 1: Plan
claude -p --model sonnet "You are a Product Planner. Read PLANNER_PROMPT.md. Expand this brief into a full product spec: 'Build a Kanban board app'. Write spec to spec.md"

# Step 2: Generate (iteration 1)
claude -p --model sonnet "You are a Generator. Read spec.md. Implement Sprint 1. Start the dev server on port 3000."

# Step 3: Evaluate (iteration 1)
claude -p --model sonnet --allowedTools "Read,Bash,mcp__playwright__*" "You are an Evaluator. Read EVALUATOR_PROMPT.md. Test the live app at http://localhost:3000. Score against the rubric. Write feedback to feedback-001.md"

# Step 4: Generate (iteration 2 — reads feedback)
claude -p --model sonnet "You are a Generator. Read spec.md and feedback-001.md. Address all issues. Improve the scores."

# Repeat steps 3-4 until pass threshold met
```
```

NEW (verbatim, in a code fence):
```
```bash
# Step 1: Plan
# Claude Code only — never executed in this plugin; upstream documentation only.
claude -p --model sonnet "You are a Product Planner. Read PLANNER_PROMPT.md. Expand this brief into a full product spec: 'Build a Kanban board app'. Write spec to spec.md"

# Step 2: Generate (iteration 1)
# Claude Code only — never executed in this plugin; upstream documentation only.
claude -p --model sonnet "You are a Generator. Read spec.md. Implement Sprint 1. Start the dev server on port 3000."

# Step 3: Evaluate (iteration 1)
# Claude Code only — never executed in this plugin; upstream documentation only.
claude -p --model sonnet --allowedTools "Read,Bash,mcp__playwright__*" "You are an Evaluator. Read EVALUATOR_PROMPT.md. Test the live app at http://localhost:3000. Score against the rubric. Write feedback to feedback-001.md"

# Step 4: Generate (iteration 2 — reads feedback)
# Claude Code only — never executed in this plugin; upstream documentation only.
claude -p --model sonnet "You are a Generator. Read spec.md and feedback-001.md. Address all issues. Improve the scores."

# Repeat steps 3-4 until pass threshold met
```
```

---

## 11d — gan-harness.sh :2 header: state the loop truth — hackathon-ecc/scripts/gan-harness.sh [build.sh patch]

Re-trace: `scripts/gan-harness.sh:2` confirmed: `# Claude Code only — this script
shells out to 'claude -p' and 'claude mcp'; it will not run in a Cursor-only
install with no 'claude' CLI.` The parent citation is correct, and the header
already states the Claude-Code-only truth — it does not state the other half of
the truth (the plugin's GAN loop runs in Cursor via `/gan-build` and never
executes this script). This spec appends that half. Script is NOT deleted.

Anchor check: old text occurs exactly 1 time in the target file.

OLD (verbatim, in a code fence):
```
# Claude Code only — this script shells out to 'claude -p' and 'claude mcp'; it will not run in a Cursor-only install with no 'claude' CLI.
```

NEW (verbatim, in a code fence):
```
# Claude Code only — this script shells out to 'claude -p' and 'claude mcp'; it will not run in a Cursor-only install with no 'claude' CLI. The plugin's GAN loop runs in Cursor via /gan-build and never executes this script; this script is the upstream Claude Code invocation path only.
```

---

## Decisions (Item 2)

1. **Rubric rows: REWRITE, not append-a-deferral.** The 1-3 rows as written ARE
   the screen verdict ("Generic, template-like"; "Default colors, stock layouts");
   appending a deferral next to a contradictory row leaves the rubric
   self-contradictory. Rewriting all 8 Design Quality / Originality rows to score
   only direction-recorded + code-level trace removes the contradiction at the
   source. Weights (0.3 / 0.2) and the 7.0 PASS/FAIL threshold are unchanged.
2. **Validation failure behavior: ADD THE NOTE (prepend + record in feedback;
   score code-level only), not refuse-the-dimension.** Refusing the Design /
   Originality dimension would make PASS unreachable (those two criteria are
   50% of the weighted score) and would halt the loop — a de facto gate.
   Prepending the note keeps the numeric gate and the loop intact with no wait,
   no user question, and no halt; the repair is recorded in the feedback file
   so it is visible, and the evaluator still never scores screen distinctiveness.
3. **gan-design :36: REWORD the assertion to be true (conditional on Setup
   step-3 validation + repair), not deleted.** Once spec 2m's validation runs,
   the claim "the rubric carries that deferral" is true on the gan-design path;
   rewording keeps the design-mode loop's guidance accurate without removing it.

## #13d writer verification (Item 2b)

All three #13d rubric writers DO carry the deferral requirement in the built
tree — grep for the scoping note confirms each:
- `agents/ecc-gan-planner.md:107` — carries it (Process step 4).
- `skills/orch-build-mvp/SKILL.md:39` — carries it (step 4).
- `commands/gan-design.md:19` — carries it (Setup step 3).

One further writer does NOT carry it in its own text (found by this re-trace):
- `scripts/gan-harness.sh:209-218` (planner prompt) — no deferral in the prompt
  itself; it inherits the requirement only indirectly via `:210` ("Read the
  agent definition in agents/ecc-gan-planner.md for your full instructions").
  Fixed by spec 2h.

## Checked, not changed

- `skills/gan-style-harness/SKILL.md:118` — scoping note already states the
  reframing correctly; the rows are fixed to match it.
- `skills/gan-style-harness/SKILL.md:132-142` — Craft / Functionality rows:
  checked all 8 bands; none touches template-ness (broken layouts, rough
  spacing, missing states, broken/missing features); left as-is.
- `skills/gan-style-harness/SKILL.md:145-149` — Scoring: weighted sum, 7.0
  threshold, max 15 iterations; numeric gate preserved per the task.
- `skills/gan-style-harness/SKILL.md:25` — "Any task where 'AI slop' aesthetics
  are unacceptable" (When to Use): use-case line, not a scored verdict.
- `skills/gan-style-harness/SKILL.md:181` — manual-section note already scopes
  the `claude -p` commands correctly (NOT executed; loop runs in Cursor).
- `skills/gan-style-harness/SKILL.md:3` — frontmatter description already scoped
  (upstream `claude -p` path is Claude Code only; loop runs in Cursor).
- `skills/gan-style-harness/SKILL.md:263-273` — Results table ("Generic AI slop"
  vs "Distinctive, polished"): Anthropic published-results summary, not a
  verdict issued by this plugin's loop.
- `agents/ecc-gan-planner.md:39-43` — Design Direction template ("unique design
  elements that prevent AI-slop aesthetics"): direction content for the spec,
  not a screen verdict.
- `agents/ecc-gan-planner.md:66-79` — spec-template Evaluation Criteria
  ("What makes this app's design 'good'?", "What would make this feel
  unique?"): prompts for the rubric writer, governed by the Process step 4
  deferral requirement (spec 2d), not scored rows.
- `agents/ecc-gan-evaluator.md:31` — "DO penalize heavily for AI-slop
  aesthetics as the rubric allows — code-level application of the recorded
  direction only … never as screen distinctiveness": already scoped.
- `agents/ecc-gan-evaluator.md:94` — "AI-slop indicators as the rubric allows …
  code-level evidence only, never a screen-distinctiveness verdict": already
  scoped.
- `agents/ecc-gan-evaluator.md:116` — scoring calibration 4-5 band already
  carries "(screen distinctiveness is not scored here — that is `browser-qa`'s
  alone)".
- `agents/ecc-gan-evaluator.md:153` and `commands/gan-build.md:82-84` — feedback
  / report "Verdict: PASS / FAIL (threshold: 7.0)": the weighted-score loop
  gate, not a screen-distinctiveness verdict; preserved.
- `commands/gan-design.md:21-29` — design-rubric weights block (0.35 / 0.30 /
  0.25 / 0.10) and weight note: weights only, no rows, no verdict language.
- `agents/ecc-gan-generator.md:3`, `agents/ecc-gan-evaluator.md:3`,
  `agents/ecc-gan-planner.md:3` — agent frontmatter descriptions already scoped
  (Cursor subagents; upstream `claude -p` path is Claude Code only, never
  executed here).
- `scripts/gan-harness.sh:106,145,268` — `claude mcp get playwright` references
  inside the script: covered by the `:2` header scope (spec 11d); no separate
  change.

## Separate finding — `claude -p` outside the GAN skill + script (Item 11 grep)

Tree-wide grep for `claude -p` found these occurrences outside
`skills/gan-style-harness/SKILL.md` and `scripts/gan-harness.sh`. None of them
is executed by the plugin's Cursor loop; no spec written for them (out of this
item's scope — reported for the parent to disposition):

- `scripts/lib/llm-summary.js:151+` — `generateSessionSummary` spawns
  `claude -p`; called from `scripts/hooks/session-end.js:15` and
  `scripts/hooks/pre-compact.js:18`. GUARDED: it skips the spawn when the
  `claude` CLI binary is absent ("not running under Claude Code") and callers
  fall back to mechanical extraction — so in a Cursor-only install it does NOT
  execute.
- `skills/plankton-code-quality/SKILL.md:3,37` — spawns `claude -p`
  subprocesses; documented Claude Code only, "no Cursor equivalent". Executes
  only if that skill is invoked under Claude Code.
- `skills/skill-comply/SKILL.md:3,13` — runs `claude -p`; documented Claude
  Code only, "no Cursor equivalent".
- `skills/continuous-learning-v2/agents/observer-loop.sh:401` — `claude --print`
  (same CLI, not `-p`); dormant by default, guards on binary presence,
  documented Claude Code only ("has no Cursor equivalent").
- `scripts/hooks/session-end.js:210` — comment only, no invocation.
- `agents/ecc-gan-generator.md:3`, `agents/ecc-gan-evaluator.md:3`,
  `agents/ecc-gan-planner.md:3` — frontmatter documentation of the upstream
  path, already scoped, never executed.
- `scripts/gan-harness.sh:209,249,272` — the script's own `claude -p`
  invocations; the script itself is Claude-Code-only per its `:2` header
  (spec 11d) and is never executed by the Cursor loop.

Conclusion: no `claude -p` invocation is actually executed by the plugin in
Cursor. The only live execution paths are the guarded/dormant/documented
Claude-Code-only ones above.

## Blocked / held back

- **Missing-rubric-file case under `--skip-planner`:** if `gan-harness/eval-rubric.md`
  does not exist at all, spec 2i only warns — no rubric can be validated or
  repaired, and creating a default rubric from scratch in the script would need
  the skill's default rubric text. Same gap on the Cursor path if the evaluator
  is launched with no rubric file. Not specced: fixing it would be new
  failure/generation behavior beyond this item. Parent to decide (fail the run
  vs. generate the default rubric vs. leave as warned).
- **Parent citation correction:** `commands/gan-build.md` has only 104 lines,
  so the task's `:112` ("the evaluator reads it as-is") is
  `agents/ecc-gan-evaluator.md:112`, not a line in gan-build.md. No spec was
  held back by this; spec 2k targets that line's Step 1 context.
- Nothing else held back. All 17 specs have unique anchors (count = 1 each,
  verified by `python3 str.count()` before writing).
