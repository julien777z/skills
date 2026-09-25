# Code Review Rubric

What a review judges by: what anchors a finding, how a finding is validated, how it is rated, and
what fix mode owes each confirmed finding. `SKILL.md` says how the review is run. Simplification
borrows the `code-simplify` skill's rubric; Security borrows the reviewed repository's local
`security-audit` rubric when that skill exists. Neither borrows the other skill's workflow.

## Scope

Anchor a finding to a changed line when that line introduces, inherits, exposes, or depends on the defect. A real defect with no faithful changed-line anchor is still in scope: anchor it to its exact current line, mark it `OUTSIDE_DIFF`, and report it without pretending an unrelated changed line caused it. "Pre-existing" describes when a defect arrived, not whether it is worth fixing, and a review that steps over one because the blame is older leaves the reader with a known defect and no record of it.

## Validation

Deduplicate findings describing the same underlying issue, then validate each one against the diff. Validators are told to refute: the burden is on the finding to survive.

**Every finding resolves to CONFIRMED or refuted. There is no third verdict.** A defect either exists or it does not, and which one is a fact about the code that reading the code settles. "Could not verify" is a statement about how far the validation got, not about the code, and reporting it hands the reader an unfinished investigation to run themselves — the one thing the review was for.

So when a validator cannot decide from the diff, it keeps going until it can: read the full file and every caller, read the library or SDK source the finding depends on, check the lock file for the resolved version, read the rule the finding cites in full, search the history for when the line was introduced, and run the code — construct the input, execute the branch, and observe the result. Uncertainty is a signal to look at something specific that has not been looked at yet. Name that thing and look at it.

Only one situation ends validation undecided, and it is never uncertainty about the code: the answer turns on intent that exists nowhere in the repository — which of two contracts the author meant, whether a behavior change is wanted. Do not invent a verdict for that and do not report it as a finding with a hedge. Ask the user, in the shape step 8 uses for an ambiguous fix.

Drop anything refuted, including anything a full investigation leaves unsupported. A finding that survives only because nobody finished checking it is not evidence of a defect.

This bar does not move with effort. A cheaper level runs fewer validators over a smaller cohort, so it searches less; the inline validation at `low` and `medium` still resolves every finding it keeps.

Drop these outright:

- Something that looks like a bug but is not.
- Pedantic nitpicks a senior engineer would not raise.
- Failures a linter, typechecker, compiler, or formatter would catch. Assume CI runs them; do not run them here.
- General code-quality gaps such as missing tests, weak documentation, or generic security hardening, unless a rule requires them.
- Rule violations explicitly silenced in the code, for example by an ignore comment.
- Deliberate configuration or design choices with no demonstrable failure.
- Self-resolving transitional states and speculative compound failures.
- Behavior changes that are intentional and part of the change's purpose.

Apply `pre-production` when validating a finding that changes a contract. A break that policy
authorizes is a cost of the fix, not a refutation of the finding.

**Refuting a finding can surface a different one.** Refutation often turns on a distinction the reviewer missed — one value meaning two different things, a fallback that exists only because a caller structurally cannot supply what the signature asks for, a special case held together by convention. The original finding is still refuted and still dropped; the design that made it refutable is a finding of its own. Raise it as one, anchored to the changed line that depends on it, and let it run through rating, reporting, and fix mode like anything else.

Every retained finding must be actionable, anchored to either the faithful changed line or the exact current defect line, and state when it fails. Never attach an `OUTSIDE_DIFF` finding to an unrelated changed line merely to satisfy a reporting tool.

## Severity And Categories

Assign severity by realistic trigger likelihood, not the worst imaginable outcome:

- **Critical** — data loss, security or auth bypass, crash, or broken core behavior.
- **High** — likely defect in normal use.
- **Medium** — real but conditional, narrowly scoped, recoverable, or limited in impact.
- **Low** — valid minor or rare-edge issue. Keep at most the three most important.

Reserve High for failures common in normal use. Prefer a short, high-confidence result over exhaustive speculation.

Assign each finding a category slug: `correctness`, `security`, `efficiency`, `simplification`, `test-coverage`, or another short kebab-case slug that fits. Never label a concrete defect a `simplification`.

## Fix Mode

**Every CONFIRMED finding gets fixed.** Surviving validation is what makes a finding legitimate, and a legitimate finding left unfixed in fix mode is the review failing at the only thing fix mode is for. "Out of scope", "pre-existing root cause", "larger than this diff", and "the obvious fix conflicts with another rule" are descriptions of the work, not permission to skip it. Report a finding as unfixed only after item 4's escalation, item 5's size bar, or the acceptance gate's second flag below, and never as a first response to difficulty.

**Severity ranks the work; it never selects which work happens.** A confirmed finding is fixed whether it is critical or cosmetic, and whether or not it touches the theme the change was opened for. "Not critical", "not what this PR is about", "lower value than the rest", and "the important ones are closed" are the same skip wearing different words — every one of them ends with a defect the review found, named, and then left in the code. Rank by severity to decide what to fix *first*, then keep going until the list is empty.

**A round is not finished while confirmed findings remain.** Do not close a round by reporting the fixes made alongside a list of confirmed findings left open; that list is the round's unfinished work, not its summary. The only finding that may outlive the round is one that item 4's escalation genuinely could not settle, that item 5 defers on size, or that the acceptance gate flagged twice, and it is reported as a blocker or a record with what it needs, not as a leftover; on a pull request confined to agent configuration a second flag is instead disposed of by the run, as the gate's **Bounds** say.

"A test patches or imports that symbol" is likewise never grounds to skip or soften a fix. Tests follow application code, not the reverse: when the fix moves, renames, or absorbs a symbol that tests patch, mock, or import, updating those patch targets and fixtures is part of the fix, and the affected suite is rerun to prove the reworked tests still pass.

**Size.** Size may keep a confirmed finding out of this round only when the finding is not a defect. A confirmed defect — anything the system does that a reader would call broken: wrong output, a lost write, a lost notification, a crash, an exhausted budget, work it cannot finish in useful time, a resource nothing bounds, work a restart throws away, as `acceptance-gate`'s admission question defines it — is fixed here whatever its size, whatever shape its fix takes, and whatever its blame or blast radius; needing a migration is how such a fix is written, never grounds to record it, and "the result is still correct" never makes a slow or unbounded path something other than a defect. For anything else the bar is a genuine multi-file redesign whose need is arguable — a boundary moved across packages, a sweep over many call sites somebody could reasonably decline — not a fix that is merely awkward or touches code the diff did not. Below that bar the finding is fixed here. At or above it, record the scope through the repository's deferral mechanism so it outlives the review, and name the record in the report: a finding described only in the report is not deferred, it is dropped. That mechanism's admission gate decides whether the scope may be recorded at all; a refusal naming fix or do means the finding is fixed here, and one naming close is recorded cancelled with its reason and reconsideration criterion.

## A Fix Inherits The Intent

**A fix inherits the change's intent, not only the repository's standing rules.** A change that exists to remove a shape — a hand-maintained field-name list, a disclosure flag, a duplicated declaration, a forwarding layer — has made that shape a defect everywhere, including in code this review is about to write. A fix that reaches for it closes the finding and reopens the thing the change was for, and it reads as correct precisely because the rule it breaks is the one the diff is still in the middle of establishing.

Read what the change is removing before writing the fix: its deletions say it more reliably than its description. Then take the remedy the change itself would take. Narrow a model by declaring less rather than subtracting a field-name set from it. Derive a set from the declaration that already carries it rather than restating the names. Extend the mechanism the change introduced rather than standing a second one beside it. Where the obvious remedy is the shape being removed, the obvious remedy is the wrong one.

This governs which of several correct fixes to write; it never excuses leaving a finding unfixed. "The change meant to do that" is not a disposition, and a defect the change itself introduced is still fixed here. What the intent rules out is the fix that puts back what the change just deleted — and where a finding genuinely cannot be fixed without reintroducing that shape, the conflict is real and never goes into the code: a fix `acceptance-gate` has flagged twice is reverted and recorded through the deferral mechanism with both flags as its reason, and a conflict on the change's own purpose goes to item 4's escalation, except on a pull request confined to agent configuration, where the gate's **Bounds** leave it with the run.

**When a fix redirects control flow, diff it against what it displaced.** A fix that routes an input to different code than before — a new dispatch key, a changed handler registration, a removed fallback, a reordered branch, a narrowed or widened type — inherits everything the old path did, not only the part the finding named. Read the displaced implementation first: it is usually short, and it is the specification the fix is replacing. Then send the same input through both paths and compare the complete observable result — status, body, headers, side effects, logs — rather than the one field the finding was about. A fix verified only on the field it targeted is how a review ships a regression in a field nobody looked at, and the next round pays for it. The regression test accompanying such a fix asserts that whole observable surface for the same reason.
