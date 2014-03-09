# -*- coding: utf-8 -*-
"""
Created on Sat Mar  8 18:09:47 2014

@author: flymperopoulos
"""
import pygame
from pygame.locals import *

class FloppyBird:
    
    def __init__(self):
        
        pygame.init()
        
        infoObject = pygame.display.Info()
        screenWidth,screenHeight = infoObject.current_w, infoObject.current_h
        height=screenHeight/2
        width=height
        
        self.screen = pygame.display.set_mode((width,height))
        pygame.display.set_caption('Floppy Bird')
        
        self.clock=pygame.time.Clock()
        self.bird=Bird(self.screen)             
        
    def update(self):
        self.clock.tick(60)
        
        self.screen.fill((12,241,52))
        for event in pygame.event.get():
            if event.type==QUIT:
                exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self.bird.jump()
                
        self.bird.update()
        
        pygame.display.flip()
        
class Bird:
    
    def __init__(self,screen):
        self.screen=screen
        
        self.radius=self.screen.get_width()/40.0
        self.yposition=self.screen.get_height()/2.0
        self.yvelocity=0.0
        self.acceleration=self.screen.get_height()/1800.0
        self.xposition=self.screen.get_width()/5.0        
        self.color = (255,255,255)
        
    def update_position(self):
        self.yposition +=self.yvelocity
        self.yvelocity += self.acceleration
        if self.yposition>self.screen.get_height()-self.radius:
            self.yposition=self.screen.get_height()-self.radius
            
    def jump(self):
        self.yvelocity=-10.0
    
    def update(self):
        self.update_position()
        pygame.draw.circle(self.screen,(120,12,32),(int(self.xposition),int(self.yposition)),int(self.radius),0)
        
        

if __name__ =='__main__':
    game = FloppyBird()
    while 1:
        game.update()
    