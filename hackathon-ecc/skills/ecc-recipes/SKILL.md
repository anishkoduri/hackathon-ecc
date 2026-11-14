---
name: ecc-recipes
description: Map a described workflow to the right ECC command group with run-order and stop condition, or browse all command-group recipe families read live from the commands directory. Advisory only — never executes. Use when asked which commands run a workflow, the command sequence for a task, or to list ECC pipelines; not for executing the task (route to the command itself), single-command docs (read the command file in commands/ directly), or prompt rewrites (this skill does not rewrite prompts).
argument-hint: <workflow description | empty=list all>
origin: community
author: KyawZinLatt
metadata:
  version: "1.0.0"
---

# ECC Recipes

One entry point for "which group of ECC slash-commands runs my workflow, in what
order, and when do I stop." Also browses every command-group recipe family.

The `commands/` directory lists commands and where to read docs, but only as a flat catalog.

This skill adds: **family grouping + run-order + stop condition.**

## When to Activate

- "Which command group do I run for <workflow>?"
- "What's the command sequence to build an MVP / fix a defect / refactor?"
- "Show me all ECC command-group recipes" (catalog mode)
- "How many workflow pipelines does ECC have?"
- User invokes the `ecc-recipes` skill with or without a description.

### Do Not Use When

- User wants the task done now — route to the actual command, don't describe it.
- User wants deep docs for ONE command — read the command file in `commands/` directly.
- User wants a draft prompt rewritten — this skill does not rewrite prompts; do the rewrite directly in the main context.

## Core Principle

**Answer from current files, not memory.** The command set changes; never
hardcode counts or member lists. Read the live `commands/` directory each run,
then classify into families.

### Live reads

Resolve the commands directory (first that exists), then list names:

Windows (PowerShell):
```powershell
$cmdDir = $null
foreach ($D in @("$env:USERPROFILE\.cursor\plugins\local\hackathon-ecc\commands", "$env:USERPROFILE\.cursor\plugins\*\hackathon-ecc\commands", ".\commands", ".\.ecc\commands", "$env:USERPROFILE\.cursor\ecc\commands")) {
  if (Test-Path $D) { $cmdDir = $D; break }
}
if (-not $cmdDir) { Write-Error "No ECC commands directory found."; return }
Get-ChildItem $cmdDir -Filter *.md | ForEach-Object { $_.BaseName } | Sort-Object
```

macOS/Linux (bash):
```bash
for D in \
  "$HOME"/.cursor/plugins/local/hackathon-ecc/commands \
  "$HOME"/.cursor/plugins/*/hackathon-ecc/commands \
  ./commands \
  ./.ecc/commands \
  "$HOME"/.cursor/ecc/commands; do
  [ -d "$D" ] && CMD_DIR="$D" && break
done
[ -z "${CMD_DIR:-}" ] && { echo "No ECC commands directory found."; return 1; }
find "$CMD_DIR" -maxdepth 1 -name '*.md' -exec basename {} .md \; | sort
```

Optionally read `manifests/install-*.json` if present for richer grouping. Use
the smallest set of reads needed.

## Family Classification (by prefix)

Group command names by leading prefix; map known singletons by hand. Families are
derived live — the table below is the *classification rule*, not a frozen list.

| Family prefix | Recipe meaning | Typical run-order |
|---|---|---|
| `orch-*` | gated Research, Plan, TDD, Review, Commit per task type | pick one orch-* by task kind; it runs its own internal phases |
| `prp-*` | PRD to plan to implement to PR pipeline | `prp-prd` then `prp-plan` then `prp-implement` then `prp-commit` then `prp-pr` |
| `epic-*` | large multi-unit epic, parallel | `epic-decompose` then `epic-claim` then `epic-validate` then `epic-review` then `epic-unblock` then `epic-sync` then `epic-publish` |
| `loop-*` | managed autonomous loop | `loop-start <pattern>` |
| `gan-*` | generator and evaluator loop | `gan-build` (code) or `gan-design` (UI); self-looping |
| `*-build` / `*-review` / `*-test` | per-language CI triad | `<lang>-test` (TDD) then `<lang>-build` (fix) then `<lang>-review` |
| `hookify-*` | behavior-hook management | `hookify` then `hookify-list` then `hookify-configure` |
| `learn` / `instinct-*` / `evolve` / `promote` / `prune` | continuous-learning | `learn` then `instinct-status` then `evolve` then `promote` |

Any command not matching a prefix rule → list it under **singletons** with its
one-line description.

## How It Works

```
1. Live-read command names from CMD_DIR.
2. Classify into families by prefix and a singleton map.
3. If a workflow description was given -> MATCH MODE.
   If none -> CATALOG MODE.
4. Advisory only: print the plan. Never run the matched commands.
```

### Catalog mode (no description)

Output the family table: each family, member count, members, one-line meaning,
typical run-order. End with the total command count and a prompt to describe a
workflow for a matched recipe.

### Match mode (description given)

1. Restate the workflow in one sentence.
2. Pick the best 1-2 families; say WHY in one line each.
3. **Run-order block** — exact command sequence for the matched family.
4. **Stop condition** — always explicit (max-runs, completion-signal,
   review-passes, or single-shot). For autonomous loops, warn about subscription
   burn and recommend a backstop bound.
5. **Where to read** — the `commands/<name>.md` path plus `/ecc-guide <name>`.

## Output Template (match mode)

```
Workflow: <one-sentence restatement>

Best fit: <family> — <why>
(Alt: <family> — <why>)

Run-order:
  /<cmd1>   # job
  /<cmd2>   # job
  /<cmd3>   # job
  STOP when: <condition>
  WARNING (autonomous loops only): an unbounded loop burns subscription/credits —
  add a max-iteration or max-cost backstop alongside the completion signal.

Read full docs:
  commands/<cmd1>.md   (or: /ecc-guide <cmd1>)
```

## Examples

**Catalog:** invoking `ecc-recipes` prints the family table and total count.

**Match:** Ask the agent to plan a whole app upfront then auto-build with adversarial
review until done → Best fit: `loop-*` (autonomous) wrapping `gan-*` or
`loop-start rfc-dag --mode safe`; STOP when all units
pass review N consecutive times (add a max-iteration backstop to bound burn).

**Match:** Ask the agent to fix a bug in a Go service → Best fit: `orch-fix-defect`
(reproduce, fix, review, commit). Alt: `go-test` then `go-build` then
`go-review`. STOP: regression test green and review pass.

## Non-Goals

- Not an executor — advisory only.
- Not per-command deep docs — read the command file in `commands/` directly.
- Not prompt rewriting — this skill maps command groups only.
- Never hardcode command counts or member lists — always live-read.
