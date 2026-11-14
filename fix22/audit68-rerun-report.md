# Audit #68 — RE-RUN (fix #22, new build)

**Date:** Nov 13, 2026 (audit run Nov 13 CST)
**Auditor:** Audit #68 re-run worker (check only — no plugin file edited, build.sh not
run, fix22.py / apply22.py / verify22.py not run or edited, nothing
bundled/committed/pushed, no message sent to anyone)
**Built tree:** `~/workspace/hackathon-plugin/hackathon-ecc/`
**Build state measured by this audit:** build.sh **23,773 lines, md5
`e9462b57429acd914cd0aacdebc486d0`** (matches the task statement). Diff vs the
pre-fix22 backup `build.sh.before-fix22` (23,647 lines): **+126 lines, 0
deletions** (the fix22 block + the DEMOGATE runtime patches + the §13–§17
follow-up). Diff vs the first Audit #68 build (23,758 lines, md5
`306dd648ab9dc4bee0e019a896e26f64`): **+15 lines** — the DEMOGATE patch lines
in build.sh.
**Verifiers re-run by this audit:** `fix22/verify22.py` **368/368 PASS**
(exit 0, run directly); prior verifiers pass except their frozen post-fix21
build.sh fingerprint lines (see §10). All counts below were re-derived
independently (own greps / own Python / own full-file reads), not copied
from verifier output or from the first Audit #68 report — every B-1/B-2/B-3
site was re-read in full context against the new build.

**Method note:** every file named in §8(b) was read IN FULL (orchestrate
SKILL.md lines 40–90, 120–122, 327, 344; orch-build-mvp skill + command;
orch-change-feature skill + command; hackathon-pitch, deploy-fast,
readme-writer, feature-expansion, fastapi-patterns `/demo` mentions with
context; hackathon-mode.mdc in full; dispatch-prompt.md in full;
commands/demo.md in full; pitch-deck-video SKILL.md lines 1–830 in full).
The /demo verdicts rest on those full-context reads, not on grep snippets.

## Verdict: AUDIT #68 RE-RUN: NOT ZERO — 0 BLOCKING, 2 MINOR

All three first-run BLOCKING findings are FIXED in this build: no orchestrate
step, no hook, no post-build trigger, no finish-report step, and no other
command invokes /demo or pitch-deck-video automatically. The §1–§17 weave is
still clean (see §§1–7, 9), verify22 is 368/368, the dry-run #37 §5 note-1
template defect (the `remotion@4.0.542` no-bin invocation) is fixed in both
template scripts, and sweep #30b Finding 2 (the stale `40x40px` hit-area
wording) is fixed — zero occurrences remain. What keeps this re-run from ZERO
is two MINOR documentation-consistency defects in the same rule file,
`rules/hackathon-mode.mdc`: (§3) one parenthetical still states the OLD
first-build order "after deploy, demo, commit, and README", and (§7) the
behavior-change sentence asserts the change "is recorded in
`fix22/MANIFEST.md`" while `fix22/MANIFEST.md` still does not exist. Neither
invokes /demo and neither changes runtime behavior — hence minor, not
blocking — but both are exactly the leftover-sequence / behavior-record
consistency the re-run was tasked to check (task items 6), so they are
findings, not open items.

## MINOR findings

### M-1 — hackathon-mode §3 still states the old first-build order (deploy → demo → commit → README)
- **File:** `hackathon-ecc/rules/hackathon-mode.mdc:22`
- **Context (quoted verbatim):** "The one permitted invocation is the named
  end-of-project run immediately before the first build's final report (after
  deploy, demo, commit, and README): that run IS the very end of the
  project — it runs once, it never gates a feature, and it never fires
  mid-build or during a one-prompt removal."
- **Why this is a finding:** this is the ONLY remaining sequence in the tree
  that lists demo as a first-build pipeline step. A tree-wide grep for
  `deploy, demo|deploy → demo|demo → commit|demo, commit|deploy, demo, commit`
  returns this line alone. It contradicts the new contract stated three times
  in the same file and in orchestrate: hackathon-mode §1 (`:12`, "… → verify →
  polish → deploy → README → final report… /demo is never part of this
  sequence", DEMOGATE_H2_F22), hackathon-mode §7 (`:68`, "Then the README is
  written and the final report is delivered (deploy → README → final
  report)", DEMOGATE_H1_F22), and orchestrate step 6 (`:82`, "Order: verify →
  polish → deploy → commit → README → final report", DEMOGATE_O9_F22). The
  §7 carve-out was already fixed to "after deploy/commit/README"; the §3
  carve-out was missed.
- **Why minor, not blocking:** the sentence describes WHEN the deferred
  end-of-project run happens; it does not dispatch /demo, and no agent
  following it would film a video. It misstates the sequence, it does not
  execute one.
- **What must change:** replace "(after deploy, demo, commit, and README)"
  with "(after deploy, commit, and README)" — matching the §7 wording
  exactly.

### M-2 — hackathon-mode §7 asserts a behavior-change record that does not exist yet
- **File:** `hackathon-ecc/rules/hackathon-mode.mdc:68`
- **Context (quoted verbatim):** "The demo video is no longer a required
  deliverable of the first build — the behavior change is recorded in
  `fix22/MANIFEST.md`."
- **Why this is a finding:** `fix22/MANIFEST.md` does not exist
  (`ls fix22/MANIFEST.md` → "No such file or directory"; verify22.py itself
  prints the "not yet written" NOTE). The sentence is otherwise correct —
  the behavior change is real and is stated consistently everywhere else —
  but as written it points at a record that is not there. It is the only
  `MANIFEST.md` reference in the built tree; the only other reference is
  verify22.py's own note.
- **Why minor, not blocking:** the rule's operative content (no auto-film,
  deploy → README → final report) is correct and verified; only the
  record-pointer is premature.
- **What must change:** write `fix22/MANIFEST.md` with the behavior change
  recorded explicitly (already a close criterion — see §10), after which this
  sentence becomes true with no text change. Alternatively, soften the
  sentence until the manifest exists; the manifest is the preferred fix.

## BLOCKING findings

None. B-1, B-2, B-3 from the first run are all verified FIXED below (§8b).

## 1. SPEC compliance §1–§17 — all placed

- **144-item disposition:** an independent script checked all 142 A–G rows
  of `fix22/disposition-merged.md` plus H1/H2 against the CURRENT tree
  (151 table rows = 144 items + 7 non-item rows: separators + the 5 process
  rows Mobbin / Directives / Libraries / Bang). Every item's content is
  present in its SPEC'd home file. 51 rows' cited line numbers are STALE
  (not missing content): the §13–§17 follow-up and the DEMOGATE edits
  inserted blocks above them — the same mechanical drift Audit #68 and
  sweep #30b recorded (56 / 61 rows then). Ten rows my first scripted pass
  flagged as "missing" (B1, B2, B3, B4, B5, B7, B10, B15, B18, H1) are all
  present by their token/value form — e.g. B1 "Entrances ease out (fix #22
  B1)" motion-foundations `:219`; B2 `dropdown: 0.2` "dropdowns animate at
  150–250ms" `:404`; B3 `staggerRow: 0.03` `:405`; B4 `scale(0.97)`
  make-interfaces-feel-better `:118`; B5 `stretch: 1.12` `:428`; B7 "Move
  along arcs" motion-patterns `:96`; B10 `popover: 0.95` `:427`; B15
  `exitFactor: 0.8` `:431`; B18 crossfade motion-patterns `:82`; H1 "accent
  colour" ui-ux-pro-max `:18`. The flag was the checker's prose-name
  matching, not a plugin gap. Content verified present; verify22 (string
  checks, not line numbers) passes 368/368. The disposition's line numbers
  should be refreshed when the manifest is written — a documentation
  staleness note, not a finding.
- **§13 depth:** orchestrate step 3 names the depth strategy per surface
  (incl. explicit "flat by choice — <reason>"); ui-ux-pro-max depth rules;
  motion-foundations depth tokens; motion-patterns 3D patterns; Taste
  depth-as-dealt-moment; polish-pass depth check. Cross-refs to A11 / Bang
  camera / Vanta / GSAP 3D / F6 present, no duplication.
- **§14 orbs:** nine states, no "thinking" state — see §4.
- **§15/§17 libraries:** pins + licenses + stack scope as specified —
  see §5.
- **§16 Vercel:** pinned snapshot + no live fetch + dedupe 136 — see §6.
- **Process additions (§9 Mobbin, §10 directives, §11 libraries, §12 Bang):**
  all present with their boundaries (evidence in §§4–6 and §7; Mobbin
  research step orchestrate `:64` MOBBIN_RESEARCH_F22, pattern refs Taste
  `:445` + ui-ux-pro-max `:167`, QA check polish-pass `:104`;
  DIRECTIVES_F22 in all 8 required locations — re-counted 8 occurrences in
  the built tree).

## 2. Standing rules — no regressions

- **Banned terms 0 in the built tree.** Own case-insensitive grep over
  `skills agents commands rules hooks README.md` (`--exclude-dir=node_modules`)
  for `claude|codex|anthropic|opus|sonnet|haiku|composer-2.5` returns 0
  lines (grep exit 1). verify22 agrees ("banned terms 0"). Note: build.sh
  itself contains ~701 `claude` hits in NON-installed text (build-script
  comments and GAN-harness shell-script strings that do not ship into the
  skills/commands/rules tree) — the SPEC criterion is the built tree, and
  the built tree is 0. The staged `new-rules/hackathon-mode.mdc` still
  carries the upstream phrase "its upstream `claude -p` invocation path"
  while the built rule reads "its upstream CLI-subprocess invocation path";
  that is the pre-existing fix #16 runtime scrub (fix16.py, recorded in
  fix16-run-log.md), not a build mismatch — the staged source is the
  pre-scrub upstream wording, the built tree is the shipped artifact.
- **Grok pins only.** Tree-wide (excl. node_modules): `grok-4.7-high` **54**,
  `cursor-grok-4.6-high-fast` **102**, bare `grok-4.6-high-fast` (proper
  negative-lookbehind grep, not substring) **0** — identical to Audit
  #67/#68's counts.
- **Font rules (fix #19/#20/#21) untouched.** verify19's font anchors pass
  (see §10); F4 Tiempos/Fraunces body-only and F7 per-element font decisions
  present in orchestrate + Taste; static instances only (no variable-font
  rows — verify19 F2 passes).
- **Screen-verdicts rule intact.** `browser-qa` remains the sole verdict
  executor: slop checklist `:7–8` ("`browser-qa` alone issues verdicts on
  rendered screens"), polish-pass `:98–99` (Vercel + slop findings are
  "candidate evidence for `browser-qa`, never verdicts"), Taste finish-gate
  `:497` (same standing). Every new check in this fix is worded as
  candidate evidence, never a verdict.
- **No new skill / command / trigger key.** Counts re-derived from the built
  directories: **166 skills / 72 agents / 123 rules / 87 commands**;
  hooks.json defines **15** hook events. Trigger keys **64**
  (`skill-triggers@1.json` `triggers` dict, 64 keys); verify22 asserts every
  key resolves to a real skill dir (PASS).
- **Anchor spot counts** (built tree, excl. node_modules) match the
  sweep #30b table: SLOP_F22 28, TRENDS_F22 53, DIRECTIVES_F22 8,
  DEPTH_F22 35, ORBS_F22 24, MOBBIN_RESEARCH_F22 1, BANG_ANTISLIDE_F22 1,
  VERCEL_F22 8, ACCENT_F22 11. No orphaned anchor found in the spot-checks.
- **D19 six-dimension reasons on every new rule** (spot-checked in the slop
  intro, unslop intro, token groups, Mobbin QA check, library scope blocks,
  Bang menus, orb + depth sections — each dimension a reason or explicit
  `none — <reason>`).
- **Theme-match precondition everywhere** (principles, tokens, slop/unslop
  intros, trends intro, library scope blocks, Mobbin QA, Bang menus).

## 3. §13 D19 form — byte-identical, extension separate

- D19 rule line byte-identical: orchestrate SKILL.md `:120` ==
  design-taste-frontend SKILL.md `:423` (2,090 chars each, compared by
  Python `==`).
- Extension line byte-identical: orchestrate `:122` == Taste `:425`
  (923 chars each, exact).
- The extension line is separate and immediately after the rule (blank line
  between, `:121`/`:424` empty in both files). No "six dimensions" text was
  rewritten: "six dimensions" occurs 2× in each file (the rule + the
  extension line's "The six dimensions above are unchanged").

## 4. §14 Thinking Orbs — verified

- **Nine states, no "thinking" state:** working, searching, solving,
  listening, connecting, weaving, composing, breathing, shaping
  (motion-patterns `:347–355` table). The file states at `:342` ("NO state
  named 'thinking'") and `:359–361` the correction to the SPEC §14 draft
  mapping ("thinking = reasoning" is wrong; reasoning maps to `working` or
  `solving`; `breathing`'s on-screen label reads "Thinking…" but it is the
  IDLE/WAITING state — never use it for reasoning).
- **Pin + license:** `thinking-orbs@0.3.2`, MIT (ui-ux-pro-max `:122`,
  motion-patterns `:334`, `:442`; orchestrate `:64`; slop-checklist `:599`).
  Pin choice (npm-published 0.3.2 vs repo main's 0.3.1) recorded with its
  reason in ui-ux-pro-max `:122`.
- **Sizes 64/20** with per-state tunings (motion-foundations `:498–540`);
  speed multiplier; monochrome rule; reduced-motion frozen one-frame orb;
  offscreen/hidden pause; DPR capped at 2; 2D canvas only.
- **RareFormLabs:** orbs-patches.md §2.5 records verbatim
  "rareformlabs connection unresolved — asset verified independently" and
  no patch text mentions RareFormLabs. The manifest half of that
  requirement is pending only because `fix22/MANIFEST.md` does not yet
  exist (see §10 open items) — the patch-report half is done.

## 5. §15/§17 libraries — verified

- **§15:** R3F (`@react-three/fiber@9.8.2` React 19 / `@react-three/fiber@8.18.0`
  React 18, MIT; strict pairing — "React 18 + R3F v9 FAILS the pairing
  check", Taste `:135`, ui-ux-pro-max `:445`); liquid-glass-js (commit
  `78cb6ccb…`, MIT, NO npm package — copy `container.js`/`button.js`/
  `glass.css`, html2canvas@1.4.1 noted, ui-ux-pro-max `:452`,
  less-flat-ui `:145–183`); ShaderGradient (`@shadergradient/react@2.4.20`,
  v2 NOT legacy v1.3.5, MIT declared in package.json + README but NO root
  LICENSE file — caveat recorded, Taste `:134`, ui-ux-pro-max `:484`);
  liquid-logo (standalone tool, commit `689bb38a…`, PolyForm Shield 1.0.0
  NOT MIT + `@paper-design/shaders-react` Apache 2.0, static-logo fallback,
  attribution comment, honest-input check — Taste `:435`, ui-ux-pro-max
  `:237–257`).
- **§17:** Casberry (standalone tool, terms unresolved, ScamAdviser 1/100
  recorded — motion-foundations `:115`, slop-checklist `:526` — exports
  reviewed as untrusted code, motion-patterns `:893`); OriginKit (10
  fetches/key/day cap, ui-ux-pro-max `:516`; Origin UI distinction,
  motion-patterns `:858–860`; conditional/source-available licence,
  redistribution restriction); daisyUI (`daisyui@5.7.50`, MIT, Tailwind v4
  ONLY pairing, default-theme-unexamined FAILS, design-system `:37–50`,
  ui-ux-pro-max `:501–514`).
- **§11 (re-checked):** Lenis `lenis@1.3.27` MIT; GSAP `gsap@3.15.1`
  GreenSock Standard "no charge", NOT MIT; Vanta `vanta@0.5.24` MIT +
  `three@0.134.0`; React Bits commit `9d9c687d…` MIT + Commons Clause
  (ui-ux-pro-max `:395`, `:422–430`).
- **One-WebGL rule:** present incl. Casberry exports (WEBGL_ONE_F22,
  motion-patterns `:805`, `:891–892`; slop-checklist `:490–491`).
- **Running total 11:** "§11's 4 + §15's 4 + §17's 3 = 11"
  (ui-ux-pro-max `:523`).
- **Dangling `liquid-glass-design` reference:** resolved — 0 occurrences
  in the built tree; the 4 hits in `build.sh` (`:18731`, `:19412`,
  `:19449`, `:19458`) are unchanged from `build.sh.before-fix22`: a
  governance/regression list noting the skill does not exist, not a live
  pointer.

## 6. §16 Vercel — verified

- **Pinned snapshot:** `skills/polish-pass/reference/vercel-checklist.md`
  (453 lines, VERCEL_F22 anchor `:1,3`), source
  `vercel-labs/web-interface-guidelines`, file `command.md`, commit
  `4ecfb9fb8d1d3b7009674869b3aaee2f904042e1`, dated 2026-10-05.
- **NO live-fetch instruction:** grep for
  `raw.githubusercontent.com/vercel-labs` over the whole built tree
  (excl. node_modules) returns **0**. The only two
  `raw.githubusercontent.com` hits in the tree are pre-existing
  codebase-memory install URLs (`DeusData/codebase-memory-mcp/v0.12.1`,
  pinned) — unrelated to Vercel. The checklist states "This file holds the
  rules. It never fetches anything" and names the upstream live-fetch form
  a flagged prompt-injection hazard that is "NEVER the weave".
- **Dedupe 136 rows:** independently re-derived by rule-id parse of
  `fix22/vercel-dedupe.md` — **136 unique rule ids: 90 `command.md` rules +
  14 anti-patterns + 32 AGENTS.md-only rules**, every row carrying a
  disposition word (already-covered / partial / new / duplicate-of /
  conflict), **0 unaccounted**.
- **AG19 conflict recorded:** vercel-dedupe.md `:262` — APCA vs WCAG 4.5:1,
  "**conflict — parent adjudication**… Until then, WCAG 4.5:1 stands and
  APCA is not woven." Sole conflict.
- **License gap recorded:** rules repo ships an MIT LICENSE (© 2025 Vercel
  Labs); skill repo has NO LICENSE file, README states MIT only; "no
  skill-repo text is copied here".
- **ECC-source check recorded:** ECC snapshot dated 2026-09-21 used as the
  form; the plugin's ECC source at its pin does NOT carry the skill, so the
  rules were ported from the rules repo at the pinned commit.
- **Sweep #30b Finding 2 FIXED:** the stale "40x40px, ideally 44x44px"
  wording is gone — `40x40px` occurs **0** times in the built tree and
  **0** times in `fix22/vercel-dedupe.md` (grep exit 1); the live rule is
  "44x44px minimum (the plugin floor)" (vercel-dedupe.md carries it twice).
- **Wiring:** polish-pass SKILL.md `:98–99` runs the Vercel checklist on
  every pass with the same standing as the slop checklist (candidate
  evidence, never verdicts; cleared only by a recorded D19 reason +
  theme-fit).

## 7. Weaving quality — woven, not appended (spot-checked)

Spot-checks only — this audit did not re-run the sweep's full
weaving-coherence pass (see §10). One item per section traced to its SPEC'd
placement AND reachable from the design-package flow:
- **A:** orchestrate step 3 slice briefs name the principles/laws
  (PRINCIPLES_F22/LAWS_F22) with one-line consequences, recorded in the
  decision record; pointers from make-interfaces-feel-better and
  ui-ux-pro-max.
- **B:** tokens in motion-foundations (`dropdown: 0.2` B2, `staggerRow:
  0.03` B3 with the Rule-5 conflict flag, `stretch: 1.12` B5, `inOut` B9,
  `popover: 0.95` B10, `exitFactor: 0.8` B15 with the quick-reference
  conflict flag) + rules/examples in motion-patterns/motion-advanced.
- **C/D:** polish-pass reference files wired into polish-pass SKILL.md
  `:98–99` on every pass; Taste finish-gate `:497` runs the SLOP_F22
  checklist as a static check; CD pointers in ui-ux-pro-max quick-reference
  and motion-* present.
- **E:** Taste menu `:248–395` (20 entries, each "Opt-in only,
  theme-matched"); TRENDS_F22 occurs **23×** in Taste SKILL.md (20 entries
  + intro line carrying 2 + finish-gate pointer); 16 Hallmark Range lines
  in 15 theme files; E12/E14/E16 menu-only.
- **F:** verification-only; all 22 treatments + #23 Soft Shadow present in
  less-flat-ui; R3 two-kinds rule intact.
- **G:** glossary `design-taste-frontend/references/design-glossary.md`
  (GLOSSARY_F22, 20 terms); owning-skill pointers bidirectional.
- **H1/H2:** H1 accent concept ui-ux-pro-max `:125`, sprawl check
  slop-checklist `:419`, D11 points at it; H2 accent hierarchy in
  orchestrate step 3 + ui-ux-pro-max `:15` + polish check `:450`.
- **§9–§17:** all woven at their SPEC'd touchpoints; pointers resolve; no
  orphaned F22 anchor found in the spot-checks.

## 8. /demo gates — verdicts

### (a) CALLABLE — PASS by wiring; live execution NOT run by this audit
- `hackathon-ecc/commands/demo.md` exists, frontmatter
  `description: "Generate a narrated product demo video, under 2:10, of
  the hackathon project. Use when the user wants a demo video, launch
  video, product walkthrough, or hackathon submission video."` — correct
  name (`demo` → `/demo`), correct placement (`commands/demo.md`).
  Reachable from the command list: the file sits in `commands/` (87
  commands, counted), is listed in the plugin README (`:44–47`, "`/demo` —
  generate a narrated product demo video, under 2:10… `/demo <path>`,
  `/demo --rebuild`, `/demo --script`, `/demo --render`"), and is named in
  `.cursor-plugin/plugin.json` ("…with … `/demo` and `/orchestrate`
  commands").
- It invokes pitch-deck-video correctly: "Use the pitch-deck-video skill
  to generate a narrated product demo video… Follow that skill exactly:
  scaffold its template next to the app, learn the app from screenshots
  before writing any narration, write shots.json, build, and QA by looking
  at the contact sheets — do not skip the QA step." Args pass through as
  the skill defines them: `/demo`, `/demo <path>`, `--rebuild`, `--script`,
  `--render`, `--montage`, `--explainer` (montage/explainer opt-in, ask
  first). Films the LOCAL app only; never a deployed URL.
- §12 port woven into pitch-deck-video's STAGED source: all 6
  BANG_*_F22 anchors present in `new-skills/pitch-deck-video/SKILL.md` at
  the same lines as the built copy — `:247` BANG_ANTISLIDE_F22, `:281`
  BANG_ONEWORLD_F22, `:304` BANG_STYLES_F22, `:337` BANG_OPENERS_F22,
  `:373` BANG_KINETIC_F22, `:409` BANG_EXPLAINER_F22 — and the staged
  SKILL.md, all staged references/, and all staged template/ files are
  byte-identical to the built tree (diff clean; staged
  `commands/demo.md` == built `commands/demo.md`).
- §15 liquid-logo brand-mark step produces the mark ONCE outside the video
  pipeline: Taste `:435` + ui-ux-pro-max `:237–257` — "liquid-logo is a
  STANDALONE TOOL, not a library to import and not a runtime dependency:
  run it (or its hosted version) to produce the animated brand mark ONCE —
  export MP4/PNG… and ship the output as an asset… never runtime-heavy,
  never the only logo" (static-logo fallback; PolyForm Shield; attribution
  comment). No runtime import of liquid-logo anywhere in the video
  pipeline; the Bang port did not change this.
- **Remotion invocation fix (dry-run #37 §5 note 1 — FIXED in this
  build):** template `scripts/build.mjs:335` now calls
  `npx @remotion/cli@4.0.526 render …` and `scripts/qa.mjs:42` now calls
  `npx @remotion/cli@4.0.526 still …` — verified in the built tree AND the
  staged source. `remotion@4.0.542` occurs **0** times in the built tree,
  staged sources, and build.sh. Template `package.json:15` pins
  `@remotion/cli: 4.0.526` (with `remotion: 4.0.526` at `:21`), so the
  scripts now match the pin. No other `remotion@` invocation exists in
  either template copy.
- **What was NOT verified (stated explicitly, per the task):** no live
  /demo execution was run in this audit — this audit is read-only (no
  build.sh runs, no filming). Dry-run #37's live evidence (35/35 contract
  checks; invocation path exercised to the `record.mjs` entry point, blocked
  only on the missing browser binary) predates this build (23,758 /
  `306dd648…`); the only template change since is the remotion-CLI
  invocation fix above, which this audit verified textually but did NOT
  live-execute — `qa.mjs` stills rendering on the fixed invocation remains
  unverified live. So callability is established by wiring (command file +
  frontmatter + command-list reachability + skill invocation path +
  staged==built + dry-run #37's prior-build live path), NOT by a live film
  on this build. The invocation path (shots.json → Remotion → film →
  narrate) resolves end-to-end in the skill text, with no missing step —
  but that is a wiring claim, not a live-execution claim, and this audit
  does not present it as one.

### (b) NOT AUTOMATIC — PASS (B-1, B-2, B-3 all verified FIXED)
- Grep-verify: hooks contain zero "demo" hits (`hooks/hooks.json` 0;
  all hook `.js` files 0) — no hook invokes /demo. No post-build trigger
  or finish-report step invokes /demo (the end-of-project checks run the
  six deferred audits, not /demo). `diff build.sh.before-fix22 build.sh`
  = 126 changed lines, of which 15 contain DEMOGATE markers — the runtime
  patches B2S1–B2S6, B2C1, B3S1–B3S7, B3C1 are present in build.sh; the
  orchestrate/hackathon-mode gates (DEMOGATE_O4/O9/H1/H2) live in staged
  sources, verified staged==built for orchestrate SKILL.md and
  pitch-deck-video, and read in full in the built tree for hackathon-mode.
- Full-context reads of every pitch-deck-video referencer:

  - **B-1 orchestrate — FIXED.** Step 5 is now "Verify → polish → deploy,
    in that order" (`:73`, three sub-steps). The old step 5d is replaced by
    a gate paragraph (`:80`): "**Demo — never automatic (fix #22 /demo
    gate, DEMOGATE_O4_F22).** `/demo` (`pitch-deck-video`) is NEVER
    dispatched by this pipeline. It runs ONLY when the user invokes
    `/demo` explicitly (or the user's request explicitly asks for a demo
    video). When it runs, it films the LOCAL app from the project dir only
    … If no video was requested, the final report notes that no demo video
    was filmed." The sequence line (`:56`) now reads "… → verify → polish
    → deploy → README → final report). /demo is never part of this
    sequence — it runs ONLY when the user invokes it explicitly (fix #22
    /demo gate)." Step 0 (`:58`) is now conditional: the narration-key
    prompt fires "ONLY when the user asked for a demo video… If the user
    did NOT ask for a demo video, do NOT send this prompt". Step 6 (`:82`)
    Order sentence: "verify → polish → deploy → commit → README → final
    report. (A demo video is filmed only when the user invokes `/demo`
    explicitly — it is never part of this order; fix #22 /demo gate,
    DEMOGATE_O9_F22.)" The final-report sequence (`:327`): "Sequence:
    verify → polish → deploy → README (`readme-writer`, orchestrate step
    6) → final report. (A demo video is filmed only when the user invokes
    `/demo` explicitly — it is never part of this sequence; if one was
    filmed, the report carries its handoff below.)" The README input is
    conditional ("passing it the deployed URL from the ledger and, if a
    video was filmed, the video file path … as inputs"). The demo-video
    handoff (`:344`) is headed "(only if a video was filmed)".
  - **B-2 orch-build-mvp — FIXED.** Skill step 8 (`:83`): "**Deploy via
    `deploy-fast`.** **Demo — never automatic (fix #22 /demo gate,
    DEMOGATE_B2S1_F22).** `/demo` is not filmed here. … Do NOT film via
    `/demo` here — `/demo` (`pitch-deck-video`) runs ONLY when the user
    invokes it explicitly (or the user's request explicitly asks for a
    demo video). If the user asked for one, film the LOCAL app from the
    project dir after deploy … If no video was requested, the final report
    notes that no demo video was filmed. (fix #22 /demo gate,
    DEMOGATE_B2S2_F22)". Step 9 (`:84`) carve-out timing reads "after
    deploy/commit/README" (DEMOGATE_B2S6_F22). Command step 8 (`:36`):
    "Deploy via `deploy-fast`. Do NOT film via `/demo` here — `/demo`
    runs ONLY when the user invokes it explicitly (or the user's request
    explicitly asks for a demo video); if the user asked for one, film the
    LOCAL app from the project dir only, never a deployed URL… (fix #22
    /demo gate, DEMOGATE_B2C1_F22)". The "required deliverable" language
    is gone from both files.
  - **B-3 orch-change-feature — FIXED, and the removal re-film was REMOVED
    (not carved out as an exception).** Skill step 5 (`:51`): "…before any
    future re-film, update `shots.json` FIRST … **If the user asks for a
    re-film, re-film via `/demo --rebuild`**, which films the LOCAL app
    from the project dir (`APP_DIR`/project root), never a deployed URL…
    (fix #22 /demo gate, DEMOGATE_B3S1_F22)". The done-condition text
    reads exactly as the task required: 'The removal's done-condition for
    the video ("the demo video reflects the removal, or is flagged as
    stale") is satisfied by the re-filmed LOCAL video (if the user asked
    for a re-film) + the honest hosting note, or by the stale-video record
    when no re-film was requested — never by a phantom upload, never by an
    automatic re-film. (fix #22 /demo gate, DEMOGATE_B3S5_F22)'. No
    unconditional re-film remains: the same paragraph states "(The poll
    verifies the redeploy; it is not a prelude to filming — no re-film
    happens here.)", step 6 (`:52`) reports "demo video STALE — shows the
    removed feature; re-film with `/demo --rebuild` on request"
    (DEMOGATE_B3S7_F22), and the command (`:25`) says "note in the final
    report that the demo video is now stale (re-film with `/demo --rebuild`
    only when the user asks), re-upload the video and update its link only
    if a re-film was requested and a hosted link exists" (DEMOGATE_B3C1_F22).
    The B-3 decision recorded in the task (REMOVED, not exception) is
    honored in the text.
  - **hackathon-mode.mdc — MANDATE REMOVED.** §1 (`:12`): first-build
    sequence ends "… → verify → polish → deploy → README → final report…
    /demo is never part of this sequence — it runs ONLY when the user
    invokes it explicitly (fix #22 /demo gate, DEMOGATE_H2_F22)". §7
    (`:68`): "The first build does NOT film `/demo` automatically (fix
    #22 /demo gate, DEMOGATE_H1_F22). `/demo` (`pitch-deck-video`) runs
    ONLY when the user invokes it explicitly (or the user's request
    explicitly asks for a demo video) — never as a pipeline step, never by
    default. … Then the README is written and the final report is
    delivered (deploy → README → final report). The demo video is no
    longer a required deliverable of the first build". One leftover
    remains in this file — see M-1 (§3) and M-2 (§7 record pointer).
  - **commands/demo.md — dispatch note FIXED.** The old note ("If this
    /demo run was dispatched by orchestrate (step 5d) or orch-build-mvp
    (step 8), do NOT prompt") is gone. The new text: "If this /demo run
    was invoked with a narration key already provided (via the dispatch's
    Environment field as an `ELEVENLABS_API_KEY` env instruction), do NOT
    prompt again… If the dispatch says no key was received, use the key if
    present, else fall back to music-only/silent."
  - **dispatch-prompt.md — Environment field FIXED.** (`:28–30`): the
    field now documents "`ELEVENLABS_API_KEY=<value held in working
    context>` on a /demo dispatch when a narration key was received
    mid-build (orchestrate step 0 — only when the user asked for a demo
    video)".
  - **hackathon-pitch — MENTION.** Owns pitch narrative only; states
    explicitly "never the demo video itself (pitch-deck-video / /demo owns
    that)"; the only /demo references are length-canonical pointers.
  - **deploy-fast — MENTION.** "the demo VIDEO is filmed from local code
    only — never a deployed URL — see `pitch-deck-video`" (`:21`); all
    other "demo" hits are live-demo/presentation usage, not /demo.
  - **readme-writer — MENTION (conditional).** "take them from
    `.hackathon/run-ledger.md` (the deployed-URL line; the video path is
    `<app-name>-video/out/demo.mp4`) — when the ledger names them, write
    the real links, never a placeholder" — a conditional read, not an
    invocation.
  - **feature-expansion, fastapi-patterns — MENTIONS.** Generic "demo"
    (demo impact scoring, dev/demo environments); no `/demo` or
    pitch-deck-video invocation.
  - **orch-pipeline, gan-build, devpost-autofiller, orch-add-feature,
    orch-fix-defect, orch-refine-code (+ commands), agents/ — NO
    REFERENCES** to `/demo` or pitch-deck-video.
  - **plugin.json / README — MENTIONS.** Command-listing text only.

### (c) CONTRACT INTACT — PASS (from the skill text; live film not run)
Verified each element from `skills/pitch-deck-video/SKILL.md` (read in
full, lines 1–830):
- **F1 feature coverage:** step 3 `features`/`cuts` arrays (a feature is
  'shown' only if visible on camera AND named); step 6 coverage table —
  "A feature whose beat id is missing… is a BLOCKING finding". Bang
  boundary: "motion graphics never replace feature coverage (F1)".
- **F2 stack labels:** step 4 `cards.arch.nodes` each with a `stack` label
  from `package.json` + decision record, "never invented"; narration names
  the stack in one spoken phrase.
- **F3 Edge at position 3:** the arc is Problem (1) → Wow (2) → Edge (3)
  → How (4) → Proof (5) → Close (6); Edge is "one beat, one sentence".
- **F4 theme pull + gorgeousness checks:** step 4 pulls `theme.colors`
  from the app's own tokens with `theme.source` recorded (QA fails the
  video if the theme is still the seed theme); step 6 Gorgeousness (a) no
  generic seed look, (b) best-looking states, (c) vignette matches.
- **F5 blocking A/V table + 10s mix listen:** step 6 per-beat A/V table —
  "A 'no' is a BLOCKING finding"; "Kinetic type and camera moves go IN
  this table as rows of their own"; Mix — "listen to a 10-second sample
  from the middle of the video… record the check"; `music.gain.under` >
  0.20 warns.
- **F6 measured runtime under 2:10 / absolute max 2:30:** step 4 "the
  video is under 2:10 (130 seconds) — hard rule… computed from the
  MEASURED narration durations… Absolute max 2:30 (150 seconds), never
  exceeded — no approval, no exception"; section budget table (features
  the largest share, 55–65s); step 6 Runtime — "over 2:10 is BLOCKING…
  2:30 is the absolute ceiling". Bang opener "is a beat inside the
  130-second cap, never extra runtime (F6)".
- **Voice rules:** Voice preflight (ElevenLabs → Piper → `say` → MiniMax
  chain, per-line fallback, never aborts), voice direction (default Rachel,
  sample-one-line-before-batch), narration-key prompt (ask once, never
  block; keys env-only, never in a file).
- **$10 budget cap:** Budget governance — "Default cap: $10 per video.
  First paid use of a new provider needs approval even under the cap…
  any single paid action estimated above $0.50 pauses for approval…
  Keep 10% of the cap back for retries"; OpenMontage pipeline defaults
  lower ($1/$2) also bind.
- **Local-only filming:** "Which app gets filmed — local only" — `app.url`
  is the local dev-server URL, "Never set it to a deployed URL, and never
  film a deployed product"; `APP_DIR` auto-starts the local app.
- **§12 port did not change the contract:** anti-slide rules are BLOCKING
  QA checks (step 6, "A 'no' on any check is BLOCKING: re-cut the
  composition, never ship a slide deck with fades"); one-world/camera/
  persistent-subject architecture governs the opener/Edge/close and the
  moves between filmed beats, not the footage; style-direction (10) and
  opener-concept (19) menus are menu-not-defaults with theme/brand reasons
  required; kinetic typography is §10 directives with A/V-table rows;
  explainer styles (6) inform How-beat motion only, "not a second output
  format"; pin SHA `c1aa65e9…`, GSAP 3.15.1 convergence, scoped Three.js
  pins, staleness + language notes all recorded.
- **Limit (stated explicitly):** this is a text-verification verdict. No
  live film was rendered in this audit (read-only), so the contract is
  verified as written, not as executed. Dry-run #37's live /demo evidence
  is from the prior build (see §8a).

## 9. less-flat-ui diff — exactly 6 hunks; global source NOT edited

- `diff -u ~/workspace/cursor-skills/less-flat-ui/SKILL.md
  hackathon-ecc/skills/less-flat-ui/SKILL.md` = **6 `@@` hunks**: 4 Batch E
  (design-decision pointer insert; wow-moment line; record-treatments
  line; re-tint line) + 2 fix22 (DEPTH-13 at the Soft Shadow section;
  L15-06 liquid-glass insert before "### 3. Thermal gradients").
- Global source contains **0** `F22` markers; the plugin-scoped notes live
  only in the built copy via the runtime block — DEPTH-13 at build.sh
  `:23714`, L15-06 at `:23722`.

## 10. Verifiers, open items, and recorded tensions (not findings)

- **verify22.py: 368/368 PASS, exit 0** (re-run by this audit). Prior
  verifiers re-run by this audit, failing ONLY the frozen post-fix21
  build.sh fingerprint lines, exactly as the task stated: verify15 42/44,
  verify17 58/60, verify18 69/72, verify19 71/76, verify20 164/169,
  verify21 96/102 (fingerprint legitimately superseded by fix #22:
  23,773 lines / md5 `e9462b57…`).
- **Open items (coordinator steps, not audit findings — same treatment as
  Audit #68):**
  1. `fix22/MANIFEST.md` **not yet written** (absent at audit time; the
     manifest must record the B-1 behavior change, the refreshed
     disposition line numbers per §1, and the RareFormLabs sentence per
     §4). This absence is also the substance of M-2 — writing the manifest
     closes M-2 with no rule-text change.
  2. **Sweep #30b not re-run against this build** — no new sweep report
     exists; the weaving-coherence pass for the DEMOGATE edits is therefore
     not yet evidenced by a sweep (this audit's §7 spot-checks are not a
     substitute for the sweep).
  3. **Dry-run #37 not re-run against this build** — its report PASSes on
     the prior build (23,758); the only template change since is the
     remotion-CLI fix (§8a), which needs a live `qa.mjs` run to confirm
     end-to-end.
  4. **Close criteria not yet met:** per parent-addendum §4, close needs
     Audit #68 ZERO + dry-run #37 PASS + sweep CLEAN + verify22 100% +
     prior verifiers + banned terms 0 + build clean + MANIFEST written.
     This audit is NOT zero (2 minor), so the fix cannot close on this
     audit regardless of items 1–3.
- **Observations (recorded, not findings — no action required for ZERO
  except where noted):**
  1. hackathon-mode §7's narration-key paragraph does not restate the
     "only when the user asked for a demo video" condition — but it defers
     explicitly to "orchestrate step 0", which IS conditional, and §1:12
     states the condition. A one-line restatement in §7 would make the
     rule robust to being read alone; not counted as a finding because the
     operative text is conditional and cross-referenced.
  2. orch-build-mvp's narration-key preamble still says "Do NOT re-prompt
     at step 8 `/demo` time" and "Key handoff to step 8" — step 8 no
     longer films by default. The preamble's own condition ("if narration
     will need a key") only fires when a video was requested, and it
     dispatches nothing, so it is not an auto-invocation; the "step-8
     /demo" phrasing is stale cross-reference wording, worth a touch-up
     alongside the next edit, not a finding.
  3. The disposition's cited line numbers are stale for ~51 rows (§1) —
     refresh when the manifest is written.
- **Recorded tensions (recorded, not findings — parent adjudication
  still open):** B3 30ms vs Rule 5's 0.05s floor; B15 0.8× vs
  quick-reference ~60–70%; B4 0.97 vs `scale.press` 0.95 (flags carried in
  motion-foundations `:405`, `:431`, `:328`); C13 eyebrows vs the
  Impeccable craft-floor ban (stricter rule applied, slop-checklist
  `:271–290`); orbs "thinking" correction + pin 0.3.2 vs repo 0.3.1
  (§4); Vercel AG19 (§6); GSAP 3.15.1 convergence + scoped Three.js pins
  (Vanta 0.134.0 / general 0.185.1 / Bang 0.161.0 recorded-only); Bang
  staleness + Indonesian-language note; GSAP GreenSock Standard (NOT MIT)
  + React Bits MIT + Commons Clause licence deviations.

## Overall verdict

**AUDIT #68 RE-RUN: NOT ZERO — 0 BLOCKING, 2 MINOR (M-1, M-2).**

Everything else audited is clean: the §1–§17 weave, all pins/licenses/
scopes, D19 form, orbs, Vercel snapshot, less-flat-ui diff, counts,
banned terms (0), Grok pins, screen-verdicts rule, the /demo (a) wiring
and (c) contract-as-written, and — the point of this re-run — the /demo (b)
NOT-AUTOMATIC gate: B-1 (orchestrate 5d + hackathon-mode mandate), B-2
(orch-build-mvp step 8), and B-3 (orch-change-feature re-film) are all
verified removed with full-context reads, the B-3 removal (not exception)
decision is honored verbatim in the skill text, the dry-run #37 template
defect is fixed in both scripts, and sweep #30b Finding 2 is fixed. The
coordinator's next steps: fix M-1 (one parenthetical in hackathon-mode
§3), write `fix22/MANIFEST.md` (closing M-2), then re-run sweep #30b +
dry-run #37 against this build and a fresh audit for ZERO.
