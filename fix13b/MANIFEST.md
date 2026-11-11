# MANIFEST — Fix program #13b (coordinator): fix the 8 minors from dry-run #14

Finding source: dry-run #14 (Campus Eats) on the fix-#13 build — 0 blocking / 8 minor, NOT CLEAN. Audit #42 on the same build: 0 blocking / 1 minor (manifest-only, parent-handled). This round fixes all 8 minors, then Audit #43 + dry-run #15 run on the same build.

## 0. Build record

- `build.sh` pre-fix13b: 22,274 lines, md5 `a0817413ee0c4be0fe24e4048c541843`. Backup: `build.sh.before-fix13b` (same md5).
- `build.sh` post-fix13b: 22,316 lines (+42), md5 `52019e0a317fff632e8f73bfc8b16967`. `bash -n` OK.
- Rebuilds: build 1 exit 0; build 2 exit 0. **Manifest diff between build 1 and build 2 = 0 (reproducible).** Manifests: `fix13b/manifest-build1.txt`, `fix13b/manifest-build2.txt` (3,383 files each).
- Counts: **169 skills, 72 agents, 123 rules, 96 commands, 15 wired hook events (16 scripts incl. adapter.js) — UNCHANGED.** Size: **57 MB — UNCHANGED.** No new skills/agents/rules/commands. No pins touched. No zip/upload. Repo/bundle untouched.
- Scripts: `fix13b/fix13b.py` (staged-source edits, all count==1 asserts) + `fix13b/fix13b-assemble.py` (build.sh block insertion, preflight anchors count==1 against the post-fix13 built tree; idempotency guard; backup). Logs: `fix13b/build1.log`, `fix13b/build2.log`.

## 1. The 8 minors — re-traced in the built pre-fix13b tree, all CONFIRMED

- **M1 CONFIRMED** — feature-expansion SKILL.md :145 UI rule + :189 reference table listed only ui-ux-pro-max + less-flat-ui + Impeccable via polish-pass + Harmony (+ Taste for landing); omitted the conditional components (motion, design-system, inherit-legacy-style).
- **M2 CONFIRMED** — orch-change-feature SKILL.md :36 listed app/landing/motion components; omitted design-system + inherit-legacy-style (no orchestrate slicing downstream to catch them).
- **M3 CONFIRMED** — blind reviewer is diff-only yet asked to judge built screens: orchestrate :184 gives it "only the diff and the contract's acceptance criteria", :187 asks it to judge built screens against the distinctiveness bar; same defect in orch-pipeline Review :71-72 and dispatch-prompt.md :177-182 `[UI diff:]` block. Conditional: orchestrate :184 fires only when "Not cheaply verifiable", :185 for large/risk-domain — small diffs may get no reviewer at all.
- **M4 CONFIRMED** — browser-qa :68 criteria (typography, hierarchy, spacing, alignment, color, contrast, responsiveness) exclude distinctiveness — the bar had no executor inside the visual loop.
- **M5 CONFIRMED** — orch-pipeline Review :71-72 carries the derivative clause ("or are derivative (the design is based on a searched external reference)"); Verification :120 drops it.
- **M6 CONFIRMED** (parent-verified) — less-flat-ui :70: "A treatment on a small surface can be bolder than on a full page: a button can carry a full thermal gradient, a page background usually should not." (Source line :69 in `~/workspace/cursor-skills/less-flat-ui/SKILL.md`; built :70 after a +1 insertion.)
- **M7 CONFIRMED** (parent-verified) — polish-pass SKILL.md :22: "if neither exists, infer the direction from the code and record it in the token file before judging" (self-certification); polish.md step 2.7 (:24) has no such infer clause — files disagree.
- **M8 CONFIRMED** — orch-build-mvp step 6 :49: code-reviewer + expansion Phase 5 checks by name only; no every-route visual loop, no sloplint `--scope app` audit (orchestrate has both at Verify steps 5-6).

## 2. M3+M4 mechanism — coordinator decision: browser-qa is the SINGLE executor

Chosen over giving the blind reviewer screenshots or naming the orchestrator: **browser-qa is the single named executor of the screen-level distinctiveness bar inside the visual loop**, because it is the only component that sees rendered screens (Playwright, desktop + mobile). The blind reviewer cannot judge screens from a diff — a category error — so it now checks only the recorded direction (diff-visible) and runs on EVERY UI diff regardless of size. Consequences:
- The bar is checked on every UI pass: orchestrate step 5 (whole-build, every primary route), orch-build-mvp step 6 (whole-build, every primary route), and the new orch-pipeline Review visual-loop invocation (touched screens only — different scope from the whole-build loop, not a duplicate).
- Orchestrate :193 and orch-build-mvp step 6 state explicitly that sloplint `--scope app` does NOT prove distinctiveness.
- No new user question, approval gate, or wait point anywhere.

## 3. Changes — file:line IN THE BUILT PLUGIN (all verified by grep, count==1 unless noted)

### Staged sources (fix13b.py)
- **feature-expansion SKILL.md:145** — UI rule gains: "Conditional components apply by surface type, never by size: motion work adds `make-interfaces-feel-better` (then the motion-* skills for React/Next motion); new design-system work adds `design-system`; legacy style drift adds `inherit-legacy-style`." **:189** — reference table gains the same conditional list.
- **orchestrate SKILL.md:187** — new item 4 in the reviewer calibration: "Any diff that touches a UI surface (any size) → a blind reviewer ALWAYS runs." **:189** — :187 paragraph rewritten as the "Design-direction record check (UI diffs)": reviewer checks the direction is RECORDED (named direction in the diff, tokens tracing to it); "does NOT judge the built screens"; "Screen-level distinctiveness is judged ONLY by `browser-qa` in the visual loop (step 5 below), the single named executor." **:193** (step 5, shifted +2) — "Distinctiveness bar (can FAIL — applies here; `browser-qa` is the SOLE executor...)". **:195** (step 6, shifted +2) — "the distinctiveness check lives ONLY in the step-5 visual loop" + "The distinctiveness judgment on the primary screens happens in the step-5 visual loop (`browser-qa`, sole executor) — do not re-judge it here".
- **orchestrate/references/dispatch-prompt.md:177-182** — `[UI diff:]` block rewritten as the record-check ("Do NOT judge the built screens — you cannot see them... Screen-level distinctiveness is judged by `browser-qa` in the visual loop, not here.").
- **less-flat-ui SKILL.md:70** (source `~/workspace/cursor-skills/less-flat-ui/SKILL.md:69`) — "A treatment on a small surface can carry more than on a full page: a button can carry a full thermal gradient, a page background usually should not — more craft on the surface, not a bolder look." Old "bolder" line: 0 hits left. (Other "bold" hits at :45/:144/:219/:417 are style vocabulary — "bold heroes/posters" — not posture framing; untouched.)
- **polish-pass SKILL.md:22** — infer clause replaced: "if neither exists, record that no direction is recorded — a missing-direction finding (minor at least), routed to the design skill — and do NOT infer a direction from the code and judge against it: a direction the check itself invented cannot certify the screen." **polish-pass/reference/polish.md step 2.7** — same rule appended: "If neither file exists, do NOT infer a direction from the code — record a missing-direction finding (minor at least) routed to the design skill, and do not pass direction-application on any screen." Old infer clause: 0 hits left; "do NOT infer a direction from the code": 1 hit in each file. Pre-existing build.sh (f) anchors in staged polish-pass SKILL.md re-verified count==1 after the edit.

### Build.sh block fix13b (LAST, just before STEP 5)
- **orch-change-feature SKILL.md:36** — UI rule gains "new design-system work: + `design-system`; legacy style drift: + `inherit-legacy-style`"; Verify sentence now routes through "`browser-qa`'s visual loop on the rebuilt surface (the single executor of the bar — see orch-pipeline Review; the reviewer checks only the recorded direction)".
- **orch-pipeline SKILL.md:72** — Review rewritten: reviewer ALWAYS runs on UI diffs regardless of size, checks the recorded direction, "does NOT judge the built screens"; browser-qa visual loop runs on the rebuilt surface after the reviewer pass (touched screens, desktop + mobile, distinctiveness bar, capped 2-round fix loop, max 3 rounds total, app-cannot-run → blocked with evidence).
- **orch-pipeline SKILL.md:120** — Verification UI line gains "or are derivative (the design is based on a searched external reference)".
- **browser-qa SKILL.md:68** — criteria gain distinctiveness: "this skill is the SOLE executor of the distinctiveness bar inside the visual loop... a screen with no named direction, no applied theme/tokens, reading as a default template, or derivative... FAILS — report it as a distinctiveness finding (minor at least) with the top-5 list... No other step judges screen distinctiveness — the blind reviewer checks only the recorded direction, and sloplint app scope does not carry it."
- **orch-build-mvp SKILL.md:49** — step 6 gains the every-route visual loop (every primary route; Review-phase loop covers only touched screens) + the app-screen design audit (sloplint `--scope app`, static tier, `--json`, fix every FAIL / fix-or-waive every REFLEX; "a sloplint app-scope pass does NOT prove distinctiveness").

## 4. Regression greps (built tree)

- Contradiction residue: "ALSO judges the built screens" / "applies here and in the blind reviewer" / "lives in the step-5 visual loop + the step-2 blind reviewer" / old infer clause: **0**. Remaining "judge the built screens" hits (2) are the new NEGATIONS ("does NOT judge the built screens") in orch-pipeline :72 and orchestrate :189.
- Grok pin intact: `grok-4.7-high` ×4 in orchestrate SKILL.md; `grok-4.7[` bracket syntax: **0** tree-wide. "Posture — more, not bolder" ×1; "No design based on a searched reference" ×1 (orchestrate). Derivative clause present: orchestrate ×1, orch-pipeline ×2, orch-build-mvp ×2 ("are derivative"), orch-change-feature ×1 ("is derivative").
- Single-executor naming: browser-qa :68, orchestrate step 5, orch-build-mvp step 6, orch-change-feature :36, orch-pipeline Review :72 — all name browser-qa as the sole/single executor; no file names a second executor.

## 5. Held back, with reasons

- No numeric distinctiveness score (per fix #13 brief; the bar is recorded-direction-AND-visibly-applied + not derivative, a finding on failure).
- No new skills/agents/rules/commands. No new gates/waits/questions. Deferred-six §3/§7 carve-out, auto-expansion/auto-approval, Grok pin + picker instruction, anti-derivative rule, "more, not bolder" posture, CBM phrasing, direction lenses/live-generate, frontend-slides untouched. No supply-chain pins or SSML truth touched. No fix11-stage.py re-run. No pip pinning pass. No bundle/repo touching.
- Audit #42's 1 minor (manifest-only) was parent-handled, not touched here.

## 6. Next: Audit #43 + dry-run #15 (spawned in parallel after the build)

Audit #43: full-tree audit of this build. Dry-run #15: Campus Eats walk-through as orchestrator + subagents, exercising the design-package routing, the single-executor distinctiveness bar (including small UI changes and one-prompt changes), and the new step-6 checks. Both report blocking/minor lists with file:line. The loop closes only when the audit returns ZERO ERRORS and the dry run is CLEAN.
