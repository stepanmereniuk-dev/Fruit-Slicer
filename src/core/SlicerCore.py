import pygame
from pygame import Surface
from .FruitObject import FruitObject

class SlicerCore():
    
    def __init__(self, screen:Surface):
        self.position:tuple[int, int] = None
        self.screen:Surface  = screen
        self.max_points = 20
        self.list_of_point = []
        self.cursor_image = pygame.image.load("src/public/images/Katana.png").convert_alpha()
        self.cursor_image = pygame.transform.scale(self.cursor_image, (52, 52))
        
    def update(self):
        self.draw_self()
        self.draw_cursor()
        
    def draw_self(self):
        #TODO: connect texture between the poits
        self.position = pygame.mouse.get_pos()
        self.list_of_point.append(self.position)
        #---REMOVE 
        if len(self.list_of_point) > self.max_points:
            self.list_of_point.pop(1)
        self.screen.fill((0, 0, 0)) 
        #---REMOVE 
        for pos in self.list_of_point:
            pygame.draw.circle(self.screen, (255, 255, 255), pos, 5)
        pass
    
    #Draw Katana
    def draw_cursor(self):
        pygame.mouse.set_visible(False)
        mouse_pos = pygame.mouse.get_pos()
        self.screen.blit(self.cursor_image, mouse_pos)
            
    def collide_with_fruit():
        
        pass
    pass