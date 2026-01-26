import pygame
from .core.SlicerCore import SlicerCore





def draw_menu():
    
    pass


def StarGame():
    #-------------------------#
    
    #-------------------------#
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    s = SlicerCore(screen)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        s.update()
        
        pygame.display.flip()
        clock.tick(60) 

    pygame.quit()