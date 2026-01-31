"""
NotificationManager - Affiche les succès débloqués.

Selon la doc :
- Position : bas gauche de l'écran
- Une seule notification visible à la fois
- File d'attente si plusieurs succès débloqués
- Durée : 3 secondes par notification
"""

import pygame
import math
from typing import List, Optional
from dataclasses import dataclass

from core.achievements import Achievement
from core.lang_manager import get as lang_get  # Import direct pour éviter circulaire


# Palette thème Mario/Yoshi
COLORS = {
    'background': (50, 50, 50, 230),
    'border': (255, 193, 7),       # Or
    'title': (255, 213, 79),       # Jaune
    'text': (255, 255, 255),
    'star': (255, 193, 7),
}


@dataclass
class Notification:
    """Une notification en cours d'affichage."""
    achievement: Achievement
    timer: float        # Temps restant en phase 'display'
    phase: str          # 'enter' -> 'display' -> 'exit'
    progress: float     # 0.0 à 1.0 pour les animations enter/exit


class NotificationManager:
    """
    Gère l'affichage des notifications de succès.
    Utilisation :
        manager.add(achievement)      # Ajoute à la file
        manager.update(dt)            # Appelé chaque frame
        manager.render(screen)        # Affiche si notification active
    """
    
    # Configuration
    DURATION = 3.0      # Durée d'affichage (secondes)
    FADE_TIME = 0.3     # Durée animation enter/exit
    WIDTH = 300
    HEIGHT = 60
    MARGIN = 20         # Distance depuis les bords
    
    def __init__(self):
        self.current: Optional[Notification] = None  # Notification affichée
        self.queue: List[Achievement] = []           # File d'attente
        self.font: Optional[pygame.font.Font] = None
        self.font_small: Optional[pygame.font.Font] = None
        self.sound: Optional[pygame.mixer.Sound] = None
    
    def set_sound(self, sound: pygame.mixer.Sound):
        """Définit le son joué lors d'un nouveau succès."""
        self.sound = sound
    
    def add(self, achievement: Achievement):
        """Ajoute un succès à la file d'attente."""
        self.queue.append(achievement)
    
    def add_many(self, achievements: List[Achievement]):
        """Ajoute plusieurs succès à la file."""
        self.queue.extend(achievements)
    
    def update(self, dt: float):
        """Met à jour l'état de la notification (appelé chaque frame)."""
        
        # Prendre le prochain succès si aucune notification active
        if not self.current and self.queue:
            self.current = Notification(
                achievement=self.queue.pop(0),
                timer=self.DURATION,
                phase='enter',
                progress=0.0
            )
            if self.sound:
                self.sound.play()
        
        if not self.current:
            return
        
        # Machine à états : enter -> display -> exit -> None
        n = self.current
        
        if n.phase == 'enter':
            n.progress += dt / self.FADE_TIME
            if n.progress >= 1.0:
                n.progress = 1.0
                n.phase = 'display'
        
        elif n.phase == 'display':
            n.timer -= dt
            if n.timer <= 0:
                n.phase = 'exit'
                n.progress = 0.0
        
        elif n.phase == 'exit':
            n.progress += dt / self.FADE_TIME
            if n.progress >= 1.0:
                self.current = None  # Notification terminée
    
    def render(self, screen: pygame.Surface):
        """Affiche la notification active (si présente)."""
        if not self.current:
            return
        
        self._init_fonts()
        
        # Position cible : bas gauche
        screen_h = screen.get_height()
        target_x = self.MARGIN
        target_y = screen_h - self.HEIGHT - self.MARGIN
        
        # Animation slide horizontal
        if self.current.phase == 'enter':
            # Slide depuis la gauche (hors écran -> position finale)
            x = -self.WIDTH + (target_x + self.WIDTH) * self._ease_out(self.current.progress)
        elif self.current.phase == 'exit':
            # Slide vers la gauche (position finale -> hors écran)
            x = target_x - (target_x + self.WIDTH) * self._ease_in(self.current.progress)
        else:
            x = target_x
        
        self._draw(screen, int(x), target_y)
    
    def _draw(self, screen: pygame.Surface, x: int, y: int):
        """Dessine la notification à la position donnée."""
        surface = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        
        # Fond + bordure dorée
        pygame.draw.rect(surface, COLORS['background'], (0, 0, self.WIDTH, self.HEIGHT), border_radius=8)
        pygame.draw.rect(surface, COLORS['border'], (0, 0, self.WIDTH, self.HEIGHT), 2, border_radius=8)
        
        # Étoile animée (pulsation pendant 'display')
        star_size = 15
        if self.current.phase == 'display':
            pulse = 1.0 + 0.15 * math.sin(self.current.timer * 10)
            star_size = int(15 * pulse)
        self._draw_star(surface, 25, self.HEIGHT // 2, star_size)
        
        # Texte "Succès débloqué !"
        header = lang_get("achievements.unlocked_notification")
        header_surf = self.font_small.render(header, True, COLORS['title'])
        surface.blit(header_surf, (50, 10))
        
        # Nom du succès (tronqué si trop long)
        name = self.current.achievement.name
        name_surf = self.font.render(name, True, COLORS['text'])
        max_width = self.WIDTH - 60
        
        while name_surf.get_width() > max_width and len(name) > 3:
            name = name[:-4] + "..."
            name_surf = self.font.render(name, True, COLORS['text'])
        
        surface.blit(name_surf, (50, 32))
        screen.blit(surface, (x, y))
    
    def _draw_star(self, surface: pygame.Surface, cx: int, cy: int, size: int):
        """Dessine une étoile à 5 branches."""
        points = []
        for i in range(10):
            angle = math.pi / 2 + i * math.pi / 5
            r = size if i % 2 == 0 else size * 0.4
            points.append((cx + r * math.cos(angle), cy - r * math.sin(angle)))
        
        pygame.draw.polygon(surface, COLORS['star'], points)
        pygame.draw.polygon(surface, (0, 0, 0), points, 1)
    
    def _init_fonts(self):
        """Initialise les fonts au premier rendu."""
        if not self.font:
            pygame.font.init()
            self.font = pygame.font.Font(None, 24)
            self.font_small = pygame.font.Font(None, 18)
    
    def _ease_out(self, t: float) -> float:
        """Courbe d'accélération pour animation fluide."""
        return 1 - pow(1 - t, 3)
    
    def _ease_in(self, t: float) -> float:
        """Courbe de décélération pour animation fluide."""
        return t * t * t
    
    def has_pending(self) -> bool:
        """Retourne True si notification active ou en attente."""
        return self.current is not None or len(self.queue) > 0
    
    def clear(self):
        """Supprime toutes les notifications."""
        self.current = None
        self.queue.clear()
