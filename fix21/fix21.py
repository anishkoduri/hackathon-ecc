#!/usr/bin/env python3
"""Fix program #21: long body and small text only; every text element gets
an artistic font design decision (fix21/SPEC.md sections 0-2).

Tightens fix #19 F4 / fix #20 F4_SCOPE so the Tiempos/Fraunces body face
cannot serve as a general default: it is for LONG-LENGTH body text and
SMALL incidental text only, never main text we see visually. And every
text element now carries a deliberate, recorded artistic font design
decision (F7) — which face, why, what job it serves, how it matches the
theme and the brand — recorded in the decision record's Type list, per
text element or per genuinely uniform text class (a blanket 'all text'
line is not a class decision).

Rules (SPEC.md section 2; constants verbatim):
  F4_TIGHT  Tiempos rule tightened: long body + small text only
  F7        every text element gets an artistic font design decision
  STATIC21  fix #21 static checks (F4-tight + F7 items)
  POLISH_F21 / TYPESET_F21 / TYPESET_CHECKBOX21 (typeset lens)

SPEC DEVIATIONS (recorded):
  - STATIC20 build.sh anchor: the parent task states "STATIC20 occurs
    once build.sh-wide" for the orch-build-mvp step-6 entry. Measured:
    the AMENDED STATIC20 (fix20.py, post-fixup) occurs once build.sh-wide
    — but that occurrence is the fixup20 block's replacement (NEW) text,
    NOT the fix20 block's mvp step-6 entry, which carries the pre-fixup
    OLD STATIC20 (recovered by reversing fixup20.py's _S20_INSERT, as
    fixup20.py itself does). The OLD text occurs twice build.sh-wide
    (fix20 block entry + fixup20 block OLD text) and once inside the
    fix20 block's mvp step-6 entry slice. The fix21 build.sh sub's
    runtime anchor is still the AMENDED STATIC20: the fix21 block runs
    after fixup20, so by then the built mvp file holds the amended text
    (verified: amended STATIC20 count==1 in the current built
    skills/orch-build-mvp/SKILL.md). Preflight asserts all three legs:
    amended STATIC20 ==1 in the built mvp file, ==1 build.sh-wide (in
    the fixup20 block), and OLD STATIC20 ==1 inside the fix20 block's
    mvp step-6 entry slice.
  - verify20.py currently reports 169/169 checks (fix20/MANIFEST.md
    says 168; the fixup20d check-18 lowercase assertion added one).
    The task expects 169/169, consistent with the measured run.
  - SPEC section 7 check 4 names the new typeset checkbox
    "TYPESET_CHECKBOX21_NEW" while section 2 names the constant
    TYPESET_CHECKBOX21. This engine defines TYPESET_CHECKBOX21 and
    aliases TYPESET_CHECKBOX21_NEW to the same text, so both namings
    resolve.

Staged-source edits (direct, build.sh copies them verbatim):
  new-skills/design-taste-frontend/SKILL.md ... F4_TIGHT+F7 (step 4a,
                                                    after X1),
                                                    STATIC21 (step 6)
  new-skills/orchestrate/SKILL.md ................. F4_TIGHT+F7
                                                    (design-package rule,
                                                    after X1),
                                                    STATIC21 (Verify 5a)
  round2-skills/polish-pass/SKILL.md .............. POLISH_F21 (harmony)
  round2-skills/polish-pass/reference/lenses/typeset.md .. TYPESET_F21
                                                    + checkbox swap
Build.sh patch block (upstream, no staged source):
  skills/ui-ux-pro-max/SKILL.md ................... F4_TIGHT_APP+F7_APP
                                                    (after X1_APP)
  skills/orch-build-mvp/SKILL.md .................. same app mirrors
                                                    (step 4, after X1_APP),
                                                    STATIC21 (step 6)

Every substitution asserts count==1. A preflight pass checks every
anchor before any file is written, so a bad anchor aborts before
touching anything. X1_APP occurs TWICE in build.sh (once per patched
file), so the preflight anchors it WITHIN each file's fix20 patch-block
entry, never as a bare build.sh-wide count (same per-entry technique
fix20.py used for D19_APP inside the fix19 block).
"""
import os
import shutil

HOME = os.path.expanduser("~")
PLUGIN = os.path.join(HOME, "workspace/hackathon-plugin")
BUILT = os.path.join(PLUGIN, "hackathon-ecc")
BUILD_SH = os.path.join(PLUGIN, "build.sh")

TASTE = os.path.join(PLUGIN, "new-skills/design-taste-frontend/SKILL.md")
ORCH = os.path.join(PLUGIN, "new-skills/orchestrate/SKILL.md")
POLISH = os.path.join(PLUGIN, "round2-skills/polish-pass/SKILL.md")
TYPESET = os.path.join(PLUGIN, "round2-skills/polish-pass/reference/lenses/typeset.md")

# --- rule texts (SPEC section 2, verbatim) ---

F4_TIGHT = """**Long body and small text only — the Tiempos rule tightened (fix #21 — fix #19 F4 tightened).** Tiempos and the Fraunces stand-in are for LONG-LENGTH body text and SMALL incidental text only — running paragraphs of reading prose, and small text here and there (ordinary small labels: captions, meta rows, table heads, form labels, chips, small nav links). They are NOT a default for text generally, and they are NEVER used for main text we see visually. 'Body and plain text use Tiempos' (fix #19 F4) reads, after this fix, as long-length body text and small incidental text only. A build that sets its labels, captions, buttons, prices, names, or any other text element in the body face by default — with no artistic font decision behind it — is an incomplete build, even if no single element is 'important' text. The body face is the face serving as body/reading text on that build; the role-scoping from fix #20 stands (a pairing that deals Fraunces as the display face, with a different face as body, is governed by fix #19 F3 / fix #20 F5, not by this scope rule)."""

F7 = """**Every text element gets an artistic font design decision (fix #21 F7).** Every text element — heading, label, caption, button, price, name, body, meta row, table head, chip, nav link, call to action — has a deliberate, recorded artistic font design decision behind it: which face, why this face, what job it serves, how it matches the theme and the brand. The decision is recorded in the decision record's Type list, per text element — or per text class where the class is genuinely uniform (one decision line per class, naming the class and the face and the reason; a blanket 'all text' line is not a class decision). No text element defaults to the body face without a decision. Main text we see visually — headings, display type, hero text, prominent labels, prices, names — uses the unique important font (fix #20 F5) or another artistic face chosen through the skills, never the body face as a default. A text element with no recorded artistic font decision, or a main visible text element set in the body face, is an incomplete build — a static check item in step 6, never a screen verdict. The decision is covered by its fix #19 D19 reason (job / considered-and-rejected / theme-fit across the six full-experience dimensions); the font decision is the D19 reason for that text element's font choice."""

STATIC21 = """**Fix #21 static checks (all static checks, never screen verdicts).** (F4 tight) The Type list marks the body face as long-body-and-small-text-only — no token for main visible text points at the body face; the body face serves long-length body text and small incidental text only. (F7) Every text element in the Type list — or every genuinely uniform text class — carries its recorded artistic font decision (face + why + job + theme/brand fit); a text element with no recorded decision is an incomplete build; a main visible text element (heading, display, hero, prominent label, price, name, call to action) set in the body face is an incomplete build; a blanket 'all text' class line is not a class decision. (F7 record) The decision record lists the font decision per text element or per uniform class; the D19 reason covers the font choice."""

# --- app-surface mirrors ---

F4_TIGHT_APP = """**Long body and small text only (fix #21 — F4 tightened, app surfaces).** On app surfaces, Tiempos and the Fraunces stand-in are for long-length body text and small incidental text only — never a default for text generally, never main visible text. The full tightened scope rule lives in `design-taste-frontend` step 4a."""

F7_APP = """**Every text element gets an artistic font design decision (fix #21 F7, app surfaces).** On app surfaces, every text element has a deliberate, recorded artistic font design decision — which face, why, what job it serves, how it matches the theme and the brand — recorded in MASTER.md's Type list, per text element or per genuinely uniform text class. No element defaults to the body face without a decision; main visible text uses the display face (fix #20 F5) or another artistic face chosen through the skills. The full F7 rule lives in `design-taste-frontend` step 4a."""

# --- typeset lens + polish-pass harmony ---

TYPESET_F21 = """**Long body and small text only; every text element gets an artistic font decision (fix #21).** The body face (Tiempos or the Fraunces stand-in) is for long-length body text and small incidental text only — a heading, hero line, call to action, key label, price, name, or prominent label set in the body face is a finding. Every text element needs a recorded artistic font decision (face + why + job + theme/brand fit) in the Type list — an element with no recorded decision is a finding, and a blanket 'all text' class line is not a decision. The squint test (check 1) is the visual proof: heading and body must read apart at a blur, by face as well as size."""

TYPESET_CHECKBOX21 = """- [ ] A custom typeface has a stated reason; shipped font files are static instances (one per weight, opsz baked in) — no variable file is shipped, no `system-ui` fallback (fix #19 F2); the body face is used for long-length body text and small incidental text only, and important text uses the dealt display face with its recorded impressive-choice justification (fix #20); every text element has a recorded artistic font decision (fix #21 F7)."""

# SPEC section 7 check 4 names this TYPESET_CHECKBOX21_NEW; section 2
# names it TYPESET_CHECKBOX21 — both resolve to the same text.
TYPESET_CHECKBOX21_NEW = TYPESET_CHECKBOX21

POLISH_F21 = """ It also verifies the tightened font scope (fix #21): each Type-list body-face row is marked long-body-and-small-text-only, no main visible text token points at the body face, and every text element carries its recorded artistic font decision — a token or element that does not is a harmony divergence, recorded as candidate evidence, never a verdict."""

# --- anchors imported from fix19 / fix20 (must stay verbatim) ---
import sys
sys.path.insert(0, os.path.join(PLUGIN, "fix19"))
sys.path.insert(0, os.path.join(PLUGIN, "fix20"))
from fix19 import (D19_RULE, STATIC19, POLISH_F19, TYPESET_F19,  # noqa: E402
                   F4_RULE, F4_APP, D19_APP)
from fix20 import (F4_SCOPE, F5, F6, B1, X1, STATIC20,  # noqa: E402
                   F4_SCOPE_APP, F5_APP, F6_APP, B1_APP, X1_APP,
                   POLISH_F20, TYPESET_F20,
                   TYPESET_CHECKBOX_NEW as TYPESET_CHECKBOX_FIX20)

# Pre-fixup OLD STATIC20, recovered by reversing fixup20.py's insertion
# (same reversal fixup20.py itself applies). The fix20 build.sh block's
# orch-build-mvp step-6 entry carries this OLD text; the fixup20 block
# swaps it for the amended STATIC20 at build time.
_S20_ANCHOR = ("(F4 scope) The Type list marks the body face as body-only; "
               "no heading")
_S20_INSERT = ("(F4 scope) The Type list marks the body face as body-only "
               "\u2014 the body face is the face serving as body/reading "
               "text on that build, so a pairing that deals Fraunces as "
               "the display face (with a different body face) is checked "
               "under F5, not here; no heading")
STATIC20_OLD = STATIC20.replace(_S20_INSERT, _S20_ANCHOR, 1)
assert STATIC20_OLD != STATIC20 and _S20_ANCHOR in STATIC20_OLD

STEP4A_ADD = "\n\n" + F4_TIGHT + "\n\n" + F7
APP_MIRRORS_ADD = "\n\n" + F4_TIGHT_APP + "\n\n" + F7_APP

# --- staged-source appends: (path, old-anchor, addition) -------------------
STAGED_SUBS = [
    # Taste step 4a: F4_TIGHT + F7 after the X1 rule.
    (TASTE, X1, STEP4A_ADD),
    # Taste step 6: STATIC21 after STATIC20.
    (TASTE, STATIC20, "\n\n   " + STATIC21),
    # Orchestrate design-package rule: same two rules after X1.
    (ORCH, X1, STEP4A_ADD),
    # Orchestrate Verify 5a: STATIC21 inline after STATIC20 (fix19
    # deviation-3 precedent: after the 5a paragraph's final sentence,
    # NOT after the two-line "...5b. Final polish" anchor).
    (ORCH, STATIC20, " " + STATIC21),
    # Polish-pass harmony: POLISH_F21 after POLISH_F20.
    (POLISH, POLISH_F20, POLISH_F21),
    # Typeset lens: TYPESET_F21 after TYPESET_F20.
    (TYPESET, TYPESET_F20, "\n\n" + TYPESET_F21),
]

# Prepend-style replacements (old -> new, full text).
REPLACEMENTS = [
    (TYPESET, TYPESET_CHECKBOX_FIX20, TYPESET_CHECKBOX21),
]

# --- build.sh patch subs (against the BUILT tree): (rel, old, addition) -----
BUILD_SUBS = [
    # ui-ux-pro-max: app mirrors after X1_APP (anti-generic bar area).
    ("skills/ui-ux-pro-max/SKILL.md", X1_APP, APP_MIRRORS_ADD),
    # orch-build-mvp: app mirrors after X1_APP (step 4).
    ("skills/orch-build-mvp/SKILL.md", X1_APP, APP_MIRRORS_ADD),
    # orch-build-mvp: STATIC21 in step 6 after STATIC20 (amended text:
    # the fix21 block runs after fixup20, so the built file holds it).
    ("skills/orch-build-mvp/SKILL.md", STATIC20, "\n\n" + STATIC21),
]

BANNED = ["claude", "codex", "anthropic", "opus", "sonnet", "haiku",
          "composer-2.5"]


def build_sh_block():
    """The fix21 patch block appended to build.sh (before STEP 5)."""
    lines = []
    lines.append("# --- fix21: long body and small text only; every text element gets an artistic font design decision (F4_TIGHT/F7) ---")
    lines.append("# (skills/ui-ux-pro-max and orch-build-mvp are upstream; they have no")
    lines.append("#  staged source and are patched here. The staged-source halves --")
    lines.append("#  design-taste-frontend (step 4a + step 6), orchestrate (design-package")
    lines.append("#  rule + Verify 5a), polish-pass (harmony), typeset lens -- are applied")
    lines.append("#  by fix21/fix21.py to their sources. All anchors were verified")
    lines.append("#  count==1 against the post-fix20 built tree by fix21.py's preflight;")
    lines.append("#  the asserts below re-verify at build time and fail the build loudly")
    lines.append("#  on mismatch. X1_APP occurs twice in build.sh (once per patched")
    lines.append("#  file) -- the runtime asserts below are per FILE, never build.sh-wide.")
    lines.append("#  STATIC20 note: the fix21 block runs after fixup20, so the built")
    lines.append("#  orch-build-mvp file holds the AMENDED STATIC20, which is the")
    lines.append("#  runtime anchor for the step-6 sub (see fix21.py docstring).)")
    lines.append("# Placement: before STEP 5 (after the fix20 blocks).")
    lines.append("python3 - \"$PLUGIN_DIR\" <<'PYEOF'")
    lines.append("import os, sys")
    lines.append("base = sys.argv[1]")
    lines.append("")
    lines.append("subs = [")
    for rel, old, add in BUILD_SUBS:
        lines.append("  (%s," % repr(rel))
        lines.append("   %s," % repr(old))
        lines.append("   %s)," % repr(add))
    lines.append("]")
    lines.append("for rel, old, add in subs:")
    lines.append("    p = os.path.join(base, rel)")
    lines.append("    t = open(p).read()")
    lines.append("    n = t.count(old)")
    lines.append("    assert n == 1, f\"fix21 anchor not found exactly once in {rel}: {old[:70]!r} (count={n})\"")
    lines.append("    open(p, \"w\").write(t.replace(old, old + add))")
    lines.append("print(\"fix21 upstream block applied\")")
    lines.append("PYEOF")
    lines.append("")
    return "\n".join(lines) + "\n"


def fix20_block_region(build_text):
    """The fix20 patch block inside build.sh (for per-entry anchoring)."""
    start = build_text.find("# --- fix20:")
    assert start != -1, "PREFLIGHT build.sh: fix20 block marker not found"
    end = build_text.find("# --- Weave program #20:", start)
    assert end != -1, "PREFLIGHT build.sh: weave20 block marker not found"
    return build_text[start:end]


def entry_slice(region, rel, occurrence=0):
    """Slice of one fix20 subs entry (from its rel line to the next entry)."""
    needle = "(%s," % repr(rel)
    idx = -1
    for _ in range(occurrence + 1):
        idx = region.find(needle, idx + 1)
        assert idx != -1, f"PREFLIGHT build.sh: fix20 entry {occurrence} for {rel} not found"
    nxt = region.find("  (", idx + 1)
    return region[idx:nxt if nxt != -1 else len(region)]


def preflight():
    """Check every anchor count==1 before writing anything."""
    # Staged-source anchors.
    grouped = {}
    for path, old, add in STAGED_SUBS:
        grouped.setdefault(path, []).append(old)
    for path, old, new in REPLACEMENTS:
        grouped.setdefault(path, []).append(old)
    for path, olds in grouped.items():
        text = open(path, encoding="utf-8").read()
        for old in olds:
            n = text.count(old)
            assert n == 1, f"PREFLIGHT {path}: anchor count={n}: {old[:70]!r}"
    # Fix19 + fix20 anchors still present verbatim in staged sources (must
    # not have been edited in place by an earlier run).
    taste = open(TASTE, encoding="utf-8").read()
    orch = open(ORCH, encoding="utf-8").read()
    for path, text, rules in ((TASTE, taste, (D19_RULE, F4_RULE, STATIC19,
                                               F4_SCOPE, F5, F6, B1, X1, STATIC20)),
                              (ORCH, orch, (D19_RULE, F4_RULE, STATIC19,
                                             F4_SCOPE, F5, F6, B1, X1, STATIC20))):
        for rule in rules:
            assert text.count(rule) == 1, \
                f"PREFLIGHT {path}: fix19/fix20 anchor missing/changed: {rule[:60]!r}"
    assert open(POLISH, encoding="utf-8").read().count(POLISH_F19) == 1
    assert open(POLISH, encoding="utf-8").read().count(POLISH_F20) == 1
    assert open(TYPESET, encoding="utf-8").read().count(TYPESET_F19) == 1
    assert open(TYPESET, encoding="utf-8").read().count(TYPESET_F20) == 1
    # Orchestrate 5b bullet must still follow the 5a paragraph (STATIC20
    # sits before it).
    assert orch.find(STATIC20) < orch.find("**5b. Final polish**"), \
        "PREFLIGHT orchestrate: STATIC20 must sit before the 5b bullet"
    # No fix21 rule text already present (idempotency guard).
    for path, text in ((TASTE, taste), (ORCH, orch)):
        for rule in (F4_TIGHT, F7, STATIC21):
            assert rule not in text, f"PREFLIGHT {path}: fix21 text already present: {rule[:60]!r}"
    for path in (POLISH, TYPESET):
        text = open(path, encoding="utf-8").read()
        for rule in (POLISH_F21, TYPESET_F21, TYPESET_CHECKBOX21):
            assert rule not in text, f"PREFLIGHT {path}: fix21 text already present: {rule[:60]!r}"
    # Built-tree anchors, per file (never a bare build.sh-wide count).
    uipro = open(os.path.join(BUILT, "skills/ui-ux-pro-max/SKILL.md"), encoding="utf-8").read()
    mvp = open(os.path.join(BUILT, "skills/orch-build-mvp/SKILL.md"), encoding="utf-8").read()
    assert uipro.count(X1_APP) == 1, f"PREFLIGHT built ui-ux-pro-max: X1_APP count={uipro.count(X1_APP)}"
    assert uipro.count(F4_APP) == 1, "PREFLIGHT built ui-ux-pro-max: F4_APP missing"
    assert uipro.count(F4_SCOPE_APP) == 1, "PREFLIGHT built ui-ux-pro-max: F4_SCOPE_APP missing"
    assert mvp.count(X1_APP) == 1, f"PREFLIGHT built orch-build-mvp: X1_APP count={mvp.count(X1_APP)}"
    assert mvp.count(STATIC20) == 1, f"PREFLIGHT built orch-build-mvp: STATIC20 (amended) count={mvp.count(STATIC20)}"
    for text, name in ((uipro, "ui-ux-pro-max"), (mvp, "orch-build-mvp")):
        for rule in (F4_TIGHT_APP, F7_APP, STATIC21):
            assert rule not in text, f"PREFLIGHT built {name}: fix21 text already present: {rule[:60]!r}"
    # build.sh: per-entry anchoring inside the fix20 block. X1_APP occurs
    # twice build.sh-wide (once per patched file) — assert count==1 within
    # EACH file's fix20 entry slice, never the bare total.
    btext = open(BUILD_SH, encoding="utf-8").read()
    region = fix20_block_region(btext)
    assert region.count(X1_APP) == 2, \
        f"PREFLIGHT build.sh fix20 block: expected X1_APP x2, got {region.count(X1_APP)}"
    uipro_entry = entry_slice(region, "skills/ui-ux-pro-max/SKILL.md", 0)
    assert uipro_entry.count(X1_APP) == 1, "PREFLIGHT build.sh: X1_APP not exactly once in the ui-ux-pro-max fix20 entry"
    mvp_entry = entry_slice(region, "skills/orch-build-mvp/SKILL.md", 0)
    assert mvp_entry.count(X1_APP) == 1, "PREFLIGHT build.sh: X1_APP not exactly once in the orch-build-mvp fix20 entry"
    mvp_static_entry = entry_slice(region, "skills/orch-build-mvp/SKILL.md", 1)
    assert mvp_static_entry.count(STATIC20_OLD) == 1, "PREFLIGHT build.sh: OLD STATIC20 not exactly once in the orch-build-mvp fix20 step-6 entry"
    # Amended STATIC20 occurs once build.sh-wide — as the fixup20 block's
    # replacement text, which is what makes the built file hold it.
    assert btext.count(STATIC20) == 1, \
        f"PREFLIGHT build.sh: expected amended STATIC20 x1 (fixup20 block), got {btext.count(STATIC20)}"
    assert btext.count("# STEP 5 — Counts") == 1, "PREFLIGHT build.sh: STEP 5 anchor"
    assert "fix21 upstream block applied" not in btext, "PREFLIGHT build.sh: fix21 block already present"
    assert "fix20 upstream block applied" in btext, "PREFLIGHT build.sh: fix20 block marker missing"
    # No banned terms (fix #16 scrub) in any addition or in the block itself.
    additions = [add for _, _, add in STAGED_SUBS]
    additions += [new for _, _, new in REPLACEMENTS]
    additions += [add for _, _, add in BUILD_SUBS]
    block = build_sh_block()
    for blob in additions + [block]:
        low = blob.lower()
        for term in BANNED:
            assert term not in low, f"PREFLIGHT banned term {term!r} in a fix21 addition"
    print("preflight OK: %d staged anchors + 2 built-tree anchors + "
          "build.sh per-entry anchors (X1_APP x1 per fix20 entry; "
          "OLD STATIC20 x1 in mvp step-6 entry; amended STATIC20 x1 "
          "build.sh-wide) + banned-term scan clean"
          % sum(len(v) for v in grouped.values()))


def self_checks():
    """After the edits: every addition present verbatim, fix19/20 intact."""
    taste = open(TASTE, encoding="utf-8").read()
    orch = open(ORCH, encoding="utf-8").read()
    polish = open(POLISH, encoding="utf-8").read()
    typeset = open(TYPESET, encoding="utf-8").read()
    for text, name, rules in (
            (taste, "Taste", (F4_TIGHT, F7, STATIC21)),
            (orch, "orchestrate", (F4_TIGHT, F7, STATIC21))):
        for rule in rules:
            assert text.count(rule) == 1, f"SELF-CHECK {name}: missing fix21 text: {rule[:60]!r}"
        for rule in (D19_RULE, F4_RULE, STATIC19, F4_SCOPE, F5, F6, B1, X1, STATIC20):
            assert text.count(rule) == 1, f"SELF-CHECK {name}: fix19/fix20 anchor damaged: {rule[:60]!r}"
        assert text.find(STATIC21) > text.find(STATIC20), f"SELF-CHECK {name}: STATIC21 not after STATIC20"
        assert text.find(F4_TIGHT) > text.find(X1), f"SELF-CHECK {name}: F4_TIGHT not after X1"
        assert text.find(F7) > text.find(F4_TIGHT), f"SELF-CHECK {name}: F7 not after F4_TIGHT"
    assert orch.find(STATIC21) < orch.find("**5b. Final polish**"), \
        "SELF-CHECK orchestrate: STATIC21 must sit before the 5b bullet"
    assert polish.count(POLISH_F21) == 1, "SELF-CHECK polish-pass: POLISH_F21 missing"
    assert polish.find(POLISH_F21) > polish.find(POLISH_F20), "SELF-CHECK polish-pass: POLISH_F21 not after POLISH_F20"
    assert polish.count(POLISH_F19) == 1, "SELF-CHECK polish-pass: POLISH_F19 damaged"
    assert polish.count(POLISH_F20) == 1, "SELF-CHECK polish-pass: POLISH_F20 damaged"
    assert typeset.count(TYPESET_F21) == 1, "SELF-CHECK typeset: TYPESET_F21 missing"
    assert typeset.find(TYPESET_F21) > typeset.find(TYPESET_F20), "SELF-CHECK typeset: TYPESET_F21 not after TYPESET_F20"
    assert typeset.count(TYPESET_CHECKBOX21) == 1, "SELF-CHECK typeset: new checkbox missing"
    assert TYPESET_CHECKBOX_FIX20 not in typeset, "SELF-CHECK typeset: fix20 checkbox still present"
    btext = open(BUILD_SH, encoding="utf-8").read()
    assert "fix21 upstream block applied" in btext, "SELF-CHECK build.sh: fix21 block missing"
    assert btext.count("# STEP 5 — Counts") == 1, "SELF-CHECK build.sh: STEP 5 anchor damaged"
    assert btext.find("fix21 upstream block applied") > btext.find("fixup20c upstream block applied"), \
        "SELF-CHECK build.sh: fix21 block must sit after the fixup20c block"
    print("self-checks OK: all fix21 additions present verbatim in staged sources; fix19/fix20 anchors intact")


def main():
    preflight()

    # 1. Staged-source edits (replacements first, then appends).
    for path, old, new in REPLACEMENTS:
        text = open(path, encoding="utf-8").read()
        assert text.count(old) == 1, f"{path}: replacement anchor not found exactly once: {old[:70]!r}"
        open(path, "w", encoding="utf-8").write(text.replace(old, new))
        print(f"{os.path.relpath(path, PLUGIN)}: replacement applied")
    by_path = {}
    for path, old, add in STAGED_SUBS:
        by_path.setdefault(path, []).append((old, add))
    for path, subs in by_path.items():
        text = open(path, encoding="utf-8").read()
        for old, add in subs:
            assert text.count(old) == 1, f"{path}: anchor not found exactly once: {old[:70]!r}"
            text = text.replace(old, old + add)
        open(path, "w", encoding="utf-8").write(text)
        print(f"{os.path.relpath(path, PLUGIN)}: {len(subs)} substitutions applied")

    # 2. Backup build.sh (keep the first pre-fix21 copy).
    backup = os.path.join(PLUGIN, "build.sh.before-fix21")
    if not os.path.exists(backup):
        shutil.copy2(BUILD_SH, backup)
        print("build.sh backup saved to build.sh.before-fix21")
    else:
        print("build.sh.before-fix21 already exists, kept")

    # 3. Append the fix21 block to build.sh before STEP 5.
    btext = open(BUILD_SH, encoding="utf-8").read()
    block = build_sh_block()
    assert btext.count("# STEP 5 — Counts") == 1
    btext = btext.replace("# STEP 5 — Counts", block + "# STEP 5 — Counts", 1)
    open(BUILD_SH, "w", encoding="utf-8").write(btext)
    print(f"build.sh: fix21 block appended ({len(BUILD_SUBS)} upstream subs, "
          f"{len(block.splitlines())} lines)")

    self_checks()


if __name__ == "__main__":
    main()
