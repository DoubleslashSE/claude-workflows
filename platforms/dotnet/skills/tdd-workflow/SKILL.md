---
name: tdd-workflow
description: Test-Driven Development workflow for .NET with xUnit, FluentAssertions, and NSubstitute. Use when implementing features using TDD practices.
---

# TDD Workflow for .NET

Test-Driven Development cycle: RED → GREEN → REFACTOR

## The TDD Cycle

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                         TDD CYCLE                               │
│                                                                 │
│        ┌─────────┐                                              │
│        │   RED   │  Write a failing test                        │
│        │  (Fail) │  that defines expected behavior              │
│        └────┬────┘                                              │
│             │                                                   │
│             ▼                                                   │
│        ┌─────────┐                                              │
│        │  GREEN  │  Write minimal code                          │
│        │  (Pass) │  to make the test pass                       │
│        └────┬────┘                                              │
│             │                                                   │
│             ▼                                                   │
│        ┌──────────┐                                             │
│        │ REFACTOR │  Clean up code                              │
│        │  (Clean) │  while keeping tests green                  │
│        └────┬─────┘                                             │
│             │                                                   │
│             └──────────────▶ Repeat                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Test Project Structure

```
tests/
├── Application.Tests/           # Unit tests for handlers
│   ├── Commands/
│   │   └── CreateAuctionCommandHandlerTests.cs
│   └── Queries/
│       └── GetAuctionQueryHandlerTests.cs
│
├── Core.Tests/                  # Domain entity tests
│   ├── Entities/
│   │   └── AuctionTests.cs
│   └── ValueObjects/
│       └── MoneyTests.cs
│
└── Integration.Tests/           # Integration tests
    ├── Api/
    │   └── AuctionsControllerTests.cs
    └── Persistence/
        └── AuctionRepositoryTests.cs
```

## Test Naming Convention

Format: `{Method}_{Scenario}_{ExpectedResult}`

```csharp
// Examples:
public void PlaceBid_WhenBidHigherThanCurrent_AddsBidToAuction()
public void PlaceBid_WhenAuctionNotActive_ThrowsDomainException()
public void Create_WithValidData_ReturnsNewAuction()
public void Create_WithEmptyTitle_ThrowsDomainException()
```

## Step 1: RED - Write Failing Test First

Before writing any production code, write a test that:
- Describes the expected behavior
- Fails for the right reason
- Is specific and focused

```csharp
// tests/Core.Tests/Entities/AuctionTests.cs
public class AuctionTests
{
    [Fact]
    public void Create_WithValidData_ReturnsAuctionWithCorrectProperties()
    {
        // Arrange
        var title = "Test Auction";
        var startingPrice = Money.Create(100);
        var endsAt = DateTime.UtcNow.AddDays(7);

        // Act
        var auction = Auction.Create(title, startingPrice, endsAt);

        // Assert
        auction.Should().NotBeNull();
        auction.Title.Should().Be(title);
        auction.StartingPrice.Should().Be(startingPrice);
        auction.EndsAt.Should().Be(endsAt);
        auction.Status.Should().Be(AuctionStatus.Active);
    }

    [Fact]
    public void Create_WithEmptyTitle_ThrowsDomainException()
    {
        // Arrange
        var startingPrice = Money.Create(100);
        var endsAt = DateTime.UtcNow.AddDays(7);

        // Act
        var act = () => Auction.Create("", startingPrice, endsAt);

        // Assert
        act.Should().Throw<DomainException>()
            .WithMessage("*Title*required*");
    }

    [Fact]
    public void Create_WithPastEndDate_ThrowsDomainException()
    {
        // Arrange
        var title = "Test Auction";
        var startingPrice = Money.Create(100);
        var endsAt = DateTime.UtcNow.AddDays(-1);

        // Act
        var act = () => Auction.Create(title, startingPrice, endsAt);

        // Assert
        act.Should().Throw<DomainException>()
            .WithMessage("*End date*future*");
    }
}
```

Run the test - it should FAIL:
```bash
dotnet test --filter "FullyQualifiedName~AuctionTests"
```

## Step 2: GREEN - Write Minimal Code to Pass

Write just enough code to make the test pass:

```csharp
// src/Core/Entities/Auction.cs
public class Auction : BaseEntity
{
    public string Title { get; private set; }
    public Money StartingPrice { get; private set; }
    public DateTime EndsAt { get; private set; }
    public AuctionStatus Status { get; private set; }

    private Auction() { }

    public static Auction Create(string title, Money startingPrice, DateTime endsAt)
    {
        if (string.IsNullOrWhiteSpace(title))
            throw new DomainException("Title is required");

        if (endsAt <= DateTime.UtcNow)
            throw new DomainException("End date must be in the future");

        return new Auction
        {
            Id = Guid.NewGuid(),
            Title = title,
            StartingPrice = startingPrice,
            EndsAt = endsAt,
            Status = AuctionStatus.Active
        };
    }
}
```

Run tests again - they should PASS:
```bash
dotnet test --filter "FullyQualifiedName~AuctionTests"
```

## Step 3: REFACTOR - Clean Up

With green tests, safely refactor:
- Extract common setup to fields/methods
- Improve naming
- Remove duplication
- Improve structure

```csharp
public class AuctionTests
{
    private readonly Money _defaultStartingPrice = Money.Create(100);
    private readonly DateTime _futureDate = DateTime.UtcNow.AddDays(7);
    private readonly DateTime _pastDate = DateTime.UtcNow.AddDays(-1);

    [Fact]
    public void Create_WithValidData_ReturnsAuctionWithCorrectProperties()
    {
        var auction = CreateValidAuction();

        auction.Should().NotBeNull();
        auction.Status.Should().Be(AuctionStatus.Active);
    }

    [Theory]
    [InlineData("")]
    [InlineData("   ")]
    [InlineData(null)]
    public void Create_WithInvalidTitle_ThrowsDomainException(string invalidTitle)
    {
        var act = () => Auction.Create(invalidTitle, _defaultStartingPrice, _futureDate);

        act.Should().Throw<DomainException>();
    }

    private Auction CreateValidAuction(string title = "Test Auction")
        => Auction.Create(title, _defaultStartingPrice, _futureDate);
}
```

## Testing Command Handlers

```csharp
// tests/Application.Tests/Commands/CreateAuctionCommandHandlerTests.cs
public class CreateAuctionCommandHandlerTests
{
    private readonly IAuctionRepository _repository;
    private readonly IUnitOfWork _unitOfWork;
    private readonly CreateAuctionCommandHandler _handler;

    public CreateAuctionCommandHandlerTests()
    {
        _repository = Substitute.For<IAuctionRepository>();
        _unitOfWork = Substitute.For<IUnitOfWork>();
        _handler = new CreateAuctionCommandHandler(_repository, _unitOfWork);
    }

    [Fact]
    public async Task Handle_WithValidCommand_CreatesAuctionAndReturnsId()
    {
        // Arrange
        var command = new CreateAuctionCommand
        {
            Title = "Test Auction",
            StartingPrice = 100,
            Currency = "USD",
            EndsAt = DateTime.UtcNow.AddDays(7)
        };

        // Act
        var result = await _handler.Handle(command, CancellationToken.None);

        // Assert
        result.Should().NotBeEmpty();
        await _repository.Received(1).AddAsync(
            Arg.Is<Auction>(a => a.Title == command.Title),
            Arg.Any<CancellationToken>());
        await _unitOfWork.Received(1).SaveChangesAsync(Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task Handle_WhenRepositoryThrows_PropagatesException()
    {
        // Arrange
        var command = CreateValidCommand();
        _repository.AddAsync(Arg.Any<Auction>(), Arg.Any<CancellationToken>())
            .ThrowsAsync(new InvalidOperationException("Database error"));

        // Act
        var act = () => _handler.Handle(command, CancellationToken.None);

        // Assert
        await act.Should().ThrowAsync<InvalidOperationException>()
            .WithMessage("*Database*");
    }

    private CreateAuctionCommand CreateValidCommand() => new()
    {
        Title = "Test",
        StartingPrice = 100,
        EndsAt = DateTime.UtcNow.AddDays(7)
    };
}
```

## Testing Query Handlers

```csharp
// tests/Application.Tests/Queries/GetAuctionByIdQueryHandlerTests.cs
public class GetAuctionByIdQueryHandlerTests
{
    private readonly IAppDbContext _context;
    private readonly IMapper _mapper;
    private readonly GetAuctionByIdQueryHandler _handler;

    [Fact]
    public async Task Handle_WhenAuctionExists_ReturnsDto()
    {
        // Arrange
        var auctionId = Guid.NewGuid();
        var query = new GetAuctionByIdQuery(auctionId);

        var auction = CreateTestAuction(auctionId);
        _context.Auctions.Returns(new[] { auction }.AsQueryable().BuildMockDbSet());
        _mapper.Map<AuctionDto>(auction).Returns(new AuctionDto { Id = auctionId });

        // Act
        var result = await _handler.Handle(query, CancellationToken.None);

        // Assert
        result.Should().NotBeNull();
        result.Id.Should().Be(auctionId);
    }

    [Fact]
    public async Task Handle_WhenAuctionNotFound_ReturnsNull()
    {
        // Arrange
        var query = new GetAuctionByIdQuery(Guid.NewGuid());
        _context.Auctions.Returns(Array.Empty<Auction>().AsQueryable().BuildMockDbSet());

        // Act
        var result = await _handler.Handle(query, CancellationToken.None);

        // Assert
        result.Should().BeNull();
    }
}
```

## Integration Tests

```csharp
// tests/Integration.Tests/Api/AuctionsControllerTests.cs
public class AuctionsControllerTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly HttpClient _client;

    public AuctionsControllerTests(WebApplicationFactory<Program> factory)
    {
        _client = factory.CreateClient();
    }

    [Fact]
    public async Task Create_WithValidRequest_Returns201AndId()
    {
        // Arrange
        var request = new
        {
            Title = "Test Auction",
            StartingPrice = 100,
            Currency = "USD",
            EndsAt = DateTime.UtcNow.AddDays(7)
        };

        // Act
        var response = await _client.PostAsJsonAsync("/api/auctions", request);

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.Created);
        var id = await response.Content.ReadFromJsonAsync<Guid>();
        id.Should().NotBeEmpty();
    }

    [Fact]
    public async Task Create_WithInvalidRequest_Returns400()
    {
        // Arrange
        var request = new { Title = "", StartingPrice = -1 };

        // Act
        var response = await _client.PostAsJsonAsync("/api/auctions", request);

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.BadRequest);
    }

    [Fact]
    public async Task GetById_WhenNotFound_Returns404()
    {
        // Act
        var response = await _client.GetAsync($"/api/auctions/{Guid.NewGuid()}");

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.NotFound);
    }
}
```

## Test Utilities

### FluentAssertions Patterns

```csharp
// Basic assertions
result.Should().NotBeNull();
result.Should().Be(expected);
result.Should().BeEquivalentTo(expected);

// Collection assertions
list.Should().HaveCount(3);
list.Should().Contain(x => x.Id == expectedId);
list.Should().BeInAscendingOrder(x => x.CreatedAt);

// Exception assertions
act.Should().Throw<DomainException>()
    .WithMessage("*expected*")
    .And.InnerException.Should().BeNull();

// Async exception assertions
await act.Should().ThrowAsync<InvalidOperationException>();

// Object graph comparison
actual.Should().BeEquivalentTo(expected, options =>
    options.Excluding(x => x.Id)
           .Excluding(x => x.CreatedAt));
```

### NSubstitute Patterns

```csharp
// Create substitute
var repository = Substitute.For<IRepository>();

// Setup return value
repository.GetByIdAsync(Arg.Any<Guid>()).Returns(entity);

// Setup async return
repository.GetAllAsync().Returns(Task.FromResult(entities));

// Verify call was made
await repository.Received(1).AddAsync(Arg.Is<Entity>(e => e.Name == "test"));

// Verify call was NOT made
repository.DidNotReceive().Delete(Arg.Any<Entity>());

// Capture argument
Entity? captured = null;
await repository.AddAsync(Arg.Do<Entity>(e => captured = e));

// Throw exception
repository.GetByIdAsync(Arg.Any<Guid>())
    .ThrowsAsync(new NotFoundException());
```

## TDD Commands Reference

```bash
# Run all tests
dotnet test

# Run tests with filter
dotnet test --filter "FullyQualifiedName~AuctionTests"
dotnet test --filter "Category=Unit"

# Run specific project
dotnet test tests/Application.Tests

# Run with coverage
dotnet test /p:CollectCoverage=true /p:CoverletOutputFormat=cobertura

# Watch mode (re-run on changes)
dotnet watch test --project tests/Application.Tests

# Verbose output
dotnet test --logger "console;verbosity=detailed"
```

## Coverage Thresholds

| Story Size | Required Coverage |
|------------|-------------------|
| S (Small)  | 70%              |
| M (Medium) | 80%              |
| L (Large)  | 85%              |
| XL (Extra Large) | 90%       |

## TDD Best Practices

1. **Write the test first** - Never write production code without a failing test
2. **One assertion per test** - Keep tests focused
3. **Test behavior, not implementation** - Tests should survive refactoring
4. **Use descriptive names** - `{Method}_{Scenario}_{Expected}`
5. **Keep tests fast** - Unit tests should run in milliseconds
6. **Isolate dependencies** - Use mocks/substitutes for external dependencies
7. **Follow AAA pattern** - Arrange, Act, Assert
8. **Don't test private methods** - Test through public API
9. **Refactor only with green tests** - Never refactor with failing tests
10. **Commit after each green-refactor cycle** - Small, incremental commits
