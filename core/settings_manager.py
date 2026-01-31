"""
SettingsManager - Gestion des paramètres utilisateur.

Responsabilités :
- Charger/sauvegarder depuis settings.json
- Fournir les valeurs par défaut
- Notifier les changements (pour que main.py puisse changer la langue, etc.)

Paramètres gérés :
- control_mode : "mouse" ou "keyboard"
- music_volume : 0.0 à 1.0
- sfx_volume : 0.0 à 1.0
- language : "fr" ou "en"
"""

import json
import os
from typing import Optional, Callable, Dict, Any

from config import SETTINGS_FILE, ControlMode, AudioConfig


class SettingsManager:
    """
    Gestionnaire des paramètres globaux.
    
    Utilisation :
        settings = SettingsManager()
        settings.set_music_volume(0.7)
        settings.save()
    """
    
    # Valeurs par défaut
    DEFAULTS = {
        'control_mode': ControlMode.DEFAULT,
        'music_volume': AudioConfig.DEFAULT_MUSIC_VOLUME,
        'sfx_volume': AudioConfig.DEFAULT_SFX_VOLUME,
        'language': 'fr',
    }
    
    def __init__(self, settings_path: str = None):
        self.settings_path = settings_path or SETTINGS_FILE
        self._settings: Dict[str, Any] = self.DEFAULTS.copy()
        
        # Callbacks pour réagir aux changements
        self._on_language_change: Optional[Callable[[str], None]] = None
        self._on_volume_change: Optional[Callable[[str, float], None]] = None
        self._on_control_mode_change: Optional[Callable[[str], None]] = None
        
        self.load()
    
    # ==================== SAUVEGARDE / CHARGEMENT ====================
    
    def save(self):
        """Sauvegarde les paramètres dans le fichier JSON."""
        try:
            with open(self.settings_path, 'w', encoding='utf-8') as f:
                json.dump(self._settings, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Erreur sauvegarde settings: {e}")
    
    def load(self):
        """Charge les paramètres depuis le fichier JSON."""
        if not os.path.exists(self.settings_path):
            # Créer le fichier avec les valeurs par défaut
            self.save()
            return
        
        try:
            with open(self.settings_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Fusionner avec les valeurs par défaut (au cas où de nouveaux paramètres existent)
            for key, default_value in self.DEFAULTS.items():
                self._settings[key] = data.get(key, default_value)
            
            # Valider les valeurs
            self._validate()
            
        except (IOError, json.JSONDecodeError) as e:
            print(f"Erreur chargement settings: {e}")
            # Garder les valeurs par défaut
    
    def _validate(self):
        """Valide et corrige les valeurs si nécessaire."""
        # Control mode
        if self._settings['control_mode'] not in [ControlMode.MOUSE, ControlMode.KEYBOARD]:
            self._settings['control_mode'] = ControlMode.DEFAULT
        
        # Volumes (clamp entre 0 et 1)
        self._settings['music_volume'] = max(0.0, min(1.0, float(self._settings['music_volume'])))
        self._settings['sfx_volume'] = max(0.0, min(1.0, float(self._settings['sfx_volume'])))
        
        # Langue
        if self._settings['language'] not in ['fr', 'en']:
            self._settings['language'] = 'fr'
    
    def reset_to_defaults(self):
        """Remet tous les paramètres aux valeurs par défaut."""
        self._settings = self.DEFAULTS.copy()
        self.save()
    
    # ==================== GETTERS ====================
    
    @property
    def control_mode(self) -> str:
        return self._settings['control_mode']
    
    @property
    def music_volume(self) -> float:
        return self._settings['music_volume']
    
    @property
    def sfx_volume(self) -> float:
        return self._settings['sfx_volume']
    
    @property
    def language(self) -> str:
        return self._settings['language']
    
    def get_all(self) -> Dict[str, Any]:
        """Retourne une copie de tous les paramètres."""
        return self._settings.copy()
    
    # ==================== SETTERS ====================
    
    def set_control_mode(self, mode: str):
        """Change le mode de contrôle (mouse/keyboard)."""
        if mode not in [ControlMode.MOUSE, ControlMode.KEYBOARD]:
            return
        
        old_mode = self._settings['control_mode']
        self._settings['control_mode'] = mode
        
        if old_mode != mode and self._on_control_mode_change:
            self._on_control_mode_change(mode)
        
        self.save()
    
    def set_music_volume(self, volume: float):
        """Change le volume de la musique (0.0 à 1.0)."""
        volume = max(0.0, min(1.0, volume))
        self._settings['music_volume'] = volume
        
        if self._on_volume_change:
            self._on_volume_change('music', volume)
        
        self.save()
    
    def set_sfx_volume(self, volume: float):
        """Change le volume des effets sonores (0.0 à 1.0)."""
        volume = max(0.0, min(1.0, volume))
        self._settings['sfx_volume'] = volume
        
        if self._on_volume_change:
            self._on_volume_change('sfx', volume)
        
        self.save()
    
    def set_language(self, lang: str):
        """Change la langue (fr/en)."""
        if lang not in ['fr', 'en']:
            return
        
        old_lang = self._settings['language']
        self._settings['language'] = lang
        
        if old_lang != lang and self._on_language_change:
            self._on_language_change(lang)
        
        self.save()
    
    # ==================== CALLBACKS ====================
    
    def on_language_change(self, callback: Callable[[str], None]):
        """Enregistre un callback appelé quand la langue change."""
        self._on_language_change = callback
    
    def on_volume_change(self, callback: Callable[[str, float], None]):
        """Enregistre un callback appelé quand un volume change."""
        self._on_volume_change = callback
    
    def on_control_mode_change(self, callback: Callable[[str], None]):
        """Enregistre un callback appelé quand le mode de contrôle change."""
        self._on_control_mode_change = callback


# Instance globale (singleton)
_instance: Optional[SettingsManager] = None


def init(settings_path: str = None) -> SettingsManager:
    """Initialise l'instance globale. À appeler une fois au démarrage."""
    global _instance
    _instance = SettingsManager(settings_path)
    return _instance


def get_instance() -> Optional[SettingsManager]:
    """Retourne l'instance globale."""
    return _instance


def get(key: str, default=None):
    """Raccourci pour récupérer une valeur."""
    if _instance is None:
        return default
    return _instance.get_all().get(key, default)
