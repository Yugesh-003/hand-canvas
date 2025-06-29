#!/usr/bin/env python3
"""
Temple Runner - Main Game File
A 3D endless runner game inspired by Temple Run
Built with Python and Pygame

Features:
- 3D perspective rendering
- Endless procedural generation
- Multiple obstacle types
- Collectible coins, gems, and power-ups
- Increasing difficulty
- High score system
- Immersive sound effects
- Particle effects
- Smooth animations

Controls:
- Arrow Keys / WASD: Move left/right
- Space: Jump
- Down/S: Slide
- ESC: Pause/Menu

Author: AI Assistant
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import all game modules
from temple_runner import *
import game_logic
import renderer

# Try to import sound effects (optional, in case numpy is not available)
try:
    import sound_effects
    from sound_effects import (play_jump_sound, play_slide_sound, play_coin_sound, 
                              play_gem_sound, play_powerup_sound, play_collision_sound, 
                              play_footstep_sound)
    SOUND_ENABLED = True
    print("Sound effects enabled!")
except ImportError as e:
    print(f"Sound effects disabled: {e}")
    print("Install numpy for sound effects: pip install numpy")
    SOUND_ENABLED = False
    
    # Create dummy sound functions
    def play_jump_sound(): pass
    def play_slide_sound(): pass
    def play_coin_sound(): pass
    def play_gem_sound(): pass
    def play_powerup_sound(): pass
    def play_collision_sound(): pass
    def play_footstep_sound(): pass

# Enhanced Player class with sound integration
class EnhancedPlayer(Player):
    def __init__(self):
        super().__init__()
        self.footstep_timer = 0
    
    def update(self):
        super().update()
        
        # Play footstep sounds while running
        if self.state == PlayerState.RUNNING and SOUND_ENABLED:
            self.footstep_timer -= 1
            if self.footstep_timer <= 0:
                play_footstep_sound()
                self.footstep_timer = 20  # Play every 20 frames
    
    def jump(self):
        if self.state == PlayerState.RUNNING:
            super().jump()
            if SOUND_ENABLED:
                play_jump_sound()
    
    def slide(self):
        if self.state == PlayerState.RUNNING:
            super().slide()
            if SOUND_ENABLED:
                play_slide_sound()

# Enhanced Game class with sound integration
class EnhancedGame(Game):
    def __init__(self):
        super().__init__()
        self.player = EnhancedPlayer()
        print("Temple Runner initialized!")
        print("=" * 50)
        print("TEMPLE RUNNER - Escape the Ancient Temple!")
        print("=" * 50)
        print("Controls:")
        print("  Arrow Keys / WASD - Move left/right")
        print("  Space - Jump over gaps and barriers")
        print("  Down/S - Slide under obstacles")
        print("  ESC - Pause game / Return to menu")
        print()
        print("Objective:")
        print("  - Avoid obstacles and survive as long as possible")
        print("  - Collect coins and gems for points")
        print("  - Grab power-ups for temporary invulnerability")
        print("  - The game gets faster and harder over time!")
        print()
        print("Tips:")
        print("  - Jump over gaps and low barriers")
        print("  - Slide under high barriers")
        print("  - Switch lanes to avoid obstacles")
        print("  - Collect items for higher scores")
        print("=" * 50)
    
    def collect_item(self, collectible):
        """Enhanced collect_item with sound effects"""
        super().collect_item(collectible)
        
        if SOUND_ENABLED:
            if collectible.type == 'coin':
                play_coin_sound()
            elif collectible.type == 'gem':
                play_gem_sound()
            elif collectible.type == 'powerup':
                play_powerup_sound()
    
    def game_over(self):
        """Enhanced game_over with sound effects"""
        super().game_over()
        
        if SOUND_ENABLED:
            play_collision_sound()
        
        print(f"\nGame Over! Final Score: {self.score}")
        print(f"Distance: {int(self.distance)}m")
        print(f"Coins: {self.coins}")
        print(f"Level: {self.difficulty}")
        if self.score == self.high_score:
            print("🎉 NEW HIGH SCORE! 🎉")

def main():
    """Main game function"""
    print("Starting Temple Runner...")
    
    # Check for required dependencies
    try:
        import pygame
        print("✓ Pygame found")
    except ImportError:
        print("❌ Pygame not found. Please install it with: pip install pygame")
        return
    
    try:
        import numpy
        print("✓ NumPy found - Sound effects enabled")
    except ImportError:
        print("⚠ NumPy not found - Sound effects disabled")
        print("  Install with: pip install numpy")
    
    print("✓ All systems ready!")
    print()
    
    # Create and run the game
    try:
        game = EnhancedGame()
        game.run()
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("Thanks for playing Temple Runner!")

if __name__ == "__main__":
    main()
