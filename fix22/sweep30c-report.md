# Sweep #30c — fix #22 confirmation sweep (new build)

**Verdict: SWEEP #30c: CLEAN — 0 blocking, 0 minor.** All three findings from the
sweep #30b re-run (1 blocking + 2 minor) are verified FIXED in this build, both
Audit #68 re-run minors (M-1, M-2) are verified FIXED except for the manifest
itself, which per the task is recorded as the known open close step and NOT
flagged this round. verify22 re-runs **368/368**, the build fingerprint matches
the task statement exactly, the anchor table re-derives to **57 tokens
(37 pre-demogate + 20 DEMOGATE)** with every DEMOGATE token exactly once, the
/demo never-automatic re-check passes at every site, and the weaving-coherence
pass is CLEAN for all of §1–§17.

**Scope:** built tree `~/workspace/hackathon-plugin/hackathon-ecc/`
(`node_modules/` excluded everywhere), `build.sh`, staged sources
(`new-skills/`, `new-rules/`), and the fix22 working files. SPEC read first
(`fix22/SPEC.md` §§1–17); sweep #30b re-run report, Audit #68 re-run report,
`fix22/PARENT-GUIDANCE.md`, and `fix22/parent-addendum-nov12.md` read before
checking. Method: every number below was re-derived by running the greps /
commands listed in §12; nothing was copied from Audit #67/#68, Dry-run
#36/#37, the sweep #30b re-run, or the coordinator's reports without
re-running. This sweep made no plugin change (read-only); its only write is
this report. No `bash build.sh` run, no bundle/commit/push, no message sent,
no live /demo film run.

**Given state (measured by this sweep):** `build.sh` **23,774 lines, md5
`4799a819791b9c3ec4c19136ad698397`**; pre-fix22 baseline
`build.sh.before-fix22` 23,647 lines, md5
`8dfacb47a2a6698d47e4b4a5f8d9126c` — diff **+127/−0, exactly 2 hunks** (§1).
Counts 166 skills / 72 agents / 123 rules / 87 commands / 15 hooks;
64 trigger keys, all resolving. `fix22/verify22.py` re-run by this sweep:
**368/368, exit 0**.

---

## Prior findings — all verified FIXED

| Prior finding | Re-check by this sweep |
|---|---|
| Sweep #30b re-run Finding 1 (BLOCKING) — bare `npx @remotion/cli@4.0.526 <cmd>` cannot execute (three binaries) | **FIXED.** Both call sites now use the `-p` form with the binary named explicitly: `hackathon-ecc/skills/pitch-deck-video/template/scripts/build.mjs:335` — `run('npx', ['-p', '@remotion/cli@4.0.526', 'remotion', 'render', …` — and `qa.mjs:42` — `execFileSync('npx', ['-p', '@remotion/cli@4.0.526', 'remotion', 'still', …`. The staged sources carry the same form at the same lines (`new-skills/pitch-deck-video/template/scripts/build.mjs:335`, `qa.mjs:42`) and are byte-identical to the built copies (`diff` clean). Bare-form count: **0** in the built tree and **0** in `new-skills/`; `remotion@4.0.542`: **0** in the built tree, **0** in `build.sh`, **0** in `new-skills/`. Note on form: the invocation is argv-element form (`'npx', ['-p', '@remotion/cli@…', 'remotion', …`), so the contiguous string `npx -p @remotion/cli@4.0.526 remotion` does not occur as text — the `-p` form was verified by direct reads of both call sites, not by that string. This sweep did not live-execute the form (read-only; no filming run). |
| Sweep #30b re-run Finding 2 (minor) — orch-build-mvp narration-key paragraph still assumed a video will be filmed | **FIXED.** `hackathon-ecc/skills/orch-build-mvp/SKILL.md:32` (runtime patch DEMOGATE_B2S7_F22, new this build) now opens: "At the start of the run (step 1), **if the user asked for a demo video** and narration will need a key and none is set … issue the single `pitch-deck-video` narration-key prompt once. **If the user did NOT ask for a demo video, do NOT send this prompt — no video is being built, so no key is needed** …". The stale references are reworded as conditional: "Do NOT re-prompt at `/demo` time: the single early prompt covers the run, and **a user-invoked `/demo`** uses the key if present, else falls back to music-only/silent." / "**Key handoff to a user-invoked `/demo`:** … pass it to `/demo` via the dispatch **if the user asks for a video** … If the key arrives after **the user-invoked `/demo`** already rendered but before the step-9 final report, re-run the video script step …". DEMOGATE_B2S7_F22 occurs **exactly once** in the built tree and **once** in `build.sh` (`:23748`, the patch tuple — whose search side is the old paragraph text, as expected for a search-and-replace patch; the built tree carries the new conditioned text). |
| Audit #68 re-run M-1 (minor) — hackathon-mode §3 still stated "(after deploy, demo, commit, and README)" | **FIXED.** `hackathon-ecc/rules/hackathon-mode.mdc:22` now reads "(after deploy, commit, and README)". Tree-wide grep for `after deploy, demo|deploy, demo, commit|deploy → demo|demo → commit` returns **0**; the string "after deploy, commit, and README" occurs **1×** in the built tree (`hackathon-mode.mdc:22`). §7 carve-out (`:61`) reads "after deploy/commit/README" as before. |
| Audit #68 re-run observation — hackathon-mode §7 narration-key paragraph did not restate the "only when the user asked" condition | **FIXED.** `hackathon-mode.mdc:59` now states: "orchestrate sends it immediately after grill-me, before scoping (orchestrate step 0) — **only when the user asked for a demo video**; on the grilled path and on the skip-grilling path alike … **If the user did NOT ask for a demo video, do NOT send this prompt — no video is being built, so no key is needed.**" §1 (`:12`) also states the condition ("only when the user asked for a demo video"). |
| Sweep #30b re-run Finding 3 / Audit #68 re-run M-2 (minor) — hackathon-mode cites `fix22/MANIFEST.md`, which does not exist | **NOT flagged this round, per the task.** `fix22/MANIFEST.md` is **still unwritten** (`ls` fails; verify22.py itself prints the "not yet written" NOTE with the measured lines/md5). Recorded as the **known open close step**: the manifest is written by the coordinator only after the loops return clean. `hackathon-mode.mdc:68` still carries the present-tense sentence "the behavior change is recorded in `fix22/MANIFEST.md`" — the only `fix22/MANIFEST.md` reference in the built tree — which becomes true when the manifest is written, with no rule-text change. |

---

## 1. Build fingerprint + diff — PASS

- `build.sh`: **23,774 lines, md5 `4799a819791b9c3ec4c19136ad698397`** (matches
  the task statement); `build.sh.before-fix22`: 23,647 lines, md5
  `8dfacb47a2a6698d47e4b4a5f8d9126c`.
- `diff build.sh.before-fix22 build.sh`: **+127 / −0, exactly 2 hunks** —
  `41a42,46` (5 `BANG_PIN` lines; `BANG_PIN="c1aa65e921c970d858705fcb4a53a8294d1a4131"`
  at `build.sh:42`) and `23635a23641,23762` (the 122-line fix22 block,
  `build.sh:23641–23762`). No other line changed. (Vs the sweep #30b re-run
  build: +1 line — the DEMOGATE_B2S7 runtime patch.)
- The fix22 block contains all 11 §13–§17 anchor tokens and the B2/B3
  DEMOGATE runtime patches; it appears exactly once.

## 2. Anchor table — all 57 tokens resolve (occurrence counts)

Counts are substring occurrences in the built tree (excl. `node_modules`)
and in `build.sh`. "Home" = the file carrying the rule text; other files are
pointers / cross-references, the established pattern. Zero-token rows: none.
Total is **57 = 37 pre-demogate + 20 DEMOGATE** — the sweep #30b re-run
counted 56 with 19 DEMOGATE; the new DEMOGATE_B2S7_F22 makes 20, as the task
predicted. Every other count below reproduces the sweep #30b re-run table
exactly. (`SLOP_F22`'s tree count of 28 includes its occurrences inside
`UNSLOP_F22`; standalone `SLOP_F22` is 12 — the known substring artifact,
same as Audit #68 §7.)

| Anchor | Built occ. (files) | build.sh occ. | Home |
|---|---:|---:|---|
| `PRINCIPLES_F22` | 5 (5) | 3 | motion-foundations Principles ×1 |
| `LAWS_F22` | 4 (4) | 3 | motion-foundations Decision Guidance laws ×1 |
| `ANIM_TOKENS_F22` | 1 (1) | 1 | motion-foundations (AB-03g group label) |
| `ANIM_RULES_F22` | 1 (1) | 1 | motion-patterns (AB-05g group label) |
| `ANIM_ADV_F22` | 1 (1) | 1 | motion-advanced (AB-09g group label) |
| `SLOP_F22` | 28 (11) | 12 | slop-checklist anchor `:1–3`, 20 indicators |
| `UNSLOP_F22` | 16 (8) | 10 | unslop-fixes anchor `:1–3`, 20 fixes |
| `TRENDS_F22` | 53 (16) | 0 | Taste SKILL.md ×23 (20 entries + intro ×2 + finish-gate pointer); 15 Hallmark theme files ×30 |
| `GLOSSARY_F22` | 5 (5) | 3 | design-glossary.md ×1, 20 terms |
| `ACCENT_F22` | 11 (6) | 2 | ui-ux-pro-max H1 + sprawl check |
| `ACCENTUATION_F22` | 6 (5) | 1 | orchestrate design-package step + hierarchy rules/check |
| `MOBBIN_RESEARCH_F22` | 1 (1) | 0 | orchestrate `:64` (mega-line) |
| `MOBBIN_PATTERN_F22` | 2 (2) | 1 | Taste `:463`, ui-ux-pro-max `:170` |
| `MOBBIN_QA_F22` | 1 (1) | 0 | polish-pass `:106` step 8 (category-conventions check) |
| `DIRECTIVES_F22` | 8 (7) | 4 | All 8 required locations (§10) |
| `LENIS_F22` | 4 (3) | 4 | motion-foundations `:273` |
| `GSAP_F22` | 2 (1) | 2 | ui-ux-pro-max `:322–346` |
| `SCROLLTRIGGER_F22` | 4 (3) | 4 | motion-patterns `:553` |
| `VANTA_F22` | 10 (3) | 5 | Taste `:127` (+ pointers) |
| `REACTBITS_F22` | 5 (2) | 5 | motion-patterns `:724` |
| `BANG_ANTISLIDE_F22` | 1 (1) | 0 | pitch-deck-video `:247` |
| `BANG_ONEWORLD_F22` | 1 (1) | 0 | pitch-deck-video `:281` |
| `BANG_STYLES_F22` | 1 (1) | 0 | pitch-deck-video `:304` |
| `BANG_OPENERS_F22` | 1 (1) | 0 | pitch-deck-video `:337` |
| `BANG_KINETIC_F22` | 1 (1) | 0 | pitch-deck-video `:373` |
| `BANG_EXPLAINER_F22` | 1 (1) | 0 | pitch-deck-video `:409` |
| `DEPTH_F22` | 35 (8) | 14 | orchestrate design-package + extension lines |
| `ORBS_F22` | 24 (6) | 12 | motion-patterns orb pattern + tokens + checks |
| `R3F_F22` | 11 (5) | 7 | Taste `:135` / motion-foundations / motion-patterns |
| `LIQGLASS_F22` | 6 (4) | 2 | less-flat-ui liquid-glass block + Taste `:136` |
| `SHADERGRAD_F22` | 7 (3) | 3 | Taste `:134`, ui-ux-pro-max `:447` |
| `LIQLOGO_F22` | 6 (3) | 4 | Taste step 4a `:435` (label home) |
| `WEBGL_ONE_F22` | 9 (6) | 5 | one-WebGL-per-surface rule, all homes |
| `VERCEL_F22` | 8 (4) | 6 | vercel-checklist.md `:1–3` (label home) |
| `CASBERRY_F22` | 5 (5) | 3 | motion-foundations `:90` + Taste `:138` |
| `ORIGINKIT_F22` | 3 (3) | 2 | Taste `:139`, motion-patterns, ui-ux-pro-max |
| `DAISYUI_F22` | 3 (3) | 2 | design-system `:35`, Taste, ui-ux-pro-max |
| `DEMOGATE_O4_F22` | 1 (1) | 0 | orchestrate `:80` (step 5d gate) |
| `DEMOGATE_O9_F22` | 1 (1) | 0 | orchestrate `:82` (step 6 Order sentence) |
| `DEMOGATE_B2S1_F22` | 1 (1) | 1 | orch-build-mvp SKILL.md `:83` |
| `DEMOGATE_B2S2_F22` | 1 (1) | 1 | orch-build-mvp SKILL.md `:83` |
| `DEMOGATE_B2S3_F22` | 1 (1) | 1 | orch-build-mvp SKILL.md `:83` |
| `DEMOGATE_B2S4_F22` | 1 (1) | 1 | orch-build-mvp SKILL.md `:84` |
| `DEMOGATE_B2S5_F22` | 1 (1) | 1 | orch-build-mvp SKILL.md `:84` |
| `DEMOGATE_B2S6_F22` | 1 (1) | 1 | orch-build-mvp SKILL.md `:84` (carve-out timing) |
| `DEMOGATE_B2S7_F22` | 1 (1) | 1 | orch-build-mvp SKILL.md `:32` (narration-key condition) — NEW |
| `DEMOGATE_B2C1_F22` | 1 (1) | 1 | commands/orch-build-mvp.md `:36` |
| `DEMOGATE_B3S1_F22` | 1 (1) | 1 | orch-change-feature SKILL.md `:51` |
| `DEMOGATE_B3S2_F22` | 1 (1) | 1 | orch-change-feature SKILL.md `:51` |
| `DEMOGATE_B3S3_F22` | 1 (1) | 1 | orch-change-feature SKILL.md `:51` |
| `DEMOGATE_B3S4_F22` | 1 (1) | 1 | orch-change-feature SKILL.md `:51` |
| `DEMOGATE_B3S5_F22` | 1 (1) | 1 | orch-change-feature SKILL.md `:51` |
| `DEMOGATE_B3S6_F22` | 1 (1) | 1 | orch-change-feature SKILL.md `:51` |
| `DEMOGATE_B3S7_F22` | 1 (1) | 1 | orch-change-feature SKILL.md `:52` |
| `DEMOGATE_B3C1_F22` | 1 (1) | 1 | commands/orch-change-feature.md `:25` |
| `DEMOGATE_H1_F22` | 1 (1) | 0 | hackathon-mode.mdc `:68` (§7 mandate) |
| `DEMOGATE_H2_F22` | 1 (1) | 0 | hackathon-mode.mdc `:12` (first-build sequence) |

All 20 DEMOGATE tokens occur **exactly once** in the built tree. 16 of them
occur in `build.sh` (the B2/B3 runtime patches, `build.sh:23733–23748`); the 4
that do not (`O4`, `O9`, `H1`, `H2`) live in staged sources installed by
`cp` — `new-skills/orchestrate/SKILL.md` and `new-rules/hackathon-mode.mdc`
— not in the fix22 runtime block. That is expected, not a gap: staged
`new-skills/orchestrate/SKILL.md` is byte-identical to the built copy, and
staged `new-rules/hackathon-mode.mdc` matches the built copy on every line
except `:38` (see §8, checked and cleared — a documented build-time fix16
scrub, not a fix #22 divergence). No duplicate anchor definitions; the Sweep
#30 finding-1 class (orphaned anchors) is absent — every anchor resolves,
each home file carrying its anchor ×1. 0 in `build.sh` for `TRENDS_F22`,
`MOBBIN_RESEARCH_F22`, `MOBBIN_QA_F22`, and all six `BANG_*` tokens is
expected (staged-source installs, not fix22 patch-block text).

## 3. /demo never-automatic re-check — PASS

Grep-verified over the whole built tree (excl. `node_modules`), then
full-context reads of every file that mentions `/demo` or
`pitch-deck-video` (referencer list below):

| Check | Result |
|---|---|
| "filmed by default" | **0** |
| "deploy → demo" | **0** |
| "after deploy, demo" / "deploy, demo, commit" / "demo → commit" | **0** |
| "deploy/demo" | **1** — `README.md:40` only: "deploy/demo/orchestration workflows" — a capability phrase in a list, not a sequence. Acceptable, as specified. |
| "required deliverable" | **2** — (1) hackathon-mode `:68`, the H-1 negation ("no longer a required deliverable"); (2) `pitch-deck-video/template/src/Video.tsx:15`, a pre-existing template comment ("Audio guards — the video is a required deliverable and must NEVER abort on a missing audio file") — staged source byte-identical, so this predates fix #22 and describes the video's own audio guards once /demo runs, not a pipeline invocation. Checked and cleared, not a finding. |
| "Film via `/demo`" | **1** — orch-change-feature `SKILL.md:51` only, conditional: "If the user asks for a re-film, re-film via `/demo --rebuild`". |
| "then film via `/demo`" | **0** |
| Hooks invoking /demo | **0** "demo" hits in `hackathon-ecc/hooks/` (hooks.json + all hook `.js` files) |

**The 6 removal sites + follow-ups, each read in full context (current build):**

| Site | Current text (built tree) | Verdict |
|---|---|---|
| orchestrate step 5d, `SKILL.md:80` | "**Demo — never automatic (fix #22 /demo gate, DEMOGATE_O4_F22).** `/demo` … is NEVER dispatched by this pipeline. It runs ONLY when the user invokes `/demo` explicitly (or the user's request explicitly asks for a demo video). … If no video was requested, the final report notes that no demo video was filmed." | Gate present |
| orchestrate step 0 narration-key prompt, `SKILL.md:58` | "ONLY when the user asked for a demo video; it never blocks the build. … If the user did NOT ask for a demo video, do NOT send this prompt — no video is being built, so no key is needed" | Conditional |
| orchestrate sequence, `SKILL.md:56` | "… → verify → polish → deploy → README → final report). /demo is never part of this sequence — it runs ONLY when the user invokes it explicitly (fix #22 /demo gate)." | Gate present |
| orchestrate step 6 Order, `SKILL.md:82` | "Order: verify → polish → deploy → commit → README → final report. (A demo video is filmed only when the user invokes `/demo` explicitly — it is never part of this order; fix #22 /demo gate, DEMOGATE_O9_F22.)" + README input conditional ("if a video was filmed, the video file path … as inputs") | Gate present |
| orchestrate final report, `SKILL.md:327`, `:344` | "After deploy and the README, write it …"; demo-video handoff "(only if a video was filmed)" | Gate present |
| orch-build-mvp skill step 8, `SKILL.md:83` | "**Demo — never automatic (… DEMOGATE_B2S1_F22).** `/demo` is not filmed here. … Do NOT film via `/demo` here — `/demo` … runs ONLY when the user invokes it explicitly … If no video was requested, the final report notes that no demo video was filmed. (… DEMOGATE_B2S2_F22)" | Gate present |
| orch-build-mvp skill step 9, `SKILL.md:84` | Carve-out timing "after deploy/commit/README" (DEMOGATE_B2S6_F22); handoff "if a video was filmed" / "If no video was filmed, the report notes that instead" (DEMOGATE_B2S4/B2S5_F22) | Gate present |
| orch-build-mvp skill step 1, `SKILL.md:32` | Narration-key prompt conditioned on the user having asked for a video; step-8 references now "a user-invoked `/demo`" / "if the user asks for a video" (DEMOGATE_B2S7_F22) | Fixed (Finding 2) |
| orch-build-mvp command step 8, `commands/orch-build-mvp.md:36` | "Do NOT film via `/demo` here — `/demo` runs ONLY when the user invokes it explicitly (or the user's request explicitly asks for a demo video); if the user asked for one, film the LOCAL app … (… DEMOGATE_B2C1_F22)" | Gate present |
| orch-change-feature skill step 5, `SKILL.md:51` | Re-film only "If the user asks for a re-film" (DEMOGATE_B3S1_F22); "(The poll verifies the redeploy; it is not a prelude to filming — no re-film happens here.)"; done-condition "re-filmed … (if the user asked for a re-film) + honest hosting note, or … stale-video record when no re-film was requested — never by an automatic re-film" (DEMOGATE_B3S5_F22) | Gate present |
| orch-change-feature skill step 6, `SKILL.md:52` | "demo video STALE — shows the removed feature; re-film with `/demo --rebuild` on request" (DEMOGATE_B3S7_F22) | Gate present |
| orch-change-feature command, `commands/orch-change-feature.md:25` | "re-film with `/demo --rebuild` only when the user asks" (DEMOGATE_B3C1_F22) | Gate present |
| hackathon-mode §7, `rules/hackathon-mode.mdc:68` | "The first build does NOT film `/demo` automatically (… DEMOGATE_H1_F22). `/demo` … runs ONLY when the user invokes it explicitly … never as a pipeline step, never by default. … (deploy → README → final report)." | Gate present |
| hackathon-mode §1 sequence, `rules/hackathon-mode.mdc:12` | First-build sequence "grill → narration-key prompt (… only when the user asked for a demo video …) → scope → expansion → build → verify → polish → deploy → README → final report. /demo is never part of this sequence — it runs ONLY when the user invokes it explicitly (… DEMOGATE_H2_F22)." | Gate present |
| hackathon-mode §3 carve-out, `:22` | "… (after deploy, commit, and README) …" | Fixed (M-1) |
| hackathon-mode §7 carve-out, `:61` | Exception text "… it runs once, after deploy/commit/README, and never gates a feature." | Gate present |
| `commands/demo.md:13` dispatch note | No longer names orchestrate 5d / orch-build-mvp step 8 as dispatchers: "When narration needs a key and none is set, the skill's narration-key prompt applies: if the user invoked /demo directly, prompt the user once, at the point the video is confirmed, for the ElevenLabs …" | Fixed |
| `orchestrate/references/dispatch-prompt.md:29` Environment field | "`ELEVENLABS_API_KEY=<redacted>` … on a /demo dispatch when a narration key was received mid-build (orchestrate step 0 — only when the user asked for a demo video)" | Conditional |

**All other `pitch-deck-video` referencers** (grep `-l` over the tree):
`commands/demo.md`, `manifests/context-packs/skill-triggers@1.json`,
`manifests/install-modules.json`, `rules/hackathon-mode.mdc`,
`skills/deploy-fast/SKILL.md`, `skills/hackathon-pitch/SKILL.md`,
`skills/orch-build-mvp/SKILL.md`, `skills/orch-change-feature/SKILL.md`,
`skills/orchestrate/SKILL.md`, `skills/pitch-deck-video/` (itself, references,
template). Checked and cleared (mentions, not invocations):
`deploy-fast/SKILL.md:21` (live-demo vs filmed-video distinction),
`hackathon-pitch/SKILL.md:3,32` (pitch storyboard; "never the demo video
itself"), `readme-writer/SKILL.md:95` (ledger video-path inputs, conditional
on a video existing), `fastapi-patterns/SKILL.md:53` /
`feature-expansion/SKILL.md:128` (generic "demo" usage, no `/demo`),
`devpost-autofiller` (post-removal video-link check), `.cursor-plugin/plugin.json`
/ `README.md` / manifests (command listings). The remaining `/demo` hits in
the tree are Taste asset `demo.html`/`demo.css`/`demo.js` files — demo pages
for dealt moments, not the `/demo` command. No hook, no post-build trigger,
no finish-report step, and no other command invokes /demo or
pitch-deck-video automatically. **Any remaining auto-invocation: none found.**

**/demo (a) callable + (c) contract intact — text-verified (no live film run
by this sweep, read-only):** `hackathon-ecc/commands/demo.md` exists with the
`/demo` frontmatter and pitch-deck-video invocation; BANG anchors at
pitch-deck-video `:247/:281/:304/:337/:373/:409` in both staged and built
copies; F6 under-2:10 hard rule / absolute max 2:30 at
pitch-deck-video `SKILL.md:102`; Edge at position 3 in the beat budget
(`:107–109`, Problem 1 → Wow 2 → Edge 3). The Remotion render/QA path is
now the corrected `-p` form at both call sites (see Prior findings); live
execution of that form was not run in this sweep.

## 4. Weaving-coherence pass — CLEAN (per §1–§17)

For every §1–§17 item I verified: (i) it is reachable from the
design-package flow at its SPEC'd placement — orchestrate step 3
design-package-in-every-UI-slice-brief (`skills/orchestrate/SKILL.md:62`,
mega-line) → Taste step 4a / ui-ux-pro-max / motion-* / less-flat-ui /
polish-pass — with its D19 reason and its §10 directive form intact;
(ii) its pointers resolve (bidirectional where the SPEC requires); (iii)
it is not duplicated elsewhere. No item is only appended. Result by
section (line numbers are the current build's; where a line is a mega-line
I cite the anchor instead of a short quote):

| Section | Flow entry point (SPEC'd placement) | Reachability / pointers | Result |
|---|---|---|---|
| §1–§3 A (A1–A20) | orchestrate `:62` "Motion principles in every UI slice brief (PRINCIPLES_F22 / LAWS_F22)" → motion-foundations Principles header `:35` (A1 `:52`, A13 `:312`, A14 `:320`) + Decision Guidance `:239` | make-interfaces-feel-better + ui-ux-pro-max point back to the laws (LAWS_F22 4 files); A7→B7, A8→B6, A2→B5/B19 cross-refs present per disposition | PASS |
| B (B1–B20) | Same brief line → motion-foundations tokens (`dropdown: 0.2` `:404`, `staggerRow: 0.03` `:405`, `popover: 0.95` `:427`, `stretch: 1.12` `:428`, `exitFactor: 0.8` `:431`) + motion-patterns Rules / motion-advanced (ANIM_RULES_F22, ANIM_ADV_F22 each 1× in home) | Group anchors AB-03g/05g/09g resolve (§2); B4/B18 covered-evidence intact; B3/B15/B4 conflict flags carried, not resolved | PASS |
| C (C1–C20) | orchestrate Verify step → polish-pass SKILL.md `:98–99` (SLOP_F22 ×4, VERCEL_F22 ×2 in the file; the slop + Vercel checklists run on every pass) → slop-checklist anchor `:1–3`, all 20 indicators as flags with D19-reason + theme-fit clearance | Taste finish gate + Impeccable detector context point at the checklist; each fix pairs to unslop-fixes | PASS |
| D (D1–D20) | Same polish-pass step → unslop-fixes anchor `:1–3`, all 20 fixes; CD pointers in quick-reference + motion-* | D11→H1, D20→A10/B8 family, D5/D8/D15 pointers (not restated) — §4 | PASS |
| E (E1–E20) | Taste step 4a trend menu (`TRENDS_F22` ×23 in Taste; menu intro `:260`, E1 `:262`, E17 `:374`, E20 `:395`) — the design package MAY draw on it; 16 Hallmark Range lines in 15 theme files | E12/E14/E16 menu-only: no theme file carries an eyebrow, sparkle, or three-icon-cards line; E6 points at less-flat-ui #21, no duplication | PASS |
| F (F1–F22) | less-flat-ui catalogue (`:8` source note, `:103` "## The 23 treatments"), reached via orchestrate `:62` ("`less-flat-ui` where dull/flat") + Taste step 4a + R3 (≥2 distinct treatment kinds) | Verification-only: no text copied; all 22 + #23 Soft Shadow present (§5) | PASS |
| G (G1–G20) | One glossary file, reached from every owning skill: ui-ux-pro-max `:69`, motion-foundations `:710` (G18), motion-patterns `:999` (G10/G14/G20) — each "Design vocabulary — the definitions … live in `design-glossary.md` (`GLOSSARY_F22`)" | Glossary carries the owning-skill column per term (e.g. G1 Kerning, G8 → ui-ux-pro-max, 44x44px floor); bidirectional | PASS |
| H1 | orchestrate `:62` (accent colour via H2 means) → ui-ux-pro-max concept + slop-checklist sprawl check (ACCENT_F22: ui-ux-pro-max ×1, slop-checklist ×3, unslop-fixes ×3); D11 points at it | H1 is the concept, D11 the fix — not duplicated | PASS |
| H2 | orchestrate `:62` "Accent hierarchy in every UI slice brief (ACCENTUATION_F22)" → ui-ux-pro-max hierarchy rules → slop-checklist hierarchy check (ACCENTUATION_F22 ×6, 5 files) | F5/dealt-moments/H1 recorded as accentuation means under H2, cross-referenced not duplicated | PASS |
| §9 Mobbin | orchestrate `:64` (MOBBIN_RESEARCH_F22) category-level research step + record requirement + no-copy boundary + free-tier + never-blocked → Taste `:463` + ui-ux-pro-max `:170` pattern reference → polish-pass step 8 QA convention check (MOBBIN_QA_F22, `:106`) | No Mobbin URL as a design source anywhere; recorded-gap fallback for unreachable/paywalled | PASS |
| §10 Directives | orchestrate `:72` "Directives, not descriptions (DIRECTIVES_F22)" in every implementer brief → Taste step 4a (×2, `:258`/`:405`) + ui-ux-pro-max `:262` + GAN planner `:46` / generator `:32` / evaluator `:134` + polish-pass `:102` (DIRECTIVES_F22 ×8, 7 files) | Every §10 rule carries its D19 parenthetical; prose-only FAILS the handoff check; ambiguity → recorded gap | PASS |
| §11 Libraries | Lenis → motion-foundations `:273` (`lenis@1.3.27` MIT) + motion-patterns + ui-ux-pro-max `:422`; GSAP → ui-ux-pro-max `:322–346` (`--domain gsap`, 17 presets intact, `gsap@3.15.1`) + ScrollTrigger motion-patterns `:553`; Vanta → Taste `:127` (`vanta@0.5.24` MIT + `three@0.134.0`) + ui-ux-pro-max `:176–177`; React Bits → motion-patterns `:724` (React-only) | Pins/licences/scopes in §7; reduced-motion + mobile fallback + scrim stated for Vanta; unpinned "latest" FAILS the pin check | PASS |
| §12 Bang | pitch-deck-video staged source `new-skills/pitch-deck-video/SKILL.md` **identical** to built (830 lines, BANG_* at `:247/:281/:304/:337/:373/:409` in both); /demo command loads the skill | Anti-slide as structural checks; one-world/camera/persistent-subject architecture; 10 style directions + 19 openers as menus (look from brand/theme deal); kinetic type as directives; explainer styles inform How beats. /demo still films the LOCAL app; no second toolchain. (Template invocation form is now the `-p` form — see Prior findings.) | PASS (weaving); (b) never-automatic is §3, PASS |
| §13 Depth | orchestrate `:66` "Depth strategy in every UI slice brief (DEPTH_F22)" + `:108` "Depth strategy recorded with the direction" → ui-ux-pro-max depth rules → motion-foundations/patterns 3D motion (`:450` 3D motion rules) → Taste dealt moments (`:129`) → polish-pass depth check (slop-checklist depth section) | Seventh-dimension extension line immediately after the frozen D19 line in both homes (§8); `flat by choice — <reason>` satisfies the dimension; depth/texture overlap recorded (less-flat-ui hunk 6, `:566–568`) | PASS |
| §14 Orbs | orchestrate `:64` "Waiting states in every UI slice brief (ORBS_F22)" → motion-patterns orb pattern (`:334`, pin `thinking-orbs@0.3.2` MIT; `:342` nine verified states, NO "thinking" state; `:347–355` state table; `:357–362` correction to the SPEC §14 draft mapping) → motion-foundations tokens (sizes 64/20, monochrome, reduced-motion frozen frame, offscreen/hidden pause, DPR ≤2) → ui-ux-pro-max `:122` component rules → polish-pass check | State-matched, never decorative; generic spinner FAILS; `thinking-orbs@0.3.2` MIT pinned. RareFormLabs note: recorded as unresolved in `fix22/orbs-patches.md:520–525`; SPEC §14 requires the note in the MANIFEST — still open with the MANIFEST itself (§9). Never invented a link. | PASS |
| §15 Libraries | R3F → Taste `:135` + motion-foundations `:152–157` (pairing rule) + motion-patterns; liquid-glass-js → Taste `:136` + less-flat-ui hunk 5 + ui-ux-pro-max `:451–452`; ShaderGradient → Taste `:134` + ui-ux-pro-max `:447` (v2, NOT legacy v1.3.5); liquid-logo → Taste step 4a `:435` (label home) + ui-ux-pro-max `:237–257` | One-WebGL-per-surface rule (`WEBGL_ONE_F22`, 9 occ., 6 files) incl. Casberry extension; R3F v8↔React 18 / v9↔React 19 pairing enforced; ShaderGradient customize-URL is the config; liquid-logo standalone tool + static fallback + attribution | PASS |
| §16 Vercel | polish-pass SKILL.md `:98–99` ("read the Vercel checklist … on every pass", candidate evidence only) → vercel-checklist.md (pinned commit `4ecfb9fb8d1d3b7009674869b3aaee2f904042e1`, 2026-10-05, ECC pinned-snapshot form, refresh on explicit request only) → pointers in ui-ux-pro-max quick-reference (×3) + motion-foundations `:212` | Dedupe 136/0 (§5); license gap recorded (skill repo NO LICENSE file; rules repo MIT); ECC-source check recorded (vercel-checklist `:20–27`); live-fetch absent (§8) | PASS |
| §17 Libraries | Casberry → motion-foundations `:90` + Taste `:138` + motion-patterns + ui-ux-pro-max; OriginKit → Taste `:139` + motion-patterns + ui-ux-pro-max; daisyUI → design-system `:35` + Taste + ui-ux-pro-max `:501–514` | Casberry: standalone tool, export reviewed as untrusted code, terms unresolved, one-WebGL rule covers exports; OriginKit: 10/day cap, Pro-marked excluded, Origin UI distinction, env-only key, no MCP wiring; daisyUI: 5.x + Tailwind v4 pinned, default-theme-unexamined FAILS | PASS |

**Weaving-coherence verdict: CLEAN.** No §1–§17 item is only appended;
every item is encountered at its SPEC'd step with its D19 reason and §10
directive form intact, pointers resolve bidirectionally where required,
and nothing is duplicated elsewhere.

## 5. Disposition — 144/144 by content (line numbers drifted, as before)

`fix22/disposition-merged.md`: **148 data rows = 144 items (A1–G20 + H1 +
H2) + 4 process rows** (Mobbin §9, Directives §10, Libraries §11, Bang
§12). An independent script checked every row's content against its cited
home file in the current built tree (word-match on the item name, anchor
fallback where the name is prose): **0 failures — 144/144 by content**.
Every item id A1–G20 + H1 + H2 is present exactly once in the table. The
disposition header is frozen at the Audit #67 build (`build.sh` 23,732
lines, md5 `891fca7b…`), so cited line numbers have drifted mechanically
(inserts since moved lines down); the drift is not a finding — same
treatment as Sweep #30b §5 — but the coordinator's still-unwritten
`fix22/MANIFEST.md` (SPEC §6.8) is where current-build placements must be
recorded (see §9).

**Vercel dedupe** (`fix22/vercel-dedupe.md`): **136 rule rows, 136 unique
rule ids, 0 unaccounted** — independently re-derived. Dispositions:
already-covered 14, partial 38, new 70 (incl. V-AP1, the one
non-duplicate anti-pattern), duplicate-of 13, **conflict 1 (AG19)** = 136.
The single conflict, AG19 (APCA vs WCAG 4.5:1), is recorded for parent
adjudication (`vercel-dedupe.md:262, 280, 289`) and **not** resolved —
"Until then, WCAG 4.5:1 stands and APCA is not woven." (The word
"conflict" appears in 9 lines of the file, e.g. V-P6 `:124` "No conflict
with the fix #19/#20/#21 self-hosted-static-fonts rule" — disposition
**new**; AG19 is the only conflict disposition.) Sweep #30b Finding 2
stays fixed: "40x40px" occurs **0** times in the built tree and **0** times
in `vercel-dedupe.md`; "44x44px minimum, the plugin floor" occurs **2×**
in the dedupe file and **3×** in the built tree.

## 6. verify22 re-run + prior verifiers — PASS (allowed-fail pattern only)

```
cd ~/workspace/hackathon-plugin && python3 fix22/verify22.py
→ 368/368 checks pass (exit 0)
```

Prior verifiers re-run directly by this sweep, each failing **only** on the
frozen post-fix21 `build.sh` fingerprint (+ cascade lines, + the
less-flat-ui diff check where applicable) — exactly the allowed pattern:

| Verifier | Result |
|---|---|
| fix15 | 42/44 |
| fix17 | 58/60 |
| fix18 | 69/72 |
| fix19 | 71/76 |
| fix20 | 164/169 |
| fix21 | 96/102 |

No other failure in any prior verifier. (The `fix22/verify22.py` tail
records the same pattern as PASS lines, and prints the MANIFEST note with
the measured lines/md5.)

## 7. §13–§17 content intact — pins / licenses / scopes

Spot-verified pins/licenses/scopes in the built tree (all present as
specified): Lenis `lenis@1.3.27` MIT; GSAP `gsap@3.15.1` GreenSock
Standard "no charge", NOT MIT; Vanta `vanta@0.5.24` MIT +
`three@0.134.0` (general `three@0.185.1` scoped separately); R3F
`@react-three/fiber@9.8.2` (React 19) / `@8.18.0` (React 18) MIT;
liquid-glass-js commit `78cb6ccb…` MIT, no npm package; ShaderGradient
`@shadergradient/react@2.4.20` v2 (NOT legacy v1.3.5); liquid-logo commit
`689bb38a…` PolyForm Shield + `@paper-design/shaders-react` Apache 2.0;
thinking-orbs `thinking-orbs@0.3.2` MIT; Casberry standalone tool, terms
unresolved + trust flag + export review; OriginKit 10/day cap +
conditional licence + Origin UI distinction; daisyUI `daisyui@5.7.50`
MIT + Tailwind v4. Running total 11 libraries/tools (§11's 4 + §15's 4
+ §17's 3) present (`ui-ux-pro-max:523`). "GSAP 3.12.5" occurs **×2**,
both Bang-reference-only in pitch-deck-video (`SKILL.md:219, :245`) — "those
are Bang's versions as found, not the plugin pins" — as specified, §12.

## 8. Counts + staged-vs-built + standing rules — PASS

| Inventory | Count | How measured |
|---|---:|---|
| skills | **166** | `ls hackathon-ecc/skills \| wc -l` |
| agents | **72** | `ls hackathon-ecc/agents \| wc -l` |
| rules | **123** | `ls hackathon-ecc/rules \| wc -l` |
| commands | **87** | `ls hackathon-ecc/commands \| wc -l` |
| hooks | **15** | `len(json.load(open('hooks/hooks.json'))['hooks'])` |
| trigger keys | **64** | `manifests/context-packs/skill-triggers@1.json` `triggers`: 64 keys; after stripping the `skill:` prefix every key resolves to a real skill dir (0 unresolvable) |

| Check | Result |
|---|---|
| Banned terms (claude/codex/anthropic/opus/sonnet/haiku/composer-2.5, case-insensitive, built tree excl. `node_modules`) | **0** |
| Model pins | `grok-4.7-high` **54**, `cursor-grok-4.6-high-fast` **102**, bare `grok-4.6-high-fast` **0** — identical to Audit #67/#68 counts |
| Font rules | F4 tightened scope ("long body and small text only", "(F4 tight)") present in Taste step 4a + orch-build-mvp; F7 (every text element gets an artistic font decision) present; static instances only. |
| Screen-verdicts rule | Intact: slop checklist, unslop fixes, Vercel checklist, and depth check are all STATIC checks / candidate evidence, never verdicts (vercel-checklist `:6–9` states it explicitly; polish-pass `:98–99` same standing). |
| No new skill/command/trigger key | Counts above unchanged; `ls commands` = 87 |
| Stale strings in built tree | "142 items" 0, "23,647" 0, old md5 `8dfacb47` 0, superseded md5 `891fca7b` 0, "ScrollTrigger: 0" 0, "3.12.2" 0, "LIB-05" 0, "40x40px" **0**. "GSAP 3.12.5" ×2, both Bang-reference-only in pitch-deck-video (as specified, §12). |
| `liquid-glass-design` dangling reference | **0** in the built tree (resolved — liquid-glass-js fills the gap per SPEC §15 option (a)). The 4 hits in `build.sh` (`:18731`, `:19412`, `:19449`, `:19458`) are unchanged from `build.sh.before-fix22`: a governance/regression list noting the skill does not exist, not a live pointer. |
| Vercel live-fetch | **0** `raw.githubusercontent.com/vercel-labs` URLs anywhere in the built tree; no unpinned Vercel fetch instruction. Only two `raw.githubusercontent.com` hits in the tree, both pre-existing pinned codebase-memory install URLs (`DeusData/codebase-memory-mcp/v0.12.1`). |

Less-flat-ui: **23 treatments** (`skills/less-flat-ui/SKILL.md:103`
"## The 23 treatments"; #23 Soft Shadow). Staged-vs-built:
`new-skills/orchestrate/SKILL.md` byte-identical to built;
`new-skills/pitch-deck-video/SKILL.md` byte-identical to built (830
lines, BANG_* at `:247/:281/:304/:337/:373/:409` in both);
`new-skills/pitch-deck-video/template/scripts/build.mjs` and `qa.mjs`
byte-identical to built; staged `new-rules/hackathon-mode.mdc` differs
from built in **exactly one line** (`:38`): staged reads "its upstream
`` `claude -p` `` invocation path", built reads "its upstream
CLI-subprocess invocation path". **Checked and cleared, not a finding:**
the replacement is a documented build-time transformation — the fix #16
Claude/Codex scrub. The staged copy retains the pre-scrub wording; the
built tree is the sanitized artifact and carries 0 banned terms.

**D19 form:** the frozen fix #19 D19 rule line is **byte-identical** in
orchestrate and Taste — `orchestrate/SKILL.md:120` ==
`design-taste-frontend/SKILL.md:423` (2,090 chars each, compared by
Python `==`). The seventh-dimension extension line sits **immediately
after it in both homes** — `orchestrate:122` == Taste `:425` (923 chars
each, exact), with a blank line between (`:121`/`:424`). No "six
dimensions" text was rewritten.

**Less-flat-ui diff** (global `~/workspace/cursor-skills/less-flat-ui/SKILL.md`,
534 lines, vs built `hackathon-ecc/skills/less-flat-ui/SKILL.md`, 579
lines): **exactly 6 non-equal hunks** (difflib), as required — 4 Batch E
(design-decision pointer; wow-moment line; record-treatments line;
re-tint line) + 2 fix22 (LIQGLASS_F22 liquid-glass insert, built
`:143–182`; DEPTH-13 depth/texture note, built `:566–568`).

## 9. Open items (coordinator / parent steps before the fix closes)

1. **`fix22/MANIFEST.md` — still unwritten** (SPEC §6.8) — the sole open
   close step this sweep records. It must record: the disposition as built
   (current-build line numbers superseding the Audit #67-as-of record, §5),
   placement map, adjudication notes (§4a/§4b pairs, B3/B15/B4 token
   conflicts, C13 vs Impeccable eyebrow tension, AG19 APCA vs WCAG 4.5:1),
   glossary-home justification, counts before/after, verifier + audit +
   dry-run + sweep results, the rareformlabs-unresolved note, and the B-1
   behavior change the built tree already claims it records
   (`hackathon-mode.mdc:68`). Writing it closes the M-2 record-pointer
   with no rule-text change. Per the task, its absence is NOT a finding
   this round.
2. **Parent adjudications still open** (carried as recorded flags, none
   silently resolved): B3 30ms vs Rule 5 0.05s floor; B15 0.8× vs
   quick-reference ~60–70%; B4 0.97 vs `scale.press` 0.95; C13 vs
   Impeccable eyebrow tension; AG19 APCA vs WCAG 4.5:1; orbs "thinking"
   correction + pin 0.3.2 vs repo 0.3.1; GSAP 3.15.1 convergence + scoped
   Three.js pins; Bang staleness + Indonesian-language note; GSAP
   GreenSock Standard (NOT MIT) + React Bits MIT + Commons Clause licence
   deviations.
3. **Live /demo execution not run in this sweep** (read-only; no filming).
   The `-p` Remotion invocation form is verified textually at both call
   sites (staged + built, byte-identical) but was not live-executed here.
   A live `qa.mjs` stills run on this build would close that last
   execution gap; the dry-run #37 re-run's live probe evidence was on the
   bare form and is superseded by the fix.

## 10. Verifiers / dry-runs observed (not re-run by this sweep)

| Check | Result as observed |
|---|---|
| `fix22/verify22.py` (re-run by this sweep) | **368/368, exit 0** (§6) |
| Audit #67 | ZERO ERRORS (build then 23,732 lines / md5 `891fca7b…` — superseded) |
| Dry-run #36 | PASS 46/46 (per Audit #67 / Sweep #30) |
| Dry-run #37 | PASS — 42/42 fixture expectations + 35/35 /demo contract checks |
| Dry-run #37 re-run (prior build) | **FAIL — 50/51 demo checks**, the 1 FAIL being the bare-npx live invocation (sweep #30b re-run Finding 1). That finding is fixed in this build (§Prior findings); no dry-run re-run against this build was in this sweep's scope. |

## 11. Findings

None. 0 blocking, 0 minor.

## 12. Commands used (full list)

```
md5sum build.sh build.sh.before-fix22 ; wc -l build.sh build.sh.before-fix22
diff build.sh.before-fix22 build.sh (hunks + counts)
python3 fix22/verify22.py
python3 fix15/verify15.py ; fix17/verify17.py ; fix18/verify18.py ; fix19/verify19.py ; fix20/verify20.py ; fix21/verify21.py (full + tail)
python3 /tmp/sweep30c.py (anchor table, DEMOGATE in build.sh, /demo string checks, banned terms, grok pins, D19 equality, less-flat-ui difflib, staged-vs-built, disposition row counts, vercel-dedupe rows, remotion counts, Vercel live-fetch, weaving spot strings)
python3 /tmp/sweep30c-disp.py (disposition content check per row, trigger-key resolution, D19 precise lines, less-flat-ui hunks, vercel-dedupe recount)
grep -rn (targeted: DEMOGATE tokens incl. build.sh; '40x40px'/'44x44px minimum'; 'required deliverable'; 'Film via'/'re-film'; hooks 'demo'; orchestrate :56/:58/:62/:64/:72/:80/:82/:327/:344; orch-build-mvp skill :32/:83/:84 + command :36; orch-change-feature skill :51/:52 + command :25; hackathon-mode :12/:22/:59/:61/:68; dispatch-prompt.md:29; commands/demo.md:13; deploy-fast/readme-writer/hackathon-pitch/fastapi-patterns/feature-expansion 'demo' lines; BANG_* lines; F1–F6/$10/A-V-table/theme.source; pins/licenses; AG19; V-AP1; 'fix22/MANIFEST.md'; 'CLI-subprocess'/'claude -p'; trigger-key resolution; D19 lines :120/:122 vs :423/:425; less-flat-ui hunks; '142 items'; old md5s; 'GSAP 3.12.5'; 'liquid-glass-design')
ls fix22/MANIFEST.md
diff new-rules/hackathon-mode.mdc hackathon-ecc/rules/hackathon-mode.mdc ; diff new-skills/orchestrate/SKILL.md … ; diff new-skills/pitch-deck-video/SKILL.md … ; diff new-skills/pitch-deck-video/template/scripts/build.mjs … ; diff new-skills/pitch-deck-video/template/scripts/qa.mjs …
sed -n (hackathon-mode :12/:18-26/:60-72; build.mjs:330-340; qa.mjs:38-48; motion-foundations :52/:312/:320; motion-patterns :340-360; Taste :374-396; polish-pass :96-106)
python3 -c (D19 byte-compare; orchestrate :56/:62/:64/:72 anchor extraction; trigger keys 64 + resolution)
```
