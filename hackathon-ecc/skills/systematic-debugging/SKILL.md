---
name: systematic-debugging
description: Use when a bug's root cause is unknown and no more specific debugging skill applies — after symptom inspection rules out an agent failure and broken-button state bugs (click-path-audit). Debugging order — `browser-qa` detects deployed-UI failures and `systematic-debugging` diagnoses them. Requires finding root cause before attempting any fixes. Do NOT use when the user asks to fix a bug through the fix pipeline — orch-fix-defect owns that; use this skill only to find an unknown root cause.
---

# Systematic Debugging

## Overview

Random fixes waste time and create new bugs. Always find root cause before fixing.

**Core principle:** NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.

**Violating the letter of this process is violating the spirit of debugging.**

### Debugging order

**Debugging order:** start with symptom inspection; a button that does nothing goes to `click-path-audit` next; everything else with an unknown root cause goes to `systematic-debugging` (which finds the other bug types). `browser-qa` detects deployed-UI failures; `systematic-debugging` diagnoses them.

Handoff: `browser-qa` hands a detected deployed-UI failure to this skill with the URL, repro steps, console/network evidence, and screenshots; this skill diagnoses the root cause. A button that does nothing goes to `click-path-audit` first — broken-button state bugs are its job, not this skill's.

## The Four Phases

### Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

1. **Read Error Messages Carefully**
   - Don't skip past errors or warnings
   - Read stack traces completely
   - Note line numbers, file paths, error codes

2. **Reproduce Consistently**
   - Can you trigger it reliably?
   - What are the exact steps?
   - Does it happen every time?

3. **Check Recent Changes**
   - What changed that could cause this?
   - Git diff, recent commits
   - New dependencies, config changes

4. **Gather Evidence in Multi-Component Systems**

   For EACH component boundary:
   - Log what data enters component
   - Log what data exits component
   - Verify environment/config propagation

### Phase 2: Pattern Analysis

1. **Find Working Examples**
   - Locate similar working code
   - What works that's similar to what's broken?

2. **Compare Against References**
   - Read reference implementation COMPLETELY
   - Don't skim - understand fully

3. **Identify Differences**
   - What's different between working and broken?
   - List every difference

### Phase 3: Hypothesis and Testing

1. **Form Single Hypothesis**
   - State clearly: "I think X is the root cause because Y"

2. **Test Minimally**
   - Make SMALLEST possible change
   - One variable at a time

3. **Verify Before Continuing**
   - Did it work? Yes → Phase 4
   - Didn't work? NEW hypothesis

### Phase 4: Implementation

1. **Create Failing Test Case**
   - Simplest possible reproduction
   - MUST have before fixing

2. **Implement Single Fix**
   - Address root cause
   - ONE change at a time

3. **Verify Fix**
   - Test passes now?
   - No other tests broken?

4. **If 3+ Fixes Failed: Question Architecture**
   - Pattern indicates architectural problem
   - STOP and discuss with human partner — except during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature, where you state the assumption, pick the safe/reversible option, and proceed without waiting; never stop for a human decision mid-build. Record the architectural concern in the final report instead.

## Red Flags - STOP and Follow Process

- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "It's probably X, let me fix that"
- **"One more fix attempt" (when already tried 2+)**
- Each fix reveals new problem in different place

**ALL mean: Return to Phase 1.**

## Quick Reference

| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| **1. Root Cause** | Read errors, reproduce, check changes | Understand WHAT and WHY |
| **2. Pattern** | Find working examples, compare | Identify differences |
| **3. Hypothesis** | Form theory, test minimally | Confirmed or new hypothesis |
| **4. Implementation** | Create test, fix, verify | Bug resolved, tests pass |

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Issue is simple" | Simple issues have root causes too |
| "Emergency, no time" | Systematic is FASTER than guess-and-check |
| "Just try this first" | First fix sets pattern - do it right |
| "I'll write test after" | Untested fixes don't stick |
| "I see the problem" | Symptoms ≠ root cause |

## When 3+ Fixes Failed

Question the architecture:
- Is this pattern fundamentally sound?
- Are we "sticking with it through sheer inertia"?
- Should we refactor architecture vs. continue fixing?

**Discuss with human partner before more fixes — except during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature, where you pick the safe/reversible option, record it in the final report, and move on; never stop for a human decision mid-build.**
