"""
Fruit Slicer - Game entry point
Initializes Pygame and starts the main loop.
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
    # Pygame initialization
    pygame.init()
    pygame.mixer.init()
    
    # Window creation
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()
    
    # User settings initialization
    settings = settings_manager.init()
    
    # Language system initialization with the saved language
    lang_manager.init(LANG_DIR)
    lang_manager.get_instance().set_language(settings.language)
    
    # Synchronize language changes
    settings.on_language_change(
        lambda lang: lang_manager.get_instance().set_language(lang)
    )
    
    # Synchronize audio volume changes
    settings.on_volume_change(_on_volume_change)
    
    # Apply initial volumes
    pygame.mixer.music.set_volume(settings.music_volume)
    
    # Scene manager creation
    scene_manager = SceneManager(screen)
    
    # Main loop
    running = True
    while running:
        # Delta time in seconds
        dt = clock.tick(FPS) / 1000.0
        
        # Retrieve events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        
        # Update active scene
        scene_manager.handle_events(events)
        scene_manager.update(dt)
        
        # Rendering
        scene_manager.render()
        
        # Display FPS (debug)
        if SHOW_FPS:
            fps = int(clock.get_fps())
            font = pygame.font.Font(None, 30)
            fps_text = font.render(f"FPS: {fps}", True, (255, 255, 255))
            screen.blit(fps_text, (10, 10))
        
        pygame.display.flip()
    
    # Clean shutdown
    pygame.quit()
    sys.exit()


def _on_volume_change(volume_type: str, volume: float):
    """Callback called when a volume setting changes."""
    if volume_type == 'music':
        pygame.mixer.music.set_volume(volume)
    # Note: For SFX, each sound should be played with the correct volume
    # via settings_manager.get_instance().sfx_volume


if __name__ == "__main__":
    main()