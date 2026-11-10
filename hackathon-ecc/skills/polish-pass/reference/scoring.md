# Scoring

How this skill judges a UI: an internal quick score before the pass (polish.md Step 2) and an honest re-score after it (polish.md Step 5). Scores are a working tool, not a deliverable — the report shows the before → after scores, not a full critique report.

## Modes

The mode changes what "good" means:

- **Persuade** (landing, marketing, pricing): earn attention, belief, and action. Distinctiveness matters.
- **Operate** (app, dashboard, admin, settings, tools, charts): task speed, scanability, consistency. Restraint is a virtue.
- **Read** (docs, blog, articles, changelog): comprehension and reading comfort.
- **Experience** (portfolio, gallery, showcase): the work leads; UI recedes.

## Dimensions (0–10 each)

| # | Dimension | 10/10 means |
|---|---|---|
| 1 | **Persona fit** | Every choice serves the users' job, context, and expectations; they'd pick this over competitors |
| 2 | **Hierarchy & clarity** | One obvious focal point per view; purpose and next action clear in 5s; ≤4 competing focal actions at any decision (Hick's law) |
| 3 | **Layout & spacing** | Consistent spacing scale; deliberate rhythm; strong alignment; related things grouped, distinct things separated (proximity, common region); long runs chunked |
| 4 | **Typography** | Clear type scale (adjacent levels ≥1.125× size or ≥200 weight); readable measure (45–75ch); purposeful families; no orphans or ragged headings |
| 5 | **Color & theming** | Purposeful palette from tokens; one accent in product UI, color carries meaning (status, data); status colors reserved for status, decorative lines neutral; meaning never by color alone; dark mode designed (surfaces lighten with elevation), not inverted |
| 6 | **Consistency** | Same thing looks and behaves the same everywhere (similarity), and familiar patterns work as users expect from other products (Jakob's law); no one-off values; one icon family; themeable variables are actually overridable from outside and match their docs |
| 7 | **Responsiveness** | Designed (not merely squeezed) for 390px through 1440px+; tap targets ≥44px (Fitts' law); no horizontal scroll; thumb-reachable primary actions |
| 8 | **Motion & interaction** | Every interactive element has hover/focus/active/disabled states; motion only where it has a purpose and the action isn't high-frequency; right easing (ease-out enter/exit), origin-aware, interruptible; routine UI under 300ms; transform/opacity only, 60fps; reduced-motion respected |
| 9 | **Accessibility** | WCAG 2.2 AA: contrast 4.5:1 text / 3:1 UI, visible focus, keyboard path, semantic HTML, labels, alt text |
| 10 | **Copy** | Specific, human, in brand voice; clear labels and errors; zero filler or lorem |
| 11 | **Robustness & performance** | Loading, empty, error, long-content states designed; every action answers within 400ms (Doherty threshold); no layout shift; LCP < 2.5s on mobile; readable with JS off; images/fonts optimized |

Mark a Dimension `n/a` only if it truly can't apply (e.g. Motion on a static screenshot of a single state). Say why.

## Calibration: be brutal

- **10**: World-class. Nothing to fix. Rare; you should almost never give it.
- **9**: Excellent; only nitpicks left.
- **7–8**: Good, professional work with clear gaps.
- **5–6**: Works, but generic, inconsistent, or rough in places. This is where most shipped UI lands.
- **3–4**: Real problems hurt the user.
- **0–2**: Broken or unusable.

## Levels: place the whole surface first

Before scoring Dimensions, place the surface on this ladder for its mode. It anchors the overall Score; Dimension scores explain *why* it sits there.

| Level | Persuade | Operate | Read / Experience |
|---|---|---|---|
| **2: template** | Centered-hero template, stock/AI imagery, hype copy, doesn't say what it does | Default component-kit look, AI-bright colors, repeated KPIs, dead cards, emoji icons | Default theme, unstyled prose, no hierarchy beyond h1/p |
| **6: clean** | Real structure and copy, one real screenshot; correct but could be any product | Consistent spacing and neutrals, works, but every card/table looks the same and nothing is prioritized | Readable measure and scale, but generic and forgettable |
| **8: considered** | Real product visuals cropped to what sells, clear nav/CTA hierarchy, social proof, motion that explains | Data drives the form, clear focal area, progressive disclosure, all states designed, light and dark both tuned | Typography with a voice, navigable structure, designed code/media/callouts |
| **10: memorable** | One well-built idea only this product could have; personality in hover, 404, empty states | Feels instant (optimistic UI, keyboard paths), invisible UI is designed, power users would pick it over rivals | Reading is a pleasure; details (anchors, TOC, progress, dark mode) are flawless |

Rules:
- Every score cites evidence (a screenshot cell, an element, a file/line).
- The **overall Score is a judgment, not an average.** It's capped by the worst blocker: any Dimension ≤3 caps overall at 6; any craft-floor ban ([craft-floor.md](craft-floor.md)) present caps overall at 7.
- Generic "AI-template" look (the craft-floor slop tells) can't score above 6 on Persona fit for a Persuade surface.
- Each vibe-code tell ([patterns/vibe-code-tells.md](patterns/vibe-code-tells.md)) is a finding. Three or more tells cap the overall Score at 6.
- An action that fails the cold read (looks like plain text at rest) caps Hierarchy & clarity at 6 and the overall Score at 7. Knowing from the code that it is a button doesn't count.
- A section seen only in an error or empty state it wasn't meant to be in is uncaptured: it caps the overall Score at 7 until its success state is captured.
- The overall Score can't exceed the surface's Level by more than 1.
- **Capture every state you know exists before scoring.** If you know about a state (from the UI, the code, or the user's task), you must capture it. Listing it as "not captured" is a miss, not a disclosure. Force each state as [capture.md](capture.md) → "Force every state" describes. Only if a state truly can't be reached (no runnable code, auth you don't have) does it cap the Dimensions that depend on it at 6 and the overall Score at 7: hover, pressed, and tooltip/menu-open states for Motion & interaction; focus-visible for Accessibility; dark mode (when supported) for Color & theming; loading, empty, and error for Robustness. Reading the CSS doesn't count. In that case, ask the user for what you need before reporting.
- Don't inflate to be kind. Don't deflate to seem tough. If it's good, say why precisely.

## Judging through users' eyes

Judge through the eyes of the product's actual users. If the project has no recorded users, use these fallback lenses:

- **First-timer**: new to the category; reads labels literally; needs the first action obvious in 5s; abandons on jargon or ambiguity.
- **Power user**: expert; wants speed, shortcuts, density, bulk actions; hates hand-holding and slow animation.
- **Keyboard & screen-reader user**: tabs linearly, relies on focus, labels, headings, and announced state; zooms to 200%.
- **Mobile skimmer**: one thumb, interrupted, slow network; needs big targets, bottom-reachable actions, fast load, preserved state.

For each, on the device they actually use: first 5 seconds (what do they see first? do they know what this is and what to do?), the primary task (where do they hesitate, misread, or get stuck?), and deal-breakers (does anything block them?). Write what broke for *that* user, naming the element. No generic prose.
