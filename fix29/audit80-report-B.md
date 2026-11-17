# Audit #80-B — Fix #29 (brief / verify coherence + verifier)

- **Date:** Mon Nov 16, 2026
- **Auditor scope (Auditor B):** DIRECTOR-BRIEF completeness across the 9 in-scope skills; NO-GUESSING carve-out airtightness; VERIFY-MERGE traceability; COST-AWARE inheritance; the verifier (`fix29/verify29.py`, re-run independently); harness honesty. Read-only; no file under `~/workspace/hackathon-plugin/` was edited except this report.
- **Sources read in full:** `fix29/SPEC.md`, `fix29/MANIFEST.md`, `fix29/verify29.py`, `fix29/fix29.py` (census §4), `fix29/verify28-rerun-after29.log`; the built routing text in `skills/orchestrate/SKILL.md` (+ `references/dispatch-prompt.md`), `rules/hackathon-mode.mdc`, `skills/orch-pipeline/SKILL.md`, `skills/feature-expansion/SKILL.md`, `skills/gan-style-harness/SKILL.md`, `skills/orch-build-mvp/SKILL.md`, and the four other orch-* wrappers.
- **Verifier re-run by this auditor:** `python3 fix29/verify29.py` → **153/153, exit 0** (confirmed independently, not taken from the coordinator's log).

## Verdict: NOT PASS — 3 blocking, 12 minor

The routing paragraphs themselves are present and the verifier passes, but the fix's central mechanism is contradicted where it actually executes: the dispatch template every orchestrate brief is composed from tells drones to assume-and-proceed on under-specified points (80-B1), the highest-traffic brief format has no verification-steps field and lets fields be dropped (80-B3), and the GAN loop substitutes an evaluator rubric score for orchestrator verification against acceptance criteria (80-B2). The manifest's §2(c)(1) reconciliation claims the Belief-vs-NO-GUESSING conflict is closed; it is not — the two carved sentences are the only ones bounded, and three uncarved copies plus the first-build carve-out remain.

---

## Findings

### 80-B1 — BLOCKING — `dispatch-prompt.md` first-build carve-out directly contradicts NO-GUESSING on the primary path

**Evidence.**

- `skills/orchestrate/references/dispatch-prompt.md:51-55` (status vocabulary):
  > "**First-build carve-out:** during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature, executors do NOT return `NEEDS_CONTEXT` for a missing user-resolvable fact or an under-specified point — they state the assumption (the safe/reversible option) and proceed."
- The same override is appended to the no-guessing instruction in four more places in the same file: mechanical template preamble `:95-98`, mechanical "Before you begin" `:115-117` (which first says "return NEEDS_CONTEXT now naming exactly what's missing — do not guess"), worked example `:202-204` and `:224-226`.
- Reasoning template `:141-142` (NOT first-build scoped at all):
  > "If under-specified: state the assumption you made and proceed; return `NEEDS_CONTEXT` only if genuinely blocked."

**Why it matters.** NO-GUESSING_F29 (GLOBAL-ROUTING block, `skills/orchestrate/SKILL.md:36`) says: "A drone that hits a decision its brief leaves unspecified stops and returns the question to the orchestrator instead of guessing". An "under-specified point" IS a decision the brief leaves unspecified. The carve-out therefore instructs the exact opposite behaviour — state an assumption and proceed — and it applies during a hackathon first build, which is the plugin's mainline path, and (for the reasoning template) in every build. The manifest §2(c)(1) reconciles only the two Belief sentences; it never mentions this file, even though orchestrate `SKILL.md:227` says "Compose every dispatch from the templates in [dispatch-prompt.md](references/dispatch-prompt.md)" — i.e. every brief is composed from the contradicting template. The carve-out's legitimate intent ("don't ask the user mid-build") does not require its wording: the question can go to the *orchestrator*, which decides scope; the text forecloses that path by banning `NEEDS_CONTEXT` outright.

**Fix.** In `dispatch-prompt.md`, bound every "state the assumption and proceed" with the same NO-GUESSING bound used at `orch-pipeline:72` / `feature-expansion:150`, scoped to execution detail only: assumption-and-proceed applies only to carrying out the briefed approach, never to an unspecified file, scope call, or acceptance criterion — those return `NEEDS_CONTEXT` to the *orchestrator* (not the user), and the orchestrator resolves them by stated assumption during first builds. Add the bound at `:35`, `:51-55`, `:93-98`, `:115-117`, `:141-146`, `:202-204`, `:224-226`. Verify29 must assert the bound string in this file (it currently asserts nothing here).

### 80-B2 — BLOCKING — gan-style-harness: the evaluator rubric is substituted for VERIFY-MERGE, and two drone outputs have no verification path

**Evidence.**

- `skills/gan-style-harness/SKILL.md:14`:
  > "The evaluator pass IS the verify step for GAN work: the orchestrator verifies every drone output against the brief's acceptance criteria and sends failed output back with a correction brief (VERIFY-MERGE_F29)"
- The evaluator's actual criteria (`gan-style-harness/SKILL.md`, "Evaluation Criteria" / rubric) are four generic scores — Design Quality, Originality, Craft, Functionality, each 1–10, weighted, "Pass threshold = 7.0" — not the brief's acceptance criteria. The rubric explicitly excludes screen distinctiveness ("Screen distinctiveness is NOT scored here… judged ONLY by `browser-qa`").
- Loop wiring (same file, "Architecture" diagram + "The Three Agents"): planner produces the spec → generator builds → evaluator scores → feedback to generator, "5-15 iterations", until score passes or plateaus. No step has the orchestrator checking generator output against the brief's acceptance criteria; no step has the orchestrator checking the *evaluator's* output (a false pass at ≥ 7.0 ends the loop) or the *planner's* spec (which feeds the generator directly, unverified).

**Why it matters.** SPEC rule 4 requires the orchestrator to verify *every* drone output *against the brief's acceptance criteria*, with failed output returned with a correction brief. The GAN paragraph asserts that sentence and then describes a loop in which generator output goes to a drone (evaluator), evaluator output goes to a drone (generator), and planner output goes to a drone (generator) — the orchestrator dispatches but never verifies. A rubric score is not an acceptance-criteria check: a slice can score 7.0+ while failing its brief's acceptance criterion (e.g. a named edge case, a performance budget), and nothing in the skill catches it. The manifest §2(a) records this as "evaluator pass named as the verify step" — naming it is exactly the problem; it was named, not implemented. (The orch-build-mvp step-6 `code-reviewer` + Phase 5 pass covers GAN output only inside the standalone pipeline, not a standalone `/gan-build` run, and a diff review is still not an acceptance-criteria check.)

**Fix.** In `gan-style-harness/SKILL.md`, add an orchestrator verify step to the loop: after the evaluator pass, the orchestrator checks the generator's output against the brief's acceptance criteria (not just the rubric score) before accepting it, and re-checks the evaluator's pass/fail call against the same criteria; the planner's spec is checked against the brief before the first generator pass. State that a rubric pass with a failed acceptance criterion is a fail, and that the failure goes back with a correction brief naming the failed criterion. Verify29 check 10i's gan line (see 80-B12) must assert the new step, not just the "IS the verify step" claim.

### 80-B3 — BLOCKING — orchestrate's six-field dispatch contract has no verification-steps field, omits files-out-of-scope, and authorises dropping fields

**Evidence.**

- `skills/orchestrate/SKILL.md:227` — the contract core:
  > "The contract core (drop fields that are genuinely N/A, never the acceptance check): `Goal: … / Inputs: … / Constraints: <what must not change; style/perf/security bounds> / Interface: … / Acceptance check: … / Return format: …`"
- `skills/orchestrate/references/dispatch-prompt.md:6-8` (skeleton): "The contract — the six fields." The six fields are Goal, Inputs, Constraints, Interface, Acceptance check, Return format. No verification-steps field exists anywhere in the skeleton or any template. "Files out of scope" appears only in the mechanical template's Constraints example (`dispatch-prompt.md`, mechanical template: "Constraints: [what must NOT change; files out of scope]"); the recon template's Constraints ("read-only; cover [scope]"), the reasoning template's Constraints ("hard requirements; what's already frozen"), the second-pass template, and the blind-reviewer template carry no out-of-scope slot.

**Why it matters.** DIRECTOR-BRIEF_F29 requires seven fields, including verification steps and files explicitly out of scope. Orchestrate's contract — the format every implementation brief is actually composed from — carries six fields, with verification steps folded into the Acceptance check at best ("run it, paste output" is a check, not the verification procedure) and out-of-scope present in one of five templates. Worse, "drop fields that are genuinely N/A" affirmatively permits a brief missing a DIRECTOR-BRIEF field, which directly contradicts the block's "an incomplete brief means the drone does not start" (`orchestrate/SKILL.md:36`). The block names the seven fields; the working template does not implement them. Verify29 7c passes on this file (see 80-B10) because it only checks the block's field-list *string*.

**Fix.** Add a seventh contract field, `Verification steps: <the exact steps/commands the executor runs to verify, distinct from the acceptance check>`, to the `SKILL.md:227` contract core and to every template in `dispatch-prompt.md`; add "files out of scope" to the `SKILL.md:227` Constraints line and to every template's Constraints; change "drop fields that are genuinely N/A" to "drop no DIRECTOR-BRIEF field; a field with nothing to list is written as `none`, never deleted". Add verify29 checks asserting the seven field labels in the contract core and in each template.

### 80-B4 — MINOR — orch-build-mvp:70 carries a third, uncarved Belief sentence

**Evidence.** `skills/orch-build-mvp/SKILL.md:70`:
> "**Belief in the brief:** implementers trust the brief and build it — they do not second-guess the plan, hedge, or wait for reassurance; they commit to the approach and make it work; if a detail is ambiguous, they pick the reasonable option and note it, they don't stall."

No "**Bounded by NO-GUESSING**" sentence follows it, unlike `orch-pipeline:72` and `feature-expansion:150`. Grep count for "pick the reasonable option" in `skills/` + `rules/`: 5 occurrences — 2 carved, 3 uncarved (`orch-build-mvp:70`, `dispatch-prompt.md:35`, `dispatch-prompt.md:93`).

**Why it matters.** The wrapper is the standalone engine's own step-4 text; a reader of `orch-build-mvp` alone sees the uncarved instruction, and the sentence sits in the step that drives the GAN loop per the feature-expansion brief format. The manifest §2(c)(1) says the carve-out was applied to "the two Belief-in-the-brief sentences" — there are five copies of the sentence in the tree, not two.

**Fix.** Append the identical carve-out sentence after `orch-build-mvp:70`. Add a verify29 check counting "pick the reasonable option" occurrences (5) and asserting each is followed by the carve-out (or is in `dispatch-prompt.md`, covered by the 80-B1 fix).

### 80-B5 — MINOR — feature-expansion: out-of-scope lives only in paragraph prose; acceptance criteria and verification steps share one format item; what-to-return is by pointer

**Evidence.** `skills/feature-expansion/SKILL.md:139` (Phase 4 paragraph): "the brief format below already carries the goal, the files in scope, constraints, acceptance criteria (completion evidence), verification steps, and what to return (the result format in Collect and reconcile) — and now also names the files explicitly OUT of scope, which the old format did not require." The 8-item format (`:143-152`): item 2 (`:146`) names "which files it touches" (in-scope only — no out-of-scope item exists); item 4 (`:148`, "Completion evidence: the exact commands or checks that prove it works") is the single slot doing duty for *both* acceptance criteria and verification steps; no item states the return format — that is defined only by reference to "Collect and reconcile" (`:158`, "read every implementer's result (status, changed files, verification evidence, residual risks, blockers)").

**Why it matters.** The paragraph asserts the gap is closed, but the numbered format — the checklist a brief-writer actually follows — was never amended: a writer following items 1–8 alone omits out-of-scope files, and item 4 lets a brief satisfy "acceptance criteria + verification steps" with commands alone and never state the pass bar separately from the procedure. The manifest §2(c)(4) claims the format "already carried" the fields; strictly, the *paragraph* carries them and the *format* carries five of seven as items.

**Fix.** Add item 9 (or amend item 2): "Files explicitly OUT of scope (named; `none` if genuinely none)". Split item 4 into 4a acceptance criteria (the pass bar) and 4b verification steps (the commands/procedure that prove it). Add a return-format item (status, changed files, verification evidence, residual risks, blockers) instead of pointing at Collect. Update verify29's "names out-of-scope files" check to assert the new format item, not just the paragraph sentence.

### 80-B6 — MINOR — orch-pipeline and gan-style-harness have no brief format at all; DIRECTOR-BRIEF rests on paragraph assertion only

**Evidence.** `skills/orch-pipeline/SKILL.md:62` states the full 7-field list for "Every drone brief", and `skills/gan-style-harness/SKILL.md:14` states it for "a director brief". Neither file contains any brief template, brief-construction step, or per-phase brief format: orch-pipeline's phases delegate to agents (`architect`, `tdd-guide`, `code-reviewer`, `:72-80`) with no brief text; gan's planner/generator/evaluator sections describe roles, rubric, and config, with no brief template for the generator or evaluator passes.

**Why it matters.** A requirement stated in a routing paragraph is not a format that constructs the fields. Nothing in either skill tells the orchestrator *where* the seven fields go, so two runs can produce briefs of wildly different completeness while both "follow" the paragraph. Contrast feature-expansion (has a format, weak — 80-B5) and orchestrate (has a format, defective — 80-B3).

**Fix.** Give orch-pipeline a brief format (reuse the dispatch-prompt.md seven-field contract once 80-B3 lands, by reference from Phase 4) and gan a generator/evaluator brief format naming the seven fields (goal, files in/out, constraints, acceptance criteria from the spec, verification steps, return format). Add a verify29 check asserting the format reference exists in each file.

### 80-B7 — MINOR — orch-build-mvp step 5 has a third, unbridged merge-order sentence

**Evidence.** `skills/orch-build-mvp/SKILL.md:71` (step 5, Reconcile): "If two implementers in the same wave touched the same files, decide the merge order — the first-listed implementer's files win on conflict unless the planner marked a dependency…" — no bridge sentence. The bridged copies are `skills/orchestrate/SKILL.md:93` ("the merge-order rule at the end of this step applies only if partitioning failed and two drones touched the same file anyway") and `skills/feature-expansion/SKILL.md:158` ("Collision procedure (sequential dispatch for overlapping scopes is the prevention rule; this is what happens if a collision still occurs)"). Grep for "merge order" in `skills/` + `rules/`: exactly these 3 sites. The manifest §2(c)(2) says the bridge was added "in both files" — there are three merge-order sites, not two.

**Why it matters.** Unbridged, the sentence reads as a normal expected path rather than a failure-only fallback, in the standalone engine's own reconcile step — the one place a collision is actually handled. It does not contradict FACTORY-DISPATCH outright (it handles the collision case), but it leaves the prevention rule unstated where it matters most.

**Fix.** Add the bridge sentence to `orch-build-mvp:71` ("this procedure applies only if partitioning failed…; sequential dispatch for overlapping scopes is the prevention rule"). Add a verify29 check asserting all three merge-order sites carry the bridge.

### 80-B8 — MINOR — "correction brief" is asserted in five paragraphs and constructed nowhere

**Evidence.** Grep for "correction brief" in `skills/` + `rules/`: exactly 5 hits, all inside the routing paragraphs — `skills/orchestrate/SKILL.md:36`, `rules/hackathon-mode.mdc:45`, `skills/orch-pipeline/SKILL.md:62`, `skills/feature-expansion/SKILL.md:139`, `skills/gan-style-harness/SKILL.md:14`. No fix loop, collect step, review step, or reconcile step anywhere in the tree names or constructs a correction brief: feature-expansion's fix loop (`:156`) says "the implementer fixes it and re-verifies — at most 2 rounds"; orch-pipeline's Review (`:75-80`) routes findings to "the capped 2-round fix loop"; orchestrate step 5's verify loop re-dispatches without naming a brief.

**Why it matters.** VERIFY-MERGE_F29's second half ("failed output goes back with a correction brief") has no operational form: a re-dispatch that re-sends the original brief is not a correction brief (it does not name the failed criterion and the required correction). The behaviour (retry in a capped loop) exists; the artifact does not.

**Fix.** In each fix loop, state that the re-dispatch carries a correction brief naming the failed acceptance criterion and the required correction, distinct from the original brief. One shared sentence in the three fix-loop sites suffices; assert it in verify29.

### 80-B9 — MINOR — slot refill is stated unconditionally in the per-skill paragraphs; only the GLOBAL-ROUTING block gates it

**Evidence.** `skills/orch-pipeline/SKILL.md:62`: "the next queued job dispatched into the freed slot"; `skills/feature-expansion/SKILL.md:139`: "the next queued feature dispatched into the freed slot"; `skills/gan-style-harness/SKILL.md:14`: factory drones "from its queue" (same retire-and-refill framing via the shared paragraph); `skills/orchestrate/SKILL.md:93`: "a drone is retired on completion and the next queued slice is dispatched into the freed slot". None of these four carries a harness qualifier. The qualifier exists only in the GLOBAL-ROUTING block (`orchestrate:36`, `hackathon-mode:45`): "Live factory behavior (per-model dispatch, slot refill at scale) is harness-gated: in Cursor, per-subagent model selection is unreliable and in-IDE parallelism caps around 4 with no slot refill, so the factory lights up fully on the later port, not in Cursor".

**Why it matters.** SPEC Honest limits state slot refill does *not* work in Cursor ("extras wait for the entire first batch to finish instead of filling slots as they free up"). A reader of orch-pipeline, feature-expansion, or gan alone — or of orchestrate step 4 alone — takes retire-and-refill as operative Cursor behaviour. The block's gate does not travel with the per-skill paragraphs. (Partial mitigation, noted fairly: feature-expansion `:139` also says "the Team shape below (one implementer per feature, up to 4 in parallel, waves by dependency…) IS the factory queue under Cursor's cap", which correctly reframes waves as slot batches for that skill.)

**Fix.** Append one harness-gate clause to each of the three factory paragraphs and to orchestrate step 4 ("in Cursor, slots refill per wave, not per completion — see GLOBAL-ROUTING"). No verify29 change needed beyond the existing harness-gate check, extended to the paragraphs.

### 80-B10 — MINOR (verifier) — check 7c is a naming check, not the SPEC-required fan-out/brief-completeness check

**Evidence.** `fix29/verify29.py`, check 7c: the "director-brief field list" check asserts only that the block contains the substring "the exact goal, the files in scope and explicitly out of scope, constraints, acceptance criteria, verification steps, and what to return". No check in verify29 examines any actual brief format for the seven fields.

**Why it matters.** This is a demonstrated false-pass: 7c passes while the underlying property is broken in three independent ways found by this audit — feature-expansion's format has no out-of-scope item (80-B5), orchestrate's contract has no verification-steps field (80-B3), and orch-pipeline/gan have no brief format at all (80-B6). SPEC Verification requires the verifier to be updated "with checks for the routing statements + a fan-out/brief-completeness check"; the completeness half was not implemented — only the routing-statement half. The check's name ("carries the director-brief field list") overstates what it proves.

**Fix.** Add a real brief-completeness check: assert the seven field labels in (a) the `SKILL.md:227` contract core + each `dispatch-prompt.md` template, (b) the feature-expansion brief format items, (c) the orch-pipeline/gan brief formats once 80-B6 lands. Rename the existing substring check to "block names the field list" so its name matches its strength.

### 80-B11 — MINOR (verifier) — check 10i's wrapper-pointer check matches only the pointer prefix

**Evidence.** `fix29/verify29.py`, check 10i: `_WRAPPER_POINTER = ("**Factory routing (fix #29, GLOBAL-ROUTING_F29):** this operation runs through the shared `orch-pipeline` engine")` and each wrapper is asserted only on `_wt.count(_WRAPPER_POINTER) == 1`. The substantive second half of the pointer — "which dispatches all implementation work through the factory — see `orch-pipeline` for the routing (task queue, single-task drones, director briefs, no-guessing, verify-and-merge, cost-aware fan-out)" — is never asserted.

**Why it matters.** A pointer truncated after "engine" (losing the routing reference and the ORCHESTRATOR-ONLY line) would still pass 10i. The check proves the pointer exists, not that it points anywhere.

**Fix.** Extend `_WRAPPER_POINTER` to the full pointer sentence (through "cost-aware fan-out)") and assert the ORCHESTRATOR-ONLY sentence in each wrapper.

### 80-B12 — MINOR (verifier) — check 10i's gan line asserts the "IS the verify step" claim, not verification

**Evidence.** `fix29/verify29.py`, check 10i: `check("gan-style-harness evaluator-is-verify line present x1 (VERIFY-MERGE_F29)", _gan.count("The evaluator pass IS the verify step for GAN work") == 1)`.

**Why it matters.** The check asserts a *claim sentence* exists. It cannot distinguish "the evaluator pass is the verify step" (a substitution — see 80-B2) from an actual orchestrator-against-acceptance-criteria step. It passes on the current text precisely because the text asserts the substitution.

**Fix.** Replace with a check asserting the orchestrator verify step added by the 80-B2 fix (orchestrator checks generator output against the brief's acceptance criteria; rubric pass ≠ acceptance pass).

### 80-B13 — MINOR (verifier scope) — verify29 never compares staged vs built; staged orchestrate/hackathon-mode have drifted, and a rebuild would regress the built tree

**Evidence.** `diff new-skills/orchestrate/SKILL.md hackathon-ecc/skills/orchestrate/SKILL.md` differs at 3 lines; `diff new-rules/hackathon-mode.mdc hackathon-ecc/rules/hackathon-mode.mdc` differs at 1 line:

- orchestrate `:100`, `:273`, `:280`: built has "blind `code-reviewer` agent (`agents/ecc-code-reviewer.md`)" (and `:280` the `security-reviewer` agent link); staged has the bare "`code-reviewer`" / "`security-reviewer`" forms.
- hackathon-mode `:38`: staged says "its upstream `claude -p` invocation path does not run in Cursor"; built says "its upstream CLI-subprocess invocation path does not run in Cursor".
- `build.sh:229` copies `new-skills/orchestrate/SKILL.md` → built, and `build.sh:263` copies `new-rules/hackathon-mode.mdc` → built, on every build. So a clean rebuild reverts the built-only rewordings — including reintroducing the banned term "claude" (`claude -p`) into the built tree, which would then fail verify29 check 8.

**Why it matters.** This drift predates fix #29 and is not a routing defect, but verify29 (built-tree-only) is blind to it, and the manifest's "staged sources only" discipline is currently violated by these four lines. The fix #29 GLOBAL-ROUTING block itself is correctly in sync (staged orchestrate `:36` = built `:36`; staged hackathon-mode `:45` = built `:45` — verified by diff).

**Fix.** Sync the four staged lines to the built text (or vice versa, coordinator's call — the built text is the better one in all four cases), and add a verify29 staged-vs-built identity check for the two staged-owned files. (Not a fix #29 routing change; record as owed if deferred.)

### 80-B14 — MINOR — COST-AWARE: the five wrapper pointers name "cost-aware fan-out" but state neither the N>3 rule nor minimal context

**Evidence.** Shared pointer string, e.g. `skills/orch-build-mvp/SKILL.md:13`: "see `orch-pipeline` for the routing (task queue, single-task drones, director briefs, no-guessing, verify-and-merge, cost-aware fan-out)". The N>3 justification rule ("the orchestrator justifies N>3 in one line") and the minimal-context rule ("drones carry minimal context, only the files and facts their partition needs") appear inline in `orch-pipeline:62`, `feature-expansion:139`, `gan-style-harness:14`, and the GLOBAL-ROUTING block — but in none of the five wrappers.

**Why it matters / why only minor.** Runtime inheritance holds: `rules/hackathon-mode.mdc` is `alwaysApply: true` (frontmatter, line 3), so the block — including both COST-AWARE rules — is in context on every Cursor run, and the pointer names the engine that states them. Textual inheritance does not hold: a reader (or agent) reading only a wrapper never sees either rule, only the name "cost-aware fan-out". The gap is therefore real but narrow.

**Fix.** Extend the shared pointer string with one clause: "(fan-out bounded by efficiency: N>3 justified in one line; drones carry minimal context)". One-line change in `fix29.py` §2; assert it in verify29 10i.

### 80-B15 — MINOR — the two carve-outs are not airtight: the drone must classify its own ambiguity, with no tie-breaker

**Evidence.** `skills/orch-pipeline/SKILL.md:72` and `skills/feature-expansion/SKILL.md:150` (identical carve-out):
> "'pick the reasonable option' applies only to carrying out the briefed approach, never to a decision the brief leaves unspecified — an unspecified file, scope call, or acceptance criterion is returned to the orchestrator as a question, not guessed."

**Why it matters.** The carve-out draws the line correctly, but the drone itself must decide which side of the line a given ambiguity falls on — and that classification is itself a judgment call on an unspecified matter. "Carrying out the briefed approach" vs "a decision the brief leaves unspecified" is genuinely ambiguous in the common case (e.g. the brief says "wire the named tool" but not which endpoint — is picking the endpoint carrying out the approach, or an unspecified scope call?). A drone that misclassifies guesses, and the text gives it no tie-breaker.

**Fix.** Add one tie-breaker sentence to both carve-outs: "When in doubt which side an ambiguity falls on, return the question — a returned question is never a stall." Assert the tie-breaker string in verify29 7c alongside the existing carve-out checks.

---

## Field-coverage table — which DIRECTOR-BRIEF fields each skill's briefs actually carry

Legend: ● = present as a field/slot in the brief format · ◐ = required only by prose assertion, pointer, or merged into another field · ○ = absent.

| Skill | Goal | Files IN | Files OUT | Constraints | Acceptance criteria | Verification steps | What to return |
|---|---|---|---|---|---|---|---|
| orchestrate (contract core `:227` + `dispatch-prompt.md`) | ● Goal | ● Inputs (exact paths) | ◐ mechanical template only; absent from contract core + 4 of 5 templates; droppable per "drop fields that are genuinely N/A" | ● Constraints | ● Acceptance check | ◐ folded into Acceptance check ("run it, paste output"); no separate field | ● Return format + report contract |
| hackathon-mode (rule; carries block `:45`) | ● (block states all 7) | ● | ● | ● | ● | ● | ● — requirement text only; it is a rule, not a brief format |
| orch-pipeline (`:62`) | ◐ paragraph asserts all 7; no brief format exists in the skill | ◐ | ◐ | ◐ | ◐ | ◐ | ◐ |
| orch-build-mvp (`:13` pointer + `:70` step 4) | ◐ via pointer to orch-pipeline; step-4 briefs use feature-expansion's format (see below) | ◐ | ◐ | ◐ | ◐ | ◐ | ◐ |
| orch-add-feature (`:13`) | ◐ via pointer to orch-pipeline | ◐ | ◐ | ◐ | ◐ | ◐ | ◐ |
| orch-change-feature (`:13`) | ◐ via pointer to orch-pipeline | ◐ | ◐ | ◐ | ◐ | ◐ | ◐ |
| orch-fix-defect (`:13`) | ◐ via pointer to orch-pipeline | ◐ | ◐ | ◐ | ◐ | ◐ | ◐ |
| orch-refine-code (`:13`) | ◐ via pointer to orch-pipeline | ◐ | ◐ | ◐ | ◐ | ◐ | ◐ |
| feature-expansion (format `:145-152`) | ● items 1–2 | ● item 2 | ◐ `:139` paragraph prose only; no numbered item | ● item 3 | ◐ item 4 merges acceptance + verification | ◐ item 4 (same slot) | ◐ by pointer to Collect (`:158` result format) |
| gan-style-harness (`:14`) | ◐ paragraph asserts all 7; no brief format exists; planner spec / generator brief untemplated | ◐ | ◐ | ◐ | ◐ (rubric scores, not brief acceptance criteria — see 80-B2) | ◐ | ◐ |

Net: **no skill's briefs carry all 7 fields as distinct format slots.** The closest is feature-expansion (5 of 7 as items, 2 by prose/pointer); orchestrate's contract carries 5 of 7 as fields with 2 partial; orch-pipeline, gan, and the five wrappers carry all 7 only as a paragraph assertion (or a pointer to one).

---

## Verify28 re-run — confirmed: the single failure is ONLY line shifts

The coordinator's `fix29/verify28-rerun-after29.log` shows **109/110**, failing only check 12 (CUT-name sweep) with 6 un-allow-listed hits. I verified each hit's content against verify28's allow-list justifications:

| Failing line (post-fix29) | Content | verify28 allow entry | Shift |
|---|---|---|---|
| `feature-expansion:194` | `code-tour` was cut (REROUTE_F27) | `:192` same justification | +2 |
| `feature-expansion:195` | `intent-driven-development` was cut | `:193` same justification | +2 |
| `feature-expansion:206` | `agent-self-evaluation` was cut | `:204` same justification | +2 |
| `feature-expansion:213` | Brainstorming techniques attribution | `:211` (attribution, not a dispatch) | +2 |
| `orchestrate:137` | `ecc-recipes` was cut | `:136` same justification | +1 |
| `hackathon-mode:47` | `product-lens` / `intent-driven-development` do not scope hackathons (negative) | `:46` same justification | +1 |

All six are the same allow-listed prose-history/negative lines, shifted by fix #29's insertions (Phase 4 paragraph + carve-out in feature-expansion, GLOBAL-ROUTING block in orchestrate/hackathon-mode). No new live dispatch, no other check failed. The log's head confirms all other 109 checks PASS. **The verify28 failure is explained entirely by line shifts; nothing else.**

## Verify29 coverage vs verify28 — confirmed preserved

Diffing check names (`grep check("…")`, sorted): **no check name present in `fix28/verify28.py` is missing from `fix29/verify29.py`** (97 distinct names in verify28, 119 in verify29; totals 110 vs 153, the difference being loop-generated per-skill/per-token checks). Verify29 keeps every verify28 check and adds the [29] checks (7c, 9b, 10i, 11b). The coverage gap is not dropped checks but *strength*: see 80-B10–B12.

---

## Checked and clean

- **Verifier re-run:** 153/153, exit 0, re-run independently by this auditor (not from the coordinator's log).
- **GLOBAL-ROUTING block:** byte-identical in `orchestrate:36` and `hackathon-mode:45` (verified by verify29 7c and by direct diff of staged vs built copies); all 7 `_F29` tokens present in the block and in all 9 in-scope skills (grep: `GLOBAL-ROUTING_F29` ×2 in orchestrate, ×1 in each of the other 8).
- **NO-GUESSING carve-outs as written:** the two carved sentences (`orch-pipeline:72`, `feature-expansion:150`) are byte-identical to each other and correctly scoped — the HOW-vs-WHAT distinction is sound as far as it goes (residual gap is the missing tie-breaker, 80-B15).
- **Merge-order bridges (2 of 3):** orchestrate step 4 (`:93`) and feature-expansion Collect (`:158`) both correctly bridge the merge-order procedure to partitioning-failure-only; the bridge sentences are present and correctly worded.
- **Model pins unchanged:** no `deepseek/` or `qwen/` model slugs anywhere in the built tree; `DeepSeek`/`Qwen` names occur only in the two GLOBAL-ROUTING blocks plus pre-existing icon-data files (`design-taste-frontend/assets/icons/` — `demo.html:48`, `icons-credits.json:1055-1056`, `index.json:1298-1299,8264`, all `logos:deepseek-icon` icon ids, not model references). Note: verify29 9b's name grep is scoped to `SKILL.md` + `*.mdc` and therefore does not itself prove the whole-tree claim; I confirmed it with an independent whole-tree grep.
- **Grep sweeps in the routing set (9 skills):** "use your judgment" / "use judgement": 0 hits. "pick the reasonable option": 5 hits (2 carved, 3 uncarved — 80-B1/B4). "assume": only benign hits — marked assumptions ("record it as an assumption, clearly marked as assumed", `hackathon-mode` §1), prohibitions ("do not assume full-library access", "not assumed held", `orchestrate:62`), and the orchestrator-level ADAPT_F25 inference rule (`orchestrate:91`, "a gap filled by inference is a stated inference, never a silent guess") — none instructs a drone to guess. "pick the safe/reversible option" (`orchestrate:290`) is orchestrator-level (blind-parallel disagreement path), not drone guessing — not a conflict.
- **Council out-of-scope (OWED-29-3):** confirmed — `council/SKILL.md:12-14,53,85-87` launches three parallel subagents (Skeptic / Pragmatist / Critic) producing analysis/decisions, not code; no implementation dispatch. The exclusion stands.
- **Harness honesty in the block:** the GLOBAL-ROUTING block's gate sentence is accurate and complete ("in Cursor, per-subagent model selection is unreliable and in-IDE parallelism caps around 4 with no slot refill, so the factory lights up fully on the later port, not in Cursor"). The overclaim is confined to the unqualified per-skill paragraphs (80-B9).
- **Staged/built block sync:** the GLOBAL-ROUTING block is identical in staged and built copies of both files (80-B13's drift is elsewhere, in 4 unrelated lines).
- **fix29.py census:** read; it asserts token presence per skill + block byte-identity + all 7 tokens in the block, and the patch log carries the census line with 0 errors. It does not (and does not claim to) check brief completeness — that gap belongs to verify29 (80-B10).
- **Counts unchanged:** 67 skills / 45 agents / 48 rules / 55 commands / 15 hooks / 49 triggers (verify29 checks 1–5 pass; re-confirmed in this auditor's re-run).

## Grep counts (for the record)

- "pick the reasonable option" in `skills/` + `rules/`: **5** (orch-pipeline:72 carved, feature-expansion:150 carved, orch-build-mvp:70 uncarved, dispatch-prompt.md:35 uncarved, dispatch-prompt.md:93 uncarved).
- "state the assumption" in `dispatch-prompt.md`: **6** (lines 54, 97, 116, 141, 203, 225).
- "correction brief" in `skills/` + `rules/`: **5**, all inside routing paragraphs, none in any fix loop.
- "merge order" in `skills/` + `rules/`: **3** sites (orchestrate:93 bridged, feature-expansion:158 bridged, orch-build-mvp:71 unbridged).
- "use your judgment": **0** in the routing set.
