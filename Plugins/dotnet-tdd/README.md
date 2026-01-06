# .NET TDD Plugin for Claude Code

A comprehensive Test-Driven Development plugin for .NET projects that enforces TDD, SOLID, DRY, KISS, YAGNI, and CQS principles.

## Features

- **TDD Workflow**: Complete RED-GREEN-REFACTOR cycle support
- **Principle Enforcement**: SOLID, DRY, KISS, YAGNI, CQS compliance checking
- **Specialized Agents**: Purpose-built agents for each TDD phase
- **Code Review**: Automated principle compliance review

## Installation

```bash
claude --plugin-dir ./Plugins/dotnet-tdd
```

## Commands

| Command | Description |
|---------|-------------|
| `/dotnet-tdd:tdd {feature}` | Execute complete TDD cycle |
| `/dotnet-tdd:red {feature}` | RED phase - Write failing tests |
| `/dotnet-tdd:green {feature}` | GREEN phase - Make tests pass |
| `/dotnet-tdd:refactor {feature}` | REFACTOR phase - Improve design |
| `/dotnet-tdd:review {code}` | Review for principle compliance |

## Skills

### tdd-workflow
Complete TDD guidance including:
- RED-GREEN-REFACTOR cycle
- AAA pattern (Arrange-Act-Assert)
- Test naming conventions
- Test doubles (Stub, Mock, Fake, Spy)

### solid-principles
SOLID principle guidance:
- **S**ingle Responsibility Principle
- **O**pen/Closed Principle
- **L**iskov Substitution Principle
- **I**nterface Segregation Principle
- **D**ependency Inversion Principle

### clean-code
Clean code principles:
- **DRY** - Don't Repeat Yourself
- **KISS** - Keep It Simple, Stupid
- **YAGNI** - You Aren't Gonna Need It

### cqs-patterns
Command Query Separation:
- Method-level CQS
- CQRS architecture patterns
- Command and Query handlers

## Agents

| Agent | Role |
|-------|------|
| `test-designer` | Designs failing tests (RED phase) |
| `implementer` | Implements minimal code (GREEN phase) |
| `refactorer` | Improves design (REFACTOR phase) |
| `reviewer` | Reviews principle compliance |

## Principles

### TDD (Test-Driven Development)
1. **RED**: Write a failing test
2. **GREEN**: Write minimal code to pass
3. **REFACTOR**: Improve design, keep tests green

### SOLID
- Single classes with single responsibilities
- Open for extension, closed for modification
- Subtypes substitutable for base types
- Specific interfaces over general ones
- Depend on abstractions, not concretions

### DRY (Don't Repeat Yourself)
- Single source of truth for knowledge
- Extract common code
- Use constants for magic values

### KISS (Keep It Simple, Stupid)
- Simplest solution that works
- Avoid over-engineering
- Clear, readable code

### YAGNI (You Aren't Gonna Need It)
- Implement only what's needed now
- No speculative features
- Remove unused code

### CQS (Command Query Separation)
- **Commands**: Change state, return void
- **Queries**: Return data, no side effects

## Test Naming Convention

```
{MethodUnderTest}_{Scenario}_{ExpectedBehavior}
```

Examples:
- `CreateOrder_WithValidItems_ReturnsOrder`
- `GetUser_WhenNotFound_ThrowsNotFoundException`
- `CalculateDiscount_WithPremiumCustomer_Applies15Percent`

## Usage Example

```bash
# Start TDD for a new feature
/dotnet-tdd:tdd Create order processing service

# Or step by step:
/dotnet-tdd:red Create order with valid items
# Write tests...

/dotnet-tdd:green CreateOrder_WithValidItems_ReturnsOrder
# Implement minimal code...

/dotnet-tdd:refactor OrderService
# Improve design...

/dotnet-tdd:review src/Services/OrderService.cs
# Review for compliance...
```

## Directory Structure

```
dotnet-tdd/
├── .claude-plugin/
│   └── plugin.json
├── agents/
│   ├── test-designer.md
│   ├── implementer.md
│   ├── refactorer.md
│   └── reviewer.md
├── commands/
│   ├── tdd.md
│   ├── red.md
│   ├── green.md
│   ├── refactor.md
│   └── review.md
├── hooks/
│   └── hooks.json
├── skills/
│   ├── tdd-workflow/
│   │   ├── SKILL.md
│   │   └── patterns.md
│   ├── solid-principles/
│   │   ├── SKILL.md
│   │   └── examples.md
│   ├── clean-code/
│   │   ├── SKILL.md
│   │   └── reference.md
│   └── cqs-patterns/
│       └── SKILL.md
└── README.md
```

## License

MIT
