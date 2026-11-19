# Obbies

The `roblox-game-overview` skill's pages for an obstacle course: a run through stages with
checkpoints, such as a tower climb whose floors each add a new hazard.

## Pages

- **Stages.** A `tree` by world or section, then stage, each stage's dialog holding the stage staged
  in the game from the checkpoint's view, its hazards and the skill each one asks (timed jumps,
  moving platforms, conveyors), its checkpoint, and its difficulty as the source rates it.
- **Route.** A `diagram` of the stages in order with every branch, shortcut and skip the game
  offers, and what a skip costs.
- **Hazards.** A `table` of each hazard type with what it does, the stages that use it and its
  settings, such as kill on touch or knockback.
- **Rewards.** Badges, trails or coins per stage or milestone, on How to play.

## Consistency

- Stages are numbered without gaps or duplicates, and every stage has a checkpoint the next one
  follows.
- Every skip or shortcut lands on a stage that exists, after the stage it leaves.
- Each badge or reward names a stage that exists and is given where its text says.
