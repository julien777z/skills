# Working environment

What `SKILL.md`'s **Working Environment** applies to the files a run writes, the browser it drives,
the installed apps it inspects, what the environment refuses, and the steps it cannot take back.

## Working Files

**A task's working files live in `.agent_sources/` at the root of the worktree the task runs in**:
briefs, captures and recordings, rendered pages, specs, findings, scratch scripts and anything else
the run writes for itself or its workers, in folders named for what they hold, such as `briefs/`
and `captures/`; a worker reads its brief there by its absolute path.

- Never in `/tmp` or another system temporary directory, which a restart clears.
- The folder stays out of Git through the repository's local exclude file,
  `$(git rev-parse --git-common-dir)/info/exclude`, never a committed `.gitignore`, its line added
  unasked before the first file lands, even in a task kept to one worktree: that shared file is the
  worktree's own Git state, as its commits are.
- What must outlive the worktree, such as the task's ledger or a lasting dashboard, stays in the
  user's state directory.
- Credentials, sign-in sessions and other secret material never go in a worktree.

## Copies A Sync Service Left Behind

**A copy a file-sync service or the operating system made is deleted once no process, worktree or
session uses it, whatever it holds.** Its name is the original's plus a copy suffix, such as
`budget 2.csv` or `HEAD 2`. Find every one with a name search of the whole tree and its Git
directories (`git rev-parse --git-dir` and `--git-common-dir`), never `git status` or `ls`, which
miss ignored and hidden ones, and delete each before anything stages, stashes or snapshots the tree.
A file, folder, clone or Git entry goes even when it differs from its original or names a commit or
branch the original lacks: nothing is compared, backed up or kept on a branch, since what a session
keeps lives in the original and on the remote. The report names each one deleted.

## Browser Access

- Run browser work in the browser `use-browser` selects: a headless browser the agent runs by
  default, and the user's own browser only when the user asks for it or gives a specific URL to
  inspect or debug. Apply its **Selecting And Binding A Tab** before any page read or action. When
  a CLI attaches to the user's browser, a named CLI session alone does not establish control of the
  selected tab.
- Continue through an appropriate API or CLI when that is more direct. Report a browser-specific
  blocker only when the selected browser's normal recovery paths cannot complete the required
  interaction. A headless browser that cannot run is reported blocked, never moved to the user's
  window.

## Environment Refusals

- **An environment refusal is a route to find, not a blocker to report.** A repository missing from
  the session is attached or cloned as a writable checkout; a host the environment refuses is reached
  through a path it does serve, and a tool that took the refused path is fixed to take the served
  one. Failed routes alone do not establish an external blocker: diagnose the refused contract
  at its owner and check whether owned code, configuration, credentials or lifecycle can satisfy
  it through the supported route. Report an external gate only with the concrete unavailable
  capability, evidence that supported recovery and authorized owned repairs are exhausted, and
  the saved next action when it returns. Repeating the same rejection is not that evidence.
  A command a permission check refuses falls under the next bullet instead, even when it targets
  a host; never bypass that boundary as recovery.
- When recovery installs a required dependency or changes a setting on a machine this task
  provisions, repair the canonical provisioning source as well as the running machine. A one-off
  host change does not fix fresh instances. Verify the corrected setup in a clean applicable
  environment before calling the repair complete. A dependency used only by a disposable test
  belongs in that test's setup rather than the provisioned machine's runtime requirements.
- **A permission check is not a route to find: what it refuses is not attempted again, and the
  decision never becomes the user's.** Use the owner's own routine tool from the start — a package
  manager's cache-clean rather than a raw delete of its cache directory — because that is the
  ordinary way to do the job, not a workaround. Once a permission boundary refuses an action,
  whether a rule the user set or an automated safety check, that outcome is not attempted again by
  any other command, tool or wording, and every other piece of work carries on. Report the refusal
  once, plainly, as a permission the user can grant: what was refused, and that it runs once
  allowed — "The permission check blocked `<command>`; it runs once you allow it, and everything
  else is done." Whether the action is wanted was settled by the guidance before the check ran, so
  the report never asks it or offers options: "Delete X? Yes or no" is the defect.

## Installed Apps

**What an installed app is, is read from its files, never by running it.** Its version, build or
other metadata comes from its bundle or package files, such as a macOS bundle's `Info.plist` or the
package manager's record. Running its binary, passing it a version flag, querying it through a
scripting bridge or opening its About window can each open a window on the user's desktop, and
whether one does changes between releases. Where only running it can tell, run it in an isolated
runner, never on the user's desktop.

## Steps That Cannot Be Taken Back

- **A step that cannot be taken back runs only once the agent has read and judged what its gating
  check found.** A deletion, an overwrite, a push, a merge or a post never shares a command, chain
  or parallel batch with the comparison, diff, listing or test that decides it: a chain follows the
  exit status, and a check can exit 0 while it reports what should stop the step, such as a folder
  comparison listing two differing files before the chained removal deletes the folder. Where one
  command must carry both, it tests the finding itself, such as a count of zero, and stops otherwise.
