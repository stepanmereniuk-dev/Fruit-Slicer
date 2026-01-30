"""
AchievementManager - Gestionnaire des succès pour Fruit Slicer (Thème Yoshi)
Jour 1 & 2 - Dev 3
"""

import json
import os
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, field, asdict
from enum import Enum


class AchievementCategory(Enum):
    """Catégories de succès"""
    FRUITS_TOTAL = "fruits_total"
    SCORE_PARTIE = "score_partie"
    COMBOS = "combos"
    GLACONS = "glacons"
    SURVIE = "survie"
    BOMBES = "bombes"
    SPECIAL = "special"


@dataclass
class Achievement:
    """Représente un succès individuel"""
    id: str
    name: str
    description: str
    category: str
    condition_type: str  # Type de condition (ex: "fruits_total_gte", "score_gte")
    condition_value: int  # Valeur seuil pour débloquer
    unlocked: bool = False
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Achievement':
        return cls(**data)


@dataclass
class GameStats:
    """Statistiques d'une partie en cours"""
    score: int = 0
    fruits_sliced: int = 0
    current_combo: int = 0
    max_combo: int = 0
    combos_count: int = 0  # Nombre de combos réalisés (3+ fruits)
    ice_sliced: int = 0
    hearts_remaining: int = 3
    bombs_avoided: int = 0
    game_time: float = 0.0
    control_mode: str = "keyboard"  # "keyboard" ou "mouse"
    hearts_lost: int = 0
    
    def reset(self):
        """Réinitialise les stats pour une nouvelle partie"""
        self.score = 0
        self.fruits_sliced = 0
        self.current_combo = 0
        self.max_combo = 0
        self.combos_count = 0
        self.ice_sliced = 0
        self.hearts_remaining = 3
        self.bombs_avoided = 0
        self.game_time = 0.0
        self.hearts_lost = 0


@dataclass
class GlobalStats:
    """Statistiques globales (cumulées entre toutes les parties)"""
    total_fruits_sliced: int = 0
    total_games_played: int = 0
    total_combos: int = 0
    total_ice_sliced: int = 0
    total_bomb_explosions: int = 0
    total_bombs_avoided: int = 0
    mode_switches: int = 0  # Pour le succès "Indécis"
    success_screen_visited: bool = False  # Pour le succès "Explorateur"
    first_launch: bool = True  # Pour le succès "Bienvenue !"
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'GlobalStats':
        return cls(**data)


class AchievementManager:
    """
    Gestionnaire principal des succès.
    Responsabilités:
    - Charger/sauvegarder les succès
    - Vérifier les conditions de déblocage
    - Déclencher les notifications
    - Maintenir les statistiques
    """
    
    SAVE_FILE = "save_data.json"
    
    def __init__(self, save_path: str = None):
        self.save_path = save_path or self.SAVE_FILE
        self.achievements: Dict[str, Achievement] = {}
        self.global_stats = GlobalStats()
        self.current_game_stats = GameStats()
        self.pending_notifications: List[Achievement] = []
        self.on_achievement_unlocked: Optional[Callable[[Achievement], None]] = None
        
        self._init_achievements()
        self.load()
    
    def _init_achievements(self):
        """Initialise la liste complète des succès"""
        achievements_data = [
            # === SUCCÈS LIÉS AU NOMBRE DE FRUITS TRANCHÉS (CUMULATIF) ===
            Achievement(
                id="premier_repas",
                name="Premier Repas",
                description="Yoshi a goûté à ses premiers fruits !",
                category=AchievementCategory.FRUITS_TOTAL.value,
                condition_type="total_fruits_gte",
                condition_value=10
            ),
            Achievement(
                id="appetit_croissant",
                name="Appétit Croissant",
                description="Yoshi commence à avoir faim...",
                category=AchievementCategory.FRUITS_TOTAL.value,
                condition_type="total_fruits_gte",
                condition_value=50
            ),
            Achievement(
                id="glouton_vert",
                name="Glouton Vert",
                description="Yoshi ne peut plus s'arrêter de manger !",
                category=AchievementCategory.FRUITS_TOTAL.value,
                condition_type="total_fruits_gte",
                condition_value=100
            ),
            Achievement(
                id="estomac_sans_fond",
                name="Estomac Sans Fond",
                description="Rien ne semble rassasier Yoshi !",
                category=AchievementCategory.FRUITS_TOTAL.value,
                condition_type="total_fruits_gte",
                condition_value=250
            ),
            Achievement(
                id="legende_ile",
                name="Légende de l'Île",
                description="Yoshi est devenu une légende de Yoshi's Island !",
                category=AchievementCategory.FRUITS_TOTAL.value,
                condition_type="total_fruits_gte",
                condition_value=500
            ),
            Achievement(
                id="maitre_gourmet",
                name="Maître Gourmet",
                description="Yoshi a atteint le nirvana culinaire !",
                category=AchievementCategory.FRUITS_TOTAL.value,
                condition_type="total_fruits_gte",
                condition_value=1000
            ),
            
            # === SUCCÈS LIÉS AU SCORE EN UNE PARTIE ===
            Achievement(
                id="bebe_yoshi",
                name="Bébé Yoshi",
                description="Premiers pas dans l'aventure !",
                category=AchievementCategory.SCORE_PARTIE.value,
                condition_type="score_gte",
                condition_value=10
            ),
            Achievement(
                id="yoshi_junior",
                name="Yoshi Junior",
                description="Yoshi grandit et s'améliore !",
                category=AchievementCategory.SCORE_PARTIE.value,
                condition_type="score_gte",
                condition_value=25
            ),
            Achievement(
                id="yoshi_confirme",
                name="Yoshi Confirmé",
                description="Yoshi maîtrise l'art du festin !",
                category=AchievementCategory.SCORE_PARTIE.value,
                condition_type="score_gte",
                condition_value=50
            ),
            Achievement(
                id="super_yoshi",
                name="Super Yoshi",
                description="Yoshi entre dans la cour des grands !",
                category=AchievementCategory.SCORE_PARTIE.value,
                condition_type="score_gte",
                condition_value=75
            ),
            Achievement(
                id="yoshi_superstar",
                name="Yoshi Superstar",
                description="Yoshi brille comme une étoile !",
                category=AchievementCategory.SCORE_PARTIE.value,
                condition_type="score_gte",
                condition_value=100
            ),
            Achievement(
                id="yoshi_legendaire",
                name="Yoshi Légendaire",
                description="Yoshi est entré dans la légende !",
                category=AchievementCategory.SCORE_PARTIE.value,
                condition_type="score_gte",
                condition_value=150
            ),
            
            # === SUCCÈS LIÉS AUX COMBOS ===
            Achievement(
                id="langue_agile",
                name="Langue Agile",
                description="Yoshi attrape plusieurs fruits d'un coup !",
                category=AchievementCategory.COMBOS.value,
                condition_type="combo_gte",
                condition_value=3
            ),
            Achievement(
                id="langue_eclair",
                name="Langue Éclair",
                description="La langue de Yoshi est plus rapide que l'éclair !",
                category=AchievementCategory.COMBOS.value,
                condition_type="combo_gte",
                condition_value=4
            ),
            Achievement(
                id="langue_divine",
                name="Langue Divine",
                description="Personne n'a jamais vu une langue aussi rapide !",
                category=AchievementCategory.COMBOS.value,
                condition_type="combo_gte",
                condition_value=5
            ),
            Achievement(
                id="combo_addict",
                name="Combo Addict",
                description="Yoshi ne jure plus que par les combos !",
                category=AchievementCategory.COMBOS.value,
                condition_type="total_combos_gte",
                condition_value=10
            ),
            Achievement(
                id="combo_master",
                name="Combo Master",
                description="Yoshi est devenu maître dans l'art du combo !",
                category=AchievementCategory.COMBOS.value,
                condition_type="total_combos_gte",
                condition_value=50
            ),
            
            # === SUCCÈS LIÉS AUX GLAÇONS ===
            Achievement(
                id="fraicheur_bienvenue",
                name="Fraîcheur Bienvenue",
                description="Yoshi découvre le pouvoir du froid !",
                category=AchievementCategory.GLACONS.value,
                condition_type="ice_sliced_gte",
                condition_value=1
            ),
            Achievement(
                id="maitre_givre",
                name="Maître du Givre",
                description="Yoshi contrôle le temps comme un pro !",
                category=AchievementCategory.GLACONS.value,
                condition_type="total_ice_gte",
                condition_value=10
            ),
            Achievement(
                id="roi_glace",
                name="Roi de la Glace",
                description="Yoshi règne sur le royaume gelé !",
                category=AchievementCategory.GLACONS.value,
                condition_type="total_ice_gte",
                condition_value=25
            ),
            Achievement(
                id="freeze_stratege",
                name="Freeze Stratège",
                description="Yoshi utilise le freeze à la perfection !",
                category=AchievementCategory.GLACONS.value,
                condition_type="ice_in_game_gte",
                condition_value=3
            ),
            
            # === SUCCÈS LIÉS À LA SURVIE ===
            Achievement(
                id="coeur_intact",
                name="Cœur Intact",
                description="Yoshi n'a pas eu une seule indigestion !",
                category=AchievementCategory.SURVIE.value,
                condition_type="no_hearts_lost",
                condition_value=1
            ),
            Achievement(
                id="prudence",
                name="Prudence est Mère de Sûreté",
                description="Yoshi sait prendre soin de lui !",
                category=AchievementCategory.SURVIE.value,
                condition_type="hearts_remaining_gte",
                condition_value=2
            ),
            Achievement(
                id="survivant",
                name="Survivant",
                description="Yoshi ne lâche jamais !",
                category=AchievementCategory.SURVIE.value,
                condition_type="games_played_gte",
                condition_value=10
            ),
            Achievement(
                id="perseverant",
                name="Persévérant",
                description="Yoshi revient toujours pour plus !",
                category=AchievementCategory.SURVIE.value,
                condition_type="games_played_gte",
                condition_value=25
            ),
            Achievement(
                id="increvable",
                name="Increvable",
                description="Rien ne peut arrêter Yoshi !",
                category=AchievementCategory.SURVIE.value,
                condition_type="games_played_gte",
                condition_value=50
            ),
            
            # === SUCCÈS LIÉS AUX BOMBES ===
            Achievement(
                id="oups",
                name="Oups...",
                description="Yoshi a fait connaissance avec Bob-omb...",
                category=AchievementCategory.BOMBES.value,
                condition_type="exploded_once",
                condition_value=1
            ),
            Achievement(
                id="demineur_amateur",
                name="Démineur Amateur",
                description="Yoshi sait reconnaître le danger !",
                category=AchievementCategory.BOMBES.value,
                condition_type="bombs_avoided_in_game_gte",
                condition_value=10
            ),
            Achievement(
                id="expert_explosifs",
                name="Expert en Explosifs",
                description="Les Bob-ombs ne font plus peur à Yoshi !",
                category=AchievementCategory.BOMBES.value,
                condition_type="bombs_avoided_in_game_gte",
                condition_value=25
            ),
            Achievement(
                id="accident_travail",
                name="Accident de Travail",
                description="Yoshi n'apprend pas de ses erreurs...",
                category=AchievementCategory.BOMBES.value,
                condition_type="total_explosions_gte",
                condition_value=10
            ),
            
            # === SUCCÈS SPÉCIAUX ===
            Achievement(
                id="bienvenue",
                name="Bienvenue !",
                description="Yoshi vous souhaite la bienvenue !",
                category=AchievementCategory.SPECIAL.value,
                condition_type="first_launch",
                condition_value=1
            ),
            Achievement(
                id="explorateur",
                name="Explorateur",
                description="Yoshi aime regarder ses trophées !",
                category=AchievementCategory.SPECIAL.value,
                condition_type="visited_success_screen",
                condition_value=1
            ),
            Achievement(
                id="indecis",
                name="Indécis",
                description="Clavier ? Souris ? Yoshi hésite...",
                category=AchievementCategory.SPECIAL.value,
                condition_type="mode_switches_gte",
                condition_value=5
            ),
            Achievement(
                id="speed_runner",
                name="Speed Runner",
                description="Yoshi mange à la vitesse de la lumière !",
                category=AchievementCategory.SPECIAL.value,
                condition_type="score_in_time",
                condition_value=20  # 20 points en moins de 30 secondes
            ),
            Achievement(
                id="marathon",
                name="Marathon",
                description="Yoshi a de l'endurance !",
                category=AchievementCategory.SPECIAL.value,
                condition_type="game_time_gte",
                condition_value=120  # 2 minutes
            ),
            Achievement(
                id="parfait",
                name="Parfait",
                description="Une partie parfaite pour Yoshi !",
                category=AchievementCategory.SPECIAL.value,
                condition_type="perfect_game",
                condition_value=50  # 50 points sans perdre de cœur
            ),
            Achievement(
                id="virtuose_clavier",
                name="Virtuose du Clavier",
                description="Les doigts de feu au service de Yoshi !",
                category=AchievementCategory.SPECIAL.value,
                condition_type="score_with_mode",
                condition_value=50  # 50 points en mode clavier
            ),
            Achievement(
                id="ninja_souris",
                name="Ninja de la souris",
                description="Un vrai ninja du slice !",
                category=AchievementCategory.SPECIAL.value,
                condition_type="score_with_mouse",
                condition_value=50  # 50 points en mode souris
            ),
        ]
        
        for achievement in achievements_data:
            self.achievements[achievement.id] = achievement
    
    # ==================== SAUVEGARDE / CHARGEMENT ====================
    
    def save(self):
        """Sauvegarde les succès et statistiques dans un fichier JSON"""
        data = {
            "achievements": {
                aid: ach.to_dict() for aid, ach in self.achievements.items()
            },
            "global_stats": self.global_stats.to_dict()
        }
        
        try:
            with open(self.save_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Erreur lors de la sauvegarde: {e}")
    
    def load(self):
        """Charge les succès et statistiques depuis le fichier JSON"""
        if not os.path.exists(self.save_path):
            return
        
        try:
            with open(self.save_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Charger les états des succès (uniquement unlocked)
            if "achievements" in data:
                for aid, ach_data in data["achievements"].items():
                    if aid in self.achievements:
                        self.achievements[aid].unlocked = ach_data.get("unlocked", False)
            
            # Charger les stats globales
            if "global_stats" in data:
                self.global_stats = GlobalStats.from_dict(data["global_stats"])
                
        except (IOError, json.JSONDecodeError) as e:
            print(f"Erreur lors du chargement: {e}")
    
    # ==================== TRACKING DES STATS ====================
    
    def start_new_game(self, control_mode: str = "keyboard"):
        """Appelé au début d'une nouvelle partie"""
        self.current_game_stats.reset()
        self.current_game_stats.control_mode = control_mode
        
        # Vérifier le succès "Bienvenue !"
        if self.global_stats.first_launch:
            self.global_stats.first_launch = False
            self._check_and_unlock("bienvenue")
    
    def end_game(self, exploded: bool = False):
        """Appelé à la fin d'une partie"""
        stats = self.current_game_stats
        
        # Mettre à jour les stats globales
        self.global_stats.total_fruits_sliced += stats.fruits_sliced
        self.global_stats.total_combos += stats.combos_count
        self.global_stats.total_ice_sliced += stats.ice_sliced
        self.global_stats.total_games_played += 1
        self.global_stats.total_bombs_avoided += stats.bombs_avoided
        
        if exploded:
            self.global_stats.total_bomb_explosions += 1
        
        # Vérifier tous les succès de fin de partie
        self._check_all_achievements(exploded)
        
        # Sauvegarder
        self.save()
    
    def on_fruit_sliced(self, count: int = 1):
        """Appelé quand un ou plusieurs fruits sont tranchés"""
        self.current_game_stats.fruits_sliced += count
        
        # Gestion des combos
        if count >= 3:
            self.current_game_stats.combos_count += 1
            self.current_game_stats.current_combo = count
            if count > self.current_game_stats.max_combo:
                self.current_game_stats.max_combo = count
            
            # Vérifier succès combo immédiatement
            self._check_combo_achievements(count)
    
    def on_score_update(self, new_score: int):
        """Appelé quand le score change"""
        self.current_game_stats.score = new_score
        
        # Vérifier succès de score en temps réel
        self._check_score_achievements()
    
    def on_ice_sliced(self):
        """Appelé quand un glaçon est tranché"""
        self.current_game_stats.ice_sliced += 1
        
        # Vérifier succès glaçon immédiat
        self._check_and_unlock("fraicheur_bienvenue")
        
        if self.current_game_stats.ice_sliced >= 3:
            self._check_and_unlock("freeze_stratege")
    
    def on_heart_lost(self):
        """Appelé quand un cœur est perdu"""
        self.current_game_stats.hearts_lost += 1
        self.current_game_stats.hearts_remaining -= 1
    
    def on_bomb_avoided(self):
        """Appelé quand une bombe sort de l'écran sans être touchée"""
        self.current_game_stats.bombs_avoided += 1
    
    def on_time_update(self, elapsed_time: float):
        """Appelé pour mettre à jour le temps de jeu"""
        self.current_game_stats.game_time = elapsed_time
        
        # Vérifier succès Speed Runner
        if elapsed_time <= 30 and self.current_game_stats.score >= 20:
            self._check_and_unlock("speed_runner")
        
        # Vérifier succès Marathon
        if elapsed_time >= 120:
            self._check_and_unlock("marathon")
    
    def on_mode_switch(self):
        """Appelé quand le joueur change de mode de contrôle"""
        self.global_stats.mode_switches += 1
        
        if self.global_stats.mode_switches >= 5:
            self._check_and_unlock("indecis")
        
        self.save()
    
    def on_success_screen_visited(self):
        """Appelé quand le joueur visite l'écran des succès"""
        if not self.global_stats.success_screen_visited:
            self.global_stats.success_screen_visited = True
            self._check_and_unlock("explorateur")
            self.save()
    
    # ==================== VÉRIFICATION DES SUCCÈS ====================
    
    def _check_and_unlock(self, achievement_id: str) -> bool:
        """Débloque un succès s'il ne l'est pas déjà"""
        if achievement_id not in self.achievements:
            return False
        
        achievement = self.achievements[achievement_id]
        if not achievement.unlocked:
            achievement.unlocked = True
            self.pending_notifications.append(achievement)
            
            if self.on_achievement_unlocked:
                self.on_achievement_unlocked(achievement)
            
            return True
        return False
    
    def _check_combo_achievements(self, combo_size: int):
        """Vérifie les succès liés aux combos"""
        if combo_size >= 3:
            self._check_and_unlock("langue_agile")
        if combo_size >= 4:
            self._check_and_unlock("langue_eclair")
        if combo_size >= 5:
            self._check_and_unlock("langue_divine")
    
    def _check_score_achievements(self):
        """Vérifie les succès liés au score"""
        score = self.current_game_stats.score
        
        if score >= 10:
            self._check_and_unlock("bebe_yoshi")
        if score >= 25:
            self._check_and_unlock("yoshi_junior")
        if score >= 50:
            self._check_and_unlock("yoshi_confirme")
            
            # Vérifier succès mode spécifique
            if self.current_game_stats.control_mode == "keyboard":
                self._check_and_unlock("virtuose_clavier")
            elif self.current_game_stats.control_mode == "mouse":
                self._check_and_unlock("ninja_souris")
            
            # Vérifier succès Parfait
            if self.current_game_stats.hearts_lost == 0:
                self._check_and_unlock("parfait")
        
        if score >= 75:
            self._check_and_unlock("super_yoshi")
        if score >= 100:
            self._check_and_unlock("yoshi_superstar")
        if score >= 150:
            self._check_and_unlock("yoshi_legendaire")
    
    def _check_all_achievements(self, exploded: bool):
        """Vérifie tous les succès en fin de partie"""
        stats = self.current_game_stats
        gstats = self.global_stats
        
        # Succès fruits totaux
        if gstats.total_fruits_sliced >= 10:
            self._check_and_unlock("premier_repas")
        if gstats.total_fruits_sliced >= 50:
            self._check_and_unlock("appetit_croissant")
        if gstats.total_fruits_sliced >= 100:
            self._check_and_unlock("glouton_vert")
        if gstats.total_fruits_sliced >= 250:
            self._check_and_unlock("estomac_sans_fond")
        if gstats.total_fruits_sliced >= 500:
            self._check_and_unlock("legende_ile")
        if gstats.total_fruits_sliced >= 1000:
            self._check_and_unlock("maitre_gourmet")
        
        # Succès combos totaux
        if gstats.total_combos >= 10:
            self._check_and_unlock("combo_addict")
        if gstats.total_combos >= 50:
            self._check_and_unlock("combo_master")
        
        # Succès glaçons totaux
        if gstats.total_ice_sliced >= 10:
            self._check_and_unlock("maitre_givre")
        if gstats.total_ice_sliced >= 25:
            self._check_and_unlock("roi_glace")
        
        # Succès survie
        if stats.hearts_lost == 0 and not exploded:
            self._check_and_unlock("coeur_intact")
        if stats.hearts_remaining >= 2 and not exploded:
            self._check_and_unlock("prudence")
        
        # Succès parties jouées
        if gstats.total_games_played >= 10:
            self._check_and_unlock("survivant")
        if gstats.total_games_played >= 25:
            self._check_and_unlock("perseverant")
        if gstats.total_games_played >= 50:
            self._check_and_unlock("increvable")
        
        # Succès bombes
        if exploded:
            self._check_and_unlock("oups")
        if gstats.total_bomb_explosions >= 10:
            self._check_and_unlock("accident_travail")
        if stats.bombs_avoided >= 10:
            self._check_and_unlock("demineur_amateur")
        if stats.bombs_avoided >= 25:
            self._check_and_unlock("expert_explosifs")
    
    # ==================== GETTERS ====================
    
    def get_all_achievements(self) -> List[Achievement]:
        """Retourne la liste de tous les succès"""
        return list(self.achievements.values())
    
    def get_unlocked_achievements(self) -> List[Achievement]:
        """Retourne la liste des succès débloqués"""
        return [a for a in self.achievements.values() if a.unlocked]
    
    def get_locked_achievements(self) -> List[Achievement]:
        """Retourne la liste des succès verrouillés"""
        return [a for a in self.achievements.values() if not a.unlocked]
    
    def get_achievements_by_category(self, category: str) -> List[Achievement]:
        """Retourne les succès d'une catégorie donnée"""
        return [a for a in self.achievements.values() if a.category == category]
    
    def get_pending_notifications(self) -> List[Achievement]:
        """Récupère et vide la liste des notifications en attente"""
        notifications = self.pending_notifications.copy()
        self.pending_notifications.clear()
        return notifications
    
    def get_progress_stats(self) -> dict:
        """Retourne les statistiques de progression"""
        total = len(self.achievements)
        unlocked = len(self.get_unlocked_achievements())
        
        return {
            "total_achievements": total,
            "unlocked_achievements": unlocked,
            "completion_percentage": round((unlocked / total) * 100, 1) if total > 0 else 0,
            "global_stats": self.global_stats.to_dict(),
            "current_game_stats": {
                "score": self.current_game_stats.score,
                "fruits_sliced": self.current_game_stats.fruits_sliced,
                "max_combo": self.current_game_stats.max_combo,
                "ice_sliced": self.current_game_stats.ice_sliced,
                "hearts_remaining": self.current_game_stats.hearts_remaining,
                "game_time": self.current_game_stats.game_time
            }
        }


# ==================== EXEMPLE D'UTILISATION ====================

if __name__ == "__main__":
    # Test du gestionnaire
    manager = AchievementManager("test_save.json")
    
    # Simuler une partie
    print("=== Démarrage d'une nouvelle partie ===")
    manager.start_new_game("keyboard")
    
    # Simuler quelques actions
    manager.on_fruit_sliced(1)
    manager.on_score_update(1)
    
    manager.on_fruit_sliced(3)  # Combo de 3
    manager.on_score_update(4)
    
    manager.on_ice_sliced()
    
    manager.on_fruit_sliced(5)  # Combo de 5
    manager.on_score_update(9)
    
    # Simuler plus de fruits pour atteindre 10 points
    manager.on_fruit_sliced(1)
    manager.on_score_update(10)
    
    manager.on_time_update(25)  # 25 secondes
    
    # Fin de partie
    manager.end_game(exploded=False)
    
    # Afficher les résultats
    print("\n=== Succès débloqués ===")
    for ach in manager.get_unlocked_achievements():
        print(f"  ✓ {ach.name}: {ach.description}")
    
    print("\n=== Statistiques ===")
    stats = manager.get_progress_stats()
    print(f"  Progression: {stats['unlocked_achievements']}/{stats['total_achievements']} ({stats['completion_percentage']}%)")
    print(f"  Fruits totaux: {stats['global_stats']['total_fruits_sliced']}")
    print(f"  Parties jouées: {stats['global_stats']['total_games_played']}")
    
    # Nettoyer le fichier de test
    if os.path.exists("test_save.json"):
        os.remove("test_save.json")
