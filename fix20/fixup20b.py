#!/usr/bin/env python3
"""Fix-up #20b (Nov 12, 2026) — three MINOR sweep #26 findings, no new
rules. Applied after audit #63 (ZERO ERRORS), dry-run #32 (13/13 PASS),
and sweep #26 (NOT CLEAN — 0 blocking, 3 minor).

 1. MINOR-1: F5's key-label definition leads with "a hero eyebrow or
    kicker" — but Hallmark gate 54 (Floor, never waivable) bans the
    eyebrow outright, and floor rule 9 opens "Never an eyebrow". The
    example invites a builder to create a hero eyebrow in the display
    face believing F5 blesses it. RULING (coordinator): drop the
    eyebrow/kicker example. The DEFINITION ("a label meant to stand
    out") is unchanged and still governs — only the illustration
    changes. New examples: featured section label, emphasis badge,
    price label. (Audit #63 had already noted this as a non-error
    observation; sweep #26 makes it a minor to fix.)
 2. MINOR-2: wrong section cite "hackathon-mode §37" (5 occurrences:
    verify20.py:84, :168; weave20.py:167, :205, :478). hackathon-mode.mdc
    has only §1–§7; the frontend-design-direction exclusion lives at
    §5, line 38. Correct cite: §5. Comment/census-reason strings only;
    no check depends on the number. (weave1/MANIFEST.md:127 hedges the
    same cite — a closed historical manifest, left as-is and noted.)
 3. MINOR-3: stale Batch E comment in build.sh:20967-20976 — claims the
    block is "placed LAST — just before STEP 5" and that "no build.sh
    patch touches skills/less-flat-ui/SKILL.md". Both false since
    weave1/weave20: the block sits ~2,500 lines before STEP 5 and three
    other subs patch less-flat-ui (W2-G9, W2-C1, weave20 A10). Comment
    corrected in place (comment-only, zero behavior).

Scope: F5 + F5_APP example lists only (definition untouched); five
§37→§5 cite fixes; one build.sh comment. No canonical-block change,
no Grok-pin change, no new skills/agents/rules/commands. The fixup20
block in build.sh still carries the OLD F5_APP text as its (already
applied) `new` literal — that is generator history, left as-is; the
fixup20b block runs after it and swaps the built text.

Mechanism (fixup20.py pattern): staged sources edited in place (Taste
+ orchestrate — build.sh copies them verbatim); fix20.py's constants
updated to the amended texts (verify20.py imports them, so it checks
the NEW texts); fixup20.py's _F5_INSERT/_F5A_INSERT updated to the
new insert texts so that module still imports and reverses correctly;
upstream app mirrors patched by a build.sh block appended LAST, just
before STEP 5. SPEC.md corrected in place (§2 constants, §1 + §11
mentions). Every substitution asserts count==1 (cite subs assert
their per-file counts).
"""
import os
import shutil
import sys

HOME = os.path.expanduser("~")
PLUGIN = os.path.join(HOME, "workspace/hackathon-plugin")
BUILT = os.path.join(PLUGIN, "hackathon-ecc")
BUILD_SH = os.path.join(PLUGIN, "build.sh")

sys.path.insert(0, os.path.join(PLUGIN, "fix20"))
from fix20 import F5 as F5_NEW2, F5_APP as F5_APP_NEW2  # noqa: E402 — fix20.py holds the fixup20b-amended texts

TASTE = os.path.join(PLUGIN, "new-skills/design-taste-frontend/SKILL.md")
ORCH = os.path.join(PLUGIN, "new-skills/orchestrate/SKILL.md")
FIX20_PY = os.path.join(PLUGIN, "fix20/fix20.py")
FIXUP20_PY = os.path.join(PLUGIN, "fix20/fixup20.py")
SPEC = os.path.join(PLUGIN, "fix20/SPEC.md")
VERIFY20 = os.path.join(PLUGIN, "fix20/verify20.py")
WEAVE20 = os.path.join(PLUGIN, "fix20/weave20.py")

BANNED = ["claude", "codex", "anthropic", "opus", "sonnet", "haiku",
          "composer-2.5"]


def _once(text, anchor, where):
    n = text.count(anchor)
    assert n == 1, f"anchor count={n} in {where}: {anchor[:70]!r}"
    return n


# --- amended F5 texts (example list only; definition untouched) -------------
_F5_EX_OLD = ("a hero eyebrow or kicker, a featured section label, "
              "an emphasis badge or price label")
_F5_EX_NEW = "a featured section label, an emphasis badge or price label"
F5 = F5_NEW2.replace(_F5_EX_NEW, _F5_EX_OLD, 1)
assert F5 != F5_NEW2 and _F5_EX_OLD in F5  # reversed: fix20.py now holds the amended text

_F5A_EX_OLD = "(hero eyebrow/kicker, featured section label, emphasis badge)"
_F5A_EX_NEW = "(featured section label, emphasis badge, price label)"
F5_APP = F5_APP_NEW2.replace(_F5A_EX_NEW, _F5A_EX_OLD, 1)
assert F5_APP != F5_APP_NEW2 and _F5A_EX_OLD in F5_APP  # reversed: fix20.py now holds the amended text

# --- staged-source subs: (path, old, new) -----------------------------------
STAGED_SUBS = [
    (TASTE, F5, F5_NEW2),
    (ORCH, F5, F5_NEW2),
]

# --- fix20.py constant updates ----------------------------------------------
ENGINE_SUBS = [
    (FIX20_PY, F5, F5_NEW2),
    (FIX20_PY, F5_APP, F5_APP_NEW2),
]

# --- SPEC.md subs ------------------------------------------------------------
SPEC_SUBS = [
    (SPEC, F5, F5_NEW2),
    (SPEC, F5_APP, F5_APP_NEW2),
    (SPEC,
     "(a label meant to stand out — hero eyebrow/kicker, featured\n"
     "  section label, emphasis badge)",
     "(a label meant to stand out — featured\n"
     "  section label, emphasis badge, price label)"),
    (SPEC,
     "meant to stand out — hero eyebrow/kicker, featured section label,\n"
     "   emphasis badge or price label.",
     "meant to stand out — featured section label,\n"
     "   emphasis badge or price label."),
]

# --- fixup20.py: keep it importable (its reversal reads the F5 constants) ---
FIXUP20_DOC_ANCHOR = "Scope is deliberately minimal:"
FIXUP20_DOC_NOTE = ("FIX-UP #2 (Nov 12, fixup20b.py): the F5 example 'hero eyebrow or '\n"
                    "kicker' was dropped (Hallmark gate 54 bans eyebrows); _F5_INSERT and\n"
                    "_F5A_INSERT below are the CURRENT insert texts so this module still\n"
                    "imports and reverses the F5 constants correctly.\n\n")
FIXUP20_SUBS = [
    # Source-fragment forms: _F5_INSERT/_F5A_INSERT are split across
    # source lines, so the evaluated phrases are not contiguous in the file.
    (FIXUP20_PY,
     '"is a label meant to stand out \\u2014 a hero eyebrow or kicker, "\n'
     '              "a featured section label, an emphasis badge or price label. "',
     '"is a label meant to stand out \\u2014 a featured section label, "\n'
     '              "an emphasis badge or price label. "'),
    (FIXUP20_PY,
     '"label\' is a label meant to stand out (hero eyebrow/kicker, "\n'
     '               "featured section label, emphasis badge); ordinary small "',
     '"label\' is a label meant to stand out (featured section label, "\n'
     '               "emphasis badge, price label); ordinary small "'),
    (FIXUP20_PY, FIXUP20_DOC_ANCHOR, FIXUP20_DOC_NOTE + FIXUP20_DOC_ANCHOR),
]

# --- fix20.py docstring: record the fix-up ----------------------------------
FIX20_DOC_ANCHOR = "Staged-source edits (direct, build.sh copies them verbatim):"
FIX20_DOC_NOTE = ("FIX-UP #2 (Nov 12, 2026 — sweep #26 MINOR-1): fix20/fixup20b.py\n"
                  "drops 'hero eyebrow or kicker' from the F5/F5_APP key-label\n"
                  "examples (Hallmark gate 54 bans eyebrows); the definition\n"
                  "('a label meant to stand out') is unchanged. See SPEC.md\n"
                  "section 11.\n\n")
FIX20_DOC_SUBS = [
    (FIX20_PY, FIX20_DOC_ANCHOR, FIX20_DOC_NOTE + FIX20_DOC_ANCHOR),
]

# --- cite fixes: (path, old, new, expected-count) — replace-all in file -----
CITE_SUBS = [
    (VERIFY20, "hackathon-mode §37", "hackathon-mode §5", 2),
    (WEAVE20, "hackathon-mode §37", "hackathon-mode §5", 2),
    (WEAVE20, "hackathon-mode section 37", "hackathon-mode section 5", 1),
]

# --- build.sh Batch E comment fix (comment-only, zero behavior) -------------
BATCHE_SUBS = [
    (BUILD_SH,
     "every build, so this fix lives here as a patch block placed LAST — just\n"
     "# before STEP 5 — after the GATE / carve-out / Batch E / Batch F /\n"
     "# fix-program-#3 patches.",
     "every build, so this fix lives here as a patch block in the fix #4 era\n"
     "# position — after the GATE / carve-out / Batch E / Batch F /\n"
     "# fix-program-#3 patches. (Fix-up Nov 12: it is NOT last — fix15/17/19/20,\n"
     "# weave20, fixup20, and fixup20b blocks run after it, before STEP 5.)"),
    (BUILD_SH,
     "# no build.sh patch touches skills/less-flat-ui/SKILL.md).",
     "# THREE other build.sh patches touch skills/less-flat-ui/SKILL.md (W2-G9,\n"
     "# W2-C1, weave20 A10) plus this block itself)."),
    (BUILD_SH,
     "The substitution asserts exactly one match. The coordinator\n"
     "# inserts this block last, just before STEP 5.",
     "The substitution asserts exactly one match.\n"
     "# (Fix-up Nov 12: this block does not sit last; later fix blocks run after it.)"),
]

# --- build.sh patch subs (against the BUILT tree): (rel, old, new) -----------
BUILD_SUBS = [
    ("skills/ui-ux-pro-max/SKILL.md", F5_APP, F5_APP_NEW2),
    ("skills/orch-build-mvp/SKILL.md", F5_APP, F5_APP_NEW2),
]


def build_sh_block():
    """The fixup20b patch block appended to build.sh (before STEP 5)."""
    lines = []
    lines.append("# --- fixup20b: F5 key-label examples (drop eyebrow/kicker) ---")
    lines.append("# (sweep #26 MINOR-1 follow-up to fix #20, Nov 12. Amends the F5/F5_APP")
    lines.append("#  example lists in place; staged halves are edited by fix20/fixup20b.py,")
    lines.append("#  upstream halves are patched here. Placement: before STEP 5")
    lines.append("#  (after the fix20, weave20, and fixup20 blocks). Each substitution")
    lines.append("#  asserts exactly one match in the BUILT file and fails the build loudly.)")
    lines.append("""python3 - "$PLUGIN_DIR" <<'PYEOF'""")
    lines.append("import os, sys")
    lines.append("base = sys.argv[1]")
    lines.append("")
    lines.append("subs = [")
    for rel, old, new in BUILD_SUBS:
        lines.append("  (%s," % repr(rel))
        lines.append("   %s," % repr(old))
        lines.append("   %s)," % repr(new))
    lines.append("]")
    lines.append("for rel, old, new in subs:")
    lines.append("    p = os.path.join(base, rel)")
    lines.append("    t = open(p).read()")
    lines.append("    n = t.count(old)")
    lines.append("""    assert n == 1, f'fixup20b anchor not found exactly once in {rel}: {old[:70]!r} (count={n})'""")
    lines.append("""    open(p, "w").write(t.replace(old, new))""")
    lines.append("""print("fixup20b upstream block applied")""")
    lines.append("PYEOF")
    lines.append("")
    return "\n".join(lines) + "\n"


def preflight():
    """Check every anchor count==1 before writing anything."""
    for path, old, _new in (STAGED_SUBS + ENGINE_SUBS + SPEC_SUBS + FIXUP20_SUBS
                            + FIX20_DOC_SUBS + BATCHE_SUBS):
        _once(open(path, encoding="utf-8").read(), old, path)
    for path, _old, new in (STAGED_SUBS + ENGINE_SUBS + SPEC_SUBS + FIXUP20_SUBS
                            + FIX20_DOC_SUBS + BATCHE_SUBS):
        text = open(path, encoding="utf-8").read()
        assert new not in text, f"PREFLIGHT {path}: amended text already present"
    for path, old, _new, n in CITE_SUBS:
        text = open(path, encoding="utf-8").read()
        assert text.count(old) == n, \
            f"PREFLIGHT {path}: cite count={text.count(old)}, expected {n}"
        assert _new not in text, f"PREFLIGHT {path}: new cite already present"
    for rel, old, _new in BUILD_SUBS:
        _once(open(os.path.join(BUILT, rel), encoding="utf-8").read(), old,
              f"built {rel}")
    btext = open(BUILD_SH, encoding="utf-8").read()
    assert btext.count("# STEP 5 — Counts") == 1, "PREFLIGHT build.sh: STEP 5 anchor"
    assert "fixup20b upstream block applied" not in btext, \
        "PREFLIGHT build.sh: fixup20b block already present"
    assert "fixup20 upstream block applied" in btext, \
        "PREFLIGHT build.sh: fixup20 block marker missing"
    blobs = [new for _, _, new in (STAGED_SUBS + ENGINE_SUBS + SPEC_SUBS
                                   + FIXUP20_SUBS + FIX20_DOC_SUBS
                                   + BATCHE_SUBS + BUILD_SUBS)]
    blobs.append(build_sh_block())
    for blob in blobs:
        low = blob.lower()
        for term in BANNED:
            assert term not in low, f"PREFLIGHT banned term {term!r} in a fixup20b addition"
    print("preflight OK: file subs + %d cite subs + %d build subs, banned-term scan clean"
          % (len(CITE_SUBS), len(BUILD_SUBS)))


def apply_subs(subs):
    grouped = {}
    for path, old, new in subs:
        grouped.setdefault(path, []).append((old, new))
    for path, pairs in grouped.items():
        text = open(path, encoding="utf-8").read()
        for old, new in pairs:
            assert text.count(old) == 1, f"APPLY {path}: anchor count!=1"
            text = text.replace(old, new, 1)
        open(path, "w", encoding="utf-8").write(text)
        print(f"{os.path.relpath(path, PLUGIN)}: {len(pairs)} substitution(s) applied")


def apply_cite_subs():
    grouped = {}
    for path, old, new, n in CITE_SUBS:
        grouped.setdefault(path, []).append((old, new, n))
    for path, triples in grouped.items():
        text = open(path, encoding="utf-8").read()
        for old, new, n in triples:
            assert text.count(old) == n, f"APPLY {path}: cite count!= {n}"
            text = text.replace(old, new)
        open(path, "w", encoding="utf-8").write(text)
        print(f"{os.path.relpath(path, PLUGIN)}: {len(triples)} cite fix(es) applied")


def self_checks():
    """After the edits: every new text present verbatim, old texts gone."""
    for path, old, new in STAGED_SUBS + ENGINE_SUBS + SPEC_SUBS + FIXUP20_SUBS[:2]:
        text = open(path, encoding="utf-8").read()
        assert text.count(new) == 1, f"SELF-CHECK {path}: amended text missing"
        assert old not in text, f"SELF-CHECK {path}: old text still present"
    for path, old, new in FIXUP20_SUBS[2:] + FIX20_DOC_SUBS:
        text = open(path, encoding="utf-8").read()
        assert new in text, f"SELF-CHECK {path}: doc note missing"
    for path, old, new, _n in CITE_SUBS:
        text = open(path, encoding="utf-8").read()
        assert old not in text, f"SELF-CHECK {path}: old cite still present"
        assert new in text, f"SELF-CHECK {path}: new cite missing"
    btext = open(BUILD_SH, encoding="utf-8").read()
    for _path, _old, new in BATCHE_SUBS:
        assert new in btext, "SELF-CHECK build.sh: Batch E comment fix missing"
    assert "fixup20b upstream block applied" in btext, "SELF-CHECK build.sh: fixup20b block missing"
    assert btext.count("# STEP 5 — Counts") == 1, "SELF-CHECK build.sh: STEP 5 anchor damaged"
    assert btext.find("fixup20b upstream block applied") > btext.find("fixup20 upstream block applied"), \
        "SELF-CHECK build.sh: fixup20b block must sit after the fixup20 block"
    print("self-checks OK: all fixup20b amendments present verbatim; old texts gone")


def main():
    preflight()
    shutil.copy2(BUILD_SH, BUILD_SH + ".before-fixup20b")
    apply_subs(STAGED_SUBS)
    apply_subs(ENGINE_SUBS)
    apply_subs(SPEC_SUBS)
    apply_subs(FIXUP20_SUBS)
    apply_subs(FIX20_DOC_SUBS)
    apply_cite_subs()
    apply_subs(BATCHE_SUBS)
    btext = open(BUILD_SH, encoding="utf-8").read()
    assert btext.count("# STEP 5 — Counts") == 1
    block = build_sh_block()
    btext = btext.replace("# STEP 5 — Counts", block + "# STEP 5 — Counts", 1)
    open(BUILD_SH, "w", encoding="utf-8").write(btext)
    print("build.sh: fixup20b block appended (%d upstream subs, before STEP 5)"
          % len(BUILD_SUBS))
    self_checks()


if __name__ == "__main__":
    main()
