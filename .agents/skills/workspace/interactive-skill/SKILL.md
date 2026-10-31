---
name: interactive-skill
description: Give a skill a command-line-style menu of what it can do. Skip the menu when the request already says which choice the user wants; otherwise ask, and accept the answer in any common form (a number, a name, a short prefix, or "y" for yes in a yes-or-no question). Use as a dependency of any skill that declares a menu, whenever that skill starts or reaches a point where the user picks what happens next.
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

1. **Leave out what is not available.** Drop every choice whose `available` condition does not hold
   now; the rest are numbered from 1 in their declared order, and every number below means that
   numbering, whether or not the menu is shown.
2. **Read the request.** Take the invocation's arguments and the user's words that led to it.
   The calling skill's own name or command never picks a choice; only its arguments and the user's
   other words count. Arguments are matched exactly as a reply is under **Match The Reply**, so `2`
   or `y` already answers. Otherwise the request picks a choice when it names its `id`, `label` or an alias as a
   whole word or phrase, ignoring case, or when the user's main ask, read as a whole rather than
   for keywords, is what the choice's `when` describes. A name the request rules out, as in "don't
   review it", picks nothing.
3. **Stop when the request picks a dropped choice.** Say what its `available` condition is missing,
   and run nothing.
4. **Skip the menu when the request settles it.** That happens when it picks exactly one choice of a
   `choice` menu, names the choices of a `multi` menu, says yes or no to a `confirm`, or gives the
   answer to a `text`. It also happens when only one choice is available. Open the reply with one
   line saying what was taken and why, such as "Running **Packing list**, from your request." or
   "Running **Plan a trip**, the only choice available.", and continue with it.
5. **Ask otherwise.** That covers a request that picks nothing, or more than one choice of a
   `choice` menu. In the second case, open the menu with one line naming the choices the request
   picked and saying that one runs at a time. Never guess between choices, and never take one only
   because it is first or most common.

## Ask

- **Use the harness's question tool when the menu fits it.** Claude's question tool holds two to
  four options. Each available choice becomes an option, its `label` as the label and its `detail`
  as the description. A `multi` menu allows several selections, and a `confirm` offers Yes and No,
  its Yes labelled Approved when it approves a plan or proposal.
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

| `kind` | Shape |
| --- | --- |
| `choice` | As above. A choice without `detail` is its label alone. Last line: `Please pick a choice to proceed.` |
| `multi` | As above. Last line: `Pick one or more, such as 1,3, all or none, to proceed.` |
| `confirm` | No list: `**<prompt> (yes/no)**`, a blank line, then `Please answer yes or no to proceed.` |
| `text` | No list: `**<prompt>**`, then `Example: <example>` when there is one, then `Please type your answer to proceed.` |

## Match The Reply

Trim the reply and ignore case and surrounding punctuation. Then take the first rule that matches:

| Reply | Means |
| --- | --- |
| `cancel`, `stop`, `never mind`, `quit`; for `text`, only when it is the whole reply | Cancelled: run nothing, and say that nothing ran. For `confirm` this differs from `no`, which runs the caller's "no" branch. |
| A number in the numbering, written as digits (`2`, `#2`, `2.`, `option 2`, `2nd`), as a word (`two`, `second`) or as `last`, with an optional leading `the` and trailing `one`, `option` or `choice` | That choice. |
| A choice's `id`, `label` or alias | That choice. |
| The start of an `id`, `label` or alias, at least three letters, when every one it starts belongs to the same choice | That choice. |
| For `confirm`: `y`, `yes`, `yeah`, `yep`, `yup`, `sure`, `ok`, `okay`, `go ahead`, `do it` | Yes. |
| For `confirm`: `n`, `no`, `nope`, `nah`, `don't` | No. |
| For `multi`: items separated by commas, spaces or `and`, each matched as above; `all` or `everything`; `none` or `nothing` | Those choices; every choice; no choice. |
| For `text`: anything else, or nothing when there is a `default` | The answer as typed, or the default. |

- **A reply that is a new request is not an answer.** A full sentence, question or instruction that
  names no choice and is about something other than the menu drops the menu, and the calling skill
  is not continued; the new request is handled as it stands.
- **Any other reply that matches no choice, or more than one, gets the menu again**, never a pick
  made for the user, as often as it takes. Put one line above it, or in the question text when the
  question tool asks: "That did not match a choice. Please reply with a number from 1 to <n> or a
  choice's name." for `choice`, the same ending "…, all or none." for `multi`, and "That did not
  match. Please answer yes or no." for `confirm`.

## Returning To The Caller

Hand back the chosen `id` or `id`s, `yes` or `no`, the typed text, or `cancelled`, and where it
came from: the request, the reply, or the only available choice. The calling skill runs that branch
with no further question about it, and stops without running any branch on `cancelled`.
