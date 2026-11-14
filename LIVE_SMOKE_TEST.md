# Live Smoke Test — hackathon-ecc plugin in Cursor

Run this in your own Cursor install to verify the plugin works at runtime. Static audits cannot prove routing, agent resolution, or hooks — only a live test can. Work through the steps in order and check each box. If a step fails, note exactly what happened (what you typed, what Cursor did, any error text) and stop there — do not work around it.

## Prerequisites

- [ ] Cursor installed and up to date (check Cursor → About / Settings → About for the version; note it here: ____).
- [ ] Node.js installed (`node --version` works in a terminal).
- [ ] The plugin repo cloned locally at `~/workspace/hackathon-plugin/` (or wherever you keep it), with the `hackathon-ecc/` directory present.
- [ ] No other hackathon/ECC plugin installed in this Cursor profile (to avoid routing confusion).

## 1. Install the plugin

- [ ] Open Cursor → **Customize** (sidebar) → **Plugins**.
- [ ] Install the plugin from the local directory (use the local-folder / "Add plugin" option if shown; otherwise push the repo to GitHub first and install via **Dashboard → Plugins & MCPs → Team Marketplaces → Add Marketplace → Import from Repo** with the repo URL — team marketplaces need a Teams or Enterprise plan).
- [ ] Confirm the plugin appears in the installed list as **hackathon-ecc 1.0.0**.
- [ ] Confirm the plugin's skills, rules, agents, and commands are listed under its details (counts should read 166 skills, 72 agents, 123 rules, 87 commands).

**If install fails:** note the exact error. A missing or malformed `.cursor-plugin/plugin.json` is the usual cause.

## 2. Create a test hackathon project

- [ ] Create a new empty folder (e.g. `~/smoke-test-hackathon/`) and open it in Cursor.
- [ ] Confirm the plugin is active in this project (its rules/skills should be available — you can check by typing `/` in chat and seeing the plugin's commands, e.g. `/demo`, `/orchestrate`).

## 3. Run grill-me

- [ ] In a new chat, type a first hackathon project prompt, e.g. "Build a web app that lets users track their daily water intake with a leaderboard."
- [ ] Confirm **grill-me runs FIRST**, before any scoping or building — it should ask one question at a time and record your decisions.
- [ ] Answer its questions. Confirm it produces a decision record.
- [ ] Confirm you can skip it by typing "skip the grilling" or "just build it" (test this in a second chat).

**Pass criteria:** grill-me asks questions one at a time, records decisions, and does not start building before the grilling is done (unless you skip it).

## 4. Build a small feature via orchestrate

- [ ] After grill-me, ask Cursor to build a small feature (e.g. "Add a water-intake form with a daily total").
- [ ] Confirm **orchestrate** is used (tiered delegation: scout → fast-worker → deep-reasoner), OR confirm Cursor routes to the right skill and says why.
- [ ] Confirm the feature is built and the code is coherent (it runs, or at least has no obvious syntax errors).

**Pass criteria:** the feature is built, and the routing (orchestrate vs direct) is sensible and explained.

## 5. Confirm routing picks the right skills

Test each of these prompts in a fresh chat and note which skill Cursor says it is using (or which skill's behavior you observe):

| Prompt | Expected skill |
|---|---|
| "Help me scope this to fit a 24-hour hackathon" | hackathon-scope |
| "Deploy this so I can demo it" | deploy-fast |
| "Add a weather API to the app" | api-integration |
| "Build a landing page for this app" | design-taste-frontend (Taste) |
| "This dashboard looks generic, improve it" | ui-ux-pro-max |
| "Make this UI feel less flat" | less-flat-ui |
| "Fix the spacing on this existing page without restyling it" | polish-pass |
| "Make a demo video of the app" | pitch-deck-video (`/demo`) |
| "Add a new feature to the app" | feature-expansion |

- [ ] For each prompt, record the skill Cursor actually used. Flag any prompt where it picked the wrong skill or a different skill than expected.

**Pass criteria:** at least 7 of 9 route to the expected skill. If fewer, the routing descriptions need work.

## 6. Agent-resolution question (D10) — the key open item

Does Cursor resolve agents by **frontmatter `name:`** or by **filename**?

- [ ] In a chat, ask Cursor to use the `code-reviewer` agent (the frontmatter short name) for a code review.
- [ ] In another chat, ask Cursor to use the `ecc-code-reviewer` agent (the filename, `agents/ecc-code-reviewer.md`).
- [ ] Note which form Cursor accepts / which one it says it cannot find.
- [ ] Check the `deep-reasoner` agent: ask for a reasoning-heavy task and see if the agent that runs reports itself as `deep-reasoner` with model `grok-4.7-high`.

**Record the answer here:** Cursor resolves agents by ____________________ (frontmatter name / filename / both / neither — it ignored the name).

This decides whether the `agents/<name>.md` path fixes and the frontmatter-name normalization are correct, or whether the agent files need renaming.

## 7. Agent `model:` slug-form pins

The agents pin models with slug-form pins (e.g. `model: grok-4.7-high`, `model: cursor-grok-4.6-high-fast`).

- [ ] Ask for a reasoning-heavy task (should use deep-reasoner → `grok-4.7-high`).
- [ ] Ask for a fast task (should use fast-worker → `cursor-grok-4.6-high-fast`).
- [ ] Note whether Cursor honors the model pin, ignores it, or errors on the pin.

**Record:** Cursor ____________________ (honors the model pin / ignores it / errors on the pin).

If Cursor errors on or ignores the slug-form pin, the `model:` lines need to be rewritten or removed.

## 8. Hooks fire

- [ ] Trigger a `sessionStart` (open a new chat / restart Cursor) — check whether the session-start hook runs (it sets the Cursor data root and loads previous context; look for any visible effect or log).
- [ ] Edit a `.js`/`.ts` file and save — check whether the `afterFileEdit` hook runs (it warns on `console.log` and runs the frontend design-quality reminder).
- [ ] Run a shell command in the chat — check whether the `beforeShellExecution` / `afterShellExecution` hooks run.
- [ ] Read a sensitive file (e.g. a `.env` file) — check whether the `beforeReadFile` hook warns you.

**Pass criteria:** at least the `afterFileEdit` and `beforeShellExecution` hooks visibly fire. If no hooks fire at all, the `hooks/hooks.json` format or the `node hooks/...` command paths are wrong.

## 9. Deferred audit skills stay deferred

- [ ] During a normal build (steps 3–4), confirm NONE of the 6 audit skills run on their own: production-audit, delivery-gate, codehealth-mcp, verification-loop, santa-method, security-scan.
- [ ] At the end of the project, explicitly ask for one (e.g. "run the verification loop") and confirm it runs.
- [ ] Confirm `security-review` (the mid-build checklist) DOES run during the build when you add auth/input handling — it is NOT deferred.

**Pass criteria:** no audit skill runs mid-build unprompted; each runs when explicitly asked at the end.

## 10. MCP servers

- [ ] Confirm the `chrome-devtools` MCP server is available (ask Cursor to use the browser / open a page).
- [ ] Confirm the `playwright` MCP server is available (ask Cursor to drive a browser with Playwright).
- [ ] If either fails, note the error (it may need `npx` / Node on the PATH, or the package may need installing).

## 11. Runtime items that static audit cannot verify

- [ ] **Plugin root resolution:** the scripts resolve the plugin root via the `ECC_PLUGIN_ROOT` env var, falling back to a path relative to the script. Confirm the hooks work (step 8) — if they do, the fallback is working. If they fail with a "cannot find" error, the root resolution is the cause.
- [ ] **`/demo`:** run `/demo` on the test app and confirm it produces a demo video (or a clear error telling you what is missing, e.g. Playwright browsers or a TTS voice).

## 12. The 6 fixed skills load (after the Audit #2 YAML fix)

Audit #2 found 6 skills with invalid YAML frontmatter (their `description:` contained a literal `: `, which breaks YAML parsing). After the fix is applied and the plugin is rebuilt:

- [ ] Confirm these 6 skills load and are routable: codehealth-mcp, delivery-gate, production-audit, security-review, security-scan, verification-loop.
- [ ] Ask Cursor to describe one of them (e.g. "what does the verification-loop skill do?") and confirm it answers from the skill, not from a guess.

## 13. Hallmark + Impeccable additions (fix program #11 — Windows)

- [ ] **Impeccable detector first run:** in a test project, run `npx impeccable@4.8.0 detect <a UI source dir>` from Git Bash (and once from PowerShell). It should download the engine binary once (~20 MB, SHA-verified) and report findings. Note whether the download works, where the binary lands (`%USERPROFILE%\.impeccable\bin\0.1.18\`), and any error.
- [ ] **Impeccable Cursor hook on Windows — EXPECTED UNKNOWN:** the shipped `.cursor/hooks.json` detector hook is POSIX-only (`[ ! -f … ]` shell syntax) and Cursor runs hook commands through PowerShell on Windows, so it likely does NOT fire. Confirm whether it fires or not; either way, record the answer here — the plugin does NOT rely on it (the detector runs as a named step in polish-pass instead).
- [ ] **Hallmark render tier:** on a Taste landing build, confirm `sloplint --render` runs: it needs `puppeteer-core@25.17.0` (`npm i -g puppeteer-core@25.17.0` if missing) + Chrome. If Chrome is not found, set `CHROME_PATH` to the Chrome install. Note whether the render tier ran or fell back to static-only.
- [ ] **Hallmark theme deal:** ask Cursor to build a landing page and confirm the deal picks a theme from the 50-theme catalog (theme name + material in the report) rather than inventing a direction.

## 14. Grok pins hold — 4.7 High design, 4.6 High Fast task tier (fix programs #13, #16)

- [ ] **Picker selection:** before the first build, select **Grok 4.7 High** in Cursor's model picker. The plugin pins its design role to `grok-4.7-high` (slug form only — no bracket syntax), but Cursor's subagent model allowlist is coupled to the picker dropdown, so the pin can silently fall back to another model if Grok 4.7 High is not selected.
- [ ] **Design role runs on Grok 4.7 High:** on a build with UI work, confirm the design lead (the agent/skill doing design direction — Taste theme deal, ui-ux-pro-max direction, polish-pass) actually runs on Grok 4.7 High, not on another model. Note what it ran on and any error or fallback.
- [ ] **Fast tier runs on Grok 4.6 High Fast:** on a mechanical task, confirm the fast-worker / scout actually runs on Grok 4.6 High Fast (`cursor-grok-4.6-high-fast` — the `cursor-` prefix is part of the pin), not on another model. Note what it ran on and any error or fallback.
- [ ] **"High" cost note:** "High" is a reasoning effort, not a price tier — higher effort generates more reasoning tokens and burns the Cursor weekly usage pool faster. Note whether usage feels materially higher; this does not change the model choice.

**Record the answer here:** the design role ran on ____________________ (Grok 4.7 High / another model — which one / fell back silently). The fast tier ran on ____________________ (Grok 4.6 High Fast / another model — which one / fell back silently).

## 15. Fix #24 Cursor-readiness — live-only items static audit cannot settle

Fix #24 made the plugin robust to either outcome on each item below; this step records which outcome is real. Cross-references: step 6 (agent resolution), step 8 (hooks fire), step 11 (runtime items), step 14 (pins).

- [ ] **D-6 Stop / SessionStart events exist?** `hooks.json` registers both `stop` and `sessionStart`, but four hook headers say "Cursor has no Stop/SessionStart hook event". Run a build to a stop and confirm: does the Stop hook fire (desktop-notify, ecc-statusline)? Does anything fire on session start? Record which side is right — do not pick one from the docs alone.
- [ ] **C-5 Stop-hook timeout unit:** `hooks.json` sets `timeout: 300` on the `stop` event with the unit unstated. Confirm whether 300 means seconds or milliseconds in practice (does a slow stop hook get cut off, and after how long?).
- [ ] **C-6 Hook runtime shape:** confirm hooks run with cwd = the plugin root, `node` on PATH, and the registered event names (`sessionStart`, `beforeShellExecution`, `afterFileEdit`, `stop`, …) matching what Cursor actually emits.
- [ ] **D-9 `.ecc/settings.json` pickup:** confirm whether Cursor picks up the plugin's `.ecc/settings.json` at all (if not, note it — the file is then documentation only).
- [ ] **E-7 Taste gate hook without Git Bash:** the Taste gate Stop hook is one POSIX `sh` line (Git Bash on Windows). If Git Bash is NOT installed, does the hook fire, fail silently, or error? Record the behavior.
- [ ] **C-1 block-no-verify on PowerShell/cmd:** run each of these as a shell command and record blocked vs allowed: `powershell -Command "git commit --no-verify"`, `pwsh -c "git commit --no-verify"`, `cmd /c git commit --no-verify`, a `-EncodedCommand` base64 bypass attempt, a `-File` script bypass attempt, and a clean `powershell -Command "echo hi"` (must be allowed). Any bypass that gets through is a FAIL — report the exact command.
- [ ] **General-subagent fallback pin:** dispatch a task to a `general subagent` (the fallback where no named agent resolves — see step 6) and confirm which model it runs on, and whether the Grok 4.7 High picker selection (step 14) holds for it.

**Record the answers here:** Stop/SessionStart fire: ____________________. Timeout 300 = ____________________. Hook cwd/node/events: ____________________. `.ecc/settings.json` picked up: yes / no. Gate hook without Git Bash: ____________________. C-1 PowerShell cases: ____________________. General-subagent model: ____________________.

## Results

- Date run: _______________
- Cursor version: _______________
- Overall: PASS / FAIL (circle one)
- Steps that failed (list): _______________
- Agent resolution answer (step 6): _______________
- Model pin answer (step 7): _______________
- Notes: _______________
