"""
AchievementManager - Gestionnaire des succès pour Fruit Slicer
"""

import json
import os
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum

from core import lang_manager


class AchievementCategory(Enum):
    FRUITS = "fruits"
    SCORE = "score"
    COMBOS = "combos"
    ICE = "ice"
    SURVIVAL = "survival"
    BOMBS = "bombs"
    SPECIAL = "special"


@dataclass
class Achievement:
    """Représente un succès individuel"""
    id: str
    category: str
    condition_type: str
    condition_value: int
    unlocked: bool = False
    
    @property
    def name(self) -> str:
        return lang_manager.get(f"achievement_names.{self.id}")
    
    @property
    def description(self) -> str:
        return lang_manager.get(f"achievement_descriptions.{self.id}")


@dataclass
class GameStats:
    """Statistiques d'une partie en cours"""
    score: int = 0
    fruits_sliced: int = 0
    max_combo: int = 0
    combos_count: int = 0
    ice_sliced: int = 0
    hearts_remaining: int = 3
    hearts_lost: int = 0
    bombs_avoided: int = 0
    game_time: float = 0.0
    control_mode: str = "keyboard"
    
    def reset(self):
        self.__init__()


@dataclass
class GlobalStats:
    """Statistiques globales cumulées"""
    total_fruits_sliced: int = 0
    total_games_played: int = 0
    total_combos: int = 0
    total_ice_sliced: int = 0
    total_bomb_explosions: int = 0
    total_bombs_avoided: int = 0
    mode_switches: int = 0
    success_screen_visited: bool = False
    first_launch: bool = True
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'GlobalStats':
        return cls(**data)


# Définition des succès : (id, category, condition_type, condition_value)
ACHIEVEMENTS_DATA = [
    # Fruits tranchés (cumulatif)
    ("premier_repas", AchievementCategory.FRUITS, "total_fruits", 10),
    ("appetit_croissant", AchievementCategory.FRUITS, "total_fruits", 50),
    ("glouton_vert", AchievementCategory.FRUITS, "total_fruits", 100),
    ("estomac_sans_fond", AchievementCategory.FRUITS, "total_fruits", 250),
    ("legende_ile", AchievementCategory.FRUITS, "total_fruits", 500),
    ("maitre_gourmet", AchievementCategory.FRUITS, "total_fruits", 1000),
    
    # Score en une partie
    ("bebe_yoshi", AchievementCategory.SCORE, "score", 10),
    ("yoshi_junior", AchievementCategory.SCORE, "score", 25),
    ("yoshi_confirme", AchievementCategory.SCORE, "score", 50),
    ("super_yoshi", AchievementCategory.SCORE, "score", 75),
    ("yoshi_superstar", AchievementCategory.SCORE, "score", 100),
    ("yoshi_legendaire", AchievementCategory.SCORE, "score", 150),
    
    # Combos
    ("langue_agile", AchievementCategory.COMBOS, "combo", 3),
    ("langue_eclair", AchievementCategory.COMBOS, "combo", 4),
    ("langue_divine", AchievementCategory.COMBOS, "combo", 5),
    ("combo_addict", AchievementCategory.COMBOS, "total_combos", 10),
    ("combo_master", AchievementCategory.COMBOS, "total_combos", 50),
    
    # Glaçons
    ("fraicheur_bienvenue", AchievementCategory.ICE, "ice_game", 1),
    ("maitre_givre", AchievementCategory.ICE, "total_ice", 10),
    ("roi_glace", AchievementCategory.ICE, "total_ice", 25),
    ("freeze_stratege", AchievementCategory.ICE, "ice_game", 3),
    
    # Survie
    ("coeur_intact", AchievementCategory.SURVIVAL, "no_hearts_lost", 1),
    ("prudence", AchievementCategory.SURVIVAL, "hearts_remaining", 2),
    ("survivant", AchievementCategory.SURVIVAL, "total_games", 10),
    ("perseverant", AchievementCategory.SURVIVAL, "total_games", 25),
    ("increvable", AchievementCategory.SURVIVAL, "total_games", 50),
    
    # Bombes
    ("oups", AchievementCategory.BOMBS, "exploded", 1),
    ("demineur_amateur", AchievementCategory.BOMBS, "bombs_avoided_game", 10),
    ("expert_explosifs", AchievementCategory.BOMBS, "bombs_avoided_game", 25),
    ("accident_travail", AchievementCategory.BOMBS, "total_explosions", 10),
    
    # Spéciaux
    ("bienvenue", AchievementCategory.SPECIAL, "first_launch", 1),
    ("explorateur", AchievementCategory.SPECIAL, "success_screen", 1),
    ("indecis", AchievementCategory.SPECIAL, "mode_switches", 5),
    ("speed_runner", AchievementCategory.SPECIAL, "speed_run", 20),
    ("marathon", AchievementCategory.SPECIAL, "game_time", 120),
    ("parfait", AchievementCategory.SPECIAL, "perfect", 50),
    ("virtuose_clavier", AchievementCategory.SPECIAL, "score_keyboard", 50),
    ("ninja_souris", AchievementCategory.SPECIAL, "score_mouse", 50),
]


class AchievementManager:
    """Gestionnaire principal des succès."""
    
    SAVE_FILE = "save_data.json"
    
    def __init__(self, save_path: str = None):
        self.save_path = save_path or self.SAVE_FILE
        self.achievements: Dict[str, Achievement] = {}
        self.global_stats = GlobalStats()
        self.game_stats = GameStats()
        self.pending_notifications: List[Achievement] = []
        self.on_achievement_unlocked: Optional[Callable[[Achievement], None]] = None
        
        self._init_achievements()
        self.load()
    
    def _init_achievements(self):
        for id, category, cond_type, cond_value in ACHIEVEMENTS_DATA:
            self.achievements[id] = Achievement(id, category.value, cond_type, cond_value)
    
    # ==================== SAUVEGARDE ====================
    
    def save(self):
        data = {
            "achievements": {aid: ach.unlocked for aid, ach in self.achievements.items()},
            "global_stats": self.global_stats.to_dict()
        }
        try:
            with open(self.save_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except IOError:
            pass
    
    def load(self):
        if not os.path.exists(self.save_path):
            return
        try:
            with open(self.save_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for aid, unlocked in data.get("achievements", {}).items():
                if aid in self.achievements:
                    self.achievements[aid].unlocked = unlocked
            
            if "global_stats" in data:
                self.global_stats = GlobalStats.from_dict(data["global_stats"])
        except (IOError, json.JSONDecodeError):
            pass
    
    # ==================== TRACKING ====================
    
    def start_new_game(self, control_mode: str = "keyboard"):
        self.game_stats.reset()
        self.game_stats.control_mode = control_mode
        
        if self.global_stats.first_launch:
            self.global_stats.first_launch = False
            self._unlock("bienvenue")
    
    def end_game(self, exploded: bool = False):
        gs = self.game_stats
        self.global_stats.total_fruits_sliced += gs.fruits_sliced
        self.global_stats.total_combos += gs.combos_count
        self.global_stats.total_ice_sliced += gs.ice_sliced
        self.global_stats.total_games_played += 1
        self.global_stats.total_bombs_avoided += gs.bombs_avoided
        
        if exploded:
            self.global_stats.total_bomb_explosions += 1
        
        self._check_all(exploded)
        self.save()
    
    def on_fruit_sliced(self, count: int = 1):
        self.game_stats.fruits_sliced += count
        if count >= 3:
            self.game_stats.combos_count += 1
            self.game_stats.max_combo = max(self.game_stats.max_combo, count)
            self._check_by_type("combo", count)
    
    def on_score_update(self, new_score: int):
        self.game_stats.score = new_score
        self._check_by_type("score", new_score)
        
        if new_score >= 50:
            if self.game_stats.control_mode == "keyboard":
                self._check_by_type("score_keyboard", new_score)
            else:
                self._check_by_type("score_mouse", new_score)
            
            if self.game_stats.hearts_lost == 0:
                self._check_by_type("perfect", new_score)
    
    def on_ice_sliced(self):
        self.game_stats.ice_sliced += 1
        self._check_by_type("ice_game", self.game_stats.ice_sliced)
    
    def on_heart_lost(self):
        self.game_stats.hearts_lost += 1
        self.game_stats.hearts_remaining -= 1
    
    def on_bomb_avoided(self):
        self.game_stats.bombs_avoided += 1
    
    def on_time_update(self, elapsed: float):
        self.game_stats.game_time = elapsed
        self._check_by_type("game_time", int(elapsed))
        
        if elapsed <= 30 and self.game_stats.score >= 20:
            self._unlock("speed_runner")
    
    def on_mode_switch(self):
        self.global_stats.mode_switches += 1
        self._check_by_type("mode_switches", self.global_stats.mode_switches)
        self.save()
    
    def on_success_screen_visited(self):
        if not self.global_stats.success_screen_visited:
            self.global_stats.success_screen_visited = True
            self._unlock("explorateur")
            self.save()
    
    # ==================== VÉRIFICATION ====================
    
    def _unlock(self, achievement_id: str) -> bool:
        ach = self.achievements.get(achievement_id)
        if ach and not ach.unlocked:
            ach.unlocked = True
            self.pending_notifications.append(ach)
            if self.on_achievement_unlocked:
                self.on_achievement_unlocked(ach)
            return True
        return False
    
    def _check_by_type(self, condition_type: str, value: int):
        """Vérifie et débloque tous les succès d'un type si le seuil est atteint"""
        for ach in self.achievements.values():
            if ach.condition_type == condition_type and value >= ach.condition_value:
                self._unlock(ach.id)
    
    def _check_all(self, exploded: bool):
        """Vérifie tous les succès en fin de partie"""
        gs = self.game_stats
        gstats = self.global_stats
        
        self._check_by_type("total_fruits", gstats.total_fruits_sliced)
        self._check_by_type("total_combos", gstats.total_combos)
        self._check_by_type("total_ice", gstats.total_ice_sliced)
        self._check_by_type("total_games", gstats.total_games_played)
        self._check_by_type("total_explosions", gstats.total_bomb_explosions)
        self._check_by_type("bombs_avoided_game", gs.bombs_avoided)
        
        if exploded:
            self._unlock("oups")
        
        if not exploded and gs.hearts_lost == 0:
            self._unlock("coeur_intact")
        
        if not exploded and gs.hearts_remaining >= 2:
            self._unlock("prudence")
    
    # ==================== GETTERS ====================
    
    def get_all_achievements(self) -> List[Achievement]:
        return list(self.achievements.values())
    
    def get_unlocked_achievements(self) -> List[Achievement]:
        return [a for a in self.achievements.values() if a.unlocked]
    
    def get_achievements_by_category(self, category: str) -> List[Achievement]:
        return [a for a in self.achievements.values() if a.category == category]
    
    def get_pending_notifications(self) -> List[Achievement]:
        notifs = self.pending_notifications.copy()
        self.pending_notifications.clear()
        return notifs
    
    def get_progress(self) -> dict:
        total = len(self.achievements)
        unlocked = len(self.get_unlocked_achievements())
        return {
            "total": total,
            "unlocked": unlocked,
            "percent": round((unlocked / total) * 100, 1) if total else 0
        }
