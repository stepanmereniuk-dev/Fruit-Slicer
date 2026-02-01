"""
Buttons - Composants de boutons réutilisables avec effets hover et clic.

Effets :
- Hover : Éclaircissement du bouton
- Clic : Assombrissement + légère réduction de taille
"""

import pygame
import os
from typing import Optional, Callable, Tuple

from config import IMAGES_DIR, FONTS_DIR, FONT_FILE, FONT_SIZE


class Button:
    """
    Bouton cliquable avec effets visuels.
    
    Utilisation :
        btn = Button(
            image_path="scenes/menu_scene/bouton jouer 458x89.png",
            center=(960, 624),
            text="Jouer",
            text_color=(254, 237, 142),
            on_click=lambda: scene_manager.change_scene('game')
        )
        
        # Dans handle_events :
        btn.handle_event(event)
        
        # Dans render :
        btn.render(screen, font)
    """
    
    # Facteurs d'effet
    HOVER_BRIGHTEN = (20, 20, 20)  # Ajout RGB pour éclaircir (léger)
    CLICK_DARKEN = (180, 180, 180)  # Multiplication RGB pour assombrir (léger)
    CLICK_SCALE = 0.97             # Réduction de taille au clic (subtile)
    
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
            image_path: Chemin relatif depuis IMAGES_DIR
            center: Position du centre du bouton
            text: Texte à afficher sur le bouton
            text_color: Couleur du texte
            font: Police (si None, sera définie lors du render)
            on_click: Fonction appelée lors du clic
            enabled: Si False, le bouton est grisé et non cliquable
        """
        self.center = center
        self.text = text
        self.text_color = text_color
        self.on_click = on_click
        self.enabled = enabled
        
        # Charger l'image originale
        self.image_original = pygame.image.load(
            os.path.join(IMAGES_DIR, image_path)
        ).convert_alpha()
        
        # Créer les versions avec effets
        self._create_effect_images()
        
        # Rectangle de collision (basé sur l'image originale)
        self.rect = self.image_original.get_rect(center=center)
        
        # États
        self.is_hovered = False
        self.is_pressed = False
        
        # Police
        self.font = font
    
    def _create_effect_images(self):
        """Crée les versions hover et clic de l'image."""
        # Version hover (éclaircie)
        self.image_hover = self.image_original.copy()
        self.image_hover.fill(self.HOVER_BRIGHTEN, special_flags=pygame.BLEND_RGB_ADD)
        
        # Version clic (assombrie + réduite)
        darkened = self.image_original.copy()
        darkened.fill(self.CLICK_DARKEN, special_flags=pygame.BLEND_RGB_MULT)
        
        # Réduire la taille
        original_size = self.image_original.get_size()
        new_size = (
            int(original_size[0] * self.CLICK_SCALE),
            int(original_size[1] * self.CLICK_SCALE)
        )
        self.image_click = pygame.transform.smoothscale(darkened, new_size)
        
        # Version désactivée (assombrie)
        self.image_disabled = self.image_original.copy()
        self.image_disabled.fill(self.CLICK_DARKEN, special_flags=pygame.BLEND_RGB_MULT)
    
    def set_text(self, text: str):
        """Change le texte du bouton."""
        self.text = text
    
    def set_enabled(self, enabled: bool):
        """Active ou désactive le bouton."""
        self.enabled = enabled
        if not enabled:
            self.is_hovered = False
            self.is_pressed = False
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Gère un événement pygame.
        Retourne True si le bouton a été cliqué.
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
        """Met à jour l'état hover selon la position de la souris."""
        if self.enabled:
            self.is_hovered = self.rect.collidepoint(mouse_pos)
    
    def render(self, screen: pygame.Surface, font: Optional[pygame.font.Font] = None):
        """Affiche le bouton avec l'effet approprié."""
        # Utiliser la police fournie ou celle stockée
        render_font = font or self.font
        
        # Sélectionner l'image selon l'état
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
        
        # Afficher l'image
        screen.blit(image, image_rect)
        
        # Afficher le texte
        if self.text and render_font:
            text_surface = render_font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=image_rect.center)
            screen.blit(text_surface, text_rect)


class ImageButton:
    """
    Bouton image simple sans texte (pour les icônes comme engrenage, croix).
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
        
        # Charger l'image
        self.image_original = pygame.image.load(
            os.path.join(IMAGES_DIR, image_path)
        ).convert_alpha()
        
        # Créer les versions avec effets
        self._create_effect_images()
        
        # Rectangle
        self.rect = self.image_original.get_rect(center=center)
        
        # États
        self.is_hovered = False
        self.is_pressed = False
    
    def _create_effect_images(self):
        """Crée les versions hover et clic."""
        # Hover
        self.image_hover = self.image_original.copy()
        self.image_hover.fill(self.HOVER_BRIGHTEN, special_flags=pygame.BLEND_RGB_ADD)
        
        # Clic
        darkened = self.image_original.copy()
        darkened.fill(self.CLICK_DARKEN, special_flags=pygame.BLEND_RGB_MULT)
        original_size = self.image_original.get_size()
        new_size = (
            int(original_size[0] * self.CLICK_SCALE),
            int(original_size[1] * self.CLICK_SCALE)
        )
        self.image_click = pygame.transform.smoothscale(darkened, new_size)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Gère un événement. Retourne True si cliqué."""
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
        """Affiche le bouton."""
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
