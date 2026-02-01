"""
Spawner - Génère les fruits, bombes et glaçons.

Gère :
- Le timing entre les spawns
- Les probabilités (bombe, glaçon)
- Les paires de fruits identiques (pour la jauge bonus)
- L'assignation des lettres (mode clavier)
"""

import random
from typing import List, Union

from config import WINDOW_WIDTH, WINDOW_HEIGHT, GameConfig, DIFFICULTY, KEYBOARD_LETTERS
from entities import Fruit, Bomb, Ice, create_random_fruit


Entity = Union[Fruit, Bomb, Ice]


class Spawner:
    """Génère les entités du jeu selon la difficulté."""
    
    def __init__(self, difficulty: str = 'normal'):
        self.set_difficulty(difficulty)
        self.spawn_timer = 0.0
        self.next_spawn_delay = 0.0
        self.used_letters: set = set()
        
        self._schedule_next_spawn()
    
    def set_difficulty(self, difficulty: str):
        """Change la difficulté."""
        self.difficulty = difficulty
        self.config = DIFFICULTY.get(difficulty, DIFFICULTY['normal'])
    
    def reset(self):
        """Remet le spawner à zéro."""
        self.spawn_timer = 0.0
        self.used_letters.clear()
        self._schedule_next_spawn()
    
    def _schedule_next_spawn(self):
        """Planifie le prochain spawn."""
        min_delay, max_delay = self.config['spawn_delay']
        self.next_spawn_delay = random.uniform(min_delay, max_delay)
    
    def _get_spawn_position(self) -> tuple:
        """Retourne une position de spawn (bas de la zone de jeu, centré horizontalement)."""
        # Marge sur les côtés de la zone de jeu
        zone_width = GameConfig.GAME_ZONE_SIZE[0]
        margin = zone_width * GameConfig.SPAWN_MARGIN
        
        # Position X dans la zone de jeu
        min_x = GameConfig.GAME_ZONE_LEFT + margin
        max_x = GameConfig.GAME_ZONE_RIGHT - margin - GameConfig.FRUIT_SIZE
        x = random.uniform(min_x, max_x)
        
        # Position Y : juste en dessous de la zone de jeu
        y = GameConfig.GAME_ZONE_BOTTOM
        
        return x, y
    
    def _get_velocity(self) -> tuple:
        """Retourne une vélocité initiale selon la difficulté."""
        vx_min, vx_max = self.config['speed_x']
        vy_min, vy_max = self.config['speed_y']
        
        vx = random.uniform(vx_min, vx_max)
        vy = random.uniform(vy_min, vy_max)  # Négatif = vers le haut
        
        return vx, vy
    
    def _get_gravity(self) -> float:
        """Retourne la gravité selon la difficulté."""
        return self.config['gravity']
    
    def _assign_letter(self, entity: Entity):
        """Assigne une lettre à l'entité (mode clavier)."""
        available = [l for l in KEYBOARD_LETTERS if l not in self.used_letters]
        
        if available:
            letter = random.choice(available)
            entity.letter = letter
            self.used_letters.add(letter)
        else:
            # Toutes les lettres utilisées, on en réutilise une
            entity.letter = random.choice(KEYBOARD_LETTERS)
    
    def release_letter(self, letter: str):
        """Libère une lettre quand l'entité disparaît."""
        self.used_letters.discard(letter)
    
    def _create_fruit(self, fruit_type: str = None) -> Fruit:
        """Crée un fruit."""
        x, y = self._get_spawn_position()
        vx, vy = self._get_velocity()
        gravity = self._get_gravity()
        
        if fruit_type:
            fruit = Fruit(fruit_type, x, y, vx, vy, gravity)
        else:
            fruit = create_random_fruit(x, y, vx, vy, gravity)
        
        return fruit
    
    def _create_bomb(self) -> Bomb:
        """Crée une bombe."""
        x, y = self._get_spawn_position()
        vx, vy = self._get_velocity()
        gravity = self._get_gravity()
        
        return Bomb(x, y, vx, vy, gravity)
    
    def _create_ice(self) -> Ice:
        """Crée une fleur de glace."""
        x, y = self._get_spawn_position()
        vx, vy = self._get_velocity()
        gravity = self._get_gravity()
        
        return Ice(x, y, vx, vy, gravity)
    
    def update(self, dt: float, keyboard_mode: bool = False) -> List[Entity]:
        """
        Met à jour le timer et retourne les nouvelles entités à spawner.
        """
        self.spawn_timer += dt
        
        if self.spawn_timer < self.next_spawn_delay:
            return []
        
        # Temps de spawn atteint
        self.spawn_timer = 0.0
        self._schedule_next_spawn()
        
        return self._spawn_wave(keyboard_mode)
    
    def _spawn_wave(self, keyboard_mode: bool) -> List[Entity]:
        """Génère une vague d'entités."""
        entities = []
        
        # Nombre de fruits à spawner
        min_fruits, max_fruits = self.config['fruits_per_spawn']
        num_fruits = random.randint(min_fruits, max_fruits)
        
        # Chance de paire identique (pour la jauge bonus)
        spawn_identical_pair = random.random() < GameConfig.IDENTICAL_PAIR_CHANCE
        identical_type = random.choice(GameConfig.FRUIT_TYPES) if spawn_identical_pair else None
        
        for i in range(num_fruits):
            # Décider du type d'entité
            roll = random.random()
            
            bomb_chance = self.config.get('bomb_chance', 0)
            ice_chance = self.config.get('ice_chance', 0)
            
            if roll < bomb_chance:
                entity = self._create_bomb()
            elif roll < bomb_chance + ice_chance:
                entity = self._create_ice()
            else:
                # Fruit - paire identique si applicable
                if spawn_identical_pair and i < 2:
                    entity = self._create_fruit(identical_type)
                else:
                    entity = self._create_fruit()
            
            # Assigner une lettre en mode clavier
            if keyboard_mode:
                self._assign_letter(entity)
            
            entities.append(entity)
        
        return entities
