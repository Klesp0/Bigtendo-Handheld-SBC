# 🎵 Rhythm Game

## Overview
Guitar Hero / osu!-style rhythm game. Hit notes in time with the music across 4-5 lanes.

## Gameplay
- **Objective**: Hit notes with perfect timing
- **Controls**: 
  - **1,2,3,4,5 keys OR D-Pad + buttons**: Hit corresponding lane notes
- **Scoring**:
  - **PERFECT**: ±50ms = 100 points
  - **GREAT**: ±100ms = 75 points
  - **GOOD**: ±150ms = 50 points
  - **MISS**: >150ms = 0 points
- **Combo**: Multiplier increases (x1, x2, x4, x8)
- **Health**: Miss notes = lose health, 0 health = game over

## Features
- ✅ 5-lane note highway
- ✅ Timing judgement system
- ✅ Combo multiplier
- ✅ Long notes (hold)
- ✅ 3-5 songs
- ✅ Difficulty levels (easy/medium/hard)
- ✅ Visual hit feedback
- ✅ Score ranking (F to SSS)

## Technical Details
- **Engine**: Godot 4.3
- **Resolution**: 800x480
- **Audio Sync**: Critical (use AudioStreamPlayer.get_playback_position())
- **Chart Format**: JSON with note timestamps
- **Key Scripts**:
  - NoteSpawner.gd (reads chart, spawns notes)
  - Note.gd (scrolls, checks timing)
  - ScoreManager.gd (judgement, combo, scoring)

## Chart JSON Format
```json
{
  "song": "Song Name",
  "bpm": 120,
  "offset": 0.5,
  "notes": [
    {"time": 1.0, "lane": 0, "type": "normal"},
    {"time": 1.5, "lane": 1, "type": "normal"},
    {"time": 2.0, "lane": 2, "type": "hold", "duration": 1.0}
  ]
}
```

## Timing Windows
```gdscript
const PERFECT_WINDOW = 0.05  # ±50ms
const GREAT_WINDOW = 0.10    # ±100ms
const GOOD_WINDOW = 0.15     # ±150ms
```

## Assets Required
- Note sprites: 5 colors (1 per lane)
- Long note: start, middle, end segments
- Highway background: 5 lanes with separators
- Hit judgement text: PERFECT, GREAT, GOOD, MISS
- Combo display: numbers + "COMBO" text
- Multiplier: x2, x4, x8 icons
- Hit effects: explosion/burst animation

## Development Time
**Estimated**: 8-10 hours
- Song sync & timing: 3h
- Note spawning: 2h
- Hit detection: 2h
- Scoring system: 1h
- Chart creation: 1h (per song)
- UI & polish: 1h

## Creating Charts
1. Load song in Audacity
2. Mark beats with labels
3. Export timestamps
4. Convert to JSON format
5. Playtest and adjust timing

## Testing Checklist
- [ ] Audio syncs with notes
- [ ] Hit detection accurate
- [ ] Timing windows feel fair
- [ ] Combo system works
- [ ] Long notes work
- [ ] Score calculates correctly
- [ ] Rank appears at end
- [ ] Multiple songs work

## Known Issues
- Audio sync can drift on slower hardware (use delta timing correction)