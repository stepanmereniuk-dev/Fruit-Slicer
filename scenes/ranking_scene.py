"""
RankingScene - Écran de classement (Top 10 par catégorie).

Fonctionnalités :
- 4 onglets : Facile, Normal, Difficile, Challenge
- Affiche le Top 10 de la catégorie sélectionnée
- Colonnes : Rang, Pseudo, Meilleur score
"""

import pygame
import os
from typing import List, Dict, Optional

from scenes.base_scene import BaseScene
from config import (
    IMAGES_DIR, FONTS_DIR, FONT_FILE,
    Images, Layout, TextColors
)
from core import lang_manager
from core.player_manager import PlayerManager
from ui.buttons import ImageButton


class RankingScene(BaseScene):
    """Scène du classement avec onglets par difficulté."""
    
    # Tailles de police
    TITLE_FONT_SIZE = 36
    TAB_FONT_SIZE = 36
    HEADER_FONT_SIZE = 36
    DATA_FONT_SIZE = 36
    
    # Catégories disponibles
    CATEGORIES = ['easy', 'normal', 'hard', 'challenge']
    
    def __init__(self, scene_manager):
        super().__init__(scene_manager)
        
        # Ressources
        self.background = None
        self.block_img = None
        self.title_img = None
        self.font_title = None
        self.font_tab = None
        self.font_header = None
        self.font_data = None
        
        # Images des onglets
        self.tab_images: Dict[str, pygame.Surface] = {}
        
        # Boutons
        self.btn_gear: Optional[ImageButton] = None
        self.btn_cross: Optional[ImageButton] = None
        
        # État
        self.selected_category = 'normal'  # Par défaut
        self.leaderboard_data: List[Dict] = []
        
        # Référence au player manager
        self.player_manager: Optional[PlayerManager] = None
    
    def setup(self):
        """Initialise la scène."""
        self._load_resources()
        self._refresh_leaderboard()
    
    def _load_resources(self):
        """Charge les images et polices."""
        # Background
        self.background = pygame.image.load(
            os.path.join(IMAGES_DIR, Images.RANKING_BG)
        ).convert()
        
        # Bloc central
        self.block_img = pygame.image.load(
            os.path.join(IMAGES_DIR, Images.RANKING_BLOCK)
        ).convert_alpha()
        
        # Titre "Classement"
        self.title_img = pygame.image.load(
            os.path.join(IMAGES_DIR, Images.RANKING_TITLE)
        ).convert_alpha()
        
        # Polices
        font_path = os.path.join(FONTS_DIR, FONT_FILE)
        self.font_title = pygame.font.Font(font_path, self.TITLE_FONT_SIZE)
        self.font_tab = pygame.font.Font(font_path, self.TAB_FONT_SIZE)
        self.font_header = pygame.font.Font(font_path, self.HEADER_FONT_SIZE)
        self.font_data = pygame.font.Font(font_path, self.DATA_FONT_SIZE)
        
        # Images des onglets
        self.tab_images = {
            'easy': pygame.image.load(
                os.path.join(IMAGES_DIR, Images.RANKING_BTN_EASY)
            ).convert_alpha(),
            'normal': pygame.image.load(
                os.path.join(IMAGES_DIR, Images.RANKING_BTN_NORMAL)
            ).convert_alpha(),
            'hard': pygame.image.load(
                os.path.join(IMAGES_DIR, Images.RANKING_BTN_HARD)
            ).convert_alpha(),
            'challenge': pygame.image.load(
                os.path.join(IMAGES_DIR, Images.RANKING_BTN_CHALLENGE)
            ).convert_alpha(),
        }
        
        # Boutons (engrenage et croix)
        self.btn_gear = ImageButton(
            image_path=Images.RANKING_GEAR,
            center=Layout.RANKING_GEAR,
            on_click=self._on_settings
        )
        self.btn_cross = ImageButton(
            image_path=Images.RANKING_CROSS,
            center=Layout.RANKING_CROSS,
            on_click=self._on_back
        )
    
    def set_player_manager(self, manager: PlayerManager):
        """Définit le gestionnaire de joueurs."""
        self.player_manager = manager
    
    def _refresh_leaderboard(self):
        """Rafraîchit les données du classement."""
        if self.player_manager:
            # Convertir la catégorie en clé pour le player_manager
            if self.selected_category == 'challenge':
                category_key = 'challenge'
            else:
                category_key = f'classic_{self.selected_category}'
            
            self.leaderboard_data = self.player_manager.get_leaderboard(category_key, limit=10)
        else:
            self.leaderboard_data = []
    
    # Callbacks
    def _on_settings(self):
        self.scene_manager.change_scene('settings')
    
    def _on_back(self):
        self.scene_manager.change_scene('menu')
    
    def _select_category(self, category: str):
        """Sélectionne une catégorie et rafraîchit le classement."""
        if category != self.selected_category:
            self.selected_category = category
            self._refresh_leaderboard()
    
    def handle_events(self, events: List[pygame.event.Event]):
        for event in events:
            # Boutons
            self.btn_gear.handle_event(event)
            self.btn_cross.handle_event(event)
            
            # Clic sur les onglets
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self._handle_tab_click(event.pos)
            
            # Raccourcis clavier
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._on_back()
                elif event.key == pygame.K_LEFT:
                    self._select_previous_category()
                elif event.key == pygame.K_RIGHT:
                    self._select_next_category()
    
    def _handle_tab_click(self, pos):
        """Gère le clic sur un onglet."""
        tab_positions = {
            'easy': Layout.RANKING_TAB_EASY,
            'normal': Layout.RANKING_TAB_NORMAL,
            'hard': Layout.RANKING_TAB_HARD,
            'challenge': Layout.RANKING_TAB_CHALLENGE,
        }
        
        for category, center in tab_positions.items():
            tab_img = self.tab_images.get(category)
            if tab_img:
                rect = tab_img.get_rect(center=center)
                if rect.collidepoint(pos):
                    self._select_category(category)
                    break
    
    def _select_previous_category(self):
        """Sélectionne la catégorie précédente."""
        idx = self.CATEGORIES.index(self.selected_category)
        new_idx = (idx - 1) % len(self.CATEGORIES)
        self._select_category(self.CATEGORIES[new_idx])
    
    def _select_next_category(self):
        """Sélectionne la catégorie suivante."""
        idx = self.CATEGORIES.index(self.selected_category)
        new_idx = (idx + 1) % len(self.CATEGORIES)
        self._select_category(self.CATEGORIES[new_idx])
    
    def update(self, dt: float):
        pass
    
    def render(self, screen: pygame.Surface):
        """Affiche la scène."""
        # Fond
        screen.blit(self.background, (0, 0))
        
        # Bloc central
        block_rect = self.block_img.get_rect(center=Layout.RANKING_BLOCK)
        screen.blit(self.block_img, block_rect)
        
        # Titre "Classement"
        self._render_title(screen)
        
        # Onglets
        self._render_tabs(screen)
        
        # En-têtes du tableau
        self._render_headers(screen)
        
        # Données du classement
        self._render_leaderboard(screen)
        
        # Boutons
        self.btn_gear.render(screen)
        self.btn_cross.render(screen)
    
    def _render_title(self, screen: pygame.Surface):
        """Affiche le titre avec son image de fond."""
        # Image de fond du titre
        title_rect = self.title_img.get_rect(center=Layout.RANKING_TITLE)
        screen.blit(self.title_img, title_rect)
        
        # Texte "Classement"
        title_text = lang_manager.get("leaderboard.title")
        text_surface = self.font_title.render(title_text, True, TextColors.RANKING_TITLE)
        text_rect = text_surface.get_rect(center=Layout.RANKING_TITLE)
        screen.blit(text_surface, text_rect)
    
    def _render_tabs(self, screen: pygame.Surface):
        """Affiche les onglets de catégorie."""
        tab_data = [
            ('easy', Layout.RANKING_TAB_EASY, TextColors.RANKING_TAB_EASY, "leaderboard.tab_easy"),
            ('normal', Layout.RANKING_TAB_NORMAL, TextColors.RANKING_TAB_NORMAL, "leaderboard.tab_normal"),
            ('hard', Layout.RANKING_TAB_HARD, TextColors.RANKING_TAB_HARD, "leaderboard.tab_hard"),
            ('challenge', Layout.RANKING_TAB_CHALLENGE, TextColors.RANKING_TAB_CHALLENGE, "leaderboard.tab_challenge"),
        ]
        
        for category, center, color, lang_key in tab_data:
            tab_img = self.tab_images.get(category)
            if not tab_img:
                continue
            
            # Assombrir si non sélectionné
            if category != self.selected_category:
                tab_img = tab_img.copy()
                tab_img.fill((120, 120, 120), special_flags=pygame.BLEND_RGB_MULT)
            
            # Image de fond de l'onglet
            tab_rect = tab_img.get_rect(center=center)
            screen.blit(tab_img, tab_rect)
            
            # Texte de l'onglet
            tab_text = lang_manager.get(lang_key)
            text_surface = self.font_tab.render(tab_text, True, color)
            text_rect = text_surface.get_rect(center=center)
            screen.blit(text_surface, text_rect)
    
    def _render_headers(self, screen: pygame.Surface):
        """Affiche les en-têtes du tableau."""
        headers = [
            (lang_manager.get("leaderboard.rank_header"), Layout.RANKING_HEADER_RANK),
            (lang_manager.get("leaderboard.pseudo_header"), Layout.RANKING_HEADER_PSEUDO),
            (lang_manager.get("leaderboard.score_header"), Layout.RANKING_HEADER_SCORE),
        ]
        
        for text, pos in headers:
            text_surface = self.font_header.render(text, True, TextColors.RANKING_HEADER)
            text_rect = text_surface.get_rect(center=pos)
            screen.blit(text_surface, text_rect)
    
    def _render_leaderboard(self, screen: pygame.Surface):
        """Affiche les données du classement (Top 10)."""
        if not self.leaderboard_data:
            # Afficher un message si pas de données
            empty_text = lang_manager.get("leaderboard.no_scores")
            text_surface = self.font_data.render(empty_text, True, TextColors.RANKING_DATA)
            text_rect = text_surface.get_rect(center=(960, 500))
            screen.blit(text_surface, text_rect)
            return
        
        start_y = Layout.RANKING_DATA_START_Y
        line_height = Layout.RANKING_DATA_LINE_HEIGHT
        
        for i, entry in enumerate(self.leaderboard_data):
            y = start_y + i * line_height
            
            # Rang
            rank_text = str(entry['rank'])
            rank_surface = self.font_data.render(rank_text, True, TextColors.RANKING_DATA)
            rank_rect = rank_surface.get_rect(center=(Layout.RANKING_DATA_RANK_X, y))
            screen.blit(rank_surface, rank_rect)
            
            # Pseudo
            pseudo_text = entry['pseudo']
            pseudo_surface = self.font_data.render(pseudo_text, True, TextColors.RANKING_DATA)
            pseudo_rect = pseudo_surface.get_rect(center=(Layout.RANKING_DATA_PSEUDO_X, y))
            screen.blit(pseudo_surface, pseudo_rect)
            
            # Score (formaté avec espaces comme séparateur de milliers)
            score = entry['score']
            score_text = f"{score:,}".replace(",", " ")
            score_surface = self.font_data.render(score_text, True, TextColors.RANKING_DATA)
            score_rect = score_surface.get_rect(center=(Layout.RANKING_DATA_SCORE_X, y))
            screen.blit(score_surface, score_rect)
    
    def cleanup(self):
        """Nettoyage à la sortie."""
        pass
