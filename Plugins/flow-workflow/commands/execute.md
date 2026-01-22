---
name: execute
description: Execute tasks from PLAN.md with fresh context per task, capability-based routing, and atomic commits
user_invocable: true
args: "[task-id]"
---

# Execute Phase

You are starting or continuing the EXECUTE phase of the flow-workflow. This phase implements tasks from the active item's PLAN.md one at a time with fresh context.

## What to Do

1. **Check for active work item** from ACTIVE.md
2. **Verify PLAN is approved** or can proceed
3. **Identify next task** to execute (or specified task)
4. **Route to appropriate agent** based on capabilities
5. **Execute task** with fresh context
6. **Verify and commit** on success
7. **Update progress** in state files

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
- `.flow/items/ITEM-XXX/PLAN.md`
- `.flow/items/ITEM-XXX/REQUIREMENTS.md`

## Starting EXECUTE Phase

### Verify Prerequisites

Check that PLAN phase is complete for the active item:
- Item's PLAN.md exists with APPROVED status
- No active blockers preventing execution
- Dependencies are satisfied for first task

If not ready:
```markdown
**Cannot Start EXECUTE Phase**

**Work Item**: ITEM-XXX - [Title]

PLAN phase must be completed first.

**Current state**:
- PLAN.md: [exists/missing/status]
- Pending approval: [yes/no]

**Options**:
1. Complete planning: `/flow-workflow:plan`
2. Override and execute anyway [requires confirmation]
```

### Update Item STATE.md

Update `.flow/items/ITEM-XXX/STATE.md`:

```markdown
## Current Phase

**Phase**: EXECUTE
**Started**: [TIMESTAMP]
**Progress**: 0%
```

Also update `.flow/BACKLOG.md` to reflect item status change to EXECUTE.

## Task Selection

### Default: Next Pending Task

If no task-id specified:
1. Read item's PLAN.md from `.flow/items/ITEM-XXX/PLAN.md`
2. Find first task with:
   - Status = "pending"
   - All dependencies completed

### Specific Task

If task-id specified:
1. Validate task exists
2. Check dependencies are met
3. Proceed with specified task

### No Available Tasks

If no tasks can proceed:
```markdown
**No Tasks Available**

All remaining tasks are blocked:
- TASK-XXX: Waiting on TASK-YYY
- TASK-ZZZ: Has BLOCKER-001

**Options**:
1. Address blockers
2. Check dependency resolution
3. Mark workflow complete (if all tasks done)
```

## Capability-Based Routing

### Check Capability Map

For each task, determine best agent:

1. Read task description and type
2. Check `.flow/capabilities.md` (project-level) for capability cache
3. Match task needs to capabilities
4. Filter by project type

### Routing Examples

| Task Type | Capability | Routed To |
|-----------|------------|-----------|
| Feature with tests | tdd-implementation | dotnet-tdd:implementer |
| Bug fix | code-implementation | flow-workflow:executor |
| Infrastructure | infrastructure | devops agent |
| General code | code-implementation | developer agent |

### Fallback

If no matching capability:
- Use flow-workflow:executor agent
- Log warning in item's STATE.md

## Task Execution Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                   EXECUTE TASK FLOW                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. SELECT TASK                                                 │
│     ├─ Find next pending task                                   │
│     ├─ Verify dependencies met                                  │
│     └─ Mark as in_progress                                      │
│                                                                 │
│  2. ROUTE TO AGENT                                              │
│     ├─ Determine capability needed                              │
│     ├─ Look up capability map                                   │
│     └─ Spawn appropriate agent with fresh context               │
│                                                                 │
│  3. EXECUTE                                                     │
│     ├─ Agent reads task definition                              │
│     ├─ Agent executes actions                                   │
│     ├─ Agent runs verification                                  │
│     └─ Agent reports result                                     │
│                                                                 │
│  4. ON SUCCESS                                                  │
│     ├─ Create atomic commit                                     │
│     ├─ Mark task completed                                      │
│     ├─ Update progress                                          │
│     └─ Select next task                                         │
│                                                                 │
│  5. ON FAILURE                                                  │
│     ├─ Record failure details                                   │
│     ├─ Create blocker if needed                                 │
│     ├─ Present options to user                                  │
│     └─ Wait for resolution                                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Spawn Executor Agent

For general tasks, spawn flow-workflow:executor:

```markdown
Spawn executor agent with:
- Active item: ITEM-XXX
- Item directory: .flow/items/ITEM-XXX/
- Task ID: [TASK-XXX]
- Task definition from item's PLAN.md
- Relevant context files
- Project conventions
```

For specialized tasks, spawn capability-matched agent:

```markdown
Spawn [plugin]:[agent] agent with:
- Active item: ITEM-XXX
- Item directory: .flow/items/ITEM-XXX/
- Task to implement
- Context from item's PLAN.md
- Verification requirements
```

## Fresh Context Per Task

Each task gets fresh context:
- Don't carry full history between tasks
- Load only: task definition, relevant files, conventions
- This prevents context bloat
- Enables clean, focused execution

## Progress Tracking

### Update Item PLAN.md

After each task, update `.flow/items/ITEM-XXX/PLAN.md`:
```xml
<!-- Before -->
<task id="TASK-001" status="pending">

<!-- After -->
<task id="TASK-001" status="completed">
```

### Update Item STATE.md

Update `.flow/items/ITEM-XXX/STATE.md`:

```markdown
## Current Phase

**Phase**: EXECUTE
**Started**: [original timestamp]
**Progress**: [calculated %]

**Tasks**: [completed]/[total]
**Current**: [TASK-XXX or "None"]
```

### Update Item ROADMAP.md

Update `.flow/items/ITEM-XXX/ROADMAP.md`:

```markdown
### M1: Core Implementation
**Status**: IN_PROGRESS
**Tasks**: TASK-001 through TASK-005
**Progress**: 40% (2/5)
```

Also update `.flow/BACKLOG.md` with item's overall progress.

## Handling Task Failures

### Verification Failure

```markdown
**Task Verification Failed**

Task: TASK-XXX
Step: [failed verification step]
Error: [error message]

**Options**:
1. Fix and retry
2. Skip verification (not recommended)
3. Mark as blocked
4. Abort execution
```

### Implementation Error

```markdown
**Task Implementation Error**

Task: TASK-XXX
Action: [failed action]
Error: [error details]

**Options**:
1. Retry with different approach
2. Mark as blocked, continue others
3. Return to PLAN for task revision
4. Abort execution
```

### Create Blocker

If task cannot proceed:

```markdown
### BLOCKER-XXX: [Title]
**Status**: ACTIVE
**Task**: TASK-XXX
**Issue**: [description]
**Impact**: [what's blocked]
**Needs**: [resolution requirements]
```

## Completing EXECUTE Phase

### All Tasks Done

When all tasks completed:

```markdown
**EXECUTE Phase Complete**

**Work Item**: ITEM-XXX - [Title]

**Summary**:
- Tasks completed: [N]
- Tasks skipped: [N]
- Commits created: [N]

**Next**: Run `/flow-workflow:verify` to validate implementation
```

### Update Item STATE.md

Update `.flow/items/ITEM-XXX/STATE.md`:

```markdown
## Current Phase

**Phase**: EXECUTE
**Started**: [original timestamp]
**Progress**: 100%
**Completed**: [TIMESTAMP]

### CHECKPOINT: EXECUTE-COMPLETE-[TIMESTAMP]
**Completed**:
- [x] Executed [N] tasks
- [x] Created [N] commits
- [x] All verifications passed

**Next Action**: Run /flow-workflow:verify for final validation
```

Also update `.flow/BACKLOG.md` with item's progress (EXECUTE complete, ready for VERIFY).

## Output Format

### Starting Execution

```markdown
**EXECUTE Phase Started**

**Work Item**: ITEM-XXX - [Title]
**Plan**: [N] tasks total
**Ready**: [M] tasks (dependencies met)
**Starting**: TASK-XXX - [name]

[Spawning executor agent...]
```

### Task Progress

```markdown
**Task Progress**

```
[===========         ] 55% (11/20 tasks)
```

**Just completed**: TASK-XXX - [name]
**Next task**: TASK-YYY - [name]
**Blocked**: [N] tasks
```

## Skills Used

- **capability-discovery**: For agent routing
- **atomic-tasks**: For task structure
- **context-engineering**: For fresh context
- **state-management**: For progress tracking

## Agents Spawned

- **executor**: Default implementation agent
- **[capability-matched agent]**: Based on task type
