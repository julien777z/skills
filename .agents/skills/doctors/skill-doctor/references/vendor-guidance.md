# Vendor Guidance

Contents: the pages to fetch; the files that ship with a harness; what each host loads and caps;
the dated summary; the quotes the summary relies on.

This is the record of what the vendors' skill and prompting guidance said when last read. The
doctor refreshes it before every audit, as `SKILL.md`'s **Pre-Pass** says. A row carries the page's
title, its URL, the date the page shows, the date it was last fetched, how much of it was read and
any redirect seen. A row the refresh could not reach keeps its earlier fetch date and is marked
`not reached` with the attempt's date. A quote is copied from the fetched page or bundled file and
never written from memory; a quote that can no longer be found on its page is removed, and the
summary line that rested on it is rewritten or dropped.

## Pages

| Vendor | Title | URL | Page date | Last fetched | Read | Redirect seen |
|---|---|---|---|---|---|---|
| Anthropic | Agent Skills | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview | none shown | 2026-11-20 | whole | from docs.claude.com |
| Anthropic | Skill authoring best practices | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices | none shown | 2026-11-20 | whole | from docs.claude.com |
| Anthropic | Prompting best practices | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices | none shown | 2026-11-20 | whole | none |
| Anthropic | Prompting Claude Fable 5.2 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2 | none shown | 2026-11-20 | whole | none |
| Anthropic | Prompting Claude Opus 5.5 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5 | none shown | 2026-11-20 | whole | none |
| Anthropic | Extend Claude with skills | https://code.claude.com/docs/en/skills | none shown | 2026-11-20 | first 119,715 characters | none |
| Anthropic | How Claude remembers your project | https://code.claude.com/docs/en/memory | none shown | 2026-11-20 | whole | none |
| Anthropic | Best practices for Claude Code | https://code.claude.com/docs/en/best-practices | none shown | 2026-11-20 | whole | none on 2026-11-20; from anthropic.com/engineering on 2026-09-05 |
| Anthropic | skill-creator `SKILL.md` | https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md | none shown | 2026-11-20 | extracts | none |
| Anthropic | Effective context engineering for AI agents | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | 2025-09-29 | 2026-11-20 | extracts | none |
| Anthropic | Equipping agents for the real world with Agent Skills | https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills | 2025-10-16 | 2026-11-20 | extracts | none |
| Anthropic | Writing effective tools for agents | https://www.anthropic.com/engineering/writing-tools-for-agents | 2025-09-11 | 2026-11-20 | extracts | none |
| Open spec | Best practices for skill creators | https://agentskills.io/skill-creation/best-practices | none shown | 2026-11-20 | whole | none |
| Open spec | Agent skills specification | https://agentskills.io/specification | not recorded | 2026-09-05 | not reached 2026-11-20 | none |
| Open format | AGENTS.md | https://agents.md/ | not recorded | 2026-09-05 | not reached 2026-11-20 | none |
| OpenAI | Codex skills | https://learn.chatgpt.com/docs/build-skills | not recorded | 2026-09-05 | not reached 2026-11-20 | from developers.openai.com/codex |
| OpenAI | Codex AGENTS.md discovery and cap | https://learn.chatgpt.com/docs/agent-configuration/agents-md | not recorded | 2026-09-05 | not reached 2026-11-20 | from developers.openai.com/codex |
| OpenAI | Skills authoring narrative | https://developers.openai.com/blog/skills-agents-sdk | not recorded | 2026-09-05 | not reached 2026-11-20 | none |

Pages of these kinds that no row holds yet, to look for on the next refresh: the prompting pages
for the other current models, each vendor's notes on what changed with its newest models and its
migration guides, the open specification's pages on descriptions and on evaluating skills, and the
coding agent's subagents page.

## Bundled Files

Files a harness ships beside its own skills, read from the running harness when present and found
by their subject, since their location differs by machine and version.

| Harness | File | Version read | Last read | Read |
|---|---|---|---|---|
| Claude Code | Prompt audit, "Finding and Removing Dated Prompting Patterns", among the bundled API skill's shared files | 2.1.328 | 2026-11-20 | whole, 255 lines |
| Claude Code | Model migration guide, among the same shared files | 2.1.328 | 2026-11-20 | the behavior-change sections for the current model families, of 2,566 lines |

The prompt audit is a vendor-written rubric for this doctor's own job, with a list of what to
keep. The doctor reads it whole when the harness has it.

## Hosts

| Host | Rules-file target | Skill body target | Listing budget | Description truncation | Rules cap |
|---|---|---|---|---|---|
| Claude Code | under 200 lines per always-loaded file | under 500 lines, about 5k tokens | 1% of context by default | 1,536 characters with the when-to-use field | none; a file over 4 MiB is skipped |
| Codex | none published | none published | 2% of context, or 8,000 characters | none published | `project_doc_max_bytes`, 32 KiB by default; content past it is dropped |
| Cursor | none published | none published | none published | none published | none published |

The Claude Code row was confirmed on 2026-11-20; the Codex and Cursor rows stand as read on
2026-09-05. After compaction Claude Code re-attaches only the first 5k tokens of each invoked
skill, within 25k tokens across all of them. Its listing budget and description cap are settings,
`skillListingBudgetFraction` and `skillListingMaxDescChars`; `skillOverrides` can list a skill by
name only; and when the listing passes its budget, descriptions are dropped starting with the
skills invoked least. The skill specification and the vendor's upload API cap a description at
1,024 characters. A SessionStart hook's plain stdout enters context on startup, resume, clear,
compact, and fork.

## Summary

Lines were read on 2026-11-20 unless marked; a line marked 2026-09-05 rests on a page the last
refresh did not reach.

- **Only what the model lacks.** The model is already very smart, so guidance adds only context it
  does not have: the audience and product, environment facts, the quality bar, tool contracts,
  hard judgment calls and the reasons behind constraints. A rules file works best holding only
  what the model could not work out from the code. The test per instruction is whether the agent
  would get the work wrong without it; an unsure answer is tested, and length alone never
  justifies a deletion.
- **Goals over constraints.** Describing success beats listing failures, and a prohibition
  against a mistake the model was not going to make can pull it toward that mistake. Say what to
  do. Prohibitions that stay: those whose failure reproduces on the current model, and those that
  carry a stated reason or a real policy constraint.
- **"Never" is absolute on the newest models.** An instruction holding "never" is applied as
  written, including to an approved step, so a firm rule is written with its scope and reason or
  as the action to take, such as asking for approval before a step. Cautions collect in
  instruction files over time and make the model ask for approval it does not need.
- **Approvals name the actions.** A broad approval rule holds back routine work; list the actions
  that need a go-ahead and the routine steps that need none, and keep a confirmation step for
  risky or irreversible actions.
- **Emphasis.** Capitals and words such as "critical" make current models over-apply the rule
  they mark, and when several lines carry them the markers stop carrying information. Explain the
  reason in plain words. A rule that cannot bend becomes a hook or a deny rule.
- **Incident patches.** Many narrow conditionals, each traceable to one incident, make the model
  navigate special cases and fail between them; generalize the principle and test removals as
  well as additions. Environment facts that defy assumptions are the exception and belong in a
  gotchas list.
- **Rules files.** A rules file holds facts and every-session conventions. Every line takes
  attention on every task, and a file past 200 lines may lower adherence. A multi-step procedure,
  or something that matters for one part of the codebase, moves to a skill or a path-scoped rule.
  Contradictory instructions are picked arbitrarily.
- **Skills.** A skill is a directory with `SKILL.md`; `name` and `description` are the only fields
  both vendors read. `name` equals the directory, lowercase with hyphens, at most 64 characters.
  `description` is 1–1024 characters, third person, key use first, and says what the skill does
  and when to use it; it names categories of intent, not a growing list of trigger phrases. Codex
  adds when it should not trigger (2026-09-05).
- **Progressive disclosure.** Metadata always loaded, body on trigger, bundled files on demand.
  Body under 500 lines and about 5k tokens, the most important instructions near the top.
  References one level deep, each named with when to read it; one over 100 lines opens with a
  table of contents. Scripts run without their code entering context.
- **Degrees of freedom.** Match specificity to how fragile the task is: exact instructions where
  one sequence is safe, general direction where judgment is needed. Step-by-step choreography
  degrades judgment tasks; numbered steps stay only where order matters.
- **Examples.** The model matches an example's length, tone and structure. Use several varied
  examples labeled as illustrations, and delete examples of judgment the model already owns.
- **Named design defaults.** For interface design on one current model, naming the specific
  patterns to avoid works where a general instruction to avoid a generic look does not.
- **Deterministic work.** Prefer scripts for deterministic operations; what must happen every
  time is a hook, a deny rule or a managed setting, since a rules file is a guideline the model
  may decide does not apply.
- **Thinking and tools.** Effort is the control for depth of thinking, so "think hard" and "be
  thorough" lines can go. An instruction to answer without deliberating does not stop thinking at
  medium effort and above. Instructions to write out reasoning in the response are removed.
  Independent tool calls already run in parallel. One keyword, `ultrathink`, still acts in Claude
  Code skill content.
- **Subagents.** Standing instructions to delegate are reviewed and removed where the model
  delegates too much. State what a subagent adds to a session's cost, when delegation is worth it
  and when it is not, and how to brief one. Handing the same task to a subagent does not improve
  the answer; a fresh reviewer does.
- **Per-model text.** Prompts are re-audited at every model release. Text that says how things
  changed, history narratives, fixed update cadences and numeric output ceilings are removed; for
  the newest model family, text that makes the agent finish its work and report clearly is added
  or kept. Hard style rules are followed closely enough to make prose choppy.
- **Other.** Offer one default and an escape hatch, never a menu. Avoid time-sensitive text. Keep
  terminology consistent. Never assume a package is installed.
- **OpenAI (2026-09-05).** The rules file carries the mandatory skill-usage triggers; if routing
  is unreliable, fix the metadata before adding code; keep each skill to one job; prefer
  instructions over scripts unless behavior must be deterministic.
- **Evaluation.** Evaluate before documenting: at least three scenarios and a no-skill baseline,
  "Tested with Haiku, Sonnet, and Opus".

Where the pages disagree, `skill-pass`'s vendor rubric records the repository's choice under
**Where The Sources Disagree**.

## Quotes

Each quote is exact as the page or file returned it on the row's fetch date.

- Skill authoring best practices: "Default assumption: Claude is already very smart. Only add
  context Claude doesn't already have." "Match the level of specificity to the task's fragility
  and variability." "Keep the `SKILL.md` body under 500 lines for optimal performance." "For
  reference files longer than 100 lines, include a table of contents at the top." "Always write in
  third person." "Maximum 1,024 characters". "Prefer scripts for deterministic operations".
- Agent Skills: "Level 2: Instructions | When Skill is triggered | Under 5k tokens".
- Prompting best practices: "Tell Claude what to do instead of what not to do". "Providing context
  or motivation behind your instructions, such as explaining to Claude why such behavior is
  important, can give Claude more information about your goals". "Where you might have said
  'CRITICAL: You MUST use this tool when...,' you can use more normal prompting such as 'Use this
  tool when...' instead." "Claude's latest models run independent tool calls in parallel."
- Prompting Claude Fable 5.2: "The model treats an instruction that contains 'never' as absolute.
  For example, write 'ask for approval before deleting files' instead of 'never delete files' if
  you want the model to keep responsibility over an action." "rewrite absolute rules with their
  scope and reason". "Standing instructions to delegate: Lines that tell the model to delegate can
  sit in system prompts, skills, and agent files. Read those files before you migrate and remove
  the lines you no longer need if the model delegates too much in testing." "state what a subagent
  adds to the cost of a session, say when delegation is worth it and when it isn't, and tell the
  model how to brief a subagent". "Telling the model to act more freely is too vague, so list the
  routine steps that it can take on its own." "Keep your own confirmation step for risky or
  irreversible actions." "If your prompts, skills, or tool descriptions ask the model to write out
  its reasoning in the response, remove those instructions."
- Prompting Claude Opus 5.5: "a general instruction such as 'avoid a generic AI look' mostly swaps
  one default for another. It responds well to instructions that name specific patterns to avoid".
- Extend Claude with skills: "Put the key use case first: the combined `description` and
  `when_to_use` text is truncated at 1,536 characters in the skill listing". "The budget scales at
  1% of the model's context window." "State what to do rather than narrating how or why".
- How Claude remembers your project: "target under 200 lines per CLAUDE.md file. Longer files
  consume more context and reduce adherence." "if two instructions contradict each other, Claude
  may pick one arbitrarily."
- Best practices for Claude Code: "every line in it takes a little of Claude's attention on
  *every* task, whether it's relevant or not." "Older models sometimes needed the emphasis.
  Current ones follow a plainly worded line, and piling on emphasis mostly makes Claude over-apply
  the rule. If it's a rule that can't bend, turn it into a hook or a deny rule." "Handing the same
  task to a subagent doesn't make the answer any better. A fresh reviewer does help". "If
  something has to happen every time, make it a hook, a deny rule, or a managed setting."
- skill-creator: "If you find yourself writing ALWAYS or NEVER in all caps, or using super rigid
  structures, that's a yellow flag". "please make the skill descriptions a little bit 'pushy'".
- Best practices for skill creators: "Would the agent get this wrong without this instruction? If
  the answer is no, cut it. If you're unsure, test it." "The highest-value content in many skills
  is a list of gotchas".
- Effective context engineering for AI agents: "smarter models require less prescriptive
  engineering".
- Prompt audit: "Describing success beats enumerating failure; a prohibition against a failure the
  model wasn't going to make can *anchor it toward* that failure". "Keep prohibitions whose
  failure reproduces on the target model; rewrite the rest as positive statements of intent".
  "Patch accretion: many narrow conditionals, each traceable to one incident". "Never justify a
  deletion by character count alone." "Re-audit at every model release. Prompts are per-model
  artifacts". "Working redundancy is not cruft".
- Model migration guide: "Under a "never" rule, the model took a step the person in charge had
  approved in about one try in ten, against nine in ten when the rule said to get a go-ahead
  first."
