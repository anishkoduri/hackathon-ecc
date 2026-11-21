---
name: prebuild-research
description: Use when a build is about to start — after scoping, before feature expansion and design — and the pipeline needs researched fuel: feature ideas for the expansion step and framework/architecture patterns for the project type, gathered from the live web under hard caps with every source logged. Produces one compact research brief (docs/research-brief.md). Never runs mid-build; a mid-build question is a brief gap, not a research phase.
---

> **Hackathon-ecc note (fix #34, RESEARCHBRIEF_F34).** This skill is the pipeline's pre-build research step (orchestrate step 1.5): it runs AFTER `hackathon-scope` and BEFORE `feature-expansion` Phases 0–3 and the design package. It exists because expansion and direction improvised in a vacuum produce generic features and default architectures — a short, bounded look at what real products ship and what the framework's own docs prescribe gives both steps material to work with. **Caps (binding):** at most **4 web searches** and at most **4 page fetches** per run, and the output brief is at most **~600 tokens (~450 words)** — the research spends a little to save a lot; a sweep that grows past its caps has become the wandering it exists to prevent. Routing: the orchestrator runs this skill itself (the model selected in this chat) or dispatches it to `scout`; `feature-expansion` consumes the brief in Phase 0 and records taken/dropped per idea; Taste reads the pattern section before the design package and lands adopted patterns in the design contract (DESIGNCONTRACT_F34). The brief is FUEL, never authority: the grill-me decision record outranks it wherever they disagree, and the anti-derivative rule binds — ideas and patterns, never copied designs, screens, or copy. **Layer role: none — pipeline step, not a design layer** (inventory `skills/orchestrate/references/design-inventory.md` §15); it carries no trigger key — the orchestrate flow invokes it by name (the fix #31 design-skill precedent: flow-invoked, no trigger key).

# Pre-build research — fuel before expansion and design

One bounded sweep, one compact brief, then the build starts. The sweep answers two questions: what do the best shipped products in this category actually do (feature fuel), and how does this stack want a product of this type built (framework patterns)?

## 1. The sweep (bounded)

- **Feature pass (≤2 searches, ≤2 fetches).** What the strongest shipped products in the build's category do: the category + the capability words from the scope ("<category> app, key features", a named product's own launch/changelog page, a case study). Shipped behaviour only — a real product's own page or a named team's write-up, never a roundup's claim about a product.
- **Framework pass (≤2 searches, ≤2 fetches).** How the build's stack builds this project type: the framework's official docs and guides first ("<framework> <project type> architecture", the official starter/guide for the closest shape), then a named team's engineering write-up if the docs run out. The pattern carried into the brief is the one the docs prescribe, not the one a tutorial happens to show.
- **Source-quality rules (binding).** Primary sources first: official documentation, the framework's own guides, shipped products' own pages and changelogs, reputable engineering blogs with named authors. NO SEO listicle farms, content aggregators, or generated roundup sites — a source the reader could not open and check does not enter the brief. Every Feature fuel and Framework patterns line carries the source it came from; no source, no line. (Gaps lines are the exception by nature: they record what was looked for and not found — they carry the query, not a source.)
- **Stop conditions.** The caps are the first stop. The second: two consecutive queries returning nothing the brief does not already hold — diminishing returns is a stop, not a challenge. A sweep that finds nothing usable records that in the brief's Gaps and ends; the build is never blocked on research (recorded-gap fallback).
- **Processing, not browsing (fix #34).** The sweep itself is this skill's own capped model step — a script never browses (SCRIPT-GATE_F34 item 4). The mechanical work AROUND the sweep — extracting, counting, and compiling the brief's source log from what the sweep gathered — is script-first work under `code-mode` (SCRIPT-FIRST_F34) when it meets that rule's shapes: the orchestrator may gate one script to assemble the log rather than chaining the calls by hand. The brief's content (what was taken, what was dropped, and why) stays model judgment, never scripted.

## 2. The brief (`docs/research-brief.md`, ≤ ~600 tokens)

Written once per run, in exactly this shape — the shape is what keeps it compact and consumable:

```
# Research brief — <project> (<date>)
## Feature fuel (for expansion)
- <idea as a capability, one line> — source: <url> — fits because: <half line>
## Framework patterns (for design + the contract)
- <pattern, one line> — source: <url> — applies to: <the surface / flow>
## Gaps
- <what was looked for and not found, or: none>
```

- Ideas are stated as capabilities ("offline-first capture with background sync"), never as a competitor's screen to reproduce — the brief carries no screenshots, no layouts, no copy.
- A Feature fuel or Framework patterns line that cannot name its source is cut, however good it sounds — an unsourced idea is an improvisation wearing research's clothes.
- The cap is on the brief, not on the reading: read what the caps allow, then compress to the lines that would change a decision. Ten lines that change nothing are worth less than three that do.

## 3. Consumption — who does what with it

- **`feature-expansion` Phase 0 reads the brief first.** Its feature ideas enter the Phase 1 brainstorm as candidates alongside the lenses' own; the approved list's record (`docs/expansion.md`) states, per research idea, taken or dropped with a one-line reason (RESEARCHBRIEF_F34). An idea silently ignored is a gap in the record.
- **Taste reads Framework patterns before dealing the direction.** A pattern adopted lands in the design contract with its citation; a pattern considered and rejected gets its D19 line like any inventory entry.
- **Resume guard:** an existing `docs/research-brief.md` is verified and used, never re-swept (the fix #24 guard, same as scope and expansion).

## What NOT to do

- **No mid-build research.** A question that surfaces during the build is a brief gap (NEEDS_CONTEXT, NO-GUESSING_F29), not a research phase — the sweep's whole value is that it happens before commitments, when ideas are cheap.
- **No uncapped browsing.** The caps are the skill. A "quick extra search" past the cap is how research eats the build it was meant to fuel.
- **No copied designs.** A researched product's screen, layout, or words are never the design source (the anti-derivative rule) — the design package generates the direction; the brief only widens what it can consider.
- **No silent authority.** Where the brief and the decision record disagree, the record wins, and the disagreement is noted in the brief's Gaps or the expansion record — never resolved by quietly following the brief.

## Files

- Consumed by: `skills/feature-expansion/SKILL.md` (Phase 0 grounding; the taken/dropped record), `skills/design-taste-frontend/SKILL.md` (framework patterns → the design contract, DESIGNCONTRACT_F34)
- Flow position: `skills/orchestrate/SKILL.md` step 1.5 (after scope, before expansion Phases 0–3)
- Processing sibling: `skills/code-mode/SKILL.md` (SCRIPT-FIRST_F34 / SCRIPT-GATE_F34 — the sweep's downstream mechanical work; the sweep itself is never scripted)
- Pattern-research sibling: MOBBIN_RESEARCH_F22 (category + pattern consultation inside the design package) — this skill is the wider pre-build sweep (features + framework); Mobbin stays the design package's own consult
- Evidence basis: the plugin's research log (SPEC §8, R1/R4 — a research worker reads widely and returns a condensed, sourced summary; this brief is that shape, capped tighter because two downstream steps consume it)
