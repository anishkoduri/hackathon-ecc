# Sweep #34 — Fix #26, weaving-coherence sweep — CHECK-ONLY report

**SWEEP #34: NOT CLEAN — 0 blocking, 2 minor, weaving-coherence NOT CLEAN**

Scope: staged sources (`new-skills/`, `round2-skills/`, `rewritten-skills/`,
`new-rules/`), the build-time patcher `fix26/fix26.py`, the built tree
`~/workspace/hackathon-plugin/hackathon-ecc/` (run 3, exit 0; node_modules
excluded everywhere), `build.sh`, and the fix #26 working files. Check-only:
no plugin file edited, no `build.sh` run, no fix/apply/verify script edited,
no bundle, commit, push, or message sent. One exception, disclosed in §8:
two generator runs rewrote the staged call map in place (the generator
takes no output argument); the staged file was restored from the scratch
copy each time and verified byte-identical to the built copy afterwards.

Read first, in full: `fix26/SPEC.md` (§0–§10), `fix26/PARENT-GUIDANCE.md`,
`fix25/MANIFEST.md` (§5/§6), `fix26/f14-note.md`, `fix26/varfont-note.md`,
`fix26/ck-note.md`, `fix26/b6-note.md`, `fix26/dim7-note.md`,
`fix26/r1r4-note.md`, `fix26/comment-fix.md`, `fix26/pip-pinning.md`,
`fix26/pip-patches.md`, `fix25/sweep33b-report.md`. Every number below was
re-derived by this sweeper's own greps/commands listed in §9; nothing was
copied from the fix notes without re-running.

## 1. Build fingerprint + counts (re-derived)

| Item | Re-derived value | Expected | Result |
|---|---|---|---|
| `build.sh` lines | 24,088 (`wc -l`) | 24,088 (task brief) | PASS |
| `build.sh` md5 | `e05bdc66599b694398e11f0d00dfdafd` | same | PASS |
| `build.sh` delta vs fix #25 baseline | +9 lines (24,079 → 24,088) | +9, the fix26.py invocation block | PASS — the §3 comment fix is 0 net lines (7 → 7); the +9 is the new invocation block (header + 6 comment lines + `python3 … fix26.py` + blank), the same shape as fix #25's +9 invocation block |
| skills / agents / rules / commands | 166 / 72 / 123 / 87 (directory counts) | 166/72/123/87 | PASS |
| hooks | 15 (`hooks.json` hooks dict) | 15 | PASS |
| trigger keys | 64 (`skill-triggers@1.json` triggers object) | 64 | PASS |
| call-map header counts | 166/72/123/87/15/64 | same | PASS |

## 2. F-14 — post-report /demo stale README (§2): VERIFIED

**The new step 7 agrees across all four staged files.**

- `README_UPDATE_F26` occurrences: **4 staged / 4 built** — exactly the
  four edited files, no other file carries the token:
  `new-skills/pitch-deck-video/SKILL.md:217`,
  `new-skills/pitch-deck-video/commands/demo.md:9`,
  `new-skills/orchestrate/SKILL.md:101`,
  `rewritten-skills/readme-writer/SKILL.md:95` (same lines in the built
  copies).
- **Step 7 itself** (staged pitch-deck-video SKILL.md:217–270, re-read in
  full): ledger record first (`demo video: <app-name>-video/out/demo.mp4`
  in `.hackathon/run-ledger.md`); first-match-wins idempotent README edit
  (a. already links the path → do nothing; b. video placeholder →
  replace; c. readme-writer badge-button block → add a matching Demo
  Video button; d. else insert a `## Demo video` section after the title
  block, or at the top with no `# ` heading); no README → write none,
  record the path in the /demo return; re-cuts (`--rebuild` / `--script` /
  `--render`) are a no-op via rule 2a; **the final report is not rewritten
  here** (orchestrate-owned, point-in-time; the /demo return carries the
  video path as handoff input).
- **Badge convention resolves:** rule 2c names the readme-writer
  house-style block as "`**Live demo:**` followed by a `<p align="center">`
  button row" — `rewritten-skills/readme-writer/references/readme-template.md:51`
  is `**Live demo:**` and :53 opens the `<p align="center">` button row
  with a black `for-the-badge` shields image, matching step 7's Demo Video
  button markup. The `<!-- 🎥 Demo video: <path> -->` comment convention
  is the same one readme-writer :95 already names.
- **Placeholder convention resolves both ways:** readme-writer :122
  ("draft with clearly-marked placeholders like
  `<!-- TODO: add demo link -->` so nothing important is silently
  dropped") is the placeholder step 7 rule 2b replaces; readme-writer :95
  now says a later-filmed video "is linked into the README by that run
  (pitch-deck-video step 7, README_UPDATE_F26) — readme-writer is not
  re-run just for the video link."
- **Orchestrate step 6 agrees:** :101 now reads "a video filmed later by
  an explicit `/demo` run is linked into the README by that run
  (pitch-deck-video step 7, README_UPDATE_F26), not by re-running this
  step". The fix #22 gate sentence in the same line ("A demo video is
  filmed only when the user invokes `/demo` explicitly — it is never part
  of this order", DEMOGATE_O9_F22) is untouched. Orchestrate :356's
  sequence ("verify → polish → deploy → commit → README (`readme-writer`)
  → final report") describes the in-sequence case only and does not
  contradict the post-report path; :378's demo-video handoff (video path
  + upload instruction) is the in-sequence handoff, and step 7 rule 5
  keeps the report point-in-time after a post-report run.
- **No new gate, no auto-/demo:** DEMOGATE tokens staged H1/H2/O4/O9 ×1
  each; built adds B2S1–S7/B3S1–S7/B2C1/B3C1 (the build-time browser-qa
  patch, same as Sweep #33b). `demo.md:9` sequences the link after QA
  ("build, and QA … — then link the video into the README per the skill's
  step 7"). Orchestrate :56/:99 and orch-build-mvp :85 ("Demo — never
  automatic", DEMOGATE_B2S1_F22) still forbid dispatching /demo; no fix
  #26 text dispatches it. Orch-build-mvp :85 ("invoke `readme-writer` to
  write/update the README … before the final report in step 9") is the
  standalone pipeline's in-sequence case and does not contradict step 7.
- **No other skill still implies the README only gets the video if filmed
  before step 6:** grep over staged + built for `TODO: add demo link` /
  `TODO: add video` returns only the three consistent sites (pitch-deck-video
  :241–242 rule 2b, readme-writer :95, readme-writer :122). No "steps 1–6"
  / "six steps" reference in pitch-deck-video goes stale with the new
  step 7 (0 hits).
- **Staged-vs-built diffs for the four files:** pitch-deck-video SKILL.md
  IDENTICAL; readme-writer SKILL.md IDENTICAL. Orchestrate SKILL.md
  differs only in the two pre-existing build-time agent-link expansions
  (:96, :261 — bare `` `code-reviewer` `` → `` `code-reviewer` agent
  (`agents/ecc-code-reviewer.md`) ``, present since run 2). `commands/demo.md`
  differs only in the pre-existing build-time narration-key paragraph
  (:13, direct-vs-dispatched invocation wording) — not a fix #26 edit.
- **Observation O1 (not a finding):** the ledger line label `demo video:`
  is defined only on the write side (pitch-deck-video :235). Readme-writer
  :95 says it takes the video path "from `.hackathon/run-ledger.md`" and
  names the path format (`<app-name>-video/out/demo.mp4`), not the line
  label. Channel and path format agree on both sides; only the label is
  single-sourced. No change needed for coherence — the label is defined
  once, in the step that writes it.

## 3. Variable-font scoped exception (§4): VERIFIED

**Inventory §11 records the exception with the scope and reason, and no
other file contradicts it or widens it.**

- `VARFONT_F26` occurrences: **1 staged / 1 built** —
  `new-skills/orchestrate/references/design-inventory.md:166`, the new
  "## 11. Scoped exceptions" section (:162–166). Scope as recorded:
  template only — `HankenGrotesk.woff2` (34,704 B, variable wght 100–900)
  + `JetBrainsMono.woff2` (30,376 B, variable wght 400–500);
  `InstrumentSerif.woff2` (21,032 B) stays static, weight 400 only.
  Reason as recorded: single controlled Chromium + fixed video output, so
  the cross-platform variance the rule guards against does not apply;
  "App UI fonts stay static-only."
- **Sizes and split verified against the files, not the note:** built
  `template/public/fonts/` holds exactly the three files at 34,704 /
  21,032 / 30,376 B. `template/src/fonts.ts:11–15` records the same split
  in its own comments (Hanken "VARIABLE font, wght 100-900", Instrument
  Serif "static, 400 only", JetBrains "VARIABLE font, wght 400-500") and
  is byte-identical staged vs built.
- **App-UI static-only stands everywhere it appears:** orchestrate :139
  ("A variable font file is NEVER the shipped delivery format… its
  interpolated weights render differently under iOS vs Windows"),
  orchestrate :96 (F2 static check — "a row naming a variable file… is
  an incomplete build", operating on the app's Type list in
  `docs/design-tokens.md`), polish-pass `reference/lenses/typeset.md:55`
  and :96 (same F2 wording, Type-list scope). None of these checks can
  fire on the video template: the template's fonts are not in any build's
  Type list, and no verifier asserts variable-font absence in the template
  (0 "variable" hits in `fix19/verify19.py` and `fix21/verify21.py`).
- **Observation O2 (not a finding):** the absolute phrasings — orchestrate
  :139 "NEVER" and pitch-deck-video SKILL.md:308 "keep fonts self-hosted
  and static (fix #19/#21)" — carry no pointer to VARFONT_F26. The
  inventory entry explicitly names the rule it narrows (citing the :308
  wording), and the F2 check's scope is the app Type list, so this is a
  missing cross-pointer, not a contradiction. SPEC §4 requires the record
  in the inventory + manifest only, which is what was done.
- **Observation O3 (not a finding):** inventory :39 "Design asset library
  pins (§11/§15/§17)" refers to fix #22 SPEC sections (§11 libraries,
  §15, §17 — verified against `fix22/SPEC.md`), not to inventory
  sections. The inventory previously had no §11, so the bare "§11" was
  unambiguous; the new inventory §11 ("Scoped exceptions", about fonts,
  not libraries) makes it newly misreadable at a glance. The row's own
  "(see §9 below)" shows internal refs are marked "below", and the row's
  "Where it lives" column points at `skills/ui-ux-pro-max/SKILL.md`, so
  the reference still resolves correctly — this is a readability
  ambiguity introduced as a side effect, not a dangling reference.

## 4. Trigger router B6 (§5): 2 MINOR FINDINGS

### 4.1 What agrees

- Staged call map :38 and the generator template
  `fix25/callmap/generate_call_map.py:753–761` carry the identical
  DOCUMENTATION-ONLY wording: "trigger router has no live Cursor entry
  point (fix #26: DOCUMENTATION-ONLY)", the consumer chain
  (`context-pack-registry.js` → `context-selection.js` →
  `context-routing-index.js` / `context-prompt-suggestions.js`), "neither
  consumer is invoked from `hooks/*.js`", the upstream-only quote, "a
  DEFINED routing path, not a LIVE one", "a documentation-only reference
  table … not a live routing table", and the pointer to `fix26/b6-note.md`.
- The triggers table's per-element flow strings are the qualified form:
  64 rows carry "on-request (trigger-routed; no live Cursor entry — see
  method note B6)" (spot-checked :597/:609 and the surrounding rows).
- `fix25/callmap/call-map-data.json` has `"trigger_only": []`; the
  generator run reports trigger-only 0, all 64 keys resolve, counts
  166/72/123/87/15/64 all OK, corpus 1,710 files — matching the fix #25
  manifest.
- Wiring-list §E agrees ("dormant router, B6"; "no live Cursor entry —
  blind spot B6").

### MINOR 1 — Generator comment still calls skill-triggers a "live routing table"

`fix25/callmap/generate_call_map.py:383`:

```python
# skill-triggers@1.json is a live routing table, not install data.
```

This directly contradicts the DOCUMENTATION-ONLY disposition recorded at
call-map.md:38 and in the same file's template (:753–761, "not a live
routing table"). The comment's functional content is correct — the file
is excluded from `manifest_files` so its entries count as invocation
evidence rather than install data — but the label is stale: it is the one
remaining place in the tree (verified by grep over staged + built, excl.
node_modules) that describes `skill-triggers@1.json` as a live routing
table. The other mentions are neutral (`context-pack-registry.js:12`
path constant; `context-retrieval.js:105` descriptive "carries a
`triggers` array (from the checked-in skill-triggers manifest)"). Fix: a
one-line reword of the comment (e.g. "a defined routing table, not
install data" / "documentation-only reference, not install data").

### MINOR 2 — 64 skills-table rows carry the bare "on-request (trigger-routed)" flow string

`fix25/callmap/generate_call_map.py:342` emits the unqualified string for
trigger-kind invokers in the main element tables:

```python
if kind == "trigger":
    return "on-request (trigger-routed)"
```

Result in the staged call map: **64 rows** (e.g. :67 `accessibility`,
:72 `ai-feature-spec`, :76 `api-design`) list "on-request (trigger-routed)"
as a flow with no B6 qualifier, while the **64 triggers-table rows** carry
the qualified string "on-request (trigger-routed; no live Cursor entry —
see method note B6)". A reader of the main element tables alone sees
trigger routing presented as an ordinary dispatch path, with no pointer
to the "no live Cursor entry" caveat that the B6 bullet and the triggers
table carry. The bare string does not assert liveness, so this is a
missing qualifier, not a false claim — but the brief's agreement check
names the qualified string as the per-element form, and the main tables
do not use it. Fix: qualify the :342 emission the same way (or point it
at B6) and regenerate.

### 4.2 Generator-vs-staged drift (prescribed procedure)

Per the parent's correction, the generator was run only via the
copy-aside → run → diff → restore procedure (scratch copies under
`fix26/`, removed afterwards). The regenerated staged file differs from
the audited staged file in **exactly 6 rows, flow-column ordering only**
(same flow set, different order — the generator puts "on-request
(trigger-routed)" last; the hand-maintained file has it earlier):

| Row | Element | Audited file | Regenerated file |
|---|---|---|---|
| :90 | `code-tour` | build (expansion); on-request (trigger-routed); build | build (expansion); build; on-request (trigger-routed) |
| :123 | `error-handling` | on-request (trigger-routed); build | build; on-request (trigger-routed) |
| :127 | `frontend-a11y` | design package; on-request (trigger-routed); build | design package; build; on-request (trigger-routed) |
| :141 | `hexagonal-architecture` | on-request (trigger-routed); build | build; on-request (trigger-routed) |
| :166 | `mcp-dependency-review` | on-request (trigger-routed); build | build; on-request (trigger-routed) |
| :205 | `redis-patterns` | on-request (trigger-routed); build | build; on-request (trigger-routed) |

`call-map-data.json` is byte-identical after regeneration. Counts all OK.
The same 6-row drift was observed in the parent's run. **Nondeterminism
observed:** an earlier accidental run of the same generator on the same
tree reproduced the staged file with 0 differing rows, while this run
(and the parent's) produced the 6-row ordering drift — flow-column order
varies run to run, so "re-run the generator" does not byte-reproduce the
staged file. The map header's "Do not edit by hand — re-run the
generator" instruction therefore invites ordering churn on every
regeneration; that is a generator property the coordinator should know
about, not a staged-file defect. No content (counts, sets, B6 wording) is
affected by the drift.

## 5. ck wire KEEP (§8): VERIFIED

- Built tree carries the corrected lines: `skills/ck/hooks/session-start.mjs:6–7`
  ("Injects ~1k tokens per session (not ~2,500 like v1): the full SKILL.md
  (~170 lines) plus the compact summary below."), :90 ("Load skill (always
  inject the full SKILL.md, ~170 lines, ~1k tokens/session)"),
  `skills/ck/SKILL.md:159` ("The hook injects ~1k tokens per session (the
  full SKILL.md plus the compact 5-line summary).").
- The intentionally-kept line is untouched: `session-start.mjs:129`
  "Compact summary block (~100 tokens)" — the only "~100 tokens" hit left
  in the built tree.
- No other stale cost claims anywhere in the ck tree: `grep -rn "~100 tokens|~50 lines"`
  over `hackathon-ecc/` (excl. node_modules) returns 0 hits outside :129;
  `grep -rn "100 tokens|50 lines|tokens per session|tokens/session"` over
  staged sources returns 0 hits (ck is upstream — 0 staged dirs exist for
  it, verified). The "~1k tokens/session" figure is the only session-cost
  figure except the kept :129 block figure.
- `fix26/fix26-patch-log.md`: 16 changes, 0 errors (3 ck + 13 pip).
  `skills/ck/SKILL.md:157` "already wired" note (fix #25 §1) is intact.
  The wire itself (`hooks/session-start.js` spawn) is untouched by
  fix26.py — the script only edits the three cost lines.

## 6. Pip pins (§1): VERIFIED

- Built tree: **42 `pip install` lines**, exactly the classification in
  `fix26/pip-pinning.md` (20 (a) / 8 (b) / 6 (c) / 8 (d)). Every one of
  the 20 (a) lines now carries `==` pins; the only line surviving an
  "unpinned named-package" filter is `tts.mjs:180`, the class-(b) runtime
  error string, deliberately left unpinned. All (b)/(c)/(d) lines are
  byte-identical to the pip-pinning.md table (spot-checked: bengali-nlp
  :87/:139/:207, django-verification :428 `-r requirements.txt`,
  ecc-agent-evaluator :33 forbidden list, insaits :205/:78 runtime
  messages, pi-core.json policy lines).
- **Staged 7 lines pinned** in `new-skills/pitch-deck-video/`: SKILL.md:843
  (all three `piper-tts==1.8.0` mentions on the one line),
  shots-reference.md:247, troubleshooting.md:212 (`piper-tts==1.8.0`),
  :232/:233 (`yt-dlp==2026.10.26`), tts.mjs:134/:135. Staged grep shows
  only tts.mjs:180 unpinned (the (b) error string). No dangling references
  to unpinned commands: no other staged file references the unpinned
  `pip install piper-tts` / `pip install yt-dlp` forms. (The pip-pinning.md
  note's "staged :843 is built-tree :788" was vs the pre-F-14 run-5 tree;
  both copies are now :843 because the rebuilt tree carries §7 too.)
- **13 fix26.py patches agree with `fix26/pip-patches.md` P-01–P-13** and
  all 13 appear in the patch log with 0 errors (django-verification :429,
  frontend-slides html-template :324 + extract-pptx.py :9, django-celery
  :26 + :411, generating-python-installer :627, plankton :81,
  windows-desktop-e2e :55/:651/:755/:880, gateguard-fact-force.js :19,
  insaits-security-monitor.py :13). P-07's FIX24-OWNED flag is honoured:
  fix26.py patches the built text once; `fix24.py` is not edited.
- **No conflict with staged text:** fix26.py patches upstream files only
  — 0 staged dirs exist for django-verification, frontend-slides,
  django-celery, generating-python-installer, plankton-code-quality,
  windows-desktop-e2e, and ck. The staged pitch-deck-video pins and the
  build-time upstream patches touch disjoint files.
- Carried flags for verify26 / the coordinator (not sweep findings):
  pip-pinning.md flag 1 — `fix24/verify24.py:389` (E-5) asserts the exact
  unpinned Windows yt-dlp line that is now pinned, so it will fail unless
  codified; flag 2 — SPEC §1's "grep for unpinned `pip install` lines =
  0" holds only scoped to category (a), since the (b)/(c)/(d) lines
  remain unpinned by design.

## 7. Dim 7 / R1/R4 (§6/§7): VERIFIED — owed records consistent, no softened pass

- **Benchmark file** (`design-benchmark-v5.md`, identical staged vs
  built): §2 Dim 7 — v5 figure "NONE RECORDED (no v5 figure)", bar "0
  problems across the full ALIGN_F23 coverage matrix", scored by
  "browser-qa live verdict (owed, never claimed statically)". §3 — "If a
  dimension cannot be scored — statically or live — the leg says which,
  and records it as a gap (owed), not as a pass. A leg that cannot score a
  dimension does not PASS on that dimension." §1 caveat on provenance —
  "The live v5 artifact is NOT in this workspace… A live re-measure
  against the real artifact would supersede these figures". Iris-opens:
  "DEALT but has NO recorded application anywhere in the available
  source"; R4 hero loop: "likewise has no recorded application". No
  softened pass language anywhere in the file.
- **Dry-run #40 record agrees:** `dryrun40-report.md` §2.3 — "6 of 7
  dimensions pass statically; dimension 7 is OWED… never passed"; "A leg
  that cannot score a dimension does not PASS on that dimension"; the Home
  Run 52-measurement run "is live alignment evidence about Home Run, not
  Campus Eats, and is not counted toward dimension 7". Dim 3's row reads
  "PASS (static); strength verdict OWED to browser-qa" — the static/live
  split is labelled, not smoothed over.
- **r1r4-note verified against the render (not trusted from the note):**
  iris-opens IS implemented in Home Run as the trip-view code-panel
  reveal — `cold-start-render/home-run/index.html:179–180`
  (`iris-wrap`/`iris-disc`), `styles.css:426–446` (`iris-ring` 0.7s,
  `iris-open` clip-path 0.6s), `app.js:187–193` (`enterTrip` adds
  `iris-open` 120ms after entering the trip view) — but that is not the
  benchmark's hero → picks transition (#67); Home Run has no picks section
  and no ramen photo. R4 hero loop: grep for
  `loop|steam|cycle|wisp|marquee|carousel|ticker|setInterval` across
  Home Run `index.html`/`styles.css`/`app.js` returns **0 hits**, and
  `loop` in `docs/design-tokens.md` returns 0 hits. Campus Eats dir holds
  only the 5 files the dim7-note lists (tokens file, hallmark salt/log,
  taste history files) — no `index.html`, nothing browser-qa could
  measure. The notes' OWED verdicts (R1 owed as defined, with adjacent
  Home Run evidence recorded; R4 owed with no adjacent evidence) match
  the files.
- **No other file claims Dim 7 / R1 / R4 as passed or verified:** grep for
  "dimension 7|dim 7" over staged + built skills/commands returns 0 hits
  outside the benchmark file; "hero loop|iris-opens" outside the benchmark
  file and the moments catalog returns only Taste :406's baseline note
  ("iris-opens was dealt and never applied" — the fix #15 R1 rule) and
  `moments.md` catalog entries.
- **Pending, not a finding:** `fix26/MANIFEST.md` and `fix26/verify26.py`
  do not exist yet at sweep time, so the "manifest record" leg of the
  owed-record consistency check cannot be verified this round. The
  benchmark file + the two fix26 notes + the dry-run #40 report are
  mutually consistent; the manifest must carry the same OWED wording when
  written.
- Nit (not a finding): two r1r4-note line refs are off by one
  (`styles.css:425–446` vs actual :426; `app.js:190–192` vs `enterTrip`
  :187–193) — the substance verified is exact.

## 8. §3 comment fix + general weaving

- **build.sh fix25 comment** matches `fix26/comment-fix.md` "After" block
  (header now "§1 wires, §2 inventory, §4 S1/benchmark"; body names the
  ck + /prp-commit wires, the orch-* inventory close, S1 80 → 89, the
  browser-qa beat-v5 line, and the loop-status removals). The comment-fix
  note's accuracy point holds: only W1/W2 live in fix25.py; W3/W4 are
  staged orchestrate edits, correctly not named as script wires. Line
  count 7 → 7.
- **Anchor census:** `_F26` — README_UPDATE_F26 4/4, VARFONT_F26 1/1
  (staged/built). `_F25` unchanged from Sweep #33b: RECIPES 1/1, TESTCOV
  1/1, PLATFORM 2/2, BENCHMARK_V5_F25 8/10 (the +2 are the fix25.py
  browser-qa patch), TECHDEPTH 8/8, ADAPT 2/2, REASON 6/6, CREATIVE 3/3.
  No new `_F25`/`_F26` token; no orphan anchor.
- **Banned terms:** 0 in the built tree. **Grok pins:** `grok-4.7-high`
  ×54, `cursor-grok-4.6-high-fast` ×103, bare `grok-4.6-high-fast` ×0 —
  exactly Audit #72's numbers.
- **Six/seven convention:** untouched by fix #26 — the only orchestrate
  edit is the :101 clause, which carries no count; the convention line
  (:66) and the Depth extension were not re-derived this round because no
  fix #26 edit touches them.
- **Sweep-process disclosure:** this sweeper's first `--help` probe of the
  generator accidentally ran it (it takes no `--help`) and rewrote the
  staged call map in place; the file was verified byte-identical to the
  built copy immediately afterwards (md5
  `414d47af3c7e59aa82e9eb3a63161a35`). The parent then ran the generator
  the same way, observed the 6-row drift, and restored the staged file
  from the built copy. This sweep's prescribed-procedure run reproduced
  the same 6 rows and restored from the scratch copy, verified afterwards:
  staged md5 `414d47af…` == built copy, data.json md5
  `a75c2a9fe99ee94a99a18c28eb4eb487` unchanged, scratch copies removed.
  The tree is left in the audited state.
- **Hygiene note (not a finding):** `fix26/scratch-clones/` (69M) and
  `fix26/scratch-tmp/` (2.9M) are pre-existing coordinator scratch from
  earlier fix #26 work, not this sweep's (this sweep's only scratch was
  the two call-map backup copies, removed after the restore).

## 9. Findings

**MINOR 1 — `fix25/callmap/generate_call_map.py:383` calls skill-triggers
"a live routing table".** Directly contradicts the B6 DOCUMENTATION-ONLY
disposition (call-map.md:38, generator :753–761). One-line comment reword;
the exclusion logic it documents stays correct.

**MINOR 2 — 64 skills-table rows use the bare "on-request
(trigger-routed)" flow string** (`generate_call_map.py:342`), without the
B6 qualifier the 64 triggers-table rows carry. A reader of the main
element tables sees trigger routing as an ordinary dispatch path with no
pointer to "no live Cursor entry". Fix: qualify the :342 emission and
regenerate (noting §4.2's ordering churn on regeneration).

**Generator-vs-hand drift (recorded, not a separate finding):** a
generator re-run differs from the audited staged call map in exactly 6
rows (:90, :123, :127, :141, :166, :205), flow-column ordering only, and
the ordering varies run to run — see §4.2.

## 10. Open items (carried, explicitly — not findings this round)

1. **Fix the two MINORs** (§9): reword the :383 comment; qualify the :342
   flow string and regenerate the call map (accepting the 6-row ordering
   churn, or sorting the flow column deterministically first).
2. **fix26/MANIFEST.md + verify26.py do not exist yet** — the manifest
   must record Dim 7 OWED and R1/R4 OWED in the same wording as §7, the
   VARFONT_F26 exception, the B6 DOCUMENTATION-ONLY disposition, the ck
   KEEP, and the §3 before/after tails; verify26 must codify the
   verify24 E-5 tail (pip-pinning flag 1) and the §3 diff movement.
3. **Dry-run #41 / Audit #73** exist in `fix26/` (report files present)
   but were not swept here — this sweep covers the staged sources and the
   built tree, not the dry-run/audit verdicts.
4. **Observations O1–O3** (§2, §3): ledger line label single-sourced in
   step 7; absolute font-rule phrasings carry no VARFONT_F26 pointer;
   inventory :39's "§11/§15/§17" (fix22 SPEC refs) is newly ambiguous
   beside the inventory's own §11. None blocks CLEAN on its own.
5. **Carried prior open items (unchanged):** Netlify row touch-up due
   after Dec 4, 2026; live smoke test still the gate before GitHub publish
   (do NOT push b2444de); live film / rendered demo.mp4 / measured
   narration / mix listen owed to the smoke test; D-6, C-5, C-6, D-9, E-7
   carried items from fix25/MANIFEST.md §5.

## 11. Commands run (method)

All run read-only from `~/workspace/hackathon-plugin` (built-tree greps
from `hackathon-ecc/`; no test copies made except the two call-map
backups under `fix26/`, removed after the restore):

- `wc -l build.sh && md5sum build.sh`; directory counts per built
  directory; `hooks.json` hooks dict (15); skill-triggers key count (64)
- `grep -rn README_UPDATE_F26 / VARFONT_F26` staged + built; full read
  of staged pitch-deck-video SKILL.md:217–270; `sed` of readme-template
  :51–55, readme-writer :95/:122, orchestrate :56/:99/:101/:356/:378,
  orch-build-mvp :32/:85–86, demo.md
- `grep -rn "TODO: add demo link|TODO: add video"` staged + built;
  `grep -rni "invoke.*/demo|/demo.*automat"` orchestrate + pitch-deck-video
- DEMOGATE token census staged + built; banned-term grep (built tree, 0);
  Grok-pin counts (54 / 103 / 0, bare via `grep -rPo '(?<!cursor-)grok-4.6-high-fast'`)
- Per-token census loop for all 8 `_F25` tokens + 2 `_F26` tokens (staged
  and built, occurrences)
- `diff` staged vs built for orchestrate SKILL.md, design-inventory.md,
  design-benchmark-v5.md, pitch-deck-video SKILL.md, commands/demo.md,
  shots-reference.md, troubleshooting.md, tts.mjs, readme-writer SKILL.md,
  call-map.md
- `grep -rni "static-only|self-hosted and static|static.*font"` staged;
  full read of orchestrate :139/:96 (F2), polish-pass typeset :55/:96;
  `grep -rn variable fix19/verify19.py fix21/verify21.py` (0 hits);
  `ls -la` template fonts (34,704 / 21,032 / 30,376 B); `diff` fonts.ts
  staged vs built (identical)
- `grep -rn "100 tokens|50 lines|tokens per session|tokens/session"`
  staged (0) + built ck (4 hits, all corrected/kept as specified);
  `grep -rn "~100 tokens|~50 lines"` built tree (0 outside :129);
  `cat fix26/fix26-patch-log.md` (16 changes, 0 errors)
- `grep -rn "pip install"` built tree (42 lines) + staged pitch-deck-video
  (8 lines incl. tts.mjs:180); unpinned-named-package filter (only
  tts.mjs:180 survives); staged-dir existence check for all 7 fix26.py
  target skills + ck (0 each)
- `sed` benchmark file §1–§3 (full read, 178 lines); `grep -rni
  "dimension 7|dim 7|hero loop|iris-opens"` staged + built;
  `grep -n iris` + loop-grep over Home Run `index.html`/`styles.css`/
  `app.js` + `docs/design-tokens.md`; `find` campus-eats (5 files);
  `grep -n "dimension 7|OWED"` dryrun40-report.md
- `sed -n '753,761p'` + `:597` + `:342` + `:383` generate_call_map.py;
  `grep -rn "skill-triggers"` staged + built; `grep -c` qualified (64)
  vs bare (64) flow strings; `python3 -c` trigger_only [] + counts
- Prescribed generator procedure: `cp` staged call-map.md +
  call-map-data.json aside → `python3 fix25/callmap/generate_call_map.py`
  → `diff` regenerated vs scratch copy (6 rows) → `cp` back → `md5sum`
  + `diff -q` staged vs built (identical) → `rm` scratch copies
- `sed -n '24055,24075p' build.sh` (fix25 comment + fix26 invocation
  block); `grep -n fix26 build.sh`

## Verdict

**SWEEP #34: NOT CLEAN — 0 BLOCKING, 2 MINOR, weaving-coherence NOT CLEAN.**

F-14 is woven consistently across all four files (ledger both ways, badge
and placeholder conventions resolve, gates stand, final report untouched);
the variable-font exception is scoped to the video template with app UI
fonts static-only and no contradicting file; the ck stale cost lines are
corrected with only the intentional :129 block figure left; all 20 real
pip-install lines are pinned with the (b)/(c)/(d) lines unchanged and the
13 build-time patches disjoint from the 7 staged pins; Dim 7 and R1/R4
stay OWED consistently across the benchmark file, the fix26 notes, and
the dry-run #40 record, with the render evidence re-verified from the
files; counts, banned terms, Grok pins, and the anchor census hold. The
two minors are both B6: the generator's :383 comment still calls
skill-triggers "a live routing table", and 64 skills-table rows carry the
bare "on-request (trigger-routed)" flow string without the B6 qualifier.
Fixing them is a one-line comment reword plus qualifying the :342 flow
emission and regenerating — with the §4.2 ordering churn (6 rows, run to
run nondeterministic) accepted or fixed by sorting the flow column first.
