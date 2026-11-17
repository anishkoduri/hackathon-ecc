# Sweep #42 — fix #31 — INDEPENDENT SWEEP REPORT (round 2)

**Verdict: SWEEP #42: CLEAN** — 0 blocking, 0 minor. The run-2 built
tree passes every check in the sweep scope, and the single round-1 fix
(97-A1, the GetLayers $199 price) is verified fixed in every place it
lived: no price remains in the built skill or in any live-tree file,
`fix31.py` matches its template at the new md5, and the patch-log
OWED-31-2 carries no price. All 5 new skills are woven into every
canonical package/palette list, the stale-count sweep is clean, the new
skill dirs match the MANIFEST exactly, every inventory §12 path exists,
all 6 key URLs resolve live (GetLayers counts have not drifted further
since Nov 17), no TODO/FIXME/XXX or model-pin text sits in the
new/edited files, the README and trigger coverage read 72/49, the
GetLayers weight language is present at all six claimed sites, and
`verify31.py` re-run by me passes 380/380, exit 0. The no-re-dry-run
rationale is confirmed (see §(j)): no dry-run leg input changed.

**Scope.** Round-2 re-sweep of the run-2 built tree
(`hackathon-ecc/`, built from fix #30 commit cfb15f9 + fix #31 changes)
+ staged sources (`new-skills/`), per the task brief: (a) weaving,
(b) stale-count sweep incl. the $199 price, (c) orphan/consistency
incl. live URL checks, (d) regression, (e) GetLayers weight,
(f) independent counts, (g) verifier re-run, (h) post-build drift,
plus the round-1 fix 97-A1 re-check and the dry-run rationale check.
Read-only except this report. I did not trust the coordinator's, the
patch log's, or `verify31.py`'s run-2 claims: every item below was
verified by my own greps, file reads, counters, and URL fetches.
`build.sh` was not run; `fix11/fix11-stage.py` was not run; nothing
was committed, pushed, or messaged. Date: Mon 2026-11-16
(Nov 17, 2026 ~04:40–05:00 UTC).

---

## BLOCKING findings

None. (Numbered 42-Ax: none issued.)

---

## MINOR findings

None. (Numbered 42-Bx: none issued.)

---

## Checks table

| # | Check | Result |
|---|---|---|
| 97-A1 | Round-1 fix: $199 price dropped everywhere live | PASS — `$199` 0 in built-tree md/mdc/json; 0 in built getlayers skill, staged skill, fix31.py/template, patch log; fix31.py == template at new md5 `241e6bcd7804e2e45ab517b3af462cba` |
| (a) | Weaving: 5 new skills in every canonical package/palette list | PASS — DESIGNPKG-AUTO (both files), palette-first, orchestrate :70, inventory §12 all include all 5; shorthands unchanged from #41 |
| (b) | Stale counts: "67 skills" / frozen GetLayers counts / GSAP 3.15.0 / Hairline UI as in-scope / $199 | PASS — 0 / 0 / 0 (literal) / 0 in-scope (3 Hairline UI hits, all out-of-scope disclaimers) / 0 `$199` |
| (c) | Orphan/consistency: new skill dir contents, inventory §12 paths, live URLs | PASS — dirs match MANIFEST exactly (staged `diff -r` silent, all 5); all §12 paths exist; all 6 URLs resolve live |
| (d) | Regression: TODO/FIXME/XXX, model pins, fix31.py template, README + triggers, patch log | PASS — 0 TODO/FIXME/XXX in fix31 files; 0 model-pin text in 5 new skills; pin census 49/22/70, old pin 0; README 72 in all 4 lines + fix31 note; triggers 72/49; patch log 0 errors / 11 changes |
| (e) | GetLayers weight at all 6 claimed sites | PASS — present at DESIGNPKG-AUTO (both files), design-taste-frontend :224, orchestrate :70, inventory §12, getlayers skill |
| (f) | Independent counts | PASS — 72 skills / 45 agents / 48 rules / 55 commands / 15 hooks / 49 trigger keys, reproduced by my own counts |
| (g) | Verifier re-run | PASS — `verify31.py` re-run by me: 380/380, exit 0 |
| (h) | Post-build drift | PASS — 0 built-tree files newer than `fix31/build-log-run2.txt` |
| (j) | No-re-dry-run rationale | CONFIRMED — no dry-run leg input changed (see §(j)) |

---

## The round-1 fix (97-A1) — verified fixed

- **Built skill:** `hackathon-ecc/skills/getlayers/SKILL.md:6` now reads
  "the GetLayers MCP … requires the Full Stack Lifetime plan and is
  NOT wired in this plugin" — **no price, no `$199`, no `$249`, no
  `199` at all** in the file (grep `199|249` returns nothing). The
  "No paid plans" prohibition and the MCP-gating fact are intact.
- **Staged skill:** `new-skills/getlayers/SKILL.md` is byte-identical
  to the built skill (`diff` silent), so the fix is in the staged
  source, not a built-tree-only patch.
- **`fix31.py` == `fix31.py.template`:** md5
  `241e6bcd7804e2e45ab517b3af462cba` for both — the new md5 the task
  stated, confirmed by my own hash. Neither file contains `199` or
  `249`.
- **Patch log:** `fix31/fix31-patch-log.md` OWED-31-2 now reads "the
  MCP stays unwired — it requires the Full Stack Lifetime plan" with
  **no price** (grep `199|249` over the whole patch log returns
  nothing). 0 errors, 11 changes, as in run 1.
- **Live-tree price sweep:** `$199` occurs **0** times in built-tree
  `.md`/`.mdc`/`.json` files, and `$249` occurs **0** times — the
  skill carries no price at all, per the fix decision. The only
  `199` substrings in built-tree prose (5 lines) are unrelated: a
  JS-safe-integer id (`9007199254740993123`), a PolyForm hash
  (`…efde19994`, 2×), and "Founded 1994". No standalone `199` price
  figure exists anywhere in the live tree.
- **Deliberate records (not live-tree claims):** the only `$199`
  mentions of the GetLayers price are the two correction notes the
  task expects — `fix31/SPEC.md:19` and `fix31/MANIFEST.md:63` — plus
  `MANIFEST.md:10`'s round-1 summary line recording the fix. All
  three deliberately record the wrong figure alongside the live
  `$249`; none is a live-tree claim.
- **Build-log diff run 1 vs run 2:** the only differences are the
  ECC re-clone/install block present in run 1 (1,977 lines — run 1
  re-cloned because /tmp was wiped, run 2 reused the clone) and one
  npm timing line (`added 9 packages in 2s` in run 2). The fix31
  section, STEP 5 counts (72/45/48/55/15), and `fix31: OK` / `build
  complete` / exit 0 are identical. **Verify logs run 1 vs run 2 are
  byte-identical** (md5 `ae1a392acdb1014954a64ce8f466865f` for both),
  380/380 each — the fix changed no verifier input.

## Notes / observations (checked and cleared)

### (a) Weaving — PASS, shorthands unchanged from #41

**Canonical lists — all 5 present, verified by my own reads:**

- **DESIGNPKG-AUTO**, `skills/orchestrate/SKILL.md:35` and
  `rules/hackathon-mode.mdc:44`: 3,463 chars each, md5
  `6f74770f3e897b3115caecd6177ed90d` (stripped of the `- ` prefix in
  hackathon-mode) — byte-identical to each other and unchanged from
  #41. Each of the 5 skills occurs 3× in each copy (package list,
  palette list, gloss line); `getlayers` is first in the palette
  list; GetLayers-consulted-FIRST sentence + USED/CONSIDERED-AND-
  REJECTED citation sentence present.
- **Palette-first**, `skills/design-taste-frontend/SKILL.md:224`:
  `getlayers` FIRST (character index 371, ahead of
  `motionsites-web-builder` at 533, `gsap` at 867), then the design
  package with `gsap`, `react-bits`, `hairline-create`,
  `hairline-adopt`; citation sentence present.
- **Orchestrate inventory paragraph**, `skills/orchestrate/SKILL.md:70`:
  "the fix #31 additions (GetLayers prompt-first layers — consulted
  FIRST in the palette inventory, the first-class foundation — GSAP
  animation, React Bits components, Hairline illustrations — see §12
  of the inventory)".
- **Design inventory §12**,
  `skills/orchestrate/references/design-inventory.md:168–186`: new
  section for the four resources, GetLayers row leads with
  "Consulted FIRST"; §1 GSAP presets row (:34) and §9 row (:146)
  point at the new usage skill (`skills/gsap/SKILL.md`,
  `gsap@3.15.1`).
- **Staged vs built:** DESIGNPKG-AUTO differs only by the designed
  pin rename (`grok-4.7-high` staged → `grok-4.7-extra-high` built;
  equal after the pin swap, OWED-30-1 class). Orchestrate :70 is
  byte-identical staged vs built. The palette paragraph is identical
  staged vs built **by content** — note the line-number trap: it sits
  at staged :223 and built :224, so a fixed-line comparison reads
  False; the paragraph text itself is identical, and the file's only
  diff is the pre-existing description-scope wording at :9–13 (the
  same staged-vs-built drift #41 recorded, not a fix #31 change).

**Sites that still omit the 5 — unchanged from #41, not re-filed.**
Spot-checked: `skills/orchestrate/SKILL.md:66` and `:139` and
`skills/feature-expansion/SKILL.md:156` still contain 0 hits for
`getlayers`/`motionsites` — the same surface-conditional shorthands
#41 recorded, each also omitting `motionsites-web-builder` (fix #27),
delegating to the canonical list or the inventory. No new omission
appeared in run 2.

### (b) Stale-count sweep — CLEAN (own greps, excl. `node_modules`)

| String | Occurrences | Notes |
|---|---|---|
| `67 skills` | **0** | in `.md`/`.mdc`/`.json` |
| `50 templates` / `114 WebGL` / `276 backgrounds` / `10 animated sections` | **0** each | frozen Nov 16 figures absent |
| `62 templates` / `222 3D` / `54 sections` / `530 backgrounds` / `1,088` | **0** each | drifted Nov 17 figures also absent — skill carries no counts |
| `gsap@3.15.0` / `GSAP 3.15.0` | **0** | |
| literal `3.15.0` in `.md` | **0** | see note below |
| `Hairline UI` | **3** | all explicit out-of-scope disclaimers (see (c)) |

Note on `3.15.0`: a bare regex grep `3.15.0` (dots = any char)
matches 2–4 lines in coordinate/icon data files
(`sample-map.json`, `demo.html`, `photos.json`) — regex false
positives on digit sequences, not version strings. The literal
string `3.15.0` occurs **0** times in any `.md`/`.json` file, and
`gsap@3.15.0` / `GSAP 3.15.0` occur 0 times tree-wide. The GSAP pin
is `3.15.1` everywhere it appears (11 hits in `.md`/`.mdc`, incl.
gsap skill :6/:24, design-inventory :146/:183).

### (c) Orphan/consistency sweep — CLEAN

**New skill dirs — contents match the MANIFEST exactly** (own
`find`, staged `diff -r` silent for all five):

- `skills/getlayers/` — `SKILL.md` only.
- `skills/gsap/` — `SKILL.md` only.
- `skills/react-bits/` — `SKILL.md` only.
- `skills/hairline-create/` — `SKILL.md` + `LICENSE` + `kernel.js`,
  `bench.html`, `build.mjs` + `validate.mjs`, `examples/riffle.js` +
  `examples/terrain.js`, `concepts.md`, `look.md`, `look.mjs`,
  `read.mjs`, `rules.md`, `source.md` — the MANIFEST's set, as
  vendored.
- `skills/hairline-adopt/` — `SKILL.md` + `LICENSE` only.
- Both LICENSE files MIT, Lucas Marques, copyright 2026, md5
  `d97393bd90aec1925bdf7413a6e0cc06` for both.
- No vendored GetLayers content, no React Bits `.tsx`/`.jsx`/`.css`
  source (the 3 new skill dirs contain only `SKILL.md`), no vendored
  GSAP source. The `.tsx` files found tree-wide are the pre-existing
  `pitch-deck-video/template` sources, not React Bits content.

**Inventory §12 paths exist on disk:** all five `SKILL.md` paths
present; §1's `skills/ui-ux-pro-max/data/motion.csv` exists with
header + 17 data rows (18 lines); §9's `skills/gsap/SKILL.md`
usage-skill pointer resolves.

**URLs — all 6 key URLs resolve to live pages** (fetched as page text
Nov 17, 2026 ~04:43–04:45 UTC):

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
  24 commits; 8 skills (`gsap-core`, `gsap-timeline`,
  `gsap-scrolltrigger`, `gsap-plugins`, `gsap-utils`, `gsap-react`,
  `gsap-performance`, `gsap-frameworks`) — matches the skill's
  reference table.
- `https://github.com/lucasmarkes/hairline` — live, public, MIT,
  HEAD `034f4bf` (same commit audit #97-A verified the vendored copy
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
  `Grok 4.7 High` ×0, bare `grok-4.6-high-fast` ×0 (total
  occurrences of the fast-worker slug equal the `cursor-`-prefixed
  count, 70 = 70). Exactly the SPEC census; the weave added no pin
  text. (Line counts read lower — 44/11/68 — because several lines
  carry multiple occurrences; occurrence counts are the census.)
- **GLOBAL-ROUTING block** still byte-identical in orchestrate
  (`SKILL.md:36`) and hackathon-mode (`hackathon-mode.mdc:45`) after
  stripping the `- ` prefix: both 2,285 chars, md5
  `68206505a08f90474dc4931b0e5fb6bb` — the fix #29 golden md5.
- **`fix31.py` == `fix31.py.template`:** md5
  `241e6bcd7804e2e45ab517b3af462cba` for both (see 97-A1 above).
- **README:** 72 skills in all 4 count lines (:13, :37, :39, :41);
  fix #31 provenance note present at :29 with all four `_F31`
  tokens; zero `67 skills` tree-wide (see (b)).
- **Trigger coverage:** `manifests/context-packs/skill-triggers@1.json`
  — coverage `{'skills': 72, 'withTriggers': 49}`, 49 trigger keys.
  `build.sh:222` lists all 5 new skills in the new-skills loop; the
  fix31 hook sits at :24136–24146, after fix30 and before STEP 5.
- **Patch log:** 0 errors, 11 changes; DECISION-31-1…31-7 and
  OWED-31-1…31-4 match the MANIFEST (OWED-31-2 now price-free).

### (e) GetLayers weight — CONFIRMED at all 6 claimed sites

| Site | Weight language present |
|---|---|
| DESIGNPKG-AUTO, `skills/orchestrate/SKILL.md:35` | "GetLayers prompts are consulted FIRST in the palette inventory — the first-class foundation the direction leans on" + citation sentence (USED/CONSIDERED-AND-REJECTED, D19) |
| DESIGNPKG-AUTO, `rules/hackathon-mode.mdc:44` | Same text (stripped byte-identical) |
| Palette-first, `skills/design-taste-frontend/SKILL.md:224` | "`getlayers` FIRST (prompt-first cinematic layers; the first-class foundation the direction leans on — consult its prompts before the other palette sources)" + citation sentence |
| Orchestrate inventory paragraph, `skills/orchestrate/SKILL.md:70` | "GetLayers prompt-first layers — consulted FIRST in the palette inventory, the first-class foundation" |
| Inventory §12, `design-inventory.md:176` | "GetLayers prompts carry the most weight in the palette-first flow — they are consulted FIRST, before the other palette sources, and the direction leans on them heavily as its foundation" + GetLayers row leads with "Consulted FIRST" |
| GetLayers skill, `skills/getlayers/SKILL.md` | Framing header ("consulted FIRST, before the other palette sources… direction leans on GetLayers layers heavily as its foundation… USED or CONSIDERED-AND-REJECTED, each with a D19 reason") + dedicated "Priority in the palette-first flow" section with the `not considered — <reason>` escape |

Ordering is also as claimed: `getlayers` is first in every palette
list (DESIGNPKG-AUTO palette list, design-taste-frontend :224).
`_F31` tokens appear in 9 tree files (the 5 new skills,
orchestrate SKILL.md, hackathon-mode.mdc, design-inventory.md,
README.md); design-taste-frontend carries none, as #41 recorded —
token-per-file is a convention, not a requirement.

### (f) Independent counts — reproduced

Own counts on disk: skills 72, agents 45, rules 48, commands 55,
hooks 15 (`hooks/hooks.json`, 15 entries), trigger keys 49
(`skill-triggers@1.json`, `triggers` dict of 49, coverage 72/49).
Build log run 2 agrees (skills 72, agents 45, rules 48, commands 55,
hooks 15). The call-map sidecar still reads 67/45/48/55/15/49 at
:9–14 — OWED-31-3, recorded, not re-filed (see below).

### (g) Carried items — still standing as recorded, not re-filed

- **OWED-31-3:** call-map sidecar still says 67 skills; map
  generator-owned, not regenerated; new skills are leaf resources.
  Present as recorded.
- **OWED-31-4:** vendored `hairline-create/SKILL.md:11` still says
  "The six figures of @lucasmarkes/hairline are the bar" — upstream's
  original-six text; the live repo's own README still carries the
  same "six figures" image caption, confirming it is upstream text.
  Present as recorded.
- **OWED-30-6** (allow-listed verify30 check-9b smuggled name) and
  the dry-run epic/`/prune` error: not re-filed per the brief. The 7
  epic commands ship in `hackathon-ecc/commands/`; `/prune` absent —
  re-confirmed, not filed.
- **OWED-31-1 / OWED-31-2:** live behaviour unverified until real
  project use; GetLayers MCP unwired (no MCP wiring found in the
  tree). Nothing in this sweep changes either.

### (h) SPEC conformance — scope MET (unchanged from #41)

Four resources, free-tier only, no paid plans; 5 skills (Hairline is
two, per SPEC); palette-first + DESIGNPKG-AUTO + inventory §12 weave;
verify31 §14 checks; no pin/routing/debloom/design-package/grill-me
change. Both SPEC corrections honoured: GSAP pinned at 3.15.1, not
3.15.0; GetLayers counts not frozen anywhere; the skill now also
carries no price, per the 97-A1 fix (prices drift like counts).

### (i) Verifier runs — my own re-run

- **`verify31.py`, re-run by me: 380/380 checks pass, exit 0.**
  (Tail: "PASS getlayers skill dir contains only SKILL.md (no
  vendored content)", "PASS hairline-create ships its engine +
  checks + LICENSE", "PASS no vendored GSAP source file…", "PASS
  README fix31 provenance note present with the four _F31 tokens",
  "PASS fix31/fix31-patch-log.md exists with 0 errors, trigger 67 ->
  72, README note added", "380/380 checks pass".) Run took ~16 s.
  The run-2 log (`fix31/verify31-run2.txt`) is byte-identical to the
  run-1 log.

### (j) No-re-dry-run rationale — CONFIRMED

I checked the rationale rather than assuming it, by tracing what the
dry-run legs actually read:

- **No leg greps the skill for a price.** Grep over
  `fix31/dryrun46/*.py` for `199|price|pricing` returns exactly two
  hits, neither a leg input: `dryrun46-leg4.py:92` cites
  `plan.md:199` — a **line number**, not a price — and
  `dryrun46-report.md:366` restates the old `$199` inside its
  OWED-31-2 record, i.e. a historical report line, not a check.
- **Leg 8 (design leg)** is the only runner that mentions GetLayers,
  and it reads its own scratch copy `leg8-getlayers-llms.txt` plus
  the leg-8 direction record (`8e-getlayers-used-cited`,
  `8e-getlayers-rejected-cited`, `8e-getlayers-first`) — it never
  opens `skills/getlayers/SKILL.md`. Its scratch docs contain no
  `199`/`249`. Its prompt path is unchanged.
- **Leg 5 (call-graph)** reads every `SKILL.md` only for "non-empty
  with frontmatter" — a header-text change cannot flip that check;
  the skill is still non-empty with frontmatter. Legs 1–4, 6, 7 do
  not touch the GetLayers skill at all.
- **Rebuilt-tree delta run 1 → run 2** is exactly the one-line skill
  header plus the patch-log OWED text: the build-log diff shows only
  the ECC re-clone block + one npm timing line, and the verify logs
  are byte-identical (see 97-A1 above).

A re-dry-run would therefore reproduce the identical leg-5 OWED-31-3
lines (2 BROKEN, stale-map artifact, 0 real breakage) and identical
results elsewhere. **The rationale holds; no re-dry-run is needed.**
One nuance, recorded not filed: the dry-run #46 report itself still
restates `$199` in its OWED-31-2 line — that is a round-1 historical
record of the wrong figure, the same class as audit #97-A's quotation
of it as the finding, not a live-tree claim.

### Other

- No file was edited, created, or deleted except this report.
  `build.sh` was not run; `fix11/fix11-stage.py` was not run; nothing
  was committed, pushed, or messaged.
