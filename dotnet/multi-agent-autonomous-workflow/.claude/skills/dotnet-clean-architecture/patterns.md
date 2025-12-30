# .NET Clean Architecture Patterns Reference

Load this file when implementing or reviewing .NET code in this project.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                        API Layer                        │
│  (ASP.NET Core Controllers/Endpoints)                   │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                   Application Layer                      │
│  (Commands, Queries, Handlers, Validators)              │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                   Infrastructure Layer                   │
│  (EF Core, External Services, Repositories)             │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                      Core Layer                          │
│  (Entities, Value Objects, Interfaces, Domain Logic)    │
└─────────────────────────────────────────────────────────┘
```

**Dependency Rule:** Dependencies flow INWARD only. Core has no external dependencies.

---

## File Organization

### Commands
```
Application/{Feature}/Commands/{Action}/
├── {Action}{Entity}Command.cs
├── {Action}{Entity}CommandHandler.cs
└── {Action}{Entity}CommandValidator.cs
```

### Queries
```
Application/{Feature}/Queries/{Action}/
├── {Action}{Entity}Query.cs
├── {Action}{Entity}QueryHandler.cs
└── {Action}{Entity}QueryResult.cs
```

### Entities
```
Core/Entities/
├── {Entity}.cs              # Domain entity
└── {Entity}Extensions.cs    # Extension methods (if needed)
```

---

## Code Patterns

### Command Pattern
```csharp
// Command.cs
public record CreateAuctionCommand(
    Guid SellerId,
    string Title,
    decimal StartingPrice,
    DateTime EndDate
) : IRequest<Guid>;

// CommandHandler.cs
public class CreateAuctionCommandHandler : IRequestHandler<CreateAuctionCommand, Guid>
{
    private readonly IAuctionRepository _repository;

    public CreateAuctionCommandHandler(IAuctionRepository repository)
    {
        _repository = repository;
    }

    public async Task<Guid> Handle(CreateAuctionCommand request, CancellationToken ct)
    {
        var auction = Auction.Create(
            request.SellerId,
            request.Title,
            request.StartingPrice,
            request.EndDate
        );

        await _repository.AddAsync(auction, ct);
        return auction.Id;
    }
}

// CommandValidator.cs
public class CreateAuctionCommandValidator : AbstractValidator<CreateAuctionCommand>
{
    public CreateAuctionCommandValidator()
    {
        RuleFor(x => x.Title)
            .NotEmpty()
            .MaximumLength(200);

        RuleFor(x => x.StartingPrice)
            .GreaterThan(0);

        RuleFor(x => x.EndDate)
            .GreaterThan(DateTime.UtcNow);
    }
}
```

### Entity Pattern
```csharp
public class Auction : Entity
{
    public Guid SellerId { get; private set; }
    public string Title { get; private set; } = string.Empty;
    public decimal StartingPrice { get; private set; }
    public DateTime EndDate { get; private set; }
    public AuctionStatus Status { get; private set; }

    private Auction() { } // EF Core

    public static Auction Create(Guid sellerId, string title, decimal startingPrice, DateTime endDate)
    {
        return new Auction
        {
            Id = Guid.NewGuid(),
            SellerId = sellerId,
            Title = title,
            StartingPrice = startingPrice,
            EndDate = endDate,
            Status = AuctionStatus.Draft
        };
    }

    public void Publish()
    {
        if (Status != AuctionStatus.Draft)
            throw new InvalidOperationException("Only draft auctions can be published");

        Status = AuctionStatus.Active;
    }
}
```

### Repository Interface (Core)
```csharp
// In Core/Repositories/
public interface IAuctionRepository
{
    Task<Auction?> GetByIdAsync(Guid id, CancellationToken ct = default);
    Task<IReadOnlyList<Auction>> GetActiveAsync(CancellationToken ct = default);
    Task AddAsync(Auction auction, CancellationToken ct = default);
    Task UpdateAsync(Auction auction, CancellationToken ct = default);
}
```

---

## Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Command | `{Action}{Entity}Command` | `CreateAuctionCommand` |
| Handler | `{Action}{Entity}CommandHandler` | `CreateAuctionCommandHandler` |
| Validator | `{Action}{Entity}CommandValidator` | `CreateAuctionCommandValidator` |
| Query | `{Action}{Entity}Query` | `GetAuctionDetailsQuery` |
| Repository | `I{Entity}Repository` | `IAuctionRepository` |
| Entity | `{Entity}` | `Auction`, `Bid`, `User` |

---

## Anti-Patterns to Avoid

### Layer Violations
- DO NOT reference Infrastructure from Core
- DO NOT reference Infrastructure from Application (except via interfaces)
- DO NOT put business logic in controllers
- DO NOT bypass Application layer from API

### Code Smells
- DO NOT catch generic `Exception` without re-throwing
- DO NOT use string concatenation for SQL
- DO NOT hardcode configuration values
- DO NOT create circular dependencies

### .NET Async Pitfalls
- DO NOT use `async void` (except event handlers)
- DO NOT use `Task.Result` or `Task.Wait()` (deadlock risk)
- DO NOT forget `CancellationToken` propagation
- DO NOT forget `ConfigureAwait(false)` in library code

### Entity Framework
- DO NOT create N+1 patterns (use `Include`/`ThenInclude`)
- DO NOT forget `AsNoTracking()` for read-only queries
- DO NOT modify tracked entities after `SaveChanges` without reloading
