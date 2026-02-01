"""
Buttons - Reusable button components with hover and click effects.

Effects:
- Hover: Brightening the button
- Click: Darkening + slight size reduction
"""

import pygame
import os
from typing import Optional, Callable, Tuple

from config import IMAGES_DIR, FONTS_DIR, FONT_FILE, FONT_SIZE


class Button:
    """
    Clickable button with visual effects.
    
    Usage:
        btn = Button(
            image_path="scenes/menu_scene/bouton jouer 458x89.png",
            center=(960, 624),
            text="Jouer",
            text_color=(254, 237, 142),
            on_click=lambda: scene_manager.change_scene('game')
        )
        
        # In handle_events:
        btn.handle_event(event)
        
        # In render:
        btn.render(screen, font)
    """
    
    # Effect factors
    HOVER_BRIGHTEN = (20, 20, 20)  # RGB add for lightening (subtle)
    CLICK_DARKEN = (180, 180, 180)  # RGB multiply for darkening (subtle)
    CLICK_SCALE = 0.97             # Size reduction on click (subtle)
    
    def __init__(
        self,
        image_path: str,
        center: Tuple[int, int],
        text: str = "",
        text_color: Tuple[int, int, int] = (255, 255, 255),
        font: Optional[pygame.font.Font] = None,
        on_click: Optional[Callable] = None,
        enabled: bool = True
    ):
        """
        Args:
            image_path: Relative path from IMAGES_DIR
            center: Button center position
            text: Text to display on the button
            text_color: Text color
            font: Font (if None, will be set during render)
            on_click: Function called on click
            enabled: If False, the button is grayed out and not clickable
        """
        self.center = center
        self.text = text
        self.text_color = text_color
        self.on_click = on_click
        self.enabled = enabled
        
        # Load original image
        self.image_original = pygame.image.load(
            os.path.join(IMAGES_DIR, image_path)
        ).convert_alpha()
        
        # Create effect versions
        self._create_effect_images()
        
        # Collision rectangle (based on original image)
        self.rect = self.image_original.get_rect(center=center)
        
        # States
        self.is_hovered = False
        self.is_pressed = False
        
        # Font
        self.font = font
    
    def _create_effect_images(self):
        """Creates hover and click versions of the image."""
        # Hover version (brightened)
        self.image_hover = self.image_original.copy()
        self.image_hover.fill(self.HOVER_BRIGHTEN, special_flags=pygame.BLEND_RGB_ADD)
        
        # Click version (darkened + scaled)
        darkened = self.image_original.copy()
        darkened.fill(self.CLICK_DARKEN, special_flags=pygame.BLEND_RGB_MULT)
        
        # Scale down
        original_size = self.image_original.get_size()
        new_size = (
            int(original_size[0] * self.CLICK_SCALE),
            int(original_size[1] * self.CLICK_SCALE)
        )
        self.image_click = pygame.transform.smoothscale(darkened, new_size)
        
        # Disabled version (darkened)
        self.image_disabled = self.image_original.copy()
        self.image_disabled.fill(self.CLICK_DARKEN, special_flags=pygame.BLEND_RGB_MULT)
    
    def set_text(self, text: str):
        """Changes the button text."""
        self.text = text
    
    def set_enabled(self, enabled: bool):
        """Enables or disables the button."""
        self.enabled = enabled
        if not enabled:
            self.is_hovered = False
            self.is_pressed = False
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handles a pygame event.
        Returns True if the button was clicked.
        """
        if not self.enabled:
            return False
        
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
            if not self.is_hovered:
                self.is_pressed = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_pressed = True
        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_pressed and self.rect.collidepoint(event.pos):
                self.is_pressed = False
                if self.on_click:
                    self.on_click()
                return True
            self.is_pressed = False
        
        return False
    
    def update_hover(self, mouse_pos: Tuple[int, int]):
        """Updates hover state based on mouse position."""
        if self.enabled:
            self.is_hovered = self.rect.collidepoint(mouse_pos)
    
    def render(self, screen: pygame.Surface, font: Optional[pygame.font.Font] = None):
        """Renders the button with the appropriate effect."""
        # Use provided font or stored one
        render_font = font or self.font
        
        # Select image based on state
        if not self.enabled:
            image = self.image_disabled
            image_rect = image.get_rect(center=self.center)
        elif self.is_pressed:
            image = self.image_click
            image_rect = image.get_rect(center=self.center)
        elif self.is_hovered:
            image = self.image_hover
            image_rect = image.get_rect(center=self.center)
        else:
            image = self.image_original
            image_rect = self.rect
        
        # Draw image
        screen.blit(image, image_rect)
        
        # Draw text
        if self.text and render_font:
            text_surface = render_font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=image_rect.center)
            screen.blit(text_surface, text_rect)


class ImageButton:
    """
    Simple image button without text (for icons like gear, cross).
    """
    
    HOVER_BRIGHTEN = (20, 20, 20)
    CLICK_DARKEN = (180, 180, 180)
    CLICK_SCALE = 0.97
    
    def __init__(
        self,
        image_path: str,
        center: Tuple[int, int],
        on_click: Optional[Callable] = None
    ):
        self.center = center
        self.on_click = on_click
        
        # Load image
        self.image_original = pygame.image.load(
            os.path.join(IMAGES_DIR, image_path)
        ).convert_alpha()
        
        # Create effect versions
        self._create_effect_images()
        
        # Rectangle
        self.rect = self.image_original.get_rect(center=center)
        
        # States
        self.is_hovered = False
        self.is_pressed = False
    
    def _create_effect_images(self):
        """Creates hover and click versions."""
        # Hover
        self.image_hover = self.image_original.copy()
        self.image_hover.fill(self.HOVER_BRIGHTEN, special_flags=pygame.BLEND_RGB_ADD)
        
        # Click
        darkened = self.image_original.copy()
        darkened.fill(self.CLICK_DARKEN, special_flags=pygame.BLEND_RGB_MULT)
        original_size = self.image_original.get_size()
        new_size = (
            int(original_size[0] * self.CLICK_SCALE),
            int(original_size[1] * self.CLICK_SCALE)
        )
        self.image_click = pygame.transform.smoothscale(darkened, new_size)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handles an event. Returns True if clicked."""
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
            if not self.is_hovered:
                self.is_pressed = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_pressed = True
        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_pressed and self.rect.collidepoint(event.pos):
                self.is_pressed = False
                if self.on_click:
                    self.on_click()
                return True
            self.is_pressed = False
        
        return False
    
    def render(self, screen: pygame.Surface):
        """Renders the button."""
        if self.is_pressed:
            image = self.image_click
            rect = image.get_rect(center=self.center)
        elif self.is_hovered:
            image = self.image_hover
            rect = self.rect
        else:
            image = self.image_original
            rect = self.rect
        
        screen.blit(image, rect)
        