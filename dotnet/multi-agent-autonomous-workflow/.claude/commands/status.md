---
description: Check the current workflow status and progress
allowed-tools: Read, Bash
---

# Workflow Status

Check the current status of the multi-agent workflow.

## Status Check

1. Read workflow state: `.claude/workflow-state.json`
2. Show progress summary:
   - Stories completed vs total
   - Current story in progress
   - Any blockers or issues

3. Run quick health checks:
   ```bash
   dotnet build --nologo -v q
   dotnet test --nologo -v q --no-build
   ```

## Report Format

```markdown
## Workflow Status

**Progress:** X/Y stories complete (Z%)
**Current:** [Story in progress or "None"]

### Completed Stories
- [x] Story 1
- [x] Story 2

### Remaining Stories
- [ ] Story 3
- [ ] Story 4

### Build Status
- Build: PASS/FAIL
- Tests: X passing, Y failing

### Blockers
- [Any issues or blockers]
```

Generate the status report now.
