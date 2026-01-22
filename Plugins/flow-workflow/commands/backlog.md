---
name: backlog
description: List and manage work items in the backlog. View status, filter by state, and get overview of all planned work.
user_invocable: true
args: "[filter]"
---

# Backlog Management

You are viewing and managing the work item backlog. This command displays all work items and their current status.

## Arguments

- No args: Show full backlog overview
- `active`: Show only in-progress items (DISCUSS/PLAN/EXECUTE/VERIFY)
- `ready`: Show items ready to start (BACKLOG status)
- `blocked`: Show blocked or on-hold items
- `complete`: Show completed items
- `[ITEM-XXX]`: Show details for specific item

## What to Do

1. **Read BACKLOG.md** to get all work items
2. **Apply filter** if specified
3. **Display formatted backlog** to user
4. **Show active item** prominently
5. **Suggest actions** based on backlog state

## Backlog Display

### Full Overview (No Filter)

```markdown
# Work Item Backlog

**Active**: [ITEM-XXX] - [Title] ([Phase])

## Summary

| Status | Count |
|--------|-------|
| In Progress | [N] |
| Ready | [N] |
| Blocked | [N] |
| Complete | [N] |

## In Progress

| Item | Title | Phase | Progress |
|------|-------|-------|----------|
| ITEM-001 | [Title] | EXECUTE | 60% |
| ITEM-002 | [Title] | DISCUSS | 30% |

## Ready to Start

| Item | Title | Priority | Created |
|------|-------|----------|---------|
| ITEM-003 | [Title] | P1 | [date] |
| ITEM-004 | [Title] | P2 | [date] |

## Blocked/On Hold

| Item | Title | Reason | Since |
|------|-------|--------|-------|
| ITEM-005 | [Title] | Waiting on API | [date] |

## Recently Completed

| Item | Title | Completed |
|------|-------|-----------|
| ITEM-000 | [Title] | [date] |

## Actions

- `/flow-workflow:new [title]` - Create new work item
- `/flow-workflow:switch ITEM-XXX` - Switch to item
- `/flow-workflow:flow` - Continue active item
```

### Active Items Filter

```markdown
# Active Work Items

| Item | Title | Phase | Progress | Last Updated |
|------|-------|-------|----------|--------------|
| ITEM-001 | [Title] | EXECUTE | 60% | [timestamp] |
| ITEM-002 | [Title] | DISCUSS | 30% | [timestamp] |

**Currently Active**: ITEM-001

To switch: `/flow-workflow:switch ITEM-XXX`
```

### Ready Items Filter

```markdown
# Ready to Start

| Item | Title | Priority | Description |
|------|-------|----------|-------------|
| ITEM-003 | [Title] | P1 | [Brief desc] |
| ITEM-004 | [Title] | P2 | [Brief desc] |

To start an item: `/flow-workflow:switch ITEM-XXX`
```

### Blocked Items Filter

```markdown
# Blocked / On Hold

### ITEM-005: [Title]
**Status**: BLOCKED
**Since**: [timestamp]
**Reason**: [blocking reason]
**Waiting for**: [what's needed]

### ITEM-006: [Title]
**Status**: ON_HOLD
**Since**: [timestamp]
**Reason**: [why on hold]
**Resume when**: [condition]
```

### Completed Items Filter

```markdown
# Completed Work Items

| Item | Title | Completed | Duration |
|------|-------|-----------|----------|
| ITEM-000 | [Title] | [date] | 3 days |

### ITEM-000: [Title]
**Completed**: [timestamp]
**Summary**: [what was delivered]
**Tasks**: [N] completed
**Commits**: [N] created
```

### Single Item Details

```markdown
# ITEM-XXX: [Title]

**Status**: [status]
**Priority**: [priority]
**Created**: [timestamp]
**Updated**: [timestamp]

## Description

[Full description]

## Current State

**Phase**: [phase]
**Progress**: [X]%
**Last Checkpoint**: [checkpoint-id]

## Phase History

| Phase | Started | Completed | Duration |
|-------|---------|-----------|----------|
| DISCUSS | [ts] | [ts] | [time] |
| PLAN | [ts] | - | ongoing |

## Key Decisions

- DECISION-001: [summary]
- DECISION-002: [summary]

## Files

- STATE.md: [path]
- PLAN.md: [exists/not created]
- REQUIREMENTS.md: [exists/not created]

## Actions

- `/flow-workflow:switch ITEM-XXX` - Make this active
- `/flow-workflow:discuss` - Continue discussion
- `/flow-workflow:plan` - Continue planning
```

## Empty Backlog

If no items exist:

```markdown
# Work Item Backlog

**No work items yet.**

To create your first work item:
```
/flow-workflow:new [title]
```

Or start a full workflow:
```
/flow-workflow:flow [task description]
```
```

## Backlog Not Initialized

If `.flow/` doesn't exist:

```markdown
**Backlog Not Initialized**

Run `/flow-workflow:init` first to set up the workflow system.
```

## Backlog Operations

### Reorder Items (Future Enhancement)
```markdown
To change priority:
1. Edit .flow/BACKLOG.md
2. Update Priority field for item
3. Backlog views will reflect new order
```

### Archive Completed Items
```markdown
Completed items remain in BACKLOG.md for reference.
Item directories in .flow/items/ are preserved.
```

## Output Format

Always show:
1. Active item prominently at top
2. Summary counts
3. Relevant items based on filter
4. Available actions

## Skills Used

- **state-management**: Reading backlog and item state
