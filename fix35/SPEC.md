# Fix #35 SPEC — design-layer parity with the factory (regular side)

Approved by Anish Nov 20, 2026 ("Sync the design layer both ways"), on the
evidence of `~/workspace/hackathon-plugin/design-parity-audit-2026-11-20.md`.
One bounded job on top of fix34 (f9fc748), then stop. The factory tree
(`factory-cursor/` at c85e549) is READ-ONLY input; factory round 14 makes
the matching factory-side edits separately. Goal: after fix #35 + round 14,
the two trees' design layers are identical under the normalization below,
and both verifiers carry a parity check so they cannot drift silently.

## Setup
- Working repo: `git clone ~/workspace/hackathon-plugin/fix34/scratch-repo
  ~/workspace/hackathon-plugin/fix35/scratch-repo` (HEAD f9fc748).
- This SPEC is copied into the repo at `fix35/SPEC.md` as part of the fix.
- Build environment: symlink the durable clones into /tmp before building
  (`/tmp/ecc-repo-clean`, `/tmp/hack-skills`, `/tmp/uipro`, `/tmp/skill-add`
  → `~/workspace/hackathon-plugin/fix26/scratch-clones/*`); build.sh's
  pin_checkout verifies HEADs. Never run fix11/fix11-stage.py.
- Follow the fix34 workflow: needle-asserted stage/weave scripts
  (`fix35/stage35.py`, `fix35/weave35.py` in the fix working dir), a
  build-time `fix35/fix35.py` wired into build.sh after fix34.py if needed,
  `fix35/verify35.py` (extend verify34), audit, sweep, dry-run, MANIFEST,
  patch log, commit (author Anish Koduri, no trailer), bundle at
  `~/workspace/hackathon-plugin/hackathon-ecc-fix35.bundle`.

## Scope (regular side)
1. **Port the kitchen skill** from the factory (catalog + copy guide only,
   ISC, no vendored source), adapted per fix34 precedent: rule ID
   KITCHEN_F32 → KITCHEN_F35; "factory variant" → "fix #35"; cite repoints.
   No trigger key (design-skill precedent).
2. **Kitchen weave** (mirror the factory's weave points):
   - Taste palette-first list gains `kitchen` (canonical list below) AND
     the two factory sentences regular lacks: the citation-coverage
     sentence ("The same citation covers every palette source …") and the
     house-rule-5 Kitchen sentence.
   - Taste step 4a motion bullet gains the factory clause: "GSAP is the
     motion engine where those skills describe motion they do not
     implement, and React Bits / Kitchen supply the animated component or
     tactile piece where the widget needs one, each cited USED or
     CONSIDERED-AND-REJECTED with a D19 reason (inventory §12)".
   - Orchestrate DESIGNPKG-AUTO + palette-first sentence → canonical texts
     below (kitchen named in both).
   - Inventory §12 gains the Kitchen row (factory text, adapted cites) and
     the staged-home line goes "All four resources" → five, naming kitchen.
   - Call-map / trigger manifest updated per regular precedent (kitchen
     called by name from orchestrate/Taste; uncalled-set rules unchanged).
3. **Inventory §0 layer map + layer roles**: port factory's §0 (layer table
   + boundary rules) verbatim (provenance-normalized), and add the
   "**Layer role: …**" lead-ins to the §12 entries (foundation / motion /
   animated components / illustrations / tactile), matching factory text.
   The §0 "Intelligence" row's wording ("General design intelligence —
   styles, palettes, pairings, guidelines, icons, charts, stacks") is a
   description of ui-ux-pro-max's DATA and stays as-is in both trees; it is
   not a lead role.
4. **Inventory renumber to factory numbering**: insert §13 MotionSites as
   its own section (factory's §13 header + home paragraph; the MotionSites
   row leaves §12's table, its content moves into §13 in factory's form);
   current §13 → §14 (Motion Principles, ThreeUI), §14 → §15 (Pre-build
   Research, Design Contract), §15 → §16 (code-mode, header mirrors
   factory's structure: "(fix #34, CODEMODE_F34; inventory entry added
   fix #35, DECISION-D35-x)"). Sweep EVERY "inventory §13/§14/§15"
   citation in the regular tree (skills, rules, commands, agents) and
   remap to the new numbers; census first, each replacement asserted.
5. **Fraunces role rule**: add the factory's sentence to Taste (palette
   area, at the factory's position) and to the inventory Type row:
   "Fraunces role rule: Fraunces is body-only as the Tiempos stand-in
   (fix #20 F4) — never a display face on a build where it is the body
   face; a dealt `fraunces` pairing uses Fraunces as the display face
   under fix #20 F3 / F5 with Figtree as body — never both roles on one
   build." (Use the regular tree's own fix-cite forms as they appear in
   regular Taste today; needle-check the F4/F5 scope rules exist in
   regular's verify checks — they do, in orchestrate step 5a.) Also add
   the step-4a typography gloss "(the dealt pairing and tokens,
   `system.md` Type — Fraunces body-only as the Tiempos stand-in, fix #20
   F4; see the F4/F5 scope rules below)" if the scope rules are present
   in the file; if not, record why in the patch log instead.
6. **Taste depth bullet**: regular gains the factory's fuller GSAP cite:
   "GSAP 3D transforms (§11; usage skill `skills/gsap/SKILL.md`,
   inventory §12)".
7. **Taste design-contract block placement**: move regular's contract
   block INTO step 4a at the factory's position (end of the 4a frozen-
   system text, before the no-landing fallback + anti-generic text), so
   Taste matches factory structure.
8. **Orchestrate routing table row 10**: add "+ `motion-principles`" to
   motion work, the "3D work — + `threeui`" item, and the clause "every
   UI slice implements the design contract (`docs/design-contract.md`,
   DESIGNCONTRACT_F34) where one is issued" — factory's row-10 text with
   regular IDs.
9. **Orchestrate routing-flow line**: insert "`prebuild-research`
   (step 1.5) →" after scope, matching the factory line.
10. **Orchestrate inventory paragraph**: extend regular's paragraph with
    the factory's missing enumerations (MotionSites §13; the round-10
    motion/3D layer §14; the pipeline artifacts §15; code-mode §16;
    Kitchen §12) in regular provenance style, so the paragraph matches
    the factory's under normalization.
11. **browser-qa**: adopt the factory's MOTION-QA and CONTRACT-QA texts
    verbatim (provenance/IDs adapted) in place of regular's reworded
    versions, and add the factory's "Scripted evidence collection"
    paragraph (adapted: regular has no dispatch; the paragraph's
    code-mode/SCRIPT-FIRST content applies as written in fix34's port —
    needle-check against factory text and adapt only machinery words,
    recording each adaptation in the patch log).
12. **getlayers**: add the factory's sentence "Layer role: foundation
    (inventory `skills/orchestrate/references/design-inventory.md`
    §12) — the first layer of the one design system, consulted first;
    the direction cites every layer considered as USED or
    CONSIDERED-AND-REJECTED with a D19 reason." at the factory's position.

## Canonical texts (both trees, exact)
- DESIGNPKG-AUTO parenthetical (orchestrate SKILL + rules/hackathon-mode.mdc):
  "(design-taste-frontend / ui-ux-pro-max / less-flat-ui / polish-pass /
  motion-foundations / motion-patterns / motion-advanced /
  make-interfaces-feel-better / design-system / motionsites-web-builder /
  motion-principles / threeui / getlayers / gsap / react-bits /
  hairline-create / hairline-adopt / kitchen, with the design-lead
  deciding which leads)" — written on one line in the files, no lead
  glosses for any skill.
- DESIGNPKG-AUTO kitchen gloss sentence (after the hairline gloss):
  "`kitchen` — dqnamo's Kitchen, 15 copy-paste tactile components, ISC,
  copied from the page per project, never embedded (fix #35,
  KITCHEN_F35)."
- Taste palette-first design-package list:
  "the design package (`ui-ux-pro-max` (lookup), `less-flat-ui`,
  `motion-foundations`, `motion-patterns`, `motion-advanced`,
  `make-interfaces-feel-better`, `design-system`, `gsap`,
  `motion-principles`, `react-bits`, `threeui`, `hairline-create`,
  `hairline-adopt`, `kitchen`)"
- Orchestrate DESIGNPKG palette-first source list: the factory's current
  list (getlayers, motionsites-web-builder, gsap, react-bits,
  hairline-create, hairline-adopt, kitchen, ui-ux-pro-max, less-flat-ui,
  motion-foundations, motion-patterns, motion-advanced,
  make-interfaces-feel-better, design-system, motion-principles,
  threeui, the dealt Hallmark theme).

## Parity check (verify35 gains a section; same design as round 14's)
- Manifest: `manifests/design-parity.json` in the built tree — per-file
  SHA-256 of NORMALIZED content for the parity file set, generated at
  the end of this job; the factory's manifest must come out byte-identical
  (the parent agent cross-checks; a mismatch is reconciled before either
  bundle ships).
- Parity file set (must be fully identical after normalization):
  skills/design-taste-frontend/SKILL.md, skills/browser-qa/SKILL.md,
  skills/getlayers/SKILL.md, skills/motion-principles/SKILL.md,
  skills/threeui/SKILL.md, skills/kitchen/SKILL.md,
  skills/orchestrate/references/design-inventory.md,
  skills/ui-ux-pro-max/SKILL.md.
- Canonical-needle set (asserted present, exact text, in both trees;
  not full-file hashed): the canonical texts above in orchestrate
  SKILL.md + rules/hackathon-mode.mdc; row-10 items; routing-flow line.
- Exempt with recorded reasons (patch log): orchestrate SKILL.md and
  design-system SKILL.md full files (placement/machinery), prebuild-
  research (CAPTIVATION cite is factory-only; regular keeps the prose
  anti-derivative form per fix34), feature-expansion (paragraph
  placement), all agent files (pins), drone-only files (factory-only).
- Normalization (provenance/IDs/pins/machinery ONLY, never content
  words): `factory round \d+` → SRC; `fix #\d+[a-z]?` → SRC;
  `Fix #\d+` → SRC; `_F\d+` → `_F#`; `F-\d+` → `F-#`;
  `DECISION-[A-Z]+-?\d*` → DECISION-X; drop lines matching
  `^model:`; drop lines mentioning drone / openrouter / cm_dispatch /
  cursor-agent / orchestrator-briefing. If a content word still differs
  after this sync, that is a defect to fix at the root, not a new
  normalization rule.

## Out of scope
Model pins (regular stays on cursor-grok-4.6-high-fast), drone machinery
(stays factory-only), deploy-fast's Netlify pricing row (byte-untouched;
Dec 4 touch-up), the GLOBAL-ROUTING block, any design-content change
beyond parity. If a needle misses in a way that changes scope, STOP and
report instead of improvising.

## Decisions
- D35-1 — Direction: the regular tree's role decisions win (ui-ux-pro-max
  lookup-only); the factory's richer catalog wins for content (kitchen,
  layer map). Parity = same design system, both directions applied.
- D35-2 — Inventory numbering: factory numbering wins (§13 MotionSites,
  §14 MP/ThreeUI, §15 Research/Contract, §16 code-mode); regular renumbers.
- D35-3 — browser-qa wording: factory's verdict texts win (more
  operational); regular adopts them.
- D35-4 — New rule ID: KITCHEN_F35. No other new IDs; ported factory IDs
  keep their regular _F34 forms.
