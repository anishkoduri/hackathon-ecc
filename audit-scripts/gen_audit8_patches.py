#!/usr/bin/env python3
"""Generate the AUDIT #8 FIXES section for build.sh (Nov 9 Audit #8).

Encodes the Audit #8 fixes (Fixers A + B) so a fresh build.sh run
reproduces the audited plugin byte-for-byte. Pattern follows Audit #7:
exact-match replacements with an assert that fails loudly on a miss.

Method (no hand transcription): every (old, new) pair is sliced from the
pre-audit8 snapshot vs the fixed plugin by line number / marker, then the
whole transform is SIMULATED in memory (apply pairs to pre copies, compare
byte-for-byte against the fixed plugin) before anything is written to
build.sh. If the simulation fails, nothing is inserted.

Usage: python3 gen_audit8_patches.py [--insert]
  --insert   also insert the section into build.sh (before STEP 4 header)
             and exit non-zero if the section is already present.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PRE = os.path.join(ROOT, "hackathon-plugin-pre-audit8")
FIX = os.path.join(ROOT, "hackathon-ecc")
BUILD = os.path.join(ROOT, "build.sh")


def pre_lines(rel):
    return open(os.path.join(PRE, rel), encoding="utf-8").read().split("\n")


def fix_lines(rel):
    return open(os.path.join(FIX, rel), encoding="utf-8").read().split("\n")


def line(rel, n, which="pre"):
    ls = pre_lines(rel) if which == "pre" else fix_lines(rel)
    return ls[n - 1]


def block(rel, a, b, which="pre"):
    """1-based inclusive line slice joined with newlines."""
    ls = pre_lines(rel) if which == "pre" else fix_lines(rel)
    return "\n".join(ls[a - 1:b])


# (relpath, old, new) — old sliced from pre, new sliced from fixed.
PAIRS = []


def pair(rel, old, new):
    assert old != new, f"{rel}: old == new"
    assert '"""' not in old and '"""' not in new, f"{rel}: triple-quote in pair"
    assert not old.endswith("\\") and not new.endswith("\\"), f"{rel}: trailing backslash"
    # A raw triple-double-quoted literal cannot hold a string ending in '"'
    # (the closing quotes would run together: '""""'). Such strings must be
    # rendered with r'''...''' instead; assert that is possible.
    for s in (old, new):
        if s.endswith('"'):
            assert "'''" not in s, f"{rel}: string ends in quote and contains '''"
    PAIRS.append((rel, old, new))


# --- M1: django build resolver drops --deploy -------------------------------
pair("agents/ecc-django-build-resolver.md",
     line("agents/ecc-django-build-resolver.md", 48),
     line("agents/ecc-django-build-resolver.md", 48, "fix"))

# --- M2: verification-loop triggers -> end-of-project phrasing --------------
pair("manifests/context-packs/skill-triggers@1.json",
     block("manifests/context-packs/skill-triggers@1.json", 300, 306),
     block("manifests/context-packs/skill-triggers@1.json", 300, 305, "fix"))

# --- L1: "Security Scan" -> "Security Review (code-level; END-ONLY)" --------
for rel, n in [("commands/go-review.md", 13), ("commands/kotlin-review.md", 13),
               ("commands/python-review.md", 13), ("commands/rust-review.md", 14)]:
    pair(rel, line(rel, n), line(rel, n, "fix"))

# --- L2: plankton-code-quality — semgrep END-ONLY ---------------------------
pair("skills/plankton-code-quality/SKILL.md",
     line("skills/plankton-code-quality/SKILL.md", 105),
     line("skills/plankton-code-quality/SKILL.md", 105, "fix"))
pair("skills/plankton-code-quality/SKILL.md",
     line("skills/plankton-code-quality/SKILL.md", 158),
     line("skills/plankton-code-quality/SKILL.md", 158, "fix"))
pair("skills/plankton-code-quality/SKILL.md",
     block("skills/plankton-code-quality/SKILL.md", 174, 176),
     block("skills/plankton-code-quality/SKILL.md", 174, 178, "fix"))

# --- D1: skill-stocktake "Agent tool" -> "Spawn a Cursor subagent" ----------
pair("skills/skill-stocktake/SKILL.md",
     line("skills/skill-stocktake/SKILL.md", 127),
     line("skills/skill-stocktake/SKILL.md", 127, "fix"))

# --- D2: multi-* commands — Claude Code tool names -> Cursor wording --------
for rel, n in [("commands/multi-backend.md", 99), ("commands/multi-frontend.md", 99),
               ("commands/multi-workflow.md", 124)]:
    pair(rel, line(rel, n), line(rel, n, "fix"))
pair("commands/multi-execute.md",
     block("commands/multi-execute.md", 157, 161),
     block("commands/multi-execute.md", 157, 161, "fix"))
pair("commands/multi-plan.md",
     block("commands/multi-plan.md", 106, 110),
     block("commands/multi-plan.md", 106, 110, "fix"))

# --- D3: instinct-cli.py generated agents emit composer-2.5 -----------------
pair("skills/continuous-learning-v2/scripts/instinct-cli.py",
     line("skills/continuous-learning-v2/scripts/instinct-cli.py", 2050),
     line("skills/continuous-learning-v2/scripts/instinct-cli.py", 2050, "fix"))

# --- D5: resolve-ecc-root.js — ~/.cursor/plugins scan ------------------------
# (a) doc comment: items 5-6 become 5 (Cursor) / 6 (fallback) / 7 (claude).
pair("scripts/lib/resolve-ecc-root.js",
     block("scripts/lib/resolve-ecc-root.js", 58, 62),
     block("scripts/lib/resolve-ecc-root.js", 58, 67, "fix"))
# (b) code insertion: anchor on the end of the cache scan + Audit #4 comment.
_pre = open(os.path.join(PRE, "scripts/lib/resolve-ecc-root.js"), encoding="utf-8").read()
_fix = open(os.path.join(FIX, "scripts/lib/resolve-ecc-root.js"), encoding="utf-8").read()
_anchor = "  }\n\n  // Host-agnostic fallback (Audit #4): this module lives at"
assert _pre.count(_anchor) == 1, "D5 code anchor not unique in pre"
assert _fix.count(_anchor) == 1, "D5 code anchor not unique in fix"
_gate_start = _fix.index("  // Cursor plugin install (Audit #8):")
_gate_end = _fix.index(_anchor, _gate_start)
_cursor_block = _fix[_gate_start:_gate_end].rstrip("\n")
pair("scripts/lib/resolve-ecc-root.js",
     _anchor,
     "  }\n\n" + _cursor_block + "\n" + _anchor)

# --- D6: unified-memory — ecc.js qualified as ecc-universal checkout --------
pair("skills/unified-memory/SKILL.md",
     line("skills/unified-memory/SKILL.md", 27),
     line("skills/unified-memory/SKILL.md", 27, "fix"))

# --- D10: gan agents — "(Claude Code only ...)" in descriptions -------------
for rel in ("agents/ecc-gan-evaluator.md", "agents/ecc-gan-generator.md",
            "agents/ecc-gan-planner.md"):
    pair(rel, line(rel, 3), line(rel, 3, "fix"))

# --- D11: santa-method — drop "# Ship it" comment ---------------------------
pair("skills/santa-method/SKILL.md",
     line("skills/santa-method/SKILL.md", 165),
     line("skills/santa-method/SKILL.md", 165, "fix"))

# --- LOW-2: "not yet present" react-native claims -> pointers ---------------
pair("rules/react-patterns.mdc",
     line("rules/react-patterns.mdc", 189),
     line("rules/react-patterns.mdc", 189, "fix"))
pair("skills/react-native-patterns/SKILL.md",
     line("skills/react-native-patterns/SKILL.md", 9),
     line("skills/react-native-patterns/SKILL.md", 9, "fix"))

# --- M3: ui-ux-pro-max search.py landing gate in --design-system branch -----
_fix_search = open(os.path.join(FIX, "skills/ui-ux-pro-max/scripts/search.py"),
                   encoding="utf-8").read()
_pre_search = open(os.path.join(PRE, "skills/ui-ux-pro-max/scripts/search.py"),
                   encoding="utf-8").read()
_gs = _fix_search.index("        # GATE (Audit #8 M3")
_ge = _fix_search.index("        result = generate_design_system(", _gs)
_gate = _fix_search[_gs:_ge].rstrip("\n")
assert "            sys.exit(0)" in _gate, "M3 gate truncated"
_stack_anchor = (
    "        if args.stack:\n"
    "            print(\n"
    '                f"note: --stack {args.stack} is ignored in --design-system mode; "\n'
    '                "run a separate --stack query for stack-specific guidelines",\n'
    "                file=sys.stderr,\n"
    "            )\n"
    "        result = generate_design_system("
)
assert _pre_search.count(_stack_anchor) == 1, "M3 anchor not unique in pre"
assert _fix_search.count(_stack_anchor) == 0, "M3 anchor still in fix (gate not inserted?)"
pair("skills/ui-ux-pro-max/scripts/search.py",
     _stack_anchor,
     _stack_anchor.replace("        result = generate_design_system(",
                           _gate + "\n        result = generate_design_system("))

ORPHANS = ["skill:deep-research", "skill:eval-harness",
           "skill:osint-investigation", "skill:plan-canvas"]
DELETED_TESTS = ["skills/ui-ux-pro-max/scripts/tests/test_catalog_refresh.py",
                 "skills/ui-ux-pro-max/scripts/tests/test_catalog_summary_line_endings.py",
                 "skills/ui-ux-pro-max/scripts/tests/test_skill_script_paths.py"]


def simulate():
    """Apply all pairs + JSON prune + deletions to pre copies; compare to fix."""
    changed = {}
    for rel, old, new in PAIRS:
        text = changed.get(rel)
        if text is None:
            text = open(os.path.join(PRE, rel), encoding="utf-8").read()
        assert text.count(old) == 1, f"SIM {rel}: old not found exactly once: {old[:70]!r}"
        changed[rel] = text.replace(old, new)
    # LOW-1: install-components.json orphan deletion via JSON round-trip.
    rel = "manifests/install-components.json"
    data = json.loads(open(os.path.join(PRE, rel), encoding="utf-8").read())
    before = len(data["components"])
    assert before == 61, f"SIM {rel}: expected 61 components, got {before}"
    for oid in ORPHANS:
        hits = [c for c in data["components"] if c["id"] == oid]
        assert len(hits) == 1, f"SIM {rel}: orphan {oid} found {len(hits)}x"
    data["components"] = [c for c in data["components"] if c["id"] not in ORPHANS]
    assert len(data["components"]) == 57, "SIM install-components: expected 57"
    changed[rel] = json.dumps(data, indent=2) + "\n"
    # Verify every changed file matches the fixed plugin byte-for-byte.
    ok = True
    for rel, text in sorted(changed.items()):
        want = open(os.path.join(FIX, rel), encoding="utf-8").read()
        if text == want:
            print(f"  SIM OK   {rel}")
        else:
            ok = False
            print(f"  SIM FAIL {rel}")
            import difflib
            for ln in list(difflib.unified_diff(
                    want.split("\n"), text.split("\n"), "fixed", "simulated",
                    lineterm=""))[:30]:
                print("   ", ln)
    # Verify deleted test files are absent in the fixed plugin.
    for rel in DELETED_TESTS:
        assert not os.path.exists(os.path.join(FIX, rel)), f"SIM {rel} still in fix"
        assert os.path.exists(os.path.join(PRE, rel)), f"SIM {rel} missing in pre"
    print(f"  SIM OK   {len(DELETED_TESTS)} test files deleted in fix (present in pre)")
    # Verify staged-source fixes need no patch.
    # feature-expansion is the exception BY DESIGN: staged is the pre-patch
    # original and build.sh STEP 3 patches it (L3 ban via the §531 note patch,
    # L29-31/L114 via the §685 ECC-process patch). Verify that applying those
    # two existing patches to the staged copy reproduces the fixed copy.
    _fe_staged = open(os.path.join(ROOT, "new-skills/feature-expansion/SKILL.md"),
                      encoding="utf-8").read()
    _fe_fo = "verifying each as it lands. Never runs automatically after a build."
    _fe_fn = ("verifying each as it lands. Feature brainstorming here is autonomous "
              "subagent ideation + implementation; do not invoke the brainstorming "
              "skill (collaborative user questioning) inside this flow. "
              "Never runs automatically after a build.")
    assert _fe_staged.count(_fe_fo) == 1, "SIM staged feature-expansion L3 anchor"
    _fe_staged = _fe_staged.replace(_fe_fo, _fe_fn)
    _fe_subs = [
        ("- **No planning documents.** The proposal is a table in the reply (Phase 2). No PRD, no spec file, no roadmap doc.",
         "- **ECC process applies.** The proposal is a table in the reply (Phase 2); the planner pass (Phase 3) writes the per-feature briefs (Phase 4) that carry what implementers need. Follow ECC's development workflow: plan first, TDD, code review while building."),
        ("- **No review gates.** There is one approval point: the planner pass (Phase 3). After that, features are implemented and verified — no code review, no second approval round.",
         "- **Review while building.** ECC code review applies as features are implemented. There is one approval point before implementation: the planner pass (Phase 3). Security tests and audits run only at the very end of the project or when explicitly asked."),
        ("- **No tests, no TDD.** Verification means running the feature and confirming it works (`verification-before-completion`). Never write a test suite, never require coverage.",
         "- **TDD.** Write tests as ECC does them — tests first, then the feature — and verify with `verification-before-completion`. Security tests and audits run only at the very end of the project or when explicitly asked."),
        ("- No PRD, no spec, no test strategy, no coverage target. The planner does not write implementation plans as files — the per-feature briefs in Phase 4 carry what implementers need.",
         "- The planner does not write PRDs, specs, or implementation plans as files — the per-feature briefs in Phase 4 carry what implementers need. Implementation follows ECC process (plan first, TDD, code review while building); security tests and audits run only at the very end or on explicit ask."),
    ]
    for _o, _n in _fe_subs:
        assert _fe_staged.count(_o) == 1, f"SIM staged feature-expansion §685 anchor: {_o[:50]!r}"
        _fe_staged = _fe_staged.replace(_o, _n)
    assert _fe_staged == open(os.path.join(
        FIX, "skills/feature-expansion/SKILL.md"), encoding="utf-8").read(), \
        "SIM staged feature-expansion + STEP 3 patches != fixed"
    print("  SIM OK   staged feature-expansion + existing STEP 3 patches == fixed (drift is by design)")
    for srel, frel in [
            ("new-skills/orchestrate/SKILL.md", "skills/orchestrate/SKILL.md"),
            ("rewritten-skills/hackathon-scope/SKILL.md", "skills/hackathon-scope/SKILL.md"),
            ("rewritten-skills/api-integration", "skills/api-integration")]:
        sp = os.path.join(ROOT, srel)
        fp = os.path.join(FIX, frel)
        if os.path.isdir(sp):
            import filecmp
            for dp, _, fns in os.walk(sp):
                for fn in fns:
                    a = os.path.join(dp, fn)
                    b = os.path.join(fp, os.path.relpath(a, sp))
                    assert open(a, "rb").read() == open(b, "rb").read(), \
                        f"SIM staged mismatch: {os.path.relpath(a, ROOT)}"
            print(f"  SIM OK   staged {srel} == fixed {frel} (dir)")
        else:
            assert open(sp, "rb").read() == open(fp, "rb").read(), \
                f"SIM staged mismatch: {srel}"
            print(f"  SIM OK   staged {srel} == fixed {frel}")
    return ok


def lit(s):
    """Render s as a raw triple-quoted literal, dodging the trailing-quote trap."""
    if s.endswith('"'):
        return "r'''" + s + "'''"
    return 'r"""' + s + '"""'


def render_section():
    """Render the AUDIT #8 FIXES section text for build.sh."""
    out = []
    out.append("# ============================================================================")
    out.append("# AUDIT #8 FIXES (Nov 9 Audit #8; encoded from the audit7-fixed-vs-fixed diff)")
    out.append("# ============================================================================")
    out.append("# Re-applies the Audit #8 fixes on every rebuild, after the AUDIT #7 FIXES")
    out.append("# and the install-profiles/install-components prune above, so a fresh")
    out.append("# build.sh run reproduces the audited plugin. Each replacement asserts an")
    out.append("# exact single match; a silent no-op fails the build.")
    out.append("#")
    out.append("# ORDERING (do not reorder):")
    out.append("#  - The install-components orphan deletion below reads")
    out.append("#    manifests/install-components.json AFTER the Audit #7 connectivity prune")
    out.append("#    (93 -> 61 components); it must run after that prune.")
    out.append("#  - The search.py gate patch runs after STEP 2 copies ui-ux-pro-max from")
    out.append("#    upstream (/tmp/uipro); the upstream file is the patch's old text.")
    out.append("#    It inserts in the --design-system branch, before")
    out.append("#    generate_design_system(); the Audit #7 Q2 gate in the domain-search")
    out.append("#    branch is a different location and is untouched.")
    out.append("#  - The test-file deletions run after STEP 2 copies ui-ux-pro-max; the")
    out.append("#    files are upstream files, so a fresh clone restores them and the")
    out.append("#    explicit deletion below is the encoding.")
    out.append("#")
    out.append("# NOT patched here (encoded elsewhere, or no change):")
    out.append("#  - D7 (claude-project-scripts-package.json) -- NO CHANGE: the audit premise")
    out.append("#    was wrong; the file IS referenced by scripts/lib/install-targets/")
    out.append("#    claude-project.js and must stay.")
    out.append("#  - D8 (Taste asset dedupe) -- NO CHANGE: judged unsafe, files untouched.")
    out.append("#  - D9 (shots.json) -- NO CHANGE: left as-is.")
    out.append("#  - Quality Defect 2 (api-integration API-PATTERNS.md), Quality Defect 3")
    out.append("#    (feature-expansion :167/:189), D4 (orchestrate :191), hackathon-scope :4")
    out.append("#    -- fixed in the staged sources (rewritten-skills/api-integration,")
    out.append("#    new-skills/feature-expansion, new-skills/orchestrate,")
    out.append("#    rewritten-skills/hackathon-scope), which STEP 2 copies verbatim.")
    out.append("#  - feature-expansion frontmatter drift (Fixer A): the staged copy's L3")
    out.append("#    lacks the 'do not invoke the brainstorming skill' ban and its L29-31")
    out.append("#    / L114 lack the ECC-process lines that the built copy has. That is BY")
    out.append("#    DESIGN, not drift to fix in the staged source: build.sh already patches")
    out.append("#    those lines at build time (the L3 ban is inserted by the")
    out.append("#    feature-expansion note patch in STEP 3, the ECC-process lines by the")
    out.append("#    '(d) feature-expansion standing rules' patch). Editing the staged source")
    out.append("#    to match would break those patches' exact-match anchors and fail the")
    out.append("#    build, so the staged source is left as the pre-patch original.")
    out.append("#  - Playwright pin (mcp.json @0.0.85) -- encoded at the source: the")
    out.append("#    '(e) Playwright MCP' block in STEP 3 writes the version literal.")
    out.append("#  - README '@latest' prose -- encoded at the source: the STEP 4 heredoc.")
    out.append('python3 - "$PLUGIN_DIR" <<\'PYEOF\'')
    out.append("import json as _json")
    out.append("import os, sys")
    out.append("base = sys.argv[1]")
    out.append("_files = set()")
    out.append("_replacements = [0]")
    out.append("")
    out.append("")
    out.append("def audit8_patch(path, subs):")
    out.append("    _files.add(path)")
    out.append('    text = open(path, encoding="utf-8").read()')
    out.append("    for old, new in subs:")
    out.append('        assert text.count(old) == 1, f"{path}: pattern not found exactly once: {old[:70]!r}"')
    out.append("        text = text.replace(old, new)")
    out.append("        _replacements[0] += 1")
    out.append('    open(path, "w", encoding="utf-8").write(text)')
    out.append("")
    # Group pairs by file, in the order the fixes were listed.
    seen = []
    for rel, _, _ in PAIRS:
        if rel not in seen:
            seen.append(rel)
    comments = {
        "agents/ecc-django-build-resolver.md": "# --- M1: django build resolver drops --deploy ---",
        "manifests/context-packs/skill-triggers@1.json": "# --- M2: verification-loop triggers reworded to end-of-project phrasing ---",
        "commands/go-review.md": "# --- L1: 'Security Scan' relabelled (code-level review; tool scans are END-ONLY) ---",
        "commands/kotlin-review.md": None,
        "commands/python-review.md": None,
        "commands/rust-review.md": None,
        "skills/plankton-code-quality/SKILL.md": "# --- L2: plankton-code-quality — semgrep is END-ONLY ---",
        "skills/skill-stocktake/SKILL.md": "# --- D1: skill-stocktake 'Agent tool' -> Cursor subagent ---",
        "commands/multi-backend.md": "# --- D2: multi-* commands — Claude Code tool names -> Cursor wording ---",
        "commands/multi-execute.md": None,
        "commands/multi-frontend.md": None,
        "commands/multi-plan.md": None,
        "commands/multi-workflow.md": None,
        "skills/continuous-learning-v2/scripts/instinct-cli.py": "# --- D3: instinct-cli.py generated agents emit model: composer-2.5 ---",
        "scripts/lib/resolve-ecc-root.js": "# --- D5: resolve-ecc-root.js — scan ~/.cursor/plugins in resolveEccRoot() ---",
        "skills/unified-memory/SKILL.md": "# --- D6: unified-memory — ecc.js qualified as an ecc-universal checkout ---",
        "agents/ecc-gan-evaluator.md": "# --- D10: gan agents — '(Claude Code only — no Cursor equivalent)' in descriptions ---",
        "agents/ecc-gan-generator.md": None,
        "agents/ecc-gan-planner.md": None,
        "skills/santa-method/SKILL.md": "# --- D11: santa-method — drop '# Ship it' comment ---",
        "rules/react-patterns.mdc": "# --- Connectivity LOW-2: 'not yet present' react-native claims -> pointers ---",
        "skills/react-native-patterns/SKILL.md": None,
        "skills/ui-ux-pro-max/scripts/search.py": "# --- M3: ui-ux-pro-max search.py — landing gate in the --design-system branch ---\n# Same redirect as the Audit #7 Q2 domain-search gate. Runs BEFORE\n# generate_design_system() so no landing design system (and no persisted\n# MASTER.md) is produced. Do NOT delete landing.csv.",
    }
    for rel in seen:
        c = comments.get(rel)
        if c:
            out.append("")
            out.append(c)
        subs = [(o, n) for (r, o, n) in PAIRS if r == rel]
        out.append(f'audit8_patch(f"{{base}}/{rel}", [')
        for old, new in subs:
            out.append(f"    ({lit(old)},")
            out.append(f"     {lit(new)}),")
        out.append("])")
    out.append("")
    out.append("# --- Connectivity LOW-1: drop 4 orphan components from install-components.json ---")
    out.append("# Orphans: the named skills do not exist in the plugin, so no module prune")
    out.append("# can catch them. Runs after the Audit #7 connectivity prune (61 left).")
    out.append('_cp = f"{base}/manifests/install-components.json"')
    out.append('_cd = _json.load(open(_cp, encoding="utf-8"))')
    out.append('_comp_before = len(_cd["components"])')
    out.append('assert _comp_before == 61, f"install-components: expected 61 before Audit #8, got {_comp_before}"')
    out.append('_orphans = ["skill:deep-research", "skill:eval-harness", "skill:osint-investigation", "skill:plan-canvas"]')
    out.append("for _oid in _orphans:")
    out.append('    assert sum(1 for c in _cd["components"] if c["id"] == _oid) == 1, f"orphan {_oid} not found exactly once"')
    out.append('_cd["components"] = [c for c in _cd["components"] if c["id"] not in _orphans]')
    out.append('assert len(_cd["components"]) == 57, f"install-components: expected 57 after Audit #8, got {len(_cd[\'components\'])}"')
    out.append('with open(_cp, "w", encoding="utf-8") as _f:')
    out.append('    _json.dump(_cd, _f, indent=2)')
    out.append('    _f.write("\\n")')
    out.append('print(f"install-components orphans removed: {_comp_before} -> {len(_cd[\'components\'])} components")')
    out.append("")
    out.append("# --- Quality Defect 4: delete 3 ui-ux-pro-max tests that error at import ---")
    out.append("# Upstream files (fresh clone restores them), so the deletion is the encoding.")
    out.append("_dead_tests = [")
    for rel in DELETED_TESTS:
        out.append(f'    "{rel}",')
    out.append("]")
    out.append("for _rel in _dead_tests:")
    out.append("    _p = os.path.join(base, _rel)")
    out.append('    assert os.path.exists(_p), f"expected upstream test file missing: {_rel}"')
    out.append("    os.remove(_p)")
    out.append('    print(f"deleted failing upstream test: {_rel}")')
    out.append("")
    out.append('print(f"audit #8 fixes applied: {len(_files)} files, {_replacements[0]} replacements")')
    out.append("PYEOF")
    return "\n".join(out) + "\n"


def main():
    print(f"pairs: {len(PAIRS)} across {len(set(r for r, _, _ in PAIRS))} files")
    ok = simulate()
    if not ok:
        print("SIMULATION FAILED — not inserting")
        return 1
    print("simulation: all patched files match the fixed plugin byte-for-byte")
    if "--insert" in sys.argv:
        text = open(BUILD, encoding="utf-8").read()
        assert "AUDIT #8 FIXES" not in text, "AUDIT #8 section already in build.sh"
        marker = "# STEP 4 — README (written by hand; the build wipes it)"
        assert text.count(marker) == 1, "STEP 4 marker not unique"
        section = render_section()
        text = text.replace(marker, section + marker)
        open(BUILD, "w", encoding="utf-8").write(text)
        print(f"inserted AUDIT #8 section into build.sh ({len(section.splitlines())} lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
