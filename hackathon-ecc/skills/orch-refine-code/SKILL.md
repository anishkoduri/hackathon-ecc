---
name: orch-refine-code
description: Orchestrate a behavior-preserving refactor — confirm tests are green, restructure without changing behavior, keep tests green, review, and gated commit. Use when the structure should improve but behavior must not change. Use ONLY when the user explicitly invokes /orch-refine-code. A prose request to refactor belongs to orchestrate, not this skill.
metadata:
  origin: ECC
---

# orch-refine-code

Actor · action · target: **orch · refine · code**. Thin wrapper over the shared
engine in [`orch-pipeline`](../orch-pipeline/SKILL.md).

**Factory routing (fix #29, GLOBAL-ROUTING_F29):** this operation runs through the shared `orch-pipeline` engine, which dispatches all implementation work through the factory — see `orch-pipeline` for the routing (task queue, single-task drones, director briefs, no-guessing, verify-and-merge, cost-aware fan-out). Fan-out is bounded by efficiency: N>3 justified in one line; drones carry minimal context. The orchestrator answers every prompt; drones never answer the user or decide scope (ORCHESTRATOR-ONLY_F29). Except the step-2 refactor-cleaner sweep, which is dispatched directly as a single-task factory drone — see step 2.

## When to Use

- Same behavior, **better structure**: extract modules, remove duplication, kill
  dead code, reduce nesting, rename for clarity.
- Distinguish from siblings: if behavior is meant to change at all, this is the
  wrong skill (`orch-change-feature` / `orch-fix-defect`).

## Operation settings

- **Default size floor:** standard — restructures touch multiple files.
- **Phase mask:** 0 → 2 (plan the restructure) → 4 (keep green) → 5 → 6. No new
  behavior tests are written — the existing suite is the safety net.
- **First move (phase 4):** confirm the relevant tests exist and are **green
  before** touching code; if coverage is thin, add characterization tests first.
  Then restructure in small steps, re-running tests after each.

## How It Works

1. Run the `orch-pipeline` engine with the settings above.
2. For dead-code / duplication sweeps, delegate to the `refactor-cleaner` agent (`agents/ecc-refactor-cleaner.md`)
   (it runs knip / depcheck / ts-prune and removes safely). Dispatched as a single-task factory drone with a director brief (goal, files in/out of scope, constraints, acceptance criteria, verification steps, what to return; GLOBAL-ROUTING_F29) — the sweep is implementation work, so the factory rules apply to it directly, not only through the engine.
3. Stop at **Gate 1** (restructure plan) and **Gate 2** (pre-commit) — except during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature, where both gates auto-approve and the run proceeds without waiting (see hackathon-mode §7).
4. **UI change / rebuild-a-surface rule.** If the change touches UI — including a restructure that rebuilds a surface — it is a UI slice under the design-package rule (orchestrate SKILL.md row 10): name the applicable design components in the brief (app/dashboard/components: `design-taste-frontend` (design lead for every surface) + `ui-ux-pro-max` lookups + Impeccable via `polish-pass` + Harmony + `less-flat-ui` where dull/flat; landing: `design-taste-frontend` + dealt Hallmark theme; motion: + `make-interfaces-feel-better`; new design-system work: + `design-system`; legacy style drift: handled inside the design package — no separate skill (fix #27, REROUTE_F27)), record the direction in the decision record / run ledger (the lightest-weight record that exists for this flow — one line, a stated default from the brief's mood/domain if silent, marked assumed) and in `docs/design-tokens.md` where the flow keeps one, and run the applicable package components before the change lands. Read the design inventory (`skills/orchestrate/references/design-inventory.md`, INVENTORY_F23) BEFORE deciding — the design-lead records used vs considered-and-rejected inventory entries with D19 reasons in the decision record; a UI change whose design-lead never read the inventory is incomplete. The design role runs on model `grok-4.7-extra-high` (slug form only). The direction is generated through the package skills, never based on a searched external reference: if the design search returns only a marketing page, that is not a direction — the skills generate it instead. Posture is more, not bolder: more design decisions made deliberately through the skills, more craft. Verify the rebuilt surface against the distinctiveness bar through `browser-qa`'s visual loop on the rebuilt surface (the single executor of the bar — see orch-pipeline Review; the reviewer checks only the recorded direction): a finding, minor at least, when it carries no named direction, no applied theme/tokens, reads as a default template, or is derivative (the design is based on a searched external reference) — within the existing fix caps. Pure backend/logic changes with no visual surface are exempt.
**Design-decision pointer:** F2/F3/F4/F5/F6/D19/B1/X1 as relevant — design-package rule — Taste step 4a / orchestrate.
5. Commit as `refactor:` — the diff must be behavior-neutral.

## Example

```
orch-refine-code: extract the NWS HTTP client out of poller.py
→ confirm tests green → plan extraction  [GATE 1: auto-approves during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature]
→ move in small steps, tests green throughout → code-review
→ commit refactor:  [GATE 2: auto-approves during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature]
```
