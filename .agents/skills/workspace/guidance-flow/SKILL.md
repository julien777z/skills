---
name: guidance-flow
description: "Show how the guidance runs — which skill invokes, spawns or borrows from which, which rules each reads, and where subagents start — as a dashboard with one page per category of skills and a page of every rule; or interrogate a skill or a whole flow, asking the user about each substantial step with a recommendation for using fewer subagents to better effect, and applying what they agree; or compare the current flows with a proposed set of skills and rules. Use when asked how skills or rules run, what calls what, which rules a skill reads or which skills read a rule, where subagents spawn, for the flow of one skill or category, to review, tune or interrogate skill flows, or how a change to the skills or rules compares with what runs now. It never runs the workflows it shows."
short_description: 'Show how the skills and rules run, or interrogate a flow to tune it.'
---

# Guidance Flow

The map covers the guidance as it runs: the skills, and the rules they read. A rule is a file under
`.agents/rules/`, `.agents/global.md`, or `.agents/project.md` where the repository has one.

## Dependencies
- `interactive-skill`
- `use-dashboard`
- `edit-skill`
- `session-ledger`
- `subagent-matrix`

## Modes

When the request does not select a mode, offer this menu through `interactive-skill`.

```yaml
prompt: What do you want to do with the guidance flows?
kind: choice
choices:
  - id: show
    label: Show
    detail: build the dashboard of how the skills run and which rules they read
    aliases: [dashboard, map, view]
    when: the request asks how skills run, what calls what, which rules a skill reads, or where subagents start
  - id: interrogate
    label: Interrogate
    detail: walk a skill or flow with you, step by step, and tune it
    aliases: [configure, tune, review the flow, audit the flow]
    when: the request asks to question, configure, tune or change how a skill or flow runs
  - id: proposed
    label: Proposed flow
    detail: compare the current flows with a proposed set of skills and rules and show what changes
    aliases: [compare, diff, before and after]
    when: the request asks how a change to the skills or rules compares with what runs now
```

**Show** follows **Pages** and **Workflow**; **Interrogate** follows **Interrogate**; **Proposed
flow** follows **Proposed Flow**.

## Scope

Interrogate asks which flows to cover, when the request names none, with a menu built from the
categories **Pages** finds: every flow first, then one choice per category page, in page order.

```yaml
prompt: Which flows should I interrogate?
kind: choice
choices:
  - id: all
    label: Every flow
    detail: every category, most subagents first
  - id: <category>
    label: <the category's page title>
```

## Pages

The dashboard's `icon` is `diagram`. After `Overview` comes `Usage`, the view across every skill
of where subagents start, what they read and how often review repeats, then `Rules`, every rule
with how it loads and which skills read it, then one page per category of skills, holding the
skills that category's flows run through and the rules they read. A skill sits on the page of its
category and appears on another only as a node that page's flow reaches.

- **The categories are the skills repository's own when it has them**: the grouping its skills are
  filed under, such as a folder per category in its skills directory, or the category its catalog
  or README gives each skill. Each becomes a page titled with the category's name as words, in the
  order the repository lists them, or alphabetically when it sets none.
- **When the repository has none, choose them by kind of work**, so each page follows one flow from
  the skill a person or workflow starts to where it hands over, such as execution (a task from plan
  to completion), review (the review loop before a merge), delivery (a draft pull request to its
  merge) or guidance (editing and delivering skills).
- A category whose skills invoke, launch and borrow nothing gets no page, and the Overview's
  `notes` name it in one line. Its skills still count in **Skills and rules mapped**, appear as
  nodes on the pages that reach them, and are named in the `Rules` table beside each rule they read.
- Each page's `icon` is the one from `use-dashboard`'s icons that best names its category, every
  one different and none of `diagram`, `overview`, `chart`, `legal`, `settings` or `compare`, which
  the dashboard and its other pages use. A page's starting skills are the skills in its category that no other skill
  in that category starts and that a person, or a skill in another category, starts.

A request that names one skill or one category builds `Overview`, `Usage`, `Rules` and only the
pages it reaches. Pages follow the categories as the sources stand when they are read.

## Workflow

1. **Locate the sources.** Find the current canonical skills and rules, from the skills
   repository's checkout or the installed canonical links, never by assuming the working directory
   holds them. Record the repository, the commit read, whether any source file is uncommitted, the
   categories **Pages** finds, and every rule file.
2. **Read each page's flow.** From each page's starting skills, read the entry points and follow
   every invocation, subagent launch and borrowed rubric the flow reaches, including conditional
   ones, such as a security review that runs only for some changes. Read `subagent-matrix` and its
   capability reference for who each launch the flow describes uses. Note, for every claim, the
   `SKILL.md` lines that state it.

   While reading a page's flow, record every rule a skill on the page reads: each rule its text
   cites, by name, by file or by section, such as "the GitHub rule's **Pre-Push Gate**", with the
   section cited and the lines that cite it. From each rule file's frontmatter and headings, record
   how it loads — always, when `alwaysApply` is true; by file pattern, with its `paths`; or only
   when a skill cites it — and its sections, each with what it governs in a few words. The agent
   running this skill reads the rule files' frontmatter and headings itself, once.

   The reading is split between at most two read-only subagents, launched under
   `subagent-matrix`, each taking about half the pages and reading them itself without starting
   subagents of its own. A scope of one or two pages takes one. Each returns, per page, the map
   facts, the rule citations and the `SKILL.md` lines that state them. Merging their maps, checking the claims and
   building the spec stay with the agent running this skill.
3. **Map it.** For each page, record the order, the choices, the parallel streams, the repair and
   rerun loops, and which skill owns each step.
   - **Connections.** Keep four kinds apart: one skill invoking another, one launching subagents,
     one borrowing another's criteria, and one reading a rule, recorded as `reads`. Invoking a
     skill, borrowing its rubric or reading a rule starts no extra agent.
   - **Rules.** For each rule, record how it loads, its sections, and the skills that cite it with
     the section each cites; a rule no skill cites is still recorded, with how it loads.
   - **Launches.** Record each subagent launch with its owner, role, capability, whether it always
     or only sometimes runs, how many run per round, and whether it recurs. A launch always runs
     when it runs on every run of the step that starts it. When one skill runs another's phases,
     the launch belongs to the skill whose run starts it. For every launch, also record the scope
     each subagent reads: the change's diff, only what changed since the last review, the whole
     files it touches, related files such as callers and siblings, one area of the repository, or
     the whole repository.
   - **Counts.** A count that depends on the work is recorded as what it grows with, such as "1
     per area touched" or "1 per finding", with the most the skill allows when it sets one, such
     as "1 per area, 3–6". A total shows the usual figure and what adds more, such as "~6, more
     per finding", never the most or a sum of every worst case, and a count with no limit is
     recorded as a "No limit set" gap. These are structural counts, never measured time or cost.
   - **A skill's own run.** For each skill on a page, record its run in order: each step it takes,
     the subagents that step launches with how many and what they do, and its review rounds —
     whether it has any, how many it allows, what ends them, and what a later round reruns. Record
     every other loop the same way: a repair loop that fixes and checks again, a wait that polls
     until something finishes, and a retry, each with its cap, what ends it, what a repeat reruns,
     and the loop it runs inside, if any.
4. **Recheck the sources** before building. When a file the map cites changed while you read, map it
   again; never show a mix of two snapshots as current. A change to a file the map does not cite
   leaves it standing, and links stay on the commit read. A source that is missing or still
   changing makes the map incomplete, and the page says which connection is unknown.
5. **Build the spec** for `use-dashboard` as the [dashboard spec reference](references/dashboard-spec.md)
   describes under **Show**.
6. **Deliver** through `use-dashboard`, as a dashboard of a subject that outlives the session, so an
   existing page with the same title and topic, the repository, is updated when this session can
   update it. Name what is incomplete, if anything, in one line.

## Proposed Flow

Compare two sets of skills and rules: the **current** flows, the default branch as freshly fetched, and the
**proposed** flows, the set the request names — a branch, a pull request, a commit, or the
checkout's uncommitted edits — or, when it names none, the checked-out branch. The page answers one
question: what would change in how the skills run and which rules they read. It shows the change, not two whole dashboards.

1. **Map both sets** as **Workflow** steps 1 to 4 do, recording each set's repository, commit and
   uncommitted state. List the skills whose package differs between them, with the skills added and
   removed, and the rules whose file differs, with the rules added and removed. A rule whose text
   moved into a skill is listed as removed, with where it went; a rule split into several files is
   listed as changed, with the new files. Map every page whose flow reaches one of those skills,
   through an invocation, a launch or a borrowed rubric, or cites one of those rules, on either
   side, so a caller whose totals the change moves is mapped too; on the current side, read only
   those pages. **A neighbor that only inherits is mapped as well**: every skill that reads a
   changed rule or cites a changed section of a skill appears on its page with what changes for
   it, found from the citations **Workflow** step 2 records and from the readers a scope statement
   the invocation supplies for the change lists. A changed rule that loads always or by file
   pattern maps to the pages whose steps its changed sections govern — the steps that make the
   decision a section changed, found by that decision's subject — whether or not a skill there
   cites it, and never to every page because it loads everywhere.
   Split the reading by side between at most two read-only readers, one current and one proposed.
2. **Compare the maps.** For each skill on a mapped page, record what was added, removed or changed:
   a skill, a step, a launch, a loop, an invocation or a borrow, a count, a scope or a cap, or a
   decision: what an agent decides or does at a step, though no launch, loop or count moves, such
   as who decides, whether it acts or asks, keeps or removes, stops or continues, or what a rule
   the step reads requires of it. A change of wording that changes none of these is no change. An
   inheriting skill's record names the step that reads the changed text and what that step
   decides on each side, or that nothing changes for it. For each changed rule, record the sections
   added, removed, changed or moved, and the skill or rule each moved to; a section whose
   requirements all arrive elsewhere is a move, never a removal beside an addition.
3. **Build the spec** as the same reference describes under **Proposed flow**.
4. **Deliver** as **Workflow** step 6 does, as its own dashboard beside the one Show builds.

## Interrogate

Walk a skill or a flow with the user and change what they decide should change. The goal is to cut
excess usage: subagents and reading that buy little, in steps that run often. A step that fires
rarely, or a saving of a few subagents across a whole pull request, is not worth weakening what the
step exists to catch.

1. **Set the scope.** Context the user gives — a skill, a category, a concern such as review
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
4. **Show the questions on the dashboard.** Deliver the dashboard as the dashboard spec reference's
   **Show** section and **Workflow** step 6 build it, with a page `Interrogation`, `icon`
   `settings` and `layout` `rows`, right after `Overview`, its `subtitle` what the interrogation is for, such as "Deciding, step by step, which
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
   choice taken and what changes, never a quote of the user's reply). Publish the page before the first question, with that question's
   node `warning`, and again after each answer, with the answered node `done` and the next question's
   node `warning`, so the page always shows where the conversation is.
5. **Ask one question at a time, in the order the run reaches them** — skill by skill, and within a
   skill from its first step to its last — through the question tool, and wait for its answer before
   asking the next. Each question opens with its place and the sequence's total, such as "Q7/19",
   beside the page's highlighted node. Each says when the flow runs — what starts it and how often
   in a task, such as "once per pull request, when its task finishes, and again for each follow-up"
   — then what the step does in a sentence: the skill and step, how many subagents, what they read
   and for how many rounds. How often the step runs decides the recommendation, never whether it is
   asked: for a step on every task, pull request or round, a change that saves a modest number of
   subagents can be the recommended choice; for one that fires rarely, such as a security review of
   trust-boundary code or the review of a plan, keeping it is recommended unless the change only
   removes reads that add no coverage. Every fact it states is read from the lines that state it
   before it is asked, so a question never rests on a repeat or a gap the sources do not have. A
   question about a step that reads a rule names the rule and what its cited section requires of the
   step. Its choices are keeping it as it is and one or two concrete changes, such as fewer
   subagents, a narrower scope, a condition on the launch, fewer rounds, or later rounds that rerun
   only the reviewers a repair affects. The recommended choice comes first, with its reason in what
   it saves and what it could miss.
6. **Record every question** with `session-ledger` as a `question` entry when it is asked, with
   its options and recommendation, and mark it answered with the user's words.
7. **Make each agreed change as soon as it is answered** through `edit-skill`, on one draft pull
   request every answer of the interrogation joins: push the first change and open the draft then,
   never holding it until the remaining questions are answered. Report per skill what changed and
   what was kept.

## Guardrails

- Never invoke or dispatch a workflow the dashboard shows, apart from the read-only readers step 2
  launches under `subagent-matrix`; reading the sources, skill and rule files alike, is the whole
  job of Show, and of Interrogate until the user answers.
- Show draws the current flow only. A recommendation or proposed change reaches a Show dashboard
  only when the request asks for it, as an outline beside the flow, never drawn into the diagram;
  **Proposed Flow** marks its changes in its own diagram.
