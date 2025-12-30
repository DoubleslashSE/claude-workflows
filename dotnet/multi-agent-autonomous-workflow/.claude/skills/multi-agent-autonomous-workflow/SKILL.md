---
name: multi-agent-autonomous-workflow
description: Orchestrates multi-agent workflow for feature implementation using specialized subagents. Use when implementing features, epics, or complex multi-story tasks that need analyst, architect, developer, tester, reviewer, and security agents.
---

# Multi-Agent Autonomous Workflow

Orchestrates specialized subagents for extended autonomous work with minimal human intervention.

## When to Use

- Feature implementation
- Epic-level requests
- Complex multi-story tasks

## Architecture

```
ORCHESTRATOR (You)
    │
    ├── analyst     → Requirements & user stories
    ├── architect   → Technical design
    ├── developer   → TDD implementation
    ├── tester      → Verification
    ├── reviewer    → Code review
    ├── security    → Security audit (if flagged)
    └── devops      → Infrastructure (if needed)
```

## Workflow Phases

### Phase 1: Analysis
1. Invoke `analyst` subagent with the goal
2. Receive user stories with acceptance criteria
3. Invoke `architect` for technical design

### Phase 2: Story Execution (for each story)
1. Invoke `developer` with story + design
2. Invoke `tester` to verify implementation
3. Invoke `reviewer` for code review
4. If `[SECURITY-SENSITIVE]`: invoke `security`

### Phase 3: Completion
1. Invoke `devops` if deployment needed
2. Report completion to human

## Quality Gates

| Gate | When | Check |
|------|------|-------|
| G1 | Before dev | Design complete, AC clear |
| G2 | After dev | Build passes, tests pass |
| G3 | After test | Coverage threshold met |
| G4 | If security | Security scan passes |

## Escalation Triggers

- 5 stories completed → checkpoint review
- 3+ failed attempts → escalate blocker
- Security issue → immediate escalation
- Scope creep → clarification needed

## Commands

- `/workflow [goal]` - Start workflow
- `/status` - Check progress
- `/implement [story]` - Implement specific story

For detailed reference, see [workflow-reference.md](workflow-reference.md).
