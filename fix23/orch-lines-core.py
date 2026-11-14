"""Fix #23 CORE orchestrate lines (worker W-CORE) — THE CORE, memorability.

One string constant, ORCH_LINES_CORE, holding the EXACT lines the
integration worker inserts mechanically into the design-package step
(step 3) of orchestrate's SKILL.md. Do NOT edit orchestrate SKILL.md
here — this file is the insertion payload.

INSERTION POINT (for the integration worker): staged orchestrate
SKILL.md (new-skills/orchestrate/SKILL.md), step 3 (Slice), immediately
AFTER the "Ambition — use the inventory, or say specifically why not
(fix #23 §1, AMBITION_F23)" paragraph — i.e. after its closing
sentence, anchor verified count==1 in the current staged file:

  F6 (impressive is the governing bar) is the PRIMARY gate: browser-qa judges impressive AND ambitious, not just rule-correct — a rule-correct but unambitious design fails at the finish review.

and immediately BEFORE the "**Motion is the default, not an afterthought
(fix #23 §2, MOTION_F23).**" paragraph that follows it. Mode: after.
Insert the constant verbatim as a new paragraph (blank line before and
after), in the same bold-lead style as the neighbouring step-3
paragraphs (Ambition / Motion / Depth strategy / Hero moment and
functionality story / Dynamic story).

NOTE on the old anchor: W1's integration anchor comment
`<!-- F23-ORCHESTRATE-EXTENSIONS: ... -->` is NO LONGER in the staged
file — integration consumed it when inserting the W2/W3/W4 lines — so
this file names the AMBITION_F23 paragraph's closing sentence instead
(verified count==1, Nov 12, 2026).

What the lines do: they ELEVATE the ambition / F6-primary-gate language
W1 wrote (AMBITION_F23) with the memorability criterion — THE CORE
(SPEC §1, Anish, Nov 12). Impressive is the floor, memorable is the
bar; browser-qa judges memorability as the TOP criterion at the finish
review; "over the top" is ambition and impact, NOT loudness for its own
sake ("more, not bolder" still governs styling — a build can be over
the top and quiet in palette; it cannot be forgettable); a build the
user forgets the next day fails, however rule-correct.

What the lines do NOT do: they do not restate the §1/§2/§4/§5/§9
rules. The ambition bar (AMBITION_F23), the motion bar (MOTION_F23),
the hero bar (HERO_F23), the functionality bar (FUNC_F23), and the
dynamic bar (DYNAMIC_F23) are cross-referenced, not restated — the
memorability criterion governs them, and each keeps its own home. The
step-6 F6-primary-gate extension (same AMBITION_F23 token, staged
orchestrate line 147) is likewise cross-referenced by token, not
rewritten: it already states F6 as the PRIMARY gate, and this paragraph
states what sits above it. The frozen D19 text is untouched.

Anchor tokens carried: MEMORABLE_F23 (the CORE token family — used
everywhere in this worker's output: orch-lines-core.py,
polish-lines-core.py, apply-core.py).
"""

ORCH_LINES_CORE = """**Memorable is the bar — above F6 (fix #23 §1, MEMORABLE_F23):** dynamic + over the top + wow + striking + stunning + above all MEMORABLE is the core, and it governs the ambition bar above (AMBITION_F23): impressive is the floor, memorable is the bar. The design package step records, per build, what makes it memorable — the dynamic behaviour, the over-the-top ambition in elements and motion, and the moment that hits on first sight and on use — alongside the used vs considered-and-rejected inventory record. Browser-qa judges memorability as the TOP criterion at the finish review: a build the user would forget the next day FAILS, however rule-correct. "Over the top" is ambition and impact, not loudness for its own sake — "more, not bolder" still governs styling (do not just crank weight, color, or size): a build can be over the top and quiet in palette; it cannot be forgettable. The bars below answer to it without restating it: motion is the default (MOTION_F23), the hero carries the amazing moment (HERO_F23), the mechanism shows (FUNC_F23), and the interface is live and responsive (DYNAMIC_F23). A UI brief with no memorable moment named is not ready to dispatch. (D19 — Motion: the memorable moment's entrance and motion values, or `none — <reason>` where still; Theme: the moment is the dealt theme's material; Texture: the theme's treatment or `none — <reason>`; Visuals: the moment is what the user remembers tomorrow; Techniques: the moment routes through the dealt moment and the motion tokens, never hardcoded values; Colors: the theme's own tokens; Depth: the moment's layer order, or `flat by choice — <reason>`.)"""
