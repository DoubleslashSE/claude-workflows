# Flow Workflow Plugin

A technology-agnostic workflow management plugin for Claude Code, providing structured phases (Discuss → Plan → Execute → Verify), explicit state management through markdown files, atomic task execution with fresh context, and built-in verification patterns.

## Overview

Flow Workflow helps you manage complex development tasks by breaking them into structured phases with explicit state tracking. It supports a **backlog of work items** (epics/stories) at different states, allowing you to plan multiple features upfront and implement them one at a time.

Inspired by "Get Shit Done" (GSD) methodologies, it brings discipline to AI-assisted development.

## Core Philosophy

| Principle | Implementation |
|-----------|----------------|
| **Backlog-driven** | Multiple work items tracked at different states |
| **Context is managed** | Fresh context per task, orchestrator stays under 40% |
| **State is explicit** | Markdown files track everything |
| **Tasks are atomic** | One task = one commit = one thing |
| **Verification is built-in** | Every task has verify steps + UAT phase |
| **Technology agnostic** | Works with any stack, integrates with tech-specific plugins |

## Quick Start

### Initialize a Project

```
/flow-workflow:init
```

Creates `.flow/` directory with backlog structure.

### Create Work Items (Backlog)

```
/flow-workflow:new Add user authentication
/flow-workflow:new Fix cart calculation bug --priority P0
/flow-workflow:new Implement dark mode --priority P2
```

Creates work items in the backlog for later execution.

### Run Full Workflow

```
/flow-workflow:flow Add user authentication
```

Creates a work item and runs complete cycle: DISCUSS → PLAN → EXECUTE → VERIFY

### Work with Backlog

```
/flow-workflow:backlog              # View all work items
/flow-workflow:switch ITEM-002      # Switch to different item
/flow-workflow:status               # See current status
```

### Quick Mode for Small Tasks

```
/flow-workflow:quick Fix the login button alignment
```

Lightweight path for simple, well-defined tasks.

## Commands

### Backlog Management

| Command | Description |
|---------|-------------|
| `/flow-workflow:backlog` | List all work items and their status |
| `/flow-workflow:new` | Create a new work item in the backlog |
| `/flow-workflow:switch` | Switch to a different work item |
| `/flow-workflow:status` | Display current state and backlog overview |

### Workflow Execution

| Command | Description |
|---------|-------------|
| `/flow-workflow:init` | Initialize project with .flow/ backlog structure |
| `/flow-workflow:discuss` | Explore requirements for active item |
| `/flow-workflow:plan` | Create atomic task plan for active item |
| `/flow-workflow:execute` | Execute tasks with fresh context |
| `/flow-workflow:verify` | Run verification and UAT |
| `/flow-workflow:flow` | Full workflow cycle (creates work item) |
| `/flow-workflow:quick` | Lightweight path for small tasks |
| `/flow-workflow:resume` | Resume from checkpoint |

## Workflow Phases

### DISCUSS Phase

Explores requirements through adaptive questioning:
- Maintains exploration map of discussed areas
- Tracks explored vs. uncharted territory
- Detects and resolves conflicts
- Records decisions in STATE.md

### PLAN Phase

Creates atomic task plan:
- Decomposes work into single-commit tasks
- Defines verification steps for each task
- Maps dependencies between tasks
- Cross-verifies against requirements

### EXECUTE Phase

Implements tasks with fresh context:
- Routes to appropriate agents based on capabilities
- Executes one task at a time
- Creates atomic commits on success
- Tracks progress in state files

### VERIFY Phase

Validates implementation:
- Runs automated checks (build, test, lint)
- Verifies requirements traceability
- Guides user acceptance testing
- Collects sign-off

## State Files

All state is stored in the `.flow/` directory:

| File | Purpose |
|------|---------|
| `STATE.md` | Current phase, decisions, blockers, checkpoints |
| `PROJECT.md` | Vision, scope, stakeholders |
| `EXPLORATION.md` | Discussion progress and territory map |
| `REQUIREMENTS.md` | Functional/non-functional requirements |
| `PLAN.md` | XML-structured atomic tasks |
| `ROADMAP.md` | Milestones and progress |

## Capability Discovery

The plugin dynamically discovers and uses other installed plugins:

- Scans installed plugins at initialization
- Maps plugin capabilities to abstract categories
- Routes tasks to appropriate specialized agents
- Falls back to internal agents when no match found

### Capability Categories

| Capability | Used For |
|------------|----------|
| requirements-gathering | Structured interviews |
| codebase-analysis | Understanding existing code |
| brainstorming | Exploring options |
| tdd-implementation | Test-driven development |
| code-implementation | General coding |
| infrastructure | DevOps tasks |
| code-review | Quality validation |
| requirements-validation | Compliance checking |

## Agents

| Agent | Role |
|-------|------|
| `orchestrator` | Coordinates phases, spawns agents, maintains state |
| `interviewer` | Adaptive questioning, exploration mapping |
| `researcher` | Codebase investigation |
| `planner` | Atomic task planning |
| `executor` | Task implementation |
| `verifier` | Validation and UAT |

## Skills

| Skill | Purpose |
|-------|---------|
| `state-management` | State file operations and templates |
| `atomic-tasks` | Task structure and XML format |
| `capability-discovery` | Plugin enumeration and mapping |
| `exploration-tracking` | Discussion territory tracking |
| `conflict-detection` | Conflict identification and resolution |
| `context-engineering` | Context window management |
| `workflow-orchestration` | Phase coordination |

## Atomic Task Format

Tasks are defined in XML for clarity and parsing:

```xml
<task id="TASK-001" status="pending">
  <name>Implement user authentication service</name>
  <description>Create core auth service with login/logout</description>
  <files>
    <file action="create">src/services/AuthService.ts</file>
    <file action="modify">src/config/services.ts</file>
  </files>
  <actions>
    <action>Create AuthService class with login/logout methods</action>
    <action>Add dependency injection configuration</action>
  </actions>
  <verify>
    <step>npm test -- AuthService</step>
    <step>npm run build</step>
  </verify>
  <done>
    <criterion>AuthService exists and is properly injected</criterion>
    <criterion>Tests cover login success and failure</criterion>
  </done>
  <commit>feat(auth): add AuthService with login/logout</commit>
</task>
```

## Exploration Map

During DISCUSS, progress is tracked visually:

```
[MAIN TOPIC]
├── ✓ EXPLORED: Authentication
│   ├── ✓ Login flow - Using OAuth, DECISION-003
│   └── ◐ PARTIAL: Session management - JWT chosen, expiry TBD
├── → CURRENT: Data storage
│   └── ○ UNCHARTED: Caching strategy
├── ○ UNCHARTED: API design
└── ⊘ SKIPPED: Mobile support - Phase 2, per user
```

### Status Indicators

- ✓ EXPLORED: Fully discussed, decisions made
- ◐ PARTIAL: Started but incomplete
- → CURRENT: Currently exploring
- ○ UNCHARTED: Identified but not yet explored
- ⊘ SKIPPED: User chose to skip (with reason)
- ⚑ FLAGGED: Needs follow-up or has blockers

## Conflict Detection

The plugin automatically detects conflicts:
- Contradictory requirements
- Conflicting decisions
- Technical incompatibilities
- Scope vs. timeline issues

Conflicts must be resolved before proceeding.

## Resume Capability

If workflow is interrupted:

```
/flow-workflow:resume
```

Reconstructs context from STATE.md and continues from last checkpoint.

## Integration with Other Plugins

Flow Workflow works with technology-specific plugins:

- **dotnet-tdd**: Routes TDD implementation tasks
- **business-analyst**: Uses for requirements gathering
- **workshop-facilitator**: Leverages for brainstorming

If no matching plugin is found, internal fallback agents are used.

## Best Practices

1. **Start with init**: Always initialize before starting work
2. **Don't skip DISCUSS**: Even quick tasks benefit from clarity
3. **Review the plan**: Approve tasks before execution starts
4. **Commit atomically**: Each task should be one commit
5. **Verify everything**: Don't skip the VERIFY phase
6. **Use state files**: They're your external memory

## Example Workflow

```
> /flow-workflow:init
Initialized .flow/ with STATE.md and PROJECT.md
Discovered 3 capability-matched plugins

> /flow-workflow:flow Add user registration feature

[DISCUSS Phase]
Exploring: User registration requirements
- What authentication method? → OAuth + email/password
- What user data to collect? → Email, name, password
- Email verification required? → Yes
...

[PLAN Phase]
Creating atomic tasks:
- TASK-001: Create User model
- TASK-002: Add registration endpoint
- TASK-003: Implement email verification
- TASK-004: Add registration form
...

[EXECUTE Phase]
Executing TASK-001... completed
Executing TASK-002... completed
Executing TASK-003... completed
Executing TASK-004... completed

[VERIFY Phase]
Running automated checks... PASSED
Verifying requirements... 4/4 met
UAT: Please test registration flow... PASSED

Workflow complete!
```

## License

MIT
