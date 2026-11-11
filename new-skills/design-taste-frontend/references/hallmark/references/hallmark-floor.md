<!-- Hallmark floor, condensed for this plugin.
Source: Nutlope/hallmark, MIT, v2.0.0, HEAD 7e213cb6feb4ef82733bd66a0600b2e54ca0994c.
Upstream: skills/hallmark/SKILL.md "The Floor" (16 non-waivable rules) +
references/gates.md §1-§2 (tiers). Condensed here so the landing slice can
read the Floor without loading Hallmark's whole build playbook (Taste owns
the build). Gate numbers are Hallmark's; where a rule duplicates this
plugin's own craft floor, the stricter ban wins. -->

# Hallmark floor (condensed)

These 16 rules bind every Hallmark-dealt landing page. None is waivable,
even when nothing else is read. Above the Floor, a **Reflex** gate is a
default a model falls into, waivable on the record with a real reason, and
a **Finish** check is craft detail, answered, never blocking
(`references/gates.md` §1-§2). The full gate list is 90 clauses across 71
numbers (14 retired, never reused) + 26 Finish checks F1-F26 — see
`references/gates.md` §4-§5. (Note: older write-ups say "57 gates"; that
count does not match v2.0.0.)

1. Every colour and every font goes through a token declared at `:root`
   (or a declared theme block). No literal colour or `font-family` past
   the token block. (48)
2. Never `transition: all`. Never animate `width`, `height`, `top` or
   `left`. (10a)
3. Never one italic word inside a roman heading. (38i)
4. `overflow-x: clip` on both `html` and `body`. Never `hidden`, never
   `100vw`. (34)
5. Image-bearing grid tracks use `minmax(0, 1fr)`; display heads carry
   `overflow-wrap: break-word; min-width: 0`. (50)
6. Every interactive element has `:focus-visible`, appearing instantly.
   (26a, 15)
7. Every animation has a `prefers-reduced-motion: reduce` fallback, and
   content is visible with scripting off. (27, 62)
8. Never an invented metric, testimonial, logo wall or case-study count.
   (46a)
9. Never an eyebrow, and never a label in tracked capitals or small caps:
   labels, captions, table heads, tags and nav links are the body face
   (or the theme's label face), a step smaller, sentence or lower case,
   untracked. (54, 67)
10. Never middle-dot-joined meta strings, arrows glued to link text, or
    decorative status dots. (63)
11. Never a purple-to-blue gradient, a card inside a card, an emoji as an
    icon, or a hand-drawn browser or OS window. (2a, 4, 30a, 47a)
12. The hero's headline, one sentence and primary action are all visible
    at 1280 x 800 without scrolling. (44b)
13. About 80 words on any one screen; the hero's text is the headline,
    one sentence and its actions. (58)
14. The container is capped and centred: at 1920 the gutters grow, the
    measure and the grids do not. (44d)
15. The first non-empty line of the CSS source is the Hallmark stamp,
    then the critique line, then any waivers. (20) — applies to files
    the landing slice writes on a Hallmark-dealt page, not to the whole
    codebase.
16. If Node is available, run `node <skill>/references/hallmark/scripts/sloplint.mjs <output> --render`
    before handing back. Fix every `FAIL`; fix or waive every `REFLEX`.
    (The render tier needs `puppeteer-core@25.17.0` + Chrome; without
    them run the static tier only and record that the render tier did
    not run.)

## The 6-axis pre-emit self-critique (gates.md §3)

Before the sweep, score the planned page 1-5 on six axes; anything under 3
triggers a revision first — under the Scope note below (Specificity is candidate evidence for `browser-qa`, never a verdict; only the five craft axes join the fix list). Stamp line:
`/* Hallmark · pre-emit critique: P5 H4 E5 S3 R5 V4 · weakest: S, <fix> */`
— name the weakest axis + the fix taken; straight 5s name what was cut.

**Scope:** the Specificity axis is candidate evidence for `browser-qa`, never a distinctiveness verdict (see gates.md §3); the other five axes join the fix list as craft judgments.

- **P**hilosophy — 3: has a tone; 5: has an argument a reader could
  disagree with.
- **H**ierarchy — 3: needs a second look; 5: survives the squint test.
- **E**xecution — 3: two or three loose details; 5: would pass the gates
  first time.
- **S**pecificity — 3: fits the category; 5: could belong to no other
  product.
- **R**estraint — 3: keeps one decoration too many; 5: lost something
  you liked.
- **V**ariety — 3: differs from the log on three of six structural axes;
  5: shares almost nothing with the last three runs.
