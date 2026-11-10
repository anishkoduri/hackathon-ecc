---
name: mobile-ship
description: >-
  Playbook for shipping a TEST BUILD of an Expo/React Native mobile app at a hackathon — EAS builds (local iOS builds need a Mac; EAS cloud builds work from any OS), build-failure triage, TestFlight and Play closed testing, store sequencing, App
  Review anti-rejection tactics, and the simulator gotcha. Use this skill for ANY mobile shipping
  work: "build the app", "ship a test build", "get it on TestFlight", "closed testing", "submit to
  the App Store / Play Store", "why was my app rejected", store rejections (2.1, 2.3, 4.3),
  "production .ipa won't run on the Simulator", or a mobile app that needs a testable build for
  demo day. Also covers Flutter/xcodebuild archive, export and upload (including expired Xcode
  accounts). Monetization (RevenueCat, in-app subscriptions, paywalls) is covered in a secondary
  section at the end — read it only if your app actually charges.
---

# Mobile Ship Playbook (Expo/EAS → TestFlight / Closed Testing)

Field-tested on a real commercial launch (MathMonarch, 2026): two Apple
rejections recovered, every gotcha below was hit for real. The skill has two jobs: (1) sequence the work in the order the stores actually allow, and (2) stop you from re-losing hours to known traps.

**Scope:** this skill gets a TEST BUILD into testers' hands — a local build, TestFlight, or Play closed testing — in time for demo day. A full commercial launch (store agreements, subscriptions, paywalls, marketing) is a different job; the monetization half lives in `references/monetization.md` and is only for apps that charge. For the backend/API side of your app, the plugin's `deploy-fast` skill covers hosting; this skill doesn't depend on it — use it only if your app has a backend to ship.

## Route to the right reference

| Working on… | Read |
|---|---|
| Building an .ipa/.aab locally, build failures, submitting binaries | `references/local-builds.md` |
| TestFlight, submission mechanics, demo-account seeding, App Review rejections | `references/ios-store.md` |
| Play closed testing, the production gate, license testing | `references/android-store.md` |
| Promo videos from code, ad copy, minimum ad budget | `references/launch-marketing.md` (after the build ships) |
| ONLY if your app monetizes: store agreements, subscriptions, RevenueCat, paywalls | `references/monetization.md` |

Read the relevant file BEFORE acting — most store operations are one-way doors (product IDs are permanent, agreements gate everything, retries create duplicate-build errors).

## The golden sequencing rules (test build)

The stores enforce a hidden dependency order. Getting it wrong costs hours at a hackathon:

1. **Build early, build locally.** `eas build --local` skips the cloud queue and credit spend and produces the identical signed artifact. Aim for a first build in the first hour — a build that exists can be tested; a build that doesn't exist can't.
2. **Apple: a build must finish "Processing" (10–60 min) before it appears in TestFlight or the build picker.** Plan for the wait; do not rebuild while processing.
3. **Google Play: upload a build to ANY track (internal is fine) early.** It unlocks console features, and for new personal accounts the closed-testing clock (12–20 testers × 14 days) is the long pole — start it as soon as you have anything installable.
4. **Never blind-retry a submission.** The submission is a server-side job that can sit queued while the CLI looks hung. Check the real state (submission URL, App Store Connect → TestFlight, or the EAS GraphQL API) before retrying — a retry of an already-succeeded upload fails opaquely with a duplicate-build-number error.
5. **Test a release-profile build on a real device before submitting**, not just Metro dev. Most 2.1 rejections are bugs that only show up in the release build.

If your app monetizes, three more sequencing facts apply — they live in `references/monetization.md`, not here: Apple serves zero in-app products (even in sandbox/TestFlight) until the Paid Apps Agreement is Active; Google hides "Create subscription" until a billing-capable build is uploaded; and Apple's first auto-renewable subscription must be submitted attached to a binary.

## Config-gating (the architecture that makes all of this shippable)

Gate every paid or not-yet-ready surface behind build-time env keys (Expo: `EXPO_PUBLIC_*` in `eas.json` per-profile `env`). No key → the surface renders a harmless "coming soon"; key present → the real thing. Why this matters:

- You can ship store builds BEFORE products/agreements exist (unblocks Google's build-first rule and Apple review of free features).
- A build can never crash or show dead buy-buttons because config is missing.
- Public SDK keys are safe to commit in `eas.json`; SECRET values (webhook auth tokens, .p8 keys, service-account JSON, demo-account passwords) never go in git — they are pasted directly into the service.
- Platform-split modules keep native-only code out of the web bundle: a native module plus a `.web.ts` no-op stub. Same pattern for anything web-only — e.g. `expo-router/head` is WEB-ONLY and throws error alerts on every native navigation if rendered there (a real Apple 2.1 rejection): split it.

## Review anti-rejection checklist (Apple; Google analog applies)

The rejections actually hit, and their cures:

- **2.1 (crash/bug on tap):** a web-only component rendering on native. Test a release-profile build on-device before submitting, not just Metro dev.
- **2.3 (feature "marketed but coming soon"):** the reviewer opened a gated feature on a FRESH account and saw an empty state. Cure: a **seeded demo account** — pre-grant premium server-side (no purchase/webhook dependency), complete whatever content-unlocks the features need (e.g. finish placement, win one quiz) so every advertised feature demonstrably works. Verify the seeding via API before submitting. Put credentials in App Review sign-in fields AND notes.
- **4.3(a) (spam/template):** purge framework starter assets byte-identical to thousands of template apps; distinctive listing copy; never name trademarked franchises in metadata.
- **Review notes template:** demo credentials → "what changed since last submission" (map each prior rejection to its fix) → where each gated feature lives → how to test the purchase ("register a fresh account; purchases are free in Sandbox") → thanks.
- Reviewers test IAP **free in Apple Sandbox** / as **Google license testers**. Neither store charges reviewers; don't build fake bypasses for them.

The full rejection playbook (including the iPad-design trap, the 2.1 "Information Needed" first-submission round, and the resubmission notes template) is in `references/ios-store.md`.

## Working with the human

For App Store Connect, use the API key (`~/.appstoreconnect/` on the owner's Mac) and, for web-only steps, the owner's signed-in browser session. For consoles you can't reach (Play Console, RevenueCat), give **one step at a time** with exact field values, wait for confirmation or a screenshot, and adapt — console UIs shuffle constantly and a wall of 12 steps always desyncs from reality. Ask for screenshots on any error; they diagnose faster than descriptions. Anything you CAN verify yourself (webhook auth via curl, demo-account state via API, build status via CLI/GraphQL), verify yourself — never ask the human to check what you can check.

- **Owner-only steps — ask early, in one message:**
  - signing in to App Store Connect in the agent's browser (for App Privacy, agreements and first-purchase attachment; the session expires after about a day);
  - a physical-device screen recording when App Review asks for one (give a step table with button labels copied from the code);
  - which contact email goes public;
  - anything irreversible (Family Sharing, prices, final submission).
- After a review message, read it fully, list what only the owner can supply, start everything else meanwhile, and check the owner's material (video frames, device and OS) before sending it on.

## Quick triage index

| Symptom | Likely cause | Reference |
|---|---|---|
| Build hangs at "Computing project fingerprint" | Set `EAS_SKIP_AUTO_FINGERPRINT=1` | local-builds.md |
| iOS build: "iOS X.Y is not installed" | `xcodebuild -downloadPlatform iOS` | local-builds.md |
| Metro/prebuild crashes on latest Node | Use Node LTS (v20/v22) via explicit PATH | local-builds.md |
| `eas submit` hangs at "Submitting" | Job queued server-side; NEVER blind-retry (duplicate build) | local-builds.md |
| Git branch ref vanished mid-build | EAS local build's shallow-clone collided with a commit | local-builds.md |
| Flutter/xcodebuild export: "Failed to Use Accounts" | Xcode Apple Account session expired → local export + Transporter; API key durable fix | local-builds.md |
| "Redundant Binary Upload" | That build number already reached ASC → don't retry; bump the build number | local-builds.md |
| ASC Save stays disabled after filling a field | React form ignores programmatic values → click and type | ios-store.md |
| Build invisible in TestFlight after a successful upload | Still processing (10–60 min); check for an ITMS email | local-builds.md |
| Can't promote to Play production | Personal-account closed-testing rule (12–20 testers × 14 days) | android-store.md |
| Local iOS build passes TestFlight but "Invalid Binary" on submit | Built with a beta/non-RC Xcode (ITMS-90111) — rebuild with release Xcode | local-builds.md |

## Only if your app monetizes

Skip this entire section unless the demo needs a purchase flow — most hackathon test builds don't. When it applies, read `references/monetization.md`, which covers: the Paid Apps Agreement (Apple serves zero in-app products until it is Active), Apple subscription setup and the one-time-purchase model, Play merchant profile / subscriptions / service account, RevenueCat wiring and the webhook, the client pattern, the "paywall shows coming-soon / no prices" decision tree, paywall requirements both stores enforce, and the 3.1.2(c) subscription-information rejection.

Adapted from mobile-app-release by Ravish Garg, MIT licensed, for hackathon-ecc.
