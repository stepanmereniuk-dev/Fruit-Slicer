# Module Achievements - Documentation Dev 3

## Vue d'ensemble

Ce module gère le système de succès du jeu Fruit Slicer (thème Yoshi).

## Fichiers

```
core/
├── __init__.py          # Exports du module
├── achievements.py      # Gestionnaire principal des succès
└── integration_example.py  # Exemples d'intégration
```

## Classes principales

### `AchievementManager`
Gestionnaire central des succès. Une seule instance doit exister dans le jeu.

### `Achievement`
Représente un succès individuel avec :
- `id` : Identifiant unique
- `name` : Nom affiché
- `description` : Description affichée
- `category` : Catégorie du succès
- `unlocked` : État de déblocage

### `GameStats`
Statistiques de la partie en cours.

### `GlobalStats`
Statistiques cumulées entre toutes les parties.

## Utilisation rapide

```python
from core.achievements import AchievementManager

# Initialiser (une seule fois, dans SceneManager)
manager = AchievementManager()

# Début de partie
manager.start_new_game("keyboard")  # ou "mouse"

# Pendant le jeu
manager.on_fruit_sliced(1)      # Un fruit tranché
manager.on_fruit_sliced(3)      # Combo de 3 fruits
manager.on_score_update(10)     # Nouveau score
manager.on_ice_sliced()         # Glaçon tranché
manager.on_heart_lost()         # Cœur perdu
manager.on_bomb_avoided()       # Bombe évitée
manager.on_time_update(45.5)    # Temps écoulé en secondes

# Fin de partie
manager.end_game(exploded=False)  # True si mort par bombe

# Récupérer les notifications
new_achievements = manager.get_pending_notifications()
for ach in new_achievements:
    print(f"Débloqué: {ach.name}")
```

## Liste des 36 succès implémentés

### Fruits tranchés (cumulatif) - 6 succès
| ID | Nom | Condition |
|----|-----|-----------|
| premier_repas | Premier Repas | 10 fruits |
| appetit_croissant | Appétit Croissant | 50 fruits |
| glouton_vert | Glouton Vert | 100 fruits |
| estomac_sans_fond | Estomac Sans Fond | 250 fruits |
| legende_ile | Légende de l'Île | 500 fruits |
| maitre_gourmet | Maître Gourmet | 1000 fruits |

### Score en une partie - 6 succès
| ID | Nom | Condition |
|----|-----|-----------|
| bebe_yoshi | Bébé Yoshi | 10 points |
| yoshi_junior | Yoshi Junior | 25 points |
| yoshi_confirme | Yoshi Confirmé | 50 points |
| super_yoshi | Super Yoshi | 75 points |
| yoshi_superstar | Yoshi Superstar | 100 points |
| yoshi_legendaire | Yoshi Légendaire | 150 points |

### Combos - 5 succès
| ID | Nom | Condition |
|----|-----|-----------|
| langue_agile | Langue Agile | Combo de 3 |
| langue_eclair | Langue Éclair | Combo de 4 |
| langue_divine | Langue Divine | Combo de 5+ |
| combo_addict | Combo Addict | 10 combos total |
| combo_master | Combo Master | 50 combos total |

### Glaçons - 4 succès
| ID | Nom | Condition |
|----|-----|-----------|
| fraicheur_bienvenue | Fraîcheur Bienvenue | 1 glaçon |
| maitre_givre | Maître du Givre | 10 glaçons total |
| roi_glace | Roi de la Glace | 25 glaçons total |
| freeze_stratege | Freeze Stratège | 3 glaçons en 1 partie |

### Survie - 5 succès
| ID | Nom | Condition |
|----|-----|-----------|
| coeur_intact | Cœur Intact | 0 cœur perdu |
| prudence | Prudence est Mère de Sûreté | ≥2 cœurs restants |
| survivant | Survivant | 10 parties |
| perseverant | Persévérant | 25 parties |
| increvable | Increvable | 50 parties |

### Bombes - 4 succès
| ID | Nom | Condition |
|----|-----|-----------|
| oups | Oups... | 1ère explosion |
| demineur_amateur | Démineur Amateur | 10 bombes évitées/partie |
| expert_explosifs | Expert en Explosifs | 25 bombes évitées/partie |
| accident_travail | Accident de Travail | 10 explosions total |

### Spéciaux - 8 succès
| ID | Nom | Condition |
|----|-----|-----------|
| bienvenue | Bienvenue ! | 1er lancement |
| explorateur | Explorateur | Visiter l'écran succès |
| indecis | Indécis | 5 changements de mode |
| speed_runner | Speed Runner | 20 pts en <30s |
| marathon | Marathon | Partie de >2min |
| parfait | Parfait | 50 pts sans perdre de cœur |
| virtuose_clavier | Virtuose du Clavier | 50 pts en mode clavier |
| ninja_souris | Ninja de la souris | 50 pts en mode souris |

## Sauvegarde

Les données sont sauvegardées dans `save_data.json` automatiquement à chaque fin de partie.

## Intégration avec les autres développeurs

### Pour Dev 1 (SceneManager)
- Créer une instance unique de `AchievementManager`
- La passer aux scènes Game, Success et GameOver
- Appeler `on_mode_switch()` quand le mode change dans Settings

### Pour Dev 2 (GameScene)
- Voir `integration_example.py` pour les appels à faire
- Appeler les méthodes `on_*` aux bons moments du gameplay

### Pour Noémie (Sons)
- Récupérer les notifications avec `get_pending_notifications()`
- Jouer le son de succès quand une notification arrive
