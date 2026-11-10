#!/usr/bin/env python3
"""Generate the AUDIT #2 FIXES patch section for build.sh from the pristine-vs-fixed diff.

Reads the pristine plugin (~/workspace/.audit2-sync/pristine, built by
build.sh BEFORE the Audit #2 section was added) and the fixed backup
(~/workspace/hackathon-plugin-audit2-fixed-backup), and emits Python code
that applies each fix as an exact string replacement with a count==1
assert, following build.sh's existing patch conventions (same pattern as
gen_audit1_patches.py / gen_qc_patches.py).

Skipped (handled separately, NOT a bug):
  - README.md ................. STEP 4 heredoc in build.sh is updated directly
  - agents/deep-reasoner.md ... staged source new-skills/orchestrate/agents/ synced
  - rules/hackathon-mode.mdc .. staged source new-rules/ synced
  - skills/feature-expansion/SKILL.md
    ........................... staged source new-skills/feature-expansion/ synced
  - skills/less-flat-ui/SKILL.md
    ........................... staged source ~/workspace/cursor-skills/less-flat-ui synced
  - skills/orchestrate/SKILL.md, skills/orchestrate/references/agent-TEMPLATE.md
    ........................... staged sources new-skills/orchestrate/ synced

Refuses to run if a restored original (hackathon-scope, deploy-fast,
app-scaffold, api-integration, readme-writer) would be touched — those
are covered by staged sources in rewritten-skills/, not by build.sh patches.

To regenerate after the pristine snapshot is gone: copy build.sh aside,
delete the AUDIT #2 FIXES section from the copy, run the copy (it builds
~/workspace/hackathon-plugin/hackathon-ecc without the Audit #2 fixes),
snapshot that plugin as the PRISTINE dir below, and re-run this script.

Usage: python3 gen_audit2_patches.py > ~/workspace/.audit2-sync/audit2_section.py
"""
import difflib
import json
import sys

PRISTINE = "/home/hatch/workspace/.audit2-sync/pristine"
FIXED = "/home/hatch/workspace/hackathon-plugin-audit2-fixed-backup"

SKIP = {
    "README.md",
    "agents/deep-reasoner.md",
    "rules/hackathon-mode.mdc",
    "skills/feature-expansion/SKILL.md",
    "skills/less-flat-ui/SKILL.md",
    "skills/orchestrate/SKILL.md",
    "skills/orchestrate/references/agent-TEMPLATE.md",
}
FORBIDDEN = {
    "skills/hackathon-scope/SKILL.md",
    "skills/deploy-fast/SKILL.md",
    "skills/app-scaffold/SKILL.md",
    "skills/api-integration/SKILL.md",
    "skills/readme-writer/SKILL.md",
}
# Any file under these skill dirs is a restored original.
FORBIDDEN_DIRS = {
    "skills/hackathon-scope",
    "skills/deploy-fast",
    "skills/app-scaffold",
    "skills/api-integration",
    "skills/readme-writer",
}

GITHUB_FETCHED = {
    # Fetched from GitHub by build.sh (marketplace, ui-ux-pro-max, MIT repos);
    # no staged source exists, so patched here.
    "skills/agents-md-generator",
    "skills/systematic-debugging",
    "skills/hackathon-pitch",
    "skills/ui-ux-pro-max",
    "skills/dispatching-parallel-agents",
    "skills/brainstorming",
    "skills/verification-before-completion",
    "skills/ai-feature-spec",
    "skills/devpost-autofiller",
}


def lit(block: str) -> str:
    """Emit a Python string literal for block (single or multi-line)."""
    if "\n" not in block:
        return json.dumps(block)
    if "\\" not in block and '"""' not in block and not block.endswith('"'):
        return '"""' + block + '"""'
    return repr(block)


def hunks_for(rel: str):
    """Return list of (old, new) exact-replacement pairs for one file."""
    with open(f"{PRISTINE}/{rel}", encoding="utf-8") as f:
        p_text = f.read()
    with open(f"{FIXED}/{rel}", encoding="utf-8") as f:
        f_text = f.read()
    p_lines = p_text.split("\n")
    f_lines = f_text.split("\n")
    # split("\n") leaves a trailing "" if the file ends with \n; keep it so
    # joins round-trip exactly.
    sm = difflib.SequenceMatcher(a=p_lines, b=f_lines, autojunk=False)
    pairs = []
    for group in sm.get_grouped_opcodes(3):
        i1, i2 = group[0][1], group[-1][2]
        j1, j2 = group[0][3], group[-1][4]
        ctx = 3
        while True:
            a1 = max(0, i1 - ctx)
            a2 = min(len(p_lines), i2 + ctx)
            old = "\n".join(p_lines[a1:a2])
            # map the expanded pristine span onto the fixed side: the
            # expansion adds equal context lines on both sides.
            b1 = j1 - (i1 - a1)
            b2 = j2 + (a2 - i2)
            new = "\n".join(f_lines[b1:b2])
            if old == new:
                break  # context-only group (should not happen)
            if p_text.count(old) == 1:
                pairs.append((old, new))
                break
            if a1 == 0 and a2 == len(p_lines):
                raise SystemExit(
                    f"{rel}: hunk still not unique at whole-file context:\n{old[:200]}"
                )
            ctx += 3
    return pairs


def main():
    diff_files = [
        l.strip()
        for l in open("/home/hatch/workspace/.audit2-sync/rel-files.txt", encoding="utf-8")
        if l.strip()
    ]
    for rel in diff_files:
        if any(rel.startswith(d + "/") or rel == d for d in FORBIDDEN_DIRS) or rel in FORBIDDEN:
            raise SystemExit(f"STOP: diff touches a restored original: {rel}")
    patched = [r for r in diff_files if r not in SKIP]
    github = [r for r in patched if any(r.startswith(d + "/") for d in GITHUB_FETCHED)]
    stock = [r for r in patched if r not in github]

    out = []
    out.append('# --- AUDIT #2 FIXES (Nov 9 Audit #2; encoded from the pristine-vs-fixed diff) ---')
    out.append('# Audit #2 applied fixes to the built plugin. This section re-applies')
    out.append('# them on every rebuild, after all STEP 3 patches above (including the')
    out.append('# AUDIT #1 FIXES, the paths:->globs: rename, and the QUALITY CHECK')
    out.append('# FIXES), so a fresh build.sh run reproduces the audited plugin')
    out.append('# byte-for-byte. Each replacement asserts an exact single match; a')
    out.append('# silent no-op fails the build. Files fall into two groups: ECC stock')
    out.append('# files (patched here) and skills fetched from GitHub by build.sh')
    out.append('# (ui-ux-pro-max — no staged source exists, so patched here). The 6')
    out.append('# staged-source files Audit #2 fixed are NOT patched here: their staged')
    out.append('# sources were fixed too, so build.sh reproduces them by copying the')
    out.append('# staged source (deep-reasoner, hackathon-mode, feature-expansion,')
    out.append('# less-flat-ui, orchestrate + agent-TEMPLATE). README.md is written by')
    out.append('# the STEP 4 heredoc, edited directly.')
    out.append('python3 - "$PLUGIN_DIR" <<\'PYEOF\'')
    out.append('import sys')
    out.append('base = sys.argv[1]')
    out.append('')
    out.append('def audit2_patch(path, subs):')
    out.append('    text = open(path, encoding="utf-8").read()')
    out.append('    for old, new in subs:')
    out.append('        assert text.count(old) == 1, f"{path}: pattern not found exactly once: {old[:70]}"')
    out.append('        text = text.replace(old, new)')
    out.append('    open(path, "w", encoding="utf-8").write(text)')
    out.append('')

    total_pairs = 0
    for group_name, group in [
        ("ECC stock", stock),
        ("GitHub-fetched (no staged source)", github),
    ]:
        out.append(f'# --- {group_name}: {len(group)} files ---')
        for rel in group:
            pairs = hunks_for(rel)
            total_pairs += len(pairs)
            out.append(f'audit2_patch(f"{{base}}/{rel}", [')
            for old, new in pairs:
                out.append(f'  ({lit(old)},')
                out.append(f'   {lit(new)}),')
            out.append('])')
        out.append('')
    out.append(f'print("audit #2 fixes applied: {len(patched)} files, {total_pairs} replacements")')
    out.append('PYEOF')
    print("\n".join(out))
    print(f"# SUMMARY files={len(patched)} stock={len(stock)} github={len(github)} pairs={total_pairs}", file=sys.stderr)


if __name__ == "__main__":
    main()
