"""
Entities - Objets du jeu (fruits, bombes, glaçons)
"""

from entities.fruit import Fruit, create_random_fruit
from entities.bomb import Bomb
from entities.ice import Ice

__all__ = ['Fruit', 'create_random_fruit', 'Bomb', 'Ice']
