---
description: Review code for TDD best practices and clean code principles compliance
---

# Code Review

Review the code for: **$ARGUMENTS**

## Review Scope

1. **Test Quality**
   - AAA pattern compliance
   - Proper naming conventions
   - Test independence
   - Appropriate assertions

2. **SOLID Principles**
   - Single Responsibility
   - Open/Closed
   - Liskov Substitution
   - Interface Segregation
   - Dependency Inversion

3. **Clean Code**
   - DRY - No duplication
   - KISS - Simplicity
   - YAGNI - No unused code
   - CQS - Command/Query separation

4. **Code Quality**
   - Naming clarity
   - Error handling
   - Security considerations

## Review Checklist

### Tests
- [ ] Follow AAA pattern
- [ ] Naming: `{Method}_{Scenario}_{Expected}`
- [ ] One behavior per test
- [ ] No test interdependencies
- [ ] Edge cases covered

### Implementation
- [ ] Single responsibility per class
- [ ] Extensible design
- [ ] Proper abstractions
- [ ] No duplication
- [ ] Simple solutions
- [ ] No dead code

### Security
- [ ] Input validation
- [ ] No injection vulnerabilities
- [ ] Sensitive data protected

## Output Format

Provide a structured review report:

```markdown
## Review Summary
- Files Reviewed: X
- Issues Found: X
- Severity: Critical/High/Medium/Low

## Issues

| Location | Issue | Severity | Fix |
|----------|-------|----------|-----|
| file:line | Description | Level | Suggestion |

## Principle Compliance

| Principle | Status |
|-----------|--------|
| SRP | PASS/FAIL |
| OCP | PASS/FAIL |
| ... | ... |

## Recommendations
1. Critical fixes
2. High priority
3. Medium priority
4. Nice to have

## Overall Assessment
Summary and key action items
```
