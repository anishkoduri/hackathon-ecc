# Vercel web-design-guidelines — dedupe table (fix #22 §16)

**Source pinned:** `vercel-labs/web-interface-guidelines`, file `command.md`,
commit `4ecfb9fb8d1d3b7009674869b3aaee2f904042e1`, dated 2026-10-05
("Add desktop overscroll guideline"). Repo HEAD at check time (2026-11-12):
`434b7f91364665f2f733b310ec54809bf8f37937` — no `command.md` change after the
pin, so the pin IS the current ruleset. **136 rows accounted for, zero
unaccounted:** 90 `command.md` rules + 14 anti-patterns + 32 rules found only
in the same repo's `AGENTS.md` (same pinned commit; not part of the fetched
ruleset — see the AGENTS.md note at the end).

**Dispositions:** `already-covered` = an enforceable rule/check with the same
effect already exists in the plugin (cited); `partial` = the concept exists
elsewhere in the plugin but the Vercel rule as a polish-pass `file:line` check
is new; `new` = no existing rule; `duplicate-of` (anti-patterns only) = the
anti-pattern restates a numbered rule; `conflict` = parent adjudication.
Already-covered rules are still LISTED in the checklist (a pinned snapshot
with holes is not a snapshot) but carry a `Covered by:` pointer instead of new
fix guidance — cited, not duplicated. Partial rules are listed with the
pointer plus what the check adds.

**Evidence base:** greps over `build.sh` (23,735 lines), the built tree
`hackathon-ecc/skills/`, and staged `round2-skills/polish-pass/`. Counts
quoted are from those greps (Nov 12, 2026). `build.sh` alone is NOT the whole
plugin: upstream-clone skills (ui-ux-pro-max, accessibility, frontend-a11y)
live in the built tree, and polish-pass staged sources live in
`round2-skills/` — citations name the real home.

## 1. command.md rules (90)

### Accessibility (V-A1–V-A12)

| ID | Vercel rule (short) | Disposition | Existing-rule citation / note |
|---|---|---|---|
| V-A1 | Icon-only buttons need `aria-label` | partial | Concept in `accessibility` skill (labeling, SKILL.md:26,75,88) + `frontend-a11y` (10 hits); no polish-pass `file:line` check. Check is new. |
| V-A2 | Form controls need `<label>` or `aria-label` | partial | Concept in `accessibility` skill (primary-label table, SKILL.md:75); check is new. |
| V-A3 | Interactive elements need keyboard handlers (`onKeyDown`/`onKeyUp`) | partial | `accessibility` skill:43 "reachable via keyboard"; the handler form is new. |
| V-A4 | `<button>` for actions, `<a>`/`<Link>` for navigation (not `<div onClick>`) | partial | `accessibility` skill:119 "Div-Buttons" anti-pattern; polish-pass check is new. |
| V-A5 | Images need `alt` (or `alt=""` if decorative) | partial | `frontend-a11y` alt (3 hits); `accessibility` skill:122 "Redundant Alt Text"; check is new. |
| V-A6 | Decorative icons need `aria-hidden="true"` | partial | `accessibility` skill:89 example; `frontend-a11y` (8 hits); check is new. |
| V-A7 | Async updates (toasts, validation) need `aria-live="polite"` | partial | `accessibility` skill:55,78; `frontend-a11y` (4 hits); check is new. |
| V-A8 | Use semantic HTML before ARIA | partial | `accessibility` skill (semantic, 8 hits) + description "semantic ARIA roles and labels"; check is new. |
| V-A9 | Headings hierarchical `<h1>`–`<h6>`; include skip link | partial | Impeccable detector `skipped-heading` (quality) covers hierarchy; skip link is new. `design-taste-frontend` SKILL.md:559 also names `heading-order`, `skip-link` as checks. |
| V-A10 | `scroll-margin-top` on heading anchors | new | 0 hits in `build.sh`, accessibility, frontend-a11y. |
| V-A11 | Meaningful media needs captions, transcripts, or descriptions | new | 0 hits for caption/transcript in `accessibility` / `frontend-a11y` SKILL.md. |
| V-A12 | Media controls need keyboard support; decorative media needs assistive-tech hiding | partial | Keyboard support is general in the `accessibility` skill; the media-specific application is new. |

### Focus States (V-F1–V-F5)

| ID | Vercel rule (short) | Disposition | Existing-rule citation / note |
|---|---|---|---|
| V-F1 | Interactive elements need visible focus (`focus-visible:ring-*` or equivalent) | partial | `accessibility` skill:43 "visible focus indicator"; `design-taste-frontend` SKILL.md:559 names `focus-ring`, `focus-visible` as checks; the `focus-visible:ring-*` form as a polish check is new. |
| V-F2 | Never `outline-none` / `outline: none` without focus replacement | new | 0 hits for "outline" in `accessibility`, `frontend-a11y`, polish-pass craft floor. |
| V-F3 | Use `:focus-visible` over `:focus` | partial | `design-taste-frontend` SKILL.md:559 names `focus-visible`; the preference rule is new. |
| V-F4 | Group focus with `:focus-within` for compound controls | partial | Named only as a check token in `design-taste-frontend` SKILL.md:559; the rule is new. |
| V-F5 | Sticky headers/footers/overlays must not cover the focused element | already-covered | `ui-ux-pro-max` quick-reference `focus-not-obscured` (line 25): "Sticky UI, overlays, and banners must not hide the keyboard-focused control (WCAG 2.2 AA)". Same rule. |

### Forms (V-FO1–V-FO11)

| ID | Vercel rule (short) | Disposition | Existing-rule citation / note |
|---|---|---|---|
| V-FO1 | Inputs need `autocomplete` and meaningful `name` | partial | `frontend-a11y` shows `autoComplete="email"` / `"current-password"` as code examples (lines 113, 134) but states no rule; polish-pass check is new. |
| V-FO2 | Correct `type` (`email`, `tel`, `url`, `number`) and `inputmode` | new | 0 hits in `build.sh` for `inputmode`. |
| V-FO3 | Never block paste (`onPaste` + `preventDefault`) | new | 0 hits. |
| V-FO4 | Labels clickable (`htmlFor` or wrapping control) | partial | Label concept in `accessibility` skill; the `htmlFor`/wrapping form is new. |
| V-FO5 | Disable spellcheck on emails, codes, usernames (`spellCheck={false}`) | new | 0 hits in `build.sh` for `spellCheck`. |
| V-FO6 | Checkboxes/radios: label + control share single hit target (no dead zones) | partial | Plugin hit-area rule already exists (44x44px minimum, the plugin floor — Group A A14 / G8; quick-reference `touch-target-size` 44x44pt / 48x48dp); the checkbox/radio single-target application is new. |
| V-FO7 | Submit button stays enabled until request starts; spinner during request | partial | Quick-reference `loading-buttons` ("Disable button during async operations; show spinner") + Group D D19 loading-states rule cover the spinner half; "stays enabled until request starts" is new. |
| V-FO8 | Errors inline next to fields; focus first error on submit | new | Quick-reference `error-feedback` ("Clear error messages near problem") does not state inline placement or focus-first-error. |
| V-FO9 | Placeholders end with `…` and show example pattern | new | `frontend-a11y`:413–414 covers placeholder-as-label (bad); the `…` + example-pattern rule is new. |
| V-FO10 | `autocomplete="off"` on non-auth fields | new | 0 hits. |
| V-FO11 | Warn before navigation with unsaved changes (`beforeunload` or router guard) | new | 0 hits in `build.sh` for `beforeunload`. |

### Animation (V-AN1–V-AN8)

| ID | Vercel rule (short) | Disposition | Existing-rule citation / note |
|---|---|---|---|
| V-AN1 | Honor `prefers-reduced-motion` | already-covered | `motion-foundations` rule 3 (line 116) + line 389 ("`prefers-reduced-motion: reduce` — disables all transforms"); polish-pass SKILL.md:98 default standard ("reduced motion"). |
| V-AN2 | Animate `transform`/`opacity` only | already-covered | `motion-foundations` rule 4 (line 117): "Never animate layout properties… Use `transform` and `opacity` only." |
| V-AN3 | Never `transition: all` — list properties explicitly | already-covered | Polish-pass `reference/polish.md:70` (fix example: `transition: all 300ms` → `transition: transform 160ms var(--ease-out)`); `motion-foundations` rule 4 (layout props banned) is adjacent. |
| V-AN4 | Set correct `transform-origin` | new | 0 hits in `motion-foundations` / `motion-patterns` / `motion-advanced` SKILL.md. |
| V-AN5 | SVG: transforms on `<g>` wrapper with `transform-box: fill-box; transform-origin: center` | new | 0 hits. |
| V-AN6 | Animations interruptible — respond to user input mid-animation | already-covered | Glossary G18 interruptible animation (`design-taste-frontend/references/design-glossary.md`, `GLOSSARY_F22`); `motion-patterns` B14 "Don't tween while held" is the related rule (SPEC §5); `motion-foundations`:519 pointer. |
| V-AN7 | Autoplay motion >5 seconds alongside other content needs pause, stop, or hide controls | new | 0 hits. |
| V-AN8 | Muted decorative loops must stop under `prefers-reduced-motion` | already-covered | Same rule as V-AN1 applied to loops (`motion-foundations`:389, :413). |

### Typography (V-T1–V-T6)

| ID | Vercel rule (short) | Disposition | Existing-rule citation / note |
|---|---|---|---|
| V-T1 | `…` not `...` | new | 0 hits for an ellipsis rule in polish-pass craft floor / lenses. |
| V-T2 | Curly quotes `“` `”` not straight `"` | new | 0 hits. |
| V-T3 | Non-breaking spaces: `10&nbsp;MB`, `⌘&nbsp;K`, brand names | new | 0 hits. |
| V-T4 | Loading states end with `…`: `"Loading…"`, `"Saving…"` | partial | Group D D19 loading-states rule covers loading states; the `…` form is new. |
| V-T5 | `font-variant-numeric: tabular-nums` for number columns/comparisons | already-covered | Polish-pass craft floor:89; `reference/lenses/typeset.md`:61,80; quick-reference `number-tabular` + CD-P5 `tabular-polish`. |
| V-T6 | `text-wrap: balance` or `text-pretty` on headings (prevents widows) | already-covered | Group D D16 headline wrapping + quick-reference `heading-line-balance` + CD-P4 `headline-wrap-polish`. |

### Content Handling (V-C1–V-C4)

| ID | Vercel rule (short) | Disposition | Existing-rule citation / note |
|---|---|---|---|
| V-C1 | Text containers handle long content: `truncate`, `line-clamp-*`, or `break-words` | partial | Impeccable detector `text-overflow` + `clipped-overflow-container` (quality) cover overflow symptoms; the truncate/line-clamp/break-words prescription is new. |
| V-C2 | Flex children need `min-w-0` to allow text truncation | new | 0 hits in `build.sh`. |
| V-C3 | Handle empty states — don't render broken UI for empty strings/arrays | partial | Polish-pass scope already covers "loading/empty/error states" (SKILL.md description); the "no broken UI for empty strings/arrays" check is new. |
| V-C4 | User-generated content: anticipate short, average, and very long inputs | new | 0 hits. |

### Images (V-I1–V-I3)

| ID | Vercel rule (short) | Disposition | Existing-rule citation / note |
|---|---|---|---|
| V-I1 | `<img>` needs explicit `width` and `height` (prevents CLS) | partial | Layout-shift QA flag ("Flag layout shifts > 5px"), motion M2 1500ms fail-safe, craft floor:71 ("Background work never moves the page") cover shift symptoms; the explicit-dimensions rule is new. |
| V-I2 | Below-fold images: `loading="lazy"` | new | 0 hits in `build.sh` for `loading="lazy"`. |
| V-I3 | Above-fold critical images: `priority` or `fetchpriority="high"` | new | 0 hits. |

### Performance (V-P1–V-P8)

| ID | Vercel rule (short) | Disposition | Existing-rule citation / note |
|---|---|---|---|
| V-P1 | Large lists (>50 items): virtualize | new | 0 hits in `build.sh` for `virtualiz`. |
| V-P2 | No layout reads in render (`getBoundingClientRect`, `offsetHeight`, `offsetWidth`, `scrollTop`) | new | `getBoundingClientRect` appears only in polish-pass `scripts/capture.mjs` (a measurement script, not a rule). |
| V-P3 | Batch DOM reads/writes; avoid interleaving | new | 0 hits for a batching rule. |
| V-P4 | Prefer uncontrolled inputs; controlled inputs must be cheap per keystroke | new | `react-patterns` shows `value`/`onChange` usage examples only (SKILL.md:297), no rule. |
| V-P5 | Add `<link rel="preconnect">` for CDN/asset domains | new | 0 hits in `build.sh` for `preconnect`. |
| V-P6 | Critical fonts: `<link rel="preload" as="font">` with `font-display: swap` | new | No conflict with the fix #19/#20/#21 self-hosted-static-fonts rule: preload is compatible with self-hosted fonts; it does not introduce a new font or a CDN fetch. |
| V-P7 | Prefer `<video autoplay muted loop playsinline>` over animated GIF; provide a still alternative | new | 0 hits for an animated-GIF rule. |
| V-P8 | Short non-essential loops: Safari H.264 MP4 `<picture>` source, `prefers-reduced-motion` media condition, still fallback | new | 0 hits. |

### Navigation & State (V-N1–V-N4)

| ID | Vercel rule (short) | Disposition | Existing-rule citation / note |
|---|---|---|---|
| V-N1 | URL reflects state — filters, tabs, pagination, expanded panels in query params | new | No UI deep-link rule in the plugin (`build.sh` query-param hits are all API/backend skills). |
| V-N2 | Links use `<a>`/`<Link>` (Cmd/Ctrl+click, middle-click support) | partial | V-A4 covers the element choice; the Cmd/Ctrl+click + middle-click support requirement is new. |
| V-N3 | Deep-link all stateful UI (if uses `useState`, consider URL sync via nuqs or similar) | new | 0 hits. |
| V-N4 | Destructive actions need confirmation modal or undo window — never immediate | new | No destructive-confirmation rule exists (the one `build.sh` "destructive" hit is the fix #22 A10 insert text, not a rule). |

### Touch & Interaction (V-TO1–V-TO7)

| ID | Vercel rule (short) | Disposition | Existing-rule citation / note |
|---|---|---|---|
| V-TO1 | `touch-action: manipulation` | already-covered | Quick-reference `tap-delay` (line 45): "Use touch-action: manipulation to reduce 300ms delay (Web)". |
| V-TO2 | `-webkit-tap-highlight-color` set intentionally | new | 0 hits in `build.sh` for `tap-highlight`. |
| V-TO3 | `overscroll-behavior: contain` in modals/drawers/sheets | new | 0 hits in `build.sh` for `overscroll`. |
| V-TO4 | Page rubber-band suppression: `overscroll-behavior: none` on `<html>` inside `@media (pointer: fine)`; keep coarse-pointer page defaults for pull-to-refresh; test hybrid touch devices | new | The 2026-10-05 delta rule — the one rule ECC's 2026-09-21 snapshot lacks. 0 hits. |
| V-TO5 | During drag: disable text selection, `inert` on dragged elements | new | 0 hits. |
| V-TO6 | Drag/swipe/pinch/path gestures need tap/click and keyboard alternatives unless essential | partial | Quick-reference `gesture-alternative` ("Don't rely on gesture-only interactions; always provide visible controls"); the keyboard-alternative requirement is new. |
| V-TO7 | `autoFocus` sparingly — desktop only, single primary input; avoid on mobile | new | 0 hits in `build.sh` for `autoFocus`. |

### Safe Areas & Layout (V-S1–V-S3)

| ID | Vercel rule (short) | Disposition | Existing-rule citation / note |
|---|---|---|---|
| V-S1 | Full-bleed layouts need `env(safe-area-inset-*)` for notches | partial | Group G G13 safe area: pointer in `ui-ux-pro-max` (`references/pro-rules.md`:53 safe-area compliance; :74 touch targets + safe areas) + quick-reference `safe-area-awareness`; the explicit `env(safe-area-inset-*)` rule is new. |
| V-S2 | Avoid unwanted scrollbars: `overflow-x-hidden` on containers, fix content overflow | partial | Impeccable detector `first-viewport-column-overflow`, `body-text-viewport-edge`, `text-overflow` (quality) cover symptoms; the `overflow-x-hidden` prescription is new. |
| V-S3 | Flex/grid over JS measurement for layout | partial | Layout-shift rules + motion rules prefer declarative layout; the explicit "over JS measurement" rule is new. |

### Dark Mode & Theming (V-D1–V-D3)

| ID | Vercel rule (short) | Disposition | Existing-rule citation / note |
|---|---|---|---|
| V-D1 | `color-scheme: dark` on `<html>` for dark themes | new | 0 hits in `build.sh` for `color-scheme`. |
| V-D2 | `<meta name="theme-color">` matches page background | new | 0 hits in `build.sh` for `theme-color`. |
| V-D3 | Native `<select>`: explicit `background-color` and `color` (Windows dark mode) | new | 0 hits. |

### Locale & i18n (V-L1–V-L4)

| ID | Vercel rule (short) | Disposition | Existing-rule citation / note |
|---|---|---|---|
| V-L1 | Dates/times: use `Intl.DateTimeFormat` not hardcoded formats | new | 0 hits in `build.sh` for `Intl.`; `i18n-sync` skill (139 lines) states no `Intl` rule. |
| V-L2 | Numbers/currency: use `Intl.NumberFormat` not hardcoded formats | new | Same as V-L1. |
| V-L3 | Detect language via `Accept-Language` / `navigator.languages`, not IP | new | 0 hits. |
| V-L4 | Brand names, code tokens, identifiers: wrap with `translate="no"` | new | 0 hits. |

### Hydration Safety (V-H1–V-H3)

| ID | Vercel rule (short) | Disposition | Existing-rule citation / note |
|---|---|---|---|
| V-H1 | Inputs with `value` need `onChange` (or use `defaultValue` for uncontrolled) | new | `react-patterns` shows `value`/`onChange` in examples only; no rule. |
| V-H2 | Date/time rendering: guard against hydration mismatch (server vs client) | new | 0 hits. |
| V-H3 | `suppressHydrationWarning` only where truly needed | new | 0 hits in `build.sh`. |

### Hover & Interactive States (V-HO1–V-HO2)

| ID | Vercel rule (short) | Disposition | Existing-rule citation / note |
|---|---|---|---|
| V-HO1 | Buttons/links need `hover:` state (visual feedback) | partial | Craft floor:33 ("Interactive states: hover and pressed each move one step off rest") + quick-reference `press-feedback` / `hover-vs-tap`; the "need a `hover:` state" check is new. |
| V-HO2 | Interactive states increase contrast: hover/active/focus more prominent than rest | already-covered | Craft floor:24 (every pair passes in light AND dark, and in hover, active, selected, disabled states) + :33 (one step off rest). Same rule. |

### Content & Copy (V-CC1–V-CC7)

| ID | Vercel rule (short) | Disposition | Existing-rule citation / note |
|---|---|---|---|
| V-CC1 | Active voice: "Install the CLI" not "The CLI will be installed" | new | No active-voice rule in `design-taste-frontend` `references/copy-voice.md` (grep 0). |
| V-CC2 | Title Case for headings/buttons (Chicago style) | new | No Title Case rule in `copy-voice.md` (grep 0). |
| V-CC3 | Numerals for counts: "8 deployments" not "eight" | new | No numerals rule in `copy-voice.md` (grep 0). |
| V-CC4 | Specific button labels: "Save API Key" not "Continue" | partial | Group D D9 / CD-P1 `headline-specific` cover specific headlines; the button-label application is new. |
| V-CC5 | Error messages include fix/next step, not just problem | partial | Quick-reference `error-feedback` ("Clear error messages near problem"); the fix/next-step requirement is new. |
| V-CC6 | Second person; avoid first person | new | No second-person rule in `copy-voice.md` (grep 0). |
| V-CC7 | `&` over "and" where space-constrained | new | 0 hits. |

**Count check §1:** Accessibility 12 + Focus 5 + Forms 11 + Animation 8 +
Typography 6 + Content Handling 4 + Images 3 + Performance 8 + Navigation 4
+ Touch 7 + Safe Areas 3 + Dark Mode 3 + Locale 4 + Hydration 3 + Hover 2 +
Copy 7 = **90 rules**. Disposition totals: already-covered **10** (V-F5, V-AN1,
V-AN2, V-AN3, V-AN6, V-AN8, V-T5, V-T6, V-TO1, V-HO2); partial **29** (V-A1–A9,
A12; V-F1, F3, F4; V-FO1, FO4, FO6, FO7; V-T4; V-C1, C3; V-I1; V-N2; V-TO6;
V-S1, S2, S3; V-HO1; V-CC4, CC5); new **51**. 10 + 29 + 51 = 90. (The
coordinator re-counts from the table; the table rows are authoritative, not
this paragraph.)

## 2. Anti-patterns (V-AP1–V-AP14) — all restate a numbered rule, except AP1

| ID | Anti-pattern | Disposition |
|---|---|---|
| V-AP1 | `user-scalable=no` or `maximum-scale=1` disabling zoom | **new** — no corresponding rule in the Rules groups and 0 hits in `build.sh` for `user-scalable`. Ported as its own check (V-AP1) in the checklist. |
| V-AP2 | `onPaste` with `preventDefault` | duplicate-of V-FO3 |
| V-AP3 | `transition: all` | duplicate-of V-AN3 |
| V-AP4 | `outline-none` without focus-visible replacement | duplicate-of V-F2 |
| V-AP5 | Inline `onClick` navigation without `<a>` | duplicate-of V-A4 |
| V-AP6 | `<div>` or `<span>` with click handlers (should be `<button>`) | duplicate-of V-A4 |
| V-AP7 | Images without dimensions | duplicate-of V-I1 |
| V-AP8 | Large arrays `.map()` without virtualization | duplicate-of V-P1 |
| V-AP9 | Form inputs without labels | duplicate-of V-A2 |
| V-AP10 | Icon buttons without `aria-label` | duplicate-of V-A1 |
| V-AP11 | Hardcoded date/number formats (use `Intl.*`) | duplicate-of V-L1 / V-L2 |
| V-AP12 | `autoFocus` without clear justification | duplicate-of V-TO7 |
| V-AP13 | Animated GIF when compressed video is suitable | duplicate-of V-P7 |
| V-AP14 | Gesture-only action without tap/click and keyboard alternative | duplicate-of V-TO6 |

**Count check §2:** 14 anti-patterns = 13 duplicates + 1 new (V-AP1). No
anti-pattern is unaccounted for.

## 3. AGENTS.md-only rules (same pinned repo, same pinned commit — NOT part of the fetched ruleset)

The rules repo ships a second file, `AGENTS.md`, at the same pinned commit.
The upstream skill fetches `command.md` only, and ECC's snapshot mirrors
`command.md` only — so these 32 rules are **recorded here, not ported** into
the checklist. The coordinator decides whether to fold any of them in (a
follow-up patch to the checklist appendix); the default is defer, except the
one conflict, which needs parent adjudication either way.

| ID | AGENTS.md-only rule (short) | Disposition |
|---|---|---|
| AG1 | Hit target ≥24px (mobile ≥44px); expand hit area if visual <24px | already-covered — plugin rule is stricter (44x44px minimum, the plugin floor — Group A A14 / G8; quick-reference `touch-target-size` 44x44pt / 48x48dp). |
| AG2 | Mobile `<input>` font-size ≥16px to prevent iOS zoom | new (defer) |
| AG3 | Manage focus (trap, move, return) per APG patterns | partial — `accessibility` skill:121 "Uncontained Modal Focus" anti-pattern; the trap/move/return rule is new. |
| AG4 | Enter submits focused input; in `<textarea>`, ⌘/Ctrl+Enter submits | new (defer) |
| AG5 | Trim values to handle text-expansion trailing spaces | new (defer) |
| AG6 | Allow incomplete form submission to surface validation | new (defer) |
| AG7 | Back/Forward restores scroll position | new (defer) |
| AG8 | Optimistic UI; reconcile on response; on failure rollback or offer Undo | partial — relates to V-N4 (confirmation/undo); the optimistic-UI rule is new. |
| AG9 | Delay first tooltip; subsequent peers instant | new (defer) |
| AG10 | If it looks clickable, it must be clickable | partial — relates to V-A4 + quick-reference `cursor-pointer`; the rule as stated is new. |
| AG11 | Skeletons mirror final content to avoid layout shift | partial — layout-shift rules exist; the skeleton prescription is new. |
| AG12 | `<title>` matches current context | new (defer) |
| AG13 | No dead ends; always offer next step/recovery | partial — relates to V-CC5 (error next-step); the general rule is new. |
| AG14 | Redundant status cues (not color-only); icons have text labels | partial — quick-reference `visual-hierarchy` ("not color alone"); the status-cue rule is new. |
| AG15 | Layered shadows (ambient + direct) | new (defer) — distinct from `less-flat-ui` Soft Shadow #23, which is a texture treatment, not a shadow-layering rule. |
| AG16 | Nested radii: child ≤ parent; concentric | already-covered — Group D D14 "Inner radius = outer – padding" is the same rule (`UNSLOP_F22` D14). |
| AG17 | Hue consistency: tint borders/shadows/text toward bg hue | new (defer) |
| AG18 | Accessible charts (color-blind-friendly palettes) | new (defer) |
| AG19 | Meet contrast — prefer APCA over WCAG 2 | **conflict — parent adjudication.** The plugin enforces WCAG 4.5:1 (craft floor:21; polish-pass SKILL.md:115). AGENTS.md prefers APCA over WCAG 2. If AGENTS.md is ever folded in, the parent decides: keep WCAG 4.5:1 (standing rule) or adopt APCA. Until then, WCAG 4.5:1 stands and APCA is not woven. |
| AG20 | Avoid dark color gradient banding (use background images when needed) | partial — relates to slop C19 (gradient backgrounds); the banding rule is new. |
| AG21 | Test iOS Low Power Mode and macOS Safari | new (defer) — test practice, not a code rule; belongs to browser-qa's domain if ever woven. |
| AG22 | Measure reliably; track/minimize re-renders; profile with CPU/network throttling | new (defer) — process, not a code rule. |
| AG23 | Mutations (`POST`/`PATCH`/`DELETE`) target <500ms | new (defer) — performance budget, not in the plugin. |
| AG24 | Verify mobile, laptop, ultra-wide (simulate ultra-wide at 50% zoom) | new (defer) — QA practice; browser-qa's domain if ever woven. |
| AG25 | Optical alignment; adjust ±1px when perception beats geometry | already-covered — Group D D17 "Align by eye, not pixels" is the same rule (`UNSLOP_F22` D17). |
| AG26 | Balance icon/text lockups (weight/size/spacing/color) | new (defer) |
| AG27 | Inline help first; tooltips last resort | new (defer) |
| AG28 | Prefer CSS > Web Animations API > JS libraries | new (defer) |
| AG29 | Never animate layout props (`top`, `left`, `width`, `height`) | already-covered — `motion-foundations` rule 4 (line 117), same as V-AN2. |
| AG30 | Animate only to clarify cause/effect or add deliberate delight | partial — Group D D20 "animate useful feedback" is the same family; the rule as stated is new. |
| AG31 | Choose easing to match the change (size/distance/trigger) | new (defer) |
| AG32 | Autoplay only for muted, non-essential loops | partial — V-AN7 (controls) + V-AN8 (reduced-motion) cover the controls half; the "muted, non-essential only" restriction is new. |

**Count check §3:** 32 AGENTS.md-only rules = already-covered 4 (AG1, AG16,
AG25, AG29) + partial 9 (AG3, AG8, AG10, AG11, AG13, AG14, AG20, AG30, AG32)
+ new 18 (AG2, AG4, AG5, AG6, AG7, AG9, AG12, AG15, AG17, AG18, AG21, AG22,
AG23, AG24, AG26, AG27, AG28, AG31) + conflict 1 (AG19). 4 + 9 + 18 + 1 = **32**.
(Coordinator re-counts from the table rows.)

## 4. Totals

- `command.md` rules: 90 (already-covered 10, partial 29, new 51).
- Anti-patterns: 14 (13 duplicate-of, 1 new — V-AP1).
- AGENTS.md-only: 32 (already-covered 4, partial 9, new 18, conflict 1).
- **Grand total accounted for: 136. Unaccounted: 0.**
- Conflicts needing parent adjudication: **1** — AG19 (APCA vs WCAG 4.5:1).
  No `command.md` rule conflicts with an existing plugin rule; the only
  tension is V-P6 (font preload) vs the self-hosted-fonts rule, resolved in
  the table: preload is compatible with self-hosted fonts, no conflict.
