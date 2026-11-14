# Fix #22 — Parent addendum (Nov 12, ~18:52 CST): weaving quality + /demo gates

Source: Anish, via parent. This is a QUALITY BAR on the weaving and on /demo, not new scope. It is part of the close criteria for fix #22.

## 1. Weaving quality — "Make sure everything is woven smoothly into the design skill"

The fix #22 additions (§1–§16) must be woven SMOOTHLY into the design skills (the design package: ui-ux-pro-max, Taste/design-taste-frontend, motion-foundations / motion-patterns / motion-advanced, polish-pass, less-flat-ui, orchestrate's design-package step), not just appended. That means:
- the placement map is honored;
- pointers are bidirectional where the SPEC requires them (a skill that references a token/rule must resolve, and the owning skill must point back where the SPEC says so);
- no orphaned anchors (the sweep #30 finding-1 class — every anchor token resolves exactly once);
- no duplicated rules (dedupe tables honored — B4, A14/G8, D5, D8, D15, G4, G13, C13, and the §16 Vercel dedupe);
- the design package reads coherently end-to-end (a build following the package encounters each addition at the step where the SPEC places it, with its D19 reason and its §10 directive form intact).

The confirmation sweep (#30b) MUST check weaving quality explicitly — a weaving-coherence pass: for every §1–§16 item, verify it is reachable from the design-package flow at its SPEC'd placement, its pointers resolve, and it is not duplicated elsewhere. Any item that is only appended (not reachable from the flow) FAILS the sweep and gets re-woven. Record the weaving-coherence result in the sweep report and the manifest.

## 2. /demo — §12 + §15 brand-mark step

"The stuff I wanted in the /demo skill" is §12 (Bang Motion port into pitch-deck-video) plus the §15 liquid-logo brand-mark step insofar as it touches /demo's branding beats (the animated brand mark is produced once, outside the video pipeline — §15 already says this; do not let the Bang port turn it into a runtime import). Verify the §12 port is woven into pitch-deck-video's STAGED source (new-skills/pitch-deck-video/, never the built tree) per the SPEC: anti-slide rules as structural checks, one-world/camera/persistent-subject architecture for Remotion compositions, style-direction + opener-concept menus (look from the brand/theme deal, never a template), kinetic typography as §10 directives, explainer styles informing How beats. Existing /demo rules untouched (F1–F6, voice rules, $10 cap, local-only filming, under 2:10 / max 2:30).

## 3. /demo callability + non-automatic — explicit, blocking checks

Verify ALL of the following and record each in the Audit #68 report and the manifest:
- (a) CALLABLE: the /demo command exists, is wired, and invokes pitch-deck-video correctly (command file present in the built tree, correct frontmatter/name, reachable from the command list). A dry-run fixture must exercise invoking /demo on a sample app and show it reaches the filming pipeline (shots.json → Remotion → film → narrate) — or, if a full live film is not possible in the audit environment, the fixture must show the invocation path resolves end-to-end to the filming entry point with no missing step, and record exactly what was and was not executed live.
- (b) NOT AUTOMATIC: /demo NEVER runs on its own. Grep-verify: no orchestrate step, no hook, no post-build trigger, no finish-report step, and no other command invokes /demo or pitch-deck-video automatically. It runs ONLY when the user invokes /demo explicitly. Any auto-invocation found is a BLOCKING audit finding — remove it, re-run the sweep and the audit.
- (c) WORKS AS INTENDED: the §12 port did not change /demo's contract — it still films the REAL app locally (the redirect stands), still enforces F1 feature coverage, F2 stack labels, F3 Edge at position 3, F4 theme pull + gorgeousness checks, F5 blocking A/V table + 10s mix listen, F6 measured runtime under 2:10 / absolute max 2:30, voice rules, $10 budget cap, local-only filming. A dry-run fixture must assert each of these still holds with the Bang rules woven in.
- If any of (a)–(c) cannot be verified in the audit environment, say so explicitly in the report (what was checked, what was not, and why) — do not claim /demo works on the basis of the wiring alone.

## 4. Close criteria (amended)

Audit #68 ZERO + dry-run #37 PASS + sweep CLEAN + verify22 100% AND verify15/17/18/19/20/21 still pass + banned terms 0 + build clean + MANIFEST.md written — PLUS the new explicit gates: weaving-coherence CLEAN and /demo (a) callable, (b) never automatic, (c) contract intact.

## 5. Preliminary /demo findings (coordinator, Nov 12 ~18:53 — read-only greps; Audit #68 must confirm with full context reads)

- (a) CALLABLE — confirmed by wiring: `hackathon-ecc/commands/demo.md` exists, frontmatter "Generate a narrated product demo video, under 2:10, of the hackathon project. Use when the user wants a demo video, launch video, product walkthrough, or hackathon submission video." Build note: "place this file at hackathon-ecc/commands/demo.md so it is invoked as /demo. It loads the pitch-deck-video skill." Args: /demo, /demo <path>, --rebuild, --script, --render, --montage, --explainer. Films the LOCAL app only; never a deployed URL.
- §12 staged source — confirmed: all 6 BANG_*_F22 anchors present in `new-skills/pitch-deck-video/SKILL.md` (BANG_ANTISLIDE_F22 at :247).
- (b) NOT AUTOMATIC — PRELIMINARY, needs Audit #68 confirmation: `hackathon-ecc/skills/orchestrate/SKILL.md` step 5 is "Verify → polish → deploy → demo, in that order" and step 5d reads "Demo — /demo (pitch-deck-video). /demo films the LOCAL app from the project dir only" — i.e. /demo IS invoked as part of the autonomous first-build pipeline (auto-approval: after grill-me the first build runs fully autonomously; end-of-project checks run "after deploy, demo, commit, and README"). Hooks: zero "demo" hits. Other files referencing pitch-deck-video need full context reads to distinguish invocations from mentions: orch-build-mvp (skill + command), hackathon-pitch, deploy-fast, rules/hackathon-mode.mdc, orch-change-feature (the latter describes "/demo vs /demo --rebuild", likely a mention, not an invocation). Audit #68 must read each in full and apply the parent's rule (any auto-invocation = BLOCKING finding, remove it, re-run sweep + audit).
- TENSION TO RECORD (not to resolve silently): removing the orchestrate 5d demo step changes the standing first-build contract (auto-approval pipeline: deploy, demo, commit, README; the demo video is part of what a requested first build produces). If Audit #68 confirms 5d as auto-invocation and it is removed, the manifest MUST record the behavior change explicitly, and the parent spot-checks it before anything is reported to Anish.
- (c) CONTRACT — to be asserted by dry-run #37 fixtures (F1–F6, voice rules, $10 cap, local-only filming, under 2:10 / max 2:30) with the Bang rules woven in.
