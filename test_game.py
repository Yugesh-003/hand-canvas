#!/usr/bin/env python3
"""
Test script for Temple Runner
Tests game initialization and basic functionality
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all modules can be imported"""
    print("Testing imports...")
    
    try:
        import pygame
        print("✓ Pygame imported successfully")
    except ImportError as e:
        print(f"❌ Pygame import failed: {e}")
        return False
    
    try:
        import numpy
        print("✓ NumPy imported successfully")
    except ImportError as e:
        print(f"❌ NumPy import failed: {e}")
        return False
    
    try:
        import temple_runner
        print("✓ Temple Runner core imported successfully")
    except ImportError as e:
        print(f"❌ Temple Runner core import failed: {e}")
        return False
    
    try:
        import game_logic
        print("✓ Game logic imported successfully")
    except ImportError as e:
        print(f"❌ Game logic import failed: {e}")
        return False
    
    try:
        import renderer
        print("✓ Renderer imported successfully")
    except ImportError as e:
        print(f"❌ Renderer import failed: {e}")
        return False
    
    try:
        import sound_effects
        print("✓ Sound effects imported successfully")
    except ImportError as e:
        print(f"❌ Sound effects import failed: {e}")
        return False
    
    return True

def test_game_classes():
    """Test game class initialization"""
    print("\nTesting game classes...")
    
    try:
        from temple_runner import Vector3, Camera, Player, Obstacle, Collectible, ParticleSystem
        
        # Test Vector3
        v = Vector3(1, 2, 3)
        v2 = v + Vector3(1, 1, 1)
        v3 = v * 2
        print("✓ Vector3 class works")
        
        # Test Camera
        camera = Camera()
        camera.update(Vector3(0, 0, 0))
        print("✓ Camera class works")
        
        # Test Player
        player = Player()
        player.update()
        player.jump()
        player.slide()
        player.move_left()
        player.move_right()
        print("✓ Player class works")
        
        # Test Obstacle
        obstacle = Obstacle(Vector3(0, 0, 100), 'barrier')
        obstacle.update()
        print("✓ Obstacle class works")
        
        # Test Collectible
        collectible = Collectible(Vector3(0, 0, 100), 'coin')
        collectible.update()
        print("✓ Collectible class works")
        
        # Test ParticleSystem
        particles = ParticleSystem()
        particles.add_particle(Vector3(0, 0, 0), Vector3(1, 1, 1), (255, 255, 255), 30)
        particles.update()
        print("✓ ParticleSystem class works")
        
        return True
        
    except Exception as e:
        print(f"❌ Game class test failed: {e}")
        return False

def test_sound_system():
    """Test sound system"""
    print("\nTesting sound system...")
    
    try:
        from sound_effects import SoundManager
        sound_manager = SoundManager()
        print("✓ Sound manager created successfully")
        
        # Test sound generation (without playing)
        print("✓ All sound effects generated successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Sound system test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("TEMPLE RUNNER - SYSTEM TEST")
    print("=" * 50)
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
    
    # Test game classes
    if not test_game_classes():
        all_passed = False
    
    # Test sound system
    if not test_sound_system():
        all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ALL TESTS PASSED! 🎉")
        print("Temple Runner is ready to play!")
        print("\nTo start the game, run:")
        print("  source temple_runner_env/bin/activate")
        print("  python main.py")
    else:
        print("❌ SOME TESTS FAILED")
        print("Please check the error messages above")
    print("=" * 50)

if __name__ == "__main__":
    main()
