---
name: legal-review
description: "Review the Terms of Service and Privacy Policy against the law that applies to the company today and against what the site actually does: six parallel legal lenses, a code-versus-document check, an adversarial pass that tries to refute every finding, ranked findings with suggested language, a recommendation for every open question, and only the strictly necessary fixes gated through acceptance-gate and proposed through plan-change. Invoked on a branch that already changes either document, it shows those changes instead, each linked to its commit, and stops. Use only when the user invokes /legal-review or asks for a legal, privacy, terms, or compliance gap review of the published documents."
disable-model-invocation: true
---

# Legal Review

Find where the Terms of Service and Privacy Policy are wrong about the law, wrong about the
product, or silent where they must speak, and turn each gap into language and code the user
can approve.

## Dependencies

- `pre-production` — the site is pre-release; a document, contract, or code change is ordinary
  work, never a reason to soften a finding, and nothing beyond what is strictly necessary before
  launch is proposed.
- `current-changes` — on a branch that changes the documents, the material changes and the commit
  that makes each.
- `text-highlight` — the blocks that show those changes in place.
- `plan-change` — every proposed fix, to documents or code, is presented for approval and then
  implemented under that skill.
- `acceptance-gate` — every proposed fix is judged against the finding it closes and the
  product facts before it enters the plan.
- `defer-scope` — anything consciously left undone after the plan is decided.
- `i-have-adhd` — shape every response.

## Not Legal Advice

The output is a gap analysis for review by licensed counsel. Say so once at the top of the
report and nowhere else. Never present a finding as settled law without a provenance tag, and
never let the caveat soften a finding that the evidence supports.

## Scope

- **Only flows a Business, User, Contractor, or Visitor can reach.** The internal admin API and
  admin site are out of scope: never describe them, never cite them as evidence, never build a
  finding on what staff could do there. A capability the site itself never triggers is not site
  behaviour. That covers every route, service, and screen under the admin application's own
  packages, even when a reading list or a search puts those files in front of you: open them only
  to confirm they are not part of a user flow, and cite nothing from them.
- **A capability in code is not a flow.** An enum member, a step name, an endpoint, or a handler
  proves only that the code can do something. The only evidence a check runs is the job
  specification or call path that a user-reachable flow triggers, and a report describes those
  steps alone. Name each running step by quoting the job specification that lists it; a step that
  appears in a step-order constant, an enum, or a handler but in no user-reachable job
  specification is reported as not run, and never as running. Never propose disclosing a step the
  site does not run.
- The documents are Markdown assets under the public API's legal directory, served by the public
  API and rendered by the customer frontend. When the session holds a frontend checkout, read it
  for the assent surfaces and the served legal pages; when it does not, say which checks were not
  run.
- The full review reads both documents in full with line numbers before anything else, and
  re-reads them after every correction the user gives. **Changes In Flight** reads only the
  branch's diff.

## Strictly Necessary Before Launch

The site has not launched, and `pre-production` governs what a review may ask for: what is
strictly necessary now, and nothing that merely would be good to have.

- A fix is proposed only for a Required finding: the document is false about the product, a clause
  is void under the chosen law, or a notice a law that applies to the company today requires is
  missing. Everything else is Advisable, is reported in the appendix, and never enters the plan
  unless the user asks for it by name.
- **A regime with thresholds is below threshold until a finding shows otherwise.** Revenue,
  consumer counts, data sales, employee counts: name the regime's own threshold and the company's
  figure against it, in the finding, before the word *requires* appears anywhere in it. A company
  with no launch, no revenue and no users is under every such threshold, so the regime is Advisable
  whatever it would demand of a company above it, and a finding that asserts a regime applies
  without that comparison has not made its case and is Advisable too.
- A product surface — a notice on a screen, a consent step, a banner — is added only for a Required
  finding, and the smallest form the law accepts is the one proposed.
- Every proposed change names the Required finding it closes; a change that closes none is not
  proposed.

## Changes In Flight

When the branch's diff against its merge base touches the legal documents directory, the run shows
those changes and stops: no lenses, no findings, no plan. The full review runs only from a branch
that leaves the documents as the default branch does.

1. Run `current-changes` to resolve the material changes and the commit that makes each.
2. For the Terms of Service and then the Privacy Policy, skipping a document the branch does not
   change: one heading per material change that touches it, carrying that change's sentence and
   commit link, followed by `text-highlight` over that change's hunks in that document.
3. Return the shape under **Output** and nothing else.

## Repository legal facts

Read the repository operational profile for established legal and product facts. Treat them as standing owner answers, update them through `edit-skill` when the owner changes one, and do not ask a question the profile already answers.

## Disclosure Standard

- Comparable platforms that pull credit-header data disclose their sources at category level:
  "identity verification agencies, credit reference agencies, public records, data brokers". A
  field-level list of what a provider returns is never a finding.
- Under the CCPA, "collects" covers information received or accessed by any means, whether or not
  it is ever displayed, so stored enrichment triggers a **source-category** disclosure. The
  finding, if any, is a missing category of source in the notice, not a missing field.
- "Match/no-match" is an accurate description wherever only a status is surfaced.
- A statement is a Critical finding only when it is Required under **Strictly Necessary Before
  Launch**. Silence where the law does not require speech is at most Advisable.

## Always Check

Every run states a verdict, pass or fail, on each of these, whatever the lenses report:

- The contractual limitation period against the governing-law statute: under Florida law any
  shortening is void (Fla. Stat. § 95.03), inside arbitration as well as in court.
- The arbitration rule set, fee allocation, and clause registration for individual parties.
- Who is seller of record for subscriptions and which document controls a conflict.
- Whether the URL each document names for itself resolves, and where the documents are linked.
- Whether raw payment credentials are stored, and how the documents describe them.
- Whether every screening or check the documents describe exists in a user-reachable flow.

The report carries these as a table placed before the findings: one row per item, the verdict,
and the document line or code path that decides it.

## Evidence And Citation Discipline

- Every document finding cites the section and line. Every code claim cites a path and line that
  the coordinator re-reads before it is reported. A finding with neither is dropped.
- Every legal citation carries a provenance tag, derived from what was actually done:
  `[settled — last confirmed YYYY-MM-DD]` for a stable reference checked against a primary source
  on that date; `[statute / regulator site]` when the text was fetched this session;
  `[web search — verify]`; `[user provided]`; `[model knowledge — verify]` for everything else.
  Add `[verify-pinpoint]` to any subsection-level cite. `[review]` marks a judgment call for
  counsel, not a factual gap.
- **No silent supplement.** When a source cannot be reached, say what was reached and tag the
  rest; never assert. When something known would change whether a rule applies (a vacated rule, a
  pending appeal, a delayed effective date), surface it as a flagged caveat even when it cannot be
  used.
- Verify a legal fact the user states before building on it, and say so when it differs.
- Read incorporated third-party terms (billing, payments) where reachable; a conflict with them is
  a finding in its own right.
- Public sources checked on every run, each reported as read or unreachable: the state register's
  entity record and fictitious-name search for the operating entity; the current terms of the
  billing and payments providers; the served legal pages at the URLs the documents name.
- **Entity facts are verified or asked, never inferred.** The legal name, state of organization,
  status, principal and registered-agent addresses, officers, and any fictitious name are facts
  about a public record, not about a product name. A finding that a document misstates the entity
  is made only from the state register, tagged `[public register — YYYY-MM-DD]`, or from the owner
  directly.
- Deployment specifications and environment listings carry secrets. Never copy a key, token, or
  credential-bearing value into a report, a finding, or a chat message.

## Workflow

1. **Locate.** Both documents, their version line, the routes that serve them, and every assent
   surface (sign-up consent, invitation and onboarding screens, the terms banner, tax-form
   signing dialogs, bank-account entry). Confirm which frontend checkout, if any, is present.
2. **Fan out.** Launch the six lenses in `references/lenses.md` as parallel, read-only agents:
   contract enforceability; regulated activity; US privacy and consumer protection;
   controller-processor structure and international; code-versus-document consistency;
   cross-document drafting. Each receives both documents, the Scope, the Product Facts, the
   Disclosure Standard, **Strictly Necessary Before Launch**, the Evidence And Citation
   Discipline, the severity scale, the finding template, and its own seed checklist marked
   "verify, refute, or expand". Wait for all six inside the turn.
3. **Consolidate.** Merge, de-duplicate, keep the strongest citation, and rank. Where lenses
   disagree, record both positions under `[review]`.
4. **Refute.** Launch one more read-only agent whose only job is to knock findings down. It
   receives the consolidated list, both documents with line numbers, the Product Facts, and the
   cited code, and answers three questions for each finding: does the document say what the
   finding claims, quoting the line; does the code do what the finding claims, at the cited path;
   and is every premise the finding rests on established by a tagged source rather than assumed.
   A finding refuted on any of the three is dropped, or downgraded with the refutation recorded
   beside it. A finding the agent cannot refute keeps its rank. Wait for it inside the turn; the
   report is not written before it returns, and it carries a "Refutation" section stating what
   this step dropped or downgraded and why, or that it refuted nothing.
5. **Classify each gap** Required or Advisable as **Strictly Necessary Before Launch** defines
   them, and give each an effort-to-close class: document wording, product change, vendor action,
   or process.
6. **Answer every open question.** A question the code cannot settle gets a recommendation with
   its trade-off, never a bare question handed back. "I do not know, what do you recommend?" is
   answered with one recommendation and one alternative. Record the owner's answers into Product
   Facts through `edit-skill`.
7. **Deliver.** Write the report to the scratch directory and send it; summarise the top five in
   chat with one next action. Offer a shareable page in one line; do not publish unasked.
8. **Gate each fix.** Before a fix enters the plan, put it to `acceptance-gate` with the finding
   it closes, the quoted document line, the code it touches, and the Product Facts. A fix the gate
   accepts is planned; a fix it flags is reported with the gate's reason and left out of the plan.
9. **Propose fixes.** Invoke `plan-change` with one plan that carries the accepted document
   redlines and code changes together, ordered by severity. Nothing in the documents or the code
   is edited before that plan is approved. Record declined items through `defer-scope`.

## Commitment Surfaces

Practice drifts forward while documents stand still. Sweep every surface where a commitment is
made and compare each with the documents: the two documents themselves; the sign-up consent text;
the invitation, onboarding, and tax-form screens; bank-account entry; the terms banner;
transactional email footers; and the served legal pages, including whether the URL each document
names actually resolves.

## Severity Scale

- **Critical** — the document states something false about the product, a core clause is void
  under the chosen law, or a mandatory notice is legally ineffective.
- **High** — real regulatory exposure or missing mandatory content.
- **Medium** — enforceability risk or material ambiguity.
- **Low** — drafting.

## Finding Template

```
**T-n · Severity · One-line claim** (§ and line)
- Gap: what is wrong or missing, with the quoted words.
- Why it matters: legal basis with provenance tags; what the code shows with path:line.
- Fix: replacement language or the code change; effort class.
```

## Report Layout

1. Caveat, scope, document version, date, and the entity record: what the state register showed
   about the operating entity, or that it was unreachable and what was asked instead.
2. Executive summary: at most five items in fix order, then what the documents get right.
3. Terms of Service findings by severity.
4. Privacy Policy findings by severity.
5. Code-versus-document table: claim, what the code shows, verdict.
6. Cross-document consistency and drafting.
7. Refutation: each finding the Refute step dropped or downgraded, with the reason, or a statement
   that none was.
8. Appendix: checked and adequate; sources read and sources unreachable; open questions with the
   recommendation for each.
9. Proposed fixes: one list, ordered by severity, of the document redlines and code changes that
   **Strictly Necessary Before Launch** admits, to be presented through `plan-change`, each carrying its
   `acceptance-gate` verdict. The report names both as the route and never leaves a fix as a bare
   recommendation.

## Output

The changes-in-flight route returns exactly this, with a document section only for a document the
branch changes and nothing after the last block:

````markdown
Legal changes on `<branch>` — [<pull request title>](<pull request url>)

## Terms of Service

### <one sentence for the material change> ([<commit>](<link>))

<text-highlight block for that change's hunks in the Terms>

## Privacy Policy

### <one sentence for the material change> ([<commit>](<link>))

<text-highlight block for that change's hunks in the Privacy Policy>
````

Without an open pull request the first line reads `Legal changes on <branch> against <base>`.

The full review returns the report under **Report Layout**.
