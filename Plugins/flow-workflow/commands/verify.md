---
name: verify
description: Run verification and user acceptance testing to validate implementation meets requirements
user_invocable: true
---

# Verify Phase

You are starting the VERIFY phase of the flow-workflow. This phase validates that the implementation meets requirements through automated checks and user acceptance testing.

## What to Do

1. **Check for active work item** from ACTIVE.md
2. **Verify EXECUTE is complete** (all tasks done)
3. **Run automated checks** (build, test, lint)
4. **Verify requirements traceability**
5. **Conduct UAT** with user
6. **Collect sign-off** or document issues
7. **Complete workflow** on approval

## Active Item Check

### Required: Active Work Item

First, verify there's an active work item:

1. **Read `.flow/ACTIVE.md`** to get current item
2. **If no active item**: Prompt user to select or create one
3. **If active item exists**: Use its directory for all state files

```markdown
# No Active Item

There is no active work item. Please:
- `/flow-workflow:new [title] --start` - Create and start new item
- `/flow-workflow:switch ITEM-XXX` - Activate an existing item
- `/flow-workflow:flow [task]` - Start full workflow (creates item)
```

### Item State Directory

All state files are stored in the active item's directory:
- `.flow/items/ITEM-XXX/STATE.md`
- `.flow/items/ITEM-XXX/PLAN.md`
- `.flow/items/ITEM-XXX/REQUIREMENTS.md`

## Starting VERIFY Phase

### Verify Prerequisites

Check that EXECUTE phase is complete for the active item:
- All tasks in item's PLAN.md are completed (or explicitly skipped)
- No active blockers preventing verification

If not ready:
```markdown
**Cannot Start VERIFY Phase**

**Work Item**: ITEM-XXX - [Title]

EXECUTE phase must be completed first.

**Current state**:
- Tasks completed: [X]/[Y]
- Tasks blocked: [N]

**Options**:
1. Complete execution: `/flow-workflow:execute`
2. Skip remaining tasks and verify completed work
```

### Update Item STATE.md

Update `.flow/items/ITEM-XXX/STATE.md`:

```markdown
## Current Phase

**Phase**: VERIFY
**Started**: [TIMESTAMP]
**Progress**: 0%
```

Also update `.flow/BACKLOG.md` to reflect item status change to VERIFY.

## Spawn Verifier Agent

Use the Task tool to spawn the verifier agent:

```markdown
Spawn flow-workflow:verifier agent with context:
- Active item: ITEM-XXX
- Item directory: .flow/items/ITEM-XXX/
- Item's PLAN.md with completed tasks
- Item's REQUIREMENTS.md with requirements
- Item's STATE.md with decisions
```

The verifier will:
1. Run automated checks
2. Verify requirements coverage
3. Guide UAT with user
4. Collect sign-off

## Verification Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                   VERIFY PHASE FLOW                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. AUTOMATED CHECKS                                            │
│     ├─ Build verification                                       │
│     ├─ Test execution                                           │
│     ├─ Lint/style check                                         │
│     └─ Type checking (if applicable)                            │
│                                                                 │
│  2. REQUIREMENTS VERIFICATION                                   │
│     ├─ Trace requirements to tasks                              │
│     ├─ Trace tasks to implementation                            │
│     ├─ Verify acceptance criteria                               │
│     └─ Document coverage                                        │
│                                                                 │
│  3. USER ACCEPTANCE TESTING                                     │
│     ├─ Present test scenarios                                   │
│     ├─ Guide user through testing                               │
│     ├─ Collect pass/fail feedback                               │
│     └─ Document issues found                                    │
│                                                                 │
│  4. SIGN-OFF                                                    │
│     ├─ Present verification report                              │
│     ├─ Collect user approval                                    │
│     └─ Document decision                                        │
│                                                                 │
│  5. COMPLETE OR ITERATE                                         │
│     ├─ If approved: Complete workflow                           │
│     └─ If issues: Return to EXECUTE                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Automated Checks

### Build Check

```bash
# Run appropriate build command
npm run build          # Node.js
dotnet build           # .NET
python -m py_compile   # Python
```

### Test Check

```bash
# Run test suite
npm test               # Node.js
dotnet test            # .NET
pytest                 # Python
```

### Lint Check

```bash
# Run linting
npm run lint           # Node.js
dotnet format --verify-no-changes  # .NET
flake8                 # Python
```

### Results Recording

```markdown
## Automated Verification

### Build: [PASS/FAIL]
```
[build output summary]
```

### Tests: [PASS/FAIL]
- Total: [N]
- Passed: [N]
- Failed: [N]
- Coverage: [X]%

### Lint: [PASS/FAIL]
- Errors: [N]
- Warnings: [N]
```

## Requirements Verification

### Traceability Matrix

```markdown
## Requirements Traceability

| Requirement | Tasks | Implementation | Verified |
|-------------|-------|----------------|----------|
| FR-001 | TASK-001, TASK-002 | src/auth/* | YES |
| FR-002 | TASK-003 | src/user/* | YES |
| NFR-001 | TASK-004 | Performance tests | YES |
```

### Acceptance Criteria Check

For each requirement:
1. Read acceptance criteria from REQUIREMENTS.md
2. Verify each criterion is met
3. Document evidence

```markdown
### FR-001: User Authentication

**Acceptance Criteria**:
- [x] User can login with email/password
  - Evidence: LoginService.login() implemented and tested
- [x] User receives error on invalid credentials
  - Evidence: LoginService returns appropriate error codes
- [x] Session is created on successful login
  - Evidence: SessionManager.create() called in login flow
```

## User Acceptance Testing

### UAT Scenarios

Create scenarios from requirements:

```markdown
## UAT Scenarios

### Scenario 1: User Login (FR-001)

**Purpose**: Verify user can login successfully

**Steps**:
1. Navigate to login page
2. Enter valid email and password
3. Click login button

**Expected**:
- User is redirected to dashboard
- Welcome message displays user name

**Result**: [PENDING]
```

### Conduct UAT

Use AskUserQuestion to guide testing:

```javascript
AskUserQuestion({
  questions: [{
    question: "Please test the login scenario. Did it work as expected?",
    header: "Login UAT",
    multiSelect: false,
    options: [
      { label: "Pass", description: "Login works correctly as described" },
      { label: "Fail - Blocked", description: "Cannot complete the scenario" },
      { label: "Fail - Wrong behavior", description: "Completes but behaves incorrectly" }
    ]
  }]
})
```

### Document UAT Results

```markdown
### UAT Results

| Scenario | Status | Notes |
|----------|--------|-------|
| User Login | PASS | Works as expected |
| User Logout | PASS | Session cleared correctly |
| Error Handling | FAIL | Error message unclear |
```

## Issues Documentation

### Issue Format

```markdown
### ISSUE-001: [Title]
**Severity**: Critical | Major | Minor
**Found in**: [UAT scenario or automated check]
**Description**: [What went wrong]
**Expected**: [What should happen]
**Actual**: [What happened]
**Recommendation**: [Fix suggestion]
```

## Verification Report

### Generate Report

```markdown
# Verification Report

**Generated**: [TIMESTAMP]
**Workflow**: [name]

## Summary

| Category | Status |
|----------|--------|
| Automated Checks | [PASS/FAIL] |
| Requirements | [X/Y Verified] |
| UAT | [PASS/ISSUES] |

## Detailed Results

[Include all verification sections]

## Issues Found

[List all issues]

## Recommendation

[APPROVE / NEEDS_WORK]
```

## Sign-off Collection

```javascript
AskUserQuestion({
  questions: [{
    question: "Based on the verification results, do you approve this implementation?",
    header: "Sign-off",
    multiSelect: false,
    options: [
      { label: "Approve", description: "Implementation meets requirements" },
      { label: "Approve with notes", description: "Acceptable with documented issues" },
      { label: "Reject", description: "Needs more work" }
    ]
  }]
})
```

## Completing VERIFY Phase

### On Approval

```markdown
**VERIFY Phase Complete - APPROVED**

**Work Item**: ITEM-XXX - [Title]

**Results**:
- Automated checks: PASSED
- Requirements: [X/Y] verified
- UAT: PASSED
- Issues: [N] (none critical)

**Sign-off**: Approved by user at [TIMESTAMP]

Workflow completing...
```

### On Rejection

```markdown
**VERIFY Phase - Issues Found**

**Work Item**: ITEM-XXX - [Title]

**Results**:
- Issues found: [N]
- Critical issues: [N]

**Next steps**:
1. Address issues in EXECUTE phase
2. Re-run verification

Returning to EXECUTE phase...
```

### Update Item STATE.md

Update `.flow/items/ITEM-XXX/STATE.md`:

```markdown
## Current Phase

**Phase**: VERIFY
**Started**: [timestamp]
**Progress**: 100%
**Completed**: [TIMESTAMP]

### CHECKPOINT: VERIFY-COMPLETE-[TIMESTAMP]
**Result**: [APPROVED/REJECTED]
**Completed**:
- [x] Automated checks
- [x] Requirements verification
- [x] UAT
- [x] Sign-off collected

**Next Action**: [Complete workflow / Return to EXECUTE]
```

Also update `.flow/BACKLOG.md`:
- If APPROVED: Mark item as COMPLETE
- If REJECTED: Keep item in VERIFY status with note about issues

## Skills Used

- **conflict-detection**: For identifying requirement gaps
- **state-management**: For status tracking

## Agent Spawned

- **verifier**: Conducts verification and UAT
