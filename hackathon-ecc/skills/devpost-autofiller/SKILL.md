---
name: devpost-autofiller
description: Drafts a complete Devpost hackathon submission (tagline, full project story, built-with tags, checklist) from the repo's README, commit history, and any team notes. Use when the user mentions Devpost, a hackathon submission writeup, "what we learned", or needs the project story written before a deadline. Assumes a README already exists (run readme-writer first if there is none); use only when the Devpost form itself is the deliverable.
---

# Devpost Auto-Filler

You write the Devpost submission at hour 23 so the team doesn't have to choose between sleep and a writeup. The repo already contains the whole story — what was built, what broke, what got cut — your job is to excavate it and tell it in the team's voice, not LLM-brochure voice.

How the form actually works (so the draft pastes in cleanly): the **tagline has a hard 140-character limit**; the project story is **one freeform field that renders Markdown** (and LaTeX), pre-seeded with seven standard headings; "Built with" tags are freeform strings; the demo video is a **link** to a publicly-hosted YouTube/Vimeo video, not an upload. Crucially, **submissions stay editable until the deadline and freeze after it** — so the right move is submit a rough draft *early* and keep improving it, never hold for perfect. Late submissions exist only at the organizer's discretion.

## Step 1 — Mine the sources

1. **Repo:** README, `PLAN.md` if present, and the structure of the code (the tech stack list comes from lockfiles and imports, not from memory).
2. **Commit history** — this is the goldmine, read it like a diary:
   - `git log --reverse --format='%h %ad %s' --date=format:'%a %H:%M'` — the chronology. The first commit is the inspiration's timestamp; the 3 a.m. commits are the challenges.
   - Look for the *story beats*: `fix`, `revert`, `actually works now`, `WIP desperate`, a feature directory that appears and later disappears (that's a cut — cuts are "challenges we ran into" gold).
   - `git shortlog -sn` for the team list.
3. **Anything the user throws at you** — voice notes transcripts, chat fragments, "we almost gave up at 4am when the websocket kept dropping". Ask once: *"Any war stories? One sentence each — what almost killed you, and what moment felt great?"* Then move on; don't block on it.
4. **The event** — name, and any sponsor prizes being targeted (sponsor judges filter on the "built with" tags).

## Step 2 — Draft every Devpost field

Produce all fields in one markdown block, ready to paste:

```markdown
## Project name + tagline
<name> — <tagline; HARD LIMIT 140 chars, aim ≤ 80; what it does, not how clever it is>

## Inspiration
<2–3 sentences. The specific moment/problem, not "we've always been passionate
about". If the commit log shows a pivot, the honest version — "we started
building X and realized Y" — is a BETTER story. Use it. Devpost's own judge
interviews back this: "storytelling within the video and the text description
definitely helps keep the judges engaged.">

## What it does
<3–4 sentences, present tense, user's point of view. Describes only what the
demo actually shows — judges read this WHILE watching the video, and any gap
between the two reads as dishonesty. Devpost's bar: "if you can't explain how
to use your project in a sentence or two, it might be too complicated.">

## How we built it
<Stack as evidenced by the code, in build order, one line on the architecture's
one interesting decision. Name sponsor tech explicitly and first. If AI tools
wrote code, say which and for what — MLH rules require teams to "be honest and
transparent about the AI code tools they used," in the README too.>

## Challenges we ran into
<2–3 real ones from the commit archaeology, each with how it was beaten or
worked around. Specific beats impressive: "CORS ate 2 hours" outperforms
"we faced many technical challenges". MLH's Completion criterion literally asks
"how many points of failure did the hack have and how many were solved" —
this section answers it in writing.>

## Accomplishments that we're proud of
<2–3, at least one with a number (hours, commits, latency, working features).
"It actually works end-to-end" is a legitimate entry and judges know it.>

## What we learned
<2–3 sentences. Technical lesson + team lesson. Learning is one of MLH's four
equally-weighted judging criteria — this field is scored, write it like you
mean it.>

## What's next for <Project Name>
<2 sentences max, concrete ("ship the mobile view, get 10 classmates using
it"), not "revolutionize education".>

## Built with
<comma-separated lowercase tags — every real technology, sponsor tech first
under its exact product name; Devpost's public gallery filters on these and
sponsor judges look for their tool here>
```

Heading wording note: use Devpost's default headings **verbatim** as above ("Accomplishments that we're proud of", "What's next for <name>") — they're the platform's pre-seeded placeholders, judges expect them, and the story is one Markdown field so the headings are just text you control.

## Step 3 — Voice pass and checklist

After drafting, do one revision pass with these rules:

- **Kill brochure voice.** Delete every "seamlessly", "leverage", "revolutionize", "passionate". If a sentence could appear in any project's submission, it's not about this project — replace it with a specific.
- **First person plural, past tense for the build, present for the product.** "We built / it does."
- **Every claim demoable.** If the video won't show it, it isn't in "What it does" — move honest unfinished work to "What's next".
- Flag anything you inferred but couldn't verify with `<!-- CHECK: ... -->` comments so the team confirms in 30 seconds instead of proofreading everything.

Close with the non-text checklist. Devpost's own warning applies: "you'd be surprised how many submissions are disqualified simply because they didn't meet the baseline criteria" — these kill more submissions than bad prose:

```text
[ ] Video on YouTube/Vimeo, PUBLIC or unlisted — never private (it won't embed
    for judges); on YouTube mark "Not made for kids" or embedding breaks
[ ] Video uploaded HOURS early — YouTube processing can take "a few minutes to
    several hours" (Devpost's words), and the deadline doesn't care
[ ] Video length within THIS event's cap (~3 min is the norm; some events cap
    at 1 — read the rules page, not the vibes)
[ ] Repo link public + API KEYS STRIPPED (MLH rules require both)
[ ] AI tools disclosed in the README (MLH rules) + GenAI disclosure field on
    the submission form filled
[ ] Every teammate added via Manage Team (unadded teammates aren't winners)
[ ] Sponsor prize categories opted into on the form — you can't win a prize
    you didn't enter
[ ] Tagline ≤ 140 chars; thumbnail 3:2 JPG/PNG/GIF under 5 MB
[ ] SUBMITTED EARLY — drafts don't count, and you can keep editing a submitted
    project until the deadline; after it, the hackathon copy is frozen
```

Offer to also generate the 100-word version — many events ask for a short description at check-in, and it's free to make now.
