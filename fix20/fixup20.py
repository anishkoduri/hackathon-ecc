#!/usr/bin/env python3
"""Fix-up #20 (Nov 12, 2026) — rule-text amendments from the fix #20
audit loop, NOT a new fix. Two sweep #25 findings + one audit #62 finding:

 1. Sweep #25 Finding 1: Taste's type catalogue pairing `fraunces`
    (library/type.json — display Fraunces, text Figtree) deals Fraunces
    as the DISPLAY face. Read literally, F4_SCOPE's "NEVER used for
    important text" forbids it. RULING (coordinator): the scope rule
    binds the face IN ITS ROLE as the body/reading face. A pairing that
    deals Fraunces (or Tiempos) as the display face, with a different
    face as the body face, is governed by fix #19 F3 / fix #20 F5, not
    by F4. On that build the face is the display face, not the body
    stand-in. The pairing stays; F4_SCOPE gains one role-scoping
    sentence. (This also corrects SPEC section 1, which claimed no
    staged source deals a body-stand-in family as display.)
 2. Sweep #25 Minor: Hallmark gates 64/67 + hallmark-floor rule 9
    prescribe the BODY face for labels/captions/table heads/nav links/
    tags/chips, while F5 says "key labels" use the display face — with
    "key label" undefined. RULING: F5 now defines "key label" (a label
    meant to stand out — hero eyebrow/kicker, featured section label,
    emphasis badge or price label). Ordinary small labels follow the
    Hallmark gates in the body face.
 3. Audit #62: skill-triggers@1.json coverage.skills says 169 (stale
    upstream metadata, generated Oct 30, 2026); the built tree has 166
    skills. The fix-up patches it to 166 at build time and verify20
    gains a check (check 13) asserting it.

FIX-UP #2 (Nov 12, fixup20b.py): the F5 example 'hero eyebrow or '
kicker' was dropped (Hallmark gate 54 bans eyebrows); _F5_INSERT and
_F5A_INSERT below are the CURRENT insert texts so this module still
imports and reverses the F5 constants correctly.

Scope is deliberately minimal: the five amended constants only
(F4_SCOPE, F5, STATIC20, F4_SCOPE_APP, F5_APP). TYPESET_F20 and
POLISH_F20 need no amendment — their "body face" already means the
face serving as body/reading text on that build. No canonical-block
change, no Grok-pin change, no new skills/agents/rules/commands, no
Campus Eats touch, fix11 never re-run.

Mechanism (fix20.py pattern): staged sources are edited in place
(Taste + orchestrate — build.sh copies them verbatim); fix20.py's
constants are updated to the amended texts (verify20.py imports them,
so the verifier automatically checks the NEW texts); upstream files
(ui-ux-pro-max, orch-build-mvp, skill-triggers@1.json) are patched
by a build.sh block appended LAST, just before STEP 5. SPEC.md is
corrected in place (section 1 claim + section 2 constants + a
fix-up note). Every substitution asserts count==1.
"""
import os
import shutil
import sys

HOME = os.path.expanduser("~")
PLUGIN = os.path.join(HOME, "workspace/hackathon-plugin")
BUILT = os.path.join(PLUGIN, "hackathon-ecc")
BUILD_SH = os.path.join(PLUGIN, "build.sh")

sys.path.insert(0, os.path.join(PLUGIN, "fix20"))
from fix20 import F4_SCOPE as F4_SCOPE_NEW, F5 as F5_NEW, STATIC20 as STATIC20_NEW, F4_SCOPE_APP as F4_SCOPE_APP_NEW, F5_APP as F5_APP_NEW  # noqa: E402 — fix20.py already holds the AMENDED texts (fixup20.py applied them); the OLD texts below are recovered by reversing each insertion

TASTE = os.path.join(PLUGIN, "new-skills/design-taste-frontend/SKILL.md")
ORCH = os.path.join(PLUGIN, "new-skills/orchestrate/SKILL.md")
FIX20_PY = os.path.join(PLUGIN, "fix20/fix20.py")
SPEC = os.path.join(PLUGIN, "fix20/SPEC.md")
VERIFY20 = os.path.join(PLUGIN, "fix20/verify20.py")

BANNED = ["claude", "codex", "anthropic", "opus", "sonnet", "haiku",
          "composer-2.5"]


def _once(text, anchor, where):
    n = text.count(anchor)
    assert n == 1, f"anchor count={n} in {where}: {anchor[:70]!r}"
    return n


# --- amended constants (old text + one inserted passage each) ---------------

_F4_ANCHOR = "They are NEVER used for important text. Anything supposed"
_F4_INSERT = ("They are NEVER used for important text. This binds each face "
              "in its role as the body/reading face: when Tiempos/Fraunces is "
              "the body face, it is never used for important text. A pairing "
              "that deals Fraunces (or Tiempos) as the *display* face, with a "
              "different face as the body face \u2014 for example the "
              "`fraunces` pairing in Taste's type catalogue (display "
              "Fraunces, Figtree body) \u2014 is governed by fix #19 F3 / "
              "fix #20 F5, not by this scope rule: on that build the face is "
              "the display face, not the body stand-in. Anything supposed")
F4_SCOPE = F4_SCOPE_NEW.replace(_F4_INSERT, _F4_ANCHOR, 1)
assert F4_SCOPE != F4_SCOPE_NEW and _F4_ANCHOR in F4_SCOPE

_F5_ANCHOR = "Not the body face, not a generic/system font. The display face is self-hosted"
_F5_INSERT = ("Not the body face, not a generic/system font. A 'key label' "
              "is a label meant to stand out \u2014 a featured section label, "
              "an emphasis badge or price label. "
              "Ordinary small labels \u2014 nav links, table heads, captions, "
              "chips, form labels, meta rows \u2014 follow the Hallmark "
              "gates: the body face, a step smaller, sentence case, "
              "untracked. The display face is self-hosted")
F5 = F5_NEW.replace(_F5_INSERT, _F5_ANCHOR, 1)
assert F5 != F5_NEW and _F5_ANCHOR in F5

_S20_ANCHOR = ("(F4 scope) The Type list marks the body face as body-only; "
               "no heading")
_S20_INSERT = ("(F4 scope) The Type list marks the body face as body-only "
               "\u2014 the body face is the face serving as body/reading "
               "text on that build, so a pairing that deals Fraunces as "
               "the display face (with a different body face) is checked "
               "under F5, not here; no heading")
STATIC20 = STATIC20_NEW.replace(_S20_INSERT, _S20_ANCHOR, 1)
assert STATIC20 != STATIC20_NEW and _S20_ANCHOR in STATIC20

_F4A_ANCHOR = "The full scope rule lives in `design-taste-frontend` step 4a."
_F4A_INSERT = ("Role-scoped (fix #20 fix-up): this binds the face as the "
               "body face; a pairing that deals Fraunces as the display "
               "face, with a different face as body, is governed by F3/F5, "
               "not by this scope rule. The full scope rule lives in "
               "`design-taste-frontend` step 4a.")
F4_SCOPE_APP = F4_SCOPE_APP_NEW.replace(_F4A_INSERT, _F4A_ANCHOR, 1)
assert F4_SCOPE_APP != F4_SCOPE_APP_NEW

_F5A_ANCHOR = ("never the body face, never a generic/system font. "
               "The full F5 rule lives in `design-taste-frontend` step 4a.")
_F5A_INSERT = ("never the body face, never a generic/system font. A 'key "
               "label' is a label meant to stand out (featured section label, "
               "emphasis badge, price label); ordinary small "
               "labels follow the Hallmark gates in the body face. The full "
               "F5 rule lives in `design-taste-frontend` step 4a.")
F5_APP = F5_APP_NEW.replace(_F5A_INSERT, _F5A_ANCHOR, 1)
assert F5_APP != F5_APP_NEW

# --- SPEC.md section 1 correction ------------------------------------------
SPEC1_OLD = """- No staged source explicitly tells a build to use the body face for
  headings; the leak is the ABSENCE of a scope statement, not a
  contradicting instruction. Nothing in the package needs replacing for
  contradiction \u2014 only the scope line needs adding."""
SPEC1_NEW = """- One staged source DOES deal a body-stand-in family as the display
  face: Taste's type catalogue pairing `fraunces` (`library/type.json`,
  display Fraunces, text Figtree) \u2014 a live, dealable path (fix #19's
  live run dealt it, per fix19/sweep24-report.md). Sweep #25 caught
  this: read literally, F4_SCOPE's "NEVER used for important text"
  forbids it. Resolution (fix-up, Nov 12): the scope rule binds the
  face IN ITS ROLE as the body/reading face \u2014 a pairing that deals
  Fraunces as the display face, with a different face as body, is
  governed by F3/F5, not F4. F4_SCOPE now carries that role-scoping
  sentence; the pairing stays. The leak fix #20 closes remains the
  absence of a scope statement for the body face.
- Sweep #25 also found the Hallmark gates (gates 64/67, hallmark-floor
  rule 9) prescribe the body face for labels/captions/table heads/nav
  links/tags/chips while F5 says "key labels" use the display face,
  with "key label" undefined. Resolution: F5 now defines "key label"
  (a label meant to stand out \u2014 hero eyebrow/kicker, featured
  section label, emphasis badge); ordinary small labels follow the
  Hallmark gates in the body face."""

# --- staged-source subs: (path, old, new) -----------------------------------
STAGED_SUBS = [
    (TASTE, F4_SCOPE, F4_SCOPE_NEW),
    (TASTE, F5, F5_NEW),
    (TASTE, STATIC20, STATIC20_NEW),
    (ORCH, F4_SCOPE, F4_SCOPE_NEW),
    (ORCH, F5, F5_NEW),
    (ORCH, STATIC20, STATIC20_NEW),
]

# --- fix20.py constant updates: (path, old-literal, new-literal) ------------
ENGINE_SUBS = [
    (FIX20_PY, F4_SCOPE, F4_SCOPE_NEW),
    (FIX20_PY, F5, F5_NEW),
    (FIX20_PY, STATIC20, STATIC20_NEW),
    (FIX20_PY, F4_SCOPE_APP, F4_SCOPE_APP_NEW),
    (FIX20_PY, F5_APP, F5_APP_NEW),
]

# --- SPEC.md subs ------------------------------------------------------------
SPEC_SUBS = [
    (SPEC, SPEC1_OLD, SPEC1_NEW),
    (SPEC, F4_SCOPE, F4_SCOPE_NEW),
    (SPEC, F5, F5_NEW),
    (SPEC, STATIC20, STATIC20_NEW),
    (SPEC, F4_SCOPE_APP, F4_SCOPE_APP_NEW),
    (SPEC, F5_APP, F5_APP_NEW),
]

# --- verify20.py: check 13 (coverage.skills == 166) --------------------------
V20_DOC_OLD = "     has a trigger key.\n\"\"\""
V20_DOC_NEW = ("     has a trigger key.\n"
               " 13. coverage.skills in skill-triggers@1.json equals the live skill count\n"
               "     (166) \u2014 audit #62 found the stale upstream 169; the fix-up patches\n"
               "     it at build time.\n\"\"\"")
V20_CHECK_OLD = "\nfailed = [n for n, ok in checks if not ok]"
V20_CHECK_NEW = ("\n# 13. Audit #62: coverage.skills is 166, not the stale upstream 169.\n"
                 "check(\"coverage.skills == 166 (audit #62 fix-up; manifest count corrected)\",\n"
                 "      _triggers[\"coverage\"][\"skills\"] == 166)\n"
                 "\nfailed = [n for n, ok in checks if not ok]")
VERIFY20_SUBS = [
    (VERIFY20, V20_DOC_OLD, V20_DOC_NEW),
    (VERIFY20, V20_CHECK_OLD, V20_CHECK_NEW),
]

# --- build.sh patch subs (against the BUILT tree): (rel, old, new) -----------
# Full replacements (not appends): the fix20 block already placed the old
# texts; this block runs after it and swaps in the amended texts.
BUILD_SUBS = [
    ("skills/ui-ux-pro-max/SKILL.md", F4_SCOPE_APP, F4_SCOPE_APP_NEW),
    ("skills/ui-ux-pro-max/SKILL.md", F5_APP, F5_APP_NEW),
    ("skills/orch-build-mvp/SKILL.md", F4_SCOPE_APP, F4_SCOPE_APP_NEW),
    ("skills/orch-build-mvp/SKILL.md", F5_APP, F5_APP_NEW),
    ("skills/orch-build-mvp/SKILL.md", STATIC20, STATIC20_NEW),
    ("manifests/context-packs/skill-triggers@1.json",
     '    "skills": 169,', '    "skills": 166,'),
]


def build_sh_block():
    """The fixup20 patch block appended to build.sh (before STEP 5)."""
    lines = []
    lines.append("# --- fixup20: F4_SCOPE role-scope + F5 key-label definition + coverage.skills 169->166 ---")
    lines.append("# (audit #62 + sweep #25 follow-up to fix #20, Nov 12. Amends the fix20")
    lines.append("#  rule texts in place; staged halves are edited by fix20/fixup20.py,")
    lines.append("#  upstream halves are patched here. Placement: before STEP 5")
    lines.append("#  (after the fix20 and weave20 blocks). Each substitution asserts")
    lines.append("#  exactly one match in the BUILT file and fails the build loudly.)")
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
    lines.append("""    assert n == 1, f'fixup20 anchor not found exactly once in {rel}: {old[:70]!r} (count={n})'""")
    lines.append("""    open(p, "w").write(t.replace(old, new))""")
    lines.append("""print("fixup20 upstream block applied")""")
    lines.append("PYEOF")
    lines.append("")
    return "\n".join(lines) + "\n"


def preflight():
    """Check every anchor count==1 before writing anything."""
    for path, old, _new in STAGED_SUBS + ENGINE_SUBS + SPEC_SUBS + VERIFY20_SUBS:
        _once(open(path, encoding="utf-8").read(), old, path)
    for path, _old, new in STAGED_SUBS + ENGINE_SUBS + SPEC_SUBS + VERIFY20_SUBS:
        text = open(path, encoding="utf-8").read()
        assert new not in text, f"PREFLIGHT {path}: amended text already present"
    for rel, old, _new in BUILD_SUBS:
        _once(open(os.path.join(BUILT, rel), encoding="utf-8").read(), old,
              f"built {rel}")
    btext = open(BUILD_SH, encoding="utf-8").read()
    assert btext.count("# STEP 5 — Counts") == 1, "PREFLIGHT build.sh: STEP 5 anchor"
    assert "fixup20 upstream block applied" not in btext, \
        "PREFLIGHT build.sh: fixup20 block already present"
    assert "fix20 upstream block applied" in btext, \
        "PREFLIGHT build.sh: fix20 block marker missing"
    assert "weave20: upstream skill pointers applied" in btext, \
        "PREFLIGHT build.sh: weave20 block marker missing"
    # No banned terms in any addition or in the block itself.
    blobs = [new for _, _, new in STAGED_SUBS + ENGINE_SUBS + SPEC_SUBS
             + VERIFY20_SUBS + BUILD_SUBS]
    blobs.append(build_sh_block())
    for blob in blobs:
        low = blob.lower()
        for term in BANNED:
            assert term not in low, f"PREFLIGHT banned term {term!r} in a fixup20 addition"
    print("preflight OK: %d file subs + %d build subs, banned-term scan clean"
          % (len(STAGED_SUBS + ENGINE_SUBS + SPEC_SUBS + VERIFY20_SUBS),
             len(BUILD_SUBS)))


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


def self_checks():
    """After the edits: every new text present verbatim, old texts gone."""
    for path, old, new in STAGED_SUBS:
        text = open(path, encoding="utf-8").read()
        assert text.count(new) == 1, f"SELF-CHECK {path}: amended text missing"
        assert old not in text, f"SELF-CHECK {path}: old text still present"
    for path, old, new in ENGINE_SUBS:
        text = open(path, encoding="utf-8").read()
        assert text.count(new) == 1, f"SELF-CHECK {path}: amended constant missing"
        assert old not in text, f"SELF-CHECK {path}: old constant still present"
    for path, old, new in SPEC_SUBS:
        text = open(path, encoding="utf-8").read()
        assert text.count(new) == 1, f"SELF-CHECK {path}: amended SPEC text missing"
        assert old not in text, f"SELF-CHECK {path}: old SPEC text still present"
    vtext = open(VERIFY20, encoding="utf-8").read()
    assert 'coverage.skills == 166' in vtext, "SELF-CHECK verify20: check 13 missing"
    assert "13. coverage.skills in skill-triggers@1.json" in vtext, \
        "SELF-CHECK verify20: docstring check 13 missing"
    btext = open(BUILD_SH, encoding="utf-8").read()
    assert "fixup20 upstream block applied" in btext, "SELF-CHECK build.sh: fixup20 block missing"
    assert btext.count("# STEP 5 — Counts") == 1, "SELF-CHECK build.sh: STEP 5 anchor damaged"
    assert btext.find("fixup20 upstream block applied") > btext.find("weave20: upstream skill pointers applied"), \
        "SELF-CHECK build.sh: fixup20 block must sit after the weave20 block"
    print("self-checks OK: all fixup20 amendments present verbatim; old texts gone")


def main():
    preflight()
    shutil.copy2(BUILD_SH, BUILD_SH + ".before-fixup20")
    apply_subs(STAGED_SUBS)
    apply_subs(ENGINE_SUBS)
    apply_subs(SPEC_SUBS)
    apply_subs(VERIFY20_SUBS)
    btext = open(BUILD_SH, encoding="utf-8").read()
    assert btext.count("# STEP 5 — Counts") == 1
    block = build_sh_block()
    btext = btext.replace("# STEP 5 — Counts", block + "# STEP 5 — Counts", 1)
    open(BUILD_SH, "w", encoding="utf-8").write(btext)
    print("build.sh: fixup20 block appended (%d upstream subs, before STEP 5)"
          % len(BUILD_SUBS))
    self_checks()


if __name__ == "__main__":
    main()
