#!/usr/bin/env python3
"""verify27.py -- checks fix #27 in the BUILT tree (read-only).

Run after a build: python3 fix27/verify27.py [built-plugin-dir]
Default built dir: ~/workspace/hackathon-plugin/hackathon-ecc.
Exits 0 only if every check passes.

Fix #27 (SPEC fix27/SPEC.md): debloat 166 -> 67 skills (100 CUT, +1 MotionSites),
27 companion agents removed (72 -> 45), 32 CUT-only commands dropped
(87 -> 55), rules unchanged at 123, trigger keys 64 -> 49, README count
lines updated, plus the build-time text patches (delivery-gate :97,
browser-qa single capture run, verification-before-completion claim row,
hackathon-pitch CHECK-THE-SOURCE + AUDIT-AS-GUIDE, no-Co-authored-by
rule, orchestrate git-workflow re-route, security-review dispatch
removal, deferred-list six -> three).

Round 2 (audit #74): skills 66 -> 67 (motionsites-web-builder vendored),
commands 60 -> 55 (learn-eval, project-init, projects, promote, prune
CUT), trigger coverage.skills 66 -> 67, README counts 67/55, plus the
reference-cleanup patches (B1, B2, B5, B6, B7, B8, B9, B10, B11, B12,
B13, B15, M3, M4, M5, M6) and the CUT-name sweep (check 12).

Round 3 (audit #75): B-new-1 typescript-reviewer reword (drop
coding-standards) + its check-12 allow entry removed; M-new-1
accessibility -> frontend-a11y re-points (8 lines) + their allow
entries removed; M-new-2 OWED-13 record update; M-new-4 pi-core.json
prune; M-new-6 check-10b memory-learning-skill assertion; check 12b
(no imperative dispatch hides in an allow-listed line).

Checks:
  1. Counts: skills 66, agents 45, rules 123, commands 60; exact dir
     sets match the hardcoded KEPT lists (no extra, none missing).
  2. All 100 CUT skill dirs absent; all 66 KEPT skill dirs present.
  3. Removed agents absent; kept agents present (exact set).
  4. Dropped commands absent; kept commands present (exact set).
  5. Trigger file parses as JSON, zero keys pointing at CUT skills,
     49 keys remain, coverage.skills == 66, withTriggers == 49.
  6. README count lines show the new counts; zero "166 skills" /
     "72 agents" / "87 commands" remain in the built tree (excl.
     node_modules). The stock-ECC line ("144 skills, 69 agents") is
     untouched by design.
  7. Every _F27 anchor token exists in the built tree (18):
     DESIGNPKG-AUTO_F27, CEILING_F27, DELRISK_F27, CHECKSRC_F27,
     AUDITGUIDE_F27, NOCOAUTHOR_F27, THEME-START_F27, ALWAYSLEAD_F27,
     IMPL46_F27, GRILLHDR_F27, CAPTURE1_F27, TESTNOTBQA_F27,
     DEFER3_F27, W2_F27, W3_F27, W4_F27, TESTPASS_F27, REROUTE_F27.
     Most are written in the staged sources; CHECKSRC, AUDITGUIDE,
     NOCOAUTHOR, CAPTURE1, TESTNOTBQA and DEFER3 are additionally
     written by fix27.py where they live in ECC/marketplace-origin
     files the staged worker did not touch. A missing token FAILS
     here by design -- that is the verifier's job; do not weaken
     the check.
  8. Banned terms: 0 in the built tree (case-insensitive, excl.
     node_modules). (The banned list appears in THIS file only, as the
     check pattern -- same precedent as verify26.py -- never in the
     built tree.)
  9. Grok pins: grok-4.7-high and cursor-grok-4.6-high-fast present;
     bare grok-4.6-high-fast count is 0 in the built tree.
 10. Every fix27.py patch anchor still present exactly once (re-assert
     the new texts; old texts gone), so a later rebuild cannot
     silently drop them.
 11. fix27 patch log exists with 0 errors.
 12. CUT-name sweep (audit #74 M10): every CUT skill name, removed
     agent name and dropped command name occurs zero times as a live
     dispatch in skills/, agents/, commands/, rules/ (excluding the
     regenerated call map and the trigger manifest), except for the
     explicit ALLOW_LIST of prose-history / negative / pointer-style
     mentions (file -> allowed lines, each justified). Generic-word
     bare uses (accessibility, brainstorming, evolve, projects,
     promote, prune) are noise, not dispatches, and are counted
     separately; their strong forms (backticked / pathed / slashed)
     are still swept.
 12b. No imperative dispatch hides in an allow-listed line (audit #75
     B-new-1): every whole-line allow-listed line is re-scanned for an
     imperative verb (use/check/consult/run/invoke/call/load/read)
     with a CUT name backticked or followed by skill/agent/command
     within 120 characters after the verb, except negated verbs and
     "was cut" / "NOT invoked" historical notes (see the check-12b
     comment for the three pinned-down readings).
"""
import json
import os
import subprocess
import sys

HOME = os.path.expanduser("~")
PLUGIN = os.path.join(HOME, "workspace/hackathon-plugin")
BASE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(PLUGIN, "hackathon-ecc")

CUT_SKILLS = [
    "accessibility", "agent-introspection-debugging", "agent-self-evaluation",
    "agent-sort", "agents-md-generator", "ai-regression-testing",
    "android-clean-architecture", "angular-developer",
    "architecture-decision-records", "article-writing", "bengali-nlp",
    "brainstorming", "brownfield-retrospective", "bun-runtime",
    "clickhouse-io", "code-tour", "codebase-memory", "codebase-onboarding",
    "codehealth-mcp", "coding-standards", "compose-multiplatform-patterns",
    "content-engine", "continuous-learning", "continuous-learning-v2",
    "conventional-commit-review", "cpp-coding-standards", "cpp-testing",
    "csharp-testing", "dart-flutter-patterns", "database-migrations",
    "dev-team", "dispatching-parallel-agents", "django-celery",
    "django-patterns", "django-tdd", "django-verification", "dotnet-patterns",
    "ecc-recipes", "flutter-dart-code-review", "frontend-design-direction",
    "fsharp-testing", "generating-python-installer",
    "golang-patterns", "golang-testing", "hexagonal-architecture",
    "hookify-rules", "i18n-sync", "inherit-legacy-style", "intent-driven-development",
    "investor-materials", "investor-outreach", "iterative-retrieval",
    "java-coding-standards", "jpa-patterns", "kotlin-coroutines-flows",
    "kotlin-exposed-patterns", "kotlin-ktor-patterns", "kotlin-patterns",
    "kotlin-testing", "laravel-patterns", "laravel-plugin-discovery",
    "laravel-tdd", "laravel-verification", "living-docs-governance",
    "loop-design-check", "market-research", "mcp-dependency-review",
    "mcp-server-patterns", "mybatis-patterns", "mysql-patterns",
    "nestjs-patterns", "nuxt4-patterns", "opensource-pipeline",
    "perl-patterns", "perl-testing", "plankton-code-quality", "prisma-patterns",
    "product-lens", "quarkus-patterns", "quarkus-tdd", "quarkus-verification",
    "rails-patterns", "redis-patterns", "repo-scan", "rules-distill",
    "rust-patterns", "rust-testing", "santa-method", "security-scan",
    "skill-scout", "skill-stocktake", "springboot-patterns", "springboot-tdd",
    "springboot-verification", "story-lifecycle", "tinystruct-patterns",
    "ui-to-vue", "unified-memory", "vue-patterns", "windows-desktop-e2e",
]

KEPT_SKILLS = [
    "ai-feature-spec", "api-design", "api-integration", "app-scaffold",
    "backend-patterns", "browser-qa", "ck", "click-path-audit",
    "context-budget", "contract-first", "council", "delivery-gate",
    "deploy-fast", "design-system", "design-taste-frontend",
    "devpost-autofiller", "documentation-lookup", "e2e-testing",
    "error-handling", "fastapi-patterns", "feature-expansion",
    "frontend-a11y", "frontend-patterns", "frontend-slides", "gan-style-harness",
    "git-workflow",
    "grill-me", "growth-log", "hackathon-pitch", "hackathon-scope",
    "integration", "less-flat-ui", "make-interfaces-feel-better",
    "mobile-ship", "motion-advanced", "motion-foundations", "motion-patterns",
    "motionsites-web-builder",
    "nextjs-turbopack", "orch-add-feature", "orch-build-mvp",
    "orch-change-feature", "orch-fix-defect", "orch-pipeline",
    "orch-refine-code", "orchestrate", "pitch-deck-video", "polish-pass",
    "postgres-patterns", "production-audit", "python-patterns",
    "python-testing", "react-native-patterns", "react-patterns",
    "react-performance", "react-testing", "readme-writer", "security-review",
    "strategic-compact", "systematic-debugging", "tdd-workflow",
    "track-picker", "typescript-patterns", "ui-ux-pro-max",
    "verification-before-completion", "verification-loop", "vite-patterns",
]

REMOVED_AGENTS = [
    "ecc-bengali-reviewer", "ecc-csharp-reviewer", "ecc-django-build-resolver",
    "ecc-django-reviewer", "ecc-flutter-reviewer", "ecc-fsharp-reviewer",
    "ecc-kotlin-build-resolver", "ecc-kotlin-reviewer",
    "ecc-opensource-forker", "ecc-opensource-packager",
    "ecc-opensource-sanitizer", "ecc-rust-build-resolver",
    "ecc-rust-reviewer", "ecc-vue-reviewer",
    "ecc-conversation-analyzer", "ecc-cpp-build-resolver", "ecc-cpp-reviewer",
    "ecc-dart-build-resolver", "ecc-go-build-resolver", "ecc-go-reviewer",
    "ecc-java-build-resolver", "ecc-java-reviewer", "ecc-marketing-agent",
    "ecc-php-reviewer", "ecc-ruby-reviewer", "ecc-swift-build-resolver",
    "ecc-swift-reviewer",
]

KEPT_AGENTS = [
    "deep-reasoner", "ecc-a11y-architect", "ecc-agent-evaluator",
    "ecc-architect", "ecc-build-error-resolver", "ecc-chief-of-staff",
    "ecc-code-architect", "ecc-code-explorer", "ecc-code-reviewer",
    "ecc-code-simplifier", "ecc-comment-analyzer", "ecc-commit-reviewer",
    "ecc-database-reviewer", "ecc-doc-updater",
    "ecc-docs-lookup", "ecc-e2e-runner", "ecc-fastapi-reviewer",
    "ecc-gan-evaluator", "ecc-gan-generator", "ecc-gan-planner",
    "ecc-harmonyos-app-resolver",
    "ecc-healthcare-reviewer", "ecc-homelab-architect",
    "ecc-loop-operator",
    "ecc-mle-reviewer", "ecc-network-architect",
    "ecc-network-config-reviewer", "ecc-network-troubleshooter",
    "ecc-performance-optimizer", "ecc-pr-test-analyzer",
    "ecc-python-reviewer", "ecc-pytorch-build-resolver",
    "ecc-rag-pipeline-reviewer", "ecc-react-build-resolver",
    "ecc-react-reviewer", "ecc-refactor-cleaner",
    "ecc-security-reviewer", "ecc-seo-specialist", "ecc-silent-failure-hunter",
    "ecc-spec-miner",
    "ecc-tdd-guide", "ecc-type-design-analyzer", "ecc-typescript-reviewer",
    "fast-worker", "scout",
]

DROPPED_COMMANDS = [
    "flutter-build", "flutter-review", "flutter-test",
    "hookify-configure", "hookify-help", "hookify-list", "hookify",
    "kotlin-build", "kotlin-review", "kotlin-test",
    "marketing-campaign",
    "rust-build", "rust-review", "rust-test",
    "security-scan", "vue-review",
    "cpp-build", "cpp-review", "cpp-test",
    "go-build", "go-review", "go-test", "gradle-build",
    "evolve", "instinct-export", "instinct-import", "instinct-status",
    "learn-eval", "project-init", "projects", "promote", "prune",
]

KEPT_COMMANDS = [
    "aside", "astra-review", "auto-update", "build-fix", "checkpoint",
    "code-review", "demo",
    "ecc-guide", "epic-claim", "epic-decompose", "epic-publish",
    "epic-review", "epic-sync", "epic-unblock", "epic-validate",
    "fastapi-review", "feature-dev", "gan-build", "gan-design",
    "harness-audit", "issue-review", "learn", "loop-start",
    "model-route", "orch-add-feature", "orch-build-mvp", "orch-change-feature",
    "orch-fix-defect", "orch-refine-code", "orchestrate", "plan", "plan-prd",
    "pm2", "pr", "prp-commit",
    "prp-implement", "prp-plan", "prp-pr", "prp-prd",
    "python-review", "quality-gate", "react-build", "react-review",
    "react-test", "refactor-clean", "resume-session", "review-pr",
    "save-session", "sessions", "setup-pm", "skill-create", "skill-health",
    "test-coverage", "update-codemaps", "update-docs",
]

F27_TOKENS = [
    "DESIGNPKG-AUTO_F27", "CEILING_F27", "DELRISK_F27", "CHECKSRC_F27",
    "AUDITGUIDE_F27", "NOCOAUTHOR_F27", "THEME-START_F27", "ALWAYSLEAD_F27",
    "IMPL46_F27", "GRILLHDR_F27", "CAPTURE1_F27", "TESTNOTBQA_F27",
    "DEFER3_F27", "W2_F27", "W3_F27", "W4_F27", "TESTPASS_F27", "REROUTE_F27",
    "MOTIONSITES_F27", "PALETTE-FIRST_F27",
]

assert len(CUT_SKILLS) == 100 and len(KEPT_SKILLS) == 67
assert len(REMOVED_AGENTS) == 27 and len(KEPT_AGENTS) == 45
assert len(DROPPED_COMMANDS) == 32 and len(KEPT_COMMANDS) == 55
assert len(F27_TOKENS) == 20
assert not (set(CUT_SKILLS) & set(KEPT_SKILLS))
assert "growth-log" in KEPT_SKILLS

checks = []


def check(name, ok):
    checks.append((name, ok))
    print(("PASS " if ok else "FAIL ") + name)


def read(rel):
    return open(os.path.join(BASE, rel), encoding="utf-8").read()


def dir_names(d):
    return sorted(os.listdir(os.path.join(BASE, d)))


def count_in_tree(token, dirs=("skills", "agents", "commands", "rules",
                               "hooks", "manifests", "scripts")):
    n = 0
    for d in dirs:
        base = os.path.join(BASE, d)
        if not os.path.isdir(base):
            continue
        for root, _dirs, files in os.walk(base):
            _dirs[:] = [x for x in _dirs if x != "node_modules"]
            for fn in files:
                try:
                    t = open(os.path.join(root, fn),
                             encoding="utf-8", errors="strict").read()
                except (UnicodeDecodeError, ValueError, OSError):
                    continue
                n += t.count(token)
    return n


# 1. Counts + exact dir sets.
_skills = dir_names("skills")
_agents = sorted(f[:-3] for f in dir_names("agents") if f.endswith(".md"))
_commands = sorted(f[:-3] for f in dir_names("commands") if f.endswith(".md"))
_rules = dir_names("rules")
check("counts 67 skills / 45 agents / 123 rules / 55 commands",
      (len(_skills), len(_agents), len(_rules), len(_commands))
      == (67, 45, 123, 55))
if (len(_skills), len(_agents), len(_rules), len(_commands)) != (67, 45, 123, 55):
    print(f"   actual: {len(_skills)} skills, {len(_agents)} agents, "
          f"{len(_rules)} rules, {len(_commands)} commands")
check("skills dir set is exactly the 67 KEPT skills",
      _skills == sorted(KEPT_SKILLS))
if _skills != sorted(KEPT_SKILLS):
    print(f"   extra={sorted(set(_skills) - set(KEPT_SKILLS))} "
          f"missing={sorted(set(KEPT_SKILLS) - set(_skills))}")
check("agents dir set is exactly the 45 KEPT agents",
      _agents == sorted(KEPT_AGENTS))
if _agents != sorted(KEPT_AGENTS):
    print(f"   extra={sorted(set(_agents) - set(KEPT_AGENTS))} "
          f"missing={sorted(set(KEPT_AGENTS) - set(_agents))}")
check("commands dir set is exactly the 55 KEPT commands",
      _commands == sorted(KEPT_COMMANDS))
if _commands != sorted(KEPT_COMMANDS):
    print(f"   extra={sorted(set(_commands) - set(KEPT_COMMANDS))} "
          f"missing={sorted(set(KEPT_COMMANDS) - set(_commands))}")

# 2. CUT skills absent (dir set check above already implies this; assert
# explicitly per skill so a failure names the skill).
_cut_present = [s for s in CUT_SKILLS if os.path.exists(os.path.join(BASE, "skills", s))]
if _cut_present:
    print(f"   CUT skills still present: {_cut_present}")
check("all 100 CUT skill dirs are ABSENT", not _cut_present)
check("growth-log is KEPT (not in the CUT list, dir present)",
      os.path.isdir(os.path.join(BASE, "skills", "growth-log")))

# 3. Removed agents absent.
_removed_present = [a for a in REMOVED_AGENTS
                    if os.path.exists(os.path.join(BASE, "agents", a + ".md"))]
if _removed_present:
    print(f"   removed agents still present: {_removed_present}")
check("all 27 removed agents are ABSENT", not _removed_present)

# 4. Dropped commands absent.
_dropped_present = [c for c in DROPPED_COMMANDS
                    if os.path.exists(os.path.join(BASE, "commands", c + ".md"))]
if _dropped_present:
    print(f"   dropped commands still present: {_dropped_present}")
check("all 32 dropped commands are ABSENT", not _dropped_present)

# 5. Trigger table.
_triggers = json.load(open(os.path.join(
    BASE, "manifests/context-packs/skill-triggers@1.json"), encoding="utf-8"))
_trig_keys = list(_triggers["triggers"].keys())
_cut_keys = [k for k in _trig_keys if k.split(":", 1)[1] in CUT_SKILLS]
if _cut_keys:
    print(f"   trigger keys still pointing at CUT skills: {_cut_keys}")
check("trigger file parses as JSON and contains zero entries pointing at CUT skills",
      not _cut_keys)
check("trigger keys: 64 -> 49 after the prune",
      len(_trig_keys) == 49)
if len(_trig_keys) != 49:
    print(f"   actual trigger keys: {len(_trig_keys)}")
check("trigger coverage: skills 67, withTriggers 49",
      _triggers["coverage"]["skills"] == 67
      and _triggers["coverage"]["withTriggers"] == 49)

# 6. README counts + no stale counts.
_readme = read("README.md")
check("README count line shows 67 skills, 45 agents, 123 rules, 55 commands",
      "67 skills, 45 agents, 123 rules, and 55 commands in total "
      "(42 agents as-shipped + 3 staged orchestrate agents;" in _readme)
check("README comparison lines show the new counts (67 / 45 / 55)",
      "67 skills widen the routing surface" in _readme
      and "56 MB and 67 skills against a minimal set" in _readme
      and "structured process — 67 skills, 45 agents, 55 commands," in _readme)
check("README stock-ECC line untouched (144 skills, 69 agents is stock, not ours)",
      "144 skills, 69 agents, 121 rules, 94 commands" in _readme)
_stale = {}
for _tok in ("166 skills", "72 agents", "87 commands",
             "66 skills", "60 commands"):
    _n = count_in_tree(_tok, dirs=("skills", "agents", "commands", "rules",
                                   "hooks", "manifests", "scripts"))
    _n += _readme.count(_tok)
    _stale[_tok] = _n
if any(_stale.values()):
    print(f"   stale counts remaining: {_stale}")
check("zero '166 skills' / '72 agents' / '87 commands' / '66 skills' / '60 commands' remain in the built tree",
      not any(_stale.values()))

# 7. _F27 anchor tokens.
_missing_tokens = [t for t in F27_TOKENS
                   if count_in_tree(t) + _readme.count(t) == 0]
if _missing_tokens:
    print(f"   missing _F27 tokens: {_missing_tokens} "
          "(staged-worker tokens fail here until that worker lands)")
check("all 20 _F27 anchor tokens exist in the built tree",
      not _missing_tokens)
for _tok in ("CHECKSRC_F27", "AUDITGUIDE_F27"):
    check(f"fix27-written token {_tok} is in skills/hackathon-pitch/SKILL.md",
          _tok in read("skills/hackathon-pitch/SKILL.md"))
check("fix27-written token NOCOAUTHOR_F27 is in rules/common-git-workflow.mdc",
      "NOCOAUTHOR_F27" in read("rules/common-git-workflow.mdc"))
check("fix27-written token CAPTURE1_F27 is in skills/browser-qa/SKILL.md",
      "CAPTURE1_F27" in read("skills/browser-qa/SKILL.md"))
check("fix27-written token TESTNOTBQA_F27 is in skills/verification-before-completion/SKILL.md",
      "TESTNOTBQA_F27" in read("skills/verification-before-completion/SKILL.md"))
check("fix27-written token DEFER3_F27 is in rules/hackathon-mode.mdc",
      "DEFER3_F27" in read("rules/hackathon-mode.mdc"))
check("fix27-written token REROUTE_F27 is in skills/feature-expansion/SKILL.md",
      "REROUTE_F27" in read("skills/feature-expansion/SKILL.md"))
check("fix27-written token TESTPASS_F27 is in skills/orchestrate/SKILL.md",
      "TESTPASS_F27" in read("skills/orchestrate/SKILL.md"))
check("fix27-written token MOTIONSITES_F27 is in skills/motionsites-web-builder/SKILL.md",
      "MOTIONSITES_F27" in read("skills/motionsites-web-builder/SKILL.md"))
check("palette-first token PALETTE-FIRST_F27 is in skills/design-taste-frontend/SKILL.md",
      "PALETTE-FIRST_F27" in read("skills/design-taste-frontend/SKILL.md"))
check("palette-first token PALETTE-FIRST_F27 is in skills/orchestrate/SKILL.md",
      "PALETTE-FIRST_F27" in read("skills/orchestrate/SKILL.md"))
check("palette-first token PALETTE-FIRST_F27 is in rules/hackathon-mode.mdc",
      "PALETTE-FIRST_F27" in read("rules/hackathon-mode.mdc"))
check("usage-cut tokens W2/W3/W4_F27 are in skills/orchestrate/SKILL.md",
      all(t in read("skills/orchestrate/SKILL.md")
          for t in ("W2_F27", "W3_F27", "W4_F27")))

# 8. Banned terms: 0 in the built tree (case-insensitive, excl. node_modules),
# except the vendored motionsites-web-builder fetch URLs and license title.
# The SKILL.md fetch URLs carry the upstream repo name "claude-skill"
# (rewording them breaks the fetch) and are allowed by content, not line
# number — the M-new-5 insert shifted the media line 36 -> 38 and broke a
# line-number allow, so the URLs match on their (un-rewordable) address.
# The LICENSE line is the upstream license title (the MIT notice ships
# verbatim), allowed by file + line 1. A functional address and a license
# document, not Claude-product branding. ("Cursor / Claude Code" in
# builders.md was reworded to "Cursor" in the staged source instead.)
banned = ["claude", "codex", "anthropic", "opus", "sonnet", "haiku", "composer-2.5"]
CHECK8_ALLOW_URL = "raw.githubusercontent.com/Motionsites-AI/claude-skill"
CHECK8_ALLOW_LINES = {("skills/motionsites-web-builder/LICENSE", 1)}
_hits = subprocess.run(
    ["grep", "-rinE", "|".join(banned), "skills", "agents", "commands", "rules",
     "hooks", "README.md", "--exclude-dir=node_modules"],
    cwd=BASE, capture_output=True, text=True).stdout.strip().splitlines()
_unallowed = []
for _h in [h for h in _hits if h]:
    _parts = _h.split(":", 2)
    if len(_parts) >= 2 and CHECK8_ALLOW_URL in _h:
        continue
    if len(_parts) >= 2 and (_parts[0], int(_parts[1])) in CHECK8_ALLOW_LINES:
        continue
    _unallowed.append(_h)
if _unallowed:
    print(f"   banned-term hits: {_unallowed!r}")
check("banned terms 0 in built tree except the motionsites fetch URLs + license title (skills/agents/commands/rules/hooks/README)",
      not _unallowed)

# 9. Grok pins only.
_bare_grok = subprocess.run(
    ["grep", "-rn", "grok-4.6-high-fast", "skills", "agents", "commands",
     "rules", "hooks", "README.md", "--exclude-dir=node_modules"],
    cwd=BASE, capture_output=True, text=True).stdout
_bare_grok = "\n".join(
    ln for ln in _bare_grok.splitlines() if "cursor-grok-4.6-high-fast" not in ln)
if _bare_grok.strip():
    print(f"   bare grok-4.6-high-fast lines: {_bare_grok[:500]!r}")
check("bare grok-4.6-high-fast count is 0 in the built tree",
      _bare_grok.strip() == "")
_g47 = subprocess.run(
    ["grep", "-ro", "grok-4.7-high", ".", "--exclude-dir=node_modules"],
    cwd=BASE, capture_output=True, text=True).stdout.strip()
_c46 = subprocess.run(
    ["grep", "-ro", "cursor-grok-4.6-high-fast", ".", "--exclude-dir=node_modules"],
    cwd=BASE, capture_output=True, text=True).stdout.strip()
check("Grok pins present: grok-4.7-high and cursor-grok-4.6-high-fast occur",
      len(_g47.splitlines()) > 0 and len(_c46.splitlines()) > 0)
if _g47 and _c46:
    print(f"   grok-4.7-high x{len(_g47.splitlines())}, "
          f"cursor-grok-4.6-high-fast x{len(_c46.splitlines())}")

# 10. fix27.py patch anchors still present exactly once.
_dg = read("skills/delivery-gate/SKILL.md")
check("delivery-gate :97 reword present x1, old agent-self-evaluation pointer gone",
      _dg.count("pair with a manual review of the recorded entries") == 1
      and "For content quality verification, pair with `agent-self-evaluation`" not in _dg)
_bqa = read("skills/browser-qa/SKILL.md")
check("browser-qa single-capture rule present x1 (CAPTURE1_F27)",
      _bqa.count("Single capture run (CAPTURE1_F27)") == 1
      and _bqa.count("never re-shoot a state/width the polish-pass captures already cover") == 1)
_vbc = read("skills/verification-before-completion/SKILL.md")
check("verification-before-completion UI-verified row present x1 (TESTNOTBQA_F27)",
      _vbc.count("| UI verified | browser-qa verdict on the rendered screen (TESTNOTBQA_F27) | test suite passing, screenshots described but not inspected, agent report |") == 1)
_pitch = read("skills/hackathon-pitch/SKILL.md")
check("hackathon-pitch CHECK-THE-SOURCE + AUDIT-AS-GUIDE present x1 each",
      _pitch.count("**CHECK-THE-SOURCE (CHECKSRC_F27).**") == 1
      and _pitch.count("**AUDIT-AS-GUIDE (AUDITGUIDE_F27).**") == 1
      and _pitch.count("uses only exact verified numbers") == 1)
_git = read("rules/common-git-workflow.mdc")
check("common-git-workflow no-Co-authored-by rule present x1 (NOCOAUTHOR_F27)",
      _git.count("Commit messages carry no `Co-authored-by:` trailer for any AI tool") == 1
      and _git.count("NOCOAUTHOR_F27") == 1)
_orch = read("skills/orchestrate/SKILL.md")
check("orchestrate commit-draft re-route to git-workflow present x1, old skill gone",
      _orch.count("draft each commit message with the `git-workflow` skill (`skills/git-workflow/SKILL.md`)") == 1
      and "conventional-commit-review" not in _orch)
_sec = read("skills/security-review/SKILL.md")
check("security-review end-of-project security-scan dispatch removed",
      "use security-scan" not in _sec)
_obm = read("skills/orch-build-mvp/SKILL.md")
check("deferred lists shrunk to the three kept checks (DEFER3_F27)",
      _orch.count("(`production-audit`, `delivery-gate`, and `verification-loop`) (DEFER3_F27)") == 1
      and _orch.count("run the three deferred checks by name — `verification-loop`, `production-audit`, `delivery-gate`") == 1
      and _orch.count("one line per deferred check (`verification-loop`, `production-audit`, `delivery-gate`)") == 1
      and _obm.count("run the three deferred end-of-project checks by name (`verification-loop`, `production-audit`, `delivery-gate`)") == 1
      and "codehealth-mcp" not in _orch and "santa-method" not in _orch
      and "security-scan" not in _orch and "codehealth-mcp" not in _obm)

# 10b. Round-2 patch anchors (audit #74 B1/B2/B5-B13/B15, M3-M6).
# B1: legacy drift re-routed in the 5 orch-* rules + ui-ux-pro-max.
for _orch in ("orch-add-feature", "orch-build-mvp", "orch-change-feature",
              "orch-fix-defect", "orch-refine-code"):
    _t = read(f"skills/{_orch}/SKILL.md")
    check(f"B1 {_orch}: legacy drift handled inside the design package (REROUTE_F27)",
          _t.count("handled inside the design package — no separate skill (fix #27, REROUTE_F27)") == 1
          and "inherit-legacy-style" not in _t)
_uux = read("skills/ui-ux-pro-max/SKILL.md")
check("B1 ui-ux-pro-max: legacy drift handled inside the design package (REROUTE_F27)",
      _uux.count("legacy style drift is handled inside the design package — no separate skill (fix #27, REROUTE_F27)") == 1
      and "inherit-legacy-style" not in _uux)
# B2: theme cage lifted in both ECC-origin E1 copies.
for _e1 in ("orch-build-mvp", "ui-ux-pro-max"):
    _t = read(f"skills/{_e1}/SKILL.md")
    check(f"B2 {_e1}: bound (2) relaxed + new-theme clause deleted + inversion sentence (THEME-START_F27)",
          _t.count("(2) fit the theme's material world — material, tokens, palette balance, do-nots — **or a recorded departure from it** (D19 reason required) (fix #27, THEME-START_F27);") == 1
          and "a new theme (re-deal instead" not in _t
          and _t.count("Inventing a theme direction is a recorded D19 decision, not a forbidden move (fix #27, THEME-START_F27)") == 1)
# B5: prp-commit re-routed to git-workflow.
_prp = read("commands/prp-commit.md")
check("B5 prp-commit: commit draft re-routed to git-workflow",
      _prp.count("Draft the message with the `git-workflow` skill (`skills/git-workflow/SKILL.md`)") == 1
      and "conventional-commit-review" not in _prp)
# B6: CLv2 remnants gone from skill-create; /project-init + /projects pointers gone.
_sc = read("commands/skill-create.md")
check("B6 skill-create: --instincts flag, Instincts step, Step 4, Related Commands gone; description re-routed (B15)",
      "--instincts" not in _sc and "instinct" not in _sc
      and "continuous-learning-v2" not in _sc and "skill-scout" not in _sc
      and _sc.count("check the plugin's own skill list (grep-and-read) first") == 1)
_sh = read("commands/skill-health.md")
check("B6/B15 skill-health: /evolve re-routed to /learn; description re-routed",
      "/evolve" not in _sh and "skill-stocktake" not in _sh
      and _sh.count("suggest running /learn") == 1
      and _sh.count("for a qualitative compliance or quality audit use the plugin's own skill list and verify scripts.") == 1)
check("B6 ecc-guide: /project-init pointer removed",
      "/project-init" not in read("commands/ecc-guide.md"))
check("B6 epic-sync: /projects compatibility alias removed",
      "/projects" not in read("commands/epic-sync.md"))
# B7: /security-scan pointers re-pointed to security-review.
for _sf in ("commands/ecc-guide.md", "commands/fastapi-review.md",
            "commands/harness-audit.md", "rules/react-native-security.mdc"):
    check(f"B7 {_sf}: no /security-scan pointer remains",
          "security-scan" not in read(_sf))
_hjs = read("scripts/harness-audit.js")
check("B7 harness-audit.js: security-scan-command check re-pointed at security-review (id kept)",
      _hjs.count("fix: 'Add skills/security-review with the security review workflow.'") == 1
      and "commands/security-scan.md" not in _hjs
      and _hjs.count("id: 'security-scan-command'") == 1
      and "Add skills/security-review with the security review workflow." in _hjs)
# M-new-6 (audit #75): the coordinator-added memory-learning-skill
# re-point (continuous-learning-v2 -> growth-log) had no assertion; a
# later rebuild reverting it would have passed silently.
check("B7 harness-audit.js: memory-learning-skill check re-pointed at growth-log (id kept)",
      _hjs.count("id: 'memory-learning-skill'") == 1
      and _hjs.count("path: 'skills/growth-log/SKILL.md',") == 1
      and _hjs.count("description: 'Growth log skill exists',") == 1
      and _hjs.count("pass: fileExists(rootDir, 'skills/growth-log/SKILL.md'),") == 1
      and _hjs.count("fix: 'Add skills/growth-log/SKILL.md for memory evolution flow.',") == 1
      and "skills/continuous-learning-v2/SKILL.md" not in _hjs)
# M-new-4 (audit #75, coordinator follow-up): the pi-core.json prune had no
# assertion; a later rebuild reverting it would have passed silently.
_picore = json.load(open(os.path.join(BASE, "manifests/pi-core.json"), encoding="utf-8"))
_picore_skills = set(_picore.get("skills", {}).get("include", []))
_picore_cmds = {_c[:-3] if _c.endswith(".md") else _c
                for _c in _picore.get("commands", {}).get("include", [])}
check("M-new-4 pi-core.json: skills.include has no CUT skills, commands.include has no dropped commands",
      not (_picore_skills & set(CUT_SKILLS))
      and not (_picore_cmds & set(DROPPED_COMMANDS)))
# B8: council santa-method re-routed to the kept end gates.
_council = read("skills/council/SKILL.md")
check("B8 council: end-of-project verification re-routed to verification-loop / production-audit",
      _council.count("at the end of the project: `verification-loop` / `production-audit`") == 1
      and _council.count("`code-reviewer` or, at the end of the project, `verification-loop` / `production-audit`") == 1
      and "santa-method" not in _council
      and "architecture-decision-records" not in _council)
# B9: integration re-routes (names survive only in "was cut" notes).
_integ = read("skills/integration/SKILL.md")
check("B9 integration: skill-scout / mcp-server-patterns dispatches re-routed (REROUTE_F27)",
      "that is `mcp-server-patterns`" not in _integ
      and "Use `skill-scout` to search" not in _integ
      and "Use `mcp-server-patterns` for the server setup" not in _integ
      and _integ.count("REROUTE_F27 — `skill-scout` was cut") == 1
      and _integ.count("REROUTE_F27 — `mcp-server-patterns` was cut") == 2)
# B10: ai-feature-spec re-routed to hackathon-scope.
_afs = read("skills/ai-feature-spec/SKILL.md")
check("B10 ai-feature-spec: non-AI features re-routed to hackathon-scope",
      _afs.count("For non-AI features use hackathon-scope; for API contracts use contract-first.") == 1
      and "intent-driven-development" not in _afs)
# B11: ecc-agent-evaluator self-contained (rubric source is this file).
_eae = read("agents/ecc-agent-evaluator.md")
check("B11 ecc-agent-evaluator: self-contained, no agent-self-evaluation references",
      "agent-self-evaluation" not in _eae
      and _eae.count("Work through the 5 axes defined below:") == 1
      and _eae.count("Use this exact format (defined in this file):") == 1
      and _eae.count("matching the output format defined in this file exactly.") == 1)
# B12 (build-time half): mobile-ship.
_ms = read("skills/mobile-ship/SKILL.md")
check("B12 mobile-ship: screens/features belong to react-native-patterns alone",
      _ms.count("belongs to react-native-patterns.") == 1
      and "dart-flutter-patterns" not in _ms)
# B13: systematic-debugging.
check("B13 systematic-debugging: agent-introspection-debugging reference removed",
      "(agent-introspection-debugging)" not in read("skills/systematic-debugging/SKILL.md"))
# M3: trigger notes list only the three kept deferred checks.
_notes = _triggers.get("notes", "")
check("M3 trigger notes: deferred list is the three kept checks (DEFER3_F27)",
      _notes.count("Deferred: verification-loop, production-audit, delivery-gate. (DEFER3_F27)") == 1
      and "codehealth-mcp" not in _notes and "santa-method" not in _notes
      and "security-scan" not in _notes)
# M4: delivery-gate "shipped" claims gone, ecc-agent-evaluator pointed at.
_dg = read("skills/delivery-gate/SKILL.md")
check("M4 delivery-gate: agent-self-evaluation 'shipped' claims removed, evaluator pointed at",
      _dg.count("Complements the `ecc-agent-evaluator` agent (whose 5-axis rubric is defined in the agent file itself)") == 1
      and _dg.count("the former `agent-self-evaluation` skill — cut in fix #27") == 1
      and _dg.count("- **`ecc-agent-evaluator`** (reasoning-quality gate;") == 1
      and _dg.count("- `ecc-agent-evaluator` — Reasoning quality gate (accuracy/completeness/clarity/actionability/conciseness;") == 1
      and "the shipped equivalent of upstream self-audit" not in _dg
      and "shipped equivalent of upstream `self-audit`" not in _dg
      and "like the shipped `agent-self-evaluation` skill" not in _dg)
# M5: README stale CUT references gone.
check("M5 README: marketplace list, codebase-memory line, deferred set updated",
      _readme.count("plus the marketplace skills (systematic-debugging,\n  verification-before-completion)") == 1
      and "dispatching-parallel-agents" not in _readme
      and "codebase-memory` queries a local knowledge graph" not in _readme
      and "security-scan" not in _readme
      and _readme.count("Security tests and audits (`verification-loop`, `production-audit`, and `delivery-gate`) run ONLY at the") == 1
      and _readme.count("Playwright MCP and the audit deferral") == 1
      and _readme.count("## Commands (highlights — 3 of 55)") == 1)
# M6: dangling "see skill" pointers gone.
check("M6 contract-first: ai-regression-testing pointers removed",
      "ai-regression-testing" not in read("skills/contract-first/SKILL.md"))
check("M6 ecc-database-reviewer: database-migrations pointer removed",
      "database-migrations" not in read("agents/ecc-database-reviewer.md")
      and read("agents/ecc-database-reviewer.md").count("see skill: `postgres-patterns`.") == 1)
check("M6 tdd-workflow / postgres-patterns / react-native-patterns pointers removed",
      "bun-runtime" not in read("skills/tdd-workflow/SKILL.md")
      and "clickhouse-io" not in read("skills/postgres-patterns/SKILL.md")
      and "coding-standards" not in read("skills/react-native-patterns/SKILL.md"))
check("M6 react-patterns: accessibility / angular-developer links removed",
      ", [accessibility](../accessibility/SKILL.md), [angular-developer](../angular-developer/SKILL.md) for framework comparison" not in read("skills/react-patterns/SKILL.md")
      and "../angular-developer/SKILL.md" not in read("skills/react-patterns/SKILL.md"))
check("M6 typescript-patterns: nestjs / prisma pointers removed",
      "nestjs-patterns" not in read("skills/typescript-patterns/SKILL.md")
      and "prisma-patterns" not in read("skills/typescript-patterns/SKILL.md"))
check("M6 strategic-compact: continuous-learning re-pointed at /learn",
      "continuous-learning" not in read("skills/strategic-compact/SKILL.md")
      and read("skills/strategic-compact/SKILL.md").count("- `/learn` command — Extracts patterns before session ends") == 1)
_rer = read("scripts/lib/resolve-ecc-root.js")
check("M6 resolve-ecc-root.js: sentinel moved to orchestrate",
      "path.join('skills', 'continuous-learning-v2')" not in _rer
      and _rer.count("path.join('skills', 'orchestrate')") == 1
      and "sentinel moved from continuous-learning-v2" in _rer)

# 11. fix27 patch log (written next to the tree under test: the real
# fix27/ dir for the default tree, the scratch fix27/ dir for a scratch
# tree — fix27.py derives the same path from BASE).
_log_dir = os.path.join(os.path.dirname(BASE.rstrip("/")), "fix27")
_log_path = os.path.join(_log_dir, "fix27-patch-log.md")
_log_ok = False
if os.path.exists(_log_path):
    _log = open(_log_path, encoding="utf-8").read()
    _log_ok = ("## Errors (0)" in _log
               and ("skills removed: 100 dirs" in _log
                    or "100 already absent" in _log)
               and ("commands dropped: 32 files" in _log
                    or "27 already absent" in _log
                    or "32 already absent" in _log))
check("fix27/fix27-patch-log.md exists with 0 errors, 100 skills and 32 commands accounted for",
      _log_ok)

# 12. CUT-name sweep (audit #74 M10): every CUT skill name, removed
# agent name and dropped command name must occur zero times as a live
# dispatch in skills/, agents/, commands/, rules/ (excluding the
# regenerated call map), except for the explicit ALLOW_LIST below.
# Two tiers, mirroring fix27/scratch/f27r2-census.py:
#   STRONG - backticked `name`, skills/<name> or agents/<name> or
#     commands/<name> path, <name>/SKILL.md, skill:<name>, "/<name>"
#     slash form, "<name>" double-quoted, "<name> skill|agent" /
#     "skill|agent <name>" adjacency. Flagged for every name.
#   BARE - bare word-boundary match. Flagged only for non-generic names;
#     generic English words (accessibility, brainstorming, evolve,
#     projects, promote, prune) match ordinary prose constantly, so bare
#     uses of those are noise (counted, never failing); their STRONG
#     forms are still swept.
# ALLOW_LIST maps file -> {line: justification}; every entry is a
# prose-history ("was cut" / "NOT invoked"), negative ("does not
# require", "is not used", "NOT wired"), pointer-style ("See skill",
# cross-link, "Covered in part by") or data (icon id, search keyword,
# test fixture) mention read in context on the post-fix census
# (fix27/scratch/f27r2-census.txt). A live dispatch must NEVER be
# allow-listed: if the sweep finds one, fix the dispatch, do not extend
# the list. NOTE: the two hackathon-mode.mdc entries (37, 38) sit in a
# staged-owned file; if the staged worker's edits shift lines above
# them, re-run the census and update the line numbers.
import re as _re
_CUT_NAMES = CUT_SKILLS + REMOVED_AGENTS + DROPPED_COMMANDS
_NAME_SET = set(_CUT_NAMES)
_GENERIC_BARE = {"accessibility", "brainstorming",
                 "evolve", "projects", "promote", "prune"}
ALLOW_LIST = {
    "skills/delivery-gate/SKILL.md": {
        13: "prose-history: 'former skill — cut in fix #27' (M4 reword)",
        15: "prose-history: 'formerly in agent-self-evaluation' (M4 reword)",
        111: "prose-history: 'formerly in agent-self-evaluation' (M4 reword)",
    },
    "skills/feature-expansion/SKILL.md": {
        3: "generic verb 'brainstorm' in the description, not the skill",
        49: "prose-history: 'code-tour was cut' (REROUTE_F27)",
        100: "prose-history: 'product-lens was cut' (REROUTE_F27)",
        188: "prose-history: 'brainstorming skill is NOT invoked' (REROUTE_F27)",
        190: "prose-history: 'dispatching-parallel-agents was cut' (REROUTE_F27)",
        192: "prose-history: 'code-tour was cut' (REROUTE_F27)",
        193: "prose-history: 'intent-driven-development was cut' (REROUTE_F27)",
        204: "prose-history: 'agent-self-evaluation was cut' (REROUTE_F27)",
        211: "attribution to upstream brainstorming techniques source, not a dispatch",
    },
    "skills/orchestrate/SKILL.md": {
        136: "prose-history: 'ecc-recipes was cut' (REROUTE_F27)",
    },
    "skills/integration/SKILL.md": {
        21: "prose-history: 'mcp-server-patterns was cut' (REROUTE_F27)",
        46: "prose-history: 'skill-scout was cut' (REROUTE_F27)",
        60: "prose-history: 'mcp-server-patterns was cut' (REROUTE_F27)",
        122: "prose-history: 'skill-scout and mcp-server-patterns were cut' (REROUTE_F27)",
    },
    "skills/design-taste-frontend/assets/icons/demo.html": {
        74: "data: icon demo page glyph, not a skill reference",
    },
    "skills/design-taste-frontend/assets/icons/index.json": {
        5569: "data: icon id 'accessibility', not a skill reference",
    },
    "skills/ui-ux-pro-max/data/phosphor-icons-upstream.json": {
        8306: "data: icon name 'accessibility' in the upstream icon dataset",
        22481: "data: icon name 'accessibility' in the upstream icon dataset",
        22557: "data: icon name 'accessibility' in the upstream icon dataset",
        28089: "data: icon name 'accessibility' in the upstream icon dataset",
        28112: "data: icon name 'accessibility' in the upstream icon dataset",
        32160: "data: icon name 'accessibility' in the upstream icon dataset",
        32184: "data: icon name 'accessibility' in the upstream icon dataset",
    },
    "skills/ui-ux-pro-max/scripts/core.py": {
        232: "data: search keyword/category mapping, not a skill reference",
        233: "data: search keyword/category mapping, not a skill reference",
        240: "data: search keyword/category mapping, not a skill reference",
        264: "data: search keyword/category mapping, not a skill reference",
        594: "data: search keyword/category mapping, not a skill reference",
    },
    "skills/ui-ux-pro-max/scripts/design_system.py": {
        622: "data: style key 'accessibility', not a skill reference",
        805: "data: style key 'accessibility', not a skill reference",
    },
    "skills/ui-ux-pro-max/scripts/reasoning_contract.py": {
        41: "data: keyword tuple for UX focus, not a skill reference",
    },
    "skills/ui-ux-pro-max/scripts/tests/fixtures/relevance-cases.json": {
        27: "data: test fixture query/domain, not a skill reference",
        29: "data: test fixture query/domain, not a skill reference",
        36: "data: test fixture query/domain, not a skill reference",
        39: "data: test fixture query/domain, not a skill reference",
        105: "data: test fixture query/domain, not a skill reference",
    },
    "agents/ecc-spec-miner.md": {
        3: "negative: 'does not require codebase-onboarding' (description)",
        40: "negative: 'does not require codebase-onboarding'",
        201: "negative: 'does not require codebase-onboarding'",
    },
    "commands/learn.md": {
        2: "negative: description distinguishes /learn from the removed CLv2 system",
    },
    "rules/golang-coding-style.mdc": {
        31: "pointer: 'See skill: golang-patterns' (OWED-11 / M7)",
    },
    "rules/golang-patterns.mdc": {
        44: "pointer: 'See skill: golang-patterns' (OWED-11 / M7)",
    },
    "rules/golang-testing.mdc": {
        30: "pointer: 'See skill: golang-testing' (OWED-11 / M7)",
    },
    "rules/kotlin-coding-style.mdc": {
        39: "pointer: 'See skill: kotlin-patterns' (OWED-11 / M7)",
    },
    "rules/kotlin-patterns.mdc": {
        50: "pointer: 'See skill: kotlin-patterns' (OWED-11 / M7)",
    },
    "rules/kotlin-testing.mdc": {
        38: "pointer: 'See skill: kotlin-testing' (OWED-11 / M7)",
    },
    "rules/angular-patterns.mdc": {
        249: "pointer: 'See skill: angular-developer' (OWED-11 / M7)",
    },
    "rules/angular-testing.mdc": {
        164: "pointer: 'See skill: angular-developer' (OWED-11 / M7)",
    },
    "rules/cpp-coding-style.mdc": {
        44: "pointer: 'See skill: cpp-coding-standards' (OWED-11 / M7)",
    },
    "rules/cpp-patterns.mdc": {
        51: "pointer: 'See skill: cpp-coding-standards' (OWED-11 / M7)",
    },
    "rules/cpp-security.mdc": {
        51: "pointer: 'See skill: cpp-coding-standards' (OWED-11 / M7)",
    },
    "rules/cpp-testing.mdc": {
        44: "pointer: 'See skill: cpp-testing' (OWED-11 / M7)",
    },
    "rules/dart-patterns.mdc": {
        260: "pointer: 'See skill: flutter-dart-code-review' (OWED-11 / M7)",
        261: "pointer: 'See skill: compose-multiplatform-patterns' (OWED-11 / M7)",
    },
    "rules/java-coding-style.mdc": {
        113: "pointer: 'See skill: java-coding-standards' (OWED-11 / M7)",
        114: "pointer: 'See skill: jpa-patterns' (OWED-11 / M7)",
    },
    "rules/java-patterns.mdc": {
        145: "pointer: 'See skill: springboot-patterns' (OWED-11 / M7)",
        146: "pointer: 'See skill: quarkus-patterns' (OWED-11 / M7)",
        147: "pointer: 'See skill: jpa-patterns' (OWED-11 / M7)",
    },
    "rules/java-testing.mdc": {
        114: "pointer: 'See skill: springboot-tdd' (OWED-11 / M7)",
        115: "pointer: 'See skill: quarkus-tdd' (OWED-11 / M7)",
        131: "pointer: 'See skill: springboot-tdd' (OWED-11 / M7)",
        132: "pointer: 'See skill: quarkus-tdd' (OWED-11 / M7)",
        133: "pointer: 'See skill: java-coding-standards' (OWED-11 / M7)",
    },
    "rules/nuxt-coding-style.mdc": {
        45: "pointer: 'ECC skills: nuxt4-patterns' list entry (OWED-11 / M7)",
    },
    "rules/nuxt-hooks.mdc": {
        37: "pointer: 'ECC skills: nuxt4-patterns' list entry (OWED-11 / M7)",
    },
    "rules/nuxt-patterns.mdc": {
        51: "pointer: 'ECC skills: nuxt4-patterns' list entry (OWED-11 / M7)",
    },
    "rules/nuxt-security.mdc": {
        46: "pointer: 'ECC skills: nuxt4-patterns' list entry (OWED-11 / M7)",
    },
    "rules/nuxt-testing.mdc": {
        47: "pointer: 'ECC skills: nuxt4-patterns' list entry (OWED-11 / M7)",
    },
    "rules/perl-coding-style.mdc": {
        46: "pointer: 'See skill: perl-patterns' (OWED-11 / M7)",
    },
    "rules/perl-patterns.mdc": {
        76: "pointer: 'See skill: perl-patterns' (OWED-11 / M7)",
    },
    "rules/perl-testing.mdc": {
        54: "pointer: 'See skill: perl-testing' (OWED-11 / M7)",
    },
    "rules/react-patterns.mdc": {
        194: "pointer: 'For accessibility see skills/accessibility/SKILL.md' (OWED-11 / M7)",
    },
    "rules/rust-coding-style.mdc": {
        151: "pointer: 'See skill: rust-patterns' (OWED-11 / M7)",
    },
    "rules/rust-patterns.mdc": {
        168: "pointer: 'See skill: rust-patterns' (OWED-11 / M7)",
    },
    "rules/rust-security.mdc": {
        140: "pointer: 'See skill: rust-patterns' (OWED-11 / M7)",
    },
    "rules/rust-testing.mdc": {
        154: "pointer: 'See skill: rust-testing' (OWED-11 / M7)",
    },
    "rules/hackathon-mode.mdc": {
        37: "negative: 'frontend-design-direction is not used for hackathon UI work'",
        38: "negative: 'Design skills deliberately NOT wired into the UI design package'",
    },
}
# Name-scoped allows: file -> {line: {name: justification}}. For lines
# that mix a live dispatch with negative mentions, only the negative
# names are allowed — the dispatch name still fails the sweep until it
# is re-routed. (hackathon-mode:46: `brainstorming` is a live B12
# dispatch until the staged worker re-routes it to feature-expansion;
# `product-lens` / `intent-driven-development` on the same line are
# negative statements — 'do not scope hackathons' — and are allowed
# now, so the line passes the moment the staged fix lands.)
ALLOW_NAMES = {
    "rules/hackathon-mode.mdc": {
        46: {
            "intent-driven-development": "negative: 'do not scope hackathons'",
            "product-lens": "negative: 'do not scope hackathons'",
        },
    },
}


def _sweep_strong_names(line):
    found = set()
    for m in _re.finditer(r"`([^`\n]+)`", line):
        if m.group(1) in _NAME_SET:
            found.add(m.group(1))
    for m in _re.finditer(r"(?:skills|agents|commands)/([a-z0-9][a-z0-9-]*)", line):
        if m.group(1) in _NAME_SET:
            found.add(m.group(1))
    for m in _re.finditer(r"([a-z0-9][a-z0-9-]*)/SKILL\.md", line):
        if m.group(1) in _NAME_SET:
            found.add(m.group(1))
    for m in _re.finditer(r"skill:([a-z0-9][a-z0-9-]*)", line):
        if m.group(1) in _NAME_SET:
            found.add(m.group(1))
    for m in _re.finditer(r"(?<![A-Za-z0-9_/\-])/([a-z0-9][a-z0-9-]*)", line):
        if m.group(1) in _NAME_SET:
            found.add(m.group(1))
    for m in _re.finditer(r'"([A-Za-z0-9][A-Za-z0-9_-]{2,})"', line):
        if m.group(1) in _NAME_SET:
            found.add(m.group(1))
    for m in _re.finditer(r"([a-z0-9][a-z0-9-]*)\s+(?:skill|agent|command)s?\b", line, _re.I):
        if m.group(1) in _NAME_SET:
            found.add(m.group(1))
    for m in _re.finditer(r"\b(?:skill|agent|command)s?:?\s+([a-z0-9][a-z0-9-]*)", line, _re.I):
        if m.group(1) in _NAME_SET:
            found.add(m.group(1))
    return found


_sweep_pat = (r"(?<![A-Za-z0-9_-])(?:" + "|".join(_CUT_NAMES) + r")(?![A-Za-z0-9_-])")
_sweep = subprocess.run(
    ["grep", "-rnP", _sweep_pat, "skills", "agents", "commands", "rules",
     "--exclude=call-map.md", "--exclude-dir=node_modules"],
    cwd=BASE, capture_output=True, text=True)
_WORD_RE = _re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]*")
_unallowed, _allowed_n, _noise_n = [], 0, 0
for _ln in _sweep.stdout.splitlines():
    if not _ln:
        continue
    _path, _, _rest = _ln.partition(":")
    _lineno, _, _text = _rest.partition(":")
    _lineno = int(_lineno)
    _words = set(_WORD_RE.findall(_text))
    _bare = [n for n in _CUT_NAMES if n in _words]
    _strong = sorted(_sweep_strong_names(_text))
    _flagged = sorted({n for n in _bare if n not in _GENERIC_BARE} | set(_strong))
    if not _flagged:
        _noise_n += 1
        continue
    _whole = _lineno in ALLOW_LIST.get(_path, {})
    _named = ALLOW_NAMES.get(_path, {}).get(_lineno, {})
    _remaining = [n for n in _flagged if not _whole and n not in _named]
    if _remaining:
        _unallowed.append(f"{_path}:{_lineno}: {','.join(_remaining)} :: {_text.strip()[:160]}")
    else:
        _allowed_n += 1
if _unallowed:
    print(f"   un-allow-listed CUT-name hits ({len(_unallowed)}):")
    for _u in _unallowed:
        print(f"   ! {_u}")
print(f"   CUT-name sweep: {len(_unallowed)} un-allow-listed, "
      f"{_allowed_n} allow-listed, {_noise_n} generic bare-word noise lines")
check("CUT-name sweep: zero live dispatches to CUT skills/agents/commands (check-12 allow-list only)",
      not _unallowed)

# 12b. No imperative dispatch to a CUT skill/agent/command hides in an
# allow-listed line (audit #75 B-new-1: the whole-line allow-list hid a
# live "use the `coding-standards` skill" dispatch in
# agents/ecc-typescript-reviewer.md:119 while check 12 passed 76/76).
# Re-scan every whole-line allow-listed line: fail if the line contains
# an imperative verb (use/check/consult/run/invoke/call/load/read,
# word-boundary, case-insensitive) with a CUT name backticked or
# followed by skill/agent/command within 120 characters after the verb
# — except when the verb is negated (preceded within 15 characters by
# "not", "never", "n't", or "do not"). Three readings are pinned down
# here, because the literal rule as first written false-positived on
# two legitimate allow-listed lines (see the round-3 log):
#   (a) Negation is a SUBSTRING search in the 15 characters before the
#       verb (the task states word-boundary only for the verbs, not
#       for the negation) — so "cannot run" counts as negated, which
#       is what rules/hackathon-mode.mdc:38 needs ("live modes need an
#       interactive browser session that cannot run in an unattended
#       build").
#   (b) A verb match inside backticks or inside a hyphenated compound
#       is not an imperative verb — the "check" in `loop-design-check`
#       (hackathon-mode.mdc:38) and in "Sanity-check"
#       (feature-expansion/SKILL.md:100) are noun fragments of a
#       longer token, not instructions.
#   (c) A CUT name annotated as cut in the same breath ("was cut" /
#       "were cut" / "NOT invoked" within 20 characters after the
#       name) is a historical note, not a dispatch target — that is
#       what feature-expansion/SKILL.md:100 needs ("... (fix #27,
#       REROUTE_F27 — `product-lens` was cut)"). A live dispatch never
#       phrases its target as already cut.
# With (a)-(c) the check passes on the post-fix tree and still fails on
# the old :119 line (proven by the round-3 both-ways test).
_VERB_12B_RE = _re.compile(r"\b(use|check|consult|run|invoke|call|load|read)\b", _re.I)
_NEG_12B = ("not", "never", "n't", "n\u2019t", "do not")
_NOTE_12B_RE = _re.compile(r"(?:was|were)\s+cut\b|NOT\s+invoked\b|not\s+invoked\b", _re.I)
_SKILL_WORD_12B_RE = _re.compile(r"\b(?:skill|agent|command)s?\b", _re.I)


def _imperative_dispatch_12b(line):
    """First (verb, CUT name) imperative dispatch in line, else None."""
    _bt_spans = [(m.start(), m.end())
                 for m in _re.finditer(r"`[^`\n]*`", line)]
    for _vm in _VERB_12B_RE.finditer(line):
        if any(s <= _vm.start() < e for s, e in _bt_spans):
            continue
        if _vm.start() > 0 and line[_vm.start() - 1] == "-":
            continue
        if _vm.end() < len(line) and line[_vm.end()] == "-":
            continue
        _prefix = line[max(0, _vm.start() - 15):_vm.start()].lower()
        if any(_neg in _prefix for _neg in _NEG_12B):
            continue
        _window = line[_vm.end():_vm.end() + 120]
        for _name in _CUT_NAMES:
            for _nm in _re.finditer(
                    r"(?<![A-Za-z0-9_-])" + _re.escape(_name) + r"(?![A-Za-z0-9_-])",
                    _window):
                _a = _vm.end() + _nm.start()
                _b = _vm.end() + _nm.end()
                _backticked = (_a > 0 and line[_a - 1] == "`"
                               and _b < len(line) and line[_b] == "`")
                _followed = bool(_SKILL_WORD_12B_RE.search(line[_b:_b + 30]))
                if not (_backticked or _followed):
                    continue
                if _NOTE_12B_RE.search(line[_b:_b + 20]):
                    continue
                return (_vm.group(0), _name)
    return None


_12b_bad = []
for _path12b, _lines12b in sorted(ALLOW_LIST.items()):
    _fp12b = os.path.join(BASE, _path12b)
    if not os.path.exists(_fp12b):
        _12b_bad.append(f"{_path12b}: allow-listed file missing from the built tree")
        continue
    _text12b = open(_fp12b, encoding="utf-8").read().splitlines()
    for _ln12b in sorted(_lines12b):
        if _ln12b > len(_text12b):
            _12b_bad.append(f"{_path12b}:{_ln12b}: allow-listed line missing from the built tree")
            continue
        _hit12b = _imperative_dispatch_12b(_text12b[_ln12b - 1])
        if _hit12b:
            _12b_bad.append(f"{_path12b}:{_ln12b}: imperative dispatch "
                            f"'{_hit12b[0]}' -> CUT '{_hit12b[1]}' :: "
                            f"{_text12b[_ln12b - 1].strip()[:160]}")
if _12b_bad:
    print(f"   check-12b hits ({len(_12b_bad)}):")
    for _u in _12b_bad:
        print(f"   ! {_u}")
print(f"   check-12b: {len(_12b_bad)} imperative dispatch(es) hiding in allow-listed lines")
check("check 12b: no imperative dispatch to a CUT skill/agent/command hides in an allow-listed line",
      not _12b_bad)

failed = [n for n, ok in checks if not ok]
print(f"\n{len(checks) - len(failed)}/{len(checks)} checks pass")
sys.exit(1 if failed else 0)
