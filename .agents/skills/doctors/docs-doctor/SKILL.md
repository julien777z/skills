---
name: docs-doctor
description: Find and fix documentation that no longer matches the code. It covers paths, commands, symbols, variables, and flags that do not exist, behavior the code no longer has, history narration, repeated explanations, descriptions of inputs and options that do not say what the value is, paths only one machine has, and README structure against the repository's README rules. Use to audit docs, READMEs, docstrings, or stale references across a repository. Run only when the user asks for it.
short_description: 'Find and fix documentation that no longer matches the code.'
---

# Docs Doctor

Documentation describes what exists now. This doctor finds every sentence that describes something
else.

## Dependencies
- `doctor-protocol`
- `pre-production`
- `get-doctors`
- `council`

## Inventory

Run `doctor-protocol`.

Apply the repository's documentation and README rules; this doctor never restates them.

Every README and documentation tree; every docstring; every description a manifest, action,
workflow or settings model gives an input, option or field; and, for each, every path, command,
symbol, variable, flag, URL, and described behavior it names. Agent guidance files belong to the
doctor `get-doctors` lists for agent guidance, every lens included. Resolve each reference against
the current tree, the commands the manifests declare, the runner's targets, and the settings models.
Generated documentation is excluded and corrected at its generator; vendored documents are
excluded as another owner's.

**Shared index.** From the index `doctor-protocol`'s **Share The Index** keeps, this doctor reads
the file inventory, symbol table, dependency list with each manifest's scripts, and configuration
names. It writes the reference table: one row per reference with its document, line, kind and
whether it resolved.

### Pre-Pass

These are the mechanical steps `doctor-protocol` runs once before any reviewer reads. They fill the
reference table: a reference that resolved is read by nobody, and a reviewer judges only the rows
that did not and the lenses no step covers. A tool the repository does not configure is handled as
`doctor-protocol`'s **Measure Before Fan-Out** says.

- **Extract** — a script kept in the run's working files lists, per Markdown file and docstring,
  every backticked token, link target and fenced command, each classified as a path, command,
  symbol, environment name, flag or URL.
- **Paths and links** — each path resolved against the tree; relative links and heading anchors
  with an offline link checker.
- **Commands** — each command's program and script name against the manifests' scripts, the
  runner's targets and the executables the repository ships.
- **Environment names and flags** — each against the settings models and the commands' own
  argument declarations.
- **Symbols** — a whole-word search of the source for each.
- **Inputs tables** — each README's inputs table against the inputs its action or workflow
  declares, by name and default.
- **History words and one-machine paths** — the searches below, over documentation and
  descriptions.

```sh
lychee --offline --no-progress '**/*.md'
rg -nw '<symbol>' <source roots>
rg -ni 'formerly|used to|no longer|replaces|deprecated|kept for|backwards compat|previously' -g '*.md'
rg -n '/home/|/Users/|/tmp/|[A-Za-z]:\\' -g '*.md'
```

### Measures

The counts `doctor-protocol` takes before the audit and again after the fixes: documents and
docstrings in scope; references extracted and unresolved, by kind; broken links and anchors;
history-word and one-machine-path hits; and inputs-table rows that disagree with their declaration.
The unresolved counts read zero when the run is finished.

## Lenses

Every finding is recorded in `doctor-protocol`'s
finding shape: its fix is the corrected reference or the sentence to delete, and its proving check
is the pre-pass step that listed it returning nothing for that row.

### Unresolvable References

Flags a path, command, symbol, variable, flag, link or anchor named in prose that the tree, a
manifest, or the runner does not have. Reach: partition.

- every unresolved row of the reference table, by kind: path, link and anchor, command, environment
  name, flag, symbol;
- every inputs-table row whose name or default disagrees with the declared input;
- every fenced command whose program resolves but whose subcommand, script or flag does not.

Remedy: the reference is corrected to what exists; where the thing is gone, the sentence goes with
it, apart from a command that ought to exist, which **Dispositions** settles. Left alone: a placeholder written as one, such as a name in angle brackets; a URL outside the
repository, which is checked only when the run has network access and is reported unchecked
otherwise; and a reference inside generated documentation, fixed at its generator.

### Retired Behavior

Flags a described behavior the code no longer has, or a described default, order, or response the
code contradicts. Reach: partition.

- every sentence stating a default, a limit, an order of steps, a response or an error: read
  against the declaration or handler that decides it;
- every documented command's described effect, against the script or target it runs;
- every setup or usage sequence, walked against the manifests and bootstrap it names;
- every docstring whose summary names a behavior its body no longer has.

Remedy: the sentence states what the code does, or is deleted when the behavior is gone. Left
alone: a statement of intended behavior the code fails to meet, which is a defect in the code and
is fixed there, as `doctor-protocol`'s **Resolve The Scope** says.

### History Narration

Flags documentation that recounts what changed: "formerly", "used to", "replaces", migration
tables, upgrade notes, and deprecation prose, against `pre-production`'s **Documentation**
conventions. Reach: partition.

- every history-word hit in a document or a description;
- every table or section whose columns or headings are a before and an after.

Remedy: the sentence is deleted rather than reworded as history, and what still holds is stated in
the present. Left alone: a changelog or release record whose purpose is that history; and history
narration inside code comments and docstrings, which belongs to the doctor `get-doctors` lists for
code slop.

### Structure

Flags README shape against the repository's README rules, one explanation repeated across
documents where one home and a link would do, and content whose reader is not the document's
reader, such as a runbook or design specification in a README. Reach: whole repository.

- every README against the README rule, bullet by bullet: its heading, its sections
  and their order, its Local Development commands, and for an action or library its Features,
  Examples and Inputs table;
- every explanation that appears in two documents, matched by the commands, paths and headings
  they share;
- every section whose reader is an agent, an operator or a designer rather than the document's own.

Remedy: a README is restructured to the rules rather than patched one heading at a time; a
repeated explanation collapses to one home and a link; misplaced content moves to the document
whose reader acts on it. Left alone: a short restatement at a point of use that links its home.

### Descriptions

Flags a description that does not tell its reader what the value or operation is. Reach: partition.

- every description of an input, output, option, setting or field, against `pre-production`'s
  **Repository Text**: one that restates the flag or variable the value becomes, stands a
  value grammar in place of words, or lists which callers use it;
- every route handler's docstring, against the FastAPI rules' **Route Metadata**: one that restates
  the router's prefix, tag or guard, or names the caller, in place of the operation.

Remedy: a plain sentence saying what the value is, or what the operation does, and for a value
from a fixed set what each one does. Left alone: an external action's or library's own
descriptions; and docstring length and style, which belong to the doctor `get-doctors` lists for
code slop — this doctor takes a docstring only for a nonexistent thing, a retired behavior or a
route description.

### Machine And Example Values

Flags prose that holds a value from one machine or one person's data, against `pre-production`'s
**Examples And Paths** and **Whose Standards Apply** conventions. Reach: partition.

- every one-machine-path hit: a home directory, a temporary directory, the place a checkout sits, a
  drive letter;
- every environment named without its full domain name;
- every sample value in an example that is shaped like a real identifier, address or amount rather
  than a plainly synthetic one.

Remedy: a path from the repository root, or the file named for what it is and how a reader obtains
it; the environment's full domain name; a newly invented synthetic value keeping only the trait the
example turns on. Left alone: a literal a protocol or provider defines for every caller, and the
same values in source code, which belong to the doctor `get-doctors` lists for code slop.

## Reviewers

Reviewers are capped as `doctor-protocol`'s **Launches** sets. The
document dictates the partition cut: a documentation tree and the docstrings of the packages it
documents stay in one partition where the size bound allows. The cross-cutting reviewer owns
**Structure**, working from the reference table, and compares documents with each other: one
command, path, or behavior described differently in two places. The final reviewer
re-resolves every retained reference against the current tree and confirms that a collapsed
explanation lost no distinct fact.

## Dispositions

Apply `pre-production` to the target contract documented.

- This doctor changes documentation, docstrings and descriptions. A document that is right about
  what the code should do is evidence of a code defect, fixed at its owner.
- A documented command that ought to exist but does not is a finding about the manifest, which the
  run settles itself: it declares the command where the code shows what it runs, deletes the
  sentence otherwise, puts it to `council` when the code shows neither, and names the outcome in
  the report.
- A finding another doctor owns is not fixed here; the report names it with that doctor, found
  through `get-doctors`.

## Report Additions

- per document: references checked, fixed, and deleted, by kind;
- structural changes made, and each explanation collapsed with its home;
- each description rewritten, and each one-machine path or sample value replaced.
