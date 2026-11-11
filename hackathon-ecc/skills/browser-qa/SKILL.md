---
name: browser-qa
description: "Run automated post-deploy UI verification with a browser automation MCP (claude-in-chrome, Playwright, or Puppeteer): console-error and Core Web Vitals smoke checks, form and auth-flow interaction tests, screenshot visual regression across three breakpoints, and axe-core accessibility audits ending in a SHIP / DO-NOT-SHIP verdict. Use when testing a deployed feature on staging or preview, before shipping frontend changes, reviewing a frontend PR, or checking responsive layout and accessibility."
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

Uses the browser automation MCP (claude-in-chrome, Playwright, or Puppeteer) to interact with live pages like a real user.

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
```

### Phase 3: Visual Regression
```
1. Screenshot key pages at 3 breakpoints (375px, 768px, 1440px)
2. Compare against committed baseline screenshots — when `polish-pass` ran first, use `.polish-pass/captures/after/capture.json` + its PNGs as the committed baseline — no baseline ⇒ report INCONCLUSIVE, never a silent PASS
3. Flag layout shifts > 5px, missing elements, overflow
4. Check dark mode if applicable
```

### Visual iteration loop (run the app, look at the real UI)

Run the app (local dev server, or staging/preview URL) and inspect the ACTUAL rendered interface with Playwright — desktop + mobile viewports — never from source code or a description alone. Each round: capture screenshots, then judge the rendered UI on typography, hierarchy, spacing, alignment, color, contrast, and responsiveness; list the FIVE most noticeable visual/usability problems; fix them; re-inspect. Return the top-5 problem list each round so the caller can decide whether to run another round — the caller caps rounds (max 3, then note diminishing returns and move on). Never claim visual verification without actually inspecting the rendered interface.

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

### Visual
- [✗] Hero section overflows on 375px viewport
- [✓] Dark mode: all pages consistent

### Accessibility
- 2 AA violations: missing alt text on hero image, low contrast on footer links

### Verdict: SHIP WITH FIXES (2 issues, 0 blockers)
# verdict ∈ SHIP / SHIP WITH FIXES / DO NOT SHIP; use INCONCLUSIVE if no visual baseline
```

## Integration

Works with any browser MCP:
- `mChild__claude-in-chrome__*` tools (preferred — uses your actual Chrome)
- Playwright via `mcp__browserbase__*`
- Direct Puppeteer scripts

(The `mChild__*` and `mcp__browserbase__*` tool names are provided by the harness, not by this plugin — no such MCP is defined here. If the harness provides neither, use direct Puppeteer scripts against the running app.)

