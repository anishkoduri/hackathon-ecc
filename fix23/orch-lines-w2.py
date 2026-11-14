"""Fix #23 section 3 orchestrate lines (worker W2) — fonts, no defaulting.

One string constant, ORCH_LINES_W2: the EXACT lines the integration worker
inserts mechanically into the design-package step of orchestrate's
SKILL.md (the design-package rule, row 10), immediately AFTER the line:

  **Depth strategy recorded with the direction (fix #22 \u00a713, DEPTH_F22):** ...

(that line occurs exactly once in the built orchestrate SKILL.md — verified
by grep before this file was written). Mode: after. The insertion follows
the fix #22 section 13 precedent (DEPTH_F22 line appended after the
design-package rule the same way).

What the lines do: the Type list feeds the type-audit, and the trio is
re-dealt per build. The design package's Type list is the type-audit input
(per-face visual shares + trio-vs-previous-build line), the trio is
re-chosen per build (never inherited without a recorded reason), and the
share bars + variety floor the audit checks are stated here so the brief
carries them before any UI is built. The full rule lives in polish-pass
(reference/lenses/typeset.md, TYPEAUDIT_F23); the record checks live in
orch-build-mvp step 6 (TYPEAUDIT_F23); the verdict is browser-qa's alone
(TYPEAUDIT_F23). No UI slice builds on an unstated trio.

Anchor tokens carried: TYPEAUDIT_F23, TRIO_F23.
"""

ORCH_LINES_W2 = """

**Type audit feeds from the Type list; the trio is re-dealt per build (fix #23 \u00a73, TYPEAUDIT_F23 / TRIO_F23):** the design package's Type list is also the type-audit input \u2014 every UI slice brief names the build's trio (display family + body family + data/mono family) and records it in `docs/design-tokens.md` with the per-face visual shares (visual share = \u03a3 size \u00d7 visible characters per face \u00f7 total, per primary screen + build roll-up) and the trio-vs-previous-build line (this build's trio, the previous build's recorded trio, match? + reuse reason if matched; a first build records `previous trio: none (first build)`). The trio is re-dealt per build \u2014 Hallmark already deals type, and the pairing must be re-dealt, not inherited from the previous build; a brief that reuses the previous build's trio without a recorded reason (why this same trio is right for THIS build, fix #19 D19 reason + theme-fit) is an incomplete brief. The Type list also carries the variety count (distinct faces \u2265 max(3, ceil(N/20)) for N Type-list text elements, each counted face \u2265 5% visual share) and the share bars the audit checks (body face \u2264 40% of the build's visual share and \u2264 55% on any primary screen; display/important faces \u2265 25% of the build's visual share; display > body on the hero/home surface). The full type-audit rule lives in `polish-pass` (reference/lenses/typeset.md, TYPEAUDIT_F23); the record checks live in `orch-build-mvp` step 6 (TYPEAUDIT_F23); the verdict is `browser-qa`'s alone. No UI slice builds on an unstated trio."""
