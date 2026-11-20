# Product constraints

What `SKILL.md`'s **Product Constraints** applies before an implementation is recommended,
delegated or edited.

## Scope Of Broad Words

Resolve broad words in the context of the outcome the user named before selecting or inventorying
implementation targets. For a contextual follow-up, derive the operational category from the purpose
of the work being changed, not the implementation mechanism shared by candidates. State that purpose,
then check each candidate's actual role against it. A shared filename, label, directory or provider does not make
unrelated automation part of that scope. Broad words such as "every" or "anywhere" quantify that
category; they do not add unrelated categories. Expand only for a required dependency or a user
instruction naming an additional operational category or outcome, never for a broad quantifier
alone or everything a text search happens to return.

## Target Receipt

Before recommending an implementation, asking a question that presupposes one, or delegating its
edits, trace the requested behavior through the caller, transport, configured destination and
execution owner, including the entrypoint that launches or deploys it. Establish where it runs and
which existing capabilities and stored data it can use from configuration and, when available, the
running artifact; a client request alone establishes neither a remote dependency nor missing local
behavior. An independent inventory receives the request, observed evidence and unresolved facts,
not a proposed topology to assume. Its result must reconcile that runtime path before it supports
a new mechanism or a product question. Reconcile the complete
accepted target with the user's instructions, the plan, repository guidance and observed
mechanism; record each settled outcome or constraint with its source and the evidence the proposed
implementation will need to satisfy it. Identify unresolved facts rather than silently replacing
them with an assumption. Compare the proposal against every part of this receipt before selecting
it: resolving the reported symptom or passing a component check cannot excuse violating another
settled requirement. A proposal that fails one is repaired before implementation; a genuinely
unresolved user decision follows **Task Authorization**. Apply the guidance and analogous
implementations below to that choice, not only to the later edit.

For an ownership or scope change, build `acceptance-gate`'s owned-boundary receipt before selecting
the implementation. Follow the runtime binding as well as the source owner: who executes the
operation, which resources it may reach, and which destinations must not receive its components,
data or authority. Carry this receipt into review and deployment verification; a component check
or an internally consistent configuration does not replace it.

## Rules And Analogous Files

Before each edit, read the shared and repository rules governing every surface it reaches — its
language, framework and package, and the kind of thing it changes, such as a form, a query, a test
or interface copy — and nearby analogous files. Where those files disagree, the one departing from
the rest, or from the mechanism that owns the concern, is an encountered issue to fix, never the
pattern to copy. That holds at every point new instructions arrive, not only at the task's start:
a correction, a fix step or a resumed brief that sends the work to a surface whose rules the run has
not read has them read before it is acted on, and having worked in the same language or package
earlier in the run is not having read them. Match the analogous files' code grouping and spacing in
every new or substantially edited file; inspect the complete result beside those siblings before
delivery. A formatter passing is not a substitute for that comparison.
