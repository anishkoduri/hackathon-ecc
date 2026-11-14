# Audit #69 (fix #22, new build)

**Date:** Nov 13, 2026 (audit run Nov 13 CST)
**Auditor:** Audit #69 worker (check only — no plugin file edited, build.sh not
run, fix22.py / apply22.py / verify22.py not run or edited, nothing
bundled/committed/pushed, no message sent to anyone)
**Built tree:** `~/workspace/hackathon-plugin/hackathon-ecc/`
**Build state measured by this audit:** build.sh **23,774 lines, md5
`4799a819791b9c3ec4c19136ad698397`** (matches the task statement). Diff vs the
pre-fix22 backup `build.sh.before-fix22` (23,647 lines): **+127 lines, 0
deletions, exactly 2 hunks** (`41a42,46` BANG_PIN block; `23635a23641,23762`
fix22 block). Diff vs the Audit #68 re-run build (23,773 lines, md5
`e9462b57429acd914cd0aacdebc486d0`): **+1 line** — the DEMOGATE_B2S7 runtime
patch line in build.sh (`:23748`).
**Verifiers re-run by this audit:** `fix22/verify22.py` **368/368 PASS**
(exit 0, run directly); prior verifiers match the allowed-fail pattern
exactly (see §5). All counts below were re-derived independently (own greps /
own Python / own full-file reads), not copied from verifier output or from
the Audit #68 re-run / sweep #30b re-run reports — every changed site was
re-read in full context against the new build.

**Method note:** every file named in the /demo gate (§4b) was read IN FULL
(orchestrate SKILL.md lines 56, 58, 80, 82, 327, 344; orch-build-mvp SKILL.md
lines 32, 83, 84; orch-change-feature SKILL.md lines 51, 52, 54; hackathon-mode
§1/§3/§7 in full; commands/demo.md in full; dispatch-prompt.md Environment
field; hackathon-pitch, deploy-fast, readme-writer, feature-expansion,
fastapi-patterns `/demo` mentions with context; commands/orch-build-mvp.md:36
and commands/orch-change-feature.md:25; pitch-deck-video SKILL.md lines
1–830 spot-read for F1–F6 + the full Bang section). The /demo verdicts rest
on those full-context reads, not on grep snippets.

## Verdict: AUDIT #69: ZERO — 0 BLOCKING, 0 MINOR

All five items that changed since the Audit #68 re-run are verified fixed
(§0). The §1–§17 weave is clean (§§1–3), the /demo (a) callable / (b) never
automatic / (c) contract-intact gates all pass (§4), verify22 is 368/368 and
the prior verifiers match the allowed-fail pattern (§5), and the
behavior-change record is consistent everywhere (§6). No blocking and no
minor findings.

## BLOCKING findings

None.

## MINOR findings

None.

## 0. What changed since the Audit #68 re-run — all five verified FIXED

### 0.1 M-1 fixed — hackathon-mode §3 now reads "(after deploy, commit, and README)"
- **File:** `hackathon-ecc/rules/hackathon-mode.mdc:22`
- **Current text (quoted verbatim):** "The one permitted invocation is the
  named end-of-project run immediately before the first build's final report
  (after deploy, commit, and README): that run IS the very end of the
  project — it runs once, it never gates a feature, and it never fires
  mid-build or during a one-prompt removal."
- **Tree-wide check:** `after deploy, demo` **0**; `deploy, demo` **0**;
  `deploy → demo` **0**; `demo → commit` **0**; `demo, commit` **0**.
  `deploy/demo` occurs **1×** only — `hackathon-ecc/README.md:40`,
  "deploy/demo/orchestration workflows" — the capability phrase the task
  records as acceptable, not a sequence. `after deploy, commit` occurs 2×:
  hackathon-mode `:22` (this fix) and orchestrate SKILL.md `:84`
  ("After deploy, commit, and README, run the six deferred checks").
  No sequence anywhere in the built tree still lists demo as a first-build
  pipeline step.

### 0.2 M-2 / manifest — `fix22/MANIFEST.md` STILL unwritten (known open close step, NOT a finding this round)
- `ls fix22/MANIFEST.md` → "No such file or directory" (confirmed by this
  audit). Per the task, its absence is **not** flagged as a finding this
  round; it is recorded here as the known open close step (§7.1). The
  hackathon-mode `:68` sentence ("the behavior change is recorded in
  `fix22/MANIFEST.md`") therefore still points at a record that does not
  exist yet — the same premature-pointer wording the Audit #68 re-run
  recorded as M-2 — but the task explicitly defers that finding to the
  manifest write, and this audit follows the task: the sentence becomes true
  when the coordinator writes the manifest after this audit returns ZERO.
  No rule text was changed to work around it.

### 0.3 Sweep Finding 1 (blocking) fixed — Remotion invocation is now the `-p` form at both call sites
- **Built tree:**
  - `hackathon-ecc/skills/pitch-deck-video/template/scripts/build.mjs:335`:
    `run('npx', ['-p', '@remotion/cli@4.0.526', 'remotion', 'render',
    'src/index.ts', 'Demo', 'out/demo.mp4', …`
  - `hackathon-ecc/skills/pitch-deck-video/template/scripts/qa.mjs:42`:
    `execFileSync('npx', ['-p', '@remotion/cli@4.0.526', 'remotion',
    'still', 'src/index.ts', 'Demo', file, `--frame=${p.frame}`,
    '--log=error'], { …`
- **Verified:** 0 bare `npx @remotion/cli@4.0.526` invocations in the built
  tree, staged sources, and build.sh; 0 `remotion@4.0.542` anywhere in the
  built tree, staged sources, or build.sh; template `package.json:15` pins
  `@remotion/cli: 4.0.526` (with `remotion: 4.0.526` at `:21`), so the
  scripts match the pin. The staged template is byte-identical to the built
  template (`diff -r` clean), so staged and built carry the same fixed form.
- **Live corroboration (not run by this audit — see §4.4):** the dry-run
  #37 re-run #2 logs (`fix22/dryrun37-rerun2/`, run Nov 13 02:09–02:13,
  after this build) show `qa.mjs` executing exactly
  `npx -p @remotion/cli@4.0.526 remotion still …` — no "could not determine
  executable to run" error; Remotion bundled 100% and opened its browser.
  The invocation-form defect is fixed live, not just textually. The
  remaining `qa.mjs` failure in that log is a sandbox Google Fonts fetch
  (`fonts.gstatic.com` SSL errors), an environment limitation, not the
  invocation (§4.4).

### 0.4 Sweep Finding 2 (minor) fixed — orch-build-mvp narration-key paragraph is now conditioned on the user having asked for a video
- **File:** `hackathon-ecc/skills/orch-build-mvp/SKILL.md:32` (2,106-char
  line, read in full; DEMOGATE_B2S7_F22 at char 2088, end of the line)
- **Current text (quoted verbatim, opening):** "**Narration-key prompt —
  once, at the start of the standalone run, never blocking.** At the start
  of the run (step 1), if the user asked for a demo video and narration
  will need a key and none is set (no `ELEVENLABS_API_KEY` in the
  environment, no MiniMax credentials), issue the single `pitch-deck-video`
  narration-key prompt once. If the user did NOT ask for a demo video, do
  NOT send this prompt — no video is being built, so no key is needed …"
- **Stale references gone:** "step 8" / "step-8" occur **0×** in `:32`
  (previously "Do NOT re-prompt at step 8 `/demo` time" / "Key handoff to
  step 8"). The replacements: "Do NOT re-prompt at `/demo` time: the single
  early prompt covers the run, and a user-invoked `/demo` uses the key if
  present, else falls back to music-only/silent." / "**Key handoff to a
  user-invoked `/demo`:** if the user replies with a key mid-run, hold it
  in working context ONLY and pass it to `/demo` via the dispatch if the
  user asks for a video …". "user-invoked `/demo`" occurs 3× in the
  paragraph; the late-key re-run clause is conditioned on "the user-invoked
  `/demo` already rendered". No stale "step-8 /demo" dispatch remains
  anywhere in the paragraph, and a grep for `step 8 /demo|step-8 /demo`
  over the built tree returns 0.

### 0.5 Audit observation fixed — hackathon-mode §7 narration-key paragraph now states the condition
- **File:** `hackathon-ecc/rules/hackathon-mode.mdc:59` (the §7 narration-key
  paragraph, read in full)
- **Current text (quoted verbatim, relevant clauses):** "The narration-key
  prompt is the ONE sanctioned user prompt during the first build besides
  grill-me itself; it never blocks the build. **Scheduled here, sent by
  orchestrate:** orchestrate sends it immediately after grill-me, before
  scoping (orchestrate step 0) — only when the user asked for a demo video;
  on the grilled path and on the skip-grilling path … alike, at the start of
  the build either way. If the user did NOT ask for a demo video, do NOT
  send this prompt — no video is being built, so no key is needed. … If no
  key ever arrives, a requested /demo renders music-only/silent with a note
  in the final report — no second ask, no stall."
- The paragraph now states the condition itself ("only when the user asked
  for a demo video" + "If the user did NOT ask … do NOT send this prompt")
  and the no-key fallback applies to "a requested /demo". It no longer
  relies solely on the cross-reference to orchestrate step 0.

## 1. SPEC compliance §1–§17 — all placed

- **144-item disposition:** an independent script parsed
  `fix22/disposition-merged.md` — **142 A–G rows + H1 + H2 rows** (`:151–152`)
  + 4 process rows (Mobbin §9, Directives §10, Libraries §11, Bang §12).
  Every A–G row's home file contains the item's distinctive name words
  (**0 content fails** out of 142 by that check); H1 content verified
  ("accent colour" 12× in ui-ux-pro-max, sprawl check in slop-checklist,
  D11 points at it) and H2 verified ("Accent hierarchy" in orchestrate
  step 3, hierarchy rules in ui-ux-pro-max, hierarchy check in
  slop-checklist). verify22's string checks (368/368) assert the same
  placements independently. The disposition's cited line numbers are stale
  for ~51–64 rows (mechanical drift from the §13–§17 follow-up and the
  DEMOGATE edits — e.g. A13–A20 cited `:217–281`, now `:312–376`; H1 cited
  ui-ux-pro-max `:122` vs the concept now spanning `:15–40` with the
  `:122` pin record) — a documentation staleness note, not a finding; the
  disposition header is frozen at the Audit #67 build and is to be
  refreshed when the manifest is written.
- **§13 depth:** orchestrate step 3 names the depth strategy per surface
  (`:66`, incl. explicit "flat by choice — <reason>"); ui-ux-pro-max depth
  rules; motion-foundations depth tokens; motion-patterns 3D patterns;
  Taste depth-as-dealt-moment; polish-pass depth check (`:101`,
  slop-checklist depth section). Cross-refs to A11 / Bang camera / Vanta /
  GSAP 3D present, no duplication.
- **§14 orbs:** nine states, no "thinking" state — see §3.
- **§15/§17 libraries:** pins + licenses + stack scope as specified —
  see §3.
- **§16 Vercel:** pinned snapshot + no live fetch + dedupe 136 — see §3.
- **Process additions (§9 Mobbin, §10 directives, §11 libraries, §12 Bang):**
  all present with their boundaries. Mobbin research step orchestrate `:64`
  (MOBBIN_RESEARCH_F22, quoted in §3); pattern refs Taste `:445` +
  ui-ux-pro-max `:167`; QA check polish-pass `:106`; DIRECTIVES_F22 in all
  8 required locations (re-counted 8 occurrences in the built tree:
  orchestrate, Taste ×2, ui-ux-pro-max, GAN planner/generator/evaluator,
  polish-pass).

## 2. Standing rules — no regressions

- **Banned terms 0 in the built tree.** Own case-insensitive grep over the
  built tree (`--exclude-dir=node_modules`) for
  `claude|codex|anthropic|opus|sonnet|haiku|composer-2.5` returns 0 lines.
  verify22 agrees.
- **Grok pins only.** Tree-wide occurrence counts (excl. node_modules):
  `grok-4.7-high` **54**, `cursor-grok-4.6-high-fast` **102**, bare
  `grok-4.6-high-fast` (proper negative-lookbehind grep) **0** — identical
  to Audit #67/#68's counts.
- **Font rules (fix #19/#20/#21) untouched.** verify19's font anchors pass
  (see §5); F4 Tiempos/Fraunces body-only and F7 per-element font decisions
  present in orchestrate + Taste; static instances only.
- **Screen-verdicts rule intact.** `browser-qa` remains the sole verdict
  executor: slop checklist, unslop fixes, Vercel checklist, and depth check
  are all worded as static checks / candidate evidence, never verdicts
  (polish-pass `:98–99`, Taste finish-gate `:497`).
- **No new skill / command / trigger key.** Counts re-derived from the built
  directories: **166 skills / 72 agents / 123 rules / 87 commands**;
  hooks.json defines **15** hook events. Trigger keys **64**
  (`hackathon-ecc/manifests/context-packs/skill-triggers@1.json` `triggers`
  dict, 64 keys); after stripping the `skill:` prefix every key resolves
  to a real skill dir (0 unresolvable).
- **Anchor spot counts** (built tree, excl. node_modules; occurrence
  counts, matching the sweep #30b re-run table exactly): SLOP_F22 28,
  UNSLOP_F22 16, TRENDS_F22 53, DIRECTIVES_F22 8, DEPTH_F22 35, ORBS_F22 24,
  VERCEL_F22 8, ACCENT_F22 11, ACCENTUATION_F22 6, MOBBIN_RESEARCH_F22 1,
  MOBBIN_PATTERN_F22 2, MOBBIN_QA_F22 1, BANG_ANTISLIDE_F22 1,
  BANG_ONEWORLD_F22 1, BANG_STYLES_F22 1, BANG_OPENERS_F22 1,
  BANG_KINETIC_F22 1, BANG_EXPLAINER_F22 1, LENIS_F22 4, GSAP_F22 2,
  SCROLLTRIGGER_F22 4, VANTA_F22 10, REACTBITS_F22 5, R3F_F22 11,
  LIQGLASS_F22 6, SHADERGRAD_F22 7, LIQLOGO_F22 6, WEBGL_ONE_F22 9,
  CASBERRY_F22 5, ORIGINKIT_F22 3, DAISYUI_F22 3, PRINCIPLES_F22 5,
  LAWS_F22 4, ANIM_TOKENS_F22 1, ANIM_RULES_F22 1, ANIM_ADV_F22 1,
  GLOSSARY_F22 5. No orphaned anchor found in the spot-checks.
- **D19 six-dimension reasons on every new rule** (spot-checked in the slop
  intro, unslop intro, token groups, Mobbin QA check, library scope blocks,
  Bang menus, orb + depth sections — each dimension a reason or explicit
  `none — <reason>`).
- **Theme-match precondition everywhere** (principles, tokens, slop/unslop
  intros, trends intro, library scope blocks, Mobbin QA, Bang menus).

## 3. §13 D19 form, §14 orbs, §15/§17 libraries, §16 Vercel — verified

### 3.1 §13 D19 form — byte-identical, extension separate
- D19 rule line byte-identical: orchestrate SKILL.md `:120` ==
  design-taste-frontend SKILL.md `:423` (2,090 chars each, compared by
  Python `==`).
- Extension line byte-identical: orchestrate `:122` == Taste `:425`
  (923 chars each, exact).
- The extension line is separate and immediately after the rule (blank line
  between, `:121`/`:424` empty in both files). No "six dimensions" text was
  rewritten.

### 3.2 §14 Thinking Orbs — verified
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
- **RareFormLabs:** orbs-patches.md `:522` records verbatim
  "rareformlabs connection unresolved — asset verified independently" and
  no patch text mentions RareFormLabs. `rareformlabs` occurs 0× in the
  built tree. The manifest half of that requirement is pending only because
  `fix22/MANIFEST.md` does not yet exist (§0.2, §7.1).

### 3.3 §15/§17 libraries — verified (spot-checked pins/licenses/scopes)
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
  reviewed as untrusted code, motion-patterns `:893`); OriginKit ("10
  component fetches per key per day", ui-ux-pro-max `:516`; Origin UI
  distinction, motion-patterns `:858–860`; conditional/source-available
  licence, redistribution restriction); daisyUI (`daisyui@5.7.50`, MIT,
  Tailwind v4 ONLY pairing, default-theme-unexamined FAILS, design-system
  `:37–50`, ui-ux-pro-max `:501–514`).
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

### 3.4 §16 Vercel — verified
- **Pinned snapshot:** `skills/polish-pass/reference/vercel-checklist.md`
  (453 lines by `wc -l`, VERCEL_F22 anchor `:1,3`), source
  `vercel-labs/web-interface-guidelines`, file `command.md`, commit
  `4ecfb9fb8d1d3b7009674869b3aaee2f904042e1`, dated 2026-10-05 (`:16`).
  (Note: Python `splitlines()` counts 454 — a trailing-newline counting
  artifact, not a content change; `wc -l` = 453, matching the Audit #68
  re-run.)
- **NO live-fetch instruction:** grep for
  `raw.githubusercontent.com/vercel-labs` over the whole built tree
  (excl. node_modules) returns **0**. The only two
  `raw.githubusercontent.com` hits in the tree are pre-existing
  codebase-memory install URLs (`DeusData/codebase-memory-mcp/v0.12.1`,
  pinned) — unrelated to Vercel. The checklist states "This file holds the
  rules. It never fetches anything" and names the upstream live-fetch form
  a flagged prompt-injection hazard that is "NEVER the weave".
- **Dedupe 136 rows:** independently re-derived by rule-id parse of
  `fix22/vercel-dedupe.md` — **136 unique rule ids**, dispositions:
  already-covered 14, partial 38, new 70, duplicate-of 13, **conflict 1
  (AG19)** = 136, **0 unaccounted**.
- **AG19 conflict recorded:** vercel-dedupe.md `:262` — APCA vs WCAG 4.5:1,
  "**conflict — parent adjudication**… Until then, WCAG 4.5:1 stands and
  APCA is not woven." Sole conflict.
- **License gap recorded:** rules repo ships an MIT LICENSE (© 2025 Vercel
  Labs); skill repo has NO LICENSE file, README states MIT only; "no
  skill-repo text is copied here".
- **ECC-source check recorded:** ECC snapshot dated 2026-09-21 used as the
  form; the plugin's ECC source at its pin does NOT carry the skill, so the
  rules were ported from the rules repo at the pinned commit.
- **Sweep #30b Finding 2 still fixed:** `40x40px` occurs **0** times in
  the built tree and **0** times in `vercel-dedupe.md`; the live rule is
  "44x44px minimum (the plugin floor)".
- **Wiring:** polish-pass SKILL.md `:98–99` runs the Vercel checklist on
  every pass with the same standing as the slop checklist (candidate
  evidence, never verdicts; cleared only by a recorded D19 reason +
  theme-fit).

### 3.5 Weaving spot-checks (own, not copied from sweep #30b re-run)
- **C:** slop-checklist carries all 20 indicators (distinct C1–C20
  verified); **D:** unslop-fixes carries all 20 fixes (distinct D1–D20
  verified); **E:** Taste carries TRENDS_F22 23× (20 entries + intro ×2 +
  finish-gate pointer); **G:** glossary
  `design-taste-frontend/references/design-glossary.md` carries 20 terms
  (20 table rows); **H1/H2:** see §1; **§9 Mobbin:** orchestrate `:64`
  research step quoted verbatim — "before the direction is generated
  through the design package skills, a named research step consults the
  Mobbin pattern library (mobbin.com) for the build's pattern categories …
  consultation is at CATEGORY + PATTERN level …, never a specific app's
  screen. The decision record notes which categories were consulted. …
  Mobbin … NEVER supplies the design direction, and the generating skill is
  always the recorded source in `docs/design-tokens.md`, never a Mobbin
  URL. A build that cites a Mobbin screen as its design source FAILS the
  check." Free tier + never-blocked recorded in the same paragraph.
  **§10:** DIRECTIVES_F22 8× in the 8 required locations (§1).
  No item found only-appended in these spot-checks.

### 3.6 less-flat-ui diff — exactly 6 hunks; global source NOT edited
- `diff -u ~/workspace/cursor-skills/less-flat-ui/SKILL.md
  hackathon-ecc/skills/less-flat-ui/SKILL.md` = **6 `@@` hunks**: 4 Batch E
  (design-decision pointer insert; wow-moment line; record-treatments
  line; re-tint line) + 2 fix22 (DEPTH-13 at the Soft Shadow section;
  L15-06 liquid-glass insert before "### 3. Thermal gradients").
- Global source contains **0** `F22` markers; the plugin-scoped notes live
  only in the built copy via the runtime block.

## 4. /demo gates — verdicts

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
  pipeline (0 `from`/`import`/`require` of liquid-logo in pitch-deck-video;
  "liquid-logo" occurs 0× in the pitch-deck-video skill itself). The Bang
  port did not change this.
- **Remotion invocation (sweep Finding 1 — FIXED, §0.3):** template
  `scripts/build.mjs:335` and `scripts/qa.mjs:42` now call
  `npx -p @remotion/cli@4.0.526 remotion <cmd>` in the built tree AND the
  staged source. `remotion@4.0.542` occurs **0** times in the built tree,
  staged sources, and build.sh. Template `package.json:15` pins
  `@remotion/cli: 4.0.526` (with `remotion: 4.0.526` at `:21`), so the
  scripts match the pin.
- **What was NOT verified by this audit (stated explicitly, per the task):**
  no live /demo execution was run in this audit — this audit is read-only
  (no build.sh runs, no filming). So callability is established by wiring
  (command file + frontmatter + command-list reachability + skill
  invocation path + staged==built), NOT by a live film on this build by
  this audit. Corroborating live evidence from the dry-run #37 re-run #2
  (not this audit's work) is recorded in §4.4 — it does not change the
  limit on this audit's own verdict.

### (b) NOT AUTOMATIC — PASS (all prior auto-invocations still removed; the two stale-wording minors still fixed)
- Grep-verify: hooks contain zero "demo" hits (`hooks/hooks.json` 0;
  all hook `.js` files 0) — no hook invokes /demo. No post-build trigger
  or finish-report step invokes /demo (the end-of-project checks run the
  six deferred audits, not /demo). All **20 DEMOGATE tokens occur exactly
  once** in the built tree (re-counted by this audit):
  DEMOGATE_O4_F22 1, O9 1, B2S1–B2S7 1 each (7), B2C1 1, B3S1–B3S7 1 each
  (7), B3C1 1, H1 1, H2 1 — 20 distinct, sum 20. (The 20th token vs the
  sweep's 19 is DEMOGATE_B2S7_F22, the new orch-build-mvp narration-key
  patch at SKILL.md `:32`, §0.4.)
- Full-context reads of every pitch-deck-video referencer:

  - **orchestrate — gate present.** Step 5d (`:80`): "**Demo — never
    automatic (fix #22 /demo gate, DEMOGATE_O4_F22).** `/demo`
    (`pitch-deck-video`) is NEVER dispatched by this pipeline. It runs ONLY
    when the user invokes `/demo` explicitly (or the user's request
    explicitly asks for a demo video). … If no video was requested, the
    final report notes that no demo video was filmed." Sequence (`:56`):
    "… → verify → polish → deploy → README → final report). /demo is never
    part of this sequence — it runs ONLY when the user invokes it
    explicitly". Step 0 (`:58`) conditional (quoted §0.5 pattern; same
    form). Step 6 (`:82`) Order sentence: "verify → polish → deploy →
    commit → README → final report. (A demo video is filmed only when the
    user invokes `/demo` explicitly — it is never part of this order…)"
    Final report (`:327`, `:344`): sequence without demo; demo-video handoff
    "(only if a video was filmed)".
  - **orch-build-mvp — gate present, narration paragraph fixed.** Skill
    step 8 (`:83`): "**Demo — never automatic (… DEMOGATE_B2S1_F22).**
    `/demo` is not filmed here. … Do NOT film via `/demo` here — `/demo`
    runs ONLY when the user invokes it explicitly … If no video was
    requested, the final report notes that no demo video was filmed."
    Step 9 (`:84`) carve-out timing "after deploy/commit/README"
    (DEMOGATE_B2S6_F22). Command step 8 (`:36`): "Do NOT film via `/demo`
    here — `/demo` runs ONLY when the user invokes it explicitly (or the
    user's request explicitly asks for a demo video); if the user asked for
    one, film the LOCAL app from the project dir only, never a deployed
    URL… (… DEMOGATE_B2C1_F22)". Narration-key paragraph (`:32`) fixed
    per §0.4. The "required deliverable" language is gone from both files.
  - **orch-change-feature — gate present, removal re-film REMOVED (not
    carved out as an exception).** Skill step 5 (`:51`): "…before any future
    re-film, update `shots.json` FIRST … **If the user asks for a re-film,
    re-film via `/demo --rebuild`**, which films the LOCAL app from the
    project dir (`APP_DIR`/project root), never a deployed URL…
    (DEMOGATE_B3S1_F22)". "(The poll verifies the redeploy; it is not a
    prelude to filming — no re-film happens here.)" Done-condition:
    "satisfied by the re-filmed LOCAL video (if the user asked for a
    re-film) + the honest hosting note, or by the stale-video record when
    no re-film was requested — never by a phantom upload, never by an
    automatic re-film. (… DEMOGATE_B3S5_F22)". Step 6 (`:52`) reports
    "demo video STALE — shows the removed feature; re-film with
    `/demo --rebuild` on request" (DEMOGATE_B3S7_F22). Command (`:25`):
    "re-film with `/demo --rebuild` only when the user asks"
    (DEMOGATE_B3C1_F22). Skill `:54` is a definitional note (`/demo` vs
    `/demo --rebuild` on an existing video project), not an invocation.
  - **hackathon-mode.mdc — mandate removed.** §1 (`:12`): first-build
    sequence ends "… → verify → polish → deploy → README → final report…
    /demo is never part of this sequence — it runs ONLY when the user
    invokes it explicitly (… DEMOGATE_H2_F22)". §3 (`:22`): carve-out
    timing fixed per §0.1. §7 (`:68`): "The first build does NOT film
    `/demo` automatically (… DEMOGATE_H1_F22). `/demo` … runs ONLY when the
    user invokes it explicitly … never as a pipeline step, never by
    default. … Then the README is written and the final report is delivered
    (deploy → README → final report). The demo video is no longer a required
    deliverable of the first build — the behavior change is recorded in
    `fix22/MANIFEST.md`." (§7's narration-key paragraph fixed per §0.5;
    the MANIFEST pointer is the known open step, §0.2.)
  - **commands/demo.md — dispatch note fixed.** The old note ("If this
    /demo run was dispatched by orchestrate (step 5d) or orch-build-mvp
    (step 8), do NOT prompt") is gone. The new text (`:13`): "If this /demo
    run was invoked with a narration key already provided (via the
    dispatch's Environment field as an `ELEVENLABS_API_KEY` env
    instruction), do NOT prompt again… If the dispatch says no key was
    received, use the key if present, else fall back to music-only/silent."
  - **dispatch-prompt.md — Environment field fixed.** (`:28–31`): the
    field documents "`ELEVENLABS_API_KEY=<value held in working
    context>` on a /demo dispatch when a narration key was received
    mid-build (orchestrate step 0 — only when the user asked for a demo
    video)".
  - **hackathon-pitch — MENTION.** Owns pitch narrative only; states
    explicitly "never the demo video itself (pitch-deck-video / /demo owns
    that)"; the only /demo references are length-canonical pointers (`:3`,
    `:32`).
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
    REFERENCES** to `/demo` or pitch-deck-video (grep over the built tree
    returns only the files listed above, plus README/plugin.json
    command-listing text and the pitch-deck-video skill's own files).
  - **"required deliverable"** occurs 2× in the built tree: hackathon-mode
    `:68` (the H-1 negation, "no longer a required deliverable") and
    `pitch-deck-video/template/src/Video.tsx:15`, a pre-existing template
    comment ("Audio guards — the video is a required deliverable and must
    NEVER abort on a missing audio file") — staged source byte-identical,
    predates fix #22, describes the video's own audio guards once /demo
    runs, not a pipeline invocation. Checked and cleared, not a finding.
  - **"filmed by default"** 0×; **"Film via `/demo`"** as an instruction
    0× (the only "Do NOT film via `/demo`" hits are the two gates above).

### (c) CONTRACT INTACT — PASS (from the skill text; live film not run by this audit)
Verified from `skills/pitch-deck-video/SKILL.md` (830 lines, read in full
for the contract sections):
- **F1 feature coverage:** step 3 `features`/`cuts` arrays; step 6 coverage
  table — "A feature whose beat id is missing… is a BLOCKING finding".
  Bang boundary: "motion graphics never replace feature coverage (F1)".
- **F2 stack labels:** step 4 `cards.arch.nodes` each with a `stack` label
  from `package.json` + decision record, "never invented"; narration names
  the stack in one spoken phrase.
- **F3 Edge at position 3:** the arc is Problem (1) → Wow (2) → Edge (3)
  → How (4) → Proof (5) → Close (6); budget table lists Edge third
  ("| Edge (uniqueness) | 1 | 8–10 |"); Edge is "one beat, one sentence".
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
  moves between filmed beats, not the footage; style-direction menu (10
  directions, incl. "Cinematic dark") and opener-concept menu (19) are
  menu-not-defaults with theme/brand reasons required; kinetic typography
  is §10 directives with A/V-table rows; explainer styles (6) inform
  How-beat motion only, "not a second output format"; pin SHA `c1aa65e9…`,
  GSAP 3.12.5 Bang reference, scoped Three.js pins, staleness + language
  notes all recorded.
- **Limit (stated explicitly):** this is a text-verification verdict. No
  live film was rendered by this audit (read-only), so the contract is
  verified as written, not as executed. See §4.4 for the corroborating
  live evidence that exists from the dry-run re-run #2.

### 4.4 Dry-run #37 re-run #2 — corroborating live evidence on THIS build (not this audit's work)
`fix22/dryrun37-rerun2/` (timestamps Nov 13 02:09–02:13, after this build's
02:05 build.sh / 02:07 built-tree writes) has no formal report .md, but its
logs and output establish three facts about this build:
- **Fixtures 42/42 PASS** (`dryrun37-rerun2-output.txt`: "42/42 fixture
  expectations met", covering the §13–§17 and §8–§12 fixtures).
- **The `-p` invocation resolves live:** `qa-run.log` shows `qa.mjs`
  executing `npx -p @remotion/cli@4.0.526 remotion still src/index.ts Demo
  …/out/qa/00111_problem.png --frame=111 --log=error` with NO "could not
  determine executable to run" error; the Remotion probe log shows bundling
  reaching 100% and the bundled chrome-headless-shell browser opening.
  Sweep Finding 1 is therefore fixed live, not only textually.
- **Remaining live limits are environmental, not plugin defects:** `qa.mjs`
  exits 1 because the composition's Google Fonts fail to fetch in this
  sandbox (`fonts.gstatic.com` SSL errors → `TypeError Failed to fetch`
  from `@remotion/google-fonts` — the template's pre-existing font loading,
  not the invocation); `record.mjs` (filming) cannot start because no
  Playwright browser binary exists at
  `~/.cache/ms-playwright/chromium_headless_shell-1243/` ("Executable
  doesn't exist… Please run `npx playwright install`"). A full live film /
  stills render on this build is therefore still unverified in this
  environment. This audit records that limit; it is not an audit finding
  (the invocation defect it replaces is fixed, and the font/browser limits
  are the sandbox's, shared with all prior dry-runs).

## 5. Verifiers — PASS (allowed-fail pattern only)

- **verify22.py: 368/368 PASS, exit 0** (re-run by this audit, directly).
  Its tail also records the prior-verifier pattern and the not-yet-written
  MANIFEST note (lines=23774, md5=4799a819791b9c3ec4c19136ad698397).
- Prior verifiers re-run by this audit, each failing **only** on the frozen
  post-fix21 `build.sh` fingerprint (+ cascade lines, + the less-flat-ui
  diff check where applicable) — exactly the allowed pattern:

  | Verifier | Result | FAIL lines (exact) |
  |---|---|---|
  | fix15 | 42/44 | less-flat-ui diff (now 6 hunks, pre-fix22 expectation 4 — legitimately superseded by fix #22's 2 added hunks) + fingerprint |
  | fix17 | 58/60 | less-flat-ui diff + fingerprint |
  | fix18 | 69/72 | fingerprint + fix15/fix17 cascade lines |
  | fix19 | 71/76 | less-flat-ui diff + fingerprint + fix15/17/18 cascade lines |
  | fix20 | 164/169 | fingerprint + fix15/17/18/19 cascade lines |
  | fix21 | 96/102 | fingerprint + fix15/17/18/19/20 cascade lines |

  No other failure in any prior verifier.

## 6. Behavior-change record — consistent everywhere

- **First-build sequence is deploy → commit → README everywhere:**
  orchestrate step 6 (`:82`, "Order: verify → polish → deploy → commit →
  README → final report"), orchestrate `:84` ("After deploy, commit, and
  README, run the six deferred checks"), hackathon-mode §3 (`:22`, "after
  deploy, commit, and README"), hackathon-mode §7 exception ("it runs once,
  after deploy/commit/README"), orch-build-mvp step 9 (`:84`, same form).
  The README input is conditional everywhere ("if a video was filmed, the
  video file path … as inputs").
- **Demo no longer a required deliverable:** stated in hackathon-mode `:68`
  ("The demo video is no longer a required deliverable of the first
  build"), orchestrate `:80` ("If no video was requested, the final report
  notes that no demo video was filmed"), orch-build-mvp `:83` ("If no video
  was requested, the final report notes that no demo video was filmed"),
  and the `:344` handoff ("If no video was filmed … this handoff is
  omitted").
- **No leftover sequence lists demo as a pipeline step:** see §0.1
  (all old-sequence patterns 0×; the single `deploy/demo` hit is the
  README `:40` capability phrase, recorded as acceptable).
- The one forward reference to the behavior-change record is the
  hackathon-mode `:68` MANIFEST pointer (§0.2) — the record itself is the
  known open close step, not a finding this round.

## 7. Open items (coordinator / parent steps, NOT audit findings)

1. **`fix22/MANIFEST.md` not yet written** (SPEC §6.8). Per the task this
   is the known open close step, not a finding. When written it must record
   the B-1 behavior change (making the hackathon-mode `:68` pointer true
   with no rule-text change), the refreshed disposition line numbers (§1),
   the RareFormLabs sentence (§3.2), the §4a/§4b adjudication pairs, the
   token conflicts (B3/B15/B4), the C13-vs-Impeccable eyebrow tension, AG19,
   and the verifier + audit + dry-run + sweep results.
2. **Dry-run #37 formal re-run report not yet written for this build.**
   `fix22/dryrun37-rerun2/` exists with logs and a 42/42 fixture output
   (§4.4) but no report .md; its live evidence (invocation resolves;
   stills blocked on sandbox font fetch; filming blocked on the missing
   Playwright browser binary) is recorded in §4.4. A formal re-run report
   would close the loop on the close criteria.
3. **Sweep #30b not re-run against this build** — no new sweep report
   exists for the 23,774 build. This audit's §1/§3.5 spot-checks and §4
   full-context reads are not a substitute for the sweep's
   weaving-coherence pass; the sweep re-run is a coordinator step before
   close.
4. **Disposition line numbers stale** (~51–64 rows, §1) — refresh when the
   manifest is written.
5. **Recorded tensions (carried, not findings — parent adjudication
   still open):** B3 30ms vs Rule 5's 0.05s floor; B15 0.8× vs
   quick-reference ~60–70%; B4 0.97 vs `scale.press` 0.95 (flags carried in
   motion-foundations `:405`, `:431`, `:328`); C13 eyebrows vs the
   Impeccable craft-floor ban (stricter rule applied, slop-checklist
   `:271–290`); orbs "thinking" correction + pin 0.3.2 vs repo 0.3.1
   (§3.2); Vercel AG19 (§3.4); GSAP 3.15.1 convergence + scoped Three.js
   pins (Vanta 0.134.0 / general 0.185.1 / Bang 0.161.0 recorded-only); Bang
   staleness + Indonesian-language note; GSAP GreenSock Standard (NOT MIT)
   + React Bits MIT + Commons Clause licence deviations.

## Overall verdict

**AUDIT #69: ZERO — 0 BLOCKING, 0 MINOR.**

Everything audited is clean: the §1–§17 weave (144 items by content,
D19 byte-identical with the seventh-dimension extension separate, orbs
nine states with no "thinking" state, all §15/§17 pins/licenses/scopes,
Vercel pinned snapshot commit `4ecfb9fb` 2026-10-05 with 0 live-fetch URLs,
dedupe 136 rows / 0 unaccounted / AG19 sole conflict, less-flat-ui diff
exactly 6 hunks with 0 F22 markers in the global source, counts 166/72/123/
87/15, 64 trigger keys, banned terms 0, Grok pins only), the /demo (a)
wiring and (c) contract-as-written, and — the point of this audit — the
/demo (b) NOT-AUTOMATIC gate with all 20 DEMOGATE tokens occurring exactly
once and every referencer read in full context: no orchestrate step, no
hook, no post-build trigger, no finish-report step, and no other command
invokes /demo or pitch-deck-video automatically. The five changes since the
Audit #68 re-run are each verified fixed from the files: M-1 (hackathon-mode
§3 sequence), Sweep Finding 1 (the `-p` Remotion invocation at both call
sites, corroborated live by the dry-run re-run #2 logs), Sweep Finding 2
(the orch-build-mvp narration-key paragraph, DEMOGATE_B2S7_F22), the
hackathon-mode §7 narration-key condition, and the still-unwritten manifest
recorded as the known open close step rather than a finding. The
coordinator's next step is to write `fix22/MANIFEST.md`, then re-run sweep
#30b and formalize the dry-run #37 re-run report against this build for the
parent spot-check.
