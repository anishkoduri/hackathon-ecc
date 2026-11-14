# Fix #22 — Disposition, Group A (20 UX & animation principles)

Baseline re-verified 2026-11-12 by the Groups A+B implementation agent with word-boundary
greps (`grep -P` with lookarounds) over `build.sh`, the built tree
(`hackathon-ecc/skills/...`), and the staged sources. The parent's substring greps had
false positives; every hit below was inspected.

Anchor tokens: PRINCIPLES_F22 (motion-foundations `## Principles`, A1–A12),
LAWS_F22 (motion-foundations Decision Guidance, A13–A20).

| Item | Baseline | Placement (skill + section + anchor) | Status |
|---|---|---|---|
| A1 Squash & stretch | NEW — word-boundary grep `squash` over build.sh: 0 hits | motion-foundations `## Principles` (PRINCIPLES_F22), patch AB-01 | Placed in patch spec |
| A2 Anticipation wind-up | NEW — `anticipation`: 0 hits | motion-foundations `## Principles` (PRINCIPLES_F22), AB-01; cross-ref B5/B19 (instances) | Placed in patch spec |
| A3 Staging the focus | NEW — `staging`: hits are all open-source staging dirs (`opensource-staging/`, `{STAGING_PATH}`), none about staging a focus | motion-foundations `## Principles` (PRINCIPLES_F22), AB-01 | Placed in patch spec |
| A4 Pose to pose | NEW — `pose to pose`: 0 hits | motion-foundations `## Principles` (PRINCIPLES_F22), AB-01 | Placed in patch spec |
| A5 Follow through | NEW — `follow through`: 0 hits | motion-foundations `## Principles` (PRINCIPLES_F22), AB-01 | Placed in patch spec |
| A6 Slow in & slow out | NEW — `slow in`: 0 hits | motion-foundations `## Principles` (PRINCIPLES_F22), AB-01; cross-ref B1/B9 (values in tokens, AB-03/AB-04) | Placed in patch spec |
| A7 Moving in arcs | NEW — `arcs`: 0 word-boundary hits. Note: motion-advanced SVG draw-on uses an arc-shaped path (`M 0 100 Q 50 0 100 100`) for drawing a path, not for moving an object along an arc — not coverage | motion-foundations `## Principles` (PRINCIPLES_F22), AB-01, points at B7; primary: motion-patterns Rules (AB-05 rule 19) | Placed in patch spec |
| A8 Secondary action | NEW — `secondary action`: 0 hits | motion-foundations `## Principles` (PRINCIPLES_F22), AB-01; cross-ref B6 (AB-06) | Placed in patch spec |
| A9 Snappy timing | NEW — `snappy timing`: 0 hits. Note: the `snappy` spring preset exists (a name, not the timing principle) | motion-foundations `## Principles` (PRINCIPLES_F22), AB-01 | Placed in patch spec |
| A10 Exaggerated feedback | NEW — `exaggerat`: 0 hits | motion-foundations `## Principles` (PRINCIPLES_F22), AB-01; one family with B8 (AB-05 rule 17) and D20 (other agent's item; D20 points here) | Placed in patch spec |
| A11 Solid drawing in 3D | NEW — `solid drawing`: 0 hits | motion-foundations `## Principles` (PRINCIPLES_F22), AB-01 | Placed in patch spec |
| A12 Overall appeal | NEW — `appeal`: 0 hits | motion-foundations `## Principles` (PRINCIPLES_F22), AB-01 | Placed in patch spec |
| A13 Fitts's law | NEW — `Fitts`: 0 hits | motion-foundations Decision Guidance `### UX laws that decide motion` (LAWS_F22), AB-02 | Placed in patch spec |
| A14 Bigger hit areas | PARTIAL — the size rule already exists: `make-interfaces-feel-better` Hit Areas ("at least a 44x44px hit area", built file line 135) and build.sh:22077/22080 (40x40px, ideally 44x44px). What is NEW is naming it as Fitts's law (A13) and giving the rule its rationale. The size rule is NOT duplicated | motion-foundations Decision Guidance (LAWS_F22), AB-02 — law + rationale + pointer to the existing rule | Placed in patch spec (naming + rationale only; no size-rule duplication) |
| A15 Hick's law | NEW — `Hick`: 0 hits | motion-foundations Decision Guidance (LAWS_F22), AB-02 | Placed in patch spec |
| A16 Miller's law | NEW — `Miller`: 0 hits | motion-foundations Decision Guidance (LAWS_F22), AB-02 | Placed in patch spec |
| A17 Doherty threshold | NEW — `Doherty`: 0 hits | motion-foundations Decision Guidance (LAWS_F22), AB-02 | Placed in patch spec |
| A18 Postel's law | NEW — `Postel`: 0 hits | motion-foundations Decision Guidance (LAWS_F22), AB-02 | Placed in patch spec |
| A19 Jakob's law | NEW — `Jakob`: 0 hits | motion-foundations Decision Guidance (LAWS_F22), AB-02 | Placed in patch spec |
| A20 Frequency of use | NEW — `frequency of use`: 0 hits | motion-foundations Decision Guidance (LAWS_F22), AB-02 | Placed in patch spec |

Cross-pointers (also placed in patch spec):
- make-interfaces-feel-better: motion feel decisions route through the principles — AB-11.
- orchestrate design-package step (step 3, staged file `new-skills/orchestrate/SKILL.md`
  line 62): the design package must name which principles the build leans on, recorded
  in the decision record — DIRECT EDIT, applied 2026-11-12 (see report for exact text).
- ui-ux-pro-max: pointer to the laws only, no duplicated law texts — AB-12.

Coverage: 20/20 accounted for (19 new + 1 partial, A14). Zero already-covered, zero dropped.
