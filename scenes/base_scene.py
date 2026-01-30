"""
BaseScene - Classe de base pour toutes les scènes du jeu
"""

import pygame
from abc import ABC, abstractmethod
from typing import List


class BaseScene(ABC):
    """
    Classe abstraite définissant l'interface commune pour toutes les scènes.
    Chaque scène doit implémenter les méthodes handle_events, update et render.
    """
    
    def __init__(self, scene_manager):
        """
        Initialise la scène.
        
        Args:
            scene_manager: Référence vers le SceneManager pour les transitions
        """
        self.scene_manager = scene_manager
    
    def setup(self):
        """
        Appelé quand la scène devient active.
        Permet d'initialiser les ressources spécifiques à la scène.
        À surcharger si nécessaire.
        """
        pass
    
    @abstractmethod
    def handle_events(self, events: List[pygame.event.Event]):
        """
        Gère les événements utilisateur (clavier, souris, etc.)
        
        Args:
            events: Liste des événements Pygame de cette frame
        """
        pass
    
    @abstractmethod
    def update(self, dt: float):
        """
        Met à jour la logique de la scène.
        
        Args:
            dt: Temps écoulé depuis la dernière frame (en secondes)
        """
        pass
    
    @abstractmethod
    def render(self, screen: pygame.Surface):
        """
        Affiche la scène à l'écran.
        
        Args:
            screen: Surface Pygame sur laquelle dessiner
        """
        pass
    
    def cleanup(self):
        """
        Appelé quand la scène devient inactive.
        Permet de libérer les ressources.
        À surcharger si nécessaire.
        """
        pass
