---
name: quick
description: Lightweight workflow path for small tasks that still maintains state tracking
user_invocable: true
args: "<task description>"
---

# Quick Mode Workflow

You are running a lightweight workflow for a small, well-defined task. Quick mode skips deep requirements gathering while still maintaining state tracking and backlog integration.

## When to Use Quick Mode

Quick mode is appropriate for:
- Single, well-defined changes
- Bug fixes with clear scope
- Small features with obvious requirements
- Tasks that don't need extensive discussion

Quick mode is NOT appropriate for:
- Complex features with unclear requirements
- Changes that affect multiple systems
- Work requiring stakeholder input
- Tasks with potential conflicts

## What Quick Mode Does

1. **Create Work Item**: Add to backlog with QUICK mode marker
2. **Minimal DISCUSS**: Ask clarifying questions only if needed
3. **Rapid PLAN**: Create 1-3 atomic tasks
4. **Focused EXECUTE**: Implement tasks
5. **Quick VERIFY**: Run automated checks + brief UAT
6. **Mark Complete**: Update backlog and close item

## Quick Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    QUICK MODE FLOW                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. CREATE WORK ITEM                                            │
│     ├─ Generate ITEM-XXX                                        │
│     ├─ Add to BACKLOG.md with mode=QUICK                        │
│     ├─ Create .flow/items/ITEM-XXX/                             │
│     └─ Set as active in ACTIVE.md                               │
│                                                                 │
│  2. ASSESS                                                      │
│     ├─ Is task clear enough for quick mode?                     │
│     ├─ Any obvious conflicts with existing work?                │
│     └─ If unclear → suggest full workflow                       │
│                                                                 │
│  3. CLARIFY (if needed)                                         │
│     ├─ Ask 1-2 critical questions only                          │
│     └─ Record key decisions in item's STATE.md                  │
│                                                                 │
│  4. QUICK PLAN                                                  │
│     ├─ Create 1-3 atomic tasks in item's PLAN.md                │
│     ├─ Define verification steps                                │
│     └─ No extensive requirements doc                            │
│                                                                 │
│  5. IMPLEMENT                                                   │
│     ├─ Execute tasks                                            │
│     ├─ Verify each task                                         │
│     └─ Commit on success                                        │
│                                                                 │
│  6. QUICK VERIFY                                                │
│     ├─ Run automated checks                                     │
│     ├─ Brief confirmation with user                             │
│     └─ Mark item COMPLETE in BACKLOG.md                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Starting Quick Mode

### Create Work Item

First, create a work item in the backlog:

1. **Generate next item ID** (ITEM-XXX)
2. **Create item directory**: `.flow/items/ITEM-XXX/`
3. **Add to BACKLOG.md** with mode=QUICK
4. **Set as active** in ACTIVE.md

### Initialize Minimal State

Create `.flow/items/ITEM-XXX/STATE.md` with minimal state:

```markdown
# Workflow State

**Work Item**: ITEM-XXX
**Title**: [task description]
**Session Started**: [TIMESTAMP]
**Mode**: QUICK

## Current Phase

**Phase**: QUICK
**Task**: [task description]
**Progress**: 0%

## Quick Decisions

[Any decisions made during clarification]

## Tasks

[Quick task list]
```

### Assess Task Suitability

Check if task is suitable for quick mode:

```markdown
**Quick Mode Assessment**

Task: [task description]

**Suitability check**:
- [ ] Single, focused change
- [ ] Clear requirements (no ambiguity)
- [ ] Limited scope (1-5 files)
- [ ] No complex dependencies
- [ ] No stakeholder input needed

**Assessment**: [SUITABLE / RECOMMEND_FULL_WORKFLOW]
```

If not suitable:
```markdown
**Task May Be Too Complex for Quick Mode**

This task might benefit from full workflow because:
- [reason 1]
- [reason 2]

**Options**:
1. Continue with quick mode anyway
2. Switch to full workflow: `/flow-workflow:flow [task]`
```

## Clarification (If Needed)

Only ask questions that are critical:

```javascript
AskUserQuestion({
  questions: [{
    question: "Quick clarification: [specific question]?",
    header: "Clarify",
    multiSelect: false,
    options: [
      { label: "[Option A]", description: "[brief description]" },
      { label: "[Option B]", description: "[brief description]" }
    ]
  }]
})
```

Record any decisions in item's STATE.md but skip full EXPLORATION.md.

## Quick Planning

Create minimal `.flow/items/ITEM-XXX/PLAN.md`:

```markdown
# Quick Plan

**Work Item**: ITEM-XXX
**Task**: [task description]
**Created**: [TIMESTAMP]
**Mode**: QUICK

## Tasks

<task id="TASK-001" status="pending">
  <name>[task name]</name>
  <description>[brief description]</description>
  <files>
    <file action="[action]">[path]</file>
  </files>
  <actions>
    <action>[action]</action>
  </actions>
  <verify>
    <step>[verification]</step>
  </verify>
  <done>
    <criterion>[done criterion]</criterion>
  </done>
  <commit>[commit message]</commit>
</task>
```

## Implementation

Execute tasks as in normal workflow:
1. Mark task in_progress
2. Execute actions
3. Run verification
4. Commit on success
5. Mark completed

## Quick Verification

Run automated checks:

```bash
# Build
[build command]

# Tests (relevant subset)
[test command]

# Lint (changed files only)
[lint command]
```

Brief UAT:

```javascript
AskUserQuestion({
  questions: [{
    question: "Does this change work as expected?",
    header: "Quick UAT",
    multiSelect: false,
    options: [
      { label: "Yes, looks good", description: "Change works correctly" },
      { label: "No, needs adjustment", description: "Something isn't right" }
    ]
  }]
})
```

## Completion

### Quick Complete

```markdown
**Quick Mode Complete**

**Work Item**: ITEM-XXX - [task description]
**Duration**: [time]
**Commits**: [N]

**Changes made**:
- [summary of changes]

**Verification**:
- Build: PASS
- Tests: PASS
- User confirmation: YES

All done!
```

### Update State Files

Update `.flow/items/ITEM-XXX/STATE.md`:

```markdown
## Current Phase

**Phase**: COMPLETE
**Mode**: QUICK
**Completed**: [TIMESTAMP]

**Summary**:
- Tasks: [N]
- Commits: [N]
- Duration: [time]
```

Update `.flow/BACKLOG.md`:
- Mark ITEM-XXX as COMPLETE
- Update status counts

Update `.flow/ACTIVE.md`:
- Clear active item or suggest next item

## Escalation to Full Workflow

If during quick mode you discover:
- Task is more complex than expected
- Requirements are unclear
- Conflicts exist
- Multiple stakeholders needed

Escalate:

```markdown
**Escalating to Full Workflow**

Quick mode revealed this task is more complex:
- [reason]

Transitioning to full workflow mode...

State will be preserved and expanded.
```

## Output Format

### Starting Quick Mode

```markdown
**Quick Mode Started**

**Work Item**: ITEM-XXX - [task description]

**Plan**:
1. [Task 1 brief]
2. [Task 2 brief if any]

Beginning implementation...
```

### Progress

```markdown
**Quick Progress**: [X]/[Y] tasks

**Work Item**: ITEM-XXX
**Current**: [task name]
**Status**: [status]
```

### Completion

```markdown
**Quick Mode Complete**

**Work Item**: ITEM-XXX - [description]
**Result**: [summary]
**Duration**: [time]

**Backlog updated**: Item marked COMPLETE
```

## When to Switch to Full Workflow

Signs you should switch:
- More than 3 clarifying questions needed
- More than 5 tasks needed
- Touching more than 10 files
- Discovering unclear requirements
- Finding conflicts

Switching is always an option:
```markdown
This is getting complex. Would you like to switch to full workflow mode?
```

## Skills Used

- **atomic-tasks**: For task structure
- **state-management**: For minimal state tracking
