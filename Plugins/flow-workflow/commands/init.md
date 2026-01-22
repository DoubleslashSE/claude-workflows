---
name: init
description: Initialize project with .flow/ backlog structure and scan for available plugin capabilities
user_invocable: true
---

# Initialize Flow Workflow

You are initializing the flow-workflow system for this project. This creates the backlog structure, state files, and discovers available capabilities.

## What to Do

1. **Create .flow/ directory structure** with backlog support
2. **Scan installed plugins** to discover capabilities
3. **Detect project type** from file patterns
4. **Create BACKLOG.md** for work item tracking
5. **Create ACTIVE.md** for current item pointer
6. **Create PROJECT.md** stub for user to fill in
7. **Cache capabilities** in capabilities.md
8. **Report initialization results**

## Initialization Steps

### Step 1: Create Directory Structure

Create the `.flow/` directory structure:

```bash
mkdir -p .flow/items
```

This creates:
```
.flow/
├── items/          # Work item directories will go here
├── BACKLOG.md      # Master work item list
├── ACTIVE.md       # Current active item pointer
├── PROJECT.md      # Project context (shared)
└── capabilities.md # Cached plugin capabilities
```

### Step 2: Scan for Plugins

Scan the Plugins/ directory to find installed plugins:

1. List all directories in Plugins/
2. For each plugin directory:
   - Read `.claude-plugin/plugin.json` for metadata
   - Scan `agents/*.md` files for agent definitions
   - Scan `commands/*.md` files for command definitions
   - Extract descriptions from YAML frontmatter
3. Map descriptions to capability categories using keywords

### Capability Keywords

| Capability | Keywords |
|------------|----------|
| requirements-gathering | requirements, interview, elicitation, stakeholder |
| codebase-analysis | codebase, analyze, reverse-engineer, patterns |
| brainstorming | brainstorm, ideation, workshop, creative |
| tdd-implementation | tdd, test-driven, red-green |
| code-implementation | implement, developer, code, write |
| infrastructure | infra, devops, pipeline, deploy |
| code-review | review, quality, clean code |
| requirements-validation | validate, verification, compliance |

### Step 3: Detect Project Type

Check for project type indicators:

| File Pattern | Project Type |
|--------------|--------------|
| `*.csproj`, `*.sln` | dotnet |
| `package.json` | node |
| `*.py`, `requirements.txt` | python |
| `go.mod` | go |
| `Cargo.toml` | rust |
| `pom.xml`, `build.gradle` | java |

### Step 4: Create BACKLOG.md

Create `.flow/BACKLOG.md`:

```markdown
# Work Item Backlog

**Created**: [TIMESTAMP]
**Last Updated**: [TIMESTAMP]
**Total Items**: 0

## Backlog Summary

| Status | Count |
|--------|-------|
| BACKLOG | 0 |
| DISCUSS | 0 |
| PLAN | 0 |
| EXECUTE | 0 |
| VERIFY | 0 |
| ON_HOLD | 0 |
| BLOCKED | 0 |
| COMPLETE | 0 |

## Active Item

**Current**: None

## Work Items

[No work items yet. Use `/flow-workflow:new [title]` to create one.]

## Completed Items

[None yet]
```

### Step 5: Create ACTIVE.md

Create `.flow/ACTIVE.md`:

```markdown
# Active Work Item

**Current Item**: None
**Switched At**: [TIMESTAMP]

## Quick Context

No active work item. Create one with:
- `/flow-workflow:new [title]` - Create a new work item
- `/flow-workflow:flow [task]` - Start full workflow (creates item automatically)

## Recent Items

[No items yet]

## Switch History

[No switches yet]
```

### Step 6: Create PROJECT.md

Create `.flow/PROJECT.md` stub:

```markdown
# Project Overview

**Created**: [TIMESTAMP]
**Last Updated**: [TIMESTAMP]

## Vision

[Describe the high-level project vision]

## Scope

### In Scope
- [Feature/capability 1]

### Out of Scope
- [Explicitly excluded items]

## Stakeholders

| Role | Interest | Key Concerns |
|------|----------|--------------|
| [Role] | [What they care about] | [Main concerns] |

## Success Criteria

- [ ] [Criterion 1]

## Technical Context

**Stack**: [DETECTED_PROJECT_TYPE]
**Repository**: [Current directory]
**Key Files**:
- [To be identified]

## Constraints

### Technical Constraints
- [To be defined]

### Business Constraints
- [To be defined]
```

### Step 7: Create capabilities.md

Create `.flow/capabilities.md`:

```markdown
# Available Capabilities

**Project Type**: [DETECTED_TYPE]
**Last Scanned**: [TIMESTAMP]

## Capability Map

| Capability | Matched Plugin | Agent/Command |
|------------|----------------|---------------|
[DISCOVERED_CAPABILITIES]

## Fallback Agents

When no plugin matches a capability:

| Capability | Fallback |
|------------|----------|
| requirements-gathering | flow-workflow:interviewer |
| codebase-analysis | flow-workflow:researcher |
| code-implementation | flow-workflow:executor |
| code-review | flow-workflow:verifier |

## Plugin Scan Log

[List of plugins scanned and their matched capabilities]
```

## Output Format

After initialization:

```markdown
**Flow Workflow Initialized**

**Directory Structure**:
```
.flow/
├── items/          (work item directories)
├── BACKLOG.md      (work item tracking)
├── ACTIVE.md       (current item pointer)
├── PROJECT.md      (project context)
└── capabilities.md (plugin capabilities)
```

**Project Type**: [detected type]

**Capabilities Discovered**:
| Capability | Plugin | Agent/Command |
|------------|--------|---------------|
| [cap] | [plugin] | [agent] |
...

**Next Steps**:
1. Review and update `.flow/PROJECT.md` with your project details
2. Create a work item: `/flow-workflow:new [title]`
3. Or start full workflow: `/flow-workflow:flow [task description]`
4. View backlog: `/flow-workflow:backlog`
```

## If Already Initialized

If `.flow/` already exists:

```markdown
**Flow Workflow Already Initialized**

Found existing .flow/ directory with:
- BACKLOG.md: [N] items ([M] active)
- ACTIVE.md: [current item or "None"]
- PROJECT.md: [exists/missing]
- capabilities.md: [exists/missing]
- items/: [N] item directories

**Current Active Item**: [ITEM-XXX - Title] or "None"

**Options**:
1. View backlog: `/flow-workflow:backlog`
2. Check status: `/flow-workflow:status`
3. Resume work: `/flow-workflow:resume`
4. Re-initialize (will reset): `/flow-workflow:init --force`
```

## Re-initialization (--force)

If `--force` flag provided on existing directory:
1. Backup existing BACKLOG.md and items/
2. Create fresh structure
3. Preserve PROJECT.md if exists
4. Re-scan capabilities

```markdown
**Warning**: Re-initializing will reset your backlog.

Existing items will be backed up to .flow/backup-[timestamp]/

Proceed? [Requires explicit confirmation]
```

## Skills Used

- **capability-discovery**: For plugin enumeration and mapping
- **state-management**: For creating state files and backlog structure
