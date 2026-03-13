# CS Flashcard Game - Changelog

## Version 1.0 (Initial Release)
**Released:** *Base Version*

### Features
- **Core Flashcard Gameplay**: Basic flashcard system with term/definition pairs
- **Two Game Modes**:
  - **Normal Mode**: Reach 11 points to win (wrong answers: -2)
  - **Endless Mode**: Play until wrong answer
- **User System**: 4-digit code login/registration
- **Badge System**: 6 achievement badges
  - First Time, Fast Learner, Endless 10, Endless 25, Endless 50, Flash Master
- **Leaderboard**: Rank players by Endless Mode high score
- **Visual Effects**:
  - Floating score animations
  - Confetti on victory
  - Custom progress bar with shake animation
- **Fullscreen Support**: F11 toggle, Escape to exit

### Technical
- SQLite3 database for user data and badges
- Label-based custom buttons (cross-platform compatibility)
- Dark theme colour palette


## Version 2.0
**Released:** *Minor Update*

### Changes
- **No new features** – codebase identical to v1.0
- *Note: This version appears to be a duplicate in the provided files*

### Status
- Identical to Version 1.0


## Version 3.0 — Extended Edition
**Released:** *Major Expansion*

### Features Added
- **Expanded Flashcard Library**: 100+ new terms across categories
- **Speedrun Mode** (locked until 50 questions answered):
  - 60 Seconds Chaos – timed run
  - Marathon (10 minutes) – endurance challenge
  - Reflex Mode – 10 seconds per question, resets on correct
- **Endless Mode Improvements**:
  - Cash Out button – save your score voluntarily
  - Risk achievements (Gambler, Risk Taker)
- **Expanded Achievement System**: 24+ new badges
  - Progress achievements (First Steps → Data Bank)
  - Speed achievements (Lightning Brain, Human Cache, CPU Overclocked)
  - Endless achievements (Survivor, Untouchable, Legend)
  - Fun achievements (Night Coder, Addicted, Database Brain)
- **Achievement Dependencies**: Some badges require prerequisites
- **Game History Tracking**: Saves each game session
- **Enhanced Leaderboard**: Shows Speedrun scores and badge counts
- **Rewards Screen**: Categorised badge display

### Database Upgrades
- Auto-migration for new user columns
- Game history table
- Card performance tracking (weak spot identification)

### UI Improvements
- Glow effect on Cash Out button
- Achievement popup notifications
- Scrollable rewards screen


## Version 4.0 — (Broken / Test Version)
**Released:** *Experimental Build*

### Features Added
- **Basic game engine refactor**
- **Speedrun timer implementation**

### Known Issues (Broken)
- **Incomplete database schema** – missing migration logic
- **Achievement Engine partially implemented** – not fully integrated
- **Timer display bugs** – flashing inconsistent
- **Cash Out logic** – not properly integrated with scoring
- **Missing power-up system** – framework present but incomplete
- **No working login system** – user authentication placeholder
- **Error handling missing** – crashes on missing DB columns

### Status
- **Not production-ready** – contains incomplete features and bugs
- Served as a testbed for later improvements

---

## Version 4.0 — Test Version (Alternate)
**Released:** *Simplified Prototype*

### Features Added
- **Simplified Game Engine**: Lightweight implementation
- **Basic Modes**: Normal, Endless, Speedrun (60s/600s/Reflex)
- **Leaderboard**: Basic ranking system
- **Achievement Unlock Messages**: Popup notifications

### Limitations
- No database persistence (in-memory only)
- No user authentication system
- Simplified scoring rules
- No badge dependencies
- UI minimal compared to main versions

### Purpose
- **Proof of concept** for speedrun mechanics
- Testbed for timer implementations
- Later merged into Version 5


## Version 5.0 — Extended Edition (Stable)
**Released:** *Refined and Stable*

### Features Added (from v3.0 + v4.0 lessons)
- **Speedrun Mode Unlock**: Requires 40 Normal Mode questions
- **Endless Mode Rules Clarified**:
  - Wrong answer → run ends, score lost
  - Cash Out → score saved, high score updated
- **Time Warp Mode**: New game type
  - Timer starts at 60s, +3s per correct, -5s per wrong
  - Survive as long as possible
- **Power-Up System** (5 types):
  - Shield – protect from one wrong answer
  - Time Freeze – +10 seconds
  - Peek – show first letter
  - Skip – skip card without penalty
  - Double Points – next answer worth 2×
- **Daily Challenge**: 10 fixed cards per day (RNG seeded by date)
- **Daily Quests**: 5 rotating objectives
- **Heatmap**: Performance by topic category
- **Learning Curve Graph**: Accuracy over time
- **Weak Spots**: Cards with highest wrong counts
- **Multiplayer Duel**: Hotseat mode, 2 players alternate
- **Coins Economy**: Earn 1 coin per correct answer, spend in shop

### Achievements Added (40+ total)
- Skill-based: Triple Threat, Bullseye, Puzzle Master
- Fun hidden: Owl, Tortoise, Hare, Joker
- Mode-specific: Lightning Rod, Infinity, Sharpshooter
- Risk: High Roller, Balance
- Daily: Daily Dedication, Weekly Warrior
- Multiplayer: Duelist, Dominant
- Power-Ups: Big Spender, Coin Collector
- Time Warp: Time Bender, Chrono Master

### Database Upgrades
- Coins and power-up columns
- Daily challenge/quest tracking
- Session mode tracking for Triple Threat

### Bug Fixes (from v4.0)
- Fixed timer display across all speedrun variants
- Corrected Cash Out vs Wrong Answer logic
- Database migrations now handle missing columns gracefully
- Scrollable areas work correctly with mouse wheel
- Achievement popups no longer crash on missing sound
- Progress bar shake animation restored

### UI Enhancements
- Power-Up HUD during gameplay
- Daily challenge calendar view
- Two-column main menu
- Audio controls (SFX/music toggles)


## Version 6.0 — Extended Edition v2.0
**Released:** *Feature Complete*

### Features Added
- **Time Warp Unlock**: Requires 100 Normal Mode questions
- **Triple Threat Achievement**: Win all 3 modes in one session
- **Omniscient Achievement**: Answer every unique card correctly
- **High Roller**: Cash out with prime score
- **Balance**: Finish with exactly 21 points
- **Hare**: 3 cards in under 10 seconds
- **Tortoise**: 120+ seconds on single card

### UI Improvements
- **Fixed scrolling**: Mouse wheel works everywhere
- **Grid-based leaderboard**: Proper column alignment
- **Stats screen tabs**: Heatmap, curve, weak spots unified
- **Duel result screen**: Confetti for winner

### Bug Fixes
- Fixed mouse wheel scrolling in rewards screen
- Leaderboard column widths now respect minsize
- Scrollable areas now properly capture wheel events on all widgets
- Removed duplicate screen classes (WeakSpots/Heatmap redirect to Stats)
- Fixed achievement popup queue order

### Balance Tweaks
- Speedrun unlock reduced to 40 questions
- Time Warp unlock at 100 questions
- Coin rewards balanced for shop purchases


## Version 7.0 — Extended Edition v2.0 (Audio)
**Released:** *Final Polish*

### Features Added
- **Pure-Stdlib Sound System**:
  - No external dependencies (plays via winsound/afplay/aplay)
  - Procedurally generated PCM tones
  - SFX: correct, wrong, achievement, reveal, cashout, click
  - Lo-fi background music loop (8s, layered sine waves)
- **Audio Controls** in main menu:
  - SFX toggle
  - Music toggle
- **Context-Aware Music**:
  - Plays during gameplay screens
  - Stops automatically on menu screens

### Audio Improvements
- Achievement popups now play sound
- Button clicks have subtle feedback
- Volume envelope to prevent clicks/pops
- Non-blocking playback (threaded)

### Bug Fixes
- Fixed sound playback on all platforms
- No external dependencies required
- Graceful degradation if audio fails
- Music stops properly on window close

### Final Polish
- Complete audio immersion
- Professional feel with in‑engine synthesis
- No reliance on external sound files