---
name: code-mode
description: Use when the orchestrator faces data-heavy mechanical work — scanning, filtering, counting, or transforming across many files, multi-file consistency checks — and chaining individual tool calls would flood its context with intermediate results. The orchestrator writes ONE program against this skill's helper library, gates it, runs it, and reads only a distilled digest (≤500 E3); raw output stays in files. Never for design judgment or verdicts: script-first applies to the orchestrator's own mechanical work, and subagent briefs and returns are unchanged.
---

> **Hackathon-ecc note (fix #34, CODEMODE_F34).** This skill implements the code-mode PATTERN for this plugin — it is **not the Code Mode feature and enables nothing**. Code Mode the feature exists only inside its vendor's own runtime (an interactive terminal session, the vendor API, the vendor's models only; vendor docs — evidence basis in fix34/SPEC.md) and this plugin runs in Cursor, so nothing here turns it on or claims its name for the result. What this skill takes from the pattern is the working shape: instead of calling tools one at a time and reading every result before deciding the next step, the orchestrator writes a small program that does the mechanical work — loops, filters, counts — and returns only the digest it needs to read. The plugin's runtime is the one it already has: the orchestrator's terminal and Python (stdlib only). The vendors' savings figures for the pattern (the 150K→2K example, the −37% programmatic-tool-calling average, Cloudflare's 99.9%) are vendor-reported numbers from their workloads; this skill adopts none of them as a plugin claim. This plugin's own effect is a live-test question. **Routing:** the orchestrator itself works this way; the skill carries no trigger key — `orchestrate` (the cost policy + the step-5a statics) and `browser-qa` (scripted evidence collection — verdicts unchanged) invoke it by name.

# Code mode — script-first mechanical work

One gated program, one distilled digest, raw output in files. This skill exists because chained tool calls tax the orchestrator twice: every intermediate result passes through its context, and every call costs a full inference pass to decide the next one. Mechanical work — the kind with a right answer a program can compute — should not pay either tax. Judgment work should never be scripted at all (§5).

## 1. The helper library (`scripts/`)

Four small stdlib-only Python modules live in this skill's `scripts/` directory (shipped as `skills/code-mode/scripts/`). They are the typed API the orchestrator writes against (the pattern's premise: models write code against an API better than they chain tool calls). **Progressive disclosure:** a script imports only the modules it needs — a module not imported is never read — and this table is the contract; read a module's source only when a signature here is not enough.

| Module | Signatures (the contract) | Job |
|---|---|---|
| `cm_read` | `read_text(path) -> str`; `list_files(root, suffixes) -> [relpath]`; `grep(root, pattern, suffixes) -> [{path, line, text}]` | Read-side only: read one file, enumerate a tree, search with match records built for counting and digesting |
| `cm_census` | `e3(text) -> int`; `census_file(path) -> {path, e3, bytes, lines}`; `census_tree(root, suffixes) -> {files, totals}` | The plugin's canonical E3 estimator (the ruler every census in this tree uses) + per-file / per-tree token census |
| `cm_write` | `write_text(path, text, root, overwrite=False) -> record`; `append_line(path, line, root) -> record`; raises `GuardError` | Guarded writes: paths resolved and confined to the declared root in code, one file per call, overwrite only with the flag stated — and **no delete operation exists in the library at all** |
| `cm_report` | `CAP_E3 = 500`; `distill(headline, counts, exceptions, raw_pointer) -> str`; `finish(raw_text, raw_path, headline, counts, exceptions) -> str` | The return discipline, enforced mechanically: raw output to a file, a digest of at most the cap back to the model |

A script starts by putting this directory on `sys.path` and importing the two or three modules its job needs — never all four by default. The library's guards are enforced in code, not prose: `cm_write` refuses an out-of-scope path at write time even if a script's own logic missed it, and a delete cannot be expressed through the helpers at all.

## 2. The script-first rule (SCRIPT-FIRST_F34)

**For data-heavy mechanical work, write ONE program and run it, instead of chaining individual tool calls; loops and conditionals live in the code.** The rule fires on these shapes (the pattern's "most beneficial" list, in this tree's terms):

- scanning, filtering, counting, or transforming across many files (a tree census, a needle sweep, a consistency scan);
- multi-file consistency checks — the data gathering under `orchestrate` step 5a's static checks, QA evidence gathering (§4);
- processing what the research sweep gathered (RESEARCHBRIEF_F34): extracting, counting, deduping, and compiling the brief's source log from fetched material — the sweep's browsing itself stays `prebuild-research`'s own capped model step (gate item 4 below); only its mechanical downstream is script-first;
- any job of 3+ related calls whose intermediate results the model does not need to read.

The rule does **not** fire on a single one-off call, a quick lookup with a small response, or work whose intermediate results the model must reason over (the pattern's "less beneficial" list): the write-gate-run overhead exceeds the saving, and judgment smuggled into a script is a finding, not an optimization.

**Relationship to the regular batching discipline (explicit):** direct calls keep this tree's own discipline — independent read-only calls (reads, greps, searches) batched in parallel, writes serialized. When a gated script does the work, the script's internal batching governs **inside the script** (its parallelism is code, bounded by the gate record), and the direct-call discipline continues to govern every call outside it; the two never mix inside one operation. **Budget accounting:** a gated script run counts as ONE orchestrator action; the script logs every operation it performs to its raw-output file, so the work stays bounded and auditable — the count moves, the audit trail does not shrink.

## 3. Distilled returns (the 500 E3 cap)

A script's model-facing output is at most **500 E3**, enforced by `cm_report` (it truncates the exception list with a "+N more" pointer rather than overflowing). Why 500: a full work return runs to ~2,000 tokens (status, files changed, decisions); a script return is a mechanical digest — status, counts, exceptions, pointers — a strict subset of that, so a quarter of it is generous. It also sits under the ~600-token research-brief cap (RESEARCHBRIEF_F34), a richer artifact consumed inline by two pipeline steps. A digest that cannot fit in 500 E3 is not a digest; it is the firehose wearing a summary's clothes.

Raw output goes to files: `.hackathon/script-output/<script>.log` in a project run. The model reads the digest, and re-reads the raw file selectively — by line range, only when a digest line needs evidence. Pasting raw output into context "to be thorough" is the exact failure this skill exists to prevent.

## 4. The review-before-run gate (SCRIPT-GATE_F34)

**Before a script executes, it passes a recorded review against this checklist. A script that fails any item does not run — fix the script and re-gate.** (The shape is the pattern's: Code Mode's auto mode reviews the code once, before it runs, rather than each call inside it. This plugin's version is a human-readable checklist, kept stricter — it binds reads as well as writes, because it is cheap.)

1. **Scope** — every path the script touches is inside the project tree / the run's declared scope. No path is computed from untrusted content.
2. **Serialized writes** — one writer per file; no parallel writes to the same file; writes go through `cm_write` or are plainly serialized in the code.
3. **No destructive operations** — no deletes, no overwrites without the explicit flag visible in the script, nothing the helpers' guards would refuse.
4. **Network bounds** — no network calls. A script never browses; the research sweep stays `prebuild-research`'s own capped step.
5. **Operations log** — the script writes its op log (what it read and wrote) to its raw-output file, and the gate outcome is recorded as one line in `.hackathon/run-ledger.md`: script name, `gate: PASS`, op count, raw file.
6. **Guardrails untouched** — the script makes no decision a rule reserves to the orchestrator or the user: MODELSEL_F33, the approval rules, the design contract's deviation rules (DESIGNCONTRACT_F34), and the restatement gate all bind exactly as before. Script-first changes HOW mechanical work runs, never WHO decides.

**Contract citation (fix #34).** A gated script that executes or evidences a build step is recorded in the run ledger by item 5's gate line, and the design contract's Deviations field may cite that line (script name + gate record) as the deviation's evidence (DESIGNCONTRACT_F34, Taste step 4a). The ledger is the script's record; the contract cites it rather than re-logging it, and a citation never turns a script's output into a decision — item 6 still binds.

## 5. Applicability boundary (binding)

Script-first applies to **the orchestrator's own mechanical work, full stop** — there is no other leg in this tree for it to apply to. Subagents do not run these scripts: their briefs and returns stay exactly as they are. And a script gathers evidence; it never judges: design decisions, the restatement gate's comparisons, and every `browser-qa` verdict remain model work. `browser-qa`'s mechanical data collection (DOM / screenshot inventories, coverage-matrix measurements, console / network log digests) may be scripted — the verdicts are still read off that evidence by `browser-qa` alone, the sole verdict executor.

## 6. Worked shape

**A census / consistency scan (the common case).** The orchestrator needs the built tree's census + a needle check across 80 files. Script: import `cm_census`, `cm_read`, `cm_report`; census the tree; grep the needle; write the full records to `.hackathon/script-output/census.log` via `cm_report.finish`; print the digest — `DONE tree census / counts: files=83, e3=…, missing_needle=2 / ! skills/x/SKILL.md / ! skills/y/SKILL.md / raw: …`. The model reads ~40 E3 instead of 80 file reads.


## What NOT to do

- **No scripting one-off calls.** A single read or lookup is a direct call (batched in parallel if several are independent) — writing, gating, and running a program for it costs more than it saves.
- **No ungated runs.** "It's just a read" is not an exemption; the gate is one recorded checklist line, and it is what makes the pattern auditable.
- **No verdicts from scripts.** A script that prints PASS/FAIL on a judgment question has smuggled a decision past the rules that own it (browser-qa's verdicts, the contract gate, MODELSEL) — a finding against the run.
- **No raw output in context.** If the model needs more than the digest, it reads the raw file by line range. Dumping the file defeats the round.
- **No claiming Code Mode.** Plugin prose never says a run "used Code Mode" — it used the code-mode pattern, in Cursor, via this skill (CODEMODE_F34's boundary).

## Files

- Helper library: `skills/code-mode/scripts/` (`cm_read.py`, `cm_census.py`, `cm_write.py`, `cm_report.py`) — stdlib-only Python, typed signatures, imported on demand
- Invoked by: `skills/orchestrate/SKILL.md` (Cost & context policy; step 5a static-check gathering), `skills/browser-qa/SKILL.md` (scripted evidence collection — verdicts unchanged)
- Raw-output home in a project run: `.hackathon/script-output/` (digests return to the orchestrator; raw files stay on disk)
- Evidence basis: fix34/SPEC.md (the Code Mode docs + code-execution-with-MCP + programmatic tool calling; Cloudflare's Code Mode posts), all savings figures vendor-reported and none adopted as plugin claims
