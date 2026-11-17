# Sweep #43 — fix #31 — INDEPENDENT SWEEP REPORT (round 3)

**Verdict: SWEEP #43: CLEAN** — 0 blocking, 0 minor. The run-3 built
tree passes every check in the sweep scope, and the round-2 fix
(98-B1, the call-map regeneration) is verified fixed in every place
it touches: the regenerated map is staged AND built with identical
md5 `a2e7454e14a0e36feac9fbd031c14e29`, its counts table reads 72/72
with a "Skills (72)" header and all 5 new skill rows present with
STRONG invokers (including the `hairline-adopt` → `hairline-create`
and `gsap` → `react-bits` edges), the sidecar now reads
72/45/48/55/15/49, the generator's `EXPECTED` is 72, verify31 check
10g expects 72, and the dry-run leg-5 re-run is 0 BROKEN. All
round-2 results re-verify unchanged on the run-3 tree (weaving,
stale-count sweep, skill dirs, inventory §12, URLs live with no
further GetLayers drift, regression, GetLayers weight, independent
counts), and `verify31.py` re-run by me passes 380/380, exit 0, with
output byte-identical to the recorded run 3. The stale-map sidecar
saying 67 is gone, as expected — it is not re-filed.

**Scope.** Round-3 re-sweep of the run-3 built tree
(`hackathon-ecc/`, built from fix #30 commit cfb15f9 + fix #31
changes + regenerated call map) + staged sources (`new-skills/`),
per the task brief: (a) weaving, (b) stale-count sweep, (c)
orphan/consistency incl. live URL checks, (d) regression, (e)
GetLayers weight, (f) independent counts, (g) verifier re-run,
(h) post-build drift, plus (i) the regenerated map as a sweep item.
Read-only except this report. I did not trust the coordinator's,
the patch log's, the regen log's, or `verify31.py`'s run-3 claims:
every item below was verified by my own greps, file reads,
counters, hashes, and URL fetches. `build.sh` was not run; the
generator was not run; `fix11/fix11-stage.py` was not run; nothing
was committed, pushed, or messaged. Date: Mon 2026-11-16
(Nov 17, 2026 ~05:00–05:10 UTC).

---

## BLOCKING findings

None. (Numbered 43-Ax: none issued.)

---

## MINOR findings

None. (Numbered 43-Bx: none issued.)

---

## Checks table

| # | Check | Result |
|---|---|---|
| 98-B1 | Round-2 fix: call map regenerated | PASS — map staged == built, md5 `a2e7454e…`, counts table 72/72, "Skills (72)" header, 5 new rows with STRONG invokers incl. both new-skill edges; sidecar 72/45/48/55/15/49; generator `EXPECTED` 72; verify31 10g expects 72; leg-5 re-run 0 BROKEN; pre-regen backups exist |
| (a) | Weaving: 5 new skills in every canonical package/palette list | PASS — DESIGNPKG-AUTO (both files, 3× each skill, byte-identical), palette-first, orchestrate :70, inventory §12 all include all 5; shorthands unchanged from #41/#42 |
| (b) | Stale counts: "67 skills" / frozen GetLayers counts / GSAP 3.15.0 / Hairline UI as in-scope / $199 | PASS — 0 / 0 / 0 (literal) / 0 in-scope (3 Hairline UI hits, all out-of-scope disclaimers) / 0 `$199` (and 0 `$249`) |
| (c) | Orphan/consistency: new skill dir contents, inventory §12 paths, live URLs | PASS — dirs match MANIFEST exactly (staged `diff -r` silent, all 5); all §12 paths exist; all 6 URLs resolve live, GetLayers counts undrifted |
| (d) | Regression: TODO/FIXME/XXX, model pins, fix31.py template, README + triggers, patch log | PASS — 0 TODO/FIXME/XXX in fix31 files; 0 model-pin text in 5 new skills; pin census 49/22/70/0/0; README 72 in all 4 lines + fix31 note; triggers 72/49; patch log 0 errors / 11 changes; GLOBAL-ROUTING md5 `68206505…` |
| (e) | GetLayers weight at all 6 claimed sites | PASS — present at DESIGNPKG-AUTO (both files), design-taste-frontend :224, orchestrate :70, inventory §12, getlayers skill |
| (f) | Independent counts | PASS — 72 skills / 45 agents / 48 rules / 55 commands / 15 hooks / 49 trigger keys, reproduced by my own counts |
| (g) | Verifier re-run | PASS — `verify31.py` re-run by me: 380/380, exit 0, output byte-identical to `fix31/verify31-run3.txt` |
| (h) | Post-build drift | PASS — 0 built-tree files newer than `fix31/build-log-run3.txt` |
| (i) | Regenerated map as a sweep item | PASS — see 98-B1 row and §(i) below |

---

## The round-2 fix (98-B1) — verified fixed

- **Map staged == built:** `new-skills/orchestrate/references/call-map.md`
  and `hackathon-ecc/skills/orchestrate/references/call-map.md` are
  byte-identical (`diff` silent), md5
  `a2e7454e14a0e36feac9fbd031c14e29` for both — the md5 the task
  stated, confirmed by my own hash.
- **Counts table + header:** the map's counts table reads
  `skills | 72 | 72` (agents 45, rules 48, commands 55, hooks 15,
  triggers 49, all count == expected) and the section header is
  `## Skills (72)` (line 63, both copies).
- **The 5 new rows, all with STRONG invokers:** `getlayers` (:92),
  `gsap` (:96), `hairline-adopt` (:99), `hairline-create` (:100),
  `react-bits` (:123) — each lists STRONG invokers from
  `rules/hackathon-mode.mdc`, `skills/design-taste-frontend/SKILL.md`,
  `skills/orchestrate/SKILL.md` (built + staged) plus
  `design-inventory.md` [inventory]. The two new-skill edges from
  audit #98-B §6(d) are present: `hairline-create` lists
  `hairline-adopt/SKILL.md [strong]` (built + staged), and
  `react-bits` lists `gsap/SKILL.md [strong]` (built + staged).
  The `gsap` row also carries its pre-existing library mentions
  (`motion-patterns`, `ui-ux-pro-max`, icon/fixture JSONs), as
  #98-B recorded.
- **Sidecar:** `fix28/callmap/call-map-data.json` counts read
  `{"skills": 72, "agents": 45, "rules": 48, "commands": 55,
  "hooks": 15, "triggers": 49}`; uncalled skills are exactly
  `['context-budget', 'vite-patterns']` (2), uncalled agents 9,
  commands 6, rules 0; second-order orphans are agents 3
  (`ecc-docs-lookup`, `ecc-fastapi-reviewer`, `ecc-mle-reviewer`)
  + commands 4 (`harness-audit`, `python-review`, `skill-create`,
  `skill-health`) — matching the regen log.
- **Generator + verifier pins updated:** `fix28/callmap/generate_call_map.py:100`
  now reads `EXPECTED = {"skills": 72, …}`; `fix31/verify31.py:1573`
  (check 10g) asserts the sidecar counts equal
  `{"skills": 72, "agents": 45, "rules": 48, "commands": 55,
  "hooks": 15, "triggers": 49}`. The regen log
  (`fix31/regen31-run1.txt`) shows all six counts OK against the
  72 expectation, 1,354 corpus files scanned, map + data written.
- **Map diff vs pre-regen backup is exactly the claimed 38 lines:**
  counts table 67→72, "Skills (67)"→"Skills (72)", the 5 new rows,
  and grown invoker lists on pre-existing rows (7 skills + 2
  commands gained invokers only, per MANIFEST §3 — e.g.
  `git-workflow`, `motion-foundations`, `motion-patterns`,
  `orchestrate`, `ui-ux-pro-max` gain the new-skill STRONG
  invokers; the `error-handling` row only reorders its use column).
  No other structural change.
- **Pre-regen backups exist:** `fix31/call-map-pre-regen.md`
  (md5 `b066413a1a7dd6efcd8571c8abf93942` — the md5 audit #98-B
  recorded for the stale map) and
  `fix31/call-map-data-pre-regen.json` (counts 67/45/48/55/15/49,
  confirmed by my own read).
- **Build run 3 + leg-5 re-run:** `fix31/build-log-run3.txt` ends
  `fix31: OK` / `build complete`, `BUILD EXIT: 0`, STEP 5 counts
  72/45/48/55/15. `fix31/leg5-rerun/leg5-rerun-output.txt` ends
  `BROKEN: 0` (19 STATIC-OK, 17 EXERCISED, 5 DORMANT), with
  `skills:map-agrees -- map skills=72 tree skills=72; diff=[]`
  and `counts:skills -- map=72 tree=72`.

## Notes / observations (checked and cleared)

### (a) Weaving — PASS, shorthands unchanged from #41/#42

- **DESIGNPKG-AUTO**, `skills/orchestrate/SKILL.md:35` and
  `rules/hackathon-mode.mdc:44`: 3,463 chars each, md5
  `6f74770f3e897b3115caecd6177ed90d` — byte-identical to each other
  and unchanged from #41/#42. Each of the 5 skills occurs 3× in
  each copy (package list, palette list, gloss line). The palette
  list reads `(`getlayers`, `motionsites-web-builder`, `gsap`,
  `react-bits`, `hairline-create`, `hairline-adopt`, …)` —
  `getlayers` first. GetLayers-consulted-FIRST sentence +
  used/considered-and-rejected citation sentence present.
- **Palette-first**, `skills/design-taste-frontend/SKILL.md:224`:
  all 5 skills named once each; `getlayers` FIRST (char index 371,
  ahead of `motionsites-web-builder` at 533); citation sentence
  present.
- **Orchestrate inventory paragraph**, `skills/orchestrate/SKILL.md:70`:
  "the fix #31 additions (GetLayers prompt-first layers — consulted
  FIRST in the palette inventory, the first-class foundation — GSAP
  animation, React Bits components, Hairline illustrations — see §12
  of the inventory)".
- **Design inventory §12**,
  `skills/orchestrate/references/design-inventory.md:168–186`: new
  section for the four resources, GetLayers row leads with
  "Consulted FIRST"; §1 GSAP presets row (:34) and §9 row (:146)
  point at the new usage skills (`skills/gsap/SKILL.md`,
  `gsap@3.15.1`).
- **Staged vs built:** `diff -rq` over all 5 new skill dirs is
  silent. The DESIGNPKG-AUTO staged-vs-built pin drift
  (OWED-30-1 class) is unchanged from #41/#42.

**Sites that still omit the 5 — unchanged from #41/#42, not re-filed.**
Spot-check basis unchanged: `skills/orchestrate/SKILL.md:66` and
`:139` and `skills/feature-expansion/SKILL.md:156` still contain 0
hits for `getlayers`/`motionsites` — the same surface-conditional
shorthands #41 recorded. No new omission appeared in run 3.

### (b) Stale-count sweep — CLEAN (own greps, excl. `node_modules`)

| String | Occurrences | Notes |
|---|---|---|
| `67 skills` | **0** | in `.md`/`.mdc`/`.json` |
| `50 templates` / `114 WebGL` / `276 backgrounds` / `10 animated sections` | **0** each | frozen Nov 16 figures absent |
| `62 templates` / `222 3D` / `54 sections` / `530 backgrounds` / `1,088` | **0** each | drifted Nov 17 figures also absent — skill carries no counts |
| `gsap@3.15.0` / `GSAP 3.15.0` / literal `3.15.0` in `.md`/`.json` | **0** | GSAP pin is `3.15.1` (9 hits in `.md`/`.mdc`, incl. gsap skill, design-inventory :146/:183) |
| `$199` / `$249` | **0** each | no price anywhere in the live tree |
| `Hairline UI` | **3** | all explicit out-of-scope disclaimers (hairline-create :7, hairline-adopt :7, design-inventory :185) |

### (c) Orphan/consistency sweep — CLEAN

**New skill dirs — contents match the MANIFEST exactly** (own
`find`, staged `diff -r` silent for all five):

- `skills/getlayers/` — `SKILL.md` only.
- `skills/gsap/` — `SKILL.md` only.
- `skills/react-bits/` — `SKILL.md` only.
- `skills/hairline-create/` — `SKILL.md` + `LICENSE` + `kernel.js`,
  `bench.html`, `build.mjs` + `validate.mjs`, `examples/riffle.js` +
  `examples/terrain.js`, `concepts.md`, `look.md`, `look.mjs`,
  `read.mjs`, `rules.md`, `source.md` — the MANIFEST's set.
- `skills/hairline-adopt/` — `SKILL.md` + `LICENSE` only.
- No vendored GetLayers content, no React Bits `.tsx`/`.jsx`/`.css`
  source, no vendored GSAP source.

**Inventory §12 paths exist on disk:** all five `SKILL.md` paths
present; §1's `skills/ui-ux-pro-max/data/motion.csv` exists.

**URLs — all 6 key URLs resolve to live pages** (fetched as page
text Nov 17, 2026 ~04:56 UTC):

- `https://getlayers.ai/llms.txt` — live; counts still read 62
  templates / 222 3D scenes / 54 sections / 530 backgrounds / 1,088
  gradients — **no further drift** since the Nov 17 reading. MCP
  confirmed a Full Stack Lifetime benefit; every layer carries a
  commercial licence.
- `https://gsap.com/standard-license` — live; Webflow "Standard no
  charge" licence, IP stays with Webflow, bans competing no-code
  visual animation builders, termination at discretion; FAQ confirms
  all former Club plugins free for commercial use.
- `https://reactbits.dev/get-started/installation` — live; CLI form
  `npx shadcn@latest add @react-bits/SplitText-TS-TW` matches the
  skill verbatim, including the JS/TS + CSS/TW variant rule.
- `https://hairline.lucasmarkes.com` — live; "Thirty-three isometric
  figures", MIT and free — matches the skill/inventory's 33.
- `https://github.com/greensock/gsap-skills` — live, public, MIT,
  24 commits, HEAD `aed9cfd`; 8 skills (`gsap-core`,
  `gsap-timeline`, `gsap-scrolltrigger`, `gsap-plugins`,
  `gsap-utils`, `gsap-react`, `gsap-performance`,
  `gsap-frameworks`) — matches the skill's reference table.
- `https://github.com/lucasmarkes/hairline` — live, public, MIT,
  HEAD `034f4bf` (same commit the vendored copy was verified
  against); "Thirty-three isometric line figures", install
  `npm i @lucasmarkes/hairline`, shadcn registry URL matches the
  skill; `hairline-create` / `hairline-adopt` both documented there.

### (d) Regression sweep — CLEAN

- **TODO/FIXME/XXX in the fix #31 files: 0.** Own grep over the 5
  new skill dirs + orchestrate SKILL.md, hackathon-mode.mdc,
  design-taste-frontend SKILL.md, design-inventory.md, README.md.
- **Model-pin text in the 5 new skills: 0.** Own case-insensitive
  grep for `grok-4.7`, `grok-4.6`, `deepseek`, `qwen`, `claude`,
  `sonnet` over the 5 new skill dirs returns nothing.
- **Pin census (occurrence counts, whole tree excl. `node_modules`):**
  `grok-4.7-extra-high` ×49, `Grok 4.7 Extra High` ×22,
  `cursor-grok-4.6-high-fast` ×70, old `grok-4.7-high` ×0, old
  `Grok 4.7 High` ×0, bare `grok-4.6-high-fast` ×0 (70 = 70, all
  `cursor-`-prefixed). Exactly the SPEC census.
- **GLOBAL-ROUTING block** still byte-identical in orchestrate
  (`SKILL.md:36`) and hackathon-mode (`hackathon-mode.mdc:45`):
  both 2,285 chars, md5 `68206505a08f90474dc4931b0e5fb6bb` — the
  fix #29 golden md5.
- **`fix31.py` == `fix31.py.template`:** md5
  `241e6bcd7804e2e45ab517b3af462cba` for both.
- **README:** 72 skills in all 4 count lines (:13, :37, :39, :41);
  fix #31 provenance note present at :29 with all four `_F31`
  tokens.
- **Trigger coverage:** `manifests/context-packs/skill-triggers@1.json`
  — coverage `{'skills': 72, 'withTriggers': 49}`, 49 trigger keys.
  `build.sh:222` lists all 5 new skills in the new-skills loop; the
  fix31 hook sits at :24136–24146, after fix30 and before STEP 5.
- **Patch log:** 0 errors, 11 changes (`## Errors (0)`,
  `## Changes (11)`).

### (e) GetLayers weight — CONFIRMED at all 6 claimed sites

| Site | Weight language present |
|---|---|
| DESIGNPKG-AUTO, `skills/orchestrate/SKILL.md:35` | "GetLayers prompts are consulted FIRST in the palette inventory — the first-class foundation the direction leans on" + used/considered-and-rejected citation sentence (D19) |
| DESIGNPKG-AUTO, `rules/hackathon-mode.mdc:44` | Same text (stripped byte-identical) |
| Palette-first, `skills/design-taste-frontend/SKILL.md:224` | "`getlayers` FIRST (prompt-first cinematic layers; the first-class foundation the direction leans on — consult its prompts before the other palette sources)" + citation sentence |
| Orchestrate inventory paragraph, `skills/orchestrate/SKILL.md:70` | "GetLayers prompt-first layers — consulted FIRST in the palette inventory, the first-class foundation" |
| Inventory §12, `design-inventory.md:176` | "GetLayers prompts carry the most weight in the palette-first flow — they are consulted FIRST, before the other palette sources, and the direction leans on them heavily as its foundation" + GetLayers row leads with "Consulted FIRST" |
| GetLayers skill, `skills/getlayers/SKILL.md` | Framing header ("consulted FIRST, before the other palette sources… direction leans on GetLayers layers heavily as its foundation… USED or CONSIDERED-AND-REJECTED, each with a D19 reason") + dedicated "Priority in the palette-first flow" section |

Ordering is also as claimed: `getlayers` is first in every palette
list (DESIGNPKG-AUTO palette list, design-taste-frontend :224).

### (f) Independent counts — reproduced

Own counts on disk: skills 72, agents 45, rules 48, commands 55,
hooks 15 (`hooks/hooks.json`, `hooks` list of 15), trigger keys 49
(`skill-triggers@1.json`, `triggers` dict of 49, coverage 72/49).
Build log run 3 agrees (skills 72, agents 45, rules 48, commands 55,
hooks 15). The call-map sidecar now reads 72/45/48/55/15/49 — the
OWED-31-3 staleness is gone (see 98-B1 above).

### (g) Carried items — still standing as recorded, not re-filed

- **OWED-31-4:** vendored `hairline-create/SKILL.md:11` still says
  "The six figures of @lucasmarkes/hairline are the bar" — upstream's
  original-six text; the live repo's own README still carries the
  same "six figures" image caption, confirming it is upstream text.
  Present as recorded.
- **OWED-30-6** (allow-listed verify30 check-9b smuggled name) and
  the dry-run epic/`/prune` error: not re-filed per the brief. The 7
  epic commands ship in `hackathon-ecc/commands/`
  (`epic-claim`, `epic-decompose`, `epic-publish`, `epic-review`,
  `epic-sync`, `epic-unblock`, `epic-validate`); `/prune` absent —
  re-confirmed, not filed.
- **OWED-31-1 / OWED-31-2:** live behaviour unverified until real
  project use; GetLayers MCP unwired. Nothing in this sweep changes
  either.
- **OWED-31-3:** SUPERSEDED — the map was regenerated (see 98-B1);
  the sidecar saying 67 is gone and is not filed as still-stale.

### (h) SPEC conformance — scope MET (unchanged from #41/#42)

Four resources, free-tier only, no paid plans; 5 skills (Hairline is
two, per SPEC); palette-first + DESIGNPKG-AUTO + inventory §12 weave;
verify31 §14 checks; no pin/routing/debloom/design-package/grill-me
change. Both SPEC corrections honoured: GSAP pinned at 3.15.1, not
3.15.0; GetLayers counts not frozen anywhere; the skill carries no
price, per the 97-A1 fix.

### (i) Verifier runs — my own re-run

- **`verify31.py`, re-run by me: 380/380 checks pass, exit 0.**
  Output is **byte-identical** to the recorded run-3 log
  (`fix31/verify31-run3.txt`, md5 `d3ac4f33d8901ea4ad90f3d81b2c97b5`
  for both). Run took ~16 s.

### Observations (not findings)

1. **Leg-5 re-run prose vs disk (epic wording).** The leg-5 re-run
   output's `wire:epic-dormant-in-use` line says "no epic commands
   exist in the tree", but 7 `epic-*.md` files do exist in
   `hackathon-ecc/commands/` (re-confirmed above). The wording is
   inherited verbatim from the original leg-5 script
   (`fix31/dryrun46/dryrun46-leg5.py:255`, same comment) — it was
   not introduced by the re-run, the check's outcome is DORMANT
   with 0 BROKEN, and per the brief the epic/`/prune` matter is
   not re-filed. Recorded here only so the prose mismatch is not
   mistaken for a new defect.
2. **One stale $199 survives — in a frozen round-1 record, not the
   tree.** `fix31/dryrun46/dryrun46-report.md:366` still reads the
   old `$199` in its OWED-31-2 line (recorded by audit #98-A §9,
   not re-filed). The live tree has 0 `$199` / 0 `$249`.

### Other

- No file was edited, created, or deleted except this report.
  `build.sh` was not run; the generator was not run;
  `fix11/fix11-stage.py` was not run; nothing was committed, pushed,
  or messaged.
