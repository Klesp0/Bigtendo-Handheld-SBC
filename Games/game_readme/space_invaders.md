# 👾 Space Invaders

## Overview
Classic Space Invaders. Shoot aliens, avoid bullets, protect shields.

## Gameplay
- **Objective**: Destroy all aliens
- **Controls**: 
  - **Arrow keys / D-Pad**: Move ship
  - **SPACE / A button**: Shoot
- **Lives**: 3
- **Scoring**: 
  - Top row: 30 points
  - Middle row: 20 points
  - Bottom row: 10 points
  - UFO: 50-300 points

## Features
- ✅ Alien formation movement
- ✅ Shooting (player & aliens)
- ✅ Destructible shields
- ✅ UFO bonus enemy
- ✅ Explosion animations
- ✅ Wave system
- ✅ High score

## Technical Details
- **Key Classes**:
  - `SpaceInvaders(Game)`: Main
  - `Player`: Ship control
  - `AlienGrid`: Formation logic
  - `Bullet`: Project
  
# Move all aliens together

if any_alien_hit_edge():
    move_down()
    reverse_direction()
else:
    move_horizontal()

# Speed up as aliens die
alien_speed = base_speed * (1 + (total_aliens - alive_aliens) * 0.1)

## Assets Required
- Player ship: 60x40 (triangle/spaceship)
- Aliens: 3 types, 40x40 each, 2-frame animation
- UFO: 60x30 (flying saucer)
- Bullets: 8x20 (player = yellow, alien = red)
- Shields: 80x60, 4 damage states
- Explosions: 3-frame animation (60x60)
- Background: starfield

## Development Time
**Estimated**: 5-6 hours
- Player & movement: 1h
- Alien grid & movement: 2h
- Shooting & collision: 1.5h
- Shields: 1h
- UI & polish: 0.5h

## Testing Checklist
- [ ] Player moves left/right
- [ ] Player shoots
- [ ] Aliens move in formation
- [ ] Aliens move down at edges
- [ ] Aliens shoot randomly
- [ ] Bullets hit aliens
- [ ] Alien bullets hit player
- [ ] Shields take damage
- [ ] UFO appears randomly
- [ ] Lives system works
- [ ] Wave completes when all aliens dead
- [ ] Game over works