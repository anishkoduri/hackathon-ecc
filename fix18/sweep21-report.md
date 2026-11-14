# Sweep #21 — fix program #18 (hackathon-ecc), built-tree verification

**Verdict: NOT CLEAN** — one finding (item 3): 5 stale `1:30–1:50` demo-video length
references survive outside `pitch-deck-video`, contradicting the new under-2:10 regime.
Everything else verified clean. See §3 for the finding.

**Scope:** built tree `~/workspace/hackathon-plugin/hackathon-ecc/`, `node_modules/` excluded
everywhere. SPEC read first: `~/workspace/hackathon-plugin/fix18/SPEC.md`.
Every number below was re-derived by running the greps/commands shown; nothing was copied
from fix16/fix17 manifests without re-running (pin counts were then compared to the
fix16 MANIFEST baseline and match exactly).

---

## 1. Banned terms (fix #16 scrub) — 0

Command:
```
grep -rniE 'claude|codex|anthropic|opus|sonnet|haiku|composer-2\.5' --exclude-dir=node_modules skills agents commands rules hooks README.md
```
Result: **0 hits** (exit 0, empty output). Scope covers skills/agents/commands/rules/hooks/README.

## 2. Grok pins (fix #16) — unchanged, match fix16 MANIFEST exactly

| String | Occurrences | Lines |
|---|---:|---:|
| `grok-4.7-high` | 52 | 45 |
| `cursor-grok-4.6-high-fast` | 100 | 99 |

Commands: `grep -ro 'grok-4.7-high' --exclude-dir=node_modules . | wc -l` (52),
`grep -r 'grok-4.7-high' --exclude-dir=node_modules . | wc -l` (45), same pair for
`cursor-grok-4.6-high-fast` (100 / 99). Fix16 MANIFEST §(line 29–31) baseline is
identical: 45 lines / 52 occurrences and 99 lines / 100 occurrences. Delta 0.

- Bare `grok-4.6-high-fast` (not preceded by `cursor-`):
  `grep -rP '(?<!cursor-)grok-4\.6-high-fast' --exclude-dir=node_modules . | wc -l` → **0**
- Bracket syntax `grok-4.7[`: `grep -r 'grok-4\.7\[' --exclude-dir=node_modules . | wc -l` → **0**
- `effort=`: `grep -r 'effort=' --exclude-dir=node_modules . | wc -l` → **0**
- Per-vendor key `reasoning_effort` (separate count): **2 occurrences / 2 lines**
  - `rules/common-performance.mdc:30` — "Grok takes per-vendor `reasoning_effort`, which Cursor does not expose in a pin."
  - `skills/orchestrate/SKILL.md:160` — same rule in the fallback pin paragraph.

`grok-4.7-high` appears in 20 files (incl. `agents/deep-reasoner.md`, `agents/ecc-architect.md`,
`commands/gan-build.md`, `commands/model-route.md`); `cursor-grok-4.6-high-fast` in 84 files.

## 3. Old time regime — FINDING: `1:30–1:50` survives in 5 places

| String | Hits |
|---|---:|
| `1:30–1:50` (en dash) | **5 — see below** |
| `1:30-1:50` (hyphen) | 0 |
| `2:00 cap` | 0 |
| `90–110 seconds` / `90-110` | 0 / 0 |

The 5 `1:30–1:50` hits (all state the demo-video length as 1:30–1:50, i.e. the
pre-F6 regime F6 replaces):

1. `rules/hackathon-mode.mdc:48` — "the demo video is 1:30–1:50" in the **canonical**
   length statement ("Demo lengths (canonical — this is the one place that says which
   length governs what)").
2. `skills/hackathon-scope/SKILL.md:17` — "the demo video is 1:30–1:50".
3. `skills/hackathon-pitch/SKILL.md:32` — "not the demo video (1:30–1:50, pitch-deck-video / /demo)".
4. `skills/hackathon-pitch/assets/pitch-script-template.md:79` — "Video (demo video, 1:30–1:50)".
5. `README.md:44` — "`/demo` — generate a narrated 1:30–1:50 product demo video of the app".

Why this matters: `commands/demo.md` now says "under 2:10" (item 4) and
`skills/pitch-deck-video/SKILL.md:101` says the video is under 2:10, so the README
advertises a different length than the command delivers, and hackathon-mode's
"canonical" statement now contradicts the skill it claims to govern. Fix #18's SPEC
§6 lists only pitch-deck-video files to change, so these cross-references were never
in scope for the implementation — the sweep flags them as a follow-up, not as a
fix18 implementation miss inside its own files.

Deliberate 90-second quota examples — exactly the three expected, all confirmed:

- `skills/pitch-deck-video/SKILL.md:420` — "A 90-second demo narration is about …"
  (voice character-count guidance)
- `skills/pitch-deck-video/SKILL.md:529` — "A 90-second demo narration is about 1,300 characters, so …"
- `skills/pitch-deck-video/references/shots-reference.md:242` — "A 90-second demo is about …"
  (voice quota)

Non-quota `90` hits that are NOT findings: `shots-reference.md:62–63,113` and
`record.mjs` are `ms: 900` timeouts; `troubleshooting.md:193` ("A ~90 s take renders
in ~40 s") is a render-time note, not a length quota; `SKILL.md:101` ("the pitch
storyboard is <90s") is the pitch storyboard, explicitly distinguished from the video.

## 4. Fix #18 anchors — all present, exact counts

| Anchor | Location | Count |
|---|---|---:|
| `under 2:10 (130 seconds)` | `skills/pitch-deck-video/SKILL.md:101` | 1 |
| `Absolute max 2:30` | `skills/pitch-deck-video/SKILL.md:101` | 1 |
| `Write the time budget before writing the lines.` | `skills/pitch-deck-video/SKILL.md:102` | 1 |
| `3. **Edge**` (Edge beat) | `skills/pitch-deck-video/SKILL.md:137` | 1 |
| `features` array doc + `cuts` doc | `skills/pitch-deck-video/references/shots-reference.md:19–20` (table rows), `:36` (`## features / cuts`), examples `:41–42` | present |
| `stack?: string` | `skills/pitch-deck-video/template/src/scenes/Arch.tsx:10` (`type Node = { label: string; note: string; kind: 'in' \| 'llm' \| 'code' \| 'out'; stack?: string };`) | 1 |
| `SEED_THEME` | `skills/pitch-deck-video/template/scripts/qa.mjs:99` (defined; used `:101`) | 1 def |
| `process.exitCode = 1` | `skills/pitch-deck-video/template/scripts/qa.mjs:138` | 1 |
| `under 2:10` | `commands/demo.md:2` (description) and `:9` (body) | 2 |

Supporting: Edge shot exists in the seed — `template/shots.example.json:180`
(`"id": "edge"`), `:182` say line. `under 2:10` tree-wide: 8 occurrences.

Staged-vs-built diff: **0 content differences.**
- `diff -r ~/workspace/hackathon-plugin/new-skills/pitch-deck-video/ hackathon-ecc/skills/pitch-deck-video/`
  → only output: `Only in new-skills/pitch-deck-video/: commands` — a structural path
  difference (staged nests `commands/demo.md` under the skill dir; build.sh copies it
  to `commands/`). No file content differs.
- md5 MATCH for all 7 fix18 files: `SKILL.md` (f39bb12c081b7767108d139116a0ea46 both),
  `references/shots-reference.md`, `references/troubleshooting.md`,
  `template/shots.example.json`, `template/scripts/qa.mjs`,
  `template/src/scenes/Arch.tsx`, and `commands/demo.md`
  (61c32ce0deaf670d9d18d79943c642d7 both).

## 5. Fix #17 anchors intact — spot-check, all pass

- **E1 identical ×4.** `E1_RULE` from `fix17/fix17.py` (1724 chars) occurs exactly once in
  each of the four placements, and the extracted text md5 is identical in all four:
  `e9d2102572611fe7a6ba507b961013b2` — matches the fix17 baseline md5 exactly.
  - `skills/design-taste-frontend/SKILL.md:254`
  - `skills/orchestrate/SKILL.md:94`
  - `skills/orch-build-mvp/SKILL.md:42`
  - `skills/ui-ux-pro-max/SKILL.md:97`
  - `may invent` tree-wide: 0 (`grep -ri 'may invent' hackathon-ecc --exclude-dir=node_modules | wc -l`).
- **Sticker exceptions A+B present** (`skills/design-taste-frontend/references/hallmark/references/themes/sticker.md:88–91`):
  - Exception A — "Hand-drawn ink marks (fix #17, exception A). …"
  - Exception B — "Scroll rise-and-settle entrances (fix #17, exception B). …"
  - Motion line `:74` reads "nothing on scroll, except the scoped exception in 'Scoped exceptions' below (scroll rise-and-settle entrances as sticker motion)."
- **less-flat-ui treatments still 1..23** — `re.findall(r"^### (\d+)\. ", less-flat-ui/SKILL.md)`
  returns exactly `[1..23]`.
- **Canonical block verbatim ×1 in all 11 fix #15 files** (`CANONICAL` from `fix15/fix15.py`,
  `text.count(CANONICAL) == 1` for each):
  `design-taste-frontend/SKILL.md`, `ui-ux-pro-max/SKILL.md`, `less-flat-ui/SKILL.md`,
  `polish-pass/SKILL.md`, `design-taste-frontend/references/hallmark/references/hallmark-floor.md`,
  `make-interfaces-feel-better/SKILL.md`, `motion-foundations/SKILL.md`,
  `motion-patterns/SKILL.md`, `motion-advanced/SKILL.md`, `orchestrate/SKILL.md`,
  `orch-build-mvp/SKILL.md` — all count 1.

## 6. build.sh exception inventory re-derived — delta 0

- `md5sum build.sh` → `1a999d763e6ec1fb16985d346b106df0` (unchanged), **23,276 lines** (unchanged).
- Fresh banned-term line count: `grep -c -iE 'claude|codex|anthropic|opus|sonnet|haiku|composer-2\.5' build.sh` → **798 lines**.
- Re-derivation: parsed the full 796-row inventory table in `fix16/sweep18-report.md`
  (§Check 16, lines 196–~1004) and cross-checked its line-number set against a fresh
  `grep -in` of build.sh. Class counts from the table: **(a) OLD-side 389, (b) comment 52,
  (c1) NEW-side transient 355**; the table's line set + the two (c3) build-time `.claude/skills/`
  `cp` paths (`:265`, `:298`) equals the fresh 798-line set exactly — no missing, no extra
  lines. (c2) heredoc: 0.
  - `:265` `cp -r "$UIPRO_DIR/.claude/skills/ui-ux-pro-max" "$PLUGIN_DIR/skills/ui-ux-pro-max"`
  - `:298` `cp -r "$SKILL_SRC/flecto-shade/.claude/skills/hackathon-pitch" "$PLUGIN_DIR/skills/hackathon-pitch"`
- Per-term line counts (fresh grep): `claude` 701, `codex` 103, `anthropic` 5, `opus` 22,
  `sonnet` 23, `haiku` 13, `composer-2.5` 0 — identical to the sweep18 baseline.
- **Delta vs sweep #18 baseline (798 = 389/52/355/0/2): 0.** Fix18 made no build.sh change,
  as required; the byte-identical md5 makes the category inventory necessarily unchanged.

## 7. Counts

| Inventory | Count | Command |
|---|---:|---|
| skills | **166** | `ls skills \| wc -l` |
| agents | **72** | `ls agents \| wc -l` |
| rules | **123** | `ls rules \| wc -l` |
| commands | **87** | `ls commands \| wc -l` |
| hooks | **15** | `python3 -c "len(json.load(open('hooks/hooks.json'))['hooks'])"` → 15 event keys |

Hooks detail: `hooks/` holds 17 files — 16 `.js` (15 hook scripts + `adapter.js`) plus
`hooks.json`. The 15 events: sessionStart, sessionEnd, beforeShellExecution,
afterShellExecution, afterFileEdit, beforeMCPExecution, afterMCPExecution, beforeReadFile,
beforeSubmitPrompt, subagentStart, subagentStop, beforeTabFileRead, afterTabFileEdit,
preCompact, stop. `du -sh hackathon-ecc/` = 56M.

## Commands used (full list)

```
grep -rniE 'claude|codex|anthropic|opus|sonnet|haiku|composer-2\.5' --exclude-dir=node_modules skills agents commands rules hooks README.md
grep -ro 'grok-4.7-high' --exclude-dir=node_modules . | wc -l ; grep -r 'grok-4.7-high' --exclude-dir=node_modules . | wc -l
grep -ro 'cursor-grok-4.6-high-fast' --exclude-dir=node_modules . | wc -l ; grep -r 'cursor-grok-4.6-high-fast' --exclude-dir=node_modules . | wc -l
grep -rP '(?<!cursor-)grok-4\.6-high-fast' --exclude-dir=node_modules . | wc -l
grep -r 'grok-4\.7\[' --exclude-dir=node_modules . | wc -l
grep -r 'effort=' --exclude-dir=node_modules . | wc -l
grep -ro 'reasoning_effort' --exclude-dir=node_modules . | wc -l ; grep -r 'reasoning_effort' --exclude-dir=node_modules . | wc -l
grep -rn '1:30–1:50' --exclude-dir=node_modules . ; grep -rn '2:00 cap' --exclude-dir=node_modules .
grep -rn '90–110 seconds' --exclude-dir=node_modules . ; grep -rn '90' skills/pitch-deck-video/
grep -rn '1:30-1:50' / '90-110' --exclude-dir=node_modules . | wc -l
grep -c 'under 2:10 (130 seconds)' / 'Absolute max 2:30' / 'Write the time budget before writing the lines\.' /
  '3\. \*\*Edge\*\*' skills/pitch-deck-video/SKILL.md
grep -n 'features' / '"cuts"' / 'cuts' skills/pitch-deck-video/references/shots-reference.md
grep -n 'stack?: string' skills/pitch-deck-video/template/src/scenes/Arch.tsx
grep -n 'SEED_THEME' / 'process.exitCode = 1' skills/pitch-deck-video/template/scripts/qa.mjs
grep -n 'under 2:10' commands/demo.md ; grep -rn 'under 2:10' --exclude-dir=node_modules .
grep -rn 'Absolute max 2:30' --exclude-dir=node_modules .
diff -r new-skills/pitch-deck-video/ hackathon-ecc/skills/pitch-deck-video/
diff -q new-skills/pitch-deck-video/commands/demo.md hackathon-ecc/commands/demo.md
md5sum new-skills/pitch-deck-video/{SKILL.md,references/shots-reference.md,references/troubleshooting.md,
  template/shots.example.json,template/scripts/qa.mjs,template/src/scenes/Arch.tsx,commands/demo.md}
  + built counterparts
python3 (E1_RULE md5 ×4 from fix17/fix17.py; CANONICAL count ×11 from fix15/fix15.py;
  less-flat-ui treatment numbers; sticker exceptions; build.sh inventory table parse +
  fresh-grep cross-check; hooks.json parse)
grep -ri 'may invent' hackathon-ecc --exclude-dir=node_modules | wc -l
grep -c -iE 'claude|codex|anthropic|opus|sonnet|haiku|composer-2\.5' build.sh
md5sum build.sh ; wc -l build.sh ; ls skills|wc -l ; ls agents|wc -l ; ls rules|wc -l ; ls commands|wc -l
```
