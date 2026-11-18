---
name: orch-pipeline
description: Shared orchestration engine behind the orch-* skill family — the gated Research-Plan-TDD-Review-Commit pipeline, size classifier, agent and command map, and two human gates (plan approval, commit confirmation) that orch-* operation skills delegate to. Use indirectly via orch-add-feature, orch-fix-defect, orch-change-feature, orch-refine-code, or orch-build-mvp; read directly only when adding an orch operation or tuning shared phases.
metadata:
  origin: ECC
---

# Orchestrator Pipeline (shared engine)

The `orch-*` skills are thin wrappers. They do not re-implement any work — they
classify the request, choose which phases of *this* pipeline run, and delegate
each phase to an existing ECC agent or command. This file is that pipeline.

**One build engine per run:** `orch-build-mvp` is the STANDALONE pipeline that delegates to this engine — it runs only when the user invokes `/orch-build-mvp` directly. Orchestrate IS the first-build engine and never invokes `orch-build-mvp` (and so never reaches this engine through it) in the same run. One engine per run, never both.

> Invoke an operation skill (`orch-add-feature`, `orch-fix-defect`, …) rather
> than this engine directly. This file is the reference they point at.

## When to Use

- Loaded indirectly whenever an `orch-*` operation skill runs.
- Read directly only when adding a new operation to the family or tuning the
  shared phases, gates, or agent map.

## The operation family

| Skill | Operation | Trigger | First move |
|-------|-----------|---------|------------|
| `orch-add-feature` | feature | capability does not exist yet | research + plan a new slice |
| `orch-change-feature` | tweak | works, but desired behavior differs | amend existing behavior *and its tests* |
| `orch-fix-defect` | fix | broken; behavior is wrong | reproduce as a failing test, then fix |
| `orch-refine-code` | refactor | behavior stays, structure improves | restructure while keeping tests green |
| `orch-build-mvp` | mvp | bootstrap from a design/spec doc (standalone only — user-invoked) | ingest record/scope by default (spec doc only as standalone fallback) → vertical slices |

> These wrappers **compose** existing ECC commands rather than replace them:
> `/feature-dev`, `/plan`, `/code-review`, `/build-fix`, `/refactor-clean`, and
> `/gan-build`, plus the `tdd-workflow` skill. The orch-* family adds the shared
> size classifier and the two gates
> on top of them, so one umbrella covers all five operations consistently.

## Step 0 — Classify size (right-sizing)

**MODEL check (fix #33, MODELSEL_F33):** before anything else, state the model the orchestrator is running on and record it in the run ledger (`MODEL: <name>` — the actual selected model). If the selected model is Auto, or the model cannot be determined to be a specific model, tell the user to pick a specific model before proceeding; do not silently orchestrate on an unknown fallback.

Ceremony scales to blast radius. Score the request on three signals, take the
**highest** tier any signal reaches, and state the result in one line so the user
can override — except during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature, where no user is present and the classifier result stands:

| Tier | Files touched | New dependency / contract | Design ambiguity | Phases that run |
|------|---------------|---------------------------|------------------|-----------------|
| trivial | 1, a few lines | none | none — the change is obvious | 4 → 5 → 6 |
| small | 1 file / 1 function | none | clear once you read the code | (1 light) → 4 → 5 → 6 |
| standard | 2–5 files | maybe a new internal module | one real choice to make | 1 → 2 → 4 → 5 → 6 |
| large | many / cross-cutting | new external dep, public API, or a spec doc | multiple open questions | 1 → 2 → (3) → 4 → 5 → 6 |

Phase 0 (Intake) always runs and is omitted from the mask column above. The
tie-breaker: anything touching a security trigger (below) or a public API /
contract is **at least** standard, regardless of file count.

## The phases

Each phase delegates — it does not do the work inline. **Binding routing (fix #20 BIND/INNOV):** each phase names its operating skill before delegating; a decision with no named skill is refused and routed; on-skill innovation passes with its D19 reason, off-skill improvisation fails.

**Factory routing (fix #29, GLOBAL-ROUTING_F29):** every phase dispatches through the factory — the orchestrator's queue of independent single-task jobs, one drone per job, retired on completion, the next queued job dispatched into the freed slot (in Cursor, slots refill per wave, not per completion — the factory lights up fully on the later port, not in Cursor) (FACTORY-DISPATCH_F29). Every drone brief is a director brief (DIRECTOR-BRIEF_F29): the exact goal, the files in scope and explicitly out of scope, constraints, acceptance criteria, verification steps, and what to return — an incomplete brief means the drone does not start. Briefs follow the seven-field contract in `skills/orchestrate/references/dispatch-prompt.md`. A drone that hits a decision its brief leaves unspecified stops and returns the question to the orchestrator instead of guessing (NO-GUESSING_F29). The orchestrator verifies every drone output against the brief's acceptance criteria and sends failed output back with a correction brief (VERIFY-MERGE_F29); fan-out is bounded by efficiency, N>3 justified in one line, drones carrying minimal context (COST-AWARE_F29). The orchestrator answers every prompt; drones never answer the user or decide scope (ORCHESTRATOR-ONLY_F29).

- **0. Intake** — restate the request. For `orch-build-mvp`, read `docs/decision-record.md` + `docs/scope.md` by default — the grill-me decision record and the scope output — and extract scope, locked decisions, and a feature list; if neither file exists, fall back to the spec/design doc (or the raw prompt with a stated assumption) — never ask the user for a path during a first build. The pipeline ingests the record/scope at Phase 0; they are the handoff from grill-me and hackathon-scope. Numbering: Phases 0–6 here are orch-pipeline phases — not orch-build-mvp steps (which map 1:1 onto them: orch-build-mvp steps 1/3/4/6/7 are Phases 0–2/3/4/5/6) and not feature-expansion phases.
- **1. Research & Reuse** — per `rules/common-development-workflow.mdc`: `gh search repos` /
  `gh search code`, then Context7 / vendor docs, then package registries, then
  Exa. Prefer adopting a proven implementation over net-new code.
- **2. Plan** — delegate to the `architect` agent (`agents/ecc-architect.md`) (or `code-architect` agent (`agents/ecc-code-architect.md`) for structural decisions). Output a `task_list` ordered as
  thin vertical slices. → **GATE 1** (auto-approves during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature).
- **3. Scaffold** — `orch-build-mvp` only: stand up the first end-to-end slice.
- **4. Implement (TDD)** — drive each task through the `tdd-guide` agent (or the `tdd-workflow` skill):
  red → green → refactor. Honor the operation's first-move rule. **Belief in the brief:** implementers trust the brief and build it — they do not second-guess the plan, hedge, or wait for reassurance; they commit to the approach and make it work; if a detail is ambiguous, they pick the reasonable option and note it, they don't stall. **Bounded by NO-GUESSING (fix #29, NO-GUESSING_F29):** 'pick the reasonable option' applies only to carrying out the briefed approach, never to a decision the brief leaves unspecified — an unspecified file, scope call, or acceptance criterion is returned to the orchestrator as a question, not guessed. When in doubt which side an ambiguity falls on, return the question — a returned question is never a stall. In a standalone `orch-build-mvp` run, this phase builds the approved expansions per the feature-expansion Phase 4 brief format (Tool/API cell + UI rule + capped 2-round fix loop + per-feature `code-reviewer` agent (`agents/ecc-code-reviewer.md`) pass).
- **5. Review** — `code-reviewer` agent / `/code-review`. Add `security-reviewer`
  whenever the diff touches a security trigger (below). On any diff that touches a UI surface, the reviewer ALWAYS runs regardless of size (UI diffs are not exempt from review) and checks the direction is RECORDED — a named direction in `docs/design-tokens.md` / the decision record, present in the diff, with tokens tracing to it in the changed code; a missing record is a finding, minor at least. The reviewer does NOT judge the built screens (it receives only the diff). Screen-level distinctiveness is judged ONLY by `browser-qa`'s visual loop, which runs on the rebuilt surface after the reviewer pass: enumerate the touched screens, inspect the rendered UI (desktop + mobile), and apply the distinctiveness bar (orchestrate SKILL.md Verify step 5) — a finding, minor at least, when screens carry no named direction, no applied theme/tokens, read as a default template, or are derivative (the design is based on a searched external reference); findings route to the capped 2-round fix loop (max 3 rounds total); the re-dispatch carries a correction brief naming the failed acceptance criterion and the required correction, distinct from the original brief; if the app cannot run, record that as blocked with evidence instead of iterating.
**Design-decision pointer:** F2/F3/F4/F5/F6/D19/B1/X1 as relevant — design-package rule — Taste step 4a / orchestrate.
- **6. Commit** — conventional commits (`feat:` / `fix:` / `refactor:` / …), one
  per logical chunk. → **GATE 2** (auto-approves during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature). (Orch-pipeline Phase 6 = Commit — not orch-build-mvp step 6, which is Verify, and not feature-expansion Phase 6, which feeds the final report; orch-build-mvp step 5 is Reconcile, which has no orch-pipeline phase of its own.)

## The two gates

This family is **gated, not autonomous** — except during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature (hackathon-mode §7), where both gates auto-approve and the run proceeds without waiting:

1. **GATE 1 — after Plan.** Present the `task_list`; do not write implementation
   code until the user approves — except during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature, where the gate auto-approves and the run proceeds without waiting. Record the approved `task_list` (one line per slice, with its files) in `docs/run-ledger-appendix.md` at Gate 1, with a one-line pointer (slice count + file) in `.hackathon/run-ledger.md`, so later phases read it from there instead of the transcript.
2. **GATE 2 — before Commit.** Present the diff summary and proposed messages;
   do not commit until the user confirms — except during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature, where the gate auto-approves and the run proceeds without waiting.

Everything between the gates flows without stopping.

## Agent / command map

| Phase | Primary | Fallback / escalation |
|-------|---------|----------------------|
| Intake / understand | `code-explorer` | trace existing paths before a tweak, fix, or refactor |
| Plan | `architect` | `code-architect` for structural calls |
| Implement | `tdd-guide` (or `tdd-workflow` skill) | `build-error-resolver` / `/build-fix` on build breaks |
| Review | `code-reviewer` / `/code-review` | language reviewer (`python-reviewer`, `typescript-reviewer`, …) |
| Security | `security-reviewer` | — |
| MVP inner loop | `/gan-build "<brief>" --skip-planner` | drives `gan-generator` → `gan-evaluator`; tune `--max-iterations` / `--pass-threshold` |

Match the language reviewer to the repo (see the repo's own `AGENTS.md`).

## Security-review trigger

Pull in `security-reviewer` when the diff touches any of: authentication or
authorization, user-input handling, database queries, file-system paths,
external API calls, cryptography, or secrets / credentials. (Per `rules/common-security.mdc`.)

## Handoff artifacts

The pipeline carries no hidden state — the planning docs *are* the handoff:

- `task_list` (from Plan) drives the Implement loop.
- Larger work may also emit PRD / architecture / system_design under the repo's
  `docs/` per `rules/common-development-workflow.mdc`.
- Review findings (CRITICAL / HIGH) must be resolved before Gate 2 — capped at 2 fix rounds, like the feature-expansion Phase 4 fix loop: after 2 rounds an unresolvable finding is recorded as blocked in the final report and work moves on. During a hackathon first build after grill-me, or a one-prompt removal of a first-build feature, an unresolvable CRITICAL finding at Gate 2 does not deadlock the commit — it is recorded as blocked in the final report and the commit proceeds under auto-approval.

## Verification

- size tier was stated and matched the work
- Gate 1 (plan) and Gate 2 (commit) were both honored (or auto-approved during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature)
- `security-reviewer` ran iff a security trigger was touched
- UI work (if any): the design package was named in the brief, the direction is recorded, the design inventory was read before deciding (used vs considered-and-rejected recorded, INVENTORY_F23), and the distinctiveness bar passed or its findings were fixed within the caps (finding, minor at least, when screens carry no named direction, no applied theme/tokens, read as a default template, or are derivative — the design is based on a searched external reference)
- commits are conventional and scoped to one logical change
- new / changed behavior has tests; coverage ≥ 80% per `rules/common-testing.mdc`
