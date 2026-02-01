"""
PlayerManager - Management of players and their data.

Responsibilities:
- Create/load player profiles by username
- Manage high scores (4 categories)
- Track whether the tutorial has been seen
- Save/load from save_data.json
"""

import json
import os
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict, field

from config import SAVE_FILE


@dataclass
class PlayerData:
    """Data for a single player."""
    pseudo: str
    high_scores: Dict[str, int] = field(default_factory=lambda: {
        'classic_easy': 0,
        'classic_normal': 0,
        'classic_hard': 0,
        'challenge': 0,
    })
    tutorial_seen: bool = False
    total_games: int = 0
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'PlayerData':
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
        )


class PlayerManager:
    """
    Manages player profiles.
    
    Usage:
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
    
    # ==================== SAVE ====================
    
    def save(self):
        """Save all players to the file."""
        # Load existing data (to avoid overwriting achievements)
        existing_data = {}
        if os.path.exists(self.save_path):
            try:
                with open(self.save_path, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
            except (IOError, json.JSONDecodeError):
                pass
        
        # Update the players section
        existing_data['players'] = {
            pseudo: player.to_dict() 
            for pseudo, player in self.players.items()
        }
        
        try:
            with open(self.save_path, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, indent=2, ensure_ascii=False)
        except IOError:
            pass
    
    def load(self):
        """Load players from the file."""
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
    
    # ==================== PLAYER MANAGEMENT ====================
    
    def set_current_player(self, pseudo: str) -> PlayerData:
        """
        Set the current player. Creates the profile if it is new.
        Returns the player's data.
        """
        pseudo = self._sanitize_pseudo(pseudo)
        
        if pseudo not in self.players:
            self.players[pseudo] = PlayerData(pseudo=pseudo)
            self.save()
        
        self.current_player = self.players[pseudo]
        return self.current_player
    
    def get_player(self, pseudo: str) -> Optional[PlayerData]:
        """Return a player's data or None."""
        return self.players.get(pseudo)
    
    def get_all_pseudos(self) -> List[str]:
        """Return the list of all usernames."""
        return list(self.players.keys())
    
    def player_exists(self, pseudo: str) -> bool:
        """Check if a player exists."""
        return pseudo in self.players
    
    def is_new_player(self, pseudo: str) -> bool:
        """Check if this is a new player (for the tutorial)."""
        player = self.players.get(pseudo)
        if not player:
            return True
        return not player.tutorial_seen
    
    def _sanitize_pseudo(self, pseudo: str) -> str:
        """Clean the username (letters only, max 10 characters)."""
        # Keep only letters
        clean = ''.join(c for c in pseudo if c.isalpha())
        # Limit to 10 characters
        return clean[:10]
    
    # ==================== HIGH SCORES ====================
    
    def update_high_score(self, category: str, score: int) -> bool:
        """
        Update the high score if the new score is higher.
        Returns True if a new record was set.
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
        """Return the current player's high score for a category."""
        if not self.current_player:
            return 0
        return self.current_player.high_scores.get(category, 0)
    
    def get_category_key(self, mode: str, difficulty: str) -> str:
        """Return the category key for the high score."""
        if mode == 'challenge':
            return 'challenge'
        return f'classic_{difficulty}'
    
    # ==================== LEADERBOARD ====================
    
    def get_leaderboard(self, category: str, limit: int = 10) -> List[Dict]:
        """
        Return the leaderboard for a category.
        Format: [{'rank': 1, 'pseudo': 'Yoshi', 'score': 150}, ...]
        """
        # Collect scores
        scores = []
        for pseudo, player in self.players.items():
            score = player.high_scores.get(category, 0)
            if score > 0:
                scores.append({'pseudo': pseudo, 'score': score})
        
        # Sort by score descending
        scores.sort(key=lambda x: x['score'], reverse=True)
        
        # Add ranks and limit
        leaderboard = []
        for i, entry in enumerate(scores[:limit]):
            leaderboard.append({
                'rank': i + 1,
                'pseudo': entry['pseudo'],
                'score': entry['score'],
            })
        
        return leaderboard
    
    # ==================== TUTORIAL ====================
    
    def mark_tutorial_seen(self):
        """Mark the tutorial as seen for the current player."""
        if self.current_player:
            self.current_player.tutorial_seen = True
            self.save()
    
    def should_show_tutorial(self) -> bool:
        """Return True if the tutorial should be shown."""
        if not self.current_player:
            return True
        return not self.current_player.tutorial_seen
    
    # ==================== STATS ====================
    
    def increment_games_played(self):
        """Increment the counter of games played."""
        if self.current_player:
            self.current_player.total_games += 1
            self.save()
            