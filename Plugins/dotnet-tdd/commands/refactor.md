---
description: REFACTOR phase - Improve code design while keeping tests green
---

# REFACTOR Phase - Improve Design

Improve the code design for: **$ARGUMENTS**

## Your Task

1. **Identify Improvements**
   - Code smells
   - Principle violations
   - Duplication
   - Complexity

2. **Apply Refactorings**
   - One change at a time
   - Run tests after each change
   - Keep tests GREEN

3. **Verify Quality**
   - All tests still pass
   - Code is cleaner
   - Principles followed

## Principles Checklist

### SOLID
- [ ] **S**ingle Responsibility - One reason to change
- [ ] **O**pen/Closed - Extensible without modification
- [ ] **L**iskov Substitution - Subtypes substitutable
- [ ] **I**nterface Segregation - Specific interfaces
- [ ] **D**ependency Inversion - Depend on abstractions

### Clean Code
- [ ] **DRY** - No duplication
- [ ] **KISS** - Simple solutions
- [ ] **YAGNI** - No unused code
- [ ] **CQS** - Separated commands/queries

## Common Refactorings

| Refactoring | When to Apply |
|-------------|---------------|
| Extract Method | Long methods, repeated code |
| Rename | Unclear naming |
| Extract Interface | Concrete dependencies |
| Replace Conditional | Switch statements |
| Extract Class | Mixed responsibilities |

## REFACTOR Rules

1. **Tests stay GREEN** - Never break tests
2. **Small steps** - One change at a time
3. **Run tests often** - After every change
4. **Commit frequently** - Preserve progress

## Commands

```bash
# Run tests
dotnet test

# Format code
dotnet format

# Check coverage
dotnet test /p:CollectCoverage=true
```

## Output Required

Provide:
1. Identified code smells/violations
2. Refactorings applied (before/after)
3. Test results showing GREEN
4. Summary of improvements
