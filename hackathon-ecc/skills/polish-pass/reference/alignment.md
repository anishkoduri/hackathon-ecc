# Alignment checklist — candidate evidence for browser-qa (fix #23 §6, ALIGN_F23)

Status: **candidate evidence only — never a verdict.** This checklist is what
`polish-pass` measures and records per screen; `browser-qa` alone issues
pass/fail verdicts on rendered screens (screen-verdicts rule, fix #13e).
Findings go to `.hallmark/candidate-evidence.md` (screen + measurement +
screenshot) the same way slop findings are recorded.

The failure this fixes (SPEC §6): the Home Run render shipped with alignment
verified only by eyeballing screenshots. The 768–1100px layout was never
screenshotted; mobile flow states (offer / accepted / delivered / wrong-code)
were never screenshotted. Eyeballing is not a check.

## Tolerances

- **0px** for overflow: any horizontal overflow, any text overflowing its
  container, any element escaping the page is a fail.
- **≤ 2px** for centering / grid / spacing equality: sub-pixel rounding and
  the 1px label-center deltas the Home Run audit measured at 390px are
  rounding, not misalignment. Anything above 2px is a fail.
- Measure geometry from `getBoundingClientRect()` on the live rendered page
  (the Home Run audit harness, `cold-start-render/home-run/qa/align-audit.mjs`,
  is the measurement model: `docOverflowX`, frame center offset, gutters,
  panel top deltas, view-children offsets, card edges, tab rects, text
  overflow, beyond-frame elements, stamp offsets, SVG label boxes).
  Never judge alignment from source code or from a screenshot alone.

## The assertion list (browser-qa executes these; polish-pass records the evidence)

### ALIGN_F23_OVERFLOW — no horizontal overflow at any tested width

- `document.documentElement.scrollWidth - window.innerWidth == 0` at every
  tested width. Any positive value fails.
- No leaf text element has `scrollWidth > clientWidth + 1` (clipped /
  overflowing text). The Home Run audit found zero such elements at all
  three widths — that is the bar.

### ALIGN_F23_CENTER — the hero / phone frame is centered in the viewport

- Desktop 1440 and mobile 390: frame center offset from the viewport center
  ≤ 2px. (Home Run audit: 0px at both.)
- Mid band 768–1100 (default probe 900): if side panels share the row with
  the frame, the **hero group** (frame + side panels) must be centered —
  equal outer margins ≤ 2px — not the frame alone. The Home Run audit at 900
  measured the phone alone at −209px but the phone + left-panel group at
  46px / 46px margins: group-centered passes, a naive frame-only check
  would false-fail. If no side content shares the row, the frame alone
  must be centered ≤ 2px.

### ALIGN_F23_NAV — nav items evenly spaced and centered

- Adjacent nav-item gaps equal within 2px; the nav group as a whole centered
  in its bar (group center offset ≤ 2px).
- Each nav item's label center equals the item's own center within 2px.
  (Home Run audit: 1px deltas on two tabs at 390px only — inside tolerance.)

### ALIGN_F23_GRID — card edges aligned to a common left/right grid

- Full-width children of a view share one left edge and one right edge,
  equal to the view padding within 2px. (Home Run audit: every view child
  at `offL 22 / offR 22`.)
- A narrower child must be either left-aligned (`offL` == padding ± 2px)
  or centered (`offL` == `offR` ± 2px). A narrow left-aligned child (e.g.
  a back button with a far right edge) is aligned, not a failure.
- Feed / list cards: one shared left edge and one shared right edge across
  ALL cards at a given width. (Home Run audit: a single left and a single
  right per width.)

### ALIGN_F23_CLIP — no text clipped, no element escaping its frame

- No text clipped or overflowing its container (see ALIGN_F23_OVERFLOW).
- No element extends beyond its frame — **unless it is a declared
  intentional bleed recorded in the decision record**, and the page-level
  overflow is still 0. The Home Run audit found one such element:
  `.iris-disc` on the trip states extends beyond the phone frame at all
  three widths (up to 82px past the edge at 390px) while page overflow
  stays 0. Undeclared, that is a fail; declared in the decision record as
  intentional bleed, it passes with the declaration cited.

### ALIGN_F23_LABELS — no label collisions (diagrams, strips, stamps)

- SVG / diagram text boxes: pairwise non-overlapping, and all inside the
  SVG viewport. (Home Run audit: route map and branch strip, 0 overlaps,
  0 out of bounds.)
- Stamps / rotated labels: centered on their parent (center offset ≤ 2px).
  (Home Run audit: 0px.)
- Status-bar-style pairs (time left, icons right): compare **vertical
  centers**, not tops — elements of different heights have different tops
  by construction. The Home Run audit recorded a 5px top delta with
  matching 27px / 27px side insets; tops alone are not evidence of
  misalignment, centers are the check.

### ALIGN_F23_ACTIONS — primary actions centered on their axis

- Grouped inputs (e.g. code boxes): the group's center equals its panel's
  center within 2px. (Home Run audit: offset 0 at all widths.)
- A full-width primary action shares the grid edges (ALIGN_F23_GRID); a
  narrower primary action is centered (`offL` == `offR` ± 2px).

### ALIGN_F23_PANELS — desktop side panels symmetric and top-aligned

- Desktop: left gutter equals right gutter within 2px. (Home Run audit
  at 1440: 44px / 44px.)
- Desktop: side-panel tops aligned within 2px **unless a stagger is
  recorded in the decision record**. The Home Run audit measured a 26px
  top delta at 1440 (left panel top 232, right panel top 206) — a flag
  unless the decision record records the stagger as deliberate.
- Mid band, stacked layout: gutter / top-delta metrics do not apply.
  Instead each stacked block is centered as a group (outer margins equal
  ± 2px, or block center == viewport center ± 2px), and a side-by-side
  row is judged by the group-centering rule (ALIGN_F23_CENTER).

## Coverage matrix (COVER_F23) — mandatory, every width × every state

Widths (three, mandatory):

| Band | Width | Note |
|---|---|---|
| Desktop | 1440 | viewport 1440×900 |
| Mid | 900 (default probe for the 768–1100 band) | viewport 900×900; if a layout breakpoint falls inside 768–1100, probe at the breakpoint ± 1 as well; take a full-page composition shot |
| Mobile | 390 | viewport 390×844 |

States (every flow state, not just the happy path): enumerate **all**
screens × **all** reachable states — including error / wrong-code, empty,
success / delivered, accepted, and scrolled positions — and measure +
screenshot each at all three widths. The Home Run audit is the template:
13 states × 3 widths = 39 measurements (home, home-bottom scrolled,
detail, offer, offer-accepted, trip, trip-wrongcode, trip-delivered,
branches, trips, you, post, post-done), one screenshot per
(width, state) plus a mid full-page shot.

## The blocking-gap rule (BLOCK_F23)

A build with an unverified width or an unverified flow state is **NOT
shippable** — the gap is a **blocking finding**, not a note. Missing
coverage → blocking finding → `browser-qa` verdict **DO NOT SHIP**.
A coverage matrix with an empty cell is never reported as SHIP, SHIP WITH
FIXES, or INCONCLUSIVE-as-pass; the matrix is complete or the build does
not ship. `polish-pass` records the gap as candidate evidence;
`browser-qa` alone issues the verdict.
