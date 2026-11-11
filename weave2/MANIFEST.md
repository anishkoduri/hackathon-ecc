# Weave fix program #2 — MANIFEST

Dry-run #12 was NOT CLEAN (1 blocking, 2 minor) on the weave1 tree; Audit #40
was ZERO ERRORS. All three dry-run findings were verified against the built
files before fixing. Program: `weave2/weave2.py` (run once — asserts
exactly-one-match per substitution; do NOT re-run). Build logs:
`weave2/build1.log`, `weave2/build2.log`.

## B1 (blocking) — deferred-six invocation vs hackathon-mode §3/§7

The dry-run worker was right: weave1's O9b / orch-build-mvp step-9 invocation
("run the six deferred checks … before the final report") contradicted
hackathon-mode §3 ("the deferred skills never fire — not even if another
skill, rule, or reference file invokes them") and §7, with §4 giving the
deferral precedence over any rule that would run a deferred audit mid-build.
Worker 4's G7 proposal had not accounted for that sentence.

Fix (the worker's proposed carve-out, implemented as a clarification of WHEN
the deferred set fires — NOT an expansion of the §7 auto-approval scope: no
gate removed, no question added):
- `new-rules/hackathon-mode.mdc` §3: "The one permitted invocation is the
  named end-of-project run immediately before the first build's final report
  (after deploy, demo, commit, and README): that run IS the very end of the
  project — it runs once, it never gates a feature, and it never fires
  mid-build or during a one-prompt removal."
- `new-rules/hackathon-mode.mdc` §7: matching exception sentence.
- Both flows cite the carve-out as the invocation's authority (orchestrate
  O9b; orch-build-mvp step 9 via the weave2 build.sh block).
- The removal flow never invokes the six — the §3 ban during removals stands
  unmodified. The §3 wording "run ONLY at the very end of the project" and
  §6 ("verification-loop … runs only at the very end") already contemplated
  an end-of-project run; the carve-out makes "the very end" precise.

## M1 (minor) — ledger 20-line cap vs weave1 loads

Verified: orchestrate:8/:111 cap the ledger at ≤20 lines (Decided · Rejected ·
Risks · Files touched · Remaining); weave1 added task_list (~7 lines) +
Verify lines (~6) + polish 10-list (10) + deploy URL + council verdict +
KEY-RECEIPT + expansion section — over the cap with no overflow rule except
the expansion section's.

Fix (appendix pattern, same shape as the expansion overflow):
- orchestrate process rule: "Bulky loads overflow to
  `docs/run-ledger-appendix.md` (one line per item) with a one-line pointer
  in the ledger — the 20-line cap applies to the ledger file itself."
- Verify outcomes → appendix + pointer (orchestrate step 5).
- Polish 10-list → appendix + pointer (orchestrate step 5b).
- Approved task_list → appendix + pointer (orch-pipeline Gate 1, via the
  weave2 build.sh block).
- One-line loads stay in the ledger (deploy URL, council verdict,
  KEY-RECEIPT, expansion pointer).

## M2 (minor) — theme.mjs 'entry' + gates.md citation

Verified: theme.mjs:93's missing-field list demanded an `'entry'` field no
log entry can carry — `'entry'` is the CLI flag name (`--entry`, theme.mjs:16
VALUED set, :84 `flag('entry', '')`), not a log-entry field. Upstream
Hallmark bug; the warning could never clear. Fix: removed `'entry'` from the
missing list in the staged script (the two remaining `'entry'` hits are the
legitimate CLI-flag uses). Also corrected the Taste:240 citation:
gates.md:187 → :189 (the repetition rule "**8 and 32, repetition.**" sits at
:189; :187 is the 6b hero-shape note). Correction to the weave1 manifest's
claim that the log entry "carries every field theme.mjs reads": true for
every field except the unfillable `'entry'`, now removed from the list.

## Verification (built plugin, after rebuild)
- Build 1 exit 0; build 2 exit 0; md5 manifest identical across both builds
  (`258dd1bb197198f17a9511f9828f57a4`) — diff = 0. (Note: a service restart
  interrupted an earlier duplicate build2 invocation and wiped /tmp; the
  partial tree hash differed, build.sh was verified intact, and two fresh
  rebuilds restored the tree — the hash matches the pre-restart weave2
  build1, confirming full reproducibility. Build logs now live in
  `weave2/` instead of /tmp.)
- Counts unchanged: 169 skills / 72 agents / 123 rules / 96 commands /
  15 hooks, 57M.
- All 10 weave2 edits grepped in the BUILT tree: §3/§7 carve-out present
  (3× "the very end of the project" incl. the pre-existing §3 sentence);
  appendix pointers 3× orchestrate + 1× orch-pipeline; gates.md:189 1×,
  gates.md:187 0×; theme.mjs:93 missing list has no 'entry'; §3 carve-out
  cited 1× in each flow file.

## Next step
Audit #41 + dry-run #13 on this tree. If both are clean, the bundle step
follows (fresh git bundle — re-stage repo staging first; the old bundle is
stale many times over). Do NOT bundle before both read clear.
