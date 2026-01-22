---
name: resume
description: Resume workflow from STATE.md checkpoint after interruption
user_invocable: true
args: "[ITEM-XXX]"
---

# Resume Workflow

You are resuming the flow-workflow from its last checkpoint. This command reconstructs context from state files and continues where the workflow left off.

## What to Do

1. **Check for active work item** from ACTIVE.md (or use specified item)
2. **Read item's STATE.md** to understand current state
3. **Find most recent checkpoint** in item's STATE.md
4. **Reconstruct context** from item's state files
5. **Identify next action** from checkpoint
6. **Continue workflow** from that point

## Active Item Resolution

### Determine Which Item to Resume

1. **If ITEM-XXX specified**: Resume that specific item
2. **If no item specified**: Use active item from `.flow/ACTIVE.md`
3. **If no active item**: Show list of items and prompt for selection

```markdown
# No Active Item

There is no active work item. Which item would you like to resume?

| Item | Title | Status | Progress |
|------|-------|--------|----------|
| ITEM-001 | [Title] | EXECUTE | 60% |
| ITEM-002 | [Title] | DISCUSS | 30% |

Use `/flow-workflow:resume ITEM-XXX` to specify, or `/flow-workflow:switch ITEM-XXX` to activate one.
```

### Item State Directory

All state files are stored in the active item's directory:
- `.flow/items/ITEM-XXX/STATE.md`
- `.flow/items/ITEM-XXX/EXPLORATION.md`
- `.flow/items/ITEM-XXX/REQUIREMENTS.md`
- `.flow/items/ITEM-XXX/PLAN.md`
- `.flow/items/ITEM-XXX/ROADMAP.md`

## Resume Protocol

### Step 1: Validate State

Check that `.flow/` exists and contains valid state for the item:

```markdown
Required files:
- .flow/ACTIVE.md (project-level)
- .flow/items/ITEM-XXX/STATE.md (required)
- .flow/PROJECT.md (optional, shared)
- .flow/items/ITEM-XXX/PLAN.md (if PLAN phase or later)
- .flow/items/ITEM-XXX/EXPLORATION.md (if DISCUSS phase or later)
- .flow/items/ITEM-XXX/REQUIREMENTS.md (if PLAN phase or later)
```

### Step 2: Read Current State

From item's STATE.md (`.flow/items/ITEM-XXX/STATE.md`), extract:
- Current phase
- Phase progress
- Most recent checkpoint
- Active blockers
- Active conflicts

### Step 3: Find Checkpoint

Locate the most recent checkpoint in STATE.md:

```markdown
### CHECKPOINT: [PHASE]-[TIMESTAMP]
**Phase**: [phase]
**Completed**:
- [x] [item 1]
- [x] [item 2]

**Pending**:
- [ ] [item 1]
- [ ] [item 2]

**Next Action**: [what to do]
```

### Step 4: Reconstruct Context

Based on current phase, load relevant context from item directory:

| Phase | Load |
|-------|------|
| DISCUSS | item's STATE.md, PROJECT.md (shared), item's EXPLORATION.md |
| PLAN | item's STATE.md, item's REQUIREMENTS.md, item's EXPLORATION.md |
| EXECUTE | item's STATE.md, item's PLAN.md, item's REQUIREMENTS.md |
| VERIFY | item's STATE.md, item's PLAN.md, item's REQUIREMENTS.md |

### Step 5: Continue Workflow

Based on checkpoint's "Next Action", either:
- Spawn appropriate agent
- Present status and options to user
- Continue from specific point

## Resume Scenarios

### Resume DISCUSS Phase

```markdown
**Resuming DISCUSS Phase**

**Work Item**: ITEM-XXX - [Title]

**Context loaded**:
- Project: [project summary]
- Decisions made: [N]
- Exploration progress: [X]%

**Last checkpoint**: [DISCUSS-TIMESTAMP]
**Next action**: [from checkpoint]

**Exploration map**:
[Current territory map]

Ready to continue discussion. Would you like to:
1. Continue exploring [current area]
2. Move to [next uncharted area]
3. Review decisions made so far
4. Complete DISCUSS and move to PLAN
```

### Resume PLAN Phase

```markdown
**Resuming PLAN Phase**

**Work Item**: ITEM-XXX - [Title]

**Context loaded**:
- Requirements: [N] functional, [N] non-functional
- Plan status: [DRAFT/IN_PROGRESS]

**Last checkpoint**: [PLAN-TIMESTAMP]
**Next action**: [from checkpoint]

**Plan progress**:
- Tasks defined: [N]
- Verification needed: [items]

Ready to continue planning. Would you like to:
1. Continue creating tasks
2. Review current plan
3. Run cross-plan verification
4. Approve plan and start execution
```

### Resume EXECUTE Phase

```markdown
**Resuming EXECUTE Phase**

**Work Item**: ITEM-XXX - [Title]

**Context loaded**:
- Tasks: [completed]/[total]
- Current task: [TASK-XXX] - [name]
- Task status: [status]

**Last checkpoint**: [EXECUTE-TIMESTAMP]
**Next action**: [from checkpoint]

**Task progress**:
```
[===========         ] 55% (11/20 tasks)
```

**Current task details**:
[Task summary]

Ready to continue execution. Would you like to:
1. Continue current task
2. Skip to next task
3. Review task dependencies
4. Check for blocked tasks
```

### Resume VERIFY Phase

```markdown
**Resuming VERIFY Phase**

**Work Item**: ITEM-XXX - [Title]

**Context loaded**:
- Automated checks: [status]
- Requirements verified: [X/Y]
- UAT progress: [status]

**Last checkpoint**: [VERIFY-TIMESTAMP]
**Next action**: [from checkpoint]

Ready to continue verification. Would you like to:
1. Continue automated checks
2. Continue requirements verification
3. Continue UAT
4. Review verification results
```

## Handling Issues

### Missing State Files

If required files are missing:

```markdown
**Cannot Resume: Missing State**

The following required files are missing:
- [file 1]
- [file 2]

**Options**:
1. Run `/flow-workflow:init` to reinitialize
2. Manually create missing files
3. Start new workflow with `/flow-workflow:flow`
```

### Corrupted State

If state files can't be parsed:

```markdown
**Cannot Resume: Invalid State**

STATE.md could not be parsed correctly.

**Issues found**:
- [issue 1]
- [issue 2]

**Options**:
1. Manually fix STATE.md
2. Reset to last valid checkpoint
3. Reinitialize with `/flow-workflow:init`
```

### Active Blockers

If blockers prevent resumption:

```markdown
**Resume Blocked**

Active blockers prevent continuation:

### BLOCKER-001: [Title]
[details]

**Options**:
1. Resolve blocker first
2. Skip blocked work (if possible)
3. Reset to before blocker
```

## Output Format

```markdown
# Workflow Resumed

**Work Item**: ITEM-XXX - [Title]
**Restored from**: CHECKPOINT [PHASE]-[TIMESTAMP]
**Current phase**: [PHASE]
**Progress**: [X]%

## Context Summary

[Phase-appropriate context summary]

## Next Steps

Based on checkpoint: [next action]

**Options**:
1. [Recommended option]
2. [Alternative option]
3. [Other option]

## Backlog Status

Other items in backlog:
- ITEM-YYY: [Status] - [Title]
- ITEM-ZZZ: [Status] - [Title]

Switch item: `/flow-workflow:switch ITEM-XXX`
```

## Skills Used

- **state-management**: For reading and interpreting state files
- **workflow-orchestration**: For determining next steps
