"""
LangManager - Gestionnaire de langues pour Fruit Slicer
Charge les fichiers JSON de traduction et fournit les textes traduits.
"""

import json
import os
from typing import Dict, Any, Optional


class LangManager:
    """Gestionnaire centralisé des traductions."""
    
    SUPPORTED_LANGUAGES = ["fr", "en"]
    DEFAULT_LANGUAGE = "fr"
    
    def __init__(self, lang_dir: str):
        """
        Args:
            lang_dir: Chemin vers le dossier contenant fr.json et en.json
        """
        self.lang_dir = lang_dir
        self.current_lang = self.DEFAULT_LANGUAGE
        self.translations: Dict[str, Any] = {}
        self._load_language(self.current_lang)
    
    def _load_language(self, lang_code: str) -> bool:
        """Charge un fichier de traduction JSON en mémoire."""
        file_path = os.path.join(self.lang_dir, f"{lang_code}.json")
        
        if not os.path.exists(file_path):
            return False
        
        with open(file_path, "r", encoding="utf-8") as file:
            self.translations = json.load(file)
        
        return True
    
    def set_language(self, lang_code: str) -> bool:
        """Change la langue active. Retourne True si réussi."""
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
        Récupère un texte traduit via sa clé hiérarchique.
        
        Exemple:
            get("menu.title") -> "Fruit Slicer"
            get("game.combo_text", count=3) -> "COMBO x3"
        """
        # Parcourir la hiérarchie (ex: "menu.title" -> ["menu", "title"])
        segments = key.split(".")
        value = self.translations
        
        for segment in segments:
            if not isinstance(value, dict) or segment not in value:
                return key  # Clé non trouvée
            value = value[segment]
        
        if not isinstance(value, str):
            return key
        
        # Substituer les variables si présentes
        if kwargs:
            value = value.format(**kwargs)
        
        return value
    
    def get_language(self) -> str:
        """Retourne le code de la langue active ("fr" ou "en")."""
        return self.current_lang
    
    def get_language_name(self) -> str:
        """Retourne le nom de la langue ("Français" ou "English")."""
        return self.get("_meta.language")


# Instance globale
_instance: Optional[LangManager] = None


def init(lang_dir: str) -> LangManager:
    """Initialise l'instance globale. À appeler une fois au démarrage."""
    global _instance
    _instance = LangManager(lang_dir)
    return _instance


def get_instance() -> Optional[LangManager]:
    """Retourne l'instance globale du LangManager."""
    return _instance


def get(key: str, **kwargs) -> str:
    """Raccourci pour récupérer un texte depuis l'instance globale."""
    if _instance is None:
        return key
    return _instance.get(key, **kwargs)
