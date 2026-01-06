---
description: GREEN phase - Write minimal code to make failing tests pass
---

# GREEN Phase - Make Tests Pass

Write minimal code to make tests pass for: **$ARGUMENTS**

## Your Task

1. **Identify Failing Tests**
   - Run `dotnet test` to see failures
   - Focus on ONE failing test at a time

2. **Write Minimal Code**
   - Implement ONLY what the test requires
   - Use the simplest possible solution
   - Hardcoding is acceptable initially

3. **Run Tests**
   - Verify the test passes
   - Ensure no other tests broke

4. **Repeat**
   - Move to next failing test
   - Continue until all tests pass

## GREEN Phase Rules

1. **MINIMAL code** - Just enough to pass
2. **No extra features** - Only what tests demand
3. **No optimization** - That's for REFACTOR
4. **Ugly is OK** - Clean up later
5. **One test at a time** - Focus

## Fake It Till You Make It

Start simple, generalize as needed:

```csharp
// Test expects specific value
Assert.Equal("Hello", greeter.GetGreeting());

// GREEN: Just return it
public string GetGreeting() => "Hello";
```

## Commands

```bash
# Run all tests
dotnet test

# Run specific test
dotnet test --filter "FullyQualifiedName~{TestName}"

# Run with output
dotnet test --verbosity normal
```

## Output Required

Provide:
1. Implementation code
2. Test execution showing all tests pass
3. Notes on simplifications made
4. Potential refactoring opportunities identified
