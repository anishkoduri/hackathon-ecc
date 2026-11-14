# Fix #22 Group E disposition — 20 AI Design Trends (TRENDS_F22)

Agent: Group E implementation. Date: Nov 12, 2026.
Scope: SPEC §1 Group E (20 items), §3 placement (design-taste-frontend + Hallmark cross-references),
§4b adjudication (menu, never defaults), §4a conditions on overlapping pairs.

## Baseline method

Re-verified every item with word-boundary greps (`grep -P -i`, `\b...\b`) over four
locations: `build.sh` (23,647 lines, md5 `8dfacb47a2a6698d47e4b4a5f8d9126c`), the built tree
`hackathon-ecc/skills/` (`.md` files), the staged `new-skills/design-taste-frontend/`
(`.md` files), and the less-flat-ui source `~/workspace/cursor-skills/less-flat-ui/SKILL.md`
(copied into the plugin by `build.sh:258`). Hyphen-joined compounds do not count as coverage.
The parent's substring greps had false positives, confirmed and discarded here: "disco"
matched discoverable/discovered; "Monet" matched Monetization; "tween" matched between;
"tracking" matched cost-tracking. All counts below are word-boundary counts.

Result: the trends menu as a whole is new. No item was recorded anywhere as a trend option.
Individual techniques exist in places (noted per row); none was recorded as a trend entry.

## Overlapping slop pairs (§4a/§4b, all named in the menu intro, SKILL.md:244)

E1 dithering ↔ C14; E2 ASCII over video ↔ C15; E9 Instrument Serif ↔ C3;
E12 all-caps eyebrows ↔ C13/C18; E19 squircles ↔ C16; E7 dark gradient heroes ↔ C19.
Each overlapping entry carries the §4a condition (deliberate + theme-matched + recorded).
Trend-only items (no slop counterpart): E3, E4, E5, E6, E8, E11, E13, E14, E15, E16, E18, E20.

## Placement

- Menu: `new-skills/design-taste-frontend/SKILL.md`, step 4, immediately after the Hallmark
  theme-deal paragraph, lines 244–385 (intro 244, entries E1–E20 at 246, 253, 260, 267, 274,
  281, 288, 295, 302, 309, 316, 323, 330, 337, 344, 351, 358, 365, 372, 379). Anchor: TRENDS_F22.
  Every entry states "Opt-in only, theme-matched" and carries a fix #19 D19 reason with all six
  dimensions (Motion / Theme / Texture / Visuals / Techniques / Colors), verified 20/20 per
  dimension. No trend is a default.
- Finish-gate pointer: same SKILL.md, step 6, line 477 ("Fix #22 static check"), anchors
  TRENDS_F22 + SLOP_F22: "Run the SLOP_F22 slop checklist in polish-pass as a static check;
  its flags are candidate evidence for browser-qa, never verdicts".
- Hallmark cross-references: one `TRENDS_F22` Range bullet per fitting theme file (15 lines in
  14 files; Blueprint carries E3 + E17). Full D19 reason lives in the menu entry; the theme line
  points back to it. All 15 files pass `node theme.mjs validate` (exit 0).
- Nothing else touched: `build.sh` md5 unchanged, `hackathon-ecc/` untouched, `build.sh` never run.

## Disposition table (one row per item)

| Item | Baseline (new as a trend entry + where the technique already exists, if anywhere) | Placement (skill + section + anchor) | Status |
|---|---|---|---|
| E1 Dithering | New as a trend entry. Technique exists: less-flat-ui #11 Dithered images (`~/workspace/cursor-skills/less-flat-ui/SKILL.md:257`); Taste `ascii-shade` effect family and `references/backgrounds.md`. Word-boundary `dither` in build.sh: 0 hits. | SKILL.md:246 (menu, TRENDS_F22, §4a C14 condition) + `references/hallmark/references/themes/halftone.md:64` Range line | placed |
| E2 ASCII over video | New as a trend entry. No "ASCII over video" anywhere: `ascii.*video\|video.*ascii` 0 hits in build.sh, staged taste, built tree. Technique exists: Taste `ascii-shade` effect (`assets/effects/README.md:87`); less-flat-ui #22 ASCII and pixels (`SKILL.md:448`). build.sh `\bascii\b`: 5 hits, all unrelated (ASCII/markdown output format, `--format ascii`). | SKILL.md:253 (menu, TRENDS_F22, §4a C15 condition) + `references/hallmark/references/themes/terminal.md:57` Range line | placed |
| E3 Infinite canvases | New. `infinite canvas` 0 hits in build.sh, staged taste, built tree, less-flat-ui. No prior technique. | SKILL.md:260 (menu, TRENDS_F22, trend-only) + `references/hallmark/references/themes/blueprint.md:63` Range line | placed |
| E4 Disco logos | New. Word-boundary `disco` 0 hits everywhere (parent substring hits were discoverable/discovered). No prior technique. | SKILL.md:267 (menu, TRENDS_F22, trend-only) + `references/hallmark/references/themes/carnival.md:67` Range line | placed |
| E5 Renaissance branding | New. Word-boundary `renaissance` 0 hits everywhere. No prior technique. | SKILL.md:274 (menu, TRENDS_F22, trend-only) + `references/hallmark/references/themes/vellum.md:64` Range line | placed |
| E6 Monet backgrounds | New as a trend entry. Technique exists: less-flat-ui #21 Impressionist paintings (`SKILL.md:430`). Word-boundary `monet` 0 hits everywhere (parent substring hits were Monetization). | SKILL.md:281 (menu, TRENDS_F22, trend-only) — POINTER to less-flat-ui #21, treatment not duplicated. No Hallmark line: no theme's material is impressionist painting. | pointer |
| E7 Dark gradient heroes | New as a trend entry. "Dark gradient" exists as a technique, never as a trend option: Taste `references/backgrounds.md:92` ("every dark gradient gets a static…"), `references/hallmark/references/gates.md:61` (2a bans purple-to-blue / purple-to-pink / cyan-on-dark gradients); gradient treatments exist in less-flat-ui #3/#9. build.sh "dark gradient": 0 hits. | SKILL.md:288 (menu, TRENDS_F22, §4a C19 condition + gates.md 2a) + `references/hallmark/references/themes/dusk.md:68` Range line (short form, see notes) | placed |
| E8 Pixel loaders | New. "Pixel loader" 0 hits everywhere. "Loader" exists only generically (`references/motion.md:125,176`: "Never a loader, a gate…"). Pixel technique exists (less-flat-ui pixel mosaics; Arcade Silkscreen pixel figures). | SKILL.md:295 (menu, TRENDS_F22, trend-only) + `references/hallmark/references/themes/arcade.md:59` Range line | placed |
| E9 Instrument Serif | New as a trend entry. Face exists as a dealt display face, never as a trend option: `references/hallmark/references/themes/lumen.md:6,10,28,40` (display IS Instrument Serif); `references/layout-v4.md:262` (static-face example). build.sh "instrument serif": 0 hits. | SKILL.md:302 (menu, TRENDS_F22, §4a C3 condition; font rules fix #19/#20/#21 untouched) + `references/hallmark/references/themes/lumen.md:60` Range line | placed |
| E10 One italic word | New as a trend entry. "Italic" exists widely but never as a one-word trend option: SKILL.md fix #19 F2 (`font-synthesis: none` re synthesised italic); Spore italic second name; Editorial italic quotation; Newsprint italic emphasis in running text only. | SKILL.md:309 (menu, TRENDS_F22, §4a C2/D3 one rule + Reflex 38) + `references/hallmark/references/themes/spore.md:65` Range line | placed |
| E11 Cream backgrounds | New as a trend entry. "Cream" exists as paper/material, never as a trend option: Taste `references/backgrounds.md:18` (cream page); `references/hallmark/references/gates.md:68,219` (#65 named look); Halftone butter-cream stock; Hum grained cream paper; Atelier/Bloom explicitly say "not a cream page…". build.sh `\bcream\b`: 0 hits. | SKILL.md:316 (menu, TRENDS_F22, trend-only + gates.md 65 guard) + `references/hallmark/references/themes/hum.md:63` Range line | placed |
| E12 All-caps eyebrows | New as a trend entry. "Eyebrow" exists as a template tell / label pattern, never as a trend option: `references/copy-tells.md:88`, `references/copy-voice.md:108,152` (eyebrow labels 1–2 a page), `references/sections.md:425`; build.sh 5 hits (fix #20 F5 key-label context + fixup20b). All-caps exists in `references/copy.md` and `themes/editorial.md`. | SKILL.md:323 (menu, TRENDS_F22, §4a C13/C18 condition + gates.md 67). NO theme-file line: the theme contract forbids eyebrows in any form and `theme.mjs validate` rejects the word "eyebrow" (see notes). Menu names the caps-led themes (Manifesto, Broadside). | placed (menu only) |
| E13 Pulsing live dots | New as a trend entry. "Live dot" exists as a status treatment, never as a trend option: `references/motion.md:150` (live dot 2.4s); `references/hallmark/references/themes/wayfind.md:62,73` (cobalt live dot, blinks once, never loops). "Pulsing" exists in motion/effects contexts only. | SKILL.md:330 (menu, TRENDS_F22, trend-only) + `references/hallmark/references/themes/wayfind.md:64` Range line | placed |
| E14 Sparkle icons | New. Word-boundary `sparkle` 0 hits in build.sh, staged taste, built tree, less-flat-ui. No prior technique. | SKILL.md:337 (menu, TRENDS_F22, trend-only). No Hallmark line: no theme's material names a sparkle motif; forcing one would invent a fit. | placed (menu only) |
| E15 Liquid Glass | New. "Liquid glass" 0 hits everywhere. Glass as a material exists: Dusk smoked glass (`themes/dusk.md:10,46,72`), Dose translucent tinted plastic (`themes/dose.md:10`); Refract explicitly bans frosted glass (`themes/refract.md:84`) and is NOT a fit. | SKILL.md:344 (menu, TRENDS_F22, trend-only) + `references/hallmark/references/themes/dose.md:63` Range line (short form, see notes) | placed |
| E16 Three icon cards | New as a trend entry. "Three cards" exists only as the anti-pattern: `references/copy-voice.md:108` ("Not the skeleton: eyebrow, claim heading, two-line lede, three cards…"), `references/sections.md:55` (a card layout at most twice a page). Fix #15 canonical variety pushes against default three-card layouts; entry records that. | SKILL.md:351 (menu, TRENDS_F22, trend-only + variety note). No Hallmark line: no theme prescribes three icon cards. | placed (menu only) |
| E17 Decorative flowcharts | New as a trend entry. "Flowchart" 0 hits in staged taste (occurs only in unrelated skills: accessibility, readme-template). Diagram technique exists (`references/diagrams.md`, fix #15 R2 one diagram by default). | SKILL.md:358 (menu, TRENDS_F22, §4a C5/C9 condition) + `references/hallmark/references/themes/blueprint.md:64` Range line | placed |
| E18 Endless marquees | New as a trend entry. "Marquee" exists as a moment/loop, never as a trend option: `references/moments.md:31,102` (marquee-row, words only, never logos, pause button), `references/motion.md:32,164,228` (logo marquee banned); build.sh 1 hit (fix #17 M4 marquee pause-on-hover). | SKILL.md:365 (menu, TRENDS_F22, trend-only) + `references/hallmark/references/themes/editorial.md:54` Range line | placed |
| E19 Squircles | New as a trend entry. "Squircle" 0 hits in staged taste and build.sh. Shape exists only as an option in `round2-skills/polish-pass/reference/lenses/polish-details.md:69` (optional corner smoothing (squircle) if the Design System uses it). | SKILL.md:372 (menu, TRENDS_F22, §4a C16 condition) + `references/hallmark/references/themes/squeeze.md:57` Range line | placed |
| E20 Pretext text wrapping | New. "Pretext" 0 hits everywhere. "Text wrapping" 1 build.sh hit (`build.sh:809`, a skill description line in make-interfaces-feel-better), no trend option. | SKILL.md:379 (menu, TRENDS_F22, trend-only) + `references/hallmark/references/themes/newsprint.md:58` Range line | placed |

## Hallmark cross-reference map (menu names vs theme-file lines)

Menu names a fitting theme for every trend except E6, E14, E16 (recorded menu-only with reasons
above). Theme-file Range lines exist for 15 trend/theme pairs; where the menu names two themes,
the file line went to the single strongest fit and the second theme is cited in the menu only:

- E1: Halftone (file) + Riso (menu only). E2: Terminal (file) + Cobalt (menu only; Cobalt is at
  7,919/8,000 bytes, a pointer line would breach the validator cap). E4: Carnival (file) +
  Arcade (menu only). E5: Vellum (file) + Atelier (menu only; Atelier at 7,821 bytes).
  E9: Lumen (file). E10: Spore (file). E11: Hum (file) + Halftone (menu only).
  E12: Manifesto + Broadside (menu only, validator forbids the word). E13: Wayfind (file).
  E15: Dose (file) + Dusk (menu only; Dusk carries the E7 line). E17: Blueprint (file, second
  line). E18: Editorial (file) + Arcade (menu only). E19: Squeeze (file) + Bloom (menu only;
  Bloom at 7,925/8,000 bytes). E20: Newsprint (file). E3: Blueprint (file). E7: Dusk (file).
  E8: Arcade (file).

## Notes / judgment calls (no SPEC deviation; all within §3/§4b)

1. E12 has no theme-file line. The theme contract (`references/hallmark/references/themes/README.md`,
   "What a theme may not carry") forbids "an eyebrow in any form", and `theme.mjs validate`
   rejects any file containing the word "eyebrow" (also "kicker", "overline"). Writing the
   cross-reference into Manifesto/Broadside would fail validation. The fit (caps-led display
   voices, gates.md 67) is recorded in the menu entry instead.
2. E14 and E16 have no Hallmark line. E14: no theme material names a sparkle motif. E16: no
   theme prescribes three icon cards, and fix #15 variety rules push against the shape. Both
   are menu-only by the task's "do not force one per theme" instruction.
3. E6 has no Hallmark line (pointer to less-flat-ui #21 per SPEC §4b); no theme's material is
   impressionist painting.
4. Dose (E15) and Dusk (E7) Range lines are short forms without the "Full D19 reason…"
   sentence: Dose was 7,833/8,000 bytes and Dusk 7,879/8,000 before the edit; the full sentence
   would have breached the validator's 8,000-byte cap. Final sizes: Dose 7,956, Dusk 7,974,
   both validate ok. The TRENDS_F22 token in each line is itself the pointer to the menu entry.
5. Cobalt (E2) and Bloom (E19) got no file line for the same byte-cap reason (7,919 and 7,925
   bytes pre-edit); their fits are cited in the menu entries.
6. Theme-file lines sit in the Range section (what the material makes without a photograph),
   as material-native treatments, not new components; they add no section, no component, no
   eyebrow, no tracked caps, no em/en dash, and no banned term. All 15 files pass
   `theme.mjs validate` (exit 0; the "no picture yet" notes are pre-existing — theme pictures
   are not staged in this plugin).
7. E10's Hallmark Reflex 38 note: Spore already declares its italic outlier as material, so no
   new waiver was needed; the menu entry records the Reflex 38 condition.
8. E7's entry explicitly excludes Midnight (solid blue ground, "not a moody gradient") and E15's
   entry explicitly excludes Refract (bans frosted glass) — negative fits recorded so a later
   reader does not "fix" them in.

## Verification (re-run after all edits)

- Menu: 20/20 entries present (SKILL.md:246–379), each "Opt-in only, theme-matched" (20/20),
  each with all six D19 dimensions (Motion 20, Theme 20, Texture 20, Visuals 20, Techniques 20,
  Colors 20). Overlapping pairs named in intro (SKILL.md:244). TRENDS_F22 appears 22× in SKILL.md.
- Finish-gate pointer: SKILL.md:477, names SLOP_F22 once, wording as tasked.
- Theme files: 15 TRENDS_F22 Range lines at the file:line numbers in the table above;
  `node ../../scripts/theme.mjs validate <15 files>` → all ok, exit 0.
- Banned terms: 0 (pattern redacted — see verify22.py)
- Em/en dashes in the 15 edited theme files → 0 hits.
- `build.sh` md5 still `8dfacb47a2a6698d47e4b4a5f8d9126c`, 23,647 lines; `hackathon-ecc/` untouched;
  `build.sh` never run; `fix11/fix11-stage.py` never run. No model pins, font rules, screen-verdicts
  rule, marketplace manifest, or Audit #4 backup touched.
