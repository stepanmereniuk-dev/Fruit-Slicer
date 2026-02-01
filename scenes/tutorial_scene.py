"""
TutorialScene - Tutorial screen for new players.

Classic Tutorial (6 screens):
1. Game objective
2. Controls
3. Hearts and strikes
4. Bombs
5. Ice flowers
6. Combos and bonus gauge

Challenge Tutorial (4 screens):
1. Game objective
2. Controls
3. Timer and bombs
4. Combos and bonus gauge
"""

import pygame
import os
from typing import List, Optional

from scenes.base_scene import BaseScene
from config import (
    IMAGES_DIR, FONTS_DIR, WINDOW_WIDTH, WINDOW_HEIGHT,
    Images, Layout, TextColors, FONT_FILE
)
from core import lang_manager
from core.player_manager import PlayerManager
from ui.buttons import Button


class TutorialScene(BaseScene):
    """Tutorial scene - adapted according to the mode (classic or challenge)."""
    
    # Font sizes
    TITLE_FONT_SIZE = 36
    TEXT_FONT_SIZE = 30
    BUTTON_FONT_SIZE = 30
    
    # Line height for 2-line texts
    LINE_HEIGHT = 1.4
    
    def __init__(self, scene_manager):
        super().__init__(scene_manager)
        
        # Resources
        self.background = None
        self.font_title = None
        self.font_text = None
        self.font_button = None
        
        # Block images
        self.blocks: List[pygame.Surface] = []
        
        # Buttons
        self.btn_prev: Optional[Button] = None
        self.btn_next: Optional[Button] = None
        self.btn_play: Optional[Button] = None
        
        # State
        self.mode = 'classic'  # 'classic' or 'challenge'
        self.current_screen = 0
        self.total_screens = 6
        
        # Player manager
        self.player_manager: Optional[PlayerManager] = None
    
    def setup(self):
        """Initializes the scene according to the mode."""
        # Retrieve the mode
        self.mode = self.scene_manager.shared_data.get('mode', 'classic')
        self.current_screen = 0
        
        # Number of screens depending on mode
        if self.mode == 'challenge':
            self.total_screens = 4
        else:
            self.total_screens = 6
        
        # Load resources
        self._load_resources()
        
        # Create buttons for the current screen
        self._setup_buttons()
    
    def _load_resources(self):
        """Loads images and fonts."""
        # Fonts
        font_path = os.path.join(FONTS_DIR, FONT_FILE)
        self.font_title = pygame.font.Font(font_path, self.TITLE_FONT_SIZE)
        self.font_text = pygame.font.Font(font_path, self.TEXT_FONT_SIZE)
        self.font_button = pygame.font.Font(font_path, self.BUTTON_FONT_SIZE)
        
        # Background (one per mode)
        if self.mode == 'challenge':
            bg_path = os.path.join(IMAGES_DIR, Images.TUTO_CHALLENGE_BG)
        else:
            bg_path = os.path.join(IMAGES_DIR, Images.TUTO_CLASSIC_BG)
        self.background = pygame.image.load(bg_path).convert()
        
        # Load all blocks
        self.blocks = []
        if self.mode == 'challenge':
            block_paths = Images.TUTO_CHALLENGE_BLOCKS
        else:
            block_paths = Images.TUTO_CLASSIC_BLOCKS
        
        for path in block_paths:
            img = pygame.image.load(os.path.join(IMAGES_DIR, path)).convert_alpha()
            self.blocks.append(img)
    
    def _setup_buttons(self):
        """Configures buttons for the current screen."""
        screen = self.current_screen
        
        # Retrieve paths according to mode
        if self.mode == 'challenge':
            prev_paths = Images.TUTO_CHALLENGE_BTN_PREV
            next_paths = Images.TUTO_CHALLENGE_BTN_NEXT
            play_path = Images.TUTO_CHALLENGE_BTN_PLAY
        else:
            prev_paths = Images.TUTO_CLASSIC_BTN_PREV
            next_paths = Images.TUTO_CLASSIC_BTN_NEXT
            play_path = Images.TUTO_CLASSIC_BTN_PLAY
        
        # Previous button (except screen 1)
        if prev_paths[screen] is not None:
            self.btn_prev = Button(
                image_path=prev_paths[screen],
                center=Layout.TUTO_BTN_PREV,
                text=lang_manager.get("tutorial.previous"),
                text_color=TextColors.TUTO_PREVIOUS,
                on_click=self._on_previous
            )
        else:
            self.btn_prev = None
        
        # Next button or Play button
        is_last_screen = screen == self.total_screens - 1
        
        if is_last_screen:
            # Last screen: Play button
            self.btn_next = None
            self.btn_play = Button(
                image_path=play_path,
                center=Layout.TUTO_BTN_PLAY,
                text=lang_manager.get("tutorial.play"),
                text_color=TextColors.TUTO_PLAY,
                on_click=self._on_play
            )
        else:
            # Other screens: Next button
            self.btn_play = None
            if next_paths[screen] is not None:
                self.btn_next = Button(
                    image_path=next_paths[screen],
                    center=Layout.TUTO_BTN_NEXT,
                    text=lang_manager.get("tutorial.next"),
                    text_color=TextColors.TUTO_NEXT,
                    on_click=self._on_next
                )
            else:
                self.btn_next = None
    
    def set_player_manager(self, manager: PlayerManager):
        """Sets the player manager."""
        self.player_manager = manager
    
    # Callbacks
    def _on_previous(self):
        """Previous screen."""
        if self.current_screen > 0:
            self.current_screen -= 1
            self._setup_buttons()
    
    def _on_next(self):
        """Next screen."""
        if self.current_screen < self.total_screens - 1:
            self.current_screen += 1
            self._setup_buttons()
    
    def _on_play(self):
        """Starts the game."""
        # Mark tutorial as seen
        if self.player_manager:
            self.player_manager.mark_tutorial_seen()
        
        # Start the game
        self.scene_manager.change_scene('game')
    
    def handle_events(self, events: List[pygame.event.Event]):
        for event in events:
            # Buttons
            if self.btn_prev:
                self.btn_prev.handle_event(event)
            if self.btn_next:
                self.btn_next.handle_event(event)
            if self.btn_play:
                self.btn_play.handle_event(event)
            
            # Keyboard shortcuts
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_BACKSPACE:
                    self._on_previous()
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_SPACE:
                    if self.current_screen < self.total_screens - 1:
                        self._on_next()
                    else:
                        self._on_play()
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    if self.current_screen == self.total_screens - 1:
                        self._on_play()
                    else:
                        self._on_next()
                elif event.key == pygame.K_ESCAPE:
                    # Back to menu (cancel tutorial)
                    self.scene_manager.change_scene('menu')
    
    def update(self, dt: float):
        pass
    
    def render(self, screen: pygame.Surface):
        """Renders the scene."""
        # Background
        screen.blit(self.background, (0, 0))
        
        # Central block
        block_img = self.blocks[self.current_screen]
        block_rect = block_img.get_rect(center=Layout.TUTO_BLOCK)
        screen.blit(block_img, block_rect)
        
        # Title
        self._render_title(screen)
        
        # Text
        self._render_text(screen)
        
        # Buttons
        if self.btn_prev:
            self.btn_prev.render(screen, self.font_button)
        if self.btn_next:
            self.btn_next.render(screen, self.font_button)
        if self.btn_play:
            self.btn_play.render(screen, self.font_button)
    
    def _render_title(self, screen: pygame.Surface):
        """Renders the screen title."""
        # Translation key according to mode and screen
        if self.mode == 'challenge':
            title_key = f"tutorial.challenge.screen{self.current_screen + 1}.title"
        else:
            title_key = f"tutorial.classic.screen{self.current_screen + 1}.title"
        
        title_text = lang_manager.get(title_key)
        title_surface = self.font_title.render(title_text, True, TextColors.TUTO_TITLE)
        title_rect = title_surface.get_rect(center=Layout.TUTO_TITLE)
        screen.blit(title_surface, title_rect)
    
    def _render_text(self, screen: pygame.Surface):
        """Renders the screen text (may span 2 lines)."""
        # Translation key
        if self.mode == 'challenge':
            text_key = f"tutorial.challenge.screen{self.current_screen + 1}.text"
        else:
            text_key = f"tutorial.classic.screen{self.current_screen + 1}.text"
        
        full_text = lang_manager.get(text_key)
        
        # Check if text contains a newline
        if "\n" in full_text:
            lines = full_text.split("\n")
            self._render_multiline_text(screen, lines)
        else:
            # Single line
            text_surface = self.font_text.render(full_text, True, TextColors.TUTO_TEXT)
            text_rect = text_surface.get_rect(center=Layout.TUTO_TEXT)
            screen.blit(text_surface, text_rect)
    
    def _render_multiline_text(self, screen: pygame.Surface, lines: List[str]):
        """Renders multiline text with line spacing."""
        line_height = int(self.TEXT_FONT_SIZE * self.LINE_HEIGHT)
        total_height = line_height * len(lines)
        
        # Starting position (vertically centered around TUTO_TEXT)
        start_y = Layout.TUTO_TEXT[1] - total_height // 2 + line_height // 2
        
        for i, line in enumerate(lines):
            text_surface = self.font_text.render(line.strip(), True, TextColors.TUTO_TEXT)
            text_rect = text_surface.get_rect(
                centerx=Layout.TUTO_TEXT[0],
                centery=start_y + i * line_height
            )
            screen.blit(text_surface, text_rect)
    
    def cleanup(self):
        """Cleanup on scene exit."""
        pass
