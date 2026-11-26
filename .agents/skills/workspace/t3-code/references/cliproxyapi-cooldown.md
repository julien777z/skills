# CLIProxyAPI cooldown recovery

1. Read the failing T3 request's environment, provider instance, model, and error. Inspect the
   effective provider endpoint on that environment. Resolve its address and identify the running
   proxy that serves it, using service routing, runtime identity, or a matching request log. A
   localhost listener, a matching service name, or an HTTP success from another proxy does not
   identify the request path. If needed, reproduce with a short prompt in a separate T3 chat.
2. Match the provider account's identity, including its organization when relevant, to one entry
   in the active proxy's credential list and resolve its `auth_index`. A display name or pooled
   usage total alone cannot identify the account. Read every active routing cooldown on that
   credential, including model-specific blocks. Use the user's confirmed reset as evidence for
   the matching account and allowance. If the user's instructions already identify the reset,
   carry that evidence forward without asking them to repeat it. Compare the reset with the
   proxy's recorded reason and timing to determine which blocks are stale. Keep a cooldown
   supported by a newer provider rejection or a separate active limit.

   Skip quota endpoint calls, including calls relayed through the proxy. A cached quota reading
   from before the reset or a quota lookup's HTTP 429 does not establish an active inference
   limit. If the account or an affected block remains unclear, continue with available account
   and routing evidence and resolve the specific uncertainty before acting. The reset clears
   the entire credential's routing cooldowns, so use it only when every active block it would
   remove is stale.
3. For a confirmed stale cooldown, use **Clear cooldown** on that credential in the active
   proxy's management page. For a supported CLIProxyAPI v8 installation, the management API
   lists credentials with `GET /v8/management/credentials` or the installed version's
   equivalent. Clear the selected entry with `POST /v8/management/routing/cooldown/reset` and
   JSON body `{"auth_index":"<matched index>"}`. Check the
   [management API contract](https://github.com/router-for-me/CLIProxyAPI/blob/main/docs/management-api-v8.md)
   for the running version. Use the credential for that instance's management API through its
   existing authorized route. Keep the key and account identifiers out of logs and reports.
   If authentication is temporarily locked, wait for the reported expiry before retrying with
   the verified key. Do not restart the proxy, change its routing settings, or spend a second
   allowance reset to clear this state.
4. Read back the credential's routing state and verify the blocking cooldown is gone. If the
   separate test chat is still snoozed, use **Wake now** there and send a short prompt using the
   same model and provider instance on the affected T3 environment. A completed model reply
   verifies recovery. If the turn fails, match the new error to the active proxy and the upstream
   provider before taking another action.
