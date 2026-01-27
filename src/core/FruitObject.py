import pygame
from pygame import  Surface
import random

class FruitObject:
    """
    """
    #TODO: Complate all methods, make collider detect mouse
    #TODO: Add smoth movement and randomize it 
    #TODO: 
    def __init__(self, screen:Surface,collider_visibility=True): 
        self.screen:Surface  = screen
        self.position:tuple[int, int] = None
        self.collision_range = 10
        self.collider:pygame.Rect  = None
        self.collider_visibility: bool = collider_visibility# <---- just for test
        
        pass
    
    def draw_collider(self)->None:
        colider = pygame.draw.circle(self.screen, (255, 255, 255), self.position, 100).inflate(75, 75)
        self.collider = colider

    def collision(self):
        #TODO: Change it to colliderect not collide
        mouse_pos = pygame.mouse.get_pos()
        if self.collider.collidepoint(mouse_pos):
            print("COLLIDE")
        
            
        pass
    
    def draw_self():
        pass
    
    def move_random():
        """
        formule = 2X^2
        """
        
        pass 

    def update(self):
        self.draw_collider()
        self.collision()
        pass
    
    