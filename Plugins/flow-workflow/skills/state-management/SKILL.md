---
name: state-management
description: State file management techniques for explicit workflow state tracking with multi-item backlog support
triggers:
  - workflow state
  - state files
  - STATE.md
  - checkpoint
  - resume
  - backlog
  - work item
---

# State Management Skill

This skill provides techniques for managing workflow state through explicit markdown files in the `.flow/` directory, with support for multiple work items (epics/stories) in a backlog.

## Core Principles

1. **Single Source of Truth**: BACKLOG.md tracks all work items, per-item STATE.md tracks each item's progress
2. **Human Readable**: All state files are plain markdown, easily reviewed and edited
3. **Checkpoint Recovery**: State enables resumption from any interruption point
4. **Phase Tracking**: Clear indication of current workflow phase and progress per work item
5. **Multi-Item Support**: Multiple plans/specs can exist in different states simultaneously

## Directory Structure

```
.flow/
├── BACKLOG.md              # Master list of all work items
├── ACTIVE.md               # Points to currently active work item
├── PROJECT.md              # Project-level context (shared)
├── capabilities.md         # Cached plugin capabilities (shared)
└── items/
    ├── ITEM-001/           # First work item (epic/story)
    │   ├── STATE.md        # Item-specific state and phase
    │   ├── EXPLORATION.md  # Item-specific exploration map
    │   ├── REQUIREMENTS.md # Item-specific requirements
    │   ├── PLAN.md         # Item-specific task plan
    │   └── ROADMAP.md      # Item-specific milestones
    ├── ITEM-002/           # Second work item
    │   └── ...
    └── ...
```

## State Files Overview

### Project-Level Files (Shared)

| File | Purpose | Updated |
|------|---------|---------|
| `BACKLOG.md` | Master list of all work items with status | When items created/updated |
| `ACTIVE.md` | Currently active work item pointer | When switching items |
| `PROJECT.md` | Vision, scope, stakeholders | At project initialization |
| `capabilities.md` | Cached plugin capabilities | At initialization |

### Per-Item Files (in items/ITEM-XXX/)

| File | Purpose | Updated |
|------|---------|---------|
| `STATE.md` | Current phase, decisions, blockers, checkpoints | Every phase transition |
| `REQUIREMENTS.md` | Functional/non-functional requirements | During DISCUSS/PLAN |
| `ROADMAP.md` | Milestones, progress tracking | During PLAN/EXECUTE |
| `PLAN.md` | XML-structured atomic tasks | During PLAN phase |
| `EXPLORATION.md` | Exploration map of discussed areas | During DISCUSS phase |

## STATE.md Structure

The STATE.md file tracks:

### Phase Information
- Current phase (INIT, DISCUSS, PLAN, EXECUTE, VERIFY, COMPLETE)
- Phase start timestamp
- Phase progress percentage

### Session Context
- Original user request
- Session goals
- Key constraints

### Decisions Made
- Numbered list of decisions with rationale
- Timestamp for each decision
- Links to supporting discussions

### Blockers and Conflicts
- Active blockers requiring resolution
- Detected conflicts between requirements/decisions
- Resolution status and options

### Checkpoints
- Named checkpoints for resume capability
- State snapshot at each checkpoint
- Next actions from checkpoint

### Capability Cache
- Discovered plugins and their capabilities
- Detected project type
- Capability-to-agent mappings

## Backlog Item States

Work items progress through these states:

| State | Description | Next States |
|-------|-------------|-------------|
| `BACKLOG` | Defined but not started | DISCUSS |
| `DISCUSS` | Gathering requirements | PLAN, BACKLOG |
| `PLAN` | Creating task plan | EXECUTE, DISCUSS |
| `EXECUTE` | Implementing tasks | VERIFY, PLAN |
| `VERIFY` | Validating implementation | COMPLETE, EXECUTE |
| `COMPLETE` | Done | (terminal) |
| `ON_HOLD` | Paused intentionally | Any |
| `BLOCKED` | Waiting on external dependency | Previous state |

## State Operations

### Initialize Project
```markdown
1. Create .flow/ directory if not exists
2. Create .flow/items/ directory
3. Create BACKLOG.md (empty backlog)
4. Create ACTIVE.md (no active item)
5. Scan for installed plugins
6. Cache capability mappings in capabilities.md
7. Create PROJECT.md stub
```

### Create New Work Item
```markdown
1. Generate next item ID (ITEM-XXX)
2. Create .flow/items/ITEM-XXX/ directory
3. Create STATE.md with BACKLOG status
4. Add entry to BACKLOG.md
5. Optionally set as active item
```

### Switch Active Item
```markdown
1. Verify target item exists
2. Create checkpoint for current item (if any)
3. Update ACTIVE.md to point to new item
4. Load new item's STATE.md
5. Report current phase and status
```

### Initialize Item State
```markdown
1. Create items/ITEM-XXX/ directory if not exists
2. Create STATE.md with INIT phase
3. Link to project-level capabilities
4. Create item-specific file stubs
```

### Update State on Phase Transition
```markdown
1. Update current phase in STATE.md
2. Record phase transition timestamp
3. Capture decisions made in previous phase
4. Create checkpoint for previous phase
5. Initialize next phase section
```

### Create Checkpoint
```markdown
1. Generate checkpoint name (PHASE-TIMESTAMP)
2. Snapshot current state section
3. List completed items
4. List pending items
5. Record next recommended action
```

### Resume from Checkpoint
```markdown
1. Read STATE.md
2. Find most recent checkpoint
3. Restore context from checkpoint
4. Identify next action
5. Continue workflow
```

## State Validation

Before any phase transition, validate:

1. **Completeness**: Required sections are filled
2. **Consistency**: No contradictory decisions
3. **Traceability**: All decisions have rationale
4. **Recoverability**: Checkpoint exists for current progress

## Best Practices

### Writing State Updates
- Use timestamps in ISO format
- Include brief rationale for decisions
- Reference related files/sections
- Mark status clearly (ACTIVE, RESOLVED, DEFERRED)

### Reading State for Context
- Load STATE.md first for current phase
- Load phase-specific files as needed
- Check for blockers before proceeding
- Verify checkpoint validity

### Handling Conflicts
- Document conflict immediately when detected
- Stop workflow until resolved
- Record resolution with rationale
- Update affected state sections

## Integration Points

State management integrates with:
- **Capability Discovery**: Cache plugin mappings in STATE.md
- **Conflict Detection**: Record conflicts and resolutions
- **Exploration Tracking**: Link EXPLORATION.md progress
- **Workflow Orchestration**: Phase transitions and handoffs

See `templates.md` for full file templates.
