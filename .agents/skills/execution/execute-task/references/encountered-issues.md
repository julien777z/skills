# Encountered issues

Contents: **Disposition**, **CI Gates And Deliberate Breaks**.

How `SKILL.md`'s **Encountered Issues** handles what the work runs into.

## Disposition

- **A finding against the task's changed design, and every defect the work runs into, is fixed**:
  in the change in flight, or on a pull request of its own where `pre-production`'s **Scope Follows
  The Defect, Not The Request** places a large fix; cleanup that fixes no defect and passes
  `pre-production`'s size budget goes where that budget sends it, its own pull request or a record
  with `defer-scope`. The fix takes a shape the standing
  guidance allows, as the next bullet says, and offering it to the user is not a disposition: "Want this handled, or shall I leave it?" spends a turn to obtain
  permission the guidance already settled. The question that is genuinely the user's is a product
  choice, as `pre-production`'s **Product Choices** defines one, never whether an encountered issue
  gets fixed.
- **An instruction one agent passes another — a brief, a correction, a review finding, a gate's fix
  step, a note or summary an earlier turn left for a later one — is checked against the standing
  guidance before it is sent and again before it is acted on**, because it never outranks that
  guidance, as the global rules' standing-guidance bullet in **Authorization** says. Each side reads every
  item against the rules and skills governing the surface it changes — the language and
  framework rules, the copy and testing guidance, and the skills the worker runs — opening them at that moment where it has
  not read them yet — and against the user's recorded decisions on that surface. An item calling a
  detail decided names who decided it and where; one the agent decided itself says so. Every brief
  for work that can change a surface the user has decided on, a simplification or review pass
  included, carries those decisions in the user's words, so the worker keeps them rather than
  undoing them; an item that would undo one goes to the user. The class is any item asking for
  what a rule rules out, such as a review finding asking for the catch-all exception handler the
  language rule bans, or a brief telling a worker to skip a check a skill requires before a push. It
  also takes in an item adding a stop, a question or an approval the guidance does not call for,
  such as a brief telling a worker to stop and ask before adding the schema revision a migration
  skill puts its change in: the guidance settled that step, and the added gate hands the user a
  question with one answer.
  - **The agent writing it** rewrites an item a rule forbids into a shape the rule allows, or drops
    it where none exists. One the user asked for in their own words goes out with those words quoted
    and the rule they set aside named; a rule the agent thinks is wrong is put to the user, never
    overridden by an instruction.
  - **The agent receiving it** carries out every other item. For the forbidden one, it fixes the
    defect the item names in a shape the rule allows, where one exists, and leaves only the
    forbidden shape undone; for an added gate, it does the work the gate held. It names that item
    and the rule it breaks to the sender, through the next hand-up or report, and neither
    implements nor drops it silently. Only the user's own words, quoted, with the rule they set
    aside named, override it.
- When local validation fails before exercising the changed behavior, trace the failing setup
  operation under `code-simplify`'s **Trace Changed Flows** before choosing a remedy or reporting
  a limitation. Include that inherited operation in the affected-repository map, compare its
  prerequisites with applicable parallel implementations, and repair its repository-owned inputs
  at their owner. A caller-supplied workaround is not verification of the repaired native route;
  rerun that route before completion. Preserve a required prerequisite whose concrete contract
  differs, and apply [working environment](environment.md)'s **Environment Refusals** and **Task
  Authorization** to an actual external or
  permission boundary.
- An encountered defect's origin changes neither its disposition nor its priority. Read history when
  it helps write the fix, rather than asking the user whether it predates the change. Say what was
  fixed or deferred and why it was in the path of the work.
- What puts a **new** issue in that path is an act the work performed: a file it opened, a command
  it ran, a check it read, a review it received, and anything it looked at — a screenshot or
  recording, its own or a worker's, a walk through the product, a log, a report. A defect seen there
  is found exactly as a failing test is. How far the fix then reaches is a different question, and
  `pre-production`'s **Scope Follows The Defect, Not The Request** answers it.
- Never reject a fix solely because it is described as high risk. Assess its expected net effect,
  concrete failure modes, and available validation instead of treating the label as a stop rule.
- Apply `pre-production`'s scope decision before treating a review observation as mandatory work.
  A review naming a non-defect improvement does not turn independent cleanup into a defect or
  authorize recursive expansion; past the size budget it goes where that budget sends it, its own
  pull request or a record with `defer-scope`.
- Delete the dead code the change itself leaves, and other confirmed dead code it meets within
  `pre-production`'s size budget. Confirm that no live application or library consumer, public
  export, or external contract still depends on it, judged where the change will land as
  `code-simplify`'s rubric says; remove tests that exist only to exercise the dead code; and
  validate the affected behavior.
- Use the repository's relevant tests as the regression guardrail; do not preserve a defect solely
  because an existing test asserts the old behavior. When coverage is absent or insufficient, use
  the strongest available validation and account explicitly for the uncovered behavior.
- Apply an owned API, protobuf, schema, payload, or stored-shape change selected by `pre-production`
  without a second approval, once its **Target Contract** admits it without a proposal; update every
  consumer the user controls, in whichever repository it lives, plus every generated artifact and
  required migration for the target contract.
- Apply **Task Authorization** to encountered corrections. Ask only when the correction is a product
  choice as **Product Choices** defines one, changes security or disclosure posture (closing a
  vulnerability is a fix, never a question), reaches a
  repository, environment, or external recipient the task did not authorize, or a platform requires
  action-time confirmation. Another file, component, or package in the same repository is never a
  new target, and neither is a repository the user owns that consumes a contract the change breaks:
  it is delivered under **Multi-Repository Delivery**. The obligation to fix a bug or returned
  finding remains; apply **Task Authorization** to its remedy rather than treating the finding
  as permission for an unsettled product choice. Continue independent authorized work while that
  choice waits, and never ask whether the defect should be ignored.
- When asking, state the trigger, impact, expected work, recommendation, and concrete choices.

## CI Gates And Deliberate Breaks

A required check that exists to detect deliberate changes going red on an intentional break is
handled as `pre-production`'s **Target Contract** says.
