---
name: tdd-workflow
description: Test-Driven Development workflow with xUnit, Moq, and FluentValidation testing patterns. Use when writing tests or implementing features with TDD.
---

# TDD Workflow

## The TDD Cycle

```
1. RED    → Write a failing test that defines expected behavior
2. GREEN  → Write minimum code to make the test pass
3. REFACTOR → Clean up while keeping tests green
4. COMMIT → Save working increment
```

## Test Organization

```
tests/
├── {Project}.Core.Tests/
│   └── Entities/
├── {Project}.Application.Tests/
│   ├── Commands/
│   └── Queries/
└── {Project}.Api.Tests/
    └── Controllers/
```

## Test Naming Convention

```
{MethodName}_{Scenario}_{ExpectedResult}
```

Examples:
- `Create_WithValidData_ReturnsNewAuction`
- `PlaceBid_WhenAuctionEnded_ThrowsInvalidOperationException`

## Test Patterns

### Unit Test (Arrange-Act-Assert)
```csharp
[Fact]
public async Task Handle_WithValidCommand_CreatesAuction()
{
    // Arrange
    var command = new CreateAuctionCommand(...);
    _repositoryMock.Setup(x => x.AddAsync(...)).Returns(Task.CompletedTask);

    // Act
    var result = await _handler.Handle(command, CancellationToken.None);

    // Assert
    Assert.NotEqual(Guid.Empty, result);
    _repositoryMock.Verify(x => x.AddAsync(...), Times.Once);
}
```

### Validator Test
```csharp
[Theory]
[InlineData("")]
[InlineData(null)]
public void Validate_WithEmptyTitle_ReturnsError(string? title)
{
    var command = new CreateAuctionCommand(..., title!, ...);
    var result = _validator.Validate(command);

    Assert.False(result.IsValid);
    Assert.Contains(result.Errors, e => e.PropertyName == nameof(command.Title));
}
```

## Coverage Requirements

| Size | Unit Tests | Integration Tests | Target |
|------|------------|-------------------|--------|
| S | 2+ | 0 | 70% |
| M | 5+ | 1+ | 80% |
| L | 10+ | 3+ | 85% |

## Commands

```bash
dotnet test
dotnet test --collect:"XPlat Code Coverage"
dotnet test --filter "FullyQualifiedName~CreateAuction"
```

## Test Quality Red Flags

- Tests that never fail (assertions too loose)
- Tests with no assertions
- Tests that test mocks instead of behavior
- Tests that rely on execution order

## Additional Resources

For detailed test patterns and examples, see [patterns.md](patterns.md).
