# Typeset

Typeset is about whether the words are comfortable to read and whether their size, weight, and spacing tell you what each piece of text is. A designer looks for decisions: a real scale, deliberate weights, a readable measure, and type that survives every viewport, theme, and font load.

**Raises:** Typography.
**Skip it when:** the type is sound and the problem is structure (use layout) or copy (use clarify). Do not swap typefaces when DESIGN.md confirms them; improve their use instead. Replacing the brand's typeface is a DESIGN.md decision to confirm with the user — except during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature, where you do NOT confirm with the user: leave the brand typeface in place, improve its use instead, and record the replacement as blocked in the final report; never stop for a human decision mid-build.

## What a designer looks at

Open the Capture and look before touching code. Run these checks in order.

**1. The squint test.** Blur the screenshot (~8px).
- Can you still tell heading, body, label, and caption apart? If heading and body sizes are too close, they merge into one grey block.
- Is hierarchy carried by size alone? Good hierarchy combines size, weight, color, and space. Can you see ~3 text tints (heading near-black, body dark gray, subtext mid gray)?

**2. Count the sizes and weights.** Inventory every distinct font-size, weight, line-height, and letter-spacing in use, with where it appears. More than ~8 sizes or ~4 weights usually means no system; random font sizes are a sign nobody chose a scale. One weight everywhere means nothing is emphasized. One `letter-spacing` applied to every size is wrong somewhere: large text looks loose or tiny text looks cramped.

**3. Read a paragraph aloud.** Where do you lose your place?
- Lines longer than ~80 characters make the eye miss the next line.
- Cramped leading makes lines collide; loose leading makes a paragraph fall apart.
- Center-aligned paragraphs longer than 3 lines are hard to scan.
- Do accented, Vietnamese, or Thai lines collide or clip at the same leading as Latin text?

**4. Look at the defaults.** Is this default system or Inter styling with one weight and default tracking, with no visible decisions? If so, it looks generic. Are display or script faces used in buttons, labels, inputs, or data? Is monospace worn as a "techy" costume on non-code text?

**5. Check line breaks.** Does any heading wrap into a single orphan word? Does any text clip or overflow its container, especially long words and URLs?

**6. Look at the numbers.** In tables, prices, and timers, do digits jump in width as values change or fail to line up in columns? That means proportional numerals where tabular ones belong.

**7. Check the details.** Straight quotes ("), hyphens used for ranges, and all-caps paragraphs are signs of unfinished type.

**8. Watch it load.** Reload on a throttled connection. Does the layout jump when fonts load? Is there a flash of invisible text?

**9. Consider the Persona's reading context:** scanning a dashboard, reading long docs, or judging a landing page. Each wants a different scale: dashboards and product UI use smaller sizes with tighter steps; landing pages use bigger sizes with wider steps. Does large display text (≳ 70–80px) still have default tracking? It will look loose.

**10. Turn the text up.** Set the browser's default font size to 20px, then zoom to 200%. Does text scale, or is it locked in px? Does spacing scale with it, or do labels collide and containers clip?

## How to fix

1. **Read DESIGN.md's Design System typography:** families, weights, scale, and roles, plus the Personas' reading context.
2. **Define roles before values:** `display`, `h1`–`h3`, `body`, `body-sm`, `label`, `caption`, `mono`/`data`. Use the fewest roles that make hierarchy unmistakable.
3. **Choose a scale ratio by surface:**
   - task UIs (dashboards, tools, settings): 1.125–1.2, fixed rem sizes;
   - docs and articles: 1.2–1.25;
   - marketing and portfolios: 1.25–1.5, display may use `clamp()` (e.g. `clamp(2.5rem, 5vw + 1rem, 5rem)`).
4. **Set the values:**
   - body 16–18px (1rem–1.125rem); never below 16px for body on mobile (iOS zooms inputs under 16px); mobile web base ≈ 16–17px, and text often gets *bigger* on mobile, not smaller;
   - dense desktop app UI (tables, sidebars, toolbars) may use 13–14px for secondary/data text; reading body and all inputs stay ≥ 16px;
   - line-height runs inverse to size: body 1.5–1.7; headings 1.05–1.25; tighter as size grows; looser for scripts with tall ascenders or stacked diacritics; 1.4 allowed for dense UI text ≤ 14px;
   - prose `max-width: 60–70ch`;
   - tracking is size-specific, never one value for all sizes: display -0.01 to -0.03em (floor -0.04em), always applied to text ≳ 70–80px; body ≈ 0; small caps, labels, and tiny text (≤ 12px) slightly positive (+0.04 to +0.1em for caps);
   - weights: body 400, emphasis 500–600, headings 600–800; Lens target: adjacent roles differ by ≥ 200 weight or ≥ 1.25× size (above the craft-floor minimum of 1.125×);
   - tints: 3 text colors (heading, body, subtext) combined with weight and size for hierarchy;
   - set size, weight, and leading together per role; to emphasize inside a role, add weight before size.
5. **Pairing:** one family is often enough for task UIs. The system font stack (`system-ui`) is NOT a legitimate live path for a built page (fix #19 F2): a system font is a failure, not a fallback — the stack names bundled static faces only. A custom face needs a reason (brand voice, a job system fonts can't do); shipped files are static instances (one per weight, opsz baked in) — a variable font is the generation source only, never a shipped file. Set `font-optical-sizing: auto` on the static instances where the face ships an opsz axis.

**Body-only scope; important text gets the display face (fix #20).** The body face (Tiempos or the Fraunces stand-in) is for basic text only — a heading, hero line, call to action, or key label set in the body face is a finding. Important text uses the dealt display face; check the Type list for the face's fix #19 D19 reason and its fix #20 F6 justification (why it is the impressive choice for that surface) — a display face with no recorded justification is a finding. The squint test (check 1) is the visual proof: heading and body must read apart at a blur, by face as well as size.

**Long body and small text only; every text element gets an artistic font decision (fix #21).** The body face (Tiempos or the Fraunces stand-in) is for long-length body text and small incidental text only — a heading, hero line, call to action, key label, price, name, or prominent label set in the body face is a finding. Every text element needs a recorded artistic font decision (face + why + job + theme/brand fit) in the Type list — an element with no recorded decision is a finding, and a blanket 'all text' class line is not a decision. The squint test (check 1) is the visual proof: heading and body must read apart at a blur, by face as well as size. Add a second family only when it does a job the first cannot (display voice, code). Never more than two families plus mono.

**Type audit — the body face must never dominate (fix #23 §3, TYPEAUDIT_F23).** The Home Run lesson: all five static faces loaded and the record chose a real display face, yet Fraunces — the body face — carried the whole page by volume, because in an app most visible text IS body text. The type audit runs on every pass (SKILL.md non-negotiable 5) and records, per build, the distinct faces used, the share of visible text each face carries, and whether the trio matches the previous build's trio. It is candidate evidence for `browser-qa`, never a verdict — but its fail conditions are real: a hit with no recorded clearance is a FAIL that `browser-qa` turns into a build failure.

How to measure. A "face" is family + weight (Fraunces 400 and Fraunces 500 are two faces). From the Capture + computed styles (`getComputedStyle`), list every visible text element on each primary screen: element, role, rendered face, computed size in px, visible character count. **Visual share** of a face = Σ (size × visible characters) over that face's elements ÷ Σ over all faces — size × characters, not character count alone, because a 48px heading carries more of the visual field than a 14px meta row. Record per screen and as a build roll-up (summed across primary screens) in `docs/design-tokens.md` as the Type-audit table: face | roles | visual share % | element count. The trio is the three families named in the Type list as display, body, and data/mono (a build with no data face records the third as `none — <reason>`); the previous build's trio is the trio recorded in the same project's decision record from its most recent prior build — a first build records `previous trio: none (first build)` and passes the comparison.

Fail conditions (all checkable from the table):

- **T1a — body-face cap, build roll-up:** the body face carries ≤ 40% of the build's total visual share. Past 40% the display and data faces together no longer carry the majority of what the eye reads, and the body face IS the visual identity — the Home Run failure, where Fraunces carried the page by volume.
- **T1b — body-face cap, per screen:** the body face carries ≤ 55% on any single primary screen. One screen may be text-heavy; past 55% that screen's identity is the body face.
- **T1c — display floor, build roll-up:** the display/important face(s) combined carry ≥ 25% of the build's total visual share. Home Run's display face was dealt for display yet carried only headings — a small fraction. The floor forces display type into hero lines, names, prices, and key labels, not just H1s.
- **T1d — hero rule:** on the hero/home surface, the display face's share exceeds the body face's share. The hero is the highest-weight surface; if the body face leads there, the identity is the body face.
- **T2 — trio re-deal:** this build's trio identical to the previous build's trio → FAIL unless the decision record carries a recorded reason for the reuse — why this same trio is the right choice for THIS build, with a fix #19 D19 reason + theme-fit. The trio is re-chosen per build (Hallmark already deals type); the pairing must be re-dealt, not inherited (TRIO_F23, defined in orchestrate SKILL.md, fix #23 §3 — the trio is the display + body + data/mono families). A blanket "same trio as last time" line is not a reason.
- **T3 — variety floor:** distinct faces F ≥ max(3, ceil(N/20)), where N is the Type-list text-element row count — at least three faces (display, body, data/mono), plus one more face per 20 text elements past the first 20 (a 61-element build needs ≥ 4 faces). Each counted face must carry ≥ 5% of the build's visual share — a face used on one tiny label does not count toward variety. The ≤ 2 families (+ mono) rule still binds: the extra faces come from weights and styles within those families, never from a new family per element.

Clearance. A T1a/T1b hit is cleared ONLY by a scoped exception recorded in the decision record — a fix #19 D19 reason + theme-fit stating why THIS build must be body-led (a long-form reader surface is the honest case) — and T1c still binds under any exception: there is no clearance for a display face doing no work. A T2 hit is cleared only by the recorded reuse reason above. T1c, T1d, and T3 have no clearance: re-deal the trio or re-balance the shares — a reason does not substitute for display type doing the visible work. A cleared hit is recorded in the report with its reason cited, never silently dropped. Every hit with no clearance goes to `.hallmark/candidate-evidence.md` (screen + face shares + trio comparison + which threshold) for `browser-qa`, which alone renders the build verdict: a type-audit FAIL is a distinctiveness finding (minor at least) and fails the build, routed back to the design skill for a re-deal.

- **D19 (for the type audit)** — Motion: none — the audit measures type, not motion; Theme: every share is judged against the dealt theme's type voice — a face that fits the theme still fails the caps if it dominates; Texture: none — the audit measures faces, not surface treatment; Visuals: the visual-share metric IS the visual test — which face the eye actually reads most; Techniques: the audit routes to the Type list and the Capture's computed styles, never to a fresh font choice; Colors: none — the audit measures faces, not colours; Depth: none — the audit measures type, not the z-axis.

6. **Line breaks:** `text-wrap: balance` on headings and short centered text; `text-wrap: pretty` on paragraphs. Hand-break headings only between phrases, and check every viewport.
7. **Details:** `font-variant-numeric: tabular-nums` on tables, prices, timers; `lining-nums` in UI; real quotes and apostrophes (“ ” ’); en dash for ranges; `hyphens: auto` only on narrow justified or long-word text.
8. **Respect the user's text size:** font sizes in `rem`; spacing that sits around text in `rem`/`em` so it grows with it; no fixed px heights on text containers; the root font size is never set in px.
9. **Dark mode:** light text on dark reads heavier and tighter; add +0.02–0.05 line-height and +0.01em tracking, or drop one weight step if the face blooms.
10. **Loading:** load only used weights (woff2, subsetted), `font-display: swap` with a metric-matched fallback (`size-adjust`, `ascent-override`) so swap causes no visible shift; preload the 1–2 critical files.
11. **Record the scale as tokens in DESIGN.md** and replace every ad-hoc size with a role token.

## Rules
- [ ] Every text element maps to a named role; no stray px values.
- [ ] Measure `getComputedStyle(heading).fontSize` after fonts and styles settle in every route that renders it and every matrix cell. It must match the role's declared size (within 1px), or its declared fluid range. A declaration is not evidence when a generic heading selector wins the cascade; fix scope or specificity at the owning role, not by overriding library typography globally.
- [ ] Heading, body, label, and caption distinguishable in a blurred Capture.
- [ ] Body ≥ 16px, line-height 1.5–1.7 (1.4 for dense UI text ≤ 14px), headings 1.05–1.25, measure ≤ 75ch (dense desktop data/secondary text may be 13–14px; inputs never < 16px).
- [ ] Hierarchy uses 3 text tints + weight + size, not size alone.
- [ ] Display text ≳ 70–80px has negative tracking.
- [ ] No heading wraps to a single orphan word at any captured width.
- [ ] Tracking never below -0.04em; all-caps only on short labels with positive tracking.
- [ ] Tracking and line-height vary by role (negative tracking/tight leading on display, ≈ 0/looser on body, positive on tiny labels); no single global `letter-spacing`.
- [ ] Sizes and text-adjacent spacing in `rem`/`em`; a 20px browser default and 200% zoom don't break layout.
- [ ] A custom typeface has a stated reason; shipped font files are static instances (one per weight, opsz baked in) — no variable file is shipped, no `system-ui` fallback (fix #19 F2); the body face is used for long-length body text and small incidental text only, and important text uses the dealt display face with its recorded impressive-choice justification (fix #20); every text element has a recorded artistic font decision (fix #21 F7).
- [ ] ≤ 2 families (+ mono); ≤ 4 weights loaded.
- [ ] Type audit (TYPEAUDIT_F23) recorded: per-face visual shares per screen + build roll-up; body ≤ 40% roll-up and ≤ 55% per screen; display ≥ 25% roll-up; display > body on the hero/home surface.
- [ ] Trio re-dealt per build: this build's trio differs from the previous build's recorded trio, or the reuse carries a recorded D19 reason + theme-fit.
- [ ] Variety: distinct faces ≥ max(3, ceil(N/20)) for N Type-list text elements, each counted face ≥ 5% visual share; ≤ 2 families (+ mono) still binds.
- [ ] Tabular numerals wherever numbers align or change.
- [ ] Text zooms to 200% without clipping or overlap.
- [ ] Display, figure and label type fills its bubble (glyph box ≥ 60% of the container's inner size); no dead space, no overflow, no crowding (fix #17 T1).
- [ ] Font loading causes no visible layout shift (CLS contribution ≈ 0).

## Avoid
- Generic Inter-on-white with one weight and default tracking; if Inter is the choice, tune it.
- Display or script faces in buttons, labels, inputs, or data.
- Monospace as a "techy" costume for non-code text.
- Fluid `clamp()` sizes on dense app UI; they shrink unpredictably in panels.
- Gradient text and all-caps paragraphs.
- Center-aligned paragraphs longer than 3 lines.
- Using size alone for hierarchy; combine size, weight, color, and space.
- One `letter-spacing` value for every size; px font sizes that ignore the user's setting.
- `overflow: hidden` plus tight leading on text that may contain tall scripts.

## Verify in the Capture Matrix
- **Desktop light/dark:** blur the Capture; roles still separate. Check dark-mode weight and leading compensation.
- **Mobile light/dark:** headings wrap cleanly at 375px and 320px; body stays ≥ 16px; long words and URLs wrap instead of overflowing.
- Test real copy, the longest localized string you can find, and 200% zoom.
- Typography should rise with no overflow regressions.
- Fill (fix #17 T1): display, figure and label type inside a bounded container fills it (glyph box ≥ 60% of the container's inner size along the fill axis); a bubble, card, or tile whose largest empty band exceeds 25% of its minor dimension is a finding, fed to the fix batch like other checks.
