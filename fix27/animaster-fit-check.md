# Animaster Lib fit-check (fix #27, Nov 16, 2026)

**Verdict: LEAVE IT OUT — effectively fully paywalled; no free tier, no free sample.**

## Evidence (checked Nov 16, 2026, ~01:09 CST)

- Homepage fetched live (https://animmasterlib.dev/, crawled <1 min before the check): "300 PRO UI COMPONENTS FOR MODERN WEB PRODUCTS". Pricing section: **PRO $4.99** (struck-through $10) — 300 PRO-level components, lifetime access; **Premium $8** (struck-through $20) — 300 components + templates, Figma mockups, courses, lifetime updates, community. Buttons: "Unlock PRO Get 300 Components" / "Go Premium Unlock Everything".
- FAQ, verbatim: "How will I get access to the components? You'll receive access to a Google Drive folder containing all the components." (i.e. after purchase). "Are these components prompts or code? This is code, all components built from scratch, tested and optimized." "Is this a one-time payment or subscription? This is a one-time purchase with access to materials for a lifetime." "What languages? 60% HTML/CSS/JS, 30% React, 10% Next.js."
- **No free tier, free sample, or free download anywhere on the homepage** (full 720-line fetch). The only free thing is viewing the thumbnail gallery (preview images, no code).
- Corroborated by commenters on the reels promoting it: "you have to pay", "Pricing in the menu", "Paid service, don't waste your time", "Lie. Don't believe it. You have to pay." (One source quotes the same $4.99 PRO / $8 Premium prices.) The "free" framing in the reels is engagement bait.

## Decision

- **Not vendored, not wired into the design package, not a dependency.** Adding it would put a paid gate ($4.99/$8, Google Drive folder after payment) in the design path, violating the standing rule (free tiers only, local-first, no paid services) and the user's explicit instruction ("if the free portion is thin, unclear, or effectively paywalled, say so plainly and leave it out").
- **Inspiration-only reference also rejected:** the gallery thumbnails carry no usable component code, and pointing the design flow at a paywalled catalog invites paywall friction mid-build. MotionSites (free sample + techniques + media) already supplies the cinematic-component source. The user can overrule and ask for an inspiration-only pointer.
- The design-process palette (PALETTE-FIRST_F27) therefore lists MotionSites + the existing design package only — Animaster is not in it.
