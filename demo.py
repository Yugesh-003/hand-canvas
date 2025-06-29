#!/usr/bin/env python3
"""
Temple Runner Demo
Demonstrates game functionality without requiring a display
"""

import sys
import os
import time

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from temple_runner import *
import game_logic
import renderer
import sound_effects

def demo_game_simulation():
    """Simulate a game session"""
    print("🎮 TEMPLE RUNNER DEMO SIMULATION 🎮")
    print("=" * 50)
    
    # Create game components
    player = Player()
    camera = Camera()
    obstacles = []
    collectibles = []
    particles = ParticleSystem()
    
    score = 0
    distance = 0
    coins = 0
    
    print("🏃 Starting temple escape simulation...")
    print()
    
    # Simulate 10 seconds of gameplay
    for frame in range(600):  # 60 FPS * 10 seconds
        # Update player
        player.update()
        
        # Update camera
        camera.update(player.position)
        
        # Update distance and score
        distance += player.velocity.z
        score = int(distance / 10)
        
        # Spawn obstacles occasionally
        if frame % 90 == 0:  # Every 1.5 seconds
            obstacle_pos = Vector3(0, 0, player.position.z + 200)
            obstacles.append(Obstacle(obstacle_pos, 'barrier'))
            print(f"⚠️  Obstacle spawned at distance {int(distance)}m")
        
        # Spawn collectibles
        if frame % 60 == 0:  # Every second
            collectible_pos = Vector3(0, 10, player.position.z + 150)
            collectibles.append(Collectible(collectible_pos, 'coin'))
            coins += 1
            score += 10
            print(f"🪙 Coin collected! Total coins: {coins}")
        
        # Simulate player actions
        if frame % 120 == 0:  # Jump every 2 seconds
            player.jump()
            print("🦘 Player jumped!")
        
        if frame % 180 == 30:  # Slide occasionally
            player.slide()
            print("🏃 Player sliding!")
        
        if frame % 200 == 0:  # Change lanes
            if player.lane == 0:
                player.move_left()
                print("⬅️  Moved to left lane")
            else:
                player.move_right()
                print("➡️  Moved to right lane")
        
        # Update obstacles
        for obstacle in obstacles[:]:
            obstacle.update()
            if not obstacle.active:
                obstacles.remove(obstacle)
        
        # Update collectibles
        for collectible in collectibles[:]:
            collectible.update()
            if not collectible.active:
                collectibles.remove(collectible)
        
        # Update particles
        particles.update()
        
        # Print status every 2 seconds
        if frame % 120 == 0:
            print(f"📊 Status - Distance: {int(distance)}m, Score: {score}, Speed: {player.velocity.z:.1f}")
    
    print()
    print("🏁 SIMULATION COMPLETE!")
    print(f"Final Score: {score}")
    print(f"Distance Traveled: {int(distance)}m")
    print(f"Coins Collected: {coins}")
    print(f"Player State: {player.state.name}")

def demo_sound_effects():
    """Demonstrate sound effect generation"""
    print("\n🔊 SOUND EFFECTS DEMO")
    print("=" * 30)
    
    try:
        from sound_effects import SoundManager
        sound_manager = SoundManager()
        
        print("Generated sound effects:")
        for sound_name in sound_manager.sounds.keys():
            print(f"  ✓ {sound_name}")
        
        print("\nSound effects are ready to play!")
        print("(In the actual game, these would play during actions)")
        
    except Exception as e:
        print(f"Sound demo failed: {e}")

def demo_3d_projection():
    """Demonstrate 3D to 2D projection"""
    print("\n🎯 3D PROJECTION DEMO")
    print("=" * 30)
    
    camera = Camera()
    
    # Test various 3D points
    test_points = [
        Vector3(0, 0, 100),    # Center, close
        Vector3(-60, 0, 200),  # Left lane, medium distance
        Vector3(60, 0, 300),   # Right lane, far
        Vector3(0, 50, 150),   # Center, elevated
    ]
    
    print("3D Point -> 2D Screen Position:")
    for i, point in enumerate(test_points):
        screen_pos = camera.project_3d_to_2d(point)
        print(f"  Point {i+1}: ({point.x:3.0f}, {point.y:3.0f}, {point.z:3.0f}) -> ({screen_pos[0]:4.0f}, {screen_pos[1]:4.0f})")

def main():
    """Run the demo"""
    print("TEMPLE RUNNER - COMPREHENSIVE DEMO")
    print("=" * 50)
    print("This demo shows the game working without requiring a display")
    print()
    
    # Run demos
    demo_game_simulation()
    demo_sound_effects()
    demo_3d_projection()
    
    print("\n" + "=" * 50)
    print("🎉 DEMO COMPLETE!")
    print()
    print("To play the actual game with graphics:")
    print("1. Make sure you have a display available")
    print("2. Run: source temple_runner_env/bin/activate")
    print("3. Run: python main.py")
    print()
    print("Game Features:")
    print("• 3D perspective rendering")
    print("• Endless procedural generation")
    print("• Multiple obstacle types")
    print("• Collectible system")
    print("• Progressive difficulty")
    print("• High score tracking")
    print("• Immersive sound effects")
    print("• Particle effects")
    print("=" * 50)

if __name__ == "__main__":
    main()
