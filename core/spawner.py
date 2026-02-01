"""
Spawner - Generates fruits, bombs, and ice flowers.

Handles:
- Timing between spawns
- Probabilities (bomb, ice flower)
- Identical fruit pairs (for the bonus gauge)
- Letter assignment (keyboard mode)
"""

import random
from typing import List, Union

from config import WINDOW_WIDTH, WINDOW_HEIGHT, GameConfig, DIFFICULTY, KEYBOARD_LETTERS
from entities import Fruit, Bomb, Ice, create_random_fruit


Entity = Union[Fruit, Bomb, Ice]


class Spawner:
    """Generates game entities according to difficulty."""
    
    def __init__(self, difficulty: str = 'normal'):
        self.set_difficulty(difficulty)
        self.spawn_timer = 0.0
        self.next_spawn_delay = 0.0
        self.used_letters: set = set()
        
        self._schedule_next_spawn()
    
    def set_difficulty(self, difficulty: str):
        """Changes the difficulty."""
        self.difficulty = difficulty
        self.config = DIFFICULTY.get(difficulty, DIFFICULTY['normal'])
    
    def reset(self):
        """Resets the spawner."""
        self.spawn_timer = 0.0
        self.used_letters.clear()
        self._schedule_next_spawn()
    
    def _schedule_next_spawn(self):
        """Schedules the next spawn."""
        min_delay, max_delay = self.config['spawn_delay']
        self.next_spawn_delay = random.uniform(min_delay, max_delay)
    
    def _get_spawn_position(self) -> tuple:
        """Returns a spawn position (bottom of game zone, horizontally centered)."""
        # Margin on sides of game zone
        zone_width = GameConfig.GAME_ZONE_SIZE[0]
        margin = zone_width * GameConfig.SPAWN_MARGIN
        
        # X position within game zone
        min_x = GameConfig.GAME_ZONE_LEFT + margin
        max_x = GameConfig.GAME_ZONE_RIGHT - margin - GameConfig.FRUIT_SIZE
        x = random.uniform(min_x, max_x)
        
        # Y position: just below game zone
        y = GameConfig.GAME_ZONE_BOTTOM
        
        return x, y
    
    def _get_velocity(self) -> tuple:
        """Returns initial velocity according to difficulty."""
        vx_min, vx_max = self.config['speed_x']
        vy_min, vy_max = self.config['speed_y']
        
        vx = random.uniform(vx_min, vx_max)
        vy = random.uniform(vy_min, vy_max)  # Negative = upward
        
        return vx, vy
    
    def _get_gravity(self) -> float:
        """Returns gravity according to difficulty."""
        return self.config['gravity']
    
    def _assign_letter(self, entity: Entity):
        """Assigns a letter to the entity (keyboard mode)."""
        available = [l for l in KEYBOARD_LETTERS if l not in self.used_letters]
        
        if available:
            letter = random.choice(available)
            entity.letter = letter
            self.used_letters.add(letter)
        else:
            # All letters used, reuse one
            entity.letter = random.choice(KEYBOARD_LETTERS)
    
    def release_letter(self, letter: str):
        """Releases a letter when the entity disappears."""
        self.used_letters.discard(letter)
    
    def _create_fruit(self, fruit_type: str = None) -> Fruit:
        """Creates a fruit."""
        x, y = self._get_spawn_position()
        vx, vy = self._get_velocity()
        gravity = self._get_gravity()
        
        if fruit_type:
            fruit = Fruit(fruit_type, x, y, vx, vy, gravity)
        else:
            fruit = create_random_fruit(x, y, vx, vy, gravity)
        
        return fruit
    
    def _create_bomb(self) -> Bomb:
        """Creates a bomb."""
        x, y = self._get_spawn_position()
        vx, vy = self._get_velocity()
        gravity = self._get_gravity()
        
        return Bomb(x, y, vx, vy, gravity)
    
    def _create_ice(self) -> Ice:
        """Creates an ice flower."""
        x, y = self._get_spawn_position()
        vx, vy = self._get_velocity()
        gravity = self._get_gravity()
        
        return Ice(x, y, vx, vy, gravity)
    
    def update(self, dt: float, keyboard_mode: bool = False) -> List[Entity]:
        """
        Updates the timer and returns new entities to spawn.
        """
        self.spawn_timer += dt
        
        if self.spawn_timer < self.next_spawn_delay:
            return []
        
        # Spawn time reached
        self.spawn_timer = 0.0
        self._schedule_next_spawn()
        
        return self._spawn_wave(keyboard_mode)
    
    def _spawn_wave(self, keyboard_mode: bool) -> List[Entity]:
        """Generates a wave of entities."""
        entities = []
        
        # Number of fruits to spawn
        min_fruits, max_fruits = self.config['fruits_per_spawn']
        num_fruits = random.randint(min_fruits, max_fruits)
        
        # Chance of identical pair (for bonus gauge)
        spawn_identical_pair = random.random() < GameConfig.IDENTICAL_PAIR_CHANCE
        identical_type = random.choice(GameConfig.FRUIT_TYPES) if spawn_identical_pair else None
        
        for i in range(num_fruits):
            # Decide entity type
            roll = random.random()
            
            bomb_chance = self.config.get('bomb_chance', 0)
            ice_chance = self.config.get('ice_chance', 0)
            
            if roll < bomb_chance:
                entity = self._create_bomb()
            elif roll < bomb_chance + ice_chance:
                entity = self._create_ice()
            else:
                # Fruit - identical pair if applicable
                if spawn_identical_pair and i < 2:
                    entity = self._create_fruit(identical_type)
                else:
                    entity = self._create_fruit()
            
            # Assign letter in keyboard mode
            if keyboard_mode:
                self._assign_letter(entity)
            
            entities.append(entity)
        
        return entities