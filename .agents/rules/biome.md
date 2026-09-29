---
alwaysApply: false
paths:
- '**/*.ts'
- '**/*.tsx'
- biome.json
---

# Biome Conventions

## Usage and Configuration

- Use the repository's configured lint command to apply fixes. The check that gates a push is the
  command CI runs, as `execute-task`'s **Pre-Push Gate** defines.
- Respect any checked-in hook that runs Biome automatically.

Discover the active Biome configuration from the repository. Do not change formatting or lint policy unless the task requires it.

## Formatting and Imports

Follow the configured import organization, typically:
1. External packages
2. Internal aliases (`@/`)
3. Relative imports

Let Biome own configured indentation, quote style, semicolons, trailing commas, and line width.

## Linting

### Enabled by Default

- No unused variables
- No unreachable code
- Prefer `const` over `let` when possible
- No implicit `any` in TypeScript
- No console.log in production code

### React-Specific

- Exhaustive hook dependencies
- No direct DOM manipulation
- Proper key props for lists

## Guardrails

Only ignore when truly necessary:

```typescript
// biome-ignore lint/suspicious/noConsoleLog: Debug logging needed
console.log("Debug info");
```

Or for a file:

```typescript
// biome-ignore-file lint/suspicious/noConsoleLog
```
