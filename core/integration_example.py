"""
Exemple d'intégration de l'AchievementManager avec la GameScene
Ce fichier montre comment connecter le gestionnaire de succès au reste du jeu.

À intégrer dans scenes/game_scene.py par Dev 2
"""

# ==================== IMPORTS NÉCESSAIRES ====================
# from core.achievements import AchievementManager


# ==================== DANS LA CLASSE GAMESCENE ====================

class GameSceneIntegrationExample:
    """
    Exemple de code à intégrer dans GameScene.
    Ce n'est PAS une classe fonctionnelle, juste une référence.
    """
    
    def __init__(self):
        # Initialiser le gestionnaire de succès
        self.achievement_manager = None  # Sera passé par le SceneManager
    
    def set_achievement_manager(self, manager):
        """Permet au SceneManager de passer le gestionnaire de succès"""
        self.achievement_manager = manager
    
    # ==================== MÉTHODES À APPELER ====================
    
    def on_game_start(self, control_mode: str):
        """Appelé quand une nouvelle partie commence"""
        if self.achievement_manager:
            self.achievement_manager.start_new_game(control_mode)
    
    def on_fruit_sliced(self, fruits_count: int, new_score: int):
        """
        Appelé quand des fruits sont tranchés.
        
        Args:
            fruits_count: Nombre de fruits tranchés (1 = normal, 3+ = combo)
            new_score: Nouveau score après l'action
        """
        if self.achievement_manager:
            self.achievement_manager.on_fruit_sliced(fruits_count)
            self.achievement_manager.on_score_update(new_score)
    
    def on_ice_sliced(self):
        """Appelé quand un glaçon (Fleur de glace) est tranché"""
        if self.achievement_manager:
            self.achievement_manager.on_ice_sliced()
    
    def on_fruit_missed(self):
        """Appelé quand un fruit sort de l'écran sans être tranché"""
        if self.achievement_manager:
            self.achievement_manager.on_heart_lost()
    
    def on_bomb_missed(self):
        """Appelé quand une bombe sort de l'écran sans être touchée"""
        if self.achievement_manager:
            self.achievement_manager.on_bomb_avoided()
    
    def on_update(self, elapsed_time: float):
        """Appelé à chaque frame pour mettre à jour le temps"""
        if self.achievement_manager:
            self.achievement_manager.on_time_update(elapsed_time)
    
    def on_game_over(self, by_bomb: bool = False):
        """
        Appelé quand la partie se termine.
        
        Args:
            by_bomb: True si la partie s'est terminée par une explosion
        """
        if self.achievement_manager:
            self.achievement_manager.end_game(exploded=by_bomb)
    
    def get_new_achievements(self):
        """
        Récupère les succès débloqués pendant cette frame.
        À appeler pour afficher les notifications.
        
        Returns:
            Liste des Achievement nouvellement débloqués
        """
        if self.achievement_manager:
            return self.achievement_manager.get_pending_notifications()
        return []


# ==================== EXEMPLE DE CODE DANS UPDATE() ====================

"""
def update(self, dt, events):
    # ... logique de jeu existante ...
    
    # Mettre à jour le temps pour les succès
    self.game_time += dt
    self.on_update(self.game_time)
    
    # Vérifier les nouvelles notifications de succès
    new_achievements = self.get_new_achievements()
    for achievement in new_achievements:
        # Déclencher l'affichage de la notification
        self.notification_manager.show(achievement)
        # Jouer le son de succès
        self.play_sound("achievement")
"""


# ==================== EXEMPLE DE CODE DANS SLICE_FRUIT() ====================

"""
def slice_fruit(self, fruit):
    # Logique existante pour trancher le fruit
    self.score += 1
    fruit.sliced = True
    
    # Informer le gestionnaire de succès
    self.on_fruit_sliced(1, self.score)

def slice_fruits_combo(self, fruits_list):
    # Logique existante pour combo
    combo_size = len(fruits_list)
    bonus = combo_size - 1  # N fruits = N-1 points bonus
    self.score += combo_size + bonus
    
    for fruit in fruits_list:
        fruit.sliced = True
    
    # Informer le gestionnaire de succès avec le nombre de fruits
    self.on_fruit_sliced(combo_size, self.score)
"""


# ==================== EXEMPLE DANS SCENE_MANAGER ====================

"""
class SceneManager:
    def __init__(self):
        # Créer une seule instance du gestionnaire de succès
        self.achievement_manager = AchievementManager()
        
        # Créer les scènes
        self.scenes = {
            'menu': MenuScene(self),
            'game': GameScene(self),
            'game_over': GameOverScene(self),
            'settings': SettingsScene(self),
            'success': SuccessScene(self)
        }
        
        # Passer le gestionnaire aux scènes qui en ont besoin
        self.scenes['game'].set_achievement_manager(self.achievement_manager)
        self.scenes['success'].set_achievement_manager(self.achievement_manager)
        self.scenes['game_over'].set_achievement_manager(self.achievement_manager)
    
    def on_settings_mode_changed(self):
        # Appelé quand le mode de contrôle change dans les settings
        self.achievement_manager.on_mode_switch()
    
    def on_success_screen_opened(self):
        # Appelé quand on ouvre l'écran des succès
        self.achievement_manager.on_success_screen_visited()
"""
