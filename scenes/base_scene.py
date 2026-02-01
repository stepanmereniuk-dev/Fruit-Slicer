"""
BaseScene - Base class for all game scenes
"""

import pygame
from abc import ABC, abstractmethod
from typing import List


class BaseScene(ABC):
    """
    Abstract class defining the common interface for all scenes.
    Each scene must implement the methods handle_events, update, and render.
    """
    
    def __init__(self, scene_manager):
        """
        Initializes the scene.
        
        Args:
            scene_manager: Reference to the SceneManager for transitions
        """
        self.scene_manager = scene_manager
    
    def setup(self):
        """
        Called when the scene becomes active.
        Allows initializing scene-specific resources.
        Override if necessary.
        """
        pass
    
    @abstractmethod
    def handle_events(self, events: List[pygame.event.Event]):
        """
        Handles user events (keyboard, mouse, etc.)
        
        Args:
            events: List of Pygame events for this frame
        """
        pass
    
    @abstractmethod
    def update(self, dt: float):
        """
        Updates the scene logic.
        
        Args:
            dt: Time elapsed since the last frame (in seconds)
        """
        pass
    
    @abstractmethod
    def render(self, screen: pygame.Surface):
        """
        Renders the scene to the screen.
        
        Args:
            screen: Pygame surface to draw on
        """
        pass
    
    def cleanup(self):
        """
        Called when the scene becomes inactive.
        Allows releasing resources.
        Override if necessary.
        """
        pass