#!/usr/bin/env python3
"""Fix program #13b — ASSEMBLER (coordinator).

Inserts the fix13b patch block into build.sh LAST, just before STEP 5
(after the fix13-A/B blocks). The block patches the five files with no
staged sources (upstream ECC patched at build time):
  M2  orch-change-feature/SKILL.md :36 — design-system + inherit-legacy-style
      in the UI rule; distinctiveness verified through browser-qa (single
      executor), reviewer checks only the recorded direction.
  M3  orch-pipeline/SKILL.md Review :71-72 — reviewer checks the recorded
      direction (unconditional for UI diffs); browser-qa visual loop runs
      on the rebuilt surface (touched screens) after the reviewer pass.
  M5  orch-pipeline/SKILL.md Verification :120 — derivative clause added.
  M4  browser-qa/SKILL.md :68 — distinctiveness added to the visual-loop
      criteria; browser-qa named SOLE executor of the bar.
  M8  orch-build-mvp/SKILL.md step 6 :49 — every-route visual loop +
      sloplint --scope app audit (mirrors orchestrate Verify steps 5-6).

Preflight: every anchor is verified count==1 against the CURRENT built
tree (post-fix13) before assembly — build.sh does `rm -rf $PLUGIN_DIR`
and regenerates the tree from scratch, so a stale or partial tree proves
nothing, but the anchors are the post-fix13 text and the current tree IS
post-fix13. The block's own inner asserts re-verify each anchor count==1
at build time and fail the build loudly on any mismatch.
Idempotency guard: refuses to run if a fix13b block is already in build.sh.
Backup: run `cp build.sh build.sh.before-fix13b` before this script.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PLUGIN_ROOT = os.path.dirname(HERE)          # ~/workspace/hackathon-plugin
BUILD_SH = os.path.join(PLUGIN_ROOT, "build.sh")
BUILT = os.path.join(PLUGIN_ROOT, "hackathon-ecc")
STEP5_ANCHOR = "\n# STEP 5 — Counts\n"

BLOCK = r"""# --- fix13b: dry-run #14 minors — M2/M3/M4/M5/M8 (orch pipelines + browser-qa) ---
# (orch-change-feature / orch-pipeline / browser-qa / orch-build-mvp have no
#  staged sources; they are upstream ECC patched here). Placement: LAST, just
#  before STEP 5 (after the fix13-A/B blocks).
python3 - "$PLUGIN_DIR" <<'PYEOF'
import os, sys
base = sys.argv[1]
subs = [
  # M2 orch-change-feature: conditional components + browser-qa as executor.
  ("skills/orch-change-feature/SKILL.md",
   r'''name the applicable design components in the brief (app/dashboard/components: `ui-ux-pro-max` + Impeccable via `polish-pass` + Harmony + `less-flat-ui` where dull/flat; landing: `design-taste-frontend` + dealt Hallmark theme; motion: + `make-interfaces-feel-better`)''',
   r'''name the applicable design components in the brief (app/dashboard/components: `ui-ux-pro-max` + Impeccable via `polish-pass` + Harmony + `less-flat-ui` where dull/flat; landing: `design-taste-frontend` + dealt Hallmark theme; motion: + `make-interfaces-feel-better`; new design-system work: + `design-system`; legacy style drift: + `inherit-legacy-style`)'''),
  ("skills/orch-change-feature/SKILL.md",
   r'''Verify the rebuilt surface against the distinctiveness bar (named direction recorded AND visibly applied; a finding, minor at least, when it carries no named direction, no applied theme/tokens, reads as a default template, or is derivative — the design is based on a searched external reference) within the existing fix caps.''',
   r'''Verify the rebuilt surface against the distinctiveness bar through `browser-qa`'s visual loop on the rebuilt surface (the single executor of the bar — see orch-pipeline Review; the reviewer checks only the recorded direction): a finding, minor at least, when it carries no named direction, no applied theme/tokens, reads as a default template, or is derivative (the design is based on a searched external reference) — within the existing fix caps.'''),
  # M3 orch-pipeline Review: record-check + visual loop on the rebuilt surface.
  ("skills/orch-pipeline/SKILL.md",
   r'''- **5. Review** — `code-reviewer` agent / `/code-review`. Add `security-reviewer`
  whenever the diff touches a security trigger (below). On any diff that touches a UI surface, the reviewer ALSO judges the built screens against the distinctiveness bar (orchestrate SKILL.md Verify step 5): a named direction recorded AND visibly applied (tokens, type, colour, spacing trace to it) — a finding, minor at least, when screens carry no named direction, no applied theme/tokens, read as a default template, or are derivative (the design is based on a searched external reference).''',
   r'''- **5. Review** — `code-reviewer` agent / `/code-review`. Add `security-reviewer`
  whenever the diff touches a security trigger (below). On any diff that touches a UI surface, the reviewer ALWAYS runs regardless of size (UI diffs are not exempt from review) and checks the direction is RECORDED — a named direction in `docs/design-tokens.md` / the decision record, present in the diff, with tokens tracing to it in the changed code; a missing record is a finding, minor at least. The reviewer does NOT judge the built screens (it receives only the diff). Screen-level distinctiveness is judged ONLY by `browser-qa`'s visual loop, which runs on the rebuilt surface after the reviewer pass: enumerate the touched screens, inspect the rendered UI (desktop + mobile), and apply the distinctiveness bar (orchestrate SKILL.md Verify step 5) — a finding, minor at least, when screens carry no named direction, no applied theme/tokens, read as a default template, or are derivative (the design is based on a searched external reference); findings route to the capped 2-round fix loop (max 3 rounds total); if the app cannot run, record that as blocked with evidence instead of iterating.'''),
  # M5 orch-pipeline Verification: derivative clause.
  ("skills/orch-pipeline/SKILL.md",
   r'''- UI work (if any): the design package was named in the brief, the direction is recorded, and the distinctiveness bar passed or its findings were fixed within the caps (finding, minor at least, when screens carry no named direction, no applied theme/tokens, or read as a default template)''',
   r'''- UI work (if any): the design package was named in the brief, the direction is recorded, and the distinctiveness bar passed or its findings were fixed within the caps (finding, minor at least, when screens carry no named direction, no applied theme/tokens, read as a default template, or are derivative — the design is based on a searched external reference)'''),
  # M4 browser-qa: distinctiveness in the visual-loop criteria; sole executor.
  ("skills/browser-qa/SKILL.md",
   r'''Each round: capture screenshots, then judge the rendered UI on typography, hierarchy, spacing, alignment, color, contrast, and responsiveness; list the FIVE most noticeable visual/usability problems; fix them; re-inspect.''',
   r'''Each round: capture screenshots, then judge the rendered UI on typography, hierarchy, spacing, alignment, color, contrast, responsiveness, and distinctiveness — this skill is the SOLE executor of the distinctiveness bar inside the visual loop: on every enumerated screen, check that a named direction (generated through the package skills, recorded in `docs/design-tokens.md` or the decision record) is visibly applied (tokens, type, colour, spacing trace to it); a screen with no named direction, no applied theme/tokens, reading as a default template, or derivative (the design is based on a searched external reference) FAILS — report it as a distinctiveness finding (minor at least) with the top-5 list, so the caller routes it to the fix loop within the existing caps. No other step judges screen distinctiveness — the blind reviewer checks only the recorded direction, and sloplint app scope does not carry it. List the FIVE most noticeable visual/usability problems; fix them; re-inspect.'''),
  # M8 orch-build-mvp step 6: every-route visual loop + sloplint --scope app.
  ("skills/orch-build-mvp/SKILL.md",
   r'''6. **Verify — orch-pipeline Phase 5 (Review) + expansion Phase 5.** `code-reviewer` (+ `security-reviewer` on any security-trigger slice) reviews each slice; then run the whole-build verification: expansion Phase 5 checks BY NAME — `browser-qa` / `click-path-audit` / `verification-before-completion` per feature, after the MVP is built. Review findings are fixed inside the capped 2-round fix loop; past that, the item is recorded blocked with evidence and work moves on.''',
   r'''6. **Verify — orch-pipeline Phase 5 (Review) + expansion Phase 5.** `code-reviewer` (+ `security-reviewer` on any security-trigger slice) reviews each slice; then run the whole-build verification: expansion Phase 5 checks BY NAME — `browser-qa` / `click-path-audit` / `verification-before-completion` per feature, after the MVP is built. Then run the every-route visual loop: enumerate the app's key screens/routes (every primary route — the Review-phase loop above covers only the touched screens; this loop covers every primary route) and invoke `browser-qa`'s visual iteration on the running app (desktop + mobile) — `browser-qa` is the SOLE executor of the distinctiveness bar inside the loop (a named direction recorded AND visibly applied; a finding, minor at least, when screens carry no named direction, no applied theme/tokens, read as a default template, or are derivative — the design is based on a searched external reference); fix and re-inspect within the same caps as orchestrate (max 3 rounds total, at most 2 fix rounds per problem list; if the app cannot run, record that as blocked with evidence instead of iterating). Then run the app-screen design audit: sloplint with `--scope app` on the built app's primary screens (`node <plugin>/skills/design-taste-frontend/references/hallmark/scripts/sloplint.mjs <built app screens> --scope app`, static tier; `--json`, paste summary counts into the Verify fix list) — fix every `FAIL`, fix or waive every `REFLEX` on the record; a sloplint app-scope pass does NOT prove distinctiveness (that check lives only in the visual loop above). Review findings are fixed inside the capped 2-round fix loop; past that, the item is recorded blocked with evidence and work moves on.'''),
]
for rel, old, new in subs:
    p = os.path.join(base, rel)
    t = open(p).read()
    n = t.count(old)
    assert n == 1, f"fix13b anchor not found exactly once in {rel}: {old[:70]!r} (count={n})"
    open(p, "w").write(t.replace(old, new))
print("fix13b orch-pipeline block applied")
PYEOF
"""

# --- preflight: verify every anchor count==1 against the current built tree
ANCHORS = [
    ("skills/orch-change-feature/SKILL.md",
     "name the applicable design components in the brief (app/dashboard/components: `ui-ux-pro-max` + Impeccable via `polish-pass` + Harmony + `less-flat-ui` where dull/flat; landing: `design-taste-frontend` + dealt Hallmark theme; motion: + `make-interfaces-feel-better`)"),
    ("skills/orch-change-feature/SKILL.md",
     "Verify the rebuilt surface against the distinctiveness bar (named direction recorded AND visibly applied; a finding, minor at least, when it carries no named direction, no applied theme/tokens, reads as a default template, or is derivative — the design is based on a searched external reference) within the existing fix caps."),
    ("skills/orch-pipeline/SKILL.md",
     "On any diff that touches a UI surface, the reviewer ALSO judges the built screens against the distinctiveness bar (orchestrate SKILL.md Verify step 5)"),
    ("skills/orch-pipeline/SKILL.md",
     "- UI work (if any): the design package was named in the brief, the direction is recorded, and the distinctiveness bar passed or its findings were fixed within the caps (finding, minor at least, when screens carry no named direction, no applied theme/tokens, or read as a default template)"),
    ("skills/browser-qa/SKILL.md",
     "Each round: capture screenshots, then judge the rendered UI on typography, hierarchy, spacing, alignment, color, contrast, and responsiveness; list the FIVE most noticeable visual/usability problems; fix them; re-inspect."),
    ("skills/orch-build-mvp/SKILL.md",
     "6. **Verify — orch-pipeline Phase 5 (Review) + expansion Phase 5.** `code-reviewer` (+ `security-reviewer` on any security-trigger slice) reviews each slice; then run the whole-build verification: expansion Phase 5 checks BY NAME — `browser-qa` / `click-path-audit` / `verification-before-completion` per feature, after the MVP is built. Review findings are fixed inside the capped 2-round fix loop; past that, the item is recorded blocked with evidence and work moves on."),
]
for rel, old in ANCHORS:
    p = os.path.join(BUILT, rel)
    n = open(p).read().count(old)
    assert n == 1, f"preflight: anchor count={n} in {rel}: {old[:70]!r}"
    print(f"preflight OK count==1: {rel}")

with open(BUILD_SH) as f:
    build = f.read()
assert "fix13b orch-pipeline block applied" not in build, "fix13b block already in build.sh — refusing"
assert "fix13b:" not in build, "fix13b marker already in build.sh — refusing"
assert STEP5_ANCHOR in build, "STEP 5 anchor not found in build.sh"
build = build.replace(STEP5_ANCHOR, BLOCK + STEP5_ANCHOR, 1)
with open(BUILD_SH, "w") as f:
    f.write(build)
print("fix13b block inserted into build.sh (LAST, just before STEP 5)")
