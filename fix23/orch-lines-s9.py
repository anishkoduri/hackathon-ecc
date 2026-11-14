"""Fix #23 §9 orchestrate lines (worker W-§9) — dynamic interface.

One string constant, ORCH_LINES_S9, holding the EXACT lines the
integration worker inserts mechanically into the design-package step
(step 3) of orchestrate's SKILL.md. Do NOT edit orchestrate SKILL.md
here — another worker owns it; this file is the insertion payload.

INSERTION POINT (for the integration worker): staged orchestrate
SKILL.md (new-skills/orchestrate/SKILL.md), step 3 (Slice), immediately
AFTER the "Hero moment and functionality story in every UI slice brief
(fix #23, HERO_F23 / FUNC_F23)" paragraph — i.e. after its closing D19
line, anchor verified count==1 in the current staged file:

  Depth: the moment's and the mechanism's layer order, or `flat by choice — <reason>`.)

and immediately BEFORE "**Two-pass briefing for UI slices:**" (which
follows that paragraph). Mode: after. Insert the constant verbatim as a
new paragraph (blank line before and after), in the same bold-lead style
as the neighbouring step-3 paragraphs (Motion / Depth strategy / Hero
moment and functionality story).

NOTE on the old anchor: W1's integration anchor comment
`<!-- F23-ORCHESTRATE-EXTENSIONS: ... -->` is NO LONGER in the staged
file — integration consumed it when inserting the W2/W3/W4 lines — so
this file names the HERO/FUNC paragraph's closing line instead (verified
count==1, Nov 12, 2026).

What the lines do: the brief names the slice's dynamic story per
surface — WHAT changes, WHAT triggers it, HOW it moves — recorded in
the decision record before any UI is built. A brief with no dynamic
story named is not ready to dispatch. The step-4 "Design package in
every UI brief" restatement needs no separate edit: it points back at
step 3 ("same rule as step 3"), so these lines govern it too.

§9 vs §2 vs §5 (stated in the lines, not restated): §2 (MOTION_F23) is
the motion-presence rule — deliberate motion on every build. §5
(FUNC_F23) is the functionality-showing rule — live data IS the
functionality showing. §9 (DYNAMIC_F23) is the state-change and
interactivity rule — what changes, what triggers it, how it moves.

Anchor tokens carried: DYNAMIC_F23.
"""

ORCH_LINES_S9 = """**Dynamic story in every UI slice brief (fix #23 §9, DYNAMIC_F23):** the brief also names the slice's dynamic story, recorded in the decision record before any UI is built: per surface, WHAT changes (live data, statuses, counts and totals), WHAT triggers it (a user action, data arriving, time passing), and HOW it moves (the choreographed state change — entering/leaving, loading to loaded, empty to filled, selected, confirmed — with its motion tokens, and a dealt moment where the change is a moment). Surfaces show live state, not frozen mock content; interactive elements respond immediately (press states, hover, transitions); the interface invites interaction — sortable, filterable, expandable, draggable where it serves the job — the user can DO things, not just look. A state change with no motion is a gap; a control that looks interactive but does nothing is a gap. Calibration: dynamic never means gratuitous — motion serves the state change, and the reduced-motion fallback stays complete. This is the state-change and interactivity rule: §2 (MOTION_F23) is the motion-presence rule (deliberate motion on every build) and §5 (FUNC_F23) is the functionality-showing rule (live data IS the functionality showing); this section states what changes, what triggers it, and how it moves, and does not restate either. A UI brief with no dynamic story named is not ready to dispatch. (D19 — Motion: the dynamic story IS the motion decision for the surface — what changes, its trigger, its tokens; Theme: changes move in the dealt theme's motion voice; Texture: the theme's treatment or `none — <reason>`; Visuals: live, choreographed surfaces are what make the build read as alive; Techniques: changes route through the motion-* skills and their tokens, never hardcoded values; Colors: the theme's own tokens; Depth: a change that reorders layers names the layer order, or `flat by choice — <reason>`.)"""
