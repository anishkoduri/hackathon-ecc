#!/usr/bin/env python3
"""Generate the AUDIT #1 patch section for build.sh from the pristine-vs-fixed diff.

Reads the pristine plugin (~/workspace/hackathon-plugin/hackathon-ecc, just
rebuilt by build.sh) and the fixed backup (~/workspace/hackathon-plugin-fixed-backup),
and emits Python code that applies each fix as an exact string replacement
with a count==1 assert, following build.sh's existing patch conventions.

Skipped (handled separately):
  - README.md ................. STEP 4 heredoc in build.sh is updated directly
  - agents/scout.md, agents/fast-worker.md, agents/deep-reasoner.md
    ................. staged sources in new-skills/orchestrate/agents/ synced
  - the 5 restored originals .. must not appear in the diff at all (checked)

Usage: python3 gen_audit1_patches.py > /tmp/audit1_section.py
"""
import difflib
import json
import sys

PRISTINE = "/home/hatch/workspace/hackathon-plugin/hackathon-ecc"
FIXED = "/home/hatch/workspace/hackathon-plugin-fixed-backup"

SKIP = {
    "README.md",
    "agents/scout.md",
    "agents/fast-worker.md",
    "agents/deep-reasoner.md",
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
    "skills/agents-md-generator",
    "skills/systematic-debugging",
    "skills/hackathon-pitch",
    "skills/ui-ux-pro-max",
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
        for l in open("/tmp/diff-files.txt", encoding="utf-8")
        if l.strip()
    ]
    for rel in diff_files:
        if any(rel.startswith(d + "/") or rel == d for d in FORBIDDEN_DIRS) or rel in FORBIDDEN:
            raise SystemExit(f"STOP: diff touches a restored original: {rel}")
    patched = [r for r in diff_files if r not in SKIP]
    github = [r for r in patched if any(r.startswith(d + "/") for d in GITHUB_FETCHED)]
    stock = [r for r in patched if r not in github]

    out = []
    out.append('# --- AUDIT #1 FIXES (Nov 9 audit; encoded from the pristine-vs-fixed diff) ---')
    out.append('# The Nov 9 audit applied ~200 fixes to the built plugin. This section')
    out.append('# re-applies them on every rebuild, after all STEP 3 patches above, so a')
    out.append('# fresh build.sh run reproduces the audited plugin byte-for-byte. Each')
    out.append('# replacement asserts an exact single match; a silent no-op fails the build.')
    out.append('# Files fall into two groups: ECC stock files (patched here) and skills')
    out.append('# fetched from GitHub by build.sh (agents-md-generator, systematic-debugging,')
    out.append('# hackathon-pitch, ui-ux-pro-max — no staged source exists, so patched here).')
    out.append('# Staged additions needed no patch: their staged sources already match the')
    out.append('# fixed plugin (orchestrate agents were synced to new-skills/orchestrate/agents/).')
    out.append('python3 - "$PLUGIN_DIR" <<\'PYEOF\'')
    out.append('import sys')
    out.append('base = sys.argv[1]')
    out.append('')
    out.append('def audit_patch(path, subs):')
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
            out.append(f'audit_patch(f"{{base}}/{rel}", [')
            for old, new in pairs:
                out.append(f'  ({lit(old)},')
                out.append(f'   {lit(new)}),')
            out.append('])')
        out.append('')
    out.append(f'print("audit #1 fixes applied: {len(patched)} files, {total_pairs} replacements")')
    out.append('PYEOF')
    print("\n".join(out))
    print(f"# SUMMARY files={len(patched)} stock={len(stock)} github={len(github)} pairs={total_pairs}", file=sys.stderr)


if __name__ == "__main__":
    main()
