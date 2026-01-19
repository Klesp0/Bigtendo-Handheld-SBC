# 👻 Pac-Man

## Overview
Classic Pac-Man maze game with 4 ghosts (Blinky, Pinky, Inky, Clyde). Eat pellets, avoid ghosts, use power-ups.

## Gameplay
- **Objective**: Eat all pellets without getting caught by ghosts
- **Controls**: 
  - **Arrow keys / D-Pad**: Move Pac-Man
- **Scoring**: 
  - Small pellet: 10 points
  - Power pellet: 50 points
  - Ghost: 200/400/800/1600 points (combo)
  - Fruit: 100-1000 points
- **Lives**: 3

## Features
- ✅ Classic maze layout
- ✅ 4 ghosts with unique AI
- ✅ Power pellets (eat ghosts)
- ✅ Fruit bonus items
- ✅ Ghost house behavior
- ✅ Scatter/Chase mode switching
- ✅ Warp tunnels
- ✅ Death/respawn animation
- ✅ Level progression

## Technical Details
- **Engine**: Godot 4.3
- **Grid-based movement**: 32x32 tiles
- **AI Algorithms**:
  - **Blinky**: Chases Pac-Man directly
  - **Pinky**: Targets 4 tiles ahead of Pac-Man
  - **Inky**: Uses Blinky's position + Pac-Man
  - **Clyde**: Chases until close, then scatters
- **Pathfinding**: BFS (Breadth-First Search)

## Ghost AI States
1. **Scatter**: Each ghost targets corner
2. **Chase**: Hunt Pac-Man with unique strategy
3. **Frightened**: Run away (after power pellet)
4. **Eyes**: Return to ghost house after eaten

## Assets Required
- Pac-Man: 8 directional sprites, death animation
- Ghosts: 4 colors x 4 directions, frightened state, eyes
- Maze: tileset for walls, pellets, power pellets
- Fruit: cherry, strawberry, orange, apple
- UI: lives indicator, score, ready text

## Development Time
**Estimated**: 7-9 hours
- Maze & movement: 2h
- Ghost AI (basic): 3h
- Ghost AI (advanced): 2h
- Power pellets & scoring: 1h
- UI & polish: 1h

## Testing Checklist
- [ ] Pac-Man moves in 4 directions
- [ ] Can't move through walls
- [ ] Eats pellets correctly
- [ ] Ghosts chase properly
- [ ] Power pellets work
- [ ] Eating ghosts gives points
- [ ] Warp tunnels work
- [ ] Level completes when all pellets eaten
- [ ] Lives system works
- [ ] Game over at 0 lives

## Known Issues
- Ghost AI can get stuck in corners (workaround: add random scatter)