---
name: skill-flow
description: "Show how the skills run as a dashboard: one page per kind of work (execution, review, delivery, guidance, doctors, deferrals), each a diagram of which skill invokes, spawns or borrows from which, where subagents start and how many, read from the current canonical guidance; or interrogate a skill or a whole flow, asking the user about each substantial step with a recommendation for using fewer subagents to better effect, and applying what they agree. Use when asked how skills run, what calls what, where subagents spawn, for the flow of one skill or kind of work, or to review, tune or interrogate skill flows. It never runs the workflows it shows."
short_description: 'Show how the skills run, or interrogate a flow to tune it.'
---

# Skill Flow

## Dependencies

- `interactive-skill` — offer the **Modes** menu when the request does not pick one.
- `use-dashboard` — render the dashboard and deliver it.
- `edit-skill` — make the changes the user agrees to in Interrogate.
- `session-ledger` — record each answer the user gives in Interrogate.

## Modes

```yaml
prompt: What do you want to do with the skill flows?
kind: choice
choices:
  - id: show
    label: Show
    detail: build the dashboard of how the skills run
    aliases: [dashboard, map, view]
    when: the request asks how skills run, what calls what, or where subagents start
  - id: interrogate
    label: Interrogate
    detail: walk a skill or flow with you, step by step, and tune it
    aliases: [configure, tune, review the flow, audit the flow]
    when: the request asks to question, configure, tune or change how a skill or flow runs
```

**Show** follows **Pages** and **Workflow**; **Interrogate** follows **Interrogate**.

## Scope

Interrogate asks which flows to cover, when the request names none, with this menu:

```yaml
prompt: Which flows should I interrogate?
kind: choice
choices:
  - id: all
    label: Every flow
    detail: every kind of work, most subagents first
  - id: execution
    label: Execution
  - id: review
    label: Review
  - id: delivery
    label: Delivery
  - id: guidance
    label: Guidance
  - id: doctors
    label: Doctors
  - id: deferrals
    label: Deferrals
```

## Pages

The dashboard's `icon` is `diagram`. After `Overview` comes `Usage`, the view across every skill
of where subagents start, what they read and how often review repeats, then one page per kind of
work, each named and iconed as below and holding the skills that kind of work runs through. A skill sits on the page of
the work it belongs to and appears on another only as a node that page's flow reaches.

| Page | `icon` | Starts from |
| --- | --- | --- |
| Execution | `activity` | `execute-task`, through planning, `pre-production`, the per-step gates and completion |
| Review | `check` | `review-pass`, with `code-simplify`, `code-review`, `acceptance-gate` and `security-audit` |
| Delivery | `pull-request` | a draft pull request to its merge: `rewrite-git-history`, `merge-conflict`, `merge-gate`, `finish-pr`, `merge-now` |
| Guidance | `guide` | `edit-skill`, through `session-ledger`, `process-ledger`, `test-skill`, `update-skills` and `review-proposal` |
| Doctors | `shield` | `doctor-protocol` and the doctors that run on it |
| Deferrals | `checklist` | `defer-scope`, `execute-defer-scope` and `defer-execution` |

A request that names one skill or one kind of work builds `Overview`, `Usage` and only the pages it
reaches.
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
   recurs. A count that depends on the work is recorded as what it grows with, such as "1 per
   area touched" or "1 per finding", with the most the skill allows when it sets one, such as
   "1 per area, 3–6": the most a total shows counts that most, and a count with no limit shows as "grows with
   <what>" instead of a number, toned `warning`, in every total above it. A launch always runs
   when it runs on every run of the step that starts it. When one skill
   runs another's phases, the launch belongs to the skill whose run starts it. These are structural
   counts, never measured time or cost. For each skill on a page, also record its own run in
   order: each step it takes, the subagents that step launches with how many and what they do, and
   its review rounds — whether it has any, how many it allows, what ends them, and what a later
   round reruns. Record every other loop the same way: a repair loop that fixes and checks again, a
   wait that polls until something finishes, and a retry, each with its cap, what ends it, what a
   repeat reruns, and the loop it runs inside, if any. For every launch, also record the scope each
   subagent reads: the change's diff,
   only what changed since the last review, the whole files it touches, related files such as
   callers and siblings, one area of the repository, or the whole repository.
4. **Recheck the sources** before building. When a file the map cites changed while you read, map it
   again; never show a mix of two snapshots as current. A change to a file the map does not cite
   leaves it standing, and links stay on the commit read. A source that is missing or still
   changing makes the map incomplete, and the page says which connection is unknown.
5. **Build the spec** for `use-dashboard`:
   - `title` `Skill Flow Dashboard`, `topic` the repository's name, `icon` `diagram`, and `subtitle` "How the skills run, read from
     <repository> at <short commit>.", with `references` linking the repository and the commit.
   - `metrics`: **Skills mapped**, **Pages** (the kind-of-work pages), **Subagent launches** (each
     launch point counted once, however many pages reach it), and **Unknown** (connections the
     sources left open).
   - `Overview`, `icon` `overview` and `layout` `rows`: a `table` `By kind of work` with a row per
     page and the columns Page, Skills (every skill its flow reaches), Starts from, Subagent
     launches (the launch points its flow reaches) and Loops (how many of the loops the Usage
     `Loops` tree shows run in its flow, then each in a few words); then `notes` `How to read the flows`, one line each for an invocation
     arrow, a launch arrow and a borrowed-rubric arrow as their labels show them.
   - `Usage`, `icon` `chart` and `layout` `rows`, across every skill the dashboard maps:
     - a `tree` `Where subagents go`, `open_depth` 2, one root per skill a person starts directly,
       most subagents first, with `meta` the subagents one run of it typically starts, then the most
       it can start, everything beneath it counted, such as "about 6 subagents, up to 24". The
       typical figure counts, for one round each, only launches whose every ancestor always runs; a
       count that depends on the work counts at its stated least, or at one, and shows "grows with
       <what>" only when such a launch always runs. Beneath a skill, its steps in order,
       labelled "<n>. <step>" with the same typical and most figures for what sits beneath them; beneath a step, each
       skill it runs, nested the same way wherever it runs so every total counts it, and each
       launch as an entry labelled "<count> <role>", `meta` its rounds and what it reads, such as
       "up to 3 rounds · diff and whole touched files", and `detail` what the subagents do, what a
       later round reruns, and the condition it runs under when it only sometimes runs. A launch
       that always runs is toned `warning`. Every entry's `details` open what it is: a skill's,
       its skill write-up; a step's or a launch's, its entry write-up. A step with no subagents anywhere beneath it is left
       out, so the tree holds only where subagents start;
     - a `tree` `Loops`, `open_depth` 2, one root per kind of loop the skills run, each only when
       one exists: `Review loops`, rounds of reviewers; `Repair loops`, fixing and checking again;
       `Wait loops`, polling until something finishes; and `Retry loops`. A root's `meta` counts
       its loops and the most subagents they can start. Beneath a root, each loop, labelled
       "<skill>: <what repeats>", most subagents first, `meta` "up to <n> rounds · up to <m>
       subagents across them", or "no cap" when nothing bounds it, and `detail` what ends it and
       what each later round reruns. Beneath a loop, what one round starts, as the launch entries
       above, and any loop that runs inside it, its counts multiplied by the outer loop's rounds.
       A loop is toned `warning` when its later rounds rerun everything rather than only what a
       repair touched, or when nothing caps it. Its `details` open its entry write-up;
     - an `outline` `Overlapping scope`, `collapsible` false, one item per stretch of code more
       than one skill's subagents read in one run, whether the same scope or one that contains
       another, such as the diff and the diff with its callers, titled with that code and naming
       each skill and what it is doing when it reads it, toned `warning` when every one of those
       launches always runs; left out when nothing overlaps.
   - Each kind-of-work page, `layout` `rows`: a `diagram` `Flow` whose nodes are the skills the
     page's starting skills reach directly, each labelled with its name and its role in a few words,
     and one node per launch named for the subagents it starts and how many, such as `Plan
     attackers ×3 per round`. Edges are labelled `invokes`,
     `launches` (from the skill to its launch node) or `borrows`, and `steps` say in order how the
     work moves through them; a skill reached only further down appears in the `Skills` table
     alone. Then a `tree` `How it runs`, `open_depth` 2, one root per skill the page's work starts
     from, nested as the Usage tree is but with every step, each with `detail` what it does and
     `meta` the most subagents beneath it when there are any, and, on a step that repeats, an entry
     saying how many rounds and what each repeat reruns, toned `warning` when it reruns everything;
     its entries' `details` open the same write-ups. A launch's entry here also names in its `meta`
     the capability level its subagents run at, from `subagent-matrix`, or says it is unstated.
     Then a `table` `Skills` with the columns Skill, Role and
     Started by, and `details` holding each row's skill write-up, so clicking a skill opens it.
   - **Skill write-up**: the dialog a reader opens to learn what a skill does and how it spends
     subagents and rounds. An `outline` with `stacked` set and `collapsible` false, `title` the
     skill's name and `description` what it does and why, in one or two sentences. Each item is a
     label beside a fact that teaches something; an item with nothing to say is left out. Its
     groups:
     - "Summary": "Subagents", the most one run starts and who they are, such as "Up to 16 per
       run: 3 inspectors and 1 checker each round, plus 1 safety inspector for sign-in or payment
       changes", or "None"; and "Review rounds", how many and what ends them, or "None, it runs
       once".
     - "How it runs": one item per step in order, labelled "<n>. <step>", `detail` what happens,
       and `points` for what that step spends: one per launch, "<count> <role> read <scope> and
       <what they look for or produce>", and, on the step that repeats, how many rounds, what ends
       them and what each repeat reruns.
     - "Modes", only for a skill whose menu declares more than one: one item per choice, its
       label beside what it changes about the subagents, rounds or steps.
   - **Entry write-up**: an `outline` with `stacked` set and `collapsible` false, `title` the
     entry's label and `description` what it does in a sentence. Its groups, each only when it has
     something in it: "Why subagents start", one item per launch at or beneath the entry, saying
     what those subagents exist to catch or produce; and "Good to know", what a reader tuning the flow
     should know, such as the condition that starts a launch, what a later round reruns, a scope
     another skill also reads in the same run, or a count that grows with the size of the change.
   - `references` make each skill's name a link to its whole `SKILL.md`, at the commit read,
     wherever the page's text names it; outline items carry no `links`.
6. **Deliver** through `use-dashboard`, as a dashboard of a subject that outlives the session, so an
   existing page with the same title and topic, the repository, is updated when this session can
   update it. Name what is incomplete, if anything, in one line.

## Interrogate

Walk a skill or a flow with the user and change what they decide should change. The goal is skill
flows that start fewer subagents and read less without missing what the step exists to catch.

1. **Set the scope.** Context the user gives — a skill, a kind of work, a concern such as review
   rounds — sets it. With none, ask the **Scope** menu.
2. **Map it** as **Workflow** steps 1 to 4 do, recording every launch, its scope and condition, and
   every review loop with what a later round reruns.
3. **Pick the steps worth a question.** A step is worth one when changing it would change how many
   subagents start, how much they read, or what a review can miss: a launch, a review loop and what
   its later rounds rerun, a scope wider than the step's job, a scope another skill reads in the
   same run, or a launch that always runs where a condition would do. Every other step passes
   without a question, and the report lists them in one line.
4. **Ask one question at a time, most subagents first**, through the question tool, and wait for
   its answer before asking the next. Each says when the flow runs — what starts it and how often in
   a task, such as "once per pull request, when its task finishes, and again for each follow-up" —
   then what the step does in a sentence: the skill and step, how many subagents, what they read and
   for how many rounds. Every fact it states is read from the lines that state it before it is
   asked, so a question never rests on a repeat or a gap the sources do not have. Its choices are keeping it as it is and one or two concrete changes,
   such as fewer subagents, a narrower scope, a condition on the launch, fewer rounds, or later
   rounds that rerun only the reviewers a repair affects. The recommended choice comes first, with
   its reason in what it saves and what it could miss.
5. **Record every question** with `session-ledger` as a `question` entry when it is asked, with
   its options and recommendation, and mark it answered with the user's words.
6. **Make the agreed changes** through `edit-skill`, as one change across the skills they touch,
   then report per skill what changed and what was kept.

## Guardrails

- Never invoke or dispatch a workflow the dashboard shows; reading its sources is the whole job of
  Show, and of Interrogate until the user answers.
- Show draws the current flow only. A proposed change, or a recommendation, appears only when the
  request asks for it, as an outline beside the flow, never drawn into it.
