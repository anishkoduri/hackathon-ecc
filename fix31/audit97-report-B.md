# Audit #97-B — weave + GetLayers weight + regression (fix #31, round 1)

**Verdict: PASS — 0 blocking, 0 minor.**

Auditor B (half B: the weave + the weight + regression).
Read-only except this report. Method: read `fix31/SPEC.md` (including the
GetLayers weight direction update), `fix31/MANIFEST.md` §2c/§6, and
`fix31/fix31-patch-log.md` in full; independently re-ran verify31 —
**380/380, exit 0** (real tree), matching the recorded run 1; direct
byte-level block extraction and comparison (md5) rather than trust;
direct pin/count greps; full-tree `diff -rq` plus per-file `diff` of
the fix #30 built tree (`fix31/scratch-repo/hackathon-ecc`, 67 skills)
against the rebuilt fix #31 tree (`hackathon-ecc`); staged-vs-built
comparison of the weave sources. The real tree was never edited by
this audit.

## §1 DESIGNPKG-AUTO byte-identity — PASS

- Block appears exactly once in `skills/orchestrate/SKILL.md:35` and
  once in `rules/hackathon-mode.mdc:44`.
- Both blocks are 3,463 chars, md5
  `6f74770f3e897b3115caecd6177ed90d`, byte-identical to each other
  (compared after stripping the `- ` list prefix in hackathon-mode,
  the way verify31 extracts them).
- All 5 new skills named in the package list
  (`getlayers / gsap / react-bits / hairline-create / hairline-adopt`)
  and in the palette list, each with its gloss line and `_F31` token
  (`GETLAYERS_F31`, `GSAP_F31`, `REACTBITS_F31`, `HAIRLINE_F31`).
- Staged-vs-built: the staged block in
  `new-skills/orchestrate/SKILL.md` and in
  `new-rules/hackathon-mode.mdc` differs from the built block ONLY by
  the known OWED-30-1 pin drift (`grok-4.7-high` staged →
  `grok-4.7-extra-high` built, 3,457 vs 3,463 chars; replacing the pin
  makes them identical). By design, not a finding.

## §2 GetLayers WEIGHT — the weight is real and visible

The direction update (Anish Nov 16 ~10:02 PM) is implemented in all
three ways the SPEC requires — ordering, explicit priority language,
and the citation check — and GetLayers is not a minor entry anywhere
it appears.

### (a) Ordering

- DESIGNPKG-AUTO palette list starts with `getlayers`:
  `(`getlayers`, `motionsites-web-builder`, `gsap`, `react-bits`,
  `hairline-create`, `hairline-adopt`, …)` —
  `skills/orchestrate/SKILL.md:35`, `rules/hackathon-mode.mdc:44`.
- design-taste-frontend palette-first paragraph
  (`skills/design-taste-frontend/SKILL.md:224`) names
  "`getlayers` FIRST" before MotionSites and the design package.

### (b) Explicit priority language

- DESIGNPKG-AUTO block (both files): "GetLayers prompts are consulted
  FIRST in the palette inventory — the first-class foundation the
  direction leans on: the design-lead reads the live GetLayers
  library before the other palette sources, and the direction names
  the GetLayers layers used or considered-and-rejected, each with a
  fix #19 D19 reason."
- `skills/getlayers/SKILL.md:6`: "GetLayers prompts are a first-class,
  high-priority source — the design-lead consults them FIRST, before
  the other palette sources, and the direction leans on GetLayers
  layers heavily as its foundation." Plus a dedicated
  "## Priority in the palette-first flow" section (`:30–:38`):
  "consulted FIRST in the palette inventory — ahead of MotionSites,
  the design package, and the dealt Hallmark theme", with the
  not-forcing caveat (`not considered — <reason>`).
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

**Judgment:** the weight is real and visible, not a minor entry.
GetLayers is first in every palette list, carries first-class /
consulted-FIRST language in the skill, the DESIGNPKG-AUTO block, the
inventory §12 row, and the orchestrate inventory paragraph, and the
citation rule is enforced identically in all three flow paragraphs.
The not-forcing caveat (a surface with no fitting free layer records
`not considered — <reason>`) is present in the skill and matches
DECISION-31-7; it bounds the weight, it does not dilute it.

## §3 Palette-first flow (design-taste-frontend SKILL.md:224) — PASS

- All 5 skills named, each exactly once in the paragraph
  (`getlayers` 1×, `gsap` 1×, `react-bits` 1×, `hairline-create` 1×,
  `hairline-adopt` 1×; `motionsites-web-builder`, `ui-ux-pro-max`,
  `less-flat-ui` also 1× each — no duplicated names).
- The paragraph reads coherently after the re-weave: "`getlayers`
  FIRST (…), then `motionsites-web-builder` (…), the design package
  (…, `gsap`, `react-bits`, `hairline-create`, `hairline-adopt`),
  and the dealt Hallmark theme" — no broken sentences, no leftover
  `getlayers` inside the design-package parenthetical (0 occurrences
  there; it is correctly listed separately, first).
- Staged-vs-built: the palette paragraph in
  `new-skills/design-taste-frontend/SKILL.md` is identical to the
  built paragraph.

## §4 Regression — PASS

- **GLOBAL-ROUTING block** still byte-identical in orchestrate
  (`SKILL.md:36`) and hackathon-mode (`hackathon-mode.mdc:45`): both
  2,285 chars, md5 `68206505a08f90474dc4931b0e5fb6bb` — the same md5
  audit #96-B recorded against the fix #29 golden copy. All 7 `_F29`
  tokens present in each copy.
- **Pin census (independent grep, whole tree excl. `node_modules`):**
  `grok-4.7-extra-high` ×49, `Grok 4.7 Extra High` ×22,
  `cursor-grok-4.6-high-fast` ×70, `grok-4.7-high` ×0,
  `Grok 4.7 High` ×0, bare `grok-4.6-high-fast` ×0 (all 70 hits are
  the `cursor-` form) — exactly the SPEC census; the weave added no
  pin text (zero pin strings in the 5 new skill dirs, per the patch
  log and confirmed by the census holding).
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
  and 5 added skill dirs — nothing else. The 6 differing files differ
  ONLY by the intended weave / generated writes, verified by
  per-file `diff`: `README.md` (4 count lines 67→72 + provenance
  note), `skill-triggers@1.json` (coverage 67→72), `rules/hackathon-mode.mdc:44`
  (DESIGNPKG-AUTO only), `skills/design-taste-frontend/SKILL.md:224`
  (palette-first paragraph only),
  `skills/orchestrate/SKILL.md:35, :70` (DESIGNPKG-AUTO + inventory
  paragraph only), `skills/orchestrate/references/design-inventory.md`
  (`:34`, `:146` usage-skill pointers + new §12, lines 167–185).
  Added: `skills/getlayers/`, `skills/gsap/`, `skills/react-bits/`,
  `skills/hairline-create/`, `skills/hairline-adopt/`.
- **No other text changed:** no routing (#29), debloat (#28),
  design-package, or grill-me text changed — `grill-me/SKILL.md` is
  byte-identical to the fix #30 tree, and the diff above shows no
  other file touched at all.
- **Build run 1:** `fix31/build-log-run1.txt` ends `fix31: OK` /
  `build complete`, STEP 5 counts 72/45/48/55/15, exit 0.
- **Epic commands:** all 7 ship (`epic-claim`, `epic-decompose`,
  `epic-publish`, `epic-review`, `epic-sync`, `epic-unblock`,
  `epic-validate`); `/prune` absent, as adjudicated — not re-filed.

## §5 Findings

None. 0 blocking, 0 minor.

## §6 Tested and NOT filed

- **OWED-30-6** (allow-listed verify30 check-9b smuggled name):
  recorded known limitation, per instructions — not re-filed.
- **Dry-run epic/`/prune` error:** already adjudicated (only `/prune`
  was dropped in fix #27; all 7 epic commands ship, verified above)
  — not re-filed.
- **Staged-vs-built pin drift (OWED-30-1):** the staged DESIGNPKG-AUTO
  block carries `grok-4.7-high` where the built tree carries
  `grok-4.7-extra-high`; the difference is exactly the fix #30 rename
  and nothing else. By design, not a finding.
- **OWED-31-1/31-2/31-3/31-4:** carried as recorded in MANIFEST §6
  (live behavior unverified until real project use; GetLayers MCP
  unwired; call-map sidecar still says 67; upstream "six figures"
  text in vendored hairline-create). None is in this half's scope
  and none was re-filed.

## §7 SPEC §7 verification criteria — status

- The audit loop is at round 1 (this report + the parallel #97-A);
  sweep #41 and dry-run #46 (including the design leg) have not run
  yet. **SPEC Verification is therefore NOT YET MET — pending, not
  failed.** No finding in this audit required a post-hoc fix, so the
  fix #27 convention (a minor fixed post-hoc without a re-audit ⇒
  SPEC Verification NOT MET as written) is not triggered by half B.
  The criterion can only be judged once round 2, the sweep, and the
  dry-run have landed.
- The verifier half of §7 holds for this scope: verify31 independently
  re-run **380/380, exit 0**, and its §14 checks cover the weight
  explicitly (DESIGNPKG-AUTO palette list starts with getlayers,
  `getlayers` FIRST in the palette-first paragraph, inventory §12
  "Consulted FIRST", getlayers skill first-class language —
  `fix31/verify31.py:2258–2287`).

## §8 Methodology note

- Independent re-run: `python3 fix31/verify31.py hackathon-ecc` →
  **380/380, exit 0** (real tree), matching `fix31/verify31-run1.txt`.
- Block comparisons used direct extraction from the built files with
  md5 (`DESIGNPKG-AUTO 6f74770f…`, `GLOBAL-ROUTING 68206505…`),
  not the verifier's assertions.
- Tree diff baseline is `fix31/scratch-repo/hackathon-ecc` (the fix #30
  built tree, 67 skills); the file-list diff shows only the 5 new
  skill dirs added (including the hairline-create engine/checks/
  examples files) and the 6 files above changed.
- The real tree was never edited by this audit; the only file written
  is this report.
