# Fix #30 live-test prompt — Grok 4.7 Extra High orchestrator

Run this in Cursor after fix #30 lands (plugin installed from the fix #30
bundle). Paste the whole prompt into a fresh Cursor chat in a **scratch
project** (not a real repo — the coding task writes files). Before starting,
select **Grok 4.7 Extra High** in the model picker.

## The prompt (paste into Cursor)

> You are the orchestrator for this session. Do BOTH tasks below, in order,
> and then report which model ran each part.
>
> **Task A — reasoning-heavy (no code yet).** Design the merge-order rule
> for this situation: two implementers in the same wave both edit
> `src/billing/invoice.ts`, one renaming a function the other calls in a
> new code path. Write a one-page decision doc (`DECISION.md`) that: (1)
> states the rule for which implementer's version wins on conflict and
> why, (2) names the two failure modes if the rule is applied blindly,
> (3) gives the exact verification steps the orchestrator runs before
> accepting the merge, and (4) says what you would do differently if a
> third implementer also touched the same file. Reason from first
> principles — do not just restate the question.
>
> **Task B — repo-scale coding.** In this scratch project, build a tiny
> in-memory task queue in TypeScript: `src/queue.ts` (a `TaskQueue` class
> with `enqueue`, `dequeue`, `size`, and a max-concurrency of 2),
> `src/worker.ts` (a worker that takes tasks from the queue and records
> results), `src/index.ts` (a demo that enqueues 5 tasks and prints the
> results in completion order), and `test/queue.test.ts` (tests for
> enqueue/dequeue order, the concurrency cap, and the empty-queue case).
> Run the tests and report the result.
>
> **Report (required, at the end).** For Task A and Task B separately,
> state: (1) which model ran the parent agent (the model shown in the
> chat model indicator), (2) which model ran each subagent you spawned,
> if any (from the subagent rows), and (3) whether any subagent fell back
> to a different model than you asked for. Do not guess — report only
> what the indicators actually showed.

## Pass / fail

- **PASS:** the parent agent ran **Grok 4.7 Extra High** on both Task A
  and Task B (the model indicator says so). Report the subagent models
  for information — subagent routing is a known Cursor limitation
  (per-subagent model selection is unreliable), so a subagent on another
  model does not fail this test; only the parent matters.
- **FAIL:** the parent ran anything other than Grok 4.7 Extra High on
  either task (e.g. it fell back to Grok 4.7 High, or to Auto). If it
  fails, note exactly what ran instead and what the picker showed before
  you started — that is the bug to report back.

## Notes

- Keep it small on purpose: the point is to prove which model the parent
  runs, not to burn pool tokens on a big build.
- Task A is the reasoning check (a decision doc with failure modes and
  verification steps, not code). Task B is the repo-scale check (four
  files + tests, run end to end). If Extra High runs the parent on both,
  the fix #30 pin change is doing its job.
- The live smoke test for real project behavior is still skipped since
  Nov 15 — this prompt checks the pin, not the full plugin.
