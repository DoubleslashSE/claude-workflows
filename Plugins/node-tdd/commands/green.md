# /green - Implement Minimal Code (GREEN Phase)

## Description
Write minimal code to make failing tests pass in the GREEN phase of TDD.

## Usage
```
/green [test-file-path]
```

## Arguments
- `test-file-path`: (Optional) Path to the test file to implement against

## Agent
Uses the `implementer` agent with `tdd-workflow` and `solid-principles` skills.

## Workflow

1. **Identify Failing Tests**
   - Run test suite
   - List all failing tests
   - Prioritize by dependency order

2. **Implement Incrementally**
   - Focus on one failing test
   - Write minimal code to pass
   - Run tests to verify

3. **Progress Tracking**
   - Track tests passing vs failing
   - Document implementation decisions
   - Note any design discoveries

4. **Achieve GREEN**
   - All tests passing
   - TypeScript compiling
   - No extra code added

## Implementation Philosophy

### Minimal Code
Write ONLY what's needed to pass the current test:

```typescript
// Test expects: add(2, 3) === 5

// Step 1: Fake it (if only one test case)
const add = (a: number, b: number): number => 5;

// Step 2: Generalize (when more tests force it)
const add = (a: number, b: number): number => a + b;
```

### One Test at a Time
```
Run tests → Pick first failure → Implement → Run tests → Repeat
```

### Ugly is OK
```typescript
// Acceptable in GREEN phase:
const processOrder = (order: Order) => {
  if (order.items.length === 0) return Result.fail('empty');
  if (order.total < 0) return Result.fail('invalid');
  // More inline logic is fine - refactor later
  return Result.ok({ processed: true });
};
```

## TypeScript Patterns

### Factory Functions
```typescript
export const createValidator = () => ({
  validate: (input: string) => {
    // Minimal implementation
  },
});
```

### Dependency Injection
```typescript
export const createService = (deps: Dependencies) => ({
  execute: async () => {
    // Use injected deps
  },
});
```

### Result Pattern
```typescript
export const parseInput = (raw: string): Result<Parsed, ParseError> => {
  try {
    return Result.ok(JSON.parse(raw));
  } catch {
    return Result.fail({ code: 'PARSE_ERROR' });
  }
};
```

## Test Execution

```bash
# Run all tests
npm test

# Run specific test file
npm test -- path/to/test.ts

# Watch mode
npm test -- --watch

# With Vitest
vitest run
vitest watch
```

## Progress Output

```
Test Suite: user-service.test.ts
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ should create user with valid data
✓ should reject invalid email
✗ should hash password before storing
✗ should emit user.created event

Progress: 2/4 tests passing
Next: Implement password hashing
```

## Output

The command produces:
1. Implementation code
2. Test execution results
3. Progress summary
4. Remaining failures (if any)

## Example

```
/green src/services/user-service.test.ts
```

## Related Commands
- `/tdd` - Complete TDD cycle
- `/red` - Design failing tests
- `/refactor` - Improve code design
