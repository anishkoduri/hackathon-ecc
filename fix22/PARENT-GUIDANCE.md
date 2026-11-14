# Fix #22 — Parent guidance for the coordinator

## Task
Weave 7 @charles.unemployed reels (142 items: 20 UX & animation principles, 20 beautiful-AI-animation techniques, 20 AI-design slop indicators, 20 unslop fixes, 20 AI design trends, 22 less-flat backgrounds, 20 design terms) into the plugin's design process so all of them are considered when a design is made. Full inventory, placement map, adjudications, dedupe table, and verification criteria are in `fix22/SPEC.md` — the SPEC is the authority for WHAT goes WHERE. This file is the authority for HOW the work is done.

## Starting state (verified by parent, Nov 12)
- Plugin is post-fix-#21, audit-clean: Audit #66 ZERO, dry-run #35 9/9, sweep #29 CLEAN.
- `build.sh` = 23,647 lines, md5 `8dfacb47a2a6698d47e4b4a5f8d9126c`. Counts: 166 skills / 72 agents / 123 rules / 87 commands / 15 hooks; 64 trigger keys.
- Next audit number is #67. Verify scripts live in their fix dirs (e.g. `fix21/verify21.py`); follow that pattern for `fix22/verify22.py`.
- `build.sh` embeds skill contents (e.g. `('skills/motion-foundations/SKILL.md', ...)` ~line 23174) and is the source of truth. Staged sources also exist for some skills (`round2-skills/polish-pass`, `new-skills/design-taste-frontend`). Determine the edit point per skill; never edit the built tree `hackathon-ecc/` directly; rebuild with `bash build.sh` and verify the built tree matches.

## Standing rules (do not regress)
- **Audit loop until fully clear:** audit, dry-run, and sweep must ALL return zero (0 blocking, 0 minor) before the fix closes. Then the parent spot-checks (manifest exists, build.sh md5/lines match, banned terms 0, all verifiers pass) before anything is reported to Anish.
- **Banned terms 0** in the built tree (case-insensitive, excl. node_modules): claude, codex, anthropic, opus, sonnet, haiku, composer-2.5. The word "AI" is NOT banned. Never write "Claude Code" anywhere, including in comments.
- **Grok only:** all model pins stay Grok (`grok-4.7-high` orchestrator/design-lead, `cursor-grok-4.6-high-fast` underlings). Never use the bare form `grok-4.6-high-fast`.
- **Screen-verdicts rule:** browser-qa is the SOLE executor of pass/fail verdicts on rendered screens. The slop checklist is STATIC checks producing candidate evidence, never verdicts.
- **D19:** every new rule/decision carries its six-dimension reason (Motion / Theme / Texture / Visuals / Techniques / Colors), each a reason or explicit `none — <reason>`. Layout-only reasoning fails.
- **Theme-match precondition:** every element, treatment, trend, and slop-flag clearance must match the dealt theme; record it in `docs/design-tokens.md` with the element.
- **Anti-derivative:** no design based on a searched reference. These reels are vocabulary and checks, not a reference to copy. Do not import anything wholesale — the SPEC's adjudications (§4) and dedupe (§5) govern what is kept, merged, or dropped.
- **"More, not bolder":** the user's correction stands. Trends are a menu, never defaults.
- **Weaving is binding:** every decision routes through a named skill; creativity runs through the skills; needed work never stalls (recorded-gap fallback). Prefer pointers over duplication (§10 weaving).
- **Verify your own claims:** every audit round's first-pass claims have contained at least one error. The coordinator verifies each subagent's claims itself (re-run the greps, read the files) before reporting the fix closed. Repair compliance is repair-reported only until verified.

## Process
1. Coordinator reads SPEC.md fully, then fans out to implementation subagents per group (A–G), keeping the 142-item disposition table as the single source of truth for coverage.
2. Coverage: re-verify EVERY item's baseline with word-boundary greps (the parent's greps were case-insensitive substring matches — "tween" matched "between", "tracking" matched cost-tracking, "Monet" matched "Monetization"). Record already-covered / partial / new per item.
3. Implement per the placement map (§3). If a SPEC adjudication proves unworkable, do NOT silently change it: propose the alternative in the manifest and flag it for the parent.
4. Write `fix22/verify22.py` (SPEC §6.2), run it to 100%. Run all previous verifiers (verify15/17/18/19/20/21) — they must still pass.
5. Audit (#67) → dry-run (with the SPEC §6.3 fixtures) → sweep → fix → repeat until all three are zero/clean. Rebuild after every change (`bash build.sh`, exit 0) and confirm the built tree matches.
6. Write `fix22/MANIFEST.md` (SPEC §6.8) with the disposition table, counts before/after, and all verifier/audit/dry-run/sweep results.
7. Report back to the parent with: manifest path, build.sh md5 + line count, banned-term count, verifier results, audit/dry-run/sweep results, and any SPEC deviations proposed. Do NOT bundle, commit, or push anything. Do NOT message Anish directly.

## Hazards
- NEVER re-run `fix11/fix11-stage.py` — it copies critique.md verbatim and would clobber the fix #12 edits.
- `/tmp` is a 512 MB tmpfs (has hit 100% before). Keep intermediates in `~/workspace/hackathon-plugin/fix22/` or the fix scratch dirs, never /tmp for anything large.
- Do NOT touch the durable Audit #4 backup (`hackathon-plugin-fixed-backup-audit4/`).
- Do NOT touch the font rules (fix #19/#20/#21), the screen-verdicts rule, the model pins, or the marketplace manifest.
- The live smoke test in Anish's Cursor is still pending and is a separate gate — this fix does not depend on it and must not block on it.
