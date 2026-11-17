---
description: Recommend the best model tier for the current task based on complexity, risk, and budget.
---

# Model Route Command

Recommend the best model tier for the current task by complexity and budget.

## Usage

`/model-route [task-description] [--budget low|med|high]`

## Routing Heuristic

- `cursor-grok-4.6-high-fast`: deterministic, low-risk mechanical changes
- `grok-4.7-extra-high`: default for implementation and refactors
- `grok-4.7-extra-high`: architecture, deep review, ambiguous requirements

## Required Output

- recommended model
- confidence level
- why this model fits
- fallback model if first attempt fails

## Arguments

$ARGUMENTS:
- `[task-description]` optional free-text
- `--budget low|med|high` optional
