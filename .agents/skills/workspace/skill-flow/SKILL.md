---
name: skill-flow
description: "Show how the skills run as a dashboard: one page per kind of work (execution, review, delivery, guidance, doctors, deferrals), each a diagram of which skill invokes, spawns or borrows from which, where subagents start and how many, read from the current canonical guidance; or interrogate a skill or a whole flow, asking the user about each substantial step with a recommendation for using fewer subagents to better effect, and applying what they agree. Use when asked how skills run, what calls what, where subagents spawn, for the flow of one skill or kind of work, or to review, tune or interrogate skill flows. It never runs the workflows it shows."
short_description: 'Show how the skills run, or interrogate a flow to tune it.'
---

# Skill Flow

## Dependencies
- `interactive-skill`
- `use-dashboard`
- `edit-skill`
- `session-ledger`

## Modes

When the request does not select a mode, offer this menu through `interactive-skill`.

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
| Review | `check` | `review-pass`, with `review-loop`, `council`, `acceptance-gate` and `security-audit` |
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
   "1 per area, 3–6". A total shows the usual figure and what adds more, such as "~6, more per
   finding", never the most or a sum of every worst case, and a count with no limit is recorded as a
   "No limit set" gap. A launch always runs
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
   - `metrics`: **Skills mapped**; **Subagents in a typical task**, the usual figure for
     `execute-task`'s run from start to merge, `detail` "from start to merge, before findings add
     more"; **Skills that start subagents**, `detail` "of <n> mapped"; and **Launches with no
     limit**, the "No limit set" gaps, `detail` "where usage can grow unchecked".
   - `Overview`, `icon` `overview` and `layout` `rows`, read at a glance:
     - a `table` `By kind of work` with a row per page and the columns Page, What it covers (a few
       words), Subagents per run (the usual figure and what adds more, such as "~6, more per finding") and
       Loops (how many of each kind, such as "3 review · 2 repair · 1 wait", or "None"). Each row's
       `details` opens an outline of that page's loops, one item per loop titled "<skill>: <what
       repeats>" with its cap as `meta` and what ends it as `detail`. The table never lists a
       page's skills: its page shows them;
     - an `outline` `Gaps in the sources`, `expanded` false, its groups the kinds of gap — "No limit
       set", "No capability level", "Unclear who does it", "Unclear order or route" and "Other",
       each only when it has items — with one item per gap: `title` the gap in a few plain words,
       such as "Bugs reviewers have no maximum", `tag` the skill it sits in, and `detail` one or two
       sentences on what is open and why it matters, with no line numbers;
     - `notes` `How to read the flows`, one line each for an invocation arrow, a launch arrow and a
       borrowed-rubric arrow as their labels show them.
   - `Usage`, `icon` `chart` and `layout` `rows`, across every skill the dashboard maps:
     - a `tree` `Where subagents go`, `open_depth` 2, one root per skill a person starts directly,
       most subagents first. Its `figure` is the subagents one run usually starts, everything
       beneath it counted, such as "~6 subagents"; its `meta` names what adds more, such as "more
       per finding and per area", or "fixed" when nothing does. The usual figure counts, for one
       round each, only launches whose every ancestor always runs, a skill a step runs only under a
       condition counting as one that does not; a count that depends on the work counts at its stated
       least, or at one. No figure sums a worst case across the whole graph, and none reads "0+": a
       range shows as its range, such as "2–4", and a count that only varies shows what it varies
       with, such as "1 per finding". Beneath a skill, its steps in order, labelled "<n>. <step>"
       with the same `figure` and `meta` for what sits beneath them; beneath a step, each
       skill it runs, nested the same way wherever it runs so every total counts it, and each
       launch as an entry labelled with its role, `figure` its count, such as "3", "2–4" or "1 per
       finding", and `meta` its rounds and what it reads, such as
       "up to 3 rounds · diff and whole touched files", and `detail` what the subagents do, what a
       later round reruns, and the condition it runs under when it only sometimes runs. A launch
       that always runs is toned `warning`. Every entry's `details` open what it is: a skill's,
       its skill write-up; a step's or a launch's, its entry write-up. A step with no subagents anywhere beneath it is left
       out, so the tree holds only where subagents start;
     - a `tree` `Loops`, `open_depth` 2, one root per kind of loop the skills run, each only when
       one exists: `Review loops`, rounds of reviewers; `Repair loops`, fixing and checking again;
       `Wait loops`, polling until something finishes; and `Retry loops`. A root's `meta` counts
       its loops and the usual subagents a round starts. Beneath a root, each loop, labelled
       "<skill>: <what repeats>", most subagents first, `meta` "up to <n> rounds · ~<m> per round,
       more per <what>", or "no cap" when nothing bounds the rounds, and `detail` what ends it and
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
     alone. Then a `tree` `Scenarios`, `open_depth` 1: two to four stories this work commonly
     meets, each one concrete run told in order, such as a review that finds nothing, a lens that
     finds a bug, or findings that keep coming for three rounds. A root names the story. Beneath it,
     what happens in run order: each round or step, such as "review-loop round 1", holding one leaf
     per subagent it starts, named for its role, such as "Reviewer"; and each event that changes
     the path, such as "Reviewer reports a missing empty-list check", toned `warning`, holding
     what it sets off — a validator, a fix, a fresh gate — with an outcome that settles it toned
     `good`. A step that starts none says "In process" in its `meta`, and a round that reruns fewer
     subagents says why, such as a lens retired or a slice the fix left untouched. Every node with
     subagents beneath it has `figure` their count, so each root's figure is the sum of its leaves,
     and a node with none beneath it, a story included, shows no count. Every entry below a story
     has `details`, an `outline` with `stacked` set and `collapsible` false, `title` its label and
     `description` what that kind of subagent, round or step does, and one group "In this scenario":
     the story; for a subagent, the step that started it and the subagents running alongside it;
     otherwise what it is part of and why it is there; what comes before and after it in the run;
     and its subagent count;
     the counts and conditions come from the sources, never from a guess. Then a
     `tree` `How it runs`, `open_depth` 2, one root per skill the page's work starts
     from, nested as the Usage tree is but with every step, each with `detail` what it does and
     `figure` the usual subagents beneath it when there are any and `meta` what adds more, and, on a step that repeats, an entry
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
     - "Summary": "Subagents", the usual figure one run starts, what adds more and who they
       are, such as "~4 per run, more for sign-in or payment changes: 3 inspectors and 1 checker
       each round, plus 1 safety inspector for those changes", or "None"; and "Review rounds", how
       many and what ends them, or "None, it runs once".
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

Walk a skill or a flow with the user and change what they decide should change. The goal is to cut
excess usage: subagents and reading that buy little, in steps that run often. A step that fires
rarely, or a saving of a few subagents across a whole pull request, is not worth weakening what the
step exists to catch.

1. **Set the scope.** Context the user gives — a skill, a kind of work, a concern such as review
   rounds — sets it. With none, ask the **Scope** menu.
2. **Map it** as **Workflow** steps 1 to 4 do, recording every launch, its scope and condition, and
   every review loop with what a later round reruns.
3. **Pick the steps worth a question.** A step is worth one when changing it would change how many
   subagents start, how much they read, or what a review can miss: a launch, a review loop and what
   its later rounds rerun, a scope wider than the step's job, a scope another skill reads in the
   same run, or a launch that always runs where a condition would do. So every subagent launch and
   every review loop in scope gets its own question, a launch two pages share asked once; none is
   skipped because no saving is apparent, since keeping it is then the recommended choice. Every
   step that starts no subagent and repeats nothing passes without a question, and the report lists
   them in one line. Every question is picked before the first is asked, so the page's progress
   shows the whole set from the start.
4. **Show the questions on the dashboard.** Deliver the dashboard as **Workflow** steps 5 and 6
   build it, with a page `Interrogation`, `icon` `settings` and `layout` `rows`, right after
   `Overview`, its `subtitle` what the interrogation is for, such as "Deciding, step by step, which
   subagents are worth what they cost, so the skills start fewer without missing what they catch.",
   its `status` the count of questions still open and its `progress` how many are
   decided, `label` "Questions decided" and `detail` "<decided> of <total> decided", with one segment per question in the order
   they are asked, toned `done` once answered and `warning` while asked. It holds one `diagram` per skill a
   question concerns, the skill being asked about first so its flow sits right under the progress
   bar, then an `outline` `Decided so far` listing each answer and what it changes once there is
   one, then the other skills in asking order. A diagram holds that
   skill's steps in order, joined by `then` arrows, with each step's launches hanging off it and a
   `runs` arrow to a node for each skill it runs that has a diagram of its own on the page, its
   `detail` what that skill does in a few words and its `target` that diagram's title, so clicking
   it scrolls there, so the questioned
   step is seen beside the rest of the run and where it hands over. Its
   description says what the skill's run does in a sentence, never how to read the colors or that
   nodes can be clicked;
   its `legend` is `[{tone: warning, label: Being asked}, {tone: done, label: Decided}]`. The node a
   question concerns — the launch it questions — carries
   `tone` `warning` while it is asked and `done` once answered, and none before, and its `details`
   is an outline with `stacked` set and `collapsible` false whose groups are "What it does" (when
   the flow runs and what the step does now), "Proposed changes" (each choice, with what it saves
   and what it could miss), "Recommended" (the choice and why) and, once answered, "Decision" (the
   user's words and what changes). Publish the page before each question, with that question's
   node `warning`, and again after its answer, with the node `done`, so the page always shows where
   the conversation is.
5. **Ask one question at a time, in the order the run reaches them** — skill by skill, and within
   a skill from its first step to its last — through the question tool, and wait for its answer
   before asking the next. The question leaves out its number and where it sits on the dashboard,
   since the page's highlighted node shows that. Each says when
   the flow runs — what starts it and how often in a task, such as "once per pull request, when its
   task finishes, and again for each follow-up" — then what the step does in a sentence: the skill
   and step, how many subagents, what they read and for how many rounds. How often the step runs
   decides the recommendation, never whether it is asked: for a step on every task, pull request or
   round, a change that saves a modest number of subagents can be the recommended choice; for one
   that fires rarely, such as a security review of trust-boundary code or the review of a plan,
   keeping it is recommended unless the change only removes reads that add no coverage. Every fact
   it states is read from the lines that state it before it is asked, so a question never rests on a
   repeat or a gap the sources do not have. Its choices are keeping it as it is and one or two
   concrete changes, such as fewer subagents, a narrower scope, a condition on the launch, fewer
   rounds, or later rounds that rerun only the reviewers a repair affects. The recommended choice
   comes first, with its reason in what it saves and what it could miss.
6. **Record every question** with `session-ledger` as a `question` entry when it is asked, with
   its options and recommendation, and mark it answered with the user's words.
7. **Make each agreed change as soon as it is answered** through `edit-skill`, on one draft pull
   request every answer of the interrogation joins: push the first change and open the draft then,
   never holding it until the remaining questions are answered. Report per skill what changed and
   what was kept.

## Guardrails

- Never invoke or dispatch a workflow the dashboard shows; reading its sources is the whole job of
  Show, and of Interrogate until the user answers.
- Show draws the current flow only. A proposed change, or a recommendation, appears only when the
  request asks for it, as an outline beside the flow, never drawn into it.
