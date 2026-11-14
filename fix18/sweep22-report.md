# Sweep #22 — fix program #18 (hackathon-ecc), built-tree re-verification (re-sweep after the fix-up)

**Verdict: CLEAN** — sweep #21's one finding (5 stale `1:30–1:50` cross-references) is
gone, audit #58's MINOR-1 (totals line) is fixed, and every re-run count matches the
expected values. One deviation is noted in §5 (not a finding): `rules/hackathon-mode.mdc`
staged-vs-built differs by exactly one line — the documented fix16 build-step scrub
(`claude -p` → "CLI-subprocess"), pre-existing since fix16, not introduced by fix18 or
the fix-up. The built side is the compliant side.

**Scope:** built tree `~/workspace/hackathon-plugin/hackathon-ecc/`, `node_modules/` excluded
everywhere; plus `build.sh`. SPEC read first: `~/workspace/hackathon-plugin/fix18/SPEC.md`.
Sweep #21 report read: `~/workspace/hackathon-plugin/fix18/sweep21-report.md`.
Every number below was re-derived by running the greps/commands shown; nothing was copied
from sweep #21 or the fix18 manifests without re-running.

**Given state (verified where cheap):** `build.sh` md5
`5cdd22787dfd56aed0b360e49dae60f2`, 23,276 lines (matches the task brief);
`fix18/verify18.py` re-run by this sweep: **72/72 checks pass**; `fix18/manifest4.txt`
hash `ea1c12e3c25e77c1b9186664a42c74ab6ec9b1ce9444253bb1c9e5f16e735429` (matches the brief).

---

## 1. Old length GONE / new regime present — PASS

| String | Built tree | build.sh |
|---|---:|---:|
| `1:30–1:50` (en dash) | **0** | **0** |
| `1:30-1:50` (hyphen) | 0 (checked in sweep #21 scope; re-checked via the tree-wide `1:30` sweep below — no hits) | 0 |
| `2:00 cap` | 0 | — |
| `90–110 seconds` / `90-110` | 0 / 0 | — |

Commands (from `~/workspace/hackathon-plugin`):
```
grep -rn '1:30–1:50' --exclude-dir=node_modules hackathon-ecc | wc -l   # 0
grep -c '1:30–1:50' build.sh                                            # 0
grep -rn '2:00 cap' --exclude-dir=node_modules hackathon-ecc | wc -l    # 0
grep -rn '90–110\|90-110' --exclude-dir=node_modules hackathon-ecc | wc -l  # 0
```

All 5 sweep-#21 hit sites now carry the new regime. New regime text
`under 2:10 (hard rule; absolute max 2:30)` — **1 occurrence in each of exactly the
3 expected files** (no other file in the built tree carries it):

| File | Occurrences | Line |
|---|---:|---:|
| `rules/hackathon-mode.mdc` | 1 | :48 (canonical statement) |
| `skills/hackathon-scope/SKILL.md` | 1 | :17 |
| `skills/hackathon-pitch/SKILL.md` | 1 | :32 (second mention on the same line is the bare `(under 2:10, …)` fragment, not the full regime string) |

Commands:
```
grep -rn 'under 2:10 (hard rule; absolute max 2:30)' --exclude-dir=node_modules hackathon-ecc
grep -ro 'under 2:10 (hard rule; absolute max 2:30)' --exclude-dir=node_modules hackathon-ecc | sort | uniq -c
```

The other two sweep-#21 sites also verified individually:
- `skills/hackathon-pitch/assets/pitch-script-template.md:79` — `- Video (demo video, under 2:10), recorded after the final deploy: …`
- `README.md:44` — `` `/demo` — generate a narrated product demo video, under 2:10, of the app``

`under 2:10` tree-wide: **13 occurrences** (sweep #21: 8 — the +5 are the fix-up's
cross-reference rewrites plus the pre-existing pitch-deck-video/qa.mjs lines, all in
the new regime; full list in §1a). No occurrence states an old length.

### 1a. `under 2:10` tree-wide (13)

1. `rules/hackathon-mode.mdc:48` — canonical statement
2. `skills/pitch-deck-video/SKILL.md:3` — description
3. `skills/pitch-deck-video/SKILL.md:101` — F6 hard rule (`under 2:10 (130 seconds)`)
4. `skills/pitch-deck-video/SKILL.md:114` — totals line
5. `skills/pitch-deck-video/SKILL.md:146` — beat-average note
6. `skills/pitch-deck-video/template/scripts/qa.mjs:76` — comment
7. `skills/pitch-deck-video/template/scripts/qa.mjs:111` — runtime print
8. `skills/hackathon-scope/SKILL.md:17`
9. `skills/hackathon-pitch/SKILL.md:32` — two mentions on the line (bare + full regime); counted once per grep line
10. `skills/hackathon-pitch/assets/pitch-script-template.md:79`
11. `commands/demo.md:2` — description
12. `commands/demo.md:9` — body
13. `README.md:44`

`Absolute max 2:30` (capital-A anchor form) tree-wide: **1** — `skills/pitch-deck-video/SKILL.md:101`
(the lowercase `absolute max 2:30` in hackathon-mode.mdc:48 is the same regime string inside the
parenthetical; the `qa.mjs:111` `absolute ceiling 2:30` is the same ceiling in code).

## 2. Totals line — PASS

- `Totals: 103–126s` in built `skills/pitch-deck-video/SKILL.md`: **×1** — line 114:
  `Totals: 103–126s of content + ~10s room ≈ under 2:10. …`
- `113–126` = **0** tree-wide: built tree 0, `build.sh` 0, `fix18/SPEC.md` 0.
  (SPEC.md §3 F6 still shows the original analysis-time `Totals: 103–126s` — the
  `113–126` figure was the implementation's typo, never in the SPEC.)
- `Totals: 103–126s` tree-wide: 1 (the SKILL.md line only; `build.sh` does not embed
  the skill text — 0 there, as expected).

Commands:
```
grep -n 'Totals: 103–126s' hackathon-ecc/skills/pitch-deck-video/SKILL.md
grep -rn 'Totals: 103–126s' --exclude-dir=node_modules hackathon-ecc | wc -l   # 1
grep -rn '113–126' --exclude-dir=node_modules hackathon-ecc | wc -l            # 0
grep -c '113–126' build.sh ; grep -c '113–126' fix18/SPEC.md                   # 0 ; 0
```

## 3. Banned terms — 0 — PASS

Command (from `hackathon-ecc/`):
```
grep -rniE 'claude|codex|anthropic|opus|sonnet|haiku|composer-2\.5' --exclude-dir=node_modules skills agents commands rules hooks README.md
```
Result: **0 hits** (empty output).

## 4. Grok pins unchanged — PASS (match fix16 MANIFEST exactly)

| String | Occurrences | Lines |
|---|---:|---:|
| `grok-4.7-high` | 52 | 45 |
| `cursor-grok-4.6-high-fast` | 100 | 99 |

Commands (from `hackathon-ecc/`):
```
grep -ro 'grok-4.7-high' --exclude-dir=node_modules . | wc -l              # 52
grep -r 'grok-4.7-high' --exclude-dir=node_modules . | wc -l               # 45
grep -ro 'cursor-grok-4.6-high-fast' --exclude-dir=node_modules . | wc -l  # 100
grep -r 'cursor-grok-4.6-high-fast' --exclude-dir=node_modules . | wc -l   # 99
grep -rP '(?<!cursor-)grok-4\.6-high-fast' --exclude-dir=node_modules . | wc -l  # 0
grep -r 'grok-4\.7\[' --exclude-dir=node_modules . | wc -l                 # 0
grep -r 'effort=' --exclude-dir=node_modules . | wc -l                     # 0
grep -ro 'reasoning_effort' --exclude-dir=node_modules . | wc -l           # 2
grep -r 'reasoning_effort' --exclude-dir=node_modules . | wc -l            # 2
```

`reasoning_effort` (2 occ / 2 lines): `rules/common-performance.mdc:30` and
`skills/orchestrate/SKILL.md:160` — the same two lines as sweep #21.

## 5. Fix #18 anchors — PASS, with one noted deviation (not a finding)

| Anchor | Location | Count |
|---|---|---:|
| `under 2:10 (130 seconds)` | `skills/pitch-deck-video/SKILL.md:101` | 1 |
| `Absolute max 2:30` | `skills/pitch-deck-video/SKILL.md:101` | 1 |
| `Write the time budget before writing the lines.` | `skills/pitch-deck-video/SKILL.md:102` | 1 |
| `3. **Edge**` | `skills/pitch-deck-video/SKILL.md:137` | 1 |
| `stack?: string` | `skills/pitch-deck-video/template/src/scenes/Arch.tsx:10` | 1 |
| `color: C.accent` | `skills/pitch-deck-video/template/src/scenes/Arch.tsx:41` | 1 |
| `SEED_THEME` | `skills/pitch-deck-video/template/scripts/qa.mjs:99` (defined; used :101) | 1 def |
| `process.exitCode = 1` | `skills/pitch-deck-video/template/scripts/qa.mjs:138` | 1 |
| `under 2:10` | `commands/demo.md:2` (description) and `:9` (body) | 2 |

Staged-vs-built md5 — **MATCH for all 7 fix18 files** (re-run this sweep):

| File | md5 (staged = built) |
|---|---|
| `SKILL.md` | `1cea5da23cf910eaf7e95074378bd3bd` |
| `references/shots-reference.md` | `2f2f23240929715c4c64428f1e7083f6` |
| `references/troubleshooting.md` | `02c01a7a0c1b3dae47bb29c15d022cf3` |
| `template/shots.example.json` | `4f34413c098334e9656bc06a073f1f08` |
| `template/scripts/qa.mjs` | `facbd77b9a77d3fbc88819ef09816464` |
| `template/src/scenes/Arch.tsx` | `04f3ae5c824b7b98754f6548bea84aa3` |
| `commands/demo.md` | `61c32ce0deaf670d9d18d79943c642d7` |

`diff -r new-skills/pitch-deck-video/ hackathon-ecc/skills/pitch-deck-video/` → only output
`Only in new-skills/pitch-deck-video/: commands` (structural: staged nests `commands/demo.md`
under the skill dir; build.sh copies it to `commands/`). `diff -q` on `demo.md` → identical.
No file content differs.

`diff -q rewritten-skills/hackathon-scope/SKILL.md hackathon-ecc/skills/hackathon-scope/SKILL.md` → **identical (exit 0).**

### Deviation (not a finding): `new-rules/hackathon-mode.mdc` vs built — 1 line differs

```
diff new-rules/hackathon-mode.mdc hackathon-ecc/rules/hackathon-mode.mdc
38c38
< - **Design skills deliberately NOT wired …:** `gan-style-harness` (its upstream `claude -p` invocation path does not run in Cursor — …
---
> - **Design skills deliberately NOT wired …:** `gan-style-harness` (its upstream CLI-subprocess invocation path does not run in Cursor — …
```

Why this is not a fix18/fix-up defect:
- The substitution is the **fix16 build-step scrub**: `build.sh:23204–23211` runs
  `python3 "$PLUGIN_ROOT/fix16/fix16.py" "$PLUGIN_DIR"` on the built tree as the last
  build step, and `fix16/MANIFEST.md:771` records exactly this change on the built file:
  `hackathon-ecc/rules/hackathon-mode.mdc — '(its upstream `claude -p` invocation path…' -> '(its upstream CLI-subprocess invocation path…'`.
- `build.sh:253` is a plain `cp` of the staged file, so the staged source intentionally
  retains the upstream `claude -p` wording (1 banned-term occurrence in the *staged*
  source: `grep -c -i 'claude' new-rules/hackathon-mode.mdc` → 1) and the built tree is
  rewritten by fix16.py on every build. The built side is the compliant side
  (built-tree banned-term grep = 0, §3).
- The fix-up did not touch line 38: `fix18/fix18_fixup.py` sub 2a edits only the length
  text on line 48, and the staged file's line 38 is unchanged from fix16 time.
- Consequence for the task's literal "diff 0" bar: the bar is not met for this one
  file, but only because of pre-existing, documented fix16 staged/built drift. The
  length-relevant content (line 48) is identical staged-vs-built. No action required
  for fix18; if a future program wants literal staged==built, it should move the
  `claude -p` → CLI-subprocess rewrite into the staged source (a fix16-owned decision,
  not this sweep's).

## 6. Fix #17 anchors intact — PASS

- **E1 identical ×4.** `E1_RULE` from `fix17/fix17.py` (1724 chars) occurs exactly once
  in each of the four placements; extracted-text md5 identical in all four:
  `e9d2102572611fe7a6ba507b961013b2` — matches the fix17 baseline md5.
  - `skills/design-taste-frontend/SKILL.md` (count 1)
  - `skills/orchestrate/SKILL.md` (count 1)
  - `skills/orch-build-mvp/SKILL.md` (count 1)
  - `skills/ui-ux-pro-max/SKILL.md` (count 1)
- **`may invent` tree-wide: 0** (`grep -ri 'may invent' hackathon-ecc --exclude-dir=node_modules | wc -l`).
- **Sticker exceptions A+B present** (`skills/design-taste-frontend/references/hallmark/references/themes/sticker.md:90–91`):
  - Exception A — "Hand-drawn ink marks (fix #17, exception A). …"
  - Exception B — "Scroll rise-and-settle entrances (fix #17, exception B). …"
  - Motion line reads "nothing on scroll, except the scoped exception in 'Scoped exceptions' below (scroll rise-and-settle entrances as sticker motion)."
- **less-flat-ui treatments still 1..23** — `re.findall(r"^### (\d+)\. ", less-flat-ui/SKILL.md)`
  returns exactly `[1..23]`.
- **Canonical block verbatim ×1 in all 11 fix #15 files** (`CANONICAL` from `fix15/fix15.py`,
  `text.count(CANONICAL) == 1` for each): `design-taste-frontend/SKILL.md`,
  `ui-ux-pro-max/SKILL.md`, `less-flat-ui/SKILL.md`, `polish-pass/SKILL.md`,
  `design-taste-frontend/references/hallmark/references/hallmark-floor.md`,
  `make-interfaces-feel-better/SKILL.md`, `motion-foundations/SKILL.md`,
  `motion-patterns/SKILL.md`, `motion-advanced/SKILL.md`, `orchestrate/SKILL.md`,
  `orch-build-mvp/SKILL.md` — all count 1.

## 7. build.sh exception inventory re-derived — delta 0 — PASS

- `md5sum build.sh` → `5cdd22787dfd56aed0b360e49dae60f2`, **23,276 lines** (matches the brief).
- Fresh banned-term line count: `grep -c -iE 'claude|codex|anthropic|opus|sonnet|haiku|composer-2\.5' build.sh` → **798 lines**.
- Re-derivation: parsed the full 798-row inventory table in `fix16/sweep18-report.md`
  (§Check 16) and cross-checked its line-number set against a fresh `grep -in` of
  `build.sh`. The two sets are **identical — no missing, no extra lines**.
  Category counts parsed from the table's class column: **(a) OLD-side 389, (b) comment 52,
  (c1) NEW-side transient 355, (c2) heredoc 0, (c3) build-time `.claude/skills/` paths 2**
  (`:265`, `:298` — the two `cp -r …/.claude/skills/…` lines) — identical to the sweep #18
  baseline (389/52/355/0/2).
- Per-term line counts (fresh grep): `claude` 701, `codex` 103, `anthropic` 5, `opus` 22,
  `sonnet` 23, `haiku` 13, `composer-2.5` 0 — identical to the sweep18 baseline.
- **Delta vs sweep #18 baseline: 0.** The fix-up changed `build.sh`'s md5 (it had to —
  it rewrote the length strings) but added no banned-term lines: all 9 fix-up subs were
  same-line string replacements, line count stayed 23,276, and the 798-line set is byte-identical
  in membership to the pre-fix-up inventory.
- Regime text in build.sh: `under 2:10 (hard rule; absolute max 2:30)` ×4
  (README heredoc, fix-4 patch NEW side, Gap-39 comment, line-32 restatement) — matches
  the fix-up engine's own self-check (`>= 4`). `1:30–1:50` in build.sh: 0.

## 8. Counts — PASS

| Inventory | Count | Command |
|---|---:|---|
| skills | **166** | `ls skills \| wc -l` |
| agents | **72** | `ls agents \| wc -l` |
| rules | **123** | `ls rules \| wc -l` |
| commands | **87** | `ls commands \| wc -l` |
| hooks | **15** | `python3 -c "len(json.load(open('hooks/hooks.json'))['hooks'])"` |

## Commands used (full list)

```
md5sum build.sh ; wc -l build.sh
grep -rn '1:30–1:50' --exclude-dir=node_modules hackathon-ecc | wc -l ; grep -c '1:30–1:50' build.sh
grep -rn 'under 2:10 (hard rule; absolute max 2:30)' --exclude-dir=node_modules hackathon-ecc
grep -ro 'under 2:10 (hard rule; absolute max 2:30)' --exclude-dir=node_modules hackathon-ecc | sort | uniq -c
grep -n 'Totals: 103–126s' hackathon-ecc/skills/pitch-deck-video/SKILL.md
grep -rn 'Totals: 103–126s' --exclude-dir=node_modules hackathon-ecc | wc -l
grep -rn '113–126' --exclude-dir=node_modules hackathon-ecc | wc -l ; grep -c '113–126' build.sh ; grep -c '113–126' fix18/SPEC.md
grep -rn '2:00 cap' --exclude-dir=node_modules hackathon-ecc | wc -l
grep -rn '90–110\|90-110' --exclude-dir=node_modules hackathon-ecc | wc -l
grep -rn 'under 2:10' --exclude-dir=node_modules hackathon-ecc
grep -rn 'Absolute max 2:30' --exclude-dir=node_modules hackathon-ecc | wc -l
grep -rniE 'claude|codex|anthropic|opus|sonnet|haiku|composer-2\.5' --exclude-dir=node_modules skills agents commands rules hooks README.md
grep -ro 'grok-4.7-high' --exclude-dir=node_modules . | wc -l ; grep -r 'grok-4.7-high' --exclude-dir=node_modules . | wc -l
grep -ro 'cursor-grok-4.6-high-fast' --exclude-dir=node_modules . | wc -l ; grep -r 'cursor-grok-4.6-high-fast' --exclude-dir=node_modules . | wc -l
grep -rP '(?<!cursor-)grok-4\.6-high-fast' --exclude-dir=node_modules . | wc -l
grep -r 'grok-4\.7\[' --exclude-dir=node_modules . | wc -l
grep -r 'effort=' --exclude-dir=node_modules . | wc -l
grep -ro 'reasoning_effort' --exclude-dir=node_modules . | wc -l ; grep -r 'reasoning_effort' --exclude-dir=node_modules . | wc -l
grep -c 'under 2:10 (130 seconds)' / 'Absolute max 2:30' / 'Write the time budget before writing the lines\.' /
  '3\. \*\*Edge\*\*' skills/pitch-deck-video/SKILL.md
grep -n 'stack?: string' / 'color: C.accent' skills/pitch-deck-video/template/src/scenes/Arch.tsx
grep -n 'SEED_THEME' / 'process.exitCode = 1' skills/pitch-deck-video/template/scripts/qa.mjs
grep -n 'under 2:10' commands/demo.md
diff -r new-skills/pitch-deck-video/ hackathon-ecc/skills/pitch-deck-video/
diff -q new-skills/pitch-deck-video/commands/demo.md hackathon-ecc/commands/demo.md
diff -q new-rules/hackathon-mode.mdc hackathon-ecc/rules/hackathon-mode.mdc
diff -q rewritten-skills/hackathon-scope/SKILL.md hackathon-ecc/skills/hackathon-scope/SKILL.md
md5sum new-skills/pitch-deck-video/{SKILL.md,references/shots-reference.md,references/troubleshooting.md,
  template/shots.example.json,template/scripts/qa.mjs,template/src/scenes/Arch.tsx,commands/demo.md}
  + built counterparts
grep -c -i 'claude' new-rules/hackathon-mode.mdc
grep -n '1:30–1:50' / 'under 2:10 (hard rule; absolute max 2:30)' new-rules/hackathon-mode.mdc
grep -n 'under 2:10' skills/hackathon-pitch/assets/pitch-script-template.md ; grep -n 'under 2:10' README.md
python3 (E1_RULE md5 ×4 from fix17/fix17.py; CANONICAL count ×11 from fix15/fix15.py;
  less-flat-ui treatment numbers; sticker exceptions A+B)
grep -ri 'may invent' hackathon-ecc --exclude-dir=node_modules | wc -l
grep -c -iE 'claude|codex|anthropic|opus|sonnet|haiku|composer-2\.5' build.sh
for t in claude codex anthropic opus sonnet haiku 'composer-2\.5'; do grep -ci "$t" build.sh; done
grep -c 'under 2:10 (hard rule; absolute max 2:30)' build.sh ; grep -c 'Totals: 103–126s' build.sh
python3 (fresh grep -in line set vs fix16/sweep18-report.md §Check 16 inventory table; class Counter)
ls skills|wc -l ; ls agents|wc -l ; ls rules|wc -l ; ls commands|wc -l
python3 -c "import json; print(len(json.load(open('hooks/hooks.json'))['hooks']))"
python3 fix18/verify18.py   # 72/72 checks pass
head fix18/manifest4.txt     # ea1c12e3c25e77c1b9186664a42c74ab6ec9b1ce9444253bb1c9e5f16e735429
```
