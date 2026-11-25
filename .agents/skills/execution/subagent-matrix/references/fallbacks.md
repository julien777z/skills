# Fallbacks

Read when a dispatch is refused or a model is reported unavailable: what launches first, how each
kind of refusal is handled, and which fallbacks a specialist or an ordinary assignment may take.

Contents: **Launch The Assignment First**, **A Refusal That Names Its Cause**, **A Capacity
Refusal**, **A Launch On Another Provider's Model**, **The Accepted Worker**, **A Specialist
Assignment**, **Ordinary Fallbacks**.

## Launch The Assignment First

Before a caller marks a requested capability level or explicit model unavailable, follows an
unavailable-model fallback, or takes the launch fallback, launch the actual assigned work once with
its exact candidate identifier and explicit reasoning effort when the native tool is available.

- A successful dispatch establishes that the host accepted the requested identifier for that launch;
  it does not establish catalog availability or runtime identity.
- An explicit host receipt that the candidate is unsupported establishes unavailability only as the
  sections below define.

## A Refusal That Names Its Cause

**A refusal that names its own cause or fix is a repair, never unavailability**: a client or runtime
version too old, a sign-in, a disabled provider, a stale process.

- A rate limit or quota refusal is not this kind; it follows **A Capacity Refusal** below.
- The repair is the first step and every fallback comes after it: update the client, sign in,
  enable the provider or restart the process, or confirm the condition no longer holds, then launch
  the same assignment again with the same identifier. A launch on another provider's model that no
  provider or exact-model requirement binds instead moves to the session's own provider at once, as
  **A Launch On Another Provider's Model** below says.
- Updating or repairing the agent's own client or runtime is that repair, never a repository or
  global settings change, which **The Accepted Worker** forbids.
- Repair the component that actually holds the refused value, read from the running request path
  rather than from the refusal's own advice, such as a proxy between the agent and the provider.
- Only when that component is out of reach — every route the agent's tools have to it has been
  tried, and what remains needs the user's own identity, device, password or physical presence —
  does its repair go to the user, as a question naming the whole step with the exact command.
- Record the original refusal, the repair attempted, and any relaunch receipt.
- If the failure remains operational or the repair cannot be made, use the launch fallback and
  retain that classification.
- Model substitution requires an explicit receipt that the exact model is unsupported or, where **A
  Specialist Assignment** allows it, denied, apart from the move to the session's own provider
  below.

## A Capacity Refusal

When the user or calling skill requires a provider or exact model, a rate limit or quota refusal
is rerun within that requirement when capacity returns.

**For an assignment with no provider or exact-model requirement, a rate limit or quota refusal
moves the assignment to the other harness's matching model**: a Codex model's refusal relaunches the same assignment, with the same brief and reasoning effort, on
the Claude family at the same capability level in **model capabilities**, and a Claude model's
refusal on the Codex family, because the refusal is one provider's capacity and the other's model at
that level does the same work without waiting out a reset time the refusal can only guess.

- It is not unavailability: it permits none of the unsupported-model fallbacks of **A Specialist
  Assignment** and **Ordinary Fallbacks**, no lower capability level and no absorbing the work into
  the coordinator's own process, and it never holds work.
- Resolve the matching model through **Workflow** step 2 and **Launch The Assignment First**, and
  record the original refusal beside the relaunch.
- In a comparison pair, relaunch both sides on the matching model so the pair keeps one model.
- When that model also refuses for capacity, or the host cannot launch the other harness's models,
  relaunch on whichever permitted model
  the request path shows cleared first: the coordinator answering on that model, or a relaunch being
  accepted, shows it has cleared, and only a refused relaunch shows it still holds.

## A Launch On Another Provider's Model

**A launch on another provider's model that does not start moves to the session's own provider.**
Where a step calls for or prefers a model on a provider other than the running session's — a default
council seat, the capacity relaunch above — and that launch is refused, never starts, or shows no
activity after its brief at the first of two moments — a sibling returning, or 15 minutes after
its brief (with no siblings, the 15 minutes alone) — relaunch the same assignment, with the same
brief and effort, on the session's own provider at the same capability level, record both
launches, and carry on: the other provider is a preference that improves independence, never a
blocker, and its repair never holds the step. The coordinator waits on one launch at a time, never
past 15 minutes after that launch's brief, and once any sibling returns its very next call reads
the other-provider launch's activity, before any wait on another launch; a launch still running is
cancelled once its replacement starts.

- A provider or exact model the user or calling skill requires is honored: its launch is repaired
  or rerun within that requirement as the sections above say, never moved.
- Inside **Ordinary Fallbacks** below, where the ladder reached the other provider because the
  session's own family at that level was refused as unsupported, a launch there that does not start
  goes on to the ladder's next step instead.

## The Accepted Worker

The accepted worker performs the assignment; never launch a throwaway availability probe.

- Record the runtime identifier only when the host exposes its exact value.
- Generic provider or product branding, a worker-reported label, or no runtime identifier is neither
  confirmation nor a contradiction of the accepted selection.
- Availability is not permission to change repository or global settings, such as a model policy or
  a provider's configuration.

## A Specialist Assignment

For a specialist assignment, after **Launch The Assignment First** establishes that Claude Mythos is
unsupported or denied, launch the same assignment directly on the latest Claude family at the
`frontier` capability level, unless the calling skill explicitly selects a different ordinary
fallback capability level.

- Resolve its latest Claude family through **Workflow** step 2 and **Launch The Assignment First**
  and apply that fallback only if it respects the user's explicit model or capability constraint;
  otherwise hold the assignment.
- Do not try older Mythos, or another provider on an unsupported receipt.
- Apply the repair, retry, and capacity rules above to every attempt, including the selected
  fallback and Codex Astra.
- Hold when the selected fallback or specialist Codex Astra is confirmed unsupported or denied.
- Catalog omission, identifier-resolution failure, and operational or capacity failures do not
  establish Mythos unavailability or denial.
- No ordinary assignment may select specialist as a fallback.

## Ordinary Fallbacks

For ordinary assignments, when a requested capability level or model is explicitly unsupported,
apply a fallback only when the calling skill declares its direction and limits and the candidate
meets any provider, exact model or capability-level requirement set by the user or calling skill.
**A permitted fallback steps down as little as it
can**, in this order, launching the actual assignment at each step and moving on only on an explicit
unsupported receipt:

1. earlier versions of the same family, newest first, resolved through the host or official provider
   discovery in **Workflow** step 2;
2. the other provider's family at the requested level;
3. the family one capability level below, on the same provider first, then the other provider's
   family at that level;
4. each lower level in turn, never skipping one.

A family another seat or worker already uses is still the next step: a fallback chooses by
capability, never to keep the families distinct. Report the original request as unavailable and name
the actual fallback capability and model; never relabel it as the requested level. Without that
policy, report the unsupported request and host receipt; do not substitute another model. If the
required worker cannot launch, apply the launch fallback in **Dispatch**. Preserve one resolved
model within comparison pairs.
