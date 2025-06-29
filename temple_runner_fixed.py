#!/usr/bin/env python3
"""
Temple Runner - Complete Game Implementation
A 3D endless runner game inspired by Temple Run
"""

import pygame
import sys
import random
import math
import json
from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple, Optional

# Try to import numpy for sound effects
try:
    import numpy as np
    SOUND_ENABLED = True
except ImportError:
    SOUND_ENABLED = False
    print("NumPy not available - sound effects disabled")

# Initialize Pygame
pygame.init()
if SOUND_ENABLED:
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

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

class SoundManager:
    def __init__(self):
        self.sounds = {}
        if SOUND_ENABLED:
            self.generate_sounds()
    
    def generate_sounds(self):
        """Generate all game sound effects"""
        self.sounds['jump'] = self.generate_jump_sound()
        self.sounds['slide'] = self.generate_slide_sound()
        self.sounds['coin'] = self.generate_coin_sound()
        self.sounds['gem'] = self.generate_gem_sound()
        self.sounds['powerup'] = self.generate_powerup_sound()
        self.sounds['collision'] = self.generate_collision_sound()
        self.sounds['footstep'] = self.generate_footstep_sound()
    
    def generate_jump_sound(self):
        duration = 0.3
        sample_rate = 22050
        frames = int(duration * sample_rate)
        arr = np.zeros((frames, 2))
        for i in range(frames):
            t = i / sample_rate
            freq = 200 + (t / duration) * 300
            amplitude = 0.3 * (1 - t / duration)
            wave = amplitude * np.sin(2 * np.pi * freq * t)
            arr[i] = [wave, wave]
        arr = (arr * 32767).astype(np.int16)
        return pygame.sndarray.make_sound(arr)
    
    def generate_slide_sound(self):
        duration = 0.4
        sample_rate = 22050
        frames = int(duration * sample_rate)
        arr = np.zeros((frames, 2))
        for i in range(frames):
            t = i / sample_rate
            noise = random.uniform(-1, 1) * 0.2
            rumble = 0.1 * np.sin(2 * np.pi * 80 * t)
            amplitude = 0.3 * (1 - t / duration)
            wave = amplitude * (noise + rumble)
            arr[i] = [wave, wave]
        arr = (arr * 32767).astype(np.int16)
        return pygame.sndarray.make_sound(arr)
    
    def generate_coin_sound(self):
        duration = 0.2
        sample_rate = 22050
        frames = int(duration * sample_rate)
        arr = np.zeros((frames, 2))
        for i in range(frames):
            t = i / sample_rate
            freq1, freq2, freq3 = 800, 1200, 1600
            amplitude = 0.4 * np.exp(-t * 8)
            wave = amplitude * (
                0.5 * np.sin(2 * np.pi * freq1 * t) +
                0.3 * np.sin(2 * np.pi * freq2 * t) +
                0.2 * np.sin(2 * np.pi * freq3 * t)
            )
            arr[i] = [wave, wave]
        arr = (arr * 32767).astype(np.int16)
        return pygame.sndarray.make_sound(arr)
    
    def generate_gem_sound(self):
        duration = 0.4
        sample_rate = 22050
        frames = int(duration * sample_rate)
        arr = np.zeros((frames, 2))
        for i in range(frames):
            t = i / sample_rate
            freq = 1000 + 500 * np.sin(2 * np.pi * 3 * t)
            amplitude = 0.3 * np.exp(-t * 3)
            wave = amplitude * np.sin(2 * np.pi * freq * t)
            sparkle = 0.1 * amplitude * np.sin(2 * np.pi * freq * 3 * t)
            arr[i] = [wave + sparkle, wave + sparkle]
        arr = (arr * 32767).astype(np.int16)
        return pygame.sndarray.make_sound(arr)
    
    def generate_powerup_sound(self):
        duration = 0.6
        sample_rate = 22050
        frames = int(duration * sample_rate)
        arr = np.zeros((frames, 2))
        notes = [261.63, 329.63, 392.00, 523.25]
        note_duration = duration / len(notes)
        
        for note_idx, freq in enumerate(notes):
            start_frame = int(note_idx * note_duration * sample_rate)
            end_frame = int((note_idx + 1) * note_duration * sample_rate)
            
            for i in range(start_frame, min(end_frame, frames)):
                t = (i - start_frame) / sample_rate
                amplitude = 0.4 * (1 - t / note_duration)
                wave = amplitude * np.sin(2 * np.pi * freq * t)
                arr[i] = [wave, wave]
        
        arr = (arr * 32767).astype(np.int16)
        return pygame.sndarray.make_sound(arr)
    
    def generate_collision_sound(self):
        duration = 0.5
        sample_rate = 22050
        frames = int(duration * sample_rate)
        arr = np.zeros((frames, 2))
        for i in range(frames):
            t = i / sample_rate
            noise = random.uniform(-1, 1) * 0.5
            thump = 0.3 * np.sin(2 * np.pi * 60 * t)
            crash = 0.2 * np.sin(2 * np.pi * 200 * t)
            amplitude = 0.8 * np.exp(-t * 4)
            wave = amplitude * (noise + thump + crash)
            arr[i] = [wave, wave]
        arr = (arr * 32767).astype(np.int16)
        return pygame.sndarray.make_sound(arr)
    
    def generate_footstep_sound(self):
        duration = 0.1
        sample_rate = 22050
        frames = int(duration * sample_rate)
        arr = np.zeros((frames, 2))
        for i in range(frames):
            t = i / sample_rate
            noise = random.uniform(-1, 1) * 0.1
            thud = 0.3 * np.sin(2 * np.pi * 120 * t)
            amplitude = 0.2 * (1 - t / duration)
            wave = amplitude * (thud + noise)
            arr[i] = [wave, wave]
        arr = (arr * 32767).astype(np.int16)
        return pygame.sndarray.make_sound(arr)
    
    def play_sound(self, sound_name, volume=1.0):
        if SOUND_ENABLED and sound_name in self.sounds:
            sound = self.sounds[sound_name]
            sound.set_volume(volume)
            sound.play()

class Camera:
    def __init__(self):
        self.position = Vector3(0, -50, -200)
        self.target = Vector3(0, 0, 0)
        self.shake_intensity = 0
        self.shake_duration = 0
        
    def update(self, player_pos):
        target_x = player_pos.x * 0.3
        target_z = player_pos.z - 200
        
        self.position.x += (target_x - self.position.x) * 0.1
        self.position.z += (target_z - self.position.z) * 0.1
        
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
        rel_x = point3d.x - self.position.x
        rel_y = point3d.y - self.position.y
        rel_z = point3d.z - self.position.z
        
        if rel_z <= 0:
            rel_z = 0.1
            
        fov = 500
        screen_x = (rel_x * fov / rel_z) + SCREEN_WIDTH // 2
        screen_y = (rel_y * fov / rel_z) + SCREEN_HEIGHT // 2
        
        return (int(screen_x), int(screen_y))

class Player:
    def __init__(self, sound_manager):
        self.position = Vector3(0, 0, 0)
        self.velocity = Vector3(0, 0, 8)
        self.state = PlayerState.RUNNING
        self.lane = 0
        self.jump_velocity = 0
        self.slide_timer = 0
        self.turn_timer = 0
        self.invulnerable_timer = 0
        self.size = 20
        self.animation_frame = 0
        self.animation_timer = 0
        self.footstep_timer = 0
        self.sound_manager = sound_manager
        
    def update(self):
        self.position = self.position + self.velocity
        
        if self.state == PlayerState.JUMPING:
            self.position.y += self.jump_velocity
            self.jump_velocity -= 1.2
            
            if self.position.y <= 0:
                self.position.y = 0
                self.jump_velocity = 0
                self.state = PlayerState.RUNNING
        
        if self.state == PlayerState.SLIDING:
            self.slide_timer -= 1
            if self.slide_timer <= 0:
                self.state = PlayerState.RUNNING
        
        if self.state in [PlayerState.TURNING_LEFT, PlayerState.TURNING_RIGHT]:
            self.turn_timer -= 1
            if self.turn_timer <= 0:
                self.state = PlayerState.RUNNING
        
        target_x = self.lane * 60
        self.position.x += (target_x - self.position.x) * 0.2
        
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1
            
        self.animation_timer += 1
        if self.animation_timer >= 10:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 4
        
        # Footstep sounds
        if self.state == PlayerState.RUNNING:
            self.footstep_timer -= 1
            if self.footstep_timer <= 0:
                self.sound_manager.play_sound('footstep', 0.3)
                self.footstep_timer = 20
    
    def jump(self):
        if self.state == PlayerState.RUNNING:
            self.state = PlayerState.JUMPING
            self.jump_velocity = 18
            self.sound_manager.play_sound('jump', 0.7)
    
    def slide(self):
        if self.state == PlayerState.RUNNING:
            self.state = PlayerState.SLIDING
            self.slide_timer = 30
            self.sound_manager.play_sound('slide', 0.6)
    
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
    
    def get_collision_rect(self, camera):
        screen_pos = camera.project_3d_to_2d(self.position)
        if self.state == PlayerState.SLIDING:
            return pygame.Rect(screen_pos[0] - self.size//2, screen_pos[1] - self.size//4, 
                             self.size, self.size//2)
        else:
            return pygame.Rect(screen_pos[0] - self.size//2, screen_pos[1] - self.size, 
                             self.size, self.size * 2)

class Obstacle:
    def __init__(self, position, obstacle_type, lane=0):
        self.position = position
        self.type = obstacle_type
        self.lane = lane
        self.size = 30
        self.active = True
        
    def update(self, player_z):
        if self.position.z < player_z - 300:
            self.active = False
    
    def get_collision_rect(self, camera):
        screen_pos = camera.project_3d_to_2d(self.position)
        return pygame.Rect(screen_pos[0] - self.size//2, screen_pos[1] - self.size//2, 
                          self.size, self.size)

class Collectible:
    def __init__(self, position, collectible_type):
        self.position = position
        self.type = collectible_type
        self.size = 15
        self.active = True
        self.rotation = 0
        
    def update(self, player_z):
        self.rotation += 5
        if self.position.z < player_z - 100:
            self.active = False
    
    def get_collision_rect(self, camera):
        screen_pos = camera.project_3d_to_2d(self.position)
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
            if 0 <= screen_pos[0] <= SCREEN_WIDTH and 0 <= screen_pos[1] <= SCREEN_HEIGHT:
                alpha = particle['life'] / particle['max_life']
                color = tuple(int(c * alpha) for c in particle['color'])
                pygame.draw.circle(screen, color, screen_pos, 3)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Temple Runner")
        self.clock = pygame.time.Clock()
        
        # Initialize sound manager
        self.sound_manager = SoundManager()
        
        # Game state
        self.state = GameState.MENU
        self.player = Player(self.sound_manager)
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
        
        print("Temple Runner initialized successfully!")
    
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
        self.player = Player(self.sound_manager)
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
    
    def update(self):
        """Main game update loop"""
        # Update player
        self.player.update()
        
        # Update camera
        self.camera.update(self.player.position)
        
        # Update distance and score
        self.distance += self.player.velocity.z * self.speed_multiplier
        self.score = int(self.distance / 10)
        
        # Increase difficulty over time
        if self.score > 0 and self.score % 500 == 0:
            if self.difficulty < 10:
                self.difficulty += 1
                self.speed_multiplier += 0.1
                self.player.velocity.z += 0.5
        
        # Spawn obstacles
        self.obstacle_spawn_timer -= 1
        if self.obstacle_spawn_timer <= 0:
            self.spawn_obstacle()
            self.obstacle_spawn_timer = max(30, 90 - self.difficulty * 5)
        
        # Spawn collectibles
        self.collectible_spawn_timer -= 1
        if self.collectible_spawn_timer <= 0:
            self.spawn_collectible()
            self.collectible_spawn_timer = random.randint(40, 80)
        
        # Update obstacles
        for obstacle in self.obstacles[:]:
            obstacle.update(self.player.position.z)
            if not obstacle.active:
                self.obstacles.remove(obstacle)
        
        # Update collectibles
        for collectible in self.collectibles[:]:
            collectible.update(self.player.position.z)
            if not collectible.active:
                self.collectibles.remove(collectible)
        
        # Update particles
        self.particles.update()
        
        # Check collisions
        self.check_collisions()
    
    def spawn_obstacle(self):
        """Spawn a new obstacle"""
        spawn_z = self.player.position.z + 400 + random.randint(0, 200)
        
        obstacle_types = ['barrier', 'gap', 'boulder']
        if self.difficulty >= 3:
            obstacle_types.append('moving_barrier')
        if self.difficulty >= 5:
            obstacle_types.append('spike_trap')
        
        obstacle_type = random.choice(obstacle_types)
        
        if self.difficulty >= 4 and random.random() < 0.3:
            # Multi-lane obstacle
            lanes = [-1, 0, 1]
            safe_lane = random.choice(lanes)
            for lane in lanes:
                if lane != safe_lane:
                    pos = Vector3(lane * 60, 0, spawn_z)
                    self.obstacles.append(Obstacle(pos, obstacle_type, lane))
        else:
            # Single lane obstacle
            lane = random.choice([-1, 0, 1])
            pos = Vector3(lane * 60, 0, spawn_z)
            self.obstacles.append(Obstacle(pos, obstacle_type, lane))
    
    def spawn_collectible(self):
        """Spawn a new collectible"""
        spawn_z = self.player.position.z + 300 + random.randint(0, 150)
        
        collectible_types = ['coin', 'coin', 'coin', 'gem', 'powerup']
        collectible_type = random.choice(collectible_types)
        
        if random.random() < 0.4:
            # Line of coins
            for i in range(3):
                pos = Vector3(0, 10, spawn_z + i * 30)
                self.collectibles.append(Collectible(pos, 'coin'))
        else:
            # Single collectible
            lane = random.choice([-1, 0, 1])
            height = 10 if collectible_type == 'coin' else 20
            pos = Vector3(lane * 60, height, spawn_z)
            self.collectibles.append(Collectible(pos, collectible_type))
    
    def check_collisions(self):
        """Check for collisions between player and objects"""
        player_rect = self.player.get_collision_rect(self.camera)
        
        # Check obstacle collisions
        for obstacle in self.obstacles:
            if obstacle.active and abs(obstacle.lane - self.player.lane) < 0.5:
                obstacle_rect = obstacle.get_collision_rect(self.camera)
                if player_rect.colliderect(obstacle_rect) and self.player.invulnerable_timer <= 0:
                    can_avoid = False
                    
                    if obstacle.type == 'barrier' and self.player.state == PlayerState.SLIDING:
                        can_avoid = True
                    elif obstacle.type == 'gap' and self.player.state == PlayerState.JUMPING:
                        can_avoid = True
                    
                    if not can_avoid:
                        self.game_over()
                        return
        
        # Check collectible collisions
        for collectible in self.collectibles[:]:
            if collectible.active:
                collectible_rect = collectible.get_collision_rect(self.camera)
                if player_rect.colliderect(collectible_rect):
                    self.collect_item(collectible)
                    collectible.active = False
                    self.collectibles.remove(collectible)
    
    def collect_item(self, collectible):
        """Handle collecting an item"""
        if collectible.type == 'coin':
            self.coins += 1
            self.score += 10
            self.sound_manager.play_sound('coin', 0.8)
            # Add coin particle effect
            for _ in range(5):
                vel = Vector3(random.uniform(-2, 2), random.uniform(-2, 2), random.uniform(-1, 1))
                self.particles.add_particle(collectible.position, vel, GOLD, 30)
        
        elif collectible.type == 'gem':
            self.coins += 5
            self.score += 50
            self.sound_manager.play_sound('gem', 0.9)
            # Add gem particle effect
            for _ in range(8):
                vel = Vector3(random.uniform(-3, 3), random.uniform(-3, 3), random.uniform(-2, 2))
                self.particles.add_particle(collectible.position, vel, BLUE, 40)
        
        elif collectible.type == 'powerup':
            self.player.invulnerable_timer = 180
            self.score += 100
            self.sound_manager.play_sound('powerup', 0.8)
            # Add powerup particle effect
            for _ in range(10):
                vel = Vector3(random.uniform(-4, 4), random.uniform(-4, 4), random.uniform(-2, 2))
                self.particles.add_particle(collectible.position, vel, RED, 50)
    
    def game_over(self):
        """Handle game over"""
        self.state = GameState.GAME_OVER
        self.sound_manager.play_sound('collision', 1.0)
        
        # Update high score
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
        
        # Add explosion effect
        self.camera.add_shake(10, 30)
        for _ in range(20):
            vel = Vector3(random.uniform(-5, 5), random.uniform(-5, 5), random.uniform(-3, 3))
            self.particles.add_particle(self.player.position, vel, RED, 60)
    
    def draw(self):
        """Main drawing function"""
        self.screen.fill(BLACK)
        
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.PLAYING:
            self.draw_game_world()
            self.draw_ui()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_world()
            self.draw_game_over()
        elif self.state == GameState.PAUSED:
            self.draw_game_world()
            self.draw_pause_menu()
    
    def draw_menu(self):
        """Draw the main menu"""
        # Background gradient
        for y in range(SCREEN_HEIGHT):
            color_intensity = int(50 + (y / SCREEN_HEIGHT) * 100)
            color = (color_intensity // 3, color_intensity // 2, color_intensity)
            pygame.draw.line(self.screen, color, (0, y), (SCREEN_WIDTH, y))
        
        # Title
        title_text = self.font_large.render("TEMPLE RUNNER", True, GOLD)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 200))
        self.screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_text = self.font_medium.render("Escape the Ancient Temple!", True, WHITE)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH//2, 250))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Instructions
        instructions = [
            "ARROW KEYS or WASD - Move left/right",
            "SPACE - Jump",
            "DOWN/S - Slide",
            "ESC - Pause/Menu",
            "",
            "PRESS SPACE TO START"
        ]
        
        y_offset = 350
        for instruction in instructions:
            if instruction:
                text = self.font_small.render(instruction, True, WHITE)
                text_rect = text.get_rect(center=(SCREEN_WIDTH//2, y_offset))
                self.screen.blit(text, text_rect)
            y_offset += 30
        
        # High score
        high_score_text = self.font_medium.render(f"High Score: {self.high_score}", True, GOLD)
        high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH//2, 650))
        self.screen.blit(high_score_text, high_score_rect)
    
    def draw_game_world(self):
        """Draw the 3D game world"""
        # Draw background gradient
        for y in range(SCREEN_HEIGHT):
            if y < SCREEN_HEIGHT // 2:
                intensity = int(135 + (y / (SCREEN_HEIGHT // 2)) * 120)
                color = (intensity // 4, intensity // 3, intensity)
            else:
                intensity = int(100 - ((y - SCREEN_HEIGHT // 2) / (SCREEN_HEIGHT // 2)) * 50)
                color = (intensity // 2, intensity, intensity // 3)
            pygame.draw.line(self.screen, color, (0, y), (SCREEN_WIDTH, y))
        
        # Draw path
        self.draw_path()
        
        # Draw environment
        self.draw_environment()
        
        # Draw obstacles
        for obstacle in self.obstacles:
            if obstacle.active:
                self.draw_obstacle(obstacle)
        
        # Draw collectibles
        for collectible in self.collectibles:
            if collectible.active:
                self.draw_collectible(collectible)
        
        # Draw particles
        self.particles.draw(self.screen, self.camera)
        
        # Draw player
        self.draw_player()
    
    def draw_path(self):
        """Draw the temple path"""
        for i in range(-5, 20):
            z_pos = self.player.position.z + i * 50
            
            for lane in [-1, 0, 1]:
                for j in range(3):
                    stone_z = z_pos + j * 15
                    stone_pos = Vector3(lane * 60, -5, stone_z)
                    screen_pos = self.camera.project_3d_to_2d(stone_pos)
                    
                    distance = abs(stone_z - self.camera.position.z)
                    size = max(5, int(30 * (500 / (distance + 100))))
                    
                    if 0 <= screen_pos[0] <= SCREEN_WIDTH and 0 <= screen_pos[1] <= SCREEN_HEIGHT:
                        pygame.draw.rect(self.screen, STONE_COLOR, 
                                       (screen_pos[0] - size//2, screen_pos[1] - size//2, size, size))
            
            for side in [-1, 1]:
                border_pos = Vector3(side * 120, 0, z_pos)
                screen_pos = self.camera.project_3d_to_2d(border_pos)
                distance = abs(z_pos - self.camera.position.z)
                size = max(3, int(20 * (500 / (distance + 100))))
                
                if 0 <= screen_pos[0] <= SCREEN_WIDTH and 0 <= screen_pos[1] <= SCREEN_HEIGHT:
                    pygame.draw.circle(self.screen, BROWN, screen_pos, size)
    
    def draw_environment(self):
        """Draw environmental elements"""
        for i in range(-3, 15):
            z_pos = self.player.position.z + i * 80
            
            for j in range(2, 5):
                env_pos = Vector3(-150 - j * 30, 0, z_pos + random.randint(-20, 20))
                screen_pos = self.camera.project_3d_to_2d(env_pos)
                distance = abs(z_pos - self.camera.position.z)
                
                if distance < 800:
                    size = max(5, int(40 * (500 / (distance + 100))))
                    
                    if 0 <= screen_pos[0] <= SCREEN_WIDTH and 0 <= screen_pos[1] <= SCREEN_HEIGHT:
                        if (i + j) % 3 == 0:
                            self.draw_tree(screen_pos, size)
                        else:
                            self.draw_ruin(screen_pos, size)
            
            for j in range(2, 5):
                env_pos = Vector3(150 + j * 30, 0, z_pos + random.randint(-20, 20))
                screen_pos = self.camera.project_3d_to_2d(env_pos)
                distance = abs(z_pos - self.camera.position.z)
                
                if distance < 800:
                    size = max(5, int(40 * (500 / (distance + 100))))
                    
                    if 0 <= screen_pos[0] <= SCREEN_WIDTH and 0 <= screen_pos[1] <= SCREEN_HEIGHT:
                        if (i + j) % 3 == 0:
                            self.draw_tree(screen_pos, size)
                        else:
                            self.draw_ruin(screen_pos, size)
    
    def draw_tree(self, pos, size):
        """Draw a jungle tree"""
        trunk_rect = pygame.Rect(pos[0] - size//6, pos[1] - size//4, size//3, size//2)
        pygame.draw.rect(self.screen, BROWN, trunk_rect)
        pygame.draw.circle(self.screen, DARK_GREEN, (pos[0], pos[1] - size//3), size//2)
        pygame.draw.circle(self.screen, GREEN, (pos[0], pos[1] - size//3), size//3)
    
    def draw_ruin(self, pos, size):
        """Draw ancient ruins"""
        for i in range(2):
            for j in range(3):
                block_x = pos[0] - size//2 + j * size//3
                block_y = pos[1] - size//4 + i * size//4
                block_size = size//4
                
                color = (100 + random.randint(-20, 20), 100 + random.randint(-20, 20), 80)
                pygame.draw.rect(self.screen, color, 
                               (block_x, block_y, block_size, block_size))
    
    def draw_obstacle(self, obstacle):
        """Draw an obstacle"""
        screen_pos = self.camera.project_3d_to_2d(obstacle.position)
        distance = abs(obstacle.position.z - self.camera.position.z)
        size = max(10, int(obstacle.size * (500 / (distance + 100))))
        
        if not (0 <= screen_pos[0] <= SCREEN_WIDTH and 0 <= screen_pos[1] <= SCREEN_HEIGHT):
            return
        
        if obstacle.type == 'barrier':
            pygame.draw.rect(self.screen, GRAY, 
                            (screen_pos[0] - size//2, screen_pos[1] - size, size, size * 2))
            pygame.draw.rect(self.screen, (80, 80, 80), 
                            (screen_pos[0] - size//2 + 2, screen_pos[1] - size + 2, size - 4, size * 2 - 4))
        
        elif obstacle.type == 'gap':
            pygame.draw.ellipse(self.screen, BLACK, 
                               (screen_pos[0] - size, screen_pos[1] - size//2, size * 2, size))
            pygame.draw.ellipse(self.screen, (20, 20, 20), 
                               (screen_pos[0] - size + 5, screen_pos[1] - size//2 + 5, size * 2 - 10, size - 10))
        
        elif obstacle.type == 'boulder':
            pygame.draw.circle(self.screen, (120, 100, 80), screen_pos, size)
            pygame.draw.circle(self.screen, (100, 80, 60), screen_pos, size - 3)
            for _ in range(3):
                spot_x = screen_pos[0] + random.randint(-size//2, size//2)
                spot_y = screen_pos[1] + random.randint(-size//2, size//2)
                pygame.draw.circle(self.screen, (80, 60, 40), (spot_x, spot_y), 3)
    
    def draw_collectible(self, collectible):
        """Draw a collectible item"""
        screen_pos = self.camera.project_3d_to_2d(collectible.position)
        distance = abs(collectible.position.z - self.camera.position.z)
        size = max(5, int(collectible.size * (500 / (distance + 100))))
        
        if not (0 <= screen_pos[0] <= SCREEN_WIDTH and 0 <= screen_pos[1] <= SCREEN_HEIGHT):
            return
        
        if collectible.type == 'coin':
            rotation_offset = math.sin(math.radians(collectible.rotation)) * size // 4
            pygame.draw.ellipse(self.screen, GOLD, 
                               (screen_pos[0] - size//2 + rotation_offset, screen_pos[1] - size//2, 
                                size - abs(rotation_offset * 2), size))
            pygame.draw.ellipse(self.screen, (200, 180, 0), 
                               (screen_pos[0] - size//2 + rotation_offset + 2, screen_pos[1] - size//2 + 2, 
                                size - abs(rotation_offset * 2) - 4, size - 4))
        
        elif collectible.type == 'gem':
            points = [
                (screen_pos[0], screen_pos[1] - size),
                (screen_pos[0] + size//2, screen_pos[1]),
                (screen_pos[0], screen_pos[1] + size),
                (screen_pos[0] - size//2, screen_pos[1])
            ]
            pygame.draw.polygon(self.screen, BLUE, points)
            pygame.draw.polygon(self.screen, (0, 150, 255), points, 3)
        
        elif collectible.type == 'powerup':
            for i in range(3):
                alpha = 255 - i * 60
                color = (255, alpha // 2, alpha // 4)
                pygame.draw.circle(self.screen, color, screen_pos, size - i * 2)
    
    def draw_player(self):
        """Draw the player character"""
        screen_pos = self.camera.project_3d_to_2d(self.player.position)
        size = self.player.size
        
        if self.player.invulnerable_timer > 0:
            if (self.player.invulnerable_timer // 5) % 2:
                body_color = (255, 200, 200)
            else:
                body_color = RED
        else:
            body_color = BLUE
        
        if self.player.state == PlayerState.SLIDING:
            pygame.draw.ellipse(self.screen, body_color, 
                               (screen_pos[0] - size//2, screen_pos[1] - size//4, size, size//2))
            for i in range(3):
                line_start = (screen_pos[0] - size - i * 5, screen_pos[1])
                line_end = (screen_pos[0] - size//2 - i * 5, screen_pos[1])
                pygame.draw.line(self.screen, (100, 100, 100), line_start, line_end, 2)
        else:
            pygame.draw.ellipse(self.screen, body_color, 
                               (screen_pos[0] - size//2, screen_pos[1] - size, size, size * 2))
            pygame.draw.circle(self.screen, (255, 220, 177), 
                              (screen_pos[0], screen_pos[1] - size), size//3)
            
            if self.player.state == PlayerState.RUNNING:
                arm_offset = math.sin(self.player.animation_frame) * 3
                pygame.draw.line(self.screen, body_color, 
                               (screen_pos[0] - size//3, screen_pos[1] - size//2), 
                               (screen_pos[0] - size//2 + arm_offset, screen_pos[1]), 3)
                pygame.draw.line(self.screen, body_color, 
                               (screen_pos[0] + size//3, screen_pos[1] - size//2), 
                               (screen_pos[0] + size//2 - arm_offset, screen_pos[1]), 3)
    
    def draw_ui(self):
        """Draw the game UI"""
        score_text = self.font_medium.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (20, 20))
        
        coins_text = self.font_medium.render(f"Coins: {self.coins}", True, GOLD)
        self.screen.blit(coins_text, (20, 60))
        
        distance_text = self.font_small.render(f"Distance: {int(self.distance)}m", True, WHITE)
        self.screen.blit(distance_text, (20, 100))
        
        speed_text = self.font_small.render(f"Speed: {self.speed_multiplier:.1f}x", True, WHITE)
        self.screen.blit(speed_text, (20, 130))
        
        diff_text = self.font_small.render(f"Level: {self.difficulty}", True, WHITE)
        self.screen.blit(diff_text, (20, 160))
        
        state_text = ""
        if self.player.state == PlayerState.JUMPING:
            state_text = "JUMPING"
        elif self.player.state == PlayerState.SLIDING:
            state_text = "SLIDING"
        elif self.player.invulnerable_timer > 0:
            state_text = "INVULNERABLE"
        
        if state_text:
            state_surface = self.font_small.render(state_text, True, RED)
            state_rect = state_surface.get_rect(center=(SCREEN_WIDTH//2, 50))
            self.screen.blit(state_surface, state_rect)
    
    def draw_game_over(self):
        """Draw game over screen"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.font_large.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, 250))
        self.screen.blit(game_over_text, game_over_rect)
        
        final_score_text = self.font_medium.render(f"Final Score: {self.score}", True, WHITE)
        final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH//2, 320))
        self.screen.blit(final_score_text, final_score_rect)
        
        if self.score == self.high_score:
            new_high_text = self.font_medium.render("NEW HIGH SCORE!", True, GOLD)
            new_high_rect = new_high_text.get_rect(center=(SCREEN_WIDTH//2, 360))
            self.screen.blit(new_high_text, new_high_rect)
        else:
            high_score_text = self.font_medium.render(f"High Score: {self.high_score}", True, GOLD)
            high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH//2, 360))
            self.screen.blit(high_score_text, high_score_rect)
        
        stats = [
            f"Distance: {int(self.distance)}m",
            f"Coins Collected: {self.coins}",
            f"Max Speed: {self.speed_multiplier:.1f}x",
            f"Level Reached: {self.difficulty}"
        ]
        
        y_offset = 420
        for stat in stats:
            stat_text = self.font_small.render(stat, True, WHITE)
            stat_rect = stat_text.get_rect(center=(SCREEN_WIDTH//2, y_offset))
            self.screen.blit(stat_text, stat_rect)
            y_offset += 30
        
        continue_text = self.font_medium.render("PRESS SPACE TO CONTINUE", True, WHITE)
        continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH//2, 650))
        self.screen.blit(continue_text, continue_rect)
    
    def draw_pause_menu(self):
        """Draw pause menu"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        paused_text = self.font_large.render("PAUSED", True, WHITE)
        paused_rect = paused_text.get_rect(center=(SCREEN_WIDTH//2, 300))
        self.screen.blit(paused_text, paused_rect)
        
        resume_text = self.font_medium.render("Press ESC to Resume", True, WHITE)
        resume_rect = resume_text.get_rect(center=(SCREEN_WIDTH//2, 400))
        self.screen.blit(resume_text, resume_rect)
    
    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS)
            
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
            
            if self.state == GameState.PLAYING:
                self.update()
            
            self.draw()
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()

def main():
    """Main function"""
    print("🏛️  TEMPLE RUNNER 🏛️")
    print("=" * 30)
    print("Starting game...")
    
    try:
        game = Game()
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
