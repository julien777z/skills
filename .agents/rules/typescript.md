---
globs:
- '**/*.ts'
- '**/*.tsx'
alwaysApply: false
paths:
- '**/*.ts'
- '**/*.tsx'
---

# TypeScript Rules

## Types And Interfaces

- Enable strict mode in `tsconfig.json`.
- Avoid `any`; use `unknown` with type guards instead.
- Give exported functions explicit return types.
- Use `interface` for object shapes that may be extended and `type` for unions, intersections, and utility types.
- Mark type-only imports with `type`.
- Give generics meaningful names and constrain them when possible.
- Prefer built-in utility types such as `Partial`, `Required`, `Pick`, `Omit`, and `Record` over equivalent hand-written shapes.
- Do not use `React.FC`; type props explicitly. Use `ComponentProps<typeof Component>` to extract component props and `PropsWithChildren` when a component accepts children.
- Prefer const objects with inferred value unions over enums for tree-shaking.

```typescript
import type { ComponentProps, PropsWithChildren } from "react";

interface ButtonProps {
  variant: "primary" | "secondary";
  onClick: () => void;
}

function Button({ variant, onClick, children }: PropsWithChildren<ButtonProps>) {
  // ...
}

const Status = {
  Active: "active",
  Inactive: "inactive",
} as const;

type Status = (typeof Status)[keyof typeof Status];
```

## Module Structure

- A TS/TSX module must own a broad domain, not a single feature, action, watcher, or one-shot helper. Name modules after the domain (`payments.ts`), not the feature (`paymentsRefundButton.ts`).
- Avoid role-suffixed file names like `*Action.ts`, `*Lookup.ts`, `*Watcher.ts`, `*Extractor.ts`, `*Url.ts`, or `*Collections.ts`; the folder already conveys the role.
- Cross-domain helpers belong in a generic `utils` or `lib` module, not in a module named after a single feature.
- Split a domain module into a subfolder only when the single file would exceed approximately 1000 lines. Name the folder after the domain and its files after subareas.
- When renaming or merging a module, update every importer in the same commit. Do not leave a re-export shim at the old location.
- **Fewer files, and fewer functions in them, is the default.** Each one is a cost every later reader
  pays: another place to look, another name to learn. A module whose public surface is one function,
  one small type, or one constant has not earned a file — merge it into the module that already owns
  its concern. Several modules that each hold one symbol of one shape are one module under several
  names.
- A function with one caller belongs in that caller unless it is genuinely reused, genuinely
  recursive, or long enough that inlining would bury the caller's own shape.
- **A module that only forwards is not a layer.** When every function in it is one call to the module
  beneath with the same arguments, delete it and let consumers reach that module. An area's index is
  not this: it re-exports rather than wraps, and adds no call.
- Never alias a project import to a second name. A collision between two modules' exports is a naming
  defect in one of them; rename it rather than aliasing at the import site.

## Area Imports

- **An area publishes what it offers, and a consumer reaches it in one line.** A directory several
  modules import from — the controls, the hooks, the helpers, the shared screens — carries an index
  that re-exports its modules, and a consumer imports the names it needs from that directory rather
  than from each file inside it. A file wanting four controls and a hook then opens with two import
  lines instead of five, and moving a module within an area rewrites nothing outside it.
- **That index is the area's surface, not a shim.** It re-exports every module the area holds and
  grows as modules are added. The re-export the rule above forbids is the one left behind at a
  module's old path after a rename, which exists only so stale importers keep resolving; update
  those importers and delete it.
- Modules inside an area import their siblings by relative path, never through their own index, so
  an area never depends on itself. An area whose index would have to re-export another area's
  modules is two areas rather than one, and an index that would import from a module that imports it
  back names the cycle rather than creating it.
- Two names that collide across an area's modules cannot both be published from one index. Rename
  one for what it is; an index that silently drops the duplicate is a name nobody can import.

## Functions

- **A function whose body is one call to the canonical function is banned**, whether it forwards its
  arguments unchanged or supplies a fixed value for one of them. Call the canonical function at the
  use site and name the argument there. Several call sites passing the same constant is not a defect
  and does not earn a wrapper to hold it.
- That remedy assumes the callee is ours. A third-party signature cannot be changed, so one named
  helper holding its fixed arguments is allowed and beats repeating them everywhere — but any logic
  of our own in its body makes it an ordinary function subject to the rule above.
- Name a guard for the condition it asserts rather than the outcome it prevents, so the call site
  reads as the rule that must hold. Keep the name truthful to what the guard actually checks.
- Do not rebind a parameter to a second local name when the value is unchanged; name the parameter
  correctly in the signature instead.
- Give domain-specific parsers, builders and formatters domain-qualified names. A generic name
  promises that any compatible input is accepted and collides when two domains are imported together.
- **Widen a narrow helper rather than writing a second one beside it.** Two live implementations of
  one guard, check or transform is the defect whichever came first; a differing message, error type
  or argument shape is a parameter, not a reason to keep both.

## Constants

- Declare constants at the top of the module, after the imports.
- Every module-level declaration states its type, through `as const` or an explicit annotation. An
  untyped module-level name is a finding on its own, whatever it holds.
- **Several constants of one shape are a data structure, not a pile of names.** Parallel per-kind
  values become one mapping keyed by the union that names those kinds, read at the use site.
- Reserve constants for what is genuinely invariant. A value operators, environments or releases may
  reasonably change belongs in typed configuration even when it has a safe default; capitalization
  does not make it invariant.
- Extract a literal only when it is reused or carries domain meaning. Keep trivial single-use
  literals inline.
- Do not prefix a name with the area it already lives in. The module path says it; add a qualifier
  only for a real collision, or when the name travels outside its home.
- **Never write out a list of names as string literals when a type already declares them.** Derive
  the set from that type, so adding a member cannot silently leave the list behind.

## External Data And Errors

- **Any unsuccessful response from a service gets one branch.** Report the status and raise the
  caller's error. Do not branch per status code or map a provider's codes onto distinct messages;
  that restates a contract we do not own.
- Success is the whole `2xx` range, not `200`. A create call answers `201`.
- Read a domain outcome from the body of a successful response, never from the status of a refused
  one.
- Implement the one contract the boundary actually has. Do not widen a type or add a branch for a
  shape that is not part of it, and prefer fixing the call site over adding defensive conversion in a
  shared helper.
- Do not add speculative fallbacks for a dependency's surface — no catching a missing-method error to
  try another call path. Call the method the contract states and update it explicitly when it
  changes.
- Do not wrap a canonical lookup in a `catch` that swallows the failure and continues with a guessed
  value or a degraded mode. Handling a legitimate *state* of the data is fine; inventing a substitute
  when the source is unavailable or malformed hides drift and turns an outage into wrong behaviour.
- Catch the specific error type, never a bare catch-all, unless the handler compensates for a durable
  trace and then re-throws.

## Suppressions

- **Never add a suppression.** No `@ts-ignore`, no `@ts-expect-error`, no `biome-ignore`, no
  `eslint-disable`, no new entry in a tool's ignore list, no lowered threshold, and no hand-written
  declaration file standing in for a dependency's own types.
- A suppression removes the report and leaves the thing reported exactly where it was. It reads
  identically whether its author weighed the finding and judged it wrong or never looked, so the next
  reader cannot tell which, and the exemption outlives whoever had a reason for it.
- Fix what the tool reports, publish types at the source when the package is ours, or leave the
  report standing. A red run carrying known reports is a truthful record of work still to do.
- The Comments section's exception admits a tooling directive as something other than prose, so a
  sweep that strips comments leaves it alone. That is about not deleting one that already exists; it
  is not licence to add one.

## Comments

- **The code carries its own explanation, so it carries no comments.** A name, a type, and a
  function small enough to read at once say what a sentence beside them would, and they cannot drift
  from the code the way the sentence does. Where a line needs prose to be understood, rename it,
  split it, or give the value a type that states what it is.
- The exception is a directive the tooling reads — a linter suppression, a type-checker instruction
  — which is not prose and stays.
- **The other exception is behaviour somebody else owns, which no amount of renaming can make the
  code show.** A framework that consumes its own headers before your code runs, a browser that sends
  a request for a document when nobody navigated, a library whose call means something other than it
  reads: the reason lives outside this repository, so the code cannot state it and the next reader
  cannot derive it. One or two lines, factual, about the external behaviour alone.
- Judge it by where the reason lives, never by how surprising the line looks. A branch that puzzles a
  reader because the code around it is tangled is a refactor; the same branch puzzling them because a
  protocol says something unexpected is the comment this exception is for.
- **A sweep that removes comments is where this exception gets lost**, because such a comment reads
  like every other one and its subject is the thing the sweeper cannot see. Before deleting a comment,
  ask whether it names something outside this repository; keep it when it does.

## Guardrails

- Do not delete feature logic because it looks extra. Check the active request, the nearby tests, and
  the call sites before concluding that newly added code is dead.
- Where a cleanup instruction meets clear feature intent, preserve the behaviour and ask rather than
  removing the feature.
