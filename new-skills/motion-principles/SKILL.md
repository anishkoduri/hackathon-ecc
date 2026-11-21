---
name: motion-principles
description: Use when deciding how an interface should move — entrances, feedback, transitions, gestures, scroll motion — or when motion feels robotic, slow, or over-animated, or when the user names a motion principle (Doherty threshold, Fitts's law, squash and stretch, staggering, rubber banding, origin awareness, peak-end rule) or asks for an immersive surface. The why layer for motion: 19 principles with guardrails, plus the immersion direction. GSAP is the how; this skill is the why.
---

> **Hackathon-ecc note (fix #34, MOTIONPRINCIPLES_F34).** This skill is authored natively for this plugin from textbook public knowledge: Disney's twelve principles of animation (Thomas & Johnston, *The Illusion of Life*, 1981) adapted to UI, plus the standard HCI laws (Fitts 1954; Hick 1952; Doherty & Thadhani 1982; von Restorff 1933; Kahneman's peak-end rule). The 19-item list's origin is a Nov 19, 2026 reel by @bendoescareer (co-founder of Amoeba) naming the same 19 terms; the creator's own skill file is NOT used, copied, or vendored — it sits behind product/Discord links with no verifiable open licence, and the principles themselves are public knowledge that needs no licence. **Layer role: motion principles** (inventory `skills/orchestrate/references/design-inventory.md` §14) — the why layer of the one design system. Routing: `design-taste-frontend` (Taste) consults this skill whenever it decides motion and names the principle(s) each motion serves in the D19 record; `gsap` implements against it (the engine is the how, this skill is the why); the motion tokens (`motion-foundations`) still carry the values — this skill's guardrails are the ceilings and floors the tokens must respect, and where a token and a guardrail conflict, the guardrail wins and the conflict is recorded (D19). `browser-qa` renders the motion verdict (MOTION-QA_F34) from the checkable subset below and remains the sole executor of pass/fail screen verdicts. The checkable subset: Doherty response, the 300ms timing ceiling, origin-aware entrances, interruptibility, frequency-of-use restraint, and the reduced-motion fallback.

# Motion principles — why an interface moves the way it does

Motion is decided, not decorated. Every animation on a surface serves a named principle below, with its values from the motion tokens and its reason in the D19 record. A motion that serves no principle is cut; a principle claimed but not visible in the result is a finding.

## 1. Response — the user is never left waiting

- **Doherty threshold** — productivity rises when the system responds fast enough that neither side waits on the other. *In UI:* every input gets a visible response — a press state, an optimistic update, a skeleton — immediately, not when the work finishes. *Guardrail:* visible feedback within **400ms** of input, and the design aims far under it; a response slower than 400ms with no interim feedback is a defect, not a style.
- **Timing** — UI animation is feedback, not cinema. *In UI:* entrances, exits, hovers, and state changes are short and purposeful. *Guardrail:* UI animations stay **under 300ms**; longer motion is allowed only where it is the content itself (a dealt hero moment, a scroll-scrubbed sequence) and is recorded as such.
- **Interruptible motion** — the user can change their mind mid-animation. *In UI:* a second tap, a swipe back, or a route change cancels or retargets the running animation from its current position — never a locked-out wait for an animation to finish, never a snap back to the start. *Restrain:* interruptibility is not jitter — a retarget eases from the current state, it does not restart.
- **Frequency of use** — the more often something is used, the less animation it should carry. *In UI:* rank the surface's actions by how often they fire; daily actions (tab switches, list scrolls, the primary button) get the least motion — fast, direct, nearly invisible — and the elaborate choreography is spent on rare, high-signal moments (first run, completion, the dealt hero). *Guardrail:* an animation on a high-frequency action that a user must sit through repeatedly is a defect even if it is beautiful once.

## 2. Character — movement that reads as physical

- **Anticipation** — a small wind-up signals what is about to happen: a button compresses before it fires, a card leans before it flies. *Restrain:* the wind-up is a beat, not a delay — it never pushes feedback past the Doherty line.
- **Squash and stretch** — things deform under force: press states compress, landings absorb, fast elements elongate. *In UI:* subtle scale/axis deformation on press, drop, and bounce. *Restrain:* text and data never deform — squash and stretch is for objects and containers, and it stays small on app surfaces.
- **Slow in, slow out** — real movement accelerates and decelerates; linear motion reads as robotic. *In UI:* entrances ease out, exits ease in, moves ease in-out — the motion tokens' curves, never a bare `linear` on a UI transition (linear is for progress and scrub, where the user's hand is the easing).
- **Arcs** — things travel in arcs, not straight lines, when their path is free. *In UI:* elements moving between positions (a chip flying to a cart, a card re-sorting) curve; straight lines are for layout-constrained moves (drawers, rails).
- **Follow-through** — when the main element stops, its details keep moving a beat: the badge settles after the card lands, hair and cloth lag. *In UI:* secondary elements overshoot and settle a fraction after the primary — the cheapest signal that a surface is one physical thing.
- **Secondary action** — a small flourish that backs up the main action without competing with it: the icon that ticks as the toast lands, the counter that rolls as the total updates. *Restrain:* if the flourish is what the user notices, it is no longer secondary.
- **Exaggeration** — feedback is amplified past realism to make the moment legible: the success bounce is bigger than physics, the error shake is unmistakable. *In UI:* exaggerate the one signal the moment exists for. *Restrain:* exaggeration is spent on signal, never on decoration, and never on high-frequency actions (frequency of use governs).
- **Solid drawing** — flat things are given depth and volume, through shading, layering, or interaction, so they read as objects in a space. *In UI:* surfaces keep consistent light, elevation, and perspective while they move — an element that slides under one shadow and over another breaks the world. This is the 2D root of the immersion direction below.

## 3. Space and attention — where things come from, what is remembered

- **Origin awareness** — things grow out of where the user acted: a menu opens from its button, a detail expands from the card that was tapped, a popover points at its trigger. *Guardrail:* an entrance whose origin is an arbitrary center (or the screen's center) when a trigger exists is a defect — the eye must be able to trace every appearing element back to its cause.
- **Staggering** — related elements arrive one after another, not in unison: list rows cascade, grid items ripple from the origin. *In UI:* stagger order follows reading order or distance from the origin; the per-item delay comes from the motion tokens. *Restrain:* staggering delays the last item — a long list staggers a visible window, not all forty rows (timing and frequency govern).
- **Rubber banding** — pull past the end and the surface stretches, then springs back on release: overscroll, pull-to-refresh, drag-past-the-limit. *In UI:* resistance grows as the pull grows, and the release is a spring, never a hard stop or a teleport. It is the honest signal that a boundary is real but the gesture was heard.
- **Von Restorff effect** — the one that looks different is the one that is remembered. *In UI:* the primary action, the warning, the new thing is the visual odd-one-out on its surface — by color, shape, or motion. *Restrain:* exactly one odd-one-out per surface per job; two competing anomalies cancel each other.
- **Peak-end rule** — people judge an experience by its best moment and by how it ends, not by its average. *In UI:* design the peak (the dealt hero moment, the success state) and the ending (the completion, the summary, the last screen) deliberately; a flow that trails off wastes the two moments that decide whether it is remembered well. This is why the hero verdict and the finish review carry the weight they do.

## 4. Effort — the cost of deciding and reaching

- **Fitts's law** — the time to reach a target grows with distance and shrinks with size. *In UI:* primary targets are big and near — near the thumb, near the cursor's rest position, near the related content; destructive targets are small, far, or gated. *Motion consequence:* an element that moves toward its user (a toolbar that docks where the work is) is cheaper than one the user must chase.
- **Hick's law** — decision time grows with the number of choices. *In UI:* fewer simultaneous options, grouped and staged choices, a recommended default. *Motion consequence:* choreography cannot fix a surface that asks too much at once — cut or stage the choices first, then animate what remains.

## 5. Immersion — the direction (Anish, fix #34)

Immersion is a design direction, not a principle: the surface reads as one continuous space the user is inside, not a stack of pages they are shown. It is the direction the dealt hero moment takes when the brief calls for it, and it is decided by Taste like every other direction, with its D19 reason recorded.

- **Depth and spatial continuity** — one world, consistently lit and layered (solid drawing at scene scale): elements that persist across views keep their place and identity; transitions travel through the space (camera moves, parallax, shared-element morphs) instead of cutting between unrelated screens.
- **Full-viewport moments** — the hero takes the whole viewport and is a place, not a banner: a 3D scene, a cinematic layer, a world the user can look around in. The implementation routes: `threeui` (ready-made 3D components — the immersion toolkit), `getlayers` (cinematic layers), `gsap` ScrollTrigger (scroll-driven travel), Vanta / React Three Fiber per Taste's standing rules.
- **Scroll-driven progression** — scrolling is travel: the scene evolves, the camera advances, the story unfolds in place, rather than a static page sliding under a window. Progress is spatial (where am I in this world), not just positional (how far down the document).
- **Restraint guardrails (binding):** immersion is spent on the surfaces that earn it (heroes, stories, showcases) and never taxes the task surfaces (forms, tables, checkout) — frequency of use governs. The surface keeps ONE WebGL-heavy effect (WEBGL_ONE_F22); the performance budget binds (a scene that cannot hold its frame on a mid device falls back, it does not jank); a static or 2D fallback ships for mobile, low-power, and no-WebGL; under `prefers-reduced-motion: reduce` the finished still shows and scroll-driven travel becomes direct placement; text over a scene keeps its scrim and 4.5:1 contrast; and the user is never trapped — immersion never removes the exit, the skip, or the ordinary navigation.

## What NOT to do

- **No principle-free motion.** An animation with no named principle and no D19 reason is decoration debt — cut it or name it.
- **No ceiling-breaking defaults.** A token or preset that pushes ordinary UI motion past 300ms, or feedback past 400ms, is re-based to the guardrail, and the conflict is recorded.
- **No choreography on the daily path.** The most-used actions get the least motion (frequency of use) — a landing-page entrance replayed on every tab switch is a defect.
- **No vendoring the source list.** The reel that named these 19 terms is the list's origin, not a source to copy: the creator's skill file is not fetched, reproduced, or paraphrased into this skill — the principles are stated here in the plugin's own words from the textbook record.
- **No verdict-stealing.** This skill names what good motion is; whether a built screen has it is `browser-qa`'s verdict (MOTION-QA_F34), never this skill's.

## Files

- Textbook basis: Thomas & Johnston, *The Illusion of Life* (1981) — the twelve principles; Doherty & Thadhani, *The economic value of rapid response time* (IBM Systems Journal, 1982) — the 400ms threshold
- List origin: @bendoescareer (Amoeba), Instagram reel, Nov 19, 2026 — the 19 terms as named there
- Implementation engine: `skills/gsap/SKILL.md`; motion tokens and values: `skills/motion-foundations/SKILL.md`, `skills/motion-patterns/SKILL.md`
- Immersion toolkit: `skills/threeui/SKILL.md`; cinematic layers: `skills/getlayers/SKILL.md`
- Verdict criteria: `skills/browser-qa/SKILL.md` (MOTION-QA_F34)
