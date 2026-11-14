# Sweep #30b RE-RUN — fix #22 confirmation re-sweep (hackathon-ecc)

**Verdict: SWEEP #30b RE-RUN: FINDINGS — 1 blocking + 2 minor.** The /demo
auto-invocation removal is verified complete at all 6 sites + all follow-ups
(19/19 DEMOGATE tokens, each exactly once in the built tree; no remaining
auto-invocation), Sweep #30b Finding 2 (stale hit-area wording) is fixed in
all 3 places, the weaving-coherence pass is CLEAN, verify22 re-runs
**368/368**, and the build fingerprint matches the task statement exactly.
The blocking finding is new and was NOT in the task's text-level check: the
Remotion fix changed the package specifier but kept a bare-`npx` invocation
form that cannot execute — `@remotion/cli` exposes three binaries, so
`npx @remotion/cli@4.0.526 <cmd>` fails live with "could not determine
executable to run" at both call sites (`qa.mjs:42`, `build.mjs:335`). The
dry-run #37 re-run found the same defect live (its verdict is FAIL, 50/51);
this sweep independently re-verified it from the installed package manifest
and the live probe/QA logs. The two minor findings are stale wording left by
the removal: orch-build-mvp's narration-key paragraph still assumes a video
will be filmed, and hackathon-mode cites a `fix22/MANIFEST.md` that does not
exist yet.

**Scope:** built tree `~/workspace/hackathon-plugin/hackathon-ecc/`
(`node_modules/` excluded everywhere), `build.sh`, staged sources
(`new-skills/`, `new-rules/`, `round2-skills/`), and the fix22 working files.
SPEC read first (`fix22/SPEC.md` §§1–17); Sweep #30b report, Audit #68
report, `fix22/PARENT-GUIDANCE.md`, and `fix22/parent-addendum-nov12.md`
read before checking. Method: every number below was re-derived by running
the greps/commands shown in §12; nothing was copied from Audit #67/#68,
Dry-run #36/#37, the dry-run #37 re-run, or the coordinator's reports
without re-running — except where explicitly marked as corroboration.
This sweep made no plugin change (read-only); its only write is this report.
No `bash build.sh` run, no bundle/commit/push, no message sent.

**Given state (measured by this sweep):** `build.sh` **23,773 lines, md5
`e9462b57429acd914cd0aacdebc486d0`**; pre-fix22 baseline
`build.sh.before-fix22` 23,647 lines, md5
`8dfacb47a2a6698d47e4b4a5f8d9126c` — diff **+126/−0, exactly 2 hunks**
(§4). Counts 166 skills / 72 agents / 123 rules / 87 commands / 15 hooks;
64 trigger keys, all resolving. `fix22/verify22.py` re-run by this sweep:
**368/368, exit 0**.

---

## Findings

### Finding 1 (BLOCKING) — Remotion invocation form cannot execute: bare `npx @remotion/cli@4.0.526 <cmd>` has no resolvable binary

- **Files:**
  - `hackathon-ecc/skills/pitch-deck-video/template/scripts/qa.mjs:42`
  - `hackathon-ecc/skills/pitch-deck-video/template/scripts/build.mjs:335`
- **Actual text (read from the built tree):**
  - `qa.mjs:42`: `execFileSync('npx', ['@remotion/cli@4.0.526', 'still', 'src/index.ts', 'Demo', file, `--frame=${p.frame}`, '--log=error'], {`
  - `build.mjs:335`: `run('npx', ['@remotion/cli@4.0.526', 'render', 'src/index.ts', 'Demo', 'out/demo.mp4',`
- **Expected:** an invocation form npm can resolve to an executable — e.g.
  `npx -p @remotion/cli@4.0.526 remotion still|render …` (explicit binary
  after `-p`) or the locally installed bin (`npx --no-install remotion
  still|render …`, available because the template pins `@remotion/cli`
  `4.0.526` in its `package.json:15`).
- **Why the actual form fails:** npm's `npx <package>@<version> <args>`
  resolves the executable from the package manifest's `bin` field, and when
  `bin` is an object with multiple entries it cannot pick one. Verified
  from the package actually installed by the dry-run re-run's live
  `npm install` (`fix22/dryrun37-rerun/demo-sample-video/node_modules/`):
  `@remotion/cli@4.0.526` `package.json` `bin` =
  `{"remotion": "remotion-cli.js", "remotionb": "remotionb-cli.js",
  "remotiond": "remotiond-cli.js"}` — **three bins** — while the `remotion`
  package itself has `bin: None` (confirming the original diagnosis that
  the `remotion` package carries no executable, and that the specifier
  change alone does not fix executability).
- **Live failure, independently verified from the logs (not only the
  re-run report):**
  - `fix22/dryrun37-rerun/remotion-still-probe.log` (tail): `npm error
    could not determine executable to run` — the exact bare-npx form,
    probed live.
  - `fix22/dryrun37-rerun/qa-run.log`: `qa.mjs` itself exits 1 on
    `Command failed: npx @remotion/cli@4.0.526 still src/index.ts Demo
    …/out/qa/00111_problem.png --frame=111 --log=error` with the same npm
    error.
  - The working forms were verified live in the same session:
    `fix22/dryrun37-rerun/remotion-p-help.log` (`npx -p
    @remotion/cli@4.0.526 remotion --help` → exit 0, prints
    `@remotion/cli 4.0.526`) and `remotion-local-help.log` (`npx
    --no-install remotion --help` → exit 0, same).
- **Scope of the defect:** only these two call sites use the bare form
  (grep for `@remotion/cli` over the whole pitch-deck-video tree returns
  exactly: `package.json:15` pin, `remotion.config.ts:1` import,
  `build.mjs:335`, `qa.mjs:42`). `build.mjs:335` was not reached live
  (filming blocks first — no browser binary in the environment, see §11),
  but the invocation form is identical to `qa.mjs:42` and was probed live
  with `still`, so it fails identically.
- **What the task's text-level check DID pass (recorded, not disputed):**
  the built tree has **0** `remotion@4.0.542` and both scripts use
  `@remotion/cli@4.0.526`; the version matches the template pin. The
  defect is the invocation form, which a text check cannot catch.
- **Why blocking:** /demo's render step (`build.mjs` — the `npm run all`
  pipeline) and its QA-stills step (`qa.mjs` — the F5 A/V-table stills)
  cannot run as written. /demo contract gate (c) therefore fails live
  execution, not just wording. Fix: the coordinator picks one working form
  and applies it at both call sites, then the dry-run re-run's
  `demo-remotion-npx-live` check is re-run against the corrected form.
  This sweep does not fix it (read-only).

### Finding 2 (minor) — orch-build-mvp narration-key paragraph still assumes a video will be filmed

- **File:** `hackathon-ecc/skills/orch-build-mvp/SKILL.md:32` (1,855-char
  mega-line; the narration-key prompt paragraph at the start of the
  standalone run).
- **Actual text (verbatim excerpts):** "At the start of the run (step 1),
  **if narration will need a key** and none is set … issue the single
  `pitch-deck-video` narration-key prompt once … and **if it never arrives
  the video renders music-only/silent** with a note in the final report."
  / "**Do NOT re-prompt at step 8 `/demo` time:** the single early prompt
  covers the run, and `/demo` uses the key if present, else falls back to
  music-only/silent." / "**Key handoff to step 8:** … pass it to the
  **step-8 `/demo`** via the dispatch … If the key arrives after step 8
  already rendered but before the step-9 final report, re-run the video
  script step … so the delivered video is the narrated cut".
- **Expected:** the prompt's trigger tied to the user having asked for a
  video — the form the removal used everywhere else, e.g. orchestrate
  step 0 (`SKILL.md:58`): "ONLY when the user asked for a demo video …
  If the user did NOT ask for a demo video, do NOT send this prompt — no
  video is being built, so no key is needed". Step 8 itself now gates
  filming correctly ("Do NOT film via `/demo` here — `/demo` runs ONLY
  when the user invokes it explicitly … If no video was requested, the
  final report notes that no demo video was filmed", DEMOGATE_B2S1/B2S2).
- **Why minor, not blocking:** nothing in :32 instructs filming — it is a
  prompt + key-handoff description, and step 8 is the gate. But :32 was
  written for the old always-film flow and was not updated by the removal:
  "if narration will need a key" is never defined as "the user asked for
  a video", and "the video renders music-only/silent" / "step 8 `/demo`
  time" / "Key handoff to step 8" presuppose a video will be filmed. An
  agent can reasonably read :32 as licensing the key prompt (a
  user-facing prompt) on a run where no video was ever requested. Fix:
  condition the paragraph on the user having asked for a demo video, and
  reword the step-8 references as conditional ("if a video was
  requested"). The command file (`commands/orch-build-mvp.md`) has no
  narration-key section, so no parallel fix is needed there.

### Finding 3 (minor) — hackathon-mode cites a `fix22/MANIFEST.md` that does not exist

- **File:** `hackathon-ecc/rules/hackathon-mode.mdc:68` (DEMOGATE_H1_F22
  line): "… The demo video is no longer a required deliverable of the
  first build — **the behavior change is recorded in
  `fix22/MANIFEST.md`**."
- **Actual:** `fix22/MANIFEST.md` does not exist (`ls` fails; it was
  already unwritten at Audit #68 time and still is). It is the only
  `fix22/MANIFEST.md` reference in the built tree (grep over the tree
  returns this line alone).
- **Expected:** the referenced record exists, or the sentence is phrased
  as a forward obligation ("to be recorded in `fix22/MANIFEST.md` when
  it is written").
- **Why minor:** writing the manifest is already a close criterion
  (SPEC §6.8; parent-addendum §4), so this resolves when the manifest is
  written — but as of this sweep the built tree asserts a record that
  cannot be checked. Carried as Finding 3 rather than a bare open item
  because the claim is in the shipped rule text, present tense.

---

## 1. Sweep #30b + Audit #68 findings — all verified FIXED

| Prior finding | Re-check by this sweep |
|---|---|
| Sweep #30b Finding 1 — /demo auto-invoked at 4 sites (orchestrate 5d, orch-build-mvp step 8 skill+command, hackathon-mode §7) | **FIXED.** All four sites now carry the never-automatic gate: orchestrate `SKILL.md:80` (DEMOGATE_O4_F22, "`/demo` … is NEVER dispatched by this pipeline"), orch-build-mvp `SKILL.md:83` (DEMOGATE_B2S1/B2S2, "`/demo` is not filmed here … Do NOT film via `/demo` here"), `commands/orch-build-mvp.md:36` (DEMOGATE_B2C1_F22), hackathon-mode `§7` `:68` (DEMOGATE_H1_F22, "does NOT film `/demo` automatically"). See §3 for the full site table. |
| Audit #68 B-1 — orchestrate step 5d + hackathon-mode mandate | **FIXED** (same sites as above; hackathon-mode `:68` + `:12` sequence both gated). |
| Audit #68 B-2 — orch-build-mvp step 8 | **FIXED** (skill `:83` + command `:36`; step 9 carve-out timing now "after deploy/commit/README", DEMOGATE_B2S6_F22, at `SKILL.md:84`). |
| Audit #68 B-3 — orch-change-feature re-film | **FIXED.** Skill `:51` now reads "If the user asks for a re-film, re-film via `/demo --rebuild` … (The poll verifies the redeploy; it is not a prelude to filming — no re-film happens here.)" (DEMOGATE_B3S1_F22); done-condition is "re-filmed video (if the user asked) + honest hosting note, or stale-video record when no re-film was requested — never by an automatic re-film" (DEMOGATE_B3S5_F22); command `:25` now reads "re-film with `/demo --rebuild` only when the user asks" (DEMOGATE_B3C1_F22). |
| Sweep #30b Finding 2 — stale hit-area "40x40px, ideally 44x44px" in 3 places | **FIXED.** `vercel-checklist.md:175` now reads "plugin hit-area rule (44x44px minimum, the plugin floor — Group A A14 / G8)"; `fix22/vercel-dedupe.md:67` (V-FO6) and `:244` (AG1) both now read "44x44px minimum, the plugin floor — Group A A14 / G8". String "40x40px" occurs **0** times in the built tree and **0** times in `vercel-dedupe.md`. |
| Sweep #30 Finding 1 — `ANIM_TOKENS_F22` / `ANIM_RULES_F22` / `ANIM_ADV_F22` orphaned (0 hits) | Still fixed: each occurs 1× in its home file and 1× in `build.sh` (§2). |
| Sweep #30 Finding 2 — SPEC §6.1 "all 142 items" | Still fixed: `SPEC.md:255` reads "all 144 items accounted for". |

---

## 2. Anchor table — all 56 tokens resolve (occurrence counts)

Counts are substring occurrences in the built tree (excl. `node_modules`)
and in `build.sh`. "Home" = the file carrying the rule text; other files
are pointers / cross-references, the established pattern. Zero-token rows:
none. Total is **56 = 37 pre-demogate + 19 DEMOGATE** — note: Sweep #30b
said "38 tokens" but its own table lists 37 rows; this sweep re-derived
37, so the "38" was a miscount in that report, not a lost token. (Also:
`SLOP_F22`'s tree count of 28 includes its occurrences inside
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
| `MOBBIN_PATTERN_F22` | 2 (2) | 1 | Taste `:445`, ui-ux-pro-max `:167` |
| `MOBBIN_QA_F22` | 1 (1) | 0 | polish-pass `:106` |
| `DIRECTIVES_F22` | 8 (7) | 4 | All 8 required locations (§10) |
| `LENIS_F22` | 4 (3) | 4 | motion-foundations `:273` |
| `GSAP_F22` | 2 (1) | 2 | ui-ux-pro-max `:322–346` |
| `SCROLLTRIGGER_F22` | 4 (3) | 4 | motion-patterns `:429` |
| `VANTA_F22` | 10 (3) | 5 | Taste `:127` (+ pointers) |
| `REACTBITS_F22` | 5 (2) | 5 | motion-patterns `:552` |
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

All 19 DEMOGATE tokens occur **exactly once** in the built tree. 15 of
them occur in `build.sh` (the B2/B3 runtime patches, `build.sh:23733–
23747`); the 4 that do not (`O4`, `O9`, `H1`, `H2`) live in staged sources
installed by `cp` — `new-skills/orchestrate/SKILL.md` and
`new-rules/hackathon-mode.mdc` — not in the fix22 runtime block. That is
expected, not a gap: staged `new-skills/orchestrate/SKILL.md` is
byte-identical to the built copy, and staged `new-rules/hackathon-mode.mdc`
matches the built copy on every line except `:38` (see §8, checked and
cleared — a documented build-time fix16 scrub, not a fix #22 divergence).
No duplicate anchor definitions; the Sweep #30 finding-1 class (orphaned
anchors) is absent — every anchor resolves, each home file carrying its
anchor ×1. 0 in `build.sh` for `TRENDS_F22`, `MOBBIN_RESEARCH_F22`,
`MOBBIN_QA_F22`, and all six `BANG_*` tokens is expected (staged-source
installs, not fix22 patch-block text).

---

## 3. /demo never-automatic re-check — PASS (modulo Finding 2)

Grep-verified over the whole built tree (excl. `node_modules`), then
full-context reads of every file that mentions `/demo` or
`pitch-deck-video`:

| Check | Result |
|---|---|
| "filmed by default" | **0** |
| "deploy → demo" | **0** |
| "deploy/demo" | **1** — `README.md:40` only: "deploy/demo/orchestration workflows" — a capability phrase in a list, not a sequence. Acceptable, as specified. |
| "required deliverable" | **2** — (1) hackathon-mode `:68`, the H-1 negation ("no longer a required deliverable"); (2) `pitch-deck-video/template/src/Video.tsx:15`, a pre-existing template comment ("Audio guards — the video is a required deliverable and must NEVER abort on a missing audio file") — staged source `new-skills/pitch-deck-video/template/src/Video.tsx:15` is byte-identical, so this predates fix #22 and describes the video's own audio guards once /demo runs, not a pipeline invocation. Checked and cleared, not a finding. |
| "demo video →" | **1** — orchestrate `SKILL.md:56` only, the O-1 conditional sequence: "narration-key prompt — only when the user asked for a demo video → scope → expansion … → deploy → README → final report". |
| "Film via `/demo`" / "then film via `/demo`" | **0** |
| "re-film via `/demo --rebuild`" | **1** — orch-change-feature `SKILL.md:51` only, conditional: "If the user asks for a re-film, re-film via `/demo --rebuild`". |
| Hooks invoking /demo | **0** "demo" hits in `hackathon-ecc/hooks/` |

**The 6 removal sites + follow-ups, each read in full context:**

| Site | Current text (built tree) | Verdict |
|---|---|---|
| orchestrate step 5d, `SKILL.md:80` | "**Demo — never automatic (fix #22 /demo gate, DEMOGATE_O4_F22).** `/demo` … is NEVER dispatched by this pipeline. It runs ONLY when the user invokes `/demo` explicitly (or the user's request explicitly asks for a demo video). … If no video was requested, the final report notes that no demo video was filmed." | Gate present |
| orchestrate step 0 narration-key prompt, `SKILL.md:58` | "ONLY when the user asked for a demo video; it never blocks the build. … If the user did NOT ask for a demo video, do NOT send this prompt — no video is being built, so no key is needed" | Conditional |
| orchestrate step 6 Order, `SKILL.md:82` | "Order: verify → polish → deploy → commit → README → final report. (A demo video is filmed only when the user invokes `/demo` explicitly — it is never part of this order; fix #22 /demo gate, DEMOGATE_O9_F22.)" + README input conditional ("if a video was filmed, the video file path … as inputs") | Gate present |
| orchestrate sequence + final report, `SKILL.md:56`, `:327`, `:344` | Sequence "verify → polish → deploy → README → final report"; "… (A demo video is filmed only when the user invokes `/demo` explicitly — it is never part of this sequence …)"; demo-video handoff "only if a video was filmed" | Gate present |
| orch-build-mvp skill step 8, `SKILL.md:83` | "**Demo — never automatic (… DEMOGATE_B2S1_F22).** `/demo` is not filmed here. … Do NOT film via `/demo` here — `/demo` … runs ONLY when the user invokes it explicitly … If the user asked for one, film the LOCAL app … If no video was requested, the final report notes that no demo video was filmed. (… DEMOGATE_B2S2_F22)" | Gate present |
| orch-build-mvp skill step 9, `SKILL.md:84` | Carve-out timing "after deploy/commit/README" (DEMOGATE_B2S6_F22); handoff "if a video was filmed" / "If no video was filmed, the report notes that instead" (DEMOGATE_B2S4/B2S5_F22) | Gate present |
| orch-build-mvp command step 8, `commands/orch-build-mvp.md:36` | "Do NOT film via `/demo` here — `/demo` runs ONLY when the user invokes it explicitly (or the user's request explicitly asks for a demo video); if the user asked for one, film the LOCAL app … (… DEMOGATE_B2C1_F22)" | Gate present |
| orch-change-feature skill step 5, `SKILL.md:51` | Re-film only "If the user asks for a re-film" (DEMOGATE_B3S1_F22); "(The poll verifies the redeploy; it is not a prelude to filming — no re-film happens here.)"; done-condition "re-filmed … (if the user asked for a re-film) + honest hosting note, or … stale-video record when no re-film was requested — never by an automatic re-film" (DEMOGATE_B3S5_F22) | Gate present |
| orch-change-feature skill step 6, `SKILL.md:52` | "demo video STALE — shows the removed feature; re-film with `/demo --rebuild` on request" if not re-filmed (DEMOGATE_B3S7_F22) | Gate present |
| orch-change-feature command, `commands/orch-change-feature.md:25` | "re-film with `/demo --rebuild` only when the user asks" (DEMOGATE_B3C1_F22) | Gate present |
| hackathon-mode §7, `rules/hackathon-mode.mdc:68` | "The first build does NOT film `/demo` automatically (… DEMOGATE_H1_F22). `/demo` … runs ONLY when the user invokes it explicitly … never as a pipeline step, never by default. … (deploy → README → final report)." | Gate present |
| hackathon-mode §1 sequence, `rules/hackathon-mode.mdc:12` | First-build sequence "grill → narration-key prompt (… only when the user asked for a demo video …) → scope → expansion → build → verify → polish → deploy → README → final report. /demo is never part of this sequence — it runs ONLY when the user invokes it explicitly (… DEMOGATE_H2_F22)." | Gate present |
| hackathon-mode §7 carve-out, `:61` | Exception text for the end-of-project run "immediately before the first build's final report … it runs once, after deploy/…" — the "after deploy/demo/commit/README" form is gone; current text is "after deploy/commit/README" (DEMOGATE_B2S6_F22 mirrors it in orch-build-mvp) | Fixed |
| `commands/demo.md:13` dispatch note | No longer names orchestrate 5d / orch-build-mvp step 8 as dispatchers: "If this /demo run was invoked with a narration key already provided (via the dispatch's Environment field as an `ELEVENLABS_API_KEY` env instruction), do NOT prompt again …" | Fixed |
| `orchestrate/references/dispatch-prompt.md:30–31` Environment field | "`ELEVENLABS_API_KEY=<redacted>` on a /demo dispatch when a narration key was received mid-build (orchestrate step 0 — only when the user asked for a demo video)" | Conditional |

**Checked and cleared (mentions, not invocations):** `deploy-fast/SKILL.md:21`
(live-demo vs filmed-video distinction), `hackathon-pitch/SKILL.md:3,32`
(pitch storyboard; "never the demo video itself"), `readme-writer`
(ledger video-path inputs, conditional on a video existing),
`fastapi-patterns` / `feature-expansion` (generic "demo" usage, no
`/demo`), `devpost-autofiller` (post-removal video-link check),
`.cursor-plugin/plugin.json` / `README.md` / manifests (command listings).
No hook, no post-build trigger, no finish-report step, and no other command
invokes /demo or pitch-deck-video automatically. **Any remaining
auto-invocation: none found.** The one residual is Finding 2 (a
narration-key prompt paragraph, not an invocation).

---

## 4. Build fingerprint + diff — PASS

- `build.sh`: **23,773 lines, md5 `e9462b57429acd914cd0aacdebc486d0`**;
  `build.sh.before-fix22`: 23,647 lines, md5
  `8dfacb47a2a6698d47e4b4a5f8d9126c`.
- `diff build.sh.before-fix22 build.sh`: **+126 / −0, exactly 2 hunks** —
  `41a42,46` (5 `BANG_PIN` lines; `BANG_PIN="c1aa65e921c970d858705fcb4a53a8294d1a4131"`
  at `build.sh:42`) and `23635a23641,23761` (the 121-line fix22 block,
  `build.sh:23641–23761`; header at `:23643`, DEMOGATE B2/B3 runtime
  patches at `:23733–23747`). No other line changed. (Sweep #30b's build
  was +111: the extra 15 lines since are the DEMOGATE B2S6 patch + the
  orchestrate/hackathon-mode staged edits + the template specifier change.)
- The fix22 block contains all 11 §13–§17 anchor tokens and the 15 B2/B3
  DEMOGATE patches; it appears exactly once. No duplicated rules (every
  home anchor ×1 in its home file, §2); dedupe pairs honored (§5, §9).

## 5. Disposition — 144/144 by content (line numbers drifted, as before)

`fix22/disposition-merged.md`: **148 data rows = 144 items (A1–G20 + H1 +
H2) + 4 process rows** (Mobbin §9, Directives §10, Libraries §11, Bang
§12). Every item's content is present in its cited home file in the
current built tree — **144/144 by content**. The 12 rows a naive
exact-phrase match flagged as "missing" were verified individually by
their distinctive content (all present): B1 ease-out rule
(`motion-foundations:219`, token `smooth` `:411`); B2 `dropdown: 0.2`
(`:404`, "dropdowns animate at 150–250ms"); B3 `staggerRow: 0.03`
(`:405`, with the Rule-5 conflict flag carried); B5 `stretch: 1.12`
(`:428`); B7 "Move along arcs" rule (`motion-patterns:96`); B10
`popover: 0.95` (`:427`); B15 `exitFactor: 0.8` (`:431`, with the
quick-reference conflict flag carried); B18 "Icon swaps: cross-fade with
opacity, scale, and blur" (`make-interfaces-feel-better:120`); H1 accent
colour (`ui-ux-pro-max:15–40`, ACCENT_F22); H2 accent hierarchy
(`orchestrate:62`, ACCENTUATION_F22); Mobbin (`orchestrate:64`,
MOBBIN_RESEARCH_F22); Libraries (`motion-foundations:273`, LENIS_F22 +
pins). **64 cited line numbers drifted** (content present at a nearby or
elsewhere line — e.g. A13–A20 cited `:217–281`, now `:312–376`; E1–E20
cited `:248–381`, now `:262–395`; F3–F22 cited `:145–452`, now
`+39` from the LIQGLASS insert). The drift is mechanical (inserts since
the Audit #67 build moved lines down); the disposition header is frozen
at that build (`build.sh` 23,732 lines, md5 `891fca7b…`). **Not a
finding** — same treatment as Sweep #30b §5 — but the coordinator's
still-unwritten `fix22/MANIFEST.md` (SPEC §6.8) is where current-build
placements must be recorded (see §11; Finding 3 is the built tree's
forward reference to it).

**Vercel dedupe** (`fix22/vercel-dedupe.md`): **136 rule rows, 0
unaccounted** — independently re-derived (154 `|`-starting lines = 18
table header rows + 136 rule rows). Dispositions: already-covered 14,
partial 38, new 70, duplicate-of 13, **conflict 1 (AG19)** = 136. (One
row, V-P6 `:124`, contains the word "conflict" in its text — "No conflict
with the fix #19/#20/#21 self-hosted-static-fonts rule" — disposition
**new**; it is not a second conflict.) The single conflict, AG19 (APCA vs
WCAG 4.5:1), is recorded for parent adjudication (`vercel-dedupe.md:262,
280, 289`) and **not** resolved — "Until then, WCAG 4.5:1 stands and APCA
is not woven." V-P6 (font preload) vs self-hosted fonts is recorded as
resolved (preload compatible with self-hosted fonts).

## 6. verify22 re-run + prior verifiers — PASS (allowed-fail pattern only)

```
cd ~/workspace/hackathon-plugin && python3 fix22/verify22.py
→ 368/368 checks pass (exit 0)
```

Prior verifiers re-run by this sweep, each failing **only** on the frozen
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

No other failure in any prior verifier. (The `fix22/verify22.py` tail
records the same pattern as PASS lines.)

## 7. Leftovers + standing rules — PASS

| Check | Result |
|---|---|
| Banned terms (claude/codex/anthropic/opus/sonnet/haiku/composer-2.5, case-insensitive, built tree excl. `node_modules`) | **0** |
| Model pins | `grok-4.7-high` **54**, `cursor-grok-4.6-high-fast` **102**, bare `grok-4.6-high-fast` **0** — identical to Audit #67/#68 counts |
| Font rules | F4 tightened scope ("long body and small text only", "(F4 tight)") present in Taste step 4a + orch-build-mvp; F7 (every text element gets an artistic font decision) present; static instances only. (Same clarification as Sweep #30b §7: the literal token `F4_TIGHT` exists only in `fix21/SPEC.md`; the built tree carries the rule as "(F4 tight)" prose.) |
| Screen-verdicts rule | Intact: slop checklist, unslop fixes, Vercel checklist, and depth check are all STATIC checks / candidate evidence, never verdicts (vercel-checklist `:6–9` states it explicitly; polish-pass `:98–99` same standing). |
| No new skill/command/trigger key | Counts §8 unchanged; `ls commands` = 87 |
| Leftovers (word-boundary TODO/FIXME/XXX/HACK in the 19 F22-anchor files) | **0** (re-checked; same as Sweep #30b) |
| `LIB-05` in built tree / build.sh | **0** (referenced only as applied in fix22 working files) |
| Stale strings in built tree | "142 items" 0, "23,647" 0, old md5 `8dfacb47` 0, superseded md5 `891fca7b` 0, "ScrollTrigger: 0" 0, "3.12.2" 0, "LIB-05" 0, "40x40px" **0**. "GSAP 3.12.5" ×2, both Bang-reference-only in pitch-deck-video (as specified, §12). |
| `liquid-glass-design` dangling reference | **0** in the built tree (resolved — liquid-glass-js fills the gap per SPEC §15 option (a)). The 4 hits in `build.sh` (`:18731`, `:19412`, `:19449`, `:19458`) are unchanged from `build.sh.before-fix22`: a governance/regression list noting the skill does not exist, not a live pointer. |
| Vercel live-fetch | **0** `raw.githubusercontent.com/vercel-labs` URLs anywhere in the built tree; no unpinned Vercel fetch instruction. Only two `raw.githubusercontent.com` hits in the tree, both pre-existing pinned codebase-memory install URLs (`DeusData/codebase-memory-mcp/v0.12.1`). |

## 8. Counts + staged-vs-built — PASS (one checked-and-cleared divergence)

| Inventory | Count | How measured |
|---|---:|---|
| skills | **166** | `ls hackathon-ecc/skills \| wc -l` |
| agents | **72** | `ls hackathon-ecc/agents \| wc -l` |
| rules | **123** | `ls hackathon-ecc/rules \| wc -l` |
| commands | **87** | `ls hackathon-ecc/commands \| wc -l` |
| hooks | **15** | `len(json.load(open('hooks/hooks.json'))['hooks'])` (`ls hooks/` = 17 entries incl. `hooks.json` + `adapter.js`) |
| trigger keys | **64** | `skill-triggers@1.json` `triggers`: 64 keys; after stripping the `skill:` prefix every key resolves to a real skill dir (0 unresolvable) |

Less-flat-ui: **23 treatments** (`skills/less-flat-ui/SKILL.md:103`
"## The 23 treatments"; #23 Soft Shadow). Staged-vs-built:
`new-skills/orchestrate/SKILL.md` byte-identical to built;
`new-skills/pitch-deck-video/SKILL.md` byte-identical to built (830
lines, BANG_* at `:247/:281/:304/:337/:373/:409` in both); staged
`new-rules/hackathon-mode.mdc` differs from built in **exactly one line**
(`:38`): staged reads "its upstream `` `claude -p` `` invocation path",
built reads "its upstream CLI-subprocess invocation path". **Checked and
cleared, not a finding:** the replacement is a documented build-time
transformation — `fix22/build1.log:1454` (and `build2.log:477`) record
"`(its upstream `claude -p` invocation path …` -> `(its upstream
CLI-subprocess invocation path …`" applied to the built
`hackathon-mode.mdc` during the build (the fix #16 Claude/Codex scrub).
The staged copy retains the pre-scrub wording; the built tree is the
sanitized artifact and carries 0 banned terms. No other staged-vs-built
divergence was found in the files fix #22 touched.

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
`:144–182`; DEPTH-13 depth/texture note, built `:566–568`).

## 9. Weaving-coherence pass — CLEAN (per §1–§17)

For every §1–§17 item I verified: (i) it is reachable from the
design-package flow at its SPEC'd placement — orchestrate step 3
design-package-in-every-UI-slice-brief (`skills/orchestrate/SKILL.md:62`,
mega-line) → Taste step 4a / ui-ux-pro-max / motion-* / less-flat-ui /
polish-pass — with its D19 reason and its §10 directive form intact;
(ii) its pointers resolve (bidirectional where the SPEC requires); (iii)
it is not duplicated elsewhere. No item is only appended. Result by
section (line numbers are the current build's):

| Section | Flow entry point (SPEC'd placement) | Reachability / pointers | Result |
|---|---|---|---|
| §1–§3 A (A1–A20) | orchestrate `:62` "Motion principles in every UI slice brief (PRINCIPLES_F22 / LAWS_F22)" → motion-foundations Principles `:52–90` (A1 `:52`, A12 `:183`) + Decision Guidance `:312–376` (A13 `:312`, A14 `:320`) | make-interfaces-feel-better + ui-ux-pro-max point back to the laws; A7→B7, A8→B6, A2→B5/B19 cross-refs present | PASS |
| B (B1–B20) | Same brief line → motion-foundations tokens (`dropdown: 0.2` `:404`, `staggerRow: 0.03` `:405`, `stretch: 1.12` `:428`, `inOut`, `popover: 0.95` `:427`, `exitFactor: 0.8` `:431`) + motion-patterns Rules 11–19 + motion-advanced Rules 9–11/examples | Group anchors AB-03g/05g/09g resolve (§1); B4/B18 covered-evidence intact; B3/B15/B4 conflict flags carried, not resolved | PASS |
| C (C1–C20) | orchestrate Verify step → polish-pass SKILL.md `:98–99` ("read the slop checklist … on every pass") → slop-checklist anchor `:1–3`, all 20 indicators as flags with D19-reason + theme-fit clearance | Taste finish gate + Impeccable detector context point at the checklist; each fix pairs to unslop-fixes | PASS |
| D (D1–D20) | Same polish-pass step → unslop-fixes anchor `:1–3`, all 20 fixes (D1 `:58`); CD-P1–P7 pointers in quick-reference + motion-* | D11→H1, D20→A10/B8 family, D5/D8/D15 pointers (not restated) — §4 | PASS |
| E (E1–E20) | Taste step 4a trend menu (`TRENDS_F22` ×23 in Taste; E1 `:262`, E2 `:269`, E3 `:276`) — the design package MAY draw on it; 16 Hallmark Range lines in 15 theme files | E12/E14/E16 menu-only: no theme file carries an eyebrow, sparkle, or three-icon-cards line; E6 points at less-flat-ui #21, no duplication | PASS |
| F (F1–F22) | less-flat-ui catalogue, reached via orchestrate `:62` ("`less-flat-ui` where dull/flat") + Taste step 4a + R3 (≥2 distinct treatment kinds) | Verification-only: no text copied; all 22 + #23 Soft Shadow present (§5) | PASS |
| G (G1–G20) | One glossary file, reached from every owning skill: ui-ux-pro-max `:69`, motion-foundations `:710` (G18), motion-patterns `:999` (G10/G14/G20) — each "Design vocabulary — the definitions … live in `design-glossary.md` (`GLOSSARY_F22`)" | Glossary carries the owning-skill column per term (e.g. G1 Kerning `:20`, G8 → ui-ux-pro-max, 44x44px floor); bidirectional | PASS |
| H1 | orchestrate `:62` (accent colour via H2 means) → ui-ux-pro-max `:15–40` concept + slop-checklist `:419` sprawl check; D11 points at it | H1 is the concept, D11 the fix — not duplicated | PASS |
| H2 | orchestrate `:62` "Accent hierarchy in every UI slice brief (ACCENTUATION_F22)" → ui-ux-pro-max `:15` hierarchy rules → slop-checklist `:450` hierarchy check | F5/dealt-moments/H1 recorded as accentuation means under H2, cross-referenced not duplicated | PASS |
| §9 Mobbin | orchestrate `:64` (MOBBIN_RESEARCH_F22) category-level research step + record requirement + no-copy boundary + free-tier + never-blocked → Taste `:445` + ui-ux-pro-max `:167` pattern reference → polish-pass `:106` QA convention check (MOBBIN_QA_F22) | No Mobbin URL as a design source anywhere; recorded-gap fallback for unreachable/paywalled | PASS |
| §10 Directives | orchestrate `:72` "Directives, not descriptions (DIRECTIVES_F22)" in every implementer brief → Taste step 4a (×2) + ui-ux-pro-max `:219` + GAN planner `:46` / generator `:32` / evaluator `:134` + polish-pass `:100` | Every §10 rule carries its D19 parenthetical; prose-only FAILS the handoff check; ambiguity → recorded gap | PASS |
| §11 Libraries | Lenis → motion-foundations `:273` (`lenis@1.3.27` MIT) + motion-patterns + ui-ux-pro-max; GSAP → ui-ux-pro-max `:322–346` (`--domain gsap`, 17 presets intact, `gsap@3.15.1`) + ScrollTrigger motion-patterns `:429`; Vanta → Taste `:127` (`vanta@0.5.24` MIT + `three@0.134.0`) + ui-ux-pro-max `:176–177`; React Bits → motion-patterns `:552` (React-only) | Pins/licences/scopes in §10 below; reduced-motion + mobile fallback + scrim stated for Vanta; unpinned "latest" FAILS the pin check | PASS |
| §12 Bang | pitch-deck-video staged source `new-skills/pitch-deck-video/SKILL.md` **identical** to built (830 lines, BANG_* at `:247/:281/:304/:337/:373/:409` in both); /demo command loads the skill | Anti-slide as structural checks; one-world/camera/persistent-subject architecture; 10 style directions + 19 openers as menus (look from brand/theme deal); kinetic type as directives; explainer styles inform How beats. /demo still films the LOCAL app; no second toolchain. (The template's Remotion invocation defect is Finding 1 — a template-execution defect, not a weaving defect.) | PASS (weaving); (b) never-automatic is §3, PASS |
| §13 Depth | orchestrate `:66` "Depth strategy in every UI slice brief (DEPTH_F22)" + `:108` "Depth strategy recorded with the direction" → ui-ux-pro-max depth rules → motion-foundations/patterns 3D motion → Taste dealt moments → polish-pass depth check (`:101`, slop-checklist depth section) | Seventh-dimension extension line immediately after the frozen D19 line in both homes (§8); `flat by choice — <reason>` satisfies the dimension; depth/texture overlap recorded (less-flat-ui hunk 6) | PASS |
| §14 Orbs | orchestrate `:64` "Waiting states in every UI slice brief (ORBS_F22)" → motion-patterns orb pattern (`:334`, 9 repo-verified states, NO "thinking" state) → motion-foundations tokens (sizes 64/20, monochrome, reduced-motion frozen frame, offscreen/hidden pause, DPR ≤2) → ui-ux-pro-max `:122` component rules → polish-pass check | State-matched, never decorative; generic spinner FAILS; `thinking-orbs@0.3.2` MIT pinned. RareFormLabs note: recorded as unresolved in `fix22/orbs-patches.md:520–525`; SPEC §14 requires the note in the MANIFEST — still open with the MANIFEST itself (§11). Never invented a link. | PASS |
| §15 Libraries | R3F → Taste `:135` + motion-foundations `:152–157` (pairing rule) + motion-patterns; liquid-glass-js → Taste `:136` + less-flat-ui hunk 5 + ui-ux-pro-max; ShaderGradient → Taste `:134` + ui-ux-pro-max `:447` (v2, NOT legacy v1.3.5); liquid-logo → Taste step 4a `:435` (label home) + ui-ux-pro-max `:238/:248` | One-WebGL-per-surface rule (`WEBGL_ONE_F22`, 9 occ., 6 files) incl. Casberry extension; R3F v8↔React 18 / v9↔React 19 pairing enforced; ShaderGradient customize-URL is the config; liquid-logo standalone tool + static fallback + attribution | PASS |
| §16 Vercel | polish-pass SKILL.md `:98–99` ("read the Vercel checklist … on every pass", candidate evidence only) → vercel-checklist.md (453 lines, pinned commit `4ecfb9fb8d1d3b7009674869b3aaee2f904042e1`, 2026-10-05, ECC pinned-snapshot form, refresh on explicit request only) → pointers in ui-ux-pro-max quick-reference (×3) + motion-foundations `:212` | Dedupe 136/0 (§5); license gap recorded (skill repo NO LICENSE file; rules repo MIT); ECC-source check recorded (vercel-checklist `:20–27`); live-fetch absent (§7) | PASS |
| §17 Libraries | Casberry → motion-foundations `:90` + Taste `:138` + motion-patterns + ui-ux-pro-max; OriginKit → Taste `:139` + motion-patterns + ui-ux-pro-max; daisyUI → design-system `:35` + Taste + ui-ux-pro-max | Casberry: standalone tool, export reviewed as untrusted code, terms unresolved, one-WebGL rule covers exports; OriginKit: 10/day cap, Pro-marked excluded, Origin UI distinction, env-only key, no MCP wiring; daisyUI: 5.x + Tailwind v4 pinned, default-theme-unexamined FAILS | PASS |

**Weaving-coherence verdict: CLEAN.** No §1–§17 item is only appended;
every item is encountered at its SPEC'd step with its D19 reason and §10
directive form intact, pointers resolve bidirectionally where required,
and nothing is duplicated elsewhere.

## 10. §13–§17 content + Remotion fix — pins/licenses intact; invocation form FAILS (Finding 1)

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
+ §17's 3) present (`ui-ux-pro-max:523`).

**Remotion fix — text PASS, execution FAIL (Finding 1):** the built tree
has **0** `remotion@4.0.542`; `build.mjs:335` and `qa.mjs:42` both use
`@remotion/cli@4.0.526`; template `package.json:15` pins
`@remotion/cli` at `4.0.526`. The invocation form is the defect: bare
`npx @remotion/cli@4.0.526 <cmd>` cannot resolve because the package
exposes three binaries (verified from the installed manifest + live
probe/QA logs, §Finding 1).

**/demo (a) callable + (c) contract intact — text-verified (live film
not re-run by this sweep):** `hackathon-ecc/commands/demo.md` exists,
frontmatter "Generate a narrated product demo video, under 2:10… Use when
the user wants a demo video…", args `/demo`, `/demo <path>`,
`--rebuild/--script/--render/--montage/--explainer`; listed in the plugin
README (`:44–47`) and `.cursor-plugin/plugin.json`. Contract elements
spot-checked in `skills/pitch-deck-video/SKILL.md`: F5 per-beat A/V table
(`:199`, "A 'no' is a BLOCKING finding"; kinetic type and camera moves go
IN the table) + 10s mix listen (`:203`, `music.gain.under` 0.20 warn);
F6 under 2:10 hard rule / absolute max 2:30 (`:102`); F4 theme pull +
`theme.source` (`:98`, `:204`); $10 cap (`:805`, `:815`); local-only
filming (`commands/demo.md:11`, never a deployed URL). Staged pitch-deck-video
source == built tree (§8). **Limit, stated explicitly:** no live /demo
execution was run in this sweep (read-only; no build.sh runs, no
filming). The dry-run #37 re-run exercised it live: `tts.mjs` exit 0
(accepted the fixture `shots.json`); filming blocked by the environment
(no browser binary — Playwright CDN download fails at ~90%, same as the
first run); QA fails on Finding 1. So callability is established by
wiring + the re-run's live tts/record-entry evidence, NOT by a full live
film — and the render/QA path is blocked by Finding 1 (a plugin defect),
not by the environment.

## 11. Verifiers / dry-runs observed + open items (not findings, except Finding 3)

| Check | Result as observed |
|---|---|
| `fix22/verify22.py` (re-run by this sweep) | **368/368, exit 0** (§6) |
| Audit #67 | ZERO ERRORS (build then 23,732 lines / md5 `891fca7b…` — superseded) |
| Dry-run #36 | PASS 46/46 (per Audit #67 / Sweep #30) |
| Dry-run #37 | PASS — 42/42 fixture expectations + 35/35 /demo contract checks (`fix22/dryrun37-report.md` exists now; at Audit #68 time it did not) |
| Dry-run #37 re-run (new build) | **FAIL — 50/51 demo checks**: 42/42 fixtures, 35/35 original contract, 8/8 removal verification, 7/7 Remotion text/bin checks; **1 FAIL** — the bare-npx live invocation (Finding 1, `fix22/dryrun37-rerun/dryrun37-rerun-report.md` §5). This sweep independently re-verified that FAIL from the installed manifest + probe/QA logs. |
| `fix22/MANIFEST.md` | **Not yet written** (SPEC §6.8) — now also the subject of Finding 3 (hackathon-mode `:68` cites it as the record of the behavior change). |

**Open items (coordinator / parent steps before the fix closes):**
1. **Finding 1** — pick a working Remotion invocation form (`npx -p
   @remotion/cli@4.0.526 remotion …` or the local `remotion` bin), apply
   at `qa.mjs:42` + `build.mjs:335`, re-run the dry-run re-run's
   `demo-remotion-npx-live` check.
2. **Finding 2** — condition orch-build-mvp `SKILL.md:32` on the user
   having asked for a video; reword the step-8 references as conditional.
3. **Finding 3 / MANIFEST** — write `fix22/MANIFEST.md` (SPEC §6.8):
   disposition as built (current-build line numbers superseding the Audit
   #67-as-of record, §5), placement map, adjudication notes (§4a/§4b
   pairs, B3/B15/B4 token conflicts, C13 vs Impeccable eyebrow tension,
   AG19 APCA vs WCAG 4.5:1), glossary-home justification, counts
   before/after, verifier + audit + dry-run + sweep results, the
   rareformlabs-unresolved note, and the B-1 behavior change the built
   tree already claims it records.
4. **Audit #69** (next number) must confirm Findings 1–3 are fixed and
   return ZERO before the fix closes; the close criteria (parent-addendum
   §4) are otherwise met on the evidence above (verify22 100%, prior
   verifiers on the allowed pattern, banned terms 0, weaving-coherence
   CLEAN, /demo (a) callable / (b) never automatic / (c) contract intact
   as written).
5. **Parent adjudications still open** (carried as recorded flags, none
   silently resolved): B3 30ms vs Rule 5 0.05s floor; B15 0.8× vs
   quick-reference ~60–70%; B4 0.97 vs `scale.press` 0.95; C13 vs
   Impeccable eyebrow tension; AG19 APCA vs WCAG 4.5:1; orbs "thinking"
   correction + pin 0.3.2 vs repo 0.3.1; GSAP 3.15.1 convergence + scoped
   Three.js pins; Bang staleness + Indonesian-language note; GSAP
   GreenSock Standard (NOT MIT) + React Bits MIT + Commons Clause licence
   deviations.
6. **Live filming still blocked by the environment, not the plugin:**
   no browser binary on disk; Playwright's CDN download fails at ~90%
   (dry-run re-run §4). A machine with a working browser download would
   film the fixture as written. The A/V stills verification and the
   10-second mix listen remain owed on a real render.

## 12. Commands used (full list)

```
md5sum build.sh build.sh.before-fix22 ; wc -l build.sh build.sh.before-fix22
diff build.sh.before-fix22 build.sh (hunks + counts)
python3 fix22/verify22.py
python3 fix15/verify15.py ; fix17/verify17.py ; fix18/verify18.py ; fix19/verify19.py ; fix20/verify20.py ; fix21/verify21.py (full + '^FAIL' grep)
python3 /tmp/sweep30b-rerun.py (anchor table, DEMOGATE in build.sh, /demo string checks, banned terms, grok pins, D19 equality, less-flat-ui difflib, staged-vs-built, disposition row counts, vercel-dedupe rows, remotion counts, Vercel live-fetch, weaving spot strings)
python3 /tmp/sweep30b-disp.py (disposition content check per row)
grep -rn (targeted: DEMOGATE tokens incl. build.sh list; '40x40px'/'44x44px minimum'; 'required deliverable' incl. build.sh.before-fix22; 'demo video →'; 'Film via'/'re-film'; hooks 'demo'; orchestrate :56/:58/:80/:82/:327/:344; orch-build-mvp skill :32/:83/:84 + command :36; orch-change-feature skill :51/:52/:54 + command :25; hackathon-mode :12/:61/:68; dispatch-prompt.md:30-31; commands/demo.md:13; deploy-fast/readme-writer/hackathon-pitch/fastapi-patterns/feature-expansion 'demo' lines; BANG_* lines; F1–F6/$10/A-V-table/theme.source; pins/licenses; AG19; 'fix22/MANIFEST.md'; 'CLI-subprocess'/'claude -p' incl. fix22/build1.log:1454; trigger-key resolution; D19 lines :120/:122 vs :423/:425; less-flat-ui hunks)
python3 -c (trigger keys 64 + resolution; @remotion/cli + remotion bin fields from the dry-run re-run's installed node_modules; vercel-dedupe disposition recount; orch-build-mvp :32 substring positions)
ls fix22/MANIFEST.md ; ls fix22/dryrun37-report.md fix22/dryrun37-rerun/dryrun37-rerun-report.md
diff new-rules/hackathon-mode.mdc hackathon-ecc/rules/hackathon-mode.mdc ; diff new-skills/orchestrate/SKILL.md … ; diff new-skills/pitch-deck-video/SKILL.md …
sed -n (hackathon-mode :12/:61; Video.tsx:10-20; build.mjs:330-340; qa.mjs:38-46; make-interfaces-feel-better:115-125)
tail fix22/dryrun37-rerun/remotion-still-probe.log ; grep 'could not determine executable' fix22/dryrun37-rerun/qa-run.log fix22/dryrun37-rerun/remotion-still-probe.log
```
