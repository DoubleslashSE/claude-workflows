# Node.js TDD Plugin

Test-Driven Development plugin for Node.js/TypeScript projects with SOLID principles, clean code practices, and functional patterns.

## Features

- **TDD Workflow**: RED-GREEN-REFACTOR cycle with integrated feedback loops
- **SOLID Principles**: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion
- **Clean Code**: DRY, KISS, YAGNI principles with TypeScript best practices
- **Functional Patterns**: Pure functions, immutability, composition, Result pattern
- **Specialized Agents**: Dedicated agents for each TDD phase
- **Code Review**: Automated quality assessment against defined standards

## Installation

```bash
claude --plugin-dir ./Plugins/node-tdd
```

## Commands

| Command | Description |
|---------|-------------|
| `/tdd <feature>` | Execute complete RED-GREEN-REFACTOR cycle |
| `/red <behavior>` | Design failing tests (RED phase) |
| `/green [file]` | Implement minimal code (GREEN phase) |
| `/refactor [file]` | Improve code design (REFACTOR phase) |
| `/review [file]` | Review code for principle compliance |

## Skills

| Skill | Purpose |
|-------|---------|
| `tdd-workflow` | TDD methodology, AAA pattern, test doubles |
| `solid-principles` | SOLID principles for TypeScript |
| `clean-code` | DRY, KISS, YAGNI, naming, functions |
| `functional-patterns` | Pure functions, immutability, Result pattern |

## Agents

| Agent | TDD Phase | Purpose |
|-------|-----------|---------|
| `test-designer` | RED | Design comprehensive failing tests |
| `implementer` | GREEN | Write minimal code to pass tests |
| `refactorer` | REFACTOR | Improve design while keeping tests green |
| `reviewer` | Review | Assess code against quality standards |

## Core Principles

### TDD - Test-Driven Development

1. **RED**: Write a failing test
2. **GREEN**: Write minimal code to pass
3. **REFACTOR**: Improve design, tests stay green

### SOLID Principles

- **S**ingle Responsibility: One reason to change
- **O**pen/Closed: Open for extension, closed for modification
- **L**iskov Substitution: Subtypes substitutable for base types
- **I**nterface Segregation: Small, focused interfaces
- **D**ependency Inversion: Depend on abstractions

### Clean Code

- **DRY**: Don't Repeat Yourself
- **KISS**: Keep It Simple
- **YAGNI**: You Aren't Gonna Need It

### Functional Patterns

- Pure functions (no side effects)
- Immutable data structures
- Function composition
- Result pattern for error handling
- Dependency injection via parameters

## Quality Gates

| Metric | Target |
|--------|--------|
| SOLID Compliance | 90% |
| Clean Code (DRY/KISS/YAGNI) | 90% |
| Test Coverage | 90% |
| TypeScript Strictness | 100% |

## Test Naming Convention

Format: `should {expectedBehavior} when {scenario}`

```typescript
it('should return empty array when input is empty', ...);
it('should throw ValidationError when email is invalid', ...);
it('should emit event when state changes', ...);
```

## Usage Example

### 1. Start with RED - Design Tests

```bash
/red User registration should validate email and password
```

Creates:
```typescript
describe('UserRegistration', () => {
  it('should return success for valid email and password', () => {...});
  it('should return failure when email is invalid', () => {...});
  it('should return failure when password is too short', () => {...});
});
```

### 2. Move to GREEN - Implement

```bash
/green src/services/user-registration.test.ts
```

Implements minimal code to pass all tests.

### 3. Finish with REFACTOR - Improve

```bash
/refactor src/services/user-registration.ts
```

Reviews and improves code:
- Extracts pure validation functions
- Applies Result pattern
- Ensures dependency injection

## Directory Structure

```
Plugins/node-tdd/
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
│   └── functional-patterns/
│       └── SKILL.md
└── README.md
```

## Key TypeScript Patterns

### Factory Functions

```typescript
const createUserService = (deps: Dependencies) => ({
  findUser: (id: string) => deps.db.users.findFirst({ where: { id } }),
  createUser: async (data: CreateUserData) => {
    const validated = validateUser(data);
    if (validated.isFailure) return validated;
    return Result.ok(await deps.db.users.create({ data }));
  },
});
```

### Result Pattern

```typescript
type Result<T, E> =
  | { isSuccess: true; value: T }
  | { isSuccess: false; error: E };

const validateEmail = (email: string): Result<string, ValidationError> => {
  if (!email.includes('@')) {
    return Result.fail({ code: 'INVALID_EMAIL', field: 'email' });
  }
  return Result.ok(email);
};
```

### Dependency Injection

```typescript
type Dependencies = {
  db: Database;
  logger: Logger;
  clock: () => Date;
};

const createService = (deps: Dependencies) => ({
  // Pure business logic with injected I/O
});
```

## Test Frameworks

Supported:
- Jest
- Vitest
- Mocha + Chai

Commands:
```bash
# Jest
npm test
npm test -- --watch
npm test -- --coverage

# Vitest
npx vitest run
npx vitest watch
npx vitest --coverage
```

## License

MIT
