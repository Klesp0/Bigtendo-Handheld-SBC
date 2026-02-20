# 👾 Space Invaders

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

# Speed up as aliens die
alien_speed = base_speed * (1 + (total_aliens - alive_aliens) * 0.1)

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