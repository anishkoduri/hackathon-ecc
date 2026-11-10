---
name: feature-expansion
description: Expand a working product beyond what was originally proposed, on demand only. Use ONLY when the user explicitly asks to flesh out, expand, or "make it much better" than the original idea. Dispatches subagents to brainstorm new features that dramatically improve the product, consolidates them into a proposal, runs them through a fast planner approve/tweak/reject pass, then automatically implements the approved ones, verifying each as it lands. Feature brainstorming here is autonomous subagent ideation + implementation; do not invoke the brainstorming skill (collaborative user questioning) inside this flow. Never runs automatically after a build. Do NOT use to add a single named feature the user already specified — orch-add-feature owns that; use this skill only when the user asks to expand or brainstorm beyond the current scope.
---

Before proposing anything, read the grill-me decision record for this project. Every proposed feature must follow a recorded decision; if a proposal contradicts a recorded decision, the recorded decision wins — note the conflict instead of overriding it.

# Feature Expansion

Take a product that already works and make it much more fleshed out and extensive than what was originally proposed — on purpose, and only when asked.

The user gives an idea plus requirements and the agent builds a working product. This skill is the second pass: it finds the features that would make that product meaningfully better — better demo, better quality, more complete — and builds them, without turning the session into planning documents or review gates.

## When to Use

- The user says "expand this", "flesh it out", "make it much better", "what else should this have", "take it further", or asks for features beyond the original brief.
- The product already runs end to end. If it does not run yet, fix that first (`systematic-debugging`, `build-fix`) — expansion on top of a broken product just multiplies the breakage.

## When NOT to Use

- Never automatically. Do not run this skill after finishing a build, after a feature lands, or because the product "could be better". It runs only on an explicit ask.
- Not for bug fixes — that is `systematic-debugging`.
- Not for the initial build — that is `hackathon-scope`.
- Not for a single feature the user already named — orch-add-feature owns that. This skill exists to *find* the features, not to implement one that is already decided.

## Standing Rules (these outrank everything below)

- **Opt-in only.** No automatic triggers, no running after tasks, no session hooks.
- **ECC process applies.** The proposal is a table in the reply (Phase 2); the planner pass (Phase 3) writes the per-feature briefs (Phase 4) that carry what implementers need. Follow ECC's development workflow: plan first, TDD, code review while building.
- **Review while building.** ECC code review applies as features are implemented. There is one approval point before implementation: the planner pass (Phase 3). Security tests and audits run only at the very end of the project or when explicitly asked.
- **TDD.** Write tests as ECC does them — tests first, then the feature — and verify with `verification-before-completion`. Security tests and audits run only at the very end of the project or when explicitly asked.
- **Never expand scope beyond the approved list.** If implementation reveals a new idea, note it in the final report. Do not build it.
- **The demo must keep working.** Verify each feature as it lands. Never batch verification to the end.

## Workflow

### Phase 0 — Ground in what exists (5 minutes, main agent)

Before any brainstorming, know the product as it stands:

1. Re-read the original idea and requirements (the user's brief, or `hackathon-scope` output if it exists).
2. Map what is actually built: entry points, data model, key flows, what the demo shows today. Use `code-explorer` (agent — spawn as a subagent) or `code-tour` if the codebase is unfamiliar.
3. Name two things in one line each: the demo's current strongest moment, and its weakest point. The weakest point is where the highest-value features usually live.

Do not write a document. Keep this as working notes in the session.

### Phase 1 — Brainstorm with subagents (parallel, three lenses)

Dispatch three brainstorm subagents **in parallel, in one message**. Each gets the same grounding (original idea, what is built, strongest moment, weakest point, hours left) and a different lens. Each returns 3–5 candidates, no more — a long list is a sign nobody prioritized.

**Lens A — Demo impact.** What would make the demo visibly better to a judge or user watching for two minutes? New things to show, clearer moments, a stronger wow. Think in demo beats, not feature lists.

**Lens B — Depth and quality.** What would make the product actually work better, not just look better? Missing handling, rough edges, things that are half-built, data the product already has but does not use, workflows that dead-end. Prefer features that reuse existing data, logic, and screens over ones that need entirely new systems.

**Lens C — Bold bets.** What would make this category-defining instead of just better? One or two ambitious ideas, honestly tagged as risky. A slate with no bold bet is a slate that settled.

Each subagent must work divergently before converging. Use these moves, adapted from the ideation literature:

- **Adjacent mapping.** What sits one step away from a feature that already exists? (A list that exists → search, filter, sort. A single record → history, comparison, export.)
- **Collision.** Take two things the product already does and combine them into something neither does alone. (Existing data + existing action = new capability.)
- **Gap finding.** Where does a user hit a dead end, an empty state, a manual workaround, or a "you can't do that here"? Every gap is a feature candidate.
- **10x reframing.** What would this look like if it had to be ten times better, not ten percent better? Keep the answer only if a concrete version of it is buildable in the time left.
- **Contrarian inversion.** What if the obvious fix is wrong — what is the opposite approach, and does it fit better?
- **Cross-domain analogy.** What does a good product in a different domain do at this exact moment, and does that move translate here?

Each candidate must be returned in this shape — nothing longer:

```
- Feature: [name, phrased as the user problem it solves, not the solution]
- Why it improves quality: [one sentence — what gets better for the demo or the user]
- Effort: [S = under 30 min, M = 30–90 min, L = over 90 min]
- Depends on: [nothing, or a named existing feature/file]
- UI touched: [yes/no — which screen, if yes]
```

Anti-patterns, enforced on every lens:

- **No "more of the same".** A candidate that is just a bigger version of an existing feature is not a candidate unless it changes what the demo can show.
- **No feature-factory output.** Every candidate must name the improvement in quality or demo impact. "Add X" with no reason why is rejected on sight.
- **No premature evaluation.** The brainstorm subagents do not score, rank, or kill each other's ideas. Scoring happens in Phase 2, by the orchestrator.
- **No novelty chasing.** A wild idea with no path to working in the time left is not a bold bet, it is a distraction. Bold bets still need a buildable shape.

### Phase 2 — Consolidate into a proposal (main agent)

1. **Deduplicate.** Merge candidates that are the same feature in different words. If two lenses found the same gap independently, that is a signal, not a duplicate — note it and keep one copy.
2. **Cut the weak.** Drop anything that duplicates shipped functionality without saying so, anything with no clear quality gain, and anything whose effort exceeds the time left. A short, strong list beats a long, padded one.
3. **Check the balance.** The shortlist must contain at least one bold bet (Lens C) and at least one depth/quality item (Lens B). If it does not, say so plainly and ask the brainstorm agents for one more round on the missing lens — one round only.
4. **Sanity-check the why.** For the top candidates, run `product-lens` in your head or for real: does this feature serve a real user job, or is it decoration? Cut decoration.
5. **Write the proposal as a table in the reply.** This is the only artifact Phase 2 produces. No file.

```markdown
| # | Feature (user problem) | Why it improves quality | Effort | Depends on | UI |
|---|------------------------|-------------------------|--------|------------|----|
| 1 | ...                    | ...                     | S/M/L  | ...        | Y/N |
```

Keep it to 4–7 features. More than that means nothing was prioritized.

### Phase 3 — Planner pass: approve, tweak, or reject (fast)

Hand the proposal table to the planner. In this plugin there is no separate planner agent, so the orchestrating agent runs the planner pass itself, in the planner role:

For **each** feature, exactly one verdict:

- **Approve** — build it as proposed.
- **Tweak** — build it with a stated change (smaller scope, different approach, different file). The tweak is one sentence, not a redesign.
- **Reject** — do not build it, with a one-line reason (too big for the time left, duplicates something, weak quality gain).

The planner pass also decides **implementation order** (dependencies first, quick wins that unblock the demo early) and flags **risks** per feature in one line each (what is most likely to break, and what the fallback is if it does).

Rules for this pass:

- It is a decision, not a document. The output is the proposal table with a verdict column added, plus order and one-line risks. Nothing else is written.
- The planner does not write PRDs, specs, or implementation plans as files — the per-feature briefs in Phase 4 carry what implementers need. Implementation follows ECC process (plan first, TDD, code review while building); security tests and audits run only at the very end or on explicit ask.
- If one feature's verdict is genuinely ambiguous (approve vs. reject changes the product's direction), use `council` for that feature only. Do not convene a council for the whole list.
- The planner never adds new features. If it spots a gap, it notes it for the final report.

**Present the decided table to the user and get a yes before implementing.** This is the single approval point in the whole skill. The user can approve all, approve a subset, or change a verdict — then implementation starts. Nothing is built before this yes.

### Phase 4 — Implement the approved features automatically

Dispatch implementers per approved feature, following the execution pattern below. This is the only phase that writes code.

**Team shape.** Use the smallest team that helps: one implementer per feature, up to 4 in parallel. Features with dependencies go in waves (dependency first, dependents after). Features with overlapping write scopes go sequential, never parallel. One feature is a valid team — do not parallelize for its own sake.

**Briefs.** Each implementer gets a self-contained brief, inline in its dispatch — never a reference to "read the plan" or "use skill X". A brief contains:

1. One line on where this feature fits in the product and why it was approved.
2. The exact outcome: what the user can do after this lands that they could not do before, and which files it touches.
3. Constraints: global rules that bind this feature (the plugin's hackathon-mode rule, the UI rule below, any interface or data-shape decision from an earlier feature).
4. Completion evidence: the exact commands or checks that prove it works (run the app, exercise the feature, confirm the visible result). Verification is running it, not tests.
5. A soft time budget matching its effort estimate (S/M/L from the proposal). Report blocked with partial evidence rather than grinding past it.
6. The stopping rule: implement the brief exactly. If it is infeasible or needs redesign, report blocked with evidence instead of a replacement plan. Never redesign, never return another plan.

**UI rule (no exceptions).** Any feature that touches UI goes through the plugin's UI skills: `ui-ux-pro-max` and `less-flat-ui` together — except on a full landing/company page, where `design-taste-frontend` leads per hackathon-mode §5. The implementer's brief says so explicitly, and the implementer applies them to every surface the feature adds or changes. If a feature needs a named API, SDK, or tool wired in, use `integration`; if it needs generic REST-client mechanics on an unnamed API, use `api-integration`; if it needs auth or a database, use `app-scaffold`; if it needs to be live, use `deploy-fast`. Name the skill in the brief — implementers do not load skills by name on their own.

**Fix loop (capped).** If a feature lands but its verification fails, the implementer fixes it and re-verifies — at most 2 rounds. Past that, the feature is reported blocked with evidence, the orchestrator notes it, and work moves on to the next feature. No open-ended fix loops, no re-review rounds. A blocked feature is not a failed skill run.

**Collect and reconcile.** After each wave, read every implementer's result (status, changed files, verification evidence, residual risks, blockers). Confirm the reported files exist, stayed in scope, and carry verification evidence. If two implementers in the same wave touched the same files, that wave is a blocker — reconcile before starting dependents. Do not add agents or change scopes because one implementer is slow or quiet; handle it by waiting for its terminal result, then deciding.

**Build breaks.** A build or type error during implementation goes to the `build-fix` command or the `build-error-resolver` agent (spawn as a subagent; pick the per-language one if the feature is single-stack). Do not hand-debug inside the orchestrator.

### Phase 5 — Verify the whole (main agent, once)

After every approved feature is in (or blocked with evidence):

1. Run the app. Walk the demo flow end to end — `browser-qa` for the deployed or local flow, `click-path-audit` if buttons or shared state were touched. The demo must work. If a feature broke the demo, that feature is reverted or fixed now, before anything else.
2. Confirm every landed feature with `verification-before-completion`: run it, read the output, then claim it.
3. If the demo story changed (a new wow moment, a different flow), note the new story in one paragraph. If the user wants the pitch re-cut, `hackathon-pitch` is available — offer it, do not run it unasked.

### Phase 6 — Report (short)

Reply with:

- **Landed:** each feature, one line, what it does now.
- **Blocked:** each blocked feature, one line, why, and what the fallback is.
- **Rejected or cut:** the planner's rejects, one line each (so the user knows what was considered).
- **Demo now:** one paragraph — what to show, in what order, and where the new wow moment is.
- **Not built:** any new idea spotted during implementation, listed only, never built.

Then stop. Do not loop back to Phase 1 unasked. If the user wants another round, they will say so.

## Reference: Which Plugin Pieces This Uses

| Need | Use |
|---|---|
| Ideation structure (seed expansion, divergence) | defined in this skill (Phase 1), adapted from upstream brainstorming techniques — the `brainstorming` skill is NOT invoked |
| Proposal shape (persona, outcome framing, RICE, fail condition, bold bets) | `product-lens` (why-check), proposal table in this skill |
| Parallel brainstorm dispatch | `dispatching-parallel-agents` |
| Contested planner decisions only | `council` |
| Understanding the codebase before brainstorming | `code-explorer` (agent — spawn as a subagent), `code-tour` |
| Acceptance criteria per feature (one line each) | `intent-driven-development` |
| Build errors during implementation | `build-fix`, `build-error-resolver` (agent — spawn as a subagent) (+ per-language resolvers) |
| Design questions on a feature | `architect` (agent — spawn as a subagent), `code-architect` (agent — spawn as a subagent) |
| UI on any touched surface | `ui-ux-pro-max` + `less-flat-ui` (except a full landing/company page: `design-taste-frontend` leads) |
| Integrations a feature needs | `integration` (named API/SDK/tool), `api-integration` (generic REST-client mechanics on an unnamed API), `app-scaffold`, `deploy-fast` |
| Verifying a landed feature | `verification-before-completion` |
| Verifying the demo flow after | `browser-qa`, `click-path-audit` |
| Debugging a feature that misbehaves | `systematic-debugging` |
| Re-cutting the pitch after expansion | `hackathon-pitch` (offer, do not auto-run) |
| Long session running low on context | `strategic-compact` |
| Quality check, only if the user asks | `agent-self-evaluation` (manual-only) |

## Attribution

This skill is a composition written for hackathon-ecc. It draws on:

- **Spark** (`SpectreTechnologie/agent-skills`, MIT) — the feature-proposal shape used in Phase 2: persona and outcome framing, RICE scoring with guardrails, hypothesis plus fail condition, Horizon tags with at least one bold bet, and the brainstorm recipe's divergence moves (contrarian inversion, 10x reframing, cross-domain analogy). Used with attribution; the multi-engine mode, reference files, and companion skills were not carried over.
- **Brainstorming techniques** (`b00ng/agent-skills`, no license) — upstream brainstorming techniques adapted in Phase 1: Seed Expansion (adjacent mapping, collision generation, gap identification, transplant and stress testing) and Escape Velocity (function extraction, axis mapping, entropy injection, orthogonality audit), plus the anti-patterns (premature evaluation, novelty chase, expert anchor). The `brainstorming` skill itself is NOT invoked. Rewritten in our own words; no sentences copied.
- **claude-handoff** (`cliffordcollinsglobal/agent-skills`, no license) — the execution contract used in Phase 4: implementers implement their assigned part and never redesign or return another plan, self-contained briefs, smallest effective team, the stopping rule (report blocked with evidence instead of a replacement plan), and collect-and-reconcile. Rewritten in our own words, with the coordination tooling, polish passes, and commit steps removed.
- **Subagent-Driven Development** (`obra/superpowers`, MIT) — the task-loop mechanics used in Phase 4: dispatch with a brief as the single source of requirements, a report contract, and a capped fix loop. Used with attribution; the two-stage review gates (spec compliance + code quality), the final whole-branch review, and the helper scripts were deliberately left out, per this plugin's no-review-gates rule.
- **ecc-planner** (`affaan-m/ecc`, MIT) — the planning role used in Phase 3. The stock planner agent was NOT copied into this plugin: it activates proactively and its plan format mandates a Testing Strategy section, which violates this plugin's lightweight-planning rules. Only the planning capability it represents (break features into ordered steps with file paths, dependencies, and risks) was folded into the planner pass above, in a lightweight approve/tweak/reject form.
