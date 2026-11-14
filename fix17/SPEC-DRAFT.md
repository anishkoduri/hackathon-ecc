# Fix #17 — rule-change spec DRAFT (implementer brief, read with fix15/BASELINE.md)

**Status:** DRAFT for coordinator review — analysis only. No plugin file was
edited to produce this spec, `build.sh` was not run, the Campus Eats artifact
was not touched.

**Model:** this spec follows the structure of `fix15/SPEC.md`. Its counting
rule is `fix15/BASELINE.md` (one discrete, deliberate design application,
recorded in `docs/design-tokens.md`, one count per application, instances
count individually, kinds by BASELINE precedence). Its starting state is the
fix #15 state: build.sh 23,217 lines, md5
`1f1a232572b9e12332733688838e1233`; counts 169 skills / 72 agents / 123 rules /
96 commands / 15 hooks; last clean: Audit #53 ZERO, dry-run #25 CLEAN, sweep
#15 CLEAN; Campus Eats re-trace after fix #15: **30 elements** (Component 18,
Treatment 3, Visual 1, Motion 3, Moment 2, Type 2, Effect 0, Diagram 1).

**Concurrency warning — read first.** Fix #16 is concurrently editing the
tree (model-pin scrub). ALL file:line anchors cited in this spec are from the
pre-fix16 built tree and are therefore **provisional**: the implementer must
re-verify every anchor against the tree as it stands when implementing, and
must NOT touch model pins (fix #16 owns those). If the starting state differs
from the one above (line count / md5 / counts), stop and report before editing.

Starting-state verification (implementer, FIRST, before any edit): `wc -l` +
`md5sum` on build.sh; if it differs from 23,217 /
`1f1a232572b9e12332733688838e1233`, stop and report.

## Standing constraints (do NOT weaken any of these)

- "More, not bolder" (orchestrate :94, standalone :40).
- browser-qa is the SOLE executor of pass/fail verdicts on rendered screens.
  Everything else is guidance / candidate evidence / static checks, never a verdict.
- Impeccable craft-floor bans are absolute as static checks (no kicker/eyebrow,
  no gradient text; same-size icon+heading+text cards pattern and hero-metric
  template are candidate evidence for browser-qa, never a rewrite on this check
  alone). Hallmark floor binds. No violet. Anti-derivative rule.
  Snapshot-before-redesign. Shared fresh-verdict budget 2 rounds.
- Do NOT re-flag adjudicated items (explicit --domain plain search serves
  reference rows only; hooks/adapter.js is live Cursor infrastructure;
  byte-identical assets are not defects; agent-emit-pi.js dead code is Pi-native).
- NEVER re-run fix11/fix11-stage.py (it would clobber the fix-#12 critique.md edits).
- No new inventory (no new treatments, skills, or themes) unless a genuine gap
  is found — the point is usage of what exists. The 1500ms fail-safe (M2) is a
  code pattern inside the existing motion skills, not new inventory; if the
  implementer finds no fitting home for it, flag it as a genuine gap — do not
  silently invent a skill to hold it.
- Edit staged sources only (standalone skill sources where the plugin copies them,
  e.g. less-flat-ui lives at ~/workspace/cursor-skills/); NEVER edit the built
  tree directly — the build regenerates it. If a build.sh runtime patch anchor
  must change, change the anchor, keep the diff minimal, save a backup
  (build.sh.before-fix17).
- Do NOT commit, bundle, touch GitHub, or touch the Campus Eats artifact.

## A. The fix #17 rules

Each rule quotes the existing rule it builds on, then gives the exact
proposed new-rule text. Every rule is an enforceable, checkable rule (a
required step or checklist item with a record, not a wish). All placements
below are provisional (see the concurrency warning).

### U1 — Unique page-only elements: at least three per build

Builds on the fix #15 canonical variety block (fix15 SPEC §A, in all 11
files), which already requires variety across kinds and per-surface recording
in `docs/design-tokens.md`:

> "Every build applies design elements across a wide variety of kinds —
> treatments, moments, effects, diagrams, components, motion, and type
> moments — never all of one kind … Every element application is recorded
> per surface in `docs/design-tokens.md` (surface → elements applied, kind,
> theme-fit)."

and on Taste step 4a's anti-generic principles:

> "never a generic AI-dashboard look — no excessive gradients, no grid of
> repetitive look-alike cards, no decorative clutter that carries no
> information; every choice is deliberate typography, spacing, alignment,
> and contrast, and a surface that adds nothing is cut."

Neither yet forces a build to contain anything that exists nowhere else.
Proposed new rule (place in Taste step 4a, after the R5 line, and as a step-6
static check; mirror the check in orchestrate Verify step 6 and
orch-build-mvp step 6; app surfaces record theirs in
`design-system/<project-slug>/MASTER.md`, conforming to the tokens file):

> **Unique page-only elements — at least three per build (fix #17 U1).**
> Every build invents at least THREE unique, one-of-a-kind elements and
> records them in the "Unique elements" list in `docs/design-tokens.md`.
> "Unique" means ALL FOUR: (1) page-only — the element occurs on exactly
> one page of this build and is not repeated on any other page or surface
> of the same build (a repeated instance is one element used twice, not
> two unique elements — and a repeated element is a pattern, not unique);
> (2) not a reusable pattern — it is not built from a sections-library
> recipe, a ui-ux-pro-max pattern, a dealt moment, a Range pattern element,
> a less-flat-ui treatment, a hero spec, or any other catalogue item in any
> skill; (3) not in any skill's catalogue — no skill file names it, depicts
> it, or prescribes it as an option; (4) invented for that page through the
> skills — generated from the dealt theme's material world (its material,
> tokens, palette balance, and do-nots) to serve one section's job. Each
> list entry names the element, its surface, its kind (BASELINE.md counting
> rule), the section job it serves, the theme material it draws on, and why
> it is not a catalogue item. At least one of the three must sit on the
> primary page. A build whose Unique list has fewer than three complete
> entries is incomplete — a static check item in step 6, never a screen
> verdict. Each unique element counts once under the BASELINE.md counting
> rule, as its kind.

Checkable form: the step-6 static check reads the Unique list — count of
complete entries ≥ 3, at least one on the primary page, every entry carrying
all six fields. The "not in any skill's catalogue" limb is checked by the
reviewer (grep the element's name/description against the skills) and
recorded in the entry's "why not a catalogue item" field — it is a
human-checked record, not a script assertion.

Expected on the Campus Eats re-trace: **+3** (the fix #15 after-state's five
new elements do NOT satisfy U1 — iris-opens, the diagram, the second
treatment kind, the hero loop, and the lone figure are all rule-compelled
applications of dealt/catalogue items, not inventions). Illustrative
possibilities only — the dry-run invents its own, and the spec does NOT
hard-code which: e.g. a die-cut price-tag tab on the price-ladder card, a
sticker-peel corner on the Bento lead tile, a lime "open now" stamp-chip
inside the app-frame spot rows. Any invented element must also respect the
Sticker do-nots recorded in the tokens file (never a soft blurred drop under
a raised surface on the landing page; never a die-cut border thinner than
4px or in any colour but white; never pink text on the paper; never a drawn
sticker/mascot/doodle).

### T1 — Type fills its bubble: display/figure/label type sized to its container

Builds on fix #15 C3 (Taste step 6 :290), which records the Type list but
sets no fill requirement:

> "Copy + type checks enforced and recorded (fix #15 C3). Taste copy-voice
> rules apply to ALL copy; craft-floor type checks (body measure 65–75ch,
> obvious scale/weight steps, balanced headings, contrast 4.5:1 / 3:1 large)
> are verified per surface and recorded in `docs/design-tokens.md`'s Type
> list (surface → face/size/measure/contrast)."

and on the Sticker theme's own type-on-fill rule (sticker.md:46, cited in
dry-run #25):

> "a lone figure on a fill may run to 12rem; it is the loudest thing the
> theme owns, so one a screen."

Proposed new rule (place in Taste step 6, extending the C3 check, and in the
Taste step 4a Typography line; mirror in the ui-ux-pro-max type-scale step
and the polish-pass harmony check):

> **Type fills its bubble (fix #17 T1).** For every display, figure, or
> label type set inside a bounded container — a tile, card, bubble, chip,
> tag, badge, stat fill, or price-ladder cell — the size is chosen so the
> type fills its container: the rendered glyph bounding box must span at
> least 60% of the container's inner width where the layout fills
> horizontally, or at least 60% of its inner height where it fills
> vertically, measured in-page (glyph box vs container box) and recorded
> per surface in `docs/design-tokens.md`'s Type list as surface →
> face/size → container inner size → fill ratio. Bounded by no-overflow (no
> text clipped or spilling its container at 1440 or 390) and no-crowding
> (type never touches the container edge — the inset is at least the
> theme's own padding/rhythm token — and adjacent type runs never collide;
> the existing check.mjs collision/overflow findings govern). The step-6
> screenshot check includes a dead-space item: a bubble, card, or tile
> whose largest empty band exceeds 25% of its minor dimension is a finding,
> fed to the fix batch like other checks. Flowing body copy is not a bubble
> — the C3 body-measure rule (65–75ch) governs there, not this rule.

Checkable form: the fill ratio is a computed number per Type-list row
(glyph box / container box along the fill axis, minimum 0.60), verified in
the step-6 check; the dead-space item is a screenshot-check finding. The
60% threshold and the 25% band are PROPOSED numbers — no existing text
states them. The dry-run must confirm the 60% threshold is attainable on
the Campus Eats re-trace (e.g. the R5 lone figure) without breaking the
theme; if it is not attainable, the threshold lowers — the theme does not
bend. See "Could not be made fully checkable" in §E: the dead-space band
is a screenshot judgment, not a computed number.

Expected on the Campus Eats re-trace: **+0 elements** (a sizing rule, not
a new element — unless a fill-driven new Type element is invented, in which
case it counts under U1, not here).

### F1 — Every font decision cites the type system (extends C1–C3, does not reimplement them)

Builds on fix #15 C1 + C2 (Taste step 4a :246; ui-ux-pro-max :89):

> "The dealt pairing is the ONLY permitted faces on the build — no other
> face is introduced — and the pairing + its source are recorded in
> `docs/design-tokens.md` (fix #15 C1). Display faces are self-hosted
> (bundled woff2 + `@font-face` in the built page) whenever the face's
> character matters — the closest installed font is a failure, not a
> fallback; body faces name their source (self-hosted or link) and fallback
> stack in `docs/design-tokens.md` (fix #15 C2)."

C1–C3 already fix WHICH faces and record face/size/measure/contrast. They
do not yet require every weight, size, and tracking choice — including
labels, captions, tags, chips, numerals, and the app-frame's UI type — to
cite its source, and they do not yet forbid a value that is a default.
Proposed new rule (place in Taste step 4a, extending the Typography line,
and as a step-6 static check; mirror in the ui-ux-pro-max type-scale step
and the polish-pass harmony check at :22):

> **Every font decision cites the type system (fix #17 F1 — extends fix
> #15 C1–C3, does not replace them).** Every face, weight, size, and
> tracking value on the page is an explicit value from the skills' type
> system — the dealt pairing (Taste step 4a / ui-ux-pro-max type scale),
> the theme file's type voice, or the `system.md` Type scale step. No face,
> weight, size, or tracking on the page is a browser or framework default,
> and no value is chosen flat (unstated, inherited, "whatever it came
> with"). The Type list in `docs/design-tokens.md` gains two columns —
> weight and tracking — and every row gains a Source cell naming the exact
> skill text the choice comes from (pairing line, theme-file line, or scale
> step). A row with an empty Source cell, a Source of "default", or a value
> that traces to no recorded pairing/scale/theme line is an incomplete
> build — a static check item in step 6, never a screen verdict. The
> polish-pass harmony check verifies the Type list including the Source
> cells (consistency only — a surface whose type does not trace to the
> recorded pairing/scale is a harmony divergence, recorded as candidate
> evidence, never a verdict). App surfaces record theirs the same way in
> `design-system/<project-slug>/MASTER.md`, conforming to the tokens file.

"**Cites the type system**" means concretely: one recorded Source cell per
Type-list row, naming a specific skill text (file + line or named rule),
covering face, size, weight, and tracking together. A row whose Source cell
says "dealt pairing, step 4a" with the pairing recorded satisfies it; a row
whose Source cell says "default" or is blank does not.

Expected on the Campus Eats re-trace: **+0 elements** (a recording rule,
not a new element). It does close a gap dry-run #25 noted: the baseline
tokens file names the faces (Bowlby One SC + Sofia Sans) but no source.

### M1–M6 — Motion / interactivity density: the v4-level motion set as the default

**Terminology flag — no file anchor.** No file in the tree defines a "v4
motion set": the string "v4" occurs only in `layout-v4.md` (the Taste
layout system), which contains no motion set by that name, and no file
contains a 1500ms fail-safe (the only 1500ms in the tree is an unrelated
settle wait, `consistency.mjs:7178`). The rule text below IS the definition
of the set — six sub-items, each an enforceable check. The implementer must
not invent a "v4" source to cite.

Builds on: Taste step 4a's motion line and `references/motion.md`:

> "motion / micro-interactions (hero entrance, hover/press, the dealt
> moments — house rule 5, `motion.md`; for motion beyond the page system's
> own entrance and moments … decide feel and timing with
> `make-interfaces-feel-better` first, then implement with the motion-*
> skills (`motion-foundations`, `motion-patterns`, `motion-advanced`))"

> "Every page loads the micro-interaction layer … **It is not optional:**
> never remove, skip or override it … Give it markup to act on: a linked
> card is a `.card` holding its link … buttons are `.btn` … Shoot a
> hovered card and a hovered photograph at 1440 and see them change: the
> card 2px up, the photograph at 1.03."

and on motion-patterns' scroll-reveal pattern (rule 7 + the scroll-reveal
example):

> "7. **Scroll reveals use `viewport={{ once: true }}`.** Repeating on
> scroll-out is distracting, not informative." — with
> `whileInView={{ opacity: 1, y: 0 }}` and `viewport={{ once: true,
> margin: "-80px" }}`.

and on motion-foundations' accessibility / SSR rules:

> "`prefers-reduced-motion: reduce` — disables all transforms, limits
> opacity transitions to ≤ 0.2s" … "Rule: `initial` must always match what
> the server renders."

**Scope conflict — read before implementing.** Taste `references/motion.md`
also says, in the same file the rules above come from:

> "**Scrolling moves nothing but the dealt moment.** No card, row or tile
> ever fades, rises or staggers in as the page scrolls (stock reveals), no
> text moves at another speed than the page (parallax on text), and the page
> is never held or steered by script …"

and `layout-v4.md:90` says "No scroll tricks: no scroll-snap,
scroll-jacking or smooth-scroll library. The one exception: the big scene
(tech) and a dealt scroll moment (every kind, `moments.md`) run inside their
own [section]." Scroll entrances (M1) therefore CONFLICT with the Taste page
system as written. The spec resolves this by scoping M1 to the surfaces the
motion-* skills already govern (React/Next.js app surfaces, where
motion-patterns' scroll-reveal is the standing pattern) and keeping the
Taste ban on landing pages. Coordinator decision (see §E):

- **Option A:** amend `references/motion.md` to permit scroll entrances on
  landing pages too. This is the larger change — it rewrites a house rule —
  and on the Campus Eats re-trace it would add one Motion element per
  scrolled section, pushing the count above the §C band.
- **Option B (recommended):** keep the Taste ban; M1 applies to
  motion-*-governed app surfaces only. The re-trace prediction in §C
  assumes Option B.

Proposed new rules (place M1–M2 and M6 in the motion-* skills —
motion-foundations for the fail-safe pattern and reduced-motion gating,
motion-patterns for the scroll-reveal pattern — and M3–M5 in
make-interfaces-feel-better's Motion section + checklist; record all six in
the Motion list in `docs/design-tokens.md` and check them in Taste step 6 /
orchestrate Verify step 6 as static checks, never screen verdicts):

> **M1 — Scroll entrances on motion-governed surfaces.** On surfaces
> governed by the motion-* skills (React/Next.js app surfaces), each
> content section enters on scroll: `whileInView` with `viewport={{ once:
> true }}` (motion-patterns rule 7), using motion-foundations tokens. Each
> entrance is recorded per surface in `docs/design-tokens.md`'s Motion list
> (surface → entrance → tokens used). A section with no entrance and no
> recorded reason is an incomplete build — a static check item in step 6,
> never a screen verdict. SCOPE: the design-taste-frontend page system
> keeps its standing rule (`references/motion.md`: "Scrolling moves nothing
> but the dealt moment") — scroll entrances do NOT apply to Taste landing
> pages under this rule.

> **M2 — 1500ms fail-safe: content can never stay hidden.** Every
> scroll-entrance element becomes fully visible within 1500ms of entering
> the viewport even if its observer never fires: a timed fail-safe (a timer
> or CSS fallback that forces the visible state — opacity 1, transform none
> — 1500ms after mount/entry) is a required part of every entrance
> implementation, and its presence is recorded in the Motion list (surface
> → entrance → fail-safe mechanism). The step-6 check scrolls to each
> section, waits 1500ms, and confirms in the screenshot that no content is
> still hidden (no element left at opacity 0 or off-screen). A section
> still hidden after the wait is a finding, fed to the fix batch. Under
> `prefers-reduced-motion: reduce` the content is visible at rest, with no
> entrance to fail — reduced-motion renders are exempt from the entrance
> itself but never from visibility.

> **M3 — Hover micro-interactions on every interactive element.** Every
> link, button, linked card, and linked photograph has a visible hover
> state per the hover layer (`references/motion.md`, hover-layer table) and
> make-interfaces-feel-better's Motion section (enter: opacity + small
> translateY; press: scale 0.97; transitions scoped to the changed
> properties, never `transition: all`). The step-6 check shoots a hovered
> card and a hovered photograph at 1440 (the existing Taste rule) and
> records hovered shots per interactive surface; an interactive element
> with no visible hover change is a finding, fed to the fix batch like
> other checks.

> **M4 — Life in existing pieces.** Every authored motion element already
> on the page — hero entrance, dealt hero loop (fix #15 R4), dealt moment,
> count, diagram pulse, effect/scene loop — must actually move in the
> rendered page. The D1 screenshot pass (and browser-qa's visual loop)
> confirms each one moves; a piece that should move and does not is a
> finding. Each is recorded in the Motion list with its trigger (on load /
> on scroll / on hover / timed loop / count).

> **M5 — At least one small interactive bit per page, where the page has
> one.** Each page that carries an interactive surface — a stepper, toggle,
> tab, filter, counter, peek-list, or live total — must have at least one
> working interactive bit recorded in `docs/design-tokens.md` (name,
> surface, what it does, what state it shows). A page with an interactive
> surface and no recorded bit is incomplete — a static check item in step 6,
> never a screen verdict. A page with no interactive surface is exempt, and
> the exemption is recorded ("no interactive surface — none"). The bit is
> small: one control and its feedback, not a feature.

> **M6 — Reduced motion respected in CSS and JS.** Every motion rule in
> this section is gated on `prefers-reduced-motion: reduce`, in both
> layers: CSS via the `@media (prefers-reduced-motion: reduce)` block that
> disables all transforms and limits opacity transitions to ≤ 0.2s
> (motion-foundations), and JS via `useSafeMotion` /
> `motionConfig.shouldAnimate` (motion-foundations) or the Taste motion
> layer's reduced-motion rest. Checkable: the built page contains the
> reduced-motion CSS block and the JS guard, and the step-6 record notes
> the reduced-motion render (or records that it did not run — never claim
> a render pass that did not run). Content under reduced motion is readable
> at rest, without script.

Checkable forms, per sub-item: M1 — Motion-list entries per section
(count ≥ sections, or a recorded reason per missing section). M2 — the
fail-safe mechanism named per entrance (static) + the scroll-wait-1500ms
screenshot confirmation (step-6 check item). M3 — hovered shots recorded
per interactive surface. M4 — one Motion-list row per authored piece with
its trigger, confirmed moving in the D1 pass. M5 — one recorded bit per
interactive page, or a recorded exemption. M6 — reduced-motion CSS block +
JS guard present in the built page, render noted in the step-6 record.

Expected on the Campus Eats re-trace (Option B): **+0 elements** — the
landing page keeps the Taste scroll ban (M1 adds nothing there), the
app-frame has no scroll (M1 adds nothing there either), M3/M4/M6 are
behaviour/verification rules over already-counted elements, and M5's bit is
the budget stepper's live total, already counted as baseline #19 (stepper,
Component) and #20 (running total, Type). The dry-run must confirm the M5
+0 rather than assume it: if it finds a genuinely new Motion element the
count moves by +1 and the band in §C still holds (see the counts table).

### E1 — Creative freedom within reason: the design-lead MAY invent page-specific elements

Builds on the anti-derivative rule (orchestrate :96; standalone :40):

> "No design based on a searched reference (anti-derivative rule). … the
> direction is GENERATED through the package skills: the Hallmark theme
> deal (50-theme catalog) … `ui-ux-pro-max` styles / palettes / font
> pairings / UX guidelines … the `design-taste-frontend` page system …
> `less-flat-ui` treatments, motion skills, and `design-system` tokens as
> applicable."

and on "more, not bolder" (orchestrate :94):

> "Posture — more, not bolder: more design decisions made deliberately
> through the skills, more craft."

The package currently never says the design-lead MAY invent beyond the
dealt catalogue — it only says what the direction must not be based on.
Proposed new rule (place in the orchestrate design-package rule after the
canonical block :92, and in Taste step 4a after the anti-generic
principles; mirror in orch-build-mvp step 4):

> **The design-lead MAY invent page-specific elements, within reason (fix
> #17 E1).** Invention is allowed: the design-lead may invent elements for
> a page beyond the dealt catalogue — the unique elements of U1 are the
> normal case. "Within reason" means ALL of: (1) it serves the section's
> job, named in the Unique-list entry; (2) it fits the theme's material
> world — material, tokens, palette balance, do-nots; (3) it obeys the
> type/space rules — the C3 Type list, the T1 fill rule, measure and
> contrast checks; (4) it is theme-matched (fix #15 rule A); (5) it passes
> the craft floor; (6) it passes the Hallmark floor; (7) no violet; (8)
> anti-derivative — never based on a searched reference, and the entry
> names the theme material it draws on, never a URL; (9) browser-qa's
> verdict on the rendered screen is the final word on whether the invented
> element reads as distinct rather than generic or template. NOT within
> reason: a new theme (re-deal instead, Taste step 4); a new palette (the
> Tokens block is the page's `:root` — re-deal once if it clashes); a
> template pattern (a sections-library recipe reused as-is is a catalogue
> item, not an invention — it fails U1's not-a-catalogue test); breaking a
> floor or a ban (craft-floor bans are absolute; the Hallmark floor binds).
> Each invented element's Unique-list entry carries the nine-point bound
> checklist, one line per bound; a missing or failed bound is a static-check
> finding, and a floor/ban break blocks. Distinctiveness itself is
> browser-qa's verdict alone.

Checkable form: the Unique-list entry's nine bound lines, all present, all
passing (or the bound failure recorded as a finding); a floor/ban break is
a blocking static-check failure. The ninth bound (browser-qa's verdict)
is satisfied by the verdict run itself, not by the entry — the entry
records that the element is submitted to that verdict.

Expected on the Campus Eats re-trace: **+0 elements** (a permission +
bounds, not an element — the elements it permits are counted under U1).

## B. What is deliberately NOT changed

- Fix #15 rules stand as-is: the canonical variety + theme-match block
  (verbatim, all 11 files — do not touch it), R1–R5, C1–C3, D1. This fix
  extends C1–C3 (F1) and the step-6 check (U1, T1, M1–M6); it does not
  reimplement or reword them.
- No new inventory: no new treatments, skills, or themes unless a genuine
  gap is found. (M2's fail-safe is a pattern inside existing motion skills,
  not inventory; U1's invented elements are per-build, not catalogue
  additions — an invented element must NOT be added to any skill's
  catalogue, or it stops being unique.)
- No weakening of standing rules: "more, not bolder"; browser-qa sole
  verdict executor; craft-floor bans; Hallmark floor; no violet;
  anti-derivative; snapshot-before-redesign; 2-round fresh-verdict budget.
- No model pins in this fix (fix #16 owns all pins — do not touch any
  `model:` line, picker note, or tier table while implementing this spec).
- No commit, no git bundle, no GitHub touch, no Campus Eats artifact touch.

## C. Verification artifacts to produce

- `fix17/fix17.py`: the edits (count==1 asserts like fix14's/fix15's), +
  backup `build.sh.before-fix17` if build.sh changes.
- `fix17/verify17.py`: checks against the BUILT tree — U1/T1/F1/M1–M6/E1
  anchors present at the cited (re-verified) lines, framed as static checks
  / candidate evidence / consistency only, never verdicts; canonical block
  still byte-identical in all 11 files; treatments still 23; counts
  unchanged; build.sh diff minimal and documented. All checks must pass.
- Rebuild TWICE with `bash ~/workspace/hackathon-plugin/build.sh`; both
  exit 0 and built-tree manifest diff = 0. Record line count + md5 +
  manifest hash.
- The dry-run (separate worker) re-traces Campus Eats under the new rules
  and counts by kind using fix15/BASELINE.md's counting rule exactly —
  starting from the fix #15 after-state (30), NOT from the v1 baseline
  (25). **The re-trace must produce the FINAL artifact's element inventory
  within ±2 elements, not the v1 baseline of 25.** The final artifact
  (Campus Eats re-rendered through the updated package, Nov 11 ~16:09 CST)
  was counted at **32 elements** (MEMORY.md record of that re-render: 25 →
  32, +28%) — so the target band is **30–34 elements**. The dry-run takes
  the 32 as given: it cannot re-derive it from files (the artifact itself
  is out of scope and must not be touched).

### Expected re-trace counts (Option B for M1)

| Rule | Δ elements | Kind(s) |
|---|---|---|
| Fix #15 after-state (dry-run #25) | 30 | C18, T3, V1, Mtn3, Mom2, Ty2, E0, D1 |
| U1 — three unique elements | +3 | Kinds per the dry-run's inventions (likely Component/Type) |
| T1 — type fills bubble | 0 | Sizing rule, no new element |
| F1 — font decisions cite type system | 0 | Recording rule, no new element |
| M1–M6 — motion density (Option B) | 0 | Behaviour/verification rules; M5's bit is the already-counted budget stepper + live total (dry-run to confirm, not assume; a genuinely new Motion element would be +1 and the band still holds) |
| E1 — creative freedom within reason | 0 | Permission + bounds; elements counted under U1 |
| **Predicted total** | **33** | **Inside the 30–34 band** |

If the re-trace lands outside 30–34, the deficient rule(s) must be
strengthened (or the U1 minimum adjusted) — a rule that does not move the
count where the spec says it should, or a re-trace outside the band, is not
shipped. Do not ship a sub-target or over-band result by redefining the
band. If Option A is chosen for M1 instead, the predicted total rises by
one Motion element per scrolled landing section and the band must be
re-derived before the re-trace is judged — do not judge an Option-A
re-trace against the Option-B band.

## D. What the implementer returns

Conclusion + evidence (≤20 lines in the handoff, full detail in fix17 files):
files changed (file:line for every rule, re-verified after fix #16),
build exit/diff, md5, verify17.py result, manifest hash, the dry-run
re-trace count by kind, and anything you could not place (with the reason).
Quote actual numbers from tool outputs, not from memory.

## E. Open questions for the coordinator + what could not be made fully checkable

1. **M1 scope — Option A vs Option B.** Scroll entrances conflict with
   Taste `references/motion.md`'s standing ban on scroll reveals. This spec
   recommends Option B (scope to motion-*-governed app surfaces, keep the
   Taste ban) and its re-trace prediction assumes B. Choosing A rewrites a
   house rule and changes the count prediction — decide before implementing.
2. **T1 thresholds are proposed, not grounded.** The 60% fill ratio and the
   25% dead-space band appear in no existing skill text. The dry-run must
   confirm 60% is attainable on the Campus Eats re-trace without breaking
   the theme; if not, lower the threshold, do not bend the theme.
3. **"v4-level motion set" has no file anchor.** No file defines a "v4
   motion set" and no file contains a 1500ms fail-safe. M1–M6 as written
   ARE the definition; the implementer must not invent a v4 source.
4. **Could not be made fully checkable — T1 dead-space band.** The fill
   ratio (60%) is a computed, enforceable number. The 25% largest-empty-band
   test is a screenshot judgment (a human/browser-qa read of the shot), not
   a computed number: the check is the recorded ratio plus the screenshot
   finding, and the ratio is the enforceable part.
5. **Could not be made fully checkable — M2 visibility outcome.** The
   fail-safe mechanism's presence in the built page is statically checkable;
   the outcome ("no content still hidden after scrolling + 1500ms wait")
   needs a scroll-and-wait probe that no current step-6 tooling performs —
   it is a step-6 screenshot-check item, not an automated assertion, until
   such a probe exists. No new tooling is invented by this fix.
6. **Could not be made fully checkable by script — U1 "not in any skill's
   catalogue".** That limb is verified by the reviewer grepping the skills
   and recording the result in the entry's "why not a catalogue item" field,
   not by an automated check. The count (≥3 complete entries) IS script-checkable.
7. **Final-artifact 32 is taken as given.** The 32 comes from the MEMORY.md
   record of the Nov 11 re-render, not from a file the dry-run can recount
   (the artifact is out of scope). If that record is wrong, the band is
   wrong — flag it rather than re-counting the artifact.
