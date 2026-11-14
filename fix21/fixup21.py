#!/usr/bin/env python3
"""Fix-up #21 (Nov 12, 2026) — bump the five earlier verifiers to the
post-fix21 state. NOT a new fix. Three root causes, all verified by the
coordinator (fix21/SPEC.md section 7 check 11 + section 8: verify21.py
96/101, all 5 failures the check-11 subprocesses):

 1. build.sh pin (5 direct + cascades). All five verifiers pin build.sh
    to the post-fix20 values (23,609 lines / md5
    785fb40580a4d91f7a480e1cdbc21f24). Post-fix21 it is legitimately
    23,647 lines / md5 8dfacb47a2a6698d47e4b4a5f8d9126c (the fix21 block
    is exactly 38 lines, verified by diff against
    build.sh.before-fix21). Bump the pin in verify15/17/18/19/20:
    check lines + docstring sentences + the fix19 section-11 label
    (same scope as fixup20d's pin bump).
 2. Typeset checkbox supersession (verify19 + verify20). Both assert
    the fix20 checkbox is present. SPEC section 3 row 6 and section 7
    check 4 REQUIRE replacing it with fix21's TYPESET_CHECKBOX21 — so
    both checks now assert the fix21 checkbox is present and the fix20
    checkbox is GONE (the "old checkbox is gone" half is kept, with
    fix20 now the old one).
 3. verify19 system-ui subtraction. The check-7 RULE_TEXTS_WITH_SYSTEM_UI
    list subtracts the fix20 checkbox (comment: "the CURRENT typeset
    checkbox (fix #20's...)"). The fix21 checkbox also names `system-ui`
    once, so the subtraction list swaps in the fix21 checkbox. The
    *.md mention total stays 14 and the total stays 161 — no count
    check changes.

verify20's pin is MANIFEST-driven (check 10 reads fix20/MANIFEST.md,
the CLOSED post-fix20 record): since the MANIFEST is a closed
historical record and is NOT edited here, check 10's value comparison
is replaced by the literal post-fix21 pin — same pattern as
verify15/17/18/19. The "MANIFEST records lines + md5" presence check
is kept (the MANIFEST still records the fields).

Scope: verifier .py files ONLY (fix15/verify15.py, fix17/verify17.py,
fix18/verify18.py, fix19/verify19.py, fix20/verify20.py). fix21.py,
fix21/verify21.py, build.sh, staged sources, and the built tree are
NOT touched. No commit, no bundle, no GitHub touch. No build is run —
the fix-up edits no build input, so no rebuild is needed.

Mechanism (fix20/fixup20.py pattern): one-shot applicator with
preflight assertions, amendments in place, self-checks, and a
preflight that refuses re-run. The NEW checkbox is imported live
from fix21.py and the OLD fix20 checkbox live from fix20.py, so this
module still imports after application (fixup20b re-import precedent).
Every substitution asserts count==1. "replace" subs assert the old
text is gone afterwards; "append" subs (docstring sentences, import
lines — old is a substring of new) assert only that the new text is
present exactly once.
"""
import hashlib
import os
import sys

HOME = os.path.expanduser("~")
PLUGIN = os.path.join(HOME, "workspace/hackathon-plugin")
BUILD_SH = os.path.join(PLUGIN, "build.sh")

sys.path.insert(0, os.path.join(PLUGIN, "fix20"))
sys.path.insert(0, os.path.join(PLUGIN, "fix21"))
from fix20 import TYPESET_CHECKBOX_NEW as TYPESET_CHECKBOX_FIX20  # noqa: E402
from fix21 import TYPESET_CHECKBOX21_NEW as TYPESET_CHECKBOX21  # noqa: E402

OLD_LINES, OLD_MD5 = 23609, "785fb40580a4d91f7a480e1cdbc21f24"
NEW_LINES, NEW_MD5 = 23647, "8dfacb47a2a6698d47e4b4a5f8d9126c"
assert NEW_MD5 != OLD_MD5 and NEW_LINES != OLD_LINES
assert TYPESET_CHECKBOX21 != TYPESET_CHECKBOX_FIX20
assert TYPESET_CHECKBOX21.count("system-ui") == 1, \
    "fix21 checkbox must name system-ui exactly once (subtraction parity)"
assert TYPESET_CHECKBOX_FIX20.count("system-ui") == 1

V15 = os.path.join(PLUGIN, "fix15/verify15.py")
V17 = os.path.join(PLUGIN, "fix17/verify17.py")
V18 = os.path.join(PLUGIN, "fix18/verify18.py")
V19 = os.path.join(PLUGIN, "fix19/verify19.py")
V20 = os.path.join(PLUGIN, "fix20/verify20.py")

BANNED = ["claude", "codex", "anthropic", "opus", "sonnet", "haiku",
          "composer-2.5"]


def _once(text, anchor, where):
    n = text.count(anchor)
    assert n == 1, f"anchor count={n} in {where}: {anchor[:70]!r}"
    return n


# --- 1. build.sh pin (check line, shared by verify15/17/18/19) ------------
PIN_OLD = ('check("build.sh is 23,609 lines, md5 '
           '785fb40580a4d91f7a480e1cdbc21f24 (post-fixup20d: comment-only)",\n'
           '      len(build_lines) == 23609\n'
           '      and hashlib.md5(build.encode("utf-8")).hexdigest() == '
           '"785fb40580a4d91f7a480e1cdbc21f24")')
PIN_NEW = ('check("build.sh is 23,647 lines, md5 '
           '8dfacb47a2a6698d47e4b4a5f8d9126c (post-fix21)",\n'
           '      len(build_lines) == 23647\n'
           '      and hashlib.md5(build.encode("utf-8")).hexdigest() == '
           '"8dfacb47a2a6698d47e4b4a5f8d9126c")')

# --- docstring sentences (append: old is a substring of new) ----------------
V15_DOC_OLD = ("     same precedent. The post-fixup20d values are 23,609 lines /\n"
               "     785fb40580a4d91f7a480e1cdbc21f24 (comment-only lowercase-LAST\n"
               "     normalization, 20 lines; no block appended); updated by fix #20's\n"
               "     fourth fix-up pass (sweep #28 MINOR-1), same precedent.\n")
V15_DOC_NEW = (V15_DOC_OLD
               + "     The post-fix21 values are 23,647 lines /\n"
               + "     8dfacb47a2a6698d47e4b4a5f8d9126c (fix21 block, 38 lines); updated\n"
               + "     by fix #21, same precedent.\n")

V17_DOC_OLD = ("     Updated by fix #20's fourth fix-up pass (sweep #28 MINOR-1) to the\n"
               "     post-fixup20d values (23,609 lines, 785fb405...) — same precedent.\n")
V17_DOC_NEW = (V17_DOC_OLD
               + "     Updated by fix #21 to the\n"
               + "     post-fix21 values (23,647 lines, 8dfacb47...) — same precedent.\n")

V19_DOC_OLD = ("     same precedent. Updated by fix #20's fourth fix-up pass\n"
               "     (sweep #28 MINOR-1) to the post-fixup20d values (23,609 lines,\n"
               "     785fb40580a4d91f7a480e1cdbc21f24, comment-only lowercase-LAST\n"
               "     normalization, 20 lines; no block appended) — same precedent.\n"
               "     The typeset-lens checkbox\n"
               "     check was likewise updated by fix #20: fix #20 supersedes the\n"
               "     fix19 checkbox, so the check now asserts the fix20 checkbox is\n"
               "     present and the fix19 one is gone (and the check-7 subtraction\n"
               "     list swaps in the fix20 checkbox text).\n")
V19_DOC_NEW = ("     same precedent. Updated by fix #20's fourth fix-up pass\n"
               "     (sweep #28 MINOR-1) to the post-fixup20d values (23,609 lines,\n"
               "     785fb40580a4d91f7a480e1cdbc21f24, comment-only lowercase-LAST\n"
               "     normalization, 20 lines; no block appended) — same precedent.\n"
               "     Updated by fix #21 to the post-fix21 values (23,647 lines,\n"
               "     8dfacb47a2a6698d47e4b4a5f8d9126c, fix21 block, 38 lines) — same\n"
               "     precedent. The typeset-lens checkbox\n"
               "     check was likewise updated by fix #20: fix #20 supersedes the\n"
               "     fix19 checkbox, so the check now asserts the fix20 checkbox is\n"
               "     present and the fix19 one is gone (and the check-7 subtraction\n"
               "     list swaps in the fix20 checkbox text). Updated by fix #21: fix #21\n"
               "     supersedes the fix20 checkbox, so the check now asserts the fix21\n"
               "     checkbox is present and the fix20 one is gone (and the check-7\n"
               "     subtraction list swaps in the fix21 checkbox text).\n")

# --- verify19 section-11 label ------------------------------------------------
V19_LABEL_OLD = ("# 11. build.sh post-fixup20d (23,609 lines, md5 785fb405..., comment-only,\n"
                 "# lowercase-LAST normalization, 20 lines; no block appended). Updated by\n"
                 "# fix #20's fourth fix-up pass (sweep #28 MINOR-1) from the post-fixup20c values,\n"
                 "# same baseline-update precedent as fix #19's update of\n"
                 "# verify15/17/18 — a baseline update, not an anchor change.\n")
V19_LABEL_NEW = ("# 11. build.sh post-fix21 (23,647 lines, md5 8dfacb47..., fix21 block,\n"
                 "# 38 lines). Updated by fix #21 from the post-fixup20d values,\n"
                 "# same baseline-update precedent as fix #19's update of\n"
                 "# verify15/17/18 — a baseline update, not an anchor change.\n")

# --- 2. typeset checkbox checks ------------------------------------------------
V19_CB_OLD = ('check("typeset lens checkbox updated (fix #20 supersedes the fix19 checkbox)",\n'
              '      TYPESET_CHECKBOX_FIX20 in typeset and TYPESET_CHECKBOX_NEW not in typeset)')
V19_CB_NEW = ('check("typeset lens checkbox updated (fix #21 supersedes the fix20 checkbox)",\n'
              '      TYPESET_CHECKBOX21 in typeset and TYPESET_CHECKBOX_FIX20 not in typeset)')

V20_CB_OLD = ('check("typeset lens checkbox updated to fix #20",\n'
              '      TYPESET_CHECKBOX_NEW in typeset\n'
              '      and TYPESET_CHECKBOX_FIX19 not in typeset)')
V20_CB_NEW = ('check("typeset lens checkbox updated to fix #21",\n'
              '      TYPESET_CHECKBOX21 in typeset\n'
              '      and TYPESET_CHECKBOX_NEW not in typeset)')

# --- verify19: fix21 import (append) -------------------------------------------
V19_PATH_OLD = ('sys.path.insert(0, os.path.join(os.path.expanduser("~"),\n'
                '                                "workspace/hackathon-plugin/fix20"))')
V19_PATH_NEW = (V19_PATH_OLD + '\n'
                + 'sys.path.insert(0, os.path.join(os.path.expanduser("~"),\n'
                + '                                "workspace/hackathon-plugin/fix21"))')
V19_IMP_OLD = 'from fix20 import TYPESET_CHECKBOX_NEW as TYPESET_CHECKBOX_FIX20  # noqa: E402'
V19_IMP_NEW = (V19_IMP_OLD + '\n'
               + 'from fix21 import TYPESET_CHECKBOX21_NEW as TYPESET_CHECKBOX21  # noqa: E402')

# --- 3. verify19 system-ui subtraction (comment + list) -------------------------
V19_C7_OLD = ("# F2_APP x1), plus the CURRENT typeset checkbox (fix #20's, which\n"
              "# superseded fix19's TYPESET_CHECKBOX_NEW 1-for-1 and names `system-ui`\n"
              "# once, so the *.md mention total stays 14) — a literal *.md zero is\n"
              "# wrong: subtract the placed rule texts, then assert zero remains.\n"
              "RULE_TEXTS_WITH_SYSTEM_UI = [F2_RULE, F2_APP, STATIC19, C2_NEW, POLISH_F19,\n"
              "                             TYPESET_F19, TYPESET_CHECKBOX_FIX20]")
V19_C7_NEW = ("# F2_APP x1), plus the CURRENT typeset checkbox (fix #21's, which\n"
              "# superseded fix20's TYPESET_CHECKBOX_NEW 1-for-1 and names `system-ui`\n"
              "# once, so the *.md mention total stays 14) — a literal *.md zero is\n"
              "# wrong: subtract the placed rule texts, then assert zero remains.\n"
              "RULE_TEXTS_WITH_SYSTEM_UI = [F2_RULE, F2_APP, STATIC19, C2_NEW, POLISH_F19,\n"
              "                             TYPESET_F19, TYPESET_CHECKBOX21]")

# --- verify20: docstring checks 4 + 10 ------------------------------------------
V20_DOC4_OLD = ("  4. POLISH_F20 present in polish-pass (including the B1/X1 sentence);\n"
                "     TYPESET_F20 present in the typeset lens; TYPESET_CHECKBOX20_NEW\n"
                "     present and the fix19 checkbox GONE.\n")
V20_DOC4_NEW = ("  4. POLISH_F20 present in polish-pass (including the B1/X1 sentence);\n"
                "     TYPESET_F20 present in the typeset lens; TYPESET_CHECKBOX21_NEW\n"
                "     present and the fix20 checkbox GONE (fix #21 supersedes it).\n")

V20_DOC10_OLD = (" 10. build.sh is the post-fix20 file: it contains the fix15 + fix17 +\n"
                 "     fix19 + fix20 blocks intact and has MORE lines than post-fix19\n"
                 "     (23,314). Lines + md5 are matched against fix20/MANIFEST.md WHEN\n"
                 "     that MANIFEST exists — the coordinator writes the MANIFEST (not the\n"
                 "     fix20 worker), so until it exists this check records the measured\n"
                 "     lines + md5 for the coordinator and passes on the marker/line-count\n"
                 "     evidence; see fix20.py's docstring.\n")
V20_DOC10_NEW = (" 10. build.sh is the post-fix21 file: it contains the fix15 + fix17 +\n"
                 "     fix19 + fix20 + fix21 blocks intact and has MORE lines than post-fix19\n"
                 "     (23,314). Lines + md5 are the literal post-fix21 pair (23,647 lines,\n"
                 "     md5 8dfacb47a2a6698d47e4b4a5f8d9126c) — fix20/MANIFEST.md is the CLOSED\n"
                 "     post-fix20 record (23609 / 785fb405...) and no longer matches\n"
                 "     build.sh, so the pin is literal here, same pattern as\n"
                 "     verify15/17/18/19 (fix #21 fix-up).\n")

# --- verify20: fix21 import (path tuple = replace; import line = append) --------
V20_PATH_OLD = 'for sub in ("fix15", "fix17", "fix18", "fix19", "fix20"):'
V20_PATH_NEW = 'for sub in ("fix15", "fix17", "fix18", "fix19", "fix20", "fix21"):'
V20_IMP_OLD = ("from fix20 import (F4_SCOPE, F5, F6, B1, X1, STATIC20,  # noqa: E402\n"
               "                   F4_SCOPE_APP, F5_APP, F6_APP, B1_APP, X1_APP,\n"
               "                   POLISH_F20, POLISH_F20_BX1, TYPESET_F20,\n"
               "                   TYPESET_CHECKBOX_NEW)")
V20_IMP_NEW = (V20_IMP_OLD + "\n"
               + "from fix21 import TYPESET_CHECKBOX21_NEW as TYPESET_CHECKBOX21  # noqa: E402")

# --- verify20 check 10: MANIFEST-compare -> literal post-fix21 pin ----------------
V20_PIN10_OLD = ('manifest_path = os.path.join(PLUGIN, "fix20/MANIFEST.md")\n'
                 'if os.path.exists(manifest_path):\n'
                 '    manifest = open(manifest_path, encoding="utf-8").read()\n'
                 '    m_lines = re.search(r"^build\\.sh lines: (\\d+)$", manifest, re.M)\n'
                 '    m_md5 = re.search(r"^build\\.sh md5: ([0-9a-f]{32})$", manifest, re.M)\n'
                 '    check("fix20/MANIFEST.md records build.sh lines + md5",\n'
                 '          bool(m_lines and m_md5))\n'
                 '    if m_lines and m_md5:\n'
                 '        check(f"build.sh is {m_lines.group(1)} lines, md5 {m_md5.group(1)} (post-fix20)",\n'
                 '              len(build_lines) == int(m_lines.group(1))\n'
                 '              and build_md5 == m_md5.group(1))\n'
                 'else:\n'
                 '    print(f"   NOTE: fix20/MANIFEST.md not yet written by the coordinator; "\n'
                 '          f"measured build.sh lines={len(build_lines)}, md5={build_md5}")\n'
                 '    check("build.sh lines + md5 measured for the coordinator\'s MANIFEST "\n'
                 '          f"(lines={len(build_lines)}, md5={build_md5})", True)')
V20_PIN10_NEW = ('manifest_path = os.path.join(PLUGIN, "fix20/MANIFEST.md")\n'
                 'if os.path.exists(manifest_path):\n'
                 '    manifest = open(manifest_path, encoding="utf-8").read()\n'
                 '    m_lines = re.search(r"^build\\.sh lines: (\\d+)$", manifest, re.M)\n'
                 '    m_md5 = re.search(r"^build\\.sh md5: ([0-9a-f]{32})$", manifest, re.M)\n'
                 '    check("fix20/MANIFEST.md records build.sh lines + md5",\n'
                 '          bool(m_lines and m_md5))\n'
                 '# fix20/MANIFEST.md is the CLOSED post-fix20 record (23609 lines,\n'
                 '# md5 785fb405...); it no longer matches build.sh, so the pin below is\n'
                 '# the literal post-fix21 pair (23,647 lines / 8dfacb47...), same\n'
                 '# pattern as verify15/17/18/19 — a baseline update, not an anchor\n'
                 '# change (fix #21 fix-up).\n'
                 'check("build.sh is 23,647 lines, md5 8dfacb47a2a6698d47e4b4a5f8d9126c (post-fix21)",\n'
                 '      len(build_lines) == 23647\n'
                 '      and build_md5 == "8dfacb47a2a6698d47e4b4a5f8d9126c")')

# --- sub tables: (path, old, new, kind) -------------------------------------------
# kind "replace": old must be gone afterwards. kind "append": old is a
# substring of new; only the new text's presence is asserted afterwards.
SUBS = [
    (V15, V15_DOC_OLD, V15_DOC_NEW, "append"),
    (V15, PIN_OLD, PIN_NEW, "replace"),
    (V17, V17_DOC_OLD, V17_DOC_NEW, "append"),
    (V17, PIN_OLD, PIN_NEW, "replace"),
    (V18, V17_DOC_OLD, V17_DOC_NEW, "append"),
    (V18, PIN_OLD, PIN_NEW, "replace"),
    (V19, V19_DOC_OLD, V19_DOC_NEW, "append"),
    (V19, V19_LABEL_OLD, V19_LABEL_NEW, "replace"),
    (V19, PIN_OLD, PIN_NEW, "replace"),
    (V19, V19_CB_OLD, V19_CB_NEW, "replace"),
    (V19, V19_PATH_OLD, V19_PATH_NEW, "append"),
    (V19, V19_IMP_OLD, V19_IMP_NEW, "append"),
    (V19, V19_C7_OLD, V19_C7_NEW, "replace"),
    (V20, V20_DOC4_OLD, V20_DOC4_NEW, "replace"),
    (V20, V20_DOC10_OLD, V20_DOC10_NEW, "replace"),
    (V20, V20_PATH_OLD, V20_PATH_NEW, "replace"),
    (V20, V20_IMP_OLD, V20_IMP_NEW, "append"),
    (V20, V20_CB_OLD, V20_CB_NEW, "replace"),
    (V20, V20_PIN10_OLD, V20_PIN10_NEW, "replace"),
]


def build_sh_state():
    btext = open(BUILD_SH, encoding="utf-8").read()
    lines = btext.splitlines()
    md5 = hashlib.md5(btext.encode("utf-8")).hexdigest()
    return len(lines), md5


def preflight():
    """Check every anchor count==1 before writing anything; refuse re-run."""
    n_lines, md5 = build_sh_state()
    assert (n_lines, md5) == (NEW_LINES, NEW_MD5), \
        f"PREFLIGHT build.sh is {n_lines} lines md5 {md5}, expected {NEW_LINES} / {NEW_MD5} (post-fix21)"
    btext = open(BUILD_SH, encoding="utf-8").read()
    assert "fix21 upstream block applied" in btext, \
        "PREFLIGHT build.sh: fix21 block marker missing"
    for path, old, new, _kind in SUBS:
        text = open(path, encoding="utf-8").read()
        _once(text, old, path)
        assert new not in text, f"PREFLIGHT {path}: amended text already present"
    for _path, _old, new, _kind in SUBS:
        low = new.lower()
        for term in BANNED:
            assert term not in low, f"PREFLIGHT banned term {term!r} in a fixup21 addition"
    print("preflight OK: build.sh %d lines / %s; %d subs, banned-term scan clean"
          % (n_lines, md5, len(SUBS)))


def apply_subs():
    grouped = {}
    for path, old, new, _kind in SUBS:
        grouped.setdefault(path, []).append((old, new))
    for path, pairs in grouped.items():
        text = open(path, encoding="utf-8").read()
        for old, new in pairs:
            assert text.count(old) == 1, f"APPLY {path}: anchor count!=1"
            text = text.replace(old, new, 1)
        open(path, "w", encoding="utf-8").write(text)
        print(f"{os.path.relpath(path, PLUGIN)}: {len(pairs)} substitution(s) applied")


def self_checks():
    """After the edits: every new text present verbatim, replaced old texts gone."""
    for path, old, new, kind in SUBS:
        text = open(path, encoding="utf-8").read()
        assert text.count(new) == 1, f"SELF-CHECK {path}: amended text missing/count!=1"
        if kind == "replace":
            assert old not in text, f"SELF-CHECK {path}: old text still present"
    # Pin literals must now be the post-fix21 pair in all five verifiers.
    # NOTE: the full old md5 legitimately survives in the verify15/17/18/19
    # docstrings — they are historical pin records (one sentence per era,
    # fixup20d precedent); only the pin CHECK must be gone, and that is
    # already asserted by the "replace" kind check for PIN_OLD above.
    for path in (V15, V17, V18, V19, V20):
        text = open(path, encoding="utf-8").read()
        assert PIN_OLD not in text, f"SELF-CHECK {path}: old pin check survives"
        assert "23609" not in text or path == V20, \
            f"SELF-CHECK {path}: old line count survives"
        assert NEW_MD5 in text, f"SELF-CHECK {path}: new md5 missing"
    # verify20 never cited the full old md5 (its history cites are truncated
    # "785fb405..."), so the full old md5 must be absent there entirely.
    assert OLD_MD5 not in open(V20, encoding="utf-8").read(), \
        "SELF-CHECK verify20: old md5 survives"
    # build.sh untouched by this fix-up.
    n_lines, md5 = build_sh_state()
    assert (n_lines, md5) == (NEW_LINES, NEW_MD5), \
        f"SELF-CHECK build.sh moved: {n_lines} lines md5 {md5}"
    # The fix21 checkbox is now the asserted one in both verifiers.
    for path in (V19, V20):
        text = open(path, encoding="utf-8").read()
        assert "TYPESET_CHECKBOX21" in text, f"SELF-CHECK {path}: fix21 checkbox import missing"
    print("self-checks OK: all fixup21 amendments present verbatim; "
          "build.sh unchanged (%d lines / %s)" % (NEW_LINES, NEW_MD5))


def main():
    preflight()
    apply_subs()
    self_checks()


if __name__ == "__main__":
    main()
