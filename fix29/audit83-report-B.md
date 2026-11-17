# Audit #83-B — Fix #29 (brief / verify coherence + verifier, round 4)

- **Date:** Mon Nov 16, 2026
- **Auditor scope (Auditor B):** verify every audit #82-B finding (82-B1–82-B2) against the built tree; hunt for new brief/verify gaps with fresh eyes; audit the verifier (`fix29/verify29.py`, re-run independently); harness honesty (B13 rejection re-check). Read-only; no file under `~/workspace/hackathon-plugin/` was edited except this report.
- **Sources read in full:** `fix29/SPEC.md`, `fix29/MANIFEST.md` (including §3 "Audit #82 fixes"), `fix29/audit80-report-A.md`, `fix29/audit80-report-B.md`, `fix29/audit81-report-A.md`, `fix29/audit81-report-B.md`, `fix29/audit82-report-A.md`, `fix29/audit82-report-B.md`, `fix29/verify29.py` (§7c/7d/7e, §10i gan checks, the new 82-B1/82-B2 checks at :1425–1437), the built routing text in `commands/gan-build.md` (whole file), `skills/gan-style-harness/SKILL.md` (:14, :69, :155), `fix16/fix16.py` (`sub()` :51–60, hackathon-mode anchor :3807–3809, `main()` exit :4274–4280), `build.sh` (:23222 fix16 run).
- **Verifier re-run by this auditor:** `python3 fix29/verify29.py` → **258/258, exit 0** (confirmed independently, not taken from the coordinator's log).

## Verdict: NOT PASS — 0 blocking, 1 minor

Both #82-B findings are verified fixed in substance, with exact file:line evidence below: the GAN generator launch block now carries real Verification-steps and Return-format slots (82-B1), and verify29 now asserts the GAN wiring order with unique anchors, demonstrated to fail if the step moves (82-B2). The one new finding is a verifier weakness in the same presence-not-position class as 82-B2, one step removed: the new 82-B1 checks assert the two field lines exist *in the file*, not *in the GENERATE block*, and the Verification-steps check asserts only a prefix of the line — I demonstrated both false-passes by moving/truncating the line in a scratch copy (the tree was not touched). The live text is correct, so this is minor, not blocking.

---

## #82-B disposition — every finding re-checked

| #82-B | Status | Evidence |
|---|---|---|
| 82-B1 (minor): GAN generator launch block still 5/7 — no Verification steps or return-format slot | **VERIFIED-FIXED** | `commands/gan-build.md:46` now carries `- Verification steps: run the TDD tests you wrote plus the acceptance criteria from the spec — paste the test output; the build must pass and the acceptance criteria must hold before finishing.` and `:47` carries `- Return format: Status first, then files changed, test output, concerns.` Both sit inside the GENERATE block (`# GENERATE` :38 → `# Wait for generator` :49), verified by index arithmetic on the file text (block start 5492 < VS 6447 < RF 6645 < block end 6728). Both read as real slots, not labels on unrelated text: the Verification line names the procedure (run the TDD tests + the spec's acceptance criteria, paste the output) and the pass condition (build must pass, criteria must hold before finishing); the Return line names the return shape (status first, then files changed, test output, concerns), mirroring the mechanical template. Verify29 asserts both (`verify29.py:1434–1437`, see false-pass hunt below). |
| 82-B2 (minor, verifier): GAN wiring checks assert presence, not order | **VERIFIED-FIXED** | `verify29.py:1429–1430`: `check("ORCHESTRATOR-CHECK sits between EVALUATE and CHECK SCORE (audit #82-B2)", _gb.index("# EVALUATE") < _gb.index("# ORCHESTRATOR-CHECK") < _gb.index("# CHECK SCORE"))`. The three anchors are unique in the file — `# EVALUATE` 1× (:51), `# ORCHESTRATOR-CHECK` 1× (:62), `# CHECK SCORE` 1× (:65) — so `.index()` (first occurrence) cannot match a wrong line, and the comparison is non-vacuous: live indices 6764 < 7648 < 8484. The two bare prose mentions ("skip CHECK SCORE", "continues to CHECK SCORE", :63) carry no `#` prefix, so they cannot satisfy the `# CHECK SCORE` anchor. Demonstrated the check would fail if the step moved: relocating the whole ORCHESTRATOR-CHECK step (comment line + prose) to after the CHECK SCORE header makes the comparison `False`. The planner-spec check remains position-pinned by its `3a.` numbering, as #82-B noted. |

---

## New findings

### 83-B1 — MINOR (verifier) — the new 82-B1 checks assert file-presence, not in-block position, and the Verification-steps check is prefix-only (82-B2 class, one step removed)

**Evidence.**

- `verify29.py:1434–1437`:
  - `check("... generator block carries Verification steps (audit #82-B1)", _gb.count("    - Verification steps: run the TDD tests you wrote plus the acceptance criteria from the spec") == 1)`
  - `check("... generator block carries Return format (audit #82-B1)", _gb.count("    - Return format: Status first, then files changed, test output, concerns.") == 1)`
  Both are whole-file substring counts on `_gb` (`commands/gan-build.md`). Neither slices the GENERATE block, so neither asserts the lines sit between `# GENERATE` and `# Wait for generator`.
- Demonstrated false-pass (i), position: moving the Verification-steps line out of the GENERATE block into the EVALUATE block (same file, same text) leaves the asserted count at 1 — the check still passes while the generator's dispatch text no longer carries the slot and the evaluator's block wrongly does. The same holds for the Return-format line (whole-file count, no block slice).
- Demonstrated false-pass (ii), prefix: the Verification-steps assertion covers only the first ~90 characters of the line. Deleting the operative tail (` — paste the test output; the build must pass and the acceptance criteria must hold before finishing.`) leaves the asserted count at 1 — the check passes on a line that no longer states the verification procedure or the pass condition, i.e. exactly the "label on unrelated text" failure the audit task asked the check to exclude. The Return-format assertion does not have this weakness (it asserts the full line, ending period included).

**Why it matters.** 82-B2 was filed precisely because order/position is the property that matters for the GAN wiring, and this audit's tasking asked the same question of the 82-B1 checks ("do the asserted strings appear exactly once and in the GENERATE block, or could another occurrence satisfy them?"). Today they appear exactly once and in the block — there is no live false-pass, and the live lines are real slots (see 82-B1 above). But the checks as written cannot see a move or a truncation, so a later edit could silently re-open 82-B1 while verify29 stays green. The consequence is lower than 82-B2's (a moved line mislabels a slot; it does not silently disable a verification step, since the loop wiring is separately asserted), hence minor, not blocking.

**Fix.** Scope both 82-B1 checks to the GENERATE slice — e.g. extract `_gen = _gb[_gb.index("# GENERATE"):_gb.index("# Wait for generator")]` and assert the counts inside `_gen` — and assert the full Verification-steps line (through "must hold before finishing.") instead of the prefix. One verifier-only change; no tree change needed.

---

## Verifier false-pass hunt — the NEW checks, each tested

- **82-B2 order assertion (`verify29.py:1429–1430`).** Anchors unique (1× each, :51/:62/:65); live order correct (6764 < 7648 < 8484); move-test demonstrated the comparison goes `False` when the step is relocated after CHECK SCORE. The `.index()` first-occurrence semantics are safe here precisely because each anchor occurs once. **Holds.**
- **82-B1 field checks (`verify29.py:1434–1437`).** The asserted strings occur exactly once each in the whole file *and* inside the GENERATE block today (`gan-build.md:46–47`), and whole-tree grep confirms no other file carries either string — so no *other* occurrence can satisfy them right now. But the checks themselves are whole-file counts, not block-scoped, and the VS check is a prefix: demonstrated to pass after a block move and after a tail truncation (see 83-B1). **Holds today; weak as written.**
- **82-A2 cap alignment (checked because the task names it).** No verifier check or skill mirror line still states the old cap of one: `"at most one correction"` / `"one correction re-dispatch"` return **0 hits** in the built tree, in `verify29.py`, and in `fix29.py`. `commands/gan-build.md:30` now reads "(at most two correction re-dispatches, per the plugin's 2-round fix-loop convention; …)". The skill mirror lines (`gan-style-harness/SKILL.md:69`, `:155`) carry no cap number, and verify29's planner-spec assertion (`verify29.py:1427–1428`) asserts only the step's presence string, not a number — so no check needed a cap update and none carries a stale one. **Holds.**

---

## Fresh hunt — new brief/verify gaps

- **Unbounded assume/proceed, whole tree:** `"state the assumption you made and proceed"` **0×**; `"use your judgment"` / `"use your judgement"` **0×** in `skills/` + `rules/` + `commands/` + `agents/`; `"instead of NEEDS_CONTEXT"` **0×** in the same dirs. `"state the assumption"` **11 hits in exactly the 6 known bounded files** (`skills/orchestrate/SKILL.md` :221 orchestrator-level hard rule; `skills/orchestrate/references/dispatch-prompt.md` ×4 bounded first-build carve-outs; `agents/deep-reasoner.md:17` bounded; `skills/polish-pass/SKILL.md` ×3 + `skills/polish-pass/reference/impeccable-critique.md:216` + `skills/systematic-debugging/SKILL.md:93` pass-runner carve-outs) — same file set as #82-B, no new site. `"pick the reasonable option"` **5 lines, all carved + tie-breaker** (`orch-pipeline:72`, `feature-expansion:151`, `orch-build-mvp:70`, `dispatch-prompt.md:34`, `:92`). No new unbounded language found.
- **Every fix loop constructs a correction brief naming the failed criterion:** feature-expansion fix loop (`:158`), orch-pipeline Phase 5 Review (`:74`), orchestrate escalation ladder step 1 (`:252`), gan-build ORCHESTRATOR-CHECK (`:63`) + planner-spec check 3a (`:30`). orch-build-mvp step 6 inherits via Phase 5 Review (routes Verify through "orch-pipeline Phase 5 (Review)"). The only other re-dispatch sites are NEEDS_CONTEXT re-dispatches (supply the missing context, re-dispatch the same tier), which are not failure paths and correctly carry no correction brief. **All fix loops construct the brief.**
- **Orchestrator-level assumption language, re-checked:** `orchestrate:221` (hard rule — stated assumptions for trivial/reversible work, high-stakes irreversibles wait/escalate) remains an orchestrator move, not a drone instruction. Clean.

---

## Field-coverage table — updated from #82-B

Legend: ● = present as a distinct field/slot · ◐ = present only by prose assertion, pointer, reference, or merged/implicit · ○ = absent.

| Skill / brief | Goal | Files IN | Files OUT | Constraints | Acceptance criteria | Verification steps | What to return |
|---|---|---|---|---|---|---|---|
| orchestrate contract core (`SKILL.md:227`) | ● | ● (exact paths) | ● | ● | ● | ● | ● |
| dispatch-prompt recon / mechanical / reasoning templates | ● | ● | ● | ● | ● | ● | ● |
| dispatch-prompt worked example (:210–221) | ● | ● | ● | ● | ● | ● | ● |
| dispatch-prompt second-pass template (exempt, opinion) | ◐ (Task) | ○ | ○ | ● | ○ | ○ | ● (opinion format) — carries a NEEDS_CONTEXT line |
| dispatch-prompt blind-reviewer template (exempt, verification gate) | ● | ● (acceptance criteria only) | ● | ● | ○ ("n/a — you are the check") | ● | ● — 6/7 formal; the acceptance-check slot is the gate itself by design |
| hackathon-mode (rule; block :45) | ● (block states all 7) | ● | ● | ● | ● | ● | ● — requirement text only; a rule, not a format |
| orch-pipeline (:62) | ◐ paragraph + reference to dispatch-prompt contract | ◐ | ◐ | ◐ | ◐ | ◐ | ◐ |
| orch-build-mvp (:13 pointer + :70 step 4) | ◐ via pointer; step-4 briefs use feature-expansion's format (● per that format) | ◐ | ◐ | ◐ | ◐ | ◐ | ◐ |
| orch-add-feature / orch-change-feature / orch-fix-defect (:13) | ◐ via pointer | ◐ | ◐ | ◐ | ◐ | ◐ | ◐ |
| orch-refine-code (:13 pointer; :35 step 2) | ◐ via pointer; step-2 sweep brief names all 7 inline ● | ◐ / ● (step 2) | ◐ / ● (step 2) | ◐ / ● (step 2) | ◐ / ● (step 2) | ◐ / ● (step 2) | ◐ / ● (step 2) |
| feature-expansion (format :143–152) | ● item 1 | ● item 2 | ● item 2 | ● item 3 | ● item 4a | ● item 4b | ● item 9 |
| gan-style-harness (:14) | ◐ paragraph + reference | ◐ | ◐ | ◐ | ◐ (rubric, not brief criteria) | ◐ | ◐ |
| gan generator brief (`commands/gan-build.md` GENERATE block :38–47) | ◐ (brief/spec) | ◐ (read spec.md + tokens) | ● | ◐ (TDD + commit lines) | ◐ (spec's criteria, referenced in the Verification line) | ● (:46) — **now present** | ● (:47) — **now present** |
| gan evaluator block (`commands/gan-build.md` EVALUATE :51–58) | ◐ | ◐ (rubric + spec) | ○ | ◐ | ◐ (rubric) | ◐ (runs live app + tests, unlabeled) | ◐ (writes feedback file, unlabeled) |
| design-taste-frontend redesign (`redesign.md:68`) | ● (paragraph enumeration) | ● | ● | ● | ● | ● | ● — paragraph list, not a fill-in template |
| common-agents.mdc (:26, covered by reference) | ◐ (factory line; defers to block) | ◐ | ◐ | ◐ | ◐ | ◐ | ◐ |

**Answer to the task's question:** the GAN generator launch block is now **7/7 present** (was 5/7 in #82-B — the two ○ fields are now ●), but only **3 of the 7 are distinct labeled slots** (Files OUT, Verification steps, Return format). Goal, Files IN, Constraints, and Acceptance criteria remain reference-carried via `spec.md` — the spec *is* the goal and the acceptance criteria for this drone, and the planner-spec check (3a) verifies the spec against the brief before Phase 2. That is the same structural property #82-B already recorded (◐ on those four fields), not a new gap: the 82-B1 prescribed fix was exactly the two missing lines, and both are in. No finding filed on the reference-carried fields.

Net vs round 3: **six formats now carry all 7 fields as distinct slots** (contract core, three dispatch-prompt implementation templates, feature-expansion format, worked example, redesign paragraph enumeration — unchanged), and the GAN generator block joins them as **7/7 present** (3 labeled + 4 reference-carried). Remaining below 7/7 present: the blind reviewer (6/7 formal, acceptance-check-by-design), the second-pass template (exempt, opinion-only), the GAN evaluator block (no files-out slot; verification/return unlabeled — unchanged, not a generator-brief field), and everything carried only by paragraph assertion or reference.

---

## Harness honesty — B13 rejection re-checked and confirmed

The coordinator's rejection of the 80-B13 sync fix is **correct**, verified end to end by this auditor:

- `fix16/fix16.py:3807–3809` anchors on the staged wording: `sub(os.path.join(BASE, "rules/hackathon-mode.mdc"), "(its upstream \`claude -p\` invocation path does not run in Cursor", "(its upstream CLI-subprocess invocation path does not run in Cursor")` — default `count=1` (`sub()` def, `fix16.py:51–60`: on mismatch it appends to `ERRORS` and returns False).
- `fix16.py:4274–4280`: `main()` returns `1 if ERRORS else 0`, `sys.exit(main())` — a missed anchor fails the run.
- `build.sh:23222` runs `python3 "$PLUGIN_ROOT/fix16/fix16.py" "$PLUGIN_DIR"` on every build (last build step). Syncing staged `hackathon-mode.mdc:38` to the built text would make the anchor match 0× → `ERRORS` non-empty → exit 1 → build fails. (Manifest cites `:3807`; the `sub(` call is on line 3807 and the anchor string itself on line 3808 — the one-line citation nit from #81-B/#82-B stands, substance unchanged.)
- `fix29.py` and `fix29/fix29.py.template` are byte-identical (`diff -q` clean) — no drift in the fix script itself.

---

## Checked and clean

- **Verifier re-run:** 258/258, exit 0, re-run independently.
- **GLOBAL-ROUTING block:** md5s match #80-A/#81-A/#82-A (orchestrate `bdf1720f69f9b50e3791a14c68f5c5ea`, hackathon-mode `39a22e9247be839a841ffbea3ad19918`).
- **All five "pick the reasonable option" copies carved + tie-breaker** (whole-tree grep: exactly 5 lines — `orch-pipeline:72`, `feature-expansion:151`, `orch-build-mvp:70`, `dispatch-prompt.md:34`, `dispatch-prompt.md:92`).
- **"instead of NEEDS_CONTEXT": 0 hits** in the whole built tree. **"drop fields that are genuinely N/A": 0 hits** tree-wide (verified by this auditor's grep).
- **"use your judgment" / "use judgement": 0 hits** in `skills/`, `rules/`, `commands/`, `agents/`.
- **`agents/fast-worker.md:16` and `agents/scout.md` are clean** — fast-worker says the opposite of guessing; scout says "a bounded honest map beats an unbounded guess".
- **Polish-pass / systematic-debugging carve-outs re-checked, no finding:** `polish-pass/SKILL.md:38,76,97`, `impeccable-critique.md:216`, `systematic-debugging/SKILL.md:93` govern the pass runner's own routing decisions in orchestrator context (or enumerate safe defaults), not drone brief instructions — same reading as #81-B/#82-B, unchanged by the round-4 edits.
- **Correction briefs constructed in all four fix loops** (feature-expansion, orch-pipeline Phase 5, orchestrate ladder, gan ORCHESTRATOR-CHECK + planner-spec check) — see fresh hunt above.
- **82-A2 cap alignment holds:** no "at most one correction" / "one correction re-dispatch" anywhere in the built tree, `verify29.py`, or `fix29.py`; `gan-build.md:30` states two; skill mirrors carry no cap number.
- **Counts unchanged:** 67 skills / 45 agents / 48 rules / 55 commands / 15 hooks / 49 triggers (verify29 checks 1–5 pass in the independent 258/258 run).
- **Model pins unchanged:** no `deepseek/` or `qwen/` slugs; `DeepSeek`/`Qwen` names only in the two GLOBAL-ROUTING blocks (verify29 9b passes).

## Grep counts (for the record)

- `"pick the reasonable option"` whole built tree: **5** lines (all carved + tie-breaker).
- `"state the assumption you made and proceed"`: **0** tree-wide.
- `"state the assumption"` whole built tree: **11** — `dispatch-prompt.md` ×4 (bounded first-build carve-outs), `orchestrate/SKILL.md:221` (orchestrator-level hard rule), `agents/deep-reasoner.md:17` (bounded), `polish-pass/SKILL.md` ×3 + `polish-pass/reference/impeccable-critique.md:216` + `systematic-debugging/SKILL.md:93` (pass-runner carve-outs).
- `"instead of NEEDS_CONTEXT"`: **0**.
- `"use your judgment"` / `"use your judgement"`: **0** in `skills/` + `rules/` + `commands/` + `agents/`.
- `"correction brief"` in `skills/` + `rules/` + `commands/`: **13 occurrences** — GLOBAL-ROUTING block ×2 (`orchestrate:36`, `hackathon-mode:45`), routing paragraphs ×4 (`orch-pipeline:62`, `feature-expansion:139`, `gan:14`, `redesign.md:68`), fix-loop constructions ×7 (`feature-expansion:158`, `orch-pipeline:74`, `orchestrate:252`, `gan-style-harness:69` + `:155`, `gan-build.md:30` (3a) + `:63`).
- `"When in doubt"` (tie-breaker form): **7** sites (5 Belief copies + preamble short form + governing first-build carve-out); 4 further hits are unrelated (`python-patterns:751`, `security-review:511`, `ecc-code-reviewer.md:313`, `ecc-healthcare-reviewer.md:88`).
- `"Verification steps"` in `dispatch-prompt.md`: **6** (skeleton, recon, mechanical, reasoning, blind reviewer, worked example); `"files out of scope"`: **6** (same six sections).
- `"a rubric pass at or above 7.0 with a failed acceptance criterion is a fail"`: **3** in `gan-style-harness/SKILL.md` (:14, :69, :155); **4** in the built tree (+ `gan-build.md:63`).
- `"at most one correction"` / `"one correction re-dispatch"`: **0** (tree, verify29, fix29.py).
- `"The evaluator pass IS the verify step for GAN work"`: **0** (old substitution gone).
- GAN wiring anchors in `commands/gan-build.md`: `# EVALUATE` **1×** (:51), `# ORCHESTRATOR-CHECK` **1×** (:62), `# CHECK SCORE` **1×** (:65); live order indices 6764 < 7648 < 8484.
- 82-B1 asserted strings in `commands/gan-build.md`: `Verification steps` line **1×** (:46), `Return format` line **1×** (:47), both inside the GENERATE block (:38–49).
- `fix29.py` == `fix29/fix29.py.template` (byte-identical).
