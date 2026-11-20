---
name: agent-lock
description: Coordinate exclusive use of a shared resource between agents using an exact string key. Use as a dependency when concurrent agents would conflict over one VM desktop, browser session, or other shared mutable resource. Consume ownership for a command or delegate a bounded lock for a multi-tool agent task; no heartbeats are needed.
short_description: 'Coordinate exclusive use of a shared resource between agents using an exact string key.'
---

# Agent Lock

All agents competing for a resource use **exactly the same nonempty string key and coordinator host**. Keys are case-sensitive. Do not add an assignment ID, agent name, branch, or checkout to a key meant to serialize those agents. Different keys may run concurrently.

Use [resources/main.py](resources/main.py) with Python 3.12+ on macOS or Linux. Resolve it from this skill's own directory and hold its absolute path in `AGENT_LOCK` for the commands below. State lives under `~/.local/state/agent-lock/`, outside repositories; keys are hashed into safe filenames. All checkouts share this location. `--state-dir` is for tests or an explicitly shared coordinator configuration. When controlling a VM or remote machine, acquire on the coordinator host rather than separate guest filesystems. This is a cooperative local lock, not a distributed lock or control over unrelated human activity.

## Consume ownership

Prefer ownership scoped to the actual operation. **No heartbeat or renewal commands are needed.** Every lock expires after **600 seconds (10 minutes)** by default. Set `--ttl-seconds` when needed; the CLI rejects durations over **900 seconds (15 minutes)**, zero, negative, or nonfinite values. An operation that needs longer is too slow, never a reason for a longer lease: a test suite past its time budget is fixed, as the testing rules say, and a long multi-step job is split into operations that each take the lock. Expiry is a fixed deadline, not an inactivity timer. Finish cleanup before that deadline.

For work represented by a foreground command, use `consume`:

```sh
python3 "$AGENT_LOCK" consume "shared-resource" \
  --owner "task/researcher-1" --activity "Describe this operation" \
  --receipt .agent_sources/locks/researcher-1-lock.json --wait-seconds 50 \
  --ttl-seconds 600 -- python3 path/to/actual_worker.py
```

The helper acquires once, runs the command, and releases automatically when the command finishes or fails. It stops the command at expiry or on SIGINT/SIGTERM. It also stops subprocesses in the command's process group. The command receives `AGENT_LOCK_RECEIPT` and sends its output to stderr; the helper writes its JSON result to stdout. Exit `124` means expiry; otherwise a started command's exit code is preserved. A killed supervisor falls back to the lock deadline. Do not daemonize or detach the protected operation, and do not wrap a dummy sleeping process to pretend it tracks an agent's lifetime.

For a researcher using several separate tools, the CLI cannot observe the logical subagent's completion by itself. **The orchestrator owns that task scope:** acquire once, give the worker its receipt/deadline, and release as part of handling the worker's completion, failure, or cancellation. Workers need no periodic maintenance. If the host provides a real task-finalization callback, attach cleanup there; otherwise use the orchestrator's existing completion handling. Do not claim this release is automatic OS process tracking.

```sh
python3 "$AGENT_LOCK" acquire "shared-resource" \
  --owner "task/researcher-1" --activity "Interactive research" \
  --receipt .agent_sources/locks/researcher-1-lock.json --wait-seconds 50
```

Acquire immediately before the protected portion of the assignment, not before unrelated research. The orchestrator records the agent ID, resource key, receipt and expiry. Completion handling must finish or cancel the external operation, release held controls, verify the resource is idle, then run:

```sh
python3 "$AGENT_LOCK" release \
  --receipt .agent_sources/locks/researcher-1-lock.json --resource-idle
```

The worker may release at an earlier natural boundary, such as closing a browser session. The orchestrator checks whether that happened when processing completion. Lock expiry is the fallback if either agent disappears. Multiple resources must be acquired in lexicographic key order and released in reverse order.

## A pool of interchangeable resources

**Work that any one of several equal resources can serve takes whichever comes free first**, with
every key named in one `acquire` or `consume` call and `--any`:

```sh
python3 "$AGENT_LOCK" acquire --any \
  "shared-pool/slot-1" "shared-pool/slot-2" "shared-pool/slot-3" \
  --owner "task/researcher-1" --activity "One check" \
  --receipt .agent_sources/locks/researcher-1-lock.json --wait-seconds 50
```

The call waits in every named key's queue at once, so the first key released goes to the oldest
waiter across the pool; once it holds one, its tickets leave the other queues. The result's
`ownership.key` names the resource it holds, and the receipt releases that key alone. Name each key
once; several keys without `--any` are refused.

**Work on the whole pool takes a parent key and then every member's key**, in the lexicographic
order above, such as `shared-pool` followed by each `shared-pool/slot-N`, each with `--priority`
when the work lets the pool's waiters in. It starts only once no member is held, and holding the
parent key keeps a second such operation from interleaving with it.

## Waiting and expiry

- Acquisition exit `0` / `status: acquired` grants ownership. Exit `2` / `status: busy` means the resource is still held; never touch it while waiting. Exit `1` indicates an error. `consume` also propagates command failures, so inspect the result rather than treating every exit `2` as contention.
- **Waiters are served in arrival order.** A call that has to wait takes a place in the key's queue, and a released or expired lock goes only to the waiter at its front. A busy result reports `queue_position`, and `status` lists every waiter by position.
- **Work on the resource itself that lets the waiters in takes `--priority`**, such as resizing, restarting or repairing the shared machine they are all waiting for. Its ticket goes ahead of every ordinary waiter, behind any earlier priority ticket, and takes the lock as soon as the current holder releases it. Never use it for ordinary work, which only moves one waiter's wait onto the others.
- **A bounded-call waiter keeps its place by calling again at once with the same `--receipt`.** The receipt path is the place in the queue. A waiter's place lapses when its process dies, or 30 seconds after a busy result with no new call, and the next waiter moves up. So never sleep outside the tool and come back; work done between calls instead gives up the place once those 30 seconds pass.
- `check --receipt <path>` verifies ownership before a group of external actions, especially after waiting. It does not refresh the deadline. A failed check means stop; the old receipt cannot release a successor's lock. Acquisition is non-reentrant.
- JSON results include typed ownership records with ISO-8601 timestamps. `status "shared-resource"` reports `available`, `held`, or `expired` with the deadline and remaining seconds. Expired locks become claimable automatically; no recovery CLI or file deletion is needed. Never unlink mutex files, because waiters rely on their stable inode.
- Expiry invalidates ownership but cannot close an external desktop/browser session left behind by a separate tool. If acquisition reports `expired_owner`, the orchestrator must stop any still-running old worker and bring the resource to a known idle state before giving the successor permission for input. Never let the previous owner clean up after the successor starts using it.
- Use a unique receipt under the task's working-files folder, such as `.agent_sources/locks/`, for each acquisition. Share it only with the assigned worker and its orchestrator; never commit lock state. Keep expiry/cleanup blockers in the task evidence.
