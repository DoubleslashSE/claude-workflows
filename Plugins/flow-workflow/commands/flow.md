---
name: flow
description: Execute full workflow cycle (discuss → plan → execute → verify) for a given task or goal
user_invocable: true
args: "<task description>"
---

# Full Workflow Cycle

You are orchestrating a complete workflow cycle through all phases: DISCUSS → PLAN → EXECUTE → VERIFY.

## What to Do

1. **Initialize** if not already done
2. **Create work item** in backlog (or use active item)
3. **Set as active item**
4. **Run DISCUSS** phase to gather requirements
5. **Run PLAN** phase to create task plan
6. **Run EXECUTE** phase to implement tasks
7. **Run VERIFY** phase to validate
8. **Mark complete** and update backlog

## Arguments

`<task description>`: The goal or task to accomplish through the workflow

Examples:
- `/flow-workflow:flow Add user authentication`
- `/flow-workflow:flow Fix the cart calculation bug`
- `/flow-workflow:flow Implement dark mode support`

## Full Cycle Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    FULL WORKFLOW CYCLE                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. INITIALIZE                                                  │
│     ├─ Create .flow/ if needed                                  │
│     ├─ Scan capabilities                                        │
│     └─ Set up backlog structure                                 │
│                                                                 │
│  2. CREATE WORK ITEM                                            │
│     ├─ Generate ITEM-XXX                                        │
│     ├─ Add to BACKLOG.md                                        │
│     ├─ Create items/ITEM-XXX/ directory                         │
│     └─ Set as active in ACTIVE.md                               │
│                                                                 │
│  3. DISCUSS                                                     │
│     ├─ Explore requirements                                     │
│     ├─ Make decisions                                           │
│     ├─ Resolve conflicts                                        │
│     └─ Generate REQUIREMENTS.md                                 │
│                                                                 │
│  4. PLAN                                                        │
│     ├─ Decompose into tasks                                     │
│     ├─ Define dependencies                                      │
│     ├─ Add verification steps                                   │
│     └─ Create PLAN.md                                           │
│                                                                 │
│  5. EXECUTE                                                     │
│     ├─ Execute tasks one by one                                 │
│     ├─ Verify each task                                         │
│     ├─ Create atomic commits                                    │
│     └─ Track progress                                           │
│                                                                 │
│  6. VERIFY                                                      │
│     ├─ Run automated checks                                     │
│     ├─ Verify requirements                                      │
│     ├─ Conduct UAT                                              │
│     └─ Collect sign-off                                         │
│                                                                 │
│  7. COMPLETE                                                    │
│     ├─ Mark item COMPLETE in BACKLOG.md                         │
│     ├─ Clear active item (or suggest next)                      │
│     └─ Report summary                                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Phase Orchestration

### Starting the Cycle

```markdown
**Starting Full Workflow Cycle**

**Goal**: [task description from args]

**Phases to execute**:
1. DISCUSS - Gather requirements and make decisions
2. PLAN - Create atomic task plan
3. EXECUTE - Implement tasks
4. VERIFY - Validate implementation

**Estimated interactions**: [rough estimate]

Beginning with initialization...
```

### Phase Transitions

At each phase transition:

1. **Verify completion** of current phase
2. **Create checkpoint** in STATE.md
3. **Notify user** of transition
4. **Initialize next phase**

```markdown
**Phase Transition**

Completed: [PHASE]
Next: [NEXT_PHASE]

[Summary of what was accomplished]

Continuing to [NEXT_PHASE]...
```

### Handling Blockers

If a phase gets blocked:

1. Record blocker in STATE.md
2. Present options to user:
   - Resolve blocker and continue
   - Skip and continue (if possible)
   - Abort workflow

```markdown
**Workflow Blocked**

Phase: [current phase]
Blocker: [description]

**Options**:
1. Address the blocker
2. Skip this part and continue
3. Abort workflow
```

## Integration with Capability Routing

During EXECUTE phase, route tasks to appropriate agents:

```markdown
Task requires: [capability]
Available: [matched plugin:agent]
Routing: [agent being spawned]
```

If no capability match:
- Use internal executor agent
- Log warning for user awareness

## State Management

Throughout the cycle, maintain:

### STATE.md Updates
- Phase transitions
- Progress percentage
- Decisions made
- Checkpoints

### File Creation
| Phase | Creates |
|-------|---------|
| INIT | STATE.md, PROJECT.md |
| DISCUSS | EXPLORATION.md, REQUIREMENTS.md |
| PLAN | PLAN.md, ROADMAP.md |
| EXECUTE | (updates existing files) |
| VERIFY | Verification report in STATE.md |

## Completion

### Successful Completion

```markdown
**Workflow Complete**

**Summary**:
- Duration: [time]
- Decisions made: [N]
- Tasks executed: [N]
- Commits created: [N]

**Phases completed**:
- [x] INIT
- [x] DISCUSS - [N] decisions, [N] requirements
- [x] PLAN - [N] tasks defined
- [x] EXECUTE - [N] tasks completed
- [x] VERIFY - Approved

**Artifacts created**:
- .flow/STATE.md
- .flow/PROJECT.md
- .flow/REQUIREMENTS.md
- .flow/PLAN.md
- .flow/ROADMAP.md
- .flow/EXPLORATION.md

**Implementation**:
[Summary of what was implemented]
```

### Incomplete Workflow

If workflow doesn't complete:

```markdown
**Workflow Incomplete**

**Stopped at**: [phase]
**Reason**: [why stopped]

**State preserved in**: .flow/

**To resume**: `/flow-workflow:resume`
**To check status**: `/flow-workflow:status`
```

## Quick Mode Detection

If the task seems small:

```markdown
**Small Task Detected**

This task might be suitable for quick mode:
- Simple, well-defined task
- Single feature/fix
- No complex requirements gathering needed

Would you like to:
1. Continue with full workflow (thorough)
2. Use quick mode: `/flow-workflow:quick [task]` (faster)
```

## Output Format

### Progress Updates

```markdown
**Workflow Progress**

```
INIT → DISCUSS → PLAN → EXECUTE → VERIFY
  ✓       ✓       ●       ○         ○
```

**Current phase**: PLAN
**Overall progress**: 40%

[Phase-specific details]
```

### Phase Completion

```markdown
**[PHASE] Complete**

[Summary of phase]

**Next**: [NEXT_PHASE]

Continuing...
```

## Error Recovery

If errors occur:
1. Save state immediately
2. Create checkpoint
3. Present recovery options

```markdown
**Error Occurred**

Phase: [phase]
Error: [description]

**State saved**: Checkpoint created at [timestamp]

**Recovery options**:
1. Retry from checkpoint
2. Skip problematic step
3. Return to previous phase
4. Abort and preserve state
```

## Skills Used

- **workflow-orchestration**: Phase coordination
- **state-management**: State tracking
- **capability-discovery**: Agent routing
- **conflict-detection**: Blocker handling

## Agents Spawned

Depends on phase:
- DISCUSS: interviewer
- PLAN: planner
- EXECUTE: executor or capability-matched agents
- VERIFY: verifier
