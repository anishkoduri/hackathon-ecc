"""Fix #23 §6 — orchestrate line for worker W4 (alignment + centering).

Defines the EXACT orchestrate line this section needs. The integration
worker inserts it into the staged orchestrate SKILL.md
(new-skills/orchestrate/SKILL.md) after the fix #15 D1 screenshot-QA
sentence — anchor verified count==1 in the staged file:
"Screenshot QA at least once before finish (fix #15 D1)."
Mode: after (new paragraph following that sentence).

Do NOT edit orchestrate SKILL.md directly from here (W1 owns it).
Tokens: BLOCK_F23 (blocking-gap gate), COVER_F23 (coverage matrix).
No banned terms; no model pins needed in this line.
"""

ORCH_LINES_W4 = """**Alignment coverage gate (fix #23 §6, BLOCK_F23).** A build with an unverified width or an unverified flow state is NOT shippable — the gap is a blocking finding, not a note: `browser-qa`'s coverage matrix (COVER_F23) is complete — desktop 1440, mid 900 (band 768–1100), mobile 390, every flow state measured + screenshotted — or the verdict is DO NOT SHIP. Eyeballing screenshots is not a check."""
