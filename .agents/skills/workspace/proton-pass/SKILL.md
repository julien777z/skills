---
name: proton-pass
description: Retrieve credentials from Proton Pass with pass-cli. Use every time a task needs to log in to an account, website, service, or tool, or needs a password, API key, token, SSH key, or other secret that neither the session environment nor the repository supplies, before asking the user for it.
short_description: 'Retrieve credentials from Proton Pass with pass-cli.'
---

# Proton Pass

A credential the session environment already holds, or one the repository supplies, is used from
there: an injected token, a password file project guidance names, or a helper the repository's
tooling uses to set or generate a local or development test identity's password. A test identity a
local stack or dev container creates never comes from Proton Pass. Every other account credential
comes from Proton Pass through `pass-cli`, signed in with the personal access token in
`PROTON_PASS_PERSONAL_ACCESS_TOKEN`, before the user is asked. Never ask the user to paste a secret
into chat.

## Sign In

1. **Check the CLI.** Run `pass-cli --version`. When it is missing, install it with the official
   script from the [installation guide](https://protonpass.github.io/pass-cli/get-started/installation/)
   and put its install directory on `PATH`.
2. **Use one isolated session directory and a key store the machine supports.** Choose the
   directory name once per task and export the same values in every shell that runs `pass-cli`;
   a new name per shell starts an empty session and forces a fresh login each time:

   ```sh
   export PROTON_PASS_SESSION_DIR="/tmp/pass-agent-<task-name>"
   export PROTON_PASS_KEY_PROVIDER=fs  # only where no system keyring is available
   ```

   A headless container has no system keyring; `pass-cli` then fails with `Could not get local
   key from keyring` until `PROTON_PASS_KEY_PROVIDER=fs` is set.
3. **Check the session.** `pass-cli info` exits 0 with the session details when one is active.
4. **Log in when it is not.** Confirm `PROTON_PASS_PERSONAL_ACCESS_TOKEN` is set; when it is
   missing, stop and tell the user to add it to the environment's variables, because the run cannot
   sign in without it. Then run `pass-cli logout --force` to clear a stale session, and
   `pass-cli login`, which reads the token from that variable. Never put the token on the command
   line, in a file, or in any output.
5. **Verify.** Run `pass-cli info`, then `pass-cli vault list`; seeing the vaults confirms access.
   When the list is empty or errors, report the exact error to the user.

## Session Health

- A token session lasts about two hours. Run `pass-cli info` before each `pass-cli` command in a
  long task, and repeat steps 3–5 when it fails.
- When any command fails, read its whole output before retrying: an authentication error means
  signing in again, while a permission or argument error does not.
- `pass-cli test` checks the connection to the Proton Pass API.

## Finding Items

Use `--output json` whenever the output is parsed.

```sh
pass-cli vault list --output json                     # vaults this token can read
pass-cli share list --output json                     # vaults and single items shared with it
pass-cli item list --vault-name "<vault>" --output json
pass-cli item list --output json                      # every accessible item
```

## Reading And Changing Items

`item view`, every `item create` subcommand, `item update`, `item trash`, `item untrash`, and
`vault update` require `PROTON_PASS_AGENT_REASON`, a short statement of why this item is needed
for the current task:

```sh
PROTON_PASS_AGENT_REASON="<why this task needs it>" pass-cli item view \
  --vault-name "<vault>" --item-title "<title>" --field password
PROTON_PASS_AGENT_REASON="<why>" pass-cli item view "pass://<share-id>/<item-id>"
```

- Read only the field the task needs with `--field`.
- Hand a secret straight to the command or form that uses it, through an environment variable or
  standard input, never as a command-line argument such as `--password "$secret"`, which other
  processes can read; when writing an item, use the input mode `pass-cli item create --help` lists
  for standard input or a template. Never echo a secret, write it to a file, commit it, or repeat it
  in a message.
- Create, update, or trash an item only when the user asked for that change.

`pass-cli agent instructions` prints the CLI's current guidance for agents, and the
[documentation](https://protonpass.github.io/pass-cli/) covers every command.
