# Batch E (fix program #4): ui-ux-pro-max — captivating bar for dashboard/app surfaces.
# Upstream ECC file, copied fresh on every build — this fix lives here as a
# patch block placed LAST — just before STEP 5 — after the GATE / carve-out /
# Batch E / Batch F / fix-program-#3 patches, whose old-strings the
# substitution below is anchored on (i.e. against the CURRENT built text:
# the post-audit9a "When to Apply" paragraph, including its "Do NOT use it
# for a full company or landing-page build" sentence).
# Never edit hackathon-ecc/ directly. The substitution asserts exactly one
# match. The coordinator inserts this block last, just before STEP 5.
python3 - "$PLUGIN_DIR" <<'PYEOF'
import os, sys
base = sys.argv[1]
subs = [
  # Design Decision 7 (design part) — dashboard/app surfaces aim for
  # striking, memorable surfaces: one concrete check. The primary view must
  # have one unmistakable visual anchor a user remembers after leaving the
  # page; the test is describing it from memory without reopening the page.
  ("skills/ui-ux-pro-max/SKILL.md",
   r'''Use this Skill when the task involves **UI structure, visual design decisions, interaction patterns, or user experience quality control**: designing new pages, creating/refactoring UI components, choosing color/typography/spacing/layout systems, reviewing UI for UX/accessibility/consistency, implementing navigation/animation/responsive behavior, or improving perceived quality and usability. Do NOT use it for a full company or landing-page build — that belongs to `design-taste-frontend` (see the frontmatter, the Query Contract, and Step 2).''',
   r'''Use this Skill when the task involves **UI structure, visual design decisions, interaction patterns, or user experience quality control**: designing new pages, creating/refactoring UI components, choosing color/typography/spacing/layout systems, reviewing UI for UX/accessibility/consistency, implementing navigation/animation/responsive behavior, or improving perceived quality and usability. Do NOT use it for a full company or landing-page build — that belongs to `design-taste-frontend` (see the frontmatter, the Query Contract, and Step 2).

**Captivating bar for dashboard/app surfaces:** the primary view must have one unmistakable visual anchor a user remembers after leaving the page. Test: after closing the page, the user can describe that one anchor — its form and what it showed — without reopening it; if nothing is memorable, the surface fails even if every other check passes.'''),
]
for rel, old, new in subs:
    p = os.path.join(base, rel)
    text = open(p, encoding="utf-8").read()
    assert text.count(old) == 1, f"{rel}: pattern not found exactly once: {old[:60]!r}"
    open(p, "w", encoding="utf-8").write(text.replace(old, new))
print("batch E ui-ux-pro-max captivating bar applied")
PYEOF
