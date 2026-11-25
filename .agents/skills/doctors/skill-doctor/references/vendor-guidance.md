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
| Anthropic | Agent Skills | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview | none shown | 2026-11-23 | whole | none on 2026-11-23; from docs.claude.com earlier |
| Anthropic | Skill authoring best practices | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices | none shown | 2026-11-23 | whole | none on 2026-11-23; from docs.claude.com earlier |
| Anthropic | Prompting best practices | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices | none shown | 2026-11-23 | whole | none |
| Anthropic | Prompting Claude Fable 5.2 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2 | none shown | 2026-11-23 | whole | none |
| Anthropic | Prompting Claude Opus 5.5 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5 | none shown | 2026-11-23 | whole | none |
| Anthropic | Prompting Claude Sonnet 5.5 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5 | none shown | 2026-11-23 | whole | none |
| Anthropic | Prompting Claude Haiku 5.5 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5 | none shown | 2026-11-23 | whole | none |
| Anthropic | Claude Fable 5.2 and Claude Mythos 5.2 migration guide | https://platform.claude.com/docs/en/models/fable-5-2/migration-guide | none shown | 2026-11-23 | extracts: lines on prompts, skills and instructions | none |
| Anthropic | Extend Claude with skills | https://code.claude.com/docs/en/skills | none shown | 2026-11-23 | whole, 119,905 characters in two reads | none |
| Anthropic | How Claude remembers your project | https://code.claude.com/docs/en/memory | none shown | 2026-11-23 | whole | none |
| Anthropic | Create custom subagents | https://code.claude.com/docs/en/sub-agents | none shown | 2026-11-23 | first 100,000 of 114,867 characters | none |
| Anthropic | Best practices for Claude Code | https://code.claude.com/docs/en/best-practices | none shown | 2026-11-23 | whole | none on 2026-11-23; from anthropic.com/engineering on 2026-09-05 |
| Anthropic | skill-creator `SKILL.md` | https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md | none shown | 2026-11-23 | extracts | none |
| Anthropic | The new rules of context engineering for Claude 5 generation models | https://claude.dev/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models/ | 2026-07-24 | 2026-11-23 | extracts | from claude.com/blog, 308 |
| Anthropic | Effective context engineering for AI agents | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | 2025-09-29 | 2026-11-23 | extracts | none |
| Anthropic | Equipping agents for the real world with Agent Skills | https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills | 2025-10-16, updated 2025-12-18 | 2026-11-23 | extracts | none |
| Anthropic | Writing effective tools for agents — with agents | https://www.anthropic.com/engineering/writing-tools-for-agents | 2025-09-11 | 2026-11-23 | extracts | none |
| Open spec | Best practices for skill creators | https://agentskills.io/skill-creation/best-practices | none shown | 2026-11-23 | whole | none |
| Open spec | Optimizing skill descriptions | https://agentskills.io/skill-creation/optimizing-descriptions | none shown | 2026-11-23 | whole | none |
| Open spec | Evaluating skill output quality | https://agentskills.io/skill-creation/evaluating-skills | none shown | 2026-11-23 | whole | none |
| Open spec | Specification | https://agentskills.io/specification | none shown | 2026-11-23 | whole | none |
| Open format | AGENTS.md | https://agents.md/ | none shown | 2026-11-23 | extracts | none |
| OpenAI | Build skills | https://learn.chatgpt.com/docs/build-skills | none shown | 2026-11-23 | extracts | none on 2026-11-23; from developers.openai.com/codex on 2026-09-05 |
| OpenAI | Custom instructions with AGENTS.md | https://learn.chatgpt.com/docs/agent-configuration/agents-md | none shown | 2026-11-23 | extracts | none on 2026-11-23; from developers.openai.com/codex on 2026-09-05 |
| OpenAI | Subagents | https://learn.chatgpt.com/docs/agent-configuration/subagents | none shown | 2026-11-23 | extracts | none |
| OpenAI | Using skills to accelerate OSS maintenance | https://developers.openai.com/blog/skills-agents-sdk | none shown; cites figures from 2026-03-06 | 2026-11-23 | extracts | none |

Pages of these kinds that no row holds yet, to look for on the next refresh: the migration guides
and "What's new" pages for Claude Opus 5.5, Sonnet 5.5 and Haiku 5.5; the open specification's page
on using scripts; the skill-creator announcement the skills page links; the article on folding
subagents into the main agent loop that the context-engineering post links; and any Codex
best-practices page on the official docs, which a search on 2026-11-23 did not find.

## Bundled Files

Files a harness ships beside its own skills, read from the running harness when present and found
by their subject, since their location differs by machine and version.

| Harness | File | Version read | Last read | Read |
|---|---|---|---|---|
| Claude Code | Prompt audit, "Finding and Removing Dated Prompting Patterns", among the bundled API skill's shared files | 2.1.327 | 2026-11-23 | whole, 255 lines |
| Claude Code | Model migration guide, among the same shared files | 2.1.327 | 2026-11-23 | the Claude Fable 5.2 behavior-change lines on approvals, "never" rules and earlier instructions, of 2,566 lines |

The prompt audit is a vendor-written rubric for this doctor's own job, with a list of what to
keep. The doctor reads it whole when the harness has it. The files are not on disk until the API
skill loads; loading it extracts them under the system's temporary directory. Claude Code runs the
same audit as `/doctor prompt-audit`, which needs v2.1.283 or later.

## Hosts

| Host | Rules-file target | Skill body target | Listing budget | Description truncation | Rules cap |
|---|---|---|---|---|---|
| Claude Code | under 200 lines per always-loaded file | under 500 lines, about 5k tokens | 1% of context by default | 1,536 characters with the when-to-use field | none; a file over 4 MiB is skipped |
| Codex | none published | none published | 2% of context, or 8,000 characters; `skills.max_context_tokens` up to 10,000 tokens | no figure; descriptions are shortened first when the listing is over budget | `project_doc_max_bytes`, 32 KiB by default; files past it are not added |
| Cursor | none published | none published | none published | none published | none published |

The Claude Code and Codex rows were confirmed on 2026-11-23; the Cursor row stands as read on
2026-09-05. After compaction Claude Code re-attaches only the first 5,000 tokens of each invoked
skill, within 25,000 tokens across all of them. Its listing budget and description cap are
settings, `skillListingBudgetFraction` and `skillListingMaxDescChars`; `skillOverrides` can list a
skill by name only; and when the listing passes its budget, descriptions are dropped starting with
the skills invoked least. Claude Code warns at startup when custom subagent descriptions together
pass 15,000 tokens, and loads the first 200 lines or 25KB of `MEMORY.md`. The skill specification
and the vendor's upload API cap a description at 1,024 characters. A SessionStart hook's plain
stdout enters context on startup, resume, clear, compact, and fork (as read on 2026-11-20).

## Summary

Lines were read on 2026-11-23 unless marked.

- **Only what the model lacks.** The model is already very smart, so guidance adds only context it
  does not have: the audience and product, environment facts, the quality bar, tool contracts,
  hard judgment calls and the reasons behind constraints. A rules file works best holding only
  what the model could not work out from the code. The test per instruction is whether the agent
  would get the work wrong without it; an unsure answer is tested, and length alone never
  justifies a deletion.
- **Overconstraint.** The coding agent's own system prompt, rules files and skills were found to
  overconstrain the newest models; many constraints were deleted in favor of the model's judgment.
  Skills are lightweight guides, firm only in highly important areas.
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
- **Rules files.** A rules file holds facts and every-session conventions, kept light, with most
  of its tokens on the codebase's gotchas. Every line takes attention on every task, and a file
  past 200 lines may lower adherence. A multi-step procedure, or something that matters for one
  part of the codebase, moves to a skill or a path-scoped rule. Contradictory instructions are
  picked arbitrarily.
- **Skills.** A skill is a directory with `SKILL.md`; `name` and `description` are the only fields
  both vendors read. `name` equals the directory, lowercase with hyphens, at most 64 characters.
  `description` is 1–1024 characters, says what the skill does and when to use it, key use first,
  and names categories of intent, not a growing list of trigger phrases. Anthropic asks for the
  third person; the open specification's description guide asks for imperative phrasing ("Use
  this skill when...") and to err toward pushy. Codex and the open specification add when it
  should not trigger.
- **Progressive disclosure.** Metadata always loaded, body on trigger, bundled files on demand.
  Body under 500 lines and about 5k tokens, the most important instructions near the top.
  References one level deep, each named with when to read it; one over 100 lines opens with a
  table of contents. Scripts run without their code entering context.
- **Degrees of freedom.** Match specificity to how fragile the task is: exact instructions where
  one sequence is safe, general direction where judgment is needed. Step-by-step choreography
  degrades judgment tasks; numbered steps stay only where order matters.
- **Examples.** The model matches an example's length, tone and structure. Use several varied
  examples labeled as illustrations, and delete examples of judgment the model already owns. The
  coding agent's team found that examples constrain the newest models to an exploration space,
  and puts the effort into expressive tools, parameters and files instead.
- **Named design defaults.** For interface design on one current model, naming the specific
  patterns to avoid works where a general instruction to avoid a generic look does not.
- **Deterministic work.** Prefer scripts for deterministic operations; what must happen every
  time is a hook, a deny rule or a managed setting, since a rules file is a guideline the model
  may decide does not apply.
- **Thinking and tools.** Effort is the control for depth of thinking, so "think hard" and "be
  thorough" lines can go. An instruction to answer without deliberating, or to think less, does
  not reliably reduce thinking on the current models. Instructions to write out reasoning in the
  response are removed. Independent tool calls already run in parallel. One keyword, `ultrathink`,
  still acts in Claude Code skill content.
- **Subagents.** Standing instructions to delegate are reviewed and removed where the model
  delegates too much. State what a subagent adds to a session's cost, when delegation is worth it
  and when it is not, and how to brief one. Handing the same task to a subagent does not improve
  the answer; a fresh reviewer does. A subagent sees none of the conversation, so a rule it must
  follow is restated in the brief. Codex starts subagents only when asked directly or told to by a
  project or skill instruction.
- **Per-model text.** Prompts are re-audited at every model release. Text that says how things
  changed, history narratives, fixed update cadences and numeric output ceilings are removed; for
  the newest model family, text that makes the agent finish its work and report clearly is added
  or kept. Hard style rules are followed closely enough to make prose choppy.
- **Other.** Offer one default and an escape hatch, never a menu. Avoid time-sensitive text. Keep
  terminology consistent. Never assume a package is installed.
- **OpenAI.** The rules file carries the mandatory skill-usage triggers; if routing is unreliable,
  fix the metadata before adding code; keep each skill to one job; prefer instructions over
  scripts unless behavior must be deterministic.
- **Evaluation.** Evaluate before documenting: at least three scenarios and a no-skill baseline,
  "Tested with Haiku, Sonnet, and Opus". The open specification starts with two or three test
  cases run with and without the skill, tests a description on about 20 should- and
  should-not-trigger queries split into train and validation sets, and keeps a skill lean by
  trying removals when pass rates plateau.

Where the pages disagree, `skill-pass`'s vendor rubric records the repository's choice under
**Where The Sources Disagree**.

## Quotes

Each quote is exact as the page or file returned it on the row's fetch date.

- Skill authoring best practices: "Default assumption: Claude is already very smart. Only add
  context Claude doesn't already have." "Match the level of specificity to the task's fragility
  and variability." "Keep the `SKILL.md` body under 500 lines for optimal performance." "For
  reference files longer than 100 lines, include a table of contents at the top." "Always write in
  third person." "Maximum 1,024 characters". "Prefer scripts for deterministic operations".
  "Tested with Haiku, Sonnet, and Opus".
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
- Prompting Claude Sonnet 5.5: "Asking the model in the system prompt to think less doesn't
  reliably reduce its thinking."
- Extend Claude with skills: "Put the key use case first: the combined `description` and
  `when_to_use` text is truncated at 1,536 characters in the skill listing". "The budget scales at
  1% of the model's context window." "State what to do rather than narrating how or why".
- How Claude remembers your project: "target under 200 lines per CLAUDE.md file. Longer files
  consume more context and reduce adherence." "if two instructions contradict each other, Claude
  may pick one arbitrarily."
- Create custom subagents: "If a rule must, such as "ignore the `vendor/` directory," restate it
  in the prompt you give Claude when delegating."
- Best practices for Claude Code: "every line in it takes a little of Claude's attention on
  *every* task, whether it's relevant or not." "Older models sometimes needed the emphasis.
  Current ones follow a plainly worded line, and piling on emphasis mostly makes Claude over-apply
  the rule. If it's a rule that can't bend, turn it into a hook or a deny rule." "Handing the same
  task to a subagent doesn't make the answer any better. A fresh reviewer does help". "If
  something has to happen every time, make it a hook, a deny rule, or a managed setting."
- skill-creator: "If you find yourself writing ALWAYS or NEVER in all caps, or using super rigid
  structures, that's a yellow flag". "please make the skill descriptions a little bit 'pushy'".
- The new rules of context engineering for Claude 5 generation models: "Overall, we found that we
  were overconstraining Claude Code, both through our system prompt and in our CLAUDE.md files and
  skills." "Think of skills as lightweight guides to let Claude find information when needed.
  Avoid making them overconstrained, except in highly important areas." "Keep your CLAUDE.md
  lightweight and briefly describe what your repo is for, but spend most of the tokens on gotchas
  inside of the codebase." "With our newest models, we've found that giving examples actually
  constrains them to a certain exploration space."
- Best practices for skill creators: "Would the agent get this wrong without this instruction? If
  the answer is no, cut it. If you're unsure, test it." "The highest-value content in many skills
  is a list of gotchas".
- Optimizing skill descriptions: "Use imperative phrasing." "Err on the side of being pushy."
  "Aim for about 20 queries: 8-10 that should trigger and 8-10 that shouldn't." "Add specificity
  about what the skill does *not* do".
- Evaluating skill output quality: "Start with 2-3 test cases." "Keep the skill lean."
- Effective context engineering for AI agents: "smarter models require less prescriptive
  engineering".
- Build skills (OpenAI): "Explain exactly when this skill should and should not trigger." "Keep
  each skill focused on one job." "Prefer instructions over scripts unless you need deterministic
  behavior or external tooling."
- Subagents (OpenAI): "Current local Codex releases spawn agents after a direct request or
  applicable project or skill instruction."
- Using skills to accelerate OSS maintenance: "In practice, both repos use short if/then rules for
  mandatory skill usage." "If routing feels unreliable, fix the metadata before you add more
  code."
- Prompt audit: "Describing success beats enumerating failure; a prohibition against a failure the
  model wasn't going to make can *anchor it toward* that failure". "Keep prohibitions whose
  failure reproduces on the target model; rewrite the rest as positive statements of intent".
  "Patch accretion: many narrow conditionals, each traceable to one incident". "Never justify a
  deletion by character count alone." "Re-audit at every model release. Prompts are per-model
  artifacts". "Working redundancy is not cruft".
- Model migration guide: "Under a "never" rule, the model took a step the person in charge had
  approved in about one try in ten, against nine in ten when the rule said to get a go-ahead
  first."
