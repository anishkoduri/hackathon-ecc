#!/usr/bin/env python3
"""Generate the AUDIT #10 patch section for build.sh from the pristine-vs-fixed diff.

Reads the pristine plugin (~/workspace/hackathon-plugin/hackathon-ecc, just
rebuilt by build.sh) and the fixed backup (~/workspace/hackathon-plugin/audit10-fixed-backup),
and emits the shell section that re-applies every Audit #10 fix on rebuild,
following build.sh's existing patch conventions (Audit #9 style: r'''...'''
literals, count==1 asserts, per-file comments).

Special cases (handled separately from the exact-match patches):
  - hooks/adapter.js ............ DELETED by Fixer B; emitted as `rm -f`
    (build.sh:152 copies the whole hooks dir wholesale, so the section must
    delete it after the copy step or the next build re-copies it).
  - schemas/cursor-hooks.schema.json .. NEW file from Fixer A; emitted as a
    shell heredoc writing the full file (no pristine version to patch).
  - skills/app-scaffold/SKILL.md .... NOT in the diff: the pristine build
    already contains Fixer B's QC fix (staged rewritten-skills source drives
    it). Nothing encoded; asserted here.
  - scripts/lib/context-profile-support.js .. byte-cap fix (16 MiB -> 64 MiB,
    latent blocker found by Fixer A); a normal content patch, present in both.

Guards:
  - The 5 restored originals (deploy-fast, api-integration, hackathon-scope,
    app-scaffold, readme-writer) must NOT appear in the diff at all, and
    their staged rewritten-skills/ sources must equal the built copies.
  - The diff must be exactly the 19 changed files + 1 deletion + 1 new file.

Usage: python3 gen_audit10_patches.py > ~/workspace/hackathon-plugin/audit-scripts/audit10_section.txt
"""
import difflib
import subprocess
import sys

PLUGIN_ROOT = "/home/hatch/workspace/hackathon-plugin"
PRISTINE = f"{PLUGIN_ROOT}/hackathon-ecc"
FIXED = f"{PLUGIN_ROOT}/audit10-fixed-backup"

# Restored originals: any file under these skill dirs must never be patched.
FORBIDDEN_DIRS = {
    "skills/hackathon-scope",
    "skills/deploy-fast",
    "skills/app-scaffold",
    "skills/api-integration",
    "skills/readme-writer",
}
STAGED = {
    "skills/hackathon-scope/SKILL.md": "rewritten-skills/hackathon-scope/SKILL.md",
    "skills/deploy-fast/SKILL.md": "rewritten-skills/deploy-fast/SKILL.md",
    "skills/app-scaffold/SKILL.md": "rewritten-skills/app-scaffold/SKILL.md",
    "skills/api-integration/SKILL.md": "rewritten-skills/api-integration/SKILL.md",
    "skills/readme-writer/SKILL.md": "rewritten-skills/readme-writer/SKILL.md",
}

EXPECTED_DELETED = {"hooks/adapter.js"}
EXPECTED_ADDED = {"schemas/cursor-hooks.schema.json"}


def lit(block: str) -> str:
    """Emit a Python string literal for block, Audit #9 style (r'''...''').

    r''' breaks only if the block contains ''' or ends with a backslash;
    fall back to repr() then. Never use r\"\"\"...\"\"\": patch strings ending
    in " break it (Audit #4 lesson).
    """
    if "'''" not in block and not block.endswith("\\"):
        return "r'''" + block + "'''"
    return repr(block)


def hunks_for(rel: str):
    """Return list of (old, new) exact-replacement pairs for one file."""
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
    proc = subprocess.run(
        ["diff", "-r", "--brief", FIXED, PRISTINE],
        capture_output=True, text=True, check=False,
    )
    changed, deleted, added = [], [], []
    for line in proc.stdout.splitlines():
        if line.startswith("Files ") and line.endswith(" differ"):
            # "Files <fixed>/<rel> and <pristine>/<rel> differ"
            rel = line[len("Files "):].split(" and ")[0][len(FIXED) + 1:]
            changed.append(rel)
        elif line.startswith("Only in "):
            # "Only in <dir>: <name>"
            head, name = line[len("Only in "):].rsplit(": ", 1)
            if head.startswith(FIXED):
                added.append(head[len(FIXED) + 1:] + "/" + name if head != FIXED else name)
            elif head.startswith(PRISTINE):
                deleted.append(head[len(PRISTINE) + 1:] + "/" + name if head != PRISTINE else name)
            else:
                raise SystemExit(f"unparseable diff line: {line}")
        else:
            raise SystemExit(f"unparseable diff line: {line}")
    changed.sort()
    deleted.sort()
    added.sort()

    for rel in changed:
        if any(rel.startswith(d + "/") or rel == d for d in FORBIDDEN_DIRS):
            raise SystemExit(f"STOP: diff touches a restored original: {rel}")
    if set(deleted) != EXPECTED_DELETED:
        raise SystemExit(f"STOP: unexpected deletions: {deleted} (expected {sorted(EXPECTED_DELETED)})")
    if set(added) != EXPECTED_ADDED:
        raise SystemExit(f"STOP: unexpected additions: {added} (expected {sorted(EXPECTED_ADDED)})")
    if "skills/app-scaffold/SKILL.md" in changed:
        raise SystemExit("STOP: app-scaffold in diff; expected pristine build to already contain the fix")

    # Restored originals: staged sources must equal the built copies.
    for built_rel, staged_rel in STAGED.items():
        with open(f"{PRISTINE}/{built_rel}", encoding="utf-8") as f:
            built = f.read()
        with open(f"{PLUGIN_ROOT}/{staged_rel}", encoding="utf-8") as f:
            staged = f.read()
        if built != staged:
            raise SystemExit(f"STOP: staged source differs from built copy: {built_rel} vs {staged_rel}")
        with open(f"{FIXED}/{built_rel}", encoding="utf-8") as f:
            fixed = f.read()
        if fixed != staged:
            raise SystemExit(f"STOP: fixed backup differs from staged source: {built_rel}")

    # Per-file comments: fixer + defect, in diff order.
    comments = {
        "agents/ecc-chief-of-staff.md": "Fixer B (Cleanliness): post-send checklist claimed a PostToolUse hook enforces it; no such hook is wired in hooks/hooks.json. Reword to a manual self-check.",
        "agents/ecc-code-reviewer.md": "Fixer C (Conflicts): 800-line ceiling stated as a hard rule; soften to a soft ceiling with a deliberate-exception reason (MEDIUM / INFO).",
        "commands/evolve.md": "Fixer B (Cleanliness): frontmatter model sonnet is not a Cursor model; composer-2.5.",
        "commands/quality-gate.md": "Fixer B (Cleanliness): claimed async PostToolUse dispatcher wiring via hooks/hooks.json; no such entry exists. State the gate is manually invoked.",
        "commands/setup-pm.md": "Fixer B (Cleanliness): Claude-Code-only env var / config paths; add the Cursor equivalents (CURSOR_PACKAGE_MANAGER, .cursor/package-manager.json).",
        "commands/skill-create.md": "Fixer B (Cleanliness): skill install paths named .claude/skills/ only; add the Cursor paths (.cursor/skills/, ~/.cursor/skills/).",
        "manifests/context-packs/skill-triggers@1.json": "Fixer A (Connectivity): 11 trigger keys named skills that do not ship; prune them, coverage.withTriggers 38 -> 27. All 6 deferred skills keep their triggers.",
        "manifests/context-profiles/full@1.json": "Fixer A (Connectivity): required listed configure-ecc / ecc-guide, which are not shipped; required is now [skill:context-budget] only.",
        "manifests/context-profiles/lean@1.json": "Fixer A (Connectivity): eager + required listed configure-ecc / ecc-guide, which are not shipped; both now [skill:context-budget] only; description updated (no longer 'three-skill').",
        "manifests/install-modules.json": "Fixer A (Connectivity): no 'hackathon' module, so the 24 hackathon skills were unowned by any module; add the module with all 24 skill paths.",
        "manifests/install-profiles.json": "Fixer A (Connectivity): 'full' profile did not include the hackathon module; add 'hackathon' to it.",
        "scripts/lib/context-profile-support.js": "Byte-cap fix (latent blocker found by Fixer A): loadContextRegistry() threw 'Cumulative source byte limit exceeded' on the real plugin — skills/ totals ~45 MB (design-taste-frontend/assets ~36 MB) against a 16 MiB read guard. Raise MAX_TOTAL_BYTES 16 MiB -> 64 MiB; the bound is a read guard, 64 MiB still guards, plugin is 55 MB.",
        "scripts/lib/harness-adapter-compliance.js": "Fixer A (Connectivity): deepseek-harness source_docs was [] (empty), failing validateAdapterRecords(); restore the 2 entries.",
        "scripts/lib/package-manager.js": "Fixer B (Cleanliness): Claude-Code-only package-manager detection; make it host-aware (CURSOR_PACKAGE_MANAGER first, .cursor paths, ~/.cursor fallbacks).",
        "scripts/setup-package-manager.js": "Fixer B (Cleanliness): setup script named Claude Code only; host-aware wording and getConfigPath() reporting.",
        "skills/laravel-plugin-discovery/SKILL.md": "Fixer B (Cleanliness): LaraPlugins MCP setup named ~/.claude.json only; Cursor-first with the Claude Code alternative.",
        "skills/rules-distill/SKILL.md": "Fixer B (Cleanliness): scan commands named Claude Code paths only; add the Cursor paths.",
        "skills/santa-method/SKILL.md": "Fixer B (Cleanliness): 'Claude Code Subagents' heading in a Cursor plugin; Cursor Subagents.",
        "skills/skill-scout/SKILL.md": "Fixer B (Cleanliness): skill search paths named ~/.claude only; check ~/.cursor/skills and the plugin marketplaces first.",
    }
    missing = [r for r in changed if r not in comments]
    if missing:
        raise SystemExit(f"STOP: no comment for changed file(s): {missing}")

    out = []
    out.append('# --- AUDIT #10 FIXES (Nov 10 Audit #10; Fixers A + B + C, plus byte-cap fix) ---')
    out.append('# Re-applies the Audit #10 fixes on every rebuild, after the AUDIT #9 FIXES')
    out.append('# sections above, so a fresh build.sh run reproduces the audited plugin')
    out.append('# byte-for-byte. Each replacement asserts an exact single match; a silent')
    out.append('# no-op fails the build. 19 files patched below, plus two special cases')
    out.append('# after the python block: hooks/adapter.js is deleted (Fixer B) and')
    out.append('# schemas/cursor-hooks.schema.json is created (Fixer A, new file).')
    out.append('# skills/app-scaffold/SKILL.md needs no patch: the pristine build already')
    out.append('# contains Fixer B\'s QC fix because the staged rewritten-skills/ source')
    out.append('# drives it (verified by the generator; staged == built for all 5 restored')
    out.append('# originals).')
    out.append('python3 - "$PLUGIN_DIR" <<\'PYEOF\'')
    out.append('import sys')
    out.append('base = sys.argv[1]')
    out.append('_files = set()')
    out.append('_replacements = [0]')
    out.append('')
    out.append('')
    out.append('def audit10_patch(path, subs):')
    out.append('    _files.add(path)')
    out.append('    text = open(path, encoding="utf-8").read()')
    out.append('    for old, new in subs:')
    out.append('        assert text.count(old) == 1, f"{path}: pattern not found exactly once: {old[:70]!r}"')
    out.append('        text = text.replace(old, new)')
    out.append('        _replacements[0] += 1')
    out.append('    open(path, "w", encoding="utf-8").write(text)')
    out.append('')

    total_pairs = 0
    for rel in changed:
        pairs = hunks_for(rel)
        total_pairs += len(pairs)
        out.append(f'# --- {comments[rel]}')
        out.append(f'audit10_patch(f"{{base}}/{rel}", [')
        for old, new in pairs:
            out.append(f'  ({lit(old)},')
            out.append(f'   {lit(new)}),')
        out.append('])')
        out.append('')
    out.append(f'print(f"audit #10 fixes applied: {{len(_files)}} files, {{_replacements[0]}} replacements")')
    out.append('PYEOF')
    out.append('')
    out.append('# --- Fixer B (Cleanliness): hooks/adapter.js is deleted ---')
    out.append('# build.sh:152 copies the whole hooks dir wholesale from the ECC source,')
    out.append('# so the adapter comes back on every rebuild unless removed here. It was')
    out.append('# a dead adapter (nothing in the plugin references it); Fixer B removed it.')
    out.append('rm -f "$PLUGIN_DIR/hooks/adapter.js"')
    out.append('')
    out.append('# --- Fixer A (Connectivity): schemas/cursor-hooks.schema.json is a NEW file ---')
    out.append('# No pristine version exists to patch, so the full file is written here.')
    out.append('# It is the JSON Schema for hooks/hooks.json (Cursor hook events).')
    out.append('cat > "$PLUGIN_DIR/schemas/cursor-hooks.schema.json" <<\'SCHEMA_EOF\'')
    with open(f"{FIXED}/schemas/cursor-hooks.schema.json", encoding="utf-8") as f:
        schema_text = f.read()
    if "\nSCHEMA_EOF\n" in schema_text or schema_text.startswith("SCHEMA_EOF"):
        raise SystemExit("STOP: schema content collides with the SCHEMA_EOF heredoc delimiter")
    out.append(schema_text.rstrip("\n"))
    out.append('SCHEMA_EOF')
    print("\n".join(out))
    print(f"# SUMMARY files={len(changed)} pairs={total_pairs} deleted={deleted} added={added}", file=sys.stderr)


if __name__ == "__main__":
    main()
