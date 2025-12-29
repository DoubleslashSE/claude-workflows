# Multi-Agent Autonomous Workflow

A hierarchical workflow system using true subagents for extended autonomous work with minimal human intervention.

## Activation

Use this workflow for feature implementation, epic-level requests, or complex multi-story tasks.

```
Use the multi-agent workflow to: [describe goal]
```

---

## Architecture Overview

```
                    ┌─────────────────┐
                    │  ORCHESTRATOR   │
                    │  (You/Main)     │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│   ANALYST     │    │   ARCHITECT   │    │    DEVOPS     │
│  (Task tool)  │    │  (Task tool)  │    │  (Task tool)  │
└───────────────┘    └───────────────┘    └───────────────┘
        │                    │                    │
        ▼                    ▼                    ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│   DEVELOPER   │    │   TESTER      │    │   REVIEWER    │
│  (Task tool)  │    │  (Task tool)  │    │  (Task tool)  │
└───────────────┘    └───────────────┘    └───────────────┘
```

**Key Difference:** Each agent is spawned via the `Task` tool as an actual subagent with:
- Isolated context (won't exhaust main context window)
- Specific tool permissions per role
- Focused responsibility

---

## Orchestrator Role (Main Agent)

As the orchestrator, you:
1. Receive the goal from the human
2. Initialize workflow state
3. Delegate to specialized agents via Task tool
4. Track progress using workflow state
5. Handle escalations and blockers
6. Validate goal completion

### Before Starting

1. Initialize workflow state:
```bash
python .claude/hooks/state.py init "Goal description"
```

2. Check status anytime:
```bash
python .claude/hooks/state.py status
```

---

## Agent Delegation Patterns

### Spawn ANALYST Agent

Use when: Starting a new goal, need requirements clarification

```
Task({
  subagent_type: "Explore",
  prompt: `
    Read the analyst agent instructions from .claude/agents/analyst.md

    ## Goal to Analyze
    [Insert goal here]

    ## Codebase Context
    This is a .NET 10 Clean Architecture project with CQRS pattern.
    See CLAUDE.md for architecture details.

    ## Expected Output
    - User stories with acceptance criteria
    - Prioritized backlog
    - Open questions (if any)

    Return your analysis in the format specified in the agent instructions.
  `
})
```

### Spawn ARCHITECT Agent

Use when: Stories defined, need technical design

```
Task({
  subagent_type: "Plan",
  prompt: `
    Read the architect agent instructions from .claude/agents/architect.md

    ## Stories to Design For
    [Insert stories from analyst]

    ## Technical Constraints
    - Follow Clean Architecture (Core -> Application -> Infrastructure -> Api)
    - Use CQRS pattern (Commands/Queries with MediatR)
    - FluentValidation for validation
    - See CLAUDE.md for patterns

    ## Expected Output
    - Technical approach
    - Key decisions with rationale
    - Component design
    - File change list

    Return your design in the format specified in the agent instructions.
  `
})
```

### Spawn DEVELOPER Agent

Use when: Design ready, implementing a story

```
Task({
  subagent_type: "general-purpose",
  prompt: `
    Read the developer agent instructions from .claude/agents/developer.md

    ## Story to Implement
    Title: [Story title]
    Acceptance Criteria:
    - [AC1]
    - [AC2]

    ## Technical Design
    [Insert relevant design from architect]

    ## Instructions
    1. Follow TDD: Write failing test first, then implement
    2. Follow existing patterns in the codebase
    3. Commit after each working increment
    4. Report any blockers immediately

    Return your implementation log in the format specified in the agent instructions.
  `
})
```

### Spawn TESTER Agent

Use when: Story implemented, needs verification

```
Task({
  subagent_type: "general-purpose",
  prompt: `
    Read the tester agent instructions from .claude/agents/tester.md

    ## Story to Verify
    Title: [Story title]
    Acceptance Criteria:
    - [AC1]
    - [AC2]

    ## Implementation Summary
    [What was implemented by developer]

    ## Instructions
    1. Verify each acceptance criterion
    2. Check edge cases
    3. Run all tests
    4. Report PASS or FAIL with details

    Return your test report in the format specified in the agent instructions.
  `
})
```

### Spawn REVIEWER Agent

Use when: Tests pass, needs code review

```
Task({
  subagent_type: "code-security-reviewer",
  prompt: `
    Read the reviewer agent instructions from .claude/agents/reviewer.md

    ## Story to Review
    Title: [Story title]

    ## Files Changed
    [List from developer]

    ## Instructions
    1. Check Clean Architecture compliance
    2. Review for security issues
    3. Verify code quality
    4. Return APPROVED or CHANGES REQUESTED

    Return your review in the format specified in the agent instructions.
  `
})
```

### Spawn DEVOPS Agent

Use when: Infrastructure setup needed, deployment tasks

```
Task({
  subagent_type: "devops-engineer",
  prompt: `
    Read the devops agent instructions from .claude/agents/devops.md

    ## Task
    [Infrastructure task description]

    ## Context
    - Platform: Railway
    - CI/CD: GitHub Actions
    - Registry: GHCR

    Return your infrastructure changes in the format specified in the agent instructions.
  `
})
```

---

## Workflow Phases

### Phase 1: Initiation
```
1. ORCHESTRATOR receives goal
2. Initialize workflow state
3. Spawn ANALYST -> Get stories
4. Spawn ARCHITECT -> Get design
5. Spawn DEVOPS if infrastructure needed
6. Update state with stories
```

### Phase 2: Story Execution Loop
```
For each story:
  1. Update state: story in_progress
  2. Spawn DEVELOPER -> Implement
  3. Spawn TESTER -> Verify
     - If FAIL: Back to DEVELOPER
  4. Spawn REVIEWER -> Review
     - If CHANGES REQUESTED: Back to DEVELOPER
  5. Update state: story completed
  6. Check checkpoint (every 5 stories -> human review)
```

### Phase 3: Completion
```
1. All stories complete
2. Spawn DEVOPS for final deployment
3. Update state: workflow completed
4. Report to human
```

---

## State Management

The workflow uses `.claude/workflow-state.json` for persistence.

### Update Story Status
```bash
python .claude/hooks/state.py update-story S1 in_progress
python .claude/hooks/state.py update-story S1 completed
```

### Add Stories
```bash
python .claude/hooks/state.py add-story "Story title"
```

### Check Status
```bash
python .claude/hooks/state.py status
```

---

## Escalation Triggers

### Automatic Escalation to Human

| Condition | Action |
|-----------|--------|
| 5 stories completed | Checkpoint review |
| 3+ failed attempts on same task | Escalate blocker |
| Security issue found | Immediate escalation |
| Scope creep detected | Clarification needed |
| Agent reports blocker | Escalate to human |

### Escalation Format
```markdown
## Escalation Required

**Type:** [Blocker/Clarification/Security/Scope]
**Story:** [Story ID if applicable]
**Issue:** [Clear description]
**Options:** [Possible resolutions if known]
**Recommendation:** [Your recommendation]

Awaiting human input...
```

---

## Recovery Protocols

### Stuck in Loop
If developer -> tester -> developer cycles 3+ times:
1. Pause execution
2. Spawn ARCHITECT to review approach
3. Consider simplifying or redesigning
4. Update state with decision

### Tests Won't Pass
If tests fail repeatedly:
1. Check if requirements are achievable
2. Consider splitting story
3. Escalate if unclear

### Agent Timeout
If subagent takes too long:
1. Check task output for progress
2. Consider breaking into smaller tasks
3. Resume with focused prompt

---

## Parallel Execution

When stories are independent, spawn multiple agents in parallel:

```
// In a single message, launch multiple Task calls:

Task({
  subagent_type: "general-purpose",
  prompt: "Implement Story 1...",
  run_in_background: true
})

Task({
  subagent_type: "general-purpose",
  prompt: "Implement Story 2...",
  run_in_background: true
})

// Then wait for results:
TaskOutput({ task_id: "agent1" })
TaskOutput({ task_id: "agent2" })
```

---

## Configuration

### Strictness Levels

Set in orchestrator context:

| Level | TDD | Review | Edge Cases |
|-------|-----|--------|------------|
| strict | Full coverage | Comprehensive | All identified |
| balanced | Core logic | Pragmatic | High-risk |
| fast | Minimal | Quick | Critical only |

Default: `balanced`

### Override Example
```
Use multi-agent workflow (strict mode) to: Build payment processing
```

---

## Quick Reference

### Start Workflow
```
Use the multi-agent workflow to: [goal]
```

### Check Status
```
Orchestrator: Report workflow status
```

### Force Checkpoint
```
Pause for human review
```

### Skip to Phase
```
Skip to implementation with these stories: [list]
```

### Cancel Workflow
```
Cancel the current workflow
```

---

## Files Reference

| File | Purpose |
|------|---------|
| `.claude/agents/analyst.md` | Analyst agent prompt |
| `.claude/agents/architect.md` | Architect agent prompt |
| `.claude/agents/developer.md` | Developer agent prompt |
| `.claude/agents/tester.md` | Tester agent prompt |
| `.claude/agents/reviewer.md` | Reviewer agent prompt |
| `.claude/agents/devops.md` | DevOps agent prompt |
| `.claude/hooks/safety.py` | PreToolUse safety hook |
| `.claude/hooks/audit.py` | PostToolUse audit hook |
| `.claude/hooks/state.py` | State management CLI |
| `.claude/workflow-state.json` | Current workflow state |
| `.claude/audit.log` | Tool usage audit log |
