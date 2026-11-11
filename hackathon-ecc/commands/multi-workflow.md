---
description: Run a full multi-model development workflow with research, planning, execution, optimization, and review. (Requires external ccg-workflow runtime — not part of this plugin; Claude Code only — no Cursor equivalent in this plugin)
---

# Workflow - Multi-Model Collaborative Development

Multi-model collaborative development workflow (Research → Ideation → Plan → Execute → Optimize → Review), with intelligent routing: Frontend → Antigravity, Backend → Codex.

> **Prerequisite:** Requires the external `ccg-workflow` runtime, which is **not** part of the base ECC install. Initialize it with `npx ccg-workflow@3.7.4` to provision `~/.claude/bin/codeagent-wrapper` and the `~/.claude/.ccg/prompts/*` role files this command depends on. Without that runtime, this command will not run correctly.
> Requires the external ccg-workflow runtime (`npx ccg-workflow@3.7.4`); without it these commands cannot run.

Structured development workflow with quality gates, MCP services, and multi-model collaboration.

## Usage

```bash
/multi-workflow <task description>
```

## Context

- Task to develop: $ARGUMENTS
- Structured 6-phase workflow with quality gates
- Multi-model collaboration: Codex (backend) + Antigravity (frontend) + Claude (orchestration)
- MCP service integration (ace-tool, optional) for enhanced capabilities

## Your Role

You are the **Orchestrator**, coordinating a multi-model collaborative system (Research → Ideation → Plan → Execute → Optimize → Review). Communicate concisely and professionally for experienced developers.

**Collaborative Models**:
- **ace-tool MCP** (optional) – Code retrieval + Prompt enhancement
- **Codex** – Backend logic, algorithms, debugging (**Backend authority, trustworthy**)
- **Antigravity** – Frontend UI/UX, visual design (**Frontend expert, backend opinions for reference only**)
- **Claude (self)** – Orchestration, planning, execution, delivery

---

## Multi-Model Call Specification

**Call syntax** (parallel: run the calls concurrently; sequential: run them one at a time):

```
# New session call
Bash({
  command: "~/.claude/bin/codeagent-wrapper --backend <codex|antigravity> - \"$PWD\" <<'EOF'
ROLE_FILE: <role prompt path>
<TASK>
Requirement: <enhanced requirement (or $ARGUMENTS if not enhanced)>
Context: <project context and analysis from previous phases>
</TASK>
OUTPUT: Expected output format
EOF",
  timeout: 3600000,
  description: "Brief description"
})

# Resume session call
Bash({
  command: "~/.claude/bin/codeagent-wrapper --backend <codex|antigravity> resume <SESSION_ID> - \"$PWD\" <<'EOF'
ROLE_FILE: <role prompt path>
<TASK>
Requirement: <enhanced requirement (or $ARGUMENTS if not enhanced)>
Context: <project context and analysis from previous phases>
</TASK>
OUTPUT: Expected output format
EOF",
  timeout: 3600000,
  description: "Brief description"
})
```

**Model Parameter Notes**:
- No extra model flag is needed for `--backend antigravity` or `--backend codex`; `codeagent-wrapper` picks each backend's default model.

**Role Prompts**:

| Phase | Codex | Antigravity |
|-------|-------|--------|
| Analysis | `~/.claude/.ccg/prompts/codex/analyzer.md` | `~/.claude/.ccg/prompts/antigravity/analyzer.md` |
| Planning | `~/.claude/.ccg/prompts/codex/architect.md` | `~/.claude/.ccg/prompts/antigravity/architect.md` |
| Review | `~/.claude/.ccg/prompts/codex/reviewer.md` | `~/.claude/.ccg/prompts/antigravity/reviewer.md` |

**Session Reuse**: Each call returns `SESSION_ID: xxx`, use `resume xxx` subcommand for subsequent phases (note: `resume`, not `--resume`).

**Parallel Calls**: Start the calls in parallel and wait for their returned output. **Must wait for all models to return before proceeding to next phase**.

**Wait for Background Tasks** (use max timeout 600000ms = 10 minutes):

Wait for the subagent's returned output (block until complete, up to 10 minutes).

**IMPORTANT**:
- Must specify `timeout: 600000`, otherwise default 30 seconds will cause premature timeout.
- If still incomplete after 10 minutes, continue waiting for the subagent's returned output, **NEVER kill the process**.
- If waiting is skipped due to timeout, **ask the user in chat whether to continue waiting or kill task. Never kill directly.**

---

## Communication Guidelines

1. Start responses with mode label `[Mode: X]`, initial is `[Mode: Research]`.
2. Follow strict sequence: `Research → Ideation → Plan → Execute → Optimize → Review`.
3. Request user confirmation after each phase completion.
4. Force stop when score < 7 or user does not approve.
5. Ask the user in chat when needed (e.g., confirmation/selection/approval).

## When to Use External Orchestration

Use external tmux/worktree orchestration when the work must be split across parallel workers that need isolated git state, independent terminals, or separate build/test execution. Use in-process subagents for lightweight analysis, planning, or review where the main session remains the only writer.

Use git worktrees manually (`git worktree add <path>`) to isolate parallel workers; there is no bundled worktree orchestration script in this plugin.

---

## Execution Workflow

**Task Description**: $ARGUMENTS

### Phase 1: Research & Analysis

`[Mode: Research]` - Understand requirements and gather context:

1. **Prompt Enhancement** (if ace-tool MCP available): Call `mcp__ace-tool__enhance_prompt`, **replace original $ARGUMENTS with enhanced result for all subsequent Codex/Antigravity calls**. If unavailable, use `$ARGUMENTS` as-is.
2. **Context Retrieval** (if ace-tool MCP available): Call `mcp__ace-tool__search_context`. If unavailable, use Cursor's built-in file search, codebase search, and file reading, or spawn a Cursor subagent for deeper exploration.
3. **Requirement Completeness Score** (0-10):
   - Goal clarity (0-3), Expected outcome (0-3), Scope boundaries (0-2), Constraints (0-2)
   - ≥7: Continue | <7: Stop, ask clarifying questions

### Phase 2: Solution Ideation

`[Mode: Ideation]` - Multi-model parallel analysis:

**Parallel Calls** (run them in parallel):
- Codex: Use analyzer prompt, output technical feasibility, solutions, risks
- Antigravity: Use analyzer prompt, output UI feasibility, solutions, UX evaluation

Wait for their returned output. **Save SESSION_ID** (`CODEX_SESSION` and `ANTIGRAVITY_SESSION`).

**Follow the `IMPORTANT` instructions in `Multi-Model Call Specification` above**

Synthesize both analyses, output solution comparison (at least 2 options), wait for user selection.

### Phase 3: Detailed Planning

`[Mode: Plan]` - Multi-model collaborative planning:

**Parallel Calls** (resume session with `resume <SESSION_ID>`):
- Codex: Use architect prompt + `resume $CODEX_SESSION`, output backend architecture
- Antigravity: Use architect prompt + `resume $ANTIGRAVITY_SESSION`, output frontend architecture

Wait for their returned output.

**Follow the `IMPORTANT` instructions in `Multi-Model Call Specification` above**

**Claude Synthesis**: Adopt Codex backend plan + Antigravity frontend plan, save to `.claude/plan/task-name.md` after user approval.

### Phase 4: Implementation

`[Mode: Execute]` - Code development:

- Strictly follow approved plan
- Follow existing project code standards
- Request feedback at key milestones

### Phase 5: Code Optimization

`[Mode: Optimize]` - Multi-model parallel review:

**Parallel Calls**:
- Codex: Use reviewer prompt, focus on security, performance, error handling
- Antigravity: Use reviewer prompt, focus on accessibility, design consistency

Wait for their returned output. Integrate review feedback, execute optimization after user confirmation.

**Follow the `IMPORTANT` instructions in `Multi-Model Call Specification` above**

### Phase 6: Quality Review

`[Mode: Review]` - Final evaluation:

- Check completion against plan
- Run tests to verify functionality
- Report issues and recommendations
- Request final user confirmation

---

## Key Rules

1. Phase sequence cannot be skipped (unless user explicitly instructs)
2. External models have **zero filesystem write access**, all modifications by Claude
3. **Force stop** when score < 7 or user does not approve
