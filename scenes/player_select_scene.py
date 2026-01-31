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
from typing import List, Optional

from scenes.base_scene import BaseScene
from config import (
    IMAGES_DIR, FONTS_DIR, WINDOW_WIDTH, WINDOW_HEIGHT,
    Images, Layout, TextColors, FONT_FILE, FONT_SIZE
)
from core import lang_manager
from core.player_manager import PlayerManager


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
        
        # Images
        self.pseudo_field_img = None
        self.difficulty_label_img = None
        self.btn_easy_img = None
        self.btn_normal_img = None
        self.btn_hard_img = None
        self.btn_start_img = None
        self.gear_img = None
        self.cross_img = None
        
        # Rectangles pour les clics
        self.pseudo_field_rect = None
        self.btn_easy_rect = None
        self.btn_normal_rect = None
        self.btn_hard_rect = None
        self.btn_start_rect = None
        self.gear_rect = None
        self.cross_rect = None
        
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
        
        # Images et rectangles
        self.pseudo_field_img = pygame.image.load(
            os.path.join(IMAGES_DIR, Images.PSS_PSEUDO_FIELD)
        ).convert_alpha()
        self.pseudo_field_rect = self.pseudo_field_img.get_rect(center=Layout.PSS_PSEUDO_FIELD)
        
        self.difficulty_label_img = pygame.image.load(
            os.path.join(IMAGES_DIR, Images.PSS_DIFFICULTY_LABEL)
        ).convert_alpha()
        
        self.btn_easy_img = pygame.image.load(
            os.path.join(IMAGES_DIR, Images.PSS_BTN_EASY)
        ).convert_alpha()
        self.btn_easy_rect = self.btn_easy_img.get_rect(center=Layout.PSS_BTN_EASY)
        
        self.btn_normal_img = pygame.image.load(
            os.path.join(IMAGES_DIR, Images.PSS_BTN_NORMAL)
        ).convert_alpha()
        self.btn_normal_rect = self.btn_normal_img.get_rect(center=Layout.PSS_BTN_NORMAL)
        
        self.btn_hard_img = pygame.image.load(
            os.path.join(IMAGES_DIR, Images.PSS_BTN_HARD)
        ).convert_alpha()
        self.btn_hard_rect = self.btn_hard_img.get_rect(center=Layout.PSS_BTN_HARD)
        
        self.btn_start_img = pygame.image.load(
            os.path.join(IMAGES_DIR, Images.PSS_BTN_START)
        ).convert_alpha()
        self.btn_start_rect = self.btn_start_img.get_rect(center=Layout.PSS_BTN_START)
        
        self.gear_img = pygame.image.load(
            os.path.join(IMAGES_DIR, Images.PSS_GEAR)
        ).convert_alpha()
        self.gear_rect = self.gear_img.get_rect(center=Layout.PSS_GEAR)
        
        self.cross_img = pygame.image.load(
            os.path.join(IMAGES_DIR, Images.PSS_CROSS)
        ).convert_alpha()
        self.cross_rect = self.cross_img.get_rect(center=Layout.PSS_CROSS)
    
    def set_player_manager(self, manager: PlayerManager):
        """Définit le gestionnaire de joueurs."""
        self.player_manager = manager
    
    def handle_events(self, events: List[pygame.event.Event]):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._handle_click(event.pos)
            
            elif event.type == pygame.KEYDOWN:
                self._handle_key(event)
    
    def _handle_click(self, pos: tuple):
        """Gère les clics souris."""
        # Croix = retour menu
        if self.cross_rect.collidepoint(pos):
            self.scene_manager.change_scene('menu')
            return
        
        # Engrenage = paramètres
        if self.gear_rect.collidepoint(pos):
            self.scene_manager.change_scene('settings')
            return
        
        # Champ pseudo = activer le focus
        if self.pseudo_field_rect.collidepoint(pos):
            self.pseudo_field_focused = True
            self.cursor_visible = True
            self.cursor_timer = 0.0
            return
        else:
            # Clic ailleurs = désactiver le focus
            self.pseudo_field_focused = False
        
        # Boutons de difficulté (seulement en mode classique)
        if not self.is_challenge_mode:
            if self.btn_easy_rect.collidepoint(pos):
                self.selected_difficulty = "easy"
                return
            
            if self.btn_normal_rect.collidepoint(pos):
                self.selected_difficulty = "normal"
                return
            
            if self.btn_hard_rect.collidepoint(pos):
                self.selected_difficulty = "hard"
                return
        
        # Bouton "C'est parti !" (seulement si pseudo non vide)
        if self.btn_start_rect.collidepoint(pos) and self.pseudo:
            self._start_game()
    
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
    
    def _start_game(self):
        """Lance la partie."""
        # Sauvegarder les données dans shared_data
        self.scene_manager.shared_data['pseudo'] = self.pseudo
        self.scene_manager.shared_data['difficulty'] = self.selected_difficulty
        
        # Vérifier si c'est un nouveau joueur (pour le tutoriel)
        if self.player_manager:
            self.player_manager.set_current_player(self.pseudo)
            
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
    
    def render(self, screen: pygame.Surface):
        """Affiche la scène."""
        # Fond
        screen.blit(self.background, (0, 0))
        
        # Engrenage et croix (haut droite)
        screen.blit(self.gear_img, self.gear_rect)
        screen.blit(self.cross_img, self.cross_rect)
        
        # Champ pseudo
        self._render_pseudo_field(screen)
        
        # Section difficulté (seulement en mode classique)
        if not self.is_challenge_mode:
            self._render_difficulty_section(screen)
        
        # Bouton "C'est parti !"
        self._render_start_button(screen)
    
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
        
        # Boutons de difficulté
        difficulties = [
            ("easy", self.btn_easy_img, self.btn_easy_rect, TextColors.PSS_EASY, "player_select.difficulty_easy"),
            ("normal", self.btn_normal_img, self.btn_normal_rect, TextColors.PSS_NORMAL, "player_select.difficulty_normal"),
            ("hard", self.btn_hard_img, self.btn_hard_rect, TextColors.PSS_HARD, "player_select.difficulty_hard"),
        ]
        
        for diff_key, img, rect, color, text_key in difficulties:
            # Assombrir si non sélectionné
            if diff_key == self.selected_difficulty:
                screen.blit(img, rect)
            else:
                # Créer une copie assombrie qui respecte l'alpha original
                darkened_img = img.copy()
                # Multiplier les couleurs par un facteur sombre (garder l'alpha)
                darkened_img.fill((80, 80, 80), special_flags=pygame.BLEND_RGB_MULT)
                screen.blit(darkened_img, rect)
            
            # Texte
            text = lang_manager.get(text_key)
            text_surface = self.font.render(text, True, color)
            text_rect = text_surface.get_rect(center=rect.center)
            screen.blit(text_surface, text_rect)
    
    def _render_start_button(self, screen: pygame.Surface):
        """Affiche le bouton C'est parti."""
        # Assombrir si pseudo vide
        if self.pseudo:
            screen.blit(self.btn_start_img, self.btn_start_rect)
        else:
            # Créer une copie assombrie qui respecte l'alpha original
            darkened_img = self.btn_start_img.copy()
            darkened_img.fill((80, 80, 80), special_flags=pygame.BLEND_RGB_MULT)
            screen.blit(darkened_img, self.btn_start_rect)
        
        # Texte
        text = lang_manager.get("player_select.start_button")
        text_surface = self.font.render(text, True, TextColors.PSS_START)
        text_rect = text_surface.get_rect(center=self.btn_start_rect.center)
        screen.blit(text_surface, text_rect)
    
    def cleanup(self):
        """Nettoyage à la sortie de la scène."""
        pass
