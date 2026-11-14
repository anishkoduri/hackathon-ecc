# Fix #15 — baseline: design-element count for the Campus Eats cold-start build

Source: the Campus Eats cold-start dry-run (dry-run #24 trace) + the direction recorded
in `~/workspace/cold-start-render/campus-eats/docs/design-tokens.md` (as written
2026-11-11, BEFORE the separate artifact edit adding more elements — the artifact
itself is out of scope for this program and must not be touched).

## Definition — what counts as one design element

One discrete, deliberate design application in a build, recorded in
`docs/design-tokens.md` (dealt items also in `.hallmark/picks.md`). One application =
one count. Instances count individually (3 spot rows = 3; 4 Bento tiles = 4).
Each element is classified into exactly ONE kind, by this precedence
(first match wins):

1. **Moment** — a dealt moment applied (letters-assemble, iris-opens,
   photo-chapters, word-highlight, pinned-chapters, picture-develops, etc.)
2. **Effect** — a shader ground, CSS ground, lit ground, scene, or WebGL part
3. **Visual** — a photograph frame, UI fragment, app-frame window,
   product render, key art
4. **Diagram** — a diagram card (hub, lanes, pulses) or still diagram
5. **Treatment** — a less-flat-ui treatment application on ONE surface
   (per the Treatments record in design-tokens.md)
6. **Component** — a distinct functional UI piece (button pair, nav form,
   footer form, stepper control, price ladder, tag/chip, spot row, fill tile,
   step card)
7. **Motion** — a hero entrance, hover layer, card loop, count, or other
   authored motion element
8. **Type** — a type-led element BEYOND a section heading: a lone figure,
   a statement set large, an oversized numeral

What does NOT count: copy words, sections as such, the theme itself (the theme
is the direction, not an element), a dealt item with no recorded application.

## Baseline enumeration — Campus Eats landing page (25 elements)

Hero:
1. news pill — Component
2. button pair (primary + ghost) — Component
3. app-frame window — Visual
4. search bar (inside app-frame) — Component
5. spot row 1 (tacos) — Component
6. spot row 2 (burger) — Component
7. spot row 3 (coffee) — Component
8. floating card 1 — Treatment (Soft Shadow)
9. floating card 2 — Treatment (Soft Shadow)
10. hero entrance — Motion
11. hover layer (page-wide) — Motion

Bento (4 tiles):
12–15. tile x4 — Component

Steps (3 cards):
16–18. step card x3 — Component

Lime field:
19. budget stepper — Component
20. running total (Bowlby figure) — Type
21. threshold bar — Component
22. price ladder card — Component

Ink band:
23. ink-band statement — Moment (letters-assemble)
24. pink corner tag — Component

Footer:
25. footer (footer-dark) — Component

## Baseline by kind

| Kind | Count |
|---|---|
| Component | 18 |
| Treatment | 2 |
| Visual | 1 |
| Motion | 2 |
| Moment | 1 |
| Type | 1 |
| Effect | 0 |
| Diagram | 0 |
| **Total** | **25** |

## Baseline gaps (dealt but NOT applied — not counted)

- iris-opens: second dealt moment, no recorded application anywhere.
- Hero window loop: the centred-hero spec's loop inside the window, no recorded
  application anywhere.
- No Diagram, no Effect applied on this build (none was required by any rule).

## Target

**+4 to +5 elements (+16% to +20% of 25), spread across at least 4 kinds,
every one theme-matched.** A rise that is all one kind does not satisfy the
brief. The "after" count is measured by re-tracing the same Campus Eats build
under the new rules with this same counting rule — not by counting the edited
artifact (out of scope) and not by assertion.
