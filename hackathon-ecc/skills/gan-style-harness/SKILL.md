---
name: gan-style-harness
description: "GAN-inspired Generator-Evaluator agent harness for building high-quality applications autonomously. Based on the upstream multi-agent harness design paper (March 2026). Use when a feature should be built autonomously through generator and evaluator iteration until it clears a quality bar. (In this plugin the harness loop runs in Cursor through `/gan-build` + `/gan-design` and the `ecc-gan-*` agents as Cursor subagents — the skill contributes the harness design, prompts, and rubric, never the CLI commands.)"
metadata:
  origin: ECC-community
---

# GAN-Style Harness Skill

> Inspired by the upstream multi-agent harness design paper (March 24, 2026)

A multi-agent harness that separates **generation** from **evaluation**, creating an adversarial feedback loop that drives quality far beyond what a single agent can achieve.

**Factory routing (fix #29, GLOBAL-ROUTING_F29):** the generator/evaluator loop runs as factory drones — the orchestrator dispatches each generator and evaluator pass as a single-task drone from its queue, with a director brief (DIRECTOR-BRIEF_F29): the exact goal, the files in scope and explicitly out of scope, constraints, acceptance criteria, verification steps, and what to return — an incomplete brief means the drone does not start. Generator and evaluator briefs follow the seven-field contract in `skills/orchestrate/references/dispatch-prompt.md`. A drone that hits a decision its brief leaves unspecified stops and returns the question to the orchestrator instead of guessing (NO-GUESSING_F29). The evaluator pass is an input to verification, not the verify step itself: after each evaluator pass the orchestrator checks the generator's output against the brief's acceptance criteria (not just the rubric score — a rubric pass at or above 7.0 with a failed acceptance criterion is a fail), re-checks the evaluator's pass/fail call against the same criteria, and checks the planner's spec against the brief before the first generator pass; failed output goes back with a correction brief naming the failed criterion (VERIFY-MERGE_F29). Fan-out is bounded by efficiency, N>3 justified in one line, drones carrying minimal context (COST-AWARE_F29); in Cursor, slots refill per wave, not per completion — the factory lights up fully on the later port, not in Cursor (GLOBAL-ROUTING_F29). The orchestrator answers every prompt; drones never answer the user or decide scope (ORCHESTRATOR-ONLY_F29).

## Core Insight

> When asked to evaluate their own work, agents are pathological optimists — they praise mediocre output and talk themselves out of legitimate issues. But engineering a **separate evaluator** to be ruthlessly strict is far more tractable than teaching a generator to self-critique.

This is the same dynamic as GANs (Generative Adversarial Networks): the Generator produces, the Evaluator critiques, and that feedback drives the next iteration.

## When to Use

- Building complete applications from a one-line prompt
- Frontend design tasks requiring high visual quality
- Full-stack projects that need working features, not just code
- Any task where "AI slop" aesthetics are unacceptable
- Projects where you want to invest $50-200 for production-quality output

## When NOT to Use

- Quick single-file fixes (use the Cursor agent loop, never a CLI subprocess)
- Tasks with tight budget constraints (<$10)
- Simple refactoring (use de-sloppify pattern instead)
- Tasks that are already well-specified with tests (use TDD workflow)

## Architecture

```
                    ┌─────────────┐
                    │   PLANNER   │
                    │  (Grok 4.6 High Fast)   │
                    └──────┬──────┘
                           │ Product Spec
                           │ (features, sprints, design direction)
                           ▼
              ┌────────────────────────┐
              │                        │
              │   GENERATOR-EVALUATOR  │
              │      FEEDBACK LOOP     │
              │                        │
              │  ┌──────────┐          │
              │  │GENERATOR │--build-->│──┐
              │  │ (Grok 4.6 High Fast) │          │  │
              │  └────▲─────┘          │  │
              │       │                │  │ live app
              │    feedback             │  │
              │       │                │  │
              │  ┌────┴─────┐          │  │
              │  │EVALUATOR │<-test----│──┘
              │  │ (Grok 4.6 High Fast) │          │
              │  │+Playwright│         │
              │  └──────────┘          │
              │                        │
              │   5-15 iterations      │
              └────────────────────────┘
```

**Orchestrator check (fix #29, VERIFY-MERGE_F29):** the orchestrator sits outside the loop — after each evaluator pass it checks the generator's output against the brief's acceptance criteria and re-checks the evaluator's pass/fail call (a rubric pass at or above 7.0 with a failed acceptance criterion is a fail); failed output goes back with a correction brief naming the failed criterion. The planner's spec is checked against the brief before the first generator pass. The loop's CHECK SCORE step (`commands/gan-build.md` Phase 2) runs only after the orchestrator check passes.

## The Three Agents

### 1. Planner Agent

**Role:** Product manager — expands a brief prompt into a full product specification.

**Key behaviors:**
- Takes a one-line prompt and produces a 16-feature, multi-sprint specification
- Defines user stories, technical requirements, and visual design direction
- Is deliberately **ambitious** — conservative planning leads to underwhelming results
- Produces evaluation criteria that the Evaluator will use later

**Model:** Grok 4.6 High Fast (`cursor-grok-4.6-high-fast`) by default; raise via `GAN_PLANNER_MODEL` (set it to the model selected in this chat) for deeper spec expansion

### 2. Generator Agent

**Role:** Developer — implements features according to the spec.

**Key behaviors:**
- Works in structured sprints (or continuous mode with newer models)
- Negotiates a "sprint contract" with the Evaluator before writing code
- Uses full-stack tooling: React, FastAPI/Express, databases, CSS
- Manages git for version control between iterations
- Reads Evaluator feedback and incorporates it in next iteration

**Model:** Grok 4.6 High Fast (`cursor-grok-4.6-high-fast`) by default; raise via `GAN_GENERATOR_MODEL` (set it to the model selected in this chat) for maximum coding capability

### 3. Evaluator Agent

**Role:** QA engineer — tests the live running application, not just code.

**Key behaviors:**
- Uses **Playwright MCP** to interact with the live application
- Clicks through features, fills forms, tests API endpoints
- Scores against four criteria (configurable):
  1. **Design Quality** — Is the recorded direction applied coherently in code (tokens, type, and spacing trace to it)?
  2. **Originality** — Do the code-level choices trace to the recorded direction rather than defaults?
  3. **Craft** — Typography, spacing, animations, micro-interactions?
  4. **Functionality** — Do all features actually work?
- Returns structured feedback with scores and specific issues
- Is engineered to be **ruthlessly strict** — never praises mediocre work

**Model:** Grok 4.6 High Fast (`cursor-grok-4.6-high-fast`) by default; raise via `GAN_EVALUATOR_MODEL` (set it to the model selected in this chat) for stronger judgment + tool use

## Evaluation Criteria

The default four criteria, each scored 1-10:

```markdown
## Evaluation Rubric

**Screen distinctiveness is NOT scored here.** Whether a named direction is recorded AND visibly applied on the rendered screens is judged ONLY by `browser-qa` in the visual loop (orch-build-mvp step 6) — never by this evaluator. The Design Quality and Originality rows below score the recorded direction and its code-level application only (direction recorded in `docs/design-tokens.md`; tokens, type, and spacing trace to it in the code). A screen that reads as a default template is a browser-qa finding, not a rubric deduction — do not raise or lower a score for screen distinctiveness.
**Design-decision pointer:** F2/F3/F4/F5/F6/D19/B1/X1 as relevant — design-package rule — Taste step 4a / orchestrate.

### Design Quality (weight: 0.3)
- 1-3: No named direction recorded, or tokens, type, and spacing in the code do not trace to any recorded direction
- 4-6: A direction is recorded but only partly applied in code — some tokens, type, or spacing trace to it, the rest do not
- 7-8: Direction recorded and applied in code — tokens, type, and spacing trace to it coherently across the app
- 9-10: Direction recorded and applied with professional-level craft in code — tokens, type, and spacing trace to it consistently, including edge states

### Originality (weight: 0.2)
- 1-3: Code-level choices do not trace to the recorded direction — defaults throughout, no direction-specific decisions in code
- 4-6: Some code-level choices trace to the recorded direction, most do not
- 7-8: Clear creative direction recorded and applied in code — direction-specific choices in tokens, type, and spacing throughout
- 9-10: Direction recorded and applied in code in a surprising, inventive way — direction-specific choices throughout, including details and edge states

### Craft (weight: 0.3)
- 1-3: Broken layouts, missing states, no animations
- 4-6: Works but feels rough, inconsistent spacing
- 7-8: Polished, smooth transitions, responsive
- 9-10: Pixel-perfect, delightful micro-interactions

### Functionality (weight: 0.2)
- 1-3: Core features broken or missing
- 4-6: Happy path works, edge cases fail
- 7-8: All features work, good error handling
- 9-10: Bulletproof, handles every edge case
```

### Scoring

- **Weighted score** = sum of (criterion_score * weight)
- **Pass threshold** = 7.0 (configurable)
- **Max iterations** = 15 (configurable, typically 5-15 sufficient)
- **Orchestrator check** — after each evaluator pass the orchestrator checks the generator's output against the brief's acceptance criteria (a rubric pass at or above 7.0 with a failed acceptance criterion is a fail) and re-checks the evaluator's pass/fail call; failed output goes back with a correction brief naming the failed criterion; a correction re-dispatch consumes one iteration within max iterations; the planner's spec is checked against the brief before the first generator pass

## Usage

### Via Command

```bash
# Full three-agent harness
/gan-build "Build a project management app with Kanban boards, team collaboration, and dark mode"

# With custom config
/gan-build "Build a recipe sharing platform" --max-iterations 10 --pass-threshold 7.5

# Frontend design mode (generator + evaluator only, no planner)
/gan-design "Create a landing page for a crypto portfolio tracker"
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GAN_MAX_ITERATIONS` | `15` | Maximum generator-evaluator cycles |
| `GAN_PASS_THRESHOLD` | `7.0` | Weighted score to pass (1-10) |
| `GAN_PLANNER_MODEL` | `cursor-grok-4.6-high-fast` | Model for planning agent |
| `GAN_GENERATOR_MODEL` | `cursor-grok-4.6-high-fast` | Model for generator agent |
| `GAN_EVALUATOR_MODEL` | `cursor-grok-4.6-high-fast` | Model for evaluator agent |
| `GAN_EVAL_CRITERIA` | `design,originality,craft,functionality` | Comma-separated criteria |
| `GAN_DEV_SERVER_PORT` | `3000` | Port for the live app |
| `GAN_DEV_SERVER_CMD` | `npm run dev` | Command to start dev server |
| `GAN_PROJECT_DIR` | `.` | Project working directory |
| `GAN_SKIP_PLANNER` | `false` | Skip planner, use spec directly |
| `GAN_EVAL_MODE` | `playwright` | `playwright`, `screenshot`, or `code-only` |

### Evaluation Modes

| Mode | Tools | Best For |
|------|-------|----------|
| `playwright` | Browser MCP + live interaction | Full-stack apps with UI |
| `screenshot` | Screenshot + visual analysis | Static sites, design-only |
| `code-only` | Tests + linting + build | APIs, libraries, CLI tools |

## Anti-Patterns

1. **Evaluator too lenient** — If the evaluator passes everything on iteration 1, your rubric is too generous. Tighten scoring criteria and add explicit penalties for common AI patterns (code-level direction-application failures only — never screen distinctiveness, which is judged ONLY by `browser-qa`).

2. **Generator ignoring feedback** — Ensure feedback is passed as a file, not inline. The generator should read `feedback-NNN.md` at the start of each iteration.

3. **Infinite loops** — Always set `GAN_MAX_ITERATIONS`. If the generator can't improve past a score plateau after 3 iterations, stop and flag for human review.

4. **Evaluator testing superficially** — The evaluator must use Playwright to **interact** with the live app, not just screenshot it. Click buttons, fill forms, test error states.

5. **Evaluator praising its own fixes** — Never let the evaluator suggest fixes and then evaluate those fixes. The evaluator only critiques; the generator fixes.

6. **Context exhaustion** — For long sessions, use Cursor Agent SDK's automatic compaction or reset context between major phases.

## Results: What to Expect

Based on the upstream harness paper's published results:

| Metric | Solo Agent | GAN Harness | Improvement |
|--------|-----------|-------------|-------------|
| Time | 20 min | 4-6 hours | 12-18x longer |
| Cost | $9 | $125-200 | 14-22x more |
| Quality | Barely functional | Production-ready | Phase change |
| Core features | Broken | All working | N/A |
| Design | Generic AI slop | Distinctive, polished | N/A |

**The tradeoff is clear:** ~20x more time and cost for a qualitative leap in output quality. This is for projects where quality matters.

## References

- Harness Design for Long-Running Apps (upstream multi-agent harness design paper) — Original paper by Prithvi Rajasekaran
- Epsilla: The GAN-Style Agent Loop — Architecture deconstruction
- [Martin Fowler: Harness Engineering](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html) — Broader industry context
- [OpenAI: Harness Engineering](https://openai.com/index/harness-engineering/) — OpenAI's parallel work
