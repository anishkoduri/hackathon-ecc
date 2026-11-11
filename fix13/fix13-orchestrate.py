#!/usr/bin/env python3
"""fix13-orchestrate.py — Fix program #13, fixer A (ORCHESTRATION CORE).

Closes the row-10 design escape hatch, names the full design package in
every UI brief, records a named design direction before any UI is built,
extends Verify with a distinctiveness bar that can FAIL, and pins the
design role to grok-4.7-high (slug form only).

Each hunk is an anchored substitution: the OLD string must occur EXACTLY
ONCE in the target file. If an anchor does not match, that hunk is SKIPPED
(not guessed) and reported; the script exits non-zero if any hunk failed.
Only staged sources under ~/workspace/hackathon-plugin are touched.
Does NOT touch build.sh, the repo, the bundle, or any fixer-B file
(polish-pass, ui-ux-pro-max, design-taste-frontend, less-flat-ui, motion
skills, design-system, inherit-legacy-style).

Usage: python3 fix13-orchestrate.py
"""
import sys
from pathlib import Path

ROOT = Path.home() / "workspace" / "hackathon-plugin"

# (label, relative path, old exact text, new exact text)
HUNKS = []

# ---------------------------------------------------------------- A. orchestrate/SKILL.md
F = "new-skills/orchestrate/SKILL.md"

HUNKS.append(("A1-team-table-design-lead-row", F,
 "| **scout** | composer-2.5 (read-only) | locating code, mapping structure, inventorying symbols/call sites, summarizing current state |",
 "| **scout** | composer-2.5 (read-only) | locating code, mapping structure, inventorying symbols/call sites, summarizing current state |\n"
 "| **design-lead** | grok-4.7-high | design leadership for any UI surface — the design skill for that surface leads (row 10), executors implement under it |"))

HUNKS.append(("A2-step3-design-package-in-every-UI-brief", F,
 "**Integration skill in every slice brief:** the brief of any slice that wires an integration names `integration` (for the decision record's named API/SDK/tool) or `api-integration` (for unnamed REST mechanics) as its operating skill.",
 "**Integration skill in every slice brief:** the brief of any slice that wires an integration names `integration` (for the decision record's named API/SDK/tool) or `api-integration` (for unnamed REST mechanics) as its operating skill. "
 "**Design package in every UI slice brief:** the brief of every slice that touches a UI surface names the applicable design components for that surface (design-package rule, routing table row 10) — landing: `design-taste-frontend` + dealt Hallmark theme + `ui-ux-pro-max` + Impeccable via `polish-pass` + Harmony; app/dashboard/components: `ui-ux-pro-max` + Impeccable via `polish-pass` + Harmony + `less-flat-ui` where dull/flat; motion work: + `make-interfaces-feel-better`; new design-system work: + `design-system`; legacy drift: + `inherit-legacy-style` — and records the slice's chosen direction (from `docs/decision-record.md` and `docs/design-tokens.md`) BEFORE any UI is built. A UI brief with no named design components and no recorded direction is not ready to dispatch."))

HUNKS.append(("A3-step4-design-package-beside-TDD", F,
 "cited in the final report. If two implementers in the same wave touch the same files,",
 "cited in the final report. **Design package in every UI brief** (same rule as step 3): every implementer brief for a UI slice names its design components and restates the recorded direction + tokens inline before building UI — no UI slice builds on an unstated direction. If two implementers in the same wave touch the same files,"))

HUNKS.append(("A4-step4-grok-picker-note", F,
 "before that wave ends; later waves build the remaining UI slices from briefs restating those tokens (briefs written after the file exists, per step 3).",
 "before that wave ends; later waves build the remaining UI slices from briefs restating those tokens (briefs written after the file exists, per step 3). "
 "**Before the first build — Grok 4.7 High in the model picker (pre-build setup, not a mid-build ask):** the design role is pinned to `grok-4.7-high` (slug form only — never bracket syntax; Cursor's subagent model allowlist is coupled to the model-picker dropdown, so a frontmatter pin can fail or silently fall back, reportedly running on Opus, if Grok 4.7 High is not selected in the dropdown). Select **Grok 4.7 High** in Cursor's model picker before the first build, or the design pin may silently fall back to another model. This is a setup note read before building starts; it never pauses the build and never asks the user anything mid-build. File-level pin only — the live smoke test decides whether the pin holds; do not claim it is verified working."))

HUNKS.append(("A5a-row10-carveout-closed", F,
 'A mechanical, fully-specified UI component slice whose design is already fixed by the design system does NOT match this row (no design decision is left, so design leadership is not the question) — it routes by the other rows (row 6 if mechanical and fully specified)',
 'Relevance is by SURFACE TYPE, never by size: every slice that touches a UI surface matches this row — a full landing/company page, a dashboard/app surface, a single component, a small UI fix, a redesign, a one-prompt change that rebuilds a surface. A slice whose design is already fixed by the recorded direction still matches this row and routes with the design package (at minimum a `ui-ux-pro-max` direction check + Harmony check against the recorded direction in `docs/design-tokens.md`); "already fixed" changes which design work is left, never whether the package applies. The only work that does NOT match this row is non-UI mechanical work — pure backend/logic with no visual surface — which routes by the other rows (row 6 if mechanical and fully specified). A mechanical, fully-specified UI component slice is never exempt because it is small or "mechanical"'))

HUNKS.append(("A5b-row10-route-grok-pin", F,
 "**route to the design skill for that surface** — `design-taste-frontend` for a landing page, `ui-ux-pro-max` for a dashboard/app surface; the design skill leads, executors implement under it",
 "**route to the design skill for that surface** — `design-taste-frontend` for a landing page, `ui-ux-pro-max` for a dashboard/app surface; the design skill leads on model `grok-4.7-high` (design-lead tier, slug form only — see the picker note in step 4), executors implement under it"))

HUNKS.append(("A5c-design-package-rule-paragraph", F,
 "**Mixed UI+backend slice (split rule):**",
 "**Design-package rule (row 10 — relevance by surface type, never by size).** Every implementer brief for a UI slice names the applicable design components for that surface, and records the chosen direction + components BEFORE UI is built: landing/company page — `design-taste-frontend` (design lead) + the dealt Hallmark theme + `ui-ux-pro-max` + Impeccable via `polish-pass` + Harmony; dashboard/app surface or component — `ui-ux-pro-max` (design lead) + Impeccable via `polish-pass` + Harmony + `less-flat-ui` where the surface is dull/flat; motion work — + `make-interfaces-feel-better`; new design-system work — + `design-system`; work drifting from a legacy system — + `inherit-legacy-style`. The direction is recorded in `docs/design-tokens.md` (landing: dealt Hallmark theme slug + Tokens; app: the `ui-ux-pro-max` direction — theme/axes/mood, named, never \"modern clean\") before the slice builds UI; a UI brief written before the tokens exist would have to guess them (see step 3 two-pass briefing). Small changes, one-prompt changes, redesigns, UI fixes, and removal flows that rebuild a surface are UI slices under this rule — they record the direction in the decision record / run ledger (the lightest-weight record that exists for that flow) and run the applicable package components. No UI slice builds on an unstated direction.\n\n"
 "**Mixed UI+backend slice (split rule):**"))

HUNKS.append(("A6-handoff-direction-recorded-before-building", F,
 "where the two diverge, the brief restates the landing tokens and the dashboard slice follows them, and the divergence is noted in the stage ledger.",
 "where the two diverge, the brief restates the landing tokens and the dashboard slice follows them, and the divergence is noted in the stage ledger. "
 "**Direction recorded before building:** every UI brief records its chosen direction (the `Design direction:` line from `docs/decision-record.md`, restated in `docs/design-tokens.md`) and its design components before any UI is built — landing: dealt Hallmark theme slug + Tokens; app/dashboard: the `ui-ux-pro-max` direction (theme/axes/mood, named, never \"modern clean\"). No UI slice builds on an unstated direction."))

HUNKS.append(("A7-fallback-pins-design-lead-tier", F,
 "- **Fallback:** spawn a general subagent and pin the model to the tier's Cursor ID — deep-reasoner tier `claude-opus-5`, fast-worker tier `composer-2.5[fast=false]`, scout tier `composer-2.5` — pins the model only; the executor is otherwise a bare generalist. **Prepend the role preamble from dispatch-prompt.md**, or it won't know its operating contract.",
 "- **Fallback:** spawn a general subagent and pin the model to the tier's Cursor ID — deep-reasoner tier `claude-opus-5`, fast-worker tier `composer-2.5[fast=false]`, scout tier `composer-2.5`, design-lead tier `grok-4.7-high` (slug form only — never bracket syntax, never `effort=xhigh`; Grok 4.7 takes per-vendor `reasoning_effort=xhigh`, which Cursor does not expose in a pin, so the pin is the slug alone) — pins the model only; the executor is otherwise a bare generalist. **Prepend the role preamble from dispatch-prompt.md**, or it won't know its operating contract."))

HUNKS.append(("A8-blind-reviewer-design-distinctiveness-scope", F,
 "You adjudicate the defect list; fixes route by the routing rule (mechanical fix → fast-worker; design flaw → deep-reasoner).",
 "You adjudicate the defect list; fixes route by the routing rule (mechanical fix → fast-worker; design flaw → deep-reasoner). "
 "**Design-distinctiveness scope (UI diffs):** on any diff that touches a UI surface, the blind reviewer ALSO judges the built screens against the distinctiveness bar (step 5 below): a finding — minor at least — when the screens carry no named direction, no applied theme/tokens, or read as a default template. Design findings route to the fix loop within the existing caps (at most 2 fix rounds per defect list)."))

HUNKS.append(("A9a-visual-loop-enumerate-screens", F,
 "**5. Visual iteration loop (`browser-qa` — after tests pass, before deploy).** Run the app and invoke `browser-qa`'s visual iteration: capture and inspect the ACTUAL rendered interface (desktop + mobile), not a description of it. `browser-qa` returns the top 5 visual/usability problems; fix them, then re-inspect",
 "**5. Visual iteration loop (`browser-qa` — after tests pass, before deploy).** Run the app and invoke `browser-qa`'s visual iteration: capture and inspect the ACTUAL rendered interface (desktop + mobile), not a description of it. First enumerate the app's key screens/routes (every primary route, not just \"key pages\" — the dashboard, each main screen, each flow's landing state) and inspect each enumerated screen. `browser-qa` returns the top 5 visual/usability problems; fix them, then re-inspect"))

HUNKS.append(("A9b-distinctiveness-bar-can-fail", F,
 "If the app cannot run, record that as blocked with evidence instead of iterating.",
 "If the app cannot run, record that as blocked with evidence instead of iterating. "
 "**Distinctiveness bar (can FAIL — applies here and in the blind reviewer, step 2 above).** On the primary app screens, apply the captivating/wow test (does a screen make a judge stop and stare — hackathon-scope's wow test, feature-expansion Lens D, design-taste-frontend's captivating-hero bar) and the anti-generic bar (`ui-ux-pro-max`: if a surface looks like a default template, it fails even if every checklist item passes). The bar is: **a named direction is recorded AND visibly applied (tokens, type, colour, spacing decisions trace to it)** — no numeric score. A design check FAILS (a finding, minor at least) when screens carry no named direction, no applied theme/tokens, or read as a default template. The finding routes to the fix loop within the existing caps (max 3 rounds total, at most 2 fix rounds per problem list), not a pass."))

HUNKS.append(("A10a-hallmark-audit-retitled", F,
 "**6. Hallmark audit (landing/company pages only).** After the visual loop, run the Hallmark audit on the built landing page:",
 "**6. Hallmark audit (landing/company pages) + app-screen design audit.** After the visual loop, run the Hallmark audit on the built landing page:"))

HUNKS.append(("A10b-app-screen-design-audit", F,
 "This is a named check, not a user gate: it never asks the user anything and never blocks the run on anything but the page's own defects.",
 "This is a named check, not a user gate: it never asks the user anything and never blocks the run on anything but the page's own defects. "
 "**App screens (every build, landing or not).** On the built app's primary screens (the enumerated screens from step 5), run sloplint with `--scope app`: `node <plugin>/skills/design-taste-frontend/references/hallmark/scripts/sloplint.mjs <built app screens> --scope app` (static tier; render tier only where it applies). sloplint's app scope does NOT carry the distinctiveness check — `--scope app` exists (sloplint.mjs usage line) but `APP_SKIP` (sloplint.mjs:798-799) skips gate 32 (repetition/ledger bookkeeping, NOTE-only per gates.md §1, never part of the verdict) and other page gates in app scope, so do NOT claim a sloplint app-scope pass proves distinctiveness: the distinctiveness check lives in the step-5 visual loop + the step-2 blind reviewer instead. Fix every app-scope `FAIL`; fix or waive every `REFLEX` on the record. Then judge the primary screens against the distinctiveness bar (step 5 above) — a finding, minor at least, when a screen carries no named direction, no applied theme/tokens, or reads as a default template — and route findings to the fix loop within the existing caps. Run sloplint with `--json` and paste its summary counts into the Verify fix list. On a build with no landing page, this app-screen audit IS the step-6 design audit (the landing-only Hallmark audit does not run); on a build with a landing page, both run."))

HUNKS.append(("A11-final-report-design-direction-line", F,
 "- **Important design + engineering decisions** — each decision that shaped the product",
 "- **Design direction applied** — the named direction recorded in `docs/decision-record.md` and `docs/design-tokens.md`, which design-package components ran on which surfaces, and the Verify distinctiveness outcome (pass, findings fixed, or blocked with evidence).\n"
 "- **Important design + engineering decisions** — each decision that shaped the product"))

# ---------------------------------------------------------------- B. orchestrate/references/dispatch-prompt.md
G = "new-skills/orchestrate/references/dispatch-prompt.md"

HUNKS.append(("B1-skeleton-design-package-by-default", G,
 "5. **Operating skill** — ONLY when the custom roster injected a skill whose\n"
 "   domain matches this dispatch: add to the Inputs — *\"Read this first — it\n"
 "   is your operating procedure; follow it: `<path>/SKILL.md`\"*. The tier's\n"
 "   contract and return format still bind. On the blind-parallel path this\n"
 "   line is part of the verbatim task body both executors receive.",
 "5. **Operating skill** — ONLY when the custom roster injected a skill whose\n"
 "   domain matches this dispatch: add to the Inputs — *\"Read this first — it\n"
 "   is your operating procedure; follow it: `<path>/SKILL.md`\"*. The tier's\n"
 "   contract and return format still bind. On the blind-parallel path this\n"
 "   line is part of the verbatim task body both executors receive.\n"
 "5a. **Design package — named by default on every UI dispatch (not custom-roster-only).** Every dispatch whose work touches a UI surface names the design components for that surface in the Inputs, per the design-package rule (orchestrate SKILL.md row 10): landing/company page — `design-taste-frontend` + dealt Hallmark theme + `ui-ux-pro-max` + Impeccable via `polish-pass` + Harmony; dashboard/app surface or component — `ui-ux-pro-max` + Impeccable via `polish-pass` + Harmony + `less-flat-ui` where dull/flat; motion work — + `make-interfaces-feel-better`; new design-system work — + `design-system`; legacy drift — + `inherit-legacy-style`. The dispatch also restates the recorded direction from `docs/design-tokens.md` (theme/axes/mood, named) inline — never \"see the design system\". A UI dispatch with no named design skill is incomplete; the custom roster is not the only path a design skill reaches a dispatch."))

HUNKS.append(("B2-blind-reviewer-template-design-scope", G,
 "Constraints:      Review the changed code PLUS its callers and callees.\n"
 "                  [risk-domain:] explicit security/correctness focus.",
 "Constraints:      Review the changed code PLUS its callers and callees.\n"
 "                  [risk-domain:] explicit security/correctness focus.\n"
 "                  [UI diff:] ALSO judge the built screens against the\n"
 "                  distinctiveness bar (orchestrate SKILL.md Verify step 5):\n"
 "                  a named direction recorded AND visibly applied (tokens,\n"
 "                  type, colour, spacing trace to it); a finding, minor at\n"
 "                  least, when screens carry no named direction, no applied\n"
 "                  theme/tokens, or read as a default template."))

# ---------------------------------------------------------------- C. grill-me/SKILL.md
H = "new-skills/grill-me/SKILL.md"

HUNKS.append(("C1-design-direction-line-in-decision-record", H,
 "a decision/choice/rationale/consequence table, the hours-left number (or the recorded hours-left assumption from step 2 if the user stopped answering before giving it), `### Risks`, accepted unknowns (each with an owner and a resolution point), rejected alternatives that matter, and `### Completion criteria`",
 "a decision/choice/rationale/consequence table, the hours-left number (or the recorded hours-left assumption from step 2 if the user stopped answering before giving it), `### Risks`, accepted unknowns (each with an owner and a resolution point), rejected alternatives that matter, and `### Completion criteria`, plus one `Design direction:` line — the product's design direction (theme/axes/mood, named from the brief's mood/domain). If the user said nothing about look/feel, record the stated default as an assumption (marked assumed, not user-stated), derived from the brief's mood/domain — never leave the line blank: `hackathon-scope` and orchestrate's slice briefs build on it, and every UI slice restates it in `docs/design-tokens.md` before building UI"))

# ---------------------------------------------------------------- D. hackathon-scope/SKILL.md
I = "rewritten-skills/hackathon-scope/SKILL.md"

HUNKS.append(("D1-scope-carries-design-direction", I,
 "- The hours-left number, copied from the decision record, plus the time budget split (build vs demo vs slack, rule of thirds below)",
 "- The hours-left number, copied from the decision record, plus the time budget split (build vs demo vs slack, rule of thirds below)\n"
 "- The design direction, copied from the decision record's `Design direction:` line (theme/axes/mood, named) — if the record has no such line, record the stated default as an assumption in `docs/scope.md` (derived from the brief's mood/domain, marked assumed, not user-stated), never leave it blank; orchestrate's slice briefs and `docs/design-tokens.md` build on this line"))

# ---------------------------------------------------------------- E. feature-expansion/SKILL.md
J = "new-skills/feature-expansion/SKILL.md"

HUNKS.append(("E1-ui-rule-full-design-package", J,
 "Any feature that touches UI goes through the plugin's UI skills: `ui-ux-pro-max` and `less-flat-ui` together — except on a full landing/company page, where `design-taste-frontend` leads per hackathon-mode §5. The implementer's brief says so explicitly, and the implementer applies them to every surface the feature adds or changes.",
 "Any feature that touches UI goes through the full design package: `ui-ux-pro-max` and `less-flat-ui` together, plus the Impeccable craft floor via `polish-pass` and the Harmony rule — except on a full landing/company page, where `design-taste-frontend` leads (with the dealt Hallmark theme) per hackathon-mode §5, and `ui-ux-pro-max` + Impeccable via `polish-pass` + Harmony still apply. The implementer's brief says so explicitly, names the applicable components, and records the feature's direction (from `docs/decision-record.md` / `docs/design-tokens.md`, named, never \"modern clean\") BEFORE any UI is built — and the implementer applies them to every surface the feature adds or changes, however small."))

HUNKS.append(("E2-reference-table-ui-row", J,
 "| UI on any touched surface | `ui-ux-pro-max` + `less-flat-ui` (except a full landing/company page: `design-taste-frontend` leads) |",
 "| UI on any touched surface | full design package: `ui-ux-pro-max` + `less-flat-ui` + Impeccable via `polish-pass` + Harmony (except a full landing/company page: `design-taste-frontend` leads with the dealt Hallmark theme; direction recorded in `docs/design-tokens.md` before building) |"))


def main():
    failed = []
    applied = []
    cache = {}
    for label, rel, old, new in HUNKS:
        path = ROOT / rel
        if rel not in cache:
            cache[rel] = path.read_text(encoding="utf-8")
        text = cache[rel]
        n = text.count(old)
        if text.count(new) >= 1:
            # Already applied (checked FIRST: for append-style hunks the old
            # anchor survives inside the new text, so count(old)==1 even
            # after application — testing new is the only safe check).
            print(f"ALREADY {label}: new text present — nothing to do")
            applied.append(label)
            continue
        if n != 1:
            print(f"SKIP {label}: anchor occurs {n}x in {rel} (need exactly 1) — hunk NOT applied")
            failed.append(label)
            continue
        cache[rel] = text.replace(old, new, 1)
        applied.append(label)
        print(f"OK   {label}")
    for rel, text in cache.items():
        (ROOT / rel).write_text(text, encoding="utf-8")
    print(f"\nApplied {len(applied)}/{len(HUNKS)} hunks.")
    if failed:
        print("FAILED (anchor mismatch — not guessed):")
        for label in failed:
            print(f"  - {label}")
        sys.exit(1)
    print("All hunks applied.")


if __name__ == "__main__":
    main()
