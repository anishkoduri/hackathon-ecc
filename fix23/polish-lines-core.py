"""Fix #23 CORE — polish-pass SKILL.md memorability-candidates line for worker W-CORE.

Defines the EXACT polish-pass SKILL.md line this section needs. The
integration worker inserts it into the staged polish-pass SKILL.md
(round2-skills/polish-pass/SKILL.md), step 5's trailing paragraph, after
the dynamic-story sentence — anchor verified count==1 in the staged file:

  Read the dynamic story from the decision record (per surface: what changes, what triggers it, how it moves) and check the static code for it: live-state wiring present (not frozen mock content), interactive controls present with handlers (sortable / filterable / expandable / draggable where the story names them), and each state change routed through motion tokens; a surface whose recorded story has no wiring, a control with no handler, or a state change with no motion token is candidate evidence for `browser-qa`, never a verdict — whether the control actually responds and the change is actually choreographed is `browser-qa`'s live check alone (DYNAMIC_F23).

Mode: after (new sentence following that sentence, same paragraph —
the constant starts with a leading space, per the polish-lines-s9.py
pattern).

Do NOT edit round2-skills/polish-pass/SKILL.md directly from here.
What the line does: a memorability-candidates static check —
polish-pass reads the memorable moment named in the decision record
(per screen: the moment, element, or motion intended to make it
memorable) and records, as candidate evidence, whether the static code
reads as dynamic, over the top, and wow / striking / stunning on first
sight and on use. A screen with no memorable moment named, or a named
moment that reads as merely adequate on the static code, is CANDIDATE
EVIDENCE for `browser-qa`, never a verdict: whether the build is
actually memorable is browser-qa's finish-review verdict alone
(MEMORABLE_F23, apply-core.py sub MEMORABLE-BQA-01). Standing:
candidate evidence, never a verdict (screen-verdicts rule, fix #13e).

Why this line fits (and is not duplication): polish-pass already
records the same standing of candidate evidence for the neighbouring
bars in this paragraph — the type audit (TYPEAUDIT_F23) and the
dynamic story (DYNAMIC_F23). Memorability needs the same static-code
evidence feed (what was INTENDED to be memorable, and whether it reads
that way before rendering) for browser-qa to judge against at the
finish review. The line states the over-the-top / loudness distinction
once, in candidate-evidence terms, and does not restate the verdict.

Token: MEMORABLE_F23. No banned terms; no model pins needed in this line.
"""

POLISH_LINES_CORE = """ Then record the memorability candidates (fix #23 §1, MEMORABLE_F23) on the same target — same standing: candidate evidence for `browser-qa`, never a verdict — and record them in `.hallmark/candidate-evidence.md` (screen + the moment, element, or motion intended to make it memorable + whether it reads as dynamic, over the top, and wow / striking / stunning on first sight and on use) the same way slop findings are recorded. A screen with no memorable moment named in the decision record, or a named moment that reads as merely adequate on the static code, is candidate evidence for `browser-qa`, never a verdict — whether the build is actually memorable is `browser-qa`'s finish-review verdict alone (MEMORABLE_F23). "Over the top" here is ambition and impact, not loudness: "more, not bolder" still governs styling, so a quiet-palette build with a strong moment is not flagged for being quiet."""
