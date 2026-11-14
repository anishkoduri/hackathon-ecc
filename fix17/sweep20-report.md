# Sweep #20 — plugin fix program #17 (hackathon-ecc) — RE-SWEEP, CHECK ONLY

- **Date:** Wed 2026-11-11 (evening CT)
- **Scope:** built tree `~/workspace/hackathon-plugin/hackathon-ecc/` (excluding `node_modules/`) + staged sources for fix17 (`fix17/fix17.py`, `fix17/SPEC-DRAFT.md`) + `~/workspace/hackathon-plugin/build.sh`
- **Context:** sweep #19 was CLEAN (0 blocking, 0 minor) on the pre-fix-up tree. The fix-up changed exactly one word in the built tree (`motion-patterns/SKILL.md`: `useScrollReveal` -> `useScrollRevealSafe`) and one line in `build.sh`. Every number below was re-derived from scratch; sweep #19 was used only as a comparison baseline, not trusted.
- **No edits made.** No plugin file touched, `build.sh` not run, Campus Eats artifact not touched, no commit/bundle/GitHub.
- **build.sh identity confirmed:** 23,276 lines, md5 `1a999d763e6ec1fb16985d346b106df0` (matches the task's stated hash; differs from sweep #19's `0775d6f33c5eeb4cf509fdee1cd319d7` by the single fix-up line, as expected).
- **Sanity re-runs (read-only):** `fix17/verify17.py` → **59/59 checks pass**; `fix15/verify15.py` → **43/43 checks pass**.

## Verdict: CLEAN

- **Blocking: 0**
- **Minor: 0**
- No live banned term, no wrong pin, no E1 permission wording, no band leak, no wording drift, no inventory drift, fix-up pointer correct.

---

## 1. Banned terms in the built tree — 0 hits

Pattern (case-insensitive): `claude|codex|anthropic|opus|sonnet|haiku|composer-2.5`, run over the whole built tree excluding `node_modules/`.

| Term | Hits in built tree |
|---|---:|
| claude | 0 |
| codex | 0 |
| anthropic | 0 |
| opus | 0 |
| sonnet | 0 |
| haiku | 0 |
| composer-2.5 | 0 |
| **Total** | **0** |

Hit table: empty — there are no hits to list, so no live-vs-exception classification is needed for the built tree. (All 798 build.sh exception lines are classified under check 4 below; none of them ship.)

## 2. Model pins — all slug-only, no wrong pins, counts unchanged

| Check | Result |
|---|---:|
| `grok-4.7-high` occurrences (slug form) | 52 (50 + 2 sentence-final `grok-4.7-high.`) — identical to sweep #19 |
| `cursor-grok-4.6-high-fast` occurrences | 100 (98 + 2 sentence-final `cursor-grok-4.6-high-fast.`) — identical to sweep #19 |
| Bare `grok-4.6-high-fast` (no `cursor-` prefix, `grep -P '(?<!cursor-)grok-4\.6-high-fast'`) | **0** |
| Bracket syntax (`grok-4.7[` / `grok-4.6[`) | **0** |
| Version-suffix residue (`Grok 4.7 High [0-9]`, `grok-4.7-high-[0-9]`, etc.) | **0** |
| Any `effort=` key (bare or `reasoning_effort=`) | **0** |
| `composer-2.5` pin | **0** |
| Any other grok version token (`grep -rhoE 'grok-[0-9][a-z0-9.-]*'`) | only the two sanctioned slugs above |
| Non-Grok model pins (`model: gpt|gemini|claude|sonnet|opus|haiku`) | **0** |

Notes:
- Display names (not pins): `Grok 4.7 High` ×19, `Grok 4.6 High Fast` ×19, all in prose/picker instructions, no version suffix — unchanged from sweep #19.
- **Correction to a sweep #19 note (not a finding):** sweep #19 said "`reasoning_effort` appears exactly once as prose, `rules/common-performance.mdc:30`". The true count is **2**: `rules/common-performance.mdc:30` ("Grok takes per-vendor `reasoning_effort`, which Cursor does not expose in a pin") and `skills/orchestrate/SKILL.md:160` (same sentence, inside the fallback-pin prose). The orchestrate mention is not in `fix17/fix17.py`, `fix17/SPEC-DRAFT.md`, or `build.sh` (grep count 0 in all three) — it arrives from the staged orchestrate source and predates fix17 and the fix-up, so sweep #19 simply undercounted it. Both occurrences are prose mentions in backticks; there is still no `=` key anywhere, so there is no bare `effort=` key to flag.

## 3. Fix17 residues — 0 leaks

| Check | Result |
|---|---:|
| "may invent" permission wording (case-insensitive, incl. "MAY invent", "Invention is allowed") | **0** |
| "30–34" / "30-34" band | **0** (both en-dash and hyphen forms) |
| "SPEC draft" / "SPEC-DRAFT" reference | **0** |
| "v4 motion set" phrase used bare | **0** |

Investigated non-findings (not counted as findings):
- `skills/make-interfaces-feel-better/SKILL.md:108` — "**Default motion set (fix #17, v4-level).** Every page carries the default motion set — scroll entrances with a 1500ms fail-safe (M1/M2…), hover micro-interactions… (M3), life in existing pieces (M4), and at least one small interactive bit per page… (M5)…" — the only `v4-level` hit in the tree (1 occurrence). Same as sweep #19: the phrase "v4 motion set" does not occur; the wording cites **fix #17** as its source and immediately defines the set as M1–M6. Not a bare citation to a nonexistent source. Not a finding.
- `skills/polish-pass/reference/polish.md:35` — "…a product idea or a new direction that polish isn't allowed to invent." Same as sweep #19: a **prohibition on polish-pass**, not a "may invent" permission for the design-lead. Not a residue.

## 4. build.sh banned-term exception inventory — re-derived, delta 0

Total banned-term lines in `build.sh`: **798** — identical to fix16's inventory and to sweep #19.

| Class | Count | Meaning | Ships a banned term? |
|---|---:|---|---:|
| (a) OLD-side match pattern | 389 | Upstream text / regex the build patches *away from* | No |
| (b) Comment / build log | 52 | Bash comments + Python comments + `print` log strings | No |
| (c1) NEW-side patch text | 355 | Replacement text written into the tree mid-build by the audit-fix heredocs; rewritten/removed by fix16 (final tree grep = 0) | No |
| (c2) Heredoc file write | 0 | No banned-term hit inside any `cat >` / `cat >>` file-write heredoc | — |
| (c3) Build-time source path | 2 | `:265` `cp -r "$UIPRO_DIR/.claude/skills/ui-ux-pro-max" …`, `:298` `cp -r "$SKILL_SRC/flecto-shade/.claude/skills/hackathon-pitch" …` (verified still at those lines) | No — upstream-layout paths, not shipped text |
| **Total** | **798** | | **0 live pins; 0 shipped banned terms** |

**Delta vs fix16 (798 = 389/52/355/0/2): 0 in every class. Delta vs sweep #19: 0. No new exception class.**

Method (independent re-derivation, not a copy of the old numbers):
1. Grepped current `build.sh` and `build.sh.before-fix17` with the same 7-term case-insensitive pattern: both yield **798** hit lines.
2. Hit **line-number sets** of current vs before-fix17: **IDENTICAL** (set diff empty both ways). Hit **content** (line numbers stripped, sorted): **IDENTICAL**.
3. Parsed the sweep #18 full inventory table (`fix16/sweep18-report.md`, "Full build.sh inventory table", 798 rows, 798 unique line numbers): class counts re-derived from the table itself are **a=389, b=52, c1=355, c3=2** — exactly the sweep #19 numbers.
4. Current `build.sh` hit line set vs the table's line set: **identical** (798 = 798, empty diff both ways).
5. Text check: every one of the 798 table rows matches the current `build.sh` line at that number after backslash-escape normalization (`\|` → `|` in the table) — **0 mismatches** (45 apparent mismatches under a naive prefix check are all that escaping artifact, verified and discarded).
6. Therefore the class assignments carry over exactly; no re-classification drift is possible on an identical line set.

Per-term line counts (a line can carry >1 term) — identical to sweep #19's re-derived numbers: `claude` 701 lines / 930 occurrences, `codex` 103/126, `anthropic` 5/8, `opus` 22/26, `sonnet` 23/24, `haiku` 13/13, `composer-2.5` 0/0.

Fix17 block check: lines 23212–23264 (`# --- fix17: back-port ALL Campus Eats render feedback …`) contain **0 banned-term hits** and **0 grok/model pins**. The fix17 block added no live pins and no new exception class — and the one-line fix-up inside it (the `useScrollRevealSafe` pointer, see check 5) contains no banned term, so the inventory could not have moved.

## 5. Fix-up pointer — confirmed, no stale pointer

- `skills/motion-patterns/SKILL.md:271` reads: "…See `motion-advanced` `useScrollRevealSafe` for the shared implementation." — the fix-up word is in place. ✅
- `build.sh:23235` (the fix17 patch text that writes that line) also reads `useScrollRevealSafe`. ✅
- Remaining bare `useScrollReveal` occurrences in the built tree: **6, all in `skills/motion-advanced/SKILL.md`** — `:22` and `:34` (prose mentions of the hook in the skill's intro/lists), `:315` (heading `### useScrollReveal hook`), `:323` (`export function useScrollReveal() {` — the hook's own definition), `:332` (usage example `const { ref, style } = useScrollReveal()`), `:340` (`const { ref, style } = useScrollReveal()` inside the `useScrollRevealSafe` wrapper). These are the **upstream hook definition and its own examples**, not fix17 pointers: the hook definition appears nowhere in `build.sh` (it arrives via the upstream skill copy), `build.sh.before-fix17` contains zero `useScrollReveal` lines, and fix17 only added the `Safe` wrapper (`build.sh:23244`), which deliberately delegates to the underlying hook at `:340`. No stale fix17 pointer remains. **Not a finding.**

## 5b. Fix17 addition exactness — spot re-check (parity)

E1 paragraph extracted from all four placements and compared: identical in all four (`skills/design-taste-frontend/SKILL.md`, `skills/orchestrate/SKILL.md`, `skills/orch-build-mvp/SKILL.md`, `skills/ui-ux-pro-max/SKILL.md` — 1722 chars, md5 `9007d40b9f79` under this sweep's extraction, which starts at the bold lead "Push boundaries" without the preceding bullet marker; sweep #19's 1724-char / `e9d210257261` value differs only by that extraction boundary — cross-placement parity is what matters, and it holds). No wording drift.

## Summary

- Banned terms in built tree: **0**
- Wrong pins / bracket syntax / `effort=` keys / version-suffix residue: **0**
- Pin counts unchanged by the fix-up: `grok-4.7-high` ×52, `cursor-grok-4.6-high-fast` ×100, bare `grok-4.6-high-fast` ×0
- Fix17 residues (E1 permission wording, 30–34 band, SPEC-draft reference, bare "v4 motion set"): **0**
- build.sh exception inventory: **798 = 389 OLD-side + 52 comment/log + 355 NEW-side transient + 0 heredoc + 2 build-time paths; delta vs fix16 and vs sweep #19 = 0; fix17 block added 0 hits, 0 pins, no new class**
- Fix-up pointer: `motion-patterns:271` reads `useScrollRevealSafe`; the 6 remaining bare `useScrollReveal` hits are the upstream hook's own definition/examples, wrapped by design
- `verify17.py` re-run: **59/59 pass**; `verify15.py` re-run: **43/43 pass**
- One record correction (not a defect): `reasoning_effort` prose mentions are 2, not 1 as sweep #19 stated — the second is `skills/orchestrate/SKILL.md:160`, from staged source predating fix17; still no `effort=` key

**Verdict: CLEAN — 0 blocking, 0 minor.**
