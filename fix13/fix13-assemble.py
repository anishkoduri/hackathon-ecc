#!/usr/bin/env python3
"""Fix program #13 — ASSEMBLER (coordinator).

Inserts the two fix13 patch blocks into build.sh LAST, just before STEP 5.

Block A (fixer A, orch pipelines): design package + Grok pin for
  orch-build-mvp / orch-change-feature / orch-pipeline (no staged sources;
  upstream ECC patched here).
  CORRECTIONS vs MANIFEST-A §5 (coordinator-verified against the built tree):
  - `import sys` -> `import os, sys` (the loop uses os.path.join).
  - orch-build-mvp anchor: the manifest's "3. Stop at Gate 1..." text is STALE
    (pre-fix-#3 numbering, count=0). Re-anchored on the step-4 sentence
    "Have the first UI slice in the GAN loop write `docs/design-tokens.md`..."
    (count==1). The rule is appended as a sub-bullet INSIDE step 4, NOT as a
    new "5." — the file already has a step 5 (Reconcile); a numbered "5."
    would collide with it.
  - orch-change-feature anchor: the manifest's 4-line block WITHOUT the
    carve-out clause is count=0. Re-anchored on the full 4-line block
    INCLUDING the carve-out clause on line 34 (count==1); step 5 appended
    after line 35.
Block B (fixer B, ui-ux-pro-max runtime patch): verbatim from MANIFEST-B §2,
  plus a 5th substitution (coordinator addition, posture-correction steer
  Nov 11): the generated-direction rule — no design based on a searched
  reference; posture is more, not bolder.

Preflight: NONE against the built tree — build.sh does `rm -rf $PLUGIN_DIR`
at line 92 and regenerates the tree from scratch on every run, so a stale or
partial tree (e.g. left by an aborted build) proves nothing. All 8 anchors
were verified count==1 by the coordinator against the complete pre-fix13
tree before assembly; the blocks' own inner asserts re-verify each anchor
count==1 at build time and fail the build loudly on any mismatch.
Idempotency guard: refuses to run if a fix13 block is already in build.sh.
Backup: run `cp build.sh build.sh.before-fix13` before this script.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PLUGIN_ROOT = os.path.dirname(HERE)          # ~/workspace/hackathon-plugin
BUILD_SH = os.path.join(PLUGIN_ROOT, "build.sh")
STEP5_ANCHOR = "\n# STEP 5 — Counts\n"

BLOCK_A = r"""# --- fix13-A: design package + Grok pin for the orch-* pipelines ---
# (orch-build-mvp / orch-change-feature / orch-pipeline have no staged sources;
#  they are upstream ECC patched here). Placement: LAST, just before STEP 5.
python3 - "$PLUGIN_DIR" <<'PYEOF'
import os, sys
base = sys.argv[1]
subs = [
  # orch-build-mvp: design package + Grok pin on every UI slice (step 4).
  ("skills/orch-build-mvp/SKILL.md",
   r'''Have the first UI slice in the GAN loop write `docs/design-tokens.md` from its design system (per orchestrate's no-landing fallback) so later slices brief from real tokens.''',
   r'''Have the first UI slice in the GAN loop write `docs/design-tokens.md` from its design system (per orchestrate's no-landing fallback) so later slices brief from real tokens.
   - **Design package on every UI slice (relevance by surface type, never by size).** Every slice that touches a UI surface names its design components in its brief and records its direction in `docs/design-tokens.md` before building UI (landing: `design-taste-frontend` + dealt Hallmark theme + `ui-ux-pro-max` + Impeccable via `polish-pass` + Harmony; app/dashboard/components: `ui-ux-pro-max` + Impeccable via `polish-pass` + Harmony + `less-flat-ui` where dull/flat; motion: + `make-interfaces-feel-better`; new design-system work: + `design-system`; legacy drift: + `inherit-legacy-style`). The design role runs on model `grok-4.7-high` (slug form only — never bracket syntax; select Grok 4.7 High in Cursor's model picker before the first build, or the pin may silently fall back — file-level pin only, the live smoke test decides). Small changes, one-prompt changes, redesigns, and UI fixes are UI slices under this rule. The direction is generated through the package skills, never based on a searched external reference (orchestrate row-10 rule): if the design search returns only a marketing page, that is not a direction — the skills generate it instead. Posture is more, not bolder: more design decisions made deliberately through the skills, more craft. Verify the built app's primary screens against the distinctiveness bar — a named direction recorded AND visibly applied (tokens, type, colour, spacing trace to it); a finding, minor at least, when screens carry no named direction, no applied theme/tokens, read as a default template, or are derivative (the design is based on a searched external reference) — within the existing fix caps.'''),
  # orch-change-feature: UI change / rebuild-a-surface rule (step 5).
  ("skills/orch-change-feature/SKILL.md",
   r'''1. Run the `orch-pipeline` engine with the settings above.
2. Keep the plan light — only `standard`+ size warrants the full planning pass.
3. Stop at **Gate 1** (plan / changed-test approval) and **Gate 2** (pre-commit) — except during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature, where both gates auto-approve and the run proceeds without waiting (see hackathon-mode §7).
4. Add `security-reviewer` if the change touches a security trigger.''',
   r'''1. Run the `orch-pipeline` engine with the settings above.
2. Keep the plan light — only `standard`+ size warrants the full planning pass.
3. Stop at **Gate 1** (plan / changed-test approval) and **Gate 2** (pre-commit) — except during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature, where both gates auto-approve and the run proceeds without waiting (see hackathon-mode §7).
4. Add `security-reviewer` if the change touches a security trigger.
5. **UI change / rebuild-a-surface rule.** If the change touches UI — including a one-prompt change, a redesign, or a removal that rebuilds a surface — it is a UI slice under the design-package rule (orchestrate SKILL.md row 10): name the applicable design components in the brief (app/dashboard/components: `ui-ux-pro-max` + Impeccable via `polish-pass` + Harmony + `less-flat-ui` where dull/flat; landing: `design-taste-frontend` + dealt Hallmark theme; motion: + `make-interfaces-feel-better`), record the direction in the decision record / run ledger (the lightest-weight record that exists for this flow — one line, a stated default from the brief's mood/domain if silent, marked assumed) and in `docs/design-tokens.md` where the flow keeps one, and run the applicable package components before the change lands. The design role runs on model `grok-4.7-high` (slug form only). The direction is generated through the package skills, never based on a searched external reference: if the design search returns only a marketing page, that is not a direction — the skills generate it instead. Posture is more, not bolder: more design decisions made deliberately through the skills, more craft. Verify the rebuilt surface against the distinctiveness bar (named direction recorded AND visibly applied; a finding, minor at least, when it carries no named direction, no applied theme/tokens, reads as a default template, or is derivative — the design is based on a searched external reference) within the existing fix caps. Pure backend/logic changes with no visual surface are exempt.'''),
  # orch-pipeline step 5 Review: distinctiveness scope on UI diffs.
  ("skills/orch-pipeline/SKILL.md",
   r'''- **5. Review** — `code-reviewer` agent / `/code-review`. Add `security-reviewer`
  whenever the diff touches a security trigger (below).''',
   r'''- **5. Review** — `code-reviewer` agent / `/code-review`. Add `security-reviewer`
  whenever the diff touches a security trigger (below). On any diff that touches a UI surface, the reviewer ALSO judges the built screens against the distinctiveness bar (orchestrate SKILL.md Verify step 5): a named direction recorded AND visibly applied (tokens, type, colour, spacing trace to it) — a finding, minor at least, when screens carry no named direction, no applied theme/tokens, read as a default template, or are derivative (the design is based on a searched external reference).'''),
  # orch-pipeline Verification: UI / design-package / distinctiveness line.
  ("skills/orch-pipeline/SKILL.md",
   r'''- `security-reviewer` ran iff a security trigger was touched''',
   r'''- `security-reviewer` ran iff a security trigger was touched
- UI work (if any): the design package was named in the brief, the direction is recorded, and the distinctiveness bar passed or its findings were fixed within the caps (finding, minor at least, when screens carry no named direction, no applied theme/tokens, or read as a default template)'''),
]
for rel, old, new in subs:
    p = os.path.join(base, rel)
    t = open(p).read()
    assert t.count(old) == 1, f"anchor mismatch (x{t.count(old)}) in {rel}"
    open(p, "w").write(t.replace(old, new, 1))
print("fix13-A orch-pipeline block applied")
PYEOF

"""

BLOCK_B = r"""# --- fix13-B: ui-ux-pro-max — named direction record + enforced anti-generic /
# captivating bars + related-skill routing (motion-*, design-system, legacy) ---
# Plus coordinator 5th sub (posture-correction steer): generated direction —
# never based on a searched reference; posture is more, not bolder.
python3 - "$PLUGIN_DIR/skills/ui-ux-pro-max/SKILL.md" <<'PYEOF'
import sys
p = sys.argv[1]
text = open(p, encoding="utf-8").read()
subs = [
  (
    "This is a pre-UI step, not an approval gate: define it, then build.",
    "This is a pre-UI step, not an approval gate: define it, then build. **Name the direction in the record:** the first lines of `design-system/<project-slug>/MASTER.md` — and of `docs/design-tokens.md`, which you write from it when there is no landing slice — must carry the NAMED direction (the theme slug and its axes/mood, or the named style + axes from the `--design-system` output), never a bare \"modern clean\" or an unnamed search result, so any later slice can recover which direction the UI traces to.",
  ),
  (
    "if nothing is memorable, the surface fails even if every other check passes.",
    "if nothing is memorable, the surface fails even if every other check passes. Enforced fail criterion (the brief names the anchor; Verify checks it as pass/fail): after closing the page, a user can describe that one anchor — its form and what it showed — without reopening it. If no anchor can be named, the surface FAILS.",
  ),
  (
    "if a surface looks like a default template, it fails even if every checklist item passes.",
    "if a surface looks like a default template, it fails even if every checklist item passes. Enforced fail criteria (the brief and Verify check these as pass/fail against the recorded named direction): (1) Direction trace — every primary screen visibly traces to the named direction recorded in MASTER.md / `docs/design-tokens.md`; a screen that could belong to any product fails. (2) Memorable anchor — the primary view carries the one unmistakable anchor from the captivating bar above; if no anchor can be named, the surface FAILS. (3) Not a default template — a surface that looks like a default template fails even if every checklist item passes.",
  ),
  (
    "Do not use `--motion` to make a feel/timing decision on its own.",
    "Do not use `--motion` to make a feel/timing decision on its own.\n\n**Related-skill routing.** Motion implementation in React/Next.js goes to the motion-* skills (`motion-foundations`, `motion-patterns`, `motion-advanced`) — but only after feel/timing is decided with `make-interfaces-feel-better` (above). New design-system work, or a consistency audit of an existing UI, goes to the `design-system` skill (tokens to `design-tokens.json`, 10-dimension score) — its output becomes the MASTER.md / `docs/design-tokens.md` record, not a second competing system. On a hand-written legacy codebase, run `inherit-legacy-style` before writing UI, so new work follows the codebase's own conventions instead of drifting from them.",
  ),
  (
    "never a bare \"modern clean\" or an unnamed search result, so any later slice can recover which direction the UI traces to.",
    "never a bare \"modern clean\" or an unnamed search result, so any later slice can recover which direction the UI traces to.\n\n**Generated direction — never based on a searched reference.** Web search may inform facts (real product details, competitor awareness) but never the design direction: no design may be based off a searched external reference — not a marketing website, not a Dribbble shot, not a template, not any found page. If the design search returns nothing usable, or only a marketing page, that is not a direction — generate the direction through the package instead: a Hallmark theme via `design-taste-frontend` on landing, or a named ui-ux-pro-max direction (theme/axes/mood, from the skill's own styles, palettes, font pairings, and UX guidelines) on app screens. Record the direction with its SOURCE named as the skill that generated it — never a URL, never 'based on [found site]'. **More, not bolder:** apply the package fully — more design decisions made deliberately through the skills, more craft — boldness is neither the goal nor a defect; uniqueness and craft are the goal.",
  ),
]
for old, new in subs:
    assert text.count(old) == 1, f"ui-ux-pro-max fix13-B anchor not found exactly once: {old[:60]}"
    text = text.replace(old, new)
open(p, "w", encoding="utf-8").write(text)
print("ui-ux-pro-max patched (fix13-B: named direction + enforced bars + routing + generated-direction rule)")
PYEOF

"""

def main():
    # 1. build.sh guards.
    sh = open(BUILD_SH, encoding="utf-8").read()
    assert "fix13-A" not in sh, "fix13-A already in build.sh — refusing to double-insert"
    assert "fix13-B" not in sh, "fix13-B already in build.sh — refusing to double-insert"
    assert sh.count(STEP5_ANCHOR) == 1, \
        f"STEP 5 anchor count={sh.count(STEP5_ANCHOR)} — expected 1"

    # 2. Insert LAST, just before STEP 5.
    new_sh = sh.replace(STEP5_ANCHOR, BLOCK_A + BLOCK_B + STEP5_ANCHOR, 1)
    assert new_sh != sh
    open(BUILD_SH, "w", encoding="utf-8").write(new_sh)
    print("fix13 blocks inserted into build.sh before STEP 5")


if __name__ == "__main__":
    main()
