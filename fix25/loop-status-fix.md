# Fix #25 — dry-run #40 Leg 5 MINOR: `/loop-status` has no command file

- **Date:** 2026-11-13. Worker: loop-status fix worker (fix #25 Phase 3b).
- **Finding (dry-run #40 §5.1):** `commands/epic-unblock.md:20–22` declares
  `/loop-status` a "Compatibility alias" and `skills/ecc-recipes/SKILL.md:81,142`
  tells the agent to "watch with `loop-status`" / "monitor `loop-status`" —
  but no `commands/loop-status.md` exists anywhere in the built tree, so
  `/loop-status` resolves to nothing in Cursor. The dry-run's Leg 5 runner
  recorded it as `BROKEN cmd:epic-unblock -- unresolvable dispatch:
  command:/loop-status` (`fix25/dryrun40/dryrun40-leg5-output.txt:7,49–50`).

## Decision: option (b) — correct the references; do NOT ship a loop-status command file

Evidence, all read from the files:

1. **The file was deliberately deleted, not lost.** `fix16/fix16.py:210–211`
   (`DELETE_FILES`) lists `"commands/loop-status.md"` with the comment
   "Sessions cluster: no Cursor equivalent for Claude transcript scanning
   (loop-status) — see targeted decisions in CHANGES.md", and
   `fix16/CHANGES.md` D16 records: "`commands/santa-loop.md`, the five
   `commands/multi-*.md`, `commands/loop-status.md` DELETED (CLI-only)".
   The upstream body (`/tmp/ecc-dev-install/.cursor/commands/loop-status.md`)
   runs `npx --package ecc-universal ecc loop-status --json`, scanning
   Claude transcript JSONL under `~/.claude/projects/**` — a Claude-only
   tool with no verified Cursor equivalent. Re-creating the file would
   reverse a recorded fix #16 decision, which SPEC §6 forbids re-litigating.
   (build.sh still patches the file at :2371, :11821, :21817 — those patches
   run before the fix16 deletion step at build.sh:23217, so they still apply
   to the upstream copy at patch time.)
2. **No real command exists to dispatch to.** Dispatching `/loop-status` to
   `/epic-unblock` (the "real command" the alias line names) is semantically
   wrong: loop-status monitors an autonomous loop; epic-unblock sweeps
   blocked epic issues and reopens unblocked ones. No shipped command
   performs loop monitoring — `commands/loop-start.md:24` only prints the
   commands to start and monitor a loop, and the monitor command it would
   print IS loop-status. There is nothing truthful to reword the references
   to.
3. **The alias convention itself confirms the line is the defect.** Every
   other epic-* "Compatibility aliases" entry names a command that ships,
   all verified present in `hackathon-ecc/commands/`: epic-claim →
   orch-add-feature, orch-change-feature; epic-decompose → plan, prp-plan;
   epic-publish → pr, prp-pr; epic-review → review-pr, code-review;
   epic-sync → projects; epic-validate → quality-gate. Only `/loop-status`
   dangles.
4. **Precedent:** fix16 D15 — "References belonging to a removed feature
   went with the feature." The three references go with the removed
   loop-status feature. The `loop-*` family itself stays — `loop-start`
   ships — only the monitor half, which names the removed command, is
   dropped.

## Fix (in `fix25/fix25.py`, new section before `# --- main`; upstream files have no staged source, so the build-time patch script is the sanctioned home)

| File (built tree) | Old text | New text |
|---|---|---|
| `commands/epic-unblock.md:20–22` | `4. Updates labels, comments, and local snapshots.\n\nCompatibility aliases:\n\n- \`/loop-status\`` (file ends here, 22 lines) | `4. Updates labels, comments, and local snapshots.` (file now ends at step 4; whole alias section removed — an empty "Compatibility aliases:" header would be noise, and no shipped command is a genuine alias for epic-unblock) |
| `skills/ecc-recipes/SKILL.md:81` (family table) | `` \| `loop-*` \| managed autonomous loop and monitor \| `loop-start <pattern>` then watch with `loop-status` \| `` | `` \| `loop-*` \| managed autonomous loop \| `loop-start <pattern>` \| `` (meaning trimmed too: with no monitor command shipped, "and monitor" is no longer true) |
| `skills/ecc-recipes/SKILL.md:142` (Match example) | `` `loop-start rfc-dag --mode safe` then monitor `loop-status`; STOP when all units `` | `` `loop-start rfc-dag --mode safe`; STOP when all units `` |

No `build.sh` edit: `build.sh` is untouched (md5 `f19483f50e89998f8b9dc052ed5d5fae`,
24,079 lines, diff vs `build.sh.before-fix23` +305/−0 intact). The
`build.sh` audit/audit2 old-side anchors containing "monitor `loop-status`"
(:5593, :12815) match UPSTREAM text at their run time (they run before
fix16/fix25), so this later edit cannot break them. No verifier asserts any
of the three strings (grep over `verify*.py`, `fix24/`, `fix25/`).

## Rebuild state (build run 5, log `fix25/build-log-run5.txt`)

- `bash build.sh > fix25/build-log-run5.txt 2>&1` — **exit 0**.
- fix16: **ERRORS: 0**, NOTES: 38, CHANGES: 649, REMOVALS: 88 (identical to
  run 4), TOTAL BANNED-TERM HITS: 0.
- fix25: **17 change(s)** (14 prior + these 3), "fix25: OK", Errors (0)
  (`fix25/fix25-patch-log.md`).
- STEP 5 counts: skills **166**, agents **72**, rules **123**, commands
  **87**, hooks **15** — **command count unchanged (87, not 88)**.
- Call-map regeneration: `python3 fix25/callmap/generate_call_map.py` —
  **exit 0**, counts assert **166/72/123/87/15/64**, corpus 1,710 files.
  Staged `new-skills/orchestrate/references/call-map.md` is byte-identical
  to the pre-fix map, and identical to the built-tree copy, so **no second
  build was needed**.

## Built-tree confirmation (read from `hackathon-ecc/` after run 5)

- `grep -rn "loop-status" hackathon-ecc/` → **0 hits** (also 0 across
  `new-skills/`, `round2-skills/`, `rewritten-skills/`, `new-rules/`, and
  `fix25/callmap/call-map-data.json`).
- `commands/epic-unblock.md` now ends at step 4 (19 lines), no alias section.
- `skills/ecc-recipes/SKILL.md:81` reads
  `` | `loop-*` | managed autonomous loop | `loop-start <pattern>` | ``.
- `skills/ecc-recipes/SKILL.md:142` reads
  `` `loop-start rfc-dag --mode safe`; STOP when all units ``.
- `ls hackathon-ecc/commands/ | wc -l` → **87**.

## What I could not verify

- **The exact `call-map-data.json` delta.** The regeneration changed the
  data sidecar (`diff` reported a difference) while `call-map.md` is
  byte-identical to the pre-fix map — but I deleted the pre-regeneration
  copy of the data file before diffing it, so the precise delta is
  unverified and is NOT asserted here. What is verified instead: the
  generator is deterministic (two consecutive post-fix runs produce
  byte-identical outputs, md5 `1e8bccb869e9c45687b111cb0b949d46`), counts
  assert, the new data file has 0 "loop-status" hits, and the
  `loop-start` / `epic-unblock` / `ecc-recipes` entries in it are
  consistent with the fixed tree (epic-unblock still called via
  ecc-recipes STRONG + orchestrate STRONG + struct-command; loop-start
  called via loop-design-check STRONG + struct-command). The verify25
  worker can re-derive the delta if it needs it; the durable artifact
  (`call-map.md`) did not change.

## Not done (out of scope, for the verify25 worker)

- No audit / sweep / dry-run / verify run (verify25 asserts this fix).
- No bundle, no commit, no push. `fix11/fix11-stage.py` never run.
- Nothing in `pitch-deck-video` templates, any `verify*.py`, or
  `design-inventory.md` was touched.
