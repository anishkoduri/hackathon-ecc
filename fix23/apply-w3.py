#!/usr/bin/env python3
"""Fix #23 §4/§5 applier (worker W3) — hero + functionality, upstream half.

Inserts ONE runtime-patch block into build.sh immediately BEFORE the line
`# STEP 5 — Counts`, following the fix22 block pattern (fix22/fix22.py):
the block patches the BUILT tree at build time, after STEP 2 assembles it
and after the fix22 block runs. ui-ux-pro-max and browser-qa are
upstream/ECC with no staged source, so they are patched here, never by
editing the built tree.

Subs (id, built-tree rel path, old anchor, add text, mode, token):
  FUNC-UIPRO_F23  ui-ux-pro-max functionality pointer (after the Element
                  variety paragraph — the design-element rule that names
                  diagrams as an element kind).
  HERO-BQA_F23    browser-qa hero verdict (after the visual-iteration-loop
                  paragraph — the sole-verdict loop).
  FUNC-BQA_F23    browser-qa functionality verdict (after Phase 3 step 4,
                  as Phase 3 step 5 inside the Visual Regression fence).

Every anchor was verified count==1 against the CURRENT built tree
(build.sh md5 4799a819791b9c3ec4c19136ad698397) before this script was
written; the preflight below re-verifies (in-memory simulation, in list
order) and fails loudly on any mismatch. A silently dropped patch is the
worst outcome, so failures are loud: the patch id + anchor + count are
printed and the script exits 1.

Usage: python3 apply-w3.py            # dry-run: preflight only, writes nothing
       python3 apply-w3.py --apply    # preflight + insert the block into build.sh

Do NOT run build.sh from here (integration runs it later). Do NOT run
fix11/fix11-stage.py. Do NOT touch /demo wiring or DEMOGATE tokens.
"""
import ast
import os
import re
import sys

HOME = os.path.expanduser("~")
PLUGIN = os.path.join(HOME, "workspace/hackathon-plugin")
BUILT = os.path.join(PLUGIN, "hackathon-ecc")
BUILD_SH = os.path.join(PLUGIN, "build.sh")

BANNED = ("claude", "codex", "anthropic", "opus", "sonnet", "haiku",
          "composer-2.5")
MARKER = "fix23-W3 upstream block applied"
STEP5 = "# STEP 5 — Counts"
APPLY = "--apply" in sys.argv

UIPRO = "skills/ui-ux-pro-max/SKILL.md"
BQA = "skills/browser-qa/SKILL.md"

# --- patch table: (id, rel, old, new, mode, token) ---
# mode: 'after' (old -> old+new), 'before' (old -> new+old), 'replace'.
# token: a distinctive string of the new text that must be ABSENT from the
# original built file (idempotency / already-applied guard).

SUBS = [
    ("FUNC-UIPRO_F23", UIPRO,
     "Every element application is recorded per surface in "
     "`docs/design-tokens.md` (surface \u2192 elements applied, kind, "
     "theme-fit).",
     "\n\n**Functionality pointer \u2014 show how it works (fix #23 \u00a75, "
     "FUNC-UIPRO_F23).** App and dashboard surfaces show their mechanism, "
     "not just their chrome: the pipeline, the live data, the stack, the "
     "live system state \u2014 as a first-class surface, theme-matched, "
     "visible early (on the home/feed surface or the first screen after "
     "it). The full rule lives in `design-taste-frontend` step 4a "
     "(FUNC_F23) and its diagram form in "
     "`design-taste-frontend/references/diagrams.md` (FUNC-DIAG_F23): the "
     "mechanism shown must be THIS build's mechanism \u2014 its pipeline, "
     "its data, its stack \u2014 with the product's own names and real "
     "figures; a generic diagram relabelled with generic words does not "
     "satisfy it. The decision record states the functionality story: "
     "what is technically new here, and how the design shows it. A build "
     "that looks good but hides what the thing does fails. (D19 \u2014 "
     "Motion: the mechanism moves where it is live or records "
     "`none \u2014 <reason>` where still; Theme: drawn in the theme's own "
     "lines and tokens; Texture: the theme's treatment or "
     "`none \u2014 <reason>`; Visuals: the mechanism is the section's "
     "picture; Techniques: routes through `diagrams.md` or the live-data "
     "surface; Colors: the theme's ink and one signal; Depth: layer order "
     "named or `flat by choice \u2014 <reason>`.)",
     "after", "FUNC-UIPRO_F23"),
    ("HERO-BQA_F23", BQA,
     "Never claim visual verification without actually inspecting the "
     "rendered interface.",
     "\n\n**Hero verdict \u2014 amazing is the bar (fix #23 \u00a74, "
     "HERO-BQA_F23).** In the visual loop, the hero surface \u2014 a landing "
     "hero, or the home/feed surface of an app \u2014 carries the highest "
     "weight: judge it against the hero-moment line recorded in "
     "`docs/design-tokens.md` and the Picks block's Hero-moment row (a "
     "dealt moment + a distinctive composition + motion). A merely "
     "adequate hero \u2014 correct but unremarkable \u2014 FAILS F6, however "
     "correct the rest of the screens are. Calibration: on a phone-first "
     "utility app the home/feed surface IS the hero surface; the amazing "
     "bar is calibrated to the product's job, not to decoration \u2014 the "
     "moment must serve what the user opens the app to do. \"Amazing\" "
     "never means a generic hero section pasted onto an app that does not "
     "need one. This verdict is `browser-qa`'s alone: no other step judges "
     "the hero.",
     "after", "HERO-BQA_F23"),
    ("FUNC-BQA_F23", BQA,
     "4. Check dark mode if applicable",
     "\n5. Functionality check (fix #23 \u00a75, FUNC-BQA_F23): the build "
     "shows HOW it works early \u2014 its mechanism (diagram / live data / "
     "system state) is visible on the hero surface or the first screen "
     "after it, theme-matched, naming THIS build's pipeline, data, and "
     "stack with the product's own names and real figures. A build that "
     "looks good but hides what the thing does FAILS, even with zero "
     "layout findings. A generic diagram relabelled with generic words "
     "does not pass.",
     "after", "FUNC-BQA_F23"),
]


def build_sh_block():
    """The fix23-W3 patch block inserted into build.sh (before STEP 5)."""
    lines = []
    lines.append("# --- fix23-W3: hero amazing + functionality verdicts (fix #23 SS4/SS5) ---")
    lines.append("# (ui-ux-pro-max and browser-qa are upstream/ECC; they have no staged")
    lines.append("#  source and are patched here. The staged-source halves -- Taste")
    lines.append("#  SKILL.md (HERO_F23 / FUNC_F23 + fix #23 static checks + checklist),")
    lines.append("#  Taste diagrams.md (FUNC-DIAG_F23), Hallmark review-hero.md")
    lines.append("#  (Hero-moment row) -- were applied directly to their staged sources")
    lines.append("#  by worker W3. The orchestrate lines live in fix23/orch-lines-w3.py")
    lines.append("#  for the integration worker to insert mechanically.)")
    lines.append("#  All anchors were verified count==1 against the post-fix22 built tree")
    lines.append("#  by apply-w3.py's preflight (in-memory simulation, in list order);")
    lines.append("#  the asserts below re-verify at build time and fail the build loudly")
    lines.append("#  on mismatch. browser-qa remains the SOLE executor of pass/fail")
    lines.append("#  verdicts on rendered screens; the static halves are candidate")
    lines.append("#  evidence / completeness checks only, never verdicts.")
    lines.append("# Placement: before STEP 5 (after the fix22 block).")
    lines.append("python3 - \"$PLUGIN_DIR\" <<'PYEOF'")
    lines.append("import os, sys")
    lines.append("base = sys.argv[1]")
    lines.append("")
    lines.append("subs = [")
    for pid, rel, old, new, mode, _token in SUBS:
        lines.append("  (%s, %s, %s, %s, %s),  # %s" % (
            repr(pid), repr(rel), repr(old), repr(new), repr(mode), repr(pid)))
    lines.append("]")
    lines.append("for pid, rel, old, add, mode in subs:")
    lines.append("    p = os.path.join(base, rel)")
    lines.append("    t = open(p).read()")
    lines.append("    n = t.count(old)")
    lines.append("    assert n == 1, f\"fix23-W3 anchor not found exactly once in {rel}: {old[:70]!r} (count={n})\"")
    lines.append("    if mode == 'after':")
    lines.append("        new = old + add")
    lines.append("    elif mode == 'before':")
    lines.append("        new = add.rstrip('\\n') + '\\n\\n' + old")
    lines.append("    else:  # replace")
    lines.append("        new = add")
    lines.append("    open(p, \"w\").write(t.replace(old, new))")
    lines.append("print(\"%s\")" % MARKER)
    lines.append("PYEOF")
    lines.append("")
    return "\n".join(lines) + "\n"


def _apply_patch(text, old, new, mode):
    if mode == "after":
        return text.replace(old, old + new)
    if mode == "before":
        return text.replace(old, new.rstrip("\n") + "\n\n" + old)
    return text.replace(old, new)  # replace


def preflight():
    """Check every anchor count==1 (in-memory simulation, in list order)
    before writing anything. FAIL LOUDLY on any mismatch."""
    originals = {}
    sim = {}
    for _pid, rel, _old, _new, _mode, _token in SUBS:
        if rel not in originals:
            path = os.path.join(BUILT, rel)
            originals[rel] = open(path, encoding="utf-8").read()
            sim[rel] = originals[rel]
    failures = []
    for pid, rel, old, new, mode, token in SUBS:
        # Idempotency guard: the new text must not already be in the file.
        if token in originals[rel]:
            failures.append((pid, rel, "TOKEN-ALREADY-PRESENT", token))
            continue
        if '"""' in new:
            failures.append((pid, rel, "TRIPLE-QUOTE-IN-NEW-TEXT", ""))
            continue
        n = sim[rel].count(old)
        if n != 1:
            failures.append((pid, rel, "ANCHOR-COUNT=%d" % n, old[:100]))
            continue
        sim[rel] = _apply_patch(sim[rel], old, new, mode)
    # build.sh anchors.
    btext = open(BUILD_SH, encoding="utf-8").read()
    if btext.count(STEP5) != 1:
        failures.append(("BUILD-SH", "build.sh", "STEP-5-ANCHOR",
                         STEP5))
    if MARKER in btext:
        failures.append(("BUILD-SH", "build.sh", "BLOCK-ALREADY-PRESENT",
                         MARKER))
    if "fix22 upstream block applied" not in btext:
        failures.append(("BUILD-SH", "build.sh", "FIX22-BLOCK-MISSING",
                         "fix22 upstream block applied"))
    # Banned-term scan over every addition and the generated block.
    block = build_sh_block()
    # Block-structure validation: the generated subs tuples must each have
    # exactly 5 elements (pid, rel, old, new, mode) with a valid mode, or
    # the build-time unpack fails.
    _m = re.search(r"subs = \[(.*?)\n\]", block, re.S)
    assert _m, "PREFLIGHT: subs list not found in generated block"
    _subs = ast.literal_eval("[" + _m.group(1) + "\n]")
    assert len(_subs) == len(SUBS), \
        "PREFLIGHT: generated subs count %d != SUBS %d" % (len(_subs), len(SUBS))
    for _t in _subs:
        assert len(_t) == 5 and _t[4] in ("after", "before", "replace"), \
            "PREFLIGHT: malformed subs tuple: %r" % (_t[:1],)
    compile(block, "fix23-W3-block", "exec")
    for pid, _rel, _old, new, _mode, _token in SUBS:
        low = new.lower()
        for term in BANNED:
            if term in low:
                failures.append((pid, "addition", "BANNED-TERM=%s" % term,
                                 new[:80]))
    for term in BANNED:
        if term in block.lower():
            failures.append(("BLOCK", "build.sh block", "BANNED-TERM=%s" % term,
                             term))
    if failures:
        print("PREFLIGHT FAILED \u2014 %d problem(s), nothing written:" % len(failures))
        for pid, rel, kind, detail in failures:
            print("  FAILED %s in %s: %s: %r" % (pid, rel, kind, detail))
        sys.exit(1)
    print("preflight OK: %d subs, all anchors count==1, all tokens absent, "
          "banned-term scan clean" % len(SUBS))


def self_checks():
    btext = open(BUILD_SH, encoding="utf-8").read()
    assert MARKER in btext, \
        "SELF-CHECK build.sh: fix23-W3 block missing"
    assert btext.count(STEP5) == 1, \
        "SELF-CHECK build.sh: STEP 5 anchor damaged"
    assert btext.find(MARKER) > btext.find(
        "fix22 upstream block applied"), \
        "SELF-CHECK build.sh: fix23-W3 block must sit after the fix22 block"
    for _pid, _rel, _old, _new, _mode, token in SUBS:
        assert token in btext, \
            "SELF-CHECK build.sh: sub %s token missing from block: %r" % (_pid, token)
    print("self-checks OK: fix23-W3 block present in build.sh; "
          "all %d sub tokens present in the block" % len(SUBS))


def main():
    preflight()
    if not APPLY:
        print("dry-run only (no files written). Re-run with --apply.")
        return
    btext = open(BUILD_SH, encoding="utf-8").read()
    block = build_sh_block()
    assert btext.count(STEP5) == 1
    assert MARKER not in btext
    btext = btext.replace(STEP5, block + STEP5, 1)
    open(BUILD_SH, "w", encoding="utf-8").write(btext)
    print("build.sh: fix23-W3 block inserted (%d upstream subs, %d lines)"
          % (len(SUBS), len(block.splitlines())))
    self_checks()
    for pid, _r, _o, _n, _m, _t in SUBS:
        print("APPLIED %s" % pid)


if __name__ == "__main__":
    main()
