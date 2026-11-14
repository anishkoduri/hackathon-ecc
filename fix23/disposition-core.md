# Fix #23 CORE disposition — THE CORE (Anish, Nov 12), memorability above F6

Worker W-CORE. Scope: SPEC §1 THE CORE only — the governing bar for all
of fix #23. §1–§6 + §9 rules are NOT restated here; they are elevated by
cross-reference. No bundle, no commit, no push. `build.sh` NOT run, NOT
edited (still 23,984 lines, md5 `df7e52f8aa33605c952f58dfea9801fd` —
re-checked after this worker's work). The built tree was read-only for
anchor verification. `fix11/fix11-stage.py` not re-run. Prior verifiers
not edited. `~/workspace/cursor-skills/less-flat-ui` not touched.
No /demo or DEMOGATE token touched. No staged skill file edited directly
by this worker — orchestrate/polish-pass lines are payload files for
integration to insert.

## Token family

**MEMORABLE_F23** — one consistent token family, used everywhere in this
worker's output (orch lines, polish lines, both runtime subs, this
disposition). The alternative CORE_F23 was not used.

## Files changed / created by W-CORE

| File | Change |
|---|---|
| `fix23/apply-core.py` | NEW — inserts the CORE runtime-patch block into build.sh before `# STEP 5 — Counts` (integration runs it; W-CORE did NOT run it) |
| `fix23/orch-lines-core.py` | NEW — one constant `ORCH_LINES_CORE` with the exact orchestrate design-package-step lines (memorability elevation of AMBITION_F23); integration inserts it |
| `fix23/polish-lines-core.py` | NEW — one constant `POLISH_LINES_CORE` with the exact polish-pass memorability-candidates line; integration inserts it |
| `fix23/disposition-core.md` | This file |

## Per-item placement table

Status: new = W-CORE wrote new text; pointer = cross-referenced, not
restated; covered = already present, unchanged.

### THE CORE (SPEC §1)

| SPEC item | Placement (file + anchor token) | Status |
|---|---|---|
| Dynamic + over the top + wow + striking + stunning + above all MEMORABLE is the core — the governing bar, above F6's impressive | `fix23/orch-lines-core.py` `ORCH_LINES_CORE` (MEMORABLE_F23), to be inserted in staged `new-skills/orchestrate/SKILL.md` step 3 after the AMBITION_F23 paragraph (line 68); `fix23/apply-core.py` sub MEMORABLE-BQA-01 (MEMORABLE_F23) | new |
| A build the user forgets the next day fails, however rule-correct | Orch lines (MEMORABLE_F23); MEMORABLE-BQA-01 add-text (MEMORABLE_F23); MEMORABLE-BQA-02 report row (MEMORABLE_F23) | new |
| Browser-qa judges memorability as the TOP criterion — dynamic (moves and responds), over the top (beyond adequate in ambition, elements, motion), wow / striking / stunning (hits on first sight and on use) | MEMORABLE-BQA-01 (MEMORABLE_F23) — visual-loop verdict paragraph; orch lines state it as the finish-review criterion (MEMORABLE_F23) | new |
| "Over the top" is ambition and impact, NOT loudness for its own sake — "more, not bolder" still governs styling (do not just crank weight, color, or size) | Orch lines (MEMORABLE_F23); MEMORABLE-BQA-01 (MEMORABLE_F23); polish lines (MEMORABLE_F23) | new |
| A build can be over the top and quiet in palette; it cannot be forgettable | Orch lines (MEMORABLE_F23); MEMORABLE-BQA-01 (MEMORABLE_F23); polish lines (quiet-palette build with a strong moment is not flagged for being quiet) | new |
| Updated F6 bullet: F6 (impressive is the governing bar) is now the PRIMARY gate — browser-qa judges impressive AND ambitious, not just rule-correct; a rule-correct but unambitious design fails | Staged `new-skills/orchestrate/SKILL.md:68` (AMBITION_F23, step 3) + staged line 147 (AMBITION_F23, step-6 F6-primary-gate extension) — both already state this (W1); the CORE elevation cross-references them by token, it does not rewrite them | pointer (covered by W1, elevated here) |
| Memorability sits ABOVE F6: impressive is the floor, memorable is the bar | Orch lines (MEMORABLE_F23); MEMORABLE-BQA-01 (MEMORABLE_F23) | new |
| The governing bar applies across the sections already implemented (§1–§6, §9): the ambition bar, the motion bar, the hero bar, and the browser-qa verdicts all answer to it | Orch lines cross-reference AMBITION_F23, MOTION_F23, HERO_F23, FUNC_F23, DYNAMIC_F23 without restating them (MEMORABLE_F23); MEMORABLE-BQA-01 cross-references HERO-BQA_F23 and the F6/impressive verdicts (MEMORABLE_F23) | pointer |
| Memorability as a polish-pass consideration (candidate evidence only) | `fix23/polish-lines-core.py` `POLISH_LINES_CORE` (MEMORABLE_F23), to be inserted in staged `round2-skills/polish-pass/SKILL.md` step 5 trailing paragraph (line 101), after the dynamic-story sentence | new |
| THE INVENTORY — cross-reference only | The inventory is a catalog, not a rule surface: no inventory-file edit. The ambition bar it serves (AMBITION_F23) is elevated by the orch lines, and the orch lines cite the used vs considered-and-rejected inventory record alongside the memorable-moment record | pointer |
| Frozen D19_RULE text | NOT rewritten anywhere (verified: this worker wrote no D19-rule text; the orch constant carries a fresh seven-dimension D19 parenthetical in the S9 style, not a rewrite) | covered (untouched) |

### Runtime patches (`fix23/apply-core.py` → build.sh block before `# STEP 5 — Counts`)

Each sub is (id, rel-path, old-anchor, add-text, mode). All anchors verified
count==1 against the CURRENT (post-§9) built tree by grep before the script
was written, and re-verified by extracting the subs from `apply-core.py`
and counting (see Verification). The block re-asserts count==1 at build
time and fails loudly. Idempotency guard: the script refuses if its marker
comment (`# --- fix23 CORE: memorability verdict (fix #23 §1, MEMORABLE_F23) ---`)
is already in build.sh. The script was NOT run (integration runs it).
`py_compile` passed; the block's inner Python compiles; marker absent from
build.sh; `# STEP 5 — Counts` count==1.

| Sub | Target (built tree) | Anchor (count==1) | Mode | Token |
|---|---|---|---|---|
| MEMORABLE-BQA-01 | `skills/browser-qa/SKILL.md` | `This verdict is \`browser-qa\`'s alone: no other step judges the hero.` (hero verdict closing sentence, W3's HERO-BQA_F23 add-text) | after | MEMORABLE_F23 |
| MEMORABLE-BQA-02 | `skills/browser-qa/SKILL.md` | `- [✓/✗] Dynamic (DYNAMIC_F23): controls respond immediately; every state change choreographed (motion present); live state, not frozen mock content` (Dynamic report row, §9 DYNAMIC-BQA-02 add-text) | after | MEMORABLE_F23 |

Anchor-collision check: neither anchor string was used as an anchor by
any earlier sub (BQA-TYPEAUDIT: distinctiveness sentence;
HERO-BQA_F23: "Never claim visual verification..." sentence;
FUNC-BQA_F23: Phase 3 step 4; ALIGN_F23-A–E: Phase 3 heading / step 1 /
step 3 / verdict line / Visual example row; DYNAMIC-BQA-01: Phase 2
step-5 block; DYNAMIC-BQA-02: Interactions auth-flow row). The two
anchors are FRESH strings. Note: MEMORABLE-BQA-02's anchor is the
§9 block's own add-text — this is a documented dependency, not a
collision: the CORE block is inserted into build.sh AFTER the §9 block,
so at build time the §9 block has already run and the Dynamic row
exists (it is already present in the current built tree, count==1).
MEMORABLE-BQA-01's anchor appears 0× in build.sh only because the W3
block stores it repr-escaped (`browser-qa\'s`); it is count==1 in the
built-tree file, which is what the runtime assert checks.

### Staged insertion anchors (for integration)

| Payload | Target staged file | Anchor (count==1, verified) | Mode |
|---|---|---|---|
| `ORCH_LINES_CORE` | `new-skills/orchestrate/SKILL.md` step 3 | AMBITION_F23 paragraph closing sentence (staged line 68): "F6 (impressive is the governing bar) is the PRIMARY gate: browser-qa judges impressive AND ambitious, not just rule-correct — a rule-correct but unambitious design fails at the finish review." | after (new paragraph, before the MOTION_F23 paragraph) |
| `POLISH_LINES_CORE` | `round2-skills/polish-pass/SKILL.md` step 5 trailing paragraph (line 101) | Dynamic-story closing sentence: "…whether the control actually responds and the change is actually choreographed is `browser-qa`'s live check alone (DYNAMIC_F23)." | after (new sentence, same paragraph; constant starts with a leading space) |

Note: W1's `<!-- F23-ORCHESTRATE-EXTENSIONS: ... -->` anchor comment is
no longer in the staged orchestrate file (integration consumed it for
the W2/W3/W4 lines) — the AMBITION_F23 closing sentence is the
replacement anchor, same as orch-lines-s9.py did with the HERO/FUNC
paragraph.

## Anchors that did NOT resolve count==1

None. Every anchor above resolved count==1 (browser-qa ×2, orchestrate
×1, polish-pass ×1). One candidate was REJECTED before use: the Output
Format row `- [✗] Hero section overflows on 375px viewport` is
count==1 but sits inside W4's ALIGN_F23-E anchor string
(`### Visual\n- [✗] Hero section overflows on 375px viewport`), so
it was not used — MEMORABLE-BQA-02 uses the Dynamic report row instead.

## Verification done by W-CORE

- Baseline re-checked: `build.sh` 23,984 lines, md5
  `df7e52f8aa33605c952f58dfea9801fd` — unchanged after W-CORE's work.
- `py_compile` OK for all three new files; the rendered block's inner
  Python compiles OK.
- Sub anchors re-verified by extracting SUBS from `apply-core.py` and
  counting against the current built tree: MEMORABLE-BQA-01 = 1,
  MEMORABLE-BQA-02 = 1.
- Orch anchor re-verified count==1 in the staged orchestrate file;
  polish anchor re-verified count==1 in the staged polish-pass file.
- Banned terms (claude/codex/anthropic/opus/sonnet/haiku/composer-2.5,
  case-insensitive): 0 in all three new files (asserted programmatically
  on every add-text and constant).
- Grok pins: this worker wrote no model pins at all (grep exit 1 for
  `grok-4.7-high` / `grok-4.6-high-fast` in the three files) — nothing
  to pin, and no bare `grok-4.6-high-fast`.
- MEMORABLE_F23 occurrences: `apply-core.py` 5, `orch-lines-core.py` 2,
  `polish-lines-core.py` 3; 0 occurrences anywhere else in the tree
  before integration (grep).
- Orch constant carries all seven D19 dimensions (Motion / Theme /
  Texture / Visuals / Techniques / Colors / Depth) — asserted.
- "More, not bolder" stands, anti-derivative stands (not re-litigated,
  cited only where the distinction requires it), browser-qa remains
  the sole verdict executor (orch lines say the verdict is browser-qa's
  at the finish review; polish lines say candidate evidence, never a
  verdict).

## What W-CORE could NOT verify / open items for integration

- `apply-core.py` was NOT run per instructions, so the block's insertion
  into `build.sh` and the resulting built tree are unverified until
  integration runs it (the block's own asserts are the check).
- `orch-lines-core.py` / `polish-lines-core.py` were NOT inserted into
  the staged skill files (integration inserts them); their effect on the
  built tree is unverified until the integration rebuild.
- MEMORABLE-BQA-02 depends on the §9 block having run first at build
  time (its anchor is the Dynamic report row DYNAMIC-BQA-02 inserts).
  This holds as long as the CORE block stays AFTER the §9 block in
  build.sh — integration must preserve that order (both blocks sit
  before `# STEP 5 — Counts`, in insertion order).
