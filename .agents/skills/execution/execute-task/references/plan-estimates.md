# Plan estimates

Build a step's estimate from what the run does and waits on, never from how big the change feels,
and round each step to the nearest whole minute, never below 1:

- an edit step — read, edit, commit, push — is 2–3 minutes whatever the file count;
- each run of a local check, test suite or build is its observed duration, counted once per run
  the plan makes;
- an independent gate or review dispatch is 2–4 minutes, and each repair round after it about 3
  more, counted once for each step later steps build on and once for the pull request's
  `review-pass` at **Completion**;
- a round of parallel readers or reviewers is about a minute, and a round of auditing reviewers
  over a tree is 5–10 minutes;
- CI, a merge's check gate, or a deployment the user's request names is the observed duration of
  that job.
