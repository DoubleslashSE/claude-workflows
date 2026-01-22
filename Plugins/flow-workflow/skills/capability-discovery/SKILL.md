---
name: capability-discovery
description: Dynamic plugin enumeration and capability mapping for technology-agnostic workflow routing
triggers:
  - plugin discovery
  - capability mapping
  - agent routing
  - plugin enumeration
---

# Capability Discovery Skill

This skill enables dynamic discovery and mapping of installed plugins to abstract capability categories, allowing the workflow to route tasks to appropriate agents without hardcoding plugin names.

## Core Principles

1. **Technology Agnostic**: Map capabilities, not specific plugins
2. **Dynamic Discovery**: Scan at runtime, not compile time
3. **Graceful Fallback**: Work with internal agents when no match found
4. **Project-Aware Routing**: Prefer plugins matching detected project type

## Capability Categories

| Capability | Purpose | Used In Phase | Keywords |
|------------|---------|---------------|----------|
| `requirements-gathering` | Structured requirements elicitation | DISCUSS | requirements, interview, elicitation, stakeholder |
| `codebase-analysis` | Understanding existing code | DISCUSS, PLAN | codebase, analyze, reverse-engineer, patterns |
| `brainstorming` | Ideation and option exploration | DISCUSS | brainstorm, ideation, workshop, creative |
| `tdd-implementation` | Test-driven development | EXECUTE | tdd, test-driven, red-green |
| `code-implementation` | General code writing | EXECUTE | implement, developer, code, write |
| `infrastructure` | DevOps/infra tasks | EXECUTE | infra, devops, pipeline, deploy |
| `code-review` | Quality validation | VERIFY | review, quality, clean code |
| `requirements-validation` | Requirements compliance | VERIFY | validate, verification, compliance |

## Discovery Process

### Step 1: Enumerate Installed Plugins

```markdown
1. Locate Plugins/ directory
2. List all subdirectories (each is a plugin)
3. For each plugin:
   a. Read .claude-plugin/plugin.json for metadata
   b. Scan agents/*.md for agent definitions
   c. Scan commands/*.md for command definitions
4. Build plugin registry
```

### Step 2: Extract Descriptions

For each agent/command file, extract the description from YAML frontmatter:

```yaml
---
name: implementer
description: TDD implementation specialist. Use to write minimal code that makes tests pass.
model: opus
tools: [Read, Write, Edit, Bash, Grep, Glob]
---
```

### Step 3: Map to Capabilities

Apply keyword matching to descriptions:

```markdown
For each plugin agent/command:
  1. Tokenize description into words
  2. Match against capability keywords
  3. Score based on keyword count and position
  4. Assign to highest-scoring capability
  5. Record in capability map
```

### Step 4: Detect Project Type

Scan project root for technology indicators:

| File Pattern | Project Type |
|--------------|--------------|
| `*.csproj`, `*.sln` | dotnet |
| `package.json`, `*.js`, `*.ts` | node |
| `*.py`, `requirements.txt`, `setup.py` | python |
| `go.mod`, `*.go` | go |
| `Cargo.toml`, `*.rs` | rust |
| `pom.xml`, `build.gradle` | java |

### Step 5: Cache Results

Store in STATE.md:

```markdown
## Available Capabilities

| Capability | Matched Plugin | Agent/Command |
|------------|----------------|---------------|
| tdd-implementation | dotnet-tdd | dotnet-tdd:implementer |
| code-review | dotnet-tdd | dotnet-tdd:reviewer |
| requirements-gathering | business-analyst | business-analyst:stakeholder-interviewer |

**Project Type**: dotnet
**Last Scanned**: 2024-01-15T10:30:00Z
```

## Routing Logic

### When Phase Needs Capability

```markdown
1. Look up capability in STATE.md cache
2. If multiple matches:
   a. Filter by project type preference
   b. Prefer exact keyword match over partial
   c. Prefer agent over command
3. If single match:
   a. Return agent/command reference
4. If no match:
   a. Log warning in STATE.md
   b. Return internal fallback agent
```

### Project Type Preferences

```markdown
Project Type | Prefer Descriptions Containing
-------------|--------------------------------
dotnet       | ".NET", "dotnet", "C#", "csharp"
node         | "node", "javascript", "typescript", "npm"
python       | "python", "pip", "pytest"
go           | "go", "golang"
rust         | "rust", "cargo"
java         | "java", "maven", "gradle"
```

## Capability Usage by Phase

### DISCUSS Phase
```markdown
Capabilities Needed:
- requirements-gathering: For structured interviews
- brainstorming: For exploring options
- codebase-analysis: For understanding existing code

Routing Example:
"Need to gather requirements"
→ Look up 'requirements-gathering'
→ Found: business-analyst:stakeholder-interviewer
→ Spawn that agent
```

### PLAN Phase
```markdown
Capabilities Needed:
- codebase-analysis: For understanding what exists
- (internal planner for task creation)

Routing Example:
"Need to analyze existing patterns"
→ Look up 'codebase-analysis'
→ Found: business-analyst:codebase-analyzer
→ Spawn that agent
```

### EXECUTE Phase
```markdown
Capabilities Needed:
- tdd-implementation: If tests first approach
- code-implementation: For general coding
- infrastructure: For devops tasks

Routing Example:
"Need to implement with TDD" + project_type=dotnet
→ Look up 'tdd-implementation'
→ Multiple matches, filter by 'dotnet'
→ Found: dotnet-tdd:implementer
→ Spawn that agent
```

### VERIFY Phase
```markdown
Capabilities Needed:
- code-review: For quality checks
- requirements-validation: For compliance

Routing Example:
"Need code review"
→ Look up 'code-review'
→ Found: dotnet-tdd:reviewer
→ Spawn that agent
```

## Fallback Agents

When no plugin matches a capability, use internal agents:

| Capability | Fallback Agent |
|------------|----------------|
| requirements-gathering | flow-workflow:interviewer |
| codebase-analysis | flow-workflow:researcher |
| code-implementation | flow-workflow:executor |
| code-review | flow-workflow:verifier |

## Re-Discovery Triggers

Re-scan plugins when:
1. `/flow-workflow:init` is run
2. STATE.md capability cache is older than 24 hours
3. Requested capability returns no match
4. User explicitly requests refresh

## Integration Points

- **State Management**: Cache capability map in STATE.md
- **Workflow Orchestration**: Use capability routing for agent selection
- **Orchestrator Agent**: Performs discovery on initialization

See `categories.md` for detailed capability category definitions.
