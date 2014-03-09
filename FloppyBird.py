# -*- coding: utf-8 -*-
"""
Created on Sat Mar  8 18:09:47 2014

@author: flymperopoulos
"""
import pygame
from pygame.locals import *
import os
from os import chdir
from random import *
from os.path import dirname

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
        self.score =0

        self.bird=Bird(self.screen)
     
        self.startGame = False

        self.pipes = []    
        
    def display_score(self):
        message = 'Score: ' + str(self.score)
        fontobject=pygame.font.SysFont('Arial', 18)
        if len(message) != 0:
            self.screen.blit(fontobject.render(message, 1, (255, 255, 255)),((self.screen.get_width()*0.8), 0))
            
    def display_loss(self):
        message = 'YOU LOST'
        fontobject=pygame.font.SysFont('Arial', 50)
        self.screen.blit(fontobject.render(message, 1, (255, 255, 255)),(self.screen.get_width()/4.0,self.screen.get_height()/2.5))
        
    
    def update_display_score(self):
        self.score += 1

 
    def update_pipes(self):
        if len(self.pipes)==0:
            self.pipes.append(Pipe(self.screen))
        if self.pipes[0].x<=-1*self.pipes[0].width:
            self.pipes.pop(0)
        if self.pipes[-1].x==self.screen.get_width()-250:
            self.pipes.append(Pipe(self.screen))
    
    def game(self):
            
        if self.bird.yposition>=self.screen.get_height()-self.bird.radius:
            return False
        else:
            return True
#        elif self.pipes:  
#            for pipe in self.pipes:
#                if self.bird.xposition == range(pipe.x, pipe.x+ pipe.width) and self.bird.yposition == range( 0,pipe.y+ pipe.length1+ pipe.space):
#                    return False
        
        
        
    def update(self):
        self.clock.tick(60)
        
        self.screen.fill((12,241,52))
        for event in pygame.event.get():
            if event.type==QUIT:
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit()
                if event.key == K_SPACE:
                    self.startGame=True
                    self.bird.jump()
        
        if self.game():
            self.display_score()
            
            for pipe in self.pipes:
                pipe.update()
                if self.bird.xposition == pipe.x:
                    self.update_display_score()
            self.update_pipes()
            self.bird.update()
        else:
           self.display_loss()
        
        pygame.display.flip()
        
class Bird:
    
    def __init__(self,screen):
        self.screen=screen
        temppic=pygame.image.load(os.path.join('','paul.png'))
        self.picture=pygame.transform.scale(temppic,(int(temppic.get_width()*0.4),int(temppic.get_height()*0.4)))
        self.yposition=self.screen.get_height()/2.0
        self.yvelocity=0.0
        self.acceleration=self.screen.get_height()/1800.0
        self.xposition=self.screen.get_width()/5.0        

    def update_position(self):
        self.yposition +=self.yvelocity
        self.yvelocity += self.acceleration
        if self.yposition>self.screen.get_height()-self.picture.get_height()*0.5:                
            self.yposition=self.screen.get_height()-self.picture.get_height()*0.5
            
    def jump(self):
        self.yvelocity=-7.0
        
#    def rotate(self):
#        orig_rect = self.picture.get_rect()
#        rot_image = pygame.transform.rotate(self.picture,10)
#        rot_rect = orig_rect.copy()
#        rot_rect.center = rot_image.get_rect().center
#        rot_image = rot_image.subsurface(rot_rect).copy()
#        self.picture=rot_image
        
    def update(self):
#        self.rotate()
        self.update_position()
        self.screen.blit(self.picture,(self.xposition,self.yposition))
    
    def drawInit(self):
        self.screen.blit(self.picture,(self.xposition,self.yposition))
        
class Pipe:
    def __init__(self,screen):
        self.screen=screen        
        rand = random()
        self.space = self.screen.get_height()/3.5*(random()*.3+.7)
        
        self.x = self.screen.get_width()
        self.y = 0  
        self.length1 = self.screen.get_height()*rand
        self.length2 = self.screen.get_height() - self.length1 - self.space
        self.width = self.screen.get_width()/8.0
        
    def update_position(self):
        self.x += -2.0
        
    def update(self):
        self.update_position()
        pygame.draw.rect(self.screen, (255,255,255),pygame.Rect(self.x,self.y,self.width,self.length1-self.space))     
        pygame.draw.rect(self.screen, (255,255,255),pygame.Rect(self.x ,(self.y+ self.length1+ self.space),self.width,self.length2))  

if __name__ =='__main__':
    game = FloppyBird()
    while 1:
        game.update()
