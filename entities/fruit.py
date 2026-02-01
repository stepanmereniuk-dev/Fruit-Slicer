"""
Fruit - Fruit entity to slice.
Handles its display, physics, and different states.
"""

import pygame
import os
import random
from typing import Optional

from config import IMAGES_DIR, Images, GameConfig


class Fruit:
    """
    A fruit that moves on the screen.
    States: normal, frozen, sliced
    """
    
    def __init__(self, fruit_type: str, x: float, y: float, velocity_x: float, velocity_y: float, gravity: float):
        self.fruit_type = fruit_type
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.gravity = gravity
        
        # States
        self.sliced = False
        self.frozen = False
        self.missed = False  # Exited bottom without being sliced
        
        # Letter for keyboard mode (assigned by spawner)
        self.letter: Optional[str] = None
        
        # Load sprites
        self._load_sprites()
        
        # Circular hitbox centered
        self.radius = GameConfig.FRUIT_SIZE // 2 - 20  # Margin for more precise hitbox
    
    def _load_sprites(self):
        """Loads the fruit sprites."""
        sprites_data = Images.FRUITS.get(self.fruit_type)
        
        self.sprite_normal = pygame.image.load(
            os.path.join(IMAGES_DIR, sprites_data['normal'])
        ).convert_alpha()
        
        self.sprite_sliced = pygame.image.load(
            os.path.join(IMAGES_DIR, sprites_data['sliced'])
        ).convert_alpha()
        
        self.sprite_frozen = pygame.image.load(
            os.path.join(IMAGES_DIR, sprites_data['frozen'])
        ).convert_alpha()
        
        self.sprite_splash = pygame.image.load(
            os.path.join(IMAGES_DIR, sprites_data['splash'])
        ).convert_alpha()
    
    @property
    def current_sprite(self) -> pygame.Surface:
        """Returns the sprite according to the current state."""
        if self.sliced:
            return self.sprite_sliced
        elif self.frozen:
            return self.sprite_frozen
        return self.sprite_normal
    
    @property
    def center(self) -> tuple:
        """Center position of the fruit."""
        half = GameConfig.FRUIT_SIZE // 2
        return (self.x + half, self.y + half)
    
    @property
    def rect(self) -> pygame.Rect:
        """Bounding rectangle for rendering."""
        return pygame.Rect(self.x, self.y, GameConfig.FRUIT_SIZE, GameConfig.FRUIT_SIZE)
    
    def update(self, dt: float):
        """Updates position according to physics."""
        if self.frozen:
            return
        
        # Sliced fruits continue falling (to exit the screen)
        # Update velocity (gravity)
        self.velocity_y += self.gravity * dt
        
        # Update position
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
    
    def freeze(self):
        """Freezes the fruit (stops its movement)."""
        self.frozen = True
    
    def unfreeze(self):
        """Unfreezes the fruit."""
        self.frozen = False
    
    def slice(self):
        """Slices the fruit."""
        self.sliced = True
    
    def is_off_screen(self, screen_height: int) -> bool:
        """Checks if the fruit has exited from the bottom."""
        return self.y > screen_height
    
    def collides_with_point(self, point: tuple) -> bool:
        """Checks collision with a point (mouse mode)."""
        cx, cy = self.center
        px, py = point
        distance = ((cx - px) ** 2 + (cy - py) ** 2) ** 0.5
        return distance <= self.radius
    
    def collides_with_line(self, p1: tuple, p2: tuple) -> bool:
        """Checks collision with a line segment (mouse trail)."""
        # Simplified point-to-segment distance
        cx, cy = self.center
        x1, y1 = p1
        x2, y2 = p2
        
        # Segment vector
        dx = x2 - x1
        dy = y2 - y1
        
        # Squared length of segment
        length_sq = dx * dx + dy * dy
        
        if length_sq == 0:
            # Zero-length segment = point
            return self.collides_with_point(p1)
        
        # Project center onto segment
        t = max(0, min(1, ((cx - x1) * dx + (cy - y1) * dy) / length_sq))
        
        # Closest point on segment
        closest_x = x1 + t * dx
        closest_y = y1 + t * dy
        
        # Distance to center
        distance = ((cx - closest_x) ** 2 + (cy - closest_y) ** 2) ** 0.5
        
        return distance <= self.radius
    
    def render(self, screen: pygame.Surface, font: Optional[pygame.font.Font] = None):
        """Renders the fruit."""
        screen.blit(self.current_sprite, (self.x, self.y))
        
        if self.letter and font and not self.sliced:
            # Yellow color like the score, positioned above the fruit
            letter_surface = font.render(self.letter, True, (254, 237, 142))
            cx, cy = self.center
            letter_rect = letter_surface.get_rect(centerx=cx, bottom=cy - 100)
            screen.blit(letter_surface, letter_rect)
    
    def render_splash(self, screen: pygame.Surface):
        """Renders the splash (after slicing)."""
        if self.sliced:
            screen.blit(self.sprite_splash, (self.x, self.y))


def create_random_fruit(x: float, y: float, velocity_x: float, velocity_y: float, gravity: float) -> Fruit:
    """Creates a fruit of random type."""
    fruit_type = random.choice(GameConfig.FRUIT_TYPES)
    return Fruit(fruit_type, x, y, velocity_x, velocity_y, gravity)
