"""
Script de test et vérification des succès
Jour 4 - Dev 3

Ce script permet de :
- Tester tous les succès
- Vérifier que les conditions fonctionnent
- Simuler des parties complètes
- Générer un rapport de test
"""

import os
import sys
import json
from typing import List, Tuple

# Ajouter le dossier parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.achievements import AchievementManager, Achievement, AchievementCategory


class AchievementTester:
    """Testeur automatique du système de succès"""
    
    def __init__(self):
        self.test_save_file = "test_achievements_save.json"
        self.results: List[Tuple[str, bool, str]] = []  # (test_name, passed, details)
    
    def cleanup(self):
        """Supprime le fichier de sauvegarde de test"""
        if os.path.exists(self.test_save_file):
            os.remove(self.test_save_file)
    
    def log_result(self, test_name: str, passed: bool, details: str = ""):
        """Enregistre un résultat de test"""
        self.results.append((test_name, passed, details))
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status}: {test_name}")
        if details and not passed:
            print(f"         {details}")
    
    def run_all_tests(self):
        """Exécute tous les tests"""
        print("\n" + "="*60)
        print("TESTS DU SYSTÈME DE SUCCÈS - FRUIT SLICER")
        print("="*60 + "\n")
        
        # Nettoyer avant les tests
        self.cleanup()
        
        # Tests
        self.test_initialization()
        self.test_save_load()
        self.test_fruit_achievements()
        self.test_score_achievements()
        self.test_combo_achievements()
        self.test_ice_achievements()
        self.test_survival_achievements()
        self.test_bomb_achievements()
        self.test_special_achievements()
        self.test_full_game_simulation()
        
        # Nettoyer après les tests
        self.cleanup()
        
        # Rapport final
        self.print_report()
    
    def test_initialization(self):
        """Test l'initialisation du manager"""
        print("\n[Test Initialisation]")
        
        manager = AchievementManager(self.test_save_file)
        
        # Vérifier le nombre de succès
        all_achievements = manager.get_all_achievements()
        expected_count = 38
        self.log_result(
            f"Nombre de succès ({expected_count} attendus)",
            len(all_achievements) == expected_count,
            f"Trouvé: {len(all_achievements)}"
        )
        
        # Vérifier qu'aucun n'est débloqué au départ
        unlocked = manager.get_unlocked_achievements()
        self.log_result(
            "Aucun succès débloqué au départ",
            len(unlocked) == 0,
            f"Trouvé: {len(unlocked)} débloqués"
        )
        
        # Vérifier les catégories
        categories = set(a.category for a in all_achievements)
        expected_categories = {c.value for c in AchievementCategory}
        self.log_result(
            "Toutes les catégories présentes",
            categories == expected_categories,
            f"Manquantes: {expected_categories - categories}"
        )
        
        self.cleanup()
    
    def test_save_load(self):
        """Test la sauvegarde et le chargement"""
        print("\n[Test Sauvegarde/Chargement]")
        
        # Créer et modifier
        manager1 = AchievementManager(self.test_save_file)
        manager1.start_new_game("keyboard")
        
        # Simuler pour débloquer quelques succès
        for _ in range(15):
            manager1.on_fruit_sliced(1)
        manager1.on_score_update(15)
        manager1.end_game(False)
        
        unlocked_before = len(manager1.get_unlocked_achievements())
        
        # Recharger depuis le fichier
        manager2 = AchievementManager(self.test_save_file)
        unlocked_after = len(manager2.get_unlocked_achievements())
        
        self.log_result(
            "Succès persistés après rechargement",
            unlocked_before == unlocked_after and unlocked_after > 0,
            f"Avant: {unlocked_before}, Après: {unlocked_after}"
        )
        
        # Vérifier les stats globales
        self.log_result(
            "Stats globales persistées",
            manager2.global_stats.total_fruits_sliced == 15,
            f"Fruits: {manager2.global_stats.total_fruits_sliced}"
        )
        
        self.cleanup()
    
    def test_fruit_achievements(self):
        """Test les succès liés aux fruits"""
        print("\n[Test Succès Fruits]")
        
        manager = AchievementManager(self.test_save_file)
        
        # Simuler plusieurs parties pour accumuler des fruits
        total_fruits = 0
        thresholds = [(10, "premier_repas"), (50, "appetit_croissant"), (100, "glouton_vert")]
        
        for threshold, achievement_id in thresholds:
            while total_fruits < threshold:
                manager.start_new_game("keyboard")
                fruits_this_game = min(20, threshold - total_fruits)
                for _ in range(fruits_this_game):
                    manager.on_fruit_sliced(1)
                total_fruits += fruits_this_game
                manager.end_game(False)
            
            is_unlocked = manager.achievements[achievement_id].unlocked
            self.log_result(
                f"'{manager.achievements[achievement_id].name}' débloqué à {threshold} fruits",
                is_unlocked,
                f"Total: {manager.global_stats.total_fruits_sliced}"
            )
        
        self.cleanup()
    
    def test_score_achievements(self):
        """Test les succès liés au score"""
        print("\n[Test Succès Score]")
        
        manager = AchievementManager(self.test_save_file)
        
        scores_to_test = [
            (10, "bebe_yoshi"),
            (25, "yoshi_junior"),
            (50, "yoshi_confirme"),
            (75, "super_yoshi"),
            (100, "yoshi_superstar"),
        ]
        
        for score, achievement_id in scores_to_test:
            manager.start_new_game("keyboard")
            manager.on_score_update(score)
            manager.end_game(False)
            
            is_unlocked = manager.achievements[achievement_id].unlocked
            self.log_result(
                f"'{manager.achievements[achievement_id].name}' débloqué à {score} points",
                is_unlocked
            )
        
        self.cleanup()
    
    def test_combo_achievements(self):
        """Test les succès liés aux combos"""
        print("\n[Test Succès Combos]")
        
        manager = AchievementManager(self.test_save_file)
        manager.start_new_game("keyboard")
        
        # Combo de 3
        manager.on_fruit_sliced(3)
        self.log_result(
            "'Langue Agile' débloqué (combo 3)",
            manager.achievements["langue_agile"].unlocked
        )
        
        # Combo de 4
        manager.on_fruit_sliced(4)
        self.log_result(
            "'Langue Éclair' débloqué (combo 4)",
            manager.achievements["langue_eclair"].unlocked
        )
        
        # Combo de 5
        manager.on_fruit_sliced(5)
        self.log_result(
            "'Langue Divine' débloqué (combo 5+)",
            manager.achievements["langue_divine"].unlocked
        )
        
        manager.end_game(False)
        self.cleanup()
    
    def test_ice_achievements(self):
        """Test les succès liés aux glaçons"""
        print("\n[Test Succès Glaçons]")
        
        manager = AchievementManager(self.test_save_file)
        manager.start_new_game("keyboard")
        
        # Premier glaçon
        manager.on_ice_sliced()
        self.log_result(
            "'Fraîcheur Bienvenue' débloqué (1 glaçon)",
            manager.achievements["fraicheur_bienvenue"].unlocked
        )
        
        # 3 glaçons en une partie
        manager.on_ice_sliced()
        manager.on_ice_sliced()
        self.log_result(
            "'Freeze Stratège' débloqué (3 glaçons/partie)",
            manager.achievements["freeze_stratege"].unlocked
        )
        
        manager.end_game(False)
        
        # Accumuler 10 glaçons au total
        for _ in range(7):
            manager.start_new_game("keyboard")
            manager.on_ice_sliced()
            manager.end_game(False)
        
        self.log_result(
            "'Maître du Givre' débloqué (10 glaçons total)",
            manager.achievements["maitre_givre"].unlocked,
            f"Total: {manager.global_stats.total_ice_sliced}"
        )
        
        self.cleanup()
    
    def test_survival_achievements(self):
        """Test les succès liés à la survie"""
        print("\n[Test Succès Survie]")
        
        manager = AchievementManager(self.test_save_file)
        
        # Partie parfaite (sans perdre de cœur)
        manager.start_new_game("keyboard")
        for _ in range(10):
            manager.on_fruit_sliced(1)
        manager.on_score_update(10)
        manager.end_game(False)
        
        self.log_result(
            "'Cœur Intact' débloqué (0 cœur perdu)",
            manager.achievements["coeur_intact"].unlocked
        )
        
        # Partie avec 2 cœurs restants
        manager.start_new_game("keyboard")
        manager.on_heart_lost()  # Perd 1 cœur
        manager.end_game(False)
        
        self.log_result(
            "'Prudence' débloqué (≥2 cœurs restants)",
            manager.achievements["prudence"].unlocked
        )
        
        # Jouer 10 parties
        for i in range(8):  # Déjà 2 parties jouées
            manager.start_new_game("keyboard")
            manager.end_game(False)
        
        self.log_result(
            "'Survivant' débloqué (10 parties)",
            manager.achievements["survivant"].unlocked,
            f"Parties: {manager.global_stats.total_games_played}"
        )
        
        self.cleanup()
    
    def test_bomb_achievements(self):
        """Test les succès liés aux bombes"""
        print("\n[Test Succès Bombes]")
        
        manager = AchievementManager(self.test_save_file)
        
        # Première explosion
        manager.start_new_game("keyboard")
        manager.end_game(exploded=True)
        
        self.log_result(
            "'Oups...' débloqué (1ère explosion)",
            manager.achievements["oups"].unlocked
        )
        
        # Éviter 10 bombes en une partie
        manager.start_new_game("keyboard")
        for _ in range(10):
            manager.on_bomb_avoided()
        manager.end_game(False)
        
        self.log_result(
            "'Démineur Amateur' débloqué (10 bombes évitées)",
            manager.achievements["demineur_amateur"].unlocked
        )
        
        # Exploser 10 fois au total
        for _ in range(9):  # Déjà 1 explosion
            manager.start_new_game("keyboard")
            manager.end_game(exploded=True)
        
        self.log_result(
            "'Accident de Travail' débloqué (10 explosions)",
            manager.achievements["accident_travail"].unlocked,
            f"Explosions: {manager.global_stats.total_bomb_explosions}"
        )
        
        self.cleanup()
    
    def test_special_achievements(self):
        """Test les succès spéciaux"""
        print("\n[Test Succès Spéciaux]")
        
        manager = AchievementManager(self.test_save_file)
        
        # Bienvenue (premier lancement)
        manager.start_new_game("keyboard")
        self.log_result(
            "'Bienvenue !' débloqué (1er lancement)",
            manager.achievements["bienvenue"].unlocked
        )
        manager.end_game(False)
        
        # Explorateur (visiter écran succès)
        manager.on_success_screen_visited()
        self.log_result(
            "'Explorateur' débloqué (visite écran succès)",
            manager.achievements["explorateur"].unlocked
        )
        
        # Indécis (5 changements de mode)
        for _ in range(5):
            manager.on_mode_switch()
        self.log_result(
            "'Indécis' débloqué (5 changements mode)",
            manager.achievements["indecis"].unlocked
        )
        
        # Speed Runner (20 points en moins de 30 secondes)
        manager.start_new_game("keyboard")
        manager.on_score_update(20)
        manager.on_time_update(25)  # 25 secondes
        self.log_result(
            "'Speed Runner' débloqué (20 pts en <30s)",
            manager.achievements["speed_runner"].unlocked
        )
        manager.end_game(False)
        
        # Marathon (partie de plus de 2 minutes)
        manager.start_new_game("keyboard")
        manager.on_time_update(125)  # 2min 5sec
        self.log_result(
            "'Marathon' débloqué (>2min)",
            manager.achievements["marathon"].unlocked
        )
        manager.end_game(False)
        
        # Parfait (50 points sans perdre de cœur)
        manager.start_new_game("keyboard")
        manager.on_score_update(50)
        self.log_result(
            "'Parfait' débloqué (50 pts, 0 cœur perdu)",
            manager.achievements["parfait"].unlocked
        )
        manager.end_game(False)
        
        # Virtuose du Clavier (50 points en mode clavier)
        self.log_result(
            "'Virtuose du Clavier' débloqué (50 pts clavier)",
            manager.achievements["virtuose_clavier"].unlocked
        )
        
        # Ninja de la souris (50 points en mode souris)
        manager.start_new_game("mouse")
        manager.on_score_update(50)
        manager.end_game(False)
        self.log_result(
            "'Ninja de la souris' débloqué (50 pts souris)",
            manager.achievements["ninja_souris"].unlocked
        )
        
        self.cleanup()
    
    def test_full_game_simulation(self):
        """Simule une session de jeu complète"""
        print("\n[Test Simulation Partie Complète]")
        
        manager = AchievementManager(self.test_save_file)
        
        # Partie 1 : Bonne performance
        manager.start_new_game("keyboard")
        
        # Simuler le gameplay
        for i in range(30):
            manager.on_fruit_sliced(1)
            manager.on_score_update(i + 1)
            
            # Quelques combos
            if i % 7 == 0:
                manager.on_fruit_sliced(3)
                manager.on_score_update(manager.current_game_stats.score + 3)
            
            # Quelques glaçons
            if i % 10 == 0:
                manager.on_ice_sliced()
            
            # Éviter des bombes
            if i % 5 == 0:
                manager.on_bomb_avoided()
            
            manager.on_time_update(i * 2)  # 2 secondes par fruit
        
        manager.end_game(False)
        
        # Compter les succès débloqués
        unlocked = manager.get_unlocked_achievements()
        self.log_result(
            "Simulation partie complète",
            len(unlocked) >= 5,
            f"Succès débloqués: {len(unlocked)}"
        )
        
        # Vérifier la progression
        stats = manager.get_progress_stats()
        self.log_result(
            "Statistiques de progression correctes",
            stats['total_achievements'] == 38,
            f"Total: {stats['total_achievements']}, Débloqués: {stats['unlocked_achievements']}"
        )
        
        self.cleanup()
    
    def print_report(self):
        """Affiche le rapport final"""
        print("\n" + "="*60)
        print("RAPPORT DE TESTS")
        print("="*60)
        
        passed = sum(1 for _, p, _ in self.results if p)
        total = len(self.results)
        
        print(f"\nRésultat: {passed}/{total} tests passés ({100*passed//total}%)")
        
        if passed < total:
            print("\nTests échoués:")
            for name, p, details in self.results:
                if not p:
                    print(f"  - {name}")
                    if details:
                        print(f"    {details}")
        
        print("\n" + "="*60)
        
        return passed == total


# ==================== MAIN ====================

if __name__ == "__main__":
    tester = AchievementTester()
    success = tester.run_all_tests()
    
    # Code de sortie pour CI/CD
    sys.exit(0 if success else 1)
