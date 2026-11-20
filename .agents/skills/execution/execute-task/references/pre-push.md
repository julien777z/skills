# Pre-Push Gate

Every push goes out once the pre-push checks below pass, on a draft and on a pull request ready for
review alike. Follow an explicitly selected workflow’s own declared check sequence and delivery
constraints where it specifies them; nothing holds committed work on one machine — not a gate, review or simplification
pass pending on it, an integration merge, or a plan that orders one first. The one exception is
commits that `lock-revision`'s **After Locking** hold keeps local until the user lets revisions
resume. `code-simplify` and `acceptance-gate` do not run per push; this skill's workflow and `review-pass`
set when they run. A fix pushed for a flag a review or gate raised is pushed once
the agent that made it has re-read the changed lines against the flag and rerun the checks covering
that code; that recorded check is what other skills mean by an increment's **Pre-Push Gate**
verdict. It never closes the flag: the review's next round or, for a gate's flag, the fresh gate
`acceptance-gate`'s **Bounds** require does.

Read this skill's [verification reference](verification.md) before planning test runs or briefing
an implementation worker. Its **Verification Cadence** governs tests, builds, browser walkthroughs and reviews, including
pre-push checks. Deferred feature verification does not hold an intermediate push and remains
required afterward, and a suite still running holds none either: that section's superseded-run
bullet says what happens to it. Run the relevant batch after the feature is complete, then the required final
checks before delivery; retain evidence that the change has not invalidated.

- **Required checks use CI’s commands and scope, at the verification checkpoints above.** Read
  the workflow files that trigger on a pull request and run every checking job that can run
  locally — lint, format, type checks, build, tests, generated-output drift, docs or coverage
  checks — with the job's own command and scope, plus any check a skill in use requires. Do not
  restart the batch for each push; retain results whose code and inputs remain unchanged. Project
  guidance that lists those commands is a shortcut to the workflows, never a
  substitute; where the two disagree, the workflow is right. A job that needs a hosted service or a
  running stack, or is too slow to run before every push, joins the slow verification below and is
  named in the report. Room on this machine never leaves a job to its hosted run: a shortage of
  disk, memory or ports is recovered as the global rules' local-stack bullet says, and the job runs
  here. Only a hosted service or credentials the session lacks, each established as the
  verification reference's cannot-run bullet says, or runner-specific behavior does.
  A non-essential check left red on findings the change did not write, as `pre-production`'s
  essential-checks bullet classifies them, holds no push; invoke `pre-production` for those
  findings and handle them as that bullet says.
- **A local variant of a CI check is not that check**, and each of these passes locally and fails
  in CI: lint or type checks scoped to the changed files, where CI's whole-tree run finds an
  untouched caller of a signature the change altered; a formatter or linter in write
  mode, which rewrites what CI's check mode reports; a tool at a version or with a config other than
  the one CI resolves; a job left out because the diff looks unrelated to it, such as a
  generated-output drift check or a whole-tree check that every shared component has a docs page.

Before each push, list the exact adjacent line pairs where setup, a guard, transformation, side effect,
or return meets the next phase without the blank line required by the global code-layout rule.
For changed Python files, `acceptance-gate`'s `python_rule_findings.py` script lists the candidate pairs.
Fix every listed boundary in the lines the change writes or edits, and elsewhere in the changed files
within `pre-production`'s incidental size budget, as the global code-layout rule says; an unrelated
bug or a passing formatter does not satisfy this spacing check.

- **Commit each small coherent step and push it as soon as its checks pass**, and at least every
  five minutes of work — a function and its callers updated, a test brought to pass, one finding
  fixed — never at the end of a unit or task. Define coherence against `pre-production`'s
  complete target boundary, not the latest edited files: required consumer updates, superseded
  owners and declarations, generated contracts and retained-data migration are implementation,
  never later cleanup. An intermediate push may preserve ongoing work; it neither narrows the
  remaining obligation nor qualifies that feature for completion, review delivery or rollout.
  A push is what lets the user review and test the work, and the only copy that
  outlives the machine: a recycled container or an ended session takes every commit and edit no
  remote holds.
- **Nothing outside the change holds a push, a check or a walkthrough, or becomes a question about
  pushing or merging.** A dependency
  still in review in another repository, an unreleased package version, a sibling pull request not
  yet merged, CI expected to stay red until one of those lands: the branch consumes the
  dependency's pull-request branch, or its default branch once merged — in the manifest, the
  lockfile and any workflow checkout, as the global rules' version-reference bullet allows while
  developing — or builds on a same-repository sibling's branch as the GitHub rule's branch bullets
  set out, and pushes. Every build, test and walkthrough runs against that checked-in reference,
  never a local copy the manifest does not name. A consumer that cannot build until its dependency
  merges is a manifest still naming the default branch: point it at the pull-request branch, never
  ask for the dependency's merge or report the consumer blocked on it. Which branch it consumes,
  and a red check that dependency explains, are
  surfaced in user chat under the GitHub rule's independent publishing context rather than waited on; adopting
  its maintained delivery target is named work for when the dependency merges.
- **No edit sits uncommitted through a long wait outside the checks.** Before the slow verification
  below, a background worker, CI on the pushed head, or a question to the user, bring the work to a
  coherent step, commit it, and push it; the checks' own runs are part of the push, not such a wait.
- **Delegated edits run at this cadence.** A brief handing a worker edits states it, names the
  branch the worker pushes to — the branch of the pull request the work continues, under the GitHub rule's **Branches and Pull Requests** — and names the exact files to change, under `subagent-matrix`'s **Dispatch**. The
  worker pushes each step once its checks pass and reports the branch and head. The brief has the
  worker fix every defect it meets, in the product or the repository's tooling, and report as left
  alone only cleanup past `pre-production`'s size budget and any item
  `pre-production`'s scope bullets leave to the user. The delegating agent reads that head under
  the global rules’ **Reported Outcomes** before any dependent work starts. The worker
  ends with nothing uncommitted and nothing unpushed beyond the one exception above,
  never amends or rebases a pushed commit, and
  its report names the branch and head.
- **Pull requests stay draft until the authorized merge gate readies them**, so these pushes may
  start no test jobs. Readiness can enqueue duplicate hosted jobs without changing the head;
  `merge-gate` decides whether completed exact-head evidence is equivalent before it waits for
  fresh coverage. The local checks above are what stand between a push and hosted validation.
- **The order is change, checks, push, then the slow verification**: a browser walkthrough, a full
  or end-to-end suite, a run against a service without the change, root-causing a failure seen
  along the way — anything slow or needing a running stack. What it finds goes out as fix pushes, each once its checks pass.
- **Pushed is not done**: the change is reported done only once that verification has passed.
