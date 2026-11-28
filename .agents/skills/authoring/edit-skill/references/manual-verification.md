# Manual Verification

How this skill verifies skill behavior that needs a live agent chat: choosing and recording the
dispatch, then the procedure for each host.

When skill behavior needs a live agent chat, use `subagent-matrix` to choose the least-capable
sufficient capability and resolve its exact model ID. Select that ID in the chat UI and record its
**Output** dispatch line with the tested branch, exact commit, session type and observed result. A
missing ID or any refusal holds manual verification rather than selecting a substitute. A resumed
container proves its maintenance path, not a fresh setup run.

## Claude Desktop

1. In Claude Desktop's Code view, choose Remote, open the environment picker, and use the settings
   control beside the selected environment to edit its setup script. Check out the pull-request
   branch and invoke the installer from that checkout. Preserve unrelated setup commands and
   settings; save the script and verify the editor reports the update.
2. Start a new cloud session with the pull-request branch attached. Verify from session evidence
   that setup ran the script at the intended commit, then check the skill and rule used by the
   session resolve into the intended checkout in both Claude's cloud home and the runtime's home.
   If the session reused an older setup image, record that result and obtain a fresh setup run
   before claiming setup passed.
3. After the source pull request merges and the verification task is finalized and closed, update
   the remote setup script to check out the repository's default branch. Save the script. Remove
   only stale test sessions created for this verification:
   right-click each session in Claude Desktop and delete it through the UI, one at a time; never
   use a script or API to delete sessions.

## Codex Cloud

1. In Codex cloud Settings → Environments, create or edit an environment attached to the repository.
   Set its setup script to obtain the Skills checkout on the pull-request branch and invoke its
   installer. Set its maintenance script to invoke the same installer on a resumed container. Keep
   the network access needed by the test.
2. Start a fresh task on the pull-request branch. Verify the installed skill and shared rule links,
   and Codex's global `AGENTS.md`, resolve into the installed checkout at the intended commit.
   Run the installer again and verify it succeeds without changing unrelated content.
3. Resume a cached container and verify the maintenance script ran and the same links still resolve.
   Distinguish this result from a fresh setup result.
4. After the source pull request merges and the verification task is finalized and closed, update
   the environment setup script to obtain the Skills checkout on the repository's default branch.
   Save the script. Archive test tasks created for this verification.
