#!/usr/bin/env python3
"""Fix #33 — unpin the orchestrator: it runs on the model selected in this chat.

Run by build.sh as a patch step (in fix #30's slot: after fix29.py,
before fix31.py):
    python3 "$PLUGIN_ROOT/fix33/fix33.py" "$PLUGIN_DIR"

Operates on the BUILT tree only. Replaces the remaining orchestrator-pin
text (grok-4.7-high / "Grok 4.7 High") with model-agnostic wording
("the model selected in this chat" / `model: inherit`), then asserts the
result exactly. Exits non-zero on any error so the build fails rather
than shipping a half-unpinned tree.

Why this slot, and what is already gone before this script runs: the
staged sources were unpinned in the staged weave (fix33/weave33.py —
orchestrate SKILL.md, deep-reasoner.md, agent-TEMPLATE.md,
hackathon-mode.mdc, README.md, LIVE_SMOKE_TEST.md), and the build.sh
opus mapping now yields `model: inherit` for the opus-tier agents, so
those pin mentions never reach the built tree. What remains for this
script is the pin text written by build.sh heredocs and by fix16/fix24/
fix29 (which anchor on the old pin text — editing their sources would
break their builds, so the replacement happens here, fix #30 pattern).

Pre-state census (MEASURED Nov 17, 2026 on the real fix33 build output,
build run 2 — the first derivation was wrong and is corrected by D33-16;
any drift fails loudly and no file is written):
  grok-4.7-high             x20  (README 1, ecc-gan-planner 2, astra-review 3,
                                  gan-build 2, gan-design 3, model-route 2,
                                  common-agents 1, common-performance 2,
                                  agent.schema.json 1, gan-style-harness 3,
                                  orch-* 0 — round 33d, B-M2/D33-31: build.sh
                                  fix13-A now writes the model-agnostic
                                  design-role wording, so no scrub tuple
                                  remains for the orch-* skills)
  "Grok 4.7 High"           x7   (5 replaceable: README 3 in one line,
                                  astra-review 1, pi-core.json 1; PLUS the 2
                                  strategic-compact keeps, which are in High
                                  form now that fix30's rename no longer runs)
  grok-4.7-extra-high       x0   (fix #30 retired — no rename runs)
  "Grok 4.7 Extra High"     x0   (nothing renames to it anymore)
  cursor-grok-4.6-high-fast x71  (70 + 1: the fix33 staged weave added a fast
                                  mention in the orchestrate L93 picker note)
  bare grok-4.6-high-fast   x0

Round 33c (Nov 17, 2026): the MODEL check is re-sequenced before grill-me in the STAGED orchestrate skill (the staged weave is the mechanism there — this script does not touch it, but the MODELSEL_F33 guard below now names the pre-grill block), and the guardrail is woven into the 9 direct command entry points (10 new replacements: gan-build, gan-design, astra-review, orch-pipeline Step 0, the five orch-* command pointers, the orchestrate.md command pointer). Change count rises 31 → 41.

Round 33d (Nov 17, 2026): audit #111-B (6 blocking bypasses B-B1..B-B6 +
minors B-M1/B-M2/B-M3) and audit #111-A (A-M1/A-M2). The guardrail is woven
at each bypass itself: the full MODEL check at the top of the
orch-change-feature `Removing a feature` section (the section never invokes
the engine), orch-build-mvp step 1 runs orch-pipeline Step 0 first (Step 0
is the classifier section, not a phase — D33-22's 'each skill's step 1 runs
the engine' was false for orch-build-mvp), and the full check at the entries
of commands/feature-dev.md and commands/react-build.md; the grill-me and
feature-expansion skills carry the check at their entries via their staged
sources (the trigger paths load the skills directly). B-M2 moves the
design-role unpin into build.sh fix13-A itself, so the five orch-* scrub
tuples below are removed and the pre-state census drops ID 25 → 20 (PROSE
x7, FAST x71 unchanged). Change count stays 41 (35 tuples: −5 scrub + 5
guardrail).

Round 33e (Nov 17, 2026): audit #112-B (1 blocking bypass B-N1) + audit
#112-A (2 minor A-M1/A-M2) + sweep #55 (1 minor S-M1, same as A-M1). B-N1:
the trigger-routed design-taste-frontend skill routes a full-page redesign
to the Hallmark redesign flow, whose >3-page fan-out dispatches one factory
drone per page with no MODEL check anywhere on the path — closed by the full
MODEL check at the skill's entry via its staged source (D33-36; no tuple
here, same mechanism as B-B5/B-B6). A-M1/S-M1: the stale "fast 70" prose
parentheticals corrected to 71 (D33-38; DECISION-33-4 string above). A-M2:
SPEC §3(h) reworded (D33-39; no script change). Verifier gains 6 B-N1 §16n
checks (D33-37); the scan r4/r5 regression site for this skill moves
444 → 446 (the +2-line insertion). Change count stays 41; DECISIONS
35 → 39.

Post-state: old ID x0, old prose x2 (the strategic-compact keeps ONLY),
new ID x0, new prose x0, fast x72 (71 pre-existing + 1 added by the schema
description replacement, D33-17 — the description now names the fast tier),
bare x0. `model: inherit` present in agents/deep-reasoner.md,
agents/ecc-architect.md, agents/ecc-healthcare-reviewer.md and
agents/ecc-spec-miner.md.

Mechanism note (Cursor docs, Subagents — https://cursor.com/docs/subagents,
read Nov 17, 2026): the `model` frontmatter field takes `inherit`
(default — "Uses the same model as the parent agent") or a specific
model ID; custom subagents default to `inherit`. The model picker,
including Auto, applies to the parent agent. `inherit` is therefore the
correct frontmatter value for the chat-model tier — not a deletion (a
missing line is ambiguous: inherit, or an oversight?).

Guard (D33-14, fix32 DECISION-32-14/15 lesson): the whole executable
body lives in main() under `if __name__ == "__main__":`, and module
level assigns BASE = '' and ROOT = ''. Importing this module must never
execute the census or overwrite the patch log.
"""
import os
import sys

BASE = ""  # D33-14: set from sys.argv[1] inside main() only;
ROOT = ""  # importing this module must leave BASE '' and touch nothing.
CHANGES = []
ERRORS = []
OWED = []
DECISIONS = []

OLD_ID = "grok-4.7-high"
OLD_PROSE = "Grok 4.7 High"
NEW_ID = "grok-4.7-extra-high"
NEW_PROSE = "Grok 4.7 Extra High"
FAST_ID = "cursor-grok-4.6-high-fast"
FAST_BARE = "grok-4.6-high-fast"
KEEP_FILE = "skills/strategic-compact/SKILL.md"

# Exact pre-state census (see docstring). Any drift fails loudly.
# Keeps are OLD_PROSE ("Grok 4.7 High") x2 in strategic-compact — fix30's
# rename no longer runs, so they are never rewritten to Extra High (D33-16).
EXPECT = {
    OLD_ID: 20,
    OLD_PROSE: 7,
    FAST_ID: 71,
    NEW_ID: 0,
    NEW_PROSE: 0,
}

SKIP_DIRS = {"node_modules", ".git"}


def p(rel):
    return os.path.join(BASE, rel)


def exists(f):
    return os.path.exists(f)


def read(f):
    with open(f, encoding="utf-8") as fh:
        return fh.read()


def write(f, text):
    with open(f, "w", encoding="utf-8") as fh:
        fh.write(text)


def _walk_files():
    """All files under BASE except SKIP_DIRS, as (path, text-or-None).

    _dirs is sorted (D33-12): fix30.py did not sort it, so its per-file
    log lines could come out in a different order run to run (same changes
    as a set) and the patch log was not byte-stable across rebuilds.
    A file that is not valid UTF-8 is returned with text=None; the caller
    byte-checks it for pin text instead of silently skipping it.
    """
    for _root, _dirs, _files in os.walk(BASE):
        _dirs[:] = sorted(d for d in _dirs if d not in SKIP_DIRS)
        for _name in sorted(_files):
            _path = os.path.join(_root, _name)
            try:
                with open(_path, encoding="utf-8") as _fh:
                    yield _path, _fh.read()
            except (UnicodeDecodeError, OSError):
                yield _path, None


def _count_in(text):
    return {
        OLD_ID: text.count(OLD_ID),
        OLD_PROSE: text.count(OLD_PROSE),
        FAST_ID: text.count(FAST_ID),
        NEW_ID: text.count(NEW_ID),
        NEW_PROSE: text.count(NEW_PROSE),
    }


def _bare_fast_count(text):
    """Occurrences of grok-4.6-high-fast NOT preceded by 'cursor-'."""
    _n = 0
    _i = 0
    while True:
        _i = text.find(FAST_BARE, _i)
        if _i < 0:
            return _n
        if not text[max(0, _i - 7):_i].endswith("cursor-"):
            _n += 1
        _i += len(FAST_BARE)


def _block(text, marker):
    _i = text.find(marker)
    if _i < 0:
        return None
    _j = text.find("\n", _i)
    return text[_i:_j] if _j > _i else text[_i:]


# ---------------------------------------------------------------- replacements
# (relpath, old, new, expected-count-in-file). Exact anchors, one site
# each — no blind global replace: frontmatter needs `inherit`, prose
# needs wording, and the schema enum needs a list edit.
REPLACEMENTS = [
    ("README.md",
     "- **Before the first build — Grok 4.7 High in the model picker:** select Grok 4.7 High in Cursor's model picker before the first build; see the picker note in `skills/orchestrate/SKILL.md` step 4. Task agents pin to Grok 4.6 High Fast (`cursor-grok-4.6-high-fast`); the orchestrator and the design/implementation roles pin to Grok 4.7 High (`grok-4.7-high`).",
     "- **Before the first build — select a specific model in the model picker:** select a specific model in Cursor's model picker before the first build; see the picker note in `skills/orchestrate/SKILL.md` step 4. Task agents pin to Grok 4.6 High Fast (`cursor-grok-4.6-high-fast`); the orchestrator and the design/implementation roles run on the model selected in this chat.",
     1),
    ("agents/ecc-gan-planner.md",
     "(model grok-4.7-high)",
     "(model: the model selected in this chat)",
     1),
    ("agents/ecc-gan-planner.md",
     "(model `grok-4.7-high`)",
     "(on the model selected in this chat)",
     1),
    ("commands/astra-review.md",
     "as a **fresh subagent on Grok 4.7 High (`grok-4.7-high`)**",
     "as a **fresh subagent on the model selected in this chat**",
     1),
    ("commands/astra-review.md",
     "or back to **deep-reasoner** (`grok-4.7-high`)",
     "or back to **deep-reasoner** (on the model selected in this chat)",
     1),
    ("commands/astra-review.md",
     "Model: grok-4.7-high",
     "Model: inherit",
     1),
    ("commands/gan-build.md",
     "(model `grok-4.7-high`)",
     "(on the model selected in this chat)",
     1),
    ("commands/gan-build.md",
     "on model `grok-4.7-high`, first to generate",
     "on the model selected in this chat, first to generate",
     1),
    ("commands/gan-design.md",
     "(model `grok-4.7-high`)",
     "(on the model selected in this chat)",
     2),
    ("commands/gan-design.md",
     "on model `grok-4.7-high`, first to generate",
     "on the model selected in this chat, first to generate",
     1),
    ("commands/model-route.md",
     "- `grok-4.7-high`: default for implementation and refactors\n- `grok-4.7-high`: architecture, deep review, ambiguous requirements",
     "- the model selected in this chat: default for implementation and refactors, architecture, deep review, ambiguous requirements",
     1),
    ("rules/common-agents.mdc",
     "(or `grok-4.7-high` for the 4.7-pinned agents: `architect`, `healthcare-reviewer`, `spec-miner`, `deep-reasoner`)",
     "(or `inherit` — the model selected in this chat — for the chat-model agents: `architect`, `healthcare-reviewer`, `spec-miner`, `deep-reasoner`)",
     1),
    ("rules/common-performance.mdc",
     "**grok-4.7-high** (deepest reasoning; deep-reasoner)",
     "**the model selected in this chat** (deepest reasoning; deep-reasoner)",
     1),
    ("rules/common-performance.mdc",
     "agent model pins in agents/ (notably grok-4.7-high for deep-reasoner)",
     "agent model inheritance in agents/ (notably `inherit` for deep-reasoner — it runs on the model selected in this chat)",
     1),
    ("schemas/agent.schema.json",
     '"enum": ["cursor-grok-4.6-high-fast", "grok-4.7-high"]',
     '"enum": ["cursor-grok-4.6-high-fast", "inherit"]',
     1),
    ("schemas/agent.schema.json",
     '"Source model tier, when present. Grok model slugs only in v1."',
     '"Source model tier, when present. `inherit` runs on the model selected in the chat; the fast tier pins `cursor-grok-4.6-high-fast`."',
     1),
    ("skills/gan-style-harness/SKILL.md",
     "raise via `GAN_PLANNER_MODEL=grok-4.7-high` for deeper spec expansion",
     "raise via `GAN_PLANNER_MODEL` (set it to the model selected in this chat) for deeper spec expansion",
     1),
    ("skills/gan-style-harness/SKILL.md",
     "raise via `GAN_GENERATOR_MODEL=grok-4.7-high` for maximum coding capability",
     "raise via `GAN_GENERATOR_MODEL` (set it to the model selected in this chat) for maximum coding capability",
     1),
    ("skills/gan-style-harness/SKILL.md",
     "raise via `GAN_EVALUATOR_MODEL=grok-4.7-high` for stronger judgment + tool use",
     "raise via `GAN_EVALUATOR_MODEL` (set it to the model selected in this chat) for stronger judgment + tool use",
     1),
    ("manifests/pi-core.json",
     '"astra-review.md": "deep review via the deep-reasoner agent (Grok 4.7 High)"',
     '"astra-review.md": "deep review via the deep-reasoner agent (model selected in this chat)"',
     1),
    # --- Round 33c (D33-22): Auto guardrail woven into every direct command
    # entry point. No staged source exists for these files (built-tree-only,
    # written by build.sh heredocs + fix patches), so the weave is a built-tree
    # replacement here, the same mechanism as the other command edits above.
    # Full MODEL check at the entry of gan-build / gan-design / astra-review
    # and in orch-pipeline Step 0 (the shared choke point for the five
    # orch-* commands); a one-line guardrail reference in each orch-* command
    # file + commands/orchestrate.md, pointing at the operative check.
    ('commands/gan-build.md',
     '---\n\nParse the following from $ARGUMENTS:',
     '---\n\n**MODEL check (fix #33, MODELSEL_F33):** before anything else, state the model the orchestrator is running on and record it in the run ledger (`MODEL: <name>` — the actual selected model). If the selected model is Auto, or the model cannot be determined to be a specific model, tell the user to pick a specific model before proceeding; do not silently orchestrate on an unknown fallback.\n\nParse the following from $ARGUMENTS:',
     1),
    ('commands/gan-design.md',
     '---\n\nParse the following from $ARGUMENTS:',
     '---\n\n**MODEL check (fix #33, MODELSEL_F33):** before anything else, state the model the orchestrator is running on and record it in the run ledger (`MODEL: <name>` — the actual selected model). If the selected model is Auto, or the model cannot be determined to be a specific model, tell the user to pick a specific model before proceeding; do not silently orchestrate on an unknown fallback.\n\nParse the following from $ARGUMENTS:',
     1),
    ('commands/astra-review.md',
     '---\n\n# Deep Review',
     '---\n\n**MODEL check (fix #33, MODELSEL_F33):** before anything else, state the model the orchestrator is running on and record it in the run ledger (`MODEL: <name>` — the actual selected model). If the selected model is Auto, or the model cannot be determined to be a specific model, tell the user to pick a specific model before proceeding; do not silently orchestrate on an unknown fallback.\n\n# Deep Review',
     1),
    ('skills/orch-pipeline/SKILL.md',
     '## Step 0 — Classify size (right-sizing)\n\nCeremony scales to blast radius.',
     '## Step 0 — Classify size (right-sizing)\n\n**MODEL check (fix #33, MODELSEL_F33):** before anything else, state the model the orchestrator is running on and record it in the run ledger (`MODEL: <name>` — the actual selected model). If the selected model is Auto, or the model cannot be determined to be a specific model, tell the user to pick a specific model before proceeding; do not silently orchestrate on an unknown fallback.\n\nCeremony scales to blast radius.',
     1),
    ('commands/orch-add-feature.md',
     '# /orch-add-feature\n',
     '# /orch-add-feature\n\n**MODEL check (fix #33, MODELSEL_F33):** before anything else — the `orch-pipeline` engine runs its MODEL check first (Step 0, before classifying): if the selected model is Auto, or the model cannot be determined to be a specific model, tell the user to pick a specific model before proceeding; do not silently orchestrate on an unknown fallback.\n',
     1),
    ('commands/orch-build-mvp.md',
     '# /orch-build-mvp\n',
     '# /orch-build-mvp\n\n**MODEL check (fix #33, MODELSEL_F33):** before anything else — the `orch-pipeline` engine runs its MODEL check first (Step 0, before classifying): if the selected model is Auto, or the model cannot be determined to be a specific model, tell the user to pick a specific model before proceeding; do not silently orchestrate on an unknown fallback.\n',
     1),
    ('commands/orch-change-feature.md',
     '# /orch-change-feature\n',
     '# /orch-change-feature\n\n**MODEL check (fix #33, MODELSEL_F33):** before anything else — the `orch-pipeline` engine runs its MODEL check first (Step 0, before classifying): if the selected model is Auto, or the model cannot be determined to be a specific model, tell the user to pick a specific model before proceeding; do not silently orchestrate on an unknown fallback.\n',
     1),
    ('commands/orch-fix-defect.md',
     '# /orch-fix-defect\n',
     '# /orch-fix-defect\n\n**MODEL check (fix #33, MODELSEL_F33):** before anything else — the `orch-pipeline` engine runs its MODEL check first (Step 0, before classifying): if the selected model is Auto, or the model cannot be determined to be a specific model, tell the user to pick a specific model before proceeding; do not silently orchestrate on an unknown fallback.\n',
     1),
    ('commands/orch-refine-code.md',
     '# /orch-refine-code\n',
     '# /orch-refine-code\n\n**MODEL check (fix #33, MODELSEL_F33):** before anything else — the `orch-pipeline` engine runs its MODEL check first (Step 0, before classifying): if the selected model is Auto, or the model cannot be determined to be a specific model, tell the user to pick a specific model before proceeding; do not silently orchestrate on an unknown fallback.\n',
     1),
    ('commands/orchestrate.md',
     'Act as the multi-model orchestrator (tech lead). Load and follow the `orchestrate` skill — the routing rule, budget modes, delegation contract, escalation ladder, verification stage, and reconciliation rules all live there; do not improvise around them.',
     "Act as the multi-model orchestrator (tech lead). Load and follow the `orchestrate` skill — the routing rule, budget modes, delegation contract, escalation ladder, verification stage, and reconciliation rules all live there; do not improvise around them.\n\n**MODEL check (fix #33, MODELSEL_F33):** the orchestrate skill's MODEL check runs first, before grill-me (see the skill): if the selected model is Auto, or the model cannot be determined to be a specific model, tell the user to pick a specific model before proceeding; do not silently orchestrate on an unknown fallback.",
     1),
    # --- Round 33d (D33-25..D33-28): guardrail woven at each bypass itself
    # (audit #111-B). B-B1's section never invokes the engine, B-B2's step 1
    # ran phases without Step 0, and feature-dev / react-build are standalone
    # entry points — a pointer at a command entry cannot cover any of them.
    # B-B5/B-B6 live in staged sources (new-skills/grill-me,
    # new-skills/feature-expansion), so they need no tuple here.
    ('skills/orch-change-feature/SKILL.md',
     '## Removing a feature\n\nWhen the request is to remove a feature — including a one-prompt removal of a first-build feature routed here by orchestrate:',
     '## Removing a feature\n\n**MODEL check (fix #33, MODELSEL_F33):** before anything else, state the model the orchestrator is running on and record it in the run ledger (`MODEL: <name>` — the actual selected model). If the selected model is Auto, or the model cannot be determined to be a specific model, tell the user to pick a specific model before proceeding; do not silently orchestrate on an unknown fallback.\n\nWhen the request is to remove a feature — including a one-prompt removal of a first-build feature routed here by orchestrate:',
     1),
    ('skills/orch-build-mvp/SKILL.md',
     '1. Run orch-pipeline Phases 0–2 ONLY (Intake/Research/Plan) with the settings above — read the record/scope, extract scope, locked decisions, and the feature list, order it into thin vertical slices, ending at Gate 1 (slice plan).',
     '1. Run orch-pipeline Step 0 first (Classify size — the MODEL check, fix #33, MODELSEL_F33, is the first content of Step 0 and runs before anything else: if the selected model is Auto, or the model cannot be determined to be a specific model, tell the user to pick a specific model before proceeding; do not silently orchestrate on an unknown fallback), then Phases 0–2 ONLY (Intake/Research/Plan) with the settings above — read the record/scope, extract scope, locked decisions, and the feature list, order it into thin vertical slices, ending at Gate 1 (slice plan).',
     1),
    ('commands/orch-build-mvp.md',
     'This is orch-build-mvp step 1 = orch-pipeline Phases 0–2 only — it never runs the full engine.',
     'This is orch-build-mvp step 1 = orch-pipeline Step 0 (MODEL check + Classify) first, then Phases 0–2 only — it never runs the full engine.',
     1),
    ('commands/feature-dev.md',
     '---\n\nA structured feature-development workflow that emphasizes understanding existing code before writing new code.',
     '---\n\n**MODEL check (fix #33, MODELSEL_F33):** before anything else, state the model the orchestrator is running on and record it in the run ledger (`MODEL: <name>` — the actual selected model). If the selected model is Auto, or the model cannot be determined to be a specific model, tell the user to pick a specific model before proceeding; do not silently orchestrate on an unknown fallback.\n\nA structured feature-development workflow that emphasizes understanding existing code before writing new code.',
     1),
    ('commands/react-build.md',
     '---\n\n# React Build and Fix',
     '---\n\n**MODEL check (fix #33, MODELSEL_F33):** before anything else, state the model the orchestrator is running on and record it in the run ledger (`MODEL: <name>` — the actual selected model). If the selected model is Auto, or the model cannot be determined to be a specific model, tell the user to pick a specific model before proceeding; do not silently orchestrate on an unknown fallback.\n\n# React Build and Fix',
     1),
]

# Agent files whose `model:` line must read `inherit` after the build
# (staged deep-reasoner + the three opus-mapped ecc-* agents).
INHERIT_AGENTS = (
    "agents/deep-reasoner.md",
    "agents/ecc-architect.md",
    "agents/ecc-healthcare-reviewer.md",
    "agents/ecc-spec-miner.md",
)


def main():
    global BASE, ROOT  # D33-14: sys.argv is read here, never at import time.
    BASE = sys.argv[1] if len(sys.argv) > 1 else ""
    ROOT = os.path.dirname(BASE.rstrip("/")) if BASE else ""

    # ---------------------------------------------------------------- 1. Census (pre-replace, no writes)
    _totals = {k: 0 for k in EXPECT}
    _totals["bare_fast"] = 0
    _keep_prose = 0
    _binary_skipped = []
    for _path, _text in _walk_files():
        if _text is None:
            _raw = open(_path, "rb").read()
            for _needle in (OLD_ID, OLD_PROSE, NEW_ID, NEW_PROSE, FAST_ID):
                if _needle.encode("utf-8") in _raw:
                    ERRORS.append(
                        f"census: pin text {_needle!r} found in non-UTF-8 file "
                        f"{os.path.relpath(_path, BASE)} — refusing to guess")
            _binary_skipped.append(os.path.relpath(_path, BASE))
            continue
        _c = _count_in(_text)
        for _k in _totals:
            if _k in _c:
                _totals[_k] += _c[_k]
        _totals["bare_fast"] += _bare_fast_count(_text)
        if os.path.relpath(_path, BASE) == KEEP_FILE:
            _keep_prose = _c[OLD_PROSE]
    for _k, _want in EXPECT.items():
        if _totals[_k] != _want:
            ERRORS.append(
                f"census: {_k} found {_totals[_k]}x, expected {_want}x — "
                f"tree drifted from the fix33 pre-state census; refusing to unpin")
    if _keep_prose != 2:
        ERRORS.append(
            f"census: {OLD_PROSE!r} in {KEEP_FILE} found {_keep_prose}x, "
            f"expected 2x — the keeps must live only there (D33-16)")
    if _totals["bare_fast"] != 0:
        ERRORS.append(
            f"census: bare {FAST_BARE} found {_totals['bare_fast']}x, expected 0x")
    CHANGES.append(
        f"census: {OLD_ID} x{_totals[OLD_ID]}, {OLD_PROSE!r} x{_totals[OLD_PROSE]}, "
        f"{FAST_ID} x{_totals[FAST_ID]}, bare {FAST_BARE} x{_totals['bare_fast']}, "
        f"{NEW_ID} x{_totals[NEW_ID]}, {NEW_PROSE!r} x{_totals[NEW_PROSE]} "
        f"(keeps in {KEEP_FILE} x{_keep_prose}), "
        f"{len(_binary_skipped)} non-UTF-8 file(s) skipped (byte-checked, no pin text)")
    # Anchor check: every replacement anchor present exactly as expected.
    for _rel, _old, _new, _want in REPLACEMENTS:
        if not exists(p(_rel)):
            ERRORS.append(f"census: replacement target {_rel} missing")
            continue
        _n = read(p(_rel)).count(_old)
        if _n != _want:
            ERRORS.append(
                f"census: {_rel}: expected {_want}x { _old[:60]!r}, found {_n}x")
    if ERRORS:
        # Fail before writing anything.
        _write_log()
        print("fix33: ERROR(S) in census — no files written", file=sys.stderr)
        for e in ERRORS:
            print(f"  ! {e}", file=sys.stderr)
        sys.exit(1)

    # ---------------------------------------------------------------- 2. Replace
    for _rel, _old, _new, _want in REPLACEMENTS:
        _f = p(_rel)
        _t = read(_f)
        _n = _t.count(_old)
        write(_f, _t.replace(_old, _new))
        CHANGES.append(
            f"{_rel}: unpinned ({_old[:50]!r} ... x{_n})")

    # ---------------------------------------------------------------- 3. Post-assertions (re-census)
    _post = {k: 0 for k in EXPECT}
    _post["bare_fast"] = 0
    _post_keep = 0
    for _path, _text in _walk_files():
        if _text is None:
            continue
        _c = _count_in(_text)
        for _k in _post:
            if _k in _c:
                _post[_k] += _c[_k]
        _post["bare_fast"] += _bare_fast_count(_text)
        if os.path.relpath(_path, BASE) == KEEP_FILE:
            _post_keep = _c[OLD_PROSE]
    if _post[OLD_ID] != 0:
        ERRORS.append(f"post: {OLD_ID} still present {_post[OLD_ID]}x after unpin")
    if _post[OLD_PROSE] != 2 or _post_keep != 2:
        ERRORS.append(
            f"post: {OLD_PROSE!r} found {_post[OLD_PROSE]}x (keeps file x{_post_keep}), "
            f"expected 2x all in {KEEP_FILE} (D33-16)")
    if _post[NEW_ID] != 0:
        ERRORS.append(f"post: {NEW_ID} still present {_post[NEW_ID]}x after unpin")
    if _post[NEW_PROSE] != 0:
        ERRORS.append(
            f"post: {NEW_PROSE!r} found {_post[NEW_PROSE]}x after unpin, "
            f"expected 0x (fix30 retired — nothing renames to Extra High)")
    if _post[FAST_ID] != EXPECT[FAST_ID] + 1:
        ERRORS.append(
            f"post: {FAST_ID} found {_post[FAST_ID]}x, expected {EXPECT[FAST_ID] + 1}x "
            f"(71 pre-existing + 1 added by the schema description replacement, "
            f"D33-17 — the fast tier itself is unchanged)")
    if _post["bare_fast"] != 0:
        ERRORS.append(f"post: bare {FAST_BARE} found {_post['bare_fast']}x, expected 0x")
    CHANGES.append(
        f"post: {OLD_ID} x{_post[OLD_ID]}, {OLD_PROSE!r} x{_post[OLD_PROSE]}, "
        f"{NEW_ID} x{_post[NEW_ID]}, {NEW_PROSE!r} x{_post[NEW_PROSE]} "
        f"(keeps in {KEEP_FILE} x{_post_keep}), {FAST_ID} x{_post[FAST_ID]} "
        f"(71 pre-existing + 1 in the schema description, D33-17), "
        f"bare {FAST_BARE} x{_post['bare_fast']}")

    # ---------------------------------------------------------------- 4. `model: inherit` + guardrail anchors
    for _rel in INHERIT_AGENTS:
        if not exists(p(_rel)):
            ERRORS.append(f"post: agent file {_rel} missing")
            continue
        _t = read(p(_rel))
        if "model: inherit" not in _t:
            ERRORS.append(f"post: {_rel} carries no `model: inherit` line")
        if "grok-4.7" in _t:
            ERRORS.append(f"post: {_rel} still carries a grok-4.7 pin")
    if not ERRORS:
        CHANGES.append(
            "post: `model: inherit` present in all 4 chat-model agent files "
            "(deep-reasoner, ecc-architect, ecc-healthcare-reviewer, ecc-spec-miner)")
    _orch = read(p("skills/orchestrate/SKILL.md")) if exists(p("skills/orchestrate/SKILL.md")) else ""
    if _orch.count("MODELSEL_F33") != 2:
        ERRORS.append(
            f"post: MODELSEL_F33 found {_orch.count('MODELSEL_F33')}x in skills/orchestrate/SKILL.md, expected 2x (L14 identity + pre-grill MODEL check)")
    else:
        CHANGES.append("post: MODELSEL_F33 present 2x in skills/orchestrate/SKILL.md (identity L14 + pre-grill MODEL check)")

    # ---------------------------------------------------------------- 5. Regression guards: blocks untouched
    _F29_TOKENS = ("ORCHESTRATOR-ONLY_F29", "FACTORY-DISPATCH_F29",
                   "DIRECTOR-BRIEF_F29", "NO-GUESSING_F29", "VERIFY-MERGE_F29",
                   "GLOBAL-ROUTING_F29", "COST-AWARE_F29")
    _orch_p = p("skills/orchestrate/SKILL.md")
    _hm_p = p("rules/hackathon-mode.mdc")
    if not exists(_orch_p) or not exists(_hm_p):
        ERRORS.append("guard: orchestrate SKILL.md or hackathon-mode.mdc missing")
    else:
        _o = read(_orch_p)
        _h = read(_hm_p)
        _b1 = _block(_o, "**GLOBAL-ROUTING")
        _b2 = _block(_h, "**GLOBAL-ROUTING")
        if _b1 is None or _b2 is None:
            ERRORS.append("guard: GLOBAL-ROUTING block not found in orchestrate or hackathon-mode")
        elif _b1 != _b2:
            ERRORS.append("guard: GLOBAL-ROUTING block differs between orchestrate and hackathon-mode")
        else:
            CHANGES.append("guard: GLOBAL-ROUTING block byte-identical in orchestrate + hackathon-mode (unpin did not touch it)")
        for _tok in _F29_TOKENS:
            if _b1 is None or _tok not in _b1:
                ERRORS.append(f"guard: GLOBAL-ROUTING block missing token {_tok}")
        _d1 = _block(_o, "**DESIGNPKG-AUTO")
        _d2 = _block(_h, "**DESIGNPKG-AUTO")
        if _d1 is None or _d2 is None:
            ERRORS.append("guard: DESIGNPKG-AUTO block not found in orchestrate or hackathon-mode")
        elif _d1 != _d2:
            ERRORS.append("guard: DESIGNPKG-AUTO block differs between orchestrate and hackathon-mode")
        else:
            CHANGES.append("guard: DESIGNPKG-AUTO block byte-identical in orchestrate + hackathon-mode (unpin did not touch it)")

    # ---------------------------------------------------------------- Decisions + OWED
    DECISIONS.extend([
        "DECISION-33-1 (mechanism): fix30/fix30.py is RETIRED (build.sh no longer invokes it) and fix33.py runs in its slot (after fix29, before fix31). Keeping fix30 as an intermediate would rename to Extra High and then un-rename — a stale rename that re-pins the orchestrator mid-build. fix31.py and fix32.py EXPECT_PIN are updated to the post-unpin census ({OLD 0, OLD_PROSE 2, FAST 72, NEW 0, NEW_PROSE 0} — the 2 OLD_PROSE are the strategic-compact keeps in High form, D33-16; FAST 72 = 71 pre-existing + 1 in the schema description, D33-17); only the census constants, messages and comments change in those scripts.",
        "DECISION-33-2 (staged weave): the staged pin text is replaced too, not build-time-only — the task requires no orchestrator-identity pin in staged text. Safe: no fix script anchors on the staged files edited here (fix16.py:4207 is a guarded no-op on a path that does not exist in the built tree; fix24/fix29 anchor on built-tree text from build.sh heredocs). The DESIGNPKG-AUTO sentence is edited IDENTICALLY in orchestrate + hackathon-mode so the cross-file byte-identity checks still pass.",
        "DECISION-33-3 (model: inherit): per Cursor docs (Subagents), `inherit` is the subagent default and means 'same model as the parent agent'. It is the frontmatter value for the chat-model tier (deep-reasoner, the three opus-mapped ecc-* agents, the astra-review verdict block, the agent template). Deleting the line was rejected: `inherit` is explicit, greppable and verifiable; a missing line is ambiguous.",
        "DECISION-33-4 (scope): the unpin covers the whole 'decides' tier (orchestrator + design-lead + deep-reasoner), per the plugin's own hierarchy grouping. The fast tier (x71) and the drones are untouched.",
        "DECISION-33-5 (Auto guardrail): home is orchestrate/SKILL.md L14 (identity, MODELSEL_F33) + the pre-grill MODEL check (staged L52, MODELSEL_F33 — runs before grill-me, D33-20) + L95 picker note; step 0 (L64) carries only a back-reference to the pre-grill check; hackathon-mode L12 + §7 point to the MODEL check as the sole precondition to grill-me (D33-20). If the selected model is Auto or cannot be determined, the orchestrator tells the user to pick a specific model before proceeding and does not silently orchestrate.",
        "DECISION-33-6 (cost accounting): finding, no new system — the regular tree has no cost-accounting text stating the orchestrator model. The MODEL check records the ACTUAL selected model (`MODEL: <name>`); unknown/unrecorded means cost is marked unknown, never assumed Grok/pool.",
        "DECISION-33-7 (keeps): only §1(b) of the SPEC — strategic-compact :68/:102 (factual model examples), LIVE_SMOKE_TEST :132 (test baseline), FACTORY_CURSOR_PLAN.md (factory round 4), fix*/ history (never edited), build.sh patch literals/heredocs (out of scan scope per fix32 precedent).",
        "DECISION-33-8 (schema enum): agent.schema.json enum becomes [\"cursor-grok-4.6-high-fast\", \"inherit\"]; grok-4.7-extra-high is REMOVED, not kept as a model list — the enum validates agent files and no agent file may carry a decides-tier pin after this fix.",
        "DECISION-33-9 (model-route merge): both Extra High lines name the same model after the unpin, so they merge into one chat-model line; the heuristic becomes fast-vs-chat-model.",
        "DECISION-33-10 (GAN env examples): GAN_*_MODEL examples drop the Extra High ID ('set it to the model selected in this chat'). His default (Extra High) is not named in plugin text; it lives in the live-test prompt and the SPEC.",
        "DECISION-33-11 (live-test prompt): fix30/live-test-prompt.md updated to state explicitly that Grok 4.7 Extra High is to be selected in the chat for the test; pass = the parent ran the SELECTED model on both tasks.",
        "DECISION-33-12 (log determinism): _walk_files sorts _dirs as well as files — fix30.py did not, so its log lines could reorder run to run.",
        "DECISION-33-13 (wording standard): prose 'the model selected in this chat', frontmatter `model: inherit`, ledger `MODEL: <name>`, design-lead parenthetical '(on the model selected in this chat)'.",
        "DECISION-33-14 (import guard): the whole executable body lives in main() under `if __name__ == \"__main__\":`; module level assigns BASE = '' and ROOT = ''. Importing this module must never execute the census or overwrite the patch log (fix32 DECISION-32-14/15 lesson).",
        "DECISION-33-15 (build.sh STEP 5 audit2_patch anchors follow the opus mapping): the STEP 5 inline audit2_patch anchors on the three opus agents' frontmatter (ecc-architect.md, ecc-healthcare-reviewer.md, ecc-spec-miner.md) include the `model:` line, and the opus->inherit mapping runs in STEP 2, before STEP 5 — build run 1 failed at ecc-architect.md ('pattern not found exactly once'). The six `model: grok-4.7-high` lines in those anchors (old + new blocks) now say `model: inherit`; the patch's purpose (drop the `tools:` line, reorder frontmatter) is unchanged. The astra-review STEP 5 anchor is NOT changed: the mapping touches agents/ only, so its frontmatter/body pin lines still match, and fix33.py handles the final astra-review text after fix29 rewrites it.",
        "DECISION-33-16 (census corrected from measurement, not derivation): the first pre-state census was derived from the fix30 tree (49/22) by subtracting staged-copy and mapping removals, and it was wrong in two places — build run 2 failed loudly on it, which is the census doing its job. (a) The strategic-compact keeps are 'Grok 4.7 High' x2 in the fix33 tree, NOT 'Grok 4.7 Extra High' x2: in the fix30 tree they read Extra High only because fix30's rename rewrote them; with fix30 retired they stay in High form. So pre-state OLD_PROSE is x7 (5 replaceable + 2 keeps) and NEW_PROSE is x0, and post-state OLD_PROSE is x2 (keeps only) with NEW_PROSE x0. (b) FAST is x71, not x70: the fix33 staged weave added one fast mention in the orchestrate L93 picker note ('the fast tier pins `cursor-grok-4.6-high-fast`'). All census numbers in this script, in fix31.py/fix32.py EXPECT_PIN, and in SPEC.md §1 are the MEASURED fix33-build numbers (run 2 output + direct grep of the built tree), not the derivation.",
        "DECISION-33-17 (schema description adds one fast mention): the new agent.schema.json description names the fast tier ('the fast tier pins `cursor-grok-4.6-high-fast`') where the old description named no model — so the post-fix33 fast count is x72, not x71 (71 pre-existing + 1 in the description). The fast tier itself is unchanged: all 71 pre-existing mentions are still there, no fast pin was added or removed, only a descriptive mention. fix33.py's post-assertion expects 72, and fix31.py/fix32.py EXPECT_PIN FAST_ID is 72. (Found by build run 3 failing loudly on 72 vs 71 — the census doing its job again.)",
        "DECISION-33-18 (fix32.py STAGED_BUILT anchor follows the unpin): fix32.py's orchestrate anchor #3 asserted the DESIGNPKG-AUTO sentence up to 'the design skill leads on model' — written pin-free so the fix30 rename would not trip it, but the unpin changed the continuation from 'leads on model `grok-4.7-high`' to 'leads on the model selected in this chat', so 'leads on model' is no longer a substring and build run 4 failed fix32's census (staged + built). The anchor is updated to the new wording ('...leads on the model selected in this chat'), which asserts the fix32 demotion AND the fix33 unpin — in fix32.py's STAGED_BUILT list AND in verify33.py's two copies of it (§15c check + §15h _STAGED_BUILT32). Same class as D33-15: a prior fix's anchor following the unpin. No other fix31/fix32 anchor trips on the unpin (fix31 has no such anchor; fix32's remaining anchors passed run 4's census).",
        "DECISION-33-19 (SPEC correction: guardrail home is orchestrate-only): D33-5 as written claimed hackathon-mode.mdc L42 carries a one-line pointer to the MODEL check — that pointer was never woven (L42 is the hierarchy paragraph in model-agnostic wording; grep-verified while building verify33 section 16c). SPEC error, not a tree defect: the guardrail is fully present in orchestrate L14 + pre-grill MODEL check L52 + L95 picker note (MODELSEL_F33 x2), and the MODEL check is an orchestrate pre-grill block (step 0, L64, carries only a back-reference to it). No tree change is made for the pointer. [Corrected by D33-32, round 33d, audit #111-A A-M1: L62/L93 were the pre-33c lines; the check moved to the pre-grill block in round 33c.]",
        "DECISION-33-20 (MODEL check re-sequenced before grill-me — round 33c, D-1/S-M2): the operative MODEL check moves out of orchestrate step 0 to a new pre-grill block under ## Run (staged orchestrate L52; step 0 is now L64, picker note L95): it fires in the first reply, before grill-me starts, and grill-me does not start until a specific model is picked. Step 0 keeps only a back-reference ('already ran before grill-me — if the model is still Auto ... stop and ask again'). L14's 'before proceeding' now reads true as written (verified — the ask precedes all work); L14/L95 cross-references now point at the pre-grill check. hackathon-mode L12 points to the MODEL check as the sole precondition to grill-me FIRST, its first-build sequence now reads 'MODEL check → grill → narration-key prompt → ...', and §7 names the MODEL check as the one question that precedes grill-me. The D33-19 'no pointer' stance is revised for L12/§7 only (a pointer, not the operative check — the home stays orchestrate); the D33-19 correction itself (the L42 pointer was never woven) stands as history. MODELSEL_F33 stays 2x in orchestrate (L14 + pre-grill block).",
        "DECISION-33-21 ('proceeding' defined; grill-me-first-for-build-work preserved — round 33c): 'before proceeding' in D33-5/L14 means before ANY work, grill-me included — grill-me is proceeding (D-1). The standing 'grill-me FIRST after the first project prompt' rule is about BUILD work, and the model ask is not build work: grill-me stays FIRST among build steps, and the MODEL check is its sole precondition. hackathon-mode L12 and the pre-grill block both state this explicitly, so the two rules no longer read as contradicting each other.",
        "DECISION-33-22 (direct-command guardrail weave — round 33c, D-2/OWED-33-4): inventory (grepped, not guessed) — commands/gan-build.md, commands/gan-design.md, commands/astra-review.md, commands/orch-add-feature.md, commands/orch-build-mvp.md, commands/orch-change-feature.md, commands/orch-fix-defect.md, commands/orch-refine-code.md, commands/orchestrate.md (9 files; the five orch-* match the 'orch-*' glob, orchestrate.md is the /orchestrate command). No staged source exists for any of these files (they are built-tree-only, written by build.sh heredocs + fix patches), so the weave is a fix33.py built-tree replacement, the same mechanism as the other command edits in this fix. Mechanism: the full MODEL check (MODELSEL_F33 wording, mirroring orchestrate) is woven at each entry — gan-build/gan-design right after the frontmatter (before arg parsing), astra-review before '# Deep Review', orch-pipeline Step 0 (the shared choke point for the orch-* commands: Step 0 is the classifier section — the MODEL check is its first content, before the classifier's scoring text and before Phase 0 Intake, which always runs). The five orch-* command files + orchestrate.md carry a one-line guardrail reference (MODELSEL_F33) at their entry pointing at the operative check (orch-pipeline Step 0 / the orchestrate skill), so MODELSEL_F33 is present in EVERY direct command file and no cold start bypasses the ask. The orch-pipeline choke point was verified genuine for three orch-* commands only (add/fix/refine — each skill's step 1 runs the engine) and for orch-change-feature's change path; it was NOT genuine for orch-change-feature's removal branch (which never invokes the engine) or for orch-build-mvp (whose step 1 runs Phases 0–2, and Step 0 is the classifier section, not a phase) — both are closed in round 33d by D33-25/D33-26, and the 33c claim otherwise is corrected here rather than deleted — and it sits at Step 0, not Intake, because the size classifier runs before the phases list, so an Intake check would not precede all entry work — gan-build/gan-design/astra-review do not route through it, so they carry the full ask at their own entries. A downstream /gan-build drive (orch-build-mvp step 4, --skip-planner) re-runs the check after the model is already picked, so it passes silently — no second ask. fix33.py change count rises 31 → 41 (25 + 10 new replacements).",
        'DECISION-33-23 (OWED-33-4 SUPERSEDED — round 33c): OWED-33-4 (direct commands carry no Auto ask) is FIXED by D33-22 in this round and marked SUPERSEDED in SPEC §6 + MANIFEST, not deleted — the deferral-and-reversal history stays readable. The fix33.py OWED list records it as superseded.',
        'DECISION-33-24 (verifier extended — round 33c): verify33.py gains §16l (re-sequence: MODEL-check-before-grill-me line-order in staged + built orchestrate and hackathon-mode; MODELSEL_F33 still 2x; step 0 back-reference; L14 accurate; grill-me-first-for-build-work preserved) and §16m (direct commands: MODELSEL_F33 in all 9 command files, full ask in gan-build/gan-design/astra-review/orch-pipeline, pointers in the orch-* + orchestrate command files, guardrail-before-first-work-step line-order per file). §16c check 4 now asserts the bold MODEL check lives in the pre-grill block; §16f asserts D33-20..D33-24 + OWED-33-4 SUPERSEDED in the patch log. Verifier count rises 526 → 565 (recorded in the round report + MANIFEST).',
        "DECISION-33-25 (B-B1 — removal branch guardrail, round 33d): the full MODEL check (MODELSEL_F33 wording) is woven at the top of the `## Removing a feature` section in skills/orch-change-feature/SKILL.md (fix33.py built-tree replacement), as the section's first content, before its step 1 (code-explorer trace / deletion). The section is self-contained and never invokes the orch-pipeline engine, so the command file's L7 pointer could not cover it — a pointer without a routing edge is not coverage. This closes both reachable paths: the direct /orch-change-feature removal branch (command L27 routes to the section) and the skill:orch-change-feature trigger path ('remove a feature'), which loads the skill directly. The orchestrate-routed one-prompt removal was already covered upstream by the orchestrate pre-grill check.",
        "DECISION-33-26 (B-B2 — orch-build-mvp step 1 runs Step 0, round 33d): orch-build-mvp step 1 now runs orch-pipeline Step 0 FIRST, then Phases 0–2. Mechanism chosen (of the two the audit allowed): step 1 names Step 0 explicitly AND restates the MODEL ask (MODELSEL_F33) at step 1's entry, so the check fires before scoping, slicing, Gate 1, and expansion even if Step 0 is read as classifier-only — the routing edge and the operative ask are both present, not one or the other. The command file's step-1 sentence is corrected the same way (Step 0 first, then Phases 0–2). This corrects D33-22's self-contradictory sentence ('each skill's step 1 runs the engine; orch-build-mvp runs Phases 0–2 in step 1') and the same sentence in the round-33c report §1.3: Step 0 is the classifier section, not a phase, so running Phases 0–2 never ran it. The downstream /gan-build drive at step 4 still re-checks after the model is picked and passes silently.",
        "DECISION-33-27 (B-B3 — /feature-dev guardrail, round 33d): the full MODEL check (MODELSEL_F33 wording, mirroring gan-build) is woven at the entry of commands/feature-dev.md (fix33.py built-tree replacement, right after the frontmatter), before Phase 1's code-explorer dispatch, the code-architect design, implementation, and review. /feature-dev is the standalone version of the orch-add-feature flow and was outside the round-33c 9-file inventory; it now carries the same guardrail as the orch-* commands.",
        "DECISION-33-28 (B-B4 — /react-build guardrail, round 33d): the full MODEL check (MODELSEL_F33 wording, mirroring gan-build) is woven at the entry of commands/react-build.md (fix33.py built-tree replacement, right after the frontmatter), before the Factory routing paragraph dispatches the react-build-resolver drone and before the fix loop. Drone pins and dispatch mechanisms are untouched — only the guardrail ask is added, as the task scoped it.",
        "DECISION-33-29 (B-B5 — trigger-routed grill-me guardrail, round 33d): the full MODEL check (MODELSEL_F33 wording) is woven at the entry of the grill-me skill (staged new-skills/grill-me/SKILL.md, first content under '# Grill Me' — the staged source flows verbatim into the built tree, the same mechanism as the round-33c orchestrate re-sequence; no fix33.py tuple is needed or added). The skill:grill-me triggers ('grill me', 'ask me questions about my idea', ...) load the skill directly, bypassing hackathon-mode §1 and the orchestrate pre-grill block. Harm is bounded (Q&A only; the check still fires before any build work), but the entry point must ask before proceeding. In the first-build flow the check re-fires after the upstream check and passes silently once a model is picked — no second ask.",
        "DECISION-33-30 (B-B6 — trigger-routed feature-expansion guardrail, round 33d): the full MODEL check (MODELSEL_F33 wording) is woven at the entry of the feature-expansion skill (staged new-skills/feature-expansion/SKILL.md, first content of the file body, before the decision-record read and Phase 0 grounding — the staged source flows verbatim into the built tree; no fix33.py tuple is needed or added). The skill:feature-expansion triggers ('make it much better', 'expand this', ...) load the skill directly, and its Phase 1 dispatches four brainstorm subagents. The MODEL check is not a user approval gate for features — the skill's 'no user approval gate' standing rule is about the feature list going straight into the build, not the model ask — so there is no conflict. In the first-build flow the check re-fires after the upstream check and passes silently once a model is picked.",
        "DECISION-33-31 (B-M2 — design-role unpin moves into build.sh, round 33d): build.sh fix13-A (orch-build-mvp, orch-change-feature) and the fix13e block (orch-add-feature, orch-fix-defect, orch-refine-code) now write the model-agnostic design-role wording instead of the `grok-4.7-high` pin, so the unpin of those five lines no longer depends on fix33.py running after — the scrub is no longer load-bearing. The five orch-* design-role scrub tuples are removed from fix33.py (their old text no longer exists) and the pre-state census drops ID 25 → 20 (PROSE x7, FAST x71 unchanged). Required consequence, same class as D33-15/D33-18: fix24.py's G-4 sub() anchored on the fix13-A parenthetical, which no longer exists — that one sub is removed (fix13-A now writes the pointer form directly) with a comment; the other two G-4 subs are untouched. Verified in code: no other build.sh patch writes the pin into any skill — the remaining build.sh `grok-4.7-high` new-text sites target only commands/ (gan-build, gan-design, astra-review), agents/ (ecc-gan-planner), rules/ (common-performance/common-agents old-side anchors), README.md, or comments, all still scrubbed by fix33.py; the only skill-targeting new-text pins were the five design-role lines. The fix13/fix13e-assemble.py copies still carry the old text — they are historical assemble scripts, never invoked by build.sh, and are left as history.",
        "DECISION-33-32 (A-M1 — stale guardrail-home line numbers, round 33d): the guardrail home is the pre-grill block L52 / step-0 back-reference L64 / picker note L95 (measured in the current built orchestrate skill — the 33c edits moved them from L62/L93). Corrected now in SPEC D33-5 + §3(c) Guards, MANIFEST Decisions summary + section header, implementation-report D33-5, the fix33.py DECISION-33-19 string (re-emitted into every regenerated patch log), and the verify33.py §16c check name. The check is a pre-grill block, not a step-0 procedure (step 0 is only a back-reference). Historical pre-33c mentions correctly framed as history (SPEC §3(a) table + replacement text, SPEC D33-19's as-of-then wording, MANIFEST :20/:103, implementation-report :37/:148) are NOT findings and are left alone.",
        "DECISION-33-33 (A-M2/S-M1/B-M1 — 'Phase 0' vs 'Step 0', round 33d): the orch-pipeline MODEL check sits at Step 0 (the classifier section), NOT Phase 0 (Intake). 'Phase 0' → 'Step 0' in the SPEC D33-22 parenthetical + §6 OWED-33-4, the fix33.py DECISION-33-22 + OWED-33-4 strings (the patch log corrects itself on the rebuild), and the verify33.py §16m header comment + check names. The incoherent 'Step 0 is the first thing the engine does, before the size classifier' phrasing is reworded: Step 0 IS the classifier — the MODEL check is the first content of Step 0, before the classifier's scoring text.",
        "DECISION-33-34 (B-M3 — review-only dispatches, round 33d): /review-pr, /plan's optional second deep-reasoner pass, and skill:council carry no guardrail and get none — review/deliberation only, no code written, no commit, no deploy, no dispatch of build work. Outside the claimed scope. Recorded as OWED-33-5 (observation), not fixed.",
        "DECISION-33-35 (verifier §16n + verifier-limit honesty, round 33d): verify33.py gains §16n (21 checks): routing-aware checks for EACH of B-B1..B-B6 (MODEL check present in the RIGHT file + section, before the first work step/dispatch on that path, in staged + built copies where a staged source exists) plus a B-M2 check that build.sh writes no design-role pin and fix24.py no longer anchors on the vanished parenthetical, plus patch-log assertions for D33-25..D33-35, OWED-33-5, and OWED-33-4 RE-OPENED. Verifier count rises 565 → 586. Stated honestly in the SPEC: §16l/§16m/§16n are static presence + line-order checks within files, not proof of execution — the re-audit re-traces each bypass path manually, and this round's own trace is recorded in the round-33d report.",
        "DECISION-33-36 (B-N1 — trigger-routed design-taste-frontend Hallmark redesign guardrail, round 33e): the full MODEL check (MODELSEL_F33 wording) is woven at the entry of the design-taste-frontend skill (staged new-skills/design-taste-frontend/SKILL.md, first content under '# Taste skill v2.5.1', :18 — the staged source flows into the built tree, the same mechanism as the round-33c orchestrate re-sequence and the round-33d B-B5/B-B6 staged weaves; no fix33.py tuple is needed or added). Traced path, read end to end: trigger skill:design-taste-frontend ('redesign the landing page', 'redesign the app ui', ... in skill-triggers@1.json) loads the skill directly → the check at :18 fires before any work → the 'Redesign of an existing page' paragraph (now :456) routes a full-page redesign to references/hallmark/references/redesign.md → its '## Build' 'More than one page' paragraph (:68) fans out past three pages at restyle/full depth, one single-task factory drone per page with a director brief (GLOBAL-ROUTING_F29). Placement is the skill entry, not the top of redesign.md: the entry covers the trigger path and every other load of the skill, and it cannot misfire — the check only interrupts on Auto/undetermined and passes silently on a specific selected model, so the in-flow routes (orchestrate pre-grill check; orch-change-feature change path → engine Step 0; orch-build-mvp Step 0) re-fire it with no second ask. The redesign flow's own 'The ask' (what must stay / what is wrong / anything new) does not resolve Auto and is not a substitute. Scope, as audited: the bypass needs 4+ pages at restyle/full depth (1–3 pages work inline and never dispatch; polish never fans out). The skill's hero/finish review subagents and the manual-gate / fresh-reader subagents are review-only (B-M3/OWED-33-5 class) and get no targeted weave — the entry check fires before them anyway.",
        "DECISION-33-37 (verifier §16n extended for B-N1 + scan maintenance, round 33e): verify33.py gains 6 B-N1 §16n checks (MODEL check present in the built design-taste-frontend skill, full ask at its entry, present in the staged source too, before the redesign routing paragraph, and the redesign.md fan-out paragraph still present downstream of it so the coverage claim is not vacuous, plus a patch-log assertion for D33-36..D33-39). Verifier count rises 586 → 592. Required consequence, same class as the round-33d §12 allow-list re-numbering: the +2-line insertion shifts the B1 brand-identity line in the skill from :444 to :446, so the scan r4/r5 regression sites (skills/design-taste-frontend/SKILL.md, 444) are re-numbered to 446 in both scripts, and the verify33.py check name quoting that site is updated the same way. Content re-read at the new line; nothing else in either scan changes.",
        "DECISION-33-38 (S-M1/A-M1 — fast count 70 → 71 in live prose, round 33e): the measured truth is 71 pre-state / 72 post-state (D33-16/D33-17; patch-log census, fix33.py EXPECT, verifier §16f, direct grep of the built tree). 'fast 70' / 'x70' is corrected to 71 in the five live spots: SPEC §0 scope (D33-4), §3(e) (16f), §4, and the fix33.py DECISION-33-4 string (the patch log regenerates from it on the rebuild — it is not hand-edited). Adjudicated as NOT stale and left alone: SPEC §0 source 2 (the fix30-tree census, a different tree's measured fact) and SPEC §1(d) (the dd106ade-tree measurement — verified 70 by git grep -o at HEAD dd106ade, since the fix33 staged weave adds the 71st mention); the 'not x70' framings inside D33-16 itself (SPEC, fix33.py, patch log, implementation report) and MANIFEST's D33-16 history line, which quote the corrected number to record the correction.",
        "DECISION-33-39 (A-M2 leftover — SPEC §3(h) Step 0 reword, round 33e): SPEC §3(h) still said 'Step 0 (before the size classifier)'; Step 0 IS the classifier (D33-33). Reworded to the D33-33 formulation: the MODEL check is the first content of Step 0, before the classifier's scoring text. The remaining 'before the classifier('s scoring text)' phrasings in SPEC D33-22/D33-33, fix33.py DECISION-33-22/D33-33, verify33.py §16m, and the patch log already use the correct form; the two quotes of the old phrasing (SPEC §3(i) 'reworded' note, fix33.py DECISION-33-33) are explicitly framed as the reworded wording and are left alone.",
    ])
    OWED.extend([
        "OWED-33-1 (Cursor `inherit` behavior is doc-verified, not live-verified): Cursor docs say `inherit` is the subagent default and uses the parent's model, but the plugin has never run with `model: inherit` on these agents. The live test (updated prompt) is the verification; if `inherit` does not hold in a live install, that is a live-test observation, not a fix33 defect in the text.",
        "OWED-33-2 (factory plan doc still pins): FACTORY_CURSOR_PLAN.md still says the orchestrator is Grok 4.7 Extra High. Factory round 4's job; flagged for the coordinator, not fixed here.",
        "OWED-33-3 (cost accounting gap): the regular tree has no cost-accounting text (D33-6). If the audit wants cost recorded per model, that is a new feature (a cost-accounting rule), not a fix33 defect.",
        "OWED-30-3 (live test, carried forward): the updated live-test prompt (fix30/live-test-prompt.md) is still owed Anish's run in Cursor.",
        "OWED-33-5 (observation, audit #111-B B-M3 — NOT fixed, outside scope): review-only multi-agent dispatches (/review-pr's six review agents, /plan's optional second deep-reasoner pass, skill:council's Skeptic/Pragmatist/Critic) carry no MODEL check. Review/deliberation only: no code written, no commit, no deploy, no dispatch of build work. Outside the guardrail's harm model (no build work on an unknown fallback). Recorded for the coordinator to scope; no weave.",
        "OWED-33-4 (RE-OPENED by audit #111-B, FIXED again in round 33d, D33-25/D33-26): direct commands carried no Auto ask (MODELSEL_F33 was orchestrate-only by deliberate design, D33-19). Round 33c wove the guardrail into all 9 direct command entry points (full ask in gan-build/gan-design/astra-review + orch-pipeline Step 0; guardrail reference in each orch-* + orchestrate command file) and marked this SUPERSEDED — but audit #111-B showed the choke-point claim was false for 2 of the 5 orch-* commands (B-B1: the orch-change-feature removal branch never runs the engine; B-B2: orch-build-mvp step 1 runs Phases 0–2, and Step 0 is the classifier, not a phase) plus 4 uncovered entry points (B-B3..B-B6). Round 33d closes all six (D33-25..D33-30) and the verifier gains routing-aware §16n checks. Kept here as history of the deferral, reversal, re-opening, and re-fix; no longer open.",
    ])

    # ---------------------------------------------------------------- main / run log
    _write_log()
    print(f"fix33: {len(CHANGES)} change(s)")
    for c in CHANGES:
        print(f"  - {c}")
    print(f"fix33: {len(OWED)} OWED item(s) recorded in the patch log")
    if ERRORS:
        print(f"fix33: {len(ERRORS)} ERROR(S)", file=sys.stderr)
        for e in ERRORS:
            print(f"  ! {e}", file=sys.stderr)
        sys.exit(1)
    print("fix33: OK")


def _write_log():
    _log_lines = ["# fix33 run log", "",
                  f"## Errors ({len(ERRORS)})"]
    _log_lines += [f"- {e}" for e in ERRORS] or ["- none"]
    _log_lines += ["", f"## Changes ({len(CHANGES)})"]
    _log_lines += [f"- {c}" for c in CHANGES] or ["- none"]
    _log_lines += ["", f"## Command decisions ({len(DECISIONS)})"]
    _log_lines += [f"- {d}" for d in DECISIONS] or ["- none"]
    _log_lines += ["", f"## OWED ({len(OWED)})"]
    _log_lines += [f"- {o}" for o in OWED] or ["- none"]
    _log_dir = os.path.join(ROOT, "fix33")
    os.makedirs(_log_dir, exist_ok=True)
    with open(os.path.join(_log_dir, "fix33-patch-log.md"), "w",
              encoding="utf-8") as _fh:
        _fh.write("\n".join(_log_lines) + "\n")


if __name__ == "__main__":
    main()
