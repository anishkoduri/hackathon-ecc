# hackathon-ecc

A Cursor plugin that is the hackathon version of ECC: the ECC
Developer profile (minus 6 guide skills, 2 agents, and 4 commands —
see below) plus hackathon workflow skills, UI skills, and the
`/demo` and `/orchestrate` commands. Install it in a hackathon project and
every chat in that project uses it.

## What is inside

- **ECC Developer profile as shipped** — 144 skills, 69 agents, 121 rules, 94 commands (stock Developer install is 140/71/121/98; +10 backfilled ECC skills, −6 guide skills, −2 agents, −4 commands — see build.sh), hooks (15 events covering session lifecycle, shell/file/MCP handling, secret guards, subagent logging, and a stop hook that formats, typechecks, and persists state), and the chrome-devtools and playwright MCP servers. ECC process applies in full: plan first, TDD, code review
  while building. With the hackathon additions below, the plugin ships
  72 skills, 45 agents, 48 rules, and 55 commands in total (42 agents as-shipped + 3 staged orchestrate agents; 46 rules as-shipped + 2 new rules — `hackathon-mode`, `ponytail`; skill and command totals per build.sh STEP 5 counts).
  Install profiles: the `hackathon` module (those 25 skills) is included in the `developer` and `full` profiles; `minimal` and `core` do not include it.
- **Grill-me first** — after your first hackathon project prompt, the
  plugin asks one question at a time until every decision is recorded, and
  that decision record steers scoping, expansion, and orchestration. Say
  "skip the grilling" or "just build it" to skip it.
- **UI skills, used together** — `ui-ux-pro-max` (design direction) +
  `less-flat-ui` (texture layer) on non-landing UI work (dense dashboards, forms, and tables stay flat). Exception: `less-flat-ui`'s texture layer also applies inside a `design-taste-frontend` landing-page build, on surfaces where the Taste page system leaves a surface unstyled (never over its hero, dealt moments, or shader scenes — see `rules/hackathon-mode.mdc` §5). Taste
  (`design-taste-frontend`) leads full company/landing-page builds.
  `polish-pass` fixes existing UI without restyling. Hallmark's 50-theme catalog supplies the theme vocabulary Taste deals from, and its gate checker (`sloplint`) + fresh-context reviewer run at Verify; Impeccable's 62-rule detector + craft floor are wired into `polish-pass` (its direction lenses were left out on purpose — polish never restyles).
- **Hackathon workflow** — `hackathon-scope` (MVP scoping), `feature-expansion`
  (brainstorm, plan, and implement the next features), `integration` (wire a chosen API/SDK), `track-picker`, `mobile-ship`, `deploy-fast`, `app-scaffold`,
  `api-integration`, `readme-writer`, `ai-feature-spec`, `hackathon-pitch`,
  `devpost-autofiller`, plus the marketplace skills (systematic-debugging,
  verification-before-completion).
- **Codebase memory** — `codebase-memory` was cut in fix #27 and is not shipped. Explore unfamiliar code with grep-and-read and the `ecc-code-explorer` agent instead: find where a feature lives, trace callers/callees, hunt dead code, and run impact analysis before a change.
- **Fix #31 design libraries (Nov 17, 2026)** — GetLayers (free set only), GSAP, React Bits, and Hairline illustrations added to the palette-first inventory. Skills are now 72. (`GETLAYERS_F31` `GSAP_F31` `REACTBITS_F31` `HAIRLINE_F31`)
- **Fix #28 bloat cut (Nov 16, 2026)** — 75 cut-language rules, the stale install-manifest paths, and 135 dead scripts removed. Rules are now 48. (`CUTRULES_F28` `MANIFEST28_F28` `DEADSCRIPTS_F28` `README48_F28`)
- **Orchestration** — `/orchestrate` runs a tiered scout / fast-worker /
  deep-reasoner team; on high-stakes work (high blast radius and hard to verify) two independent deep-reasoner passes verify in parallel, and a disagreement stops the run.
  Single-feature, single-bug, single-change, and single-refactor work belongs to the `/orch-*` pipelines; invoke `orchestrate` only for general delegation or work spanning several pieces at once. Trivial one-step work (a typo fix, a one-line change) can be done in the main context.

## How this compares

**vs stock ECC (Developer):** The edge is hackathon-specific: grill-me-first decision capture, MVP scoping, a deploy runbook, the UI stack, the `/demo` video pipeline, the `/orchestrate` team, Playwright MCP and the audit deferral that stops security gates blocking a feature mid-build. The risk is that the deferral means security issues surface only at the end, when there is little time left to fix them; the plugin is also a frozen ECC snapshot; a rebuild re-clones upstream when /tmp is wiped, so rebuilds are not frozen, 72 skills widen the routing surface, and the deferral relies on model judgment rather than enforcement.

**vs the earlier curated plugin:** The edge is full ECC process — TDD, planning, code review, orchestration, and verification — so the output is more likely to actually work, and `/demo` plus the UI skills raise the presentation ceiling. The risk is weight: 56 MB and 72 skills against a minimal set means heavier context load, slower startup, and more misrouting surface, while planning, TDD, and review overhead tax hackathon time and grill-me adds an interrogation round before any building starts.

**vs plain Cursor:** The edge is structured process — 72 skills, 45 agents, 55 commands, deploy/demo/orchestration workflows, and MCP servers — where plain Cursor has none of that built in. The risk is that the plugin steers every chat through `alwaysApply` rules, so a bad routing decision can waste more time than a blank slate would; installation is manual with no official Cursor Marketplace listing, updates follow the Updating section below (git pull for a local clone, rebuild + re-copy for a copy install), and 56 MB is loaded into a project that may only need a tenth of it.

## Commands (highlights — 3 of 55)

- `/demo` — generate a narrated product demo video, under 2:10, of the app
  (films the real app with Playwright; rebuilds in ~2 minutes after a
  frontend change; opt-in montage and explainer modes via OpenMontage). `/demo <path>`, `/demo --rebuild`, `/demo --script`,
  `/demo --render`.
- `/orchestrate` — run the tiered orchestration team on a task.
- `/build-fix` — fix the build (ECC).

## Audit deferral

Security tests and audits (`verification-loop`, `production-audit`, and `delivery-gate`) run ONLY at the
very end of the project or when you explicitly ask for them. They never gate
a feature mid-build (stock ECC rules/commands such as `/quality-gate` and the `*-build`/`*-test` commands still reference them; the deferral wins per `rules/hackathon-mode.mdc` §3–§4).

`security-review` is a seventh security skill that is NOT deferred — it fires mid-build on auth, secrets, and endpoints.

## Prerequisites

- **Node.js** (for the Playwright MCP server and the `/demo` video
  template). The plugin adds a `playwright` MCP server (`npx -y
  @playwright/mcp@0.0.85`) alongside `chrome-devtools`; on first use it
  downloads the Playwright browser. The `/demo` skill also needs a MiniMax
  key for good narration (or record the narration yourself).
- **Taste** needs Node 22+ and Chrome/Edge/Chromium for its finish gate (run the gate explicitly — it does not auto-run on stop in Cursor).
- **Before the first build — Grok 4.7 Extra High in the model picker:** select Grok 4.7 Extra High in Cursor's model picker before the first build; see the picker note in `skills/orchestrate/SKILL.md` step 4. Task agents pin to Grok 4.6 High Fast (`cursor-grok-4.6-high-fast`); the orchestrator and the design/implementation roles pin to Grok 4.7 Extra High (`grok-4.7-extra-high`).
- The plugin's Node scripts (`/harness-audit`, the
  `/epic-*` commands, `validate-skills.js`) ship with their dependencies
  vendored in `node_modules/` (~4.9 MB after pruning unused sql.js builds);
  no install step is needed.

## Install

1. Push the `hackathon-plugin/` directory (the repo root — the parent of `hackathon-ecc/`) to GitHub first — a public repo is recommended (simplest), and its root
   must contain `.cursor-plugin/marketplace.json`. A private repo can also work if Cursor can read it (via the Cursor GitHub App, or **Serve marketplace from Cursor** under Marketplace Settings, which keeps a synced copy Cursor serves). (Do NOT push `hackathon-ecc/` alone: its root contains only `.cursor-plugin/plugin.json`, not the marketplace manifest, and the import will fail.) Then in Cursor:
   **Dashboard → Plugins & MCPs → Team Marketplaces → Add Marketplace → Import from Repo**, paste the repo
   URL (for example `https://github.com/<you>/hackathon-plugin`), then add and review the plugins using **Add to Marketplace**.
   Under **Marketplace Settings**, set **Marketplace Access**, optionally enable **Auto Refresh**, then save. Only then find **`hackathon-ecc`** in **Customize** and install it, choosing
   **project scope** (in a hackathon project) or **user scope**.
   Then restart Cursor or run **Developer: Reload Window** and start a
   new chat. (Team marketplaces require a Teams or Enterprise plan — on a solo free plan, use step 2, the local install, instead.)
2. Or test it locally: clone the repo directly into `~/.cursor/plugins/local/hackathon-ecc` (clone it — do not symlink it in from elsewhere, and do not copy it: a plain copy has no `.git`, so it cannot be updated with `git pull` — see Updating below), then restart Cursor or run **Developer: Reload
   Window**, and open **Customize** to confirm the plugin's rules,
   skills, agents, commands, and MCP servers appear.

## Updating

This is the single authoritative update path — every other mention of updating in the plugin points here.

- **Local clone (the normal install):** the plugin lives as a git clone at `~/.cursor/plugins/local/hackathon-ecc`. Update it with `git pull` inside that directory, then run **Developer: Reload Window** in Cursor. No rebuild, no re-copy.
- **Copy install:** if the plugin dir is a plain copy (no `.git` inside it), `git pull` cannot work there — update by rebuilding from the source repo (`bash ~/workspace/hackathon-plugin/build.sh`) and re-copying the rebuilt `hackathon-ecc/` directory over the installed one, then **Developer: Reload Window**.
- **Delta bundles:** for an incremental update without a full re-clone, the maintainer can ship a bundle (`git bundle create update.bundle main ^<prev-commit>`); apply it with `git fetch <bundle> main` + `git merge --ff-only FETCH_HEAD` (the positive side must be a branch name, not a bare SHA), then **Developer: Reload Window**.
- **Never symlink** a plugin directory in from elsewhere — Cursor skips symlinks pointing outside `~/.cursor/plugins/local/`. If a repo-link copy of the plugin is also installed, remove it first: a repo-link copy takes precedence over the local one.

## Rebuild

`bash ~/workspace/hackathon-plugin/build.sh` rebuilds the plugin from the
ECC installer and the staged additions in `~/workspace/hackathon-plugin/`.
