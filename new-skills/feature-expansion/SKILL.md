---
name: feature-expansion
description: Elevate a product beyond its original brief — automatically during the first build, on demand after that. Runs right after hackathon-scope sets the MVP scope — subagents brainstorm new features and tools that elevate the product in line with docs/decision-record.md, the planner approves/tweaks/rejects them, then the approved ones are built as part of the first build, verified as they land. No user approval gate — the user removes anything unwanted with one prompt through orch-change-feature. After the first build, runs only when the user explicitly asks to flesh out, expand, or "make it much better" than the original idea. Do NOT use to add a single named feature the user already specified — orch-add-feature owns that.
---

Before proposing anything, read `docs/decision-record.md` for this project. If it does not exist, fall back to the raw user prompt plus `docs/scope.md`. Every proposed feature must follow a recorded decision; if a proposal contradicts a recorded decision, the recorded decision wins — note the conflict instead of overriding it.

# Feature Expansion

Take a product and make it much more fleshed out and extensive than what was originally proposed — on purpose, and automatically during the first build.

**The skill is split across the first build — it is NO LONGER invoked whole at one step.** Phases 0–3 run PRE-BUILD, right after scoping, producing the planner-approved list of features and tools. **One build engine per run:** in a first build orchestrate IS the engine and drives Phases 4–6 inside its build; in a standalone `orch-build-mvp` run, `orch-build-mvp` drives them instead. Orchestrate never invokes `orch-build-mvp` in the same run, and neither flow runs Phases 0–3 in the other's flow — expansion Phases 0–3 run ONCE per run. **Expansion wiring, both flows:** orchestrate-driven — expansion Phase 4 = orchestrate slicing builds the expansions per the routing table, USING the Phase 4 brief format below (Tool/API cell + UI rule + capped 2-round fix loop + per-feature `code-reviewer` pass); expansion Phase 5 = orchestrate's Verification stage runs the expansion checks BY NAME (`browser-qa` / `click-path-audit` / `verification-before-completion` per feature, after the MVP is built); expansion Phase 6 = ORCHESTRATE composes the section from the stage ledger + the implementers' return texts (orchestrate is the named producer). Standalone `orch-build-mvp` — expansion Phase 4 dispatches its own implementers (the GAN loop in `orch-build-mvp` step 4 drives them); expansion Phase 5 runs in `orch-build-mvp` step 6 (verification); expansion Phase 6 feeds `orch-build-mvp` step 9 (final report). No phase is orphaned in either flow. The project directory IS the project root — the folder opened in Cursor; no separate directory is created, and all `docs/…` paths are relative to it (create `docs/` under the project root if needed).

The user gives an idea plus requirements and the agent builds a working product. This skill runs right after `hackathon-scope` sets the MVP scope, as part of the first build: it finds the features and tools that would make that product meaningfully better — better demo, better quality, more complete — and builds them alongside the MVP, without turning the session into planning documents or approval gates. After the first build it runs only when the user explicitly asks for it.

## When to Use

- Automatically, as part of the first build: Phases 0–3 run right after `hackathon-scope` sets the MVP scope and before building starts, producing the planner-approved list; Phases 4–6 run inside the build (orchestrate-driven: orchestrate slicing builds them per the routing table using the Phase 4 brief format, orchestrate's Verification stage runs the Phase 5 checks by name, orchestrate composes the Phase 6 section; standalone `orch-build-mvp`: the GAN loop drives Phase 4, step 6 verifies Phase 5, step 9 takes Phase 6).
- The user says "expand this", "flesh it out", "make it much better", "what else should this have", "take it further", or asks for features beyond the original brief — after the first build, this is the only way it runs.
- On an explicit ask after the first build, the product already runs end to end. If it does not run yet, fix that first (`systematic-debugging`, `build-fix`) — expansion on top of a broken product just multiplies the breakage.

## When NOT to Use

- Never automatically after the first build. Do not run it after finishing a build, after a feature lands, or because the product "could be better" — after the first build it runs only on an explicit ask.
- Not for bug fixes — that is `systematic-debugging`.
- Not for the initial scoping — that is `hackathon-scope`. Expansion runs after scoping, as part of the first build.
- Not for a single feature the user already named — orch-add-feature owns that. This skill exists to *find* the features, not to implement one that is already decided.

## Standing Rules (these outrank everything below)

- **Automatic during the first build, opt-in after.** Runs on its own right after `hackathon-scope`, as part of the first build. After the first build it runs only on an explicit ask — no automatic triggers, no running after tasks, no session hooks.
- **No planning documents.** The proposal is a table in the reply (Phase 2), recorded in the session and the run ledger / final report as needed. No PRD, no spec file, no roadmap doc.
- **No user approval gate.** The planner pass (Phase 3) is the only gate, and it is internal — the approved list goes straight into the build. The user removes anything unwanted afterward with one prompt through `orch-change-feature` — except during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature, where the gate auto-approves and the run proceeds without waiting; that is the intended correction path, not a failure.
- **Tests AND running it.** TDD and code review stay, per hackathon-mode §4 — verification means running the feature and confirming it works (`verification-before-completion`) plus the tests the brief requires. Order: the `code-reviewer` pass (Phase 4) happens before verification counts as complete — reviewer findings are fixed inside the capped 2-round fix loop, not after verification.
- **Never expand scope beyond the approved list.** If implementation reveals a new idea, note it in the final report. Do not build it.
- **The demo must keep working.** Verify each feature as it lands (Phase 4). Pre-MVP, "verify as it lands" means the tests the brief requires plus running the feature in isolation (exercised on its own, before the whole app exists) — the whole-app demo check waits for Phase 5. The whole-build verification (Phase 5) runs after the MVP is built, with the expansion features verified together with the MVP — never before building starts.

## Workflow

### Phase 0 — Ground in what exists (5 minutes, main agent)

Before any brainstorming, know the product as it stands — or, during the first build, as it is scoped to stand:

1. Re-read the original idea and requirements — the raw user prompt and `docs/scope.md`. Read `docs/decision-record.md` — it is the source of the user's vision, and every proposal must follow it. Extract the recorded decisions and paste them into the Phase 1 dispatch below — the brainstorm subagents get the decisions inline, never a bare filename. If `docs/decision-record.md` does not exist, fall back to the raw user prompt plus `docs/scope.md` and say so in the dispatch.
2. During the first build (automatic run): map what is scoped from `docs/scope.md` — entry points, data model, key flows, what the demo will show. Read hours-left (the time budget) from `docs/scope.md` if it is recorded — effort estimates in Phase 1 are judged against it. Hours-left is never required to proceed: if it is not recorded, use the default — remaining time until the demo deadline if known, else 8 hours — record that assumption in `.hackathon/run-ledger.md` and proceed. Name the planned demo's strongest moment and weakest point in one line each; the weakest point is where the highest-value features usually live.
3. On an explicit ask after the first build: map what is actually built — entry points, data model, key flows, what the demo shows today. Use `code-explorer` (agent — spawn as a subagent) or `code-tour` if the codebase is unfamiliar. Name the demo's current strongest moment and weakest point in one line each.

Record the grounding in `.hackathon/run-ledger.md` (≤20 lines) and the final report as needed.

### Phase 1 — Brainstorm with subagents (parallel, four lenses)

Dispatch four brainstorm subagents **in parallel, in one message**. Each gets the same grounding (original idea, what is built or scoped, strongest moment, weakest point, hours left, and the decisions extracted from `docs/decision-record.md` in Phase 0, pasted inline in this dispatch — never just the filename) and a different lens. Hours left is the value from `docs/scope.md`, or the Phase 0 default assumption if not recorded — never block on it being present. If the decision record does not exist, the grounding is the raw user prompt plus `docs/scope.md` (Phase 0 fallback). Each returns 3–5 candidates, no more — a long list is a sign nobody prioritized. A candidate can be a feature or a tool/integration — a tool candidate names the tool (a named API, SDK, or library) and the capability it unlocks for the product.

**Lens A — Demo impact.** What would make the demo visibly better to a judge or user watching for two minutes? New things to show, clearer moments, a stronger wow. Think in demo beats, not feature lists.

**Lens B — Depth and quality.** What would make the product actually work better, not just look better? Missing handling, rough edges, things that are half-built, data the product already has but does not use, workflows that dead-end. Prefer features that reuse existing data, logic, and screens over ones that need entirely new systems.

**Lens C — Bold bets.** What would make this category-defining instead of just better? One or two ambitious ideas, honestly tagged as risky. A slate with no bold bet is a slate that settled.

**Lens D — Captivating / mind-blowing.** What would make this the most memorable project in the room — a surprising interaction, a striking visual, a demo moment that lands? Not decoration: a concrete moment a judge remembers after seeing ten other projects.

Each subagent must work divergently before converging. Use these moves, adapted from the ideation literature:

- **Adjacent mapping.** What sits one step away from a feature that already exists? (A list that exists → search, filter, sort. A single record → history, comparison, export.)
- **Collision.** Take two things the product already does and combine them into something neither does alone. (Existing data + existing action = new capability.)
- **Gap finding.** Where does a user hit a dead end, an empty state, a manual workaround, or a "you can't do that here"? Every gap is a feature candidate.
- **10x reframing.** What would this look like if it had to be ten times better, not ten percent better? Keep the answer only if a concrete version of it is buildable in the time left.
- **Contrarian inversion.** What if the obvious fix is wrong — what is the opposite approach, and does it fit better?
- **Cross-domain analogy.** What does a good product in a different domain do at this exact moment, and does that move translate here?

Each candidate must be returned in this shape — nothing longer:

```
- Feature or tool: [name, phrased as the user problem it solves, not the solution]
- Tool/API: [named tool, API, SDK, or library this feature needs — or none]
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

1. **Deduplicate.** Merge candidates that are the same feature in different words. If two lenses found the same gap independently, that is a signal, not a duplicate — note it and keep one copy. Preserve the Tool/API value through dedup: the surviving copy keeps its Tool/API cell, and if merged candidates name different tools, keep both (or the one the surviving candidate needs) — never drop the Tool/API column in the merge.
2. **Cut the weak.** Drop anything that duplicates shipped functionality without saying so, anything with no clear quality gain, and anything whose effort exceeds the time left. A short, strong list beats a long, padded one.
3. **Check the balance.** The shortlist must contain at least one bold bet (Lens C) and at least one depth/quality item (Lens B). **Re-brainstorm cap (shared, stated once): one extra round total per run, shared across both triggers below — the balance-miss round and the empty-shortlist round are the same single round, not one each.** If the balance does not hold, note the gap in `.hackathon/run-ledger.md` and in the Phase 6 report (no user is present to tell — do not wait for the user) and ask the brainstorm agents for one more round on the missing lens — that round is the shared cap round. Terminal rule: if the balance still misses after that one extra round, proceed unbalanced — do not re-brainstorm again — and note "proceeded unbalanced: <missing lens>" in the ledger and the Phase 6 report. Empty-shortlist edge case: if every candidate is cut, proceed with zero expansions — re-brainstorm at most the one shared-cap round (this round counts toward that cap; if the cap round was already spent on a balance miss, there is no second round) — note "zero expansions — all candidates cut" in the ledger and the Phase 6 report, and continue to Phase 4 with the MVP scope only.
4. **Sanity-check the why.** For the top candidates, run `product-lens` in your head or for real: does this feature serve a real user job, or is it decoration? Cut decoration.
5. **Write the proposal as a table in the reply.** The table is recorded in `.hackathon/run-ledger.md` (≤20 lines) — if the table exceeds the 20-line ledger, the full table goes in `docs/expansion.md` (a dedicated file that exists at Phase 3 time) and the ledger carries a one-line pointer to `docs/expansion.md`.

```markdown
| # | Feature (user problem) | Why it improves quality | Effort | Depends on | UI | Tool/API |
|---|------------------------|-------------------------|--------|------------|----|----------|
| 1 | ...                    | ...                     | S/M/L  | ...        | Y/N | ...      |
```

Keep it to 4–7 features. More than that means nothing was prioritized.

### Phase 3 — Planner pass: approve, tweak, or reject (fast)

Hand the proposal table to the planner. In this plugin there is no separate planner agent, so the orchestrating agent runs the planner pass itself, in the planner role:

For **each** feature, exactly one verdict:

- **Approve** — build it as proposed.
- **Tweak** — build it with a stated change (smaller scope, different approach, different file). The tweak is one sentence, not a redesign.
- **Reject** — do not build it, with a one-line reason (too big for the time left, duplicates something, weak quality gain, contradicts a recorded decision in `docs/decision-record.md`).

The planner pass also decides **implementation order** (dependencies first, quick wins that unblock the demo early) and flags **risks** per feature in one line each (what is most likely to break, and what the fallback is if it does).

Rules for this pass:

- The output is the proposal table with a verdict column added, plus order and one-line risks — recorded in `.hackathon/run-ledger.md` (≤20 lines) and in `docs/expansion.md` as needed; if the table exceeds the 20-line ledger, the full table goes in `docs/expansion.md` (a dedicated file that exists at Phase 3 time) and the ledger carries a one-line pointer to `docs/expansion.md`. Orchestrate's final report (step 6) picks the table up from `docs/expansion.md` if the table overflowed there, else from the ledger.
- No PRD, no spec. Test expectations ride in the Phase 4 briefs, per hackathon-mode §4.
- The planner judges every feature with `docs/decision-record.md` in front of it — a feature that contradicts a recorded decision is rejected, never tweaked around the decision.
- If one feature's verdict is genuinely ambiguous (approve vs. reject changes the product's direction), use `council` for that feature only. Do not convene a council for the whole list. During the first build, and during a one-prompt removal of a first-build feature, the council must NOT ask the user — if the question is vague, resolve it by stated assumption (safe/reversible default); never ask.
- The planner never adds new features. If it spots a gap, it notes it for the final report.

**Planner scoring rubric (before the verdict).** Score each shortlisted candidate 1–3 on each of these, then select by impact vs. effort: **user value** (does it serve a real user job, not decoration), **originality** (does it make the product distinct, not more of the same), **feasibility** (can it actually be built and verified in the time left), **technical differentiation** (does it do something hard or novel, not a thin wrapper), **visual/demo impact** (does it make the demo visibly better in two minutes), and **implementation effort** (the S/M/L estimate from Phase 1 — low effort scores high here). Approve the high-impact, low-effort candidates first; a bold bet (Lens C) may be approved on originality + differentiation even at higher effort, but only one such bet, and only with a stated fallback. Then check the approved set tells **one coherent product story**: one sentence naming what the product is and why these features together make it captivating — if a feature does not fit that sentence, tweak it until it does or reject it. Fewer exceptional features beat many mediocre ones. The scores live in the proposal table's verdict column area (one compact `value/originality/feasibility/differentiation/demo/effort` score string per feature) and the story sentence goes in the ledger and the Phase 6 report.

**The decided table goes straight into the build — no user approval step.** The planner's approved list is the scope for Phase 4. The user sees the decided table in the final report (Phase 6) and removes anything unwanted with one prompt through `orch-change-feature` — except during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature, where the gate auto-approves and the run proceeds without waiting; that is the intended correction path.

### Phase 4 — Implement the approved features automatically

Dispatch implementers per approved feature, following the execution pattern below. This is the only phase that writes code. During the first build, the approved features are built as part of that build, alongside the MVP slices — not as a second pass after the product works. **Single owner:** in the orchestrate-driven first build, Phase 4 does NOT dispatch its own implementers — it hands the approved list to orchestrate, and orchestrate's slicing owns building the expansions (so nothing is built twice), using this Phase 4 brief format (Tool/API cell + UI rule + capped 2-round fix loop + per-feature `code-reviewer` pass) — orchestrate slicing uses it, it does not invent its own. Phase 4 dispatches its own implementers only on a standalone run (an explicit post-first-build ask, or a standalone `orch-build-mvp` run where orchestrate is not driving — there the GAN loop in `orch-build-mvp` step 4 drives them).

**Team shape.** Use the smallest team that helps: one implementer per feature, up to 4 in parallel. Features with dependencies go in waves (dependency first, dependents after). Features with overlapping write scopes go sequential, never parallel. One feature is a valid team — do not parallelize for its own sake.

**Briefs.** Each implementer gets a self-contained brief, inline in its dispatch — never a bare reference to "read the plan". Briefs name the skill AND carry self-contained inputs, so the implementer never has to go read another document to start. A brief contains:

1. One line on where this feature fits in the product and why it was approved.
2. The exact outcome: what the user can do after this lands that they could not do before, and which files it touches — during the first build, the planner states the intended file layout and interface decisions explicitly in the brief instead of pointing at files that don't exist yet. The scaffold owns the final layout (the scaffold = orchestrate's first-wave slice built via `app-scaffold`, per orchestrate step 3): if the implementer must move a file from the intended layout, the implementer records the move in its result (status, old path → new path) and the orchestrator reconciles it in the collect-and-reconcile step below.
3. Constraints: global rules that bind this feature (the plugin's hackathon-mode rule, the UI rule below, any interface or data-shape decision from an earlier feature — stated explicitly in the brief, not by reference).
4. Completion evidence: the exact commands or checks that prove it works (run the app, exercise the feature, confirm the visible result). Verification is tests AND running it: the tests the brief requires plus running the feature and confirming the visible result — pre-MVP, running it means running the feature in isolation (the whole app may not exist yet).
5. A soft time budget matching its effort estimate (S/M/L from the proposal). Report blocked with partial evidence rather than grinding past it.
6. The stopping rule: implement the brief exactly. If it is infeasible or needs redesign, report blocked with evidence instead of a replacement plan. Never redesign, never return another plan. **Belief in the brief:** trust the brief and build it — do not second-guess the plan, hedge, or wait for reassurance; commit to the approach and make it work; if a detail is ambiguous, pick the reasonable option and note it, don't stall.
7. Tool/API: the proposal's Tool/API value for this feature, named explicitly (the named tool, API, SDK, or library from the Phase 2 table — or "none") — the implementer wires that tool, not a substitute it picks itself.

**UI rule (no exceptions).** Any feature that touches UI goes through the full design package: `ui-ux-pro-max` and `less-flat-ui` together, plus the Impeccable craft floor via `polish-pass` and the Harmony rule — except on a full landing/company page, where `design-taste-frontend` leads (with the dealt Hallmark theme) per hackathon-mode §5, and `ui-ux-pro-max` + Impeccable via `polish-pass` + Harmony still apply. Conditional components apply by surface type, never by size: motion work adds `make-interfaces-feel-better` (then the motion-* skills for React/Next motion); new design-system work adds `design-system`; legacy style drift adds `inherit-legacy-style`. The implementer's brief says so explicitly, names the applicable components, and records the feature's direction (from `docs/decision-record.md` / `docs/design-tokens.md`, named, never "modern clean") BEFORE any UI is built — and the implementer applies them to every surface the feature adds or changes, however small. If a feature needs a named API, SDK, or tool wired in, use `integration`; if it needs generic REST-client mechanics on an unnamed API, use `api-integration`; if it needs auth or a database, use `app-scaffold`; if it needs to be live, use `deploy-fast`. If a feature is AI-powered (model choice, prompt/context contracts, output schema, fallbacks, eval), use `ai-feature-spec`. Name the skill in the brief — implementers do not load skills by name on their own.

**Fix loop (capped).** If a feature lands but its verification fails, the implementer fixes it and re-verifies — at most 2 rounds. Past that, the feature is reported blocked with evidence, the orchestrator notes it, and work moves on to the next feature. No open-ended fix loops, no re-review rounds. A blocked feature is not a failed skill run.

**Collect and reconcile.** After each wave, read every implementer's result (status, changed files, verification evidence, residual risks, blockers). Confirm the reported files exist, stayed in scope, and carry verification evidence. If an implementer moved a file from the planner's intended layout (the scaffold owns the final layout; the implementer records the move), record the actual layout in `.hackathon/run-ledger.md` and use the actual layout in later briefs. Collision procedure (sequential dispatch for overlapping scopes is the prevention rule; this is what happens if a collision still occurs): if two implementers in the same wave touched the same files, the orchestrator decides the merge order; the first-listed implementer's files win on conflict unless the planner marked a dependency (then the dependency's files win); record the decision in `.hackathon/run-ledger.md`; dependents proceed on the merged result. Scaffold-vs-expansion collision: if the scaffold's first slice and an expansion feature touch the same files, the same rule applies — the orchestrator decides the merge order (scaffold first unless the planner marked the expansion as the dependency), records the decision in the ledger, and dependents proceed on the merged result. When orchestrate runs the build, orchestrate owns reconciliation; on a standalone `orch-build-mvp` run, `orch-build-mvp` step 5 (reconcile) owns it. Do not add agents or change scopes because one implementer is slow or quiet; handle it by waiting for its terminal result, then deciding.

**Review step.** Each landed feature goes through `code-reviewer` once before its verification counts as complete — the review happens first, then verification; reviewer findings are fixed inside the capped 2-round fix loop above (at most 2 rounds) or the feature is noted as blocked. This is a code-review pass, not an approval gate: it never asks the user anything and never blocks on anything but the feature's own defects.

**Build breaks.** A build or type error during implementation goes to the `build-fix` command or the `build-error-resolver` agent (spawn as a subagent; pick the per-language one if the feature is single-stack). Do not hand-debug inside the orchestrator.

### Phase 5 — Verify the whole (main agent, once)

**Trigger — one definition.** This phase runs exactly once, when the MVP is built AND every approved expansion feature is in or blocked with evidence. (On an explicit ask after the first build, the trigger is the same minus the MVP clause: when every approved feature is in or blocked with evidence.) It never runs before building starts — expansion features are verified together with the MVP in the whole-build verification steps below. **Ownership:** in the orchestrate-driven first build, expansion Phase 5 IS orchestrate's Verification stage (orchestrate step 5), which runs the checks BY NAME — `browser-qa` / `click-path-audit` / `verification-before-completion` per feature. In a standalone `orch-build-mvp` run, expansion Phase 5 runs in `orch-build-mvp` step 6 (verification).

1. Run the app. Walk the demo flow end to end — `browser-qa` for the deployed or local flow, `click-path-audit` if buttons or shared state were touched. The demo must work. If a feature broke the demo, that feature is reverted or fixed now, before anything else.
2. Confirm every landed feature with `verification-before-completion`: run it, read the output, then claim it.
3. If the demo story changed (a new wow moment, a different flow), note the new story in one paragraph. If the user wants the pitch re-cut, `hackathon-pitch` is available — offer it, do not run it unasked.

### Phase 6 — Report: expansion section for orchestrate's final report (short)

Contribute this section to orchestrate's whole-build final report — this is not the final report itself; orchestrate folds it in. **Named producer:** in the orchestrate-driven first build, ORCHESTRATE composes this section from the stage ledger + the implementers' return texts; in a standalone `orch-build-mvp` run, `orch-build-mvp` step 9 takes it. Handoff mechanism: write this section to `.hackathon/run-ledger.md` (expansion section, within the ledger's ≤20 lines — if the Phase 6 section exceeds the ledger's 20 lines, append the full Landed/Blocked lists (with files) to `docs/expansion.md` and leave a one-line pointer in the ledger; long tables go in the return text instead) AND include it in the Phase 6 return text (landed / blocked / rejected lists). Orchestrate takes it from there. It contains:

- **Landed:** each feature, one line, what it does now, with the files it touched — this is the feature-to-files inventory, so a later removal does not have to re-derive them.
- **Blocked:** each blocked feature, one line, why, and what the fallback is.
- **Rejected or cut:** the planner's rejects, one line each (so the user knows what was considered).
- **Assumptions:** every assumption made during expansion, one line each.
- **Removable:** each landed expansion feature with its files (from Landed above), so the user can remove it with one prompt through `orch-change-feature`.
- **Demo now:** one paragraph — what to show, in what order, and where the new wow moment is.
- **Not built:** any new idea spotted during implementation, listed only, never built.

Then stop. Do not loop back to Phase 1 unasked. If the user wants another round, they will say so. If the user asks to remove something that was added, that is a normal one-prompt removal through `orch-change-feature` only — except during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature, where the gate auto-approves and the run proceeds without waiting — not a failure of the expansion.

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
| UI on any touched surface | full design package: `ui-ux-pro-max` + `less-flat-ui` + Impeccable via `polish-pass` + Harmony (except a full landing/company page: `design-taste-frontend` leads with the dealt Hallmark theme; direction recorded in `docs/design-tokens.md` before building; conditional by surface type: motion + `make-interfaces-feel-better`, new design-system work + `design-system`, legacy drift + `inherit-legacy-style`) |
| Integrations a feature needs | `integration` (named API/SDK/tool), `api-integration` (generic REST-client mechanics on an unnamed API), `app-scaffold`, `deploy-fast` |
| AI-powered feature spec | `ai-feature-spec` (model, prompt, fallbacks, eval) |
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
- **Subagent-Driven Development** (`obra/superpowers`, MIT) — the task-loop mechanics used in Phase 4: dispatch with a brief as the single source of requirements, a report contract, and a capped fix loop. Used with attribution; the two-stage review gates (spec compliance + code quality), the final whole-branch review, and the helper scripts were deliberately left out, per this plugin's no-review-gates rule (the single `code-reviewer` pass in Phase 4 is a code review, not one of those gates).
- **ecc-planner** (`affaan-m/ecc`, MIT) — the planning role used in Phase 3. The stock planner agent was NOT copied into this plugin: it activates proactively and its plan format mandates a Testing Strategy section, which violates this plugin's lightweight-planning rules. Only the planning capability it represents (break features into ordered steps with file paths, dependencies, and risks) was folded into the planner pass above, in a lightweight approve/tweak/reject form.
