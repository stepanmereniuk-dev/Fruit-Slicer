"""
Fruit Slicer - Point d'entrée du jeu
Initialise Pygame et lance la boucle principale.
"""

import pygame
import sys

from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, 
    FPS, LANG_DIR, SHOW_FPS
)
from core import lang_manager
from core import settings_manager
from scene_manager import SceneManager


def main():
    # Initialisation Pygame
    pygame.init()
    pygame.mixer.init()
    
    # Création de la fenêtre
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()
    
    # Initialisation des paramètres utilisateur
    settings = settings_manager.init()
    
    # Initialisation du système de langues avec la langue sauvegardée
    lang_manager.init(LANG_DIR)
    lang_manager.get_instance().set_language(settings.language)
    
    # Synchroniser les changements de langue
    settings.on_language_change(
        lambda lang: lang_manager.get_instance().set_language(lang)
    )
    
    # Synchroniser les volumes audio
    settings.on_volume_change(_on_volume_change)
    
    # Appliquer les volumes initiaux
    pygame.mixer.music.set_volume(settings.music_volume)
    
    # Création du gestionnaire de scènes
    scene_manager = SceneManager(screen)
    
    # Boucle principale
    running = True
    while running:
        # Delta time en secondes
        dt = clock.tick(FPS) / 1000.0
        
        # Récupération des événements
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        
        # Mise à jour de la scène active
        scene_manager.handle_events(events)
        scene_manager.update(dt)
        
        # Rendu
        scene_manager.render()
        
        # Affichage FPS (debug)
        if SHOW_FPS:
            fps = int(clock.get_fps())
            font = pygame.font.Font(None, 30)
            fps_text = font.render(f"FPS: {fps}", True, (255, 255, 255))
            screen.blit(fps_text, (10, 10))
        
        pygame.display.flip()
    
    # Fermeture propre
    pygame.quit()
    sys.exit()


def _on_volume_change(volume_type: str, volume: float):
    """Callback appelé quand un volume change dans les settings."""
    if volume_type == 'music':
        pygame.mixer.music.set_volume(volume)
    # Note: Pour les SFX, chaque son devra être joué avec le bon volume
    # via settings_manager.get_instance().sfx_volume


if __name__ == "__main__":
    main()
