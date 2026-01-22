# State File Templates

## BACKLOG.md Template

```markdown
# Work Item Backlog

**Created**: [TIMESTAMP]
**Last Updated**: [TIMESTAMP]
**Total Items**: [N]

## Backlog Summary

| Status | Count |
|--------|-------|
| BACKLOG | [N] |
| DISCUSS | [N] |
| PLAN | [N] |
| EXECUTE | [N] |
| VERIFY | [N] |
| ON_HOLD | [N] |
| BLOCKED | [N] |
| COMPLETE | [N] |

## Active Item

**Current**: [ITEM-XXX] - [Title] (or "None")

## Work Items

### ITEM-001: [Title]
**Status**: [BACKLOG | DISCUSS | PLAN | EXECUTE | VERIFY | COMPLETE | ON_HOLD | BLOCKED]
**Priority**: [P0 | P1 | P2 | P3]
**Created**: [TIMESTAMP]
**Updated**: [TIMESTAMP]
**Description**: [Brief description of the work item]
**Phase Progress**: [0-100]%
**Tags**: [tag1, tag2]

### ITEM-002: [Title]
**Status**: [status]
**Priority**: [priority]
**Created**: [TIMESTAMP]
**Updated**: [TIMESTAMP]
**Description**: [Brief description]
**Phase Progress**: [0-100]%
**Tags**: [tags]

## Completed Items

### ITEM-000: [Title]
**Completed**: [TIMESTAMP]
**Duration**: [time from creation to completion]
**Summary**: [What was delivered]

## Backlog Views

### By Priority
#### P0 - Critical
- ITEM-XXX: [Title] ([Status])

#### P1 - High
- ITEM-XXX: [Title] ([Status])

#### P2 - Medium
- ITEM-XXX: [Title] ([Status])

#### P3 - Low
- ITEM-XXX: [Title] ([Status])

### By Status
#### In Progress (DISCUSS/PLAN/EXECUTE/VERIFY)
- ITEM-XXX: [Title] ([Phase] - [Progress]%)

#### Ready to Start (BACKLOG)
- ITEM-XXX: [Title]

#### Blocked/On Hold
- ITEM-XXX: [Title] - [Reason]
```

## ACTIVE.md Template

```markdown
# Active Work Item

**Current Item**: [ITEM-XXX] (or "None")
**Switched At**: [TIMESTAMP]

## Quick Context

**Title**: [Work item title]
**Status**: [Current phase]
**Progress**: [Phase progress]%

**Last Checkpoint**: [CHECKPOINT-ID]
**Next Action**: [What to do next]

## Recent Items

| Item | Title | Last Active | Status |
|------|-------|-------------|--------|
| ITEM-XXX | [Title] | [TIMESTAMP] | [Status] |
| ITEM-YYY | [Title] | [TIMESTAMP] | [Status] |

## Switch History

| Timestamp | From | To | Reason |
|-----------|------|-----|--------|
| [TS] | ITEM-XXX | ITEM-YYY | [reason] |
```

## STATE.md Template (Per-Item)

```markdown
# Workflow State

**Session Started**: [TIMESTAMP]
**Last Updated**: [TIMESTAMP]

## Current Phase

**Phase**: [INIT | DISCUSS | PLAN | EXECUTE | VERIFY | COMPLETE]
**Started**: [TIMESTAMP]
**Progress**: [0-100]%

## Session Context

**Original Request**:
> [User's original request or goal]

**Goals**:
1. [Primary goal]
2. [Secondary goal]

**Constraints**:
- [Constraint 1]
- [Constraint 2]

## Decisions

### DECISION-001: [Title]
**Made**: [TIMESTAMP]
**Phase**: [DISCUSS | PLAN]
**Decision**: [What was decided]
**Rationale**: [Why this decision]
**Alternatives Considered**:
- [Alternative 1]: [Why rejected]
- [Alternative 2]: [Why rejected]

## Conflicts

### CONFLICT-001: [Title]
**Status**: [ACTIVE | RESOLVED | DEFERRED]
**Detected**: [TIMESTAMP]
**Type**: [Requirement | Decision | Plan | Technical]

**What conflicts:**
- A: [First item]
- B: [Second item]

**Why they conflict:**
[Explanation]

**Resolution options:**
1. [Option 1]
2. [Option 2]

**Resolution**: [PENDING | Chose option X]
**Rationale**: [Why this resolution]
**Resolved**: [TIMESTAMP]

## Blockers

### BLOCKER-001: [Title]
**Status**: [ACTIVE | RESOLVED]
**Detected**: [TIMESTAMP]
**Impact**: [What's blocked]
**Resolution**: [How resolved or pending action]

## Checkpoints

### CHECKPOINT: [PHASE]-[TIMESTAMP]
**Phase**: [Phase name]
**Completed**:
- [x] [Completed item 1]
- [x] [Completed item 2]

**Pending**:
- [ ] [Pending item 1]
- [ ] [Pending item 2]

**Next Action**: [What to do next]

**State Snapshot**:
```
[Key state values at checkpoint]
```

## Available Capabilities

| Capability | Matched Plugin | Agent/Command |
|------------|----------------|---------------|
| [capability] | [plugin-name] | [agent:name or command] |

**Project Type**: [Detected type or "Not detected"]
**Last Scanned**: [TIMESTAMP]

## Phase History

| Phase | Started | Completed | Duration |
|-------|---------|-----------|----------|
| INIT | [TS] | [TS] | [duration] |
| DISCUSS | [TS] | [TS] | [duration] |
```

## PROJECT.md Template

```markdown
# Project Overview

**Created**: [TIMESTAMP]
**Last Updated**: [TIMESTAMP]

## Vision

[High-level project vision statement]

## Scope

### In Scope
- [Feature/capability 1]
- [Feature/capability 2]

### Out of Scope
- [Explicitly excluded item 1]
- [Explicitly excluded item 2]

## Stakeholders

| Role | Interest | Key Concerns |
|------|----------|--------------|
| [Role] | [What they care about] | [Main concerns] |

## Success Criteria

- [ ] [Criterion 1]
- [ ] [Criterion 2]

## Technical Context

**Stack**: [Technologies/frameworks]
**Repository**: [Path or URL]
**Key Files**:
- `[path]`: [Purpose]

## Constraints

### Technical Constraints
- [Constraint 1]

### Business Constraints
- [Constraint 1]

### Timeline
[Any timeline considerations]
```

## REQUIREMENTS.md Template

```markdown
# Requirements

**Created**: [TIMESTAMP]
**Last Updated**: [TIMESTAMP]
**Status**: [DRAFT | REVIEWED | APPROVED]

## Functional Requirements

### FR-001: [Title]
**Priority**: [MUST | SHOULD | COULD | WONT]
**Status**: [PENDING | PLANNED | IMPLEMENTED | VERIFIED]
**Description**: [What the system must do]
**Acceptance Criteria**:
- [ ] [Criterion 1]
- [ ] [Criterion 2]
**Source**: [DECISION-XXX or stakeholder]
**Tasks**: [TASK-XXX, TASK-YYY]

## Non-Functional Requirements

### NFR-001: [Title]
**Category**: [Performance | Security | Usability | Reliability]
**Priority**: [MUST | SHOULD | COULD]
**Description**: [Quality attribute requirement]
**Metric**: [How to measure]
**Target**: [Specific target value]

## Requirement Traceability

| Requirement | Source | Tasks | Status |
|-------------|--------|-------|--------|
| FR-001 | DECISION-001 | TASK-001, TASK-002 | PLANNED |

## Open Questions

- [ ] [Question 1]
- [ ] [Question 2]
```

## ROADMAP.md Template

```markdown
# Roadmap

**Created**: [TIMESTAMP]
**Last Updated**: [TIMESTAMP]

## Milestones

### M1: [Milestone Name]
**Target**: [Date or "Next"]
**Status**: [NOT_STARTED | IN_PROGRESS | COMPLETED]
**Description**: [What this milestone delivers]

**Deliverables**:
- [ ] [Deliverable 1]
- [ ] [Deliverable 2]

**Tasks**:
- [ ] TASK-001: [Name]
- [ ] TASK-002: [Name]

**Progress**: [0-100]%

## Progress Summary

| Milestone | Tasks | Completed | Progress |
|-----------|-------|-----------|----------|
| M1 | 5 | 2 | 40% |

## Timeline

```
[Current] ─── M1 ─── M2 ─── M3 ─── [Done]
              ↑
           You are here
```

## Risks

### RISK-001: [Title]
**Probability**: [LOW | MEDIUM | HIGH]
**Impact**: [LOW | MEDIUM | HIGH]
**Mitigation**: [Strategy]
```

## EXPLORATION.md Template

```markdown
# Exploration Map

**Topic**: [What we're discussing]
**Started**: [TIMESTAMP]
**Last Updated**: [TIMESTAMP]
**Status**: [IN_PROGRESS | COMPLETE]

## Territory Map

```
[MAIN TOPIC]
├── ✓ EXPLORED: [Area 1]
│   ├── ✓ [Sub-area 1.1] - [Summary of findings]
│   └── ◐ PARTIAL: [Sub-area 1.2] - [What we know, what's unclear]
├── → CURRENT: [Area 2]
│   └── ○ UNCHARTED: [Sub-area 2.1]
├── ○ UNCHARTED: [Area 3]
│   └── [Suspected topics to explore]
└── ⊘ SKIPPED: [Area 4] - [Reason skipped]
```

## Status Legend
- ✓ EXPLORED: Fully discussed, decisions made
- ◐ PARTIAL: Started but incomplete
- → CURRENT: Currently exploring
- ○ UNCHARTED: Identified but not yet explored
- ⊘ SKIPPED: User chose to skip (with reason)
- ⚑ FLAGGED: Needs follow-up or has blockers

## Exploration Log

### [TIMESTAMP] - [Area]
**Status**: [EXPLORED | PARTIAL | SKIPPED]
**Findings**:
- [Key finding 1]
- [Key finding 2]

**Decisions Made**:
- DECISION-XXX: [Summary]

**Questions Raised**:
- [Question 1]

**Next**: [What to explore next]

## Summary of Findings

### [Area 1]
[Consolidated findings from exploration]

### [Area 2]
[Consolidated findings from exploration]

## Uncharted Territory

Areas identified but not yet explored:
1. [Area] - [Why identified, suspected relevance]
2. [Area] - [Why identified, suspected relevance]

## Skipped Areas

| Area | Reason Skipped | Revisit Later? |
|------|----------------|----------------|
| [Area] | [Reason] | [Yes/No] |
```

## PLAN.md Template

```markdown
# Execution Plan

**Created**: [TIMESTAMP]
**Last Updated**: [TIMESTAMP]
**Status**: [DRAFT | APPROVED | IN_PROGRESS | COMPLETED]

## Plan Summary

**Total Tasks**: [N]
**Completed**: [M]
**Progress**: [%]

## Cross-Plan Verification

**Against REQUIREMENTS.md:**
- [x] All requirements have at least one task
- [x] No tasks contradict requirements
- [x] Priority order respected

**Against STATE.md decisions:**
- [x] Tasks align with recorded decisions
- [x] No tasks contradict decisions

## Tasks

<task id="TASK-001" status="pending">
  <name>[Task name]</name>
  <description>[What this task accomplishes]</description>
  <depends>[TASK-XXX, TASK-YYY]</depends>
  <files>
    <file action="create">[path/to/new/file]</file>
    <file action="modify">[path/to/existing/file]</file>
  </files>
  <actions>
    <action>[Specific action 1]</action>
    <action>[Specific action 2]</action>
  </actions>
  <verify>
    <step>[Verification command or check]</step>
    <step>[Another verification]</step>
  </verify>
  <done>
    <criterion>[Completion criterion 1]</criterion>
    <criterion>[Completion criterion 2]</criterion>
  </done>
  <commit>[Conventional commit message]</commit>
</task>

## Task Dependencies

```
TASK-001 ──┬── TASK-003
           │
TASK-002 ──┘
           │
           └── TASK-004 ── TASK-005
```

## Execution Order

1. [ ] TASK-001: [Name] (no dependencies)
2. [ ] TASK-002: [Name] (no dependencies)
3. [ ] TASK-003: [Name] (depends: TASK-001, TASK-002)
4. [ ] TASK-004: [Name] (depends: TASK-003)
5. [ ] TASK-005: [Name] (depends: TASK-004)
```
