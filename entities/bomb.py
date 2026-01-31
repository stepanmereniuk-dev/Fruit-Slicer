"""
Bomb - Entité bombe (Bob-omb).
Si tranchée : game over instantané (mode classique) ou -10 points (challenge).
"""

import pygame
import os
from typing import Optional

from config import IMAGES_DIR, Images, GameConfig


class Bomb:
    """Une bombe qui se déplace comme un fruit."""
    
    def __init__(self, x: float, y: float, velocity_x: float, velocity_y: float, gravity: float):
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.gravity = gravity
        
        # États
        self.sliced = False
        self.frozen = False
        
        # Lettre pour mode clavier
        self.letter: Optional[str] = None
        
        # Chargement du sprite
        self.sprite = pygame.image.load(
            os.path.join(IMAGES_DIR, Images.BOMB)
        ).convert_alpha()
        
        # Hitbox
        self.radius = GameConfig.FRUIT_SIZE // 2 - 20
    
    @property
    def center(self) -> tuple:
        half = GameConfig.FRUIT_SIZE // 2
        return (self.x + half, self.y + half)
    
    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, GameConfig.FRUIT_SIZE, GameConfig.FRUIT_SIZE)
    
    def update(self, dt: float):
        if self.frozen or self.sliced:
            return
        
        self.velocity_y += self.gravity * dt
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
    
    def freeze(self):
        self.frozen = True
    
    def unfreeze(self):
        self.frozen = False
    
    def slice(self):
        self.sliced = True
    
    def is_off_screen(self, screen_height: int) -> bool:
        return self.y > screen_height
    
    def collides_with_point(self, point: tuple) -> bool:
        cx, cy = self.center
        px, py = point
        distance = ((cx - px) ** 2 + (cy - py) ** 2) ** 0.5
        return distance <= self.radius
    
    def collides_with_line(self, p1: tuple, p2: tuple) -> bool:
        cx, cy = self.center
        x1, y1 = p1
        x2, y2 = p2
        
        dx = x2 - x1
        dy = y2 - y1
        length_sq = dx * dx + dy * dy
        
        if length_sq == 0:
            return self.collides_with_point(p1)
        
        t = max(0, min(1, ((cx - x1) * dx + (cy - y1) * dy) / length_sq))
        closest_x = x1 + t * dx
        closest_y = y1 + t * dy
        distance = ((cx - closest_x) ** 2 + (cy - closest_y) ** 2) ** 0.5
        
        return distance <= self.radius
    
    def render(self, screen: pygame.Surface, font: Optional[pygame.font.Font] = None):
        screen.blit(self.sprite, (self.x, self.y))
        
        if self.letter and font and not self.sliced:
            letter_surface = font.render(self.letter, True, (255, 255, 255))
            letter_rect = letter_surface.get_rect(center=self.center)
            screen.blit(letter_surface, letter_rect)
