"""
PlayerSelectScene - Player name and difficulty selection screen.

Features:
- Name input (max 10 characters, letters only)
- Difficulty choice (Easy/Normal/Hard) - hidden in Challenge mode
- "Let's go!" button (grayed out if name is empty)
- Back button (cross) and settings button (gear)
"""

import pygame
import os
from typing import List, Optional, Dict

from scenes.base_scene import BaseScene
from config import (
    IMAGES_DIR, FONTS_DIR, WINDOW_WIDTH, WINDOW_HEIGHT,
    Images, Layout, TextColors, FONT_FILE, FONT_SIZE
)
from core import lang_manager
from core.player_manager import PlayerManager
from ui.buttons import Button, ImageButton


class PlayerSelectScene(BaseScene):
    """Player and difficulty selection scene."""
    
    # Name: max 10 characters, letters only
    MAX_PSEUDO_LENGTH = 10
    
    def __init__(self, scene_manager):
        super().__init__(scene_manager)
        
        # Resources
        self.background = None
        self.font = None
        self.font_large = None
        
        # Specific images (not buttons)
        self.pseudo_field_img = None
        self.pseudo_field_rect = None
        self.difficulty_label_img = None
        
        # Buttons with effects
        self.btn_gear: Optional[ImageButton] = None
        self.btn_cross: Optional[ImageButton] = None
        self.btn_start: Optional[Button] = None
        self.difficulty_buttons: Dict[str, Button] = {}
        
        # State
        self.pseudo = ""
        self.selected_difficulty = "normal"  # easy, normal, hard
        self.is_challenge_mode = False
        
        # Text field state
        self.pseudo_field_focused = False
        self.cursor_visible = True
        self.cursor_timer = 0.0
        self.CURSOR_BLINK_RATE = 0.5  # Blink every 0.5 seconds
        
        # Player manager
        self.player_manager: Optional[PlayerManager] = None
    
    def setup(self):
        """Initializes the scene."""
        # Retrieve mode from shared_data
        self.is_challenge_mode = self.scene_manager.shared_data.get('mode') == 'challenge'
        
        # Reset name and difficulty
        self.pseudo = ""
        self.selected_difficulty = "normal"
        self.pseudo_field_focused = False
        self.cursor_visible = True
        self.cursor_timer = 0.0
        
        # Load resources
        self._load_resources()
    
    def _load_resources(self):
        """Loads images and fonts."""
        # Background
        self.background = pygame.image.load(
            os.path.join(IMAGES_DIR, Images.PSS_BG)
        ).convert()
        
        # Fonts
        font_path = os.path.join(FONTS_DIR, FONT_FILE)
        self.font = pygame.font.Font(font_path, FONT_SIZE)
        self.font_large = pygame.font.Font(font_path, 42)
        
        # Name field (not a button, just an image)
        self.pseudo_field_img = pygame.image.load(
            os.path.join(IMAGES_DIR, Images.PSS_PSEUDO_FIELD)
        ).convert_alpha()
        self.pseudo_field_rect = self.pseudo_field_img.get_rect(center=Layout.PSS_PSEUDO_FIELD)
        
        # Difficulty label
        self.difficulty_label_img = pygame.image.load(
            os.path.join(IMAGES_DIR, Images.PSS_DIFFICULTY_LABEL)
        ).convert_alpha()
        
        # Icon buttons (gear, cross)
        self.btn_gear = ImageButton(
            image_path=Images.PSS_GEAR,
            center=Layout.PSS_GEAR,
            on_click=self._on_settings
        )
        
        self.btn_cross = ImageButton(
            image_path=Images.PSS_CROSS,
            center=Layout.PSS_CROSS,
            on_click=self._on_back
        )
        
        # Start button
        self.btn_start = Button(
            image_path=Images.PSS_BTN_START,
            center=Layout.PSS_BTN_START,
            text=lang_manager.get("player_select.start_button"),
            text_color=TextColors.PSS_START,
            on_click=self._on_start,
            enabled=False  # Disabled by default (empty name)
        )
        
        # Difficulty buttons
        self.difficulty_buttons = {
            'easy': Button(
                image_path=Images.PSS_BTN_EASY,
                center=Layout.PSS_BTN_EASY,
                text=lang_manager.get("player_select.difficulty_easy"),
                text_color=TextColors.PSS_EASY,
                on_click=lambda: self._select_difficulty('easy')
            ),
            'normal': Button(
                image_path=Images.PSS_BTN_NORMAL,
                center=Layout.PSS_BTN_NORMAL,
                text=lang_manager.get("player_select.difficulty_normal"),
                text_color=TextColors.PSS_NORMAL,
                on_click=lambda: self._select_difficulty('normal')
            ),
            'hard': Button(
                image_path=Images.PSS_BTN_HARD,
                center=Layout.PSS_BTN_HARD,
                text=lang_manager.get("player_select.difficulty_hard"),
                text_color=TextColors.PSS_HARD,
                on_click=lambda: self._select_difficulty('hard')
            ),
        }
    
    def set_player_manager(self, manager: PlayerManager):
        """Sets the player manager."""
        self.player_manager = manager
    
    # Callbacks
    def _on_settings(self):
        self.scene_manager.change_scene('settings')
    
    def _on_back(self):
        self.scene_manager.change_scene('menu')
    
    def _on_start(self):
        if self.pseudo:
            self._start_game()
    
    def _select_difficulty(self, difficulty: str):
        self.selected_difficulty = difficulty
    
    def handle_events(self, events: List[pygame.event.Event]):
        for event in events:
            # Icon buttons
            self.btn_gear.handle_event(event)
            self.btn_cross.handle_event(event)
            
            # Start button
            self.btn_start.handle_event(event)
            
            # Difficulty buttons: no hover/click effects, just click detection
            if not self.is_challenge_mode:
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    for diff_key, btn in self.difficulty_buttons.items():
                        if btn.rect.collidepoint(event.pos):
                            self._select_difficulty(diff_key)
            
            # Name field handling
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Click on name field?
                if self.pseudo_field_rect.collidepoint(event.pos):
                    self.pseudo_field_focused = True
                    self.cursor_visible = True
                    self.cursor_timer = 0.0
                else:
                    self.pseudo_field_focused = False
            
            elif event.type == pygame.KEYDOWN:
                self._handle_key(event)
    
    def _handle_key(self, event: pygame.event.Event):
        """Handles keyboard input for the name."""
        if event.key == pygame.K_BACKSPACE:
            # Delete last character
            self.pseudo = self.pseudo[:-1]
        
        elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
            # Enter = start if name is valid
            if self.pseudo:
                self._start_game()
        
        elif event.key == pygame.K_ESCAPE:
            # Escape = back to menu
            self.scene_manager.change_scene('menu')
        
        else:
            # Add character (letters only)
            if len(self.pseudo) < self.MAX_PSEUDO_LENGTH:
                char = event.unicode
                if char.isalpha():
                    self.pseudo += char
        
        # Update start button state
        self.btn_start.set_enabled(bool(self.pseudo))
    
    def _start_game(self):
        """Starts the game."""
        # Save data to shared_data
        self.scene_manager.shared_data['pseudo'] = self.pseudo
        self.scene_manager.shared_data['difficulty'] = self.selected_difficulty
        
        # Check if new player (for tutorial)
        if self.player_manager:
            self.player_manager.set_current_player(self.pseudo)
            
            if self.player_manager.should_show_tutorial():
                self.scene_manager.change_scene('tutorial')
                return
        
        # Start game directly
        self.scene_manager.change_scene('game')
    
    def update(self, dt: float):
        """Updates the blinking cursor."""
        if self.pseudo_field_focused:
            self.cursor_timer += dt
            if self.cursor_timer >= self.CURSOR_BLINK_RATE:
                self.cursor_timer = 0.0
                self.cursor_visible = not self.cursor_visible
        
        # Update start button state based on name
        self.btn_start.set_enabled(bool(self.pseudo))
    
    def render(self, screen: pygame.Surface):
        """Renders the scene."""
        # Background
        screen.blit(self.background, (0, 0))
        
        # Icon buttons (gear and cross)
        self.btn_gear.render(screen)
        self.btn_cross.render(screen)
        
        # Name field
        self._render_pseudo_field(screen)
        
        # Difficulty section (only in classic mode)
        if not self.is_challenge_mode:
            self._render_difficulty_section(screen)
        
        # "Let's go!" button
        self.btn_start.render(screen, self.font)
    
    def _render_pseudo_field(self, screen: pygame.Surface):
        """Renders the name input field."""
        # Field background image
        screen.blit(self.pseudo_field_img, self.pseudo_field_rect)
        
        # Name text, cursor, or placeholder
        if self.pseudo:
            # Show name + cursor if focused
            text = self.pseudo
            if self.pseudo_field_focused and self.cursor_visible:
                text += "|"
            color = TextColors.PSS_PSEUDO
        elif self.pseudo_field_focused:
            # Focused but no text: show cursor only
            text = "|" if self.cursor_visible else ""
            color = TextColors.PSS_PSEUDO
        else:
            # Not focused, no text: placeholder
            text = lang_manager.get("player_select.pseudo_placeholder")
            color = (150, 150, 150)  # Gray for placeholder
        
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(center=self.pseudo_field_rect.center)
        screen.blit(text_surface, text_rect)
    
    def _render_difficulty_section(self, screen: pygame.Surface):
        """Renders the difficulty selection section."""
        # "Difficulty" label
        label_rect = self.difficulty_label_img.get_rect(center=Layout.PSS_DIFFICULTY_LABEL)
        screen.blit(self.difficulty_label_img, label_rect)
        
        difficulty_text = lang_manager.get("player_select.difficulty_label")
        text_surface = self.font.render(difficulty_text, True, TextColors.PSS_DIFFICULTY)
        text_rect = text_surface.get_rect(center=label_rect.center)
        screen.blit(text_surface, text_rect)
        
        # Difficulty buttons (no hover/click effects, just selection)
        for diff_key, btn in self.difficulty_buttons.items():
            if diff_key == self.selected_difficulty:
                # Selected button: normal render
                screen.blit(btn.image_original, btn.rect)
            else:
                # Unselected button: darkened
                darkened_img = btn.image_original.copy()
                darkened_img.fill((80, 80, 80), special_flags=pygame.BLEND_RGB_MULT)
                screen.blit(darkened_img, btn.rect)
            
            # Text
            text_surface = self.font.render(btn.text, True, btn.text_color)
            text_rect = text_surface.get_rect(center=btn.rect.center)
            screen.blit(text_surface, text_rect)
    
    def cleanup(self):
        """Cleanup on scene exit."""
        pass