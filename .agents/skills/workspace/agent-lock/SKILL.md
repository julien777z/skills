---
name: agent-lock
description: Coordinate exclusive use of a shared resource between agents using an exact string key, or take whichever of several interchangeable resources comes free first. Use as a dependency when concurrent agents would conflict over one VM desktop, browser session, or other shared mutable resource. Consume ownership for a command, which renews it while the command runs, or delegate a lock for a multi-tool agent task, whose holder keeps renewing it.
short_description: 'Coordinate exclusive use of a shared resource between agents using an exact string key.'
---

# Agent Lock

All agents competing for a resource use **exactly the same nonempty string key and coordinator host**. Keys are case-sensitive. Keep the key free of an assignment ID, agent name, branch or checkout when it is meant to serialize those agents, since different keys run concurrently and any added part puts the agents on separate locks.

Use [resources/main.py](resources/main.py) with Python 3.12+ on macOS or Linux. Resolve it from this skill's own directory and hold its absolute path in `AGENT_LOCK` for the commands below. State lives under `~/.local/state/agent-lock/`, outside repositories; keys are hashed into safe filenames. All checkouts share this location. `--state-dir` is for tests or an explicitly shared coordinator configuration. When controlling a VM or remote machine, acquire on the coordinator host rather than separate guest filesystems. This is a cooperative local lock, not a distributed lock or control over unrelated human activity.

## Consume ownership

Prefer ownership scoped to the actual operation. **A lock lasts as long as its holder keeps renewing it**, so nobody picks a duration in advance: a holder that is still working keeps the resource however long the work takes, and one that has died or wandered off loses it within minutes, without anyone having guessed how long the work would run. A lease is five minutes from the last acquisition or renewal; the holder renews about every minute, which leaves room for a slow call between renewals, and a lock nobody renews for five minutes expires and goes to the next waiter.

For work represented by a foreground command, use `consume`:

```sh
python3 "$AGENT_LOCK" consume "shared-resource" \
  --owner "task/researcher-1" --activity "Describe this operation" \
  --receipt .agent_sources/locks/researcher-1-lock.json --wait-seconds 50 \
  -- python3 path/to/actual_worker.py
```

The helper acquires once, renews the lock every minute while the command runs, and releases automatically when the command finishes or fails. It never stops a command for running long; it stops the command, with its process group's subprocesses, on SIGINT/SIGTERM or when a renewal finds the lock lost, since the command then no longer owns the resource. The command receives `AGENT_LOCK_RECEIPT` and sends its output to stderr; the helper writes its JSON result to stdout. Exit `124` means the lock was lost; otherwise a started command's exit code is preserved. A killed supervisor stops renewing, so its lock expires. Run the protected operation as the foreground command itself, so the lock follows its real lifetime: a daemonized or detached operation keeps running after the helper releases the lock, and a dummy sleeping process holds the lock for something that tracks no agent's lifetime.

For a researcher using several separate tools, the CLI cannot observe the logical subagent's completion by itself. **The orchestrator owns that task scope:** acquire once, give the worker its receipt, and release as part of handling the worker's completion, failure, or cancellation. **The worker renews the lock with `check` about every minute while it works**, and before each group of external actions, especially after waiting. If the host provides a real task-finalization callback, attach cleanup there; otherwise use the orchestrator's existing completion handling. Do not claim this release is automatic OS process tracking.

```sh
python3 "$AGENT_LOCK" acquire "shared-resource" \
  --owner "task/researcher-1" --activity "Interactive research" \
  --receipt .agent_sources/locks/researcher-1-lock.json --wait-seconds 50
```

Acquire immediately before the protected portion of the assignment, not before unrelated research. The orchestrator records the agent ID, resource key and receipt. Completion handling must finish or cancel the external operation, release held controls, verify the resource is idle, then run:

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
- `check --receipt <path>` verifies ownership and renews the lease. A failed check means the lock was lost: stop, since the old receipt cannot release a successor's lock. Acquisition is non-reentrant.
- JSON results include typed ownership records with ISO-8601 timestamps. `status "shared-resource"` reports `available`, `held`, or `expired` with the expiry and remaining seconds, and `last_activity_at`, when the key's lock was last acquired, renewed or released (`null` for a key never used), so a caller can tell a resource nobody has touched in a while from one in use. Expired locks become claimable automatically; no recovery CLI or file deletion is needed. Never unlink mutex files, because waiters rely on their stable inode.
- Expiry invalidates ownership but cannot close an external desktop/browser session left behind by a separate tool. If acquisition reports `expired_owner`, the orchestrator must stop any still-running old worker and bring the resource to a known idle state before giving the successor permission for input, so the old worker's cleanup cannot run against the successor's session.
- Use a unique receipt under the task's working-files folder, such as `.agent_sources/locks/`, for each acquisition. Share it only with the assigned worker and its orchestrator; never commit lock state. Keep expiry/cleanup blockers in the task evidence.
