#!/usr/bin/env python3
"""Fix #23 W1 applier (worker W1 tool).

Inserts ONE runtime-patch block into build.sh immediately BEFORE the line
`# STEP 5 — Counts`. The block patches the upstream/ECC motion skills
(motion-foundations, motion-patterns, motion-advanced,
make-interfaces-feel-better, ui-ux-pro-max) at build time — those skills
have no staged source, so they are never edited in the built tree directly.

DO NOT RUN THIS SCRIPT YOURSELF — the fix #23 integration worker runs it.
Running it twice is refused by the idempotency guard (the block's marker
comment must be absent from build.sh).

Usage: python3 apply-w1.py

Anchors were verified count==1 against the CURRENT (post-fix22) built tree
with greps before this script was written; the block's own asserts
re-verify at build time and fail the build loudly on mismatch.
"""

import os
import sys

PLUGIN = os.path.expanduser("~/workspace/hackathon-plugin")
BUILD_SH = os.path.join(PLUGIN, "build.sh")
MARKER = "# --- fix23 W1: motion default (fix #23 §2, MOTION_F23) ---"
STEP5 = "# STEP 5 — Counts"

BLOCK = r'''# --- fix23 W1: motion default (fix #23 §2, MOTION_F23) ---
# (motion-foundations / motion-patterns / motion-advanced /
#  make-interfaces-feel-better / ui-ux-pro-max are upstream/ECC; they have
#  no staged source and are patched here. The staged-source half --
#  orchestrate (design-package step: AMBITION_F23 / INVENTORY_F23 /
#  MOTION_F23) + the inventory file
#  (new-skills/orchestrate/references/design-inventory.md) + the
#  design-lead dispatch prompt (dispatch-prompt.md §5a) -- was applied
#  directly to its staged sources by the W1 worker. All anchors were
#  verified count==1 against the post-fix22 built tree by greps before
#  this script was written; the asserts below re-verify at build time
#  and fail the build loudly on mismatch. Motion default respects the
#  standing scope: Taste landing pages keep the scroll ban (scrolling
#  moves nothing but the dealt moment) -- their motion is the hero
#  entrance + dealt moments + micro-interactions; motion-governed
#  (React/Next) app surfaces get entrances + staggers as well.
#  Known open token conflicts carried from fix #22 (parent adjudicates):
#  B3 30ms vs Rule 5 floor 0.05s; B15 0.8x vs exit-faster ~60-70%;
#  B4 0.97 vs scale.press 0.95. This block changes no token value.
# Placement: before STEP 5 (after the fix22 block).
python3 - "$PLUGIN_DIR" <<'PYEOF'
import os, sys
base = sys.argv[1]

subs = [
  ('MOTION-01', 'skills/motion-foundations/SKILL.md', '## Rules', """

**Motion is the default, not an afterthought (fix #23 §2, MOTION_F23).** Every build ships deliberate, eye-catching motion: entrances, staggers, dealt moments, micro-interactions, state transitions -- routed through the fix #22 motion tokens (Group A principles + Group B values, e.g. stagger 30ms, press scale 0.97, dropdowns 150-250ms). A build that feels static fails, even if every static rule passes. Motion is recorded in the decision record with its D19 reason (Motion dimension) and its token values, directed per §10 (direct, don't describe). Scope: on motion-governed surfaces (React/Next app surfaces) this means scroll entrances (M1) + staggers + micro-interactions; on Taste landing pages the scroll ban stands (scrolling moves nothing but the dealt moment) and the motion is the hero entrance + dealt moments + micro-interactions. `prefers-reduced-motion` is respected everywhere with a complete static fallback -- content visible at rest, no entrance to fail, every loop/scene rendered at its final state -- never a broken one. (D19 -- Motion: this rule IS the motion decision -- deliberate motion on every build, token-routed; Theme: motion is the dealt theme's motion voice, never a generic effect; Texture: none -- motion carries no surface treatment; Visuals: motion is what makes the build read as alive rather than static; Techniques: values come from `motionTokens` and the Group B rules, never hardcoded; Colors: none -- motion chooses no colours.)""", 'after'),
  ('MOTION-02', 'skills/motion-patterns/SKILL.md', '## Rules', """

**Motion is the default, not an afterthought (fix #23 §2, MOTION_F23).** Every pattern on a build ships with its motion live: entrances, staggers, dealt moments, micro-interactions, state transitions -- routed through the fix #22 motion tokens (Group A principles + Group B values, e.g. stagger 30ms, press scale 0.97, dropdowns 150-250ms). A build that feels static fails, even if every static rule passes. Each pattern is recorded in `docs/design-tokens.md`'s Motion list with its trigger and its token values, and its D19 reason (Motion dimension), directed per §10 (direct, don't describe). A pattern that should move and does not move in the rendered page is a finding (M4). `prefers-reduced-motion` is respected in every pattern with a complete static fallback -- a frozen one-frame state or the static final state, content visible at rest -- never a broken one. (D19 -- Motion: each pattern IS a motion decision -- trigger + tokens recorded; Theme: patterns move in the dealt theme's motion voice; Texture: none -- patterns carry no surface treatment; Visuals: live patterns are what make the build read as alive; Techniques: values come from `motion-foundations` tokens, never inline numbers (Rule 8); Colors: none -- patterns choose no colours.)""", 'after'),
  ('MOTION-03', 'skills/motion-advanced/SKILL.md', '## Rules', """

**Motion is the default, not an afterthought (fix #23 §2, MOTION_F23).** Advanced choreography is deliberate motion too: every drag, reveal, counter, mask, knob, overlap, cursor-follow, shimmer, or loading piece on a build must actually move in the rendered page, routed through the fix #22 motion tokens (Group A principles + Group B values, e.g. B5 knob stretch 12%, B16 overlap old & new states, B17 masks, B19 rubber band) and recorded in `docs/design-tokens.md`'s Motion list with its trigger and its token values, plus its D19 reason (Motion dimension), directed per §10 (direct, don't describe). A build that feels static fails, even if every static rule passes -- an advanced piece that sits still is a finding (M4). `prefers-reduced-motion` is respected everywhere with a complete static fallback -- the piece renders at its final state, content visible at rest -- never a broken one. (D19 -- Motion: each advanced piece IS a motion decision -- trigger + tokens recorded; Theme: choreography moves in the dealt theme's motion voice; Texture: none -- choreography carries no surface treatment; Visuals: moving pieces are what make the build read as alive; Techniques: values come from `motion-foundations` tokens, never inline numbers (Rule 6); Colors: none -- choreography chooses no colours.)""", 'after'),
  ('MOTION-04', 'skills/make-interfaces-feel-better/SKILL.md', '### Motion', """

**Motion is the default, not an afterthought (fix #23 §2, MOTION_F23).** The feel/timing decisions made here include a deliberate-motion inventory per surface: what moves (entrances, staggers, dealt moments, micro-interactions, state transitions), what triggers it, and which fix #22 motion tokens it runs on (Group A principles + Group B values, e.g. stagger 30ms, press scale 0.97, dropdowns 150-250ms). A surface with no deliberate motion and no recorded reason fails -- a build that feels static fails, even if every static rule passes. Motion is recorded in the decision record with its D19 reason (Motion dimension) and its token values, directed per §10 (direct, don't describe). `prefers-reduced-motion` is respected everywhere with a complete static fallback -- content visible at rest, no entrance to fail -- never a broken one. (D19 -- Motion: the inventory IS the motion decision for the surface; Theme: motion is the dealt theme's motion voice; Texture: none -- motion carries no surface treatment; Visuals: deliberate motion is what makes the surface read as alive; Techniques: feel/timing decided here, implemented with the motion-* skills; Colors: none -- motion chooses no colours.)""", 'after'),
  ('MOTION-05', 'skills/ui-ux-pro-max/SKILL.md', '## Before Delivering App UI', """

**Motion is the default, not an afterthought (fix #23 §2, MOTION_F23).** Before delivering app UI, check the motion default alongside the checklist above: every app/dashboard surface ships deliberate, eye-catching motion -- entrances, staggers, dealt moments, micro-interactions, state transitions -- implemented with the GSAP presets (`data/motion.csv`, 17 presets) and the fix #22 motion tokens (Group A principles + Group B values, e.g. stagger 30ms, press scale 0.97, dropdowns 150-250ms), directed per §10 (direct, don't describe). A build that feels static fails, even if every static rule passes. Motion is recorded in the decision record with its D19 reason (Motion dimension) and its token values. `prefers-reduced-motion` is respected everywhere with a complete static fallback -- content visible at rest, no entrance to fail -- never a broken one. (D19 -- Motion: this check IS the motion decision for the surface; Theme: motion is the dealt theme's motion voice; Texture: none -- motion carries no surface treatment; Visuals: deliberate motion is what makes the surface read as alive; Techniques: GSAP presets + motion tokens, never hardcoded values; Colors: none -- motion chooses no colours.)""", 'after'),
]
for pid, rel, old, add, mode in subs:
    p = os.path.join(base, rel)
    t = open(p).read()
    n = t.count(old)
    assert n == 1, f"fix23 W1 anchor not found exactly once in {rel}: {old[:70]!r} (count={n})"
    if mode == 'after':
        new = old + add
    elif mode == 'before':
        new = add.rstrip('\n') + '\n\n' + old
    else:  # replace
        new = add
    open(p, "w").write(t.replace(old, new))
print("fix23 W1 upstream block applied")
PYEOF

'''


def main():
    with open(BUILD_SH, encoding="utf-8") as f:
        text = f.read()
    # Idempotency guard: refuse if the block's marker is already present.
    assert MARKER not in text, (
        "fix23 W1 block already present in build.sh — refusing to insert twice")
    n = text.count(STEP5)
    assert n == 1, (
        f"STEP 5 anchor not found exactly once in build.sh: {STEP5!r} "
        f"(count={n})")
    new_text = text.replace(STEP5, BLOCK + STEP5, 1)
    with open(BUILD_SH, "w", encoding="utf-8") as f:
        f.write(new_text)
    print("fix23 W1 block inserted before STEP 5")


if __name__ == "__main__":
    main()
