---
description: Implement a specific user story using TDD with the developer subagent
argument-hint: [story title or description]
allowed-tools: Read, Glob, Grep, Edit, Write, Bash, Task
---

# Implement Story

Implement this story using iterative development and verification:

**Story:** $ARGUMENTS

## CRITICAL: Iterative Implementation Loop

This command implements a **self-correcting loop** that iterates between development and testing until the story passes all verification. Do NOT stop after a single failure.

## Implementation Loop (ITERATE UNTIL PASS)

```
iteration_count = 0
MAX_ITERATIONS = 3

WHILE iteration_count < MAX_ITERATIONS:

    iteration_count += 1

    ┌─────────────────────────────────────────────────────────────┐
    │ STEP 1: DEVELOPER                                           │
    │                                                             │
    │ Invoke `developer` subagent with:                           │
    │ - Story: "$ARGUMENTS"                                       │
    │ - Iteration: {iteration_count}/3                            │
    │ - Previous failures: [list from prior iterations]           │
    │ - Fix instructions: [specific issues to address]            │
    │                                                             │
    │ IF build/tests FAIL within developer:                       │
    │   → Developer should self-correct (up to 3 internal tries)  │
    │   → If still failing, return with error details             │
    └─────────────────────────────────────────────────────────────┘
                              │
                              ▼
    ┌─────────────────────────────────────────────────────────────┐
    │ STEP 2: TESTER VERIFICATION                                 │
    │                                                             │
    │ Invoke `tester` subagent with:                              │
    │ - Story: "$ARGUMENTS"                                       │
    │ - Implementation summary from developer                      │
    │ - Files changed: [list]                                     │
    │                                                             │
    │ Parse tester response:                                      │
    │ - If PASS → proceed to STEP 3                               │
    │ - If FAIL → extract failure details, loop to STEP 1         │
    └─────────────────────────────────────────────────────────────┘
                              │
                              ▼
    ┌─────────────────────────────────────────────────────────────┐
    │ STEP 3: REVIEWER                                            │
    │                                                             │
    │ Invoke `reviewer` subagent with:                            │
    │ - Story: "$ARGUMENTS"                                       │
    │ - Files changed: [list]                                     │
    │                                                             │
    │ Parse reviewer response:                                    │
    │ - If APPROVED → proceed to STEP 4                           │
    │ - If CHANGES_REQUESTED → extract changes, loop to STEP 1    │
    └─────────────────────────────────────────────────────────────┘
                              │
                              ▼
    ┌─────────────────────────────────────────────────────────────┐
    │ STEP 4: SECURITY (if applicable)                            │
    │                                                             │
    │ IF story involves auth, payments, PII, or external input:   │
    │   Invoke `security` subagent                                │
    │                                                             │
    │   - If SECURE → COMPLETE                                    │
    │   - If NEEDS_REMEDIATION → loop to STEP 1                   │
    └─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                         [ COMPLETE ]
```

## Passing Context Between Iterations

When looping back to developer, ALWAYS include:

```markdown
## Retry Context for Developer

**Story:** $ARGUMENTS
**Iteration:** 2/3 (or 3/3)

### Previous Attempt Summary
[Brief summary of what was implemented]

### Failure Details
**Source:** Tester/Reviewer/Security
**Issues Found:**
1. [Specific issue with file:line reference]
2. [Another issue]

### Required Fixes
1. [Specific action to take]
2. [Another action]

### Files to Focus On
- `path/to/file.cs` - [what needs changing]
```

## Escalation (After 3 Iterations)

If still failing after 3 complete iterations:

1. **Analyze root cause:**
   - Is the acceptance criteria unclear?
   - Is the technical approach wrong?
   - Is there a missing dependency?

2. **Consider architectural redesign:**
   - Invoke `architect` to reconsider the approach
   - Split story into smaller pieces if too complex

3. **Escalate to human with:**
   - All 3 attempt summaries
   - Specific blocking issue
   - Recommended path forward

## Expected Outcomes (Per Iteration)

| Check | How to Verify |
|-------|---------------|
| Build passes | `dotnet build` returns 0 |
| Tests pass | `dotnet test` returns 0 |
| Coverage adequate | Tester reports PASS |
| Code quality | Reviewer returns APPROVED |
| Security (if flagged) | Security returns SECURE |

## Tracking Progress

Update workflow state after completion:
```bash
python .claude/hooks/state.py update-story S{n} completed
```

Begin by gathering context about the story and starting the implementation loop.
