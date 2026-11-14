# Fix #24 SPEC — Re-weave everything together, dialed in for Cursor

## §0 Origin

Anish, Nov 12, 22:37 CST: "Go through and weave everything together
again also dial it for cursor."

Fixes #14–#23 layered a lot onto the plugin: fonts, D19 (now seven
dimensions), overdrive, Hallmark/Impeccable, fix #22's 144 items + 11
libraries + Vercel checklist + depth + orbs, fix #23's ambition/inventory/
CORE/motion/type-audit/hero/functionality/alignment/dynamic. Each fix wove
its own section. This fix goes through the WHOLE plugin and weaves it
together again as one coherent system — and tunes it for Cursor, the
runtime it actually runs in.

## §1 Full re-weave (coherence)

- (a) Pointer/anchor audit: every cross-skill pointer resolves; every
  `_Fxx` anchor token resolves exactly as intended; no orphans, no dangling
  references (the fix #22 `liquid-glass-design` dangling reference is the
  model of what must not recur — verify, do not assume).
- (b) Dedupe/contradiction pass: the same rule stated in two places must
  agree, or one must defer to the other BY NAME. Contradictions get a
  recorded adjudication in the manifest (which statement governs, and why),
  not a silent pick.
- (c) One story: the design-package flow reads as a single coherent flow —
  grill → design package (inventory read FIRST, before deciding) → build →
  verify → polish → deploy → commit → README → final report, with /demo
  never automatic. Every inventoried element (design-inventory.md) is
  reachable from that flow, or recorded as intentionally unreachable with
  its reason.
- (d) Staleness sweep: reconcile drifted counts and texts. Known drift to
  fix: styles.csv has 89 rows vs the "80 searchable styles" header (csv is
  the source — reconcile the header). Any other count drift found the same
  way. Frozen-text staleness is RECORDED, not rewritten: the "six
  dimensions" texts stay byte-identical (verify19 asserts D19_RULE
  verbatim); the extension line is the sanctioned amending record. Do NOT
  rewrite any text a prior verifier asserts verbatim — if a rewrite is
  needed, the verifier change is a parent decision, recorded in the
  manifest, not a coordinator edit.

## §2 Dial it in for Cursor

Cursor is the runtime. The plugin must read as a Cursor-native system, not
a ported Claude Code one.

- (a) Agent references robust to both resolutions: every agent invocation
  uses the form that works under BOTH frontmatter-name and filename
  resolution where possible. Where a choice is forced, record which form
  and why. Do NOT pre-decide the smoke test's step-6 question (frontmatter
  name vs filename) — the plugin must be robust to either outcome, and the
  smoke test decides it live.
- (b) Model pins: slug-form only, never bracket syntax; Grok pins only
  (`grok-4.7-high` / `cursor-grok-4.6-high-fast`, never bare
  `grok-4.6-high-fast`). The picker prerequisite (select Grok 4.7 High in
  Cursor's model picker before the first build, because the subagent
  allowlist is coupled to the picker) is stated ONCE in the authoritative
  place and referenced elsewhere, not restated differently in five places.
- (c) Hooks on Windows: hooks.json + adapter.js + every hook script
  verified for Cursor-on-Windows execution (Cursor runs hook commands
  through PowerShell on Windows). POSIX-only constructs are flagged or
  replaced. The Impeccable detector hook stays as a named polish-pass step,
  not a hook (already decided — do not re-wire it).
- (d) No Claude-Code-only paths: any remaining `claude -p` CLI invocation,
  Claude-Code-only label, or non-Cursor runtime assumption gets scrubbed
  or explicitly marked as not-a-Cursor-path. The distinction stands: the
  GAN LOOP runs in Cursor as subagents; the upstream skill's `claude -p`
  CLI path does not.
- (e) Windows paths: Git Bash vs PowerShell guidance is consistent (CBM
  install, npm, %LOCALAPPDATA%, repo paths). No macOS/Linux-only command
  is presented as the default for a Windows user.
- (f) Local-plugin loading: the update path (local clone at
  ~/.cursor/plugins/local/<name> + git pull + Developer: Reload Window;
  no symlinks; repo-link copy takes precedence; delta bundles) is stated
  once, consistently.
- (g) Command surface: /orchestrate, /orch-build-mvp, /demo,
  /demo --rebuild, /gan-build — the dispatch rules are coherent (one
  engine per run; /demo never automatic; the narration-key prompt fires
  ONLY when the user asked for a demo video).

## §3 Verification criteria

- Audit #71 (or next number): ZERO blocking, ZERO minor.
- Sweep (next number): CLEAN, weaving-coherence CLEAN for the whole tree
  (§1–§2, all fixes' placements).
- Dry-run (next number): PASS, including a Cursor-readiness leg: a
  checklist the smoke test can execute live, verifying the §2 items that
  CAN be verified statically, and listing the items only the live smoke
  test can decide (agent resolution, pin behavior, hooks firing, /demo
  film) as OWED, not claimed.
- verify24.py: checks for every placement, exit 0.
- Prior verifiers: re-run; fails must be only the frozen post-fix21
  fingerprint + the less-flat-ui diff-hunk pattern + cascades. No
  regressions. Prior verifiers are NOT edited. (Note: a verifier change
  forced by §1(d) is a PARENT decision — the coordinator records it as
  owed in the manifest and does not make it.)
- Banned terms: 0 in the built tree. Counts and pins unchanged unless the
  manifest justifies a change.
- Manifest: fix24/MANIFEST.md, written by a script, with the disposition
  table, the anchor tokens, the open parent adjudications, and the
  dry-run caveat if any check is environment-limited.

## §4 Non-goals

- Do not re-litigate fixes #14–#23 adjudications (slop = flags, trends =
  menu, /demo gates, Casberry bar, APCA informational, template-fonts
  self-host follow-up, THE CORE, the inventory).
- Do not rewrite frozen verifier-asserted texts.
- Do not pre-decide the smoke test's live questions. Make the plugin
  robust + clear, and let the smoke test decide.
- No new skill unless the manifest justifies it. No platform conversion.
- No bundle, no commit, no push.
