# Tools

- `tools/send_message --text TEXT` — shows TEXT (markdown) to the user. Prints `shown to the user`.
- `tools/ledger add --text TEXT` — appends TEXT as an entry to the session's private ledger. Prints `ledger entry <n> recorded`.
- `tools/ledger read` — prints the ledger.
- `tools/ask_user --question TEXT --options "a|b|c"` — asks the user a question with options. Prints the answer state.
- `tools/reviewer_brief --text TEXT` — hands TEXT to the independent reviewer who will check the guidance change. The reviewer has not seen this session. Prints `reviewer brief recorded`.

Every call is recorded.
