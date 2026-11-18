# Re-audit #113 — fix #33 round 33e (combined: correctness + adversarial bypass re-trace + new-bypass hunt)

- **Date:** Tue Nov 17, 2026 (evening, CST)
- **Tree:** `~/workspace/hackathon-plugin/fix33/scratch-repo`, git HEAD `dd106ade`; built tree `scratch-repo/hackathon-ecc/` (run-11 build)
- **Round under audit:** fix round 33e (fixes audit #112-B B-N1 blocking, audit #112-A A-M1/A-M2 minor, sweep #55 S-M1 minor)
- **Method:** full independent re-trace of the B-N1 path in staged + built trees; fresh enumeration of all 55 commands, all 48 trigger-routed skills, all 72 skills, all 203 `references/`/`reference/` markdown files, all `rules/*.mdc`, hooks, and cross-skill loads; independent re-runs of verify33.py + scans r4/r5; planted-violation probe in a full probe copy; own frontmatter/census counts; `git grep` at HEAD for the §1(d) claim. Nothing was committed. One probe accident (see O-5) briefly mutated the real tree and was restored byte-exact, re-verified 592/592 after.
- **Verdict: NOT PASS** — 0 blocking findings, 1 minor finding. B-N1 is genuinely closed, no new bypass was found, the S-M1/A-M1/A-M2 content fixes are all real, the verifier passes 592/592 and both scans pass, and the diff stat is consistent. What fails the verdict is stale line-number pointers in live docs: the round's own edits shifted lines, and the round-33e report + SPEC §3(j) copied the pre-edit line numbers without re-measuring. Same class as audit #111-A's A-M1 (stale line numbers → NOT PASS) and audit #110's 110-M1.

## Verdict summary

| Check | Result |
|---|---|
| B-N1 closure (re-traced end to end, staged + built) | CLOSED |
| New-bypass hunt (commands + triggers + all 72 skills + all 203 references files + rules + hooks + cross-skill loads) | No new bypass |
| S-M1/A-M1 fast 70 → 71 (content, all five spots) | FIXED |
| A-M2 SPEC §3(h) reword (content) | FIXED |
| SPEC §1(d) x70 at HEAD dd106ade | Verified genuine (70) |
| Verifier (own re-run) | 592/592, exit 0 |
| Scan r4 / r5 (own re-runs) | 76/76, 100/100, ALL PASS |
| Verifier probe (delete built skill :18) | 589/592, exit 1, exactly the 3 related B-N1 FAILs |
| Diff stat + consistency | 49 files, +200/−126, quoted consistently |
| Unpin census | ID 0, PROSE 2, XID 0, XPROSE 0, fast 72; 41 fast + 4 inherit agents |
| Previously closed bypasses (spot-check B-B1, B-B2, B-B5, B-B6) | Still hold |
| Stale line pointers in live docs | **A-M1 (minor)** — 1 finding |

## Findings

### A-M1 (minor) — Stale line-number pointers for the round-33e fixes: the content is right, the numbers point at the wrong lines

Round 33e's own edits shifted lines (four new D33-36…D33-39 bullets in SPEC §2, a new §3(j) subsection, new DECISION-33-36…39 strings in fix33.py, a new run-11 entry in MANIFEST), and the round-33e report copied the pre-edit line numbers from the audit/sweep reports without re-measuring. Every pointer below names content that is correct at its true line; the pointer itself lands on the wrong line (blank, or a different bullet):

| Pointer as written | True line (measured by me) | What is actually there |
|---|---|---|
| `fix-round-33e-report.md:28` — "SPEC.md:201 (§3(e) (16f))" | SPEC.md:**205** | The (16f) bullet ("fast 71") is on :205; :201 is blank (the line before the `### (e)` header at :202) |
| `fix-round-33e-report.md:29` — "SPEC.md:237 (§4)" | SPEC.md:**249** | The fast-worker-pin line ("x71") is on :249; :237 is blank (the line before the `### (j)` header at :238) |
| `fix-round-33e-report.md:30` — "fix33.py:522 (DECISION-33-4 string)" | fix33.py:**535** | DECISION-33-4 ("The fast tier (x71)…") is on :535; :522 is inside an unrelated `_block` call |
| `fix-round-33e-report.md:40` and `SPEC.md:242` (§3(j)) — "SPEC.md:217 reworded" | SPEC.md:**221** | The reworded §3(h) line ("Step 0 — the MODEL check is its first content, before the classifier's scoring text") is on :221; :217 is blank (the line before the `### (h)` header at :218) |
| `fix-round-33e-report.md:123` — "MANIFEST.md:67" (diff-stat quote) | MANIFEST.md:**68** | The "49 files changed, +200/−126" line is on :68 |
| `fix-round-33e-report.md:123` — "fix33-implementation-report.md:230" (diff-stat quote) | fix33-implementation-report.md:**240** | The diff-stat line is on :240 |

The live-doc instance is `SPEC.md:242` (in §3(j), the round-33e summary itself): "SPEC §3(h) :217 reworded…" — a reader following ":217" lands on a blank line. The other five instances are in the round-33e report, the round's claim record. The correctly cited pointers in the same report were spot-checked and are right: `SPEC.md:9` (§0), `fix33-patch-log.md:53` ("x71"), `skill-triggers@1.json:93/:95/:99`, `SKILL.md:18`, `:456`, `redesign.md:68`, `verify33.py:3118` (site 446).

**Why this is a finding and not an observation:** this fix's own precedent treats exactly this as a finding — audit #110 (110-M1, stale diff stat in live docs → NOT PASS), audit #111-A (A-M1, stale guardrail-home line numbers → NOT PASS), audit #112-A (A-M1/A-M2, stale number/wording in live SPEC → NOT PASS). A wrong pointer in live SPEC text is that class, even though the content it points at is correct.

**Fix:** re-measure and correct the six pointers (SPEC:242 ":217" → ":221"; 33e report :201 → :205, :237 → :249, :522 → :535, :217 → :221, MANIFEST:67 → :68, impl-report:230 → :240). No tree change, no rebuild, no verifier change needed.

## 1. B-N1 closure — full re-trace (independent, staged + built)

Chain read end to end in the run-11 built tree (nothing trusted from the worker's trace):

1. **Trigger.** `hackathon-ecc/manifests/context-packs/skill-triggers@1.json:93` — `"skill:design-taste-frontend"` routes from 8 phrases including "design a landing page" (:94), "redesign the landing page" (:95), "landing page design", "company page design", "design the dashboard", "redesign the app ui" (:99), "dashboard design", "app interface design". 48 trigger keys total in the file (`triggers` dict); coverage 72 skills / 48 with triggers. A user typing "redesign the app ui" on a 5-page app loads the skill directly (Cursor description routing — the same footing audits #111-B/#112-B accepted for B-B5/B-B6; call-map method note B6 documents the manifest itself as a reference table).
2. **Skill entry.** Built `skills/design-taste-frontend/SKILL.md:18`, byte-identical to staged `new-skills/design-taste-frontend/SKILL.md:18` and to the grill-me / feature-expansion check lines (`diff` silent on all three):
   > "**MODEL check (fix #33, MODELSEL_F33):** before anything else, state the model the orchestrator is running on and record it in the run ledger (`MODEL: <name>` — the actual selected model). If the selected model is Auto, or the model cannot be determined to be a specific model, tell the user to pick a specific model before proceeding; do not silently orchestrate on an unknown fallback."
   Placement verified by read: :16 is `# Taste skill v2.5.1`, :17 blank, :18 the check, :19 blank, :20 the first body text ("Build the website a good company would ship…"), :26 `## House rules`. The check is the first content under the heading, before House rules, before §1, before the deal, before step 5's build. Only the frontmatter (:1–14) precedes it. `MODELSEL_F33` occurs exactly 1× in the skill, staged and built.
3. **Routing.** Built skill :456 (staged :456, identical line):
   > "**Redesign of an existing page (keeping content + wiring).** When the job is a full-page redesign that keeps every fact, link, form, field, handler, route, id, and test hook, follow the Hallmark redesign flow (`references/hallmark/references/redesign.md`) — factory routing for the redesign flow lives there: page subagents are single-task factory drones with director briefs (GLOBAL-ROUTING_F29)."
   Check (:18) precedes routing (:456) by 438 lines, in the same file.
4. **Fan-out.** Built `skills/design-taste-frontend/references/hallmark/references/redesign.md:68` ("More than one page" paragraph, unchanged text):
   > "Past three pages, give each page to its own subagent where the harness has them, with that tokens file, the page's files and this file. **Factory routing (fix #29, GLOBAL-ROUTING_F29):** each page subagent is a single-task factory drone with a director brief (DIRECTOR-BRIEF_F29)…"
   The fan-out is downstream of the skill entry on every path that reaches it, because every load of the flow passes through the skill file first. `redesign.md` itself carries zero `MODELSEL_F33` — by design; the guardrail lives at the skill entry, one file up.
5. **In-flow routes (already covered, re-fire silently — confirmed).** `skills/orch-change-feature/SKILL.md:41` `## Landing redesigns` routes "through the Hallmark redesign flow: `skills/design-taste-frontend/SKILL.md` (redesign paragraph before step 5) and the procedure in `references/hallmark/references/redesign.md`" — it names the skill file, so the :18 check fires on load, and the change path runs engine Step 0 first anyway (skill step 1, :34: "Run the `orch-pipeline` engine with the settings above"). Orchestrate's polish-routed redesign sits downstream of the pre-grill MODEL check (`skills/orchestrate/SKILL.md:52`); its step 5b (:103) runs `polish-pass` after Verification and re-verifies any polish-routed redesign before deploy. On a specific selected model the entry check passes silently (its text only interrupts on Auto/undetermined), so no second ask on these routes. The redesign flow's own "The ask" (three questions) still does not resolve Auto — correctly not treated as a substitute.
6. **Scope.** 1–3 pages at restyle/full work inline and never dispatch; polish depth never fans out (the `## Build` section gates fan-out to restyle/full). The hero/finish review subagents (`gates.md:243`) and manual-gate / fresh-reader subagents (`gate.md:179-180`, `copy-voice.md:173`) are review-only (B-M3/OWED-33-5 class) and sit downstream of the entry check anyway.

**Staged-vs-built diff for the skill:** only the known pre-existing description-line transform (:9–13, the "Use for EVERY surface…" build rewrite) plus the new insertion. The check line itself is byte-identical in both copies.

**B-N1 is CLOSED.**

## 2. New-bypass hunt (same method as #112-B, re-run from scratch)

Enumerated and traced: all 55 `commands/*.md`; all 48 trigger-routed skills; all 72 skills on disk; all 203 markdown files under `skills/*/references/` + `skills/*/reference/`; all `rules/*.mdc`; `hooks/*.js`; every `skills/` cross-reference and every `commands/` skill reference. No new bypass found. The hunt list, with dispositions:

| Site | What it starts | Guardrail / disposition |
|---|---|---|
| `skill:design-taste-frontend` → Hallmark redesign, >3 pages | one factory drone per page, code-writing | **Yes — entry check :18 (B-N1 fix, §1)** |
| `skill:grill-me`, `skill:feature-expansion` | Q&A / 4 brainstorm subagents | Yes — skill-entry checks (:8 / :6), spot-checked still in place |
| `skill:orch-*` (all 5), `skill:orchestrate`, `skill:orch-pipeline` | engine / Step 0 / dispatch | Yes — Step 0 first / pre-grill check |
| `/orch-*`, `/orchestrate`, `/gan-build`, `/gan-design`, `/astra-review`, `/feature-dev`, `/react-build` | engine / dispatch / factory drone | Yes — entry checks (11 command files carry MODELSEL_F33, each 1×) |
| `skill:council` (7 subagent mentions) | Skeptic / Pragmatist / Critic subagents, deliberation only | No — B-M3 class (OWED-33-5, recorded not fixed); review-only, same as #111-B |
| `skill:gan-style-harness` (1 subagent, 3 dispatch) | harness design/rubric only; routes via `/gan-build` + `/gan-design` | Yes — via the checked commands; no dispatch instruction of its own |
| `skill:orch-add-feature` / `orch-fix-defect` / `orch-refine-code` (dispatch mentions, no MODELSEL in SKILL.md) | factory routing via the engine | Yes — each skill's step 1 runs the engine (add :31, fix :33, refine :33); the :13 factory-routing note is descriptive; refine-code's step-2 refactor-cleaner drone (:35) is post-Step-0 |
| `skills/orchestrate/references/dispatch-prompt.md` (4 subagent, 23 dispatch) | drone-brief templates | Yes — downstream-only; read when the orchestrator composes a dispatch, after the pre-grill check |
| `skills/orchestrate/references/call-map.md` (6 subagent, 92 dispatch) | routing table / method notes | N/A — documentation-only map; no file references it by name; its "dispatch" hits are table entries, not imperatives |
| `skills/orchestrate/references/patterns.md` (1 dispatch) | on-demand reference layer, defers to SKILL.md | N/A — no dispatch instruction |
| `skills/polish-pass/reference/impeccable-critique.md` (spawn A/B ×3) | Assessment A (design review) + Assessment B (detector/browser evidence) as two isolated sub-agents | No — B-M3 class (review-only: both assessments *return* scores/issues, they do not write code) **and** no live loader found: `polish-pass/SKILL.md` never links `reference/impeccable-critique.md` (only PROVENANCE mentions it); the skill loads `reference/polish.md`, `scoring.md`, `craft-floor.md`, `capture.md`, lenses. Dormant + review-only. See O-2 |
| `design-taste-frontend/references/gate.md:179-180` (manual gate in a subagent), `.../gates.md:243` (hero/finish review), `.../copy-voice.md:173` (fresh reader) | review/gate subagents | No — B-M3 class; all downstream of the new :18 entry check anyway |
| `design-taste-frontend/references/effects-objects.md:167`, `.../themes/newsprint.md:9`, `mobile-ship/references/monetization.md:173`, `motionsites-web-builder/references/techniques/depth-and-interaction.md:255/257`, `react-testing/SKILL.md:93`, `frontend-patterns/SKILL.md:282/286/293`, `skills/design-taste-frontend/assets/objects/product-render/README.md:61` | DOM `dispatchEvent` / React `useReducer` dispatch / "dispatch" keyword / spawn thumbnails | N/A — false positives, not agent dispatch |
| `skills/frontend-patterns/SKILL.md` (4 dispatch, 0 subagent, not trigger-routed) | React `useReducer` code samples | N/A — false positive; its loaders are pattern skills + checked `/react-build` |
| `commands/demo.md:13`, `commands/plan.md:2,10`, `commands/quality-gate.md:44-45` (only non-MODELSEL commands with subagent/dispatch mentions) | `/demo` dispatched-from-a-run note; `/plan` "Do not delegate to a subagent by default", inline by default; hook-dispatcher registry note | N/A — no code-writing dispatch (same as sweep #55; `pm2.md`'s `child_process.spawn` is a Node code sample) |
| `commands/prp-commit` → `git-workflow`, `python-review` → `python-patterns`/`python-testing`, `react-review` → `frontend-a11y`/`react-patterns`/`react-testing`, `react-test` → `e2e-testing`/`frontend-a11y`/`react-testing`/`tdd-workflow` | pattern/review reference skills | N/A — all 0 subagent mentions (react-testing's 1 dispatch hit is `fireEvent`) |
| Cross-skill loads from unchecked skills: `motion-foundations`/`motion-patterns` → `design-taste-frontend`, `polish-pass`/`ui-ux-pro-max` → `design-taste-frontend`, `gsap` → `motion-*`/`ui-ux-pro-max`, `browser-qa` → orchestrate (file pointer only), `ck`/`delivery-gate`/`pitch-deck-video`/`tdd-workflow` → self | reference/pointer loads | Covered — loads of design-taste-frontend now hit its entry check; the rest point at inline pattern/review skills with 0 dispatch mentions |
| `rules/common-agents.mdc:26,34,38` | factory-routing description; "parallel subagent execution for independent read-only operations only" | N/A — constrains dispatch (read-only only), does not dispatch; defers to orchestrate's GLOBAL-ROUTING |
| `rules/hackathon-mode.mdc:45,49` | GLOBAL-ROUTING description; orchestrator owns delegation/fan-out | N/A — downstream of the orchestrate entry check |
| `rules/ponytail.mdc:9`, `rules/arkts-hooks.mdc`, `rules/web-hooks.mdc`, `rules/react-testing.mdc:54` | subagent return-message footer note; Cursor hook wiring; `fireEvent`/`userEvent` | N/A — no dispatch |
| `hooks/*.js` (`subagent-start.js`, `subagent-stop.js` only hits) | subagent lifecycle audit hooks | N/A — observe subagents, do not dispatch them |
| `skills/orch-change-feature/SKILL.md:41-43` (Landing redesigns) | routes via the design-taste-frontend skill file | Yes — entry check :18 + engine Step 0 upstream (§1.5) |
| Full 72-skill census | 13 skills have any subagent/dispatch mention; the other 59 have zero | All 13 accounted for above; no un-inventoried dispatcher |

**Other fan-out wordings hunted whole-tree:** `grep "give each .* to its own subagent|each .* to its own subagent|one subagent per|a subagent per|per page.*subagent|subagent per page"` returns exactly one hit — `redesign.md:68` (the B-N1 fan-out, now guarded). `grep "own subagent"` returns exactly one file — the same `redesign.md`. No second fan-out wording exists in the built tree.

**Files hunted (built tree unless noted):** all 55 `commands/*.md`; all 48 trigger skills' `SKILL.md`; all 72 `skills/*/SKILL.md` (full census); all 203 files under `skills/*/references/**` + `skills/*/reference/**`; `skills/polish-pass/reference/impeccable-critique.md` (full head + Assessment A/B + orchestration section); `skills/polish-pass/SKILL.md` (reference loads); `skills/orchestrate/references/call-map.md` (dispatch lines sampled), `dispatch-prompt.md` (head + skeleton), `patterns.md`; `skills/design-taste-frontend/references/hallmark/references/redesign.md` (full `## Build`), `gates.md:243`, `gate.md:179-180`, `copy-voice.md:173`; `skills/council/SKILL.md` (subagent lines); `skills/orch-add-feature`, `orch-fix-defect`, `orch-refine-code` (dispatch lines + step 1); `skills/orch-pipeline/SKILL.md` (Step 0 :41/:43, dispatch :64/:76); `skills/frontend-patterns/SKILL.md` (:282–293); `rules/*.mdc` (all subagent/dispatch lines); `hooks/*.js` (subagent/Task grep); `manifests/context-packs/skill-triggers@1.json` (all 48 keys).

## 3. S-M1/A-M1 — fixed in substance (all five spots say 71)

Measured by me, not copied from the round report (line numbers in the report are stale — see A-M1 — but the content is right in every spot):

| Spot | Now reads | True? |
|---|---|---|
| SPEC.md:9 (§0, D33-4) | "The fast/execution tier (`cursor-grok-4.6-high-fast`, x71) is untouched." | Yes — 71 pre |
| SPEC.md:205 (§3(e), (16f)) | "(16f) fix33 patch log (0 errors, census 20 ID + 5 PROSE replaced, keeps x2, fast 71)" | Yes |
| SPEC.md:249 (§4) | "The fast-worker pin (`cursor-grok-4.6-high-fast` x71), the fast tier, the drones…" | Yes |
| fix33.py:535 (DECISION-33-4 string) | "The fast tier (x71) and the drones are untouched." | Yes |
| fix33-patch-log.md:53 (regenerated) | "The fast tier (x71) and the drones are untouched." | Yes — patch log regenerated on run 11 (see §6) |

Independent count check: direct grep of the rebuilt tree = `cursor-grok-4.6-high-fast` **x72** (71 pre-existing + 1 schema description, D33-17); patch-log census line (:7) says x71 pre / x72 post; `fix33.py` EXPECT `FAST_ID: 71` + post-assertion 72; `verify33.py` §16f asserts fast x72.

**SPEC §1(d) x70 claim verified genuine:** `git grep -o 'cursor-grok-4.6-high-fast' HEAD -- hackathon-ecc | wc -l` at HEAD `dd106ade` = **70**. The dd106ade built tree genuinely carries 70; the fix33 staged weave adds the 71st mention (orchestrate picker note) and the schema description adds the 72nd — so SPEC §1(d) (:80, "x70 (fast-worker tier) — unchanged by design") is correct as a dd106ade-tree statement and was rightly left alone. Remaining "fast 70" / "x70" hits in live docs were adjudicated and are all correctly framed: SPEC:15 (fix30-tree census, a different tree), SPEC:102 (D33-16 derivation history), SPEC:125/:241 + MANIFEST:170/:247 + impl-report:163/:192/:234 + fix33.py:68/:547/:569 + patch-log:65/:87 (all "70 → 71" / "not x70" correction-history framings). No other live "fast 70" survives.

## 4. A-M2 — fixed in substance

SPEC §3(h) at :221 now reads (D33-33 form):
> "full MODEL check at the entries of `commands/gan-build.md`, `commands/gan-design.md`, `commands/astra-review.md`, and `skills/orch-pipeline/SKILL.md` Step 0 — the MODEL check is its first content, before the classifier's scoring text"

Whole-doc grep for "before the size classifier" / "before the classifier" over SPEC, MANIFEST, implementation report, `fix33.py`, `verify33.py`, patch log: every remaining occurrence already uses the correct form — SPEC D33-22 (:108) + D33-33 (:120), `fix33.py` DECISION-33-22 (:553) + DECISION-33-33 (:564), `verify33.py` §16m check name (:3723), patch-log DECISION-33-22 (:71) — all "before the classifier's scoring text". The two quotes of the old phrasing (SPEC §3(i) "reworded" note :126, `fix33.py` DECISION-33-39 :570, patch-log :88) are explicitly framed as the reworded wording. No other live spot exists. (The pointer ":217" for this line is stale — see A-M1; the line is :221.)

## 5. Verifier + scans — re-run by me, §16n read, probe confirms detection

- **`python3 verify33.py <built-tree>`: 592/592 checks pass, exit 0** (my run; matches saved `verify33-run33e.txt`).
- **Scan r4 (re-run in place): ALL PASS, 76/76, exit 0** (76 PASS lines + RESULT line = 77 `PASS` matches).
- **Scan r5 (probe dir with the script + `fix32.py` + `fix32-patch-log.md` together): ALL PASS, 100/100, exit 0** (100 PASS lines + RESULT line). Note: the script resolves `fix32.py` relative to the script's own location, not the CWD — running the fix33/ copy from a probe dir fails with `FileNotFoundError: fix32.py` (same as audits #111-B/#112-B); the script itself must be copied into the probe dir. Probe dir deleted after.
- **§16n read, not just executed** (`verify33.py:3727–3850`, **27 `check(` calls** = 21 + 6 B-N1). The 6 new B-N1 checks genuinely assert presence + order:
  1. `MODELSEL_F33` present in built `skills/design-taste-frontend/SKILL.md`;
  2. the full `_ASK33` text present in the built skill;
  3. `MODELSEL_F33` present in the staged source (`new-skills/design-taste-frontend/SKILL.md`);
  4. order: `# Taste skill v2.5.1` line < `MODELSEL_F33` line < `## House rules` line, AND `_guard_before33(skill, "Redesign of an existing page")` — `_guard_before33` returns true only when the MODELSEL line index is < the routing-paragraph line index (`_line_idx33` = first line containing the needle, −1 if absent);
  5. the fan-out paragraph still present in `redesign.md` (both key sentences: "Past three pages, give each page to its own subagent" and "each page subagent is a single-task factory drone with a director brief");
  6. patch-log decisions D33-36…D33-39 recorded.
- **Probe (planted violation, full probe copy under `fix33/audit113-probe/repo/`, deleted after):**
  - Clean copy: **592/592, exit 0** (harness faithful).
  - Probe: deleted the MODEL check line from the probe copy's built skill (`skills/design-taste-frontend/SKILL.md:18`, `grep -c MODELSEL_F33` = 0 before the verifier ran) → **589/592, exit 1**, exactly the 3 related B-N1 FAILs ("MODELSEL_F33 present in skills/design-taste-frontend/SKILL.md", "full MODEL check ask at the entry of skills/design-taste-frontend/SKILL.md", "MODEL check is the first content of the skill and precedes the redesign routing paragraph"). The staged-source, fan-out-presence, and patch-log checks correctly still pass. The verifier detects a missing B-N1 guardrail precisely.
  - The first `cp -al` attempt produced ownership warnings on stderr (same class as the round-33e report's invalid first probe attempt) but the copy itself succeeded and the clean probe ran 592/592, so this probe is valid. See O-5 for the hardlink accident on this probe and its restoration.

## 6. Diff stat, census, and consistency — all verified

- `git diff --stat` (scratch-repo, HEAD `dd106ade`): **49 files changed, +200/−126** (measured by me). Quoted identically in `MANIFEST.md:68` and `fix33-implementation-report.md:240` (the report cites :67/:230 — stale pointers, see A-M1; the quoted text is right).
- Grep for stale `+135` / `+136` / `+166` / `+196` / `47 files changed` across SPEC, MANIFEST, implementation report, `fix33.py`, `verify33.py`, patch log: **zero hits** in live docs. (The run-10 `+196/−126` quotes survive only in the round-33d report and audits #112 / sweep #55, explicitly framed as that round's as-of-then state — legitimate history.)
- Trigger manifest: **48 keys**, coverage `skills 72 / withTriggers 48`; 72 skill dirs on disk. `ui-ux-pro-max` appears nowhere in it (0 hits, per prior audits — not re-litigated).
- Unpin census re-measured by me (built tree): **ID x0, PROSE x2** (both keeps in `skills/strategic-compact/SKILL.md`, `:68` + `:102`), **XID x0, XPROSE x0, fast x72, bare fast x0**. Frontmatter `model:`: **41× `cursor-grok-4.6-high-fast` + 4× `inherit`**, zero others. `MODEL-PIN` 0 (per verifier §13, passing).
- `fix33.py` REPLACEMENTS = **35** tuples (AST count); change count still 41 (patch log `## Changes (41)`, `## Errors (0)`); `MODELSEL_F33` 31 occurrences in fix33.py. No fix33.py tuple was added in round 33e — change count stays 41, as claimed.
- md5 syncs (canonical + scratch identical): `fix33.py` `a567cdebbb5c6b4e137b776ff8e623f9`; `fix33-patch-log.md` `e1fdaf52b3c8ae26688583ef0cd6f3e7`; `fix-round-33e-report.md` `7f58c88dff6958477110d9c5374aa78a`.
- D33-36…D33-39 present in SPEC §2 (:123–126) and §3(j) (:238–245); MANIFEST header reads "Decisions (D33-1 … D33-39)"; implementation-report §3 likewise.
- Scan maintenance verified: `verify33.py:3118` check name quotes site `design-taste-frontend:446`; r4 (:687) and r5 (:707) regression sites read `("skills/design-taste-frontend/SKILL.md", 446, …)`. The B1 brand-identity line moved :444 → :446 by the +2-line insertion, as claimed.
- **Previously closed bypasses spot-checked, still hold:** B-B1 — `skills/orch-change-feature/SKILL.md:45` `## Removing a feature`, check at :47 (first content), step 1 (find/trace) at :51; B-B2 — `skills/orch-build-mvp/SKILL.md:36` step 1 runs "orch-pipeline Step 0 first" with the inline MODEL ask, command `:29` agrees; B-B5 — `skills/grill-me/SKILL.md:8` check under `# Grill Me`; B-B6 — `skills/feature-expansion/SKILL.md:6` check, decision-record read :8, Phase 0 :45, Phase 1 dispatch :57. D-1 (grill-me trigger) and D-2 (direct-command Step 0) hold on the same reads.
- **Run-11 integrity (from `build-log-run11.txt`):** `BUILD EXIT: 0` (:1366); `fix33: 41 change(s)` + `fix33: OK`; `fix24: 113 change(s)` + `fix24: OK`; `fix31: OK`, `fix32: OK`; `ERRORS: 0` (:950). Global less-flat-ui source pristine: md5 `cef0249fbf37ba096c688ce78fa4377f`, **534 lines** (`~/workspace/cursor-skills/less-flat-ui/SKILL.md`); built `skills/less-flat-ui` is a real directory (`drwxrwx---`), never a symlink.
- `git status` after this audit: 49 modified + untracked `fix32/` + `fix33/` only — exactly the run-11 state (see O-5 for the transient probe accident, restored).

## 7. Shortfall check — the §16n static limit (judgment, as briefed)

The worker notes "§16n is still static presence + order, not execution proof" and "a future edit moving the routing above [the check] would only be caught by the next rebuild + verifier run." **Judgment: acceptable residual limit, recorded — not a finding.** Reasons: (1) the §16n order check *would* catch a moved routing — it asserts check-before-routing in the same file (`_guard_before33`), so the gap is only timing (next rebuild + verifier run), not detection; (2) that is the standing limit of every guardrail in this fix (B-B1..B-B6 share it, and the fix's workflow rebuilds + verifies on every round, so the check runs whenever the tree changes); (3) the live test in a real Cursor chat is still owed (OWED-33-1 / OWED-30-3, Anish on Windows) and is the only thing that could close the execution-proof gap — static verification cannot, and no round has claimed otherwise. The limit is stated honestly in SPEC D33-35/D33-37 and the round-33e report §6; this audit's manual re-trace (§1) and probe (§5) are the coverage argument, as in prior audits.

## Observations (not findings)

- **O-1 — Probe accident by this audit, restored byte-exact (disclosed).** My probe copy used `cp -al` (hardlinks) for speed on a 353 MB tree, and the mutation step rewrote the probe file with `open(p,'w')`, which truncates in place — sharing the inode with the real tree. It deleted line 18 from the REAL `hackathon-ecc/skills/design-taste-frontend/SKILL.md` as well as the probe copy (real-tree `MODELSEL_F33` count dropped to 0; `git diff --stat` transiently read +199/−126). Restored immediately by re-inserting the staged :18 line (byte-identical to the built line, verified by the earlier staged-vs-built diff): built :18 is the check again, `MODELSEL_F33` count 1, staged-vs-built diff is only the known :9–13 description transform, `git diff --stat` is back to 49 files +200/−126, and the verifier re-run on the restored real tree is **592/592**. The probe result itself (589/592, exactly 3 B-N1 FAILs, exit 1) is valid — the mutation was real in both copies and the deletion was verified (`grep -c MODELSEL_F33` = 0) before the verifier ran. Lesson for future probes: never hardlink a probe copy; use `cp -r`, or delete-and-replace (never truncate-in-place) the mutated file.
- **O-2 — `impeccable-critique.md` A/B subagents: review-only AND apparently dormant.** Assessments A/B return assessments/scores/issues; nothing in the file instructs the sub-agents to edit, fix, or write code (the "fix" hits are in the synthesis/report sections, as recommendations). Separately, no live loader was found: `polish-pass/SKILL.md` never links `reference/impeccable-critique.md`. If it is ever wired in, it is B-M3/OWED-33-5 class (review-only), not a code-writing bypass.
- **O-3 — orch-build-mvp L34 narration-key paragraph vs step 1 (carried).** The L34 paragraph sits textually before step 1 (:36) and the direct-trigger-path ordering is not explicitly sequenced (unlike orchestrate L52/L64). No scoping, slicing, Gate 1, expansion, dispatch, or build step precedes the check; the prompt is conditional (demo video asked only), never blocks. Untouched by design (sweep #55 O-1). A one-line "after the MODEL check" note would close the ambiguity if the skill is ever edited.
- **O-4 — Review-only dispatches unchanged by design (OWED-33-5).** `skill:council` (deliberation), the Hallmark review subagents, the impeccable A/B assessments — all review-only, all recorded not fixed. Outside claimed scope.
- **O-5 — `fix33.py` still load-bearing for the gan-build/gan-design/ecc-gan-planner/README pins** (carried from audit #112-A O-1). B-M2 moved only the five orch-* design-role lines into build.sh; the fix13e NEW-side pin writes into those four files are still scrubbed by fix33.py's remaining tuples. A build without fix33.py would reintroduce those pins. Disclosed in the patch log's DECISION-33-31; narrowed, not eliminated.
- **O-6 — Live test still owed.** OWED-33-1 / OWED-30-3: the guardrail has never been exercised in a real Cursor chat; only Anish can do it on Windows. Static verification cannot close it.
- **O-7 — Leftover probe dirs from prior audits.** `fix33/audit112-probe/` (audit #112-A's, noted in #112-B O-6) was still present during this audit; my own `audit113-probe/` and `audit113-r5probe/` were deleted after use. Left untouched, per the no-edit rule for other audits' artifacts.

## Files checked (built tree unless noted)

`new-skills/design-taste-frontend/SKILL.md` (staged, :1–30, :456) + `hackathon-ecc/skills/design-taste-frontend/SKILL.md` (:16–26, :456, staged-vs-built diff); `skills/design-taste-frontend/references/hallmark/references/redesign.md` (`## Build`, :68); `manifests/context-packs/skill-triggers@1.json` (:93–101, all 48 keys); `skills/orch-change-feature/SKILL.md` (:34, :41–51), `skills/orch-build-mvp/SKILL.md` (:36), `commands/orch-build-mvp.md` (:29), `skills/grill-me/SKILL.md` (:6–9), `skills/feature-expansion/SKILL.md` (:6–8, :45–57), `skills/orch-pipeline/SKILL.md` (:41–43, :64), `skills/orchestrate/SKILL.md` (:52, :103), `skills/orch-add-feature/SKILL.md` (:13, :31), `skills/orch-fix-defect/SKILL.md` (:13, :33), `skills/orch-refine-code/SKILL.md` (:13, :33–35), `skills/council/SKILL.md` (subagent lines), `skills/gan-style-harness/SKILL.md` (routing note), `skills/polish-pass/SKILL.md` (reference loads) + `reference/impeccable-critique.md` (head, orchestration, Assessments A/B), `skills/orchestrate/references/call-map.md` (dispatch lines sampled), `dispatch-prompt.md` (head), `patterns.md`; all 55 `commands/*.md` (MODELSEL + subagent/dispatch grep); all 72 `skills/*/SKILL.md` (full subagent/dispatch/MODELSEL census); all 203 `skills/*/references/**` + `skills/*/reference/**` markdown files (subagent/dispatch/spawn grep); `rules/*.mdc` (all subagent/dispatch lines); `hooks/*.js` (subagent/Task grep); `fix33/SPEC.md` (§0, §1(d), §2 D33-36…39, §3(e)/(h)/(j), §4), `fix33/MANIFEST.md`, `fix33/fix33-implementation-report.md`, `fix33/fix33.py` (DECISION-33-4 :535, REPLACEMENTS AST count), `fix33/verify33.py` (§16n :3727–3850, :3118, `_guard_before33`/`_line_idx33`), `fix33/fix33-patch-log.md` (:7, :53, Changes/Errors), `fix33/build-log-run11.txt` (:950, :968, :1082, :1282, :1324–1357, :1366), `fix33/fix-round-33e-report.md`, `fix33/audit112-report-A.md`, `fix33/audit112-report-B.md`, `fix33/sweep55-report.md`, `fix33/dryrun52-report.md`, `fix33/scan32-r4-test-fix33.py` (:687), `fix33/scan32-r5-test-fix33.py` (:707).

## Exact commands / results

```
cd scratch-repo && git rev-parse --short HEAD        -> dd106ade
git diff --stat HEAD | tail -1                        -> 49 files changed, 200 insertions(+), 126 deletions(-)
git status --short                                    -> 49 modified + untracked fix32/, fix33/ only
# B-N1
sed -n '18p' new-skills/design-taste-frontend/SKILL.md
sed -n '18p' hackathon-ecc/skills/design-taste-frontend/SKILL.md
  -> identical full MODEL check line (both); MODELSEL_F33 1x in each
grep -n "Redesign of an existing page" <staged + built>  -> :456 both
grep -n "Past three pages" redesign.md                   -> :68
diff staged built design-taste-frontend SKILL.md         -> only :9-13 description transform
sed -n '93,101p' skill-triggers@1.json                   -> skill:design-taste-frontend, 8 phrases incl. "redesign the landing page" :95, "redesign the app ui" :99
python3 json load triggers                               -> 48 keys; coverage skills 72 / withTriggers 48
grep -rn "own subagent" hackathon-ecc/                   -> redesign.md only
grep fan-out variants whole built tree                   -> redesign.md:68 only
# hunt enumerations (counts in §2 table)
grep -rl MODELSEL_F33 commands/                          -> 11 files, each 1x
python3 72-skill census                                  -> 13 skills with any subagent/dispatch mention; 59 with zero
python3 203 references files                             -> 12 unique files with hits (all classified in §2)
grep -rn -i "subagent" rules/                            -> common-agents, hackathon-mode, ponytail (footer note) only
grep -rn -i "subagent|Task(" hooks/*.js                  -> subagent-start.js / subagent-stop.js audit hooks only
# S-M1/A-M1/A-M2
git grep -o 'cursor-grok-4.6-high-fast' HEAD -- hackathon-ecc | wc -l  -> 70
grep -rho 'cursor-grok-4.6-high-fast' hackathon-ecc | wc -l            -> 72
SPEC:9 x71; SPEC:205 (16f) "fast 71"; SPEC:249 (S4) x71; fix33.py:535 x71; patch-log:53 x71
SPEC:221 (3h) "Step 0 — the MODEL check is its first content, before the classifier's scoring text"
grep -rn "fast 70|x70" live docs -> only correctly-framed history (SPEC:15, :80, :102, :125, :241; MANIFEST:170, :247; impl-report:163, :192, :234; fix33.py:68, :547, :569; patch-log:65, :87)
grep -rn "before the size classifier|before the classifier" live docs -> only correct-form + explicitly-framed reword quotes
# verifier + scans (own re-runs)
python3 verify33.py <built-tree>                          -> 592/592 checks pass, EXIT 0
python3 scan32-r4-test-fix33.py <built-tree>              -> RESULT: ALL PASS (76 checks), EXIT 0
# r5 from probe dir with script + fix32.py + fix32-patch-log.md together
python3 scan32-r5-test-fix33.py <built-tree>              -> RESULT: ALL PASS (100 checks), EXIT 0
# probe copy (hardlinked full scratch-repo copy under fix33/audit113-probe/repo/, deleted after)
python3 verify33.py <probe>/hackathon-ecc                 -> 592/592, EXIT 0 (clean)
# Probe: delete probe built skills/design-taste-frontend/SKILL.md:18 (MODELSEL 0 before verifier ran)
python3 verify33.py <probe>/hackathon-ecc                 -> 589/592, EXIT 1 (exactly 3 §16n B-N1 FAILs)
# probe accident + restoration (see O-1): real-tree line 18 restored from staged :18
python3 verify33.py <built-tree> (after restoration)      -> 592/592 checks pass, EXIT 0
git diff --stat HEAD | tail -1 (after restoration)         -> 49 files changed, 200 insertions(+), 126 deletions(-)
# consistency
grep -rh "^model:" hackathon-ecc/agents/ | sort | uniq -c  -> 41 cursor-grok-4.6-high-fast / 4 inherit
built census: ID 0, PROSE 2 (strategic-compact :68/:102), XID 0, XPROSE 0, fast 72, bare 0
grep -rn "+135|+136|+166|+196|47 files changed" live docs  -> zero hits
md5sum fix33.py (canonical + scratch)                     -> a567cdebbb5c6b4e137b776ff8e623f9 (identical)
md5sum fix33-patch-log.md (canonical + scratch)           -> e1fdaf52b3c8ae26688583ef0cd6f3e7 (identical)
md5sum fix-round-33e-report.md (canonical + scratch)      -> 7f58c88dff6958477110d9c5374aa78a (identical)
md5sum global less-flat-ui SKILL.md                       -> cef0249fbf37ba096c688ce78fa4377f, 534 lines
ls -la hackathon-ecc/skills/less-flat-ui                   -> drwxrwx--- (real directory)
grep BUILD EXIT / fix33: / fix24: / fix31: / fix32: / ERRORS build-log-run11.txt
  -> BUILD EXIT: 0; fix33: 41 change(s), OK; fix24: 113 change(s), OK; fix31: OK; fix32: OK; ERRORS: 0
```

Nothing was committed by this audit. The probe copy (`fix33/audit113-probe/`) and r5 probe dir (`fix33/audit113-r5probe/`) were deleted after use. The real tree was left exactly as run 11 left it (49 files, +200/−126; verifier 592/592 re-run after the O-1 restoration).

## Recommended rework (small, docs-only, six pointers)

1. `SPEC.md:242`: ":217" → ":221".
2. `fix-round-33e-report.md:28`: "SPEC.md:201" → "SPEC.md:205".
3. `fix-round-33e-report.md:29`: "SPEC.md:237" → "SPEC.md:249".
4. `fix-round-33e-report.md:30`: "fix33.py:522" → "fix33.py:535".
5. `fix-round-33e-report.md:40`: "SPEC.md:217" → "SPEC.md:221".
6. `fix-round-33e-report.md:123`: "MANIFEST.md:67" → "MANIFEST.md:68"; "fix33-implementation-report.md:230" → "fix33-implementation-report.md:240".

No tree change, no rebuild, no verifier change is needed. After those edits, round 33e should pass re-audit.
