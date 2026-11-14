#!/usr/bin/env python3
"""Fix #23 section 3 applier (worker W2) — fonts, no defaulting.

Inserts ONE runtime-patch block into build.sh immediately BEFORE the line
`# STEP 5 — Counts`. The block patches three upstream skills (no staged
source) in the built tree at build time, following the fix22 block pattern:

  - subs are (id, rel-path, old-anchor, add-text, mode) 5-tuples;
  - the inserted block asserts count==1 per anchor at build time and fails
    loudly on mismatch;
  - modes are 'after' / 'before' / 'replace' (same semantics as fix22).

Preflight (this script, before touching build.sh): every anchor is verified
count==1 against the CURRENT built tree (hackathon-ecc). Idempotency guard:
refuses (exit 1) if the marker comment is already present in build.sh.

Do NOT run build.sh here — integration runs it. Do NOT run this script
against the built tree — it only edits build.sh.

The three subs:

  BQA-TYPEAUDIT  browser-qa/SKILL.md — type-audit verdict lines: a build
    whose typography reads as defaulted (body face dominating, display
    faces doing too little visible work, trio reused with no recorded
    reason, variety floor missed) FAILS at browser-qa.
  UIPRO-F7VAR    ui-ux-pro-max/SKILL.md — F7 strengthened: every text
    element gets a distinctive artistic font decision AND the decision
    record must show VARIETY across the build; the trio is a pattern,
    not a default.
  ORCH-TYPEAUDIT orch-build-mvp/SKILL.md — extends the fix #19/#20/#21
    static checks with the fix #23 type-audit record checks. The fix #21
    text is NOT rewritten (extension paragraph only, the fix22 section 13
    DEPTH-12 precedent); no frozen D19 text is touched.

Thresholds (defined in polish-pass reference/lenses/typeset.md,
TYPEAUDIT_F23 — the full home of the rule):
  T1a body face <= 40% of build visual share (roll-up);
  T1b body face <= 55% on any single primary screen;
  T1c display/important faces combined >= 25% of build visual share;
  T1d on the hero/home surface, display share > body share;
  T2  trio identical to the previous build's trio with no recorded reuse
      reason -> FAIL;
  T3  distinct faces >= max(3, ceil(N/20)) for N Type-list text elements,
      each counted face >= 5% visual share.
Visual share = SUM(size in px x visible characters) per face / total.
Justification: Home Run (Nov 12, 2026) — all 5 static faces loaded, real
display face dealt, yet Fraunces (the body face) carried the whole page by
volume because in an app most visible text IS body text.

Usage: python3 apply-w2.py
"""

import os
import sys

PLUGIN = os.path.expanduser("~/workspace/hackathon-plugin")
BUILT = os.path.join(PLUGIN, "hackathon-ecc")
BUILD_SH = os.path.join(PLUGIN, "build.sh")
STEP5 = "# STEP 5 — Counts"
MARKER = "# --- fix23 \u00a73: type audit \u2014 fonts, no defaulting (TYPEAUDIT_F23) ---"

BANNED = ("claude", "codex", "anthropic", "opus", "sonnet", "haiku",
          "composer-2.5")

# ---------------------------------------------------------------- subs
# (id, rel-path, old-anchor, add-text, mode). Anchors were verified
# count==1 against the CURRENT built tree by grep preflight before this
# script was written; the preflight below re-verifies them before insert.

SUBS = [
  ('BQA-TYPEAUDIT', 'skills/browser-qa/SKILL.md',
   """a screen with no named direction, no applied theme/tokens, reading as a default template, or derivative (the design is based on a searched external reference) FAILS \u2014 report it as a distinctiveness finding (minor at least) with the top-5 list, so the caller routes it to the fix loop within the existing caps.""",
   """

**Type-audit verdict (fix #23 \u00a73, TYPEAUDIT_F23).** Typography that reads as defaulted fails here, on the rendered screen: before rendering a verdict in any round, read the type-audit table from `.hallmark/candidate-evidence.md` (per-face visual shares, trio-vs-previous-build comparison, variety count \u2014 recorded by `polish-pass`, TYPEAUDIT_F23) alongside the other candidate evidence. A type-audit FAIL \u2014 the body face over 40% of the build's visual share (or over 55% on any primary screen), the display face(s) under 25% of the build's visual share, the display face losing to the body face on the hero/home surface, the trio identical to the previous build's trio with no recorded reuse reason, or fewer distinct faces than the variety floor (max(3, ceil(N/20)) for N Type-list text elements, each counted face at least 5% share) \u2014 is a distinctiveness finding (minor at least) that FAILS the build, routed back to the design skill for a re-deal of the trio or a re-balance of the shares. A hit cleared in the decision record by its recorded reason (trio reuse) or scoped exception (body-led build, display floor still binding) is not a FAIL \u2014 the clearance is cited in the verdict, never assumed. Only this skill renders the type-audit verdict; `polish-pass` records the evidence, never the verdict.""",
   'after'),
  ('UIPRO-F7VAR', 'skills/ui-ux-pro-max/SKILL.md',
   """No element defaults to the body face without a decision; main visible text uses the display face (fix #20 F5) or another artistic face chosen through the skills. The full F7 rule lives in `design-taste-frontend` step 4a.""",
   """

**F7 strengthened \u2014 the decision record must show VARIETY across the build (fix #23 \u00a73, F7VAR_F23).** One artistic decision per text element is the floor, not the bar: the decisions together must show variety. The trio "one display face + body stand-in + mono" is a pattern, not a default \u2014 the trio itself is re-chosen per build (Hallmark already deals type; the pairing is re-dealt, not inherited from the previous build), and a build that reuses the previous build's trio without a recorded reason fails (see the type-audit trio check, TYPEAUDIT_F23). Distinct faces number at least max(3, ceil(N/20)) for N Type-list text elements, each counted face carrying at least 5% of the build's visual share \u2014 a face that appears on one label is not variety. The display face must do the visible work: the display/important faces together carry at least 25% of the build's visual share, and on the hero/home surface the display face's share exceeds the body face's. A decision record in which every element's decision names the same face for different jobs, or in which the display face appears only on H1s, has not met F7. The full F7 variety rule and the type-audit thresholds live in `polish-pass` (reference/lenses/typeset.md, TYPEAUDIT_F23); this skill states the variety requirement, `polish-pass` measures it, `browser-qa` alone verdicts it.""",
   'after'),
  ('ORCH-TYPEAUDIT', 'skills/orch-build-mvp/SKILL.md',
   """a blanket 'all text' class line is not a class decision. (F7 record) The decision record lists the font decision per text element or per uniform class; the D19 reason covers the font choice.""",
   """

**Fix #23 static checks \u2014 type audit (TYPEAUDIT_F23, all static checks, never screen verdicts).** The Type list carries the type-audit table (face | roles | visual share % | element count, per primary screen + build roll-up, visual share = \u03a3 size \u00d7 visible characters per face \u00f7 total) and the trio-vs-previous-build line (this build's trio, the previous build's recorded trio, match? + reuse reason if matched; a first build records `previous trio: none (first build)`); a Type list with no type-audit table or no trio line is an incomplete build. (T1 record) The record states the body-face share (\u2264 40% roll-up, \u2264 55% per screen), the display-face share (\u2265 25% roll-up), and the hero-surface comparison (display > body); a missing share is an incomplete build \u2014 the numbers themselves are judged by `browser-qa`, never here. (T2 record) The trio line states whether the trio matches the previous build's; a match with no recorded reuse reason is an incomplete build. (T3 record) The record states the distinct-face count against the variety floor (max(3, ceil(N/20)) for N Type-list text elements, each counted face \u2265 5% share); a count below the floor is an incomplete build. (T1/T2/T3 verdict) Whether a recorded share, trio, or count FAILS the build is `browser-qa`'s verdict on the rendered screen alone \u2014 this check records the numbers, never the verdict. The fix #21 text above is unchanged; this paragraph extends it.""",
   'after'),
]


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def fail(msg):
    print(f"apply-w2: FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


def render_block(subs):
    """Render the fix22-style runtime-patch block from SUBS."""
    lines = []
    lines.append(MARKER)
    lines.append("# (browser-qa / ui-ux-pro-max / orch-build-mvp are upstream; they have no")
    lines.append("#  staged source and are patched here. The staged-source half --")
    lines.append("#  polish-pass (SKILL.md harmony + non-negotiable 5, typeset lens,")
    lines.append("#  slop checklist) -- was applied directly to its sources by worker W2.")
    lines.append("#  All anchors were verified count==1 against the post-fix22 built tree")
    lines.append("#  by apply-w2.py's preflight; the asserts below re-verify at build time")
    lines.append("#  and fail the build loudly on mismatch. The fix #21 static-checks text")
    lines.append("#  is NOT rewritten: the orch-build-mvp sub appends an extension paragraph")
    lines.append("#  only (fix22 section 13 DEPTH-12 precedent).)")
    lines.append("# Placement: before STEP 5 (after the fix22 block).")
    lines.append("python3 - \"$PLUGIN_DIR\" <<'PYEOF'")
    lines.append("import os, sys")
    lines.append("base = sys.argv[1]")
    lines.append("")
    lines.append("subs = [")
    for pid, rel, old, add, mode in subs:
        lines.append(f"  ({pid!r}, {rel!r}, {old!r}, {add!r}, {mode!r}),  # {pid!r}")
    lines.append("]")
    lines.append("for pid, rel, old, add, mode in subs:")
    lines.append("    p = os.path.join(base, rel)")
    lines.append("    t = open(p).read()")
    lines.append("    n = t.count(old)")
    lines.append("    assert n == 1, f\"fix23 anchor not found exactly once in {rel}: {old[:70]!r} (count={n})\"")
    lines.append("    if mode == 'after':")
    lines.append("        new = old + add")
    lines.append("    elif mode == 'before':")
    lines.append("        new = add.rstrip('\\n') + '\\n\\n' + old")
    lines.append("    else:  # replace")
    lines.append("        new = add")
    lines.append("    open(p, \"w\").write(t.replace(old, new))")
    lines.append("print(\"fix23 section 3 upstream block applied\")")
    lines.append("PYEOF")
    lines.append("")
    return "\n".join(lines)


def main():
    # Idempotency guard: refuse if the marker comment is already present.
    buildsh = read(BUILD_SH)
    if MARKER in buildsh:
        fail("marker comment already present in build.sh — refusing to insert twice")
    if buildsh.count(STEP5) != 1:
        fail(f"{STEP5!r} must occur exactly once in build.sh "
             f"(count={buildsh.count(STEP5)})")

    # Preflight: every anchor resolves count==1 against the CURRENT built
    # tree, and no new text carries a banned term.
    for pid, rel, old, add, mode in SUBS:
        if mode not in ("after", "before", "replace"):
            fail(f"{pid}: unknown mode {mode!r}")
        p = os.path.join(BUILT, rel)
        if not os.path.exists(p):
            fail(f"{pid}: target file missing from built tree: {rel}")
        t = read(p)
        n = t.count(old)
        if n != 1:
            fail(f"{pid}: anchor not found exactly once in {rel} "
                 f"(count={n}): {old[:70]!r}")
        low = add.lower()
        for term in BANNED:
            if term in low:
                fail(f"{pid}: add-text carries banned term {term!r}")
        print(f"apply-w2: preflight OK {pid} ({rel}, count==1)")

    block = render_block(SUBS)
    if MARKER not in block:
        fail("rendered block lost its marker comment")
    new = buildsh.replace(STEP5, block + STEP5, 1)
    if new == buildsh:
        fail("insertion produced no change")
    with open(BUILD_SH, "w", encoding="utf-8") as f:
        f.write(new)
    print("apply-w2: fix23 section 3 block inserted into build.sh before STEP 5")


if __name__ == "__main__":
    main()
