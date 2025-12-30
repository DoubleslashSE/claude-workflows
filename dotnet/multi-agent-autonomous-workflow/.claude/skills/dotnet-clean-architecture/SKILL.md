---
name: dotnet-clean-architecture
description: .NET Clean Architecture patterns with CQRS, MediatR, and FluentValidation. Use when implementing features, designing components, or reviewing code in this codebase.
---

# .NET Clean Architecture Patterns

## Architecture Layers

```
API Layer (Controllers/Endpoints)
    ↓
Application Layer (Commands, Queries, Handlers, Validators)
    ↓
Infrastructure Layer (EF Core, External Services)
    ↓
Core Layer (Entities, Value Objects, Interfaces)
```

**Dependency Rule:** Dependencies flow INWARD only. Core has no external dependencies.

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

## Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Command | `{Action}{Entity}Command` | `CreateAuctionCommand` |
| Handler | `{Action}{Entity}CommandHandler` | `CreateAuctionCommandHandler` |
| Validator | `{Action}{Entity}CommandValidator` | `CreateAuctionCommandValidator` |
| Query | `{Action}{Entity}Query` | `GetAuctionDetailsQuery` |
| Repository | `I{Entity}Repository` | `IAuctionRepository` |

## Code Patterns

### Command Example
```csharp
public record CreateAuctionCommand(
    Guid SellerId,
    string Title,
    decimal StartingPrice,
    DateTime EndDate
) : IRequest<Guid>;
```

### Entity Example
```csharp
public class Auction : Entity
{
    public Guid SellerId { get; private set; }
    public string Title { get; private set; } = string.Empty;

    private Auction() { } // EF Core

    public static Auction Create(Guid sellerId, string title, ...)
    {
        return new Auction { ... };
    }
}
```

## Anti-Patterns to Avoid

- DO NOT reference Infrastructure from Core
- DO NOT put business logic in controllers
- DO NOT bypass Application layer from API
- DO NOT use `async void` (except event handlers)
- DO NOT use `Task.Result` or `Task.Wait()`
- DO NOT create N+1 query patterns
- DO NOT forget `AsNoTracking()` for read-only queries

## Additional Resources

For detailed code examples and patterns, see [patterns.md](patterns.md).
