# Sweep #29 — fix program #21 (hackathon-ecc), built-tree re-verification

**Verdict: CLEAN — 0 blocking / 0 minor.** Every fix21 rule text is
identical, count 1, in every placement the SPEC requires (staged and
built); the fix20 typeset checkbox is gone from every live surface
(staged, built, build.sh); the fix21 block in build.sh is exactly 38
lines, placed before STEP 5, with no LAST claim; banned terms are 0 in
the built tree, the staged sources, the fix21 block, and all eight
fix21 constants; no TODO/FIXME/XXX residue; counts unchanged;
verify21 re-run by this sweep: **101/101 checks pass**. The only
broad-scope font statements still standing are the verify19/verify20
anchor texts fix #21 is forbidden to edit (F4_RULE, F4_APP, F4_SCOPE,
F4_SCOPE_APP, TYPESET_F20) — each is documented in §4 with its anchor
evidence and the adjacent new tightened rule, recorded as checked and
cleared rather than as findings.

**Scope:** built tree `~/workspace/hackathon-plugin/hackathon-ecc/`,
`node_modules/` excluded everywhere; plus `build.sh` and the staged
sources `new-skills/`, `round2-skills/`. SPEC read first:
`~/workspace/hackathon-plugin/fix21/SPEC.md`; sweep format example:
`~/workspace/hackathon-plugin/fix19/sweep23-report.md`. Every number
below was re-derived by running the greps/commands shown; nothing was
copied from the fix21 implementation report without re-running. This
sweep made no plugin change (read-only); its only write is this report.
`fix21/MANIFEST.md` does not exist yet (the task forbids writing it);
there is no dry-run report in `fix21/` yet either.

**Given state (verified):** `build.sh` md5
`8dfacb47a2a6698d47e4b4a5f8d9126c`, 23,647 lines (matches the task
brief; 23,609 pre-fix21 + 38 = 23,647); `fix21/verify21.py` re-run by
this sweep: **101/101 checks pass** (its check 11 runs verify15/17/18/
19/20 as subprocesses, exit 0 required — so all five earlier verifiers
pass as well).

---

## 1. Banned terms — 0 everywhere in scope — PASS

| Scope | Banned-term lines | How counted |
|---|---:|---|
| Built tree (`hackathon-ecc/skills agents commands rules hooks README.md`, excl. `node_modules`) | **0** | `grep -rciE 'claude\|codex\|anthropic\|opus\|sonnet\|haiku\|composer-2\.5'` — no file with a nonzero count |
| Staged sources (`new-skills/`, `round2-skills/`) | **0** | same grep — no file with a nonzero count |
| fix21 block in build.sh (lines 23600–23637) | **0** | `sed -n '23600,23637p' build.sh \| grep -niE …` — empty |
| All eight fix21 constants (fix21.py) | **0** | per-constant regex scan: F4_TIGHT, F7, STATIC21, F4_TIGHT_APP, F7_APP, TYPESET_F21, TYPESET_CHECKBOX21, POLISH_F21 — 0 hits each |

Note: `fix21/fix21.py:172–173` defines the `BANNED` list itself
(`["claude", "codex", "anthropic", "opus", "sonnet", "haiku",
"composer-2.5"]`) — the scrub list, not rule text. No fix21 addition
contains a banned term.

## 2. The fix20 typeset checkbox is GONE — PASS

Old checkbox = `fix20.TYPESET_CHECKBOX_NEW` (336 chars, md5
`c7beeef5b4d3`); distinctive phrase `the body face is used for basic
text only`:

| Surface | Old checkbox count |
|---|---:|
| Built Taste / orchestrate / polish-pass / typeset lens / ui-ux-pro-max / orch-build-mvp | **0 each** |
| Staged Taste / orchestrate / polish-pass / typeset lens | **0 each** |
| `build.sh` (whole file) | **0** |
| Tree-wide `used for basic text only` (`new-skills`, `round2-skills`, `hackathon-ecc`, excl. `node_modules`) | **0 hits** |

No reference to `TYPESET_CHECKBOX_NEW` exists outside the fix
directories (`fix20/fix20.py` constant definition, `fix21/fix21.py`
old-text import for the replacement, `fix19/verify19.py` +
`fix20/verify20.py` now asserting it gone per `fix21/fixup21.py`).
The only typeset-lens checkbox line is the new one
(`typeset.md:78`, staged and built): `- [ ] A custom typeface has a
stated reason; … the body face is used for long-length body text and
small incidental text only, … every text element has a recorded
artistic font decision (fix #21 F7).`
A tree-wide `checkbox` grep finds only HTML `<input type="checkbox">`
elements, form-pattern prose, and data files — no other rule-text
checkbox cites the fix20 checkbox as current.

## 3. Fix #21 rule-text identity and ordering — PASS

Constants imported from `fix21/fix21.py`; counts are
`text.count(constant)`; md5s are of the constant text (12-char
prefix shown).

| Rule | md5 (prefix) | Built Taste | Built Orch | Built polish | Built typeset | Built uum | Built obm | Staged Taste | Staged Orch | Staged polish | Staged typeset |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| F4_TIGHT (1070 chars) | `80a83d530b65` | 1 | 1 | — | — | — | — | 1 | 1 | — | — |
| F7 (1308 chars) | `b08fe9c55d36` | 1 | 1 | — | — | — | — | 1 | 1 | — | — |
| STATIC21 (845 chars) | `dc8ca85561a5` | 1 | 1 | — | — | — | 1 | 1 | 1 | — | — |
| F4_TIGHT_APP (320 chars) | `37396ac7233d` | — | — | — | — | 1 | 1 | — | — | — | — |
| F7_APP (571 chars) | `5b34ce3cf3fa` | — | — | — | — | 1 | 1 | — | — | — | — |
| TYPESET_F21 (659 chars) | `101cea2108be` | — | — | — | 1 | — | — | — | — | — | 1 |
| TYPESET_CHECKBOX21 (444 chars) | `ce9bb145508d` | — | — | — | 1 | — | — | — | — | — | 1 |
| POLISH_F21 (351 chars) | `130680a53e56` | — | — | 1 | — | — | — | — | — | 1 | — |

Ordering (all re-derived by this sweep, line numbers built tree
unless noted; staged Taste is 1 line earlier throughout — the
frontmatter patch hunk, §6):

- Taste: X1 `:275`, F4_TIGHT `:277`, F7 `:279` (staged `:274/:276/
  :278`); STATIC20 `:331`, STATIC21 `:333` (staged `:330/:332`).
- Orchestrate: X1 `:120`, F4_TIGHT `:122`, F7 `:124`; STATIC21 on
  the Verify 5a paragraph line `:69`, after STATIC20 and before the
  `5b. Final polish` bullet (verified by `find()` offsets, staged
  and built).
- ui-ux-pro-max: X1_APP `:112`, F4_TIGHT_APP `:114`, F7_APP `:116`.
- orch-build-mvp: X1_APP `:55`, F4_TIGHT_APP `:57`, F7_APP `:59`;
  STATIC20 `:74`, STATIC21 `:76`.
- Typeset lens: TYPESET_F20 `:57`, TYPESET_F21 `:59`, new checkbox
  `:78`.
- polish-pass: POLISH_F21 inside the harmony paragraph (line `:22`),
  after POLISH_F20 (verified by `find()` offsets, staged and built).

App mirrors are intentionally different from the full rules (MASTER.md
home instead of `docs/design-tokens.md`, plus the pointer "The full
tightened scope rule / full F7 rule lives in `design-taste-frontend`
step 4a") — recorded as specified, not as drift. Build.sh's fix21
block carries the same texts: after unescaping, F4_TIGHT_APP ×2,
F7_APP ×2, STATIC21 ×1 inside lines 23600–23637 — exactly the two
patched files plus the one static-checks sub (§5). No truncated or
half-pasted copy anywhere: every placement is a full-constant match.

## 4. Stale cross-references — PASS, with the anchor texts checked and cleared

### 4a. "Body and plain text use Tiempos" — only anchors and the new rule's own quotation

| Hit | Disposition |
|---|---|
| `hackathon-ecc/skills/design-taste-frontend/SKILL.md:263` and `new-skills/…:262` (staged) — the F4_RULE sentence | **Anchor.** verify19 full-text `in` check; SPEC §3 forbids editing. F4_TIGHT follows at `:277`/`:276` and re-reads it. |
| `hackathon-ecc/skills/orchestrate/SKILL.md:108` and `new-skills/…:108` — same F4_RULE sentence | **Anchor**, same as above. F4_TIGHT follows at `:122`. |
| F4_TIGHT itself (`:277` Taste / `:122` orchestrate, staged + built) — quotes the sentence to reinterpret it: "'Body and plain text use Tiempos' (fix #19 F4) reads, after this fix, as long-length body text and small incidental text only." | **The new rule.** Not a stale cite; it is the tightening. |
| `hackathon-ecc/skills/ui-ux-pro-max/SKILL.md:100` — F4_APP: "Body and plain text use Tiempos, or the recorded stand-in …" | **Anchor.** verify19 asserts F4_APP present in ui-ux-pro-max. F4_TIGHT_APP follows at `:114`. |
| `build.sh:23287` — the fix19 block's F4_APP string | **Build machinery, not live rule text.** The fix19 patch block's appended string (inside the fix19 block, lines ~23267–23304); fix21 did not touch it. |

### 4b. "basic text only" — only verify19/verify20 anchor texts, each with the tightened rule adjacent

| Hit | Disposition |
|---|---|
| F4_SCOPE, Taste `:267` / orchestrate `:112` (staged + built): "for BASIC text only — body copy and plain reading text" | **Anchor, excluded.** The fix20 F4_SCOPE text itself — SPEC §3 forbids editing; verify20 asserts it verbatim. F4_TIGHT follows at `:277`/`:122`. |
| F4_SCOPE_APP, ui-ux-pro-max `:104` / orch-build-mvp `:47`: "for basic text only — body copy and plain reading text, never important text" | **Anchor.** The F4_SCOPE text in app-surface form; verify20 check 5 asserts F4_SCOPE_APP present in both files. F4_TIGHT_APP follows at `:114`/`:57`. |
| TYPESET_F20, typeset lens `:57` (staged + built): "The body face … is for basic text only" | **Anchor, not a finding.** `fix20/verify20.py:354` asserts TYPESET_F20 present in the lens (and `:355–356` that it sits after TYPESET_F19); editing it would break verify20. TYPESET_F21 follows at `:59` stating the tightened scope, and the new checkbox at `:78` states it as well. |
| `build.sh` hits (`:23325`, `:23328` fix20 block; `:23519–23520`, `:23525–23526` fixup20 blocks) | **Build machinery.** The fix20/fixup20 patch-block strings (old-side anchors and amended F4_SCOPE_APP), not live rule text; fix21 did not touch them. |

Judgment call, stated openly: the task brief's item-1 exclusion names
"the fix19 F4_RULE and fix20 F4_SCOPE texts themselves". TYPESET_F20
and F4_SCOPE_APP are not the F4_SCOPE constant literally, but they
are verify20 anchors asserted present by `verify20.py` (`:354` for
TYPESET_F20; SPEC §7 check 5 for F4_SCOPE_APP), and SPEC §3 forbids
editing any fix20 rule text in place — the design is that the new
rules govern the old ones by interpretation, with the tightened rule
placed immediately after in every file (table above). Flagging them
would demand edits that break verify20. They are therefore recorded
here as checked-and-cleared, not findings; if the parent intended a
different reading, that is a SPEC decision, not a sweep miss.

## 5. build.sh hygiene — PASS

- **fix21 block present and correct:** header
  `# --- fix21: long body and small text only; every text element gets
  an artistic font design decision (F4_TIGHT/F7) ---` at `:23600`;
  `print("fix21 upstream block applied")` at `:23635`; `PYEOF` at
  `:23636`; trailing blank line `:23637`; `# STEP 5 — Counts` at
  `:23638`. **38 lines** (`23600–23637` inclusive), confirmed
  independently: `diff build.sh.before-fix21 build.sh` =
  **+38 lines, −0 lines**; 23,609 + 38 = 23,647 ✓. (Fixup21's
  docstring independently records "exactly 38 lines, verified by
  diff against build.sh.before-fix21".)
- **Before STEP 5:** the block sits immediately before the STEP 5
  comment; its header reads `# Placement: before STEP 5 (after the
  fix20 blocks).` at `:23613`. The fix20-family headers all read the
  same way: fix20 `:23317` ("Placement: before STEP 5 (after the
  fix19 block)."), weave20 `:23344` ("this block runs before STEP 5,
  after the fix20 block."), fixup20 `:23511–23512`, fixup20b
  `:23550–23551`, fixup20c `:23576–23577` (all "Placement: before
  STEP 5 …").
- **No LAST claims:** `inserts this block last` in build.sh = **0**;
  `section 37` in build.sh = **0**; uppercase `LAST` lines in
  build.sh = exactly **2**, both the documented TRUE exception —
  `:19846` and `:19880`, "This patch runs LAST (after every
  audit_patch and qc_patch …)" in the two orch pipeline-gates patch
  blocks. `fix20/fixup20c.py:340–342` self-checks exactly this: the
  build must retain precisely those two lines. The fix21 block's own
  header contains no LAST claim (0 `LAST` lines in 23600–23637).
- **fix21 references in build.sh:** `grep -n fix21 build.sh`
  returns only lines 23600–23635 — the block itself, nothing stray.

## 6. Staged-vs-built diffs — PASS, pre-existing hunks only

`diff -q` staged → built for the four fix21 staged files:

| File | Result |
|---|---|
| `new-skills/orchestrate/SKILL.md` | IDENTICAL |
| `round2-skills/polish-pass/reference/lenses/typeset.md` | IDENTICAL |
| `new-skills/design-taste-frontend/SKILL.md` | DIFFERS — 1 hunk only (lines 9–13, frontmatter description) |
| `round2-skills/polish-pass/SKILL.md` | DIFFERS — 4 hunks only (lines 3, 15, 25, 32) |

Both diffs are the pre-existing build.sh patch blocks documented in
sweep23 §11, not fix21: the Taste hunk is the
`replace_text("design-taste-frontend", …)` "Use ONLY for a full company
or landing-page build from scratch…" description replacement at
`build.sh:606–614`; the polish-pass hunks are block "(f) polish-pass"
at `build.sh:~759`. All built-side strings are present in
`build.sh.before-fix21` (grep count 1 each — verified for all four
polish strings including the backticked
`` `ui-ux-pro-max`, `less-flat-ui`, and `design-taste-frontend` for
design direction `` line, and for the Taste string). Note: the
polish hunks sit one line lower than sweep23's listing (3/15/24/31 →
3/15/25/32); the hunk contents are identical and the shift is present
in both staged and built, so it is not a staged/built drift and not a
fix21 edit (fix21 touched only the harmony paragraph, line 22). The
fix21-relevant regions match exactly (§3 counts).

## 7. Leftover / placeholder text — PASS

`TODO|FIXME|XXX` (case-insensitive) in all ten fix21 files (4 staged
+ 6 built) = **0 hits**; in the fix21 block (build.sh lines
23600–23637) = **0 hits**. No half-finished sentence in any fix21
rule text or placement (all eight constants are full-text matches in
every placement, §3).

## 8. Counts — PASS

| Inventory | Count | Command |
|---|---:|---|
| skills | **166** | `ls skills \| wc -l` |
| agents | **72** | `ls agents \| wc -l` |
| rules | **123** | `ls rules \| wc -l` |
| commands | **87** | `ls commands \| wc -l` |
| hooks | **15** | `python3 -c "len(json.load(open('hooks/hooks.json'))['hooks'])"` |

Unchanged post-fix20, per SPEC §7 check 8 (166/72/123/87/15).

## 9. Verifiers re-run by this sweep — all green

| Verifier | Result |
|---|---:|
| `fix21/verify21.py` | **101/101 checks pass** (re-run by this sweep; its check 11 runs verify15/17/18/19/20 as subprocesses with exit 0 required) |

## Commands used (full list)

```
md5sum build.sh ; wc -l build.sh
python3 fix21/verify21.py
grep -n "fix21" build.sh ; grep -n "section 37" build.sh ; grep -n "inserts this block last" build.sh ; grep -n "LAST" build.sh ; grep -n "before STEP 5" build.sh ; grep -n "STEP 5" build.sh
sed -n '23595,23640p' build.sh ; sed -n '23307,23325p' build.sh ; sed -n '19830,19890p' build.sh
grep -rn "LAST|last" fix20/fixup20c.py fix21/fixup21.py ; grep -rn "fixup20d" fix20/ fix21/ build.sh
grep -n "TYPESET_F20|TYPESET_CHECKBOX" fix20/verify20.py
python3 /tmp/sweep29.py  (fix21/fix20 constant counts + md5s in all staged/built files; old-checkbox counts staged+built+build.sh; fix21-block unescape comparison; 'basic text only' and 'Body and plain text use Tiempos' greps staged+built+build.sh)
grep -n "Long body and small text only|Every text element gets an artistic font design decision|Fix #21 static checks|tightened font scope (fix #21)|Every component is an experience|Fix #20 static checks|Body-only scope; important text" <10 fix21 files>
grep -rni "used for basic text only" --exclude-dir=node_modules new-skills round2-skills hackathon-ecc
grep -rniE "TODO|FIXME|XXX" <10 fix21 files> ; sed -n '23600,23637p' build.sh | grep -niE "TODO|FIXME|XXX"
grep -rciE 'claude|codex|anthropic|opus|sonnet|haiku|composer-2\.5' --exclude-dir=node_modules hackathon-ecc/skills hackathon-ecc/agents hackathon-ecc/commands hackathon-ecc/rules hackathon-ecc/hooks hackathon-ecc/README.md ; same for new-skills round2-skills ; sed -n '23600,23637p' build.sh | grep -niE … ; per-constant banned scan of fix21.py
grep -n "Fix #21 static checks" new-skills/orchestrate/SKILL.md hackathon-ecc/skills/orchestrate/SKILL.md ; grep -n "5b. Final polish" … ; grep -n "tightened font scope (fix #21)" round2-skills/polish-pass/SKILL.md hackathon-ecc/skills/polish-pass/SKILL.md ; python3 (ordering find() checks: STATIC21 after STATIC20 + before 5b; POLISH_F21 after POLISH_F20; TYPESET_F21 after TYPESET_F20; checkbox line)
diff -q + diff (4 staged files vs built) ; grep -c <built-side strings> build.sh.before-fix21 build.sh
diff build.sh.before-fix21 build.sh | grep -c '^>' / '^<'
grep -rn "checkbox" --exclude-dir=node_modules new-skills round2-skills hackathon-ecc/skills ; grep -rn "TYPESET_CHECKBOX_NEW" --exclude-dir=node_modules --exclude-dir=__pycache__ . | grep -v "^./fix"
ls skills|wc -l ; ls agents|wc -l ; ls rules|wc -l ; ls commands|wc -l ; python3 -c "import json; print(len(json.load(open('hooks/hooks.json'))['hooks']))"
```
