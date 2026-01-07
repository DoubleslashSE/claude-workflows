# Business Analyst Plugin for Claude Code

A comprehensive Senior Business Analyst plugin that helps gather requirements, analyze codebases, conduct stakeholder interviews, and generate formal SRS documents. Supports both greenfield (new projects) and brownfield (existing codebase) development contexts.

## Features

- **Requirements Gathering**: Structured and adaptive interview techniques
- **Codebase Analysis**: Reverse-engineer requirements from existing code
- **SRS Generation**: IEEE 830 compliant Software Requirements Specification
- **Validation Feedback Loop**: Built-in verification and quality checks
- **Dual Context Support**: Greenfield and brownfield workflows

## Installation

```bash
claude --plugin-dir ./Plugins/business-analyst
```

## Commands

| Command | Description |
|---------|-------------|
| `/business-analyst:analyze {context}` | Full analysis workflow (auto-detects greenfield/brownfield) |
| `/business-analyst:interview {topic}` | Interactive requirements gathering session |
| `/business-analyst:greenfield {project}` | New project requirements analysis |
| `/business-analyst:brownfield {path}` | Existing codebase analysis |
| `/business-analyst:generate-srs` | Generate IEEE 830 SRS document |
| `/business-analyst:validate {artifact}` | Validate work quality and completeness |

## Agents

| Agent | Role |
|-------|------|
| `requirements-analyst` | Core BA for requirements gathering and prioritization |
| `codebase-analyzer` | Reverse-engineers requirements from existing code |
| `stakeholder-interviewer` | Conducts structured and adaptive interviews |
| `srs-generator` | Generates IEEE 830 compliant SRS documents |
| `validator` | Validates work quality and ensures feedback loop |

## Skills

### requirements-elicitation
Requirements gathering techniques including:
- Structured question templates by category
- Adaptive questioning techniques
- Gap identification methods
- MoSCoW prioritization

### codebase-analysis
Code analysis patterns for:
- Domain models and entities
- Business rules and validation logic
- Workflows and state machines
- API contracts and data flows

### srs-documentation
SRS writing guidance including:
- IEEE 830 template structure
- Writing guidelines for clarity
- Validation checklists (SMART + INVEST criteria)
- Traceability matrix patterns

### technical-analysis
Technical analysis capabilities:
- API endpoint analysis
- Data model inference
- Integration pattern identification
- Security requirements extraction

## Workflows

### Greenfield Analysis Flow
```
1. Identify stakeholders
2. Define project scope and objectives
3. Gather functional requirements via interview
4. Gather non-functional requirements (FURPS+)
5. Document constraints and assumptions
6. Prioritize using MoSCoW
7. Validate with stakeholders
8. Generate SRS
```

### Brownfield Analysis Flow
```
1. Analyze codebase structure
2. Identify domain models and entities
3. Extract business rules from code
4. Map integrations and dependencies
5. Interview stakeholders for gaps/changes
6. Document as-is requirements
7. Identify technical debt
8. Validate findings
9. Generate SRS with recommendations
```

## Feedback Loop System

The plugin includes a comprehensive feedback loop that continuously improves output quality by feeding validation results back to the business analyst.

### Feedback Loop Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    FEEDBACK IMPROVEMENT CYCLE                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌────────────┐    ┌────────────┐    ┌────────────┐            │
│  │ Gather     │───▶│ Validate   │───▶│ Generate   │            │
│  │Requirements│    │            │    │ Feedback   │            │
│  └────────────┘    └────────────┘    └────────────┘            │
│        ▲                                    │                   │
│        │                                    ▼                   │
│        │           ┌────────────────────────────┐               │
│        │           │ Process Feedback:          │               │
│        │           │ - Rewrite vague reqs       │               │
│        │           │ - Add missing sections     │               │
│        │           │ - Ask targeted questions   │               │
│        │           │ - Resolve conflicts        │               │
│        │           └────────────────────────────┘               │
│        │                                    │                   │
│        └────────────────────────────────────┘                   │
│                    Iterate until PASS                           │
└─────────────────────────────────────────────────────────────────┘
```

### How Feedback Improves Output

The validator generates structured feedback that the business analyst processes:

1. **Specific Rewrites**: Vague requirements are rewritten with metrics
   - BEFORE: "System should be fast"
   - AFTER: "System shall respond within 3 seconds"

2. **Targeted Questions**: Questions generated from gaps
   - "What authentication method is preferred?" (for missing NFR-SEC)
   - "What is the expected concurrent user count?" (for NFR-PERF)

3. **Templates for Missing Items**: Pre-filled templates for gaps
4. **Conflict Resolution**: Options with recommendations

### Validation Checkpoints
- **Stakeholder List**: "Are these all the stakeholders?"
- **Scope Boundaries**: "Is this in/out of scope assessment correct?"
- **Key Assumptions**: "Do you agree with these assumptions?"
- **Business Rules**: "Did I capture these correctly?"
- **Priority Rankings**: "Does this MoSCoW prioritization look right?"
- **SRS Draft**: "What needs adjustment?"

### Quality Metrics
- Completeness Score (0-100%)
- Quality Score (0-100%)
- SMART criteria validation
- INVEST criteria for user stories
- Traceability verification

### Improvement Tracking

```markdown
| Cycle | Completeness | Quality | Issues | Status |
|-------|--------------|---------|--------|--------|
| 1     | 65%          | 70%     | 15     | FAIL   |
| 2     | 82%          | 85%     | 6      | COND   |
| 3     | 95%          | 92%     | 2      | PASS   |
```

### Validation Report
```markdown
## Validation Report

### Summary
- Artifact: SRS Document
- Completeness Score: 85%
- Quality Score: 90%
- Issues Found: 3

### Completeness Check
[checkmark] Introduction - Complete
[warning] Stakeholders - Missing 1 item
[checkmark] Functional Requirements - Complete

### Feedback for Improvement
| Issue | Current | Fix | Action |
|-------|---------|-----|--------|
| FB-001 | Vague | Add metric | Ask user |
```

## Interview Categories

The plugin covers these requirement categories:

- **Stakeholders**: Who uses, maintains, and pays for the system?
- **Scope**: What's in/out? What are the boundaries?
- **Functional**: What should the system do?
- **Non-functional**: Performance, security, scalability, usability (FURPS+)
- **Constraints**: Budget, timeline, technology, regulatory
- **Integrations**: External systems, APIs, data sources

## Usage Examples

### Start Full Analysis
```bash
# Auto-detect project type and run complete analysis
/business-analyst:analyze My E-commerce Platform
```

### Greenfield Project
```bash
# Start requirements gathering for a new project
/business-analyst:greenfield Customer Portal Application
```

### Brownfield Analysis
```bash
# Analyze existing codebase
/business-analyst:brownfield ./src
```

### Interactive Interview
```bash
# Start focused interview session
/business-analyst:interview functional requirements
```

### Generate SRS
```bash
# Compile requirements into formal SRS
/business-analyst:generate-srs
```

### Validate Work
```bash
# Run validation on generated artifact
/business-analyst:validate SRS
```

## Directory Structure

```
business-analyst/
├── .claude-plugin/
│   └── plugin.json
├── agents/
│   ├── requirements-analyst.md
│   ├── codebase-analyzer.md
│   ├── stakeholder-interviewer.md
│   ├── srs-generator.md
│   └── validator.md
├── commands/
│   ├── analyze.md
│   ├── interview.md
│   ├── greenfield.md
│   ├── brownfield.md
│   ├── generate-srs.md
│   └── validate.md
├── skills/
│   ├── requirements-elicitation/
│   │   ├── SKILL.md
│   │   └── question-templates.md
│   ├── codebase-analysis/
│   │   ├── SKILL.md
│   │   └── patterns.md
│   ├── srs-documentation/
│   │   ├── SKILL.md
│   │   ├── template.md
│   │   └── checklists.md
│   └── technical-analysis/
│       ├── SKILL.md
│       └── integration-patterns.md
├── hooks/
│   └── hooks.json
└── README.md
```

## Requirements Categories (FURPS+)

- **F**unctionality: Features, capabilities, security
- **U**sability: Human factors, aesthetics, documentation
- **R**eliability: Availability, failure rate, recoverability
- **P**erformance: Response time, throughput, resource usage
- **S**upportability: Maintainability, configurability, testability
- **+**: Constraints (design, implementation, interface, physical)

## License

MIT
