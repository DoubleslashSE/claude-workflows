---
name: discuss
description: Explore requirements and make decisions through adaptive questioning. Records findings in EXPLORATION.md and STATE.md.
user_invocable: true
args: "[topic]"
---

# Discuss Phase

You are starting or continuing the DISCUSS phase of the flow-workflow. This phase explores requirements through adaptive questioning and records decisions.

## What to Do

1. **Check for active work item** from ACTIVE.md
2. **Initialize or resume** DISCUSS phase
3. **Spawn interviewer agent** to conduct exploration
4. **Maintain exploration map** in item's EXPLORATION.md
5. **Record decisions** in item's STATE.md
6. **Detect and resolve conflicts**
7. **Complete when coverage sufficient**

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
- `.flow/items/ITEM-XXX/EXPLORATION.md`
- `.flow/items/ITEM-XXX/REQUIREMENTS.md`

## Starting DISCUSS Phase

### Check Current State

After confirming active item, verify workflow state:
- Does item directory exist? If not, run init first
- Is current phase compatible with DISCUSS?
  - From BACKLOG: Start fresh DISCUSS
  - From DISCUSS: Resume
  - From PLAN+: May need to backtrack

### Update Item STATE.md

Update `.flow/items/ITEM-XXX/STATE.md`:

```markdown
## Current Phase

**Phase**: DISCUSS
**Started**: [TIMESTAMP]
**Progress**: 0%
```

Also update `.flow/BACKLOG.md` to reflect item status change to DISCUSS.

### Initialize EXPLORATION.md

If not exists, create `.flow/items/ITEM-XXX/EXPLORATION.md`:

```markdown
# Exploration Map

**Topic**: [from args or user request]
**Started**: [TIMESTAMP]
**Last Updated**: [TIMESTAMP]
**Status**: IN_PROGRESS

## Territory Map

```
[TOPIC]
├── ○ UNCHARTED: [Area 1]
├── ○ UNCHARTED: [Area 2]
├── ○ UNCHARTED: [Area 3]
└── ○ UNCHARTED: [Area 4]
```

## Status Legend
- ✓ EXPLORED: Fully discussed, decisions made
- ◐ PARTIAL: Started but incomplete
- → CURRENT: Currently exploring
- ○ UNCHARTED: Identified but not yet explored
- ⊘ SKIPPED: User chose to skip (with reason)
- ⚑ FLAGGED: Needs follow-up or has blockers

## Exploration Log

[Log entries will be added here]

## Summary of Findings

[Summaries will be added here]
```

## Spawn Interviewer Agent

Use the Task tool to spawn the interviewer agent:

```markdown
Spawn flow-workflow:interviewer agent with context:
- Active item: ITEM-XXX
- Item directory: .flow/items/ITEM-XXX/
- Topic: [from args or item title]
- Current exploration map (if resuming)
- Decisions made so far
- Active conflicts
```

The interviewer will:
1. Ask adaptive questions using AskUserQuestion
2. Update item's EXPLORATION.md with findings
3. Record decisions in item's STATE.md
4. Detect and present conflicts
5. Track coverage of topic areas

## DISCUSS Phase Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    DISCUSS PHASE FLOW                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. START                                                       │
│     └─ Initialize exploration map with topic areas              │
│                                                                 │
│  2. EXPLORE LOOP                                                │
│     ├─ Select current area                                      │
│     ├─ Ask adaptive questions                                   │
│     ├─ Record findings and decisions                            │
│     ├─ Check for conflicts                                      │
│     ├─ Update exploration map                                   │
│     └─ Offer checkpoint/navigation choices                      │
│                                                                 │
│  3. CHECKPOINT (periodic)                                       │
│     ├─ Display exploration map                                  │
│     ├─ Summarize findings                                       │
│     └─ User chooses: continue, skip, complete                   │
│                                                                 │
│  4. COMPLETE (when user signals or coverage sufficient)         │
│     ├─ Coverage analysis                                        │
│     ├─ Document uncharted areas                                 │
│     ├─ Generate REQUIREMENTS.md                                 │
│     └─ Transition to PLAN phase                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Completing DISCUSS Phase

### Coverage Check

Before completing, calculate coverage:

```markdown
Coverage Analysis:
- Total areas identified: [N]
- Fully explored: [X] (✓)
- Partially explored: [Y] (◐)
- Uncharted: [Z] (○)
- Skipped: [W] (⊘)

Coverage: [X/(N-W)]%
```

### Coverage Thresholds

| Coverage | Action |
|----------|--------|
| 90%+ | Safe to complete |
| 70-89% | Review uncharted with user |
| <70% | Continue DISCUSS |

### Generate REQUIREMENTS.md

On completion, create `.flow/items/ITEM-XXX/REQUIREMENTS.md` from findings:

```markdown
# Requirements

**Created**: [TIMESTAMP]
**Last Updated**: [TIMESTAMP]
**Status**: DRAFT

## Functional Requirements

### FR-001: [Title]
**Priority**: [MUST/SHOULD/COULD]
**Description**: [from exploration findings]
**Acceptance Criteria**:
- [ ] [criterion]
**Source**: DECISION-XXX

[Additional requirements...]

## Non-Functional Requirements

### NFR-001: [Title]
**Category**: [Performance/Security/Usability]
**Description**: [requirement]
**Metric**: [how to measure]
**Target**: [specific target]

## Requirement Traceability

| Requirement | Source | Status |
|-------------|--------|--------|
| FR-001 | DECISION-001 | PENDING |
```

### Update Item STATE.md

Update `.flow/items/ITEM-XXX/STATE.md`:

```markdown
## Current Phase

**Phase**: DISCUSS
**Started**: [original timestamp]
**Progress**: 100%
**Completed**: [TIMESTAMP]

### CHECKPOINT: DISCUSS-COMPLETE-[TIMESTAMP]
**Completed**:
- [x] Explored [N] topic areas
- [x] Made [N] decisions
- [x] Resolved [N] conflicts
- [x] Generated REQUIREMENTS.md

**Next Action**: Run /flow-workflow:plan to create execution plan
```

Also update `.flow/BACKLOG.md` with item's progress (DISCUSS complete, ready for PLAN).

## Output Format

### Starting DISCUSS

```markdown
**DISCUSS Phase Started**

**Work Item**: ITEM-XXX - [Title]
**Topic**: [topic]
**Initial areas identified**: [N]

Beginning requirements exploration. The interviewer will guide you through
adaptive questions to understand your needs.

[Spawning interviewer agent...]
```

### During DISCUSS

The interviewer agent handles interaction, updating:
- Item's EXPLORATION.md with territory map
- Item's STATE.md with decisions
- BACKLOG.md with progress
- Presenting checkpoints to user

### Completing DISCUSS

```markdown
**DISCUSS Phase Complete**

**Work Item**: ITEM-XXX - [Title]
**Coverage**: [X]%
**Decisions made**: [N]
**Conflicts resolved**: [N]
**Uncharted areas**: [list or "None"]

**Generated**: .flow/items/ITEM-XXX/REQUIREMENTS.md with [N] requirements

**Next**: Run `/flow-workflow:plan` to create execution plan
```

## Skills Used

- **exploration-tracking**: For map management
- **conflict-detection**: For identifying conflicts
- **state-management**: For state updates

## Agent Spawned

- **interviewer**: Conducts adaptive questioning session
