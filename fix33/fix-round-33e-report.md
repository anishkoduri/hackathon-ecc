# Fix #33 — Round 33e report (audit #112-A / #112-B + sweep #55 findings)

- **Date:** Tue Nov 17, 2026 (evening, CST)
- **Fix dir:** `~/workspace/hackathon-plugin/fix33/`
- **Scratch repo:** `~/workspace/hackathon-plugin/fix33/scratch-repo`, git HEAD `dd106ade`
- **Round under report:** fix round 33e (fixes audit #112-B B-N1 blocking, audit #112-A A-M1/A-M2 minor, sweep #55 S-M1 minor — S-M1 is the same issue as A-M1)
- **Status:** all four findings fixed; rebuild run 11 green; verifier **592/592**; scans r4 76/76 + r5 100/100. **NOT committed, NOT bundled, NOT pushed.**

## 0. What was wrong

Audit #112-B came back NOT PASS with 1 blocking finding (B-N1: a new bypass of the same class as B-B6 — a trigger-routed skill dispatching code-writing subagents on Auto with no MODEL check). Audit #112-A came back NOT PASS with 2 minor findings (A-M1: stale "fast 70" census number; A-M2: a leftover of the exact incoherence A-M2 was assigned to reword). Sweep #55 came back NOT CLEAN with 1 minor finding (S-M1: the same stale "fast 70" in five live spots, of which audit #112-A named one). Nothing else in either audit or the sweep failed: all six #111-B bypasses were confirmed closed, B-M2 fixed at the root, the unpin census held, and the verifier + both scans reproduced green at 586/586.

## 1. Findings fixed

### B-N1 — trigger-routed Hallmark redesign fans out page drones past three pages with no MODEL check (D33-36)

- **The bypass (as audited):** trigger-routed `design-taste-frontend` ("redesign the landing page", "redesign the app ui", …) → `SKILL.md:454` routes a full-page redesign to `references/hallmark/references/redesign.md` → past three pages at restyle/full depth, "give each page to its own subagent" — factory drones that write code. Zero `MODELSEL_F33` anywhere in the skill, staged or built. Narrow (needs 4+ pages at restyle/full depth; 1–3 pages work inline and never dispatch; polish never fans out) but the same class as B-B6, with strictly greater harm than B-B5 (Q&A only).
- **Fix — skill-entry weave (preferred placement).** The full MODEL check (MODELSEL_F33 wording, byte-identical to the grill-me / feature-expansion lines) is woven at the entry of the staged skill, `scratch-repo/new-skills/design-taste-frontend/SKILL.md`, as the first content under `# Taste skill v2.5.1` (new :18, +2 lines; the staged source flows into the built tree, the same mechanism as the round-33c orchestrate re-sequence and the round-33d B-B5/B-B6 staged weaves). **No fix33.py tuple is needed or added** — the change count stays 41 and REPLACEMENTS stays 35 tuples.
- **Why the skill entry and not the top of `redesign.md`.** The entry covers the trigger path and every other load of the skill, and it cannot misfire: the MODEL check only interrupts when the selected model is Auto or undetermined — on a specific selected model it passes silently — so the in-flow routes (orchestrate pre-grill check; orch-change-feature change path → engine Step 0; orch-build-mvp Step 0) re-fire it with no second ask. No context exists in which the skill loads and asking is wrong: the skill's own first work (step 0 "The stack", step 1 "Read the brief", step 4 deal) all follow the check, and the redesign flow's own "The ask" (what must stay / what is wrong / anything new) does not resolve Auto — answering "go ahead" does not pick a model — so it is not a substitute. A `redesign.md`-top check would have covered only the redesign flow, not the skill's other loads, and would have left the trigger path's first work (the deal, the Picks block) ahead of the ask.
- **Scope kept.** The skill's hero/finish review subagents (`gates.md:243`) and the manual-gate / fresh-reader subagents (`gate.md:179-180`, `copy-voice.md:173`) are review-only (B-M3/OWED-33-5 class) and get no targeted weave — the entry check fires before them anyway. Drone pins, fast tier, fix31/fix32 bundles, and the factory round-3 bundle untouched.
- **Verified in the built tree:** built `skills/design-taste-frontend/SKILL.md:18` carries the check; the redesign routing paragraph is now :456; `redesign.md:68` still carries the fan-out paragraph ("Past three pages, give each page to its own subagent … each page subagent is a single-task factory drone with a director brief"); staged-vs-built diff for the skill is only the known pre-existing description-line transform (:9–13) plus the new insertion. See §3 for the manual trace.

### S-M1 + A-M1 — stale fast count "70" in five live spots (D33-38)

- **Measured truth first (re-measured this round, not copied):** pre-state `cursor-grok-4.6-high-fast` **x71**, post-state **x72**. Evidence, all agreeing: regenerated patch-log census line (`x71` pre; post "x72 (71 pre-existing + 1 in the schema description, D33-17)"); `fix33.py` EXPECT `FAST_ID: 71` + post-assertion 72; `verify33.py` §16f asserts fast x72 in the patch log; direct grep of the rebuilt tree = 72.
- **Fix — 70 → 71 in the four source spots** (the patch log regenerates from `fix33.py` on the rebuild — it was not hand-edited; verified after: patch-log :53 now reads "The fast tier (x71)"):
  1. `SPEC.md:9` (§0 scope, D33-4)
  2. `SPEC.md:205` (§3(e) (16f) census series — sharpest instance: 20 ID ✓, 5 PROSE ✓, keeps x2 ✓, fast 70 ✗; now fast 71)
  3. `SPEC.md:249` (§4 What does NOT change)
  4. `fix33.py:535` (DECISION-33-4 string)
  5. `fix33-patch-log.md:53` (regenerated)
- **Whole-dir grep for any other "fast 70" / "x70" statement about this count** (SPEC, MANIFEST, implementation report, `fix33.py`, `verify33.py`, patch log, plus the round/audit/sweep reports): every remaining occurrence was adjudicated as correctly framed and left alone —
  - `SPEC.md:15` — the fix30-tree census (a different tree's measured fact, pre-rename);
  - `SPEC.md:80` (§1(d)) — the dd106ade-tree measurement. Verified this round by `git grep -o 'cursor-grok-4.6-high-fast' HEAD -- hackathon-ecc` = **70**: the dd106ade built tree genuinely carries 70, because the fix33 staged weave adds the 71st mention (orchestrate L93 picker note). Correct as a dd106ade-tree statement;
  - the "not x70" framings inside D33-16 itself (SPEC:102, `fix33.py:534`, patch-log:65, implementation-report:163) and MANIFEST's D33-16 history line — they quote the corrected number to record the correction;
  - the new D33-38 / §3(j) / run-11 entries, which quote "70 → 71" to record this correction.

### A-M2 — SPEC §3(h) still says "Step 0 (before the size classifier)" (D33-39)

- **Fix:** `SPEC.md:221` reworded to the D33-33 formulation: "Step 0 — the MODEL check is its first content, before the classifier's scoring text". Step 0 IS the classifier; the old parenthetical positioned it before the classifier — the same incoherence A-M2 was assigned to reword.
- **Whole-doc grep for any other surviving "before the size classifier" / "before the classifier" phrasing tied to Step 0** (SPEC, MANIFEST, `fix33.py`, `verify33.py`, implementation report, patch log): every remaining occurrence already uses the correct form — SPEC D33-22 (:108) + D33-33 (:120), `fix33.py` DECISION-33-22 (:540) + DECISION-33-33, `verify33.py` §16m check name (:3723), patch-log DECISION-33-22 (:71) — all "before the classifier's scoring text". The two quotes of the old phrasing (SPEC §3(i) "reworded" note, `fix33.py` DECISION-33-33) are explicitly framed as the reworded wording and are left alone. No other live spot existed.

### NOT fixed (observations, per the task scope)

- Sweep #55 O-1 (orch-build-mvp L34 narration-key paragraph vs step 1) stays an observation — not touched.
- Sweep #55 O-2 is B-N1, fixed above as a finding.
- OWED-33-5 (review-only dispatches) stays recorded, not fixed, by design.

## 2. New decisions (D33-36…D33-39)

| Decision | Content |
|---|---|
| D33-36 | B-N1: full MODEL check at the design-taste-frontend skill entry (staged, :18), before the :456 redesign routing → redesign.md :68 fan-out. Placement rationale (skill entry, not redesign.md top), traced path, idempotence in-flow, scope (4+ pages, restyle/full). |
| D33-37 | Verifier §16n extended for B-N1 (+6 checks, 586 → 592) + scan maintenance: r4/r5 design-taste-frontend regression site 444 → 446 (the +2-line insertion shifts the B1 brand-identity line), verify33.py check name updated the same way. |
| D33-38 | S-M1/A-M1: fast 70 → 71 in the five live spots; adjudication of the remaining x70 mentions as correct other-tree/history framings. |
| D33-39 | A-M2 leftover: SPEC §3(h) reworded to the D33-33 formulation; adjudication of the remaining "before the classifier" phrasings. |

Full text in SPEC.md §2 + the `fix33.py` DECISION-33-36..39 strings (patch-log output). MANIFEST Decisions header now reads D33-1 … D33-39; implementation-report §3 likewise.

## 3. B-N1 trace (manual, built run-11 tree — not the verifier alone)

Traced end to end by reading the files, in the rebuilt tree:

1. **Trigger.** `hackathon-ecc/manifests/context-packs/skill-triggers@1.json:93` — `"skill:design-taste-frontend"` routes from "design a landing page" (:94), "redesign the landing page" (:95), "landing page design", "company page design", "design the dashboard", "redesign the app ui" (:99), "dashboard design", "app interface design". A user typing "redesign the app ui" on a 5-page app loads the skill directly (Cursor description routing — the same footing audit #111-B and round 33d accepted for B-B5/B-B6).
2. **Skill entry.** Built `skills/design-taste-frontend/SKILL.md:18` — the full MODEL check, first content under `# Taste skill v2.5.1` (:16), before `## House rules` (:21), before §1, before step 4's deal, before step 5's build. On Auto/undetermined it tells the user to pick a specific model before proceeding; on a specific selected model it passes silently.
3. **Routing.** Built skill :456 — "**Redesign of an existing page (keeping content + wiring).** When the job is a full-page redesign that keeps every fact, link, form, field, handler, route, id, and test hook, follow the Hallmark redesign flow (`references/hallmark/references/redesign.md`) — factory routing for the redesign flow lives there: page subagents are single-task factory drones with director briefs (GLOBAL-ROUTING_F29)." The check at :18 precedes this line (verified by the §16n order check and by read).
4. **Fan-out.** Built `skills/design-taste-frontend/references/hallmark/references/redesign.md:68` ("More than one page" paragraph) — "Past three pages, give each page to its own subagent where the harness has them, with that tokens file, the page's files and this file. **Factory routing (fix #29, GLOBAL-ROUTING_F29):** each page subagent is a single-task factory drone with a director brief (DIRECTOR-BRIEF_F29)…" Each page drone builds its page — code-writing dispatch. The skill-entry check precedes it on every path that reaches it, because every load of the flow passes through the skill file first.
5. **In-flow routes (already covered, re-fire silently).** orch-change-feature `## Landing redesigns` ("The engine steps above still run" — engine Step 0 first) and orchestrate's polish-routed redesign (downstream of the pre-grill MODEL check) both hit a MODEL check before reaching this flow; the new skill-entry check re-fires after the model is picked and passes silently — no second ask. Only the standalone skill-load path was open; it is now closed.
6. **What the check does NOT cover (by design).** The redesign flow's "The ask" (three questions) precedes the build but does not resolve Auto. The hero/finish review subagents and manual-gate / fresh-reader subagents are review-only (OWED-33-5 class). A 1–3 page redesign at restyle/full depth works inline and never dispatches; polish depth never fans out.

## 4. Rebuild + verification (run 11)

### Exact invocation used (run 11)

Recorded here verbatim — the MANIFEST invocation, with run number 11. Fake HOME is `fix33/fakehome33` on real disk, NOT `/tmp`. Pre-build re-sync used `rsync` WITHOUT `--delete` (run 8's accident rule).

```sh
rsync -a --exclude=.git --exclude=hackathon-ecc --exclude='fix*/dryrun*' \
  --exclude='*/demo-sample-video' --exclude='*.webm' --exclude=.npm-cache \
  --exclude=.tmp --exclude=__pycache__ --exclude='fix32/scratch-repo' \
  ~/workspace/hackathon-plugin/fix33/scratch-repo/ \
  ~/workspace/hackathon-plugin/fix33/fakehome33/workspace/hackathon-plugin/
# each run, from fix33/fakehome33/workspace/hackathon-plugin:
HOME=~/workspace/hackathon-plugin/fix33/fakehome33 \
MS_DIR=~/workspace/hackathon-plugin/fix26/scratch-clones/hack-skills \
UIPRO_DIR=~/workspace/hackathon-plugin/fix26/scratch-clones/uipro \
SKILL_SRC=~/workspace/hackathon-plugin/fix26/scratch-clones/skill-add \
TMPDIR=~/workspace/hackathon-plugin/fix33/.tmp \
NPM_CONFIG_CACHE=~/workspace/hackathon-plugin/fix33/.npm-cache \
bash build.sh > ~/workspace/hackathon-plugin/fix33/build-log-run11.txt 2>&1
echo "BUILD EXIT: $?" >> ~/workspace/hackathon-plugin/fix33/build-log-run11.txt
```

- **Run 11 — BUILD EXIT: 0** (`fix33/build-log-run11.txt`). fix24 OK (113 changes), fix33 OK (41 changes), fix31 OK, fix32 OK, ERRORS: 0. Sync-back: built tree (`hackathon-ecc/`, rsync `--delete`) + `fix33/fix33-patch-log.md` only; the five historical logs and the fix31/fix32 regenerated logs were NOT synced back.
- **Pre-build verifier: 588/592, exit 1** (`fix33/verify33-run33e-prebuild.txt`) — exactly the 4 expected FAILs: the 3 new §16n B-N1 built-tree checks + the patch-log D33-36..D33-39 assertion, all against the un-rebuilt run-10 tree. The staged-source check and the fan-out-presence check already passed pre-rebuild (those files were already correct).
- **Post-build verifier: 592/592, exit 0** (`fix33/verify33-run33e.txt`). §16n now 27 checks (21 + 6 B-N1). No CUT allow-list shift: no §12 allow-list entry exists for `skills/design-taste-frontend/SKILL.md` (only its `assets/icons/` data files), so the +2-line insertion tripped nothing — unlike the round-33d B-B6 insertion.
- **Scan r4: ALL PASS (76/76, exit 0)** (`fix33/scan32-r4-run-fix33e.txt`, re-run in place from fix33/).
- **Scan r5: ALL PASS (100/100, exit 0)** (`fix33/scan32-r5-run-fix33e.txt`, probe dir with `fix32.py` + `fix32-patch-log.md` adjacent to the script, probe dir deleted after — in-place run from fix33/ crashes with `FileNotFoundError: fix32.py`, same as audits #111-B/#112-B).
- **Scan maintenance (D33-37, required consequence of the +2-line insertion):** the B1 brand-identity line in the skill moved :444 → :446 (content re-read at the new line), so the r4/r5 regression sites (`skills/design-taste-frontend/SKILL.md`, 444) were re-numbered to 446 in both scripts, and the `verify33.py:3118` check name quoting that site was updated the same way. Same class as the round-33d §12 allow-list re-numbering.
- **Probe (planted violation, full probe copy under `fix33/audit112e-probe/repo/`, deleted after):** deleting the MODEL check line from the probe copy's built skill (`skills/design-taste-frontend/SKILL.md:18`) → **589/592, exit 1**, exactly the 3 related B-N1 checks fail ("MODELSEL_F33 present", "full MODEL check ask at the entry", "first content of the skill and precedes the redesign routing paragraph"). The staged-source, fan-out-presence, and patch-log checks correctly still pass (those files untouched in the probe). The verifier detects a missing B-N1 guardrail precisely. (First probe attempt was invalid — `cp -a` failed to preserve ownership and the `&&` chain skipped the `sed`, so the probe ran unmutated at 592/592; re-run with `cp -r` + explicit deletion check, `grep -c MODELSEL_F33` = 0 before the verifier ran. Recorded so the invalid first attempt is not mistaken for a pass.)

### Post-build confirmations (all measured, not read from the logs)

| Check | Result |
|---|---|
| Built design-taste-frontend skill carries the MODEL check at the chosen placement | :18, first content under `# Taste skill v2.5.1`, staged + built |
| Patch log regenerated with "fast 71" at :53 | "The fast tier (x71) and the drones are untouched." (DECISION-33-4) |
| Patch log "Step 0" labels | DECISION-33-22/33-33 use "before the classifier's scoring text"; D33-36..D33-39 present (39 decisions), Changes (41), Errors (0) |
| Built-tree census | ID 0, PROSE 2 (strategic-compact keeps), XID 0, XPROSE 0, fast 72, bare 0 |
| Agent `model:` inventory | 41 × `cursor-grok-4.6-high-fast` + 4 × `inherit`, zero others |
| Global less-flat-ui source unchanged | md5 `cef0249fbf37ba096c688ce78fa4377f`, 534 lines |
| Built less-flat-ui | real directory (`drwxrwx---`), never a symlink |
| Staged-vs-built design-taste-frontend SKILL.md | only the known description-line transform (:9–13) + the new insertion |
| `fix33.py` copies | canonical + scratch-repo md5-identical (`a567cdebbb5c6b4e137b776ff8e623f9`); REPLACEMENTS still 35 tuples; change count still 41 |
| Patch-log copies | canonical + scratch-repo md5-identical (`e1fdaf52b3c8ae26688583ef0cd6f3e7`) |
| Diff stat | **49 files changed, +200/−126** (see §5) |
| `git status` (scratch-repo) | 49 modified + untracked `fix32/`, `fix33/` only; no probe residue |

## 5. Diff stat

- `git diff --stat` vs HEAD `dd106ade`: **49 files changed, 200 insertions(+), 126 deletions(-)**.
- Delta vs run 10 (47 files, +196/−126): +2 files, +4 insertions — exactly the staged + built design-taste-frontend SKILL.md copies, each +2 lines (the MODEL check line + blank line). No other tracked file changed in this round: `fix33.py` / `verify33.py` / scan scripts live in untracked `fix33/` and do not enter the stat; SPEC/MANIFEST/implementation-report live outside the scratch repo.
- Quoted consistently in MANIFEST.md:68 and `fix33-implementation-report.md:240` (both now read "49 files changed, +200/−126"). Grep for stale stat quotes (`+196`, `47 files`) over SPEC, MANIFEST, implementation report, `fix33.py`, `verify33.py`: **zero hits** in live docs. (The run-10 `+196/−126` quotes survive only in the round-33d report and audit #112 / sweep #55, explicitly framed as that round's as-of-then state — legitimate history.)
- Verifier count quoted consistently as 592: SPEC §3(e) (16n) + D33-37, MANIFEST run-11 entry, implementation-report §5 round-33e bullet. Remaining "586" mentions in live docs are all run-10/33d history or "586 → 592" transitions.

## 6. Honest shortfalls

- **Static checks, not execution proof.** §16n (now 27 checks) asserts presence + line order within files, including the new B-N1 checks. It cannot prove a trigger loads the skill or that the check fires at runtime; the manual trace in §3 is the coverage argument, and the live test in a real Cursor chat is still owed (OWED-33-1 / OWED-30-3, Anish on Windows).
- **The B-N1 guardrail is one line at a skill entry.** If a future edit moves the redesign routing above the check, or duplicates the routing in another file, the §16n order check fails loudly (it asserts check-before-routing in the same file) — but only the next rebuild + verifier run would catch it. Same standing limit as B-B1..B-B6.
- **No live run of any kind was done by this worker** (subagents have no live browser); every number above comes from the build + verifier + scan suites + direct reads, not from Cursor.
- **The first B-N1 probe attempt was invalid** (see §4) — the valid re-run is the one reported (589/592, exactly 3 B-N1 FAILs). The invalid attempt's 592/592 is not a result.
- **O-1 (sweep #55) untouched by design** — the orch-build-mvp L34 narration-key ordering ambiguity remains an observation, not a finding.

## 7. Files changed / deliverables

- `scratch-repo/new-skills/design-taste-frontend/SKILL.md` — MODEL check woven at :18 (+2 lines). The only staged change.
- `scratch-repo/hackathon-ecc/skills/design-taste-frontend/SKILL.md` — same, via the run-11 build.
- `fix33/SPEC.md` — D33-36…D33-39 (§2), §3(e) (16f)/(16n) + §3(j) round-33e, S-M1/A-M1 70 → 71 (§0, §3(e), §4), A-M2 §3(h) reword.
- `fix33/fix33.py` — DECISION-33-4 (x70 → x71), DECISION-33-36…D33-39 strings, round-33e docstring paragraph; synced to `scratch-repo/fix33/fix33.py` (md5-identical).
- `fix33/verify33.py` — §16n +6 B-N1 checks (586 → 592), §16n header comment, patch-log D33-36..D33-39 check, :3118 check name 444 → 446.
- `fix33/scan32-r4-test-fix33.py`, `fix33/scan32-r5-test-fix33.py` — design-taste-frontend regression site 444 → 446.
- `fix33/fix33-patch-log.md` — regenerated on run 11 (41 changes, 39 decisions, 6 OWED, 0 errors); synced to `scratch-repo/fix33/fix33-patch-log.md` (md5-identical).
- `fix33/MANIFEST.md` — run-11 entry, Decisions D33-1 … D33-39, diff stat 49/+200/−126.
- `fix33/fix33-implementation-report.md` — run-11 table row, Decisions D33-1 … D33-39 + round-33e summary, diff stat 49/+200/−126, fix33.py md5 updated.
- `fix33/build-log-run11.txt`, `fix33/verify33-run33e-prebuild.txt` (588/592), `fix33/verify33-run33e.txt` (592/592), `fix33/scan32-r4-run-fix33e.txt` (76/76), `fix33/scan32-r5-run-fix33e.txt` (100/100).
- **This report:** `fix33/fix-round-33e-report.md` (+ md5-identical copy in `scratch-repo/fix33/`).
- **NOT done:** commit, bundle, push — separate legs. Nothing was committed by this round.
