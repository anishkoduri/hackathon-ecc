# Audit #111-A — fix #33 round 33c re-audit (correctness of the fix + the tree)

- **Auditor:** A (correctness of the fix itself + the tree)
- **Date:** Nov 17, 2026
- **Fix dir:** `~/workspace/hackathon-plugin/fix33/`
- **Scratch repo:** `~/workspace/hackathon-plugin/fix33/scratch-repo`, git HEAD `dd106ade`
- **Scope:** audit #110 (110-M1), sweep #53 (S-M1/S-M2), dry-run #50 (D-1/D-2) fixes as
  claimed in `fix-round-33c-report.md`. The worker's report was read but every claim was
  re-verified from scratch. Nothing was edited, nothing committed.

## Verdict: NOT PASS (minor findings only — no blocking defect)

The three fixes are **genuine**: the stale stat is gone, the MODEL check really runs before
grill-me in staged + built trees, and all 9 direct commands really carry the guardrail.
The verifier passes 565/565 on my own re-run, both scans pass, the unpin census holds, and
the rebuild is intact. What fails the verdict is **doc accuracy in live decision text**:
stale pre-33c line numbers (L62/L93) and a stale "Phase 0" label survive in the SPEC,
MANIFEST, implementation report, `fix33.py` decision strings (re-emitted into every
regenerated patch log), and `verify33.py` check names/comments. Audit #110 set the
precedent that a stale number in a live doc is a NOT PASS finding (110-M1 was exactly
that); the same standard applies here. None of these changes the tree, none makes the
guardrail bypassable, and the rework is small — but under the stated verdict rules
("PASS only if everything checks out; any real defect = NOT PASS") this is NOT PASS.

- Blocking findings: **none** (no A-B item).
- Minor findings: **A-M1, A-M2** below.

## Findings

### A-M1 (minor) — Stale pre-33c line numbers L62/L93 stated as the current guardrail home

Round 33c moved the operative MODEL check from orchestrate step 0 (old L62) to the
pre-grill block (now **L52**); step 0 is now **L64** (back-reference only) and the picker
note is now **L95**. The tree is correct everywhere (verified §2 below), but live
decision text still cites the old numbers as current:

- `SPEC.md:91` (D33-5 base sentence): "L62 (the MODEL check, renamed from MODEL-PIN
  check, token `MODELSEL_F33`). The picker note (L93) carries the pre-build form." The
  same bullet's D33-20 revision note gives the correct L52/L64/L95, so the bullet
  contradicts itself.
- `SPEC.md:179` (§3(c) Guards, a live post-assertion description): "MODELSEL_F33
  present in orchestrate L14 + L62." (The actual `fix33.py` post-assertion string is
  correct — "identity L14 + pre-grill MODEL check" — so code and SPEC disagree.)
- `MANIFEST.md:182` (Decisions summary): "D33-5 Auto guardrail home (orchestrate
  L14/L62/L93; corrected by D33-19)". Also `MANIFEST.md:178` section header still reads
  "Decisions (D33-1 … D33-19)" although D33-20…D33-24 are listed in the same section.
- `fix33-implementation-report.md:110-111` (D33-5 restatement): "L62 (MODEL check…) +
  L93 picker note" with no D33-20 revision note.
- `fix33.py:513` DECISION-33-19 string, re-emitted verbatim into every regenerated
  patch log (confirmed present in `fix33-patch-log.md` DECISION-33-19): "the guardrail
  is fully present in orchestrate L14 + L62 + L93 (MODELSEL_F33 x2), and the MODEL
  check is an orchestrate step-0 procedure." Both halves are now false: the check is
  at L52/L95, and it is a pre-grill block, not a step-0 procedure (step 0 is only a
  back-reference).
- `verify33.py:3521` §16c check name: "L93 picker note names the specific-model
  selection" (picker note is now L95; the check itself is content-based and passes).

A reader following any of these looks at L62 — the one-engine paragraph — for the MODEL
check and does not find it. **Not findings:** the pre-33c record — SPEC §3(a) table
(:27) and replacement text (:124–126), SPEC D33-19's as-of-then wording (:105),
MANIFEST :20/:103, implementation-report :37/:148 — is historical and correctly framed
(SPEC :204 explicitly says the §3(a) L62/L93 text "describes the pre-33c weave").

**Fix:** L62 → L52, L93 → L95, "step-0 procedure" → "pre-grill block" in the six live
spots above (SPEC D33-5 + §3(c), MANIFEST summary + section header, implementation
report D33-5, `fix33.py` DECISION-33-19 string, `verify33.py` check name). The patch log
picks up the DECISION-33-19 correction on the next regeneration.

### A-M2 (minor) — "Phase 0" mislabel for the orch-pipeline check (it is at Step 0)

The operative check for the five orch-* commands sits at built
`skills/orch-pipeline/SKILL.md` L43, first content of `## Step 0 — Classify size`,
before the classifier's scoring text ("Ceremony scales to blast radius", L45) and far
before Phase 0 Intake (L66). The tree, the orch-* pointer strings ("(Step 0, before
classifying)"), and the §16m line-order checks are all Step-0-correct. But four live
texts call the location "Phase 0":

- `SPEC.md:108` (D33-22 pointer parenthetical): "pointing at the operative check
  (orch-pipeline Phase 0 / the orchestrate skill)".
- `SPEC.md:233` (§6 OWED-33-4): "full ask in gan-build/gan-design/astra-review +
  orch-pipeline Phase 0".
- `fix33.py:516` DECISION-33-22 string (also patch-log DECISION-33-22) and the
  patch-log OWED-33-4 entry: same "Phase 0" wording. The same string also says
  "Step 0 is the first thing the engine does, before the size classifier" — incoherent,
  since Step 0 **is** the size classifier; the accurate statement is that the check is
  the first content of Step 0, before the classifier scores.
- `verify33.py:3677` §16m header comment ("orch-pipeline Phase 0 (the shared choke
  point…)") and `:3696` check name ("points at the orch-pipeline Phase 0 MODEL check").
  Both checks themselves assert the correct "(Step 0, before classifying)" string.

This is an iteration-1 leftover: in iteration 1 the check was woven into Phase 0
Intake, and the move to Step 0 (iteration 2) did not update these labels. SPEC §3(h)
(:205) and D33-22's own mechanism sentence already say Step 0 correctly, so the SPEC
contradicts itself.

**Fix:** "Phase 0" → "Step 0" in the four spots above (and reword the "before the size
classifier" clause). No tree or verifier-logic change is needed.

## What verified clean (with numbers)

### 1. 110-M1 / S-M1 — stale diff stat: FIXED
- `git diff --stat` in scratch-repo: **40 files changed, +166/−115** (measured by me).
  All 40 files are fix33-scope; the 7 files new vs the pre-round 33 are exactly the
  five `commands/orch-*.md`, `commands/orchestrate.md`, and
  `skills/orch-pipeline/SKILL.md` (each confirmed present in the diff).
- `MANIFEST.md:62` and `fix33-implementation-report.md:203` both state exactly
  "40 files changed, +166/−115".
- Grep for `+135` / `+136` / `135/−109` / `136/−109` across SPEC, MANIFEST,
  implementation report, `fix33.py`, `verify33.py`: **zero matches**. The only
  remaining `+135`/`+136` occurrences in the fix dir are inside
  `fix-round-33c-report.md` itself, explicitly framed as the pre-round as-of-then
  state ("was 33 files, +136/−109 pre-round") — legitimate history, not a live quote.

### 2. D-1 / S-M2 — re-sequence: FIXED, genuine in staged + built trees
Staged `new-skills/orchestrate/SKILL.md` and built `skills/orchestrate/SKILL.md` are
identical at every cited line (same line numbers in both trees):
- **L14** cross-ref: "(see the MODEL check below — it runs before grill-me)" ✓.
- **L52** pre-grill block under `## Run`: "**MODEL check — first, before grill-me
  (fix #33, MODELSEL_F33):** in the first reply, state the model…" with the full Auto
  ask; "Grill-me does not start until a specific model is picked — the MODEL check is
  a precondition, not a build step, so grill-me stays FIRST among build steps." ✓
- **L62** one-engine paragraph contains the sequence "MODEL check → grill → scope →
  expansion → build" ✓.
- **L64** step 0: "**MODEL check (fix #33):** already ran before grill-me (see the
  MODEL check above) — if the model is still Auto… stop and ask again" — back-reference
  only, no second operative check ✓.
- **L95** picker note: "select a specific model in the model picker… if the picker is
  on Auto, the orchestrator asks the user to pick a specific model before proceeding
  (see the MODEL check, before grill-me)" ✓.
- `MODELSEL_F33` exactly **2x** in orchestrate, staged + built (L14 + L52) ✓.
- `new-rules/hackathon-mode.mdc` L12 (staged = built): "the MODEL check (fix #33,
  MODELSEL_F33) runs first — before grill-me: … tell the user to pick a specific model
  before grill-me starts. Then run `grill-me` FIRST among build steps… grill-me is the
  first BUILD step, and the MODEL check is not build work." The MODEL clause textually
  precedes "grill-me FIRST" within the line ✓. §7 (L61, staged = built): "plus the
  MODEL check just before it (fix #33, MODELSEL_F33), the one question that precedes
  grill-me" ✓.
- Grill-me-first-for-build-work preserved: grill-me is still FIRST among build steps;
  the model ask is a precondition, not build work (stated in both L52 and L12) ✓.
- SPEC D33-20/D33-21 (:106–107) match the tree line-for-line (L52/L64/L95, L12/§7,
  "proceeding = any work, grill-me included") ✓.
- Staged-vs-built diffs are only the known build transformations: orchestrate differs
  in exactly **3 lines** (102, 276, 283 — `code-reviewer` → `code-reviewer` agent
  (`agents/ecc-code-reviewer.md`) path rewrites); hackathon-mode differs in exactly
  **1 line** (L38 — the known fix16 `claude -p` → `CLI-subprocess` scrub) ✓.

### 3. D-2 / OWED-33-4 — direct-command guardrail: FIXED, genuine in the built tree
Inventory done by me from the built tree (not taken from the report): **9 files** —
`gan-build`, `gan-design`, `astra-review`, five orch-* (`orch-add-feature`,
`orch-build-mvp`, `orch-change-feature`, `orch-fix-defect`, `orch-refine-code`), and
`orchestrate.md`. No staged source exists for any of them (confirmed: `new-skills/`
has no command sources; the commands are built-tree-only) — the `fix33.py` built-tree
weave is the only possible mechanism, and it is the one used.
- `MODELSEL_F33` present **1x in each of the 9 command files** ✓.
- Full MODEL check with the Auto ask ("tell the user to pick a specific model before
  proceeding; do not silently orchestrate on an unknown fallback"):
  - `commands/gan-build.md` **L5** (after frontmatter, before arg parsing at L7) ✓
  - `commands/gan-design.md` **L5** ✓
  - `commands/astra-review.md` **L6** (before `# Deep Review` at L8; `## Step 1: Scope`
    at L12) ✓
  - `skills/orch-pipeline/SKILL.md` **L43** — first content of `## Step 0 — Classify
    size` (header L41, blank L42, check L43), before "Ceremony scales to blast radius"
    (L45) and before Phase 0 Intake (L66) ✓
- One-line pointers at each orch-* entry (**L7**) and `commands/orchestrate.md` (**L7**):
  orch-* pointer reads "the `orch-pipeline` engine runs its MODEL check first (Step 0,
  before classifying)…"; orchestrate.md pointer reads "the orchestrate skill's MODEL
  check runs first, before grill-me (see the skill)…" ✓.
- Guardrail-before-first-work-step ordering verified by line number in each file:
  gan-build L5 < `### Phase 0: Setup` L20; gan-design L5 < `### Setup` L20; astra-review
  L6 < `# Deep Review` L8 / `## Step 1: Scope` L12; orch-* L7 < `## What It Does`
  L24–25; orchestrate.md L7 < `$ARGUMENTS` L13 ✓.
- Choke point verified genuine: each of the five orch-* skills runs the engine in its
  step 1 (`orch-add-feature` L31, `orch-change-feature` L34, `orch-fix-defect` L33,
  `orch-refine-code` L33: "Run the `orch-pipeline` engine…"; `orch-build-mvp` L36:
  "Run orch-pipeline Phases 0–2 ONLY"). The engine file's Step 0 precedes the phases
  list, and the tier table depends on classification, so engine entry runs Step 0
  (and its L43 check) first. gan-build/gan-design/astra-review do not route through
  it (no `orch-pipeline` reference in their skill paths) and carry the full ask at
  their own entries, as designed ✓.
- `fix33.py` has exactly **10 round-33c tuples** (3 full checks + orch-pipeline + 5
  orch-* pointers + orchestrate pointer) — 35 tuples total (25 + 10) — and the patch
  log lists all 10 as applied ✓.
- OWED-33-4 is marked **SUPERSEDED / FIXED** (not deleted) in SPEC §6 (:233), SPEC
  D33-23 (:109), MANIFEST OWED section, `fix33.py` OWED list, and the patch log
  (OWED-33-4 entry) — history retained in all five places ✓. SPEC D33-22/D33-23/D33-24
  (:108–110) match the tree (modulo the A-M2 "Phase 0" label).

### 4. Verifier + scans — re-run by me, and §16l/§16m read, not just executed
- `python3 verify33.py <built-tree>`: **565/565 checks pass, exit 0** (my run,
  `/tmp/audit111-verify.txt`; 565 `PASS` lines, 0 FAILs). Matches the saved
  `verify33-run33c.txt` (565/565).
- Scan r4 (re-run in place): **76/76, ALL PASS, exit 0**.
- Scan r5 (re-run in a probe dir with `fix32.py` + `fix32-patch-log.md` adjacent, probe
  deleted after): **100/100, ALL PASS, exit 0**. Confirms the known B-M2 constraint
  (r5 is not re-runnable in place from fix33/) still holds exactly as documented.
- §16l (9 checks, `verify33.py:3622–3673`) genuinely asserts line order in **both**
  staged and built trees: pre-grill block index < `### Hackathon first build` and <
  step 0; within-line order MODEL-before-grill-me in hackathon-mode L12; MODELSEL 2x;
  L14 cross-ref string; step-0 back-reference string; grill-me-first preserved strings;
  §7 phrase. Not mere text existence.
- §16m (29 checks, `:3675–3720`) genuinely asserts: MODELSEL in all 9 files; the full
  ask anchor in gan-build/gan-design/astra-review + orch-pipeline (with MODELSEL <
  "Ceremony scales…" line-order); the "(Step 0, before classifying)" pointer string in
  the five orch-* + the pre-grill pointer in orchestrate.md; guardrail-before-first-work
  line-order per file (9 files, each against its real first-work anchor); and that the
  MODELSEL line is exactly 2 lines below the `## Step 0` header (first content of the
  section). The two "Phase 0" labels (comment :3677, check name :3696) are the A-M2
  staleness; the asserted strings and order checks are Step-0-correct.
- §16c check 4 now asserts the bold MODEL check lives in the pre-grill block (before
  the first-build sequence and step 0, and that the old "**MODEL check (fix #33,
  MODELSEL_F33):**" bold form is absent from built orchestrate) ✓; §16f asserts
  D33-20…D33-24 + OWED-33-4 SUPERSEDED in the patch log ✓ (24 DECISION-33-* entries
  present in the patch log, D33-1…D33-24).

### 5. Rebuild integrity — run 9
- `build-log-run9.txt`: **BUILD EXIT: 0**; "fix33: 41 change(s)", "fix33: OK",
  "fix31: OK", "fix32: OK" (lines 1283, 1326, 1340, 1358). No traceback; the only
  "error" matches are benign (error strings inside code, house-form notes, and the
  build summary "ERRORS: 0").
- `build-log-run7.txt`: BUILD EXIT: 0, "fix33: 41 change(s)". Run 8: EXIT 1 in ~2s,
  `cp: cannot stat '…/fakehome33/…/fix26/scratch-clones/uipro/.claude/skills/ui-ux-pro-max':
  No such file or directory` — matches the reported rsync `--delete` accident.
- Patch log: **41 changes, 0 errors**; bullet count under `## Changes` re-counted by
  me = 41 (1 census + 36 replacement applications + 3 post-assertions + 2 guards; the
  35 REPLACEMENTS tuples sum to 36 expected applications because one tuple has
  expected-count 2). md5 `4d31215dba852f0c86b19381ee7990cc` in both copies ✓;
  `fix33.py` md5 `8e878b28fe287534afff27f6ca92a9a4` in both copies ✓.
- `less-flat-ui`: global `SKILL.md` md5 `cef0249fbf37ba096c688ce78fa4377f`,
  **534 lines**, unchanged ✓; built `skills/less-flat-ui` is a real directory, not a
  symlink ✓.
- Run-8 residue: fakehome `fix26/scratch-clones/` contains `hack-skills`,
  `skill-add`, `uipro` (restored); durable `~/workspace/hackathon-plugin/fix26/scratch-clones/`
  intact (`uipro/.claude/skills/ui-ux-pro-max` present with SKILL.md). No residue found.

### 6. Unpin still holds
Built census re-measured by me: **ID x0** (`grok-4.7-high`: zero matches outside
strategic-compact), **PROSE x2** (both keeps in `skills/strategic-compact/SKILL.md`,
L68 + L102), **XID x0**, **XPROSE x0**, **fast x72** (72 `grok-4.6-high-fast`
occurrences). `model: inherit` in exactly **4** chat-model agents: `deep-reasoner`,
`ecc-architect`, `ecc-healthcare-reviewer`, `ecc-spec-miner`. Drones/fast tier untouched
(fast count is the pre-existing 71 + 1 schema-description mention, as before).

### 7. Shortfall check — `weave33.py`: confirmed dead, not run by the build
- `grep -rn weave33 <build.sh>`: **no matches** — `build.sh` never invokes it.
  The only references are a comment in `fix33.py:15` and MANIFEST's file list /
  staged-weave description. The worker's "historical one-off script" claim is verified.
- Its stale strings are real (`weave33.py:59,118` "(see the MODEL check in step 0)";
  `:96` "L62 MODEL-PIN check -> MODEL check") but inert: the staged files it once wrote
  have been re-edited by hand in round 33c (L52 block, L64 back-reference, L95 picker
  note), and no build step re-runs the script. Not a finding; recorded as confirmed.

## Observations (not findings)

- **Run-7 562/565 is not independently re-verifiable.** The run-7 post-rebuild verifier
  output was overwritten in `verify33-run33c.txt` by the run-9 565/565 pass, and the
  pre-rebuild 524/565 was observed on stdout only. The 562/565 figure (3 iteration-2
  FAILs: CUT allow-list 137→139, 16l L12 order, 16m orch-pipeline Intake→Step 0) survives
  only in the 33c report + MANIFEST run-7 entry. I verified the *fixes* for all three
  are present in the current tree and verifier (allow-list 139, L12 MODEL-first wording,
  Step 0 location), so the account is consistent — but the 562/565 number itself is
  taken on record, not re-measured.
- **Orch-build-mvp choke-point reading.** Its skill step 1 says "Run orch-pipeline
  Phases 0–2 ONLY" — a literal reader could ask whether Step 0 (the classifier + the
  L43 check) is inside "Phases 0–2". The engine's own structure settles it: Step 0
  precedes the phases list, the tier table is driven by classification, and the other
  four orch-* skills say "Run the `orch-pipeline` engine" without a phase restriction.
  No change needed; noted so the next auditor does not re-open it.
- **Hackathon-mode L2 frontmatter** still says "grill-me first" in the rule description
  ("Hackathon mode — full ECC process, grill-me first, …"). That is a description tag,
  not an instruction; the operative L12 now qualifies it ("grill-me is the first BUILD
  step, and the MODEL check is not build work"). Not a finding.
- **Live test still owed.** The guardrail is verified statically only (565 checks +
  r4/r5). Whether Cursor actually surfaces the ask before grill-me on Auto can only be
  shown by Anish's live test in Cursor (`fix30/live-test-prompt.md`); unchanged from
  prior rounds.

## Commands run (exact)

```sh
cd ~/workspace/hackathon-plugin/fix33/scratch-repo && git diff --stat   # 40 files, +166/−115
grep -rn '+135\|+136' SPEC/MANIFEST/impl-report/fix33.py/verify33.py     # ZERO in live docs
# staged + built orchestrate / hackathon-mode line checks (L14/L52/L62/L64/L95; L12/§7 L61)
# direct-command inventory + line checks (gan-build L5, gan-design L5, astra-review L6,
#   orch-pipeline L43, orch-*/orchestrate.md L7 pointers; 9 files)
cd ~/workspace/hackathon-plugin/fix33 && python3 verify33.py <built-tree>  # 565/565, exit 0
python3 scan32-r4-test-fix33.py                                             # 76/76 ALL PASS
# r5 in /tmp probe dir with fix32.py + fix32-patch-log.md adjacent              # 100/100 ALL PASS
md5sum fix33-patch-log.md scratch-repo/fix33/fix33-patch-log.md              # 4d31215d… both
md5sum fix33.py scratch-repo/fix33/fix33.py                                 # 8e878b28… both
md5sum ~/workspace/cursor-skills/less-flat-ui/SKILL.md                      # cef0249f…, 534 lines
grep -rn 'weave33' scratch-repo/build.sh                                    # no matches
```

## Recommended rework (small, docs-only)

Correct A-M1 + A-M2 in SPEC.md (D33-5, §3(c) Guards, D33-22, §6 OWED-33-4), MANIFEST.md
(Decisions summary + section header), `fix33-implementation-report.md` (D33-5),
`fix33.py` (DECISION-33-19, DECISION-33-22, OWED-33-4 strings), and `verify33.py`
(§16c check name, §16m comment + check name). No tree change is needed. The patch log
picks up the `fix33.py` string corrections on the next build regeneration; if no rebuild
is run, note the patch log still carries the stale DECISION-33-19/33-22 wording.
