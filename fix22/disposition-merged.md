# Fix #22 — Merged disposition (144 items)

Built from the six source dispositions after the post-fix22 rebuild (`bash build.sh`, exit 0; build.sh 23,732 lines, md5 `891fca7b5f34aa74db95cb04501345a0`; built tree 166 skills / 72 agents / 123 rules / 87 commands / 15 hooks; 64 trigger keys). Every placement below is a file:line in the REBUILT tree (`hackathon-ecc/`), located by anchor grep — not copied from the pre-build staged line numbers in the source dispositions.

Status vocabulary: **new** (did not exist), **partial** (mechanism existed, the rule/value/wording is new), **covered** (already existed, no new text), **pointer** (points at an existing home, does not restate), **verification-only** (verified present, no text copied).

| Item | Placement (built tree) | Status | Source |
|---|---|---|---|
| A1 Squash & stretch | `skills/motion-foundations/SKILL.md:52` — motion-foundations Principles (PRINCIPLES_F22), AB-01 | new | disposition-A.md |
| A2 Anticipation wind-up | `skills/motion-foundations/SKILL.md:56` — motion-foundations Principles (PRINCIPLES_F22), AB-01 | new | disposition-A.md |
| A3 Staging the focus | `skills/motion-foundations/SKILL.md:60` — motion-foundations Principles (PRINCIPLES_F22), AB-01 | new | disposition-A.md |
| A4 Pose to pose | `skills/motion-foundations/SKILL.md:63` — motion-foundations Principles (PRINCIPLES_F22), AB-01 | new | disposition-A.md |
| A5 Follow through | `skills/motion-foundations/SKILL.md:67` — motion-foundations Principles (PRINCIPLES_F22), AB-01 | new | disposition-A.md |
| A6 Slow in & slow out | `skills/motion-foundations/SKILL.md:70` — motion-foundations Principles (PRINCIPLES_F22), AB-01 | new | disposition-A.md |
| A7 Moving in arcs | `skills/motion-foundations/SKILL.md:73` — motion-foundations Principles (PRINCIPLES_F22), AB-01 | new | disposition-A.md |
| A8 Secondary action | `skills/motion-foundations/SKILL.md:76` — motion-foundations Principles (PRINCIPLES_F22), AB-01 | new | disposition-A.md |
| A9 Snappy timing | `skills/motion-foundations/SKILL.md:79` — motion-foundations Principles (PRINCIPLES_F22), AB-01 | new | disposition-A.md |
| A10 Exaggerated feedback | `skills/motion-foundations/SKILL.md:83` — motion-foundations Principles (PRINCIPLES_F22), AB-01 | new | disposition-A.md |
| A11 Solid drawing in 3D | `skills/motion-foundations/SKILL.md:87` — motion-foundations Principles (PRINCIPLES_F22), AB-01 | new | disposition-A.md |
| A12 Overall appeal | `skills/motion-foundations/SKILL.md:90` — motion-foundations Principles (PRINCIPLES_F22), AB-01 | new | disposition-A.md |
| A13 Fitts's law | `skills/motion-foundations/SKILL.md:217` — motion-foundations Decision Guidance laws (LAWS_F22), AB-02 | new | disposition-A.md |
| A14 Bigger hit areas | `skills/motion-foundations/SKILL.md:225` — motion-foundations Decision Guidance laws (LAWS_F22), AB-02; names the existing 44x44px rule (Fitts's law), no size-rule duplication | partial | disposition-A.md |
| A15 Hick's law | `skills/motion-foundations/SKILL.md:236` — motion-foundations Decision Guidance laws (LAWS_F22), AB-02 | new | disposition-A.md |
| A16 Miller's law | `skills/motion-foundations/SKILL.md:244` — motion-foundations Decision Guidance laws (LAWS_F22), AB-02 | new | disposition-A.md |
| A17 Doherty threshold | `skills/motion-foundations/SKILL.md:252` — motion-foundations Decision Guidance laws (LAWS_F22), AB-02 | new | disposition-A.md |
| A18 Postel's law | `skills/motion-foundations/SKILL.md:262` — motion-foundations Decision Guidance laws (LAWS_F22), AB-02 | new | disposition-A.md |
| A19 Jakob's law | `skills/motion-foundations/SKILL.md:271` — motion-foundations Decision Guidance laws (LAWS_F22), AB-02 | new | disposition-A.md |
| A20 Frequency of use | `skills/motion-foundations/SKILL.md:281` — motion-foundations Decision Guidance laws (LAWS_F22), AB-02 | new | disposition-A.md |
| B1 Ease-out for entrances | `skills/motion-foundations/SKILL.md:124` — motion-foundations Rules rule 11 (AB-04); token `smooth` annotated B1, :313 | partial | disposition-B.md |
| B2 Dropdowns at 150–250ms | `skills/motion-foundations/SKILL.md:306` — motion-foundations token `dropdown: 0.2`; Dropdown example in motion-patterns (AB-06) | new | disposition-B.md |
| B3 Stagger list rows by 30ms | `skills/motion-foundations/SKILL.md:307` — motion-foundations token `staggerRow: 0.03`; CONFLICT FLAG: 30ms below Rule 5's 0.05s floor, parent adjudicates | partial | disposition-B.md |
| B4 Scale to 0.97 on press | `skills/make-interfaces-feel-better/SKILL.md:118` — make-interfaces-feel-better press default; no new text. OBSERVATION: motion-foundations `scale.press` is 0.95, not the 0.97 default — neither value changed | covered | disposition-B.md |
| B5 Stretch moving knobs 12% | `skills/motion-foundations/SKILL.md:330` — motion-foundations token `stretch: 1.12`; Stretching knob example in motion-advanced (AB-10) | new | disposition-B.md |
| B6 Stagger as details settle | `skills/motion-patterns/SKILL.md:230` — motion-patterns note after the Stagger list example (AB-06); cross-ref A8 | partial | disposition-B.md |
| B7 Arcs for object movement | `skills/motion-patterns/SKILL.md:93` — motion-patterns Rules rule 19 (AB-05); primary home, A7 points at it | new | disposition-B.md |
| B8 Pulse to confirm success | `skills/motion-patterns/SKILL.md:82` — motion-patterns Rules rule 17 (AB-05); cross-ref A10 | partial | disposition-B.md |
| B9 Ease-in-out for moves | `skills/motion-foundations/SKILL.md:317` — motion-foundations token `inOut: [0.65, 0, 0.35, 1]`; Rules rule 12 (AB-04) | new | disposition-B.md |
| B10 Start popovers at 0.95 | `skills/motion-foundations/SKILL.md:329` — motion-foundations token `popover: 0.95` (separate token, never merge with press); Popover example in motion-patterns (AB-07) | partial | disposition-B.md |
| B11 Enter from the trigger | `skills/motion-patterns/SKILL.md:57` — motion-patterns Rules rule 11 (AB-05); Dropdown (AB-06) / Popover (AB-07) examples | new | disposition-B.md |
| B12 Exit to the trigger | `skills/motion-patterns/SKILL.md:61` — motion-patterns Rules rule 12 (AB-05); Dropdown (AB-06) / Popover (AB-07) examples | new | disposition-B.md |
| B13 No bounce on everyday UI | `skills/motion-patterns/SKILL.md:64` — motion-patterns Rules rule 13 (AB-05) | new | disposition-B.md |
| B14 Don't tween while held | `skills/motion-patterns/SKILL.md:68` — motion-patterns Rules rule 14 (AB-05); cross-ref G18 | new | disposition-B.md |
| B15 Make exits 20% shorter | `skills/motion-foundations/SKILL.md:333` — motion-foundations token `exitFactor: 0.8`; CONFLICT FLAG: quick-reference `exit-faster-than-enter` says ~60–70%, not changed, parent adjudicates; Rules rule 15 (AB-05) | partial | disposition-B.md |
| B16 Overlap old & new states | `skills/motion-patterns/SKILL.md:77` — motion-patterns Rules rule 16 (AB-05); motion-advanced Rules rule 9 + Overlapping state change example (AB-09/AB-10); scoped vs Rule 3 (`mode="wait"` still governs page transitions) | partial | disposition-B.md |
| B17 Masks for reveals & colour | `skills/motion-advanced/SKILL.md:61` — motion-advanced Rules rule 10 (AB-09); Mask reveal example (AB-10) | new | disposition-B.md |
| B18 Crossfade icons + blur | `skills/make-interfaces-feel-better/SKILL.md:120` — make-interfaces-feel-better Motion defaults; no new text; named in AB-05 insert | covered | disposition-B.md |
| B19 Rubber band past bounds | `skills/motion-advanced/SKILL.md:66` — motion-advanced Rules rule 11 (AB-09); cross-ref A2 | partial | disposition-B.md |
| B20 Reuse the same layoutId | `skills/motion-patterns/SKILL.md:87` — motion-patterns Rules rule 18 (AB-05); note AB-08 on the Shared-element crossfade example; dedupe: primary = motion-patterns example + glossary G20 | partial | disposition-B.md |
| C1 Tags & pills | `skills/polish-pass/reference/slop-checklist.md:72` — polish-pass slop checklist (SLOP_F22); flags, cleared by a recorded D19 reason + theme-fit | partial | disposition-CD.md |
| C2 Excessive italics | `skills/polish-pass/reference/slop-checklist.md:89` — polish-pass slop checklist (SLOP_F22); flags, cleared by a recorded D19 reason + theme-fit | new | disposition-CD.md |
| C3 Instrument Serif | `skills/polish-pass/reference/slop-checklist.md:104` — polish-pass slop checklist (SLOP_F22); flags, cleared by a recorded D19 reason + theme-fit | new | disposition-CD.md |
| C4 Negative kerning | `skills/polish-pass/reference/slop-checklist.md:123` — polish-pass slop checklist (SLOP_F22); flags, cleared by a recorded D19 reason + theme-fit | partial | disposition-CD.md |
| C5 Over-the-top detailed UI | `skills/polish-pass/reference/slop-checklist.md:140` — polish-pass slop checklist (SLOP_F22); flags, cleared by a recorded D19 reason + theme-fit | new | disposition-CD.md |
| C6 Overusing dividers | `skills/polish-pass/reference/slop-checklist.md:156` — polish-pass slop checklist (SLOP_F22); flags, cleared by a recorded D19 reason + theme-fit | partial | disposition-CD.md |
| C7 Color shades & opacities | `skills/polish-pass/reference/slop-checklist.md:172` — polish-pass slop checklist (SLOP_F22); flags, cleared by a recorded D19 reason + theme-fit | partial | disposition-CD.md |
| C8 Containers with borders | `skills/polish-pass/reference/slop-checklist.md:187` — polish-pass slop checklist (SLOP_F22); flags, cleared by a recorded D19 reason + theme-fit | partial | disposition-CD.md |
| C9 Overly detailed diagrams | `skills/polish-pass/reference/slop-checklist.md:204` — polish-pass slop checklist (SLOP_F22); flags, cleared by a recorded D19 reason + theme-fit | partial | disposition-CD.md |
| C10 Verbose, redundant text | `skills/polish-pass/reference/slop-checklist.md:222` — polish-pass slop checklist (SLOP_F22); flags, cleared by a recorded D19 reason + theme-fit | partial | disposition-CD.md |
| C11 Code breadcrumbs | `skills/polish-pass/reference/slop-checklist.md:239` — polish-pass slop checklist (SLOP_F22); flags, cleared by a recorded D19 reason + theme-fit | new | disposition-CD.md |
| C12 Section numbering | `skills/polish-pass/reference/slop-checklist.md:254` — polish-pass slop checklist (SLOP_F22); flags, cleared by a recorded D19 reason + theme-fit | partial | disposition-CD.md |
| C13 Eyebrows | `skills/polish-pass/reference/slop-checklist.md:271` — polish-pass slop checklist (SLOP_F22); flags, cleared by a recorded D19 reason + theme-fit | partial | disposition-CD.md |
| C14 Dithering | `skills/polish-pass/reference/slop-checklist.md:300` — polish-pass slop checklist (SLOP_F22); flags, cleared by a recorded D19 reason + theme-fit | partial | disposition-CD.md |
| C15 ASCII images | `skills/polish-pass/reference/slop-checklist.md:318` — polish-pass slop checklist (SLOP_F22); flags, cleared by a recorded D19 reason + theme-fit | partial | disposition-CD.md |
| C16 Squircles | `skills/polish-pass/reference/slop-checklist.md:334` — polish-pass slop checklist (SLOP_F22); flags, cleared by a recorded D19 reason + theme-fit | partial | disposition-CD.md |
| C17 Excessive mono fonts | `skills/polish-pass/reference/slop-checklist.md:353` — polish-pass slop checklist (SLOP_F22); flags, cleared by a recorded D19 reason + theme-fit | partial | disposition-CD.md |
| C18 ALL CAPS subtitles | `skills/polish-pass/reference/slop-checklist.md:369` — polish-pass slop checklist (SLOP_F22); flags, cleared by a recorded D19 reason + theme-fit | partial | disposition-CD.md |
| C19 Gradient backgrounds | `skills/polish-pass/reference/slop-checklist.md:385` — polish-pass slop checklist (SLOP_F22); flags, cleared by a recorded D19 reason + theme-fit | partial | disposition-CD.md |
| C20 Periods in titles | `skills/polish-pass/reference/slop-checklist.md:406` — polish-pass slop checklist (SLOP_F22); flags, cleared by a recorded D19 reason + theme-fit | new | disposition-CD.md |
| D1 Delete filler badges | `skills/polish-pass/reference/unslop-fixes.md:58` — polish-pass unslop fixes (UNSLOP_F22) | new | disposition-CD.md |
| D2 Drop redundant labels | `skills/polish-pass/reference/unslop-fixes.md:68` — polish-pass unslop fixes (UNSLOP_F22) | partial | disposition-CD.md |
| D3 Unitalicize random words | `skills/polish-pass/reference/unslop-fixes.md:82` — polish-pass unslop fixes (UNSLOP_F22) | new | disposition-CD.md |
| D4 Mono only where needed | `skills/polish-pass/reference/unslop-fixes.md:94` — polish-pass unslop fixes (UNSLOP_F22) | new | disposition-CD.md |
| D5 Use a design system | `skills/polish-pass/reference/unslop-fixes.md:106` — polish-pass unslop fixes (UNSLOP_F22); covered-by-architecture — the plugin IS a design system | covered | disposition-CD.md |
| D6 Show the actual product | `skills/polish-pass/reference/unslop-fixes.md:121` — polish-pass unslop fixes (UNSLOP_F22) | partial | disposition-CD.md |
| D7 Enlarge the main feature | `skills/polish-pass/reference/unslop-fixes.md:136` — polish-pass unslop fixes (UNSLOP_F22) | partial | disposition-CD.md |
| D8 Group with spacing | `skills/polish-pass/reference/unslop-fixes.md:150` — polish-pass unslop fixes (UNSLOP_F22); pointer spec P6 (ui-ux-pro-max / motion-patterns) | partial | disposition-CD.md |
| D9 Make headlines specific | `skills/polish-pass/reference/unslop-fixes.md:163` — polish-pass unslop fixes (UNSLOP_F22); pointer spec P1 (ui-ux-pro-max / motion-patterns) | new | disposition-CD.md |
| D10 Emphasize the CTA | `skills/polish-pass/reference/unslop-fixes.md:177` — polish-pass unslop fixes (UNSLOP_F22); pointer spec P2 (ui-ux-pro-max / motion-patterns) | partial | disposition-CD.md |
| D11 Add an accent colour | `skills/polish-pass/reference/unslop-fixes.md:193` — polish-pass unslop fixes (UNSLOP_F22); points at H1 (ACCENT_F22), does not duplicate it | new | disposition-CD.md |
| D12 Keep icons consistent | `skills/polish-pass/reference/unslop-fixes.md:209` — polish-pass unslop fixes (UNSLOP_F22) | partial | disposition-CD.md |
| D13 Remove embellishments | `skills/polish-pass/reference/unslop-fixes.md:223` — polish-pass unslop fixes (UNSLOP_F22) | partial | disposition-CD.md |
| D14 Inner radius = outer – padding | `skills/polish-pass/reference/unslop-fixes.md:236` — polish-pass unslop fixes (UNSLOP_F22); point, do not restate (craft floor) | covered | disposition-CD.md |
| D15 Improve text contrast | `skills/polish-pass/reference/unslop-fixes.md:250` — polish-pass unslop fixes (UNSLOP_F22); pointer spec P3 (ui-ux-pro-max / motion-patterns); point, do not restate (4.5:1 rule) | covered | disposition-CD.md |
| D16 Wrap headlines properly | `skills/polish-pass/reference/unslop-fixes.md:264` — polish-pass unslop fixes (UNSLOP_F22); pointer spec P4 (ui-ux-pro-max / motion-patterns) | partial | disposition-CD.md |
| D17 Align by eye, not pixels | `skills/polish-pass/reference/unslop-fixes.md:277` — polish-pass unslop fixes (UNSLOP_F22) | partial | disposition-CD.md |
| D18 Use tabular nums | `skills/polish-pass/reference/unslop-fixes.md:292` — polish-pass unslop fixes (UNSLOP_F22); pointer spec P5 (ui-ux-pro-max / motion-patterns); primary home is ui-ux-pro-max `number-tabular` (SPEC §5) | covered | disposition-CD.md |
| D19 Add loading states | `skills/polish-pass/reference/unslop-fixes.md:309` — polish-pass unslop fixes (UNSLOP_F22) | new | disposition-CD.md |
| D20 Animate useful feedback | `skills/polish-pass/reference/unslop-fixes.md:326` — polish-pass unslop fixes (UNSLOP_F22); pointer spec P7 (ui-ux-pro-max / motion-patterns) | partial | disposition-CD.md |
| E1 Dithering | `skills/design-taste-frontend/SKILL.md:248` — Hallmark theme Range line in references/hallmark/references/themes/halftone.md | new | disposition-E.md |
| E2 ASCII over video | `skills/design-taste-frontend/SKILL.md:255` — Hallmark theme Range line in references/hallmark/references/themes/terminal.md | new | disposition-E.md |
| E3 Infinite canvases | `skills/design-taste-frontend/SKILL.md:262` — Hallmark theme Range line in references/hallmark/references/themes/blueprint.md | new | disposition-E.md |
| E4 Disco logos | `skills/design-taste-frontend/SKILL.md:269` — Hallmark theme Range line in references/hallmark/references/themes/carnival.md | new | disposition-E.md |
| E5 Renaissance branding | `skills/design-taste-frontend/SKILL.md:276` — Hallmark theme Range line in references/hallmark/references/themes/vellum.md | new | disposition-E.md |
| E6 Monet backgrounds | `skills/design-taste-frontend/SKILL.md:283` — Taste menu entry points at less-flat-ui #21 Impressionist paintings; no theme-file line, does not duplicate the treatment | pointer | disposition-E.md |
| E7 Dark gradient heroes | `skills/design-taste-frontend/SKILL.md:290` — Hallmark theme Range line in references/hallmark/references/themes/dusk.md | new | disposition-E.md |
| E8 Pixel loaders | `skills/design-taste-frontend/SKILL.md:297` — Hallmark theme Range line in references/hallmark/references/themes/arcade.md | new | disposition-E.md |
| E9 Instrument Serif | `skills/design-taste-frontend/SKILL.md:304` — Hallmark theme Range line in references/hallmark/references/themes/lumen.md | new | disposition-E.md |
| E10 One italic word | `skills/design-taste-frontend/SKILL.md:311` — Hallmark theme Range line in references/hallmark/references/themes/spore.md | new | disposition-E.md |
| E11 Cream backgrounds | `skills/design-taste-frontend/SKILL.md:318` — Hallmark theme Range line in references/hallmark/references/themes/hum.md | new | disposition-E.md |
| E12 All-caps eyebrows | `skills/design-taste-frontend/SKILL.md:325` — menu only — no theme-file line (validator forbids eyebrows / sparkle / three-icon-cards as theme lines) | new | disposition-E.md |
| E13 Pulsing live dots | `skills/design-taste-frontend/SKILL.md:332` — Hallmark theme Range line in references/hallmark/references/themes/wayfind.md | new | disposition-E.md |
| E14 Sparkle icons | `skills/design-taste-frontend/SKILL.md:339` — menu only — no theme-file line (validator forbids eyebrows / sparkle / three-icon-cards as theme lines) | new | disposition-E.md |
| E15 Liquid Glass | `skills/design-taste-frontend/SKILL.md:346` — Hallmark theme Range line in references/hallmark/references/themes/dose.md | new | disposition-E.md |
| E16 Three icon cards | `skills/design-taste-frontend/SKILL.md:353` — menu only — no theme-file line (validator forbids eyebrows / sparkle / three-icon-cards as theme lines) | new | disposition-E.md |
| E17 Decorative flowcharts | `skills/design-taste-frontend/SKILL.md:360` — Hallmark theme Range line in references/hallmark/references/themes/blueprint.md | new | disposition-E.md |
| E18 Endless marquees | `skills/design-taste-frontend/SKILL.md:367` — Hallmark theme Range line in references/hallmark/references/themes/editorial.md | new | disposition-E.md |
| E19 Squircles | `skills/design-taste-frontend/SKILL.md:374` — Hallmark theme Range line in references/hallmark/references/themes/squeeze.md | new | disposition-E.md |
| E20 Pretext text wrapping | `skills/design-taste-frontend/SKILL.md:381` — Hallmark theme Range line in references/hallmark/references/themes/newsprint.md | new | disposition-E.md |
| F1 Felt texture | `skills/less-flat-ui/SKILL.md:107` — less-flat-ui catalogue; no text copied (verification-only) | verification-only | disposition-F.md |
| F2 Fluted glass | `skills/less-flat-ui/SKILL.md:123` — less-flat-ui catalogue; no text copied (verification-only) | verification-only | disposition-F.md |
| F3 Thermal gradients | `skills/less-flat-ui/SKILL.md:145` — less-flat-ui catalogue; no text copied (verification-only) | verification-only | disposition-F.md |
| F4 Water ripples | `skills/less-flat-ui/SKILL.md:161` — less-flat-ui catalogue; no text copied (verification-only) | verification-only | disposition-F.md |
| F5 Speckled graphite | `skills/less-flat-ui/SKILL.md:176` — less-flat-ui catalogue; no text copied (verification-only) | verification-only | disposition-F.md |
| F6 Single-hue landscapes | `skills/less-flat-ui/SKILL.md:190` — less-flat-ui catalogue; no text copied (verification-only) | verification-only | disposition-F.md |
| F7 Blueprint grids | `skills/less-flat-ui/SKILL.md:202` — less-flat-ui catalogue; no text copied (verification-only) | verification-only | disposition-F.md |
| F8 Halftone | `skills/less-flat-ui/SKILL.md:220` — less-flat-ui catalogue; no text copied (verification-only) | verification-only | disposition-F.md |
| F9 Grainy gradients | `skills/less-flat-ui/SKILL.md:234` — less-flat-ui catalogue; no text copied (verification-only) | verification-only | disposition-F.md |
| F10 Grass texture | `skills/less-flat-ui/SKILL.md:246` — less-flat-ui catalogue; no text copied (verification-only) | verification-only | disposition-F.md |
| F11 Dithered images | `skills/less-flat-ui/SKILL.md:261` — less-flat-ui catalogue; no text copied (verification-only) | verification-only | disposition-F.md |
| F12 Paper texture | `skills/less-flat-ui/SKILL.md:279` — less-flat-ui catalogue; no text copied (verification-only) | verification-only | disposition-F.md |
| F13 Contour lines | `skills/less-flat-ui/SKILL.md:295` — less-flat-ui catalogue; no text copied (verification-only) | verification-only | disposition-F.md |
| F14 Cloud sky | `skills/less-flat-ui/SKILL.md:310` — less-flat-ui catalogue; no text copied (verification-only) | verification-only | disposition-F.md |
| F15 Pixel mosaics | `skills/less-flat-ui/SKILL.md:326` — less-flat-ui catalogue; no text copied (verification-only) | verification-only | disposition-F.md |
| F16 Lens distortion | `skills/less-flat-ui/SKILL.md:340` — less-flat-ui catalogue; no text copied (verification-only) | verification-only | disposition-F.md |
| F17 Stippled gradients | `skills/less-flat-ui/SKILL.md:364` — less-flat-ui catalogue; no text copied (verification-only) | verification-only | disposition-F.md |
| F18 Square-dot grids | `skills/less-flat-ui/SKILL.md:380` — less-flat-ui catalogue; no text copied (verification-only) | verification-only | disposition-F.md |
| F19 Blurred photos | `skills/less-flat-ui/SKILL.md:397` — less-flat-ui catalogue; no text copied (verification-only) | verification-only | disposition-F.md |
| F20 Iridescent shapes | `skills/less-flat-ui/SKILL.md:418` — less-flat-ui catalogue; no text copied (verification-only) | verification-only | disposition-F.md |
| F21 Impressionist paintings | `skills/less-flat-ui/SKILL.md:434` — less-flat-ui catalogue; no text copied (verification-only) | verification-only | disposition-F.md |
| F22 ASCII and pixels | `skills/less-flat-ui/SKILL.md:452` — less-flat-ui catalogue; no text copied (verification-only) | verification-only | disposition-F.md |
| G1 Kerning | `skills/design-taste-frontend/references/design-glossary.md:20` — glossary definition; pointer spec P-G1 | new | disposition-G.md |
| G2 Optical centre | `skills/design-taste-frontend/references/design-glossary.md:21` — glossary definition; pointer spec P-G1 | new | disposition-G.md |
| G3 Tabular numbers | `skills/design-taste-frontend/references/design-glossary.md:22` — glossary definition; pointer spec P-G1 | partial | disposition-G.md |
| G4 Layout shift | `skills/design-taste-frontend/references/design-glossary.md:23` — glossary definition; pointer spec P-G1 | partial | disposition-G.md |
| G5 Tracking | `skills/design-taste-frontend/references/design-glossary.md:24` — glossary definition; pointer spec P-G1 | partial | disposition-G.md |
| G6 Optimistic update | `skills/design-taste-frontend/references/design-glossary.md:25` — glossary definition; pointer spec P-G1 | partial | disposition-G.md |
| G7 x-height | `skills/design-taste-frontend/references/design-glossary.md:26` — glossary definition; pointer spec P-G1 | partial | disposition-G.md |
| G8 Touch target | `skills/design-taste-frontend/references/design-glossary.md:27` — glossary definition; pointer spec P-G1; owning column: 44x44px minimum (the plugin floor, W2-C4) | partial | disposition-G.md |
| G9 Leading | `skills/design-taste-frontend/references/design-glossary.md:28` — glossary definition; pointer spec P-G1 | partial | disposition-G.md |
| G10 Origin-aware animation | `skills/design-taste-frontend/references/design-glossary.md:29` — glossary definition; pointer spec P-G3 | partial | disposition-G.md |
| G11 OKLCH | `skills/design-taste-frontend/references/design-glossary.md:30` — glossary definition; pointer spec P-G1 | partial | disposition-G.md |
| G12 Widow | `skills/design-taste-frontend/references/design-glossary.md:31` — glossary definition; pointer spec P-G1 | new | disposition-G.md |
| G13 Safe area | `skills/design-taste-frontend/references/design-glossary.md:32` — glossary definition; pointer spec P-G1 | partial | disposition-G.md |
| G14 Stagger | `skills/design-taste-frontend/references/design-glossary.md:33` — glossary definition; pointer spec P-G3 | partial | disposition-G.md |
| G15 Line length | `skills/design-taste-frontend/references/design-glossary.md:34` — glossary definition; pointer spec P-G1 | partial | disposition-G.md |
| G16 Affordance | `skills/design-taste-frontend/references/design-glossary.md:35` — glossary definition; pointer spec P-G1 | partial | disposition-G.md |
| G17 Combobox | `skills/design-taste-frontend/references/design-glossary.md:36` — glossary definition; pointer spec P-G1 | partial | disposition-G.md |
| G18 Interruptible animation | `skills/design-taste-frontend/references/design-glossary.md:37` — glossary definition; pointer spec P-G2 | partial | disposition-G.md |
| G19 Progressive disclosure | `skills/design-taste-frontend/references/design-glossary.md:38` — glossary definition; pointer spec P-G1 | partial | disposition-G.md |
| G20 Shared element transition | `skills/design-taste-frontend/references/design-glossary.md:39` — glossary definition; pointer spec P-G1 | partial | disposition-G.md |
| H1 Color accents | ui-ux-pro-max `skills/ui-ux-pro-max/SKILL.md:122`; polish-pass accent-sprawl check `skills/polish-pass/reference/slop-checklist.md:419`; D11 points at it | partial | disposition-B.md + disposition-CD.md |
| H2 Accentuation accents | orchestrate design-package step `skills/orchestrate/SKILL.md:62`; ui-ux-pro-max hierarchy rules `skills/ui-ux-pro-max/SKILL.md:16`; polish-pass hierarchy check `skills/polish-pass/reference/slop-checklist.md:450` | new | disposition-B.md + disposition-CD.md |

## Process rows (not item rows)

| Process | Placement (built tree) | Status | Source |
|---|---|---|---|
| Mobbin (§9) | orchestrate `skills/orchestrate/SKILL.md:62` (MOBBIN_RESEARCH_F22: category-level research step, record requirement, no-copy boundary, free tier, never blocked); design-taste-frontend `skills/design-taste-frontend/SKILL.md:445` (MOBBIN_PATTERN_F22); ui-ux-pro-max `skills/ui-ux-pro-max/SKILL.md:167` (MOBBIN_PATTERN_F22, PROC-P1); polish-pass `skills/polish-pass/SKILL.md:104` (MOBBIN_QA_F22) | placed | process-report.md |
| Directives, not descriptions (§10) | orchestrate `skills/orchestrate/SKILL.md:64` (DIRECTIVES_F22, step 4 Build); design-taste-frontend `skills/design-taste-frontend/SKILL.md:391` (step 4a) + `skills/design-taste-frontend/SKILL.md:391` (Hallmark theme-deal pointer); ui-ux-pro-max `skills/ui-ux-pro-max/SKILL.md:219` (PROC-P2); GAN planner `agents/ecc-gan-planner.md:46`, generator `agents/ecc-gan-generator.md:32`, evaluator `agents/ecc-gan-evaluator.md:134`; polish-pass `skills/polish-pass/SKILL.md:100` (DIRECTIVES_F22); prose-only FAILS the handoff check | placed | process-report.md |
| Libraries (§11) | Lenis: motion-foundations `skills/motion-foundations/SKILL.md:178` (LENIS_F22, `lenis@1.3.27`, MIT, smooth-scroll rule); GSAP: motion-patterns `skills/motion-patterns/SKILL.md:429` (SCROLLTRIGGER_F22; `gsap@3.15.1`, GreenSock Standard "no charge", NOT MIT; `--domain gsap` 17 presets in ui-ux-pro-max `skills/ui-ux-pro-max/SKILL.md:346`); Vanta: design-taste-frontend `skills/design-taste-frontend/SKILL.md:127` (VANTA_F22, `vanta@0.5.24` MIT + `three@0.134.0`, MUST-disable/static-fallback/mobile/scrim); React Bits: motion-patterns `skills/motion-patterns/SKILL.md:552` (REACTBITS_F22, commit `9d9c687d…`, MIT + Commons Clause, React-only); three.js scoped pins: Vanta `three@0.134.0`, general `three@0.185.1`, Bang's 0.161.0 recorded-only; stale GSAP CDN 3.12.2 in threejs.csv row 35 fixed to 3.15.1 (CSV-GSAP) | placed | libraries-report.md |
| Bang Motion port (§12) | pitch-deck-video `skills/pitch-deck-video/SKILL.md:247` (anti-slide), `skills/pitch-deck-video/SKILL.md:281` (one-world), `skills/pitch-deck-video/SKILL.md:304` (10 style directions, menu), `skills/pitch-deck-video/SKILL.md:337` (19 openers, menu), `skills/pitch-deck-video/SKILL.md:373` (kinetic typography as directives), `skills/pitch-deck-video/SKILL.md:409` (explainer); pin SHA `c1aa65e9…` in pitch-deck-video + `build.sh:42` (BANG_PIN) + fix22/bang-report.md; MIT; GSAP 3.15.1 plugin pin (Bang's 3.12.5 / Three.js 0.161.0 recorded as Bang's only); repo quiet since Sep 15, 2026, SKILL.md in Indonesian; /demo still films the real app, no second toolchain | placed | bang-report.md |

## Notes and flags for the coordinator

- **Three token conflicts applied exactly as specified, flags carried, NOT resolved** (SPEC §4c): B3 30ms vs Rule 5 0.05s floor; B15 0.8× vs quick-reference ~60–70%; B4 0.97 vs `scale.press` 0.95 (plus the B4 observation that the motion-* press scale 0.95 differs from the polish press default 0.97 — neither value changed). Parent adjudicates.
- **GSAP converges on 3.15.1 everywhere** (GreenSock Standard "no charge", NOT MIT). Three.js is SCOPED, not single-version: Vanta `three@0.134.0`, general `three@0.185.1`, Bang's 0.161.0 recorded as Bang's version only. This supersedes the Bang staged note's earlier "ONE pinned version each" alignment flag — SPEC tension (§12 alignment vs §11 deviations D3–D4 in `fix22/libraries-report.md`).
- **Counts corrected against the source dispositions during verification:** TRENDS_F22 occurs 23× in Taste SKILL.md (20 entries + intro ×2 + finish-gate pointer), not 22×; Hallmark carries 16 Range lines in 15 theme files (Blueprint E3+E17), not 15/14.
- **Group F note:** the less-flat-ui catalogue carries 23 treatments; F1–F22 are the 22 reel items in this table, and treatment #23 Soft shadow (`skills/less-flat-ui/SKILL.md:488`) was also verified present — it came from the @lnunesdesigns reel, not the 22-backgrounds reel, so it is not a 145th item row.
- **C13 vs Impeccable craft-floor eyebrow tension** (stricter rule wins; flagged in disposition-CD, not changed).
- **Prior verifiers:** verify15/17/18/19/20/21 each fail ONLY their frozen post-fix21 build.sh fingerprint check (23,647 lines / md5 8dfacb47…) plus the resulting cascade lines; all substantive checks still pass. The fingerprint is legitimately superseded by fix #22 (23,732 lines / md5 891fca7b…). verify22.py §17 allows exactly those lines.
- **Banned terms:** 0 in the rebuilt tree (case-insensitive grep for claude|codex|anthropic|opus|sonnet|haiku|composer-2.5, excluding node_modules).
