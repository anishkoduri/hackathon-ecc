---
name: deploy-fast
description: CLI deployment runbook for hackathons covering Vercel (Next.js), Railway (FastAPI/Node workers), Supabase and Clerk, with env vars, CORS, common failures and the pre-pitch checklist. Use when deploying or debugging a deploy during a hackathon.
---

# Deployment Runbook: CLI Only

<!-- markdownlint-disable MD013 -->

> From "works locally" to "judges can see it". Adapted from [maxi-cmyk/help-me-papi](https://github.com/maxi-cmyk/help-me-papi) `hackathons/skills/deployment.md`, with commands **re-verified against official docs on 2026-09-21**. Corrections are marked ✏️.

---

> **First deploy ever?** The beginner click-through (website only, no CLI): import the GitHub repo in Vercel → add env vars → Deploy. Every push to `main` then redeploys; **changing an env var needs a manual redeploy**. Errors outside deployment: see `systematic-debugging`.

## Golden rules

1. **Deploy in the first hour.** Push a hello world, get the URL, and confirm it works.
2. **Set env vars before deploying.** A build with missing env vars can break silently.
3. **Build locally first.** `npm run build` catches errors before the deploy does.
4. **Demo from the production URL**, not localhost. Keep localhost running only as a fallback.
5. **One person owns deployment**: logins, env vars, rollback.

---

## Which host?

```text
Next.js app (UI + API routes)?  → Vercel (one repo, one deploy, no CORS)
Python / heavy ML / long workers? → Railway for the API + worker, Vercel for the frontend
Something else                    → whatever the sponsor provides or the team knows
```

**One repo, one deployment** where possible. A split frontend/backend deploy means CORS, two sets of env vars and two things that can break.

---

## Frontend: Vercel (Next.js)

```bash
npm i -g vercel
vercel login
vercel                 # first deploy: scope, project name, framework detection
vercel --prod          # promote to the production URL
vercel link            # link a local folder to an existing project
```

Env vars:

```bash
vercel env add NEXT_PUBLIC_SUPABASE_URL production
vercel env add CLERK_SECRET_KEY production
vercel env pull .env.local        # pull them down for local dev
```

✏️ **Function timeouts:** with Fluid compute (the default for new projects), Hobby functions get **300 s default and maximum** and 2 GB memory. The request/response body limit is **4.5 MB**. The old "10 s on the free plan" figure is outdated ([Vercel limits](https://vercel.com/docs/functions/limitations), updated 2026-08-24).

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Works locally, blank in production | Missing env vars | Dashboard → Settings → Environment Variables, then redeploy |
| Proxy/middleware crashes | Node-only import in the Edge runtime | Move the logic out of proxy, or use the Node runtime |
| Stale deploy | Build cache | Redeploy with the cache off |
| `FUNCTION_INVOCATION_TIMEOUT` (504) | Long LLM or processing call | Stream the response; move heavy work to a Railway worker |
| `413 FUNCTION_PAYLOAD_TOO_LARGE` | Upload over 4.5 MB | Upload straight to Supabase Storage with a signed URL |
| OAuth redirect broken | Only localhost is configured | Add the production URL to the OAuth provider |

---

## Backend / workers: Railway (FastAPI, Node, Celery)

✏️ Commands verified against the [Railway CLI reference](https://docs.railway.com/reference/cli-api):

```bash
npm i -g @railway/cli
railway login
railway init                       # new project, linked to the current folder
railway link                       # or link to an existing project
railway up                         # deploy the current directory (add --detach to skip log streaming)
railway add --database postgres    # ✏️ was: --plugin postgres
railway variable set OPENAI_API_KEY=sk-...                          # ✏️ was: railway variables set
railway variable set FRONTEND_ORIGIN=https://your-app.vercel.app
railway domain                     # generate a public Railway domain
railway logs                       # stream logs (--build for build logs, -n 100 for the last 100 lines)
```

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Build fails | Manifest not at the root | Put `requirements.txt` or `package.json` in the root, or set the root directory |
| Worker won't start | Wrong start command | Settings → Deploy → Start Command, or `railway.toml` |
| DB connection refused | Hard-coded connection string | Use the `${{Postgres.DATABASE_URL}}` reference variable |
| Out of memory | Worker too heavy | One job per worker; restart the worker after heavy ML jobs |

**Expose localhost** (a webhook callback, or a demo from your laptop): use [cloudflared](https://github.com/cloudflare/cloudflared) quick tunnels (no account needed) or [frp](https://github.com/fatedier/frp). **localtunnel is stale**.

**CORS** (split deploys only): the backend allows **only** the Vercel origin (`FRONTEND_ORIGIN`), never `*` with credentials.

---

## Database: Supabase

```bash
npm i -g supabase            # or: npx supabase ...
supabase login
supabase link --project-ref <ref>
supabase db push                                   # apply local migrations to remote
supabase db push --include-seed                    # ✏️ also run supabase/seed.sql on the remote
supabase db reset                                  # local: re-run migrations + seed.sql
supabase gen types typescript --linked > types/database.ts
```

✏️ **There is no `supabase db seed` command.** `seed.sql` runs on `db reset` or `db push --include-seed`. `supabase seed buckets` only seeds Storage buckets ([Supabase CLI](https://supabase.com/docs/reference/cli/supabase-seed)).

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| RLS blocks everything | No policy for that operation | Add one policy per operation |
| Connection refused from serverless | Direct connection used | Use the pooled connection string (Supavisor) |
| Migration fails | Drift from dashboard edits | `supabase db diff` before pushing |
| Project unreachable on judging day | **Free projects pause after 7 days idle** | Wake it up the day before |

---

## Other hosts (Deepen run, 2026-09-22)

| Host | Best for | Free tier | Sleep / cold start | Gotcha |
| --- | --- | --- | --- | --- |
| **Render** | Python/Node web API from Git | 750 instance-hours/mo | **Sleeps after 15 min idle; ~1 min to wake** | Free Postgres **deleted after 30 days** (+14-day grace); no disk; SMTP blocked |
| **Railway** | Workers (see above) | ✏️ **$0/mo Free plan** ($1/mo usage credit; $5 one-time 30-day trial credit) (0.5 GB RAM) | Not stated | **Card required for paid plans; the $5 trial needs no card**; plan on Hobby ($5) for demo week |
| **Fly.io** | Docker apps in chosen regions | **No free tier**: $1 of free credit for 7 days | Not verified | The trial runs out fast (medium confidence) |
| **Cloudflare Workers** | Edge APIs, proxies | 100K requests/day | — | **10 ms CPU per request**; Error 1027 at the daily cap |
| **Netlify** | Static front ends | 300 credits/mo | — | **15 credits per production deploy**, so about 20 deploys uses up the month (the 300-credit model applies to accounts created since Sep 4, 2025; older accounts keep prior limits) |
| **Hugging Face Spaces** | ML demos | Static free; **Gradio/Docker need PRO**; free accounts (>30 days old) get **2 ZeroGPU Gradio Spaces** | Sleeps when unused | Streamlit isn't a native SDK; outbound ports 80/443/8080 only |
| **Streamlit Community Cloud** | Streamlit data apps | Free (up to ~2.7 GB RAM) | **Sleeps after 12 h** without traffic; a viewer clicks to wake it | US-only hosting |
| **Modal** | GPU inference | **$0/mo Starter plan — $30/mo free compute credits** | Serverless containers | Cap concurrency; watch GPU spend |

**Demo-day rule:** open every free-tier URL **5–10 minutes before presenting**, and never demo from a service that sleeps without warming it first.

## Mobile distribution

Android: an EAS internal build gives an **APK link or QR code**, the fastest path. iOS: demo on your own device, or use the web build; TestFlight and ad hoc builds need Apple accounts and time.

## Auth: Clerk

1. [Clerk docs](https://clerk.com/docs) → **Add application** → choose sign-in methods.
2. Copy `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` and `CLERK_SECRET_KEY` into Vercel env vars.
3. Add **both** `http://localhost:3000` and the production domain wherever redirect URLs are configured.
4. ✏️ On **Next.js 16+**, route protection lives in **`proxy.ts`**, not `middleware.ts`.
5. With Supabase, use **Third-Party Auth**; the JWT template is deprecated.

**Python backend verifying Clerk tokens** (from help-me-papi; verified against `clerk-backend-api` 7.1.0 on PyPI — `verify_token` lives in `clerk_backend_api.security` and takes `(token, VerifyTokenOptions)`; the `Clerk` client has NO `verify_token` method, only `authenticate_request`):

```python
import os
from clerk_backend_api.security import verify_token, VerifyTokenOptions

def get_user_id(authorization_header: str) -> str:
    # verify the session token from the Authorization header, then read claims["sub"] as the user id
    token = authorization_header.removeprefix("Bearer ")
    claims = verify_token(token, VerifyTokenOptions(secret_key=os.environ["CLERK_SECRET_KEY"]))
    return claims["sub"]
```

---

## Pre-pitch deployment checklist

- [ ] Production URL works on a **different network** (phone hotspot)
- [ ] Demo account seeded and logged in (Clerk sessions are fixed at 7 days on Hobby)
- [ ] Full demo flow works on the deployed version
- [ ] All env vars set in Vercel **and** Railway
- [ ] OAuth redirect URLs include the production domain
- [ ] RLS enabled on every user-facing table
- [ ] CORS allows only the frontend origin
- [ ] Supabase project awake
- [ ] Backup screen recording uploaded
- [ ] Rollback path known (Vercel: Deployments → Promote a previous deploy; Railway: redeploy the previous commit)

---

Original by Bread04 (hackathon-deployment), adapted in hackathon-ecc as deploy-fast, with commands re-verified and corrections marked ✏️.
