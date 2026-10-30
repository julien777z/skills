---
name: interactive-skill
description: Give a skill a command-line-style menu of what it can do. Skip the menu when the request already says which choice the user wants; otherwise ask, and accept the answer in any common form (a number, a name, "y" for yes). Use as a dependency of any skill that declares a menu, whenever that skill starts or reaches a point where the user picks what happens next.
short_description: 'Offer a skill’s choices as a menu, skipped when the request already says.'
---

# Interactive Skill

Works like a command-line prompt for a skill. The calling skill declares its menu once. Each run
then takes the user's choice from the request when the request already gives one, and asks only
when it does not.

## Declaring A Menu

A calling skill lists `interactive-skill` under its `## Dependencies` and declares each menu in a
section named for it, as a fenced `yaml` block:

```yaml
prompt: What do you want to do?
kind: choice
choices:
  - id: plan
    label: Plan a trip
    detail: build a day-by-day itinerary
    aliases: [itinerary, schedule]
    when: the request asks to plan, schedule or lay out days
  - id: pack
    label: Packing list
    detail: list what to bring for the weather and activities
    aliases: [packing, luggage]
    when: the request asks what to bring or pack
    available: the trip has dates and a destination
```

| Field | Meaning |
| --- | --- |
| `prompt` | The question, written as the user will read it. |
| `kind` | `choice` (pick one, the default), `multi` (pick any number), `confirm` (yes or no) or `text` (a typed answer). |
| `choices` | For `choice` and `multi`: each has an `id`, a short `label`, and optionally a one-line `detail`, other words that name it in `aliases`, `when` (the kind of request that already picks it), and `available` (the condition under which it is offered). |
| `default` | For `confirm` and `text`: the answer an empty reply takes, if any. |
| `example` | For `text`: one sample answer, shown under the prompt. |

## Resolve From The Request

1. **Drop what is not available.** Leave out every choice whose `available` condition does not hold
   now. When exactly one choice remains, that is the choice; when none remains, say what is missing
   and stop.
2. **Read the request.** Take the invocation's arguments and the user's words that led to it. The
   request picks a choice when it names its `id`, `label` or an alias, or matches its `when`.
   Arguments count the same way as a typed reply below, so `2` or `y` already answers.
3. **Skip the menu when the request settles it.** That happens when it picks exactly one choice of a
   `choice` menu, names the choices of a `multi` menu, says yes or no to a `confirm`, or gives the
   answer to a `text`. Open the reply with one line saying what was taken and why, such as
   "Running **Packing list**, from your request.", and continue with it.
4. **Ask otherwise.** That covers a request that picks nothing, or more than one choice of a `choice`
   menu. Never guess between choices, and never take one only because it is first or most common.

## Ask

- **Use the harness's question tool when the menu fits it.** Claude's question tool holds two to
  four options. Each available choice becomes an option, its `label` as the label and its `detail`
  as the description. A `multi` menu allows several selections, and a `confirm` offers Yes and No.
  A reply typed into the tool's free-text answer is matched as below.
- **Otherwise write the menu in chat**, exactly in this shape. That covers a harness with no
  question tool, a menu longer than the tool can hold, and a `text` prompt. Then end the turn;
  nothing that depends on the answer runs before it arrives.

```markdown
**What do you want to do?**

1. Plan a trip — build a day-by-day itinerary
2. Packing list — list what to bring for the weather and activities

Please pick a choice to proceed.
```

| `kind` | Last line of the menu |
| --- | --- |
| `choice` | `Please pick a choice to proceed.` |
| `multi` | `Pick one or more, such as 1,3, all or none, to proceed.` |
| `confirm` | No list; the prompt ends with `(yes/no)`, then `Please answer yes or no to proceed.` |
| `text` | No list; `Example: <example>` when there is one, then `Please type your answer to proceed.` |

Number the choices from 1 in their declared order. Leave out a choice that is not available, so a
number never points at a choice that cannot run.

## Match The Reply

Trim the reply, ignore case and surrounding punctuation, then take the first rule that matches:

| Reply | Means |
| --- | --- |
| A number shown, alone or as `#2`, `2.`, `option 2`; or an ordinal such as `second`, `the last one` | That choice. |
| A choice's `id`, `label` or alias | That choice. |
| The start of exactly one choice's `id`, `label` or alias, at least three letters | That choice. |
| For `confirm`: `y`, `yes`, `yeah`, `yep`, `yup`, `sure`, `ok`, `okay`, `go ahead`, `do it`, `1` | Yes. |
| For `confirm`: `n`, `no`, `nope`, `nah`, `don't`, `2` | No. |
| For `multi`: items separated by commas, spaces or `and`, each matched as above; `all` or `everything`; `none` or `nothing` | Those choices; every choice; no choice. |
| For `text`: anything else, or nothing when there is a `default` | The answer as typed, or the default. |
| `cancel`, `stop`, `never mind`, `quit` | Run nothing, and say that nothing ran. |

- **A reply that matches no choice, or more than one, gets the menu again.** Put this line above
  it: "That did not match a choice. Please reply with a number from 1 to <n> or a choice's name."
  Never pick for the user; repeat this until a reply matches.
- **A reply that asks something else is a new request.** The menu is dropped, and the calling skill
  is not continued.

## Returning To The Caller

Hand back the chosen `id` or `id`s, `yes` or `no`, or the typed text, and whether it came from the
request or the reply. The calling skill runs that branch with no further question about it.

## Guardrails

- Never run a choice the user's request or reply did not select, and never offer one whose
  `available` condition does not hold.
