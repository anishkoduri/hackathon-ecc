# Fix #22 Group G — disposition (20 design terms)

Method: word-boundary greps with hyphen lookarounds
(`grep -P -i '(?<![\w-])<term>(?![\w-])'`), run Nov 12, 2026 over
`build.sh`, the built tree (`hackathon-ecc/`), and the staged sources
(`new-skills/` + `round2-skills/`). Hyphen-joined compounds do NOT count
as coverage. Raw grep output saved at `fix22/g-baseline-grep.txt`
(script: `fix22/g-baseline-grep.sh`). Classification: **new as vocabulary**
= the term never appears; **partial** = the word/phrase or the underlying
concept appears somewhere (rule, checklist, incidental use, or a bare name
in a list) but there is NO one-line definition anywhere — the glossary
definition is still new in every case. No term was already defined.

Glossary: `new-skills/design-taste-frontend/references/design-glossary.md`
(anchor `GLOSSARY_F22`). Pointer specs: `fix22/g-pointers.md`.

| Item | Baseline | Placement (glossary + owning skill) | Status |
|---|---|---|---|
| G1 Kerning | New as vocabulary. 0 hits build.sh / built tree / staged (word-boundary). | Glossary G1 + ui-ux-pro-max (font rules / type scale), pointer P-G1 | Defined; pointer spec P-G1 |
| G2 Optical centre | New as vocabulary. 0 hits everywhere (word-boundary; neither "centre" nor "center" spelling). | Glossary G2 + ui-ux-pro-max (font rules / type scale), pointer P-G1 | Defined; pointer spec P-G1 |
| G3 Tabular numbers | Partial. "Tabular numbers" itself 0 hits; "tabular numerals" used, not defined: polish-pass `reference/lenses/typeset.md:80` checklist, `reference/lenses/layout.md:78`, hallmark `references/gates.md:183` (F6), themes editorial/garden/riso. 6 staged-md hits / 8 built. Dedupe D18: primary ui-ux-pro-max type rules + glossary G3. | Glossary G3 + ui-ux-pro-max (type rules), pointer P-G1 | Defined; pointer spec P-G1 |
| G4 Layout shift | Partial. Concept covered as a QA flag + motion rule, term not defined: `build.sh:21236,21241` ("Flag layout shifts > 5px"), `build.sh:23242` ("must never cause layout shift"); staged: polish-pass `reference/lenses/animate.md:25,99`, `optimize.md:92`, `typeset.md:83`, Taste `references/perf.md:28`. 3 build.sh / 34 built / 15 staged hits. | Glossary G4 + ui-ux-pro-max + existing layout-shift QA flag, pointer P-G1 | Defined; pointer spec P-G1 |
| G5 Tracking | Partial. Type sense used, not defined: polish-pass `reference/lenses/typeset.md:51,63,73,76` (tracking values per role), Taste `SKILL.md:252` (Type-list tracking column), `references/layout-v4.md:251,260`. Other word-boundary hits are non-type uses (e.g. cost/event tracking) and were inspected, not counted as type coverage. 32 staged-md hits. | Glossary G5 + ui-ux-pro-max (font rules / type scale), pointer P-G1 | Defined; pointer spec P-G1 |
| G6 Optimistic update | Partial. Rule exists, term not defined: polish-pass `reference/lenses/optimize.md:23,69,88` ("use an optimistic update (rolled back visibly on failure) for low-risk actions"). 5 staged-md hits / 12 built. | Glossary G6 + ui-ux-pro-max, pointer P-G1 | Defined; pointer spec P-G1 |
| G7 x-height | Partial. Term used incidentally once, not defined: hallmark `references/gates.md:183` (F11, "a highlighter band at the baseline instead of behind the x-height"). Remaining built hits are the same gates file / theme files / a consistency script. 4 staged-md hits. | Glossary G7 + ui-ux-pro-max (font rules / type scale), pointer P-G1 | Defined; pointer spec P-G1 |
| G8 Touch target | Partial. Rule exists, term not defined as vocabulary: polish-pass `reference/craft-floor.md:74` (touch targets >= 44x44px, Fitts' law), `reference/impeccable-critique.md:755`, ui-ux-pro-max `data/app-interface.csv:7,8`, `rules/react-native-accessibility.mdc:34,36`. 4 staged-md hits / 65 built. Dedupe A14: primary is the existing hit-area rule, now named Fitts's law (A13); glossary G8 points at it. | Glossary G8 + ui-ux-pro-max, pointer P-G1 | Defined; pointer spec P-G1 |
| G9 Leading | Partial. Type sense used, not defined: polish-pass `reference/lenses/typeset.md:20,22,54,76` ("Cramped leading makes lines collide..."). Other hits are JSON `"leading": 1.02` line-height values and "leading edge" prose — inspected, not type definitions. 12 staged-md hits / 110 built (mostly JSON values). | Glossary G9 + ui-ux-pro-max (font rules / type scale), pointer P-G1 | Defined; pointer spec P-G1 |
| G10 Origin-aware animation | Partial. The full phrase 0 hits; standalone "origin-aware" is only NAMED, not defined: polish-pass `reference/patterns/motion-recipes.md:102` (vocabulary list: "Use exact names when describing motion: ... origin-aware ...") and `reference/scoring.md:25`. Dedupe B11/B12: primary motion-patterns (enter/exit from the trigger). | Glossary G10 + motion-patterns, pointer P-G3 | Defined; pointer spec P-G3 |
| G11 OKLCH | Partial. The `oklch()` color function is used ~1,015 times in staged sources (CSS/JS color values) and the space is named in passing (Taste `references/system.md:85`, `references/backgrounds.md:91`); there is NO definition of what OKLCH is anywhere. The glossary definition is new. | Glossary G11 + ui-ux-pro-max (color tokens), pointer P-G1 | Defined; pointer spec P-G1 |
| G12 Widow | New as vocabulary. 0 hits build.sh / built tree / staged (word-boundary). | Glossary G12 + ui-ux-pro-max (font rules / type scale), pointer P-G1 | Defined; pointer spec P-G1 |
| G13 Safe area | Partial. Covered only as a pointer + a platform rule, term not defined: `build.sh:13129,13145` (ui-ux-pro-max: "app-specific polish rules ... safe areas", `references/pro-rules.md`); polish-pass `reference/lenses/adapt.md:68,69,87` (`viewport-fit=cover`, `env(safe-area-inset-*)`), `reference/patterns/mobile-web.md:53`. 2 build.sh / 38 built / 4 staged-md hits. | Glossary G13 + ui-ux-pro-max + `references/pro-rules.md`, pointer P-G1 | Defined; pointer spec P-G1 |
| G14 Stagger | Partial. Technique exists, glossary definition new: motion-patterns stagger-list example + rule 5 (0.05s–0.10s interval), polish-pass `reference/lenses/animate.md:74` (stagger siblings 30–50ms), `reference/patterns/motion-recipes.md:55,102`. 6 build.sh / 100 built / 46 staged hits. Dedupe B3/B6: primary motion-patterns stagger example + 30ms token + glossary G14. | Glossary G14 + motion-patterns, pointer P-G3 | Defined; pointer spec P-G3 |
| G15 Line length | Partial. Concept exists as caps, term not defined: polish-pass `reference/lenses/layout.md:72` (`max-width: 65ch` on prose), `reference/lenses/adapt.md:73` (prose blocks cap line length at <= 75ch). 3 staged hits / 7 built. | Glossary G15 + ui-ux-pro-max (font rules / type scale), pointer P-G1 | Defined; pointer spec P-G1 |
| G16 Affordance | Partial. Used incidentally, not defined: polish-pass `reference/lenses/adapt.md:61` ("horizontal scroll container with a visible affordance"), `reference/lenses/polish-details.md`. 2 staged-md hits / 13 built (rest are data CSVs). | Glossary G16 + ui-ux-pro-max, pointer P-G1 | Defined; pointer spec P-G1 |
| G17 Combobox | Partial. Used as a control type, not defined: polish-pass `reference/patterns/forms.md:52,137` ("Combobox with type-to-filter..."), `reference/polish.md:50`. 3 staged-md hits / 21 built. | Glossary G17 + ui-ux-pro-max, pointer P-G1 | Defined; pointer spec P-G1 |
| G18 Interruptible animation | Partial. Rule exists, term not defined: polish-pass `reference/lenses/animate.md:71,96` ("Make it interruptible: use CSS transitions..."), `reference/patterns/motion-recipes.md:71,87,102`, `reference/scoring.md:25`. 6 staged-md hits / 9 built. Dedupe B14: related to "don't tween while held", keep both, cross-reference. | Glossary G18 + motion-foundations, pointer P-G2 | Defined; pointer spec P-G2 |
| G19 Progressive disclosure | Partial. Used, not defined: polish-pass `reference/lenses/distill.md:61`, `reference/impeccable-critique.md:286,303,321,333,349`, `reference/impeccable-onboard.md:44,228`, `reference/scoring.md:49`; ui-ux-pro-max rule table row 8. 9 staged-md hits / 21 built. | Glossary G19 + ui-ux-pro-max, pointer P-G1 | Defined; pointer spec P-G1 |
| G20 Shared element transition | Partial. Named once in a vocabulary list, not defined: polish-pass `reference/patterns/motion-recipes.md:102` ("Use exact names when describing motion: ... shared element transition ..."). 1 staged-md hit / 1 built. Dedupe B20: primary motion-patterns shared-element example (`layoutId`) + glossary G20; B20 points at it. | Glossary G20 + motion-patterns, pointer P-G3 | Defined; pointer spec P-G3 |

## Summary

- 20/20 terms defined in the glossary (one line each: definition + owning skill).
- Baseline: 3 new as vocabulary (G1, G2, G12); 17 partial (concept/rule/name
  exists somewhere, definition new in every case). 0 already defined.
- Pointer specs: 3 (P-G1 ui-ux-pro-max, P-G2 motion-foundations, P-G3
  motion-patterns) in `fix22/g-pointers.md`; all anchors verified count == 1
  in the current built tree (re-verify at apply time).
- No SPEC deviations. No `build.sh` edit, no built-tree edit, no new skill,
  no enforcement added for any term, font rules / screen-verdicts rule /
  model pins untouched.
