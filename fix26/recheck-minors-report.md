# Fix #26 — Recheck of Audit #73 / Sweep #34 minor findings

Re-verification run: Sat 2026-11-14, after rebuild run 4. Every number below was
re-derived with fresh greps/counts/diffs by this re-checker; nothing was copied
from the coordinator's claims. No build was run, no plugin file was edited, and
`generate_call_map.py` was read only, never executed.

## 1. Sweep #34 MINOR 1 — generator :383 "live routing table" comment — PASS

- `fix25/callmap/generate_call_map.py:383` now reads:
  `# skill-triggers@1.json is a documentation-only reference table, not install data.`
  (context :380–386 verified by `sed -n '375,390p'`).
- Remaining occurrences of the phrase "live routing table" (grep over
  `new-skills/ round2-skills/ rewritten-skills/ new-rules/ hackathon-ecc/
  fix25/callmap/generate_call_map.py`):
  - `new-skills/orchestrate/references/call-map.md:38` and the identical built
    copy `hackathon-ecc/skills/orchestrate/references/call-map.md:38` — the B6
    bullet, which says the file is "not a live routing table". Correct
    negation; does not count.
  - `fix25/callmap/generate_call_map.py:764` — the same B6 bullet string the
    generator emits into the call map ("not a live routing table — verified by
    grep in fix #26"). Same correct negation.
- No place asserts skill-triggers **is** a live routing table. Fixed as claimed.

## 2. Sweep #34 MINOR 2 — bare "on-request (trigger-routed)" flow strings — PASS

- Generator `fix25/callmap/generate_call_map.py:342` now returns
  `"on-request (trigger-routed; no live Cursor entry — see method note B6)"`.
- Staged `new-skills/orchestrate/references/call-map.md`:
  qualified `128`, bare `0` (`grep -c "on-request (trigger-routed)"` = 0; the
  qualified form does not contain the bare substring). Split: skills table 64
  qualified / 0 bare; trigger-keys table 64 qualified / 0 bare.
- Built `hackathon-ecc/skills/orchestrate/references/call-map.md`: qualified
  `128`, bare `0`. md5 staged = built = `8d4c10efefbd844603e6743ed9893718`.
- Regen diff re-derived against the retained pre-fix copy
  `fix26/scratch/call-map-before-minor-fix.md`: `diff` gives 64 `<` lines and
  64 `>` lines, all single-line `NcN` changes (128 lines total, 64 rows x 2
  sides), each changing only the flow string — no flow-ordering churn, no
  insertions/deletions. Pre-fix file had 64 bare + 64 qualified; post-fix 0
  bare + 128 qualified.
- B6 bullet intact at call-map `:38` (staged and built), wording
  "DOCUMENTATION-ONLY" present.
- `fix25/callmap/call-map-data.json`: counts `skills 166 / agents 72 /
  rules 123 / commands 87 / hooks 15 / triggers 64`, `trigger_only: []`;
  md5 `d78622ce4e218bdea197365f15bae623`, moved from pre-fix
  `a75c2a9fe99ee94a99a18c28eb4eb487` (retained copy
  `fix26/scratch/call-map-data-before-minor-fix.json`, counts identical —
  only the stored flow strings changed).

## 3. Audit #73 M1 — verify25.py docstring "+305/-0" — PASS

- `fix25/verify25.py:22` (via `sed -n '22p'`): `diff vs
  build.sh.before-fix23 additions only (+314/-0); counts`.
- Assertion `fix25/verify25.py:176`: `check("diff vs build.sh.before-fix23
  is additions only (+314/-0)", ...)` — docstring and assertion agree.
- `grep -n "+305" fix25/verify25.py`: no matches (exit 1). `grep -n "+314"`:
  lines 22 and 176 only.

## 4. Audit #73 M2 — build.sh fix #26 comment — PASS

- `build.sh:24070` header: `# --- fix #26: build-time patches (ck cost lines
  + §1 pip pins) ---` (verified via `awk NR 24068–24078`).
- `build.sh:24075`: `# §1 pip pins (13 upstream lines, P-01–P-13) land in the
  same script.` (the task text cited :24075 for this line; the header is
  :24070 and the pip-pins line is :24075 in the current file — both read as
  claimed).
- `grep -n "placeholder section" build.sh`: no matches (exit 1).
- Re-measured: `wc -l build.sh` = `24088` lines; md5
  `e1944a6e2b81bf3b869c191633c04aae` (matches the post-M2-edit value; the M2
  edit came after run 4, as stated). `diff build.sh.before-fix23 build.sh`:
  `grep -c "^>"` = `314` additions, `grep -c "^<"` = `0` deletions — i.e.
  **+314/-0**, as claimed.

## 5. Regression spot-check on the rebuilt tree — PASS

All counts taken from `hackathon-ecc/` (excl. `node_modules` where applicable):

- Counts: skills `166` (`ls skills | wc -l`), agents `72`, rules `123` files,
  commands `87`, hooks `15` entries in `hooks/hooks.json` (15 event keys, 1
  each). (`ls hooks` shows 17 files: 15 hook scripts + `adapter.js` +
  `hooks.json`.)
- Trigger keys: `64` — `call-map-data.json` triggers 64; `skill-triggers@1.json`
  coverage `withTriggers: 64` (of 166 skills).
- Banned terms 0: `grep -rniE "claude|codex|anthropic|opus|sonnet|haiku|
  composer-2\.5"` over the built tree excl. `node_modules` = 0 lines.
- Grok pins (occurrences, `grep -rho`): `grok-4.7-high` x54;
  `cursor-grok-4.6-high-fast` x103; bare `grok-4.6-high`
  (`grep -rP "(?<!cursor-)grok-4\.6-high(?!-fast)"`) x0.
- Pip install lines: 42 total, 20 pinned (`==`) — matches the fix #26
  expectation (13 newly pinned lines among them; 20 pinned overall).
- `README_UPDATE_F26` x4 (orchestrate SKILL.md, pitch-deck-video SKILL.md
  step 7, readme-writer SKILL.md, commands/demo.md).
- `VARFONT_F26` x1 (design-inventory.md:166, variable-font exception row).
- ck: three corrected lines present in the built tree —
  `session-start.mjs:6–7` ("Injects ~1k tokens per session … (~170 lines)"),
  `:90` ("Load skill (always inject the full SKILL.md, ~170 lines,
  ~1k tokens/session)"), `skills/ck/SKILL.md:159` ("The hook injects ~1k
  tokens per session …"); `:129` kept as the untouched
  "Compact summary block (~100 tokens)" line, per `fix26/ck-note.md` #4.

## 6. Staged-change census (Nov 14 modifications) — PASS, with note

- `find new-skills round2-skills rewritten-skills new-rules -type f` with
  mtime 2026-11-14 lists 9 files. The 5 expected minor-fix files are among
  them, with mtimes 21:40–21:45:
  `fix25/callmap/generate_call_map.py` (21:40), staged `call-map.md` (21:41),
  `fix25/callmap/call-map-data.json` (21:41), `fix25/verify25.py` (21:45),
  `build.sh` (21:45).
- The other 8 Nov 14 staged files are timestamped 21:03–21:06, **before** the minor-fix edits, and are the
  earlier fix #26 main-work edits (§1 pip pins, §4 README/F-14 + VARFONT),
  not side effects of the minor fixes:
  `new-skills/orchestrate/SKILL.md`, `new-skills/orchestrate/references/
  design-inventory.md`, `new-skills/pitch-deck-video/SKILL.md`,
  `new-skills/pitch-deck-video/commands/demo.md`,
  `new-skills/pitch-deck-video/references/shots-reference.md`,
  `new-skills/pitch-deck-video/references/troubleshooting.md`,
  `new-skills/pitch-deck-video/template/scripts/tts.mjs`,
  `rewritten-skills/readme-writer/SKILL.md`.
- No other staged-source file carries a Nov 14 mtime. `fix25/callmap/
  wiring-list.md` is untouched since Nov 13 07:22. No git repo exists at the
  plugin root, so the census is by mtime, not by `git status`.
- Note: the 8 pre-minor-fix files are flagged here only for completeness;
  they are expected fix #26 work, not new issues.

## Overall verdict: CLEAN

All four minors (Sweep #34 MINOR 1, Sweep #34 MINOR 2, Audit #73 M1,
Audit #73 M2) are fixed as claimed, with every number re-derived above.
The regenerated call map is byte-identical staged vs built, the regen diff
is exactly the 128 flow-string lines with no churn, the rebuilt tree
passes the regression spot-check, and no unexpected staged file was
modified by the fixes. No new issues found.
