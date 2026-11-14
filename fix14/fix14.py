#!/usr/bin/env python3
"""Fix program #14: add Soft Shadow as treatment #23 to less-flat-ui.

Edits the STANDALONE skill only: ~/workspace/cursor-skills/less-flat-ui/SKILL.md
(source of truth; build.sh copies it fresh on every build). Never edits the
staged copy. Also updates the W2-C1 build.sh patch anchor, which is anchored
on the "## The 22 treatments" heading — it must read 23 after this fix or the
build-time assert (count == 1) fails.

9 of the @lnunesdesigns reel's 10 treatments were already in the skill;
Soft Shadow is the only new one. The quoted reel title "22 Backgrounds..."
stays 22 (it is the reel's own title).
"""
import os

HOME = os.path.expanduser("~")
SKILL = os.path.join(HOME, "workspace/cursor-skills/less-flat-ui/SKILL.md")
BUILD = os.path.join(HOME, "workspace/hackathon-plugin/build.sh")

SOFT_SHADOW = """Characters cluster into a soft radial blob. Keep opacity low; ASCII is texture, not content, so it must never be readable as text or selectable.

### 23. Soft shadow

Best for: cards, buttons, modals, floating panels — any raised surface that needs depth without a pattern. The quietest treatment on this list: it adds dimension while leaving the surface itself untouched.

```css
.soft-shadow {
  background-color: #ffffff;
  box-shadow:
    0 1px 2px rgba(30, 30, 60, 0.06),
    0 8px 16px -4px rgba(30, 30, 60, 0.10),
    0 24px 48px -12px rgba(30, 30, 60, 0.18);
}
```

Three layers, not one: a tight contact shadow grounds the element, a mid shadow lifts it, and a large soft shadow (24–48px blur, low opacity) sells the height. One shadow alone reads flat; three at different blurs read as real depth. Tint the shadow color to the surface: warm brown-gray (`rgba(60, 40, 30, ...)`) on warm surfaces, cool blue-gray (`rgba(30, 40, 80, ...)`) on cool ones — a neutral black shadow on a warm page looks dirty.

Smaller variant for buttons and chips (tighter, closer to the surface):

```css
.soft-shadow-sm {
  box-shadow:
    0 1px 2px rgba(30, 30, 60, 0.08),
    0 4px 10px -2px rgba(30, 30, 60, 0.14);
}
```

Larger variant for modals and floating panels (float higher, spread wider):

```css
.soft-shadow-lg {
  box-shadow:
    0 2px 4px rgba(30, 30, 60, 0.06),
    0 16px 32px -8px rgba(30, 30, 60, 0.14),
    0 48px 80px -24px rgba(30, 30, 60, 0.25);
}
```

On dark surfaces, flip it: use a faint light glow instead of a dark shadow (`0 8px 32px rgba(255, 255, 255, 0.08)`), or a shadow tinted to the surface hue at very low opacity — a black shadow is invisible on black. Never use a hard-edged shadow (small blur, high opacity); that reads as a 2010s drop shadow, not depth.

Layers with everything: a shadow is a depth cue, not a pattern, so it stacks on top of any other treatment without competing. Never put two separate drop shadows on one element (the layered single `box-shadow` above is the treatment; a second one reads as a mistake).

## Record what you applied"""

skill_subs = [
    # 1. Frontmatter description count.
    ("description: Make the UI more striking with 22 textured treatments",
     "description: Make the UI more striking with 23 textured treatments"),
    # 2. Source line: 22 -> 23, add the @lnunesdesigns reel as second source.
    ("""Source of the 22 treatments: Instagram reel by @charles.unemployed, "22 Backgrounds to Make Designs Less Flat (In under 30 seconds)". The reel frames them as backgrounds, but each one is a texture/pattern treatment that can go on any surface: page backgrounds, cards, buttons, dividers, headings, modals, nav.""",
     """Source of the 23 treatments: Instagram reel by @charles.unemployed, "22 Backgrounds to Make Designs Less Flat (In under 30 seconds)"; plus Instagram reel by @lnunesdesigns, "How to make your design feel less flat in under 10 seconds" — 9 of its 10 treatments were already covered (thermal gradients, blueprint grids, water ripples, speckled graphite, fluted glass, contour lines, grainy gradients, single-hue landscapes, grass texture); Soft Shadow is the new one from it. The reels frame them as backgrounds, but each one is a texture/pattern treatment that can go on any surface: page backgrounds, cards, buttons, dividers, headings, modals, nav."""),
    # 3. Picker table: Premium row gains soft shadow.
    ("| Premium, soft, wellness, beauty | Paper texture, cloud sky, felt texture, grainy gradients |",
     "| Premium, soft, wellness, beauty | Paper texture, cloud sky, felt texture, grainy gradients, soft shadow |"),
    # 4. Surface table: cards, buttons, modals gain soft shadow.
    ("| Cards and panels | Felt, paper, fluted glass, grainy gradients, speckled graphite |",
     "| Cards and panels | Felt, paper, fluted glass, grainy gradients, speckled graphite, soft shadow |"),
    ("| Buttons and CTAs | Thermal gradients, iridescent shapes, grainy gradients |",
     "| Buttons and CTAs | Thermal gradients, iridescent shapes, grainy gradients, soft shadow |"),
    ("| Modals and overlays | Fluted glass, blurred photos |",
     "| Modals and overlays | Fluted glass, blurred photos, soft shadow |"),
    # 5. Section heading count.
    ("## The 22 treatments",
     "## The 23 treatments"),
    # 6. New treatment #23, appended after #22 (ASCII and pixels).
    ("""Characters cluster into a soft radial blob. Keep opacity low; ASCII is texture, not content, so it must never be readable as text or selectable.

## Record what you applied""",
     SOFT_SHADOW),
]

text = open(SKILL, encoding="utf-8").read()
for old, new in skill_subs:
    assert text.count(old) == 1, f"SKILL.md: pattern not found exactly once: {old[:70]!r}"
    text = text.replace(old, new)
open(SKILL, "w", encoding="utf-8").write(text)
print("less-flat-ui SKILL.md: 8 substitutions applied")

# build.sh W2-C1 patch anchor: "## The 22 treatments" appears exactly twice
# (old + new of the same patch). Both must read 23 after the heading rename.
btext = open(BUILD, encoding="utf-8").read()
assert btext.count("## The 22 treatments") == 2, (
    f"build.sh: expected 2 hits of '## The 22 treatments', got {btext.count('## The 22 treatments')}")
btext = btext.replace("## The 22 treatments", "## The 23 treatments")
open(BUILD, "w", encoding="utf-8").write(btext)
print("build.sh: W2-C1 anchor updated 22 -> 23 (2 occurrences)")
