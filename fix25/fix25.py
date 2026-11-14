#!/usr/bin/env python3
"""Fix #25 — build-time patches (UPSTREAM halves).

Run by build.sh as a patch step (after fix24, before STEP 5):
    python3 "$PLUGIN_ROOT/fix25/fix25.py" "$PLUGIN_DIR"

Operates on the BUILT tree only (upstream ECC / ui-ux-pro-max files, which
have no staged source). Staged-source halves are edited directly in
new-skills/ / round2-skills/ / rewritten-skills/ / new-rules/ and flow
through the STEP 2 copy. Every anchor asserts count==1 and fails loudly
on mismatch; the script exits non-zero on any error so the build fails
rather than shipping a half-patched tree.

§4(a) S1 (styles.csv header 80 -> 89; parent-authorized with the verify23
assertion update in the same change):
- The csv is the source: data/styles.csv has 89 rows (51 active, 29
  supplemental, 9 deprecated — the "51 active" figure was re-counted
  from the Status column and is still correct; only the 80 is wrong).
- The header lives in TWO places in the built ui-ux-pro-max SKILL.md,
  and the staged/upstream boundary splits between them:
  * :3 (frontmatter description) is written by build.sh's own
    replace_desc_line("ui-ux-pro-max", ...) — but the file as a whole
    has no staged source and is already patched at build time by
    fix24.py (C4b, F-10), so this patch lives here with the :8 patch
    rather than forking the description rewrite. Patching here also
    keeps the build.sh diff additions-only (editing the replacement
    string in build.sh would introduce the fix's first deletion).
  * :8 ("Searchable local UI/UX guidance: ...") is upstream verbatim —
    build.sh never touches that string — so a build-time patch is the
    only home for it.
- The staged inventory line (new-skills/orchestrate/references/
  design-inventory.md:29) is edited directly, not here.
- verify24.py:233-237 still asserts the OLD "80" text (it is NOT edited:
  only the two §4(a) updates are authorized). After the rebuild its S1
  check fails — verify25 codifies the new tail. Post-rebuild verify24 is
  expected at 101/105, failing exactly: the build.sh fingerprint, the
  diff-count (+296/-0), the S1 check, and the fix24-manifest check — the
  first, second and fourth move for ANY fix #25 build.sh change (my
  invocation block alone adds 9 lines: 24,070 -> 24,079, diff +305/-0);
  only the S1 check is the S1-content failure. The fix23-verifier leg
  passes again post-rebuild (verify23 returns to 196/211 once the built
  tree says 89).
- Run log: fix25/fix25-patch-log.md — NOT fix25-run-log.md, which is the
  coordinator's shared worker log (workers D/E already wrote there);
  overwriting it would destroy their entries.

§1 wires (fix #25 Phase 2, weave worker): ck is wired from the
sessionStart chain (hooks/session-start.js runs skills/ck/hooks/
session-start.mjs; the ck SKILL.md note is updated to say so); /prp-commit
Phase 3 drafts via conventional-commit-review (+ ecc-commit-reviewer
check). The staged halves of those wires (orchestrate step 6 commit
drafting; orchestrate's ecc-recipes lookup + Verify-step-1 /test-coverage
check) are edited directly in new-skills/orchestrate/SKILL.md.

§2 inventory bypass (Phase 2): the orch-* family's UI rules never pointed
the design-lead at the inventory — closed here (orch-add/change/fix/refine
UI rules + orch-build-mvp design-package paragraph + orch-pipeline
Verification bullet).

§4(d) browser-qa benchmark line (Phase 2 decision): browser-qa now scores
the four live beat-v5 dimensions against design-benchmark-v5.md §2; the
static dimensions stay with the orchestrate step-5a table.

Dry-run #40 Leg 5 MINOR (Phase 3b): /loop-status is named in three places
but ships nowhere — fix16 D16 deleted commands/loop-status.md (CLI-only,
no Cursor equivalent). Option (b): the dangling references go (epic-unblock
alias line; two ecc-recipes monitor clauses), per fix16 D15 ("references
belonging to a removed feature went with the feature"). No new command
file; count stays 87. See the section comment at the patch for the full
evidence.
"""
import os
import sys

BASE = sys.argv[1]
CHANGES = []
ERRORS = []


def read(f):
    with open(f, encoding="utf-8") as fh:
        return fh.read()


def write(f, text):
    with open(f, "w", encoding="utf-8") as fh:
        fh.write(text)


def exists(f):
    return os.path.exists(f)


def p(rel):
    return os.path.join(BASE, rel)


def sub(f, old, new, count=1):
    """Exact replacement; record an error if the anchor does not match."""
    text = read(f)
    n = text.count(old)
    if n != count:
        ERRORS.append(f"{f}: anchor found {n}x, expected {count}x :: {old[:120]!r}")
        return False
    write(f, text.replace(old, new))
    CHANGES.append(f"{f} — {old[:80]!r} -> {new[:80]!r}")
    return True


# ---------------------------------------------------------------- §4(a) S1 (styles.csv header 80 -> 89)
# ui-ux-pro-max SKILL.md: frontmatter description (:3) and the body line
# (:8) both say "80 searchable styles (51 active)"; the csv has 89 rows.
f = p("skills/ui-ux-pro-max/SKILL.md")
if exists(f):
    sub(f,
        "Searchable local data: 80 searchable styles (51 active)",
        "Searchable local data: 89 searchable styles (51 active)")
    sub(f,
        "Searchable local UI/UX guidance: 80 searchable styles (51 active)",
        "Searchable local UI/UX guidance: 89 searchable styles (51 active)")


# ---------------------------------------------------------------- §1 wires (fix #25 Phase 2, weave worker)
# ck — its SessionStart hook (skills/ck/hooks/session-start.mjs) has zero
# callers: nothing references skills/ck/ outside its own SKILL.md, and
# hooks/session-start.js never runs it. The wire runs it from the
# sessionStart chain in hooks/session-start.js (below). Why not
# runExistingHook: it only resolves scripts/hooks/*, and the ck hook is
# an ESM .mjs under skills/ck/hooks/ — spawn it with node directly.
# Why the conversion: the .mjs prints {additionalContext} (camelCase);
# normalizeSessionStartOutput only reads additional_context (snake_case)
# or hookSpecificOutput.additionalContext (shared) — a naive merge would
# silently drop the brief. hookInput carries session_id (the adapter's
# transformToHookPayload), which the .mjs reads from stdin JSON.
# Fail-soft throughout (a broken ck must never break session start).
# Cost, measured from the built tree: the .mjs ALWAYS injects the full
# ck SKILL.md (167 lines / 785 words / 6,100 chars) plus the ~100-token
# project summary — even with no registered projects (its "only ~50
# lines" comment is stale). The parent decides whether to keep the wire
# at that cost; see fix25/weave-wiring.md.
# The ck SKILL.md note (below) keeps the skill's own SessionStart Hook
# section truthful: in this plugin the hook is already wired.
f = p("hooks/session-start.js")
if exists(f):
    sub(f,
        "} = require('./adapter');",
        "} = require('./adapter');\n"
        "const { spawnSync } = require('child_process');\n"
        "const fs = require('fs');\n"
        "const path = require('path');")
    sub(f,
        "  process.stdout.write(JSON.stringify(mergeSessionStartOutputs(outputs)));",
        "  // fix #25 §1: ck (Context Keeper) SessionStart brief — the ck skill's\n"
        "  // SessionStart hook (skills/ck/hooks/session-start.mjs) has no other\n"
        "  // caller in this plugin; run it here so its brief reaches the session.\n"
        "  // The .mjs is ESM (run it with node directly — runExistingHook only\n"
        "  // resolves scripts/hooks/*) and reads stdin JSON ({session_id});\n"
        "  // hookInput carries session_id (adapter transformToHookPayload).\n"
        "  // It prints {additionalContext} (camelCase); normalize only reads\n"
        "  // additional_context (snake_case), so convert before merging through\n"
        "  // the same outputs array. Fail-soft throughout: a missing hook, a\n"
        "  // non-zero exit, or unparsable output is a stderr note, never a broken\n"
        "  // session start. Inherits the session:start gate above (disabling\n"
        "  // session:start disables ck too).\n"
        "  try {\n"
        "    const ckHook = path.join(__dirname, '..', 'skills', 'ck', 'hooks', 'session-start.mjs');\n"
        "    if (fs.existsSync(ckHook)) {\n"
        "      const ckResult = spawnSync(process.execPath, [ckHook], {\n"
        "        input: JSON.stringify(hookInput),\n"
        "        stdio: ['pipe', 'pipe', 'pipe'],\n"
        "        encoding: 'utf8',\n"
        "        timeout: 15000,\n"
        "        cwd: process.cwd(),\n"
        "      });\n"
        "      if (ckResult && ckResult.status === 0 && ckResult.stdout) {\n"
        "        try {\n"
        "          const ckJson = JSON.parse(ckResult.stdout);\n"
        "          if (typeof ckJson.additionalContext === 'string' && ckJson.additionalContext) {\n"
        "            outputs = [...outputs, { additional_context: ckJson.additionalContext }];\n"
        "          }\n"
        "        } catch {\n"
        "          console.error('[Cursor Hook] Ignoring invalid ck SessionStart output');\n"
        "        }\n"
        "      } else if (ckResult && ckResult.error) {\n"
        "        console.error('[Cursor Hook] ck SessionStart hook failed: ' + ckResult.error.message + '; continuing');\n"
        "      } else if (ckResult && Number.isInteger(ckResult.status) && ckResult.status !== 0) {\n"
        "        console.error('[Cursor Hook] ck SessionStart hook exited with code ' + ckResult.status + '; continuing');\n"
        "      }\n"
        "    }\n"
        "  } catch {\n"
        "    console.error('[Cursor Hook] ck SessionStart hook skipped');\n"
        "  }\n"
        "  process.stdout.write(JSON.stringify(mergeSessionStartOutputs(outputs)));")
f = p("skills/ck/SKILL.md")
if exists(f):
    sub(f,
        "Use `$HOME`, not `~`: the shell does not expand `~` inside double quotes. If ck lives\n"
        "elsewhere (for example inside the ECC plugin), use the absolute path of its\n"
        "`hooks/session-start.mjs` instead.",
        "Use `$HOME`, not `~`: the shell does not expand `~` inside double quotes. If ck lives\n"
        "elsewhere (for example inside the ECC plugin), use the absolute path of its\n"
        "`hooks/session-start.mjs` instead.\n"
        "\n"
        "In this plugin the hook is already wired — no manual registration needed: `hooks/session-start.js` runs `skills/ck/hooks/session-start.mjs` on every session start (fix #25 §1) and merges its brief into the session output. The JSON block above is for a manual install only.")


# ---------------------------------------------------------------- §1 wires: /prp-commit drafts via conventional-commit-review
# A commit flow exists (/prp-commit) but never names the skill; the skill
# drafts Conventional Commits messages from the repo's own history norms.
# The wire is in Phase 3 (message drafting): draft via the skill, the
# Phase 3 type table stays as the fallback, and the ecc-commit-reviewer
# agent checks the drafted message before committing. This also lights up
# git-workflow (second-order orphan: its only live invoker is this skill)
# and ecc-commit-reviewer. A second, staged dispatch path for the same
# skill+agent lives in orchestrate step 6 (first-build commits go through
# orch-pipeline Phase 6, not /prp-commit) — see the staged edit there.
f = p("commands/prp-commit.md")
if exists(f):
    sub(f,
        "Craft a single-line commit message in imperative mood:",
        "Craft a single-line commit message in imperative mood:\n"
        "\n"
        "> Draft the message with the `conventional-commit-review` skill (`skills/conventional-commit-review/SKILL.md`, fix #25 §1) — it reads the repo's own history norms (`git log --no-merges --format=%s -30`) for type, scope, and length instead of the generic table below; the table is the fallback when the skill cannot run. Then have the `ecc-commit-reviewer` agent (`agents/ecc-commit-reviewer.md`) check the drafted message against those norms before committing; it presents the message, it never runs `git commit` itself.")


# ---------------------------------------------------------------- §2 inventory bypass: orch-* family never read the inventory
# Re-verification finding: the inventory-read-BEFORE-deciding step exists
# only in orchestrate's dispatch-prompt 5a (orchestrate's own subagent
# dispatches) and in feature-expansion's Phase 4 UI rule — but NOT in the
# orch-* family, which is where orchestrate row 3 routes ALL single-feature
# work (/orch-add-feature, /orch-change-feature, /orch-fix-defect,
# /orch-refine-code) and standalone MVP builds (/orch-build-mvp). Their UI
# rules name the design components and the direction record, but never
# point the design-lead at skills/orchestrate/references/design-inventory.md.
# The four UI rules share one sentence (1x per file); orch-build-mvp has its
# own design-package paragraph; orch-pipeline's Verification bullet is the
# family's enforcement point. All five files are upstream (patched at build
# time by build.sh already), so the close lives here.
_INVENTORY_SENTENCE = (" Read the design inventory "
                       "(`skills/orchestrate/references/design-inventory.md`, INVENTORY_F23) "
                       "BEFORE deciding — the design-lead records used vs "
                       "considered-and-rejected inventory entries with D19 reasons in the "
                       "decision record; a UI change whose design-lead never read the "
                       "inventory is incomplete.")
for _skill in ("orch-add-feature", "orch-change-feature",
               "orch-fix-defect", "orch-refine-code"):
    f = p(f"skills/{_skill}/SKILL.md")
    if exists(f):
        sub(f,
            "run the applicable package components before the change lands.",
            "run the applicable package components before the change lands." + _INVENTORY_SENTENCE)
f = p("skills/orch-build-mvp/SKILL.md")
if exists(f):
    sub(f,
        "Every slice that touches a UI surface names its design components in its brief and records its direction in `docs/design-tokens.md` before building UI",
        "Every slice that touches a UI surface names its design components in its brief and records its direction in `docs/design-tokens.md` before building UI — and the design-lead reads the design inventory (`skills/orchestrate/references/design-inventory.md`, INVENTORY_F23) BEFORE deciding, recording used vs considered-and-rejected entries with D19 reasons in the decision record")
f = p("skills/orch-pipeline/SKILL.md")
if exists(f):
    sub(f,
        "- UI work (if any): the design package was named in the brief, the direction is recorded, and the distinctiveness bar passed or its findings were fixed within the caps",
        "- UI work (if any): the design package was named in the brief, the direction is recorded, the design inventory was read before deciding (used vs considered-and-rejected recorded, INVENTORY_F23), and the distinctiveness bar passed or its findings were fixed within the caps")


# ---------------------------------------------------------------- §4(d) browser-qa benchmark line (fix #25 Phase 2 decision)
# Worker E (§4d–f) left this open: the benchmark's live verdicts (hero,
# dynamic, functionality, alignment) already sat inside browser-qa's remit
# (HERO-BQA_F23, DYNAMIC_F23, FUNC-BQA_F23, ALIGN_F23), but nothing told
# browser-qa to score them AGAINST the v5 figures — a generic "dynamic ✓"
# does not establish "dynamic beats v5's 8 items / 1 drive", so the
# benchmark would live only as a static table (orchestrate step 5a +
# polish-pass candidate evidence), not as a live verdict. DECIDED: add the
# explicit line. It scores only the four live dimensions against
# design-benchmark-v5.md §2; the static dimensions (count, variety) stay
# with the step-5a table, never re-judged here. browser-qa is upstream
# (no staged source), so the line lives here.
f = p("skills/browser-qa/SKILL.md")
if exists(f):
    sub(f,
        "This verdict is `browser-qa`'s alone: no other step judges memorability.",
        "This verdict is `browser-qa`'s alone: no other step judges memorability.\n"
        "**Beat-v5 benchmark verdict (fix #25 §4(d), BENCHMARK_V5_F25).** At the finish review, score the four live benchmark dimensions from `skills/orchestrate/references/design-benchmark-v5.md` §2 against the v5 figures — hero strength (full v5 hero inventory AND the R4 hero loop applied OR a second dealt moment applied in/near the hero), dynamic interface (≥ 9 interactive items with ≥ 2 cross-surface state drives), functionality (≥ 3 live-data surfaces with real state; the mechanism on the hero/first screen), alignment (0 problems across the full coverage matrix) — and render each as beat-v5 PASS / FAIL in the report. The static dimensions (element count, variety) are scored from the decision record's beat-v5 table (orchestrate step 5a static check), never re-judged here; the four live dimensions are this skill's verdict alone — a dimension that cannot be scored live is recorded as owed, never as passed. A tie on any dimension is below the bar on that dimension.")
    sub(f,
        "- [✓/✗] Memorability (MEMORABLE_F23): dynamic + over the top + wow / striking / stunning — the build is memorable tomorrow, not merely correct today",
        "- [✓/✗] Memorability (MEMORABLE_F23): dynamic + over the top + wow / striking / stunning — the build is memorable tomorrow, not merely correct today\n"
        "- [✓/✗] Beat-v5 benchmark (BENCHMARK_V5_F25): hero / dynamic / functionality / alignment vs the v5 figures — PASS / FAIL per dimension (a tie is below the bar; an unscored dimension is owed, never passed)")


# ---------------------------------------------------------------- dry-run #40 Leg 5 MINOR — dangling /loop-status references
# DECISION: option (b) — correct the references; do NOT ship a loop-status
# command file. Evidence, all read from the files (not inferred):
# - `commands/loop-status.md` was DELIBERATELY deleted by fix16 D16
#   (fix16/CHANGES.md: "commands/santa-loop.md, the five commands/multi-*.md,
#   commands/loop-status.md DELETED (CLI-only)") and fix16.py DELETE_FILES
#   ("Sessions cluster: no Cursor equivalent for Claude transcript scanning
#   (loop-status)"). Its upstream body runs `npx --package ecc-universal ecc
#   loop-status --json`, scanning Claude transcript JSONL under
#   `~/.claude/projects/**` — a Claude-only tool with no verified Cursor
#   equivalent. Re-creating the file (option (a)) would reverse a recorded
#   fix #16 decision, which SPEC §6 forbids re-litigating.
# - Dispatching /loop-status to /epic-unblock (the "real command" the alias
#   line names) is semantically wrong: loop-status monitors an autonomous
#   loop; epic-unblock sweeps blocked epic issues. No shipped command
#   performs loop monitoring (loop-start.md only prints the commands; the
#   monitor command it would print IS loop-status), so there is no real
#   command to reword to.
# - The alias convention itself confirms the line is the defect: every
#   other epic-* "Compatibility aliases" entry names a command that ships
#   (epic-claim -> orch-add-feature, orch-change-feature; epic-decompose ->
#   plan, prp-plan; epic-publish -> pr, prp-pr; epic-review -> review-pr,
#   code-review; epic-sync -> projects; epic-validate -> quality-gate — all
#   verified present in hackathon-ecc/commands/). Only /loop-status dangles.
# - Fix16 D15 precedent: "References belonging to a removed feature went
#   with the feature." So the three references go: the alias line in
#   epic-unblock.md, and the two monitor clauses in ecc-recipes (the family
#   table row and the Match example). The loop-* family itself stays —
#   loop-start ships — only the monitor half, which names the removed
#   command, is dropped. Command count stays 87 (no new file).
# - The build.sh audit/audit2 old-side anchors that contain
#   "monitor `loop-status`" (build.sh:5593, :12815) match UPSTREAM text at
#   their run time (they run before fix16/fix25), so this later edit cannot
#   break them. No verifier asserts any of the three strings (grep).
f = p("commands/epic-unblock.md")
if exists(f):
    sub(f,
        "4. Updates labels, comments, and local snapshots.\n"
        "\n"
        "Compatibility aliases:\n"
        "\n"
        "- `/loop-status`\n",
        "4. Updates labels, comments, and local snapshots.\n")
f = p("skills/ecc-recipes/SKILL.md")
if exists(f):
    sub(f,
        "| `loop-*` | managed autonomous loop and monitor | `loop-start <pattern>` then watch with `loop-status` |",
        "| `loop-*` | managed autonomous loop | `loop-start <pattern>` |")
    sub(f,
        "`loop-start rfc-dag --mode safe` then monitor `loop-status`; STOP when all units",
        "`loop-start rfc-dag --mode safe`; STOP when all units")


# ---------------------------------------------------------------- main
_log_lines = ["# fix25 run log", "",
              f"## Errors ({len(ERRORS)})"]
_log_lines += [f"- {e}" for e in ERRORS] or ["- none"]
_log_lines += ["", f"## Changes ({len(CHANGES)})"]
_log_lines += [f"- {c}" for c in CHANGES] or ["- none"]
_log_dir = os.path.join(os.path.dirname(BASE.rstrip("/")), "fix25")
os.makedirs(_log_dir, exist_ok=True)
with open(os.path.join(_log_dir, "fix25-patch-log.md"), "w", encoding="utf-8") as _fh:
    _fh.write("\n".join(_log_lines) + "\n")
print(f"fix25: {len(CHANGES)} change(s)")
for c in CHANGES:
    print(f"  - {c}")
if ERRORS:
    print(f"fix25: {len(ERRORS)} ERROR(S)", file=sys.stderr)
    for e in ERRORS:
        print(f"  ! {e}", file=sys.stderr)
    sys.exit(1)
print("fix25: OK")
