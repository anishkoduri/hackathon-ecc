"""Fix #23 §9 — polish-pass SKILL.md dynamic-story line for worker W-§9.

Defines the EXACT polish-pass SKILL.md line this section needs. The
integration worker inserts it into the staged polish-pass SKILL.md
(round2-skills/polish-pass/SKILL.md), step 5's trailing paragraph, after
the type-audit sentence — anchor verified count==1 in the staged file:

  Then run the type audit ([reference/lenses/typeset.md](reference/lenses/typeset.md), `TYPEAUDIT_F23`) on the same target — same standing: candidate evidence for `browser-qa`, never a verdict — and record its table and any fail-condition hit in `.hallmark/candidate-evidence.md` (screen + face shares + trio comparison + which threshold) the same way slop findings are recorded.

Mode: after (new sentence following that sentence, same paragraph).

Do NOT edit round2-skills/polish-pass/SKILL.md directly from here
(W2 owns it). What the line does: a dynamic-story static check —
polish-pass reads the dynamic story from the decision record (per
surface: what changes, what triggers it, how it moves) and checks the
static code for it (live-state wiring, interactive controls with
handlers, state changes routed through motion tokens). A surface whose
recorded story has no wiring, a control with no handler, or a state
change with no motion token is CANDIDATE EVIDENCE for `browser-qa`,
never a verdict: whether the control actually responds and the change
is actually choreographed is browser-qa's LIVE check alone
(DYNAMIC_F23, Phase 2 step 6). Standing: candidate evidence, never a
verdict (screen-verdicts rule, fix #13e).

Token: DYNAMIC_F23. No banned terms; no model pins needed in this line.
"""

POLISH_LINES_S9 = """ Then run the dynamic-story check (fix #23 §9, DYNAMIC_F23) on the same target — same standing: candidate evidence for `browser-qa`, never a verdict — and record its findings in `.hallmark/candidate-evidence.md` (surface + what should change + trigger + whether the wiring and motion are present) the same way slop findings are recorded. Read the dynamic story from the decision record (per surface: what changes, what triggers it, how it moves) and check the static code for it: live-state wiring present (not frozen mock content), interactive controls present with handlers (sortable / filterable / expandable / draggable where the story names them), and each state change routed through motion tokens; a surface whose recorded story has no wiring, a control with no handler, or a state change with no motion token is candidate evidence for `browser-qa`, never a verdict — whether the control actually responds and the change is actually choreographed is `browser-qa`'s live check alone (DYNAMIC_F23)."""
