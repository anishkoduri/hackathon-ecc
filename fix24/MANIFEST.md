# Fix #24 — MANIFEST

**Fix:** re-weave the whole hackathon-ecc plugin as one coherent system and dial it in for Cursor, the runtime it actually runs in. Coherence fix, not a feature fix — value is in what it removes and aligns.
**Authority:** `fix24/SPEC.md` (§0–§4) + `fix24/PARENT-GUIDANCE.md`.
**Close date:** Nov 12–13, 2026. **Coordinator:** fix #24 coordinator (session ae486d05).
**Status:** CLOSED — with the open parent adjudications in §5 and the environment-limited items in §6 recorded as owed, not as verified.

## Results

build.sh lines: 24070
build.sh md5: b0b2645a7d647f96296f9e9c45e09ef5
- build.sh diff vs pre-fix23 (`build.sh.before-fix23`, 23,774 lines): +296/-0 vs build.sh.before-fix23 (23,774 lines): +285 fix #23, +11 fix #24 wire block
- verify24.py: 105/105 PASS, exit 0 (re-run on build #4)
- Audit (final): Audit #71: ZERO blocking, 2 minor (both manifest-only: stale TBD placeholders in RESULTS; wrong F-06/:163 citation + misquoted phrase — both fixed in this regeneration)
- Sweep (final, incl. weaving-coherence pass): Sweep #32: 0 BLOCKING, 6 MINOR (all manifest-only; fixed in this regeneration), weaving-coherence CLEAN
- Dry-run (final, incl. Cursor-readiness leg): Dry-run #39: PASS — Leg 1 101/101 fixtures; Leg 2 Home Run re-run 52 measurements, 0 problems (1 pre-documented MINOR: panel-top stagger — substance already recorded in the render decision record, explicit ALIGN_F23_PANELS citation added by the coordinator); Leg 3 /demo 58/59 (1 FAIL environmental, live qa.mjs + film OWED); Leg 4 Cursor-readiness 37/37
- Prior verifiers (fix15/17/18/19/20/21/22/23 re-run): fix15 42/44, fix17 58/60, fix18 69/72, fix19 71/76, fix20 164/169, fix21 96/102, fix22 366/369, fix23 196/211 excl. manifest check (all at their expected tails, re-run on build #4)
- Banned terms: 0 in the built tree (case-insensitive, excl. node_modules)
- Counts: 166 skills / 72 agents / 123 rules / 87 commands / 15 hooks; 64 trigger keys
- Grok pin files: 27 files carry grok-4.7-high, 86 carry cursor-grok-4.6-high-fast (was 26/85; common-agents.mdc gained both via the fix #24 fallback paragraph)

## §1 Scope

§1 (full re-weave) and §2 (dial it for Cursor) per `fix24/SPEC.md`. Staged sources only, never the built tree; build.sh is the source of truth; `fix11/fix11-stage.py` never re-run. Upstream halves are patched at build time by `fix24/fix24.py` (same pattern as `fix16/fix16.py`), invoked by build.sh after fix23, before STEP 5. One build-time repair also landed in `fix16/fix16.py` (`edit_post_generic()`: the D-series Claude-scrub repairs) and one anchor update (gate.md parenthetical, E-7). No new skill, command, rule, agent, hook, or trigger. No bundle, no commit, no push.

## §2 Disposition table

Every SPEC item, what happened to it, and where it lives. "Staged" = edited in `new-skills/` / `round2-skills/` / `rewritten-skills/` / `new-rules/` and flows through the STEP 2 copy. "Build-time" = patched by `fix24/fix24.py` on the built tree. "fix16" = repaired in `fix16/fix16.py`.

| Item | Disposition | Location |
| --- | --- | --- |
| §1(a) A1 ANIM_TOKENS_F22 orphan | Cited in the inventory | Staged: `new-skills/orchestrate/references/design-inventory.md` |
| §1(a) A2 FUNC-UIPRO_F23 orphan | Cited from orchestrate SKILL.md:81 (step 3 hero/functionality paragraph) | Staged: `new-skills/orchestrate/SKILL.md` |
| §1(a) A3 FUNC-BQA_F23 orphan | Cited from orchestrate SKILL.md:81 (step 3 hero/functionality paragraph) | Staged: `new-skills/orchestrate/SKILL.md` |
| §1(a) A4 HERO-BQA_F23 orphan | Cited from orchestrate SKILL.md:81 (step 3 hero/functionality paragraph) | Staged: `new-skills/orchestrate/SKILL.md` |
| §1(a) A5 TRIO_F23 orphan | Cited in typeset.md:71 + browser-qa type-audit section | Staged: `round2-skills/polish-pass/reference/lenses/typeset.md`; build-time: `skills/browser-qa/SKILL.md` |
| §1(a) A6 MOBBIN_QA_F22 orphan | Cited from orchestrate step 5b | Staged: `new-skills/orchestrate/SKILL.md` |
| §1(a) A7 BANG_*_F22 section locators | Index line (naming all six tokens) + six section headings in pitch-deck-video | Staged: `new-skills/pitch-deck-video/SKILL.md:244,:255,:289,:312,:345,:381,:417` |
| §1(a) A8 ALIGN_F23_* sub-checks | 5 of 8 named by token at browser-qa:61 (NAV/LABELS/CLIP/ACTIONS/PANELS); OVERFLOW/CENTER/GRID described in prose items (a)/(b)/(d), meanings verified from alignment.md headings | Build-time: `skills/browser-qa/SKILL.md:61` |
| §1(a) A9 DEMOGATE_O4/O9/H1/H2 pairings | Recorded: O4 pairs with H2, O9 pairs with H1 | Staged: `new-skills/orchestrate/SKILL.md` (DEMOGATE_O4 line) |
| §1(a) B1 SCROLLTRIGGER_F22 / GSAP_F22 shared paragraph | Resolves via the shared paragraph; no change (optional hardening declined) | — |
| §1(a) C1 slop-checklist broken link | Fixed: `reference/lenses/typeset.md` → `lenses/typeset.md` | Staged: `round2-skills/polish-pass/reference/slop-checklist.md:681` |
| §1(a) C2 screen-demo.yaml synthetic skill | Documented inoperable in-plugin; no skill invented | Staged: `new-skills/pitch-deck-video/references/openmontage/runtime-fetch.md` |
| §1(b) C1 APCA vs WCAG | Fixed: APCA informational only, an APCA pass does not clear a WCAG fail | Staged: `new-skills/design-taste-frontend/references/hallmark/references/gates.md:170` |
| §1(b) C2 B3 30ms vs Rule 5 0.05s floor | Adjudicated: Rule 5 governs container-level `staggerChildren`; B3 0.03s governs per-row settle steps (different scopes) | Build-time: `skills/motion-patterns/SKILL.md:53,:574`, `skills/motion-foundations/SKILL.md:409` |
| §1(b) C3 B15 0.8x vs quick-ref ~60-70% | Adjudicated: B15 `motionTokens.exitFactor` is the single source of truth per Rule 8; quick-reference defers | Build-time: `skills/motion-patterns/SKILL.md:577-578`, `skills/motion-foundations/SKILL.md:435`, `skills/ui-ux-pro-max/references/quick-reference.md:155` |
| §1(b) C4 six/seven | Governing statement is the fix #22 extension line (seven required). Frozen texts stay byte-identical (D19_RULE, D19_APP, X1/X1_APP, STATIC19, LF_D19, DEPTH_F22 extension). Editable sites moved to seven + count-convention line added. TWO WORKER ERRORS CAUGHT BY THE verify19 LEG AND REVERTED: I-DESIGN's C4b seven-edit inside the frozen POLISH_F19 text (polish-pass SKILL.md) and I-ORCH's C4b seven-edit inside the frozen D19_ROUTING line (orchestrate SKILL.md:163 — Worker B's "routing:163 is editable" call was wrong; verify19 asserts D19_ROUTING verbatim). Both lines are byte-identical to the frozen constants again; the count-convention line governs the seven reading. See §4. | Staged: orchestrate DIRECTIVES, Taste trends, slop-checklist, unslop-fixes, vercel-checklist; build-time: ui-ux-pro-max:264, less-flat-ui:173 |
| §1(b) C5 commit missing from first-build sequence | Fixed: commit in orchestrate step 6 + hackathon-mode §7; leaked "(Batch B must mirror...)" note deleted; `gate)..` double period fixed | Staged: `new-skills/orchestrate/SKILL.md`, `new-rules/hackathon-mode.mdc` |
| §1(b) C6 F<n> collision (font vs film) | CORRECTED post-Audit #71: no film-rule definitions exist anywhere in pitch-deck-video. The bare (F1)/(F5)/(F6) pointers in pitch-deck-video are ALL film usages — F1 feature coverage, F5 per-beat A/V table, F6 runtime cap — defined only in fix22/SPEC.md:395, not in the skill. All three renamed: (FILM_F1) at :241, (FILM_F5) at :404, (FILM_F6) at :405, each defined by its sentence. The bare (F1)-(F7) pointers in the orchestrate/Taste static-check lists ARE the font rules, correctly used. (The earlier "F2-F6 are font rules" reading was wrong for pitch-deck-video:404-405.) | Staged: `new-skills/pitch-deck-video/SKILL.md:241,:404,:405` (coordinator edits) |
| §1(b) C7 Taste scroll ban vs MOTION_F23 | CLEAN (scoped). Scope qualifier appended to orchestrate:72 and ui-ux-pro-max:607; motion-foundations:205 already stated the scope, no edit | Staged: `new-skills/orchestrate/SKILL.md:72` (coordinator edit); build-time: `skills/ui-ux-pro-max/SKILL.md:607` |
| §1(b) D1-D5 duplications | No action except D4 count fix (part of C4b). Type-audit thresholds (D2) and OVERDRIVE 7-12 (D3) are verifier-asserted restatements — kept, accepted duplication | — |
| §1(c) F-01 double-run contradiction | Fixed: orchestrate steps 0-2 reframed as resume guards + one line in grill-me "After Grilling" | Staged: `new-skills/orchestrate/SKILL.md:58`, `new-skills/grill-me/SKILL.md` |
| §1(c) F-02 step 0 narration-key executor | Fixed: the orchestrator sends it | Staged: `new-skills/orchestrate/SKILL.md:58` |
| §1(c) F-03 Verify steps unnamed in 5a | Fixed: steps 1-4b named in step 5a; per-wave vs once timings split | Staged: `new-skills/orchestrate/SKILL.md:92` |
| §1(c) F-04 step-6 numbering collision | Fixed: "Verify step 6" is now "Verify stage 6 (Hallmark audit)" | Staged: `new-skills/orchestrate/SKILL.md:264` |
| §1(c) F-05 dangling "Gate 1" anchor in 5b | Fixed: now "start of the build — orchestrate step 0" | Staged: `new-skills/orchestrate/SKILL.md:93` |
| §1(c) F-06 six/seven (flow) | Count-convention lines in Taste:255 + polish-pass:23 + orchestrate:66. The routing paragraph (orchestrate:163) was NOT edited — it stays frozen six per D19_ROUTING; see §4. (An earlier draft of this row wrongly cited :163 as edited; corrected post-Audit #71.) | Staged: Taste SKILL.md:255, polish-pass SKILL.md:23, orchestrate SKILL.md:66 |
| §1(c) F-07 final report thin | Fixed: +4 bullets (inventory used vs rejected; memorable moment + verdict; type audit; re-verification PASSED/BLOCKED) | Staged: `new-skills/orchestrate/SKILL.md:348-365` |
| §1(c) F-08 order authority unclear | Fixed: step 6 is the one order line; the step-5 header (:86) defers ("full build order: see step 6") | Staged: `new-skills/orchestrate/SKILL.md:86,97` |
| §1(c) F-09 readme-writer URL source | Fixed: reads deployed URL + demo video path from the ledger itself; orchestrate step 6 reworded to match ("readme-writer reads...", no longer "passing it...") | Staged: `rewritten-skills/readme-writer/SKILL.md:95`; `new-skills/orchestrate/SKILL.md:97` (coordinator edit) |
| §1(c) F-10 inventory never named | Fixed: Taste step 4a + ui-ux-pro-max Query Contract both point at the inventory | Staged: Taste SKILL.md:220,:255; build-time: `skills/ui-ux-pro-max/SKILL.md` (fix24.py F-10) |
| §1(c) F-11 Phase 4 UI rule omits inventory | Fixed: "UI decisions route through the design inventory" | Staged: `new-skills/feature-expansion/SKILL.md:148` |
| §1(c) F-12 duplicated Lenses block | Fixed: duplicate deleted, one "## Lenses" heading | Staged: `round2-skills/polish-pass/SKILL.md:40-42` |
| §1(c) F-13 5b redesign never names Hallmark redesign.md | Fixed: wired + Bang Motion /demo-only qualifier | Staged: `new-skills/orchestrate/SKILL.md:93` |
| §1(c) F-14 post-report /demo stale README | NO EDIT — parent call, recorded open in §5 | — |
| §1(c) F-15 F6 qualifier nit | Fixed: ", below memorable (THE CORE)" appended; verify23 substring survives | Staged: `new-skills/orchestrate/SKILL.md:149` |
| §1(c) Inventory reachability R1/R2/R3 | R1 reachable; R2 fixed (expanded step-3 inventory paragraph + Taste step 4 deal line + dispatch-prompt pins pointer); R3 intentionally unreachable recorded; §10 cross-note added | Staged: orchestrate SKILL.md + design-inventory.md:152 |
| §1(d) S1 styles.csv 80 vs 89 | BLOCKED — NOT fixed: verify23:214-218 asserts the header exactly that way; changing it breaks verify23. OWED for a parent decision (verifier change) | — (see §5) |
| §1(d) S5 fix22 SPEC 142 vs 144 | Reconciled in the SPEC: 142 reel items + H1 + H2 = 144 | `fix22/SPEC.md:275,284` |
| §1(d) Other counts | All verified clean (palettes 192, pairings 74, guidelines 120, icons 105, GSAP 17, charts 25, stacks 22, products 192, app-interface 32, landing 34, Hallmark 50 themes, less-flat-ui 23, daisyUI 68, orbs 9 states at 0.3.2, Bang 10+19, glossary 20) | — |
| §2(a) Agent refs (dual citation) | 19 path lines in commands/ dual-cited (`X` agent (`agents/ecc-X.md`)); plan.md:199 was already house form (the 20th line); house-form invocations tree-wide; fallback paragraph in common-agents.mdc; duplicate architect row merged | Build-time: `fix24/fix24.py` (agent-ref regexes) |
| §2(a) general-purpose x3 | All three → "general subagent" (dispatch-prompt:12, skill-stocktake:127, rules-distill:85) | Build-time: `fix24/fix24.py` |
| §2(a) design-lead invocations x2 | Replaced with design-skill dispatch (gan-build:24, gan-design:17) | Build-time: `fix24/fix24.py` |
| §2(a) observer agent | Never invoked — parent decision, no change | — (see §5) |
| §2(a) ecc-planner | Explicitly not shipped — no change | — |
| §2(a) Rename vs dual citation | Dual citation implemented; renaming 69 files / 69 frontmatter names is a parent decision only if a one-token world is wanted | — (see §5) |
| §2(b) Model pins | All 72 `model:` pins slug-form Grok, zero violations (4 x grok-4.7-high, 68 x cursor-grok-4.6-high-fast) | — (verified, no change needed) |
| §2(b) Picker prerequisite | Stated once, verbatim, in orchestrate SKILL.md step 4; pointers elsewhere (:14, :24, :119, orch-build-mvp:41, README:68) | Staged: orchestrate + orch-build-mvp; build-time: README |
| §2(c) C-1 block-no-verify PowerShell gap | Fixed: powershellRole/cmdRole model the wrappers; -EncodedCommand/-File stay opaque (documented). Live-tested by the coordinator: powershell/pwsh/cmd `-Command`/`-c`/`/c` bypasses BLOCKED (exit 2); clean commands allowed; `-EncodedCommand` base64 NOT blocked (documented gap) | Build-time: `scripts/hooks/block-no-verify.js` |
| §2(c) C-2 auto-tmux-dev.js | Header note: unwired and dead in this plugin | Build-time: `scripts/hooks/auto-tmux-dev.js` |
| §2(c) C-3 desktop-notify.js | Header note: Windows branch needs BurntToast, never declared | Build-time: `scripts/hooks/desktop-notify.js` |
| §2(c) C-4 no .sh wired | Intentionally unwired, record only | — |
| §2(c) C-5 timeout 300 unit unstated | OWED to the live smoke test | `LIVE_SMOKE_TEST.md` §15 |
| §2(c) C-6 cwd/node/event names | OWED to the live smoke test | `LIVE_SMOKE_TEST.md` §15 |
| §2(c) C-7 Impeccable detector not a hook | No action, do not re-wire | — |
| §2(d) D-1 "Cursor only — no Cursor equivalent" | 10 occurrences in 9 files → "(Upstream only — …)" | fix16: `fix16/fix16.py` edit_post_generic() |
| §2(d) D-2 generic hook headers | 30 headers "Cursor-only" → "Upstream-only" + 3 specials (check-hook-enabled, ecc-statusline, hookify-runtime) | fix16: `fix16/fix16.py` edit_post_generic() |
| §2(d) D-3 plankton:118 | Same inversion, included in the fix | fix16 |
| §2(d) D-4 learn.md:2 | Same inversion, included in the fix | fix16 |
| §2(d) D-5 continuous-learning-v2:41,:86 | Parentheticals swapped | fix16 |
| §2(d) D-6 Stop/SessionStart contradiction | NOT decided — recorded open, OWED to Cursor docs / smoke test | — (see §5) |
| §2(d) D-7 GAN distinction | CORRECT — no fix | — |
| §2(d) D-8 OpenCode stragglers | harness-audit.js:393 reworded (parity check can never pass here); rest checked-harmless | Build-time: `scripts/harness-audit.js` |
| §2(d) D-9 .ecc/settings.json pickup | Unverified — OWED; angular mcp.md:53 Gemini CLI scope note added | Build-time: angular mcp; `LIVE_SMOKE_TEST.md` §15 |
| §2(e) E-1 pitch-deck-video APP_DIR | PowerShell form added (`$env:APP_DIR=...`) | Staged: `new-skills/pitch-deck-video/SKILL.md:162` |
| §2(e) E-2 plankton brew install | Windows branch first | Build-time: `skills/plankton-code-quality/SKILL.md` |
| §2(e) E-3 app-scaffold macOS Docker | Scoped (Windows: launch Docker Desktop from the Start menu) | Staged: `rewritten-skills/app-scaffold/reference/troubleshooting.md:17` |
| §2(e) E-4 auto-update + ecc-recipes | PowerShell first in both | Build-time: `commands/auto-update.md`, `skills/ecc-recipes/SKILL.md` |
| §2(e) E-5 pitch-deck-video venv paths | Windows forms added (troubleshooting.md:231-233 + tts.mjs:134 comment + :180 error string); music.mjs:53 `.tools/bin/yt-dlp` checked harmless (fallback array tries bare `yt-dlp` next) | Staged: `new-skills/pitch-deck-video/references/troubleshooting.md:231-233`, `new-skills/pitch-deck-video/template/scripts/tts.mjs:134,:180` (coordinator edits) |
| §2(e) E-6 brew/chmod/swiftlint | `brew install ruby` macOS-only; `chmod +x` macOS/Linux (Git Bash or skip on Windows); `brew install swiftlint` macOS-only | Staged: `round2-skills/mobile-ship/references/local-builds.md:85` (coordinator edit); build-time: agents/ecc-opensource-packager.md:149, agents/ecc-swift-reviewer.md:101 |
| §2(e) E-7 Taste gate hook Git Bash | Prerequisite recorded; no-Git-Bash behavior OWED | Staged: `new-skills/design-taste-frontend/references/gate.md:137` (coordinator edit); `LIVE_SMOKE_TEST.md` §15. NB: this edit broke a fix16.py anchor (gate.md parenthetical) and the anchor was updated in fix16.py:2992-2993 to match. |
| §2(f) F-1/F-2 local-plugin loading | README "Updating" section added as the single authoritative place; clone-into-local + git pull + Reload Window; copy install = rebuild + re-copy; delta bundles; never symlink; repo-link copy takes precedence | Build-time: `README.md` |
| §2(g) G-1 direct invocation | Defined in demo.md ("user typed `/demo`"); orch-build-mvp:32 reworded to "/demo dispatched from this run" | Build-time: `commands/demo.md`, `skills/orch-build-mvp/SKILL.md` |
| §2(g) G-2 demo.md env check | Rewritten: check env once for ELEVENLABS_API_KEY, else music-only/silent, never prompt on dispatched run | Build-time: `commands/demo.md` |
| §2(g) G-3 orchestrate.md:9 Show-the-plan-first | Qualified (after grill-me + narration-key prompt) | Build-time: `commands/orchestrate.md` |
| §2(g) G-4 orch-build-mvp step-8 | Environment-field dispatch line appended at SKILL.md:85 ("The `/demo` dispatch carries the Environment field naming `ELEVENLABS_API_KEY`…"); "Key handoff" referenced at :32. The literal token KEY-RECEIPT does not occur in orch-build-mvp (it lives in orchestrate step 0/6). | Build-time: `skills/orch-build-mvp/SKILL.md:85` |
| §2(g) /demo gates | Stand: never automatic, callable only on explicit invocation, contract intact; narration-key prompt ONLY when a demo video was asked for | — (verified, no change) |
| Coordinator | orchestrate:72 C7 scope qualifier; A9 DEMOGATE pairing record; C6 FILM_F1 + FILM_F5/FILM_F6 (F5/F6 are film rules — corrected post-Audit #71); F-09 orchestrate:97 reword; E-5 venv Windows form + tts.mjs Windows forms; E-6 local-builds macOS label; E-7 gate.md prerequisite. (An earlier draft of this row wrongly listed an orchestrate:163 edit; :163 was never edited — it stays frozen six.) | Staged (see rows above) |

## §3 Anchor tokens

No new anchor-token family: fix #24 reuses the _F22/_F23 families and adds three tokens, `FILM_F1` (pitch-deck-video SKILL.md:241 — "motion graphics never replace filmed feature coverage"), `FILM_F5` (:404 — per-beat A/V table), `FILM_F6` (:405 — runtime cap), each defined by its sentence; the film-rule F1/F5/F6 definitions live only in fix22/SPEC.md:395, not in the skill. Fix #24's own marker is the string `fix #24` (used in comments, count-convention lines, and the fallback paragraph). The picker prerequisite's authoritative site is orchestrate SKILL.md step 4; every other mention is a pointer ("see the picker note in step 4").

## §4 Adjudications (coordinator-made, parent spot-check)

- **C2:** Rule 5's 0.05s floor governs container-level `staggerChildren`; B3 `staggerRow` 0.03s governs per-row settle steps. Different scopes, no contradiction.
- **C3:** B15 `motionTokens.exitFactor` (0.8x) is the single source of truth per Rule 8; the quick-reference ~60-70% defers to it.
- **C6 (corrected post-Audit #71):** the film-rule definitions do not exist anywhere in pitch-deck-video; the (F1)/(F5)/(F6) pointers in pitch-deck-video are film usages (F1 feature coverage, F5 A/V table, F6 runtime cap), renamed to FILM_F1/FILM_F5/FILM_F6, each defined by its sentence. The bare (F1)-(F7) pointers in the orchestrate/Taste static-check lists are the font rules, correctly used. The earlier "F2-F6 are font rules" reading was wrong for pitch-deck-video:404-405 — Audit #71's spot-check repeated it because it ran on the pre-fix tree; the correction is verified in the staged sources.
- **C7:** Taste scroll ban vs MOTION_F23 is CLEAN (scoped); scope qualifier added to both MOTION_F23 statements that lacked it.
- **C4 frozen reclassification (caught by the verify19 leg, reverted not excused):** the routing line (orchestrate SKILL.md:163, D19_ROUTING) and the POLISH_F19 harmony sentence (polish-pass SKILL.md) are FROZEN — verify19 asserts both verbatim. Worker B's "routing:163 is editable" call was wrong, and I-DESIGN's C4b sweep edited inside POLISH_F19. Both lines were restored byte-identical; the seven reading comes from the count-convention line ("wherever a frozen rule text says 'six dimensions', read seven") and the DEPTH_F22 extension line, never from rewriting the frozen text.
- **C2/C3 vs verify22:** verify22's B3/B15 "conflict flag carried" checks fail by design — fix #24's adjudications replaced the flags with scope splits. New fix22 tail is 366/369 (fingerprint + B3 + B15).
- **_F23 counts vs verify23:** the SPEC-mandated orphan citations moved verify23's exact counts. New counts (asserted in verify24.py §11): INVENTORY_F23 5 lines / 5 occ, AMBITION_F23 7/8, MOTION_F23 9/12, TYPEAUDIT_F23 15/19, TRIO_F23 4/4, HERO-BQA_F23 4/4, FUNC-BQA_F23 3/3, FUNC-UIPRO_F23 2/2, ALIGN_F23 15/21, MEMORABLE_F23 5/6; 18 files carry _F23 tokens (was 17; feature-expansion gained one). New fix23 tail is 196/211 excluding its manifest check (fingerprint + diff + pins + 11 counts + manifest + fix22-leg). verify23's manifest check fails because its manifest records fix23's build.sh (24,059/df2cb850) — a permanent cascade of any later fix, not a fix #24 defect.
- **README picker "once per audience":** README:68 is a pointer, not a restatement; the "once per audience" reading is a legitimate parent call, recorded here.
- **F-2 layout:** resolved per the established Nov 11 convention (clone into `~/.cursor/plugins/local/hackathon-ecc`, `git pull` + Developer: Reload Window; copy install = rebuild + re-copy; never symlink).

## §5 Open parent adjudications

- **D-6 Stop/SessionStart:** four hook headers say "Cursor has no Stop/SessionStart hook event" while hooks.json registers both. Neither side picked; OWED to Cursor docs / the live smoke test (`LIVE_SMOKE_TEST.md` §15).
- **F-14 post-report /demo stale README:** a /demo run after the final report leaves the README stale (no video link). No edit proposed; parent call.
- **S1 styles.csv header:** "80 searchable styles" header vs 89 csv rows. NOT fixed — verify23 asserts it exactly that way. Changing it needs a verifier change, which is a parent decision.
- **Rename vs dual citation:** dual citation is implemented and robust to either resolution. Renaming 69 agent files or 69 frontmatter names to a single-token form is a parent decision only if a one-token world is wanted. Smoke-test step 6 is undecided; do not pre-decide.
- **observer agent:** named invocation vs background process — parent decision.
- **verify13h cascade (F-04 rename):** the rename breaks 2 verify13h checks (fix13h/verify13h.py:57,63 — old "Verify step 6" strings). verify13h is NOT in the fix #24 re-run set and is referenced nowhere outside its own MANIFEST/audit49-report; recorded cascade, no verifier edited.
- **hackathon-mode prose agent mentions:** hackathon-mode.mdc:42,66 unbackticked prose role mentions (scout, fast-worker, deep-reasoner) left short — parent call whether the §2a house form applies to prose mentions too.
- **D-9 `.ecc/settings.json` pickup:** unverified whether Cursor reads it; OWED to the smoke test.
- **C-5 timeout unit / C-6 hook runtime shape / E-7 no-Git-Bash behavior / C-1 -EncodedCommand gap:** all OWED to the live smoke test (`LIVE_SMOKE_TEST.md` §15).
- **Prior open items carried forward (not fix #24 scope):** Netlify row in deploy-fast (touch-up due after Dec 4, 2026); pip pinning pass (Audit #37 scope); fix #17 R1/R4 unverified; pitch-deck-video template fonts self-host follow-up; fresh bundle needed before any push (do NOT push b2444de).

## §6 Environment-limited caveats

- The full live `qa.mjs` exit-0 + live film is OWED to the smoke test (same sandbox Chrome egress limit as fixes #22/#23: fonts.gstatic.com unreachable).
- The C-1 `-EncodedCommand` base64 bypass is NOT blocked (documented in code + smoke-test §15): the scanner cannot read base64. A PowerShell-ism hiding the git call behind variables, `&`, `Invoke-Expression`, or `Start-Process` likewise falls back to the opaque word scan, which catches only a literal `git ... --no-verify` in the raw text.
- The build was re-run once after the first attempt died at fix16.py (ERRORS: 1 — the coordinator's E-7 gate.md edit broke a fix16.py anchor; the anchor was updated in fix16.py:2992-2993 and the build re-run clean).
- fix16.py re-run on an already-built tree reports hundreds of anchor errors (anchors already consumed) — that is re-application noise, not a defect; it runs once per fresh build.
- Build #4 (post-Audit-#71 coordinator fixes — C6 FILM_F5/FILM_F6, F-09, E-5 tts.mjs): clean, fix16 ERRORS 0 / NOTES 38 / CHANGES 649 / REMOVALS 88, fix24 114 changes OK, banned terms 0; durable record in fix16/fix16-run-log.md + fix24/fix24-run-log.md. (Sweep #32's caveat that no build #4 log exists is wrong — /tmp/fix24-build4.log exists; /tmp is ephemeral, the run-logs are the durable record.)
- /tmp hygiene: /tmp is a 512 MB tmpfs; fix #24 test copies filled it to 97% (20 MB free), crashing Chrome on load until dry-run #39 redirected TMPDIR into its own scratch. Test copies removed after build #4 (132 MB free). Upstream clones in /tmp (ecc-repo-clean, uipro, ecc-dev-install, hackathon-skills) must be kept — build.sh assembles from them. NOTE: /tmp/skill-add holds three pinned upstream clones (chwezi-dev-engine, flecto-shade, hackathon-agent-skills) — do not delete on a "scratch" assumption.
