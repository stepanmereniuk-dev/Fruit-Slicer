"""
InputHandler - Gère les entrées utilisateur (clavier et souris).

Principe d'abstraction (selon la doc) :
Le jeu ne sait pas quel mode est actif. L'InputHandler traduit
les événements en actions : "trancher ces entités".
"""

import pygame
from typing import List, Union, Tuple, Set
from collections import deque

from entities import Fruit, Bomb, Ice


Entity = Union[Fruit, Bomb, Ice]


class InputHandler:
    """
    Gère les entrées et détecte les collisions avec les entités.
    Mode souris : traînée de points, collision avec segment.
    Mode clavier : touche pressée = tranche tous les éléments avec cette lettre.
    """
    
    # Longueur max de la traînée souris
    TRAIL_LENGTH = 20
    
    def __init__(self, mode: str = "mouse"):
        self.mode = mode
        
        # Mode souris
        self.mouse_down = False
        self.mouse_trail: deque = deque(maxlen=self.TRAIL_LENGTH)
        self.last_mouse_pos: Tuple[int, int] = (0, 0)
        
        # Entités déjà tranchées dans ce tracé (pour éviter les doublons)
        self._sliced_this_stroke: Set[int] = set()
        
        # Accumulation des fruits tranchés dans le tracé actuel
        self._pending_sliced: List[Entity] = []
        
        # Mode clavier
        self.pressed_keys: set = set()
    
    def set_mode(self, mode: str):
        """Change le mode de contrôle."""
        self.mode = mode
        self.reset()
    
    def reset(self):
        """Remet l'état à zéro."""
        self.mouse_down = False
        self.mouse_trail.clear()
        self.pressed_keys.clear()
        self._sliced_this_stroke.clear()
        self._pending_sliced.clear()
    
    def handle_event(self, event: pygame.event.Event):
        """Traite un événement pygame."""
        if self.mode == "mouse":
            self._handle_mouse_event(event)
        else:
            self._handle_keyboard_event(event)
    
    def _handle_mouse_event(self, event: pygame.event.Event):
        """Gère les événements souris."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.mouse_down = True
            self.mouse_trail.clear()
            self.mouse_trail.append(event.pos)
            self.last_mouse_pos = event.pos
            self._sliced_this_stroke.clear()
        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.mouse_down = False
            self.mouse_trail.clear()
            self._sliced_this_stroke.clear()
        
        elif event.type == pygame.MOUSEMOTION and self.mouse_down:
            self.mouse_trail.append(event.pos)
            self.last_mouse_pos = event.pos
    
    def _handle_keyboard_event(self, event: pygame.event.Event):
        """Gère les événements clavier."""
        if event.type == pygame.KEYDOWN:
            key_name = pygame.key.name(event.key).upper()
            self.pressed_keys.add(key_name)
        
        elif event.type == pygame.KEYUP:
            key_name = pygame.key.name(event.key).upper()
            self.pressed_keys.discard(key_name)
    
    def get_sliced_entities(self, entities: List[Entity]) -> List[Entity]:
        """
        Retourne la liste des entités tranchées ce frame.
        C'est la méthode principale utilisée par le jeu.
        """
        if self.mode == "mouse":
            return self._get_mouse_sliced(entities)
        else:
            return self._get_keyboard_sliced(entities)
    
    def _get_mouse_sliced(self, entities: List[Entity]) -> List[Entity]:
        """Détecte les entités traversées par la traînée souris."""
        if not self.mouse_down or len(self.mouse_trail) < 2:
            return []
        
        sliced = []
        
        # Vérifier collision avec le dernier segment de la traînée
        p1 = self.mouse_trail[-2]
        p2 = self.mouse_trail[-1]
        
        # Il faut un mouvement minimum pour couper
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        if dx * dx + dy * dy < 25:  # Seuil de mouvement
            return []
        
        for entity in entities:
            if entity.sliced:
                continue
            
            # Éviter de retrancher la même entité dans ce tracé
            entity_id = id(entity)
            if entity_id in self._sliced_this_stroke:
                continue
            
            if entity.collides_with_line(p1, p2):
                sliced.append(entity)
                self._sliced_this_stroke.add(entity_id)
        
        return sliced
    
    def _get_keyboard_sliced(self, entities: List[Entity]) -> List[Entity]:
        """Détecte les entités dont la lettre a été pressée."""
        if not self.pressed_keys:
            return []
        
        sliced = []
        
        for entity in entities:
            if entity.sliced:
                continue
            if entity.letter and entity.letter in self.pressed_keys:
                sliced.append(entity)
        
        # Vider les touches pressées (une pression = une action)
        self.pressed_keys.clear()
        
        return sliced
    
    def get_trail_points(self) -> List[Tuple[int, int]]:
        """Retourne les points de la traînée pour l'affichage."""
        return list(self.mouse_trail)
    
    def is_slicing(self) -> bool:
        """Retourne True si l'utilisateur est en train de trancher."""
        return self.mouse_down if self.mode == "mouse" else bool(self.pressed_keys)
