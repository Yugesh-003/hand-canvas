"""
3D Rendering Module for Temple Runner
Contains all drawing and visual effects methods
"""

import pygame
import math
import random
from temple_runner import *

def draw_path(self):
    """Draw the temple path/runway"""
    # Draw main path segments
    for i in range(-5, 20):
        z_pos = self.player.position.z + i * 50
        
        # Path segments
        for lane in [-1, 0, 1]:
            # Path stones
            for j in range(3):
                stone_z = z_pos + j * 15
                stone_pos = Vector3(lane * 60, -5, stone_z)
                screen_pos = self.camera.project_3d_to_2d(stone_pos)
                
                # Calculate size based on distance
                distance = abs(stone_z - self.camera.position.z)
                size = max(5, int(30 * (500 / (distance + 100))))
                
                if 0 <= screen_pos[0] <= SCREEN_WIDTH and 0 <= screen_pos[1] <= SCREEN_HEIGHT:
                    pygame.draw.rect(self.screen, STONE_COLOR, 
                                   (screen_pos[0] - size//2, screen_pos[1] - size//2, size, size))
        
        # Path borders
        for side in [-1, 1]:
            border_pos = Vector3(side * 120, 0, z_pos)
            screen_pos = self.camera.project_3d_to_2d(border_pos)
            distance = abs(z_pos - self.camera.position.z)
            size = max(3, int(20 * (500 / (distance + 100))))
            
            if 0 <= screen_pos[0] <= SCREEN_WIDTH and 0 <= screen_pos[1] <= SCREEN_HEIGHT:
                pygame.draw.circle(self.screen, BROWN, screen_pos, size)

def draw_environment(self):
    """Draw environmental elements like trees, ruins, etc."""
    # Draw trees and ruins on the sides
    for i in range(-3, 15):
        z_pos = self.player.position.z + i * 80
        
        # Left side environment
        for j in range(2, 5):
            env_pos = Vector3(-150 - j * 30, 0, z_pos + random.randint(-20, 20))
            screen_pos = self.camera.project_3d_to_2d(env_pos)
            distance = abs(z_pos - self.camera.position.z)
            
            if distance < 800:  # Only draw nearby objects
                size = max(5, int(40 * (500 / (distance + 100))))
                
                if 0 <= screen_pos[0] <= SCREEN_WIDTH and 0 <= screen_pos[1] <= SCREEN_HEIGHT:
                    # Alternate between trees and ruins
                    if (i + j) % 3 == 0:
                        self.draw_tree(screen_pos, size)
                    else:
                        self.draw_ruin(screen_pos, size)
        
        # Right side environment
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
    # Tree trunk
    trunk_rect = pygame.Rect(pos[0] - size//6, pos[1] - size//4, size//3, size//2)
    pygame.draw.rect(self.screen, BROWN, trunk_rect)
    
    # Tree canopy
    pygame.draw.circle(self.screen, DARK_GREEN, (pos[0], pos[1] - size//3), size//2)
    pygame.draw.circle(self.screen, GREEN, (pos[0], pos[1] - size//3), size//3)

def draw_ruin(self, pos, size):
    """Draw ancient ruins"""
    # Ruin blocks
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
        # Draw barrier as a wall
        pygame.draw.rect(self.screen, GRAY, 
                        (screen_pos[0] - size//2, screen_pos[1] - size, size, size * 2))
        # Add some detail
        pygame.draw.rect(self.screen, (80, 80, 80), 
                        (screen_pos[0] - size//2 + 2, screen_pos[1] - size + 2, size - 4, size * 2 - 4))
    
    elif obstacle.type == 'gap':
        # Draw gap as dark pit
        pygame.draw.ellipse(self.screen, BLACK, 
                           (screen_pos[0] - size, screen_pos[1] - size//2, size * 2, size))
        pygame.draw.ellipse(self.screen, (20, 20, 20), 
                           (screen_pos[0] - size + 5, screen_pos[1] - size//2 + 5, size * 2 - 10, size - 10))
    
    elif obstacle.type == 'boulder':
        # Draw boulder as a circle with texture
        pygame.draw.circle(self.screen, (120, 100, 80), screen_pos, size)
        pygame.draw.circle(self.screen, (100, 80, 60), screen_pos, size - 3)
        # Add some spots for texture
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
        # Animated spinning coin
        rotation_offset = math.sin(math.radians(collectible.rotation)) * size // 4
        pygame.draw.ellipse(self.screen, GOLD, 
                           (screen_pos[0] - size//2 + rotation_offset, screen_pos[1] - size//2, 
                            size - abs(rotation_offset * 2), size))
        pygame.draw.ellipse(self.screen, (200, 180, 0), 
                           (screen_pos[0] - size//2 + rotation_offset + 2, screen_pos[1] - size//2 + 2, 
                            size - abs(rotation_offset * 2) - 4, size - 4))
    
    elif collectible.type == 'gem':
        # Diamond-shaped gem
        points = [
            (screen_pos[0], screen_pos[1] - size),
            (screen_pos[0] + size//2, screen_pos[1]),
            (screen_pos[0], screen_pos[1] + size),
            (screen_pos[0] - size//2, screen_pos[1])
        ]
        pygame.draw.polygon(self.screen, BLUE, points)
        pygame.draw.polygon(self.screen, (0, 150, 255), points, 3)
    
    elif collectible.type == 'powerup':
        # Glowing orb
        for i in range(3):
            alpha = 255 - i * 60
            color = (255, alpha // 2, alpha // 4)
            pygame.draw.circle(self.screen, color, screen_pos, size - i * 2)

def draw_player(self):
    """Draw the player character"""
    screen_pos = self.camera.project_3d_to_2d(self.player.position)
    size = self.player.size
    
    # Player body color changes based on state
    if self.player.invulnerable_timer > 0:
        # Flashing effect when invulnerable
        if (self.player.invulnerable_timer // 5) % 2:
            body_color = (255, 200, 200)
        else:
            body_color = RED
    else:
        body_color = BLUE
    
    if self.player.state == PlayerState.SLIDING:
        # Draw sliding player (smaller height)
        pygame.draw.ellipse(self.screen, body_color, 
                           (screen_pos[0] - size//2, screen_pos[1] - size//4, size, size//2))
        # Add some motion lines
        for i in range(3):
            line_start = (screen_pos[0] - size - i * 5, screen_pos[1])
            line_end = (screen_pos[0] - size//2 - i * 5, screen_pos[1])
            pygame.draw.line(self.screen, (100, 100, 100), line_start, line_end, 2)
    
    else:
        # Draw normal player
        # Body
        pygame.draw.ellipse(self.screen, body_color, 
                           (screen_pos[0] - size//2, screen_pos[1] - size, size, size * 2))
        
        # Head
        pygame.draw.circle(self.screen, (255, 220, 177), 
                          (screen_pos[0], screen_pos[1] - size), size//3)
        
        # Simple animation for running
        if self.player.state == PlayerState.RUNNING:
            arm_offset = math.sin(self.player.animation_frame) * 3
            # Arms
            pygame.draw.line(self.screen, body_color, 
                           (screen_pos[0] - size//3, screen_pos[1] - size//2), 
                           (screen_pos[0] - size//2 + arm_offset, screen_pos[1]), 3)
            pygame.draw.line(self.screen, body_color, 
                           (screen_pos[0] + size//3, screen_pos[1] - size//2), 
                           (screen_pos[0] + size//2 - arm_offset, screen_pos[1]), 3)

def draw_ui(self):
    """Draw the game UI"""
    # Score
    score_text = self.font_medium.render(f"Score: {self.score}", True, WHITE)
    self.screen.blit(score_text, (20, 20))
    
    # Coins
    coins_text = self.font_medium.render(f"Coins: {self.coins}", True, GOLD)
    self.screen.blit(coins_text, (20, 60))
    
    # Distance
    distance_text = self.font_small.render(f"Distance: {int(self.distance)}m", True, WHITE)
    self.screen.blit(distance_text, (20, 100))
    
    # Speed
    speed_text = self.font_small.render(f"Speed: {self.speed_multiplier:.1f}x", True, WHITE)
    self.screen.blit(speed_text, (20, 130))
    
    # Difficulty level
    diff_text = self.font_small.render(f"Level: {self.difficulty}", True, WHITE)
    self.screen.blit(diff_text, (20, 160))
    
    # Player state indicator
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
    # Semi-transparent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(128)
    overlay.fill(BLACK)
    self.screen.blit(overlay, (0, 0))
    
    # Game Over text
    game_over_text = self.font_large.render("GAME OVER", True, RED)
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, 250))
    self.screen.blit(game_over_text, game_over_rect)
    
    # Final score
    final_score_text = self.font_medium.render(f"Final Score: {self.score}", True, WHITE)
    final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH//2, 320))
    self.screen.blit(final_score_text, final_score_rect)
    
    # High score
    if self.score == self.high_score:
        new_high_text = self.font_medium.render("NEW HIGH SCORE!", True, GOLD)
        new_high_rect = new_high_text.get_rect(center=(SCREEN_WIDTH//2, 360))
        self.screen.blit(new_high_text, new_high_rect)
    else:
        high_score_text = self.font_medium.render(f"High Score: {self.high_score}", True, GOLD)
        high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH//2, 360))
        self.screen.blit(high_score_text, high_score_rect)
    
    # Stats
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
    
    # Continue instruction
    continue_text = self.font_medium.render("PRESS SPACE TO CONTINUE", True, WHITE)
    continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH//2, 650))
    self.screen.blit(continue_text, continue_rect)

def draw_pause_menu(self):
    """Draw pause menu"""
    # Semi-transparent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(128)
    overlay.fill(BLACK)
    self.screen.blit(overlay, (0, 0))
    
    # Paused text
    paused_text = self.font_large.render("PAUSED", True, WHITE)
    paused_rect = paused_text.get_rect(center=(SCREEN_WIDTH//2, 300))
    self.screen.blit(paused_text, paused_rect)
    
    # Instructions
    resume_text = self.font_medium.render("Press ESC to Resume", True, WHITE)
    resume_rect = resume_text.get_rect(center=(SCREEN_WIDTH//2, 400))
    self.screen.blit(resume_text, resume_rect)

# Add these methods to the Game class
Game.draw_path = draw_path
Game.draw_environment = draw_environment
Game.draw_tree = draw_tree
Game.draw_ruin = draw_ruin
Game.draw_obstacle = draw_obstacle
Game.draw_collectible = draw_collectible
Game.draw_player = draw_player
Game.draw_ui = draw_ui
Game.draw_game_over = draw_game_over
Game.draw_pause_menu = draw_pause_menu
