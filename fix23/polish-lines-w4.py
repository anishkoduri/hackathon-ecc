"""Fix #23 §6 — polish-pass SKILL.md pointer line for worker W4
(alignment + centering).

Defines the EXACT polish-pass SKILL.md pointer line to
reference/alignment.md. The integration worker inserts it into the staged
polish-pass SKILL.md (round2-skills/polish-pass/SKILL.md), non-negotiable 4,
after the slop-checklist sentence — anchor verified count==1 in the staged
file:
"Also read the slop checklist ([reference/slop-checklist.md](reference/slop-checklist.md), `SLOP_F22`)"
Mode: after (new sentence following that sentence).

Do NOT edit round2-skills/polish-pass/SKILL.md directly from here
(W2 owns it). The checklist itself is the new staged file
round2-skills/polish-pass/reference/alignment.md (W4 owns it).
Token: ALIGN_F23. Standing: candidate evidence for `browser-qa`, never
a verdict (screen-verdicts rule, fix #13e).
"""

POLISH_LINES_W4 = """Also read the alignment checklist ([reference/alignment.md](reference/alignment.md), `ALIGN_F23`) and run its measurements on every pass — same standing: candidate evidence for `browser-qa`, never a verdict — and record alignment findings in `.hallmark/candidate-evidence.md` (screen + measurement + screenshot) the same way slop findings are recorded."""
