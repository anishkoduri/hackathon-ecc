#!/usr/bin/env python3
"""Fix #28 — cut all remaining bloat that provably does not affect the plugin.

Run by build.sh as a patch step (after fix27, before STEP 5 Counts):
    python3 "$PLUGIN_ROOT/fix28/fix28.py" "$PLUGIN_DIR"

Operates on the BUILT tree only. Staged-source halves are edited directly
in new-skills/ / round2-skills/ / rewritten-skills/ / new-rules/ and flow
through the STEP 2 copy. Every text patch asserts its anchor occurs
EXACTLY once and fails loudly on mismatch; the script exits non-zero on
any error so the build fails rather than shipping a half-patched tree.
Removals are idempotent-tolerant: a dir/file already absent is recorded
as already-absent and does NOT fail the build (the STEP 2 assembly may
vary); text-patch anchor misses DO fail the build.

SPEC fix28/SPEC.md:
  §1 Rules 123 -> 48 (75 CUT: the 68 in analysis/rule-inventory.md §7
     plus the 7 NEEDS-DECISION files in §9, cut on the misfire argument
     NDMISFIRE_F28 — their only effect on kept-stack files is injecting
     wrong-framework guidance; see SPEC §1(b)). CUTRULES_F28.
  §2 Install manifests 16 -> 14 modules, 184 -> 84 paths, 57 -> 55
     components (analysis/install-manifests.md §6). MANIFEST28_F28.
  §3 Dead scripts: 135 files (~1.24 MiB) + the mcp.json
     codebase-memory-mcp entry (analysis/dead-weight.md §1).
     DEADSCRIPTS_F28.
  §4 Fixes: F1 sessions.md cost-tracker clause dropped; F2
     evaluate-session.js config load + orphan log lines removed
     (EVALSESS_F28); F4 README codebase-memory phrase removed; README
     count lines 67/45/48/55 (README48_F28); react-patterns.mdc:194
     accessibility -> frontend-a11y (REACTA11Y_F28).
  §5 NOT cut: orchestration-session.js + tmux-worktree-orchestrator.js
     (runtime-dead but the whole orchestration module; ORCHKEEP_F28),
     validate-skills.js, the 22 misleading components (kept with
     description corrections), motionsites module membership (parent call).

Do NOT delete from build.sh STEP 2: the STEP 3 patches assume the full
tree. Removal happens here, after fix27, before STEP 5 Counts.
Never re-run fix11/fix11-stage.py. Never edit the built tree directly
outside this script; never edit build.sh or any staged skill here.

Anchor tokens (_F28): CUTRULES_F28, MANIFEST28_F28, DEADSCRIPTS_F28,
EVALSESS_F28, README48_F28, REACTA11Y_F28, NDMISFIRE_F28, ORCHKEEP_F28.
CUTRULES_F28, MANIFEST28_F28, DEADSCRIPTS_F28 also appear in the built
README.md fix #28 note line (§5); the other five live in this script and
the patch log.
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
        return
    write(f, text.replace(old, new, count))
    CHANGES.append(f"{os.path.relpath(f, BASE)}: patched anchor :: {old[:80]!r}")


def remove_file(rel):
    """Idempotent-tolerant file removal."""
    f = p(rel)
    if os.path.isfile(f):
        os.remove(f)
        return True
    if os.path.lexists(f):
        ERRORS.append(f"remove_file: {rel} exists but is not a file")
        return False
    return False


def remove_dir(rel):
    """Idempotent-tolerant dir removal."""
    d = p(rel)
    if os.path.isdir(d):
        shutil.rmtree(d)
        return True
    if os.path.lexists(d):
        ERRORS.append(f"remove_dir: {rel} exists but is not a dir")
        return False
    return False


CUT_RULES = ['angular-coding-style.mdc', 'angular-hooks.mdc', 'angular-patterns.mdc', 'angular-security.mdc', 'angular-testing.mdc', 'cpp-coding-style.mdc', 'cpp-hooks.mdc', 'cpp-patterns.mdc', 'cpp-security.mdc', 'cpp-testing.mdc', 'csharp-coding-style.mdc', 'csharp-hooks.mdc', 'csharp-patterns.mdc', 'csharp-security.mdc', 'csharp-testing.mdc', 'dart-coding-style.mdc', 'dart-hooks.mdc', 'dart-patterns.mdc', 'dart-security.mdc', 'dart-testing.mdc', 'fsharp-coding-style.mdc', 'fsharp-hooks.mdc', 'fsharp-patterns.mdc', 'fsharp-security.mdc', 'fsharp-testing.mdc', 'golang-coding-style.mdc', 'golang-hooks.mdc', 'golang-patterns.mdc', 'golang-security.mdc', 'golang-testing.mdc', 'java-coding-style.mdc', 'java-hooks.mdc', 'java-patterns.mdc', 'java-security.mdc', 'java-testing.mdc', 'kotlin-coding-style.mdc', 'kotlin-hooks.mdc', 'kotlin-patterns.mdc', 'kotlin-security.mdc', 'kotlin-testing.mdc', 'nuxt-coding-style.mdc', 'nuxt-hooks.mdc', 'nuxt-patterns.mdc', 'nuxt-security.mdc', 'nuxt-testing.mdc', 'perl-coding-style.mdc', 'perl-hooks.mdc', 'perl-patterns.mdc', 'perl-security.mdc', 'perl-testing.mdc', 'php-coding-style.mdc', 'php-hooks.mdc', 'php-patterns.mdc', 'php-security.mdc', 'php-testing.mdc', 'ruby-coding-style.mdc', 'ruby-hooks.mdc', 'ruby-patterns.mdc', 'ruby-security.mdc', 'ruby-testing.mdc', 'rust-coding-style.mdc', 'rust-hooks.mdc', 'rust-patterns.mdc', 'rust-security.mdc', 'rust-testing.mdc', 'swift-coding-style.mdc', 'swift-hooks.mdc', 'swift-patterns.mdc', 'swift-security.mdc', 'swift-testing.mdc', 'vue-coding-style.mdc', 'vue-hooks.mdc', 'vue-patterns.mdc', 'vue-security.mdc', 'vue-testing.mdc']

KEPT_RULES = ['arkts-coding-style.mdc', 'arkts-hooks.mdc', 'arkts-patterns.mdc', 'arkts-security.mdc', 'arkts-testing.mdc', 'common-agents.mdc', 'common-code-review.mdc', 'common-coding-style.mdc', 'common-development-workflow.mdc', 'common-git-workflow.mdc', 'common-hooks.mdc', 'common-patterns.mdc', 'common-performance.mdc', 'common-security.mdc', 'common-testing.mdc', 'hackathon-mode.mdc', 'ponytail.mdc', 'python-coding-style.mdc', 'python-fastapi.mdc', 'python-hooks.mdc', 'python-patterns.mdc', 'python-security.mdc', 'python-testing.mdc', 'react-coding-style.mdc', 'react-hooks.mdc', 'react-native-accessibility.mdc', 'react-native-coding-style.mdc', 'react-native-hooks.mdc', 'react-native-patterns.mdc', 'react-native-performance.mdc', 'react-native-production-readiness.mdc', 'react-native-security.mdc', 'react-native-testing.mdc', 'react-patterns.mdc', 'react-security.mdc', 'react-testing.mdc', 'typescript-coding-style.mdc', 'typescript-hooks.mdc', 'typescript-patterns.mdc', 'typescript-security.mdc', 'typescript-testing.mdc', 'web-coding-style.mdc', 'web-design-quality.mdc', 'web-hooks.mdc', 'web-patterns.mdc', 'web-performance.mdc', 'web-security.mdc', 'web-testing.mdc']

DEAD_SCRIPTS = ['scripts/hooks/auto-tmux-dev.js', 'scripts/hooks/bash-hook-dispatcher.js', 'scripts/hooks/check-hook-enabled.js', 'scripts/hooks/config-protection.js', 'scripts/hooks/context-prompt-suggestions.js', 'scripts/hooks/context-routing-index.js', 'scripts/hooks/desktop-notify.js', 'scripts/hooks/doc-file-warning.js', 'scripts/hooks/ecc-context-monitor.js', 'scripts/hooks/ecc-metrics-bridge.js', 'scripts/hooks/ecc-statusline.js', 'scripts/hooks/gateguard-fact-force.js', 'scripts/hooks/gateguard-heredoc.js', 'scripts/hooks/governance-capture.js', 'scripts/hooks/hook-input-limits.js', 'scripts/hooks/hook-input.js', 'scripts/hooks/hookify-frontmatter.js', 'scripts/hooks/hookify-runtime.js', 'scripts/hooks/insaits-security-monitor.py', 'scripts/hooks/insaits-security-wrapper.js', 'scripts/hooks/lifecycle-hook-bootstrap.js', 'scripts/hooks/mcp-health-check.js', 'scripts/hooks/observe-runner.js', 'scripts/hooks/plan-canvas-pending.js', 'scripts/hooks/plan-canvas-sessions.js', 'scripts/hooks/plugin-hook-bootstrap.js', 'scripts/hooks/post-bash-build-complete.js', 'scripts/hooks/post-bash-command-log.js', 'scripts/hooks/post-bash-dispatcher.js', 'scripts/hooks/post-bash-pr-created.js', 'scripts/hooks/post-edit-typecheck.js', 'scripts/hooks/posttooluse-dispatcher.js', 'scripts/hooks/pre-bash-dispatcher.js', 'scripts/hooks/pre-bash-git-push-reminder.js', 'scripts/hooks/pre-bash-tmux-reminder.js', 'scripts/hooks/pre-write-doc-warn.js', 'scripts/hooks/pretooluse-visible-output.js', 'scripts/hooks/run-with-flags-shell.sh', 'scripts/hooks/run-with-flags.js', 'scripts/hooks/session-activity-tracker.js', 'scripts/hooks/session-start-bootstrap.js', 'scripts/hooks/skill-run-tracker.js', 'scripts/lib/agent-compress.js', 'scripts/lib/agent-emit-pi.js', 'scripts/lib/agent-ir.js', 'scripts/lib/agent-proximity/distance.js', 'scripts/lib/agent-proximity/graph.js', 'scripts/lib/agent-proximity/index.js', 'scripts/lib/agent-proximity/projection.js', 'scripts/lib/agent-proximity/shadow-trail.js', 'scripts/lib/agent-tool-map.js', 'scripts/lib/agent-tools.js', 'scripts/lib/compute-sponsor.js', 'scripts/lib/context-carriers.js', 'scripts/lib/context-pack-registry.js', 'scripts/lib/context-profile-commands.js', 'scripts/lib/context-profile-store-fs.js', 'scripts/lib/context-profile-store.js', 'scripts/lib/context-profile-support.js', 'scripts/lib/context-profiles.js', 'scripts/lib/context-retrieval.js', 'scripts/lib/context-routing-index.js', 'scripts/lib/context-selection.js', 'scripts/lib/control-pane/actions.js', 'scripts/lib/control-pane/control-plane-view-ui.js', 'scripts/lib/control-pane/control-plane-view.js', 'scripts/lib/control-pane/message-sink.js', 'scripts/lib/control-pane/proximity-viz.js', 'scripts/lib/control-pane/proximity.js', 'scripts/lib/control-pane/server.js', 'scripts/lib/control-pane/state.js', 'scripts/lib/control-pane/ui.js', 'scripts/lib/control-pane/work-item-mutations.js', 'scripts/lib/control-pane/work-item-runner.js', 'scripts/lib/control-pane/work-item-worker.js', 'scripts/lib/coordination-inventory.js', 'scripts/lib/ecc_dashboard_runtime.py', 'scripts/lib/eval-harness/canonical.js', 'scripts/lib/eval-harness/capsule.js', 'scripts/lib/eval-harness/effect-fence.js', 'scripts/lib/eval-harness/envelope.js', 'scripts/lib/eval-harness/gate.js', 'scripts/lib/eval-harness/index.js', 'scripts/lib/eval-harness/receipt.js', 'scripts/lib/eval-harness/replay.js', 'scripts/lib/eval-harness/retrospective.js', 'scripts/lib/feedback-links.js', 'scripts/lib/gateguard-change-profile.js', 'scripts/lib/gateguard-code-lexer.js', 'scripts/lib/gateguard-file-context.js', 'scripts/lib/gateguard-metrics.js', 'scripts/lib/gateguard-readonly-shell.js', 'scripts/lib/gateguard-search-evidence.js', 'scripts/lib/gateguard-search-filters.js', 'scripts/lib/gateguard-state.js', 'scripts/lib/gateguard-target-class.js', 'scripts/lib/gateguard-turn-scan.js', 'scripts/lib/github-discussions.js', 'scripts/lib/github-origin.js', 'scripts/lib/harness-adapter-compliance.js', 'scripts/lib/harness-capabilities.js', 'scripts/lib/inspection.js', 'scripts/lib/install-state-store-sync.js', 'scripts/lib/install/config.js', 'scripts/lib/install/plugin-namespace.js', 'scripts/lib/ito-environment.js', 'scripts/lib/loopback-guard.js', 'scripts/lib/memory-vault-format.js', 'scripts/lib/memory-vault.js', 'scripts/lib/missing-dependency.js', 'scripts/lib/nasiko-release.js', 'scripts/lib/opencode-paths.js', 'scripts/lib/plan-canvas/markdown.js', 'scripts/lib/plan-canvas/sdk.js', 'scripts/lib/plan-canvas/server.js', 'scripts/lib/plan-canvas/sessions.js', 'scripts/lib/plan-canvas/ui.js', 'scripts/lib/platform-launch.js', 'scripts/lib/powershell-destructive-command.js', 'scripts/lib/session-adapters/canonical-session.js', 'scripts/lib/session-adapters/dmux-tmux.js', 'scripts/lib/session-adapters/registry.js', 'scripts/lib/session-bridge.js', 'scripts/lib/session-cost-snapshot.js', 'scripts/lib/skill-evolution/index.js', 'scripts/lib/skill-improvement/amendify.js', 'scripts/lib/skill-improvement/evaluate.js', 'scripts/lib/skill-improvement/health.js', 'scripts/lib/skill-improvement/observations.js', 'scripts/lib/statusline-render.js', 'scripts/lib/terminal-spinner.js', 'scripts/lib/terminal-welcome.js', 'scripts/lib/windows-bash.js', 'scripts/lib/worktree-lifecycle/git.js', 'scripts/lib/worktree-lifecycle/lifecycle.js']

# Per-module dead paths in install-modules.json (verified against disk:
# each path does not exist in the fix #27 built tree).
MANIFEST_DEAD = {'framework-language': ['skills/android-clean-architecture', 'skills/angular-developer', 'skills/bengali-nlp', 'skills/coding-standards', 'skills/compose-multiplatform-patterns', 'skills/csharp-testing', 'skills/fsharp-testing', 'skills/cpp-coding-standards', 'skills/cpp-testing', 'skills/dart-flutter-patterns', 'skills/django-patterns', 'skills/django-tdd', 'skills/django-verification', 'skills/dotnet-patterns', 'skills/frontend-design-direction', 'skills/i18n-sync', 'skills/golang-patterns', 'skills/golang-testing', 'skills/java-coding-standards', 'skills/kotlin-coroutines-flows', 'skills/kotlin-exposed-patterns', 'skills/kotlin-ktor-patterns', 'skills/kotlin-patterns', 'skills/kotlin-testing', 'skills/laravel-plugin-discovery', 'skills/laravel-patterns', 'skills/laravel-tdd', 'skills/laravel-verification', 'skills/mcp-server-patterns', 'skills/nestjs-patterns', 'skills/perl-patterns', 'skills/perl-testing', 'skills/quarkus-patterns', 'skills/quarkus-tdd', 'skills/quarkus-verification', 'skills/rails-patterns', 'skills/rust-patterns', 'skills/rust-testing', 'skills/springboot-patterns', 'skills/springboot-tdd', 'skills/springboot-verification', 'skills/ui-to-vue', 'skills/vue-patterns', 'skills/accessibility', 'skills/bun-runtime', 'skills/django-celery', 'skills/flutter-dart-code-review', 'skills/generating-python-installer', 'skills/hexagonal-architecture', 'skills/nuxt4-patterns', 'skills/tinystruct-patterns'], 'database': ['skills/clickhouse-io', 'skills/database-migrations', 'skills/jpa-patterns', 'skills/mybatis-patterns', 'skills/mysql-patterns', 'skills/prisma-patterns', 'skills/redis-patterns'], 'workflow-quality': ['skills/agent-sort', 'skills/agent-introspection-debugging', 'skills/ai-regression-testing', 'skills/code-tour', 'skills/continuous-learning', 'skills/continuous-learning-v2', 'skills/dev-team', 'skills/hookify-rules', 'skills/iterative-retrieval', 'skills/plankton-code-quality', 'skills/skill-scout', 'skills/skill-stocktake', 'skills/story-lifecycle', 'skills/windows-desktop-e2e', 'skills/agent-self-evaluation', 'skills/architecture-decision-records', 'skills/brownfield-retrospective', 'skills/codebase-onboarding', 'skills/codehealth-mcp', 'skills/ecc-recipes', 'skills/inherit-legacy-style', 'skills/intent-driven-development', 'skills/living-docs-governance', 'skills/loop-design-check', 'skills/product-lens', 'skills/repo-scan', 'skills/rules-distill', 'skills/santa-method', 'skills/conventional-commit-review'], 'security': ['skills/mcp-dependency-review', 'skills/security-scan'], 'agentic-patterns': ['skills/opensource-pipeline'], 'hackathon': ['skills/agents-md-generator', 'skills/brainstorming', 'skills/codebase-memory', 'skills/dispatching-parallel-agents']}

# Description replacements for kept install components (report §6b item 4):
# component id -> (exact old description, new description).
COMPONENT_DESC_FIXES = {
    "skill:continuous-learning": (
        "Legacy v1 Stop-hook session pattern extraction skill; prefer continuous-learning-v2 for new installs.",
        "Legacy v1 Stop-hook session pattern extraction skill. (Removed in fix #27; resolves to the shared workflow-quality module.)",
    ),
    "lang:python": (
        "Python and Django-oriented engineering guidance. Currently resolves through the shared framework-language module.",
        "Python engineering guidance. Currently resolves through the shared framework-language module.",
    ),
    "skill:windows-desktop-e2e": (
        "E2E testing for Windows native desktop apps with pywinauto and Windows UI Automation.",
        "E2E testing for Windows native desktop apps with pywinauto and Windows UI Automation. (Removed in fix #27; resolves to the shared workflow-quality module.)",
    ),
    "skill:coding-standards": (
        "Language-agnostic coding standards and best practices.",
        "Language-agnostic coding standards and best practices. (Removed in fix #27; resolves to the shared framework-language module.)",
    ),
    "skill:vue-patterns": (
        "Vue.js 3 Composition API, reactivity, Pinia, Vue Router, and Nuxt SSR patterns.",
        "Vue.js 3 Composition API, reactivity, Pinia, Vue Router, and Nuxt SSR patterns. (Removed in fix #27; resolves to the shared framework-language module.)",
    ),
}

# The 18 dead language/framework components: append the same note to each
# exact description (old descriptions verified against the fix #27 tree).
LANG_FRAMEWORK_NOTE = " (Guidance for this language/framework was removed in fix #27; resolves to the shared framework-language module.)"
LANG_FRAMEWORK_DESCS = {
    "lang:go": "Go-focused coding and testing guidance. Currently resolves through the shared framework-language module.",
    "lang:java": "Java and Spring application guidance. Currently resolves through the shared framework-language module.",
    "lang:cpp": "C++ coding standards and testing guidance. Currently resolves through the shared framework-language module.",
    "lang:c": "C engineering guidance using the shared C/C++ standards and testing stack. Currently resolves through the shared framework-language module.",
    "lang:kotlin": "Kotlin, Ktor, Exposed, Coroutines, and Compose Multiplatform guidance. Currently resolves through the shared framework-language module.",
    "lang:arkts": "HarmonyOS, ArkTS, and ArkUI development guidance including V2 state management, Navigation routing, and HarmonyOS API best practices.",
    "lang:perl": "Modern Perl patterns, testing, and security guidance. Currently resolves through framework-language and security modules.",
    "lang:ruby": "Ruby and Rails coding, testing, and security guidance. Resolves through framework-language and security modules.",
    "lang:rust": "Rust patterns and testing guidance. Currently resolves through the shared framework-language module.",
    "lang:csharp": "C# coding standards and patterns guidance. Currently resolves through the shared framework-language module.",
    "lang:fsharp": "F# functional patterns and testing guidance. Currently resolves through the shared framework-language module.",
    "framework:angular": "Angular-focused engineering guidance and rules. Currently resolves through the shared framework-language module.",
    "framework:vue": "Vue.js, Nuxt, Pinia, and Vue Router engineering guidance. Currently resolves through the shared framework-language module.",
    "framework:django": "Django-focused engineering guidance. Currently resolves through the shared framework-language module.",
    "framework:springboot": "Spring Boot-focused engineering guidance. Currently resolves through the shared framework-language module.",
    "framework:quarkus": "Quarkus-focused engineering guidance for REST, Panache, security, testing, and verification.",
    "framework:rails": "Rails 8 application guidance for MVC, Hotwire, Solid Queue/Cache/Cable, authentication, testing, and security.",
    "framework:laravel": "Laravel patterns, TDD, verification, and security guidance. Resolves through framework-language and security modules.",
}


def _load_json(rel):
    with open(p(rel), encoding="utf-8") as fh:
        return json.load(fh)


def _dump_json(rel, data):
    with open(p(rel), "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


# ---------------------------------------------------------------- 1. Rules 123 -> 48 (CUTRULES_F28, NDMISFIRE_F28)
_rules_before = sorted(fn for fn in os.listdir(p("rules")) if fn.endswith(".mdc"))
if len(_rules_before) != 123:
    ERRORS.append(f"rules: expected 123 before cut, found {len(_rules_before)}")
_removed_rules = []
_already_absent_rules = []
for _r in CUT_RULES:
    if remove_file(os.path.join("rules", _r)):
        _removed_rules.append(_r)
    else:
        _already_absent_rules.append(_r)
if len(_removed_rules) != 75:
    ERRORS.append(f"rules: expected 75 removed, removed {len(_removed_rules)}")
if _already_absent_rules:
    CHANGES.append(f"rules already absent (STEP 2 variance): {', '.join(sorted(_already_absent_rules))}")
_rules_after = sorted(fn for fn in os.listdir(p("rules")) if fn.endswith(".mdc"))
if _rules_after != sorted(KEPT_RULES):
    ERRORS.append(f"rules: after cut, set mismatch — extra={sorted(set(_rules_after) - set(KEPT_RULES))} missing={sorted(set(KEPT_RULES) - set(_rules_after))}")
CHANGES.append(f"rules cut: 123 -> {len(_rules_after)} (removed {len(_removed_rules)}: 68 clean CUT + 7 NEEDS-DECISION on the NDMISFIRE_F28 misfire argument)")

# ---------------------------------------------------------------- 2. Install manifests (MANIFEST28_F28)
# 2a. install-modules.json: 16 -> 14 modules, 184 -> 84 paths.
_mf = p("manifests/install-modules.json")
if exists(_mf):
    _mods = _load_json("manifests/install-modules.json")
    _mlist = _mods["modules"]
    if len(_mlist) != 16:
        ERRORS.append(f"install-modules: expected 16 modules before, found {len(_mlist)}")
    _paths_before = sum(len(m.get("paths", [])) for m in _mlist)
    if _paths_before != 184:
        ERRORS.append(f"install-modules: expected 184 paths before, found {_paths_before}")
    _by_id = {m["id"]: m for m in _mlist}
    for _mid, _dead in MANIFEST_DEAD.items():
        _m = _by_id.get(_mid)
        if _m is None:
            ERRORS.append(f"install-modules: module {_mid} missing")
            continue
        _before = list(_m.get("paths", []))
        for _dp in _dead:
            if _dp not in _before:
                ERRORS.append(f"install-modules: {_mid} does not list dead path {_dp}")
        _m["paths"] = [x for x in _before if x not in set(_dead)]
    # Delete the two empty modules whole.
    for _gone in ("skill-unified-memory", "business-content"):
        if _gone not in _by_id:
            ERRORS.append(f"install-modules: module {_gone} missing, cannot delete")
    _mods["modules"] = [m for m in _mlist if m["id"] not in ("skill-unified-memory", "business-content")]
    # workflow-quality: drop the dead dependency + fix the description.
    _wq = next((m for m in _mods["modules"] if m["id"] == "workflow-quality"), None)
    if _wq is None:
        ERRORS.append("install-modules: workflow-quality missing after prune")
    else:
        if _wq.get("dependencies") != ["skill-unified-memory"]:
            ERRORS.append(f"install-modules: workflow-quality dependencies unexpected: {_wq.get('dependencies')!r}")
        else:
            # Empty the list, do NOT delete the key: install-manifests.js
            # resolveModule iterates module.dependencies unconditionally,
            # so a missing key crashes every profile resolve (verify28
            # run 1 caught this: TypeError, module.dependencies is not
            # iterable). An empty list resolves cleanly.
            _wq["dependencies"] = []
        _wq_old = "Evaluation, TDD, verification, compaction, learning, and cross-harness memory skills, including the legacy continuous-learning v1 path. The unified-memory workflow requires the separately installed ecc-universal CLI runtime."
        if _wq.get("description") != _wq_old:
            ERRORS.append("install-modules: workflow-quality description anchor mismatch")
        else:
            _wq["description"] = "Evaluation, TDD, verification, compaction, learning, and memory skills."
    # hackathon: drop "brainstorming, " from the description.
    _hk = next((m for m in _mods["modules"] if m["id"] == "hackathon"), None)
    if _hk is None:
        ERRORS.append("install-modules: hackathon missing after prune")
    else:
        _hk_old = "Hackathon workflow skills: scoping, brainstorming, orchestration, shipping, pitching, and demo-video production."
        if _hk.get("description") != _hk_old:
            ERRORS.append("install-modules: hackathon description anchor mismatch")
        else:
            _hk["description"] = "Hackathon workflow skills: scoping, orchestration, shipping, pitching, and demo-video production."
    _paths_after = sum(len(m.get("paths", [])) for m in _mods["modules"])
    if len(_mods["modules"]) != 14 or _paths_after != 84:
        ERRORS.append(f"install-modules: expected 14 modules / 84 paths after, found {len(_mods['modules'])} / {_paths_after}")
    else:
        _dump_json("manifests/install-modules.json", _mods)
        CHANGES.append("install-modules.json pruned: 16 -> 14 modules, 184 -> 84 paths (skill-unified-memory + business-content deleted whole; workflow-quality dependency + descriptions fixed)")
else:
    ERRORS.append("install-modules.json missing")

# 2b. install-components.json: 57 -> 55 components + description fixes.
_cf = p("manifests/install-components.json")
if exists(_cf):
    _comps = _load_json("manifests/install-components.json")
    _clist = _comps["components"]
    if len(_clist) != 57:
        ERRORS.append(f"install-components: expected 57 before, found {len(_clist)}")
    _cby_id = {c["id"]: c for c in _clist}
    for _gone in ("skill:unified-memory", "capability:content"):
        if _gone not in _cby_id:
            ERRORS.append(f"install-components: component {_gone} missing, cannot delete")
    _comps["components"] = [c for c in _clist if c["id"] not in ("skill:unified-memory", "capability:content")]
    _cby_id = {c["id"]: c for c in _comps["components"]}
    for _cid, (_old, _new) in COMPONENT_DESC_FIXES.items():
        _c = _cby_id.get(_cid)
        if _c is None:
            ERRORS.append(f"install-components: component {_cid} missing for description fix")
        elif _c.get("description") != _old:
            ERRORS.append(f"install-components: {_cid} description anchor mismatch")
        else:
            _c["description"] = _new
    for _cid, _old in LANG_FRAMEWORK_DESCS.items():
        _c = _cby_id.get(_cid)
        if _c is None:
            ERRORS.append(f"install-components: component {_cid} missing for description fix")
        elif _c.get("description") != _old:
            ERRORS.append(f"install-components: {_cid} description anchor mismatch")
        else:
            _c["description"] = _old + LANG_FRAMEWORK_NOTE
    if len(_comps["components"]) != 55:
        ERRORS.append(f"install-components: expected 55 after, found {len(_comps['components'])}")
    else:
        _dump_json("manifests/install-components.json", _comps)
        CHANGES.append("install-components.json pruned: 57 -> 55 components (skill:unified-memory + capability:content deleted; 23 description corrections)")
else:
    ERRORS.append("install-components.json missing")

# 2c. install-profiles.json: research 8 -> 7, full 16 -> 14.
_pf = p("manifests/install-profiles.json")
if exists(_pf):
    _profs = _load_json("manifests/install-profiles.json")
    # profiles is a name-keyed dict, NOT a list of {"id": ...} objects
    # (run 2 crashed here on that wrong assumption: iterating a dict
    # yields its string keys, so x["id"] raised TypeError).
    _pby_id = _profs["profiles"]
    _res = _pby_id.get("research")
    _full = _pby_id.get("full")
    if _res is None or _full is None:
        ERRORS.append("install-profiles: research/full profile missing")
    else:
        if "business-content" not in _res.get("modules", []):
            ERRORS.append("install-profiles: research does not list business-content")
        else:
            _res["modules"] = [m for m in _res["modules"] if m != "business-content"]
        _res_old = "Research and content-oriented setup for investigation, synthesis, and publishing workflows."
        if _res.get("description") != _res_old:
            ERRORS.append("install-profiles: research description anchor mismatch")
        else:
            _res["description"] = "Research-oriented setup for investigation and synthesis workflows."
        for _gone in ("skill-unified-memory", "business-content"):
            if _gone not in _full.get("modules", []):
                ERRORS.append(f"install-profiles: full does not list {_gone}")
        _full["modules"] = [m for m in _full["modules"] if m not in ("skill-unified-memory", "business-content")]
        if len(_res["modules"]) != 7 or len(_full["modules"]) != 14:
            ERRORS.append(f"install-profiles: expected research 7 / full 14, found {len(_res['modules'])} / {len(_full['modules'])}")
        else:
            _dump_json("manifests/install-profiles.json", _profs)
            CHANGES.append("install-profiles.json pruned: research 8 -> 7, full 16 -> 14 modules")
else:
    ERRORS.append("install-profiles.json missing")

# ---------------------------------------------------------------- 3. Dead scripts (DEADSCRIPTS_F28)
_removed_scripts = []
_already_absent_scripts = []
for _s in DEAD_SCRIPTS:
    if remove_file(_s):
        _removed_scripts.append(_s)
    else:
        _already_absent_scripts.append(_s)
if len(_removed_scripts) != 135:
    ERRORS.append(f"dead scripts: expected 135 removed, removed {len(_removed_scripts)}")
if _already_absent_scripts:
    CHANGES.append(f"dead scripts already absent (STEP 2 variance): {', '.join(sorted(_already_absent_scripts))}")
CHANGES.append(f"dead scripts removed: {len(_removed_scripts)} files")

# Live hook entry points must survive the cut (15 events + adapter + manifest).
_hj = _load_json("hooks/hooks.json")
if len(_hj.get("hooks", {})) != 15:
    ERRORS.append(f"hooks.json: expected 15 events after script cut, found {len(_hj.get('hooks', {}))}")
if not exists(p("hooks/adapter.js")) or not exists(p("hooks/hooks.json")):
    ERRORS.append("hooks: adapter.js or hooks.json missing after script cut")

# 3b. mcp.json: delete the codebase-memory-mcp server entry.
_mcp = p("mcp.json")
if exists(_mcp):
    _mc = _load_json("mcp.json")
    _servers = _mc.get("mcpServers", {})
    if "codebase-memory-mcp" not in _servers:
        ERRORS.append("mcp.json: codebase-memory-mcp entry missing, cannot delete")
    else:
        del _servers["codebase-memory-mcp"]
        _dump_json("mcp.json", _mc)
        CHANGES.append("mcp.json: codebase-memory-mcp server entry deleted (chrome-devtools + playwright remain)")
else:
    ERRORS.append("mcp.json missing")

# ---------------------------------------------------------------- 4. README count lines -> 67 / 45 / 48 / 55 (README48_F28) + F4
_f = p("README.md")
if exists(_f):
    sub(_f,
        "67 skills, 45 agents, 123 rules, and 55 commands in total (42 agents as-shipped + 3 staged orchestrate agents; 121 rules as-shipped",
        "67 skills, 45 agents, 48 rules, and 55 commands in total (42 agents as-shipped + 3 staged orchestrate agents; 46 rules as-shipped")
    sub(_f,
        "and the chrome-devtools, playwright, and codebase-memory MCP servers",
        "and the chrome-devtools and playwright MCP servers")
    # Fix #28 provenance note, appended after the codebase-memory cut note
    # (:28). Carries the three built-tree _F28 tokens for the verifier census.
    _lines = read(_f).split("\n")
    _idx = next((i for i, _ln in enumerate(_lines) if _ln.startswith("- **Codebase memory**")), None)
    if _idx is None:
        ERRORS.append("README: codebase-memory note line not found for fix28 note insert")
    else:
        _note = "- **Fix #28 bloat cut (Nov 16, 2026)** — 75 cut-language rules, the stale install-manifest paths, and 135 dead scripts removed. Rules are now 48. (`CUTRULES_F28` `MANIFEST28_F28` `DEADSCRIPTS_F28` `README48_F28`)"
        if _note in _lines:
            ERRORS.append("README: fix28 note line already present (double run?)")
        else:
            _lines.insert(_idx + 1, _note)
            write(_f, "\n".join(_lines))
            CHANGES.append("README: fix28 provenance note added after the codebase-memory line")
else:
    ERRORS.append("README missing")

# ---------------------------------------------------------------- 5a. F1 — sessions.md:295 cost-tracker clause (drop; no surviving cost source)
_f = p("commands/sessions.md")
if exists(_f):
    sub(_f,
        "- For command-center style monitoring, combine `/sessions info`, `git diff --stat`, and the cost metrics emitted by `scripts/hooks/cost-tracker.js`.",
        "- For command-center style monitoring, combine `/sessions info` and `git diff --stat`.")
else:
    ERRORS.append("commands/sessions.md missing")

# ---------------------------------------------------------------- 5b. F2 — evaluate-session.js config load + orphan logs (EVALSESS_F28)
_f = p("scripts/hooks/evaluate-session.js")
if exists(_f):
    sub(_f,
        " * Runs on Stop hook to extract reusable patterns from Cursor sessions.",
        " * Runs on Stop hook. Pattern extraction was removed with the\n * continuous-learning skills (fix #27); the evaluator now only enforces\n * the minimum session length and exits.")
    sub(_f,
        "  // Get script directory to find config\n"
        "  const scriptDir = __dirname;\n"
        "  const configFile = path.join(scriptDir, '..', '..', 'skills', 'continuous-learning', 'config.json');\n"
        "\n"
        "  // Default configuration\n"
        "  let minSessionLength = 10;\n"
        "  let learnedSkillsPath = getLearnedSkillsDir();\n"
        "\n"
        "  // Load config if exists\n"
        "  const configContent = readFile(configFile);\n"
        "  if (configContent) {\n"
        "    try {\n"
        "      const config = JSON.parse(configContent);\n"
        "      minSessionLength = config.min_session_length ?? 10;\n"
        "\n"
        "      if (config.learned_skills_path) {\n"
        "        // Handle ~ in path\n"
        "        learnedSkillsPath = config.learned_skills_path.replace(/^~/, require('os').homedir());\n"
        "      }\n"
        "    } catch (err) {\n"
        "      log(`[ContinuousLearning] Failed to parse config: ${err.message}, using defaults`);\n"
        "    }\n"
        "  }\n",
        "  // Default configuration (the continuous-learning skill that owned the\n"
        "  // config file was cut in fix #27, so defaults always apply — EVALSESS_F28)\n"
        "  let minSessionLength = 10;\n"
        "  let learnedSkillsPath = getLearnedSkillsDir();\n")
    sub(_f,
        "  // Signal to Cursor that session should be evaluated for extractable patterns\n"
        "  log(`[ContinuousLearning] Session has ${messageCount} messages - evaluate for extractable patterns`);\n"
        "  log(`[ContinuousLearning] Save learned skills to: ${learnedSkillsPath}`);\n",
        "")
else:
    ERRORS.append("scripts/hooks/evaluate-session.js missing")

# ---------------------------------------------------------------- 5c. react-patterns.mdc:194 accessibility -> frontend-a11y (REACTA11Y_F28)
_f = p("rules/react-patterns.mdc")
if exists(_f):
    sub(_f,
        "For accessibility see `skills/accessibility/SKILL.md`.",
        "For accessibility see `skills/frontend-a11y/SKILL.md`.")
else:
    ERRORS.append("rules/react-patterns.mdc missing")

# ---------------------------------------------------------------- 5d. 77-A1 — port dart-security manifest bullets to react-native-security (DARTSEC_F28)
# Audit #77 showed the dart-security cut removed genuine kept-stack
# guidance: the Android/iOS manifest sections have no equivalent in the
# kept tree, and the globs **/AndroidManifest.xml / **/Info.plist occur
# in Expo prebuild output (kept mobile path). Port the framework-neutral
# bullets (not the Flutter-specific ~80%) into the kept RN security rule,
# including the two manifest globs so the guidance loads on those files.
_f = p("rules/react-native-security.mdc")
if exists(_f):
    sub(_f,
        '  - "**/*.tsx"\n',
        '  - "**/*.tsx"\n  - "**/AndroidManifest.xml"\n  - "**/Info.plist"\n')
    sub(_f,
        "- HTTPS only; reject cleartext. Consider certificate pinning for high-risk apps.",
        "- HTTPS only; reject cleartext. Consider certificate pinning for high-risk apps.\n- Configure Android `network_security_config.xml` to block cleartext traffic.\n- Set request timeouts on all HTTP clients — never leave defaults.")
    sub(_f,
        "## Dependencies",
        "## Native Manifests (AndroidManifest.xml / Info.plist)\n\nExpo prebuild generates these files; the hardening below applies to them.\nPorted from the cut `dart-security` rule in fix #28 (audit #77-A1) — the\nguidance is framework-neutral native hardening, not Flutter-specific.\n(DARTSEC_F28)\n\n- Declare only required permissions in `AndroidManifest.xml`.\n- Export Android components (`Activity`, `Service`, `BroadcastReceiver`)\n  only when necessary; add `android:exported=\"false\"` where not needed.\n- Review intent filters — exported components with implicit intent filters\n  are accessible by any app.\n- Use `FLAG_SECURE` for screens displaying sensitive data (prevents\n  screenshots).\n- Declare only required usage descriptions in `Info.plist`\n  (`NSCameraUsageDescription`, etc.).\n- Set `NSAppTransportSecurity` in `Info.plist` to disallow arbitrary loads.\n- Enable data protection entitlement for sensitive files.\n\n## Dependencies")
else:
    ERRORS.append("rules/react-native-security.mdc missing")

# ---------------------------------------------------------------- 5e. 77-B1 — reword run-with-flags.js caller comments (file is cut)
for _rel, _old, _new in (
    ("scripts/hooks/block-no-verify.js",
     " * Exportable run() for in-process execution via run-with-flags.js.",
     " * Exportable run() for in-process execution."),
    ("scripts/hooks/post-edit-format.js",
     " * Core logic — exported so run-with-flags.js can call directly",
     " * Core logic — exported for in-process use and testability"),
    ("scripts/hooks/quality-gate.js",
     " * Core logic — exported so run-with-flags.js can call directly.",
     " * Core logic — exported for in-process use and testability."),
    ("scripts/hooks/stop-format-typecheck.js",
     " * Exported so run-with-flags.js uses require() instead of spawnSync,",
     " * Exported for in-process execution (rather than spawnSync),"),
):
    _f = p(_rel)
    if exists(_f):
        sub(_f, _old, _new)
    else:
        ERRORS.append(f"{_rel} missing")

# ---------------------------------------------------------------- 5f. 77-B2 — schema description names a cut script as enforcing
_f = p("schemas/capsule-envelope.schema.json")
if exists(_f):
    sub(_f,
        '"description": "One append-only journal entry recorded by the ECC eval-harness capsule. Mirrors scripts/lib/eval-harness/envelope.js, which is the enforcing implementation.",',
        '"description": "One append-only journal entry recorded by the ECC eval-harness capsule.",')
else:
    ERRORS.append("schemas/capsule-envelope.schema.json missing")

# ---------------------------------------------------------------- 5g. 77-B3 — F2 leftovers in evaluate-session.js (dead imports + stale title)
_f = p("scripts/hooks/evaluate-session.js")
if exists(_f):
    sub(_f, "const path = require('path');\n", "")
    sub(_f, "  readFile,\n", "")
    sub(_f, " * Continuous Learning - Session Evaluator", " * Session Evaluator")
    sub(_f, "[ContinuousLearning]", "[SessionEvaluator]", count=2)
else:
    ERRORS.append("scripts/hooks/evaluate-session.js missing")

# ---------------------------------------------------------------- stale-count scan: no old counts may survive
# The call map is excluded: it is generator-owned output, regenerated by
# the fix28 generator copy after this step (SPEC §6); its rows are
# regenerated, not hand-edited.
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
        for _tok in ("123 rules", "121 rules as-shipped"):
            if _tok in _t:
                _stale.append(f"{os.path.relpath(_fp, BASE)}: {_tok!r}")
if _stale:
    ERRORS.append("stale counts remain in the built tree: " + "; ".join(_stale))

# ---------------------------------------------------------------- OWED (recorded, not patched blindly)
OWED = [
    "OWED-28-1 (SPEC §5): orchestration-session.js + tmux-worktree-orchestrator.js are runtime-dead but kept — they are the whole orchestration module in install-modules.json; cutting them deletes the module, drops orchestration from the developer profile, and deletes the capability:orchestration component. Parent decision (ORCHKEEP_F28).",
    "OWED-28-2 (SPEC §5): the 22 misleading install components (§2(b) item 3) are kept with description corrections; deletion is a parent-callable stricter alternative (request would throw Unknown install component instead of installing the shared module).",
    "OWED-28-3 (SPEC §5): motionsites-web-builder is a kept skill in no module (reachable only via the synthetic skill:motionsites-web-builder component). Adding it to hackathon.paths is a parent decision.",
    "OWED-28-4: the call map (skills/orchestrate/references/call-map.md) is generator-owned; it is regenerated by the fix28 generator copy after the build (SPEC §6), not patched here. Until regeneration it lists the 75 cut rules as [struct-rule-globs] self-entries.",
    "OWED-28-5: build.sh RULE_DIRS/RULE_FILES rewriter still lists the cut families; no kept file references a CUT rule in old or new form, so it is a no-op for these families — left alone (SPEC §1(d)).",
    "OWED-28-6: fix27's OWED-11 is closed by this fix for 29 of 31 pointers (the cut rule files carried them); the 2 that stay are react-patterns.mdc:194 (reworded here, REACTA11Y_F28) and hackathon-mode.mdc:37-38 (negative prose, kept as-is).",
]

# ---------------------------------------------------------------- main / run log
_log_lines = ["# fix28 run log", "",
              f"## Errors ({len(ERRORS)})"]
_log_lines += [f"- {e}" for e in ERRORS] or ["- none"]
_log_lines += ["", f"## Changes ({len(CHANGES)})"]
_log_lines += [f"- {c}" for c in CHANGES] or ["- none"]
_log_lines += ["", f"## Command decisions ({len(DECISIONS)})"]
_log_lines += [f"- {d}" for d in DECISIONS] or ["- none"]
_log_lines += ["", f"## OWED ({len(OWED)})"]
_log_lines += [f"- {o}" for o in OWED] or ["- none"]
_log_dir = os.path.join(os.path.dirname(BASE.rstrip("/")), "fix28")
os.makedirs(_log_dir, exist_ok=True)
with open(os.path.join(_log_dir, "fix28-patch-log.md"), "w", encoding="utf-8") as _fh:
    _fh.write("\n".join(_log_lines) + "\n")
print(f"fix28: {len(CHANGES)} change(s)")
for c in CHANGES:
    print(f"  - {c}")
print(f"fix28: {len(OWED)} OWED item(s) recorded in the patch log")
if ERRORS:
    print(f"fix28: {len(ERRORS)} ERROR(S)", file=sys.stderr)
    for e in ERRORS:
        print(f"  ! {e}", file=sys.stderr)
    sys.exit(1)
print("fix28: OK")
