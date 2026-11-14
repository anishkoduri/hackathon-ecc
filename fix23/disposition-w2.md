# Fix #23 §3 disposition — worker W2 (fonts, no defaulting)

Every §3 item, where placed (file + anchor token), status.
Anchor tokens: every new rule carries a `_F23` token.
Thresholds (one definition, in the typeset lens; repeated verbatim
elsewhere): visual share = Σ (computed size in px × visible characters)
per face ÷ total, per primary screen + build roll-up. **T1a** body face
≤ 40% of build visual share. **T1b** body face ≤ 55% on any single primary
screen. **T1c** display/important faces combined ≥ 25% of build visual
share. **T1d** on the hero/home surface, display share > body share.
**T2** trio identical to the previous build's trio with no recorded reuse
reason → FAIL. **T3** distinct faces ≥ max(3, ceil(N/20)) for N Type-list
text elements, each counted face ≥ 5% visual share. Justification: Home
Run (Nov 12, 2026) — all 5 static faces loaded and a real display face
dealt, yet Fraunces (the body face) carried the whole page by volume,
because in an app most visible text IS body text; 40% keeps the body face
from being the identity (display + data carry the ≥ 60% majority), 55%
lets one screen be text-heavy without letting it BE the body face, 25%
forces display type past headings into hero lines, names, prices, and key
labels. Clearance: T1a/T1b only by a scoped exception (recorded D19
reason + theme-fit, T1c still binding); T2 only by a recorded reuse
reason; T1c/T1d/T3 have no clearance — re-deal or re-balance.

## Placement table

| §3 item | Placement (file + anchor token) | Status |
|---|---|---|
| Body face must never be the visually dominant face; display/important faces carry the visual identity | `round2-skills/polish-pass/reference/lenses/typeset.md` — Type-audit section, `TYPEAUDIT_F23`, T1a–T1d; `round2-skills/polish-pass/reference/slop-checklist.md` — Type-audit section, `TYPEAUDIT_F23`, T1a–T1d | new |
| Type-audit step in polish-pass: records distinct faces used, share of visible text per face, whether the trio matches the previous build's | `reference/lenses/typeset.md` — Type-audit section, `TYPEAUDIT_F23` (full home: measurement method, Type-audit table, trio definition); `reference/slop-checklist.md` — Type-audit section, `TYPEAUDIT_F23` (checklist half: flags + clearance); `round2-skills/polish-pass/SKILL.md` non-negotiable 5 — run wiring, `TYPEAUDIT_F23` | new |
| Type audit must be able to FAIL a build (not just record faces) | `reference/lenses/typeset.md` — fail conditions T1a–T1d/T2/T3, `TYPEAUDIT_F23`; `reference/slop-checklist.md` — same, `TYPEAUDIT_F23`; `skills/browser-qa/SKILL.md` via `fix23/apply-w2.py` sub `BQA-TYPEAUDIT` — verdict lines, `TYPEAUDIT_F23` | new |
| A build whose typography reads as defaulted fails at browser-qa (one face dominating, or same trio as last build without a recorded reason) | `skills/browser-qa/SKILL.md` via `fix23/apply-w2.py` sub `BQA-TYPEAUDIT`, mode after, anchor "a screen with no named direction … FAILS — report it as a distinctiveness finding …" — `TYPEAUDIT_F23` | new |
| F7 strengthened: every text element gets a distinctive artistic font decision AND the decision record must show VARIETY across the build | `skills/ui-ux-pro-max/SKILL.md` via `fix23/apply-w2.py` sub `UIPRO-F7VAR`, mode after, anchor "No element defaults to the body face without a decision … The full F7 rule lives in `design-taste-frontend` step 4a." — `F7VAR_F23` (+ `TYPEAUDIT_F23` pointer) | new |
| Trio "one display face + body stand-in + mono" is a pattern, not a default; trio re-chosen per build; reuse without a recorded reason fails | `reference/lenses/typeset.md` — T2, `TYPEAUDIT_F23`; `reference/slop-checklist.md` — T2, `TYPEAUDIT_F23`; `skills/browser-qa/SKILL.md` via `BQA-TYPEAUDIT` — `TYPEAUDIT_F23`; `skills/orch-build-mvp/SKILL.md` via `ORCH-TYPEAUDIT` — T2 record, `TYPEAUDIT_F23`; `fix23/orch-lines-w2.py` — `ORCH_LINES_W2`, `TRIO_F23` | new |
| Too few distinct faces for the build's text-element count fails (variety floor) | `reference/lenses/typeset.md` — T3, `TYPEAUDIT_F23`; `reference/slop-checklist.md` — T3, `TYPEAUDIT_F23`; `skills/orch-build-mvp/SKILL.md` via `ORCH-TYPEAUDIT` — T3 record, `TYPEAUDIT_F23` | new |
| F4 stands: Fraunces is for long body text and small incidental text ONLY | Unchanged — fix #21 tightened scope text is NOT rewritten anywhere. Enforcement is new (T1 caps + T1c display floor) | covered (rule unchanged) + new enforcement |
| Enforcement change: body face may not dominate; display faces must do more of the visible work | T1a/T1b (caps) + T1c/T1d (display must do the work) in the typeset lens, slop checklist, browser-qa verdict lines, and orch-build-mvp record checks — all `TYPEAUDIT_F23` | new |
| Extend the fix #19/#20/#21 static checks in orch-build-mvp (extension line, fix22 §13 DEPTH-12 precedent; do not rewrite frozen D19 text) | `skills/orch-build-mvp/SKILL.md` via `fix23/apply-w2.py` sub `ORCH-TYPEAUDIT`, mode after, anchor "a blanket 'all text' class line is not a class decision. (F7 record) …" — `TYPEAUDIT_F23`. Appends a "Fix #23 static checks" paragraph; the fix #21 text is untouched | new |
| Orchestrate design-package step: Type list feeds the type-audit + trio re-deal requirement | `fix23/orch-lines-w2.py` — `ORCH_LINES_W2`, tokens `TYPEAUDIT_F23` / `TRIO_F23`. Insertion by the integration worker, mode after, anchor the "Depth strategy recorded with the direction (fix #22 §13, DEPTH_F22)" line in orchestrate's SKILL.md (count==1 verified) | new (insertion pending integration) |
| Type list feeds the type-audit (harmony side) | `round2-skills/polish-pass/SKILL.md` harmony paragraph — sentence after the fix #21 sentence, `TYPEAUDIT_F23` | new |

## Files changed / created

- Staged (edited in place):
  - `round2-skills/polish-pass/reference/lenses/typeset.md` — Type-audit
    section + 3 Rules checklist lines (`TYPEAUDIT_F23`).
  - `round2-skills/polish-pass/reference/slop-checklist.md` — Type-audit
    section appended at end (`TYPEAUDIT_F23`).
  - `round2-skills/polish-pass/SKILL.md` — harmony paragraph sentence +
    non-negotiable 5 run wiring (`TYPEAUDIT_F23`).
- Created under `fix23/`:
  - `fix23/apply-w2.py` — inserts one runtime-patch block into build.sh
    before `# STEP 5 — Counts` (subs `BQA-TYPEAUDIT`, `UIPRO-F7VAR`,
    `ORCH-TYPEAUDIT`; count==1 asserts; idempotency guard refuses if the
    marker comment is already present). NOT run — integration runs it.
  - `fix23/orch-lines-w2.py` — `ORCH_LINES_W2` string constant, the exact
    orchestrate design-package insertion.
  - `fix23/disposition-w2.md` — this file.

## Notes / things the coordinator should know

- **Path correction:** the task named `reference/typeset.md`; no such file
  exists. The typeset file is `reference/lenses/typeset.md` (that is where
  the fix #20/#21 type rules already live). All staged typeset edits went
  there.
- **polish.md Step 2 not edited:** it is outside the owned file set
  (SKILL.md, typeset lens, slop checklist). The type-audit run is wired
  through SKILL.md non-negotiable 5, which binds every pass; polish.md
  Step 2 picks it up through that non-negotiable, the same way the depth
  check is wired (SKILL.md non-negotiable 5, not polish.md).
- **No prior verifiers edited. No build.sh run. No built-tree edits.**
  build.sh md5 is unchanged from baseline
  (4799a819791b9c3ec4c19136ad698397, 23,774 lines). The built tree was
  only read (greps / counts). `fix11/fix11-stage.py` not re-run.
  `~/workspace/cursor-skills/less-flat-ui` untouched. No `/demo` wiring
  or DEMOGATE tokens touched.
- **Anchors:** all three runtime-patch anchors verified count==1 against
  the CURRENT built tree (AST-extracted from apply-w2.py and counted, plus
  an in-memory simulated apply of each sub). The orchestrate anchor line
  (DEPTH_F22) verified count==1 in the built orchestrate SKILL.md.
- **Banned terms:** 0 in all new text (checked case-insensitively:
  claude/codex/anthropic/opus/sonnet/haiku/composer-2.5) across the three
  staged files, apply-w2.py subs, and orch-lines-w2.py.
- **Grok pins:** no model names appear in any new text.
- **Standing preserved:** type-audit findings are candidate evidence for
  `browser-qa`, never a verdict, everywhere except the browser-qa verdict
  lines themselves (browser-qa remains the sole verdict executor).
  "More, not bolder", anti-derivative, D19 seven dimensions, and static
  self-hosted fonts (no variable file, no system-ui fallback) are
  untouched and restated as binding in the new text.
