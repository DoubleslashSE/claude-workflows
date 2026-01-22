---
name: plan
description: Create atomic task plan with XML-structured tasks, verification steps, and dependency mapping
user_invocable: true
---

# Plan Phase

You are starting the PLAN phase of the flow-workflow. This phase creates an atomic task plan from the requirements gathered in DISCUSS.

## What to Do

1. **Check for active work item** from ACTIVE.md
2. **Verify DISCUSS is complete** or can proceed
3. **Read requirements and decisions** from item's state files
4. **Spawn planner agent** to create task plan
5. **Cross-verify plan** against requirements and decisions
6. **Get user approval** for plan
7. **Create ROADMAP.md** with milestones

## Active Item Check

### Required: Active Work Item

First, verify there's an active work item:

1. **Read `.flow/ACTIVE.md`** to get current item
2. **If no active item**: Prompt user to select or create one
3. **If active item exists**: Use its directory for all state files

```markdown
# No Active Item

There is no active work item. Please:
- `/flow-workflow:new [title] --start` - Create and start new item
- `/flow-workflow:switch ITEM-XXX` - Activate an existing item
- `/flow-workflow:flow [task]` - Start full workflow (creates item)
```

### Item State Directory

All state files are stored in the active item's directory:
- `.flow/items/ITEM-XXX/STATE.md`
- `.flow/items/ITEM-XXX/REQUIREMENTS.md`
- `.flow/items/ITEM-XXX/PLAN.md`
- `.flow/items/ITEM-XXX/ROADMAP.md`

## Starting PLAN Phase

### Verify Prerequisites

Check that DISCUSS phase is complete for the active item:
- Item's REQUIREMENTS.md exists with requirements
- Item's STATE.md shows DISCUSS complete (or user confirms to proceed)
- No active blockers

If prerequisites not met:
```markdown
**Cannot Start PLAN Phase**

**Work Item**: ITEM-XXX - [Title]

DISCUSS phase must be completed first.

**Current state**:
- DISCUSS: [status]
- REQUIREMENTS.md: [exists/missing]
- Active blockers: [list]

**Options**:
1. Complete DISCUSS: `/flow-workflow:discuss`
2. Override and start planning anyway [requires confirmation]
```

### Update Item STATE.md

Update `.flow/items/ITEM-XXX/STATE.md`:

```markdown
## Current Phase

**Phase**: PLAN
**Started**: [TIMESTAMP]
**Progress**: 0%
```

Also update `.flow/BACKLOG.md` to reflect item status change to PLAN.

## Spawn Planner Agent

Use the Task tool to spawn the planner agent:

```markdown
Spawn flow-workflow:planner agent with context:
- Active item: ITEM-XXX
- Item directory: .flow/items/ITEM-XXX/
- Requirements from item's REQUIREMENTS.md
- Decisions from item's STATE.md
- Exploration summary from item's EXPLORATION.md
- Project context from .flow/PROJECT.md (shared)
```

The planner will:
1. Read requirements and context from item directory
2. Decompose into atomic tasks
3. Define task dependencies
4. Add verification steps
5. Cross-verify plan
6. Create item's PLAN.md

## PLAN Phase Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     PLAN PHASE FLOW                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. GATHER CONTEXT                                              │
│     ├─ Read item's REQUIREMENTS.md                              │
│     ├─ Read item's STATE.md decisions                           │
│     ├─ Read item's EXPLORATION.md for additional context        │
│     └─ Understand existing codebase (if brownfield)             │
│                                                                 │
│  2. DECOMPOSE                                                   │
│     ├─ Identify work items from requirements                    │
│     ├─ Break into atomic tasks                                  │
│     ├─ Define files to create/modify                            │
│     └─ Write specific actions for each task                     │
│                                                                 │
│  3. ORDER                                                       │
│     ├─ Identify dependencies between tasks                      │
│     ├─ Create dependency graph                                  │
│     ├─ Determine execution order                                │
│     └─ Maximize parallelization opportunities                   │
│                                                                 │
│  4. VERIFY                                                      │
│     ├─ Add verification steps to each task                      │
│     ├─ Define done criteria                                     │
│     ├─ Write commit messages                                    │
│     └─ Cross-verify against requirements                        │
│                                                                 │
│  5. APPROVE                                                     │
│     ├─ Present plan summary                                     │
│     ├─ User reviews and approves                                │
│     └─ Mark plan as APPROVED                                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Cross-Plan Verification

Before finalizing, verify:

```markdown
## Cross-Plan Verification Checklist

**Against item's REQUIREMENTS.md:**
- [ ] All requirements have at least one task
- [ ] No tasks contradict requirements
- [ ] Priority order respected

**Against item's STATE.md decisions:**
- [ ] Tasks align with recorded decisions
- [ ] No tasks contradict decisions
- [ ] Deferred items not accidentally included

**Against existing item's PLAN.md (if exists):**
- [ ] New tasks don't conflict with pending tasks
- [ ] File modifications don't overlap dangerously
- [ ] Dependency order preserved

**Conflicts found**: [List or "None"]
```

## Create PLAN.md

The planner creates `.flow/items/ITEM-XXX/PLAN.md`:

```markdown
# Execution Plan

**Work Item**: ITEM-XXX
**Title**: [from work item]
**Created**: [TIMESTAMP]
**Last Updated**: [TIMESTAMP]
**Status**: DRAFT

## Plan Summary

**Total Tasks**: [N]
**Completed**: 0
**Progress**: 0%

## Cross-Plan Verification

[Verification results]

## Tasks

<task id="TASK-001" status="pending">
  <name>[name]</name>
  <description>[description]</description>
  <files>
    <file action="create">[path]</file>
  </files>
  <actions>
    <action>[action]</action>
  </actions>
  <verify>
    <step>[verification]</step>
  </verify>
  <done>
    <criterion>[criterion]</criterion>
  </done>
  <commit>[commit message]</commit>
</task>

[Additional tasks...]

## Task Dependencies

```
TASK-001 ──┬── TASK-003
           │
TASK-002 ──┘
```

## Execution Order

1. [ ] TASK-001: [name]
2. [ ] TASK-002: [name]
...
```

## Create ROADMAP.md

Create `.flow/items/ITEM-XXX/ROADMAP.md` with milestones:

```markdown
# Roadmap

**Work Item**: ITEM-XXX
**Title**: [from work item]
**Created**: [TIMESTAMP]
**Last Updated**: [TIMESTAMP]

## Milestones

### M1: Core Implementation
**Status**: NOT_STARTED
**Tasks**: TASK-001 through TASK-005
**Progress**: 0%

### M2: Integration
**Status**: NOT_STARTED
**Tasks**: TASK-006 through TASK-008
**Progress**: 0%

## Progress Summary

| Milestone | Tasks | Completed | Progress |
|-----------|-------|-----------|----------|
| M1 | 5 | 0 | 0% |
| M2 | 3 | 0 | 0% |
```

## Plan Approval

Present plan for user approval:

```markdown
**Plan Ready for Review**

**Work Item**: ITEM-XXX - [Title]

**Summary**:
- Total tasks: [N]
- Feature tasks: [X]
- Bug fix tasks: [Y]
- Refactor tasks: [Z]

**Execution order**:
1. [TASK-001] → [TASK-003]
2. [TASK-002] ↗
3. [TASK-003] → [TASK-004]

**Requirements coverage**:
| Requirement | Tasks |
|-------------|-------|
| FR-001 | TASK-001, TASK-002 |
| FR-002 | TASK-003 |

**Cross-verification**: [PASSED/issues]

**Options**:
1. Approve plan - start execution
2. Modify plan - make changes
3. Add tasks - include more work
4. Return to DISCUSS - need more clarity
```

## Completing PLAN Phase

### Update Item STATE.md

Update `.flow/items/ITEM-XXX/STATE.md`:

```markdown
## Current Phase

**Phase**: PLAN
**Started**: [original timestamp]
**Progress**: 100%
**Completed**: [TIMESTAMP]

### CHECKPOINT: PLAN-COMPLETE-[TIMESTAMP]
**Completed**:
- [x] Created [N] atomic tasks
- [x] Defined dependencies
- [x] Added verification steps
- [x] Cross-verified against requirements
- [x] User approved plan

**Next Action**: Run /flow-workflow:execute to begin implementation
```

Also update `.flow/BACKLOG.md` with item's progress (PLAN complete, ready for EXECUTE).

## Output Format

### Plan Complete

```markdown
**PLAN Phase Complete**

**Work Item**: ITEM-XXX - [Title]
**Plan created**: .flow/items/ITEM-XXX/PLAN.md
**Roadmap created**: .flow/items/ITEM-XXX/ROADMAP.md

**Summary**:
- Tasks: [N]
- Milestones: [M]
- Estimated commits: [N]

**Requirements coverage**: [X]%
**Cross-verification**: PASSED

**Next**: Run `/flow-workflow:execute` to begin implementation
```

## Skills Used

- **atomic-tasks**: For task structure
- **conflict-detection**: For cross-plan verification
- **state-management**: For state updates

## Agent Spawned

- **planner**: Creates atomic task plan
