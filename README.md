# Claude Code Workflows

A collection of **platform-agnostic** autonomous workflows for [Claude Code](https://claude.com/claude-code) that enable extended, high-quality code production with minimal human intervention.

## Architecture Overview

This repository is organized to support **separation of concerns** between orchestration logic and platform-specific details:

```
Workflows/
├── orchestration/                  # Platform-agnostic workflow definitions
│   └── multi-agent-workflow/       # Multi-agent autonomous workflow
│       └── .claude/
│           ├── agents/             # Subagent definitions (generic)
│           ├── skills/             # Workflow knowledge
│           ├── commands/           # Slash commands
│           └── hooks/              # Safety & audit hooks
│
├── platforms/                      # Platform-specific configurations
│   ├── dotnet/
│   │   ├── platform.json           # Build commands, conventions
│   │   └── skills/                 # .NET-specific knowledge
│   ├── typescript/
│   │   ├── platform.json           # TypeScript/Next.js commands
│   │   └── skills/                 # TypeScript patterns
│   └── python/
│       └── platform.json           # Python commands
│
└── dotnet/                         # (Legacy) Combined workflow + platform
    └── multi-agent-autonomous-workflow/
```

## Key Concepts

### Separation of Concerns

| Component | Responsibility | Location |
|-----------|---------------|----------|
| **Orchestration** | Agent coordination, quality gates, iteration loops | `orchestration/` |
| **Platform** | Build/test commands, naming conventions, patterns | `platforms/` |
| **Agent** | Infrastructure, task management, PR creation | Agent repo |

### Platform Configuration

Each platform defines a `platform.json` that provides:

```json
{
  "name": "dotnet",
  "commands": {
    "build": "dotnet build",
    "test": "dotnet test",
    "coverage": "dotnet test /p:CollectCoverage=true"
  },
  "conventions": {
    "testNaming": "{Method}_{Scenario}_{Expected}"
  },
  "qualityGates": {
    "coverageThresholds": { "S": 70, "M": 80, "L": 85, "XL": 90 }
  }
}
```

Agents reference these via the platform CLI:
```bash
python .claude/core/platform.py get-command build
python .claude/core/platform.py get-threshold M
```

## Available Workflows

### Multi-Agent Autonomous Workflow

**Location:** `orchestration/multi-agent-workflow/.claude/`

A hierarchical multi-agent system that coordinates specialized agents for extended autonomous work.

#### Agents

| Agent | Purpose | Tools |
|-------|---------|-------|
| `analyst` | Break goals into user stories | Read, Glob, Grep, WebSearch |
| `architect` | Technical design | Read, Glob, Grep, WebSearch |
| `developer` | TDD implementation | Read, Edit, Write, Bash |
| `tester` | Verify acceptance criteria | Bash, Read, Grep, Glob |
| `reviewer` | Code quality review | Read, Grep, Glob |
| `security` | Security audit | Read, Grep, Bash |
| `devops` | Infrastructure | Read, Edit, Write, Bash |

#### Workflow Phases

```
Phase 1: Analysis
├── analyst → User stories with acceptance criteria
└── architect → Technical design

Phase 2: Implementation Loop (per story)
├── developer → Implement with TDD
├── tester → Verify tests pass
├── reviewer → Code review
└── security → Security audit (if flagged)

Phase 3: Completion
└── devops → Infrastructure (if needed)
```

## Available Platforms

### .NET with Clean Architecture
- **Path:** `platforms/dotnet/`
- **Skills:** dotnet-clean-architecture, tdd-workflow
- **Pattern:** CQRS with MediatR, Entity Framework Core

### TypeScript with Next.js
- **Path:** `platforms/typescript/`
- **Skills:** typescript-patterns
- **Pattern:** App Router, React Query, Zustand

## Usage

### With Claude Code Agent (Docker)

Configure environment variables:
```env
WORKFLOW_REPO=your-org/claude-workflows
WORKFLOW_PATH=orchestration/multi-agent-workflow
PLATFORM=dotnet  # or typescript
```

The Agent will load the orchestration workflow and platform config automatically.

### Direct Installation

Copy the workflow to your project:
```bash
# Copy orchestration workflow
cp -r orchestration/multi-agent-workflow/.claude /path/to/project/

# Copy platform config
cp platforms/dotnet/platform.json /path/to/project/
cp -r platforms/dotnet/skills/* /path/to/project/.claude/skills/
```

### Slash Commands

```bash
/workflow [goal]      # Start full autonomous workflow
/implement [story]    # Implement single story
/review [files]       # Run code review
/status               # Check workflow progress
```

## Creating Custom Platforms

1. Create platform directory:
```
platforms/your-platform/
├── platform.json
└── skills/
    └── your-platform-patterns/
        ├── SKILL.md
        └── patterns.md
```

2. Define `platform.json`:
```json
{
  "name": "your-platform",
  "displayName": "Your Platform",
  "commands": {
    "build": "your-build-command",
    "test": "your-test-command"
  },
  "conventions": {
    "testNaming": "your-test-naming-pattern"
  }
}
```

3. Create platform-specific skills with domain knowledge.

## Anthropic Best Practices

This workflow implements best practices from Anthropic's engineering blog:

- **State Persistence**: Track workflow state for session recovery
- **Checkpoints**: Human review at 5-story intervals
- **Fail-First Verification**: Stories must pass all checks before completion
- **Iteration Loops**: Retry up to 3 times before escalating
- **Context Management**: Progressive disclosure, drop completed details

## Resources

- [Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [Building Agents with the Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)
- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)

## License

MIT
