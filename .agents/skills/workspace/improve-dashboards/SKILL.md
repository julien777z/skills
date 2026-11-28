---
name: improve-dashboards
description: Improve the dashboard skills by using their dashboards — render each skill that delivers a dashboard from real session data, go through every page as its reader would, hovering, clicking and opening dialogs, judge whether it serves the skill's purpose and is easy to use, and fix the renderer, its shared components and rules, or the owning skill until satisfied, then report the changes per skill. Use when the user asks to improve, judge or review the dashboards. Run only when the user asks for it.
short_description: 'Render, use and improve every dashboard skill until satisfied.'
---

# Improve Dashboards

Run `self-improvement-protocol` over every dashboard the skills deliver. This skill adds what is
specific to dashboards.

## Dependencies
- `self-improvement-protocol`
- `use-dashboard`
- `use-browser`
- `session-ledger`
- `edit-skill`

## Which Dashboards

Every skill that declares `use-dashboard` as a dependency, unless the user names fewer. Invoking
this skill is the user's request for each of them, a skill that runs only when asked included.

## Data

- **Real data, from one session.** Build each dashboard from the current session's records. When
  the current session holds no task that gives a dashboard meaningful data, pick one earlier session
  that does and build every dashboard of the pass from it alone, never mixing sessions, so the
  pages agree with each other.
- **Copy, never touch.** Copy that session's ledger, transcript extracts and earlier specs into this
  run's working folder and build from the copies. Never write that session's ledger, its specs or
  the output paths its dashboards were delivered to; render to paths of this run's own.
- Build each spec as the dashboard's skill says, from the current text of that skill, never from a
  spec an earlier run built under older rules.

## Run

Run `self-improvement-protocol` over every dashboard, rendered as its skill builds it, and judge
the dashboards against each other as well as each against its own skill's purpose: the same fact
is drawn, named and formatted the same way on every dashboard, and a part two skills each define,
such as a board of plan steps or a list of pull requests, is defined once in `use-dashboard` and
reused. A wrong value in this run's spec is fixed in the spec too. Deliver each final dashboard
through `use-dashboard` and report the protocol's **Output**.
