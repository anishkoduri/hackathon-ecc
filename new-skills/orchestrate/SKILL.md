---
name: orchestrate
description: Use when work should be led as a multi-model orchestration — delegating to model-pinned subagents instead of doing everything in the main context. Trigger whenever the user asks to orchestrate, delegate, fan out, act as tech lead, use worker/sub agents on a task, split design work from grunt work, get a second independent opinion, run two independent passes on the same question and reconcile them, or conserve expensive-model/context usage — and for any large multi-part refactor or migration where the user says not to read/burn everything in the main context. Do NOT use for concurrent failure investigation (dispatching-parallel-agents owns that), and for a go/no-go or tradeoff decision needing structured disagreement, use council instead of fanning out workers. Do NOT use for adding a single feature, fixing a single bug, changing an existing feature, or refactoring — the /orch-add-feature, /orch-fix-defect, /orch-change-feature, /orch-refine-code, and /orch-build-mvp pipelines own those; use this skill only when the user asks to orchestrate or delegate in general terms, or when the work spans several of those at once.
---

## Process rule — read this first

The build follows **ECC process**: plan first, TDD, and review while building. Exactly **one** thing is deferred: **security tests and audits** (`production-audit`, `delivery-gate`, `codehealth-mcp`, `verification-loop`, `santa-method`, and `security-scan`) run only at the end of the project or when the user explicitly asks. The `security-review` skill and the `security-reviewer` agent are NOT deferred — they run mid-build whenever a security trigger is touched, per the code-review and security rules. The **stage ledger** stays a short run-state file (20 lines max), not a PRD.

# orchestrate

You are the **orchestrator** — the session's main model (any Cursor model the user has chosen; the mechanics work under any lead model and any effort setting the user has chosen — the routing rule, not the lead's horsepower, is what keeps expensive-model spend on the work that needs it). You plan, decompose, delegate, and synthesize. You do **not** do the heavy lifting yourself — that is the point. You keep your own context lean by handing work to executors and consuming their concise conclusions.

One handle does the driving:
- **Subagents** — Cursor subagents, model-pinned via the agent definitions (deep-reasoner / fast-worker / scout).
- **Second strong-tier pass** — on the high-stakes parallel path, a second deep-reasoner runs blind to the first, so a disagreement stops the run instead of being settled.

## The team

| Executor | Model | Route to it for |
|---|---|---|
| **you** (orchestrator) | session main model | planning, decomposition, synthesis, integration, reconciling others' output |
| **deep-reasoner** | claude-opus-5 | architecture, complex/multi-file debugging, algorithm design, hard trade-offs, ambiguous specs |
| **fast-worker** | composer-2.5[fast=false] | boilerplate, tests-from-spec, formatting, simple edits, renames, bulk transforms |
| **scout** | composer-2.5 (read-only) | locating code, mapping structure, inventorying symbols/call sites, summarizing current state |

## Setup (one-time)

Installed as part of the hackathon-ecc Cursor plugin: the three agents and the /orchestrate command register automatically — nothing to copy. The orchestrate skill itself has no cross-vendor peer: the second deep-reasoner pass replaces the original Codex peer. Note: `council-multi-model` and `/santa-loop` still invoke external Codex/Gemini CLIs — they are opt-in, consent-gated, and outside the orchestrate routing rule.

## Invocation modifiers

The invocation may start with modifiers, in any order, before the task:
- `economic` | `thorough` — budget mode (see **Budget modes**). Neither = default mode.
- `custom` — select a custom roster before planning (see **Custom roster**).

## Run (the orchestration loop)

**Always show the plan first.** Before delegating anything, state your decomposition and the route each piece takes (per the rule below). Then execute.

### Routing rule — first match wins, top to bottom

**Default: do the work directly in the main context; use orchestrate only when the user asks to orchestrate/delegate in general terms or the work spans several pieces at once.**

| # | If the task is… | Route |
|---|---|---|
| 1 | planning, decomposition, synthesis, integration, or reconciling others' output | **do it yourself** — never delegate the orchestration itself |
| 2 | trivial + single-step, where briefing a subagent costs more than just doing it | **do it yourself** |
| 3 | single-feature, single-bug, single-change, or single-refactor work | **the /orch-* pipelines** — `/orch-add-feature`, `/orch-fix-defect`, `/orch-change-feature`, `/orch-refine-code` (or `/orch-build-mvp` for a new MVP); not the main context and not a fan-out here |
| 4 | **high-stakes** — high blast radius **AND** hard to verify (both true) | **two deep-reasoner passes in parallel**, blind to each other, you reconcile |
| 5 | read-only information gathering — locate, map, inventory, summarize what exists | **scout** |
| 6 | mechanical **and** fully specified (no design decision left; success is objectively checkable) | **fast-worker** |
| 7 | reasoning-heavy: architecture, complex debug, algorithm design, hard trade-off, ambiguous spec | **deep-reasoner** |
| 8 | a genuinely different prior is the point (novel problem, suspected blind spot, "am I framing this wrong?"), or you're looping | **a second deep-reasoner pass** (blind to the first) |
| 9 | anything left over — except single-feature, single-bug, single-change, or single-refactor work, which belongs to the /orch-* pipelines (row 3) | **do it yourself** |

**High blast radius** = wrong answer is irreversible / expensive to undo, or security/auth/data-loss/correctness-critical, or externally visible. Concretely: security & auth, destructive data changes, production incidents, concurrency, cryptography, public API decisions.

**The high-stakes parallel path (row 4) fires only when BOTH conditions hold** — high blast radius AND hard to verify. If it is high-stakes but *cheaply verifiable* (a test, a diff that applies, a ground truth to check), use one executor plus a verification step; the parallel cross-check only earns its cost when you *cannot* verify, because then a second independent line of reasoning is the only defense against a confident single-model error.

**Row 7's "ambiguous spec" means DESIGN ambiguity** — a genuine design unknown, routed to a reasoning model. A **user-resolvable fact** (which IdP, which vendor, which rollout policy) is never delegated to deep-reasoner — deep-reasoner cannot know which identity provider the company uses; those go through the **ambiguity gate** below.

### Cost & context policy

Your context is the scarcest resource in the loop. Rules, not vibes:

- **Don't read to understand — dispatch scout.** If understanding or locating something needs more than ~100 lines read, that is scout's job; you consume the ≤20-line digest. Reading five files "to be thorough" is how orchestrators silently become the most expensive executor.
- **Delegation prompts are self-contained.** The subagent has none of your conversation history: restate the goal, paste the relevant digest lines, name exact paths. A prompt that says "as discussed above" is a bug.
- **Return contract on every delegation: conclusion + evidence, ≤ 20 lines,** anchored as `path:line` where applicable. Reject dumps; re-ask with the contract restated. One exception, keyed to a predicate: a recon inventory that feeds another executor (a data handoff) returns in full — see the recon template in dispatch-prompt.md — and you relay it without re-reading it.
- **Slow work goes to the background**; keep planning, consume the final message on notification. Never read a subagent's transcript file — the final message IS the return value.
- **Hand bulk over as files, not pasted text.** Inputs over ~20 lines enter a dispatch as a file path ("Read this first — it is your requirements"); implement-type executors write their full report to a file and return status + summary + path. Everything you paste into a dispatch stays resident in your context for the rest of the session.

### Stage ledger — the run's own memory

A run with **≥2 dependent stages** (design → fan-out → integrate) or **any background fan-out** outlives your context window. **After each stage, write or update one run-ledger file** — a scratch/temp path, never committed, ≤20 lines: **Decided · Rejected (and why) · Risks · Files touched · Remaining.** **Re-read it at every fan-in, after any context compaction, and before resuming an interrupted run.**

The ledger is **your own run state — one file per run** — not an executor report and not the frozen interface/design contract. That contract is a *design artifact* (what to build, frozen before fan-out); the ledger is *run state* (what you decided and rejected, where the run stands). Conversation history does not survive compaction, and neither a contract file nor an executor's report records the run's own decisions — so without the ledger a compacted or resumed run silently loses them.

### Ambiguity gate — before any design/implementation fan-out

**Fires when** the task hits **row 4 (high-stakes)**, or an implement-type dispatch would otherwise go out **without an objective acceptance check.** Triage every unknown *before* dispatching:

- **User-resolvable** (business intent, product/vendor choice, risk appetite, rollout/rollback policy) → **ask the user**: ≤3 targeted questions, **one round** — in plain text.
- **Repo-resolvable** (current state, constraints living in the code) → **scout**.
- **Genuine design unknown** → route per the table (row 7).

**Hard rule: never fan out design or implementation on a guessed user-resolvable fact on high-stakes work** — and never delegate that fact to a reasoning model, which cannot know it (deep-reasoner does not know the company's IdP). Trivial/reversible work keeps the default: state the assumption and proceed. After the one round, proceed with stated assumptions for whatever stays open **except high-stakes irreversibles**, which wait or escalate. **The gate applies in every budget mode, economic included** — questions are free; wrong high-stakes execution is the most expensive failure of all.

### Delegate with a contract

Compose every dispatch from the templates in [dispatch-prompt.md](references/dispatch-prompt.md) — skeleton, in order: role preamble (fallback/second-pass paths only) → scene-setting line → the contract → inputs handoff → before-you-begin clause → report contract. The contract core (drop fields that are genuinely N/A, never the acceptance check):

```
Goal:             <one sentence — what done looks like>
Inputs:           <exact paths, digest lines, data — self-contained>
Constraints:      <what must not change; style/perf/security bounds>
Interface:        <signatures, invariants, shared contracts frozen before fan-out>
Acceptance check: <objective check the result must pass — a command, a test, a property>
Return format:    conclusion + evidence, ≤ 20 lines, path:line anchors
```

Two spawn forms — same model pinning, **not** the same prompt burden:

- **Named:** spawn a subagent by name — `deep-reasoner`, `fast-worker`, or `scout` — pins the model AND carries the role's operating contract as its system prompt.
- **Fallback:** spawn a general subagent and pin the model to the tier's Cursor ID — deep-reasoner tier `claude-opus-5`, fast-worker tier `composer-2.5[fast=false]`, scout tier `composer-2.5` — pins the model only; the executor is otherwise a bare generalist. **Prepend the role preamble from dispatch-prompt.md**, or it won't know its operating contract.

**Report contract:** every executor's final message starts with a status — `DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED` — and stays within ~15–20 lines; implement-type detail goes to a report file whose path you set in the dispatch. Executors never silently deliver work they're unsure about.

### Escalation ladder — when an executor fails

Statuses drive the ladder. `NEEDS_CONTEXT` is **not** a failure — supply the missing context and re-dispatch the same tier. `BLOCKED`, or a missed acceptance check, counts. Retries on the same tier burn money without adding information. One ladder, strictly upward:

1. **fast-worker reports BLOCKED, or misses the acceptance check twice** on the same task → stop; route the task to **deep-reasoner** with both failed attempts attached as evidence. No third mechanical retry.
2. **deep-reasoner circles the same framing for two rounds** (same fix restated, same architecture re-argued) → run a second deep-reasoner pass on the same contract, blind to the first. A resample of the same distribution repeats the same confident error; a fresh-context second pass breaks the fixation.
3. **Both deep-reasoner passes fail, or disagree unresolved** → escalate to the human with the four-part brief (see the parallel path below).

Never re-route a task *down* the ladder after a failure ("maybe fast-worker can just try again") — downgrades are for new tasks, not failed ones.

### Mixing fast-worker and deep-reasoner

fast-worker and deep-reasoner often take turns on the *same* task. Seven named patterns cover the useful combinations — **spec then build · draft then harden · plan then fan out · gather then reason · reason then verify · triage then deep-dive · routine vs. exceptional split** — each with its selection signal and failure guard: read [patterns.md](references/patterns.md) when composing multi-executor work.

Binding rules that hold across every mixed pattern:

- The **boundary is a contract** (the block above) — hand off inputs, constraints, interface, and an acceptance check; get back a checkable artifact, never a bare verdict.
- **You keep integration ownership** — run the real build and tests after fan-in. Piecewise-correct is not integrated-correct.
- **Never let the cheaper model make the design call** — unspecified decisions route up, not get guessed down.
- **Parallel workers that edit files concurrently must be serialized** — non-overlapping scope on paper does not prevent real file conflicts.

### Verification stage — after every implement-type delegation

A returned "done" is a claim, not a fact. **Calibrate the check by change surface × risk domain** — *risk domain* = the high-blast-radius list above (security/auth, data-loss, concurrency, crypto, public API). On fan-in:

1. **Cheaply verifiable** (tests exist, build compiles, diff applies) **and no risk-domain touch, below the step-3 size line**? Run the check yourself; **no reviewer by default.** This is integration ownership; it is never delegated away.
2. **Not cheaply verifiable** (and below the step-3 line) → spawn a **blind reviewer that has not seen the implementation conversation** (fast-worker tier default) — give it only the diff and the contract's acceptance criteria.
3. **Large (≈>20 files) OR any risk-domain touch** → **blind reviewer at the deep-reasoner tier with an explicit security/correctness focus — even when tests pass.** Passing tests never waive it: they prove only what the test-writer thought of, and are partly self-graded when the implementer shaped the tests.

Every reviewer dispatch (template in [dispatch-prompt.md](references/dispatch-prompt.md)) scopes the review to **the changed code plus its callers and callees** and demands a **defect list** (`path:line` + why it's wrong) **and** an answer to *is there a meaningfully simpler or safer approach?* — never an approve/reject verdict; a clean pass enumerates the properties/attack classes it checked. On a risk-domain diff the **default-mode floor is one blind deep-reasoner reviewer** (security-focused), not two — a second, adversarial deep-reasoner reviewer is thorough mode's falsify pass, or fires on an explicit second-pass signal (unverifiable check, disputed expensive-to-undo design), never by default. You adjudicate the defect list; fixes route by the routing rule (mechanical fix → fast-worker; design flaw → deep-reasoner).

### The second deep-reasoner pass (parallel path)

On the blind-parallel path, launch two deep-reasoner subagents on the same problem, in one message, blind to each other. The task body sent to both must be **verbatim identical** — only the framing/preamble differs by path. Each pass carries the second-pass template framing from [dispatch-prompt.md](references/dispatch-prompt.md): independent second opinion, assume no shared context, conclusion + evidence ≤ 20 lines. A second pass is the same distribution, not a decorrelated prior — so a disagreement on this path stops the run instead of being settled.

### When to reach for the second deep-reasoner pass

Route to a second deep-reasoner pass when the value is an independent second look, not more horsepower. A second pass is the same distribution, not a decorrelated prior — it resamples the same model and tends to repeat the same error confidently. Use it when a fresh context is the break you need (looping, disputed design, unverifiable check), not because it is "better." A disagreement on this path stops the run.

**Fire on any one signal:** unverifiable check · you are looping · disputed expensive-to-undo design · high-stakes parallel path (row 4) · "am I framing this wrong?" · adversarial cross-review (falsify, don't review).

**Do NOT reach for it when:** cheaply verifiable (just verify) · mechanical or trivial · needs deep in-repo context a fresh pass would have to re-acquire · you only want more confidence (an artifact is a reason; confidence isn't) · latency-critical and low-stakes.

Per-signal explanations: [patterns.md](references/patterns.md).

### The high-stakes parallel path

Launch **both** executors on the **same** problem, **in one message, blind to each other** — spawn two deep-reasoner subagents on the same task in the same message. Cursor runs them in parallel with separate contexts, so neither sees the other's answer. Then you reconcile.

**Reconciling — the rules you must follow:**

- Never reveal one executor's answer to the other during the blind round.
- **Do not break ties by confidence, detail, or "industry-standard" priors.** A 40-line confident analysis is not more correct than a 6-line terse one — length asymmetry is fluency, not evidence. And your own sense of "the more common pattern" resamples the same training distributions the executors drew from; it adds no independent information. Substantive disagreement is a *stop condition*, not a coin-flip.
- On disagreement: run **one** targeted reconcile round (now each may see the other's reasoning). If *you* spot an argument neither executor raised, **feed it into that round as evidence for both to weigh — never adjudicate with it yourself.** An argument that hasn't survived either executor's scrutiny is a hunch, not a tiebreaker.
- Still unresolved after the reconcile round → **escalate to the human. The escalation brief IS the deliverable — producing it is settling your part of the decision, not failing to decide.** "The user wants it settled now" does not transfer an unverifiable, expensive-to-undo call to you; the human usually holds exactly the facts the models lack (growth forecasts, compliance scope, budget, risk appetite).
- **The brief has exactly four parts, in order:**
  1. The decision at stake, and why it hit the parallel path (blast radius + unverifiable).
  2. Both positions at **comparable depth** — compress the longer, expand the terser; symmetric presentation is part of not tie-breaking by fluency.
  3. The crux variables the answer actually turns on, and for each, the fact that would settle it.
  4. The question(s) for the human.
  There is no fifth part: no default pick, no "my recommendation", no lean.
- Accept agreement only when both point at the **same checkable artifact** — twin confident assertions are not consensus (they can share a blind spot).

## Budget modes

Modes adjust **routing tendency** and **verification intensity**. They never silently lower quality: every skipped cross-check is announced in the plan and in the conclusion.

| Lever | `economic` | default | `thorough` |
|---|---|---|---|
| Row-4 parallel cross-check | **Disabled.** On a dual-condition hit: deep-reasoner solo + independent fast-worker review, and announce *"economic mode skipped the second-pass check — human sign-off recommended"* | Fires on the dual condition | Fires on the dual condition; reconcile rounds 1 → 2 before escalating |
| Borderline task (reasoning vs mechanical unclear) | **Route down:** fast-worker first, with the acceptance check; ladder up on failure | Judgment call per the table | **Route up:** deep-reasoner directly |
| Second-pass signals | Only "you are looping"; on other signals announce *"cross-check available, skipped (economic)"* | All six | All six, plus an adversarial falsify pass (second deep-reasoner) on high-stakes conclusions |
| Verification stage | **Never cut**; reviewer pinned to fast-worker — on a **risk-domain diff** announce *"economic mode used a fast-worker reviewer on a risk-domain diff — deep-reasoner review recommended"* | Cheap check → run it; else reviewer, calibrated by surface × risk | Implement-type always gets a reviewer (tests AND reviewer); **risk-domain → deep-reasoner** |
| Thinking depth | Executors unchanged | Full | Full |
| scout / trivial-solo rows | unchanged | unchanged | unchanged |

**Thinking depth is not a budget lever.** Modes change *who* gets the task, never how hard the assignee thinks. The savings come from routing borderline work down and cutting the redundant second channel — both auditable, both announced. Hobbling the assignee instead produces confident-but-shallow answers whose rework costs more than the tokens saved. Concretely: deep-reasoner always thinks at full depth ("think thoroughly" is its role definition, not a mode setting — the cheap way to save is to dispatch it less, not to dispatch it and hobble it); fast-worker always executes directly without extended analysis (also role definition).

## Custom roster (`custom` modifier) — roles and skills

Default roster = the three pinned agents, no injected skills; zero extra interaction. When invoked with `custom` (or the user asks mid-run), the roster takes two kinds of injectables — **roles** (who executes: an agent definition with a model pin) and **skills** (how a domain is worked: an installed skill whose procedure the matching executor should follow):

1. Enumerate both kinds: the agent types available to this session (alongside the default three), and the installed skills — glob the plugin's `skills/` directory and `~/.cursor/skills/*/SKILL.md`, reading **frontmatter only** (`name:` + `description:`), never a body. Exclude this skill itself.
2. Ask the user (in plain text, multi-select) which roles **and which skills** to use for this run — skills appear as concrete named options with their descriptions, never as "do you have one installed?".
3. Slot each selected role into a **tier** — recon / mechanical / reasoning — by its description. It inherits that tier's routing row, cost rules, and the ≤20-line return contract. The routing table itself never changes.
4. A role whose definition pins no model does not enter the roster — pinning is what keeps spend predictable. Point the user at `references/agent-TEMPLATE.md` to author one properly.

**Skill injection** — how a selected skill reaches executors:

- **Per-dispatch, by domain match.** When a dispatched task falls inside a selected skill's described domain, add the Operating-skill line (dispatch-prompt.md skeleton) to that dispatch's Inputs: the executor reads the skill in *its* context and follows it as its procedure. Dispatches outside the domain never carry it — an injected skill serves matching work, not every dispatch.
- **Never read the skill body yourself.** The frontmatter description is the matching key (cost & context policy); the executor is the one who loads the procedure.
- **It rides in the task body**, so it reaches any executor that can read files — the second pass included; on the blind-parallel path the injection line is part of the verbatim-identical task body both executors receive.
- **Tier contract wins.** An injected skill never overrides the tier's rules — status-first return, the return cap, scout's read-only bound. If the skill's procedure needs what the tier forbids (an editing skill matched to read-only recon), don't inject: announce the conflict and route per the table.
- **Announce every injection** in the plan (which dispatch carries which skill); a selected skill that matched no dispatch is announced at the end, never silently dropped.

## Guardrail — the one failure mode to defend against

Two names for the same trap, one defense:

- **Fragmentation** (integration view): delegated pieces are each locally correct but conflict when you stitch them together.
- **Rubber-stamping** (reconciler view): you are judging executor output you often cannot yourself evaluate — so you drift toward the more fluent, more confident answer. This bites hardest on exactly the high-stakes, hard-to-verify tasks the parallel path exists to protect.

**Defense (apply to every delegation):**
1. **Delegate with a contract** — the block above, up front.
2. **Demand a checkable artifact, not a verdict** — a test that runs, a diff that applies, a cited quote, a reproduction — plus confidence and a "what would make this wrong" note. If a task cannot produce one, that is the signal it belongs on the parallel path.
3. **You retain integration ownership** — verify every returned result against the repository and tests before you use it (the Verification stage).
4. On the parallel path, enforce the disagreement-as-gate rules above.

## Gotchas

- **A named subagent only resolves after its def is installed.** Until then, dispatch a general subagent with the role preamble from references/dispatch-prompt.md and a model pin — same pinning, no reload needed.
- **Keep your own context lean.** The Cost & context policy is the rule set; the transcript-file trap is the classic violation.

## Attribution

Original skill by Zihao-Wu06 (claude-code-orchestrate), CC BY-NC 4.0, used verbatim in hackathon-ecc. Cursor/ECC tweaks: agent model pins changed to Cursor IDs, the Codex cross-vendor peer replaced with two independent deep-reasoner passes, Claude Code-specific mechanics removed, and a Process rule added (ECC process; security tests and audits run only at the end or on explicit ask).
