---
name: new
description: Create a new work item in the backlog. Optionally start working on it immediately.
user_invocable: true
args: "<title> [--priority P0|P1|P2|P3] [--start]"
---

# Create New Work Item

You are creating a new work item (epic/story) in the backlog.

## Arguments

- `<title>`: Required. The title/name of the work item
- `--priority`: Optional. Priority level (P0=Critical, P1=High, P2=Medium, P3=Low). Default: P2
- `--start`: Optional. Immediately make this the active item and begin DISCUSS phase

## Examples

```
/flow-workflow:new Add user authentication
/flow-workflow:new Fix cart calculation bug --priority P0
/flow-workflow:new Implement dark mode --priority P1 --start
```

## What to Do

1. **Verify initialization**: Check `.flow/` exists
2. **Generate item ID**: Get next available ITEM-XXX
3. **Create item directory**: `.flow/items/ITEM-XXX/`
4. **Create initial STATE.md**: With BACKLOG status
5. **Update BACKLOG.md**: Add new item entry
6. **Optionally activate**: If `--start` flag, switch to this item

## Creation Protocol

### Step 1: Verify Prerequisites

```markdown
Check:
- .flow/ directory exists
- BACKLOG.md exists
- Can determine next item ID
```

If not initialized:
```markdown
**Cannot Create Work Item**

Workflow not initialized. Run `/flow-workflow:init` first.
```

### Step 2: Generate Item ID

Read BACKLOG.md to find highest existing item number:
- ITEM-001, ITEM-002, ... → Next is ITEM-003
- No items → Start with ITEM-001

### Step 3: Create Item Directory

```bash
mkdir -p .flow/items/ITEM-XXX
```

### Step 4: Create Initial STATE.md

Create `.flow/items/ITEM-XXX/STATE.md`:

```markdown
# Work Item State

**Item**: ITEM-XXX
**Title**: [title from args]
**Created**: [TIMESTAMP]
**Last Updated**: [TIMESTAMP]

## Current Status

**Status**: BACKLOG
**Phase**: Not started
**Progress**: 0%

## Description

[Title] - awaiting discussion to define scope and requirements.

## Context

**Original Request**:
> [title]

**Goals**:
1. [To be defined in DISCUSS phase]

**Constraints**:
- [To be defined]

## Decisions

[No decisions yet - start DISCUSS phase]

## Checkpoints

[No checkpoints yet]

## Phase History

| Phase | Started | Completed | Duration |
|-------|---------|-----------|----------|
| BACKLOG | [TS] | - | - |
```

### Step 5: Update BACKLOG.md

Add entry to BACKLOG.md:

```markdown
### ITEM-XXX: [Title]
**Status**: BACKLOG
**Priority**: [priority or P2]
**Created**: [TIMESTAMP]
**Updated**: [TIMESTAMP]
**Description**: [Title] - awaiting discussion
**Phase Progress**: 0%
**Tags**: [new]
```

Also update summary counts.

### Step 6: Handle --start Flag

If `--start` specified:
1. Update ACTIVE.md to point to new item
2. Transition item to DISCUSS phase
3. Spawn interviewer to begin exploration

## Output Format

### Without --start

```markdown
**Work Item Created**

**ID**: ITEM-XXX
**Title**: [title]
**Priority**: [priority]
**Status**: BACKLOG

**Location**: .flow/items/ITEM-XXX/

**Next steps**:
- `/flow-workflow:switch ITEM-XXX` - Make this active
- `/flow-workflow:backlog` - View all items
- `/flow-workflow:new [another]` - Create another item
```

### With --start

```markdown
**Work Item Created and Activated**

**ID**: ITEM-XXX
**Title**: [title]
**Priority**: [priority]
**Status**: DISCUSS (starting)

**Location**: .flow/items/ITEM-XXX/

Beginning requirements exploration...

[Spawns interviewer agent]
```

## Priority Levels

| Level | Name | Use For |
|-------|------|---------|
| P0 | Critical | Urgent issues, blockers |
| P1 | High | Important features, significant bugs |
| P2 | Medium | Normal priority (default) |
| P3 | Low | Nice-to-have, minor improvements |

## Validation

### Title Validation
- Must be non-empty
- Reasonable length (5-100 characters recommended)
- No special characters that break markdown

### Priority Validation
- Must be P0, P1, P2, or P3
- Default to P2 if not specified or invalid

## Error Handling

### Duplicate Detection
Not enforced - multiple items can have similar titles. Use unique IDs.

### Directory Creation Failure
```markdown
**Error Creating Work Item**

Could not create directory: .flow/items/ITEM-XXX
Error: [error message]

Please check file permissions.
```

## Skills Used

- **state-management**: Creating and updating state files
