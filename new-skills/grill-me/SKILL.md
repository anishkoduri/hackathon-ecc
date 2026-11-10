---
name: grill-me
description: Interview the user about a hackathon project idea, one question at a time, until every material decision is recorded. Runs FIRST, right after the user sends the first project prompt and before any scoping, building, or expansion, so the automatic work that follows goes in the direction the user wants. Use when the user sends a first hackathon idea, says "grill me", or asks to be questioned about a plan or design.
---

# Grill Me

Before anything is scoped, built, or expanded, make sure the idea is actually decided. This skill asks the user one question at a time about their hackathon project until every material branch has an explicit recorded decision. The decision record it produces is what the rest of the plugin works from — scope, build, and expansion all follow it, so the product ends up going the direction the user wants instead of the direction the agent guessed.

## When to Use

- The user sends the first hackathon project prompt (an idea plus requirements). Run this skill FIRST, before `hackathon-scope`, before any building, and before any expansion skill. This is the default, not an option.
- The user says "grill me", "ask me questions", or "stress-test this idea".
- The user wants to be questioned about a plan or design before it is built.

## When NOT to Use

- The user says "skip the grilling" or "just build it" — go straight to `hackathon-scope`.
- The idea is already fully decided (the user gave a complete spec with every decision made). Skim for open branches; if there are none, say so and move on.
- Bug fixes or small changes to an existing project — that is not a first prompt.

## Workflow

1. Extract the current objective, constraints, assumptions, and already-made decisions from the user's first prompt and anything they have already said. Investigate any answer discoverable from the supplied material instead of asking the user.
2. Maintain a running decision record with: decision, chosen option, rationale, dependencies, and consequences. Update it after every answer; do not reopen a recorded decision unless new evidence conflicts with it.
3. Ask exactly one question at a time. Format the turn as `### Decision <N> — <topic>`, then `Recommended`, `Why`, `Tradeoff`, and `Question`. Choose the highest-leverage unresolved branch whose answer constrains the most downstream decisions. After each answer, acknowledge `Recorded: <choice> — <consequence>` before the next question. Show settled and currently open counts when useful; never show a percentage because the decision tree can grow.
4. Work through the branches below, but only where they are material to this project. Skip any branch that does not matter for a hackathon demo:
   - What the product is and who it is for
   - The core demo: what the judge sees in two minutes, and what the wow moment is
   - Must-have features vs. nice-to-have features (what gets cut if time runs short)
   - Data and state: what data the product needs, where it comes from, what is fake or seeded for the demo
   - Stack and platform: what it is built with, and whether it is web, mobile, or both
   - Integrations and tracks: which APIs, tools, or sponsor tracks it must use (see `integration` and `track-picker`)
   - Failure modes: what happens if the demo path breaks, the API is down, or the wifi drops
   - Time: how many hours are left, and what the stopping criteria are (when it is done enough to demo)
   - Success: what "good" looks like at demo time
   Do not ask about migration, rollout, operations, or ownership unless the user brings them up — those are not hackathon decisions.
5. When no material open branches remain, return `### Decision record` with a decision/choice/rationale/consequence table, then `### Risks`, accepted unknowns with owner/resolution point, rejected alternatives that matter, and `### Completion criteria`. Do not end with another question.

Completion requires every material branch to have a recorded decision or an explicitly accepted unknown with an owner and resolution point.

## After Grilling

The decision record is the input to everything that follows. Hand it to `hackathon-scope` (which turns it into the must-have/cut lists and the demo storyboard), and keep it available for `feature-expansion` (which expands the product in the direction the record points, not a direction it invents) and `integration` (which wires the integrations the record names). If a later skill proposes something that contradicts a recorded decision, the recorded decision wins — note the conflict instead of overriding it.

## Attribution

Adapted from grill-me by Paul Razvan Berg (MIT licensed) for hackathon-ecc. The coordination-system reference in the original was removed, the question domains were trimmed to hackathon-relevant decisions, and the trigger was set to the first project prompt.
