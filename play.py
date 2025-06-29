#!/usr/bin/env python3
"""
Temple Runner - Simple Launcher
Fixed version of the Temple Run-inspired game
"""

import os
import sys

def main():
    print("🏛️  TEMPLE RUNNER - LAUNCHER 🏛️")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists('temple_runner_fixed.py'):
        print("❌ Game files not found!")
        print("Please run this from the game directory.")
        return
    
    # Check if virtual environment exists
    if not os.path.exists('temple_runner_env'):
        print("❌ Virtual environment not found!")
        print("Please run setup.sh first or create the environment manually:")
        print("  python3 -m venv temple_runner_env")
        print("  source temple_runner_env/bin/activate")
        print("  pip install pygame numpy")
        return
    
    print("✅ All files found!")
    print("🚀 Starting Temple Runner...")
    print()
    print("CONTROLS:")
    print("  Arrow Keys / WASD - Move left/right")
    print("  Space - Jump")
    print("  Down/S - Slide")
    print("  ESC - Pause/Menu")
    print()
    print("OBJECTIVE:")
    print("  Survive as long as possible!")
    print("  Collect coins and gems for points!")
    print("  Avoid obstacles by jumping, sliding, or changing lanes!")
    print()
    print("=" * 40)
    
    # Import and run the game
    try:
        from temple_runner_fixed import main as game_main
        game_main()
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're in the virtual environment:")
        print("  source temple_runner_env/bin/activate")
        print("  python play.py")
    except Exception as e:
        print(f"❌ Game error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
