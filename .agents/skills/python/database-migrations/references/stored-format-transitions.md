# Stored-Format Transitions

Apply this section when a revision transforms values retained under **Data Scope**. A schema-only
change still tests its schema upgrade and downgrade; generated rows do not require a value-preserving
format transition or recovery mechanism for data explicitly declared disposable or nonexistent.

- A migration reads the representation stored by the revision immediately before it, not the ORM or
  decoder as they exist after the application change. Prepare tests with raw pre-revision values so an
  expected old format cannot reach a new decoder and abort the upgrade.
- Test the transition in both directions: upgrade real old-format values into the new representation,
  verify their domain value under the new reader, downgrade real new-format values, and verify the old
  reader sees the original domain value again. Compare stored bytes too when the operation promises to
  move rather than rewrite them.
- When a migration can commit in batches, call an external service, resume after failure, or encounter
  legitimately mixed storage, recognize both representations explicitly. Treat an already-converted
  row as complete and transform only the old representation; test mixed rows and retrying the operation.
- An encryption change carries every decrypt capability needed for the old ciphertext through the
  rewrite and verifies ciphertext written for the new backend or key. Do not switch configuration first
  and then assume the new backend can decode the value being replaced. Downgrade either restores the
  original ciphertext or re-encrypts the same plaintext for the old reader with a tested key path.
- Never classify a row as malformed merely because it has the format the migration exists to replace.
  An unconvertible row fails the revision with its sensitive value omitted from logs; it is never
  silently skipped, nulled, or deleted.
