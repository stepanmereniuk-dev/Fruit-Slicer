"""
NotificationManager - Affiche les notifications de succès pendant le jeu.

Fonctionnalités :
- File d'attente (un succès à la fois)
- Affichage pendant 3 secondes
- Apparition instantanée, sortie en fondu
- Position en bas à gauche (342 x 1016)
"""

import pygame
import os
from typing import Optional
from collections import deque

from config import IMAGES_DIR, FONTS_DIR, FONT_FILE, TextColors


class NotificationManager:
    """
    Gère l'affichage des notifications de succès pendant le jeu.
    
    Utilisation :
        notif_manager = NotificationManager(mode='classic')
        
        # Dans update :
        notif_manager.add_notification("Glouton Vert")  # ou via Achievement
        notif_manager.update(dt)
        
        # Dans render :
        notif_manager.render(screen)
    """
    
    # Durées
    DISPLAY_DURATION = 3.0  # Durée totale d'affichage
    FADE_DURATION = 0.5     # Durée du fondu sortant (inclus dans DISPLAY_DURATION)
    
    # Police
    FONT_SIZE = 24
    
    # Assets selon le mode
    ASSET_CLASSIC = "scenes/game_scene/Bouton succes 544x80.png"
    ASSET_CHALLENGE = "scenes/challenge_scene/Bouton succes 544x80.png"
    
    # Positions fixes (specs)
    BUTTON_CENTER = (342, 1016)
    TEXT_LEFT = 170
    TEXT_CENTERY = 1016
    
    def __init__(self, mode: str = 'classic'):
        """
        Args:
            mode: 'classic' ou 'challenge' pour charger le bon asset
        """
        self.mode = mode
        
        # File d'attente des notifications (noms de succès)
        self.queue: deque = deque()
        
        # Notification actuellement affichée
        self.current_notification: Optional[str] = None
        self.display_timer = 0.0
        
        # Ressources
        self.background_img: Optional[pygame.Surface] = None
        self.font: Optional[pygame.font.Font] = None
        
        self._load_resources()
    
    def _load_resources(self):
        """Charge l'image de fond et la police."""
        # Image de fond selon le mode
        if self.mode == 'challenge':
            asset_path = self.ASSET_CHALLENGE
        else:
            asset_path = self.ASSET_CLASSIC
        
        full_path = os.path.join(IMAGES_DIR, asset_path)
        if os.path.exists(full_path):
            self.background_img = pygame.image.load(full_path).convert_alpha()
        else:
            print(f"Asset notification introuvable: {full_path}")
            self.background_img = None
        
        # Police
        font_path = os.path.join(FONTS_DIR, FONT_FILE)
        if os.path.exists(font_path):
            self.font = pygame.font.Font(font_path, self.FONT_SIZE)
        else:
            self.font = pygame.font.Font(None, self.FONT_SIZE)
    
    def set_mode(self, mode: str):
        """Change le mode et recharge l'asset correspondant."""
        if mode != self.mode:
            self.mode = mode
            self._load_resources()
    
    def add_notification(self, achievement_name: str):
        """
        Ajoute une notification à la file d'attente.
        
        Args:
            achievement_name: Nom du succès à afficher
        """
        self.queue.append(achievement_name)
        
        # Si aucune notification n'est affichée, démarrer immédiatement
        if self.current_notification is None:
            self._start_next_notification()
    
    def add_from_achievement(self, achievement):
        """
        Ajoute une notification depuis un objet Achievement.
        
        Args:
            achievement: Instance de Achievement avec propriété .name
        """
        self.add_notification(achievement.name)
    
    def _start_next_notification(self):
        """Démarre l'affichage de la prochaine notification dans la file."""
        if self.queue:
            self.current_notification = self.queue.popleft()
            self.display_timer = self.DISPLAY_DURATION
        else:
            self.current_notification = None
            self.display_timer = 0.0
    
    def update(self, dt: float):
        """
        Met à jour le timer et gère la transition entre notifications.
        
        Args:
            dt: Delta time en secondes
        """
        if self.current_notification is None:
            # Vérifier s'il y a des notifications en attente
            if self.queue:
                self._start_next_notification()
            return
        
        # Décrémenter le timer
        self.display_timer -= dt
        
        # Notification terminée ?
        if self.display_timer <= 0:
            self._start_next_notification()
    
    def render(self, screen: pygame.Surface):
        """
        Affiche la notification courante avec effet de fondu sortant.
        
        Args:
            screen: Surface Pygame sur laquelle dessiner
        """
        if self.current_notification is None:
            return
        
        if self.background_img is None or self.font is None:
            return
        
        # Calculer l'alpha pour le fondu sortant
        if self.display_timer <= self.FADE_DURATION:
            # Phase de fondu : alpha diminue de 255 à 0
            alpha = int(255 * (self.display_timer / self.FADE_DURATION))
            alpha = max(0, min(255, alpha))
        else:
            # Phase d'affichage normal : alpha = 255
            alpha = 255
        
        # Fond avec alpha
        bg_copy = self.background_img.copy()
        bg_copy.set_alpha(alpha)
        bg_rect = bg_copy.get_rect(center=self.BUTTON_CENTER)
        screen.blit(bg_copy, bg_rect)
        
        # Texte avec alpha
        text_surface = self.font.render(self.current_notification, True, TextColors.GAMEOVER_SUCCES)
        text_surface.set_alpha(alpha)
        text_rect = text_surface.get_rect(left=self.TEXT_LEFT, centery=self.TEXT_CENTERY)
        screen.blit(text_surface, text_rect)
    
    def clear(self):
        """Vide la file d'attente et arrête la notification courante."""
        self.queue.clear()
        self.current_notification = None
        self.display_timer = 0.0
    
    @property
    def is_active(self) -> bool:
        """Retourne True si une notification est en cours d'affichage."""
        return self.current_notification is not None
    
    @property
    def pending_count(self) -> int:
        """Retourne le nombre de notifications en attente (sans compter la courante)."""
        return len(self.queue)
