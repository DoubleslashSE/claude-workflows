# Claude Code Workflows

A collection of autonomous workflows for [Claude Code](https://claude.com/claude-code) that enable extended, high-quality code production with minimal human intervention.

## Overview

These workflows leverage Claude Code's extension system—**subagents**, **skills**, **slash commands**, and **hooks**—to orchestrate complex software development tasks. Each workflow follows [Anthropic's best practices](https://www.anthropic.com/engineering/claude-code-best-practices) for building agents.

## Available Workflows

### .NET Multi-Agent Autonomous Workflow

**Location:** `dotnet/multi-agent-autonomous-workflow/.claude/`

A hierarchical multi-agent system for .NET projects following Clean Architecture and CQRS patterns.

#### Quick Start

```bash
# Copy to your project
cp -r dotnet/multi-agent-autonomous-workflow/.claude /path/to/your/project/

# Activate with slash command
/workflow Add user authentication with JWT tokens

# Or natural language (skill auto-invokes)
Use the multi-agent workflow to implement a bidding feature
```

#### Components

| Type | Count | Purpose |
|------|-------|---------|
| Subagents | 7 | Task execution (analyst, architect, developer, tester, reviewer, security, devops) |
| Skills | 4 | Knowledge patterns (clean-architecture, tdd, security-review, workflow orchestration) |
| Commands | 4 | Explicit triggers (`/workflow`, `/implement`, `/review`, `/status`) |
| Hooks | 2 | Safety checks and audit logging |

#### Tech Stack

- .NET 10 with Clean Architecture
- CQRS with MediatR
- FluentValidation
- Entity Framework Core
- xUnit + Moq

---

## Architecture

Each workflow follows Claude Code's extension architecture:

```
.claude/
├── settings.json         # Hook configuration
├── agents/               # Subagents (task executors with separate context)
│   └── {name}.md
├── commands/             # Slash commands (explicit /command invocation)
│   └── {name}.md
├── skills/               # Skills (knowledge, auto-invoked by model)
│   └── {name}/
│       ├── SKILL.md
│       └── {supporting-files}.md
└── hooks/                # Hooks (event-based automation)
    └── {name}.py
```

### Component Types

| Component | Invocation | Context | Use Case |
|-----------|------------|---------|----------|
| **Subagents** | Automatic/delegated | Separate | Delegate specialized tasks |
| **Skills** | Automatic (model) | Shared | Teach patterns and knowledge |
| **Commands** | Explicit (`/cmd`) | Shared | Frequently used prompts |
| **Hooks** | Event-based | N/A | Enforce rules, automation |

### File Formats

**Subagent** (`.claude/agents/{name}.md`):
```yaml
---
name: developer
description: When to invoke this subagent
tools: Read, Edit, Write, Bash
model: sonnet
skills: skill1, skill2
---

System prompt content here...
```

**Skill** (`.claude/skills/{name}/SKILL.md`):
```yaml
---
name: skill-name
description: What this skill teaches and when to use it
---

# Skill content with patterns and guidance...
```

**Command** (`.claude/commands/{name}.md`):
```yaml
---
description: What this command does
argument-hint: [args]
allowed-tools: Tool1, Tool2
---

Prompt template with $ARGUMENTS placeholder...
```

---

## Workflow Execution

### Agent Hierarchy

```
ORCHESTRATOR (Main Claude)
    │
    ├── analyst     → User stories & acceptance criteria
    ├── architect   → Technical design
    ├── developer   → TDD implementation
    ├── tester      → Verification
    ├── reviewer    → Code review
    ├── security    → Security audit (if flagged)
    └── devops      → Infrastructure (if needed)
```

### Quality Gates

| Gate | When | Checks |
|------|------|--------|
| G1 | Pre-Implementation | Design complete, AC clear |
| G2 | Post-Implementation | `dotnet build` + `dotnet test` pass |
| G3 | Coverage | Meets threshold (70-90%) |
| G4 | Security | OWASP Top 10 compliance |

### Escalation Triggers

- 5 stories completed → checkpoint review
- 3+ failed attempts → escalate blocker
- Security issue → immediate escalation

---

## Safety Features

Configured in `settings.json`:

- **PreToolUse Hook**: Blocks dangerous operations (`rm -rf`, `DROP TABLE`, force push)
- **PostToolUse Hook**: Audit logs all tool usage
- **Protected Files**: `.env`, credentials, secrets cannot be modified
- **Confirmation Required**: `git push`, migrations, deployments

---

## Installation

1. Copy the workflow's `.claude/` directory to your project root
2. Ensure Python 3 is available for hooks
3. Use slash commands or natural language to activate

```bash
# Example
cp -r dotnet/multi-agent-autonomous-workflow/.claude ./

# Then in Claude Code:
/workflow Implement feature X
```

---

## Creating New Workflows

### Directory Structure

```
{platform}/
└── {workflow-name}/
    └── .claude/
        ├── settings.json
        ├── agents/
        ├── commands/
        ├── skills/
        └── hooks/
```

### Checklist

- [ ] Subagents with proper YAML frontmatter (`name`, `description`, `tools`)
- [ ] Skills with SKILL.md and supporting files (progressive disclosure)
- [ ] Slash commands for common operations
- [ ] Safety hooks in settings.json
- [ ] Quality gates appropriate to tech stack

---

## Resources

- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Building Agents with Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)
- [Agent Skills Documentation](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [Claude Code Docs](https://code.claude.com/docs)

---

## License

MIT

---

*Built for autonomous software development with Claude Code*
