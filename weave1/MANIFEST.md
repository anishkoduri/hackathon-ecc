# Weave program #1 — MANIFEST

Ordered by Anish Nov 10, ~23:05 CST: connection/weaving loop before bundling.
Coordinator session ba3f2c69. Program: `weave1/weave1.py` (run once — it asserts
exactly-one-match per substitution and inserts the build.sh block; do NOT re-run).

## What changed

- 40 staged-source edits (Part A of weave1.py) across 12 files.
- 1 build.sh patch block, placed LAST just before STEP 5 (upstream ECC files
  + skill-triggers JSON). 21 upstream substitutions + JSON rewrite.
- No new skills, agents, rules, or commands. No new gates, wait points, or
  user questions. No pin touched. No direction lenses, no live/generate mode.

## Connections added (producer → consumer → carrier)

### Core flow (worker 1)
- W1-G1 expansion list → slicing: `docs/expansion.md` else ledger expansion
  section → orchestrate step 3.
- W1-G2 first-build commit: each landed slice as `feat:` via orch-pipeline
  Phase 6 → orchestrate step 6 (Gate 2 auto-approves).
- W1-G3 Verify outcomes → ledger: one line per check → orchestrate step 5.
- W1-G4 Phase 6 overflow → `docs/expansion.md` + ledger pointer (feature-expansion).
- W1-G5/W4-G1 deploy URL + path → ledger + final-report Deployed URL bullet
  (orchestrate 5c; orch-build-mvp step 8).
- W1-G6 polish target + 10-list → ledger (orchestrate 5b).
- W1-G7 integration skill named in slice briefs (orchestrate step 3).
- W1-G8 approved `task_list` → ledger at Gate 1 (orch-pipeline).
- W1-G9 removal takes URL/path from ledger (or final report) (orch-change-feature:49).
- W1-G10 removal refreshes pitch/Devpost only where artifacts exist (orch-change-feature:49).
- W1-G11 redesign re-runs the hero review, updates `.hallmark/hero-review.md`
  (orch-change-feature landing-redesigns section).
- W1-G12 GAN spec takes the expansion list (orch-build-mvp step 4).
- W1-G13 reconcile reads `gan-harness/build-report.md` + `feedback-*.md`
  (orch-build-mvp step 5).
- W1-G14 standalone flow gains polish step 6b before commit (orch-build-mvp).
- W1-G15 first GAN UI slice writes `docs/design-tokens.md` (orch-build-mvp step 4).

### Build / deploy / demo chain (worker 4)
- W4-G2 readme-writer takes ledger URL + `<app-name>-video/out/demo.mp4` as
  inputs (orchestrate step 6; readme-writer scan).
- W4-G3 exact video path named in both demo handoffs (orchestrate final
  report; orch-build-mvp steps 8–9). Path confirmed at build.mjs:335.
- W4-G4 remaining shots re-checked vs updated scope storyboard before
  `/demo --rebuild` (orch-change-feature step 5).
- W4-G5 tts usage + decision-log + music credit → final report via the /demo
  return (pitch-deck-video; orchestrate + orch-build-mvp handoffs).
- W4-G6 adversarial findings bullet in both final reports (CONFIRMED/SUSPECTED
  + fixed-or-open).
- W4-G7 deferred six (`verification-loop`, `production-audit`, `delivery-gate`,
  `codehealth-mcp`, `santa-method`, `security-scan`) invoked by name before the
  final report in both flows; results recorded per check.
- W4-G8 council verdict (consensus, dissent, recommendation) → ledger
  (orchestrate process rule).
- W4-G9 `tdd-guide` named in every brief; evidence to
  `docs/releases/<version>/<name>.tdd.md` (orchestrate step 4).
- W4-G10 blind reviewer in the Verification stage named `code-reviewer`.
- W4-G11 orch-build-mvp step 3 names `app-scaffold`.
- W4-G12 `security-review` pre-deployment checklist gates the final deploy
  at orchestrate 5c (deploy-fast Timing rule).
- W4-G13(c1) pre-pitch checklist gets a §7 carve-out (deploy-fast). The
  "Live-demo from the production URL" line already carried the video carve-out
  — no change needed there.
- W4-G13(c2) interactive-login rule in orch-change-feature points at deploy-fast.
- W4-G13(c3) proxy.ts (route protection) vs middleware.ts (session refresh)
  cross-referenced both ways (deploy-fast + app-scaffold).
- W4-G13(c4) narration-key wording: pitch-deck-video is canonical
  (orchestrate step 0 cross-ref; demo.md already defers to the skill).
- W4-G13(c5) `supabase db push` already cites deploy-fast in both
  orch-change-feature spots — no change needed.
- W4-G14 santa-method Eval Harness row removed (no such skill); pitch-deck-video
  cost rules stated as the skill's own (no `tools/cost_tracker.py` citation).

### Design bundle (worker 2)
- W2-G1 dealt theme slug + Tokens block + palette balance → first two lines
  of `docs/design-tokens.md` (Taste step 4a).
- W2-G2 log entry carries every field theme.mjs reads (theme, axes, prompt,
  shape, hero, nav, footer, imagery, sections, fingerprint, signature);
  re-log if the build changes the shape (Taste:240).
- W2-G3 sloplint `--json` summary counts → Verify fix list (orchestrate:182).
- W2-G4 render-absent branch passes `.hallmark/hero-review.md` to browser-qa
  (orchestrate:182).
- W2-G5 Impeccable findings listed (fixed + open, rule id + file:line) in
  polish.md Step 6 "Accepted detector findings".
- W2-G6 10-list gets its template slot in polish.md Step 6.
- W2-G7 browser-qa baseline = `.polish-pass/captures/after/capture.json` + PNGs
  when polish-pass ran.
- W2-G8 feel/timing decision recorded as one line in the MASTER.md brief
  before `--motion` (ui-ux-pro-max).
- W2-G9 applied less-flat-ui treatments recorded in `docs/design-tokens.md`
  (or MASTER.md on dashboard-only).
- W2-G10 Picks block → `.hallmark/picks.md`; hero review takes it as the file
  path (Taste deal + step 6).
- W2-G12 polish.md Step 1 reads `docs/design-tokens.md` (else MASTER.md).
- W2-C1 gradient-text conflict resolved: Hallmark gate 2b's guarded single-hue
  ramp is permitted on landing pages (Taste:242 exception; vibe-code-tells
  detector exception; less-flat-ui re-tint note for the purple examples).
- W2-C2 pro-max cites Taste step 4a as the canonical 10-item list.
- W2-C3 token rules: gates.md 48/24a on landing; quick-reference
  `color-semantic` / `spacing-scale` on app surfaces.
- W2-C4 touch floor unified at 44px (make-interfaces-feel-better was 40/ideal-44).
- W2-C5 press scale unified at 0.97 (polish default; was 0.96 in
  make-interfaces-feel-better; inside polish's 0.95–0.98 range either way).
- W2-C6 one accent/button pair/card style: gates.md F4/F15 on landing,
  craft floor on app surfaces.
- W2 dead-ends: gates.md staged-scope note (11 companion docs not staged);
  redesign.md `design.md`/`design-md.md` → design-tokens.md/MASTER.md;
  redesign.md no longer prescribes `theme.mjs scaffold`; theme.mjs deal
  stdout no longer instructs scaffold; browser-qa MCP tool names marked
  harness-provided.

### Long-tail census (worker 3)
- W3-1 `ai-feature-spec` routed: new branch in feature-expansion:145 + table
  row at :190. (The only class-B gap in the 52-skill zero-reference list;
  the other 51 are legitimately on-demand — see worker 3 report.)
- W3 triggers: 22 new keys (api-integration, app-scaffold, brainstorming,
  click-path-audit, council, deploy-fast, design-taste-frontend,
  devpost-autofiller, frontend-slides, hackathon-pitch, hookify-rules,
  less-flat-ui, make-interfaces-feel-better, mcp-dependency-review, mobile-ship,
  pitch-deck-video, polish-pass, readme-writer, systematic-debugging,
  track-picker, ui-ux-pro-max, verification-before-completion). 36 → 58 keys;
  `coverage.withTriggers` updated to 58. All 58 keys resolve to real skill dirs.
- W3 pointer fixes: "axe accessibility audit" moved browser-qa → frontend-a11y;
  "end of project mcp server audit" moved security-scan → mcp-dependency-review;
  "final hook configuration audit before launch" moved security-scan →
  hookify-rules. Deliberately triggerless (unchanged): frontend-design-direction
  (excluded by hackathon-mode §7... §5/§37), product-lens /
  intent-driven-development (do not scope hackathons), orch-pipeline (internal
  engine), council-multi-model (opt-in external CLI), integration (too generic),
  stack skills (reached via rules/agents/commands).

### Dry-run #11 observation #2 (parent-verified)
- Re-dealt pick gets logged too (Taste:234): "If you re-deal, log the re-dealt
  pick too — the log must record the theme actually built, not the first pick."

## Held back (with reasons)
- W2-G11 frontend-slides ownership: orchestrate never invokes it; deck/video
  goes through pitch-deck-video /demo. Whether pitch-deck-video or
  frontend-slides owns the deck in a first build is a scope decision for the
  parent — NOT wired. (Worker 2 flagged it as a scope note, no connection
  proposed.)
- No wiring for the 51 class-A zero-reference skills (stack-specific,
  meta/ops, business) — legitimately on-demand per the reasonableness bound.
- No trigger keys for frontend-design-direction, product-lens,
  intent-driven-development, orch-pipeline, council-multi-model, integration
  (deliberately triggerless — frontend-design-direction is excluded by
  hackathon-mode.mdc:37; product-lens / intent-driven-development do not scope
  hackathons; orch-pipeline is the internal engine; council-multi-model is
  opt-in external CLI; integration is too generic to phrase).
- Dry-run #11 observation #1 recorded as INTENDED (landing redesign Gates
  apply) — not "fixed".

## Verification (built plugin, after rebuild)
- Build 1 exit 0; build 2 exit 0; md5 manifest identical across both builds
  (`94bba42d3f98b4e971b0d59a447a8bc7`) — diff = 0.
- Counts unchanged: 169 skills / 72 agents / 123 rules / 96 commands /
  15 wired hook events; size 57M.
- Every added connection grepped in the BUILT tree (all anchors present, 1×
  each unless noted; santa-method Eval Harness row = 0 hits).
- Pins spot-checked intact: impeccable@4.8.0, remotion@4.0.542 (build.mjs:335,
  qa.mjs:42), vercel@65.14.0, supabase@3.1.0, Hallmark SHA
  7e213cb6feb4ef82733bd66a0600b2e54ca0994c. GATE carve-outs intact in build.sh.

## Next step
Audit #40 + dry-run #12 on this tree. If both are clean, the bundle step
follows (fresh git bundle — re-stage repo staging first; the old bundle is
stale many times over). Do NOT bundle before both read clear.
