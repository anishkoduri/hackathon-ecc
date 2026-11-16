---
name: browser-qa
description: "Run automated post-deploy UI verification with a browser automation MCP (Playwright or Puppeteer): console-error and Core Web Vitals smoke checks, form and auth-flow interaction tests, screenshot visual regression across three breakpoints, and axe-core accessibility audits ending in a SHIP / DO-NOT-SHIP verdict. Use when testing a deployed feature on staging or preview, before shipping frontend changes, reviewing a frontend PR, or checking responsive layout and accessibility."
metadata:
  origin: ECC
---

# Browser QA — Automated Visual Testing & Interaction

## When to Use

- After deploying a feature to staging/preview
- When you need to verify UI behavior across pages
- Before shipping — confirm layouts, forms, interactions actually work
- When reviewing PRs that touch frontend code
- Accessibility audits and responsive testing

## Debugging order

**Debugging order:** start with symptom inspection; a button that does nothing goes to `click-path-audit` next; everything else with an unknown root cause goes to `systematic-debugging` (which finds the other bug types). `browser-qa` detects deployed-UI failures; `systematic-debugging` diagnoses them.

Handoff: when this skill finds a deployed-UI failure whose root cause is unknown, hand it to `systematic-debugging` with the URL, repro steps, console/network evidence, and screenshots — do not guess a fix from the symptom alone. When the failure is a button that does nothing, hand off to `click-path-audit` first.

## How It Works

Uses the browser automation MCP (Playwright or Puppeteer) to interact with live pages like a real user.

### Safety first — blast radius (run read-only by default)

Browser QA drives real auth and real user journeys, so treat the blast radius explicitly.
Default to **read-only**: never run a **mutating** journey (checkout, payment, delete,
mass-update) against a production URL — require an explicit opt-in **and** a staging/preview
URL. Use seeded **test credentials**, never real production logins, and **redact**
credentials/tokens/PII before saving any screenshot.

### Phase 1: Smoke Test
```
1. Navigate to target URL
2. Check for console errors (filter noise: analytics, third-party)
3. Verify no 4xx/5xx in network requests
4. Check displayed values are real data, not wrong values — NaN, undefined, or empty where data is expected (a page can load cleanly, with no console errors and no failed requests, and still show wrong values)
5. Screenshot above-the-fold on desktop + mobile viewport
6. Check Core Web Vitals: LCP < 2.5s, CLS < 0.1, INP < 200ms
   (INP replaced FID in March 2024; thresholds per web.dev)
```

### Phase 2: Interaction Test
```
1. Click every nav link — verify no dead links
2. Submit forms with valid data — verify success state
3. Submit forms with invalid data — verify error state
4. Test auth flow: login → protected page → logout (test creds only, never prod)
5. Test critical user journeys (checkout, onboarding, search)
   — read-only by default; only exercise mutating journeys against staging
     with explicit opt-in (see "Safety first" above)
6. Dynamic-interface live check (fix #23 §9, DYNAMIC_F23): interact with the app like a user — click/press/hover every interactive control, and sort, filter, expand, and drag where the job calls for it — and confirm the interface responds immediately (press state, hover, transition visible) and that live state moves (data updating, statuses changing, counts and totals moving) rather than frozen mock content. Read the dynamic story from `docs/design-tokens.md` / the decision record (per surface: what changes, what triggers it, how it moves) and confirm each state change observed is choreographed (motion present — entering/leaving, loading to loaded, empty to filled, selected, confirmed). A control that does not respond, or a state that changes without motion, FAILS the build. If the harness cannot drive an interaction the job calls for, record that interaction as unverified — a gap, never a silent pass; the Dynamic row is not ✓ on an interaction never driven. Read-only by default; only exercise mutating journeys against staging with explicit opt-in (see "Safety first" above).
```

### Phase 3: Visual Regression

**Alignment assertions (fix #23 §6, ALIGN_F23).** Eyeballing screenshots is not a check: run these programmatic assertions wherever the harness allows, on the live rendered page via `getBoundingClientRect()`. Tolerances: 0px for overflow; ≤ 2px for centering / grid / spacing equality. (a) No horizontal overflow at any tested width (`scrollWidth - innerWidth == 0`); no leaf text element with `scrollWidth > clientWidth + 1`. (b) Hero / phone frame centered in the viewport (offset ≤ 2px); at the mid band, if side panels share the row, the hero GROUP is centered with equal outer margins ≤ 2px. (c) Nav items evenly spaced (adjacent gaps equal ± 2px) and the nav group centered; each label center == its item center ± 2px. (d) Card edges aligned to a common left/right grid: full-width children share one left and one right edge (± 2px); a narrower child is left-aligned or centered; feed cards share one left and one right edge. (e) No text clipped or overflowing its container; no element beyond its frame unless a declared intentional bleed recorded in the decision record (page overflow still 0). (f) No label collisions: diagram / SVG text boxes pairwise non-overlapping and inside the viewport; stamps centered on their parent ± 2px; status pairs judged by vertical CENTERS, not tops. (g) Primary actions centered on their axis: grouped inputs centered on their panel ± 2px; full-width actions share the grid edges, narrower ones centered. (h) Desktop side panels: gutters symmetric ± 2px, tops aligned ± 2px unless a stagger is recorded in the decision record; stacked mid-band blocks centered as a group. Full checklist (candidate evidence): `polish-pass` reference/alignment.md (`ALIGN_F23`) — sub-checks `ALIGN_F23_NAV` (nav items evenly spaced and centered), `ALIGN_F23_LABELS` (no label collisions — diagrams, strips, stamps), `ALIGN_F23_CLIP` (no text clipped, no element escaping its frame), `ALIGN_F23_ACTIONS` (primary actions centered on their axis), `ALIGN_F23_PANELS` (desktop side panels symmetric and top-aligned).
```
1. Screenshot key pages at 3 breakpoints (375px, 768px, 1440px)

Widths (fix #23 §6, COVER_F23): 1440 desktop, 900 mid-band default probe (band 768–1100), 390 mobile — these three widths supersede the 375 / 768 / 1440 breakpoints in step 1 above for alignment coverage. If a layout breakpoint falls inside 768–1100, probe at the breakpoint ± 1 as well and take a mid full-page composition shot.
2. Compare against committed baseline screenshots — when `polish-pass` ran first, use `.polish-pass/captures/after/capture.json` + its PNGs as the committed baseline — no baseline ⇒ report INCONCLUSIVE, never a silent PASS
Single capture run (CAPTURE1_F27): `polish-pass` captures once; `browser-qa` consumes those captures and shoots only what the capture matrix lacks — never re-shoot a state/width the polish-pass captures already cover.
3. Flag layout shifts > 5px, missing elements, overflow

Coverage is MANDATORY for EVERY flow state, not just the happy path (COVER_F23): enumerate all screens × all reachable states — error / wrong-code, empty, success / delivered, accepted, scrolled positions — and measure + screenshot each at all three widths. A build with an unverified width or an unverified flow state is NOT shippable (BLOCK_F23, see the verdict rule below).
4. Check dark mode if applicable
5. Functionality check (fix #23 §5, FUNC-BQA_F23): the build shows HOW it works early — its mechanism (diagram / live data / system state) is visible on the hero surface or the first screen after it, theme-matched, naming THIS build's pipeline, data, and stack with the product's own names and real figures. A build that looks good but hides what the thing does FAILS, even with zero layout findings. A generic diagram relabelled with generic words does not pass.
```

### Visual iteration loop (run the app, look at the real UI)

Run the app (local dev server, or staging/preview URL) and inspect the ACTUAL rendered interface with Playwright — desktop + mobile viewports — never from source code or a description alone. Each round: capture screenshots, then judge the rendered UI on typography, hierarchy, spacing, alignment, color, contrast, responsiveness, and distinctiveness — this skill is the SOLE executor of the distinctiveness bar inside the visual loop: before rendering a verdict in any round, read `.hallmark/candidate-evidence.md` if it exists in the project root and treat its entries as candidate evidence (screen + what reads as a template), never as a verdict; the orchestrator passes this file as a standing input to the visual loop, not from memory. on every enumerated screen, check that a named direction (generated through the package skills, recorded in `docs/design-tokens.md` or the decision record) is visibly applied (tokens, type, colour, spacing trace to it); a screen with no named direction, no applied theme/tokens, reading as a default template, or derivative (the design is based on a searched external reference) FAILS — report it as a distinctiveness finding (minor at least) with the top-5 list, so the caller routes it to the fix loop within the existing caps.

**Type-audit verdict (fix #23 §3, TYPEAUDIT_F23).** Typography that reads as defaulted fails here, on the rendered screen: before rendering a verdict in any round, read the type-audit table from `.hallmark/candidate-evidence.md` (per-face visual shares, trio-vs-previous-build comparison, variety count — recorded by `polish-pass`, TYPEAUDIT_F23) alongside the other candidate evidence. A type-audit FAIL — the body face over 40% of the build's visual share (or over 55% on any primary screen), the display face(s) under 25% of the build's visual share, the display face losing to the body face on the hero/home surface, the trio (`TRIO_F23`) identical to the previous build's trio with no recorded reuse reason, or fewer distinct faces than the variety floor (max(3, ceil(N/20)) for N Type-list text elements, each counted face at least 5% share) — is a distinctiveness finding (minor at least) that FAILS the build, routed back to the design skill for a re-deal of the trio or a re-balance of the shares. A hit cleared in the decision record by its recorded reason (trio reuse) or scoped exception (body-led build, display floor still binding) is not a FAIL — the clearance is cited in the verdict, never assumed. Only this skill renders the type-audit verdict; `polish-pass` records the evidence, never the verdict. No other step judges screen distinctiveness — the blind reviewer checks only the recorded direction, and sloplint app scope does not carry it. List the FIVE most noticeable visual/usability problems; fix them; re-inspect. Return the top-5 problem list each round so the caller can decide whether to run another round — the caller caps rounds (max 3, then note diminishing returns and move on). Never claim visual verification without actually inspecting the rendered interface.

**Hero verdict — amazing is the bar (fix #23 §4, HERO-BQA_F23).** In the visual loop, the hero surface — a landing hero, or the home/feed surface of an app — carries the highest weight: judge it against the hero-moment line recorded in `docs/design-tokens.md` and the Picks block's Hero-moment row (a dealt moment + a distinctive composition + motion). A merely adequate hero — correct but unremarkable — FAILS F6, however correct the rest of the screens are. Calibration: on a phone-first utility app the home/feed surface IS the hero surface; the amazing bar is calibrated to the product's job, not to decoration — the moment must serve what the user opens the app to do. "Amazing" never means a generic hero section pasted onto an app that does not need one. This verdict is `browser-qa`'s alone: no other step judges the hero.

**Memorability verdict — memorable is the bar, above F6 (fix #23 §1, MEMORABLE_F23).** At the finish review, browser-qa judges memorability as the TOP criterion, above the F6 impressive bar: dynamic (it moves and responds), over the top (it goes beyond adequate in ambition, elements, and motion), wow / striking / stunning (it hits on first sight and on use). Judge it across the enumerated screens — the hero surface carries the highest weight (HERO-BQA_F23), but a memorable hero on a forgettable build does not pass. A build the user would forget the next day FAILS, however rule-correct — this extends the hero verdict (a merely adequate hero fails F6) and the F6/impressive verdicts: rule-correct but unambitious, unimpressive, or forgettable all fail. "Over the top" is ambition and impact, not loudness for its own sake: "more, not bolder" still governs styling (do not just crank weight, color, or size) — a build can be over the top and quiet in palette; it cannot be forgettable. This verdict is `browser-qa`'s alone: no other step judges memorability.
**Beat-v5 benchmark verdict (fix #25 §4(d), BENCHMARK_V5_F25).** At the finish review, score the four live benchmark dimensions from `skills/orchestrate/references/design-benchmark-v5.md` §2 against the v5 figures — hero strength (full v5 hero inventory AND the R4 hero loop applied OR a second dealt moment applied in/near the hero), dynamic interface (≥ 9 interactive items with ≥ 2 cross-surface state drives), functionality (≥ 3 live-data surfaces with real state; the mechanism on the hero/first screen), alignment (0 problems across the full coverage matrix) — and render each as beat-v5 PASS / FAIL in the report. The static dimensions (element count, variety) are scored from the decision record's beat-v5 table (orchestrate step 5a static check), never re-judged here; the four live dimensions are this skill's verdict alone — a dimension that cannot be scored live is recorded as owed, never as passed. A tie on any dimension is below the bar on that dimension.
**Design-decision pointer:** F2/F3/F4/F5/F6/D19/B1/X1 as relevant — design-package rule — Taste step 4a / orchestrate.

### Phase 4: Accessibility
```
1. Run axe-core or equivalent on each page
2. Flag WCAG 2.2 AA violations (contrast, labels, focus order)
3. Verify keyboard navigation works end-to-end
4. Check screen reader landmarks
```

> Note: axe-core automatically covers roughly 30–40% of WCAG. A clean run is **necessary,
> not sufficient** — keyboard nav, focus order, and a screen-reader pass still need a manual
> check. Don't report "accessible" from an automated pass alone.

## Output Format

```markdown
## QA Report — [URL] — [timestamp]

### Smoke Test
- Console errors: 0 critical, 2 warnings (analytics noise)
- Network: all 200/304, no failures
- Displayed values: real data shown — no NaN / undefined / empty where data is expected
- Core Web Vitals: LCP 1.2s ✓, CLS 0.02 ✓, INP 89ms ✓

### Interactions
- [✓] Nav links: 12/12 working
- [✗] Contact form: missing error state for invalid email
- [✓] Auth flow: login/logout working
- [✓/✗] Dynamic (DYNAMIC_F23): controls respond immediately; every state change choreographed (motion present); live state, not frozen mock content
- [✓/✗] Memorability (MEMORABLE_F23): dynamic + over the top + wow / striking / stunning — the build is memorable tomorrow, not merely correct today
- [✓/✗] Beat-v5 benchmark (BENCHMARK_V5_F25): hero / dynamic / functionality / alignment vs the v5 figures — PASS / FAIL per dimension (a tie is below the bar; an unscored dimension is owed, never passed)

### Visual
- [✗] Hero section overflows on 375px viewport

### Alignment (fix #23 §6, ALIGN_F23)
- [✓/✗] Overflow: 0px at 1440 / 900 / 390; text overflow: 0 elements
- [✓/✗] Centering: frame / hero-group offset ≤ 2px at every width
- [✓/✗] Nav: gaps equal ± 2px, group centered, labels centered on items
- [✓/✗] Grid: card edges share one left / one right per width
- [✓/✗] Clipping / collisions: 0 clipped, 0 label collisions, 0 undeclared beyond-frame
- [✓/✗] Actions: primary actions centered on their axis ± 2px
- [✓/✗] Coverage: every width × every flow state measured + screenshotted (BLOCK_F23: any gap → DO NOT SHIP)
- [✓] Dark mode: all pages consistent

### Accessibility
- 2 AA violations: missing alt text on hero image, low contrast on footer links

### Verdict: SHIP WITH FIXES (2 issues, 0 blockers)
# verdict ∈ SHIP / SHIP WITH FIXES / DO NOT SHIP; use INCONCLUSIVE if no visual baseline

**Blocking-gap rule (fix #23 §6, BLOCK_F23).** A build with an unverified width or an unverified flow state is NOT shippable — the gap is a blocking finding, not a note. Missing coverage → blocking finding → verdict DO NOT SHIP. A coverage matrix with an empty cell is never reported as SHIP, SHIP WITH FIXES, or INCONCLUSIVE-as-pass; the matrix is complete or the build does not ship.
```

## Integration

Works with any browser MCP:
- Playwright via `mcp__browserbase__*`
- Direct Puppeteer scripts

(The `mChild__*` and `mcp__browserbase__*` tool names are provided by the harness, not by this plugin — no such MCP is defined here. If the harness provides neither, use direct Puppeteer scripts against the running app.)

