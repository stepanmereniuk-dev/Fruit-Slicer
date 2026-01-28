import pygame
from pygame import  Surface, Rect

import random
import math

class FruitObject:
    """
    """
    #TODO: FINISHED - Complate all methods, make collider detect mouse
    #TODO: Add smoth0 movement and randomize it 
    #TODO: 
    def __init__(self, screen:Surface,collider_visibility=True,slicer = None,): 
        from .SlicerCore import SlicerCore
        self.screen:Surface  = screen
        self.collision_range = 10
        self.collider:pygame.Rect  = None
        self.collider_visibility: bool = collider_visibility# <---- just for test
        self.is_cated = False
        self.radius = 100
        self.slicer:SlicerCore = slicer
        self.list_of_images = pygame.image.load("src/assets/images/apple_PNG12423.png").convert_alpha()
        self.image = pygame.transform.scale(self.list_of_images, (60, 60)) 
        
        #--------------------ParabolaSettings--------------------------#
        #coef
        # y = ax^x2 + bx + c
        self.a = 0.01
        self.b = 0
        self.c = 0
        
        self.trail = []
        self.reset_parabola()  
        #--------------------ParabolaSettings--------------------------#
        pass

    def reset_parabola(self):
        self.vertex_y = random.uniform(80, 220)                  
        self.a = random.uniform(0.0008, 0.0022)                  
        self.dx = random.uniform(3.8, 6.8) * random.choice([-1, 1])
        
        screen_w = self.screen.get_width()
        screen_h = self.screen.get_height()
        

        if self.dx > 0:
            initial_rel_x = -random.uniform(600, 1000)   
            self.start_x = random.randint(350, screen_w - 150)
        else:
            initial_rel_x = random.uniform(600, 1000)   
            self.start_x = random.randint(150, screen_w - 350)
        
        self.position = [0.0, 0.0]
        self.position[0] = self.start_x + initial_rel_x
        
        rel_x = self.position[0] - self.start_x
        self.position[1] = self.vertex_y + self.a * rel_x ** 2  
        
        self.trail = []
        self.is_cated = False
    
    def draw_collider(self) -> None:
        rect2 = pygame.Rect(0, 0, 60, 60)
        rect2.center = (int(self.position[0]), int(self.position[1]))
        image_rect = self.image.get_rect(center=rect2.center)
        self.screen.blit(self.image, image_rect)

        if len(self.trail) > 1:
            pygame.draw.lines(self.screen, (255, 255, 0), False, self.trail, 4)
        
        #TRIGGER
        if self.slicer: 
            if rect2.colliderect(self.slicer.colision_rectangle):
                print("Collision")
                self.is_cated = True
                color = (255, 0, 0)
            else:
                color = (255, 255, 0)
        else:
            color = (255, 255, 0)
        #DRAW 
        pygame.draw.rect(self.screen, color, rect2, width=6, border_radius=1)
    
    def collision(self):
        
        pass
     
    def draw_self(self):
        pass
    
    def move_random(self):
        if not self.is_cated:
            self.position[0] += self.dx
            rel_x = self.position[0] - self.start_x
            self.position[1] = self.vertex_y + self.a * rel_x ** 2
            
            #TRAGECTORY
            self.trail.append((int(self.position[0]), int(self.position[1])))
            if len(self.trail) > 400:
                self.trail.pop(0)
            
            if (self.position[1] > self.screen.get_height() + 150 or
                self.position[0] < -300 or self.position[0] > self.screen.get_width() + 300):
                self.reset_parabola()

    def update(self):
        self.move_random()
        self.collision()
        self.draw_collider()
        pass