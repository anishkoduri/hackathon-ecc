# Audit #73 — fix #26 (hackathon-ecc Cursor plugin)

**Auditor:** Audit #73 (subagent, read-only). **Date:** Nov 14, 2026.
**Scope:** fix #26 SPEC §1–§8 placements, full-tree regression, the one
authorized verifier edit, supply-chain spot-check.
**Method:** every claim below was re-checked by re-reading the files and
re-running the greps — the fix26 notes, the task brief, and the fix25
manifest were treated as claims to verify, not as evidence. No file was
edited, build.sh was not run, nothing was committed, bundled, or pushed.
**Baseline verified:** build.sh 24,088 lines, md5
`e05bdc66599b694398e11f0d00dfdafd` (post-fix-25 baseline 24,079 lines,
md5 `f19483f50e89998f8b9dc052ed5d5fae`). Built tree is run 3
(`fix26/build-log-run3.txt`: `fix26: 16 change(s)`, `fix26: OK`,
counts 166/72/123/87/15). Runs 1–2 failed on environment faults
(run 1: `/tmp/ecc-repo-clean/.git/index.lock` "Out of diskspace" —
tmpfs; run 2: git checkout aborted on untracked files); run 3 is the
live tree. Those failures are environment, not plugin, findings.

**Concurrent rebuild during this audit (read first):** while this
audit was running, the coordinator started build run 4 (21:41 UTC,
after regenerating the staged call map a second time at 21:41:28)
and it completed at ~21:43:57 (`fix26: 16 change(s)`, `fix26: OK`,
counts 166/72/123/87/15, "build complete"). The run-4 build
overwrote the run-3 tree mid-audit. Every built-tree claim in this
report was therefore verified TWICE — once against the run-3 tree
and once again against the completed run-4 tree — and every claim
reproduced exactly (see "Re-verification on the run-4 tree" below).
The only audit observation that changed between the two trees is
the verify25 re-run tail (see §9): a verify25 run executed while
run 4 was mid-build produced a spurious verify13h failure, explained
below. The audit's verdict is on the final (run-4) tree.

## Verdict

**2 MINOR findings, 0 BLOCKING.** Both minors are stale-comment
inaccuracies of the same class fix #26 §3 was created to close; neither
affects any check, count, gate, or shipped behavior.

- **M1 — `fix25/verify25.py:22` docstring still says `+305/-0`.**
  The §3 authorized edit updated the assertion (`:176–177`, now
  `+314/-0`) but not the header docstring describing check 1, which
  still reads "diff vs build.sh.before-fix23 additions only (+305/-0)".
  The assertion is correct (recomputed diff is exactly 314 additions /
  0 deletions — see §9); the docstring now misstates the invariant it
  documents. One-word fix (`+305` → `+314`), or a parent adjudication
  that the docstring records the fix #25 baseline and stays. Note the
  same docstring line also still cites the fix #25 fingerprint
  (24,079 lines, md5 `f19483f5…`), which the fingerprint check itself
  still asserts — so the docstring is consistent with the (now
  expected-failing) fingerprint check and inconsistent only with the
  diff assertion.
- **M2 — `build.sh:24070–24075` new fix #26 comment misdescribes
  `fix26/fix26.py`.** The header says "(ck cost lines)" only, but the
  script's 13 of 16 changes are the §1 pip pins; and `:24075` says
  "§1 pip pins land in the same script (placeholder section, pip
  worker)" — there is no placeholder section in `fix26.py` (grep for
  `placeholder` in `fix26/fix26.py`: 0 hits). The §1 section is fully
  implemented (`fix26.py:98`, P-01–P-13). The comment reads as if
  written when the pip section was still a placeholder and never
  updated — the exact staleness class §3 just fixed for the fix25
  comment. Suggested reword: header "(ck cost lines + §1 pip pins)",
  `:24075` → "§1 pip pins (13 upstream lines, P-01–P-13) land in the
  same script." Note: fixing this comment is a pure reword of
  lines that are themselves additions vs before-fix23, so the
  count should stay +314/-0 — but the coordinator must re-verify
  the tail after any reword rather than assume it, and any M2 fix
  also needs a rebuild + re-run of the audit's built-tree checks
  if it lands after this report (the tree would be unchanged, but
  the diff tail is a build.sh property, not a tree property).

## §1 Pip pinning — PASS

- Built-tree `grep -rn "pip install"` (excl. `node_modules`): **42
  lines, 20 pinned (`==`), 22 unpinned** — full listing saved at
  `fix26/audit73-pip-grep.txt` / `audit73-pip-unpinned.txt`. The 20
  pinned lines are exactly the 20 category-(a) lines in
  `pip-pinning.md` (7 staged + 13 via `fix26.py`); **zero unpinned
  category-(a) lines remain**.
- All 22 unpinned lines re-classified independently against the
  `pip-pinning.md` 42-line table — every one matches its claimed
  class, none is actually (a):
  - (b) prose/mention, 8: `skills/bengali-nlp/SKILL.md:87, :139, :207`
    (inline code comments); `skills/python-patterns/SKILL.md:546`
    (comment); `skills/pitch-deck-video/template/scripts/tts.mjs:180`
    (runtime error string — the (b) line deliberately left);
    `agents/ecc-django-build-resolver.md:229` (prose, no package);
    `scripts/hooks/insaits-security-monitor.py:205` (log warning);
    `scripts/hooks/insaits-security-wrapper.js:78` (stderr message).
  - (c) `-r requirements.txt`, 6: `skills/django-verification/
    SKILL.md:428`; `skills/generating-python-installer/SKILL.md:150`;
    `skills/windows-desktop-e2e/SKILL.md:610`;
    `agents/ecc-django-build-resolver.md:85, :94`;
    `agents/ecc-opensource-packager.md:137`. Confirmed: no
    `requirements.txt` exists anywhere in the built tree (`find`
    returns none), so there is nothing in the plugin to pin here —
    the note's claim holds.
  - (d) policy/table/placeholder, 8: `agents/ecc-agent-evaluator.md:33`
    (forbidden-command list, bare `pip install`);
    `agents/ecc-django-build-resolver.md:77` (placeholder `X`), `:79`
    (table; `--upgrade pip` + a (c) line), `:182` (table cell
    `psycopg2-binary` fix-pattern example);
    `manifests/pi-core.json:25, :223, :297, :407` (policy text,
    `<dep>` placeholder, bare mentions).
- Pin spot-checks against the `pip-patches.md` specs (all 13 present
  in the built tree with the specified versions): django-verification
  `:429` (9 packages), frontend-slides `:324` Pillow==13.0.0,
  extract-pptx.py `:9` python-pptx==1.0.2, django-celery `:26`
  celery[redis]==5.7.0 + results==2.6.0 + beat==2.9.0 and `:411`
  flower==2.2.0, generating-python-installer `:627`
  opencv-python-headless==5.0.0.93, plankton-code-quality `:81`
  uv==0.13.8 ruff==0.17.5, windows-desktop-e2e `:55, :651, :755, :880`,
  gateguard-fact-force.js `:19` gateguard-ai==0.6.2,
  insaits-security-monitor.py `:13` insa-its==4.9.10. Staged 7
  confirmed in `new-skills/pitch-deck-video/` (SKILL.md `:843` all
  three piper-tts mentions pinned, shots-reference `:247`,
  troubleshooting `:212, :232, :233`, tts.mjs `:134, :135`).
- Version reality spot-check vs PyPI JSON API (2026-11-14):
  ruff 0.17.5, Pillow 13.0.0, piper-tts 1.8.0, yt-dlp 2026.10.26,
  opencv-python-headless 5.0.0.93 all equal `info.version` (latest).
  pytest-timeout: `info.version` is 2.4.0 but the releases list
  contains stable 2.5.0 — confirms the note's claim; the
  `==2.5.0` pin is what pip installs today.
- The 20-vs-17 Audit #37 discrepancy is honestly reported in
  `pip-pinning.md` (no audit37 report file exists to recover the
  enumeration; hypothesis: tts.mjs 2-line comment counted once +
  2 hook header lines excluded = 17). All 20 are pinned anyway; no
  line is owed for lack of a version.
- Flag carried forward (not a finding of this audit — it belongs to
  verify26): `pip-pinning.md` flag 1 notes `fix24/verify24.py:389`
  asserts the now-pinned yt-dlp line, so verify24 E-5 will fail
  until codified in verify26. No verifier was edited in this fix to
  address it, correctly per the §3 authorization scope.

## §2 F-14 — PASS

- Anchor `README_UPDATE_F26` present in all 4 edited files, staged
  and built, at the noted lines: pitch-deck-video SKILL.md `:217`
  (step 7 heading), `commands/demo.md` `:9`, orchestrate SKILL.md
  `:101` (step 6 clause), readme-writer SKILL.md `:95` (Step 2).
  (Built demo.md lives at `hackathon-ecc/commands/demo.md`, not under
  `skills/pitch-deck-video/commands/` — the f14-note's "commands/
  demo.md" is relative to the staged skill dir; verified at the built
  path.)
- Step 7 content re-read in full (built SKILL.md `:217–270`): the
  five rules match the f14-note mechanism (a) exactly — (1) ledger
  record first (`demo video: <app-name>-video/out/demo.mp4` in
  `.hackathon/run-ledger.md`); (2) first-match-wins idempotent README
  edit, rules a–d (already links → nothing; placeholder → replace;
  badge-button block → add Demo Video button + comment; else insert
  `## Demo video` after the title block / at top); (3) no README →
  write none, report the path; (4) re-cuts are a no-op; (5) final
  report not rewritten. The four files' wordings are mutually
  consistent (orchestrate step 6: "linked into the README by that
  run … not by re-running this step"; readme-writer: "readme-writer
  is not re-run just for the video link").
- No new gate: step 7 states "no new gate, no approval" and "/demo
  still runs only when the user invokes it explicitly". /demo gates
  intact: `DEMOGATE_O4_F22` at orchestrate `:99` ("NEVER dispatched
  by this pipeline … ONLY when the user invokes `/demo` explicitly"),
  `DEMOGATE_O9_F22` at orchestrate `:101` ("it is never part of this
  order"). No orchestrate dispatch of /demo was added; no approval
  gate was added to the first build.

## §3 Comment fix — PASS (modulo M1, which is the verifier side)

- `build.sh:24061–24067`, 7 lines → 7 lines, text matches the
  `comment-fix.md` "After" block exactly (verified by direct read):
  header now "(§1 wires, §2 inventory, §4 S1/benchmark)"; body names
  the ck + /prp-commit wires, the orch-* inventory-bypass close, S1
  80 → 89, the §4(d) browser-qa line, and the loop-status removals.
- Accuracy of the new comment checked against `fix25/fix25.py`:
  ck wire (`:48–49, :124–204`), /prp-commit wire (`:207–217`),
  INVENTORY_F23 patches (`:240, :256, :261`), S1 header
  (`:117, :120`), browser-qa benchmark line (`:60, :264–266`),
  loop-status (`:64–65`). The comment correctly names only the
  script's own wires (W3/W4 are staged orchestrate edits, not
  fix25.py — the comment-fix.md accuracy note holds).
- Net line effect 0 for this edit; the +9 build.sh growth (24,079 →
  24,088) is entirely the new fix26 block (`:24069–24077`: blank +
  7 comment lines + invocation line), consistent with the diff
  tail moving +305 → +314 (see §9).

## §4 Variable-font exception — PASS

- Inventory §11 "Scoped exceptions" present in the built tree
  (`skills/orchestrate/references/design-inventory.md:164–166`,
  staged file identical, line 166): `VARFONT_F26` records Hanken
  Grotesk (34,704 B, variable wght 100–900) + JetBrains Mono
  (30,376 B, variable wght 400–500) as the exception, Instrument
  Serif (21,032 B) as staying static weight 400 only, scope
  "Template only", reason (single controlled Chromium, fixed video
  output), and "App UI fonts stay static-only".
- Sizes verified against the staged font files (34,704 / 21,032 /
  30,376 B) and the weights against template `src/fonts.ts:11–15`
  (Hanken `'100 900'`, Instrument `'400'`, JetBrains `'400 500'`)
  and its header comments (`:11–15` variable/static split). The
  note's figures match the files exactly.
- No font file, loader, or rule text was changed (recording only);
  the static-only rule text in pitch-deck-video SKILL.md is untouched.

## §5 B6 trigger router — PASS (DOCUMENTATION-ONLY confirmed)

- Call map `:38` (staged and built, 622 lines each, byte-identical
  after a concurrent regeneration — see note below) records
  "fix #26: DOCUMENTATION-ONLY" with the consumer chain and the
  upstream-only citation. The generator template was also updated
  (`fix25/callmap/generate_call_map.py:753–761` now emits the
  DOCUMENTATION-ONLY wording), closing the b6-note's follow-up item.
- Grep evidence spot-checked in the built tree, all confirmed:
  - 64 trigger keys in `manifests/context-packs/skill-triggers@1.json`,
    all `skill:`-prefixed, **0 unresolved** (every name resolves to
    `skills/<name>/`).
  - `fix25/callmap/call-map-data.json`: `"trigger_only": []`.
  - `scripts/lib/context-pack-registry.js:12` defines
    `TRIGGERS_PATH`; `loadSkillTriggers` at `:128–142`.
  - `scripts/lib/context-selection.js:4` requires the registry;
    calls it at `:315` and `:340`.
  - `context-selection.js` is required only by
    `scripts/lib/context-profile-commands.js` and
    `scripts/lib/context-routing-index.js`.
  - `context-profile-commands.js` has **no requirers** anywhere
    (js/mjs/md/json, excl. node_modules).
  - `grep -rn "context-" hooks/*.js` → **0 hits**; no `hooks/*.js`
    file requires anything under `scripts/lib/` (only `./adapter`).
  - `hooks/hooks.json` `sessionStart` runs only
    `node hooks/session-start.js`; no hook registration names
    `context-routing-index` or `context-prompt-suggestions`.
  - `scripts/hooks/context-prompt-suggestions.js:4–10` header
    confirms upstream-only ("not wired in this Cursor plugin —
    Cursor has no UserPromptSubmit event").
  - No `package.json`/bin entry point or test file references
    `context-selection`, `context-routing-index`, or
    `loadSkillTriggers` (verified by the requirer greps above).
- Observation (note wording, not a plugin finding): b6-note.md §(4)
  says "The only references to `context-prompt-suggestions` /
  `context-routing-index` by name anywhere are the call-map B6 bullet
  itself and `context-profile-commands.js:94`." That sentence
  over-narrows: the string `context-routing-index` also occurs at
  `scripts/hooks/context-prompt-suggestions.js:53` and
  `scripts/hooks/context-routing-index.js:16` (both requiring
  `../lib/context-routing-index`) and at
  `scripts/lib/context-routing-index.js:13` (its own schema string).
  The note's §(3) already lists those consumers correctly, and the
  load-bearing conclusion — no live consumer reachable from
  `hooks/*.js` — is verified true by my own greps. The disposition
  stands; the sentence is sloppy, the evidence is complete.
- Note on timing: during this audit the staged call map was
  regenerated twice by concurrent coordinator work (21:36:31 and
  21:41:28 UTC). My first staged-vs-built diff caught a `:90`
  `code-tour` row-ordering difference from the first regeneration;
  end state (after the second regeneration + run 4): staged and
  built call-map.md are byte-identical (md5
  `8d4c10efefbd844603e6743ed9893718`, 622 lines each), B6 `:38`
  unchanged. No audit conclusion depends on the pre-regeneration
  ordering; the md5 movement between regenerations is generator
  ordering noise (see "Re-verification on the run-4 tree").

## §6 Dim 7 — PASS (recorded as OWED, not a pass)

- `~/workspace/cold-start-render/campus-eats/` contains only
  `.hallmark/log.json`, `.hallmark/salt`,
  `.taste-skill/history.json`, `.taste-skill/layout-history.json`,
  `docs/design-tokens.md` (v1-era tokens file). No `index.html`,
  CSS, JS, assets, or app frame. Nothing browser-qa could run the
  ALIGN_F23 matrix against. No file under `campus-eats/` is newer
  than the fix25 manifest — no Campus Eats render was built in
  this fix.
- Benchmark file untouched as a record: built
  `design-benchmark-v5.md` is 178 lines, byte-identical to the
  staged file; v5 figures 61 literal / 60 stricter (`:40, :42`);
  Dim 7 `:147` reads "NONE RECORDED (no v5 figure)", verdict
  "browser-qa live verdict (owed, never claimed statically)". §3
  states a dimension that cannot be scored "records it as a gap
  (owed), not as a pass". No benchmark figure was edited.
- `dim7-note.md`'s §2 citations check out against the files
  (benchmark §1 caveat + §2 Dim 7; dry-run #40 report §2.3 "6 of 7
  dimensions pass statically; dimension 7 is OWED"; fix25 MANIFEST
  §6). The Home Run 52-measurement run is correctly not counted
  toward Dim 7.

## §7 R1/R4 — PASS (recorded as OWED, not verified)

Verified against the actual Home Run render files in
`~/workspace/cold-start-render/home-run/` — the r1r4-note's claims
hold, including the ones that cut against verification:

- **R1 iris-opens: applied in Home Run, but NOT as defined (#67
  hero → picks transition).** `index.html:179–180`
  (`iris-wrap` + `iris-disc` in the trip view);
  `styles.css:426–446` (`.iris-disc` hairline ring,
  `@keyframes iris-ring` scale 0.2 → 1.6, 0.7s;
  `.iris-open .code-panel` `@keyframes iris-open` clip-path
  `circle(0% …)` → `circle(150% …)`, 0.6s — note's cited range
  `:425–446` is off by one at the start, `.iris-wrap` is `:426`;
  immaterial); `app.js:190–192` (`enterTrip()` adds `iris-open`
  120 ms after entering the trip view, once per trip, skipped under
  reduced motion); `app.js:384, :392–393` reset;
  `docs/design-tokens.md:199–202, :245, :342` records the moment.
  No hero → picks transition exists in Home Run: grep for
  `picks|ramen` across `index.html`, `app.js`, `styles.css`,
  `docs/design-tokens.md` returns nothing — no picks section, no
  ramen photo. Dry-run #40 report `:43` corroborates the disc's
  live existence (assertion (e) CLIP: `.iris-disc` beyond the phone
  frame in 8 measurements, bleed declared).
- **R4 hero loop: NOT applied anywhere in Home Run.** Grep for
  `loop|steam|cycle|wisp|marquee|carousel|ticker|setInterval`
  across `index.html`, `styles.css`, `app.js`: **zero hits**.
  `loop` in `docs/design-tokens.md`: **0 hits**. The only repeating
  machinery is one-shot: counter-roll (`app.js:180–186`,
  `requestAnimationFrame`, rolls once on entry then rests) and the
  wrong-code shake (`app.js:230–236`, 650 ms reset). The hero
  (`index.html:50–76`) is a static statement + subline + live-run
  card + sort keys + feed list; nothing cycles.
- The SPEC §7 premise is correctly refused: dry-run #40's "hero loop
  + iris-opens applied" is the Campus Eats benchmark re-trace
  (`dryrun40-report.md:64`, rows #67/#68 — paper additions under
  current rules), while the 17/17 §6 assertions are Home Run
  alignment assertions that say nothing about moment/loop
  application. Conflating them would have been a false verification.
  R1 OWED as defined (with adjacent trip-reveal evidence recorded),
  R4 OWED as defined (no adjacent evidence). No render file was
  modified; no benchmark figure edited.

## §8 ck wire KEEP — PASS

- Built-tree corrections, all three landed at the noted lines:
  `skills/ck/hooks/session-start.mjs:6–7` now "Injects ~1k tokens per
  session (not ~2,500 like v1): the full SKILL.md (~170 lines) plus
  the compact summary below."; `:90` now "Load skill (always inject
  the full SKILL.md, ~170 lines, ~1k tokens/session)";
  `skills/ck/SKILL.md:159` now "The hook injects ~1k tokens per
  session (the full SKILL.md plus the compact 5-line summary)."
- `session-start.mjs:129` "Compact summary block (~100 tokens)"
  correctly LEFT unchanged.
- No other stale cost claims in `skills/ck/`: grep for
  `100 tokens|50 lines|tokens per session` returns exactly the three
  corrected lines plus `:129`.
- Measurement reconciliation: `skills/ck/SKILL.md` is now 169 lines /
  830 words / 6,403 chars vs the ck-note's run-5 figures 169 / 825 /
  6,377. The delta (+5 words, +26 chars) is exactly the fix26
  SKILL.md patch itself ("the full SKILL.md plus the " added inside
  the parenthetical). "~170 lines" stays accurate (169 lines). The
  wire itself is untouched: `hooks/session-start.js:79–81` still
  spawns `session-start.mjs` (15 s timeout, fail-soft), inheriting
  the `session:start` gate.
- `fix26-patch-log.md`: 16 changes, 0 errors — matches the build log
  (3 ck + 13 pip) and `fix26.py`'s own patch list.

## Full-tree regression — PASS

- Banned terms (claude/codex/anthropic/opus/sonnet/haiku/
  composer-2.5, case-insensitive, excl. node_modules): **0** in the
  built tree (independent grep; also build-log-run3: TOTAL
  BANNED-TERM HITS: 0).
- Grok pins only: `grok-4.7-high` ×54, `cursor-grok-4.6-high-fast`
  ×103, bare `grok-4.6-high-fast` ×0 — identical to the fix #25
  counts.
- Counts unchanged: 166 skills / 72 agents / 123 rules / 87 commands
  / 15 hooks; trigger keys 64. No new skill, command, rule, agent,
  hook, or trigger.
- Staged-change census (files modified Nov 14): exactly the 9
  expected files — orchestrate SKILL.md + call-map.md +
  design-inventory.md, pitch-deck-video SKILL.md + commands/demo.md
  + shots-reference.md + troubleshooting.md + tts.mjs,
  readme-writer SKILL.md. No unexpected staged edit.
- Staged-vs-built parity for the fix26 placements: pitch-deck-video
  SKILL.md, readme-writer SKILL.md, design-inventory.md,
  call-map.md are byte-identical staged vs built. orchestrate
  SKILL.md differs only at `:96, :261, :268` (pre-existing build-time
  agent-name → agent-path rewrites, e.g. `` `code-reviewer` `` →
  `` `code-reviewer` agent (`agents/ecc-code-reviewer.md`) ``) and
  demo.md only at `:13` (pre-existing narration-key prompt
  expansion) — none touches the fix26 placements (`:101` F-14
  clause and demo.md `:9` are identical in both).

## §9 The one authorized verifier edit — PASS except M1

- `fix25/verify25.py:176–177` now asserts
  `diff vs build.sh.before-fix23 is additions only (+314/-0)`.
  Recomputed independently: `diff build.sh.before-fix23 build.sh`
  = **314 additions, 0 deletions**. The edit is arithmetically
  correct (+305 + 9 new fix26-block lines = +314; the §3 comment
  reword is 0 net lines).
- No other verifier file was changed: every other `fix*/verify*.py`
  carries a Nov 11–13 mtime; only `fix25/verify25.py` is Nov 14
  (21:32). No git repo exists in this workspace, so this is mtime +
  content evidence rather than a diff against a pristine copy; the
  content evidence is that the only `305`/`314` references in
  `verify25.py` are `:22` (docstring, still +305 — M1) and `:176–177`
  (assertion, +314).
- Expected consequence, not a finding: verify25's fingerprint check
  (build.sh 24,079 lines / md5 `f19483f5…`) now fails on the fix26
  tree by design — it is a fix-#25-time verifier and fix26 changed
  build.sh. verify26 must codify the new fingerprint (24,088 lines,
  md5 `e05bdc66…`). Final re-run on the completed run-4 tree
  (`fix26/audit73-verify25-run4.txt`, exit 1): **72/75 checks pass
  (72/74 excl. the manifest check)**. The 3 FAILs are exactly the
  predicted set: (1) the fingerprint check (by design, see above);
  (2) fix24 97/104 vs expected 98/104 — the single unexpected FAIL
  is E-5 "pitch-deck-video venv Windows form", the pip-pinning.md
  flag-1 prediction: the §1 pin of the yt-dlp line broke verify24's
  assertion of the old unpinned line (to be codified in verify26,
  not a plugin defect); (3) the fix26-manifest check (OWED — the
  manifest is written after this audit, correctly failing until
  then). The diff check PASSES (`+314/-0`). All other prior
  verifiers match their codified tails exactly: fix15 42/44,
  fix17 58/60, fix18 69/72, fix19 71/76, fix20 164/169, fix21 96/102,
  fix22 366/369, fix23 194/211 excl. manifest, verify13h 6/97
  (2 B2 + M3 :61, :62, :70, :71; F-04 :57, :63, :66 pass) — the
  run-1 reading against the intact run-3 tree (72/75) reproduces
  exactly on the run-4 tree.
- **Mid-build artifact — do not misread an earlier run:** a
  verify25 run executed while build run 4 was still mid-flight
  (tree at 169 skills / 96 commands, fix26.py not yet run) reported
  71/75 with verify13h FAILING at 29/97 instead of 6/97
  (`fix26/audit73-verify25-output.txt`). The 29 fails were all
  count=0 absences of strings the build-time patch blocks insert
  (standalone snapshot-integrity items, B3 gan-design record-first
  items, B4 carve-out) — i.e. the verifier read a half-built tree,
  not a broken plugin. Two direct verify13h runs made during the
  mid-build window are byte-identical to each other at 29/97,
  proving the verifier is deterministic — the 29 is a property of
  the half-built tree, not flakiness. Against the completed run-4
  tree, verify13h is back to exactly 6/97 (verify25-run4 `:75`
  PASS). The mid-build reading is discarded; the run-4-tree
  reading is the audit's result.

## Re-verification on the run-4 tree

After run 4 completed (~21:43:57 UTC), every built-tree claim was
re-checked from scratch against the new tree. All reproduced
exactly — no claim changed:

- Run-4 log: `fix26: 16 change(s)`, `fix26: OK`, counts
  166/72/123/87/15, TOTAL BANNED-TERM HITS: 0.
- Pip: 42 lines, 22 unpinned (same 22 (b)/(c)/(d) lines).
- Banned terms 0; Grok 54/103/0; counts 166/72/123/87/15.
- ck: all three `~1k tokens per session` lines at
  SKILL.md `:159`, mjs `:6`, mjs `:90`; `:129` unchanged; 0 stale
  claims in `skills/ck/`.
- F-14: `README_UPDATE_F26` in all 4 files at the same lines
  (`:217`, `commands/demo.md:9`, orchestrate `:101`,
  readme-writer `:95`).
- VARFONT_F26 ×1 in the inventory; B6 `:38`
  DOCUMENTATION-ONLY; call-map staged == built (md5
  `8d4c10efefbd844603e6743ed9893718`, 622 lines each — the md5
  moved from the 21:36 regeneration's `414d47af…` because the
  staged file was regenerated a second time at 21:41:28 before
  run 4; content checks — 52 uncalled, trigger-only 0, B1–B6
  bullets — are unchanged, so this is generator ordering noise,
  not a content change).
- Benchmark: 178 lines, "NONE RECORDED" Dim 7 intact.
- B6 grep evidence re-checked on the run-4 tree: 64 keys,
  0 unresolved, 0 `context-` refs in `hooks/*.js`,
  `trigger_only: []`.

## Supply-chain spot-check — PASS

Pins in `build.sh:37–41` vs disk scratch clones at
`fix26/scratch-clones/` (HEADs read directly):

| Pin | build.sh | Scratch clone HEAD | Match |
|---|---|---|---|
| UIPRO_PIN | `6ae86f61…` | `fix26/scratch-clones/uipro` `6ae86f61f520d6ca229d2f40e070410638c908c5` | yes |
| MARKETPLACE_PIN | `f210c6d0…` | `fix26/scratch-clones/hack-skills` `f210c6d05b10a6a17c5cf67d7b7d13565d1f5dc9` | yes |
| CHWEZI_PIN | `d7d85b6e…` | `fix26/scratch-clones/skill-add/chwezi-dev-engine` `d7d85b6e2687cad33e0f3cc826ae835c423e83ae` | yes |
| FLECTO_PIN | `3a0f7e52…` | `fix26/scratch-clones/skill-add/flecto-shade` `3a0f7e52cdb53c52494c7c34235001a042dd9822` | yes |
| AGENTSKILLS_PIN | `c13e8b35…` | `fix26/scratch-clones/skill-add/hackathon-agent-skills` `c13e8b35d44085accc7ec3b1b4410247d4969514` | yes |

- `fix26/scratch-clones/ecc-repo-clean` is not a git repo (plain
  copy); no pin applies to it. Left alone.
- `/tmp/skill-add/chwezi-dev-engine` — state recorded only, NOT
  touched: HEAD `8590f971517520c5b34cd41a16780e4f1cd74ceb` (not the
  pin); `git status` shows the whole tree staged ("Changes to be
  committed"), consistent with the known-corrupt empty-index state.
  The disk re-clone bypassed it; the build used the pinned clone.
  Nothing was deleted or "repaired".

## Findings summary

| # | Severity | Location | Issue |
|---|---|---|---|
| M1 | Minor | `fix25/verify25.py:22` | Docstring still says `+305/-0` after the assertion moved to `+314/-0` |
| M2 | Minor | `build.sh:24070–24075` | New fix #26 comment: header "(ck cost lines)" omits the §1 pip pins; `:24075` "(placeholder section, pip worker)" — no placeholder section exists in `fix26.py` |

No blocking findings. The close criteria (ZERO blocking, ZERO minor)
are not met until M1 and M2 are fixed or adjudicated by the parent;
both are one-line comment corrections, and M2's fix must be followed
by a re-verification of the +314/-0 tail (a pure reword of existing
added lines keeps it at +314/-0, but verify, don't assume).

## Evidence files

- `fix26/audit73-pip-grep.txt` — all 42 `pip install` lines in the
  built tree (run-3 tree).
- `fix26/audit73-pip-unpinned.txt` — the 22 unpinned lines.
- `fix26/audit73-comment-after.txt` — `build.sh:24061–24067` as read.
- `fix26/audit73-verify25-output.txt` — verify25 re-run executed
  mid-run-4-build (DISCARDED reading: verify13h 29/97 against a
  half-built tree; kept as the record of why that reading is not
  the audit's result).
- `fix26/audit73-verify25-run4.txt` — verify25 re-run against the
  completed run-4 tree (the audit's §9 result).
- `fix26/audit73-verify13h-runA.txt` /
  `fix26/audit73-verify13h-runB.txt` — two byte-identical direct
  verify13h runs made during the mid-build window (29/97 — the
  half-built tree; proves determinism, not a result).
