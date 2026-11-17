#!/usr/bin/env python3
"""verify31.py -- checks fix #31 in the BUILT tree (read-only).

Run after a build: python3 fix31/verify31.py [built-plugin-dir]
Default built dir: ~/workspace/hackathon-plugin/hackathon-ecc.
Exits 0 only if every check passes.

Fix #29 (SPEC fix29/SPEC.md): adaptable orchestration — forced
orchestrator, factory dispatch, director-grade briefs. Adds the routing
rules + anchor tokens (ORCHESTRATOR-ONLY_F29, FACTORY-DISPATCH_F29,
DIRECTOR-BRIEF_F29, NO-GUESSING_F29, VERIFY-MERGE_F29,
GLOBAL-ROUTING_F29, COST-AWARE_F29), woven into orchestrate,
hackathon-mode, and the 9 skills that dispatch implementation work
(orchestrate, orch-pipeline, orch-build-mvp, orch-add-feature,
orch-change-feature, orch-fix-defect, orch-refine-code,
feature-expansion, gan-style-harness). The GLOBAL-ROUTING block is
byte-identical in orchestrate + hackathon-mode. Model pins ARE changed (fix #30, SPEC fix30/SPEC.md): the orchestrator
pin changes grok-4.7-high -> grok-4.7-extra-high (49 ID + 22 prose) in
the BUILT tree only — staged sources and build.sh inline keep the old
pin by design (fix16/24/29 anchors abort the build on mismatch; fix #16
precedent). The fast-worker pin cursor-grok-4.6-high-fast is unchanged
(70). The DeepSeek/Qwen assignment in the GLOBAL-ROUTING block stays a
forward reference (OWED-29-4 overridden — the drone assignment lives in
the factory copy, not #30). Counts: skills 67 -> 72 (5 new: getlayers, gsap, react-bits,
hairline-create, hairline-adopt), agents 45, rules 48, commands 55,
hooks 15, trigger keys 49. Call map NOT regenerated (no new dispatch
edges — the new skills are leaf resources, not dispatchers); the fix28
map stands (OWED-31-3).

Fix #31 (SPEC fix31/SPEC.md): design-library additions — GetLayers
(prompt-first cinematic layers, free set only, MCP not wired), GSAP
(timeline/scroll animation, npm install, pin gsap@3.15.1), React Bits
(animated React components, CLI install, no embedded source), Hairline
illustrations (MIT, 33 figures; skills hairline-create + hairline-adopt
vendored). One skill/inventory entry per resource, woven into the
palette-first flow + single inventory catalog (fix #23). GetLayers
prompts carry first-class weight (direction update, Anish Nov 16 ~10:02
PM): consulted FIRST in the palette inventory, the direction leans on
them heavily, and the direction cites the layers USED or
CONSIDERED-AND-REJECTED with a D19 reason.

Build fixes folded in (not cuts): build.sh MS_SRC now follows MS_DIR
(run 1 died on "cp: cannot stat ''" once /tmp/hack-skills was wiped);
fix28.py §2c profiles is a name-keyed dict, not a list of {"id"} objects
(run 2 crashed on that assumption).

Checks (verify27's checks kept, adapted; new checks marked [28]/[29]):
  1. Counts: skills 72, agents 45, rules 48, commands 55; exact dir
     sets match the hardcoded KEPT lists (no extra, none missing).
  1b. [28] All 75 CUT rule files absent; rules dir set is exactly the
     48 KEPT rules.
  2. All 100 CUT skill dirs absent; all 72 KEPT skill dirs present.
  3. Removed agents absent; kept agents present (exact set).
  4. Dropped commands absent; kept commands present (exact set).
  5. Trigger file parses as JSON, zero keys pointing at CUT skills,
     49 keys remain, coverage.skills == 72, withTriggers == 49.
  6. README count lines show the new counts (72/45/48/55, 46 rules
     as-shipped); zero "166 skills" / "72 agents" / "87 commands" /
     "66 skills" / "60 commands" / "123 rules" / "121 rules as-shipped"
     remain in the built tree (excl. node_modules). The stock-ECC line
     ("144 skills, 69 agents, 121 rules, 94 commands") is untouched by
     design.
  7. Every _F27 anchor token still exists in the built tree (20), and
     the _F28 tokens that live in the tree exist where fix28.py wrote
     them (CUTRULES/MANIFEST28/DEADSCRIPTS/README48 in the README fix28
     note, EVALSESS in evaluate-session.js, DARTSEC_F28 in
     react-native-security.mdc asserted in check 10h). The other three _F28 tokens
     (REACTA11Y, NDMISFIRE, ORCHKEEP) live in the patch log,
     asserted in check 11.
  8. Banned terms: 0 in the built tree (case-insensitive, excl.
     node_modules). (The banned list appears in THIS file only, as the
     check pattern -- same precedent as verify26.py -- never in the
     built tree.)
  9. [30] Grok pins: grok-4.7-extra-high x49 (ID) + "Grok 4.7 Extra
     High" x22 (prose); old grok-4.7-high x0 + old prose x0; fast-worker
     pin cursor-grok-4.6-high-fast unchanged x70; bare grok-4.6-high-fast
     count is 0 in the built tree.
 10. Every fix27.py patch anchor still present exactly once (re-assert
     the new texts; old texts gone), so a later rebuild cannot
     silently drop them.
 10b. Round-2 patch anchors (audit #74 B1/B2/B5-B13/B15, M3-M6).
 10c. [28] Every fix28.py patch anchor still present exactly once
     (F1 sessions.md clause drop, F2 evaluate-session.js config-load
     removal + orphan logs, react-patterns.mdc:194 frontend-a11y
     re-point, README F4 MCP line + fix28 provenance note).
 10d. [28] Install manifests: 14 modules / 84 paths / 55 components,
     profiles research 7 / full 14, no dangling module/component
     references, all 84 module paths exist on disk.
 10e. [28] All 135 dead scripts absent; the deliberately kept
     orchestration files and validate-skills.js present; hooks.json
     still 15 events; mcp.json has no codebase-memory entry.
 10f. [28] resolveInstallPlan succeeds for every install profile and
     for the full component set (node, real installer code).
 10g. [28] Regenerated call map: rules 48, no "123" anywhere, sidecar
     counts agree.
 10h. [28] Audit #77 fixes: DARTSEC port present in
     react-native-security.mdc (globs + Native Manifests section +
     network bullets), run-with-flags.js caller comments gone, schema
     description reworded, evaluate-session.js dead imports + stale
     title cleaned.
 11. fix28 patch log exists with 0 errors, 75 rules and 135 scripts
     accounted for, and carries the three patch-log _F28 tokens
     (REACTA11Y, NDMISFIRE, ORCHKEEP).
 12. CUT-name sweep (audit #74 M10, extended in fix #28 to the 75 CUT
     rule basenames): every CUT skill/agent/command/rule name occurs
     zero times as a live dispatch in skills/, agents/, commands/,
     rules/ (excluding the regenerated call map and the trigger
     manifest), except for the explicit ALLOW_LIST of prose-history /
     negative / pointer-style mentions (file -> allowed lines, each
     justified). The 29 orphaned rules/* allow entries from verify27
     are GONE with the cut rule files; only rules/hackathon-mode.mdc
     (kept) remains from rules/, plus the new
     rules/react-native-security.mdc:47 prose-history entry for the
     DARTSEC port note. Generic-word bare uses
     (accessibility, brainstorming, evolve, projects, promote, prune)
     are noise, not dispatches, and are counted separately; their
     strong forms are still swept.
 12b. No imperative dispatch hides in an allow-listed line (audit #75
     B-new-1): every whole-line allow-listed line is re-scanned for an
     imperative verb (use/check/consult/run/invoke/call/load/read)
     with a CUT name backticked or followed by skill/agent/command
 13. [30] fix30 patch log exists with 0 errors, 49 ID + 22 prose renamed,
     fast-worker pin unchanged at 70, GLOBAL-ROUTING block untouched.
     within 120 characters after the verb, except negated verbs and
     "was cut" / "NOT invoked" historical notes (see the check-12b
     comment for the three pinned-down readings).
  7c. [29] _F29 anchor tokens: all 7 exist in the built tree; the
     GLOBAL-ROUTING block is byte-identical in orchestrate +
     hackathon-mode and appears exactly once in each; every one of the
     10 in-scope skills carries GLOBAL-ROUTING_F29; the block names the
     director-brief field list (a naming check only — the real
     brief-completeness check is 7d); the NO-GUESSING carve-out on all
     5 Belief copies with the tie-breaker, the partitioning rule, the
     N>3 justification, the orchestrator-only line, the merge-order
     bridges (3 sites), the correction-brief construction, and the
     harness-gate clause in every factory paragraph are present.
  7d. [29] Real brief-completeness check (audit #80-B10): the seven
     DIRECTOR-BRIEF fields exist as distinct slots in the orchestrate
     contract core, in each of the three implementation templates in
     dispatch-prompt.md, in the feature-expansion brief format, and by
     reference in orch-pipeline + gan-style-harness; the first-build
     carve-out is reconciled (no "instead of NEEDS_CONTEXT" remains).
  7e. [29] _F29 staged-vs-built identity (audit #80-B13, narrow): every
     _F29 line in a staged file is byte-identical in its built copy,
     modulo the [30] pin rename (built lines pin-normalized first).
     (Full-file identity does NOT hold by design — fix16.py scrubs the
     built tree — so only the _F29 lines are asserted.)
  9b. [29] Model pins unchanged: Grok pins as in check 9, and no
     deepseek-/qwen- model slugs exist in the built tree; the names
     DeepSeek/Qwen occur only inside the GLOBAL-ROUTING block's fix-#30
     forward reference (once per block, two blocks).
 10i. [29] Every fix29.py patch anchor still present exactly once
     (orch-pipeline factory paragraph + NO-GUESSING carve-out + Review
     correction-brief sentence, the five orch-* wrapper pointers in
     full, the gan-style-harness factory paragraph + orchestrator
     verify step, the §5 patches: orch-build-mvp carve-out + bridge,
     orch-refine-code step 2 + command mirror, common-agents.mdc
     pointer, gan-build.md pointer + out-of-scope line) and every
     staged half (orchestrate step-4 bridge + contract core,
     feature-expansion Phase 4 paragraph + format items + carve-out,
     design-taste-frontend redesign paragraph + pointer,
     dispatch-prompt.md bounds).
 11b. [29] fix29 patch log exists with 0 errors and the census line
     (all 10 in-scope skills).
 14. [31] Fix #31 design libraries: the 5 new skills exist with
     SKILL.md + frontmatter and no model pin text; all 4 _F31 tokens
     exist and live in their skills; DESIGNPKG-AUTO is byte-identical
     in orchestrate + hackathon-mode, names all 5 skills, and carries
     the GetLayers weight (palette list starts with getlayers, priority
     sentence, citation sentence); the palette-first paragraph names
     getlayers FIRST with the citation sentence; the inventory has §12
     with the GetLayers weight; the getlayers skill carries the
     first-class weight language and invokes no MCP tools and no frozen
     counts; react-bits/gsap/getlayers dirs contain only SKILL.md;
     hairline engine/checks/LICENSE vendored; no vendored GSAP source;
     README fix31 note present; fix31 patch log exists with 0 errors.
"""
import json
import os
import subprocess
import sys

HOME = os.path.expanduser("~")
PLUGIN = os.path.join(HOME, "workspace/hackathon-plugin")
BASE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(PLUGIN, "hackathon-ecc")
BASE = os.path.abspath(BASE)  # audit #77 invocation note: "." as arg broke log/sidecar paths

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
    "frontend-a11y", "frontend-patterns", "frontend-slides", "gan-style-harness", "getlayers",
    "git-workflow",
    "grill-me", "growth-log", "gsap", "hackathon-pitch", "hackathon-scope",
    "hairline-adopt", "hairline-create",
    "integration", "less-flat-ui", "make-interfaces-feel-better",
    "mobile-ship", "motion-advanced", "motion-foundations", "motion-patterns",
    "motionsites-web-builder",
    "nextjs-turbopack", "orch-add-feature", "orch-build-mvp",
    "orch-change-feature", "orch-fix-defect", "orch-pipeline",
    "orch-refine-code", "orchestrate", "pitch-deck-video", "polish-pass",
    "postgres-patterns", "production-audit", "python-patterns",
    "python-testing", "react-bits", "react-native-patterns", "react-patterns",
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

F29_TOKENS = [
    "ORCHESTRATOR-ONLY_F29", "FACTORY-DISPATCH_F29", "DIRECTOR-BRIEF_F29",
    "NO-GUESSING_F29", "VERIFY-MERGE_F29", "GLOBAL-ROUTING_F29",
    "COST-AWARE_F29",
]

# The 10 skills that dispatch implementation work (SPEC §1 scope rule;
# audit #80-A1 added design-taste-frontend — its routing lives in
# references/hallmark/references/redesign.md, with a pointer at SKILL.md:455).
F29_IN_SCOPE = [
    "orchestrate", "orch-pipeline", "orch-build-mvp", "orch-add-feature",
    "orch-change-feature", "orch-fix-defect", "orch-refine-code",
    "feature-expansion", "gan-style-harness", "design-taste-frontend",
]

CUT_RULES = [
    "angular-coding-style.mdc", "angular-hooks.mdc", "angular-patterns.mdc", "angular-security.mdc",
    "angular-testing.mdc", "cpp-coding-style.mdc", "cpp-hooks.mdc", "cpp-patterns.mdc",
    "cpp-security.mdc", "cpp-testing.mdc", "csharp-coding-style.mdc", "csharp-hooks.mdc",
    "csharp-patterns.mdc", "csharp-security.mdc", "csharp-testing.mdc", "dart-coding-style.mdc",
    "dart-hooks.mdc", "dart-patterns.mdc", "dart-security.mdc", "dart-testing.mdc",
    "fsharp-coding-style.mdc", "fsharp-hooks.mdc", "fsharp-patterns.mdc", "fsharp-security.mdc",
    "fsharp-testing.mdc", "golang-coding-style.mdc", "golang-hooks.mdc", "golang-patterns.mdc",
    "golang-security.mdc", "golang-testing.mdc", "java-coding-style.mdc", "java-hooks.mdc",
    "java-patterns.mdc", "java-security.mdc", "java-testing.mdc", "kotlin-coding-style.mdc",
    "kotlin-hooks.mdc", "kotlin-patterns.mdc", "kotlin-security.mdc", "kotlin-testing.mdc",
    "nuxt-coding-style.mdc", "nuxt-hooks.mdc", "nuxt-patterns.mdc", "nuxt-security.mdc",
    "nuxt-testing.mdc", "perl-coding-style.mdc", "perl-hooks.mdc", "perl-patterns.mdc",
    "perl-security.mdc", "perl-testing.mdc", "php-coding-style.mdc", "php-hooks.mdc",
    "php-patterns.mdc", "php-security.mdc", "php-testing.mdc", "ruby-coding-style.mdc",
    "ruby-hooks.mdc", "ruby-patterns.mdc", "ruby-security.mdc", "ruby-testing.mdc",
    "rust-coding-style.mdc", "rust-hooks.mdc", "rust-patterns.mdc", "rust-security.mdc",
    "rust-testing.mdc", "swift-coding-style.mdc", "swift-hooks.mdc", "swift-patterns.mdc",
    "swift-security.mdc", "swift-testing.mdc", "vue-coding-style.mdc", "vue-hooks.mdc",
    "vue-patterns.mdc", "vue-security.mdc", "vue-testing.mdc",
]

KEPT_RULES = [
    "arkts-coding-style.mdc", "arkts-hooks.mdc", "arkts-patterns.mdc", "arkts-security.mdc",
    "arkts-testing.mdc", "common-agents.mdc", "common-code-review.mdc", "common-coding-style.mdc",
    "common-development-workflow.mdc", "common-git-workflow.mdc", "common-hooks.mdc", "common-patterns.mdc",
    "common-performance.mdc", "common-security.mdc", "common-testing.mdc", "hackathon-mode.mdc",
    "ponytail.mdc", "python-coding-style.mdc", "python-fastapi.mdc", "python-hooks.mdc",
    "python-patterns.mdc", "python-security.mdc", "python-testing.mdc", "react-coding-style.mdc",
    "react-hooks.mdc", "react-native-accessibility.mdc", "react-native-coding-style.mdc", "react-native-hooks.mdc",
    "react-native-patterns.mdc", "react-native-performance.mdc", "react-native-production-readiness.mdc", "react-native-security.mdc",
    "react-native-testing.mdc", "react-patterns.mdc", "react-security.mdc", "react-testing.mdc",
    "typescript-coding-style.mdc", "typescript-hooks.mdc", "typescript-patterns.mdc", "typescript-security.mdc",
    "typescript-testing.mdc", "web-coding-style.mdc", "web-design-quality.mdc", "web-hooks.mdc",
    "web-patterns.mdc", "web-performance.mdc", "web-security.mdc", "web-testing.mdc",
]

DEAD_SCRIPTS = [
    "scripts/hooks/auto-tmux-dev.js", "scripts/hooks/bash-hook-dispatcher.js", "scripts/hooks/check-hook-enabled.js", "scripts/hooks/config-protection.js",
    "scripts/hooks/context-prompt-suggestions.js", "scripts/hooks/context-routing-index.js", "scripts/hooks/desktop-notify.js", "scripts/hooks/doc-file-warning.js",
    "scripts/hooks/ecc-context-monitor.js", "scripts/hooks/ecc-metrics-bridge.js", "scripts/hooks/ecc-statusline.js", "scripts/hooks/gateguard-fact-force.js",
    "scripts/hooks/gateguard-heredoc.js", "scripts/hooks/governance-capture.js", "scripts/hooks/hook-input-limits.js", "scripts/hooks/hook-input.js",
    "scripts/hooks/hookify-frontmatter.js", "scripts/hooks/hookify-runtime.js", "scripts/hooks/insaits-security-monitor.py", "scripts/hooks/insaits-security-wrapper.js",
    "scripts/hooks/lifecycle-hook-bootstrap.js", "scripts/hooks/mcp-health-check.js", "scripts/hooks/observe-runner.js", "scripts/hooks/plan-canvas-pending.js",
    "scripts/hooks/plan-canvas-sessions.js", "scripts/hooks/plugin-hook-bootstrap.js", "scripts/hooks/post-bash-build-complete.js", "scripts/hooks/post-bash-command-log.js",
    "scripts/hooks/post-bash-dispatcher.js", "scripts/hooks/post-bash-pr-created.js", "scripts/hooks/post-edit-typecheck.js", "scripts/hooks/posttooluse-dispatcher.js",
    "scripts/hooks/pre-bash-dispatcher.js", "scripts/hooks/pre-bash-git-push-reminder.js", "scripts/hooks/pre-bash-tmux-reminder.js", "scripts/hooks/pre-write-doc-warn.js",
    "scripts/hooks/pretooluse-visible-output.js", "scripts/hooks/run-with-flags-shell.sh", "scripts/hooks/run-with-flags.js", "scripts/hooks/session-activity-tracker.js",
    "scripts/hooks/session-start-bootstrap.js", "scripts/hooks/skill-run-tracker.js", "scripts/lib/agent-compress.js", "scripts/lib/agent-emit-pi.js",
    "scripts/lib/agent-ir.js", "scripts/lib/agent-proximity/distance.js", "scripts/lib/agent-proximity/graph.js", "scripts/lib/agent-proximity/index.js",
    "scripts/lib/agent-proximity/projection.js", "scripts/lib/agent-proximity/shadow-trail.js", "scripts/lib/agent-tool-map.js", "scripts/lib/agent-tools.js",
    "scripts/lib/compute-sponsor.js", "scripts/lib/context-carriers.js", "scripts/lib/context-pack-registry.js", "scripts/lib/context-profile-commands.js",
    "scripts/lib/context-profile-store-fs.js", "scripts/lib/context-profile-store.js", "scripts/lib/context-profile-support.js", "scripts/lib/context-profiles.js",
    "scripts/lib/context-retrieval.js", "scripts/lib/context-routing-index.js", "scripts/lib/context-selection.js", "scripts/lib/control-pane/actions.js",
    "scripts/lib/control-pane/control-plane-view-ui.js", "scripts/lib/control-pane/control-plane-view.js", "scripts/lib/control-pane/message-sink.js", "scripts/lib/control-pane/proximity-viz.js",
    "scripts/lib/control-pane/proximity.js", "scripts/lib/control-pane/server.js", "scripts/lib/control-pane/state.js", "scripts/lib/control-pane/ui.js",
    "scripts/lib/control-pane/work-item-mutations.js", "scripts/lib/control-pane/work-item-runner.js", "scripts/lib/control-pane/work-item-worker.js", "scripts/lib/coordination-inventory.js",
    "scripts/lib/ecc_dashboard_runtime.py", "scripts/lib/eval-harness/canonical.js", "scripts/lib/eval-harness/capsule.js", "scripts/lib/eval-harness/effect-fence.js",
    "scripts/lib/eval-harness/envelope.js", "scripts/lib/eval-harness/gate.js", "scripts/lib/eval-harness/index.js", "scripts/lib/eval-harness/receipt.js",
    "scripts/lib/eval-harness/replay.js", "scripts/lib/eval-harness/retrospective.js", "scripts/lib/feedback-links.js", "scripts/lib/gateguard-change-profile.js",
    "scripts/lib/gateguard-code-lexer.js", "scripts/lib/gateguard-file-context.js", "scripts/lib/gateguard-metrics.js", "scripts/lib/gateguard-readonly-shell.js",
    "scripts/lib/gateguard-search-evidence.js", "scripts/lib/gateguard-search-filters.js", "scripts/lib/gateguard-state.js", "scripts/lib/gateguard-target-class.js",
    "scripts/lib/gateguard-turn-scan.js", "scripts/lib/github-discussions.js", "scripts/lib/github-origin.js", "scripts/lib/harness-adapter-compliance.js",
    "scripts/lib/harness-capabilities.js", "scripts/lib/inspection.js", "scripts/lib/install-state-store-sync.js", "scripts/lib/install/config.js",
    "scripts/lib/install/plugin-namespace.js", "scripts/lib/ito-environment.js", "scripts/lib/loopback-guard.js", "scripts/lib/memory-vault-format.js",
    "scripts/lib/memory-vault.js", "scripts/lib/missing-dependency.js", "scripts/lib/nasiko-release.js", "scripts/lib/opencode-paths.js",
    "scripts/lib/plan-canvas/markdown.js", "scripts/lib/plan-canvas/sdk.js", "scripts/lib/plan-canvas/server.js", "scripts/lib/plan-canvas/sessions.js",
    "scripts/lib/plan-canvas/ui.js", "scripts/lib/platform-launch.js", "scripts/lib/powershell-destructive-command.js", "scripts/lib/session-adapters/canonical-session.js",
    "scripts/lib/session-adapters/dmux-tmux.js", "scripts/lib/session-adapters/registry.js", "scripts/lib/session-bridge.js", "scripts/lib/session-cost-snapshot.js",
    "scripts/lib/skill-evolution/index.js", "scripts/lib/skill-improvement/amendify.js", "scripts/lib/skill-improvement/evaluate.js", "scripts/lib/skill-improvement/health.js",
    "scripts/lib/skill-improvement/observations.js", "scripts/lib/statusline-render.js", "scripts/lib/terminal-spinner.js", "scripts/lib/terminal-welcome.js",
    "scripts/lib/windows-bash.js", "scripts/lib/worktree-lifecycle/git.js", "scripts/lib/worktree-lifecycle/lifecycle.js",
]

assert len(CUT_SKILLS) == 100 and len(KEPT_SKILLS) == 72
assert len(REMOVED_AGENTS) == 27 and len(KEPT_AGENTS) == 45
assert len(DROPPED_COMMANDS) == 32 and len(KEPT_COMMANDS) == 55
assert len(F27_TOKENS) == 20
assert len(F29_TOKENS) == 7 and len(F29_IN_SCOPE) == 10
assert len(CUT_RULES) == 75 and len(KEPT_RULES) == 48
assert len(DEAD_SCRIPTS) == 135
assert not (set(CUT_RULES) & set(KEPT_RULES))
assert not (set(r[:-4] for r in CUT_RULES) & set(KEPT_RULES))
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
check("counts 72 skills / 45 agents / 48 rules / 55 commands",
      (len(_skills), len(_agents), len(_rules), len(_commands))
      == (72, 45, 48, 55))
if (len(_skills), len(_agents), len(_rules), len(_commands)) != (72, 45, 48, 55):
    print(f"   actual: {len(_skills)} skills, {len(_agents)} agents, "
          f"{len(_rules)} rules, {len(_commands)} commands")
check("skills dir set is exactly the 72 KEPT skills",
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

# 1b. Rules: exact kept set (48) and all 75 CUT rules absent.
check("rules dir set is exactly the 48 KEPT rules",
      _rules == sorted(KEPT_RULES))
if _rules != sorted(KEPT_RULES):
    print(f"   extra={sorted(set(_rules) - set(KEPT_RULES))} "
          f"missing={sorted(set(KEPT_RULES) - set(_rules))}")
_cut_rules_present = [r for r in CUT_RULES
                      if os.path.exists(os.path.join(BASE, "rules", r))]
if _cut_rules_present:
    print(f"   CUT rules still present: {_cut_rules_present}")
check("all 75 CUT rule files are ABSENT", not _cut_rules_present)

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
check("trigger coverage: skills 72, withTriggers 49",
      _triggers["coverage"]["skills"] == 72
      and _triggers["coverage"]["withTriggers"] == 49)

# 6. README counts + no stale counts.
_readme = read("README.md")
check("README count line shows 72 skills, 45 agents, 48 rules, 55 commands (46 rules as-shipped)",
      "72 skills, 45 agents, 48 rules, and 55 commands in total "
      "(42 agents as-shipped + 3 staged orchestrate agents; 46 rules as-shipped" in _readme)
check("README comparison lines show the new counts (72 / 45 / 55)",
      "72 skills widen the routing surface" in _readme
      and "56 MB and 72 skills against a minimal set" in _readme
      and "structured process — 72 skills, 45 agents, 55 commands," in _readme)
check("README stock-ECC line untouched (144 skills, 69 agents is stock, not ours)",
      "144 skills, 69 agents, 121 rules, 94 commands" in _readme)
_stale = {}
for _tok in ("166 skills", "72 agents", "87 commands",
             "66 skills", "60 commands", "123 rules", "67 skills",
             "121 rules as-shipped"):
    _n = count_in_tree(_tok, dirs=("skills", "agents", "commands", "rules",
                                   "hooks", "manifests", "scripts"))
    _n += _readme.count(_tok)
    _stale[_tok] = _n
if any(_stale.values()):
    print(f"   stale counts remaining: {_stale}")
check("zero '166 skills' / '72 agents' / '87 commands' / '66 skills' / '60 commands' / '123 rules' / '67 skills' / '121 rules as-shipped' remain in the built tree",
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

# 7b. _F28 tokens that live in the built tree (fix28.py §4/§5b). The
# other three _F28 tokens (REACTA11Y, NDMISFIRE, ORCHKEEP) live only
# in the patch log -- asserted in check 11, not here.
check("fix28 note tokens CUTRULES/MANIFEST28/DEADSCRIPTS/README48_F28 are in README.md",
      _readme.count("- **Fix #28 bloat cut (Nov 16, 2026)** — 75 cut-language rules, "
                    "the stale install-manifest paths, and 135 dead scripts removed. "
                    "Rules are now 48. (`CUTRULES_F28` `MANIFEST28_F28` `DEADSCRIPTS_F28` `README48_F28`)") == 1)
check("fix28-written token EVALSESS_F28 is in scripts/hooks/evaluate-session.js",
      "EVALSESS_F28" in read("scripts/hooks/evaluate-session.js"))

# 7c. [29] _F29 anchor tokens + GLOBAL-ROUTING block byte-identity.
_missing_f29 = [t for t in F29_TOKENS
                if count_in_tree(t) + _readme.count(t) == 0]
if _missing_f29:
    print(f"   missing _F29 tokens: {_missing_f29}")
check("all 7 _F29 anchor tokens exist in the built tree",
      not _missing_f29)


def _global_routing_block(text):
    """The GLOBAL-ROUTING paragraph text (bullet prefix stripped)."""
    for _ln in text.split("\n"):
        if "**GLOBAL-ROUTING" in _ln:
            return _ln[_ln.index("**GLOBAL-ROUTING"):]
    return None


_orch_text = read("skills/orchestrate/SKILL.md")
_hm_text = read("rules/hackathon-mode.mdc")
_orch_block = _global_routing_block(_orch_text)
_hm_block = _global_routing_block(_hm_text)
check("GLOBAL-ROUTING block appears exactly once in orchestrate and once in hackathon-mode",
      _orch_text.count("**GLOBAL-ROUTING") == 1
      and _hm_text.count("**GLOBAL-ROUTING") == 1)
check("GLOBAL-ROUTING block is byte-identical in orchestrate + hackathon-mode",
      _orch_block is not None and _orch_block == _hm_block)
if _orch_block is not None and _hm_block is not None and _orch_block != _hm_block:
    print(f"   orchestrate block: {_orch_block[:120]!r}")
    print(f"   hackathon-mode block: {_hm_block[:120]!r}")
# Audit #85-B3: pin the block against the golden copy in fix29/ — the
# relative staged-vs-built identity check passes a coordinated identical
# edit to both files (e.g. a model assignment smuggled into the block),
# and 9b passes any name on a GLOBAL-ROUTING line. The golden file is
# resolved from the script's own directory first, then from the tree
# root, so scratch-tree runs find it either way.
_GOLDEN_CANDIDATES = [
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 "global-routing-block.txt"),
    os.path.join(os.path.dirname(BASE.rstrip("/")),
                 "fix29", "global-routing-block.txt"),
]
_golden = None
for _gp in _GOLDEN_CANDIDATES:
    if os.path.exists(_gp):
        _golden = open(_gp, encoding="utf-8").read().strip()
        break
if _golden is None:
    print("   golden GLOBAL-ROUTING block file not found")
check("GLOBAL-ROUTING block in orchestrate is byte-identical to the golden copy (audit #85-B3)",
      _golden is not None and _orch_block == _golden)
check("GLOBAL-ROUTING block in hackathon-mode is byte-identical to the golden copy (audit #85-B3)",
      _golden is not None and _hm_block == _golden)
for _tok in F29_TOKENS:
    check(f"GLOBAL-ROUTING block carries token {_tok}",
          _orch_block is not None and _tok in _orch_block)
check("GLOBAL-ROUTING block names the director-brief field list (naming check only — the real completeness check is 7d)",
      _orch_block is not None
      and "the exact goal, the files in scope and explicitly out of scope, constraints, acceptance criteria, verification steps, and what to return" in _orch_block)
check("GLOBAL-ROUTING block carries the partitioning rule (file/module boundary, no shared files)",
      _orch_block is not None
      and "work is partitioned by file/module boundary so no two drones share files or mutable state" in _orch_block)
check("GLOBAL-ROUTING block carries the N>3 justification + minimal context (COST-AWARE)",
      _orch_block is not None
      and "the orchestrator justifies N>3 in one line" in _orch_block
      and "drones carry minimal context, only the files and facts their partition needs" in _orch_block)
check("GLOBAL-ROUTING block carries the orchestrator-only line",
      _orch_block is not None
      and "drones never answer the user directly and never decide scope" in _orch_block)
check("GLOBAL-ROUTING block carries the harness-gate sentence",
      _orch_block is not None
      and "the rules are built as designed, not shrunk to fit Cursor" in _orch_block)
for _skill in F29_IN_SCOPE:
    check(f"in-scope skill {_skill} carries GLOBAL-ROUTING_F29",
          "GLOBAL-ROUTING_F29" in read(f"skills/{_skill}/SKILL.md"))
check("hackathon-mode.mdc carries GLOBAL-ROUTING_F29",
      "GLOBAL-ROUTING_F29" in _hm_text)
_NO_GUESS_CARVE = ("'pick the reasonable option' applies only to carrying out the briefed approach, "
                   "never to a decision the brief leaves unspecified — an unspecified file, scope call, "
                   "or acceptance criterion is returned to the orchestrator as a question, not guessed.")
_TIE_BREAKER = ("When in doubt which side an ambiguity falls on, return the question"
                " — a returned question is never a stall.")
check("NO-GUESSING carve-out present in orch-pipeline (Belief-in-the-brief bounded)",
      _NO_GUESS_CARVE in read("skills/orch-pipeline/SKILL.md"))
check("NO-GUESSING carve-out present in feature-expansion (brief item 6 bounded)",
      _NO_GUESS_CARVE in read("skills/feature-expansion/SKILL.md"))
check("NO-GUESSING carve-out present in orch-build-mvp step 4 (third Belief copy bounded, audit #80-A2/B4)",
      _NO_GUESS_CARVE in read("skills/orch-build-mvp/SKILL.md"))
_dp = read("skills/orchestrate/references/dispatch-prompt.md")
check("NO-GUESSING carve-out present in dispatch-prompt.md Belief line (audit #80-A2/B1)",
      _NO_GUESS_CARVE in _dp)
check("NO-GUESSING bound present in dispatch-prompt.md fast-worker preamble",
      "(Bounded by NO-GUESSING_F29:" in _dp)
# Tree-wide: every "pick the reasonable option" occurrence is bounded
# (audit #80-A2: the fix #29 run-1 census covered only 2 of 5 copies;
# audit #81-B8(i): the run-2 grep excluded agents/, commands/ and every
# references/ file despite the check's name — the next copy would live
# exactly there, so the grep now covers the whole built tree).
_belief_hits = subprocess.run(
    ["grep", "-rn", "pick the reasonable option", "skills", "rules",
     "commands", "agents"],
    cwd=BASE, capture_output=True, text=True).stdout.strip().splitlines()
_belief_hits = [ln for ln in _belief_hits if ln]
if len(_belief_hits) != 5:
    print(f"   'pick the reasonable option' hits: {_belief_hits!r}")
check("'pick the reasonable option' occurs exactly 5x in the whole built tree (all bounded)",
      len(_belief_hits) == 5)
# Carve-out order (audit #81-B8(iv)): the NO-GUESSING carve-out must
# FOLLOW the Belief sentence it bounds in each file — a carve-out that
# moved to another paragraph in the same file would leave the bound
# detached, and the old order-insensitive 7e would still pass.
for _cf in ("skills/orch-pipeline/SKILL.md",
            "skills/feature-expansion/SKILL.md",
            "skills/orch-build-mvp/SKILL.md",
            "skills/orchestrate/references/dispatch-prompt.md"):
    _ct = read(_cf)
    _start = 0
    while True:
        _pos = _ct.find("pick the reasonable option", _start)
        if _pos < 0:
            break
        _carve = _ct.find("applies only to carrying out the briefed approach", _pos)
        check(f"NO-GUESSING carve-out follows the Belief sentence in {_cf}",
              0 < _carve - _pos < 600)
        _start = _pos + 1
# Audit #89-B3: the file-wide `in` was a proxy in the movement mode —
# moving the tie-breaker out of its Belief carve-out left verify29 green
# (88-B2 covered deletion-masking only; a single copy cannot be deleted
# while a second copy masks it, but it can be moved). Scope each
# assertion to the 600-char window after the Belief sentence (the 81-B8
# carve-out-order pattern: live Belief→tie-breaker distances are 356–361
# chars).
for _carve_file in ("skills/orch-pipeline/SKILL.md",
                    "skills/feature-expansion/SKILL.md",
                    "skills/orch-build-mvp/SKILL.md"):
    _cf_text = read(_carve_file)
    _cf_pos = _cf_text.find("pick the reasonable option")
    check(f"tie-breaker present in {_carve_file} Belief carve-out (audit #80-B15, #89-B3)",
          _TIE_BREAKER in _cf_text[_cf_pos:_cf_pos + 600])
# Audit #88-B2: file-wide presence was a proxy — the tie-breaker occurs
# twice in dispatch-prompt.md (Belief paragraph :34 and first-build
# carve-out :52), so deleting the Belief copy left verify29 green.
# Scope the assertion to the Belief paragraph.
_dp_belief = _dp[_dp.index("**Belief in the brief:**"):_dp.index("## Status vocabulary")]
check("tie-breaker present in dispatch-prompt.md Belief line (audit #88-B2)",
      _TIE_BREAKER in _dp_belief)
check("tie-breaker present in dispatch-prompt.md fast-worker preamble (short form)",
      "When in doubt, return the question — a returned question is never a stall." in _dp)
# Audit #89-B2: the construction/bridge checks below were whole-file `in`
# assertions — moving the sentence out of its section left verify29 green.
# They are now scoped to their section paragraph (the 85-B2 pattern).
# The helper is defined here because the 7c checks below need it.
def _para_with(text, marker):
    for _para in text.split("\n\n"):
        if marker in _para:
            return _para
    return ""
# Merge-order bridges at all three sites (audit #80-A3/B7).
check("merge-order bridge present in orchestrate step 4 (partitioning-failure-only)",
      "the merge-order rule at the end of this step applies only if partitioning failed and two drones touched the same file anyway" in _orch_text)
check("merge-order bridge present in feature-expansion Collect (collision procedure) (audit #89-B2)",
      "Collision procedure (sequential dispatch for overlapping scopes is the prevention rule; this is what happens if a collision still occurs)" in _para_with(read("skills/feature-expansion/SKILL.md"), "**Collect and reconcile.**"))
# Audit #89-B2: the MVP step-5 bridge was a whole-file `in` too — scope
# it to the Reconcile step (line-sliced: the step list is not blank-line
# delimited, so _para_with would return the whole section paragraph).
_obm_rec = read("skills/orch-build-mvp/SKILL.md")
_obm_rec = _obm_rec[_obm_rec.index("5. **Reconcile after each wave"):_obm_rec.index("6. **Verify")]
check("merge-order bridge present in orch-build-mvp step 5 Reconcile (audit #89-B2)",
      "This procedure applies only if partitioning failed and two implementers touched the same file anyway" in _obm_rec)
# Correction-brief construction (audit #80-B8): the re-dispatch carries a
# correction brief naming the failed criterion, distinct from the original.
_CORR_BRIEF = ("carries a correction brief naming the failed acceptance criterion "
               "and the required correction, distinct from the original brief")
check("correction brief constructed in feature-expansion fix loop (audit #89-B2)",
      _CORR_BRIEF in _para_with(read("skills/feature-expansion/SKILL.md"), "**Fix loop (capped).**"))
# Audit #89-B2: the orch-pipeline sentence lives in the Phase 5 Review
# list item (line-sliced: the phase list is one paragraph, so _para_with
# would return items 2–6 together).
_op = read("skills/orch-pipeline/SKILL.md")
_op_review = _op[_op.index("- **5. Review**"):_op.index("- **6. Commit**")]
check("correction brief constructed in orch-pipeline Phase 5 Review fix loop (audit #89-B2)",
      _CORR_BRIEF in _op_review)
# Audit #81-B3: orchestrate step 5's own verify loop constructs the
# correction brief (the manifest's inheritance claim for step 5 was
# unsupported — only orch-build-mvp step 6 inherits via Phase 5 Review).
# The GLOBAL-ROUTING block mentions "correction brief" but not this
# construction sentence, so count == 1 is the ladder only.
# Audit #90-B2: the whole-file count was NOT 7e-guarded as the #89-B2
# adjudication claimed — line :252 is the last _F29 line in the file, so
# 7e order-sensitivity is vacuous for a whole-line move to EOF. Scope to
# the escalation-ladder section (89-B2 pattern). The step-4 bridge half
# of that adjudication stands (line :93 is mid-file) and is not re-filed.
_orch_ladder = _orch_text[_orch_text.index("One ladder, strictly upward:"):_orch_text.index("### Mixing fast-worker and deep-reasoner")]
check("correction brief constructed in orchestrate escalation ladder (audit #81-B3, #90-B2)",
      _orch_ladder.count(_CORR_BRIEF) == 1)
# Audit #85-B1: the redesign paragraph's correction-brief path did not
# name the failed criterion — every other consumption site does. The
# redesign sentence carries its own wording ("sends failed output back
# with …"), so this asserts the full clause, not the shared _CORR_BRIEF
# string (which starts "carries a correction brief …").
check("correction brief constructed in design-taste-frontend redesign paragraph (audit #85-B1)",
      "sends failed output back with a correction brief naming the failed acceptance criterion and the required correction, distinct from the original brief" in read("skills/design-taste-frontend/references/hallmark/references/redesign.md"))
# Harness-gate clause on slot refill in every factory paragraph (audit #80-B9).
# Audit #85-B2: the old checks asserted file-wide presence, not
# in-paragraph position — moving the clause out of orch-pipeline's
# factory paragraph to an EOF footnote left verify29 green while the
# paragraph promised unconditional slot refill. Each assertion is now
# scoped to the paragraph containing the factory/step-4 marker, the way
# 83-B1 scoped the GENERATE checks to the _gen slice.
_HARNESS_GATE = "in Cursor, slots refill per wave, not per completion"
for _gf, _gname, _gmarker in (
        ("skills/orch-pipeline/SKILL.md", "orch-pipeline",
         "**Factory routing (fix #29, GLOBAL-ROUTING_F29):** every phase dispatches through the factory"),
        ("skills/feature-expansion/SKILL.md", "feature-expansion",
         "**Factory routing (fix #29, GLOBAL-ROUTING_F29).** Phase 4 implementers are factory drones"),
        ("skills/gan-style-harness/SKILL.md", "gan-style-harness",
         "**Factory routing (fix #29, GLOBAL-ROUTING_F29):** the generator/evaluator loop runs as factory drones"),
        ("skills/design-taste-frontend/references/hallmark/references/redesign.md", "redesign",
         "**Factory routing (fix #29, GLOBAL-ROUTING_F29):** each page subagent is a single-task factory drone")):
    check(f"harness-gate clause on slot refill in {_gname} factory paragraph",
          _HARNESS_GATE in _para_with(read(_gf), _gmarker))
check("harness-gate clause on slot refill in orchestrate step 4",
      _HARNESS_GATE in _para_with(
          _orch_text,
          "Each wave is a set of slots in the orchestrator's factory queue (GLOBAL-ROUTING_F29)"))
# design-taste-frontend routing (audit #80-A1): paragraph in redesign.md,
# pointer at SKILL.md:455.
check("design-taste-frontend redesign.md carries the factory routing paragraph",
      "each page subagent is a single-task factory drone with a director brief" in read("skills/design-taste-frontend/references/hallmark/references/redesign.md"))
check("design-taste-frontend redesign.md locks shared stylesheet/tokens single-writer",
      "are single-writer: locked once before page fan-out" in read("skills/design-taste-frontend/references/hallmark/references/redesign.md"))
# Audit #81-A2: the single-writer rule states the outcome but the
# enforcement mechanism is the out-of-scope slot of every page brief
# (tokens file passed read-only; orchestrator locks before fan-out).
check("design-taste-frontend redesign.md lists shared files out of scope in every page brief (audit #81-A2)",
      "are listed out of scope in every page brief, and the tokens file is passed to page drones read-only" in read("skills/design-taste-frontend/references/hallmark/references/redesign.md"))
# Audit #81-A3: the redesign paragraph is the fifth factory paragraph —
# it carries the harness-gate clause and a queue sentence like the other four.
check("design-taste-frontend redesign.md carries the factory queue sentence (audit #81-A3)",
      "Page drones queue in the factory queue and dispatch into freed slots as drones retire" in read("skills/design-taste-frontend/references/hallmark/references/redesign.md"))
# Audit #91-B5: the whole-file `in` was a proxy — moving line :455 to EOF
# left verify29 green, and 7e cannot guard it (the file carries exactly
# one _F29 line, so a whole-line move preserves the _F29 line list — the
# same vacuity as the ladder :252 case 90-B2 fixed). A line-content check
# alone does not fix it either: the clause travels with the line. Scope
# to the step-4→step-5 span of "## 4. The run", where the redesign
# paragraph sits, and assert the pointer clause on the redesign-flow line
# inside that span (7d(c) _fe_item line pattern, position-scoped).
_dtf = read("skills/design-taste-frontend/SKILL.md")
_dtf_run45 = _dtf[_dtf.index("4. **Deal, never choose by taste.**"):_dtf.index("5. **Build.**")]
_dtf_redesign_lines = [ln for ln in _dtf_run45.splitlines() if "follow the Hallmark redesign flow" in ln]
check("design-taste-frontend SKILL.md:455 points at the redesign flow factory routing (audit #91-B5)",
      len(_dtf_redesign_lines) == 1 and "factory routing for the redesign flow lives there" in _dtf_redesign_lines[0])
check("orchestrate step-4 factory bridge present (waves are factory-queue slots)",
      "Each wave is a set of slots in the orchestrator's factory queue (GLOBAL-ROUTING_F29)" in _orch_text)

# 7d. [29] Real brief-completeness check (audit #80-B10): the seven
# DIRECTOR-BRIEF fields exist as distinct slots in the formats that
# actually construct briefs — not just named in the GLOBAL-ROUTING block.
# (a) Orchestrate contract core: extract the fenced contract block and
# assert all seven field labels + the no-drop rule + out-of-scope files.
_contract = _orch_text.split("The contract core")[1].split("```")[1]
for _field in ("Goal:", "Inputs:", "Constraints:", "Interface:",
               "Acceptance check:", "Verification steps:", "Return format:"):
    check(f"contract core carries field {_field}",
          _field in _contract)
check("contract core Constraints names files explicitly out of scope",
      "files explicitly out of scope" in _contract)
check("contract core forbids dropping a DIRECTOR-BRIEF field",
      "drop no field" in _orch_text.split("The contract core")[1].split("```")[0])
# Audit #87-B2: the no-drop check asserted only "drop no field" — the
# `none` mechanism (the placeholder that makes "drop no field"
# implementable when a field is genuinely empty) was unasserted; deleting
# "written as `none`, " left verify29 green.
check("contract core no-drop rule names the `none` mechanism (audit #87-B2)",
      "written as `none`" in _orch_text.split("The contract core")[1].split("```")[0])
# (b) dispatch-prompt.md: per-template presence (audit #81-A1/B6/B8(iii)).
# A bare count cannot distinguish "four occurrences in the right places"
# from "one template missing and another doubled" — the worked example
# lacked Verification steps while the old count check passed. Each
# brief-shaped section must carry all seven DIRECTOR-BRIEF fields itself.
# Audit #84-B1: the round-4 loop asserted only 2 of the 7 fields per
# section (Verification steps + files out of scope) — deleting the recon
# template's Acceptance check line left verify29 green. Each template
# now asserts all seven field labels; the skeleton names the seven fields
# in its item-3 enumeration instead of labeled slots. (The second-pass
# template is exempt as an opinion template; it carries a NEEDS_CONTEXT
# line instead — asserted below, audit #81-A5.)
def _dp_section(start_marker, end_marker):
    _i = _dp.find(start_marker)
    _j = _dp.find(end_marker, _i) if end_marker else len(_dp)
    return _dp[_i:_j] if _i >= 0 else ""
_SKELETON_ENUM = ("Goal, Inputs, Constraints (incl. files out of scope), "
                  "Interface, Acceptance check, Verification steps, Return format")
check("dispatch-prompt.md skeleton names all seven DIRECTOR-BRIEF fields (audit #84-B1)",
      _SKELETON_ENUM in _dp_section("## Skeleton", "## Template — recon"))
for _sec_name, _start, _end in (
        ("recon template", "## Template — recon", "## Template — mechanical"),
        ("mechanical template", "## Template — mechanical", "## Template — reasoning"),
        ("reasoning template", "## Template — reasoning", "## Template — second"),
        ("blind-reviewer template", "## Template — blind reviewer", "## Worked example"),
        ("worked example", "## Worked example", "## Common mistakes")):
    _sec = _dp_section(_start, _end)
    for _field in ("Goal:", "Inputs:", "Constraints:", "Acceptance check:",
                   "Verification steps:", "files out of scope", "Return format:"):
        check(f"dispatch-prompt.md {_sec_name} carries {_field} (audit #84-B1)",
              _field in _sec)
# Audit #93-B2: the tuple above never asserted `Interface:` — recon and
# reasoning carried only 6 of the 7 slots while the check claimed all seven
# field labels (#84-B1's "all seven field labels" was wrong for Interface;
# #92-B §6's "all five templates 7/7" likewise). The blind reviewer is
# exempt by design (dispatch-prompt.md:15 gives it its own verification-gate
# contract) and the second-pass template is exempt (opinion-only). Assert
# `Interface:` for the three implementation templates + worked example only.
for _sec_name, _start, _end in (
        ("recon template", "## Template — recon", "## Template — mechanical"),
        ("mechanical template", "## Template — mechanical", "## Template — reasoning"),
        ("reasoning template", "## Template — reasoning", "## Template — second"),
        ("worked example", "## Worked example", "## Common mistakes")):
    check(f"dispatch-prompt.md {_sec_name} carries Interface: (audit #93-B2)",
          "Interface:" in _dp_section(_start, _end))
check("dispatch-prompt.md has no 'delete fields that are genuinely N/A'",
      "delete fields that are genuinely N/A" not in _dp)
check("dispatch-prompt.md has no 'six fields'",
      "six fields" not in _dp)
check("dispatch-prompt.md has no 'instead of NEEDS_CONTEXT' (first-build carve-out reconciled)",
      "instead of NEEDS_CONTEXT" not in _dp)
# Audit #90-B1: whole-file `in` was a proxy — moving the sentence out of
# the reasoning template left verify29 green. Scope to the template
# section (7d(b) pattern).
check("dispatch-prompt.md first-build carve-out routes the question to the orchestrator (audit #90-B1)",
      "the question goes to the orchestrator" in _dp_section("## Template — reasoning", "## Template — second"))
# Tree-wide (audit #81-B1/B8(ii)): the unbounded phrase is gone from the
# whole built tree, and every remaining "state the assumption" sits in a
# known bounded site — the old file-scoped check passed while
# agents/deep-reasoner.md:17 carried the identical phrase.
_assume_hits = subprocess.run(
    ["grep", "-rn", "state the assumption you made and proceed",
     "skills", "rules", "commands", "agents"],
    cwd=BASE, capture_output=True, text=True).stdout.strip().splitlines()
_assume_hits = [ln for ln in _assume_hits if ln]
check("'state the assumption you made and proceed' occurs 0x in the built tree (audit #81-B1)",
      len(_assume_hits) == 0)
_assume_files = subprocess.run(
    ["grep", "-rln", "state the assumption",
     "skills", "rules", "commands", "agents"],
    cwd=BASE, capture_output=True, text=True).stdout.strip().splitlines()
_assume_files = sorted(ln for ln in _assume_files if ln)
check("'state the assumption' occurs only in the known bounded sites (audit #81-B8(ii))",
      _assume_files == ["agents/deep-reasoner.md",
                        "skills/orchestrate/SKILL.md",
                        "skills/orchestrate/references/dispatch-prompt.md",
                        "skills/polish-pass/SKILL.md",
                        "skills/polish-pass/reference/impeccable-critique.md",
                        "skills/systematic-debugging/SKILL.md"])
check("agents/deep-reasoner.md carries the NO-GUESSING bound + tie-breaker (audit #81-B1)",
      "Bounded by NO-GUESSING_F29" in read("agents/deep-reasoner.md")
      and "returned to the orchestrator as a question, not guessed" in read("agents/deep-reasoner.md")
      and "When in doubt which side an ambiguity falls on, return the question" in read("agents/deep-reasoner.md"))
# First-build carve-out scope + actor reconciliation + tie-breaker
# (audit #81-B4/B5): the scope sentence at all four drone-side sites,
# the actor line and the tie-breaker in the governing status-vocabulary
# carve-out.
# Audit #89-B4: the bare count (== 4) was a proxy — deleting the scope
# sentence at one site and doubling it at another left verify29 green.
# Assert per-site presence instead. The four sites are the mechanical
# template's preamble and "Before you begin" paragraphs, and the worked
# example's copies of the same two paragraphs. (The auditor's "reasoning
# template" label for the third site is wrong: the reasoning template
# carries no scope sentence — :212 is the worked example's preamble
# copy. The fix stands; only the label was off.)
_mech = _dp_section("## Template — mechanical", "## Template — reasoning")
_wex = _dp_section("## Worked example", "## Common mistakes")
_SCOPE_SENT = "for carrying out the briefed approach only, state the assumption"
check("first-build carve-out scope sentence in mechanical preamble (audit #81-B4, #89-B4)",
      _mech[:_mech.index("Context: [one line")].count(_SCOPE_SENT) == 1)
check("first-build carve-out scope sentence in mechanical Before-you-begin (audit #81-B4, #89-B4)",
      _mech[_mech.index("Before you begin:"):].count(_SCOPE_SENT) == 1)
check("first-build carve-out scope sentence in worked-example preamble (audit #81-B4, #89-B4)",
      _wex[:_wex.index("Context:")].count(_SCOPE_SENT) == 1)
check("first-build carve-out scope sentence in worked-example Before-you-begin (audit #81-B4, #89-B4)",
      _wex[_wex.index("Before you begin:"):].count(_SCOPE_SENT) == 1)
_fb_carve = _dp.split("**First-build carve-out")[1].split("## Template")[0]
check("first-build carve-out reconciles who states the assumption (audit #81-B4)",
      "The drone states assumptions only for execution detail; for an unspecified decision the orchestrator states the assumption." in _fb_carve)
check("tie-breaker present in dispatch-prompt.md first-build carve-out (audit #81-B5)",
      _TIE_BREAKER in _fb_carve)
check("second-pass template returns NEEDS_CONTEXT on an unspecified decision (audit #81-A5, #90-B1)",
      "If the task body leaves a decision unspecified, return `NEEDS_CONTEXT` naming it — do not guess." in _dp_section("## Template — second deep-reasoner pass", "## Template — blind reviewer"))
# (c) feature-expansion brief format: out-of-scope item, split 4a/4b,
# return-format item (audit #80-B5). Audit #84-B1: the round-4 check
# asserted only items 2/4a/4b/9 — deleting the Constraints label from
# item 3 left verify29 green. Items 1 and 3 are asserted as well now.
# Audit #87-B2: every check above was a whole-file substring — moving
# the item-2 in-scope phrase to item 5, or deleting the 4a/4b bodies or
# the item-3 parenthetical, left verify29 green. Each assertion is now
# scoped to its own item's line (extracted from the format block the way
# 83-B1 scopes the GENERATE checks) and asserts the fuller content.
_fe = read("skills/feature-expansion/SKILL.md")
_fe_format = _fe.split("A brief contains:")[1].split("**UI rule")[0]
def _fe_item(marker):
    for _ln in _fe_format.split("\n"):
        if _ln.startswith(marker):
            return _ln
    return ""
check("feature-expansion format item 1 states where the feature fits and why (audit #84-B1)",
      "1. One line on where this feature fits in the product and why it was approved." in _fe_item("1. "))
check("feature-expansion format item 2 names the files it touches (in scope) (audit #86-B2)",
      "and which files it touches" in _fe_item("2. "))
check("feature-expansion format item 2 names files explicitly OUT of scope",
      "and the files explicitly OUT of scope (named; `none` if genuinely none)" in _fe_item("2. "))
check("feature-expansion format item 3 names Constraints (audit #84-B1)",
      "3. Constraints: global rules that bind this feature" in _fe_item("3. "))
check("feature-expansion format item 3 states constraints explicitly, not by reference (audit #87-B2)",
      "stated explicitly in the brief, not by reference" in _fe_item("3. "))
check("feature-expansion format splits acceptance criteria (4a) from verification steps (4b)",
      "4a. Acceptance criteria:" in _fe_item("4a. ") and "4b. Verification steps:" in _fe_item("4b. "))
check("feature-expansion format item 4a states the pass bar (audit #87-B2)",
      "the pass bar the feature must meet — the exact outcome, named (what counts as done, not how to check it)" in _fe_item("4a. "))
check("feature-expansion format item 4b states the verification procedure (audit #87-B2)",
      "the exact commands or checks that prove it works (run the app, exercise the feature, confirm the visible result)" in _fe_item("4b. "))
check("feature-expansion format item 9 states the return format",
      "9. Return format: status, changed files, verification evidence, residual risks, blockers" in _fe_item("9. "))
# (d) orch-pipeline + gan-style-harness brief formats by reference
# (audit #80-B6): the seven-field contract is named where briefs are built.
# Audit #90-B4: whole-file presence was a proxy — the reference sentence
# is only meaningful in the factory paragraph where briefs are built.
# Scope to the factory paragraph (_para_with, 85-B2 pattern).
check("orch-pipeline briefs follow the seven-field contract (by reference) (audit #90-B4)",
      "Briefs follow the seven-field contract in `skills/orchestrate/references/dispatch-prompt.md`" in _para_with(read("skills/orch-pipeline/SKILL.md"), "**Factory routing (fix #29, GLOBAL-ROUTING_F29):** every phase dispatches through the factory"))
check("gan-style-harness briefs follow the seven-field contract (by reference) (audit #90-B4)",
      "Generator and evaluator briefs follow the seven-field contract in `skills/orchestrate/references/dispatch-prompt.md`" in _para_with(read("skills/gan-style-harness/SKILL.md"), "**Factory routing (fix #29, GLOBAL-ROUTING_F29):** the generator/evaluator loop runs as factory drones"))

# 7e. [29] _F29 staged-vs-built identity (audit #80-B13, narrow form).
# Full-file identity does NOT hold by design (fix16.py scrubs the built
# tree from staged anchors — e.g. hackathon-mode:38 `claude -p` — and
# build steps normalize agent citations in orchestrate), so only the
# _F29 lines are asserted: a rebuild must not drop or alter routing text.
# [30] The built lines are pin-normalized first (see the loop): the
# rename is the one permitted staged-vs-built difference (OWED-30-1).
_PLUGIN_ROOT = os.path.dirname(BASE.rstrip("/"))
_STAGED_F29 = [
    ("new-skills/orchestrate/SKILL.md", "skills/orchestrate/SKILL.md"),
    ("new-skills/orchestrate/references/dispatch-prompt.md",
     "skills/orchestrate/references/dispatch-prompt.md"),
    ("new-skills/orchestrate/agents/deep-reasoner.md",
     "agents/deep-reasoner.md"),
    ("new-skills/feature-expansion/SKILL.md", "skills/feature-expansion/SKILL.md"),
    ("new-skills/design-taste-frontend/SKILL.md", "skills/design-taste-frontend/SKILL.md"),
    ("new-skills/design-taste-frontend/references/hallmark/references/redesign.md",
     "skills/design-taste-frontend/references/hallmark/references/redesign.md"),
    ("new-rules/hackathon-mode.mdc", "rules/hackathon-mode.mdc"),
]
for _staged_rel, _built_rel in _STAGED_F29:
    _staged_path = os.path.join(_PLUGIN_ROOT, _staged_rel)
    _built_path = os.path.join(BASE, _built_rel)
    if not os.path.exists(_staged_path) or not os.path.exists(_built_path):
        check(f"_F29 lines identical staged-vs-built for {_built_rel}",
              False)
        continue
    # Order-sensitive (audit #81-B8(iv)): the old sorted comparison let a
    # _F29 line move within a file pass silently — the NO-GUESSING
    # carve-out must follow the Belief sentence it bounds, so the line
    # order itself is part of the assertion now.
    _s_lines = [ln for ln in open(_staged_path, encoding="utf-8").read().split("\n") if "_F29" in ln]
    _b_lines = [ln for ln in open(_built_path, encoding="utf-8").read().split("\n") if "_F29" in ln]
    # [30] Normalize the by-design pin drift (OWED-30-1): the built tree
    # says grok-4.7-extra-high / "Grok 4.7 Extra High" where staged says
    # grok-4.7-high / "Grok 4.7 High" (fix30.py renames at build time
    # because fix16/24/29 anchor on the old pin). Only the pin is
    # normalized — any other staged-vs-built difference still fails.
    # (skills/orchestrate/SKILL.md:93 carries both _F29 tokens and the
    # pin, so without this the rename breaks the identity check.)
    _b_lines = [ln.replace("grok-4.7-extra-high", "grok-4.7-high").replace(
        "Grok 4.7 Extra High", "Grok 4.7 High") for ln in _b_lines]
    if _s_lines != _b_lines:
        print(f"   _F29 staged-vs-built mismatch in {_built_rel}: "
              f"staged {len(_s_lines)} lines, built {len(_b_lines)} lines")
    check(f"_F29 lines identical staged-vs-built for {_built_rel}",
          _s_lines == _b_lines and len(_s_lines) > 0)

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

# 9. [30] Grok pins: orchestrator is now grok-4.7-extra-high (49 ID +
# 22 prose); the old grok-4.7-high pin is gone (0 ID + 0 prose); the
# fast-worker pin cursor-grok-4.6-high-fast is unchanged (70) and no
# bare grok-4.6-high-fast exists. Exact counts (not >0): a partial
# rename is worse than a failed build.
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
_g47x = subprocess.run(
    ["grep", "-ro", "grok-4.7-extra-high", ".", "--exclude-dir=node_modules"],
    cwd=BASE, capture_output=True, text=True).stdout.strip()
_c46 = subprocess.run(
    ["grep", "-ro", "cursor-grok-4.6-high-fast", ".", "--exclude-dir=node_modules"],
    cwd=BASE, capture_output=True, text=True).stdout.strip()
_p47 = subprocess.run(
    ["grep", "-ro", "Grok 4.7 High", ".", "--exclude-dir=node_modules"],
    cwd=BASE, capture_output=True, text=True).stdout.strip()
_p47x = subprocess.run(
    ["grep", "-ro", "Grok 4.7 Extra High", ".", "--exclude-dir=node_modules"],
    cwd=BASE, capture_output=True, text=True).stdout.strip()
_n_g47 = len(_g47.splitlines())
_n_g47x = len(_g47x.splitlines())
_n_c46 = len(_c46.splitlines())
_n_p47 = len(_p47.splitlines())
_n_p47x = len(_p47x.splitlines())
print(f"   grok-4.7-high x{_n_g47}, grok-4.7-extra-high x{_n_g47x}, "
      f"cursor-grok-4.6-high-fast x{_n_c46}, "
      f"'Grok 4.7 High' x{_n_p47}, 'Grok 4.7 Extra High' x{_n_p47x}")
check("orchestrator pin is grok-4.7-extra-high x49 and old grok-4.7-high is 0",
      _n_g47x == 49 and _n_g47 == 0)
check("orchestrator prose is 'Grok 4.7 Extra High' x22 and old prose is 0",
      _n_p47x == 22 and _n_p47 == 0)
check("fast-worker pin cursor-grok-4.6-high-fast unchanged at x70",
      _n_c46 == 70)

# 9b. [29] Model pins unchanged: no fix-#30 model slugs in the tree;
# DeepSeek/Qwen names occur only in the GLOBAL-ROUTING block's
# forward reference (once per block, two blocks) plus two allow-listed
# benign pre-existing hits (audit #95-B1). Audit #84-B2: the name grep
# used to be scoped to SKILL.md + *.mdc in skills/rules, so a model
# reference in a references/ or commands/ file passed (a
# "reasoning-heavy work goes to DeepSeek" line in dispatch-prompt.md and
# in gan-build.md both left verify29 green). Audit #95-B1: the grep was
# still scoped to 6 dirs (skills/agents/commands/rules/hooks/README.md)
# while the comment claimed "tree-wide" — a name in manifests/ or
# scripts/ passed. Both greps are now whole-tree (".", minus
# node_modules). The name allow-list is file-level for the three
# pre-existing icon-data files that carry "DeepSeek" as an icon name
# (data, not a model reference), and file+line for the two benign hits
# outside the old scope (a planted reference elsewhere in either file
# must still fail):
#   manifests/pi-core.json:243 — "deepseek-harness-setup" provider note
#   scripts/lib/install/content-transform.js:4 — Qwen in a
#     removed-transforms comment (not a model reference or slug).
# Every remaining hit must sit on a GLOBAL-ROUTING line.
_deepseek_slugs = subprocess.run(
    ["grep", "-rn", "deepseek/", ".", "--exclude-dir=node_modules"],
    cwd=BASE, capture_output=True, text=True).stdout.strip()
_qwen_slugs = subprocess.run(
    ["grep", "-rn", "qwen/", ".", "--exclude-dir=node_modules"],
    cwd=BASE, capture_output=True, text=True).stdout.strip()
if _deepseek_slugs or _qwen_slugs:
    print(f"   fix-#30 model slugs found: {(_deepseek_slugs + _qwen_slugs)[:400]!r}")
check("no deepseek-/qwen- model slugs in the built tree (fix #30 has not landed)",
      _deepseek_slugs == "" and _qwen_slugs == "")
_DSQ_ALLOW = {
    "skills/design-taste-frontend/assets/icons/demo.html",
    "skills/design-taste-frontend/assets/icons/demo/icons-credits.json",
    "skills/design-taste-frontend/assets/icons/index.json",
}
_DSQ_ALLOW_LINES = {
    "manifests/pi-core.json": {243},
    "scripts/lib/install/content-transform.js": {4},
}
_dsq = subprocess.run(
    ["grep", "-rn", "-E", "DeepSeek|Qwen", ".",
     "--exclude-dir=node_modules"],
    cwd=BASE, capture_output=True, text=True).stdout.strip().splitlines()


def _dsq_allowed(_ln):
    """True if a grep hit is an allow-listed benign name (audit #95-B1)."""
    _parts = _ln.split(":", 2)
    if len(_parts) < 2:
        return False
    _f = _parts[0][2:] if _parts[0].startswith("./") else _parts[0]
    if _f in _DSQ_ALLOW:
        return True
    try:
        _n = int(_parts[1])
    except ValueError:
        return False
    return _n in _DSQ_ALLOW_LINES.get(_f, set())


_dsq = [ln for ln in _dsq if ln and not _dsq_allowed(ln)]
if len(_dsq) != 2 or not all("GLOBAL-ROUTING" in ln for ln in _dsq):
    print(f"   DeepSeek/Qwen name hits outside the allow-list: {_dsq!r}")
check("DeepSeek/Qwen names occur only in the GLOBAL-ROUTING block + 2 allow-listed benign hits (audit #84-B2, #95-B1)",
      len(_dsq) == 2 and all("GLOBAL-ROUTING" in ln for ln in _dsq))
# Audit #86-B1: the line count above cannot see a second name on an
# already-matching line — the #85-B3 X1 smuggle (a second Qwen on each
# block line) left 9b passing. Assert occurrence counts too: one DeepSeek
# and one Qwen per block. (The golden pin in 7c guards the same class;
# this is defense-in-depth.)
check("DeepSeek/Qwen name occurrences are exactly one of each per GLOBAL-ROUTING block (audit #86-B1)",
      sum(ln.count("DeepSeek") for ln in _dsq) == 2
      and sum(ln.count("Qwen") for ln in _dsq) == 2)

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

# 10c. fix28 patch anchors (F1/F2/react-patterns/README F4).
_sess = read("commands/sessions.md")
check("F1 sessions.md: cost-tracker clause dropped, monitoring clause present x1",
      _sess.count("- For command-center style monitoring, combine `/sessions info` and `git diff --stat`.") == 1
      and "cost-tracker.js" not in _sess)
_eval = read("scripts/hooks/evaluate-session.js")
check("F2 evaluate-session.js: new header + EVALSESS default-config comment present, config load + orphan logs gone",
      _eval.count("Pattern extraction was removed with the") == 1
      and _eval.count("so defaults always apply — EVALSESS_F28") == 1
      and "skills', 'continuous-learning', 'config.json'" not in _eval
      and "continuous-learning', 'config.json'" not in _eval
      and "Failed to parse config" not in _eval
      and "evaluate for extractable patterns" not in _eval
      and "Save learned skills to:" not in _eval)
_rp = read("rules/react-patterns.mdc")
check("react-patterns.mdc:194 re-pointed at frontend-a11y (REACTA11Y_F28), old accessibility link gone",
      _rp.count("For accessibility see `skills/frontend-a11y/SKILL.md`.") == 1
      and "skills/accessibility/SKILL.md" not in _rp)
check("F4 README: MCP-servers line drops codebase-memory, fix28 note present x1",
      _readme.count("and the chrome-devtools and playwright MCP servers") == 1
      and "codebase-memory MCP servers" not in _readme)

# 10d. Install manifests (fix28 §2).
_mods = json.load(open(os.path.join(BASE, "manifests/install-modules.json"), encoding="utf-8"))
_mlist = _mods["modules"]
_mby_id = {m["id"]: m for m in _mlist}
_mpaths = [p for m in _mlist for p in m.get("paths", [])]
check("install-modules.json: 14 modules / 84 paths, skill-unified-memory + business-content gone",
      len(_mlist) == 14 and len(_mpaths) == 84
      and "skill-unified-memory" not in _mby_id
      and "business-content" not in _mby_id)
if len(_mlist) != 14 or len(_mpaths) != 84:
    print(f"   actual: {len(_mlist)} modules, {len(_mpaths)} paths")
check("install-modules.json: workflow-quality dependencies emptied to [] (key must stay: the installer iterates it unconditionally)",
      _mby_id.get("workflow-quality", {}).get("dependencies") == [])
check("install-modules.json: hackathon description no longer lists brainstorming",
      "brainstorming" not in _mby_id.get("hackathon", {}).get("description", ""))
_missing_paths = [p for p in _mpaths if not os.path.exists(os.path.join(BASE, p))]
if _missing_paths:
    print(f"   module paths missing on disk: {_missing_paths}")
check("install-modules.json: all 84 module paths exist on disk (no silent-skip dangles)",
      not _missing_paths)
_comps = json.load(open(os.path.join(BASE, "manifests/install-components.json"), encoding="utf-8"))
_clist = _comps["components"]
_cby_id = {c["id"]: c for c in _clist}
check("install-components.json: 55 components, skill:unified-memory + capability:content gone",
      len(_clist) == 55
      and "skill:unified-memory" not in _cby_id
      and "capability:content" not in _cby_id)
_bad_comp_refs = sorted({m for c in _clist for m in c.get("modules", []) if m not in _mby_id})
if _bad_comp_refs:
    print(f"   components referencing unknown modules: {_bad_comp_refs}")
check("install-components.json: every component module id exists in install-modules.json",
      not _bad_comp_refs)
_profs = json.load(open(os.path.join(BASE, "manifests/install-profiles.json"), encoding="utf-8"))
_plist = _profs["profiles"]
check("install-profiles.json: profiles is a name-keyed dict; research 7 / full 14 modules",
      isinstance(_plist, dict)
      and len(_plist.get("research", {}).get("modules", [])) == 7
      and len(_plist.get("full", {}).get("modules", [])) == 14)
check("install-profiles.json: business-content gone from research; skill-unified-memory + business-content gone from full",
      "business-content" not in _plist.get("research", {}).get("modules", [])
      and "skill-unified-memory" not in _plist.get("full", {}).get("modules", [])
      and "business-content" not in _plist.get("full", {}).get("modules", []))
check("install-profiles.json: research description reworded (no content-oriented publishing)",
      _plist.get("research", {}).get("description", "") == "Research-oriented setup for investigation and synthesis workflows.")
_bad_prof_refs = sorted({m for p in _plist.values() for m in p.get("modules", []) if m not in _mby_id})
if _bad_prof_refs:
    print(f"   profiles referencing unknown modules: {_bad_prof_refs}")
check("install-profiles.json: every profile module id exists in install-modules.json",
      not _bad_prof_refs)

# 10e. Dead scripts gone; deliberate keeps present; hooks + mcp.json.
_dead_present = [s for s in DEAD_SCRIPTS if os.path.exists(os.path.join(BASE, s))]
if _dead_present:
    print(f"   dead scripts still present: {_dead_present}")
check("all 135 dead scripts are ABSENT", not _dead_present)
check("deliberately kept orchestration files present (OWED-28-1, ORCHKEEP_F28)",
      os.path.exists(os.path.join(BASE, "scripts/lib/orchestration-session.js"))
      and os.path.exists(os.path.join(BASE, "scripts/lib/tmux-worktree-orchestrator.js")))
check("deliberately kept validate-skills.js present (documented CI tool)",
      os.path.exists(os.path.join(BASE, "scripts/ci/validate-skills.js")))
_hj = json.load(open(os.path.join(BASE, "hooks/hooks.json"), encoding="utf-8"))
check("hooks.json still registers 15 hook events; adapter.js present",
      len(_hj.get("hooks", {})) == 15
      and os.path.exists(os.path.join(BASE, "hooks/adapter.js")))
_mcp = json.load(open(os.path.join(BASE, "mcp.json"), encoding="utf-8"))
check("mcp.json: codebase-memory-mcp gone; chrome-devtools + playwright remain",
      "codebase-memory-mcp" not in _mcp.get("mcpServers", {})
      and "chrome-devtools" in _mcp.get("mcpServers", {})
      and "playwright" in _mcp.get("mcpServers", {}))

# 10f. resolveInstallPlan succeeds for every profile and the full
# component set (real installer code, read-only: it only computes the
# plan). Catches "Unknown install module/component" and dangling
# module dependencies that a structural check alone would miss.
# operations is [] without a target adapter (operations are built by
# createManifestInstallPlan per target), so the assertion is on
# selectedModuleIds: every profile module must be selected, and the
# component call must select something.
import tempfile as _tempfile
_js = (
    "const { resolveInstallPlan } = require("
    + json.dumps(os.path.join(BASE, "scripts/lib/install-manifests.js")) + ");\n"
    "const profiles = " + json.dumps(sorted(_plist.keys())) + ";\n"
    "const expected = " + json.dumps({k: v.get("modules", []) for k, v in _plist.items()}) + ";\n"
    "const components = " + json.dumps(sorted(_cby_id.keys())) + ";\n"
    "for (const p of profiles) {\n"
    "  const plan = resolveInstallPlan({ repoRoot: " + json.dumps(BASE)
    + ", profileId: p, projectRoot: '/tmp', homeDir: '/tmp' });\n"
    "  const sel = plan.selectedModuleIds || [];\n"
    "  const miss = expected[p].filter(m => !sel.includes(m));\n"
    "  if (miss.length) throw new Error('profile ' + p + ' missing modules: ' + miss.join(','));\n"
    "  console.log('profile ' + p + ' OK (' + sel.length + ' modules selected)');\n"
    "}\n"
    "const cplan = resolveInstallPlan({ repoRoot: " + json.dumps(BASE)
    + ", includeComponentIds: components, projectRoot: '/tmp', homeDir: '/tmp' });\n"
    "const csel = cplan.selectedModuleIds || [];\n"
    "if (!csel.length) throw new Error('no modules selected for components');\n"
    "console.log('components OK (' + csel.length + ' modules selected)');\n"
)
with _tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as _tf:
    _tf.write(_js)
    _jspath = _tf.name
try:
    _plan = subprocess.run(["node", _jspath], capture_output=True, text=True)
    if _plan.returncode != 0:
        print(f"   resolveInstallPlan failed: {_plan.stderr.strip()[:600]}")
    else:
        print("   " + _plan.stdout.strip().replace("\n", "\n   "))
finally:
    os.unlink(_jspath)
check("resolveInstallPlan succeeds for all 7 profiles + the full 55-component set",
      _plan.returncode == 0)

# 10g. Regenerated call map.
_cmap = read("skills/orchestrate/references/call-map.md")
check("call map regenerated for fix #28: Rules (48), counts table 48, zero '123'",
      "## Rules (48)" in _cmap
      and "| rules | 48 | 48 |" in _cmap
      and "123" not in _cmap
      and "fix #28" in _cmap)
_sidecar_dir = os.path.join(os.path.dirname(BASE.rstrip("/")), "fix28", "callmap")
_sidecar = os.path.join(_sidecar_dir, "call-map-data.json")
_sidecar_ok = False
if os.path.exists(_sidecar):
    _sd = json.load(open(_sidecar, encoding="utf-8"))
    _sidecar_ok = (_sd.get("counts") == {"skills": 72, "agents": 45, "rules": 48,
                                         "commands": 55, "hooks": 15, "triggers": 49}
                   and _sd.get("uncalled", {}).get("rules") == [])
check("call-map sidecar exists with counts 72/45/48/55/15/49 and 0 uncalled rules",
      _sidecar_ok)

# 10h. Audit #77 fixes (DARTSEC port, B1/B2/B3).
_rns = read("rules/react-native-security.mdc")
check("77-A1 DARTSEC port: manifest globs + Native Manifests section + network bullets present (DARTSEC_F28)",
      _rns.count('  - "**/AndroidManifest.xml"') == 1
      and _rns.count('  - "**/Info.plist"') == 1
      and _rns.count("## Native Manifests (AndroidManifest.xml / Info.plist)") == 1
      and _rns.count("DARTSEC_F28") == 1
      and 'android:exported="false"' in _rns
      and "FLAG_SECURE" in _rns
      and "NSAppTransportSecurity" in _rns
      and "network_security_config.xml" in _rns
      and "Set request timeouts on all HTTP clients — never leave defaults." in _rns
      and "Review intent filters" in _rns
      and "Enable data protection entitlement for sensitive files." in _rns)
check("77-B1: no run-with-flags.js caller comment remains in live hook files",
      "run-with-flags" not in read("scripts/hooks/block-no-verify.js")
      and "run-with-flags" not in read("scripts/hooks/post-edit-format.js")
      and "run-with-flags" not in read("scripts/hooks/quality-gate.js")
      and "run-with-flags" not in read("scripts/hooks/stop-format-typecheck.js"))
check("77-B2: capsule-envelope schema no longer names the cut envelope.js as enforcing",
      "envelope.js" not in read("schemas/capsule-envelope.schema.json")
      and read("schemas/capsule-envelope.schema.json").count("One append-only journal entry recorded by the ECC eval-harness capsule.") == 1)
_eval2 = read("scripts/hooks/evaluate-session.js")
check("77-B3: dead path/readFile imports gone, header + log prefix retitled",
      "require('path')" not in _eval2
      and "readFile" not in _eval2
      and "Continuous Learning - Session Evaluator" not in _eval2
      and "[ContinuousLearning]" not in _eval2
      and _eval2.count(" * Session Evaluator") == 1
      and _eval2.count("[SessionEvaluator]") == 2)

# 10i. [29] fix29.py patch anchors still present exactly once.
_op = read("skills/orch-pipeline/SKILL.md")
# Audit #92-B1: the opening-clause-only check left the paragraph body
# unasserted — deleting the COST-AWARE or VERIFY-MERGE sentence left
# verify29 green (orch-pipeline is ECC-origin, outside 7e). Assert the
# full paragraph line (87-B1 pattern).
check("orch-pipeline factory paragraph present in full x1 (GLOBAL-ROUTING_F29, audit #92-B1)",
      _op.count("**Factory routing (fix #29, GLOBAL-ROUTING_F29):** every phase dispatches through the factory — the orchestrator's queue of independent single-task jobs, one drone per job, retired on completion, the next queued job dispatched into the freed slot (in Cursor, slots refill per wave, not per completion — the factory lights up fully on the later port, not in Cursor) (FACTORY-DISPATCH_F29). Every drone brief is a director brief (DIRECTOR-BRIEF_F29): the exact goal, the files in scope and explicitly out of scope, constraints, acceptance criteria, verification steps, and what to return — an incomplete brief means the drone does not start. Briefs follow the seven-field contract in `skills/orchestrate/references/dispatch-prompt.md`. A drone that hits a decision its brief leaves unspecified stops and returns the question to the orchestrator instead of guessing (NO-GUESSING_F29). The orchestrator verifies every drone output against the brief's acceptance criteria and sends failed output back with a correction brief (VERIFY-MERGE_F29); fan-out is bounded by efficiency, N>3 justified in one line, drones carrying minimal context (COST-AWARE_F29). The orchestrator answers every prompt; drones never answer the user or decide scope (ORCHESTRATOR-ONLY_F29).") == 1)
check("orch-pipeline NO-GUESSING carve-out present x1",
      _op.count("**Bounded by NO-GUESSING (fix #29, NO-GUESSING_F29):**") == 1)
check("orch-pipeline briefs follow the seven-field contract (audit #80-B6, #90-B4)",
      _para_with(_op, "**Factory routing (fix #29, GLOBAL-ROUTING_F29):** every phase dispatches through the factory").count("Briefs follow the seven-field contract in `skills/orchestrate/references/dispatch-prompt.md`") == 1)
check("orch-pipeline Review correction-brief sentence present x1 (audit #80-B8)",
      _op.count("the re-dispatch carries a correction brief naming the failed acceptance criterion and the required correction, distinct from the original brief") == 1)
# Full wrapper pointer (audit #80-B11: the run-1 check matched only the
# prefix; audit #80-B14: the pointer now states the COST-AWARE rules).
_WRAPPER_POINTER = ("**Factory routing (fix #29, GLOBAL-ROUTING_F29):** this operation runs "
                    "through the shared `orch-pipeline` engine, which dispatches all "
                    "implementation work through the factory — see `orch-pipeline` for the "
                    "routing (task queue, single-task drones, director briefs, no-guessing, "
                    "verify-and-merge, cost-aware fan-out). Fan-out is bounded by efficiency: "
                    "N>3 justified in one line; drones carry minimal context. The orchestrator "
                    "answers every prompt; drones never answer the user or decide scope "
                    "(ORCHESTRATOR-ONLY_F29).")
for _w in ("orch-build-mvp", "orch-add-feature", "orch-change-feature",
           "orch-fix-defect", "orch-refine-code"):
    _wt = read(f"skills/{_w}/SKILL.md")
    # Audit #91-B4: whole-file counts were proxies — moving the pointer
    # to EOF left verify29 green. Scope each to the header block: the
    # pointer attaches to the thin-wrapper intro above "## When to Use"
    # (first ## heading at :17 in orch-build-mvp, :15 in the other four;
    # the pointer is at :13 in all five).
    _wt_head = _wt[:_wt.index("## When to Use")]
    check(f"{_w} factory pointer present in full x1 in header block (GLOBAL-ROUTING_F29, audit #91-B4)",
          _wt_head.count(_WRAPPER_POINTER) == 1)
_gan = read("skills/gan-style-harness/SKILL.md")
# Audit #92-B1: same opening-clause-only gap as orch-pipeline — deleting
# the COST-AWARE, NO-GUESSING, or VERIFY-MERGE sentence left verify29
# green (gan-style-harness is ECC-origin, outside 7e). Assert the full
# paragraph line (87-B1 pattern).
check("gan-style-harness factory paragraph present in full x1 (GLOBAL-ROUTING_F29, audit #92-B1)",
      _gan.count("**Factory routing (fix #29, GLOBAL-ROUTING_F29):** the generator/evaluator loop runs as factory drones — the orchestrator dispatches each generator and evaluator pass as a single-task drone from its queue, with a director brief (DIRECTOR-BRIEF_F29): the exact goal, the files in scope and explicitly out of scope, constraints, acceptance criteria, verification steps, and what to return — an incomplete brief means the drone does not start. Generator and evaluator briefs follow the seven-field contract in `skills/orchestrate/references/dispatch-prompt.md`. A drone that hits a decision its brief leaves unspecified stops and returns the question to the orchestrator instead of guessing (NO-GUESSING_F29). The evaluator pass is an input to verification, not the verify step itself: after each evaluator pass the orchestrator checks the generator's output against the brief's acceptance criteria (not just the rubric score — a rubric pass at or above 7.0 with a failed acceptance criterion is a fail), re-checks the evaluator's pass/fail call against the same criteria, and checks the planner's spec against the brief before the first generator pass; failed output goes back with a correction brief naming the failed criterion (VERIFY-MERGE_F29). Fan-out is bounded by efficiency, N>3 justified in one line, drones carrying minimal context (COST-AWARE_F29); in Cursor, slots refill per wave, not per completion — the factory lights up fully on the later port, not in Cursor (GLOBAL-ROUTING_F29). The orchestrator answers every prompt; drones never answer the user or decide scope (ORCHESTRATOR-ONLY_F29).") == 1)
check("gan-style-harness evaluator is an input to verification, not the verify step (audit #80-B2)",
      _gan.count("The evaluator pass is an input to verification, not the verify step itself") == 1)
check("gan-style-harness old evaluator-is-verify substitution is gone",
      _gan.count("The evaluator pass IS the verify step for GAN work") == 0)
check("gan-style-harness orchestrator re-checks the evaluator pass/fail call",
      _gan.count("re-checks the evaluator's pass/fail call against the same criteria") == 1)
check("gan-style-harness orchestrator checks the planner spec before the first generator pass",
      _gan.count("checks the planner's spec against the brief before the first generator pass") == 1)
# Audit #90-B3: the bare == 3 count was a proxy (89-B4 shape) — moving a
# mirror line out of its section left verify29 green. Assert per-site
# presence instead: factory paragraph, Architecture note, Scoring bullet.
_GAN_RP = "a rubric pass at or above 7.0 with a failed acceptance criterion is a fail"
check("gan-style-harness rubric-pass rule in factory paragraph (audit #90-B3)",
      _GAN_RP in _para_with(_gan, "**Factory routing (fix #29, GLOBAL-ROUTING_F29):** the generator/evaluator loop runs as factory drones"))
check("gan-style-harness rubric-pass rule in Architecture note (audit #90-B3)",
      _GAN_RP in _gan[_gan.index("## Architecture"):_gan.index("## The Three Agents")])
check("gan-style-harness rubric-pass rule in Scoring bullet (audit #90-B3)",
      _GAN_RP in _gan[_gan.index("### Scoring"):_gan.index("## Usage")])
# The three sites (audit #81-B2 mirror): the factory paragraph, the
# Architecture orchestrator-check note, and the Scoring bullet — the
# run-2 check asserted == 1 when only the paragraph carried it.
check("gan-style-harness briefs follow the seven-field contract (audit #80-B6, #90-B4)",
      _para_with(_gan, "**Factory routing (fix #29, GLOBAL-ROUTING_F29):** the generator/evaluator loop runs as factory drones").count("Generator and evaluator briefs follow the seven-field contract in `skills/orchestrate/references/dispatch-prompt.md`") == 1)
# Audit #81-B2: the orchestrator check mirrored in the skill's loop
# wiring (diagram note + Scoring bullet), not only in the paragraph.
check("gan-style-harness loop wiring carries the orchestrator-check note (audit #81-B2, #90-B3)",
      _gan[_gan.index("## Architecture"):_gan.index("## The Three Agents")].count("**Orchestrator check (fix #29, VERIFY-MERGE_F29):** the orchestrator sits outside the loop") == 1)
check("gan-style-harness Scoring carries the orchestrator-check bullet (audit #81-B2, #90-B3)",
      _gan[_gan.index("### Scoring"):_gan.index("## Usage")].count("- **Orchestrator check** — after each evaluator pass the orchestrator checks the generator's output") == 1)
_fe = read("skills/feature-expansion/SKILL.md")
check("feature-expansion Phase 4 factory paragraph present x1 (GLOBAL-ROUTING_F29)",
      _fe.count("**Factory routing (fix #29, GLOBAL-ROUTING_F29).** Phase 4 implementers are factory drones") == 1)
check("feature-expansion NO-GUESSING carve-out present x1",
      _fe.count("**Bounded by NO-GUESSING (fix #29, NO-GUESSING_F29):**") == 1)
# §5 patches (audit #80-A3/A4/A5/A6/B4/B7).
_obm = read("skills/orch-build-mvp/SKILL.md")
check("orch-build-mvp NO-GUESSING carve-out present x1 (third Belief copy)",
      _obm.count("**Bounded by NO-GUESSING (fix #29, NO-GUESSING_F29):**") == 1)
check("orch-build-mvp merge-order bridge present x1 in step 5 Reconcile (audit #89-B2)",
      _obm[_obm.index("5. **Reconcile after each wave"):_obm.index("6. **Verify")].count("This procedure applies only if partitioning failed and two implementers touched the same file anyway") == 1)
_orc = read("skills/orch-refine-code/SKILL.md")
# Audit #90-B6: whole-file count was a proxy — moving the qualification
# out of step 2 left verify29 green. Scope to step 2 (89-B2 MVP pattern:
# line-slice, since the step list is not blank-line delimited).
_orc_step2 = _orc[_orc.index("2. For dead-code"):_orc.index("3. Stop at **Gate 1**")]
check("orch-refine-code step-2 refactor-cleaner sweep is a factory drone (audit #80-A4, #90-B6)",
      _orc_step2.count("Dispatched as a single-task factory drone with a director brief (goal, files in/out of scope, constraints, acceptance criteria, verification steps, what to return; GLOBAL-ROUTING_F29)") == 1)
# Audit #81-A4: the pointer itself claimed ALL work runs "through the
# engine" while step 2 concedes the sweep applies "not only through the
# engine" — the exception is appended after the shared pointer text, so
# the full-pointer assertion above still matches.
# Audit #92-B3: whole-file count was a proxy — moving the exception to EOF
# left verify29 green, silently restoring the 81-A4 overclaim. Scope to
# the header block (91-B4 pattern: the exception qualifies the pointer on
# the :13 line, inside the header).
_orc_head = _orc[:_orc.index("## When to Use")]
check("orch-refine-code pointer qualified with the step-2 exception (audit #81-A4, #92-B3)",
      _orc_head.count("Except the step-2 refactor-cleaner sweep, which is dispatched directly as a single-task factory drone — see step 2.") == 1)
_orcc = read("commands/orch-refine-code.md")
# Audit #90-B6: the command mirror is the same whole-file shape on step 3.
_orcc_step3 = _orcc[_orcc.index("3. Restructure in small steps"):_orcc.index("4. `code-reviewer`, then commit")]
check("commands/orch-refine-code.md step-3 refactor-cleaner sweep is a factory drone (audit #90-B6)",
      _orcc_step3.count("dispatched as a single-task factory drone with a director brief (GLOBAL-ROUTING_F29)") == 1)
# Audit #92-B3: whole-file count was a proxy — moving the mirror exception
# to EOF left verify29 green. Scope to the "## What It Does" intro span
# that carries :26 (the exception qualifies the engine-routing sentence
# there, not step 3).
_orcc_intro = _orcc[_orcc.index("## What It Does"):_orcc.index("1. Classify size")]
check("commands/orch-refine-code.md mirror qualified with the step-3 exception (audit #81-A4, #92-B3)",
      _orcc_intro.count("except the step-3 refactor-cleaner sweep, which the skill dispatches directly as a single-task factory drone") == 1)
_ca = read("rules/common-agents.mdc")
# Audit #90-B5: whole-file counts were proxies — a pointer's function is
# adjacency to the dispatch it qualifies, and moving it to EOF left
# verify29 green. Scope each pointer to its operative span.
_ca_imm = _ca[_ca.index("## Immediate Agent Usage"):_ca.index("## If a named agent does not resolve")]
# Audit #91-B8: the check asserted only the lead clause of the :26 line —
# deleting the operative middle (director brief / no-guessing /
# orchestrator verification) left verify29 green. Assert the full line
# in _ca_imm (87-B1 pattern); the COST-AWARE check below stays as
# defense-in-depth.
check("common-agents.mdc carries the factory routing line in full (audit #80-A5, #90-B5, #91-B8)",
      _ca_imm.count("Implementation-agent dispatch follows the factory routing in orchestrate's GLOBAL-ROUTING block (fix #29, GLOBAL-ROUTING_F29): every implementation dispatch carries a director brief, no-guessing applies, and the orchestrator verifies the output against the brief's acceptance criteria before use. Fan-out is bounded by efficiency: N>3 justified in one line; drones carry minimal context.") == 1)
# Audit #81-A6: the 80-B14 COST-AWARE standard (state both rules, not
# just the name) applied to the two newer pointers.
check("common-agents.mdc factory line states the COST-AWARE rules (audit #81-A6, #90-B5)",
      _ca_imm.count("Fan-out is bounded by efficiency: N>3 justified in one line; drones carry minimal context.") == 1)
_gb = read("commands/gan-build.md")
# Audit #89-B1: the _gen slice is defined here (not below the 82-B1
# checks) so the 81-A7 out-of-scope check can use it too.
_gen = _gb[_gb.index("# GENERATE"):_gb.index("# Wait for generator")]
# Audit #90-B5: scope the pointer to the header/arg-parse block it sits in.
_gb_head = _gb[:_gb.index("## GAN-Style Harness Build")]
# Audit #91-B6: the check asserted only a fragment of the :12 pointer —
# deleting the director-brief / no-guessing / orchestrator-verification
# middle left verify29 green. Assert the full pointer line in _gb_head
# (87-B1 pattern); the COST-AWARE check below stays as defense-in-depth.
check("commands/gan-build.md carries the factory routing pointer in full (audit #80-A6, #90-B5, #91-B6)",
      _gb_head.count("**Factory routing (fix #29, GLOBAL-ROUTING_F29):** the planner, generator, and evaluator passes below run as factory drones per `gan-style-harness` — each with a director brief (goal, files in/out of scope, constraints, acceptance criteria, verification steps, what to return), no-guessing, and orchestrator verification against the brief's acceptance criteria (a rubric pass with a failed acceptance criterion is a fail). Fan-out is bounded by efficiency: N>3 justified in one line; drones carry minimal context.") == 1)
check("commands/gan-build.md pointer states the COST-AWARE rules (audit #81-A6, #90-B5)",
      _gb_head.count("Fan-out is bounded by efficiency: N>3 justified in one line; drones carry minimal context.") == 1)
# Audit #91-B1: the gan-build step-0 inline-invocation pin (82-A1) had NO
# check at all — deleting the parenthetical from :26 left verify29 green.
# Scope to step 0 (mirroring the gan-design check, 91-B2).
_gb_step0 = _gb[_gb.index("0. Design-direction check"):_gb.index("1. Launch the `gan-planner`")]
check("commands/gan-build.md step 0 carries the inline design-lead pin (audit #82-A1, #91-B1)",
      _gb_step0.count("(the design-lead is invoked inline as the orchestrator here, not spawned as a drone — a spawned execution must carry a director brief)") == 1)
# Audit #81-A7: the out-of-scope line pointed at "the brief", but the
# only brief in the command is the user's one-line description — the
# orchestrator names the files from the spec before launch.
check("commands/gan-build.md generator block names files out of scope (audit #89-B1)",
      _gen.count("Files out of scope: [named by the orchestrator from the spec before launch; `none` if genuinely none]") == 1)
# Audit #81-B2: the executed loop wiring — the ORCHESTRATOR-CHECK step
# between EVALUATE and CHECK SCORE, the planner-spec check at the end of
# Phase 1, and the CHECK SCORE gate note.
check("commands/gan-build.md Phase 2 has the ORCHESTRATOR-CHECK step (audit #81-B2)",
      _gb.count("# ORCHESTRATOR-CHECK") == 1)
# Audit #92-B2: the header-only check proved the step exists, not that it
# does anything — deleting the whole body line left verify29 green. Assert
# the body line (verdict against acceptance criteria + correction-brief
# re-dispatch) inside the EVALUATE → CHECK SCORE span (82-B2 pattern).
_gb_loop = _gb[_gb.index("# EVALUATE"):_gb.index("# CHECK SCORE")]
check("commands/gan-build.md ORCHESTRATOR-CHECK body verifies against acceptance criteria (audit #81-B2, #92-B2)",
      _gb_loop.count("    After each evaluator pass, the orchestrator checks the generator's output against the brief's acceptance criteria (not just the rubric score — a rubric pass at or above 7.0 with a failed acceptance criterion is a fail) and re-checks the evaluator's pass/fail call against the same criteria. A rubric pass with a failed acceptance criterion is a fail: the generator is re-dispatched with a correction brief naming the failed criterion and the required correction, distinct from the original brief — the re-dispatch is the next iteration's GENERATE, consuming one iteration within max_iterations; skip CHECK SCORE and continue the loop. A rubric fail the orchestrator finds actually passes the criteria is a re-check, not a loop exit: the evaluator's call is corrected and the loop continues to CHECK SCORE.") == 1)
# Audit #91-B3: whole-file count was a proxy — moving the 3a line to EOF
# left verify29 green (the `3a.` label travels with the line, so the
# 82-B2 "label pins it" note does not hold). Scope to Phase 1.
_gb_ph1 = _gb[_gb.index("### Phase 1: Planning (Planner Agent)"):_gb.index("### Phase 2: Generator-Evaluator Loop")]
# Audit #93-B1: the check asserted only the ~90-char lead of the 616-char
# line — deleting the match criteria or the failure-path sentence left
# verify29 green, leaving the planner's correction-brief path (one of
# the eight VERIFY-MERGE sites) unguarded. Assert the full :30 line in
# _gb_ph1 (87-B1 pattern, as the 92-B2 fix did for the OC body line).
check("commands/gan-build.md Phase 1 has the planner-spec check in full (audit #81-B2, #91-B3, #93-B1)",
      _gb_ph1.count("3a. Orchestrator checks the planner's spec against the brief before Phase 2 (on the `--skip-planner` path, against the existing `gan-harness/spec.md`): the spec's files, scope, and acceptance criteria must match the brief's goal, files in/out of scope, constraints, and acceptance criteria. If the spec fails the check, the planner is re-dispatched with a correction brief naming the failed criterion and the required correction, distinct from the original brief (at most two correction re-dispatches, per the plugin's 2-round fix-loop convention; if the spec still fails, stop and report the failure with evidence).") == 1)
check("commands/gan-build.md CHECK SCORE runs only after the orchestrator check (audit #81-B2)",
      _gb.count("# CHECK SCORE — runs only after the orchestrator check above passes") == 1)
# Audit #82-B2: the wiring checks above assert presence, not order — a
# later edit could move ORCHESTRATOR-CHECK below CHECK SCORE (where it
# would be dead code, re-introducing the exact 81-B2 failure mode) and
# still pass. The order is the property that matters, so it is asserted.
check("ORCHESTRATOR-CHECK sits between EVALUATE and CHECK SCORE (audit #82-B2)",
      _gb.index("# EVALUATE") < _gb.index("# ORCHESTRATOR-CHECK") < _gb.index("# CHECK SCORE"))
# Audit #82-B1: the GENERATE block is the generator's only dispatch text
# and was 5/7 as a standalone brief — both missing slots are now lines
# in the block, mirroring the mechanical template's return format.
# Audit #83-B1: the run-4 checks asserted whole-file presence, not
# in-block position, and the Verification-steps check was prefix-only —
# both are scoped to the GENERATE slice here, and the full line (through
# the pass condition) is asserted.
check("commands/gan-build.md generator block carries Verification steps (audit #82-B1)",
      _gen.count("    - Verification steps: run the TDD tests you wrote plus the acceptance criteria from the spec — paste the test output; the build must pass and the acceptance criteria must hold before finishing.") == 1)
check("commands/gan-build.md generator block carries Return format (audit #82-B1)",
      _gen.count("    - Return format: Status first, then files changed, test output, concerns.") == 1)
# Audit #83-A1: gan-design.md carries the twin step-0 design-direction
# dispatch — same inline pin as gan-build step 0.
_gd = read("commands/gan-design.md")
# Audit #91-B2: whole-file count was a proxy — moving the parenthetical
# to EOF left verify29 green. Scope to step 0 (91-B1 sibling pattern).
_gd_step0 = _gd[_gd.index("0. Design-direction check"):_gd.index("1. Create `gan-harness/`")]
check("commands/gan-design.md step-0 carries the inline design-lead pin (audit #83-A1, #91-B2)",
      _gd_step0.count("(the design-lead is invoked inline as the orchestrator here, not spawned as a drone — a spawned execution must carry a director brief)") == 1)
# Audit #84-A1: the 83-A1 fix added the parenthetical but no _F29 token —
# the file still grepped as uncovered. The pointer below mirrors
# gan-build.md:12 (step-0 inline reading named, loop defers to gan-build).
# Audit #90-B5: scope the pointer to the header/arg-parse block it sits in.
_gd_head = _gd[:_gd.index("## GAN-Style Design Harness")]
# Audit #91-B7: the check asserted only the pointer's prefix — deleting
# the loop clause (factory drones per /gan-build, director brief,
# no-guessing, orchestrator verification) left verify29 green. Assert
# the full pointer line in _gd_head (87-B1 pattern).
check("commands/gan-design.md carries the factory routing pointer in full (audit #84-A1, #90-B5, #91-B7)",
      _gd_head.count("**Factory routing (fix #29, GLOBAL-ROUTING_F29):** the design-lead is invoked inline as the orchestrator in Setup step 0 (not spawned as a drone — a spawned execution must carry a director brief); the generator/evaluator loop below runs as factory drones per the `/gan-build` pointer, each with a director brief (goal, files in/out of scope, constraints, acceptance criteria, verification steps, what to return), no-guessing, and orchestrator verification against the brief's acceptance criteria.") == 1)
check("commands/gan-design.md carries a _F29 token (audit #84-A1)",
      "_F29" in _gd)
# Audit #86-A1: react-build.md dispatches the file-writing
# react-build-resolver agent with no routing coverage — "invokes" is not
# in the base-pattern grep set, so it escaped rounds 1-6 (same escape
# class as 83-A1). Pointer mirrors gan-build.md:12.
# Audit #87-B1: the round-8 check asserted only the pointer's prefix, so
# the verification sentence itself was unasserted — and the pointer's
# claim was false until step 6 existed. The pointer is now asserted in
# full, and step 6 (the orchestrator verify step + correction-brief path)
# is asserted by its full text.
_rb = read("commands/react-build.md")
# Audit #90-B5: scope the pointer to the invocation + pointer block above
# the procedure (88-B1 precedent: the step-6 check is procedure-scoped;
# the pointer it guards was never scoped).
_rb_head = _rb[:_rb.index("## What This Command Does")]
check("commands/react-build.md carries the factory routing pointer in full (audit #86-A1, #87-B1, #90-B5)",
      _rb_head.count("**Factory routing (fix #29, GLOBAL-ROUTING_F29):** the react-build-resolver runs as a single-task factory drone with a director brief (goal, files in/out of scope, constraints, acceptance criteria, verification steps, what to return), no-guessing, and orchestrator verification against the brief's acceptance criteria (the re-run build is evidence, not the verdict). Fan-out is bounded by efficiency: N>3 justified in one line; drones carry minimal context.") == 1)
# Audit #88-B1: whole-file count was a proxy — moving step 6 out of the
# procedure (to EOF) left verify29 green. Scope the assertion to the
# procedure section (83-B1 pattern: slice, then assert inside the slice).
_rb_proc = _rb[_rb.index("## What This Command Does"):_rb.index("## When to Use")]
check("commands/react-build.md carries the orchestrator verify step (audit #87-B1, #88-B1)",
      _rb_proc.count("6. **Orchestrator Verify**: After the resolver reports, the commanding agent verifies the resolver's output against the brief's acceptance criteria — the build is green AND the changes are minimal in scope AND no suppression (`// @ts-ignore`, disabled type-checking) lacks an explanation. A green build with a failed acceptance criterion is a fail. On a failed criterion, re-dispatch the resolver with a correction brief naming the failed acceptance criterion and the required correction, distinct from the original brief (at most two correction re-dispatches; past that, report the remaining issue as blocked with evidence).") == 1)
check("commands/react-build.md carries a _F29 token (audit #86-A1)",
      "_F29" in _rb)
# Audit #90-A1: astra-review.md dispatches implementation work in its
# Step 3 fix cycle with zero _F29 coverage — "Fixes go to X" is a
# role-routing sentence with no dispatch verb (new escape class in the
# 83-A1/86-A1 family). Pointer mirrors react-build.md:9; the :33 second
# blind pass is extended to name the fix brief's acceptance criteria
# (87-B1 lesson) and to construct the correction brief (eighth site).
# The pointer + :33 checks are scoped to Step 3 (90-B5 pattern — a new
# pointer check written in this round follows it).
_ar = read("commands/astra-review.md")
_ar_step3 = _ar[_ar.index("## Step 3: Fix cycle"):_ar.index("## Verdict")]
check("commands/astra-review.md carries the factory routing pointer in full (audit #90-A1)",
      _ar_step3.count("**Factory routing (fix #29, GLOBAL-ROUTING_F29):** the fast-worker/deep-reasoner fix runs as a single-task factory drone with a director brief (goal, files in/out of scope, constraints, acceptance criteria, verification steps, what to return), no-guessing, and orchestrator verification against the brief's acceptance criteria (the second blind pass is the verification — a zero-blocker verdict with a failed acceptance criterion is a fail). Fan-out is bounded by efficiency: N>3 justified in one line; drones carry minimal context.") == 1)
check("commands/astra-review.md second blind pass verifies against the fix brief's acceptance criteria (audit #90-A1)",
      _ar_step3.count("- After fixes, run a **second blind deep-reasoner pass** over the fixed diff to re-verify against the fix brief's acceptance criteria (the second-pass pattern replaces any second-model peer review; a zero-blocker verdict with a failed acceptance criterion is a fail). On a failed criterion, re-dispatch the fixer with a correction brief naming the failed acceptance criterion and the required correction, distinct from the original brief (at most two correction re-dispatches; past that, report the remaining issue as blocked with evidence).") == 1)
check("commands/astra-review.md carries a _F29 token (audit #90-A1)",
      "_F29" in _ar)
# Audit #83-A2: the planner fallback is re-routed — the planner drone
# returns the missing direction to the orchestrator instead of invoking
# the design-lead itself (a drone cannot execute the inline reading).
_gp = read("agents/ecc-gan-planner.md")
# Audit #92-B4: whole-file `in` was a proxy — moving the sentence out of
# the Direction-source bracket to EOF left verify29 green (deletion is
# caught; position is not). Scope to the Direction-source line itself
# (line-content pattern: the sentence and the slot share line :44, so
# co-location is the property that matters).
_gp_dir_lines = [ln for ln in _gp.splitlines() if "**Direction source**" in ln]
check("agents/ecc-gan-planner.md fallback returns the missing direction to the orchestrator (audit #83-A2, #92-B4)",
      len(_gp_dir_lines) == 1 and "STOP and return NEEDS_CONTEXT naming the missing direction to the orchestrator instead of invoking the design-lead itself" in _gp_dir_lines[0])
check("agents/ecc-gan-planner.md no longer instructs the planner to invoke the design-lead (audit #83-A2)",
      "invoke the design-lead (model `grok-4.7-extra-high`) to generate it" not in _gp)

# 11. fix28 patch log (written next to the tree under test: the real
# fix28/ dir for the default tree, the scratch fix28/ dir for a scratch
# tree — fix28.py derives the same path from BASE). Also asserts the
# three _F28 tokens that live only in the log (REACTA11Y, NDMISFIRE,
# ORCHKEEP); README48_F28 lives in the README note (check 7b).
_log_dir = os.path.join(os.path.dirname(BASE.rstrip("/")), "fix28")
_log_path = os.path.join(_log_dir, "fix28-patch-log.md")
_log_ok = False
_log_text = ""
if os.path.exists(_log_path):
    _log_text = open(_log_path, encoding="utf-8").read()
    _log_ok = ("## Errors (0)" in _log_text
               and "rules cut: 123 -> 48" in _log_text
               and "dead scripts removed: 135 files" in _log_text)
check("fix28/fix28-patch-log.md exists with 0 errors, 75 rules and 135 scripts accounted for",
      _log_ok)
check("patch-log _F28 tokens present (REACTA11Y, NDMISFIRE, ORCHKEEP)",
      all(t in _log_text for t in ("REACTA11Y_F28",
                                   "NDMISFIRE_F28", "ORCHKEEP_F28")))

# 11b. [29] fix29 patch log (same derivation as check 11, fix29/ dir).
_log29_dir = os.path.join(os.path.dirname(BASE.rstrip("/")), "fix29")
_log29_path = os.path.join(_log29_dir, "fix29-patch-log.md")
_log29_ok = False
_log29_text = ""
if os.path.exists(_log29_path):
    _log29_text = open(_log29_path, encoding="utf-8").read()
    _log29_ok = ("## Errors (0)" in _log29_text
                 and "census: GLOBAL-ROUTING block byte-identical" in _log29_text
                 and "all 10 in-scope skills" in _log29_text)
check("fix29/fix29-patch-log.md exists with 0 errors and the census line (all 10 in-scope skills)",
      _log29_ok)

# 12. CUT-name sweep (audit #74 M10, extended in fix #28 to the 75 CUT
# rule basenames): every CUT skill/agent/command/rule name must occur
# zero times as a live
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
_CUT_NAMES = (CUT_SKILLS + REMOVED_AGENTS + DROPPED_COMMANDS
              + [r[:-4] for r in CUT_RULES])  # rule basenames w/o .mdc
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
        192: "prose-history: 'brainstorming skill is NOT invoked' (REROUTE_F27)",
        194: "prose-history: 'dispatching-parallel-agents was cut' (REROUTE_F27)",
        196: "prose-history: 'code-tour was cut' (REROUTE_F27)",
        197: "prose-history: 'intent-driven-development was cut' (REROUTE_F27)",
        208: "prose-history: 'agent-self-evaluation was cut' (REROUTE_F27)",
        215: "attribution to upstream brainstorming techniques source, not a dispatch",
    },
    "skills/orchestrate/SKILL.md": {
        137: "prose-history: 'ecc-recipes was cut' (REROUTE_F27)",
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
    "rules/react-native-security.mdc": {
        47: "prose-history: 'Ported from the cut `dart-security` rule' (DARTSEC_F28 port note)",
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
        47: {
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

# 13. [30] fix30 patch log (written next to the tree under test: the real
# fix30/ dir for the default tree, the scratch fix30/ dir for a scratch
# tree — fix30.py derives the same path from BASE). Asserts the census
# (49 ID + 22 prose replaced, fast-worker pin unchanged at 70) and 0 errors.
_log30_dir = os.path.join(os.path.dirname(BASE.rstrip("/")), "fix30")
_log30_path = os.path.join(_log30_dir, "fix30-patch-log.md")
_log30_ok = False
_log30_text = ""
if os.path.exists(_log30_path):
    _log30_text = open(_log30_path, encoding="utf-8").read()
    _log30_ok = ("## Errors (0)" in _log30_text
                 and "grok-4.7-high x49" in _log30_text
                 and "'Grok 4.7 High' x22" in _log30_text
                 and "cursor-grok-4.6-high-fast x70" in _log30_text
                 and "grok-4.7-extra-high x49" in _log30_text)
check("fix30/fix30-patch-log.md exists with 0 errors, 49 ID + 22 prose renamed, fast-worker pin unchanged at 70",
      _log30_ok)


# 14. [31] Fix #31 design libraries.
_NEW31 = ("getlayers", "gsap", "react-bits", "hairline-create", "hairline-adopt")
for _s in _NEW31:
    _f31 = os.path.join(BASE, "skills", _s, "SKILL.md")
    check(f"fix31 skill {_s} exists with SKILL.md", os.path.exists(_f31))
    if os.path.exists(_f31):
        _t31 = open(_f31, encoding="utf-8").read()
        check(f"fix31 skill {_s} frontmatter names {_s}",
              _t31.startswith("---\nname: " + _s + "\n"))
        check(f"fix31 skill {_s} carries no model pin text",
              "grok-4.7-high" not in _t31 and "grok-4.7-extra-high" not in _t31
              and "Grok 4.7 High" not in _t31 and "Grok 4.7 Extra High" not in _t31)
# _F31 tokens exist in the built tree and live in their skills.
for _tok in ("GETLAYERS_F31", "GSAP_F31", "REACTBITS_F31", "HAIRLINE_F31"):
    check(f"fix31 anchor token {_tok} exists in the built tree",
          count_in_tree(_tok) + _readme.count(_tok) > 0)
check("fix31 token GETLAYERS_F31 is in skills/getlayers/SKILL.md",
      "GETLAYERS_F31" in read("skills/getlayers/SKILL.md"))
check("fix31 token GSAP_F31 is in skills/gsap/SKILL.md",
      "GSAP_F31" in read("skills/gsap/SKILL.md"))
check("fix31 token REACTBITS_F31 is in skills/react-bits/SKILL.md",
      "REACTBITS_F31" in read("skills/react-bits/SKILL.md"))
check("fix31 token HAIRLINE_F31 is in skills/hairline-create/SKILL.md",
      "HAIRLINE_F31" in read("skills/hairline-create/SKILL.md"))
check("fix31 token HAIRLINE_F31 is in skills/hairline-adopt/SKILL.md",
      "HAIRLINE_F31" in read("skills/hairline-adopt/SKILL.md"))
# DESIGNPKG-AUTO: byte-identical, names all five, carries the weight.
def _dpkg_block(text):
    _i = text.find("**DESIGNPKG-AUTO")
    if _i < 0:
        return None
    _j = text.find("\n", _i)
    return text[_i:_j] if _j > _i else text[_i:]
_dp1 = _dpkg_block(read("skills/orchestrate/SKILL.md"))
_dp2 = _dpkg_block(read("rules/hackathon-mode.mdc"))
check("DESIGNPKG-AUTO block is byte-identical in orchestrate + hackathon-mode",
      _dp1 is not None and _dp1 == _dp2)
for _s in _NEW31:
    check(f"DESIGNPKG-AUTO block names {_s}",
          _dp1 is not None and _s in _dp1)
check("DESIGNPKG-AUTO palette list starts with getlayers (weight: consulted FIRST)",
      _dp1 is not None and "`getlayers`, `motionsites-web-builder`" in _dp1)
check("DESIGNPKG-AUTO block carries the GetLayers priority sentence",
      _dp1 is not None and "consulted FIRST in the palette inventory" in _dp1)
check("DESIGNPKG-AUTO block carries the GetLayers citation sentence",
      _dp1 is not None and "GetLayers layers are cited the same way" in _dp1)
# Palette-first paragraph (design-taste-frontend).
_dtf31 = read("skills/design-taste-frontend/SKILL.md")
check("palette-first paragraph names getlayers FIRST",
      "`getlayers` FIRST" in _dtf31)
check("palette-first paragraph carries the GetLayers citation sentence",
      "GetLayers layers are cited the same way" in _dtf31)
for _s in _NEW31:
    check(f"palette-first paragraph names {_s}", _s in _dtf31)
# Inventory §12 + weight.
_inv31 = read("skills/orchestrate/references/design-inventory.md")
check("design-inventory has §12 (fix #31 additions)",
      "## 12. Fix #31 additions" in _inv31)
check("design-inventory §12 names the GetLayers weight (Consulted FIRST)",
      "Consulted FIRST in the palette inventory" in _inv31)
for _ref in ("skills/getlayers/SKILL.md", "skills/gsap/SKILL.md",
             "skills/react-bits/SKILL.md", "skills/hairline-create/SKILL.md",
             "skills/hairline-adopt/SKILL.md"):
    check(f"design-inventory §12 references {_ref}", _ref in _inv31)
check("orchestrate inventory paragraph names the fix #31 additions with GetLayers weight",
      "the fix #31 additions" in read("skills/orchestrate/SKILL.md")
      and "consulted FIRST in the palette inventory" in read("skills/orchestrate/SKILL.md"))
# GetLayers skill weight language + license.
_gl31 = read("skills/getlayers/SKILL.md")
check("getlayers skill carries the first-class weight language",
      "first-class, high-priority source" in _gl31
      and "consulted FIRST" in _gl31
      and "Priority in the palette-first flow" in _gl31)
check("getlayers skill invokes no getlayers_* MCP tools",
      "getlayers_start" not in _gl31 and "getlayers_search" not in _gl31
      and "getlayers_materialize" not in _gl31)
for _fig in ("50 templates", "114 WebGL", "276 backgrounds", "10 animated sections"):
    check(f"getlayers skill carries no frozen count {_fig!r}", _fig not in _gl31)
check("react-bits skill dir contains only SKILL.md (no embedded source)",
      sorted(os.listdir(os.path.join(BASE, "skills", "react-bits"))) == ["SKILL.md"])
check("gsap skill dir contains only SKILL.md (no vendored source)",
      sorted(os.listdir(os.path.join(BASE, "skills", "gsap"))) == ["SKILL.md"])
check("getlayers skill dir contains only SKILL.md (no vendored content)",
      sorted(os.listdir(os.path.join(BASE, "skills", "getlayers"))) == ["SKILL.md"])
check("hairline-create ships its engine + checks + LICENSE",
      all(os.path.exists(os.path.join(BASE, "skills", "hairline-create", _f))
          for _f in ("kernel.js", "bench.html", "build.mjs", "validate.mjs",
                     "examples/terrain.js", "LICENSE")))
check("hairline-adopt ships its LICENSE",
      os.path.exists(os.path.join(BASE, "skills", "hairline-adopt", "LICENSE")))
_gsap_vendored = []
for _root, _dirs, _files in os.walk(BASE):
    _dirs[:] = [d for d in _dirs if d != "node_modules"]
    for _fn in _files:
        if _fn.lower() in ("gsap.js", "gsap.min.js", "gsap.ts"):
            _gsap_vendored.append(os.path.join(_root, _fn))
if _gsap_vendored:
    print(f"   vendored GSAP source: {_gsap_vendored}")
check("no vendored GSAP source file (gsap.js / gsap.min.js / gsap.ts) in the built tree",
      not _gsap_vendored)
# README fix31 note.
check("README fix31 provenance note present with the four _F31 tokens",
      "Fix #31 design libraries" in _readme
      and all(_tok in _readme for _tok in ("GETLAYERS_F31", "GSAP_F31", "REACTBITS_F31", "HAIRLINE_F31")))
# fix31 patch log.
_log31_dir = os.path.join(os.path.dirname(BASE.rstrip("/")), "fix31")
_log31_path = os.path.join(_log31_dir, "fix31-patch-log.md")
_log31_ok = False
_log31_text = ""
if os.path.exists(_log31_path):
    _log31_text = open(_log31_path, encoding="utf-8").read()
    _log31_ok = ("## Errors (0)" in _log31_text
                 and "coverage.skills 67 -> 72" in _log31_text
                 and "README: fix31 provenance note added" in _log31_text)
check("fix31/fix31-patch-log.md exists with 0 errors, trigger 67 -> 72, README note added",
      _log31_ok)

failed = [n for n, ok in checks if not ok]
print(f"\n{len(checks) - len(failed)}/{len(checks)} checks pass")
sys.exit(1 if failed else 0)
