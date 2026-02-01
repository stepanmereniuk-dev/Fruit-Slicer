"""
Splash - Splash effect that appears when a fruit is sliced.
"""

import pygame
import os
from typing import Optional

from config import IMAGES_DIR, Images, GameConfig


class Splash:
    """Temporary splash at the location where a fruit was sliced."""
    
    # Splash display duration
    DURATION = 2.0  # seconds
    
    def __init__(self, fruit_type: str, x: float, y: float):
        """
        Args:
            fruit_type: Fruit type (to load the correct splash)
            x: X position of the center
            y: Y position of the center
        """
        self.x = x
        self.y = y
        self.timer = self.DURATION
        self.finished = False
        
        # Load splash sprite
        splash_path = Images.FRUITS.get(fruit_type, {}).get('splash')
        if splash_path:
            self.sprite = pygame.image.load(
                os.path.join(IMAGES_DIR, splash_path)
            ).convert_alpha()
        else:
            self.sprite = None
    
    def update(self, dt: float):
        """Updates the timer."""
        self.timer -= dt
        if self.timer <= 0:
            self.finished = True
    
    def render(self, screen: pygame.Surface):
        """Renders the splash with a fade effect."""
        if self.sprite and not self.finished:
            # Calculate alpha based on remaining time (progressive fade)
            alpha = int(255 * (self.timer / self.DURATION))
            alpha = max(0, min(255, alpha))
            
            # Copy sprite and apply alpha
            sprite_copy = self.sprite.copy()
            sprite_copy.set_alpha(alpha)
            
            # Center sprite on position
            rect = sprite_copy.get_rect(center=(self.x, self.y))
            screen.blit(sprite_copy, rect)