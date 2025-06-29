# Temple Runner - Troubleshooting Guide 🔧

## Quick Fix - Use the Working Version

The game has been fixed! Use this command to play:

```bash
# Activate virtual environment
source temple_runner_env/bin/activate

# Run the fixed game
python temple_runner_fixed.py
```

Or use the launcher:
```bash
source temple_runner_env/bin/activate
python play.py
```

## Common Issues and Solutions

### 1. "python: command not found"
**Solution:** Use `python3` instead of `python`
```bash
python3 temple_runner_fixed.py
```

### 2. "No module named 'pygame'" or "No module named 'numpy'"
**Solution:** Install dependencies in virtual environment
```bash
# Create virtual environment (if not exists)
python3 -m venv temple_runner_env

# Activate it
source temple_runner_env/bin/activate

# Install packages
pip install pygame numpy

# Run game
python temple_runner_fixed.py
```

### 3. "externally-managed-environment" error
**Solution:** Use virtual environment (already handled above)

### 4. Game window doesn't appear
**Possible causes:**
- No display available (SSH/headless environment)
- Display issues in WSL

**Solutions:**
- Run the demo instead: `python demo.py`
- For WSL, install X11 server or use Windows terminal
- For SSH, enable X11 forwarding: `ssh -X username@server`

### 5. Sound effects not working
**Cause:** NumPy not installed or audio system issues

**Solution:**
```bash
pip install numpy
# Sound will be automatically disabled if NumPy unavailable
```

### 6. Game crashes on startup
**Solution:** Check error message and try:
```bash
# Test imports
python test_game.py

# Run demo (no display needed)
python demo.py

# Run with error details
python temple_runner_fixed.py
```

### 7. Controls not responding
**Solutions:**
- Make sure game window has focus (click on it)
- Try different keys (arrows vs WASD)
- Check if game is paused (press ESC)

### 8. Poor performance/low FPS
**Solutions:**
- Close other applications
- Reduce game resolution in code
- Lower particle count in renderer

## File Structure Check

Your directory should contain:
```
AWS_Game/
├── temple_runner_fixed.py    # ✅ WORKING GAME FILE
├── play.py                   # ✅ LAUNCHER
├── demo.py                   # ✅ DEMO (no display needed)
├── test_game.py             # ✅ TEST SCRIPT
├── setup.sh                 # ✅ SETUP SCRIPT
├── requirements.txt         # ✅ DEPENDENCIES
├── temple_runner_env/       # ✅ VIRTUAL ENVIRONMENT
└── README.md               # ✅ DOCUMENTATION
```

## Testing Steps

1. **Test imports:**
   ```bash
   source temple_runner_env/bin/activate
   python test_game.py
   ```

2. **Test without display:**
   ```bash
   source temple_runner_env/bin/activate
   python demo.py
   ```

3. **Test full game:**
   ```bash
   source temple_runner_env/bin/activate
   python temple_runner_fixed.py
   ```

## Environment Setup

### Fresh Installation:
```bash
# 1. Navigate to game directory
cd /path/to/AWS_Game

# 2. Create virtual environment
python3 -m venv temple_runner_env

# 3. Activate environment
source temple_runner_env/bin/activate

# 4. Install dependencies
pip install pygame numpy

# 5. Test installation
python test_game.py

# 6. Run game
python temple_runner_fixed.py
```

### Using Setup Script:
```bash
chmod +x setup.sh
./setup.sh
```

## Game Features Verification

The working game includes:
- ✅ 3D perspective rendering
- ✅ Player movement (3 lanes)
- ✅ Jump and slide mechanics
- ✅ Obstacle generation (barriers, gaps, boulders)
- ✅ Collectibles (coins, gems, power-ups)
- ✅ Sound effects (if NumPy available)
- ✅ Particle effects
- ✅ Progressive difficulty
- ✅ High score system
- ✅ Pause/resume functionality

## Performance Tips

1. **Optimize for your system:**
   - Edit `SCREEN_WIDTH` and `SCREEN_HEIGHT` in the game file
   - Reduce `FPS` if needed
   - Lower particle count for better performance

2. **System requirements:**
   - Python 3.7+
   - 2GB RAM minimum
   - Graphics card recommended but not required

## Getting Help

If you're still having issues:

1. **Check the error message** - it usually tells you what's wrong
2. **Run the test script** - `python test_game.py`
3. **Try the demo** - `python demo.py` (works without display)
4. **Check Python version** - `python3 --version` (need 3.7+)
5. **Verify packages** - `pip list | grep -E "(pygame|numpy)"`

## Success Indicators

You'll know it's working when you see:
```
🏛️  TEMPLE RUNNER 🏛️
==============================
Starting game...
Temple Runner initialized successfully!
```

And a game window opens with the Temple Runner menu.

---

**The game is fully functional - use `temple_runner_fixed.py` for the best experience!** 🎮
