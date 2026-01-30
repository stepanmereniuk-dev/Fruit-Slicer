"""
Configuration du jeu Fruit Slicer
Constantes, chemins et paramètres globaux
"""

import os

# ==================== CHEMINS ====================

# Dossier racine du projet
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Dossiers des ressources
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")

# Fichiers de sauvegarde
SAVE_FILE = os.path.join(ROOT_DIR, "save_data.json")
SETTINGS_FILE = os.path.join(ROOT_DIR, "settings.json")


# ==================== FENÊTRE ====================

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Fruit Slicer - Sauve Yoshi !"
FPS = 60


# ==================== COULEURS (Thème Mario/Yoshi) ====================

class Colors:
    """Palette de couleurs du jeu"""
    PRIMARY = (124, 179, 66)        # Vert Yoshi #7CB342
    SECONDARY = (229, 57, 53)       # Rouge Mario #E53935
    ACCENT = (255, 213, 79)         # Jaune pièces #FFD54F
    BACKGROUND = (129, 212, 250)    # Bleu ciel #81D4FA
    DANGER = (33, 33, 33)           # Noir Bob-omb #212121
    WHITE = (255, 255, 255)         # Blanc nuages
    GOLD = (255, 193, 7)            # Or étoile #FFC107
    GRAY = (158, 158, 158)          # Gris verrouillé #9E9E9E
    GRAY_DARK = (97, 97, 97)        # Gris foncé


# ==================== GAMEPLAY ====================

class GameConfig:
    """Configuration du gameplay"""
    
    # Cœurs / Vies
    MAX_HEARTS = 3
    
    # Fruits
    FRUIT_SPAWN_RATE_MIN = 0.8      # Temps min entre spawns (secondes)
    FRUIT_SPAWN_RATE_MAX = 1.5      # Temps max entre spawns (secondes)
    FRUIT_SPEED_MIN = 200           # Vitesse min des fruits (pixels/sec)
    FRUIT_SPEED_MAX = 350           # Vitesse max des fruits (pixels/sec)
    FRUIT_TYPES = ['apple', 'melon', 'watermelon', 'grape', 'banana']
    
    # Bombes
    BOMB_SPAWN_CHANCE = 0.15        # Probabilité d'apparition (15%)
    
    # Glaçons
    ICE_SPAWN_CHANCE = 0.08         # Probabilité d'apparition (8%)
    FREEZE_DURATION_MIN = 3.0       # Durée min du freeze (secondes)
    FREEZE_DURATION_MAX = 5.0       # Durée max du freeze (secondes)
    
    # Scoring
    SCORE_PER_FRUIT = 1
    COMBO_BONUS = lambda n: n - 1   # N fruits = N-1 points bonus
    
    # Difficulté progressive
    DIFFICULTY_INCREASE_INTERVAL = 30   # Augmenter difficulté toutes les X secondes
    SPEED_INCREASE_RATE = 1.1           # Multiplier vitesse par ce facteur


# ==================== CONTRÔLES ====================

class ControlMode:
    """Modes de contrôle disponibles"""
    KEYBOARD = "keyboard"
    MOUSE = "mouse"


# ==================== SONS ====================

class SoundConfig:
    """Configuration audio"""
    MUSIC_VOLUME = 0.5
    SFX_VOLUME = 0.7
    
    # Noms des fichiers sons (à placer dans assets/sounds/)
    SOUND_SLICE = "slice.wav"
    SOUND_MISS = "miss.wav"
    SOUND_BOMB = "explosion.wav"
    SOUND_FREEZE = "freeze.wav"
    SOUND_COMBO = "combo.wav"
    SOUND_ACHIEVEMENT = "achievement.wav"  # Son 1-UP style
    
    # Musiques
    MUSIC_MENU = "menu_music.ogg"
    MUSIC_GAME = "game_music.ogg"
    MUSIC_GAMEOVER = "gameover_music.ogg"


# ==================== SUCCÈS ====================

class AchievementConfig:
    """Configuration du système de succès"""
    NOTIFICATION_DURATION = 3.0     # Durée d'affichage (secondes)
    MAX_NOTIFICATIONS = 3           # Nombre max simultané
    

# ==================== DEBUG ====================

DEBUG_MODE = False
SHOW_FPS = True
SHOW_HITBOXES = False
