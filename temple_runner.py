#!/usr/bin/env python3
"""
Temple Runner - A 3D Endless Runner Game
Inspired by Temple Run, built with Python and Pygame
"""

import pygame
import sys
import random
import math
import json
from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple, Optional

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
GREEN = (34, 139, 34)
GOLD = (255, 215, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
GRAY = (128, 128, 128)
DARK_GREEN = (0, 100, 0)
STONE_COLOR = (105, 105, 105)

class GameState(Enum):
    MENU = 1
    PLAYING = 2
    GAME_OVER = 3
    PAUSED = 4

class PlayerState(Enum):
    RUNNING = 1
    JUMPING = 2
    SLIDING = 3
    TURNING_LEFT = 4
    TURNING_RIGHT = 5

@dataclass
class Vector3:
    x: float
    y: float
    z: float
    
    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __mul__(self, scalar):
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

class Camera:
    def __init__(self):
        self.position = Vector3(0, -50, -200)
        self.target = Vector3(0, 0, 0)
        self.shake_intensity = 0
        self.shake_duration = 0
        
    def update(self, player_pos):
        # Follow player with smooth camera movement
        target_x = player_pos.x * 0.3
        target_z = player_pos.z - 200
        
        self.position.x += (target_x - self.position.x) * 0.1
        self.position.z += (target_z - self.position.z) * 0.1
        
        # Camera shake effect
        if self.shake_duration > 0:
            shake_x = random.uniform(-self.shake_intensity, self.shake_intensity)
            shake_y = random.uniform(-self.shake_intensity, self.shake_intensity)
            self.position.x += shake_x
            self.position.y += shake_y
            self.shake_duration -= 1
    
    def add_shake(self, intensity, duration):
        self.shake_intensity = intensity
        self.shake_duration = duration
    
    def project_3d_to_2d(self, point3d):
        """Simple 3D to 2D projection"""
        # Translate relative to camera
        rel_x = point3d.x - self.position.x
        rel_y = point3d.y - self.position.y
        rel_z = point3d.z - self.position.z
        
        # Perspective projection
        if rel_z <= 0:
            rel_z = 0.1
            
        fov = 500
        screen_x = (rel_x * fov / rel_z) + SCREEN_WIDTH // 2
        screen_y = (rel_y * fov / rel_z) + SCREEN_HEIGHT // 2
        
        return (int(screen_x), int(screen_y))

class Player:
    def __init__(self):
        self.position = Vector3(0, 0, 0)
        self.velocity = Vector3(0, 0, 8)  # Forward speed
        self.state = PlayerState.RUNNING
        self.lane = 0  # -1 left, 0 center, 1 right
        self.jump_velocity = 0
        self.slide_timer = 0
        self.turn_timer = 0
        self.invulnerable_timer = 0
        self.size = 20
        
        # Animation
        self.animation_frame = 0
        self.animation_timer = 0
        
    def update(self):
        # Update position
        self.position = self.position + self.velocity
        
        # Handle jumping
        if self.state == PlayerState.JUMPING:
            self.position.y += self.jump_velocity
            self.jump_velocity -= 1.2  # Gravity
            
            if self.position.y <= 0:
                self.position.y = 0
                self.jump_velocity = 0
                self.state = PlayerState.RUNNING
        
        # Handle sliding
        if self.state == PlayerState.SLIDING:
            self.slide_timer -= 1
            if self.slide_timer <= 0:
                self.state = PlayerState.RUNNING
        
        # Handle turning
        if self.state in [PlayerState.TURNING_LEFT, PlayerState.TURNING_RIGHT]:
            self.turn_timer -= 1
            if self.turn_timer <= 0:
                self.state = PlayerState.RUNNING
        
        # Lane movement
        target_x = self.lane * 60
        self.position.x += (target_x - self.position.x) * 0.2
        
        # Update timers
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1
            
        # Animation
        self.animation_timer += 1
        if self.animation_timer >= 10:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 4
    
    def jump(self):
        if self.state == PlayerState.RUNNING:
            self.state = PlayerState.JUMPING
            self.jump_velocity = 18
    
    def slide(self):
        if self.state == PlayerState.RUNNING:
            self.state = PlayerState.SLIDING
            self.slide_timer = 30
    
    def move_left(self):
        if self.lane > -1:
            self.lane -= 1
            self.state = PlayerState.TURNING_LEFT
            self.turn_timer = 10
    
    def move_right(self):
        if self.lane < 1:
            self.lane += 1
            self.state = PlayerState.TURNING_RIGHT
            self.turn_timer = 10
    
    def get_collision_rect(self):
        screen_pos = game.camera.project_3d_to_2d(self.position)
        if self.state == PlayerState.SLIDING:
            return pygame.Rect(screen_pos[0] - self.size//2, screen_pos[1] - self.size//4, 
                             self.size, self.size//2)
        else:
            return pygame.Rect(screen_pos[0] - self.size//2, screen_pos[1] - self.size, 
                             self.size, self.size * 2)

class Obstacle:
    def __init__(self, position, obstacle_type, lane=0):
        self.position = position
        self.type = obstacle_type  # 'barrier', 'gap', 'boulder'
        self.lane = lane
        self.size = 30
        self.active = True
        
    def update(self):
        # Remove obstacles that are far behind
        if self.position.z < game.player.position.z - 300:
            self.active = False
    
    def get_collision_rect(self):
        screen_pos = game.camera.project_3d_to_2d(self.position)
        return pygame.Rect(screen_pos[0] - self.size//2, screen_pos[1] - self.size//2, 
                          self.size, self.size)

class Collectible:
    def __init__(self, position, collectible_type):
        self.position = position
        self.type = collectible_type  # 'coin', 'gem', 'powerup'
        self.size = 15
        self.active = True
        self.rotation = 0
        
    def update(self):
        self.rotation += 5
        if self.position.z < game.player.position.z - 100:
            self.active = False
    
    def get_collision_rect(self):
        screen_pos = game.camera.project_3d_to_2d(self.position)
        return pygame.Rect(screen_pos[0] - self.size//2, screen_pos[1] - self.size//2, 
                          self.size, self.size)

class ParticleSystem:
    def __init__(self):
        self.particles = []
    
    def add_particle(self, position, velocity, color, life):
        self.particles.append({
            'pos': Vector3(position.x, position.y, position.z),
            'vel': velocity,
            'color': color,
            'life': life,
            'max_life': life
        })
    
    def update(self):
        for particle in self.particles[:]:
            particle['pos'] = particle['pos'] + particle['vel']
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.particles.remove(particle)
    
    def draw(self, screen, camera):
        for particle in self.particles:
            screen_pos = camera.project_3d_to_2d(particle['pos'])
            alpha = particle['life'] / particle['max_life']
            color = tuple(int(c * alpha) for c in particle['color'])
            pygame.draw.circle(screen, color, screen_pos, 3)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Temple Runner")
        self.clock = pygame.time.Clock()
        
        # Game state
        self.state = GameState.MENU
        self.player = Player()
        self.camera = Camera()
        self.obstacles = []
        self.collectibles = []
        self.particles = ParticleSystem()
        
        # Game stats
        self.score = 0
        self.coins = 0
        self.distance = 0
        self.speed_multiplier = 1.0
        self.difficulty = 1
        
        # Spawn timers
        self.obstacle_spawn_timer = 0
        self.collectible_spawn_timer = 0
        
        # Load high score
        self.high_score = self.load_high_score()
        
        # Fonts
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
    def load_high_score(self):
        try:
            with open('high_score.json', 'r') as f:
                data = json.load(f)
                return data.get('high_score', 0)
        except:
            return 0
    
    def save_high_score(self):
        try:
            with open('high_score.json', 'w') as f:
                json.dump({'high_score': self.high_score}, f)
        except:
            pass
    
    def reset_game(self):
        self.player = Player()
        self.camera = Camera()
        self.obstacles = []
        self.collectibles = []
        self.particles = ParticleSystem()
        self.score = 0
        self.coins = 0
        self.distance = 0
        self.speed_multiplier = 1.0
        self.difficulty = 1
        self.obstacle_spawn_timer = 0
        self.collectible_spawn_timer = 0
    
    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS)
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.KEYDOWN:
                    if self.state == GameState.MENU:
                        if event.key == pygame.K_SPACE:
                            self.reset_game()
                            self.state = GameState.PLAYING
                        elif event.key == pygame.K_ESCAPE:
                            running = False
                    
                    elif self.state == GameState.PLAYING:
                        if event.key == pygame.K_SPACE:
                            self.player.jump()
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            self.player.slide()
                        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            self.player.move_left()
                        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            self.player.move_right()
                        elif event.key == pygame.K_ESCAPE:
                            self.state = GameState.PAUSED
                    
                    elif self.state == GameState.GAME_OVER:
                        if event.key == pygame.K_SPACE:
                            self.state = GameState.MENU
                        elif event.key == pygame.K_ESCAPE:
                            running = False
                    
                    elif self.state == GameState.PAUSED:
                        if event.key == pygame.K_ESCAPE:
                            self.state = GameState.PLAYING
            
            # Update game
            if self.state == GameState.PLAYING:
                self.update()
            
            # Draw everything
            self.draw()
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()

# Create global game instance
game = Game()

if __name__ == "__main__":
    game.run()
