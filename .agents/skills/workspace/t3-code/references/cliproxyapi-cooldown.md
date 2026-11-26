# CLIProxyAPI cooldown recovery

1. Read the failing T3 request's environment, provider instance, model, and error. Inspect the
   effective provider endpoint on that environment. Resolve its address and identify the running
   proxy that serves it, using service routing, runtime identity, or a matching request log. A
   localhost listener, a matching service name, or an HTTP success from another proxy does not
   identify the request path. If needed, reproduce with a short prompt in a separate T3 chat.
2. Check fresh provider quota and the proxy's routing state for the same account. Match the
   provider account's identity, including its organization when relevant, to one entry in the
   active proxy's credential list and resolve its `auth_index`. A pooled Usage total or a matching display name does not
   identify the credential, and a quota refresh can show restored allowance while a routing
   cooldown remains. An upstream quota rejection or a still-exhausted window does not justify
   clearing the proxy's cooldown. Inspect the full cooldown list for the credential, including
   model-specific blocks. The reset clears routing cooldowns for the entire credential. Use it
   only when every active block it would clear is confirmed stale.
3. For a confirmed stale cooldown, use **Clear cooldown** on that credential in the active
   proxy's management page. For a supported CLIProxyAPI v8 installation, the management API
   lists credentials with `GET /v8/management/credentials` or the installed version's
   equivalent. Clear the selected entry with `POST /v8/management/routing/cooldown/reset` and
   JSON body `{"auth_index":"<matched index>"}`. Check the
   [management API contract](https://github.com/router-for-me/CLIProxyAPI/blob/main/docs/management-api-v8.md)
   for the running version. Use the credential for that instance's management API through its
   existing authorized route. Keep the key and account identifiers out of logs and reports.
   If authentication is temporarily locked, wait for the reported expiry before retrying with
   the verified key. Clear the cooldown through the reset call alone, leaving the proxy running
   with its routing settings and allowance as they are: a restart, a settings change or a second
   allowance reset is a different operation that this recovery does not cover.
4. Read back the credential's routing state and verify the blocking cooldown is gone. If the
   separate test chat is still snoozed, use **Wake now** there and send a short prompt using the
   same model and provider instance on the affected T3 environment. A completed model reply
   verifies recovery. If the turn fails, match the new error to the active proxy and the upstream
   provider before taking another action.
