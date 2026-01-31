"""
SceneManager - Gestionnaire des scènes du jeu.
Gère les transitions entre les écrans (menu, jeu, game over, etc.)
"""

import pygame
from typing import Dict, Optional, List

from scenes.base_scene import BaseScene


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
        
        # Données partagées entre scènes
        self.shared_data = {
            'pseudo': '',
            'difficulty': 'normal',
            'mode': 'classic',        # 'classic' ou 'challenge'
            'control_mode': 'mouse',  # 'mouse' ou 'keyboard'
            'last_score': 0,
            'is_new_record': False,
        }
        
        self._init_scenes()
        self.change_scene('menu')
    
    def _init_scenes(self):
        """Initialise toutes les scènes du jeu."""
        # Import ici pour éviter les imports circulaires
        from scenes.menu_scene import MenuScene
        
        self.scenes = {
            'menu': MenuScene(self),
            # TODO: Ajouter les autres scènes quand elles seront prêtes
            # 'player_select': PlayerSelectScene(self),
            # 'tutorial': TutorialScene(self),
            # 'game': GameScene(self),
            # 'game_over': GameOverScene(self),
            # 'settings': SettingsScene(self),
            # 'ranking': RankingScene(self),
            # 'success': SuccessScene(self),
        }
    
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
