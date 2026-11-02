---
name: skill-flow
description: "Show how the skills run as a dashboard: one page per kind of work (execution, review, delivery, guidance, doctors, deferrals), each a diagram of which skill invokes, spawns or borrows from which, where subagents start and how many, read from the current canonical guidance. Use when asked how skills run, what calls what, where subagents spawn, or for the flow of one skill or kind of work. Read-only: it never runs the workflows it shows."
short_description: 'Show how the skills run, as a dashboard of flows by kind of work.'
---

# Skill Flow

## Dependencies

- `use-dashboard` — render the dashboard and deliver it.

## Pages

The dashboard's `icon` is `diagram`. After `Overview`, one page per kind of work, each named and
iconed as below and holding the skills that kind of work runs through. A skill sits on the page of
the work it belongs to and appears on another only as a node that page's flow reaches.

| Page | `icon` | Starts from |
| --- | --- | --- |
| Execution | `activity` | `execute-task`, through planning, `pre-production`, the per-step gates and completion |
| Review | `check` | `review-pass`, with `code-simplify`, `code-review`, `acceptance-gate` and `security-audit` |
| Delivery | `pull-request` | a draft pull request to its merge: `rewrite-git-history`, `merge-conflict`, `merge-gate`, `finish-pr`, `merge-now` |
| Guidance | `guide` | `edit-skill`, through `session-ledger`, `process-ledger`, `test-skill`, `update-skills` and `review-proposal` |
| Doctors | `shield` | `doctor-protocol` and the doctors that run on it |
| Deferrals | `checklist` | `defer-scope`, `execute-defer-scope` and `defer-execution` |

A request that names one skill or one kind of work builds `Overview` and only the pages it reaches.
A kind of work that gains or loses skills changes its page's flow, never this table's pages, unless
the request asks for a new page.

## Workflow

1. **Locate the sources.** Find the current canonical skills, from the skills repository's checkout
   or the installed canonical links, never by assuming the working directory holds them. Record the
   repository, the commit read, and whether any source file is uncommitted.
2. **Read each page's flow.** From each page's starting skills, read the entry points and follow
   every invocation, subagent launch and borrowed rubric the flow reaches, including conditional
   ones such as `security-audit` and `test-skill`. Read `subagent-matrix` and its capability
   reference for who a launch uses, without dispatching anything. Note, for every claim, the
   `SKILL.md` lines that state it.
3. **Map it.** For each page, record the order, the choices, the parallel streams, the repair and
   rerun loops, and which skill owns each step. Keep three kinds of connection apart: one skill
   invoking another, one launching subagents, and one borrowing another's criteria. Invoking a skill
   or borrowing its rubric starts no extra agent. Record each subagent launch with its owner, role,
   capability, whether it always or only sometimes runs, how many run per round, and whether it
   recurs. A launch always runs when it runs on every run of the step that starts it. When one skill
   runs another's phases, the launch belongs to the skill whose run starts it. These are structural
   counts, never measured time or cost.
4. **Recheck the sources** before building. When a file the map cites changed while you read, map it
   again; never show a mix of two snapshots as current. A change to a file the map does not cite
   leaves it standing, and links stay on the commit read. A source that is missing or still
   changing makes the map incomplete, and the page says which connection is unknown.
5. **Build the spec** for `use-dashboard`:
   - `title` `Skill flow`, `icon` `diagram`, and `subtitle` "How the skills run, read from
     <repository> at <short commit>.", with `references` linking the repository and the commit.
   - `metrics`: **Skills mapped**, **Pages** (the kind-of-work pages), **Subagent launches** (each
     launch point counted once, however many pages reach it), and **Unknown** (connections the
     sources left open).
   - `Overview`, `icon` `overview` and `layout` `rows`: a `table` `By kind of work` with a row per
     page and the columns Page, Skills (every skill its flow reaches), Starts from, Subagent
     launches (the launch points its flow reaches) and Loops (how many repair or rerun loops, then
     each in a few words); then `notes` `How to read the flows`, one line each for an invocation
     arrow, a launch arrow and a borrowed-rubric arrow as their labels show them.
   - Each kind-of-work page, `layout` `rows`: a `diagram` `Flow` whose nodes are the skills the
     page's starting skills reach directly, each labelled with its name and its role in a few words,
     and one node per launch named for the subagents it starts and how many, such as `Plan
     attackers ×3 per round`, as its outline item is titled. Edges are labelled `invokes`,
     `launches` (from the skill to its launch node) or `borrows`, and `steps` say in order how the
     work moves through them; a skill reached only further down appears in the `Skills` table
     alone. Then an `outline` `Where subagents start`, grouped by the skill that launches them, one
     item per launch saying who, how many and when, toned `warning` for a launch that always runs
     and neutral for a conditional one; then a `table` `Skills` with the columns Skill, Role and
     Started by.
   - Every claim points at its source: each outline item's `links` take a `spec` link to the
     `SKILL.md` lines that state it, at the commit read, and `references` make each skill's name a
     link to its whole `SKILL.md` wherever the page's text names it. Each item's `meta` names the
     launch's capability level from `subagent-matrix`, or says it is unstated.
6. **Deliver** through `use-dashboard`. Name what is incomplete, if anything, in one line.

## Guardrails

- Never invoke or dispatch a workflow the dashboard shows; reading its sources is the whole job.
- Show the current flow only. A proposed change, or a recommendation, appears only when the request
  asks for it, as an outline beside the flow, never drawn into it.
