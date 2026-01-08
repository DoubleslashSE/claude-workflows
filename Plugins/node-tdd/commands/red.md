# /red - Design Failing Tests (RED Phase)

## Description
Design comprehensive failing tests for a feature or behavior in the RED phase of TDD.

## Usage
```
/red <behavior-description>
```

## Arguments
- `behavior-description`: Description of the behavior to test

## Agent
Uses the `test-designer` agent with `tdd-workflow` skill.

## Workflow

1. **Analyze Behavior**
   - Parse the behavior description
   - Identify testable units
   - Map out test scenarios

2. **Design Test Cases**
   - Happy path scenarios
   - Edge cases (empty, null, boundaries)
   - Error scenarios
   - Async behavior

3. **Create Test Suite**
   - TypeScript test file
   - AAA pattern (Arrange-Act-Assert)
   - Proper test naming

4. **Execute and Verify**
   - Run: `npm test` or `vitest run`
   - Verify tests fail
   - Confirm failures are for correct reasons

## Test Structure Template

```typescript
import { describe, it, expect, beforeEach } from 'vitest';

describe('FeatureName', () => {
  describe('methodName', () => {
    // Happy path
    it('should return expected result when given valid input', () => {
      // Arrange
      const sut = createSystemUnderTest();

      // Act
      const result = sut.methodName(validInput);

      // Assert
      expect(result).toEqual(expectedOutput);
    });

    // Edge case
    it('should handle empty input gracefully', () => {
      const sut = createSystemUnderTest();

      const result = sut.methodName([]);

      expect(result).toEqual([]);
    });

    // Error case
    it('should return failure result when validation fails', () => {
      const sut = createSystemUnderTest();

      const result = sut.methodName(invalidInput);

      expect(result.isFailure).toBe(true);
      expect(result.error.code).toBe('VALIDATION_ERROR');
    });
  });
});
```

## Test Naming Convention

Format: `should {expectedBehavior} when {scenario}`

Examples:
- `should return user when id exists`
- `should return empty array when no matches found`
- `should throw ValidationError when email is invalid`

## Test Categories

| Category | Purpose | Example |
|----------|---------|---------|
| Unit | Pure logic | Validators, transformers |
| Integration | I/O boundaries | API calls, DB access |
| Contract | Type safety | API responses |

## Output

The command produces:
1. Test file with comprehensive test cases
2. Test execution command
3. Expected failure output
4. Test design rationale

## Example

```
/red User email validation should accept valid formats and reject invalid ones
```

Output:
```typescript
describe('validateEmail', () => {
  it('should return success for valid email format', () => {...});
  it('should return failure for email without @ symbol', () => {...});
  it('should return failure for email without domain', () => {...});
  it('should return failure for empty string', () => {...});
});
```

## Related Commands
- `/tdd` - Complete TDD cycle
- `/green` - Implement to pass tests
