"""
LangManager - Language manager for Fruit Slicer
Loads translation JSON files and provides translated texts.
"""

import json
import os
from typing import Dict, Any, Optional


class LangManager:
    """Centralized translation manager."""
    
    SUPPORTED_LANGUAGES = ["fr", "en"]
    DEFAULT_LANGUAGE = "fr"
    
    def __init__(self, lang_dir: str):
        """
        Args:
            lang_dir: Path to the folder containing fr.json and en.json
        """
        self.lang_dir = lang_dir
        self.current_lang = self.DEFAULT_LANGUAGE
        self.translations: Dict[str, Any] = {}
        self._load_language(self.current_lang)
    
    def _load_language(self, lang_code: str) -> bool:
        """Loads a translation JSON file into memory."""
        file_path = os.path.join(self.lang_dir, f"{lang_code}.json")
        
        if not os.path.exists(file_path):
            return False
        
        with open(file_path, "r", encoding="utf-8") as file:
            self.translations = json.load(file)
        
        return True
    
    def set_language(self, lang_code: str) -> bool:
        """Changes the active language. Returns True if successful."""
        if lang_code not in self.SUPPORTED_LANGUAGES:
            return False
        
        if lang_code == self.current_lang:
            return True
        
        if self._load_language(lang_code):
            self.current_lang = lang_code
            return True
        
        return False
    
    def get(self, key: str, **kwargs) -> str:
        """
        Retrieves a translated text using its hierarchical key.
        
        Example:
            get("menu.title") -> "Fruit Slicer"
            get("game.combo_text", count=3) -> "COMBO x3"
        """
        # Traverse the hierarchy (e.g., "menu.title" -> ["menu", "title"])
        segments = key.split(".")
        value = self.translations
        
        for segment in segments:
            if not isinstance(value, dict) or segment not in value:
                return key  # Key not found
            value = value[segment]
        
        if not isinstance(value, str):
            return key
        
        # Substitute variables if present
        if kwargs:
            value = value.format(**kwargs)
        
        return value
    
    def get_language(self) -> str:
        """Returns the code of the active language ("fr" or "en")."""
        return self.current_lang
    
    def get_language_name(self) -> str:
        """Returns the name of the language ("French" or "English")."""
        return self.get("_meta.language")


# Global instance
_instance: Optional[LangManager] = None


def init(lang_dir: str) -> LangManager:
    """Initializes the global instance. Call once at startup."""
    global _instance
    _instance = LangManager(lang_dir)
    return _instance


def get_instance() -> Optional[LangManager]:
    """Returns the global instance of LangManager."""
    return _instance


def get(key: str, **kwargs) -> str:
    """Shortcut to retrieve a text from the global instance."""
    if _instance is None:
        return key
    return _instance.get(key, **kwargs)