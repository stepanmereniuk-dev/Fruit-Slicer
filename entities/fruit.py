"""
Fruit - Entité fruit à trancher.
Gère son affichage, sa physique et ses différents états.
"""

import pygame
import os
import random
from typing import Optional

from config import IMAGES_DIR, Images, GameConfig


class Fruit:
    """
    Un fruit qui se déplace à l'écran.
    États : normal, frozen (gelé), sliced (tranché)
    """
    
    def __init__(self, fruit_type: str, x: float, y: float, velocity_x: float, velocity_y: float, gravity: float):
        self.fruit_type = fruit_type
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.gravity = gravity
        
        # États
        self.sliced = False
        self.frozen = False
        self.missed = False  # Sorti par le bas sans être tranché
        
        # Lettre pour mode clavier (assignée par le spawner)
        self.letter: Optional[str] = None
        
        # Chargement des sprites
        self._load_sprites()
        
        # Hitbox circulaire centrée
        self.radius = GameConfig.FRUIT_SIZE // 2 - 20  # Marge pour hitbox plus précise
    
    def _load_sprites(self):
        """Charge les sprites du fruit."""
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
        """Retourne le sprite selon l'état actuel."""
        if self.sliced:
            return self.sprite_sliced
        elif self.frozen:
            return self.sprite_frozen
        return self.sprite_normal
    
    @property
    def center(self) -> tuple:
        """Position du centre du fruit."""
        half = GameConfig.FRUIT_SIZE // 2
        return (self.x + half, self.y + half)
    
    @property
    def rect(self) -> pygame.Rect:
        """Rectangle englobant pour le rendu."""
        return pygame.Rect(self.x, self.y, GameConfig.FRUIT_SIZE, GameConfig.FRUIT_SIZE)
    
    def update(self, dt: float):
        """Met à jour la position selon la physique."""
        if self.frozen or self.sliced:
            return
        
        # Mise à jour vitesse (gravité)
        self.velocity_y += self.gravity * dt
        
        # Mise à jour position
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
    
    def freeze(self):
        """Gèle le fruit (arrête son mouvement)."""
        self.frozen = True
    
    def unfreeze(self):
        """Dégèle le fruit."""
        self.frozen = False
    
    def slice(self):
        """Tranche le fruit."""
        self.sliced = True
    
    def is_off_screen(self, screen_height: int) -> bool:
        """Vérifie si le fruit est sorti par le bas."""
        return self.y > screen_height
    
    def collides_with_point(self, point: tuple) -> bool:
        """Vérifie la collision avec un point (mode souris)."""
        cx, cy = self.center
        px, py = point
        distance = ((cx - px) ** 2 + (cy - py) ** 2) ** 0.5
        return distance <= self.radius
    
    def collides_with_line(self, p1: tuple, p2: tuple) -> bool:
        """Vérifie la collision avec un segment de ligne (traînée souris)."""
        # Distance point-segment simplifiée
        cx, cy = self.center
        x1, y1 = p1
        x2, y2 = p2
        
        # Vecteur du segment
        dx = x2 - x1
        dy = y2 - y1
        
        # Longueur au carré du segment
        length_sq = dx * dx + dy * dy
        
        if length_sq == 0:
            # Segment de longueur nulle = point
            return self.collides_with_point(p1)
        
        # Projection du centre sur le segment
        t = max(0, min(1, ((cx - x1) * dx + (cy - y1) * dy) / length_sq))
        
        # Point le plus proche sur le segment
        closest_x = x1 + t * dx
        closest_y = y1 + t * dy
        
        # Distance au centre
        distance = ((cx - closest_x) ** 2 + (cy - closest_y) ** 2) ** 0.5
        
        return distance <= self.radius
    
    def render(self, screen: pygame.Surface, font: Optional[pygame.font.Font] = None):
        """Affiche le fruit."""
        screen.blit(self.current_sprite, (self.x, self.y))
        
        # Affiche la lettre en mode clavier
        if self.letter and font and not self.sliced:
            letter_surface = font.render(self.letter, True, (255, 255, 255))
            letter_rect = letter_surface.get_rect(center=self.center)
            screen.blit(letter_surface, letter_rect)
    
    def render_splash(self, screen: pygame.Surface):
        """Affiche l'éclaboussure (après tranchage)."""
        if self.sliced:
            screen.blit(self.sprite_splash, (self.x, self.y))


def create_random_fruit(x: float, y: float, velocity_x: float, velocity_y: float, gravity: float) -> Fruit:
    """Crée un fruit de type aléatoire."""
    fruit_type = random.choice(GameConfig.FRUIT_TYPES)
    return Fruit(fruit_type, x, y, velocity_x, velocity_y, gravity)
