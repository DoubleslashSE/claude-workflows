---
name: multi-agent-autonomous-workflow
description: Orchestrates multi-agent workflow for feature implementation using specialized subagents. Use when implementing features, epics, or complex multi-story tasks that need analyst, architect, developer, tester, reviewer, and security agents.
---

# Multi-Agent Autonomous Workflow

Orchestrates specialized subagents for **extended autonomous work** (minutes to hours) with minimal human intervention.

## Execution Model: Continuous Until Complete

This workflow is designed for **long-running autonomous execution**. Like the Ralph Wiggum plugin pattern:

> **Never exit until the goal is complete or a true blocker is encountered.**
> **Iterate continuously. Use previous failures as context for next attempt.**
> **State persists on disk. Each iteration sees all previous work.**

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     LONG-RUNNING EXECUTION MODEL                         │
│                                                                          │
│   ┌──────────────────────────────────────────────────────────────────┐  │
│   │                    OUTER LOOP: PHASES                             │  │
│   │                                                                   │  │
│   │   Phase 0 ──▶ Phase 1 ──▶ Phase 2 ──▶ Phase 3 ──▶ COMPLETE       │  │
│   │   (Setup)    (Analyze)   (Execute)   (Finalize)                   │  │
│   │                              │                                    │  │
│   │              ┌───────────────┴───────────────┐                    │  │
│   │              │  MIDDLE LOOP: STORIES         │                    │  │
│   │              │                               │                    │  │
│   │              │  for each story:              │                    │  │
│   │              │    ┌────────────────────┐     │                    │  │
│   │              │    │ INNER LOOP: ITERATE│     │                    │  │
│   │              │    │ until verified     │     │                    │  │
│   │              │    │ or max retries     │     │                    │  │
│   │              │    └────────────────────┘     │                    │  │
│   │              └───────────────────────────────┘                    │  │
│   └──────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│   COMPLETION MARKER: All stories verified + PR created                   │
└─────────────────────────────────────────────────────────────────────────┘
```

## Phase 0: Setup & Platform Detection

Before any work, set up the execution context. **This phase produces visible output.**

### Step 0.1: Session Recovery Check

**ALWAYS run at the start of every session:**

```bash
# Check if resuming existing workflow
python .claude/core/state.py recover

# If workflow exists, read current state
python .claude/core/state.py status
```

If resuming, skip to the appropriate phase/story based on state.

### Step 0.2: Discover Available Platforms

Scan `Workflows/platforms/` for all subdirectories containing `platform.json`.

**Output the discovery:**

```markdown
## Platform Discovery

Scanning Workflows/platforms/ for available platforms...

| Platform | Markers | Match Mode | Priority |
|----------|---------|------------|----------|
| dotnet | *.sln, *.csproj | any | 100 |
| typescript | package.json, tsconfig.json | all | 90 |

Found {n} platform configurations.
```

### Step 0.3: Match Platform to Codebase

Check each platform's markers against the target project.

**Output the matching process:**

```markdown
## Platform Detection

Scanning codebase for platform markers...

| Platform | Markers Found | Match Result |
|----------|---------------|--------------|
| dotnet | MyApp.sln, MyApp.csproj | MATCH |
| typescript | (none) | NO MATCH |

**Selected Platform:** dotnet (priority: 100)
**Reason:** Found *.sln file in project root
```

### Step 0.4: Load Platform Configuration

From selected `platform.json`, extract and cache configuration.

**Output the loaded configuration:**

```markdown
## Platform Configuration Loaded

**Platform:** .NET with Clean Architecture (v1.0.0)

### Commands
| Action | Command |
|--------|---------|
| Build | `dotnet build` |
| Test | `dotnet test` |
| Lint | `dotnet format --verify-no-changes` |
| Coverage | `dotnet test /p:CollectCoverage=true` |

### Project Structure
Clean Architecture with CQRS

| Layer | Path | Contains |
|-------|------|----------|
| Core | src/Core | Entities, ValueObjects, Interfaces |
| Application | src/Application | Commands, Queries, Handlers |
| Infrastructure | src/Infrastructure | Persistence, Services |
| Api | src/Api | Controllers, Middleware |

### Skills Loaded
- dotnet-clean-architecture
- tdd-workflow

### Conventions
- Test naming: `{Method}_{Scenario}_{ExpectedResult}`
- Commit format: `type: description`
- Branch format: `feature/{storyId}-{description}`

---
Platform detection complete. Proceeding with workflow.
```

### Step 0.5: Load Platform Skills

For each skill in `platform.json.skills[]`, read the skill file:

```
Read: Workflows/platforms/{platform}/skills/{skill}/SKILL.md
```

The loaded skills provide platform-specific patterns and best practices that guide implementation.

---

## Phase 1: Analysis & Planning

### Step 1.1: Pre-Analysis Clarification (REQUIRED)

**Before invoking the analyst**, ask clarifying questions if the goal is ambiguous:

```markdown
## Clarification Needed

Before I begin analysis, I need to clarify a few things:

1. **Scope:** [Question about boundaries/scope]
2. **Constraints:** [Question about technical constraints]
3. **Priority:** [Question about what's most important]

Please answer these questions, or say "proceed with your best judgment."
```

**When to ask:**
- Goal mentions multiple features without priority
- Technical approach is unclear
- Integration points are ambiguous
- User mentioned but didn't specify requirements

**When to skip:**
- Goal is very specific and clear
- Requirements are well-defined
- User has provided detailed specifications

### Step 1.2: Initialize Workflow State

```bash
python .claude/core/state.py init "Goal description"
```

### Step 1.3: Invoke Analyst Subagent

```markdown
## Task for Analyst

{PLATFORM CONTEXT BLOCK}

**Goal:** {User's goal}

Break this down into user stories with acceptance criteria.
```

Parse output and add stories to state:
```bash
python .claude/core/state.py add-story "Story 1 title" --size M
python .claude/core/state.py add-story "Story 2 title" --size L --security
```

### Step 1.4: Pre-Plan Clarification (REQUIRED)

**Before invoking the architect**, review stories and ask:

```markdown
## Design Clarification

I've identified these stories:
1. {Story 1}
2. {Story 2}
...

Before I design the technical approach, please confirm:
1. **Priority order:** Is this the right order? Any changes?
2. **Technical preferences:** Any specific patterns/libraries to use or avoid?
3. **Existing code:** Any areas I should be careful modifying?

Say "proceed" to continue with my proposed approach, or provide guidance.
```

### Step 1.5: Invoke Architect Subagent

```markdown
## Task for Architect

{PLATFORM CONTEXT BLOCK}

**Stories:** {List from analyst}

Create technical design following platform.projectStructure.
```

### Step 1.6: Gate G1 - Verify Design Complete

Check:
- [ ] All stories have technical design
- [ ] File changes identified per story
- [ ] No open questions blocking implementation

If not complete, iterate with architect.

---

## Phase 2: Story Execution Loop

This is the main execution loop. **Continue until ALL stories are completed.**

**CRITICAL: Every iteration MUST run build and tests before exiting the loop.**

```python
# MIDDLE LOOP: Iterate over stories
while get_incomplete_stories():
    story = get_next_incomplete_story()

    # INNER LOOP: Iterate until story verified or max retries
    iteration = 0
    previous_failures = []

    while story.status != 'completed' and iteration < MAX_RETRIES:
        iteration += 1

        # === DEVELOP ===
        update_status(story, 'in_progress')
        dev_result = invoke_developer(story, iteration, previous_failures)

        # === MANDATORY BUILD VERIFICATION ===
        build_result = run_platform_command('build')  # e.g., dotnet build / npm run build
        if build_result.failed:
            previous_failures.append(f"Build failed: {build_result.error}")
            continue  # Retry development - DO NOT EXIT LOOP

        # === MANDATORY TEST VERIFICATION ===
        test_result = run_platform_command('test')  # e.g., dotnet test / npm test
        if test_result.failed:
            previous_failures.append(f"Tests failed: {test_result.error}")
            continue  # Retry development - DO NOT EXIT LOOP

        # === TESTER AGENT VERIFICATION ===
        update_status(story, 'testing')
        tester_result = invoke_tester(story, dev_result.files)

        if tester_result == 'FAIL':
            previous_failures.append(tester_result.issues)
            continue  # Loop back to developer

        mark_verification(story, 'testsPass', True)
        mark_verification(story, 'coverageMet', tester_result.coverage_ok)

        # === REVIEW ===
        update_status(story, 'review')
        review_result = invoke_reviewer(story, dev_result.files)

        if review_result == 'CHANGES_REQUESTED':
            previous_failures.append(review_result.changes)
            continue  # Loop back to developer

        mark_verification(story, 'reviewApproved', True)

        # === SECURITY (if flagged) ===
        if story.is_security_sensitive:
            security_result = invoke_security(story, dev_result.files)

            if security_result == 'NEEDS_REMEDIATION':
                previous_failures.append(security_result.issues)
                continue  # Loop back to developer

            mark_verification(story, 'securityCleared', True)

        # === FINAL VERIFICATION BEFORE COMPLETING STORY ===
        final_build = run_platform_command('build')
        final_test = run_platform_command('test')

        if final_build.failed or final_test.failed:
            previous_failures.append("Final verification failed")
            continue  # DO NOT COMPLETE - retry

        # === STORY COMPLETE ===
        update_status(story, 'completed')
        commit_story_changes(story)
        log_progress(f"Story {story.id} completed in {iteration} iterations")

    if story.status != 'completed':
        # Max retries exceeded - escalate
        escalate_blocker(story, previous_failures)
```

### Mandatory Verification Commands

**Before exiting ANY loop iteration, run these platform commands:**

```bash
# Using platform.json commands
{platform.commands.build}    # Must pass
{platform.commands.test}     # Must pass
```

**Example for .NET:**
```bash
dotnet build
dotnet test
```

**Example for TypeScript:**
```bash
npm run build
npm test
```

**If either command fails, DO NOT:**
- Exit the inner loop
- Mark the story as completed
- Proceed to the next story
- Create a PR

**Instead:**
- Log the failure
- Add to `previous_failures` context
- Retry with the developer agent

### Retry Context Template

When retrying development, ALWAYS include:

```markdown
## Retry Context

**Story:** {story.title}
**Iteration:** {n}/3
**Previous Attempts:** {n-1}

### What Failed:
{List each failure with file:line references}

### What To Fix:
{Specific actionable instructions based on failures}

### Files Changed So Far:
{List of files modified in previous iterations}
```

### Progress Checkpoints

Every **3 completed stories** OR **60 minutes**, generate a progress report:

```markdown
## Progress Report

**Workflow:** {goal}
**Runtime:** {elapsed_time}
**Stories:** {completed}/{total} completed

### Completed Stories:
- S1: {title} - {iterations} iterations
- S2: {title} - {iterations} iterations
- S3: {title} - {iterations} iterations

### Current Story:
- {title} - Iteration {n}, Status: {status}

### Blockers:
- {any blockers or "None"}

### Next:
- Continue with {next_story}
```

---

## Phase 3: Completion & PR Creation

### Step 3.1: Verify All Stories Complete

```bash
python .claude/core/state.py status
```

All stories must have status `completed` with all verification checks passed.

### Step 3.2: Final Build & Test Verification (REQUIRED)

**Before creating a PR, run a complete build and test cycle:**

```bash
# Run full build
{platform.commands.build}

# Run all tests
{platform.commands.test}

# Run linting (if available)
{platform.commands.lint}
```

**Example for .NET:**
```bash
dotnet build
dotnet test
dotnet format --verify-no-changes
```

**Example for TypeScript:**
```bash
npm run build
npm test
npm run lint
```

**Output verification results:**

```markdown
## Pre-PR Verification

| Check | Command | Result |
|-------|---------|--------|
| Build | `dotnet build` | ✅ PASS |
| Tests | `dotnet test` | ✅ PASS (47 tests) |
| Lint | `dotnet format --verify-no-changes` | ✅ PASS |

All verification checks passed. Proceeding with PR creation.
```

**If ANY check fails:**
- DO NOT create the PR
- Return to Phase 2 to fix the issues
- Re-run verification after fixes

### Step 3.3: Invoke DevOps (if needed)

If deployment configuration is required:
```markdown
## Task for DevOps

{PLATFORM CONTEXT BLOCK}

Create/update deployment configuration for implemented features.
```

### Step 3.4: Create Pull Request (REQUIRED)

```bash
# Ensure clean working state
git status

# Push branch
git push -u origin HEAD

# Create PR
gh pr create --title "[Feature] {Goal Summary}" --body "$(cat <<'EOF'
## Summary
{Brief description of implementation}

## Stories Implemented
{For each story:}
- {story.id}: {story.title}

## Changes
{Key files changed grouped by feature}

## Testing
- All {test_count} tests passing
- Coverage thresholds met

## Pre-PR Verification
- [x] Build passes
- [x] All tests pass
- [x] Lint checks pass

## Agent Verification
- [x] Code review approved by reviewer agent
- [x] Security review passed (if applicable)
- [x] All acceptance criteria verified by tester agent

## Workflow Metrics
- **Runtime:** {total_time}
- **Stories:** {story_count}
- **Total iterations:** {total_iterations}

---
Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

### Step 3.5: Complete Workflow

```bash
python .claude/core/state.py complete
```

### Step 3.6: Output Completion Marker

```markdown
## WORKFLOW_COMPLETE

**Goal:** {goal}
**Status:** SUCCESS
**PR:** {pr_url}
**Runtime:** {total_time}
**Stories:** {completed}/{total}

All stories verified. Pull request created. Workflow complete.
```

---

## Architecture

```
ORCHESTRATOR (You) ─── Drives workflow through all phases
    │
    │   Phase 1
    ├── analyst     → Requirements & user stories
    ├── architect   → Technical design
    │
    │   Phase 2 (Loop)
    ├── developer   → Implementation (TDD)
    ├── tester      → Verification
    ├── reviewer    → Code review
    ├── security    → Security audit (if flagged)
    │
    │   Phase 3
    └── devops      → Infrastructure & deployment
```

---

## State Management

### Persistence Commands

```bash
# Initialize
python .claude/core/state.py init "Goal"

# Session recovery (ALWAYS run at session start)
python .claude/core/state.py recover

# Story management
python .claude/core/state.py add-story "Title" --size M [--security]
python .claude/core/state.py update-story S1 in_progress
python .claude/core/state.py update-story S1 testing
python .claude/core/state.py update-story S1 review
python .claude/core/state.py update-story S1 completed

# Verification checks
python .claude/core/state.py verify S1 testsPass --passed
python .claude/core/state.py verify S1 coverageMet --passed --details "85%"
python .claude/core/state.py verify S1 reviewApproved --passed
python .claude/core/state.py verify S1 securityCleared --passed

# Progress tracking
python .claude/core/state.py status
python .claude/core/state.py progress --lines 20

# Completion
python .claude/core/state.py complete
```

### State File Location

State persists in `workflow-state.json`. This enables:
- Session recovery after interruptions
- Progress tracking across long runs
- Rollback capability per story

---

## Long-Running Execution Strategies

### For Runs Under 1 Hour
- Update state after each story completion
- Generate progress report every 3 stories

### For Runs 1-4 Hours
- Update state after each phase transition
- Generate progress report every 30 minutes
- Checkpoint review at 5-story intervals
- Update lessons-learned.md with insights

### For Runs 4+ Hours
- Aggressive context management (drop completed story details)
- State sync every 15 minutes
- Consider session handoff at natural breakpoints
- Keep only current story + summary of completed work in context

### Context Efficiency

Maintain a **working context** that includes:
- Current story (full details)
- Completed stories (ID + title + key decisions only)
- Active architectural decisions
- Current blockers

Drop from context:
- Full implementation details of completed stories
- Raw test output (keep summary only)
- Superseded design decisions

---

## Quality Gates

| Gate | When | Check | On Fail |
|------|------|-------|---------|
| G1 | Before dev | Design complete, AC clear | Clarify with analyst/architect |
| G2 | After dev | `{platform.commands.build}` passes | Retry developer with build error context |
| G3 | After build | `{platform.commands.test}` passes | Retry developer with test failure context |
| G4 | After test | Coverage threshold met | Add tests, retry |
| G5 | Before story complete | Final build + test verification | DO NOT complete story, retry |
| G6 | If security | Security scan passes | Remediate, retry |
| G7 | Before PR | Full build + test + lint passes | DO NOT create PR, return to Phase 2 |

### Gate Verification Commands

```bash
# G2: Build verification
{platform.commands.build}

# G3: Test verification
{platform.commands.test}

# G5: Final story verification (before marking complete)
{platform.commands.build} && {platform.commands.test}

# G7: Pre-PR verification (all checks)
{platform.commands.build} && {platform.commands.test} && {platform.commands.lint}
```

**IMPORTANT:** Gates G2, G3, G5, and G7 are MANDATORY. The workflow MUST NOT proceed if these gates fail.

---

## Clarifying Question Guidelines

### When to Ask (Pre-Analysis)
- Goal is vague or multi-part without priority
- Technical constraints not specified
- Integration requirements unclear
- User data handling involved but not specified

### When to Ask (Pre-Plan)
- Multiple valid technical approaches exist
- Story order could significantly impact development
- Dependencies between stories are complex
- User has shown strong opinions about technology choices

### How to Ask
1. Be specific - ask about concrete decisions
2. Offer options when possible
3. Provide your recommendation with rationale
4. Always allow "proceed with your judgment" as an option

### When NOT to Ask
- Requirements are explicit and complete
- Standard patterns clearly apply
- Technical choice is obvious from codebase
- User explicitly requested autonomous execution

---

## Escalation Triggers

| Trigger | Action |
|---------|--------|
| 3 failed iterations on same story | Log blocker, ask user for guidance |
| Security vulnerability found | Immediate escalation |
| 5 stories completed | Optional checkpoint (can be skipped if autonomous) |
| Unclear requirements blocking progress | Ask clarifying question |
| External dependency unavailable | Log and escalate |

---

## Commands Reference

- `/workflow [goal]` - Start full autonomous workflow
- `/status` - Check current progress
- `/implement [story]` - Implement single story with iteration loop
- `/review [files]` - Run code review

For detailed invocation patterns, see [workflow-reference.md](workflow-reference.md).
