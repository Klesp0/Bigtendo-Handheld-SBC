# 🗼 Tower Defense

## Overview
Classic tower defense. Build towers, upgrade them, stop enemy waves from reaching your base.

## Gameplay
- **Objective**: Survive all waves without losing all lives
- **Controls**: 
  - **Mouse / D-Pad**: Select tower, place on map
  - **Click tower**: Upgrade or sell
- **Resources**: 
  - **Money**: Build/upgrade towers
  - **Lives**: Lose when enemies reach end
- **Towers**: Basic, Cannon, Laser, Ice
- **Enemies**: Basic, Fast, Tank, Flying

## Features
- ✅ 4 tower types (3 upgrade levels each)
- ✅ 4 enemy types
- ✅ Path-based enemy movement
- ✅ Tower range indicators
- ✅ Upgrade system
- ✅ Sell towers (50% refund)
- ✅ 10-15 waves
- ✅ Speed up button (2x)
- ✅ Pause menu

## Technical Details
- **Engine**: Godot 4.3
- **Pathfinding**: Predefined path (not A*)
- **Key Scripts**:
  - Tower.gd (targeting, shooting, upgrading)
  - Enemy.gd (path following, health)
  - WaveManager.gd (spawn timing, difficulty scaling)
  - GameManager.gd (money, lives, win/lose)

## Tower Stats

### Basic Tower
- **Cost**: 100
- **Damage**: 10 → 20 → 30
- **Fire Rate**: 1.0s → 0.8s → 0.6s
- **Range**: 150 → 170 → 200

### Cannon Tower
- **Cost**: 200
- **Damage**: 50 → 80 → 120 (AOE)
- **Fire Rate**: 2.0s → 1.5s → 1.0s
- **Range**: 180 → 200 → 220

### Laser Tower
- **Cost**: 250
- **Damage**: 5 (continuous)
- **Fire Rate**: 0.1s
- **Range**: 200 → 220 → 250

### Ice Tower
- **Cost**: 150
- **Damage**: 5 → 10 → 15
- **Slow**: 50% → 60% → 70%
- **Range**: 120 → 140 → 160

## Enemy Types
- **Basic**: 100 HP, 50 speed, 10 reward
- **Fast**: 60 HP, 100 speed, 15 reward
- **Tank**: 300 HP, 30 speed, 30 reward
- **Flying**: 80 HP, 70 speed, 20 reward (immune to ground towers)

## Wave Scaling
```gdscript
func calculate_wave_difficulty(wave_num):
    enemy_count = 5 + wave_num * 2
    enemy_health_multiplier = 1.0 + wave_num * 0.1
    enemy_speed_multiplier = 1.0 + wave_num * 0.05
```

## Assets Required
- Towers: 4 types x 3 levels = 12 sprites
- Tower projectiles: bullet, cannonball, laser beam, ice shard
- Enemies: 4 types x 2 frames = 8 sprites
- Map tiles: grass, path
- UI: tower menu, upgrade panel, money/lives display
- Effects: explosion (3 frames), ice effect

## Development Time
**Estimated**: 10-12 hours
- Tower system: 3h
- Enemy pathfinding: 2h
- Wave manager: 2h
- Upgrade system: 2h
- UI & map: 2h
- Balancing: 1h

## Balancing Tips
- Early waves should be easy (teach mechanics)
- Introduce 1 new enemy type every 3 waves
- Boss waves at 5, 10, 15
- Money rewards should allow 1 tower per wave
- Player should need 3-4 upgraded towers to win

## Testing Checklist
- [ ] Towers place correctly
- [ ] Range indicators show
- [ ] Towers shoot enemies in range
- [ ] Targeting works (closest, strongest, etc.)
- [ ] Upgrades apply correctly
- [ ] Selling works
- [ ] Enemies follow path
- [ ] Money system works
- [ ] Lives decrease when enemy reaches end
- [ ] All waves completable
- [ ] Win condition works
- [ ] Lose condition works

## Known Issues
- Towers can shoot through obstacles (add line-of-sight check)