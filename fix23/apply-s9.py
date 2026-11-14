#!/usr/bin/env python3
"""Fix #23 section 9 applier (worker W-§9) — dynamic interface.

Inserts ONE runtime-patch block into build.sh immediately BEFORE the line
`# STEP 5 — Counts`. The block patches three upstream skills (no staged
source) in the built tree at build time, following the fix22 block pattern
(fix22/fix22.py, and fix23/apply-w2.py):

  - subs are (id, rel-path, old-anchor, add-text, mode) 5-tuples;
  - the inserted block asserts count==1 per anchor at build time and fails
    loudly on mismatch;
  - modes are 'after' / 'before' / 'replace' (same semantics as fix22).

Preflight (this script, before touching build.sh): every anchor is verified
count==1 against the CURRENT built tree (hackathon-ecc, post-fix23
§1–§6 integration: build.sh 23,940 lines, md5
536235ac5d34caf473646fd4452ba8a5). Idempotency guard: refuses (exit 1) if
the marker comment is already present in build.sh.

Do NOT run build.sh here — integration runs it. Do NOT run this script
against the built tree — it only edits build.sh. Do NOT run this script
yourself at all — the fix #23 integration worker runs it.

The five subs:

  DYNAMIC-01  motion-foundations/SKILL.md — state changes are
    choreographed, not instant swaps (entering/leaving, loading to
    loaded, empty to filled, selected, confirmed); a state change with
    no motion is a gap.
  DYNAMIC-02  motion-patterns/SKILL.md — interactive depth: patterns
    invite interaction (sortable, filterable, expandable, draggable
    where it serves the job); controls respond immediately; surfaces
    show live state, not frozen mock content.
  DYNAMIC-03  motion-advanced/SKILL.md — advanced pieces are live and
    interactive (drag physics, reorder, counters tweening to live
    values, loading states); a piece that snaps without physics or a
    counter that jumps without tweening is a gap.
  DYNAMIC-BQA-01  browser-qa/SKILL.md — Phase 2, step 6: the LIVE
    dynamic check. browser-qa interacts with the app (click/press/
    hover, sort, filter, expand, drag where the job calls for it),
    confirms controls respond immediately and live state moves, and
    confirms every state change observed is choreographed (motion
    present). A control that does not respond, or a state that changes
    without motion, FAILS the build.
  DYNAMIC-BQA-02  browser-qa/SKILL.md — Output Format, Interactions
    rows: the dynamic report row for the QA report.

§9 vs §2 (no duplication): §2 (MOTION_F23, W1) is the motion-PRESENCE
rule — deliberate, eye-catching motion on every build, routed through
the fix #22 tokens. §9 (DYNAMIC_F23, this block) is the state-change
and interactivity rule — WHAT changes, WHAT triggers it, HOW it moves,
and that controls respond. Each §9 add-text says so and cross-references
MOTION_F23 instead of restating it. §5 (FUNC_F23, W3) is the
functionality-showing rule; §9 notes live data IS the functionality
showing and does not restate it.

Anchors were chosen FRESH against the current built tree and do not
collide with the W1/W2/W3/W4 additions: W1's MOTION-01–03 sit after
`## Rules` in the three motion skills (this block anchors on
`## Decision Guidance` instead); W2's BQA-TYPEAUDIT sits after the
distinctiveness sentence, W3's HERO-BQA_F23 after the "Never claim
visual verification..." sentence and FUNC-BQA_F23 after Phase 3 step 4,
W4's ALIGN_F23-A–E after the Phase 3 heading / step 1 / step 3 /
verdict line / Visual example row (this block anchors on the Phase 2
step-5 block and the Interactions auth-flow row instead).

Usage: python3 apply-s9.py
"""

import os
import sys

PLUGIN = os.path.expanduser("~/workspace/hackathon-plugin")
BUILT = os.path.join(PLUGIN, "hackathon-ecc")
BUILD_SH = os.path.join(PLUGIN, "build.sh")
STEP5 = "# STEP 5 — Counts"
MARKER = "# --- fix23 §9: dynamic interface (DYNAMIC_F23) ---"

BANNED = ("claude", "codex", "anthropic", "opus", "sonnet", "haiku",
          "composer-2.5")

# ---------------------------------------------------------------- subs
# (id, rel-path, old-anchor, add-text, mode). Anchors were verified
# count==1 against the CURRENT built tree by grep preflight before this
# script was written; the preflight below re-verifies them before insert.

SUBS = [
  ('DYNAMIC-01', 'skills/motion-foundations/SKILL.md',
   '## Decision Guidance',
   """

**State changes are choreographed, not instant swaps (fix #23 §9, DYNAMIC_F23).** Every state change on a build is a choreographed transition, routed through the fix #22 motion tokens (Group A principles + Group B values) and, where the change is a moment, a dealt moment: entering/leaving, loading to loaded, empty to filled, selected, confirmed. A state change with no motion is a gap — the interface must never snap between states with nothing in between. Each state change is recorded in `docs/design-tokens.md`'s Motion list with its trigger, its token values, and its D19 reason (Motion dimension), directed per §10 (direct, don't describe). This is the state-change rule; §2 (MOTION_F23) is the motion-presence rule — deliberate motion on every build — and this section says how each change moves, it does not restate it. `prefers-reduced-motion` is respected everywhere: the state still changes and the content is correct at rest — opacity-only fades at ≤ 0.2s or no motion — with a complete static fallback, never a broken state. (D19 — Motion: each state change IS a motion decision — trigger + tokens recorded; Theme: changes move in the dealt theme's motion voice; Texture: none — state changes carry no surface treatment; Visuals: choreographed changes are what make the interface read as alive rather than frozen; Techniques: values come from `motionTokens` and the Group B rules, never hardcoded; Colors: none — state changes choose no colours; Depth: a change that reorders layers names the layer order, or `flat by choice — <reason>`.)""",
   'after'),
  ('DYNAMIC-02', 'skills/motion-patterns/SKILL.md',
   '## Decision Guidance',
   """

**Interactive depth — the interface invites interaction (fix #23 §9, DYNAMIC_F23).** Patterns are chosen so the user can DO things, not just look: sortable, filterable, expandable, draggable where it serves the job (Accordion, Expanding card, Dropdown, Modal, Popover, Toast stack, Page transition — each with its live behaviour, not a static mock). Every interactive pattern responds immediately: press states (press scale 0.97), hover, transitions — and every state change it drives is choreographed (AnimatePresence enter/exit, `layout` for size/position changes, stagger for lists), with its trigger and token values recorded in `docs/design-tokens.md`'s Motion list. A control that looks interactive but does nothing on press is a gap; a surface showing frozen mock content — counts and totals that never move — is a gap: surfaces show live state (data updating, statuses changing, counts and totals moving). A state change with no motion is a gap. `prefers-reduced-motion` is respected in every pattern with a complete static fallback — the state still changes, content visible at rest — never a broken one. (D19 — Motion: each interactive pattern IS a motion decision — trigger + tokens recorded; Theme: patterns move in the dealt theme's motion voice; Texture: none — patterns carry no surface treatment; Visuals: live patterns are what make the build read as alive; Techniques: values come from `motion-foundations` tokens, never inline numbers (Rule 8); Colors: none — patterns choose no colours; Depth: a pattern that reorders layers names the layer order, or `flat by choice — <reason>`.)""",
   'after'),
  ('DYNAMIC-03', 'skills/motion-advanced/SKILL.md',
   '## Decision Guidance',
   """

**Advanced pieces are live and interactive (fix #23 §9, DYNAMIC_F23).** Every advanced piece on a build must actually respond and move in the rendered page: drags with physics on release, reorderable lists, drag-to-dismiss, swipe detection, long-press, counters tweening to live values, SVG draws, mask reveals, shimmer skeletons and button loading states — routed through the fix #22 motion tokens (Group A principles + Group B values) and recorded in `docs/design-tokens.md`'s Motion list with trigger and token values, plus its D19 reason (Motion dimension), directed per §10 (direct, don't describe). A draggable that snaps without physics, a counter that jumps to its value without tweening, or a loading state that flips to loaded with no transition is a gap — a state change with no motion is a gap, and a control that does not respond is a gap. `prefers-reduced-motion` is respected everywhere with a complete static fallback — the piece renders at its final state, content visible at rest — never a broken one. (D19 — Motion: each advanced piece IS a motion decision — trigger + tokens recorded; Theme: choreography moves in the dealt theme's motion voice; Texture: none — choreography carries no surface treatment; Visuals: moving pieces are what make the build read as alive; Techniques: values come from `motion-foundations` tokens, never inline numbers (Rule 6); Colors: none — choreography chooses no colours; Depth: a piece that reorders layers names the layer order, or `flat by choice — <reason>`.)""",
   'after'),
  ('DYNAMIC-BQA-01', 'skills/browser-qa/SKILL.md',
   """5. Test critical user journeys (checkout, onboarding, search)
   — read-only by default; only exercise mutating journeys against staging
     with explicit opt-in (see "Safety first" above)""",
   """
6. Dynamic-interface live check (fix #23 §9, DYNAMIC_F23): interact with the app like a user — click/press/hover every interactive control, and sort, filter, expand, and drag where the job calls for it — and confirm the interface responds immediately (press state, hover, transition visible) and that live state moves (data updating, statuses changing, counts and totals moving) rather than frozen mock content. Read the dynamic story from `docs/design-tokens.md` / the decision record (per surface: what changes, what triggers it, how it moves) and confirm each state change observed is choreographed (motion present — entering/leaving, loading to loaded, empty to filled, selected, confirmed). A control that does not respond, or a state that changes without motion, FAILS the build. Read-only by default; only exercise mutating journeys against staging with explicit opt-in (see "Safety first" above).""",
   'after'),
  ('DYNAMIC-BQA-02', 'skills/browser-qa/SKILL.md',
   '- [✓] Auth flow: login/logout working',
   """
- [✓/✗] Dynamic (DYNAMIC_F23): controls respond immediately; every state change choreographed (motion present); live state, not frozen mock content""",
   'after'),
]


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def fail(msg):
    print(f"apply-s9: FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


def render_block(subs):
    """Render the fix22-style runtime-patch block from SUBS."""
    lines = []
    lines.append(MARKER)
    lines.append("# (motion-foundations / motion-patterns / motion-advanced /")
    lines.append("#  browser-qa are upstream; they have no staged source and are")
    lines.append("#  patched here. The staged-source halves -- orchestrate")
    lines.append("#  (design-package step: DYNAMIC_F23, fix23/orch-lines-s9.py)")
    lines.append("#  + polish-pass (dynamic-story candidate evidence,")
    lines.append("#  fix23/polish-lines-s9.py) -- are inserted by the integration")
    lines.append("#  worker from those files, not by this block.")
    lines.append("#  All anchors were verified count==1 against the post-fix23")
    lines.append("#  §1–§6 built tree by apply-s9.py's preflight; the asserts")
    lines.append("#  below re-verify at build time and fail the build loudly on")
    lines.append("#  mismatch. browser-qa remains the SOLE executor of pass/fail")
    lines.append("#  verdicts on rendered screens; the motion skills state the")
    lines.append("#  rule, polish-pass records candidate evidence, never a verdict.")
    lines.append("#  §9 vs §2: §2 (MOTION_F23) is motion presence on every build;")
    lines.append("#  §9 (DYNAMIC_F23) is state changes + interactivity — what")
    lines.append("#  changes, what triggers it, how it moves. Cross-referenced,")
    lines.append("#  never restated.")
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
    lines.append("    assert n == 1, f\"fix23 §9 anchor not found exactly once in {rel}: {old[:70]!r} (count={n})\"")
    lines.append("    if mode == 'after':")
    lines.append("        new = old + add")
    lines.append("    elif mode == 'before':")
    lines.append("        new = add.rstrip('\\n') + '\\n\\n' + old")
    lines.append("    else:  # replace")
    lines.append("        new = add")
    lines.append("    open(p, \"w\").write(t.replace(old, new))")
    lines.append("print(\"fix23 section 9 upstream block applied\")")
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
        print(f"apply-s9: preflight OK {pid} ({rel}, count==1)")

    block = render_block(SUBS)
    if MARKER not in block:
        fail("rendered block lost its marker comment")
    new = buildsh.replace(STEP5, block + STEP5, 1)
    if new == buildsh:
        fail("insertion produced no change")
    with open(BUILD_SH, "w", encoding="utf-8") as f:
        f.write(new)
    print("apply-s9: fix23 section 9 block inserted into build.sh before STEP 5")


if __name__ == "__main__":
    main()
