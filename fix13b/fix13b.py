#!/usr/bin/env python3
"""Fix program #13b — fix the 8 minors from dry-run #14 (Audit #42 was clean).

Staged-source edits (durable sources of truth; build.sh copies them verbatim
or patches them with pre-existing blocks whose anchors are re-verified here):
  M1  new-skills/feature-expansion/SKILL.md :145 + :189 — conditional
      components (motion, design-system, inherit-legacy-style) in the UI rule.
  M3  new-skills/orchestrate/SKILL.md — reviewer unconditional for UI diffs
      (new item 4), :187 record-check (no screen judgment), :191 sole
      executor, :193 sole-executor wording.
  M3  new-skills/orchestrate/references/dispatch-prompt.md [UI diff:] block
      — record-check, not screen judgment.
  M6  ~/workspace/cursor-skills/less-flat-ui/SKILL.md :69 (built :70) —
      "bolder" framing reworded to the "more, not bolder" posture.
  M7  round2-skills/polish-pass/SKILL.md :22 — remove the infer-direction
      fallback; round2-skills/polish-pass/reference/polish.md step 2.7 —
      same rule, so the two files agree.
No-staged-source files (orch-change-feature, orch-pipeline, browser-qa,
orch-build-mvp) are patched by the fix13b build.sh block inserted by
fix13b-assemble.py (M2, M3 pipeline half, M4, M5, M8).

M3+M4 mechanism (coordinator decision): browser-qa is the SINGLE named
executor of the screen-level distinctiveness bar inside the visual loop —
it is the only component that sees rendered screens (Playwright,
desktop + mobile). The blind reviewer checks only the recorded direction
(diff-visible) and runs on EVERY UI diff regardless of size. The
orch-pipeline Review phase gains a visual-loop invocation for UI diffs
(touched screens) so change flows have an executor; the whole-build loop
(orchestrate step 5 / orch-build-mvp step 6) covers every primary route.

All substitutions assert count==1 before any write; on failure the script
exits non-zero having written nothing.
"""
import os
import sys

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOME = os.path.expanduser("~")


def sub(path, old, new, label):
    with open(path) as f:
        text = f.read()
    n = text.count(old)
    assert n == 1, f"{label}: anchor count={n} (expected 1) in {path}: {old[:80]!r}"
    text = text.replace(old, new)
    with open(path, "w") as f:
        f.write(text)
    print(f"applied {label}")


# ---------------------------------------------------------------- M1
fe = os.path.join(PLUGIN_ROOT, "new-skills/feature-expansion/SKILL.md")
sub(fe,
    "and `ui-ux-pro-max` + Impeccable via `polish-pass` + Harmony still apply.",
    "and `ui-ux-pro-max` + Impeccable via `polish-pass` + Harmony still apply. "
    "Conditional components apply by surface type, never by size: motion work adds "
    "`make-interfaces-feel-better` (then the motion-* skills for React/Next motion); "
    "new design-system work adds `design-system`; legacy style drift adds "
    "`inherit-legacy-style`.",
    "M1 feature-expansion:145 conditional components")
sub(fe,
    "direction recorded in `docs/design-tokens.md` before building) |",
    "direction recorded in `docs/design-tokens.md` before building; conditional by "
    "surface type: motion + `make-interfaces-feel-better`, new design-system work + "
    "`design-system`, legacy drift + `inherit-legacy-style`) |",
    "M1 feature-expansion:189 conditional components")

# ---------------------------------------------------------------- M3 (orchestrate)
orc = os.path.join(PLUGIN_ROOT, "new-skills/orchestrate/SKILL.md")
sub(orc,
    "and are partly self-graded when the implementer shaped the tests.",
    "and are partly self-graded when the implementer shaped the tests.\n\n"
    "4. **Any diff that touches a UI surface (any size)** → a blind reviewer ALWAYS "
    "runs — UI diffs are not exempt from review, however small. Its UI scope is the "
    "design-direction record check below, not the built screens.",
    "M3 orchestrate reviewer unconditional for UI diffs")
sub(orc,
    "**Design-distinctiveness scope (UI diffs):** on any diff that touches a UI surface, "
    "the blind reviewer ALSO judges the built screens against the distinctiveness bar "
    "(step 5 below): a finding — minor at least — when the screens carry no named "
    "direction, no applied theme/tokens, read as a default template, or are derivative "
    "(the design is based on a searched external reference). Design findings route to "
    "the fix loop within the existing caps (at most 2 fix rounds per defect list).",
    "**Design-direction record check (UI diffs):** on any diff that touches a UI surface, "
    "the blind reviewer checks the direction is RECORDED — a named direction in "
    "`docs/design-tokens.md` / the decision record, present in the diff, with tokens "
    "tracing to it in the changed code; a missing record is a finding, minor at least. "
    "The reviewer does NOT judge the built screens — it cannot see them (it receives "
    "only the diff and the contract's acceptance criteria). Screen-level distinctiveness "
    "is judged ONLY by `browser-qa` in the visual loop (step 5 below), the single named "
    "executor of the distinctiveness bar. Record-check findings route to the fix loop "
    "within the existing caps (at most 2 fix rounds per defect list).",
    "M3 orchestrate:187 record-check")
sub(orc,
    "**Distinctiveness bar (can FAIL — applies here and in the blind reviewer, step 2 above).**",
    "**Distinctiveness bar (can FAIL — applies here; `browser-qa` is the SOLE executor of "
    "this bar inside the visual loop — the step-2 reviewer checks only the recorded "
    "direction, never the screens).**",
    "M3 orchestrate:191 sole executor")
sub(orc,
    "the distinctiveness check lives in the step-5 visual loop + the step-2 blind reviewer instead.",
    "the distinctiveness check lives ONLY in the step-5 visual loop (`browser-qa`, the sole "
    "executor); the step-2 reviewer checks only the recorded direction.",
    "M3 orchestrate:193 sole-executor wording")
sub(orc,
    "Then judge the primary screens against the distinctiveness bar (step 5 above) — a finding, "
    "minor at least, when a screen carries no named direction, no applied theme/tokens, reads as "
    "a default template, or is derivative (the design is based on a searched external reference) "
    "— and route findings to the fix loop within the existing caps.",
    "The distinctiveness judgment on the primary screens happens in the step-5 visual loop "
    "(`browser-qa`, sole executor) — do not re-judge it here; a finding, minor at least, when a "
    "screen carries no named direction, no applied theme/tokens, reads as a default template, or "
    "is derivative (the design is based on a searched external reference) — routed to the fix "
    "loop within the existing caps.",
    "M3 orchestrate:193 no re-judgment")

# ------------------------------------------------- M3 (dispatch-prompt template)
dp = os.path.join(PLUGIN_ROOT, "new-skills/orchestrate/references/dispatch-prompt.md")
sub(dp,
    "                  [UI diff:] ALSO judge the built screens against the\n"
    "                  distinctiveness bar (orchestrate SKILL.md Verify step 5):\n"
    "                  a named direction recorded AND visibly applied (tokens,\n"
    "                  type, colour, spacing trace to it); a finding, minor at\n"
    "                  least, when screens carry no named direction, no applied\n"
    "                  theme/tokens, read as a default template, or are derivative\n"
    "                  (the design is based on a searched external reference).",
    "                  [UI diff:] ALSO check the design-direction record: a\n"
    "                  named direction recorded in `docs/design-tokens.md` /\n"
    "                  the decision record, present in the diff, with tokens\n"
    "                  tracing to it in the changed code; a missing record is\n"
    "                  a finding, minor at least. Do NOT judge the built\n"
    "                  screens — you cannot see them (you receive only the\n"
    "                  diff and the acceptance criteria). Screen-level\n"
    "                  distinctiveness is judged by `browser-qa` in the\n"
    "                  visual loop, not here.",
    "M3 dispatch-prompt [UI diff:] record-check")

# ---------------------------------------------------------------- M6
lf = os.path.join(HOME, "workspace/cursor-skills/less-flat-ui/SKILL.md")
sub(lf,
    "A treatment on a small surface can be bolder than on a full page: a button can carry "
    "a full thermal gradient, a page background usually should not.",
    "A treatment on a small surface can carry more than on a full page: a button can carry "
    "a full thermal gradient, a page background usually should not — more craft on the "
    "surface, not a bolder look.",
    "M6 less-flat-ui:69 more-not-bolder reword")

# ---------------------------------------------------------------- M7
pp = os.path.join(PLUGIN_ROOT, "round2-skills/polish-pass/SKILL.md")
sub(pp,
    "if neither exists, infer the direction from the code and record it in the token file "
    "before judging (see Design system below).",
    "if neither exists, record that no direction is recorded — a missing-direction finding "
    "(minor at least), routed to the design skill — and do NOT infer a direction from the "
    "code and judge against it: a direction the check itself invented cannot certify the screen.",
    "M7 polish-pass:22 no infer-direction fallback")
pm = os.path.join(PLUGIN_ROOT, "round2-skills/polish-pass/reference/polish.md")
sub(pm,
    "it routes to the design skill for a redesign (see Step 3), it is never restyled here, and "
    "it stays listed under \"Still short of 10/10\" until redesigned.",
    "it routes to the design skill for a redesign (see Step 3), it is never restyled here, and "
    "it stays listed under \"Still short of 10/10\" until redesigned. If neither file exists, "
    "do NOT infer a direction from the code — record a missing-direction finding (minor at "
    "least) routed to the design skill, and do not pass direction-application on any screen.",
    "M7 polish.md step 2.7 agreement")

# ------------------------------------------- re-verify pre-existing (f) anchors
# build.sh patch (f) anchors in staged polish-pass SKILL.md must still be count==1
# after the :22 edit (they live in the description, the never-redesigns line, the
# "point them at" line, and the When-to-use table row).
with open(pp) as f:
    t = f.read()
for anchor in [
    "a new look belongs to ui-ux-pro-max and less-flat-ui, not this skill.",
    "The plugin already has `ui-ux-pro-max` and `less-flat-ui` for design direction and surface treatments. Those skills own the look.",
    "point them at `ui-ux-pro-max`.",
    "| A new look, direction, or visual style (\"redesign\", \"revamp\", \"make it look different\") | `ui-ux-pro-max` / `less-flat-ui` — not this skill |",
]:
    n = t.count(anchor)
    assert n == 1, f"(f) anchor count={n}: {anchor[:60]!r}"
print("pre-existing build.sh (f) anchors in staged polish-pass SKILL.md: all count==1")

print("fix13b staged edits: all applied")
