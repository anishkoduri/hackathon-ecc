#!/usr/bin/env python3
"""Supply-chain pinning, fix program #9: pin the 4 dry-run #8 minors plus the
remaining registry-fetching install instructions the sweep found.

Every version below was verified against the npm registry (npm view) BEFORE
writing it in:
- vercel 65.14.0, @railway/cli 5.71.0, supabase 3.1.0 (CLI),
  @supabase/supabase-js 2.119.0, @supabase/ssr 0.12.7,
  playwright 1.65.0 (matches export-pdf.sh, already pinned),
  ecc-agentshield 1.6.0, agent-browser 0.42.0, pm2 7.1.2,
  @openai/codex 0.167.1, @angular/aria 22.2.6, tailwindcss 4.3.5,
  @tailwindcss/postcss 4.3.5, postcss 8.5.32,
  @modelcontextprotocol/sdk 1.32.2, zod 4.6.7.

M1: README.md:29 (written by the build.sh heredoc) states the CBM
no-network/no-API-key claim as flat fact; append the same caveat as
skills/codebase-memory/SKILL.md:18. hackathon-mode.mdc:50 and
unified-memory SKILL.md:176 do NOT state the claim (verified) and are
left alone.
M2: deploy-fast SKILL.md — pin the three global CLI installs.
M3: app-scaffold SKILL.md + reference/best-practices.md — pin the Supabase
CLI (npx) and the client libs.
M4: polish-pass capture.mjs — pin the Playwright install + Chromium fetch
to 1.65.0 (matches export-pdf.sh).
Sweep: the remaining registry fetches live in upstream ECC files, copied
fresh on every build, so they are pinned by the build.sh patch block this
script inserts LAST (after the fix8 findings block, just before STEP 5),
following the fix8-findings pattern. Each substitution asserts exactly one
match in the built file.

Usage: python3 fix9-pins.py  (run from ~/workspace/hackathon-plugin)
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

FIX9_PATCH = '''
# --- Fix program #9: pin the remaining registry-fetching installs ---
# Upstream ECC files, copied fresh on every build — these fixes live here as a
# patch block placed LAST in build.sh, just before STEP 5, after all prior
# patches (including fix8 findings), whose old-strings the substitutions below
# are anchored on (i.e. against the CURRENT built text). Versions verified on
# npm (npm view) before writing. Never edit hackathon-ecc/ directly. Each
# substitution asserts exactly one match in its built file.
# Deliberately left unpinned (same class, not genuine fetches):
# - ui-to-vue SKILL.md:69 `npm install -g ui-to-vue-converter@1.0.2` and
#   unified-memory SKILL.md:22 `npm install -g ecc-universal@2.2.3` — already
#   pinned (fix #8).
# - app-scaffold troubleshooting.md:36 "Don't `npm install -g supabase`" —
#   prose that PROHIBITS the unpinned fetch.
# - ecc-react-build-resolver.md:169 `# npm i react@^<major> react-dom@^<major>`
#   — commented-out template with a <major> placeholder the agent fills in
#   from the project; no concrete version exists to pin.
# - scripts/lib/missing-dependency.js:51-52 — the install suggestion reads its
#   version from package.json dependencies (already pinned); the unversioned
#   branch fires only when package.json is unreachable, where no version
#   exists to pin to. It suggests; it never installs.
# - bare `npx <pkg>` invocations (npx tsc/vitest/eslint/prettier/prisma,
#   `npx ecc-agentshield scan`, `npx supabase` in prose) resolve an installed
#   binary first; no install is involved.
# - pip installs (bengali-nlp, django-*, frontend-slides html-template,
#   python-patterns) are a different package manager, outside this sweep's
#   npm scope; noted for a future pass, not pinned here.
python3 - "$PLUGIN_DIR" <<'PYEOF'
import os, sys
base = sys.argv[1]
subs = [
  # Sweep — security-scan: pin the global install.
  ("skills/security-scan/SKILL.md",
   r"""npm install -g ecc-agentshield""",
   r"""npm install -g ecc-agentshield@1.6.0"""),
  # Sweep — ecc-e2e-runner: pin the global install.
  ("agents/ecc-e2e-runner.md",
   r"""npm install -g agent-browser && agent-browser install""",
   r"""npm install -g agent-browser@0.42.0 && agent-browser install"""),
  # Sweep — pm2 command: pin the global install.
  ("commands/pm2.md",
   r"""npm install -g pm2""",
   r"""npm install -g pm2@7.1.2"""),
  # Sweep — astra-review codex.js: pin the version in the install hint.
  ("scripts/lib/astra-review/codex.js",
   r"""npm i -g @openai/codex""",
   r"""npm i -g @openai/codex@0.167.1"""),
  # Sweep — angular-aria: pin the conditional install.
  ("skills/angular-developer/references/angular-aria.md",
   r"""npm install @angular/aria""",
   r"""npm install @angular/aria@22.2.6"""),
  # Sweep — tailwind-css: pin all three installs.
  ("skills/angular-developer/references/tailwind-css.md",
   r"""npm install tailwindcss @tailwindcss/postcss postcss""",
   r"""npm install tailwindcss@4.3.5 @tailwindcss/postcss@4.3.5 postcss@8.5.32"""),
  # Sweep — mcp-server-patterns: pin both installs.
  ("skills/mcp-server-patterns/SKILL.md",
   r"""npm install @modelcontextprotocol/sdk zod""",
   r"""npm install @modelcontextprotocol/sdk@1.32.2 zod@4.6.7"""),
]
for rel, old, new in subs:
    p = os.path.join(base, rel)
    text = open(p, encoding="utf-8").read()
    assert text.count(old) == 1, f"{rel}: pattern not found exactly once: {old[:60]!r}"
    open(p, "w", encoding="utf-8").write(text.replace(old, new))
print("fix9: sweep registry pins applied (ecc-agentshield@1.6.0, agent-browser@0.42.0, pm2@7.1.2, codex@0.167.1, angular/aria@22.2.6, tailwindcss@4.3.5, postcss@8.5.32, sdk@1.32.2, zod@4.6.7)")
PYEOF
'''

print("== build.sh: M1 README CBM caveat ==")
edit(BUILD,
     "needs no network calls and no API key, and the plugin's `mcp.json` points at the installed binary.",
     "needs no network calls and no API key, and the plugin's `mcp.json` points at the installed binary. (Per the project's own docs — not independently verifiable from this plugin; the binary is neither bundled nor audited here.)")

print("== staged: M2 deploy-fast ==")
edit(f"{ROOT}/rewritten-skills/deploy-fast/SKILL.md",
     "npm i -g vercel",
     "npm i -g vercel@65.14.0")
edit(f"{ROOT}/rewritten-skills/deploy-fast/SKILL.md",
     "npm i -g @railway/cli",
     "npm i -g @railway/cli@5.71.0")
edit(f"{ROOT}/rewritten-skills/deploy-fast/SKILL.md",
     "npm i -g supabase            # or: npx supabase ...",
     "npm i -g supabase@3.1.0            # or: npx supabase@3.1.0 ...")

print("== staged: M3 app-scaffold ==")
edit(f"{ROOT}/rewritten-skills/app-scaffold/SKILL.md",
     "npx supabase --version",
     "npx supabase@3.1.0 --version")
edit(f"{ROOT}/rewritten-skills/app-scaffold/SKILL.md",
     "On Windows, use `npx supabase` in place of `supabase` in every command below.",
     "On Windows, use `npx supabase@3.1.0` in place of `supabase` in every command below.")
edit(f"{ROOT}/rewritten-skills/app-scaffold/SKILL.md",
     "npm install @supabase/supabase-js @supabase/ssr",
     "npm install @supabase/supabase-js@2.119.0 @supabase/ssr@0.12.7")
edit(f"{ROOT}/rewritten-skills/app-scaffold/reference/best-practices.md",
     "npm install @supabase/supabase-js @supabase/ssr",
     "npm install @supabase/supabase-js@2.119.0 @supabase/ssr@0.12.7")

print("== staged: M4 polish-pass capture.mjs ==")
edit(f"{ROOT}/round2-skills/polish-pass/scripts/capture.mjs",
     'run("npm", ["install", "--silent", "--no-audit", "--no-fund", "playwright"], CACHE);',
     'run("npm", ["install", "--silent", "--no-audit", "--no-fund", "playwright@1.65.0"], CACHE);')
edit(f"{ROOT}/round2-skills/polish-pass/scripts/capture.mjs",
     'run("npx", ["-y", "playwright", "install", "chromium"], process.cwd());',
     'run("npx", ["-y", "playwright@1.65.0", "install", "chromium"], process.cwd());')

print("== build.sh: fix9 sweep patch block (LAST, before STEP 5) ==")
edit(BUILD,
     '''print("fix8: F2 registry pins applied (ecc-universal@2.2.3, ccg-workflow@3.7.4)")
PYEOF

# STEP 5 — Counts''',
     '''print("fix8: F2 registry pins applied (ecc-universal@2.2.3, ccg-workflow@3.7.4)")
PYEOF
''' + FIX9_PATCH + '''
# STEP 5 — Counts''')

print("fix9: all pins applied (M1 caveat, M2 vercel/railway/supabase, M3 supabase CLI + client libs, M4 playwright@1.65.0, sweep x7)")
