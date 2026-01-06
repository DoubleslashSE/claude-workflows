---
description: Execute complete TDD cycle (RED-GREEN-REFACTOR) for implementing a feature
---

# TDD Workflow

Execute the complete TDD cycle for: **$ARGUMENTS**

## Workflow Steps

### Phase 1: RED - Design Tests
1. Analyze the feature requirements
2. Identify test scenarios (happy path, edge cases, errors)
3. Write failing tests following AAA pattern
4. Verify tests fail for the RIGHT reason

### Phase 2: GREEN - Implement
1. Write minimal code to pass tests
2. Focus on simplest solution
3. Run tests to confirm they pass
4. Do NOT optimize yet

### Phase 3: REFACTOR - Improve
1. Identify code smells and improvements
2. Apply SOLID, DRY, KISS, YAGNI, CQS principles
3. Run tests after each change
4. Keep tests green throughout

## Test Naming Convention
```
{MethodUnderTest}_{Scenario}_{ExpectedBehavior}
```

## Commands Available
```bash
# Run all tests
dotnet test

# Run specific test
dotnet test --filter "FullyQualifiedName~{TestName}"

# Run with coverage
dotnet test /p:CollectCoverage=true
```

## Principles to Follow

### TDD
- Tests first, implementation second
- One test at a time
- Refactor only with green tests

### SOLID
- **S**: Single Responsibility
- **O**: Open/Closed
- **L**: Liskov Substitution
- **I**: Interface Segregation
- **D**: Dependency Inversion

### Clean Code
- **DRY**: Don't Repeat Yourself
- **KISS**: Keep It Simple
- **YAGNI**: You Aren't Gonna Need It
- **CQS**: Command Query Separation

## Output Expected
Provide a summary after completing the TDD cycle:
- Tests created
- Implementation details
- Refactorings applied
- Final test results
