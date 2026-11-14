"""Fix #23 §4/§5 orchestrate lines (worker W3) — hero + functionality.

One string constant, ORCH_LINES_W3, holding the EXACT lines the
integration worker inserts mechanically into orchestrate's design-package
step (step 3). Do NOT edit orchestrate SKILL.md here — another worker owns
it; this file is the insertion payload.

INSERTION POINT (for the integration worker): orchestrate SKILL.md, step 3
(Slice), immediately AFTER the "Depth strategy in every UI slice brief
(fix #22 §13, DEPTH_F22)" paragraph and its D19 + theme-match lines, and
immediately BEFORE "**Two-pass briefing for UI slices:**". Insert the
constant verbatim as a new paragraph (blank line before and after), in the
same bold-lead style as the neighbouring step-3 paragraphs (Motion
principles / Accent hierarchy / Waiting states / Depth strategy).

The step-4 "Design package in every UI brief" restatement needs no
separate edit: it points back at step 3 ("same rule as step 3"), so these
lines govern it too.
"""

ORCH_LINES_W3 = """**Hero moment and functionality story in every UI slice brief (fix #23, HERO_F23 / FUNC_F23):** the brief also names the slice's hero moment and its functionality story, recorded in the decision record before any UI is built. **Hero moment:** the hero surface — a landing hero, or the home/feed surface of an app — gets a dealt amazing moment: a dealt moment + a distinctive composition + motion, with its fix #19 D19 reason (Taste HERO_F23). On a phone-first utility app the home/feed surface IS the hero surface and still gets the moment treatment, but the amazing bar is calibrated to the product — the moment must serve the product's job, not decorate it; "amazing" never means a generic hero section pasted onto an app that does not need one. The hero-moment line (moment + composition + motion values) is recorded in `docs/design-tokens.md` and in the Picks block (`.hallmark/picks.md`, Hero-moment row). The hero is the highest-weight `browser-qa` surface: a merely adequate hero fails F6. **Functionality story:** the brief states what is technically new here and how the design shows it — the mechanism (diagram / live data / system state) this build shows, visible early (on the hero surface or the first screen after it), theme-matched, naming THIS build's pipeline, data, and stack with the product's own names and real figures (Taste FUNC_F23; `diagrams.md`, FUNC-DIAG_F23). A build that looks good but hides what the thing does fails. A UI brief with no hero moment and no functionality story named is not ready to dispatch. (D19 — Motion: the hero moment's entrance and motion values, and the mechanism's live motion or `none — <reason>` where still; Theme: the moment and the mechanism are the dealt theme's material; Texture: the theme's treatment or `none — <reason>`; Visuals: the moment is the hero's distinctive composition, the mechanism is the section's picture; Techniques: the moment routes through the dealt moment and the hero deal, the mechanism through `diagrams.md` or the live-data surface; Colors: the theme's own tokens; Depth: the moment's and the mechanism's layer order, or `flat by choice — <reason>`.)"""
