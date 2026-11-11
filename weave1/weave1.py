#!/usr/bin/env python3
"""Weave program #1 — connection/weaving loop (ordered Nov 10, ~23:05 CST).

Adds the useful connections the four mapping workers found (build/deploy/demo
chain, design bundle, core flow, long-tail census), plus the dry-run #11
observation #2 fix (re-dealt pick gets logged too).

Applies staged-source edits (each substitution asserts exactly one match)
and inserts the weave1 build.sh patch block (upstream ECC files + the
skill-triggers JSON) LAST, just before STEP 5.
Run from ~/workspace/hackathon-plugin as: python3 weave1/weave1.py
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


# ============================================================================
# PART A — staged sources (edited directly; STEP 2 copies them verbatim)
# ============================================================================

# ---- A1: orchestrate (new-skills/orchestrate/SKILL.md) ----
orch = os.path.join(ROOT, "new-skills/orchestrate/SKILL.md")

# W4-G13(c4): narration-key wording — pitch-deck-video is canonical.
sub(orch,
    "Record `KEY-RECEIPT` as a boolean in `.hackathon/run-ledger.md` (received: yes/no — NEVER the key value).",
    "Record `KEY-RECEIPT` as a boolean in `.hackathon/run-ledger.md` (received: yes/no — NEVER the key value). (Wording: `pitch-deck-video`'s narration-key prompt section is canonical — use its wording.)",
    "O1 step-0 narration canonical cross-ref")

# W1-G1: slicing reads the expansion list from its carrier file first.
sub(orch,
    "3. **Slice** — decompose the approved scope (MVP slices plus approved expansions) into dispatchable pieces, per the routing rule below.",
    "3. **Slice** — read the planner-approved expansion list from `docs/expansion.md` if it exists there, else from the expansion section of `.hackathon/run-ledger.md`, then decompose the approved scope (MVP slices plus approved expansions) into dispatchable pieces, per the routing rule below.",
    "O2 step-3 expansion-list carrier")

# W1-G7: slice briefs name the integration skill.
sub(orch,
    "**Scaffold owner:** the first-wave slice is the scaffold slice, built via `app-scaffold` — it owns the scaffold and the final layout (feature-expansion Phase 4's \"the scaffold owns the final layout\" anchors here).",
    "**Scaffold owner:** the first-wave slice is the scaffold slice, built via `app-scaffold` — it owns the scaffold and the final layout (feature-expansion Phase 4's \"the scaffold owns the final layout\" anchors here). **Integration skill in every slice brief:** the brief of any slice that wires an integration names `integration` (for the decision record's named API/SDK/tool) or `api-integration` (for unnamed REST mechanics) as its operating skill.",
    "O3 step-3 integration skill in briefs")

# W4-G9: TDD named in briefs; evidence path picked (tdd-workflow Step 8).
sub(orch,
    "Every implementer brief carries a soft time budget matching its effort estimate (S/M/L, per feature-expansion Phase 4) — and that budget is a real cap, not guidance: when it is spent, the implementer reports `BLOCKED` with partial evidence and stops; it does not grind past it.",
    "Every implementer brief carries a soft time budget matching its effort estimate (S/M/L, per feature-expansion Phase 4) — and that budget is a real cap, not guidance: when it is spent, the implementer reports `BLOCKED` with partial evidence and stops; it does not grind past it. **TDD in every brief:** each implementer brief names `tdd-guide` — tests first (red → green → refactor) for the slice's new/changed behaviour — and test evidence goes to `docs/releases/<version>/<name>.tdd.md` (the orchestrator's pick from tdd-workflow Step 8's three paths), cited in the final report.",
    "O4 step-4 TDD in briefs + evidence path")

# W4-G8: council verdict reaches the orchestrator via the ledger.
sub(orch,
    "The **stage ledger** stays a short run-state file (20 lines max), not a PRD.",
    "The **stage ledger** stays a short run-state file (20 lines max), not a PRD. When a go/no-go or tradeoff decision goes to `council`, record its verdict — consensus, strongest dissent, recommendation — in the stage ledger; the verdict feeds your synthesis, it is not only a reply to the user.",
    "O5 council verdict to ledger")

# W1-G3: Verify outcomes recorded in the ledger.
sub(orch,
    "5. **Verify → polish → deploy → demo, in that order** — four sub-steps inside this one step, never reordered (polish runs after verification and before deploy; deploy runs before demo):",
    "5. **Verify → polish → deploy → demo, in that order** — four sub-steps inside this one step, never reordered (polish runs after verification and before deploy; deploy runs before demo). Record each Verification-stage check's outcome as one ledger line (check name, findings count, fixed/blocked counts) in `.hackathon/run-ledger.md` before proceeding to polish.",
    "O6 step-5 Verify outcomes to ledger")

# W1-G6: polish target + 10-list carrier.
sub(orch,
    "   - **5b. Final polish** — after the Verification stage and before deploy, run `polish-pass` on the built UI. It returns the 10 highest-impact REMAINING improvements, prioritized by impact/effort/risk;",
    "   - **5b. Final polish** — after the Verification stage and before deploy, run `polish-pass` on the built UI at the project root (its local dev-server URL). It returns the 10 highest-impact REMAINING improvements, prioritized by impact/effort/risk, recorded in `.hackathon/run-ledger.md`;",
    "O7 step-5b polish target + ledger")

# W1-G5 + W4-G1 + W4-G12: deploy URL/path to ledger; security-review gate at 5c.
sub(orch,
    "   - **5c. Deploy** — deploy the app (`deploy-fast`).",
    "   - **5c. Deploy** — deploy the app (`deploy-fast`). Before the final deploy, run the `security-review` pre-deployment checklist (deploy-fast Timing rule) and record pass/blockers in the final report. Record the production URL and the deploy path used (Vercel CLI link, git-linked push, Railway, static-only, or blocked with the failing command and error) in `.hackathon/run-ledger.md`.",
    "O8 step-5c deploy URL + security gate")

# W1-G2 + W4-G2 + W4-G3: commit before the report; readme inputs; order line.
sub(orch,
    "6. **README, then final report** — invoke `readme-writer` to write the README first (after the build, before the final report — `devpost-autofiller` writes the Devpost submission from it, so the README must exist first); then write the final report — orchestrate owns it; see the concluding step at the end of this skill. Order: verify → polish → deploy → demo video → README → final report.",
    "6. **Commit, README, then final report** — commit each landed slice as a conventional `feat:` commit via orch-pipeline Phase 6 (Gate 2 auto-approves in a first build) before writing the final report; invoke `readme-writer` to write the README first (after the build, before the final report — `devpost-autofiller` writes the Devpost submission from it, so the README must exist first), passing it the deployed URL from the ledger and the video file path `<app-name>-video/out/demo.mp4` as inputs, so the README links the real URL and video instead of a placeholder; then write the final report — orchestrate owns it; see the concluding step at the end of this skill. Order: verify → polish → deploy → demo video → commit → README → final report.",
    "O9 step-6 commit + readme inputs")

# W4-G7: the deferred six get their named end-of-project invocation.
sub(orch,
    "Order: verify → polish → deploy → demo video → commit → README → final report.",
    "Order: verify → polish → deploy → demo video → commit → README → final report.\n\n**End-of-project checks (before the final report).** After deploy, demo, commit, and README, run the six deferred checks by name — `verification-loop`, `production-audit`, `delivery-gate`, `codehealth-mcp`, `santa-method`, `security-scan` — and record each result in the final report (check name, pass/fail, findings count). This is the deferred set's named end-of-project invocation (orchestrate process rule); it is not a user gate and never waits on anything.",
    "O9b end-of-project checks invocation")

# W4-G10: the blind reviewer in the Verification stage is code-reviewer.
sub(orch,
    "2. **Not cheaply verifiable** (and below the step-3 line) → spawn a **blind reviewer that has not seen the implementation conversation** (fast-worker tier default) — give it only the diff and the contract's acceptance criteria.",
    "2. **Not cheaply verifiable** (and below the step-3 line) → spawn a **blind `code-reviewer` that has not seen the implementation conversation** (fast-worker tier default) — give it only the diff and the contract's acceptance criteria.",
    "O10 Verification stage names code-reviewer")

# W2-G3: sloplint --json summary into the Verify fix list.
sub(orch,
    "Fix every `FAIL`; fix or waive every `REFLEX` (waivers on the record, in the CSS stamp).",
    "Fix every `FAIL`; fix or waive every `REFLEX` (waivers on the record, in the CSS stamp). Run sloplint with `--json` and paste its summary counts into the Verify fix list, so the FAIL/REFLEX/waiver list survives as a durable record, not just stdout.",
    "O11 sloplint --json into fix list")

# W2-G4: render-absent branch passes the hero review to browser-qa.
sub(orch,
    "If the render tier did not run, skip the finish review as a named step — record that it was skipped and judge the page from browser-qa's step-5 captures instead — and never return `recapture` in that case (there is nothing to recapture from)",
    "If the render tier did not run, skip the finish review as a named step — record that it was skipped and judge the page from browser-qa's step-5 captures instead, passing `.hallmark/hero-review.md` to the browser-qa visual loop as an input file — and never return `recapture` in that case (there is nothing to recapture from)",
    "O12 hero-review.md to browser-qa in skip branch")

# W4-G1: Deployed URL bullet in the final report.
sub(orch,
    "- **Important design + engineering decisions** — each decision that shaped the product (architecture, data model, key trade-offs, what was chosen and what was rejected and why), one line each, taken from the stage ledger's Decided/Rejected fields.",
    "- **Deployed URL** — the production URL from the ledger (plus the deploy path used), or the blocked-deploy note with the failing command and error.\n- **Important design + engineering decisions** — each decision that shaped the product (architecture, data model, key trade-offs, what was chosen and what was rejected and why), one line each, taken from the stage ledger's Decided/Rejected fields.",
    "O13 final report: Deployed URL bullet")

# W4-G6 + W4-G7: adversarial findings + end-of-project checks bullets.
sub(orch,
    "- **Highest-value next improvements** — the top remaining improvements from the final polish list (whatever `polish-pass` ranked highest and was not implemented), plus planner-noted gaps, prioritized by impact/effort/risk, one line each.",
    "- **Adversarial audit findings** — every blocker/major/minor from the adversarial audit, each with its CONFIRMED/SUSPECTED label and fixed-or-open status (minors live here, not just in the audit step).\n- **End-of-project checks** — one line per deferred check (`verification-loop`, `production-audit`, `delivery-gate`, `codehealth-mcp`, `santa-method`, `security-scan`): pass/fail and findings count.\n- **Highest-value next improvements** — the top remaining improvements from the final polish list (whatever `polish-pass` ranked highest and was not implemented), plus planner-noted gaps, prioritized by impact/effort/risk, one line each.",
    "O14 final report: adversarial + end-of-project bullets")

# W4-G3 + W4-G5: exact video path + narration record in the demo handoff.
sub(orch,
    "- **Demo video handoff** — the video file path AND the instruction \"upload this file to YouTube/Vimeo and paste the link into Devpost\" (the first build cannot upload the video — that needs the user's YouTube/Devpost account — so the report hands the file to the user with that instruction).",
    "- **Demo video handoff** — the video file path (`<app-name>-video/out/demo.mp4`) AND the instruction \"upload this file to YouTube/Vimeo and paste the link into Devpost\" (the first build cannot upload the video — that needs the user's YouTube/Devpost account — so the report hands the file to the user with that instruction). Also the narration record: ElevenLabs usage remaining (`src/elevenlabs-usage.json`), narration status per line-set, the provider decision-log entries, and the music credit (`public/music/SOURCE.txt`).",
    "O15 final report: demo handoff exact path + narration record")

# ---- A2: feature-expansion (new-skills/feature-expansion/SKILL.md) ----
fexp = os.path.join(ROOT, "new-skills/feature-expansion/SKILL.md")

# W3-1: ai-feature-spec gets its routing branch (the AI half was unrouted).
sub(fexp,
    "If a feature needs a named API, SDK, or tool wired in, use `integration`; if it needs generic REST-client mechanics on an unnamed API, use `api-integration`; if it needs auth or a database, use `app-scaffold`; if it needs to be live, use `deploy-fast`.",
    "If a feature needs a named API, SDK, or tool wired in, use `integration`; if it needs generic REST-client mechanics on an unnamed API, use `api-integration`; if it needs auth or a database, use `app-scaffold`; if it needs to be live, use `deploy-fast`. If a feature is AI-powered (model choice, prompt/context contracts, output schema, fallbacks, eval), use `ai-feature-spec`.",
    "F1 ai-feature-spec routing branch")

# W3-1: ai-feature-spec row in the routing table.
sub(fexp,
    "| Integrations a feature needs | `integration` (named API/SDK/tool), `api-integration` (generic REST-client mechanics on an unnamed API), `app-scaffold`, `deploy-fast` |",
    "| Integrations a feature needs | `integration` (named API/SDK/tool), `api-integration` (generic REST-client mechanics on an unnamed API), `app-scaffold`, `deploy-fast` |\n| AI-powered feature spec | `ai-feature-spec` (model, prompt, fallbacks, eval) |",
    "F2 ai-feature-spec table row")

# W1-G4: Phase 6 overflow file for the Landed/Blocked inventory.
sub(fexp,
    "Handoff mechanism: write this section to `.hackathon/run-ledger.md` (expansion section, within the ledger's ≤20 lines — long tables go in the return text instead) AND include it in the Phase 6 return text (landed / blocked / rejected lists).",
    "Handoff mechanism: write this section to `.hackathon/run-ledger.md` (expansion section, within the ledger's ≤20 lines — if the Phase 6 section exceeds the ledger's 20 lines, append the full Landed/Blocked lists (with files) to `docs/expansion.md` and leave a one-line pointer in the ledger; long tables go in the return text instead) AND include it in the Phase 6 return text (landed / blocked / rejected lists).",
    "F3 Phase 6 overflow to docs/expansion.md")

# ---- A3: design-taste-frontend (new-skills/design-taste-frontend/SKILL.md) ----
taste = os.path.join(ROOT, "new-skills/design-taste-frontend/SKILL.md")

# Dry-run #11 observation #2 (parent-verified real gap): a re-dealt final
# pick gets logged too.
sub(taste,
    "If the dealt theme clashes with the client's own logo or photographs, re-deal once (`--reroll 1`); the client's own colours go through `start.mjs brand` instead.",
    "If the dealt theme clashes with the client's own logo or photographs, re-deal once (`--reroll 1`); the client's own colours go through `start.mjs brand` instead. If you re-deal, log the re-dealt pick too — the log must record the theme actually built, not the first pick.",
    "T1 re-dealt pick gets logged too")

# W2-G2: the log entry carries every field theme.mjs reads.
sub(taste,
    "After picking, log the pick so the next deal avoids it: `node <skill>/references/hallmark/scripts/theme.mjs log --entry '{\"theme\":\"<picked theme name>\",\"axes\":\"<paper>/<display>/<accent> triple from the deal line>\",\"prompt\":\"<the brief>\"}' --log .hallmark/log.json` — the deal reads the recent 3 log entries to avoid re-dealing recent themes and axes, and without the log entry that avoidance never works.",
    "After picking, log the pick so the next deal avoids it: `node <skill>/references/hallmark/scripts/theme.mjs log --entry '{\"theme\":\"<picked theme name>\",\"axes\":\"<paper>/<display>/<accent> triple from the deal line>\",\"prompt\":\"<the brief>\",\"shape\":\"<dealt hero/layout shape>\",\"hero\":\"<hero posture>\",\"nav\":\"<nav form>\",\"footer\":\"<footer form>\",\"imagery\":\"<imagery plan>\",\"sections\":\"<section list>\",\"fingerprint\":\"<shape + axes fingerprint>\",\"signature\":\"<theme signature>\"}' --log .hallmark/log.json` — the deal reads the recent 3 log entries to avoid re-dealing recent themes and axes, and without the log entry that avoidance never works. Log every field `theme.mjs` reads (it warns `missing … which Rotation reads` for a short entry): take shape/hero/nav/footer/imagery/sections/fingerprint/signature from the deal, the theme file, and the plan — and if the build changes the shape, re-log with the settled values, so the repetition check (gates.md:187) reads the real page.",
    "T2 full log entry")

# W2-G10: the Picks block gets a file.
sub(taste,
    "and build exactly that (a short page drops what it has no section for: `sections.md` section 4).",
    "and build exactly that (a short page drops what it has no section for: `sections.md` section 4). Also write the deal's Picks block (Material and Signature rows) to `.hallmark/picks.md` in the project root — the hero review and finish review take those rows as file paths.",
    "T3 Picks block to .hallmark/picks.md")

# W2-G10: the hero review takes the Picks file as its path.
sub(taste,
    "pass the hero screenshots, the stamp's first two lines, and the Picks Material + Signature rows as file paths",
    "pass the hero screenshots, the stamp's first two lines, and the Picks block (`.hallmark/picks.md`, written at the deal — its Material + Signature rows) as file paths",
    "T4 hero review takes the Picks file")

# W2-G1: the dealt theme lands in design-tokens.md as the first two lines.
sub(taste,
    "Then write the frozen system to `docs/design-tokens.md` in the project root (one line each, same items) — this file is the durable single source of truth:",
    "Then write the frozen system to `docs/design-tokens.md` in the project root (one line each, same items) — first two lines are the dealt Hallmark theme: its slug, its Tokens block values, and its palette balance, so a later slice briefing from this file alone can recover which theme (and its Range/material) the landing used — and this file is the durable single source of truth:",
    "T5 theme slug/Tokens into design-tokens.md")

# W2-C3: token rule on landing — gates.md 48/24a is canonical.
sub(taste,
    "**colour palette + semantic tokens** (ink, `--action`, `--g-main`/`--g-alt`/`--g-dark`, `--muted` — what each token MEANS, e.g. action, success, error, disabled — `system.md` Colour);",
    "**colour palette + semantic tokens** (ink, `--action`, `--g-main`/`--g-alt`/`--g-dark`, `--muted` — what each token MEANS, e.g. action, success, error, disabled — `system.md` Colour; no raw hex in components — gates.md 48/24a governs on landing);",
    "T6 token rule cites gates.md 48/24a")

# W2-C6: one button pair / one card style — gates.md F4/F15 on landing.
sub(taste,
    "**component hierarchy** (which components exist, which are primary vs. secondary, one button pair / one card style / one radius scale — `system.md` Radius and buttons, Cards);",
    "**component hierarchy** (which components exist, which are primary vs. secondary, one button pair / one card style / one radius scale — `system.md` Radius and buttons, Cards; gates.md F4/F15 governs on landing);",
    "T7 one-accent rule cites gates.md F4/F15")

# W2-C1: the gradient-text conflict — Hallmark gate 2b governs on landing.
sub(taste,
    "Also read the Impeccable craft floor (`skills/polish-pass/reference/impeccable-craft-floor.md` in the plugin) before building any UI: its bans are absolute — a pinned brief never overrides a ban — and where it and this skill disagree, the stricter ban wins.",
    "Also read the Impeccable craft floor (`skills/polish-pass/reference/impeccable-craft-floor.md` in the plugin) before building any UI: its bans are absolute — a pinned brief never overrides a ban — and where it and this skill disagree, the stricter ban wins — except that on a landing page Hallmark gate 2b's guarded single-hue gradient-text ramp is permitted (gates.md §4 governs there; the polish detector's gradient-text tell does not apply to it).",
    "T8 gate 2b exception to stricter-ban-wins")

print("weave1: Part A staged edits (orchestrate, feature-expansion, taste) applied")

# ---- A4: pitch-deck-video (new-skills/pitch-deck-video/SKILL.md) ----
pdv = os.path.join(ROOT, "new-skills/pitch-deck-video/SKILL.md")

# W4-G14: the cost-tracker citation is a dead end — the files are not shipped.
sub(pdv,
    "Anything paid (Runway, Veo, HeyGen, ElevenLabs beyond\nthe free tier, and similar) follows these rules, adapted from\nOpenMontage's cost tracker (`tools/cost_tracker.py`, `config.yaml`):",
    "Anything paid (Runway, Veo, HeyGen, ElevenLabs beyond\nthe free tier, and similar) follows these rules — the skill's own budget rules, adapted from OpenMontage's cost-tracker design (the tracker script and config are not shipped in this plugin):",
    "P1 cost rules are the skill's own (no dead citation)")

# W4-G5: usage / decision-log / music credit reach the final report.
sub(pdv,
    "if the line would take it past 10,000, that line falls back to Piper\n  instead. Check the remaining quota before starting a video and tell the\n  user where it stands.",
    "if the line would take it past 10,000, that line falls back to Piper\n  instead. Check the remaining quota before starting a video and tell the\n  user where it stands. Hand the usage remaining, the narration status per line-set, the `decision-log.md` entries, and the music credit (`public/music/SOURCE.txt`) to the final report via the /demo return — they are inputs to the report's demo-video handoff, not chat-only numbers.",
    "P2 usage/decision-log/credit to the final report")

# ---- A5: deploy-fast (rewritten-skills/deploy-fast/SKILL.md) ----
dfast = os.path.join(ROOT, "rewritten-skills/deploy-fast/SKILL.md")

# W4-G13(c1): the pre-pitch checklist cannot hard-stop a first build (§7).
sub(dfast,
    "> This checklist gates the **final** deploy, not the first-hour deploy — ship a hello-world URL in the first hour first, then work through this list before the pitch-ready deploy.",
    "> This checklist gates the **final** deploy, not the first-hour deploy — ship a hello-world URL in the first hour first, then work through this list before the pitch-ready deploy. During a hackathon first build after grill-me, or a one-prompt removal of a first-build feature, an item that cannot be completed is recorded as blocked in the final report instead of stopping the deploy (hackathon-mode §7).",
    "D1 pre-pitch checklist §7 carve-out")

# W4-G13(c3): proxy.ts is route protection; middleware.ts is session refresh.
sub(dfast,
    "4. ✏️ On **Next.js 16+**, route protection lives in **`proxy.ts`**, not `middleware.ts`.",
    "4. ✏️ On **Next.js 16+**, route protection lives in **`proxy.ts`**, not `middleware.ts`. (Route protection only — the Supabase session-refresh middleware in `app-scaffold` is a separate job, not route protection.)",
    "D2 proxy.ts vs session-refresh middleware")

# ---- A6: app-scaffold (rewritten-skills/app-scaffold/SKILL.md) ----
scaf = os.path.join(ROOT, "rewritten-skills/app-scaffold/SKILL.md")

# W4-G13(c3): middleware.ts is session refresh, not route protection.
sub(scaf,
    "- `middleware.ts` — refreshes the auth session cookie on every request",
    "- `middleware.ts` — refreshes the auth session cookie on every request (session refresh only — route protection itself lives in `proxy.ts` on Next.js 16+ per `deploy-fast` Auth §4)",
    "A6 middleware.ts cross-ref to deploy-fast")

# ---- A7: readme-writer (rewritten-skills/readme-writer/SKILL.md) ----
rw = os.path.join(ROOT, "rewritten-skills/readme-writer/SKILL.md")

# W4-G2: the README takes its URL + video path from the ledger, not a TODO.
sub(rw,
    "a deployed URL in config, CI workflows. Reuse it.",
    "a deployed URL in config, CI workflows. Reuse it. **Deployed URL and demo video path:** in a first build, take them from `.hackathon/run-ledger.md` (the deployed-URL line; the video path is `<app-name>-video/out/demo.mp4`) — when the ledger names them, write the real links, never a `<!-- TODO: add demo link -->` placeholder.",
    "R1 readme URL + video path from the ledger")

# ---- A8: polish-pass reference files (round2-skills/polish-pass/) ----
polish = os.path.join(ROOT, "round2-skills/polish-pass/reference/polish.md")

# W2-G12: Step 1 reads the token file as the source of truth.
sub(polish,
    "1. Read the target's design system (SKILL.md → Design system): the project's tokens, theme file, and shared components, plus who the product is for and what the target must do. If the project has no recorded tokens, infer the system from the code and proceed.",
    "1. Read the target's design system (SKILL.md → Design system): read `docs/design-tokens.md` when it exists (else `design-system/<project-slug>/MASTER.md`) as the token source of truth, plus the project's theme file and shared components, and who the product is for and what the target must do. If the project has no recorded tokens, infer the system from the code and proceed.",
    "PM1 Step 1 reads design-tokens.md")

# W2-G5 + W2-G6: detector findings get their durable list; the 10-list
# gets its template slot.
sub(polish,
    "### Accepted detector findings\n- <rule> at <file:line>: <why it's safe, and how you verified it> (omit if none)\n\n### Still short of 10/10",
    "### Accepted detector findings\n- <rule> at <file:line>: <why it's safe, and how you verified it> (omit if none)\n\nList every real Impeccable detector finding here, fixed and left open, with its rule id and file:line — this section is the findings' durable record, not the detector's stdout.\n\n### 10 highest-impact REMAINING improvements\n1. <highest-impact remaining improvement, with impact/effort/risk>\n2. …\n\nRanked by impact/effort/risk; this is the list orchestrate's final report consumes as highest-value next improvements.\n\n### Still short of 10/10",
    "PM2 detector-findings list + 10-list section")

vibes = os.path.join(ROOT, "round2-skills/polish-pass/reference/patterns/vibe-code-tells.md")

# W2-C1: the detector's gradient-text tell does not apply to a guarded 2b ramp.
sub(vibes,
    "1. Run `node <skill dir>/scripts/detect.mjs <paths>` (catches emoji icons, gradient text, slop gradients, and some others).",
    "1. Run `node <skill dir>/scripts/detect.mjs <paths>` (catches emoji icons, gradient text, slop gradients, and some others). On a landing page, a guarded single-hue gradient-text ramp (Hallmark gate 2b: stops within 40°, both stops tokens) is permitted, not a tell — do not flag it.",
    "V1 gate 2b exception in the detector tell")

# ---- A9: Hallmark staged references (new-skills/design-taste-frontend/) ----
hall = os.path.join(ROOT, "new-skills/design-taste-frontend/references/hallmark/references")
hscripts = os.path.join(ROOT, "new-skills/design-taste-frontend/references/hallmark/scripts")

gates = os.path.join(hall, "gates.md")

# W2 dead-ends: the companion docs gates.md cites are not staged — say so
# once, at the top, instead of leaving 20 dangling citations.
sub(gates,
    "# Gates\n",
    "# Gates\n\n**Staged-scope note (this plugin):** the companion Hallmark docs this file cites (`layout.md`, `craft.md`, `imagery.md`, `anatomy.md`, `macrostructures.md`, `direction.md`, `fonts.md`, `flow.md`, `patterns.md`, `interaction-and-states.md`, `export-formats.md`) are NOT staged in this plugin — where a gate cites one, the staged Hallmark files (`hallmark-floor.md`, `review-hero.md`, `review-finish.md`, `redesign.md`) and the plugin skills govern instead; a citation to an unstaged file is never a reason to stop the build.\n",
    "G1 gates.md staged-scope note")

redesign = os.path.join(hall, "redesign.md")

# W2 dead-ends: redesign.md cites a locked design.md / design-md.md that
# has no such convention in the plugin.
sub(redesign,
    "A locked `design.md` is the system at every depth.",
    "A locked design system (`docs/design-tokens.md` on a landing build, `design-system/<project-slug>/MASTER.md` on a dashboard-only build) is the system at every depth.",
    "RD1 locked design.md -> design-tokens.md / MASTER.md")

# W2 dead-ends: redesign.md prescribes theme.mjs scaffold — the command
# Taste forbids.
sub(redesign,
    "- **Restyle and full** start from the scaffold, with the depth in the stamp: `theme.mjs scaffold <slug> --redesign <depth>`, or `scaffold --brand --redesign <depth>` for a kept brand, its tokens filled from the palette and faces the pre-flight found (no `check`: the coordinates are the user's); add `--scope app` for app screens. It writes `tokens.css` and `base.css` beside the project's stylesheet and prints the imports that fit it (`export-formats.md` has the Tailwind and shadcn names).",
    "- **Restyle and full** start from the project's existing scaffold, with the depth in the stamp — do not run `theme.mjs scaffold` in this plugin (Taste owns shape and scaffold); for a kept brand, its tokens are filled from the palette and faces the pre-flight found (no `check`: the coordinates are the user's); add `--scope app` for app screens. It writes `tokens.css` and `base.css` beside the project's stylesheet and prints the imports that fit it.",
    "RD2 no theme.mjs scaffold in redesigns")

sub(redesign,
    "- **More than one page** at restyle or full: lock the system once the scaffold has run (`design-md.md`). Every page reads it and the variety rule inverts: pages share theme, type and accent, and differ only in shape. One stylesheet for several pages lists a hero posture per route, `hero: Settled (/), Stage (/contact)`. Past three pages, give each page to its own subagent where the harness has them, with `design.md`, the page's files and this file.",
    "- **More than one page** at restyle or full: lock the system once the scaffold has run (in `docs/design-tokens.md`, or `design-system/<project-slug>/MASTER.md` on a dashboard-only build). Every page reads it and the variety rule inverts: pages share theme, type and accent, and differ only in shape. One stylesheet for several pages lists a hero posture per route, `hero: Settled (/), Stage (/contact)`. Past three pages, give each page to its own subagent where the harness has them, with that tokens file, the page's files and this file.",
    "RD3 design-md.md -> tokens file")

theme = os.path.join(hscripts, "theme.mjs")

# W2 dead-ends: theme.mjs deal stdout instructs the forbidden scaffold cmd.
sub(theme,
    "  console.log(`next: look at the pictures, pick the material this prompt wants, read references/themes/<slug>.md, then theme.mjs scaffold <slug> --dealt \"<n>/${picked.length}, seed ${seedKey}\"`);",
    "  console.log(`next: look at the pictures, pick the material this prompt wants, read references/themes/<slug>.md, then build with Taste — do not run theme.mjs scaffold in this plugin (Taste owns shape and scaffold)`);",
    "TH1 deal stdout no longer instructs scaffold")

print("weave1: Part A staged edits (pitch-deck-video, deploy-fast, app-scaffold, readme-writer, polish-pass, hallmark) applied")

# ============================================================================
# PART B — build.sh patch block (upstream ECC files; runs LAST, before STEP 5)
# ============================================================================
buildsh = os.path.join(ROOT, "build.sh")
with open(buildsh, encoding="utf-8") as f:
    btext = f.read()
anchor = "# STEP 5 — Counts"
assert btext.count(anchor) == 1, f"STEP 5 anchor found {btext.count(anchor)}x"
block = r'''# --- Weave program #1: connection/weaving loop (ordered Nov 10, ~23:05 CST).
# Upstream ECC files, copied fresh on every build — these fixes live here as
# a patch block placed LAST — just before STEP 5 — after the GATE patch and
# all earlier patch blocks. Each substitution asserts exactly one match.
# Staged-source edits live in weave1/weave1.py Part A; this block covers
# only files no staged source owns, plus the skill-triggers JSON.
python3 - "$PLUGIN_DIR" <<'PYEOF'
import json, os, sys
base = sys.argv[1]
subs = [
  # W1-G8: the approved task_list gets a durable file at Gate 1.
  ("skills/orch-pipeline/SKILL.md",
   """1. **GATE 1 — after Plan.** Present the `task_list`; do not write implementation
   code until the user approves — except during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature, where the gate auto-approves and the run proceeds without waiting.""",
   """1. **GATE 1 — after Plan.** Present the `task_list`; do not write implementation
   code until the user approves — except during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature, where the gate auto-approves and the run proceeds without waiting. Record the approved `task_list` (one line per slice, with its files) in `.hackathon/run-ledger.md` at Gate 1, so later phases read it from there instead of the transcript."""),
  # W4-G11: orch-build-mvp step 3 names app-scaffold.
  ("skills/orch-build-mvp/SKILL.md",
   """3. **Scaffold — orch-pipeline Phase 3.** Stand up the first end-to-end slice (the first thin vertical slice from orch-build-mvp step 1).""",
   """3. **Scaffold — orch-pipeline Phase 3.** Stand up the first end-to-end slice via `app-scaffold` (the first thin vertical slice from orch-build-mvp step 1)."""),
  # W1-G12 + W1-G15: GAN spec takes the expansion list; first UI slice
  # writes design-tokens.md.
  ("skills/orch-build-mvp/SKILL.md",
   """   - Translate the record/scope (or the fallback spec doc, if that was the input) into `gan-harness/spec.md` + `gan-harness/eval-rubric.md`
     (this stands in for what `gan-planner` would generate — you already have the spec).""",
   """   - Translate the record/scope (or the fallback spec doc, if that was the input) — plus the planner-approved expansion list from `docs/expansion.md` (or the ledger's expansion section) — into `gan-harness/spec.md` + `gan-harness/eval-rubric.md`
     (this stands in for what `gan-planner` would generate — you already have the spec). Have the first UI slice in the GAN loop write `docs/design-tokens.md` from its design system (per orchestrate's no-landing fallback) so later slices brief from real tokens."""),
  # W1-G13: reconcile reads the GAN loop's build report + feedback files.
  ("skills/orch-build-mvp/SKILL.md",
   """5. **Reconcile after each wave — this step owns collision reconciliation.** After each implementer wave, read every implementer's result (status, changed files, verification evidence, blockers); confirm the reported files exist, stayed in scope, and carry verification evidence.""",
   """5. **Reconcile after each wave — this step owns collision reconciliation.** After each implementer wave, read every implementer's result (status, changed files, verification evidence, blockers) — the GAN loop's results are `gan-harness/build-report.md` and `gan-harness/feedback/feedback-*.md`; read those files, not just the return texts; confirm the reported files exist, stayed in scope, and carry verification evidence."""),
  # W1-G14: the standalone flow gets its polish step (6b, before commit).
  ("skills/orch-build-mvp/SKILL.md",
   """Fix blockers and majors inside the capped 2-round fix loop; minors go in the final report.
7. **Commit — orch-pipeline Phase 6.**""",
   """Fix blockers and majors inside the capped 2-round fix loop; minors go in the final report.

6b. **Final polish — after verification and before the step-7 commit.** Run `polish-pass` on the built UI (same role as orchestrate step 5b: it implements the subset that materially increases quality without destabilizing the build, at most one fix round per item) and carry its 10 highest-impact remaining improvements into the step-9 final report.

7. **Commit — orch-pipeline Phase 6.**"""),
  # W4-G3 + W1-G5: step 8 records the deploy URL/path; exact video path.
  ("skills/orch-build-mvp/SKILL.md",
   """8. **Deploy via `deploy-fast`, then film via `/demo` (`pitch-deck-video`) — LOCAL only.** Deploy the working MVP; then film the LOCAL app from the project dir (`APP_DIR` to the app dir) — `/demo` never films the deployed URL, so do NOT set `shots.json` `app.url` to it. The demo video is a required deliverable.""",
   """8. **Deploy via `deploy-fast`, then film via `/demo` (`pitch-deck-video`) — LOCAL only.** Deploy the working MVP — record the production URL and the deploy path used in `.hackathon/run-ledger.md` (Vercel CLI link, git-linked push, Railway, static-only, or blocked with the failing command and error) — then film the LOCAL app from the project dir (`APP_DIR` to the app dir) — `/demo` never films the deployed URL, so do NOT set `shots.json` `app.url` to it. The demo video is a required deliverable; its file is `<app-name>-video/out/demo.mp4`."""),
  # W4-G6 + W4-G7: step 9 runs the deferred six and reports the deployed
  # URL, the adversarial findings, and the video handoff with its record.
  ("skills/orch-build-mvp/SKILL.md",
   """9. **Deliver the final report — this is the done signal.** Write it to `docs/final-report.md` in the project AND deliver it as the reply. State what was built, every assumption made, anything blocked or skipped, and anything the user may want to remove, with the files for each removable item (feature-to-files inventory — the inventory lives in that file).""",
   """9. **Deliver the final report — this is the done signal.** Before writing the report, run the six deferred end-of-project checks by name (`verification-loop`, `production-audit`, `delivery-gate`, `codehealth-mcp`, `santa-method`, `security-scan`) and record each result in the report (check name, pass/fail, findings count). Write it to `docs/final-report.md` in the project AND deliver it as the reply. State what was built, every assumption made, anything blocked or skipped, and anything the user may want to remove, with the files for each removable item (feature-to-files inventory — the inventory lives in that file). Also state the deployed URL from the ledger (or the blocked-deploy note), every adversarial-audit finding with its CONFIRMED/SUSPECTED label and fixed-or-open status, and the demo-video handoff: the video file path (`<app-name>-video/out/demo.mp4`) plus the narration record (ElevenLabs usage remaining, narration status per line-set, the provider decision-log entries, and the music credit)."""),
  # W1-G11: a landing redesign re-runs the hero review.
  ("skills/orch-change-feature/SKILL.md",
   """Depths: **full** (system + composition change; default), **restyle** (system only, keep the layout), **polish** (only what a gate names). A dashboard/app-surface change is not a landing redesign — route that to `ui-ux-pro-max` instead.""",
   """Depths: **full** (system + composition change; default), **restyle** (system only, keep the layout), **polish** (only what a gate names). A dashboard/app-surface change is not a landing redesign — route that to `ui-ux-pro-max` instead. After rebuilding a redesigned landing page, re-run the Hallmark hero review and update `.hallmark/hero-review.md` with the new findings and settlements before finishing — the old file holds pre-redesign findings, which Verify would otherwise read as current."""),
  # W1-G9: removal polls the URL the first build recorded.
  ("skills/orch-change-feature/SKILL.md",
   """Otherwise poll the deployed app until it serves the new version (no removed feature, no dangling references), with a BOUNDED wait — check every ~30s, stop after ~5 minutes.""",
   """Otherwise take the deployed URL and deploy path from `.hackathon/run-ledger.md` (or `docs/final-report.md` if the ledger is absent), then poll the deployed app until it serves the new version (no removed feature, no dangling references), with a BOUNDED wait — check every ~30s, stop after ~5 minutes."""),
  # W1-G10: pitch/Devpost refresh only where those artifacts exist.
  ("skills/orch-change-feature/SKILL.md",
   """the pitch narrative, scripts, and demo storyboard (`hackathon-pitch` — refresh them so the pitch no longer promises the removed feature), and the Devpost submission (`devpost-autofiller`) if one exists — if no Devpost submission exists yet there is nothing to update, say so in the final report rather than leaving it silently stale —""",
   """the pitch narrative, scripts, and demo storyboard (`hackathon-pitch` — refresh them only where those artifacts already exist, so the pitch no longer promises the removed feature; if no pitch artifacts exist yet, say so in the final report rather than leaving it silently stale), and the Devpost submission (`devpost-autofiller`) if one exists — if no Devpost submission exists yet there is nothing to update, say so in the final report rather than leaving it silently stale —"""),
  # W4-G4: remaining shots re-checked against the updated storyboard
  # before the re-film.
  ("skills/orch-change-feature/SKILL.md",
   """Then, before re-filming, update `shots.json` FIRST relative to the re-film — remove the feature's shots, selectors, and narration lines (FIRST means first before the re-film, not first in this step overall: the push/re-deploy above precedes it) — then re-film via `/demo --rebuild`,""",
   """Then, before re-filming, update `shots.json` FIRST relative to the re-film — remove the feature's shots, selectors, and narration lines (FIRST means first before the re-film, not first in this step overall: the push/re-deploy above precedes it) — then re-check every remaining shot against the updated demo storyboard in `docs/scope.md` (move the feature to the cut list first, so the storyboard is current): a shot whose feature was removed, or whose narration still promises the removed feature, is removed or rewritten before the re-film — then re-film via `/demo --rebuild`,"""),
  # W4-G13(c2): the interactive-login rule points at its canonical home.
  ("skills/orch-change-feature/SKILL.md",
   """Do not run an interactive deploy CLI for this step: if a deploy CLI is unauthenticated (or the project has no git-linked deploy), do not wait for a login""",
   """Do not run an interactive deploy CLI for this step (per `deploy-fast` — never stall on a login): if a deploy CLI is unauthenticated (or the project has no git-linked deploy), do not wait for a login"""),
  # W2-G7: browser-qa uses the polish-pass captures as its baseline.
  ("skills/browser-qa/SKILL.md",
   """2. Compare against committed baseline screenshots
   — no baseline ⇒ report INCONCLUSIVE, never a silent PASS""",
   """2. Compare against committed baseline screenshots — when `polish-pass` ran first, use `.polish-pass/captures/after/capture.json` + its PNGs as the committed baseline — no baseline ⇒ report INCONCLUSIVE, never a silent PASS"""),
  # W2 dead-ends: the browser-MCP tool names are harness-provided, not plugin.
  ("skills/browser-qa/SKILL.md",
   """Works with any browser MCP:
- `mChild__claude-in-chrome__*` tools (preferred — uses your actual Chrome)
- Playwright via `mcp__browserbase__*`
- Direct Puppeteer scripts""",
   """Works with any browser MCP:
- `mChild__claude-in-chrome__*` tools (preferred — uses your actual Chrome)
- Playwright via `mcp__browserbase__*`
- Direct Puppeteer scripts

(The `mChild__*` and `mcp__browserbase__*` tool names are provided by the harness, not by this plugin — no such MCP is defined here. If the harness provides neither, use direct Puppeteer scripts against the running app.)"""),
  # W2-G9: applied treatments get a durable record.
  ("skills/less-flat-ui/SKILL.md",
   """Put these in a `backgrounds.css` file (or a `<style>` block) and reference them by class. Do not cram data-URI SVGs into Tailwind arbitrary values.""",
   """Put these in a `backgrounds.css` file (or a `<style>` block) and reference them by class. Do not cram data-URI SVGs into Tailwind arbitrary values. Record every treatment applied, on which surface, in `docs/design-tokens.md` (or MASTER.md on a dashboard-only build) — later slices and polish-pass read the record from there, not from the CSS."""),
  # W2-C1: example hexes are placeholders — re-tint to the dealt palette.
  ("skills/less-flat-ui/SKILL.md",
   """## The 22 treatments

### 1. Felt texture""",
   """## The 22 treatments

Re-tint every example below to the project's dealt palette and tokens before using it — the hex values are placeholders, not the palette. Never copy a purple/violet gradient onto a landing page (Hallmark gate 2a and Taste §6 Never ban it); the craft floor's purple-blue-gradient ban applies the same way on app surfaces.

### 1. Felt texture"""),
  # W2-C4: the touch floor is 44px, not 40-ideal-44.
  ("skills/make-interfaces-feel-better/SKILL.md",
   """Interactive controls should have at least a 40x40px hit area, ideally 44x44px
where the layout allows it. Expand with a pseudo-element when the visible icon
is smaller, but do not let expanded hit areas overlap.""",
   """Interactive controls must have at least a 44x44px hit area (the plugin floor — quick-reference §2). Expand with a pseudo-element when the visible icon is smaller, but do not let expanded hit areas overlap."""),
  # W2-C5: press scale aligns to the polish default 0.97.
  ("skills/make-interfaces-feel-better/SKILL.md",
   """- Press: `scale(0.96)` for tactile buttons, with a way to disable it when the
  movement distracts.""",
   """- Press: `scale(0.97)` for tactile buttons (the polish default — animate.md's 0.95–0.98 range, default 0.97), with a way to disable it when the
  movement distracts."""),
  # W2-C2 + W2-C3 + W2-C6: pro-max cites Taste step 4a for the item list;
  # token rules and the one-accent rule name their canonical homes.
  ("skills/ui-ux-pro-max/SKILL.md",
   """**Define the design system before implementing UI (dashboard/app surfaces):** before writing any UI code, record the system in `design-system/<project-slug>/MASTER.md` (Step 2b) — visual identity; typography + type scale; color palette + semantic tokens (no raw hex in components); spacing/layout system; component hierarchy; navigation/IA; responsive behavior; motion/microinteractions; accessibility; and loading / empty / success / error states for every data surface. Take the values from the `--design-system` output and `references/quick-reference.md` — this step fixes the decisions, it does not re-derive them.""",
   """**Define the design system before implementing UI (dashboard/app surfaces):** before writing any UI code, record the system in `design-system/<project-slug>/MASTER.md` (Step 2b) — the same 10 items `design-taste-frontend` step 4a defines (that step is the canonical item list). Take the values from the `--design-system` output and `references/quick-reference.md` — this step fixes the decisions, it does not re-derive them. Token rules: no raw hex in components (quick-reference `color-semantic`, `spacing-scale` govern on app surfaces; gates.md 48/24a on landing). One accent, one button pair, one card style: gates.md F4/F15 governs on landing pages, the Impeccable craft floor on app surfaces."""),
  # W2-G8: the feel/timing decision is recorded in the design-system brief.
  ("skills/ui-ux-pro-max/SKILL.md",
   """Motion feel and timing decisions belong to `make-interfaces-feel-better` (see `rules/hackathon-mode.mdc` §5): decide feel/timing there first, then use `--motion` only to set the intensity tier of the implementation.""",
   """Motion feel and timing decisions belong to `make-interfaces-feel-better` (see `rules/hackathon-mode.mdc` §5): decide feel/timing there first and record the decision as one line in the design-system brief (MASTER.md) before setting `--motion`, then use `--motion` only to set the intensity tier of the implementation."""),
  # W4-G14: the Eval Harness row points at a skill that does not exist.
  ("skills/santa-method/SKILL.md",
   """| Eval Harness | Santa Method results feed eval metrics. Track pass@k across Santa runs to measure generator quality over time. |
""",
   """"""),
]
for rel, old, new in subs:
    p = os.path.join(base, rel)
    text = open(p, encoding="utf-8").read()
    assert text.count(old) == 1, f"{rel}: pattern not found exactly once: {old[:60]!r}"
    open(p, "w", encoding="utf-8").write(text.replace(old, new))
print("weave1: upstream skill patches applied")

# W3 trigger gaps: 22 new keys for flow-invoked skills, 3 mis-pointed
# phrases moved to their owner skill. JSON round-trip verified identical
# with indent=2 + ensure_ascii=False (the em dash in "notes" stays literal).
tp = os.path.join(base, "manifests/context-packs/skill-triggers@1.json")
data = json.load(open(tp, encoding="utf-8"))
tr = data["triggers"]
new_keys = {
  "skill:api-integration": ["call this api", "wire up the api", "rest client setup"],
  "skill:app-scaffold": ["scaffold the app", "set up auth and database"],
  "skill:brainstorming": ["brainstorm features", "more ideas for this feature", "ideate on this feature"],
  "skill:click-path-audit": ["button does nothing", "click doesn't work", "button not working", "click does nothing"],
  "skill:council": ["should we do x or y", "go or no-go", "help us decide", "which approach should we take"],
  "skill:deploy-fast": ["deploy this", "ship it live", "put it online", "deploy to vercel", "make it live"],
  "skill:design-taste-frontend": ["design a landing page", "redesign the landing page", "landing page design", "company page design"],
  "skill:devpost-autofiller": ["devpost submission", "submit to devpost", "fill in devpost"],
  "skill:frontend-slides": ["pitch deck slides", "make slides for the pitch", "slide deck"],
  "skill:hackathon-pitch": ["pitch script", "demo script", "judge q&a", "what do we say to the judges", "pitch rehearsal"],
  "skill:hookify-rules": ["final hook configuration audit before launch", "hook rule audit", "review hook config"],
  "skill:less-flat-ui": ["add texture to the ui", "less flat ui", "depth and texture"],
  "skill:make-interfaces-feel-better": ["make it feel better", "motion design", "interaction feel"],
  "skill:mcp-dependency-review": ["end of project mcp server audit", "mcp config review", "review mcp server config"],
  "skill:mobile-ship": ["ship a testable mobile build", "package the mobile app"],
  "skill:pitch-deck-video": ["demo video", "film the demo", "pitch video", "submission video"],
  "skill:polish-pass": ["polish the ui", "fix the spacing", "make it look cleaner", "ui consistency fixes"],
  "skill:readme-writer": ["write the readme", "readme for this project"],
  "skill:systematic-debugging": ["find the root cause", "why is this broken", "debug this", "unknown bug cause"],
  "skill:track-picker": ["which track should we enter", "pick a sponsor track"],
  "skill:ui-ux-pro-max": ["design the dashboard", "redesign the app ui", "dashboard design", "app interface design"],
  "skill:verification-before-completion": ["check my work before i finish", "verify everything works"],
}
for k, v in new_keys.items():
    assert k not in tr, f"trigger key already exists: {k}"
    tr[k] = v
# Mis-pointed phrases: move them to their owner skill.
assert "axe accessibility audit" in tr["skill:browser-qa"]
tr["skill:browser-qa"].remove("axe accessibility audit")
tr["skill:frontend-a11y"].append("axe accessibility audit")
assert "end of project mcp server audit" in tr["skill:security-scan"]
tr["skill:security-scan"].remove("end of project mcp server audit")
assert "final hook configuration audit before launch" in tr["skill:security-scan"]
tr["skill:security-scan"].remove("final hook configuration audit before launch")
# Rebuild in alphabetical key order (the file's existing order).
data["triggers"] = {k: tr[k] for k in sorted(tr)}
data["coverage"]["withTriggers"] = len(data["triggers"])
assert data["coverage"]["withTriggers"] == 58, data["coverage"]
open(tp, "w", encoding="utf-8").write(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
print("weave1: skill-triggers updated (36 -> 58 keys; 3 phrases re-pointed)")
PYEOF

'''
btext = btext.replace(anchor, block + anchor, 1)
with open(buildsh, "w", encoding="utf-8") as f:
    f.write(btext)
print("  applied weave1 build.sh patch block (LAST, before STEP 5)")

print("weave1: all staged edits + build.sh block applied")
