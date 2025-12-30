---
description: Implement a specific user story using TDD with the developer subagent
argument-hint: [story title or description]
allowed-tools: Read, Glob, Grep, Edit, Write, Bash, Task
---

# Implement Story

Implement this story using the developer subagent:

**Story:** $ARGUMENTS

## Process

1. Invoke the `developer` subagent with:
   - The story title and acceptance criteria
   - Any relevant technical design context
   - Instructions to follow TDD (RED → GREEN → REFACTOR → COMMIT)

2. After developer completes, invoke `tester` to verify:
   - All acceptance criteria met
   - Test coverage adequate
   - Edge cases handled

3. After tests pass, invoke `reviewer` for code review:
   - Architecture compliance
   - Code quality
   - Security considerations

4. If the story is security-sensitive, invoke `security` subagent

## Expected Outcomes

- All tests pass (`dotnet test`)
- Build succeeds (`dotnet build`)
- Code review approved
- Commit with clear message

Begin by gathering context about the story and invoking the developer subagent.
