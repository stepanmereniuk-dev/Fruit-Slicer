"""
PlayerSelectScene - Écran de sélection du pseudo et de la difficulté.

Fonctionnalités :
- Saisie du pseudo (max 10 caractères, lettres uniquement)
- Choix de la difficulté (Facile/Normal/Difficile) - masqué en mode Challenge
- Bouton "C'est parti !" (grisé si pseudo vide)
- Bouton retour (croix) et paramètres (engrenage)
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
    """Scène de sélection du joueur et de la difficulté."""
    
    # Pseudo : max 10 caractères, lettres uniquement
    MAX_PSEUDO_LENGTH = 10
    
    def __init__(self, scene_manager):
        super().__init__(scene_manager)
        
        # Ressources
        self.background = None
        self.font = None
        self.font_large = None
        
        # Images spécifiques (pas des boutons)
        self.pseudo_field_img = None
        self.pseudo_field_rect = None
        self.difficulty_label_img = None
        
        # Boutons avec effets
        self.btn_gear: Optional[ImageButton] = None
        self.btn_cross: Optional[ImageButton] = None
        self.btn_start: Optional[Button] = None
        self.difficulty_buttons: Dict[str, Button] = {}
        
        # État
        self.pseudo = ""
        self.selected_difficulty = "normal"  # easy, normal, hard
        self.is_challenge_mode = False
        
        # État du champ de texte
        self.pseudo_field_focused = False
        self.cursor_visible = True
        self.cursor_timer = 0.0
        self.CURSOR_BLINK_RATE = 0.5  # Clignotement toutes les 0.5 secondes
        
        # Player manager
        self.player_manager: Optional[PlayerManager] = None
    
    def setup(self):
        """Initialise la scène."""
        # Récupérer le mode depuis shared_data
        self.is_challenge_mode = self.scene_manager.shared_data.get('mode') == 'challenge'
        
        # Reset pseudo et difficulté
        self.pseudo = ""
        self.selected_difficulty = "normal"
        self.pseudo_field_focused = False
        self.cursor_visible = True
        self.cursor_timer = 0.0
        
        # Charger les ressources
        self._load_resources()
    
    def _load_resources(self):
        """Charge les images et polices."""
        # Background
        self.background = pygame.image.load(
            os.path.join(IMAGES_DIR, Images.PSS_BG)
        ).convert()
        
        # Polices
        font_path = os.path.join(FONTS_DIR, FONT_FILE)
        self.font = pygame.font.Font(font_path, FONT_SIZE)
        self.font_large = pygame.font.Font(font_path, 42)
        
        # Champ pseudo (pas un bouton, juste une image)
        self.pseudo_field_img = pygame.image.load(
            os.path.join(IMAGES_DIR, Images.PSS_PSEUDO_FIELD)
        ).convert_alpha()
        self.pseudo_field_rect = self.pseudo_field_img.get_rect(center=Layout.PSS_PSEUDO_FIELD)
        
        # Label difficulté
        self.difficulty_label_img = pygame.image.load(
            os.path.join(IMAGES_DIR, Images.PSS_DIFFICULTY_LABEL)
        ).convert_alpha()
        
        # Boutons icônes (engrenage, croix)
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
        
        # Bouton Start
        self.btn_start = Button(
            image_path=Images.PSS_BTN_START,
            center=Layout.PSS_BTN_START,
            text=lang_manager.get("player_select.start_button"),
            text_color=TextColors.PSS_START,
            on_click=self._on_start,
            enabled=False  # Désactivé par défaut (pseudo vide)
        )
        
        # Boutons de difficulté
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
        """Définit le gestionnaire de joueurs."""
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
            # Boutons icônes
            self.btn_gear.handle_event(event)
            self.btn_cross.handle_event(event)
            
            # Bouton start
            self.btn_start.handle_event(event)
            
            # Boutons difficulté : pas d'effets hover/clic, juste détection du clic
            if not self.is_challenge_mode:
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    for diff_key, btn in self.difficulty_buttons.items():
                        if btn.rect.collidepoint(event.pos):
                            self._select_difficulty(diff_key)
            
            # Gestion du champ pseudo
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Clic sur le champ pseudo ?
                if self.pseudo_field_rect.collidepoint(event.pos):
                    self.pseudo_field_focused = True
                    self.cursor_visible = True
                    self.cursor_timer = 0.0
                else:
                    self.pseudo_field_focused = False
            
            elif event.type == pygame.KEYDOWN:
                self._handle_key(event)
    
    def _handle_key(self, event: pygame.event.Event):
        """Gère la saisie clavier pour le pseudo."""
        if event.key == pygame.K_BACKSPACE:
            # Supprimer le dernier caractère
            self.pseudo = self.pseudo[:-1]
        
        elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
            # Entrée = lancer si pseudo valide
            if self.pseudo:
                self._start_game()
        
        elif event.key == pygame.K_ESCAPE:
            # Échap = retour menu
            self.scene_manager.change_scene('menu')
        
        else:
            # Ajouter un caractère (lettres uniquement)
            if len(self.pseudo) < self.MAX_PSEUDO_LENGTH:
                char = event.unicode
                if char.isalpha():
                    self.pseudo += char
        
        # Mettre à jour l'état du bouton start
        self.btn_start.set_enabled(bool(self.pseudo))
    
    def _start_game(self):
        """Lance la partie."""
        # Sauvegarder les données dans shared_data
        self.scene_manager.shared_data['pseudo'] = self.pseudo
        self.scene_manager.shared_data['difficulty'] = self.selected_difficulty
        
        # Définir le joueur courant dans PlayerManager
        if self.player_manager:
            self.player_manager.set_current_player(self.pseudo)
            
            # Synchroniser les achievements avec le nouveau joueur
            self.scene_manager.on_player_selected(self.pseudo)
            
            # Vérifier si c'est un nouveau joueur (pour le tutoriel)
            if self.player_manager.should_show_tutorial():
                self.scene_manager.change_scene('tutorial')
                return
        
        # Lancer directement le jeu
        self.scene_manager.change_scene('game')
    
    def update(self, dt: float):
        """Mise à jour du curseur clignotant."""
        if self.pseudo_field_focused:
            self.cursor_timer += dt
            if self.cursor_timer >= self.CURSOR_BLINK_RATE:
                self.cursor_timer = 0.0
                self.cursor_visible = not self.cursor_visible
        
        # Mettre à jour l'état du bouton start selon le pseudo
        self.btn_start.set_enabled(bool(self.pseudo))
    
    def render(self, screen: pygame.Surface):
        """Affiche la scène."""
        # Fond
        screen.blit(self.background, (0, 0))
        
        # Boutons icônes (engrenage et croix)
        self.btn_gear.render(screen)
        self.btn_cross.render(screen)
        
        # Champ pseudo
        self._render_pseudo_field(screen)
        
        # Section difficulté (seulement en mode classique)
        if not self.is_challenge_mode:
            self._render_difficulty_section(screen)
        
        # Bouton "C'est parti !"
        self.btn_start.render(screen, self.font)
    
    def _render_pseudo_field(self, screen: pygame.Surface):
        """Affiche le champ de saisie du pseudo."""
        # Image de fond du champ
        screen.blit(self.pseudo_field_img, self.pseudo_field_rect)
        
        # Texte du pseudo, curseur, ou placeholder
        if self.pseudo:
            # Afficher le pseudo + curseur si focus
            text = self.pseudo
            if self.pseudo_field_focused and self.cursor_visible:
                text += "|"
            color = TextColors.PSS_PSEUDO
        elif self.pseudo_field_focused:
            # Focus mais pas de texte : afficher juste le curseur
            text = "|" if self.cursor_visible else ""
            color = TextColors.PSS_PSEUDO
        else:
            # Pas de focus, pas de texte : placeholder
            text = lang_manager.get("player_select.pseudo_placeholder")
            color = (150, 150, 150)  # Gris pour le placeholder
        
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(center=self.pseudo_field_rect.center)
        screen.blit(text_surface, text_rect)
    
    def _render_difficulty_section(self, screen: pygame.Surface):
        """Affiche la section de sélection de difficulté."""
        # Label "Difficulté"
        label_rect = self.difficulty_label_img.get_rect(center=Layout.PSS_DIFFICULTY_LABEL)
        screen.blit(self.difficulty_label_img, label_rect)
        
        difficulty_text = lang_manager.get("player_select.difficulty_label")
        text_surface = self.font.render(difficulty_text, True, TextColors.PSS_DIFFICULTY)
        text_rect = text_surface.get_rect(center=label_rect.center)
        screen.blit(text_surface, text_rect)
        
        # Boutons de difficulté (sans effets hover/clic, juste sélection)
        for diff_key, btn in self.difficulty_buttons.items():
            if diff_key == self.selected_difficulty:
                # Bouton sélectionné : rendu normal
                screen.blit(btn.image_original, btn.rect)
            else:
                # Bouton non sélectionné : assombri
                darkened_img = btn.image_original.copy()
                darkened_img.fill((80, 80, 80), special_flags=pygame.BLEND_RGB_MULT)
                screen.blit(darkened_img, btn.rect)
            
            # Texte
            text_surface = self.font.render(btn.text, True, btn.text_color)
            text_rect = text_surface.get_rect(center=btn.rect.center)
            screen.blit(text_surface, text_rect)
    
    def cleanup(self):
        """Nettoyage à la sortie de la scène."""
        pass
