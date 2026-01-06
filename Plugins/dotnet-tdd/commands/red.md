---
description: RED phase - Write failing tests for a feature before implementation
---

# RED Phase - Write Failing Tests

Design and write failing tests for: **$ARGUMENTS**

## Your Task

1. **Analyze Requirements**
   - Understand the feature to be tested
   - Identify the system under test (SUT)

2. **Identify Test Scenarios**
   - Happy path scenarios
   - Edge cases
   - Error conditions
   - Boundary conditions

3. **Write Failing Tests**
   - Follow AAA pattern (Arrange-Act-Assert)
   - Use proper naming: `{Method}_{Scenario}_{Expected}`
   - One logical assertion per test

4. **Verify Tests Fail**
   - Run tests: `dotnet test`
   - Confirm they fail for the RIGHT reason

## Test Template

```csharp
[Fact]
public void MethodName_Scenario_ExpectedBehavior()
{
    // Arrange - Set up preconditions
    var sut = new SystemUnderTest();

    // Act - Execute the behavior
    var result = sut.MethodUnderTest();

    // Assert - Verify outcome
    Assert.Equal(expected, result);
}
```

## Test Categories

- **Unit Tests**: Single unit in isolation, mock dependencies
- **Integration Tests**: Component interactions
- **Edge Cases**: Boundaries, null, empty, max values

## Output Required

Provide:
1. Test class with all test methods
2. List of scenarios covered
3. Test execution output showing failures
4. Any interfaces/classes needed for implementation
