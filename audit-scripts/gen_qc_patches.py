#!/usr/bin/env python3
"""Generate the QUALITY CHECK FIXES patch section for build.sh.

Compares the plugin before the quality-check fixes (/tmp/qc-before) with the
fixed plugin (~/workspace/hackathon-plugin/hackathon-ecc) and emits Python
code that re-applies each fix as an exact string replacement with a
count==1 assert, following build.sh's existing patch conventions.

Excluded from the patch (handled separately, NOT a bug):
  - The 6 staged-source files the quality check fixed (deploy-fast,
    api-integration, pitch-deck-video, design-taste-frontend, orchestrate,
    hackathon-mode): their staged sources were fixed too, so build.sh
    reproduces them by copying the staged source. Encoding them here as
    well would fail the exact-match assert (the staged copy already has
    the fixed text).
  - README.md / plugin.json / marketplace.json: written by build.sh
    heredocs, edited directly in build.sh.

Usage:
  diff -rq /tmp/qc-before ~/workspace/hackathon-plugin/hackathon-ecc > /tmp/qc-diff-files.txt
  (then trim the diff output to relative paths, one per line)
  python3 gen_qc_patches.py > /tmp/qc_section.py
"""
import difflib
import json
import sys

PRISTINE = "/tmp/qc-before"
FIXED = "/home/hatch/workspace/hackathon-plugin/hackathon-ecc"

# Staged-source files: fixed at the staged source, reproduced by build.sh copy.
SKIP = {
    "skills/deploy-fast/SKILL.md",
    "skills/api-integration/SKILL.md",
    "skills/pitch-deck-video/SKILL.md",
    "skills/design-taste-frontend/SKILL.md",
    "skills/orchestrate/SKILL.md",
    "rules/hackathon-mode.mdc",
    "README.md",
}


def lit(block: str) -> str:
    """Emit a Python string literal for a (possibly multi-line) block."""
    if "\n" not in block:
        return json.dumps(block)
    if "\\" not in block and '"""' not in block and not block.endswith('"'):
        return '"""' + block + '"""'
    return repr(block)


def pairs_for(rel: str):
    """Return (old, new) exact-replacement pairs for one changed file."""
    with open(f"{PRISTINE}/{rel}", encoding="utf-8") as f:
        p_text = f.read()
    with open(f"{FIXED}/{rel}", encoding="utf-8") as f:
        f_text = f.read()
    p_lines = p_text.split("\n")
    f_lines = f_text.split("\n")
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
            b1 = j1 - (i1 - a1)
            b2 = j2 + (a2 - i2)
            new = "\n".join(f_lines[b1:b2])
            if old == new:
                break
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
        line.strip()
        for line in open("/tmp/qc-diff-files.txt", encoding="utf-8")
        if line.strip()
    ]
    patched = [r for r in diff_files if r not in SKIP]
    skipped = [r for r in diff_files if r in SKIP]

    out = []
    out.append('# --- QUALITY CHECK FIXES (Nov 9 quality check; encoded from the qc-before-vs-fixed diff) ---')
    out.append('# The Nov 9 quality check applied fixes to the built plugin. This section')
    out.append('# re-applies them on every rebuild, after all STEP 3 patches above (including')
    out.append('# the AUDIT #1 FIXES and the paths:->globs: rename), so a fresh build.sh run')
    out.append('# reproduces the quality-checked plugin byte-for-byte. Each replacement asserts')
    out.append('# an exact single match; a silent no-op fails the build.')
    out.append('# Files fall into two groups: ECC stock files (patched here) and ui-ux-pro-max')
    out.append('# (fetched from GitHub by build.sh — no staged source exists, so patched here).')
    out.append('# The 6 staged-source files the quality check fixed are NOT patched here: their')
    out.append('# staged sources were fixed too, so build.sh reproduces them by copying the')
    out.append('# staged source (deploy-fast, api-integration, pitch-deck-video,')
    out.append('# design-taste-frontend, orchestrate, hackathon-mode). README/plugin.json/')
    out.append('# marketplace.json are written by build.sh heredocs, edited directly.')
    out.append('python3 - "$PLUGIN_DIR" <<\'PYEOF\'')
    out.append('import sys')
    out.append('base = sys.argv[1]')
    out.append('')
    out.append('def qc_patch(path, subs):')
    out.append('    text = open(path, encoding="utf-8").read()')
    out.append('    for old, new in subs:')
    out.append('        assert text.count(old) == 1, f"{path}: pattern not found exactly once: {old[:70]}"')
    out.append('        text = text.replace(old, new)')
    out.append('    open(path, "w", encoding="utf-8").write(text)')
    out.append('')

    github = [r for r in patched if r.startswith("skills/ui-ux-pro-max/")]
    stock = [r for r in patched if r not in github]
    total_pairs = 0
    for group_name, group in [
        ("ECC stock", stock),
        ("GitHub-fetched (no staged source)", github),
    ]:
        out.append(f'# --- {group_name}: {len(group)} files ---')
        for rel in group:
            pairs = pairs_for(rel)
            total_pairs += len(pairs)
            out.append(f'qc_patch(f"{{base}}/{rel}", [')
            for old, new in pairs:
                out.append(f'  ({lit(old)},')
                out.append(f'   {lit(new)}),')
            out.append('])')
        out.append('')
    out.append(f'print("quality check fixes applied: {len(patched)} files, {total_pairs} replacements")')
    out.append('PYEOF')
    print("\n".join(out))
    print(
        f"# SUMMARY files={len(patched)} stock={len(stock)} github={len(github)} "
        f"pairs={total_pairs} skipped_staged={len(skipped)}",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
