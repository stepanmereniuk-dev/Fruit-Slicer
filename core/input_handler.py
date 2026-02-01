"""
InputHandler - Handles user inputs (keyboard and mouse).

Abstraction principle (according to the doc):
The game does not know which mode is active. The InputHandler translates
events into actions: "slice these entities".
"""

import pygame
from typing import List, Union, Tuple, Set
from collections import deque

from entities import Fruit, Bomb, Ice


Entity = Union[Fruit, Bomb, Ice]


class InputHandler:
    """
    Handles inputs and detects collisions with entities.
    Mouse mode: trail of points, collision with line segment.
    Keyboard mode: pressed key = slice all elements with that letter.
    """
    
    # Maximum length of the mouse trail
    TRAIL_LENGTH = 20
    
    def __init__(self, mode: str = "mouse"):
        self.mode = mode
        
        # Mouse mode
        self.mouse_down = False
        self.mouse_trail: deque = deque(maxlen=self.TRAIL_LENGTH)
        self.last_mouse_pos: Tuple[int, int] = (0, 0)
        
        # Entities already sliced in this stroke (to avoid duplicates)
        self._sliced_this_stroke: Set[int] = set()
        
        # Accumulation of fruits sliced in the current stroke
        self._pending_sliced: List[Entity] = []
        
        # Keyboard mode
        self.pressed_keys: set = set()
    
    def set_mode(self, mode: str):
        """Change the control mode."""
        self.mode = mode
        self.reset()
    
    def reset(self):
        """Reset the state to initial values."""
        self.mouse_down = False
        self.mouse_trail.clear()
        self.pressed_keys.clear()
        self._sliced_this_stroke.clear()
        self._pending_sliced.clear()
    
    def handle_event(self, event: pygame.event.Event):
        """Process a pygame event."""
        if self.mode == "mouse":
            self._handle_mouse_event(event)
        else:
            self._handle_keyboard_event(event)
    
    def _handle_mouse_event(self, event: pygame.event.Event):
        """Handle mouse events."""
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
        """Handle keyboard events."""
        if event.type == pygame.KEYDOWN:
            key_name = pygame.key.name(event.key).upper()
            self.pressed_keys.add(key_name)
        
        elif event.type == pygame.KEYUP:
            key_name = pygame.key.name(event.key).upper()
            self.pressed_keys.discard(key_name)
    
    def get_sliced_entities(self, entities: List[Entity]) -> List[Entity]:
        """
        Returns the list of entities sliced this frame.
        This is the main method used by the game.
        """
        if self.mode == "mouse":
            return self._get_mouse_sliced(entities)
        else:
            return self._get_keyboard_sliced(entities)
    
    def _get_mouse_sliced(self, entities: List[Entity]) -> List[Entity]:
        """Detect entities intersected by the mouse trail."""
        if not self.mouse_down or len(self.mouse_trail) < 2:
            return []
        
        sliced = []
        
        # Check collision with the last segment of the trail
        p1 = self.mouse_trail[-2]
        p2 = self.mouse_trail[-1]
        
        # A minimum movement is required to slice
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        if dx * dx + dy * dy < 25:  # Movement threshold
            return []
        
        for entity in entities:
            if entity.sliced:
                continue
            
            # Avoid re-slicing the same entity in this stroke
            entity_id = id(entity)
            if entity_id in self._sliced_this_stroke:
                continue
            
            if entity.collides_with_line(p1, p2):
                sliced.append(entity)
                self._sliced_this_stroke.add(entity_id)
        
        return sliced
    
    def _get_keyboard_sliced(self, entities: List[Entity]) -> List[Entity]:
        """Detect entities whose letter key was pressed."""
        if not self.pressed_keys:
            return []
        
        sliced = []
        
        for entity in entities:
            if entity.sliced:
                continue
            if entity.letter and entity.letter in self.pressed_keys:
                sliced.append(entity)
        
        # Clear pressed keys (one press = one action)
        self.pressed_keys.clear()
        
        return sliced
    
    def get_trail_points(self) -> List[Tuple[int, int]]:
        """Returns the trail points for rendering."""
        return list(self.mouse_trail)
    
    def is_slicing(self) -> bool:
        """Returns True if the user is currently slicing."""
        return self.mouse_down if self.mode == "mouse" else bool(self.pressed_keys)