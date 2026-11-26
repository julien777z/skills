Intent: `fetch_rates()` retries up to 3 times with a 2 s delay when the rates provider times out, so a
single timeout no longer fails the nightly import. After the third failure the error must still reach the
caller. Note: the Codex runtime kills any task that is silent for more than 30 s.
