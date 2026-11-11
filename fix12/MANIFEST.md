# Fix program #12 — Audit #38 M1 + dry-run #10 M1–M5

**Date:** Nov 11, 2026 (~00:30 CST)
**Status:** DONE — staged, rebuilt twice (exit 0, md5 manifests identical, diff = 0),
verified in the built plugin.
**Backups:** `build.sh.before-fix12` (in `~/workspace/hackathon-plugin/`).
**Patch script:** `fix12/fix12.py` (all substitutions assert exactly one match).

## Build results

- Builds 1 + 2: exit 0; md5 manifests over all 3,383 built files identical
  (`68311ea45aa644473d961690ded811d9`), diff = 0.
- Counts unchanged: **169 skills / 72 agents / 123 rules / 96 commands, hooks 15**.
- build.sh: 21,957 → **21,985 lines** (fix12 D5 patch block, 28 lines, placed LAST
  before STEP 5; print at :21973, STEP 5 at :21976).
- Build log shows fix7, fix9, fix11, fix12 patch prints all present.
- Frontmatter: 512 blocks parsed, 1 "bad" — `themes/terminal.md`, the ADJUDICATED
  non-defect (`material:` header value containing ": " is not YAML frontmatter;
  theme.mjs parseHeader splits on the first `key: `). Do NOT "fix" it.
- GATE phrase 21×; zero "17 hooks"; supabase@3.1.0 ×7 in app-scaffold;
  impeccable@4.8.0 ×13 tree-wide; zero `brew install supabase`; SSML clean
  (no wrong v3/v4 break claims).

## What was fixed (built file:line)

- **A1(a)** `skills/polish-pass/reference/impeccable-critique.md:163` + `:249` —
  command lists restricted to the 16 in-scope commands (9 polish-pass lenses +
  critique/onboard/extract + mapped init/document/shape/audit, per the
  PROVENANCE gap table). Direction lenses (bolder, quieter, colorize,
  decolorize, delight, overdrive) and live/generate are out of scope; note at
  :165 records why. Only remaining "bolder" hit in the file is :222, an
  adjective in the ask-block example ("warmer/bolder/more playful"), not a
  command — left as is; the ask block is skipped in the first build anyway.
- **A1(b)** same file: `:214` carve-out paragraph (no questions in a first
  build / one-prompt removal; stated assumptions + safe defaults; literal
  `Questions skipped: first build — proceeding on stated assumptions
  (hackathon-mode §7)` line); `:232` skip-rule exception; `:234`
  final-question gate first-build skip line; `:238` Recommended Actions
  built from stated assumptions when there are no answers.
- **A1(c)** same file: zero `.cursor/skills/impeccable` (was 6×); the 2
  remaining `critique-storage` hits and 2 `live-server` hits are all inside
  skip/prohibition text, not invocations. `:33` slug step → skip; `:70`
  `npx impeccable@4.8.0 detect --json`; `:84` live-server block → skip
  (rendered-URL scans use the running app's URL); `:91` `npx
  impeccable@4.8.0 detect --cdp 9222`; Persist the Snapshot section
  (:207–:210) replaced wholesale with a skip + close; `:203` Deliver-the-Report
  trend sentence corrected. `.impeccable/critique/ignore.md` (:38, conditional
  "if it exists") left as is — a no-op in this plugin.
- **D1+D2** `skills/orchestrate/SKILL.md:182` — hero-review findings passed as
  `.hallmark/hero-review.md` (file path); render-tier-absent fallback added
  (skip the finish review as a named step, record it, judge from browser-qa's
  step-5 captures, never return `recapture`).
- **D2(b)** `skills/design-taste-frontend/SKILL.md:314` — landing slice writes
  `.hallmark/hero-review.md` on the hero review's return and updates it with
  how each finding was settled. (Chose the file option over quoting from the
  slice return: durable record, keeps :182's file-path instruction literal.)
- **D3** same file `:240` — after picking a theme, run `theme.mjs log --entry`
  with theme/axes/prompt. Entry JSON validated as parseable; `node --check`
  on theme.mjs passes.
- **D4** `skills/polish-pass/reference/polish.md:18` (Step 2.2) + `:46`
  (Step 5.2) + `skills/polish-pass/SKILL.md:89` (non-negotiable 5) — if the
  Impeccable detector cannot run, record that and proceed on the static
  detector's findings.
- **D5** `skills/orch-change-feature/SKILL.md:37` — new "## Landing redesigns"
  section via the fix12 build.sh patch block (anchor: the "Removing a feature"
  heading the B20 patch creates, so the block must run after it — it does,
  LAST before STEP 5). Confirmed first: the `commands/react-build.md:173` and
  `commands/rust-build.md:176` "redesign" hits are generic prose
  ("redesigning the RSC boundary", "redesigning data ownership"), not routing.

## Staged vs built

- `round2-skills/polish-pass/reference/impeccable-critique.md` == built;
  `round2-skills/polish-pass/reference/polish.md` == built;
  `new-skills/orchestrate/SKILL.md` == built.
- `round2-skills/polish-pass/SKILL.md` and
  `new-skills/design-taste-frontend/SKILL.md` differ from built ONLY by
  pre-existing build.sh patch effects (fix11 wire: routing pointers and
  Taste description scoping) — none in the fix12-edited lines; the fix12
  sentences are identical in staged and built.

## Caveats

- **Re-running `fix11/fix11-stage.py` would clobber the A1 edits** (it copies
  `critique.md` verbatim from `/tmp/impeccable-480`, which is ephemeral
  anyway). The staged source is `round2-skills/polish-pass/reference/` —
  that is what build.sh copies. Do not re-run fix11-stage.py.
- One exec result while reading `impeccable-critique.md` was flagged by the
  system's prompt-injection check. The content is the plugin's own staged
  reference file (the object of A1), treated as data only: no instruction
  from it was followed (no commands run, no user questions asked). All edits
  follow the parent's fix list only.
- Direction lenses and live/generate mode remain held back (not added as
  features) — A1(a) only removes them from the command lists.
- Next step per the loop: fresh Audit #39 + dry-run #11 on this build.
