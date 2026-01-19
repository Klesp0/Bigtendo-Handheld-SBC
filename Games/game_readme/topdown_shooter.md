# 🔫 Top-Down Shooter

## Overview
Hotline Miami-style top-down shooter. Aim with mouse/joystick, shoot enemies, clear rooms.

## Gameplay
- **Objective**: Clear all enemies in each room
- **Controls**: 
  - **Arrow keys / Left stick**: Move (8-way)
  - **Mouse / Right stick**: Aim
  - **SPACE / A button**: Shoot
  - **R**: Reload
- **Weapons**: Pistol, Rifle, Shotgun
- **Health**: 100 HP
- **Scoring**: Kills, accuracy, time bonus

## Features
- ✅ 8-way movement
- ✅ Mouse/joystick aiming
- ✅ 3 weapon types
- ✅ Enemy AI (patrol, chase, shoot)
- ✅ Line of sight system
- ✅ Destructible objects
- ✅ Multiple rooms/levels
- ✅ Ammo management
- ✅ Health pickups
- ✅ Blood effects

## Technical Details
- **Engine**: Godot 4.3
- **View**: Top-down orthogonal
- **Key Scripts**:
  - Player.gd (movement, aiming, shooting)
  - Enemy.gd (AI state machine)
  - Weapon.gd (fire rate, damage, ammo)
  - Bullet.gd (projectile physics)

## Weapon Stats
```gdscript
# Pistol
damage = 20
fire_rate = 0.3
ammo_capacity = 12
reload_time = 1.5

# Rifle
damage = 15
fire_rate = 0.1
ammo_capacity = 30
reload_time = 2.0

# Shotgun
damage = 10 (x6 pellets)
fire_rate = 0.8
ammo_capacity = 6
reload_time = 2.5
```

## Enemy AI States
1. **Patrol**: Walk along waypoints
2. **Alert**: Player spotted, move to last seen position
3. **Chase**: Follow player
4. **Attack**: Stop and shoot at player
5. **Cover**: Hide behind obstacles when low health

## Assets Required
- Player: idle (4 directions), walk (4 directions x 2 frames)
- Enemies: soldier, robot, turret
- Weapons: pistol, rifle, shotgun sprites
- Bullets: small projectile, muzzle flash
- Environment: walls, crates, doors, barrels
- Effects: blood splatter, explosion, smoke
- UI: health bar, ammo counter, crosshair

## Development Time
**Estimated**: 8-10 hours
- Player controller: 2h
- Enemy AI: 3h
- Weapons & shooting: 2h
- Level design: 2h
- Polish: 1h

## Level Design
- Start with tutorial room (1 enemy)
- Gradually increase enemy count
- Mix enemy types for variety
- Place cover strategically
- Add health/ammo pickups after tough fights

## Testing Checklist
- [ ] Mouse aiming smooth
- [ ] Joystick aiming works
- [ ] Shooting feels responsive
- [ ] Enemies chase properly
- [ ] Line of sight works
- [ ] Cover system works
- [ ] Ammo system works
- [ ] Reload works
- [ ] Health system works
- [ ] Death/respawn works

## Known Issues
- AI can get stuck on corners (add navigation mesh)