# Slop checklist — SLOP_F22

**Anchor: `SLOP_F22`.** Fix #22, Group C: 20 AI-design slop indicators, woven from the
@charles.unemployed reels. This checklist is a STATIC check run by `polish-pass`
on source and Capture, in the same standing as the sloplint gates and the
craft-floor bans: every finding is **CANDIDATE EVIDENCE for `browser-qa`, NEVER a
pass/fail verdict on a rendered screen** (fix #13e screen-verdicts rule —
`browser-qa` alone issues verdicts on rendered screens). A finding is appended
to `.hallmark/candidate-evidence.md` (screen + indicator + what was seen) and
fixed with the matching fix in [unslop-fixes.md](unslop-fixes.md) (`UNSLOP_F22`).

## Standing: flags, not bans

A slop indicator is a **FLAG, not a ban** (SPEC §4a). Several indicators below
are legitimate techniques the plugin already uses deliberately (dithering,
ASCII, gradient backgrounds, Instrument Serif, eyebrows, squircles). The check
flags **unconsidered default usage**, never deliberate use. A flagged instance is
**cleared by a recorded D19 reason + theme-fit in the decision record**
(`docs/design-tokens.md`, or `design-system/<project-slug>/MASTER.md` on app
surfaces) — the same mechanism as the fix #17 theme-clash exceptions. If the
check were a ban it would prohibit the plugin's own texture vocabulary — that
outcome is forbidden.

**Theme-match precondition:** every clearance requires the instance to match the
dealt theme (its material, tokens, palette balance, and do-nots). An element
that clashes with the theme is not applied, and the reason is recorded with the
element. A flag with no D19 reason and no theme-fit stays a finding.

**Relation to the craft-floor bans:** where a ban in
[craft-floor.md](craft-floor.md) (or the Impeccable craft floor) already covers
an indicator, the ban still governs as a static check — this checklist never
overrides a ban. The checklist adds flag granularity and the justified-use path
for cases the ban does not already decide. Where the two floors disagree, the
stricter rule wins (SKILL.md non-negotiable 4).

## How to run it

1. Read this file before judging or editing on every pass (SKILL.md
   non-negotiable 4), alongside the craft floor.
2. Walk the 20 checks against the target's source and Capture. One line per
   flagged instance in the report: screen, check id, what was seen.
3. Fix flagged instances with the paired fix in
   [unslop-fixes.md](unslop-fixes.md), or clear them with a recorded D19 reason
   + theme-fit. A cleared flag is recorded in the report with its reason cited,
   never silently dropped.
4. Template-pattern instances (a whole screen built from the flagged defaults)
   go to `.hallmark/candidate-evidence.md` for `browser-qa`; they are fixed
   only on `browser-qa`'s verdict or a design-notes exception, never on this
   check alone.

## D19 reason for this checklist (fix #19 D19 — seven dimensions)

- **Motion:** none — these are static checks; no motion is judged here except
  where a check names a treatment, and those treatments are still, not animated.
- **Theme:** theme-fit decides every flag vs justified call; the dealt theme is
  the test, and a clearance without theme-fit is not a clearance.
- **Texture:** the texture treatments (dithering, ASCII, gradients) are judged
  here as identity-vs-accent: a treatment that IS the whole identity is a flag;
  the same treatment as a theme-matched accent is justified.
- **Visuals:** the visual test is whether the screen reads as assembled from
  defaults (pill badges, divider soup, bordered boxes, gradient wash) rather
  than decided; the flag names the default, the fix names the decision.
- **Techniques:** the deliberate path for each flagged technique runs through
  the named skill (`less-flat-ui` treatments, the fix #19 font-choice rule,
  the dealt theme) — never a fresh default invented in this pass.
- **Colors:** color-default flags (shade scales, gradient washes, accent
  sprawl) are judged against the dealt palette and the one-accent rule; no new
  palette is introduced here.
- **Depth:** none — depth is not judged by this checklist; the depth check judges layers and elevation, and a flat surface recorded `flat by choice — <reason>` satisfies the dimension.

## The 20 checks

### C1 — Tags & pills

- **Flag:** pill / badge / tag chips used as decoration or filler — status words
  that restate nearby copy, a row of pills with no job, pills on every card.
- **Justified use:** a pill that carries meaning the copy does not (a live
  status, a count, a filter state), per the dealt theme, with a D19 reason.
  The craft floor already requires pills only for small controls and chips on
  the text baseline — a pill that breaks those is a floor finding, not just a
  flag.
- **Clearance:** recorded D19 reason + theme-fit in `docs/design-tokens.md`.
- **Fix:** D1 Delete filler badges ([unslop-fixes.md](unslop-fixes.md)).
- **D19 —** Motion: none — static check, no motion judged; Theme: theme-fit
  decides whether a pill earns its place; Texture: none — no texture in this
  check; Visuals: a row of jobless pills reads as assembled defaults; Techniques:
  the deliberate path is the dealt theme's chip rules; Colors: none — color is
  judged by the one-accent rule, not here.

### C2 — Excessive italics

- **Flag:** more than one italic accent per screen, or italics on random words,
  whole sentences, or body copy.
- **Justified use:** a single deliberate italic accent (one word or short
  phrase) chosen through the type rules, with a D19 reason. One rule with D3:
  a single deliberate italic accent is fine; random or excessive italics are slop.
- **Clearance:** recorded D19 reason + theme-fit in `docs/design-tokens.md`.
- **Fix:** D3 Unitalicize random words ([unslop-fixes.md](unslop-fixes.md)).
- **D19 —** Motion: none — static check, no motion judged; Theme: the accent
  must fit the theme's type voice; Texture: none — no texture in this check;
  Visuals: random italics scatter the eye instead of pointing it; Techniques:
  the deliberate path is the type scale's italic use, recorded; Colors: none —
  no color rule in this check.

### C3 — Instrument Serif

- **Flag:** Instrument Serif used as a display or body face with no recorded
  choice through the skills — the default. Defaulting to it IS the tell.
- **Justified use:** the face chosen through the skills (fix #19 F3: a unique
  font chosen through the type scale, recorded with its Source cell) with a
  recorded reason. Instrument Serif is not banned; defaulting to it is. Any
  face can be justified that way.
- **Clearance:** recorded D19 reason + theme-fit + Source cell naming the skill
  text the choice comes from.
- **Fix:** none paired in Group D — the fix is the fix #19 F3 font-choice rule
  itself (choose through the skills, record the reason); do not invent a new
  font rule here.
- **D19 —** Motion: none — static check, no motion judged; Theme: the face must
  fit the dealt theme's type voice; Texture: none — no texture in this check;
  Visuals: a default face reads as a template; a chosen face reads as decided;
  Techniques: the deliberate path is the fix #19 F3 choice through the skills;
  Colors: none — no color rule in this check.

### C4 — Negative kerning

- **Flag:** letter-spacing tighter than −0.04em (the craft-floor floor), or any
  negative kerning / tight tracking with no recorded type reason.
- **Justified use:** tighter tracking with a recorded type reason (display text
  ≥70–80px per `reference/lenses/typeset.md`, never below the −0.04em floor).
  Kerning is a Group G glossary term (G1); the glossary defines it, this check
  enforces the flag.
- **Clearance:** recorded D19 reason + theme-fit in `docs/design-tokens.md`.
- **Fix:** none paired in Group D — the fix is the type-scale tracking rule in
  `reference/lenses/typeset.md`; do not invent a new tracking rule here.
- **D19 —** Motion: none — static check, no motion judged; Theme: tracking must
  fit the theme's type voice; Texture: none — no texture in this check; Visuals:
  over-tight tracking collapses letterforms and reads as a default squeeze;
  Techniques: the deliberate path is the type scale's tracking values, recorded;
  Colors: none — no color rule in this check.

### C5 — Over-the-top detailed UI

- **Flag:** dense detail that adds no job — micro-labels, nested chrome, extra
  controls and ornaments on every surface, a screen crowded with detail no
  Persona asked for.
- **Justified use:** detail that serves the surface's job, recorded with a D19
  reason — the detail earns its place by doing work the Persona needs.
- **Clearance:** recorded D19 reason + theme-fit in `docs/design-tokens.md`.
- **Fix:** D13 Remove embellishments; D2 Drop redundant labels
  ([unslop-fixes.md](unslop-fixes.md)).
- **D19 —** Motion: none — static check, no motion judged; Theme: detail must
  fit the theme's material world; Texture: none — no texture in this check;
  Visuals: unearned detail crowds the focal point and reads as generated;
  Techniques: the deliberate path is the dealt moments and the element-variety
  rule (fix #15); Colors: none — no color rule in this check.

### C6 — Overusing dividers

- **Flag:** divider soup — dividers between every item, or dividers as the only
  grouping device on a screen.
- **Justified use:** dividers that mark real group boundaries per the theme,
  with spacing doing the primary grouping (D8). The craft floor already
  requires decorative structure (connector lines, rails, dividers, borders) to
  stay neutral.
- **Clearance:** recorded D19 reason + theme-fit in `docs/design-tokens.md`.
- **Fix:** D8 Group with spacing ([unslop-fixes.md](unslop-fixes.md)).
- **D19 —** Motion: none — static check, no motion judged; Theme: dividers must
  fit the theme's material and token set; Texture: none — no texture in this
  check; Visuals: a divider between every item is chrome, not structure;
  Techniques: the deliberate path is spacing-first grouping (D8); Colors: none
  — dividers stay neutral per the craft floor.

### C7 — Color shades & opacities

- **Flag:** shade-scale / opacity-step chrome applied by default — tints of
  tints, washed overlays, opacity used to fake a palette — with no theme reason.
- **Justified use:** shades and opacities from the dealt theme tokens, with a
  D19 reason — the same elements used deliberately per the dealt theme.
- **Clearance:** recorded D19 reason + theme-fit in `docs/design-tokens.md`.
- **Fix:** D11 Add an accent colour; D15 Improve text contrast
  ([unslop-fixes.md](unslop-fixes.md)).
- **D19 —** Motion: none — static check, no motion judged; Theme: shades must
  come from the dealt theme tokens; Texture: none — no texture in this check;
  Visuals: default shade scales read as an unchosen palette; Techniques: the
  deliberate path is the theme's own color tokens; Colors: the palette is the
  dealt one — no new shades are invented here.

### C8 — Containers with borders

- **Flag:** bordered boxes as the default container — every card and section
  boxed with a border, cards inside cards, borders where spacing or a heading
  would do.
- **Justified use:** a border that marks state or a real boundary per the theme,
  with a D19 reason. The craft floor already requires elevation declared once
  per element (border OR shadow, not both) and cards inside cards grouped with
  spacing, dividers, or headings.
- **Clearance:** recorded D19 reason + theme-fit in `docs/design-tokens.md`.
- **Fix:** D8 Group with spacing ([unslop-fixes.md](unslop-fixes.md)).
- **D19 —** Motion: none — static check, no motion judged; Theme: borders must
  fit the theme's material and token set; Texture: none — no texture in this
  check; Visuals: a border on every box is the default container, not a
  decision; Techniques: the deliberate path is spacing-first grouping (D8);
  Colors: none — borders stay neutral per the craft floor.

### C9 — Overly detailed diagrams

- **Flag:** a diagram or flowchart whose detail adds nothing — a decorative
  flowchart, a diagram that restates the copy — or more than the dealt diagram
  budget (`design-taste-frontend` `references/diagrams.md`: one diagram a
  section, two a page at most).
- **Justified use:** a diagram that earns its detail — it explains something
  the copy cannot — with a D19 reason. A diagram must earn its detail
  (fix #15 R2: one diagram by default on software pages).
- **Clearance:** recorded D19 reason + theme-fit in `docs/design-tokens.md`.
- **Fix:** D6 Show the actual product ([unslop-fixes.md](unslop-fixes.md)).
- **D19 —** Motion: none — static check, no motion judged (a pulsing diagram
  is a motion decision, judged by the motion skills, not here); Theme: the
  diagram must fit the theme's material world; Texture: none — no texture in
  this check; Visuals: an unearned diagram is decoration pretending to be
  explanation; Techniques: the deliberate path is the dealt diagram budget and
  the diagram's job, recorded; Colors: none — no color rule in this check.

### C10 — Verbose, redundant text

- **Flag:** copy that repeats the heading, states the obvious, or runs long
  without adding information.
- **Justified use:** none — verbose redundant text is never justified; the fix
  is to cut it. Point at the existing copy-voice + craft-floor type checks
  (fix #15 C3: Taste `copy-voice.md` rules apply to ALL copy; craft-floor copy
  checks) — do not restate them here.
- **Clearance:** not applicable — fix, do not clear.
- **Fix:** D2 Drop redundant labels; D9 Make headlines specific
  ([unslop-fixes.md](unslop-fixes.md)).
- **D19 —** Motion: none — static check, no motion judged; Theme: copy must
  speak in the theme's voice; Texture: none — no texture in this check; Visuals:
  redundant copy buries the focal point; Techniques: the deliberate path is the
  fix #15 C3 copy-voice rules, pointed at not restated; Colors: none — no color
  rule in this check.

### C11 — Code breadcrumbs

- **Flag:** breadcrumb trails that expose implementation detail instead of user
  orientation — file paths, stack names, route internals, `src/components/...`
  as navigation.
- **Justified use:** breadcrumbs that orient the user (where am I, how do I get
  back) with real section names the Persona recognises.
- **Clearance:** recorded D19 reason + theme-fit in `docs/design-tokens.md`.
- **Fix:** D2 Drop redundant labels ([unslop-fixes.md](unslop-fixes.md)).
- **D19 —** Motion: none — static check, no motion judged; Theme: breadcrumb
  labels must use the product's own language; Texture: none — no texture in
  this check; Visuals: implementation detail in the chrome reads as a shipped
  scaffold; Techniques: the deliberate path is the product's information
  architecture, not the repo layout; Colors: none — no color rule in this check.

### C12 — Section numbering

- **Flag:** decorative numbering (01 / 02 / 03) on sections whose order carries
  no meaning.
- **Justified use:** numbering on real structure — numbered steps, a genuine
  sequence the reader must follow — with a D19 reason. The craft floor already
  bans section numbers when order carries no meaning, and the Impeccable
  detector flags tiny numbered section labels; this check adds the
  flag-vs-justified wording for the same pattern.
- **Clearance:** recorded D19 reason + theme-fit in `docs/design-tokens.md`.
- **Fix:** D2 Drop redundant labels ([unslop-fixes.md](unslop-fixes.md)).
- **D19 —** Motion: none — static check, no motion judged; Theme: numbering
  must fit the theme's type voice; Texture: none — no texture in this check;
  Visuals: decorative numbers are chrome pretending to be structure; Techniques:
  the deliberate path is the real sequence, recorded; Colors: none — no color
  rule in this check.

### C13 — Eyebrows

- **Flag:** an eyebrow / kicker label above a heading, especially repeated above
  every section heading ("FEATURES", "WHY US"). Never a default label style.
- **Justified use:** a single deliberate, theme-matched key label under
  fix #20 F5 (a label meant to stand out — hero key label, featured section
  label, emphasis badge), recorded with a D19 reason. The plugin leans away
  from eyebrows (fixup20b dropped eyebrow/kicker from the F5 examples); a
  repeated eyebrow above every section heading stays a craft-floor ban
  regardless of any reason recorded.
- **Note — stricter rule wins:** `reference/impeccable-craft-floor.md` states
  a kicker/eyebrow above a heading is a ban no brief earns back. This check
  follows SPEC §4a (a single deliberate theme-matched key label with a D19
  reason, per fix #20 F5, is justified). Where the two disagree, the stricter
  rule wins in this skill's standing order — so a C13 clearance must ALSO be
  recorded as a fix #20 F5 key label with its D19 reason and its F6
  justification, and it covers one deliberate key label only, never a repeated
  eyebrow pattern. Flagged for the parent: the SPEC §4a allowance and the
  Impeccable absolute ban point in different directions; this check records
  both and applies the stricter one.
- **Clearance:** recorded D19 reason + theme-fit + fix #20 F5 key-label record
  in `docs/design-tokens.md`.
- **Fix:** D2 Drop redundant labels ([unslop-fixes.md](unslop-fixes.md)).
- **D19 —** Motion: none — static check, no motion judged; Theme: a key label
  must fit the dealt theme; Texture: none — no texture in this check; Visuals:
  a repeated eyebrow is the most recognisable AI-design tell on the page;
  Techniques: the deliberate path is the fix #20 F5 key-label record, not a
  fresh label style; Colors: none — no color rule in this check.

### C14 — Dithering

- **Flag:** dithering IS the whole visual identity, or applied as a default wash
  with no theme reason.
- **Justified use:** a theme-matched `less-flat-ui` treatment #11 (Dithered
  images) with a D19 reason — the normal `less-flat-ui` path. The technique
  exists as a treatment; the slop check is about default usage, not the
  technique.
- **Clearance:** recorded D19 reason + theme-fit in `docs/design-tokens.md`.
- **Fix:** none paired in Group D — the fix is choosing the treatment
  deliberately through `less-flat-ui`, recorded; do not invent a new rule here.
- **D19 —** Motion: none — static check; the treatment is still, not animated;
  Theme: the treatment must match the dealt theme's material; Texture: dithering
  IS a texture — as an accent it adds grain, as the whole identity it is a wash;
  Visuals: a dither wash as the identity reads as a default; Techniques: the
  deliberate path is `less-flat-ui` #11, recorded; Colors: the treatment uses the
  dealt palette, no new colors.

### C15 — ASCII images

- **Flag:** ASCII art / ASCII imagery as the default visual, or applied as a
  wash with no theme reason.
- **Justified use:** a theme-matched `less-flat-ui` treatment #22 (ASCII and
  pixels) with a D19 reason — the normal `less-flat-ui` path.
- **Clearance:** recorded D19 reason + theme-fit in `docs/design-tokens.md`.
- **Fix:** none paired in Group D — the fix is choosing the treatment
  deliberately through `less-flat-ui`, recorded; do not invent a new rule here.
- **D19 —** Motion: none — static check; the treatment is still, not animated;
  Theme: the treatment must match the dealt theme's material; Texture: ASCII is
  a texture — as an accent it adds character, as the whole identity it is a wash;
  Visuals: ASCII as the default visual reads as a costume; Techniques: the
  deliberate path is `less-flat-ui` #22, recorded; Colors: the treatment uses the
  dealt palette, no new colors.

### C16 — Squircles

- **Flag:** the squircle as the default container shape with no reason — every
  container smoothed the same way because that is what the generator does.
- **Justified use:** a theme-matched squircle (corner smoothing) where the
  design system uses it, with a D19 reason.
  `reference/lenses/polish-details.md` already allows optional corner smoothing
  (squircle) "if the Design System uses it" — this check adds the flag for the
  unconsidered-default case.
- **Clearance:** recorded D19 reason + theme-fit in `docs/design-tokens.md`.
- **Fix:** D14 Inner radius = outer – padding ([unslop-fixes.md](unslop-fixes.md))
  for the nesting geometry; the shape choice itself is fixed by recording the
  theme reason or dropping the squircle.
- **D19 —** Motion: none — static check, no motion judged; Theme: the shape must
  fit the dealt theme's material; Texture: none — no texture in this check;
  Visuals: a default squircle on every container is sameness, not a decision;
  Techniques: the deliberate path is the design system's own radius rules;
  Colors: none — no color rule in this check.

### C17 — Excessive mono fonts

- **Flag:** monospace as a default body or display face, or as a "technical"
  costume. The craft floor already bans monospace used as a technical costume
  rather than for code, data, or measurements.
- **Justified use:** mono where the content needs it — code, data, terminals,
  tabular figures — with a D19 reason. One rule with D4: mono where the content
  needs it; mono as a default body/display face is slop.
- **Clearance:** recorded D19 reason + theme-fit in `docs/design-tokens.md`.
- **Fix:** D4 Mono only where needed ([unslop-fixes.md](unslop-fixes.md)).
- **D19 —** Motion: none — static check, no motion judged; Theme: mono use must
  fit the theme's type voice; Texture: none — no texture in this check; Visuals:
  mono everywhere reads as a costume, not a voice; Techniques: the deliberate
  path is the type scale's mono roles, recorded; Colors: none — no color rule
  in this check.

### C18 — ALL CAPS subtitles

- **Flag:** all-caps subtitles or labels as the default label style, or
  all-caps paragraphs. `reference/lenses/typeset.md` already flags all-caps
  paragraphs as unfinished type.
- **Justified use:** short labels in caps with positive tracking (+0.04 to
  +0.1em per `reference/lenses/typeset.md`), theme-matched, with a D19 reason.
  Never a default label style. Eyebrow labels are usually all-caps — see C13.
- **Clearance:** recorded D19 reason + theme-fit in `docs/design-tokens.md`.
- **Fix:** D2 Drop redundant labels ([unslop-fixes.md](unslop-fixes.md)).
- **D19 —** Motion: none — static check, no motion judged; Theme: caps labels
  must fit the theme's type voice; Texture: none — no texture in this check;
  Visuals: all-caps everywhere removes word shape and reads as a default;
  Techniques: the deliberate path is the type scale's caps rules with positive
  tracking, recorded; Colors: none — no color rule in this check.

### C19 — Gradient backgrounds

- **Flag:** a gradient wash as the default background or brand look — especially
  the purple-to-blue / pink-to-orange default — or a gradient that IS the whole
  visual identity, applied with no theme reason. The craft floor already bans
  purple-to-blue (or pink-to-orange) gradients as the default brand look, and
  `scripts/detect.mjs` flags the slop gradient; this check adds the
  flag-vs-justified wording.
- **Justified use:** a theme-matched gradient treatment (`less-flat-ui` #3
  Thermal gradients / #9 Grainy gradients) with a D19 reason. A guarded
  single-hue gradient-text ramp (Hallmark gate 2b: stops within 40°, both stops
  tokens) is permitted, not a flag.
- **Clearance:** recorded D19 reason + theme-fit in `docs/design-tokens.md`.
- **Fix:** D11 Add an accent colour ([unslop-fixes.md](unslop-fixes.md)).
- **D19 —** Motion: none — static check, no motion judged; Theme: the gradient
  must match the dealt theme's material; Texture: a gradient is a surface
  treatment — as an accent it adds depth, as a wash it is the identity; Visuals:
  a default gradient wash is the most recognisable AI-template look; Techniques:
  the deliberate path is `less-flat-ui` #3 / #9, recorded; Colors: the gradient
  uses the dealt palette's own hues, no new colors.

### C20 — Periods in titles

- **Flag:** a period at the end of a title or heading.
- **Justified use:** none — a title never ends with a period. Straight check.
- **Clearance:** not applicable — fix, do not clear.
- **Fix:** D9 Make headlines specific; D16 Wrap headlines properly
  ([unslop-fixes.md](unslop-fixes.md)).
- **D19 —** Motion: none — static check, no motion judged; Theme: titles speak
  in the theme's voice, without sentence punctuation; Texture: none — no texture
  in this check; Visuals: a period turns a title into a sentence fragment;
  Techniques: the deliberate path is the fix #15 C3 copy-voice rules; Colors:
  none — no color rule in this check.

## Accent sprawl — ACCENT_F22 (fix #22 §8, H1 — polish-pass portion)

**Anchor: `ACCENT_F22`.** The H1 color-accents concept (one accent color, used
sparingly and consistently for CTAs, active states, highlights, the single most
important element per screen; part of the brand identity tokens, fix #20 B1)
lives in `ui-ux-pro-max` (another agent's portion). This is the polish-pass
check on it: **accent sprawl is a flag, slop-adjacent.** Same standing as the
checklist above — static check, candidate evidence for `browser-qa`, never a
verdict.

- **Flag:** two or more competing accent hues on one screen; accent used on
  non-action elements (decorative fills, body text, backgrounds, chrome); accent
  sprawl where color stops meaning anything. The craft floor already requires
  one accent in product UI and the distill lens already caps the palette at
  1 accent + neutrals + semantic colors — this check names the sprawl flag for
  the H1 concept.
- **Justified use:** one accent (or a defined accent palette recorded in the
  brand identity tokens, fix #20 B1), used for action/emphasis only — CTA,
  active state, highlight, the single most important element per screen —
  theme-matched, with a D19 reason.
- **Clearance:** recorded D19 reason + theme-fit + the accent recorded in the
  brand identity tokens in `docs/design-tokens.md`.
- **Fix:** D11 Add an accent colour ([unslop-fixes.md](unslop-fixes.md)) — D11 is
  the fix, H1 is the concept; the D11 text points at this check, it does not
  duplicate it.
- **D19 —** Motion: none — static check, no motion judged; Theme: the accent
  must be the dealt theme's accent, recorded in the brand tokens; Texture: none
  — no texture in this check; Visuals: competing accents leave the eye nowhere
  to land; Techniques: the deliberate path is the fix #20 B1 brand tokens;
  Colors: one accent, used for action/emphasis only — accent sprawl is the flag.

## Accent hierarchy — ACCENTUATION_F22 (fix #22 §8, H2 — polish-pass portion)

**Anchor: `ACCENTUATION_F22`.** The H2 accentuation-accents concept (deliberate
accent elements creating hierarchy and focal points; every screen declares its
accent hierarchy in the decision record — first/second/third + means + D19
reasons) lives in the orchestrate design-package step and `ui-ux-pro-max`
(another agent's portion). This is the polish-pass check on it: a **static check
on the recorded hierarchy**, producing candidate evidence for `browser-qa` on
whether the eye lands where the design intends — never a verdict.

- **Flag:** no accent hierarchy declared in the decision record; or everything
  the same weight — nothing draws the eye, no first/second/third. The layout
  lens squint test (`reference/lenses/layout.md`: "What do you see 1st, 2nd,
  3rd?") is the visual half of this check: if the Capture's first-glance order
  does not match the declared hierarchy, that mismatch is candidate evidence
  for `browser-qa`.
- **Justified use:** a declared hierarchy — first, second, third, each with its
  means (size, weight, color via H1, spacing, motion, texture) and a D19 reason
  — recorded in the decision record, and the Capture's first-glance order
  matches it.
- **Clearance:** the hierarchy is recorded with means + D19 reasons, and the
  squint test confirms the eye lands where the design intends. A screen with no
  deliberate accentuation fails this check — there is no clearance for "no
  hierarchy".
- **Cross-references, do not duplicate:** fix #20 F5 (the unique important font
  IS an accentuation means), dealt moments (fix #15 R1/R4/R5 ARE accentuation),
  and H1 (`ACCENT_F22` above) is one means under this umbrella. H2 is the
  umbrella principle; F5, dealt moments, and H1 are specific means under it.
- **D19 —** Motion: motion is one accentuation means — a means recorded as
  motion must name its tokens; Theme: the hierarchy must fit the dealt theme;
  Texture: texture (`less-flat-ui` treatments) is one accentuation means;
  Visuals: the visual test is the squint test — first/second/third must read at
  a glance; Techniques: the deliberate path is the recorded hierarchy in the
  decision record; Colors: color (H1) is one accentuation means, used for
  action/emphasis only.
## One WebGL-heavy effect per surface — WEBGL_ONE_F22 (fix #22 §15)

- **What counts as a flag:** a surface (or page) carrying TWO OR MORE
    WebGL-heavy library effects at once — any two of: an R3F scene
    (R3F_F22), a Vanta scene (VANTA_F22), a ShaderGradient
    (SHADERGRAD_F22), liquid glass (LIQGLASS_F22), liquid metal
    (LIQLOGO_F22), a Casberry particle export. Stacking them is a performance failure and a
  "more, not bolder" failure: a surface stacking two WebGL-heavy effects
  FAILS this check. One effect plus a non-WebGL treatment (a CSS
  gradient, a less-flat-ui texture, a static image) is not stacking.
- **Justified use:** exactly ONE WebGL-heavy effect on the surface,
  theme-matched, with its static fallback and its reduced-motion handling
  recorded — a surface with one theme-matched WebGL effect + static
  fallback PASSES. There is no clearance for two effects on one surface:
  the fix is to remove all but one, never to record a reason for the
  stack.
- **Clearance:** not applicable — fix, do not clear. (A single effect
  needs no clearance under this check; its own theme-fit + fallback are
  checked under its own rule.)
- **Standing:** a static check producing candidate evidence for
  `browser-qa`, never a verdict — same standing as every check in this
  file (fix #13e screen-verdicts rule).
- **Cross-references, do not duplicate:** the per-library rules own their
  own effect (R3F_F22 in `motion-foundations` / `motion-patterns`,
  VANTA_F22 in `design-taste-frontend` step 2, SHADERGRAD_F22 in
  `design-taste-frontend` step 2, LIQGLASS_F22 in `less-flat-ui`, the
  one-effect deal in `design-taste-frontend` step 2). This check only
  counts effects per surface; it never restates any library's install or
  parameters.
- **D19 —** Motion: the count is what keeps the surface's motion budget
  to one WebGL effect; Theme: the one effect must fit the dealt theme;
  Texture: the one effect is the surface's texture/depth layer — a second
  effect adds no theme value; Visuals: one effect reads as a deliberate
  anchor, two read as clutter; Techniques: count the WebGL contexts and
  effects per surface in the static check; Colors: none — the check counts
  effects, it chooses no colours.
## Exported code is reviewed before it enters the build — Casberry (CASBERRY_F22, fix #22 §17)

- **What counts as a flag:** a Casberry particle export (or any
  hosted-tool export) pasted into the build without a line-by-line
  review — the exported snippet is UNTRUSTED code (very low automated
  trust score on the domain, ScamAdviser 1/100; terms unresolved). A
  build pasting exported code blind FAILS the security check.
- **Justified use:** the exported snippet reviewed line by line
  against the theme and D19, with no network / DOM / storage access,
  no obfuscated payloads, and no code outside the particle function —
  then the reviewed snippet enters the build as the surface's one
  WebGL-heavy effect, with its static fallback and reduced-motion
  handling recorded.
- **Clearance:** the review is recorded (what was checked + the
  reviewer's note) in the decision record; an unreviewed export has no
  clearance — fix, do not clear, by reviewing it or removing it.
- **Standing:** a static check producing candidate evidence for
  `browser-qa`, never a verdict — same standing as every check in this
  file (fix #13e screen-verdicts rule).
- **Cross-references, do not duplicate:** the Casberry rule lives in
  `motion-foundations`; the one-WebGL-heavy-effect-per-surface check
  above counts the export as the surface's one effect. This check only
  reviews the exported code; it never restates the tool's install or
  parameters.
- **D19 —** Motion: the review keeps the effect's motion to what the
  directive specified; Theme: the reviewed effect must fit the dealt
  theme; Texture: the particle scene is the surface's texture / depth
  layer; Visuals: the reviewed scene reads as a deliberate anchor;
  Techniques: line-by-line review against the security bar, recorded
  in the decision record; Colors: none — the check reviews code, it
  chooses no colours.
## Thinking Orb check — ORBS_F22 (fix #22 §14, polish-pass portion)

**Anchor: `ORBS_F22`.** The Thinking Orb check (a generic spinner, a
mismatched orb state, or an orb used as decoration is a flag). This is a
STATIC check producing candidate evidence for `browser-qa` — never a
verdict. The pattern lives in `motion-patterns` (ORBS_F22), the tokens in
`motion-foundations` (ORBS_F22), the component rules in `ui-ux-pro-max`
(ORBS_F22); this is the polish-pass check on it. It is the check half of
Group D fix D19 "Add loading states" (unslop-fixes.md): the orb is the
approved implementation of that fix for AI/agent waits.

- **Flag:** (1) a generic spinner shown for an AI/agent wait — a generic
  spinner FAILS; (2) a mismatched orb state — an orb whose state does not
  match the actual agent activity (e.g. a `solving` orb while the app is
  just loading a page, or a `breathing` orb used for reasoning — `breathing`
  is idle/waiting only; there is no `thinking` state) — a mismatched orb
  state FAILS; (3) an orb used as decoration — shown where nothing is
  waiting, or used as a logo, brand mark, or decorative element — an orb
  used as decoration FAILS; (4) an orb used as a general spinner for
  non-AI loading (page loads, uploads, form submits with no agent behind
  them); (5) an orb that does not respect reduced motion — animating under
  `prefers-reduced-motion: reduce` instead of rendering a frozen one-frame
  orb — an orb that does not respect reduced motion FAILS; (6) an orb in a
  rainbow, brand, or accent colour instead of the theme's monochrome ink;
  (7) an orb at a CSS-scaled size other than 64 or 20; (8) an unpinned
  (`"latest"`) `thinking-orbs` version.
- **Justified use:** a state-matched orb PASSES — the orb state matches the
  actual agent activity, only the states the product actually uses are
  shipped, the size is 64 in agent messages or 20 next to status text, the
  ink is the theme's monochrome ink, the orb pauses offscreen/hidden, and
  under reduced motion it renders a frozen one-frame orb.
- **Clearance:** the check passes on the record — the design package names
  the states the product uses and when each appears (orchestrate step 3,
  ORBS_F22), and the built surface shows the matching orb. A flagged
  instance is cleared only by fixing the state, the placement, or the
  colour — there is no D19-reason clearance for a mismatched state or a
  decorative orb: the state either matches the activity or it does not.
- **Cross-references, do not duplicate:** Group D D19 (the fix this check
  enforces — the loading-states rule) and D20 (animate useful feedback —
  the orb IS useful feedback); `motion-patterns` B8 (pulse to confirm
  success — a confirmation pulse is not an orb, and a looping pulse is a
  live indicator, not a confirmation); fix #20 F5 / H2 (accentuation — an
  orb is never an accentuation means).
- **D19 —** Motion: the check is the waiting-state motion check — state,
  pause, and reduced-motion behaviour; Theme: the orb must fit the dealt
  theme (ink, states used); Texture: none — no texture in this check;
  Visuals: the check is whether the wait visibly says what the agent is
  doing; Techniques: the deliberate path is the `thinking-orbs@0.3.2`
  implementation (`ui-ux-pro-max`, ORBS_F22); Colors: strictly monochrome
  theme ink — a coloured orb is the flag.

## Depth check — the z-axis (fix #22 §13, DEPTH_F22)

**Anchor: `DEPTH_F22`.** This section is a STATIC check run by `polish-pass`
on source and Capture, in the same standing as the slop checklist above: every
finding is **CANDIDATE EVIDENCE for `browser-qa`, NEVER a pass/fail verdict
on a rendered screen** (fix #13e screen-verdicts rule — `browser-qa` alone
issues verdicts on rendered screens). A finding is appended to
`.hallmark/candidate-evidence.md` (screen + what was seen). A finding is
cleared only by a recorded D19 reason (seven dimensions, Depth included) +
theme-fit in the decision record (`docs/design-tokens.md`, or
`design-system/<project-slug>/MASTER.md` on app surfaces).

- **D1 — A depth strategy is named for every surface.** The design package
  names one strategy per surface: flat / layered / deep-3D / parallax /
  Vanta scene / 3D-transform hero / camera-through-world (orchestrate step 3,
  DEPTH_F22). **What counts as a flag:** a surface with no strategy named.
  **Justified use:** the strategy `flat by choice — <reason>` — an explicit
  flat call with its reason recorded. A design package with no depth strategy
  named FAILS this check; a package naming `flat by choice — <reason>`
  PASSES it.
- **D2 — Depth is deliberate, not decoration.** **What counts as a flag:** a
  3D effect, parallax layer, or tilt applied with no theme reason and no D19
  reason — depth as decoration. **Justified use:** the depth is theme-matched
  (brutalist hard offset shadows, luxury soft elevation, sticker die-cut
  layers) with a recorded D19 reason. A design with depth applied as
  decoration with no theme reason FAILS this check.
- **D3 — Depth reads on the rendered screen.** **What counts as a flag:** the
  design package names depth, but the Capture shows a flat screen — no layers
  read, no elevation, no parallax, no occlusion (compare against the
  recorded strategy; the closest existing flag is the build.sh line
  "Flat layouts with no layering, depth, or motion" — this check is that
  flag made per-surface and recorded). **Justified use:** the recorded
  strategy is `flat by choice — <reason>` and the screen is deliberately
  flat (dense dashboards, forms, and data tables stay flat per
  hackathon-mode §2).
- **D4 — 3D motion has a reduced-motion fallback.** **What counts as a flag:**
  3D motion (parallax, 3D transforms, camera moves, Vanta scenes) with no
  `prefers-reduced-motion: reduce` handling — no static fallback, no off
  state. **Justified use:** the motion disables under
  `prefers-reduced-motion: reduce` (the finished still shows instead) with a
  mobile/low-power fallback. A design with 3D motion and no reduced-motion
  fallback FAILS this check.
- **D5 — Depth never hurts readability.** **What counts as a flag:** text over
  a 3D/deep background with no scrim and no 4.5:1 contrast check. **Justified
  use:** a scrim is present and contrast is 4.5:1 (same rule as §11 Vanta).
  A design with 3D that hurts text contrast FAILS this check.
- **D6 — The Depth dimension is recorded.** **What counts as a flag:** a
  decision-record entry with six dimension lines and no Depth line.
  **Justified use:** the entry carries all seven dimension lines, Depth
  included (or `flat by choice — <reason>` as its Depth line).
- **Cross-references, do not duplicate:** Group A A11 solid drawing in 3D
  (`motion-foundations` Principles); Group B arcs + parallax-adjacent motion
  values; Bang Motion camera-through-world (§12); Vanta 3D backgrounds (§11,
  VANTA_F22); GSAP 3D transforms (§11); fix #20 F6 (impressive as the bar —
  depth is one way a design earns "impressive"); dealt moments (fix #15
  R1/R4/R5 — a dealt moment can be a depth moment); H2 accentuation (a depth
  moment IS an accentuation means).
- **D19 —** Motion: the check covers parallax, camera moves, and 3D
  transforms — values come from `motion-foundations` depth tokens (DEPTH_F22);
  Theme: every depth finding is judged against the dealt theme; Texture:
  depth and texture are different axes (Soft Shadow #23 is both — see the
  overlap note in `less-flat-ui`, DEPTH_F22); Visuals: the check is read off
  the Capture — does depth read on the rendered screen; Techniques: the check
  routes to the depth rules in `ui-ux-pro-max` (DEPTH_F22); Colors: a depth
  treatment uses the theme's own tokens; Depth: the check IS the depth
  decision — strategy named per surface, or `flat by choice — <reason>`.

## Type audit — the body face must never dominate (fix #23 §3, TYPEAUDIT_F23)

**Anchor: `TYPEAUDIT_F23`.** This section is a STATIC check run by
`polish-pass` on source and Capture, in the same standing as the slop
checklist above: every finding is **CANDIDATE EVIDENCE for `browser-qa`,
NEVER a pass/fail verdict on a rendered screen** (fix #13e screen-verdicts
rule — `browser-qa` alone issues verdicts on rendered screens). A finding
is appended to `.hallmark/candidate-evidence.md` (screen + face shares +
trio comparison + which threshold). The full rule — measurement method,
thresholds, clearance — lives in
[reference/lenses/typeset.md](lenses/typeset.md)
(`TYPEAUDIT_F23`); this section is the checklist half of it: what counts
as a flag, what clears it. The run itself is wired in SKILL.md
non-negotiable 5 (run the type audit on every pass, same standing as the
slop checklist and the depth check).

The failure it catches (Home Run, Nov 12, 2026): all five static faces
loaded and the record chose a real display face, yet Fraunces — the body
face, the Tiempos stand-in under F4 — carried the whole page by volume,
because in an app most visible text IS body text. The audit measures
**visual share** per face — Σ (computed size in px × visible character
count) over that face's elements ÷ Σ over all faces, per primary screen
and as a build roll-up — recorded in `docs/design-tokens.md` as the
Type-audit table (face | roles | visual share % | element count). A "face"
is family + weight. The **trio** is the three families named in the Type
list as display, body, and data/mono; the previous build's trio is the
trio recorded in the same project's decision record from its most recent
prior build (a first build records `previous trio: none (first build)`).

- **T1a — body-face cap, build roll-up. What counts as a flag:** the body
  face carries more than 40% of the build's total visual share. **Justified
  use:** none by default — past 40% the body face IS the visual identity.
  **Clearance:** a scoped exception ONLY — a recorded fix #19 D19 reason +
  theme-fit in the decision record stating why THIS build must be body-led
  (a long-form reader surface is the honest case) — and T1c still binds
  under any exception. A flag with no scoped exception stays a finding.
- **T1b — body-face cap, per screen. What counts as a flag:** the body face
  carries more than 55% on any single primary screen. **Justified use:**
  none by default — one screen may be text-heavy, but past 55% that
  screen's identity is the body face. **Clearance:** the same scoped
  exception as T1a (recorded D19 reason + theme-fit); T1c still binds.
- **T1c — display floor, build roll-up. What counts as a flag:** the
  display/important face(s) combined carry less than 25% of the build's
  total visual share. **Justified use:** none — a display face that carries
  only headings is decoration, not identity. **Clearance:** not applicable
  — fix, do not clear, by re-dealing the trio or re-balancing the shares
  (display type into hero lines, names, prices, key labels).
- **T1d — hero rule. What counts as a flag:** on the hero/home surface,
  the body face's share exceeds the display face's share. **Justified use:**
  none — the hero is the highest-weight surface; if the body face leads
  there, the identity is the body face. **Clearance:** not applicable —
  fix, do not clear.
- **T2 — trio re-deal. What counts as a flag:** this build's trio is
  identical to the previous build's recorded trio. **Justified use:** the
  same trio re-chosen for THIS build, with a recorded reason — why this
  trio is the right choice here, with a fix #19 D19 reason + theme-fit. A
  blanket "same trio as last time" line is not a reason. **Clearance:**
  the recorded reuse reason in the decision record. A flag with no reuse
  reason stays a finding.
- **T3 — variety floor. What counts as a flag:** distinct faces F below
  max(3, ceil(N/20)) for N Type-list text-element rows, or a counted face
  carrying less than 5% of the build's visual share (a face used on one
  tiny label does not count toward variety). **Justified use:** none — the
  floor is the floor. **Clearance:** not applicable — fix, do not clear,
  by re-dealing (an added face from a weight or style within the ≤ 2
  families (+ mono) rule) or consolidating elements.
- **Standing:** a static check producing candidate evidence for
  `browser-qa`, never a verdict — same standing as every check in this
  file (fix #13e screen-verdicts rule). `browser-qa` alone turns a
  type-audit FAIL into a build failure (a distinctiveness finding, minor
  at least), routed back to the design skill for a re-deal.
- **Cross-references, do not duplicate:** the full rule (measurement,
  thresholds, clearance) lives in `reference/lenses/typeset.md`
  (TYPEAUDIT_F23); the run is wired in SKILL.md non-negotiable 5; the
  record checks (Type-audit table + trio line present in the Type list)
  live in `orch-build-mvp` step 6 (TYPEAUDIT_F23); the variety
  requirement on the design side lives in `ui-ux-pro-max` (F7
  strengthened, F7VAR_F23); the verdict lines live in `browser-qa`
  (TYPEAUDIT_F23). This section only flags the hits; it never restates
  the measurement method or the verdict.
- **D19 —** Motion: none — the audit measures type, not motion; Theme:
  every share is judged against the dealt theme's type voice — a face
  that fits the theme still fails the caps if it dominates; Texture: none
  — the audit measures faces, not surface treatment; Visuals: the
  visual-share metric IS the visual test — which face the eye actually
  reads most; Techniques: the audit routes to the Type list and the
  Capture's computed styles, never to a fresh font choice; Colors: none —
  the audit measures faces, not colours; Depth: none — the audit measures
  type, not the z-axis.
