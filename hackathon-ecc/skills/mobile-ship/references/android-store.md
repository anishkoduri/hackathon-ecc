# Google Play Console — testing tracks and the production gate

## Testing tracks + the personal-account production gate

- Personal developer accounts registered after ~Nov 2023 must run a **closed
  test with 12–20 testers (console states the exact number) opted-in for 14
  continuous days** before applying for production. Organisation accounts and
  older personal accounts are exempt.
- **How to know if you're gated**: the "Promote release" menu — if Open
  testing/Production are GREYED OUT on a closed-testing release, the rule
  applies. The *absence of a warning banner elsewhere proves nothing* (learned
  the embarrassing way).
- Strategy: start the closed test and its tester recruitment EARLY — the
  14-day clock is the long pole and runs while you keep shipping. Uploading
  new builds to the track does NOT reset the clock; letting testers drop
  below the threshold does.
- Testers: any Gmail works; a Google Group makes list management painless;
  developer tester-exchange communities exist to fill quotas.
- Each closed-testing release goes through a short Google review (hours);
  the app shows "Changes in review" and testers keep the OLD build until it
  clears — a tester reporting stale behavior usually just hasn't got the new
  build yet.

## License testing (free purchase testing)

- **License testing** (account level → Setup → License testing): add tester
  Gmails; their purchases use a test card — full purchase flow, zero charge.
  This is how you verify the IAP end-to-end without spending money. A
  non-license account WILL be charged real money.
- Only relevant if the app monetizes — see `monetization.md` for the
  subscription setup that license testing exercises.

## First upload: budget an hour for the questionnaires

- Play review can raise one-time app-content tasks on first upload
  (Data safety, Content rating, Target audience, Privacy policy) — budget an
  hour for the questionnaire pass.

## If the app monetizes

- A **payments/merchant profile** is required before any subscription can
  exist, a billing-capable build must be uploaded before "Create
  subscription" appears, and a **service account** lets RevenueCat validate
  purchases (and also enables `eas submit` for Android). All of that lives
  in `monetization.md` — skip it for a free test build.
