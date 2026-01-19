# 🃏 Memory Game

## Overview
(Pexeso). Flip cards, find matching pairs.

## Gameplay
- **Objective**: Match all pairs
- **Controls**: 
  - **Arrow keys / D-Pad**: Move cursor
  - **SPACE / A button**: Flip card
- **Scoring**: Fewer moves = higher score
- **Grid**: 4x4 (8 pairs) or 6x6 (18 pairs)

## Features
- ✅ Card flip animation
- ✅ Match detection
- ✅ Move counter
- ✅ Timer
- ✅ Difficulty levels (4x4, 6x6)
- ✅ High score (fewest moves)

## Technical Details
- **Key Functions**:
  - `flip_card()`: Animate flip
  - `check_match()`: Compare cards
  - `shuffle_cards()`: Randomize

## Card Types (8 pairs)
- Apple, Banana, Cherry, Grape
- Orange, Strawberry, Watermelon, Pineapple

## Assets Required
- Card back: 100x100 (purple with pattern)
- Card faces: 8 fruits (100x100 each)
- UI: move counter, timer display

## Development Time
**Estimated**: 2-3 hours
- Grid & cards: 1h
- Flip animation: 0.5h
- Match logic: 0.5h
- UI & polish: 1h

## Testing Checklist
- [ ] Cards shuffle randomly
- [ ] Cursor moves
- [ ] Cards flip on select
- [ ] Matching works
- [ ] Non-matching cards flip back
- [ ] Move counter accurate
- [ ] Timer works
- [ ] Win condition works