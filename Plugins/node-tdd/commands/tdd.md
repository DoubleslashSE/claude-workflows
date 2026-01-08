# /tdd - Complete TDD Cycle

## Description
Execute a complete RED-GREEN-REFACTOR TDD cycle for Node.js/TypeScript development.

## Usage
```
/tdd <feature-description>
```

## Arguments
- `feature-description`: Description of the feature or behavior to implement

## Workflow

### Phase 1: RED (Design Failing Tests)

1. **Analyze Requirements**
   - Parse feature description
   - Identify core behaviors to test
   - Plan test categories (unit, integration)

2. **Design Tests**
   - Use the `test-designer` agent
   - Create comprehensive test suite
   - Cover happy path, edge cases, errors

3. **Verify RED**
   - Run tests: `npm test`
   - Confirm tests fail for correct reasons
   - Adjust test design if needed

### Phase 2: GREEN (Implement Minimal Code)

1. **Implement Incrementally**
   - Use the `implementer` agent
   - One failing test at a time
   - Minimal code to pass

2. **Verify Each Step**
   - Run tests after each implementation
   - Track progress through test suite
   - Document design decisions

3. **Achieve GREEN**
   - All tests passing
   - No implementation beyond requirements
   - TypeScript compiling clean

### Phase 3: REFACTOR (Improve Design)

1. **Review Code**
   - Use the `reviewer` agent
   - Assess SOLID compliance
   - Check clean code practices

2. **Apply Improvements**
   - Use the `refactorer` agent
   - Incremental refactorings
   - Tests stay GREEN

3. **Quality Gates**
   | Metric | Target |
   |--------|--------|
   | SOLID Compliance | 90% |
   | Clean Code | 90% |
   | Test Coverage | 90% |
   | TypeScript Strict | 100% |

### Feedback Loop

Each phase includes iterative feedback:

```
RED:
  Design → Run → Analyze → Adjust
  ↑__________________________|

GREEN:
  Implement → Run → Analyze → Fix
  ↑____________________________|

REFACTOR:
  Review → Refactor → Run → Verify
  ↑_____________________________|
```

## Example

```
/tdd Create a user registration service that validates email format, checks password strength, and stores user data
```

This will:
1. Design tests for email validation, password strength, user storage
2. Implement validators and service incrementally
3. Refactor for SOLID principles and clean code

## Output

The command produces:
- Complete test suite
- Implementation code
- Review report with scores
- Iteration history

## Related Commands
- `/red` - Run only the RED phase
- `/green` - Run only the GREEN phase
- `/refactor` - Run only the REFACTOR phase
- `/review` - Run code review
