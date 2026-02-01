"""
SceneManager - Gestionnaire des scènes du jeu.
Gère les transitions entre les écrans (menu, jeu, game over, etc.)
"""

import pygame
from typing import Dict, Optional, List

from scenes.base_scene import BaseScene
from core.achievements import AchievementManager
from core.player_manager import PlayerManager
from core.settings_manager import SettingsManager


class SceneManager:
    """
    Orchestre les différentes scènes du jeu.
    Une seule scène est active à la fois.
    """
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.scenes: Dict[str, BaseScene] = {}
        self.current_scene: Optional[BaseScene] = None
        self.current_scene_name: str = ""
        
        # Gestionnaires partagés
        self.achievement_manager = AchievementManager()
        self.player_manager = PlayerManager()
        self.settings_manager = SettingsManager()
        
        # Données partagées entre scènes
        self.shared_data = {
            'pseudo': '',
            'difficulty': 'normal',
            'mode': 'classic',        # 'classic' ou 'challenge'
            'control_mode': self.settings_manager.control_mode,
            'last_score': 0,
            'is_new_record': False,
        }
        
        self._init_scenes()
        self.change_scene('menu')
    
    def _init_scenes(self):
        """Initialise toutes les scènes du jeu."""
        # Import ici pour éviter les imports circulaires
        from scenes.menu_scene import MenuScene
        from scenes.game_scene import GameScene
        from scenes.player_select_scene import PlayerSelectScene
        from scenes.tutorial_scene import TutorialScene
        
        self.scenes = {
            'menu': MenuScene(self),
            'game': GameScene(self),
            'player_select': PlayerSelectScene(self),
            'tutorial': TutorialScene(self),
            # TODO: Ajouter les autres scènes quand elles seront prêtes
            # 'game_over': GameOverScene(self),
            # 'settings': SettingsScene(self),
            # 'ranking': RankingScene(self),
            # 'success': SuccessScene(self),
        }
        
        # Passer le gestionnaire de succès aux scènes qui en ont besoin
        self.scenes['game'].set_achievement_manager(self.achievement_manager)
        
        # Passer le gestionnaire de joueurs aux scènes qui en ont besoin
        self.scenes['player_select'].set_player_manager(self.player_manager)
        self.scenes['tutorial'].set_player_manager(self.player_manager)
    
    def change_scene(self, scene_name: str):
        """
        Change la scène active.
        Appelle cleanup() sur l'ancienne et setup() sur la nouvelle.
        """
        if scene_name not in self.scenes:
            print(f"Scène inconnue: {scene_name}")
            return
        
        # Nettoyage de la scène actuelle
        if self.current_scene:
            self.current_scene.cleanup()
        
        # Activation de la nouvelle scène
        self.current_scene = self.scenes[scene_name]
        self.current_scene_name = scene_name
        self.current_scene.setup()
    
    def handle_events(self, events: List[pygame.event.Event]):
        """Transmet les événements à la scène active."""
        if self.current_scene:
            self.current_scene.handle_events(events)
    
    def update(self, dt: float):
        """Met à jour la scène active."""
        if self.current_scene:
            self.current_scene.update(dt)
    
    def render(self):
        """Affiche la scène active."""
        if self.current_scene:
            self.current_scene.render(self.screen)
    
    def quit_game(self):
        """Ferme le jeu proprement."""
        pygame.event.post(pygame.event.Event(pygame.QUIT))
