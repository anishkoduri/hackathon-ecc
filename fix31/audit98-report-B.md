# Audit #98-B — weave + GetLayers weight + regression (fix #31, round 2)

**Verdict: NOT PASS — 0 blocking, 1 minor.**

Auditor B (half B: the weave + the weight + regression), round 2.
Re-audit after round 1, following the round-1 fix of 97-A1 (the $199
GetLayers price, dropped from the skill + `fix31.py`/template).
Read-only except this report. Method: read `fix31/SPEC.md`,
`fix31/MANIFEST.md` §2c/§6/§3, `fix31/audit97-report-B.md`,
`fix31/audit97-report-A.md`, `fix31/sweep41-report.md`, and
`fix31/dryrun46/dryrun46-report.md` (§5 leg-5 leaf-premise
verification) in full; independently re-ran verify31 — **380/380,
exit 0**, output byte-identical to the recorded run 2; direct
byte-level block extraction and comparison (md5) rather than trust;
direct pin/count greps; full-tree `diff -rq` plus per-file `diff` of
the fix #30 built tree (`fix31/scratch-repo/hackathon-ecc`, 67 skills)
against the rebuilt fix #31 tree (`hackathon-ecc`); staged-vs-built
comparison of the weave sources; and a faithful re-run of the
fix28 call-map generator's own evidence rules against the current
tree (see §6). The real tree was never edited by this audit.

**Headline:** everything in this half re-verifies clean after the
97-A1 price fix — DESIGNPKG-AUTO byte-identity, the GetLayers weight
at every site, the palette-first paragraph, the pin census, the
counts, the full-tree diff, grill-me untouched — with one exception.
The OWED-31-3 premise does **not** hold: the DESIGNPKG-AUTO
additions **are** dispatch edges by the call-map generator's own
definition, and there are two further dispatch edges between new
skills. The map is therefore wrong as a record (67 vs the tree's 72,
5 called skills absent), and the fix is map regeneration — finding
98-B1 (minor). No shipped routing behavior is wrong; the defect is
confined to the generated map sidecar and the verifier line that
pins its staleness.

## Findings

| # | Severity | Finding |
|---|---|---|
| 98-B1 | Minor | OWED-31-3 premise fails — the DESIGNPKG-AUTO additions ARE dispatch edges, and two new-skill→new-skill edges exist, so the fix28 call map (67 skills, no rows for the 5 new skills) is missing edges. Map regeneration is the fix (generator `EXPECTED` 67→72, re-run generator, rebuild, update verify31 check 10g's sidecar expectation 67→72, re-run verify31 + dry-run leg 5). See §6. |

## §1 DESIGNPKG-AUTO byte-identity — PASS (unchanged by the price fix)

- Block appears exactly once in `skills/orchestrate/SKILL.md:35` and
  once in `rules/hackathon-mode.mdc:44`.
- Both blocks are 3,463 chars, md5
  `6f74770f3e897b3115caecd6177ed90d`, byte-identical to each other
  (compared after stripping the `- ` list prefix in hackathon-mode,
  the way verify31 extracts them). **Identical md5 to audit #97-B** —
  the price removal touched nothing here.
- All 5 new skills named in the package list
  (`getlayers / gsap / react-bits / hairline-create / hairline-adopt`)
  and in the palette list, each with its gloss line and `_F31` token
  (`GETLAYERS_F31`, `GSAP_F31`, `REACTBITS_F31`, `HAIRLINE_F31`).
  `getlayers` is first in the palette list
  (`(`getlayers`, `motionsites-web-builder`, `gsap`, `react-bits`,
  `hairline-create`, `hairline-adopt`, …)`).
- Staged-vs-built: the staged block in
  `new-skills/orchestrate/SKILL.md` and in
  `new-rules/hackathon-mode.mdc` differs from the built block ONLY by
  the known OWED-30-1 pin drift (`grok-4.7-high` staged →
  `grok-4.7-extra-high` built, 3,457 vs 3,463 chars; replacing the pin
  makes them identical). By design, not a finding.

## §2 GetLayers WEIGHT — the weight is real and visible (unchanged)

### (a) Ordering

- DESIGNPKG-AUTO palette list starts with `getlayers`
  (`skills/orchestrate/SKILL.md:35`, `rules/hackathon-mode.mdc:44`).
- design-taste-frontend palette-first paragraph
  (`skills/design-taste-frontend/SKILL.md:224`) names
  "`getlayers` FIRST" before MotionSites and the design package.

### (b) Explicit priority language — present at all six sites

- DESIGNPKG-AUTO block (both files): "GetLayers prompts are consulted
  FIRST in the palette inventory — the first-class foundation the
  direction leans on: the design-lead reads the live GetLayers
  library before the other palette sources, and the direction names
  the GetLayers layers used or considered-and-rejected, each with a
  fix #19 D19 reason."
- `skills/getlayers/SKILL.md:6` framing header: "GetLayers prompts are
  a first-class, high-priority source — the design-lead consults them
  FIRST, before the other palette sources, and the direction leans on
  GetLayers layers heavily as its foundation." Plus the dedicated
  "## Priority in the palette-first flow" section (`:30–:38`).
- Inventory §12 (`skills/orchestrate/references/design-inventory.md:168–182`):
  intro "GetLayers prompts carry the most weight in the palette-first
  flow — they are consulted FIRST…", and the GetLayers row's
  "Reach for it when" column leads with "Consulted FIRST in the
  palette inventory — the first-class foundation the direction leans
  on."
- Orchestrate inventory paragraph (`skills/orchestrate/SKILL.md:70`):
  "the fix #31 additions (GetLayers prompt-first layers — consulted
  FIRST in the palette inventory, the first-class foundation — GSAP
  animation, React Bits components, Hairline illustrations — see §12
  of the inventory)".

### (c) Citation check — present in all three flow paragraphs

The sentence "GetLayers layers are cited the same way as every
inventory entry — USED or CONSIDERED-AND-REJECTED, each with a D19
reason" is present exactly once in each of:

- `skills/orchestrate/SKILL.md:35` (DESIGNPKG-AUTO),
- `rules/hackathon-mode.mdc:44` (DESIGNPKG-AUTO),
- `skills/design-taste-frontend/SKILL.md:224` (palette-first),

each followed by the "a direction that names no GetLayers layer at
all … is a finding" enforcement clause.

## §3 Palette-first flow (design-taste-frontend SKILL.md:224) — PASS

- All 5 skills named, each exactly once in the paragraph
  (`getlayers` 1×, `gsap` 1×, `react-bits` 1×, `hairline-create` 1×,
  `hairline-adopt` 1×; `motionsites-web-builder`, `ui-ux-pro-max`,
  `less-flat-ui` also 1× each — no duplicated names).
- The paragraph reads coherently: "`getlayers` FIRST (…), then
  `motionsites-web-builder` (…), the design package (…,
  `gsap`, `react-bits`, `hairline-create`, `hairline-adopt`), and the
  dealt Hallmark theme" — no broken sentences, no leftover
  `getlayers` inside the design-package parenthetical (0 occurrences
  there; it is correctly listed separately, first).
- Staged-vs-built: the palette paragraph in
  `new-skills/design-taste-frontend/SKILL.md` is identical to the
  built paragraph.

## §4 Regression — PASS

- **GLOBAL-ROUTING block** still byte-identical in orchestrate
  (`SKILL.md:36`) and hackathon-mode (`hackathon-mode.mdc:45`): both
  2,285 chars, md5 `68206505a08f90474dc4931b0e5fb6bb` — the same md5
  audit #96-B recorded against the fix #29 golden copy and audit
  #97-B re-recorded. All 7 `_F29` tokens present in each copy.
- **Pin census (independent grep, whole tree excl. `node_modules`):**
  `grok-4.7-extra-high` ×49, `Grok 4.7 Extra High` ×22,
  `cursor-grok-4.6-high-fast` ×70, `grok-4.7-high` ×0,
  `Grok 4.7 High` ×0, bare `grok-4.6-high-fast` ×0 (all 70 hits are
  the `cursor-` form) — exactly the SPEC census; the weave added no
  pin text, and the price fix added none either.
- **Counts (direct listing):** skills 72, agents 45, rules 48,
  commands 55, hook entries 15 (`hooks/hooks.json`), trigger keys 49
  (`skill-triggers@1.json` coverage `{"skills": 72, "withTriggers":
  49}`) — all as specified in MANIFEST §2a. No trigger keys for the
  new skills (0 matches for getlayers/gsap/react-bits/hairline in
  the trigger file).
- **README:** `72` in all 4 count lines (`README.md:13, :37, :39,
  :41`), zero `67 skills` tree-wide (0 hits, excl. `node_modules`),
  plus the fix #31 provenance note at `:29`.
- **Full-tree diff, fix #30 built tree vs fix #31 rebuilt tree:**
  `diff -rq` (excl. `node_modules`) finds exactly 6 differing files
  and 5 added skill dirs — nothing else, identical to the round-1
  result. Per-file `diff` confirms each file differs ONLY by the
  intended weave / generated writes: `README.md` (4 count lines
  67→72 + provenance note), `skill-triggers@1.json` (coverage 67→72),
  `rules/hackathon-mode.mdc:44` (DESIGNPKG-AUTO only),
  `skills/design-taste-frontend/SKILL.md:224` (palette-first paragraph
  only), `skills/orchestrate/SKILL.md:35, :70` (DESIGNPKG-AUTO +
  inventory paragraph only),
  `skills/orchestrate/references/design-inventory.md` (`:34`, `:146`
  usage-skill pointers + new §12, lines 167–185). Added:
  `skills/getlayers/`, `skills/gsap/`, `skills/react-bits/`,
  `skills/hairline-create/`, `skills/hairline-adopt/`.
- **No other text changed:** no routing (#29), debloat (#28),
  design-package, or grill-me text changed — `grill-me/SKILL.md` is
  byte-identical to the fix #30 tree (`diff -rq` on the dir is
  silent), and the diff above shows no other file touched at all.
  The empty `commands/` diff also carries the round-1 epic-command
  state forward: all 7 epic commands ship, `/prune` absent — not
  re-filed.
- **Build run 2:** `fix31/build-log-run2.txt` ends `fix31: OK` /
  `build complete`, STEP 5 counts 72/45/48/55/15, exit 0. Its diff
  against run 1 is only the ECC re-clone/install block (run 1
  re-cloned because /tmp was wiped; run 2 reused the clone) + an npm
  timing line — no fix31 content difference.

## §5 The 97-A1 price fix did not disturb this half — PASS

- `$199` occurs **0 times** in the built tree (excl.
  `node_modules`), in `skills/getlayers/SKILL.md`, in
  `fix31/fix31.py`, in `fix31/fix31.py.template`, and in
  `fix31/fix31-patch-log.md` (its OWED-31-2 line now reads "it
  requires the Full Stack Lifetime plan" with no price — the patch
  log regenerated on build run 2 as stated).
- `fix31.py` == `fix31.py.template`, md5
  `241e6bcd7804e2e45ab517b3af462cba` for both — the post-fix value
  given in the task, confirmed independently.
- The staged skill is likewise price-free and byte-identical to the
  built skill (`new-skills/getlayers/SKILL.md` ==
  `hackathon-ecc/skills/getlayers/SKILL.md`; no `$199`, no `$249` —
  the skill carries no price, as the SPEC correction directs).
- The live $249 is recorded where fix records belong: `SPEC.md:19`
  ("the live pricing page lists Full Stack Lifetime at $249 ($499
  struck through; $199 is Unlimited Plus)") and `MANIFEST.md` §3.
  The only remaining `$199` strings in `fix31/` are inside those two
  correction sentences themselves (describing the error that was
  fixed) — not live claims.
- Byte-identity, weight, and census assertions all still hold at
  their round-1 values: DESIGNPKG-AUTO md5 `6f74770f…` (§1),
  GLOBAL-ROUTING md5 `68206505…` (§4), pin census 49/22/70/0/0 (§4),
  verify31 output byte-identical to run 2 (§8).

## §6 OWED-31-3 adjudication — PREMISE FAILS (finding 98-B1)

MANIFEST OWED-31-3 records the call map as generator-owned and not
regenerated because "the new skills are leaf resources (invoked by
the design-lead), not dispatchers; no new orchestration edges, so the
fix28 map stands (its sidecar still says 67 skills)", with the
conditional: **"If the audit finds the DESIGNPKG-AUTO additions are
dispatch edges, regeneration is the fix."** Dry-run #46 §5 verified
the leaf premise live as: "no command or agent file names any of the
5 new skills as a dispatch target … and the 5 new skills name no
other skill or agent as a dispatch target (grep over their SKILL.md
files: no `skills/` or `agents/` dispatch references)".

That verification is incomplete in both directions, and its
conclusion is wrong under the map generator's own rules.

### (a) What the generator counts as a dispatch edge

`fix28/callmap/generate_call_map.py` (docstring, lines 22–27):
STRONG evidence is a backticked `` `name` ``, `skill:name`, a path
`skills/<name>/`, or a `/command` slash form; INVENTORY is a listing
in `references/design-inventory.md`. "Called" for a skill is ≥1
STRONG, INVENTORY, or TRIGGER invoker. The `scan()` code
(lines 409–426) implements exactly that: a skill name in a file's
backticked-token set (or `skills/` path set, etc.) is a STRONG
invoker, unless it is the skill's own file; the inventory file
counts as INVENTORY instead of STRONG.

### (b) The motionsites precedent — the same weave, recorded as called

`motionsites-web-builder` was added in fix #27 by the same weave
(DESIGNPKG-AUTO + palette-first + inventory), and the fix28 map
records it as `called: true` with STRONG invokers from exactly the
files that now name the 5 new skills:
`hackathon-ecc/rules/hackathon-mode.mdc`,
`hackathon-ecc/skills/design-taste-frontend/SKILL.md`,
`hackathon-ecc/skills/orchestrate/SKILL.md` (built + staged), plus
the call-map.md row 104. There is no reading of the generator's
rules under which DESIGNPKG-AUTO membership counts for motionsites
but not for the fix #31 additions.

### (c) Faithful re-run of the generator's rules on the current tree

I imported `generate_call_map.py` (no generation run — read-only)
and applied its own `tokenise()` + `scan()` skill rule to the
built-tree + staged corpus (`/tmp/audit98b-owed313.py`, exit 0).
Result — every one of the 5 new skills would be recorded as called:

| Skill | STRONG invokers (built + staged) | INVENTORY |
|---|---|---|
| `getlayers` | `rules/hackathon-mode.mdc`, `skills/design-taste-frontend/SKILL.md`, `skills/orchestrate/SKILL.md` (each built + staged), via backticked name | `design-inventory.md` §12 |
| `gsap` | same three files (built + staged), via backticked name (+ pre-existing strong hits in `motion-patterns`, `ui-ux-pro-max`, icon/fixture JSONs — library mentions predating fix #31, not new edges) | `design-inventory.md` §12 |
| `react-bits` | same three files (built + staged), via backticked name; plus `skills/gsap/SKILL.md` (see (d)) | `design-inventory.md` §12 |
| `hairline-create` | same three files (built + staged), via backticked name; plus `skills/hairline-adopt/SKILL.md` (see (d)) | `design-inventory.md` §12 |
| `hairline-adopt` | same three files (built + staged), via backticked name | `design-inventory.md` §12 |

So the DESIGNPKG-AUTO additions **are** dispatch edges, by the
generator's own definition — the OWED-31-3 conditional fires.

### (d) Two further dispatch edges between new skills

- **`hairline-adopt` → `hairline-create`.** The fix #31 framing
  header (`skills/hairline-adopt/SKILL.md:7`) states the skill
  rebuilds an SVG "by invoking the `hairline-create` skill in this
  plugin", and the vendored upstream text (`:20`) says "Invoke
  `/hairline-create` with the file's path…". Backticked name +
  slash form = STRONG under the generator's rules. The dry-run's
  grep for `skills/`/`agents/` path forms missed both: neither is a
  path reference.
- **`gsap` → `react-bits`.** `skills/gsap/SKILL.md:19` ("For
  components, use `react-bits` (React/Next)…") and `:91` ("Do NOT
  reach for it for a component (use `react-bits`…)") — a routing
  pointer from one new skill to another, backticked = STRONG.
  (`getlayers` and `react-bits` name no other new skill; the
  `skills/…/SKILL.md` path references in `gsap` :115–117 and
  `react-bits` :70–71 point at pre-existing skills — lookup pointers,
  not new edges.)

### (e) What is actually wrong, and what is not

- **Wrong as a record:** the fix28 map (`call-map.md`, md5
  `b066413a1a7dd6efcd8571c8abf93942`, byte-identical to the fix #30
  tree's copy) still says 67 skills and has no rows for the 5 new
  skills; `fix28/callmap/call-map-data.json` counts
  `{"skills": 67, …}` and contains 0 occurrences of `getlayers`,
  `hairline`, `react-bits` (and `gsap` only in its pre-existing
  library sense). The map's own header states the currency rule —
  "kept current by the same change that adds or removes an element"
  — which this fix breaches. Dry-run #46 leg 5's 2 BROKEN lines are
  this same fact, not a separate issue.
- **Not wrong:** no shipped routing behavior. Nothing fails to
  route at runtime; the design-lead can and does reach all 5 skills
  through the DESIGNPKG-AUTO / palette-first / inventory text that
  the generator would count. The dry-run's "0 real breakage"
  judgment about runtime dispatch still stands; what fails is the
  claim that no dispatch edge is missing from the map.
- **Severity — minor, not blocking.** The defect is confined to a
  generated verification record (map + sidecar) and the verifier
  line that pins its staleness; the shipped tree is correct and
  verify31 passes 380/380 on it. The fix is mechanical
  regeneration, not a design or behavior change.

### (f) The fix, and its cascade (for the parent to decide)

Regeneration is the fix, per OWED-31-3's own conditional, but it is
not a one-file edit — the stale count is pinned in three places:

1. `fix28/callmap/generate_call_map.py`: `EXPECTED` counts
   `{"skills": 67, …}` — must become 72, or the generator fails
   loudly on the count mismatch (its documented behavior).
2. Re-run the generator, producing a regenerated
   `new-skills/orchestrate/references/call-map.md` + updated
   `fix28/callmap/call-map-data.json` (67→72, 5 new called-skill
   rows incl. the §6(c) invokers and the §6(d) edges), then rebuild
   so the staged map flows into the built tree via the STEP 2 copy.
3. `fix31/verify31.py` check 10g (`verify31.py:1561–1580`)
   hard-asserts the sidecar counts equal
   `{"skills": 67, "agents": 45, "rules": 48, "commands": 55,
   "hooks": 15, "triggers": 49}` — it must be updated to 72, or
   the regenerated map fails verification.
4. Re-run verify31 (expect 380/380 on the updated expectation) and
   re-run dry-run leg 5 (its runner reads `call-map-data.json`;
   the 2 BROKEN lines should clear).

This audit changed no file, ran no generator, and ran no build —
regeneration is the coordinator's call, and per the fix #27
convention a minor fixed post-hoc without a re-audit/re-sweep leaves
SPEC Verification NOT MET as written (see §9).

## §7 Findings — summary

- **98-B1 (minor):** OWED-31-3 premise fails — DESIGNPKG-AUTO
  additions are dispatch edges (STRONG backticked references from
  orchestrate / hackathon-mode / design-taste-frontend, built +
  staged, exactly as motionsites-web-builder is recorded), plus
  `hairline-adopt` → `hairline-create` and `gsap` → `react-bits`
  edges between new skills. The fix28 call map is missing all of
  them and its counts (67) disagree with the tree (72). Fix: map
  regeneration with the §6(f) cascade.
- No other findings. 0 blocking, 1 minor.

## §8 Tested and NOT filed

- **OWED-30-6** (allow-listed verify30 check-9b smuggled name):
  recorded known limitation, per instructions — not re-filed.
- **Dry-run epic/`/prune` error:** already adjudicated (only `/prune`
  was dropped in fix #27; all 7 epic commands ship; the empty
  `commands/` diff in §4 carries that state forward) — not re-filed.
- **Staged-vs-built pin drift (OWED-30-1):** the staged DESIGNPKG-AUTO
  block carries `grok-4.7-high` where the built tree carries
  `grok-4.7-extra-high`; the difference is exactly the fix #30 rename
  and nothing else. By design, not a finding.
- **OWED-31-1/31-2/31-4:** carried as recorded in MANIFEST §6 (live
  behavior unverified until real project use; GetLayers MCP unwired;
  upstream "six figures" text in vendored hairline-create). None is
  in this half's scope and none was re-filed. Note OWED-31-3 is no
  longer carried as recorded — it is superseded by finding 98-B1.
- **97-A1 (GetLayers $199):** confirmed fixed (§5) — not re-filed.
- **Dry-run leg 5's 2 BROKEN lines:** the same fact as 98-B1 (stale
  map counts), not a separate finding.

## §9 SPEC §7 verification criteria — status

- The audit loop is at round 2 (this report + the parallel #98-A);
  sweep #42 is parallel round-2 work. The verifier half of §7 holds
  for this scope: verify31 independently re-run **380/380, exit 0**,
  and its §14 checks cover the weight explicitly.
- **SPEC Verification is NOT MET as written** — this audit carries
  one minor (98-B1) whose fix (map regeneration + verify31 10g
  update) would land post-hoc without a re-audit/re-sweep of the
  regenerated map, per the fix #27 convention. The criterion can only
  be judged MET once the regeneration lands and the affected checks
  (verify31 re-run, dry-run leg 5 re-run, and a re-audit of the map)
  have re-verified it. This is a statement about the verification
  loop's completeness, not about the shipped tree, which passes
  every check in this half.

## §10 Methodology note

- Independent re-run: `python3 fix31/verify31.py hackathon-ecc` →
  **380/380, exit 0**, output byte-identical to
  `fix31/verify31-run2.txt` (`diff` silent).
- Block comparisons used direct extraction from the built files with
  md5 (`DESIGNPKG-AUTO 6f74770f…`, `GLOBAL-ROUTING 68206505…`),
  not the verifier's assertions.
- Tree diff baseline is `fix31/scratch-repo/hackathon-ecc` (the fix #30
  built tree, 67 skills); the file-list diff shows only the 5 new
  skill dirs added and the 6 files in §4 changed.
- OWED-31-3 adjudication used the generator's own code
  (`fix28/callmap/generate_call_map.py`, docstring tiers +
  `scan()` lines 409–426 + `tokenise()`), its own data
  (`fix28/callmap/call-map-data.json`, incl. the
  `motionsites-web-builder` entry as the precedent), and a read-only
  replication script (`/tmp/audit98b-owed313.py`, exit 0) that
  applied `tokenise()` + the `scan()` skill rule to the built +
  staged corpus without writing anything to the tree. The generator
  itself was not executed (it would write outputs and fail loudly
  on its hardcoded `EXPECTED` 67 counts).
- The real tree was never edited by this audit; the only file written
  is this report.
