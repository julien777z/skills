# Manual Verification

How this skill verifies skill behavior that needs a live agent chat: choosing and recording the
dispatch, then the procedure for each host.

When skill behavior needs a live agent chat, select the dispatch identifier the entry point
resolved in the chat UI and
record catalog state, dispatch identifier, assignment state and receipt, tested branch, exact commit, session
type, and observed result separately. A catalog-hidden candidate remains dispatch-required until the actual
chat assignment is accepted; a missing identifier or any rejection other than an explicit unsupported receipt
holds manual verification rather than selecting a substitute. An explicit unsupported receipt records the chat
as unavailable and keeps manual verification blocked. A resumed container proves its maintenance path, not a
fresh setup run.

## Claude Desktop

1. Edit the remote environment's setup script so it checks out the pull-request branch and invokes
   the installer from that checkout. Preserve unrelated setup commands and settings; save the
   script and verify the editor reports the update.
2. Start a new cloud session with the pull-request branch attached. Verify from session evidence
   that setup ran the script at the intended commit, then check the skill and rule used by the
   session resolve into the intended checkout in both Claude's cloud home and the runtime's home.
   If the session reused an older setup image, record that result and obtain a fresh setup run
   before claiming setup passed.
3. After the source pull request merges and the verification task is finalized and closed, update
   the remote setup script to check out the repository's default branch. Save the script. Remove
   only stale test sessions created for this verification: right-click each in Claude Desktop and
   delete it through the UI, one at a time, so a bulk call cannot remove a session this
   verification did not create.

## Codex Cloud

1. Create or edit an environment attached to the repository. Its setup script obtains the Skills
   checkout on the pull-request branch and invokes its installer; its maintenance script invokes
   the same installer on a resumed container; it keeps the network access the test needs.
2. Start a fresh task on the pull-request branch. Verify the installed skill and shared rule links,
   and Codex's global `AGENTS.md`, resolve into the installed checkout at the intended commit.
   Run the installer again and verify it succeeds without changing unrelated content.
3. Resume a cached container and verify the maintenance script ran and the same links still resolve.
   Distinguish this result from a fresh setup result.
4. After the source pull request merges and the verification task is finalized and closed, update
   the environment setup script to obtain the Skills checkout on the repository's default branch.
   Save the script. Archive test tasks created for this verification.
