# Fix #22 Groups C+D — disposition (disposition-CD.md)

One row per item (C1–C20, D1–D20, H1, H2 = 42 rows). Baseline re-verified
Nov 12, 2026 with **word-boundary greps** (`grep -rniP`, word boundaries) over
`build.sh`, the built tree (`hackathon-ecc/`), and the staged sources
(`round2-skills/`, `new-skills/`); full output in `fix22/baseline-greps.txt`
(script: `fix22/baseline-greps.sh`). "Covered" means the rule already exists
and is only pointed at; "partial" means a neighbouring rule or the technique
exists but the slop check / fix wording is new; "new" means no covering rule.

Placement: all staged edits are in `round2-skills/polish-pass/` (copied verbatim
by `build.sh` line ~230 — `cp -r "$PLUGIN_ROOT/round2-skills/$s"`). Anchors:
`SLOP_F22` (slop checklist), `UNSLOP_F22` (unslop fix guidance), `ACCENT_F22`
(H1 sprawl check), `ACCENTUATION_F22` (H2 hierarchy check). Pointer specs for
build.sh-embedded skills are in `fix22/cd-pointers.md` (integrator applies them).

## Group C — 20 AI Design Slop Indicators (SLOP_F22)

| Item | Baseline + grep evidence | Placement (skill + section + anchor) | Status |
|---|---|---|---|
| C1 Tags & pills | partial — no slop check. `\bpill\b` hits are Taste component options (pill button styles, fx-tabs pill); fix #17 T1 names chip/tag/badge only as bounded containers; craft-floor requires pills only for small controls + chips on the text baseline. | polish-pass `reference/slop-checklist.md`, "C1 — Tags & pills", `SLOP_F22` | placed |
| C2 Excessive italics | new — `\bitalic\b` hits are unrelated (font-synthesis, a toolbar button); no italic-use rule in polish-pass. (Impeccable detector rule `italic-serif-display` is a different check — oversized italic serif hero.) | polish-pass `reference/slop-checklist.md`, "C2 — Excessive italics", `SLOP_F22` | placed |
| C3 Instrument Serif | new — "Instrument Serif" hits only as a Taste library option (`design-taste-frontend/library/type.json:1210`, `assets/layout/hero-product.html:21`); no slop check. | polish-pass `reference/slop-checklist.md`, "C3 — Instrument Serif", `SLOP_F22` | placed |
| C4 Negative kerning | partial — "negative kerning" 0 hits; craft-floor tracking floor −0.04em exists; `\bkerning\b` only in Taste `shared.js` (a CSS property list). | polish-pass `reference/slop-checklist.md`, "C4 — Negative kerning", `SLOP_F22` | placed |
| C5 Over-the-top detailed UI | new — "over-the-top" 0 hits, "overly detailed" 0 hits. | polish-pass `reference/slop-checklist.md`, "C5 — Over-the-top detailed UI", `SLOP_F22` | placed |
| C6 Overusing dividers | partial — `\bdivider\b` hits are Taste components (fx-band divider band); craft-floor requires decorative structure (dividers included) to stay neutral; no overuse check. | polish-pass `reference/slop-checklist.md`, "C6 — Overusing dividers", `SLOP_F22` | placed |
| C7 Color shades & opacities | partial — `\bshade\b`/`\bopacity\b` hits unrelated (flecto-shade repo name, fx-feature-card shades); craft-floor color-system rules exist; no shade-scale slop check. | polish-pass `reference/slop-checklist.md`, "C7 — Color shades & opacities", `SLOP_F22` | placed |
| C8 Containers with borders | partial — `\bbordered\b` hits unrelated; craft-floor "elevation declared once: border OR shadow" + "cards inside cards" rules exist; no bordered-default check. | polish-pass `reference/slop-checklist.md`, "C8 — Containers with borders", `SLOP_F22` | placed |
| C9 Overly detailed diagrams | partial — diagram budget exists (Taste `references/diagrams.md:14`: one diagram a section, two a page at most; fix #15 R2 one diagram by default on software pages); no check that a diagram earns its detail. | polish-pass `reference/slop-checklist.md`, "C9 — Overly detailed diagrams", `SLOP_F22` | placed |
| C10 Verbose, redundant text | partial — `\bverbose\b`/`\bredundant\b` hits unrelated; fix #15 C3 copy-voice rules exist (Taste `copy-voice.md` applies to ALL copy + craft-floor copy checks). Checklist points at them, does not restate them. | polish-pass `reference/slop-checklist.md`, "C10 — Verbose, redundant text", `SLOP_F22` | placed |
| C11 Code breadcrumbs | new — `\bbreadcrumb\b` hits only a Taste asset (`assets/ui/index.json`: a product-window breadcrumb as content); no check. | polish-pass `reference/slop-checklist.md`, "C11 — Code breadcrumbs", `SLOP_F22` | placed |
| C12 Section numbering | partial — polish-pass `reference/lenses/layout.md:109` ("Eyebrow labels and decorative section numbers above every heading") + `impeccable-detector-rules.json:216` ("Tiny numbered section labels") + craft-floor ban (numbers when order carries no meaning); no flag-vs-justified check. | polish-pass `reference/slop-checklist.md`, "C12 — Section numbering", `SLOP_F22` | placed |
| C13 Eyebrows | partial — craft-floor bans eyebrow/kicker labels above every section heading; fix #20 F5 key-label context exists (fixup20b dropped eyebrow/kicker from the F5 examples); Impeccable craft floor bans kickers outright (see C13 note — stricter-wins tension flagged). The flag-vs-justified check is new. | polish-pass `reference/slop-checklist.md`, "C13 — Eyebrows", `SLOP_F22` | placed |
| C14 Dithering | partial — TECHNIQUE exists as less-flat-ui #11 (Dithered images, `less-flat-ui/SKILL.md:261`); the SLOP CHECK is new. | polish-pass `reference/slop-checklist.md`, "C14 — Dithering", `SLOP_F22` | placed |
| C15 ASCII images | partial — TECHNIQUE exists as less-flat-ui #22 (ASCII and pixels, `less-flat-ui/SKILL.md:452`); the SLOP CHECK is new. | polish-pass `reference/slop-checklist.md`, "C15 — ASCII images", `SLOP_F22` | placed |
| C16 Squircles | partial — `polish-details.md:69` allows corner smoothing (squircle) "if the Design System uses it"; no slop check for default use. | polish-pass `reference/slop-checklist.md`, "C16 — Squircles", `SLOP_F22` | placed |
| C17 Excessive mono fonts | partial — craft-floor bans monospace as a "technical" costume; no excessive-mono check. One rule with D4. | polish-pass `reference/slop-checklist.md`, "C17 — Excessive mono fonts", `SLOP_F22` | placed |
| C18 ALL CAPS subtitles | partial — `typeset.md:30/75/90` (all-caps paragraphs are unfinished type; all-caps only on short labels with positive tracking) + Taste `system.md` sentence-case rule; no subtitle-default check. | polish-pass `reference/slop-checklist.md`, "C18 — ALL CAPS subtitles", `SLOP_F22` | placed |
| C19 Gradient backgrounds | partial — craft-floor bans purple-to-blue gradients as the default brand look + `scripts/detect.mjs` slop-gradient rule; no flag-vs-justified check. Technique exists as less-flat-ui #3/#9 (Thermal / Grainy gradients). | polish-pass `reference/slop-checklist.md`, "C19 — Gradient backgrounds", `SLOP_F22` | placed |
| C20 Periods in titles | new — `\bperiod\b` hits unrelated (build.sh comments). Straight check. | polish-pass `reference/slop-checklist.md`, "C20 — Periods in titles", `SLOP_F22` | placed |

## Group D — 20 Ways to Unslop AI Designs (UNSLOP_F22)

| Item | Baseline + grep evidence | Placement (skill + section + anchor) | Status |
|---|---|---|---|
| D1 Delete filler badges | new — "filler badge" 0 hits. | polish-pass `reference/unslop-fixes.md`, "D1 — Delete filler badges", `UNSLOP_F22` | placed |
| D2 Drop redundant labels | partial — `reference/lenses/distill.md:57` ("Remove decorative and redundant elements first"); the fix wording pairing it to C5/C10/C11/C12/C13/C18 is new. | polish-pass `reference/unslop-fixes.md`, "D2 — Drop redundant labels", `UNSLOP_F22` | placed |
| D3 Unitalicize random words | new — "unitalic" 0 hits. One rule with C2. | polish-pass `reference/unslop-fixes.md`, "D3 — Unitalicize random words", `UNSLOP_F22` | placed |
| D4 Mono only where needed | new (as a fix rule) — paired with C17 as one rule; mono-costume ban exists (craft floor) but the fix wording is new. | polish-pass `reference/unslop-fixes.md`, "D4 — Mono only where needed", `UNSLOP_F22` | placed |
| D5 Use a design system | covered-by-architecture — the plugin IS a design system; `ui-ux-pro-max` ("Define the design system before implementing UI") records it in `design-system/<project-slug>/MASTER.md` / `docs/design-tokens.md`. One line, no new rule. | polish-pass `reference/unslop-fixes.md`, "D5 — Use a design system", `UNSLOP_F22` | already-covered |
| D6 Show the actual product | partial — "show the product" hits: Taste `layout-v4.md:157` + craft-floor Persuade rule (a feature section that "shows no product artifact"); the polish-pass fix wording is new. | polish-pass `reference/unslop-fixes.md`, "D6 — Show the actual product", `UNSLOP_F22` | placed |
| D7 Enlarge the main feature | partial — Taste `references/sections-library.md:324` ("One main feature large and four small"); the polish-pass application on any surface is new. | polish-pass `reference/unslop-fixes.md`, "D7 — Enlarge the main feature", `UNSLOP_F22` | placed |
| D8 Group with spacing | partial (pointer) — `ui-ux-pro-max` owns spacing (`references/quick-reference.md`: `spacing-scale`, `whitespace-balance`) + craft-floor spacing rules; fix points at them, does not restate. Pointer spec P6 in `fix22/cd-pointers.md`. | polish-pass `reference/unslop-fixes.md`, "D8 — Group with spacing", `UNSLOP_F22` + pointer spec P6 | pointer spec |
| D9 Make headlines specific | new — "specific headline" 0 hits. Pointer spec P1 in `fix22/cd-pointers.md` (`ui-ux-pro-max` `visual-hierarchy`). | polish-pass `reference/unslop-fixes.md`, "D9 — Make headlines specific", `UNSLOP_F22` + pointer spec P1 | placed + pointer spec |
| D10 Emphasize the CTA | partial — `ui-ux-pro-max` `primary-action` exists (one primary CTA per screen); the emphasis means (size/weight/fill/accent) are new. Pointer spec P2 in `fix22/cd-pointers.md`. | polish-pass `reference/unslop-fixes.md`, "D10 — Emphasize the CTA", `UNSLOP_F22` + pointer spec P2 | placed + pointer spec |
| D11 Add an accent colour | new — the fix wording is new; points at the H1 concept (`ACCENT_F22`), does not duplicate it. | polish-pass `reference/unslop-fixes.md`, "D11 — Add an accent colour", `UNSLOP_F22` | placed |
| D12 Keep icons consistent | partial — craft-floor bans (emoji/Unicode glyphs as the icon system; mixed icon sets) + `reference/lenses/consistency.md` ("Unify icons"); the fix wording is new. | polish-pass `reference/unslop-fixes.md`, "D12 — Keep icons consistent", `UNSLOP_F22` | placed |
| D13 Remove embellishments | partial — "embellish" 0 hits; `reference/lenses/distill.md:57` covers removing decorative/redundant elements; the fix wording pairing it to C5/C6/C8 is new. | polish-pass `reference/unslop-fixes.md`, "D13 — Remove embellishments", `UNSLOP_F22` | placed |
| D14 Inner radius = outer – padding | covered — craft floor (Depth: "Nested corners: inner radius = outer radius − padding between them (pills exempt)") + `reference/lenses/polish-details.md:69`. Point, do not restate. | polish-pass `reference/unslop-fixes.md`, "D14 — Inner radius = outer – padding", `UNSLOP_F22` | already-covered |
| D15 Improve text contrast | covered — the 4.5:1 rule already exists (craft floor Contrast + less-flat-ui). Point, do not restate. Pointer spec P3 in `fix22/cd-pointers.md` (`ui-ux-pro-max` `color-contrast`). | polish-pass `reference/unslop-fixes.md`, "D15 — Improve text contrast", `UNSLOP_F22` + pointer spec P3 | already-covered + pointer spec |
| D16 Wrap headlines properly | partial — craft floor ("Headings use `text-wrap: balance`") + `ui-ux-pro-max` `heading-line-balance` exist; the fix wording (balanced, no orphans, no mid-phrase breaks) is new. Pointer spec P4 in `fix22/cd-pointers.md`. | polish-pass `reference/unslop-fixes.md`, "D16 — Wrap headlines properly", `UNSLOP_F22` + pointer spec P4 | placed + pointer spec |
| D17 Align by eye, not pixels | partial — "align by eye" 0 hits, but `reference/lenses/layout.md:33/76` (optical alignment) + make-interfaces-feel-better Optical Alignment exist; the fix wording is new. | polish-pass `reference/unslop-fixes.md`, "D17 — Align by eye, not pixels", `UNSLOP_F22` | placed |
| D18 Use tabular nums | covered (pointer) — the rule exists: `ui-ux-pro-max` `number-tabular` (SPEC §5 primary) + craft floor ("Numbers in tables and changing values use `font-variant-numeric: tabular-nums`") + make-interfaces-feel-better tabular-nums rule. Pointer spec P5 in `fix22/cd-pointers.md`. | polish-pass `reference/unslop-fixes.md`, "D18 — Use tabular nums", `UNSLOP_F22` + pointer spec P5 | already-covered + pointer spec |
| D19 Add loading states | new — "loading state" hits are only a slot in a spec template (`build.sh:23361`: "[Where result appears, loading state, …]"); the RULE (every async action gets a loading state) is new. | polish-pass `reference/unslop-fixes.md`, "D19 — Add loading states", `UNSLOP_F22` | placed |
| D20 Animate useful feedback | partial (pointer) — animate lens + motion-patterns "Button feedback" exist; the A10/B8 family items belong to the Groups A+B agent; the D20 fix wording + pointer are new. Pointer spec P7 in `fix22/cd-pointers.md`. | polish-pass `reference/unslop-fixes.md`, "D20 — Animate useful feedback", `UNSLOP_F22` + pointer spec P7 | placed + pointer spec |

## H1 / H2 — polish-pass portions only (shared with A+B agent)

The `ui-ux-pro-max` H1 concept and the orchestrate design-package / `ui-ux-pro-max`
H2 hierarchy rules belong to the Groups A+B agent. The rows below are this
agent's polish-pass portion only; the integrator merges them into single H1/H2
rows in the manifest.

| Item | Baseline + grep evidence (polish-pass) | Placement (skill + section + anchor) | Status |
|---|---|---|---|
| H1 Color accents — polish-pass portion (accent sprawl flag) | partial — the one-accent rule exists (craft floor `craft-floor.md:29`: "Product UI: one accent"; distill lens `distill.md:101`: "≤ 1 accent hue"); no named accent-sprawl check existed (`\bsprawl\b` 0 hits in polish-pass). The `ACCENT_F22` sprawl check is new. | polish-pass `reference/slop-checklist.md`, "Accent sprawl — ACCENT_F22", `ACCENT_F22`; fix D11 points at it | placed (polish-pass portion) — shared with A+B agent (`ui-ux-pro-max` concept portion) |
| H2 Accentuation accents — polish-pass portion (hierarchy candidate-evidence check) | partial — the visual half exists (layout lens squint test, `reference/lenses/layout.md:14`: "What do you see 1st, 2nd, 3rd?"); no check on whether a hierarchy is declared in the decision record with first/second/third + means + D19 reasons. The `ACCENTUATION_F22` check is new. | polish-pass `reference/slop-checklist.md`, "Accent hierarchy — ACCENTUATION_F22", `ACCENTUATION_F22` | placed (polish-pass portion) — shared with A+B agent (orchestrate design-package + `ui-ux-pro-max` hierarchy-rules portions) |

## Notes / deviations flagged (not silently changed)

1. **C13 vs the Impeccable craft floor (tension, recorded in the file).** SPEC §4a
   allows an eyebrow as a single deliberate theme-matched key label with a D19
   reason (fix #20 F5). `reference/impeccable-craft-floor.md` states a kicker /
   eyebrow above a heading is a ban no brief earns back. The C13 check follows
   SPEC §4a and records both, applying the stricter rule: a clearance must ALSO
   be recorded as a fix #20 F5 key label with its D19 reason and F6
   justification, covers one deliberate key label only, and a repeated eyebrow
   above every section heading stays a craft-floor ban regardless. Flagged for
   the parent; no adjudication was changed.
2. **Impeccable craft floor not edited.** `reference/impeccable-craft-floor.md`
   is staged verbatim from upstream (its own header says so); the SLOP_F22
   pointer from the detector context was placed in SKILL.md non-negotiable 5
   (detector runs) instead, and the checklist file cross-references the
   Impeccable floor. No verbatim upstream file was touched.
3. **D18 primary home confirmed with a note.** SPEC §5 names `ui-ux-pro-max`
   type rules as primary for tabular numbers — confirmed: `number-tabular`
   exists in `ui-ux-pro-max/references/quick-reference.md:129`. The same value
   also exists in make-interfaces-feel-better (tabular-nums rule + table); the
   pointer spec (P5) records that as a cross-reference, not a second primary.
4. **No slop indicator was turned into a ban.** Every C check carries the
   flag-vs-justified wording and the clearance path (recorded D19 reason +
   theme-fit). The craft-floor bans that already overlap an indicator still
   govern as static checks; the checklist never overrides a ban.
5. **No font rules, screen-verdicts rule, model pins, or marketplace manifest
   touched.** No `bash build.sh` run; the built tree (`hackathon-ecc/`) was not
   edited; `fix11/fix11-stage.py` was not run.
