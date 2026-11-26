# Tools

- `tools/send_message --text TEXT` — shows TEXT (markdown) to the user. Prints `shown to the user`.
- `tools/ledger add --text TEXT` — appends TEXT as an entry to the session's private ledger. Prints `ledger entry <n> recorded`.
- `tools/ledger read` — prints the ledger.
- `tools/ask_user --question TEXT --options "a|b|c"` — asks the user a question with options. Prints the answer state.

Every call is recorded.
