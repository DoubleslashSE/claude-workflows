---
name: typescript-best-practices
description: TypeScript development best practices including SOLID, KISS, YAGNI, DRY principles, design patterns, and anti-patterns to avoid.
---

# TypeScript Best Practices

Fundamental principles and patterns for writing maintainable, scalable, and clean TypeScript code.

## Core Principles

```
┌─────────────────────────────────────────────────────────────────┐
│                     GUIDING PRINCIPLES                          │
│                                                                 │
│   SOLID ─── Foundation for object-oriented design               │
│   DRY   ─── Don't Repeat Yourself                               │
│   KISS  ─── Keep It Simple, Stupid                              │
│   YAGNI ─── You Aren't Gonna Need It                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## SOLID Principles

### S - Single Responsibility Principle

A module/class should have only one reason to change.

```typescript
// BAD - Multiple responsibilities
class UserService {
  createUser(user: User): void { /* ... */ }
  sendWelcomeEmail(user: User): void { /* ... */ }
  generateReport(user: User): void { /* ... */ }
  validatePassword(password: string): boolean { /* ... */ }
  hashPassword(password: string): string { /* ... */ }
}

// GOOD - Single responsibility per module
// services/userService.ts
export class UserService {
  constructor(
    private readonly userRepository: UserRepository,
    private readonly emailService: EmailService
  ) {}

  async createUser(request: CreateUserRequest): Promise<User> {
    const user = User.create(request.email, request.name);
    await this.userRepository.save(user);
    await this.emailService.sendWelcomeEmail(user);
    return user;
  }
}

// services/emailService.ts
export class EmailService {
  async sendWelcomeEmail(user: User): Promise<void> { /* ... */ }
}

// services/passwordService.ts
export class PasswordService {
  validate(password: string): ValidationResult { /* ... */ }
  hash(password: string): Promise<string> { /* ... */ }
}
```

### O - Open/Closed Principle

Software entities should be open for extension, but closed for modification.

```typescript
// BAD - Must modify function to add new payment types
function processPayment(payment: Payment): PaymentResult {
  switch (payment.type) {
    case 'credit_card':
      return processCreditCard(payment);
    case 'paypal':
      return processPayPal(payment);
    case 'bank_transfer':
      return processBankTransfer(payment);
    // Must add new cases here...
    default:
      throw new Error(`Unknown payment type: ${payment.type}`);
  }
}

// GOOD - Open for extension via new implementations
interface PaymentProcessor {
  readonly type: string;
  process(payment: Payment): Promise<PaymentResult>;
}

class CreditCardProcessor implements PaymentProcessor {
  readonly type = 'credit_card';

  async process(payment: Payment): Promise<PaymentResult> {
    // Process credit card
    return { success: true, transactionId: '...' };
  }
}

class PayPalProcessor implements PaymentProcessor {
  readonly type = 'paypal';

  async process(payment: Payment): Promise<PaymentResult> {
    // Process PayPal
    return { success: true, transactionId: '...' };
  }
}

// New processors added without modifying existing code
class CryptoProcessor implements PaymentProcessor {
  readonly type = 'crypto';

  async process(payment: Payment): Promise<PaymentResult> {
    return { success: true, transactionId: '...' };
  }
}

// Payment service uses processors
class PaymentService {
  private processors: Map<string, PaymentProcessor>;

  constructor(processors: PaymentProcessor[]) {
    this.processors = new Map(processors.map(p => [p.type, p]));
  }

  async process(payment: Payment): Promise<PaymentResult> {
    const processor = this.processors.get(payment.type);
    if (!processor) {
      throw new Error(`Unsupported payment type: ${payment.type}`);
    }
    return processor.process(payment);
  }
}
```

### L - Liskov Substitution Principle

Subtypes must be substitutable for their base types.

```typescript
// BAD - Square breaks Rectangle behavior
class Rectangle {
  constructor(protected width: number, protected height: number) {}

  setWidth(width: number): void {
    this.width = width;
  }

  setHeight(height: number): void {
    this.height = height;
  }

  getArea(): number {
    return this.width * this.height;
  }
}

class Square extends Rectangle {
  setWidth(width: number): void {
    this.width = width;
    this.height = width; // Breaks LSP
  }

  setHeight(height: number): void {
    this.width = height;
    this.height = height; // Breaks LSP
  }
}

// This breaks LSP:
const rect: Rectangle = new Square(5, 5);
rect.setWidth(10);
rect.setHeight(5);
// Expected: 50, Actual: 25

// GOOD - Separate abstractions
interface Shape {
  getArea(): number;
}

class Rectangle implements Shape {
  constructor(
    private readonly width: number,
    private readonly height: number
  ) {}

  getArea(): number {
    return this.width * this.height;
  }
}

class Square implements Shape {
  constructor(private readonly side: number) {}

  getArea(): number {
    return this.side * this.side;
  }
}
```

### I - Interface Segregation Principle

Clients should not be forced to depend on interfaces they don't use.

```typescript
// BAD - Fat interface
interface Worker {
  work(): void;
  eat(): void;
  sleep(): void;
  attendMeeting(): void;
  writeCode(): void;
  reviewCode(): void;
}

class Robot implements Worker {
  work(): void { /* ... */ }
  eat(): void { throw new Error('Robots do not eat'); }
  sleep(): void { throw new Error('Robots do not sleep'); }
  attendMeeting(): void { throw new Error('Robots do not attend meetings'); }
  writeCode(): void { /* ... */ }
  reviewCode(): void { throw new Error('Robots do not review code'); }
}

// GOOD - Segregated interfaces
interface Workable {
  work(): void;
}

interface Feedable {
  eat(): void;
}

interface Restable {
  sleep(): void;
}

interface Developer {
  writeCode(): void;
  reviewCode(): void;
}

class Human implements Workable, Feedable, Restable, Developer {
  work(): void { /* ... */ }
  eat(): void { /* ... */ }
  sleep(): void { /* ... */ }
  writeCode(): void { /* ... */ }
  reviewCode(): void { /* ... */ }
}

class Robot implements Workable {
  work(): void { /* ... */ }
}

class CodingBot implements Workable, Pick<Developer, 'writeCode'> {
  work(): void { /* ... */ }
  writeCode(): void { /* ... */ }
}
```

### D - Dependency Inversion Principle

High-level modules should not depend on low-level modules. Both should depend on abstractions.

```typescript
// BAD - High-level depends on low-level
import { PostgresDatabase } from './postgres';
import { SendGridEmailer } from './sendgrid';

class OrderService {
  private database = new PostgresDatabase();
  private emailer = new SendGridEmailer();

  async processOrder(order: Order): Promise<void> {
    await this.database.save(order);
    await this.emailer.send(order.customerEmail, 'Order confirmed');
  }
}

// GOOD - Both depend on abstractions
interface OrderRepository {
  save(order: Order): Promise<void>;
}

interface EmailSender {
  send(to: string, message: string): Promise<void>;
}

class OrderService {
  constructor(
    private readonly repository: OrderRepository,
    private readonly emailSender: EmailSender
  ) {}

  async processOrder(order: Order): Promise<void> {
    await this.repository.save(order);
    await this.emailSender.send(order.customerEmail, 'Order confirmed');
  }
}

// Implementations
class PostgresOrderRepository implements OrderRepository {
  async save(order: Order): Promise<void> { /* ... */ }
}

class SendGridEmailSender implements EmailSender {
  async send(to: string, message: string): Promise<void> { /* ... */ }
}

// Dependency injection
const orderService = new OrderService(
  new PostgresOrderRepository(),
  new SendGridEmailSender()
);
```

---

## DRY - Don't Repeat Yourself

Every piece of knowledge should have a single, unambiguous representation.

```typescript
// BAD - Repeated validation logic
function createUser(data: UserData): User {
  if (!data.email || !data.email.includes('@')) {
    throw new Error('Invalid email');
  }
  // ...
}

function updateUser(data: UserData): User {
  if (!data.email || !data.email.includes('@')) {
    throw new Error('Invalid email');
  }
  // ...
}

// GOOD - Single source of truth
const emailSchema = z.string().email('Invalid email format');

const createUserSchema = z.object({
  email: emailSchema,
  name: z.string().min(1, 'Name is required'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});

const updateUserSchema = z.object({
  email: emailSchema.optional(),
  name: z.string().min(1).optional(),
});

function createUser(data: unknown): User {
  const validated = createUserSchema.parse(data);
  // ...
}

function updateUser(data: unknown): User {
  const validated = updateUserSchema.parse(data);
  // ...
}
```

---

## KISS - Keep It Simple, Stupid

Prefer simple solutions over complex ones.

```typescript
// BAD - Over-engineered
class StringReverserFactory {
  create(): StringReverser {
    return new StringReverser(new CharacterIterator());
  }
}

class CharacterIterator {
  *iterate(str: string): Generator<string> {
    for (let i = str.length - 1; i >= 0; i--) {
      yield str[i];
    }
  }
}

class StringReverser {
  constructor(private iterator: CharacterIterator) {}

  reverse(input: string): string {
    return [...this.iterator.iterate(input)].join('');
  }
}

// GOOD - Simple and clear
function reverseString(input: string): string {
  return input.split('').reverse().join('');
}

// Or even simpler with spread
const reverseString = (s: string) => [...s].reverse().join('');
```

---

## YAGNI - You Aren't Gonna Need It

Don't add functionality until it's necessary.

```typescript
// BAD - Building for hypothetical requirements
interface UserServiceConfig {
  enableCaching?: boolean;
  cacheStrategy?: 'lru' | 'fifo' | 'ttl';
  cacheTtl?: number;
  enableAnalytics?: boolean;
  analyticsProvider?: 'mixpanel' | 'amplitude' | 'custom';
  enableAuditLog?: boolean;
  auditLogLevel?: 'basic' | 'detailed' | 'paranoid';
  retryStrategy?: RetryConfig;
  circuitBreaker?: CircuitBreakerConfig;
}

class UserService {
  constructor(
    private repository: UserRepository,
    private cache?: CacheService,
    private analytics?: AnalyticsService,
    private auditLog?: AuditLogService,
    private config?: UserServiceConfig
  ) {}

  async getUser(id: string): Promise<User | null> {
    // 50 lines of caching, analytics, audit logging...
    // When all you need is:
    return this.repository.findById(id);
  }
}

// GOOD - Only what's needed now
class UserService {
  constructor(private readonly repository: UserRepository) {}

  async getUser(id: string): Promise<User | null> {
    return this.repository.findById(id);
  }
}

// Add caching WHEN you have performance issues
// Add analytics WHEN you have analytics requirements
```

---

## Design Patterns

### Strategy Pattern

Encapsulate algorithms and make them interchangeable.

```typescript
// Define strategy interface
interface CompressionStrategy {
  compress(data: Buffer): Promise<Buffer>;
  decompress(data: Buffer): Promise<Buffer>;
}

// Concrete strategies
class GzipCompression implements CompressionStrategy {
  async compress(data: Buffer): Promise<Buffer> {
    return zlib.gzipSync(data);
  }

  async decompress(data: Buffer): Promise<Buffer> {
    return zlib.gunzipSync(data);
  }
}

class BrotliCompression implements CompressionStrategy {
  async compress(data: Buffer): Promise<Buffer> {
    return zlib.brotliCompressSync(data);
  }

  async decompress(data: Buffer): Promise<Buffer> {
    return zlib.brotliDecompressSync(data);
  }
}

class NoCompression implements CompressionStrategy {
  async compress(data: Buffer): Promise<Buffer> {
    return data;
  }

  async decompress(data: Buffer): Promise<Buffer> {
    return data;
  }
}

// Context
class FileStorage {
  constructor(private compression: CompressionStrategy) {}

  async save(filename: string, data: Buffer): Promise<void> {
    const compressed = await this.compression.compress(data);
    await fs.writeFile(filename, compressed);
  }

  async load(filename: string): Promise<Buffer> {
    const compressed = await fs.readFile(filename);
    return this.compression.decompress(compressed);
  }

  // Change strategy at runtime
  setCompression(strategy: CompressionStrategy): void {
    this.compression = strategy;
  }
}
```

### Factory Pattern

Encapsulate object creation logic.

```typescript
// Simple Factory
type LogLevel = 'debug' | 'info' | 'warn' | 'error';

interface Logger {
  log(message: string): void;
}

class ConsoleLogger implements Logger {
  constructor(private level: LogLevel) {}
  log(message: string): void {
    console.log(`[${this.level.toUpperCase()}] ${message}`);
  }
}

class FileLogger implements Logger {
  constructor(private filepath: string) {}
  log(message: string): void {
    fs.appendFileSync(this.filepath, `${message}\n`);
  }
}

class CloudLogger implements Logger {
  constructor(private endpoint: string) {}
  log(message: string): void {
    // Send to cloud logging service
  }
}

// Factory
class LoggerFactory {
  static create(type: 'console' | 'file' | 'cloud', config?: unknown): Logger {
    switch (type) {
      case 'console':
        return new ConsoleLogger((config as { level: LogLevel })?.level ?? 'info');
      case 'file':
        return new FileLogger((config as { path: string }).path);
      case 'cloud':
        return new CloudLogger((config as { endpoint: string }).endpoint);
      default:
        throw new Error(`Unknown logger type: ${type}`);
    }
  }
}

// Usage
const logger = LoggerFactory.create('console', { level: 'debug' });

// Abstract Factory with generics
interface UIComponent {
  render(): string;
}

interface UIFactory<T extends UIComponent> {
  create(props: Record<string, unknown>): T;
}

class ButtonFactory implements UIFactory<Button> {
  create(props: { label: string; onClick: () => void }): Button {
    return new Button(props.label, props.onClick);
  }
}
```

### Repository Pattern

Abstract data access logic.

```typescript
// Generic repository interface
interface Repository<T, ID = string> {
  findById(id: ID): Promise<T | null>;
  findAll(): Promise<T[]>;
  save(entity: T): Promise<T>;
  delete(id: ID): Promise<void>;
}

// Specification pattern for complex queries
interface Specification<T> {
  isSatisfiedBy(entity: T): boolean;
  toQuery(): Record<string, unknown>;
}

class ActiveUsersSpec implements Specification<User> {
  isSatisfiedBy(user: User): boolean {
    return user.isActive && !user.isDeleted;
  }

  toQuery(): Record<string, unknown> {
    return { isActive: true, isDeleted: false };
  }
}

class UserRepository implements Repository<User> {
  constructor(private prisma: PrismaClient) {}

  async findById(id: string): Promise<User | null> {
    return this.prisma.user.findUnique({ where: { id } });
  }

  async findAll(): Promise<User[]> {
    return this.prisma.user.findMany();
  }

  async findBySpec(spec: Specification<User>): Promise<User[]> {
    return this.prisma.user.findMany({ where: spec.toQuery() });
  }

  async save(user: User): Promise<User> {
    return this.prisma.user.upsert({
      where: { id: user.id },
      create: user,
      update: user,
    });
  }

  async delete(id: string): Promise<void> {
    await this.prisma.user.delete({ where: { id } });
  }
}

// Usage
const activeUsers = await userRepository.findBySpec(new ActiveUsersSpec());
```

### Builder Pattern

Construct complex objects step by step.

```typescript
interface EmailMessage {
  from: string;
  to: string[];
  cc: string[];
  bcc: string[];
  subject: string;
  body: string;
  isHtml: boolean;
  attachments: Attachment[];
}

class EmailBuilder {
  private email: Partial<EmailMessage> = {
    to: [],
    cc: [],
    bcc: [],
    attachments: [],
    isHtml: false,
  };

  from(address: string): this {
    this.email.from = address;
    return this;
  }

  to(address: string | string[]): this {
    const addresses = Array.isArray(address) ? address : [address];
    this.email.to!.push(...addresses);
    return this;
  }

  cc(address: string): this {
    this.email.cc!.push(address);
    return this;
  }

  bcc(address: string): this {
    this.email.bcc!.push(address);
    return this;
  }

  subject(subject: string): this {
    this.email.subject = subject;
    return this;
  }

  body(content: string, isHtml = false): this {
    this.email.body = content;
    this.email.isHtml = isHtml;
    return this;
  }

  htmlBody(content: string): this {
    return this.body(content, true);
  }

  attach(attachment: Attachment): this {
    this.email.attachments!.push(attachment);
    return this;
  }

  build(): EmailMessage {
    if (!this.email.from) {
      throw new Error('From address is required');
    }
    if (!this.email.to?.length) {
      throw new Error('At least one recipient is required');
    }
    if (!this.email.subject) {
      throw new Error('Subject is required');
    }

    return this.email as EmailMessage;
  }
}

// Usage
const email = new EmailBuilder()
  .from('noreply@example.com')
  .to(['user1@example.com', 'user2@example.com'])
  .cc('manager@example.com')
  .subject('Weekly Report')
  .htmlBody('<h1>Report</h1><p>See attached.</p>')
  .attach({ name: 'report.pdf', content: pdfBuffer })
  .build();
```

### Decorator Pattern

Add behavior to objects dynamically.

```typescript
// Function decorator pattern (common in TypeScript)
interface ApiClient {
  fetch<T>(url: string): Promise<T>;
}

class BaseApiClient implements ApiClient {
  async fetch<T>(url: string): Promise<T> {
    const response = await fetch(url);
    return response.json();
  }
}

// Decorators as wrapper functions
function withLogging(client: ApiClient): ApiClient {
  return {
    async fetch<T>(url: string): Promise<T> {
      console.log(`Fetching: ${url}`);
      const start = Date.now();
      try {
        const result = await client.fetch<T>(url);
        console.log(`Fetched ${url} in ${Date.now() - start}ms`);
        return result;
      } catch (error) {
        console.error(`Failed to fetch ${url}:`, error);
        throw error;
      }
    },
  };
}

function withRetry(client: ApiClient, maxRetries = 3): ApiClient {
  return {
    async fetch<T>(url: string): Promise<T> {
      let lastError: Error | undefined;

      for (let i = 0; i < maxRetries; i++) {
        try {
          return await client.fetch<T>(url);
        } catch (error) {
          lastError = error as Error;
          await new Promise(r => setTimeout(r, Math.pow(2, i) * 1000));
        }
      }

      throw lastError;
    },
  };
}

function withCache(client: ApiClient, ttl = 60000): ApiClient {
  const cache = new Map<string, { data: unknown; expires: number }>();

  return {
    async fetch<T>(url: string): Promise<T> {
      const cached = cache.get(url);
      if (cached && cached.expires > Date.now()) {
        return cached.data as T;
      }

      const data = await client.fetch<T>(url);
      cache.set(url, { data, expires: Date.now() + ttl });
      return data;
    },
  };
}

// Compose decorators
const client = withLogging(
  withRetry(
    withCache(new BaseApiClient())
  )
);

// TypeScript decorators (experimental)
function Log(target: any, propertyKey: string, descriptor: PropertyDescriptor) {
  const original = descriptor.value;

  descriptor.value = async function (...args: unknown[]) {
    console.log(`Calling ${propertyKey} with:`, args);
    const result = await original.apply(this, args);
    console.log(`${propertyKey} returned:`, result);
    return result;
  };

  return descriptor;
}

class UserService {
  @Log
  async getUser(id: string): Promise<User> {
    // ...
  }
}
```

### Observer Pattern (Events)

Define a subscription mechanism for notifications.

```typescript
// Type-safe event emitter
type EventMap = {
  userCreated: { user: User };
  orderPlaced: { order: Order; user: User };
  paymentReceived: { amount: number; orderId: string };
};

type EventHandler<T> = (data: T) => void | Promise<void>;

class TypedEventEmitter<Events extends Record<string, unknown>> {
  private handlers = new Map<keyof Events, Set<EventHandler<unknown>>>();

  on<K extends keyof Events>(event: K, handler: EventHandler<Events[K]>): () => void {
    if (!this.handlers.has(event)) {
      this.handlers.set(event, new Set());
    }
    this.handlers.get(event)!.add(handler as EventHandler<unknown>);

    // Return unsubscribe function
    return () => {
      this.handlers.get(event)?.delete(handler as EventHandler<unknown>);
    };
  }

  async emit<K extends keyof Events>(event: K, data: Events[K]): Promise<void> {
    const handlers = this.handlers.get(event);
    if (!handlers) return;

    await Promise.all(
      [...handlers].map(handler => handler(data))
    );
  }
}

// Usage
const events = new TypedEventEmitter<EventMap>();

// Type-safe subscriptions
events.on('userCreated', async ({ user }) => {
  await sendWelcomeEmail(user);
});

events.on('orderPlaced', async ({ order, user }) => {
  await updateInventory(order);
  await notifyUser(user, order);
});

// Type-safe emit
await events.emit('userCreated', { user: newUser });
await events.emit('orderPlaced', { order, user }); // Type error if wrong shape
```

---

## Anti-Patterns to Avoid

### Any Type Abuse

```typescript
// BAD - Using any everywhere
function processData(data: any): any {
  return data.map((item: any) => item.value);
}

const result: any = processData(someData);

// GOOD - Proper typing
interface DataItem {
  id: string;
  value: number;
}

function processData(data: DataItem[]): number[] {
  return data.map(item => item.value);
}

// When type is truly unknown
function processUnknown(data: unknown): number[] {
  if (!Array.isArray(data)) {
    throw new Error('Expected array');
  }

  return data.map(item => {
    if (typeof item !== 'object' || item === null || !('value' in item)) {
      throw new Error('Invalid item shape');
    }
    return (item as { value: number }).value;
  });
}

// Or use Zod for runtime validation
const dataSchema = z.array(z.object({
  id: z.string(),
  value: z.number(),
}));

function processDataSafe(data: unknown): number[] {
  const validated = dataSchema.parse(data);
  return validated.map(item => item.value);
}
```

### Callback Hell

```typescript
// BAD - Nested callbacks
function processOrder(orderId: string, callback: (error: Error | null, result?: string) => void) {
  getOrder(orderId, (err, order) => {
    if (err) return callback(err);
    validateOrder(order, (err, isValid) => {
      if (err) return callback(err);
      if (!isValid) return callback(new Error('Invalid order'));
      processPayment(order, (err, payment) => {
        if (err) return callback(err);
        updateInventory(order, (err) => {
          if (err) return callback(err);
          sendConfirmation(order, (err) => {
            if (err) return callback(err);
            callback(null, 'Order processed');
          });
        });
      });
    });
  });
}

// GOOD - Async/await
async function processOrder(orderId: string): Promise<string> {
  const order = await getOrder(orderId);

  const isValid = await validateOrder(order);
  if (!isValid) {
    throw new Error('Invalid order');
  }

  await processPayment(order);
  await updateInventory(order);
  await sendConfirmation(order);

  return 'Order processed';
}
```

### Mutable Shared State

```typescript
// BAD - Mutable shared state
const config = {
  apiUrl: 'https://api.example.com',
  timeout: 5000,
};

function updateConfig(newUrl: string) {
  config.apiUrl = newUrl; // Mutation affects all consumers
}

// GOOD - Immutable state
interface Config {
  readonly apiUrl: string;
  readonly timeout: number;
}

const defaultConfig: Config = Object.freeze({
  apiUrl: 'https://api.example.com',
  timeout: 5000,
});

function createConfig(overrides: Partial<Config>): Config {
  return Object.freeze({ ...defaultConfig, ...overrides });
}

// Or use a class with private state
class ConfigService {
  private config: Config;

  constructor(config: Config) {
    this.config = Object.freeze({ ...config });
  }

  get(): Readonly<Config> {
    return this.config;
  }

  with(overrides: Partial<Config>): ConfigService {
    return new ConfigService({ ...this.config, ...overrides });
  }
}
```

### God Module

```typescript
// BAD - God module doing everything
// utils.ts
export function formatDate(date: Date): string { /* ... */ }
export function formatCurrency(amount: number): string { /* ... */ }
export function validateEmail(email: string): boolean { /* ... */ }
export function hashPassword(password: string): string { /* ... */ }
export function generateId(): string { /* ... */ }
export function parseQueryString(qs: string): object { /* ... */ }
export function deepClone<T>(obj: T): T { /* ... */ }
export function debounce(fn: Function, ms: number): Function { /* ... */ }
// ... 50 more unrelated functions

// GOOD - Focused modules
// utils/date.ts
export function formatDate(date: Date): string { /* ... */ }
export function parseDate(str: string): Date { /* ... */ }

// utils/currency.ts
export function formatCurrency(amount: number, currency?: string): string { /* ... */ }

// utils/validation.ts
export function isValidEmail(email: string): boolean { /* ... */ }

// utils/crypto.ts
export function hashPassword(password: string): Promise<string> { /* ... */ }
export function verifyPassword(password: string, hash: string): Promise<boolean> { /* ... */ }
```

### Type Assertions Abuse

```typescript
// BAD - Forcing types with assertions
const data = fetchData() as UserData; // Dangerous if fetchData returns wrong type
const element = document.getElementById('app') as HTMLDivElement; // Could be null

function process(input: unknown) {
  const user = input as User; // No validation
  console.log(user.name);
}

// GOOD - Type guards and validation
function isUserData(data: unknown): data is UserData {
  return (
    typeof data === 'object' &&
    data !== null &&
    'id' in data &&
    'name' in data &&
    typeof (data as UserData).id === 'string' &&
    typeof (data as UserData).name === 'string'
  );
}

const data = fetchData();
if (isUserData(data)) {
  console.log(data.name); // Type-safe
}

// For DOM elements
const element = document.getElementById('app');
if (element instanceof HTMLDivElement) {
  element.innerHTML = 'Hello'; // Type-safe
}

// Or use Zod
const userSchema = z.object({
  id: z.string(),
  name: z.string(),
  email: z.string().email(),
});

function processUser(input: unknown): User {
  return userSchema.parse(input); // Throws if invalid
}
```

### Boolean Parameters

```typescript
// BAD - What do these booleans mean?
createUser(name, email, true, false, true);
fetchData(url, true, false);

// GOOD - Use options object
interface CreateUserOptions {
  sendWelcomeEmail?: boolean;
  requireEmailVerification?: boolean;
  isAdmin?: boolean;
}

function createUser(
  name: string,
  email: string,
  options: CreateUserOptions = {}
): User {
  const {
    sendWelcomeEmail = true,
    requireEmailVerification = true,
    isAdmin = false,
  } = options;
  // ...
}

createUser('John', 'john@example.com', {
  sendWelcomeEmail: true,
  isAdmin: true,
});

// Or use separate functions for different behaviors
function createAdminUser(name: string, email: string): User { /* ... */ }
function createRegularUser(name: string, email: string): User { /* ... */ }
```

---

## Industry Best Practices

### Strict TypeScript Configuration

```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "alwaysStrict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noImplicitOverride": true,
    "exactOptionalPropertyTypes": true
  }
}
```

### Error Handling

```typescript
// BAD - Generic error handling
try {
  await processOrder(order);
} catch (e) {
  console.log('Error:', e);
}

// GOOD - Typed error handling
class AppError extends Error {
  constructor(
    message: string,
    public readonly code: string,
    public readonly statusCode: number = 500,
    public readonly isOperational: boolean = true
  ) {
    super(message);
    this.name = 'AppError';
    Error.captureStackTrace(this, this.constructor);
  }
}

class ValidationError extends AppError {
  constructor(
    message: string,
    public readonly errors: Record<string, string[]>
  ) {
    super(message, 'VALIDATION_ERROR', 400);
  }
}

class NotFoundError extends AppError {
  constructor(resource: string, id: string) {
    super(`${resource} with id ${id} not found`, 'NOT_FOUND', 404);
  }
}

// Result type for explicit error handling
type Result<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E };

async function getUser(id: string): Promise<Result<User, NotFoundError>> {
  const user = await userRepository.findById(id);

  if (!user) {
    return { success: false, error: new NotFoundError('User', id) };
  }

  return { success: true, data: user };
}

// Usage
const result = await getUser('123');
if (!result.success) {
  // Handle error - type is narrowed to NotFoundError
  console.log(result.error.code);
} else {
  // Use data - type is narrowed to User
  console.log(result.data.name);
}
```

### Null Safety

```typescript
// BAD - Unsafe null access
function getDisplayName(user: User): string {
  return user.profile.displayName.toUpperCase();
}

// GOOD - Optional chaining and nullish coalescing
function getDisplayName(user: User): string {
  return user.profile?.displayName?.toUpperCase() ?? 'Anonymous';
}

// GOOD - Explicit null handling with types
interface User {
  id: string;
  name: string;
  email: string | null; // Explicitly nullable
  profile?: UserProfile; // Optional
}

function formatEmail(user: User): string {
  if (user.email === null) {
    return 'No email provided';
  }
  return user.email.toLowerCase();
}

// GOOD - NonNullable utility type
function processEmail(email: NonNullable<User['email']>): void {
  // email is guaranteed to be string here
  console.log(email.toLowerCase());
}

const user = await getUser(id);
if (user.email) {
  processEmail(user.email); // Type-safe
}
```

### Async Patterns

```typescript
// BAD - Not handling promise rejections
async function loadData() {
  const data = await fetch('/api/data'); // Unhandled rejection
  return data.json();
}

// BAD - Sequential when parallel is possible
async function loadDashboard(userId: string) {
  const user = await getUser(userId);
  const orders = await getOrders(userId);
  const notifications = await getNotifications(userId);
  return { user, orders, notifications };
}

// GOOD - Parallel execution
async function loadDashboard(userId: string) {
  const [user, orders, notifications] = await Promise.all([
    getUser(userId),
    getOrders(userId),
    getNotifications(userId),
  ]);
  return { user, orders, notifications };
}

// GOOD - Promise.allSettled for independent operations
async function syncData(items: Item[]) {
  const results = await Promise.allSettled(
    items.map(item => syncItem(item))
  );

  const succeeded = results.filter(r => r.status === 'fulfilled');
  const failed = results.filter(r => r.status === 'rejected');

  console.log(`Synced ${succeeded.length}/${items.length} items`);

  if (failed.length > 0) {
    console.error('Failed items:', failed.map(r => r.reason));
  }
}

// GOOD - Timeout wrapper
function withTimeout<T>(promise: Promise<T>, ms: number): Promise<T> {
  const timeout = new Promise<never>((_, reject) => {
    setTimeout(() => reject(new Error(`Timeout after ${ms}ms`)), ms);
  });
  return Promise.race([promise, timeout]);
}

const data = await withTimeout(fetchData(), 5000);
```

### Immutability

```typescript
// BAD - Mutating arrays/objects
function addItem(cart: CartItem[], item: CartItem): CartItem[] {
  cart.push(item); // Mutation!
  return cart;
}

function updateUser(user: User, name: string): User {
  user.name = name; // Mutation!
  return user;
}

// GOOD - Immutable updates
function addItem(cart: readonly CartItem[], item: CartItem): CartItem[] {
  return [...cart, item];
}

function updateUser(user: Readonly<User>, updates: Partial<User>): User {
  return { ...user, ...updates };
}

// GOOD - Use readonly types
interface User {
  readonly id: string;
  readonly email: string;
  name: string; // Only name is mutable
}

type ReadonlyUser = Readonly<User>;

// GOOD - Immer for complex immutable updates
import { produce } from 'immer';

const nextState = produce(state, draft => {
  draft.users[0].name = 'New Name';
  draft.settings.theme = 'dark';
});
```

### Module Organization

```typescript
// BAD - Barrel exports with side effects
// index.ts
export * from './user';
export * from './order';
export * from './product';
// Imports everything even if you only need one thing

// GOOD - Explicit exports
// users/index.ts
export { UserService } from './UserService';
export { UserRepository } from './UserRepository';
export type { User, CreateUserDTO } from './types';

// GOOD - Path aliases
// tsconfig.json
{
  "compilerOptions": {
    "paths": {
      "@/services/*": ["src/services/*"],
      "@/utils/*": ["src/utils/*"],
      "@/types/*": ["src/types/*"]
    }
  }
}

// Usage
import { UserService } from '@/services/users';
import { formatDate } from '@/utils/date';
```

---

## Quick Reference

| Principle | Remember |
|-----------|----------|
| SRP | One reason to change |
| OCP | Extend, don't modify |
| LSP | Subtypes are substitutable |
| ISP | Small, focused interfaces |
| DIP | Depend on abstractions |
| DRY | Single source of truth |
| KISS | Simple beats clever |
| YAGNI | Build what you need now |

| Pattern | Use When |
|---------|----------|
| Strategy | Multiple algorithms, swap at runtime |
| Factory | Complex object creation |
| Repository | Abstract data access |
| Builder | Complex object construction |
| Decorator | Add behavior dynamically |
| Observer | Event notifications |

| Anti-Pattern | Solution |
|--------------|----------|
| Any Abuse | Proper types, generics, Zod |
| Callback Hell | Async/await |
| Mutable State | Immutable updates, Immer |
| God Module | Focused modules |
| Type Assertions | Type guards, validation |
| Boolean Params | Options objects |

| Type Utility | Use For |
|--------------|---------|
| `Partial<T>` | All properties optional |
| `Required<T>` | All properties required |
| `Readonly<T>` | All properties readonly |
| `Pick<T, K>` | Subset of properties |
| `Omit<T, K>` | Exclude properties |
| `Record<K, V>` | Object with key type K |
| `NonNullable<T>` | Remove null/undefined |
| `ReturnType<F>` | Function return type |
| `Parameters<F>` | Function parameters tuple |
