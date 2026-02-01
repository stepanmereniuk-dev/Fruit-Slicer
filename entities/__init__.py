"""
Entities - Objets du jeu (fruits, bombes, glaçons, éclaboussures)
"""

from entities.fruit import Fruit, create_random_fruit
from entities.bomb import Bomb
from entities.ice import Ice
from entities.splash import Splash

__all__ = ['Fruit', 'create_random_fruit', 'Bomb', 'Ice', 'Splash']
