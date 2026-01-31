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
from scene_manager import SceneManager


def main():
    # Initialisation Pygame
    pygame.init()
    pygame.mixer.init()
    
    # Création de la fenêtre
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()
    
    # Initialisation du système de langues
    lang_manager.init(LANG_DIR)
    
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


if __name__ == "__main__":
    main()
