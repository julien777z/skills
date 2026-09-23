---
name: agent-lock
description: Coordinate exclusive use of a shared resource between agents using an exact string key. Use as a dependency when concurrent agents would conflict over one VM desktop, browser session, or other shared mutable resource. Consume ownership for a command or delegate a bounded lock for a multi-tool agent task; no heartbeats are needed.
---

# Agent Lock

All agents competing for a resource use **exactly the same nonempty string key and coordinator host**. Keys are case-sensitive. Do not add an assignment ID, agent name, branch, or checkout to a key meant to serialize those agents. Different keys may run concurrently.

Use [resources/main.py](resources/main.py) with Python 3.12+ on macOS or Linux. State lives under `~/.local/state/agent-lock/`, outside repositories; keys are hashed into safe filenames. All checkouts share this location. `--state-dir` is for tests or an explicitly shared coordinator configuration. When controlling a VM or remote machine, acquire on the coordinator host rather than separate guest filesystems. This is a cooperative local lock, not a distributed lock or control over unrelated human activity.

## Consume ownership

Prefer ownership scoped to the actual operation. **No heartbeat or renewal commands are needed.** Every lock expires after **600 seconds (10 minutes)** by default. Set `--ttl-seconds` when needed; the CLI rejects durations over **1800 seconds (30 minutes)**, zero, negative, or nonfinite values. Expiry is a fixed deadline, not an inactivity timer. Finish cleanup before that deadline.

For work represented by a foreground command, use `consume`:

```sh
python3 .agents/skills/agent-lock/resources/main.py consume "shared-resource" \
  --owner "task/researcher-1" --activity "Describe this operation" \
  --receipt verification/researcher-1-lock.json --wait-seconds 50 \
  --ttl-seconds 600 -- python3 path/to/actual_worker.py
```

The helper acquires once, runs the command, and releases automatically when the command finishes or fails. It stops the command at expiry or on SIGINT/SIGTERM. It also stops subprocesses in the command's process group. The command receives `AGENT_LOCK_RECEIPT` and sends its output to stderr; the helper writes its JSON result to stdout. Exit `124` means expiry; otherwise a started command's exit code is preserved. A killed supervisor falls back to the lock deadline. Do not daemonize or detach the protected operation, and do not wrap a dummy sleeping process to pretend it tracks an agent's lifetime.

For a researcher using several separate tools, the CLI cannot observe the logical subagent's completion by itself. **The orchestrator owns that task scope:** acquire once, give the worker its receipt/deadline, and release as part of handling the worker's completion, failure, or cancellation. Workers need no periodic maintenance. If the host provides a real task-finalization callback, attach cleanup there; otherwise use the orchestrator's existing completion handling. Do not claim this release is automatic OS process tracking.

```sh
python3 .agents/skills/agent-lock/resources/main.py acquire "shared-resource" \
  --owner "task/researcher-1" --activity "Interactive research" \
  --receipt verification/researcher-1-lock.json --wait-seconds 50
```

Acquire immediately before the protected portion of the assignment, not before unrelated research. The orchestrator records the agent ID, resource key, receipt and expiry. Completion handling must finish or cancel the external operation, release held controls, verify the resource is idle, then run:

```sh
python3 .agents/skills/agent-lock/resources/main.py release \
  --receipt verification/researcher-1-lock.json --resource-idle
```

The worker may release at an earlier natural boundary, such as closing a browser session. The orchestrator checks whether that happened when processing completion. Lock expiry is the fallback if either agent disappears. Multiple resources must be acquired in lexicographic key order and released in reverse order.

## Waiting and expiry

- Acquisition exit `0` / `status: acquired` grants ownership. Exit `2` / `status: busy` means wait in bounded calls or do independent work; never touch the resource while waiting. Exit `1` indicates an error. `consume` also propagates command failures, so inspect the result rather than treating every exit `2` as contention.
- `check --receipt <path>` verifies ownership before a group of external actions, especially after waiting. It does not refresh the deadline. A failed check means stop; the old receipt cannot release a successor's lock. Acquisition is non-reentrant.
- JSON results include typed ownership records with ISO-8601 timestamps. `status "shared-resource"` reports `available`, `held`, or `expired` with the deadline and remaining seconds. Expired locks become claimable automatically; no recovery CLI or file deletion is needed. Never unlink mutex files, because waiters rely on their stable inode.
- Expiry invalidates ownership but cannot close an external desktop/browser session left behind by a separate tool. If acquisition reports `expired_owner`, the orchestrator must stop any still-running old worker and bring the resource to a known idle state before giving the successor permission for input. Never let the previous owner clean up after the successor starts using it.
- Use a unique receipt under ignored `verification/` for each acquisition. Share it only with the assigned worker and its orchestrator; never commit lock state. Keep expiry/cleanup blockers in the task evidence.
