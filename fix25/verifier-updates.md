# Fix #25 §4(a) — verifier updates (worker C)

Parent-authorized exception to "prior verifiers are NOT edited". Only the
two files named in the task were edited among verifiers: `fix23/verify23.py`
(S1 assertion) and `fix13h/verify13h.py` (F-04 M3 expectations).
`fix24/verify24.py` was NOT edited. No rebuild was run; a later worker
builds and runs the loops.

## "51 active" finding

Re-counted from `data/styles.csv` (Status column): **51 active is correct**
— 51 active / 29 supplemental / 9 deprecated = 89 rows, 89 distinct Style
IDs. Only the "80" in the header was wrong. The header now reads
"89 searchable styles (51 active)" in both places; the active count is
unchanged.

## Update 1 — S1 styles.csv header 80 → 89

### Where the staged/upstream boundary actually is (verified, not assumed)

The task assumed the whole header was a build-time patch. It splits:

- **Built `skills/ui-ux-pro-max/SKILL.md:3` (frontmatter description)** is
  written by `build.sh:584-586` (`replace_desc_line("ui-ux-pro-max", …)`):
  the NEW string carries "80 searchable styles (51 active)". The OLD string
  (line 585) is the upstream anchor and stays 80.
- **Built `SKILL.md:8`** ("Searchable local UI/UX guidance: 80 searchable
  styles…") is upstream verbatim — `build.sh` never touches that string.
- **Inventory `:29`** is staged
  (`new-skills/orchestrate/references/design-inventory.md`), edited directly.

### Decision: patch BOTH header lines in `fix25/fix25.py`, not `build.sh:586`

Editing the replacement string in `build.sh` would introduce the fix's
first deletion in `diff build.sh.before-fix23 build.sh` (breaking the
additions-only invariant every verifier asserts). The file as a whole has
no staged source and is already patched at build time by `fix24.py`
(C4b, F-10), so the S1 patch lives there with the `:8` patch, and the
`build.sh` diff stays additions-only (+305/-0 after my 9-line invocation
block). Recorded in `fix25/fix25.py`'s header.

### Edits

1. `new-skills/orchestrate/references/design-inventory.md:29`
   - Old: `| Styles — 89 rows in \`data/styles.csv\` (skill header describes 80 searchable styles, 51 active; the csv is the inventory source) | …`
   - New: same line with `80 searchable styles` → `89 searchable styles`
     (rest of the line unchanged; "the csv is the inventory source" kept).
2. `fix25/fix25.py` (NEW, fix24.py pattern: `sub()` asserts count==1,
   fails loudly, run log, exit non-zero on error)
   - Patch 1: `skills/ui-ux-pro-max/SKILL.md`,
     `"Searchable local data: 80 searchable styles (51 active)"` →
     `"Searchable local data: 89 searchable styles (51 active)"`
   - Patch 2: same file,
     `"Searchable local UI/UX guidance: 80 searchable styles (51 active)"` →
     `"Searchable local UI/UX guidance: 89 searchable styles (51 active)"`
   - Run log is `fix25/fix25-patch-log.md` — NOT `fix25-run-log.md`,
     which is the coordinator's shared worker log (workers D/E already
     wrote there); overwriting it would destroy their entries.
   - Tested against a scratch copy of the built SKILL.md: 2 changes,
     exit 0, 0 occurrences of "80 searchable styles" left. Scratch
     removed from /tmp afterwards.
3. `build.sh` (+9 lines, additions only, after the fix24 invocation,
   before STEP 5 Counts): comment block + invocation
   `python3 "$PLUGIN_ROOT/fix25/fix25.py" "$PLUGIN_DIR"`.
   build.sh is now **24,079 lines, md5 f19483f50e89998f8b9dc052ed5d5fae**;
   diff vs `build.sh.before-fix23` is **+305/-0**.
4. `fix23/verify23.py` — assertion + docstring:
   - Docstring (§1): the "known styles.csv 89 vs header 80 discrepancy"
     paragraph → "the styles.csv count (89 rows; fix #25 §4(a) corrected
     the header from 80 to 89 searchable styles, 51 active, with this
     assertion updated in the same change; the csv remains the inventory
     source)".
   - Check name: `"inventory ui-ux-pro-max styles: 89 csv rows (header 80 recorded, csv is source)"`
     → `"inventory ui-ux-pro-max styles: 89 csv rows (header 89, csv is source)"`
   - `"80 searchable styles" in uipro` → `"89 searchable styles" in uipro`
   - `"80 searchable styles, 51 active" in inv` → `"89 searchable styles, 51 active" in inv`
   - (csv_rows == 89, "89 rows in \`data/styles.csv\`", "the csv is the
     inventory source" conjuncts unchanged.)

### verify23 tails (before / after — both PRE-rebuild; built tree still says 80)

- BEFORE: **196/212** (196/211 excl. the owed manifest check). Failing
  checks: build.sh fingerprint (24,059/df2cb8…), diff +285/-0, the
  INVENTORY/AMBITION/MEMORABLE/MOTION/TYPEAUDIT/TRIO/HERO-BQA/FUNC-BQA/
  FUNC-UIPRO/ALIGN token-census lines, Grok-pins file counts, fix22
  verifier (366/369 vs expected 368/369 — B3/B15 flags), fix23 manifest
  (owed).
- AFTER: **195/212** (195/211 excl. manifest). Exactly ONE new fail:
  `FAIL inventory ui-ux-pro-max styles: 89 csv rows (header 89, csv is source)`
  — the new assertion reads the stale built tree (still "80"). This fail
  clears on rebuild, returning verify23 to 196/212. Confirmed by
  conjunct check: csv_rows==89 True, "89 searchable styles" in uipro
  False (stale), "89 rows" in inv True, "89 searchable styles, 51 active"
  in inv False (stale), "the csv is the inventory source" True.

### verify24 tail — moves, and how

`fix24/verify24.py:233-237` DOES assert the old "80" text
("S1 styles.csv discrepancy asserted as-is (80 header / 89 rows, csv is
source)") and was NOT edited, per the task.

- BEFORE (baseline): **105/105, exit 0.**
- AFTER (pre-rebuild): **101/105** (101/104 excl. manifest). The 4 fails:
  1. `FAIL build.sh is 24,070 lines, md5 b0b2645a… (post-fix24)` — my +9
     invocation lines (now 24,079 / f19483f5…).
  2. `FAIL diff vs build.sh.before-fix23 is additions only (+296/-0)` —
     now +305/-0.
  3. `FAIL fix23 verifier: only expected fails, tail is … 195/211 checks
     pass (expected … 196/211 checks pass)` — cascade of verify23's
     styles check failing pre-rebuild (clears post-rebuild).
  4. `FAIL fix24/MANIFEST.md exists and records build.sh lines + md5` —
     the manifest's recorded post-fix24 fingerprint is stale vs the
     edited build.sh.
  - The S1 check itself PASSES pre-rebuild (built tree still says 80).
- POST-REBUILD expectation (for verify25 to codify): **101/105** with a
  different composition — the fix23-verifier leg passes again (verify23
  back to 196/211), and the **S1 check newly fails** (built tree now says
  89, verify24 asserts 80). Expected post-rebuild fails: fingerprint,
  diff-count, S1, manifest. Only the S1 check is the S1-content failure;
  the other three move for ANY fix #25 build.sh change (my block
  contributes 9 of the added diff lines; sibling workers' blocks add
  more, so the exact +count grows).

## Update 2 — verify13h M3 expectations for the F-04 rename

### Causation analysis (verified from the built tree, not the manifest)

Fix #24's MANIFEST claimed the F-04 rename broke "2 checks (:57,63)".
That count was wrong: a third M3 check fails from the same rename.

Built `hackathon-ecc/skills/orchestrate/SKILL.md` now carries
"Verify-stage-6" / "Verify stage 6" (3 lines, 0 occurrences of
"Verify-step-6" / "Verify step 6"):

| verify13h.py | Old expectation | Built-tree reality | Cause | Action |
|---|---|---|---|---|
| :57 M3 Verify step 6 header | `"**Verify step 6. Hallmark audit"` | `:264` `"**Verify stage 6 (Hallmark audit)"` | F-04 | UPDATED |
| :61 M3 Verify step 4 (UI) header | `"Verify step 4. **Any diff…"` | `:256` `"Verify step 4a. **Any diff…"` | F-03 (steps 1–4b, fix24 MANIFEST §1(c)) | left |
| :62 M3 Verify step 4 (audit) header | `"**Verify step 4. Adversarial audit"` | `:260` `"**Verify step 4b. Adversarial audit"` | F-03 | left |
| :63 M3 budget refs renamed | `"2 rounds total across 5b and Verify step 6"`, want 2 | `"2 rounds total across 5b and Verify stage 6 (Hallmark audit)"` ×2 (`:93`, `:264`) | F-04 | UPDATED |
| :66 M3 design-audit renamed | `"this app-screen audit IS the Verify-step-6 design audit"` | `:264` `"this app-screen audit IS the Verify-stage-6 design audit"` ×1 | F-04 | UPDATED |
| :70 M3 own step-6 ref untouched | `"the step-6 README/final report"` | `:94` `"The step-6 README/final report reports…"` (capital T; sentence reworded) | fix #22 demogate rewrite — `fix22/demogate-apply.py:75` replaced "The 5d demo and the step-6 README/final report film and report…" | left |
| :71 M3 own step-5 ref untouched | `"per orchestrate step 5 above"` | absent (was orchestrate `:279` per fix13h MANIFEST; the sequence line was rewritten by fix #22 demogate, `fix22/demogate-apply.py:86`) | fix #22 demogate cascade | left |

The 2 B2 failures (`"copy the WHOLE tree into"` ×2, orchestrate +
standalone) are not M3 and not F-04 (built `:93` says "copy the whole
tree, except…" — lowercase, reworded); left untouched.

### Edits (`fix13h/verify13h.py` only)

- :57: `"**Verify step 6. Hallmark audit"` →
  `"**Verify stage 6 (Hallmark audit)"` (label also updated:
  "Verify step 6 header" → "Verify stage 6 header").
- :63: `"2 rounds total across 5b and Verify step 6"` →
  `"2 rounds total across 5b and Verify stage 6 (Hallmark audit)"`
  (want stays 2).
- :66: `"this app-screen audit IS the Verify-step-6 design audit"` →
  `"this app-screen audit IS the Verify-stage-6 design audit"`.

### verify13h tails (before / after)

- BEFORE: **VERIFY FAILED (9 of 97)** — 2 B2 + 7 M3 (:57, :61, :62, :63,
  :66, :70, :71). Exit 1. (Matches the parent spot-check: 7 M3 lines.)
- AFTER: **VERIFY FAILED (6 of 97)** — 2 B2 + 4 M3 (:61, :62, :70, :71).
  Exit 1. The three F-04 checks now pass. Remaining fails are all
  out of the authorized scope (F-03 ×2, fix #22 demogate cascades ×2,
  B2 ×2) and are left failing for the coordinator / verify25 to codify
  or a future authorized update to address.

## Files touched (complete list)

- `fix23/verify23.py` — S1 assertion + docstring (authorized).
- `fix13h/verify13h.py` — 3 M3 expectations (authorized).
- `new-skills/orchestrate/references/design-inventory.md:29` — staged
  inventory line 80→89.
- `fix25/fix25.py` (new) — build-time S1 patch, 2 anchors.
- `build.sh` — +9 lines (fix25 invocation block); 24,079 lines,
  md5 f19483f50e89998f8b9dc052ed5d5fae; diff vs before-fix23 +305/-0.
- `fix25/verifier-updates.md` (this note).

NOT edited: `fix24/verify24.py`, `fix23/` + `fix24/` SPECs/MANIFESTs
(historical records), any other verifier, the built tree
(`hackathon-ecc/`), `fix11/fix11-stage.py` (never run).

## Open items / things I could not verify

- Post-rebuild tails are PREDICTED, not measured: no rebuild was run
  (per task). The later build worker must confirm verify23 returns to
  196/212 and verify24 lands at 101/105 with fails = fingerprint,
  diff-count, S1, manifest. If sibling workers' build.sh additions
  change the diff +count further, the diff-count check still fails on
  the count (and verify25 codifies the final number).
- The upstream ui-ux-pro-max clone (`/tmp/uipro`) is absent from this
  VM, so the `:8` line could not be checked against upstream directly;
  it is confirmed upstream-verbatim only by elimination (no `build.sh`
  hit for that string, and the built `:3` is fully explained by
  `replace_desc_line`). If upstream ever changes the counts, the
  `fix25.py` anchors fail loudly at build time, which is the intended
  behavior.
- Worker A (call map) was still running when this note was written; if
  it also needs a `fix25.py` patch, the coordinator must merge it with
  this script (workers D/E needed none).
