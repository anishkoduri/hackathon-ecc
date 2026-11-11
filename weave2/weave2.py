#!/usr/bin/env python3
"""Weave fix program #2 — dry-run #12 findings (B1 blocking, M1 + M2 minor).

Audit #40 was ZERO ERRORS; dry-run #12 was NOT CLEAN. All three findings
were verified against the built files before fixing (see weave2/MANIFEST.md).

- B1: weave1's deferred-six invocation contradicts hackathon-mode §3/§7
  ("never fire — not even if another skill invokes them"). Fix: an explicit
  carve-out in §3 and §7 naming the end-of-project run immediately before
  the first build's final report as "the very end of the project" — it runs
  once, never gates a feature, never fires mid-build or during a removal.
  This is a clarification of WHEN the deferred set fires, not an expansion
  of the §7 auto-approval scope (no gate removed, no question added).
- M1: the weave1 ledger loads exceed the ledger's 20-line cap. Fix: bulky
  loads (task_list, Verify lines, polish 10-list) live in
  docs/run-ledger-appendix.md with a one-line pointer in the ledger.
- M2: theme.mjs's missing-field list demands an 'entry' field no log entry
  can carry (upstream Hallmark bug — 'entry' is the CLI flag name), and the
  Taste:240 citation reads gates.md:187 where the repetition rule is :189.

Applies staged-source edits (each substitution asserts exactly one match)
and inserts the weave2 build.sh patch block LAST, just before STEP 5 (after
the weave1 block — weave2 anchors depend on weave1's output).
Run from ~/workspace/hackathon-plugin as: python3 weave2/weave2.py
Then rebuild twice and verify diff = 0.
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def sub(path, old, new, label):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    n = text.count(old)
    assert n == 1, f"{label}: pattern found {n}x (expected 1): {old[:70]!r}"
    with open(path, "w", encoding="utf-8") as f:
        f.write(text.replace(old, new))
    print(f"  applied {label}")


# ============================================================================
# PART A — staged sources
# ============================================================================

# ---- A1: hackathon-mode (new-rules/hackathon-mode.mdc) — B1 carve-out ----
hmode = os.path.join(ROOT, "new-rules/hackathon-mode.mdc")

sub(hmode,
    "During the first build (and during a one-prompt removal of a first-build feature) the deferred skills never fire — not even if another skill, rule, or reference file invokes them. The registry cannot enforce this; this rule is the gate.",
    "During the first build (and during a one-prompt removal of a first-build feature) the deferred skills never fire — not even if another skill, rule, or reference file invokes them. The registry cannot enforce this; this rule is the gate. The one permitted invocation is the named end-of-project run immediately before the first build's final report (after deploy, demo, commit, and README): that run IS the very end of the project — it runs once, it never gates a feature, and it never fires mid-build or during a one-prompt removal.",
    "B1 §3 carve-out: end-of-project run is the very end")

sub(hmode,
    "§7 overrides any ask/stop/wait instruction in any skill, rule, or reference file during the first build and during one-prompt removal. The deferred skills from §3 never fire during the first build or a one-prompt removal — the registry cannot enforce this, so this rule is the gate.",
    "§7 overrides any ask/stop/wait instruction in any skill, rule, or reference file during the first build and during one-prompt removal. The deferred skills from §3 never fire during the first build or a one-prompt removal — the registry cannot enforce this, so this rule is the gate. (Exception: the single named end-of-project run immediately before the first build's final report — §3 — is the very end of the project, not 'during the first build' for this rule; it runs once, after deploy/demo/commit/README, and never gates a feature.)",
    "B1 §7 carve-out: end-of-project run exception")

# ---- A2: orchestrate (new-skills/orchestrate/SKILL.md) ----
orch = os.path.join(ROOT, "new-skills/orchestrate/SKILL.md")

# M1: the ledger cap gets its overflow rule (appendix file + pointer).
sub(orch,
    "The **stage ledger** stays a short run-state file (20 lines max), not a PRD.",
    "The **stage ledger** stays a short run-state file (20 lines max), not a PRD. Bulky loads overflow to `docs/run-ledger-appendix.md` (one line per item) with a one-line pointer in the ledger — the 20-line cap applies to the ledger file itself.",
    "M1 ledger overflow rule")

# M1: Verify outcomes go to the appendix with a ledger pointer.
sub(orch,
    "Record each Verification-stage check's outcome as one ledger line (check name, findings count, fixed/blocked counts) in `.hackathon/run-ledger.md` before proceeding to polish.",
    "Record each Verification-stage check's outcome as one line (check name, findings count, fixed/blocked counts) in `docs/run-ledger-appendix.md`, with a one-line pointer (check count + file) in `.hackathon/run-ledger.md`, before proceeding to polish.",
    "M1 Verify outcomes to appendix")

# M1: the polish 10-list goes to the appendix with a ledger pointer.
sub(orch,
    "It returns the 10 highest-impact REMAINING improvements, prioritized by impact/effort/risk, recorded in `.hackathon/run-ledger.md`;",
    "It returns the 10 highest-impact REMAINING improvements, prioritized by impact/effort/risk, recorded in `docs/run-ledger-appendix.md` (one line per improvement) with a one-line pointer in `.hackathon/run-ledger.md`;",
    "M1 polish 10-list to appendix")

# B1: the O9b invocation cites the §3 carve-out as its authority.
sub(orch,
    "This is the deferred set's named end-of-project invocation (orchestrate process rule); it is not a user gate and never waits on anything.",
    "This is the deferred set's named end-of-project invocation (per the hackathon-mode §3 carve-out, this run is the very end of the project, not 'during the first build' for the deferral rule); it is not a user gate and never waits on anything.",
    "B1 O9b cites the §3 carve-out")

# ---- A3: design-taste-frontend (new-skills/design-taste-frontend/SKILL.md) ----
taste = os.path.join(ROOT, "new-skills/design-taste-frontend/SKILL.md")

# M2: the repetition rule is at gates.md:189, not :187.
sub(taste,
    "so the repetition check (gates.md:187) reads the real page.",
    "so the repetition check (gates.md:189) reads the real page.",
    "M2 repetition-rule citation :187 -> :189")

# ---- A4: theme.mjs (staged Hallmark script) ----
theme = os.path.join(ROOT, "new-skills/design-taste-frontend/references/hallmark/scripts/theme.mjs")

# M2: 'entry' is the CLI flag name (--entry), not a log-entry field — no log
# entry can ever carry entry['entry'], so the warning could never clear.
# Upstream Hallmark bug; one-token fix in the staged script.
sub(theme,
    "const missing = [...(composed ? ['shape', 'axes', 'hero', 'nav', 'footer', 'imagery', 'entry', 'fingerprint', 'sections', 'signature'] : []), ...(entry.depth === 'polish' ? [] : ['theme']), 'prompt'].filter((k) => !entry[k]);",
    "const missing = [...(composed ? ['shape', 'axes', 'hero', 'nav', 'footer', 'imagery', 'fingerprint', 'sections', 'signature'] : []), ...(entry.depth === 'polish' ? [] : ['theme']), 'prompt'].filter((k) => !entry[k]);",
    "M2 drop unfillable 'entry' from the missing-field list")

print("weave2: Part A staged edits applied")

# ============================================================================
# PART B — build.sh patch block (runs LAST, before STEP 5, after weave1)
# ============================================================================
buildsh = os.path.join(ROOT, "build.sh")
with open(buildsh, encoding="utf-8") as f:
    btext = f.read()
anchor = "# STEP 5 — Counts"
assert btext.count(anchor) == 1, f"STEP 5 anchor found {btext.count(anchor)}x"
block = r'''# --- Weave fix program #2 (dry-run #12: B1 blocking, M1 + M2 minor).
# Upstream ECC files, copied fresh on every build — this block runs LAST,
# just before STEP 5, AFTER the weave1 block (its anchors depend on weave1's
# output). Each substitution asserts exactly one match.
python3 - "$PLUGIN_DIR" <<'PYEOF'
import os, sys
base = sys.argv[1]
subs = [
  # M1: the approved task_list lives in the appendix, pointer in the ledger.
  ("skills/orch-pipeline/SKILL.md",
   """Record the approved `task_list` (one line per slice, with its files) in `.hackathon/run-ledger.md` at Gate 1, so later phases read it from there instead of the transcript.""",
   """Record the approved `task_list` (one line per slice, with its files) in `docs/run-ledger-appendix.md` at Gate 1, with a one-line pointer (slice count + file) in `.hackathon/run-ledger.md`, so later phases read it from there instead of the transcript."""),
  # B1: the step-9 invocation cites the §3 carve-out as its authority.
  ("skills/orch-build-mvp/SKILL.md",
   """Before writing the report, run the six deferred end-of-project checks by name (`verification-loop`, `production-audit`, `delivery-gate`, `codehealth-mcp`, `santa-method`, `security-scan`) and record each result in the report (check name, pass/fail, findings count).""",
   """Before writing the report, run the six deferred end-of-project checks by name (`verification-loop`, `production-audit`, `delivery-gate`, `codehealth-mcp`, `santa-method`, `security-scan`) and record each result in the report (check name, pass/fail, findings count). (Per the hackathon-mode §3 carve-out, this run is the very end of the project, not 'during the first build' for the deferral rule; it runs once, after deploy/demo/commit/README, and never gates a feature.)"""),
]
for rel, old, new in subs:
    p = os.path.join(base, rel)
    text = open(p, encoding="utf-8").read()
    assert text.count(old) == 1, f"{rel}: pattern not found exactly once: {old[:60]!r}"
    open(p, "w", encoding="utf-8").write(text.replace(old, new))
print("weave2: upstream patches applied")
PYEOF

'''
btext = btext.replace(anchor, block + anchor, 1)
with open(buildsh, "w", encoding="utf-8") as f:
    f.write(btext)
print("  applied weave2 build.sh patch block (LAST, before STEP 5)")

print("weave2: all staged edits + build.sh block applied")
