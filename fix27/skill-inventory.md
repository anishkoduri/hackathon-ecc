# Fix #27 — Skill inventory: all 166 skills, KEEP / CUT / REVIEW

Date: 2026-11-16. Read-only inventory worker. Method: read the `SKILL.md`
frontmatter (name + description) of every skill dir in
`~/workspace/hackathon-plugin/hackathon-ecc/skills/` (166 dirs confirmed by
`ls | wc -l`); read more of a SKILL.md only where the description left the
purpose unclear. Verdicts judged against the actual weekend-build stack:
Next.js/React + TypeScript frontend, FastAPI/Python backend, Supabase/Postgres,
plus demo video — and against the goal of a lean set that serves WINNING
hackathon projects.

## Summary counts

| Verdict | Count |
|---|---|
| KEEP | 64 |
| CUT | 91 |
| REVIEW | 11 |
| **Total** | **166** |

Cutting all 91 CUT skills would leave 64 kept + 11 under review = 75 skills
(55% smaller than 166). Cutting CUT + REVIEW would leave 64 skills (61% smaller).

## Reachability evidence (call map)

Source: `hackathon-ecc/skills/orchestrate/references/call-map.md` (fix #25 §1,
generated from the built tree + staged sources). Consistent with the fix #26
MANIFEST §Results counts cited in the task.

- **24 skills uncalled** (no dispatch path): `agents-md-generator`,
  `bengali-nlp`, `brownfield-retrospective`, `context-budget`, `dev-team`,
  `django-celery`, `generating-python-installer`, `i18n-sync`,
  `investor-materials`, `investor-outreach`, `kotlin-exposed-patterns`,
  `kotlin-ktor-patterns`, `laravel-plugin-discovery`, `laravel-verification`,
  `living-docs-governance`, `mybatis-patterns`, `quarkus-verification`,
  `repo-scan`, `rules-distill`, `springboot-verification`, `story-lifecycle`,
  `tinystruct-patterns`, `ui-to-vue`, `windows-desktop-e2e`.
- **8 skills are second-order orphans** (called only by an uncalled element, so
  the reference never fires): `django-tdd`, `django-verification`,
  `fsharp-testing`, `iterative-retrieval`, `laravel-tdd`, `mysql-patterns`,
  `rails-patterns`, `unified-memory`.
- **Overlap of the two lists with this report's CUT list: 23 of the 24
  uncalled skills are CUT here, and all 8 orphan skills are CUT here.**
  The single exception is `context-budget` (uncalled, but KEEP — see its row:
  it is the tool that surfaces Cursor usage, the exact complaint behind this
  trim; uncalled-by-text is expected for a meter the user invokes by asking).
- "Uncalled" was NOT used alone as a cut reason: end-only skills
  (`verification-loop`, `production-audit`, `delivery-gate`, `codehealth-mcp`
  etc.) are uncalled by design, so each verdict below rests on the
  description/stack fit first, with uncalled/orphan status as supporting
  evidence (marked `[uncalled]` / `[orphan]` in the reason where it applies).

## Full table (166 skills, alphabetical)

| skill | verdict | reason |
|---|---|---|
| accessibility | CUT | WCAG audit/implementation; overlaps frontend-a11y (React/Next impl.) + browser-qa (axe-core audit) |
| agent-introspection-debugging | REVIEW | Meta skill for diagnosing failed agent runs; useful when a build run fails, but not part of building — decide if agent-failure diagnosis belongs in the plugin |
| agent-self-evaluation | CUT | On-demand 1–5 scorecard of the agent's own output; not a build step, never automatic |
| agent-sort | CUT | Builds an ECC install plan for a repo — plugin-maintenance meta-tool, not a hackathon build tool |
| agents-md-generator | CUT | Generates AGENTS.md on explicit ask only; one-off doc generation, not a winning-build step [uncalled] |
| ai-feature-spec | KEEP | Specs an AI feature end to end (model, prompt contract, fallbacks, eval) — most hackathon projects are AI features |
| ai-regression-testing | CUT | Generic AI regression-testing patterns; covered by tdd-workflow + stack testing skills (python-testing / react-testing) |
| android-clean-architecture | CUT | Android/Kotlin Multiplatform architecture — not the stack |
| angular-developer | CUT | Angular — not the stack (React/Next.js) |
| api-design | KEEP | REST design (naming, status codes, pagination, versioning) for the FastAPI/Next.js API surface |
| api-integration | KEEP | Generic REST-client mechanics for unnamed APIs; complements integration (named APIs) |
| app-scaffold | KEEP | Supabase backend scaffold (auth/DB/storage/RLS) for React/Next.js MVPs — core stack |
| architecture-decision-records | CUT | ADR files in docs/adr/; weekend builds record decisions in decision-record.md via orchestrate, not ADRs |
| article-writing | CUT | Long-form article/blog writing helper — writing, not building |
| backend-patterns | KEEP | Node/Express/Next.js API-route + data-access patterns — core stack |
| bengali-nlp | CUT | Bengali text processing — the skill the user explicitly named to cut; no build role [uncalled] |
| brainstorming | REVIEW | Collaborative ideation via questioning; overlaps grill-me (first prompt) + feature-expansion (autonomous) — keep only if later-feature ideation with the user is wanted |
| brownfield-retrospective | CUT | Retroactive ECC audit of an inherited codebase — fresh weekend builds have no legacy code [uncalled] |
| browser-qa | KEEP | Post-deploy UI verification (Playwright, console errors, screenshots, axe) with SHIP/DO-NOT-SHIP verdict — sole executor of pass/fail screen verdicts |
| bun-runtime | REVIEW | Bun runtime/pm/bundler/test runner; only if a project chooses Bun — Next.js default is npm/pnpm, so decide whether Bun is a supported path |
| ck | KEEP | Per-project memory for Cursor (save/resume across sessions) — weekend builds span sessions |
| click-path-audit | KEEP | Traces buttons through state changes to find dead/broken click paths; first stop for a dead button per systematic-debugging order |
| clickhouse-io | CUT | ClickHouse analytics DB — not the stack (Supabase/Postgres) |
| code-tour | CUT | CodeTour walkthrough files for onboarding/PR tours — not a winning-build step |
| codebase-memory | CUT | Queries a codebase knowledge graph; fresh weekend builds have no large unfamiliar codebase to query |
| codebase-onboarding | CUT | Onboarding guide for joining an unfamiliar codebase — fresh builds, not onboarding |
| codehealth-mcp | CUT | End-only Code Health via external CodeScene MCP — needs an external service, not part of the build |
| coding-standards | REVIEW | Generic baseline conventions fallback when no framework skill applies; overlaps typescript/python-patterns — keep only if a framework-neutral fallback is wanted |
| compose-multiplatform-patterns | CUT | Jetpack Compose / Kotlin Multiplatform UI — not the stack |
| content-engine | CUT | Social-content system (X/LinkedIn/TikTok/YouTube) — content marketing, not building |
| context-budget | KEEP | Surfaces the live Cursor context meter; directly addresses the user's Cursor-usage-burn complaint [uncalled, kept deliberately] |
| continuous-learning | CUT | Deprecated v1, description says do not invoke — v2 is the superset |
| continuous-learning-v2 | REVIEW | Hook-observed session learning / instinct system; meta-learning, not building — decide if cross-project learning capture belongs in the plugin |
| contract-first | KEEP | One authoritative API contract (OpenAPI/JSON Schema) for parallel frontend/backend work — the Next.js + FastAPI split |
| conventional-commit-review | CUT | Drafts Conventional Commits messages; overlaps git-workflow (commit conventions) |
| council | KEEP | Four-voice council for ambiguous go/no-go decisions; orchestrate explicitly routes go/no-go calls here |
| cpp-coding-standards | CUT | C++ — not the stack |
| cpp-testing | CUT | C++ tests (GoogleTest/CTest) — not the stack |
| csharp-testing | CUT | C#/.NET testing — not the stack |
| dart-flutter-patterns | CUT | Dart/Flutter — not the stack (React Native is the mobile path) |
| database-migrations | REVIEW | Safe migration patterns across Postgres/Prisma/Django/Go; overlaps app-scaffold + postgres-patterns — keep only if direct migration authoring is expected |
| delivery-gate | KEEP | End-only gate blocking "done" until quality checks + learning capture pass |
| deploy-fast | KEEP | Hackathon deploy runbook (Vercel/Railway/Supabase/Clerk) + pre-pitch checklist |
| design-system | KEEP | Extracts/audits design tokens + visual consistency; supports the design package |
| design-taste-frontend | KEEP | Taste v2.5.1 — leads full landing-page builds, anti-slop design |
| dev-team | CUT | Simulated multi-role panel on explicit ask only; council covers decisions, orchestrate covers delegation [uncalled] |
| devpost-autofiller | KEEP | Drafts the Devpost submission from README/commits — the submission itself |
| dispatching-parallel-agents | CUT | Only for 2+ independent concurrent failure investigations; orchestrate owns general fan-out |
| django-celery | CUT | Django + Celery background jobs — not the stack [uncalled] |
| django-patterns | CUT | Django — not the stack |
| django-tdd | CUT | Django testing — not the stack [orphan] |
| django-verification | CUT | Django verification loop — not the stack [orphan] |
| documentation-lookup | KEEP | Up-to-date framework docs via Context7 instead of training data (React/Next.js/FastAPI) |
| dotnet-patterns | CUT | C#/.NET — not the stack |
| e2e-testing | KEEP | Playwright E2E patterns (Page Object Model, flaky-test strategy) — writing tests, distinct from browser-qa's verdict run |
| ecc-recipes | CUT | Maps a workflow to ECC command groups, advisory only — plugin-internal navigation, not building |
| error-handling | KEEP | Typed errors, retries, circuit breakers across TypeScript/Python/Go — stack-relevant, cross-cutting |
| fastapi-patterns | KEEP | FastAPI + Pydantic v2 patterns — core backend stack |
| feature-expansion | KEEP | Autonomous feature elevation right after hackathon-scope in the first build — the "make it much better" step |
| flutter-dart-code-review | CUT | Flutter/Dart review — not the stack |
| frontend-a11y | KEEP | React/Next.js accessibility implementation patterns (forms, modals, focus) — stack-specific |
| frontend-design-direction | CUT | Description says explicitly: do NOT use for hackathon UI (design-taste-frontend / ui-ux-pro-max lead) — non-hackathon skill |
| frontend-patterns | KEEP | React/Next.js frontend patterns, state, performance — core stack |
| frontend-slides | KEEP | HTML pitch-deck construction; hackathon-pitch explicitly routes deck-building here |
| fsharp-testing | CUT | F# testing — not the stack [orphan] |
| gan-style-harness | CUT | Alternative generator-evaluator build harness; duplicates the orch-build-mvp / orchestrate generator-evaluator loop, not in the main flow |
| generating-python-installer | CUT | Commercial Windows installer packaging (Nuitka/Inno Setup) — not a web app or demo [uncalled] |
| git-workflow | KEEP | Branching, commit conventions, history hygiene, merge/rebase — core workflow |
| golang-patterns | CUT | Go — not the stack |
| golang-testing | CUT | Go testing — not the stack |
| grill-me | KEEP | First-step interview of the user, one question at a time, before any scoping/building |
| growth-log | REVIEW | Learning-capture log entries; delivery-gate checks learning logs, so keep only if delivery-gate's learning-capture requirement is kept |
| hackathon-pitch | KEEP | Pitch narrative, demo storyboard, judge Q&A from the HackMIT playbook |
| hackathon-scope | KEEP | MVP scoping after grill-me — demo-first, scope traps, time budget |
| hexagonal-architecture | CUT | Ports & Adapters across TS/Java/Kotlin/Go — over-engineering for a weekend MVP |
| hookify-rules | CUT | Hookify rules; description says upstream only, no Cursor equivalent in this plugin |
| i18n-sync | CUT | Locale-file translation/sync — writing/translation helper, not a build tool [uncalled] |
| inherit-legacy-style | CUT | Extracts style rules from a hand-written legacy codebase — fresh builds have none |
| integration | KEEP | Wires a named API/SDK/sponsor integration in (auth, client, live-call verify, demo path) — core to winning sponsor tracks |
| intent-driven-development | REVIEW | Acceptance-criteria scoping for ambiguous changes; overlaps grill-me/hackathon-scope on the first prompt — keep only for later ambiguous changes |
| investor-materials | CUT | Fundraising decks/memos/models — not hackathon judging [uncalled] |
| investor-outreach | CUT | Investor cold emails/intros — fundraising, not hackathon [uncalled] |
| iterative-retrieval | CUT | Subagent context-retrieval refinement — agent-internals meta skill [orphan] |
| java-coding-standards | CUT | Java (Spring Boot/Quarkus) — not the stack |
| jpa-patterns | CUT | JPA/Hibernate — not the stack |
| kotlin-coroutines-flows | CUT | Kotlin coroutines/Flow (Android/KMP) — not the stack |
| kotlin-exposed-patterns | CUT | Exposed ORM (Kotlin) — not the stack [uncalled] |
| kotlin-ktor-patterns | CUT | Ktor server (Kotlin) — not the stack [uncalled] |
| kotlin-patterns | CUT | Kotlin — not the stack |
| kotlin-testing | CUT | Kotlin testing — not the stack |
| laravel-patterns | CUT | Laravel/PHP — not the stack |
| laravel-plugin-discovery | CUT | Laravel package discovery via LaraPlugins MCP — not the stack [uncalled] |
| laravel-tdd | CUT | Laravel testing — not the stack [orphan] |
| laravel-verification | CUT | Laravel verification loop — not the stack [uncalled] |
| less-flat-ui | KEEP | 23 textured UI treatments — the texture layer inside design builds |
| living-docs-governance | CUT | Long-lived-project doc governance; a weekend project is not long-lived [uncalled] |
| loop-design-check | CUT | Designs/reviews agent loops — agent-internals meta skill, not building |
| make-interfaces-feel-better | KEEP | Motion/interaction-feel details (timing, easing, hover/press feedback) |
| market-research | CUT | Market sizing / competitive / investor due diligence — business research; track-picker + hackathon-scope cover winnability |
| mcp-dependency-review | CUT | Static review of MCP config — plugin-config meta, not building |
| mcp-server-patterns | REVIEW | Building MCP servers (Node/TS SDK); keep only if an MCP-server hackathon track is a real possibility, otherwise niche |
| mobile-ship | KEEP | Playbook for shipping an Expo/React Native test build (EAS, TestFlight) — the mobile path (cf. Outrunn iOS) |
| motion-advanced | KEEP | Advanced React/Next.js motion (gestures, drag, SVG, text animation) |
| motion-foundations | KEEP | Motion tokens/springs/performance/reduced-motion foundation all motion skills depend on |
| motion-patterns | KEEP | Production animation patterns for React/Next.js UI elements |
| mybatis-patterns | CUT | MyBatis (Java persistence) — not the stack [uncalled] |
| mysql-patterns | CUT | MySQL/MariaDB — not the stack (Postgres via Supabase) [orphan] |
| nestjs-patterns | CUT | NestJS — not the stack (FastAPI is the backend) |
| nextjs-turbopack | KEEP | Next.js 16+ / Turbopack guidance — core frontend stack |
| nuxt4-patterns | CUT | Nuxt/Vue — not the stack |
| opensource-pipeline | CUT | Fork/sanitize/package for public release — post-hackathon publishing, not winning |
| orch-add-feature | KEEP | Orchestrated pipeline for adding a feature (plan–TDD–review–gated commit) |
| orch-build-mvp | KEEP | Orchestrated MVP bootstrap from the grill-me decision record + scope |
| orch-change-feature | KEEP | Orchestrated pipeline for changing existing behaviour |
| orch-fix-defect | KEEP | Orchestrated pipeline for fixing a bug (regression test first) |
| orch-pipeline | KEEP | Shared gated Research–Plan–TDD–Review–Commit engine behind all orch-* skills |
| orch-refine-code | KEEP | Orchestrated behaviour-preserving refactor |
| orchestrate | KEEP | Top-level multi-model orchestration / delegation entry point |
| perl-patterns | CUT | Perl — not the stack |
| perl-testing | CUT | Perl testing — not the stack |
| pitch-deck-video | KEEP | Demo video under 2:10 filmed from the real app with Playwright + narration — the /demo deliverable |
| plankton-code-quality | CUT | Write-time lint via Plankton hooks; upstream only, Cursor lacks PostToolUse hooks, auto-fix removed |
| polish-pass | KEEP | Final UI polish (states, responsive, consistency) without restyling |
| postgres-patterns | KEEP | Postgres schema/index/RLS patterns (Supabase best practices) — core data stack |
| prisma-patterns | REVIEW | Prisma ORM for TS backends; keep only if Prisma (vs Supabase client) is a supported data path |
| product-lens | CUT | YC-style product diagnostics / go-no-go; description defers hackathon scoping to hackathon-scope |
| production-audit | KEEP | End-only production-readiness audit (local evidence, no external service) |
| python-patterns | KEEP | Pythonic idioms / PEP 8 / typing — core backend stack |
| python-testing | KEEP | pytest + TDD patterns — core backend stack |
| quarkus-patterns | CUT | Quarkus/Java — not the stack |
| quarkus-tdd | CUT | Quarkus testing — not the stack |
| quarkus-verification | CUT | Quarkus verification loop — not the stack [uncalled] |
| rails-patterns | CUT | Ruby on Rails — not the stack [orphan] |
| react-native-patterns | KEEP | React Native / Expo patterns — the mobile path alongside mobile-ship |
| react-patterns | KEEP | React 18/19 patterns (hooks, server/client boundaries, Suspense) — core stack |
| react-performance | KEEP | React/Next.js performance (waterfalls, bundle, re-render) — winning demos must feel fast |
| react-testing | KEEP | React Testing Library / Vitest component testing — core stack |
| readme-writer | KEEP | Judge-ready README; devpost-autofiller depends on it existing |
| redis-patterns | REVIEW | Redis caching/locks/rate-limiting/pub-sub; keep only if a project needs caching or rate limiting beyond Supabase |
| repo-scan | CUT | Pointer that installs an external skill; performs no audit itself [uncalled] |
| rules-distill | CUT | Distills skills into rule files — plugin-maintenance meta [uncalled] |
| rust-patterns | CUT | Rust — not the stack |
| rust-testing | CUT | Rust testing — not the stack |
| santa-method | CUT | Multi-agent adversarial verification gate; duplicates verification-loop / production-audit end-gates |
| security-review | KEEP | Mid-build security checklist (auth, input, secrets, endpoints) — distinct from end-only security-scan |
| security-scan | CUT | Audits the plugin/Cursor configuration (.cursor dir), not application code — plugin-config meta |
| skill-scout | CUT | Searches skill sources before creating a new skill — plugin-maintenance meta |
| skill-stocktake | CUT | Audits Cursor skills/commands for quality — plugin-maintenance meta |
| springboot-patterns | CUT | Spring Boot/Java — not the stack |
| springboot-tdd | CUT | Spring Boot testing — not the stack |
| springboot-verification | CUT | Spring Boot verification loop — not the stack [uncalled] |
| story-lifecycle | CUT | Epic/story/sprint tracking without Jira — weekend projects don't run sprints [uncalled] |
| strategic-compact | KEEP | Manual context-compaction guidance at phase boundaries — manages Cursor usage burn in long builds |
| systematic-debugging | KEEP | Root-cause-first debugging when no more specific skill applies — core workflow |
| tdd-workflow | KEEP | TDD loop (failing test → green → refactor, 80%+ coverage) — core workflow |
| tinystruct-patterns | CUT | tinystruct Java framework — not the stack [uncalled] |
| track-picker | KEEP | Matches the idea to sponsor prizes / themed tracks and plans the integration to win them |
| typescript-patterns | KEEP | Strict TypeScript patterns — core stack |
| ui-to-vue | CUT | Batch-converts UI screenshots to Vue 3 — Vue is not the stack [uncalled] |
| ui-ux-pro-max | KEEP | Design intelligence for dashboards/apps/components (palettes, fonts, UX guidelines) |
| unified-memory | CUT | Shared context between agents via Memory Vault; duplicates ck and is unreachable [orphan] |
| verification-before-completion | KEEP | Lightweight mid-build check before claiming work is complete/fixed/passing |
| verification-loop | KEEP | Six-phase end-of-project verification (build, typecheck, lint, tests+coverage, security grep, diff review) |
| vite-patterns | KEEP | Vite config/plugins/HMR — the build tool under the frontend |
| vue-patterns | CUT | Vue 3 — not the stack |
| windows-desktop-e2e | CUT | Windows native desktop E2E (pywinauto) — not the stack [uncalled] |

## CUT list (91 — plain skill names, for the implementation step)

- accessibility
- agent-self-evaluation
- agent-sort
- agents-md-generator
- ai-regression-testing
- android-clean-architecture
- angular-developer
- architecture-decision-records
- article-writing
- bengali-nlp
- brownfield-retrospective
- clickhouse-io
- code-tour
- codebase-memory
- codebase-onboarding
- codehealth-mcp
- compose-multiplatform-patterns
- content-engine
- continuous-learning
- conventional-commit-review
- cpp-coding-standards
- cpp-testing
- csharp-testing
- dart-flutter-patterns
- dev-team
- dispatching-parallel-agents
- django-celery
- django-patterns
- django-tdd
- django-verification
- dotnet-patterns
- ecc-recipes
- flutter-dart-code-review
- frontend-design-direction
- fsharp-testing
- gan-style-harness
- generating-python-installer
- golang-patterns
- golang-testing
- hexagonal-architecture
- hookify-rules
- i18n-sync
- inherit-legacy-style
- investor-materials
- investor-outreach
- iterative-retrieval
- java-coding-standards
- jpa-patterns
- kotlin-coroutines-flows
- kotlin-exposed-patterns
- kotlin-ktor-patterns
- kotlin-patterns
- kotlin-testing
- laravel-patterns
- laravel-plugin-discovery
- laravel-tdd
- laravel-verification
- living-docs-governance
- loop-design-check
- market-research
- mcp-dependency-review
- mybatis-patterns
- mysql-patterns
- nestjs-patterns
- nuxt4-patterns
- opensource-pipeline
- perl-patterns
- perl-testing
- plankton-code-quality
- product-lens
- quarkus-patterns
- quarkus-tdd
- quarkus-verification
- rails-patterns
- repo-scan
- rules-distill
- rust-patterns
- rust-testing
- santa-method
- security-scan
- skill-scout
- skill-stocktake
- springboot-patterns
- springboot-tdd
- springboot-verification
- story-lifecycle
- tinystruct-patterns
- ui-to-vue
- unified-memory
- vue-patterns
- windows-desktop-e2e

## REVIEW list (11) — what would settle each

- **agent-introspection-debugging** — Settle by deciding whether diagnosing failed agent runs is in scope for the plugin; if yes KEEP, else CUT (it is meta, not build).
- **brainstorming** — Settle by deciding whether user-facing collaborative ideation after the first prompt is wanted; if yes KEEP, else CUT (grill-me + feature-expansion already cover ideation).
- **bun-runtime** — Settle by deciding whether Bun is a supported runtime/package-manager path; if builds stay npm/pnpm, CUT.
- **coding-standards** — Settle by checking whether any kept skill actually routes to it as a framework-neutral fallback; if typescript/python-patterns cover all fallback cases, CUT.
- **continuous-learning-v2** — Settle by deciding whether cross-session instinct/learning capture is wanted in the plugin; if not, CUT (v1 is already CUT as deprecated).
- **database-migrations** — Settle by checking whether builds author migrations directly or only through app-scaffold/Supabase; if the latter, CUT.
- **growth-log** — Settle with delivery-gate: if delivery-gate's learning-capture requirement is kept, KEEP growth-log; if that requirement is dropped, CUT.
- **intent-driven-development** — Settle by deciding whether post-first-prompt ambiguous changes need acceptance-criteria scoping; if grill-me/hackathon-scope suffice, CUT.
- **mcp-server-patterns** — Settle by whether an MCP-server hackathon track is a realistic target; if not, CUT.
- **prisma-patterns** — Settle by whether Prisma is a supported data path alongside Supabase; if Supabase client only, CUT.
- **redis-patterns** — Settle by whether weekend builds ever need Redis (caching, rate limiting, locks); if not, CUT.

## Notes / caveats for the implementation step

- No verdict rests on "uncalled" alone: every CUT above has a stack-fit or
  duplication reason in its row. The one uncalled skill kept is
  `context-budget` (usage meter — the complaint behind this trim).
- Biggest CUT clusters: per-language framework/testing skills for stacks the
  builds never use (47 of the 91: Django, Laravel, Spring Boot, Quarkus,
  Rails, Kotlin, Go, Rust, C++, C#, F#, Perl, Vue/Nuxt, NestJS, Angular,
  Flutter, MySQL, MyBatis, ClickHouse, tinystruct, Windows desktop, etc.);
  writing/content helpers (4: article-writing, bengali-nlp, content-engine,
  i18n-sync); plugin-maintenance meta skills (agent-sort, ecc-recipes,
  rules-distill, skill-scout, skill-stocktake, repo-scan, security-scan,
  mcp-dependency-review, etc.); and end-gate duplicates (santa-method vs
  verification-loop/production-audit; gan-style-harness vs orch-build-mvp).
- Headline cuts the user asked about: `bengali-nlp` is CUT (also uncalled),
  along with the other writing helpers.
- This inventory covers skills only. Agents, rules, commands, hooks and
  triggers were not inventoried; several CUT skills have companion agents
  (e.g. `ecc-bengali-reviewer`, `ecc-django-reviewer`) that the implementation
  step should check for orphaning.
- Method limit: verdicts are from SKILL.md frontmatter descriptions (first
  ~30 lines, more where unclear), not from running the skills; Cursor can
  also route by description with no textual reference (call-map blind spot
  B1), so a CUT skill could in principle have been description-routed at
  runtime — the call map measures textual dispatch only.
