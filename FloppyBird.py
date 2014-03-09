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
import numpy as np

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
        self.soundPlayed=False
        self.startGame = False

        self.pipes = []    
        self.song=pygame.mixer.music.load('Pirates of the caribbean 8-bit.mp3')        
        pygame.mixer.music.play()
        
    def explosion(self):
        self.track = pygame.mixer.music.load('Explosion.wav')        
        pygame.mixer.music.play()
        self.soundPlayed=True
                            
    def display_score(self):
        message = 'Score: ' + str(self.score)
        fontobject=pygame.font.SysFont('Arial', 18)
        if len(message) != 0:
            self.screen.blit(fontobject.render(message, 1, (255, 255, 255)),((self.screen.get_width()*0.8), 0))
        
    def display_instructions(self):
        message = 'PRESS THE [SPACE] KEY TO START!'
        fontobject=pygame.font.SysFont('Arial', 18)
        self.screen.blit(fontobject.render(message, 1, (255, 255, 255)),(self.screen.get_width()*0.15,self.screen.get_height()*0.4))
        
        
    def display_loss(self):
        message = 'YOU LOST'  
        message2 = 'Your score: '+ str(self.score)
        fontobject=pygame.font.SysFont('Arial', 50)
        fontobject2=pygame.font.SysFont('Arial', 30)
        self.screen.blit(fontobject2.render(message2, 1, (255, 255, 255)),(self.screen.get_width()/3.0,self.screen.get_height()/1.8))
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
            
    def drange(start, stop, step):
        r = start
        while r < stop:
            yield r
            r += step
            
    def gameOn(self):            
        if self.bird.yposition>=self.screen.get_height()-self.bird.picture.get_height():
            return False
        for pipe in self.pipes:
            print pipe.length2
#            print self.bird.yposition
            if self.bird.xposition in range(int(pipe.x) , int(pipe.x+pipe.width)) and self.bird.yposition in range(0, int(pipe.length1- pipe.space)):
                return False
            if self.bird.xposition +self.bird.picture.get_width() in range(int(pipe.x) , int(pipe.x+pipe.width)) and self.bird.yposition in range(0, int(pipe.length1- pipe.space)):
                return False
            if self.bird.xposition in range(int(pipe.x) , int(pipe.x+pipe.width)) and self.bird.yposition +self.bird.picture.get_height() in range(0, int(pipe.length1- pipe.space)):
                return False
            if self.bird.xposition +self.bird.picture.get_width() in range(int(pipe.x) , int(pipe.x+pipe.width)) and self.bird.yposition +self.bird.picture.get_height() in range(0, int(pipe.length1- pipe.space)):
                return False
            
            if self.bird.xposition in range(int(pipe.x) , int(pipe.x+pipe.width)) and self.bird.yposition in range(int(pipe.length1+ pipe.space), int(pipe.length1+ pipe.space+ pipe.length2)):
                return False
            if self.bird.xposition +self.bird.picture.get_width() in range(int(pipe.x) , int(pipe.x+pipe.width)) and self.bird.yposition in range(int(pipe.length1+ pipe.space), int(pipe.length1+ pipe.space+pipe.length2)):
                return False
            if self.bird.xposition in range(int(pipe.x) , int(pipe.x+pipe.width)) and self.bird.yposition +self.bird.picture.get_height() in range(int(pipe.length1+ pipe.space), int(pipe.length1+ pipe.space+pipe.length2)):
                return False
            if self.bird.xposition +self.bird.picture.get_width() in range(int(pipe.x) , int(pipe.x+pipe.width)) and self.bird.yposition +self.bird.picture.get_height() in range(int(pipe.length1+ pipe.space), int(pipe.length1+ pipe.space+pipe.length2)):
                return False
                                                                

     
        return True
        
    
            
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
         
        if self.gameOn():
            self.display_score()
            
            for pipe in self.pipes:
                pipe.update()
                if self.bird.xposition == pipe.x:
                    self.update_display_score()
            if self.startGame:
                self.update_pipes()
                self.bird.update()
            else: 
                self.bird.drawInit()
                self.display_instructions()
        else:
            if not self.soundPlayed:
                self.explosion()
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
        self.thing=False

    def update_position(self):
        self.yposition +=self.yvelocity
        self.yvelocity += self.acceleration
        if self.yposition>self.screen.get_height()-self.picture.get_height()*0.5:                
            self.yposition=self.screen.get_height()-self.picture.get_height()*0.5
        elif self.yposition<0:                
            self.yposition=0
            
    def jump(self):
        self.yvelocity=-7.0
        
#    def rotate(self):
#        orig_rect = self.picture.get_rect()
#        orig_center = orig_rect.center
#        
#        rot_image = pygame.transform.rotate(self.picture,60)
#        
#        rot_rect = rot_image.get_rect()
#        rot_center = rot_rect.center
#        rot_center = orig_center
#        
#        self.picture=rot_image
        
    def update(self):
#        self.rotate()
        self.thing = True
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