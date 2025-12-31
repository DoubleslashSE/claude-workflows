# Workflow Reference

Detailed reference for the multi-agent autonomous workflow with iteration patterns.

## Subagent Invocation Patterns

### Analyst (Phase 1)
```markdown
## Task for Analyst Subagent

**Goal:** [User's goal description]
**Context:** This is a .NET 10 Clean Architecture project with CQRS pattern.

**Requirements:**
1. Break down the goal into discrete user stories
2. Define clear acceptance criteria for each story
3. Estimate size (S/M/L/XL) for each story
4. Flag security-sensitive stories
5. Identify dependencies between stories

**Expected Output Format:**
- List of user stories with acceptance criteria
- Recommended implementation order
- Open questions requiring clarification
```

### Architect (Phase 1)
```markdown
## Task for Architect Subagent

**Stories:** [Stories from analyst]
**Constraints:** Follow Clean Architecture, use CQRS pattern

**Requirements:**
1. Design component structure for each story
2. Document key architectural decisions (ADRs)
3. Identify file changes per story
4. Flag technical risks and mitigations

**Expected Output Format:**
- Technical design per story
- File change list with purposes
- Architecture decisions with rationale
```

### Developer (Phase 2 - with Retry Context)
```markdown
## Task for Developer Subagent

**Story:** [Story title]
**Acceptance Criteria:**
- AC1: [Criterion]
- AC2: [Criterion]

**Technical Design:** [Relevant design from architect]

**Iteration:** {n}/3
**Previous Failures:** [List issues from prior attempts, or "First attempt"]
**Fix Instructions:** [Specific guidance, or "None - initial implementation"]

**Requirements:**
1. Follow TDD: RED → GREEN → REFACTOR
2. Run `dotnet build` and `dotnet test` before completion
3. Return structured implementation log
4. If build/tests fail, analyze and retry (up to 3 times)

**Expected Output Format:**
- Implementation log with test results
- Files changed with descriptions
- Build status: PASS/FAIL
- Test status: X passing, Y failing
```

### Tester (Phase 2 - Verification)
```markdown
## Task for Tester Subagent

**Story:** [Story title]
**Acceptance Criteria:**
- AC1: [Criterion]
- AC2: [Criterion]

**Implementation Summary:** [From developer]
**Files Changed:** [List from developer]

**Requirements:**
1. Run `dotnet test` and verify all pass
2. Check coverage meets threshold for story size
3. Verify each acceptance criterion has tests
4. Add edge case tests if missing
5. Return PASS or FAIL with specific issues

**Expected Output Format:**
- Verdict: PASS or FAIL
- Acceptance criteria status (each one)
- Coverage analysis
- Issues found (if FAIL): specific file:line references
```

### Reviewer (Phase 2 - Code Review)
```markdown
## Task for Reviewer Subagent

**Story:** [Story title]
**Files Changed:** [List of files]
**Implementation Summary:** [Brief description]

**Requirements:**
1. Check architecture compliance (Clean Architecture)
2. Verify code quality and naming conventions
3. Check for anti-patterns and code smells
4. Identify security considerations
5. Return APPROVED or CHANGES_REQUESTED

**Expected Output Format:**
- Verdict: APPROVED or CHANGES_REQUESTED
- Architecture compliance: PASS/FAIL
- Code quality findings
- Required changes (if any): specific file:line with fix
```

### Security (Phase 2 - If Flagged)
```markdown
## Task for Security Subagent

**Story:** [Story title]
**Files Changed:** [List of security-sensitive files]
**Security Concerns:** [Specific areas to review]

**Requirements:**
1. Check OWASP Top 10 compliance
2. Review authentication/authorization logic
3. Check input validation and output encoding
4. Verify secure data handling
5. Return SECURE or NEEDS_REMEDIATION

**Expected Output Format:**
- Verdict: SECURE or NEEDS_REMEDIATION
- OWASP checklist results
- Vulnerabilities found (if any): CWE reference, file:line, fix
```

## Iteration Loop Protocol

### Standard Flow (Happy Path)
```
Developer → PASS → Tester → PASS → Reviewer → APPROVED → [Security if needed] → COMPLETE
```

### Retry Flow (On Failure)
```
Developer → PASS → Tester → FAIL
                              ↓
                    Extract failure details
                              ↓
            Developer (iteration 2, with failures) → ...
```

### Iteration Context Template
When invoking developer on retry, ALWAYS include:

```markdown
## Retry Context

**Iteration:** 2/3 (or 3/3)
**Story:** [Title]

### What Was Implemented
[Summary of implementation from last attempt]

### What Failed
**Source:** Tester (or Reviewer/Security)
**Issues:**
1. `src/Domain/Entity.cs:45` - Validation missing for null input
2. `tests/UnitTests/EntityTests.cs:23` - Test expects exception but none thrown

### Required Fixes
1. Add null check in Entity constructor
2. Ensure ArgumentNullException is thrown

### Files to Review
- `src/Domain/Entity.cs` - Add validation
- `tests/UnitTests/EntityTests.cs` - Verify test correctness
```

## State Management Commands

### Full Command Reference
```bash
# Initialize or resume workflow
python .claude/hooks/state.py init "Goal description"
python .claude/hooks/state.py init "Goal" --session SESSION_ID

# Add stories with metadata
python .claude/hooks/state.py add-story "Story title"
python .claude/hooks/state.py add-story "Story title" --size L
python .claude/hooks/state.py add-story "Story title" --size M --ac "First criterion"

# Update story status
python .claude/hooks/state.py update-story S1 pending
python .claude/hooks/state.py update-story S1 in_progress
python .claude/hooks/state.py update-story S1 in_progress --agent developer
python .claude/hooks/state.py update-story S1 completed

# Manage blockers
python .claude/hooks/state.py add-blocker "Description" --severity high
python .claude/hooks/state.py resolve-blocker 0

# Record decisions
python .claude/hooks/state.py add-decision "Title" "Choice" "Rationale"

# Checkpoint management
python .claude/hooks/state.py checkpoint  # Returns exit code 2 if checkpoint due
python .claude/hooks/state.py record-review

# Check status
python .claude/hooks/state.py status

# Complete workflow
python .claude/hooks/state.py complete
```

## Quality Gates

### G1: Pre-Implementation
- [ ] Design is complete for the story
- [ ] Acceptance criteria are clear and testable
- [ ] Dependencies on other stories identified
- [ ] Required interfaces/contracts defined

### G2: Post-Implementation
- [ ] `dotnet build` passes with no errors
- [ ] `dotnet test` passes with no failures
- [ ] All acceptance criteria have corresponding tests
- [ ] No compiler warnings in new code

### G3: Coverage
| Story Size | Unit Tests | Integration Tests | Coverage Target |
|------------|------------|-------------------|-----------------|
| S (Small)  | 2+         | 0                 | 70%             |
| M (Medium) | 5+         | 1+                | 80%             |
| L (Large)  | 10+        | 3+                | 85%             |
| XL (Extra) | 20+        | 5+                | 90%             |

### G4: Security (if applicable)
- [ ] OWASP Top 10 compliance verified
- [ ] No hardcoded secrets or credentials
- [ ] Input validation on all user input
- [ ] Output encoding where applicable
- [ ] Secure session/token handling

## Failure Recovery Strategies

### Developer Fails Build (3+ times)
1. **Analyze error patterns:**
   - Missing dependency? → Check project references
   - Type mismatch? → Review interface contracts
   - Ambiguous reference? → Check using statements
2. **Invoke architect for redesign** if structural issue
3. **Escalate to human** with full error log if unclear

### Tester Reports FAIL
1. **Parse failure report** for specific issues
2. **Categorize failures:**
   - Missing functionality → Developer implements
   - Incorrect behavior → Developer fixes logic
   - Test incorrect → Tester reviews test
3. **Pass context to developer** with file:line references
4. **Track iteration count** - escalate after 3 cycles

### Reviewer Requests Changes
1. **Compile change requests** into actionable list
2. **Prioritize:** Security > Architecture > Quality
3. **Re-invoke developer** with changes as requirements
4. **Re-run full verification** after changes

### Security Finds Vulnerability
1. **Immediate escalation** for high/critical severity
2. **Document vulnerability** with CWE reference
3. **Block completion** until remediated
4. **Re-verify after fix** with security agent

## Progress Reporting Template

Generate every 60 minutes or 3 completed stories:

```markdown
## Workflow Progress Report

**Workflow ID:** {workflow_id}
**Goal:** {original_goal}
**Runtime:** {hours}h {minutes}m

### Progress Summary
**Status:** {completed}/{total} stories complete ({percentage}%)

### Story Status
| ID | Title | Status | Attempts |
|----|-------|--------|----------|
| S1 | [Title] | ✅ completed | 1 |
| S2 | [Title] | ✅ completed | 2 |
| S3 | [Title] | 🔄 in_progress | 1 |
| S4 | [Title] | ⏳ pending | 0 |

### Quality Metrics
- **Build:** PASSING
- **Tests:** {passing} passing, {total} total
- **Coverage:** {percentage}%
- **Reviews:** {approved}/{total} approved

### Architectural Decisions
- **ADR-001:** {title} - {choice}
- **ADR-002:** {title} - {choice}

### Current Blockers
{blockers_or_none}

### Next Actions
1. {next_action}
2. {following_action}

### Checkpoint Status
- Stories since last review: {count}/5
- Next checkpoint: {when}
```
