# Fix #23 §9 disposition — Dynamic interface

Worker W-§9. Scope: SPEC §9 only. No bundle, no commit, no push.
`build.sh` NOT run, NOT edited (still 23,940 lines, md5
`536235ac5d34caf473646fd4452ba8a5` — the post-fix23 §1–§6 integration
baseline). The built tree was read-only for counting/anchor
verification. `fix23/apply-w1.py` … `apply-w4.py` NOT re-run.
`fix11/fix11-stage.py` not re-run. Prior verifiers not edited.
`~/workspace/cursor-skills/less-flat-ui` not edited (read-only; D-A2).
No /demo wiring or DEMOGATE token touched. `apply-s9.py` itself was NOT
run (integration runs it); verification was `py_compile` + an in-memory
simulation of the subs against the current built tree + `compile()` of
the rendered block, all read-only.

## Files changed / created by W-§9

| File | Change |
|---|---|
| `fix23/apply-s9.py` | NEW — inserts the §9 runtime-patch block into build.sh before `# STEP 5 — Counts` (integration runs it; W-§9 did NOT run it) |
| `fix23/orch-lines-s9.py` | NEW — one string constant `ORCH_LINES_S9`, the exact design-package-step lines for integration to insert into staged orchestrate SKILL.md |
| `fix23/polish-lines-s9.py` | NEW — one string constant `POLISH_LINES_S9`, the exact dynamic-story candidate-evidence sentence for integration to insert into staged polish-pass SKILL.md |
| `fix23/disposition-s9.md` | This file |

No staged skill file was edited directly by W-§9: orchestrate and
polish-pass lines live in the `*-lines-s9.py` payload files for
integration to insert mechanically.

## §9 vs §2 vs §5 — no duplication (stated in the lines themselves)

- §2 (MOTION_F23, W1) is the motion-PRESENCE rule: deliberate,
  eye-catching motion on every build, routed through the fix #22
  tokens. A build that feels static fails.
- §9 (DYNAMIC_F23, this section) is the STATE-CHANGE and
  INTERACTIVITY rule: WHAT changes, WHAT triggers it, HOW it moves —
  plus that controls respond immediately and surfaces show live state.
  A state change with no motion is a gap; a control that does not
  respond is a gap.
- §5 (FUNC_F23, W3) is the FUNCTIONALITY-SHOWING rule: the design
  shows HOW it works. §9 notes live data IS the functionality showing
  and does not restate it.
- Each §9 add-text cross-references MOTION_F23 / FUNC_F23 instead of
  restating them. The §2 motion-default rule is not duplicated anywhere
  in §9 text.

## Per-item placement table

Status: new = W-§9 wrote new text; covered = already present, cited as
pointer.

| SPEC §9 item | Placement (file + anchor token) | Status |
|---|---|---|
| Live and reactive: surfaces show live state (data updating, statuses changing, counts and totals moving), not frozen mock content | `apply-s9.py` DYNAMIC-02 (`skills/motion-patterns/SKILL.md`, `## Decision Guidance`, DYNAMIC_F23); DYNAMIC-BQA-01 (Phase 2 step 6, DYNAMIC_F23); `orch-lines-s9.py` ORCH_LINES_S9 (DYNAMIC_F23); `polish-lines-s9.py` POLISH_LINES_S9 (DYNAMIC_F23) | new |
| Interactive elements respond immediately: press states, hover, transitions, state changes | DYNAMIC-02 (press scale 0.97, hover, transitions); DYNAMIC-BQA-01 (confirms immediate response live); ORCH_LINES_S9 | new |
| Motion as behavior, not decoration: every state change choreographed (motion tokens, dealt moments) — entering/leaving, loading to loaded, empty to filled, selected, confirmed | DYNAMIC-01 (`skills/motion-foundations/SKILL.md`, `## Decision Guidance`, DYNAMIC_F23); DYNAMIC-03 (`skills/motion-advanced/SKILL.md`, DYNAMIC_F23); DYNAMIC-BQA-01; ORCH_LINES_S9 | new |
| A state change with no motion is a gap | DYNAMIC-01, DYNAMIC-02, DYNAMIC-03, DYNAMIC-BQA-01 (FAIL), ORCH_LINES_S9 | new |
| Interactive depth: sortable, filterable, expandable, draggable where it serves the job; the user can DO things, not just look | DYNAMIC-02; DYNAMIC-03 (drag/reorder/dismiss/swipe); DYNAMIC-BQA-01 (sort/filter/expand/drag live); ORCH_LINES_S9; POLISH_LINES_S9 (handlers check) | new |
| Decision record states the dynamic story per surface: what changes, what triggers it, how it moves | ORCH_LINES_S9 (design-package step, DYNAMIC_F23); POLISH_LINES_S9 (reads the story from the decision record); DYNAMIC-BQA-01 (reads the story to know what to check) | new |
| Placement — design-package step | `orch-lines-s9.py` ORCH_LINES_S9, inserted after the HERO/FUNC paragraph in step 3 (DYNAMIC_F23) | new |
| Placement — motion skills | DYNAMIC-01/02/03 in the three motion skills (DYNAMIC_F23) | new |
| Placement — QA checks; browser-qa verifies state changes LIVE (interacts, confirms response); controls that do not respond, or states that change without motion, FAIL | DYNAMIC-BQA-01 (Phase 2 step 6, live check + FAIL); DYNAMIC-BQA-02 (Output Format Interactions row, DYNAMIC_F23) | new |
| Calibration: dynamic never means gratuitous; motion serves the state change; reduced-motion fallback stays complete | DYNAMIC-01/02/03 (each carries the complete-fallback line); ORCH_LINES_S9 (calibration sentence) | new |
| Works with §2 (motion), §4 (hero moments), §5 (functionality made visible) | ORCH_LINES_S9 + `apply-s9.py` header (cross-references, no restatement) | new |
| Reduced-motion fallback (standing rule) | DYNAMIC-01/02/03 (state still changes, content correct at rest, complete fallback, never broken); ORCH_LINES_S9 | covered (standing rule, restated as the fallback line in each §9 sub, not a new rule) |
| "More, not bolder" / anti-derivative / D19 seven dimensions / browser-qa sole verdict executor / static self-hosted fonts | Unchanged by §9; DYNAMIC-01/02/03 and ORCH_LINES_S9 each carry a full seven-dimension D19 line; `apply-s9.py` block header states browser-qa remains the sole verdict executor | covered |

## Runtime patches (`fix23/apply-s9.py` → build.sh block before `# STEP 5 — Counts`)

Each sub is (id, rel-path, old-anchor, add-text, mode). All anchors
verified count==1 against the CURRENT built tree (post-§1–§6
integration) by grep before the script was written, and re-verified by
in-memory simulation after writing; the block re-asserts count==1 at
build time and fails loudly. Idempotency guard: the script refuses if
its marker comment (`# --- fix23 §9: dynamic interface (DYNAMIC_F23) ---`)
is already in build.sh. The script was NOT run (integration runs it).
`py_compile` passed; the rendered block compiles; marker absent from
build.sh; `# STEP 5 — Counts` count==1.

| Sub | Target (built tree) | Anchor (count==1) | Mode | Token |
|---|---|---|---|---|
| DYNAMIC-01 | `skills/motion-foundations/SKILL.md` | `## Decision Guidance` | after | DYNAMIC_F23 |
| DYNAMIC-02 | `skills/motion-patterns/SKILL.md` | `## Decision Guidance` | after | DYNAMIC_F23 |
| DYNAMIC-03 | `skills/motion-advanced/SKILL.md` | `## Decision Guidance` | after | DYNAMIC_F23 |
| DYNAMIC-BQA-01 | `skills/browser-qa/SKILL.md` | Phase 2 step-5 block (`5. Test critical user journeys (checkout, onboarding, search)` + its 2 continuation lines) | after | DYNAMIC_F23 |
| DYNAMIC-BQA-02 | `skills/browser-qa/SKILL.md` | `- [✓] Auth flow: login/logout working` | after | DYNAMIC_F23 |

Fresh-anchor note (no collisions with W1–W4): W1's MOTION-01–03 sit
after `## Rules` in the three motion skills — §9 anchors on
`## Decision Guidance` instead. W2's BQA-TYPEAUDIT sits after the
distinctiveness sentence, W3's HERO-BQA_F23 after the "Never claim
visual verification..." sentence and FUNC-BQA_F23 after Phase 3 step 4,
W4's ALIGN_F23-A–E after the Phase 3 heading / step 1 / step 3 /
verdict line / Visual example row — §9 anchors on the Phase 2 step-5
block and the Interactions auth-flow row instead.

## Orchestrate insertion (`fix23/orch-lines-s9.py`)

- Constant: `ORCH_LINES_S9` — the dynamic-story paragraph for step 3.
- Insertion point: staged `new-skills/orchestrate/SKILL.md`, step 3,
  immediately AFTER the HERO/FUNC paragraph's closing D19 line
  (`Depth: the moment's and the mechanism's layer order, or `flat by
  choice — <reason>`.)` — verified count==1) and immediately BEFORE
  `**Two-pass briefing for UI slices:**` (count==1). Mode: after.
- NOTE: W1's integration anchor comment
  (`<!-- F23-ORCHESTRATE-EXTENSIONS: ... -->`) is NO LONGER in the
  staged file — integration consumed it inserting the W2/W3/W4 lines —
  so this file names the HERO/FUNC paragraph's closing line instead.

## Polish-pass insertion (`fix23/polish-lines-s9.py`)

- Constant: `POLISH_LINES_S9` — the dynamic-story candidate-evidence
  sentence. A polish-pass line FITS (the dynamic story is statically
  checkable in code: live-state wiring, control handlers, motion
  tokens per state change), so the file exists — it is not omitted.
- Insertion point: staged `round2-skills/polish-pass/SKILL.md`, step
  5's trailing paragraph, immediately AFTER the type-audit sentence
  (full sentence verified count==1). Mode: after.
- Standing: candidate evidence for `browser-qa`, never a verdict
  (screen-verdicts rule, fix #13e). Whether a control actually
  responds and a change is actually choreographed is browser-qa's live
  check alone (DYNAMIC-BQA-01).

## Verification done by W-§9

- Baseline re-checked: `build.sh` 23,940 lines, md5
  `536235ac5d34caf473646fd4452ba8a5` — unchanged after W-§9's work.
- All 5 runtime-patch anchors verified count==1 against the current
  built tree (grep preflight + in-memory simulation after writing, in
  list order); orch anchor count==1; polish anchor count==1.
- Anchors that did NOT resolve count==1: none. (One false alarm during
  verification: an orch-closing probe returned 0 only because shell
  quoting mangled the apostrophe/backtick in the probe string; the
  exact string re-checked via heredoc resolves count==1.)
- Banned terms (claude/codex/anthropic/opus/sonnet/haiku/composer-2.5,
  case-insensitive): 0 in all new text (SUBS add-texts, rendered
  block, ORCH_LINES_S9, POLISH_LINES_S9).
- Grok pins: no model pins in any §9 text; no bare
  `grok-4.6-high-fast` anywhere.
- `apply-s9.py`: `py_compile` OK; rendered block `compile()` OK;
  marker absent from build.sh; STEP 5 count==1.
- D19 seven dimensions stand (every §9 D19 line carries all seven:
  Motion / Theme / Texture / Visuals / Techniques / Colors / Depth);
  "more, not bolder" and anti-derivative untouched; browser-qa remains
  the sole verdict executor (stated in the block header; polish-pass
  line is candidate evidence only); /demo untouched.

## What W-§9 could NOT verify / open items for integration

- `apply-s9.py` was NOT run per instructions, so the block's insertion
  into `build.sh` and the resulting built tree are unverified until
  integration runs it (the block's own asserts are the check).
- `orch-lines-s9.py` / `polish-lines-s9.py` were NOT inserted per
  instructions (integration inserts them mechanically); the anchors
  are verified count==1 in the current staged files, but if
  integration inserts another worker's lines at the same points first,
  the anchor strings themselves are unaffected (they are full
  sentences/lines, not positional), so no re-verification should be
  needed — integration should still confirm count==1 at insert time.
- The §9 live check (DYNAMIC-BQA-01) assumes the harness can drive
  sort/filter/expand/drag interactions via the browser MCP; if a given
  harness cannot drive a particular interaction, the check records
  that as an unverified interaction (a gap to note), never a silent
  pass — the text does not yet say this explicitly, and the parent may
  want it added at audit time.
