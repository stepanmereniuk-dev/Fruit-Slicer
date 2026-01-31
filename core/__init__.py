"""
Module core - Logique métier du jeu Fruit Slicer
"""

from . import lang_manager
from .achievements import AchievementManager, Achievement, GameStats, GlobalStats, AchievementCategory
from .scoring import ScoringManager, BonusGauge
from .spawner import Spawner
from .input_handler import InputHandler
