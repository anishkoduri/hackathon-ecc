# Master prompt (fix program #4): ui-ux-pro-max — design-system definition
# before implementing UI, + anti-generic principles, for dashboard/app
# surfaces.
# Upstream ECC file (cloned fresh from github.com/nextlevelbuilder/
# ui-ux-pro-max-skill on every build) — this fix lives here as a patch
# block placed LAST — just before STEP 5 — after the GATE / carve-out /
# Batch E / Batch F / fix-program-#3 patches, whose old-strings the
# substitution below is anchored on (i.e. against the CURRENT built text).
# Never edit hackathon-ecc/ directly. The substitution asserts exactly one
# match. The coordinator inserts this block last, just before STEP 5.
#
# What it adds, and what it deliberately does NOT duplicate:
# - Step 2 already generates a design system via --design-system (SKILL.md
#   :77-85) and the priority table + references/quick-reference.md already
#   define the individual values (type scale, semantic tokens, spacing
#   scale, hierarchy, nav, responsive, motion, accessibility, and the
#   loading/empty/success/error state rules scattered in quick-reference
#   §2/§3/§6/§8). What was missing was the pre-UI DEFINITION step itself:
#   the checklist of what must be recorded in MASTER.md before any UI code
#   is written. This snippet adds only that checklist, reusing the existing
#   tool output and reference rules for the values.
# - The anti-generic principles (generic AI-dashboard aesthetics, excessive
#   gradients, repetitive cards, decorative clutter) appear nowhere in
#   SKILL.md or references/ — the Batch E captivating bar (:14) covers
#   memorability, not this. Added here, pointing at the bar above it.
# - This is a pre-UI step, not a gate: define it, then build. No approval
#   gate, no wait point, no new agent/skill/file.
python3 - "$PLUGIN_DIR" <<'PYEOF'
import os, sys
base = sys.argv[1]
subs = [
  # Master prompt — define the design system BEFORE implementing UI
  # (dashboard/app surfaces only; landing/company builds belong to
  # design-taste-frontend). The --design-system output sketches the
  # system; this step fixes the decisions in MASTER.md first.
  ("skills/ui-ux-pro-max/SKILL.md",
   r'''This aggregates product/style/color/typography matches, applies reasoning rules from `ui-reasoning.csv`, and returns pattern, style, colors, typography, effects, and anti-patterns to avoid.''',
   r'''This aggregates product/style/color/typography matches, applies reasoning rules from `ui-reasoning.csv`, and returns pattern, style, colors, typography, effects, and anti-patterns to avoid.

**Define the design system before implementing UI (dashboard/app surfaces):** before writing any UI code, record the system in `design-system/<project-slug>/MASTER.md` (Step 2b) — visual identity; typography + type scale; color palette + semantic tokens (no raw hex in components); spacing/layout system; component hierarchy; navigation/IA; responsive behavior; motion/microinteractions; accessibility; and loading / empty / success / error states for every data surface. Take the values from the `--design-system` output and `references/quick-reference.md` — this step fixes the decisions, it does not re-derive them. This is a pre-UI step, not an approval gate: define it, then build.

**Anti-generic bar:** avoid generic AI-dashboard aesthetics — excessive gradients, repetitive same-size cards, decorative clutter. Earn distinction through deliberate typography, spacing, alignment, and contrast, plus the one memorable anchor from the captivating bar above; if a surface looks like a default template, it fails even if every checklist item passes.'''),
]
for rel, old, new in subs:
    p = os.path.join(base, rel)
    text = open(p, encoding="utf-8").read()
    assert text.count(old) == 1, f"{rel}: pattern not found exactly once: {old[:60]!r}"
    open(p, "w", encoding="utf-8").write(text.replace(old, new))
print("master-prompt ui-ux-pro-max design-system definition applied")
PYEOF
