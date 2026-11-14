# Thinking Orbs — patch spec (§14) for fix #22

**Author:** §14 implementation subagent. **Date:** Nov 12, 2026.
**Authority:** `fix22/SPEC.md` §14 + `fix22/PARENT-GUIDANCE.md` + SPEC §§1–7.
**Deliverable type:** PATCH-SPEC ONLY. No plugin file was edited. No `build.sh`
run. No change to `fix22.py` / `verify22.py`. The coordinator applies these
patches (build.sh fix22-block patches for the upstream skills; direct
staged-source edits for orchestrate and polish-pass, per the edit-point table
below).

## 0. How to read this file

Each patch is a 5-tuple `(id, file, anchor, new_text, mode)` in the
`fix22/fix22.py` form: mode `before` inserts the new text before the anchor,
`after` inserts it after the anchor, `replace` replaces the anchor. Every
anchor below was copied verbatim from its target file and verified `count==1`
with grep (see §3 report). Anchor token `ORBS_F22` appears ×1 in the home
file (`motion-patterns`, patch ORB-MP) and is named as a pointer in the other
patches, following the existing `_F22` anchor convention.

**Edit points** (determined by reading `build.sh` + the staged-source layout):

| Patch | Target | Edit point |
|---|---|---|
| ORB-MP | `skills/motion-patterns/SKILL.md` | build.sh fix22 block (upstream skill, no staged source) |
| ORB-MF | `skills/motion-foundations/SKILL.md` | build.sh fix22 block (upstream skill, no staged source) |
| ORB-UIPRO | `skills/ui-ux-pro-max/SKILL.md` | build.sh fix22 block (upstream skill, no staged source) |
| ORB-ORCH | `new-skills/orchestrate/SKILL.md` | direct staged-source edit (orchestrate has a staged source) |
| ORB-PP1 | `round2-skills/polish-pass/reference/slop-checklist.md` | direct staged-source edit (polish-pass has a staged source) |
| ORB-PP2 | `round2-skills/polish-pass/reference/unslop-fixes.md` | direct staged-source edit (polish-pass has a staged source) |

No new skill, command, or trigger key is created. No model pin, font rule,
screen-verdicts rule, marketplace manifest, or Audit #4 backup is touched.

**Banned-term scan (self-check):** the patch texts below contain none of
the seven banned terms on the standing list (case-insensitive). The word "AI" appears (it is not banned) only in
"AI/agent waiting states", matching the library's own description.

---

## 1. Patch tuples

### ORB-MP — the orb as the loading-state pattern (motion-patterns)

- **id:** `ORB-MP`
- **file:** `skills/motion-patterns/SKILL.md`
- **anchor (verbatim, count==1 in the built tree):**
```
### Toast stack
```
- **mode:** `before`
- **new_text:**

```
### Thinking Orb — the loading indicator for AI/agent waiting states (fix #22 §14, ORBS_F22)

The approved loading indicator for AI/agent waiting states is the Thinking
Orb (Jakub Antalik, `thinking-orbs@0.3.2`, MIT — see the pin record in
`ui-ux-pro-max`, ORBS_F22): a dotted orb on a plain 2D canvas, one distinct
hand-tuned animation per agent state — never a generic spinner. This is the
approved IMPLEMENTATION of Group D fix D19 "Add loading states" (polish-pass
unslop-fixes.md): the loading state for an AI/agent wait is an orb, not a
spinner, and the state must match what the agent is actually doing.

**The nine verified states (repo-verified — see the report §2; there is NO
"tenth" state and NO state named "thinking").** Each state is a distinct
animation, not a recolour:

| State | What the agent is doing | The animation does | Use it when |
|---|---|---|---|
| `working` | general activity | particles on tilted orbits | the agent is working and no narrower state fits |
| `searching` | retrieving | a scan meridian sweeps a dotted globe | retrieving / looking something up |
| `solving` | computing | bands scramble, then click back solved | computing / solving a problem |
| `listening` | capturing input | a waveform rolls through the rings | capturing input (voice, audio, live input) |
| `connecting` | establishing | a constellation wires itself | establishing a connection / handshake |
| `weaving` | combining | three strands plait around the sphere | combining / merging sources or results |
| `composing` | generating | an undulating multi-band sash | generating text, code, or media |
| `breathing` | idle / waiting | a ring slowly morphing | waiting with nothing active to report (idle hold) |
| `shaping` | transforming | dotted outline: circle → triangle → square | transforming / reshaping output |

**Correction to the SPEC §14 mapping draft:** the draft mapped "thinking =
reasoning". There is no `thinking` state in the library. Reasoning maps to
`working` (general activity) or `solving` (computing), whichever the moment
actually is. The `breathing` state's on-screen label reads "Thinking…" but
`breathing` is the IDLE/WAITING state — never use it for reasoning. A build
that shows a "thinking" orb while the agent reasons is a mismatched state.

**Sizes — two tuned presets, not a scale factor.** `size={64}` is the
chat-avatar scale (in agent messages, beside the agent's avatar or name);
`size={20}` is the inline-text scale (next to status text, e.g. "Searching…
<orb>"). Each size carries its own dot count, dot size, and speed tuning
(tokens in `motion-foundations`, ORBS_F22). Never scale an orb with CSS to
some other size — pick 64 or 20.

**Usage (React/Next):**

```tsx
import { ThinkingOrb } from 'thinking-orbs';

// Chat-avatar scale, in an agent message while the agent retrieves:
<ThinkingOrb state="searching" size={64} />

// Inline-text scale, next to status text:
<span>Searching… <ThinkingOrb state="searching" size={20} /></span>
```

`speed` is a multiplier on the preset's baked speed (`speed={1.5}` runs 1.5x
the baked speed). `paused` freezes on the current frame. Every orb carries
`role="img"` with a per-state `aria-label` out of the box ("Working…",
"Searching…", … — the `breathing` label reads "Thinking…"); pass an explicit
`aria-label` only to override it with the product's own status wording.

**Rules — state-matched, never decorative.**

- The orb state MUST match the actual agent activity. A `solving` orb while
  the app is just loading a page is a mismatched state. A generic spinner
  anywhere an AI/agent wait is shown is out — the orb replaces it.
- Menu, not defaults: use ONLY the states the product actually uses. A
  product that only ever retrieves and generates uses `searching` and
  `composing` — it does not ship all nine. The design package names the
  states the product uses (orchestrate step 3, ORBS_F22).
- Not decoration, not a brand mark: an orb never appears where nothing is
  waiting, never as a logo, never as a decorative background element.
- Not a general spinner: non-AI loading (page loads, file uploads, form
  submits with no agent behind them) does NOT use an orb — it uses the
  product's ordinary loading treatment. The orb is for AI/agent waits only.
- Monochrome + theme-matched: the orb takes the theme's ink colour (light
  ink on dark substrates, dark ink on light ones — `theme="auto"` detects
  from the host project; pin with `theme="dark"` / `theme="light"` where the
  substrate is fixed). Never a rainbow orb, never a brand-colour orb, never
  the accent colour — the ink is a neutral, never the accent.
- Cursor gravity is an OPTIONAL interactive extra, off by default: the
  `gravity={{ sprite }}` prop bends the pointer toward the orb, and it needs
  a pointer-raster `sprite` the package does NOT ship. It is documented in
  the author's Libraries.dev skill reference, NOT in the standalone repo's
  component at main — a build that wants it verifies the prop exists in the
  installed version first, and records a gap if it does not. Gravity turns
  itself off under reduced motion. Never a default, never required.
- Performance is the point (requirements, not options — tokens in
  `motion-foundations`, ORBS_F22): plain 2D canvas arcs only (no WebGL, no
  SVG filters, no `ctx.filter`); every instance pauses itself when scrolled
  offscreen (`IntersectionObserver`) or when the tab is hidden, then resumes
  in phase, and still paints one frame while paused; device-pixel-ratio
  capped at 2; `prefers-reduced-motion: reduce` renders a frozen one-frame
  orb (no animation) that still follows the live theme.

**Dry-run fixture check phrases (fixtures (a)–(e) judge against these):**
(a) "a generic spinner" FAILS — a build with a generic spinner for an
AI/agent wait FAILS the check. (b) "a state-matched orb" PASSES — a build
whose orb state matches the actual agent activity PASSES. (c) "a mismatched
orb state" FAILS — an orb whose state does not match the actual agent
activity FAILS. (d) "an orb used as decoration" FAILS — an orb shown where
nothing is waiting, or used as a logo or decorative element, FAILS.
(e) "an orb that does not respect reduced motion" FAILS — an orb that
animates under `prefers-reduced-motion: reduce` instead of rendering a
frozen one-frame orb FAILS.

- **D19 (for the orb pattern)** — Motion: the orb IS the waiting-state
motion — its state, size, and speed are the motion decision, and it pauses
offscreen/hidden and freezes under reduced motion; Theme: the orb takes the
theme's ink and is used only for the states the dealt theme's product
actually has, never as decoration; Texture: none — the orb is a canvas
animation, not a surface treatment; Visuals: the state-matched orb tells the
user what the agent is actually doing, where a generic spinner tells them
nothing; Techniques: the single approved implementation is
`thinking-orbs@0.3.2` on React/Next (ORBS_F22 pin in `ui-ux-pro-max`),
non-React stacks implement the pattern with their own tools; Colors: the
orb is strictly monochrome in the theme's ink — never a rainbow, brand, or
accent colour.

- **Theme-match precondition:** as AB-03 — every orb must still match the
dealt theme (its ink is the theme's ink); an orb in a colour that clashes
with the theme is not applied, and the reason is recorded in
`docs/design-tokens.md`.
```

### ORB-MF — orb tokens (motion-foundations)

- **id:** `ORB-MF`
- **file:** `skills/motion-foundations/SKILL.md`
- **anchor (verbatim, count==1 in the built tree):**
```
### Accessibility
```
- **mode:** `before`
- **new_text:**

```
### Thinking Orb tokens (fix #22 §14, ORBS_F22)

The tokens for the Thinking Orb pattern (`motion-patterns`, ORBS_F22). The
library ships nine states × two sizes as baked tunings (`src/presets.ts` in
the repo): each (state, size) pair resolves to an engine mode plus
speed/count/size multipliers over the mode's base profile, resolved once and
cached. The numbers below ARE the tokens — a build uses the library's baked
tunings, never re-tunes them per component.

**Sizes.** `64` = chat-avatar scale; `20` = inline-text scale. Two tuned
presets, not a scale factor: each size has its own dot count, dot size, and
speed tuning. The engine produces 24–600 dots per frame depending on state
and size. Never scale an orb with CSS to another size — pick 64 or 20.

**Per-state tunings (speed / count / size multipliers over the base profile;
`extra` where the mode carries one).** Verified live from
`src/presets.ts` (repo main, Nov 12, 2026):

| State (engine mode) | size 64 — speed / count / size | size 20 — speed / count / size |
|---|---|---|
| `working` (orbits) | 1.885 / 1 / 1 | 3.9 / 0.238 / 2.4 |
| `searching` (globe) | 2.015 / 0.42 / 1.15, extra scanMul 4.08, dimBase 0.45 | 2.665 / 0.105 / 1.75, extra scanMul 4.335, dimBase 0.45 |
| `solving` (rubik) | 1.82 / 0.35 / 1.05 | 1.95 / 0.088 / 1.9 |
| `listening` (wave) | 4.388 / 0.341 / 1 | 3.998 / 0.105 / 1.6 |
| `connecting` (web) | 3.315 / 1.35 / 0.95 | 6.63 / 0.25 / 1.52 |
| `weaving` (braid) | 1.625 / 0.5 / 1 | 2.75 / 0.1125 / 1.36 |
| `composing` (ribbon) | 2.34 / 0.25 / 0.85, extra spin 0, bandMul 3.9, wobMul 1 | 3.12 / 0.051 / 1.073, extra spin 0, bandMul 4.94, wobMul 1 |
| `breathing` (ring) | 3.24 / 0.25 / 0.956, extra spin 0, bandMul 3.627, wobMul 0.368 | 3.78 / 0.028 / 1.622, extra spin 0, bandMul 3.968, wobMul 0.565 |
| `shaping` (morph) | 2.405 / 0.702 / 0.395, extra spread 1.45 | 2.08 / 0.53 / 1.011, extra spread 1.45 |

**Speed multiplier.** The `speed` prop is a multiplier on the preset's baked
speed (`speed={1.5}` = 1.5x the baked speed). The baked speed is the default;
a build changes it only with a recorded reason (e.g. a deliberately slower
idle orb), never per component by taste.

**Monochrome rule.** Strictly monochrome: light ink on dark substrates, dark
ink on light ones. `theme="auto"` (default) resolves in three layers and
updates live: an ancestor `data-theme="dark|light"` attribute or `dark` /
`light` class (watched via `MutationObserver`); otherwise
`prefers-color-scheme`; SSR-safe (the canvas paints only on the client,
after the theme has resolved). Pin with `theme="dark"` / `theme="light"`
where the substrate is fixed. The ink is the theme's ink — never a rainbow,
brand, or accent colour.

**Reduced-motion behaviour — frozen one-frame orb.** Under
`prefers-reduced-motion: reduce` the orb renders ONE static representative
frame (frame at t=0.6 in the library) and does not animate — and still
follows the live theme. This is a requirement, not an option: an orb that
animates under reduced motion FAILS the check (fixture (e)).

**Offscreen / hidden pause.** Every instance pauses itself when scrolled
offscreen (`IntersectionObserver`) or when the tab is hidden
(`visibilitychange`), then resumes in phase — all instances share one clock.
A paused orb still paints one frame. This is a requirement, not an option.

**Device-pixel-ratio cap.** DPR is capped at 2 (`Math.min(2,
devicePixelRatio)` in the library). This is a requirement, not an option.

**Render budget.** Plain 2D canvas arcs only — no `ctx.filter`, no SVG
filters, no WebGL — the same pixels everywhere, cheap on low-end devices,
60 fps, minimal main-thread use. The heaviest state is under 1% of a 60 fps
frame budget in the library's own measurement; the plugin records the 2D
canvas + pause + DPR-cap requirements and does not re-measure them.

- **D19 (for the orb tokens)** — Motion: the tunings ARE the motion values —
baked per (state, size), speed a multiplier on them, pause offscreen/hidden,
frozen one frame under reduced motion; Theme: the monochrome rule is the
theme's ink, resolved live from the host project; Texture: none — tokens
carry no surface treatment; Visuals: two tuned sizes keep the orb legible at
avatar scale and inline scale, never a CSS-scaled blur; Techniques: the
tunings are the library's baked presets, imported, never re-tuned per
component; Colors: strictly monochrome ink — the tokens choose no colour
beyond the theme's ink.

- **Theme-match precondition:** as AB-03 — tokens are values, not designs;
every orb rendered with them must still match the dealt theme; a clash is
not applied, with the reason recorded in `docs/design-tokens.md`.
```

### ORB-UIPRO — the orb as a component (ui-ux-pro-max)

- **id:** `ORB-UIPRO`
- **file:** `skills/ui-ux-pro-max/SKILL.md`
- **anchor (verbatim, count==1 in the built tree):**
```
One accent, one button pair, one card style: gates.md F4/F15 governs on landing pages, the Impeccable craft floor on app surfaces.
```
- **mode:** `after`
- **new_text:**

```

**Thinking Orb — the loading indicator component for AI/agent waiting states (fix #22 §14, ORBS_F22).** The component rules live here; the pattern lives in `motion-patterns` (ORBS_F22) and the tokens in `motion-foundations` (ORBS_F22). **Where it goes:** size 64 (chat-avatar scale) inside agent messages, beside the agent's avatar or name; size 20 (inline-text scale) next to status text ("Searching… <orb>"). **When to use it:** AI/agent waiting states only — while the agent is working, searching, solving, listening, connecting, weaving, composing, breathing (idle hold), or shaping, with the state matched to the actual activity. **When NOT to use it:** never as a general spinner for non-AI loading (page loads, uploads, form submits with no agent behind them — those use the product's ordinary loading treatment); never as decoration; never as a brand mark or logo. **Menu, not defaults:** only the states the product actually uses are shipped — the design package names them (orchestrate step 3, ORBS_F22). **Supply chain (pinned, verified live Nov 12, 2026):** `thinking-orbs@0.3.2` — exact pin in the project's `package.json` + lockfile; "latest" FAILS the pin check. The repo's `package.json` at main reads 0.3.1; 0.3.2 is the version published on npm (registry `latest`, verified Nov 12, 2026) — pin 0.3.2, the published version, not the repo's 0.3.1. License MIT, verified live (repo LICENSE + `package.json` `"license": "MIT"` + npm registry `"license": "MIT"`); free for commercial use. Peer dependency: React >= 18. **Stack scope:** React/Next via npm `thinking-orbs`. React Native: a package (`thinking-orbs-native`) exists IN the repo under `ports/react-native/`, is NOT published on npm, and has NOT run on a device or simulator yet — install-from-repo only, gated on that verification, never assumed shippable. SwiftUI: PLANNED only (`ports/ios/ThinkingOrbsKit` in the repo's port plan) — no Swift package exists in the repo; do not claim SwiftUI support until it ships. Non-React stacks implement the pattern with their own tools (same routing rule as React Bits, §11): the orb PATTERN (state-matched, monochrome, two sizes, pause + reduced-motion behaviour) is implemented natively, never by forcing the React package outside React. **Monochrome + theme-matched:** the orb takes the theme's ink colour, never a rainbow, brand, or accent colour. Theme-match precondition: an orb is applied only when it matches the dealt theme; a clash is not applied, with the reason recorded in `docs/design-tokens.md`.

(D19 — Motion: the orb is the waiting-state motion, state-matched and pausing offscreen/hidden; Theme: theme-matched ink, used only for the product's real agent states; Texture: none — the orb adds motion, not a surface treatment; Visuals: the orb sits at avatar or inline scale where the wait is, never as a decorative element; Techniques: the pinned npm package on React/Next, install-from-repo-gated on React Native, planned-only on SwiftUI, native re-implementation elsewhere; Colors: strictly monochrome theme ink, never the accent.)
```

### ORB-ORCH — waiting states in the design package (orchestrate, staged source)

- **id:** `ORB-ORCH`
- **file:** `new-skills/orchestrate/SKILL.md` (staged source — direct edit, NOT the build.sh block)
- **anchor (verbatim, count==1 in the staged source):**
```
A screen with no deliberate accentuation (everything the same weight, nothing draws the eye) fails the check.
```
- **mode:** `after`
- **new_text:**

```
 **Waiting states in every UI slice brief (fix #22 §14, ORBS_F22):** the brief also names the slice's waiting states — which Thinking Orb states the product uses and when each appears (the state-matched orb is the approved loading indicator for AI/agent waits; `motion-patterns`, ORBS_F22). Only the states the product actually uses are named (menu, not defaults); a brief that names no waiting states for a slice whose product has agent waits is incomplete, and a brief that lists states the product never shows is inaccurate. The waiting states are part of the design package: they are recorded in `docs/design-tokens.md` alongside the other directives, with the orb size per surface (64 chat-avatar scale in agent messages, 20 inline-text scale next to status text) and the theme ink. Theme-match precondition: the named states and their ink must match the dealt theme; a clash is not applied, with the reason recorded in `docs/design-tokens.md`. (D19 — Motion: the waiting states are the product's agent-wait motion, state-matched; Theme: the states and ink are the dealt theme's; Texture: none — waiting states set no surface treatment; Visuals: the named states tell the user what the agent is doing at each wait; Techniques: the states route to the `thinking-orbs@0.3.2` implementation (`ui-ux-pro-max`, ORBS_F22); Colors: the orb ink is the theme's ink, never the accent.)
```

### ORB-PP1 — the orb check (polish-pass slop checklist, staged source)

- **id:** `ORB-PP1`
- **file:** `round2-skills/polish-pass/reference/slop-checklist.md` (staged source — direct edit, NOT the build.sh block)
- **anchor (verbatim, count==1 in the staged source; the file's last line):**
```
  Colors: color (H1) is one accentuation means, used for
  action/emphasis only.
```
- **mode:** `after`
- **new_text:**

```

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
```

### ORB-PP2 — D19 pointer (polish-pass unslop fixes, staged source)

- **id:** `ORB-PP2`
- **file:** `round2-skills/polish-pass/reference/unslop-fixes.md` (staged source — direct edit, NOT the build.sh block)
- **anchor (verbatim, count==1 in the staged source):**
```
  the loading indicator uses the dealt accent or neutrals only.
```
- **mode:** `after`
- **new_text:**

```
  For AI/agent waiting states the approved implementation of this fix is the
  Thinking Orb (`motion-patterns`, ORBS_F22) — a state-matched orb, not a
  generic spinner. The orb takes the theme's monochrome ink (the "neutrals
  only" branch of this fix's colour rule); the accent branch does NOT apply
  to orbs — an orb in the accent colour is a polish-pass flag (see the
  ORBS_F22 check in the slop checklist), not a justified use.
```

---

## 2. Verification report

### 2.1 Verified state list (from the repo itself — README + source)

**Nine states, verified.** Sources:

- README "States" section (github.com/Jakubantalik/thinking-orbs, read
  Nov 12, 2026): "Nine verbs an agent can be doing, each a distinct
  animation" — `working`, `searching`, `solving`, `listening`, `connecting`,
  `weaving`, `composing`, `breathing`, `shaping`, with the per-state
  animation descriptions quoted in patch ORB-MP.
- `src/presets.ts` `STATE_TO_MODE` (read live): `working: 'orbits'`,
  `searching: 'globe'`, `solving: 'rubik'`, `listening: 'wave'`,
  `connecting: 'web'`, `weaving: 'braid'`, `composing: 'ribbon'`,
  `breathing: 'ring'`, `shaping: 'morph'` — nine keys, no `thinking`.
- `src/ThinkingOrb.tsx` `LABELS` (read live): the same nine keys.
- `PORT_PLAN.md` scope line: "all 9 states (`working`, `searching`,
  `solving`, `listening`, `connecting`, `weaving`, `composing`, `breathing`,
  `shaping`) × 2 sizes (64, 20) × dark/light."

| State | Meaning (repo) | Product moment (SPEC mapping, confirmed) |
|---|---|---|
| `working` | particles on tilted orbits | general activity |
| `searching` | a scan meridian sweeps a dotted globe | retrieving |
| `solving` | bands scramble, then click back solved | computing |
| `listening` | a waveform rolls through the rings | capturing input |
| `connecting` | a constellation wires itself | establishing |
| `weaving` | three strands plait around the sphere | combining |
| `composing` | an undulating multi-band sash | generating |
| `breathing` | a ring slowly morphing | idle / waiting |
| `shaping` | dotted outline: circle → triangle → square | transforming |

**The "thinking" / "working" confusion — resolved from source.** There is
NO state named `thinking`. The phantom tenth state comes from the
`breathing` state's aria-label: `src/ThinkingOrb.tsx` line 26–27 sets
`breathing: 'Thinking…'` — demos and social posts that list "thinking" are
reading that label (or the product family name) as a state. The Levenium
six-verb list (working, searching, solving, listening, composing, shaping)
is a SUBSET of the verified nine — it omits `connecting`, `weaving`, and
`breathing`. The SPEC §14 draft mapping "thinking = reasoning" is therefore
CORRECTED in patch ORB-MP: reasoning maps to `working` or `solving`;
`breathing` is idle/waiting only. **Coordinator/parent adjudication item:**
confirm this correction stands (it contradicts the SPEC's draft mapping,
which the SPEC itself flagged as pending verification).

**The engine `web` mode is NOT a tenth state.** `src/presets.ts`
`ModeKey` includes `'web'`, but it is the engine mode for the `connecting`
state (`connecting: 'web'` — the constellation that wires itself, stroking
proximity edges). Nine public states; nine engine modes; `web` is one of
them, not an extra.

### 2.2 Package support (verified live)

- **npm package:** `thinking-orbs`. **Pin: `thinking-orbs@0.3.2`** (exact).
  npm registry `latest` returns version `0.3.2` (tarball
  `thinking-orbs-0.3.2.tgz`, integrity sha512 recorded in the registry
  response; gitHead `5e7afad5fc8f3661e0bf0b4cd3f87de482ffcf16`). The
  standalone repo's `package.json` at main reads `0.3.1` — pin the
  PUBLISHED version 0.3.2, not the repo's 0.3.1. Note: the registry
  response lists the repository as `git+https://github.com/Jakubantalik/
  Libraries.dev.git`, directory `packages/thinking-orbs` — the package now
  ships from the author's Libraries.dev monorepo; the standalone repo
  (commit `de85557`, 4,014 stars) remains the public home. Peer
  dependency: `react >= 18.0.0`. Zero runtime dependencies.
- **React/Next:** shipped, on npm. `import { ThinkingOrb } from
  'thinking-orbs'`; `<ThinkingOrb state="searching" size={64} />`.
  Also ships a React-free engine subpath `thinking-orbs/engine`.
- **React Native:** EXISTS in-repo, NOT published. `PORT_PLAN.md` Phase 1:
  package `ports/react-native/thinking-orbs-native` exists, typechecks
  against real Skia/RN/Reanimated types, reproduces the golden vectors
  exactly — but "has not run on a device or simulator yet; that is the
  remaining gate before it can ship." Install-from-repo only, gated.
  Peers: `@shopify/react-native-skia >=1.0`,
  `react-native-reanimated >=3`, `react`, `react-native`.
- **SwiftUI:** PLANNED ONLY, does not exist. `PORT_PLAN.md` Phase 2
  (`ports/ios/ThinkingOrbsKit`) is a plan; the repo root listing shows no
  `ports/ios/` directory — only `ports/react-native/`. Do not claim SwiftUI
  support until it ships. (Social posts claiming SwiftUI support are
  describing the plan, not a shipped package.)
- **Cursor gravity:** documented in the author's Libraries.dev skill
  reference (`02-thinking-orbs.md`: `gravity={{ sprite }}`, off by
  default, needs a caller-supplied pointer raster, turns itself off under
  reduced motion / forced colors / coarse or touch pointers / page zoom).
  NOT present in the standalone repo's `src/ThinkingOrb.tsx` at main
  (props are `state, size, theme, speed, paused, style, aria-label` only).
  Recorded in ORB-MP as optional with a verify-first caveat — NOT a
  requirement. **Coordinator note:** if the coordinator wants gravity as a
  hard requirement it must first verify the prop exists in the pinned
  0.3.2 build (the monorepo version may carry it); as written, the patch
  is safe either way.

### 2.3 License verification (live)

- **MIT, verified three ways (Nov 12, 2026):** GitHub repo details list
  "License: MIT License (MIT)"; repo `package.json` `"license": "MIT"`,
  author Jakub Antalik; npm registry `latest` `"license": "MIT"`;
  README "License" section: "MIT © Jakub Antalik". Free for commercial
  use. (No Pro/paid tier gates the npm package itself; the author's
  Libraries Pro Studio/presets are separate paid content and are NOT part
  of this integration — not referenced in any patch.)

### 2.4 The two sizes + tunings, reduced motion, pause (verified from source)

- **Sizes:** README "Sizes": "Two tuned presets — separate designs, not a
  scale factor. `64` for chat-avatar scale, `20` for inline-text scale.
  Each carries its own dot count, dot size and speed tuning."
- **Tunings:** `src/presets.ts` `PRESETS` table reproduced in full in patch
  ORB-MF (speed / count / size multipliers per state × size, plus mode
  extras). Engine produces 24–600 dots per frame (`PORT_PLAN.md`).
- **Speed:** `speed` prop is a multiplier on the preset's baked speed
  (README "Other props": `speed={1.5} // multiplier on the preset's baked
  speed`; `ThinkingOrb.tsx` line 56: `effSpeed = baseSpeed * speed`).
- **Reduced motion:** README: "`prefers-reduced-motion: reduce` renders a
  static representative frame — no animation — and still follows the live
  theme." `ThinkingOrb.tsx` lines 68–76: reduced → `frame(0.6)` once and
  return. The plugin records this as the frozen one-frame orb.
- **Offscreen/hidden pause:** README: "Every instance pauses automatically
  when scrolled offscreen (`IntersectionObserver`) or when the tab is
  hidden, and resumes in phase — all instances share one clock."
  `ThinkingOrb.tsx` lines 108–144: one frame painted even when paused
  (`frame(...)` before the pause wiring), `IntersectionObserver` +
  `visibilitychange` pause/resume.
- **DPR cap 2:** `ThinkingOrb.tsx` line 42: `Math.min(2, devicePixelRatio)`.
  README: "Device-pixel-ratio capped at 2."
- **Rendering:** "Plain 2D canvas arcs only: no `ctx.filter`, no SVG
  filters, no WebGL — the same pixels everywhere, cheap on low-end
  devices." (`ThinkingOrb.tsx` header comment + README.)
- **Theme:** strictly monochrome, `theme="auto"` default, 3-layer resolve
  (`data-theme` attribute / class → `prefers-color-scheme` → SSR-safe
  client-only paint). `role="img"` + per-state `aria-label` out of the box.

### 2.5 RareFormLabs outcome

**rareformlabs connection unresolved — asset verified independently.**

A web search for "RareFormLabs thinking orbs Jakub Antalik" returned no
hit connecting RareFormLabs to the orbs — only unrelated creators' reels
and posts about the library itself. No RareFormLabs link, repo, endorsement,
feature, distribution, or star was found or invented. The asset stands on
its verified identity (Jakub Antalik's `thinking-orbs`, MIT, §2.2–2.4
above), exactly as the SPEC §14 fallback prescribes. No patch text mentions
RareFormLabs. The coordinator records the sentence above verbatim in the
manifest.

### 2.6 Coverage re-verification (word-boundary greps over build.sh)

- `thinking-orb` / `ThinkingOrb` / `thinking orbs`: **0** (confirmed).
- `spinner` (word): **0** (confirmed). Note: `unslop-fixes.md` D19 (staged
  source, not build.sh) mentions "a spinner inside an existing badge or
  button" — that is the generic loading-indicator wording the orb
  supersedes for AI/agent waits; ORB-PP2 patches that section to name the
  orb as the approved implementation.
- `loading indicator`: **0** in build.sh (confirmed).
- `loading state`: **2** in build.sh (confirmed) — line 23366, the
  spec-template slot ("[Where result appears, loading state, streaming vs
  batch, feedback mechanism]"); line 23665, inside the fix22 block itself
  (the AB-02 patch text: "every interaction gets visible feedback inside
  400ms (an optimistic update, a loading state, a press response)").
  The RULE (every async action gets a loading state) lives in staged
  `unslop-fixes.md` D19; the orbs are its approved implementation for
  AI/agent waits — cross-referenced, not duplicated (ORB-PP2).

### 2.7 Edit points with file:line evidence

All anchors verified `count==1` by grep against the CURRENT tree (post
wave-1 fix22 block applied):

| Patch | Anchor evidence |
|---|---|
| ORB-MP | `hackathon-ecc/skills/motion-patterns/SKILL.md:331` — `### Toast stack` (grep `-c '^### Toast stack'` = 1). Also `ORBS_F22` absent (grep = 0). |
| ORB-MF | `hackathon-ecc/skills/motion-foundations/SKILL.md:385` — `### Accessibility` (grep `-c '^### Accessibility'` = 1). |
| ORB-UIPRO | `hackathon-ecc/skills/ui-ux-pro-max/SKILL.md:121` — the "One accent, one button pair, one card style: gates.md F4/F15…" sentence (grep `-c` = 1). Note: this is also AB-13's anchor; AB-13's text lands after it, so ORB-UIPRO's insert lands between the anchor line and AB-13's text — order between the two rules is immaterial. |
| ORB-ORCH | `new-skills/orchestrate/SKILL.md:62` — the H2 accent-hierarchy sentence "A screen with no deliberate accentuation (everything the same weight, nothing draws the eye) fails the check." (grep `-c` = 1). Step 3 is a single long line; the insert lands mid-paragraph after that sentence, matching the existing style of that paragraph. |
| ORB-PP1 | `round2-skills/polish-pass/reference/slop-checklist.md` last line — "Colors: color (H1) is one accentuation means, used for action/emphasis only." (grep `-c` = 1; file ends at the ACCENTUATION_F22 section, line ~458). Appends the orb check as the new final section. |
| ORB-PP2 | `round2-skills/polish-pass/reference/unslop-fixes.md:324` — "the loading indicator uses the dealt accent or neutrals only." (grep `-c` = 1; inside the D19 "Add loading states" section, lines ~309–324). |

### 2.8 Decisions made

1. **Pin `thinking-orbs@0.3.2`** (npm-published `latest`), not the repo
   main's 0.3.1. Recorded in ORB-UIPRO with the reason. If the coordinator
   prefers pinning to the repo state, the parent adjudicates — but the
   published version is the correct pin under the plugin's supply-chain
   policy.
2. **"Thinking" is not a state; `breathing` is idle-only.** Corrected the
   SPEC §14 draft mapping in ORB-MP and flagged it for adjudication (§2.1).
3. **Gravity is optional + verify-first**, not a requirement, because it
   is absent from the standalone repo's component at main (§2.2).
4. **SwiftUI is "planned only"** in the patches — the SPEC's "verify from
   the repo" instruction resolved against claiming it (§2.2).
5. **React Native is "in-repo, not published, not device-verified"** —
   recorded as install-from-repo-gated, never assumed shippable (§2.2).
6. **Orb ink is the theme's neutral ink, never the accent.** This reads
   D19's "accent or neutrals" colour rule as: orbs take the neutrals
   branch; the accent branch does not apply to orbs. ORB-PP2 states this
   explicitly so the D19 text and the orb rule cannot be read as
   conflicting. No existing rule text was changed to achieve this — the
   pointer is additive.
7. **No D19-reason clearance for a mismatched state or decorative orb**
   (ORB-PP1): unlike slop flags (§4a), a wrong orb state is a fact about
   what the agent is doing, not a taste call — it is fixed, not cleared
   by a recorded reason. Flagged for parent confirmation if the parent
   wants the §4a clearance mechanism to apply here instead.
8. **D19 dimension form:** every patch carries a full six-dimension D19
   (Motion / Theme / Texture / Visuals / Techniques / Colors), each a
   reason or explicit `none`. No seventh Depth dimension is asserted here
   (§13 owns that decision; the orb patches do not pre-empt it).
9. **Fixture decidability:** each SPEC §14 fixture (a)–(e) maps to an
   exact check phrase in ORB-MP and ORB-PP1: (a) "a generic spinner"
   FAILS; (b) "a state-matched orb" PASSES; (c) "a mismatched orb state"
   FAILS; (d) "an orb used as decoration" FAILS; (e) "an orb that does not
   respect reduced motion" FAILS. verify22.py should assert those five
   phrases (plus `ORBS_F22`, `thinking-orbs@0.3.2`, and the nine state
   names) in their target files.

### 2.9 Anything needing coordinator / parent adjudication

1. **The "thinking = reasoning" mapping correction** (§2.1, §2.8.2) —
   contradicts the SPEC §14 draft mapping; needs parent confirmation
   (the SPEC itself invited verification).
2. **No D19-reason clearance for mismatched/decorative orbs** (§2.8.7) —
   parent to confirm the stricter stance vs the §4a clearance mechanism.
3. **Pin choice 0.3.2 vs repo 0.3.1** (§2.8.1) — coordinator to confirm
   the published-version pin (recommended) or record otherwise.
4. **Gravity** (§2.2) — if the parent wants it as a requirement, the
   coordinator must first verify the prop in the pinned 0.3.2 build.
5. **Repo migration note:** npm 0.3.2's repository field now points at
   the Libraries.dev monorepo (`packages/thinking-orbs`); the standalone
   repo remains public. If the coordinator re-verifies the source at
   apply time and the monorepo has diverged from the standalone repo,
   the tunings/state list should be re-checked against the monorepo path.
