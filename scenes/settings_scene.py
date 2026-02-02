"""
SettingsScene - Écran des paramètres du jeu.

Contenu :
- Mode de contrôle : Clavier / Souris
- Volume musique : Slider 0% à 100%
- Volume effets sonores : Slider 0% à 100%
- Langue : Français / Anglais
- Revoir le tutoriel

Les paramètres sont globaux (pas liés au pseudo).
"""

import pygame
import os
from typing import List, Optional, Tuple

from scenes.base_scene import BaseScene
from config import (
    IMAGES_DIR, FONTS_DIR, WINDOW_WIDTH, WINDOW_HEIGHT,
    Images, Layout, TextColors, FONT_FILE, ControlMode
)
from core import lang_manager
from core import settings_manager
from ui.buttons import ImageButton


class SettingsScene(BaseScene):
    """Scène des paramètres."""
    
    # Tailles de police selon les specs
    LABEL_FONT_SIZE = 30       # mode controle, volume musique, volume sonore, langue
    PARAM_FONT_SIZE = 36       # "paramètre" (titre)
    CONTROL_FONT_SIZE = 25     # clavier, souris
    TUTORIAL_FONT_SIZE = 30    # revoir le tutoriel
    VOLUME_FONT_SIZE = 25      # 0%, 100%
    LANG_FONT_SIZE = 25        # Français, Anglais
    INFO_FONT_SIZE = 30        # "Les paramètres sont globaux"
    
    def __init__(self, scene_manager):
        super().__init__(scene_manager)
        
        # Ressources
        self.background = None
        self.block_params = None
        
        # Polices
        self.font_label = None
        self.font_param = None
        self.font_control = None
        self.font_tutorial = None
        self.font_volume = None
        self.font_lang = None
        self.font_info = None
        
        # Boutons mode de contrôle
        self.btn_clavier_img = None
        self.btn_souris_img = None
        self.btn_clavier_rect = None
        self.btn_souris_rect = None
        
        # Boutons langue
        self.btn_francais_img = None
        self.btn_anglais_img = None
        self.btn_francais_rect = None
        self.btn_anglais_rect = None
        
        # Bouton tutoriel
        self.btn_tutorial_img = None
        self.btn_tutorial_rect = None
        
        # Boutons navigation
        self.btn_gear: Optional[ImageButton] = None
        self.btn_cross: Optional[ImageButton] = None
        
        # États hover/clic
        self.hovered_element: Optional[str] = None
        self.clicked_element: Optional[str] = None
        
        # Sliders
        self.music_slider_rect = None
        self.sfx_slider_rect = None
        self.dragging_slider: Optional[str] = None  # 'music' ou 'sfx'
        
        # Settings manager
        self.settings = None
    
    def setup(self):
        """Initialise la scène."""
        self.settings = settings_manager.get_instance()
        self._load_resources()
        self.hovered_element = None
        self.clicked_element = None
        self.dragging_slider = None
    
    def _load_resources(self):
        """Charge les images et polices."""
        # Polices
        font_path = os.path.join(FONTS_DIR, FONT_FILE)
        self.font_label = pygame.font.Font(font_path, self.LABEL_FONT_SIZE)
        self.font_param = pygame.font.Font(font_path, self.PARAM_FONT_SIZE)
        self.font_control = pygame.font.Font(font_path, self.CONTROL_FONT_SIZE)
        self.font_tutorial = pygame.font.Font(font_path, self.TUTORIAL_FONT_SIZE)
        self.font_volume = pygame.font.Font(font_path, self.VOLUME_FONT_SIZE)
        self.font_lang = pygame.font.Font(font_path, self.LANG_FONT_SIZE)
        self.font_info = pygame.font.Font(font_path, self.INFO_FONT_SIZE)
        
        # Background
        self.background = pygame.image.load(
            os.path.join(IMAGES_DIR, Images.SETTINGS_BG)
        ).convert()
        
        # Bloc paramètres
        self.block_params = pygame.image.load(
            os.path.join(IMAGES_DIR, Images.SETTINGS_BLOCK_PARAMS)
        ).convert_alpha()
        
        # Boutons mode de contrôle
        self.btn_clavier_img = pygame.image.load(
            os.path.join(IMAGES_DIR, Images.SETTINGS_BTN_CLAVIER)
        ).convert_alpha()
        self.btn_clavier_rect = self.btn_clavier_img.get_rect(center=Layout.SETTINGS_BTN_CLAVIER)
        
        self.btn_souris_img = pygame.image.load(
            os.path.join(IMAGES_DIR, Images.SETTINGS_BTN_SOURIS)
        ).convert_alpha()
        self.btn_souris_rect = self.btn_souris_img.get_rect(center=Layout.SETTINGS_BTN_SOURIS)
        
        # Boutons langue
        self.btn_francais_img = pygame.image.load(
            os.path.join(IMAGES_DIR, Images.SETTINGS_BTN_FRANCAIS)
        ).convert_alpha()
        self.btn_francais_rect = self.btn_francais_img.get_rect(center=Layout.SETTINGS_BTN_FRANCAIS)
        
        self.btn_anglais_img = pygame.image.load(
            os.path.join(IMAGES_DIR, Images.SETTINGS_BTN_ANGLAIS)
        ).convert_alpha()
        self.btn_anglais_rect = self.btn_anglais_img.get_rect(center=Layout.SETTINGS_BTN_ANGLAIS)
        
        # Bouton tutoriel
        self.btn_tutorial_img = pygame.image.load(
            os.path.join(IMAGES_DIR, Images.SETTINGS_BTN_TUTORIAL)
        ).convert_alpha()
        self.btn_tutorial_rect = self.btn_tutorial_img.get_rect(center=Layout.SETTINGS_BTN_TUTORIAL)
        
        # Boutons navigation (engrenage et croix)
        self.btn_gear = ImageButton(
            image_path=Images.SETTINGS_GEAR,
            center=Layout.SETTINGS_GEAR,
            on_click=None  # Déjà sur la page settings
        )
        
        self.btn_cross = ImageButton(
            image_path=Images.SETTINGS_CROSS,
            center=Layout.SETTINGS_CROSS,
            on_click=self._on_back
        )
        
        # Définir les rectangles des sliders (basés sur les specs de jauge 540x22)
        self.music_slider_rect = pygame.Rect(0, 0, 540, 22)
        self.music_slider_rect.center = Layout.SETTINGS_GAUGE_MUSIC
        
        self.sfx_slider_rect = pygame.Rect(0, 0, 540, 22)
        self.sfx_slider_rect.center = Layout.SETTINGS_GAUGE_SFX
    
    # Callbacks
    def _on_back(self):
        """Retourne à la scène précédente."""
        self.scene_manager.change_scene('menu')
    
    def _on_clavier(self):
        """Sélectionne le mode clavier."""
        if self.settings:
            old_mode = self.settings.control_mode
            self.settings.set_control_mode(ControlMode.KEYBOARD)
            if old_mode != ControlMode.KEYBOARD:
                # Notifier le changement pour le succès "indécis"
                if self.scene_manager.achievement_manager:
                    self.scene_manager.achievement_manager.on_mode_switch()
            # Mettre à jour shared_data
            self.scene_manager.shared_data['control_mode'] = ControlMode.KEYBOARD
    
    def _on_souris(self):
        """Sélectionne le mode souris."""
        if self.settings:
            old_mode = self.settings.control_mode
            self.settings.set_control_mode(ControlMode.MOUSE)
            if old_mode != ControlMode.MOUSE:
                # Notifier le changement pour le succès "indécis"
                if self.scene_manager.achievement_manager:
                    self.scene_manager.achievement_manager.on_mode_switch()
            # Mettre à jour shared_data
            self.scene_manager.shared_data['control_mode'] = ControlMode.MOUSE
    
    def _on_francais(self):
        """Sélectionne le français."""
        if self.settings:
            self.settings.set_language('fr')
    
    def _on_anglais(self):
        """Sélectionne l'anglais."""
        if self.settings:
            self.settings.set_language('en')
    
    def _on_tutorial(self):
        """Relance le tutoriel."""
        # Marquer le tutoriel comme non vu pour le joueur courant
        if self.scene_manager.player_manager and self.scene_manager.player_manager.current_player:
            self.scene_manager.player_manager.current_player.tutorial_seen = False
            self.scene_manager.player_manager.save()
        
        # Indiquer qu'on vient des paramètres
        self.scene_manager.shared_data['tutorial_from_settings'] = True
        
        # Aller à la scène tutoriel
        self.scene_manager.change_scene('tutorial')
    
    def handle_events(self, events: List[pygame.event.Event]):
        for event in events:
            # Bouton croix (retour)
            self.btn_cross.handle_event(event)
            
            if event.type == pygame.MOUSEMOTION:
                self._handle_mouse_motion(event.pos)
                
                # Gestion du drag des sliders
                if self.dragging_slider:
                    self._update_slider_from_mouse(event.pos)
            
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._handle_mouse_down(event.pos)
            
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self._handle_mouse_up(event.pos)
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._on_back()
    
    def _handle_mouse_motion(self, pos: Tuple[int, int]):
        """Gère le survol de la souris."""
        self.hovered_element = None
        
        # Boutons mode de contrôle
        if self.btn_clavier_rect.collidepoint(pos):
            self.hovered_element = 'clavier'
        elif self.btn_souris_rect.collidepoint(pos):
            self.hovered_element = 'souris'
        
        # Boutons langue
        elif self.btn_francais_rect.collidepoint(pos):
            self.hovered_element = 'francais'
        elif self.btn_anglais_rect.collidepoint(pos):
            self.hovered_element = 'anglais'
        
        # Bouton tutoriel
        elif self.btn_tutorial_rect.collidepoint(pos):
            self.hovered_element = 'tutorial'
        
        # Sliders (zone élargie pour faciliter le clic)
        elif self._is_near_slider(pos, self.music_slider_rect):
            self.hovered_element = 'music_slider'
        elif self._is_near_slider(pos, self.sfx_slider_rect):
            self.hovered_element = 'sfx_slider'
    
    def _is_near_slider(self, pos: Tuple[int, int], slider_rect: pygame.Rect) -> bool:
        """Vérifie si la souris est proche d'un slider (zone élargie)."""
        expanded = slider_rect.inflate(20, 30)
        return expanded.collidepoint(pos)
    
    def _handle_mouse_down(self, pos: Tuple[int, int]):
        """Gère le clic de la souris."""
        self.clicked_element = self.hovered_element
        
        # Commencer le drag d'un slider
        if self._is_near_slider(pos, self.music_slider_rect):
            self.dragging_slider = 'music'
            self._update_slider_from_mouse(pos)
        elif self._is_near_slider(pos, self.sfx_slider_rect):
            self.dragging_slider = 'sfx'
            self._update_slider_from_mouse(pos)
    
    def _handle_mouse_up(self, pos: Tuple[int, int]):
        """Gère le relâchement du clic."""
        # Arrêter le drag
        self.dragging_slider = None
        
        # Exécuter l'action si on relâche sur le même élément
        if self.clicked_element and self.clicked_element == self.hovered_element:
            if self.clicked_element == 'clavier':
                self._on_clavier()
            elif self.clicked_element == 'souris':
                self._on_souris()
            elif self.clicked_element == 'francais':
                self._on_francais()
            elif self.clicked_element == 'anglais':
                self._on_anglais()
            elif self.clicked_element == 'tutorial':
                self._on_tutorial()
        
        self.clicked_element = None
    
    def _update_slider_from_mouse(self, pos: Tuple[int, int]):
        """Met à jour le volume selon la position de la souris sur le slider."""
        if not self.settings:
            return
        
        if self.dragging_slider == 'music':
            slider_rect = self.music_slider_rect
            volume = self._calculate_volume_from_pos(pos[0], slider_rect)
            self.settings.set_music_volume(volume)
        
        elif self.dragging_slider == 'sfx':
            slider_rect = self.sfx_slider_rect
            volume = self._calculate_volume_from_pos(pos[0], slider_rect)
            self.settings.set_sfx_volume(volume)
    
    def _calculate_volume_from_pos(self, x: int, slider_rect: pygame.Rect) -> float:
        """Calcule le volume (0.0 à 1.0) selon la position X sur le slider."""
        left = slider_rect.left
        right = slider_rect.right
        
        # Clamp la position
        x = max(left, min(right, x))
        
        # Calculer le ratio
        return (x - left) / (right - left)
    
    def update(self, dt: float):
        pass
    
    def render(self, screen: pygame.Surface):
        """Affiche la scène."""
        # Fond
        screen.blit(self.background, (0, 0))
        
        # Bloc paramètres (centre)
        block_rect = self.block_params.get_rect(center=Layout.SETTINGS_BLOCK_PARAMS)
        screen.blit(self.block_params, block_rect)
        
        # Labels des options
        self._render_labels(screen)
        
        # Mode de contrôle (boutons clavier/souris)
        self._render_control_buttons(screen)
        
        # Sliders volume
        self._render_volume_sliders(screen)
        
        # Langue (boutons français/anglais)
        self._render_language_buttons(screen)
        
        # Bouton tutoriel
        self._render_tutorial_button(screen)
        
        # Info "Les paramètres sont globaux"
        self._render_info(screen)
        
        # Boutons navigation
        self.btn_cross.render(screen)
    
    def _render_labels(self, screen: pygame.Surface):
        """Affiche les labels des options."""
        # Mode contrôle
        label = lang_manager.get("settings.control_mode")
        surface = self.font_label.render(label, True, TextColors.SETTINGS_LABEL)
        rect = surface.get_rect(left=Layout.SETTINGS_LABEL_CONTROL[0], centery=Layout.SETTINGS_LABEL_CONTROL[1])
        screen.blit(surface, rect)
        
        # Volume musique
        label = lang_manager.get("settings.music_volume")
        surface = self.font_label.render(label, True, TextColors.SETTINGS_LABEL)
        rect = surface.get_rect(left=Layout.SETTINGS_LABEL_MUSIC[0], centery=Layout.SETTINGS_LABEL_MUSIC[1])
        screen.blit(surface, rect)
        
        # Volume sonore
        label = lang_manager.get("settings.sfx_volume")
        surface = self.font_label.render(label, True, TextColors.SETTINGS_LABEL)
        rect = surface.get_rect(left=Layout.SETTINGS_LABEL_SFX[0], centery=Layout.SETTINGS_LABEL_SFX[1])
        screen.blit(surface, rect)
        
        # Langue
        label = lang_manager.get("settings.language")
        surface = self.font_label.render(label, True, TextColors.SETTINGS_LABEL)
        rect = surface.get_rect(left=Layout.SETTINGS_LABEL_LANG[0], centery=Layout.SETTINGS_LABEL_LANG[1])
        screen.blit(surface, rect)
    
    def _render_control_buttons(self, screen: pygame.Surface):
        """Affiche les boutons de mode de contrôle."""
        current_mode = self.settings.control_mode if self.settings else ControlMode.MOUSE
        
        # Bouton Clavier
        self._render_selectable_button(
            screen,
            self.btn_clavier_img,
            self.btn_clavier_rect,
            lang_manager.get("settings.control_keyboard"),
            self.font_control,
            TextColors.SETTINGS_CONTROL,
            is_selected=(current_mode == ControlMode.KEYBOARD),
            is_hovered=(self.hovered_element == 'clavier'),
            is_clicked=(self.clicked_element == 'clavier')
        )
        
        # Bouton Souris
        self._render_selectable_button(
            screen,
            self.btn_souris_img,
            self.btn_souris_rect,
            lang_manager.get("settings.control_mouse"),
            self.font_control,
            TextColors.SETTINGS_CONTROL,
            is_selected=(current_mode == ControlMode.MOUSE),
            is_hovered=(self.hovered_element == 'souris'),
            is_clicked=(self.clicked_element == 'souris')
        )
    
    def _render_language_buttons(self, screen: pygame.Surface):
        """Affiche les boutons de langue."""
        current_lang = self.settings.language if self.settings else 'fr'
        
        # Bouton Français
        self._render_selectable_button(
            screen,
            self.btn_francais_img,
            self.btn_francais_rect,
            lang_manager.get("settings.language_fr"),
            self.font_lang,
            TextColors.SETTINGS_LANG,
            is_selected=(current_lang == 'fr'),
            is_hovered=(self.hovered_element == 'francais'),
            is_clicked=(self.clicked_element == 'francais')
        )
        
        # Bouton Anglais
        self._render_selectable_button(
            screen,
            self.btn_anglais_img,
            self.btn_anglais_rect,
            lang_manager.get("settings.language_en"),
            self.font_lang,
            TextColors.SETTINGS_LANG,
            is_selected=(current_lang == 'en'),
            is_hovered=(self.hovered_element == 'anglais'),
            is_clicked=(self.clicked_element == 'anglais')
        )
    
    def _render_selectable_button(self, screen: pygame.Surface, image: pygame.Surface,
                                   rect: pygame.Rect, text: str, font: pygame.font.Font,
                                   color: Tuple[int, int, int], is_selected: bool,
                                   is_hovered: bool, is_clicked: bool):
        """Affiche un bouton sélectionnable avec effets."""
        # Copier l'image pour appliquer les effets
        img = image.copy()
        
        if is_clicked:
            # Assombrir au clic
            img.fill((180, 180, 180), special_flags=pygame.BLEND_RGB_MULT)
        elif is_hovered:
            # Éclaircir au survol
            img.fill((30, 30, 30), special_flags=pygame.BLEND_RGB_ADD)
        elif not is_selected:
            # Assombrir si non sélectionné
            img.fill((120, 120, 120), special_flags=pygame.BLEND_RGB_MULT)
        
        screen.blit(img, rect)
        
        # Texte
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)
    
    def _render_volume_sliders(self, screen: pygame.Surface):
        """Affiche les sliders de volume."""
        music_vol = self.settings.music_volume if self.settings else 0.5
        sfx_vol = self.settings.sfx_volume if self.settings else 0.5
        
        # Slider musique
        self._render_slider(screen, self.music_slider_rect, music_vol, 
                           Layout.SETTINGS_VOL_MUSIC_0, Layout.SETTINGS_VOL_MUSIC_100)
        
        # Slider SFX
        self._render_slider(screen, self.sfx_slider_rect, sfx_vol,
                           Layout.SETTINGS_VOL_SFX_0, Layout.SETTINGS_VOL_SFX_100)
    
    def _render_slider(self, screen: pygame.Surface, rect: pygame.Rect, value: float,
                       pos_0: Tuple[int, int], pos_100: Tuple[int, int]):
        """Affiche un slider avec sa valeur."""
        # Fond du slider (violet foncé)
        pygame.draw.rect(screen, TextColors.SETTINGS_GAUGE_DARK, rect, border_radius=11)
        
        # Partie remplie (violet clair)
        if value > 0:
            filled_width = int(rect.width * value)
            filled_rect = pygame.Rect(rect.left, rect.top, filled_width, rect.height)
            pygame.draw.rect(screen, TextColors.SETTINGS_GAUGE_LIGHT, filled_rect, border_radius=11)
        
        # Curseur (petit cercle)
        cursor_x = rect.left + int(rect.width * value)
        cursor_y = rect.centery
        pygame.draw.circle(screen, (255, 255, 255), (cursor_x, cursor_y), 12)
        pygame.draw.circle(screen, TextColors.SETTINGS_GAUGE_LIGHT, (cursor_x, cursor_y), 10)
        
        # Texte "0%" à gauche (justifié droite)
        text_0 = "0%"
        surface_0 = self.font_volume.render(text_0, True, TextColors.SETTINGS_LABEL)
        rect_0 = surface_0.get_rect(right=pos_0[0], centery=pos_0[1])
        screen.blit(surface_0, rect_0)
        
        # Texte "100%" à droite (justifié gauche)
        text_100 = "100%"
        surface_100 = self.font_volume.render(text_100, True, TextColors.SETTINGS_LABEL)
        rect_100 = surface_100.get_rect(left=pos_100[0], centery=pos_100[1])
        screen.blit(surface_100, rect_100)
    
    def _render_tutorial_button(self, screen: pygame.Surface):
        """Affiche le bouton 'Revoir le tutoriel'."""
        is_hovered = (self.hovered_element == 'tutorial')
        is_clicked = (self.clicked_element == 'tutorial')
        
        img = self.btn_tutorial_img.copy()
        
        if is_clicked:
            img.fill((180, 180, 180), special_flags=pygame.BLEND_RGB_MULT)
        elif is_hovered:
            img.fill((30, 30, 30), special_flags=pygame.BLEND_RGB_ADD)
        
        screen.blit(img, self.btn_tutorial_rect)
        
        # Texte
        text = lang_manager.get("settings.tutorial_replay")
        text_surface = self.font_tutorial.render(text, True, TextColors.SETTINGS_TUTORIAL)
        text_rect = text_surface.get_rect(center=self.btn_tutorial_rect.center)
        screen.blit(text_surface, text_rect)
    
    def _render_info(self, screen: pygame.Surface):
        """Affiche le texte d'info en bas."""
        text = lang_manager.get("settings.global_info")
        surface = self.font_info.render(text, True, TextColors.SETTINGS_LABEL)
        rect = surface.get_rect(center=Layout.SETTINGS_INFO)
        screen.blit(surface, rect)
    
    def cleanup(self):
        """Nettoyage à la sortie de la scène."""
        pass
