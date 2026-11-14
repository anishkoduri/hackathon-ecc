#!/usr/bin/env python3
"""Weave program #20 — weave the design-decision rule set (fix #19 F2/F3/F4/D19,
fix #20 F4_SCOPE/F5/F6/B1/X1) into every in-scope skill at its decision points
(SPEC §10).

Run once, from ~/workspace/hackathon-plugin as: python3 fix20/weave20.py
Then rebuild twice and verify (verify20.py check 12 covers the weave).

What it does:
  Part A — staged-source edits (each substitution asserts exactly one match):
    design-taste-frontend, orchestrate, pitch-deck-video, polish-pass,
    grill-me, hackathon-scope, feature-expansion.
  Part B — one build.sh patch block, placed LAST just before STEP 5
    (upstream ECC files + the skill-triggers JSON), mirroring weave1/fix20.
  The block adds a one-line pointer at each decision point of every
  in-scope upstream skill, plus 6 new trigger keys (58 -> 64).

The weave adds POINTERS only — no rule text is edited, the canonical block
is untouched, no new skills/agents/rules/commands. Do NOT re-run: the
preflight fails if any pointer is already present.
"""
import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ROOT, "hackathon-ecc")

# ---------------------------------------------------------------------------
# Pointer lines (one line each; the marker is "Design-decision pointer:").
# Naming: the applicable rules by name + the canonical home
# ("design-package rule — Taste step 4a / orchestrate"). No rule text.
# ---------------------------------------------------------------------------
POINTER_FULL = ("**Design-decision pointer:** F2/F3/F4/F5/F6/D19/B1/X1 as "
                "relevant — design-package rule — Taste step 4a / orchestrate.")
POINTER_MOTION = ("**Design-decision pointer:** D19/F6/X1 as relevant "
                  "(motion is a D19 dimension; the experience is the moment) "
                  "— design-package rule — Taste step 4a / orchestrate.")
POINTER_X1 = ("**Design-decision pointer:** D19/F6/X1 as relevant "
              "(UX states are the component's experience — what the user "
              "feels) — design-package rule — Taste step 4a / orchestrate.")
MARKER = "Design-decision pointer:"
BANNED = ["claude", "codex", "anthropic", "opus", "sonnet", "haiku",
          "composer-2.5"]

# ---------------------------------------------------------------------------
# §10 CENSUS (166 staged skills; every skill classified).
# IN_SCOPE maps skill -> number of woven pointer decision points.
# ---------------------------------------------------------------------------
IN_SCOPE = {
    # staged (Part A)
    "design-taste-frontend": 2,   # the deal (run step 4); step 5 checklist
    "orchestrate": 2,             # step 3 slicing (design package in briefs);
                                  # step 5 Verify outcomes to ledger
    "pitch-deck-video": 2,        # step 4 shots.json theme/tokens; storyboard craft
    "polish-pass": 2,             # harmony check (every pass); Design system section
    "grill-me": 1,                # step 5: Design direction: line in the record
    "hackathon-scope": 1,         # scope.md design-direction line
    "feature-expansion": 1,       # Phase 1 lenses (A demo impact, D captivating)
    # upstream (Part B)
    "accessibility": 1,           # When to Use: UI component specifications
    "ai-feature-spec": 1,         # blueprint §10 UX Integration (UX states)
    "browser-qa": 1,              # visual iteration loop (the F6 verdict executor)
    "click-path-audit": 1,        # Step 2: audit each touchpoint
    "design-system": 2,           # Mode 1 generate (direction step);
                                  # Mode 2 visual audit (10 dimensions)
    "frontend-a11y": 1,           # When to Activate: form/interactive components
    "frontend-slides": 1,         # step 3 Discover Style (feeling -> previews)
    "gan-style-harness": 1,       # Evaluation Rubric (Design Quality row)
    "less-flat-ui": 1,            # Check-every-surface decision
    "make-interfaces-feel-better": 1,  # Motion section (feel/timing decisions)
    "motion-advanced": 1,         # Decision Guidance: choosing the API
    "motion-foundations": 1,      # Decision Guidance: choosing a duration
    "motion-patterns": 1,         # Decision Guidance: choosing the pattern
    "orch-add-feature": 1,        # UI change / build-a-surface rule
    "orch-build-mvp": 1,          # step 4: first UI slice writes design-tokens.md
    "orch-change-feature": 1,     # UI change / rebuild-a-surface rule
    "orch-fix-defect": 1,         # UI change / rebuild-a-surface rule
    "orch-pipeline": 1,           # Review: direction RECORDED check + QA loop
    "orch-refine-code": 1,        # UI change / rebuild-a-surface rule
    "ui-ux-pro-max": 1,           # Define the design system (Step 2)
}
assert sum(IN_SCOPE.values()) == 32, sum(IN_SCOPE.values())
assert len(IN_SCOPE) == 27, len(IN_SCOPE)

STACK = ("stack-specific framework/language pattern library — implements a "
         "given design, does not decide visual design")
TEST = ("testing/verification — checks code or behaviour, does not decide UI")
META = ("meta/ops/process — plugin, agent, or project process, "
        "no UI decisions")
BIZ = ("business/content — copy, pitch, or market content, "
       "not UI/visual design")
BACKEND = ("backend/data/infra — server, data, or deployment mechanics, "
           "not UI")

OUT_OF_SCOPE = {}
for _s in ["android-clean-architecture", "angular-developer",
           "backend-patterns", "bengali-nlp", "bun-runtime", "clickhouse-io",
           "compose-multiplatform-patterns", "cpp-coding-standards",
           "dart-flutter-patterns", "django-celery", "django-patterns",
           "dotnet-patterns", "fastapi-patterns", "golang-patterns",
           "hexagonal-architecture", "java-coding-standards", "jpa-patterns",
           "kotlin-coroutines-flows", "kotlin-exposed-patterns",
           "kotlin-ktor-patterns", "kotlin-patterns", "laravel-patterns",
           "mcp-server-patterns", "mybatis-patterns", "mysql-patterns",
           "nestjs-patterns", "nextjs-turbopack", "nuxt4-patterns",
           "perl-patterns", "postgres-patterns", "prisma-patterns",
           "python-patterns", "quarkus-patterns", "rails-patterns",
           "react-native-patterns", "react-patterns", "react-performance",
           "redis-patterns", "rust-patterns", "springboot-patterns",
           "tinystruct-patterns", "typescript-patterns", "vite-patterns",
           "vue-patterns"]:
    OUT_OF_SCOPE[_s] = STACK
for _s in ["ai-regression-testing", "cpp-testing", "csharp-testing",
           "django-tdd", "django-verification", "e2e-testing",
           "flutter-dart-code-review", "fsharp-testing", "golang-testing",
           "kotlin-testing", "laravel-tdd", "laravel-verification",
           "perl-testing", "python-testing", "quarkus-tdd",
           "quarkus-verification", "react-testing", "rust-testing",
           "springboot-tdd", "springboot-verification",
           "verification-before-completion", "verification-loop",
           "windows-desktop-e2e"]:
    OUT_OF_SCOPE[_s] = TEST
for _s in ["agent-introspection-debugging", "agent-self-evaluation",
           "agent-sort", "agents-md-generator", "architecture-decision-records",
           "brownfield-retrospective", "ck", "code-tour", "codebase-memory",
           "codebase-onboarding", "codehealth-mcp", "context-budget",
           "continuous-learning", "continuous-learning-v2",
           "conventional-commit-review", "delivery-gate",
           "dispatching-parallel-agents", "documentation-lookup",
           "ecc-recipes", "git-workflow", "growth-log", "hookify-rules",
           "iterative-retrieval", "laravel-plugin-discovery",
           "living-docs-governance", "loop-design-check",
           "mcp-dependency-review", "opensource-pipeline",
           "plankton-code-quality", "production-audit", "repo-scan",
           "rules-distill", "santa-method", "security-review",
           "security-scan", "skill-scout", "skill-stocktake",
           "story-lifecycle", "strategic-compact", "systematic-debugging",
           "tdd-workflow", "unified-memory"]:
    OUT_OF_SCOPE[_s] = META
for _s in ["article-writing", "content-engine", "devpost-autofiller",
           "hackathon-pitch", "investor-outreach", "market-research",
           "readme-writer"]:
    OUT_OF_SCOPE[_s] = BIZ
for _s in ["api-design", "api-integration", "contract-first",
           "database-migrations", "deploy-fast", "generating-python-installer",
           "integration"]:
    OUT_OF_SCOPE[_s] = BACKEND
# Borderline calls, each with its own recorded reason.
OUT_OF_SCOPE.update({
    "app-scaffold": ("backend scaffolding (Supabase/auth/database) — no UI "
                     "decision text in its SKILL.md; the scaffold's 'final "
                     "layout' ownership is orchestrate's claim, not a "
                     "decision this skill makes"),
    "brainstorming": ("ideation facilitation — explores ideas with the user "
                      "before implementation; makes no UI decisions itself"),
    "coding-standards": ("baseline coding conventions — cross-project code "
                         "style, not UI design"),
    "council": ("decision facilitation (four-voice council) — a process for "
                "ambiguous decisions, not a UI decision-maker"),
    "dev-team": ("persona discussion session (PM/Architect/Developer/QA) — "
                 "discusses designs; decisions land in the skills that act "
                 "on the discussion"),
    "error-handling": ("error-handling patterns (typed errors, retries, "
                       "circuit breakers) — not UI decisions"),
    "frontend-design-direction": ("excluded by hackathon-mode §5 — "
                                  "production UI outside hackathons; its own "
                                  "description forbids hackathon use; never "
                                  "invoked for hackathon UI work"),
    "frontend-patterns": ("framework implementation patterns "
                          "(composition/hooks/state/forms/animation "
                          "implementation) — implements a given design, does "
                          "not decide visual design"),
    "i18n-sync": ("locale-file translation mechanics — copy translation, "
                  "not UI design decisions"),
    "inherit-legacy-style": ("code-convention extraction (file anatomy, "
                             "state, infra, error handling) — not UI/visual "
                             "design; its design-package mention covers "
                             "legacy code style, not visual decisions"),
    "intent-driven-development": ("acceptance-criteria scoping for "
                                  "ambiguous/high-impact changes — "
                                  "product/engineering scoping, not UI "
                                  "decisions"),
    "investor-materials": ("fundraising documents (decks, one-pagers, memos, "
                           "models) — business content; deck layout itself "
                           "is frontend-slides' job"),
    "mobile-ship": ("packaging/deployment of a testable mobile build — "
                    "not UI decisions"),
    "product-lens": ("product validation diagnostics (go/no-go) — business "
                     "decision, not UI; deliberately triggerless per weave1 "
                     "(does not scope hackathons)"),
    "track-picker": ("track/prize matching + integration plan — "
                     "not UI decisions"),
    "ui-to-vue": ("batch conversion of UI screenshots/design exports into "
                  "Vue components — implements a given design, does not "
                  "decide it"),
})
assert len(IN_SCOPE) + len(OUT_OF_SCOPE) == 166, (
    len(IN_SCOPE), len(OUT_OF_SCOPE))
assert not (set(IN_SCOPE) & set(OUT_OF_SCOPE))

# Trigger keys to add (in-scope skills that lack one). Deliberately NOT added:
# orch-pipeline (internal engine, not user-triggered — weave1 precedent) and
# frontend-design-direction (out of scope — hackathon-mode §5 exclusion).
NEW_KEYS = {
    "skill:accessibility": ["make this accessible", "wcag compliance",
                            "accessibility audit", "aria labels"],
    "skill:ai-feature-spec": ["spec an ai feature", "ai feature spec",
                              "specify the ai feature"],
    "skill:gan-style-harness": ["gan build", "generator evaluator loop",
                                "build with the gan harness"],
    "skill:motion-advanced": ["advanced motion", "drag and drop animation",
                              "gesture animation"],
    "skill:motion-foundations": ["motion tokens", "spring animation",
                                 "motion presets"],
    "skill:motion-patterns": ["animate this component", "button animation",
                              "page transition", "modal animation"],
}

# ============================================================================
# PART A — staged sources (edited directly; STEP 2 copies them verbatim)
# Each tuple: (relative path, old anchor, pointer line, label).
# The pointer is appended after the anchor on its own line.
# ============================================================================
STAGED = [
    # --- design-taste-frontend (new-skills/design-taste-frontend/SKILL.md) ---
    ("new-skills/design-taste-frontend/SKILL.md",
     "4. **Deal, never choose by taste.** Each command keeps a history, so pages differ:",
     "\n" + POINTER_FULL, "T1 deal"),
    ("new-skills/design-taste-frontend/SKILL.md",
     "## 5. Checklist",
     "\n" + POINTER_FULL, "T2 step-5 checklist"),
    # --- orchestrate (new-skills/orchestrate/SKILL.md) ---
    ("new-skills/orchestrate/SKILL.md",
     "One writer at a time — never two slices writing the file, never a brief that guesses tokens, never a wait.",
     "\n" + POINTER_FULL, "O1 step-3 slicing"),
    ("new-skills/orchestrate/SKILL.md",
     "Record each Verification-stage check's outcome as one line (check name, findings count, fixed/blocked counts) in `docs/run-ledger-appendix.md`, with a one-line pointer (check count + file) in `.hackathon/run-ledger.md`, before proceeding to polish.",
     "\n" + POINTER_FULL, "O2 step-5 Verify"),
    # --- pitch-deck-video (new-skills/pitch-deck-video/SKILL.md) ---
    ("new-skills/pitch-deck-video/SKILL.md",
     "### 4 · Write `shots.json`",
     "\n" + POINTER_FULL, "P1 shots.json"),
    ("new-skills/pitch-deck-video/SKILL.md",
     "### Storyboard craft — lead with the wow moment",
     "\n" + POINTER_FULL, "P2 storyboard craft"),
    # --- polish-pass (round2-skills/polish-pass/SKILL.md) ---
    ("round2-skills/polish-pass/SKILL.md",
     "There is no standalone harmony skill: this rule, executed by the steps in [reference/polish.md](reference/polish.md), is the harmony check.",
     "\n" + POINTER_FULL, "PP1 harmony check"),
    ("round2-skills/polish-pass/SKILL.md",
     "## Design system",
     "\n" + POINTER_FULL, "PP2 Design system section"),
    # --- grill-me (new-skills/grill-me/SKILL.md) ---
    ("new-skills/grill-me/SKILL.md",
     "Unanswered material branches become accepted unknowns (owner: the builder, resolution point: during the build, per hackathon-mode §7's assumption rule) — they are not blockers.",
     "\n" + POINTER_FULL, "G1 Design direction line"),
    # --- hackathon-scope (rewritten-skills/hackathon-scope/SKILL.md) ---
    ("rewritten-skills/hackathon-scope/SKILL.md",
     "orchestrate's slice briefs and `docs/design-tokens.md` build on this line",
     "\n" + POINTER_FULL, "H1 scope.md design direction"),
    # --- feature-expansion (new-skills/feature-expansion/SKILL.md) ---
    ("new-skills/feature-expansion/SKILL.md",
     "Not decoration: a concrete moment a judge remembers after seeing ten other projects.",
     "\n" + POINTER_FULL, "F1 Lens D captivating"),
]

# ============================================================================
# PART B — build.sh patch block (upstream ECC files + trigger JSON).
# Runs LAST, just before STEP 5, after the fix20 block. Each substitution
# asserts exactly one match in the BUILT file. Same (rel, old, add) shape
# as fix20's block: add is appended after old.
# ============================================================================
UPSTREAM = [
    ("skills/accessibility/SKILL.md",
     "- Defining UI component specifications for Web, iOS, or Android.",
     "\n" + POINTER_FULL, "A1 accessibility When to Use"),
    ("skills/ai-feature-spec/SKILL.md",
     "[Where result appears, loading state, streaming vs batch, feedback mechanism]",
     "\n" + POINTER_X1, "A2 ai-feature-spec UX Integration"),
    ("skills/browser-qa/SKILL.md",
     "Never claim visual verification without actually inspecting the rendered interface.",
     "\n" + POINTER_FULL, "A3 browser-qa visual iteration loop"),
    ("skills/click-path-audit/SKILL.md",
     "For each button/toggle/form submit in the target area:",
     "\n" + POINTER_FULL, "A4 click-path-audit Step 2"),
    ("skills/design-system/SKILL.md",
     "— never competitor sites and never a searched external reference (orchestrate row-10 anti-derivative rule)",
     "\n" + POINTER_FULL, "A5 design-system Mode 1 generate"),
    ("skills/design-system/SKILL.md",
     "Scores your UI across 10 dimensions (0-10 each):",
     "\n" + POINTER_FULL, "A6 design-system Mode 2 audit"),
    ("skills/frontend-a11y/SKILL.md",
     "- Building or reviewing form components (`<input>`, `<select>`, `<textarea>`)",
     "\n" + POINTER_FULL, "A7 frontend-a11y When to Activate"),
    ("skills/frontend-slides/SKILL.md",
     "1. Ask what feeling the deck should create: impressed, energized, focused, inspired.",
     "\n" + POINTER_FULL, "A8 frontend-slides Discover Style"),
    ("skills/gan-style-harness/SKILL.md",
     "do not raise or lower a score for screen distinctiveness.",
     "\n" + POINTER_FULL, "A9 gan-style-harness rubric"),
    ("skills/less-flat-ui/SKILL.md",
     "Never skip the check because a surface is small.",
     "\n" + POINTER_FULL, "A10 less-flat-ui check-every-surface"),
    ("skills/make-interfaces-feel-better/SKILL.md",
     "one-shot entrances or loading sequences.",
     "\n" + POINTER_FULL, "A11 make-interfaces-feel-better Motion"),
    ("skills/motion-advanced/SKILL.md",
     "### Choosing the right advanced API",
     "\n\n" + POINTER_MOTION, "A12 motion-advanced Decision Guidance"),
    ("skills/motion-foundations/SKILL.md",
     "### Choosing a duration",
     "\n\n" + POINTER_MOTION, "A13 motion-foundations Decision Guidance"),
    ("skills/motion-patterns/SKILL.md",
     "### Choosing the right pattern",
     "\n\n" + POINTER_MOTION, "A14 motion-patterns Decision Guidance"),
    ("skills/orch-add-feature/SKILL.md",
     "Pure backend/logic changes with no visual surface are exempt.",
     "\n" + POINTER_FULL, "A15 orch-add-feature UI-change rule"),
    ("skills/orch-build-mvp/SKILL.md",
     "if it is missing, prepend it — never start the loop on a rubric without it.",
     "\n" + POINTER_FULL, "A16 orch-build-mvp step 4"),
    ("skills/orch-change-feature/SKILL.md",
     "Pure backend/logic changes with no visual surface are exempt.",
     "\n" + POINTER_FULL, "A17 orch-change-feature UI-change rule"),
    ("skills/orch-fix-defect/SKILL.md",
     "Pure backend/logic changes with no visual surface are exempt.",
     "\n" + POINTER_FULL, "A18 orch-fix-defect UI-change rule"),
    ("skills/orch-pipeline/SKILL.md",
     "if the app cannot run, record that as blocked with evidence instead of iterating.",
     "\n" + POINTER_FULL, "A19 orch-pipeline Review"),
    ("skills/orch-refine-code/SKILL.md",
     "Pure backend/logic changes with no visual surface are exempt.",
     "\n" + POINTER_FULL, "A20 orch-refine-code UI-change rule"),
    ("skills/ui-ux-pro-max/SKILL.md",
     "so any later slice can recover which direction the UI traces to.",
     "\n" + POINTER_FULL, "A21 ui-ux-pro-max define design system"),
]
assert len(STAGED) == 11 and len(UPSTREAM) == 21, (len(STAGED), len(UPSTREAM))

# The build.sh block (raw string; inserted before "# STEP 5 — Counts").
# NOTE: keep the triple-double-quoted subs literal; no ''' sequence may
# appear inside this string.
BLOCK = r'''# --- Weave program #20: design-decision pointers at every decision point
# (SPEC §10, ordered Nov 11 evening). Upstream ECC files, patched on every
# build — this block runs before STEP 5, after the fix20 block.
# Staged-source edits live in fix20/weave20.py Part A; this block covers
# only files no staged source owns, plus the skill-triggers JSON.
# Each substitution asserts exactly one match in the BUILT file. The weave
# adds POINTERS only — no rule text, no canonical-block change, no new
# skills/agents/rules/commands.
python3 - "$PLUGIN_DIR" <<'PYEOF'
import json, os, sys
base = sys.argv[1]
subs = [
  # A1: accessibility — When to Use (UI component specifications).
  ("skills/accessibility/SKILL.md",
   "- Defining UI component specifications for Web, iOS, or Android.",
   """
**Design-decision pointer:** F2/F3/F4/F5/F6/D19/B1/X1 as relevant — design-package rule — Taste step 4a / orchestrate."""),
  # A2: ai-feature-spec — blueprint section 10 UX Integration (UX states).
  ("skills/ai-feature-spec/SKILL.md",
   "[Where result appears, loading state, streaming vs batch, feedback mechanism]",
   """
**Design-decision pointer:** D19/F6/X1 as relevant (UX states are the component's experience — what the user feels) — design-package rule — Taste step 4a / orchestrate."""),
  # A3: browser-qa — visual iteration loop (the F6 verdict executor).
  ("skills/browser-qa/SKILL.md",
   "Never claim visual verification without actually inspecting the rendered interface.",
   """
**Design-decision pointer:** F2/F3/F4/F5/F6/D19/B1/X1 as relevant — design-package rule — Taste step 4a / orchestrate."""),
  # A4: click-path-audit — Step 2 audit each touchpoint.
  ("skills/click-path-audit/SKILL.md",
   "For each button/toggle/form submit in the target area:",
   """
**Design-decision pointer:** F2/F3/F4/F5/F6/D19/B1/X1 as relevant — design-package rule — Taste step 4a / orchestrate."""),
  # A5: design-system — Mode 1 generate (direction step).
  ("skills/design-system/SKILL.md",
   "— never competitor sites and never a searched external reference (orchestrate row-10 anti-derivative rule)",
   """
**Design-decision pointer:** F2/F3/F4/F5/F6/D19/B1/X1 as relevant — design-package rule — Taste step 4a / orchestrate."""),
  # A6: design-system — Mode 2 visual audit (10 dimensions).
  ("skills/design-system/SKILL.md",
   "Scores your UI across 10 dimensions (0-10 each):",
   """
**Design-decision pointer:** F2/F3/F4/F5/F6/D19/B1/X1 as relevant — design-package rule — Taste step 4a / orchestrate."""),
  # A7: frontend-a11y — When to Activate (form/interactive components).
  ("skills/frontend-a11y/SKILL.md",
   "- Building or reviewing form components (`<input>`, `<select>`, `<textarea>`)",
   """
**Design-decision pointer:** F2/F3/F4/F5/F6/D19/B1/X1 as relevant — design-package rule — Taste step 4a / orchestrate."""),
  # A8: frontend-slides — step 3 Discover Style (feeling -> previews).
  ("skills/frontend-slides/SKILL.md",
   "1. Ask what feeling the deck should create: impressed, energized, focused, inspired.",
   """
**Design-decision pointer:** F2/F3/F4/F5/F6/D19/B1/X1 as relevant — design-package rule — Taste step 4a / orchestrate."""),
  # A9: gan-style-harness — Evaluation Rubric (Design Quality row).
  ("skills/gan-style-harness/SKILL.md",
   "do not raise or lower a score for screen distinctiveness.",
   """
**Design-decision pointer:** F2/F3/F4/F5/F6/D19/B1/X1 as relevant — design-package rule — Taste step 4a / orchestrate."""),
  # A10: less-flat-ui — check-every-surface decision.
  ("skills/less-flat-ui/SKILL.md",
   "Never skip the check because a surface is small.",
   """
**Design-decision pointer:** F2/F3/F4/F5/F6/D19/B1/X1 as relevant — design-package rule — Taste step 4a / orchestrate."""),
  # A11: make-interfaces-feel-better — Motion section (feel/timing decisions).
  ("skills/make-interfaces-feel-better/SKILL.md",
   "one-shot entrances or loading sequences.",
   """
**Design-decision pointer:** F2/F3/F4/F5/F6/D19/B1/X1 as relevant — design-package rule — Taste step 4a / orchestrate."""),
  # A12: motion-advanced — Decision Guidance (choosing the API).
  ("skills/motion-advanced/SKILL.md",
   "### Choosing the right advanced API",
   """

**Design-decision pointer:** D19/F6/X1 as relevant (motion is a D19 dimension; the experience is the moment) — design-package rule — Taste step 4a / orchestrate."""),
  # A13: motion-foundations — Decision Guidance (choosing a duration).
  ("skills/motion-foundations/SKILL.md",
   "### Choosing a duration",
   """

**Design-decision pointer:** D19/F6/X1 as relevant (motion is a D19 dimension; the experience is the moment) — design-package rule — Taste step 4a / orchestrate."""),
  # A14: motion-patterns — Decision Guidance (choosing the pattern).
  ("skills/motion-patterns/SKILL.md",
   "### Choosing the right pattern",
   """

**Design-decision pointer:** D19/F6/X1 as relevant (motion is a D19 dimension; the experience is the moment) — design-package rule — Taste step 4a / orchestrate."""),
  # A15: orch-add-feature — UI change / build-a-surface rule.
  ("skills/orch-add-feature/SKILL.md",
   "Pure backend/logic changes with no visual surface are exempt.",
   """
**Design-decision pointer:** F2/F3/F4/F5/F6/D19/B1/X1 as relevant — design-package rule — Taste step 4a / orchestrate."""),
  # A16: orch-build-mvp — step 4 (first UI slice writes design-tokens.md).
  ("skills/orch-build-mvp/SKILL.md",
   "if it is missing, prepend it — never start the loop on a rubric without it.",
   """
**Design-decision pointer:** F2/F3/F4/F5/F6/D19/B1/X1 as relevant — design-package rule — Taste step 4a / orchestrate."""),
  # A17: orch-change-feature — UI change / rebuild-a-surface rule.
  ("skills/orch-change-feature/SKILL.md",
   "Pure backend/logic changes with no visual surface are exempt.",
   """
**Design-decision pointer:** F2/F3/F4/F5/F6/D19/B1/X1 as relevant — design-package rule — Taste step 4a / orchestrate."""),
  # A18: orch-fix-defect — UI change / rebuild-a-surface rule.
  ("skills/orch-fix-defect/SKILL.md",
   "Pure backend/logic changes with no visual surface are exempt.",
   """
**Design-decision pointer:** F2/F3/F4/F5/F6/D19/B1/X1 as relevant — design-package rule — Taste step 4a / orchestrate."""),
  # A19: orch-pipeline — Review (direction RECORDED check + QA loop).
  ("skills/orch-pipeline/SKILL.md",
   "if the app cannot run, record that as blocked with evidence instead of iterating.",
   """
**Design-decision pointer:** F2/F3/F4/F5/F6/D19/B1/X1 as relevant — design-package rule — Taste step 4a / orchestrate."""),
  # A20: orch-refine-code — UI change / rebuild-a-surface rule.
  ("skills/orch-refine-code/SKILL.md",
   "Pure backend/logic changes with no visual surface are exempt.",
   """
**Design-decision pointer:** F2/F3/F4/F5/F6/D19/B1/X1 as relevant — design-package rule — Taste step 4a / orchestrate."""),
  # A21: ui-ux-pro-max — Define the design system (Step 2).
  ("skills/ui-ux-pro-max/SKILL.md",
   "so any later slice can recover which direction the UI traces to.",
   """
**Design-decision pointer:** F2/F3/F4/F5/F6/D19/B1/X1 as relevant — design-package rule — Taste step 4a / orchestrate."""),
]
for rel, old, add in subs:
    p = os.path.join(base, rel)
    t = open(p, encoding="utf-8").read()
    n = t.count(old)
    assert n == 1, f"weave20 anchor not found exactly once in {rel}: {old[:70]!r} (count={n})"
    if old + add in t:
        continue
    open(p, "w", encoding="utf-8").write(t.replace(old, old + add))
print("weave20: upstream skill pointers applied")

# Trigger keys for in-scope skills that lack one (6 new keys, 58 -> 64).
# Deliberately NOT added: orch-pipeline (internal engine, weave1 precedent)
# and frontend-design-direction (out of scope — hackathon-mode section 5).
tp = os.path.join(base, "manifests/context-packs/skill-triggers@1.json")
data = json.load(open(tp, encoding="utf-8"))
tr = data["triggers"]
assert data["coverage"]["withTriggers"] == 58, data["coverage"]
new_keys = {
  "skill:accessibility": ["make this accessible", "wcag compliance",
                          "accessibility audit", "aria labels"],
  "skill:ai-feature-spec": ["spec an ai feature", "ai feature spec",
                            "specify the ai feature"],
  "skill:gan-style-harness": ["gan build", "generator evaluator loop",
                              "build with the gan harness"],
  "skill:motion-advanced": ["advanced motion", "drag and drop animation",
                            "gesture animation"],
  "skill:motion-foundations": ["motion tokens", "spring animation",
                               "motion presets"],
  "skill:motion-patterns": ["animate this component", "button animation",
                            "page transition", "modal animation"],
}
seen = [p for v in tr.values() for p in v]
for k, v in new_keys.items():
    assert k not in tr, f"trigger key already exists: {k}"
    for p in v:
        assert p not in seen, f"trigger phrase already used elsewhere: {p!r}"
    tr[k] = v
data["triggers"] = {k: tr[k] for k in sorted(tr)}
data["coverage"]["withTriggers"] = len(data["triggers"])
assert data["coverage"]["withTriggers"] == 64, data["coverage"]
open(tp, "w", encoding="utf-8").write(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
print("weave20: skill-triggers updated (58 -> 64 keys)")
PYEOF

'''

def sub(path, old, add, label):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    n = text.count(old)
    assert n == 1, f"{label}: pattern found {n}x (expected 1): {old[:70]!r}"
    if old + add in text:
        print(f"  already applied {label} (skipping)")
        return
    with open(path, "w", encoding="utf-8") as f:
        f.write(text.replace(old, old + add))
    print(f"  applied {label}")


def main():
    # ---- Preflight 0: banned terms in every added string. ----
    added = [POINTER_FULL, POINTER_MOTION, POINTER_X1, BLOCK]
    added += [a for _, _, a, _ in STAGED] + [a for _, _, a, _ in UPSTREAM]
    for s in added:
        for b in BANNED:
            assert b not in s.lower(), f"banned term {b!r} in added text"
    print("preflight: banned terms 0 in all added text")

    # ---- Preflight 1: census covers the built skill set exactly. ----
    built = sorted(os.listdir(os.path.join(BASE, "skills")))
    assert set(built) == set(IN_SCOPE) | set(OUT_OF_SCOPE), (
        "census mismatch vs built skills:",
        sorted(set(built) - (set(IN_SCOPE) | set(OUT_OF_SCOPE))),
        sorted((set(IN_SCOPE) | set(OUT_OF_SCOPE)) - set(built)))
    print(f"preflight: census covers all {len(built)} built skills "
          f"({len(IN_SCOPE)} in scope, {len(OUT_OF_SCOPE)} out of scope)")

    # ---- Preflight 2: every staged anchor matches exactly once, and no
    # staged target already carries a pointer. ----
    for rel, old, add, label in STAGED:
        p = os.path.join(ROOT, rel)
        text = open(p, encoding="utf-8").read()
        assert text.count(old) == 1, (
            f"{label}: staged anchor found {text.count(old)}x: {old[:70]!r}")
    print(f"preflight: {len(STAGED)} staged anchors all count==1")

    # ---- Preflight 3: every upstream anchor matches exactly once in the
    # CURRENT built tree, and no built target already carries a pointer. ----
    for rel, old, add, label in UPSTREAM:
        p = os.path.join(BASE, rel)
        text = open(p, encoding="utf-8").read()
        assert text.count(old) == 1, (
            f"{label}: built anchor found {text.count(old)}x: {old[:70]!r}")
    print(f"preflight: {len(UPSTREAM)} upstream anchors all count==1 "
          "in the post-fix20 built tree")

    # ---- Preflight 4: the BLOCK's subs mirror UPSTREAM exactly, and the
    # block's trigger keys mirror NEW_KEYS. ----
    for rel, old, add, label in UPSTREAM:
        assert f'("{rel}",' in BLOCK, f"block missing sub for {rel}"
        assert old in BLOCK, f"block missing anchor for {label}"
    for k in NEW_KEYS:
        assert f'"{k}":' in BLOCK, f"block missing trigger key {k}"
    assert "# --- Weave program #20" not in open(
        os.path.join(ROOT, "build.sh"), encoding="utf-8").read(), (
        "weave20 block already in build.sh — do not re-run")
    print("preflight: block mirrors UPSTREAM + NEW_KEYS; block not yet in build.sh")

    # ---- Preflight 5: trigger JSON baseline (58 keys, all resolving). ----
    tp = os.path.join(BASE, "manifests/context-packs/skill-triggers@1.json")
    data = json.load(open(tp, encoding="utf-8"))
    assert len(data["triggers"]) == 58, len(data["triggers"])
    assert data["coverage"]["withTriggers"] == 58
    for k in data["triggers"]:
        name = k[len("skill:"):]
        assert os.path.isfile(os.path.join(
            BASE, "skills", name, "SKILL.md")), f"unresolving key: {k}"
    seen = [p for v in data["triggers"].values() for p in v]
    for k, v in NEW_KEYS.items():
        assert k not in data["triggers"]
        for p in v:
            assert p not in seen, f"phrase collision: {p!r}"
    print("preflight: triggers baseline 58 keys, all resolving, no phrase collisions")

    # ---- Part A: staged edits. ----
    for rel, old, add, label in STAGED:
        sub(os.path.join(ROOT, rel), old, add, label)
    print("weave20: Part A staged edits applied")

    # ---- Part B: insert the block LAST, just before STEP 5. ----
    buildsh = os.path.join(ROOT, "build.sh")
    with open(buildsh, encoding="utf-8") as f:
        btext = f.read()
    anchor = "# STEP 5 — Counts"
    assert btext.count(anchor) == 1, f"STEP 5 anchor found {btext.count(anchor)}x"
    with open(buildsh, "w", encoding="utf-8") as f:
        f.write(btext.replace(anchor, BLOCK + anchor, 1))
    print("weave20: Part B block inserted (LAST, before STEP 5)")

    # ---- Report the new build.sh identity for the pin bumps. ----
    nb = open(buildsh, encoding="utf-8").read()
    print(f"weave20: build.sh now {len(nb.splitlines())} lines, "
          f"md5={hashlib.md5(nb.encode('utf-8')).hexdigest()}")
    print("weave20: done — rebuild twice, then run fix20/verify20.py")


if __name__ == "__main__":
    main()
