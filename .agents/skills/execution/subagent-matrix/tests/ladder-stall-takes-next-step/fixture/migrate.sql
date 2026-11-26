-- 3.0: add settlement currency
BEGIN;
ALTER TABLE ledger_entries
  ADD COLUMN settlement_currency CHAR(3) NOT NULL;
UPDATE ledger_entries SET settlement_currency = currency;
COMMIT;

BEGIN;
CREATE INDEX settlement_idx ON ledger_entries (settlement_currency);
COMMIT;
