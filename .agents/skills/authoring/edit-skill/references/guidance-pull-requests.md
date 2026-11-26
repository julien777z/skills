# Guidance Pull Requests

How a change to anything under `.agents` is delivered: which pull request it joins, why it never
shares a branch with source work, and where guidance that depends on an open source pull request
goes. What counts as agent configuration and what as source work is the GitHub rule's
**Branches and Pull Requests**.

- **Each session opens its own agent-configuration pull request in each repository.** Select an open
  pull request only when this session's ledger records its creation receipt or the user explicitly
  directs its continuation, and verify its state and scope remotely; a touch or reference receipt,
  matching topic, branch, open state or batch record establishes neither. If none qualifies, open
  one from the freshly fetched default branch; later guidance edits and worker tasks join it.
  Consolidate a duplicate this session opened onto it and close the duplicate, saying where the
  work went; never retarget, close or fold in one this session did not open.
- **Agent configuration and source never share a branch**, even when a guidance change follows the
  source work checked out: sharing holds the guidance behind source review and outside the
  agent-configuration merge permission in the GitHub rule's **Merge Authorization**. A pull request
  found carrying both is split by moving one kind's files onto the pull request of that kind the
  work continues.
- **The one exception is guidance true only once a still-open source pull request merges**: it
  describes behavior that pull request introduces, drops guidance about something it removes, or
  needs a workflow or tool change it carries. It goes on that pull request and merges with it when
  this session created the pull request, as its ledger receipt proves, or the user explicitly
  directs its continuation; a separate agent-configuration pull request this session opened for it
  is folded in and closed, saying where the work went. Otherwise it joins the session's
  agent-configuration pull request and is held until the source pull request merges, in this
  repository or another. A dependency never authorizes continuing another session's pull request
  or opening a second agent-configuration one.
