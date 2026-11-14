#!/usr/bin/env python3
"""Fix #16: re-pin all model pins to Grok and scrub Claude/Codex/Anthropic
from the hackathon-ecc Cursor plugin.

Operates on the BUILT tree (hackathon-ecc/) as the last build step, mirroring
fix #15's inline-Python-in-build.sh precedent. Usage:
    python3 fix16.py <plugin_dir>

Fail loudly: any targeted anchor that does not match exactly (count != 1)
aborts the run. Self-check at the end reports remaining banned-term hits.

Decisions D1-D19 (coordinator) govern; the tier rule is:
  opus-tier -> grok-4.7-high ; composer/sonnet/haiku-tier -> cursor-grok-4.6-high-fast
"""

import json
import os
import re
import shutil
import subprocess
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
CHANGES = []   # "relpath — description"
REMOVALS = []  # "relpath — what was removed; what is lost"
NOTES = []     # decisions / deviations to record in CHANGES.md
ERRORS = []

FAST = "cursor-grok-4.6-high-fast"
HIGH = "grok-4.7-high"


def rel(p):
    return os.path.relpath(p, BASE)


def read(f):
    with open(os.path.join(BASE, f), "r", encoding="utf-8") as fh:
        return fh.read()


def write(f, text):
    with open(os.path.join(BASE, f), "w", encoding="utf-8") as fh:
        fh.write(text)


def exists(f):
    return os.path.exists(os.path.join(BASE, f))


def sub(f, old, new, count=1):
    """Exact replacement; abort the run if the anchor does not match count times."""
    text = read(f)
    n = text.count(old)
    if n != count:
        ERRORS.append(f"{f}: anchor found {n}x, expected {count}x :: {old[:120]!r}")
        return False
    write(f, text.replace(old, new))
    CHANGES.append(f"{f} — {old[:80]!r} -> {new[:80]!r}")
    return True


def resub(f, pattern, repl, count=None, flags=0):
    text = read(f)
    new, n = re.subn(pattern, repl, text, flags=flags)
    if count is not None and n != count:
        ERRORS.append(f"{f}: regex {pattern!r} matched {n}x, expected {count}x")
        return False
    if n == 0:
        ERRORS.append(f"{f}: regex {pattern!r} matched 0x (expected >= 1)")
        return False
    write(f, new)
    CHANGES.append(f"{f} — regex {pattern!r} ({n}x)")
    return True


def sub_if_new_present(f, old, new, count=1):
    """Like sub(), but tolerates the new text already being present (the
    staged source was scrubbed in the fix-up round, so the built copy
    already carries the new text). Still ERRORS if neither old nor new is
    found — that means the anchor itself changed, which must be looked at."""
    text = read(f)
    if text.count(old) == count:
        return sub(f, old, new, count)
    if new in text:
        NOTES.append(f"{f}: already applied at staged source, skipped: {old[:80]!r}")
        return True
    ERRORS.append(f"{f}: anchor found {text.count(old)}x, expected {count}x :: {old[:120]!r}")
    return False


def resub_if_present(f, pattern, repl, count=None, flags=0):
    """Like resub(), but tolerates zero matches (the staged source was
    scrubbed in the fix-up round, so there is nothing left to remove).
    A non-zero mismatch against an explicit count is still an ERROR."""
    text = read(f)
    new, n = re.subn(pattern, repl, text, flags=flags)
    if n == 0:
        NOTES.append(f"{f}: already applied at staged source, skipped: regex {pattern!r}")
        return True
    if count is not None and n != count:
        ERRORS.append(f"{f}: regex {pattern!r} matched {n}x, expected {count}x")
        return False
    write(f, new)
    CHANGES.append(f"{f} — regex {pattern!r} ({n}x)")
    return True


def remove_array_entry_if_present(f, id_value):
    """Like remove_array_entry(), but tolerates the entry already being
    gone (the staged source was scrubbed in the fix-up round)."""
    text = read(f)
    for needle in (f'"id": "{id_value}"', f'"file": "{id_value}"'):
        if needle in text:
            return remove_array_entry(f, id_value)
    NOTES.append(f"{rel(f)}: remove_array_entry {id_value!r} already applied at staged source, skipped")
    return True


def del_file(f):
    p = os.path.join(BASE, f)
    if not os.path.exists(p):
        ERRORS.append(f"{f}: DELETE skipped — file does not exist")
        return
    os.remove(p)
    REMOVALS.append(f)


def del_dir(d):
    p = os.path.join(BASE, d)
    if not os.path.exists(p):
        ERRORS.append(f"{d}: DELETE skipped — dir does not exist")
        return
    shutil.rmtree(p)
    REMOVALS.append(d)


# ---------------------------------------------------------------- deletions
DELETE_FILES = [
    # D5 — Astra review backend (Codex delegate + wrapper script)
    "scripts/astra-review.js",
    # D6 — GAN harness shell wrapper (loop runs in Cursor via /gan-build)
    "scripts/gan-harness.sh",
    # D10 — multi-host installer: non-Cursor install targets
    "scripts/lib/install-targets/adal-project.js",
    "scripts/lib/install-targets/antigravity-project.js",
    "scripts/lib/install-targets/claude-home.js",
    "scripts/lib/install-targets/claude-project.js",
    "scripts/lib/install-targets/codebuddy-project.js",
    "scripts/lib/install-targets/codex-home.js",
    "scripts/lib/install-targets/copilot-project.js",
    "scripts/lib/install-targets/gemini-project.js",
    "scripts/lib/install-targets/hermes-home.js",
    "scripts/lib/install-targets/joycode-project.js",
    "scripts/lib/install-targets/kimi-project.js",
    "scripts/lib/install-targets/openclaw-home.js",
    "scripts/lib/install-targets/opencode-home.js",
    "scripts/lib/install-targets/qwen-home.js",
    "scripts/lib/install-targets/zed-project.js",
    # D10 — host-specific install modules
    "scripts/lib/install/antigravity-agent.js",
    "scripts/lib/install/antigravity-legacy-migration.js",
    "scripts/lib/install/antigravity-rule.js",
    "scripts/lib/install/claude-settings-lock.js",
    "scripts/lib/install/claude-settings.js",
    "scripts/lib/install/claude-skill-migration.js",
    "scripts/lib/install/codex-user-config.js",
    "scripts/lib/install/copilot-agent.js",
    "scripts/lib/install/copilot-rule.js",
    "scripts/lib/install/opencode-install-lock.js",
    "scripts/lib/install/opencode-legacy-migration.js",
    "scripts/lib/install/opencode-script-boundary.js",
    # D10 — host-specific lib modules
    "scripts/lib/claude-plugin-setup.js",
    "scripts/lib/codex-plugin-setup.js",
    "scripts/lib/codex-legacy-sync.js",
    "scripts/lib/claude-scope-migration.js",
    "scripts/lib/claude-dry-run-sandbox.js",
    "scripts/lib/claude-commit-attribution.js",
    "scripts/lib/multi-harness-setup.js",
    # D10 — session adapters for other hosts
    "scripts/lib/session-adapters/claude-history.js",
    "scripts/lib/session-adapters/codex-worktree.js",
    "scripts/lib/session-adapters/opencode.js",
    # D10 — MCP inventory readers (no Cursor reader exists)
    # (whole dir deleted below — collect.js + canonical-mcp.js are dead code
    # too: no importers anywhere in .js/.md/.json)
    # D10 — host-compat lint (validator + command)
    "scripts/ci/validate-skill-host-compat.js",
    "commands/skill-host-compat.md",
    # D14 — qwen adapter generator
    "scripts/qwen-adapt-agents.js",
    # D12 — cost tracker + LLM summary (no verified Cursor cost source; claude -p)
    "scripts/hooks/cost-tracker.js",
    "scripts/lib/llm-summary.js",
    "commands/cost-report.md",
    # D13 — observer's migration script
    "skills/continuous-learning-v2/scripts/migrate-homunculus.sh",
    # D13 follow-up — session-guardian.sh is orphaned: its only caller was
    # observer-loop.sh's gate (removed under D13); zero callers remain.
    "skills/continuous-learning-v2/agents/session-guardian.sh",
    # D16 — multi-model council / santa loop / multi-* commands (CLI-only)
    "commands/santa-loop.md",
    "commands/multi-backend.md",
    "commands/multi-plan.md",
    "commands/multi-execute.md",
    "commands/multi-frontend.md",
    "commands/multi-workflow.md",
    # Sessions cluster: no Cursor equivalent for Claude transcript scanning
    # (loop-status) — see targeted decisions in CHANGES.md.
    "commands/loop-status.md",
    # D20 — context-profile native execution (spawns codex/claude CLIs only;
    # no Cursor provider exists in the PROVIDERS table). The carrier/resolve
    # machinery in context-profile-commands.js + context-carriers.js stays.
    "scripts/lib/context-profile-native.js",
    "scripts/lib/context-profile-native-executable.js",
    "scripts/lib/context-profile-native-discovery.js",
    "scripts/lib/context-profile-interactive.js",
    "scripts/lib/context-profile-launch.js",
    # D20 — context-profile-proposal.js: selects a context skill by spawning
    # codex/claude CLIs; zero callers anywhere in the tree (dead code).
    "scripts/lib/context-profile-proposal.js",
]

DELETE_DIRS = [
    "scripts/lib/astra-review",      # D5 supporting libs (fix/prompt/scope, codex delegate)
    "skills/skill-comply",           # D13 whole skill
    "skills/council-multi-model",    # D16
    "skills/config-gc",              # round 2: GCs the ~/.claude config layout; no verified Cursor equivalent
    "scripts/lib/mcp-inventory",     # round 2: dead code, no importers
]


def do_deletes():
    for f in DELETE_FILES:
        del_file(f)
    for d in DELETE_DIRS:
        del_dir(d)

# ------------------------------------------------- targeted edits, part 1

def edit_transcript_context():
    """D7: the model->window table holds ABSOLUTE constants (200k / 1M) that
    mismatch Grok's verified windows (4.7: 256k / 500k) and 4.6's window is
    unverified — drop the model-specific table and wire the existing
    fallback/default + env override. NEVER invent a 4.6 window number."""
    f = "scripts/lib/transcript-context.js"
    sub(f, "Reads the latest assistant `usage` record from a Claude Code session",
        "Reads the latest assistant `usage` record from an agent session")
    # Drop the table comment + array + family-match helper (one block)
    text = read(f)
    m = re.search(
        r"// Known large-window model families.*?"
        r"function isKnownModelFamilyMatch\(model, familyId\) \{.*?\n\}\n",
        text, re.S)
    if not m:
        ERRORS.append(f"{f}: model-window table block not found")
    else:
        write(f, text[: m.start()] + text[m.end():])
        CHANGES.append(f"{f} — dropped KNOWN_MODEL_WINDOW_TOKENS table + isKnownModelFamilyMatch (D7)")
    # resolveContextWindow: drop the known-family lookup block
    sub(f, """  // Large-window model families without a [1m] marker fall through the checks
  // above and would be misreported against the 200k default (#2461).
  if (typeof model === 'string') {
    const known = KNOWN_MODEL_WINDOW_TOKENS.find(([familyId]) => isKnownModelFamilyMatch(model, familyId));
    if (known) {
      return { windowTokens: known[1], inferred: false };
    }
  }
""", "")
    sub(f, """  // Explicit window override wins: 400k models (e.g. Opus 4.x) match neither the
  // 200k default nor the 1M marker and would otherwise report ~double usage (#2290).""",
        """  // Explicit window override wins: a model whose window matches neither the
  // 200k default nor the 1M marker would otherwise report ~double usage (#2290).""")
    # Drop the CLAUDE_CODE_AUTO_COMPACT_WINDOW fallback block (whole block)
    sub(f, """  // Claude Code's CLAUDE_CODE_AUTO_COMPACT_WINDOW is the harness auto-compact
  // trigger point (e.g. 786432 on a 1M-window model), not the context window
  // size. Honor it only as a last-resort fallback so it cannot mask the [1m]
  // marker, known large-window families, or >200k observed tokens above.
  const autoCompactWindow = Number(env.CLAUDE_CODE_AUTO_COMPACT_WINDOW || '');
  if (Number.isSafeInteger(autoCompactWindow) && autoCompactWindow > 0) {
    return { windowTokens: autoCompactWindow, inferred: false };
  }
""", "")
    # Docstrings: drop "known large-window model family" + Opus tier example
    sub(f, """ * Detect the context window size for a turn.
 * 1M when the model id carries the `[1m]` marker, matches a known large-window
 * model family, or when the observed token count already exceeds the standard
 * 200k window (covers logs that drop the suffix); otherwise the standard 200k
 * window.""", """ * Detect the context window size for a turn.
 * 1M when the model id carries the `[1m]` marker, or when the observed token
 * count already exceeds the standard 200k window (covers logs that drop the
 * suffix); otherwise the standard 200k window.""")
    sub(f, "(e.g. a 1M-context Opus tier, where the base tier is 200k and the",
        "(e.g. a 1M-context tier, where the base tier is 200k and the")
    # resolveContextThreshold: drop the native-budget cap
    sub(f, """ * `COMPACT_CONTEXT_THRESHOLD=0` disables the context signal entirely;
 * other invalid values fall back to the window-scaled default, capped at
 * 80 percent of a valid native compaction budget when that is earlier.""",
        """ * `COMPACT_CONTEXT_THRESHOLD=0` disables the context signal entirely;
 * other invalid values fall back to the window-scaled default.""")
    sub(f, """  const defaultThreshold = windowTokens >= LARGE_CONTEXT_WINDOW_TOKENS ? DEFAULT_CONTEXT_THRESHOLD_LARGE : DEFAULT_CONTEXT_THRESHOLD_STANDARD;
  const nativeBudget = Number(env && env.CLAUDE_CODE_AUTO_COMPACT_WINDOW);
  if (!Number.isSafeInteger(nativeBudget) || nativeBudget <= 0) return defaultThreshold;
  // Keep the standard 160k/200k headroom before native compaction, without
  // changing model-capacity evidence or an explicit reminder policy above.
  const nativeThreshold = Math.max(1, Math.floor(nativeBudget * (DEFAULT_CONTEXT_THRESHOLD_STANDARD / STANDARD_CONTEXT_WINDOW_TOKENS)));
  return Math.min(defaultThreshold, nativeThreshold);""",
        """  const defaultThreshold = windowTokens >= LARGE_CONTEXT_WINDOW_TOKENS ? DEFAULT_CONTEXT_THRESHOLD_LARGE : DEFAULT_CONTEXT_THRESHOLD_STANDARD;
  return defaultThreshold;""")


def edit_agent_schema_and_emitters():
    """D8: enum ["haiku","sonnet","opus"] -> Grok slugs."""
    f = "schemas/agent.schema.json"
    sub(f, '"haiku", "sonnet", "opus"', f'"{FAST}", "{HIGH}"')
    sub(f, "Claude aliases only in v1", "Grok model slugs only in v1")
    sub(f, "agents/*.md Claude frontmatter", "agents/*.md frontmatter")
    sub(f, "Claude tool identifiers such as Read, Grep", "tool identifiers such as Read, Grep")
    sub(f, "Claude color tag", "color tag")
    f = "scripts/lib/agent-ir.js"
    sub(f, "VALID_MODELS = ['haiku', 'sonnet', 'opus']",
        f"VALID_MODELS = ['{FAST}', '{HIGH}']")
    sub(f, "(expected haiku, sonnet, or opus)",
        f"(expected {FAST} or {HIGH})")
    sub(f, "Claude frontmatter markdown", "frontmatter markdown")
    sub(f, "Claude agents use comma-separated strings",
        "Agents use comma-separated strings")
    f = "scripts/lib/agent-emit-pi.js"
    sub(f, "Claude tiers are not valid Pi model ids",
        "Grok slugs are not valid Pi model ids")
    sub(f, "# source model tier: opus", "# source model tier: grok-4.7-high")
    # Remaining "Claude" prose in the emitter header comment
    text = read(f)
    if "Claude" in text:
        text = text.replace("Claude", "Cursor")
        write(f, text)
        CHANGES.append(f"{f} — remaining 'Claude' prose -> 'Cursor'")


def edit_adapter():
    """D9: rename vendor identifiers; KEEP payload shape unchanged."""
    f = "hooks/adapter.js"
    sub(f, "transformToClaude", "transformToHookPayload", count=2)
    sub(f, "CLAUDE_SESSION_ID", "ECC_SESSION_ID")
    sub(f, "not a Claude Code-only or unwired script", "not an unwired script")
    f = "hooks/session-start.js"
    sub(f, "CLAUDE_SESSION_ID", "ECC_SESSION_ID")
    f = "hooks/stop.js"
    sub(f, "CLAUDE_SESSION_ID", "ECC_SESSION_ID")
    # D12: stop.js also calls the deleted cost-tracker hook — remove the WHOLE
    # if-block (run 1 removed only the opener line, leaving an orphaned
    # runExistingHook call + brace and a SyntaxError).
    text = read(f)
    m = re.search(
        r"[ \t]*if \(hookEnabled\('stop:cost-tracker', \[[^\]]*\]\)\) \{\n"
        r"[ \t]*runExistingHook\('cost-tracker\.js', [^;]*;\n[ \t]*\}\n", text)
    if m:
        write(f, text[: m.start()] + text[m.end():])
        CHANGES.append("hooks/stop.js — removed whole cost-tracker hook if-block (D12)")
    else:
        ERRORS.append("hooks/stop.js: cost-tracker if-block not found")


def edit_model_route_and_common_performance():
    """D2: model-route rows. common-performance effort sentence."""
    f = "commands/model-route.md"
    sub(f, "`haiku`", f"`{FAST}`")
    sub(f, "`sonnet`", f"`{HIGH}`")
    sub(f, "`opus`", f"`{HIGH}`")
    f = "rules/common-performance.mdc"
    # :30 effort-controls sentence. The build.sh NEW-side patch (edited in the
    # earlier session) may already have written the new sentence into the
    # rebuilt tree — then this is a no-op (run 1 errored on the missing anchor).
    new_sentence = "Reasoning depth is controlled by the agent model pins in agents/ (notably grok-4.7-high for deep-reasoner). Do not use effort controls — Grok takes per-vendor `reasoning_effort`, which Cursor does not expose in a pin."
    old_sentence = "Reasoning depth is controlled by the agent model pins in agents/ (notably claude-opus-5 for deep-reasoner). Do not use Claude Code effort controls (/effort, CLAUDE_CODE_EFFORT_LEVEL, MAX_THINKING_TOKENS) — they do not exist in Cursor."
    text = read(f)
    if new_sentence in text:
        NOTES.append("rules/common-performance.mdc — effort-controls sentence already rewritten by the build.sh NEW-side patch; fix16 edit skipped (no-op)")
    elif old_sentence in text:
        write(f, text.replace(old_sentence, new_sentence, 1))
        CHANGES.append("rules/common-performance.mdc — effort-controls sentence rewritten to Grok pins")
    else:
        ERRORS.append("rules/common-performance.mdc: effort-controls sentence (old or new) not found")

ASTRA_REVIEW_NEW = '''---
name: astra-review
description: "Deep, blind code review of a scoped change set by a fresh Grok deep-reasoner, followed by a fix cycle. (The Astra/Codex backend was removed in fix #16; review now runs via Grok reviewers in Cursor.)"
---

# Deep Review

> The Astra/Codex backend was removed in fix #16. Review now runs entirely in Cursor via Grok reviewers: a blind deep-reasoner pass for the review, fast-worker for fixes, deep-reasoner again for re-verification.

## Step 1: Scope

Scope the change set directly from git — no review tool needed:

```bash
git status --short
git diff --stat HEAD
git diff HEAD -- <paths>
```

Write down the scope: which files and hunks are in scope, which are out of scope, and the claim the change is making (what it is supposed to do).

## Step 2: Blind review (deep-reasoner)

Dispatch a blind review to the deep-reasoner as a **fresh subagent on Grok 4.7 High (`grok-4.7-high`)**, with no context from this conversation except the scope and the diff. The reviewer must not know who wrote the code or what the intended fix was beyond the claim:

- "Review this diff blind. For each finding: severity (blocker / major / minor), the exact file:line, what is wrong, and the concrete fix. Do not praise what works; list only findings. If a line is fine, say nothing about it."

The reviewer returns findings only — no code changes.

## Step 3: Fix cycle

- Fixes go to **fast-worker** (`cursor-grok-4.6-high-fast`) for mechanical fixes, or back to **deep-reasoner** (`grok-4.7-high`) for architectural ones.
- After fixes, run a **second blind deep-reasoner pass** over the fixed diff to re-verify (the second-pass pattern replaces any second-model peer review).
- Repeat until the second pass returns zero blockers.

## Verdict

```
Model: grok-4.7-high
Fixer: [fast-worker | deep-reasoner]
Scope: <files/hunks reviewed>
Blockers: <count>
Majors: <count>
Minors: <count>
Verdict: PASS | FAIL
```
'''


def remove_section_by_heading(f, heading_substr, must_contain=None):
    """Delete a markdown section starting at a heading line containing
    heading_substr, up to (not including) the next heading of equal-or-higher
    level. Fenced code blocks are skipped (a '# ...' comment inside a fence
    is not a heading). Returns True on success."""
    text = read(f)
    lines = text.split("\n")

    def fence_states(ls):
        in_fence = False
        states = []
        for ln in ls:
            states.append(in_fence)
            if ln.lstrip().startswith("```"):
                in_fence = not in_fence
        return states

    in_fence = fence_states(lines)
    start = None
    level = None
    for i, ln in enumerate(lines):
        if in_fence[i]:
            continue
        if heading_substr in ln and ln.lstrip().startswith("#"):
            start, level = i, len(ln) - len(ln.lstrip("#"))
            break
    if start is None:
        ERRORS.append(f"{f}: heading {heading_substr!r} not found")
        return False
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if in_fence[i]:
            continue
        ln = lines[i]
        if ln.lstrip().startswith("#"):
            lv = len(ln) - len(ln.lstrip("#"))
            if lv <= level:
                end = i
                break
    body = "\n".join(lines[start:end])
    if must_contain and must_contain not in body:
        ERRORS.append(f"{f}: section {heading_substr!r} does not contain {must_contain!r}")
        return False
    new_lines = lines[:start] + lines[end:]
    while new_lines and new_lines[start:start + 1] == [""]:
        new_lines = new_lines[:start] + new_lines[start + 1:]
    write(f, "\n".join(new_lines))
    CHANGES.append(f"{f} — removed section {heading_substr!r}")
    return True


def edit_astra_review():
    """D5: rewrite the command prose-only; the Astra review step and its
    Codex delegate are deleted (see DELETE_FILES / DELETE_DIRS)."""
    if not exists("commands/astra-review.md"):
        ERRORS.append("commands/astra-review.md: missing")
        return
    write("commands/astra-review.md", ASTRA_REVIEW_NEW)
    CHANGES.append("commands/astra-review.md — rewritten prose-only (deep-reasoner blind review; D5)")
    REMOVALS.append("commands/astra-review.md — Astra review step + Codex delegate removed; review continues via Grok reviewers (D5). Loss: Codex-backed review; the `--consent-to-openai` / `codex login` / `ECC_ASTRA_MODEL` / MCP-Codex paths are gone.")


def edit_gan_style_harness():
    """D6: rewrite claude -p invocations to the Cursor-native GAN loop; delete
    the shell-script section, the 'Via Claude Code' block, and the
    'Evolution Across Model Capabilities' section. D11: Anthropic citation
    -> host-neutral wording."""
    f = "skills/gan-style-harness/SKILL.md"
    sub(f, "Based on Anthropic's March 2026 harness design paper.",
        "Based on the upstream multi-agent harness design paper (March 2026).")
    sub(f, "(The upstream `claude -p` invocation path is Claude Code only and does not run in Cursor; in this plugin the harness loop runs in Cursor through `/gan-build` + `/gan-design` and the `ecc-gan-*` agents as Cursor subagents — the skill contributes the harness design, prompts, and rubric, never the CLI commands.)",
        "(In this plugin the harness loop runs in Cursor through `/gan-build` + `/gan-design` and the `ecc-gan-*` agents as Cursor subagents — the skill contributes the harness design, prompts, and rubric, never the CLI commands.)")
    sub(f, "> Inspired by [Anthropic's Harness Design for Long-Running Application Development](https://www.anthropic.com/engineering/harness-design-long-running-apps) (March 24, 2026)",
        "> Inspired by the upstream multi-agent harness design paper (March 24, 2026)")
    for var in ("GAN_PLANNER_MODEL", "GAN_GENERATOR_MODEL", "GAN_EVALUATOR_MODEL"):
        sub(f, f"**Model:** Sonnet by default; raise via `{var}=opus`",
            f"**Model:** Grok 4.6 High Fast (`{FAST}`) by default; raise via `{var}={HIGH}`")
        sub(f, f"| `{var}` | `sonnet` |", f"| `{var}` | `{FAST}` |")
    remove_section_by_heading(f, "Via Shell Script", must_contain="gan-harness.sh")
    remove_section_by_heading(f, "Via Claude Code", must_contain="claude -p")
    remove_section_by_heading(f, "Evolution Across Model Capabilities", must_contain="Anthropic")
    REMOVALS.append("skills/gan-style-harness/SKILL.md — 'Via Shell Script', 'Via Claude Code' and 'Evolution Across Model Capabilities' sections removed (D6). Loss: the shell wrapper and the Anthropic-model-history narrative; the loop now runs only via /gan-build + ecc-gan-* Cursor subagents.")


def edit_observer_loop():
    """D13: remove the observer's claude spawn + its process helpers/watchdog.
    The loop keeps observation collection/pruning; analysis no longer runs."""
    f = "skills/continuous-learning-v2/agents/observer-loop.sh"
    # D13 follow-up: session-guardian.sh is deleted (zero callers); drop the
    # now-dangling sibling-script reference from the SCRIPT_DIR comment.
    sub(f, "# Resolve this script's own directory so sibling scripts (session-guardian.sh)\n"
           "# and relative helpers (../scripts/instinct-cli.py) resolve correctly whether",
        "# Resolve this script's own directory so relative helpers\n"
           "# (../scripts/instinct-cli.py) resolve correctly whether")
    sub(f, "parallel Claude analysis processes", "parallel analysis processes")
    sub(f, "unset CLAUDECODE\n\n", "")
    sub(f, 'SLEEP_PID=""\nCLAUDE_PID=""\nCLAUDE_PROCESS_GROUP=0\nWATCHDOG_PID=""\n',
        'SLEEP_PID=""\n')
    # Delete the four claude-process helper functions
    for fn in ("claude_process_alive", "signal_claude_process",
               "stop_claude_process", "wait_for_claude_analysis"):
        text = read(f)
        m = re.search(rf"^{fn}\(\) \{{.*?\n\}}\n", text, re.S | re.M)
        if not m:
            ERRORS.append(f"{f}: function {fn} not found")
            continue
        write(f, text[: m.start()] + text[m.end():])
        CHANGES.append(f"{f} — deleted function {fn} (D13)")
    # Trim cleanup_analysis_resources: drop the watchdog + claude-pid blocks
    sub(f, """  if [ -n "$WATCHDOG_PID" ]; then
    kill "$WATCHDOG_PID" 2>/dev/null || true
    wait "$WATCHDOG_PID" 2>/dev/null || true
    WATCHDOG_PID=""
  fi
  if [ -n "$CLAUDE_PID" ]; then
    stop_claude_process "$CLAUDE_PID"
    CLAUDE_PID=""
  fi
""", "")
    # Stub analyze_observations: keep the entry point (callers invoke it), drop
    # the spawn/watchdog/archive body — no Cursor equivalent exists (D13).
    text = read(f)
    m = re.search(r"analyze_observations\(\) \{.*?\n\}\n\non_usr1\(\)", text, re.S)
    if not m:
        ERRORS.append(f"{f}: analyze_observations body not found for stubbing")
    else:
        stub = ("analyze_observations() {\n"
                "  # Background analysis was removed in fix #16: it spawned the\n"
                "  # `claude` CLI, which has no Cursor equivalent. Observations are\n"
                "  # retained (not archived) and the loop keeps its guards, cooldown,\n"
                "  # and instinct pruning. No reimplementation on Cursor subagents.\n"
                "  echo \"[$(date)] Background analysis disabled (fix #16): observations retained, not analyzed\" >> \"$LOG_FILE\"\n"
                "}\n\non_usr1()")
        write(f, text[: m.start()] + stub + text[m.end():])
        CHANGES.append(f"{f} — analyze_observations stubbed (D13)")
    REMOVALS.append("skills/continuous-learning-v2/agents/observer-loop.sh — claude spawn, watchdog, and process helpers removed (D13). Loss: background instinct extraction; observations accumulate unanalyzed.")


def edit_plankton():
    """D13: remove plankton's `claude -p` path only; Phase 1 (linters) +
    Phase 2 (violations JSON) + verification stay. Phase 3 is a flow-diagram
    entry, not a heading, so it is reworded line by line."""
    f = "skills/plankton-code-quality/SKILL.md"
    sub(f, "Write-time code quality enforcement using Plankton — auto-formatting, linting, and Claude-powered fixes on every file edit via hooks. Use when setting up write-time formatting, linting, or auto-fix hooks on file edits. (Claude Code only — uses PostToolUse hooks and spawns `claude -p` subprocesses; no Cursor equivalent)",
        "Write-time code quality enforcement using Plankton — auto-formatting, linting, and violation reporting on every file edit via hooks. Use when setting up write-time formatting, linting, or violation-report hooks on file edits. (Cursor only — uses PostToolUse hooks; the auto-fix subprocess was removed in fix #16, so Plankton reports violations instead of auto-fixing)")
    sub(f, "Phase 3: Delegate + Verify", "Phase 3: Report + Verify")
    sub(f, "├─ Spawns claude -p subprocess with violations JSON",
        "├─ Reports violations JSON (no auto-fix subprocess since fix #16)")
    # "Start Claude Code" is a shell comment inside a ```bash fence, not a
    # markdown heading — the fence-aware section remover correctly skipped it
    # (run 1 error). Replace the fence block: keep the linter installs, drop
    # the `claude` start line (no start command in Cursor; hooks activate via
    # the plugin).
    sub(f,
        "```bash\n# Install core dependencies\nbrew install jaq ruff uv\n\n# Install Python linters\nuv sync --all-extras\n\n# Start Claude Code — hooks activate automatically\nclaude\n```",
        "```bash\n# Install core dependencies\nbrew install jaq ruff uv\n\n# Install Python linters\nuv sync --all-extras\n\n# Hooks activate automatically via the plugin — no start command needed\n```")
    REMOVALS.append("skills/plankton-code-quality/SKILL.md — claude -p auto-fix delegation removed (D13). Loss: Claude-powered auto-fixes; Plankton now reports violations instead of auto-fixing.")


def edit_utils():
    f = "scripts/lib/utils.js"
    sub(f, """/**
 * Get the Claude config directory (alias of getAgentDataHome for backwards compatibility).
 */
function getClaudeDir() {
  return getAgentDataHome();
}


""", "")
    sub(f, "  getAgentDataHome,\n  getClaudeDir,\n", "  getAgentDataHome,\n")
    sub(f, "Log to stderr (visible to user in Claude Code)", "Log to stderr (visible to user)")
    sub(f, "Output to stdout (returned to Claude)", "Output to stdout (returned to the agent)")


def edit_agent_data_home():
    """D15: the Cursor equivalent IS verified here (~/.cursor/ecc +
    ECC_AGENT_DATA_HOME + .cursor/ecc-agent-data.json). Make Cursor the only
    default; drop the ~/.claude fallback and CLAUDE_CONFIG_DIR."""
    f = "scripts/lib/agent-data-home.js"
    sub(f, "const CLAUDE_CONFIG_DIR_ENV = 'CLAUDE_CONFIG_DIR';\n", "")
    sub(f, "const DEFAULT_CLAUDE_DIR_NAME = '.claude';\n", "")
    sub(f, """function getDefaultClaudeAgentDataHome() {
  // Launcher-owned CLAUDE_CONFIG_DIR moves the Claude trusted root with its
  // profile. Project-provided paths must still remain inside that root.
  const fromClaudeConfigDir = expandHomePath(process.env[CLAUDE_CONFIG_DIR_ENV]);
  if (fromClaudeConfigDir) return fromClaudeConfigDir;
  return path.join(getHomeDirFromEnv(), DEFAULT_CLAUDE_DIR_NAME);
}

""", "")
    sub(f, "within the default Cursor or Claude data directories.",
        "within the default Cursor data directory.")
    sub(f, """  const allowedRoots = [
    getDefaultCursorAgentDataHome(),
    getDefaultClaudeAgentDataHome(),
    // Keep ~/.claude eligible when CLAUDE_CONFIG_DIR points elsewhere.
    path.join(getHomeDirFromEnv(), DEFAULT_CLAUDE_DIR_NAME),
  ];""", """  const allowedRoots = [
    getDefaultCursorAgentDataHome(),
  ];""")
    sub(f, "    process.env.CLAUDE_PROJECT_DIR,\n", "")
    sub(f, """  if (options.preferCursorDefault === true || isCursorHookRuntime()) {
    return getDefaultCursorAgentDataHome();
  }

  return getDefaultClaudeAgentDataHome();""", """  // Cursor-only: the default agent data home is ~/.cursor/ecc.
  // (preferCursorDefault / isCursorHookRuntime are kept as accepted
  // options for callers that pass them; they no longer change the answer.)
  return getDefaultCursorAgentDataHome();""")
    sub(f, "  CLAUDE_CONFIG_DIR_ENV,\n", "")
    sub(f, "  DEFAULT_CLAUDE_DIR_NAME,\n", "")
    sub(f, "  getDefaultClaudeAgentDataHome,\n", "")
    sub(f, "which would create a circular\n * dependency and risk divergent defaults for `~/.cursor/ecc` vs `~/.claude`.",
        "which would create a circular\n * dependency and risk divergent defaults.")
    NOTES.append("agent-data-home.js: Cursor home ~/.cursor/ecc is VERIFIED in this file (getDefaultCursorAgentDataHome + ECC_AGENT_DATA_HOME + .cursor/ecc-agent-data.json), so it becomes the only default. getAgentDataHome() callers (metrics, session aliases, package manager) now resolve under ~/.cursor/ecc automatically.")


def edit_llm_summary_call_sites():
    """D12: remove llm-summary usage from session-end.js and pre-compact.js."""
    f = "scripts/hooks/session-end.js"
    resub(f, r"const \{[^}]*generateSessionSummary[^}]*\} = require\('\.\./lib/llm-summary'\);\n", "")
    text = read(f)
    m = re.search(r"function maybeGenerateLlmSummary\(transcriptPath, summary\) \{.*?\n\}\n", text, re.S)
    if not m:
        ERRORS.append(f"{f}: maybeGenerateLlmSummary not found")
    else:
        write(f, text[: m.start()] + text[m.end():])
        CHANGES.append(f"{f} — deleted maybeGenerateLlmSummary (D12)")
    sub(f,
        "const llmSummary = transcriptPath && summary && transcriptExists ? maybeGenerateLlmSummary(transcriptPath, summary) : null;",
        "const llmSummary = null; // LLM summary removed in fix #16 (no Cursor equivalent)")
    f = "scripts/hooks/pre-compact.js"
    sub(f, "const { generateSessionSummary } = require('../lib/llm-summary');\n", "")
    sub(f, """/**
 * PreCompact Hook - Save LLM-generated summary before context compaction
 *
 * Cross-platform (Windows, macOS, Linux)
 *
 * Runs before Claude compacts context. Generates a rich LLM summary of the
 * current session and writes it to the active session .tmp file so that the
 * next session start gets a high-quality summary even after lossy compaction.
 *
 * Falls back to a plain log entry when transcript_path is unavailable or the
 * LLM call fails.
 */""", """/**
 * PreCompact Hook - Log the compaction event before context compaction.
 *
 * Cross-platform (Windows, macOS, Linux)
 *
 * Runs before the agent compacts context. Logs the compaction event to the
 * active session .tmp file. (The LLM-generated summary that used to be
 * written here was removed in fix #16: it needed `claude -p` and has no
 * Cursor equivalent.)
 */""")
    # Remove the summary-generation block (from the "Generate LLM summary"
    # comment through the if/else write block) — keep the plain log + exit.
    text = read(f)
    m = re.search(r"  // Generate LLM summary right before compaction.*?\n  \}\n\n  process\.exit\(0\);\n",
                  text, re.S)
    if not m:
        ERRORS.append(f"{f}: LLM summary block not found for removal")
    else:
        write(f, text[: m.start()]
              + "  appendFile(activeSession, `\\n---\\n**[Compaction occurred at ${timeStr}]** - Context was summarized\\n`);\n"
              + "  log('[PreCompact] Compaction event logged (no LLM summary since fix #16)');\n"
              + "  process.exit(0);\n"
              + text[m.end():])
        CHANGES.append(f"{f} — removed LLM summary generation block (D12)")
    # SUMMARY_START/END markers + escapeRegExp are now unused
    for old in ("const SUMMARY_START_MARKER = '<!-- ECC:SUMMARY:START -->';\n",
                "const SUMMARY_END_MARKER = '<!-- ECC:SUMMARY:END -->';\n"):
        sub(f, old, "")
    text = read(f)
    m = re.search(r"function escapeRegExp\(value\) \{.*?\n\}\n", text, re.S)
    if m:
        write(f, text[: m.start()] + text[m.end():])
        CHANGES.append(f"{f} — removed now-unused escapeRegExp (D12)")
    REMOVALS.append("scripts/lib/llm-summary.js + call sites (D12). Loss: LLM-generated session summaries at pre-compact and session-end (and the context-low trigger that gated them); mechanical session summaries still run. scripts/hooks/cost-tracker.js + commands/cost-report.md removed with the same decision: no verified Cursor cost source exists.")

def edit_resolve_ecc_root():
    """D11: remove the legacy-migration branch (everything-claude-code).
    Cursor-only resolution: ECC_PLUGIN_ROOT env, ~/.cursor/plugins scan,
    host-agnostic selfRoot fallback."""
    f = "scripts/lib/resolve-ecc-root.js"
    sub(f, """const CURRENT_PLUGIN_SLUG = 'ecc';
// Legacy install id, kept for existing installs.
const LEGACY_PLUGIN_SLUG = 'everything-claude-code';
const CURRENT_PLUGIN_HANDLE = `${CURRENT_PLUGIN_SLUG}@${CURRENT_PLUGIN_SLUG}`;
const LEGACY_PLUGIN_HANDLE = `${LEGACY_PLUGIN_SLUG}@${LEGACY_PLUGIN_SLUG}`;
const PLUGIN_CACHE_SLUGS = [CURRENT_PLUGIN_SLUG, LEGACY_PLUGIN_SLUG];
const PLUGIN_ROOT_SEGMENTS = [
  [CURRENT_PLUGIN_SLUG],
  [CURRENT_PLUGIN_HANDLE],
  ['marketplaces', CURRENT_PLUGIN_SLUG],
  [LEGACY_PLUGIN_SLUG],
  [LEGACY_PLUGIN_HANDLE],
  ['marketplaces', LEGACY_PLUGIN_SLUG],
];""", """const CURRENT_PLUGIN_SLUG = 'ecc';
const CURRENT_PLUGIN_HANDLE = `${CURRENT_PLUGIN_SLUG}@${CURRENT_PLUGIN_SLUG}`;
const PLUGIN_ROOT_SEGMENTS = [
  [CURRENT_PLUGIN_SLUG],
  [CURRENT_PLUGIN_HANDLE],
  ['marketplaces', CURRENT_PLUGIN_SLUG],
];""")
    sub(f, 'a user\'s own ~/.claude/skills/ can',
        'a user\'s own agent data directory\'s skills/ can')
    sub(f, """ * Tries, in order:
 *   1. CLAUDE_PLUGIN_ROOT env var (set by Claude Code for hooks, or by user)
 *   2. Standard install location (~/.claude/) — when scripts exist there
 *   3. Known plugin roots under ~/.claude/plugins/ (current + legacy slugs)
 *   4. Plugin cache auto-detection — scans ~/.claude/plugins/cache/{ecc,everything-claude-code}/
 *   5. Cursor plugin install — scans ~/.cursor/plugins/ (local install
 *      first, then any two-level marketplace layout) for a directory
 *      passing the resolver's probe (Audit #8: previously only the
 *      inline resolver scanned here, so a direct require() of this
 *      module never found a Cursor install)
 *   6. Host-agnostic fallback — the plugin root relative to this file
 *      (this module lives at <plugin-root>/scripts/lib/resolve-ecc-root.js
 *      in every host, so two levels up is the plugin root; this is what
 *      finds the plugin in a Cursor install, where ~/.claude does not exist)
 *   7. Fallback to ~/.claude/ (original behaviour)""", """ * Tries, in order:
 *   1. ECC_PLUGIN_ROOT env var (set by the host for hooks, or by user)
 *   2. Cursor plugin install — scans ~/.cursor/plugins/ (local install
 *      first, then any two-level marketplace layout) for a directory
 *      passing the resolver's probe
 *   3. Host-agnostic fallback — the plugin root relative to this file
 *      (this module lives at <plugin-root>/scripts/lib/resolve-ecc-root.js,
 *      so two levels up is the plugin root)""")
    sub(f, "@param {string} [options.envRoot]  Override CLAUDE_PLUGIN_ROOT (for testing)",
        "@param {string} [options.envRoot]  Override ECC_PLUGIN_ROOT (for testing)")
    sub(f, """  const envRoot = options.envRoot !== undefined
    ? options.envRoot
    : (process.env.CLAUDE_PLUGIN_ROOT || '');""", """  const envRoot = options.envRoot !== undefined
    ? options.envRoot
    : (process.env.ECC_PLUGIN_ROOT || '');""")
    sub(f, """  const homeDir = options.homeDir || os.homedir();
  const configuredDir = options.configDir !== undefined
    ? options.configDir
    : process.env.CLAUDE_CONFIG_DIR;
  // On WSL, convert Windows paths (e.g., C:\\Users\\name\\.claude) to WSL paths
  // (/mnt/c/Users/name/.claude) so the resolver finds the correct location.
  const wslConfiguredDir = convertWindowsPathToWSL(configuredDir);
  const rawDir = typeof wslConfiguredDir === 'string' ? wslConfiguredDir.trim() : '';
  const expandedDir = rawDir === '~'
    ? homeDir
    : (rawDir.startsWith('~/') || rawDir.startsWith('~\\\\'))
      ? path.join(homeDir, rawDir.slice(2))
      : rawDir;
  const claudeDir = expandedDir ? path.resolve(expandedDir) : path.join(homeDir, '.claude');
""", """  const homeDir = options.homeDir || os.homedir();
""")
    sub(f, """  // Standard install — files are copied directly into ~/.claude/
  if (isRoot(claudeDir)) {
    return claudeDir;
  }
""", "")
    # Legacy plugin roots loop
    text = read(f)
    m = re.search(r"  // Exact legacy plugin install locations\..*?\n  \}\n\n", text, re.S)
    if not m:
        ERRORS.append(f"{f}: legacy plugin roots block not found")
    else:
        write(f, text[: m.start()] + text[m.end():])
        CHANGES.append(f"{f} — removed legacy plugin roots scan (D11)")
    # Cache scan loop
    text = read(f)
    m = re.search(r"  // Missing cache locations are independent;.*?\n  \}\n\n", text, re.S)
    if not m:
        ERRORS.append(f"{f}: cache scan block not found")
    else:
        write(f, text[: m.start()] + text[m.end():])
        CHANGES.append(f"{f} — removed plugin cache scan (D11)")
    sub(f, "  return claudeDir;\n}", "  return selfRoot;\n}")
    # convertWindowsPathToWSL lazy loader is now unused (only fed the
    # removed configuredDir block) — remove it and its WSL comment
    text = read(f)
    m = re.search(r"// Lazily loaded so this module can be required from stripped-down directories\n// \(e\.g\., temp dirs in tests that copy only resolve-ecc-root\.js \+ utils\.js\)\.\n// Falls back to identity on failure, which matches non-WSL behavior\.\nlet _convertWindowsPathToWSL = null;\nfunction convertWindowsPathToWSL\(windowsPath\) \{.*?\n\}\n", text, re.S)
    if m:
        write(f, text[: m.start()] + text[m.end():])
        CHANGES.append(f"{f} — removed now-unused convertWindowsPathToWSL loader")
    else:
        NOTES.append(f"{f}: convertWindowsPathToWSL loader block not matched (check manually)")
    # Remove the inline-WSL-conversion loader (only used by the old inline)
    text = read(f)
    m = re.search(r"// Lazily loaded so this module can be required from stripped-down directories\n// \(e\.g\., temp dirs in tests that copy only resolve-ecc-root\.js \+ utils\.js\)\.\n// Falls back to canonical inline string with identical escaping when unavailable\.\nlet _inlineWslConversion = null;\nfunction getInlineWslConversion\(\) \{.*?\n\}\n", text, re.S)
    if m:
        write(f, text[: m.start()] + text[m.end():])
        CHANGES.append(f"{f} — removed now-unused getInlineWslConversion")
    else:
        NOTES.append(f"{f}: getInlineWslConversion block not matched (check manually)")
    # Rewrite the buildInlineResolve docstring
    text = read(f)
    m = re.search(r"/\*\*\n \* Compact inline locator for embedding.*?\n \*/\n", text, re.S)
    if m:
        new_doc = (
            "/**\n"
            " * Compact inline locator for embedding in hooks.json and command .md code blocks.\n"
            " *\n"
            " * This minified form contains no spread, no nested array literals, and no\n"
            " * escaped double quotes, so it survives `node -e \"...\"` quoting on every shell.\n"
            " * When ECC_PLUGIN_ROOT is set (as the host does for plugin hooks and\n"
            " * commands) it is used directly. Otherwise the inline scans\n"
            " * ~/.cursor/plugins (local install first, then any two-level marketplace\n"
            " * layout) for a directory passing the resolver's probe, so it finds the\n"
            " * plugin in a Cursor install. Only then does it fall back to the local\n"
            " * install path. The inline runs under `node -e` with no __dirname, so it\n"
            " * cannot use the selfRoot fallback in resolveEccRoot() directly.\n"
            " *\n"
            " * Usage in commands:\n"
            " *   const _r = <paste INLINE_RESOLVE>;\n"
            " *   const sm = require(_r + '/scripts/lib/session-manager');\n"
            " */\n"
        )
        write(f, text[: m.start()] + new_doc + text[m.end():])
        CHANGES.append(f"{f} — rewrote buildInlineResolve docstring (Cursor-only)")
    else:
        NOTES.append(f"{f}: buildInlineResolve docstring not matched (check manually)")
    # Replace the buildInlineResolve function body
    text = read(f)
    m = re.search(r"function buildInlineResolve\(options = \{\}\) \{.*?\n\}\n", text, re.S)
    if not m:
        ERRORS.append(f"{f}: buildInlineResolve function not found")
    else:
        new_fn = (
            "function buildInlineResolve(options = {}) {\n"
            "  let probeArg = '';\n"
            "  if (options && options.probe) {\n"
            "    const segments = String(options.probe).split(/[\\\\/]/).filter(Boolean);\n"
            "    for (const seg of segments) {\n"
            "      if (!/^[\\w.-]+$/.test(seg)) {\n"
            "        throw new Error(`Invalid probe segment: ${seg}`);\n"
            "      }\n"
            "    }\n"
            "    probeArg = `{probe:p.join(${segments.map((s) => `'${s}'`).join(',')})}`;\n"
            "  }\n"
            "  // Cursor-only: the inline runs under `node -e` with no __dirname, so it\n"
            "  // cannot use the selfRoot fallback in resolveEccRoot() directly; instead\n"
            "  // it scans ~/.cursor/plugins (the documented local install at\n"
            "  // plugins/local/hackathon-ecc first, then any two-level marketplace\n"
            "  // layout) for a directory passing the same probe the shared resolver\n"
            "  // uses. L() delegates to the shared resolver when a candidate loads.\n"
            "  return `(function(){var p=require('path'),f=require('fs'),o=require('os');var e=process.env.ECC_PLUGIN_ROOT;if(e&&e.trim())return e.trim();function L(x){try{return require(p.join(x,'scripts','lib','resolve-ecc-root')).resolveEccRoot(${probeArg})}catch(_){return null}}function D(x){try{return f.readdirSync(x,{withFileTypes:true}).filter(function(z){return z.isDirectory()}).map(function(z){return z.name})}catch(e){if(e.code==='ENOENT')return [];throw e}}var h=o.homedir();var cp=p.join(h,'.cursor','plugins');var q=p.join(cp,'local','hackathon-ecc');var r=L(q);if(r)return r;var A=D(cp);for(var a=0;a<A.length;a++){var B=D(p.join(cp,A[a]));for(var b=0;b<B.length;b++){r=L(p.join(cp,A[a],B[b]));if(r)return r}}return q})()`;\n"
            "}\n"
        )
        write(f, text[: m.start()] + new_fn + text[m.end():])
        CHANGES.append(f"{f} — rewrote buildInlineResolve (Cursor-only inline)")
    REMOVALS.append("scripts/lib/resolve-ecc-root.js — legacy everything-claude-code migration branch removed (D11). Loss: legacy everything-claude-code installs are no longer auto-detected/migrated; resolution is ECC_PLUGIN_ROOT -> ~/.cursor/plugins scan -> selfRoot.")


def regenerate_inline_blobs():
    """Compute the new INLINE_RESOLVE (default + auto-update probe variant)
    from the rewritten resolver and replace every embedded old blob."""
    code = (
        "const m=require('./scripts/lib/resolve-ecc-root');"
        "console.log(m.INLINE_RESOLVE);"
        "console.log(m.buildInlineResolve({probe:'scripts/auto-update.js'}));"
    )
    proc = subprocess.run(["node", "-e", code], cwd=BASE,
                          capture_output=True, text=True)
    if proc.returncode != 0:
        ERRORS.append(f"inline blob regeneration failed: {proc.stderr[:500]}")
        return
    default_blob, probe_blob = proc.stdout.rstrip("\n").split("\n")
    if not default_blob.startswith("(function(){var p=require('path')"):
        ERRORS.append("inline blob regeneration: unexpected default blob shape")
        return
    blob_re = re.compile(r"\(function\(\)\{var p=require\('path'\),f=require\('fs'\),o=require\('os'\);[^\n]*\}\)\(\)")
    replaced = 0
    for root, dirs, files in os.walk(BASE):
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules")]
        for name in files:
            p = os.path.join(root, name)
            try:
                with open(p, "r", encoding="utf-8") as fh:
                    text = fh.read()
            except (UnicodeDecodeError, OSError):
                continue
            if "function(){var p=require('path')" not in text:
                continue

            def repl(m):
                return probe_blob if "auto-update" in m.group(0) else default_blob

            new_text, n = blob_re.subn(repl, text)
            if n:
                with open(p, "w", encoding="utf-8") as fh:
                    fh.write(new_text)
                replaced += n
                CHANGES.append(f"{rel(p)} — regenerated inline resolver blob ({n}x)")
    if replaced == 0:
        ERRORS.append("inline blob regeneration: no embedded blobs replaced (expected ~18)")
    else:
        CHANGES.append(f"inline resolver blobs regenerated in tree ({replaced} blobs)")

def maybe_resub(f, pattern, repl, flags=0):
    """Best-effort regex replace; logs instead of erroring when absent
    (used for installer internals whose exact text is verified by the
    self-check grep afterwards)."""
    if not exists(f):
        NOTES.append(f"{f}: not present for maybe_resub {pattern!r}")
        return False
    text = read(f)
    new, n = re.subn(pattern, repl, text, flags=flags)
    if n == 0:
        NOTES.append(f"{f}: pattern not found (verify manually): {pattern!r}")
        return False
    write(f, new)
    CHANGES.append(f"{f} — regex {pattern!r} ({n}x)")
    return True


def edit_installer():
    """D10: narrow the multi-host installer to Cursor-only."""
    # install-manifests.js: supported targets + legacy compat default
    maybe_resub("scripts/lib/install-manifests.js",
                r"SUPPORTED_INSTALL_TARGETS\s*=\s*\[[^\]]*\]",
                "SUPPORTED_INSTALL_TARGETS = ['cursor']")
    sub("scripts/lib/install-manifests.js",
        "LEGACY_COMPAT_BASE_MODULE_IDS_BY_TARGET[target || 'claude']",
        "LEGACY_COMPAT_BASE_MODULE_IDS_BY_TARGET[target || 'cursor']")
    # (opencode entries are removed as whole objects below, not by line —
    # a line regex broke the file's object literals in run 1.)
    # install-executor.js: default target + adapter id
    maybe_resub("scripts/lib/install-executor.js",
                r"adapterId:\s*'claude'", "adapterId: 'cursor'")
    maybe_resub("scripts/lib/install-executor.js",
                r"target = 'claude'", "target = 'cursor'")
    maybe_resub("scripts/lib/install-executor.js",
                r"target \|\| 'claude'", "target || 'cursor'")
    # install/apply.js: host branches
    maybe_resub("scripts/lib/install/apply.js",
                r"\['claude',\s*'claude-project'\]", "['cursor']")
    # content-transform.js: qwen frontmatter branch (D14 — generator deleted)
    # (qwen branch is removed by the round-2 content-transform rewrite —
    # a regex cut left the file syntactically broken in run 1.)
    # Remove the require of the deleted qwen adapter generator, if present
    maybe_resub("scripts/lib/install/content-transform.js",
                r"[^\n]*qwen-adapt-agents[^\n]*\n", "")
    # control-pane owner regex -> Grok-era tokens
    sub("scripts/lib/control-pane/state.js",
        r"AGENT_OWNER_RE = /(agent|claude|codex|hermes|gemini|opencode|qwen|joycode|codebuddy|\bbot\b|gpt|sonnet|opus|haiku|fable)/i",
        r"AGENT_OWNER_RE = /(agent|grok|cursor|\bbot\b)/i")


def edit_misc_targeted():
    """Small per-file targeted edits (prose + references)."""
    f = "skills/ecc-recipes/SKILL.md"
    # (multi-backend/frontend/execute/workflow lines never existed in this
    # file — those dead maybe_resubs were removed; only multi-plan + santa-loop
    # lines were real.)
    maybe_resub(f, r"[^\n]*multi-plan[^\n]*\n", "")
    maybe_resub(f, r"[^\n]*santa-loop[^\n]*\n", "")
    f = "commands/plan.md"
    sub(f, "for a dual-model (Codex/Antigravity) plan use /multi-plan",
        "for a second deep-reasoner verification pass, dispatch a fresh deep-reasoner subagent")
    f = "rules/common-git-workflow.mdc"
    sub(f, "describes Claude Code installs", "describes Cursor installs")
    f = "rules/common-hooks.mdc"
    # :19 mentions ~/.claude/settings.json as the Claude half of a sentence
    maybe_resub(f, r" \(or [^)]*\.claude/settings\.json[^)]*\)", "")
    maybe_resub(f, r"[^\n]*\.claude/settings\.json[^\n]*\n", "")
    f = "skills/strategic-compact/SKILL.md"
    sub(f, "Fable 5, Mythos 5 and newer models", "current models and newer")
    f = "skills/continuous-learning/SKILL.md"
    maybe_resub(f, r"`~/.claude/skills/learned/`", "the agent's local learned-skills directory")
    f = "skills/continuous-learning-v2/SKILL.md"
    maybe_resub(f, r"`~/.claude/skills/learned/`", "the agent's local learned-skills directory")


def edit_manifests_and_schemas():
    """Remove deleted-feature entries from install manifests; narrow host
    enums in schemas to Cursor. Descriptive strings are handled by the
    generic pass; host labels in catalogs are dropped (not relabelled —
    a false 'Cursor-only' claim would be worse than the neutral text).
    NOTE (fix #16 round 2): the structures were verified against the run-1
    tree, not the inventory summary: install-modules.json `modules` is a
    LIST of 16 dicts (each with `targets` + `paths`); pi-core.json
    `skills.exclude` is a DICT name->reason (180 entries); the
    'claude-devfleet' key lives in skills.exclude, not in skills.rename
    (rename is {'council': 'ecc-council'}); skills/claude-devfleet does
    NOT exist in the tree, so its exclude entry is deleted, not renamed."""
    deleted_path_markers = [
        "astra-review", "gan-harness", "cost-tracker", "llm-summary",
        "cost-report", "skill-comply", "council-multi-model", "santa-loop",
        "multi-backend", "multi-plan", "multi-execute", "multi-frontend",
        "multi-workflow", "skill-host-compat", "qwen-adapt",
        "validate-skill-host-compat", "install-targets/adal",
        "install-targets/antigravity", "install-targets/claude",
        "install-targets/codebuddy", "install-targets/codex",
        "install-targets/copilot", "install-targets/gemini",
        "install-targets/hermes", "install-targets/joycode",
        "install-targets/kimi", "install-targets/openclaw",
        "install-targets/opencode", "install-targets/qwen",
        "install-targets/zed", "install/antigravity", "install/claude",
        "install/codex", "install/copilot", "install/opencode",
        "claude-plugin-setup", "codex-plugin-setup", "codex-legacy-sync",
        "claude-scope-migration", "claude-dry-run-sandbox",
        "claude-commit-attribution", "multi-harness-setup",
        "session-adapters/claude", "session-adapters/codex",
        "session-adapters/opencode", "mcp-inventory/readers",
        "migrate-homunculus", "loop-status", "config-gc",
        "mcp-inventory", "context-profile-native",
        "context-profile-interactive", "context-profile-launch",
        "install/inventory",
    ]

    def path_deleted(p):
        return any(m in p for m in deleted_path_markers)

    # --- install-modules.json: modules is a LIST; targets -> ["cursor"] ---
    mf = "manifests/install-modules.json"
    if exists(mf):
        data = json.loads(read(mf))
        changed = False
        for mod in data.get("modules", []):
            if not isinstance(mod, dict):
                continue
            if mod.get("targets") != ["cursor"]:
                mod["targets"] = ["cursor"]
                changed = True
            paths = mod.get("paths", [])
            kept = [p for p in paths if not path_deleted(str(p))]
            if len(kept) != len(paths):
                mod["paths"] = kept
                changed = True
                CHANGES.append(f"{mf}:{mod.get('id')} paths trimmed "
                               f"({len(paths)} -> {len(kept)})")
        if changed:
            write(mf, json.dumps(data, indent=2) + "\n")
            CHANGES.append(f"{mf} — all module targets narrowed to ['cursor']")

    # --- pi-core.json: skills.include (list), skills.exclude (dict),
    # commands.include (list), commands.exclude (dict) ---
    mf = "manifests/pi-core.json"
    if exists(mf):
        data = json.loads(read(mf))
        changed = False
        skills = data.get("skills", {})
        inc = skills.get("include", [])
        for name in ("council-multi-model", "skill-comply", "config-gc"):
            if name in inc:
                inc.remove(name)
                changed = True
                CHANGES.append(f"{mf}:skills.include:{name} removed")
        exc = skills.get("exclude", {})
        for name in ("council-multi-model", "skill-comply", "config-gc",
                     "claude-devfleet"):
            if name in exc:
                del exc[name]
                changed = True
                CHANGES.append(f"{mf}:skills.exclude:{name} removed")
        cmds = data.get("commands", {})
        cexc = cmds.get("exclude", {})
        for name in ("multi-backend.md", "multi-execute.md",
                     "multi-frontend.md", "multi-plan.md",
                     "multi-workflow.md", "santa-loop.md", "cost-report.md",
                     "skill-host-compat.md", "loop-status.md"):
            if name in cexc:
                del cexc[name]
                changed = True
                CHANGES.append(f"{mf}:commands.exclude:{name} removed")
        if "astra-review.md" in cexc:
            cexc["astra-review.md"] = ("deep review via the deep-reasoner "
                                       "agent (Grok 4.7 High)")
            changed = True
        # Repair the run-1 generic-pass mangling "Claude-Code-only" ->
        # "Cursor-Code-only" (36x in exclude reasons): drop the prefix
        # entirely (neutral text, not a relabel). Also fix the two
        # session-data paths in the resume/save reasons.
        def strip_labels(o):
            nonlocal changed
            if isinstance(o, dict):
                for k, v in list(o.items()):
                    if isinstance(v, str):
                        nv = v.replace("Cursor-Code-only ", "")
                        nv = nv.replace(" (Cursor-Code-only)", "")
                        nv = nv.replace("~/.claude/session-data",
                                        "~/.cursor/ecc/session-data")
                        if nv != v:
                            o[k] = nv
                            changed = True
                    else:
                        strip_labels(v)
            elif isinstance(o, list):
                for item in o:
                    strip_labels(item)
        strip_labels(data)
        if changed:
            write(mf, json.dumps(data, indent=2) + "\n")
            CHANGES.append(f"{mf} — deleted-feature entries removed; "
                           f"'Cursor-Code-only' prefixes stripped; "
                           f"astra-review reason reworded to Grok review")
        REMOVALS.append("pi-core.json catalog entries for the deleted skills "
                        "(council-multi-model, skill-comply, config-gc, "
                        "claude-devfleet) and commands (multi-*, santa-loop, "
                        "cost-report, skill-host-compat, loop-status)")

    # --- provenance.schema.json:4 agent-data-home paths ---
    pf = "schemas/provenance.schema.json"
    if exists(pf):
        sub(pf, "Required in ~/.claude/skills/learned/* and ~/.claude/skills/imported/*",
            "Required in ~/.cursor/ecc/skills/learned/* and ~/.cursor/ecc/skills/imported/*")

    # Schemas: narrow host/target enums to Cursor where the enum is a host
    # list; drop update-claude-settings conditional blocks (the operation
    # kind no longer exists); an enum narrowed to empty becomes ["cursor"].
    for root, dirs, files in os.walk(os.path.join(BASE, "schemas")):
        for name in files:
            if not name.endswith(".json"):
                continue
            p = os.path.join(root, name)
            try:
                data = json.loads(open(p, encoding="utf-8").read())
            except Exception as e:
                ERRORS.append(f"{rel(p)}: JSON parse failed: {e}")
                continue
            changed = []

            def has_const(o, value):
                if isinstance(o, dict):
                    return any(has_const(v, value) for v in o.values())
                if isinstance(o, list):
                    return any(has_const(v, value) for v in o)
                return o == value

            def walk(o):
                if isinstance(o, dict):
                    for k, v in list(o.items()):
                        if k == "enum" and isinstance(v, list) and v and all(
                                isinstance(x, str) for x in v):
                            lowered = [x.lower() for x in v]
                            if any("claude" in x or "codex" in x for x in lowered):
                                if "cursor" in lowered:
                                    o[k] = ["cursor"]
                                    changed.append("enum narrowed to ['cursor']")
                                else:
                                    o[k] = [x for x in v if "claude" not in x.lower()
                                            and "codex" not in x.lower()]
                                    if not o[k]:
                                        o[k] = ["cursor"]
                                    changed.append(f"enum host entries dropped: {o[k]}")
                        elif k == "allOf" and isinstance(v, list):
                            kept = [item for item in v
                                    if not (isinstance(item, dict)
                                            and has_const(item.get("if"),
                                                          "update-claude-settings"))]
                            if len(kept) != len(v):
                                changed.append("update-claude-settings conditional removed")
                            if kept:
                                o[k] = kept
                                for item in kept:
                                    walk(item)
                            else:
                                del o[k]
                        else:
                            walk(v)
                elif isinstance(o, list):
                    for item in o:
                        walk(item)

            walk(data)
            if changed:
                with open(p, "w", encoding="utf-8") as fh:
                    fh.write(json.dumps(data, indent=2) + "\n")
                for c in changed:
                    CHANGES.append(f"{rel(p)} — schema {c}")

# ---------------------------------------------------------------- generic pass

TEXT_EXTS = {".md", ".mdc", ".js", ".json", ".py", ".sh", ".txt", ".ts",
              ".yaml", ".yml", ".html", ".css", ".mjs", ".cjs"}
PROSE_EXTS = {".md", ".mdc", ".txt", ".json"}


def iter_text_files():
    for root, dirs, files in os.walk(BASE):
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules")]
        for name in files:
            if os.path.splitext(name)[1].lower() not in TEXT_EXTS:
                continue
            p = os.path.join(root, name)
            try:
                with open(p, "r", encoding="utf-8") as fh:
                    fh.read()
            except (UnicodeDecodeError, OSError):
                continue
            yield p


def generic_pass():
    """Ordered mechanical replacements over remaining text, AFTER targeted
    edits. No generic rule for bare `codex`, `~/.claude`, `CLAUDE_CONFIG_DIR`
    or bare `claude` CLI invocations — those are per-file targeted (or the
    file was deleted); stragglers surface in the self-check.
    Round 2: `Claude-Code` (hyphenated) is replaced BEFORE the word-boundary
    `Claude` rule so it becomes `Cursor`, not `Cursor-Code` (the run-1
    mangling). `CLAUDE.md` -> `AGENTS.md` on all text files. The `.claude/`
    slash rule now runs on ALL text files (project-local artifact dirs);
    the bare `.claude` rule stays prose-only so home-path string args in
    .js (e.g. path.join(home, '.claude', ...)) are not silently rewritten
    to a guessed ~/.ecc home."""
    counts = {}
    for p in iter_text_files():
        text = open(p, "r", encoding="utf-8").read()
        orig = text
        ext = os.path.splitext(p)[1].lower()
        # Pins first
        text = text.replace("composer-2.5[fast=false]", FAST)
        text = text.replace("composer-2.5", FAST)
        text = text.replace("claude-opus-5[effort=high]", HIGH)
        text = text.replace("claude-opus-5", HIGH)
        text = re.sub(r"(?i)\bmodel:\s*opus\b", f"model: {HIGH}", text)
        text = re.sub(r"(?i)\bmodel:\s*sonnet\b", f"model: {FAST}", text)
        text = re.sub(r"(?i)\bmodel:\s*haiku\b", f"model: {FAST}", text)
        # Instruction-file rename (Cursor projects use AGENTS.md)
        text = text.replace("CLAUDE.md", "AGENTS.md")
        if ext in PROSE_EXTS:
            # Anthropic version tiers first (avoid "Grok 4.7 High 4.5-class").
            # Literal "Opus 4.x" (no digit) is covered too — without it the
            # bare Opus rule below leaves a " 4.x" residue (sweep #17 M1).
            # The pattern is Opus-specific, so it cannot match inside the
            # Grok pin names ("Grok 4.7 High" / "Grok 4.6 High Fast").
            text = re.sub(r"\bOpus 4\.(?:\d+|x)(?:-class)?", "Grok 4.7 High", text)
            text = re.sub(r"\bHaiku\b", "Grok 4.6 High Fast", text)
            text = re.sub(r"\bSonnet\b", "Grok 4.6 High Fast", text)
            text = re.sub(r"\bOpus\b", "Grok 4.7 High", text)
        # Host rename (word-boundary; excludes getClaudeDir/transformToClaude/
        # CLAUDE_* identifiers and lowercase claude-code-orchestrate).
        # Hyphenated form FIRST so "Claude-Code-only" -> "Cursor-only".
        text = text.replace("Claude Code", "Cursor")
        text = text.replace("Claude-Code", "Cursor")
        text = re.sub(r"\bClaude\b", "Cursor", text)
        if ext in PROSE_EXTS:
            text = re.sub(r"\bclaude code\b", "Cursor", text)
        # Env / identifier renames
        text = text.replace("CLAUDE_PLUGIN_ROOT", "ECC_PLUGIN_ROOT")
        text = text.replace("CLAUDE_SESSION_ID", "ECC_SESSION_ID")
        text = text.replace("transformToClaude", "transformToHookPayload")
        text = text.replace("claudeInput", "hookInput")
        text = text.replace("getClaudeDir", "getAgentDataHome")
        # Project-local .claude/ artifact dirs -> .ecc/ (NOT ~/.claude/
        # home paths: the (?<![~/\w]) guard blocks those). The slash rule
        # runs on ALL text files; the bare rule stays prose-only.
        text = re.sub(r"(?<![~/\w])\.claude/", ".ecc/", text)
        if ext in PROSE_EXTS:
            text = re.sub(r"(?<![~/\w])\.claude\b", ".ecc", text)
        if text != orig:
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(text)
            counts[rel(p)] = True
    CHANGES.append(f"generic pass — {len(counts)} files changed by mechanical rules")


# ---------------------------------------------------------------- self-check

def grep_count(pattern, flags=re.I):
    hits = []
    for p in iter_text_files():
        text = open(p, "r", encoding="utf-8").read()
        for i, ln in enumerate(text.split("\n"), 1):
            if re.search(pattern, ln, flags):
                hits.append(f"{rel(p)}:{i}: {ln.strip()[:160]}")
    return hits


def self_check():
    out = []
    banned = [r"composer-2\.5", r"claude", r"codex", r"anthropic",
              r"sonnet", r"haiku"]
    total = 0
    for pat in banned:
        hits = grep_count(pat)
        total += len(hits)
        out.append(f"BANNED {pat}: {len(hits)}")
        for h in hits[:60]:
            out.append(f"  {h}")
        if len(hits) > 60:
            out.append(f"  ... and {len(hits) - 60} more")
    opus = grep_count(r"opus")
    out.append(f"OPUS (list individually; may false-positive): {len(opus)}")
    for h in opus[:80]:
        out.append(f"  {h}")
    pin_ctx = []
    for pat in (r"gemini", r"gpt-"):
        for h in grep_count(pat):
            if re.search(r"model:|pin|Model:", h, re.I):
                pin_ctx.append(h)
    out.append(f"GEMINI/GPT- in model-pin contexts: {len(pin_ctx)}")
    for h in pin_ctx[:40]:
        out.append(f"  {h}")
    # JS syntax check
    js_bad = []
    for root, dirs, files in os.walk(BASE):
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules")]
        for name in files:
            if name.endswith(".js"):
                p = os.path.join(root, name)
                proc = subprocess.run(["node", "--check", p],
                                      capture_output=True, text=True)
                if proc.returncode != 0:
                    js_bad.append(f"{rel(p)}: {proc.stderr.strip()[:200]}")
    out.append(f"JS SYNTAX FAILURES: {len(js_bad)}")
    for h in js_bad[:20]:
        out.append(f"  {h}")
    # JSON validity
    json_bad = []
    for root, dirs, files in os.walk(BASE):
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules")]
        for name in files:
            if name.endswith(".json"):
                p = os.path.join(root, name)
                try:
                    json.loads(open(p, encoding="utf-8").read())
                except Exception as e:
                    json_bad.append(f"{rel(p)}: {e}")
    out.append(f"JSON FAILURES: {len(json_bad)}")
    for h in json_bad[:20]:
        out.append(f"  {h}")
    # Cursor install-path smoke test
    try:
        proc = subprocess.run(
            ["node", "-e",
             "const r=require('./scripts/lib/install-targets/registry');"
             "console.log(Object.keys(r).join(','));"
             "const fn=r.getInstallTargetAdapter||r.resolveInstallTarget||r.getAdapter;"
             "console.log(fn?String(fn('cursor')):'no-resolver-export');"],
            cwd=BASE, capture_output=True, text=True)
        out.append(f"INSTALL REGISTRY SMOKE: rc={proc.returncode} "
                   f"stdout={proc.stdout.strip()[:300]!r} "
                   f"stderr={proc.stderr.strip()[:300]!r}")
    except Exception as e:
        out.append(f"INSTALL REGISTRY SMOKE: exception {e}")
    # Design-lead pins must still be Grok 4.7 High
    for f in ("commands/gan-build.md", "commands/gan-design.md"):
        if exists(f):
            t = read(f)
            out.append(f"{f}: grok-4.7-high x{t.count(HIGH)}, "
                       f"claude-opus-5 x{t.count('claude-opus-5')}, "
                       f"composer-2.5 x{t.count('composer-2.5')}")
    out.append(f"TOTAL BANNED-TERM HITS: {total}")
    return "\n".join(out)


# ---------------------------------------------------------------- round 2
# (post-run-1: installer narrowing, session/state re-points, skill prose,
# D20 context-profile removal, manifest fixes)

FILE_LOCK_JS = r''''use strict';

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const INVALID_LOCK_STALE_MS = 5 * 60 * 1000;
const acquiredLockIdentities = new WeakMap();

function sameFileIdentity(left, right) {
  if (left.ino !== right.ino) {
    return false;
  }
  // Node's path-based stats can omit the Windows volume serial (`dev = 0`)
  // while fstat() on the same file handle reports it. Preserve strict device
  // checks everywhere else, including when both Windows stats report a device.
  if (process.platform === 'win32' && (!left.dev || !right.dev)) {
    return true;
  }
  return left.dev === right.dev;
}

function createFileLock(lockPath, label = 'ECC file') {
  const tempPath = `${lockPath}.create-${process.pid}-${crypto.randomBytes(8).toString('hex')}`;
  let descriptor;
  let ownedStats;
  try {
    descriptor = fs.openSync(tempPath, 'wx', 0o600);
    fs.writeFileSync(descriptor, `${JSON.stringify({
      pid: process.pid,
      startedAt: new Date().toISOString(),
    })}\n`);
    fs.fsyncSync(descriptor);
    ownedStats = fs.fstatSync(descriptor, { bigint: true });
    fs.closeSync(descriptor);
    descriptor = undefined;
    fs.linkSync(tempPath, lockPath);
  } catch (error) {
    if (descriptor !== undefined) fs.closeSync(descriptor);
    fs.rmSync(tempPath, { force: true });
    throw error;
  }
  fs.rmSync(tempPath, { force: true });

  let released = false;
  const release = () => {
    if (released) return;
    const quarantinePath = `${lockPath}.release-${process.pid}-${crypto.randomBytes(8).toString('hex')}`;
    fs.renameSync(lockPath, quarantinePath);
    const quarantinedStats = fs.lstatSync(quarantinePath, { bigint: true });
    if (!sameFileIdentity(quarantinedStats, ownedStats)) {
      if (!fs.existsSync(lockPath)) fs.renameSync(quarantinePath, lockPath);
      throw new Error(`Refusing to release a changed ${label} lock: ${lockPath}`);
    }
    released = true;
    fs.rmSync(quarantinePath, { force: true });
  };
  // Retain the identity observed through the creation descriptor. A pathname
  // sampled after publication may already refer to a replacement lock.
  acquiredLockIdentities.set(release, Object.freeze({ dev: ownedStats.dev, ino: ownedStats.ino }));
  return release;
}

function getFileLockIdentity(release) {
  const identity = acquiredLockIdentities.get(release);
  if (!identity) throw new Error('No acquired file lock identity for this release function.');
  return identity;
}

function inspectFileLock(lockPath) {
  const descriptor = fs.openSync(lockPath, fs.constants.O_RDONLY | (fs.constants.O_NOFOLLOW || 0));
  try {
    const stats = fs.fstatSync(descriptor, { bigint: true });
    const pathStats = fs.lstatSync(lockPath, { bigint: true });
    if (
      !stats.isFile()
      || pathStats.isSymbolicLink()
      || !pathStats.isFile()
      || !sameFileIdentity(stats, pathStats)
    ) {
      return { metadata: null, stats };
    }
    let metadata = null;
    try {
      metadata = JSON.parse(fs.readFileSync(descriptor, 'utf8'));
    } catch (_error) {
      // Invalid locks may be recovered only after the bounded lease below.
    }
    return { metadata, stats };
  } finally {
    fs.closeSync(descriptor);
  }
}

function processIsAlive(pid) {
  try {
    process.kill(pid, 0);
    return true;
  } catch (error) {
    return error.code !== 'ESRCH';
  }
}

function recoverFileLock(lockPath, label = 'ECC file') {
  const recoveryPath = `${lockPath}.recover`;
  try {
    fs.mkdirSync(recoveryPath, { mode: 0o700 });
  } catch (error) {
    if (error && error.code === 'EEXIST') return null;
    throw error;
  }

  const quarantinePath = `${lockPath}.stale-${process.pid}-${crypto.randomBytes(8).toString('hex')}`;
  try {
    let inspected;
    try {
      inspected = inspectFileLock(lockPath);
    } catch (error) {
      if (error && error.code === 'ENOENT') return createFileLock(lockPath, label);
      throw error;
    }
    const validOwner = Number.isSafeInteger(inspected.metadata && inspected.metadata.pid)
      && inspected.metadata.pid > 0;
    const stale = validOwner
      ? !processIsAlive(inspected.metadata.pid)
      : Date.now() - Number(inspected.stats.mtimeMs) >= INVALID_LOCK_STALE_MS;
    if (!stale) return null;

    fs.renameSync(lockPath, quarantinePath);
    const quarantinedStats = fs.lstatSync(quarantinePath, { bigint: true });
    if (!sameFileIdentity(quarantinedStats, inspected.stats)) {
      if (!fs.existsSync(lockPath)) fs.renameSync(quarantinePath, lockPath);
      return null;
    }
    fs.rmSync(quarantinePath, { force: true });
    return createFileLock(lockPath, label);
  } finally {
    fs.rmSync(recoveryPath, { recursive: true, force: true });
    fs.rmSync(quarantinePath, { force: true });
  }
}

/**
 * Acquire exclusive file access, optionally waiting for another writer.
 * A recovery guard (`.ecc.lock.recover`) is never removed by a contender: if its
 * owner crashes during recovery, inspect and remove the orphaned guard manually
 * only after confirming no ECC process is active.
 * @param {string} filePath - File protected by the lock
 * @param {object} options - Diagnostic label and bounded wait duration
 * @returns {Function} Release callback for the acquired lock
 */
function acquireFileLock(filePath, { label = 'ECC file', timeoutMs = 0 } = {}) {
  if (!Number.isFinite(timeoutMs) || timeoutMs < 0) {
    throw new TypeError('Lock timeoutMs must be a finite non-negative number.');
  }
  const lockPath = `${filePath}.ecc.lock`;
  const deadline = performance.now() + timeoutMs;
  const sleeper = new Int32Array(new SharedArrayBuffer(4));
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  while (true) {
    try {
      return createFileLock(lockPath, label);
    } catch (error) {
      if (!error || error.code !== 'EEXIST') throw error;
    }
    try {
      const recovered = recoverFileLock(lockPath, label);
      if (recovered) return recovered;
    } catch (error) {
      // A different writer can acquire or release between inspection and recovery.
      if (!error || (error.code !== 'EEXIST' && !(timeoutMs > 0 && error.code === 'ENOENT'))) throw error;
    }
    const remaining = deadline - performance.now();
    if (remaining <= 0) {
      throw new Error(
        `Another ECC process is updating ${label}: ${filePath}. `
        + `If no ECC process is active, inspect and remove ${lockPath}.`
      );
    }
    Atomics.wait(sleeper, 0, 0, Math.min(10, remaining));
  }
}

function runWithFileLock(filePath, callback) {
  const releaseLock = acquireFileLock(filePath);
  let primaryError = null;
  let result;
  try {
    result = callback();
  } catch (error) {
    primaryError = error;
  }

  let releaseError = null;
  try {
    releaseLock();
  } catch (error) {
    releaseError = error;
  }

  if (primaryError) {
    if (releaseError) primaryError.releaseError = releaseError;
    throw primaryError;
  }
  if (releaseError) throw releaseError;
  return result;
}

module.exports = {
  acquireFileLock,
  getFileLockIdentity,
  runWithFileLock,
  sameFileIdentity,
};
'''


def _scan_string(text, i):
    """If text[i] opens a string (' \" `), return the index just past its
    close, else return i. Handles backslash escapes. A template literal's
    ${...} interpolations are skipped as code (their braces balance within
    themselves, and nested strings/templates inside them are handled
    recursively), so the caller never mistakes the interpolation's closing
    backtick for a new opening quote."""
    q = text[i]
    if q not in ("'", '"', "`"):
        return i
    i += 1
    while i < len(text):
        ch = text[i]
        if ch == "\\":
            i += 2
            continue
        if q == "`" and ch == "$" and i + 1 < len(text) and text[i + 1] == "{":
            # Skip the interpolation: brace-match from its '{', string-aware.
            depth = 0
            j = i + 1
            while j < len(text):
                c2 = text[j]
                if c2 in ("'", '"', "`"):
                    j2 = _scan_string(text, j)
                    j = j2 if j2 > j else j + 1
                    continue
                if c2 == "{":
                    depth += 1
                elif c2 == "}":
                    depth -= 1
                    if depth == 0:
                        break
                j += 1
            i = j + 1  # just past the interpolation's closing '}'
            continue
        if ch == q:
            return i + 1
        i += 1
    return i


def _brace_match_end(text, brace):
    """Return the index just past the `}` matching the `{` at brace,
    or -1 if unbalanced. String-aware (braces inside '...' "..." `...`
    do not count)."""
    depth = 0
    i = brace
    while i < len(text):
        ch = text[i]
        if ch in ("'", '"', "`"):
            j = _scan_string(text, i)
            if j == i:
                i += 1
            else:
                # Inside a template literal we stopped at ${ (or the end);
                # if we stopped at ${, treat it as code from there.
                if text[i] == "`" and j < len(text) and text[j] == "$":
                    i = j
                    continue
                i = j
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return -1


def _paren_match_end(text, paren):
    """Return the index just past the `)` matching the `(` at paren,
    string-aware; -1 if unbalanced."""
    depth = 0
    i = paren
    while i < len(text):
        ch = text[i]
        if ch in ("'", '"', "`"):
            j = _scan_string(text, i)
            if j == i:
                i += 1
            else:
                if text[i] == "`" and j < len(text) and text[j] == "$":
                    i = j
                    continue
                i = j
            continue
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return -1


def _function_span(text, name):
    """Return (start, end) of a top-level `function name(...) {...}`,
    or None. The parameter list is skipped by paren matching, so
    default values like `options = {}` do not end the span early."""
    m = re.search(rf"^function {re.escape(name)}\(", text, re.M)
    if not m:
        return None
    start = m.start()
    # NOTE: the regex consumed the `(` (m.end() is past it), so the
    # parameter-list paren is at m.end() - 1 — do NOT search for the
    # next `(` (that would be the first `if (` in the body).
    paren = m.end() - 1
    close = _paren_match_end(text, paren)
    if close < 0:
        return None
    brace = text.index("{", close)
    end = _brace_match_end(text, brace)
    if end < 0:
        return None
    return (start, end)


def remove_function(f, name):
    """Delete a top-level `function name(...) { ... }` by brace matching.
    Parameter-list braces (e.g. `options = {}`) are skipped, and braces
    inside strings do not count. node --check verifies the result."""
    text = read(f)
    span = _function_span(text, name)
    if span is None:
        ERRORS.append(f"{f}: function {name} not found")
        return False
    start, end = span
    while end < len(text) and text[end] == "\n":
        end += 1
    write(f, text[:start] + text[end:])
    CHANGES.append(f"{f} — deleted function {name}")
    return True


def replace_function(f, name, new_text):
    """Replace a top-level function with new_text (same position)."""
    text = read(f)
    span = _function_span(text, name)
    if span is None:
        ERRORS.append(f"{f}: function {name} not found")
        return False
    start, end = span
    while end < len(text) and text[end] == "\n":
        end += 1
    write(f, text[:start] + new_text.rstrip("\n") + "\n\n" + text[end:])
    CHANGES.append(f"{f} — replaced function {name}")
    return True


def edit_installer_round2():
    """D10/D12/D13/D14/D15: finish the installer narrowing run 1 left open.
    Every removed require pointed at a file deleted in run 1 (load-time
    breakers); every removed function/branch is host-specific or dead for a
    Cursor-only plan. Losses are recorded in REMOVALS."""
    # --- install-manifests.js: legacy compat map + default profile/exclusions
    f = "scripts/lib/install-manifests.js"
    resub(f,
          r"const LEGACY_COMPAT_BASE_MODULE_IDS_BY_TARGET = Object\.freeze\(\{.*?\n\}\);",
          "const LEGACY_COMPAT_BASE_MODULE_IDS_BY_TARGET = Object.freeze({\n"
          "  cursor: [\n"
          "    'rules-core',\n"
          "    'agents-core',\n"
          "    'commands-core',\n"
          "    'hooks-runtime',\n"
          "    'platform-configs',\n"
          "    'workflow-quality',\n"
          "  ],\n"
          "});",
          count=1, flags=re.S)
    sub(f, "const TARGET_DEFAULT_PROFILE_IDS = Object.freeze({\n  opencode: 'opencode',\n});\n", "")
    sub(f, "const TARGET_DEFAULT_EXCLUSIONS = Object.freeze({\n  opencode: [\n    {\n      moduleId: 'hooks-runtime',\n      reason: 'OpenCode defaults intentionally exclude hooks-runtime until users opt in.',\n      optInCommand: './install.sh --target opencode --modules hooks-runtime',\n    },\n  ],\n});\n", "")
    replace_function(f, "getTargetDefaultProfileId",
                     "function getTargetDefaultProfileId(target, manifests) {\n"
                     "  // fix #16 (D10): the only default profile was for OpenCode;\n"
                     "  // Cursor installs have no default profile.\n"
                     "  return null;\n"
                     "}")
    replace_function(f, "getTargetDefaultExclusions",
                     "function getTargetDefaultExclusions(target, manifests) {\n"
                     "  // fix #16 (D10): the only default exclusion was for OpenCode;\n"
                     "  // Cursor installs have no default exclusion.\n"
                     "  return [];\n"
                     "}")
    sub(f, "|| LEGACY_COMPAT_BASE_MODULE_IDS_BY_TARGET.claude;",
        "|| LEGACY_COMPAT_BASE_MODULE_IDS_BY_TARGET.cursor;")
    sub(f, "    ...(target === 'antigravity'\n"
            "      ? []\n"
            "      : canonicalLegacyLanguages.flatMap(language => LEGACY_LANGUAGE_EXTRA_MODULE_IDS[language] || [])),",
        "    ...canonicalLegacyLanguages.flatMap(language => LEGACY_LANGUAGE_EXTRA_MODULE_IDS[language] || []),")
    # --- install-executor.js: legacy installers -> cursor only
    f = "scripts/lib/install-executor.js"
    resub(f, r"CLAUDE_ECC_NAMESPACE", "ECC_NAMESPACE", count=2)
    resub(f, r"planClaudeStyleLegacyInstall", "planCursorStyleLegacyInstall", count=3)
    resub(f, r"'legacy-claude-rules'", "'legacy-cursor-rules'", count=3)
    remove_function(f, "planClaudeLegacyInstall")
    remove_function(f, "planClaudeProjectLegacyInstall")
    remove_function(f, "planAntigravityLegacyInstall")
    sub(f, "    claudeRulesDir: options.claudeRulesDir || process.env.CLAUDE_RULES_DIR || null",
        "    cursorRulesDir: options.cursorRulesDir || process.env.CURSOR_RULES_DIR || null")
    sub(f, "  let plan;\n"
            "  if (target === 'claude') {\n"
            "    plan = planClaudeLegacyInstall(context);\n"
            "  } else if (target === 'claude-project') {\n"
            "    plan = planClaudeProjectLegacyInstall(context);\n"
            "  } else if (target === 'cursor') {\n"
            "    plan = planCursorLegacyInstall(context);\n"
            "  } else {\n"
            "    plan = planAntigravityLegacyInstall(context);\n"
            "  }",
        "  let plan;\n"
        "  if (target === 'cursor') {\n"
        "    plan = planCursorLegacyInstall(context);\n"
        "  } else {\n"
        "    throw new Error(`Unknown legacy install target: ${target}`);\n"
        "  }")
    # --- install-targets/registry.js: cursor adapter only
    f = "scripts/lib/install-targets/registry.js"
    write(f, """const cursorProject = require('./cursor-project');
const { resolveInvocationEnvironment } = require('../invocation-environment');

// fix #16 (D10): the installer is Cursor-only. All other host adapters were
// deleted with their install-target files.
const ADAPTERS = Object.freeze([
  cursorProject,
]);

function listInstallTargetAdapters() {
  return ADAPTERS.slice();
}

function getInstallTargetAdapter(targetOrAdapterId) {
  const adapter = ADAPTERS.find(candidate => candidate.supports(targetOrAdapterId));

  if (!adapter) {
    throw new Error(`Unknown install target adapter: ${targetOrAdapterId}`);
  }

  return adapter;
}

function planInstallTargetScaffold(options = {}) {
  const adapter = getInstallTargetAdapter(options.target);
  const modules = Array.isArray(options.modules) ? options.modules : [];
  const exemptValidationCodes = new Set(Array.isArray(options.exemptValidationCodes) ? options.exemptValidationCodes : []);
  const planningInput = {
    repoRoot: options.repoRoot,
    projectRoot: options.projectRoot || options.repoRoot,
    homeDir: options.homeDir,
    env: resolveInvocationEnvironment(options),
  };
  const validationIssues = adapter.validate(planningInput);
  const blockingIssues = validationIssues.filter(issue => (
    issue.severity === 'error' && !exemptValidationCodes.has(issue.code)
  ));
  if (blockingIssues.length > 0) {
    throw new Error(blockingIssues.map(issue => issue.message).join('; '));
  }
  const targetRoot = adapter.resolveRoot(planningInput);
  const installStatePath = adapter.getInstallStatePath(planningInput);
  const operations = adapter.planOperations({
    ...planningInput,
    modules,
  });

  return {
    adapter: {
      id: adapter.id,
      target: adapter.target,
      kind: adapter.kind,
    },
    targetRoot,
    installStatePath,
    validationIssues,
    operations,
  };
}

module.exports = {
  getInstallTargetAdapter,
  listInstallTargetAdapters,
  planInstallTargetScaffold,
};
""")
    CHANGES.append("scripts/lib/install-targets/registry.js — rewritten Cursor-only (D10)")
    # --- install/content-transform.js: passthrough (all host transforms gone)
    f = "scripts/lib/install/content-transform.js"
    write(f, """'use strict';

// fix #16 (D10/D14): the installer is Cursor-only. All host-specific content
// transforms (Claude manual-plugin namespace, Qwen/Antigravity/Copilot
// frontmatter, OpenCode hook disabling) are removed with their host adapters.
// No Cursor plan names a transform, so this is a passthrough that fails
// loudly on any named transform instead of silently passing it through.
function transformInstallContent(operation, content) {
  if (!operation.contentTransform) {
    return content;
  }
  throw new Error(`Unknown install content transform: ${operation.contentTransform}`);
}

module.exports = { transformInstallContent };
""")
    CHANGES.append("scripts/lib/install/content-transform.js — rewritten as passthrough (D10/D14)")
    REMOVALS.append("install/content-transform.js host branches removed (D10/D14). Loss: Claude manual-plugin namespace projection, Qwen/Antigravity/Copilot frontmatter adaptation, OpenCode hook disabling — all host-specific, unused by Cursor plans.")
    # --- install/request.js: legacy targets -> cursor
    f = "scripts/lib/install/request.js"
    sub(f, "const LEGACY_INSTALL_TARGETS = ['claude', 'claude-project', 'cursor', 'antigravity'];",
        "const LEGACY_INSTALL_TARGETS = ['cursor'];")
    sub(f, "const target = options.target || config?.target || 'claude';",
        "const target = options.target || config?.target || 'cursor';")
    sub(f, "const supportsLocale = target === 'claude' || target === 'claude-project';",
        "const supportsLocale = target === 'cursor';")
    sub(f, "throw new Error('--locale can only be used with --target claude or --target claude-project');",
        "throw new Error('--locale can only be used with --target cursor');")
    # --- install/runtime.js: claudeRulesDir -> cursorRulesDir
    f = "scripts/lib/install/runtime.js"
    resub(f, r"claudeRulesDir", "cursorRulesDir", count=4)
    # --- install/plan.js: claude-settings + antigravity + namespace branch
    f = "scripts/lib/install/plan.js"
    sub(f, "const {\n  materializeManagedHooks,\n} = require('./claude-settings');\n", "")
    remove_function(f, "materializeClaudeSettingsOperation")
    sub(f, "function materializeScaffoldOperation(sourceRoot, operation) {\n"
            "  if (operation.kind === 'update-claude-settings') {\n"
            "    return materializeClaudeSettingsOperation(sourceRoot, operation);\n"
            "  }\n",
        "function materializeScaffoldOperation(sourceRoot, operation) {\n")
    sub(f, "  const applicableTransform = (contentTransform === 'copilot-workflow-paths'\n"
            "    || contentTransform === 'copilot-agent-frontmatter'\n"
            "    || contentTransform === 'antigravity-agent-frontmatter'\n"
            "    || contentTransform === 'qwen-agent-frontmatter')\n"
            "    && !/\\.md$/i.test(sourceRelativePath) ? undefined : contentTransform;",
        "  // Cursor-only: no host frontmatter/workflow transform applies.\n"
        "  const applicableTransform = contentTransform;")
    sub(f, "  const target = options.target || 'claude';",
        "  const target = options.target || 'cursor';")
    sub(f, "    // Persist this projection so install, doctor and repair compare the same\n"
            "    // native component names rather than restoring plugin-only references.\n"
            "    if (['claude', 'claude-project'].includes(target)\n"
            "      && operation.kind === 'copy-file'\n"
            "      && /\\.(md|mdx|markdown)$/i.test(operation.destinationPath)\n"
            "      && !operation.contentTransform) {\n"
            "      return { ...operation, contentTransform: 'claude-manual-plugin-namespace' };\n"
            "    }\n"
            "    return operation;",
        "    // Cursor-only: operations pass through unchanged (no host projection).\n"
        "    return operation;")
    remove_function(f, "isSelectedAntigravityLegacyRule")
    sub(f, "  const operations = dedupeCopyFileOperations(\n"
            "    options.legacyMode && target === 'antigravity'\n"
            "      ? materializedOperations.filter(operation => (\n"
            "        isSelectedAntigravityLegacyRule(operation, ruleLanguages)\n"
            "      ))\n"
            "      : materializedOperations\n"
            "  );",
        "  const operations = dedupeCopyFileOperations(materializedOperations);")
    sub(f, "  // of them target the same path (e.g. a generic `commands/<name>.md` shadowed\n"
            "  // by an OpenCode `.opencode/commands/<name>.md` override) only the last one",
        "  // of them target the same path (e.g. a generic `commands/<name>.md` shadowed\n"
        "  // by a later override) only the last one")
    # --- install-state.js: claude-settings require + validation block
    f = "scripts/lib/install-state.js"
    sub(f, "const {\n  CLAUDE_HOOKS_CONFIG_PATH,\n  getClaudeSettingsPath,\n  validateRecordedManagedHooks,\n} = require('./install/claude-settings');\n", "")
    text = read(f)
    m = re.search(r"        if \(operation\.kind === 'update-claude-settings'\) \{.*?\n        \}\n", text, re.S)
    if not m:
        ERRORS.append("scripts/lib/install-state.js: update-claude-settings validation block not found")
    else:
        write(f, text[: m.start()] + text[m.end():])
        CHANGES.append("scripts/lib/install-state.js — removed update-claude-settings validation block")
    # validateRecordedManagedHooks use at :244 (inside the same validator) —
    # the remaining call site validates recorded managed hooks; replace with a
    # no-op check is wrong, so check whether it is still reachable:
    text = read(f)
    if "validateRecordedManagedHooks" in text:
        NOTES.append("scripts/lib/install-state.js: validateRecordedManagedHooks still referenced after the claude-settings require removal — check the remaining call site")
    # --- install/hook-consent.js: update-claude-settings kind branch
    f = "scripts/lib/install/hook-consent.js"
    sub(f, "    operation.kind === 'update-claude-settings'\n    || operation.moduleId === HOOK_RUNTIME_MODULE_ID",
        "    operation.moduleId === HOOK_RUNTIME_MODULE_ID")
    # --- install/ownership-guard.js: codex user-config require + uses
    f = "scripts/lib/install/ownership-guard.js"
    sub(f, "const { hasEditedCodexUserConfig } = require('./codex-user-config');\n", "")
    sub(f, "    const editedConfig = previousOperation\n      && hasEditedCodexUserConfig(plan, operation, previousOperation);",
        "    const editedConfig = false;")
    sub(f, "  const previousOperation = migration.previousManagedOperations.get(comparablePath(operation.destinationPath));\n"
            "  if (plan && hasEditedCodexUserConfig(plan, operation, previousOperation)) {\n"
            "    throw new Error(`Refusing to overwrite user configuration changed after planning: ${operation.destinationPath}. Rerun to preserve it.`);\n"
            "  }\n",
        "  const previousOperation = migration.previousManagedOperations.get(comparablePath(operation.destinationPath));\n")
    REMOVALS.append("install/ownership-guard.js codex-user-config guard removed (D10). Loss: refusing to overwrite a user-edited Codex user config during install/repair (no Codex config exists in a Cursor-only install).")
    # --- install/guarded-write.js: local sameFileIdentity (D10)
    f = "scripts/lib/install/guarded-write.js"
    sub(f, "const { sameFileIdentity } = require('./claude-settings-lock');\n",
        "// fix #16 (D10): the file-identity check lived in the deleted\n"
        "// claude-settings-lock module; it is a generic dev+ino comparison.\n"
        "function sameFileIdentity(left, right) {\n"
        "  if (left.ino !== right.ino) {\n"
        "    return false;\n"
        "  }\n"
        "  if (process.platform === 'win32' && (!left.dev || !right.dev)) {\n"
        "    return true;\n"
        "  }\n"
        "  return left.dev === right.dev;\n"
        "}\n")
    # --- install/contained-fs.js: claude-settings destination guard
    f = "scripts/lib/install/contained-fs.js"
    sub(f, "const { assertClaudeSettingsPath } = require('./claude-settings');\n", "")
    remove_function(f, "assertClaudeSettingsDestination")
    sub(f, "  assertClaudeSettingsDestination,\n", "")
    # --- install-targets/helpers.js: claude-settings import + hook ops
    f = "scripts/lib/install-targets/helpers.js"
    text = read(f)
    if "claude-settings" in text:
        resub(f, r"const \{\n  CLAUDE_HOOKS_CONFIG_PATH,\n  getClaudeSettingsPath,\n\} = require\('\.\./install/claude-settings'\);\n", "", count=1)
    remove_function(f, "planClaudeHooksOperations")
    # --- install/plugin-namespace.js + excluded-paths comment
    f = "scripts/lib/install/plugin-namespace.js"
    maybe_resub(f, r"\(install-apply --target claude\|claude-project\)",
                "(install-apply --target cursor)")
    f = "scripts/lib/install/excluded-paths-reconciliation.js"
    maybe_resub(f, r"and Codex home targets\)", "targets)")
    # --- session-aliases.js: settings lock -> file lock; default path
    f = "scripts/lib/session-aliases.js"
    sub(f, "const { acquireSettingsLock } = require('./install/claude-settings-lock');",
        "const { acquireFileLock } = require('./install/file-lock');")
    sub(f, "    release = acquireSettingsLock(aliasesPath, { label: 'session aliases', timeoutMs: 5000 });",
        "    release = acquireFileLock(aliasesPath, { label: 'session aliases', timeoutMs: 5000 });")
    sub(f, "Manages session aliases stored in $ECC_AGENT_DATA_HOME/session-aliases.json (default ~/.claude).",
        "Manages session aliases stored in $ECC_AGENT_DATA_HOME/session-aliases.json (default ~/.cursor/ecc).")
    # --- scripts/lib/install/inventory.js: dead code, no callers anywhere
    del_file("scripts/lib/install/inventory.js")
    REMOVALS.append("scripts/lib/install/inventory.js deleted (round 2). Loss: the manual/managed Claude install discovery helpers (findManualClaudePlugin / findManagedClaudeInstalls / resolveClaudePaths) — nothing in the plugin called them; the Cursor install is discovered via the plugin root, not a Claude config dir.")
    # --- scripts/lib/install/file-lock.js: host-neutral file lock (new file)
    # The deleted claude-settings-lock module was a generic file lock + dev/ino
    # identity check, used by two surviving callers (session-aliases.js lock,
    # guarded-write.js identity check). Recreate it under a neutral name with
    # the same logic (labels reworded; lock suffix `.ecc.lock` unchanged).
    write("scripts/lib/install/file-lock.js", FILE_LOCK_JS)
    CHANGES.append("scripts/lib/install/file-lock.js — created (host-neutral file lock, from the deleted claude-settings-lock logic)")
    # --- install/apply.js: the deep surgery (D10/D12/D13)
    f = "scripts/lib/install/apply.js"
    sub(f, "const {\n  hasExplicitCommitAttributionPreference,\n  withCommitAttributionDisabled,\n} = require('../claude-commit-attribution');\n", "")
    sub(f, "const {\n  getClaudeSettingsPath,\n  mergeManagedHooks,\n  readSettings,\n  runWithSettingsLock,\n  uninstallManagedHooks,\n  updateSettingsAtomic,\n  validateManagedHooks,\n  validateRecordedManagedHooks,\n} = require('./claude-settings');\n", "")
    sub(f, "const {\n  assertSafeClaudeSkillOperation,\n  prepareClaudeSkillMigration,\n  removeLegacyClaudeSkillFiles,\n} = require('./claude-skill-migration');\n", "")
    sub(f, "const { cleanupLegacyAntigravityInstall } = require('./antigravity-legacy-migration');\n", "")
    sub(f, "const { cleanupLegacyOpencodeInstall, getLegacyLocationForPlan, inspectLegacyOpencodeState,\n  verifyManagedLegacyFile } = require('./opencode-legacy-migration');\n",
        "// fix #16 (D10): the OpenCode legacy-migration module is removed\n"
        "// (Cursor-only). These stubs return exactly what it returned for a\n"
        "// non-OpenCode plan: no legacy location exists, legacy state is\n"
        "// absent, legacy cleanup finds nothing.\n"
        "function getLegacyLocationForPlan() { return null; }\n"
        "function inspectLegacyOpencodeState() {\n"
        "  return { status: 'absent', state: null, error: null };\n"
        "}\n"
        "function verifyManagedLegacyFile() { return { skipped: true }; }\n"
        "function cleanupLegacyOpencodeInstall() {\n"
        "  return { detected: false, complete: false, removedPaths: [], retainedPaths: [], warnings: [] };\n"
        "}\n")
    sub(f, "const { withOpenCodeInstallLocks } = require('./opencode-install-lock');\n", "")
    sub(f, "const { assertScriptBoundary, isScriptBoundary } = require('./opencode-script-boundary');\n", "")
    # Disabled-migration factory (same shape as the upstream
    # createDisabledMigration for non-Claude targets, so the ownership guard
    # and stale/excluded-paths reconciliation see the same fields).
    sub(f, "function isMarkdownPath(filePath) {",
        "function uniqueOperations(operations) {\n"
        "  const byDestination = new Map();\n"
        "  for (const operation of operations) {\n"
        "    byDestination.set(comparablePath(operation.destinationPath), operation);\n"
        "  }\n"
        "  return [...byDestination.values()];\n"
        "}\n"
        "\n"
        "// fix #16 (D13): the legacy Claude-skill migration is gone. The install\n"
        "// proceeds with the plan's own operations and no legacy skill moves.\n"
        "// Shape mirrors the upstream disabled migration (enabled: false, plan\n"
        "// operations applied, previous install-state operations retained in\n"
        "// the final state so selective reinstalls keep earlier modules).\n"
        "function createDisabledMigration(plan) {\n"
        "  const previousState = fs.existsSync(plan.installStatePath)\n"
        "    ? readInstallState(plan.installStatePath)\n"
        "    : null;\n"
        "  const finalState = {\n"
        "    ...plan.statePreview,\n"
        "    operations: uniqueOperations([\n"
        "      ...((previousState && previousState.operations) || []),\n"
        "      ...((plan.statePreview && plan.statePreview.operations) || []),\n"
        "    ]).map(operation => ({ ...operation })),\n"
        "  };\n"
        "  return {\n"
        "    enabled: false,\n"
        "    appliedOperations: [...plan.operations],\n"
        "    skippedOperations: [],\n"
        "    warnings: [],\n"
        "    bridgeState: finalState,\n"
        "    finalState,\n"
        "    legacyOperationsToRemove: [],\n"
        "    retainedLegacyOperations: [],\n"
        "    requiresBridgeState: plan.operations.length > 0,\n"
        "  };\n"
        "}\n"
        "\n"
        "function isMarkdownPath(filePath) {")
    resub(f, r"[ \t]*assertSafeClaudeSkillOperation\([^;]*;\n", "", count=5)
    resub(f, r"prepareClaudeSkillMigration\(plan\)", "createDisabledMigration(plan)", count=2)
    remove_function(f, "shouldSetClaudeCommitAttributionPreference")
    remove_function(f, "writeClaudeCommitAttributionPreference")
    remove_function(f, "preflightClaudeSettingsOperations")
    remove_function(f, "findPreviousManagedHooks")
    replace_function(f, "prepareHookConsentMigration",
                     "// fix #16 (D10/D12): hook-consent migration is a passthrough. The\n"
                     "// OpenCode bridge-state branch and the declined-consent\n"
                     "// 'remove-claude-settings-hooks' removal both targeted host\n"
                     "// settings files Cursor installs never produce; Cursor hooks live\n"
                     "// in the plugin's hooks.json, not in a settings file.\n"
                     "function prepareHookConsentMigration(plan, migration) {\n"
                     "  return migration;\n"
                     "}")
    replace_function(f, "assertOpenCodeScriptBoundary",
                     "// fix #16 (D10): the scripts/package.json CommonJS boundary check is\n"
                     "// a no-op — the boundary copy is produced only by the deleted\n"
                     "// OpenCode/Claude adapters, never by the Cursor adapter.\n"
                     "function assertOpenCodeScriptBoundary(plan, writtenDestinations = new Set()) {\n"
                     "  return;\n"
                     "}")
    replace_function(f, "assertOpenCodeLeaseCoverage",
                     "// fix #16 (D10): OpenCode installs are gone; the lease check is a\n"
                     "// no-op (kept as an exported no-op because install-lifecycle still\n"
                     "// calls it on the repair path).\n"
                     "function assertOpenCodeLeaseCoverage(plan, lease) {\n"
                     "  return;\n"
                     "}")
    # previewInstallPlan: drop the preflight line
    sub(f, "  preflightClaudeSettingsOperations(appliedPlan);\n", "")
    # applyInstallPlan: drop the opencode branch + the claude settings lock
    sub(f, "  if (plan.adapter?.target === 'opencode') {\n"
            "    assertSafeInstallOperation(plan, { destinationPath: plan.installStatePath });\n"
            "    return withOpenCodeInstallLocks(\n"
            "      getOpenCodeInstallRoots(plan),\n"
            "      lease => applyInstallPlanLocked(plan, { ...dependencies, opencodeLease: lease }, false),\n"
            "      dependencies.opencodeLease\n"
            "    );\n"
            "  }\n", "")
    sub(f, "  const isClaudeManualTarget = plan.adapter\n"
            "    && (plan.adapter.target === 'claude' || plan.adapter.target === 'claude-project');\n"
            "  const settingsPathToLock = isClaudeManualTarget\n"
            "    ? getClaudeSettingsPath(plan.targetRoot)\n"
            "    : null;\n"
            "  if (settingsPathToLock) {\n"
            "    assertSafeInstallOperation(plan, { destinationPath: settingsPathToLock });\n"
            "  }\n"
            "  return settingsPathToLock\n"
            "    ? runWithSettingsLock(\n"
            "      settingsPathToLock,\n"
            "      () => applyInstallPlanLocked(plan, dependencies, true)\n"
            "    )\n"
            "    : applyInstallPlanLocked(plan, dependencies, false);",
        "  return applyInstallPlanLocked(plan, dependencies, false);")
    # applyInstallPlanLocked: hook-removal accounting is gone (always zero now)
    sub(f, "  const hookRemovalCount = appliedPlan.operations.filter(operation => (\n"
            "    operation.kind === 'remove-claude-settings-hooks'\n"
            "  )).length;",
        "  // fix #16 (D12): settings-hook removal is gone; this stays zero.\n"
        "  const hookRemovalCount = 0;")
    text = read(f)
    m = re.search(r"      if \(\n        operation\.kind === 'update-claude-settings'\n"
                  r"        \|\| operation\.kind === 'remove-claude-settings-hooks'\n"
                  r"      \) \{.*?\n        continue;\n      \}\n", text, re.S)
    if not m:
        ERRORS.append("scripts/lib/install/apply.js: settings-apply if-block not found")
    else:
        write(f, text[: m.start()] + text[m.end():])
        CHANGES.append("scripts/lib/install/apply.js — removed settings-apply branch from the install loop")
    sub(f, "      if (hasLegacyMigration) {\n"
            "        removeLegacyClaudeSkillFiles(migration, plan.targetRoot);\n"
            "      }\n", "")
    sub(f, "  const hasLegacyMigration = migration.legacyOperationsToRemove.length > 0;\n", "")
    sub(f, "      if (shouldSetClaudeCommitAttributionPreference(appliedPlan)) {\n"
            "        writeClaudeCommitAttributionPreference(\n"
            "          getClaudeSettingsPath(plan.targetRoot),\n"
            "          { lockHeld: settingsLockHeld }\n"
            "        );\n"
            "      }\n", "")
    text = read(f)
    m = re.search(r"    let antigravityMigrationWarnings = \[\];\n"
                  r"  try \{\n"
                  r"    const antigravityMigration = cleanupLegacyAntigravityInstall\(appliedPlan\);\n"
                  r".*?\n  \} catch \(error\) \{\n"
                  r".*?\n  \}\n", text, re.S)
    if not m:
        ERRORS.append("scripts/lib/install/apply.js: antigravity cleanup try/catch not found")
    else:
        write(f, text[: m.start()]
              + "    // fix #16 (D10): legacy Antigravity cleanup removed with the adapter.\n"
              + "    let antigravityMigrationWarnings = [];\n"
              + text[m.end():])
        CHANGES.append("scripts/lib/install/apply.js — removed legacy Antigravity cleanup block")
    sub(f, "  prepareHookConsentMigration,\n", "  prepareHookConsentMigration,\n  createDisabledMigration,\n")
    REMOVALS.append("install/apply.js: commit-attribution preference write removed (D12/D15). Loss: the installer no longer writes the commit-attribution preference into the host settings file (default attribution behavior applies). The Claude-settings module it ran through is deleted and no verified Cursor settings path was invented for it.")
    REMOVALS.append("install/apply.js: legacy Claude-skill migration removed (D13). Loss: migrating legacy Claude flat skills into the install — replaced by the disabled-migration shape (plan operations only), so a Cursor install never moves legacy skill files.")
    # --- install-lifecycle.js: the same narrowing for doctor/repair/uninstall
    f = "scripts/lib/install-lifecycle.js"
    sub(f, "const { withOpenCodeInstallLocks } = require('./install/opencode-install-lock');\n", "")
    sub(f, "const { isCodexUserConfig } = require('./install/codex-user-config');\n", "")
    sub(f, "const {\n  prepareClaudeSkillMigration,\n} = require('./install/claude-skill-migration');\n", "")
    sub(f, "const {\n  getLegacyAntigravityLocation,\n  inspectLegacyAntigravityState,\n} = require('./install/antigravity-legacy-migration');\n", "")
    sub(f, "const {\n  getLegacyOpencodeLocation,\n  inspectLegacyOpencodeState,\n} = require('./install/opencode-legacy-migration');\n", "")
    sub(f, "const {\n  acquireSettingsLock,\n  getClaudeSettingsPath,\n  inspectManagedHooks,\n  materializeManagedHooks,\n  repairManagedHooks,\n  uninstallManagedHooks,\n  updateSettingsAtomic,\n  validateManagedHooks,\n} = require('./install/claude-settings');\n", "")
    sub(f, "  assertClaudeSettingsDestination,\n", "")
    remove_function(f, "repairClaudeSettings")
    remove_function(f, "uninstallClaudeSettings")
    remove_function(f, "inspectClaudeSettingsOperation")
    replace_function(f, "acquireRepairSettingsLock",
                     "function acquireRepairSettingsLock(record, options) {\n"
                     "  // fix #16 (D10/D12): the Cursor settings lock only existed for\n"
                     "  // update-claude-settings operations, which Cursor installs never\n"
                     "  // produce.\n"
                     "  return null;\n"
                     "}")
    sub(f, "    case 'update-claude-settings':\n      return repairClaudeSettings(operation, trustedRoot, resolved);",
        "")
    sub(f, "    case 'update-claude-settings':\n      return uninstallClaudeSettings(operation, trustedRoot, options);",
        "")
    sub(f, "    case 'update-claude-settings':\n      return inspectClaudeSettingsOperation(operation, inspectedPath, trustedRoot, target);",
        "")
    sub(f, "  if (operationHealth.invalidSettings.length > 0) {\n"
            "    issues.push(\n"
            "      buildIssue(\n"
            "        'error',\n"
            "        'invalid-claude-settings',\n"
            "        operationHealth.invalidSettings[0].error,\n"
            "        { paths: destinationPaths(operationHealth.invalidSettings) }\n"
            "      )\n"
            "    );\n"
            "  }\n", "")
    sub(f, "    ...desiredPlan.operations\n"
            "      .filter(operation => (\n"
            "        operation.kind === 'update-claude-settings'\n"
            "        && operation.previousManagedHooks\n"
            "        && !isDeepStrictEqual(operation.previousManagedHooks, operation.managedHooks)\n"
            "      ))\n"
            "      .map(operation => ({ ...operation })),\n", "")
    # Exact full-block removal (the old regex looked for a bare 6-space
    # `}` close, which this block does not have — its return object closes
    # with `};`).
    sub(f, "    if (operation.kind === 'update-claude-settings') {\n"
            "      const sourcePath = resolveOperationSourcePath(repoRoot, operation);\n"
            "      if (!sourcePath || !fs.existsSync(sourcePath)) {\n"
            "        throw new Error(\n"
            "          `Missing source file for repair: ${sourcePath || operation.sourceRelativePath}`\n"
            "        );\n"
            "      }\n"
            "      return {\n"
            "        ...operation,\n"
            "        sourcePath,\n"
            "        previousManagedHooks: operation.managedHooks,\n"
            "        managedHooks: materializeManagedHooks(\n"
            "          readHooksConfigNoFollow(sourcePath),\n"
            "          trustedRoot\n"
            "        ),\n"
            "      };\n"
            "    }\n", "")
    sub(f, "      if ((isCodexUserConfig(record, operation)\n"
            "        || (record.adapter.target === 'opencode'\n"
            "          && require('./install/apply').getOpenCodeActivationKind(record, operation)))",
        "      if ((record.adapter.target === 'opencode'\n"
            "          && require('./install/apply').getOpenCodeActivationKind(record, operation))")
    sub(f, "  const initialMigration = prepareClaudeSkillMigration(trustedPlan);",
        "  const initialMigration = require('./install/apply').createDisabledMigration(trustedPlan);")
    sub(f, "  const migration = trustedPlan.target === 'opencode'\n"
            "    ? require('./install/apply').prepareHookConsentMigration(trustedPlan, guardedMigration)\n"
            "    : guardedMigration;",
        "  const migration = guardedMigration;")
    # discoverInstalledStates: drop the opencode + antigravity legacy branches
    text = read(f)
    start_marker = "    if (adapter.target === 'opencode') {"
    end_marker = ("    return [\n"
                  "      canonicalRecord,\n"
                  "      buildDiscoveryRecord(adapter, context, legacyLocation, legacyInspection.state),\n"
                  "    ];")
    s = text.find(start_marker)
    e = text.find(end_marker)
    if s < 0 or e < 0:
        ERRORS.append("scripts/lib/install-lifecycle.js: discoverInstalledStates legacy branches not found")
    else:
        e_end = e + len(end_marker)
        if text[e_end: e_end + 1] == "\n":
            e_end += 1
        write(f, text[:s] + "    return [canonicalRecord];\n" + text[e_end:])
        CHANGES.append("scripts/lib/install-lifecycle.js — removed opencode/antigravity legacy branches from discoverInstalledStates")
    # repairInstalledStates: replace the opencode repair block with an error result
    text = read(f)
    m = re.search(r"    if \(record\.adapter\.target !== 'opencode' \|\| options\.dryRun\) return performRepair\(\);\n"
                  r"    let repairResult;\n"
                  r"    try \{.*?\n    \}\n", text, re.S)
    if not m:
        ERRORS.append("scripts/lib/install-lifecycle.js: opencode repair block not found")
    else:
        write(f, text[: m.start()]
              + "    if (record.adapter.target !== 'opencode' || options.dryRun) return performRepair();\n"
              + "    // fix #16 (D10): OpenCode repair is removed with the adapter; no\n"
              + "    // Cursor-only discovery ever yields an OpenCode record.\n"
              + "    return repairErrorResult(record, 'OpenCode repair is no longer supported (fix #16: Cursor-only).');\n"
              + text[m.end():])
        CHANGES.append("scripts/lib/install-lifecycle.js — replaced opencode repair block with an error result")
    # uninstall: drop the settings-lock block + script-boundary require
    sub(f, "      if (operations.some(operation => operation.kind === 'update-claude-settings')) {\n"
            "        releaseSettingsLock = acquireSettingsLock(\n"
            "          getClaudeSettingsPath(record.targetRoot)\n"
            "        );\n"
            "      }\n", "")
    sub(f, "      const { isScriptBoundary, retainScriptBoundary } = require('./install/opencode-script-boundary');",
        "      // fix #16 (D10): the scripts/package.json boundary copy is produced\n"
        "      // only by the deleted OpenCode/Claude adapters, so no Cursor\n"
        "      // install ever contains a boundary operation.\n"
        "      const isScriptBoundary = () => false;\n"
        "      const retainScriptBoundary = () => false;")
    REMOVALS.append("install-lifecycle.js: Claude settings repair/uninstall/inspect handlers removed (D12). Loss: doctor/repair/uninstall of update-claude-settings operations (Cursor installs never produce them; Cursor hooks live in the plugin's hooks.json).")
    REMOVALS.append("install-lifecycle.js: legacy OpenCode/Antigravity discovery + repair removed (D10). Loss: discovering/repairing legacy multi-host installs; doctor/repair now cover Cursor installs only.")

def remove_braced_block(f, start_pattern):
    """Delete a braced block starting at the line matching start_pattern
    (e.g. an `if (...) {` branch) by brace matching. If the pattern
    itself ends with `{`, that brace IS the block's opener (the old
    code searched past it and deleted the wrong span)."""
    text = read(f)
    m = re.search(start_pattern, text, re.M)
    if not m:
        ERRORS.append(f"{f}: block not found: {start_pattern}")
        return False
    start = m.start()
    matched = m.group(0)
    if matched.rstrip().endswith("{"):
        brace = m.start() + len(matched.rstrip()) - 1
    else:
        brace = text.index("{", m.end())
    end = _brace_match_end(text, brace)
    if end < 0:
        ERRORS.append(f"{f}: block {start_pattern}: unbalanced braces")
        return False
    while end < len(text) and text[end] == "\n":
        end += 1
    write(f, text[:start] + text[end:])
    CHANGES.append(f"{f} — removed block {start_pattern}")
    return True


def remove_array_entry(f, id_value):
    """Delete one flat object-literal entry from a JSON-ish array, found by
    its "id": "<value>" (or "file": "<value>") line. Scans back to the
    entry's opening `  {` line, brace-matches forward, and deletes the span
    plus a following comma. Caller must verify the file still parses."""
    text = read(f)
    idx = -1
    for needle in (f'"id": "{id_value}"', f"'id': '{id_value}'",
                   f"id: '{id_value}'", f'id: "{id_value}"',
                   f'"file": "{id_value}"', f"'file': '{id_value}'",
                   f"file: '{id_value}'", f'file: "{id_value}"'):
        idx = text.find(needle)
        if idx >= 0:
            break
    if idx < 0:
        ERRORS.append(f"{rel(f)}: remove_array_entry {id_value!r} not found")
        return
    start = text.rfind("\n  {", 0, idx)
    if start < 0:
        ERRORS.append(f"{rel(f)}: remove_array_entry {id_value!r}: no opening brace line")
        return
    start += 1  # at the '{'
    depth = 0
    i = start
    instr = False
    while i < len(text):
        ch = text[i]
        if instr:
            if ch == "\\":
                i += 2
                continue
            if ch == '"':
                instr = False
        else:
            if ch == '"':
                instr = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    break
        i += 1
    if depth != 0:
        ERRORS.append(f"{rel(f)}: remove_array_entry {id_value!r}: unbalanced braces")
        return
    end = i + 1
    # Swallow a following comma and the newline after the closing brace.
    if end < len(text) and text[end] == ",":
        end += 1
    if end < len(text) and text[end] == "\n":
        end += 1
    write(f, text[:start] + text[end:])
    CHANGES.append(f"{rel(f)} — removed array entry {id_value!r}")


def edit_session_paths_round2():
    """Session/state paths re-pointed to the verified Cursor agent data home
    (~/.cursor/ecc) and project-local .ecc/ (D15: never invent a Cursor path;
    .ecc/ is the plugin-owned namespace)."""
    f = "scripts/lib/session-manager.js"
    sub(f, " * Sessions are stored as markdown files in ~/.claude/session-data/ with\n"
            " * legacy read compatibility for ~/.claude/sessions/:",
        " * Sessions are stored as markdown files in ~/.cursor/ecc/session-data/ with\n"
        " * legacy read compatibility for ~/.cursor/ecc/sessions/:")
    f = "scripts/lib/state-store/index.js"
    sub(f, "const DEFAULT_STATE_STORE_RELATIVE_PATH = path.join('.claude', 'ecc', 'state.db');",
        "const DEFAULT_STATE_STORE_RELATIVE_PATH = path.join('.ecc', 'state.db');")
    f = "scripts/lib/skill-improvement/observations.js"
    sub(f, "  return path.join(resolveProjectRoot(options), '.claude', 'ecc', 'skills');",
        "  return path.join(resolveProjectRoot(options), '.ecc', 'skills');")
    f = "scripts/lib/skill-evolution/tracker.js"
    sub(f, "  return path.join(resolveHomeDir(options.homeDir), '.claude', 'state', 'skill-runs.jsonl');",
        "  return path.join(resolveHomeDir(options.homeDir), '.cursor', 'ecc', 'state', 'skill-runs.jsonl');")
    f = "scripts/lib/skill-evolution/provenance.js"
    sub(f, "    learned: path.join(homeDir, '.claude', 'skills', 'learned'),\n"
            "    imported: path.join(homeDir, '.claude', 'skills', 'imported'),",
        "    learned: path.join(homeDir, '.cursor', 'ecc', 'skills', 'learned'),\n"
        "    imported: path.join(homeDir, '.cursor', 'ecc', 'skills', 'imported'),")
    f = "scripts/lib/observer-sessions.js"
    sub(f, "  const envRoot = process.env.CLAUDE_PROJECT_DIR;",
        "  const envRoot = process.env.CURSOR_PROJECT_DIR;")
    # plan-canvas: the lib resolver + the three hook-side duplicates all land
    # on the agent data home (ECC_AGENT_DATA_HOME / ~/.cursor/ecc) so the
    # producer and the hooks share one directory.
    f = "scripts/lib/plan-canvas/sessions.js"
    sub(f, "// The producer and the SessionStart/Stop hooks must land on one directory. The\n"
            "// hooks resolve CLAUDE_CONFIG_DIR (they cannot require this file: managed\n"
            "// installs ship scripts/ without scripts/lib/, see #3259), so writing to\n"
            "// ~/.claude here regardless would hide queued feedback from them whenever a\n"
            "// session runs under a second profile.\n"
            "function resolveClaudeConfigDir(env = process.env) {\n"
            "  const configured = env.CLAUDE_CONFIG_DIR;\n"
            "  const trimmed = configured ? String(configured).trim() : '';\n"
            "  if (!trimmed) return path.join(os.homedir(), '.claude');",
        "// The producer and the SessionStart/Stop hooks must land on one directory. The\n"
        "// hooks resolve ECC_AGENT_DATA_HOME (they cannot require this file: managed\n"
        "// installs ship scripts/ without scripts/lib/, see #3259), so writing to\n"
        "// ~/.cursor/ecc here regardless would hide queued feedback from them whenever a\n"
        "// session runs under a second profile.\n"
        "function resolveAgentDataHome(env = process.env) {\n"
        "  const configured = env.ECC_AGENT_DATA_HOME;\n"
        "  const trimmed = configured ? String(configured).trim() : '';\n"
        "  if (!trimmed) return path.join(os.homedir(), '.cursor', 'ecc');")
    sub(f, "  return path.join(resolveClaudeConfigDir(env), 'plan-canvas');",
        "  return path.join(resolveAgentDataHome(env), 'plan-canvas');")
    f = "scripts/lib/plan-canvas/markdown.js"
    sub(f, " * Renders .claude/plans/*.plan.md artifacts to HTML body content.",
        " * Renders .ecc/plans/*.plan.md artifacts to HTML body content.")
    f = "scripts/lib/orchestration-session.js"
    sub(f, "    coordinationDir: path.join(cwd, '.claude', 'orchestration', targetPath),",
        "    coordinationDir: path.join(cwd, '.ecc', 'orchestration', targetPath),")
    f = "scripts/lib/session-adapters/dmux-tmux.js"
    sub(f, "  const coordinationDir = path.resolve(cwd, '.claude', 'orchestration', target);",
        "  const coordinationDir = path.resolve(cwd, '.ecc', 'orchestration', target);")
    f = "scripts/lib/control-pane/state.js"
    sub(f, "const DEFAULT_STATE_STORE_RELATIVE_PATH = path.join('.claude', 'ecc', 'state.db');",
        "const DEFAULT_STATE_STORE_RELATIVE_PATH = path.join('.ecc', 'state.db');")
    sub(f, "  return path.join(homeDir(env), '.claude', 'ecc2.db');",
        "  return path.join(homeDir(env), '.cursor', 'ecc', 'ecc2.db');")
    sub(f, "  const paths = [path.join(home, 'Library', 'Application Support', 'ecc2', 'config.toml'), path.join(home, '.config', 'ecc2', 'config.toml'), path.join(home, '.claude', 'ecc2.toml')];",
        "  const paths = [path.join(home, 'Library', 'Application Support', 'ecc2', 'config.toml'), path.join(home, '.config', 'ecc2', 'config.toml'), path.join(home, '.cursor', 'ecc', 'ecc2.toml')];")
    sub(f, "    paths.push(path.join(current, '.claude', 'ecc2.toml'));",
        "    paths.push(path.join(current, '.ecc', 'ecc2.toml'));")
    f = "scripts/hooks/hookify-runtime.js"
    resub(f, r"'\.claude'", "'.ecc'", count=7)
    resub(f, r"\.claude/", ".ecc/", count=1)
    # Agent-data-home readers (duplicated on purpose: hooks ship without
    # scripts/lib/ — see #3259). Re-point from ~/.claude to ~/.cursor/ecc.
    for hf in ("scripts/hooks/mcp-health-check.js",
               "scripts/hooks/plan-canvas-pending.js",
               "scripts/hooks/plan-canvas-sessions.js",
               "scripts/hooks/post-bash-command-log.js"):
        if not exists(hf):
            continue
        t = read(hf)
        t2 = t.replace("function claudeConfigDir() {", "function agentDataHome() {")
        t2 = t2.replace("const configured = process.env.CLAUDE_CONFIG_DIR;",
                        "const configured = process.env.ECC_AGENT_DATA_HOME;")
        t2 = t2.replace("if (!trimmed) return path.join(os.homedir(), '.claude');",
                        "if (!trimmed) return path.join(os.homedir(), '.cursor', 'ecc');")
        t2 = t2.replace("claudeConfigDir()", "agentDataHome()")
        if t2 != t:
            write(hf, t2)
            CHANGES.append(f"{hf} — claudeConfigDir() re-pointed to the agent data home (~/.cursor/ecc)")
    f = "scripts/hooks/ecc-statusline.js"
    sub(f, "    const claudeDir = process.env.CLAUDE_CONFIG_DIR || path.join(os.homedir(), '.claude');\n"
            "    const todosDir = path.join(claudeDir, 'todos');",
        "    const agentDataDir = process.env.ECC_AGENT_DATA_HOME || path.join(os.homedir(), '.cursor', 'ecc');\n"
        "    const todosDir = path.join(agentDataDir, 'todos');")
    # mcp-health-check: MCP config candidates + trust logic -> Cursor files
    f = "scripts/hooks/mcp-health-check.js"
    sub(f, "  return [\n"
            "    path.join(cwd, '.claude.json'),\n"
            "    path.join(cwd, '.claude', 'settings.json'),\n"
            "    path.join(home, '.claude.json'),\n"
            "    path.join(home, '.claude', 'settings.json')\n"
            "  ];",
        "  return [\n"
        "    path.join(cwd, '.cursor', 'mcp.json'),\n"
        "    path.join(home, '.cursor', 'mcp.json')\n"
        "  ];")
    sub(f, "  // SECURITY: cloning a malicious repo must not auto-execute its MCP servers.\n"
            "  // Workspace configs (cwd .claude.json / .claude/settings.json) are untrusted\n"
            "  // by default; only probe them with explicit operator opt-in.\n"
            "  // Home configs (~/.claude.json) and explicit ECC_MCP_CONFIG_PATH remain allowed.",
        "  // SECURITY: cloning a malicious repo must not auto-execute its MCP servers.\n"
        "  // Workspace configs (cwd .cursor/mcp.json) are untrusted by default; only\n"
        "  // probe them with explicit operator opt-in.\n"
        "  // Home configs (~/.cursor/mcp.json) and explicit ECC_MCP_CONFIG_PATH remain allowed.")
    sub(f, "    // A config file in the user's home directory (~/.claude.json or\n"
            "    // ~/.claude/settings.json) is always trusted regardless of cwd.\n"
            "    const isHomeSource = src === pathMod.join(home, '.claude.json')\n"
            "      || src === pathMod.join(home, '.claude', 'settings.json')\n"
            "      || src.startsWith(pathMod.join(home, '.claude') + pathMod.sep);",
        "    // A config file in the user's home directory (~/.cursor/mcp.json) is\n"
        "    // always trusted regardless of cwd.\n"
        "    const isHomeSource = src === pathMod.join(home, '.cursor', 'mcp.json')\n"
        "      || src.startsWith(pathMod.join(home, '.cursor') + pathMod.sep);")
    sub(f, "      const isWorkspaceSource = src === pathMod.join(cwd, '.claude.json')\n"
            "        || src === pathMod.join(cwd, '.claude', 'settings.json')\n"
            "        || src.startsWith(cwd + pathMod.sep + '.claude' + pathMod.sep);",
        "      const isWorkspaceSource = src === pathMod.join(cwd, '.cursor', 'mcp.json')\n"
        "        || src.startsWith(cwd + pathMod.sep + '.cursor' + pathMod.sep);")
    # session adapters: dmux-tmux only (F2)
    f = "scripts/lib/session-adapters/registry.js"
    write(f, """'use strict';

const { createDmuxTmuxAdapter } = require('./dmux-tmux');

// fix #16 (D10/F2): session adapters are dmux-tmux only. The Claude-history,
// Codex-worktree and OpenCode adapters (and their transcript/history readers)
// were deleted with their host modules.
const TARGET_TYPE_TO_ADAPTER_ID = Object.freeze({
  plan: 'dmux-tmux',
  session: 'dmux-tmux',
});

function buildDefaultAdapterOptions(options, adapterId) {
  const sharedOptions = {
    loadStateStoreImpl: options.loadStateStoreImpl,
    persistSnapshots: options.persistSnapshots,
    recordingDir: options.recordingDir,
    stateStore: options.stateStore
  };

  return {
    ...sharedOptions,
    ...(options.adapterOptions && options.adapterOptions[adapterId]
      ? options.adapterOptions[adapterId]
      : {})
  };
}

function createDefaultAdapters(options = {}) {
  return [
    createDmuxTmuxAdapter(buildDefaultAdapterOptions(options, 'dmux-tmux'))
  ];
}

function coerceTargetValue(value) {
  if (typeof value !== 'string' || value.trim().length === 0) {
    throw new Error('Structured session targets require a non-empty string value');
  }

  return value.trim();
}

function normalizeStructuredTarget(target, context = {}) {
  if (!target || typeof target !== 'object' || Array.isArray(target)) {
    return {
      target,
      context: { ...context }
    };
  }

  const value = coerceTargetValue(target.value);
  const type = typeof target.type === 'string' ? target.type.trim() : '';
  if (type.length === 0) {
    throw new Error('Structured session targets require a non-empty type');
  }

  const adapterId = target.adapterId || TARGET_TYPE_TO_ADAPTER_ID[type] || context.adapterId || null;
  const nextContext = {
    ...context,
    adapterId
  };

  return {
    target: value,
    context: nextContext
  };
}

function createAdapterRegistry(options = {}) {
  const adapters = options.adapters || createDefaultAdapters(options);

  return {
    adapters,
    getAdapter(id) {
      const adapter = adapters.find(candidate => candidate.id === id);
      if (!adapter) {
        throw new Error(`Unknown session adapter: ${id}`);
      }

      return adapter;
    },
    listAdapters() {
      return adapters.map(adapter => ({
        id: adapter.id,
        description: adapter.description || '',
        targetTypes: Array.isArray(adapter.targetTypes) ? [...adapter.targetTypes] : []
      }));
    },
    select(target, context = {}) {
      const normalized = normalizeStructuredTarget(target, context);
      const adapter = normalized.context.adapterId
        ? this.getAdapter(normalized.context.adapterId)
        : adapters.find(candidate => candidate.canOpen(normalized.target, normalized.context));
      if (!adapter) {
        throw new Error(`No session adapter matched target: ${target}`);
      }

      return adapter;
    },
    open(target, context = {}) {
      const normalized = normalizeStructuredTarget(target, context);
      const adapter = this.select(normalized.target, normalized.context);
      return adapter.open(normalized.target, normalized.context);
    }
  };
}

function inspectSessionTarget(target, options = {}) {
  const registry = createAdapterRegistry(options);
  return registry.open(target, options).getSnapshot();
}

module.exports = {
  createAdapterRegistry,
  createDefaultAdapters,
  inspectSessionTarget,
  normalizeStructuredTarget
};
""")
    CHANGES.append("scripts/lib/session-adapters/registry.js — rewritten dmux-tmux only (D10/F2)")
    f = "scripts/lib/session-adapters/canonical-session.js"
    remove_function(f, "deriveClaudeWorkerId")
    remove_function(f, "normalizeClaudeHistorySession")
    remove_function(f, "normalizeCodexWorktreeSession")
    remove_function(f, "normalizeOpencodeSession")
    sub(f, "  normalizeClaudeHistorySession,\n", "")
    sub(f, "  normalizeCodexWorktreeSession,\n", "")
    sub(f, "  normalizeOpencodeSession,\n", "")
    REMOVALS.append("session-adapters: Claude-history / Codex-worktree / OpenCode adapters + their canonical-session normalizers removed (D10/F2). Loss: reading Claude/Codex/OpenCode session transcripts and worktrees as orchestrated sessions; dmux-tmux sessions are unaffected.")


def edit_context_profile_round2():
    """D20: context-profile native execution removed (CLI-only, no Cursor
    provider). Carrier/resolve machinery stays (cursor layout exists)."""
    f = "scripts/lib/context-carriers.js"
    sub(f, "const LAYOUTS = Object.freeze({\n"
            "  claude: { id: 'claude-plugin@1', skillRoot: 'skills', manifestPath: '.claude-plugin/plugin.json' },\n"
            "  codex: { id: 'codex-plugin@1', skillRoot: 'skills', manifestPath: '.codex-plugin/plugin.json' },\n"
            "  pi: { id: 'pi-package@1', skillRoot: 'skills', manifestPath: 'package.json' },\n"
            "  opencode: { id: 'opencode-project@1', skillRoot: '.opencode/skills', manifestPath: null },\n"
            "  cursor: { id: 'cursor-project@1', skillRoot: '.cursor/skills', manifestPath: null },\n"
            "});",
        "const LAYOUTS = Object.freeze({\n"
        "  cursor: { id: 'cursor-project@1', skillRoot: '.cursor/skills', manifestPath: null },\n"
        "});")
    replace_function(f, "generatedManifest",
                     "// New, allowlisted discovery manifests. Cursor uses native project\n"
                     "// directories, so no generated manifest is needed (the carrier\n"
                     "// installs skills directly under `.cursor/skills`).\n"
                     "function generatedManifest(target, layout) {\n"
                     "  return [];\n"
                     "}")
    f = "scripts/lib/context-profile-commands.js"
    sub(f, "const NATIVE_COMMANDS = ['prepare-native', 'native-status', 'native-rollback', 'native-recover'];\n"
            "const COMMANDS = ['start', 'resolve', 'run', 'set', 'mode', 'status', 'rollback', 'recover', 'routing-index', ...NATIVE_COMMANDS];",
        "const COMMANDS = ['resolve', 'set', 'mode', 'status', 'rollback', 'recover', 'routing-index'];")
    sub(f, "  '--target', '--selection', '--include', '--exclude', '--native-root'];",
        "  '--target', '--selection', '--include', '--exclude'];")
    sub(f, "} else if (!arg.startsWith('-') && !result.profileId && ['resolve', 'run', 'set', 'mode'].includes(result.command)) result.profileId = arg;",
        "} else if (!arg.startsWith('-') && !result.profileId && ['resolve', 'set', 'mode'].includes(result.command)) result.profileId = arg;")
    sub(f, "  const taskCommand = ['resolve', 'run'].includes(result.command);",
        "  const taskCommand = result.command === 'resolve';")
    sub(f, "  const allowed = result.command === 'start' ? ['--state-root', '--native-root'] : NATIVE_COMMANDS.includes(result.command)\n"
            "    ? ['--state-root', '--native-root', '--expected-revision', '--expected-digest'] : taskCommand\n"
            "    ? ['--task-input', '--previous', '--expected-digest', '--state-root', '--target', '--selection', '--include', '--exclude',\n"
            "      ...(result.command === 'run' ? ['--native-root'] : [])]\n",
        "  const allowed = taskCommand\n"
        "    ? ['--task-input', '--previous', '--expected-digest', '--state-root', '--target', '--selection', '--include', '--exclude']\n")
    sub(f, "  if ((NATIVE_COMMANDS.includes(result.command) || result.command === 'start') && !result['native-root']) throw new Error(`${result.command} requires --native-root`);\n"
            "  if (result['native-root'] && !result['state-root']) throw new Error('--native-root requires --state-root');\n",
        "")
    sub(f, "  if (result.command === 'start' && result.json && !result.dryRun) {\n"
            "    throw new Error('--json requires --dry-run for interactive start');\n"
            "  }\n", "")
    # Whole-function replacement (D20): the start / native / run
    # branches are CLI-only, so the clean function is resolve +
    # routing-index + store only, with the default target cursor.
    replace_function(f, "execute",
                     "function execute(options) {\n"
"  if (options.command === 'resolve') {\n"
"    const { resolveTaskContext } = require('./context-selection');\n"
"    const stored = options['state-root']\n"
"      ? require('./context-profile-store').getStoreStatus({ stateRoot: options['state-root'] }) : null;\n"
"    if (stored && (!stored.configured || stored.recoveryRequired)) throw new Error('Configure or recover the stored profile before resolving');\n"
"    if (stored) {\n"
"      const carrier = require('./context-carriers').planContextCarrier({ profileId: stored.profileId,\n"
"        target: stored.target, selectionMode: stored.selectionMode, include: stored.include, exclude: stored.exclude });\n"
"      if (carrier.carrierDigest !== stored.carrierDigest) throw new Error('Stored profile source is stale; preview and set the current generation before resolving');\n"
"    }\n"
"    const input = { task: readInput(options['task-input']),\n"
"      profileId: stored?.profileId || options.profileId || 'lean@1', target: stored?.target || options.target || 'cursor',\n"
"      selectionMode: stored?.selectionMode || options.selection || 'auto', include: stored?.include || options.include,\n"
"      exclude: stored?.exclude || options.exclude,\n"
"      load: options.load && !options.dryRun,\n"
"      previous: options.previous ? readInput(options.previous) : null,\n"
"      expectedDigest: options['expected-digest'] || null };\n"
"    return { selection: resolveTaskContext(input) };\n"
"  }\n"
"  if (options.command === 'routing-index') {\n"
"    const routing = require('./context-routing-index');\n"
"    return { routing: options.dryRun ? routing.routingIndexStatus(options['state-root'])\n"
"      : routing.writeRoutingIndex({ stateRoot: options['state-root'] }) };\n"
"  }\n"
"  const store = require('./context-profile-store');\n"
"  const common = { stateRoot: options['state-root'],\n"
"    ...(options['expected-revision'] === undefined ? {} : { expectedRevision: Number(options['expected-revision']) }) };\n"
"  if (options.command === 'status') return { store: store.getStoreStatus(common) };\n"
"  if (options.command === 'mode') {\n"
"    const current = store.getStoreStatus(common);\n"
"    if (!current.configured || current.recoveryRequired) throw new Error('Configure or recover the stored profile before changing mode');\n"
"    const input = { ...common, expectedRevision: common.expectedRevision ?? current.revision,\n"
"      profileId: current.profileId, target: current.target, include: current.include, exclude: current.exclude,\n"
"      selectionMode: options.profileId };\n"
"    return { store: options.dryRun ? store.previewStore(input) : store.applyStore(input) };\n"
"  }\n"
"  if (options.command === 'rollback' || options.command === 'recover') {\n"
"    if (options.dryRun) return { store: store.getStoreStatus(common), dryRun: true };\n"
"    return { store: options.command === 'rollback' ? store.rollbackStore(common) : store.recoverStore(common) };\n"
"  }\n"
"  const input = { ...common, profileId: options.profileId || 'lean@1', target: options.target || 'cursor',\n"
"    selectionMode: options.selection || 'auto', include: options.include, exclude: options.exclude,\n"
"    ...(options['expected-digest'] ? { expectedCarrierDigest: options['expected-digest'] } : {}) };\n"
"  return { store: options.dryRun ? store.previewStore(input) : store.applyStore(input) };\n"
"}\n")
    sub(f, "  return { schemaVersion: 'ecc.profile-operation.v1', status: (value.launch?.status === 'failed' || value.interactive?.status === 'failed') ? 'error' : 'success',\n"
            "    summary: options.command === 'start' ? 'Opt-in interactive session uses the verified isolated generation and inherited terminal. Context selection remains advisory.'\n"
            "      : options.command === 'run' ? 'Task launch uses selected context and the provider configuration. Inspect the launch result.'\n"
            "      : options.command === 'resolve' ? 'Task context resolved within the selected profile.'",
        "  return { schemaVersion: 'ecc.profile-operation.v1', status: 'success',\n"
        "    summary: options.command === 'resolve' ? 'Task context resolved within the selected profile.'")
    REMOVALS.append("context-profile native execution removed (D20). Loss: native isolated execution (Codex/Claude CLI sandboxing, interactive native sessions, `run` launching, prepare/rollback/recover native commands); the carrier/resolve/routing-index machinery for Cursor remains.")




def edit_post_generic():
    """Runs AFTER generic_pass() (called from main() between
    generic_pass() and self_check()). Holds every sub whose old text
    only matches the POST-generic-pass tree: the generic pass already
    rewrote "Claude Code" -> "Cursor" (and .claude/ -> .ecc/ in prose)
    before these ran, so their part-C copies failed 0x in build 2.
    New stragglers found in the build-2 tree are fixed here too."""

    # --- fix #24 (D-1/D-2): generic_pass() turned "Claude Code only" into
    # "Cursor only", inverting the meaning wherever the upstream text labelled
    # a Claude-Code-only mechanism. The mechanism is upstream-only; relabel it
    # "Upstream only" (banned-term-free). These repairs run after every
    # rebuild's generic pass, so they are idempotent by construction.
    # D-1: "(Cursor only — no Cursor equivalent in this plugin)" x10 in 9 files.
    for _f24, _n24 in [
        ("skills/hookify-rules/SKILL.md", 1),
        ("commands/hookify-configure.md", 1),
        ("commands/hookify-help.md", 1),
        ("commands/hookify-list.md", 1),
        ("commands/hookify.md", 1),
        ("commands/loop-start.md", 1),
        ("commands/resume-session.md", 1),
        ("commands/save-session.md", 1),
        ("commands/sessions.md", 2),
    ]:
        _p24 = os.path.join(BASE, _f24)
        if exists(_p24):
            resub(_p24, r"\(Cursor only — no Cursor equivalent in this plugin\)",
                  "(Upstream only — no Cursor equivalent in this plugin)", count=_n24)
    # D-2: "Cursor-only" hook headers x33 in scripts/hooks/ (one per file).
    # The 30 generic headers label a Claude Code hook event Cursor does not
    # have; the 3 special files get individual wording below.
    for _f24 in [
        "scripts/hooks/auto-tmux-dev.js",
        "scripts/hooks/config-protection.js",
        "scripts/hooks/context-prompt-suggestions.js",
        "scripts/hooks/desktop-notify.js",
        "scripts/hooks/doc-file-warning.js",
        "scripts/hooks/ecc-context-monitor.js",
        "scripts/hooks/ecc-metrics-bridge.js",
        "scripts/hooks/gateguard-fact-force.js",
        "scripts/hooks/governance-capture.js",
        "scripts/hooks/insaits-security-wrapper.js",
        "scripts/hooks/lifecycle-hook-bootstrap.js",
        "scripts/hooks/mcp-health-check.js",
        "scripts/hooks/plan-canvas-pending.js",
        "scripts/hooks/plan-canvas-sessions.js",
        "scripts/hooks/plugin-hook-bootstrap.js",
        "scripts/hooks/post-bash-build-complete.js",
        "scripts/hooks/post-bash-command-log.js",
        "scripts/hooks/post-bash-dispatcher.js",
        "scripts/hooks/post-bash-pr-created.js",
        "scripts/hooks/post-edit-typecheck.js",
        "scripts/hooks/posttooluse-dispatcher.js",
        "scripts/hooks/pre-bash-commit-quality.js",
        "scripts/hooks/pre-bash-dispatcher.js",
        "scripts/hooks/pre-bash-git-push-reminder.js",
        "scripts/hooks/pre-bash-tmux-reminder.js",
        "scripts/hooks/pre-write-doc-warn.js",
        "scripts/hooks/run-with-flags-shell.sh",
        "scripts/hooks/session-activity-tracker.js",
        "scripts/hooks/session-start-bootstrap.js",
        "scripts/hooks/skill-run-tracker.js",
    ]:
        _p24 = os.path.join(BASE, _f24)
        if exists(_p24):
            resub(_p24, r"Cursor-only", "Upstream-only", count=1)
    # D-2 specials (individual wording).
    f = os.path.join(BASE, "scripts/hooks/check-hook-enabled.js")
    if exists(f):
        sub(f, "Hook-enabled check — Cursor-only helper (not wired in this Cursor plugin — invoked only from Cursor hook configurations).",
            "Hook-enabled check — Upstream-only helper (not wired in this Cursor plugin — invoked only from upstream hook configurations).")
    f = os.path.join(BASE, "scripts/hooks/ecc-statusline.js")
    if exists(f):
        sub(f, "ECC Statusline — Cursor-only statusLine command (not wired in this Cursor plugin — registered in settings.json, reads stdin from the Cursor runtime)",
            "ECC Statusline — Upstream-only statusLine command (not wired in this Cursor plugin — registered in upstream settings.json, reads stdin from the host runtime)")
    f = os.path.join(BASE, "scripts/hooks/hookify-runtime.js")
    if exists(f):
        sub(f, "ECC-native Hookify runtime — Cursor-only (not wired in this Cursor plugin — reachable only via the unwired posttooluse-dispatcher.js)",
            "ECC-native Hookify runtime — PostToolUse-only (not wired in this Cursor plugin — reachable only via the unwired posttooluse-dispatcher.js)")
    # D-3: plankton-code-quality claims a Cursor PostToolUse hook that does
    # not exist (description :3 + pairing table :118).
    f = os.path.join(BASE, "skills/plankton-code-quality/SKILL.md")
    if exists(f):
        sub(f, "(Cursor only — uses PostToolUse hooks; the auto-fix subprocess was removed in fix #16, so Plankton reports violations instead of auto-fixing)",
            "(Upstream only — uses PostToolUse hooks, which Cursor does not have; the auto-fix subprocess was removed in fix #16, so Plankton reports violations instead of auto-fixing)")
        sub(f, "PostToolUse hooks (Prettier, tsc) — Cursor only; in Cursor, post-edit formatting via after-file-edit / stop hooks",
            "PostToolUse hooks (Prettier, tsc) — upstream only; in Cursor, post-edit formatting via after-file-edit / stop hooks")
    # D-4: learn.md labels PreToolUse/PostToolUse observation as Cursor's.
    f = os.path.join(BASE, "commands/learn.md")
    if exists(f):
        sub(f, "(PreToolUse/PostToolUse observation is Cursor-only — in Cursor only the Stop hook runs — and the background observer is disabled by default)",
            "(PreToolUse/PostToolUse observation is upstream-only — in Cursor only the Stop hook runs — and the background observer is disabled by default)")
    # D-5: continuous-learning-v2 labels PreToolUse/PostToolUse as Cursor's.
    f = os.path.join(BASE, "skills/continuous-learning-v2/SKILL.md")
    if exists(f):
        sub(f, "| Observation | Stop hook (session end) | PreToolUse/PostToolUse (Cursor only) |",
            "| Observation | Stop hook (session end) | PreToolUse/PostToolUse (upstream only) |")
        sub(f, "| Cursor hooks capture prompts + tool use (Cursor only)",
            "| Cursor hooks capture prompts + tool use (upstream only)")

    # --- moved from edit_prose_round2 (post-pass old text): scripts/lib/package-manager.js ---
    f = os.path.join(BASE, "scripts/lib/package-manager.js")
    if exists(f):
        sub(f, "// Config file path (host-aware agent data home: ~/.cursor/ecc in Cursor,\n// ~/.claude in Cursor — see scripts/lib/agent-data-home.js)",
            "// Config file path (host-aware agent data home: ~/.cursor/ecc —\n// see scripts/lib/agent-data-home.js)")

    # --- moved from edit_prose_round2 (post-pass old text): scripts/lib/package-manager.js ---
    f = os.path.join(BASE, "scripts/lib/package-manager.js")
    if exists(f):
        sub(f, " * Tries the host-aware config path first, then the explicit Cursor\n"
               " * (~/.cursor/package-manager.json) and Cursor\n"
               " * (~/.claude/package-manager.json) global paths.",
            " * Tries the host-aware config path first, then the explicit Cursor\n"
               " * (~/.cursor/package-manager.json) global path.")

    # --- moved from edit_prose_round2 (post-pass old text): scripts/lib/package-manager.js ---
    f = os.path.join(BASE, "scripts/lib/package-manager.js")
    if exists(f):
        sub(f, " * 1. Environment variable CURSOR_PACKAGE_MANAGER (Cursor) or\n"
               " *    CLAUDE_PACKAGE_MANAGER (Cursor)\n"
               " * 2. Project-specific config (.cursor/package-manager.json, then\n"
               " *    .ecc/package-manager.json)\n"
               " * 3. package.json packageManager field\n"
               " * 4. Lock file detection\n"
               " * 5. Global user preference (host-aware config path, then\n"
               " *    ~/.cursor/package-manager.json, then ~/.claude/package-manager.json)",
            " * 1. Environment variable CURSOR_PACKAGE_MANAGER\n"
               " * 2. Project-specific config (.cursor/package-manager.json)\n"
               " * 3. package.json packageManager field\n"
               " * 4. Lock file detection\n"
               " * 5. Global user preference (host-aware config path, then\n"
               " *    ~/.cursor/package-manager.json)")

    # --- moved from edit_prose_round2 (post-pass old text): scripts/lib/package-manager.js ---
    f = os.path.join(BASE, "scripts/lib/package-manager.js")
    if exists(f):
        sub(f, "  // 1. Check environment variable (Cursor first, then Cursor)\n"
               "  const envPm = process.env.CURSOR_PACKAGE_MANAGER || process.env.CLAUDE_PACKAGE_MANAGER;",
            "  // 1. Check environment variable\n"
               "  const envPm = process.env.CURSOR_PACKAGE_MANAGER;")

    # --- moved from edit_prose_round2 (post-pass old text): scripts/lib/package-manager.js ---
    f = os.path.join(BASE, "scripts/lib/package-manager.js")
    if exists(f):
        sub(f, " * Set user's preferred package manager (global). Saved to the host-aware\n"
               " * config path (getConfigPath): ~/.cursor/ecc/package-manager.json in Cursor,\n"
               " * ~/.claude/package-manager.json in Cursor. A preference saved at\n"
               " * ~/.cursor/package-manager.json or ~/.claude/package-manager.json is still\n"
               " * honoured on read (see loadConfig).",
            " * Set user's preferred package manager (global). Saved to the host-aware\n"
               " * config path (getConfigPath): ~/.cursor/ecc/package-manager.json. A\n"
               " * preference saved at ~/.cursor/package-manager.json is still honoured\n"
               " * on read (see loadConfig).")

    # --- moved from edit_prose_round2 (post-pass old text): scripts/lib/package-manager.js ---
    f = os.path.join(BASE, "scripts/lib/package-manager.js")
    if exists(f):
        sub(f, " * Set project's preferred package manager.\n"
               " * Saved to .cursor/package-manager.json (Cursor, this plugin's host). An\n"
               " * existing .ecc/package-manager.json is still honoured on read as a\n"
               " * fallback for Cursor installs (see getPackageManager step 2).",
            " * Set project's preferred package manager.\n"
               " * Saved to .cursor/package-manager.json (Cursor, this plugin's host).")

    # --- moved from edit_prose_round2 (post-pass old text): scripts/lib/package-manager.js ---
    f = os.path.join(BASE, "scripts/lib/package-manager.js")
    if exists(f):
        sub(f, "  message += '  - Global: Set CURSOR_PACKAGE_MANAGER (Cursor) or CLAUDE_PACKAGE_MANAGER (Cursor) environment variable\\n';\n"
               "  message += '  - Or add to ~/.cursor/package-manager.json or ~/.claude/package-manager.json: {\"packageManager\": \"pnpm\"}\\n';",
            "  message += '  - Global: Set CURSOR_PACKAGE_MANAGER environment variable\\n';\n"
               "  message += '  - Or add to ~/.cursor/package-manager.json: {\"packageManager\": \"pnpm\"}\\n';")

    # --- moved from edit_prose_round2 (post-pass old text): scripts/setup-package-manager.js ---
    f = os.path.join(BASE, "scripts/setup-package-manager.js")
    if exists(f):
        sub(f, "                  ~/.cursor/ecc/package-manager.json in Cursor,\n"
               "                  ~/.claude/package-manager.json in Cursor;\n"
               "                  ~/.cursor/package-manager.json is also read as a fallback)",
            "                  ~/.cursor/ecc/package-manager.json;\n"
               "                  ~/.cursor/package-manager.json is also read as a fallback)")

    # --- moved from edit_prose_round2 (post-pass old text): skills/tdd-workflow/SKILL.md ---
    sub(os.path.join(BASE, "skills/tdd-workflow/SKILL.md"),
        "It resolves the package manager (npm / pnpm / yarn / bun) from, in order: `CURSOR_PACKAGE_MANAGER` (Cursor) or `CLAUDE_PACKAGE_MANAGER` (Cursor), then `.cursor/package-manager.json` then `.ecc/package-manager.json`, then the `package.json` `packageManager` field, then the lockfile, then global config.",
        "It resolves the package manager (npm / pnpm / yarn / bun) from, in order: `CURSOR_PACKAGE_MANAGER`, then `.cursor/package-manager.json` then `.ecc/package-manager.json`, then the `package.json` `packageManager` field, then the lockfile, then global config.")

    # --- moved from edit_prose_round2 (post-pass old text): commands/setup-pm.md ---
    f = os.path.join(BASE, "commands/setup-pm.md")
    if exists(f):
        sub(f, "1. **Environment variable**: `CURSOR_PACKAGE_MANAGER` (Cursor) or `CLAUDE_PACKAGE_MANAGER` (Cursor)",
            "1. **Environment variable**: `CURSOR_PACKAGE_MANAGER`")

    # --- moved from edit_prose_round2 (post-pass old text): commands/setup-pm.md ---
    f = os.path.join(BASE, "commands/setup-pm.md")
    if exists(f):
        sub(f, "5. **Global config**: host-aware config path (`~/.cursor/ecc/package-manager.json` in Cursor, `~/.claude/package-manager.json` in Cursor), then `~/.cursor/package-manager.json`, then `~/.claude/package-manager.json`",
            "5. **Global config**: host-aware config path (`~/.cursor/ecc/package-manager.json`), then `~/.cursor/package-manager.json`")

    # --- moved from edit_prose_round2 (post-pass old text): commands/setup-pm.md ---
    f = os.path.join(BASE, "commands/setup-pm.md")
    if exists(f):
        sub(f, "// Cursor: ~/.cursor/ecc/package-manager.json\n// (also read from ~/.cursor/package-manager.json)\n// Cursor: ~/.claude/package-manager.json\n",
            "// Cursor: ~/.cursor/ecc/package-manager.json\n// (also read from ~/.cursor/package-manager.json)\n")

    # --- moved from edit_prose_round2 (post-pass old text): commands/setup-pm.md ---
    f = os.path.join(BASE, "commands/setup-pm.md")
    if exists(f):
        sub(f, "// Cursor: .cursor/package-manager.json\n// (an existing .ecc/package-manager.json is still honoured on read)\n",
            "// Cursor: .cursor/package-manager.json\n")

    # --- moved from edit_prose_round2 (post-pass old text): commands/setup-pm.md ---
    f = os.path.join(BASE, "commands/setup-pm.md")
    if exists(f):
        sub(f, "Set `CURSOR_PACKAGE_MANAGER` (Cursor) or `CLAUDE_PACKAGE_MANAGER` (Cursor\nCode) to override all other detection methods. The Cursor variable takes\nprecedence when both are set:",
            "Set `CURSOR_PACKAGE_MANAGER` to override all other detection methods:")

    # --- moved from edit_prose_round2 (post-pass old text): skills/design-taste-frontend/references/gate.md ---
    # (tolerant: the fix-up round scrubbed this paragraph from the staged
    # source, so the post-generic-pass anchor may already be gone.)
    f = os.path.join(BASE, "skills/design-taste-frontend/references/gate.md")
    if exists(f):
        sub_if_new_present(f, "command is one POSIX `sh` line (Git Bash on Windows — prerequisite: the hook needs Git Bash installed; whether it fires at all on Windows without Git Bash is untested, OWED to the live smoke test — `sh` on macOS and Linux) that runs the first\n`gate.mjs` it finds, in this order: `$CLAUDE_SKILL_DIR/scripts/`, `$ECC_PLUGIN_ROOT/scripts/` and\n`$ECC_PLUGIN_ROOT/skills/design-taste-frontend/scripts/` (a plugin install), each only when the variable is\nset; then the install folders by name, `$CLAUDE_PROJECT_DIR/.claude/skills/design-taste-frontend/`,\n`$CLAUDE_PROJECT_DIR/.agents/skills/design-taste-frontend/`, `~/.claude/skills/design-taste-frontend/`\nand `~/.agents/skills/design-taste-frontend/` (`npx skills`, `install.sh`).",
            "command is one POSIX `sh` line (Git Bash on Windows — prerequisite: the hook needs Git Bash installed; whether it fires at all on Windows without Git Bash is untested, OWED to the live smoke test — `sh` on macOS and Linux) that runs the first\n`gate.mjs` it finds, in this order: `$ECC_PLUGIN_ROOT/skills/design-taste-frontend/scripts/`,\n`$ECC_PLUGIN_ROOT/scripts/` (a plugin install), each only when the variable is set; then the\ninstall folders by name, `$CURSOR_PROJECT_DIR/.cursor/skills/design-taste-frontend/`,\n`$CURSOR_PROJECT_DIR/.agents/skills/design-taste-frontend/`, `~/.cursor/skills/design-taste-frontend/`\nand `~/.agents/skills/design-taste-frontend/` (`npx skills`, `install.sh`).")

    # --- moved from edit_prose_round2 (post-pass old text): skills/unified-memory/SKILL.md ---
    f = os.path.join(BASE, "skills/unified-memory/SKILL.md")
    if exists(f):
        sub(f, "description: Share durable, inspectable context and handoffs between Cursor, Codex, Hermes, Cursor, OpenCode, and other agents through the local ECC Memory Vault.",
            "description: Share durable, inspectable context and handoffs between Cursor agents through the local ECC Memory Vault.")

    # --- moved from edit_prose_round2 (post-pass old text): skills/unified-memory/SKILL.md ---
    f = os.path.join(BASE, "skills/unified-memory/SKILL.md")
    if exists(f):
        sub(f, "- Hand work from Cursor to Codex, Hermes to Cursor, or any other harness pair.",
            "- Hand work between Cursor agents in the same project.")

    # --- moved from edit_prose_round2 (post-pass old text): skills/context-budget/SKILL.md ---
    f = os.path.join(BASE, "skills/context-budget/SKILL.md")
    if exists(f):
        sub(f, "description: Routes live context checks to the native Codex or Cursor meter without scanning files, and performs a bounded static component audit only when explicitly requested.",
            "description: Routes live context checks to the native Cursor meter without scanning files, and performs a bounded static component audit only when explicitly requested.")

    # --- moved from edit_prose_round2 (post-pass old text): skills/context-budget/SKILL.md ---
    f = os.path.join(BASE, "skills/context-budget/SKILL.md")
    if exists(f):
        sub(f, "These commands are documented in the [Codex command reference](https://developers.openai.com/codex/cli/slash-commands) and [Cursor command reference](https://code.claude.com/docs/en/commands).",
            "These commands are documented in the Cursor command reference.")

    # --- moved from edit_prose_round2 (post-pass old text): skills/app-scaffold/SKILL.md ---
    sub(os.path.join(BASE, "skills/app-scaffold/SKILL.md"),
        "- **Reuse across projects:** copy this `app-scaffold/` folder into any project's `.cursor/skills/` (Cursor) or `.ecc/skills/` (Cursor), or drop it in `~/.cursor/skills/` or `~/.claude/skills/` to make it available in *every* project on your machine.",
        "- **Reuse across projects:** copy this `app-scaffold/` folder into any project's `.cursor/skills/` or `.ecc/skills/`, or drop it in `~/.cursor/skills/` to make it available in *every* project on your machine.")

    # --- moved from edit_prose_round2 (post-pass old text): skills/skill-scout/SKILL.md ---
    f = os.path.join(BASE, "skills/skill-scout/SKILL.md")
    if exists(f):
        sub(f, "# Cursor (this skill also works there) — same searches under ~/.claude\nfind ~/.claude/skills -maxdepth 2 -name SKILL.md 2>/dev/null | grep -iE \"keyword|synonym\"\nfind ~/.claude/plugins/marketplaces -path '*/skills/*/SKILL.md' 2>/dev/null | grep -iE \"keyword|synonym\"",
            "# Cursor — same searches under ~/.cursor\nfind ~/.cursor/skills -maxdepth 2 -name SKILL.md 2>/dev/null | grep -iE \"keyword|synonym\"\nfind ~/.cursor/plugins/marketplaces -path '*/skills/*/SKILL.md' 2>/dev/null | grep -iE \"keyword|synonym\"")

    # --- moved from edit_prose_round2 (post-pass old text): skills/codehealth-mcp/SKILL.md ---
    sub(os.path.join(BASE, "skills/codehealth-mcp/SKILL.md"),
        "**Cursor** (`~/.claude.json` → `mcpServers`):",
        "**Cursor** (`~/.cursor/mcp.json` → `mcpServers`):")

    # --- moved from edit_prose_round2 (post-pass old text): skills/ck/SKILL.md ---
    f = os.path.join(BASE, "skills/ck/SKILL.md")
    if exists(f):
        sub(f, "(Cursor only — this skill uses Cursor's SessionStart hook and ~/.claude/ck storage; it does not work in Cursor.)",
            "(Cursor only — this skill uses Cursor's SessionStart hook and ~/.cursor/ecc/ck storage.)")

    # --- moved from edit_prose_round2 (post-pass old text): skills/ck/SKILL.md ---
    f = os.path.join(BASE, "skills/ck/SKILL.md")
    if exists(f):
        sub(f, "> **Cursor only** — this skill uses Cursor's SessionStart hook and ~/.claude/ck storage; it does not work in Cursor.",
            "> **Cursor only** — this skill uses Cursor's SessionStart hook and ~/.cursor/ecc/ck storage.")

    # --- moved from edit_prose_round2 (post-pass old text): skills/strategic-compact/SKILL.md ---
    f = os.path.join(BASE, "skills/strategic-compact/SKILL.md")
    if exists(f):
        sub(f, "- `CLAUDE_CODE_AUTO_COMPACT_WINDOW` — Cursor's native auto-compact trigger, which may be smaller than the model's context window. For context-window resolution, ECC uses it only as a last-resort fallback, after an explicit ECC override, a `[1m]` model marker, a known large-window model family, and inference from observed tokens above 200k. It is not an exact model-capacity declaration.",
            "- `ECC_CONTEXT_WINDOW_TOKENS` — an explicit override for the context window, used when the host's native auto-compact trigger does not match the model's capacity. For context-window resolution, ECC consults it first, then a `[1m]` model marker, then inference from observed tokens above 200k. The transcript-context model-family table was removed in fix #16 — no model name is consulted.")

    # --- moved from edit_prose_round2 (post-pass old text): skills/strategic-compact/SKILL.md ---
    f = os.path.join(BASE, "skills/strategic-compact/SKILL.md")
    if exists(f):
        sub(f, "- Same rules in both `~/.claude/rules/` and project `.ecc/rules/`",
            "- Same rules in both `~/.cursor/rules/` and project `.ecc/rules/`")

    # --- sweep #17 M1/M2 (generic-pass version-suffix residue, build 15) ---
    # strategic-compact has no staged copy (upstream ECC skill copied by
    # build.sh; audited at build.sh:1015, :6844, :13025), so both fixes live
    # here, post-generic. M1: the generic pass turned "400k Opus 4.x" (audit
    # NEW text, build.sh:6925) into "400k Grok 4.7 High" once the Opus 4.x
    # regex above covered the literal "4.x"; this sub fixes the wrong
    # "400k" figure (Grok 4.7 High's verified window is 256k standard /
    # 500k long context — 500k is the long-context figure). M2: the generic
    # pass turned "Sonnet 5" into "Grok 4.6 High Fast 5" (bare Sonnet rule
    # has no version handling); drop the stray " 5". No broad
    # version-stripping rule is added: stripping digits after a Grok name
    # would corrupt "Grok 4.7 High" itself.
    f = os.path.join(BASE, "skills/strategic-compact/SKILL.md")
    if exists(f):
        sub(f, "(e.g. 400k Grok 4.7 High, or a new 1M-window model family)",
            "(e.g. 500k Grok 4.7 High, or a new 1M-window model family)")
        sub(f, "on Grok 4.7 High, Grok 4.6 High Fast 5,",
            "on Grok 4.7 High, Grok 4.6 High Fast,")

    # --- moved from edit_prose_round2 (post-pass old text): skills/continuous-learning-v2/SKILL.md ---
    f = os.path.join(BASE, "skills/continuous-learning-v2/SKILL.md")
    if exists(f):
        sub(f, "Continuous-learning-v2 stores observer data outside `~/.claude` so Cursor's sensitive-path guard does not block background instinct writes:",
            "Continuous-learning-v2 stores observer data under `~/.local/share/ecc-homunculus/` (outside the agent's config directory) so the agent's sensitive-path guard does not block background instinct writes:")

    # --- moved from edit_prose_round2 (post-pass old text): skills/continuous-learning-v2/SKILL.md ---
    f = os.path.join(BASE, "skills/continuous-learning-v2/SKILL.md")
    if exists(f):
        sub(f, "**If installed manually in Cursor** to `~/.claude/skills`, add this to your `~/.claude/settings.json`:",
            "**If installed manually** to `~/.cursor/skills`, add this to your hook config:")

    # --- moved from edit_prose_round2 (post-pass old text): skills/continuous-learning-v2/hooks/observe.sh ---
    f = os.path.join(BASE, "skills/continuous-learning-v2/hooks/observe.sh")
    if exists(f):
        sub(f, "# wrapper's positional phase argument, but Cursor still exposes the hook\n"
               "# event name in CLAUDE_HOOK_EVENT_NAME.  Fall back to that env var before\n"
               "# defaulting to post so manually registered PreToolUse hooks are recorded as\n"
               "# tool_start instead of being silently misclassified as tool_complete.",
            "# wrapper's positional phase argument, but the hook event name is\n"
               "# available in ECC_HOOK_EVENT_NAME.  Fall back to that env var before\n"
               "# defaulting to post so manually registered PreToolUse hooks are recorded as\n"
               "# tool_start instead of being silently misclassified as tool_complete.")

    # --- session-guardian.sh edit REMOVED (D13 follow-up): the file is now
    # deleted by do_deletes(), so the reword below would target a missing file.
    # (Was: "# Called by observer-loop.sh before spawning any Cursor session."
    #  -> "# Called by observer-loop.sh before spawning any agent session.")

    # --- security-scan: delete the Deep Analysis section ---
    REMOVALS.append("skills/security-scan/SKILL.md 'Grok 4.7 High Deep Analysis' section — "
                    "the ANTHROPIC_API_KEY / npx ecc-agentshield scan --opus pipeline has no "
                    "verified Grok equivalent; the rest of the skill is unchanged (fix #16)")

    # --- security-scan: delete the Deep Analysis section (heading to the
    # end of the numbered list that follows it) ---
    f = os.path.join(BASE, "skills/security-scan/SKILL.md")
    if exists(f):
        text = read(f)
        start = text.find("### Grok 4.7 High Deep Analysis")
        if start < 0:
            ERRORS.append(f"{rel(f)}: security-scan Deep Analysis heading not found")
        else:
            # The section ends at the Auditor line (the last item of the
            # numbered list), plus following blank lines.
            end_marker = "3. **Auditor (Final Verdict)** — synthesizes both perspectives"
            end = text.find(end_marker, start)
            if end < 0:
                ERRORS.append(f"{rel(f)}: security-scan Deep Analysis list end not found")
            else:
                end = text.find("\n", end) + 1
                # Swallow following blank lines.
                while end < len(text) and text[end] == "\n":
                    end += 1
                write(f, text[:start] + text[end:])
                CHANGES.append("skills/security-scan/SKILL.md — Deep Analysis section removed")

    # --- new stragglers (old texts verified against the build-2 tree) ---
    # gan-style-harness: :30 CLI-subprocess line; :208 Results intro;
    # :222-223 reference lines (URLs dropped; the Anthropic title is
    # de-branded so the self-check stays at zero "anthropic" hits — the
    # Epsilla title keeps its name, it carries no banned term).
    f = os.path.join(BASE, "skills/gan-style-harness/SKILL.md")
    if exists(f):
        sub(f, "- Quick single-file fixes (Cursor only — use standard `claude -p` there; in this plugin use the Cursor agent loop, never `claude -p`)",
            "- Quick single-file fixes (use the Cursor agent loop, never a CLI subprocess)")
        sub(f, "Based on Anthropic's published results:",
            "Based on the upstream harness paper's published results:")
        sub(f, "- [Anthropic: Harness Design for Long-Running Apps](https://www.anthropic.com/engineering/harness-design-long-running-apps) — Original paper by Prithvi Rajasekaran",
            "- Harness Design for Long-Running Apps (upstream multi-agent harness design paper) — Original paper by Prithvi Rajasekaran")
        sub(f, "- [Epsilla: The GAN-Style Agent Loop](https://www.epsilla.com/blogs/anthropic-harness-engineering-multi-agent-gan-architecture) — Architecture deconstruction",
            "- Epsilla: The GAN-Style Agent Loop — Architecture deconstruction")

    # gan agent description parentheticals (all three carry the same line)
    for ag in ("ecc-gan-planner.md", "ecc-gan-generator.md", "ecc-gan-evaluator.md"):
        f = os.path.join(BASE, "agents", ag)
        if exists(f):
            resub(f, r"the upstream `claude -p` path is Cursor only and is never executed here",
                  "the upstream CLI-subprocess path is never executed here", count=1)

    # laravel / council / mcp-health-check one-liners
    sub(os.path.join(BASE, "skills/laravel-plugin-discovery/SKILL.md"),
        "In Cursor, add the same entry to your `~/.claude.json` `mcpServers`",
        "In Cursor, add the same entry to your `~/.cursor/mcp.json` `mcpServers`")
    sub(os.path.join(BASE, "skills/council/SKILL.md"),
        "Do **not** write ad-hoc notes to `~/.claude/notes` or other shadow paths from this skill.",
        "Do **not** write ad-hoc notes to the agent's notes directory or other shadow paths from this skill.")
    sub(os.path.join(BASE, "scripts/hooks/mcp-health-check.js"),
        "// `~/.claude-work` resolves to one place rather than two.",
        "// `~/some-dir` resolves to one place rather than two.")

    # ck code files: claudeMd -> agentsMd, ~/.claude re-point, CLAUDE_SKILL_DIR
    f = os.path.join(BASE, "skills/ck/commands/init.mjs")
    if exists(f):
        resub(f, r"\bclaudeMd\b", "agentsMd", count=7)
    f = os.path.join(BASE, "skills/ck/commands/shared.mjs")
    if exists(f):
        sub(f, "resolve(homedir(), '.claude', 'ck')",
            "resolve(homedir(), '.cursor', 'ecc', 'ck')")
        sub(f, "resolve(homedir(), '.claude', 'projects', encoded, 'memory')",
            "resolve(homedir(), '.cursor', 'ecc', 'projects', encoded, 'memory')")
    f = os.path.join(BASE, "skills/ck/hooks/session-start.mjs")
    if exists(f):
        sub(f, "resolve(homedir(), '.claude', 'ck')",
            "resolve(homedir(), '.cursor', 'ecc', 'ck')")
        sub(f, "// Resolve SKILL.md next to this hook, so plugin installs work as well as ~/.claude/skills/ck.",
            "// Resolve SKILL.md next to this hook, so plugin installs work as well as ~/.cursor/skills/ck.")
        resub(f, r"\bextractClaudeMdGoal\b", "extractAgentsMdGoal", count=2)
        resub(f, r"\bclaudeMdGoal\b", "agentsMdGoal", count=4)
        sub(f, "// The host does not expand ${CLAUDE_SKILL_DIR} in hook output, so fill it in here.",
            "// The host does not expand ${ECC_PLUGIN_ROOT}/skills/ck in hook output, so fill it in here.")
        sub(f, ".replaceAll('${CLAUDE_SKILL_DIR}', () => shellSkillDir)",
            ".replaceAll('${ECC_PLUGIN_ROOT}/skills/ck', () => shellSkillDir)")

    # opensource-packager fence line, evolve homunculus line, sessions alias path
    sub(os.path.join(BASE, "agents/ecc-opensource-packager.md"),
        "claude    # Start Cursor — reads AGENTS.md automatically",
        "# Start Cursor in this project — it reads AGENTS.md automatically")
    sub(os.path.join(BASE, "commands/evolve.md"),
        "   - Legacy data under `~/.claude/homunculus/` is not read; migrate it once with `skills/continuous-learning-v2/scripts/migrate-homunculus.sh`.",
        "   - Legacy homunculus data is not read (the migration script was removed in fix #16).")
    sub(os.path.join(BASE, "commands/sessions.md"),
        "- Aliases are stored in `~/.claude/session-aliases.json` (Cursor only)",
        "- Aliases are stored in `~/.cursor/ecc/session-aliases.json` (Cursor only)")

    # gate.md Codex section (bold text, not a heading — delete by span).
    # Tolerates the section already being gone: the fix-up round scrubbed
    # it from the staged source, so a rebuild stages it removed.
    f = os.path.join(BASE, "skills/design-taste-frontend/references/gate.md")
    if exists(f):
        text = read(f)
        start = text.find("**Codex**, `.codex/hooks.json`")
        if start < 0:
            NOTES.append(f"{rel(f)}: gate.md Codex section already removed at staged source, skipped")
        else:
            end = text.find("\n```\n", start)
            if end < 0:
                ERRORS.append(f"{rel(f)}: gate.md Codex section fence end not found")
            else:
                end = end + len("\n```\n")
                while end < len(text) and text[end] == "\n":
                    end += 1
                write(f, text[:start] + text[end:])
                CHANGES.append("skills/design-taste-frontend/references/gate.md — Codex hooks section removed")

    # D14: the Qwen agent-adaptation preflight is dead — qwen-adapt-agents.js
    # is deleted, so no operation can carry the 'qwen-agent-frontmatter'
    # transform (content-transform.js throws on any named transform).
    f = os.path.join(BASE, "scripts/lib/install/apply.js")
    if exists(f):
        remove_function(f, "preflightQwenAgentOperations")
        resub(f, r"  preflightQwenAgentOperations\(plan\);\n", "", count=2)
        sub(f, "// 'remove-claude-settings-hooks' removal both targeted host",
            "// settings-hooks removal both targeted host")
    f = os.path.join(BASE, "scripts/lib/install-lifecycle.js")
    if exists(f):
        sub(f, "  // update-claude-settings operations, which Cursor installs never",
            "  // host settings-update operations, which Cursor installs never")

    # demo.html: drop the 4 removed-brand icon chips, fix the AI count
    # (tolerant: the fix-up round scrubbed the chips from the staged source)
    f = os.path.join(BASE, "skills/design-taste-frontend/assets/icons/demo.html")
    if exists(f):
        resub_if_present(f, r'<span class="ic-chip" title="(anthropic|claude|claude-code|codex)">.*?</span>', "", count=4)
        sub_if_new_present(f, 'AI <span class="muted">53</span>', 'AI <span class="muted">49</span>')

    # plankton: /model opus pin + subprocess tier keys (pin contexts).
    # haiku + sonnet collapse into the single fast slug (duplicate JSON
    # keys are not allowed); sonnet's 300s timeout is kept for the merged
    # fast tier, opus-tier keeps 600s on grok-4.7-high.
    f = os.path.join(BASE, "skills/plankton-code-quality/SKILL.md")
    if exists(f):
        sub(f, "| Model routing | Manual (`/model opus`) | Automatic (violation complexity → tier) |",
            "| Model routing | Manual (`/model grok-4.7-high`) | Automatic (violation complexity → tier) |")
        sub(f, '      "haiku":  { "timeout": 120, "max_turns": 10 },\n'
               '      "sonnet": { "timeout": 300, "max_turns": 10 },\n'
               '      "opus":   { "timeout": 600, "max_turns": 15 }',
            '      "cursor-grok-4.6-high-fast": { "timeout": 300, "max_turns": 10 },\n'
            '      "grok-4.7-high":   { "timeout": 600, "max_turns": 15 }')


    # --- wave 2: stragglers found by the dry-run self-check (113 claude /
    # 38 codex / 2 anthropic hits on the build-2 tree + post-generic phase).
    # Files whose round-2 fixes already cover them (harness tables, lifecycle
    # hydrate block, apply.js assertSafe/preflight lines, runtime
    # claudeRulesDir, helpers.js require, context-profile run branch,
    # agent-tool-map exports) are NOT repeated here — build 3 handles them.
    # --- auto-update: drop the legacy package name from the trust set (D11:
    # legacy everything-claude-code installs are no longer auto-detected).
    f = os.path.join(BASE, "scripts/auto-update.js")
    if exists(f):
        sub(f, "// 'everything-claude-code' is the legacy 1.x package name, kept for existing checkouts.\n", "")
        sub(f, "const ECC_PACKAGE_NAMES = new Set(['ecc-universal', 'everything-claude-code']);",
            "const ECC_PACKAGE_NAMES = new Set(['ecc-universal']);")

    # --- hook-flags: drop the Claude Code plugin-option env fallbacks.
    # The plugin's own ECC_HOOKS_ENABLED / ECC_HOOK_PROFILE vars (checked
    # first) and the managed config remain; the CLAUDE_PLUGIN_OPTION_*
    # vars do not exist in Cursor.
    f = os.path.join(BASE, "scripts/lib/hook-flags.js")
    if exists(f):
        sub(f, "  const raw = env.ECC_HOOKS_ENABLED !== undefined\n"
               "    ? env.ECC_HOOKS_ENABLED\n"
               "    : (\n"
               "      env.CLAUDE_PLUGIN_OPTION_HOOKS_ENABLED !== undefined\n"
               "        ? env.CLAUDE_PLUGIN_OPTION_HOOKS_ENABLED\n"
               "        : managed.enabled\n"
               "    );",
            "  const raw = env.ECC_HOOKS_ENABLED !== undefined\n"
            "    ? env.ECC_HOOKS_ENABLED\n"
            "    : managed.enabled;")
        sub(f, "  const selected = env.ECC_HOOK_PROFILE !== undefined\n"
               "    ? env.ECC_HOOK_PROFILE\n"
               "    : (\n"
               "      env.CLAUDE_PLUGIN_OPTION_HOOK_PROFILE !== undefined\n"
               "        ? env.CLAUDE_PLUGIN_OPTION_HOOK_PROFILE\n"
               "        : managed.profile\n"
               "    );",
            "  const selected = env.ECC_HOOK_PROFILE !== undefined\n"
            "    ? env.ECC_HOOK_PROFILE\n"
            "    : managed.profile;")

    # --- context-carrier schema: narrow the layout enums to cursor-only.
    f = os.path.join(BASE, "schemas/context-carrier.schema.json")
    if exists(f):
        sub(f, '              "enum": [\n'
               '                "pi-package@1",\n'
               '                "opencode-project@1",\n'
               '                "cursor-project@1"\n'
               '              ]',
            '              "enum": [\n'
            '                "cursor-project@1"\n'
            '              ]')
        sub(f, '              "enum": [\n'
               '                "skills",\n'
               '                ".opencode/skills",\n'
               '                ".cursor/skills"\n'
               '              ]',
            '              "enum": [\n'
            '                ".cursor/skills"\n'
            '              ]')
        sub(f, '              "enum": [\n'
               '                null,\n'
               '                ".ecc-plugin/plugin.json",\n'
               '                ".codex-plugin/plugin.json",\n'
               '                "package.json"\n'
               '              ]',
            '              "enum": [\n'
            '                null\n'
            '              ]')

    # --- session-adapters registry header comment (my own rewrite's note)
    f = os.path.join(BASE, "scripts/lib/session-adapters/registry.js")
    if exists(f):
        sub(f, "// fix #16 (D10/F2): session adapters are dmux-tmux only. The Cursor-history,\n"
               "// Codex-worktree and OpenCode adapters (and their transcript/history readers)\n"
               "// were deleted with their host modules.",
            "// fix #16 (D10/F2): session adapters are dmux-tmux only. The other host\n"
            "// adapters (and their transcript/history readers) were deleted with\n"
            "// their host modules.")

    # --- install-targets/helpers.js: narrow the platform-owner map to
    # cursor-only (D10); reword the .agents exclusion comment; drop the
    # dangling planClaudeHooksOperations export (function deleted in round 2,
    # the shorthand export would throw ReferenceError at load time).
    f = os.path.join(BASE, "scripts/lib/install-targets/helpers.js")
    if exists(f):
        sub(f, "const PLATFORM_SOURCE_PATH_OWNERS = Object.freeze({\n"
               "  '.claude-plugin': 'claude',\n"
               "  '.codex': 'codex',\n"
               "  '.cursor': 'cursor',\n"
               "  '.gemini': 'gemini',\n"
               "  '.hermes': 'hermes',\n"
               "  '.kimi': 'kimi',\n"
               "  '.kimi-code': 'kimi',\n"
               "  '.joycode': 'joycode',\n"
               "  '.opencode': 'opencode',\n"
               "  '.openclaw': 'openclaw',\n"
               "  // Pi loads ECC through `pi install`, not install-apply, so `.pi` is\n"
               "  // foreign to every install target.\n"
               "  '.pi': 'pi',\n"
               "  '.codebuddy': 'codebuddy',\n"
               "  '.qwen': 'qwen',\n"
               "  '.zed': 'zed',\n"
               "  '.adal': 'adal',\n"
               "});",
            "const PLATFORM_SOURCE_PATH_OWNERS = Object.freeze({\n"
            "  '.cursor': 'cursor',\n"
            "});")
        sub(f, "// Source paths that home installs must never copy into a harness home\n"
               "// directory. `.agents` is ECC's repo-local skills/plugins staging area:\n"
               "// project targets such as kimi and antigravity consume it, but neither\n"
               "// Cursor nor Codex reads a `.agents` directory under ~/.claude or\n"
               "// ~/.codex, so copying it there produces unread files that doctor flags as\n"
               "// drift and repair keeps restoring.",
            "// Source paths that home installs must never copy into a harness home\n"
            "// directory. `.agents` is ECC's repo-local skills/plugins staging area.\n"
            "// Cursor does not read a `.agents` directory under ~/.cursor, so copying\n"
            "// it there produces unread files that doctor flags as drift and repair\n"
            "// keeps restoring.")
        sub(f, "  planClaudeHooksOperations,\n", "")

    # --- harness tables: leftovers the entry removals do not cover.
    f = os.path.join(BASE, "scripts/lib/harness-adapter-compliance.js")
    if exists(f):
        sub(f, "// rules/common/, .claude-plugin/plugin.json,",
            "// rules/common/,")

    # --- agent-tool-map: claudeTool parameter name -> cursorTool
    f = os.path.join(BASE, "scripts/lib/agent-tool-map.js")
    if exists(f):
        resub(f, r"\bclaudeTool\b", "cursorTool", count=3)

    # --- one-line comment rewords
    sub(os.path.join(BASE, "scripts/lib/install/guarded-write.js"),
        "// claude-settings-lock module; it is a generic dev+ino comparison.",
        "// file-lock module; it is a generic dev+ino comparison.")
    sub(os.path.join(BASE, "scripts/lib/resolve-ecc-root.js"),
        "  // otherwise a scripts-only ~/.claude short-circuits and every skill path",
        "  // otherwise a scripts-only agent-data short-circuits and every skill path")
    sub(os.path.join(BASE, "scripts/lib/resolve-ecc-root.js"),
        "  // is no ~/.claude and no ECC_PLUGIN_ROOT, so all the probing above",
        "  // is no agent data home and no ECC_PLUGIN_ROOT, so all the probing above")

    # --- gateguard cluster (live: bash-hook-dispatcher, run-with-flags,
    # governance-capture). Established renames only; no behaviour change.
    f = os.path.join(BASE, "scripts/lib/gateguard-turn-scan.js")
    if exists(f):
        sub(f, "/** Transcript path from the hook payload or CLAUDE_TRANSCRIPT_PATH; '' when none. */",
            "/** Transcript path from the hook payload or ECC_TRANSCRIPT_PATH; '' when none. */")
        sub(f, "process.env.CLAUDE_TRANSCRIPT_PATH",
            "process.env.ECC_TRANSCRIPT_PATH")
    f = os.path.join(BASE, "scripts/lib/gateguard-target-class.js")
    if exists(f):
        sub(f, "const INSTRUCTION_BASENAMES = new Set([\n"
               "  'claude.md',\n"
               "  'agents.md',\n"
               "  'agent.md',\n"
               "  'gemini.md',\n"
               "  'skill.md',\n"
               "  'copilot-instructions.md',\n"
               "  '.cursorrules',\n"
               "  '.windsurfrules'\n"
               "]);",
            "const INSTRUCTION_BASENAMES = new Set([\n"
            "  'agents.md',\n"
            "  'agent.md',\n"
            "  'skill.md',\n"
            "  '.cursorrules'\n"
            "]);")
        sub(f, "const INSTRUCTION_DIRS = new Set(['.claude', 'agents', 'commands', 'skills', 'rules', 'hooks', '.cursor', '.codex', '.opencode']);",
            "const INSTRUCTION_DIRS = new Set(['agents', 'commands', 'skills', 'rules', 'hooks', '.cursor', '.ecc']);")
        sub(f, "const WORKTREE_PREFIX_PATTERN = /^\\.claude\\/worktrees\\/([^/]+)\\//;",
            "const WORKTREE_PREFIX_PATTERN = /^\\.ecc\\/worktrees\\/([^/]+)\\//;")
        resub(f, r"process\.env\.CLAUDE_PROJECT_DIR", "process.env.CURSOR_PROJECT_DIR", count=2)
        sub(f, "  return fs.existsSync(paths.join(rootNative, '.claude', 'worktrees', name, '.git'));",
            "  return fs.existsSync(paths.join(rootNative, '.ecc', 'worktrees', name, '.git'));")
        sub(f, "  loader: 'Name the harness/loader that reads this file (Cursor, Codex, Cursor, OpenCode, …) and when it loads it',",
            "  loader: 'Name the harness/loader that reads this file (Cursor, …) and when it loads it',")
    f = os.path.join(BASE, "scripts/lib/gateguard-search-evidence.js")
    if exists(f):
        sub(f, "process.env.CLAUDE_PROJECT_DIR",
            "process.env.CURSOR_PROJECT_DIR")
    f = os.path.join(BASE, "scripts/hooks/gateguard-fact-force.js")
    if exists(f):
        resub(f, r"process\.env\.CLAUDE_PROJECT_DIR", "process.env.CURSOR_PROJECT_DIR", count=2)
        sub(f, "const transcriptPath = (data && (data.transcript_path || data.transcriptPath)) || process.env.CLAUDE_TRANSCRIPT_PATH;",
            "const transcriptPath = (data && (data.transcript_path || data.transcriptPath)) || process.env.ECC_TRANSCRIPT_PATH;")
        # The settings-file exemption: .claude/settings*.json -> the
        # plugin's project-local settings (.ecc/settings*.json).
        sub(f, "function isClaudeSettingsPath(filePath) {\n"
               "  const normalized = normalizeForMatch(filePath);\n"
               "  return /(^|\\/)\\.claude\\/settings(?:\\.[^/]+)?\\.json$/.test(normalized);\n"
               "}",
            "function isAgentSettingsPath(filePath) {\n"
            "  const normalized = normalizeForMatch(filePath);\n"
            "  return /(^|\\/)\\.ecc\\/settings(?:\\.[^/]+)?\\.json$/.test(normalized);\n"
            "}")
        resub(f, r"\bisClaudeSettingsPath\b", "isAgentSettingsPath", count=2)
        sub(f, "  if (isAgentSettingsPath(filePath)) return 'claude-settings';",
            "  if (isAgentSettingsPath(filePath)) return 'agent-settings';")

    # --- context-profile defaults: codex -> cursor (the carrier layouts
    # now only have cursor, so the defaults must be cursor).
    f = os.path.join(BASE, "scripts/lib/context-selection.js")
    if exists(f):
        resub(f, r"target = 'codex'", "target = 'cursor'", count=2)
    f = os.path.join(BASE, "scripts/lib/context-profiles.js")
    if exists(f):
        resub(f, r"target = 'codex'", "target = 'cursor'", count=2)
    f = os.path.join(BASE, "scripts/lib/context-profile-support.js")
    if exists(f):
        resub(f, r"target = 'codex'", "target = 'cursor'", count=1)
    f = os.path.join(BASE, "scripts/lib/context-pack-registry.js")
    if exists(f):
        resub(f, r"target = 'codex'", "target = 'cursor'", count=1)

    # --- .d.ts doc comments re-pointed to the Cursor-era paths
    f = os.path.join(BASE, "scripts/lib/utils.d.ts")
    if exists(f):
        sub(f, " * Defaults to ~/.claude; override with ECC_AGENT_DATA_HOME (e.g. ~/.cursor/ecc).",
            " * Defaults to ~/.cursor/ecc; override with ECC_AGENT_DATA_HOME.")
    f = os.path.join(BASE, "scripts/lib/session-manager.d.ts")
    if exists(f):
        sub(f, " * ~/.claude/session-data/ with legacy read compatibility for ~/.claude/sessions/.",
            " * ~/.cursor/ecc/session-data/ with legacy read compatibility for ~/.cursor/ecc/sessions/.")
    f = os.path.join(BASE, "scripts/lib/session-aliases.d.ts")
    if exists(f):
        sub(f, " * Manages named aliases for session files, stored in $ECC_AGENT_DATA_HOME/session-aliases.json (default ~/.claude).",
            " * Manages named aliases for session files, stored in $ECC_AGENT_DATA_HOME/session-aliases.json (default ~/.cursor/ecc).")
    f = os.path.join(BASE, "scripts/lib/package-manager.d.ts")
    if exists(f):
        sub(f, " * 1. CLAUDE_PACKAGE_MANAGER environment variable",
            " * 1. CURSOR_PACKAGE_MANAGER environment variable")
        sub(f, " * 5. Global user preference (~/.claude/package-manager.json)",
            " * 5. Global user preference (~/.cursor/package-manager.json)")
        sub(f, " * Saves to ~/.claude/package-manager.json.",
            " * Saves to ~/.cursor/package-manager.json.")
        sub(f, " * Saves to <projectDir>/.claude/package-manager.json.",
            " * Saves to <projectDir>/.cursor/package-manager.json.")

    # --- hook files: temp-file prefixes, plugin roots, env renames
    f = os.path.join(BASE, "scripts/hooks/suggest-compact.js")
    if exists(f):
        resub(f, r"claude-tool-count-", "ecc-tool-count-", count=2)
        resub(f, r"claude-context-bucket-", "ecc-context-bucket-", count=2)
    f = os.path.join(BASE, "scripts/hooks/stop-format-typecheck.js")
    if exists(f):
        sub(f, "  const roots = [path.join(cwd, '.claude', 'plugins')];",
            "  const roots = [path.join(cwd, '.cursor', 'plugins')];")
        sub(f, "  if (homeDir) roots.push(path.join(homeDir, '.claude', 'plugins'));",
            "  if (homeDir) roots.push(path.join(homeDir, '.cursor', 'plugins'));")
    f = os.path.join(BASE, "scripts/hooks/skill-run-tracker.js")
    if exists(f):
        sub(f, " * ~/.claude/state/skill-runs.jsonl was never written and",
            " * ~/.cursor/ecc/state/skill-runs.jsonl was never written and")
    f = os.path.join(BASE, "scripts/hooks/session-end.js")
    if exists(f):
        sub(f, "  const envTranscriptPath = process.env.CLAUDE_TRANSCRIPT_PATH;",
            "  const envTranscriptPath = process.env.ECC_TRANSCRIPT_PATH;")
        sub(f, " * Without this, a parent session and any `claude -p ...` subprocess spawned by",
            " * Without this, a parent session and any CLI subprocess spawned by")
    f = os.path.join(BASE, "scripts/hooks/session-activity-tracker.js")
    if exists(f):
        sub(f, " * ~/.claude/metrics/tool-usage.jsonl for ECC2 metric sync.",
            " * ~/.cursor/ecc/metrics/tool-usage.jsonl for ECC2 metric sync.")
        sub(f, "  // Cursor does not set CLAUDE_HOOK_EVENT_NAME for hook subprocesses.",
            "  // Cursor does not set ECC_HOOK_EVENT_NAME for hook subprocesses.")
        sub(f, "    input?.hook_event_name || env.CLAUDE_HOOK_EVENT_NAME || ''",
            "    input?.hook_event_name || env.ECC_HOOK_EVENT_NAME || ''")
    f = os.path.join(BASE, "scripts/hooks/pre-compact.js")
    if exists(f):
        sub(f, " * written here was removed in fix #16: it needed `claude -p` and has no",
            " * written here was removed in fix #16: it needed a CLI subprocess and has no")
    for hf, pat in (("scripts/hooks/post-bash-command-log.js", None),
                    ("scripts/hooks/plan-canvas-sessions.js", None),
                    ("scripts/hooks/plan-canvas-pending.js", None)):
        f = os.path.join(BASE, hf)
        if exists(f):
            sub(f, "// `~/.claude-work` resolves to one place rather than two.",
                "// `~/some-dir` resolves to one place rather than two.")
    f = os.path.join(BASE, "scripts/hooks/mcp-health-check.js")
    if exists(f):
        sub(f, "  const eventName = process.env.CLAUDE_HOOK_EVENT_NAME || 'PreToolUse';",
            "  const eventName = process.env.ECC_HOOK_EVENT_NAME || 'PreToolUse';")
    f = os.path.join(BASE, "scripts/hooks/insaits-security-monitor.py")
    if exists(f):
        sub(f, '            session_name="claude-code-hook",',
            '            session_name="ecc-hook",')
        sub(f, '            sender_id="claude-code",',
            '            sender_id="cursor",')
    f = os.path.join(BASE, "scripts/hooks/governance-capture.js")
    if exists(f):
        sub(f, "  const hookPhase = process.env.CLAUDE_HOOK_EVENT_NAME || 'unknown';",
            "  const hookPhase = process.env.ECC_HOOK_EVENT_NAME || 'unknown';")
    f = os.path.join(BASE, "hooks/before-shell-execution.js")
    if exists(f):
        resub(f, r"\bclaudeRaw\b", "hookRaw", count=3)
    f = os.path.join(BASE, "scripts/hooks/doc-file-warning.js")
    if exists(f):
        sub(f, "const STRUCTURED_DIRS = /(^|\\/)(docs|\\.claude|\\.github|commands|skills|benchmarks|templates|\\.history|memory)\\//;",
            "const STRUCTURED_DIRS = /(^|\\/)(docs|\\.cursor|\\.github|commands|skills|benchmarks|templates|\\.history|memory)\\//;")

    # --- command prose stragglers
    sub(os.path.join(BASE, "commands/skill-create.md"),
        "a global skill uses `~/.cursor/skills/` or `~/.claude/skills/`.",
        "a global skill uses `~/.cursor/skills/`.")
    sub(os.path.join(BASE, "commands/save-session.md"),
        "mkdir -p ~/.claude/session-data",
        "mkdir -p ~/.cursor/ecc/session-data")
    sub(os.path.join(BASE, "commands/resume-session.md"),
        "SESSION LOADED: /Users/you/.claude/session-data/2024-01-15-abc123de-session.tmp",
        "SESSION LOADED: /Users/you/.cursor/ecc/session-data/2024-01-15-abc123de-session.tmp")
    for cf in ("commands/promote.md", "commands/projects.md",
               "commands/instinct-status.md"):
        f = os.path.join(BASE, cf)
        if exists(f):
            sub(f, "   Legacy data under `~/.claude/homunculus/` is not read; migrate it once with `skills/continuous-learning-v2/scripts/migrate-homunculus.sh`.",
                "   Legacy homunculus data is not read (the migration script was removed in fix #16).")
    f = os.path.join(BASE, "commands/instinct-import.md")
    if exists(f):
        sub(f, "   - Legacy data under `~/.claude/homunculus/` is not read; migrate it once with `skills/continuous-learning-v2/scripts/migrate-homunculus.sh`.",
            "   - Legacy homunculus data is not read (the migration script was removed in fix #16).")
    f = os.path.join(BASE, "commands/instinct-status.md")
    if exists(f):
        sub(f, "while a legacy `~/.claude/skills/continuous-learning-v2/` directory still",
            "while a legacy `~/.cursor/skills/continuous-learning-v2/` directory still")
    f = os.path.join(BASE, "commands/project-init.md")
    if exists(f):
        sub(f, "/project-init --target claude",
            "/project-init --target cursor")
        sub(f, "If `AGENTS.md`, `.ecc/settings.local.json`, `.cursor/`, `.codex/`, `.gemini/`, `.opencode/`, `.codebuddy/`, `.joycode/`, or `.qwen/` already exists, inspect it and propose a merge/append plan instead of overwriting.",
            "If `AGENTS.md`, `.ecc/settings.local.json`, or `.cursor/` already exists, inspect it and propose a merge/append plan instead of overwriting.")
        sub(f, "1. Identify the target harness. Default to `claude` unless the user asks for `cursor`, `codex`, `gemini`, `opencode`, `codebuddy`, `joycode`, or `qwen`.",
            "1. Identify the target harness. Default to `cursor`.")
    f = os.path.join(BASE, "commands/astra-review.md")
    if exists(f):
        sub(f, "(The Astra/Codex backend was removed in fix #16; review now runs via Grok reviewers in Cursor.)",
            "(The Astra review backend was removed in fix #16; review now runs via Grok reviewers in Cursor.)")
        sub(f, "> The Astra/Codex backend was removed in fix #16.",
            "> The Astra review backend was removed in fix #16.")

    # --- skill prose stragglers
    # (tolerant: the fix-up round scrubbed these lines from the staged
    # sources, so the old anchors may already be gone.)
    f = os.path.join(BASE, "skills/polish-pass/reference/impeccable-detector-rules.json")
    if exists(f):
        sub_if_new_present(f, '    "id": "codex-grid-background",',
            '    "id": "grid-background",')
    f = os.path.join(BASE, "skills/orchestrate/SKILL.md")
    if exists(f):
        sub_if_new_present(f, "they invoked external Codex/Gemini CLIs.",
            "they invoked external model CLIs.")
    f = os.path.join(BASE, "skills/ai-regression-testing/SKILL.md")
    if exists(f):
        sub(f, "- AI agent (Cursor, Cursor, Codex) has modified API routes or backend logic",
            "- AI agent (Cursor) has modified API routes or backend logic")
    f = os.path.join(BASE, "skills/frontend-design-direction/SKILL.md")
    if exists(f):
        sub(f, "Note: ECC intentionally does not rebundle the canonical Anthropic\n"
               "`frontend-design` skill. Install that from `anthropics/skills` when you want the\n"
               "official upstream skill.",
            "Note: ECC intentionally does not rebundle the canonical upstream\n"
            "`frontend-design` skill.")
    f = os.path.join(BASE, "skills/documentation-lookup/SKILL.md")
    if exists(f):
        sub(f, "Applies across harnesses that have the Context7 MCP configured (e.g. Cursor, Cursor, Codex).",
            "Applies in Cursor when the Context7 MCP is configured.")
    f = os.path.join(BASE, "skills/continuous-learning-v2/agents/observer-loop.sh")
    if exists(f):
        sub(f, "  # `claude` CLI, which has no Cursor equivalent. Observations are",
            "  # a CLI subprocess, which has no Cursor equivalent. Observations are")

    # --- apply.js: drop the second (dead) preflight call site. The
    # function was deleted in round 2; the const is assigned and never read.
    f = os.path.join(BASE, "scripts/lib/install/apply.js")
    if exists(f):
        sub(f, "  const preparedClaudeSettings = preflightClaudeSettingsOperations(appliedPlan);\n", "")
    # --- context-budget :133 (moved from part C: the generic pass rewrote
    # the line to "Cursor only" before part C ran) ---
    f = os.path.join(BASE, "skills/context-budget/SKILL.md")
    if exists(f):
        sub(f, "[`/context` and `/usage` commands (Cursor only; `/cost` is an alias)](https://code.claude.com/docs/en/commands)",
            "`/context` and `/usage` commands (Cursor only; `/cost` is an alias)")

    # --- hookify-runtime: the remaining CLAUDE_PROJECT_DIR env read
    # (the .claude path resubs in part C do not cover it) ---
    f = os.path.join(BASE, "scripts/hooks/hookify-runtime.js")
    if exists(f):
        sub(f, "  const configured = String(env.CLAUDE_PROJECT_DIR || '').trim();",
            "  const configured = String(env.CURSOR_PROJECT_DIR || '').trim();")

    # --- wave 3: session commands' remaining ~/.claude/ store paths.
    # Part B re-pointed the description labels; these 13 body/example lines
    # still cite the old store. The generic pass deliberately skips ~/.
    # paths (D15 guard), so re-point them here to the verified Cursor-era
    # store ~/.cursor/ecc/session-data/ (legacy reads: ~/.cursor/ecc/sessions/).
    for _cf, _n_data, _n_legacy in (("commands/resume-session.md", 6, 2),
                                    ("commands/save-session.md", 3, 0),
                                    ("commands/sessions.md", 2, 2)):
        _f = os.path.join(BASE, _cf)
        if exists(_f):
            resub(_f, r"~/\.claude/session-data/", "~/.cursor/ecc/session-data/", count=_n_data)
            if _n_legacy:
                resub(_f, r"~/\.claude/sessions/", "~/.cursor/ecc/sessions/", count=_n_legacy)

    # --- wave 4: rules-distill scan-skills.sh:10. The part-C catch-all
    # `\.claude/skills` -> `.ecc/skills` (unguarded) rewrote the HOME path
    # in the RULES_DISTILL_GLOBAL_DIR comment to an invented ~/.ecc/skills.
    # The global override in Cursor is ~/.cursor/skills (consistent with
    # the $HOME/.claude/skills -> $HOME/.cursor/skills sub for this file).
    f = os.path.join(BASE, "skills/rules-distill/scripts/scan-skills.sh")
    if exists(f):
        sub(f, "#   RULES_DISTILL_GLOBAL_DIR   Override ~/.ecc/skills (for testing only;",
            "#   RULES_DISTILL_GLOBAL_DIR   Override ~/.cursor/skills (for testing only;")

# ---------------------------------------------------------------- main

def edit_prose_round2():
    """Part C — package-manager re-point, harness re-point, skill prose,
    observer env renames, session-command re-point, icon/brand removal."""
    f = os.path.join(BASE, "scripts/lib/package-manager.js")
    if exists(f):
        remove_function(f, "getClaudeGlobalConfigPath")
        resub(f, r"    getClaudeGlobalConfigPath\(\)\n", "")
        sub(f, "  // 2. Check project-specific config (.cursor first, then .claude)\n"
               "  for (const configDir of ['.cursor', '.claude']) {",
            "  // 2. Check project-specific config (.cursor)\n"
               "  for (const configDir of ['.cursor']) {")
        CHANGES.append("scripts/lib/package-manager.js — Cursor-only config paths (fix #16)")

    f = os.path.join(BASE, "scripts/setup-package-manager.js")
    if exists(f):
        sub(f, "  --project <pm>  Set project preference (saves to .cursor/package-manager.json;\n"
               "                  an existing .claude/package-manager.json is still honoured)",
            "  --project <pm>  Set project preference (saves to .cursor/package-manager.json)")
        sub(f, "  console.log(`  Environment var: ${process.env.CURSOR_PACKAGE_MANAGER || process.env.CLAUDE_PACKAGE_MANAGER || 'not set'}`);",
            "  console.log(`  Environment var: ${process.env.CURSOR_PACKAGE_MANAGER || 'not set'}`);")
        sub(f, "    console.log('  (Also read from ~/.cursor/package-manager.json and ~/.claude/package-manager.json)');",
            "    console.log('  (Also read from ~/.cursor/package-manager.json)');")
        sub(f, "    console.log('  (An existing .claude/package-manager.json is still honoured on read)');\n", "")
        CHANGES.append("scripts/setup-package-manager.js — Cursor-only config paths (fix #16)")

    sub(os.path.join(BASE, "scripts/lib/resolve-formatter.js"),
        " * Resolve the runner binary and prefix args for the configured package\n * manager (respects CLAUDE_PACKAGE_MANAGER env and project config).",
        " * Resolve the runner binary and prefix args for the configured package\n * manager (respects CURSOR_PACKAGE_MANAGER env and project config).")

    f = os.path.join(BASE, "commands/setup-pm.md")
    if exists(f):
        CHANGES.append("commands/setup-pm.md — Cursor-only package-manager config (fix #16)")

    # agent-tool-map.js — the Pi emitter's tool table is host-neutral; the
    # model-tier const is re-keyed to Grok slugs. Only agent-emit-pi.js
    # imports this module, and only mapToolToPi, so the renames are safe.
    f = os.path.join(BASE, "scripts/lib/agent-tool-map.js")
    if exists(f):
        resub(f, r"\bCLAUDE_TO_PI_TOOLS\b", "CURSOR_TO_PI_TOOLS")
        sub(f, "const CLAUDE_MODEL_TIERS = Object.freeze(['haiku', 'sonnet', 'opus']);",
            "const GROK_MODEL_TIERS = Object.freeze(['cursor-grok-4.6-high-fast', 'grok-4.7-high']);")
        sub(f, "  CURSOR_TO_PI_TOOLS,\n  CLAUDE_MODEL_TIERS,",
            "  CURSOR_TO_PI_TOOLS,\n  GROK_MODEL_TIERS,")
        CHANGES.append("scripts/lib/agent-tool-map.js — CLAUDE_MODEL_TIERS -> GROK_MODEL_TIERS (Grok slugs)")

    sub(os.path.join(BASE, "scripts/hooks/pre-bash-commit-quality.js"),
        "{ pattern: /sk-ant-[a-zA-Z0-9_-]{20,}/, name: 'Anthropic API key' },",
        "{ pattern: /sk-ant-[a-zA-Z0-9_-]{20,}/, name: 'sk-ant API key' },")
    sub(os.path.join(BASE, "scripts/hooks/insaits-security-monitor.py"),
        '  INSAITS_MODEL      LLM model identifier for fingerprinting. Default: claude-opus.',
        '  INSAITS_MODEL      LLM model identifier for fingerprinting. Default: grok-4.7-high.')
    sub(os.path.join(BASE, "scripts/hooks/insaits-security-monitor.py"),
        'DEFAULT_MODEL: str = "claude-opus"',
        'DEFAULT_MODEL: str = "grok-4.7-high"')

    # --- gate.mjs / gate.md (design-taste-frontend finish gate) ---
    # (subs below are tolerant: the fix-up round scrubbed the staged
    # gate.mjs/gate.md to the cursor-only form, so the old anchors may
    # already be gone.)
    f = os.path.join(BASE, "skills/design-taste-frontend/scripts/gate.mjs")
    if exists(f):
        sub_if_new_present(f, "const MODES = { claude: 'block', codex: 'block', antigravity: 'continue' };",
            "const MODES = { cursor: 'block' };")
        sub_if_new_present(f, "if (HOOK !== null && !MODES[HOOK]) { console.error('gate: --hook takes claude, codex or antigravity'); process.exit(HOOK === true ? 2 : 0); }",
            "if (HOOK !== null && !MODES[HOOK]) { console.error('gate: --hook takes cursor'); process.exit(HOOK === true ? 2 : 0); }")
        maybe_resub(f, r"node <skill>/scripts/gate\.mjs --hook claude\|codex\|antigravity",
                    "node <skill>/scripts/gate.mjs --hook cursor")
        maybe_resub(f, r"\{\"decision\":\"block\",\"reason\":\.\.\.\} for claude and codex,\n  \{",
                    '{"decision":"block","reason":...} for cursor,\n  {')
        maybe_resub(f, r"for claude and codex", "for cursor")
        CHANGES.append("skills/design-taste-frontend/scripts/gate.mjs — hook mode cursor-only (fix #16)")
    f = os.path.join(BASE, "skills/design-taste-frontend/references/gate.md")
    if exists(f):
        sub_if_new_present(f, "{ \"hooks\": [ { \"type\": \"command\", \"command\": \"node \\\"/path/to/skill/scripts/gate.mjs\\\" --hook claude\", \"timeout\": 600 } ] }",
            "{ \"hooks\": [ { \"type\": \"command\", \"command\": \"node \\\"/path/to/skill/scripts/gate.mjs\\\" --hook cursor\", \"timeout\": 600 } ] }")
        # (The Codex .codex/hooks.json section is deleted in edit_post_generic
        # by span deletion — its heading is bold text, not a markdown heading,
        # so remove_section_by_heading cannot find it.)
        CHANGES.append("skills/design-taste-frontend/references/gate.md — cursor-only hook paths (fix #16)")

    # --- design-taste brand icon removal (JSON object entries + viewBox keys) ---
    # (tolerant: the fix-up round removed the 4 brand entries from the
    # staged index.json / icons-credits.json, so there may be nothing left
    # to remove.)
    f = os.path.join(BASE, "skills/design-taste-frontend/assets/icons/index.json")
    if exists(f):
        for brand in ("anthropic", "claude", "claude-code", "codex"):
            remove_array_entry_if_present(f, brand)
        for key in ("logos:anthropic-icon", "logos:claude-icon", "logos:claude-code", "logos:codex"):
            resub_if_present(f, rf'  "{re.escape(key)}": \[\n(?:   [^\n]*\n){{4}}  \],\n', "")
        CHANGES.append("skills/design-taste-frontend/assets/icons/index.json — 4 brand icon entries + viewBox keys removed")
    f = os.path.join(BASE, "skills/design-taste-frontend/assets/icons/demo/icons-credits.json")
    if exists(f):
        for svg in ("anthropic.svg", "claude-code.svg", "claude.svg", "codex.svg"):
            remove_array_entry_if_present(f, svg)
        CHANGES.append("skills/design-taste-frontend/assets/icons/demo/icons-credits.json — 4 brand credit entries removed")
    sub_if_new_present(os.path.join(BASE, "skills/design-taste-frontend/assets/layout/heroes.json"),
        '"from": "Anthropic, Stripe Press, Mercury, private banks and advisers"',
        '"from": "Stripe Press, Mercury, private banks and advisers"')
    REMOVALS.append("design-taste-frontend brand icons (anthropic/claude/claude-code/codex) — "
                    "removed from assets/icons/index.json + demo/icons-credits.json; the "
                    "heroes.json 'from' attribution drops Anthropic (fix #16)")

    # README + package.json skill-host-compat mentions (command deleted D16)
    sub(os.path.join(BASE, "README.md"),
        "The plugin's Node scripts (`/harness-audit`, `/skill-host-compat`, the",
        "The plugin's Node scripts (`/harness-audit`, the")
    sub(os.path.join(BASE, "package.json"),
        '"description": "Runtime dependencies for the hackathon-ecc Cursor plugin\'s Node scripts (harness-audit, skill-host-compat, epic-*, validate-skills). Versions pinned to the ECC repo\'s package.json."',
        '"description": "Runtime dependencies for the hackathon-ecc Cursor plugin\'s Node scripts (harness-audit, epic-*, validate-skills). Versions pinned to the ECC repo\'s package.json."')
    sub(os.path.join(BASE, "scripts/lib/utils.js"),
        ' * leading/trailing hyphens, and removes leading dots so hidden-dir names\n * like ".claude" map cleanly to "claude".',
        ' * leading/trailing hyphens, and removes leading dots so hidden-dir names\n * like ".ecc" map cleanly to "ecc".')
    resub(os.path.join(BASE, "hooks/after-file-edit.js"), r"\bclaudeStr\b", "hookStr", count=4)
    sub(os.path.join(BASE, "scripts/hooks/evaluate-session.js"),
        "    transcriptPath = process.env.CLAUDE_TRANSCRIPT_PATH;",
        "    transcriptPath = process.env.ECC_TRANSCRIPT_PATH;")

    # GAN attributions (D11) — gan-build / gan-design / ecc-gan-* agents
    sub(os.path.join(BASE, "commands/gan-build.md"),
        "This command orchestrates a three-agent build loop inspired by Anthropic's March 2026 harness design paper.",
        "This command orchestrates a three-agent build loop inspired by the upstream multi-agent harness design paper.")
    sub(os.path.join(BASE, "commands/gan-design.md"),
        "This is the same mode Anthropic used for their frontend design experiments, where they saw creative breakthroughs like the 3D Dutch art museum with CSS perspective and doorway navigation.",
        "This mode was used for frontend design experiments, with creative breakthroughs like the 3D Dutch art museum with CSS perspective and doorway navigation.")
    for agent in ("ecc-gan-planner.md", "ecc-gan-generator.md", "ecc-gan-evaluator.md"):
        maybe_resub(os.path.join(BASE, "agents", agent),
                    r"\(inspired by Anthropic's harness design paper, March 2026\)",
                    "(inspired by the upstream multi-agent harness design paper)")
    # hackathon-mode.mdc:38 — upstream claude -p invocation path (true statement,
    # but the invocation name must go)
    sub(os.path.join(BASE, "rules/hackathon-mode.mdc"),
        "(its upstream `claude -p` invocation path does not run in Cursor",
        "(its upstream CLI-subprocess invocation path does not run in Cursor")

    # --- harness-audit.js (scripts/harness-audit.js, not scripts/lib/) ---
    f = os.path.join(BASE, "scripts/harness-audit.js")
    if exists(f):
        sub(f, "  // 'everything-claude-code' is the legacy package name, kept for older checkouts.\n"
               "  if (['ecc-universal', 'everything-claude-code'].includes(packageJson?.name)) {",
            "  if (['ecc-universal'].includes(packageJson?.name)) {")
        sub(f, "    fileExists(rootDir, '.claude-plugin/plugin.json') &&",
            "    fileExists(rootDir, '.cursor-plugin/plugin.json') &&")
        sub(f, "// The everything-claude-code entries below are legacy install ids, kept so\n"
               "// existing 1.x installs are still detected.\n"
               "const ECC_PLUGIN_KEY_PATTERNS = [\n"
               "  /^ecc@/i,\n"
               "  /^everything-claude-code@/i,\n"
               "];\n"
               "\n"
               "const ECC_LEGACY_PLUGIN_DIRS = [\n"
               "  'ecc',\n"
               "  'ecc@ecc',\n"
               "  'everything-claude-code',\n"
               "  'everything-claude-code@everything-claude-code',\n"
               "];\n"
               "\n"
               "const ECC_CACHE_MARKETPLACES = ['everything-claude-code', 'ecc'];\n"
               "const ECC_CACHE_PLUGIN_NAMES = ['ecc', 'everything-claude-code'];",
            "const ECC_PLUGIN_KEY_PATTERNS = [\n"
               "  /^ecc@/i,\n"
               "];\n"
               "\n"
               "const ECC_LEGACY_PLUGIN_DIRS = [\n"
               "  'ecc',\n"
               "  'ecc@ecc',\n"
               "];\n"
               "\n"
               "const ECC_CACHE_MARKETPLACES = ['ecc'];\n"
               "const ECC_CACHE_PLUGIN_NAMES = ['ecc'];")
        sub(f, "  const pluginJson = path.join(installRoot, '.claude-plugin', 'plugin.json');",
            "  const pluginJson = path.join(installRoot, '.cursor-plugin', 'plugin.json');")
        sub(f, "    path.join(rootDir, '.claude', 'plugins'),\n"
               "    ...homeDirs.map(homeDir => path.join(homeDir, '.claude', 'plugins')),",
            "    path.join(rootDir, '.cursor', 'plugins'),\n"
               "    ...homeDirs.map(homeDir => path.join(homeDir, '.cursor', 'plugins')),")
        sub(f, "    path.join(rootDir, '.claude', 'plugins', 'installed_plugins.json'),\n"
               "    ...homeDirs.map(homeDir => path.join(homeDir, '.claude', 'plugins', 'installed_plugins.json')),",
            "    path.join(rootDir, '.cursor', 'plugins', 'installed_plugins.json'),\n"
               "    ...homeDirs.map(homeDir => path.join(homeDir, '.cursor', 'plugins', 'installed_plugins.json')),")
        sub(f, "  const projectHooks = safeRead(rootDir, '.claude/settings.json');",
            "  const projectHooks = safeRead(rootDir, '.ecc/settings.json');")
        sub(f, "      path: '~/.claude/plugins/ecc/ (legacy everything-claude-code paths also supported)',",
            "      path: '~/.cursor/plugins/hackathon-ecc/',")
        sub(f, "      path: '.claude/',\n"
               "      description: 'Project-specific harness overrides exist under .claude/',\n"
               "      pass: countFiles(rootDir, '.claude/agents', '.md') > 0 ||\n"
               "        countFiles(rootDir, '.claude/skills', 'SKILL.md') > 0 ||\n"
               "        countFiles(rootDir, '.claude/commands', '.md') > 0 ||\n"
               "        fileExists(rootDir, '.claude/settings.json') ||\n"
               "        fileExists(rootDir, '.claude/hooks.json'),\n"
               "      fix: 'Add project-local .claude hooks, commands, skills, or settings that tailor ECC to this repo.',",
            "      path: '.ecc/',\n"
               "      description: 'Project-specific harness overrides exist under .ecc/',\n"
               "      pass: countFiles(rootDir, '.ecc/agents', '.md') > 0 ||\n"
               "        countFiles(rootDir, '.ecc/skills', 'SKILL.md') > 0 ||\n"
               "        countFiles(rootDir, '.ecc/commands', '.md') > 0 ||\n"
               "        fileExists(rootDir, '.ecc/settings.json') ||\n"
               "        fileExists(rootDir, '.ecc/hooks.json'),\n"
               "      fix: 'Add project-local .ecc hooks, commands, skills, or settings that tailor ECC to this repo.',")
        sub(f, "      pass: fileExists(rootDir, 'AGENTS.md') || fileExists(rootDir, 'CLAUDE.md') || fileExists(rootDir, '.claude/CLAUDE.md'),\n"
               "      fix: 'Add AGENTS.md or CLAUDE.md so the harness has project-specific instructions.',",
            "      pass: fileExists(rootDir, 'AGENTS.md') || fileExists(rootDir, '.ecc/AGENTS.md'),\n"
               "      fix: 'Add AGENTS.md so the harness has project-specific instructions.',")
        sub(f, "      pass: fileExists(rootDir, '.mcp.json') || fileExists(rootDir, '.claude/settings.json') || fileExists(rootDir, '.claude/settings.local.json'),\n"
               "      fix: 'Add .mcp.json or .claude/settings.json so project-local tool configuration is explicit.',",
            "      pass: fileExists(rootDir, '.mcp.json') || fileExists(rootDir, '.ecc/settings.json'),\n"
               "      fix: 'Add .mcp.json or .ecc/settings.json so project-local tool configuration is explicit.',")
        sub(f, "      path: '.claude/memory.md',\n"
               "      description: 'Project memory or durable notes are checked in',\n"
               "      pass: fileExists(rootDir, '.claude/memory.md') || countFiles(rootDir, 'docs/adr', '.md') > 0,\n"
               "      fix: 'Add durable project memory such as .claude/memory.md or ADRs under docs/adr/.',",
            "      path: '.ecc/memory.md',\n"
               "      description: 'Project memory or durable notes are checked in',\n"
               "      pass: fileExists(rootDir, '.ecc/memory.md') || countFiles(rootDir, 'docs/adr', '.md') > 0,\n"
               "      fix: 'Add durable project memory such as .ecc/memory.md or ADRs under docs/adr/.',")
        sub(f, "      path: '.claude/settings.json',\n"
               "      description: 'Project-local hook settings reference tool/prompt guardrails',\n"
               "      pass: projectHooks.includes('PreToolUse') || projectHooks.includes('beforeSubmitPrompt') || fileExists(rootDir, '.claude/hooks.json'),\n"
               "      fix: 'Add project-local hook settings or hook definitions for prompt/tool guardrails.',",
            "      path: '.ecc/settings.json',\n"
               "      description: 'Project-local hook settings reference tool/prompt guardrails',\n"
               "      pass: projectHooks.includes('PreToolUse') || projectHooks.includes('beforeSubmitPrompt') || fileExists(rootDir, '.ecc/hooks.json'),\n"
               "      fix: 'Add project-local hook settings or hook definitions for prompt/tool guardrails.',")
        CHANGES.append("scripts/harness-audit.js — Cursor-only paths + legacy everything-claude-code ids removed")

    # --- harness-capabilities.js: narrow HARNESS_CAPABILITIES to cursor only ---
    f = os.path.join(BASE, "scripts/lib/harness-capabilities.js")
    if exists(f):
        for hid in ("claude", "codex", "kimi", "antigravity", "copilot", "gemini",
                    "opencode", "codebuddy", "joycode", "qwen", "zed", "adal",
                    "hermes", "openclaw"):
            remove_array_entry(f, hid)
        CHANGES.append("scripts/lib/harness-capabilities.js — HARNESS_CAPABILITIES narrowed to the cursor entry")
    # --- harness-adapter-compliance.js: narrow ADAPTER_RECORDS to cursor only ---
    f = os.path.join(BASE, "scripts/lib/harness-adapter-compliance.js")
    if exists(f):
        for rid in ("claude-code", "codex", "opencode", "pi", "gemini", "zed",
                    "dmux", "deepseek-harness", "orca", "superset", "ghast",
                    "terminal-only"):
            remove_array_entry(f, rid)
        CHANGES.append("scripts/lib/harness-adapter-compliance.js — ADAPTER_RECORDS narrowed to the cursor entry")
    REMOVALS.append("harness-capabilities.js + harness-adapter-compliance.js non-Cursor "
                    "entries — the cross-harness capability/compliance catalogs are now "
                    "Cursor-only; the DeepSeek DSH bridge record goes with them (fix #16)")

    # --- statusline-render.js (scripts/lib/) ---
    f = os.path.join(BASE, "scripts/lib/statusline-render.js")
    if exists(f):
        sub(f, "Inspired by leeguooooo/claude-code-usage-bar (MIT). ECC re-implementation",
            "Inspired by an open-source usage-bar project (MIT). ECC re-implementation")
        sub(f, " * @param {string} [claudeDir] selected profile root",
            " * @param {string} [agentDataDir] selected profile root")
        sub(f, "function readInstalledPlugins(claudeDir, workspace) {\n"
               "  try {\n"
               "    const dir = claudeDir || process.env.CLAUDE_CONFIG_DIR || path.join(os.homedir(), '.claude');",
            "function readInstalledPlugins(agentDataDir, workspace) {\n"
               "  try {\n"
               "    const dir = agentDataDir || process.env.ECC_AGENT_DATA_HOME || path.join(os.homedir(), '.cursor', 'ecc');")
        sub(f, "    const enabled = pluginEnablement([path.join(dir, 'settings.json'),\n"
               "      path.join(project, '.claude', 'settings.json'), path.join(project, '.claude', 'settings.local.json')]);",
            "    const enabled = pluginEnablement([path.join(dir, 'settings.json')]);")
        CHANGES.append("scripts/lib/statusline-render.js — plugin scan re-pointed to ~/.cursor/ecc; .claude settings reads dropped")


    # --- skill prose: unified-memory (Cursor-only) ---
    f = os.path.join(BASE, "skills/unified-memory/SKILL.md")
    if exists(f):
        sub(f, 'ecc memory search "authentication migration" --target-harness codex',
            'ecc memory search "authentication migration" --target-harness cursor')
        sub(f, "    --source-harness codex \\",
            "    --source-harness cursor \\")
        sub(f, "  --from codex \\\n  --target claude \\",
            "  --from cursor \\\n  --target cursor \\")
        sub(f, "ECC_MEMORY_HARNESS=codex ecc-memory-mcp",
            "ECC_MEMORY_HARNESS=cursor ecc-memory-mcp")
        CHANGES.append("skills/unified-memory/SKILL.md — narrowed to Cursor-only")
        REMOVALS.append("unified-memory cross-host transfer — handoff flags now take cursor "
                        "only; the Codex/Hermes/OpenCode paths are gone (fix #16)")

    # --- context-budget: delete Codex rows + Codex link; drop the docs URL
    # (code.claude.com is the Claude Code docs host, not a verified Cursor URL) ---
    f = os.path.join(BASE, "skills/context-budget/SKILL.md")
    if exists(f):
        resub(f, r"\| Codex CLI \(Codex only\)[^\n]*\n", "")
        resub(f, r"\| Codex app \(Codex only\)[^\n]*\n", "")
        CHANGES.append("skills/context-budget/SKILL.md — Codex rows/link removed; Cursor meter kept")

    # --- small prose fixes ---
    # (tolerant except ai-feature-spec: the fix-up round scrubbed these
    # lines from the staged sources, so the old anchors may already be
    # gone. ai-feature-spec is upstream-copied, not staged — strict sub.)
    sub(os.path.join(BASE, "skills/ai-feature-spec/SKILL.md"),
        "  compatible_with:\n  - claude-code\n  - codex\n",
        "  compatible_with:\n  - cursor\n")
    sub_if_new_present(os.path.join(BASE, "skills/polish-pass/reference/impeccable-critique.md"),
        "Run Assessment A alone in this context and skip both sub-agent gates below, the Codex permission question included: with no B there is nothing to isolate A from, so this is the complete native method and carries no degraded banner.",
        "Run Assessment A alone in this context and skip both sub-agent gates below: with no B there is nothing to isolate A from, so this is the complete native method and carries no degraded banner.")
    sub_if_new_present(os.path.join(BASE, "skills/integration/SKILL.md"),
        "- `integrations` by whawkinsiv (claude-code-skills): NOT used.",
        "- `integrations` by whawkinsiv (whawkinsiv's skills repo): NOT used.")
    sub_if_new_present(os.path.join(BASE, "skills/feature-expansion/SKILL.md"),
        "- **claude-handoff** (`cliffordcollinsglobal/agent-skills`, no license) — the execution contract used in Phase 4:",
        "- **handoff** (`cliffordcollinsglobal/agent-skills`, no license) — the execution contract used in Phase 4:")
    f = os.path.join(BASE, "skills/skill-scout/SKILL.md")
    if exists(f):
        sub(f, "grep -RilE \"keyword|synonym\" ~/.cursor/skills ~/.cursor/plugins/marketplaces ~/.claude/skills ~/.claude/plugins/marketplaces 2>/dev/null",
            "grep -RilE \"keyword|synonym\" ~/.cursor/skills ~/.cursor/plugins/marketplaces 2>/dev/null")
    # skill-stocktake scripts
    for sh in ("scripts/scan.sh", "scripts/quick-diff.sh"):
        f = os.path.join(BASE, "skills/skill-stocktake", sh)
        if exists(f):
            sub(f, "# When CWD_SKILLS_DIR is omitted, defaults to $PWD/.claude/skills so the",
                "# When CWD_SKILLS_DIR is omitted, defaults to $PWD/.ecc/skills so the")
            sub(f, "#   SKILL_STOCKTAKE_GLOBAL_DIR   Override ~/.claude/skills (for testing only;",
                "#   SKILL_STOCKTAKE_GLOBAL_DIR   Override ~/.cursor/skills (for testing only;")
            maybe_resub(f, r"\$HOME/\.claude/skills", "$HOME/.cursor/skills")
            maybe_resub(f, r"\$PWD/\.claude/skills", "$PWD/.ecc/skills")
            maybe_resub(f, r"\*/\.claude/skills\*", "*/.ecc/skills*")
            maybe_resub(f, r"\.claude/skills", ".ecc/skills")
            if "scan.sh" in sh:
                sub(f, "OBSERVATIONS=\"${SKILL_STOCKTAKE_OBSERVATIONS:-$HOME/.claude/observations.jsonl}\"",
                    "OBSERVATIONS=\"${SKILL_STOCKTAKE_OBSERVATIONS:-$HOME/.cursor/ecc/observations.jsonl}\"")
    # rules-distill scripts + SKILL.md
    for sh in ("scripts/scan-skills.sh", "scripts/scan-rules.sh"):
        f = os.path.join(BASE, "skills/rules-distill", sh)
        if exists(f):
            maybe_resub(f, r"\$HOME/\.claude/skills", "$HOME/.cursor/skills")
            maybe_resub(f, r"\$PWD/\.claude/skills", "$PWD/.ecc/skills")
            maybe_resub(f, r"\$HOME/\.claude/rules", "$HOME/.cursor/rules")
            maybe_resub(f, r"\*/\.claude/skills\*", "*/.ecc/skills*")
            maybe_resub(f, r"\.claude/skills", ".ecc/skills")
            maybe_resub(f, r"\.claude/rules", ".cursor/rules")
    sub(os.path.join(BASE, "skills/rules-distill/SKILL.md"),
        "bash ~/.claude/skills/rules-distill/scripts/scan-skills.sh",
        "bash \"$ECC_PLUGIN_ROOT/skills/rules-distill/scripts/scan-skills.sh\"")
    sub(os.path.join(BASE, "skills/rules-distill/SKILL.md"),
        "bash ~/.claude/skills/rules-distill/scripts/scan-rules.sh",
        "bash \"$ECC_PLUGIN_ROOT/skills/rules-distill/scripts/scan-rules.sh\"")
    sub(os.path.join(BASE, "skills/repo-scan/SKILL.md"),
        'REPO_SCAN_INSTALL_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills/repo-scan"',
        'REPO_SCAN_INSTALL_DIR="$ECC_PLUGIN_ROOT/skills/repo-scan"')
    # delivery-gate quality-gate.py
    f = os.path.join(BASE, "skills/delivery-gate/hooks/quality-gate.py")
    if exists(f):
        sub(f, "    cwd = os.environ.get('CLAUDE_PROJECT_DIR', os.getcwd())",
            "    cwd = os.environ.get('CURSOR_PROJECT_DIR', os.getcwd())")
        sub(f, "    mem = os.path.expanduser(f'~/.claude/projects/{safe}/memory')",
            "    mem = os.path.expanduser(f'~/.cursor/ecc/projects/{safe}/memory')")
    # ecc-recipes command search paths
    f = os.path.join(BASE, "skills/ecc-recipes/SKILL.md")
    if exists(f):
        sub(f, '  "$HOME"/.claude/plugins/marketplaces/ecc/commands \\\n'
               '  "$HOME"/.claude/plugins/cache/ecc/ecc/*/commands \\\n'
               '  ./commands \\\n'
               '  ./.claude/commands \\\n'
               '  "$HOME"/.claude/commands; do',
            '  "$HOME"/.cursor/plugins/local/hackathon-ecc/commands \\\n'
               '  "$HOME"/.cursor/plugins/*/hackathon-ecc/commands \\\n'
               '  ./commands \\\n'
               '  ./.ecc/commands \\\n'
               '  "$HOME"/.cursor/ecc/commands; do')
    # living-docs-governance:61
    sub(os.path.join(BASE, "skills/living-docs-governance/SKILL.md"),
        "- Codex and harness-neutral projects commonly use `AGENTS.md`.",
        "- Harness-neutral projects commonly use `AGENTS.md`.")
    # codehealth-mcp:42 + :113 (the :113 line would duplicate AGENTS.md under
    # the generic CLAUDE.md -> AGENTS.md rule, so it is reworded here first)
    sub(os.path.join(BASE, "skills/codehealth-mcp/SKILL.md"),
        "Paste into the project `AGENTS.md` or `CLAUDE.md`:",
        "Paste into the project `AGENTS.md`:")
    # browser-qa — claude-in-chrome is not a Cursor MCP
    f = os.path.join(BASE, "skills/browser-qa/SKILL.md")
    if exists(f):
        sub(f, 'description: "Run automated post-deploy UI verification with a browser automation MCP (claude-in-chrome, Playwright, or Puppeteer):',
            'description: "Run automated post-deploy UI verification with a browser automation MCP (Playwright or Puppeteer):')
        sub(f, "Uses the browser automation MCP (claude-in-chrome, Playwright, or Puppeteer) to interact with live pages like a real user.",
            "Uses the browser automation MCP (Playwright or Puppeteer) to interact with live pages like a real user.")
        sub(f, "- `mChild__claude-in-chrome__*` tools (preferred — uses your actual Chrome)\n", "")
        CHANGES.append("skills/browser-qa/SKILL.md — claude-in-chrome MCP removed")
        REMOVALS.append("browser-qa claude-in-chrome MCP — not a Cursor MCP; Playwright / "
                        "Puppeteer remain (fix #16)")


    # --- ck skill: re-point ~/.claude/ck -> ~/.cursor/ecc/ck ---
    f = os.path.join(BASE, "skills/ck/SKILL.md")
    if exists(f):
        resub(f, r"\$\{CLAUDE_SKILL_DIR\}", "${ECC_PLUGIN_ROOT}/skills/ck", count=10)
        CHANGES.append("skills/ck/SKILL.md — storage re-pointed to ~/.cursor/ecc/ck")

    # --- strategic-compact ---
    f = os.path.join(BASE, "skills/strategic-compact/SKILL.md")
    if exists(f):
        sub(f, "Do not copy the block below into your `hooks/hooks.json` — `~/.claude/scripts/` does not exist on plugin installs, and duplicating a plugin hook causes double execution.",
            "Do not copy the block below into your `hooks/hooks.json` — plugin scripts live under the plugin root, and duplicating a plugin hook causes double execution.")
        sub(f, "| Memory files (`~/.claude/memory/`) | Multi-step conversation context |",
            "| Memory files (the agent's memory directory) | Multi-step conversation context |")
        sub(f, "> `CLAUDE_CODE_ENABLE_TODO_TOOLS=1` brings them back, but that is a per-machine\n> environment setting — **it does not travel with this skill**, so you cannot assume the\n> reader has it.",
            "> The tools cannot be re-enabled from this skill — **they do not travel with it**, so you cannot assume the reader has them.")
        CHANGES.append("skills/strategic-compact/SKILL.md — auto-compact/env + path re-points")

    # --- continuous-learning (v1) ---
    f = os.path.join(BASE, "skills/continuous-learning/SKILL.md")
    if exists(f):
        sub(f, '  "learned_skills_path": "~/.claude/skills/learned/",',
            '  "learned_skills_path": "~/.cursor/ecc/skills/learned/",')
        sub(f, "Add to your `~/.claude/settings.json`:",
            "The plugin registers this hook itself via `hooks/hooks.json`; for a manual install, add to your hook config:")
        sub(f, '        "command": "~/.claude/skills/continuous-learning/evaluate-session.sh"',
            '        "command": "$ECC_PLUGIN_ROOT/skills/continuous-learning/evaluate-session.sh"')
    f = os.path.join(BASE, "skills/continuous-learning/config.json")
    if exists(f):
        sub(f, '  "learned_skills_path": "~/.claude/skills/learned/",',
            '  "learned_skills_path": "~/.cursor/ecc/skills/learned/",')
    f = os.path.join(BASE, "skills/continuous-learning/evaluate-session.sh")
    if exists(f):
        sub(f, "# Hook config (in ~/.claude/settings.json):",
            "# Hook config (registered via the plugin's hooks/hooks.json):")
        sub(f, '#         "command": "~/.claude/skills/continuous-learning/evaluate-session.sh"',
            '#         "command": "$ECC_PLUGIN_ROOT/skills/continuous-learning/evaluate-session.sh"')
        sub(f, "# Extracted skills saved to: ~/.claude/skills/learned/",
            "# Extracted skills saved to: ~/.cursor/ecc/skills/learned/")
        sub(f, 'LEARNED_SKILLS_PATH="${HOME}/.claude/skills/learned"',
            'LEARNED_SKILLS_PATH="${HOME}/.cursor/ecc/skills/learned"')
        sub(f, """    LEARNED_SKILLS_PATH=$(jq -r '.learned_skills_path // "~/.claude/skills/learned/"' "$CONFIG_FILE" | sed "s|~|$HOME|")""",
            """    LEARNED_SKILLS_PATH=$(jq -r '.learned_skills_path // "~/.cursor/ecc/skills/learned/"' "$CONFIG_FILE" | sed "s|~|$HOME|")""")
        sub(f, '  transcript_path="${CLAUDE_TRANSCRIPT_PATH:-}"',
            '  transcript_path="${ECC_TRANSCRIPT_PATH:-}"')
        CHANGES.append("skills/continuous-learning — paths re-pointed to ~/.cursor/ecc/skills/learned")

    # --- continuous-learning-v2: SKILL.md + observer scripts ---
    f = os.path.join(BASE, "skills/continuous-learning-v2/SKILL.md")
    if exists(f):
        sub(f, "| Storage | Global (`~/.claude/homunculus/`) | Project-scoped (`${XDG_DATA_HOME:-~/.local/share}/ecc-homunculus/projects/<hash>/`) |",
            "| Storage | Global (`~/.local/share/ecc-homunculus/`) | Project-scoped (`${XDG_DATA_HOME:-~/.local/share}/ecc-homunculus/projects/<hash>/`) |")
        sub(f, "1. **`CLAUDE_PROJECT_DIR` env var** (highest priority) -- honored as an explicit override even when the directory is not a git repo (hashed by its absolute path)",
            "1. **`CURSOR_PROJECT_DIR` env var** (highest priority) -- honored as an explicit override even when the directory is not a git repo (hashed by its absolute path)")
        sub(f, "Existing users with data at `~/.claude/homunculus` can migrate once:\n\n```bash\nbash skills/continuous-learning-v2/scripts/migrate-homunculus.sh\n```\n",
            "")
        sub(f, "If you previously copied `observe.sh` into `~/.claude/settings.json`, remove that duplicate `PreToolUse` / `PostToolUse` block.",
            "If you previously copied `observe.sh` into a host settings file, remove that duplicate `PreToolUse` / `PostToolUse` block.")
        resub(f, r'"command": "~/\.claude/skills/continuous-learning-v2/hooks/observe\.sh"',
              '"command": "$ECC_PLUGIN_ROOT/skills/continuous-learning-v2/hooks/observe.sh"')
        sub(f, "- Existing global instincts can be migrated from `~/.claude/homunculus/instincts/` with `skills/continuous-learning-v2/scripts/migrate-homunculus.sh` (shipped with this skill; run it from the plugin root)\n",
            "")
        CHANGES.append("skills/continuous-learning-v2/SKILL.md — paths/env re-pointed; migration lines removed")
        REMOVALS.append("continuous-learning-v2 homunculus migration — migrate-homunculus.sh "
                        "was deleted (D13); there is no migration path from the old "
                        "`~/.claude/homunculus` location (fix #16)")
    # observer scripts: CLAUDE_PROJECT_DIR -> CURSOR_PROJECT_DIR (verified
    # Cursor env, same override semantics); hook-event/entrypoint envs ->
    # plugin-owned ECC_* names (mechanism unchanged: caller-set fallbacks).
    f = os.path.join(BASE, "skills/continuous-learning-v2/scripts/detect-project.sh")
    if exists(f):
        resub(f, r"\bCLAUDE_PROJECT_DIR\b", "CURSOR_PROJECT_DIR")
    f = os.path.join(BASE, "skills/continuous-learning-v2/scripts/instinct-cli.py")
    if exists(f):
        resub(f, r"\bCLAUDE_PROJECT_DIR\b", "CURSOR_PROJECT_DIR")
        sub(f, "    _warn_legacy_data()\n", "")
        sub(f, '''def _warn_legacy_data() -> None:
    """Warn if legacy ~/.claude/homunculus/ contains data while the active
    path has moved to the XDG directory."""
    legacy_dir = Path.home() / ".claude" / "homunculus"
    if legacy_dir == HOMUNCULUS_DIR:
        return  # CLV2_HOMUNCULUS_DIR explicitly points at the legacy path
    if not legacy_dir.is_dir():
        return

    # Count substantive files (skip empty dirs and the directory itself)
    try:
        legacy_files = [f for f in legacy_dir.rglob("*") if f.is_file()]
    except (PermissionError, OSError):
        print(f"\\n  Note: legacy directory exists but cannot be read: {legacy_dir}", file=sys.stderr)
        return
    if not legacy_files:
        return

    migrate_script = Path(__file__).resolve().parent / "migrate-homunculus.sh"

    print(f"\\n{'!'*60}")
    print("  LEGACY DATA DETECTED")
    print(f"{'!'*60}")
    print(f"  Found {len(legacy_files)} file(s) in legacy path:")
    print(f"    {legacy_dir}")
    print("  Active data directory:")
    print(f"    {HOMUNCULUS_DIR}")
    print()
    print("  Run the migration script to move your data:")
    print(f'    bash "{migrate_script}"')
    print(f"  Or set CLV2_HOMUNCULUS_DIR={legacy_dir} to use the legacy path.")
    print(f"{'!'*60}\\n")
''', "")
        CHANGES.append("skills/continuous-learning-v2/scripts/instinct-cli.py — CURSOR_PROJECT_DIR; legacy-data warning removed")
    f = os.path.join(BASE, "skills/continuous-learning-v2/scripts/test_parse_instinct.py")
    if exists(f):
        resub(f, r"\bCLAUDE_PROJECT_DIR\b", "CURSOR_PROJECT_DIR")
        sub(f, '    homunculus = tmp_path / ".claude" / "homunculus"',
            '    homunculus = tmp_path / ".ecc" / "homunculus"')
    f = os.path.join(BASE, "skills/continuous-learning-v2/hooks/observe.sh")
    if exists(f):
        sub(f, "# Can also be registered manually in ~/.claude/settings.json.",
            "# Can also be registered manually in a host settings file.")
        sub(f, '  case "${CLAUDE_HOOK_EVENT_NAME:-}" in',
            '  case "${ECC_HOOK_EVENT_NAME:-}" in')
        sub(f, '    export CLAUDE_PROJECT_DIR="$_GIT_ROOT"',
            '    export CURSOR_PROJECT_DIR="$_GIT_ROOT"')
        sub(f, '    unset CLAUDE_PROJECT_DIR',
            '    unset CURSOR_PROJECT_DIR')
        sub(f, 'case "${CLAUDE_CODE_ENTRYPOINT:-cli}" in\n'
               '  cli|sdk-ts|sdk-cli|claude-desktop|claude-vscode) ;;',
            'case "${ECC_ENTRYPOINT:-cli}" in\n'
               '  cli|sdk-ts|sdk-cli|cursor) ;;')
        sub(f, '_ECC_SKIP_PATHS="${ECC_OBSERVE_SKIP_PATHS:-observer-sessions,.claude-mem}"',
            '_ECC_SKIP_PATHS="${ECC_OBSERVE_SKIP_PATHS:-observer-sessions,.ecc-mem}"')
        CHANGES.append("skills/continuous-learning-v2/hooks/observe.sh — Cursor env names")
    # --- session-guardian.sh path re-point REMOVED (D13 follow-up): the file
    # is now deleted by do_deletes(). (Was: OBSERVER_LAST_RUN_LOG default
    # ~/.claude/observer-last-run.log -> ~/.cursor/ecc/observer-last-run.log,
    # comment + LOG_PATH line.)
    f = os.path.join(BASE, "skills/continuous-learning-v2/agents/start-observer.sh")
    if exists(f):
        sub(f, "# to prevent claude CLI failures from killing the observer loop.",
            "# to prevent agent CLI failures from killing the observer loop.")
    # observer-loop.sh:121 — the claude CLI line (post-generic-pass text already
    # says Cursor; keep the stub note honest)
    maybe_resub(os.path.join(BASE, "skills/continuous-learning-v2/agents/observer-loop.sh"),
                r"# `claude` CLI, which has no Cursor equivalent\.",
                "# `claude` CLI, which has no Cursor equivalent.")

    # --- orchestrate built-tree leftovers (staged copies already edited;
    # these are maybe_resub so a no-op is fine) ---
    f = os.path.join(BASE, "new-skills/orchestrate/SKILL.md")
    if exists(f):
        maybe_resub(f, r"reportedly running on Opus", "reportedly running on another model")

    # --- fix-up round (audit #54 B1 / dry-run #26 M1 / sweep #16 F1+F3):
    # upstream re-staged files carrying non-Grok model strings that no
    # earlier rule touched. Verified upstream-identical in
    # /tmp/ecc-repo-clean, so the fix lives here, not in a staged source:
    # build.sh contains 0 mentions of "agent-compress" and does not stage
    # start-observer.sh / observe.sh from new-skills/ or round2-skills/.
    f = os.path.join(BASE, "scripts/lib/agent-compress.js")
    if exists(f):
        sub(f, "    model: frontmatter.model || 'sonnet',",
            "    model: frontmatter.model || 'cursor-grok-4.6-high-fast',")
    f = os.path.join(BASE, "skills/continuous-learning-v2/agents/start-observer.sh")
    if exists(f):
        sub(f, "# and creates instincts. Uses Haiku model for cost efficiency.",
            "# and creates instincts. Uses the fast-tier model for cost efficiency.")
    f = os.path.join(BASE, "skills/continuous-learning-v2/hooks/observe.sh")
    if exists(f):
        sub(f, "#   - ECC observing its own Haiku observer sessions (self-loop)",
            "#   - ECC observing its own observer sessions (self-loop)")

def main():
    global CHANGES, REMOVALS, NOTES, ERRORS
    do_deletes()
    edit_transcript_context()
    edit_agent_schema_and_emitters()
    edit_adapter()
    edit_model_route_and_common_performance()
    edit_astra_review()
    edit_gan_style_harness()
    edit_observer_loop()
    edit_plankton()
    edit_utils()
    edit_agent_data_home()
    edit_llm_summary_call_sites()
    edit_resolve_ecc_root()
    regenerate_inline_blobs()
    edit_installer()
    edit_installer_round2()
    edit_session_paths_round2()
    edit_context_profile_round2()
    edit_prose_round2()
    edit_misc_targeted()
    edit_manifests_and_schemas()
    generic_pass()
    edit_post_generic()
    check = self_check()
    log_lines = [
        "# fix16 run log",
        "",
        f"## Errors ({len(ERRORS)})",
    ]
    log_lines += [f"- {e}" for e in ERRORS] or ["- none"]
    log_lines += ["", f"## Notes ({len(NOTES)})"]
    log_lines += [f"- {n}" for n in NOTES] or ["- none"]
    log_lines += ["", f"## Changes ({len(CHANGES)})"]
    log_lines += [f"- {c}" for c in CHANGES]
    log_lines += ["", f"## Removals ({len(REMOVALS)})"]
    log_lines += [f"- {r}" for r in REMOVALS]
    log_lines += ["", "## Self-check", "", "```", check, "```", ""]
    log_dir = os.path.join(os.path.dirname(BASE.rstrip("/")), "fix16")
    os.makedirs(log_dir, exist_ok=True)
    with open(os.path.join(log_dir, "fix16-run-log.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(log_lines))
    print("\n".join(log_lines))
    print(f"\nERRORS: {len(ERRORS)}  NOTES: {len(NOTES)}  "
          f"CHANGES: {len(CHANGES)}  REMOVALS: {len(REMOVALS)}")
    return 1 if ERRORS else 0


if __name__ == "__main__":
    sys.exit(main())
