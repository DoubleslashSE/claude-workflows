# /review - Code Review

## Description
Review code for principle compliance and generate structured feedback.

## Usage
```
/review [file-path]
```

## Arguments
- `file-path`: (Optional) Path to file or directory to review

## Agent
Uses the `reviewer` agent with all skills.

## Skills
- `tdd-workflow`
- `solid-principles`
- `clean-code`
- `functional-patterns`

## Review Scope

### 1. Test Quality
- AAA pattern adherence
- Meaningful test names
- Comprehensive coverage
- Test isolation
- Async testing patterns

### 2. SOLID Principles
- **S**ingle Responsibility
- **O**pen/Closed
- **L**iskov Substitution
- **I**nterface Segregation
- **D**ependency Inversion

### 3. Clean Code
- **DRY**: No duplication
- **KISS**: Simple solutions
- **YAGNI**: No unused code
- Small functions (< 20 lines)
- Clear naming

### 4. TypeScript Quality
- Strict mode compliance
- No `any` abuse
- Proper null handling
- Type-safe patterns

### 5. Functional Patterns
- Pure functions
- Immutability
- Composition
- Result pattern
- Explicit error handling

## Quality Gates

| Category | Weight | Target |
|----------|--------|--------|
| SOLID Compliance | 30% | 90% |
| Clean Code | 25% | 90% |
| Test Quality | 25% | 90% |
| TS/Functional | 20% | 95% |

## Output Format

```markdown
# Code Review Report

## Summary
Brief overview of findings.

## Scores

| Category | Score | Target | Status |
|----------|-------|--------|--------|
| SOLID | 85% | 90% | NEEDS WORK |
| Clean Code | 78% | 90% | NEEDS WORK |
| Tests | 92% | 90% | PASS |
| TS/Functional | 88% | 95% | NEEDS WORK |

**Overall**: 85% (Weighted Average)

## Critical Issues

### 1. SRP Violation in OrderService
- **Location**: `src/services/order-service.ts:45-120`
- **Issue**: Class handles validation, processing, and notification
- **Impact**: Difficult to test and maintain
- **Fix**: Extract into ValidatorService, ProcessorService, NotifierService

### 2. Missing Error Handling
- **Location**: `src/api/handlers.ts:23`
- **Issue**: JSON.parse without try/catch
- **Impact**: Unhandled exceptions crash server
- **Fix**: Wrap in Result pattern

## Recommendations

### 1. Introduce Result Pattern
- **Current**: Throwing exceptions for business errors
- **Suggested**: Return Result<T, E> types
- **Benefit**: Explicit error handling, type safety

### 2. Extract Pure Functions
- **Current**: Business logic mixed with I/O
- **Suggested**: Separate pure core from impure shell
- **Benefit**: Easier testing, better composition

## Action Items

Priority order for refactoring:

1. [ ] Extract validation into separate module
2. [ ] Implement Result pattern for error handling
3. [ ] Add missing async error handling
4. [ ] Split large functions (> 20 lines)
5. [ ] Remove code duplication in validators
```

## Common Issues Detected

### TypeScript Issues
```typescript
// Flagged: any type usage
const process = (data: any) => { ... }

// Flagged: implicit undefined
const name = user.profile.name;

// Flagged: type assertion abuse
const user = data as User;
```

### Clean Code Issues
```typescript
// Flagged: magic numbers
if (password.length < 8) { ... }

// Flagged: long function
const processOrder = () => {
  // 50+ lines of code
};

// Flagged: unclear naming
const d = new Date();
const x = calculate(a, b);
```

### SOLID Issues
```typescript
// Flagged: God class
class OrderService {
  validate() { ... }
  process() { ... }
  notify() { ... }
  report() { ... }
}

// Flagged: hardcoded dependency
import { db } from './database';
```

## Verification Commands

```bash
# Run tests
npm test

# TypeScript strict check
npx tsc --noEmit --strict

# Lint
npm run lint

# Coverage
npm test -- --coverage
```

## Example

```
/review src/services/
```

## Related Commands
- `/refactor` - Apply improvements
- `/tdd` - Full TDD cycle
