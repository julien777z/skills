# Completion streams

The two streams `SKILL.md`'s **Completion** runs side by side once its checkpoint starts: the
guidance stream and the source stream, with the steps each takes in order.

Contents: **Guidance Stream**, **Source Stream**.

## Guidance Stream

Invoke `process-ledger` for the task's private ledger. It sends the `guidance_correction` batch it
freezes to `edit-skill`'s **Guidance Delivery** route, which the primary agent coordinates so its
review and checks never wait on the source stream. Before a source pull request's **Review the pull
request**, every pending `guidance_correction` entry that rides it, as the GitHub rule's **Branches
and Pull Requests** and `edit-skill`'s guidance pull-request reference set out, in the batch in
flight or the one after it, is pushed to it and passes its source check, as **Guidance Delivery**'s
**Resume the batch** says, so its review pass, history and ready message cover them. An entry
recorded after the batch in flight merged is delivered in the batch frozen once that one is done, so
the source stream then waits for that delivery too, and for nothing else before **Review the pull
request**. Each such entry's skill-test round runs on the head **Review the pull request** accepted,
before **Shape the history**, and a repair it makes returns to review as **Guidance Delivery**'s
**Conclude the skill test** says. A task with none has no guidance stream.

## Source Stream

In this order for each source pull request; an agent-configuration pull request belongs to the
guidance stream:

1. **Review the pull request.** Invoke `review-pass` on the pull request with the intent statement.
   It runs its review loop and one final `acceptance-gate` over the changes no earlier pass
   reviewed, brings in a moved base, and returns the head its final acceptance passed.
2. **Shape the history** with `rewrite-git-history`. The first time a pull request is sent for
   review, rebuild it into one commit per material change. Each later **Completion** of the same
   pull request, after a follow-up, folds every change into the commit it amends through that
   skill's fixup route, or adds a new commit for a new material change, and never rebuilds it again,
   so the commits the user already reviewed keep their shape. A rewrite whose tree proof shows an
   identical tree keeps the acceptance verdict and moves `review-pass`'s reviewed head to the
   rewritten head.
3. **Reconcile the result** with **Product Constraints**' target receipt, updating its sources when
   accepted requirements changed. Verify every requested outcome and every incidental fix, confirm
   tests and relevant validation cover each of them and every simplification, confirm intentional
   contract changes are reflected in the expected behavior, and confirm multi-repository delivery
   artifacts describe only their owning repository. Then build this pull request's ready-for-review
   message, in the shape `SKILL.md`'s **Completion** gives, from `list-prs`, what the run did and
   `review-pass`'s **Output**.
4. **Merge when authorized.** When **Task Authorization** finds the merge authorized, send
   **Reconcile the result**'s message together with the invocation of `merge-gate`, passing the
   accepted head, `review-pass`'s **Checks** results with their commands and head as the behaviors
   local tests already cover, every exclusion it returned with its evidence, and, as its fix rule,
   `review-pass` over each fix's delta since the accepted head and the GitHub rule's **Pre-Push
   Gate**, with each fix folded into its commit through `rewrite-git-history`'s fixup route. It
   inventories exact-head hosted coverage, obtains fresh results only where no equivalent terminal
   coverage exists, fixes what relevant checks report and merges; when it returns, send one line
   with the result it read: the merge, or the gate that holds it. Otherwise send **Reconcile the
   result**'s message; the pull request stays draft.
