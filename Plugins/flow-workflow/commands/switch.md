---
name: switch
description: Switch the active work item to a different item from the backlog. Saves current progress and loads new item context.
user_invocable: true
args: "<item-id>"
---

# Switch Active Work Item

You are switching to a different work item from the backlog. This saves the current item's state and loads the new item's context.

## Arguments

- `<item-id>`: Required. The item ID to switch to (e.g., ITEM-001, ITEM-002)

## Examples

```
/flow-workflow:switch ITEM-001
/flow-workflow:switch ITEM-005
```

## What to Do

1. **Validate target item** exists
2. **Save current item state** (create checkpoint)
3. **Update ACTIVE.md** to new item
4. **Load new item context**
5. **Display new item status**
6. **Suggest next action**

## Switch Protocol

### Step 1: Validate Target

Check that target item exists:
- `.flow/items/ITEM-XXX/` directory exists
- STATE.md exists in that directory

If not found:
```markdown
**Item Not Found**

ITEM-XXX does not exist in the backlog.

**Available items**:
- ITEM-001: [title] ([status])
- ITEM-002: [title] ([status])

Use `/flow-workflow:backlog` to see all items.
```

### Step 2: Save Current Item

If there's a current active item:

1. Read current item from ACTIVE.md
2. Create checkpoint in current item's STATE.md:

```markdown
### CHECKPOINT: SWITCH-[TIMESTAMP]
**Phase**: [current phase]
**Progress**: [X]%
**Reason**: Switching to ITEM-XXX
**Completed**:
- [x] [completed items]
**Pending**:
- [ ] [pending items]
**Next Action**: [what to do when returning]
```

3. Update current item's status in BACKLOG.md (preserve phase)

### Step 3: Update ACTIVE.md

```markdown
# Active Work Item

**Current Item**: ITEM-XXX
**Switched At**: [TIMESTAMP]

## Quick Context

**Title**: [new item title]
**Status**: [new item phase]
**Progress**: [new item progress]%

**Last Checkpoint**: [if any]
**Next Action**: [recommended action]

## Recent Items

| Item | Title | Last Active | Status |
|------|-------|-------------|--------|
| ITEM-XXX | [new item] | [now] | [status] |
| [previous] | [title] | [timestamp] | [status] |

## Switch History

| Timestamp | From | To | Reason |
|-----------|------|-----|--------|
| [now] | [previous] | ITEM-XXX | User requested |
```

### Step 4: Load New Item Context

Read from `.flow/items/ITEM-XXX/`:
- STATE.md for current phase and progress
- Recent checkpoint for context
- Phase-specific files as needed

### Step 5: Display Status

```markdown
**Switched to ITEM-XXX**

## [Title]

**Status**: [phase]
**Progress**: [X]%
**Priority**: [priority]

### Current State

[Phase-specific summary]

### Last Activity

[From most recent checkpoint or phase history]

### Next Action

Based on current phase:
- BACKLOG: `/flow-workflow:discuss` to start
- DISCUSS: Continue requirements exploration
- PLAN: Continue task planning
- EXECUTE: Continue task execution
- VERIFY: Continue verification
```

## Phase-Specific Context Loading

### If BACKLOG Status
```markdown
**Item not yet started**

This item is in the backlog awaiting discussion.

To begin: `/flow-workflow:discuss`
```

### If DISCUSS Phase
```markdown
**Exploration in progress**

**Coverage**: [X]% explored
**Decisions made**: [N]

**Current area**: [from EXPLORATION.md]

To continue: Answer questions or navigate exploration map
```

### If PLAN Phase
```markdown
**Planning in progress**

**Tasks defined**: [N]
**Plan status**: [DRAFT/APPROVED]

To continue: Complete task planning or approve plan
```

### If EXECUTE Phase
```markdown
**Execution in progress**

**Progress**: [X/Y] tasks completed
**Current task**: TASK-XXX - [name]

To continue: `/flow-workflow:execute`
```

### If VERIFY Phase
```markdown
**Verification in progress**

**Automated checks**: [status]
**Requirements verified**: [X/Y]

To continue: `/flow-workflow:verify`
```

### If ON_HOLD or BLOCKED
```markdown
**Item is [ON_HOLD/BLOCKED]**

**Reason**: [reason from STATE.md]
**Since**: [timestamp]

To resume: Address the blocking issue, then continue
```

## Switching to Completed Item

```markdown
**Note: ITEM-XXX is already complete**

Completed: [timestamp]

You can:
1. View the completed state (read-only)
2. Switch to a different item
3. Create a follow-up item: `/flow-workflow:new [follow-up title]`
```

## No Current Active Item

If switching when no item is active:

```markdown
**Activating ITEM-XXX**

(No previous item to save)

[Display new item status]
```

## Error Handling

### Same Item
```markdown
**Already Active**

ITEM-XXX is already the active item.

Use `/flow-workflow:status` to see current state.
```

### Corrupted State
```markdown
**Warning: Item State Issue**

ITEM-XXX exists but STATE.md is missing or corrupted.

**Options**:
1. Reinitialize item state
2. Choose different item
3. Check .flow/items/ITEM-XXX/ manually
```

## Output Format

```markdown
**Switched: [Previous] → ITEM-XXX**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## ITEM-XXX: [Title]

**Phase**: [phase]
**Progress**: [X]%

[Phase-specific context]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Previous item saved**: [checkpoint info]

**Next action**: [recommended command or action]
```

## Skills Used

- **state-management**: Reading and updating state files
- **workflow-orchestration**: Context switching and checkpoints
