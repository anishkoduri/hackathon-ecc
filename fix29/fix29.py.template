#!/usr/bin/env python3
"""Fix #29 — adaptable orchestration: forced orchestrator, factory dispatch,
director-grade briefs.

Run by build.sh as a patch step (after fix28, before STEP 5 Counts):
    python3 "$PLUGIN_ROOT/fix29/fix29.py" "$PLUGIN_DIR"

Operates on the BUILT tree only. Staged-source halves are edited directly
in new-skills/ (orchestrate, feature-expansion, design-taste-frontend) and
new-rules/ (hackathon-mode) and flow through the STEP 2 copy. Every text
patch asserts its anchor occurs EXACTLY once and fails loudly on mismatch;
the script exits non-zero on any error so the build fails rather than
shipping a half-patched tree.

SPEC fix29/SPEC.md:
  ORCHESTRATOR-ONLY_F29 (extends ALWAYSLEAD_F27): every prompt is
     answered by the orchestrator model; drones never answer the user
     directly and never decide scope.
  FACTORY-DISPATCH_F29: the orchestrator keeps a queue of independent
     single-task jobs and dispatches drones into free slots — one drone
     per task, retired on completion, the next queued task dispatched
     into the freed slot; cap = what the harness supports; partition by
     file/module boundary.
  DIRECTOR-BRIEF_F29: every drone brief carries the exact goal, the
     files in scope and explicitly out of scope, constraints, acceptance
     criteria, verification steps, and what to return; an incomplete
     brief means the drone does not start.
  NO-GUESSING_F29: a drone that hits a decision its brief leaves
     unspecified stops and returns the question to the orchestrator
     instead of guessing; it never invents scope, files, or acceptance
     criteria.
  VERIFY-MERGE_F29: the orchestrator verifies every drone output
     against the brief's acceptance criteria; failed output goes back
     with a correction brief.
  GLOBAL-ROUTING_F29: automatic for ALL making/building work in every
     skill, not opt-in; byte-identical in orchestrate + hackathon-mode.
  COST-AWARE_F29: fan-out bounded by efficiency; justify N>3 in one
     line; drones carry minimal context.

HARNESS HONESTY (SPEC, Honest limits): these rules are harness-agnostic
design. In Cursor, per-subagent model selection is unreliable and in-IDE
parallelism caps around 4 with no slot refill — so live factory behavior
(per-model dispatch, slot refill at scale) is harness-gated and lights up
fully on the later port, not in Cursor. The rules are built AS DESIGNED,
not shrunk to fit Cursor. Model pins are NOT changed here (fix #30).

Anchor tokens (_F29): ORCHESTRATOR-ONLY_F29, FACTORY-DISPATCH_F29,
DIRECTOR-BRIEF_F29, NO-GUESSING_F29, VERIFY-MERGE_F29, GLOBAL-ROUTING_F29,
COST-AWARE_F29. All seven live in the built tree (GLOBAL-ROUTING block in
orchestrate + hackathon-mode; per-skill paragraphs in the 10 in-scope
skills); the patch log records the census. The in-scope skills are the 10
that dispatch implementation work: orchestrate, orch-pipeline,
orch-build-mvp, orch-add-feature, orch-change-feature, orch-fix-defect,
orch-refine-code, feature-expansion, gan-style-harness,
design-taste-frontend (audit #80-A1: its Hallmark redesign flow dispatches
one subagent per page past three pages to edit/create project files; the
routing lives in references/hallmark/references/redesign.md, with a
pointer at SKILL.md:455). Council and click-path-audit dispatch
parallel/review subagents but no implementation work — out of the
routing-line set by the SPEC's scope rule (OWED-29-3; audit #80-A rows
15-16 confirm the exclusion stands for those two).
"""
import os
import sys

BASE = sys.argv[1]
CHANGES = []
ERRORS = []
OWED = []
DECISIONS = []


def read(f):
    with open(f, encoding="utf-8") as fh:
        return fh.read()


def write(f, text):
    with open(f, "w", encoding="utf-8") as fh:
        fh.write(text)


def exists(f):
    return os.path.exists(f)


def p(rel):
    return os.path.join(BASE, rel)


def sub(f, old, new, count=1):
    """Exact replacement; record an error if the anchor does not match."""
    text = read(f)
    n = text.count(old)
    if n != count:
        ERRORS.append(f"{f}: anchor found {n}x, expected {count}x :: {old[:120]!r}")
        return
    write(f, text.replace(old, new, count))
    CHANGES.append(f"{os.path.relpath(f, BASE)}: patched anchor :: {old[:80]!r}")


# The shared pointer paragraph for the five orch-* wrappers (all run
# through the shared orch-pipeline engine; the routing lives there).
# Audit #80-B14: the pointer now states the COST-AWARE rules, not just
# the name "cost-aware fan-out".
ORCH_WRAPPER_POINTER = (
    "\n\n**Factory routing (fix #29, GLOBAL-ROUTING_F29):** this operation runs "
    "through the shared `orch-pipeline` engine, which dispatches all "
    "implementation work through the factory — see `orch-pipeline` for the "
    "routing (task queue, single-task drones, director briefs, no-guessing, "
    "verify-and-merge, cost-aware fan-out). Fan-out is bounded by efficiency: "
    "N>3 justified in one line; drones carry minimal context. The orchestrator "
    "answers every prompt; drones never answer the user or decide scope "
    "(ORCHESTRATOR-ONLY_F29)."
)

# ---------------------------------------------------------------- 1. orch-pipeline: factory paragraph + NO-GUESSING carve-out
# Audit #80-B6: briefs follow the seven-field contract in dispatch-prompt.md
# (named here; the contract itself lives in orchestrate's templates).
# Audit #80-B9: harness-gate clause on slot refill. Audit #80-B15:
# tie-breaker on the carve-out. Audit #80-B8: correction-brief
# construction in the Phase 5 Review fix-loop routing.
_f = p("skills/orch-pipeline/SKILL.md")
if exists(_f):
    sub(_f,
        "each phase names its operating skill before delegating; a decision with no named skill is refused and routed; on-skill innovation passes with its D19 reason, off-skill improvisation fails.",
        "each phase names its operating skill before delegating; a decision with no named skill is refused and routed; on-skill innovation passes with its D19 reason, off-skill improvisation fails."
        "\n\n**Factory routing (fix #29, GLOBAL-ROUTING_F29):** every phase dispatches through the factory — the orchestrator's queue of independent single-task jobs, one drone per job, retired on completion, the next queued job dispatched into the freed slot (in Cursor, slots refill per wave, not per completion — the factory lights up fully on the later port, not in Cursor) (FACTORY-DISPATCH_F29). Every drone brief is a director brief (DIRECTOR-BRIEF_F29): the exact goal, the files in scope and explicitly out of scope, constraints, acceptance criteria, verification steps, and what to return — an incomplete brief means the drone does not start. Briefs follow the seven-field contract in `skills/orchestrate/references/dispatch-prompt.md`. A drone that hits a decision its brief leaves unspecified stops and returns the question to the orchestrator instead of guessing (NO-GUESSING_F29). The orchestrator verifies every drone output against the brief's acceptance criteria and sends failed output back with a correction brief (VERIFY-MERGE_F29); fan-out is bounded by efficiency, N>3 justified in one line, drones carrying minimal context (COST-AWARE_F29). The orchestrator answers every prompt; drones never answer the user or decide scope (ORCHESTRATOR-ONLY_F29).")
    # Belief-in-the-brief vs NO-GUESSING reconciliation: 'pick the
    # reasonable option' applies only to carrying out the briefed
    # approach, never to a decision the brief leaves unspecified.
    sub(_f,
        "if a detail is ambiguous, they pick the reasonable option and note it, they don't stall.",
        "if a detail is ambiguous, they pick the reasonable option and note it, they don't stall."
        " **Bounded by NO-GUESSING (fix #29, NO-GUESSING_F29):** 'pick the reasonable option' applies only to carrying out the briefed approach, never to a decision the brief leaves unspecified — an unspecified file, scope call, or acceptance criterion is returned to the orchestrator as a question, not guessed. When in doubt which side an ambiguity falls on, return the question — a returned question is never a stall.")
    # Phase 5 Review: the fix loop's re-dispatch carries a correction
    # brief naming the failed criterion (audit #80-B8).
    sub(_f,
        "findings route to the capped 2-round fix loop (max 3 rounds total); if the app cannot run, record that as blocked with evidence instead of iterating.",
        "findings route to the capped 2-round fix loop (max 3 rounds total); the re-dispatch carries a correction brief naming the failed acceptance criterion and the required correction, distinct from the original brief; if the app cannot run, record that as blocked with evidence instead of iterating.")
else:
    ERRORS.append("skills/orch-pipeline/SKILL.md missing")

# ---------------------------------------------------------------- 2. The five orch-* wrappers: pointer to orch-pipeline
_WRAPPER_ANCHORS = {
    "orch-build-mvp": "Thin wrapper over the shared\nengine in [`orch-pipeline`](../orch-pipeline/SKILL.md).",
    "orch-add-feature": "Thin wrapper over the shared\nengine in [`orch-pipeline`](../orch-pipeline/SKILL.md).",
    "orch-fix-defect": "Thin wrapper over the shared\nengine in [`orch-pipeline`](../orch-pipeline/SKILL.md).",
    "orch-refine-code": "Thin wrapper over the shared\nengine in [`orch-pipeline`](../orch-pipeline/SKILL.md).",
    # orch-change-feature wraps the line one word earlier.
    "orch-change-feature": "Thin wrapper over the\nshared engine in [`orch-pipeline`](../orch-pipeline/SKILL.md).",
}
for _name, _anchor in _WRAPPER_ANCHORS.items():
    _f = p(f"skills/{_name}/SKILL.md")
    if exists(_f):
        sub(_f, _anchor, _anchor + ORCH_WRAPPER_POINTER)
    else:
        ERRORS.append(f"skills/{_name}/SKILL.md missing")

# ---------------------------------------------------------------- 3. gan-style-harness: factory paragraph
# Audit #80-B2: the evaluator pass is an INPUT to verification, not the
# verify step itself — the orchestrator checks generator output against
# the brief's acceptance criteria, re-checks the evaluator's pass/fail
# call, and checks the planner's spec before the first generator pass.
# Audit #80-B6: generator/evaluator briefs follow the seven-field
# contract. Audit #80-B9: harness-gate clause on slot refill.
# Audit #81-B2: the paragraph stated the verify step but the loop wiring
# (diagram + Scoring) did not carry it — the orchestrator check is
# mirrored in both, so the paragraph is not the only place it exists.
_f = p("skills/gan-style-harness/SKILL.md")
if exists(_f):
    sub(_f,
        "creating an adversarial feedback loop that drives quality far beyond what a single agent can achieve.",
        "creating an adversarial feedback loop that drives quality far beyond what a single agent can achieve."
        "\n\n**Factory routing (fix #29, GLOBAL-ROUTING_F29):** the generator/evaluator loop runs as factory drones — the orchestrator dispatches each generator and evaluator pass as a single-task drone from its queue, with a director brief (DIRECTOR-BRIEF_F29): the exact goal, the files in scope and explicitly out of scope, constraints, acceptance criteria, verification steps, and what to return — an incomplete brief means the drone does not start. Generator and evaluator briefs follow the seven-field contract in `skills/orchestrate/references/dispatch-prompt.md`. A drone that hits a decision its brief leaves unspecified stops and returns the question to the orchestrator instead of guessing (NO-GUESSING_F29). The evaluator pass is an input to verification, not the verify step itself: after each evaluator pass the orchestrator checks the generator's output against the brief's acceptance criteria (not just the rubric score — a rubric pass at or above 7.0 with a failed acceptance criterion is a fail), re-checks the evaluator's pass/fail call against the same criteria, and checks the planner's spec against the brief before the first generator pass; failed output goes back with a correction brief naming the failed criterion (VERIFY-MERGE_F29). Fan-out is bounded by efficiency, N>3 justified in one line, drones carrying minimal context (COST-AWARE_F29); in Cursor, slots refill per wave, not per completion — the factory lights up fully on the later port, not in Cursor (GLOBAL-ROUTING_F29). The orchestrator answers every prompt; drones never answer the user or decide scope (ORCHESTRATOR-ONLY_F29).")
    sub(_f,
        "## The Three Agents",
        "**Orchestrator check (fix #29, VERIFY-MERGE_F29):** the orchestrator sits outside the loop — after each evaluator pass it checks the generator's output against the brief's acceptance criteria and re-checks the evaluator's pass/fail call (a rubric pass at or above 7.0 with a failed acceptance criterion is a fail); failed output goes back with a correction brief naming the failed criterion. The planner's spec is checked against the brief before the first generator pass. The loop's CHECK SCORE step (`commands/gan-build.md` Phase 2) runs only after the orchestrator check passes.\n\n## The Three Agents")
    sub(_f,
        "- **Max iterations** = 15 (configurable, typically 5-15 sufficient)",
        "- **Max iterations** = 15 (configurable, typically 5-15 sufficient)\n- **Orchestrator check** — after each evaluator pass the orchestrator checks the generator's output against the brief's acceptance criteria (a rubric pass at or above 7.0 with a failed acceptance criterion is a fail) and re-checks the evaluator's pass/fail call; failed output goes back with a correction brief naming the failed criterion; a correction re-dispatch consumes one iteration within max iterations; the planner's spec is checked against the brief before the first generator pass")
else:
    ERRORS.append("skills/gan-style-harness/SKILL.md missing")

# ---------------------------------------------------------------- 4. Census guard: the staged GLOBAL-ROUTING block + all 10 skills
_F29_TOKENS = ("ORCHESTRATOR-ONLY_F29", "FACTORY-DISPATCH_F29",
               "DIRECTOR-BRIEF_F29", "NO-GUESSING_F29", "VERIFY-MERGE_F29",
               "GLOBAL-ROUTING_F29", "COST-AWARE_F29")
_IN_SCOPE = ("orchestrate", "orch-pipeline", "orch-build-mvp",
             "orch-add-feature", "orch-change-feature", "orch-fix-defect",
             "orch-refine-code", "feature-expansion", "gan-style-harness")
for _skill in _IN_SCOPE:
    _f = p(f"skills/{_skill}/SKILL.md")
    if not exists(_f):
        ERRORS.append(f"census: skills/{_skill}/SKILL.md missing")
        continue
    _t = read(_f)
    if "GLOBAL-ROUTING_F29" not in _t:
        ERRORS.append(f"census: skills/{_skill}/SKILL.md carries no GLOBAL-ROUTING_F29")
# design-taste-frontend (audit #80-A1): the routing lives in the Hallmark
# redesign flow, not in SKILL.md — the census checks redesign.md for the
# paragraph and SKILL.md:455 for the pointer.
_dtf = p("skills/design-taste-frontend/references/hallmark/references/redesign.md")
if not exists(_dtf):
    ERRORS.append("census: skills/design-taste-frontend/references/hallmark/references/redesign.md missing")
elif "GLOBAL-ROUTING_F29" not in read(_dtf):
    ERRORS.append("census: design-taste-frontend redesign.md carries no GLOBAL-ROUTING_F29")
_dtf_s = p("skills/design-taste-frontend/SKILL.md")
if not exists(_dtf_s):
    ERRORS.append("census: skills/design-taste-frontend/SKILL.md missing")
elif "GLOBAL-ROUTING_F29" not in read(_dtf_s):
    ERRORS.append("census: design-taste-frontend SKILL.md carries no GLOBAL-ROUTING_F29 pointer")
_hm = p("rules/hackathon-mode.mdc")
if not exists(_hm):
    ERRORS.append("census: rules/hackathon-mode.mdc missing")
elif "GLOBAL-ROUTING_F29" not in read(_hm):
    ERRORS.append("census: rules/hackathon-mode.mdc carries no GLOBAL-ROUTING_F29")
# The block text itself must be byte-identical in orchestrate + hackathon-mode.
_orch = read(p("skills/orchestrate/SKILL.md")) if exists(p("skills/orchestrate/SKILL.md")) else ""
_hm_t = read(_hm) if exists(_hm) else ""
if _orch and _hm_t:
    def _block(text):
        _i = text.find("**GLOBAL-ROUTING")
        if _i < 0:
            return None
        _j = text.find("\n", _i)
        return text[_i:_j] if _j > _i else text[_i:]
    _b1, _b2 = _block(_orch), _block(_hm_t)
    if _b1 is None or _b2 is None:
        ERRORS.append("census: GLOBAL-ROUTING block not found in orchestrate or hackathon-mode")
    elif _b1 != _b2:
        ERRORS.append("census: GLOBAL-ROUTING block differs between orchestrate and hackathon-mode")
    else:
        CHANGES.append("census: GLOBAL-ROUTING block byte-identical in orchestrate + hackathon-mode")
    # All seven tokens must appear in the block.
    for _tok in _F29_TOKENS:
        if _b1 is None or _tok not in _b1:
            ERRORS.append(f"census: GLOBAL-ROUTING block missing token {_tok}")
    CHANGES.append("census: all 10 in-scope skills + hackathon-mode carry GLOBAL-ROUTING_F29; all 7 _F29 tokens in the block")

# ---------------------------------------------------------------- 5. Audit #80 follow-ups in ECC-origin files
# 5a. orch-build-mvp: the third Belief sentence gets the same NO-GUESSING
# carve-out + tie-breaker (audit #80-A2 / #80-B4), and the third
# merge-order site gets the factory bridge (audit #80-A3 / #80-B7).
_f = p("skills/orch-build-mvp/SKILL.md")
if exists(_f):
    sub(_f,
        "if a detail is ambiguous, they pick the reasonable option and note it, they don't stall.",
        "if a detail is ambiguous, they pick the reasonable option and note it, they don't stall."
        " **Bounded by NO-GUESSING (fix #29, NO-GUESSING_F29):** 'pick the reasonable option' applies only to carrying out the briefed approach, never to a decision the brief leaves unspecified — an unspecified file, scope call, or acceptance criterion is returned to the orchestrator as a question, not guessed. When in doubt which side an ambiguity falls on, return the question — a returned question is never a stall.")
    sub(_f,
        "If two implementers in the same wave touched the same files, decide the merge order — the first-listed implementer's files win on conflict unless the planner marked a dependency (then the dependency's files win) — record the decision in `.hackathon/run-ledger.md`, and dependents proceed on the merged result.",
        "If two implementers in the same wave touched the same files, decide the merge order — the first-listed implementer's files win on conflict unless the planner marked a dependency (then the dependency's files win) — record the decision in `.hackathon/run-ledger.md`, and dependents proceed on the merged result. This procedure applies only if partitioning failed and two implementers touched the same file anyway — sequential dispatch for overlapping scopes is the prevention rule (GLOBAL-ROUTING_F29).")
else:
    ERRORS.append("skills/orch-build-mvp/SKILL.md missing")
# 5b. orch-refine-code: the step-2 refactor-cleaner sweep is dispatched
# directly, not through the engine — it runs as a single-task factory
# drone with a director brief (audit #80-A4). Same qualification in the
# command mirror (commands/orch-refine-code.md:33). Audit #81-A4: the
# line-13 pointer itself still claimed ALL work runs "through the engine"
# while step 2 concedes the sweep applies "not only through the engine" —
# the pointer (and the mirror's "via the engine" framing) is qualified
# here with the exception, appended after the shared pointer text so the
# full-pointer assertion in verify29 still matches.
_f = p("skills/orch-refine-code/SKILL.md")
if exists(_f):
    sub(_f,
        "2. For dead-code / duplication sweeps, delegate to the `refactor-cleaner` agent (`agents/ecc-refactor-cleaner.md`)\n   (it runs knip / depcheck / ts-prune and removes safely).",
        "2. For dead-code / duplication sweeps, delegate to the `refactor-cleaner` agent (`agents/ecc-refactor-cleaner.md`)\n   (it runs knip / depcheck / ts-prune and removes safely). Dispatched as a single-task factory drone with a director brief (goal, files in/out of scope, constraints, acceptance criteria, verification steps, what to return; GLOBAL-ROUTING_F29) — the sweep is implementation work, so the factory rules apply to it directly, not only through the engine.")
    sub(_f,
        "The orchestrator answers every prompt; drones never answer the user or decide scope (ORCHESTRATOR-ONLY_F29).",
        "The orchestrator answers every prompt; drones never answer the user or decide scope (ORCHESTRATOR-ONLY_F29). Except the step-2 refactor-cleaner sweep, which is dispatched directly as a single-task factory drone — see step 2.")
else:
    ERRORS.append("skills/orch-refine-code/SKILL.md missing")
_f = p("commands/orch-refine-code.md")
if exists(_f):
    sub(_f,
        "Dead-code/dup sweeps\n   delegate to `refactor-cleaner` agent (`agents/ecc-refactor-cleaner.md`).",
        "Dead-code/dup sweeps\n   delegate to `refactor-cleaner` agent (`agents/ecc-refactor-cleaner.md`) — dispatched as a single-task factory drone with a director brief (GLOBAL-ROUTING_F29).")
    sub(_f,
        "The skill\n(via the shared `orch-pipeline` engine) will:",
        "The skill\n(via the shared `orch-pipeline` engine — except the step-3 refactor-cleaner sweep, which the skill dispatches directly as a single-task factory drone) will:")
else:
    ERRORS.append("commands/orch-refine-code.md missing")
# 5c. rules/common-agents.mdc (alwaysApply): implementation-agent dispatch
# follows the factory routing (audit #80-A5). The rule already defers to
# "the orchestrate skill's routing rule"; this names the fix #29 factory
# paragraph explicitly. Audit #81-A6: the 80-B14 COST-AWARE standard
# (state both rules, not just the name) is applied here too.
_f = p("rules/common-agents.mdc")
if exists(_f):
    sub(_f,
        "No user prompt needed — subject to the orchestrate skill's routing rule, which governs this list too:",
        "No user prompt needed — subject to the orchestrate skill's routing rule, which governs this list too:\n\nImplementation-agent dispatch follows the factory routing in orchestrate's GLOBAL-ROUTING block (fix #29, GLOBAL-ROUTING_F29): every implementation dispatch carries a director brief, no-guessing applies, and the orchestrator verifies the output against the brief's acceptance criteria before use. Fan-out is bounded by efficiency: N>3 justified in one line; drones carry minimal context.")
else:
    ERRORS.append("rules/common-agents.mdc missing")
# 5d. commands/gan-build.md: the actual launch site of the code-writing
# gan-generator carries no F29 pointer (audit #80-A6). Pointer at the
# top; files out of scope named in the generator launch block.
# Audit #81-A6: the pointer states the COST-AWARE rules (80-B14 standard).
# Audit #81-A7: the out-of-scope line named "the brief", but the only
# brief in the command is the user's one-line description, which cannot
# name files — the orchestrator names them from the spec before launch.
# Audit #81-B2: the Phase 2 loop terminated on the rubric score with no
# orchestrator verify step in its wiring — an ORCHESTRATOR-CHECK step is
# added between EVALUATE and CHECK SCORE, and a planner-spec check at
# the end of Phase 1 (against the existing spec on the --skip-planner
# path), each with the correction-brief failure path.
_f = p("commands/gan-build.md")
if exists(_f):
    sub(_f,
        "## GAN-Style Harness Build",
        "**Factory routing (fix #29, GLOBAL-ROUTING_F29):** the planner, generator, and evaluator passes below run as factory drones per `gan-style-harness` — each with a director brief (goal, files in/out of scope, constraints, acceptance criteria, verification steps, what to return), no-guessing, and orchestrator verification against the brief's acceptance criteria (a rubric pass with a failed acceptance criterion is a fail). Fan-out is bounded by efficiency: N>3 justified in one line; drones carry minimal context.\n\n## GAN-Style Harness Build")
    sub(_f,
        "- Read spec.md and `docs/design-tokens.md` (the tokens file carries the decision record's direction; on any divergence between spec.md and the tokens file, the record's direction — as carried in the tokens file — wins: spec.md is derived from the record/scope, so a divergence means the translation drifted and the record is authoritative; never re-derive a direction from spec.md alone)",
        "- Read spec.md and `docs/design-tokens.md` (the tokens file carries the decision record's direction; on any divergence between spec.md and the tokens file, the record's direction — as carried in the tokens file — wins: spec.md is derived from the record/scope, so a divergence means the translation drifted and the record is authoritative; never re-derive a direction from spec.md alone)\n    - Files out of scope: [named by the orchestrator from the spec before launch; `none` if genuinely none] — the generator touches only the spec's files.")
    sub(_f,
        "3. Display the spec summary to the user\n4. Proceed to Phase 2",
        "3. Display the spec summary to the user\n3a. Orchestrator checks the planner's spec against the brief before Phase 2 (on the `--skip-planner` path, against the existing `gan-harness/spec.md`): the spec's files, scope, and acceptance criteria must match the brief's goal, files in/out of scope, constraints, and acceptance criteria. If the spec fails the check, the planner is re-dispatched with a correction brief naming the failed criterion and the required correction, distinct from the original brief (at most two correction re-dispatches, per the plugin's 2-round fix-loop convention; if the spec still fails, stop and report the failure with evidence).\n4. Proceed to Phase 2")
    sub(_f,
        "    # Wait for evaluator to finish\n\n    # CHECK SCORE",
        "    # Wait for evaluator to finish\n\n    # ORCHESTRATOR-CHECK\n    After each evaluator pass, the orchestrator checks the generator's output against the brief's acceptance criteria (not just the rubric score — a rubric pass at or above 7.0 with a failed acceptance criterion is a fail) and re-checks the evaluator's pass/fail call against the same criteria. A rubric pass with a failed acceptance criterion is a fail: the generator is re-dispatched with a correction brief naming the failed criterion and the required correction, distinct from the original brief — the re-dispatch is the next iteration's GENERATE, consuming one iteration within max_iterations; skip CHECK SCORE and continue the loop. A rubric fail the orchestrator finds actually passes the criteria is a re-check, not a loop exit: the evaluator's call is corrected and the loop continues to CHECK SCORE.\n\n    # CHECK SCORE — runs only after the orchestrator check above passes")
    # Audit #82-B1: the GENERATE block is the generator's only dispatch
    # text and still lacks the Verification steps + Return format slots
    # (5/7 as a standalone brief) — both added here, mirroring the
    # mechanical template's return format.
    sub(_f,
        "    - Ensure dev server is running\n    - Commit changes",
        "    - Ensure dev server is running\n    - Commit changes\n    - Verification steps: run the TDD tests you wrote plus the acceptance criteria from the spec — paste the test output; the build must pass and the acceptance criteria must hold before finishing.\n    - Return format: Status first, then files changed, test output, concerns.")
    # Audit #82-A1 (option (a)): pin the step-0 execution reading — the
    # design-lead is invoked inline as the orchestrator, not spawned.
    sub(_f,
        "and record it in `docs/design-tokens.md`, then launch the planner with that recorded direction.",
        "and record it in `docs/design-tokens.md` (the design-lead is invoked inline as the orchestrator here, not spawned as a drone — a spawned execution must carry a director brief), then launch the planner with that recorded direction.")
else:
    ERRORS.append("commands/gan-build.md missing")

# ---------------------------------------------------------------- 5e. commands/gan-design.md: the twin step-0 design-direction
# dispatch (audit #83-A1). Setup step 0 carries the verbatim twin of
# gan-build step 0 with no inline pin and zero _F29 tokens, and the
# MANIFEST record named only gan-build. Same parenthetical as §5d.
# (Audit #80-A row 25's "No launch/subagent lines" claim for gan-design
# was false — step 0 is a dispatch line; it escaped all prior rounds
# because `dispatch` is not in the base-pattern grep set.)
# Audit #84-A1: the 83-A1 fix added the parenthetical but no _F29 token,
# so the file still greps as uncovered. Add a one-line factory pointer
# mirroring gan-build.md:12 (step-0 inline reading named, loop defers to
# the gan-build pointer) after the arg-parse block.
_f = p("commands/gan-design.md")
if exists(_f):
    sub(_f,
        "and record it in `docs/design-tokens.md`, then restate that recorded direction in the brief/spec and proceed.",
        "and record it in `docs/design-tokens.md` (the design-lead is invoked inline as the orchestrator here, not spawned as a drone — a spawned execution must carry a director brief), then restate that recorded direction in the brief/spec and proceed.")
    sub(_f,
        "3. `--pass-threshold N` — (optional, default 7.5) weighted score to pass (higher default for design)\n\n## GAN-Style Design Harness",
        "3. `--pass-threshold N` — (optional, default 7.5) weighted score to pass (higher default for design)\n\n**Factory routing (fix #29, GLOBAL-ROUTING_F29):** the design-lead is invoked inline as the orchestrator in Setup step 0 (not spawned as a drone — a spawned execution must carry a director brief); the generator/evaluator loop below runs as factory drones per the `/gan-build` pointer, each with a director brief (goal, files in/out of scope, constraints, acceptance criteria, verification steps, what to return), no-guessing, and orchestrator verification against the brief's acceptance criteria.\n\n## GAN-Style Design Harness")
else:
    ERRORS.append("commands/gan-design.md missing")
# ---------------------------------------------------------------- 5f. agents/ecc-gan-planner.md: the planner fallback
# (audit #83-A2). Direction source told the planner drone to invoke the
# design-lead itself if launched with no direction recorded — but a drone
# cannot execute the 82-A1 inline-as-orchestrator reading, because the
# planner is not the orchestrator. Re-routed (option (a)): the planner
# stops and returns NEEDS_CONTEXT naming the missing direction to the
# orchestrator, which invokes the design-lead inline and re-dispatches.
# Pre-existing from the fix28 base, not a fix #29 regression.
_f = p("agents/ecc-gan-planner.md")
if exists(_f):
    sub(_f,
        "if this agent is ever launched with no direction recorded, invoke the design-lead (model `grok-4.7-high`) to generate it through the package skills and record it in `docs/design-tokens.md` first, then copy it here",
        "if this agent is ever launched with no direction recorded, STOP and return NEEDS_CONTEXT naming the missing direction to the orchestrator instead of invoking the design-lead itself — the orchestrator invokes the design-lead inline (per the design-package rule) and re-dispatches this agent with the recorded direction, then copy it here")
else:
    ERRORS.append("agents/ecc-gan-planner.md missing")

# ---------------------------------------------------------------- 5g. commands/react-build.md: the react-build-resolver launch
# site (audit #86-A1, blocking). The command's whole purpose is invoking
# the file-writing react-build-resolver agent (drone tier,
# cursor-grok-4.6-high-fast) to fix React build errors with minimal
# surgical file edits — a live implementation dispatch with zero _F29
# coverage in the command or the agent file, and the resolver is not in
# the common-agents.mdc governed list (only the generic
# build-error-resolver is). It escaped rounds 1-6 because "invokes" is
# not in the base-pattern grep set — the same escape class as 83-A1
# (gan-design's "dispatch"). Same treatment as the gan-build precedent
# (§5d): a one-line factory pointer after the invocation line.
# Audit #87-B1 (blocking): the pointer claims orchestrator verification
# but the command has no orchestrator verify step and no correction-brief
# path — the resolver's own re-run build is the only check (the 81-B2
# structural defect). A step 6 is added after the resolver's report:
# the commanding agent verifies the output against the brief's acceptance
# criteria and re-dispatches with a correction brief on a failed
# criterion, capped at two re-dispatches per the plugin's 2-round
# fix-loop convention.
_f = p("commands/react-build.md")
if exists(_f):
    sub(_f,
        "This command invokes the **react-build-resolver** agent to incrementally fix React build errors with minimal changes.\n\n## What This Command Does",
        "This command invokes the **react-build-resolver** agent to incrementally fix React build errors with minimal changes.\n\n**Factory routing (fix #29, GLOBAL-ROUTING_F29):** the react-build-resolver runs as a single-task factory drone with a director brief (goal, files in/out of scope, constraints, acceptance criteria, verification steps, what to return), no-guessing, and orchestrator verification against the brief's acceptance criteria (the re-run build is evidence, not the verdict). Fan-out is bounded by efficiency: N>3 justified in one line; drones carry minimal context.\n\n## What This Command Does")
    sub(_f,
        "5. **Report Summary**: Show what was fixed and what remains",
        "5. **Report Summary**: Show what was fixed and what remains\n6. **Orchestrator Verify**: After the resolver reports, the commanding agent verifies the resolver's output against the brief's acceptance criteria — the build is green AND the changes are minimal in scope AND no suppression (`// @ts-ignore`, disabled type-checking) lacks an explanation. A green build with a failed acceptance criterion is a fail. On a failed criterion, re-dispatch the resolver with a correction brief naming the failed acceptance criterion and the required correction, distinct from the original brief (at most two correction re-dispatches; past that, report the remaining issue as blocked with evidence).")
else:
    ERRORS.append("commands/react-build.md missing")

# ---------------------------------------------------------------- 5h. commands/astra-review.md: the Step 3 fix cycle (audit
# #90-A1, blocking). The command was triaged review-only in every prior
# round on the strength of step 2 (blind review, :24) alone — but step 3
# dispatches implementation work: fixes go to fast-worker (mechanical)
# or back to deep-reasoner (architectural), both file-writing subagent
# roles with subagent-tier pins, with zero _F29 coverage. It escaped
# rounds 1-10 because "Fixes go to X" is a role-routing sentence with no
# dispatch verb at all — a new escape class in the 83-A1/86-A1 family.
# Same treatment as the react-build precedent (§5g): a one-line factory
# pointer after the :32 fix-cycle line. Audit #87-B1 lesson applied to
# the verification claim: the pointer names the second blind pass as the
# orchestrator verification, so :33 is extended to name the fix brief's
# acceptance criteria as what the pass checks (a zero-blocker verdict
# with a failed criterion is a fail) and to construct the correction
# brief on a failed criterion, capped at two re-dispatches per the
# plugin's 2-round fix-loop convention.
_f = p("commands/astra-review.md")
if exists(_f):
    sub(_f,
        "- Fixes go to **fast-worker** (`cursor-grok-4.6-high-fast`) for mechanical fixes, or back to **deep-reasoner** (`grok-4.7-high`) for architectural ones.",
        "- Fixes go to **fast-worker** (`cursor-grok-4.6-high-fast`) for mechanical fixes, or back to **deep-reasoner** (`grok-4.7-high`) for architectural ones.\n\n**Factory routing (fix #29, GLOBAL-ROUTING_F29):** the fast-worker/deep-reasoner fix runs as a single-task factory drone with a director brief (goal, files in/out of scope, constraints, acceptance criteria, verification steps, what to return), no-guessing, and orchestrator verification against the brief's acceptance criteria (the second blind pass is the verification — a zero-blocker verdict with a failed acceptance criterion is a fail). Fan-out is bounded by efficiency: N>3 justified in one line; drones carry minimal context.")
    sub(_f,
        "- After fixes, run a **second blind deep-reasoner pass** over the fixed diff to re-verify (the second-pass pattern replaces any second-model peer review).",
        "- After fixes, run a **second blind deep-reasoner pass** over the fixed diff to re-verify against the fix brief's acceptance criteria (the second-pass pattern replaces any second-model peer review; a zero-blocker verdict with a failed acceptance criterion is a fail). On a failed criterion, re-dispatch the fixer with a correction brief naming the failed acceptance criterion and the required correction, distinct from the original brief (at most two correction re-dispatches; past that, report the remaining issue as blocked with evidence).")
else:
    ERRORS.append("commands/astra-review.md missing")

# ---------------------------------------------------------------- OWED (recorded, not patched blindly)
OWED = [
    "OWED-29-1 (SPEC §6): the call map (skills/orchestrate/references/call-map.md) is generator-owned and NOT regenerated in this fix — the routing adds no new dispatch edges (no new skill invocations), counts are unchanged (67/45/48/55/15/49), and the fix28 map stands. Verified by regenerating twice with the fix28 generator copy and diffing: 2-line diff (error-handling purpose-order noise + one pre-existing git-workflow staged invoker), neither a fix #29 edge; the fix28 map was restored byte-identical (md5 b066413a…) — see MANIFEST §2(d).",
    "OWED-29-2 (SPEC Honest limits): live factory behavior (per-model dispatch, slot refill at scale) is harness-gated — in Cursor, per-subagent model selection is unreliable and in-IDE parallelism caps around 4 with no slot refill. The dry-run factory leg verifies the design statically (partitioning, brief completeness, no-guessing, merge/verification), not live Cursor dispatch. It lights up fully on the later port.",
    "OWED-29-3 (SPEC §1 scope rule, corrected by audit #80-A1): council and click-path-audit dispatch parallel/review subagents but no implementation work, so they carry no factory routing line (audit #80-A rows 15-16 confirm). design-taste-frontend was wrongly in this list — its Hallmark redesign flow dispatches implementation subagents, so it is in the routing set (10 skills) with the paragraph in redesign.md. Recorded for the audit to challenge: if the audit finds an implementation dispatch in council or click-path-audit, it belongs in the routing set.",
    "OWED-29-4 (fix #30 handoff): the DeepSeek/Qwen model assignment in the GLOBAL-ROUTING block is a forward reference to fix #30; no model pins change in this fix. verify29 asserts the Grok pins are unchanged and no deepseek-/qwen- model slugs exist in the built tree.",
    "OWED-29-5 (audit #80-B13, partially rejected; enumeration corrected per audit #91-B nit 2): the 41 staged-vs-built diff lines across 4 files (orchestrate :100/:274/:281 agent-citation expansions, hackathon-mode :38 `claude -p` -> CLI-subprocess, feature-expansion 11 changed lines, design-taste-frontend description block 5 lines -> 6) are BY-DESIGN build-time transforms, NOT synced — fix16.py:3808 anchors on the staged `claude -p` wording with count==1 and fails the build (exit 1) if the anchor misses, so syncing staged to the built text would break the build. No full-file staged-vs-built identity check is added; verify29 instead asserts the _F29 lines are byte-identical staged-vs-built (the actual fix #29 regression risk).",
]

# ---------------------------------------------------------------- main / run log
_log_lines = ["# fix29 run log", "",
              f"## Errors ({len(ERRORS)})"]
_log_lines += [f"- {e}" for e in ERRORS] or ["- none"]
_log_lines += ["", f"## Changes ({len(CHANGES)})"]
_log_lines += [f"- {c}" for c in CHANGES] or ["- none"]
_log_lines += ["", f"## Command decisions ({len(DECISIONS)})"]
_log_lines += [f"- {d}" for d in DECISIONS] or ["- none"]
_log_lines += ["", f"## OWED ({len(OWED)})"]
_log_lines += [f"- {o}" for o in OWED] or ["- none"]
_log_dir = os.path.join(os.path.dirname(BASE.rstrip("/")), "fix29")
os.makedirs(_log_dir, exist_ok=True)
with open(os.path.join(_log_dir, "fix29-patch-log.md"), "w", encoding="utf-8") as _fh:
    _fh.write("\n".join(_log_lines) + "\n")
print(f"fix29: {len(CHANGES)} change(s)")
for c in CHANGES:
    print(f"  - {c}")
print(f"fix29: {len(OWED)} OWED item(s) recorded in the patch log")
if ERRORS:
    print(f"fix29: {len(ERRORS)} ERROR(S)", file=sys.stderr)
    for e in ERRORS:
        print(f"  ! {e}", file=sys.stderr)
    sys.exit(1)
print("fix29: OK")
