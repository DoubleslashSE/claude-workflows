# Capability Category Definitions

## Overview

Capability categories provide an abstraction layer between workflow phases and specific plugin implementations. This enables technology-agnostic orchestration.

## Category Definitions

### requirements-gathering

**Purpose**: Structured elicitation of project requirements from stakeholders

**When Used**: DISCUSS phase, when understanding what to build

**Keywords**: `requirements`, `interview`, `elicitation`, `stakeholder`, `gathering`, `discover`, `needs`

**Expected Behaviors**:
- Conduct structured interviews
- Ask clarifying questions
- Document functional requirements
- Document non-functional requirements
- Identify constraints and assumptions

**Example Plugins**:
- business-analyst (stakeholder-interviewer agent)

**Fallback**: flow-workflow:interviewer

---

### codebase-analysis

**Purpose**: Understanding existing code, patterns, and architecture

**When Used**: DISCUSS phase (for brownfield projects), PLAN phase (for implementation planning)

**Keywords**: `codebase`, `analyze`, `reverse-engineer`, `patterns`, `architecture`, `existing`, `legacy`

**Expected Behaviors**:
- Scan project structure
- Identify design patterns
- Detect technologies in use
- Find integration points
- Document existing behavior

**Example Plugins**:
- business-analyst (codebase-analyzer agent)

**Fallback**: flow-workflow:researcher

---

### brainstorming

**Purpose**: Creative exploration of ideas and options

**When Used**: DISCUSS phase, when exploring possible approaches

**Keywords**: `brainstorm`, `ideation`, `workshop`, `creative`, `explore`, `options`, `ideas`

**Expected Behaviors**:
- Facilitate idea generation
- Divergent thinking exercises
- Option comparison
- Trade-off analysis
- Convergent selection

**Example Plugins**:
- workshop-facilitator (brainstorm command)

**Fallback**: flow-workflow:interviewer (with brainstorming prompts)

---

### tdd-implementation

**Purpose**: Test-driven development with RED-GREEN-REFACTOR cycle

**When Used**: EXECUTE phase, when implementing with tests first

**Keywords**: `tdd`, `test-driven`, `red-green`, `refactor`, `tests first`, `failing test`

**Expected Behaviors**:
- Write failing tests first (RED)
- Implement minimal code to pass (GREEN)
- Refactor for quality (REFACTOR)
- Maintain test coverage
- Follow clean code principles

**Example Plugins**:
- dotnet-tdd (implementer, test-designer agents)
- node-tdd (implementer, test-designer agents)

**Fallback**: flow-workflow:executor (with TDD guidance)

---

### code-implementation

**Purpose**: General code writing and modification

**When Used**: EXECUTE phase, for any coding task

**Keywords**: `implement`, `developer`, `code`, `write`, `create`, `build`, `feature`

**Expected Behaviors**:
- Write production code
- Follow project conventions
- Handle errors appropriately
- Integrate with existing code
- Document as needed

**Example Plugins**:
- dotnet-developer (developer agent)
- Any plugin with "developer" or "implementer" agents

**Fallback**: flow-workflow:executor

---

### infrastructure

**Purpose**: DevOps, CI/CD, and infrastructure tasks

**When Used**: EXECUTE phase, for deployment and operations

**Keywords**: `infra`, `devops`, `pipeline`, `deploy`, `docker`, `kubernetes`, `ci`, `cd`, `terraform`

**Expected Behaviors**:
- Configure build pipelines
- Write deployment scripts
- Manage infrastructure as code
- Set up environments
- Configure monitoring

**Example Plugins**:
- devops-azure-infrastructure
- infra-plugin

**Fallback**: flow-workflow:executor (with infrastructure guidance)

---

### code-review

**Purpose**: Quality validation of implemented code

**When Used**: VERIFY phase, after implementation

**Keywords**: `review`, `quality`, `clean code`, `solid`, `dry`, `kiss`, `standards`

**Expected Behaviors**:
- Review code for quality
- Check adherence to standards
- Identify potential issues
- Suggest improvements
- Validate best practices

**Example Plugins**:
- dotnet-tdd (reviewer agent)
- node-tdd (reviewer agent)

**Fallback**: flow-workflow:verifier

---

### requirements-validation

**Purpose**: Verify implementation meets requirements

**When Used**: VERIFY phase, for acceptance testing

**Keywords**: `validate`, `verification`, `compliance`, `acceptance`, `requirements`, `uat`

**Expected Behaviors**:
- Check requirements coverage
- Validate acceptance criteria
- Identify gaps
- Conduct UAT
- Document compliance

**Example Plugins**:
- business-analyst (validator agent)

**Fallback**: flow-workflow:verifier

---

## Keyword Matching Algorithm

### Scoring Rules

```
1. Exact keyword match: +10 points
2. Partial match (word contains keyword): +3 points
3. Keyword in first sentence: +5 bonus
4. Multiple keywords from same category: +2 each after first
```

### Matching Examples

**Description**: "TDD implementation specialist for .NET. Write minimal code that makes tests pass."

```
Keyword matches:
- "TDD" → tdd-implementation (+10)
- "implementation" → code-implementation (+10)
- "tests" → tdd-implementation (+10)
- ".NET" → (project type indicator)

Scores:
- tdd-implementation: 20 + 5 (first sentence) = 25
- code-implementation: 10

Winner: tdd-implementation
```

---

## Project Type Routing

### When Multiple Capabilities Match

If multiple plugins match a capability, filter by project type:

```
Capability: tdd-implementation
Matches:
- dotnet-tdd:implementer (description contains ".NET")
- node-tdd:implementer (description contains "Node.js")

Detected project type: dotnet

Selected: dotnet-tdd:implementer
```

### Project Type Keywords

| Project Type | Description Keywords |
|--------------|---------------------|
| dotnet | `.NET`, `dotnet`, `C#`, `csharp`, `NuGet` |
| node | `Node.js`, `node`, `JavaScript`, `TypeScript`, `npm`, `yarn` |
| python | `Python`, `pip`, `pytest`, `Django`, `Flask` |
| go | `Go`, `golang`, `Gin`, `Echo` |
| rust | `Rust`, `Cargo`, `crate` |
| java | `Java`, `Maven`, `Gradle`, `Spring` |

---

## Capability Gaps

### Logging Unmatched Capabilities

When no plugin matches a capability:

```markdown
## Capability Warnings

**[TIMESTAMP]**: No plugin found for capability 'infrastructure'
- Searched: [list of plugins scanned]
- Keywords tried: [list of keywords]
- Using fallback: flow-workflow:executor
- Recommendation: Consider installing an infrastructure plugin
```

### Suggesting Plugins

Based on detected gaps, suggest relevant plugins:

| Missing Capability | Suggested Plugin Type |
|-------------------|----------------------|
| requirements-gathering | business-analyst |
| tdd-implementation | dotnet-tdd, node-tdd |
| brainstorming | workshop-facilitator |
| infrastructure | devops plugin |
