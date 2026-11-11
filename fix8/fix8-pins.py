#!/usr/bin/env python3
"""Supply-chain pinning (fix program #8): pin the 5 unpinned items from the
Nov 10 security audit to verified versions, in staged sources and build.sh.

Every version/tag/SHA below was verified upstream BEFORE writing:
- Clone SHAs: each is its repo's current HEAD (git ls-remote), equal to the
  local cache HEAD, so the pin freezes exactly the audited content. Release
  tags exist for ECC (v2.2.3), ui-ux-pro-max (v2.15.0), chwezi (v1.1.0) but
  point at EARLIER commits than the audited HEADs, so a tag pin would roll
  back audited content. The other three repos have no tags at all.
- npm versions: latest per `npm view` (create-next-app 16.4.6,
  @angular/cli 22.2.6, shadcn 4.23.0, create-nuxt 4.0.3, playwright 1.65.0,
  remotion 4.0.542).
- Playwright Chromium revision 1254: from playwright-core@1.65.0
  browsers.json (npm pack, read directly).
- CBM installer tag v0.12.1: tag exists (a7158ac2...); install.sh and
  install.ps1 both return HTTP 200 at that tag.

Usage: python3 fix8-pins.py  (run from ~/workspace/hackathon-plugin)
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

PIN_BLOCK = '''
# --- Supply-chain pins (pinned Nov 10, 2026, on the Audit #35 zero-error tree) ---
# Every upstream clone is pinned to the exact commit the audited plugin was
# built from. Each SHA below was verified as its repo's current HEAD
# (git ls-remote). Release tags exist for ECC (v2.2.3), ui-ux-pro-max
# (v2.15.0) and chwezi-dev-engine (v1.1.0), but those tags point at EARLIER
# commits than the audited HEADs, so a tag pin would roll back audited
# content -- the SHA pin freezes exactly what was audited. The other three
# repos have no tags at all, so a SHA is the only pin available. Never
# clone HEAD: a rebuild must produce the same tree.
ECC_PIN="d2ef2680594f9a17526a6e1a2e18b3d242c5d17b"
UIPRO_PIN="6ae86f61f520d6ca229d2f40e070410638c908c5"
MARKETPLACE_PIN="f210c6d05b10a6a17c5cf67d7b7d13565d1f5dc9"
CHWEZI_PIN="d7d85b6e2687cad33e0f3cc826ae835c423e83ae"
FLECTO_PIN="3a0f7e52cdb53c52494c7c34235001a042dd9822"
AGENTSKILLS_PIN="c13e8b35d44085accc7ec3b1b4410247d4969514"

# Check out the pinned commit in an existing clone (fetch it first if the
# shallow clone does not contain it yet). Fails the build if the pin cannot
# be satisfied -- a build from unpinned code must never succeed silently.
pin_checkout() { # $1 = repo dir, $2 = pinned SHA
  if ! git -C "$1" rev-parse --verify -q "$2^{commit}" >/dev/null 2>&1; then
    git -C "$1" fetch --quiet --depth 1 origin "$2" 2>/dev/null || git -C "$1" fetch --quiet origin "$2"
  fi
  git -C "$1" checkout --quiet "$2"
  [ "$(git -C "$1" rev-parse HEAD)" = "$2" ] || { echo "[build] ERROR: could not pin $1 to $2" >&2; exit 1; }
}
# Shallow-clone a repo, then check out the pinned commit.
pin_clone() { # $1 = owner/repo, $2 = dir, $3 = pinned SHA
  git clone --depth 1 --quiet "https://github.com/$1" "$2"
  pin_checkout "$2" "$3"
}
'''

PIN_PATCH = '''
# --- Supply-chain pins: @latest / unpinned installs (pinned Nov 10, 2026) ---
# Versions verified against the npm registry (npm view) and the
# playwright-core 1.65.0 browsers.json (Chromium revision 1254) before
# writing them in. No other patch block references these files, so this
# block's placement before the fix6-batch-4 / fix7 late blocks is safe.
# The clone pins (item 1) are shell edits in STEP 2, not patches here.
python3 - "$PLUGIN_DIR" <<'PYEOF'
import os, sys
base = sys.argv[1]

def pin(rel, old, new, count=1):
    p = os.path.join(base, rel)
    text = open(p, encoding="utf-8").read()
    n = text.count(old)
    assert n == count, f"{rel}: expected {count} occurrence(s) of {old[:60]!r}, found {n}"
    open(p, "w", encoding="utf-8").write(text.replace(old, new))

# (2) angular-developer (ECC-derived): @angular/cli@latest -> 22.2.6.
# The prose above the command said "fetch the latest version" -- it now
# names the pinned version so the file stays self-consistent.
pin("skills/angular-developer/SKILL.md",
    "you must use `npx` to fetch the latest version.",
    "you must use `npx` to fetch the pinned version (`@angular/cli@22.2.6`).")
pin("skills/angular-developer/SKILL.md",
    "- **Command:** `npx @angular/cli@latest new <project-name>`",
    "- **Command:** `npx @angular/cli@22.2.6 new <project-name>`")

# (2) ui-ux-pro-max data (upstream clone): shadcn@latest (15x) -> 4.23.0,
# npm create nuxt@latest (2x) -> create-nuxt 4.0.3. (The "nuxt-ui 4.12.0"
# column in nuxt-ui.csv is the template's UI version, not the scaffolder.)
pin("skills/ui-ux-pro-max/data/stacks/shadcn.csv", "shadcn@latest", "shadcn@4.23.0", 15)
pin("skills/ui-ux-pro-max/data/stacks/nuxt-ui.csv", "npm create nuxt@latest", "npm create nuxt@4.0.3", 2)

# (3) frontend-slides export-pdf.sh (ECC-derived): playwright -> 1.65.0.
# The version pin is what pins Chromium: playwright 1.65.0 ships Chromium
# revision 1254 (playwright-core browsers.json), so the npx install of the
# pinned CLI downloads exactly that revision. The revision is recorded in
# the comment so a future version bump knows to re-check browsers.json.
pin("skills/frontend-slides/scripts/export-pdf.sh",
    "# Ensure Chromium browser binary is downloaded",
    "# Ensure Chromium browser binary is downloaded (playwright 1.65.0 ships Chromium revision 1254)")
pin("skills/frontend-slides/scripts/export-pdf.sh",
    "npm install playwright &>/dev/null || {",
    "npm install playwright@1.65.0 &>/dev/null || {")
pin("skills/frontend-slides/scripts/export-pdf.sh",
    '    err "Try running: npm install playwright"',
    '    err "Try running: npm install playwright@1.65.0"')
pin("skills/frontend-slides/scripts/export-pdf.sh",
    "npx playwright install chromium 2>/dev/null || {",
    "npx playwright@1.65.0 install chromium 2>/dev/null || {")
pin("skills/frontend-slides/scripts/export-pdf.sh",
    '    err "Try running manually: npx playwright install chromium"',
    '    err "Try running manually: npx playwright@1.65.0 install chromium"')

print("supply-chain pins applied: angular 22.2.6, shadcn 4.23.0, nuxt 4.0.3, playwright 1.65.0 / chromium r1254")
PYEOF
'''

print("== build.sh: pin constants + helpers ==")
edit(BUILD, 'MS_SRC="/tmp/hack-skills/skills"\n', 'MS_SRC="/tmp/hack-skills/skills"\n' + PIN_BLOCK)

print("== build.sh: ECC clone guard + pin enforcement ==")
edit(BUILD,
     '''  git clone --depth 1 --quiet https://github.com/affaan-m/ecc "$ECC_REPO"
fi
[ -f "$ECC_REPO/install.sh" ] || { echo "[build] ERROR: ECC repo has no install.sh" >&2; exit 1; }''',
     '''  pin_clone "affaan-m/ecc" "$ECC_REPO" "$ECC_PIN"
fi
[ -f "$ECC_REPO/install.sh" ] || { echo "[build] ERROR: ECC repo has no install.sh" >&2; exit 1; }
# Enforce the pin even when the repo already exists: the installer below must
# run the pinned checkout, not whatever commit a stale cache sits at.
pin_checkout "$ECC_REPO" "$ECC_PIN"''')

print("== build.sh: ui-ux-pro-max clone ==")
edit(BUILD,
     '''if [ -d "$UIPRO_DIR/.git" ]; then
  git -C "$UIPRO_DIR" pull --quiet || true
else
  git clone --depth 1 --quiet https://github.com/nextlevelbuilder/ui-ux-pro-max-skill "$UIPRO_DIR"
fi''',
     '''if [ -d "$UIPRO_DIR/.git" ]; then
  pin_checkout "$UIPRO_DIR" "$UIPRO_PIN"
else
  pin_clone "nextlevelbuilder/ui-ux-pro-max-skill" "$UIPRO_DIR" "$UIPRO_PIN"
fi''')

print("== build.sh: marketplace clone ==")
edit(BUILD,
     '''if [ -d "$MS_DIR/.git" ]; then
  git -C "$MS_DIR" pull --quiet || true
else
  git clone --depth 1 --quiet https://github.com/asadullah48/hackathon-skills-marketplace "$MS_DIR"
fi''',
     '''if [ -d "$MS_DIR/.git" ]; then
  pin_checkout "$MS_DIR" "$MARKETPLACE_PIN"
else
  pin_clone "asadullah48/hackathon-skills-marketplace" "$MS_DIR" "$MARKETPLACE_PIN"
fi''')

print("== build.sh: fetch_repo + call sites ==")
edit(BUILD,
     '''fetch_repo() { # $1 = owner/repo, $2 = local dir name
  local dest="$SKILL_SRC/$2"
  if [ -d "$dest/.git" ]; then
    git -C "$dest" pull --quiet || true
  else
    git clone --depth 1 --quiet "https://github.com/$1" "$dest"
  fi
}
mkdir -p "$SKILL_SRC"
fetch_repo "peterbamuhigire/chwezi-dev-engine" "chwezi-dev-engine"
fetch_repo "andomo3/flecto-shade" "flecto-shade"
fetch_repo "asrayg/hackathon-agent-skills" "hackathon-agent-skills"''',
     '''fetch_repo() { # $1 = owner/repo, $2 = local dir name, $3 = pinned SHA
  local dest="$SKILL_SRC/$2"
  if [ -d "$dest/.git" ]; then
    pin_checkout "$dest" "$3"
  else
    pin_clone "$1" "$dest" "$3"
  fi
}
mkdir -p "$SKILL_SRC"
fetch_repo "peterbamuhigire/chwezi-dev-engine" "chwezi-dev-engine" "$CHWEZI_PIN"
fetch_repo "andomo3/flecto-shade" "flecto-shade" "$FLECTO_PIN"
fetch_repo "asrayg/hackathon-agent-skills" "hackathon-agent-skills" "$AGENTSKILLS_PIN"''')

print("== build.sh: pin patch block (before fix6 batch 4) ==")
edit(BUILD,
     '''print("fix6 batch 3: gan-build M9 applied")
PYEOF

# --- Fix program #6, Batch 4: ui-ux-pro-max — design-token source is the''',
     '''print("fix6 batch 3: gan-build M9 applied")
PYEOF
''' + PIN_PATCH + '''
# --- Fix program #6, Batch 4: ui-ux-pro-max — design-token source is the''')

print("== staged: app-scaffold create-next-app ==")
edit(f"{ROOT}/rewritten-skills/app-scaffold/SKILL.md",
     "npx create-next-app@latest your-app --ts --tailwind --app",
     "npx create-next-app@16.4.6 your-app --ts --tailwind --app")

print("== staged: codebase-memory installer pins ==")
edit(f"{ROOT}/new-skills/codebase-memory/SKILL.md",
     "https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.ps1",
     "https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/v0.12.1/install.ps1")
edit(f"{ROOT}/new-skills/codebase-memory/SKILL.md",
     "https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.sh",
     "https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/v0.12.1/install.sh")

print("== staged: remotion pins ==")
edit(f"{ROOT}/new-skills/pitch-deck-video/template/scripts/build.mjs",
     "run('npx', ['remotion', 'render', 'src/index.ts', 'Demo', 'out/demo.mp4',",
     "run('npx', ['remotion@4.0.542', 'render', 'src/index.ts', 'Demo', 'out/demo.mp4',")
edit(f"{ROOT}/new-skills/pitch-deck-video/template/scripts/qa.mjs",
     "execFileSync('npx', ['remotion', 'still', 'src/index.ts', 'Demo', file, `--frame=${p.frame}`, '--log=error'], {",
     "execFileSync('npx', ['remotion@4.0.542', 'still', 'src/index.ts', 'Demo', file, `--frame=${p.frame}`, '--log=error'], {")

print("ALL PIN EDITS APPLIED")
