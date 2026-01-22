---
name: status
description: Display current workflow state including backlog overview, active item, phase, progress, and blockers
user_invocable: true
---

# Show Workflow Status

You are displaying the current state of the flow-workflow system, including backlog overview and active item details.

## What to Do

1. **Read BACKLOG.md** for backlog overview
2. **Read ACTIVE.md** for current item
3. **Read item's STATE.md** for active item details
4. **Read item's PLAN.md** if exists for task progress
5. **Display formatted status** to user
6. **Suggest next actions** based on current state

## Status Display

### Check for Initialization

First, check if `.flow/` exists:
- If not: Report "Not initialized. Run /flow-workflow:init first."
- If yes: Continue reading state

### Read State Files

Read the following files:
- `.flow/BACKLOG.md` - All work items
- `.flow/ACTIVE.md` - Current active item
- `.flow/items/ITEM-XXX/STATE.md` - Active item's state (if active)
- `.flow/items/ITEM-XXX/PLAN.md` - Active item's tasks (if exists)

### Full Status Display

```markdown
# Flow Workflow Status

## Backlog Overview

| Status | Count |
|--------|-------|
| In Progress | [N] |
| Ready | [N] |
| Blocked | [N] |
| Complete | [N] |
| **Total** | [N] |

### Work Items at a Glance

| Item | Title | Status | Progress |
|------|-------|--------|----------|
| → ITEM-001 | [Title] | EXECUTE | 60% |
| ITEM-002 | [Title] | BACKLOG | 0% |
| ITEM-003 | [Title] | COMPLETE | 100% |

(→ indicates active item)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Active Item: ITEM-XXX

**Title**: [Title]
**Phase**: [CURRENT_PHASE]
**Started**: [phase start time]
**Progress**: [X]%

### Quick Summary

| Metric | Value |
|--------|-------|
| Decisions made | [N] |
| Active blockers | [N] |
| Active conflicts | [N] |
| Tasks total | [N] |
| Tasks completed | [N] |
| Tasks remaining | [N] |

### Current Phase Details

[Phase-specific details]

### Recent Activity

- [TIMESTAMP]: [Activity 1]
- [TIMESTAMP]: [Activity 2]

### Blockers

[List active blockers or "None"]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Available Actions

**For active item**:
1. [Phase-appropriate action]
2. [Alternative action]

**For backlog**:
- `/flow-workflow:backlog` - View full backlog
- `/flow-workflow:new [title]` - Create new item
- `/flow-workflow:switch ITEM-XXX` - Switch to different item
```

## No Active Item

If no item is currently active:

```markdown
# Flow Workflow Status

## Backlog Overview

| Status | Count |
|--------|-------|
| In Progress | 0 |
| Ready | [N] |
| Blocked | [N] |
| Complete | [N] |
| **Total** | [N] |

### Work Items

| Item | Title | Status | Priority |
|------|-------|--------|----------|
| ITEM-001 | [Title] | BACKLOG | P1 |
| ITEM-002 | [Title] | BACKLOG | P2 |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## No Active Item

Select a work item to begin:
- `/flow-workflow:switch ITEM-XXX` - Activate an existing item
- `/flow-workflow:new [title] --start` - Create and start new item
- `/flow-workflow:flow [task]` - Create item and run full workflow
```

## Empty Backlog

If backlog is empty:

```markdown
# Flow Workflow Status

## Backlog Overview

**No work items yet.**

Get started:
- `/flow-workflow:new [title]` - Create a work item
- `/flow-workflow:flow [task]` - Start full workflow
```

## Phase-Specific Details

### BACKLOG Status (Item Not Started)
```markdown
### Status: BACKLOG

This item is defined but not yet started.

**Created**: [timestamp]
**Priority**: [priority]

**To begin**: `/flow-workflow:discuss` or `/flow-workflow:flow`
```

### DISCUSS Phase
```markdown
### Phase: DISCUSS

Gathering requirements and making decisions.

**Exploration map**:
- Areas explored: [N]
- Areas uncharted: [N]
- Current area: [name]

**Decisions made**: [N]

**Next**: Continue discussion or run `/flow-workflow:plan` when ready
```

### PLAN Phase
```markdown
### Phase: PLAN

Creating execution plan.

**Plan status**: [DRAFT/APPROVED/IN_PROGRESS]
**Tasks defined**: [N]

**Next**: Review plan and run `/flow-workflow:execute` to begin
```

### EXECUTE Phase
```markdown
### Phase: EXECUTE

Implementing tasks.

**Progress**:
```
[===========         ] 55% (11/20 tasks)
```

**Current task**: [TASK-XXX] - [name]
**Completed**: [N]
**Remaining**: [N]
**Blocked**: [N]

**Next**: Continue execution or check blocked tasks
```

### VERIFY Phase
```markdown
### Phase: VERIFY

Validating implementation.

**Automated checks**: [PASS/FAIL/PENDING]
**Requirements verified**: [X/Y]
**UAT status**: [PENDING/IN_PROGRESS/COMPLETE]

**Next**: Complete verification or address issues
```

### COMPLETE Status
```markdown
### Status: COMPLETE

Work item completed successfully.

**Completed**: [timestamp]
**Duration**: [time]
**Summary**:
- Tasks completed: [N]
- Requirements verified: [N]

**Actions**: Switch to another item or create new one
```

### ON_HOLD / BLOCKED Status
```markdown
### Status: [ON_HOLD/BLOCKED]

**Since**: [timestamp]
**Reason**: [reason]

**To resume**: [what needs to happen]
```

## Task Progress (If in EXECUTE)

```markdown
## Task Progress

| Status | Count | Tasks |
|--------|-------|-------|
| Completed | [N] | TASK-001, TASK-002 |
| In Progress | [N] | TASK-005 |
| Pending | [N] | TASK-006, TASK-007 |
| Blocked | [N] | TASK-004 |

### Current Task

**TASK-XXX**: [name]
**Status**: [status]
**Actions remaining**: [N]
**Dependencies**: [met/waiting on TASK-YYY]
```

## Blocker Display

```markdown
## Active Blockers

### BLOCKER-001: [Title]
**Type**: [type]
**Impact**: [what's blocked]
**Needs**: [what's needed to resolve]
```

## Available Actions by State

| State | Suggested Actions |
|-------|-------------------|
| No active item | `/flow-workflow:switch`, `/flow-workflow:new --start` |
| BACKLOG | `/flow-workflow:discuss`, `/flow-workflow:flow` |
| DISCUSS in progress | Continue, `/flow-workflow:plan` |
| PLAN ready | `/flow-workflow:execute` |
| EXECUTE in progress | Continue, check blockers |
| VERIFY pending | `/flow-workflow:verify` |
| Blocked | Address blockers, `/flow-workflow:resume` |
| Complete | `/flow-workflow:switch`, `/flow-workflow:new` |

## Skills Used

- **state-management**: For reading state files and backlog
