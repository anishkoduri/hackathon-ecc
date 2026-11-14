#!/usr/bin/env python3
"""Fix #24 — coherence re-weave + Cursor dial-in (UPSTREAM halves).

Run by build.sh as the last patch step (after fix23, before STEP 5):
    python3 "$PLUGIN_ROOT/fix24/fix24.py" "$PLUGIN_DIR"

Operates on the BUILT tree only (upstream ECC / ui-ux-pro-max / marketplace
files, which have no staged source). Staged-source halves are edited
directly in new-skills/ / round2-skills/ / rewritten-skills/ / new-rules/
and flow through the STEP 2 copy. Every anchor asserts count==1 and fails
loudly on mismatch; the script exits non-zero on any error so the build
fails rather than shipping a half-patched tree.

Adjudications recorded here (see fix24/MANIFEST.md for the full table):
- C2: Rule 5's 0.05s floor governs container-level `staggerChildren`;
  B3 `staggerRow` 0.03s governs per-row settle steps (different scopes).
- C3: B15 `motionTokens.exitFactor` (0.8x) is the single source of truth
  per Rule 8; the quick-reference ~60-70% defers to it.
- C4: frozen verifier-asserted texts stay byte-identical (D19_RULE,
  D19_APP, X1/X1_APP, STATIC19, LF_D19, the DEPTH_F22 extension line);
  only non-asserted "six" sites move to "seven", plus a count-convention
  line in the staged files ("wherever a frozen rule text says 'six
  dimensions', read seven").
- S1 (styles.csv 89 rows vs "80 searchable styles" header) is NOT fixed
  here: verify23.py asserts the header exactly that way (verify23:214-218),
  so the change is OWED for a parent decision. Do not "fix" it in this
  script.
- D-6 (Stop/SessionStart hook existence) is NOT decided here: recorded
  as OWED to Cursor docs / the live smoke test (LIVE_SMOKE_TEST.md §15).
"""
import os
import re
import sys

BASE = sys.argv[1]
CHANGES = []
ERRORS = []


def read(f):
    with open(f, encoding="utf-8") as fh:
        return fh.read()


def write(f, text):
    with open(f, "w", encoding="utf-8") as fh:
        fh.write(text)


def exists(f):
    return os.path.exists(f)


def p(rel):
    return os.path.join(BASE, rel)


def sub(f, old, new, count=1):
    """Exact replacement; record an error if the anchor does not match."""
    text = read(f)
    n = text.count(old)
    if n != count:
        ERRORS.append(f"{f}: anchor found {n}x, expected {count}x :: {old[:120]!r}")
        return False
    write(f, text.replace(old, new))
    CHANGES.append(f"{f} — {old[:80]!r} -> {new[:80]!r}")
    return True


def resub(f, pattern, repl, count=None):
    text = read(f)
    new, n = re.subn(pattern, repl, text)
    if count is not None and n != count:
        ERRORS.append(f"{f}: regex {pattern!r} matched {n}x, expected {count}x")
        return False
    if n == 0:
        ERRORS.append(f"{f}: regex {pattern!r} matched 0x (expected >= 1)")
        return False
    write(f, new)
    CHANGES.append(f"{f} — regex {pattern!r} ({n}x)")
    return True


# ---------------------------------------------------------------- C2 (B3 30ms vs Rule 5 0.05s floor)
# Adjudication: Rule 5 governs container-level staggerChildren; B3 governs
# per-row settle steps. Different scopes, no conflict. The AB-03 conflict
# flags are replaced by the adjudication (they are not verifier-asserted).
f = p("skills/motion-patterns/SKILL.md")
if exists(f):
    sub(f,
        "5. **Stagger interval must stay between `0.05s` and `0.10s`.** Below feels mechanical; above feels sluggish.",
        "5. **Stagger interval must stay between `0.05s` and `0.10s`.** Below feels mechanical; above feels sluggish. Scope: this floor governs container-level `staggerChildren` intervals; per-row settle steps (`motionTokens.duration.staggerRow`, B3, 0.03s) are a different scope and are not bound by this floor (fix #24 adjudication of the AB-03 conflict flag).")
    sub(f,
        "`motionTokens.duration.staggerRow` (0.03s — under the AB-03 conflict flag vs\nRule 5's 0.05s floor; the parent adjudicates)",
        "`motionTokens.duration.staggerRow` (0.03s — per-row settle steps under B3; Rule 5's 0.05s floor governs container-level `staggerChildren` only, fix #24 adjudication)")
    sub(f,
        "exits at `motionTokens.exitFactor`\n(0.8× the enter — under the AB-03 conflict flag vs quick-reference ~60–70%;\nthe parent adjudicates)",
        "exits at `motionTokens.exitFactor`\n(0.8× the enter — `motionTokens.exitFactor` (B15) is the single source of truth per Rule 8; the quick-reference ~60–70% defers to it, fix #24 adjudication)")
f = p("skills/motion-foundations/SKILL.md")
if exists(f):
    sub(f,
        "    staggerRow: 0.03, // B3 (fix #22): list rows stagger by 30ms per row. CONFLICT FLAG (SPEC §4c): 0.03s sits below motion-patterns Rule 5's 0.05s floor — Rule 5 is NOT changed here; the parent adjudicates.",
        "    staggerRow: 0.03, // B3 (fix #22): list rows stagger by 30ms per row. Adjudicated fix #24: Rule 5's 0.05s floor governs container-level `staggerChildren`; B3 governs per-row settle steps — different scopes, no conflict.")
    sub(f,
        "  exitFactor: 0.8, // B15 (fix #22): exits run 20% shorter than their enter — exit duration = 0.8 x the matching enter duration. CONFLICT FLAG (SPEC §4c): quick-reference `exit-faster-than-enter` says ~60–70%; quick-reference is NOT changed here; the parent adjudicates.",
        "  exitFactor: 0.8, // B15 (fix #22): exits run 20% shorter than their enter — exit duration = 0.8 x the matching enter duration. Adjudicated fix #24: `motionTokens.exitFactor` (B15) is the single source of truth per Rule 8; the quick-reference ~60–70% defers to it.")

# ---------------------------------------------------------------- C3 (B15 0.8x vs quick-reference ~60-70%)
# The quick-reference entry defers to the token (same adjudication as above).
f = p("skills/ui-ux-pro-max/references/quick-reference.md")
if exists(f):
    sub(f,
        "- `exit-faster-than-enter` - Exit animations shorter than enter (~60–70% of enter duration) to feel responsive (MD motion)",
        "- `exit-faster-than-enter` - Exit animations shorter than enter (~60–70% of enter duration) to feel responsive (MD motion). Defers to `motionTokens.exitFactor` (B15, 0.8×) as the single source of truth per motion-foundations Rule 8 (fix #24 adjudication).")

# ---------------------------------------------------------------- C4b (six -> seven, editable sites only)
# ui-ux-pro-max:264 DIRECTIVES paragraph. NOT the X1_APP paragraph (:262,
# frozen — verify20 asserts X1_APP verbatim) and NOT D19_APP (:228, frozen
# — verify19 asserts it). verify22 asserts only the DIRECTIVES heading,
# never this body text, so the body is editable.
f = p("skills/ui-ux-pro-max/SKILL.md")
if exists(f):
    sub(f,
        "Every component entry in `design-system/<project-slug>/MASTER.md` records its directive alongside the experience it creates and its six fix #19 D19 dimension lines.",
        "Every component entry in `design-system/<project-slug>/MASTER.md` records its directive alongside the experience it creates and its seven fix #19 D19 dimension lines.")
    # C7: the MOTION_F23 statement here has no scope qualifier (motion-foundations
    # :205 already states the scope; the count-convention covers the frozen texts).
    sub(f,
        "Motion is recorded in the decision record with its D19 reason (Motion dimension) and its token values.",
        "Motion is recorded in the decision record with its D19 reason (Motion dimension) and its token values. Scope: on motion-governed surfaces (React/Next app surfaces) this means scroll entrances (M1) + staggers + micro-interactions; on Taste landing pages the scroll ban stands (scrolling moves nothing but the dealt moment) and the motion is the hero entrance + dealt moments + micro-interactions (fix #24 — same scope as motion-foundations MOTION_F23).")
# less-flat-ui LIQGLASS entry (:173 in the built copy; inserted by fix22's
# block, not by the home source). verify22 asserts only the LIQGLASS_F22
# token, never this body text. The home file's :527 sentence is inside
# LF_D19 (verify19 asserts it verbatim) and stays frozen.
f = p("skills/less-flat-ui/SKILL.md")
if exists(f):
    sub(f,
        "Record the treatment per surface in\n`docs/design-tokens.md` like every other treatment, with its six fix #19\nD19 dimension lines.",
        "Record the treatment per surface in\n`docs/design-tokens.md` like every other treatment, with its seven fix #19\nD19 dimension lines.")

# ---------------------------------------------------------------- E-2 (plankton install: macOS-only brew)
# Windows branch first (the plugin runs on Windows); the brew block stays,
# labelled macOS/Linux. Also softens the .ecc/settings.json pickup claim
# (D-9: unverified whether Cursor reads it — OWED to the smoke test, do not
# assert it either way).
f = p("skills/plankton-code-quality/SKILL.md")
if exists(f):
    sub(f,
        r'''```bash
# Install core dependencies
brew install jaq ruff uv

# Install Python linters
uv sync --all-extras

# Hooks activate automatically via the plugin — no start command needed
```''',
        r'''Windows (PowerShell) first — the plugin runs on Windows:
```powershell
# Install core dependencies (uv and ruff are pip-installable; jaq is a Rust tool)
py -m pip install uv ruff
cargo install jaq  # needs Rust; or download the jaq release binary from GitHub

# Install Python linters
uv sync --all-extras

# Hooks activate automatically via the plugin — no start command needed
```

macOS/Linux (bash):
```bash
# Install core dependencies
brew install jaq ruff uv

# Install Python linters
uv sync --all-extras

# Hooks activate automatically via the plugin — no start command needed
```''')
    sub(f,
        "No install command, no plugin config. The hooks in `.ecc/settings.json` are picked up automatically when you run Cursor in the Plankton directory.",
        "No install command, no plugin config. The hooks in `.ecc/settings.json` are picked up automatically when you run Cursor in the Plankton directory — whether Cursor reads `.ecc/settings.json` is decided by the live smoke test (LIVE_SMOKE_TEST.md §15), not asserted here (fix #24 D-9).")

# ---------------------------------------------------------------- E-4 (POSIX-only snippets: PowerShell first)
# auto-update.md: the node one-liner is platform-neutral JS; the shell
# wrapping is not. The JS contains no `$` and no double quotes, so it sits
# unchanged inside a PowerShell double-quoted string.
f = p("commands/auto-update.md")
if exists(f):
    sub(f,
        r'''```bash
# Preview the update without mutating anything''',
        r'''Windows (PowerShell):
```powershell
# Preview the update without mutating anything
$ECC_ROOT = node -e "var r=(function(){var p=require('path'),f=require('fs'),o=require('os');var e=process.env.ECC_PLUGIN_ROOT;if(e&&e.trim())return e.trim();function L(x){try{return require(p.join(x,'scripts','lib','resolve-ecc-root')).resolveEccRoot({probe:p.join('scripts','auto-update.js')})}catch(_){return null}}function D(x){try{return f.readdirSync(x,{withFileTypes:true}).filter(function(z){return z.isDirectory()}).map(function(z){return z.name})}catch(e){if(e.code==='ENOENT')return [];throw e}}var h=o.homedir();var cp=p.join(h,'.cursor','plugins');var q=p.join(cp,'local','hackathon-ecc');var r=L(q);if(r)return r;var A=D(cp);for(var a=0;a<A.length;a++){var B=D(p.join(cp,A[a]));for(var b=0;b<B.length;b++){r=L(p.join(cp,A[a],B[b]));if(r)return r}}return q})();console.log(r)"
node "$ECC_ROOT/scripts/auto-update.js" --dry-run

# Update only Cursor-managed files in the current project
node "$ECC_ROOT/scripts/auto-update.js" --target cursor

# Override the ECC repo root explicitly
node "$ECC_ROOT/scripts/auto-update.js" --repo-root /path/to/ECC
```

macOS/Linux (bash):
```bash
# Preview the update without mutating anything''')
# ecc-recipes: the $HOME / [ -d ] / find -exec directory probe.
f = p("skills/ecc-recipes/SKILL.md")
if exists(f):
    sub(f,
        r'''```bash
for D in \
  "$HOME"/.cursor/plugins/local/hackathon-ecc/commands''',
        r'''Windows (PowerShell):
```powershell
$cmdDir = $null
foreach ($D in @("$env:USERPROFILE\.cursor\plugins\local\hackathon-ecc\commands", "$env:USERPROFILE\.cursor\plugins\*\hackathon-ecc\commands", ".\commands", ".\.ecc\commands", "$env:USERPROFILE\.cursor\ecc\commands")) {
  if (Test-Path $D) { $cmdDir = $D; break }
}
if (-not $cmdDir) { Write-Error "No ECC commands directory found."; return }
Get-ChildItem $cmdDir -Filter *.md | ForEach-Object { $_.BaseName } | Sort-Object
```

macOS/Linux (bash):
```bash
for D in \
  "$HOME"/.cursor/plugins/local/hackathon-ecc/commands''')

# ---------------------------------------------------------------- E-6 (macOS-only commands, scoped)
f = p("agents/ecc-opensource-packager.md")
if exists(f):
    sub(f,
        "After writing, make it executable: `chmod +x setup.sh`",
        "After writing, make it executable: `chmod +x setup.sh` (macOS/Linux; on Windows use Git Bash for this step, or skip it — Windows has no executable bit)")
f = p("agents/ecc-swift-reviewer.md")
if exists(f):
    sub(f,
        """if command -v swiftlint >/dev/null 2>&1; then swiftlint lint --quiet; else echo "[info] swiftlint not installed - skipping lint (install via 'brew install swiftlint')"; fi""",
        """if command -v swiftlint >/dev/null 2>&1; then swiftlint lint --quiet; else echo "[info] swiftlint not installed - skipping lint (macOS: install via 'brew install swiftlint'; SwiftLint is macOS-only and does not run on Windows — skip this lint step on Windows)"; fi""")

# ---------------------------------------------------------------- G-1/G-2 (demo.md: direct invocation + dispatched-run key)
f = p("commands/demo.md")
if exists(f):
    sub(f,
        "When narration needs a key and none is set, the skill's narration-key prompt applies: if the user invoked /demo directly, prompt the user once, at the point the video is confirmed, for the ElevenLabs key (free tier, 10,000 chars/month, no credit card), and keep building meanwhile.",
        "When narration needs a key and none is set, the skill's narration-key prompt applies. **Direct invocation** means the user typed `/demo` at the prompt (not a `/demo` dispatched from a run — a dispatched `/demo` never prompts, see below): if the user invoked /demo directly, prompt the user once, at the point the video is confirmed, for the ElevenLabs key (free tier, 10,000 chars/month, no credit card), and keep building meanwhile.")
    sub(f,
        "If the dispatch says no key was received, use the key if present, else fall back to music-only/silent.",
        "If the dispatch carries no key, check the environment once for `ELEVENLABS_API_KEY`; if present, use it, else fall back to music-only/silent. Never prompt on a dispatched run.")

# ---------------------------------------------------------------- G-3 (orchestrate.md: "Show the plan first")
f = p("commands/orchestrate.md")
if exists(f):
    sub(f,
        "**Show the plan first** — your decomposition and the route each piece takes — then execute.",
        "**Show the plan first** (after grill-me and the narration-key prompt on a first build — the plan is shown before execution starts, not before grilling) — your decomposition and the route each piece takes — then execute.")

# ---------------------------------------------------------------- G-4 + picker (orch-build-mvp step 8 + step-4 design role)
f = p("skills/orch-build-mvp/SKILL.md")
if exists(f):
    sub(f,
        "Do NOT re-prompt at `/demo` time: the single early prompt covers the run, and a user-invoked `/demo` uses the key if present, else falls back to music-only/silent.",
        "Do NOT re-prompt at `/demo` time: the single early prompt covers the run, and a `/demo` dispatched from this run uses the key if present, else falls back to music-only/silent.")
    sub(f,
        "If the user asked for one, film the LOCAL app from the project dir after deploy (`APP_DIR` to the app dir) — `/demo` never films the deployed URL, so do NOT set `shots.json` `app.url` to it; the video file is `<app-name>-video/out/demo.mp4`.",
        "If the user asked for one, film the LOCAL app from the project dir after deploy (`APP_DIR` to the app dir) — `/demo` never films the deployed URL, so do NOT set `shots.json` `app.url` to it; the video file is `<app-name>-video/out/demo.mp4`. The `/demo` dispatch carries the Environment field naming `ELEVENLABS_API_KEY` when a key was received mid-run (see the Key handoff in the narration-key prompt above); otherwise it carries no key and `/demo` falls back to music-only/silent.")
    sub(f,
        "(slug form only — never bracket syntax; select Grok 4.7 High in Cursor's model picker before the first build, or the pin may silently fall back — file-level pin only, the live smoke test decides)",
        "(slug form only — never bracket syntax; see the picker note in orchestrate SKILL.md step 4)")

# ---------------------------------------------------------------- §2(a) agent references
# House form: `X` agent (`agents/ecc-X.md`) — short name first (frontmatter
# resolution), file path in parens (filename resolution). The 3 staged agents
# (deep-reasoner, fast-worker, scout) have name == filename and need nothing.
def agent_map():
    """short name -> filename for the 69 ecc-* agents (name != filename)."""
    m = {}
    adir = p("agents")
    for fn in sorted(os.listdir(adir)):
        if not fn.endswith(".md"):
            continue
        stem = fn[:-3]
        text = read(os.path.join(adir, fn))
        mm = re.search(r"^name: (\S+)\s*$", text, re.M)
        if mm and mm.group(1) != stem and stem.startswith("ecc-"):
            m[mm.group(1)] = fn
    return m


AMAP = agent_map()
CHANGES.append(f"agent map: {len(AMAP)} ecc-* agents (name != filename)")

# 1. Path lines: `- Agent: `agents/ecc-X.md`` -> `- Agent: `X` (`agents/ecc-X.md`)`.
#    Same for `- Companion agent:`. Expect exactly 19 in commands/; the 20th
#    `agents/ecc-*.md` line there is plan.md:199, already in house form
#    (`architect` agent (`agents/ecc-architect.md`)) — skipped by the
#    negative lookahead in dual_cite_invocations below. skills/ carries none
#    of this pattern.
def dual_cite_paths(f):
    text = read(f)
    n = [0]

    def repl(m):
        n[0] += 1
        return f"- Agent: `{m.group(2)}` (`agents/ecc-{m.group(2)}.md`)"

    text = re.sub(r"- Agent: `(agents/ecc-([a-z0-9-]+)\.md)`", repl, text)

    def repl_companion(m):
        n[0] += 1
        return f"- Companion agent: `{m.group(2)}` (`agents/ecc-{m.group(2)}.md`)"

    text = re.sub(r"- Companion agent: `(agents/ecc-([a-z0-9-]+)\.md)`", repl_companion, text)
    if n[0]:
        write(f, text)
        CHANGES.append(f"{f} — dual-cited {n[0]} Agent path line(s)")
    return n[0]


_total_paths = 0
for _fn in sorted(os.listdir(p("commands"))):
    if _fn.endswith(".md"):
        _total_paths += dual_cite_paths(p(os.path.join("commands", _fn)))
if _total_paths != 19:
    ERRORS.append(f"agent path lines in commands/: found {_total_paths}, expected 19")
for _root, _dirs, _files in os.walk(p("skills")):
    for _fn in sorted(_files):
        if _fn.endswith(".md"):
            dual_cite_paths(os.path.join(_root, _fn))

# 2. House form on invocation-grade lines (description frontmatter + lines
#    with an invocation verb), outside fenced code blocks. A line already
#    carrying `agents/ecc-X.md` is skipped. Prose mentions without an
#    invocation verb are covered by the fallback paragraph (common-agents.mdc).
_VERBS = re.compile(r"\b(spawn|use|invoke|launch|delegate|dispatch|run|call)\b", re.I)


def dual_cite_invocations(f):
    text = read(f)
    lines = text.split("\n")
    in_fence = False
    changed = 0
    for i, line in enumerate(lines):
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if "agents/ecc-" in line:
            continue
        if not (line.startswith("description:") or _VERBS.search(line)):
            continue
        new = line
        for short, fn in AMAP.items():
            pat = re.compile(r"`" + re.escape(short) + r"`( agent)?")
            new2, n = pat.subn(f"`{short}` agent (`agents/{fn}`)", new)
            if n:
                new = new2
        if new != line:
            lines[i] = new
            changed += 1
            CHANGES.append(f"{f}:{i + 1} — house form: {line.strip()[:100]!r}")
    if changed:
        write(f, "\n".join(lines))
    return changed


for _fn in sorted(os.listdir(p("commands"))):
    if _fn.endswith(".md"):
        dual_cite_invocations(p(os.path.join("commands", _fn)))
for _root, _dirs, _files in os.walk(p("skills")):
    for _fn in sorted(_files):
        if _fn.endswith(".md"):
            dual_cite_invocations(os.path.join(_root, _fn))
for _fn in sorted(os.listdir(p("rules"))):
    if _fn.endswith(".mdc"):
        dual_cite_invocations(p(os.path.join("rules", _fn)))

# 3. Roster + usage list + fallback paragraph (rules/common-agents.mdc).
f = p("rules/common-agents.mdc")
if exists(f):
    sub(f,
        "| architect | Implementation planning | Complex features, refactoring |\n| architect | System design | Architectural decisions |",
        "| architect (`agents/ecc-architect.md`) | Implementation planning + system design | Complex features, refactoring, architectural decisions |")
    for _short, _purpose, _when in [
        ("tdd-guide", "Test-driven development", "New features, bug fixes"),
        ("code-reviewer", "Code review", "After writing code"),
        ("security-reviewer", "Security analysis", "Before commits"),
        ("build-error-resolver", "Fix build errors", "When build fails"),
        ("e2e-runner", "E2E testing", "Critical user flows"),
        ("refactor-cleaner", "Dead code cleanup", "Code maintenance"),
        ("doc-updater", "Documentation", "Updating docs"),
    ]:
        sub(f,
            f"| {_short} | {_purpose} | {_when} |",
            f"| {_short} (`agents/ecc-{_short}.md`) | {_purpose} | {_when} |")
    sub(f,
        "1. Complex feature requests — Use **architect** agent, but only when the work spans several pieces at once or the user asks to delegate; otherwise do the work directly in the main context",
        "1. Complex feature requests — Use **architect** agent (`agents/ecc-architect.md`), but only when the work spans several pieces at once or the user asks to delegate; otherwise do the work directly in the main context")
    sub(f,
        "2. Code just written/modified - Use **code-reviewer** agent",
        "2. Code just written/modified - Use **code-reviewer** agent (`agents/ecc-code-reviewer.md`)")
    sub(f,
        "3. Bug fix or new feature - Use **tdd-guide** agent",
        "3. Bug fix or new feature - Use **tdd-guide** agent (`agents/ecc-tdd-guide.md`)")
    sub(f,
        "4. Architectural decision — Use **architect** agent, but only when the work spans several pieces at once or the user asks to delegate; otherwise do the work directly in the main context",
        "4. Architectural decision — Use **architect** agent (`agents/ecc-architect.md`), but only when the work spans several pieces at once or the user asks to delegate; otherwise do the work directly in the main context")
    sub(f,
        "## Parallel Task Execution",
        """## If a named agent does not resolve (fix #24)

Cursor may resolve agents by frontmatter `name:` or by filename — the plugin cites both forms at every invocation (`` `X` agent (`agents/ecc-X.md`) ``) so either resolution works. If a named agent still cannot be resolved (Cursor reports it cannot find `X`), spawn a general subagent on `cursor-grok-4.6-high-fast` (or `grok-4.7-high` for the 4.7-pinned agents: `architect`, `healthcare-reviewer`, `spec-miner`, `deep-reasoner`) with the agent file's instructions inlined, and record the miss in the run ledger.

## Parallel Task Execution""")

# 4. `general-purpose` is a Claude Code built-in agent type, not a plugin
#    agent — use Cursor wording (dispatch-prompt.md is staged; these two are upstream).
f = p("skills/skill-stocktake/SKILL.md")
if exists(f):
    sub(f,
        "Spawn a Cursor subagent (general-purpose) with the actual JSON emitted by Phase 1",
        "Spawn a Cursor subagent (general subagent) with the actual JSON emitted by Phase 1")
f = p("skills/rules-distill/SKILL.md")
if exists(f):
    sub(f,
        "Launch a general-purpose Agent with the following prompt:",
        "Launch a general subagent with the following prompt:")

# 5. `design-lead` is a role, not an agent file — name the executor skill + pin.
_DESIGN_LEAD_OLD = "INVOKE the design-lead (model `grok-4.7-high`) first to generate the direction through the package skills (`design-taste-frontend` for a landing page, `ui-ux-pro-max` for a dashboard/app surface, per the design-package rule)"
_DESIGN_LEAD_NEW = "dispatch to the design skill for that surface — `design-taste-frontend` for a landing page, `ui-ux-pro-max` for a dashboard/app surface — on model `grok-4.7-high`, first to generate the direction through the package skills (per the design-package rule)"
for _rel in ("commands/gan-build.md", "commands/gan-design.md"):
    f = p(_rel)
    if exists(f):
        sub(f, _DESIGN_LEAD_OLD, _DESIGN_LEAD_NEW)

# 6. continuous-learning-v2 :123 — table cell in the ASCII diagram (the box
#    is already ragged, so the longer dual-cited cell does not newly break it).
f = p("skills/continuous-learning-v2/SKILL.md")
if exists(f):
    sub(f,
        "|   * agents/ecc-refactor-cleaner.md           |",
        "|   * `refactor-cleaner` (`agents/ecc-refactor-cleaner.md`) |")

# ---------------------------------------------------------------- A5/A8 (browser-qa citations for orphan tokens)
f = p("skills/browser-qa/SKILL.md")
if exists(f):
    sub(f,
        "the trio identical to the previous build's trio with no recorded reuse reason",
        "the trio (`TRIO_F23`) identical to the previous build's trio with no recorded reuse reason")
    sub(f,
        "Full checklist (candidate evidence): `polish-pass` reference/alignment.md (`ALIGN_F23`).",
        "Full checklist (candidate evidence): `polish-pass` reference/alignment.md (`ALIGN_F23`) — sub-checks `ALIGN_F23_NAV` (nav items evenly spaced and centered), `ALIGN_F23_LABELS` (no label collisions — diagrams, strips, stamps), `ALIGN_F23_CLIP` (no text clipped, no element escaping its frame), `ALIGN_F23_ACTIONS` (primary actions centered on their axis), `ALIGN_F23_PANELS` (desktop side panels symmetric and top-aligned).")

# ---------------------------------------------------------------- C-1 (block-no-verify: PowerShell/cmd branch)
# The POSIX scanner tokenizes `git ... --no-verify` correctly in the common
# case, and the opaque word scan is the backstop — but a `powershell
# -Command "..."` / `cmd /c ...` wrapper was unmodeled (SHELLS has no
# PowerShell entry), so a nested bypass was only caught by the backstop.
# Model the wrappers the way shellRole models sh -c: extract the script
# operand as code to be re-scanned; -EncodedCommand/-File stay opaque.
_POWERSHELL_JS = r'''// --- PowerShell / cmd wrappers (fix #24, C-1) ---------------------------------
// Cursor runs shell commands through PowerShell on Windows. The POSIX shell
// grammar above cannot read PowerShell: `-Command`/`-c` takes the script as
// its operand (or as all remaining words), `-EncodedCommand` is base64 the
// scanner cannot read, and `-File` is a file we cannot read. Best-effort
// only: PowerShell quoting, variables, the `&` call operator,
// `Invoke-Expression`, and `Start-Process` are NOT modeled — a bypass hidden
// behind one of those falls back to the opaque word scan (inspectOpaque),
// which still catches a literal `git ... --no-verify` in the raw text.
function powershellRole(words, budget) {
  let i = 1;
  while (i < words.length) {
    const option = words[i].value;
    budget.spend(option.length + 1);
    if (option === '--' || option === '-') { i++; break; }
    if (!/^-/.test(option)) break;
    const lower = option.toLowerCase();
    if (lower === '-command' || lower === '-c') {
      // The script is the next operand, or all remaining words when unquoted.
      const rest = words.slice(i + 1).map(word => word.value).join(' ');
      return { kind: 'shell', code: rest || undefined, stdin: false };
    }
    if (lower === '-encodedcommand' || lower === '-e' || lower === '-ec') return { ...OPAQUE_SHELL };
    if (lower === '-file' || lower === '-f') return { ...OPAQUE_SHELL };
    if (lower === '-executionpolicy' || lower === '-ep' || lower === '-windowstyle' || lower === '-workingdirectory' || lower === '-inputformat' || lower === '-outputformat' || lower === '-configurationname') { i += 2; continue; }
    if (lower === '-noprofile' || lower === '-noninteractive' || lower === '-nologo' || lower === '-sta' || lower === '-mta') { i++; continue; }
    return { ...OPAQUE_SHELL };
  }
  // No -Command/-File: a script filename and its arguments are not shell source.
  return { kind: 'shell', stdin: i === words.length };
}

// cmd.exe: `/c` (or `/k`) runs the rest of the line as the command; anything
// else is opaque. Best-effort (fix #24, C-1): cmd quoting/expansion is not modeled.
function cmdRole(words, budget) {
  let i = 1;
  while (i < words.length) {
    const option = words[i].value;
    budget.spend(option.length + 1);
    const lower = option.toLowerCase();
    if (lower === '/c' || lower === '/k') {
      const rest = words.slice(i + 1).map(word => word.value).join(' ');
      return { kind: 'shell', code: rest || undefined, stdin: false };
    }
    if (lower === '/d' || lower === '/q') { i++; continue; }
    return { ...OPAQUE_SHELL };
  }
  return { kind: 'shell', stdin: i === words.length };
}

'''
f = p("scripts/hooks/block-no-verify.js")
if exists(f):
    sub(f,
        "function shellRole(words, budget, shell) {",
        _POWERSHELL_JS + "function shellRole(words, budget, shell) {")
    sub(f,
        "const SHELLS = new Set(['sh', 'bash', 'dash', 'zsh', 'ksh']);",
        "const SHELLS = new Set(['sh', 'bash', 'dash', 'zsh', 'ksh']); // POSIX shells only — PowerShell/cmd are handled by powershellRole/cmdRole below (fix #24, C-1); do not add them here, their option grammar differs.")
    sub(f,
        "  if (SHELLS.has(name)) return shellRole(words, budget, name);",
        "  if (SHELLS.has(name)) return shellRole(words, budget, name);\n  // fix #24 (C-1): PowerShell/cmd wrappers (POSIX SHELLS set above is not them).\n  const lowerName = name.toLowerCase();\n  if (lowerName === 'powershell' || lowerName === 'powershell.exe' || lowerName === 'pwsh' || lowerName === 'pwsh.exe') return powershellRole(words, budget);\n  if (lowerName === 'cmd' || lowerName === 'cmd.exe') return cmdRole(words, budget);")

# ---------------------------------------------------------------- C-2/C-3 (unwired hook headers: flag-and-document)
# Anchors are POST-fix16 text ("Upstream-only") — fix16 runs before this script.
f = p("scripts/hooks/auto-tmux-dev.js")
if exists(f):
    sub(f,
        " * Auto-Tmux Dev Hook — Upstream-only (not wired in this Cursor plugin — Cursor has no PreToolUse event) — start dev servers in tmux/cmd automatically",
        " * Auto-Tmux Dev Hook — Upstream-only (not wired in this Cursor plugin — Cursor has no PreToolUse event) — start dev servers in tmux/cmd automatically\n * fix #24: unwired and dead in this plugin — the POSIX tmux path (`which`, `2>/dev/null`) never runs under Cursor-on-Windows/PowerShell, and the Windows cmd path is likewise unwired; kept as reference only.")
f = p("scripts/hooks/desktop-notify.js")
if exists(f):
    sub(f,
        " * Desktop Notification Hook (Stop) — Upstream-only (not wired in this Cursor plugin — Cursor has no Stop hook event)",
        " * Desktop Notification Hook (Stop) — Upstream-only (not wired in this Cursor plugin — Cursor has no Stop hook event)\n * fix #24: unwired in this plugin; the Windows branch needs the BurntToast module, which the plugin neither declares nor installs — on Windows this hook cannot notify without it.")

# ---------------------------------------------------------------- D-8 (harness-audit reads a .opencode/ path that does not ship)
f = p("scripts/harness-audit.js")
if exists(f):
    sub(f,
        "  const commandParity = safeRead(rootDir, '.opencode/commands/harness-audit.md').trim();",
        "  // fix #24 (D-8): '.opencode/commands/harness-audit.md' is an upstream-only\n  // path and does not ship in this Cursor plugin, so the parity check below\n  // can never pass here — treat a failure of tool-command-parity as\n  // not-applicable, not as a real finding.\n  const commandParity = safeRead(rootDir, '.opencode/commands/harness-audit.md').trim();")
    sub(f,
        "      description: 'Harness-audit command parity exists between primary and OpenCode command docs',",
        "      description: 'Harness-audit command parity exists between primary and OpenCode command docs (upstream-only path; does not ship in this Cursor plugin — not applicable here)',")
    sub(f,
        "      fix: 'Sync commands/harness-audit.md and .opencode/commands/harness-audit.md.',",
        "      fix: 'Upstream-only path; does not ship in this Cursor plugin — ignore this check here.',")

# ---------------------------------------------------------------- D-9 (angular mcp.md: Gemini CLI is not a Cursor path)
f = p("skills/angular-developer/references/mcp.md")
if exists(f):
    sub(f,
        "### Gemini CLI\n\nCreate `.gemini/settings.json` in the project root:",
        "### Gemini CLI\n\n> Not a Cursor path: the Gemini CLI is a separate Google tool, not a Cursor MCP server — this section documents the upstream Angular setup, not a plugin install step.\n\nCreate `.gemini/settings.json` in the project root:")

# ---------------------------------------------------------------- F-1/F-2 + picker + counts (README.md)
# README is written by build.sh before this script runs, so it is patched here.
f = p("README.md")
if exists(f):
    sub(f,
        "2. Or test it locally: copy this `hackathon-ecc` directory to\n   `~/.cursor/plugins/local/hackathon-ecc` (copy it — do not symlink it\n   in from elsewhere), then restart Cursor or run **Developer: Reload\n   Window**, and open **Customize** to confirm the plugin's rules,\n   skills, agents, commands, and MCP servers appear.",
        "2. Or test it locally: clone the repo directly into `~/.cursor/plugins/local/hackathon-ecc` (clone it — do not symlink it in from elsewhere, and do not copy it: a plain copy has no `.git`, so it cannot be updated with `git pull` — see Updating below), then restart Cursor or run **Developer: Reload\n   Window**, and open **Customize** to confirm the plugin's rules,\n   skills, agents, commands, and MCP servers appear.")
    sub(f,
        "  while building. With the 25 hackathon additions below, the plugin ships\n  166 skills, 72 agents, 123 rules, and 87 commands in total.",
        "  while building. With the hackathon additions below, the plugin ships\n  166 skills, 72 agents, 123 rules, and 87 commands in total (69 agents as-shipped + 3 staged orchestrate agents; 121 rules as-shipped + 2 new rules — `hackathon-mode`, `ponytail`; skill and command totals per build.sh STEP 5 counts).")
    sub(f,
        "installation is manual with no official Cursor Marketplace listing, updates require rebuilding from `build.sh`, and 56 MB is loaded into a project that may only need a tenth of it.",
        "installation is manual with no official Cursor Marketplace listing, updates follow the Updating section below (git pull for a local clone, rebuild + re-copy for a copy install), and 56 MB is loaded into a project that may only need a tenth of it.")
    sub(f,
        "- **Before the first build — Grok 4.7 High in the model picker:** the plugin pins its design role to `grok-4.7-high`. Cursor's subagent model allowlist is coupled to the model-picker dropdown, so select **Grok 4.7 High** in Cursor's model picker before the first build, or the design pin may silently fall back to another model. This is a one-time setup note, not a mid-build ask. File-level pin only — whether it holds is decided by the live smoke test (`LIVE_SMOKE_TEST.md` §14). Task agents pin to Grok 4.6 High Fast (`cursor-grok-4.6-high-fast`); the orchestrator and the design/implementation roles pin to Grok 4.7 High (`grok-4.7-high`).",
        "- **Before the first build — Grok 4.7 High in the model picker:** select Grok 4.7 High in Cursor's model picker before the first build; see the picker note in `skills/orchestrate/SKILL.md` step 4. Task agents pin to Grok 4.6 High Fast (`cursor-grok-4.6-high-fast`); the orchestrator and the design/implementation roles pin to Grok 4.7 High (`grok-4.7-high`).")
    sub(f,
        "## Rebuild",
        """## Updating

This is the single authoritative update path — every other mention of updating in the plugin points here.

- **Local clone (the normal install):** the plugin lives as a git clone at `~/.cursor/plugins/local/hackathon-ecc`. Update it with `git pull` inside that directory, then run **Developer: Reload Window** in Cursor. No rebuild, no re-copy.
- **Copy install:** if the plugin dir is a plain copy (no `.git` inside it), `git pull` cannot work there — update by rebuilding from the source repo (`bash ~/workspace/hackathon-plugin/build.sh`) and re-copying the rebuilt `hackathon-ecc/` directory over the installed one, then **Developer: Reload Window**.
- **Delta bundles:** for an incremental update without a full re-clone, the maintainer can ship a bundle (`git bundle create update.bundle main ^<prev-commit>`); apply it with `git fetch <bundle> main` + `git merge --ff-only FETCH_HEAD` (the positive side must be a branch name, not a bare SHA), then **Developer: Reload Window**.
- **Never symlink** a plugin directory in from elsewhere — Cursor skips symlinks pointing outside `~/.cursor/plugins/local/`. If a repo-link copy of the plugin is also installed, remove it first: a repo-link copy takes precedence over the local one.

## Rebuild""")


# ---------------------------------------------------------------- F-10 (ui-ux-pro-max: name the inventory)
# Worker C F-10: Taste step 4a names the inventory (staged, I-DESIGN), but
# ui-ux-pro-max — an upstream skill, only patchable at build time — never did.
# Pointer goes on the Query Contract line that decides visual direction.
f = p("skills/ui-ux-pro-max/SKILL.md")
if exists(f):
    sub(f,
        "1. **New project/page or system-wide visual direction** (except a full landing/company page — that belongs to `design-taste-frontend`) → use `--design-system`.",
        "1. **New project/page or system-wide visual direction** (except a full landing/company page — that belongs to `design-taste-frontend`) → use `--design-system`. Before deciding, read the design inventory (`skills/orchestrate/references/design-inventory.md`) and choose from its inventoried elements — the direction is generated from the inventory, never from taste (fix #24 F-10).")


# ---------------------------------------------------------------- main
_log_lines = ["# fix24 run log", "",
              f"## Errors ({len(ERRORS)})"]
_log_lines += [f"- {e}" for e in ERRORS] or ["- none"]
_log_lines += ["", f"## Changes ({len(CHANGES)})"]
_log_lines += [f"- {c}" for c in CHANGES] or ["- none"]
_log_dir = os.path.join(os.path.dirname(BASE.rstrip("/")), "fix24")
os.makedirs(_log_dir, exist_ok=True)
with open(os.path.join(_log_dir, "fix24-run-log.md"), "w", encoding="utf-8") as _fh:
    _fh.write("\n".join(_log_lines) + "\n")
print(f"fix24: {len(CHANGES)} change(s)")
for c in CHANGES:
    print(f"  - {c}")
if ERRORS:
    print(f"fix24: {len(ERRORS)} ERROR(S)", file=sys.stderr)
    for e in ERRORS:
        print(f"  ! {e}", file=sys.stderr)
    sys.exit(1)
print("fix24: OK")
