# Fix program #5, Batch 3: ui-ux-pro-max — M9 MASTER.md conformance + Audit M3 ask-user carve-out.
# Upstream ECC file, copied fresh on every build — this fix lives here as a
# patch block placed LAST, just before STEP 5, after the GATE / carve-out /
# Batch E / Batch F / fix-program-#4 / master-prompt patches, whose
# old-strings the substitutions below are anchored on (i.e. against the
# CURRENT built text in hackathon-ecc/skills/ui-ux-pro-max/SKILL.md).
# Never edit hackathon-ecc/ directly. Each substitution asserts exactly one
# match. The coordinator inserts this block last, just before STEP 5.
python3 - "$PLUGIN_DIR" <<'PYEOF'
import os, sys
base = sys.argv[1]
subs = [
  # Audit M3 — uncarved "ask the user" (Step 1, Stack): inline carve-out in the wording used elsewhere (council): during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature, do NOT ask — resolve by stated assumption with the safe/reversible default and proceed. Not a new wait point: the carve-out removes the ask in the first build.
  ("skills/ui-ux-pro-max/SKILL.md",
   r'''- **Stack**: detect from the project — check `package.json` deps (react/next/vue/svelte/nuxt/@angular), `pubspec.yaml` (Flutter), `*.xcodeproj`/`Package.swift` (SwiftUI), `composer.json` (Laravel), or React Native markers (`app.json` + `react-native` dep). If nothing is detectable and stack guidance matters, ask the user. **Never assume a stack** — a hardcoded default silently misroutes every recommendation.''',
   r'''- **Stack**: detect from the project — check `package.json` deps (react/next/vue/svelte/nuxt/@angular), `pubspec.yaml` (Flutter), `*.xcodeproj`/`Package.swift` (SwiftUI), `composer.json` (Laravel), or React Native markers (`app.json` + `react-native` dep). If nothing is detectable and stack guidance matters, ask the user — except during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature, where you do NOT ask: resolve by stated assumption with the safe/reversible default and proceed. **Never assume a stack** — a hardcoded default silently misroutes every recommendation.'''),
  # M9 — design-system cross-slice handoff (dashboard side): the frozen landing system (design-taste-frontend, frozen on the plan) is the single source of truth; this MASTER.md must conform to it, and on divergence the frozen landing system wins.
  ("skills/ui-ux-pro-max/SKILL.md",
   r'''**Define the design system before implementing UI (dashboard/app surfaces):** before writing any UI code, record the system in `design-system/<project-slug>/MASTER.md` (Step 2b) — visual identity; typography + type scale; color palette + semantic tokens (no raw hex in components); spacing/layout system; component hierarchy; navigation/IA; responsive behavior; motion/microinteractions; accessibility; and loading / empty / success / error states for every data surface. Take the values from the `--design-system` output and `references/quick-reference.md` — this step fixes the decisions, it does not re-derive them. This is a pre-UI step, not an approval gate: define it, then build.''',
   r'''**Define the design system before implementing UI (dashboard/app surfaces):** before writing any UI code, record the system in `design-system/<project-slug>/MASTER.md` (Step 2b) — visual identity; typography + type scale; color palette + semantic tokens (no raw hex in components); spacing/layout system; component hierarchy; navigation/IA; responsive behavior; motion/microinteractions; accessibility; and loading / empty / success / error states for every data surface. Take the values from the `--design-system` output and `references/quick-reference.md` — this step fixes the decisions, it does not re-derive them. This is a pre-UI step, not an approval gate: define it, then build. **Single source of truth on divergence:** if a landing-page system was already frozen by `design-taste-frontend` on the plan, that frozen landing system is the single source of truth: this MASTER.md must conform to it — same tokens, same type scale, same component decisions. If the two diverge, the frozen landing system wins; do not re-derive a competing system.'''),
]
for rel, old, new in subs:
    p = os.path.join(base, rel)
    text = open(p, encoding="utf-8").read()
    assert text.count(old) == 1, f"{rel}: pattern not found exactly once: {old[:60]!r}"
    open(p, "w", encoding="utf-8").write(text.replace(old, new))
print("fix5 batch 3: ui-ux-pro-max M9 conformance + M3 ask-user carve-out applied")
PYEOF
