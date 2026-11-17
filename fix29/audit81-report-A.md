# Audit #81-A — Fix #29 (adaptable orchestration): dispatch coverage, round 2

**Date:** Mon 2026-11-16
**Auditor scope (Auditor A):** dispatch coverage only — verify every audit #80-A finding is actually fixed; re-hunt dispatch coverage with fresh eyes (including `references/` subdirectories, `commands/`, `rules/`, `agents/`); challenge the coordinator's scoping decisions; check the GLOBAL-ROUTING block byte-identity, the 10-skill census, and build consistency (staged vs built).
**Sources read in full:** `fix29/SPEC.md`, `fix29/MANIFEST.md`, `fix29/audit80-report-A.md`, `fix29/audit80-report-B.md`, `fix29/fix29.py`, `fix29/verify29.py` (re-run independently — see below).
**Method:** re-checked each 80-A file:line in the built tree; grepped the whole built tree (`hackathon-ecc/`) for `spawn|subagent|sub-agent|Task tool|delegate|delegat|implementer` (167 hits, vs 166 in #80-A) plus follow-up greps for `dispatch`, `launch|parallel|fresh-context|isolated`, and agent-file dispatch; read every new hit in context. Read-only; no file under `~/workspace/hackathon-plugin/` was edited except this report.

## Verdict: NOT PASS — 0 blocking, 8 minor

All seven #80-A findings are fixed in substance — the routing set is genuinely 10, all five Belief copies are carved, the merge-order bridges, the refactor-cleaner qualification, the common-agents line, the gan-build pointer, and the OWED-29-1 text are all present. What round 2 found is that the fixes are incomplete at their edges: the one filled brief example still omits a DIRECTOR-BRIEF field (81-A1), the redesign single-writer rule has no operative linkage to the brief that would enforce it (81-A2), the redesign paragraph is the one factory paragraph without a harness-gate clause (81-A3), the orch-refine-code pointer still overclaims (81-A4), the second-pass template has no under-specification path (81-A5), two pointers omit the COST-AWARE rules (81-A6), the gan-build out-of-scope line points at a brief that cannot name files (81-A7), and the gan-build step-0 design dispatch escapes the pointer's enumeration (81-A8). None is blocking — the normative templates and paragraphs are correct — but each is a live instruction a brief-writer or drone will follow literally, and 81-A1 additionally requires a verifier change (check 7d bakes the omission in as `== 4`).

## #80-A disposition — every finding re-checked

| #80-A | Status | Evidence |
|---|---|---|
| 80-A1 (blocking): design-taste-frontend routing set 9 → 10 | **VERIFIED-FIXED** | Factory paragraph in `skills/design-taste-frontend/references/hallmark/references/redesign.md:68` ("each page subagent is a single-task factory drone with a director brief"); pointer at `skills/design-taste-frontend/SKILL.md:455` ("factory routing for the redesign flow lives there: page subagents are single-task factory drones with director briefs (GLOBAL-ROUTING_F29)"); `fix29.py` docstring + census guard list 10 skills. Residuals filed as new minors 81-A2, 81-A3. |
| 80-A2 (blocking): NO-GUESSING reconciliation, 5 Belief copies + first-build carve-out | **VERIFIED-FIXED** | All 5 "pick the reasonable option" copies now carry the carve-out + tie-breaker (`orch-pipeline:72`, `feature-expansion:151`, `orch-build-mvp:70`, `dispatch-prompt.md:34`, `dispatch-prompt.md:92`); `instead of NEEDS_CONTEXT` count is 0 tree-wide; first-build carve-out reconciled at all 6 sites in `dispatch-prompt.md` (status vocabulary :50–55, mechanical preamble :94–97, "Before you begin" :115–118, reasoning template :144–146, worked example :202–205 and :224–227) — the question goes to the orchestrator, never the user. |
| 80-A3 (minor): orch-build-mvp merge-order bridge | **VERIFIED-FIXED** | `skills/orch-build-mvp/SKILL.md:71`: "This procedure applies only if partitioning failed and two implementers touched the same file anyway — sequential dispatch for overlapping scopes is the prevention rule (GLOBAL-ROUTING_F29)." All 3 merge-order sites now bridged. |
| 80-A4 (minor): orch-refine-code direct refactor-cleaner dispatch | **VERIFIED-FIXED** (substance) | Step-2 qualification present at `skills/orch-refine-code/SKILL.md:35` ("Dispatched as a single-task factory drone with a director brief … the factory rules apply to it directly, not only through the engine") and in the command mirror (`commands/orch-refine-code.md`, step 3). Residual: the :13 pointer itself was never qualified — new minor 81-A4. |
| 80-A5 (minor): common-agents.mdc unrecorded | **VERIFIED-FIXED** | Factory line present at `rules/common-agents.mdc:26`. Residual: no COST-AWARE clause — new minor 81-A6. |
| 80-A6 (minor): commands/gan-build.md no pointer | **VERIFIED-FIXED** | Pointer at `commands/gan-build.md:12` + out-of-scope line at `:40`. Residuals: placeholder unresolvable (81-A7), step-0 design dispatch outside the pointer's enumeration (81-A8), no COST-AWARE clause (81-A6). |
| 80-A7 (minor): fix29.py OWED-29-1 contradiction | **VERIFIED-FIXED** | `fix29/fix29.py:292` and `fix29/fix29.py.template:292` both now read "2-line diff (error-handling purpose-order noise + one pre-existing git-workflow staged invoker)". |

## Findings

### 81-A1 — MINOR: the worked example in `dispatch-prompt.md` still omits the Verification steps field (80-B3 fix incomplete where briefs are actually copied from)

**Evidence.**

- `skills/orchestrate/references/dispatch-prompt.md:195–221` (Worked example — mechanical tier, fallback path, filled) lists exactly six contract fields: `Goal:` (:210), `Inputs:` (:212), `Constraints:` (:215), `Interface:` (:216), `Acceptance check:` (:218), `Return format:` (:220). There is **no `Verification steps:` line** between the Acceptance check and the Return format. Its Constraints also name out-of-scope files only inline — "Do not modify function bodies. Do not touch `src/auth/tokens.go` or `src/auth/store.go`." — without the `files out of scope` label the other three templates carry.
- `grep -c "Verification steps" skills/orchestrate/references/dispatch-prompt.md` = **4** (skeleton :15 + recon :71 + mechanical :107 + reasoning :139). The worked example is the fifth brief-shaped block and is not counted.

**Why it matters.** The skeleton (:15) and the three implementation templates are correct, but the worked example is the one *filled* brief in the file — the concrete model a brief-writer copies when composing a dispatch. A brief composed from it carries six fields, not seven, and therefore violates DIRECTOR-BRIEF_F29's "an incomplete brief means the drone does not start" while looking complete. Worse, the verifier bakes the omission in: `fix29/verify29.py` check 7d asserts `_dp.count("Verification steps") == 4` and `_dp.count("files out of scope") == 4`, so adding the field to the worked example would make the counts 5 and **fail** the verifier as written — the gap is asserted-correct, not just unasserted.

**Fix.** Add a `Verification steps:` line (distinct from the Acceptance check) and a `files out of scope:` label to the worked example's Constraints in `dispatch-prompt.md:210–221`; update verify29 check 7d counts from 4 to 5 for both strings.

### 81-A2 — MINOR: the redesign.md single-writer rule asserts the outcome but never states the mechanism that enforces it

**Evidence.**

- `skills/design-taste-frontend/references/hallmark/references/redesign.md:68`: "The shared stylesheet and tokens files (`app/globals.css`, `app/tokens.css`, `app/base.css`, `docs/design-tokens.md`) are single-writer: locked once before page fan-out (or written by one named drone) — no two page drones share files (FACTORY-DISPATCH_F29)."
- The same line's dispatch instruction hands the shared file to *every* page drone without a read-only qualifier: "Past three pages, give each page to its own subagent where the harness has them, with that tokens file, the page's files and this file."
- The paragraph requires each page brief to carry "the page's files in scope and explicitly out of scope" but never says the shared stylesheet/tokens files go in the **out-of-scope slot** of every page brief.

**Why it matters.** This was the core hazard of 80-A1 (blocking): pages share mutable state, so partition-by-boundary is violated by construction unless the briefs serialize the shared files. The fix states the *rule* (single-writer) but not the *operation* that makes it true. Three gaps: (1) "locked once" is passive — no named locker (the orchestrator? the design-lead?) and no cross-reference to the "lock the system once the scaffold has run" instruction in the first half of the same line, so a reader cannot tell whether the lock is a step that happens or a property that holds; (2) "or written by one named drone" names no selection rule and no timing (before, during, or after page fan-out?); (3) the tokens file is an *input* to every page drone as written, while the Files block (`redesign.md:55–60`, "create: app/tokens.css, app/base.css") shows page drones creating tokens files — so a brief-writer following the paragraph literally can still put `app/tokens.css` in scope for a page drone, and the only defence is the orchestrator's verification catching it after the fact. The out-of-scope slot is the enforcement mechanism, and the paragraph never connects the shared files to it.

**Fix.** Add one sentence to the `redesign.md:68` paragraph: the shared stylesheet/tokens files are listed **out of scope in every page brief** and the tokens file is passed to page drones **read-only**; the orchestrator locks the system once the scaffold has run (per the first half of the same line) before fan-out, or names the single writer drone and its timing before fan-out.

### 81-A3 — MINOR: the redesign.md factory paragraph is the only factory paragraph with no harness-gate clause and no queue/slot sentence

**Evidence.**

- `grep -rn "slots refill per wave" hackathon-ecc/` returns exactly 4 hits: `skills/orch-pipeline/SKILL.md:62`, `skills/feature-expansion/SKILL.md:139`, `skills/gan-style-harness/SKILL.md:14`, `skills/orchestrate/SKILL.md:93`. The `redesign.md:68` factory paragraph contains neither "slots refill per wave" nor any queue/slot language — it calls each page subagent "a single-task factory drone" and cites `FACTORY-DISPATCH_F29` only for the no-shared-files rule.
- `fix29/verify29.py` lines 676–681 assert the harness-gate clause in exactly those same 4 places (`orch-pipeline`, `feature-expansion`, `gan-style-harness`, orchestrate step 4); `redesign.md` is not in the list. The verifier's redesign checks (:684–689) assert only the paragraph, the single-writer sentence, and the SKILL.md pointer.

**Why it matters.** MANIFEST §2(c)(8) records the harness-gate clause as carried by "each paragraph (orch-pipeline, feature-expansion, gan) and orchestrate step 4" — true as enumerated, but the redesign paragraph is a fifth factory paragraph added after #80, and the task brief describes "harness-gate clauses in every factory paragraph" as one of the round-2 changes. A reader of `redesign.md` alone gets no warning that in Cursor the page fan-out does not refill per completion. Mitigating (hence minor, not blocking): the paragraph states no retire-and-refill claim to correct — it has no queue mechanics at all — and the dispatch line hedges with "where the harness has them", so the omission is a consistency gap, not a live overclaim.

**Fix.** Add the harness-gate clause ("in Cursor, slots refill per wave, not per completion — the factory lights up fully on the later port, not in Cursor") and one queue sentence to the `redesign.md:68` paragraph, and add `redesign.md` to the verifier's harness-gate list. Alternatively record explicitly that redesign fan-out is one-shot per page with no refill claim, so the omission is a decision, not an oversight.

### 81-A4 — MINOR: the orch-refine-code pointer still claims all implementation work runs "through the shared engine" (80-A4 residual — step 2 was qualified, the pointer was not)

**Evidence.**

- `skills/orch-refine-code/SKILL.md:13` (pointer, unchanged by the #80 fix): "**Factory routing (fix #29, GLOBAL-ROUTING_F29):** this operation runs through the shared `orch-pipeline` engine, which dispatches all implementation work through the factory".
- `skills/orch-refine-code/SKILL.md:35` (step 2, the fix): "Dispatched as a single-task factory drone with a director brief … — the sweep is implementation work, so the factory rules apply to it directly, **not only through the engine**." (Emphasis added.)
- Same overclaim in the command mirror, `commands/orch-refine-code.md`: "The skill (**via the shared `orch-pipeline` engine**) will: … 3. … Dead-code/dup sweeps delegate to `refactor-cleaner` agent".

**Why it matters.** 80-A4 offered two fixes: route the sweep through the engine, *or* "qualify the line-13 pointer … and add the brief requirement to step 2". The coordinator did the second half of the second option (step 2) but not the first half (the pointer). Step 2's own wording concedes the pointer is inaccurate — the sweep applies "not only through the engine", i.e. not through the engine at all. The substance is now correct (the sweep IS a factory drone with a director brief), so this is a one-sentence accuracy defect, not a routing gap — but the pointer is the sentence a reader trusts first, and it still says "all … through the engine".

**Fix.** Qualify the pointer at `orch-refine-code/SKILL.md:13` ("except the step-2 refactor-cleaner sweep, which is dispatched directly as a single-task factory drone — see step 2") and the command mirror's "via the shared `orch-pipeline` engine" framing the same way.

### 81-A5 — MINOR: the second-pass template has no under-specification path — the exemption from the seven-field contract is sound, the missing NEEDS_CONTEXT line is not

**Evidence.**

- `skills/orchestrate/references/dispatch-prompt.md:150–160` (Template — second deep-reasoner pass): "You are a senior engineer giving an independent second opinion. Assume no shared context with the other pass: everything you need is in this prompt. Context: [one line] Task: [the task body — on the blind-parallel path this text must be VERBATIM identical to what the first deep-reasoner received] Constraints: [same constraints the other executor got] Return: conclusion first, then the load-bearing reasons, then what would make you wrong. Conclusion + evidence, ≤20 lines." No `NEEDS_CONTEXT`, no NO-GUESSING line anywhere in the template.
- Contrast the first pass on the *verbatim-identical* task body — the reasoning template, `dispatch-prompt.md:144`: "If under-specified: return NEEDS_CONTEXT naming exactly what is missing — do not guess."
- `skills/orchestrate/SKILL.md:289–291` (the blind-parallel path): "launch two deep-reasoner subagents on the same problem, in one message, blind to each other. The task body sent to both must be **verbatim identical** … A disagreement on this path stops the run."

**Why it matters.** The coordinator's recorded scoping decision (MANIFEST §2(c)(6)) exempts the second-pass and blind-reviewer templates from the seven-field contract because they "carry their own contract (opinion / verification gate) and are not implementation briefs". That exemption is **sound for the blind reviewer** — it *is* the verification gate ("Acceptance check: n/a — you are the check", `dispatch-prompt.md:187`), so no finding there — and sound for the second pass as to the seven fields (an opinion never writes files; the pass fires only on genuine uncertainty or different priors, `orchestrate/SKILL.md:18`, single pass by default). But the exemption is overbroad in one respect: the second pass is *forced to conclude* ("Return: conclusion first…") on a task body that the first pass, reading the same words, is instructed to return as `NEEDS_CONTEXT` if under-specified. A genuinely under-specified blind-parallel run therefore yields one `NEEDS_CONTEXT` and one confident conclusion — and the orchestrator's disagreement-stop rule (`orchestrate/SKILL.md:291`) then fires on what is really a missing-input signal, stopping the run instead of supplying the missing input.

**Fix.** Add one line to the second-pass template (`dispatch-prompt.md:150–160`): "If the task body leaves a decision unspecified, return `NEEDS_CONTEXT` naming it — do not guess." If the coordinator holds that opinion passes must always conclude, record that as an explicit decision with the reason, rather than leaving the asymmetry silent.

### 81-A6 — MINOR: the gan-build pointer and the common-agents factory line omit the COST-AWARE rules — the 80-B14 standard applied to the five wrappers was not applied to the two newer pointers

**Evidence.**

- `commands/gan-build.md:12`: "**Factory routing (fix #29, GLOBAL-ROUTING_F29):** the planner, generator, and evaluator passes below run as factory drones per `gan-style-harness` — each with a director brief (goal, files in/out of scope, constraints, acceptance criteria, verification steps, what to return), no-guessing, and orchestrator verification against the brief's acceptance criteria (a rubric pass with a failed acceptance criterion is a fail)." No N>3 rule, no minimal-context rule.
- `rules/common-agents.mdc:26`: "Implementation-agent dispatch follows the factory routing in orchestrate's GLOBAL-ROUTING block (fix #29, GLOBAL-ROUTING_F29): every implementation dispatch carries a director brief, no-guessing applies, and the orchestrator verifies the output against the brief's acceptance criteria before use." No N>3 rule, no minimal-context rule.
- Contrast the five wrapper pointers (e.g. `skills/orch-refine-code/SKILL.md:13`): "Fan-out is bounded by efficiency: N>3 justified in one line; drones carry minimal context." — extended per 80-B14, and verify29 asserts the full pointer text including that clause (`fix29/verify29.py:1245`).

**Why it matters.** 80-B14 established that a pointer naming "cost-aware fan-out" without stating either rule is a real (if narrow) gap, because "a reader (or agent) reading only a wrapper never sees either rule". The same logic applies verbatim to these two pointers — and more so to `common-agents.mdc`, which is `alwaysApply: true` and fires without any skill invocation, so it is the file most likely to be the *only* file a run ever sees. The underlying skills do state the rules (`gan-style-harness:14`, the GLOBAL-ROUTING block), so runtime inheritance holds; textual inheritance does not.

**Fix.** Append the same one clause to both pointers: "(Fan-out bounded by efficiency: N>3 justified in one line; drones carry minimal context.)" Extend the corresponding verify29 assertions (gan-build pointer check; common-agents line check) to the full clause.

### 81-A7 — MINOR: the gan-build generator out-of-scope line is an unresolvable placeholder — it points at a brief that cannot name files

**Evidence.**

- `commands/gan-build.md:40` (generator launch block): "- Files out of scope: [named in the brief; `none` if genuinely none] — the generator touches only the spec's files."
- `commands/gan-build.md:1–2`: "Parse the following from $ARGUMENTS: 1. `brief` — the user's one-line description of what to build". There is no other "brief" in the command — no step constructs a generator brief naming out-of-scope files, unlike `feature-expansion`'s format item 2 ("the files explicitly OUT of scope (named; `none` if genuinely none)"), where the orchestrator writes the brief from the plan.

**Why it matters.** The 80-A6 fix required naming "the files out of scope in the generator launch block". As written, the line delegates the naming to "the brief", and the only brief in scope is the user's one-line description, which cannot name files — so in practice no files are ever named out of scope at this site, and the generator's scope is defined only positively ("the spec's files"). A generator that strays outside the spec has no named boundary to violate. Minor because the spec itself bounds the work ("the generator touches only the spec's files") and the skill paragraph states the seven-field requirement; the defect is that the launch block's out-of-scope line can never resolve to actual filenames.

**Fix.** Either name the actual out-of-scope files in the launch block (e.g. `gan-harness/` itself, `spec.md`/`eval-rubric.md` as read-only, files outside the spec) or state who names them and when ("the orchestrator names them from the spec before launch; `none` if genuinely none").

### 81-A8 — MINOR: the gan-build step-0 design-direction dispatch escapes the pointer's enumeration, and its target `ui-ux-pro-max` carries no factory routing at all

**Evidence.**

- `commands/gan-build.md:12` (pointer): "the planner, generator, and evaluator passes below run as factory drones" — the enumeration is closed: planner, generator, evaluator.
- `commands/gan-build.md:26` (step 0, cold start): "if neither the record nor the tokens file carries a direction (cold start — no direction recorded yet), dispatch to the design skill for that surface — `design-taste-frontend` for a landing page, `ui-ux-pro-max` for a dashboard/app surface — on model `grok-4.7-high`, first to generate the direction through the package skills (per the design-package rule) and record it in `docs/design-tokens.md`, then launch the planner with that recorded direction."
- `ui-ux-pro-max` appears in the routing set nowhere: its `SKILL.md` has one dispatch-verb hit (`:264`, "Implementers execute component directives verbatim" — a reference to implementers, no dispatch instruction of its own), and it carries zero `_F29` tokens.

**Why it matters.** The step-0 dispatch is worded as a dispatch ("dispatch to the design skill … on model `grok-4.7-high`") and its product is a write to a project file (`docs/design-tokens.md`). Under the manifest's own scope rule (a skill is in the routing set if it instructs spawning/delegating an agent that writes project files), it is at least a candidate implementation dispatch — and it is not covered by the pointer above it, which names only the three loop passes. Counter-evidence, stated fairly: `skills/orchestrate/SKILL.md:31` treats the design-lead as a *role of the orchestrator model* ("the orchestrator, the design-lead, the deep-reasoner, and every big-decision role run on Grok 4.7 High"), and the design package is explicitly out of fix #29's scope (SPEC: "Do NOT change … the design package") — so this may be orchestrator-level design-lead work governed by the design package, not factory implementation dispatch. The defect is that neither reading is recorded: the manifest's §2(b) "covered by reference" table lists `commands/gan-build.md` as covered via the skill paragraph, without noting that step 0 falls outside the pointer's enumeration.

**Fix.** Either extend the `gan-build.md:12` pointer to cover the step-0 design dispatch ("including the step-0 design-direction dispatch, which runs as a single-task factory drone with a director brief"), or record the scoping decision in MANIFEST §2(b): design-direction generation is orchestrator-level design-lead work governed by the design package, not factory implementation dispatch — with the reason (design-lead is an orchestrator role per `orchestrate:31`; the design package is out of fix #29 scope).

## Scoping challenges — answers to the brief §3

- **(a) "Covered by reference" — is the reference sufficient for a reader/agent that only ever sees that file?** Largely yes. `rules/common-agents.mdc:26` states the factory rules (director brief, no-guessing, verify) in the file itself, adjacent to the dispatch list it governs, and `commands/gan-build.md:12` states them at the top of the executed path. Neither file requires the reader to load the routed skill to know the rules. The sufficiency fails only on COST-AWARE (81-A6) and, for gan-build, on step 0 (81-A8). The five `commands/orch-*.md` files route to routed skills and need no pointer of their own, except `orch-refine-code.md` (81-A4).
- **(b) orch-refine-code "dispatches ALL implementation work through the factory" — true in substance?** True for the *factory-rules* sense (the step-2 sweep is now a factory drone with a director brief), false for the *through the engine* sense (step 2 is a direct dispatch). The pointer was never qualified — 81-A4.
- **(c) Second-pass / blind-reviewer exemption from the seven-field contract — sound?** Sound for the blind reviewer (it *is* the verification gate; `dispatch-prompt.md:187`, "Acceptance check: n/a — you are the check") and sound for the second pass as to the seven fields (opinion-only, never writes files, gated to uncertainty/different-priors cases). Unsound in one narrow respect: the second pass has no under-specification path while the first pass on the verbatim-identical task body does — 81-A5.

## Checked and clean

- **Verifier re-run by this auditor: `python3 fix29/verify29.py` → 215/215, exit 0** (independently re-run, not taken from the coordinator's log).
- **GLOBAL-ROUTING block byte-identical:** staged `new-skills/orchestrate/SKILL.md` GLOBAL-ROUTING line md5 `25413b71bcb2ea09c0096701ca064650` = built `skills/orchestrate/SKILL.md`; staged `new-rules/hackathon-mode.mdc` line md5 `39a22e9247be839a841ffbea3ad19918` = built `rules/hackathon-mode.mdc` — both md5s match the values audit #80-A recorded. Cross-file difference is only hackathon-mode's leading `"- "` list marker, the established DESIGNPKG-AUTO convention.
- **Census (10 skills) verified:** `GLOBAL-ROUTING_F29` present in all 10 routing-set skills (orchestrate, orch-pipeline, orch-build-mvp, orch-add-feature, orch-change-feature, orch-fix-defect, orch-refine-code, feature-expansion, gan-style-harness, design-taste-frontend via the `:455` pointer + `redesign.md:68` paragraph) plus `rules/hackathon-mode.mdc`; 15 files tree-wide carry the token (the 10 skills + hackathon-mode + `common-agents.mdc` + `gan-build.md` + `commands/orch-refine-code.md`).
- **"Factory routing (fix #29" ×1 in exactly 10 files** (9 skill paragraphs + `commands/gan-build.md`): no duplicates, none missing.
- **Build consistency (staged vs built):** `redesign.md` diff-exit 0 (identical); `dispatch-prompt.md` diff-exit 0 (identical); orchestrate 3 changed lines, feature-expansion 11, hackathon-mode 1, design-taste-frontend SKILL.md 11 — **zero `_F29` hunks in all four diffs** (verify29 check 7e covers the _F29 lines; the differing lines are the pre-existing build-time transforms #80-B13 documented).
- **Counts unchanged:** 67 skills / 45 agents / 48 rules / 55 commands (verify29 checks pass; directory counts re-confirmed).
- **Correction briefs constructed** in both fix loops (`orch-pipeline:74`, `feature-expansion:158` — identical construction sentence); old GAN substitution gone (`"The evaluator pass IS the verify step"` 0 hits); GAN orchestrator verify step present (`gan-style-harness:14`, "evaluator pass is an input to verification" ×1, "rubric pass at or above 7.0 with a failed acceptance criterion is a fail" ×1).
- **Feature-expansion brief format** verified complete: item 2 names files explicitly OUT of scope, 4a/4b split acceptance criteria from verification steps, item 9 states the return format.
- **Orchestrate contract core** verified complete: all seven fields including `Verification steps:` and "files explicitly out of scope" in Constraints, plus the no-drop rule ("drop no field: a field with nothing to list is written as `none`, never deleted").
- **Fresh-hunt greps (whole built tree):** base dispatch pattern 167 hits (vs 166 in #80-A — the +1 line is the new `redesign.md:68` paragraph itself); literal `dispatch` grep surfaced only `feature-expansion:137` (covered — Phase 4 dispatches its own implementers only on a standalone run); `launch|parallel|fresh-context|isolated` grep returned 11 hits, all accounted for (click-path-audit read-only audit, context-budget prohibition, gan-build planner/generator/evaluator launches, five `commands/orch-*.md` skill-invocation lines); `agents/*.md` role files dispatch nothing (self-descriptions only — `ecc-chief-of-staff.md:160`, `ecc-gan-*.md` launch notes, `deep-reasoner`/`fast-worker`/`scout` role definitions); `commands/plan-prd.md:8` delegates decomposition to `/plan` (planning, not implementation dispatch); `commands/plan.md` second verification pass and `commands/astra-review.md` blind review are read-only.
- **polish-pass reference files re-confirmed verification-only:** `impeccable-critique.md:17, :40, :43–47` (mandatory isolated parallel Assessment A/B sub-agents) and `polish.md:58` (fresh-context re-score) — assessments "leave it as found" (`impeccable-critique.md:94`); fixing is done by the main context, not the sub-agents. Out of scope stands.
- **OWED-29-3 stands for council and click-path-audit** (analysis/decisions only; read-only audit respectively — re-confirmed).
- **`ui-ux-pro-max:264`, `ai-feature-spec:26`, `strategic-compact:102`, `react-native-patterns:34`** — no implementation dispatch (directive reference / read-only policy / todo-tool note / code-structure "delegate" respectively).
- **Call map:** NOT re-run by this auditor — the generator mutates tree files and #80-A already reproduced the 2-line diff twice and restored md5 `b066413a…`; no #80 fix adds a dispatch edge (the new paragraphs reference only skills the map already lists), so the restore stands on #80-A's evidence, not re-proven here.

## Grep counts (for the record)

- Base dispatch pattern (`spawn|subagent|sub-agent|Task tool|delegate|delegat|implementer`, `*.md`/`*.mdc`): **167 hits** (166 in #80-A; +1 = `redesign.md:68`).
- "pick the reasonable option": **5 hits, all 5 carved + tie-breaker** (orch-pipeline:72, feature-expansion:151, orch-build-mvp:70, dispatch-prompt.md:34, :92).
- "instead of NEEDS_CONTEXT": **0**.
- "state the assumption" sites in `dispatch-prompt.md`: **6/6 reconciled** (status vocabulary, mechanical preamble, "Before you begin", reasoning template, worked example ×2).
- "slots refill per wave": **4 hits** (orch-pipeline:62, feature-expansion:139, gan-style-harness:14, orchestrate:93) — redesign.md absent (81-A3).
- "The evaluator pass IS the verify step": **0**; "evaluator pass is an input to verification": **1**.
- "merge order": **3 sites, all 3 bridged**.
- "correction brief" outside routing paragraphs: **2** (orch-pipeline:74, feature-expansion:158).
- "Verification steps" in `dispatch-prompt.md`: **4** (skeleton + 3 templates; worked example 0 — 81-A1). "files out of scope": **4** (same distribution).
- "Factory routing (fix #29": **10 files ×1**.
- GLOBAL-ROUTING block md5s: orchestrate `25413b71…`, hackathon-mode `39a22e92…` (staged = built, matching #80-A).
