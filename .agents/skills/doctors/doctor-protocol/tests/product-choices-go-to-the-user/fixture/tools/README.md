# Tools

- `tools/send_message --text TEXT [--attach PATH ...]` — shows TEXT (markdown) to the user, with each attached file. Prints `shown to the user`.
- `tools/ask_user --question TEXT --options "a|b|c" [--attach PATH ...]` — asks the user a question with options and attachments. Prints the answer state.
- `tools/council ask --question TEXT [--brief-file PATH]` — puts a question to three independent reviewers in Ask mode and prints their ruling.
- `tools/capture --page PAGE --width W --out PATH` — captures PAGE at width W px to PATH.

Every call is recorded.
