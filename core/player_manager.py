"""
PlayerManager - Gestion des joueurs et de leurs données.

Responsabilités :
- Créer/charger les profils joueurs par pseudo
- Gérer les high scores (4 catégories)
- Stocker les succès et stats PAR JOUEUR
- Savoir si le tutoriel a été vu
- Sauvegarder/charger depuis save_data.json
"""

import json
import os
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict, field

from config import SAVE_FILE


@dataclass
class PlayerStats:
    """Statistiques d'un joueur (cumulées sur toutes ses parties)."""
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
    def from_dict(cls, data: dict) -> 'PlayerStats':
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class PlayerData:
    """Données d'un joueur."""
    pseudo: str
    high_scores: Dict[str, int] = field(default_factory=lambda: {
        'classic_easy': 0,
        'classic_normal': 0,
        'classic_hard': 0,
        'challenge': 0,
    })
    tutorial_seen: bool = False
    total_games: int = 0
    
    # Succès débloqués par ce joueur (dict: achievement_id -> bool)
    achievements: Dict[str, bool] = field(default_factory=dict)
    
    # Stats cumulées de ce joueur
    stats: PlayerStats = field(default_factory=PlayerStats)
    
    def to_dict(self) -> dict:
        return {
            'pseudo': self.pseudo,
            'high_scores': self.high_scores,
            'tutorial_seen': self.tutorial_seen,
            'total_games': self.total_games,
            'achievements': self.achievements,
            'stats': self.stats.to_dict(),
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'PlayerData':
        stats_data = data.get('stats', {})
        return cls(
            pseudo=data.get('pseudo', ''),
            high_scores=data.get('high_scores', {
                'classic_easy': 0,
                'classic_normal': 0,
                'classic_hard': 0,
                'challenge': 0,
            }),
            tutorial_seen=data.get('tutorial_seen', False),
            total_games=data.get('total_games', 0),
            achievements=data.get('achievements', {}),
            stats=PlayerStats.from_dict(stats_data) if stats_data else PlayerStats(),
        )


class PlayerManager:
    """
    Gère les profils joueurs.
    
    Utilisation :
        manager = PlayerManager()
        manager.set_current_player("Yoshi")
        manager.update_high_score('classic_normal', 150)
        manager.save()
    """
    
    def __init__(self, save_path: str = None):
        self.save_path = save_path or SAVE_FILE
        self.players: Dict[str, PlayerData] = {}
        self.current_player: Optional[PlayerData] = None
        
        self.load()
    
    # ==================== SAUVEGARDE ====================
    
    def save(self):
        """Sauvegarde tous les joueurs dans le fichier."""
        data = {
            'players': {
                pseudo: player.to_dict() 
                for pseudo, player in self.players.items()
            }
        }
        
        try:
            with open(self.save_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except IOError:
            pass
    
    def load(self):
        """Charge les joueurs depuis le fichier."""
        if not os.path.exists(self.save_path):
            return
        
        try:
            with open(self.save_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            players_data = data.get('players', {})
            for pseudo, player_dict in players_data.items():
                self.players[pseudo] = PlayerData.from_dict(player_dict)
        except (IOError, json.JSONDecodeError):
            pass
    
    # ==================== GESTION JOUEURS ====================
    
    def set_current_player(self, pseudo: str) -> PlayerData:
        """
        Définit le joueur actuel. Crée le profil si nouveau.
        Retourne les données du joueur.
        """
        pseudo = self._sanitize_pseudo(pseudo)
        
        if pseudo not in self.players:
            self.players[pseudo] = PlayerData(pseudo=pseudo)
            self.save()
        
        self.current_player = self.players[pseudo]
        return self.current_player
    
    def get_player(self, pseudo: str) -> Optional[PlayerData]:
        """Retourne les données d'un joueur ou None."""
        return self.players.get(pseudo)
    
    def get_all_pseudos(self) -> List[str]:
        """Retourne la liste de tous les pseudos."""
        return list(self.players.keys())
    
    def player_exists(self, pseudo: str) -> bool:
        """Vérifie si un joueur existe."""
        return pseudo in self.players
    
    def is_new_player(self, pseudo: str) -> bool:
        """Vérifie si c'est un nouveau joueur (pour le tutoriel)."""
        player = self.players.get(pseudo)
        if not player:
            return True
        return not player.tutorial_seen
    
    def _sanitize_pseudo(self, pseudo: str) -> str:
        """Nettoie le pseudo (lettres uniquement, max 10 caractères)."""
        # Garder uniquement les lettres
        clean = ''.join(c for c in pseudo if c.isalpha())
        # Limiter à 10 caractères
        return clean[:10]
    
    # ==================== HIGH SCORES ====================
    
    def update_high_score(self, category: str, score: int) -> bool:
        """
        Met à jour le high score si battu.
        Retourne True si nouveau record.
        """
        if not self.current_player:
            return False
        
        current_high = self.current_player.high_scores.get(category, 0)
        
        if score > current_high:
            self.current_player.high_scores[category] = score
            self.save()
            return True
        
        return False
    
    def get_high_score(self, category: str) -> int:
        """Retourne le high score du joueur actuel pour une catégorie."""
        if not self.current_player:
            return 0
        return self.current_player.high_scores.get(category, 0)
    
    def get_category_key(self, mode: str, difficulty: str) -> str:
        """Retourne la clé de catégorie pour le high score."""
        if mode == 'challenge':
            return 'challenge'
        return f'classic_{difficulty}'
    
    # ==================== CLASSEMENT ====================
    
    def get_leaderboard(self, category: str, limit: int = 10) -> List[Dict]:
        """
        Retourne le classement pour une catégorie.
        Format: [{'rank': 1, 'pseudo': 'Yoshi', 'score': 150}, ...]
        """
        # Collecter les scores
        scores = []
        for pseudo, player in self.players.items():
            score = player.high_scores.get(category, 0)
            if score > 0:
                scores.append({'pseudo': pseudo, 'score': score})
        
        # Trier par score décroissant
        scores.sort(key=lambda x: x['score'], reverse=True)
        
        # Ajouter les rangs et limiter
        leaderboard = []
        for i, entry in enumerate(scores[:limit]):
            leaderboard.append({
                'rank': i + 1,
                'pseudo': entry['pseudo'],
                'score': entry['score'],
            })
        
        return leaderboard
    
    # ==================== TUTORIEL ====================
    
    def mark_tutorial_seen(self):
        """Marque le tutoriel comme vu pour le joueur actuel."""
        if self.current_player:
            self.current_player.tutorial_seen = True
            self.save()
    
    def should_show_tutorial(self) -> bool:
        """Retourne True si le tutoriel doit être affiché."""
        if not self.current_player:
            return True
        return not self.current_player.tutorial_seen
    
    # ==================== STATS ====================
    
    def increment_games_played(self):
        """Incrémente le compteur de parties jouées."""
        if self.current_player:
            self.current_player.total_games += 1
            self.save()
    
    # ==================== ACHIEVEMENTS (accesseurs pour AchievementManager) ====================
    
    def get_player_achievements(self) -> Dict[str, bool]:
        """Retourne les succès du joueur actuel."""
        if not self.current_player:
            return {}
        return self.current_player.achievements
    
    def set_player_achievement(self, achievement_id: str, unlocked: bool = True):
        """Définit un succès pour le joueur actuel."""
        if self.current_player:
            self.current_player.achievements[achievement_id] = unlocked
    
    def get_player_stats(self) -> Optional[PlayerStats]:
        """Retourne les stats du joueur actuel."""
        if not self.current_player:
            return None
        return self.current_player.stats
