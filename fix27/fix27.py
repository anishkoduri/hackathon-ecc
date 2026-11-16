#!/usr/bin/env python3
"""Fix #27 — build-time debloat + weekend-rule patches (UPSTREAM halves).

Run by build.sh as a patch step (after fix26, before STEP 5 Counts):
    python3 "$PLUGIN_ROOT/fix27/fix27.py" "$PLUGIN_DIR"

Operates on the BUILT tree only. Staged-source halves are edited directly
in new-skills/ / round2-skills/ / rewritten-skills/ / new-rules/ and flow
through the STEP 2 copy. Every text patch asserts its anchor occurs
EXACTLY once and fails loudly on mismatch; the script exits non-zero on
any error so the build fails rather than shipping a half-patched tree.
Removals are idempotent-tolerant: a dir/file already absent is recorded
as already-absent and does NOT fail the build (the STEP 2 assembly may
vary); text-patch anchor misses DO fail the build.

SPEC fix27/SPEC.md §1 (round-1 numbers — actuals after the round-2/3
additions are 67 skills / 32 commands dropped / README 67/45/123/55;
see MANIFEST.md): 166 -> 66 skills (100 CUT: the 91 in
fix27/skill-inventory.md's CUT list + the 10 REVIEW adjudications in
SPEC §1(a), minus gan-style-harness which is KEPT per the coordinator's
dispatch-evidence adjudication — orch-build-mvp's inner loop IS
/gan-build, so the inventory's duplication claim does not hold;
growth-log is KEPT). Companion agents whose sole skill is CUT go (27
found); commands whose sole target is a CUT skill/agent go (32 after the
5 round-2 drops: learn-eval, project-init, projects, promote, prune);
the trigger table is pruned of CUT skills (15 keys); README count lines
move to 67 / 45 / 123 / 55.

Do NOT delete the skills from build.sh STEP 2: the STEP 3 patches assume
the full tree. Removal happens here, after fix26, before STEP 5 Counts.
Never re-run fix11/fix11-stage.py. Never edit the built tree directly
outside this script; never edit build.sh or any staged skill here.

Round 2 (audit #74, fix #27 round 2): the build-time half of the
reference cleanup. The 5 HELD commands are adjudicated (learn KEEP;
learn-eval, project-init, projects, promote, prune CUT), so commands
go 60 -> 55 (32 dropped total) and skills go 66 -> 67 with the vendored
motionsites-web-builder (STEP 2 copies it into skills/ before this
script runs). New patches (§7): re-route the live CUT dispatches audit
#74 found in ECC-origin files (B1, B2, B5, B7-B13, B15) and clean the
stale prose (M3-M6). The staged-owned half (orchestrate, hackathon-mode
§5/§6/§7, dispatch-prompt) is the staged-edits worker's, not this
script's.
"""
import json
import os
import shutil
import sys

BASE = sys.argv[1]
CHANGES = []
ERRORS = []
OWED = []
DECISIONS = []


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


# ---------------------------------------------------------------- §1(a) the cut: 100 skills
# 91 from skill-inventory.md CUT list + 10 REVIEW adjudications
# (SPEC §1(a)), minus gan-style-harness (KEPT — coordinator adjudication:
# orch-build-mvp's inner loop IS /gan-build, so the inventory's
# duplication claim does not hold); growth-log is KEPT and is NOT in
# this list.
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
assert len(CUT_SKILLS) == 100, f"CUT_SKILLS must be 100, got {len(CUT_SKILLS)}"
assert "growth-log" not in CUT_SKILLS, "growth-log is KEPT (SPEC §1(a))"
assert "gan-style-harness" not in CUT_SKILLS, "gan-style-harness is KEPT (coordinator adjudication)"

# ---------------------------------------------------------------- §1(b) companion agents: sole skill CUT (27)
# Exhaustively matched against agents/ + the CUT list. The first 17 are
# the companions of exactly one CUT skill (bengali-nlp, dotnet-patterns /
# csharp-testing, django-patterns, dart-flutter-patterns,
# flutter-dart-code-review, fsharp-testing, kotlin-patterns (x2),
# opensource-pipeline (x3), rust-patterns (x2), vue-patterns). The
# next 10 are the coordinator's OWED-8 adjudication: their only language
# skills are CUT (or, for Swift, nonexistent), and their only referrers
# are dropped commands or the call map — cpp x2 (cpp-build/cpp-review
# dropped), dart (flutter-build/flutter-test dropped), go x2 (go-build/
# go-review dropped), java x2 (call-map only), php (call-map only), ruby
# (call-map only), swift x2 (call-map only), conversation-analyzer
# (triggered by the dropped /hookify), marketing-agent (content-engine/
# market-research CUT). KEPT: ecc-a11y-architect (serves kept
# frontend-a11y), and the 3 gan agents (gan-style-harness is KEPT).
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
assert len(REMOVED_AGENTS) == 27

# ---------------------------------------------------------------- §1(b) commands: sole target CUT (27)
# Each candidate below was VERIFIED by reading the command file before
# dropping (reasons in DECISIONS / patch log). skill-create, skill-health
# and epic-decompose are NOT candidates (SPEC §1(b)) and are untouched.
# learn, learn-eval and project-init are HELD (not dropped): learn /
# learn-eval are skill-creation workflows, not continuous-learning-v2
# commands (their descriptions distinguish them from it), and
# project-init takes --skills as a parameter — recorded as OWED for the
# audit to adjudicate. gan-build / gan-design are KEPT (gan stays).
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
    # Round 2 (audit #74 HELD-command adjudications, coordinator's):
    # learn-eval duplicates /learn and its quality-gate rubric source
    # (agent-self-evaluation) is removed; project-init is ECC
    # install/onboarding, not a build step; projects/promote/prune are
    # thin wrappers invoking the removed
    # continuous-learning-v2/scripts/instinct-cli.py.
    "learn-eval", "project-init", "projects", "promote", "prune",
]
assert len(DROPPED_COMMANDS) == 32

COMMAND_DECISIONS = {
    "flutter-build": "DROP — invokes dart-build-resolver agent + skills/flutter-dart-code-review/ (CUT); verification-loop mention is a Related link, not a target.",
    "flutter-review": "DROP — invokes flutter-reviewer agent + skills/flutter-dart-code-review/ (CUT); /code-review is named only as the general alternative.",
    "flutter-test": "DROP — invokes flutter-reviewer + dart-build-resolver agents + skills/flutter-dart-code-review/ (CUT).",
    # gan-build / gan-design are KEPT (gan-style-harness is KEPT — coordinator
    # adjudication; orch-build-mvp's inner loop IS /gan-build). No entries here.
    "hookify-configure": "DROP — hookify-rules skill (CUT); frontmatter says upstream-only, no Cursor equivalent in this plugin.",
    "hookify-help": "DROP — hookify-rules skill (CUT); upstream-only per frontmatter.",
    "hookify-list": "DROP — hookify-rules skill (CUT); upstream-only per frontmatter.",
    "hookify": "DROP — hookify-rules skill (CUT) + conversation-analyzer agent trigger; upstream-only per frontmatter.",
    "kotlin-build": "DROP — invokes kotlin-build-resolver agent + skills/kotlin-patterns/ (CUT).",
    "kotlin-review": "DROP — invokes kotlin-reviewer agent + skills/kotlin-patterns/ + skills/kotlin-testing/ (both CUT).",
    "kotlin-test": "DROP — subject is Kotlin tests (skills/kotlin-testing/ CUT); the skills/tdd-workflow/ citation is a cited methodology, not a second served target.",
    "marketing-campaign": "DROP — delegates to the marketing-agent for campaign/content work; the content-engine + market-research skills that cover that work are CUT, and marketing is not a winning-build step. (The marketing-agent file is removed with it; see the agent list.)",
    "rust-build": "DROP — invokes rust-build-resolver agent + skills/rust-patterns/ (CUT).",
    "rust-review": "DROP — invokes rust-reviewer agent + skills/rust-patterns/ + skills/rust-testing/ (both CUT).",
    "rust-test": "DROP — skills/rust-testing/ + skills/rust-patterns/ (both CUT); no kept skill cited.",
    "security-scan": "DROP — slash-command entrypoint for the security-scan skill (CUT); frontmatter says 'prefer the security-scan skill'. The kept security-review skill / security-reviewer agent (mid-build checklist) are NOT this command's target.",
    "vue-review": "DROP — subject is Vue review (skills/vue-patterns/ CUT, vue-reviewer agent CUT); the typescript-reviewer companion runs only on Vue-related TS/JS, and pure .ts/.js changes are routed to /code-review instead — it does not serve a kept skill.",
    "cpp-build": "DROP — invokes the cpp-build-resolver agent for C++ build errors (skills/cpp-coding-standards/ + skills/cpp-testing/ CUT); coordinator adjudication.",
    "cpp-review": "DROP — invokes the cpp-reviewer agent for C++ review (C++ skills CUT); coordinator adjudication.",
    "cpp-test": "DROP — C++ test command (example writes a C++ test file; skills/cpp-testing/ CUT); coordinator adjudication.",
    "go-build": "DROP — invokes the go-build-resolver agent for Go build errors (skills/golang-patterns/ + skills/golang-testing/ CUT); coordinator adjudication.",
    "go-review": "DROP — invokes the go-reviewer agent for Go review (Go skills CUT); coordinator adjudication.",
    "go-test": "DROP — Go test command, references /go-build + /go-review (both dropped, Go skills CUT); coordinator adjudication.",
    "gradle-build": "DROP — fixes Gradle build errors for Android and Kotlin Multiplatform projects (android-clean-architecture, kotlin-patterns, compose-multiplatform-patterns all CUT); coordinator adjudication.",
    "evolve": "DROP — runs skills/continuous-learning-v2/scripts/instinct-cli.py evolve (skill dir removed); coordinator adjudication.",
    "instinct-export": "DROP — exports instincts from the continuous-learning-v2 instinct system (skill dir removed); coordinator adjudication.",
    "instinct-import": "DROP — runs skills/continuous-learning-v2/scripts/instinct-cli.py import (skill dir removed); coordinator adjudication.",
    "instinct-status": "DROP — shows learned instincts via the continuous-learning-v2 instinct CLI (skill dir removed); coordinator adjudication.",
    "learn-eval": "DROP — duplicates /learn with a quality gate whose rubric source (agent-self-evaluation skill) is removed; uncalled (call map); coordinator adjudication (audit #74 HELD-command decision).",
    "project-init": "DROP — ECC install/onboarding, not a build step (same category as CUT agent-sort); its only caller is the commands/ecc-guide.md:85 pointer, removed in this round; its example names removed continuous-learning-v2; coordinator adjudication (audit #74).",
    "projects": "DROP — runs skills/continuous-learning-v2/scripts/instinct-cli.py projects (skill dir removed); coordinator adjudication (audit #74).",
    "promote": "DROP — runs skills/continuous-learning-v2/scripts/instinct-cli.py promote (skill dir removed); coordinator adjudication (audit #74).",
    "prune": "DROP — runs skills/continuous-learning-v2/scripts/instinct-cli.py prune (skill dir removed); coordinator adjudication (audit #74).",
}

# ---------------------------------------------------------------- 1. remove the 100 CUT skill dirs
_skills_removed, _skills_absent = [], []
for _s in CUT_SKILLS:
    _d = p(f"skills/{_s}")
    if os.path.isdir(_d):
        shutil.rmtree(_d)
        _skills_removed.append(_s)
    elif exists(_d):
        os.remove(_d)
        _skills_removed.append(_s)
    else:
        _skills_absent.append(_s)
CHANGES.append(f"skills removed: {len(_skills_removed)} dirs "
               f"({len(_skills_absent)} already absent: "
               f"{', '.join(_skills_absent) or 'none'})")
if _skills_removed:
    CHANGES.append("skills removed: " + ", ".join(_skills_removed))

# ---------------------------------------------------------------- 2. remove the 27 companion agents
_agents_removed, _agents_absent = [], []
for _a in REMOVED_AGENTS:
    _f = p(f"agents/{_a}.md")
    if exists(_f):
        os.remove(_f)
        _agents_removed.append(_a)
    else:
        _agents_absent.append(_a)
CHANGES.append(f"agents removed: {len(_agents_removed)} files "
               f"({len(_agents_absent)} already absent: "
               f"{', '.join(_agents_absent) or 'none'})")
if _agents_removed:
    CHANGES.append("agents removed: " + ", ".join(_agents_removed))

# ---------------------------------------------------------------- 3. drop the 32 CUT-only commands
_cmds_removed, _cmds_absent = [], []
for _c in DROPPED_COMMANDS:
    DECISIONS.append(f"{_c}: {COMMAND_DECISIONS[_c]}")
    _f = p(f"commands/{_c}.md")
    if exists(_f):
        os.remove(_f)
        _cmds_removed.append(_c)
    else:
        _cmds_absent.append(_c)
CHANGES.append(f"commands dropped: {len(_cmds_removed)} files "
               f"({len(_cmds_absent)} already absent: "
               f"{', '.join(_cmds_absent) or 'none'})")
if _cmds_removed:
    CHANGES.append("commands dropped: " + ", ".join(_cmds_removed))

# ---------------------------------------------------------------- 4. prune the trigger table
# manifests/context-packs/skill-triggers@1.json is a JSON object; the
# per-skill trigger entries live under the top-level "triggers" key,
# keyed "skill:<name>". Prune keys whose skill is CUT; update coverage.
_tf = p("manifests/context-packs/skill-triggers@1.json")
if exists(_tf):
    with open(_tf, encoding="utf-8") as _fh:
        _trig = json.load(_fh)
    _before = len(_trig["triggers"])
    _pruned = [k for k in list(_trig["triggers"])
               if k.split(":", 1)[1] in CUT_SKILLS]
    for _k in _pruned:
        del _trig["triggers"][_k]
    _trig["coverage"]["skills"] = 67
    _trig["coverage"]["withTriggers"] = len(_trig["triggers"])
    # M3 (audit #74): the notes prose still lists three CUT skills as
    # deferred. Rewrite the deferred list to the three kept checks.
    _old_notes = _trig.get("notes", "")
    _old_deferred = ("Deferred: production-audit, delivery-gate, "
                     "codehealth-mcp, santa-method, security-scan, "
                     "verification-loop.")
    if _old_deferred not in _old_notes:
        ERRORS.append(f"trigger notes: expected deferred list not found :: {_old_deferred!r}")
    else:
        _trig["notes"] = _old_notes.replace(
            _old_deferred,
            "Deferred: verification-loop, production-audit, delivery-gate. (DEFER3_F27)")
        CHANGES.append("trigger notes deferred list -> the three kept checks (DEFER3_F27)")
    with open(_tf, "w", encoding="utf-8") as _fh:
        json.dump(_trig, _fh, indent=1, ensure_ascii=True)
        _fh.write("\n")
    CHANGES.append(f"trigger table pruned: {len(_pruned)} keys "
                   f"({_before} -> {len(_trig['triggers'])}); "
                   f"coverage.skills 166 -> 67, withTriggers -> "
                   f"{len(_trig['triggers'])}")
    CHANGES.append("trigger keys pruned: " + ", ".join(sorted(_pruned)))
    if len(_pruned) != 15:
        ERRORS.append(f"trigger prune: expected 15 CUT keys, pruned {len(_pruned)}")
else:
    ERRORS.append(f"trigger file missing: {_tf}")

# ---------------------------------------------------------------- 5. README count lines -> 67 / 45 / 123 / 55
# Found by grepping the built tree for "166 skills": README.md:13, :36,
# :38, :40 only (line 11's "144 skills, 69 agents" is the stock-ECC
# description and is NOT touched). Agents: 72 - 27 removed = 45
# (69 as-shipped - 27 = 42 as-shipped + 3 staged). Commands: 87 - 32 = 55.
# Round 2: skills 66 -> 67 (motionsites-web-builder vendored),
# commands 60 -> 55 (learn-eval, project-init, projects, promote, prune).
_f = p("README.md")
if exists(_f):
    sub(_f,
        "166 skills, 72 agents, 123 rules, and 87 commands in total (69 agents as-shipped + 3 staged orchestrate agents;",
        "67 skills, 45 agents, 123 rules, and 55 commands in total (42 agents as-shipped + 3 staged orchestrate agents;")
    sub(_f,
        "166 skills widen the routing surface",
        "67 skills widen the routing surface")
    sub(_f,
        "56 MB and 166 skills against a minimal set",
        "56 MB and 67 skills against a minimal set")
    sub(_f,
        "structured process — 166 skills, 72 agents, 87 commands,",
        "structured process — 67 skills, 45 agents, 55 commands,")
    # M5 (audit #74): stale CUT references in the README prose.
    sub(_f,
        "plus the marketplace skills (brainstorming,\n  systematic-debugging, dispatching-parallel-agents, agents-md-generator,\n  verification-before-completion)",
        "plus the marketplace skills (systematic-debugging,\n  verification-before-completion)")
    sub(_f,
        "Playwright MCP, codebase-memory MCP, and the audit deferral",
        "Playwright MCP and the audit deferral")
    sub(_f,
        "## Commands (highlights — 3 of 87)",
        "## Commands (highlights — 3 of 55)")
    sub(_f,
        "Security tests and audits (`production-audit`, `delivery-gate`,\n`codehealth-mcp`, `verification-loop`, `santa-method`, and `security-scan`) run ONLY at the",
        "Security tests and audits (`verification-loop`, `production-audit`, and `delivery-gate`) run ONLY at the")
    sub(_f,
        "such as `/quality-gate`, `/security-scan`, and the `*-build`/`*-test` commands still reference them",
        "such as `/quality-gate` and the `*-build`/`*-test` commands still reference them")
    sub(_f,
        "`codebase-memory` queries a local knowledge graph of the repo (functions, classes, call chains, routes) instead of reading files one by one: find where a feature lives, trace callers/callees, hunt dead code, and run impact analysis before a change. It is backed by the `codebase-memory-mcp` MCP server, a native binary the user installs once on their machine (Windows: run the repo's `install.ps1`; macOS/Linux: `install.sh`) — it is not bundled in the plugin, needs no network calls and no API key, and the plugin's `mcp.json` points at the installed binary. (Per the project's own docs — not independently verifiable from this plugin; the binary is neither bundled nor audited here.)",
        "`codebase-memory` was cut in fix #27 and is not shipped. Explore unfamiliar code with grep-and-read and the `ecc-code-explorer` agent instead: find where a feature lives, trace callers/callees, hunt dead code, and run impact analysis before a change.")
else:
    ERRORS.append(f"README missing: {_f}")

# ---------------------------------------------------------------- 6a. delivery-gate: dangling agent-self-evaluation pointer
# skills/delivery-gate/SKILL.md:97 — agent-self-evaluation is CUT; reword
# to pair with a manual review of the recorded entries.
_f = p("skills/delivery-gate/SKILL.md")
if exists(_f):
    sub(_f,
        "For content quality verification, pair with `agent-self-evaluation` "
        "(the shipped equivalent; upstream `self-audit` is not shipped in this plugin).",
        "For content quality verification, pair with a manual review of the "
        "recorded entries (the mechanical gate checks only that entries were "
        "touched, not their quality).")
else:
    ERRORS.append(f"delivery-gate SKILL.md missing: {_f}")

# ---------------------------------------------------------------- 6b. browser-qa: single capture run (SPEC §4(c))
# skills/browser-qa/SKILL.md Phase 3 step 2 (baseline line): polish-pass
# captures once, browser-qa consumes those captures and shoots only what
# the matrix lacks.
_f = p("skills/browser-qa/SKILL.md")
if exists(_f):
    sub(_f,
        "no baseline ⇒ report INCONCLUSIVE, never a silent PASS",
        "no baseline ⇒ report INCONCLUSIVE, never a silent PASS\n"
        "Single capture run (CAPTURE1_F27): `polish-pass` captures once; "
        "`browser-qa` consumes those captures and shoots only what the "
        "capture matrix lacks — never re-shoot a state/width the "
        "polish-pass captures already cover.")
else:
    ERRORS.append(f"browser-qa SKILL.md missing: {_f}")

# ---------------------------------------------------------------- 6c. verification-before-completion: claim-table row (SPEC §5(d))
_f = p("skills/verification-before-completion/SKILL.md")
if exists(_f):
    sub(_f,
        '| Agent completed | VCS diff shows changes | Agent reports "success" |',
        '| Agent completed | VCS diff shows changes | Agent reports "success" |\n'
        '| UI verified | browser-qa verdict on the rendered screen (TESTNOTBQA_F27) | test suite passing, screenshots described but not inspected, agent report |')
else:
    ERRORS.append(f"verification-before-completion SKILL.md missing: {_f}")

# ---------------------------------------------------------------- 6d. hackathon-pitch: CHECK-THE-SOURCE + AUDIT-AS-GUIDE (SPEC §5(c))
_f = p("skills/hackathon-pitch/SKILL.md")
if exists(_f):
    sub(_f,
        "- **Three specifics per sixty seconds.** Numbers, names, places.",
        "- **Three specifics per sixty seconds.** Numbers, names, places.\n"
        "\n"
        "**CHECK-THE-SOURCE (CHECKSRC_F27).** Every scoring, timing, or "
        "logistics claim in a final report, reply, or deliverable prompt "
        "cites the source document it was read from (spec section, invite, "
        "rubric) with the value as written there. An estimate is labelled "
        "an estimate with its basis; a measured value replaces the estimate "
        "in the record the moment it is measured. Never restate a remembered "
        "number as a fact. Final-report checklist line: "
        "\"Scoring/timing/logistics claims — source cited per claim, or the "
        "claim is removed.\"\n"
        "\n"
        "**AUDIT-AS-GUIDE (AUDITGUIDE_F27).** An audit (sloplint, reviewer, "
        "or any checklist pass) is a guide, never the source. The source is "
        "the spec / the rendered screen / the measured run. Where an audit "
        "and the source disagree, the source wins and the disagreement is "
        "recorded. Every number in a deliverable prompt or submission cites "
        "the exact spec section and uses only exact verified numbers — no "
        "rounded, remembered, or inferred figures.")
else:
    ERRORS.append(f"hackathon-pitch SKILL.md missing: {_f}")

# ---------------------------------------------------------------- 6e. common-git-workflow: no Co-authored-by rule (SPEC §5(e))
# Placed under "## Commit Message Format", where commit-message rules live.
_f = p("rules/common-git-workflow.mdc")
if exists(_f):
    sub(_f,
        "Types: feat, fix, refactor, docs, test, chore, perf, ci",
        "Types: feat, fix, refactor, docs, test, chore, perf, ci\n"
        "\n"
        "Commit messages carry no `Co-authored-by:` trailer for any AI tool "
        "(including Cursor) and name no AI tool as author or contributor. "
        "The commit author is the user. (NOCOAUTHOR_F27)")
else:
    ERRORS.append(f"common-git-workflow.mdc missing: {_f}")

# ---------------------------------------------------------------- 6f. other dispatch references to CUT skills (kept tree)
# Exhaustive grep of every CUT skill name across the kept tree
# (skills/commands/agents/rules, removed dirs excluded) found the
# references below. Two are safe, verifiable re-routes patched here;
# the rest are ambiguous and are recorded OWED, NOT patched blindly.
# Round 2 (§7) patches the OWED items this section recorded
# (B1/B5/B7-B13/B15/M4/M6) — the OWED texts below are updated to match.
# (a) orchestrate :101 drafts commit messages with the CUT
# conventional-commit-review skill — re-route to the kept git-workflow
# skill, which carries the commit conventions.
_f = p("skills/orchestrate/SKILL.md")
if exists(_f):
    sub(_f,
        "draft each commit message with the `conventional-commit-review` skill (`skills/conventional-commit-review/SKILL.md`)",
        "draft each commit message with the `git-workflow` skill (`skills/git-workflow/SKILL.md`)")
else:
    ERRORS.append(f"orchestrate SKILL.md missing: {_f}")
# (b) security-review frontmatter dispatches the end-of-project config
# audit to the CUT security-scan skill; no kept equivalent exists for the
# AgentShield config audit, so the dispatch sentence is removed (the
# kept mid-build checklist in this skill is untouched).
_f = p("skills/security-review/SKILL.md")
if exists(_f):
    sub(_f,
        " For the end-of-project configuration audit, use security-scan.",
        "")
else:
    ERRORS.append(f"security-review SKILL.md missing: {_f}")

# ---------------------------------------------------------------- 6g. deferred check lists: six -> three (SPEC §1(b))
# codehealth-mcp, santa-method and security-scan are CUT, so the
# end-of-project deferred set shrinks to the three kept checks
# (verification-loop, production-audit, delivery-gate). Anchors are the
# exact list sentences (each occurs once, in a distinct word order).
# hackathon-mode.mdc §3 carries the same list in staged sources — the
# staged-edits worker owns that file, not this script.
_f = p("skills/orchestrate/SKILL.md")
if exists(_f):
    sub(_f,
        "(`production-audit`, `delivery-gate`, `codehealth-mcp`, `verification-loop`, `santa-method`, and `security-scan`)",
        "(`production-audit`, `delivery-gate`, and `verification-loop`) (DEFER3_F27)")
    sub(_f,
        "run the six deferred checks by name — `verification-loop`, `production-audit`, `delivery-gate`, `codehealth-mcp`, `santa-method`, `security-scan`",
        "run the three deferred checks by name — `verification-loop`, `production-audit`, `delivery-gate`")
    sub(_f,
        "one line per deferred check (`verification-loop`, `production-audit`, `delivery-gate`, `codehealth-mcp`, `santa-method`, `security-scan`)",
        "one line per deferred check (`verification-loop`, `production-audit`, `delivery-gate`)")
else:
    ERRORS.append(f"orchestrate SKILL.md missing: {_f}")
_f = p("skills/orch-build-mvp/SKILL.md")
if exists(_f):
    sub(_f,
        "run the six deferred end-of-project checks by name (`verification-loop`, `production-audit`, `delivery-gate`, `codehealth-mcp`, `santa-method`, `security-scan`)",
        "run the three deferred end-of-project checks by name (`verification-loop`, `production-audit`, `delivery-gate`)")
else:
    ERRORS.append(f"orch-build-mvp SKILL.md missing: {_f}")

# ---------------------------------------------------------------- 7a. B1 (audit #74): inherit-legacy-style re-route
# The 5 orch-* UI-change rules + ui-ux-pro-max route legacy drift to the
# CUT inherit-legacy-style skill. Re-route to the feature-expansion
# wording: drift handled inside the design package, no separate skill.
# (orchestrate's own copies are staged sources — the staged worker's.)
for _f_name in ("orch-add-feature", "orch-change-feature",
                "orch-fix-defect", "orch-refine-code"):
    _f = p(f"skills/{_f_name}/SKILL.md")
    if exists(_f):
        sub(_f,
            "legacy style drift: + `inherit-legacy-style`",
            "legacy style drift: handled inside the design package — no separate skill (fix #27, REROUTE_F27)")
    else:
        ERRORS.append(f"{_f_name} SKILL.md missing: {_f}")
_f = p("skills/orch-build-mvp/SKILL.md")
if exists(_f):
    sub(_f,
        "legacy drift: + `inherit-legacy-style`",
        "legacy drift: handled inside the design package — no separate skill (fix #27, REROUTE_F27)")
else:
    ERRORS.append(f"orch-build-mvp SKILL.md missing: {_f}")
_f = p("skills/ui-ux-pro-max/SKILL.md")
if exists(_f):
    sub(_f,
        "On a hand-written legacy codebase, run `inherit-legacy-style` before writing UI, so new work follows the codebase's own conventions instead of drifting from them.",
        "On a hand-written legacy codebase, legacy style drift is handled inside the design package — no separate skill (fix #27, REROUTE_F27) — so new work follows the codebase's own conventions instead of drifting from them.")
else:
    ERRORS.append(f"ui-ux-pro-max SKILL.md missing: {_f}")

# ---------------------------------------------------------------- 7b. B2 (audit #74): lift the theme cage in the two
# ECC-origin E1 copies (orch-build-mvp:43, ui-ux-pro-max:274), mirroring
# the fixed copies in orchestrate:148 / design-taste-frontend:423.
for _f_name in ("orch-build-mvp", "ui-ux-pro-max"):
    _f = p(f"skills/{_f_name}/SKILL.md")
    if exists(_f):
        sub(_f,
            "(2) fit the theme's material world — material, tokens, palette balance, do-nots;",
            "(2) fit the theme's material world — material, tokens, palette balance, do-nots — **or a recorded departure from it** (D19 reason required) (fix #27, THEME-START_F27);")
        sub(_f,
            "NOT within reason: a new theme (re-deal instead, Taste step 4); a new palette",
            "NOT within reason: a new palette")
        sub(_f,
            "breaking a floor or a ban (craft-floor bans are absolute; the Hallmark floor binds). Each invented element's",
            "breaking a floor or a ban (craft-floor bans are absolute; the Hallmark floor binds). Inventing a theme direction is a recorded D19 decision, not a forbidden move (fix #27, THEME-START_F27): a departure from the dealt theme is recorded with what was departed from and why the job needs it — a re-deal is the easy path, a recorded departure is the permitted one. Each invented element's")
    else:
        ERRORS.append(f"{_f_name} SKILL.md missing: {_f}")

# ---------------------------------------------------------------- 7c. B5 (audit #74): prp-commit re-route
# Same re-route as orchestrate §6 (fix #25 §1): conventional-commit-review
# (CUT) -> the kept git-workflow skill.
_f = p("commands/prp-commit.md")
if exists(_f):
    sub(_f,
        "Draft the message with the `conventional-commit-review` skill (`skills/conventional-commit-review/SKILL.md`, fix #25 §1) — it reads the repo's own history norms (`git log --no-merges --format=%s -30`) for type, scope, and length instead of the generic table below; the table is the fallback when the skill cannot run.",
        "Draft the message with the `git-workflow` skill (`skills/git-workflow/SKILL.md`) — it reads the repo's own history norms (`git log --no-merges --format=%s -30`) for type, scope, and length instead of the generic table below; the table is the fallback when the skill cannot run.")
else:
    ERRORS.append(f"prp-commit.md missing: {_f}")

# ---------------------------------------------------------------- 7d. B6 (audit #74): CLv2 remnants in kept commands
# skill-create still offers the removed continuous-learning-v2 instinct
# system (--instincts flag, step 4, Step 4 section, Related Commands);
# ecc-guide still points at the dropped /project-init; epic-sync still
# lists the dropped /projects as a compatibility alias.
_f = p("commands/skill-create.md")
if exists(_f):
    sub(_f,
        "/skill-create --instincts        # Also generate instincts for continuous-learning-v2\n",
        "")
    sub(_f,
        "4. **Optionally Creates Instincts** - For the continuous-learning-v2 system\n",
        "")
    sub(_f,
        "### Step 4: Generate Instincts (if --instincts)\n"
        "\n"
        "For continuous-learning-v2 integration:\n"
        "\n"
        "```yaml\n"
        "---\n"
        "id: {repo}-commit-convention\n"
        "trigger: \"when writing a commit message\"\n"
        "confidence: 0.8\n"
        "domain: git\n"
        "source: local-repo-analysis\n"
        "---\n"
        "\n"
        "# Use Conventional Commits\n"
        "\n"
        "## Action\n"
        "Prefix commits with: feat:, fix:, chore:, docs:, test:, refactor:\n"
        "\n"
        "## Evidence\n"
        "- Analyzed {n} commits\n"
        "- {percentage}% follow conventional commit format\n"
        "```\n"
        "\n",
        "")
    sub(_f,
        "## Related Commands\n"
        "\n"
        "- `/instinct-import` - Import generated instincts\n"
        "- `/instinct-status` - View learned instincts\n"
        "- `/evolve` - Cluster instincts into skills/agents\n"
        "\n",
        "")
else:
    ERRORS.append(f"skill-create.md missing: {_f}")
_f = p("commands/ecc-guide.md")
if exists(_f):
    sub(_f,
        "- `/project-init` for stack-aware ECC onboarding of a target project\n",
        "")
else:
    ERRORS.append(f"ecc-guide.md missing: {_f}")
_f = p("commands/epic-sync.md")
if exists(_f):
    sub(_f,
        "Compatibility aliases:\n\n- `/projects`\n",
        "")
else:
    ERRORS.append(f"epic-sync.md missing: {_f}")

# ---------------------------------------------------------------- 7e. B7 (audit #74): /security-scan pointers -> kept security-review
# The security-scan command was dropped; re-point its four callers at the
# kept security-review skill, and re-point the harness-audit.js
# security-scan-command check at the kept skill (check id unchanged).
# Coordinator addition: the harness-audit.js memory-learning-skill check
# (same class — asserts removed continuous-learning-v2 exists, fails by
# design on every run) is re-pointed at the kept growth-log skill.
_f = p("commands/ecc-guide.md")
if exists(_f):
    sub(_f,
        "- `/security-scan` (END-ONLY) for agent configuration security review",
        "- `security-review` skill (END-ONLY) for agent configuration security review")
else:
    ERRORS.append(f"ecc-guide.md missing: {_f}")
_f = p("commands/fastapi-review.md")
if exists(_f):
    sub(_f,
        "- Command: `/security-scan` (END-ONLY — end of project or on explicit ask)",
        "- Skill: `security-review` (END-ONLY — end of project or on explicit ask)")
else:
    ERRORS.append(f"fastapi-review.md missing: {_f}")
_f = p("commands/harness-audit.md")
if exists(_f):
    sub(_f,
        "for a security-specific audit use the security-scan command (END-ONLY — only at the very end of the project).",
        "for a security-specific audit use the `security-review` skill (END-ONLY — only at the very end of the project).")
else:
    ERRORS.append(f"harness-audit.md missing: {_f}")
_f = p("rules/react-native-security.mdc")
if exists(_f):
    sub(_f,
        "Use `/security-scan` (AgentShield, END-ONLY — end of project or on explicit ask) on the agent configuration itself.",
        "Use the `security-review` skill (END-ONLY — end of project or on explicit ask) on the agent configuration itself.")
else:
    ERRORS.append(f"react-native-security.mdc missing: {_f}")
_f = p("scripts/harness-audit.js")
if exists(_f):
    sub(_f,
        "      path: 'commands/security-scan.md',\n"
        "      description: 'Security scan command exists',\n"
        "      pass: fileExists(rootDir, 'commands/security-scan.md'),\n"
        "      fix: 'Add commands/security-scan.md with scan and remediation workflow.',",
        "      path: 'skills/security-review/SKILL.md',\n"
        "      description: 'Security review skill exists',\n"
        "      pass: fileExists(rootDir, 'skills/security-review/SKILL.md'),\n"
        "      fix: 'Add skills/security-review with the security review workflow.',")
else:
    ERRORS.append(f"harness-audit.js missing: {_f}")

_f = p("scripts/harness-audit.js")
if exists(_f):
    sub(_f,
        "      path: 'skills/continuous-learning-v2/SKILL.md',\n"
        "      description: 'Continuous learning v2 skill exists',\n"
        "      pass: fileExists(rootDir, 'skills/continuous-learning-v2/SKILL.md'),\n"
        "      fix: 'Add skills/continuous-learning-v2/SKILL.md for memory evolution flow.',",
        "      path: 'skills/growth-log/SKILL.md',\n"
        "      description: 'Growth log skill exists',\n"
        "      pass: fileExists(rootDir, 'skills/growth-log/SKILL.md'),\n"
        "      fix: 'Add skills/growth-log/SKILL.md for memory evolution flow.',")
else:
    ERRORS.append(f"harness-audit.js missing: {_f}")

# ---------------------------------------------------------------- 7f. B8 (audit #74): council santa-method re-route
# End-of-project verification goes to the kept end gates
# (verification-loop / production-audit); drop the Related Skills entry.
_f = p("skills/council/SKILL.md")
if exists(_f):
    sub(_f,
        "| Verifying whether output is correct | mid-build: `verification-before-completion`; at the end of the project: `santa-method` |",
        "| Verifying whether output is correct | mid-build: `verification-before-completion`; at the end of the project: `verification-loop` / `production-audit` |")
    sub(_f,
        "| Reviewing code for bugs or security | `code-reviewer` or, at the end of the project, `santa-method` |",
        "| Reviewing code for bugs or security | `code-reviewer` or, at the end of the project, `verification-loop` / `production-audit` |")
    # M6 also touches this Related Skills block (architecture-decision-records);
    # both entries go in one patch.
    sub(_f,
        "- `santa-method` — adversarial verification (END-ONLY)\n"
        "- `architecture-decision-records` — formalize the outcome when the decision becomes long-lived system policy\n",
        "")
else:
    ERRORS.append(f"council SKILL.md missing: {_f}")

# ---------------------------------------------------------------- 7g. B9 (audit #74): integration re-routes
# skill-scout -> documentation-lookup / grep-and-read (the kept discovery
# path); mcp-server-patterns -> hand-rolled client via api-integration.
_f = p("skills/integration/SKILL.md")
if exists(_f):
    sub(_f,
        "or for building an MCP server from scratch (that is `mcp-server-patterns`).",
        "or for building an MCP server from scratch (hand-roll the client via `api-integration`) (fix #27, REROUTE_F27 — `mcp-server-patterns` was cut).")
    sub(_f,
        "1. **Check for an existing skill first.** Use `skill-scout` to search for a skill that already covers this integration (a vendor skill, an SDK skill, a sponsor skill).",
        "1. **Check for an existing skill first.** Use `documentation-lookup` (grep-and-read over the plugin's own skill list) to search for a skill that already covers this integration (a vendor skill, an SDK skill, a sponsor skill). (fix #27, REROUTE_F27 — `skill-scout` was cut)")
    sub(_f,
        "Use `mcp-server-patterns` for the server setup and wiring, and treat the MCP tools as the adapter.",
        "Use a hand-rolled client via `api-integration` for the server setup and wiring, and treat the MCP tools as the adapter. (fix #27, REROUTE_F27 — `mcp-server-patterns` was cut)")
    sub(_f,
        "This skill composes the plugin's own skills (`skill-scout`, `documentation-lookup`, `api-integration`, `hackathon-scope`, `verification-before-completion`, `hackathon-pitch`, `devpost-autofiller`, `ui-ux-pro-max`, `less-flat-ui`, `systematic-debugging`, `mcp-server-patterns`, `app-scaffold`)",
        "This skill composes the plugin's own skills (`documentation-lookup`, `api-integration`, `hackathon-scope`, `verification-before-completion`, `hackathon-pitch`, `devpost-autofiller`, `ui-ux-pro-max`, `less-flat-ui`, `systematic-debugging`, `app-scaffold`) (fix #27, REROUTE_F27 — `skill-scout` and `mcp-server-patterns` were cut)")
else:
    ERRORS.append(f"integration SKILL.md missing: {_f}")

# ---------------------------------------------------------------- 7h. B10 (audit #74): ai-feature-spec re-route
_f = p("skills/ai-feature-spec/SKILL.md")
if exists(_f):
    sub(_f,
        "For non-AI features use intent-driven-development; for API contracts use contract-first.",
        "For non-AI features use hackathon-scope; for API contracts use contract-first.")
else:
    ERRORS.append(f"ai-feature-spec SKILL.md missing: {_f}")

# ---------------------------------------------------------------- 7i. B11 (audit #74): ecc-agent-evaluator self-contained
# The 5-axis rubric and the full report format are ALREADY inline in this
# file; only the references to the removed skill are broken. Delete them
# and point at the rubric defined here (resolves OWED-5: the rubric
# source is now this file itself).
_f = p("agents/ecc-agent-evaluator.md")
if exists(_f):
    sub(_f,
        ", or when the agent-self-evaluation skill is active",
        "")
    sub(_f,
        "Read `skills/agent-self-evaluation/SKILL.md` for the detailed scoring rubric. ",
        "")
    sub(_f,
        "Work through the 5 axes from the `agent-self-evaluation` skill:",
        "Work through the 5 axes defined below:")
    sub(_f,
        "Use this exact format (matches `skills/agent-self-evaluation/scripts/evaluate.py` output):",
        "Use this exact format (defined in this file):")
    sub(_f,
        "Always include the structured report above, matching the `skills/agent-self-evaluation/scripts/evaluate.py` output format exactly.",
        "Always include the structured report above, matching the output format defined in this file exactly.")
else:
    ERRORS.append(f"ecc-agent-evaluator.md missing: {_f}")

# ---------------------------------------------------------------- 7j. B12 (audit #74, build-time half): mobile-ship
# Writing screens/features belongs to react-native-patterns alone
# (dart-flutter-patterns is CUT). hackathon-mode.mdc §6 is staged-owned.
_f = p("skills/mobile-ship/SKILL.md")
if exists(_f):
    sub(_f,
        "belongs to react-native-patterns / dart-flutter-patterns.",
        "belongs to react-native-patterns.")
else:
    ERRORS.append(f"mobile-ship SKILL.md missing: {_f}")

# ---------------------------------------------------------------- 7k. B13 (audit #74): systematic-debugging reword
_f = p("skills/systematic-debugging/SKILL.md")
if exists(_f):
    sub(_f,
        "after symptom inspection rules out an agent failure (agent-introspection-debugging) and broken-button state bugs (click-path-audit).",
        "after symptom inspection rules out an agent failure and broken-button state bugs (click-path-audit).")
else:
    ERRORS.append(f"systematic-debugging SKILL.md missing: {_f}")

# ---------------------------------------------------------------- 7l. B15 (audit #74): skill-create / skill-health descriptions
_f = p("commands/skill-create.md")
if exists(_f):
    sub(_f,
        "check the skill-scout skill first to avoid duplicating an existing local, marketplace, or GitHub skill.",
        "check the plugin's own skill list (grep-and-read) first to avoid duplicating an existing local, marketplace, or GitHub skill.")
else:
    ERRORS.append(f"skill-create.md missing: {_f}")
_f = p("commands/skill-health.md")
if exists(_f):
    sub(_f,
        "for a qualitative compliance or quality audit use the skill-stocktake skill.",
        "for a qualitative compliance or quality audit use the plugin's own skill list and verify scripts.")
else:
    ERRORS.append(f"skill-health.md missing: {_f}")

# ---------------------------------------------------------------- 7m. M4 (audit #74): delivery-gate "shipped" claims
# agent-self-evaluation is CUT; reword all four mentions to past tense /
# remove the "shipped" claims, and point the reasoning-quality-gate entry
# at the kept replacement (the self-contained ecc-agent-evaluator, B11).
_f = p("skills/delivery-gate/SKILL.md")
if exists(_f):
    sub(_f,
        "Complements agent-self-evaluation (the shipped equivalent of upstream self-audit, which is not shipped in this plugin) by mechanically enforcing learning capture habits.",
        "Complements the `ecc-agent-evaluator` agent (whose 5-axis rubric is defined in the agent file itself) by mechanically enforcing learning capture habits.")
    sub(_f,
        "This is distinct from reasoning gates (like the shipped `agent-self-evaluation` skill — the upstream `self-audit` skill is not shipped in this plugin): delivery-gate checks machine-verifiable facts; agent-self-evaluation checks output quality across four reasoning dimensions.",
        "This is distinct from reasoning gates (like the former `agent-self-evaluation` skill — cut in fix #27; its 5-axis rubric now lives in the `ecc-agent-evaluator` agent file): delivery-gate checks machine-verifiable facts; the evaluator checks output quality across five reasoning dimensions.")
    sub(_f,
        "- **agent-self-evaluation** (shipped; upstream `self-audit` is not shipped in this plugin): \"Is the file content correct, complete, and honest?\"",
        "- **`ecc-agent-evaluator`** (reasoning-quality gate; the 5-axis rubric formerly in `agent-self-evaluation` now lives in the agent file itself): \"Is the file content correct, complete, and honest?\"")
    sub(_f,
        "- `agent-self-evaluation` — Reasoning quality gate (completeness/consistency/groundedness/honesty; shipped equivalent of upstream `self-audit`, which is not shipped in this plugin)",
        "- `ecc-agent-evaluator` — Reasoning quality gate (accuracy/completeness/clarity/actionability/conciseness; the 5-axis rubric formerly in `agent-self-evaluation` now lives in the agent file itself)")
else:
    ERRORS.append(f"delivery-gate SKILL.md missing: {_f}")

# ---------------------------------------------------------------- 7n. M6 (audit #74): dangling "see skill" pointers
# Re-point or delete each; none is a dispatch. (council's Related Skills
# entries are handled in §7f above.)
_f = p("skills/contract-first/SKILL.md")
if exists(_f):
    sub(_f,
        "which governs what a good API looks like, and `ai-regression-testing`, which\nguards fixed bugs from returning.",
        "which governs what a good API looks like.")
    sub(_f,
        "- `ai-regression-testing` - regression tests for response-shape and path drift\n",
        "")
else:
    ERRORS.append(f"contract-first SKILL.md missing: {_f}")
_f = p("agents/ecc-database-reviewer.md")
if exists(_f):
    sub(_f,
        "see skills: `postgres-patterns` and `database-migrations`.",
        "see skill: `postgres-patterns`.")
else:
    ERRORS.append(f"ecc-database-reviewer.md missing: {_f}")
_f = p("skills/tdd-workflow/SKILL.md")
if exists(_f):
    sub(_f,
        " See the `bun-runtime` skill for runtime, install, and bundler details.",
        "")
else:
    ERRORS.append(f"tdd-workflow SKILL.md missing: {_f}")
_f = p("skills/postgres-patterns/SKILL.md")
if exists(_f):
    sub(_f,
        "- Skill: `clickhouse-io` - ClickHouse analytics patterns\n",
        "")
else:
    ERRORS.append(f"postgres-patterns SKILL.md missing: {_f}")
_f = p("skills/react-patterns/SKILL.md")
if exists(_f):
    sub(_f,
        ", [accessibility](../accessibility/SKILL.md), [angular-developer](../angular-developer/SKILL.md) for framework comparison",
        "")
else:
    ERRORS.append(f"react-patterns SKILL.md missing: {_f}")
_f = p("skills/typescript-patterns/SKILL.md")
if exists(_f):
    sub(_f,
        "- `nestjs-patterns` — NestJS architecture patterns for TypeScript backends (modules, controllers, providers, DTO validation)\n",
        "")
    sub(_f,
        "- `prisma-patterns` — database access patterns used in TypeScript applications\n",
        "")
else:
    ERRORS.append(f"typescript-patterns SKILL.md missing: {_f}")
_f = p("skills/react-native-patterns/SKILL.md")
if exists(_f):
    sub(_f,
        "- `coding-standards` — TypeScript/JavaScript idioms that apply to RN code.\n",
        "")
else:
    ERRORS.append(f"react-native-patterns SKILL.md missing: {_f}")
_f = p("skills/strategic-compact/SKILL.md")
if exists(_f):
    sub(_f,
        "- `continuous-learning` skill — Extracts patterns before session ends",
        "- `/learn` command — Extracts patterns before session ends")
else:
    ERRORS.append(f"strategic-compact SKILL.md missing: {_f}")
_f = p("scripts/lib/resolve-ecc-root.js")
if exists(_f):
    sub(_f,
        "// If that skill is ever renamed, move this sentinel with it.",
        "// If that skill is ever renamed, move this sentinel with it. (fix #27: sentinel moved from continuous-learning-v2 — cut — to orchestrate, which ships in every plugin root.)")
    sub(_f,
        "const DEFAULT_SKILL_PROBE = path.join('skills', 'continuous-learning-v2');",
        "const DEFAULT_SKILL_PROBE = path.join('skills', 'orchestrate');")
else:
    ERRORS.append(f"resolve-ecc-root.js missing: {_f}")

# ---------------------------------------------------------------- 7o. B6-adjacent (census-found): skill-health /evolve
# The check-12 census found one more live dispatch to a dropped command
# that audit #74 did not list: skill-health.md:46 suggests running
# /evolve (dropped, round 1 — CLv2 instinct clustering). Re-route to the
# kept /learn command, the session-review tool that extracts declining
# patterns as candidate skills.
_f = p("commands/skill-health.md")
if exists(_f):
    sub(_f,
        "3. If any skills are declining, highlight them and suggest running /evolve",
        "3. If any skills are declining, highlight them and suggest running /learn")
else:
    ERRORS.append(f"skill-health.md missing: {_f}")

# ---------------------------------------------------------------- 8a. B-new-1 (audit #75): typescript-reviewer coding-standards dispatch
# agents/ecc-typescript-reviewer.md:119 is a live imperative dispatch
# ("use the ... skill") to CUT coding-standards, hidden by a whole-line
# check-12 allow-list entry. Reword to the kept stack only
# (typescript-patterns + frontend-patterns / backend-patterns); the
# :119 allow-list entry is removed in verify27.py (not converted — after
# the reword the line names no CUT skill).
_f = p("agents/ecc-typescript-reviewer.md")
if exists(_f):
    sub(_f,
        "For detailed TypeScript and JavaScript patterns, use the `typescript-patterns` skill, plus `coding-standards` and `frontend-patterns` or `backend-patterns` based on the code being reviewed.",
        "For detailed TypeScript and JavaScript patterns, use the `typescript-patterns` skill, plus `frontend-patterns` or `backend-patterns` based on the code being reviewed.")
else:
    ERRORS.append(f"ecc-typescript-reviewer.md missing: {_f}")

# ---------------------------------------------------------------- 8b. M-new-1 (audit #75, ECC-origin part): re-point CUT accessibility -> kept frontend-a11y
# Eight pointer-style lines (cross-links / skills-list entries / "See
# skill") name the removed accessibility skill. Re-point each at the kept
# frontend-a11y skill; none carries a ":N" line-number suffix into the
# removed SKILL.md, so there is no suffix to drop. (The 11
# vercel-checklist citations are the staged worker's, not this script's.)
# The 8 corresponding whole-line allow-list entries are removed in
# verify27.py.
_f = p("skills/react-patterns/SKILL.md")
if exists(_f):
    sub(_f,
        "- Cross-link: [skills/accessibility/SKILL.md](../accessibility/SKILL.md) covers WCAG criteria and pattern libraries",
        "- Cross-link: [skills/frontend-a11y/SKILL.md](../frontend-a11y/SKILL.md) covers WCAG criteria and pattern libraries")
else:
    ERRORS.append(f"react-patterns SKILL.md missing: {_f}")
_f = p("skills/react-performance/SKILL.md")
if exists(_f):
    sub(_f,
        "- Skills: [react-patterns](../react-patterns/SKILL.md), [react-testing](../react-testing/SKILL.md), [frontend-patterns](../frontend-patterns/SKILL.md), [accessibility](../accessibility/SKILL.md), [nextjs-turbopack](../nextjs-turbopack/SKILL.md)",
        "- Skills: [react-patterns](../react-patterns/SKILL.md), [react-testing](../react-testing/SKILL.md), [frontend-patterns](../frontend-patterns/SKILL.md), [frontend-a11y](../frontend-a11y/SKILL.md), [nextjs-turbopack](../nextjs-turbopack/SKILL.md)")
else:
    ERRORS.append(f"react-performance SKILL.md missing: {_f}")
_f = p("skills/react-testing/SKILL.md")
if exists(_f):
    sub(_f,
        "Cross-link: [skills/accessibility/SKILL.md](../accessibility/SKILL.md) for the broader a11y testing playbook.",
        "Cross-link: [skills/frontend-a11y/SKILL.md](../frontend-a11y/SKILL.md) for the broader a11y testing playbook.")
    sub(_f,
        "- Skills: [react-patterns](../react-patterns/SKILL.md), [accessibility](../accessibility/SKILL.md), [e2e-testing](../e2e-testing/SKILL.md), [tdd-workflow](../tdd-workflow/SKILL.md)",
        "- Skills: [react-patterns](../react-patterns/SKILL.md), [frontend-a11y](../frontend-a11y/SKILL.md), [e2e-testing](../e2e-testing/SKILL.md), [tdd-workflow](../tdd-workflow/SKILL.md)")
else:
    ERRORS.append(f"react-testing SKILL.md missing: {_f}")
_f = p("agents/ecc-a11y-architect.md")
if exists(_f):
    sub(_f,
        "- See skill `accessibility` to transform raw UI requirements into platform-specific accessible code (WAI-ARIA, SwiftUI, or Jetpack Compose) based on WCAG 2.2 criteria.",
        "- See skill `frontend-a11y` to transform raw UI requirements into platform-specific accessible code (WAI-ARIA, SwiftUI, or Jetpack Compose) based on WCAG 2.2 criteria.")
else:
    ERRORS.append(f"ecc-a11y-architect.md missing: {_f}")
_f = p("agents/ecc-react-reviewer.md")
if exists(_f):
    sub(_f,
        "- Skills: `skills/react-patterns/`, `skills/react-testing/`, `skills/accessibility/`",
        "- Skills: `skills/react-patterns/`, `skills/react-testing/`, `skills/frontend-a11y/`")
else:
    ERRORS.append(f"ecc-react-reviewer.md missing: {_f}")
_f = p("commands/react-review.md")
if exists(_f):
    sub(_f,
        "- Skills: `skills/react-patterns/`, `skills/react-testing/`, `skills/accessibility/`",
        "- Skills: `skills/react-patterns/`, `skills/react-testing/`, `skills/frontend-a11y/`")
else:
    ERRORS.append(f"react-review.md missing: {_f}")
_f = p("commands/react-test.md")
if exists(_f):
    sub(_f,
        "- Skills: `skills/react-testing/`, `skills/tdd-workflow/`, `skills/accessibility/`, `skills/e2e-testing/`",
        "- Skills: `skills/react-testing/`, `skills/tdd-workflow/`, `skills/frontend-a11y/`, `skills/e2e-testing/`")
else:
    ERRORS.append(f"react-test.md missing: {_f}")

# ---------------------------------------------------------------- 8c. M-new-4 (audit #75): prune manifests/pi-core.json
# The pi-core profile claims "skills.include lists the shipped subset
# only"; after the fix #27 cut it still lists 63 CUT skills and 6
# dropped commands. Prune both include lists to the kept set (the
# description's claim is true again afterwards: every remaining entry
# is a shipped skill/command — the list is a curated subset of the 67
# kept skills, not the full set, and it never claimed to list all of
# them). learn-eval / project-init are NOT in commands.include — they
# sit in commands.exclude with reasons — so there is nothing to remove
# for them; audit #75's ":369/:382 as included commands" reading is
# wrong, and the prune asserts the include list is clean of them.
# The pruned lists are verified against the live tree: every remaining
# skill dir and command file must exist in the built tree.
_pf = p("manifests/pi-core.json")
if exists(_pf):
    with open(_pf, encoding="utf-8") as _fh:
        _pi = json.load(_fh)
    _pi_skills_before = list(_pi["skills"]["include"])
    _pi_cmds_before = list(_pi["commands"]["include"])
    _pi_cut_skills = [s for s in _pi_skills_before if s in CUT_SKILLS]
    _pi_cut_cmds = [c[:-3] for c in _pi_cmds_before
                    if c.endswith(".md") and c[:-3] in DROPPED_COMMANDS]
    if len(_pi_cut_skills) != 63:
        ERRORS.append(f"pi-core skills.include: expected 63 CUT skills, found {len(_pi_cut_skills)}")
    if len(_pi_cut_cmds) != 6:
        ERRORS.append(f"pi-core commands.include: expected 6 dropped commands, found {len(_pi_cut_cmds)}")
    if "learn-eval.md" in _pi_cmds_before or "project-init.md" in _pi_cmds_before:
        ERRORS.append("pi-core commands.include unexpectedly lists learn-eval/project-init (they belong in commands.exclude)")
    _pi["skills"]["include"] = [s for s in _pi_skills_before if s not in CUT_SKILLS]
    _pi["commands"]["include"] = [c for c in _pi_cmds_before
                                  if not (c.endswith(".md") and c[:-3] in DROPPED_COMMANDS)]
    _pi_missing_skills = [s for s in _pi["skills"]["include"]
                          if not os.path.isdir(p(f"skills/{s}"))]
    _pi_missing_cmds = [c for c in _pi["commands"]["include"]
                        if not exists(p(f"commands/{c}"))]
    if _pi_missing_skills:
        ERRORS.append(f"pi-core skills.include lists skills absent from the built tree: {_pi_missing_skills}")
    if _pi_missing_cmds:
        ERRORS.append(f"pi-core commands.include lists commands absent from the built tree: {_pi_missing_cmds}")
    with open(_pf, "w", encoding="utf-8") as _fh:
        json.dump(_pi, _fh, indent=2, ensure_ascii=True)
        _fh.write("\n")
    CHANGES.append(f"pi-core.json pruned: skills.include {len(_pi_skills_before)} -> {len(_pi['skills']['include'])} "
                   f"(removed {len(_pi_cut_skills)} CUT skills); commands.include {len(_pi_cmds_before)} -> "
                   f"{len(_pi['commands']['include'])} (removed {len(_pi_cut_cmds)} dropped commands)")
    CHANGES.append("pi-core.json pruned skills: " + ", ".join(sorted(_pi_cut_skills)))
    CHANGES.append("pi-core.json pruned commands: " + ", ".join(sorted(_pi_cut_cmds)))
    # M-new-4 decision (install-modules / install-components): LEFT
    # UNPRUNED — recorded here so the generated patch log carries it.
    # Both files enumerate the full upstream ECC install catalog
    # (install-modules.json: exactly the 166 pre-cut skill paths, 100
    # CUT + 66 kept; install-components.json: 5 CUT skill components),
    # not the plugin's shipped subset. The install machinery derives
    # the live single-skill surface from the actual skills/ directory
    # at load time (addSyntheticSkillComponents, install-manifests.js)
    # and silently skips missing source paths at plan time
    # (materializeScaffoldOperation returns [] for a nonexistent
    # source, scripts/lib/install/plan.js), so a stale CUT path
    # installs nothing and fails nothing. A paths-only prune would
    # leave misleading components (skill:coding-standards ->
    # framework-language, which would no longer contain it) and an
    # empty skill-unified-memory module that install-profiles.json
    # still references; a coherent prune would change installer
    # behaviour with no verifier coverage in this fix, and SPEC §1(b)
    # never tasked fix27 with it. Stale install-time metadata, same
    # class as audit #74 M3/M5 — not a live dispatch.
    CHANGES.append("M-new-4 decision: manifests/install-modules.json (100 CUT skill paths of 166) and "
                   "manifests/install-components.json (5 CUT skill components: skill:unified-memory, "
                   "skill:continuous-learning, skill:windows-desktop-e2e, skill:coding-standards, "
                   "skill:vue-patterns, plus a continuous-learning-v2 mention in the continuous-learning "
                   "component description) LEFT UNPRUNED as upstream-catalog artifacts — see the round-3 log")
else:
    ERRORS.append(f"pi-core.json missing: {_pf}")

# ---------------------------------------------------------------- stale-count scan: no old counts may survive
# Round 2 also flags the round-1 counts (66 skills / 60 commands) as
# stale. The call map is excluded: it is generator-owned output,
# regenerated by the fix25 generator, whose own EXPECTED counts guard it.
_callmap_rel = os.path.join("skills", "orchestrate", "references", "call-map.md")
_stale = []
for _root, _dirs, _files in os.walk(BASE):
    _dirs[:] = [d for d in _dirs if d != "node_modules"]
    for _fn in _files:
        _fp = os.path.join(_root, _fn)
        if os.path.relpath(_fp, BASE) == _callmap_rel:
            continue
        try:
            _t = open(_fp, encoding="utf-8", errors="strict").read()
        except (UnicodeDecodeError, ValueError, OSError):
            continue
        for _tok in ("166 skills", "72 agents", "87 commands",
                     "66 skills", "60 commands"):
            if _tok in _t:
                _stale.append(f"{os.path.relpath(_fp, BASE)}: {_tok!r}")
if _stale:
    ERRORS.append("stale counts remain in the built tree: " + "; ".join(_stale))

# ---------------------------------------------------------------- OWED (recorded, not patched blindly)
OWED = [
    "OWED-1 RESOLVED (round 1): the call map was regenerated from the reduced tree with the fix25 generator (SPEC §1(c)); it lists the reduced set (67 skills / 45 agents / 123 rules / 55 commands after round 2). Do NOT hand-edit its rows.",
    "OWED-2 RESOLVED (coordinator adjudication): gan-style-harness is KEPT, so no /gan-build re-route is needed. The inventory's duplication claim was contradicted by dispatch evidence — orch-build-mvp/SKILL.md (:39, :62, :95) and orch-pipeline/SKILL.md (:37, :97) drive /gan-build as the MVP inner loop; the GAN harness IS the loop, not a duplicate of it.",
    "OWED-3 RESOLVED: the deferred check lists are patched in this script (§6g) to the three kept checks (verification-loop, production-audit, delivery-gate) in orchestrate (:8, :103, :370) and orch-build-mvp (:86). hackathon-mode.mdc §3 carries the same list in staged sources — the staged-edits worker owns that file.",
    "OWED-4 RESOLVED (round 2): the continuous-learning-v2 commands are all DROPPED by this script — evolve, instinct-export, instinct-import, instinct-status (round 1) plus projects, promote, prune (round 2, audit #74). learn is KEPT (a user-invoked session-review tool, not a CLv2 command — audit #74 adjudication). learn-eval is DROPPED in round 2 (duplicates /learn; its quality-gate rubric source is removed). project-init is DROPPED in round 2 (ECC onboarding, not a build step). The skill-create --instincts flag, 'Optionally Creates Instincts' step, Step 4 CLv2 section and Related Commands instinct lines are removed in round 2 (B6); the ecc-guide /project-init pointer and the epic-sync /projects alias go with them.",
    "OWED-5 RESOLVED (round 2, B11): the ecc-agent-evaluator agent is now self-contained — the 5-axis rubric (Accuracy, Completeness, Clarity, Actionability, Conciseness) and the full report format are defined in the agent file itself (:54-69, :71-110); all references to the removed agent-self-evaluation skill/script are removed (:3, :24, :54, :69, :110). The rubric source is now this file itself.",
    "OWED-6 RESOLVED: feature-expansion's CUT dispatches were re-routed in round 1 (REROUTE_F27 at :49, :100, :188, :190, :192-193, :204; audit #74 check 12) — legacy drift handled inside the design package, the product-lens why-check via hackathon-scope, and the remaining mentions are 'was cut' / 'NOT invoked' notes.",
    "OWED-7 RESOLVED (round 2, M3): the trigger-file notes string now lists only the three kept deferred checks (verification-loop, production-audit, delivery-gate) (DEFER3_F27).",
    "OWED-8 RESOLVED (coordinator adjudication): the 13 held agents are removed by this script (conversation-analyzer, cpp x2, dart, go x2, java x2, php, ruby, swift x2, marketing-agent) — their only language skills are CUT (or absent) and their only referrers are dropped commands or the call map. KEPT: ecc-a11y-architect (serves kept frontend-a11y). Agents are now 72 - 27 = 45.",
    "OWED-9 RESOLVED (round 2, M4): delivery-gate's agent-self-evaluation prose (:3, :13, :15, :111) is reworded to past tense / the 'shipped' claims removed; the reasoning-quality-gate entry now points at the kept `ecc-agent-evaluator` agent (B11). Only :97 was reworded in round 1 per SPEC §1(b).",
    "OWED-10 RESOLVED (round 2, B15): skill-create.md:3 and skill-health.md:3 descriptions are reworded to the kept discovery/audit path (grep-and-read over the plugin's own skill list / verify scripts). The commands themselves stay (SPEC §1(b)) — the 'advisory' label in the round-1 record was wrong: these were imperative routing lines in descriptions, and they are now fixed.",
    "OWED-11 rules/*.mdc references to CUT skills (e.g. angular/dart/kotlin/rust/nuxt/perl rule families naming CUT skills, react-patterns naming accessibility). Rules are NOT cut in this fix (SPEC §1(d)); left alone — carried to the rules-debloat follow-up. Pointer-style only, not dispatches (audit #74 M7).",
    "OWED-12 LANDED (staged worker, round 2): rules/hackathon-mode.mdc is a staged source; the staged-edits worker owns it in this round — the §5/§6 CUT routings (B12: brainstorming, codebase-memory, dart-flutter-patterns) and the §7 precondition contradiction vs orchestrate:57 (B14) are that worker's patches. This build-time script does not touch staged sources. (Note: gan-style-harness is KEPT, so its mention there is no longer a dangling reference.)",
    "OWED-13 CORRECTED (round 2, updated round 3): the round-1 blanket claim ('All are prose-history or single-mention references') was wrong. The live dispatches — inherit-legacy-style in the orch-* files + ui-ux-pro-max (B1), santa-method in council (B8), mcp-server-patterns + skill-scout in integration (B9), intent-driven-development in ai-feature-spec (B10), agent-introspection-debugging in systematic-debugging (B13) — are re-routed in this round (§7). The remaining CUT-name mentions are prose-history, per the post-fix census (fix27/scratch/f27r2-census.txt, updated in round 3: 82 whole-line allow-list entries + 1 name-scoped line = 83 allow-listed lines, counted from verify27.py's ALLOW_LIST/ALLOW_NAMES literals after the round-3 removals (102 whole-line + 1 name-scoped = 103 before round 3; -1 typescript-reviewer:119, -8 accessibility pointers, -11 vercel-checklist citations); the round-2 census recorded 101 lines at census time, +1 for orchestrate:136): skills/delivery-gate/SKILL.md:13, :15, :111 (former/cut notes, M4); skills/feature-expansion/SKILL.md:3 (generic verb), :49, :100, :188, :190, :192, :193, :204 (was-cut / NOT-invoked REROUTE notes), :211 (upstream attribution); skills/integration/SKILL.md:21, :46, :60, :122 (was-cut REROUTE notes, B9); skills/orchestrate/SKILL.md:136 (prose-history: 'ecc-recipes was cut' REROUTE note, B3); skills/design-taste-frontend/assets/icons/demo.html:74, index.json:5569 (icon data); skills/polish-pass/reference/vercel-checklist.md:93, :105, :108, :111, :115, :118, :121, :124, :127, :139, :146, :171 (citations re-pointed to frontend-a11y in round 3 by the staged worker — :93 was a 12th bare-word hit the audit had not listed; their 11 allow-list entries removed once the re-point landed); skills/ui-ux-pro-max/data/phosphor-icons-upstream.json:8306, :22481, :22557, :28089, :28112, :32160, :32184, scripts/core.py:232, :233, :240, :264, :594, scripts/design_system.py:622, :805, scripts/reasoning_contract.py:41, scripts/tests/fixtures/relevance-cases.json:27, :29, :36, :39, :105 (icon-name / search-keyword / test-fixture data); agents/ecc-spec-miner.md:3, :40, :201 (negative: does not require); commands/learn.md:2 (negative: distinguishes from CLv2); rules/*.mdc 'See skill' pointers (OWED-11/M7): golang-coding-style:31, golang-patterns:44, golang-testing:30, kotlin-coding-style:39, kotlin-patterns:50, kotlin-testing:38, angular-patterns:249, angular-testing:164, cpp-coding-style:44, cpp-patterns:51, cpp-security:51, cpp-testing:44, dart-patterns:260, :261, java-coding-style:113, :114, java-patterns:145, :146, :147, java-testing:114, :115, :131, :132, :133, nuxt-coding-style:45, nuxt-hooks:37, nuxt-patterns:51, nuxt-security:46, nuxt-testing:47, perl-coding-style:46, perl-patterns:76, perl-testing:54, react-patterns:194, rust-coding-style:151, rust-patterns:168, rust-security:140, rust-testing:154; rules/hackathon-mode.mdc:37, :38 (negative) and :46 product-lens / intent-driven-development (negative: do not scope hackathons). Generic bare-word noise (accessibility 131, projects 156, promote 4, brainstorming 3, evolve 1, prune 1 lines) is ordinary prose, not skill references. (Round 3, audit #76 M-new-7: the census counted 132 including vercel-checklist.md:93, a bare-word routing reference the staged worker also re-pointed to frontend-a11y, so the live count is 131.) Round 3 (audit #75 M-new-1/B-new-1) re-pointed the 8 accessibility pointers (skills/react-patterns/SKILL.md:254, skills/react-performance/SKILL.md:566, skills/react-testing/SKILL.md:247, :359, agents/ecc-a11y-architect.md:148, agents/ecc-react-reviewer.md:161, commands/react-review.md:169, commands/react-test.md:263) to frontend-a11y and reworded agents/ecc-typescript-reviewer.md:119 to drop coding-standards; their 9 allow-list entries are removed in round 3. The 9 staged-owned live dispatches listed in the round-2 record — skills/orchestrate/SKILL.md:3 (B4), :65 (B1), :136 (B3), :138 (B1), skills/orchestrate/references/dispatch-prompt.md:24 (B1), rules/hackathon-mode.mdc:46 brainstorming (B12), :48 (B4), :53 (B12), :55 (B12) — LANDED in round 2 (verified in the built tree, audit #75 B1/B3/B4/B12/B14); none of the 9 is outstanding.",
]

# ---------------------------------------------------------------- main / run log
_log_lines = ["# fix27 run log", "",
              f"## Errors ({len(ERRORS)})"]
_log_lines += [f"- {e}" for e in ERRORS] or ["- none"]
_log_lines += ["", f"## Changes ({len(CHANGES)})"]
_log_lines += [f"- {c}" for c in CHANGES] or ["- none"]
_log_lines += ["", f"## Command decisions ({len(DECISIONS)})"]
_log_lines += [f"- {d}" for d in DECISIONS] or ["- none"]
_log_lines += ["", f"## OWED ({len(OWED)})"]
_log_lines += [f"- {o}" for o in OWED] or ["- none"]
_log_dir = os.path.join(os.path.dirname(BASE.rstrip("/")), "fix27")
os.makedirs(_log_dir, exist_ok=True)
with open(os.path.join(_log_dir, "fix27-patch-log.md"), "w", encoding="utf-8") as _fh:
    _fh.write("\n".join(_log_lines) + "\n")
print(f"fix27: {len(CHANGES)} change(s)")
for c in CHANGES:
    print(f"  - {c}")
print(f"fix27: {len(OWED)} OWED item(s) recorded in the patch log")
if ERRORS:
    print(f"fix27: {len(ERRORS)} ERROR(S)", file=sys.stderr)
    for e in ERRORS:
        print(f"  ! {e}", file=sys.stderr)
    sys.exit(1)
print("fix27: OK")
