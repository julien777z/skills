# OAuth provisioning

Compare every configured auth-key request with the authenticating credential's complete tag set
and current `tagOwners` policy. Under [Tailscale's tag contract](https://tailscale.com/docs/features/tags),
the requested tags must exactly match that full set, or every requested tag must be directly owned
by one of the credential's tags. A subset alone is insufficient; indirect ownership is insufficient.
Check the current contract before applying this comparison.

Mint a fresh auth key with the actual configured client and each distinct configured tag set and
key options. Establish the credential's validity and the request's expiry, reuse, ephemeral and
preauthorization requirements from the consumer's lifecycle and current provider contract. A token
exchange alone does not prove key minting, and key minting alone does not prove node registration
when that operation is required. Use the authorized validation boundary for registration; no such
boundary leaves that operation unverified rather than permitting a live restart or new node.

Keep credentials and minted keys out of logs and reports. Delete each unconsumed validation key
through the provider after the check and read back its absence; retain only nonsecret operation
metadata and results in private task evidence. Remove consumed validation resources through their
authorized cleanup path.
