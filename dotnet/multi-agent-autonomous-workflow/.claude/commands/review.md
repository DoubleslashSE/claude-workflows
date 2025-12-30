---
description: Perform a code review using the reviewer subagent
argument-hint: [files or story to review]
allowed-tools: Read, Glob, Grep, Task
---

# Code Review

Perform a code review on:

**Target:** $ARGUMENTS

## Process

1. Gather changed files using git:
   ```bash
   git diff --name-only HEAD~1
   ```

2. Invoke the `reviewer` subagent with:
   - List of files to review
   - Context about what was changed
   - Instructions to check architecture, security, and code quality

3. If any security concerns, also invoke `security` subagent

## Review Checklist

The reviewer will check:
- [ ] Clean Architecture compliance
- [ ] SOLID principles
- [ ] No security vulnerabilities
- [ ] Proper error handling
- [ ] Test coverage adequate
- [ ] Code is maintainable

Begin by identifying the files to review and invoking the reviewer subagent.
