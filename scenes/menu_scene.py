"""
MenuScene - Menu principal du jeu.
Affiche le fond et les 6 boutons de navigation.
"""

import pygame
import os
from typing import List, Dict

from scenes.base_scene import BaseScene
from config import IMAGES_DIR, FONTS_DIR, Images, Layout, TextColors, FONT_FILE, FONT_SIZE
from core import lang_manager
from ui.buttons import Button


class MenuScene(BaseScene):
    """Scène du menu principal."""
    
    def __init__(self, scene_manager):
        super().__init__(scene_manager)
        self.background = None
        self.font = None
        self.buttons: Dict[str, Button] = {}
    
    def setup(self):
        """Charge les ressources du menu."""
        # Background
        bg_path = os.path.join(IMAGES_DIR, Images.MENU_BG)
        self.background = pygame.image.load(bg_path).convert()
        
        # Police
        font_path = os.path.join(FONTS_DIR, FONT_FILE)
        self.font = pygame.font.Font(font_path, FONT_SIZE)
        
        # Création des boutons avec callbacks
        self.buttons = {
            'jouer': Button(
                image_path=Images.BTN_JOUER,
                center=Layout.MENU_BTN_JOUER,
                text=lang_manager.get("menu.play_classic"),
                text_color=TextColors.BTN_JOUER,
                on_click=self._on_play_classic
            ),
            'challenge': Button(
                image_path=Images.BTN_CHALLENGE,
                center=Layout.MENU_BTN_CHALLENGE,
                text=lang_manager.get("menu.play_challenge"),
                text_color=TextColors.BTN_CHALLENGE,
                on_click=self._on_play_challenge
            ),
            'classement': Button(
                image_path=Images.BTN_CLASSEMENT,
                center=Layout.MENU_BTN_CLASSEMENT,
                text=lang_manager.get("menu.leaderboard"),
                text_color=TextColors.BTN_CLASSEMENT,
                on_click=self._on_leaderboard
            ),
            'succes': Button(
                image_path=Images.BTN_SUCCES,
                center=Layout.MENU_BTN_SUCCES,
                text=lang_manager.get("menu.achievements"),
                text_color=TextColors.BTN_SUCCES,
                on_click=self._on_achievements
            ),
            'parametres': Button(
                image_path=Images.BTN_PARAMETRES,
                center=Layout.MENU_BTN_PARAMETRES,
                text=lang_manager.get("menu.settings"),
                text_color=TextColors.BTN_PARAMETRES,
                on_click=self._on_settings
            ),
            'quitter': Button(
                image_path=Images.BTN_QUITTER,
                center=Layout.MENU_BTN_QUITTER,
                text=lang_manager.get("menu.quit"),
                text_color=TextColors.BTN_QUITTER,
                on_click=self._on_quit
            ),
        }
    
    # Callbacks des boutons
    def _on_play_classic(self):
        self.scene_manager.shared_data['mode'] = 'classic'
        self.scene_manager.change_scene('player_select')
    
    def _on_play_challenge(self):
        self.scene_manager.shared_data['mode'] = 'challenge'
        self.scene_manager.change_scene('player_select')
    
    def _on_leaderboard(self):
        self.scene_manager.change_scene('ranking')
    
    def _on_achievements(self):
        self.scene_manager.change_scene('success')
    
    def _on_settings(self):
        self.scene_manager.change_scene('settings')
    
    def _on_quit(self):
        self.scene_manager.quit_game()
    
    def handle_events(self, events: List[pygame.event.Event]):
        for event in events:
            # Transmettre les événements aux boutons
            for button in self.buttons.values():
                button.handle_event(event)
    
    def update(self, dt: float):
        pass
    
    def render(self, screen: pygame.Surface):
        # Fond
        screen.blit(self.background, (0, 0))
        
        # Boutons
        for button in self.buttons.values():
            button.render(screen, self.font)
