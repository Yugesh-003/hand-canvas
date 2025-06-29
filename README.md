# Temple Runner 🏃‍♂️

A 3D endless runner game inspired by Temple Run, built with Python and Pygame. Escape from an ancient temple while dodging obstacles, collecting treasures, and surviving as long as possible!

## Features ✨

### Core Gameplay
- **3D Perspective**: Pseudo-3D rendering with depth and perspective
- **Endless Running**: Procedurally generated infinite temple path
- **Multiple Lanes**: Switch between left, center, and right lanes
- **Dynamic Obstacles**: Barriers, gaps, boulders, and more
- **Collectibles**: Coins, gems, and power-ups
- **Increasing Difficulty**: Game gets faster and harder over time

### Visual Effects
- **Vibrant Environment**: Ancient ruins, lush jungle, stone pathways
- **Particle Systems**: Coin sparkles, explosion effects
- **Smooth Animations**: Running, jumping, sliding animations
- **Camera Effects**: Following camera with shake effects
- **Environmental Details**: Trees, ruins, atmospheric elements

### Audio Experience
- **Procedural Sound Effects**: Jump, slide, collect, crash sounds
- **Immersive Audio**: Footsteps, ambient effects
- **Dynamic Audio**: Sounds generated in real-time using NumPy

### Game Systems
- **High Score System**: Persistent high score tracking
- **Power-ups**: Temporary invulnerability
- **Progressive Difficulty**: 10 difficulty levels
- **Statistics Tracking**: Distance, coins, speed multiplier

## Installation 🚀

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Quick Start
1. **Clone or download the game files**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the game:**
   ```bash
   python main.py
   ```

### Manual Installation
If you prefer to install packages manually:
```bash
pip install pygame numpy
```

## Controls 🎮

| Action | Keys |
|--------|------|
| Move Left | ← or A |
| Move Right | → or D |
| Jump | Space |
| Slide | ↓ or S |
| Pause/Menu | ESC |

## Gameplay Guide 📖

### Objective
Survive as long as possible while running through the ancient temple. Avoid obstacles, collect treasures, and achieve the highest score!

### Obstacles
- **Barriers**: Jump over or slide under depending on height
- **Gaps**: Jump across to avoid falling
- **Boulders**: Switch lanes to avoid rolling stones
- **Multi-lane Obstacles**: Find the safe lane quickly

### Collectibles
- **Coins** (Gold): +10 points, +1 coin
- **Gems** (Blue): +50 points, +5 coins
- **Power-ups** (Red): +100 points, temporary invulnerability

### Difficulty Progression
- Every 500 points increases difficulty level
- Higher difficulty = faster speed, more obstacles
- Maximum difficulty level: 10

### Scoring System
- Distance traveled: 1 point per 10 meters
- Coins collected: 10 points each
- Gems collected: 50 points each
- Power-ups collected: 100 points each

## Game Architecture 🏗️

### File Structure
```
temple_runner/
├── main.py              # Main game launcher
├── temple_runner.py     # Core game classes and logic
├── game_logic.py        # Game update and collision logic
├── renderer.py          # 3D rendering and visual effects
├── sound_effects.py     # Procedural audio generation
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── high_score.json     # High score storage (created automatically)
```

### Key Classes
- **Game**: Main game controller and state manager
- **Player**: Player character with physics and animations
- **Camera**: 3D perspective camera with following and shake effects
- **Obstacle**: Various obstacle types with collision detection
- **Collectible**: Coins, gems, and power-ups
- **ParticleSystem**: Visual effects and particles
- **SoundManager**: Procedural sound effect generation

## Technical Features 🔧

### 3D Rendering
- Perspective projection from 3D world to 2D screen
- Depth-based scaling and positioning
- Camera following with smooth interpolation
- Environmental depth with parallax effects

### Physics System
- Gravity and jumping mechanics
- Collision detection with rectangular bounds
- Lane-based movement system
- Smooth interpolation between positions

### Procedural Generation
- Dynamic obstacle spawning based on difficulty
- Randomized collectible placement
- Environmental element generation
- Balanced challenge progression

### Performance Optimizations
- Object culling for off-screen elements
- Efficient collision detection
- Minimal memory allocation during gameplay
- 60 FPS target with frame rate limiting

## Customization 🎨

### Modifying Game Parameters
Edit constants in `temple_runner.py`:
```python
SCREEN_WIDTH = 1200      # Game window width
SCREEN_HEIGHT = 800      # Game window height
FPS = 60                 # Target frame rate
```

### Adding New Obstacles
Extend the `Obstacle` class in `temple_runner.py` and add rendering in `renderer.py`.

### Custom Sound Effects
Modify the `SoundManager` class in `sound_effects.py` to add new procedural sounds.

## Troubleshooting 🔧

### Common Issues

**Game won't start:**
- Ensure Python 3.7+ is installed
- Install required packages: `pip install pygame numpy`
- Check for error messages in the console

**No sound effects:**
- Install NumPy: `pip install numpy`
- Sound will be disabled if NumPy is not available

**Poor performance:**
- Lower the FPS in `temple_runner.py`
- Reduce particle count in `renderer.py`
- Close other applications to free up resources

**Controls not responding:**
- Make sure the game window has focus
- Try different key combinations (arrows vs WASD)

## Development 👨‍💻

### Adding Features
The game is designed to be easily extensible:

1. **New Obstacle Types**: Add to `spawn_obstacle()` in `game_logic.py`
2. **Visual Effects**: Extend the `ParticleSystem` class
3. **Power-ups**: Add new types in `collect_item()` method
4. **Game Modes**: Extend the `GameState` enum

### Code Style
- Follow PEP 8 Python style guidelines
- Use type hints where appropriate
- Document new functions and classes
- Keep methods focused and single-purpose

## Credits 🙏

- **Inspiration**: Temple Run by Imangi Studios
- **Engine**: Pygame community
- **Audio**: NumPy for procedural sound generation
- **Development**: Created with AI assistance

## License 📄

This project is created for educational and entertainment purposes. Feel free to modify and distribute according to your needs.

---

**Enjoy your escape from the temple! 🏛️💨**

*May your reflexes be quick and your score be high!*
