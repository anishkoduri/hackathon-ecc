# Dry-run #44, Leg 6 — dispatched director briefs (constructed from the routing text)

Sample build "Pantry Pal v2". Each brief is built from the seven-field
contract (`skills/orchestrate/references/dispatch-prompt.md:15`:
Goal, Inputs, Constraints incl. files out of scope, Interface,
Acceptance check, Verification steps, Return format). Shared files
(`src/planner/types.ts`, `gan-harness/spec.md`, `docs/design-tokens.md`,
`src/ui/tokens.css`) are read-only / out of scope for every drone — no
two write sets share a file (Leg 6 check 6a). Minimal context: each
brief carries only its partition's files.

## T1 — orch-pipeline (slice A)

- **Goal:** Implement planWeek(): 6 dinners from the pantry inventory, $0 extra.
- **Files in scope:** `src/planner/week.ts`
- **Files out of scope:** `src/planner/types.ts` (read-only), `src/ui/tokens.css`, `gan-harness/spec.md`, `docs/design-tokens.md`
- **Constraints:** hackathon-mode rule; do not touch files out of scope.
- **Acceptance criteria:** planWeek() returns 6 dinners; total extra cost $0; unit test passes.
- **Verification steps:** run unit tests; run the app; exercise the feature; paste output.
- **What to return:** status, changed files, verification evidence, residual risks, blockers.

## T2 — orch-pipeline (slice B)

- **Goal:** Implement pantry inventory load + quantities.
- **Files in scope:** `src/pantry/inventory.ts`
- **Files out of scope:** `src/planner/types.ts` (read-only), `src/ui/tokens.css`, `gan-harness/spec.md`, `docs/design-tokens.md`
- **Constraints:** hackathon-mode rule; do not touch files out of scope.
- **Acceptance criteria:** inventory loads 6 items with quantities; unit test passes.
- **Verification steps:** run unit tests; run the app; exercise the feature; paste output.
- **What to return:** status, changed files, verification evidence, residual risks, blockers.

## T3 — gan-style-harness (generator pass)

- **Goal:** Generator pass: WeekView component per gan-harness/spec.md.
- **Files in scope:** `src/ui/WeekView.tsx`
- **Files out of scope:** `gan-harness/spec.md` (read-only), `src/ui/tokens.css`, `src/planner/types.ts`, `docs/design-tokens.md`
- **Constraints:** hackathon-mode rule; do not touch files out of scope.
- **Acceptance criteria:** WeekView renders Monday curry card with 25-minute label; rubric >= 7.0.
- **Verification steps:** run unit tests; run the app; exercise the feature; paste output.
- **What to return:** status, changed files, verification evidence, residual risks, blockers.

## T4 — feature-expansion (leftover remix)

- **Goal:** Feature: leftover remix (Wednesday dinner from yesterday's rice).
- **Files in scope:** `src/planner/remix.ts`
- **Files out of scope:** `src/planner/types.ts` (read-only), `src/ui/tokens.css`, `gan-harness/spec.md`, `docs/design-tokens.md`
- **Constraints:** hackathon-mode rule; do not touch files out of scope.
- **Acceptance criteria:** remix() returns a Wednesday dinner reusing yesterday's rice; demo flow passes.
- **Verification steps:** run unit tests; run the app; exercise the feature; paste output.
- **What to return:** status, changed files, verification evidence, residual risks, blockers.

## T5 — feature-expansion (cost tracker) — the no-guessing case

- **Goal:** Feature: cost tracker (running $ extra per dinner).
- **Files in scope:** `src/planner/cost.ts`
- **Files out of scope:** `src/planner/types.ts` (read-only), `src/ui/tokens.css`, `gan-harness/spec.md`, `docs/design-tokens.md`
- **Constraints:** hackathon-mode rule; do not touch files out of scope.
- **Acceptance criteria:** cost() reports $ extra per dinner; demo flow passes.
- **Verification steps:** run unit tests; run the app; exercise the feature; paste output.
- **What to return:** status, changed files, verification evidence, residual risks, blockers.
- **Deliberately unspecified:** cost display format (currency symbol / decimals).
  The drone returns `NEEDS_CONTEXT` naming it to the orchestrator
  (deep-reasoner.md:17; the NO-GUESSING carve-out + tie-breaker) instead
  of guessing a format. The orchestrator resolves it by stated assumption
  (dispatch-prompt.md:52) — never the user mid-build.

## T6 — design-taste-frontend (redesign, /plan page)

- **Goal:** Redesign /plan page past three pages (Hallmark redesign flow).
- **Files in scope:** `src/ui/PlanPage.tsx`
- **Files out of scope:** `docs/design-tokens.md` (read-only), `src/ui/tokens.css` (single-writer — orchestrator locks before fan-out), `src/planner/types.ts`, `gan-harness/spec.md`
- **Constraints:** hackathon-mode rule; do not touch files out of scope.
- **Acceptance criteria:** page matches recorded direction tokens; no layout regression.
- **Verification steps:** run unit tests; run the app; exercise the feature; paste output.
- **What to return:** status, changed files, verification evidence, residual risks, blockers.

## COST-AWARE justification (N = 6, one line)

Six disjoint file partitions (week.ts, inventory.ts, WeekView.tsx,
remix.ts, cost.ts, PlanPage.tsx) justify N=6.
