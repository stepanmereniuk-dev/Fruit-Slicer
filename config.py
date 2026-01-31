"""
Configuration du jeu Fruit Slicer
"""

import os

# ==================== CHEMINS ====================

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")
LANG_DIR = os.path.join(ASSETS_DIR, "lang")

SAVE_FILE = os.path.join(ROOT_DIR, "save_data.json")
SETTINGS_FILE = os.path.join(ROOT_DIR, "settings.json")


# ==================== FENÊTRE ====================

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
WINDOW_TITLE = "Fruit Slicer - Sauve Yoshi !"
FPS = 60


# ==================== POLICE ====================

FONT_FILE = "Baloo2-SemiBold.ttf"
FONT_SIZE = 36


# ==================== COULEURS TEXTE (boutons menu) ====================

class TextColors:
    BTN_JOUER = (254, 237, 142)      # #feed8e
    BTN_CHALLENGE = (255, 176, 110)  # #ffb06e
    BTN_CLASSEMENT = (202, 181, 155) # #cab59b
    BTN_SUCCES = (202, 181, 155)     # #cab59b
    BTN_PARAMETRES = (202, 181, 155) # #cab59b
    BTN_QUITTER = (239, 183, 255)    # #efb7ff
    
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)


# ==================== IMAGES ====================

class Images:
    """Chemins relatifs depuis IMAGES_DIR"""
    
    # Backgrounds
    MENU_BG = "scenes/menu_scene/Background menu_scene 1920x1080.png"
    GAME_BG = "scenes/game_scene/Background gamescene 1920x1080.png"
    CHALLENGE_BG = "scenes/challenge_scene/Background challenge 1920x1080.png"
    
    # Boutons menu
    BTN_JOUER = "scenes/menu_scene/bouton jouer 458x89.png"
    BTN_CHALLENGE = "scenes/menu_scene/bouton challenge 458x89.png"
    BTN_CLASSEMENT = "scenes/menu_scene/bouton classement 458x89.png"
    BTN_SUCCES = "scenes/menu_scene/bouton succes 458x89.png"
    BTN_PARAMETRES = "scenes/menu_scene/bouton parametres 458x89.png"
    BTN_QUITTER = "scenes/menu_scene/bouton quitter 458x89.png"
    
    # Fruits
    FRUITS = {
        'apple': {
            'normal': "elements/fruits/apple/Pomme 223x223.png",
            'sliced': "elements/fruits/apple/Pomme coupée 223x223.png",
            'frozen': "elements/fruits/apple/Pomme gelée 223x223.png",
            'splash': "elements/fruits/apple/Eclabousure Pomme 223x223.png",
        },
        'banana': {
            'normal': "elements/fruits/banana/Bananes 223x223.png",
            'sliced': "elements/fruits/banana/Bananes coupée 223x223.png",
            'frozen': "elements/fruits/banana/Bananes gelées 223x223.png",
            'splash': "elements/fruits/banana/Eclabousure Bananes 223x223.png",
        },
        'grape': {
            'normal': "elements/fruits/grape/Raisin 223x223.png",
            'sliced': "elements/fruits/grape/Raisin coupé 223x223.png",
            'frozen': "elements/fruits/grape/Raisin gelé 223x223.png",
            'splash': "elements/fruits/grape/Eclabousure Raisin 223x223.png",
        },
        'melon': {
            'normal': "elements/fruits/melon/Melon 223x223.png",
            'sliced': "elements/fruits/melon/Melon coupé 223x223.png",
            'frozen': "elements/fruits/melon/Melon gelé 223x223.png",
            'splash': "elements/fruits/melon/Eclabousure Melon 223x223.png",
        },
        'watermelon': {
            'normal': "elements/fruits/watermelon/Pastèque 223x223.png",
            'sliced': "elements/fruits/watermelon/Pastèque coupée 223x223.png",
            'frozen': "elements/fruits/watermelon/Pastèque gelée 223x223.png",
            'splash': "elements/fruits/watermelon/Eclabousure Pastèque 223x223.png",
        },
    }
    
    # Éléments spéciaux
    BOMB = "elements/bomb/Bombe 223x223 (1).png"
    ICE_FLOWER = "elements/ice_flower/Fleur de glace 223x223 (1).png"
    ICE_FLOWER_SLICED = "elements/ice_flower/Fleur de glace coupée 223x223 (1).png"
    
    # HUD
    HEART_FULL = "scenes/game_scene/Coeur rouge gamescene 78x68.png"
    HEART_EMPTY = "scenes/game_scene/Coeur gris gamescene 78x68.png"
    GAUGE = "scenes/game_scene/Jauge gamescene 520x126.png"
    GEAR = "scenes/game_scene/Engrenage gamescene 104x77.png"
    CROSS = "scenes/game_scene/Croix gamescene 151x78.png"
    
    # Segments jauge bonus
    GAUGE_YELLOW = "scenes/game_scene/jaune gamescene 81 x 36.png"
    GAUGE_ORANGE = "scenes/game_scene/orange gamescene 81 x 36.png"
    GAUGE_RED = "scenes/game_scene/rouge gamescene 81 x 36.png"
    GAUGE_PURPLE = "scenes/game_scene/violet gamescene 81 x 36.png"
    GAUGE_BLUE = "scenes/game_scene/bleu gamescene 81 x 36.png"


# ==================== POSITIONS (centre des éléments) ====================

class Layout:
    """Coordonnées des éléments UI"""
    
    # Menu - boutons (centre)
    MENU_BTN_JOUER = (960, 624)
    MENU_BTN_CHALLENGE = (960, 726)
    MENU_BTN_CLASSEMENT = (960, 826)
    MENU_BTN_SUCCES = (960, 928)
    MENU_BTN_PARAMETRES = (309, 1015)
    MENU_BTN_QUITTER = (1588, 1015)


# ==================== GAMEPLAY ====================

class GameConfig:
    MAX_HEARTS = 3
    FRUIT_SIZE = 223
    FRUIT_TYPES = ['apple', 'banana', 'grape', 'melon', 'watermelon']
    
    # Zone de jeu active
    GAME_ZONE = (1260, 770)
    SPAWN_MARGIN = 0.15  # 15% marge sur les côtés
    
    # Jauge bonus
    BONUS_MAX_CRANS = 5
    BONUS_DURATION = 10.0
    BONUS_INCREMENT = 2
    
    # Paires identiques (pour remplir la jauge)
    IDENTICAL_PAIR_CHANCE = 0.25


# ==================== DIFFICULTÉ ====================

DIFFICULTY = {
    'easy': {
        'speed_y': (-500, -400),
        'speed_x': (-50, 50),
        'gravity': 400,
        'spawn_delay': (1.5, 2.0),
        'fruits_per_spawn': (1, 2),
        'bomb_chance': 0.05,
        'ice_chance': 0.10,
        'freeze_duration': 5.0,
    },
    'normal': {
        'speed_y': (-600, -500),
        'speed_x': (-100, 100),
        'gravity': 500,
        'spawn_delay': (1.0, 1.5),
        'fruits_per_spawn': (1, 3),
        'bomb_chance': 0.10,
        'ice_chance': 0.07,
        'freeze_duration': 4.0,
    },
    'hard': {
        'speed_y': (-750, -600),
        'speed_x': (-150, 150),
        'gravity': 600,
        'spawn_delay': (0.6, 1.0),
        'fruits_per_spawn': (2, 4),
        'bomb_chance': 0.15,
        'ice_chance': 0.04,
        'freeze_duration': 3.0,
    },
    'challenge': {
        'duration': 60,
        'spawn_delay': (0.8, 1.2),
        'fruits_per_spawn': (1, 3),
        'bomb_chance': 0.10,
        'ice_chance': 0.0,
        'bomb_penalty': 10,
    },
}


# ==================== CONTRÔLES ====================

class ControlMode:
    KEYBOARD = "keyboard"
    MOUSE = "mouse"
    DEFAULT = MOUSE

KEYBOARD_LETTERS = ['A', 'Z', 'E', 'R', 'T', 'Q', 'S', 'D', 'F', 'G', 'W', 'X', 'C', 'V']


# ==================== AUDIO ====================

class AudioConfig:
    DEFAULT_MUSIC_VOLUME = 0.5
    DEFAULT_SFX_VOLUME = 0.5


# ==================== DEBUG ====================

DEBUG_MODE = False
SHOW_FPS = True
