---
name: integration
description: Wire a named API, tool, SDK, or hackathon sponsor track into the project. Use when the user says "integrate X", names an API, SDK, tool, or sponsor in the idea or requirements, or asks how to qualify for a sponsor track. Covers finding the docs, checking for an existing skill, wiring auth and client, env vars, verifying with a live call, and putting the integration in the demo path.
---

# Integration

One job: take a named integration from words to a working call in the demo path, as fast as possible, without blocking the build on a missing credential or a broken third-party API.

At the start, read `docs/decision-record.md` for the integrations the record names — fallback if that file does not exist: the raw user prompt plus `docs/scope.md`. The project directory IS the project root — the folder opened in Cursor; no separate directory is created, and all `docs/…` paths are relative to it.

An integration here means any outside system the product depends on: a REST API, an SDK, an MCP server, a sponsor tool, or a hackathon track requirement. The same steps apply whether it is one API or a sponsor prize.

## When to use

- The user says "integrate X", "add X", "wire up X", or "use X for this".
- The original idea or requirements name an API, SDK, tool, or sponsor track. Activate on those mentions without being asked separately: if the idea says "using the Gemini API" or "Best Use of Solana", the integration is part of the build, not a later add-on.
- The user asks how to qualify for a sponsor track or prize.
- The user names a tool the project should talk to (payments, email, maps, auth provider, AI API, database, storage, messaging).

Do NOT use this skill for the project's own auth or database setup (that is `app-scaffold`), or for building an MCP server from scratch (that is `mcp-server-patterns`). If the tool exposes an MCP server, see Step 3 for the MCP route.

## Step 0: Scope check, before any wiring

Before touching code, check the integration fits the hours left. Use `hackathon-scope` for this.

- Name the real job the integration does in this product, in one sentence. "We use X to <real job>" is the test. If the sentence is "we integrated X", there is no real job, and the integration is a bolt-on. Cut it.
- Estimate the hours to a meaningful integration (not a hello-world), with a 30% buffer. If it does not fit, say so and drop it. Do not produce a plan that cannot be finished.
- If it is a sponsor track, score it first (see Sponsor tracks below). A natural integration finished on time beats a valuable prize half-attempted.

## Step 1: Identify the target

Gather four things, in one message if anything is missing:

**Unattended path (first build after grill-me, or a one-prompt removal):** do NOT ask for anything missing — take the target, job, and stack from the grill-me decision record / `docs/scope.md` (the API is named there), proceed with what is known, and stub what is missing per Step 4 (never block, never wait). Missing credentials degrade to the clearly-marked stub in Step 4; a missing target or job is a stated assumption recorded in the run ledger and the final report. The gather-in-one-message below is for a direct, attended invocation only.

1. **The target**: exact name, and a link if the user has one (event page, sponsor page, docs URL).
2. **The job**: what it does in the product, and where it appears in the demo. The integration must appear in the demo path, not in a code branch nobody opens.
3. **Credentials**: what exists already (an API key, an account, a signup) and what is still missing. Never invent a key. List exactly what the user must supply.
4. **The stack**: what the project already uses, so the client matches it (Next.js, Python, and so on).

## Step 2: Docs and existing skill

Do this before writing any integration code.

1. **Check for an existing skill first.** Use `skill-scout` to search for a skill that already covers this integration (a vendor skill, an SDK skill, a sponsor skill). If one exists and is good, use it for the wiring details and skip to Step 3 with its guidance.
2. **Find the current docs.** Use `documentation-lookup` to fetch the official docs and quickstart for this exact tool. Verify the quickstart still matches what the docs say today. Never trust memory for SDK method names, endpoint paths, or auth flows: these change, and the marketing page will not list the gotchas (rate limits, missing SDKs, deprecated endpoints, free tiers that run out mid-demo).
3. **Validate with a tiny proof of concept before wiring it in.** Run the quickstart hello-world end to end. If it works within about 30 minutes, the integration is viable. If it takes longer, needs manual approval, or the free tier cannot cover the demo, plan around that now instead of discovering it at hour 23.

## Step 3: Wire auth and client

Follow the `api-integration` skill for the wiring patterns. Do not re-derive them here.

- **One adapter, one place.** All calls to the outside system go through a single client module (an anti-corruption layer). Business logic calls that module, never raw HTTP endpoints. This is what makes the integration replaceable, testable, and debuggable without rewriting the app.
- **Auth per the provider**: API key, Bearer token, OAuth 2.0 with token refresh, or Basic, exactly as the docs specify. Tokens are stored in env vars or a secret manager, never in code, never logged.
- **Typed client**: a clean wrapper with typed requests and responses, and a small error taxonomy that separates retryable failures (timeouts, 5xx, 429) from permanent ones (bad key, bad request, not found).
- **Retry and rate limits**: exponential backoff with jitter for retryable failures, honour `Retry-After` on 429s, and throttle client-side so the demo does not burn the free tier.
- **Never trust external data.** Validate every response at the adapter boundary (missing fields, wrong types, unexpected formats) before it reaches the rest of the app. Treat API responses with the same suspicion as user input.
- **Every external write must be idempotent or safely retryable.** If retrying a call can create a duplicate (a double charge, a double message), the integration has a critical bug. Use idempotency keys or check-before-write.
- **MCP route**: if the tool exposes an MCP server, prefer it over a hand-rolled client. Use `mcp-server-patterns` for the server setup and wiring, and treat the MCP tools as the adapter.

## Step 4: Env vars, config, and the missing-key fallback

- Put every secret in `.env.local` (gitignored) and document the variable names, with no values, in `.env.example`. If the project already has an env-file convention from `app-scaffold`, follow it.
- Tell the user exactly what to supply, by name: "Set `GEMINI_API_KEY` in `.env.local`. Get it at <link>." Never invent a key, a placeholder key that looks real, or a fake account.
- **Never block the build on a missing credential.** If the key is not available yet, wire a fallback chain so the demo path still works: real key first, then a mock or stub that returns realistic data, clearly marked as a stub. Build the rest of the app against the adapter, and swap in the real key the moment it arrives. Add integrations incrementally as keys land; do not wait for all of them.
- Keep the fallback visible: a stub must never silently pretend to be live data in the demo. Say what is real and what is stubbed.

## Step 5: Verify live

Verify with a real call, not by reading the code and assuming it works.

1. **Smoke first, at zero cost.** Before any paid call, validate the request shape with the cheapest possible operation (a list call, a status check, a tiny input). Fix parameter errors before spending anything.
2. **Then the demo-path call.** Run the exact call the demo will make, with the real data the demo will use. Confirm the response shape, the latency, and the error behaviour.
3. **Claim only what the call proved.** Use `verification-before-completion`: run the call, read the output, then claim it works. If the call fails, use `systematic-debugging` to find the cause. If the build itself breaks after wiring, use the `/build-fix` command.
4. **Check the free tier covers the demo.** Confirm the remaining quota or credits cover the demo runs plus a few retries. If it does not, say so now.

## Step 6: Demo and docs

An integration that never appears in the demo does not count, especially for a sponsor track.

- **Demo moment**: use `hackathon-pitch` to place the integration in the demo storyboard. Name the 10 seconds where the judge sees it working, and plan the demo around that moment. Pre-fill everything, no live typing, no signup on stage.
- **Pitch line**: one sentence, "We use <tool> to <real job it does>". Never "we integrated <tool>".
- **Devpost**: use `devpost-autofiller` for the submission. The tool goes in the "Built with" tags under its exact product name, and the "How we built it" section names what it does, not just that it is there.
- **Safety net for the demo**: if the integration involves live generation or a slow call in a timed slot, pre-render or pre-fetch a hero result the night before and keep it as a fallback that plays if the live call is slow or the venue wifi drops. Live is the wow moment; the fallback is what saves the slot.
- **Sponsor admin**: if it is a sponsor track, flag the submission items before the deadline rush (prize categories entered, GenAI usage disclosure, any sponsor-specific field such as a project number).

## Sponsor tracks

When the integration exists to win a sponsor prize, add this scoring before Step 3. It decides which prizes are worth the hours.

Score each candidate prize 1-5 on four axes:

| Axis | What it measures |
|---|---|
| **Fit** | Does the API solve a real problem in this project, or would it be bolted on? Judges smell bolt-ons instantly. |
| **Effort** | Hours to a meaningful integration (not hello-world), given the team's stack and time left. Score 5 = cheap, 1 = expensive. |
| **Competition** | How many teams will plausibly target this prize? General prizes draw everyone; niche APIs draw a few teams. Score 5 = few rivals. |
| **Reward** | Prize value, including interviews, credits, or swag the team actually cares about. |

Weighted score = `2 * Fit + 2 * Effort + Competition + Reward`. Fit and effort dominate, because a natural integration finished on time beats a valuable prize half-attempted.

Present the table sorted by score, then recommend exactly 1-2 targets and name the prizes to skip and why. For each target, produce a criteria checklist from the prize description (judges literally check these), and map each criterion to how the project satisfies it. If a prize's criteria are not on the event page, search the web for `<sponsor> <event name> prize` and the sponsor's developer docs. Never work from memory for criteria or rubric weights: if a weighted rubric exists, the weights are the strategy, so fetch it.

## UI rule

Any UI the integration touches goes through the plugin's UI skills: use `ui-ux-pro-max` and `less-flat-ui` together for it — except on a full landing/company page, where `design-taste-frontend` leads per hackathon-mode §5. That includes auth screens, connected-account states, loading and error states for the integration, and any surface that shows the integration's data. Do not hand-roll UI for an integration without them.

## Anti-patterns

- **Bolting on a sponsor API at hour 23.** Pick the prize early and build toward its criteria, or do not chase it.
- **A wrapper with no real job.** If the integration does not change what the user can do, it is decoration, and sponsor judges say so out loud.
- **Inventing credentials.** A fake key, a placeholder that looks real, or a hardcoded demo key in code. List what is needed and wait for the real one; build against the stub meanwhile.
- **Trusting the marketing page.** The docs and a live call are the truth. Verify capability before assigning: a provider's feature list may not match its API.
- **Waiting for all credentials before building.** Get one integration working early, then add the rest as keys land.
- **No fallback when the key is missing.** A missing key must degrade to a clearly marked stub, never to a blocked build or a silent fake.
- **Hiding the integration from the demo.** If the judge cannot see where it is used, it does not count.
- **Scattering API calls through business logic.** Every external call goes through the adapter from Step 3. If a second call site appears, it is a bug.

## Attribution

This skill composes the plugin's own skills (`skill-scout`, `documentation-lookup`, `api-integration`, `hackathon-scope`, `verification-before-completion`, `hackathon-pitch`, `devpost-autofiller`, `ui-ux-pro-max`, `less-flat-ui`, `systematic-debugging`, `mcp-server-patterns`, `app-scaffold`) with structure drawn from these public sources:

- `integrations` by Emmraan (github.com/Emmraan/agent-skills, MIT): the end-to-end integration lifecycle, the anti-corruption layer, and the cross-cutting rules (assume the external API will fail, never trust external data, never scatter calls, every write idempotent, concrete recommendations over option catalogs). Adapted and cut down to hackathon scale: the production phases (testing, compliance, vendor management, cost management, observability, framework design, deliverables) were dropped.
- `sponsor-matchmaker` by asrayg (github.com/asrayg/hackathon-agent-skills, MIT): the sponsor prize scoring table and weighted formula, the criteria checklist, the demo moment, the pitch line, the 30% time buffer, and the Built-with tags rule. Adapted into the Sponsor tracks section.
- `sponsor-tool-coverage-for-hackathons` by efenocchi (github.com/efenocchi/aws-hackathon, no license file): the fallback-chain idea, smoke-before-spend, incremental sponsor adds, and the pre-rendered demo safety net. Used as ideas only, rewritten in this skill's own words; no sentences copied.
- `hackathon-idea-validation` by IdkwhatImD0ing (github.com/IdkwhatImD0ing/hackathonstarterkit, no license file): the validate-first idea (tiny proof of concept and a 30-minute hello-world check before wiring an integration in, and checking gotchas like rate limits and free tiers by calling the API). Used as an idea only, rewritten in this skill's own words; no sentences copied.
- `integrations` by whawkinsiv (claude-code-skills): NOT used. The skill does not exist in the actual repo (it appears only in the learn-skills.dev mirror layout), so it was excluded.
