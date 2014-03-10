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
        self.soundPlayed=False
        self.startGame = False
        self.bg = Background(self.screen)

        self.pipes = []    
        self.song=pygame.mixer.music.load('Pirates of the caribbean 8-bit.mp3')        
        pygame.mixer.music.play()
        self.gameOn=True
        
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
            self.pipes.append(Pipe(self.screen,self.bg.sky1Size[1]))
        if self.pipes[0].x<=-1*self.pipes[0].pipeSize[0]:
            self.pipes.pop(0)
        if self.pipes[-1].x==self.screen.get_width()-250:
            self.pipes.append(Pipe(self.screen,self.bg.sky1Size[1]))
            
    def isGameOn(self):            
        if self.bird.yposition>=self.screen.get_height()-self.bird.picture.get_height()-self.bg.groundSize[1]:
            self.gameOn=False
        for pipe in self.pipes:
            bird_x = int(self.bird.xposition)
            bird_y = int(self.bird.yposition)
            bird_width = int(self.bird.picture.get_width())
            bird_height = int(self.bird.picture.get_height())
#            print int(pipe.topPipeHeight + pipe.pipeTopSize[1])
#            print int(pipe.x) , int(pipe.x+pipe.pipeSize[0])
#            pygame.draw.circle(self.screen,(255,0,0),(int(bird_x),int(bird_y)),2)
#            pygame.draw.circle(self.screen,(255,0,0),(int(bird_x+bird_width),int(bird_y)),2)
#            pygame.draw.circle(self.screen,(255,0,0),(int(bird_x),int(bird_y+bird_height)),2)
#            pygame.draw.circle(self.screen,(255,0,0),(int(bird_x+bird_width),int(bird_y+bird_height)),2)
#            pygame.draw.circle(self.screen,(255,0,0),(int(pipe.x),int(pipe.topPipeHeight+pipe.pipeTopSize[1])),2)
#            pygame.draw.circle(self.screen,(255,0,0),(int(pipe.x+pipe.pipeSize[0]),int(pipe.topPipeHeight+ pipe.width)),2)

                        
            if bird_x in range(int(pipe.x) , int(pipe.x+pipe.pipeSize[0])) and bird_y in range(0, int(pipe.topPipeHeight + pipe.pipeTopSize[1])):
               self.gameOn=False
            if bird_x +bird_width in range(int(pipe.x) , int(pipe.x+pipe.pipeSize[0])) and bird_y in range(0, int(pipe.topPipeHeight+pipe.pipeTopSize[1])):
                self.gameOn=False
            if bird_x +bird_width in range(int(pipe.x) , int(pipe.x+pipe.pipeSize[0])) and bird_y +bird_height in range(0, int(pipe.topPipeHeight+pipe.pipeTopSize[1])):
                self.gameOn=False
            
            if bird_x in range(int(pipe.x) , int(pipe.x+pipe.pipeSize[0])) and bird_y +bird_height in range(int(pipe.topPipeHeight+ pipe.width), int(pipe.topPipeHeight+pipe.pipeTopSize[1]+ pipe.width+pipe.bottomPipeHeight+pipe.pipeTopSize[1])):
                self.gameOn=False
            if bird_x +bird_width in range(int(pipe.x) , int(pipe.x+pipe.pipeSize[0])) and bird_y +bird_height in range(int(pipe.topPipeHeight+ pipe.width), int(pipe.topPipeHeight+pipe.pipeTopSize[1]+ pipe.width+pipe.bottomPipeHeight+pipe.pipeTopSize[1])):
                self.gameOn=False                                                                            
            
    def update(self):
        self.clock.tick(60)
        
        self.screen.fill(0)
        for event in pygame.event.get():
            if event.type==QUIT:
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit()
                if event.key == K_SPACE:
                    self.startGame=True
                    self.bird.jump()
         
        
                        
        if self.startGame:
            if self.gameOn:
                self.isGameOn()
                self.bg.update()
                self.update_pipes()
                for pipe in self.pipes:
                    pipe.update()
                    if self.bird.xposition == pipe.x:
                        self.update_display_score()
                self.bird.update()
                self.display_score()
            else:
                if not self.soundPlayed:
                    self.explosion()
                    self.display_loss()
        else: 
            self.bird.drawInit()
            self.display_instructions()
        
                    
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
        self.yvelocity=-1*self.screen.get_height()*.012
        
    def update(self):
        self.thing = True
        self.update_position()
        self.screen.blit(self.picture,(self.xposition,self.yposition))
    
    def drawInit(self):
        self.screen.blit(self.picture,(self.xposition,self.yposition))
        
class Pipe:
    def __init__(self,screen,yPos):
        self.screen=screen    
        
        self.x = self.screen.get_width()
        
        self.pipe = pygame.image.load(os.path.join('','pipe.png'))
        self.pipeTop = pygame.image.load(os.path.join('','pipetop.png'))
        
        self.pipeSize = self.pipe.get_size()
        self.pipeTopSize = self.pipeTop.get_size()
        factor = self.screen.get_width()/20.0/self.pipeTopSize[1]
        self.pipe=pygame.transform.scale(self.pipe,(int(factor*self.pipeSize[0]),int(self.pipeSize[1])))
        self.pipeTop=pygame.transform.scale(self.pipeTop,(int(factor*self.pipeTopSize[0]),int(factor*self.pipeTopSize[1])))
        self.pipeSize = self.pipe.get_size()
        self.pipeTopSize = self.pipeTop.get_size()
        minHeight = self.screen.get_height()/150.0
        minY = yPos-2*self.pipeTopSize[1]+2*minHeight
        maxY = 0
        minWidth = (minY-maxY)/2.5
        maxWidth = (minY-maxY)/2
        self.width = int(random()*(maxWidth-minWidth)+minWidth)
        totHeight = yPos
        self.topPipeHeight = int(random()*(minY-maxY-self.width)+minHeight)
        self.bottomPipeHeight = totHeight-self.topPipeHeight-2*self.pipeTopSize[1]-self.width
        self.bottom=yPos
        self.top=0
        
    def update_position(self):
        self.x += -2.0 
        
    def update(self): 
        self.update_position()
        #print self.topPipeHeight, self.x
        for i in range(self.topPipeHeight):
            self.screen.blit(self.pipe,(int(self.x),int(self.top+i)))
        self.screen.blit(pygame.transform.flip(self.pipeTop,False,True),(int(self.x),int(self.topPipeHeight)))
        self.screen.blit(self.pipeTop,(int(self.x),int(self.topPipeHeight+self.width)))
        for i in range(self.topPipeHeight+self.width+self.pipeTopSize[1],self.bottom):
            self.screen.blit(self.pipe,(int(self.x),int(self.top+i)))
#        pygame.draw.line(self.screen, (0,0,0) ,(self.x, 0), (self.x, self.topPipeHeight+self.pipeTopSize[1]))
#        pygame.draw.line(self.screen, (0,0,0) ,(self.x+self.pipeSize[0], self.topPipeHeight+self.pipeTopSize[1] +10), (self.x, self.topPipeHeight+self.pipeTopSize[1]+10))       
        
class Background:
    
    def __init__(self,screen):
        
        self.screen=screen
        
        self.ground = pygame.image.load(os.path.join('','ground.png'))
        self.sky1 = pygame.image.load(os.path.join('','sky1.png'))
        self.sky2 = pygame.image.load(os.path.join('','sky2.png'))
        
        self.groundSize = self.ground.get_size()
        self.sky1Size = self.sky1.get_size()
        self.sky2Size = self.sky2.get_size()
        
        totalSize = self.sky1Size[1]+self.groundSize[1]
        factor = self.screen.get_height()*1.0/totalSize
        
        self.sky1=pygame.transform.scale(self.sky1,(int(self.sky1Size[0]*factor),int(self.sky1Size[1]*factor)))
        self.sky2=pygame.transform.scale(self.sky2,(int(self.sky2Size[0]*factor),int(self.sky1Size[1]*factor)))
        self.ground=pygame.transform.scale(self.ground,(int(self.groundSize[0]*factor),self.screen.get_height()-int(self.sky2Size[1]*factor)))
        
        self.groundSize = self.ground.get_size()
        self.sky1Size = self.sky1.get_size()
        self.sky2Size = self.sky2.get_size()
        
        self.groundXPos = 0
        self.groundYPos = self.screen.get_height()-self.groundSize[1]
        self.sky1XPos = 0
        self.sky1YPos = 0
        self.sky2XPos = self.sky1XPos + self.sky1Size[0]
        self.sky2YPos = 0
    
    def updateGround(self):
        self.groundXPos-=2
        if self.groundXPos+self.groundSize[0]<=0:
            self.groundXPos=0
    
    def updateSky(self):
        self.sky1XPos-=0.5
        self.sky2XPos-=0.5
        if self.sky1XPos+self.sky1Size[0]<=0:
            self.sky1XPos=self.sky2XPos+self.sky2Size[0]
        if self.sky2XPos+self.sky2Size[0]<=0:
            self.sky2XPos=self.sky1XPos+self.sky1Size[0]    
        
    def update(self):
        self.updateGround()
        self.updateSky()
        
        for i in range(self.screen.get_width()/self.groundSize[0]+2):
            self.screen.blit(self.ground,(self.groundXPos+i*self.groundSize[0],self.groundYPos))
        
        self.screen.blit(self.sky1,(int(self.sky1XPos),int(self.sky1YPos)))
        self.screen.blit(self.sky2,(int(self.sky2XPos),int(self.sky2YPos)))

if __name__ =='__main__':
    game = FloppyBird()
    while 1:
        game.update()