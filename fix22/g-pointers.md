# Fix #22 Group G — owning-skill pointer specs (integrator applies)

Glossary file: `new-skills/design-taste-frontend/references/design-glossary.md`
(anchor token `GLOSSARY_F22`). Terms are NOT duplicated into the owning
skills — each owning skill gets ONE pointer line (below). The integrator
applies these; do NOT edit `build.sh` in this file, do NOT edit the built
tree directly.

All three owning skills are upstream skills with NO staged source in this
repo (`ui-ux-pro-max` is cloned from upstream and copied by `build.sh`;
`motion-foundations` / `motion-patterns` are ECC skills). Apply each pointer
as a `build.sh` patch block in the fix20/fix21 pattern (per-file entry,
assert the anchor occurs exactly once in the target file before inserting).
Anchor counts below were verified against the current built tree
(`hackathon-ecc/skills/<skill>/SKILL.md`) on Nov 12, 2026 — re-verify at
apply time, since the Group A agent also edits `motion-foundations`
(Principles / Decision Guidance sections only — NOT the Related Skills
anchors used here, but re-check the count anyway).

## P-G1 — ui-ux-pro-max (covers G1, G2, G3, G4, G5, G6, G7, G8, G9, G11, G12, G13, G15, G16, G17, G19)

- Target file (built tree): `skills/ui-ux-pro-max/SKILL.md`
- Anchor text (verbatim, count == 1 in the built file):

  `For the full rule list per category (all 120 UX guidelines with rationale), read `references/quick-reference.md`. For app-specific polish rules (icons, touch feedback, dark mode contrast, safe areas) and the canonical pre-delivery checklist, read `references/pro-rules.md`.`

- Where: insert the new pointer line immediately AFTER that paragraph
  (after its line, before the blank line and the `---` rule that follows it).
- New pointer line (verbatim, one line):

  `Design vocabulary — the definitions of kerning, optical centre, tabular numbers, tracking, x-height, leading, widow, line length, optimistic update, touch target, affordance, combobox, progressive disclosure, layout shift, safe area, and OKLCH live in `skills/design-taste-frontend/references/design-glossary.md` (`GLOSSARY_F22`); this skill applies those concepts, the glossary defines them.`

## P-G2 — motion-foundations (covers G18)

- Target file (built tree): `skills/motion-foundations/SKILL.md`
- Anchor text (verbatim, count == 1 in the built file, in `## Related Skills`):

  `- **`motion-patterns`** — consumes tokens and springs defined here to build button, modal, stagger, page transition, and scroll patterns. Does not redefine any values.`

- Where: insert the new pointer line immediately AFTER that bullet line,
  inside the `## Related Skills` section (before the `motion-advanced` bullet).
- New pointer line (verbatim, one line):

  `Design vocabulary — the definition of interruptible animation (G18) lives in `skills/design-taste-frontend/references/design-glossary.md` (`GLOSSARY_F22`); this skill applies the concept, the glossary defines it.`

## P-G3 — motion-patterns (covers G10, G14, G20)

- Target file (built tree): `skills/motion-patterns/SKILL.md`
- Anchor text (verbatim, count == 1 in the built file, in `## Related Skills`):

  `- **`motion-foundations`** — defines all tokens, springs, the `useSafeMotion` hook, and SSR guards that every pattern here imports. Must be set up first.`

- Where: insert the new pointer line immediately AFTER that bullet line,
  inside the `## Related Skills` section (before the `motion-advanced` bullet).
- New pointer line (verbatim, one line):

  `Design vocabulary — the definitions of origin-aware animation (G10), stagger (G14), and shared element transition (G20) live in `skills/design-taste-frontend/references/design-glossary.md` (`GLOSSARY_F22`); this skill applies those concepts, the glossary defines them.`

## Term → pointer map

| Term | Pointer spec |
|---|---|
| G1 Kerning, G2 Optical centre, G3 Tabular numbers, G5 Tracking, G7 x-height, G9 Leading, G12 Widow, G15 Line length | P-G1 (ui-ux-pro-max) |
| G6 Optimistic update, G8 Touch target, G16 Affordance, G17 Combobox, G19 Progressive disclosure | P-G1 (ui-ux-pro-max) |
| G4 Layout shift, G13 Safe area | P-G1 (ui-ux-pro-max) |
| G11 OKLCH | P-G1 (ui-ux-pro-max) |
| G10 Origin-aware animation, G14 Stagger, G20 Shared element transition | P-G3 (motion-patterns) |
| G18 Interruptible animation | P-G2 (motion-foundations) |
