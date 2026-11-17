# Audit #81-B — Fix #29 (brief / verify coherence + verifier, round 2)

- **Date:** Mon Nov 16, 2026
- **Auditor scope (Auditor B):** verify every audit #80-B finding (80-B1–80-B15) against the built tree; hunt for new brief/verify gaps; audit the verifier (`fix29/verify29.py`, re-run independently); harness honesty (B13 rejection re-check). Read-only; no file under `~/workspace/hackathon-plugin/` was edited except this report.
- **Sources read in full:** `fix29/SPEC.md`, `fix29/MANIFEST.md`, `fix29/audit80-report-A.md`, `fix29/audit80-report-B.md`, `fix29/verify29.py`, `fix29/fix29.py` (§1–§5, census §4); the built routing text in `skills/orchestrate/SKILL.md` (+ `references/dispatch-prompt.md`, contract core :227, step 4 :93, step 5 :94–100, Verification stage :240–300, escalation ladder :250), `rules/hackathon-mode.mdc`, `skills/orch-pipeline/SKILL.md`, `skills/feature-expansion/SKILL.md`, `skills/gan-style-harness/SKILL.md`, `skills/orch-build-mvp/SKILL.md`, `skills/orch-refine-code/SKILL.md`, `commands/gan-build.md`, `commands/orch-refine-code.md`, `rules/common-agents.mdc`, `skills/design-taste-frontend/references/hallmark/references/redesign.md`, `agents/deep-reasoner.md`, `agents/fast-worker.md`, `agents/scout.md`; `fix16/fix16.py` (`sub()` :51–60, hackathon-mode anchor :3808, `main()` exit :4274–4280); `build.sh` (:230 agents copy, :23222 fix16 run).
- **Verifier re-run by this auditor:** `python3 fix29/verify29.py` → **215/215, exit 0** (confirmed independently, not taken from the coordinator's log).

## Verdict: NOT PASS — 2 blocking, 6 minor

Round-1's paragraph-level fixes mostly landed: all five Belief copies are carved with the tie-breaker, the contract core carries all seven fields with a no-drop rule, the feature-expansion format carries all seven as items, the merge-order bridges are at all three sites, and the B13 rejection checks out. But the fix's central mechanism is still contradicted where it actually executes, in the same structural way round 1 found: the **named deep-reasoner — the primary reasoning drone — carries an unbounded "state the assumption you made and proceed" in its own operating contract** (`agents/deep-reasoner.md:17`), a file the verifier never looks at (81-B1); and the **GAN loop that actually runs terminates on the rubric score with no orchestrator verify step anywhere in its wiring** (`commands/gan-build.md:59-68`), so the round-1 B2 fix exists in the skill paragraph but not in the executed loop (81-B2). The remaining minors are the same pattern at smaller scale: the correction brief is still unconstructed in orchestrate's own verify loop (81-B3), the first-build carve-out's drone-side wording lacks its scope sentence and contradicts the reasoning template on who assumes (81-B4), the tie-breaker never reached the first-build texts (81-B5), the worked-example brief lacks Verification steps while the verifier's count check passes (81-B6), and the blind-reviewer exemption has no verification procedure behind it (81-B7) — plus the verifier scope gaps that let 81-B1 through (81-B8).

---

## Findings

### 81-B1 — BLOCKING — `agents/deep-reasoner.md:17` still instructs the named reasoning drone to assume-and-proceed, unbounded (80-B1/80-A2 class, missed by the verifier)

**Evidence.**

- `hackathon-ecc/agents/deep-reasoner.md:17`:
  > "- If the task is under-specified, **state the assumption you made and proceed** — do not stall on clarifying questions unless genuinely blocked."
- This is the verbatim phrase the 80-B1 fix removed from the dispatch-prompt reasoning template (`dispatch-prompt.md:141-142` in round 1). The reasoning template now says the opposite: "If under-specified: return NEEDS_CONTEXT naming exactly what is missing — do not guess."
- The role file is the drone's standing contract, not an aside. `dispatch-prompt.md:10-12`: "Named subagents (deep-reasoner / fast-worker / scout) already carry their operating contract as a system prompt"; `orchestrate/SKILL.md` "Two spawn forms": "Named: spawn a subagent by name — `deep-reasoner`, `fast-worker`, or `scout` — pins the model AND carries the role's operating contract as its system prompt." The dispatch-prompt preamble — where the NO-GUESSING bound now lives — is "ONLY on the general subagent fallback path and for the second deep-reasoner pass." So on the **named first pass, the primary reasoning path, the drone never sees the bound**; it sees only the role file's instruction to proceed on assumption.
- The staged source carries the identical line: `new-skills/orchestrate/agents/deep-reasoner.md:17`, copied verbatim by `build.sh:230` (`cp "$PLUGIN_ROOT/new-skills/orchestrate/agents/"*.md "$PLUGIN_DIR/agents/"`). No fix16 scrub touches it (no banned term involved).
- The verifier is blind to it twice over. `verify29.py:723-724` asserts `"state the assumption you made and proceed" not in _dp` — `_dp` is `dispatch-prompt.md` only. `verify29.py:641` (check 7c) greps `"pick the reasonable option"` over `skills` + `rules` with `--include=SKILL.md --include=*.mdc --include=dispatch-prompt.md` — `agents/` is not in the searched dirs at all. A whole-tree grep for the phrase returns exactly one hit outside `dispatch-prompt.md`: this line.

**Why it matters.** NO-GUESSING_F29 (`orchestrate/SKILL.md:36`) binds every drone: "A drone that hits a decision its brief leaves unspecified stops and returns the question to the orchestrator instead of guessing". The deep-reasoner is the drone that receives the under-specified work — architecture, complex debugging, hard trade-offs, "ambiguous specs" (role file :3, :13) — i.e. exactly the work where an unspecified decision is most likely. Its standing instruction is to state an assumption and proceed, with "unless genuinely blocked" as the only qualifier and no NO-GUESSING bound, no tie-breaker, no return-to-orchestrator path. The same drone therefore behaves oppositely by spawn form (named pass: assume-and-proceed; fallback/second pass: return NEEDS_CONTEXT). This is the round-1 80-A2 defect in a new file: the carve-out reached the orchestrator-side text and the template, but not the drone-facing contract that actually executes. The fast-worker role file proves the alternative was available: `agents/fast-worker.md:16` says "If a real **design decision** surfaces, or the spec is ambiguous enough that you'd have to guess at intent, **stop and return that** — do not invent an answer."

**Fix.** In the staged source `new-skills/orchestrate/agents/deep-reasoner.md:17`, append the identical NO-GUESSING bound + tie-breaker used at `orch-pipeline:72` / `feature-expansion:151` / `dispatch-prompt.md:34`, scoped the same way ("applies only to carrying out the briefed approach, never to a decision the brief leaves unspecified — … returned to the orchestrator as a question, not guessed. When in doubt which side an ambiguity falls on, return the question — a returned question is never a stall."). Extend verify29 check 7d with a tree-wide assertion (see 81-B8): the phrase `"state the assumption you made and proceed"` occurs 0× in the built tree outside the bounded first-build carve-outs, and every `"state the assumption"` occurrence is inside a bounded carve-out.

### 81-B2 — BLOCKING — the GAN loop that runs still terminates on the rubric score; the orchestrator verify step has no wiring in `commands/gan-build.md` (80-B2 paragraph-fixed, loop-not-fixed)

**Evidence.**

- `commands/gan-build.md:59-68` (Phase 2, CHECK SCORE — the loop's termination rule):
  > "Read feedback/feedback-{iteration}.md / Extract weighted total score / if score >= pass_threshold: Log "PASSED at iteration {iteration} with score {score}" / Break / if iteration >= 3 and score has not improved in last 2 iterations: Log "PLATEAU detected — stopping early" / Break"
  There is no step between EVALUATE and CHECK SCORE that checks the generator's output against the brief's acceptance criteria, no re-check of the evaluator's pass/fail call, and no correction brief. A rubric pass ≥ 7.0 breaks the loop before any acceptance-criteria evaluation can occur — the exact failure mode 80-B2 named ("a slice can score 7.0+ while failing its brief's acceptance criterion … and nothing in the skill catches it"), now relocated from the skill paragraph to the executed loop.
- Phase 1 has no planner-spec check either (`gan-build.md:24-31`): step 2 "Wait for it to produce `gan-harness/spec.md`", step 3 "Display the spec summary to the user", step 4 "Proceed to Phase 2". Step 0 is a design-direction check, not a spec-against-brief check. On the `--skip-planner` path the existing rubric "is validated in Phase 2 before any scoring" — validated for the screen-distinctiveness scoping note only, not against the brief.
- The skill's own loop wiring agrees with the command, not the paragraph: `gan-style-harness/SKILL.md` Architecture diagram (5–15 iterations, generator↔evaluator feedback loop, no orchestrator node), Scoring (:151–152: "Pass threshold = 7.0", "Max iterations = 15"), and `orch-build-mvp/SKILL.md:68`: "That command runs the `gan-generator` → `gan-evaluator` loop and writes `gan-harness/feedback/feedback-NNN.md` until the score passes or plateaus."
- What the paragraph does say is correct and complete — `gan-style-harness/SKILL.md:14`: "after each evaluator pass the orchestrator checks the generator's output against the brief's acceptance criteria (not just the rubric score — a rubric pass at or above 7.0 with a failed acceptance criterion is a fail), re-checks the evaluator's pass/fail call against the same criteria, and checks the planner's spec against the brief before the first generator pass; failed output goes back with a correction brief naming the failed criterion". The command's top pointer (`gan-build.md:11`) restates it. Neither states where in the loop it executes, what consumes the failure, or what the planner-spec failure path is.

**Why it matters.** The factory paragraph is the assertion; the Phase 2 pseudocode is the procedure an executor follows step by step. As written, the procedure cannot produce an orchestrator-against-acceptance-criteria verdict: the only verdict-producing step reads the rubric score. The correction-brief failure path therefore has no trigger, and no iteration budget (does a correction re-dispatch consume one of the 15 iterations? unstated), and a failed planner spec has no stated path at all (re-dispatch the planner with a correction brief? capped how?). Verify29 check 10i asserts the paragraph sentences and that the old substitution is gone (`"The evaluator pass IS the verify step for GAN work"` count 0 — verified gone tree-wide), but no check reads the loop pseudocode — so the verifier passes on a loop that still implements the substitution.

**Fix.** Add an ORCHESTRATOR-CHECK step to the Phase 2 pseudocode between EVALUATE and CHECK SCORE: after each evaluator pass the orchestrator checks the generator's output against the brief's acceptance criteria and re-checks the evaluator's pass/fail call; a rubric pass with a failed acceptance criterion is a fail — the generator is re-dispatched with a correction brief naming the failed criterion, consuming one iteration within `max_iterations`; a rubric fail the orchestrator finds actually passes the criteria is a re-check, not a loop exit. Add a planner-spec check step at the end of Phase 1 (before Phase 2; on the `--skip-planner` path, against the existing spec) with the same correction-brief failure path to the planner. Mirror the check in `gan-style-harness/SKILL.md`'s loop wiring (diagram + Scoring section), so the paragraph is not the only place it exists. Add a verify29 check asserting the ORCHESTRATOR-CHECK step in `commands/gan-build.md` (not just the paragraph sentences).

### 81-B3 — MINOR — orchestrate step 5's verify loop still constructs no correction brief, and the manifest's inheritance claim for step 5 is unsupported (80-B8 incomplete)

**Evidence.**

- Grep for `"correction brief"` in `skills/orchestrate/SKILL.md`: exactly **1** hit — inside the GLOBAL-ROUTING block (:36, the VERIFY-MERGE sentence). No correction-brief construction sentence exists in step 5 (:94–100), the Verification stage (:240–300), or the escalation ladder (:250).
- Grep for `"Phase 5 Review"` in `skills/orchestrate/SKILL.md`: **0** hits. `orch-pipeline` is mentioned only at :105 (Phase 6, Commit) and :279 (reviewer dispatch template). Step 5's verify path is orchestrate's own: "Verify steps 1–4b run per wave" (:100), the visual loop's "fix them", and the escalation ladder (:250): "`NEEDS_CONTEXT` is **not** a failure — supply the missing context and re-dispatch the same tier"; "fast-worker … misses the acceptance check twice … route the task to **deep-reasoner** with both failed attempts attached as evidence."
- MANIFEST §2(c)(7) claims: "(Orchestrate step 5 and orch-build-mvp step 6 route through orch-pipeline Phase 5 Review, so they inherit it.)" The second half holds: `orch-build-mvp/SKILL.md:72` says "6. **Verify — orch-pipeline Phase 5 (Review) + expansion Phase 5**", and orch-pipeline's Phase 5 fix loop now constructs the brief (`orch-pipeline/SKILL.md:74`: "the re-dispatch carries a correction brief naming the failed acceptance criterion and the required correction, distinct from the original brief"). The first half does not: nothing in orchestrate routes step 5 through Phase 5 Review.
- Mitigating, hence minor not blocking: the ladder's re-dispatch is not blind — it attaches "both failed attempts as evidence" — but it does not name the failed acceptance criterion or the required correction, and it does not call the re-dispatch a correction brief, so it does not meet the 80-B8 bar ("a correction brief naming the failed acceptance criterion and the required correction, distinct from the original brief").

**Fix.** Add the correction-brief construction sentence to orchestrate's verify loop — in the escalation ladder (:250) and/or step 5's fix path — in the same wording as `orch-pipeline:74` / `feature-expansion:158`. Correct MANIFEST §2(c)(7) to claim inheritance only for orch-build-mvp step 6. Add a verify29 check asserting the sentence in `skills/orchestrate/SKILL.md` outside the GLOBAL-ROUTING block.

### 81-B4 — MINOR — the first-build carve-out's drone-side sites lack the scope sentence, and contradict the reasoning template on who assumes (80-B1 residual)

**Evidence.** Four drone-side sites tell the drone to state the assumption and proceed, each bounded only by a trailing clause — none carries the status-vocabulary scope sentence:

- `dispatch-prompt.md:96-97` (mechanical preamble): "state the assumption — the safe/reversible option — and proceed instead of asking the USER; a decision the brief leaves unspecified still returns NEEDS_CONTEXT to the orchestrator, which resolves it by stated assumption."
- `dispatch-prompt.md:117-118` (Before you begin), `:204-205` and `:226-227` (worked example ×2): same wording.
- The scope sentence exists exactly once, at `:51-55` (status vocabulary): "State-the-assumption-and-proceed applies only to carrying out the briefed approach, never to an unspecified decision."
- The reasoning template (`:144-147`) assigns the act to the other actor: "the question goes to the orchestrator, which resolves it by stated assumption — the assumption-and-proceed is the orchestrator's, not the drone's".

**Why it matters.** The four drone-side sites are the text a mechanical drone reads while executing. Their first clause ("state the assumption … and proceed") has no stated scope; the scoping work is done by the trailing "still returns NEEDS_CONTEXT" clause, which the drone must infer as the complement of the first clause — i.e. the drone must classify its own ambiguity to know which clause applies, which is the 80-B15 problem, now without the tie-breaker (see 81-B5). And the file contradicts itself on agency: the mechanical template says the drone states the assumption and proceeds; the reasoning template says the assumption-and-proceed is the orchestrator's, not the drone's. The no-guessing core holds at every site (NEEDS_CONTEXT-to-orchestrator is preserved; `"instead of NEEDS_CONTEXT"` is 0 hits tree-wide), so this is minor — but it is the same file telling two tiers two different stories about the same act.

**Fix.** Add the scope sentence to each of the four drone-side sites (or restate the first clause as "for carrying out the briefed approach only, state the assumption … and proceed"), and reconcile the actor assignment in one line in the status-vocabulary carve-out: the drone states assumptions only for execution detail; for an unspecified decision the orchestrator states the assumption. Assert the scope sentence in verify29 7d at all four sites, not just in the status vocabulary.

### 81-B5 — MINOR — the tie-breaker never reached the first-build carve-out texts (80-B15 incomplete)

**Evidence.** Grep for `"When in doubt"` in `skills/` + `rules/` + `commands/`: the tie-breaker ("When in doubt which side an ambiguity falls on, return the question — a returned question is never a stall." / short form "When in doubt, return the question — a returned question is never a stall.") is present in exactly the five Belief copies (`orch-pipeline:72`, `feature-expansion:151`, `orch-build-mvp:70`, `dispatch-prompt.md:34`, `dispatch-prompt.md:92` preamble) and nowhere else. It is absent from all six first-build carve-out texts: `dispatch-prompt.md:51-55` (status vocabulary), `:96-97`, `:117-118`, `:144-147`, `:204-205`, `:226-227`. (The only other "When in doubt" hits in the tree are unrelated: `python-patterns/SKILL.md:751` "prioritize clarity", `security-review/SKILL.md:511` "err on the side of caution".)

**Why it matters.** 80-B15's premise was that the drone must classify its own ambiguity. That classification is most acute in the first-build carve-out, where the drone must decide in one step whether an ambiguity is "carrying out the briefed approach" (proceed on assumption) or "a decision the brief leaves unspecified" (return NEEDS_CONTEXT) — under explicit pressure not to ask the user. The tie-breaker was added where the classification is easiest (the Belief sentence, which already names both sides) and omitted where it is hardest. Verify29 asserts the tie-breaker only in the Belief copies + preamble (7c), never in the carve-out texts, so the omission passes silently.

**Fix.** Add the tie-breaker sentence to the status-vocabulary carve-out (`dispatch-prompt.md:51-55`, which governs the other five sites) — at minimum — and assert it in verify29 7d alongside the existing carve-out checks.

### 81-B6 — MINOR — the worked-example brief lacks Verification steps (and the out-of-scope slot) while verify29's count check passes (80-B3 residual)

**Evidence.**

- `dispatch-prompt.md:195-229` (worked example — mechanical tier, fallback path, filled) carries Goal, Inputs, Constraints, Interface, Acceptance check, Return format — and **no `Verification steps` field**. Its Constraints name out-of-scope files only implicitly ("Do not touch `src/auth/tokens.go` or `src/auth/store.go`") with no "files out of scope" slot.
- `verify29.py:712-714` (check 7d) asserts `_dp.count("Verification steps") == 4` and `_dp.count("files out of scope") == 4`. The four occurrences of each are at :15 (skeleton list), :71/:68 (recon), :107/:104 (mechanical), :139/:136 (reasoning) — I verified each by `grep -n`. The worked example contributes 0 to both counts, and the check still passes. A count check cannot distinguish "four occurrences in the right places" from "four occurrences with one template missing and another doubled": it asserts a total, not per-template presence.

**Why it matters.** The worked example is a filled brief — the single most-copied text in the file. A brief composed by copying it is a six-field brief: it omits the verification procedure DIRECTOR-BRIEF_F29 requires, and 80-B3's fix ("Add a seventh contract field … to every template in `dispatch-prompt.md`") did not reach it. The verifier's count-based assertion is what lets the omission stand.

**Fix.** Add the `Verification steps:` line and a `files out of scope:` slot to the worked example. Strengthen verify29 7d to assert per-template presence (each of the three templates, the skeleton list, and the worked example contains `Verification steps` and `files out of scope`) instead of — or in addition to — the bare counts.

### 81-B7 — MINOR — the blind-reviewer exemption is unsound as recorded: the reviewer brief has no verification procedure (80-B3 scoping decision, challenged)

**Evidence.**

- `dispatch-prompt.md:15` (skeleton): "The seven-field contract binds every implementation dispatch (recon, mechanical, reasoning); the second-pass and blind-reviewer templates carry their own contract (opinion / verification gate) and are not implementation briefs."
- Blind-reviewer template (`dispatch-prompt.md`, "Template — blind reviewer"): Goal ✓ ("Find defects and judge the approach"), Inputs ✓ ("The diff … The original contract's acceptance criteria ONLY"), Constraints ◐ (scope is "the changed code PLUS its callers and callees", no files-out-of-scope slot), Acceptance check ○ ("n/a — you are the check"), **Verification steps ○ (absent)**, Return format ✓ (defect list + simpler/safer-approach answer).
- SPEC rule 3 admits no exemption: "every drone brief must carry the exact goal, the files in scope (and explicitly out of scope), constraints, acceptance criteria, verification steps, and what to return." MANIFEST §2(c)(6) records the exemption as "open to the #81 audit's challenge" without a justification.
- The second-pass exemption, by contrast, is defensible: the two passes check each other through the blind-parallel comparison and the disagreement path (`orchestrate/SKILL.md` escalation ladder :250, step 3: both passes fail/disagree → escalate, or first-build safe-option pick). The blind reviewer has no equivalent mutual check: nothing states how the orchestrator verifies the reviewer's output.

**Why it matters / why only minor.** The reviewer's output does get downstream checking in practice — its findings join the fix batch and are re-verified when fixed under the fix briefs' verification steps — so no unverified output reaches the user directly. The gap is that no text states that procedure, and the reviewer brief itself cannot state what would prove its own defect list right. The exemption as written ("its own contract") is an assertion, not a verification path — the same shape as the 80-B2 defect.

**Fix.** Either (a) add a `Verification steps:` line to the blind-reviewer template (the orchestrator re-reads each cited `path:line` and confirms the defect reproduces / the property was checked) plus a files-out-of-scope line, bringing it into the seven-field contract; or (b) record the exemption with its justification in the SPEC/manifest (reviewer output is verified downstream when its findings are fixed and re-verified; the reviewer receives only acceptance criteria by design, so it cannot carry verification steps of its own). Do not leave it as an unjustified carve-out. If (a), assert the new fields in verify29 7d.

### 81-B8 — MINOR (verifier) — check 7d/7c assertions are file-scoped or count-based, not tree-wide or per-template; 7e is order-insensitive

**Evidence.**

- `verify29.py:723-724`: `check("dispatch-prompt.md has no bare 'state the assumption you made and proceed'", "state the assumption you made and proceed" not in _dp)` — `_dp` is `dispatch-prompt.md` only. **Demonstrated false-pass:** the check passes while `agents/deep-reasoner.md:17` carries the identical phrase (see 81-B1). The property the check's name claims ("no bare assume-and-proceed") is broken in the built tree and the verifier does not see it.
- `verify29.py:641` (check 7c): the `"pick the reasonable option"` grep is `["grep", "-rn", "pick the reasonable option", "skills", "rules", "--include=SKILL.md", "--include=*.mdc", "--include=dispatch-prompt.md"]` — `agents/`, `commands/`, and every `references/`/`reference/` `.md` file are excluded, despite the check's name ("Tree-wide: every … occurrence is bounded"). A whole-tree grep currently returns exactly 5 hits, all bounded, so there is no live false-pass on this phrase — but the check would still pass with a sixth copy in `agents/`, `commands/`, or `references/`, which is precisely where the next copy would live (cf. 81-B1).
- `verify29.py:712-714`: the `Verification steps` / `files out of scope` assertions are bare counts (`== 4`), not per-template assertions — demonstrated blind spot: the worked example lacks both fields while the check passes (see 81-B6).
- `verify29.py:764` (check 7e): `_s_lines = sorted(...)` / `_b_lines = sorted(...)` — the comparison is order-insensitive. A `_F29` line moving *between* files cannot pass (each file pair is compared separately — verified: a move changes both files' multisets), but a line moving *within* a file passes silently. That matters for exactly one class of line: the NO-GUESSING carve-out must *follow* the Belief sentence it bounds; if it moved to another paragraph in the same file, 7e would still pass while the bound is detached. Coverage of the file list itself is complete — I enumerated the staged dirs and exactly 6 files carry `_F29` (`new-skills/orchestrate/SKILL.md`, `new-skills/orchestrate/references/dispatch-prompt.md`, `new-skills/feature-expansion/SKILL.md`, `new-skills/design-taste-frontend/SKILL.md`, `new-skills/design-taste-frontend/references/hallmark/references/redesign.md`, `new-rules/hackathon-mode.mdc`), all six in the 7e list; `round2-skills/` and `rewritten-skills/` carry none.
- The 7d contract-core extraction itself is sound and was checked, not assumed: `"The contract core"` occurs exactly once in `skills/orchestrate/SKILL.md` (:227), and the fenced block it extracts contains all seven fields with "files explicitly out of scope" in Constraints and the "drop no field" rule in the intro line. No finding there.

**Fix.** (i) Widen the 7c belief grep to the whole built tree (`skills`, `rules`, `commands`, `agents`, no `--include` filter) and assert the count is still 5 with each followed by the carve-out. (ii) Replace the dispatch-prompt-scoped 7d phrase assertion with a tree-wide one: `"state the assumption you made and proceed"` occurs 0× in the built tree, and every `"state the assumption"` occurrence sits inside a bounded carve-out (first-build sites + the orchestrator-level hard rule at `orchestrate:221`). (iii) Replace the 7d count assertions with per-template presence assertions (skeleton + recon + mechanical + reasoning + worked example). (iv) Make 7e order-sensitive for the carve-out lines at minimum (assert the carve-out line follows the Belief sentence in each file), or record the order-insensitivity as an accepted limitation.

---

## Per-finding verdicts — all 15 audit #80-B findings

| #80-B | Verdict | Evidence in this round |
|---|---|---|
| B1 (blocking) — first-build carve-out vs NO-GUESSING | **PARTIALLY FIXED** | `"instead of NEEDS_CONTEXT"` 0 hits tree-wide; all six sites route the question to the orchestrator; residual 81-B4 (scope sentence, actor contradiction) + 81-B5 (tie-breaker) |
| B2 (blocking) — GAN evaluator substituted for VERIFY-MERGE | **PARTIALLY FIXED** | Paragraph now states the three-part verify step + failure path (`gan:14`); loop wiring not fixed → 81-B2 |
| B3 (blocking) — six-field contract, droppable fields | **MOSTLY FIXED** | Contract core (:227) + all three templates carry all 7 fields + no-drop rule; residual 81-B6 (worked example), 81-B7 (blind-reviewer exemption) |
| B4 (minor) — orch-build-mvp uncarved Belief | **VERIFIED-FIXED** | `orch-build-mvp:70` carries the carve-out + tie-breaker |
| B5 (minor) — feature-expansion format gaps | **VERIFIED-FIXED** | Item 2 out-of-scope, split 4a/4b, item 9 return format (`feature-expansion:143-152`) |
| B6 (minor) — orch-pipeline/gan no brief format | **VERIFIED-FIXED as prescribed** | Seven-field contract references in `orch-pipeline:62` + `gan:14`; note the `gan-build.md` launch block is still thin (folded into 81-B2's fix) |
| B7 (minor) — orch-build-mvp unbridged merge-order | **VERIFIED-FIXED** | Bridges at all three sites (`orchestrate:93`, `feature-expansion:158`, `orch-build-mvp:71`) |
| B8 (minor) — correction brief constructed nowhere | **PARTIALLY FIXED** | Construction sentences in `feature-expansion:158` + `orch-pipeline:74`; orchestrate step 5 missing → 81-B3; gan loop missing (in 81-B2) |
| B9 (minor) — slot refill unqualified | **VERIFIED-FIXED** | Harness-gate clause in orch-pipeline, feature-expansion, gan, orchestrate step 4 |
| B10 (minor, verifier) — 7c naming check, not completeness | **VERIFIED-FIXED** | Real completeness check 7d added; residual count-vs-per-template weakness → 81-B8 |
| B11 (minor, verifier) — wrapper-pointer prefix only | **VERIFIED-FIXED** | Full pointer asserted (`_WRAPPER_POINTER` incl. COST-AWARE rules + ORCHESTRATOR-ONLY), all five wrappers count 1 |
| B12 (minor, verifier) — gan line asserted the claim | **VERIFIED-FIXED** | Verify-step assertions + old substitution asserted gone (0 hits tree-wide); residual loop wiring → 81-B2 |
| B13 (minor) — staged-vs-built drift | **REJECTION VERIFIED** | See Harness honesty below |
| B14 (minor) — wrapper pointers state neither COST-AWARE rule | **VERIFIED-FIXED** | Pointer states N>3 + minimal context; all five wrappers count 1 |
| B15 (minor) — no tie-breaker | **PARTIALLY FIXED** | Tie-breaker in all five Belief copies + preamble short form; missing from first-build texts → 81-B5 |

Spot-checked (Auditor A's scope, not re-audited here): 80-A1 redesign paragraph present with all seven fields + single-writer (`redesign.md:68`) and pointer at `design-taste-frontend/SKILL.md:455`; 80-A2 all five Belief copies carved; 80-A3 bridge at `orch-build-mvp:71`; 80-A4 refactor-cleaner qualified (`orch-refine-code/SKILL.md:35`, `commands/orch-refine-code.md:33`); 80-A5 `common-agents.mdc:26` factory line; 80-A6 `gan-build.md` pointer + out-of-scope line. No exceptions found in the spot-check.

---

## Field-coverage table — which DIRECTOR-BRIEF fields each skill's briefs actually carry (updated from #80-B)

Legend: ● = present as a distinct field/slot · ◐ = required only by prose assertion, pointer, reference, or merged/implicit · ○ = absent.

| Skill / brief | Goal | Files IN | Files OUT | Constraints | Acceptance criteria | Verification steps | What to return |
|---|---|---|---|---|---|---|---|
| orchestrate contract core (`SKILL.md:227`) | ● | ● (exact paths) | ● | ● | ● | ● | ● |
| dispatch-prompt recon / mechanical / reasoning templates | ● | ● | ● | ● | ● | ● | ● |
| dispatch-prompt worked example (:195-229) | ● | ● | ◐ (implicit "Do not touch …") | ● | ● | ○ | ● |
| dispatch-prompt second-pass template (exempt) | ◐ (Task) | ○ | ○ | ● | ○ | ○ | ● (opinion format) |
| dispatch-prompt blind-reviewer template (exempt) | ● | ● (acceptance criteria only) | ○ | ● | ○ ("n/a — you are the check") | ○ | ● |
| hackathon-mode (rule; block :45) | ● (block states all 7) | ● | ● | ● | ● | ● | ● — requirement text only; a rule, not a format |
| orch-pipeline (:62) | ◐ paragraph + reference to dispatch-prompt contract | ◐ | ◐ | ◐ | ◐ | ◐ | ◐ |
| orch-build-mvp (:13 pointer + :70 step 4) | ◐ via pointer; step-4 briefs use feature-expansion's format (● per that format) | ◐ | ◐ | ◐ | ◐ | ◐ | ◐ |
| orch-add-feature / orch-change-feature / orch-fix-defect (:13) | ◐ via pointer | ◐ | ◐ | ◐ | ◐ | ◐ | ◐ |
| orch-refine-code (:13 pointer; :35 step 2) | ◐ via pointer; step-2 sweep brief names all 7 inline ● | ◐ / ● (step 2) | ◐ / ● (step 2) | ◐ / ● (step 2) | ◐ / ● (step 2) | ◐ / ● (step 2) | ◐ / ● (step 2) |
| feature-expansion (format :143-152) | ● item 1 | ● item 2 | ● item 2 | ● item 3 | ● item 4a | ● item 4b | ● item 9 |
| gan-style-harness (:14) | ◐ paragraph + reference | ◐ | ◐ | ◐ | ◐ (rubric, not brief criteria) | ◐ | ◐ |
| gan generator brief (`commands/gan-build.md` Phase 2) | ◐ (one-line brief) | ◐ (spec + tokens) | ● (out-of-scope line) | ◐ | ◐ (rubric only) | ○ | ○ |
| design-taste-frontend redesign (`redesign.md:68`) | ● (paragraph enumeration) | ● | ● | ● | ● | ● | ● — paragraph list, not a fill-in template; no harness-gate clause, no tie-breaker |
| common-agents.mdc (:26, covered by reference) | ◐ (factory line; defers to block) | ◐ | ◐ | ◐ | ◐ | ◐ | ◐ |

Net vs round 1: **four formats now carry all 7 fields as distinct slots** (orchestrate contract core, the three dispatch-prompt implementation templates, the feature-expansion format, the redesign paragraph enumeration). Remaining gaps: the worked example (6/7, no Verification steps), the blind reviewer (4–5/7, exempt — see 81-B7), the gan generator launch block (no Verification steps or return slot — see 81-B2), and everything that carries the fields only by paragraph assertion or reference (orch-pipeline, gan skill text, the five wrappers, common-agents).

---

## Harness honesty — B13 rejection re-checked and confirmed

The coordinator's rejection of the 80-B13 sync fix is **correct**, verified end to end by this auditor:

- `fix16/fix16.py:3808` anchors on the staged wording: `sub(os.path.join(BASE, "rules/hackathon-mode.mdc"), "(its upstream \`claude -p\` invocation path does not run in Cursor", "(its upstream CLI-subprocess invocation path does not run in Cursor")` — default `count=1` (`sub()` def, `fix16.py:51-60`: on mismatch it appends to `ERRORS` and returns False).
- `fix16.py:4274-4280`: `main()` returns `1 if ERRORS else 0`, `sys.exit(main())` — a missed anchor fails the run.
- `build.sh:23222` runs `python3 "$PLUGIN_ROOT/fix16/fix16.py" "$PLUGIN_DIR"` on every build (last build step). Syncing staged `hackathon-mode.mdc:38` to the built text would make the anchor match 0× → `ERRORS` non-empty → exit 1 → build fails. (Manifest cites `:3807`; the anchor string itself is on line 3808, the `sub(` call spanning 3805–3809 — a one-line citation nit, not a substance error.)
- Staged-vs-built drift confirmed by direct read: staged `new-rules/hackathon-mode.mdc:38` says "its upstream `claude -p` invocation path does not run in Cursor"; built `rules/hackathon-mode.mdc:38` says "its upstream CLI-subprocess invocation path does not run in Cursor".
- The narrow replacement (check 7e) holds: I diffed the `_F29` lines myself (sorted) for three staged/built pairs — orchestrate `SKILL.md` (3 lines), `hackathon-mode.mdc` (1 line), `dispatch-prompt.md` (10 lines) — all identical. The 7e file list is complete: exactly six staged files carry `_F29` across all four staged dirs, all six in the 7e list, none in `round2-skills/` or `rewritten-skills/`.

---

## Checked and clean

- **Verifier re-run:** 215/215, exit 0, re-run independently.
- **GLOBAL-ROUTING block:** byte-identical in `orchestrate:36` and `hackathon-mode:45`; all 7 `_F29` tokens in the block and in all 10 in-scope skills (verify29 7c passes; re-confirmed by grep).
- **All five "pick the reasonable option" copies carved + tie-breaker** (whole-tree grep: exactly 5 hits — `orch-pipeline:72`, `feature-expansion:151`, `orch-build-mvp:70`, `dispatch-prompt.md:34`, `dispatch-prompt.md:92`).
- **"instead of NEEDS_CONTEXT": 0 hits** in the whole built tree. **"drop fields that are genuinely N/A": 0 hits** tree-wide. **"six fields": 0 hits** in the routing text (only unrelated form-field mentions in `design-taste-frontend/references/sections-library.md` and `system.md`).
- **"use your judgment" / "use judgement": 0 hits** in `skills/`, `rules/`, `commands/`, `agents/`.
- **`agents/fast-worker.md:16` and `agents/scout.md` are clean** — fast-worker says the opposite of guessing ("stop and return that — do not invent an answer"); scout says "a bounded honest map beats an unbounded guess". The `agents/` guess/invent grep finds only `deep-reasoner.md:17` as a live instruction; the rest are prohibitions ("never guess", "Prefer evidence over guesses", "never invent behavior") or an adversarial stance (`ecc-code-reviewer.md:18`, "assume every claim … is unproven").
- **Orchestrator-level assumption language is correctly scoped, not a drone instruction:** `orchestrate:221` ("never fan out … on a guessed user-resolvable fact"), `:266` ("unspecified decisions route up, not get guessed down"), `:290` (blind-parallel disagreement — "pick the safe/reversible option" is the orchestrator's move, recorded in the final report), ADAPT_F25 (`:91`, "a gap filled by inference is a stated inference, never a silent guess").
- **7d contract-core extraction is sound:** `"The contract core"` occurs exactly once in `orchestrate/SKILL.md` (:227); the extracted fenced block carries all seven fields, "files explicitly out of scope" in Constraints, and the "drop no field" rule in the intro line.
- **Redesign paragraph complete as written** (`redesign.md:68`): all seven fields enumerated, shared stylesheet/tokens single-writer ("locked once before page fan-out"), NO-GUESSING, VERIFY-MERGE with correction brief, COST-AWARE, ORCHESTRATOR-ONLY. It carries no harness-gate clause — but it makes no slot-refill claim ("where the harness has them"), so there is nothing false to gate.
- **orch-build-mvp step 6 legitimately inherits the correction brief:** `orch-build-mvp:72` routes Verify through "orch-pipeline Phase 5 (Review)", whose fix loop constructs it (`orch-pipeline:74`).
- **Polish-pass / systematic-debugging first-build carve-outs read, no finding:** `polish-pass/SKILL.md:38,76,97` and `impeccable-critique.md:216` ("state the assumption, pick the safe option, and proceed") and `systematic-debugging/SKILL.md:93` govern the pass runner's own routing decisions in orchestrator context (or, in the critique's case, enumerate the safe defaults — priority direction, tonal intent, scope = top 3 — rather than leaving the choice open). They are not drone brief instructions, so NO-GUESSING does not bind them; the "pick the most likely candidate" line (`polish-pass:76`) is the closest call and is worth a look if polish-pass is ever dispatched as a drone, but on the current reading the runner is the orchestrator.
- **Counts unchanged:** 67 skills / 45 agents / 48 rules / 55 commands / 15 hooks / 49 triggers (verify29 checks 1–5 pass).
- **Model pins unchanged:** no `deepseek/` or `qwen/` slugs; `DeepSeek`/`Qwen` names only in the two GLOBAL-ROUTING blocks (verify29 9b passes).

## Grep counts (for the record)

- `"pick the reasonable option"` whole built tree: **5** (all carved + tie-breaker).
- `"state the assumption"` whole built tree: **11** — `dispatch-prompt.md` ×4 (all inside bounded first-build carve-outs), `orchestrate/SKILL.md:221` (orchestrator-level hard rule), `agents/deep-reasoner.md:17` (unbounded — 81-B1), `polish-pass/SKILL.md` ×3 + `polish-pass/reference/impeccable-critique.md:216` + `systematic-debugging/SKILL.md:93` (pass-runner carve-outs, see above).
- `"state the assumption you made and proceed"`: **1** in the built tree (`agents/deep-reasoner.md:17`); **0** in `dispatch-prompt.md` (verify29 7d passes on the file it checks).
- `"instead of NEEDS_CONTEXT"`: **0**.
- `"correction brief"` in `skills/` + `rules/` + `commands/`: **8** — GLOBAL-ROUTING block ×2 (`orchestrate:36`, `hackathon-mode:45`), routing paragraphs ×4 (`orch-pipeline:62`, `feature-expansion:139`, `gan:14`, `redesign.md:68`), fix-loop constructions ×2 (`feature-expansion:158`, `orch-pipeline:74`). **0** in orchestrate step 5 / Verification stage / escalation ladder; **0** in `commands/gan-build.md`.
- `"When in doubt"` (tie-breaker form): **6** sites (5 Belief copies + preamble short form); **0** in the six first-build carve-out texts.
- `"Verification steps"` in `dispatch-prompt.md`: **4** (:15, :71, :107, :139); worked example: **0**. `"files out of scope"` in `dispatch-prompt.md`: **4** (:15, :68, :104, :136); worked example: **0**.
- `"The evaluator pass IS the verify step for GAN work"`: **0** (old substitution gone).
- Staged files carrying `_F29`: **6**, all in verify29's 7e list.
