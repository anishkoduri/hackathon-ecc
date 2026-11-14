# Audit #68 — fix #22 independent audit (NOT ZERO: 3 BLOCKING)

**Date:** Nov 12–13, 2026 (audit run overnight Nov 12 → Nov 13 CST)
**Auditor:** Audit #68 worker (check only — no plugin file edited, build.sh not
run, fix22.py / apply22.py / verify22.py not run or edited, nothing
bundled/committed/pushed, no message sent to anyone)
**Built tree:** `~/workspace/hackathon-plugin/hackathon-ecc/`
**Build state measured by this audit:** build.sh **23,758 lines, md5
`306dd648ab9dc4bee0e019a896e26f64`** (matches the task statement). Diff vs the
pre-fix22 backup `build.sh.before-fix22` (23,647 lines): **0 deletions, 111
additions** — the 85-line wave-1 fix22 block + BANG_PIN (Audit #67) plus 26
lines for the §13–§17 follow-up. All additions, nothing removed or rewritten.
**Verifiers re-run by this audit:** `fix22/verify22.py` **368/368 PASS**
(exit 0, run directly); prior verifiers pass except their frozen post-fix21
build.sh fingerprint lines (see §8). All counts below were re-derived
independently (own greps / own Python / own full-file reads), not copied
from verifier output.

**Method note:** every file named in §8(b) was read IN FULL (orchestrate
SKILL.md lines 40–90 and 327, orch-build-mvp skill + command,
orch-change-feature skill :51 + command, hackathon-pitch, deploy-fast
references, hackathon-mode.mdc, dispatch-prompt.md, commands/demo.md,
pitch-deck-video SKILL.md lines 1–830). The /demo verdicts rest on those
full-context reads, not on grep snippets.

## Verdict: AUDIT #68: NOT ZERO — 3 BLOCKING, 0 MINOR

The §1–§17 weave itself is clean (see §§1–7, 9): every item placed, every
pin/license/scope as specified, every standing rule holding, verify22
368/368. But the /demo (b) NOT-AUTOMATIC gate FAILS: **/demo is invoked
automatically in three places** — as an unconditional step of the autonomous
first-build pipeline (orchestrate step 5d, mandated by hackathon-mode §1/§7),
as an unconditional step of the standalone /orch-build-mvp pipeline (step 8,
"a required deliverable"), and as an unconditional re-film step of the
/orch-change-feature removal flow (step 5, `/demo --rebuild`). The parent's
rule (parent-addendum-nov12.md §3b) is absolute — "/demo NEVER runs on its
own… It runs ONLY when the user invokes /demo explicitly" — and "any
auto-invocation found is a BLOCKING audit finding". All three are confirmed
below with exact file:line + quoted context. Per the task, none was removed
by this audit; the coordinator removes them and re-runs the sweep + audit.

## BLOCKING findings

### B-1 — orchestrate step 5d invokes /demo as part of the autonomous first build
- **File:** `hackathon-ecc/skills/orchestrate/SKILL.md:73,80`
- **Context (quoted verbatim):**
  - `:56` — "Orchestrate's numbered sequence below (orchestrate steps 0–6)
    drives the first build end to end (narration-key prompt → scope →
    expansion Phases 0–3 → slice → build via the routing table incl. row 10
    → verify → polish → deploy → demo LOCAL → README → final report)."
  - `:52` — "When the run is a hackathon first build (grill-me done, or
    skipped at the user's say-so), the phases run in this order, **with no
    user approval gate after grill-me**".
  - `:73` — "5. **Verify → polish → deploy → demo, in that order** — four
    sub-steps inside this one step, never reordered".
  - `:80` — "**5d. Demo** — `/demo` (`pitch-deck-video`). `/demo` films the
    LOCAL app from the project dir only (`APP_DIR` to the app dir)… Pass the
    scoped wow moment into the /demo step: state it explicitly in the /demo
    dispatch… If a narration key was received mid-build (step 0,
    KEY-RECEIPT: yes), the /demo dispatch ALSO carries it… If no key was
    received, say so in the dispatch (KEY-RECEIPT: no) so /demo renders
    music-only/silent without asking."
  - `:327` (final-report sequence) — "Sequence: verify → polish → deploy →
    demo video (`/demo` / `pitch-deck-video` films the LOCAL app from the
    project dir, per orchestrate step 5 above; orchestrate sequences it, it
    does not film it) → README (`readme-writer`, orchestrate step 6) →
    final report."
- **Why this is an auto-invocation, not a conditional/manual step:** there is
  no condition on 5d anywhere in the file — no "if the user asked for a
  demo", no "only when…", no opt-out. The step dispatches /demo on every
  first build, and the surrounding text anticipates it running without any
  user input (KEY-RECEIPT: no → "renders music-only/silent without asking").
  Step 0's narration-key prompt exists precisely because a demo video will
  be built. The preliminary finding in parent-addendum-nov12.md §5 is
  CONFIRMED, not refuted.
- **Rule-level corroboration (same finding, not a separate one):**
  `hackathon-ecc/rules/hackathon-mode.mdc` §1 states the first-build
  sequence as "… → verify → polish → deploy → demo → README → final
  report", and §7 states: "The first build films `/demo` (`pitch-deck-video`)
  after deploy: the demo video is a required deliverable, filmed by
  default (film the real app) — then the README is written and the final
  report is delivered (deploy → demo → README → final report)." The rule
  mandates the filming; orchestrate 5d executes it.
- **Corroborating wiring:** `hackathon-ecc/commands/demo.md` — "If this
  /demo run was dispatched by orchestrate (step 5d) or orch-build-mvp
  (step 8), do NOT prompt — the prompt was already sent once at the start
  of the run"; `hackathon-ecc/skills/orchestrate/references/dispatch-prompt.md:30`
  — the Environment field is documented as "`ELEVENLABS_API_KEY=<redacted>
  context>` on a /demo dispatch when a narration key was received mid-build
  (orchestrate step 0 / step 5d)". Both files treat the 5d dispatch as live
  design, not stale text.
- **Recorded tension (per the addendum, not resolved here):** removing 5d
  changes the standing first-build contract (auto-approval pipeline:
  deploy, demo, commit, README; the demo video is part of what a requested
  first build produces). The manifest MUST record the behavior change
  explicitly when the coordinator removes it, and the parent spot-checks it
  before anything is reported to Anish.

### B-2 — orch-build-mvp step 8 invokes /demo as part of the standalone pipeline
- **Files:** `hackathon-ecc/skills/orch-build-mvp/SKILL.md` step 8;
  `hackathon-ecc/commands/orch-build-mvp.md` step 8
- **Context (quoted verbatim):**
  - Skill step 8 — "Deploy via `deploy-fast`, then film via `/demo`
    (`pitch-deck-video`) — LOCAL only.… The demo video is a required
    deliverable; its file is `<app-name>-video/out/demo.mp4`. If deploy was
    static-only or blocked, the final report notes that — never hard-abort
    the run for lack of a deployed URL."
  - Command step 8 — "Deploy via `deploy-fast`, then film via `/demo`
    (`pitch-deck-video`) — the demo video is a required deliverable; film
    the LOCAL app from the project dir only, never a deployed URL (if deploy
    was static-only or blocked, noted in the final report)."
- **Why this is an auto-invocation:** the user invokes `/orch-build-mvp`,
  not `/demo`; step 8 then films unconditionally as a numbered pipeline
  step, with no condition and no user prompt. The skill's own narration-key
  section states "Do NOT re-prompt at step 8 `/demo` time: the single early
  prompt covers the run" — i.e. step 8 /demo is expected to run. This is a
  second, independent auto-invocation site, not a mention.
- **Note:** `commands/demo.md`'s dispatch note (quoted under B-1) names
  orch-build-mvp step 8 alongside orchestrate 5d, confirming both dispatch
  paths are live.

### B-3 — orch-change-feature removal flow re-films via /demo --rebuild automatically
- **Files:** `hackathon-ecc/skills/orch-change-feature/SKILL.md:51`;
  `hackathon-ecc/commands/orch-change-feature.md:25`
- **Context (quoted verbatim):**
  - Skill :51 — "…then re-film via `/demo --rebuild`, which films the LOCAL
    app from the project dir (`APP_DIR`/project root), never a deployed
    URL; if the deploy was blocked, film local anyway and note in the final
    report that the video shows the local app, not the deployed one.… The
    removal's done-condition ("the demo video reflects the removal") is
    satisfied by the re-filmed LOCAL video + the honest hosting note…"
  - Command :25 — "…update `shots.json` before re-filming, re-film locally
    via `/demo --rebuild`, re-upload the video and update its link, update
    the docs, inventory, and pitch, and deliver the updated final report…"
- **Why this is an auto-invocation:** the user invokes
  `/orch-change-feature` with a removal request, not `/demo`; the pipeline
  then runs `/demo --rebuild` as an unconditional step of the removal flow.
  Under the parent's stated rule ("runs ONLY when the user invokes /demo
  explicitly") this is an auto-invocation.
- **Distinguishing context, recorded for the parent's adjudication (not a
  silent exemption):** unlike B-1/B-2, this re-film is intrinsic to the
  removal's own done-condition ("the demo video reflects the removal") —
  the user-initiated removal cannot be "done" without it — and the parent's
  preliminary note expected this file to be "likely a mention, not an
  invocation" (that expectation matches :54, "`/demo` vs `/demo --rebuild`",
  which IS a mention/documentation rule; it does not match :51, which is
  an invocation step). This audit flags it as BLOCKING per the rule as
  written; the parent/coordinator may carve out a documented exception for
  the removal re-film — but that exception must be recorded explicitly, not
  assumed by this audit.

## MINOR findings

None.

## 1. SPEC compliance §1–§17 — all placed

- **144-item disposition:** an independent script checked all 142 A–G rows
  of `fix22/disposition-merged.md` plus H1/H2 against the CURRENT tree.
  Every item's content is present in its SPEC'd home file. 56 rows' cited
  line numbers are STALE (not missing content): the §13–§17 follow-up
  inserted blocks above them — e.g. the §17 Casberry block inserted after
  A11 in motion-foundations pushes A12 `:90`→`:183`, A13–A20 `:217–281`→
  `:312–376`, B-tokens `:306–333`→`:404–431`; the LIQGLASS insert pushes
  F3 `:145`→`:184`; Taste gained 14 lines above the E-menu (E1 `:248`→
  `:262`). Content verified present at the new lines; verify22 (string
  checks, not line numbers) passes 368/368. The disposition's line numbers
  should be refreshed when the manifest is written — a documentation
  staleness note, not a finding.
- **§13 depth:** orchestrate step 3 names the depth strategy per surface
  (incl. explicit "flat by choice — <reason>"); ui-ux-pro-max depth rules;
  motion-foundations depth tokens; motion-patterns 3D patterns; Taste
  depth-as-dealt-moment (`:129`); polish-pass depth check. Cross-refs to
  A11 / Bang camera / Vanta / GSAP 3D / F6 present, no duplication.
- **§14 orbs:** nine states, no "thinking" state — see §4.
- **§15/§17 libraries:** pins + licenses + stack scope as specified —
  see §5.
- **§16 Vercel:** pinned snapshot + no live fetch + dedupe 136 — see §6.
- **Process additions (§9 Mobbin, §10 directives, §11 libraries, §12 Bang):**
  all present with their boundaries (evidence in §§4–6 and §7; Mobbin
  research step orchestrate `:62` MOBBIN_RESEARCH_F22, pattern refs Taste
  `:463` + ui-ux-pro-max `:170`, QA check polish-pass `:106`; DIRECTIVES_F22
  in all 8 required locations, re-confirmed for orchestrate `:72` and
  ui-ux-pro-max `:262`).

## 2. Standing rules — no regressions

- **Banned terms 0 in the built tree.** Own case-insensitive grep over
  `skills agents commands rules hooks README.md` (`--exclude-dir=node_modules`)
  for `claude|codex|anthropic|opus|sonnet|haiku|composer-2.5` returns 0
  lines (grep exit 1). verify22 agrees ("banned terms 0").
- **Grok pins only.** Tree-wide (excl. node_modules): `grok-4.7-high` **54**,
  `cursor-grok-4.6-high-fast` **102**, bare `grok-4.6-high-fast` (without the
  `cursor-` prefix) **0** — identical to Audit #67's counts.
- **Font rules (fix #19/#20/#21) untouched.** verify19's font anchors pass
  (see §8); F4 Tiempos/Fraunces body-only and F7 per-element font decisions
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
  hooks.json defines **15** hook events (the 17 `ls hooks/` entries are 16
  `.js` files + `hooks.json`; `adapter.js` is live Cursor infrastructure,
  adjudicated, not a hook). Trigger keys **64** (`withTriggers == 64` in
  `manifests/context-packs/skill-triggers@1.json`); verify22 asserts every
  key resolves to a real skill dir (PASS).
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
  ("**Depth — the seventh dimension (fix #22 §13, DEPTH_F22).** The six
  dimensions above are unchanged — the fix #19 D19 rule text is verbatim
  and stays byte-identical (verify19 asserts it as a substring)…").
- The extension line is separate and immediately after the rule (blank line
  between, `:121`/`:424` empty in both files). No "six dimensions" text was
  rewritten: "six dimensions" occurs 2× in each file (the rule + the
  extension line's "The six dimensions above are unchanged").

## 4. §14 Thinking Orbs — verified

- **Nine states, no "thinking" state:** working, searching, solving,
  listening, connecting, weaving, composing, breathing, shaping
  (motion-patterns `:331–355` table). The file states at `:342` ("NO state
  named 'thinking'") and `:357–362` the correction to the SPEC §14 draft
  mapping ("thinking = reasoning" is wrong; reasoning maps to `working` or
  `solving`; `breathing`'s on-screen label reads "Thinking…" but it is the
  IDLE/WAITING state — never use it for reasoning). Recorded as a flagged
  correction in orbs-patches.md §2.1/§2.8.2/§2.9.1 for parent adjudication —
  the SPEC itself invited verification, so this is a recorded correction,
  not a finding.
- **Pin + license:** `thinking-orbs@0.3.2`, MIT (ui-ux-pro-max `:122`,
  motion-patterns `:334`, `:442`). Pin choice (npm-published 0.3.2 vs
  repo main's 0.3.1) recorded with its reason in orbs-patches.md §2.8.1,
  flagged for coordinator/parent confirmation.
- **Sizes 64/20** with per-state tunings (motion-foundations `:498–540`,
  verified from `src/presets.ts`); speed multiplier; monochrome rule;
  reduced-motion frozen one-frame orb; offscreen/hidden pause
  (IntersectionObserver + visibilitychange, one frame painted while
  paused); DPR capped at 2; 2D canvas only.
- **RareFormLabs:** orbs-patches.md `:520–530` §2.5 records verbatim
  "rareformlabs connection unresolved — asset verified independently" and
  states no RareFormLabs link/repo/endorsement was found or invented, and
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
- **One-WebGL rule:** present incl. Casberry exports (WEBGL_ONE_F22,
  motion-patterns `:805`, `:891–892`; slop-checklist `:490–491`).
- **Running total 11:** "§11's 4 + §15's 4 + §17's 3 = 11"
  (ui-ux-pro-max `:523`).
- **Dangling `liquid-glass-design` reference:** resolved — 0 occurrences
  in the built tree (was 4 in build.sh per SPEC §15); the liquid-glass-js
  integration fills the gap the reference pointed at (L15-06, see §9).

## 6. §16 Vercel — verified

- **Pinned snapshot:** `skills/polish-pass/reference/vercel-checklist.md`
  (454 lines, VERCEL_F22 anchor `:1,3`), source
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
- **Dedupe 136 rows:** `fix22/vercel-dedupe.md` — 104 V-rows (90
  `command.md` rules + 14 anti-patterns) + 32 AGENTS.md-only rules = **136
  accounted, 0 unaccounted** (§4 totals). Dispositions: already-covered /
  partial / new per row with citations.
- **AG19 conflict recorded:** vercel-dedupe.md `:262` — APCA vs WCAG 4.5:1,
  "conflict — parent adjudication… Until then, WCAG 4.5:1 stands and APCA
  is not woven." Sole conflict (§4: "Conflicts needing parent
  adjudication: 1 — AG19").
- **License gap recorded:** checklist pinned-snapshot section — rules repo
  ships an MIT LICENSE (© 2025 Vercel Labs); skill repo has NO LICENSE
  file, README states MIT only; "no skill-repo text is copied here".
- **ECC-source check recorded:** checklist — ECC snapshot dated 2026-09-21
  used as the form; the plugin's ECC source at its pin
  (`affaan-m/ecc` at `d2ef2680594f9a17526a6e1a2e18b3d242c5d17b`, 2026-11-06)
  does NOT carry the skill ("it landed in ECC after the pin"), so the
  rules were ported from the rules repo at the pinned commit; "Port, not
  wire: wiring the skill would need an ECC pin bump (out of scope)".
- **Wiring:** polish-pass SKILL.md `:98–99` runs the Vercel checklist on
  every pass with the same standing as the slop checklist (candidate
  evidence, never verdicts; cleared only by a recorded D19 reason +
  theme-fit).

## 7. Weaving quality — woven, not appended (spot-checked)

One item per section traced to its SPEC'd placement AND reachable from the
design-package flow:
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
  + intro line `:260` carrying 2 + finish-gate pointer `:497`); 16 Hallmark
  Range lines in 15 theme files; E12/E14/E16 menu-only (no theme-file
  lines); E6 points at less-flat-ui #21, no duplication.
- **F:** verification-only; all 22 treatments + #23 Soft Shadow present in
  less-flat-ui; R3 two-kinds rule intact.
- **G:** glossary `design-taste-frontend/references/design-glossary.md`
  (GLOSSARY_F22, 20 terms); owning-skill pointers bidirectional —
  ui-ux-pro-max `:69`, motion-foundations `:710`, motion-patterns `:999`
  point at the glossary, and glossary entries name their owning skill.
- **H1/H2:** H1 accent concept ui-ux-pro-max `:125`, sprawl check
  slop-checklist `:419`, D11 points at it; H2 accent hierarchy in
  orchestrate step 3 + ui-ux-pro-max `:15` + polish check `:450`.
- **§9–§17:** all woven at their SPEC'd touchpoints (see §§1, 4–6);
  pointers resolve; no orphaned F22 anchor found in the spot-checks
  (PRINCIPLES_F22 ×1, LAWS_F22 ×1, GLOSSARY_F22 ×1, MOBBIN_RESEARCH_F22
  ×1, MOBBIN_QA_F22 ×1, DIRECTIVES_F22 ×1 in orchestrate; SLOP_F22 /
  UNSLOP_F22 / VERCEL_F22 title + anchor only — apparent extra counts are
  substring artifacts, e.g. `SLOP_F22` inside `UNSLOP_F22`).
- **No duplicated rules** in the spot-checks (dedupe pairs honored: B4
  recorded-not-duplicated, A14/G8 named-onto-existing-rule, D5/D8/D15
  pointers, G4/G13 glossary-pointing-at-existing, Vercel dedupe §6).
- **Apply-time corrections (apply22.py D-A1/D-A2/D-A5) honored:** D-A2 —
  L15-06 is a runtime-block patch on the built copy (build.sh `:23722`),
  global source NOT edited (see §9); D-A5 — ORB-PP1 anchor corrected to
  DEPTH-08's anchor, orb check appended as the final slop-checklist
  section (`:552`); D-A1 — 'after' inserts normalised to the wave-1
  paragraph-break convention (spot-checked: DEPTH-13 insert in build.sh
  `:23714` starts with `\n\n`).

## 8. /demo gates — verdicts

### (a) CALLABLE — PASS by wiring; live execution NOT verified in this environment
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
- **What was NOT verified (stated explicitly, per the task):** no live
  /demo execution was run in this audit — this audit is read-only (no
  build.sh runs, no filming) and dry-run #37, which is scaffolding a
  sample app + demo-sample-video as this audit ran (see §10), had produced
  no report yet. So callability is established by wiring (command file +
  frontmatter + command-list reachability + skill invocation path +
  staged==built), NOT by a live film. The invocation path
  (shots.json → Remotion → film → narrate) resolves end-to-end in the skill
  text (scaffold → learn → shots.json → `APP_DIR=… npm run all` →
  narration → recording → frames → render → QA), with no missing step in
  the text — but that is a wiring claim, not a live-execution claim, and
  this audit does not present it as one.

### (b) NOT AUTOMATIC — FAIL (BLOCKING — see B-1, B-2, B-3)
- Grep-verify: hooks contain zero "demo" hits (`hooks/hooks.json` 0;
  all hook `.js` files 0) — no hook invokes /demo. No post-build trigger
  or finish-report step invokes /demo (the end-of-project checks run the
  six deferred audits, not /demo).
- Full-context reads of every other pitch-deck-video referencer:
  - **orchestrate SKILL.md — INVOCATION (B-1).** Step 5d, unconditional
    (evidence quoted in B-1).
  - **orch-build-mvp skill + command — INVOCATION (B-2).** Step 8,
    unconditional, "required deliverable".
  - **orch-change-feature skill :51 + command :25 — INVOCATION (B-3).**
    Re-film via `/demo --rebuild` in the removal flow, unconditional.
  - **hackathon-pitch — MENTION.** Owns pitch narrative only; states
    explicitly "never the demo video itself (pitch-deck-video / /demo owns
    that)"; the only /demo references are length-canonical pointers.
  - **deploy-fast — MENTION.** "the demo VIDEO is filmed from local code
    only — never a deployed URL — see `pitch-deck-video`" (`:21`); all
    other "demo" hits are live-demo/presentation usage, not /demo.
  - **hackathon-mode.mdc — MANDATE (part of B-1).** §1 sequence and §7
    ("filmed by default… required deliverable") mandate the filming that
    orchestrate 5d executes.
  - **feature-expansion, readme-writer, fastapi-patterns — MENTIONS.**
    Generic "demo" (demo flow, demo links, dev/demo environments); no
    `/demo` or pitch-deck-video invocation.
  - **orch-pipeline, gan-build, devpost-autofiller, orch-add-feature,
    orch-fix-defect, orch-refine-code (+ commands) — NO REFERENCES.**
  - **dispatch-prompt.md — DISPATCH MECHANISM (supports B-1).** The
    Environment field documents the /demo dispatch ("orchestrate step 0 /
    step 5d"); a template, not a separate invocation.
  - **plugin.json / README — MENTIONS.** Command-listing text only.
- The preliminary finding is CONFIRMED for orchestrate 5d and EXTENDED to
  orch-build-mvp step 8 and orch-change-feature's re-film. Step 5d is NOT
  a conditional/manual step: the full context (quoted in B-1) shows an
  unconditional numbered step in a pipeline that runs "with no user
  approval gate after grill-me", with fallback handling for the no-key
  case ("renders music-only/silent without asking") — i.e. it runs even
  when the user said nothing about a video.

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
  live film was rendered in this audit (read-only; dry-run #37 in
  progress, no report yet — §10), so the contract is verified as written,
  not as executed.

## 9. less-flat-ui diff — exactly 6 hunks; global source NOT edited

- `diff ~/workspace/cursor-skills/less-flat-ui/SKILL.md
  hackathon-ecc/skills/less-flat-ui/SKILL.md` = **6 hunks**: 4 Batch E
  (design-decision pointer insert; wow-moment line; record-treatments
  line; re-tint line) + 2 fix22 (DEPTH-13 at the Soft Shadow section;
  L15-06 liquid-glass insert before "### 3. Thermal gradients").
- Global source contains **0** `F22` markers (mtime Nov 12 02:08,
  pre-fix22); the plugin-scoped notes live only in the built copy via the
  runtime block — DEPTH-13 at build.sh `:23714`, L15-06 at `:23722`
  (apply22 D-A2 honored).

## 10. Verifiers, open items, and recorded tensions (not findings)

- **verify22.py: 368/368 PASS, exit 0** (re-run by this audit). Prior
  verifiers pass except their frozen post-fix21 build.sh fingerprint lines
  (verify21 96/102, verify20 164/169, verify19 71/76, verify18 69/72,
  verify17 58/60, verify15 42/44 — the fingerprint is legitimately
  superseded by fix #22: 23,758 lines / md5 `306dd648…`; verify22 §17
  allows exactly those lines).
- **Open items (coordinator steps, not audit findings — same treatment as
  Audit #67):**
  1. `fix22/MANIFEST.md` **not yet written** (absent at audit time; the
     manifest must record the B-1 behavior change when 5d is removed, the
     refreshed disposition line numbers per §1, and the RareFormLabs
     sentence per §4).
  2. **Sweep #30b not run** — no sweep30b report exists; the
     weaving-coherence pass it must contain is therefore not yet
     evidenced by a sweep (this audit's §7 spot-checks are not a
     substitute for the sweep).
  3. **Dry-run #37 in progress, no report yet** — `fix22/dryrun37/` was
     created during this audit (Nov 13 01:22; `sample-app/` + a
     `demo-sample-video/` scaffold with `npm-install.log` at 01:23). Its
     /demo (a)/(c) live-execution evidence was therefore NOT available to
     this audit; see §8(a)/(c) limits.
  4. **Close criteria not yet met:** per parent-addendum §4, close needs
     Audit #68 ZERO + dry-run #37 PASS + sweep CLEAN + verify22 100% +
     prior verifiers + banned terms 0 + build clean + MANIFEST written.
     This audit is NOT zero (3 blocking), so the fix cannot close on this
     audit regardless of items 1–3.
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

**AUDIT #68: NOT ZERO — 3 BLOCKING (B-1, B-2, B-3), 0 MINOR.**

Everything else audited is clean: the §1–§17 weave, all pins/licenses/
scopes, D19 form, orbs, Vercel snapshot, less-flat-ui diff, counts,
banned terms (0), Grok pins, screen-verdicts rule, and the /demo (a)
wiring and (c) contract-as-written. The single failing gate is (b):
/demo runs automatically in three places. The coordinator's next steps:
remove the three auto-invocations (orchestrate 5d + hackathon-mode
§1/§7 mandate, orch-build-mvp step 8, orch-change-feature re-film),
update `commands/demo.md`'s dispatch note (which currently documents the
5d/step-8 dispatches as live paths), record the B-1 behavior change in
the manifest, then re-run sweep #30b + dry-run #37 + a fresh audit.
