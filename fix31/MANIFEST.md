# Fix #31 MANIFEST — design-library additions (GetLayers, GSAP, React Bits, Hairline illustrations)

## 0. Status (fill in as verification lands)

- Implementation: DONE (5 new staged skills, palette-first / DESIGNPKG-AUTO / inventory weave, build.sh loop + fix31 hook, fix31.py, verify31.py).
- Build run 1: DONE, exit 0 (fix30 OK, fix31 OK, 11 changes; STEP 5 counts 72/45/48/55/15). Log: `fix31/build-log-run1.txt`.
- verify31.py: DONE, **380/380, exit 0** (run 1). Log: `fix31/verify31-run1.txt`.
- Build run 2: DONE, exit 0 (after the 97-A1 fix; STEP 5 counts 72/45/48/55/15). Log: `fix31/build-log-run2.txt`. Differs from run 1 only in the ECC re-clone/install block (run 1 re-cloned because /tmp was wiped; run 2 reused the clone) + an npm timing line.
- verify31.py: DONE, **380/380, exit 0** (run 2). Log: `fix31/verify31-run2.txt`.
- Audit loop / sweep / dry-run: ROUND 1 DONE — Audit #97-A NOT PASS (0 blocking, 1 minor: 97-A1, GetLayers $199 price — FIXED, see §3; price dropped from the skill + fix31.py/template + MANIFEST, live $249 recorded in SPEC + MANIFEST), Audit #97-B PASS (0/0), Sweep #41 CLEAN (0/0), Dry-run #46 PASS (legs 1–8; leg 5's 0-BROKEN target NOT MET as written — the 2 BROKEN lines are the pre-recorded OWED-31-3 stale-map artifact, 0 real breakage; design leg 27/27 across all four sources). No re-dry-run in round 2: the single fix touches no dry-run leg input (no leg greps the skill for a price; the design leg's prompt path is unchanged). ROUND 2 DONE — Audit #98-A PASS (0/0; 97-A1 fix verified; OWED-30-5 + OWED-31-4 adjudicated as recorded), Audit #98-B NOT PASS (0 blocking, 1 minor: 98-B1 — OWED-31-3's premise fails, the DESIGNPKG-AUTO additions ARE dispatch edges under the generator's own rules, so the call map must be regenerated), Sweep #42 CLEAN (0/0; no-re-dry-run rationale confirmed). ROUND 2 FIX IN PROGRESS (98-B1): call map regenerated from the current tree (generator EXPECTED 67→72 + "Skills (72)" header; 5 new called-skill rows incl. hairline-adopt → hairline-create and gsap → react-bits edges; sidecar counts 72/45/48/55/15/49; verify31 check 10g updated 67→72); build run 3 DONE, exit 0 (staged map == built map, md5 a2e7454e…); verify31 run 3 DONE, 380/380, exit 0; dry-run leg-5 re-run DONE, exit 0, 0 BROKEN (17 EXERCISED / 19 STATIC-OK / 5 DORMANT; runner+fixtures copied to `fix31/leg5-rerun/`, round-1 evidence untouched). ROUND 3 RUNNING (audit99-A, audit99-B, sweep43 — 3 verification subagents spawned Nov 17, 2026 ~05:00 UTC; reports due in `fix31/audit99-report-A.md`, `fix31/audit99-report-B.md`, `fix31/sweep43-report.md`).
- Commit / bundle: NOT YET DONE.

## 1. Scope (SPEC fix31/SPEC.md)

Four resources, ALL free-tier only, no paid plans purchased:

1. **GetLayers** (getlayers.ai) — FREE SET ONLY. MCP requires Full Stack Lifetime — NOT wired; skill/prompts path only. Licence bars scraping/redistribution/resale — the plugin vendors NO GetLayers content, reference only. A layer is a foundation, not a finished brand — restyle, never ship trial layers unchanged. **Weight (direction update, Anish Nov 16, 2026 ~10:02 PM CT): GetLayers prompts are a first-class, high-priority source — consulted FIRST in the palette inventory, the direction leans on them heavily as its foundation; the direction cites the layers USED or CONSIDERED-AND-REJECTED with a D19 reason.**
2. **GSAP** — 100% free incl. all former Club plugins, commercial use, public npm; NOT OSI open source (Webflow "Standard no charge" licence; bans competing no-code animation builders); install from npm at build time, never vendor source; official MIT skills at github.com/greensock/gsap-skills (8 skills) as reference.
3. **React Bits** (reactbits.dev) — MIT + Commons Clause (may NOT sell/sublicense/redistribute the components); plugin skill = catalog + install guide, no embedded source; install fresh per-project via shadcn CLI.
4. **Hairline illustrations** (Lucas Marques) — MIT, 33 interactive isometric SVG figures, zero runtime deps, ESM-only; `npm i @lucasmarkes/hairline@0.5.1` or shadcn registry; skills `hairline-create` + `hairline-adopt` vendored as reference. Hairline UI is a DIFFERENT product and NOT in scope.

## 2. What changed

### (a) Counts

| | Before (fix #30) | After (fix #31) |
|---|---|---|
| Skills | 67 | **72** (+5: getlayers, gsap, react-bits, hairline-create, hairline-adopt) |
| Agents | 45 | 45 |
| Rules | 48 | 48 |
| Commands | 55 | 55 |
| Hooks | 15 | 15 |
| Trigger keys | 49 | 49 (no trigger keys for the new skills, same as MotionSites) |

### (b) New staged skills (`new-skills/`)

- `getlayers/SKILL.md` — original skill: prompt-first workflow (browse live library → copy the layer's prompt → rebuild in the project stack → restyle → download media locally, never hotlink). No MCP calls, no vendored content, NO frozen counts (reads `llms.txt` live). Priority section: consulted FIRST, first-class foundation, direction cites layers USED/CONSIDERED-AND-REJECTED.
- `gsap/SKILL.md` — original skill: pinned install `gsap@3.15.1` (+ `@gsap/react`), canonical patterns, performance rules, reference table for the 8 official gsap-skills. No vendored source.
- `react-bits/SKILL.md` — original skill: catalog + install guide (`npx shadcn@latest add @react-bits/<Component>-<JS|TS>-<CSS|TW>`), variants, licence, routing (React/Next only). No embedded component source; the dir contains only SKILL.md.
- `hairline-create/` + `hairline-adopt/` — vendored MIT copies from github.com/lucasmarkes/hairline (skills/ dirs, HEAD at clone time Nov 17, 2026) + the repo LICENSE in each. Unmodified apart from the framing header (HAIRLINE_F31; maps `/hairline-create` to the skill by name; notes Hairline UI is out of scope). Zero promo/upsell content in the vendored files (verified by grep). The create skill ships its engine (`kernel.js`), page (`bench.html`), check scripts, and examples.

### (c) Weave (staged, via `fix31/weave31.py` + `fix31/reweave-getlayers-weight.py`)

- DESIGNPKG-AUTO (orchestrate SKILL.md:35 + hackathon-mode.mdc:44): the 5 new skills added to the package list + the palette list; a gloss line per resource; **GetLayers first in the palette list** + priority sentence + citation sentence. Block stays byte-identical between the two files.
- Palette-first (design-taste-frontend SKILL.md:223): GetLayers named FIRST among the sources, with priority language; the other 4 skills added to the design-package list; the citation sentence added.
- Orchestrate inventory paragraph (SKILL.md:70): the fix #31 additions named, with the GetLayers consulted-FIRST weight.
- Design inventory (`new-skills/orchestrate/references/design-inventory.md`): new §12 for the four resources (GetLayers row leads with "Consulted FIRST"); §1 GSAP presets row + §9 GSAP/React Bits rows point at the new usage skills.
- build.sh: the 5 skills added to the new-skills loop; fix31.py hook added after fix30.py, before STEP 5.

### (d) fix31.py (build-time, built tree only)

Census (no writes) + README/trigger writes + post-assertions + regression guards. See `fix31/fix31.py` docstring. Writes: README count lines 67 → 72 (four lines) + fix #31 provenance note; trigger coverage.skills 67 → 72 (withTriggers stays 49). Template: `fix31/fix31.py.template` (byte-identical).

### (e) verify31.py

Derived from verify30.py via `fix31/derive-verify31.py` (2,337 lines). All verify30 checks kept, counts 67 → 72, stale list gains "67 skills"; new §14 fix31 checks (skills, _F31 tokens, DESIGNPKG-AUTO + palette-first weight, inventory §12, license checks, README note, fix31 patch log). The call-map sidecar check (10g) is deliberately LEFT at 67: the sidecar describes the fix28 map, not regenerated in fix31 (OWED-31-3).

## 3. Corrections found live (SPEC conformance)

- **GSAP version:** the SPEC's 3.15.0 (Apr 2026) was already superseded — npm latest is **3.15.1** (verified Nov 17, 2026), matching the inventory's existing pin. The skill pins `gsap@3.15.1`. SPEC corrected with a strikethrough note (DECISION-31-2).
- **GetLayers counts:** live counts drifted in one day — `llms.txt` Nov 17 reads 62 templates / 222 3D scenes / 54 sections / 530 backgrounds / 1,088 gradients, vs the SPEC's 50 / 114 / 10 / 276 / 1,088. The skill carries NO counts; verify31 forbids the frozen Nov 16 figures (DECISION-31-3). SPEC corrected with a note.
- **@lucasmarkes/hairline:** npm latest 0.5.1 (MIT, ESM-only) — matches the SPEC.
- **GetLayers Full Stack price (audit #97-A1, Nov 17, 2026):** the SPEC's and the skill's ($199) was wrong — the live pricing page lists Full Stack Lifetime at **$249** ($499 struck through; $199 is Unlimited Plus). The price is dropped from the skill (prices drift like counts — the skill carries no price); the live $249 is recorded here and in the SPEC correction.
- **Call map regeneration (audit #98-B1, Nov 17, 2026):** OWED-31-3's premise ("the new skills are leaf resources, no new orchestration edges") was wrong under the generator's own rules — backticked skill names in DESIGNPKG-AUTO count as STRONG invokers (the fix28 map records motionsites-web-builder as called from exactly those files), and the dry-run's `skills/`/`agents/`-only grep missed hairline-adopt → hairline-create and gsap → react-bits edges. Fix: regenerated the map from the current tree (`fix28/callmap/generate_call_map.py` EXPECTED 67→72 + "Skills (72)" header; exit 0, all counts OK). The regenerated sidecar adds exactly the 5 new called skills (all with STRONG invokers from orchestrate/hackathon-mode/design-taste-frontend built+staged + INVENTORY from design-inventory §12, plus the two new-skill edges); 6 pre-existing skills gained invokers (git-workflow, integration WEAK-only, motion-foundations, motion-patterns, orchestrate with 2 invokers upgraded WEAK→STRONG from the fix #29 weave, ui-ux-pro-max) and a 7th (error-handling) only reordered its flow stages (same set); 2 commands (plan, pr) gained WEAK invokers only; called status unchanged everywhere; uncalled/second-order/weak-only sets identical. The map .md diff is 38 lines (counts table, "Skills (72)" header, 5 new rows, grown invoker lists, the error-handling flow reorder). verify31 check 10g updated 67→72.

## 4. Verification verdicts

- **Builds:** run 1 exit 0 (STEP 5: 72/45/48/55/15), run 2 exit 0 (after the 97-A1 fix), run 3 exit 0 (after the 98-B1 map regeneration; staged map == built map, md5 `a2e7454e…`). Logs: `fix31/build-log-run1.txt`, `build-log-run2.txt`, `build-log-run3.txt`.
- **verify31.py:** run 1 **380/380, exit 0**; run 2 **380/380, exit 0** (logs byte-identical to run 1); run 3 **380/380, exit 0** (after check 10g 67→72; log differs from run 2 by exactly that one line). Independent re-runs by every auditor/sweep: 380/380 each.
- **Round 1:** Audit #97-A **NOT PASS** (0 blocking, 1 minor: 97-A1 — GetLayers Full Stack price $199, live $249; fixed by dropping the price from the skill + fix31.py/template + MANIFEST, live $249 recorded in SPEC + MANIFEST). Audit #97-B **PASS** (0/0). Sweep #41 **CLEAN** (0/0). Dry-run #46 **PASS** (legs 1–8; leg 5's 0-BROKEN target NOT MET as written — the 2 BROKEN lines are the OWED-31-3 stale-map artifact, 0 real breakage; design leg 27/27 across all four sources, with the GetLayers verbatim-prompt limitation honestly recorded).
- **Round 2:** Audit #98-A **PASS** (0/0; 97-A1 fix verified; OWED-30-5 + OWED-31-4 adjudicated as recorded). Audit #98-B **NOT PASS** (0 blocking, 1 minor: 98-B1 — OWED-31-3's premise fails, the DESIGNPKG-AUTO additions ARE dispatch edges under the generator's own rules, so the call map must be regenerated). Sweep #42 **CLEAN** (0/0; no-re-dry-run rationale confirmed). No re-dry-run in round 2 (the single fix touched no dry-run leg input).
- **Round 2 fix (98-B1):** call map regenerated from the current tree (generator EXPECTED 67→72 + "Skills (72)" header + docstring; exit 0, all counts OK; 5 new called-skill rows incl. hairline-adopt → hairline-create and gsap → react-bits edges; sidecar 72/45/48/55/15/49; verify31 check 10g updated 67→72). Leg-5 re-run (targeted, from a copy in `fix31/leg5-rerun/`): **exit 0, 0 BROKEN** (17 EXERCISED / 19 STATIC-OK / 5 DORMANT; `map=72 tree=72`, `diff=[]`).
- **Round 3:** Audit #99-A **PASS** (0/0; regeneration correct in every substantive respect). Audit #99-B **PASS** (0/0; 10g is the only verifier change; leg-5 re-run verified; regression clean). Sweep #43 **CLEAN** (0/0).
- **SPEC §7 Verification: MET as written.** The audit loop ran 3 rounds; both post-hoc fixes (97-A1 in round 1, 98-B1 in round 2) were each re-audited and re-swept in the following round with clean verdicts, satisfying the fix #27 convention. The dry-run design leg used ≥1 item from each of the four sources (27/27, install-verified). The leg-5 0-BROKEN target, unmet as written in dry-run #46, is MET on the leg-5 re-run after the regeneration.
- **Reports:** `fix31/audit97-report-A.md`, `audit97-report-B.md`, `sweep41-report.md`, `dryrun46/dryrun46-report.md`, `audit98-report-A.md`, `audit98-report-B.md`, `sweep42-report.md`, `audit99-report-A.md`, `audit99-report-B.md`, `sweep43-report.md`, `leg5-rerun/leg5-rerun-output.txt`.

- verify31.py: _/_, exit _.
- Audit #97-A: _.
- Audit #97-B: _.
- Sweep #41: _.
- Dry-run #46: _ (design leg uses ≥1 item from EACH of the four sources).
- SPEC Verification: _.

## 5. Open parent adjudications

- **OWED-30-3 (fix #30 live test — OUTSTANDING, Anish's step):** he runs `fix30/live-test-prompt.md` in Cursor after installing the fix #30 bundle; pass = Extra High ran the parent on both tasks. Not a fix #31 item; carried. It does not block #31.
- **OWED-31-1 (live behavior):** live use of the four resources in a real Cursor build is unverified until real project use — the live smoke test is still skipped since Nov 15. The dry-run design leg is static + install-verified, not a live Cursor build.
- **OWED-31-2 (GetLayers MCP):** stays unwired — it requires the Full Stack Lifetime plan (live $249, verified Nov 17, 2026; the skill carries no price). If Anish ever buys Full Stack, MCP wiring is a separate decision; the skill's prompt path is the free path.
- **OWED-31-4 (Hairline "six figures"):** the vendored hairline-create SKILL.md says "The six figures of @lucasmarkes/hairline are the bar" — verbatim upstream text about the original six; the library now ships 33 (the live repo's own README caption still says "six figures"). Left as upstream wrote it.
- **Generator quirk (audit #99-A O-2):** on a count mismatch the generator writes the map + sidecar BEFORE returning exit 1. Inherited fix #28 behavior, unchanged in fix #31, not in scope.
- **Frozen round-1 records (not edited):** the dry-run #46 report still restates ($199) in its OWED-31-2 line and misstates the leg-8 screenshot path (`leg8-tidylog/leg8-shot.png` vs the actual `fix31/dryrun46/leg8-shot.png`). Historical records of round 1; editing them post-hoc would falsify them.
- **Leg-5 runner epic prose:** the `wire:epic-dormant-in-use` DORMANT line says "no epic commands exist" though 7 `epic-*.md` files ship — inherited verbatim from the original leg-5 script, outcome DORMANT / 0 BROKEN, premise already adjudicated false. Not re-filed.
- **After #31 closes:** Phase 1d (final commit + one verified bundle of the whole tree as the fork point; record commit hash + bundle path in `FACTORY_CURSOR_PLAN.md` and MEMORY), then Phase 2 fork to `~/workspace/hackathon-plugin/factory-cursor/`.

## 6. OWED

- **OWED-31-1:** live behavior of the four resources is unverified until real project use — the live smoke test is still skipped since Nov 15. The dry-run design leg is static + install-verified, not a live Cursor build.
- **OWED-31-2:** the GetLayers MCP stays unwired — it requires the Full Stack Lifetime plan. If Anish ever buys Full Stack, MCP wiring is a separate decision; the skill's prompt path is the free path.
- **OWED-31-3 (SUPERSEDED by audit #98-B1, Nov 17, 2026):** the call map was generator-owned and NOT regenerated in this fix — the new skills were recorded as leaf resources with no new orchestration edges, so the fix28 map stood (its sidecar said 67 skills). Audit #98-B found the premise wrong under the generator's own rules (backticked names in DESIGNPKG-AUTO are STRONG invokers — the motionsites-web-builder precedent — plus hairline-adopt → hairline-create and gsap → react-bits edges), so the map was REGENERATED Nov 17, 2026 (generator EXPECTED 67→72 + "Skills (72)" header; 5 new called-skill rows; sidecar 72/45/48/55/15/49; verify31 check 10g updated 67→72). The old map/sidecar are backed up at `fix31/call-map-pre-regen.md` / `fix31/call-map-data-pre-regen.json`; the generator run log is `fix31/regen31-run1.txt`.
- **OWED-31-4:** the vendored hairline-create SKILL.md says "The six figures of @lucasmarkes/hairline are the bar" — upstream's text about the original six; the library now ships 33 figures. Left as upstream wrote it (the vendored copy is unmodified apart from the framing header).

## 7. Known limitations (carried)

- OWED-30-1 (staged-vs-built pin drift, by design), OWED-30-3 (fix #30 live test outstanding — Anish runs the live-test prompt in Cursor), OWED-30-6 (allow-listed verify30 check-9b smuggled name — recorded, not re-filed), F35 verifier fragility, F-O scope note, check-12b transient.
- Generator quirk (inherited from fix #28, unchanged in fix #31): on a count mismatch the generator writes the map + sidecar BEFORE returning exit 1 — a failed run still overwrites the outputs, then fails loudly. Recorded (audit #99-A O-2), not in this fix's scope.
- The dry-run epic/`/prune` error is NOT re-filed (only `/prune` was dropped in fix #27; all 7 epic commands ship).

## 8. Commit / bundle (fill in)

- Commit: _.
- Bundle: _.
- NOT pushed (sandbox has no GitHub auth — pull from Windows and push, as with #27/#28/#29/#30).
