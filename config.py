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
    
    # Player Select Scene
    PSS_PSEUDO = (255, 255, 255)     # #ffffff
    PSS_DIFFICULTY = (202, 181, 155) # #cab59b
    PSS_EASY = (150, 224, 227)       # #96e0e3
    PSS_NORMAL = (255, 176, 110)     # #ffb06e
    PSS_HARD = (255, 119, 119)       # #ff7777
    PSS_START = (254, 237, 142)      # #feed8e
    
    # Tutorial Scene
    TUTO_TITLE = (255, 176, 110)     # #ffb06e
    TUTO_TEXT = (254, 237, 142)      # #feed8e
    TUTO_PREVIOUS = (202, 181, 155)  # #cab59b
    TUTO_NEXT = (255, 255, 255)      # #ffffff
    TUTO_PLAY = (254, 237, 142)      # #feed8e
    
    # Game Scene
    GAME_SCORE = (254, 237, 142)     # #feed8e
    GAME_NOTIF_SUCCES = (254, 237, 142)  # #feed8e - Notifications de succès

    # Game Over Scene
    GAMEOVER_SCORE = (254, 237, 142)       # #feed8e
    GAMEOVER_NEW_RECORD = (255, 176, 110)  # #ffb06e 
    GAMEOVER_BTN_REJOUER = (254, 237, 142) # #feed8e
    GAMEOVER_BTN_MENU = (239, 183, 255)    # #efb7ff
    GAMEOVER_SUCCES = (254, 237, 142)      # #feed8e
    
    # Ranking Scene (Classement)
    RANKING_TITLE = (254, 237, 142)        # #feed8e
    RANKING_TAB_EASY = (150, 224, 227)     # #96e0e3
    RANKING_TAB_NORMAL = (255, 176, 110)   # #ffb06e
    RANKING_TAB_HARD = (255, 119, 119)     # #ff7777
    RANKING_TAB_CHALLENGE = (239, 183, 255) # #efb7ff
    RANKING_HEADER = (254, 237, 142)       # #feed8e
    RANKING_DATA = (254, 237, 142)         # #feed8e


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
    
    # Challenge Scene
    CHALLENGE_TIMER_FRAME = "scenes/challenge_scene/timer challenge 371x183.png"
    
    # Yoshi - Mode Classique (game_scene)
    YOSHI_CLASSIC_ATTEND = "scenes/game_scene/Yoshi attends 351x465.png"
    YOSHI_CLASSIC_CONTENT = "scenes/game_scene/Yoshi content 351x465.png"
    YOSHI_CLASSIC_TRISTE = "scenes/game_scene/Yoshi triste 351x465.png"
    YOSHI_CLASSIC_GELE = "scenes/game_scene/Yoshi gelé351x465.png"
    YOSHI_CLASSIC_AFFAME = "scenes/game_scene/Yoshi affamé 351x465.png"
    
    # Yoshi - Mode Challenge (challenge_scene)
    YOSHI_CHALLENGE_ATTEND = "scenes/challenge_scene/Yoshi attends 351x465.png"
    YOSHI_CHALLENGE_CONTENT = "scenes/challenge_scene/Yoshi content 351x465.png"
    YOSHI_CHALLENGE_TRISTE = "scenes/challenge_scene/Yoshi triste 351x465.png"
    
    # Player Select Scene
    PSS_BG = "scenes/player_select_scene/background pss 1920x1080.png"
    PSS_PSEUDO_FIELD = "scenes/player_select_scene/Bouton tapez votre pseudo pss 599x88.png"
    PSS_DIFFICULTY_LABEL = "scenes/player_select_scene/bouton difficulté pss 460x89.png"
    PSS_BTN_EASY = "scenes/player_select_scene/bouton facile pss 353x88.png"
    PSS_BTN_NORMAL = "scenes/player_select_scene/bouton normal pss 353x90.png"
    PSS_BTN_HARD = "scenes/player_select_scene/Bouton difficile pss 354x90.png"
    PSS_BTN_START = "scenes/player_select_scene/Bouton c_est parti pss 558x89.png"
    PSS_GEAR = "scenes/player_select_scene/Engrenage pss 104x77.png"
    PSS_CROSS = "scenes/player_select_scene/Croix pss 151x78.png"
    
    # Tutorial Scene - Classic
    TUTO_CLASSIC_BG = "scenes/tutorial_scene/classic/Background tuto classic 1920x1080.png"
    TUTO_CLASSIC_BLOCKS = [
        "scenes/tutorial_scene/classic/Bloc tuto 1 classic 1049x964.png",
        "scenes/tutorial_scene/classic/Bloc tuto 2 classic 1049x964.png",
        "scenes/tutorial_scene/classic/Bloc tuto 3 classic 1049x964.png",
        "scenes/tutorial_scene/classic/Bloc tuto 4 classic 1049x964.png",
        "scenes/tutorial_scene/classic/Bloc tuto 5 classic 1049x964.png",
        "scenes/tutorial_scene/classic/Bloc tuto 6 classic 1049x964.png",
    ]
    TUTO_CLASSIC_BTN_PREV = [
        None,  # Écran 1 : pas de bouton précédent
        "scenes/tutorial_scene/classic/Bouton précédent tuto 2 classic 285x73.png",
        "scenes/tutorial_scene/classic/Bouton précédent tuto 3 classic 285x73.png",
        "scenes/tutorial_scene/classic/Bouton précédent tuto 4 classic 285x73.png",
        "scenes/tutorial_scene/classic/Bouton précédent tuto 5 classic 285x73.png",
        "scenes/tutorial_scene/classic/Bouton précédent tuto 6 classic 285x73.png",
    ]
    TUTO_CLASSIC_BTN_NEXT = [
        "scenes/tutorial_scene/classic/Bouton suivant tuto 1 classic 285x73.png",
        "scenes/tutorial_scene/classic/Bouton suivant tuto 2 classic 285x73.png",
        "scenes/tutorial_scene/classic/Bouton suivant tuto 3 classic 285x73.png",
        "scenes/tutorial_scene/classic/Bouton suivant tuto 4 classic 285x73.png",
        "scenes/tutorial_scene/classic/Bouton suivant tuto 5 classic 285x73.png",
        None,  # Écran 6 : bouton jouer à la place
    ]
    TUTO_CLASSIC_BTN_PLAY = "scenes/tutorial_scene/classic/Bouton jouer tuto 6 classic 285x73.png"
    
    # Tutorial Scene - Challenge
    TUTO_CHALLENGE_BG = "scenes/tutorial_scene/challenge/Background tuto challenge 1920x1080.png"
    TUTO_CHALLENGE_BLOCKS = [
        "scenes/tutorial_scene/challenge/Bloc tuto 1 challenge 1049x964.png",
        "scenes/tutorial_scene/challenge/Bloc tuto 2 challenge 1049x964 - Copie.png",
        "scenes/tutorial_scene/challenge/Bloc tuto 3 challenge 1049x964 - Copie.png",
        "scenes/tutorial_scene/challenge/Bloc tuto 4 challenge 1049x964.png",
    ]
    TUTO_CHALLENGE_BTN_PREV = [
        None,  # Écran 1 : pas de bouton précédent
        "scenes/tutorial_scene/challenge/Bouton précédent tuto 2 challenge 285x73.png",
        "scenes/tutorial_scene/challenge/Bouton précédent tuto 3 challenge 285x73.png",
        "scenes/tutorial_scene/challenge/Bouton précédent tuto 4 challenge 285x73.png",
    ]
    TUTO_CHALLENGE_BTN_NEXT = [
        "scenes/tutorial_scene/challenge/Bouton suivant tuto 1 challenge 285x73.png",
        "scenes/tutorial_scene/challenge/Bouton suivant tuto 2 challenge 285x73.png",
        "scenes/tutorial_scene/challenge/Bouton suivant tuto 3 challenge 285x73.png",
        None,  # Écran 4 : bouton jouer à la place
    ]
    TUTO_CHALLENGE_BTN_PLAY = "scenes/tutorial_scene/challenge/Bouton jouer tuto 4 challenge 285x73.png"

    # Game Over Scene
    # Explosion (bombe tranchée) - FR/EN
    GAMEOVER_EXPLOSION_BG_FR = "scenes/game_over_scene/explosion/Background défaite explosion1920x1080.png"
    GAMEOVER_EXPLOSION_BG_EN = "scenes/game_over_scene/explosion/Background game over explosion1920x1080.png"
    GAMEOVER_EXPLOSION_BTN_REJOUER = "scenes/game_over_scene/explosion/Bouton rejouer game over explosion 458x89.png"
    GAMEOVER_EXPLOSION_BTN_MENU = "scenes/game_over_scene/explosion/Bouton menu game over explosion 458x89.png"
    
    # K.O (3 cœurs perdus) - FR/EN
    GAMEOVER_KO_BG_FR = "scenes/game_over_scene/K.O/Background défaite ko1920x1080.png"
    GAMEOVER_KO_BG_EN = "scenes/game_over_scene/K.O/Background game over ko1920x1080.png"
    GAMEOVER_KO_BTN_REJOUER = "scenes/game_over_scene/K.O/Bouton rejouer game over ko 458x89.png"
    GAMEOVER_KO_BTN_MENU = "scenes/game_over_scene/K.O/Bouton menu game over ko 458x89.png"
    
    # Temps écoulé (challenge) - FR/EN
    GAMEOVER_TIME_BG_FR = "scenes/game_over_scene/elapsed_time/Background temps écoulé challenge1920x1080.png"
    GAMEOVER_TIME_BG_EN = "scenes/game_over_scene/elapsed_time/Background time_s up challenge1920x1080.png"
    GAMEOVER_TIME_BTN_REJOUER = "scenes/game_over_scene/elapsed_time/Bouton temps écoulé challenge 458x89.png"
    GAMEOVER_TIME_BTN_MENU = "scenes/game_over_scene/elapsed_time/Bouton menu temps écoulé challenge 458x89.png"
    
    # Bouton succès (commun à toutes les variantes)
    GAMEOVER_BTN_SUCCES = "scenes/game_over_scene/explosion/Bouton succes 544x80.png"
    
    # Notifications de succès en jeu (chaque mode a son propre asset)
    NOTIF_BTN_SUCCES_CLASSIC = "scenes/game_scene/Bouton succes 544x80.png"
    NOTIF_BTN_SUCCES_CHALLENGE = "scenes/challenge_scene/Bouton succes 544x80.png"
    
    # Ranking Scene (Classement)
    RANKING_BG = "scenes/ranking_scene/Background classement 1920x1080.png"
    RANKING_BLOCK = "scenes/ranking_scene/Bloc classement 1568x936.png"
    RANKING_TITLE = "scenes/ranking_scene/Bouton classement classement 458x89.png"
    RANKING_BTN_EASY = "scenes/ranking_scene/Bouton facile classement 281x74.png"
    RANKING_BTN_NORMAL = "scenes/ranking_scene/Bouton normal classement 281x74.png"
    RANKING_BTN_HARD = "scenes/ranking_scene/Bouton difficile classement 281x74.png"
    RANKING_BTN_CHALLENGE = "scenes/ranking_scene/Bouton challenge classement 281x74.png"
    RANKING_GEAR = "scenes/ranking_scene/Engrenage claassement 104x77.png"
    RANKING_CROSS = "scenes/ranking_scene/Croix classement 151x78.png"


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
    
    # Player Select Scene (centre des éléments)
    PSS_GEAR = (1624, 84)
    PSS_CROSS = (1765, 84)
    PSS_PSEUDO_FIELD = (960, 370)
    PSS_DIFFICULTY_LABEL = (960, 584)
    PSS_BTN_EASY = (585, 699)
    PSS_BTN_NORMAL = (960, 699)
    PSS_BTN_HARD = (1335, 699)
    PSS_BTN_START = (960, 876)
    
    # Tutorial Scene (centre des éléments)
    TUTO_BLOCK = (960, 535)
    TUTO_TITLE = (960, 164)
    TUTO_TEXT = (960, 653)
    TUTO_BTN_PREV = (706, 787)
    TUTO_BTN_NEXT = (1214, 787)
    TUTO_BTN_PLAY = (1214, 787)  # Même position que suivant
    
    # Game Scene (positions des éléments)
    GAME_SCORE_POS_CLASSIC = (171, 84)    # Point de justification gauche (classique)
    GAME_SCORE_POS_CHALLENGE = (361, 84)  # Point de justification gauche (challenge)
    GAME_HEART_1 = (878, 84)
    GAME_HEART_2 = (960, 84)
    GAME_HEART_3 = (1041, 84)
    GAME_GEAR = (1624, 84)
    GAME_CROSS = (1765, 84)
    GAME_TIMER = (960, 106)               # Timer challenge (centre)
    GAME_GAUGE = (960, 1003)
    GAME_GAUGE_SEGMENTS = [
        (763, 1016),   # Jaune
        (862, 1016),   # Orange
        (960, 1016),   # Rouge
        (1058, 1016),  # Violet
        (1157, 1016),  # Bleu
    ]
    GAME_YOSHI = (1757, 740)              # Position de Yoshi (centre)
    
    # Notifications de succès en jeu (mêmes positions que game_over)
    GAME_NOTIF_BTN = (342, 1016)           # Centre du bouton succès
    GAME_NOTIF_TEXT = (170, 1016)          # Justifié gauche, centery

    # Game Over Scene (coordonnées selon le tableau de specs)
    # Scores : justifié gauche (left=394)
    GAMEOVER_SCORE_FINAL = (394, 476)      # Point de justification gauche, centery
    GAMEOVER_BEST_SCORE = (394, 558)       # Point de justification gauche, centery
    GAMEOVER_NEW_RECORD = (962, 474)       # Justifié gauche, centery
    
    # Boutons : centre
    GAMEOVER_BTN_REJOUER = (597, 688)      # Centre du bouton
    GAMEOVER_BTN_MENU = (597, 823)         # Centre du bouton
    
    # Textes boutons (légèrement différent du centre bouton selon specs)
    GAMEOVER_TEXT_REJOUER = (597, 687)     # Centre du texte
    GAMEOVER_TEXT_MENU = (597, 823)        # Centre du texte
    
    # Succès débloqués
    GAMEOVER_SUCCES_TEXT = (170, 1016)     # Justifié gauche, centery
    GAMEOVER_BTN_SUCCES = (342, 1016)      # Centre du bouton succès
    
    # Ranking Scene (Classement)
    RANKING_BLOCK = (960, 611)             # Centre du bloc principal
    RANKING_TITLE = (960, 138)             # Centre du titre "Classement"
    RANKING_GEAR = (1624, 84)              # Centre engrenage
    RANKING_CROSS = (1765, 84)             # Centre croix
    
    # Onglets de difficulté (centre)
    RANKING_TAB_EASY = (510, 235)
    RANKING_TAB_NORMAL = (809, 235)
    RANKING_TAB_HARD = (1110, 235)
    RANKING_TAB_CHALLENGE = (1410, 235)
    
    # En-têtes du tableau (centre X, centery)
    RANKING_HEADER_RANK = (510, 331)
    RANKING_HEADER_PSEUDO = (810, 331)
    RANKING_HEADER_SCORE = (1266, 331)
    
    # Première ligne de données (Y de départ, puis +43px par ligne environ)
    RANKING_DATA_START_Y = 400
    RANKING_DATA_LINE_HEIGHT = 55
    RANKING_DATA_RANK_X = 510
    RANKING_DATA_PSEUDO_X = 810
    RANKING_DATA_SCORE_X = 1266


# ==================== GAMEPLAY ====================

class GameConfig:
    MAX_HEARTS = 3
    FRUIT_SIZE = 223
    FRUIT_TYPES = ['apple', 'banana', 'grape', 'melon', 'watermelon']
    
    # Zone de jeu active (centre 960x535, taille 1260x770)
    GAME_ZONE_CENTER = (960, 535)
    GAME_ZONE_SIZE = (1260, 770)
    GAME_ZONE_LEFT = 960 - 630  # 330
    GAME_ZONE_RIGHT = 960 + 630  # 1590
    GAME_ZONE_TOP = 535 - 385  # 150
    GAME_ZONE_BOTTOM = 535 + 385  # 920
    
    SPAWN_MARGIN = 0.10  # 10% marge sur les côtés de la zone
    
    # Jauge bonus
    BONUS_MAX_CRANS = 5
    BONUS_DURATION = 10.0
    BONUS_INCREMENT = 2
    
    # Paires identiques (pour remplir la jauge)
    IDENTICAL_PAIR_CHANCE = 0.25


# ==================== DIFFICULTÉ ====================

DIFFICULTY = {
    'easy': {
        'speed_y': (-1000, -850),    # Monte ~500-625 px
        'speed_x': (-60, 60),
        'gravity': 700,
        'spawn_delay': (1.5, 2.0),
        'fruits_per_spawn': (1, 2),
        'bomb_chance': 0.05,
        'ice_chance': 0.10,
        'freeze_duration': 5.0,
    },
    'normal': {
        'speed_y': (-1100, -950),    # Monte ~550-700 px
        'speed_x': (-80, 80),
        'gravity': 750,
        'spawn_delay': (1.0, 1.5),
        'fruits_per_spawn': (1, 3),
        'bomb_chance': 0.10,
        'ice_chance': 0.07,
        'freeze_duration': 4.0,
    },
    'hard': {
        'speed_y': (-1150, -950),    # Monte ~550-680 px
        'speed_x': (-100, 100),
        'gravity': 800,
        'spawn_delay': (0.6, 1.0),
        'fruits_per_spawn': (2, 4),
        'bomb_chance': 0.15,
        'ice_chance': 0.04,
        'freeze_duration': 3.0,
    },
    'challenge': {
        'speed_y': (-1100, -950),
        'speed_x': (-80, 80),
        'gravity': 750,
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
