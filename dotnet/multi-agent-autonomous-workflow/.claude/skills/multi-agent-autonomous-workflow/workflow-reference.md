# Workflow Reference

Detailed reference for the multi-agent autonomous workflow.

## Subagent Invocation

### Analyst
```
Invoke subagent: analyst
Goal: [User's goal description]
Context: This is a .NET 10 Clean Architecture project with CQRS pattern.

Expected output: User stories with acceptance criteria
```

### Architect
```
Invoke subagent: architect
Stories: [Stories from analyst]
Constraints: Follow Clean Architecture, use CQRS pattern

Expected output: Technical design with file changes
```

### Developer
```
Invoke subagent: developer
Story: [Story title and acceptance criteria]
Design: [Relevant design from architect]

Expected output: Implementation log with test results
```

### Tester
```
Invoke subagent: tester
Story: [Story title and acceptance criteria]
Implementation: [Summary from developer]

Expected output: Test report (PASS/FAIL)
```

### Reviewer
```
Invoke subagent: reviewer
Story: [Story title]
Files: [List of changed files]

Expected output: Review (APPROVED/CHANGES REQUESTED)
```

### Security
```
Invoke subagent: security
Story: [Story title]
Files: [List of security-sensitive files]

Expected output: Security review (SECURE/NEEDS REMEDIATION)
```

## State Management

### Initialize Workflow
```bash
python .claude/hooks/state.py init "Goal description"
```

### Update Story Status
```bash
python .claude/hooks/state.py update-story S1 in_progress
python .claude/hooks/state.py update-story S1 completed
```

### Check Status
```bash
python .claude/hooks/state.py status
```

## Quality Gates

### G1: Pre-Implementation
- [ ] Design is complete
- [ ] Acceptance criteria are clear
- [ ] Dependencies identified

### G2: Post-Implementation
- [ ] `dotnet build` passes
- [ ] `dotnet test` passes
- [ ] All acceptance criteria covered

### G3: Coverage
- [ ] Coverage meets threshold
- [ ] Edge cases tested
- [ ] Error handling verified

### G4: Security (if applicable)
- [ ] OWASP Top 10 checked
- [ ] No vulnerabilities found
- [ ] Security scan clean

## Failure Recovery

### Developer Fails (3+ times)
1. Pause execution
2. Analyze root cause
3. Invoke architect for redesign
4. If still stuck, escalate to human

### Test Loop (developer → tester → developer × 3)
1. Perform root cause analysis
2. Check if test is correct
3. Consider splitting story
4. Escalate if unclear

### Security Issue Found
1. Immediately escalate to human
2. Document vulnerability details
3. Block deployment until fixed

## Progress Reporting

Generate progress report every 60 minutes or 3 completed stories:

```markdown
## Progress Report

**Status:** X/Y stories complete (Z%)
**Current:** [Story in progress]

**Quality Metrics:**
- Tests: X passing
- Coverage: Y%
- Reviews: Z approved

**Decisions Made:**
1. [Key decision]

**Next Checkpoint:** [When]
```
