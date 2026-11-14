# Fix #23 §6 disposition — worker W4 (alignment + centering)

## Scope

SPEC §6 only: everything aligned properly, checks tightened. browser-qa
remains the SOLE executor of pass/fail verdicts on rendered screens;
everything else is candidate evidence. "More, not bolder", anti-derivative,
D19 seven dimensions stand. No bundle, no commit, no push. build.sh NOT
run (integration runs it); built tree untouched (md5 still
4799a819791b9c3ec4c19136ad698397, 23,774 lines, verified after all work).

## Assertion list + coverage matrix (the §6 deliverable, defined from the SPEC)

Tolerances: **0px** for overflow; **≤ 2px** for centering / grid / spacing
equality (sub-pixel rounding; the audit's 1px tab-label deltas at 390px are
rounding, not misalignment). Geometry from `getBoundingClientRect()` on the
live rendered page, never from source or from a screenshot alone.

| # | Assertion | Rule |
|---|---|---|
| 1 | ALIGN_F23_OVERFLOW | `scrollWidth - innerWidth == 0` at every width; no leaf text element with `scrollWidth > clientWidth + 1` |
| 2 | ALIGN_F23_CENTER | Hero/phone frame center offset ≤ 2px at 1440 and 390; at mid, if side panels share the row, the hero GROUP is centered with equal outer margins ≤ 2px (frame alone is NOT the check there) |
| 3 | ALIGN_F23_NAV | Adjacent nav gaps equal ± 2px; nav group centered in its bar; each label center == its item center ± 2px |
| 4 | ALIGN_F23_GRID | Full-width view children share one left / one right edge (± 2px); a narrower child is left-aligned or centered; feed cards share one left and one right edge per width |
| 5 | ALIGN_F23_CLIP | No text clipped / overflowing its container; no element beyond its frame unless a DECLARED intentional bleed recorded in the decision record (page overflow still 0) |
| 6 | ALIGN_F23_LABELS | Diagram/SVG text boxes pairwise non-overlapping and inside the viewport; stamps centered on parent ± 2px; status pairs judged by vertical CENTERS, not tops |
| 7 | ALIGN_F23_ACTIONS | Grouped inputs centered on their panel ± 2px; full-width primary actions share the grid edges, narrower ones centered |
| 8 | ALIGN_F23_PANELS | Desktop side-panel gutters symmetric ± 2px; tops aligned ± 2px unless a stagger is recorded in the decision record; stacked mid-band blocks centered as a group |
| 9 | COVER_F23 (matrix) | Widths: desktop 1440, mid 900 (default probe for band 768–1100; probe breakpoint ± 1 if one falls inside the band, plus a mid full-page shot), mobile 390. States: EVERY flow state — all screens × all reachable states (error/wrong-code, empty, success/delivered, accepted, scrolled) — measured + screenshotted at all three widths |
| 10 | BLOCK_F23 (gate) | A build with an unverified width or an unverified flow state is NOT shippable — the gap is a blocking finding, not a note; missing coverage → DO NOT SHIP; an empty matrix cell is never SHIP / SHIP WITH FIXES / INCONCLUSIVE-as-pass |

## Per-item placement table

| §6 item | Placement (file + anchor token) | Status |
|---|---|---|
| (a) No horizontal overflow at any tested width | `fix23/apply-w4.py` → build.sh block `ALIGN_F23-A`, anchor `### Phase 3: Visual Regression`; `round2-skills/polish-pass/reference/alignment.md` § ALIGN_F23_OVERFLOW | new |
| (a) Hero/phone frame centered in viewport | `ALIGN_F23-A` (same anchor); `alignment.md` § ALIGN_F23_CENTER | new |
| (a) Nav items evenly spaced and centered | `ALIGN_F23-A` (same anchor); `alignment.md` § ALIGN_F23_NAV | new |
| (a) Card edges aligned to a common left/right grid | `ALIGN_F23-A` (same anchor); `alignment.md` § ALIGN_F23_GRID | new |
| (a) No text clipped or overflowing its container | `ALIGN_F23-A` (same anchor); `alignment.md` § ALIGN_F23_CLIP | new |
| (a) No label collisions (diagrams, strips, stamps) | `ALIGN_F23-A` (same anchor); `alignment.md` § ALIGN_F23_LABELS | new |
| (a) Primary actions centered on their axis | `ALIGN_F23-A` (same anchor); `alignment.md` § ALIGN_F23_ACTIONS | new |
| (a) Side-panel symmetry / top alignment (derived from the render audit's gutter + top-delta measurements) | `ALIGN_F23-A` item (h); `alignment.md` § ALIGN_F23_PANELS | new |
| (b) Screenshot coverage MANDATORY at 3 widths (1440 / mid 768–1100 / 390), 900 default probe | `ALIGN_F23-B`, anchor `1. Screenshot key pages at 3 breakpoints (375px, 768px, 1440px)`; `alignment.md` § COVER_F23 | new |
| (b) Coverage for EVERY flow state, not just happy path | `ALIGN_F23-C`, anchor `3. Flag layout shifts > 5px, missing elements, overflow`; `alignment.md` § COVER_F23 | new |
| (c) Unverified width/state = NOT shippable, blocking finding | `ALIGN_F23-D` (`BLOCK_F23`), anchor `# verdict ∈ SHIP / SHIP WITH FIXES / DO NOT SHIP; use INCONCLUSIVE if no visual baseline`; `fix23/orch-lines-w4.py` `ORCH_LINES_W4` (`BLOCK_F23` + `COVER_F23`); `alignment.md` § BLOCK_F23 | new |
| QA report gains an Alignment section | `ALIGN_F23-E`, anchor `### Visual\n- [✗] Hero section overflows on 375px viewport` | new |
| polish-pass runs the checklist as candidate evidence | `fix23/polish-lines-w4.py` `POLISH_LINES_W4` (`ALIGN_F23`) — pointer line only; `alignment.md` is the new staged file this worker owns | pointer |
| Measurement model (harness approach) | `alignment.md` header + build.sh block header comment (Home Run audit harness `cold-start-render/home-run/qa/align-audit.mjs` as the model) | new |

## Files delivered (all under `~/workspace/hackathon-plugin/`)

1. `round2-skills/polish-pass/reference/alignment.md` — NEW staged file (this worker owns it): alignment checklist, candidate evidence only.
2. `fix23/apply-w4.py` — NEW: inserts ONE runtime-patch block into build.sh immediately BEFORE `# STEP 5 — Counts` (5 subs, `ALIGN_F23-A`–`E`, all mode `after`, fix22 block pattern). NOT run — integration runs it.
3. `fix23/orch-lines-w4.py` — NEW: `ORCH_LINES_W4` string constant, the exact orchestrate gate line (tokens `BLOCK_F23`, `COVER_F23`). Intended anchor: after the fix #15 D1 screenshot-QA sentence in staged orchestrate SKILL.md (count==1 verified).
4. `fix23/polish-lines-w4.py` — NEW: `POLISH_LINES_W4` string constant, the exact polish-pass SKILL.md pointer line to `reference/alignment.md` (token `ALIGN_F23`). Intended anchor: after the slop-checklist sentence in non-negotiable 4 (count==1 verified).
5. `fix23/disposition-w4.md` — this file.

## Anchor verification (all against the CURRENT built tree, by grep before writing)

- browser-qa `skills/browser-qa/SKILL.md`: all 5 patch anchors count==1
  (`### Phase 3: Visual Regression`; the 3-breakpoints line; the layout-shifts
  line; the `# verdict ∈ …` line; the `### Visual` overflow line). 3 further
  nearby strings also checked count==1 (Phase 2 header, Output Format
  header, Verdict example line). **Zero anchors failed to resolve.**
- `# STEP 5 — Counts` in build.sh: count==1 (line 23765). Marker
  `# --- fix23 §6: alignment + centering (ALIGN_F23) ---`: absent from
  build.sh (count 0); `_F23` count 0 in build.sh before this work.
- Orchestrate anchor (fix #15 D1 sentence): count==1 in staged
  `new-skills/orchestrate/SKILL.md`. Polish anchor (slop-checklist
  sentence): count==1 in staged `round2-skills/polish-pass/SKILL.md`.
- Tokens `ALIGN_F23` / `COVER_F23` / `BLOCK_F23`: novel in all four target
  files before this work (only the new `alignment.md` itself contains them).

## Verification performed (without running build.sh)

- `apply-w4.py` compiles; its inner heredoc Python parses; the BLOCK's
  `subs` list is byte-identical to the module-level `SUBS` (AST comparison).
- Simulation: the block was run against a `/tmp` copy of the built
  browser-qa SKILL.md — exit 0, tokens landed (`ALIGN_F23` ×3,
  `COVER_F23` ×2, `BLOCK_F23` ×3, as designed). Built tree untouched.
- Banned-term scan (case-insensitive) over `apply-w4.py`,
  `alignment.md`, `orch-lines-w4.py`, `polish-lines-w4.py`: 0 hits.
  Bare `grok-4.6-high-fast`: 0 (only `cursor-grok-4.6-high-fast` in a
  docstring, as required). No `/demo` or DEMOGATE tokens touched.
- build.sh re-checked after all work: md5
  4799a819791b9c3ec4c19136ad698397, 23,774 lines — unchanged.

## Known limitation (honest note)

- The block follows the fix22 pattern: its count==1 asserts guard against a
  *changed* anchor, not against re-application — re-running the block on an
  already-patched skill would duplicate the `after` insertions (verified in
  the `/tmp` simulation: second run exit 0). Idempotency is enforced where
  the task requires it: `apply-w4.py` refuses if the block marker is already
  present in build.sh, and build.sh applies the block once per build. Same
  property as the fix22 block; not a new hazard.

## Render-audit cross-check — DONE (results JSON landed)

`cold-start-render/home-run/qa/align-audit-results.json` LANDED during this
work (Nov 13, 02:58; 39 measurements = 13 states × 3 widths 1440/900/390;
all 39 screenshots present). Cross-checked measurement-by-measurement
against the assertion list defined from the SPEC. Findings:

- **PASS (supports the assertions):** `docOverflowX` = 0 at all 39
  measurements; text overflow = 0 elements; SVG label overlaps = 0,
  out-of-bounds = 0 (route map + branch strip); stamps offset 0; code-box
  group offset 0; feed cards share one left / one right edge per width
  (1440: 548/892; 900: 69/413; 390: 22/368); view children at offL 22 /
  offR 22 (narrow back-btn left-aligned, offR 286–296 — aligned, not a
  failure, which is why ALIGN_F23_GRID allows left-aligned narrow children).
- **Mid-band nuance (shaped ALIGN_F23_CENTER):** phone alone is −209px off
  center at 900, but the phone + left-panel group is centered (46px / 46px
  outer margins). A naive frame-only check would false-fail the mid band;
  the assertion therefore checks GROUP centering when side panels share
  the row. The 900 gutter/top-delta numbers (−808/−181/−872) are meaningless
  in the stacked layout and must not be asserted there — ALIGN_F23_PANELS
  says so explicitly.
- **Real flags the assertions would raise on this render:**
  (1) `.iris-disc` on trip states extends beyond the phone frame at ALL
  three widths (up to 82px past the edge at 390px) while page overflow
  stays 0 — passes ONLY if declared as intentional bleed in the decision
  record (ALIGN_F23_CLIP); (2) desktop side-panel top delta 26px at 1440
  (left 232 vs right 206) — passes ONLY if the stagger is recorded
  (ALIGN_F23_PANELS).
- **Within tolerance (not findings):** tab label-center deltas of 1px on
  two tabs at 390px only (≤ 2px tolerance); status-bar time/icons top
  delta of 5px with matching 27px/27px side insets — tops are not evidence,
  which is why ALIGN_F23_LABELS requires comparing vertical CENTERS.
- **Coverage confirmed by the audit itself:** all flow states incl.
  offer / offer-accepted / trip-wrongcode / trip-delivered were measured
  and screenshotted at all three widths — i.e. the audit already meets
  COVER_F23; the SPEC failure it fixes is that the ORIGINAL ship had only
  eyeballed 1440 screenshots and no mid-band or mobile flow-state shots.

## Not verified / owed

- Nothing owed on the cross-check: the results JSON landed and was fully
  cross-checked (above).
- `apply-w4.py` was NOT run (per task; integration runs it), so the block
  is not yet in build.sh and the built tree does not yet carry the §6 text.
  The audit loop / verify23.py / dry-run are the coordinator's job.
- One stale background full-tree grep (superseded by the targeted greps
  above) was terminated; its only purpose was token-novelty confirmation
  already established per-file.
