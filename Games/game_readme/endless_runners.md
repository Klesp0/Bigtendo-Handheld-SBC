# 🏃 Endless Runner

## Overview
Chrome Dino-style endless runner with desert theme. Jump and slide to avoid obstacles while running at increasing speed.

## Gameplay
- **Objective**: Run as far as possible without hitting obstacles
- **Controls**: 
  - **SPACE / A button**: Jump
  - **DOWN / Crouch button**: Slide
- **Scoring**: Distance traveled (meters)
- **Difficulty**: Speed increases over time

## Features
- ✅ Procedural obstacle generation
- ✅ Running, jumping, sliding animations
- ✅ Parallax scrolling background
- ✅ Collectible coins
- ✅ Power-ups (magnet, shield)
- ✅ Day/night cycle
- ✅ High score tracking

## Technical Details
- **Languages**: GDScript
- **Scenes**: 
  - Main.tscn (game world)
  - Player.gd (character controller)
  - ObstacleSpawner.gd (procedural generation)

## Assets Required
- Player sprites: run (4 frames), jump, slide
- Obstacles: cactus (3 variants), bird, rock
- Backgrounds: sky, mountains (2 layers), ground
- Collectibles: coin (3 frame animation)
- Power-ups: magnet, shield icons

## Development Time
**Estimated**: 4-5 hours
- Player movement: 1h
- Obstacle spawning: 1.5h
- Collision detection: 1h
- UI & polish: 1.5h

## Testing Checklist
- [ ] Jump feels responsive
- [ ] Slide animation works
- [ ] Obstacles spawn at correct intervals
- [ ] Collision detection accurate
- [ ] Score increments properly
- [ ] Game over screen shows
- [ ] High score saves