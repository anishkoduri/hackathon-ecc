# Fix #30 (SPEC) — Model routing: Grok 4.7 Extra High orchestrator pin

**RE-SCOPE (Nov 16, 2026, ~7:30 PM CT — supersedes the Carbon decision below; original kept as history):** the brain is now **Grok 4.7 on Extra High in Cursor, on the pool** — Anish chose this over OpenCode/Hydrogen because Cursor is the best value per token. Carbon is OUT, Grok-via-OpenRouter brain is OUT, Hydrogen brain is OUT, the $5 Google Cloud prepay is OUT, no Google API key in Cursor. The drones stay DeepSeek V3.2 + Qwen3 Coder 30B via OpenRouter, added to Cursor through Override OpenAI Base URL at `https://openrouter.ai/api/v1/cursor` (NOT plain `/api/v1`). **New #30 scope: change the orchestrator pin `grok-4.7-high` → `grok-4.7-extra-high` everywhere in the built tree (49 ID mentions + 22 prose "Grok 4.7 High" mentions in the fix29 tree — recount Nov 16, 2026; the SPEC's earlier "585" was the fix28-tree whole-tree count) + update verifier pin assertions (verify30.py, exact counts). Build-time only: staged sources and build.sh inline keep the old pin by design (fix16/24/29 anchor on it).** Drone routing stays #29's best-effort — the full drone-factory (custom subagents, CLI dispatch, OpenRouter setup skill) goes in the factory copy per `~/workspace/hackathon-plugin/FACTORY_CURSOR_PLAN.md`, NOT in #30.** Live test for #30: orchestrator on one reasoning-heavy task + one repo-scale coding task, reporting which model ran; pass = Extra High ran the parent.

**Status:** in implementation, Nov 16, 2026 (re-scoped; see note at top). **Depends on fix #29 (adaptability)** — starts after #29 lands. Do NOT start while #28 or #29 runs (two agents must never edit the plugin tree at once).

## Decision (Anish, Nov 16, 2026) — SUPERSEDED, kept as history (see RE-SCOPE note at top)

- **Orchestrator / brain:** Gemini 4 Carbon, model ID `gemini-4-carbon`. $2 in / $10 out per 1M tokens through Nov 30, 2026, then $4/$20. Paid-tier only, GA Nov 10, 2026. Quality floor: only models stronger/smarter than Grok 4.7 High do thinking work.
- **Drone A (reasoning):** DeepSeek V3.2, OpenRouter ID `deepseek/deepseek-v3.2`, ~$0.21 in / $0.31 out per 1M, 164K context, Coding Index 44.2. For: general intelligence, heavy reasoning, complex tool-use chains, structured data.
- **Drone B (coding):** Qwen3 Coder 30B A3B Instruct, OpenRouter ID `qwen/qwen3-coder-30b-a3b-instruct`, $0.15 in / $0.60 out per 1M, 262K context. For: local dev, agentic coding, repository-level context, speed.
- **Tiebreaker:** reasoning-heavy goes DeepSeek; mechanical or repo-scale goes Qwen. When a task is both, the orchestrator judges which dominates and says so in one line.
- **Drones are exempt from the quality floor** (mechanical work only). "Local dev" means coding work on the local repo via OpenRouter, NOT locally hosted Ollama Qwen (that would need the public-tunnel setup).

## Prerequisites (outside this fix) — SUPERSEDED by the re-scope (Nov 16, 2026)

The $5 prepay and the Google API key are OUT — no Google key in Cursor, no Carbon. The OpenRouter drone setup (DeepSeek/Qwen via Override OpenAI Base URL `https://openrouter.ai/api/v1/cursor`) still stands as the drone path, but it lives in the factory copy per FACTORY_CURSOR_PLAN.md, not in #30. Original kept below as history.

- **$5 prepay billing** on Google Cloud billing account `01D7AE-3C4939-AC6FAC`, else the Gemini API key cannot bill (Gemini API is excluded from the $300 Welcome credit for his Nov 2026 account). Needs Anish's go-ahead; do it via a browser task on his account.
- **Cursor settings on Anish's Windows machine:** Google API key in Settings → Models, pick/add `gemini-4-carbon`; OpenRouter custom models `deepseek/deepseek-v3.2` and `qwen/qwen3-coder-30b-a3b-instruct` at base URL `https://openrouter.ai/api/v1` with his OpenRouter key; pick Carbon in the chat picker.

## Scope

- Change the orchestrator pin `grok-4.7-high` → `grok-4.7-extra-high` everywhere in the built tree (49 ID + 22 prose; build-time only via fix30.py, last in build order after fix29.py — staged sources and build.sh inline keep the old pin by design, fix16/24/29 anchors). Fast-worker pin `cursor-grok-4.6-high-fast` unchanged (70). No drone routing added.
- Update the verifier's pin assertions (the Grok-pin checks from verify29) to the new pins; add a `verify30.py` following the fix #27/#28/#29 pattern (exact counts: extra-high x49, old pin x0, prose x22/x0, fast-worker x70; check 9b unchanged — no deepseek/qwen slugs).
- Do NOT change: the debloat from #28, the design package, grill-me, the alwaysApply rules, or any behavior beyond model routing.
- Constraints: author Anish Koduri <akoduri05@gmail.com> only, NO `Co-authored-by: Cursor` trailer, no AI tool as contributor/author; build.sh is the source of truth; staged sources only; never re-run fix11/fix11-stage.py; fix dirs stay; do NOT push (create a verified git bundle for the Windows pull).

## Verification

- Audit loop (at least 2 rounds) + sweep + dry-run, with HONEST verdicts: record NOT MET as written if the final audit or sweep carries a minor fixed post-hoc without a re-audit/re-sweep, per the fix #27 convention.
- **Live test** (Anish runs in Cursor after the fix lands): a prompt that gives the orchestrator one reasoning-heavy task and one repo-scale coding task, and asks it to report which model ran each. Pass = Grok 4.7 Extra High ran the parent (orchestrator) on both tasks, visible in the model indicator. The fix coordinator writes the exact prompt (fix30/live-test-prompt.md).
- Cost sanity: the fix must not route thinking work to a drone and must not route drone work to the orchestrator — in this fix that means the orchestrator pin is Extra High and no drone routing is added.

## Open items

- Whether Cursor honors per-subagent model choice (the live test decides).
- ~~Carbon's standing vs Grok 4.7 High on Anish's actual work (unverified; the floor assumes Carbon clears it as a frontier model).~~ **SUPERSEDED — Carbon is OUT (see RE-SCOPE note at top); kept as history.**
- Kimi K2 ($0.60/$2.50) was evaluated and skipped: good at tool loops but 4x the price of the chosen drones with a lower coding index than DeepSeek.
- **Cursor Router / Auto evaluated Nov 16, 2026 and REJECTED as the routing mechanism** (verified against Cursor docs + forum): (a) the real Router (Cost/Balance/Intelligence) is Teams/Enterprise only — individual Pro gets legacy Cost Auto only; (b) the routing pool is Cursor's own models only (GPT-5.5, Claude Opus 5, Grok 4.5, Claude Fable 5) — BYOK models (Carbon via Google key, DeepSeek/Qwen via OpenRouter) are never in the pool; (c) Auto does not control subagents — it applies to the parent agent only, subagents inherit or need frontmatter pins (the already-broken path); (d) Pro Auto bills from the included usage pool, the thing that hit 2% on Nov 15 — it does not solve cost; (e) the router optimizes for cheapest-comparable, which conflicts with the quality floor (pool includes Grok 4.5, below the Grok 4.7 High floor); (f) Cursor's own SDK docs: the underlying model can change between requests. Auto is fine for small everyday edits; it cannot run the factory.
