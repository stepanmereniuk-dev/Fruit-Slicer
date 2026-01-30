"""
SuccessScene - Écran d'affichage des succès
Jour 3 - Dev 3

Affiche tous les succès sous forme de grille :
- Succès débloqués : en couleur avec nom et description
- Succès verrouillés : en grisé avec point d'interrogation
"""

import pygame
from typing import List, Optional
from scenes.base_scene import BaseScene
from core.achievements import AchievementManager, Achievement, AchievementCategory


# Couleurs thème Mario/Yoshi
COLORS = {
    'background': (129, 212, 250),      # Bleu ciel #81D4FA
    'primary': (124, 179, 66),          # Vert Yoshi #7CB342
    'secondary': (229, 57, 53),         # Rouge Mario #E53935
    'accent': (255, 213, 79),           # Jaune pièces #FFD54F
    'white': (255, 255, 255),           # Blanc nuages
    'black': (33, 33, 33),              # Noir Bob-omb #212121
    'gold': (255, 193, 7),              # Or étoile #FFC107
    'gray': (158, 158, 158),            # Gris verrouillé #9E9E9E
    'gray_dark': (97, 97, 97),          # Gris foncé
    'card_unlocked': (255, 255, 255),   # Fond carte débloquée
    'card_locked': (200, 200, 200),     # Fond carte verrouillée
}


class SuccessScene(BaseScene):
    """
    Scène affichant tous les succès du jeu.
    """
    
    def __init__(self, scene_manager):
        super().__init__(scene_manager)
        self.achievement_manager: Optional[AchievementManager] = None
        
        # Configuration de la grille
        self.cards_per_row = 3
        self.card_width = 220
        self.card_height = 120
        self.card_margin = 15
        self.grid_start_y = 120
        
        # Scroll
        self.scroll_y = 0
        self.max_scroll = 0
        self.scroll_speed = 30
        
        # Catégorie sélectionnée (None = toutes)
        self.selected_category: Optional[str] = None
        self.categories = [
            (None, "Tous"),
            (AchievementCategory.FRUITS_TOTAL.value, "Fruits"),
            (AchievementCategory.SCORE_PARTIE.value, "Score"),
            (AchievementCategory.COMBOS.value, "Combos"),
            (AchievementCategory.GLACONS.value, "Glaçons"),
            (AchievementCategory.SURVIE.value, "Survie"),
            (AchievementCategory.BOMBES.value, "Bombes"),
            (AchievementCategory.SPECIAL.value, "Spéciaux"),
        ]
        
        # Bouton retour
        self.back_button_rect = pygame.Rect(20, 20, 100, 40)
        
        # Fonts (seront initialisées dans setup)
        self.font_title = None
        self.font_card_title = None
        self.font_card_desc = None
        self.font_button = None
        self.font_stats = None
    
    def set_achievement_manager(self, manager: AchievementManager):
        """Définit le gestionnaire de succès"""
        self.achievement_manager = manager
    
    def setup(self):
        """Initialise les ressources de la scène"""
        # Initialiser les fonts
        pygame.font.init()
        self.font_title = pygame.font.Font(None, 48)
        self.font_card_title = pygame.font.Font(None, 24)
        self.font_card_desc = pygame.font.Font(None, 18)
        self.font_button = pygame.font.Font(None, 28)
        self.font_stats = pygame.font.Font(None, 32)
        
        # Calculer le scroll maximum
        self._calculate_max_scroll()
        
        # Notifier le manager qu'on visite l'écran des succès
        if self.achievement_manager:
            self.achievement_manager.on_success_screen_visited()
    
    def _calculate_max_scroll(self):
        """Calcule la hauteur maximale de scroll"""
        achievements = self._get_filtered_achievements()
        rows = (len(achievements) + self.cards_per_row - 1) // self.cards_per_row
        content_height = self.grid_start_y + rows * (self.card_height + self.card_margin) + 50
        screen_height = pygame.display.get_surface().get_height()
        self.max_scroll = max(0, content_height - screen_height)
    
    def _get_filtered_achievements(self) -> List[Achievement]:
        """Retourne les succès filtrés par catégorie"""
        if not self.achievement_manager:
            return []
        
        if self.selected_category is None:
            return self.achievement_manager.get_all_achievements()
        else:
            return self.achievement_manager.get_achievements_by_category(self.selected_category)
    
    def handle_events(self, events: List[pygame.event.Event]):
        """Gère les événements utilisateur"""
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # Bouton retour
                if self.back_button_rect.collidepoint(mouse_pos):
                    self.scene_manager.change_scene('menu')
                    return
                
                # Boutons de catégorie
                self._handle_category_click(mouse_pos)
                
                # Scroll avec molette
            elif event.type == pygame.MOUSEWHEEL:
                self.scroll_y -= event.y * self.scroll_speed
                self.scroll_y = max(0, min(self.scroll_y, self.max_scroll))
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.scene_manager.change_scene('menu')
                elif event.key == pygame.K_UP:
                    self.scroll_y = max(0, self.scroll_y - self.scroll_speed)
                elif event.key == pygame.K_DOWN:
                    self.scroll_y = min(self.max_scroll, self.scroll_y + self.scroll_speed)
    
    def _handle_category_click(self, mouse_pos):
        """Gère le clic sur les boutons de catégorie"""
        screen = pygame.display.get_surface()
        screen_width = screen.get_width()
        
        # Position des boutons de catégorie
        button_y = 70
        button_width = 80
        button_height = 30
        button_margin = 5
        total_width = len(self.categories) * (button_width + button_margin) - button_margin
        start_x = (screen_width - total_width) // 2
        
        for i, (cat_value, cat_name) in enumerate(self.categories):
            button_x = start_x + i * (button_width + button_margin)
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            
            if button_rect.collidepoint(mouse_pos):
                self.selected_category = cat_value
                self.scroll_y = 0
                self._calculate_max_scroll()
                return
    
    def update(self, dt: float):
        """Met à jour la logique de la scène"""
        pass  # Pas d'animation particulière pour l'instant
    
    def render(self, screen: pygame.Surface):
        """Affiche la scène"""
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        
        # Fond
        screen.fill(COLORS['background'])
        
        # Titre
        title_text = self.font_title.render("Succès de Yoshi", True, COLORS['primary'])
        title_rect = title_text.get_rect(centerx=screen_width // 2, top=20)
        screen.blit(title_text, title_rect)
        
        # Statistiques de progression
        self._render_progress_stats(screen, screen_width)
        
        # Boutons de catégorie
        self._render_category_buttons(screen, screen_width)
        
        # Grille de succès
        self._render_achievements_grid(screen, screen_width, screen_height)
        
        # Bouton retour
        self._render_back_button(screen)
    
    def _render_progress_stats(self, screen: pygame.Surface, screen_width: int):
        """Affiche les statistiques de progression"""
        if not self.achievement_manager:
            return
        
        stats = self.achievement_manager.get_progress_stats()
        unlocked = stats['unlocked_achievements']
        total = stats['total_achievements']
        percentage = stats['completion_percentage']
        
        # Barre de progression
        bar_width = 300
        bar_height = 20
        bar_x = (screen_width - bar_width) // 2
        bar_y = 45
        
        # Fond de la barre
        pygame.draw.rect(screen, COLORS['gray'], (bar_x, bar_y, bar_width, bar_height), border_radius=10)
        
        # Progression
        fill_width = int(bar_width * (percentage / 100))
        if fill_width > 0:
            pygame.draw.rect(screen, COLORS['gold'], (bar_x, bar_y, fill_width, bar_height), border_radius=10)
        
        # Contour
        pygame.draw.rect(screen, COLORS['black'], (bar_x, bar_y, bar_width, bar_height), 2, border_radius=10)
        
        # Texte
        progress_text = self.font_card_title.render(f"{unlocked}/{total} ({percentage}%)", True, COLORS['black'])
        progress_rect = progress_text.get_rect(centerx=screen_width // 2, centery=bar_y + bar_height // 2)
        screen.blit(progress_text, progress_rect)
    
    def _render_category_buttons(self, screen: pygame.Surface, screen_width: int):
        """Affiche les boutons de filtrage par catégorie"""
        button_y = 75
        button_width = 80
        button_height = 30
        button_margin = 5
        total_width = len(self.categories) * (button_width + button_margin) - button_margin
        start_x = (screen_width - total_width) // 2
        
        for i, (cat_value, cat_name) in enumerate(self.categories):
            button_x = start_x + i * (button_width + button_margin)
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            
            # Couleur selon sélection
            if cat_value == self.selected_category:
                bg_color = COLORS['primary']
                text_color = COLORS['white']
            else:
                bg_color = COLORS['white']
                text_color = COLORS['black']
            
            # Dessiner le bouton
            pygame.draw.rect(screen, bg_color, button_rect, border_radius=5)
            pygame.draw.rect(screen, COLORS['black'], button_rect, 2, border_radius=5)
            
            # Texte
            text = self.font_card_desc.render(cat_name, True, text_color)
            text_rect = text.get_rect(center=button_rect.center)
            screen.blit(text, text_rect)
    
    def _render_achievements_grid(self, screen: pygame.Surface, screen_width: int, screen_height: int):
        """Affiche la grille de succès"""
        achievements = self._get_filtered_achievements()
        
        if not achievements:
            # Message si aucun succès
            no_ach_text = self.font_card_title.render("Aucun succès dans cette catégorie", True, COLORS['gray_dark'])
            no_ach_rect = no_ach_text.get_rect(centerx=screen_width // 2, centery=screen_height // 2)
            screen.blit(no_ach_text, no_ach_rect)
            return
        
        # Calculer la position de départ de la grille
        total_grid_width = self.cards_per_row * self.card_width + (self.cards_per_row - 1) * self.card_margin
        grid_start_x = (screen_width - total_grid_width) // 2
        
        # Zone de clip pour le scroll
        clip_rect = pygame.Rect(0, self.grid_start_y, screen_width, screen_height - self.grid_start_y)
        screen.set_clip(clip_rect)
        
        for i, achievement in enumerate(achievements):
            row = i // self.cards_per_row
            col = i % self.cards_per_row
            
            card_x = grid_start_x + col * (self.card_width + self.card_margin)
            card_y = self.grid_start_y + row * (self.card_height + self.card_margin) - self.scroll_y
            
            # Ne dessiner que si visible
            if card_y + self.card_height > self.grid_start_y and card_y < screen_height:
                self._render_achievement_card(screen, achievement, card_x, card_y)
        
        # Réinitialiser le clip
        screen.set_clip(None)
    
    def _render_achievement_card(self, screen: pygame.Surface, achievement: Achievement, x: int, y: int):
        """Affiche une carte de succès"""
        card_rect = pygame.Rect(x, y, self.card_width, self.card_height)
        
        if achievement.unlocked:
            # Carte débloquée
            bg_color = COLORS['card_unlocked']
            border_color = COLORS['gold']
            title_color = COLORS['primary']
            desc_color = COLORS['black']
            icon_color = COLORS['gold']
        else:
            # Carte verrouillée
            bg_color = COLORS['card_locked']
            border_color = COLORS['gray']
            title_color = COLORS['gray_dark']
            desc_color = COLORS['gray_dark']
            icon_color = COLORS['gray']
        
        # Fond de la carte
        pygame.draw.rect(screen, bg_color, card_rect, border_radius=10)
        pygame.draw.rect(screen, border_color, card_rect, 3, border_radius=10)
        
        # Icône étoile
        star_x = x + 20
        star_y = y + 25
        self._draw_star(screen, star_x, star_y, 15, icon_color)
        
        # Titre
        if achievement.unlocked:
            title_text = achievement.name
        else:
            title_text = "???"
        
        title_surface = self.font_card_title.render(title_text, True, title_color)
        # Tronquer si trop long
        max_title_width = self.card_width - 60
        if title_surface.get_width() > max_title_width:
            # Tronquer le texte
            while title_surface.get_width() > max_title_width and len(title_text) > 3:
                title_text = title_text[:-4] + "..."
                title_surface = self.font_card_title.render(title_text, True, title_color)
        
        screen.blit(title_surface, (x + 45, y + 15))
        
        # Description (avec retour à la ligne)
        if achievement.unlocked:
            desc_text = achievement.description
        else:
            desc_text = "Succès verrouillé"
        
        self._render_wrapped_text(screen, desc_text, x + 15, y + 45, 
                                  self.card_width - 30, self.font_card_desc, desc_color)
    
    def _render_wrapped_text(self, screen: pygame.Surface, text: str, x: int, y: int, 
                             max_width: int, font: pygame.font.Font, color):
        """Affiche du texte avec retour à la ligne automatique"""
        words = text.split(' ')
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " "
            test_surface = font.render(test_line, True, color)
            
            if test_surface.get_width() <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "
        
        if current_line:
            lines.append(current_line.strip())
        
        # Limiter à 3 lignes max
        lines = lines[:3]
        
        for i, line in enumerate(lines):
            line_surface = font.render(line, True, color)
            screen.blit(line_surface, (x, y + i * 18))
    
    def _draw_star(self, screen: pygame.Surface, cx: int, cy: int, size: int, color):
        """Dessine une étoile à 5 branches"""
        import math
        points = []
        for i in range(10):
            angle = math.pi / 2 + i * math.pi / 5
            if i % 2 == 0:
                r = size
            else:
                r = size * 0.4
            px = cx + r * math.cos(angle)
            py = cy - r * math.sin(angle)
            points.append((px, py))
        
        pygame.draw.polygon(screen, color, points)
        pygame.draw.polygon(screen, COLORS['black'], points, 2)
    
    def _render_back_button(self, screen: pygame.Surface):
        """Affiche le bouton retour"""
        # Fond du bouton
        pygame.draw.rect(screen, COLORS['secondary'], self.back_button_rect, border_radius=5)
        pygame.draw.rect(screen, COLORS['black'], self.back_button_rect, 2, border_radius=5)
        
        # Texte
        text = self.font_button.render("← Retour", True, COLORS['white'])
        text_rect = text.get_rect(center=self.back_button_rect.center)
        screen.blit(text, text_rect)
    
    def cleanup(self):
        """Nettoie les ressources de la scène"""
        pass
