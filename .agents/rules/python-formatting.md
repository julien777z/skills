---
description: Apply when formatting Python code or writing its docstrings and comments.
alwaysApply: false
paths:
- '**/*.py'
---

# Python Formatting And Documentation

## Formatting and Documentation

- Name things for the behavior they actually have, in terms the shared banned-terms list permits; that list says what to use instead.

- Add a blank line after each docstring.
- Never add decorative separator comments (for example, `# -----` headers).
- Use blank lines as logical phase boundaries: separate adjacent statements that advance to a different responsibility, even when both are short, such as setup from main logic, an action from logging or reporting, the construction of an object from configuring or using it, each independently configured parser or command group from the next, a module-scope runtime collaborator such as a logger from the constants and declarations after it, and a statement of a different kind that begins a new logical group (for example `assert` to a mock-verification call). Statements that jointly prepare one check, transformation or result, or a 2–3 line block whose every line contributes to the same operation, stay together; compactness alone is no reason to remove a boundary.
- Add a blank line after a multi-line statement (a function call, a context manager), before a multi-line `assert`, and before a terminating statement (`sys.exit()`, `return`, `raise`).

```python
# Good: blank line separates setup from main logic
artifacts_dir = tmp_path / "artifacts"
artifacts_dir.mkdir()

create_artifact(artifacts_dir, "first", None)
create_artifact(artifacts_dir, "second", "first")

# Bad: no separation between setup and main logic
artifacts_dir = tmp_path / "artifacts"
artifacts_dir.mkdir()
create_artifact(artifacts_dir, "first", None)
```

```python
# Good: related setup stays together, then one blank line introduces validation
start_marker = FORMAT["start_marker"]
end_marker = FORMAT["end_marker"]
start_count = content.count(start_marker)
end_count = content.count(end_marker)

if start_count != end_count:
    raise ValueError("Managed markers are malformed")
```

```python
# Good: action and reporting are separate responsibilities
perform_update(records)

logger.info("Update complete")

# Good: keep construction separate from later setup and use
parser = argparse.ArgumentParser()

subparsers = parser.add_subparsers(dest="command", required=True)

create_parser = subparsers.add_parser("create")
create_parser.add_argument("--dry-run", action="store_true")

validate_parser = subparsers.add_parser("validate")
validate_parser.set_defaults(dry_run=False)

parsed_arguments = parser.parse_args(arguments)

# Good: a runtime collaborator is separate from module declarations
logger = logging.getLogger(__name__)

MAX_ITEMS: Final[int] = 20
ALLOWED_STATES: Final[frozenset[str]] = frozenset({"ready", "complete"})
```

- Do not put docstrings or comments at the top of files (no module-level docstrings, no module-level comments, and no encoding header comments like `# coding: utf-8`).
  A migration revision file's first line may be a lock marker an invoked migration skill defines:
  it is a machine-read marker, and it stays verbatim.

- Every **function**, **method**, and **class** should have a concise docstring (purpose or role). Include `main()` and nested helpers the same way unless the file’s existing style omits docstrings on tiny locals—when in doubt, add one line.
- Keep ordinary docstrings to a single line. Do not include Args, Returns, or Raises sections.
- **Migration revision files are the only exception:** their `upgrade()` and `downgrade()` docstrings
  name the concrete schema or data transformation and why it is needed. Before writing or accepting
  either docstring, identify its principal target shape or constraint and the reader or writer
  requirement it satisfies. Put both in the text; an auxiliary preparation or recovery purpose
  cannot substitute for that transformation's reason. Use a few concise lines when both do not fit
  clearly on one; never an essay. Generic text such as “Apply this schema
  revision” or “Restore the preceding schema revision” does not identify the operation or its
  purpose. The exception does not extend to ordinary application functions or migration helpers
  outside revision files, and it permits no Args, Returns, or Raises sections.
- Class docstrings go directly after the class definition.
- Docstrings describe current behavior only — never reference what the code replaces, used to do, or PR/migration history. The docstring must read the same to a new reader who never saw the prior version.
- **Ordinary docstrings name the thing; they do not inventory it.** Say what a symbol is in the shortest phrase
  that identifies it. It is not a summary of the fields the class holds, the branches the function
  takes, or the guarantees it upholds — a reader who needs those reads the code directly, and the
  signature is already right there.
- An ordinary provider docstring names the operation and explains behavior the caller needs to
  know. Describe wire selectors and request field counts in the transport contract and verify
  them in its tests. Document a provider quirk where it explains a decision a maintainer would
  otherwise miss.
- In an ordinary docstring, the failure mode is a sentence that grows a clause per aspect, usually joined by "and", "with",
  or "as what": each clause is true, and together they restate the body in prose that now has to be
  kept in step with it. Delete the clauses and keep the noun phrase.
- In ordinary docstrings, a trailing clause explaining an invariant, a fallback, or when something
  is created is narration, not identification. Drop it.

```python
# Bad: one clause per aspect, restating the body
class Roster(BaseModel):
    """Who belongs to a team and in what capacity, with the lead protected."""


# Bad: a trailing clause narrating the mechanism
def team_cache(session: Session) -> Cache:
    """Return the cache this session carries, starting one the first time it is asked for."""


# Good: the noun phrase that identifies it
class Roster(BaseModel):
    """Members of a team and their capacities."""


def team_cache(session: Session) -> Cache:
    """Return the cache this session carries."""
```
- Prose written for a person — a docstring, a comment, a log message — must not spell out an internal role, permission, or scope identifier (the literal string a provider or authorization system checks against, such as `tenant:member` or `scope:read_billing`). Name the concept in readable words instead. The identifier belongs in the code that evaluates it, where renaming it is a change the type checker and tests can see; repeated in prose it is a second copy nothing keeps honest.

```python
# Bad: the docstring and the log both spell out the internal identifier
def ensure_tenant_member(user: User) -> None:
    """Ensure a user is a tenant:member, not a guest."""

    logger.info("Checking tenant:member for %s", user.id)


# Good: prose names the concept, and only the code carries the literal
def ensure_tenant_member(user: User) -> None:
    """Ensure a user is a tenant member, not a guest."""

    logger.info("Checking tenant membership for %s", user.id)
```

- **Comments are only for third-party quirks** — an SDK bug, a library's surprising contract, a spec oddity, a protocol requirement — that a reader could not infer from our own code. If the reason lives in code you control, it is not a comment.
- **If your own code needs a comment to be understood, the code is too complex — refactor it instead.** Rename the identifier, extract a well-named helper, split the function, or restructure until the intent is obvious without prose. Reach for a comment only after the code cannot be made clearer and the remaining "why" is genuinely external.
- **Never explain behavior in a comment — tests assert behavior.** Do not narrate what a branch, guard, ordering, or invariant does or protects against; encode that in a test that fails when it regresses. The test is the durable, executable specification; the comment is not.
- **Keep any comment to 1–2 lines**, factual, and about the external quirk only. A comment that runs longer is a signal the code (or the abstraction) needs restructuring, not more prose.
- Comments describe the current external quirk only — never reference what the code replaces, used to do, what was deleted, the current task/fix/PR, or callers ("previously…", "legacy…", "now uses X instead of Y", "added for the Y flow", "used by X"). Those belong in the PR description, not the source.
