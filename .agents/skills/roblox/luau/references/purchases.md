# Purchase integrity for future authorized monetization

Adapted from the [template purchase guidance](https://github.com/Uglypoe/roblox-game-template/blob/main/.claude/purchases.md). Add this system only when requested, checking Roblox's current receipt APIs first.

Give one server owner the receipt handler and game-pass checks behind a typed marketplace port. Keep product IDs in feature contracts with separate staging/production values. Never grant from a client purchase prompt or a client-reported success; show results from authoritative saved state.

A developer-product grant changes only owned profile data and must not yield. Record the purchase ID atomically with that change. Confirm processing only after durable saved data contains the receipt; loss of ownership or failed saves leave it unprocessed for Roblox to retry. Repeated receipt delivery must not repeat rewards. Missing players, unavailable profiles, unknown products, and unlisted/nonpersistent environments must not acknowledge an unsaved grant.

Keep receipt history bounded with an explicit retention rationale; truncation can permit a very old redelivery to grant again. Do not copy the template's numeric limit without assessing the game's actual purchase volume and durability contract. Defer tools, UI, and announcements until the saved grant is established.

Cache successful game-pass ownership for the current session. Do not cache a transient lookup failure as authoritative absence. Apply newly purchased pass perks and joining-player perks through the same policy.

Test duplicate receipts, failed saves, session loss, delayed profile availability, registration errors, and unknown environments against fakes, then verify the real engine adapter separately. Studio test purchases/mock saves are distinct from persistent staging behavior. Follow the Luau skill's current save policy rather than importing a migration framework.
