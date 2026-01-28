import pygame
from pygame import Surface
from .core.SlicerCore import SlicerCore
from .core.FruitObject import FruitObject


    

def StarGame():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Fruit Ninja Clone")
    clock = pygame.time.Clock()
    running = True
    
    # --------------OBJECTS------------#
    slicer = SlicerCore(screen)
    fruit = FruitObject(screen, slicer=slicer)  
    
    in_menu = True 
    # --------------OBJECTS------------#
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if in_menu and event.key == pygame.K_SPACE:
                    in_menu = False 
        
        screen.fill((50, 150, 255)) 
        

        slicer.update()
        fruit.update()  #
        
        pygame.display.flip()
        clock.tick(60) 

    pygame.quit()


if __name__ == "__main__":
    StarGame()