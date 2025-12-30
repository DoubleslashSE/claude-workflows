# Testing Patterns Reference

Load this file when writing or reviewing tests in this project.

---

## Test Organization

```
tests/
├── Doubleslash.Auctions.Core.Tests/
│   ├── Entities/
│   │   └── AuctionTests.cs
│   └── ValueObjects/
│       └── MoneyTests.cs
├── Doubleslash.Auctions.Application.Tests/
│   ├── Commands/
│   │   └── CreateAuctionCommandHandlerTests.cs
│   └── Queries/
│       └── GetAuctionDetailsQueryHandlerTests.cs
└── Doubleslash.Auctions.Api.Tests/
    └── Controllers/
        └── AuctionsControllerTests.cs
```

---

## Test Naming Convention

```
{MethodName}_{Scenario}_{ExpectedResult}
```

Examples:
- `Create_WithValidData_ReturnsNewAuction`
- `PlaceBid_WhenAuctionEnded_ThrowsInvalidOperationException`
- `GetById_WhenNotFound_ReturnsNull`

---

## Test Patterns

### Unit Test (xUnit + Moq)
```csharp
public class CreateAuctionCommandHandlerTests
{
    private readonly Mock<IAuctionRepository> _repositoryMock;
    private readonly CreateAuctionCommandHandler _handler;

    public CreateAuctionCommandHandlerTests()
    {
        _repositoryMock = new Mock<IAuctionRepository>();
        _handler = new CreateAuctionCommandHandler(_repositoryMock.Object);
    }

    [Fact]
    public async Task Handle_WithValidCommand_CreatesAuction()
    {
        // Arrange
        var command = new CreateAuctionCommand(
            SellerId: Guid.NewGuid(),
            Title: "Test Auction",
            StartingPrice: 100m,
            EndDate: DateTime.UtcNow.AddDays(7)
        );

        _repositoryMock
            .Setup(x => x.AddAsync(It.IsAny<Auction>(), It.IsAny<CancellationToken>()))
            .Returns(Task.CompletedTask);

        // Act
        var result = await _handler.Handle(command, CancellationToken.None);

        // Assert
        Assert.NotEqual(Guid.Empty, result);
        _repositoryMock.Verify(
            x => x.AddAsync(It.IsAny<Auction>(), It.IsAny<CancellationToken>()),
            Times.Once
        );
    }
}
```

### Validator Test
```csharp
public class CreateAuctionCommandValidatorTests
{
    private readonly CreateAuctionCommandValidator _validator = new();

    [Theory]
    [InlineData("")]
    [InlineData(null)]
    public void Validate_WithEmptyTitle_ReturnsError(string? title)
    {
        // Arrange
        var command = new CreateAuctionCommand(
            Guid.NewGuid(),
            title!,
            100m,
            DateTime.UtcNow.AddDays(7)
        );

        // Act
        var result = _validator.Validate(command);

        // Assert
        Assert.False(result.IsValid);
        Assert.Contains(result.Errors, e => e.PropertyName == nameof(command.Title));
    }

    [Fact]
    public void Validate_WithPastEndDate_ReturnsError()
    {
        // Arrange
        var command = new CreateAuctionCommand(
            Guid.NewGuid(),
            "Valid Title",
            100m,
            DateTime.UtcNow.AddDays(-1)
        );

        // Act
        var result = _validator.Validate(command);

        // Assert
        Assert.False(result.IsValid);
        Assert.Contains(result.Errors, e => e.PropertyName == nameof(command.EndDate));
    }
}
```

### Entity Test
```csharp
public class AuctionTests
{
    [Fact]
    public void Create_WithValidData_ReturnsAuctionInDraftStatus()
    {
        // Arrange & Act
        var auction = Auction.Create(
            Guid.NewGuid(),
            "Test Auction",
            100m,
            DateTime.UtcNow.AddDays(7)
        );

        // Assert
        Assert.NotEqual(Guid.Empty, auction.Id);
        Assert.Equal(AuctionStatus.Draft, auction.Status);
    }

    [Fact]
    public void Publish_WhenDraft_ChangesStatusToActive()
    {
        // Arrange
        var auction = Auction.Create(
            Guid.NewGuid(),
            "Test Auction",
            100m,
            DateTime.UtcNow.AddDays(7)
        );

        // Act
        auction.Publish();

        // Assert
        Assert.Equal(AuctionStatus.Active, auction.Status);
    }

    [Fact]
    public void Publish_WhenAlreadyActive_ThrowsInvalidOperationException()
    {
        // Arrange
        var auction = Auction.Create(
            Guid.NewGuid(),
            "Test Auction",
            100m,
            DateTime.UtcNow.AddDays(7)
        );
        auction.Publish();

        // Act & Assert
        Assert.Throws<InvalidOperationException>(() => auction.Publish());
    }
}
```

---

## Coverage Requirements

| Story Size | Unit Tests | Integration Tests | Coverage Target |
|------------|------------|-------------------|-----------------|
| S | 2+ | 0 | 70% |
| M | 5+ | 1+ | 80% |
| L | 10+ | 3+ | 85% |
| XL | 20+ | 5+ | 90% |

### Check Coverage
```bash
dotnet test --collect:"XPlat Code Coverage"
```

---

## Test Quality Checklist

### Before marking tests complete:
- [ ] Each acceptance criterion has a test
- [ ] Happy path tested
- [ ] Edge cases tested (null, empty, boundary values)
- [ ] Error scenarios tested
- [ ] Tests are independent (no shared state)
- [ ] Tests are readable (clear Arrange-Act-Assert)
- [ ] No test duplication

### Red Flags:
- Tests that never fail (assertions too loose)
- Tests with no assertions
- Tests that test mocks instead of behavior
- Tests that rely on execution order
- Tests that access external resources (DB, network)

---

## Running Tests

```bash
# All tests
dotnet test

# Specific project
dotnet test tests/Doubleslash.Auctions.Core.Tests

# With coverage
dotnet test --collect:"XPlat Code Coverage"

# Filter by name
dotnet test --filter "FullyQualifiedName~CreateAuction"
```
