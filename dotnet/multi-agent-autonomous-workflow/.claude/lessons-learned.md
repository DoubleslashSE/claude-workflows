# Lessons Learned

This file accumulates insights from autonomous workflow sessions. After each story or workflow, add learnings to help future sessions avoid mistakes and replicate successes.

---

## How to Use This File

### For ORCHESTRATOR
Before starting a new workflow, review recent lessons for relevant insights.
When spawning agents, include relevant lessons in their context.

### For DEVELOPER
Before implementing, check for lessons related to the story type.
After completing a story, add what worked and what didn't.

### After Each Story

Add an entry using this format:

```markdown
## [Story ID]: [Story Title]
**Date:** YYYY-MM-DD
**Workflow:** [workflow-id]

### What Worked
- [Successful approach or pattern]
- [Effective technique]

### What Didn't Work
- [Approach that failed and why]
- [Anti-pattern discovered]

### Key Insight
[Single most important takeaway]

### Reusable Pattern
[If applicable, a pattern that can be reused]
```

---

## Lessons by Category

### Commands & Handlers

<!-- Add lessons about implementing CQRS commands here -->

### Validation

<!-- Add lessons about FluentValidation patterns here -->

### Entity Framework

<!-- Add lessons about EF Core patterns here -->

### Testing

<!-- Add lessons about testing patterns here -->

### Clean Architecture

<!-- Add lessons about architecture compliance here -->

### Security

<!-- Add lessons about security implementation here -->

---

## Recent Lessons

<!-- New lessons go here, most recent first -->

### Template Entry

## S0: Template Story
**Date:** 2024-01-01
**Workflow:** 00000000

### What Worked
- Following existing code patterns
- Writing tests before implementation
- Breaking story into small tasks

### What Didn't Work
- Trying to implement too much at once
- Not checking existing similar code first

### Key Insight
Always search for similar existing implementations before designing from scratch.

### Reusable Pattern
Use the Command+Handler+Validator pattern for all write operations.

---

## Patterns Extracted

### P001: CQRS Command with Validation
**Context:** Adding new domain commands
**Solution:** Command + Handler + Validator structure
**Example:** See `Application/Bids/Commands/PlaceBid/`

### P002: Repository Pattern
**Context:** Data access for entities
**Solution:** Interface in Core, implementation in Infrastructure
**Example:** See `Core/Repositories/IBidRepository.cs`

---

## Common Mistakes to Avoid

1. **Not using `AsNoTracking()` for read-only queries** - Causes unnecessary tracking overhead
2. **Catching generic Exception** - Always catch specific exceptions or re-throw
3. **Hardcoding configuration** - Use IConfiguration and appsettings
4. **Skipping validation** - Every command must have a validator
5. **N+1 queries** - Always use Include/ThenInclude for related data
6. **Async void methods** - Only use for event handlers, otherwise Task
7. **Not propagating CancellationToken** - Pass through all async calls

---

## Quality Trends

Track quality over time:

| Workflow | Stories | Avg Attempts | Coverage | Review Findings |
|----------|---------|--------------|----------|-----------------|
| <!-- Add entries here --> |

---

*Last updated: [Workflow will update this]*
