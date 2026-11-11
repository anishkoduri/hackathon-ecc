#!/usr/bin/env python3
"""Fix program #8 (findings): fix the 2 low-severity findings from the
security re-scan on the pinned, quiescent tree (F1, F2).

F1: codebase-memory SKILL.md:18 states the binary's no-network / no-telemetry
/ no-API-key claim as flat fact with no unverifiability caveat. Add the
caveat next to the claim; the claim itself, the stale-installer-skill
documentation (:59-64) and the Defender false-positive note are untouched.
The skill is copied verbatim from staged sources, so no build.sh patch is
needed for F1.

F2: three unpinned registry-fetching npx/npm instructions outside the 5
pinned items (same supply-chain class as pin item 2). Versions verified on
npm before writing: ecc-universal 2.2.3, ccg-workflow 3.7.4. These files come
from the ECC clone, so the fixes live as a build.sh patch block placed LAST,
just before STEP 5, after all prior patches (incl. fix7). Deliberately NOT
touched: the mcp-dependency-review classifier example mentioning
`npx --package ecc-universal ecc` (prose, not a runnable instruction), the
other bare `npx <pkg>` mentions that resolve the project's local binary
first, and the prose @latest mentions that prohibit/describe @latest.

Usage: python3 fix8-findings.py  (run from ~/workspace/hackathon-plugin)
Exits nonzero if any replacement does not match exactly once.
"""
import sys

ROOT = "/home/hatch/workspace/hackathon-plugin"


def edit(path, old, new, count=1):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    n = text.count(old)
    assert n == count, f"{path}: expected {count} occurrence(s) of {old[:70]!r}, found {n}"
    with open(path, "w", encoding="utf-8") as f:
        f.write(text.replace(old, new))
    print(f"  ok: {path.split('hackathon-plugin/')[-1]} :: {old[:60]!r}")


BUILD = f"{ROOT}/build.sh"

print("== F1: staged codebase-memory caveat ==")
edit(f"{ROOT}/new-skills/codebase-memory/SKILL.md",
     "the intelligence. No network calls, no telemetry, no API key.",
     "the intelligence. No network calls, no telemetry, no API key. "
     "(Per the project's own docs \u2014 not independently verifiable from "
     "this plugin; the binary is neither bundled nor audited here.)")

PATCH_BLOCK = """
# --- Fix program #8 (findings): pin the three unpinned registry-fetching
# npx/npm instructions the security re-scan found outside the 5 pinned items
# (F2) ---
# Upstream ECC files, copied fresh on every build — these fixes live here as a
# patch block placed LAST in build.sh, just before STEP 5, after all prior
# patches (including fix7), whose old-strings the substitutions below are
# anchored on (i.e. against the CURRENT built text). Versions verified on npm
# before writing: ecc-universal 2.2.3, ccg-workflow 3.7.4. Never edit
# hackathon-ecc/ directly. Each substitution asserts exactly one match. The
# mcp-dependency-review classifier example mentioning `npx --package
# ecc-universal ecc` is prose, not a runnable instruction, and is
# deliberately left unpinned.
python3 - "$PLUGIN_DIR" <<'PYEOF'
import os, sys
base = sys.argv[1]
subs = [
  # F2 — loop-status: pin the packaged CLI invocation.
  ("commands/loop-status.md",
   r'''npx --package ecc-universal ecc loop-status --json''',
   r'''npx --package ecc-universal@2.2.3 ecc loop-status --json'''),
  # F2 — unified-memory: pin the global install.
  ("skills/unified-memory/SKILL.md",
   r'''npm install -g ecc-universal''',
   r'''npm install -g ecc-universal@2.2.3'''),
  # F2 — multi-* commands: pin the ccg-workflow prerequisite (both mentions).
  ("commands/multi-backend.md",
   r'''Initialize it with `npx ccg-workflow` to provision''',
   r'''Initialize it with `npx ccg-workflow@3.7.4` to provision'''),
  ("commands/multi-backend.md",
   r'''Requires the external ccg-workflow runtime (`npx ccg-workflow`)''',
   r'''Requires the external ccg-workflow runtime (`npx ccg-workflow@3.7.4`)'''),
  ("commands/multi-execute.md",
   r'''Initialize it with `npx ccg-workflow` to provision''',
   r'''Initialize it with `npx ccg-workflow@3.7.4` to provision'''),
  ("commands/multi-execute.md",
   r'''Requires the external ccg-workflow runtime (`npx ccg-workflow`)''',
   r'''Requires the external ccg-workflow runtime (`npx ccg-workflow@3.7.4`)'''),
  ("commands/multi-frontend.md",
   r'''Initialize it with `npx ccg-workflow` to provision''',
   r'''Initialize it with `npx ccg-workflow@3.7.4` to provision'''),
  ("commands/multi-frontend.md",
   r'''Requires the external ccg-workflow runtime (`npx ccg-workflow`)''',
   r'''Requires the external ccg-workflow runtime (`npx ccg-workflow@3.7.4`)'''),
  ("commands/multi-plan.md",
   r'''Initialize it with `npx ccg-workflow` to provision''',
   r'''Initialize it with `npx ccg-workflow@3.7.4` to provision'''),
  ("commands/multi-plan.md",
   r'''Requires the external ccg-workflow runtime (`npx ccg-workflow`)''',
   r'''Requires the external ccg-workflow runtime (`npx ccg-workflow@3.7.4`)'''),
  ("commands/multi-workflow.md",
   r'''Initialize it with `npx ccg-workflow` to provision''',
   r'''Initialize it with `npx ccg-workflow@3.7.4` to provision'''),
  ("commands/multi-workflow.md",
   r'''Requires the external ccg-workflow runtime (`npx ccg-workflow`)''',
   r'''Requires the external ccg-workflow runtime (`npx ccg-workflow@3.7.4`)'''),
]
for rel, old, new in subs:
    p = os.path.join(base, rel)
    text = open(p, encoding="utf-8").read()
    assert text.count(old) == 1, f"{rel}: pattern not found exactly once: {old[:60]!r}"
    open(p, "w", encoding="utf-8").write(text.replace(old, new))
print("fix8: F2 registry pins applied (ecc-universal@2.2.3, ccg-workflow@3.7.4)")
PYEOF
"""

print("== F2: build.sh patch block (LAST, just before STEP 5) ==")
edit(BUILD, "# STEP 5 \u2014 Counts", PATCH_BLOCK.strip("\n") + "\n\n# STEP 5 \u2014 Counts")

print("ALL FIX8-FINDINGS EDITS APPLIED")
