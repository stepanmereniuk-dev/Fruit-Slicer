"""
Splash - Éclaboussure qui apparaît quand un fruit est tranché.
"""

import pygame
import os
from typing import Optional

from config import IMAGES_DIR, Images, GameConfig


class Splash:
    """Éclaboussure temporaire à l'endroit où un fruit a été tranché."""
    
    # Durée d'affichage de l'éclaboussure
    DURATION = 2.0  # secondes
    
    def __init__(self, fruit_type: str, x: float, y: float):
        """
        Args:
            fruit_type: Type du fruit (pour charger la bonne éclaboussure)
            x: Position X du centre
            y: Position Y du centre
        """
        self.x = x
        self.y = y
        self.timer = self.DURATION
        self.finished = False
        
        # Charger le sprite d'éclaboussure
        splash_path = Images.FRUITS.get(fruit_type, {}).get('splash')
        if splash_path:
            self.sprite = pygame.image.load(
                os.path.join(IMAGES_DIR, splash_path)
            ).convert_alpha()
        else:
            self.sprite = None
    
    def update(self, dt: float):
        """Met à jour le timer."""
        self.timer -= dt
        if self.timer <= 0:
            self.finished = True
    
    def render(self, screen: pygame.Surface):
        """Affiche l'éclaboussure avec effet de fondu."""
        if self.sprite and not self.finished:
            # Calculer l'alpha selon le temps restant (fondu progressif)
            alpha = int(255 * (self.timer / self.DURATION))
            alpha = max(0, min(255, alpha))
            
            # Copier le sprite et appliquer l'alpha
            sprite_copy = self.sprite.copy()
            sprite_copy.set_alpha(alpha)
            
            # Centrer le sprite sur la position
            rect = sprite_copy.get_rect(center=(self.x, self.y))
            screen.blit(sprite_copy, rect)
