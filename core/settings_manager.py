"""
SettingsManager - User settings management.

Responsibilities:
- Load/save from settings.json
- Provide default values
- Notify changes (so main.py can change language, etc.)

Managed settings:
- control_mode: "mouse" or "keyboard"
- music_volume: 0.0 to 1.0
- sfx_volume: 0.0 to 1.0
- language: "fr" or "en"
"""

import json
import os
from typing import Optional, Callable, Dict, Any

from config import SETTINGS_FILE, ControlMode, AudioConfig


class SettingsManager:
    """
    Global settings manager.
    
    Usage:
        settings = SettingsManager()
        settings.set_music_volume(0.7)
        settings.save()
    """
    
    # Default values
    DEFAULTS = {
        'control_mode': ControlMode.DEFAULT,
        'music_volume': AudioConfig.DEFAULT_MUSIC_VOLUME,
        'sfx_volume': AudioConfig.DEFAULT_SFX_VOLUME,
        'language': 'fr',
    }
    
    def __init__(self, settings_path: str = None):
        self.settings_path = settings_path or SETTINGS_FILE
        self._settings: Dict[str, Any] = self.DEFAULTS.copy()
        
        # Callbacks to react to changes
        self._on_language_change: Optional[Callable[[str], None]] = None
        self._on_volume_change: Optional[Callable[[str, float], None]] = None
        self._on_control_mode_change: Optional[Callable[[str], None]] = None
        
        self.load()
    
    # ==================== SAVE / LOAD ====================
    
    def save(self):
        """Saves settings to the JSON file."""
        try:
            with open(self.settings_path, 'w', encoding='utf-8') as f:
                json.dump(self._settings, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Error saving settings: {e}")
    
    def load(self):
        """Loads settings from the JSON file."""
        if not os.path.exists(self.settings_path):
            # Create file with default values
            self.save()
            return
        
        try:
            with open(self.settings_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Merge with defaults (in case new settings were added)
            for key, default_value in self.DEFAULTS.items():
                self._settings[key] = data.get(key, default_value)
            
            # Validate values
            self._validate()
            
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading settings: {e}")
            # Keep defaults
    
    def _validate(self):
        """Validates and corrects values if necessary."""
        # Control mode
        if self._settings['control_mode'] not in [ControlMode.MOUSE, ControlMode.KEYBOARD]:
            self._settings['control_mode'] = ControlMode.DEFAULT
        
        # Volumes (clamp between 0 and 1)
        self._settings['music_volume'] = max(0.0, min(1.0, float(self._settings['music_volume'])))
        self._settings['sfx_volume'] = max(0.0, min(1.0, float(self._settings['sfx_volume'])))
        
        # Language
        if self._settings['language'] not in ['fr', 'en']:
            self._settings['language'] = 'fr'
    
    def reset_to_defaults(self):
        """Resets all settings to default values."""
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
        """Returns a copy of all settings."""
        return self._settings.copy()
    
    # ==================== SETTERS ====================
    
    def set_control_mode(self, mode: str):
        """Changes the control mode (mouse/keyboard)."""
        if mode not in [ControlMode.MOUSE, ControlMode.KEYBOARD]:
            return
        
        old_mode = self._settings['control_mode']
        self._settings['control_mode'] = mode
        
        if old_mode != mode and self._on_control_mode_change:
            self._on_control_mode_change(mode)
        
        self.save()
    
    def set_music_volume(self, volume: float):
        """Changes the music volume (0.0 to 1.0)."""
        volume = max(0.0, min(1.0, volume))
        self._settings['music_volume'] = volume
        
        if self._on_volume_change:
            self._on_volume_change('music', volume)
        
        self.save()
    
    def set_sfx_volume(self, volume: float):
        """Changes the sound effects volume (0.0 to 1.0)."""
        volume = max(0.0, min(1.0, volume))
        self._settings['sfx_volume'] = volume
        
        if self._on_volume_change:
            self._on_volume_change('sfx', volume)
        
        self.save()
    
    def set_language(self, lang: str):
        """Changes the language (fr/en)."""
        if lang not in ['fr', 'en']:
            return
        
        old_lang = self._settings['language']
        self._settings['language'] = lang
        
        if old_lang != lang and self._on_language_change:
            self._on_language_change(lang)
        
        self.save()
    
    # ==================== CALLBACKS ====================
    
    def on_language_change(self, callback: Callable[[str], None]):
        """Registers a callback called when the language changes."""
        self._on_language_change = callback
    
    def on_volume_change(self, callback: Callable[[str, float], None]):
        """Registers a callback called when a volume changes."""
        self._on_volume_change = callback
    
    def on_control_mode_change(self, callback: Callable[[str], None]):
        """Registers a callback called when the control mode changes."""
        self._on_control_mode_change = callback


# Global instance (singleton)
_instance: Optional[SettingsManager] = None


def init(settings_path: str = None) -> SettingsManager:
    """Initializes the global instance. Call once at startup."""
    global _instance
    _instance = SettingsManager(settings_path)
    return _instance


def get_instance() -> Optional[SettingsManager]:
    """Returns the global instance."""
    return _instance


def get(key: str, default=None):
    """Shortcut to retrieve a value."""
    if _instance is None:
        return default
    return _instance.get_all().get(key, default)