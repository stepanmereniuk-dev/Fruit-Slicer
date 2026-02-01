"""
GameOverScene - Game over screen.

3 variants depending on context:
- Explosion: sliced bomb (classic mode)
- K.O: 3 hearts lost (classic mode)
- Time elapsed: timer end (challenge mode)
"""

import pygame
import os
from typing import List, Optional

from scenes.base_scene import BaseScene
from config import (
    IMAGES_DIR, FONTS_DIR, WINDOW_WIDTH, WINDOW_HEIGHT,
    Images, Layout, TextColors, FONT_FILE, FONT_SIZE
)
from core import lang_manager
from ui.buttons import Button


class GameOverScene(BaseScene):
    """Game over scene."""
    
    # Font sizes
    SCORE_FONT_SIZE = 30
    RECORD_FONT_SIZE = 36
    
    def __init__(self, scene_manager):
        super().__init__(scene_manager)
        
        # Resources
        self.background = None
        self.font_score = None
        self.font_record = None
        self.font_button = None
        
        # Buttons
        self.btn_rejouer: Optional[Button] = None
        self.btn_menu: Optional[Button] = None
        
        # State
        self.game_over_type = 'ko'  # 'explosion', 'ko', 'elapsed_time'
        self.final_score = 0
        self.best_score = 0
        self.is_new_record = False
    
    def setup(self):
        """Initializes the scene according to the game over type."""
        # Retrieve data from shared_data
        self.final_score = self.scene_manager.shared_data.get('last_score', 0)
        self.is_new_record = self.scene_manager.shared_data.get('is_new_record', False)
        exploded = self.scene_manager.shared_data.get('exploded', False)
        mode = self.scene_manager.shared_data.get('mode', 'classic')
        
        # Determine game over type
        if mode == 'challenge':
            self.game_over_type = 'elapsed_time'
        elif exploded:
            self.game_over_type = 'explosion'
        else:
            self.game_over_type = 'ko'
        
        # Retrieve best score
        self._load_best_score()
        
        # Load resources
        self._load_resources()
    
    def _load_best_score(self):
        """Loads the player's best score for this mode/difficulty."""
        player_manager = self.scene_manager.player_manager
        mode = self.scene_manager.shared_data.get('mode', 'classic')
        difficulty = self.scene_manager.shared_data.get('difficulty', 'normal')
        
        if player_manager and player_manager.current_player:
            category = player_manager.get_category_key(mode, difficulty)
            self.best_score = player_manager.get_high_score(category)
            
            # Check and update record
            if self.final_score > self.best_score:
                self.is_new_record = True
                player_manager.update_high_score(category, self.final_score)
                self.best_score = self.final_score
    
    def _load_resources(self):
        """Loads images and fonts according to game over type."""
        # Fonts
        font_path = os.path.join(FONTS_DIR, FONT_FILE)
        self.font_score = pygame.font.Font(font_path, self.SCORE_FONT_SIZE)
        self.font_record = pygame.font.Font(font_path, self.RECORD_FONT_SIZE)
        self.font_button = pygame.font.Font(font_path, FONT_SIZE)
        
        # Load background and buttons according to type
        if self.game_over_type == 'explosion':
            bg_path = Images.GAMEOVER_EXPLOSION_BG
            btn_rejouer_path = Images.GAMEOVER_EXPLOSION_BTN_REJOUER
            btn_menu_path = Images.GAMEOVER_EXPLOSION_BTN_MENU
        elif self.game_over_type == 'elapsed_time':
            bg_path = Images.GAMEOVER_TIME_BG
            btn_rejouer_path = Images.GAMEOVER_TIME_BTN_REJOUER
            btn_menu_path = Images.GAMEOVER_TIME_BTN_MENU
        else:  # ko
            bg_path = Images.GAMEOVER_KO_BG
            btn_rejouer_path = Images.GAMEOVER_KO_BTN_REJOUER
            btn_menu_path = Images.GAMEOVER_KO_BTN_MENU
        
        # Background
        self.background = pygame.image.load(
            os.path.join(IMAGES_DIR, bg_path)
        ).convert()
        
        # Buttons
        self.btn_rejouer = Button(
            image_path=btn_rejouer_path,
            center=Layout.GAMEOVER_BTN_REJOUER,
            text=lang_manager.get("game_over.retry_button"),
            text_color=TextColors.GAMEOVER_BTN_REJOUER,
            on_click=self._on_rejouer
        )
        
        self.btn_menu = Button(
            image_path=btn_menu_path,
            center=Layout.GAMEOVER_BTN_MENU,
            text=lang_manager.get("game_over.menu_button"),
            text_color=TextColors.GAMEOVER_BTN_MENU,
            on_click=self._on_menu
        )
    
    # Callbacks
    def _on_rejouer(self):
        """Restarts a game with the same parameters."""
        self.scene_manager.change_scene('game')
    
    def _on_menu(self):
        """Returns to the main menu."""
        self.scene_manager.change_scene('menu')
    
    def handle_events(self, events: List[pygame.event.Event]):
        for event in events:
            # Buttons
            self.btn_rejouer.handle_event(event)
            self.btn_menu.handle_event(event)
            
            # Keyboard shortcuts
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    self._on_rejouer()
                elif event.key == pygame.K_ESCAPE:
                    self._on_menu()
    
    def update(self, dt: float):
        pass
    
    def render(self, screen: pygame.Surface):
        """Renders the scene."""
        # Background
        screen.blit(self.background, (0, 0))
        
        # Final score
        self._render_score(screen)
        
        # Best score
        self._render_best_score(screen)
        
        # New record (if applicable)
        if self.is_new_record:
            self._render_new_record(screen)
        
        # Buttons
        self.btn_rejouer.render(screen, self.font_button)
        self.btn_menu.render(screen, self.font_button)
    
    def _render_score(self, screen: pygame.Surface):
        """Renders the final score."""
        label = lang_manager.get("game_over.score_label")
        score_text = f"{label} : {self.final_score}"
        score_surface = self.font_score.render(score_text, True, TextColors.GAMEOVER_SCORE)
        score_rect = score_surface.get_rect(
            left=Layout.GAMEOVER_SCORE_FINAL[0],
            centery=Layout.GAMEOVER_SCORE_FINAL[1]
        )
        screen.blit(score_surface, score_rect)
    
    def _render_best_score(self, screen: pygame.Surface):
        """Renders the best score."""
        label = lang_manager.get("game_over.best_score_label")
        best_text = f"{label} : {self.best_score}"
        best_surface = self.font_score.render(best_text, True, TextColors.GAMEOVER_SCORE)
        best_rect = best_surface.get_rect(
            left=Layout.GAMEOVER_BEST_SCORE[0],
            centery=Layout.GAMEOVER_BEST_SCORE[1]
        )
        screen.blit(best_surface, best_rect)
    
    def _render_new_record(self, screen: pygame.Surface):
        """Renders the 'New record!' text."""
        record_text = lang_manager.get("game_over.new_record")
        record_surface = self.font_record.render(record_text, True, TextColors.GAMEOVER_NEW_RECORD)
        record_rect = record_surface.get_rect(center=Layout.GAMEOVER_NEW_RECORD)
        screen.blit(record_surface, record_rect)
    
    def cleanup(self):
        """Cleanup on scene exit."""
        pass
