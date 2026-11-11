#!/usr/bin/env python3
"""fix10-m5.py — Fix program #10, M5: pin the macOS Supabase CLI install.

Dry-run #9 found the macOS Supabase CLI install unpinned in three places
(all in the app-scaffold restored original, staged at
rewritten-skills/app-scaffold/ and copied verbatim into the built plugin by
build.sh:247-249 — no build.sh patch block anchors on these strings, so the
fix edits the staged sources directly).

Pin target: supabase@3.1.0 (the version fix #9 already pinned for the
npx/Windows paths). Homebrew's tap has no version-pin mechanism for this
formula, so the macOS path switches to the pinned npx form, which is already
a sanctioned alternative in SKILL.md:56's own comment.

Edits:
 1. SKILL.md macOS section: brew install -> pinned npx verify; the
    "On Windows, use npx ..." sentence becomes "On macOS and Windows, use
    npx ..." so the substitution rule covers both platforms.
 2. scripts/bootstrap.sh: section 3 resolves the CLI as the SUPABASE array
    (npx supabase@3.1.0) with a fail-fast npx check; every later bare
    `supabase` call goes through "${SUPABASE[@]}"; final message updated.
 3. reference/troubleshooting.md:36: brew line + bare `npx supabase`
    fallback -> pinned npx form. :26: `brew upgrade supabase` (same
    unpinned-CLI-fetch family) -> pinned npx form.
 4. build.sh: one comment line in the fix9 block drops the now-stale
    "`npx supabase` in prose" example (no bare `npx supabase` remains
    after this fix); the fix9 prohibition note about troubleshooting.md:36
    is untouched and still accurate.

Out of scope (explicitly): `brew install --cask docker` (no version-pin
mechanism for casks); reset-db.sh's bare `supabase` invocations (invocations
of an already-installed CLI, not installs — covered by the skill's
"in place of `supabase`" substitution sentence, same as SKILL.md steps 2+).

Each substitution asserts exactly one match. Run from
~/workspace/hackathon-plugin. Does NOT rebuild (caller does that).
"""
import sys

ROOT = "/home/hatch/workspace/hackathon-plugin"


def sub(path, old, new, label):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    n = text.count(old)
    assert n == 1, f"{label}: expected exactly 1 match in {path}, found {n}"
    with open(path, "w", encoding="utf-8") as f:
        f.write(text.replace(old, new))
    print(f"OK {label}")


BASE = ROOT + "/rewritten-skills/app-scaffold"

# --- 1. SKILL.md: macOS install block ---------------------------------------
sub(BASE + "/SKILL.md",
    "# Supabase CLI (do NOT install globally with npm — use Homebrew or npx)\n"
    "brew install supabase/tap/supabase\n"
    "\n"
    "# Verify\n"
    "docker --version\n"
    "supabase --version\n",
    "# Supabase CLI — use npx, pinned to 3.1.0 (do NOT install globally with npm;\n"
    "# Homebrew's tap has no version pin, so it would install latest)\n"
    "\n"
    "# Verify\n"
    "docker --version\n"
    "npx supabase@3.1.0 --version\n",
    "SKILL.md macOS install block -> pinned npx")

# --- 1b. SKILL.md: substitution sentence covers both platforms --------------
sub(BASE + "/SKILL.md",
    "On Windows, use `npx supabase@3.1.0` in place of `supabase` in every command below.",
    "On macOS and Windows, use `npx supabase@3.1.0` in place of `supabase` in every command below.",
    "SKILL.md substitution sentence -> macOS + Windows")

# --- 2. bootstrap.sh: section 3 -> pinned SUPABASE array --------------------
sub(BASE + "/scripts/bootstrap.sh",
    "# --- 3. Supabase CLI ---------------------------------------------------------\n"
    "if ! command -v supabase >/dev/null 2>&1; then\n"
    "  info \"Installing Supabase CLI...\"\n"
    "  brew install supabase/tap/supabase\n"
    "fi\n"
    "ok \"Supabase CLI: $(supabase --version)\"\n",
    "# --- 3. Supabase CLI ---------------------------------------------------------\n"
    "# Pinned to 3.1.0 via npx: Homebrew's tap has no version pin, and a global\n"
    "# npm install is unsupported. npx caches the pinned version after the first\n"
    "# run, so later calls are fast. Every CLI call in this script goes through\n"
    "# $SUPABASE, so the pinned version is what actually runs.\n"
    "if ! command -v npx >/dev/null 2>&1; then\n"
    "  warn \"npx not found. Install Node.js (https://nodejs.org) then re-run.\"\n"
    "  exit 1\n"
    "fi\n"
    "SUPABASE=(npx supabase@3.1.0)\n"
    "ok \"Supabase CLI: $(\"${SUPABASE[@]}\" --version)\"\n",
    "bootstrap.sh section 3 -> pinned SUPABASE array")

# --- 2b. bootstrap.sh: later bare calls go through the array -----------------
sub(BASE + "/scripts/bootstrap.sh",
    "  supabase init\n",
    "  \"${SUPABASE[@]}\" init\n",
    "bootstrap.sh supabase init -> array")
sub(BASE + "/scripts/bootstrap.sh",
    "supabase start\n",
    "\"${SUPABASE[@]}\" start\n",
    "bootstrap.sh supabase start -> array")
sub(BASE + "/scripts/bootstrap.sh",
    "supabase db reset\n",
    "\"${SUPABASE[@]}\" db reset\n",
    "bootstrap.sh supabase db reset -> array")
sub(BASE + "/scripts/bootstrap.sh",
    "supabase gen types typescript --local > src/lib/database.types.ts\n",
    "\"${SUPABASE[@]}\" gen types typescript --local > src/lib/database.types.ts\n",
    "bootstrap.sh supabase gen types -> array")
sub(BASE + "/scripts/bootstrap.sh",
    "ok \"Done. Run 'supabase status' to see your local URLs and keys.\"\n",
    "ok \"Done. Run 'npx supabase@3.1.0 status' to see your local URLs and keys.\"\n",
    "bootstrap.sh final message -> pinned npx")

# --- 3. troubleshooting.md:36 install line + :26 upgrade line ----------------
sub(BASE + "/reference/troubleshooting.md",
    "Install it: `brew install supabase/tap/supabase`. Don't `npm install -g supabase` (unsupported) — use Homebrew or `npx supabase`.",
    "Install it: run `npx supabase@3.1.0 --version` (pinned 3.1.0 — Homebrew's tap has no version pin). Don't `npm install -g supabase` (unsupported) — use `npx supabase@3.1.0` in place of `supabase` in every command.",
    "troubleshooting.md:36 -> pinned npx")
sub(BASE + "/reference/troubleshooting.md",
    "Recent Supabase images are multi-arch; update the CLI (`brew upgrade supabase`) and Docker Desktop.",
    "Recent Supabase images are multi-arch; update the CLI to the pinned version (`npx supabase@3.1.0 --version`) and Docker Desktop.",
    "troubleshooting.md:26 brew upgrade -> pinned npx")

# --- 4. build.sh: fix9 comment — drop the now-stale npx supabase example ----
sub(ROOT + "/build.sh",
    "# - bare `npx <pkg>` invocations (npx tsc/vitest/eslint/prettier/prisma,\n"
    "#   `npx ecc-agentshield scan`, `npx supabase` in prose) resolve an installed\n"
    "#   binary first; no install is involved.\n",
    "# - bare `npx <pkg>` invocations (npx tsc/vitest/eslint/prettier/prisma,\n"
    "#   `npx ecc-agentshield scan`) resolve an installed binary first; no install\n"
    "#   is involved.\n",
    "build.sh fix9 comment: drop stale npx supabase example")

print("fix10-m5: all substitutions applied")
