# 🦖 Fruit Slicer - Sauve Yoshi !

Un jeu de type Fruit Ninja avec une direction artistique inspirée de l'univers Mario/Yoshi.

## 🎮 Concept

**Yoshi est affamé et compte sur vous pour le nourrir !**

- Chaque fruit tranché nourrit Yoshi
- Chaque fruit raté l'affaiblit
- Les Bob-ombs mettent instantanément fin à la partie

## 📋 Règles du jeu

| Élément | Action | Résultat |
|---------|--------|----------|
| 🍎 Fruit | Trancher | +1 point, Yoshi mange |
| 💣 Bob-omb | Trancher | **Game Over instantané** |
| ❄️ Fleur de glace | Trancher | Freeze 3-5 secondes |
| ❌ Fruit raté | Sort de l'écran | -1 cœur |
| 💔 3 cœurs perdus | - | **Game Over** |

### Système de scoring

- 1 fruit tranché seul : **+1 point**
- 3 fruits en un coup (combo) : **+4 points** (3 + bonus de 2)
- 4 fruits en un coup : **+7 points** (4 + bonus de 3)
- Formule : N fruits = **N + (N-1) points**

## 🎯 Modes de contrôle

### Mode Clavier (Typing Game)
Chaque fruit affiche une lettre. Appuyez sur la touche correspondante pour trancher.
- Plusieurs fruits avec la même lettre = combo automatique !

### Mode Souris (Style Fruit Ninja)
Maintenez le clic gauche et tracez une trajectoire à travers les fruits.
- Une traînée visuelle suit votre curseur

## 🏆 Succès (38 au total)

### 🍎 Fruits tranchés (cumulatif)
| Succès | Condition | Description |
|--------|-----------|-------------|
| Premier Repas | 10 fruits | "Yoshi a goûté à ses premiers fruits !" |
| Appétit Croissant | 50 fruits | "Yoshi commence à avoir faim..." |
| Glouton Vert | 100 fruits | "Yoshi ne peut plus s'arrêter de manger !" |
| Estomac Sans Fond | 250 fruits | "Rien ne semble rassasier Yoshi !" |
| Légende de l'Île | 500 fruits | "Yoshi est devenu une légende de Yoshi's Island !" |
| Maître Gourmet | 1000 fruits | "Yoshi a atteint le nirvana culinaire !" |

### 🎯 Score en une partie
| Succès | Condition | Description |
|--------|-----------|-------------|
| Bébé Yoshi | 10 points | "Premiers pas dans l'aventure !" |
| Yoshi Junior | 25 points | "Yoshi grandit et s'améliore !" |
| Yoshi Confirmé | 50 points | "Yoshi maîtrise l'art du festin !" |
| Super Yoshi | 75 points | "Yoshi entre dans la cour des grands !" |
| Yoshi Superstar | 100 points | "Yoshi brille comme une étoile !" |
| Yoshi Légendaire | 150 points | "Yoshi est entré dans la légende !" |

### 👅 Combos
| Succès | Condition | Description |
|--------|-----------|-------------|
| Langue Agile | Combo de 3 | "Yoshi attrape plusieurs fruits d'un coup !" |
| Langue Éclair | Combo de 4 | "La langue de Yoshi est plus rapide que l'éclair !" |
| Langue Divine | Combo de 5+ | "Personne n'a jamais vu une langue aussi rapide !" |
| Combo Addict | 10 combos total | "Yoshi ne jure plus que par les combos !" |
| Combo Master | 50 combos total | "Yoshi est devenu maître dans l'art du combo !" |

### ❄️ Glaçons (Fleur de glace)
| Succès | Condition | Description |
|--------|-----------|-------------|
| Fraîcheur Bienvenue | 1 glaçon | "Yoshi découvre le pouvoir du froid !" |
| Maître du Givre | 10 glaçons total | "Yoshi contrôle le temps comme un pro !" |
| Roi de la Glace | 25 glaçons total | "Yoshi règne sur le royaume gelé !" |
| Freeze Stratège | 3 glaçons/partie | "Yoshi utilise le freeze à la perfection !" |

### 💚 Survie
| Succès | Condition | Description |
|--------|-----------|-------------|
| Cœur Intact | 0 cœur perdu | "Yoshi n'a pas eu une seule indigestion !" |
| Prudence est Mère de Sûreté | ≥2 cœurs restants | "Yoshi sait prendre soin de lui !" |
| Survivant | 10 parties | "Yoshi ne lâche jamais !" |
| Persévérant | 25 parties | "Yoshi revient toujours pour plus !" |
| Increvable | 50 parties | "Rien ne peut arrêter Yoshi !" |

### 💣 Bombes (Bob-omb)
| Succès | Condition | Description |
|--------|-----------|-------------|
| Oups... | 1ère explosion | "Yoshi a fait connaissance avec Bob-omb..." |
| Démineur Amateur | 10 bombes évitées/partie | "Yoshi sait reconnaître le danger !" |
| Expert en Explosifs | 25 bombes évitées/partie | "Les Bob-ombs ne font plus peur à Yoshi !" |
| Accident de Travail | 10 explosions total | "Yoshi n'apprend pas de ses erreurs..." |

### ⭐ Spéciaux
| Succès | Condition | Description |
|--------|-----------|-------------|
| Bienvenue ! | 1er lancement | "Yoshi vous souhaite la bienvenue !" |
| Explorateur | Visiter écran succès | "Yoshi aime regarder ses trophées !" |
| Indécis | 5 changements de mode | "Clavier ? Souris ? Yoshi hésite..." |
| Speed Runner | 20 pts en <30s | "Yoshi mange à la vitesse de la lumière !" |
| Marathon | Partie >2min | "Yoshi a de l'endurance !" |
| Parfait | 50 pts, 0 cœur perdu | "Une partie parfaite pour Yoshi !" |
| Virtuose du Clavier | 50 pts mode clavier | "Les doigts de feu au service de Yoshi !" |
| Ninja de la souris | 50 pts mode souris | "Un vrai ninja du slice !" |

## 🚀 Installation

### Prérequis
- Python 3.8+
- Pygame 2.0+

### Installation
```bash
# Cloner le repository
git clone https://github.com/votre-username/fruit-slicer.git
cd fruit-slicer

# Installer les dépendances
pip install pygame

# Lancer le jeu
python main.py
```

## 📁 Structure du projet

```
fruit-slicer/
├── main.py                 # Point d'entrée, boucle principale
├── scene_manager.py        # Gestionnaire des écrans
├── config.py               # Configuration et constantes
├── save_data.json          # Sauvegarde (généré automatiquement)
├── settings.json           # Préférences utilisateur
│
├── scenes/                 # Écrans du jeu
│   ├── base_scene.py       # Classe de base
│   ├── menu_scene.py       # Menu principal
│   ├── game_scene.py       # Écran de jeu
│   ├── game_over_scene.py  # Écran de fin
│   ├── settings_scene.py   # Paramètres
│   └── success_scene.py    # Écran des succès
│
├── core/                   # Logique métier
│   ├── achievements.py     # Gestionnaire de succès
│   ├── input_handler.py    # Gestion clavier/souris
│   ├── scoring.py          # Calcul des points
│   └── spawner.py          # Génération fruits/bombes
│
├── entities/               # Objets du jeu
│   ├── fruit.py
│   ├── bomb.py
│   └── ice.py
│
├── ui/                     # Interface utilisateur
│   ├── hud.py              # Score, cœurs, timer
│   ├── buttons.py          # Boutons de menu
│   └── notifications.py    # Notifications de succès
│
├── assets/                 # Ressources
│   ├── images/
│   ├── sounds/
│   └── fonts/
│
└── tests/                  # Tests
    └── test_achievements.py
```

## 🎨 Direction artistique

**Thème : Mario/Yoshi - Retro Nintendo**

### Palette de couleurs
| Utilisation | Couleur | Code |
|-------------|---------|------|
| Primaire | Vert Yoshi | #7CB342 |
| Secondaire | Rouge Mario | #E53935 |
| Accent | Jaune pièces | #FFD54F |
| Background | Bleu ciel | #81D4FA |
| Danger | Noir Bob-omb | #212121 |
| Succès | Or étoile | #FFC107 |

### Éléments visuels
- **Yoshi** : Animations idle, eating, sad, KO, celebrating
- **Fruits** : Pomme, Melon, Pastèque, Raisin, Banane (style Yoshi's Island)
- **Bob-omb** : Bombe explosive
- **Fleur de glace** : Glaçon/Freeze
- **UI** : Cœurs, pièces, étoiles dorées

## 🧪 Tests

```bash
# Lancer les tests du système de succès
python -m tests.test_achievements
```

## 👥 Équipe

- **Dev 1** : main.py, SceneManager, InputHandler, SettingsScene
- **Dev 2** : GameScene, Spawner, Scoring, Entités
- **Dev 3** : AchievementManager, SuccessScene, Notifications, Tests
- **Noémie** : MenuScene, Sons, Musique, Documentation

## 📄 Licence

Projet pédagogique - La Plateforme

## 🙏 Crédits

- Inspiré de Fruit Ninja par Halfbrick Studios
- Direction artistique inspirée de Nintendo (Mario, Yoshi's Island)
- Sprites et sons : [À compléter selon les assets utilisés]
