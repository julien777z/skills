# Repository helpers

What `SKILL.md`'s **Assigning Work** applies to the repository's `.agents/tools/` folder: where an
operation the task repeats is written, and how what is there is kept.

- **Written once, run from there.** In a repository the owner runs, an operation the task will run
  more than once, or is about to run again, is first written as a helper in `.agents/tools/`,
  created with its folder if missing, committed as source work on the pull request the GitHub rule
  selects for it, and run from there each time. A shell function, heredoc or temporary script is
  not a helper, though a skill's execution checks stay untracked.
- **Maintained by the same authority that adds.** A helper that nearly fits is extended rather
  than copied, one that misbehaves is fixed where it is, and one that is stale, replaced by
  another or no longer saves work is deleted once a search of the repository, its workflows and its
  guidance finds what still calls it, each caller updated in the same change. Each is made in the
  work that meets it and reported as made, never asked about.
