"""
AudioManager - Gestionnaire audio centralisé pour Fruit Slicer.

Responsabilités :
- Musique de fond en boucle (partout dans le jeu)
- SFX avec gestion du volume
- Son d'alerte bombe (joue en continu tant qu'une bombe est visible)
- Intégration avec SettingsManager pour les volumes
"""

import pygame
import os
from typing import Optional, Dict

from config import SOUNDS_DIR


class AudioManager:
    """
    Gestionnaire audio centralisé.
    
    Utilisation :
        audio = AudioManager()
        audio.play_music()
        audio.play_sfx('freeze')
        audio.start_bomb_alert()  # Quand une bombe apparaît
        audio.stop_bomb_alert()   # Quand toutes les bombes ont disparu
    """
    
    # Fichiers audio
    MUSIC_FILE = "background_music.mp3"
    SFX_FILES = {
        'bomb_alert': "bo-bombs_spawn.mp3",
        'freeze': "freeze.mp3",
        'game_over': "game_over.mp3",
        # Futurs SFX à ajouter ici :
        # 'slice': "slice.mp3",
        # 'heart_lost': "heart_lost.mp3",
        # 'combo': "combo.mp3",
        # 'achievement': "achievement.mp3",
    }
    
    def __init__(self):
        # Volumes (0.0 à 1.0)
        self._music_volume = 0.1
        self._sfx_volume = 1.0
        
        # État
        self._music_playing = False
        self._bomb_alert_playing = False
        
        # Charger les SFX
        self._sfx_sounds: Dict[str, pygame.mixer.Sound] = {}
        self._load_sounds()
        
        # Channel dédié pour l'alerte bombe (pour pouvoir l'arrêter)
        self._bomb_channel: Optional[pygame.mixer.Channel] = None
    
    def _load_sounds(self):
        """Charge tous les fichiers SFX en mémoire."""
        for sfx_name, filename in self.SFX_FILES.items():
            filepath = os.path.join(SOUNDS_DIR, filename)
            if os.path.exists(filepath):
                try:
                    self._sfx_sounds[sfx_name] = pygame.mixer.Sound(filepath)
                except pygame.error as e:
                    print(f"Erreur chargement SFX '{sfx_name}': {e}")
            else:
                print(f"Fichier SFX introuvable: {filepath}")
    
    # ==================== VOLUMES ====================
    
    def set_music_volume(self, volume: float):
        """Change le volume de la musique (0.0 à 1.0)."""
        self._music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self._music_volume)
    
    def set_sfx_volume(self, volume: float):
        """Change le volume des SFX (0.0 à 1.0)."""
        self._sfx_volume = max(0.0, min(1.0, volume))
        # Mettre à jour le volume de tous les sons chargés
        for sound in self._sfx_sounds.values():
            sound.set_volume(self._sfx_volume)
    
    @property
    def music_volume(self) -> float:
        return self._music_volume
    
    @property
    def sfx_volume(self) -> float:
        return self._sfx_volume
    
    # ==================== MUSIQUE ====================
    
    def play_music(self):
        """Lance la musique de fond en boucle infinie."""
        if self._music_playing:
            return
        
        music_path = os.path.join(SOUNDS_DIR, self.MUSIC_FILE)
        if not os.path.exists(music_path):
            print(f"Musique introuvable: {music_path}")
            return
        
        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(self._music_volume)
            pygame.mixer.music.play(-1)  # -1 = boucle infinie
            self._music_playing = True
        except pygame.error as e:
            print(f"Erreur lecture musique: {e}")
    
    def stop_music(self):
        """Arrête la musique de fond."""
        pygame.mixer.music.stop()
        self._music_playing = False
    
    def pause_music(self):
        """Met la musique en pause."""
        pygame.mixer.music.pause()
    
    def resume_music(self):
        """Reprend la musique après une pause."""
        pygame.mixer.music.unpause()
    
    @property
    def is_music_playing(self) -> bool:
        return self._music_playing and pygame.mixer.music.get_busy()
    
    # ==================== SFX ====================
    
    def play_sfx(self, sfx_name: str):
        """
        Joue un effet sonore une fois.
        
        Args:
            sfx_name: Nom du SFX ('freeze', 'game_over', etc.)
        """
        sound = self._sfx_sounds.get(sfx_name)
        if sound:
            sound.set_volume(self._sfx_volume)
            sound.play()
        else:
            print(f"SFX inconnu: {sfx_name}")
    
    # ==================== ALERTE BOMBE ====================
    
    def start_bomb_alert(self):
        """
        Démarre le son d'alerte bombe en boucle.
        Ne fait rien si déjà en cours (évite la superposition).
        """
        if self._bomb_alert_playing:
            return
        
        sound = self._sfx_sounds.get('bomb_alert')
        if not sound:
            return
        
        # Trouver un channel disponible
        self._bomb_channel = pygame.mixer.find_channel()
        if self._bomb_channel:
            sound.set_volume(self._sfx_volume)
            self._bomb_channel.play(sound, loops=-1)  # -1 = boucle infinie
            self._bomb_alert_playing = True
    
    def stop_bomb_alert(self):
        """Arrête le son d'alerte bombe."""
        if not self._bomb_alert_playing:
            return
        
        if self._bomb_channel:
            self._bomb_channel.stop()
            self._bomb_channel = None
        
        self._bomb_alert_playing = False
    
    @property
    def is_bomb_alert_playing(self) -> bool:
        return self._bomb_alert_playing
    
    # ==================== CLEANUP ====================
    
    def cleanup(self):
        """Arrête tous les sons (à appeler à la fermeture du jeu)."""
        self.stop_bomb_alert()
        self.stop_music()


# Instance globale (singleton)
_instance: Optional[AudioManager] = None


def init() -> AudioManager:
    """Initialise l'instance globale. À appeler une fois au démarrage."""
    global _instance
    _instance = AudioManager()
    return _instance


def get_instance() -> Optional[AudioManager]:
    """Retourne l'instance globale."""
    return _instance


def play_sfx(sfx_name: str):
    """Raccourci pour jouer un SFX."""
    if _instance:
        _instance.play_sfx(sfx_name)


def start_bomb_alert():
    """Raccourci pour démarrer l'alerte bombe."""
    if _instance:
        _instance.start_bomb_alert()


def stop_bomb_alert():
    """Raccourci pour arrêter l'alerte bombe."""
    if _instance:
        _instance.stop_bomb_alert()
