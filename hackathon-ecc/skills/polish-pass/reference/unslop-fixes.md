# Unslop fixes — UNSLOP_F22

**Anchor: `UNSLOP_F22`.** Fix #22, Group D: 20 ways to unslop AI designs, woven
from the @charles.unemployed reels. Each fix is the repair for its paired slop
indicator in [slop-checklist.md](slop-checklist.md) (`SLOP_F22`), where one
exists; fixes with no paired indicator are listed with the skill that owns the
rule they point at. Fixes are applied by `polish-pass` under the Lenses — they
never restyle or redesign (SKILL.md harmony rule). A fix that would need a new
look, a new palette, or a new direction is a redesign item for the report, not
a fix applied here.

## D19 reason for these fixes (fix #19 D19 — seven dimensions)

- **Motion:** motion is touched only by D20, which points at the motion skills;
  every other fix is a static change and carries `none — static fix, no motion`.
- **Theme:** every fix keeps the dealt theme — nothing here re-picks a palette,
  a face, or a direction; theme-match is a precondition on every fix (a fix
  that clashes with the theme is not applied, and the reason is recorded).
- **Texture:** texture treatments are chosen through `less-flat-ui`, never
  invented here; a fix that removes a texture wash restores the theme's own
  surface.
- **Visuals:** the visual test for every fix is the same — after the fix, the
  screen reads as decided (one focal point, one accent, real product) rather
  than assembled from defaults.
- **Techniques:** each fix names its deliberate path (the owning skill or the
  existing rule it points at) — no fix invents a new technique in this pass.
- **Colors:** no fix introduces a new color; D11 adds the theme's own accent
  where one is missing, and every other fix removes color that carries no
  meaning.
- **Depth:** no fix changes depth; a fix that would need a new depth treatment is a redesign item for the report, not a fix applied here.

## Pairing table (slop indicator → fix)

| Slop | Fix |
|---|---|
| C1 Tags & pills | D1 Delete filler badges |
| C2 Excessive italics | D3 Unitalicize random words (one rule) |
| C5 Over-the-top detailed UI | D13 Remove embellishments; D2 Drop redundant labels |
| C6 Overusing dividers | D8 Group with spacing |
| C7 Color shades & opacities | D11 Add an accent colour; D15 Improve text contrast |
| C8 Containers with borders | D8 Group with spacing |
| C9 Overly detailed diagrams | D6 Show the actual product |
| C10 Verbose, redundant text | D2 Drop redundant labels; D9 Make headlines specific |
| C11 Code breadcrumbs | D2 Drop redundant labels |
| C12 Section numbering | D2 Drop redundant labels |
| C13 Eyebrows | D2 Drop redundant labels |
| C16 Squircles | D14 Inner radius = outer – padding (geometry); record the theme reason or drop the squircle (shape) |
| C17 Excessive mono fonts | D4 Mono only where needed (one rule) |
| C18 ALL CAPS subtitles | D2 Drop redundant labels |
| C19 Gradient backgrounds | D11 Add an accent colour |
| C20 Periods in titles | D9 Make headlines specific; D16 Wrap headlines properly |
| C3 Instrument Serif | no paired D fix — the fix is the fix #19 F3 font-choice rule |
| C4 Negative kerning | no paired D fix — the fix is the type-scale tracking rule (`reference/lenses/typeset.md`) |
| C14 Dithering / C15 ASCII images | no paired D fix — the fix is choosing the treatment deliberately through `less-flat-ui`, recorded |
| (no C item) | D5, D7, D10, D12, D17, D18, D19, D20 — see below |

## The 20 fixes

### D1 — Delete filler badges

Remove badges, pills, and tags that restate nearby copy or carry no meaning
("New", "Beta", "Pro" with nothing behind it). Keep only pills with a job: a
live status, a count, a filter state. Pairs with C1. Lens: distill.
- **D19 —** Motion: none — static fix, no motion; Theme: remaining pills must
  fit the dealt theme; Texture: none — no texture in this fix; Visuals: the
  screen stops shouting in pills; Techniques: the deliberate path is the dealt
  theme's chip rules; Colors: none — no color change in this fix.

### D2 — Drop redundant labels

Remove labels the UI already implies: section labels restating the heading,
duplicate field labels, eyebrow labels above headings (C13), decorative section
numbers (C12), breadcrumb trails that expose implementation detail (C11), copy
that repeats the heading (C10). If the words matter, work them into the heading
or the body — do not keep them as a label. Pairs with C5 / C10 / C11 / C12 /
C13 / C18. Lens: distill / clarify. Points at `reference/lenses/distill.md`
("Remove decorative and redundant elements first").
- **D19 —** Motion: none — static fix, no motion; Theme: remaining labels must
  fit the theme's voice; Texture: none — no texture in this fix; Visuals:
  removing labels lets the heading carry its own weight; Techniques: the
  deliberate path is the distill lens; Colors: none — no color change in this fix.

### D3 — Unitalicize random words

Set every italic back to roman except at most one deliberate italic accent per
screen (one word or short phrase, chosen through the type rules). One rule with
C2: a single deliberate italic accent is fine; random or excessive italics are
slop. Lens: typeset.
- **D19 —** Motion: none — static fix, no motion; Theme: the kept accent must
  fit the theme's type voice; Texture: none — no texture in this fix; Visuals:
  one accent points the eye; many accents scatter it; Techniques: the
  deliberate path is the type scale's italic use, recorded; Colors: none — no
  color change in this fix.

### D4 — Mono only where needed

Monospace for code, data, terminals, and tabular figures only. Body and display
copy return to the dealt faces. One rule with C17: mono where the content needs
it; mono as a default body/display face is slop. Lens: typeset. Points at the
craft-floor ban (monospace as a technical costume) — do not restate it.
- **D19 —** Motion: none — static fix, no motion; Theme: mono roles must fit
  the theme's type voice; Texture: none — no texture in this fix; Visuals: mono
  stops being a costume and goes back to being a tool; Techniques: the
  deliberate path is the type scale's mono roles, recorded; Colors: none — no
  color change in this fix.

### D5 — Use a design system

**Already covered by architecture — no new rule.** The plugin IS a design
system: `ui-ux-pro-max` ("Define the design system before implementing UI")
records the system in `design-system/<project-slug>/MASTER.md` (or
`docs/design-tokens.md`), and `polish-pass` fixes against those tokens. This
fix is one line: use the recorded system — extend its tokens instead of
inventing ad-hoc values (SKILL.md → Design system). If a project has no
recorded tokens, that is a missing-direction finding routed to the design skill,
not a fix invented here.
- **D19 —** Motion: none — architecture, no motion; Theme: the system IS the
  theme's record; Texture: none — no texture in this fix; Visuals: one system
  stops one-off values drifting; Techniques: the deliberate path is the
  recorded token file; Colors: the system's own palette, no new colors.

### D6 — Show the actual product

Replace decorative diagrams, placeholder art, and stock visuals with the real
product artifact: a screenshot of the working product, its real output, a real
number. Pairs with C9 (an overly detailed diagram that adds nothing) and C5.
Lens: distill. Points at the craft-floor Persuade rule (a feature section that
shows no product artifact) — do not restate it. On a landing page the artifact
is the dealt moment's application, recorded in `docs/design-tokens.md`.
- **D19 —** Motion: none — static fix, no motion (a pulsing diagram is a motion
  decision, judged by the motion skills); Theme: the artifact must fit the
  theme's material world; Texture: none — no texture in this fix; Visuals: the
  real product is the proof the diagram was pretending to be; Techniques: the
  deliberate path is the dealt moment's application, recorded; Colors: none —
  no color change in this fix.

### D7 — Enlarge the main feature

Make the primary feature or view dominant — larger, more space, first in the
reading order — and subordinate everything else. Pairs with C5 (detail crowding
out the main feature). Lens: layout. Partially covered: Taste
`references/sections-library.md` ("One main feature large and four small") is
the landing-page form of this fix; this fix is its polish-pass application on
any surface.
- **D19 —** Motion: none — static fix, no motion; Theme: the enlarged feature
  must fit the dealt theme; Texture: none — no texture in this fix; Visuals: one
  dominant feature gives the eye somewhere to land; Techniques: the deliberate
  path is the layout lens and the dealt section shape; Colors: none — no color
  change in this fix.

### D8 — Group with spacing

Group related items tight; separate distinct groups by at least 2 spacing steps
more (craft-floor spacing rules). Spacing — not dividers, not borders — does the
grouping. Pairs with C6 / C8. Lens: layout. Points at `ui-ux-pro-max`
(`references/quick-reference.md`: `spacing-scale`, `whitespace-balance`) and the
craft-floor spacing rules — do not restate them. `ui-ux-pro-max` owns spacing;
this fix applies it.
- **D19 —** Motion: none — static fix, no motion; Theme: spacing comes from the
  theme's own scale; Texture: none — no texture in this fix; Visuals: spacing
  groups are structure without chrome; Techniques: the deliberate path is the
  spacing scale in `ui-ux-pro-max`; Colors: none — no color change in this fix.

### D9 — Make headlines specific

A headline names the specific outcome or value — what it does, for whom, to
what end — not a generic claim ("The future of work", "Supercharge your
workflow"). Pairs with C10 / C20. Lens: clarify. Points at `ui-ux-pro-max`
(`references/quick-reference.md`: `visual-hierarchy` — the pointer spec in
`fix22/cd-pointers.md` adds the headline-specificity pointer there); the
copy-voice rules (fix #15 C3) govern the wording.
- **D19 —** Motion: none — static fix, no motion; Theme: the headline must speak
  in the theme's voice; Texture: none — no texture in this fix; Visuals: a
  specific headline is the focal point; a generic one is filler; Techniques:
  the deliberate path is the fix #15 C3 copy-voice rules; Colors: none — no
  color change in this fix.

### D10 — Emphasize the CTA

One primary CTA per screen, emphasized by size, weight, fill, and the accent —
secondary actions visually subordinate. Pairs with no C item (CTA emphasis has
no slop indicator; it is the repair for a screen where nothing is primary).
Lens: polish-details. Points at `ui-ux-pro-max`
(`references/quick-reference.md`: `primary-action` — the pointer spec in
`fix22/cd-pointers.md` adds the emphasis pointer there) and at H1
(`ACCENT_F22` in [slop-checklist.md](slop-checklist.md)): the accent is the
CTA's emphasis means, used for action/emphasis only.
- **D19 —** Motion: none — static fix, no motion (press feedback is D20's job);
  Theme: the CTA must use the dealt theme's accent and button pair; Texture:
  none — no texture in this fix; Visuals: one emphasized CTA gives the screen
  its next action; Techniques: the deliberate path is the `primary-action` rule
  in `ui-ux-pro-max`; Colors: the dealt accent, used for the CTA only.

### D11 — Add an accent colour

Where a screen has no accent — or its accent is lost in shade scales and
gradient washes — add one accent color, used sparingly for action/emphasis only
(CTA, active state, highlight, the single most important element per screen).
Pairs with C7 / C19. **Points at the H1 concept, does not duplicate it:** the
concept and the sprawl check live at `ACCENT_F22` in
[slop-checklist.md](slop-checklist.md); this fix is the repair step (add the
accent, record it in the brand identity tokens, fix #20 B1). Lens:
polish-details.
- **D19 —** Motion: none — static fix, no motion; Theme: the accent is the dealt
  theme's accent, recorded in the brand tokens; Texture: none — no texture in
  this fix; Visuals: one accent gives the eye somewhere to land; Techniques:
  the deliberate path is the fix #20 B1 brand tokens; Colors: one accent, for
  action/emphasis only — accent sprawl is the `ACCENT_F22` flag.

### D12 — Keep icons consistent

One SVG icon library, one stroke weight, one size grid (16/20/24px) on the
screen. Replace emoji and Unicode glyphs used as icons, and any icon or mark
that does not read as one simple shape at 16px. Pairs with no C item. Lens:
consistency. Points at the craft-floor bans (emoji/Unicode glyphs as the icon
system; mixed icon sets) and `reference/lenses/consistency.md` ("Unify icons")
— do not restate them.
- **D19 —** Motion: none — static fix, no motion; Theme: the icon set must fit
  the dealt theme; Texture: none — no texture in this fix; Visuals: one icon
  language reads as one product; Techniques: the deliberate path is the
  consistency lens; Colors: icons are neutral unless they show status, per the
  craft floor.

### D13 — Remove embellishments

Remove decoration that marks nothing: extra dividers, borders, shadows, badges,
ornaments. Every remaining element marks hierarchy or state — if it does not,
it goes. Pairs with C5 / C6 / C8. Lens: distill. Points at
`reference/lenses/distill.md` ("Remove decorative and redundant elements
first") — do not restate it.
- **D19 —** Motion: none — static fix, no motion; Theme: remaining elements must
  fit the dealt theme; Texture: a removed texture wash restores the theme's own
  surface; Visuals: what remains is all decision, no decoration; Techniques:
  the deliberate path is the distill lens; Colors: removed color carried no
  meaning, so nothing is lost.

### D14 — Inner radius = outer – padding

**Already covered — point, do not restate.** The craft floor (Depth: "Nested
corners: inner radius = outer radius − padding between them (pills exempt)")
already states this rule, and `reference/lenses/polish-details.md` already
applies it ("nested radii follow `inner = outer − padding` (pills exempt)").
This fix applies that rule to nested containers. Pairs with C16 (squircle
nesting geometry).
- **D19 —** Motion: none — static fix, no motion; Theme: radii come from the
  theme's own radius tokens; Texture: none — no texture in this fix; Visuals:
  correct nesting reads as one surface, not stacked boxes; Techniques: the
  deliberate path is the craft-floor Depth rule, pointed at not restated;
  Colors: none — no color change in this fix.

### D15 — Improve text contrast

**Already covered — point, do not restate.** The contrast rule already exists:
craft floor (body/small text ≥4.5:1, large text ≥3:1, in light AND dark, in
every state) and `less-flat-ui`. This fix applies that rule to the flagged text.
Pairs with C7. Lens: typeset / polish-details. Points at `ui-ux-pro-max`
(`references/quick-reference.md`: `color-contrast` — the pointer spec in
`fix22/cd-pointers.md` adds the polish-pass pointer there).
- **D19 —** Motion: none — static fix, no motion; Theme: contrast pairs come
  from the dealt theme's tokens; Texture: none — no texture in this fix; Visuals:
  readable text is the floor, not a feature; Techniques: the deliberate path is
  the craft-floor Contrast rule, pointed at not restated; Colors: the fix
  darkens or swaps the failing color within the dealt palette.

### D16 — Wrap headlines properly

Balanced wrapping (`text-wrap: balance` on headings), no orphans, no mid-phrase
breaks, measure respected. Pairs with C20. Lens: typeset. Points at the craft
floor ("Headings use `text-wrap: balance`; body uses `text-wrap: pretty`") and
`ui-ux-pro-max` (`references/quick-reference.md`: `heading-line-balance` — the
pointer spec in `fix22/cd-pointers.md` adds the polish-pass pointer there).
- **D19 —** Motion: none — static fix, no motion; Theme: wrapping must fit the
  theme's type voice; Texture: none — no texture in this fix; Visuals: a
  balanced headline reads as one thought; Techniques: the deliberate path is the
  craft-floor type rule and `heading-line-balance`; Colors: none — no color
  change in this fix.

### D17 — Align by eye, not pixels

After rendering, fix optical alignment: icons beside text, play triangles in
circles, quotes and bullets hanging, hanging punctuation. Mathematically
centered often looks off — trust the Capture, not the pixel values. Pairs with
no C item. Lens: layout / polish-details. Points at
`reference/lenses/layout.md` ("Check optical alignment … Mathematically
centered often *looks* off") and the make-interfaces-feel-better Optical
Alignment rule — do not restate them.
- **D19 —** Motion: none — static fix, no motion; Theme: alignment must serve
  the theme's layout; Texture: none — no texture in this fix; Visuals: optical
  alignment is judged in the Capture, never from values alone; Techniques: the
  deliberate path is the layout lens squint test; Colors: none — no color change
  in this fix.

### D18 — Use tabular nums

Tabular figures (`font-variant-numeric: tabular-nums`) for data columns, prices,
timers, counters, and any changing values, so digits do not shift the layout.
Pairs with no C item. Lens: typeset / polish-details. Primary home per SPEC
§5: `ui-ux-pro-max` type rules (`references/quick-reference.md`:
`number-tabular`) + glossary G3 (another agent's portion); the same value also
lives in make-interfaces-feel-better (tabular-nums rule + table). The pointer
spec in `fix22/cd-pointers.md` adds the polish-pass pointer at `number-tabular`.
Points at the craft floor ("Numbers in tables and changing values use
`font-variant-numeric: tabular-nums`") — do not restate it.
- **D19 —** Motion: none — static fix, no motion; Theme: numerals must fit the
  theme's type voice; Texture: none — no texture in this fix; Visuals: stable
  digits stop layout jitter; Techniques: the deliberate path is the
  `number-tabular` rule in `ui-ux-pro-max`; Colors: none — no color change in
  this fix.

### D19 — Add loading states

**New rule.** Every async action gets a loading state — and every data view
gets loading, empty, error, and success states (craft-floor States). Background
work never moves the page: no "Checking…", "Refreshing…", or "Syncing…" line
above a list — show it in space that is always reserved (a fixed-width status
slot, a spinner inside an existing badge or button, `aria-busy`), or not at all.
Baseline: the rule existed only as a slot in a spec template ("[Where result
appears, loading state, …]"); the RULE (every async action gets a loading
state) is new here. Pairs with no C item. Lens: harden.
- **D19 —** Motion: the loading state IS motion feedback — it must use the
  motion tokens and respect `prefers-reduced-motion`; Theme: the loading state
  must fit the dealt theme; Texture: none — no texture in this fix; Visuals: a
  loading state tells the Persona the action was heard; Techniques: the
  deliberate path is the harden lens and the craft-floor States rule; Colors:
  the loading indicator uses the dealt accent or neutrals only.

For AI/agent waiting states the approved implementation of this fix is the
  Thinking Orb (`motion-patterns`, ORBS_F22) — a state-matched orb, not a
  generic spinner. The orb takes the theme's monochrome ink (the "neutrals
  only" branch of this fix's colour rule); the accent branch does NOT apply
  to orbs — an orb in the accent colour is a polish-pass flag (see the
  ORBS_F22 check in the slop checklist), not a justified use.

### D20 — Animate useful feedback

Animate only feedback that tells the user something: press feedback, a success
pulse, a state change. No decorative motion. Pairs with no C item. Lens:
animate. **Points at the motion family, does not duplicate it:** primary home
is motion-foundations Principles A10 (Exaggerated feedback) + motion-patterns
B8 (Pulse to confirm success) — one family with this fix (SPEC §5). The
pointer spec in `fix22/cd-pointers.md` adds the polish-pass pointer at
motion-patterns "Button feedback" and the motion-foundations duration tokens;
the A10/B8 items themselves belong to the Groups A+B agent.
- **D19 —** Motion: this fix IS motion — feedback animation uses the motion
  tokens (`fast` for button feedback), never decoration; Theme: feedback motion
  must fit the dealt theme; Texture: none — no texture in this fix; Visuals:
  feedback motion confirms the action was heard; Techniques: the deliberate path
  is the motion-foundations / motion-patterns family (A10/B8); Colors: feedback
  uses the dealt accent for success, never a new color.
