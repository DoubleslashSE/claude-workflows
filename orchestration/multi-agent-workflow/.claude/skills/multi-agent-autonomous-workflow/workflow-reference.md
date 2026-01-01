# Workflow Reference

Detailed reference for the multi-agent autonomous workflow with iteration patterns.

## Platform Auto-Detection (Phase 0)

Before invoking any subagent, dynamically discover and load the platform configuration.

### Step 1: Discover Available Platforms

Scan `Workflows/platforms/` directory for all subdirectories containing `platform.json`:

```
platforms/
├── dotnet/platform.json
├── typescript/platform.json
└── {any-future-platform}/platform.json
```

### Step 2: Read Detection Criteria from Each Platform

Each `platform.json` contains a `detection` section:

```json
{
  "name": "dotnet",
  "detection": {
    "markers": ["*.sln", "*.csproj"],
    "matchMode": "any",    // "any" = at least one marker, "all" = all markers required
    "priority": 100,       // Higher wins on conflict
    "description": "Detected by .sln or .csproj files"
  }
}
```

### Step 3: Match Platforms Against Target Codebase

For each discovered platform:
1. Check if its marker files exist in the target project root
2. Apply `matchMode` logic:
   - `"any"`: Match if ANY marker file exists
   - `"all"`: Match only if ALL marker files exist
3. Collect all matching platforms with their priorities

### Step 4: Select Best Match

```
If matches.length == 0:
    → Ask user or infer from goal
If matches.length == 1:
    → Use that platform
If matches.length > 1:
    → Select platform with highest priority
```

### Step 5: Load Selected Platform

From the winning `platform.json`, extract:
- `commands` - Build, test, lint, coverage commands
- `conventions` - Naming and formatting standards
- `patterns` - File location templates
- `antiPatterns` - Code patterns to avoid
- `qualityGates` - Coverage thresholds by story size
- `projectStructure` - Architecture layers and dependencies
- `skills` - Additional skills to load

### Step 6: Load Platform Skills

For each skill in `platform.json.skills[]`:
```
Read: Workflows/platforms/{platform}/skills/{skill}/SKILL.md
```

### Step 7: Build Platform Context Block

Create this context block to inject into ALL subagent prompts:

```markdown
## Platform Context

**Platform:** {displayName} (v{version})

### Commands
| Action | Command |
|--------|---------|
| Build | `{commands.build}` |
| Test | `{commands.test}` |
| Lint | `{commands.lint}` |
| Coverage | `{commands.coverage}` |

### Project Structure
{projectStructure.description}

**Layers:**
{For each layer in projectStructure.layers}
- **{layer.name}** (`{layer.path}`) - Contains: {layer.contains}
  - Dependencies: {layer.dependencies}

### File Patterns
| Type | Pattern |
|------|---------|
{For each pattern in patterns}
| {patternName} | `{patternPath}` |

### Conventions
- **Test naming:** {conventions.testNaming}
- **Commit format:** {conventions.commitFormat}
- **Branch format:** {conventions.branchFormat}

### Anti-Patterns to Avoid
{For each ap in antiPatterns}
- **{ap.name}:** {ap.reason}

### Quality Thresholds
| Story Size | Coverage |
|------------|----------|
| S | {qualityGates.coverageThresholds.S}% |
| M | {qualityGates.coverageThresholds.M}% |
| L | {qualityGates.coverageThresholds.L}% |
| XL | {qualityGates.coverageThresholds.XL}% |
```

---

## Subagent Invocation Patterns

**IMPORTANT:** Every subagent invocation MUST include the Platform Context block (from Phase 0) at the start.

### Analyst (Phase 1)
```markdown
## Task for Analyst Subagent

{INCLUDE PLATFORM CONTEXT BLOCK HERE}

**Goal:** [User's goal description]

**Requirements:**
1. Break down the goal into discrete user stories
2. Define clear acceptance criteria for each story
3. Estimate size (S/M/L/XL) for each story
4. Flag security-sensitive stories
5. Identify dependencies between stories
6. Consider platform-specific patterns and conventions

**Expected Output Format:**
- List of user stories with acceptance criteria
- Recommended implementation order
- Open questions requiring clarification
```

### Architect (Phase 1)
```markdown
## Task for Architect Subagent

{INCLUDE PLATFORM CONTEXT BLOCK HERE}

**Stories:** [Stories from analyst]

**Requirements:**
1. Design component structure following platform.projectStructure
2. Use file patterns from platform.patterns
3. Document key architectural decisions (ADRs)
4. Identify file changes per story using platform conventions
5. Flag technical risks and mitigations
6. Avoid platform.antiPatterns

**Expected Output Format:**
- Technical design per story
- File change list with purposes (using platform.patterns)
- Architecture decisions with rationale
```

### Developer (Phase 2 - with Retry Context)
```markdown
## Task for Developer Subagent

{INCLUDE PLATFORM CONTEXT BLOCK HERE}

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
2. Use platform.commands.build and platform.commands.test
3. Follow platform.conventions for naming
4. Place files according to platform.patterns
5. Avoid platform.antiPatterns
6. Return structured implementation log

**Expected Output Format:**
- Implementation log with test results
- Files changed with descriptions
- Build status: PASS/FAIL
- Test status: X passing, Y failing
```

### Tester (Phase 2 - Verification)
```markdown
## Task for Tester Subagent

{INCLUDE PLATFORM CONTEXT BLOCK HERE}

**Story:** [Story title]
**Acceptance Criteria:**
- AC1: [Criterion]
- AC2: [Criterion]

**Implementation Summary:** [From developer]
**Files Changed:** [List from developer]

**Requirements:**
1. Run tests using platform.commands.test
2. Check coverage using platform.commands.coverage
3. Verify coverage meets platform.qualityGates.coverageThresholds for story size
4. Verify each acceptance criterion has tests
5. Follow platform.conventions.testNaming for new tests
6. Return PASS or FAIL with specific issues

**Expected Output Format:**
- Verdict: PASS or FAIL
- Acceptance criteria status (each one)
- Coverage analysis vs threshold
- Issues found (if FAIL): specific file:line references
```

### Reviewer (Phase 2 - Code Review)
```markdown
## Task for Reviewer Subagent

{INCLUDE PLATFORM CONTEXT BLOCK HERE}

**Story:** [Story title]
**Files Changed:** [List of files]
**Implementation Summary:** [Brief description]

**Requirements:**
1. Verify files follow platform.patterns locations
2. Check architecture compliance per platform.projectStructure
3. Verify naming follows platform.conventions
4. Scan for platform.antiPatterns violations
5. Identify security considerations
6. Return APPROVED or CHANGES_REQUESTED

**Expected Output Format:**
- Verdict: APPROVED or CHANGES_REQUESTED
- Architecture compliance: PASS/FAIL (vs platform.projectStructure)
- Anti-pattern violations found
- Code quality findings
- Required changes (if any): specific file:line with fix
```

### Security (Phase 2 - If Flagged)
```markdown
## Task for Security Subagent

{INCLUDE PLATFORM CONTEXT BLOCK HERE}

**Story:** [Story title]
**Files Changed:** [List of security-sensitive files]
**Security Concerns:** [Specific areas to review]

**Requirements:**
1. Check OWASP Top 10 compliance
2. Review authentication/authorization logic
3. Check input validation and output encoding
4. Verify secure data handling
5. Check for security-related platform.antiPatterns
6. Return SECURE or NEEDS_REMEDIATION

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
1. `src/path/to/file:45` - Validation missing for null input
2. `tests/path/to/test:23` - Test expects exception but none thrown

### Required Fixes
1. Add null check in constructor
2. Ensure appropriate exception is thrown

### Files to Review
- `src/path/to/file` - Add validation
- `tests/path/to/test` - Verify test correctness
```

## State Management Commands

### Full Command Reference
```bash
# Initialize or resume workflow
python .claude/core/state.py init "Goal description"
python .claude/core/state.py init "Goal" --session SESSION_ID

# Add stories with metadata
python .claude/core/state.py add-story "Story title"
python .claude/core/state.py add-story "Story title" --size L
python .claude/core/state.py add-story "Story title" --size M --ac "First criterion"
python .claude/core/state.py add-story "Story title" --security  # For security-sensitive

# Update story status
python .claude/core/state.py update-story S1 pending
python .claude/core/state.py update-story S1 in_progress
python .claude/core/state.py update-story S1 in_progress --agent developer
python .claude/core/state.py update-story S1 completed

# Verification checks (fail-first pattern)
python .claude/core/state.py verify S1 testsPass --passed
python .claude/core/state.py verify S1 coverageMet --passed --details "85%"
python .claude/core/state.py verify S1 reviewApproved --passed
python .claude/core/state.py verify S1 securityCleared --passed

# Manage blockers
python .claude/core/state.py add-blocker "Description" --severity high
python .claude/core/state.py resolve-blocker 0

# Record decisions
python .claude/core/state.py add-decision "Title" "Choice" "Rationale"

# Checkpoint management
python .claude/core/state.py checkpoint  # Returns exit code 2 if checkpoint due
python .claude/core/state.py record-review

# Check status
python .claude/core/state.py status

# Session recovery
python .claude/core/state.py recover

# Complete workflow
python .claude/core/state.py complete
```

## Pull Request Creation (Phase 3)

After all stories are completed and verified, create a pull request:

```bash
# 1. Verify clean working state
git status

# 2. Push branch to remote
git push -u origin HEAD

# 3. Create PR using GitHub CLI
gh pr create \
  --title "[Feature] <Goal Summary>" \
  --body "$(cat <<'EOF'
## Summary
<1-2 sentence description of implementation>

## Stories Implemented
| ID | Title | Status |
|----|-------|--------|
| S1 | <title> | Completed |
| S2 | <title> | Completed |

## Changes Made
- <Key change 1>
- <Key change 2>

## Testing
- All unit tests passing
- Coverage thresholds met
- Integration tests verified

## Verification Checklist
- [x] Code review approved
- [x] Security review passed (if applicable)
- [x] All acceptance criteria met
- [x] Build passes

---
Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

### PR Creation Troubleshooting

| Issue | Solution |
|-------|----------|
| `gh: command not found` | Install GitHub CLI: https://cli.github.com/ |
| `not authenticated` | Run `gh auth login` |
| `no remote configured` | Run `git remote add origin <url>` |
| `branch doesn't exist` | Push first: `git push -u origin HEAD` |

### PR Requirements
- **Always** create a PR at workflow completion
- **Never** complete workflow without creating PR (unless user explicitly skips)
- Include all completed story IDs in description
- Link to related issues if applicable

## Quality Gates

### G1: Pre-Implementation
- [ ] Design is complete for the story
- [ ] Acceptance criteria are clear and testable
- [ ] Dependencies on other stories identified
- [ ] Required interfaces/contracts defined

### G2: Post-Implementation
- [ ] Build passes with no errors
- [ ] Tests pass with no failures
- [ ] All acceptance criteria have corresponding tests
- [ ] No warnings in new code

### G3: Coverage
Get thresholds from platform.json:

| Story Size | Coverage Target |
|------------|-----------------|
| S (Small)  | 70%             |
| M (Medium) | 80%             |
| L (Large)  | 85%             |
| XL (Extra) | 90%             |

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
   - Ambiguous reference? → Check imports/using statements
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
**Platform:** {platform_name}
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
