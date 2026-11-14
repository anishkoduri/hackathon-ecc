#!/usr/bin/env python3
"""Fix #23 CORE applier (worker W-CORE) — THE CORE, memorability verdict.

Inserts ONE runtime-patch block into build.sh immediately BEFORE the line
`# STEP 5 — Counts`. The block patches browser-qa (upstream; it has no
staged source) in the built tree at build time, following the fix22 block
pattern (fix22/fix22.py, and fix23/apply-s9.py):

  - subs are (id, rel-path, old-anchor, add-text, mode) 5-tuples;
  - the inserted block asserts count==1 per anchor at build time and fails
    loudly on mismatch;
  - modes are 'after' / 'before' / 'replace' (same semantics as fix22).

Preflight (this script, before touching build.sh): every anchor is verified
count==1 against the CURRENT built tree (hackathon-ecc, post-fix23 §9
integration: build.sh 23,984 lines, md5
df7e52f8aa33605c952f58dfea9801fd). Idempotency guard: refuses (exit 1) if
the marker comment is already present in build.sh.

Do NOT run build.sh here — integration runs it. Do NOT run this script
against the built tree — it only edits build.sh. Do NOT run this script
yourself at all — the fix #23 integration worker runs it.

The two subs:

  MEMORABLE-BQA-01  browser-qa/SKILL.md — the memorability verdict, in
    the visual loop, immediately after the hero verdict paragraph
    (HERO-BQA_F23). browser-qa judges memorability as the TOP criterion
    at the finish review — dynamic + over the top + wow / striking /
    stunning — above the F6 impressive bar: a build the user would
    forget the next day FAILS, however rule-correct. It EXTENDS the
    hero verdict ("a merely adequate hero fails F6") and the
    F6/impressive verdicts; it does not duplicate them. "Over the top"
    is ambition and impact, NOT loudness for its own sake — "more, not
    bolder" still governs styling; a build can be over the top and
    quiet in palette; it cannot be forgettable. This verdict is
    browser-qa's alone.
  MEMORABLE-BQA-02  browser-qa/SKILL.md — Output Format, Interactions
    rows: the memorability report row for the QA report, after the
    Dynamic row (DYNAMIC-BQA-02).

§1 CORE vs §4/§6 (no duplication): §4 (HERO-BQA_F23) is the hero
verdict — the hero surface carries the highest weight, a merely
adequate hero fails F6. §6 (BLOCK_F23) is the coverage blocking rule.
CORE (MEMORABLE_F23, this block) is the governing bar ABOVE both:
memorability is the TOP criterion at the finish review, judged across
the enumerated screens with the hero highest-weight, and a
rule-correct but forgettable build fails. Each add-text says so and
cross-references HERO-BQA_F23 / the F6 verdicts instead of restating
them.

ANCHOR NOTE — MEMORABLE-BQA-02 anchors on the Dynamic report row,
which is itself inserted by the fix23 §9 block (DYNAMIC-BQA-02).
That is safe because this block is inserted into build.sh AFTER the
§9 block (both sit before STEP 5, in insertion order), so at build
time the §9 block has already run and the Dynamic row exists. The
preflight below verifies the row is present in the CURRENT built tree
(the §9 integration already rebuilt it there). The other anchor —
the hero verdict's closing sentence — is pre-existing built-tree text
inserted by the W3 block, likewise already present.

Anchors were chosen FRESH against the current built tree and do not
collide with the W2/W3/W4/§9 browser-qa additions: W2's BQA-TYPEAUDIT
sits after the distinctiveness sentence, W3's HERO-BQA_F23 after the
"Never claim visual verification..." sentence and FUNC-BQA_F23 after
Phase 3 step 4, W4's ALIGN_F23-A–E after the Phase 3 heading / step 1 /
step 3 / verdict line / Visual example row, §9's DYNAMIC-BQA-01 after
the Phase 2 step-5 block and DYNAMIC-BQA-02 after the Interactions
auth-flow row (this block anchors on the hero verdict's CLOSING
sentence and on the Dynamic ROW itself — neither string was used as
an anchor by any earlier sub).

Usage: python3 apply-core.py
"""

import os
import sys

PLUGIN = os.path.expanduser("~/workspace/hackathon-plugin")
BUILT = os.path.join(PLUGIN, "hackathon-ecc")
BUILD_SH = os.path.join(PLUGIN, "build.sh")
STEP5 = "# STEP 5 — Counts"
MARKER = "# --- fix23 CORE: memorability verdict (fix #23 §1, MEMORABLE_F23) ---"

BANNED = ("claude", "codex", "anthropic", "opus", "sonnet", "haiku",
          "composer-2.5")

# ---------------------------------------------------------------- subs
# (id, rel-path, old-anchor, add-text, mode). Anchors were verified
# count==1 against the CURRENT built tree by grep preflight before this
# script was written; the preflight below re-verifies them before insert.

SUBS = [
  ('MEMORABLE-BQA-01', 'skills/browser-qa/SKILL.md',
   "This verdict is `browser-qa`'s alone: no other step judges the hero.",
   """

**Memorability verdict — memorable is the bar, above F6 (fix #23 §1, MEMORABLE_F23).** At the finish review, browser-qa judges memorability as the TOP criterion, above the F6 impressive bar: dynamic (it moves and responds), over the top (it goes beyond adequate in ambition, elements, and motion), wow / striking / stunning (it hits on first sight and on use). Judge it across the enumerated screens — the hero surface carries the highest weight (HERO-BQA_F23), but a memorable hero on a forgettable build does not pass. A build the user would forget the next day FAILS, however rule-correct — this extends the hero verdict (a merely adequate hero fails F6) and the F6/impressive verdicts: rule-correct but unambitious, unimpressive, or forgettable all fail. "Over the top" is ambition and impact, not loudness for its own sake: "more, not bolder" still governs styling (do not just crank weight, color, or size) — a build can be over the top and quiet in palette; it cannot be forgettable. This verdict is `browser-qa`'s alone: no other step judges memorability.""",
   'after'),
  ('MEMORABLE-BQA-02', 'skills/browser-qa/SKILL.md',
   '- [✓/✗] Dynamic (DYNAMIC_F23): controls respond immediately; every state change choreographed (motion present); live state, not frozen mock content',
   """
- [✓/✗] Memorability (MEMORABLE_F23): dynamic + over the top + wow / striking / stunning — the build is memorable tomorrow, not merely correct today""",
   'after'),
]


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def fail(msg):
    print(f"apply-core: FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


def render_block(subs):
    """Render the fix22-style runtime-patch block from SUBS."""
    lines = []
    lines.append(MARKER)
    lines.append("# (browser-qa is upstream; it has no staged source and is")
    lines.append("#  patched here. The staged-source halves -- orchestrate")
    lines.append("#  (design-package step: MEMORABLE_F23 elevation of")
    lines.append("#  AMBITION_F23, fix23/orch-lines-core.py) + polish-pass")
    lines.append("#  (memorability-candidates candidate evidence,")
    lines.append("#  fix23/polish-lines-core.py) -- are inserted by the")
    lines.append("#  integration worker from those files, not by this block.")
    lines.append("#  All anchors were verified count==1 against the post-fix23")
    lines.append("#  §9 built tree by apply-core.py's preflight; the asserts")
    lines.append("#  below re-verify at build time and fail the build loudly on")
    lines.append("#  mismatch. browser-qa remains the SOLE executor of pass/fail")
    lines.append("#  verdicts on rendered screens; the orchestrate line states")
    lines.append("#  the bar, polish-pass records candidate evidence, never a")
    lines.append("#  verdict. MEMORABLE-BQA-02 anchors on the Dynamic report")
    lines.append("#  row the §9 block inserts (DYNAMIC-BQA-02): this block sits")
    lines.append("#  AFTER the §9 block in build.sh, so that row exists by the")
    lines.append("#  time this block runs. CORE vs §4/§6: §4 (HERO-BQA_F23) is")
    lines.append("#  the hero verdict, §6 (BLOCK_F23) the coverage blocking")
    lines.append("#  rule; CORE is the governing bar ABOVE both — memorability")
    lines.append("#  is the TOP finish-review criterion. Cross-referenced,")
    lines.append("#  never restated. \"Over the top\" is ambition and impact,")
    lines.append("#  NOT loudness: \"more, not bolder\" governs styling.")
    lines.append("# Placement: before STEP 5 (after the fix23 §9 block).")
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
    lines.append("    assert n == 1, f\"fix23 CORE anchor not found exactly once in {rel}: {old[:70]!r} (count={n})\"")
    lines.append("    if mode == 'after':")
    lines.append("        new = old + add")
    lines.append("    elif mode == 'before':")
    lines.append("        new = add.rstrip('\\n') + '\\n\\n' + old")
    lines.append("    else:  # replace")
    lines.append("        new = add")
    lines.append("    open(p, \"w\").write(t.replace(old, new))")
    lines.append("print(\"fix23 CORE upstream block applied\")")
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
        print(f"apply-core: preflight OK {pid} ({rel}, count==1)")

    block = render_block(SUBS)
    if MARKER not in block:
        fail("rendered block lost its marker comment")
    new = buildsh.replace(STEP5, block + STEP5, 1)
    if new == buildsh:
        fail("insertion produced no change")
    with open(BUILD_SH, "w", encoding="utf-8") as f:
        f.write(new)
    print("apply-core: fix23 CORE block inserted into build.sh before STEP 5")


if __name__ == "__main__":
    main()
