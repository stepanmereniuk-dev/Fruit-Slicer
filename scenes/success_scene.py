"""
SuccessScene - Écran des succès par pseudo.

Fonctionnalités :
- Liste des pseudos à gauche (7 max visibles avec scroll via flèches)
- Affichage des succès du pseudo sélectionné à droite
- Succès débloqués : cadre or, texte jaune
- Succès verrouillés : cadre gris, texte gris
- Navigation avec flèches haut/bas pour les succès
- Effets hover/clic sur flèches et pseudos
"""

import pygame
import os
from typing import List, Optional, Dict, Tuple

from scenes.base_scene import BaseScene
from config import (
    IMAGES_DIR, FONTS_DIR, WINDOW_WIDTH, WINDOW_HEIGHT,
    Images, Layout, TextColors, FONT_FILE
)
from core import lang_manager
from core.player_manager import PlayerManager, PlayerData
from core.achievements import AchievementManager, Achievement, ACHIEVEMENTS_DATA, AchievementCategory
from ui.buttons import ImageButton


class SuccessScene(BaseScene):
    """Scène d'affichage des succès par pseudo."""
    
    # Constantes de police (selon maquette)
    TITLE_FONT_SIZE = 36
    PSEUDO_FONT_SIZE = 28
    ACHIEVEMENT_NAME_SIZE = 30       # Nom du succès : 25px
    ACHIEVEMENT_CONDITION_SIZE = 25  # Condition : 20px
    ACHIEVEMENT_DESC_SIZE = 25       # Description : 20px
    ACHIEVEMENT_PROGRESS_SIZE = 20   # Progression : 15px
    
    # Nombre max d'éléments visibles
    MAX_VISIBLE_PSEUDOS = 7
    MAX_VISIBLE_ACHIEVEMENTS = 2
    
    # Interligne pour descriptions sur 2 lignes
    LINE_HEIGHT = 1.3
    
    # Effets visuels
    HOVER_BRIGHTEN = (30, 30, 30)
    CLICK_DARKEN = (180, 180, 180)
    
    def __init__(self, scene_manager):
        super().__init__(scene_manager)
        
        # Ressources
        self.background = None
        self.font_title = None
        self.font_pseudo = None
        self.font_achievement_name = None
        self.font_achievement_condition = None
        self.font_achievement_desc = None
        self.font_achievement_progress = None
        
        # Images
        self.title_btn_img = None
        self.bloc_img = None
        self.pseudo_btn_img = None
        self.pseudo_user_img = None
        self.cadre_or_img = None
        self.cadre_gris_img = None
        
        # Flèches (normal, hover, click)
        self.arrow_up_left_img = None
        self.arrow_down_left_img = None
        self.arrow_up_right_img = None
        self.arrow_down_right_img = None
        
        # Boutons navigation (croix/engrenage)
        self.btn_cross: Optional[ImageButton] = None
        self.btn_gear: Optional[ImageButton] = None
        
        # État
        self.pseudos: List[str] = []
        self.selected_pseudo: Optional[str] = None
        self.selected_pseudo_index: int = 0
        self.pseudo_scroll_index = 0
        self.achievement_scroll_index = 0
        
        # Données du joueur sélectionné (pas le joueur courant!)
        self.selected_player_data: Optional[PlayerData] = None
        self.achievements: List[Achievement] = []
        
        # États hover/click pour les éléments interactifs
        self.hovered_pseudo_index: Optional[int] = None
        self.clicked_pseudo_index: Optional[int] = None
        self.hovered_arrow: Optional[str] = None  # 'up_left', 'down_left', 'up_right', 'down_right'
        self.clicked_arrow: Optional[str] = None
        
        # Rectangles des flèches (pour détection hover/click)
        self.arrow_rects: Dict[str, pygame.Rect] = {}
        
        # Managers
        self.player_manager: Optional[PlayerManager] = None
        self.achievement_manager: Optional[AchievementManager] = None
    
    def setup(self):
        """Initialise la scène."""
        self._load_resources()
        self._load_pseudos()
        
        # Reset scroll et sélection
        self.pseudo_scroll_index = 0
        self.achievement_scroll_index = 0
        self.hovered_pseudo_index = None
        self.clicked_pseudo_index = None
        self.hovered_arrow = None
        self.clicked_arrow = None
        
        # Sélectionner le premier pseudo par défaut
        if self.pseudos:
            self._select_pseudo(0)
        
        # Marquer la visite de l'écran succès (pour le succès "Explorateur")
        if self.achievement_manager:
            self.achievement_manager.on_success_screen_visited()
    
    def _load_resources(self):
        """Charge les images et polices."""
        # Background
        self.background = pygame.image.load(
            os.path.join(IMAGES_DIR, Images.SUCCESS_BG)
        ).convert()
        
        # Polices
        font_path = os.path.join(FONTS_DIR, FONT_FILE)
        self.font_title = pygame.font.Font(font_path, self.TITLE_FONT_SIZE)
        self.font_pseudo = pygame.font.Font(font_path, self.PSEUDO_FONT_SIZE)
        self.font_achievement_name = pygame.font.Font(font_path, self.ACHIEVEMENT_NAME_SIZE)
        self.font_achievement_condition = pygame.font.Font(font_path, self.ACHIEVEMENT_CONDITION_SIZE)
        self.font_achievement_desc = pygame.font.Font(font_path, self.ACHIEVEMENT_DESC_SIZE)
        self.font_achievement_progress = pygame.font.Font(font_path, self.ACHIEVEMENT_PROGRESS_SIZE)
        
        # Images UI
        self.title_btn_img = pygame.image.load(
            os.path.join(IMAGES_DIR, Images.SUCCESS_TITLE_BTN)
        ).convert_alpha()
        
        self.bloc_img = pygame.image.load(
            os.path.join(IMAGES_DIR, Images.SUCCESS_BLOC)
        ).convert_alpha()
        
        self.pseudo_btn_img = pygame.image.load(
            os.path.join(IMAGES_DIR, Images.SUCCESS_PSEUDO_BTN)
        ).convert_alpha()
        
        self.pseudo_user_img = pygame.image.load(
            os.path.join(IMAGES_DIR, Images.SUCCESS_PSEUDO_USER)
        ).convert_alpha()
        
        self.cadre_or_img = pygame.image.load(
            os.path.join(IMAGES_DIR, Images.SUCCESS_CADRE_OR)
        ).convert_alpha()
        
        self.cadre_gris_img = pygame.image.load(
            os.path.join(IMAGES_DIR, Images.SUCCESS_CADRE_GRIS)
        ).convert_alpha()
        
        # Flèches
        self.arrow_up_left_img = pygame.image.load(
            os.path.join(IMAGES_DIR, Images.SUCCESS_ARROW_UP_LEFT)
        ).convert_alpha()
        
        self.arrow_down_left_img = pygame.image.load(
            os.path.join(IMAGES_DIR, Images.SUCCESS_ARROW_DOWN_LEFT)
        ).convert_alpha()
        
        self.arrow_up_right_img = pygame.image.load(
            os.path.join(IMAGES_DIR, Images.SUCCESS_ARROW_UP_RIGHT)
        ).convert_alpha()
        
        self.arrow_down_right_img = pygame.image.load(
            os.path.join(IMAGES_DIR, Images.SUCCESS_ARROW_DOWN_RIGHT)
        ).convert_alpha()
        
        # Calculer les rectangles des flèches
        self.arrow_rects = {
            'up_left': self.arrow_up_left_img.get_rect(center=Layout.SUCCESS_ARROW_UP_LEFT),
            'down_left': self.arrow_down_left_img.get_rect(center=Layout.SUCCESS_ARROW_DOWN_LEFT),
            'up_right': self.arrow_up_right_img.get_rect(center=Layout.SUCCESS_ARROW_UP_RIGHT),
            'down_right': self.arrow_down_right_img.get_rect(center=Layout.SUCCESS_ARROW_DOWN_RIGHT),
        }
        
        # Boutons navigation (croix et engrenage)
        self.btn_cross = ImageButton(
            image_path=Images.SUCCESS_CROSS,
            center=Layout.SUCCESS_CROSS,
            on_click=self._on_back
        )
        
        self.btn_gear = ImageButton(
            image_path=Images.SUCCESS_GEAR,
            center=Layout.SUCCESS_GEAR,
            on_click=self._on_settings
        )
    
    def _load_pseudos(self):
        """Charge la liste des pseudos."""
        if self.player_manager:
            self.pseudos = self.player_manager.get_all_pseudos()
        else:
            self.pseudos = []
    
    def set_player_manager(self, manager: PlayerManager):
        """Définit le gestionnaire de joueurs."""
        self.player_manager = manager
    
    def set_achievement_manager(self, manager: AchievementManager):
        """Définit le gestionnaire de succès."""
        self.achievement_manager = manager
    
    def _select_pseudo(self, index: int):
        """Sélectionne un pseudo par son index et charge ses succès."""
        if index < 0 or index >= len(self.pseudos):
            return
        
        self.selected_pseudo_index = index
        self.selected_pseudo = self.pseudos[index]
        self.achievement_scroll_index = 0
        
        # Charger les données du joueur sélectionné
        if self.player_manager:
            self.selected_player_data = self.player_manager.get_player(self.selected_pseudo)
        
        # Charger les succès de ce joueur
        self._load_achievements_for_selected_player()
    
    def _load_achievements_for_selected_player(self):
        """Charge les succès du joueur sélectionné (pas le joueur courant)."""
        self.achievements = []
        
        if not self.selected_player_data:
            return
        
        # Récupérer les succès débloqués de ce joueur
        player_achievements = self.selected_player_data.achievements
        
        # Créer la liste des Achievement avec leur état pour ce joueur
        for aid, category, cond_type, cond_value in ACHIEVEMENTS_DATA:
            unlocked = player_achievements.get(aid, False)
            ach = Achievement(
                id=aid,
                category=category.value,
                condition_type=cond_type,
                condition_value=cond_value,
                unlocked=unlocked
            )
            self.achievements.append(ach)
    
    # Callbacks
    def _on_back(self):
        self.scene_manager.change_scene('menu')
    
    def _on_settings(self):
        self.scene_manager.change_scene('settings')
    
    def _scroll_pseudos_up(self):
        if self.pseudo_scroll_index > 0:
            self.pseudo_scroll_index -= 1
    
    def _scroll_pseudos_down(self):
        max_index = max(0, len(self.pseudos) - self.MAX_VISIBLE_PSEUDOS)
        if self.pseudo_scroll_index < max_index:
            self.pseudo_scroll_index += 1
    
    def _scroll_achievements_up(self):
        if self.achievement_scroll_index > 0:
            self.achievement_scroll_index -= 1
    
    def _scroll_achievements_down(self):
        max_index = max(0, len(self.achievements) - self.MAX_VISIBLE_ACHIEVEMENTS)
        if self.achievement_scroll_index < max_index:
            self.achievement_scroll_index += 1
    
    def handle_events(self, events: List[pygame.event.Event]):
        for event in events:
            # Boutons de navigation
            self.btn_cross.handle_event(event)
            self.btn_gear.handle_event(event)
            
            if event.type == pygame.MOUSEMOTION:
                self._handle_mouse_motion(event.pos)
            
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._handle_mouse_down(event.pos)
            
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self._handle_mouse_up(event.pos)
            
            elif event.type == pygame.KEYDOWN:
                self._handle_key(event.key)
    
    def _handle_mouse_motion(self, pos: Tuple[int, int]):
        """Gère le survol de la souris."""
        # Reset hover states
        self.hovered_pseudo_index = None
        self.hovered_arrow = None
        
        # Vérifier hover sur les pseudos
        visible_pseudos = self._get_visible_pseudos()
        for i in range(len(visible_pseudos)):
            rect = self._get_pseudo_rect(i)
            if rect.collidepoint(pos):
                self.hovered_pseudo_index = i
                break
        
        # Vérifier hover sur les flèches
        for arrow_name, rect in self.arrow_rects.items():
            if rect.collidepoint(pos) and self._is_arrow_active(arrow_name):
                self.hovered_arrow = arrow_name
                break
    
    def _handle_mouse_down(self, pos: Tuple[int, int]):
        """Gère le clic souris (bouton enfoncé)."""
        # Vérifier clic sur les pseudos
        visible_pseudos = self._get_visible_pseudos()
        for i in range(len(visible_pseudos)):
            rect = self._get_pseudo_rect(i)
            if rect.collidepoint(pos):
                self.clicked_pseudo_index = i
                return
        
        # Vérifier clic sur les flèches
        for arrow_name, rect in self.arrow_rects.items():
            if rect.collidepoint(pos) and self._is_arrow_active(arrow_name):
                self.clicked_arrow = arrow_name
                return
    
    def _handle_mouse_up(self, pos: Tuple[int, int]):
        """Gère le relâchement du clic souris."""
        # Vérifier si on relâche sur un pseudo
        if self.clicked_pseudo_index is not None:
            rect = self._get_pseudo_rect(self.clicked_pseudo_index)
            if rect.collidepoint(pos):
                # Sélectionner ce pseudo
                actual_index = self.pseudo_scroll_index + self.clicked_pseudo_index
                self._select_pseudo(actual_index)
        
        # Vérifier si on relâche sur une flèche
        if self.clicked_arrow is not None:
            rect = self.arrow_rects.get(self.clicked_arrow)
            if rect and rect.collidepoint(pos):
                self._execute_arrow_action(self.clicked_arrow)
        
        # Reset click states
        self.clicked_pseudo_index = None
        self.clicked_arrow = None
    
    def _handle_key(self, key: int):
        """Gère les touches clavier."""
        if key == pygame.K_ESCAPE:
            self._on_back()
        elif key == pygame.K_UP:
            self._scroll_achievements_up()
        elif key == pygame.K_DOWN:
            self._scroll_achievements_down()
        elif key == pygame.K_LEFT:
            self._scroll_pseudos_up()
        elif key == pygame.K_RIGHT:
            self._scroll_pseudos_down()
    
    def _is_arrow_active(self, arrow_name: str) -> bool:
        """Vérifie si une flèche est active (peut être cliquée)."""
        if arrow_name == 'up_left':
            return self.pseudo_scroll_index > 0
        elif arrow_name == 'down_left':
            max_index = max(0, len(self.pseudos) - self.MAX_VISIBLE_PSEUDOS)
            return self.pseudo_scroll_index < max_index
        elif arrow_name == 'up_right':
            return self.achievement_scroll_index > 0
        elif arrow_name == 'down_right':
            max_index = max(0, len(self.achievements) - self.MAX_VISIBLE_ACHIEVEMENTS)
            return self.achievement_scroll_index < max_index
        return False
    
    def _execute_arrow_action(self, arrow_name: str):
        """Exécute l'action associée à une flèche."""
        if arrow_name == 'up_left':
            self._scroll_pseudos_up()
        elif arrow_name == 'down_left':
            self._scroll_pseudos_down()
        elif arrow_name == 'up_right':
            self._scroll_achievements_up()
        elif arrow_name == 'down_right':
            self._scroll_achievements_down()
    
    def _get_visible_pseudos(self) -> List[str]:
        """Retourne les pseudos visibles."""
        start = self.pseudo_scroll_index
        end = start + self.MAX_VISIBLE_PSEUDOS
        return self.pseudos[start:end]
    
    def _get_visible_achievements(self) -> List[Achievement]:
        """Retourne les succès visibles."""
        start = self.achievement_scroll_index
        end = start + self.MAX_VISIBLE_ACHIEVEMENTS
        return self.achievements[start:end]
    
    def _get_pseudo_rect(self, visible_index: int) -> pygame.Rect:
        """Retourne le rectangle d'un bouton pseudo."""
        y = Layout.SUCCESS_PSEUDO_POSITIONS[visible_index]
        return self.pseudo_btn_img.get_rect(center=(Layout.SUCCESS_PSEUDO_X, y))
    
    def update(self, dt: float):
        pass
    
    def render(self, screen: pygame.Surface):
        # Fond
        screen.blit(self.background, (0, 0))
        
        # Bloc principal
        bloc_rect = self.bloc_img.get_rect(center=Layout.SUCCESS_BLOC)
        screen.blit(self.bloc_img, bloc_rect)
        
        # Titre
        title_rect = self.title_btn_img.get_rect(center=Layout.SUCCESS_TITLE)
        screen.blit(self.title_btn_img, title_rect)
        title_text = lang_manager.get("success.title")
        title_surface = self.font_title.render(title_text, True, TextColors.SUCCESS_TITLE)
        title_text_rect = title_surface.get_rect(center=title_rect.center)
        screen.blit(title_surface, title_text_rect)
        
        # Boutons navigation
        self.btn_cross.render(screen)
        self.btn_gear.render(screen)
        
        # Colonne gauche : pseudos
        self._render_pseudos(screen)
        self._render_arrows_left(screen)
        
        # Colonne droite : succès du pseudo sélectionné
        if self.selected_pseudo:
            self._render_selected_pseudo(screen)
            self._render_achievements(screen)
            self._render_arrows_right(screen)
    
    def _render_pseudos(self, screen: pygame.Surface):
        """Affiche la liste des pseudos avec effets hover/clic."""
        visible_pseudos = self._get_visible_pseudos()
        
        for i, pseudo in enumerate(visible_pseudos):
            rect = self._get_pseudo_rect(i)
            actual_index = self.pseudo_scroll_index + i
            is_selected = (actual_index == self.selected_pseudo_index)
            is_hovered = (i == self.hovered_pseudo_index)
            is_clicked = (i == self.clicked_pseudo_index)
            
            # Choisir l'image selon l'état
            img = self.pseudo_btn_img.copy()
            
            if is_clicked:
                img.fill(self.CLICK_DARKEN, special_flags=pygame.BLEND_RGB_MULT)
            elif is_hovered:
                img.fill(self.HOVER_BRIGHTEN, special_flags=pygame.BLEND_RGB_ADD)
            
            # Surligner le pseudo sélectionné
            if is_selected:
                # Bordure ou effet visuel pour le pseudo actif
                pygame.draw.rect(screen, TextColors.SUCCESS_PSEUDO, rect.inflate(4, 4), 2, border_radius=5)
            
            screen.blit(img, rect)
            
            # Texte du pseudo
            color = TextColors.SUCCESS_PSEUDO
            text_surface = self.font_pseudo.render(pseudo, True, color)
            text_rect = text_surface.get_rect(center=rect.center)
            screen.blit(text_surface, text_rect)
    
    def _render_arrow(self, screen: pygame.Surface, arrow_name: str, img: pygame.Surface, center: Tuple[int, int]):
        """Affiche une flèche avec effets hover/clic si active."""
        if not self._is_arrow_active(arrow_name):
            # Flèche inactive : ne pas afficher ou afficher grisée
            return
        
        rect = img.get_rect(center=center)
        
        # Appliquer les effets
        if self.clicked_arrow == arrow_name:
            img_copy = img.copy()
            img_copy.fill(self.CLICK_DARKEN, special_flags=pygame.BLEND_RGB_MULT)
            screen.blit(img_copy, rect)
        elif self.hovered_arrow == arrow_name:
            img_copy = img.copy()
            img_copy.fill(self.HOVER_BRIGHTEN, special_flags=pygame.BLEND_RGB_ADD)
            screen.blit(img_copy, rect)
        else:
            screen.blit(img, rect)
    
    def _render_arrows_left(self, screen: pygame.Surface):
        """Affiche les flèches de navigation pour les pseudos."""
        self._render_arrow(screen, 'up_left', self.arrow_up_left_img, Layout.SUCCESS_ARROW_UP_LEFT)
        self._render_arrow(screen, 'down_left', self.arrow_down_left_img, Layout.SUCCESS_ARROW_DOWN_LEFT)
    
    def _render_selected_pseudo(self, screen: pygame.Surface):
        """Affiche le pseudo sélectionné en haut de la colonne droite."""
        rect = self.pseudo_user_img.get_rect(center=Layout.SUCCESS_PSEUDO_USER)
        screen.blit(self.pseudo_user_img, rect)
        
        text_surface = self.font_pseudo.render(self.selected_pseudo, True, TextColors.SUCCESS_PSEUDO)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)
    
    def _render_achievements(self, screen: pygame.Surface):
        """Affiche les succès du pseudo sélectionné."""
        visible_achievements = self._get_visible_achievements()
        
        for i, achievement in enumerate(visible_achievements):
            if i >= len(Layout.SUCCESS_CADRE_POSITIONS):
                break
            
            cadre_center_y = Layout.SUCCESS_CADRE_POSITIONS[i]
            self._render_achievement_card(screen, achievement, cadre_center_y)
    
    def _render_achievement_card(self, screen: pygame.Surface, achievement: Achievement, center_y: int):
        """Affiche une carte de succès."""
        # Choisir le cadre (or si débloqué, gris sinon)
        if achievement.unlocked:
            cadre_img = self.cadre_or_img
            name_color = TextColors.SUCCESS_NAME_UNLOCKED
            desc_color = TextColors.SUCCESS_DESC_UNLOCKED
        else:
            cadre_img = self.cadre_gris_img
            name_color = TextColors.SUCCESS_NAME_LOCKED
            desc_color = TextColors.SUCCESS_DESC_LOCKED
        
        # Afficher le cadre (centré à SUCCESS_CADRE_X, center_y)
        cadre_rect = cadre_img.get_rect(center=(Layout.SUCCESS_CADRE_X, center_y))
        screen.blit(cadre_img, cadre_rect)
        
        # Position X gauche des textes (après l'étoile)
        TEXT_LEFT = 936 # Aligné à gauche, après l'étoile
        
        # Nom du succès (taille 25px) - aligné à gauche
        name_y = center_y - 68
        name_surface = self.font_achievement_name.render(achievement.name, True, name_color)
        name_rect = name_surface.get_rect(left=TEXT_LEFT, centery=name_y)
        screen.blit(name_surface, name_rect)
        
        # Condition (taille 20px) - aligné à gauche
        condition_y = center_y - 2
        condition_text = lang_manager.get(f"achievement_conditions.{achievement.id}")
        condition_surface = self.font_achievement_condition.render(condition_text, True, TextColors.SUCCESS_CONDITION)
        condition_rect = condition_surface.get_rect(left=TEXT_LEFT, centery=condition_y)
        screen.blit(condition_surface, condition_rect)
        
        # Description (taille 20px) - aligné à gauche
        desc_y = center_y + 70
        self._render_description(screen, achievement.description, desc_color, desc_y, TEXT_LEFT)
        
        # Progression (taille 15px, à droite)
        progress_y = center_y + 103
        progress_text = self._get_progress_text(achievement)
        progress_surface = self.font_achievement_progress.render(progress_text, True, TextColors.SUCCESS_PROGRESS)
        progress_rect = progress_surface.get_rect(right=cadre_rect.right - 85, centery=progress_y)
        screen.blit(progress_surface, progress_rect)
    
    def _get_progress_text(self, achievement: Achievement) -> str:
        """Retourne le texte de progression (ex: 47/100)."""
        current = self._get_current_progress(achievement)
        target = achievement.condition_value
        return f"{current}/{target}"
    
    def _get_current_progress(self, achievement: Achievement) -> int:
        """Retourne la progression actuelle pour un succès du joueur sélectionné."""
        if not self.selected_player_data:
            return achievement.condition_value if achievement.unlocked else 0
        
        stats = self.selected_player_data.stats
        
        # Mapper les types de condition aux stats du joueur
        condition_map = {
            "total_fruits": stats.total_fruits_sliced,
            "total_combos": stats.total_combos,
            "total_ice": stats.total_ice_sliced,
            "total_games": stats.total_games_played,
            "total_explosions": stats.total_bomb_explosions,
            "mode_switches": stats.mode_switches,
            "first_launch": 0 if stats.first_launch else 1,
            "success_screen": 1 if stats.success_screen_visited else 0,
        }
        
        if achievement.condition_type in condition_map:
            return condition_map[achievement.condition_type]
        
        # Pour les succès de partie unique, afficher cible si débloqué
        if achievement.unlocked:
            return achievement.condition_value
        
        return 0
    
    def _render_description(self, screen: pygame.Surface, text: str, color, center_y: int, text_left: int = 770):
        """Affiche la description, potentiellement sur 2 lignes, alignée à gauche."""
        if "\n" in text:
            lines = text.split("\n")
        elif len(text) > 45:
            words = text.split()
            mid = len(words) // 2
            lines = [" ".join(words[:mid]), " ".join(words[mid:])]
        else:
            lines = [text]
        
        line_height = int(self.ACHIEVEMENT_DESC_SIZE * self.LINE_HEIGHT)
        total_height = line_height * len(lines)
        start_y = center_y - total_height // 2 + line_height // 2
        
        for i, line in enumerate(lines):
            line_surface = self.font_achievement_desc.render(line.strip(), True, color)
            # Aligné à gauche
            line_rect = line_surface.get_rect(left=text_left, centery=start_y + i * line_height)
            screen.blit(line_surface, line_rect)
    
    def _render_arrows_right(self, screen: pygame.Surface):
        """Affiche les flèches de navigation pour les succès."""
        self._render_arrow(screen, 'up_right', self.arrow_up_right_img, Layout.SUCCESS_ARROW_UP_RIGHT)
        self._render_arrow(screen, 'down_right', self.arrow_down_right_img, Layout.SUCCESS_ARROW_DOWN_RIGHT)
    
    def cleanup(self):
        """Nettoyage à la sortie de la scène."""
        pass
