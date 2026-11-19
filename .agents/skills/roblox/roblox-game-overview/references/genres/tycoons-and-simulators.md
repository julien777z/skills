# Tycoons and Simulators

The `roblox-game-overview` skill's pages for a game whose play is a growth loop: earn, buy what
earns faster, unlock the next area, often with rebirths that reset progress for a multiplier — such
as a bakery tycoon whose ovens pay for bigger ovens, or a pet simulator that hatches eggs to mine
faster.

## Pages

- **Economy loop.** A `diagram` of what earns and what each earning buys, from the source's prices
  and rates, with its numbered steps. A `table` of every purchasable upgrade, machine or tool with
  its price, what it adds per second or per click, and the time a player at the previous tier needs
  to afford it.
- **Areas or zones.** A `tree` of each zone with its picture, its unlock price or requirement,
  what can be collected or bought there and the creatures or nodes it holds.
- **Collectibles.** Pets, tools or eggs as a `tree` by rarity or egg, each with its picture, odds,
  stats and where it is obtained.
- **Rebirths.** What a rebirth resets, what it keeps and the multiplier each one gives, as a `table`.

## Consistency

- Every price and rate is positive, and every tier costs more than the one before it.
- Each zone's unlock is affordable from what the earlier zones pay; flag a gap a player cannot
  close without a purchase the game does not sell.
- Odds in each egg or pool add up to the whole.
- Every item a shop, egg or reward names is defined.
