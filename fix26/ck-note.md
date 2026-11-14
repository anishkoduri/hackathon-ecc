# §8 — ck wire KEEP (fix #26)

## Decision: KEEP

Parent decision at the fix #25 close: KEEP the ck wire at its true cost
(~1k tokens/session, not ~100). No code change to the wire — the
`hooks/session-start.js` spawn of `skills/ck/hooks/session-start.mjs`
(fix #25 §1) is untouched. Only the stale cost claims are corrected,
as build-time patches in `fix26/fix26.py`. This closes the fix #25
MANIFEST §5 open item ("keep at ~1k tokens/session, trim, or record
dormant?") as KEEP.

## Measurement (the ground truth)

- Live measurement (fix #25, re-stated in the fix #26 task): **7,382 chars
  / 890 words merged with an empty ck store → ~1k tokens/session.**
- Built-tree check this fix (`wc` on the run-5 built tree):
  `skills/ck/SKILL.md` is **169 lines / 825 words / 6,377 chars**.
- Note on the fix #25 figures: the fix25 manifest says "167 lines / 785
  words / 6,100 chars". That was measured before fix25.py's own SKILL.md
  patch, which appended the "already wired" note (+2 lines, ~40 words).
  169 / 825 / 6,377 is the current built-tree figure; `fix25.py` was NOT
  edited (out of scope — its comment is a fix-#25-time record).
- The empty-store merged output (7,382 chars / 890 words) is the SKILL.md
  plus separators and the JSON wrapper: the hook injects the full SKILL.md
  on EVERY session start, even with no registered projects.

## Adjudication — every cost claim, against the measurement

| # | Location | Claim | Verdict | Reason |
|---|---|---|---|---|
| 1 | `skills/ck/hooks/session-start.mjs:6` | "Injects ~100 tokens (not ~2,500 like v1)" | CORRECTED | As a statement of the hook's total injection it is wrong by ~10x: the measured merged output is ~1k tokens. The ~100-token figure is true only of the compact summary block alone, which the header does not scope it to. The v1 contrast ("not ~2,500") is kept — it is still true. |
| 2 | `skills/ck/hooks/session-start.mjs:7` | "SKILL.md is injected separately (still small at ~50 lines)" | CORRECTED | SKILL.md is 169 lines in the built tree, not ~50 (3.4x off). "Separately" is also misleading as comfort: the full file is injected on every session start. |
| 3 | `skills/ck/hooks/session-start.mjs:90` | "Load skill (always inject — now only ~50 lines)" | CORRECTED | Same error as #2, at the load site. |
| 4 | `skills/ck/hooks/session-start.mjs:129` | "Compact summary block (~100 tokens)" | LEFT UNCHANGED | The block is 4 short lines built from `summaryLines` (name + date + session count, goal, first line of left-off, first 2 next steps). Realistic cases measure ~30 words (~40 tokens) typical and ~51 words (~70 tokens) with long goal/next lines, so ~100 tokens is a fair ceiling for the block alone. The empty-store measurement never fires the block, so nothing contradicts it. The error was presenting ~100 as the session total (claims #1 and #5), not as the block size. |
| 5 | `skills/ck/SKILL.md:159` | "The hook injects ~100 tokens per session (compact 5-line summary)" | CORRECTED | States the session total as ~100 tokens. The total is the full SKILL.md plus the summary — ~1k tokens/session. |

No other cost claims exist in the ck tree: `grep -rn "100 tokens\|50
lines\|tokens per session"` over `skills/ck/` returns exactly claims
#1–#5 above.

## Patches (in `fix26/fix26.py`, §8 — build-time, built tree only)

ck is upstream (no staged source under `new-skills/` / `round2-skills/` /
`rewritten-skills/`; build.sh's own `audit_patch` already touches its
SKILL.md), so the corrections live here as build-time patches in the
fix25.py pattern. The built tree was NOT edited by hand.

1. `skills/ck/hooks/session-start.mjs:6–7` — old:
   ` * Injects ~100 tokens (not ~2,500 like v1).` /
   ` * SKILL.md is injected separately (still small at ~50 lines).` →
   new: ` * Injects ~1k tokens per session (not ~2,500 like v1): the full SKILL.md` /
   ` * (~170 lines) plus the compact summary below.`
2. `skills/ck/hooks/session-start.mjs:90` — old:
   `  // Load skill (always inject — now only ~50 lines)` →
   new: `  // Load skill (always inject the full SKILL.md, ~170 lines, ~1k tokens/session)`
3. `skills/ck/SKILL.md:159` — old:
   `The hook injects ~100 tokens per session (compact 5-line summary). It also detects` →
   new: `The hook injects ~1k tokens per session (the full SKILL.md plus the compact 5-line summary). It also detects`

"~170 lines" is used (not "169") so the wording stays true if a later
fix adds a line or two to SKILL.md; the exact figure at this fix is 169.
Line counts are unchanged by every patch (2 lines → 2 lines, 1 → 1, 1 → 1).

## Verification (scratch run, built tree untouched)

`fix26.py` was run against scratch copies of the two ck files
(`fix26/scratch/`, since removed): first run `fix26: 3 change(s)`,
exit 0, "fix26: OK", with the corrected lines landing at :6, :7, :90 and
SKILL.md:159 and :129 untouched; a second run failed loudly with 3
anchor errors, exit 1, proving the count==1 enforcement. The scratch
copies and the scratch run log were deleted afterwards. The built tree
still carries the stale claims until the coordinator rebuilds — that is
expected; the patches apply at build time.
