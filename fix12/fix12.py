#!/usr/bin/env python3
"""Fix program #12 — Audit #38 M1 + dry-run #10 M1-M5.

Applies staged-source edits (each substitution asserts exactly one match)
and inserts the fix12 build.sh patch block (D5) LAST, just before STEP 5.
Run from ~/workspace/hackathon-plugin as: python3 fix12/fix12.py
Then rebuild twice and verify diff = 0.
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def sub(path, old, new, label):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    n = text.count(old)
    assert n == 1, f"{label}: pattern found {n}x (expected 1): {old[:70]!r}"
    with open(path, "w", encoding="utf-8") as f:
        f.write(text.replace(old, new))
    print(f"  applied {label}")


IN_SCOPE = ("adapt, animate, audit, clarify, critique, distill, document, "
            "extract, harden, init, layout, onboard, optimize, polish, "
            "shape, typeset")

# ============ A1: impeccable-critique.md ============
crit = os.path.join(ROOT, "round2-skills/polish-pass/reference/impeccable-critique.md")

# A1(a) — :167 suggested-command list -> in-scope only + note
sub(crit,
    "- **Suggested command**: Which command could address this (from: /impeccable adapt, /impeccable animate, /impeccable audit, /impeccable bolder, /impeccable clarify, /impeccable colorize, /impeccable critique, /impeccable delight, /impeccable distill, /impeccable document, /impeccable harden, /impeccable layout, /impeccable onboard, /impeccable optimize, /impeccable overdrive, /impeccable polish, /impeccable quieter, /impeccable shape, /impeccable typeset)",
    "- **Suggested command**: Which command could address this (from: /impeccable " + IN_SCOPE.replace(", ", ", /impeccable ") + ")\n\nOnly the in-scope commands above: the direction lenses (bolder, quieter, colorize, decolorize, delight, overdrive) and live/generate are out of scope in this plugin — the lenses would change the design's direction, which clashes with the never-restyles rule, and live/generate need an interactive browser session (see reference/impeccable-PROVENANCE.md).",
    "A1(a) :167 command list")

# A1(a) — :282 recommendation list -> in-scope only + pointer
sub(crit,
    "- Only recommend commands from: /impeccable adapt, /impeccable animate, /impeccable audit, /impeccable bolder, /impeccable clarify, /impeccable colorize, /impeccable critique, /impeccable delight, /impeccable distill, /impeccable document, /impeccable harden, /impeccable layout, /impeccable onboard, /impeccable optimize, /impeccable overdrive, /impeccable polish, /impeccable quieter, /impeccable shape, /impeccable typeset",
    "- Only recommend commands from: /impeccable " + IN_SCOPE.replace(", ", ", /impeccable ") + " (in-scope commands only — the direction lenses are out of scope in this plugin; see the note under Priority Issues above)",
    "A1(a) :282 command list")

# A1(b) — carve-out paragraph after the Ask-the-User intro
sub(crit,
    "**After presenting findings**, use targeted questions based on what was actually found. Ask the user directly to clarify what you cannot infer. These answers will shape the action plan.",
    "**After presenting findings**, use targeted questions based on what was actually found. Ask the user directly to clarify what you cannot infer. These answers will shape the action plan.\n\n**Plugin carve-out (hackathon first build / one-prompt removal):** in a hackathon first build after grill-me, or a one-prompt removal of a first-build feature, do NOT ask the user anything — the run proceeds without waiting (hackathon-mode §7). Instead, state the assumption for each question you would have asked and proceed on the safe default: priority direction = the highest-severity Priority Issues first; tonal intent = keep the current tone (do not change direction); scope = Priority Issues only, top 3 first. Emit the literal line `Questions skipped: first build — proceeding on stated assumptions (hackathon-mode §7)` in place of the questions, record the assumptions in the report, and build the Recommended Actions from them. The `Questions skipped` line is the permitted ending in this mode; the Final-question gate below does not require questions here.",
    "A1(b) ask-block carve-out")

# A1(b) — skip rule exception
sub(crit,
    "- Skipping is allowed only when the report listed **fewer than 3 Priority Issues**. Count them; do not judge the findings \"straightforward\" by feel. At 3 or more, the questions are required.",
    "- Skipping is allowed only when the report listed **fewer than 3 Priority Issues**. Count them; do not judge the findings \"straightforward\" by feel. At 3 or more, the questions are required. (Except in a hackathon first build / one-prompt removal, where the carve-out above applies and questions are always skipped.)",
    "A1(b) skip-rule exception")

# A1(b) — final-question gate, first-build skip line
sub(crit,
    "**Final-question gate.** The user-visible response must either include the targeted questions or carry the literal line `Questions skipped: <reason>` naming the count that permitted the skip.",
    "**Final-question gate.** The user-visible response must either include the targeted questions or carry the literal line `Questions skipped: <reason>` naming the count that permitted the skip. In a hackathon first build / one-prompt removal, the permitted skip line is `Questions skipped: first build — proceeding on stated assumptions (hackathon-mode §7)` (see the carve-out above); the count rule does not apply there.",
    "A1(b) final-question gate")

# A1(b) — Recommended Actions intro, no answers in first build
sub(crit,
    "**After receiving the user's answers**, present a prioritized action summary reflecting the user's priorities and scope from Ask the User.",
    "**After receiving the user's answers**, present a prioritized action summary reflecting the user's priorities and scope from Ask the User. In a hackathon first build / one-prompt removal there are no answers — build the summary from the stated assumptions in the carve-out above instead.",
    "A1(b) recommended-actions intro")

# A1(c) — slug step: critique-storage has no plugin equivalent -> skip
sub(crit,
    "2. **Confirm the target slugs cleanly**:\n   ```bash\n   .cursor/skills/impeccable/scripts/impeccable critique-storage slug \"<resolved-path-or-url>\"\n   ```\n   Every later command also accepts the resolved target directly and derives the same slug internally; never hand-write a slug. If this exits non-zero, skip persistence and trend for this run, but continue the critique.",
    "2. **Confirm the target**: resolve it to its path or URL (see step 1) and pass the resolved target directly to later commands; never hand-write a slug. In this plugin there is no `critique-storage` helper, so there is no slug to confirm and no persistence or trend for this run — skip both and continue the critique.",
    "A1(c) slug step -> skip")

# A1(c) — detect --json -> pinned npx form
sub(crit,
    ".cursor/skills/impeccable/scripts/impeccable detect --json [target]",
    "npx impeccable@4.8.0 detect --json [target]",
    "A1(c) detect --json -> pinned")

# A1(c) — live-server block -> skip
sub(crit,
    "4. If mutation is available, start `.cursor/skills/impeccable/scripts/impeccable live-server --background`, present the browser if supported, label `[Human]`, scroll top, inject `http://localhost:PORT/detect.js`, wait 2-3 seconds, read `impeccable` console messages, then run `.cursor/skills/impeccable/scripts/impeccable live-server stop --keep-inject`. The overlay went in through the browser, so the project's HTML has no script tag to strip; a bare `stop` also runs `live-inject --remove` against the project's entry file, an edit a read-only critique should not make.",
    "4. If mutation is available, skip the live-server overlay — it is not wired in this plugin. Rendered-URL scans use the running app's URL instead (see `polish-pass/SKILL.md:89`): run `npx impeccable@4.8.0 detect <running-app-URL>` and read its findings; do not inject anything into the page and do not start a live server.",
    "A1(c) live-server block -> skip")

# A1(c) — detect --cdp -> pinned npx form
sub(crit,
    "Run `.cursor/skills/impeccable/scripts/impeccable detect --cdp 9222 --target <part of the page URL or title> --json`.",
    "Run `npx impeccable@4.8.0 detect --cdp 9222 --target <part of the page URL or title> --json`.",
    "A1(c) detect --cdp -> pinned")

# A1(c) — Persist the Snapshot section -> skip (markers to next section)
with open(crit, encoding="utf-8") as f:
    text = f.read()
start = text.index("### Persist the Snapshot\n")
end = text.index("\n### Ask the User\n")
new_section = """### Persist the Snapshot

Persistence is not wired in this plugin: there is no `.impeccable/critique/` store and no `critique-storage` helper, so skip this whole section — do not write anything to `.impeccable/critique/`, do not pass `IMPECCABLE_CRITIQUE_META` anywhere, and do not print a trend line (there is no stored trend to read). The delivered report above is the record; polish-pass picks up the Priority Issues from the report in this run, not from stored frontmatter.

**Close the run.** Go to Ask the User below and emit the questions, or the `Questions skipped: <reason>` line when the count allows it — in a hackathon first build after grill-me, or a one-prompt removal of a first-build feature, use `Questions skipped: first build — proceeding on stated assumptions (hackathon-mode §7)` (see the carve-out there). The run is not complete until you do.
"""
text = text[:start] + new_section + text[end + 1:]
with open(crit, "w", encoding="utf-8") as f:
    f.write(text)
print("  applied A1(c) Persist section -> skip")

# A1(c) consequence — Deliver the Report trend-line sentence
sub(crit,
    "Persistence is not the end of the run. After it, the response continues with the trend line and the close.",
    "Persistence is skipped in this plugin (see Persist the Snapshot below), so there is no trend line — after the report, the run closes at Ask the User.",
    "A1(c) Deliver-the-Report trend sentence")

# ============ D1 + D2: orchestrate:182 ============
orch = os.path.join(ROOT, "new-skills/orchestrate/SKILL.md")
sub(orch,
    "pass the render-tier screenshots, the stamp theme/idea line, the theme file, and the hero review's findings as file paths",
    "pass the render-tier screenshots, the stamp theme/idea line, the theme file, and the hero review's findings (`.hallmark/hero-review.md`, written by the landing slice — see design-taste-frontend step 6) as file paths. If the render tier did not run, skip the finish review as a named step — record that it was skipped and judge the page from browser-qa's step-5 captures instead — and never return `recapture` in that case (there is nothing to recapture from)",
    "D1+D2 orchestrate:182")

# ============ D2(b) + D3: design-taste-frontend ============
taste = os.path.join(ROOT, "new-skills/design-taste-frontend/SKILL.md")
sub(taste,
    "Act on its first word (`ship` / `fix`); findings join the fix batch.",
    "Act on its first word (`ship` / `fix`); findings join the fix batch. Write the hero review's findings to `.hallmark/hero-review.md` in the project root as soon as the review returns, and update the file with how each finding was settled (fixed, or waived with its reason) when you act on it — the finish review in Verify reads this file, so it must list every finding and its settlement, not just the open ones.",
    "D2(b) hero-review file")

sub(taste,
    "The deal returns 3 themes from the 50-theme catalog (`references/hallmark/references/themes/`, `index.json`); pick the one whose material can carry the brief — read the theme file's header (paper/display/accent/posture), its `material` line, and its feel paragraph.",
    "The deal returns 3 themes from the 50-theme catalog (`references/hallmark/references/themes/`, `index.json`); pick the one whose material can carry the brief — read the theme file's header (paper/display/accent/posture), its `material` line, and its feel paragraph. After picking, log the pick so the next deal avoids it: `node <skill>/references/hallmark/scripts/theme.mjs log --entry '{\"theme\":\"<picked theme name>\",\"axes\":\"<paper>/<display>/<accent> triple from the deal line>\",\"prompt\":\"<the brief>\"}' --log .hallmark/log.json` — the deal reads the recent 3 log entries to avoid re-dealing recent themes and axes, and without the log entry that avoidance never works.",
    "D3 log-the-pick")

# ============ D4: polish.md + polish-pass SKILL.md ============
polish = os.path.join(ROOT, "round2-skills/polish-pass/reference/polish.md")
sub(polish,
    "Then run the Impeccable detector on the same paths: `npx impeccable@4.8.0 detect <paths> [--json]` (pinned; no API key, no LLM). It checks 62 rules ([reference/impeccable-detector-rules.json](reference/impeccable-detector-rules.json)) including rendered-page rules the static scan cannot see — run it against the running app's URL as well as the source when the app is running. Treat its findings the same way: evidence to verify, not verdicts.",
    "Then run the Impeccable detector on the same paths: `npx impeccable@4.8.0 detect <paths> [--json]` (pinned; no API key, no LLM). It checks 62 rules ([reference/impeccable-detector-rules.json](reference/impeccable-detector-rules.json)) including rendered-page rules the static scan cannot see — run it against the running app's URL as well as the source when the app is running. Treat its findings the same way: evidence to verify, not verdicts. If the Impeccable detector cannot run (engine download failure, SHA mismatch, or no network on first run), record that and proceed on the static detector's findings — never block the pass on it.",
    "D4 polish.md Step 2.2 fallback")
sub(polish,
    "Re-run the Impeccable detector too (`npx impeccable@4.8.0 detect <paths>`), and fix real findings the same way.",
    "Re-run the Impeccable detector too (`npx impeccable@4.8.0 detect <paths>`), and fix real findings the same way. If it cannot run here either, record that and proceed on the static detector's findings.",
    "D4 polish.md Step 5.2 fallback")

pskill = os.path.join(ROOT, "round2-skills/polish-pass/SKILL.md")
sub(pskill,
    "if a rendered-URL scan cannot find Chrome, set `CHROME_PATH` to the Chrome install.",
    "if a rendered-URL scan cannot find Chrome, set `CHROME_PATH` to the Chrome install. If the Impeccable detector cannot run (engine download failure, SHA mismatch, or no network on first run), record that and proceed on the static detector's findings — never block the pass on it.",
    "D4 SKILL.md non-negotiable 5 fallback")

# ============ D5: build.sh patch block (LAST, before STEP 5) ============
buildsh = os.path.join(ROOT, "build.sh")
with open(buildsh, encoding="utf-8") as f:
    btext = f.read()
anchor = "# STEP 5 — Counts"
assert btext.count(anchor) == 1, f"STEP 5 anchor found {btext.count(anchor)}x"
block = """# --- Fix program #12 (D5): orch-change-feature routes landing redesigns
# through the Hallmark redesign flow. Upstream ECC file, copied fresh on every
# build — this fix lives here as a patch block placed LAST — just before
# STEP 5 — after the GATE patch and all earlier patch blocks. The anchor is
# the "Removing a feature" heading the B20 patch creates, so this block must
# run after it. Each substitution asserts exactly one match.
python3 - "$PLUGIN_DIR" <<'PYEOF'
import os, sys
base = sys.argv[1]
subs = [
  ("skills/orch-change-feature/SKILL.md",
   "## Removing a feature\\n\\nWhen the request is to remove a feature",
   \"\"\"## Landing redesigns

When the change is a redesign of the landing/company page — a new visual direction that keeps every fact, link, form, field, handler, route, id, and test hook — route the design work through the Hallmark redesign flow: `skills/design-taste-frontend/SKILL.md` (redesign paragraph before step 5) and the procedure in `references/hallmark/references/redesign.md`. Record the before-state first (`sloplint --before`, links/fields/handlers/headings + screenshots to `.hallmark/before*`), build, then `sloplint --kept` — anything lost is `FAIL kept` / `WARN kept`. Depths: **full** (system + composition change; default), **restyle** (system only, keep the layout), **polish** (only what a gate names). A dashboard/app-surface change is not a landing redesign — route that to `ui-ux-pro-max` instead. The engine steps above still run (tests first, gates auto-approve during a hackathon first build after grill-me or a one-prompt removal); the redesign flow owns only the design work.

## Removing a feature

When the request is to remove a feature\"\"\"),
]
for rel, old, new in subs:
    p = os.path.join(base, rel)
    text = open(p, encoding="utf-8").read()
    assert text.count(old) == 1, f"{rel}: pattern not found exactly once: {old[:60]!r}"
    open(p, "w", encoding="utf-8").write(text.replace(old, new))
print("fix12: orch-change-feature landing-redesign routing applied")
PYEOF

"""
btext = btext.replace(anchor, block + anchor, 1)
with open(buildsh, "w", encoding="utf-8") as f:
    f.write(btext)
print("  applied D5 build.sh patch block (LAST, before STEP 5)")

print("fix12: all staged edits + build.sh block applied")
