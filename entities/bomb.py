"""
Bomb - Entité bombe (Bob-omb).
Si tranchée : game over instantané (mode classique) ou -10 points (challenge).
"""

import pygame
import os
import math
from typing import Optional

from config import IMAGES_DIR, Images, GameConfig


class Bomb:
    """Une bombe qui se déplace comme un fruit."""
    
    # Paramètres de la lueur
    GLOW_FREQUENCY = 4.0  # Pulsations par seconde
    GLOW_MIN_ALPHA = 80   # Alpha minimum de la lueur
    GLOW_MAX_ALPHA = 180  # Alpha maximum de la lueur
    GLOW_RADIUS_BASE = 40  # Rayon de base de la lueur
    GLOW_RADIUS_PULSE = 20  # Amplitude de pulsation du rayon
    
    def __init__(self, x: float, y: float, velocity_x: float, velocity_y: float, gravity: float):
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.gravity = gravity
        
        # États
        self.sliced = False
        self.missed = False
        self.frozen = False
        
        # Lettre pour mode clavier
        self.letter: Optional[str] = None
        
        # Timer pour l'effet de lueur
        self.glow_timer = 0.0
        
        # Chargement du sprite
        self.sprite = pygame.image.load(
            os.path.join(IMAGES_DIR, Images.BOMB)
        ).convert_alpha()
        
        # Créer la surface de lueur (pré-rendue pour performance)
        self._create_glow_surface()
        
        # Hitbox
        self.radius = GameConfig.FRUIT_SIZE // 2 - 20
    
    def _create_glow_surface(self):
        """Crée une surface de lueur rouge avec gradient radial."""
        max_radius = self.GLOW_RADIUS_BASE + self.GLOW_RADIUS_PULSE
        size = max_radius * 2
        self.glow_surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Dessiner un gradient radial rouge
        center = max_radius
        for r in range(max_radius, 0, -2):
            # Alpha diminue vers l'extérieur
            alpha = int(255 * (r / max_radius) ** 0.5)
            color = (255, 50, 50, alpha)
            pygame.draw.circle(self.glow_surface, color, (center, center), r)
    
    @property
    def center(self) -> tuple:
        half = GameConfig.FRUIT_SIZE // 2
        return (self.x + half, self.y + half)
    
    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, GameConfig.FRUIT_SIZE, GameConfig.FRUIT_SIZE)
    
    def update(self, dt: float):
        # Toujours mettre à jour le timer de lueur (même si frozen)
        self.glow_timer += dt
        
        if self.frozen:
            return
        
        # Continue de tomber même si tranchée
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
    
    def _render_glow(self, screen: pygame.Surface):
        """Affiche la lueur rouge pulsante derrière la bombe."""
        if self.sliced:
            return
        
        # Calculer l'intensité de la pulsation (sinusoïdale)
        pulse = (math.sin(self.glow_timer * self.GLOW_FREQUENCY * 2 * math.pi) + 1) / 2  # 0 à 1
        
        # Calculer l'alpha actuel
        alpha = int(self.GLOW_MIN_ALPHA + pulse * (self.GLOW_MAX_ALPHA - self.GLOW_MIN_ALPHA))
        
        # Calculer le rayon actuel
        current_radius = self.GLOW_RADIUS_BASE + pulse * self.GLOW_RADIUS_PULSE
        
        # Redimensionner la surface de lueur selon le rayon actuel
        max_radius = self.GLOW_RADIUS_BASE + self.GLOW_RADIUS_PULSE
        scale = current_radius / max_radius
        scaled_size = int(self.glow_surface.get_width() * scale)
        
        if scaled_size > 0:
            scaled_glow = pygame.transform.smoothscale(self.glow_surface, (scaled_size, scaled_size))
            scaled_glow.set_alpha(alpha)
            
            # Centrer la lueur sur la bombe
            cx, cy = self.center
            glow_rect = scaled_glow.get_rect(center=(cx, cy))
            screen.blit(scaled_glow, glow_rect, special_flags=pygame.BLEND_RGBA_ADD)
    
    def render(self, screen: pygame.Surface, font: Optional[pygame.font.Font] = None):
        # Afficher la lueur d'abord (derrière la bombe)
        self._render_glow(screen)
        
        # Afficher le sprite de la bombe
        screen.blit(self.sprite, (self.x, self.y))
        
        if self.letter and font and not self.sliced:
            # Couleur jaune comme le score, position au-dessus de la bombe
            letter_surface = font.render(self.letter, True, (254, 237, 142))
            cx, cy = self.center
            letter_rect = letter_surface.get_rect(centerx=cx, bottom=cy - 100)
            screen.blit(letter_surface, letter_rect)
