# /refactor - Improve Code Design (REFACTOR Phase)

## Description
Improve code design while maintaining all passing tests in the REFACTOR phase of TDD.

## Usage
```
/refactor [file-path]
```

## Arguments
- `file-path`: (Optional) Path to the file or directory to refactor

## Agents
Uses the `reviewer` agent first, then the `refactorer` agent.

## Skills
- `tdd-workflow`
- `solid-principles`
- `clean-code`
- `functional-patterns`

## Workflow

1. **Review Current State**
   - Run code review
   - Identify improvement areas
   - Score against quality gates

2. **Prioritize Refactorings**
   - Critical issues first
   - High-impact improvements
   - Quick wins

3. **Apply Incrementally**
   - One refactoring at a time
   - Run tests after each change
   - Verify GREEN maintained

4. **Verify Quality Gates**
   | Metric | Target |
   |--------|--------|
   | SOLID | 90% |
   | Clean Code | 90% |
   | Test Coverage | 90% |
   | TypeScript Strict | 100% |

## Common Refactorings

### Extract Function
```typescript
// Before
const processUser = (user: User) => {
  if (!user.email.includes('@')) throw new Error('Invalid');
  if (user.password.length < 8) throw new Error('Weak');
  // ... more logic
};

// After
const validateEmail = (email: string): Result<string, ValidationError> =>
  email.includes('@')
    ? Result.ok(email)
    : Result.fail({ code: 'INVALID_EMAIL' });

const validatePassword = (password: string): Result<string, ValidationError> =>
  password.length >= 8
    ? Result.ok(password)
    : Result.fail({ code: 'WEAK_PASSWORD' });
```

### Replace Class with Factory
```typescript
// Before
class UserService {
  constructor(private db: Database) {}
  async findUser(id: string) { ... }
}

// After
const createUserService = (db: Database) => ({
  findUser: async (id: string) => { ... },
});
```

### Introduce Result Pattern
```typescript
// Before
const parseConfig = (input: string): Config => {
  return JSON.parse(input); // throws
};

// After
const parseConfig = (input: string): Result<Config, ParseError> => {
  try {
    return Result.ok(JSON.parse(input));
  } catch (error) {
    return Result.fail(createParseError(error));
  }
};
```

### Compose Functions
```typescript
// Before
const processInput = (input: string) => {
  const trimmed = input.trim();
  const lower = trimmed.toLowerCase();
  const validated = validate(lower);
  return transform(validated);
};

// After
const pipe = <T>(...fns: Array<(x: T) => T>) =>
  (initial: T) => fns.reduce((v, f) => f(v), initial);

const processInput = pipe(
  trim,
  toLowerCase,
  validate,
  transform
);
```

### Dependency Injection
```typescript
// Before (hardcoded import)
import { logger } from './logger';
const service = { log: () => logger.info('...') };

// After (injected)
type Logger = { info: (msg: string) => void };
const createService = (logger: Logger) => ({
  log: () => logger.info('...'),
});
```

## Test Commands

```bash
# Must stay GREEN
npm test

# TypeScript strict check
npx tsc --noEmit --strict

# Lint check
npm run lint

# Coverage verification
npm test -- --coverage
```

## Feedback Loop

```
Review → Identify Issue → Plan Fix → Apply → Test → Verify
   ↑__________________________________________________|
```

## Output

The command produces:
1. Initial review scores
2. Refactored code
3. Explanation of changes
4. Final review scores
5. Test verification (GREEN)

## Example

```
/refactor src/services/order-service.ts
```

Output:
```
Initial Scores:
  SOLID: 72% (Target: 90%)
  Clean Code: 65% (Target: 90%)

Applied Refactorings:
  1. Extracted validation into separate function
  2. Replaced conditional with strategy pattern
  3. Introduced Result pattern for error handling

Final Scores:
  SOLID: 94% ✓
  Clean Code: 91% ✓

Tests: All passing ✓
```

## Related Commands
- `/tdd` - Complete TDD cycle
- `/review` - Code review only
- `/green` - Implement minimal code
