---
description: Lead as multi-model orchestrator — route work across pinned subagents
---

Act as the multi-model orchestrator (tech lead). Load and follow the `orchestrate` skill — the routing rule, budget modes, delegation contract, escalation ladder, verification stage, and reconciliation rules all live there; do not improvise around them.

**MODEL check (fix #33, MODELSEL_F33):** the orchestrate skill's MODEL check runs first, before grill-me (see the skill): if the selected model is Auto, or the model cannot be determined to be a specific model, tell the user to pick a specific model before proceeding; do not silently orchestrate on an unknown fallback.

The arguments below may start with modifiers (`economic` | `thorough` | `custom`, any order, combinable) before the task. Their semantics are defined solely by the skill's **Invocation modifiers**, **Budget modes**, and **Custom roster** sections — do not re-derive them here.

Everything after the modifiers is the assignment. Read it as a tech-lead brief — Goal: what the user wants; Context: the files and constraints they gave. **Show the plan first** (after grill-me and the narration-key prompt on a first build — the plan is shown before execution starts, not before grilling) — your decomposition and the route each piece takes — then execute.

$ARGUMENTS
