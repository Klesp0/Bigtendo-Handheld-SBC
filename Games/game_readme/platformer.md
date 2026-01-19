# 🎮 Platformer

## Overview
2D platformer inspired by Super Mario. Jump, run, collect coins, defeat enemies, reach the flag.

## Gameplay
- **Objective**: Reach the end flag
- **Controls**: 
  - **Arrow keys / D-Pad**: Move left/right
  - **SPACE / A button**: Jump
  - **DOWN**: Crouch
- **Mechanics**:
  - Double jump
  - Wall jump
  - Ground pound
  - Enemy stomp
- **Collectibles**: Coins, gems, keys
- **Lives**: 3 (get more at 100 coins)

## Features
- ✅ Physics-based movement
- ✅ Multiple enemy types
- ✅ Destructible blocks
- ✅ Moving platforms
- ✅ Checkpoints
- ✅ Secret areas
- ✅ Boss fight (optional)
- ✅ 3-5 levels

## Technical Details
- **Engine**: Godot 4.3
- **Tilemap**: 32x32 grid
- **Physics**: Godot's built-in CharacterBody2D
- **Key Scripts**:
  - Player.gd (movement, jumps, attacks)
  - Enemy.gd (patrol, chase AI)
  - MovingPlatform.gd (path following)
  - Checkpoint.gd (save progress)

## Player Abilities
```gdscript
const SPEED = 200.0
const JUMP_VELOCITY = -500.0
const DOUBLE_JUMP_VELOCITY = -400.0
const GRAVITY = 980.0
const WALL_SLIDE_SPEED = 50.0
```

## Enemy Types
- **Slime**: Patrols back and forth
- **Flying**: Sine wave pattern
- **Spikes**: Stationary hazard
- **Boss**: Multi-phase fight (if time permits)

## Assets Required
- Player: idle, walk (4 frames), run (4 frames), jump, fall, crouch, hurt, death
- Enemies: slime (2 frames), fly (2 frames), spike
- Tiles: ground, platforms, walls, spikes, coins, gems, key, door, flag
- Backgrounds: sky, clouds, mountains, trees
- Effects: jump dust, landing dust, hit effect

## Development Time
**Estimated**: 6-8 hours
- Player movement: 2h
- Tilemap & level design: 2h
- Enemy AI: 2h
- Collectibles & checkpoints: 1h
- Polish & sound: 1h

## Level Design Tips
- Start easy, increase difficulty gradually
- Teach mechanics before requiring them
- Place checkpoints after difficult sections
- Hide secrets off the main path
- Add visual hints (coins leading to platforms)

## Testing Checklist
- [ ] Jump feels good (height, gravity)
- [ ] Wall jump works
- [ ] Double jump works
- [ ] Enemy collisions work
- [ ] Stomp kills enemies
- [ ] Touching enemy hurts player
- [ ] Coins collected properly
- [ ] Checkpoints save progress
- [ ] Death respawns at checkpoint
- [ ] Can reach flag

## Known Issues
- Player can get stuck in walls if moving too fast (add collision buffer)