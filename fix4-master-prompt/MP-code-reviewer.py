# Master prompt (fix program #4): ecc-code-reviewer — adversarial audit
# stance + CONFIRMED-vs-SUSPECTED distinction.
# Upstream ECC file (agents copied fresh from the ECC Developer install on
# every build) — this fix lives here as a patch block placed LAST — just
# before STEP 5 — after the GATE / carve-out / Batch E / Batch F /
# fix-program-#3 patches, whose old-strings the substitution below is
# anchored on (i.e. against the CURRENT built text).
# Never edit hackathon-ecc/ directly. The substitution asserts exactly one
# match. The coordinator inserts this block last, just before STEP 5.
#
# Target note: the task named skills/code-reviewer/SKILL.md, but no such
# skill exists in the plugin — code review lives in the AGENT
# agents/ecc-code-reviewer.md (upstream ECC, copied from the install at
# build.sh :106-111). This snippet targets that agent file instead.
# The adversarial stance does NOT belong in agents/ecc-security-reviewer.md:
# that agent is security-only (OWASP Top 10, secrets, injection) and
# already ends "Be thorough, be paranoid, be proactive." (:116); the master
# prompt's hunt list is broader than security (functional bugs, race
# conditions, state management, performance, accessibility, duplicated
# code), so it belongs here. No snippet for security-reviewer.
#
# What it adds, and what it deliberately does NOT duplicate:
# - Severity classification already exists (CRITICAL / HIGH / MEDIUM / LOW
#   throughout, summary table, Approval Criteria) — NOT re-added.
# - The >80% confidence filter (:26, :32), the Pre-Report Gate, and
#   "HIGH / CRITICAL Require Proof" already exist — NOT re-added. The new
#   CONFIRMED-vs-SUSPECTED labels sit on top of them: a SUSPECTED finding
#   is reported with the repro/test that would settle it and never blocks
#   on its own, and the Pre-Report Gate still decides whether it is
#   reported at all.
# - The checklist already covers most hunt areas (security, error handling,
#   unvalidated input, state updates in render / stale closures, N+1,
#   performance, dead code, missing tests). What was missing was the
#   STANCE itself — no "skeptical"/"adversarial" framing anywhere in the
#   file — plus explicit naming of race conditions and accessibility
#   failures, which the checklist never mentions. Added here as stance
#   prose, not new checklist sections.
# - No approval gate, no wait point, no new agent/skill/file.
python3 - "$PLUGIN_DIR" <<'PYEOF'
import os, sys
base = sys.argv[1]
subs = [
  # Master prompt — adversarial audit stance + CONFIRMED vs SUSPECTED.
  ("agents/ecc-code-reviewer.md",
   r'''You are a senior code reviewer ensuring high standards of code quality and security.''',
   r'''You are a senior code reviewer ensuring high standards of code quality and security.

**Adversarial stance:** review as a skeptical staff engineer reading someone else's implementation — assume every claim in the code is unproven until the code, its callers, or a test proves it. Hunt across every checklist category below for incorrect assumptions, functional bugs, security vulnerabilities, broken user journeys, race conditions, state-management problems, unhandled edge cases, performance bottlenecks, accessibility failures, duplicated or unnecessary code, fragile integrations, missing validation, and inadequate tests. Fix root causes, not symptoms, and re-run tests after fixes.

**CONFIRMED vs SUSPECTED:** label every finding CONFIRMED (you traced it to a concrete failing input, state, or outcome) or SUSPECTED (a plausible risk you cannot yet prove — name the repro or test that would confirm it). Never present a SUSPECTED risk as CONFIRMED. A SUSPECTED finding is reported with the repro/test that would settle it and never blocks on its own; the Pre-Report Gate below still decides whether it is reported at all.'''),
]
for rel, old, new in subs:
    p = os.path.join(base, rel)
    text = open(p, encoding="utf-8").read()
    assert text.count(old) == 1, f"{rel}: pattern not found exactly once: {old[:60]!r}"
    open(p, "w", encoding="utf-8").write(text.replace(old, new))
print("master-prompt ecc-code-reviewer adversarial stance applied")
PYEOF
