# Dashboard Spec

Contents: **Show** (the spec **Workflow** step 5 builds), **Proposed flow** (the spec **Proposed Flow** step 3 builds).

## Show

The spec for `use-dashboard`:

- `title` `Guidance Flow Dashboard`, `topic` the repository's name, `icon` `diagram`, and `subtitle` "How the skills run and
  which rules they read, from <repository> at <short commit>.", with `references` linking the repository and the commit.
- `metrics`: **Skills and rules mapped**, its `value` both counts, such as "62 skills · 14
  rules"; **Subagents in a typical task**, the usual figure for the run of
  the skill that carries a task from start to merge, or of the skill a person starts most often
  when none does, `detail` "from start to merge, before findings add more"; **Skills that start
  subagents**, `detail` "of <n> mapped"; and **Launches with no limit**, the "No limit set" gaps,
  `detail` "where usage can grow unchecked".
- `Overview`, `icon` `overview` and `layout` `rows`, read at a glance:
  - a `table` `By category` with a row per page and the columns Page, What it covers (a few
    words), Subagents per run (the usual figure and what adds more, such as "~6, more per finding") and
    Loops (how many of each kind, such as "3 review · 2 repair · 1 wait", or "None"). Each row's
    `details` opens an outline of that page's loops, one item per loop titled "<skill>: <what
    repeats>" with its cap as `meta` and what ends it as `detail`. The table never lists a
    page's skills: its page shows them;
  - an `outline` `Gaps in the sources`, `expanded` false, its groups the kinds of gap — "No limit
    set", "No capability level", "Unclear who does it", "Unclear order or route" and "Other",
    each only when it has items — with one item per gap: `title` the gap in a few plain words,
    such as "Style reviewers have no maximum", `tag` the skill it sits in, and `detail` one or
    two sentences on what is open and why it matters, with no line numbers;
  - `notes` `How to read the flows`, one line each for an invocation arrow, a launch arrow, a
    borrowed-rubric arrow and a `reads` arrow, from a skill to a rule it reads, as their labels
    show them, then one line naming each category left without a page.
- `Usage`, `icon` `chart` and `layout` `rows`, across every skill the dashboard maps:
  - a `tree` `Where subagents go`, `open_depth` 2, one root per skill a person starts directly,
    most subagents first. Its `figure` is the subagents one run usually starts, everything
    beneath it counted, such as "~6 subagents"; its `meta` names what adds more, such as "more
    per finding and per area", or "fixed" when nothing does. The usual figure counts, for one
    round each, only launches whose every ancestor always runs, a skill a step runs only under a
    condition counting as one that does not; a count that depends on the work counts at its stated
    least, or at one. No figure sums a worst case across the whole graph, and none reads "0+": a
    range shows as its range, such as "2–4", and a count that only varies shows what it varies
    with, such as "1 per finding". Beneath a skill, its steps in order, labeled "<n>. <step>"
    with the same `figure` and `meta` for what sits beneath them; beneath a step, each
    skill it runs, nested the same way wherever it runs so every total counts it, and each
    launch as an entry labeled with its role, `figure` its count, such as "3", "2–4" or "1 per
    finding", and `meta` its rounds and what it reads, such as
    "up to 3 rounds · diff and whole touched files", and `detail` what the subagents do, what a
    later round reruns, and the condition it runs under when it only sometimes runs. A launch
    that always runs is toned `warning`. Every entry's `details` open what it is: a skill's,
    its skill write-up; a step's or a launch's, its entry write-up. A step with no subagents anywhere beneath it is left
    out, so the tree holds only where subagents start;
  - a `tree` `Loops`, `open_depth` 2, one root per kind of loop the skills run, each only when
    one exists: `Review loops`, rounds of reviewers; `Repair loops`, fixing and checking again;
    `Wait loops`, polling until something finishes; and `Retry loops`. A root's `meta` counts
    its loops and the usual subagents a round starts. Beneath a root, each loop, labeled
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
- `Rules`, `icon` `legal` and `layout` `rows`: a `table` `Rules` with a row per rule, the
  always-loading rules first, and the columns Rule (its name as words, such as `GitHub rule` or
  `Global rules`), Loads ("Always", "By file pattern: <patterns>" or "When cited"), Read by (the
  skills that cite it, or "No skill cites it") and What it governs (a few words). Each row's
  `details` is an `outline` titled with the rule's name, its `description` when the rule's
  frontmatter says to read it, with one item per section of the rule: `title` the heading,
  `detail` what the section governs in a sentence, and `meta` the skills that cite that section.
- Each category page, `layout` `rows`: a `diagram` `Flow` whose nodes are the skills the
  page's starting skills reach directly, each labeled with its name and given its role in a few
  words as its `detail`, and one node per launch labeled with the short name of the subagents it
  starts, such as `Draft reviewers`, with how many and how often, such as "×3 per round", in its
  `detail`, and one node per rule the page's skills read, labeled with the rule's name as
  words, such as `GitHub rule` or `Global rules`, with what it governs in a few words as its
  `detail`. Edges are labeled `invokes`,
  `launches` (from the skill to its launch node), `borrows` or `reads` (from a skill to a rule
  it cites), and `steps` say in order how the
  work moves through them; a skill reached only further down appears in the `Skills` table
  alone. A rule keeps the diagram readable by appearing once: one that most of the page's skills
  cite, or that loads always and none of them cites, such as the global rules, has a single
  `reads` edge from the page's first starting skill, and the `steps` say it applies throughout;
  a rule that loads by file pattern and that no skill on the page cites stays on the `Rules`
  page alone. Then a `tree` `Scenarios`, `open_depth` 1: two to four stories this work commonly
  meets, each one concrete run told in order, such as a review that finds nothing, a lens that
  finds a bug, or findings that keep coming for three rounds. A root names the story. Beneath it,
  what happens in run order: each round or step, such as "Review round 1", holding one leaf
  per subagent it starts, named for its role, such as "Reviewer"; and each event that changes
  the path, labeled with a short name such as "Unused import" and told in its `detail`, such
  as "Reviewer reports an unused import", toned `warning`, holding
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
- **Every label is the short name of what it marks**, and so is the title of the dialog it
  opens, such as `Draft reviewers` or `Style lens`. A count, condition, source or
  explanation goes in the entry's `figure`, `meta`, `detail` or `description`, never in its name,
  and a name is never cut short to fit.
- **Skill write-up**: the dialog a reader opens to learn what a skill does and how it spends
  subagents and rounds. An `outline` with `stacked` set and `collapsible` false, `title` the
  skill's name and `description` what it does and why, in one or two sentences. Each item is a
  label beside a fact that teaches something; an item with nothing to say is left out. Its
  groups:
  - "Summary": "Subagents", the usual figure one run starts, what adds more and who they
    are, such as "~4 per run, more for sign-in or payment changes: 3 inspectors and 1 checker
    each round, plus 1 safety inspector for those changes", or "None"; and "Review rounds", how
    many and what ends them, or "None, it runs once".
  - "How it runs": one item per step in order, labeled "<n>. <step>", `detail` what happens,
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
- `references` hold one entry per mapped skill and one per mapped rule: `text` the skill's name,
  or the rule's name as words, exactly as the page's text writes it, and `url` its whole
  `SKILL.md` or rule file at the commit read. A skill or rule named anywhere in a tree, an
  outline, a diagram's `steps` or a `changes` item is then a link, so every such text writes the
  name in that one form; outline items carry no `links`.

## Proposed flow

The spec is built as **Show** builds it, with these differences:

- `title` `Guidance Flow Dashboard`, `topic` "Proposed flow", `subtitle` "Current <short commit> →
  proposed <ref>.", and `references` linking both commits beside the entry per mapped skill and
  rule, which links to the proposed side's file, or to the current side's for one the proposed
  side removed. Each added, removed or changed
  skill's reference opens `details` instead of a link: a `changes` section titled with the skill's
  name, described by what changed in one sentence, one item per change step 2 recorded for it —
  each step, launch, loop, invocation, borrow, count, scope, cap or decision — its `current`
  what the current side does and its `proposed` what the proposed side does instead, and `links` to the
  skill's `SKILL.md` on each side that has it. A skill that only inherits a change opens the
  same `details`, with one item per inherited decision, and one that reads the changed text with
  nothing changing for it stays a link, as an unchanged skill's reference does. Each
  added, removed or changed rule's reference opens `details` the same way: a `changes` section
  titled with the rule's name as words, one item per section step 2 recorded for it, its
  `current` what the current side holds and its `proposed` where the proposed side puts it, and
  `links` to the rule's file on each side that has it.
- Every `changes` and `outline` item on the page that says what the current side does and what
  the proposed side does instead puts each in `current` and `proposed`, never in one `detail`
  sentence: an added item sets only `proposed`, a removed one only `current`, and `detail` holds
  only what belongs to neither side.
- `metrics`: the four **Show** names, each `value` "<current> → <proposed>", such as "~25 →
  ~12", and `detail` what moved it in a few words.
- The pages run in this order: `Overview`, `Changed`, `Usage`.
- `Overview`: a `table` `What changed` with a row per mapped page and the columns Page,
  Subagents per run (current → proposed), Loops (current → proposed) and Change (a few words),
  each row's `details` an outline of that page's changes, changed rules included; one `changes`
  section `Skills and rules`, `counted`, one item per added, removed or changed skill, with
  `group` "Skills", per skill that only inherits a changed decision, with `group` "Inherits",
  and per added, removed or changed rule, with `group` "Rules", each with what changed in one
  sentence, a removed or split rule naming where its text went; and `notes`
  naming in one line the pages with no change, which the `Changed` page leaves out.
- `Usage`: a `table` `Subagents per run`, one row per skill a person starts that changed, with
  the columns Skill, Current, Proposed and What changed, most subagents saved first; a `changes`
  section `Loops`, one item per loop added, removed or changed, its `current` and `proposed` the
  cap and what a round reruns on each side.
- `Changed`, with `icon` `compare`, holds one `tabs` section `Changed flows`
  with a tab per mapped page, labeled with the page's name and in the order the Show dashboard orders them, so the
  reader moves between the changed categories on one page. Each tab holds a `diagram` `Flow` of
  the proposed flow with the current flow's removed parts left in, each node and edge, rule
  nodes and `reads` edges included, carrying
  `change` `added`, `removed` or `changed` and no `change` when unchanged, with `steps` saying
  what changed in order; then a `changes` section `What changed`, one item per change the diagram
  marks; then a `tabs` section `How it runs` with the tabs `Proposed` and `Current`, each holding
  that side's **Show** `How it runs` tree, so the reader opens one side at a time. After
  the category tabs comes a tab `Rules`, left off when no rule changed, holding a `changes`
  section `Rule moves`: one item per section step 2 recorded, `name` "<rule>: <section>",
  `group` the rule's name as words, `current` where the section sits and what it holds, and
  `proposed` where it moved or what it holds instead. Scenarios, the `Skills` table, the `Rules` page and a page per category are left out.
