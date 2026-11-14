#!/usr/bin/env python3
"""verify20.py -- checks fix #20 in the BUILT tree (read-only).

Run after a build: python3 fix20/verify20.py
Exits 0 only if every check passes.

Checks, against ~/workspace/hackathon-plugin/hackathon-ecc:
  1. F4_SCOPE/F5/F6/B1/X1 anchors present in Taste (built) and
     orchestrate (built), after the D19 rule in each.
  2. F4_SCOPE_APP/F5_APP/F6_APP/B1_APP/X1_APP present in ui-ux-pro-max
     (built) and orch-build-mvp (built), after D19_APP in each.
  3. STATIC20 present x3 (Taste step 6, orchestrate Verify 5a,
     orch-build-mvp step 6); after STATIC19 in each; in orchestrate
     before the 5b bullet; STATIC20 contains the B1 and X1 items.
  4. POLISH_F20 present in polish-pass (including the B1/X1 sentence);
     TYPESET_F20 present in the typeset lens; TYPESET_CHECKBOX21_NEW
     present and the fix20 checkbox GONE (fix #21 supersedes it).
  5. Fix19 anchors intact: F4_RULE still present verbatim in Taste and
     orchestrate; F4_APP still present in ui-ux-pro-max; STATIC19 still
     present x3; D19_RULE still present in Taste and orchestrate;
     D19_APP still present in ui-ux-pro-max and orch-build-mvp.
  6. Canonical block (fix #15) still verbatim x1 in all 11 files; D1 rule
     still present in Taste/orchestrate/polish-pass/orch-build-mvp.
  7. vantage.md UNCHANGED in the built tree (display and body still
     Geologica) — this fix governs the deal, it does not rewrite theme
     data; the scope rule text names the collision handling.
  8. Counts unchanged post-fix19: 166/72/123/87/15.
  9. No banned terms (fix #16 scrub) in the built skill tree (excl.
     node_modules).
 10. build.sh is the post-fix21 file: it contains the fix15 + fix17 +
     fix19 + fix20 + fix21 blocks intact and has MORE lines than post-fix19
     (23,314). Lines + md5 are the literal post-fix21 pair (23,647 lines,
     md5 8dfacb47a2a6698d47e4b4a5f8d9126c) — fix20/MANIFEST.md is the CLOSED
     post-fix20 record (23609 / 785fb405...) and no longer matches
     build.sh, so the pin is literal here, same pattern as
     verify15/17/18/19 (fix #21 fix-up).
 11. verify15.py 44/44, verify17.py 60/60, verify18.py 72/72,
     verify19.py 76/76 (run as subprocesses, exit 0 required). The
     15/17/19 totals grew by one each in the weaving pass: each gained a
     named patch-4 check (weave20 less-flat-ui pointer) alongside the
     hunk-count baseline update 3 -> 4.
 12. Weaving (SPEC section 10): every in-scope skill (per the census
     constants) carries the design-decision pointer at its recorded
     decision points (pointer count per skill); every trigger key in
     skill-triggers@1.json resolves to a real skill dir;
     coverage.withTriggers equals the key count (64); no built skill is
     left unclassified in the census (27 in scope + 139 out of scope =
     166); every in-scope skill except orch-pipeline (internal engine)
     has a trigger key.
 13. coverage.skills in skill-triggers@1.json equals the live skill count
     (166) — audit #62 found the stale upstream 169; the fix-up patches
     it at build time.
 14. Interconnection (SPEC section 12.5, steer #3 item 1): every rule
     token (F2/F3/F4/F5/F6/D19/B1/X1/H1/BIND/INNOV) resolves to a
     defining phrase in the built tree; every Design-decision pointer
     line's tokens all resolve; every pointer targets the
     design-package rule, which exists in built orchestrate and
     carries the H1 + BIND/INNOV pointers — no orphan rule, no
     dead-end reference.
 15. H1 model hierarchy: full text in built orchestrate + built
     hackathon-mode §6; the design-package rule carries the H1 pointer.
 16. OVERDRIVE expansion: feature-expansion lenses return 5–9, the
     shortlist keeps 7–12 (cap, not quota), the overflow rule stands,
     the anti-drift guard is intact, the old 3–5 / 4–7 lines are gone;
     OVERDRIVE pointers in orchestrate step 2 + hackathon-mode §1.
 17. BIND + INNOV: full texts in built orchestrate + built
     hackathon-mode §6; pointers in the design-package rule, built
     orch-build-mvp, and built orch-pipeline; the fail/off-skill vs
     pass/on-skill distinction and the E1 channeling are present.
 18. build.sh hygiene (sweep #27 leftovers + sweep #28 MINOR-1):
     "section 37" is gone; "LAST" appears only in the two TRUE "runs
     LAST (after every …" lines; the lowercase "inserts this block
     last" family is gone too; the fix #20 program's block headers read
     "before STEP 5", generator = embedded copy.
"""
import hashlib
import json
import os
import re
import subprocess
import sys

HOME = os.path.expanduser("~")
PLUGIN = os.path.join(HOME, "workspace/hackathon-plugin")
for sub in ("fix15", "fix17", "fix18", "fix19", "fix20", "fix21"):
    sys.path.insert(0, os.path.join(PLUGIN, sub))
from fix15 import CANONICAL, D1_RULE  # noqa: E402
from fix17 import E1_RULE  # noqa: E402
from fix18 import FEATURES_CUTS_SECTION  # noqa: E402
from fix19 import (F4_RULE, D19_RULE, STATIC19, F4_APP, D19_APP,  # noqa: E402
                   TYPESET_CHECKBOX_NEW as TYPESET_CHECKBOX_FIX19)
from fix20 import (F4_SCOPE, F5, F6, B1, X1, STATIC20,  # noqa: E402
                   F4_SCOPE_APP, F5_APP, F6_APP, B1_APP, X1_APP,
                   POLISH_F20, POLISH_F20_BX1, TYPESET_F20,
                   TYPESET_CHECKBOX_NEW)
from fix21 import TYPESET_CHECKBOX21_NEW as TYPESET_CHECKBOX21  # noqa: E402
from fixup20c import H1_RULE, BIND_RULE, INNOV_RULE, OVERDRIVE_RULE  # noqa: E402

BASE = os.path.join(PLUGIN, "hackathon-ecc")

# ---------------------------------------------------------------------------
# §10 CENSUS (weave20.py is the source of truth; this copy is pinned here
# so the verifier does not silently change if the engine is edited).
# IN_SCOPE_CENSUS maps skill -> number of woven pointer decision points.
# OUT_OF_SCOPE_CENSUS maps skill -> the recorded out-of-scope reason.
# Deliberate triggerless exception: orch-pipeline (internal engine) is
# in scope but has no trigger key; frontend-design-direction is out of
# scope (hackathon-mode §5 exclusion) and likewise has no key.
IN_SCOPE_CENSUS = {
    "accessibility": 1,
    "ai-feature-spec": 1,
    "browser-qa": 1,
    "click-path-audit": 1,
    "design-system": 2,
    "design-taste-frontend": 2,
    "feature-expansion": 1,
    "frontend-a11y": 1,
    "frontend-slides": 1,
    "gan-style-harness": 1,
    "grill-me": 1,
    "hackathon-scope": 1,
    "less-flat-ui": 1,
    "make-interfaces-feel-better": 1,
    "motion-advanced": 1,
    "motion-foundations": 1,
    "motion-patterns": 1,
    "orch-add-feature": 1,
    "orch-build-mvp": 1,
    "orch-change-feature": 1,
    "orch-fix-defect": 1,
    "orch-pipeline": 1,
    "orch-refine-code": 1,
    "orchestrate": 2,
    "pitch-deck-video": 2,
    "polish-pass": 2,
    "ui-ux-pro-max": 1,
}
OUT_OF_SCOPE_CENSUS = {
    "agent-introspection-debugging": 'meta/ops/process — plugin, agent, or project process, no UI decisions',
    "agent-self-evaluation": 'meta/ops/process — plugin, agent, or project process, no UI decisions',
    "agent-sort": 'meta/ops/process — plugin, agent, or project process, no UI decisions',
    "agents-md-generator": 'meta/ops/process — plugin, agent, or project process, no UI decisions',
    "ai-regression-testing": 'testing/verification — checks code or behaviour, does not decide UI',
    "android-clean-architecture": 'stack-specific framework/language pattern library — implements a given design, does not decide visual design',
    "angular-developer": 'stack-specific framework/language pattern library — implements a given design, does not decide visual design',
    "api-design": 'backend/data/infra — server, data, or deployment mechanics, not UI',
    "api-integration": 'backend/data/infra — server, data, or deployment mechanics, not UI',
    "app-scaffold": "backend scaffolding (Supabase/auth/database) — no UI decision text in its SKILL.md; the scaffold's 'final layout' ownership is orchestrate's claim, not a decision this skill makes",
    "architecture-decision-records": 'meta/ops/process — plugin, agent, or project process, no UI decisions',
    "article-writing": 'business/content — copy, pitch, or market content, not UI/visual design',
    "backend-patterns": 'stack-specific framework/language pattern library — implements a given design, does not decide visual design',
    "bengali-nlp": 'stack-specific framework/language pattern library — implements a given design, does not decide visual design',
    "brainstorming": 'ideation facilitation — explores ideas with the user before implementation; makes no UI decisions itself',
    "brownfield-retrospective": 'meta/ops/process — plugin, agent, or project process, no UI decisions',
    "bun-runtime": 'stack-specific framework/language pattern library — implements a given design, does not decide visual design',
    "ck": 'meta/ops/process — plugin, agent, or project process, no UI decisions',
    "clickhouse-io": 'stack-specific framework/language pattern library — implements a given design, does not decide visual design',
    "code-tour": 'meta/ops/process — plugin, agent, or project process, no UI decisions',
    "codebase-memory": 'meta/ops/process — plugin, agent, or project process, no UI decisions',
    "codebase-onboarding": 'meta/ops/process — plugin, agent, or project process, no UI decisions',
    "codehealth-mcp": 'meta/ops/process — plugin, agent, or project process, no UI decisions',
    "coding-standards": 'baseline coding conventions — cross-project code style, not UI design',
    "compose-multiplatform-patterns": 'stack-specific framework/language pattern library — implements a given design, does not decide visual design',
    "content-engine": 'business/content — copy, pitch, or market content, not UI/visual design',
    "context-budget": 'meta/ops/process — plugin, agent, or project process, no UI decisions',
    "continuous-learning": 'meta/ops/process — plugin, agent, or project process, no UI decisions',
    "continuous-learning-v2": 'meta/ops/process — plugin, agent, or project process, no UI decisions',
    "contract-first": 'backend/data/infra — server, data, or deployment mechanics, not UI',
    "conventional-commit-review": 'meta/ops/process — plugin, agent, or project process, no UI decisions',
    "council": 'decision facilitation (four-voice council) — a process for ambiguous decisions, not a UI decision-maker',
    "cpp-coding-standards": 'stack-specific framework/language pattern library — implements a given design, does not decide visual design',
    "cpp-testing": 'testing/verification — checks code or behaviour, does not decide UI',
    "csharp-testing": 'testing/verification — checks code or behaviour, does not decide UI',
    "dart-flutter-patterns": 'stack-specific framework/language pattern library — implements a given design, does not decide visual design',
    "database-migrations": 'backend/data/infra — server, data, or deployment mechanics, not UI',
    "delivery-gate": 'meta/ops/process — plugin, agent, or project process, no UI decisions',
    "deploy-fast": 'backend/data/infra — server, data, or deployment mechanics, not UI',
    "dev-team": 'persona discussion session (PM/Architect/Developer/QA) — discusses designs; decisions land in the skills that act on the discussion',
    "devpost-autofiller": 'business/content — copy, pitch, or market content, not UI/visual design',
    "dispatching-parallel-agents": 'meta/ops/process — plugin, agent, or project process, no UI decisions',
    "django-celery": 'stack-specific framework/language pattern library — implements a given design, does not decide visual design',
    "django-patterns": 'stack-specific framework/language pattern library — implements a given design, does not decide visual design',
    "django-tdd": 'testing/verification — checks code or behaviour, does not decide UI',
    "django-verification": 'testing/verification — checks code or behaviour, does not decide UI',
    "documentation-lookup": 'meta/ops/process — plugin, agent, or project process, no UI decisions',
    "dotnet-patterns": 'stack-specific framework/language pattern library — implements a given design, does not decide visual design',
    "e2e-testing": 'testing/verification — checks code or behaviour, does not decide UI',
    "ecc-recipes": 'meta/ops/process — plugin, agent, or project process, no UI decisions',
    "error-handling": 'error-handling patterns (typed errors, retries, circuit breakers) — not UI decisions',
    "fastapi-patterns": 'stack-specific framework/language pattern library — implements a given design, does not decide visual design',
    "flutter-dart-code-review": 'testing/verification — checks code or behaviour, does not decide UI',
    "frontend-design-direction": 'excluded by hackathon-mode §5 — production UI outside hackathons; its own description forbids hackathon use; never invoked for hackathon UI work',
    "frontend-patterns": 'framework implementation patterns (composition/hooks/state/forms/animation implementation) — implements a given design, does not decide visual design',
    "fsharp-testing": 'testing/verification — checks code or behaviour, does not decide UI',
    "generating-python-installer": 'backend/data/infra — server, data, or deployment mechanics, not UI',
    "git-workflow": 'meta/ops/process — plugin, agent, or project process, no UI decisions',
    "golang-patterns": 'stack-specific framework/language pattern library — implements a given design, does not decide visual design',
    "golang-testing": 'testing/verification — checks code or behaviour, does not decide UI',
    "growth-log": 'meta/ops/process — plugin, agent, or project process, no UI decisions',
    "hackathon-pitch": 'business/content — copy, pitch, or market content, not UI/visual design',
    "hexagonal-architecture": 'stack-specific framework/language pattern library — implements a given design, does not decide visual design',
    "hookify-rules": 'meta/ops/process — plugin, agent, or project process, no UI decisions',
    "i18n-sync": 'locale-file translation mechanics — copy translation, not UI design decisions',
    "inherit-legacy-style": 'code-convention extraction (file anatomy, state, infra, error handling) — not UI/visual design; its design-package mention covers legacy code style, not visual decisions',
    "integration": 'backend/data/infra — server, data, or deployment mechanics, not UI',
    "intent-driven-development": 'acceptance-criteria scoping for ambiguous/high-impact changes — product/engineering scoping, not UI decisions',
    "investor-materials": "fundraising documents (decks, one-pagers, memos, models) — business content; deck layout itself is frontend-slides' job",
    "investor-outreach": 'business/content — copy, pitch, or market content, not UI/visual design',
    "iterative-retrieval": 'meta/ops/process — plugin, agent, or project process, no UI decisions',
    "java-coding-standards": 'stack-specific framework/language pattern library — implements a given design, does not decide visual design',
    "jpa-patterns": 'stack-specific framework/language pattern library — implements a given design, does not decide visual design',
    "kotlin-coroutines-flows": 'stack-specific framework/language pattern library — implements a given design, does not decide visual design',
    "kotlin-exposed-patterns": 'stack-specific framework/language pattern library — implements a given design, does not decide visual design',
    "kotlin-ktor-patterns": 'stack-specific framework/language pattern library — implements a given design, does not decide visual design',
    "kotlin-patterns": 'stack-specific framework/language pattern library — implements a given design, does not decide visual design',
    "kotlin-testing": 'testing/verification — checks code or behaviour, does not decide UI',
    "laravel-patterns": 'stack-specific framework/language pattern library — implements a given design, does not decide visual design',
    "laravel-plugin-discovery": 'meta/ops/process — plugin, agent, or project process, no UI decisions',
    "laravel-tdd": 'testing/verification — checks code or behaviour, does not decide UI',
    "laravel-verification": 'testing/verification — checks code or behaviour, does not decide UI',
    "living-docs-governance": 'meta/ops/process — plugin, agent, or project process, no UI decisions',
    "loop-design-check": 'meta/ops/process — plugin, agent, or project process, no UI decisions',
    "market-research": 'business/content — copy, pitch, or market content, not UI/visual design',
    "mcp-dependency-review": 'meta/ops/process — plugin, agent, or project process, no UI decisions',
    "mcp-server-patterns": 'stack-specific framework/language pattern library — implements a given design, does not decide visual design',
    "mobile-ship": 'packaging/deployment of a testable mobile build — not UI decisions',
    "mybatis-patterns": 'stack-specific framework/language pattern library — implements a given design, does not decide visual design',
    "mysql-patterns": 'stack-specific framework/language pattern library — implements a given design, does not decide visual design',
    "nestjs-patterns": 'stack-specific framework/language pattern library — implements a given design, does not decide visual design',
    "nextjs-turbopack": 'stack-specific framework/language pattern library — implements a given design, does not decide visual design',
    "nuxt4-patterns": 'stack-specific framework/language pattern library — implements a given design, does not decide visual design',
    "opensource-pipeline": 'meta/ops/process — plugin, agent, or project process, no UI decisions',
    "perl-patterns": 'stack-specific framework/language pattern library — implements a given design, does not decide visual design',
    "perl-testing": 'testing/verification — checks code or behaviour, does not decide UI',
    "plankton-code-quality": 'meta/ops/process — plugin, agent, or project process, no UI decisions',
    "postgres-patterns": 'stack-specific framework/language pattern library — implements a given design, does not decide visual design',
    "prisma-patterns": 'stack-specific framework/language pattern library — implements a given design, does not decide visual design',
    "product-lens": 'product validation diagnostics (go/no-go) — business decision, not UI; deliberately triggerless per weave1 (does not scope hackathons)',
    "production-audit": 'meta/ops/process — plugin, agent, or project process, no UI decisions',
    "python-patterns": 'stack-specific framework/language pattern library — implements a given design, does not decide visual design',
    "python-testing": 'testing/verification — checks code or behaviour, does not decide UI',
    "quarkus-patterns": 'stack-specific framework/language pattern library — implements a given design, does not decide visual design',
    "quarkus-tdd": 'testing/verification — checks code or behaviour, does not decide UI',
    "quarkus-verification": 'testing/verification — checks code or behaviour, does not decide UI',
    "rails-patterns": 'stack-specific framework/language pattern library — implements a given design, does not decide visual design',
    "react-native-patterns": 'stack-specific framework/language pattern library — implements a given design, does not decide visual design',
    "react-patterns": 'stack-specific framework/language pattern library — implements a given design, does not decide visual design',
    "react-performance": 'stack-specific framework/language pattern library — implements a given design, does not decide visual design',
    "react-testing": 'testing/verification — checks code or behaviour, does not decide UI',
    "readme-writer": 'business/content — copy, pitch, or market content, not UI/visual design',
    "redis-patterns": 'stack-specific framework/language pattern library — implements a given design, does not decide visual design',
    "repo-scan": 'meta/ops/process — plugin, agent, or project process, no UI decisions',
    "rules-distill": 'meta/ops/process — plugin, agent, or project process, no UI decisions',
    "rust-patterns": 'stack-specific framework/language pattern library — implements a given design, does not decide visual design',
    "rust-testing": 'testing/verification — checks code or behaviour, does not decide UI',
    "santa-method": 'meta/ops/process — plugin, agent, or project process, no UI decisions',
    "security-review": 'meta/ops/process — plugin, agent, or project process, no UI decisions',
    "security-scan": 'meta/ops/process — plugin, agent, or project process, no UI decisions',
    "skill-scout": 'meta/ops/process — plugin, agent, or project process, no UI decisions',
    "skill-stocktake": 'meta/ops/process — plugin, agent, or project process, no UI decisions',
    "springboot-patterns": 'stack-specific framework/language pattern library — implements a given design, does not decide visual design',
    "springboot-tdd": 'testing/verification — checks code or behaviour, does not decide UI',
    "springboot-verification": 'testing/verification — checks code or behaviour, does not decide UI',
    "story-lifecycle": 'meta/ops/process — plugin, agent, or project process, no UI decisions',
    "strategic-compact": 'meta/ops/process — plugin, agent, or project process, no UI decisions',
    "systematic-debugging": 'meta/ops/process — plugin, agent, or project process, no UI decisions',
    "tdd-workflow": 'meta/ops/process — plugin, agent, or project process, no UI decisions',
    "tinystruct-patterns": 'stack-specific framework/language pattern library — implements a given design, does not decide visual design',
    "track-picker": 'track/prize matching + integration plan — not UI decisions',
    "typescript-patterns": 'stack-specific framework/language pattern library — implements a given design, does not decide visual design',
    "ui-to-vue": 'batch conversion of UI screenshots/design exports into Vue components — implements a given design, does not decide it',
    "unified-memory": 'meta/ops/process — plugin, agent, or project process, no UI decisions',
    "verification-before-completion": 'testing/verification — checks code or behaviour, does not decide UI',
    "verification-loop": 'testing/verification — checks code or behaviour, does not decide UI',
    "vite-patterns": 'stack-specific framework/language pattern library — implements a given design, does not decide visual design',
    "vue-patterns": 'stack-specific framework/language pattern library — implements a given design, does not decide visual design',
    "windows-desktop-e2e": 'testing/verification — checks code or behaviour, does not decide UI',
}
WEAVE_MARKER = "Design-decision pointer:"
WEAVE_EXPECTED_TRIGGERS = 64
WEAVE_NEW_KEYS = ("accessibility", "ai-feature-spec",
                  "gan-style-harness", "motion-advanced",
                  "motion-foundations", "motion-patterns")

checks = []


def check(name, ok):
    checks.append((name, ok))
    print(("PASS " if ok else "FAIL ") + name)


def read(rel):
    return open(os.path.join(BASE, rel), encoding="utf-8").read()


taste = read("skills/design-taste-frontend/SKILL.md")
uipro = read("skills/ui-ux-pro-max/SKILL.md")
polish = read("skills/polish-pass/SKILL.md")
typeset = read("skills/polish-pass/reference/lenses/typeset.md")
orch = read("skills/orchestrate/SKILL.md")
mvp = read("skills/orch-build-mvp/SKILL.md")

# 1. F4_SCOPE/F5/F6/B1/X1 in Taste and orchestrate, after D19.
for label, text in (("Taste step 4a", taste),
                    ("orchestrate design-package rule", orch)):
    check(f"F4_SCOPE {label}: Tiempos rule is body-only", F4_SCOPE in text)
    check(f"F5 {label}: important text uses a unique, important font", F5 in text)
    check(f"F6 {label}: the design just has to be impressive", F6 in text)
    check(f"B1 {label}: every build carries a distinct brand identity", B1 in text)
    check(f"X1 {label}: every component is an experience", X1 in text)
    check(f"fix20 rules sit after the D19 rule in {label}",
          text.find(F4_SCOPE) > text.find(D19_RULE)
          and text.find(X1) > text.find(F4_SCOPE))
check("F6 names browser-qa's finish visual verdict, never a static check",
      "browser-qa's visual verdict on the rendered screens, never a static check" in taste
      and "browser-qa's visual verdict on the rendered screens, never a static check" in orch)

# 2. App mirrors in ui-ux-pro-max and orch-build-mvp, after D19_APP.
for label, text in (("ui-ux-pro-max anti-generic bar", uipro),
                    ("orch-build-mvp step 4", mvp)):
    check(f"F4_SCOPE_APP {label}", F4_SCOPE_APP in text)
    check(f"F5_APP {label}", F5_APP in text)
    check(f"F6_APP {label}", F6_APP in text)
    check(f"B1_APP {label}", B1_APP in text)
    check(f"X1_APP {label}", X1_APP in text)
    check(f"fix20 app mirrors sit after D19_APP in {label}",
          text.find(F4_SCOPE_APP) > text.find(D19_APP)
          and text.find(X1_APP) > text.find(F4_SCOPE_APP))

# 3. STATIC20 x3, after STATIC19, before 5b in orchestrate, B1/X1 items.
check("STATIC20 Taste step 6", STATIC20 in taste)
check("STATIC20 orchestrate Verify 5a", STATIC20 in orch)
check("STATIC20 orch-build-mvp step 6", STATIC20 in mvp)
check("STATIC20 sits after STATIC19 in Taste step 6",
      taste.find(STATIC20) > taste.find(STATIC19))
check("STATIC20 sits after STATIC19 in orchestrate 5a",
      orch.find(STATIC20) > orch.find(STATIC19))
check("STATIC20 sits after STATIC19 in orch-build-mvp step 6",
      mvp.find(STATIC20) > mvp.find(STATIC19))
check("STATIC20 in orchestrate 5a is before the 5b bullet (not injected into it)",
      orch.find(STATIC20) < orch.find("**5b. Final polish**"))
check("STATIC20 contains the B1 item (brand identity named on the record)",
      "(B1) The decision record names the build's brand identity (wordmark, identity tokens, voice)" in STATIC20
      and "(B1) The decision record names the build's brand identity" in taste)
check("STATIC20 contains the X1 item (component experience statement)",
      "(X1) Every component entry in the decision record states the experience it creates" in STATIC20
      and "(X1) Every component entry in the decision record states the experience it creates" in taste)

# 4. Polish-pass / typeset lens.
check("POLISH_F20 present in polish-pass harmony", POLISH_F20 in polish)
check("POLISH_F20 includes the B1/X1 sentence",
      POLISH_F20_BX1 in polish)
check("TYPESET_F20 present in typeset lens", TYPESET_F20 in typeset)
check("TYPESET_F20 sits after TYPESET_F19 in the typeset lens",
      typeset.find(TYPESET_F20) > typeset.find("font-optical-sizing: auto"))
check("typeset lens checkbox updated to fix #21",
      TYPESET_CHECKBOX21 in typeset
      and TYPESET_CHECKBOX_NEW not in typeset)

# 5. Fix19 anchors intact.
check("F4_RULE still verbatim in Taste", F4_RULE in taste)
check("F4_RULE still verbatim in orchestrate", F4_RULE in orch)
check("D19_RULE still verbatim in Taste", D19_RULE in taste)
check("D19_RULE still verbatim in orchestrate", D19_RULE in orch)
check("F4_APP still verbatim in ui-ux-pro-max", F4_APP in uipro)
check("STATIC19 still present in Taste step 6", STATIC19 in taste)
check("STATIC19 still present in orchestrate Verify 5a", STATIC19 in orch)
check("STATIC19 still present in orch-build-mvp step 6", STATIC19 in mvp)
check("D19_APP still verbatim in ui-ux-pro-max", D19_APP in uipro)
check("D19_APP still verbatim in orch-build-mvp", D19_APP in mvp)

# 6. Fix #15 anchors intact (canonical block + D1) + fix17/fix18 anchors.
CANON_TARGETS = [
    "skills/design-taste-frontend/SKILL.md",
    "skills/ui-ux-pro-max/SKILL.md",
    "skills/less-flat-ui/SKILL.md",
    "skills/polish-pass/SKILL.md",
    "skills/design-taste-frontend/references/hallmark/references/hallmark-floor.md",
    "skills/make-interfaces-feel-better/SKILL.md",
    "skills/motion-foundations/SKILL.md",
    "skills/motion-patterns/SKILL.md",
    "skills/motion-advanced/SKILL.md",
    "skills/orchestrate/SKILL.md",
    "skills/orch-build-mvp/SKILL.md",
]
for rel in CANON_TARGETS:
    text = read(rel)
    check(f"canonical block verbatim x1 in {rel}", text.count(CANONICAL) == 1)
check("D1 rule still in Taste step 6", D1_RULE in taste)
check("D1 rule still in orchestrate step 5", D1_RULE in orch)
check("D1 rule still in polish-pass Capture", D1_RULE in polish)
check("D1 rule still in orch-build-mvp step 6", D1_RULE in mvp)
check("fix18 FEATURES_CUTS_SECTION still in pitch-deck-video shots-reference.md",
      FEATURES_CUTS_SECTION in read("skills/pitch-deck-video/references/shots-reference.md"))
check("fix17 E1 rule still in Taste step 4a", E1_RULE in taste)

# 7. vantage.md UNCHANGED (display and body still Geologica).
vantage = read("skills/design-taste-frontend/references/hallmark/references/themes/vantage.md")
check("vantage.md still names Geologica for display AND body (unchanged)",
      '--font-display: "Geologica"; --font-body: "Geologica";' in vantage)
check("F4_SCOPE names the display==body collision handling",
      "Where a dealt theme names the same face for display and body" in taste)

# 8. Counts unchanged post-fix19.
def count_dir(d):
    return len(os.listdir(os.path.join(BASE, d)))
hooks_n = len(json.load(open(os.path.join(BASE, "hooks/hooks.json"),
                             encoding="utf-8"))["hooks"])
check("counts 166/72/123/87/15 (unchanged)",
      (count_dir("skills"), count_dir("agents"), count_dir("rules"),
       count_dir("commands"), hooks_n) == (166, 72, 123, 87, 15))

# 9. No banned terms in the built skill tree (excl. node_modules).
banned = ["claude", "codex", "anthropic", "opus", "sonnet", "haiku", "composer-2.5"]
hits = subprocess.run(
    ["grep", "-riE", "|".join(banned), "skills", "agents", "commands", "rules",
     "hooks", "README.md", "--exclude-dir=node_modules", "-l"],
    cwd=BASE, capture_output=True, text=True).stdout.strip()
check("banned terms 0 in built tree (skills/agents/commands/rules/hooks/README)",
      hits == "")
if hits:
    print("   banned-term files: %r" % (hits,))

# 10. build.sh post-fix20.
build = open(os.path.join(PLUGIN, "build.sh"), encoding="utf-8").read()
build_lines = build.splitlines()
build_md5 = hashlib.md5(build.encode("utf-8")).hexdigest()
check("build.sh contains the fix20 block marker",
      "fix20 upstream block applied" in build)
check("build.sh still contains the fix19 block marker",
      "fix19 upstream block applied" in build)
check("build.sh still contains the fix17 block marker",
      "fix17 upstream block applied" in build)
check("build.sh still contains the fix15 block marker",
      "fix15 upstream block applied" in build)
check("build.sh has MORE lines than post-fix19 (23,314)",
      len(build_lines) > 23314)
manifest_path = os.path.join(PLUGIN, "fix20/MANIFEST.md")
if os.path.exists(manifest_path):
    manifest = open(manifest_path, encoding="utf-8").read()
    m_lines = re.search(r"^build\.sh lines: (\d+)$", manifest, re.M)
    m_md5 = re.search(r"^build\.sh md5: ([0-9a-f]{32})$", manifest, re.M)
    check("fix20/MANIFEST.md records build.sh lines + md5",
          bool(m_lines and m_md5))
# fix20/MANIFEST.md is the CLOSED post-fix20 record (23609 lines,
# md5 785fb405...); it no longer matches build.sh, so the pin below is
# the literal post-fix21 pair (23,647 lines / 8dfacb47...), same
# pattern as verify15/17/18/19 — a baseline update, not an anchor
# change (fix #21 fix-up).
check("build.sh is 23,647 lines, md5 8dfacb47a2a6698d47e4b4a5f8d9126c (post-fix21)",
      len(build_lines) == 23647
      and build_md5 == "8dfacb47a2a6698d47e4b4a5f8d9126c")

# 11. verify15/17/18/19 still pass.
for name, script in (("fix15", "fix15/verify15.py"),
                     ("fix17", "fix17/verify17.py"),
                     ("fix18", "fix18/verify18.py"),
                     ("fix19", "fix19/verify19.py")):
    r = subprocess.run(["python3", script], cwd=PLUGIN, capture_output=True, text=True)
    tail = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ""
    check(f"{name} verifier still passes ({tail})", r.returncode == 0)


# 12. Weaving (SPEC section 10).
for _skill, _n in IN_SCOPE_CENSUS.items():
    _text = read(f"skills/{_skill}/SKILL.md")
    check(f"weave: {_skill} carries {_n} design-decision pointer(s)",
          _text.count(WEAVE_MARKER) == _n)
_triggers = json.load(open(os.path.join(
    BASE, "manifests/context-packs/skill-triggers@1.json"), encoding="utf-8"))
check("weave: every trigger key resolves to a real skill dir",
      all(os.path.isfile(os.path.join(
          BASE, "skills", _k[len("skill:"):], "SKILL.md"))
          for _k in _triggers["triggers"]))
check("weave: coverage.withTriggers equals the trigger key count (64)",
      _triggers["coverage"]["withTriggers"] == len(_triggers["triggers"])
      == WEAVE_EXPECTED_TRIGGERS)
check("weave: the 6 new trigger keys are present",
      all(f"skill:{_s}" in _triggers["triggers"] for _s in WEAVE_NEW_KEYS))
_built_skills = set(os.listdir(os.path.join(BASE, "skills")))
check("weave: census classifies every built skill (none unclassified)",
      set(IN_SCOPE_CENSUS) | set(OUT_OF_SCOPE_CENSUS) == _built_skills
      and not (set(IN_SCOPE_CENSUS) & set(OUT_OF_SCOPE_CENSUS)))
check("weave: census totals 27 in scope + 139 out of scope = 166",
      len(IN_SCOPE_CENSUS) == 27 and len(OUT_OF_SCOPE_CENSUS) == 139)
check("weave: every in-scope skill except orch-pipeline (internal engine) has a trigger key",
      all(f"skill:{_s}" in _triggers["triggers"]
          for _s in IN_SCOPE_CENSUS if _s != "orch-pipeline"))
check("weave: orch-pipeline stays triggerless (internal engine, weave1 precedent)",
      "skill:orch-pipeline" not in _triggers["triggers"])

# 13. Audit #62: coverage.skills is 166, not the stale upstream 169.
check("coverage.skills == 166 (audit #62 fix-up; manifest count corrected)",
      _triggers["coverage"]["skills"] == 166)

# 14. Interconnection (SPEC 12.5): every rule token resolves; every
# pointer's tokens resolve; every pointer targets the design-package
# rule, which carries the H1 + BIND/INNOV pointers.
TOKEN_MARKERS = {
    "F2": "its static files (weight → file)",
    "F3": "The pairing is recorded with a Source cell naming the exact skill text",
    "F4": "for BASIC text only",
    "F5": "Important text uses a unique, important font",
    "F6": "why it is the impressive choice for that surface",
    "D19": "six dimension lines (Motion / Theme / Texture / Visuals / Techniques / Colors)",
    "B1": "brand identity (wordmark, identity tokens, voice)",
    "X1": "the experience it creates (what it feels like, what moment it is)",
    "H1": "Grok 4.7 High decides, Grok 4.6 High executes",
    "BIND": "the skills are the only path",
    "INNOV": "Innovation builds on the skills",
}


def _tree_has(phrase):
    r = subprocess.run(["grep", "-r", "-F", "-q", phrase, "skills"],
                       cwd=BASE, capture_output=True, text=True)
    return r.returncode == 0


for _tok, _marker in TOKEN_MARKERS.items():
    check(f"interconnection: rule token {_tok} resolves to a defining phrase in the built tree",
          _tree_has(_marker))
check("interconnection: the design-package rule exists in built orchestrate",
      "**Design-package rule (row 10" in orch)
check("interconnection: the design-package rule carries the H1 pointer",
      "Model hierarchy (fix #20 H1):" in orch)
check("interconnection: the design-package rule carries the BIND/INNOV pointer",
      "Binding (fix #20 BIND/INNOV):" in orch)
_pointer_token_re = re.compile(r"F[2-6]|D19|B1|X1|H1|BIND|INNOV")
_pointer_hits = 0
_pointer_bad = []
for _skill in os.listdir(os.path.join(BASE, "skills")):
    _text = read(f"skills/{_skill}/SKILL.md")
    for _line in _text.split("\n"):
        if WEAVE_MARKER in _line:
            _pointer_hits += 1
            if "design-package rule" not in _line:
                _pointer_bad.append((_skill, "no design-package-rule target"))
            for _tok in set(_pointer_token_re.findall(_line)):
                if _tok not in TOKEN_MARKERS:
                    _pointer_bad.append((_skill, f"unresolved token {_tok}"))
check(f"interconnection: all {_pointer_hits} design-decision pointer lines target the design-package rule",
      _pointer_hits == 32 and not _pointer_bad)
if _pointer_bad:
    print("   bad pointers: %r" % (_pointer_bad,))

# 15. H1 model hierarchy.
hkm = read("rules/hackathon-mode.mdc")
check("H1 full text in built orchestrate", H1_RULE in orch)
check("H1 full text in built hackathon-mode §6", H1_RULE in hkm)
check("H1: a 4.6 worker routes decisions up, never decides on its own",
      "it never decides on its own" in orch and "it never decides on its own" in hkm)
check("H1: dispatching a big decision to 4.6 (or 4.7 execution) is a routing error",
      "is a routing error — a static check item, never a screen verdict" in orch)

# 16. OVERDRIVE expansion.
feat = read("skills/feature-expansion/SKILL.md")
check("OVERDRIVE full rule in built feature-expansion", OVERDRIVE_RULE in feat)
check("OVERDRIVE Phase 1: each lens returns 5–9 candidates",
      "Each returns 5–9 candidates, no more" in feat)
check("OVERDRIVE Phase 2: shortlist keeps 7–12 features",
      "Keep it to 7–12 features (fix #20 OVERDRIVE" in feat)
check("OVERDRIVE: 7–12 is a CAP, not a quota — never pad to reach it",
      "7–12 is a CAP, not a quota — never pad to reach it" in feat)
check("OVERDRIVE: overflow goes to docs/expansion.md, never cut to fit the ledger",
      "the full table goes in `docs/expansion.md`" in feat
      and "never cut features to fit the ledger" in feat)
check("OVERDRIVE: old 3–5 candidates line is gone",
      "Each returns 3–5 candidates" not in feat)
check("OVERDRIVE: old 4–7 features line is gone",
      "Keep it to 4–7 features" not in feat)
check("OVERDRIVE: anti-drift guard intact (contradicting a recorded decision is rejected)",
      "a feature that contradicts a recorded decision is rejected" in feat)
check("OVERDRIVE pointer in orchestrate step 2",
      "OVERDRIVE (fix #20):** 7–12 shortlisted features" in orch)
check("OVERDRIVE pointer in hackathon-mode §1",
      "fix #20 OVERDRIVE: the shortlist keeps 7–12 features" in hkm)
check("OVERDRIVE: hackathon-mode §1 fewer-exceptional guard untouched",
      "fewer exceptional features beat many mediocre ones" in hkm)

# 17. BIND + INNOV.
pipe = read("skills/orch-pipeline/SKILL.md")
check("BIND full text in built orchestrate", BIND_RULE in orch)
check("BIND full text in built hackathon-mode §6", BIND_RULE in hkm)
check("INNOV full text in built orchestrate", INNOV_RULE in orch)
check("INNOV full text in built hackathon-mode §6", INNOV_RULE in hkm)
check("BIND/INNOV pointer in the design-package rule",
      "Binding (fix #20 BIND/INNOV):" in orch)
check("BIND/INNOV pointer in built orch-build-mvp (design-package bullet)",
      "Binding routing (fix #20 BIND/INNOV):" in mvp)
check("BIND/INNOV pointer in built orch-pipeline (delegation line)",
      "Binding routing (fix #20 BIND/INNOV):" in pipe)
check("INNOV: audit/dry-run FAIL off-skill improvisation but do NOT fail on-skill innovation",
      "FAIL off-skill improvisation but do NOT fail on-skill innovation" in orch)
check("INNOV: channels the fix #17 E1 creativity push through the skills",
      "channels the fix #17 E1 creativity push" in orch)
check("BIND: a decision with no named operating skill is refused and routed",
      "A decision with no named operating skill is not a decision — it is refused and routed" in orch)
check("BIND: audit/dry-run FAIL only off-skill work where a skill exists and was bypassed",
      "FAIL any decision or work done outside a named skill where a skill exists and was bypassed" in orch)
check("BIND: recorded-gap fallback — no covering skill means record the gap, work by the closest skill's principles, flag it",
      "Recorded-gap fallback (fix #20)" in orch and "Recorded-gap fallback (fix #20)" in hkm)
check("BIND: a needed step done through the recorded-gap fallback PASSES, it is not off-skill improvisation",
      "A needed step done through the recorded-gap fallback PASSES the audit/dry-run" in orch)
check("BIND: priority order — (1) everything needed gets done, (2) on the skills, (3) recorded-gap fallback",
      "Priority order: (1) everything needed gets done, (2) on the skills wherever a skill exists, (3) through the recorded-gap fallback where none does" in orch)

# 18. build.sh hygiene (sweep #27 leftovers).
check("hygiene: 'hackathon-mode section 37' is gone from build.sh",
      "hackathon-mode section 37" not in build)
check("hygiene: 'hackathon-mode §37' is gone from build.sh",
      "hackathon-mode §37" not in build)
_last_lines = [ln for ln in build.split("\n") if "LAST" in ln]
check("hygiene: 'LAST' appears only in the two TRUE 'runs LAST (after every …' lines",
      len(_last_lines) == 2
      and all("runs LAST (after every" in ln for ln in _last_lines))
check("hygiene: no placement-'LAST' phrase survives in build.sh",
      "LAST — just before STEP 5" not in build
      and "LAST, just before STEP 5" not in build
      and "LAST in build.sh, just before STEP 5" not in build)
check("hygiene: no lowercase 'inserts this block last' placement claim survives in build.sh (sweep #28 MINOR-1)",
      "inserts this block last" not in build
      and "last, just before STEP 5" not in build)
check("hygiene: weave20 block header reads 'before STEP 5' (generator = embedded copy)",
      "# build — this block runs before STEP 5, after the fix20 block." in build)
check("hygiene: fix20 block header reads 'before STEP 5 (after the fix19 block)'",
      "# Placement: before STEP 5 (after the fix19 block)." in build)
check("hygiene: fixup20/fixup20b block headers read 'Placement: before STEP 5'",
      build.count("#  upstream halves are patched here. Placement: before STEP 5") == 2)
check("hygiene: fixup20c block is present and sits after the fixup20b block",
      "fixup20c upstream block applied" in build
      and build.find("fixup20c upstream block applied") > build.find("fixup20b upstream block applied"))

failed = [n for n, ok in checks if not ok]
print(f"\n{len(checks) - len(failed)}/{len(checks)} checks pass")
sys.exit(1 if failed else 0)
