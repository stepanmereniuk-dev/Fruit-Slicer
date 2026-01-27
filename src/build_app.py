import pygame
from pygame import Surface
from .core.SlicerCore import SlicerCore
from .core.FruitObject import FruitObject




def draw_menu(sceen: Surface):
    pygame.draw.rect()
    
    
    pass


def StarGame():
    #-------------------------#
    
    #-------------------------#
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    #--------------OBJECTS------------#
    s = SlicerCore(screen)
    f = FruitObject(screen)
    f.position = (200,200)
    #--------------OBJECTS------------#
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        s.update()
        f.draw_collider()
        
        pygame.display.flip()
        clock.tick(60) 

    pygame.quit()