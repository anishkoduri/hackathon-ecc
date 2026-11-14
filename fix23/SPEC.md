# Fix #23 SPEC — Ambition, motion, fonts, hero, functionality, alignment

## §0 Origin — the failure it fixes

Anish's verdict on the Home Run render (Nov 12, ~20:53 CST): "pretty good for
the idea we made a demo for, but for other stuff id like there to be more
creativity and just more elements and eye-catching motion and design choices
made and accepted and designs implemented, and the fonts defaulted too much...
overall solid but id like it to make more design decisions overall and make
the hero amazing, but i get for this app it doesn't need to be like that so
it's fine, we also want to instill the sense of functionality bc the biggest
thing our apps nd websites are is groundbreaking in the technical sense, so
just weave everything throughout, and make the orchestrator come up with an
ambitious and outside the box design using all the elements available to it."
Plus (Nov 12, ~20:53 CST): "make sure everything is centered and aligned
properly, tighten those checks up."

The render's own facts (parent-verified): the fonts were NOT missing. All 5
static woff2 faces loaded (0 failed requests). The design record chose
Schibsted Grotesk 700 for display, Fraunces 400/500 for body, DM Mono for
figures. The failure is that the body face (Fraunces, the Tiempos stand-in
under F4) is the page's base font, and in an app most visible text IS body
text, so Fraunces carried the whole page by volume. The render was also NOT
built by the plugin in Cursor — a coordinator read the skill files and built
it. So the defaulted feel is a design-decision failure, not an environment
failure. Fix #23 fixes the decisions and the checks, in the plugin, so the
plugin itself produces ambitious designs.

Standing rules that do NOT change: "more, not bolder"; anti-derivative (no
design based on a searched reference); D19 (every decision recorded with
reasons across all seven dimensions incl. Depth); browser-qa is the SOLE
executor of pass/fail verdicts on rendered screens; fonts are static
instances, self-hosted, never a variable file, no system-ui fallback;
fix #22 adjudications stand (slop = flags never bans, trends = menu never
defaults, /demo never automatic).

## §1 Ambition — the orchestrator designs outside the box, using ALL elements

The orchestrator must come up with an ambitious, outside-the-box design that
uses ALL the elements available to it — not a safe subset.

- THE CORE (Anish, Nov 12): dynamic + over the top + wow + striking +
  stunning + above all MEMORABLE is the core. This is the governing bar,
  above F6's impressive: a build the user forgets the next day fails,
  however rule-correct. Browser-qa judges memorability as the top
  criterion — dynamic (it moves and responds), over the top (it goes
  beyond adequate in ambition, elements, and motion), wow / striking /
  stunning (it hits on first sight and on use). "Over the top" is ambition
  and impact, not loudness for its own sake: "more, not bolder" still
  governs styling (do not just crank weight, color, or size). A build can
  be over the top and quiet in palette; it cannot be forgettable.

- The design package step (orchestrate) must RECORD which elements of the
  available inventory were used on this build AND which were considered and
  rejected, with D19 reasons: ui-ux-pro-max styles/palettes/font pairings/
  icons/GSAP presets/chart types/stacks; Taste + Hallmark theme deal + dealt
  moments; less-flat-ui treatments (all 23); motion-foundations principles +
  laws and motion-patterns tokens (§22 Groups A–B); the 11 fix #22 asset
  libraries/tools where they fit (§11/§15/§17, menu not defaults, one
  WebGL-heavy effect per surface); Depth (§13, strategy named per surface);
  Thinking Orbs for AI waiting states (§14); the Vercel pinned-snapshot
  checklist as candidate evidence (§16).
- THE INVENTORY (the mechanism — Anish, Nov 12): the reason designs come
  out thin is that the orchestrator and design-lead do not know what is
  available. Build ONE inventory catalog file (in the design package,
  referenced from orchestrate's design-package step and from the
  design-lead prompt): every design element available, grouped by owning
  skill, each with a one-line description, where it lives, and when to
  reach for it. It must cover: ui-ux-pro-max (styles, palettes, font
  pairings, UX guidelines, icons, GSAP presets, chart types, stacks);
  Taste (hero + dealt moments, finish gate); Hallmark (50-theme catalog,
  sloplint, hero/finish reviews); Impeccable (detector rules, craft
  floor); less-flat-ui (all 23 treatments); motion-foundations /
  motion-patterns / motion-advanced (principles, laws, tokens, examples);
  polish-pass (slop checklist, unslop fixes, Vercel pinned-snapshot
  checklist, accent checks); design-system; make-interfaces-feel-better;
  the fix #22 additions (glossary terms, H1/H2 accents, Mobbin pattern
  research, direct-don't-describe, the 11 asset libraries/tools, Bang
  Motion layer, Depth tokens, Thinking Orb states); and the skill-bundled
  reference inventories (palette/font/icon/theme/pattern catalogs). The
  orchestrator and design-lead READ the inventory at the design-package
  step BEFORE deciding, and the decision record cites inventory entries
  used vs considered-and-rejected. A design that could have been made
  without the package — one that uses none of the inventoried elements
  beyond the bare minimum — fails the ambition bar. The inventory is kept
  current: any future fix that adds elements updates it in the same
  change.
- A build that uses only a small slice of the available inventory without
  recorded considered-and-rejected reasons for the rest FAILS the ambition
  bar. "Considered and rejected" must be specific (why this element does not
  serve this build), never a blanket line.
- Ambition is MORE elements, MORE motion, MORE decisions — not louder.
  "More, not bolder" stands. A build that is loud but thin still fails.
- F6 (impressive is the governing bar) is now the PRIMARY gate: browser-qa
  judges impressive AND ambitious, not just rule-correct. A rule-correct but
  unambitious design fails. Memorability (THE CORE above) sits above F6:
  impressive is the floor, memorable is the bar.

## §2 Motion — eye-catching motion is the default, not an afterthought

- Every build ships deliberate, eye-catching motion: entrances, staggers,
  dealt moments, micro-interactions, state transitions — routed through the
  fix #22 motion tokens (Group A principles + Group B values, e.g. stagger
  30ms, press scale 0.97, dropdowns 150–250ms). A build that feels static
  fails, even if every static rule passes.
- Motion is recorded in the decision record with its D19 reason (Motion
  dimension) and its token values, directed per §10 (direct, don't describe).
- `prefers-reduced-motion` is respected everywhere with a static fallback;
  the fallback is a complete design, not a broken one.

## §3 Fonts — no defaulting

- The failure: the body stand-in (Fraunces) must never be the visually
  dominant face. The display/important faces must carry the visual identity.
- F7 strengthened: every text element gets a distinctive artistic font
  decision, AND the decision record must show VARIETY across the build. The
  trio "one display face + body stand-in + mono" is a pattern, not a default:
  the trio itself is re-chosen per build (Hallmark already deals type; the
  pairing must be re-dealt, not inherited from the previous build), and a
  build that reuses the previous build's trio without a recorded reason
  fails.
- The coordinator designs the exact mechanism and the check. Minimum: a
  type-audit step in polish-pass (candidate evidence, never a verdict) that
  records, per build, the distinct faces used, the share of visible text
  carried by each face, and whether the trio matches the previous build's.
  A build whose typography reads as defaulted — one face dominating the
  visual field, or the same trio as the last build without a recorded reason
  — fails at browser-qa.
- The Tiempos/Fraunces stand-in rule (F4) stands: Fraunces is for long body
  text and small incidental text ONLY. What changes is the enforcement: the
  body face may not dominate, and the display faces must do more of the
  visible work.

## §4 Hero — the hero must be amazing

- The hero surface (a landing hero, or the home/feed surface of an app)
  gets a dealt amazing moment: a dealt moment + a distinctive composition +
  motion, recorded in the decision record. The hero is the highest-weight
  browser-qa surface. A merely adequate hero fails F6.
- Calibration: for a phone-first utility app like Home Run, the home/feed
  surface IS the hero surface and still gets the moment treatment, but the
  amazing bar is calibrated to the product — the moment must serve the
  product's job, not decorate it. "Amazing" never means a generic hero
  section pasted onto an app that does not need one.

## §5 Functionality — instill the sense that the thing is technically groundbreaking

- The design must surface the technical depth: show HOW it works. A
  mechanism diagram, live figures, the pipeline, data flowing, the stack,
  the live system state — as a first-class surface, theme-matched, not an
  afterthought.
- R2 (one diagram by default on software pages) is strengthened into a
  functionality requirement: every build shows its mechanism (diagram /
  live data / system state) somewhere the user sees it early. F2 stack
  labels stand.
- The decision record states the functionality story: what is technically
  new here, and how the design shows it. A build that looks good but hides
  what the thing does fails.

## §6 Alignment and centering — everything aligned properly, checks tightened

- The failure: the Home Run render shipped with alignment verified only by
  eyeballing screenshots. The 768–1100px layout was never screenshotted;
  mobile flow states (offer/accepted/delivered/wrong-code) were never
  screenshotted. Eyeballing is not a check.
- New checks (browser-qa + polish-pass; browser-qa remains sole verdict
  executor, everything else is candidate evidence):
  (a) Programmatic alignment assertions wherever the QA harness allows:
      no horizontal overflow at any tested width; the hero/phone frame
      centered in the viewport; nav items evenly spaced and centered;
      card edges aligned to a common left/right grid; no text clipped or
      overflowing its container; no label collisions (diagrams, strips,
      stamps); primary actions centered on their axis.
  (b) Screenshot coverage is MANDATORY at three widths (desktop 1440, mid
      768–1100, mobile 390) and for EVERY flow state, not just the happy
      path.
  (c) A build with an unverified width or an unverified flow state is NOT
      shippable — the gap is a blocking finding, not a note.
- The coordinator defines the exact assertion list and the coverage matrix
  and implements them in the QA harness (qa.mjs / browser-qa / polish-pass
  as fits each). The Home Run render alignment audit (running in parallel,
  Nov 12) is the first consumer: its findings feed the assertion list.

## §7 Non-goals

- No new skill unless the manifest justifies it.
- No platform conversion (the fix #13 rule stands: a stated platform is
  never silently converted).
- Do not re-litigate fix #22 adjudications (§4 flags, the /demo gates, the
  Casberry bar, APCA informational, template-fonts self-host follow-up).
- Do not change the first-build sequence (grill → scope → expansion →
  build → verify → polish → deploy → commit → README → final report;
  /demo never automatic).

## §9 Dynamic interface (Anish, Nov 12)

The interface is DYNAMIC, not static. Every build's interface must feel
alive and responsive, not like a frozen page.

- Live and reactive: surfaces show live state (data updating, statuses
  changing, counts and totals moving) rather than frozen mock content.
  Interactive elements respond immediately: press states, hover,
  transitions, state changes.
- Motion as behavior, not decoration: every state change is choreographed
  (motion tokens, dealt moments) — entering/leaving, loading to loaded,
  empty to filled, selected, confirmed. A state change with no motion is
  a gap.
- Interactive depth: the interface invites interaction (sortable,
  filterable, expandable, draggable where it serves the job). The user can
  DO things, not just look.
- The decision record states the dynamic story per surface: what changes,
  what triggers it, how it moves.
- Placement: the dynamic-interface requirements go into the design-package
  step, the motion skills, and the QA checks. Browser-qa verifies state
  changes LIVE: it interacts with the app and confirms the interface
  responds. A build whose controls do not respond, or whose states change
  without motion, fails.
- Calibration: dynamic never means gratuitous. Motion serves the state
  change; the reduced-motion fallback stays complete. This section works
  with §2 (motion), §4 (hero moments), and §5 (functionality made
  visible — live data IS the functionality showing).

## §8 Verification criteria

- Audit #70 (or next number): ZERO blocking, ZERO minor.
- Sweep (next number): CLEAN, weaving-coherence CLEAN for all §1–§6 and §9.
- Dry-run (next number): fixtures covering each section PASS; a live
  render (or the Home Run render, re-run through the tightened checks)
  passes the new alignment assertions at all three widths and all states.
- verify23.py: checks for every placement, exit 0.
- Prior verifiers: re-run; fails must be only the frozen post-fix21
  fingerprint + the less-flat-ui diff-hunk pattern + cascades. No
  regressions. Prior verifiers are NOT edited.
- Banned terms: 0 in the built tree. Counts and pins unchanged unless the
  manifest justifies a change.
- Manifest: fix23/MANIFEST.md, written by a script, with the disposition
  table, the anchor tokens, the open parent adjudications, and the
  dry-run caveat if any check is environment-limited.
