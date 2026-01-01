---
name: multi-agent-autonomous-workflow
description: Orchestrates multi-agent workflow for feature implementation using specialized subagents. Use when implementing features, epics, or complex multi-story tasks that need analyst, architect, developer, tester, reviewer, and security agents.
---

# Multi-Agent Autonomous Workflow

Orchestrates specialized subagents for **extended autonomous work** (minutes to hours) with minimal human intervention.

## When to Use

- Feature implementation requiring multiple components
- Epic-level requests spanning multiple stories
- Complex multi-story tasks needing coordination
- Any goal requiring iterative development with verification

## Core Principle: Continuous Iteration

This workflow is designed for **extended autonomous execution**. The key principle is:

> **Never stop on first failure. Iterate until success or true blocker.**

```
┌─────────────────────────────────────────────────────────────────┐
│                    AUTONOMOUS EXECUTION MODEL                   │
│                                                                 │
│   ┌─────────┐     ┌──────────┐     ┌──────────┐                │
│   │ Analyze │ ──▶ │ Implement│ ──▶ │ Verify   │                │
│   └─────────┘     └──────────┘     └──────────┘                │
│                         ▲               │                       │
│                         │    FAIL       │                       │
│                         └───────────────┘                       │
│                                                                 │
│   Continue looping until: ALL stories PASS or 3 failures       │
└─────────────────────────────────────────────────────────────────┘
```

## Automatic Platform Detection (REQUIRED - Phase 0)

Before starting any workflow, you MUST detect and load the appropriate platform configuration. Platforms are discovered dynamically - no hardcoded file types.

### Step 1: Discover Available Platforms

Scan the `Workflows/platforms/` directory to find all available platforms:

```
Workflows/platforms/
├── dotnet/platform.json
├── typescript/platform.json
├── python/platform.json      (if exists)
├── go/platform.json          (if exists)
└── {any-new-platform}/platform.json
```

For each subdirectory, read its `platform.json` to get detection criteria.

### Step 2: Read Detection Criteria

Each `platform.json` contains a `detection` section:

```json
{
  "detection": {
    "markers": ["*.sln", "*.csproj"],  // Files/globs to look for
    "matchMode": "any",                 // "any" = at least one, "all" = all required
    "priority": 100,                    // Higher priority wins on conflict
    "description": "Detected by..."     // Human-readable explanation
  }
}
```

### Step 3: Match Against Target Codebase

For each discovered platform:
1. Check if marker files exist in the target project
2. Apply `matchMode`:
   - `"any"`: Platform matches if ANY marker exists
   - `"all"`: Platform matches only if ALL markers exist
3. Collect all matching platforms

### Step 4: Select Best Match

If multiple platforms match, select by highest `priority` value.

If no platforms match:
1. Ask the user which platform to use
2. Or infer from the goal description
3. Fall back to generic commands: `make build`, `make test`

### Step 5: Load Platform Configuration

From the selected `platform.json`, extract:
- `commands` - Build, test, lint commands
- `patterns` - File location patterns
- `conventions` - Naming and formatting conventions
- `antiPatterns` - Code patterns to avoid
- `qualityGates` - Coverage thresholds
- `projectStructure` - Architecture layers
- `skills` - Platform-specific skills to load

### Step 6: Load Platform Skills

For each skill listed in `platform.json.skills[]`:
```
Read: Workflows/platforms/{platform}/skills/{skill}/SKILL.md
```

### Platform Context Template

When invoking ANY subagent, include this context block:

```markdown
## Platform Context
**Platform:** {platform.displayName}
**Build:** {platform.commands.build}
**Test:** {platform.commands.test}
**Lint:** {platform.commands.lint}

**Project Structure:**
{platform.projectStructure.description}

**Conventions:**
- Test naming: {platform.conventions.testNaming}
- Commit format: {platform.conventions.commitFormat}
- Branch format: {platform.conventions.branchFormat}

**Anti-Patterns to Avoid:**
{List from platform.antiPatterns}
```

## Architecture

```
ORCHESTRATOR (You) ─── Drives workflow to completion
    │
    ├── analyst     → Requirements & user stories (Phase 1)
    ├── architect   → Technical design (Phase 1)
    │
    ├── developer   → Implementation ───────┐
    ├── tester      → Verification ─────────┼── Iteration Loop
    ├── reviewer    → Code review ──────────┘
    │
    ├── security    → Security audit (if flagged)
    └── devops      → Infrastructure (Phase 3)
```

## Workflow Phases

### Phase 1: Analysis (Run Once)
1. Initialize workflow state: `python .claude/core/state.py init "goal"`
2. Invoke `analyst` subagent with the goal
3. Add stories to state: `python .claude/core/state.py add-story "title"`
4. Invoke `architect` for technical design
5. **Gate G1:** Verify design complete before proceeding

### Phase 2: Story Execution Loop (ITERATE FOR EACH STORY)

```python
for story in stories:
    iteration = 0
    while story.status != 'completed' and iteration < 3:
        iteration += 1

        # Development
        result = invoke_developer(story, previous_failures)
        if result.build_failed:
            continue  # Retry with error context

        # Verification
        test_result = invoke_tester(story, result.files)
        if test_result == 'FAIL':
            previous_failures.append(test_result.issues)
            continue  # Loop back to developer

        # Review
        review = invoke_reviewer(story, result.files)
        if review == 'CHANGES_REQUESTED':
            previous_failures.append(review.changes)
            continue  # Loop back to developer

        # Security (if needed)
        if story.is_security_sensitive:
            security = invoke_security(story, result.files)
            if security == 'NEEDS_REMEDIATION':
                previous_failures.append(security.issues)
                continue  # Loop back to developer

        story.status = 'completed'
        update_state(story)

    if story.status != 'completed':
        escalate_blocker(story)
```

### Phase 3: Completion
1. Verify all stories completed: `python .claude/core/state.py status`
2. Invoke `devops` if deployment needed
3. **Create Pull Request** (REQUIRED):
   ```bash
   # Ensure all changes committed
   git status

   # Push branch to remote
   git push -u origin HEAD

   # Create PR with summary of all completed stories
   gh pr create --title "[Feature] <Goal Summary>" --body "$(cat <<'EOF'
   ## Summary
   <Brief description of what was implemented>

   ## Stories Implemented
   - S1: <title>
   - S2: <title>
   ...

   ## Testing
   - All tests passing
   - Coverage thresholds met

   ## Verification
   - [x] Code review approved
   - [x] Security review passed (if applicable)
   - [x] All acceptance criteria met

   ---
   Generated with [Claude Code](https://claude.com/claude-code)
   EOF
   )"
   ```
4. Complete workflow: `python .claude/core/state.py complete`
5. Generate final summary with PR URL

**Important:** Always create a PR at workflow completion. If `gh` CLI fails, verify installation (`gh --version`) and authentication (`gh auth status`).

## Quality Gates

| Gate | When | Check | On Fail |
|------|------|-------|---------|
| G1 | Before dev | Design complete, AC clear | Clarify with analyst |
| G2 | After dev | Build passes, tests pass | Retry developer |
| G3 | After test | Coverage threshold met | Add tests, retry |
| G4 | If security | Security scan passes | Remediate, retry |

### Platform-Specific Build/Test

Use commands from the detected platform.json:

```
Build: {platform.commands.build}
Test:  {platform.commands.test}
Lint:  {platform.commands.lint}
```

The platform is auto-detected in Phase 0. All subagents receive platform context with the correct commands.

## Fail-First Verification Pattern

Per Anthropic best practices, stories must pass ALL verification checks before completion:

```
Story Status Flow:
pending → in_progress → testing → review → verified → completed
                ↑                              │
                └──────── (on failure) ────────┘

Verification Checks (all must pass):
├── testsPass      - All tests pass
├── coverageMet    - Coverage threshold met
├── reviewApproved - Code review approved
└── securityCleared - Security review passed (if security-sensitive)
```

Stories cannot be marked `completed` until reaching `verified` status with all checks passed.

## Coverage Thresholds by Story Size

Thresholds are defined in `platform.json.qualityGates.coverageThresholds`:

| Size | Default | Source |
|------|---------|--------|
| S | 70% | `{platform.qualityGates.coverageThresholds.S}` |
| M | 80% | `{platform.qualityGates.coverageThresholds.M}` |
| L | 85% | `{platform.qualityGates.coverageThresholds.L}` |
| XL | 90% | `{platform.qualityGates.coverageThresholds.XL}` |

## Iteration Control

### Maximum Retries
- **Per story:** 3 complete iterations (dev→test→review)
- **Per build failure:** 3 attempts within developer
- **Per test failure:** Loop back to developer (counts toward story iteration)

### Context Passing on Retry
When retrying, ALWAYS pass:
1. **What was attempted:** Summary of implementation
2. **What failed:** Specific error/issue with file:line reference
3. **What to fix:** Actionable instructions

### Escalation Triggers
| Trigger | Action |
|---------|--------|
| 5 stories completed | Human checkpoint review |
| 3 failed iterations | Escalate blocker |
| Security vulnerability | Immediate escalation |
| Unclear requirements | Clarification needed |

## Extended Execution Strategies

### For 30+ Minute Runs
1. **State persistence:** Update state after each story completion
2. **Progress reports:** Generate report every 3 stories or 60 minutes
3. **Context management:** Summarize completed stories, drop details

### For 1+ Hour Runs
1. **Checkpoint reviews:** Pause at 5-story intervals for human review
2. **Lessons learned:** Update `.claude/lessons-learned.md` with insights
3. **Rollback capability:** Track file changes per story in state

### Context Efficiency
For long sessions, maintain a **working context** that includes:
- Current story only (full details)
- Completed stories (titles + key decisions only)
- Active architectural decisions
- Current blockers

Drop from context:
- Implementation details of completed stories
- Full test output (keep summary only)
- Superseded design decisions

## Commands

- `/workflow [goal]` - Start full workflow with autonomous execution
- `/status` - Check current progress and metrics
- `/implement [story]` - Implement single story with iteration loop
- `/review [files]` - Run code review on specific files

## State Management

```bash
# Initialize or resume workflow
python .claude/core/state.py init "Goal description"

# Session recovery (run at start of each session)
python .claude/core/state.py recover

# Track stories (use --security for auth/payments/user data)
python .claude/core/state.py add-story "Story title" --size M
python .claude/core/state.py add-story "Auth story" --size L --security

# Update story status
python .claude/core/state.py update-story S1 in_progress
python .claude/core/state.py update-story S1 testing
python .claude/core/state.py update-story S1 review
python .claude/core/state.py update-story S1 completed

# Verification checks (fail-first pattern)
python .claude/core/state.py verify S1 testsPass --passed
python .claude/core/state.py verify S1 coverageMet --passed --details "85%"
python .claude/core/state.py verify S1 reviewApproved --passed
python .claude/core/state.py verify S1 securityCleared --passed
python .claude/core/state.py verify-status S1

# Monitor progress
python .claude/core/state.py status
python .claude/core/state.py progress --lines 20

# Complete
python .claude/core/state.py complete
```

For detailed reference, see [workflow-reference.md](workflow-reference.md).
