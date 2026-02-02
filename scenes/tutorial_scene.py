"""
TutorialScene - Écran de tutoriel pour les nouveaux joueurs.

Tutoriel Classic (6 écrans) :
1. Objectif du jeu
2. Les contrôles
3. Les cœurs et strikes
4. Les bombes
5. Les glaçons
6. Combos et jauge bonus

Tutoriel Challenge (4 écrans) :
1. Objectif du jeu
2. Les contrôles
3. Le timer et les bombes
4. Combos et jauge bonus
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
    """Scène du tutoriel - adapté selon le mode (classic ou challenge)."""
    
    # Tailles de police
    TITLE_FONT_SIZE = 36
    TEXT_FONT_SIZE = 30
    BUTTON_FONT_SIZE = 30
    
    # Interligne pour les textes sur 2 lignes
    LINE_HEIGHT = 1.4
    
    def __init__(self, scene_manager):
        super().__init__(scene_manager)
        
        # Ressources
        self.background = None
        self.font_title = None
        self.font_text = None
        self.font_button = None
        
        # Images des blocs
        self.blocks: List[pygame.Surface] = []
        
        # Boutons
        self.btn_prev: Optional[Button] = None
        self.btn_next: Optional[Button] = None
        self.btn_play: Optional[Button] = None
        
        # État
        self.mode = 'classic'  # 'classic' ou 'challenge'
        self.current_screen = 0
        self.total_screens = 6
        self.from_settings = False  # True si on vient des paramètres
        
        # Player manager
        self.player_manager: Optional[PlayerManager] = None
    
    def setup(self):
        """Initialise la scène selon le mode."""
        # Récupérer le mode
        self.mode = self.scene_manager.shared_data.get('mode', 'classic')
        self.current_screen = 0
        
        # Savoir si on vient des paramètres
        self.from_settings = self.scene_manager.shared_data.get('tutorial_from_settings', False)
        
        # Nombre d'écrans selon le mode
        if self.mode == 'challenge':
            self.total_screens = 4
        else:
            self.total_screens = 6
        
        # Charger les ressources
        self._load_resources()
        
        # Créer les boutons pour l'écran actuel
        self._setup_buttons()
    
    def _load_resources(self):
        """Charge les images et polices."""
        # Polices
        font_path = os.path.join(FONTS_DIR, FONT_FILE)
        self.font_title = pygame.font.Font(font_path, self.TITLE_FONT_SIZE)
        self.font_text = pygame.font.Font(font_path, self.TEXT_FONT_SIZE)
        self.font_button = pygame.font.Font(font_path, self.BUTTON_FONT_SIZE)
        
        # Background (un seul par mode)
        if self.mode == 'challenge':
            bg_path = os.path.join(IMAGES_DIR, Images.TUTO_CHALLENGE_BG)
        else:
            bg_path = os.path.join(IMAGES_DIR, Images.TUTO_CLASSIC_BG)
        self.background = pygame.image.load(bg_path).convert()
        
        # Charger tous les blocs
        self.blocks = []
        if self.mode == 'challenge':
            block_paths = Images.TUTO_CHALLENGE_BLOCKS
        else:
            block_paths = Images.TUTO_CLASSIC_BLOCKS
        
        for path in block_paths:
            img = pygame.image.load(os.path.join(IMAGES_DIR, path)).convert_alpha()
            self.blocks.append(img)
    
    def _setup_buttons(self):
        """Configure les boutons pour l'écran actuel."""
        screen = self.current_screen
        
        # Récupérer les chemins selon le mode
        if self.mode == 'challenge':
            prev_paths = Images.TUTO_CHALLENGE_BTN_PREV
            next_paths = Images.TUTO_CHALLENGE_BTN_NEXT
            play_path = Images.TUTO_CHALLENGE_BTN_PLAY
        else:
            prev_paths = Images.TUTO_CLASSIC_BTN_PREV
            next_paths = Images.TUTO_CLASSIC_BTN_NEXT
            play_path = Images.TUTO_CLASSIC_BTN_PLAY
        
        # Bouton Précédent (sauf écran 1)
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
        
        # Bouton Suivant ou Jouer/Quitter
        is_last_screen = screen == self.total_screens - 1
        
        if is_last_screen:
            # Dernier écran : bouton Jouer ou Quitter selon d'où on vient
            self.btn_next = None
            
            # Texte différent si on vient des paramètres
            if self.from_settings:
                btn_text = lang_manager.get("general.quit")  # "Quitter"
            else:
                btn_text = lang_manager.get("tutorial.play")  # "Jouer"
            
            self.btn_play = Button(
                image_path=play_path,
                center=Layout.TUTO_BTN_PLAY,
                text=btn_text,
                text_color=TextColors.TUTO_PLAY,
                on_click=self._on_play
            )
        else:
            # Autres écrans : bouton Suivant
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
        """Définit le gestionnaire de joueurs."""
        self.player_manager = manager
    
    # Callbacks
    def _on_previous(self):
        """Écran précédent."""
        if self.current_screen > 0:
            self.current_screen -= 1
            self._setup_buttons()
    
    def _on_next(self):
        """Écran suivant."""
        if self.current_screen < self.total_screens - 1:
            self.current_screen += 1
            self._setup_buttons()
    
    def _on_play(self):
        """Lance le jeu ou retourne aux paramètres."""
        # Marquer le tutoriel comme vu
        if self.player_manager:
            self.player_manager.mark_tutorial_seen()
        
        # Retourner aux paramètres ou lancer le jeu
        if self.from_settings:
            # Reset le flag
            self.scene_manager.shared_data['tutorial_from_settings'] = False
            self.scene_manager.change_scene('settings')
        else:
            self.scene_manager.change_scene('game')
    
    def handle_events(self, events: List[pygame.event.Event]):
        for event in events:
            # Boutons
            if self.btn_prev:
                self.btn_prev.handle_event(event)
            if self.btn_next:
                self.btn_next.handle_event(event)
            if self.btn_play:
                self.btn_play.handle_event(event)
            
            # Raccourcis clavier
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
                    # Retour au menu ou aux paramètres selon d'où on vient
                    if self.from_settings:
                        self.scene_manager.shared_data['tutorial_from_settings'] = False
                        self.scene_manager.change_scene('settings')
                    else:
                        self.scene_manager.change_scene('menu')
    
    def update(self, dt: float):
        pass
    
    def render(self, screen: pygame.Surface):
        """Affiche la scène."""
        # Fond
        screen.blit(self.background, (0, 0))
        
        # Bloc central
        block_img = self.blocks[self.current_screen]
        block_rect = block_img.get_rect(center=Layout.TUTO_BLOCK)
        screen.blit(block_img, block_rect)
        
        # Titre
        self._render_title(screen)
        
        # Texte
        self._render_text(screen)
        
        # Boutons
        if self.btn_prev:
            self.btn_prev.render(screen, self.font_button)
        if self.btn_next:
            self.btn_next.render(screen, self.font_button)
        if self.btn_play:
            self.btn_play.render(screen, self.font_button)
    
    def _render_title(self, screen: pygame.Surface):
        """Affiche le titre de l'écran."""
        # Clé de traduction selon le mode et l'écran
        if self.mode == 'challenge':
            title_key = f"tutorial.challenge.screen{self.current_screen + 1}.title"
        else:
            title_key = f"tutorial.classic.screen{self.current_screen + 1}.title"
        
        title_text = lang_manager.get(title_key)
        title_surface = self.font_title.render(title_text, True, TextColors.TUTO_TITLE)
        title_rect = title_surface.get_rect(center=Layout.TUTO_TITLE)
        screen.blit(title_surface, title_rect)
    
    def _render_text(self, screen: pygame.Surface):
        """Affiche le texte de l'écran (peut être sur 2 lignes)."""
        # Clé de traduction
        if self.mode == 'challenge':
            text_key = f"tutorial.challenge.screen{self.current_screen + 1}.text"
        else:
            text_key = f"tutorial.classic.screen{self.current_screen + 1}.text"
        
        full_text = lang_manager.get(text_key)
        
        # Vérifier si le texte contient un retour à la ligne
        if "\n" in full_text:
            lines = full_text.split("\n")
            self._render_multiline_text(screen, lines)
        else:
            # Une seule ligne
            text_surface = self.font_text.render(full_text, True, TextColors.TUTO_TEXT)
            text_rect = text_surface.get_rect(center=Layout.TUTO_TEXT)
            screen.blit(text_surface, text_rect)
    
    def _render_multiline_text(self, screen: pygame.Surface, lines: List[str]):
        """Affiche du texte sur plusieurs lignes avec interligne."""
        line_height = int(self.TEXT_FONT_SIZE * self.LINE_HEIGHT)
        total_height = line_height * len(lines)
        
        # Position de départ (centré verticalement autour de TUTO_TEXT)
        start_y = Layout.TUTO_TEXT[1] - total_height // 2 + line_height // 2
        
        for i, line in enumerate(lines):
            text_surface = self.font_text.render(line.strip(), True, TextColors.TUTO_TEXT)
            text_rect = text_surface.get_rect(
                centerx=Layout.TUTO_TEXT[0],
                centery=start_y + i * line_height
            )
            screen.blit(text_surface, text_rect)
    
    def cleanup(self):
        """Nettoyage à la sortie de la scène."""
        # Reset le flag si on quitte autrement (Échap par exemple)
        self.scene_manager.shared_data['tutorial_from_settings'] = False
