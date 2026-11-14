# Fix #22 §13 (3D / depth) — patch spec (DEPTH_F22)

**Status:** PATCH-SPEC ONLY. No plugin file was edited. No `build.sh` run.
No change to `fix22.py` or `verify22.py` — the coordinator applies these patches.
**Authority:** `fix22/SPEC.md` §13 (read in full) + `fix22/PARENT-GUIDANCE.md` +
SPEC §§1–7 for context. **Anchor token (all patches): `DEPTH_F22`** (×1 in the
home file, following the existing `_F22` anchor convention).

**Patch form:** 5-tuples `(id, file, anchor, new_text, mode)` with mode
`before` / `after` / `replace`, exactly like `fix22/fix22.py`'s patch list.
Anchor text is copied VERBATIM from the target file (grep-verified count==1
per file — see §Report). `new_text` is given as raw text to be wrapped in a
triple-quoted constant in `fix22.py`, as the wave-1 spec files did
(`ab-patches.md`, `process-patches.md`, `libraries-patches.md`). For `after`,
the runtime does `old + new`, so each `after` text starts with `\n\n`; for
`before`, the runtime does `new.rstrip("\n") + "\n\n" + old`. Where an anchor
sits mid-paragraph (one giant line), the new text ends with `\n` so the
original continuation starts on a fresh line.

**Two groups:**

- **Group S (DEPTH-01–08): staged-source patches.** The coordinator applies
  these DIRECTLY to the staged source file named in the tuple. `build.sh`
  copies staged sources verbatim into the built tree (`build.sh:217-234`:
  `new-skills/*` and `round2-skills/*` loops), so no `fix22.py` entry is
  needed for them. Anchors were verified count==1 in the STAGED file.
- **Group R (DEPTH-09–13): runtime-block patches.** Append to `fix22.py`
  `PATCHES` (with the `DEPTH_F22` token as the 6th element, per the existing
  list shape). They are applied by the fix22 block in `build.sh` to the BUILT
  tree at build time. Anchors were verified count==1 in the CURRENT built
  tree (post-fix21 + wave-1, which the preflight simulates against).

**D19 form chosen (see Report §2): seventh-dimension EXTENSION LINE.**
The fix #19 `D19_RULE` text is left byte-identical in both canonical homes
(orchestrate, Taste). A separate line is inserted IMMEDIATELY AFTER the
existing `D19_RULE` block in each home (DEPTH-02, DEPTH-03), plus a short
mirror line after the app-surfaces `D19_APP` paragraph in ui-ux-pro-max
(DEPTH-12). `verify19.py` asserts `D19_RULE in taste` and `D19_RULE in orch`
against the built tree (`fix19/verify19.py:135-138`) — a substring assertion,
so an appended line cannot break it.

---

## Group S — staged-source patches

### DEPTH-01 — orchestrate, step 3: depth strategy in every UI slice brief

- **File:** `new-skills/orchestrate/SKILL.md` (staged source; `build.sh:224-227`
  copies it verbatim to `skills/orchestrate/SKILL.md`)
- **Edit point:** staged source, direct edit. Line 62 (the step-3 paragraph,
  one giant line).
- **Anchor (count==1 in staged file):**
```
A UI brief with no named design components, no recorded direction, no named motion principles, and no accent hierarchy is not ready to dispatch.
```
- **Mode:** `after`
- **Token:** `DEPTH_F22`
- **New text:**
```
**Depth strategy in every UI slice brief (fix #22 §13, DEPTH_F22):** the brief also names the depth strategy for every surface — flat / layered / deep-3D / parallax / Vanta scene / 3D-transform hero / camera-through-world (Bang Motion §12) — with exact values per §10 (layer order, elevation levels, parallax distances, perspective values, transform parameters), recorded in `docs/design-tokens.md` alongside the other directives. A surface may be flat only as an explicit "flat by choice — <reason>"; a brief with no depth strategy named for a surface is not ready to dispatch. Depth is directed, not described: the strategy is a directive with exact values, executed verbatim by implementers. Depth is theme-matched (a brutalist theme's depth is hard offset shadows and stacked cards; a luxury theme's is soft elevation and slow parallax; a sticker theme's is die-cut layers) and never hurts readability or performance: text over 3D/deep backgrounds needs a scrim and a 4.5:1 contrast check, 3D motion respects `prefers-reduced-motion: reduce` (static fallback or off) with a mobile/low-power fallback. The depth rules live in `ui-ux-pro-max` (DEPTH_F22), the 3D motion values in `motion-foundations` depth tokens (DEPTH_F22), the 3D patterns in `motion-patterns` (DEPTH_F22), 3D as a dealt moment in `design-taste-frontend` (DEPTH_F22), and the depth check in `polish-pass` (DEPTH_F22).

- **D19 (for the depth strategy)** — Motion: the strategy names how depth moves (parallax, camera moves, 3D transforms) or records `none — <reason>` for a still flat surface; Theme: the strategy is the dealt theme's depth, never a generic 3D effect; Texture: depth and texture are different axes — texture is the `less-flat-ui` layer, depth is the z-axis (Soft Shadow #23 is both — see the overlap note in `less-flat-ui`, DEPTH_F22); Visuals: the strategy states what sits in front, what sits behind, and how far apart the layers read; Techniques: the strategy routes to the depth rules, depth tokens, and Vanta / GSAP 3D / Bang Motion camera implementations, never to ad-hoc values; Colors: the depth treatment uses the theme's own tokens (a Vanta scene's colours are the theme's tokens); Depth: the strategy IS the depth decision — its layer order, elevation levels, and parallax distances are recorded here.

- **Theme-match precondition:** a depth strategy that clashes with the dealt theme is not applied, and the reason is recorded in `docs/design-tokens.md` with the surface.
```

### DEPTH-02 — orchestrate, D19 seventh-dimension extension line

- **File:** `new-skills/orchestrate/SKILL.md` (staged source)
- **Edit point:** staged source, direct edit. Line 110 (the `D19_RULE` block);
  the anchor is the block's final sentence, so the insert lands immediately
  after the block. Next line (111) is blank, then the fix #20 body-only scope
  rule — the insert sits cleanly between them.
- **Anchor (count==1 in staged file):**
```
The check verifies the reasoning is PRESENT and addresses the dimensions — the quality of the reasoning itself is browser-qa's and the reviewer's judgment, not a static check.
```
- **Mode:** `after`
- **Token:** `DEPTH_F22`
- **New text:**
```
**Depth — the seventh dimension (fix #22 §13, DEPTH_F22).** The six dimensions above are unchanged — the fix #19 D19 rule text is verbatim and stays byte-identical (verify19 asserts it as a substring). This line EXTENDS it: every UI decision's recorded reason now addresses SEVEN dimensions, the six above plus **Depth** (the z-axis: layers — foreground / midground / background — elevation, perspective, parallax, occlusion, and depth of field; what sits in front, what sits behind, and how far apart the layers read, or `flat by choice — <reason>` where flat is the deliberate call). A decision-record entry is complete only when it carries all seven dimension lines; a missing Depth line is the same incompleteness as a missing sixth line — a static check item in step 6, never a screen verdict. Depth is a reason, not a mandate for 3D: a flat surface with a recorded `flat by choice — <reason>` satisfies the dimension.
```

### DEPTH-03 — design-taste-frontend, D19 seventh-dimension extension line

- **File:** `new-skills/design-taste-frontend/SKILL.md` (staged source;
  `build.sh:217-219` copies it verbatim to
  `skills/design-taste-frontend/SKILL.md`)
- **Edit point:** staged source, direct edit. Line 408 (the `D19_RULE` block,
  step 4a); same anchor as DEPTH-02, count==1 in this file. Next line (409)
  is blank, then the fix #20 body-only scope rule.
- **Anchor (count==1 in staged file):**
```
The check verifies the reasoning is PRESENT and addresses the dimensions — the quality of the reasoning itself is browser-qa's and the reviewer's judgment, not a static check.
```
- **Mode:** `after`
- **Token:** `DEPTH_F22`
- **New text:** IDENTICAL to DEPTH-02's new text (same extension line in both
  canonical D19 homes).
```
**Depth — the seventh dimension (fix #22 §13, DEPTH_F22).** The six dimensions above are unchanged — the fix #19 D19 rule text is verbatim and stays byte-identical (verify19 asserts it as a substring). This line EXTENDS it: every UI decision's recorded reason now addresses SEVEN dimensions, the six above plus **Depth** (the z-axis: layers — foreground / midground / background — elevation, perspective, parallax, occlusion, and depth of field; what sits in front, what sits behind, and how far apart the layers read, or `flat by choice — <reason>` where flat is the deliberate call). A decision-record entry is complete only when it carries all seven dimension lines; a missing Depth line is the same incompleteness as a missing sixth line — a static check item in step 6, never a screen verdict. Depth is a reason, not a mandate for 3D: a flat surface with a recorded `flat by choice — <reason>` satisfies the dimension.
```

### DEPTH-04 — design-taste-frontend, 3D as a dealt moment / theme element

- **File:** `new-skills/design-taste-frontend/SKILL.md` (staged source)
- **Edit point:** staged source, direct edit. Line 126 (the Vanta bullet in
  step 2); the anchor is the bullet's closing D19 parenthetical, i.e. the
  END of line 126, so the insert lands after the complete bullet. Next line
  (127) is `- **One object never carries the page.**`
- **Anchor (count==1 in staged file):**
```
(D19 — Motion: the scene's motion is the dealt moment's motion; Theme: theme-matched, colours are the theme's own tokens; Texture: the animated ground is the page's texture layer; Visuals: the scene is the hero's visual anchor, never behind unreadable text; Techniques: Vanta + three.js at the pinned pair, destroy on unmount; Colors: effect colours are the theme's own tokens, never invented.)
```
- **Mode:** `after`
- **Token:** `DEPTH_F22`
- **New text:**
```
- **Depth as a dealt moment / theme element (fix #22 §13, DEPTH_F22).** 3D is a dealt moment and a theme element, not a coat of effects: a shader scene, a Vanta background, or a 3D hero element is the page's depth moment where the deal calls for one, and the depth strategy for every surface is named in the design package (orchestrate step 3, DEPTH_F22) — flat / layered / deep-3D / parallax / Vanta scene / 3D-transform hero / camera-through-world. A dealt moment CAN be a depth moment (fix #15 R1/R4/R5): where the deal returns a moment that reads in depth (a hero object that turns, a scene the camera travels through), the moment is recorded with its depth values, not just its look. Cross-references, do not duplicate: Group A A11 solid drawing in 3D (`motion-foundations` Principles, PRINCIPLES_F22) — an object keeps believable volume while it moves; Bang Motion's camera-through-world (§12) — the camera IS depth in motion, and the one-world / moving-camera / persistent-subject architecture is the deep-3D strategy for the video's motion layer; Vanta 3D backgrounds (§11, VANTA_F22 above) — the depth source for hero scenes; GSAP 3D transforms (§11) — the implementation for 3D motion on web builds; fix #20 F6 — depth is one of the ways a design earns "impressive". Depth is directed per §10 (effect name + exact parameters: layer order, elevation levels, parallax distances, perspective values, transform parameters), recorded in `docs/design-tokens.md` with its D19 reason (seven dimensions, Depth included). A 3D hero element with no named depth strategy, no theme reason, no scrim/contrast check (4.5:1), or no reduced-motion fallback is an incomplete build — a static check item in step 6, never a screen verdict.

- **D19 (for the depth-as-dealt-moment rule)** — Motion: the depth moment's motion is the camera move, the parallax, or the 3D transform — named with its values; Theme: the depth moment is the dealt theme's depth (brutalist hard offset shadows, luxury soft elevation, sticker die-cut layers); Texture: the depth moment may carry a `less-flat-ui` treatment, but depth and texture are different axes (Soft Shadow #23 is both); Visuals: the depth moment is the hero's visual anchor and must read at first glance; Techniques: Vanta / GSAP 3D / Bang Motion camera, at their pinned versions, never an unpinned effect; Colors: the scene's colours are the theme's own tokens; Depth: the moment's layer order, elevation, and parallax distances are the depth decision itself.

- **Theme-match precondition:** a depth moment that clashes with the dealt theme is not applied, and the reason is recorded in `docs/design-tokens.md` with the moment.
```

### DEPTH-05 — orchestrate, design-package rule (row 10): depth recorded with the direction

- **File:** `new-skills/orchestrate/SKILL.md` (staged source)
- **Edit point:** staged source, direct edit. Line 98 (the design-package
  rule, one giant paragraph); the anchor is a sentence fragment inside it.
- **Anchor (count==1 in staged file):**
```
The direction is recorded in `docs/design-tokens.md` (landing: dealt Hallmark theme slug + Tokens; app: the `ui-ux-pro-max` direction — theme/axes/mood, named, never "modern clean") before the slice builds UI; a UI brief written before the tokens exist would have to guess them (see step 3 two-pass briefing).
```
- **Mode:** `after`
- **Token:** `DEPTH_F22`
- **New text:**
```
**Depth strategy recorded with the direction (fix #22 §13, DEPTH_F22):** the design package names the depth strategy for every surface — flat / layered / deep-3D / parallax / Vanta scene / 3D-transform hero / camera-through-world — recorded in `docs/design-tokens.md` alongside the direction; a surface with no named strategy is an incomplete build, and a flat surface is recorded as an explicit `flat by choice — <reason>`. Full rule: orchestrate step 3 (DEPTH_F22).
```

### DEPTH-06 — orchestrate, design-system handoff: tokens file contents gain depth

- **File:** `new-skills/orchestrate/SKILL.md` (staged source)
- **Edit point:** staged source, direct edit. Line 185 (design-system handoff);
  `replace` mode on the parenthetical enumeration of the tokens file's lines.
- **Anchor = old text (count==1 in staged file):**
```
(one line each: visual identity, typography + type scale, colour palette + semantic tokens, spacing/layout, component hierarchy, navigation/IA, responsive behaviour, motion, accessibility, loading / empty / success / error states)
```
- **Mode:** `replace`
- **Token:** `DEPTH_F22`
- **New text:**
```
(one line each: visual identity, typography + type scale, colour palette + semantic tokens, spacing/layout, component hierarchy, navigation/IA, responsive behaviour, motion, depth strategy per surface (fix #22 §13, DEPTH_F22), accessibility, loading / empty / success / error states)
```

### DEPTH-07 — polish-pass SKILL.md, step 5: wire the depth check into the pass

- **File:** `round2-skills/polish-pass/SKILL.md` (staged source;
  `build.sh:234-236` copies it verbatim to `skills/polish-pass/SKILL.md`)
- **Edit point:** staged source, direct edit. Line 99 (step 5, the slop-checklist
  sentence). The staged and built copies differ ONLY in build.sh runtime
  patches to the description/frontmatter lines (lines 3, 15, 25, 32) — the
  step-5 anchor is identical in both (count==1 in each).
- **Anchor (count==1 in staged file):**
```
After the detector runs, run the slop checklist ([reference/slop-checklist.md](reference/slop-checklist.md), `SLOP_F22`) on the same target — same standing: candidate evidence for `browser-qa`, never a verdict — and fix flagged instances with [reference/unslop-fixes.md](reference/unslop-fixes.md) (`UNSLOP_F22`).
```
- **Mode:** `after`
- **Token:** `DEPTH_F22`
- **New text:**
```
Then run the depth check ([reference/slop-checklist.md](reference/slop-checklist.md), `DEPTH_F22` — the depth section at the end of the same file) on the same target — same standing: candidate evidence for `browser-qa`, never a verdict — and record depth findings in `.hallmark/candidate-evidence.md` (screen + what was seen) the same way slop findings are recorded.
```

### DEPTH-08 — polish-pass slop-checklist.md: the depth check itself

- **File:** `round2-skills/polish-pass/reference/slop-checklist.md` (staged
  source; staged == built, `diff` empty — no runtime patches touch it)
- **Edit point:** staged source, direct edit. End of file (line 484); the
  anchor is the file's final sentence (the H2 D19 bullet's last line), so the
  new section appends after it.
- **Anchor (count==1 in staged file):**
```
Colors: color (H1) is one accentuation means, used for
  action/emphasis only.
```
- **Mode:** `after`
- **Token:** `DEPTH_F22`
- **New text:**
```
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
```

---

## Group R — runtime-block patches (append to `fix22.py` PATCHES)

File paths below use `fix22.py`'s rel-path convention (relative to the built
tree root `hackathon-ecc/`). Constants `MF`, `MP`, `UIPRO`, `LFUI`:
`MF = "skills/motion-foundations/SKILL.md"`,
`MP = "skills/motion-patterns/SKILL.md"`,
`UIPRO = "skills/ui-ux-pro-max/SKILL.md"`,
`LFUI = "skills/less-flat-ui/SKILL.md"` (new constant — no existing short name;
`fix22.py` never patches less-flat-ui today). These skills have NO staged
source (upstream/ECC clones or the global Cursor skill) — the fix22 runtime
block in `build.sh` is their only edit point, per the block's own header
comment. Anchors verified count==1 against the CURRENT built tree
(post-fix21 + wave-1). Ordering note: DEPTH-09–13 are independent of each
other (distinct anchors, distinct files except DEPTH-11/12 which anchor on
different lines of the same file) and may be appended after `AB-09g` in any
order; DEPTH-11 must come before DEPTH-12 in list order only if the
coordinator prefers the Vanta-adjacent insert to land first — not required,
the anchors do not chain.

### DEPTH-09 — motion-foundations: depth tokens (3D motion values)

- **File:** `skills/motion-foundations/SKILL.md` (`MF`)
- **Edit point:** fix22 runtime block (`fix22.py` PATCHES). No staged source
  exists for motion-foundations (upstream/ECC).
- **Anchor (count==1 in current built tree):**
```
export const springs = {
```
- **Mode:** `before`
- **Token:** `DEPTH_F22`
- **New text:**
```
### Depth tokens — 3D motion values (fix #22 §13, DEPTH_F22)

```ts
// lib/motion-tokens.ts — depth values live beside motionTokens and are imported, never hardcoded (Rule 5).
export const depthTokens = {
  perspective: 1000, // px — the perspective distance for 3D-transform heroes; smaller reads deeper.
  parallax: { near: 0.5, mid: 0.25, far: 0.1 }, // scroll-linked translate multipliers: foreground moves most, background least.
  tilt: { max: 6 }, // degrees — maximum card tilt on pointer move; small, never a spin.
  elevation: { raised: 8, floating: 16, modal: 24 }, // px blur of the shadow that sells the height at each level (see ui-ux-pro-max depth rules, DEPTH_F22).
}
```

**3D motion rules.** Parallax distances, 3D transform values, and camera moves come from `depthTokens` (Rule 5: no inline numbers — depth values are token values too). A parallax layer moves at its `depthTokens.parallax` multiplier (`useScroll` + `useTransform`); a 3D-transform hero sets `perspective: depthTokens.perspective` on its parent and rotates on `rotateX` / `rotateY` within `depthTokens.tilt.max`; a camera move (Bang Motion §12, camera-through-world) travels through the layers at the parallax multipliers, never as a jump cut. Occlusion is real: a foreground layer may cover a background layer, and the covered content must never be the only copy of anything the user needs. Depth of field: background layers may blur while the foreground stays sharp — never the reverse. Under `prefers-reduced-motion: reduce` all depth motion is off — every layer renders at its final state immediately (same rule as Rule 3: all transforms disabled, opacity-only fades at ≤ 0.2s the only permitted fallback). A11 solid drawing in 3D (Principles above) binds here: an object keeps believable volume, weight, and depth while it moves.

- **D19 (for the depth tokens)** — Motion: the tokens are the values every depth move runs on, so parallax, tilt, and camera moves are decided once and reused; Theme: tokens are values, not looks — the theme still decides what the layered element is; Texture: none — depth tokens carry no surface treatment (Soft Shadow #23 is the texture-side depth cue, see `less-flat-ui` DEPTH_F22); Visuals: the multipliers keep near/mid/far layers legible (nothing moves so far it leaves the frame); Techniques: values live in `depthTokens` and are imported, never hardcoded (Rule 5); Colors: none — depth tokens do not choose colours; Depth: the tokens ARE the depth values — perspective, parallax distances, tilt, elevation blur.

- **Theme-match precondition:** tokens are numbers, not designs — every element moved under them must still match the dealt theme; a token applied in a way that clashes with the theme is not applied, and the reason is recorded in `docs/design-tokens.md` with the element.
```

### DEPTH-10 — motion-patterns: parallax layers + 3D-transform hero (+ camera move)

- **File:** `skills/motion-patterns/SKILL.md` (`MP`)
- **Edit point:** fix22 runtime block (`fix22.py` PATCHES). No staged source
  exists for motion-patterns (upstream/ECC).
- **Anchor (count==1 in current built tree):**
```
### Expanding card
```
- **Mode:** `before`
- **Token:** `DEPTH_F22`
- **New text:**
```
### Parallax layers and 3D-transform hero (fix #22 §13, DEPTH_F22)

```tsx
"use client"
import { motion, useScroll, useTransform } from "motion/react"
import { depthTokens } from "@/lib/motion-tokens"

// Parallax: each layer translates at its depthTokens.parallax multiplier —
// foreground (near) moves most, background (far) moves least. The multipliers
// are the depth: 0.5 / 0.25 / 0.1, never per-layer improvisation (Rule 8).
const { scrollYProgress } = useScroll()
const yNear = useTransform(scrollYProgress, [0, 1], [0, -120 * depthTokens.parallax.near])
const yFar = useTransform(scrollYProgress, [0, 1], [0, 60 * depthTokens.parallax.far])
<motion.div style={{ y: yNear }} />  // foreground layer
<motion.div style={{ y: yFar }} />   // background layer
```

**3D-transform hero.** The hero sets `perspective: depthTokens.perspective`
(1000px) on its parent; the hero object rotates within
`depthTokens.tilt.max` (6°) on pointer move (`rotateX` / `rotateY`) and
settles on release. A flip or turn keeps the object's shadow, edge, and
layering consistent through the move (A11 solid drawing in 3D) — it never
flattens into a texture or shears. **Camera move (Bang Motion §12).** A
camera-through-world move travels through the layers at the parallax
multipliers — push-through, glide, settle — with a subject that persists
across the move; the camera is depth in motion, not a slide transition.
**Depth of field.** Background layers may blur while the foreground stays
sharp; never blur the layer the user must read. Under
`prefers-reduced-motion: reduce` none of this runs — every layer renders at
its final state immediately (see `motion-foundations` Rule 3). SCOPE:
motion-governed app surfaces only; Taste landing pages keep their standing
rule (`references/motion.md`: scrolling moves nothing but the dealt moment) —
a Taste depth moment is a dealt moment (DEPTH_F22 in
`design-taste-frontend`), not a scroll parallax.

- **D19 (for the parallax / 3D-hero patterns)** — Motion: the multipliers, the
perspective, and the tilt cap are the moving values; Theme: the layered hero
is the dealt theme's depth, never a stock parallax; Texture: none — the
patterns add no surface treatment; Visuals: near/mid/far layers stay legible
and the foreground never leaves the frame; Techniques: values come from
`depthTokens` (Rule 8), the camera move follows Bang Motion §12;
Colors: none — the patterns do not choose colours; Depth: the layer order,
parallax distances, and perspective value are the depth decision itself.

- **Theme-match precondition:** as AB-03 — every element moved under these
patterns must still match the dealt theme; a clash is not applied, with the
reason recorded in `docs/design-tokens.md`.
```

### DEPTH-11 — ui-ux-pro-max: depth rules (elevation, perspective, parallax, transforms, layering, occlusion, depth of field)

- **File:** `skills/ui-ux-pro-max/SKILL.md` (`UIPRO`)
- **Edit point:** fix22 runtime block (`fix22.py` PATCHES). No staged source
  exists for ui-ux-pro-max (upstream clone, `build.sh:268` pin).
- **Anchor (count==1 in current built tree):** the Vanta D19 parenthetical —
  the END of the Vanta block, so the insert lands after the complete block.
  Next paragraph is the fix #19 F2 app-surfaces rule.
```
(D19 — Motion: the scene's motion is the dealt moment's motion; Theme:
theme-matched, colours are the theme's own tokens; Texture: the animated
ground is the surface's texture layer; Visuals: the scene is the hero anchor,
never behind unreadable text; Techniques: Vanta + three.js at the pinned pair,
destroy on unmount; Colors: effect colours are the theme's own tokens.)
```
- **Mode:** `after`
- **Token:** `DEPTH_F22`
- **New text:**
```
**Depth rules — the z-axis on app surfaces (fix #22 §13, DEPTH_F22).** Every app surface has a named depth strategy (orchestrate step 3, DEPTH_F22): flat / layered / deep-3D / parallax / Vanta scene / 3D-transform hero / camera-through-world — recorded in `docs/design-tokens.md` alongside the other directives, with exact values per §10. The rules:

- **Elevation system.** Shadow levels ARE depth: raised (`depthTokens.elevation.raised`, 8px blur), floating (16px), modal (24px) — a shadow's blur sells the height. One shadow alone reads flat; layered shadows at different blurs read as real height (see Soft Shadow #23 in `less-flat-ui`, DEPTH_F22 — the texture-side depth cue). Elevation is directed: the level per element is named in the design package, never improvised.
- **Perspective.** 3D-transform surfaces set `perspective: depthTokens.perspective` (1000px) on the parent; smaller reads deeper. A surface with no perspective value has no 3D transforms.
- **Parallax.** Layers move at `depthTokens.parallax` multipliers (near 0.5 / mid 0.25 / far 0.1): foreground moves most, background least. Parallax is a depth decision with exact distances, never a decorative drift.
- **3D transforms.** Tilt and rotation stay within `depthTokens.tilt.max` (6°); a flip or turn keeps the object's shadow, edge, and layering consistent (A11 solid drawing in 3D). GSAP 3D transforms (§11) are the implementation on GSAP builds; `react-three-fiber` (§15) is the 3D layer on React builds; Vanta (§11, VANTA_F22 above) is the vanilla-JS 3D path.
- **Layering.** Every surface declares its layer order — foreground / midground / background — in the design package. The order is the depth strategy made explicit.
- **Occlusion.** A foreground layer may cover a background layer; the covered content must never be the only copy of anything the user needs, and an occluded control must never be the only path to an action.
- **Depth of field.** Background layers may blur while the foreground stays sharp; never blur the layer the user must read.
- **Theme-matched depth.** A brutalist theme's depth is hard offset shadows and stacked cards; a luxury theme's is soft elevation and slow parallax; a sticker theme's is die-cut layers and hard offset shadows. Depth treatment must match the theme deal, with a D19 reason.
- **Never hurts readability or performance.** Text over 3D/deep backgrounds needs a scrim and a 4.5:1 contrast check (same rule as §11 Vanta). 3D motion respects `prefers-reduced-motion: reduce` (static fallback or off) with a mobile/low-power fallback. A deep design that is unreadable or that stutters on a phone FAILS the check — the finding is candidate evidence for `browser-qa`, never a verdict of this skill. One WebGL-heavy effect per surface (§15): a surface never stacks two WebGL depth effects.

- **D19 (for the depth rules)** — Motion: the rules name how depth moves (parallax distances, camera moves, 3D transforms) or record `none — <reason>` for a still flat surface; Theme: the rules are applied in the dealt theme's depth (brutalist / luxury / sticker, above), never as a generic 3D effect; Texture: depth and texture are different axes — texture is the `less-flat-ui` layer, depth is the z-axis (Soft Shadow #23 is both); Visuals: layer order, occlusion, and depth of field keep the layered picture legible; Techniques: the rules route to depth tokens, Vanta, GSAP 3D, and the Bang Motion camera, never to ad-hoc values; Colors: depth treatments use the theme's own tokens; Depth: the rules ARE the depth axis — elevation, perspective, parallax, layering, occlusion, depth of field.

- **Theme-match precondition:** a depth treatment that clashes with the dealt theme is not applied, and the reason is recorded in `docs/design-tokens.md` with the surface.
```

### DEPTH-12 — ui-ux-pro-max: D19 seventh-dimension mirror (app surfaces)

- **File:** `skills/ui-ux-pro-max/SKILL.md` (`UIPRO`)
- **Edit point:** fix22 runtime block (`fix22.py` PATCHES).
- **Anchor (count==1 in current built tree):**
```
The full D19 rule lives in `design-taste-frontend` step 4a.
```
- **Mode:** `after`
- **Token:** `DEPTH_F22`
- **New text:**
```
**Depth — the seventh dimension (fix #22 §13, DEPTH_F22).** App surfaces record the same seventh dimension as the full rule in `design-taste-frontend` step 4a (DEPTH_F22 there): every app-surface UI decision's recorded reason in MASTER.md addresses SEVEN dimensions, the six above plus **Depth** (the z-axis: layers, elevation, perspective, parallax, occlusion, depth of field — or `flat by choice — <reason>` where flat is the deliberate call). A MASTER.md entry is complete only when it carries all seven dimension lines. The six-dimension text above is unchanged; this line extends it.
```

### DEPTH-13 — less-flat-ui: texture/depth overlap note (Soft Shadow #23)

- **File:** `skills/less-flat-ui/SKILL.md` (`LFUI`)
- **Edit point:** fix22 runtime block (`fix22.py` PATCHES) on the BUILT copy.
  Do NOT edit `~/workspace/cursor-skills/less-flat-ui/SKILL.md` — it is the
  shared global Cursor skill outside the plugin, and `build.sh:263` copies it
  verbatim into the built tree at STEP 2. A plugin-scoped note belongs in the
  runtime block, following the Batch E precedent (`build.sh:20972-21004`,
  which patches the built `skills/less-flat-ui/SKILL.md` at build time).
- **Anchor (count==1 in current built tree):**
```
Layers with everything: a shadow is a depth cue, not a pattern, so it stacks on top of any other treatment without competing.
```
- **Mode:** `after`
- **Token:** `DEPTH_F22`
- **New text:**
```
**Depth and texture are different axes (fix #22 §13, DEPTH_F22).** This skill owns texture — the 23 treatments. The z-axis is owned by the depth rules (`ui-ux-pro-max` depth rules, DEPTH_F22) and the depth tokens (`motion-foundations` depth tokens, DEPTH_F22): layers, elevation, perspective, parallax, occlusion. Overlap, recorded once here and not duplicated: Soft Shadow #23 is BOTH — a texture treatment in this catalogue AND a depth cue (its three layered shadows sell elevation). A shadow used as a depth cue still needs its depth strategy named in the design package (orchestrate step 3, DEPTH_F22); a treatment with no depth intent is texture only, and its Depth dimension line records `flat by choice — <reason>` or `none — <reason>` for the z-axis. (D19 — Motion: none — a shadow does not move; Theme: the shadow tint follows the dealt theme's surface; Texture: the shadow IS the texture treatment; Visuals: layered blurs read as real height where one shadow reads flat; Techniques: the three-layer `box-shadow` above, never two separate drop shadows; Colors: the shadow tint is the surface's own hue at low opacity; Depth: the shadow is the elevation cue — its blur is the height.)
```

---

## Report

### 1. Edit points (with file:line evidence)

| Patch | Edit point | Evidence |
|---|---|---|
| DEPTH-01 | Staged `new-skills/orchestrate/SKILL.md:62` (step 3) | Step-3 paragraph; anchor sentence count==1 (grep). Staged == built (`diff` silent for orchestrate). |
| DEPTH-02 | Staged `new-skills/orchestrate/SKILL.md:110` (D19 block end) | `D19_RULE` tail sentence count==1 in staged + built; `fix19/verify19.py:135-138` asserts the substring. |
| DEPTH-03 | Staged `new-skills/design-taste-frontend/SKILL.md:408` (D19 block end, step 4a) | Same tail sentence count==1 in staged + built. |
| DEPTH-04 | Staged `new-skills/design-taste-frontend/SKILL.md:126` (Vanta bullet end) | Vanta D19 tail `(… never invented.)` count==1 in staged. |
| DEPTH-05 | Staged `new-skills/orchestrate/SKILL.md:98` (design-package rule) | Anchor fragment count==1 in staged. |
| DEPTH-06 | Staged `new-skills/orchestrate/SKILL.md:185` (design-system handoff) | `loading / empty / success / error states` count==1 in staged. |
| DEPTH-07 | Staged `round2-skills/polish-pass/SKILL.md:99` (step 5) | Slop sentence count==1 in staged AND built (the staged/built diff touches only frontmatter/description lines 3, 15, 25, 32). |
| DEPTH-08 | Staged `round2-skills/polish-pass/reference/slop-checklist.md:484` (end of file) | Staged == built (`diff` empty); tail anchor count==1. |
| DEPTH-09 | Runtime block → built `skills/motion-foundations/SKILL.md`, before `export const springs = {` | No staged source (upstream/ECC); anchor count==1 in current built tree. |
| DEPTH-10 | Runtime block → built `skills/motion-patterns/SKILL.md`, before `### Expanding card` | No staged source; anchor count==1 in current built tree. |
| DEPTH-11 | Runtime block → built `skills/ui-ux-pro-max/SKILL.md`, after Vanta D19 tail | No staged source (upstream clone, `build.sh:268` pin); anchor count==1 in current built tree. |
| DEPTH-12 | Runtime block → built `skills/ui-ux-pro-max/SKILL.md`, after D19 mirror sentence | Anchor `The full D19 rule lives in … step 4a.` count==1 in current built tree. |
| DEPTH-13 | Runtime block → built `skills/less-flat-ui/SKILL.md`, after Soft Shadow "Layers with everything" sentence | `build.sh:263` copies `~/workspace/cursor-skills/less-flat-ui` verbatim; Batch E precedent patches the built copy (`build.sh:20972-21004`). Anchor count==1 in built tree (and in the cursor-skills source, 1 each). |

Staged-copy mechanism: `build.sh:217-234` — `new-skills/` loop (incl.
`design-taste-frontend`, orchestrate via lines 224-227) and `round2-skills/`
loop (incl. `polish-pass`) copy staged sources verbatim into the built tree.
The D19 block does NOT live in `build.sh` itself: `grep "SIX dimensions"
build.sh` returns nothing — it arrives via the staged copies, which is why
the extension lines go into the staged files, not into a build.sh-embedded
string.

### 2. D19 form chosen

**Seventh-dimension EXTENSION LINE, `D19_RULE` untouched.** The exact form,
in DEPTH-02 / DEPTH-03 (identical text) and mirrored in DEPTH-12:

> "**Depth — the seventh dimension (fix #22 §13, DEPTH_F22).** The six
> dimensions above are unchanged — the fix #19 D19 rule text is verbatim and
> stays byte-identical (verify19 asserts it as a substring). This line EXTENDS
> it: every UI decision's recorded reason now addresses SEVEN dimensions, the
> six above plus **Depth** (the z-axis: layers — foreground / midground /
> background — elevation, perspective, parallax, occlusion, and depth of
> field … or `flat by choice — <reason>` …). A decision-record entry is
> complete only when it carries all seven dimension lines …"

Why this form and not a rewrite: `fix19/verify19.py:135-138` asserts
`D19_RULE in taste` and `D19_RULE in orch` (verbatim substring, imported
from `fix19/fix19.py:110`), and `verify19` also checks the six dimension
names are present in Taste. Rewriting the rule text would break verify19/20/21.
The extension line sits IMMEDIATELY AFTER the existing block in both
canonical homes, so a reader sees the six-dimension rule and then the seventh.
Alternative considered and rejected: a "named consideration inside the
design-package step only" (SPEC §13 rule 2's second option) — rejected
because the Depth line must be checkable per decision-record entry the same
way the other six are, and the design-package step alone would not put the
requirement in front of the per-decision D19 check.

### 3. Depth-hits re-verification (coordinator finding confirmed, with corrections)

- **Case-sensitive `Depth` in `build.sh`: 3 lines, all redesign-depth levels,
  NOT a design axis — CONFIRMED.** `build.sh:21965`, `22030`, `22031`:
  `Depths: **full** (system + composition change; default), **restyle** …,
  **polish** …`. (The coordinator's "3 lines" is exact.)
- **Lowercase `depth` in `build.sh`: 24 hits, NONE a design-axis rule.**
  Breakdown: `git --depth` (53, 60); "relative depth" comment (409);
  reasoning depth (4286); "Flat layouts with no layering, depth, or motion"
  (4298-4299, a flat-layout flag + its fix — the closest existing mention,
  cross-referenced by DEPTH-08 D3); "defense in depth" (5138, 5141, 5302,
  5319); "asked for depth" (7164); "scoring and narrative depth" (7178,
  7195); `maxdepth` (13746, 17717-17736); trigger key `"depth and texture"`
  (22132, a `skill:less-flat-ui` trigger phrase, not a rule).
- **Built-tree design-axis mentions — CONFIRMED, all non-rules:**
  `hackathon-ecc/skills/motion-foundations/SKILL.md:87` A11 "Solid drawing
  in 3D" (a principle, not a rule); `make-interfaces-feel-better/SKILL.md:62`
  "Use layered shadows when a card, button, dropdown, or popover needs
  depth" (a shadow note, not a rule); `design-taste-frontend/SKILL.md:425`
  "Depths: **full** …" (the redesign note). Additional lowercase hits in
  Taste asset JS files are shader parameters / WebGL `depth: false` flags —
  implementation details, not design rules.
- **Zero-hit confirmations (new):** `DEPTH_F22` = 0 everywhere (staged,
  built, `fix22/*.md`, `fix22/*.py`); `flat by choice` = 0 in every skill
  file — its only occurrences are `fix22/SPEC.md:413,430` (the SPEC itself);
  `perspective` / `elevation` / `rotateX` / `rotateY` / `translateZ` = 0 in
  all four of motion-foundations / motion-patterns / motion-advanced /
  ui-ux-pro-max SKILL.md; `parallax` = 3 mentions only (MP:468 inside a D19
  line, "never a stock parallax"; UIPRO:276,283 in search-tool descriptions)
  — none of them a rule or a value.
- **Conclusion: NO existing depth-as-design-axis rule exists.** Confirmed.

### 4. Texture / depth overlap note

Recorded in DEPTH-13 (less-flat-ui) and cross-referenced from DEPTH-01,
DEPTH-04, DEPTH-08, DEPTH-09, DEPTH-11: **depth and texture are different
axes.** less-flat-ui owns texture (the 23 treatments); the depth rules own
the z-axis. **Overlap: Soft Shadow #23 is BOTH** — a texture treatment in the
less-flat-ui catalogue AND a depth cue (its three layered shadows sell
elevation: tight contact shadow grounds the element, mid shadow lifts it,
large soft shadow sells the height — `~/workspace/cursor-skills/less-flat-ui/SKILL.md:484-523`).
Rule: a shadow used as a depth cue still needs its depth strategy named in
the design package; a treatment with no depth intent is texture only, and its
Depth dimension line records `flat by choice — <reason>` or
`none — <reason>` for the z-axis. The note lives in less-flat-ui (the
texture home) and is pointed at, not duplicated, everywhere else.

### 5. Decisions made

1. **D19 = extension line** (§2 above). No `D19_RULE` text altered anywhere.
2. **13 patches, 8 staged + 5 runtime.** SPEC §13 names 5 placements
   (orchestrate, ui-ux-pro-max, motion-foundations/patterns, Taste,
   polish-pass); this spec covers all 5, plus the design-package rule
   (DEPTH-05), the tokens-file contents list (DEPTH-06), the UIPRO D19
   mirror (DEPTH-12), and the less-flat-ui overlap note (DEPTH-13).
3. **No motion-advanced patch.** SPEC §13 places 3D motion in
   motion-foundations/patterns; MA's B16/B17/B19 rules (overlap, masks,
   rubber band) already cover advanced choreography, and the camera move is
   placed in MP (DEPTH-10) beside the scroll patterns it travels with.
4. **No make-interfaces-feel-better patch.** Its `:62` shadow line is
   corroboration, not a rule; feel decisions route through motion-*, which
   now carry the depth tokens. A pointer there would duplicate DEPTH-09.
5. **No GAN-agent patch.** GAN agents execute directives; depth reaches them
   via the design package + §10 directives (DEPTH-01/05). No new directive
   form is needed.
6. **No new skill / command / trigger key.** All weaves are into existing
   skills, per SPEC §7 and the §13 placement map.
7. **Depth token values are NEW and flagged for adjudication** (DEPTH-09):
   `perspective: 1000`, `parallax: { near: 0.5, mid: 0.25, far: 0.1 }`,
   `tilt.max: 6`, `elevation: { raised: 8, floating: 16, modal: 24 }`.
   No existing token conflicts with them (zero hits for
   perspective/elevation/parallax values in the motion skills — §3), but the
   numbers themselves are my choice, not a SPEC value. Same pattern as the
   AB-03 conflict flags: applied as specified, parent adjudicates the values.
8. **DEPTH-13 goes in the runtime block, NOT the cursor-skills source.**
   The global `~/workspace/cursor-skills/less-flat-ui/SKILL.md` is shared
   outside the plugin; a plugin-scoped overlap note belongs in the build-time
   patch of the built copy (Batch E precedent).
9. **Screen-verdicts rule untouched.** The depth check (DEPTH-08) is a static
   check producing candidate evidence for `browser-qa`, never a verdict —
   same standing as the slop checklist it appends to.
10. **No font, model-pin, or marketplace changes.** No banned terms in any
    patch text (checked by inspection against the plugin's seven-term banned
    list from PARENT-GUIDANCE — none of the seven appears in the patch texts
    above; the list itself is deliberately not spelled out in this file so a
    tree-wide scan of the fix dir stays clean).

### 6. Dry-run fixture check phrases (SPEC §13 verification — decidable)

verify22.py / the dry-run should judge the §13 fixtures against these EXACT
strings, all of which the patches above insert:

- (a) FAIL — design package with no depth strategy named: check phrase
  **`Depth strategy`** per surface in `docs/design-tokens.md` (DEPTH-01/05);
  absent → FAIL.
- (b) PASS — package naming **`flat by choice — <reason>`** (DEPTH-01/02/03/
  08 D1): the literal string with a reason present → PASS.
- (c) PASS — deliberate depth: **`layered`** + **`parallax`** +
  elevation values + **`theme-matched`** + seven D19 lines including a
  **`Depth:`** line (DEPTH-02/03/09/11) → PASS.
- (d) FAIL — 3D motion with no reduced-motion fallback: check phrases
  **`prefers-reduced-motion: reduce`** + **`static fallback`** (DEPTH-08 D4,
  DEPTH-09, DEPTH-10, DEPTH-11); absent → FAIL.
- (e) FAIL — 3D hurting text contrast: check phrases **`scrim`** + **`4.5:1`**
  (DEPTH-08 D5, DEPTH-11); absent → FAIL.
- (f) FAIL — depth as decoration with no theme reason: check phrases
  **`theme-matched`** + **`D19 reason`** alongside the depth treatment
  (DEPTH-08 D2, DEPTH-11); absent → FAIL.
- Depth-dimension check: a decision-record entry carries a **`Depth:`** line
  (seventh dimension, DEPTH-02/03/12); six lines and no Depth line → FAIL
  (DEPTH-08 D6).

### 7. Needs coordinator / parent adjudication

1. **"Six dimensions" mentions elsewhere go stale.** The extension line makes
   the count seven, but existing texts still say "six": Taste's trend line
   ("with its fix #19 D19 reason (six dimensions each, below)"),
   ui-ux-pro-max's D19_APP paragraph ("across all six dimensions"),
   X1 ("its six fix #19 D19 dimension lines"), DIRECTIVES_F22 ("its six fix
   #19 D19 dimension lines"), and every fix22 wave-1 patch D19 bullet ("six
   dimensions"). I deliberately did NOT patch these: touching the D19_APP /
   X1 / DIRECTIVES paragraphs risks the verify19/20/21-adjacent texts, and a
   sweep of every "six" is a coordinator decision (sweep + re-verify), not a
   §13 patch. Question for the parent: sweep "six" → "seven" everywhere, or
   treat the extension line as the amending record and leave the historical
   "six" in place?
2. **Depth token values** (DEPTH-09 §5.7): `perspective 1000`,
   `parallax 0.5/0.25/0.1`, `tilt.max 6°`, `elevation blur 8/16/24` — my
   values, no SPEC source. Parent adjudicates or accepts.
3. **DEPTH-13 edit point** (§5.8): runtime block on the built less-flat-ui
   copy (chosen) vs direct edit of the shared global cursor-skills source.
   If the parent prefers the global source edited instead, DEPTH-13 moves
   there and drops out of `fix22.py` — but note the global file is shared
   outside this plugin, so a plugin-only note would leak into Anish's
   general Cursor skill.
4. **No verify22.py change made** (out of scope for this spec): the
   coordinator / verify22 author should assert: `DEPTH_F22` present in
   orchestrate (step 3 + D19 line), Taste (D19 line + dealt-moment line),
   ui-ux-pro-max (depth rules + D19 mirror), motion-foundations
   (`depthTokens`), motion-patterns (parallax/3D-hero section), polish-pass
   (SKILL.md wiring + slop-checklist depth section), less-flat-ui (overlap
   note); `D19_RULE` still verbatim in Taste + orchestrate (verify19); and
   the §13 dry-run fixtures (a)–(f) against the check phrases in §6.
