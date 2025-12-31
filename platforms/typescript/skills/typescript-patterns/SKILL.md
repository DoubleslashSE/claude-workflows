---
name: typescript-patterns
description: TypeScript and Next.js best practices, patterns, and conventions. Use when working with TypeScript/JavaScript projects, React applications, or Next.js apps.
---

# TypeScript Patterns

Best practices and patterns for TypeScript with Next.js App Router.

## Project Structure

```
src/
├── app/                    # Next.js App Router
│   ├── (routes)/          # Route groups
│   ├── api/               # API routes
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Home page
├── components/            # React components
│   ├── ui/               # Base UI components
│   └── features/         # Feature-specific components
├── hooks/                 # Custom React hooks
├── services/              # API clients and business logic
├── types/                 # TypeScript type definitions
├── utils/                 # Utility functions
└── lib/                   # Third-party library configurations
```

## Type Safety Patterns

### Strict Type Checking
```typescript
// tsconfig.json strict mode is enabled
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitAny": true
  }
}
```

### Avoid 'any' - Use Proper Types
```typescript
// BAD
function processData(data: any) { ... }

// GOOD
interface UserData {
  id: string;
  name: string;
  email: string;
}
function processData(data: UserData) { ... }

// For unknown data, use 'unknown' and type guards
function processUnknown(data: unknown) {
  if (isUserData(data)) {
    // Now TypeScript knows data is UserData
  }
}
```

### Type Guards
```typescript
function isUserData(data: unknown): data is UserData {
  return (
    typeof data === 'object' &&
    data !== null &&
    'id' in data &&
    'name' in data
  );
}
```

## React Patterns

### Component Structure
```typescript
// components/UserCard/UserCard.tsx
interface UserCardProps {
  user: User;
  onSelect?: (user: User) => void;
  className?: string;
}

export function UserCard({ user, onSelect, className }: UserCardProps) {
  const handleClick = () => onSelect?.(user);

  return (
    <div className={cn('card', className)} onClick={handleClick}>
      <h3>{user.name}</h3>
      <p>{user.email}</p>
    </div>
  );
}
```

### Custom Hooks
```typescript
// hooks/useUser.ts
interface UseUserReturn {
  user: User | null;
  isLoading: boolean;
  error: Error | null;
  refetch: () => Promise<void>;
}

export function useUser(userId: string): UseUserReturn {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchUser = useCallback(async () => {
    setIsLoading(true);
    try {
      const data = await userService.getById(userId);
      setUser(data);
      setError(null);
    } catch (e) {
      setError(e instanceof Error ? e : new Error('Unknown error'));
    } finally {
      setIsLoading(false);
    }
  }, [userId]);

  useEffect(() => {
    fetchUser();
  }, [fetchUser]);

  return { user, isLoading, error, refetch: fetchUser };
}
```

### Server Components (App Router)
```typescript
// app/users/page.tsx (Server Component by default)
async function UsersPage() {
  const users = await getUsers(); // Runs on server

  return (
    <div>
      {users.map(user => (
        <UserCard key={user.id} user={user} />
      ))}
    </div>
  );
}
```

### Client Components
```typescript
// components/SearchBar.tsx
'use client';

import { useState } from 'react';

export function SearchBar({ onSearch }: { onSearch: (query: string) => void }) {
  const [query, setQuery] = useState('');

  return (
    <input
      value={query}
      onChange={(e) => setQuery(e.target.value)}
      onKeyDown={(e) => e.key === 'Enter' && onSearch(query)}
    />
  );
}
```

## API Route Patterns

### Route Handlers
```typescript
// app/api/users/[id]/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const user = await userService.getById(params.id);
    if (!user) {
      return NextResponse.json({ error: 'Not found' }, { status: 404 });
    }
    return NextResponse.json(user);
  } catch (error) {
    return NextResponse.json({ error: 'Internal error' }, { status: 500 });
  }
}
```

### Input Validation with Zod
```typescript
import { z } from 'zod';

const CreateUserSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
  role: z.enum(['admin', 'user']).default('user'),
});

export async function POST(request: NextRequest) {
  const body = await request.json();
  const result = CreateUserSchema.safeParse(body);

  if (!result.success) {
    return NextResponse.json(
      { error: 'Validation failed', details: result.error.flatten() },
      { status: 400 }
    );
  }

  const user = await userService.create(result.data);
  return NextResponse.json(user, { status: 201 });
}
```

## State Management

### React Query for Server State
```typescript
// hooks/useUsers.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

export function useUsers() {
  return useQuery({
    queryKey: ['users'],
    queryFn: () => userService.getAll(),
  });
}

export function useCreateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: userService.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
  });
}
```

### Zustand for Client State
```typescript
// store/useAppStore.ts
import { create } from 'zustand';

interface AppState {
  theme: 'light' | 'dark';
  sidebarOpen: boolean;
  toggleTheme: () => void;
  toggleSidebar: () => void;
}

export const useAppStore = create<AppState>((set) => ({
  theme: 'light',
  sidebarOpen: true,
  toggleTheme: () => set((state) => ({
    theme: state.theme === 'light' ? 'dark' : 'light'
  })),
  toggleSidebar: () => set((state) => ({
    sidebarOpen: !state.sidebarOpen
  })),
}));
```

## Testing Patterns

### Component Tests
```typescript
// components/UserCard/UserCard.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { UserCard } from './UserCard';

describe('UserCard', () => {
  const mockUser = { id: '1', name: 'John', email: 'john@example.com' };

  it('should render user information', () => {
    render(<UserCard user={mockUser} />);

    expect(screen.getByText('John')).toBeInTheDocument();
    expect(screen.getByText('john@example.com')).toBeInTheDocument();
  });

  it('should call onSelect when clicked', () => {
    const onSelect = jest.fn();
    render(<UserCard user={mockUser} onSelect={onSelect} />);

    fireEvent.click(screen.getByText('John'));

    expect(onSelect).toHaveBeenCalledWith(mockUser);
  });
});
```

### Hook Tests
```typescript
// hooks/useUser.test.ts
import { renderHook, waitFor } from '@testing-library/react';
import { useUser } from './useUser';

jest.mock('../services/userService');

describe('useUser', () => {
  it('should fetch and return user', async () => {
    const mockUser = { id: '1', name: 'John' };
    (userService.getById as jest.Mock).mockResolvedValue(mockUser);

    const { result } = renderHook(() => useUser('1'));

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    expect(result.current.user).toEqual(mockUser);
    expect(result.current.error).toBeNull();
  });
});
```

## Anti-Patterns to Avoid

### Don't Use 'any'
```typescript
// BAD
const data: any = await fetch('/api/users');

// GOOD
const data: User[] = await fetch('/api/users').then(r => r.json());
```

### Don't Mutate State Directly
```typescript
// BAD
state.items.push(newItem);

// GOOD
setState(prev => ({ ...prev, items: [...prev.items, newItem] }));
```

### Don't Use useEffect for Derived State
```typescript
// BAD
const [items, setItems] = useState([]);
const [filteredItems, setFilteredItems] = useState([]);
useEffect(() => {
  setFilteredItems(items.filter(i => i.active));
}, [items]);

// GOOD
const [items, setItems] = useState([]);
const filteredItems = useMemo(() => items.filter(i => i.active), [items]);
```

### Don't Forget Error Boundaries
```typescript
// app/error.tsx
'use client';

export default function Error({
  error,
  reset,
}: {
  error: Error;
  reset: () => void;
}) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={reset}>Try again</button>
    </div>
  );
}
```
