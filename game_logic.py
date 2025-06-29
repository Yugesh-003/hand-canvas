"""
Game Logic Module for Temple Runner
Contains update and rendering methods
"""

import pygame
import random
import math
from temple_runner import *

def update_game(self):
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
        # Decrease spawn interval as difficulty increases
        self.obstacle_spawn_timer = max(30, 90 - self.difficulty * 5)
    
    # Spawn collectibles
    self.collectible_spawn_timer -= 1
    if self.collectible_spawn_timer <= 0:
        self.spawn_collectible()
        self.collectible_spawn_timer = random.randint(40, 80)
    
    # Update obstacles
    for obstacle in self.obstacles[:]:
        obstacle.update()
        if not obstacle.active:
            self.obstacles.remove(obstacle)
    
    # Update collectibles
    for collectible in self.collectibles[:]:
        collectible.update()
        if not collectible.active:
            self.collectibles.remove(collectible)
    
    # Update particles
    self.particles.update()
    
    # Check collisions
    self.check_collisions()

def spawn_obstacle(self):
    """Spawn a new obstacle"""
    spawn_z = self.player.position.z + 400 + random.randint(0, 200)
    
    # Choose obstacle type based on difficulty
    obstacle_types = ['barrier', 'gap', 'boulder']
    if self.difficulty >= 3:
        obstacle_types.append('moving_barrier')
    if self.difficulty >= 5:
        obstacle_types.append('spike_trap')
    
    obstacle_type = random.choice(obstacle_types)
    
    # Choose lane (sometimes multiple lanes for higher difficulty)
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
    
    # Choose collectible type
    collectible_types = ['coin', 'coin', 'coin', 'gem', 'powerup']  # Coins are more common
    collectible_type = random.choice(collectible_types)
    
    # Sometimes spawn collectibles in patterns
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
    player_rect = self.player.get_collision_rect()
    
    # Check obstacle collisions
    for obstacle in self.obstacles:
        if obstacle.active and abs(obstacle.lane - self.player.lane) < 0.5:
            obstacle_rect = obstacle.get_collision_rect()
            if player_rect.colliderect(obstacle_rect) and self.player.invulnerable_timer <= 0:
                # Check if player can avoid obstacle
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
            collectible_rect = collectible.get_collision_rect()
            if player_rect.colliderect(collectible_rect):
                self.collect_item(collectible)
                collectible.active = False
                self.collectibles.remove(collectible)

def collect_item(self, collectible):
    """Handle collecting an item"""
    if collectible.type == 'coin':
        self.coins += 1
        self.score += 10
        # Add coin particle effect
        for _ in range(5):
            vel = Vector3(random.uniform(-2, 2), random.uniform(-2, 2), random.uniform(-1, 1))
            self.particles.add_particle(collectible.position, vel, GOLD, 30)
    
    elif collectible.type == 'gem':
        self.coins += 5
        self.score += 50
        # Add gem particle effect
        for _ in range(8):
            vel = Vector3(random.uniform(-3, 3), random.uniform(-3, 3), random.uniform(-2, 2))
            self.particles.add_particle(collectible.position, vel, BLUE, 40)
    
    elif collectible.type == 'powerup':
        self.player.invulnerable_timer = 180  # 3 seconds of invulnerability
        self.score += 100
        # Add powerup particle effect
        for _ in range(10):
            vel = Vector3(random.uniform(-4, 4), random.uniform(-4, 4), random.uniform(-2, 2))
            self.particles.add_particle(collectible.position, vel, RED, 50)

def game_over(self):
    """Handle game over"""
    self.state = GameState.GAME_OVER
    
    # Update high score
    if self.score > self.high_score:
        self.high_score = self.score
        self.save_high_score()
    
    # Add explosion effect
    self.camera.add_shake(10, 30)
    for _ in range(20):
        vel = Vector3(random.uniform(-5, 5), random.uniform(-5, 5), random.uniform(-3, 3))
        self.particles.add_particle(self.player.position, vel, RED, 60)

def draw_game(self):
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
    # Draw background gradient (sky to ground)
    for y in range(SCREEN_HEIGHT):
        if y < SCREEN_HEIGHT // 2:
            # Sky gradient
            intensity = int(135 + (y / (SCREEN_HEIGHT // 2)) * 120)
            color = (intensity // 4, intensity // 3, intensity)
        else:
            # Ground gradient
            intensity = int(100 - ((y - SCREEN_HEIGHT // 2) / (SCREEN_HEIGHT // 2)) * 50)
            color = (intensity // 2, intensity, intensity // 3)
        pygame.draw.line(self.screen, color, (0, y), (SCREEN_WIDTH, y))
    
    # Draw ground/path
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

# Add these methods to the Game class
Game.update = update_game
Game.spawn_obstacle = spawn_obstacle
Game.spawn_collectible = spawn_collectible
Game.check_collisions = check_collisions
Game.collect_item = collect_item
Game.game_over = game_over
Game.draw = draw_game
Game.draw_menu = draw_menu
Game.draw_game_world = draw_game_world
