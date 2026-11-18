---
name: orch-add-feature
description: Orchestrate building a brand-new feature end to end — research, plan, TDD implementation, review, and gated commit — by delegating each phase to the matching ECC agent. Use when adding a capability that does not exist yet. Use ONLY when the user explicitly invokes /orch-add-feature. A prose request to add a capability belongs to orchestrate, not this skill.
metadata:
  origin: ECC
---

# orch-add-feature

Actor · action · target: **orch · add · feature**. Thin wrapper over the shared
engine in [`orch-pipeline`](../orch-pipeline/SKILL.md).

**Factory routing (fix #29, GLOBAL-ROUTING_F29):** this operation runs through the shared `orch-pipeline` engine, which dispatches all implementation work through the factory — see `orch-pipeline` for the routing (task queue, single-task drones, director briefs, no-guessing, verify-and-merge, cost-aware fan-out). Fan-out is bounded by efficiency: N>3 justified in one line; drones carry minimal context. The orchestrator answers every prompt; drones never answer the user or decide scope (ORCHESTRATOR-ONLY_F29).

## When to Use

- The user wants a capability that does **not exist yet** ("add", "build",
  "implement", "support …").
- It is net-new behavior — not a correction (`orch-fix-defect`) and not an
  alteration of existing behavior (`orch-change-feature`).

## Operation settings

- **Default size floor:** standard — run Research + Plan unless clearly small.
- **Phase mask:** 0 → 1 → 2 → 4 → 5 → 6 (skip 3 Scaffold; that is MVP-only).
- **First move (phase 4):** write *new* failing tests for the new behavior, then
  implement to green.

## How It Works

1. Run the `orch-pipeline` engine with the settings above.
2. Classify size first; small / trivial features collapse toward 4 → 5 → 6.
3. Stop at **Gate 1** (plan approval) and **Gate 2** (pre-commit) — except during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature, where both gates auto-approve and the run proceeds without waiting (see hackathon-mode §7).
4. Add `security-reviewer` if the feature touches a security trigger.
5. **UI change / build-a-surface rule.** If the change touches UI — including a one-prompt change, a redesign, or a new feature that builds a surface — it is a UI slice under the design-package rule (orchestrate SKILL.md row 10): name the applicable design components in the brief (app/dashboard/components: `design-taste-frontend` (design lead for every surface) + `ui-ux-pro-max` lookups + Impeccable via `polish-pass` + Harmony + `less-flat-ui` where dull/flat; landing: `design-taste-frontend` + dealt Hallmark theme; motion: + `make-interfaces-feel-better`; new design-system work: + `design-system`; legacy style drift: handled inside the design package — no separate skill (fix #27, REROUTE_F27)), record the direction in the decision record / run ledger (the lightest-weight record that exists for this flow — one line, a stated default from the brief's mood/domain if silent, marked assumed) and in `docs/design-tokens.md` where the flow keeps one, and run the applicable package components before the change lands. Read the design inventory (`skills/orchestrate/references/design-inventory.md`, INVENTORY_F23) BEFORE deciding — the design-lead records used vs considered-and-rejected inventory entries with D19 reasons in the decision record; a UI change whose design-lead never read the inventory is incomplete. The design role runs on model `grok-4.7-extra-high` (slug form only). The direction is generated through the package skills, never based on a searched external reference: if the design search returns only a marketing page, that is not a direction — the skills generate it instead. Posture is more, not bolder: more design decisions made deliberately through the skills, more craft. Verify the rebuilt surface against the distinctiveness bar through `browser-qa`'s visual loop on the rebuilt surface (the single executor of the bar — see orch-pipeline Review; the reviewer checks only the recorded direction): a finding, minor at least, when it carries no named direction, no applied theme/tokens, reads as a default template, or is derivative (the design is based on a searched external reference) — within the existing fix caps. Pure backend/logic changes with no visual surface are exempt.
**Design-decision pointer:** F2/F3/F4/F5/F6/D19/B1/X1 as relevant — design-package rule — Taste step 4a / orchestrate.

> Related: `/feature-dev` is a standalone version of this flow. `orch-add-feature`
> differs by sharing the `orch-pipeline` engine — the size classifier and the two
> gates — with the rest of the family, so it right-sizes trivial features to 4 → 5 → 6.

## Example

```
orch-add-feature: add OAuth2 login to nws-poller
→ research existing auth libs → plan task_list  [GATE 1: auto-approves during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature]
→ TDD each task → code-review (+ security-reviewer: auth path)
→ commit  [GATE 2: auto-approves during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature]
```
