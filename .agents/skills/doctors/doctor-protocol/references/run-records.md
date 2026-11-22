# Doctor Run Records

The formats of the files a doctor run keeps, which `SKILL.md`'s **Keep The Run Ledger** places and
its later sections fill. Every file is YAML unless its name says otherwise, and every path in one
is written from the repository root.

## Folder

```text
.agent_sources/doctor-runs/<doctor>/<scope key>/
  run.yaml                  scope, base, route and a status per stage
  manifest.yaml             every in-scope path in exactly one partition
  prepass/index.yaml        each command, its status, its output file and each measure
  prepass/<command key>.txt one command's raw output
  receipts/<partition>.yaml what one reviewer read
  findings/<partition>.yaml one reviewer's findings; `cross-cutting.yaml` for that reviewer
  ledger.yaml               every entry and its status
  plan.md                   the plan: groups, order, entries and every decision
```

`<scope key>` is `whole` for the whole repository, otherwise a short slug of the selection.

## Run And Stage Status

```yaml
run:
  doctor: "<doctor name>"
  scope: "<whole | the selection as the caller gave it>"
  base: "<commit of the default branch the run's branch started from>"
  branch: "<the run's branch for each kind>"
  route: "<small | whole>"
  plan_shown: "<time the plan was shown, with `no open decision` or the decisions open then>"
  stages:
    - name: "<scope | prepass | manifest | audit | verify | plan | implement | checks | review | accept | leftovers | report>"
      status: "<pending | running | done>"
      finished: "<time, when done>"
      head: "<branch head when the stage finished>"
```

A stage is `done` only when every file it owes is written. A late audit a doctor declares adds its
own `audit` and `verify` entries, named for the lenses it covers.

## Shared Index

```text
.agent_sources/doctor-index/<commit>/
  index.yaml                each table, the doctor that wrote it and its file
  files.yaml                the file inventory: path, lines, language and owning area
  symbols.yaml              each exported symbol with its file, line and importers
  imports.yaml              each first-party and third-party import by file
  dependencies.yaml         each manifest's declarations, scripts and lockfile entries
  <table key>.yaml          one further table a doctor writes
```

`SKILL.md`'s **Share The Index** says who writes each file and when one is rebuilt.

## Manifest

```yaml
manifest:
  bound: "<lines and files per partition, as SKILL.md states them>"
  in_scope_paths: <count>
  excluded:
    - path: "<path or pattern>"
      reason: "<generated | vendored | binary | lockfile | other, as the doctor's inventory says>"
  partitions:
    - id: "<short area name>"
      area: "<the package, service, app or directory it covers>"
      files: <count>
      lines: <count>
      digest: "<content digest of its files at the audited head>"
      paths: ["<path>", "..."]
      status: "<assigned | read | unread>"
      reviewer: "<assignment identifier, when assigned>"
```

The manifest is correct when the sorted union of every partition's `paths` equals the in-scope
path list and no path appears twice; the parent establishes both with a command, never by reading.

## Read Receipt

```yaml
receipt:
  partition: "<id>"
  head: "<commit the reviewer read at>"
  read_whole:
    - path: "<path>"
      lines: <count>
  read_in_part:
    - path: "<path outside the partition opened for context>"
      why: "<the item traced there>"
  not_read:
    - path: "<path>"
      why: "<reason>"
  checks:
    - lens: "<lens>"
      check: "<the check as the lens states it>"
      result: "<count of instances, zero included>"
  candidates_judged: <count of pre-pass candidates in the partition confirmed or rejected>
```

## Finding

One shape for every doctor and every reviewer, a verifier and a worker's hand-up included.

```yaml
finding:
  id: "<partition id>-<n>"
  location: "<path>:<line or line range>, or the declaration's name where lines do not apply"
  lens: "<the doctor's lens>"
  evidence: "<the lines quoted from the file, or the command and the output lines that show it>"
  fix: "<the specific change, in the lens's remedy where it states one>"
  remedy_source: "<lens | designed>"
  reach: ["<each other file, caller, test, document or record that must change with it>"]
  severity: "<defect | vulnerability | cleanup>"
  confidence: "<high | medium | low>"
  check: "<the command or read that proves the fix, and what it shows once fixed>"
  verified: "<yes, at <head> | no: <what differed>>"
  candidate_from: "<the pre-pass command that listed it, or `read`>"
```

`remedy_source` is `lens` when the fix is the remedy the lens states and `designed` when the run
had to design one. A finding with no `evidence`, or whose quote the file at the audited head does
not hold, is dropped at verification and counted.

## Ledger Entry

```yaml
entry:
  id: "<finding id, or `kept-<n>` for an item retained without a finding>"
  finding: "<the finding, as above>"
  disposition: "<fix | keep | council ruling | reserved user decision | declined | deferred |
    unresolved>"
  reason: "<for keep: the distinction that retains it; for unresolved: the missing evidence;
    for declined or deferred: the record; for council ruling: the question, the options and the
    ruling; for reserved user decision: the options, each consequence, the recommendation and the
    answer once given>"
  group: "<the worker group that owns its files>"
  status: "<open | waiting on decision | assigned | fixed | recorded>"
  commit: "<the commit that fixed it>"
  proved: "<the finding's check and its result on that commit>"
```

Duplicates of one finding raised by several reviewers merge into one entry that lists every
location.

## Plan

`plan.md` holds, in this order: the intent statement; each decision the run made with its reason,
any council ruling, and each reserved decision with its answer; the groups in the order they run, each with its area, its files, its entry ids, what it
waits on and the wave it runs in; the paths no reviewer read; and the measures before the fixes.

The message the user reads lists one line per area — the area, its entry count by lens, and what
it waits on — followed by the totals, and sends `plan.md` with it once the plan holds more than
five entries.
