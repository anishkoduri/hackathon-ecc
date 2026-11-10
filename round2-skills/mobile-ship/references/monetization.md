# Monetization — ONLY if your app charges

Skip this whole file unless the demo needs a purchase flow. Most hackathon
test builds don't — a free build with a "coming soon" paywall is the normal
path, and the config-gating in `SKILL.md` is how you ship it. Everything
below is for apps that actually sell something.

## The Paid Apps Agreement — do this before anything monetized

**Apple serves ZERO in-app products — production, sandbox, AND TestFlight —
until the Paid Apps Agreement is Active.** The app-side symptom is an empty
product fetch, which a well-gated app renders as "coming soon". It looks
exactly like a RevenueCat/StoreKit bug; it never is. Check
ASC → **Business (Agreements, Tax, and Banking)** FIRST when iOS prices
don't show.

Path to Active (individual/sole-proprietor, ~30 min of forms + Apple
verification):
1. Complete **legal entity** info (a banner blocks signing until done).
2. Open the Paid Apps Agreement → accept.
3. **Banking**: add the payout account. Verification usually clears within
   hours (Apple says up to 24h; observed faster). Status: Processing → Active.
4. **Tax**: for a non-US individual, the W-8BEN + Certificate of Foreign
   Status. Signer "Title" field for a sole proprietor = **"Owner"**.
5. Status flips New → Processing → **Active**; sandbox products start loading
   shortly after (no new build needed).
6. MRDP compliance prompt ("do your apps provide personal services?"):
   **No** for pure software/subscription apps — "personal services" means
   marketplaces of human labor (tutors, drivers), not app features.

## Apple subscriptions setup

- Monetization → Subscriptions → create a **Subscription Group**, then the
  auto-renewable products (e.g. `premium_monthly` 1-month, `premium_annual`
  1-year). Product IDs are **permanent** — lowercase, no rename, no reuse.
- Each product needs: reference name, localization (display name +
  description), price, and a **review screenshot**. The screenshot must have
  **iPhone screenshot dimensions** — a 1024×1024 square is the *promo image*
  spec and gets rejected here; a full-device screenshot of the paywall works.
- Set products to **Ready to Submit**. The FIRST auto-renewable sub can only
  be submitted **attached to an app version** ("In-App Purchases" section on
  the version page → add both) — never alone.
- **Rejection silently ejects your IAPs.** When a submission is rejected, the
  subscriptions that rode with it fall back to "Prepare for Submission" — and
  resubmitting the app version does NOT re-attach them. After EVERY rejection/
  resubmission, open Monetization → Subscriptions → the group and confirm each
  product says **"Waiting for Review"**; if it says "Prepare for Submission"
  with an "Add for Review" button, click it to re-add the group to the pending
  submission (no new version needed). Unsubmitted products also serve
  unreliably in sandbox, compounding the "paywall empty" confusion.
- Credential for server-side receipt validation (RevenueCat): the
  **In-App Purchase key** (.p8) from Users and Access → Integrations →
  In-App Purchase — required for StoreKit 2. The legacy App-Specific Shared
  Secret is NOT sufficient. Also note Issuer ID + Key ID.

## One-time purchases (non-consumable "Full" / lifetime unlock)

- For an app with no server, a single **non-consumable** product is the simplest trustworthy model:
  - StoreKit restores it on any device with the same Apple ID;
  - no webhook or entitlement server is needed;
  - "Restore Purchases" must still be visible.
- **Family Sharing** (a checkbox on the IAP in ASC) lets up to five family members use the purchase.
  **Once turned on it can't be turned off.** Decide before first sale; it's a strong value lever
  for family and education apps.
- Introductory "launch price": schedule a price change in ASC rather than editing the base price.
  Only say "launch price" or "was £X" in copy while it's literally true.
- Base-price auto-equalisation makes UK or US prices steep in lower-income storefronts. Set
  manual local price points where that matters (owner decision; pricing changes need the owner's
  approval).

## Google Play: merchant profile, subscriptions, service account

Order of operations (the console enforces this silently):

1. **Payments/merchant profile** (Settings → Payments profile). Until it
   exists, Monetize → Subscriptions only shows "Upload a new APK". Fields for
   an individual: business name = your app/brand (public on receipts),
   category ≈ "Computer Software", support email (public!), credit-card
   statement name = short recognizable brand (≤22 chars).
2. **Upload a billing-capable build** to ANY track (internal is fine). "Create
   subscription" stays hidden until a build containing the billing permission
   exists. A build made with the RevenueCat/react-native-purchases dependency
   qualifies even WITHOUT the store SDK key configured — this is what breaks
   the chicken-and-egg: build #1 (no key, paywall "coming soon") unlocks the
   console; build #2 (key baked in) is the real one.
3. **Create the subscription**: ONE product (e.g. `premium`, permanent ID) with
   **base plans** `monthly` (1 month, auto-renewing) and `annual` (1 year).
   Defaults are fine (7-day grace, auto account-hold, charge-at-next-billing,
   resubscribe allow). Then per base plan: set price (accept auto-converted
   regional prices) and **Activate** — a saved-but-inactive base plan sells
   nothing.
   RevenueCat product identifiers for Google are `productId:basePlanId`
   (`premium:monthly`, `premium:annual`).
4. **Service account** (lets RevenueCat validate purchases; also enables
   `eas submit` for Android):
   - GCP console → same project → enable **Google Play Android Developer
     API** → IAM → Service Accounts → create (no project roles needed) →
     Keys → new JSON key. The JSON is a SECRET — upload directly to
     RevenueCat/EAS, never commit.
   - Play Console (account level) → Users and permissions → Invite → the
     service-account email → grant: view app info, view financial data,
     manage orders and subscriptions. Service accounts get no email invite —
     they just appear in the list.
   - **Purchase-validation permission propagates slowly (up to ~36h).**
     Catalog reads work instantly; RevenueCat's credential check may show
     "can't validate purchases" ❌ meanwhile. Not a misconfiguration — wait.

## Paywall requirements (both stores reject without these)

- A visible **Restore Purchases** control (≥44dp target) near the buy buttons.
- Auto-renew disclosure text + tappable **Terms** (Apple's standard EULA URL is
  fine) and **Privacy** links (Apple 3.1.2).
- Use the store-reported localized `priceString`, not hardcoded prices —
  hardcoded currency is wrong for most of the world.
- Layout: on phones stack plans vertically with the paid plan FIRST; never use
  fixed control heights (labels clip at large system font scales — use
  minHeight + wrapping); give each plan's CTA a distinct fill color.

## Sequencing rules for monetized apps

1. **Start store paperwork FIRST, in parallel with coding.** Apple's Paid Apps
   Agreement (legal entity → sign → banking → tax) and Google's payments/
   merchant profile are the longest poles and gate everything monetized.
   Critically: **Apple serves ZERO IAP products — even in sandbox/TestFlight —
   until the Paid Apps Agreement is Active.** A perfectly-wired app shows an
   empty paywall until then. This masquerades as a code bug; it never is.
2. **Google Play needs a build before subscriptions can exist** (the console
   hides "Create subscription" until a billing-capable build is uploaded), and
   your app needs the store products before its paywall works. Break the
   chicken-and-egg with **config-gating** (SKILL.md) and plan for **two builds**:
   one to unlock the console, a second with the store SDK key baked in.
3. **Apple requires the FIRST auto-renewable subscription to be submitted WITH
   a binary** — you cannot ship the IAP alone. Attach the subscriptions to the
   version before submitting for review.
4. **One entitlement, many rails.** Server database is the single source of
   truth for who is premium. App Store and Play purchases flow through
   RevenueCat → webhook → server; web billing (e.g. Stripe) stays a separate
   rail hitting the same server field. Do NOT wire Stripe into RevenueCat if
   web billing already works — both rails converging on one server flag is
   simpler and battle-tested.

## RevenueCat — wiring, webhook, and the "prices don't show" tree

### Canonical wiring (order matters: store products must exist first)

1. **Apps**: + New → App Store (bundle id + the In-App Purchase **.p8 key** +
   Key ID + Issuer ID — StoreKit 2 requires the key; the App-Specific Shared
   Secret alone is NOT enough) and + New → Play Store (package name + the
   service-account JSON). Each app yields a **public SDK key**
   (`appl_…` / `goog_…`) — public by design, safe to commit into `eas.json`
   build env.
2. **Products**: add by ID — Apple: `premium_monthly`, `premium_annual`;
   Google: `premium:monthly`, `premium:annual` (productId:basePlanId). The
   dashboard "Import" button may be absent — manual "+ New" is fine.
3. **Entitlement**: one identifier (e.g. `premium`) ← attach ALL four
   products. The app checks `customerInfo.entitlements.active["premium"]`,
   never per-product.
4. **Offering**: keep/create `default` with preset **Monthly** and **Annual**
   packages (`$rc_monthly`/`$rc_annual`) → the SDK reads `offering.monthly` /
   `offering.annual` with zero client changes when products change.
5. **Webhook** (Integrations → Webhooks): URL = your server endpoint;
   Authorization header = a secret YOU generate. The SAME value goes in the
   server's env (e.g. Cloud Run `REVENUECAT_WEBHOOK_AUTH`). Set environment to
   **Both Production and Sandbox** (test purchases are sandbox — production-only
   silently drops them) and it's project-level, one webhook covers all apps.
   **A server-side curl only proves YOUR half.** Curling your endpoint (401
   without header / 2xx with) verifies the receiver — it does NOT prove the
   RevenueCat-side webhook exists. Failure mode lived through: purchases
   validated, entitlements granted in RC, zero events delivered — because the
   RC webhook was never created; every downstream symptom ("purchase works,
   premium never flips, restore does nothing") followed. Definition of done =
   the webhook entry exists in RC **and** a real purchase's INITIAL_PURCHASE
   shows up in your server's event log. Also note: RC only dispatches events
   created AFTER the webhook exists — historical events are not replayed, so
   verify with a fresh purchase.

### Client pattern (react-native-purchases)

- `Purchases.configure({apiKey})` once, then **`Purchases.logIn(<your user
  id>)`** — this makes the webhook's `app_user_id` equal your database user
  id, which is what lets the server map events to accounts. Skipping logIn is
  the classic "purchase worked, entitlement never flipped" cause.
- Purchase flow: `purchasePackage(pkg)` → on success poll your own
  `/api/me`-equivalent until the server webhook lands (a 10×2s loop with a
  "will activate shortly" fallback message covers webhook latency).
- Config-gate: `IAP_ENABLED = !!API_KEY`; every export no-ops when disabled.
  Web gets a `purchases.web.ts` stub so the native module never enters the
  web bundle.
- Server keeps ONE entitlement field fed by multiple rails (RevenueCat webhook
  for stores, Stripe webhook for web). Do NOT route existing web billing
  through RevenueCat — needless migration.
- Stripe API-version gotcha (web rail): newer versions moved subscription
  `current_period_end` to item level (`items.data[].current_period_end`) —
  read top-level with an item-level fallback.

### "Paywall shows coming-soon / no prices" decision tree

1. **Is the platform SDK key in THIS build?** (Key added after the build was
   made = old build has no key. Check the build log's env list.)
2. **iOS: is the Paid Apps Agreement Active?** Not Active → Apple returns zero
   products everywhere including sandbox. (This was the real cause the one
   time everything else looked correct.)
3. **Android: is the console still reviewing the release?** Testers run the
   previous build until "Changes in review" clears.
4. **Offering packages contain THIS store's products?** A package holding only
   the other platform's product yields an empty offering on this one.
5. **Products active?** (Play base plans activated; ASC products at least
   Ready to Submit / attached to a version.)
6. **Propagation**: brand-new products can take up to ~24h (Apple sandbox) /
   hours (Play) to serve. If steps 1–5 pass, wait before touching anything.

### Dashboard badges decoded

- **"Could not check" on App Store products** — RevenueCat lacks the OPTIONAL
  App Store Connect API key used only for status display. Cosmetic; purchases
  unaffected. (Different credential from the required In-App Purchase .p8.)
- **Play credential check "can't validate purchases" ❌ with catalog reads ✅**
  — Google permission propagation (≤36h after granting). Wait, don't rewire.
- Server-side verification beats dashboard-staring: after a test purchase,
  check your own webhook logs / user row to confirm the entitlement flip.

## The 3.1.2(c) rejection (subscription information missing)

Read WHICH half Apple means. The usual failure is METADATA, not code: the
**App Description must contain a functional Terms of Use (EULA) link**
(Apple's standard EULA URL is fine) and the ASC Privacy Policy field must be
filled. Separately the in-app purchase flow must state the subscription's
title, length and price with working Terms + Privacy links. Fixing only the
app and not the description repeats the rejection verbatim.

## Monetization triage index

| Symptom | Likely cause |
|---|---|
| Paywall shows "coming soon" on iOS, Android fine | Paid Apps Agreement not Active |
| Paywall "coming soon" on one platform | Missing that platform's SDK key in the build, or offering has no products for that store |
| Play: no "Create subscription" button | No billing-capable build uploaded yet |
| RevenueCat "Could not check" badges | Cosmetic (missing optional ASC API key) or Play permission propagation (≤36h) |
| Purchase succeeds but premium doesn't unlock | Webhook auth/env missing, or app_user_id ≠ your user id |
| One-time unlock, family pricing, launch price | Non-consumable + Family Sharing (irreversible) |
