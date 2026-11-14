# Fix #22 process patches — §9 Mobbin + §10 directives (build.sh-embedded targets)

**Status:** patch specs for the integrator. Do NOT edit `build.sh` from this file alone —
apply each spec as a patch in the existing build.sh patch blocks for the target file
(same convention as the existing `audit_patch` / `audit2_patch` entries), then rebuild.
Do NOT edit `hackathon-ecc/` directly. All anchors below are verbatim from the built
tree (`hackathon-ecc/`, Audit #66 state) and were verified unique in their target file
on Nov 12, 2026. Each new rule text carries its D19 six-dimension reason and the
theme-match precondition, as the SPEC requires.

Banned terms check: none of the new texts below contains any of the seven banned
terms (case-insensitive), and no Mobbin integration tool name is mentioned anywhere —
access is stated as "web browsing only, no API/MCP on the free tier".

---

## P1 — ui-ux-pro-max: Mobbin pattern reference (MOBBIN_PATTERN_F22)

- **Target file:** `skills/ui-ux-pro-max/SKILL.md` (build.sh-patched; upstream clone
  copied in, then patched — apply inside the ui-ux-pro-max patch block, cf. build.sh:7263).
- **Built-tree location:** line 92.
- **Anchor (verbatim, unique in file):**

  > **Generated direction — never based on a searched reference.** Web search may inform facts (real product details, competitor awareness) but never the design direction: no design may be based off a searched external reference — not a marketing website, not a Dribbble shot, not a template, not any found page.

- **Position:** insert the new paragraph immediately AFTER the "Generated direction"
  paragraph (built-tree line 92), before the next paragraph.
- **New text (insert verbatim):**

  > **Pattern reference while building (fix #22 §9, MOBBIN_PATTERN_F22):** when a build needs a component or flow this skill describes abstractly, the implementing agent MAY consult the matching Mobbin pattern (mobbin.com) for how real apps handle it — structure, states, conventions — then implements it through this skill, theme-matched, with a D19 reason. The no-copy boundary: Mobbin informs pattern knowledge only — never the design direction, never a screen to copy; the generating skill is always the recorded source in `docs/design-tokens.md`, never a Mobbin URL, and a specific Mobbin screen is never cited as the source of a decision. Access is web browsing only on the free tier ($0; limited apps/sites, no search, no Flows/Animations, 3 collections) — no paid subscription, no paid account, no account creation that costs money, no API/MCP on the free tier. If the needed pattern is paywalled or Mobbin is unreachable, build from the skills alone and record the gap — the build is NEVER blocked on Mobbin. Platform match: web patterns for web builds; iOS/Android patterns only where the build is a mobile-web surface and the pattern transfers. Theme-match precondition: a pattern is applied only when it matches the dealt theme (or, on app surfaces with no landing, the named direction in `design-system/<project-slug>/MASTER.md`). (D19 — Motion: patterns inform how a flow moves; Theme: the dealt theme filters which patterns apply; Texture: none — pattern reference sets no surface treatment; Visuals: patterns inform the structure users expect; Techniques: consultation is category-level browsing, never copying a screen; Colors: none — pattern reference sets no colour.)

---

## P2 — ui-ux-pro-max: every component spec is a directive (DIRECTIVES_F22)

- **Target file:** `skills/ui-ux-pro-max/SKILL.md` (build.sh-patched, same block as P1).
- **Built-tree location:** line 112.
- **Anchor (verbatim, unique in file):**

  > **Every component is an experience (fix #20 X1, app surfaces).** On app surfaces, each component is designed as a moment/interaction, not a static functional block; every component entry in MASTER.md states the experience it creates (what it feels like, what moment it is) alongside its six fix #19 D19 dimension lines. A component recorded only as a functional block is an incomplete build. The full X1 rule lives in `design-taste-frontend` step 4a.

- **Position:** insert the new paragraph immediately AFTER the X1 paragraph
  (built-tree line 112).
- **New text (insert verbatim):**

  > **Component specs are directives, not descriptions (fix #22 §10, DIRECTIVES_F22):** every component spec on app surfaces is a DIRECTIVE — exact values (exact tokens, exact measurements, exact type decisions: face, size, weight, line-height, tracking; exact copy; exact motion values: duration, easing, distance; exact layout instructions: structure, spacing, order), naming the skill it routes through AND giving the values. Every component entry in `design-system/<project-slug>/MASTER.md` records its directive alongside the experience it creates and its six fix #19 D19 dimension lines. A component described in prose without exact values is incomplete and FAILS the handoff check; a directive without its D19 reason is incomplete; a reason without its directive is not a design decision. Implementers execute component directives verbatim and do not re-interpret them — an ambiguous, unbuildable, or conflicting directive is surfaced as a recorded gap instead of improvised around; improvising around a directive is off-skill improvisation and fails the audit. Theme-match precondition: every component directive must match the recorded direction. (D19 — Motion: directives carry exact motion values where motion is decided; Theme: directives are generated through the recorded direction; Texture: directives name the exact treatments where texture is decided; Visuals: directives fix the exact visual outcome per component; Techniques: directives name the skill they route through; Colors: directives carry exact colour tokens.)

---

## P3 — GAN planner: spec design direction recorded as directives (DIRECTIVES_F22)

- **Target file:** `agents/ecc-gan-planner.md` (build.sh-embedded; apply in the GAN
  agent patch block, same convention as the existing `audit2_patch` /
  B3 entries for this file, e.g. build.sh:10702, 22367).
- **Built-tree location:** line 44 (the Design Direction block of the spec template).
- **Anchor (verbatim, unique in file — opening of the Direction source bullet):**

  > - **Direction source**: [the design direction recorded by the design-lead (model `grok-4.7-high`) in `docs/design-tokens.md` BEFORE this loop — copied here, not generated:

- **Position:** insert the new bullet immediately AFTER the complete Direction source
  bullet (built-tree line 44), before the blank line preceding `## Features (prioritized)`.
- **New text (insert verbatim):**

  > - **Directives, not descriptions (fix #22 §10, DIRECTIVES_F22):** the Design Direction section above is recorded as DIRECTIVES, not prose — every design decision in `gan-harness/spec.md` carries exact values (exact tokens, exact measurements, exact type decisions: face, size, weight, line-height, tracking; exact copy; exact motion values: duration, easing, distance; exact layout instructions: structure, spacing, order), each naming the skill it routes through, plus its fix #19 D19 reason. A design decision written as prose without exact values is incomplete and FAILS the handoff check; a directive without its D19 reason is incomplete. The Generator executes these directives verbatim and does not re-interpret them. Theme-match precondition: every directive must match the recorded direction copied above. (D19 — Motion: directives carry exact motion values; Theme: directives are the recorded direction expressed as values; Texture: directives name the exact treatments; Visuals: directives fix the exact visual outcome; Techniques: directives name the skill they route through; Colors: directives carry exact colour tokens.)

---

## P4 — GAN generator: execute directives verbatim (DIRECTIVES_F22)

- **Target file:** `agents/ecc-gan-generator.md` (build.sh-embedded; same GAN patch
  block convention as P3).
- **Built-tree location:** lines 25–30 (Key Principles list).
- **Anchor (verbatim, unique in file):**

  > 6. **Keep the dev server running** — The Evaluator needs a live app to test.

- **Position:** insert the new paragraph immediately AFTER the Key Principles list
  (i.e. after the anchor line), before the `## Workflow` heading.
- **New text (insert verbatim):**

  > **Directives, not descriptions (fix #22 §10, DIRECTIVES_F22):** the spec's design decisions are DIRECTIVES with exact values — execute them verbatim. Do not re-interpret a directive: if a directive is ambiguous, unbuildable, or conflicts with another directive, surface it as a recorded gap (note it in the iteration commit message and in your return text) instead of improvising around it. Improvising around a directive is off-skill improvisation and fails the audit. Creativity lives in the spec's directives, fidelity in the execution. A directive without its D19 reason is incomplete — if the spec hands you a design decision as prose without exact values, or a directive without its D19 reason, flag it as a recorded gap and do not build on the prose. (D19 — Motion: execute the spec's exact motion values; Theme: execute the recorded direction as written; Texture: execute the spec's exact treatments; Visuals: execute the spec's exact visual outcome; Techniques: the spec names the skill each directive routes through; Colors: execute the spec's exact colour tokens.)

---

## P5 — GAN evaluator: feedback items are directives (DIRECTIVES_F22)

- **Target file:** `agents/ecc-gan-evaluator.md` (build.sh-embedded; same GAN patch
  block convention as P3).
- **Built-tree location:** line 132 (Step 5: Write Feedback).
- **Anchor (verbatim, unique in file):**

  > Write feedback to `gan-harness/feedback/feedback-NNN.md`:

- **Position:** insert the new rule paragraph immediately AFTER the anchor line,
  before the ```markdown feedback-template fence.
- **New text (insert verbatim):**

  > **Feedback items are directives, not descriptions (fix #22 §10, DIRECTIVES_F22):** every feedback item in the file is a DIRECTIVE — an exact replacement (exact file, exact element, exact old value → exact new value, exact tokens/measurements/copy), naming the skill it routes through, plus its fix #19 D19 reason. A feedback item described in prose without exact replacement values is incomplete and FAILS the handoff check; a directive without its D19 reason is incomplete. The Generator executes feedback directives verbatim; a feedback item that asks the Generator to re-interpret a design decision instead of giving it exact values is not a directive and must be rewritten. Theme-match precondition: every feedback directive must match the recorded direction. (D19 — Motion: feedback directives carry exact motion values where motion is fixed; Theme: fixes conform to the recorded direction; Texture: feedback names exact treatments where texture is fixed; Visuals: feedback states the exact visual outcome; Techniques: feedback names the skill it routes through; Colors: feedback carries exact colour tokens.) Scoring itself stays as the rubric requires — this rule governs the feedback items, never the scores, and never a screen-distinctiveness verdict (that is `browser-qa`'s alone).

---

## Integrator checklist for these five specs

1. Confirm each anchor still matches verbatim in the current built tree before patching
   (anchors were verified unique on Nov 12, 2026; a later wave-1 edit to the same
   files would change line numbers, not anchor text — re-grep first).
2. Apply P1–P2 in the ui-ux-pro-max build.sh patch block; P3–P5 in the GAN agent
   patch block. Do not hand-edit `hackathon-ecc/`.
3. After rebuild, verify: `MOBBIN_PATTERN_F22` occurs once in
   `skills/ui-ux-pro-max/SKILL.md`; `DIRECTIVES_F22` occurs once in each of
   `skills/ui-ux-pro-max/SKILL.md`, `agents/ecc-gan-planner.md`,
   `agents/ecc-gan-generator.md`, `agents/ecc-gan-evaluator.md` (built tree AND build.sh).
4. Banned-term scan (case-insensitive) over the five new texts and their targets:
   the seven banned terms — expect 0 new hits.
