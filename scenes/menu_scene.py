"""
MenuScene - Menu principal du jeu.
Affiche le fond et les 6 boutons de navigation.
"""

import pygame
import os
from typing import List

from scenes.base_scene import BaseScene
from config import IMAGES_DIR, FONTS_DIR, Images, Layout, TextColors, FONT_FILE, FONT_SIZE
from core import lang_manager


class Button:
    """Bouton cliquable avec image et texte."""
    
    def __init__(self, image_path: str, center: tuple, text: str, text_color: tuple):
        self.image = pygame.image.load(os.path.join(IMAGES_DIR, image_path)).convert_alpha()
        self.rect = self.image.get_rect(center=center)
        self.text = text
        self.text_color = text_color
    
    def is_clicked(self, pos: tuple) -> bool:
        return self.rect.collidepoint(pos)
    
    def render(self, screen: pygame.Surface, font: pygame.font.Font):
        screen.blit(self.image, self.rect)
        
        # Texte centré sur le bouton
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)


class MenuScene(BaseScene):
    """Scène du menu principal."""
    
    def __init__(self, scene_manager):
        super().__init__(scene_manager)
        self.background = None
        self.font = None
        self.buttons = {}
    
    def setup(self):
        """Charge les ressources du menu."""
        # Background
        bg_path = os.path.join(IMAGES_DIR, Images.MENU_BG)
        self.background = pygame.image.load(bg_path).convert()
        
        # Police
        font_path = os.path.join(FONTS_DIR, FONT_FILE)
        self.font = pygame.font.Font(font_path, FONT_SIZE)
        
        # Création des boutons
        self.buttons = {
            'jouer': Button(
                Images.BTN_JOUER,
                Layout.MENU_BTN_JOUER,
                lang_manager.get("menu.play_classic"),
                TextColors.BTN_JOUER
            ),
            'challenge': Button(
                Images.BTN_CHALLENGE,
                Layout.MENU_BTN_CHALLENGE,
                lang_manager.get("menu.play_challenge"),
                TextColors.BTN_CHALLENGE
            ),
            'classement': Button(
                Images.BTN_CLASSEMENT,
                Layout.MENU_BTN_CLASSEMENT,
                lang_manager.get("menu.leaderboard"),
                TextColors.BTN_CLASSEMENT
            ),
            'succes': Button(
                Images.BTN_SUCCES,
                Layout.MENU_BTN_SUCCES,
                lang_manager.get("menu.achievements"),
                TextColors.BTN_SUCCES
            ),
            'parametres': Button(
                Images.BTN_PARAMETRES,
                Layout.MENU_BTN_PARAMETRES,
                lang_manager.get("menu.settings"),
                TextColors.BTN_PARAMETRES
            ),
            'quitter': Button(
                Images.BTN_QUITTER,
                Layout.MENU_BTN_QUITTER,
                lang_manager.get("menu.quit"),
                TextColors.BTN_QUITTER
            ),
        }
    
    def handle_events(self, events: List[pygame.event.Event]):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._handle_click(event.pos)
    
    def _handle_click(self, pos: tuple):
        """Gère les clics sur les boutons."""
        if self.buttons['jouer'].is_clicked(pos):
            self.scene_manager.shared_data['mode'] = 'classic'
            self.scene_manager.change_scene('player_select')
        
        elif self.buttons['challenge'].is_clicked(pos):
            self.scene_manager.shared_data['mode'] = 'challenge'
            self.scene_manager.change_scene('player_select')
        
        elif self.buttons['classement'].is_clicked(pos):
            self.scene_manager.change_scene('ranking')
        
        elif self.buttons['succes'].is_clicked(pos):
            self.scene_manager.change_scene('success')
        
        elif self.buttons['parametres'].is_clicked(pos):
            self.scene_manager.change_scene('settings')
        
        elif self.buttons['quitter'].is_clicked(pos):
            self.scene_manager.quit_game()
    
    def update(self, dt: float):
        pass  # Pas d'animation pour l'instant
    
    def render(self, screen: pygame.Surface):
        # Fond
        screen.blit(self.background, (0, 0))
        
        # Boutons
        for button in self.buttons.values():
            button.render(screen, self.font)
