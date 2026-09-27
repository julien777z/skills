---
description: Read when editing skills, rules, agent prompts, provider integration, or generated agent guidance. Keep canonical sources in .agents and preserve portable wording.
alwaysApply: false
---

# Agent Authoring Rules

## Agent And Harness Portability

- This guidance is used with multiple models and agent harnesses. Prefer one provider-neutral
  implementation and one canonical source for skills, rules, and agent prompts.
- When a shared implementation is not possible, support both Claude and Codex explicitly: account
  for how each discovers, installs, and uses the guidance, and verify both paths. Include other
  supported harnesses where the same change reaches them.
- Read the other shared rules relevant to the current repository and task. If a harness does not
  load them automatically, open the applicable files from its user-level rules directory.

## Repository Skills

- Never add `agents/openai.yaml` to a repository skill. Repository skills contain `SKILL.md` and
  only supporting files required by the skill; provider UI metadata stays outside repositories
  and is never propagated.

## Agent Prompts

- In repositories that provide an agent CLI or otherwise interact with agents, store every agent prompt in a dedicated Markdown file rather than inline in application code so it is easy to find, review, and maintain. Application code may load a prompt file and interpolate runtime values into it.

## Generated Agent Outputs

- Never stage generated provider output manually. Only the repository's Agent Sync workflow may generate and commit provider mirrors.

## Rule Files

- Every `.agents/rules/*.md` file states guidance that holds in any repository using that
  technology. Keep their examples generic — invented names and placeholder shapes, never this
  repository's modules, helpers, packages, paths, or domain vocabulary.
- `.agents/project.md` is the home for repository-specific guidance: the shared base classes,
  helpers, packages, and layout this repository actually defines.
- A rule that cannot be stated without naming something this repository owns belongs in
  `.agents/project.md`. Move it there rather than rewording it into something generic but untrue.
