"""
AchievementManager - Gestionnaire des succès pour Fruit Slicer

Les succès sont maintenant liés au joueur courant via PlayerManager.
Ce gestionnaire ne sauvegarde plus directement, il travaille sur les données
du joueur et délègue la sauvegarde au PlayerManager.
"""

from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum

from core.lang_manager import get as lang_get


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
        return lang_get(f"achievement_names.{self.id}")
    
    @property
    def description(self) -> str:
        return lang_get(f"achievement_descriptions.{self.id}")


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
    """
    Gestionnaire principal des succès.
    
    Travaille avec le joueur courant fourni par PlayerManager.
    Ne gère pas directement la sauvegarde (délègue au PlayerManager).
    """
    
    def __init__(self):
        self.achievements: Dict[str, Achievement] = {}
        self.game_stats = GameStats()
        self.pending_notifications: List[Achievement] = []
        self.on_achievement_unlocked: Optional[Callable[[Achievement], None]] = None
        
        # Référence vers le PlayerManager (sera définie par SceneManager)
        self._player_manager = None
        
        self._init_achievements()
    
    def _init_achievements(self):
        """Initialise la liste des succès (tous verrouillés par défaut)."""
        for id, category, cond_type, cond_value in ACHIEVEMENTS_DATA:
            self.achievements[id] = Achievement(id, category.value, cond_type, cond_value)
    
    def set_player_manager(self, player_manager):
        """Définit le PlayerManager à utiliser."""
        self._player_manager = player_manager
    
    def sync_with_player(self):
        """Synchronise les succès avec les données du joueur courant."""
        if not self._player_manager or not self._player_manager.current_player:
            # Réinitialiser tous les succès si pas de joueur
            for ach in self.achievements.values():
                ach.unlocked = False
            return
        
        # Charger les succès du joueur
        player_achievements = self._player_manager.get_player_achievements()
        
        for aid, ach in self.achievements.items():
            ach.unlocked = player_achievements.get(aid, False)
    
    def _save(self):
        """Sauvegarde via le PlayerManager."""
        if self._player_manager:
            self._player_manager.save()
    
    def _get_player_stats(self):
        """Récupère les stats du joueur courant."""
        if self._player_manager:
            return self._player_manager.get_player_stats()
        return None
    
    # ==================== TRACKING ====================
    
    def start_new_game(self, control_mode: str = "keyboard"):
        """Appelé au début d'une nouvelle partie."""
        self.game_stats.reset()
        self.game_stats.control_mode = control_mode
        self.pending_notifications.clear()
        
        # Synchroniser avec le joueur courant
        self.sync_with_player()
        
        player_stats = self._get_player_stats()
        if player_stats and player_stats.first_launch:
            player_stats.first_launch = False
            self._unlock("bienvenue")
            self._save()
    
    def end_game(self, exploded: bool = False):
        """Appelé à la fin d'une partie."""
        gs = self.game_stats
        player_stats = self._get_player_stats()
        
        if not player_stats:
            return
        
        # Mettre à jour les stats cumulées du joueur
        player_stats.total_fruits_sliced += gs.fruits_sliced
        player_stats.total_combos += gs.combos_count
        player_stats.total_ice_sliced += gs.ice_sliced
        player_stats.total_games_played += 1
        player_stats.total_bombs_avoided += gs.bombs_avoided
        
        if exploded:
            player_stats.total_bomb_explosions += 1
        
        # Vérifier tous les succès
        self._check_all(exploded)
        self._save()
    
    def on_fruit_sliced(self, count: int = 1):
        """Appelé quand des fruits sont tranchés."""
        self.game_stats.fruits_sliced += count
        if count >= 3:
            self.game_stats.combos_count += 1
            self.game_stats.max_combo = max(self.game_stats.max_combo, count)
            self._check_by_type("combo", count)
    
    def on_score_update(self, new_score: int):
        """Appelé quand le score change."""
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
        """Appelé quand un glaçon est tranché."""
        self.game_stats.ice_sliced += 1
        self._check_by_type("ice_game", self.game_stats.ice_sliced)
    
    def on_heart_lost(self):
        """Appelé quand un cœur est perdu."""
        self.game_stats.hearts_lost += 1
        self.game_stats.hearts_remaining -= 1
    
    def on_bomb_avoided(self):
        """Appelé quand une bombe est évitée."""
        self.game_stats.bombs_avoided += 1
    
    def on_time_update(self, elapsed: float):
        """Appelé pour mettre à jour le temps de jeu."""
        self.game_stats.game_time = elapsed
        self._check_by_type("game_time", int(elapsed))
        
        if elapsed <= 30 and self.game_stats.score >= 20:
            self._unlock("speed_runner")
    
    def on_mode_switch(self):
        """Appelé quand le mode de contrôle change."""
        player_stats = self._get_player_stats()
        if player_stats:
            player_stats.mode_switches += 1
            self._check_by_type("mode_switches", player_stats.mode_switches)
            self._save()
    
    def on_success_screen_visited(self):
        """Appelé quand l'écran des succès est visité."""
        player_stats = self._get_player_stats()
        if player_stats and not player_stats.success_screen_visited:
            player_stats.success_screen_visited = True
            self._unlock("explorateur")
            self._save()
    
    # ==================== VÉRIFICATION ====================
    
    def _unlock(self, achievement_id: str) -> bool:
        """Débloque un succès s'il ne l'est pas déjà."""
        ach = self.achievements.get(achievement_id)
        if ach and not ach.unlocked:
            ach.unlocked = True
            self.pending_notifications.append(ach)
            
            # Sauvegarder dans les données du joueur
            if self._player_manager:
                self._player_manager.set_player_achievement(achievement_id, True)
            
            if self.on_achievement_unlocked:
                self.on_achievement_unlocked(ach)
            return True
        return False
    
    def _check_by_type(self, condition_type: str, value: int):
        """Vérifie et débloque tous les succès d'un type si le seuil est atteint."""
        for ach in self.achievements.values():
            if ach.condition_type == condition_type and value >= ach.condition_value:
                self._unlock(ach.id)
    
    def _check_all(self, exploded: bool):
        """Vérifie tous les succès en fin de partie."""
        gs = self.game_stats
        player_stats = self._get_player_stats()
        
        if not player_stats:
            return
        
        # Succès cumulatifs
        self._check_by_type("total_fruits", player_stats.total_fruits_sliced)
        self._check_by_type("total_combos", player_stats.total_combos)
        self._check_by_type("total_ice", player_stats.total_ice_sliced)
        self._check_by_type("total_games", player_stats.total_games_played)
        self._check_by_type("total_explosions", player_stats.total_bomb_explosions)
        self._check_by_type("bombs_avoided_game", gs.bombs_avoided)
        
        # Succès spéciaux
        if exploded:
            self._unlock("oups")
        
        if not exploded and gs.hearts_lost == 0:
            self._unlock("coeur_intact")
        
        if not exploded and gs.hearts_remaining >= 2:
            self._unlock("prudence")
    
    # ==================== GETTERS ====================
    
    def get_all_achievements(self) -> List[Achievement]:
        """Retourne tous les succès."""
        return list(self.achievements.values())
    
    def get_unlocked_achievements(self) -> List[Achievement]:
        """Retourne les succès débloqués."""
        return [a for a in self.achievements.values() if a.unlocked]
    
    def get_achievements_by_category(self, category: str) -> List[Achievement]:
        """Retourne les succès d'une catégorie."""
        return [a for a in self.achievements.values() if a.category == category]
    
    def get_pending_notifications(self) -> List[Achievement]:
        """Retourne et vide les notifications en attente."""
        notifs = self.pending_notifications.copy()
        self.pending_notifications.clear()
        return notifs
    
    def get_pending_count(self) -> int:
        """Retourne le nombre de notifications en attente (sans vider)."""
        return len(self.pending_notifications)
    
    def get_progress(self) -> dict:
        """Retourne la progression globale."""
        total = len(self.achievements)
        unlocked = len(self.get_unlocked_achievements())
        return {
            "total": total,
            "unlocked": unlocked,
            "percent": round((unlocked / total) * 100, 1) if total else 0
        }
