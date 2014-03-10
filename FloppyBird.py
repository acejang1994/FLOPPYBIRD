# -*- coding: utf-8 -*-
"""
Created on Sat Mar  8 18:09:47 2014

@authors: 
Sidd Singal
James Jang
Filippos Lymperopoulos

Software Design
Homework 6: Video Game
Floppy Paul

For our Software Design Homework 6 Assignment, we made a knockoff of
Flappy Bird, except we replaced the bird in the game with Paul's face.
The point of the game is to go through the pipes and score as many points
as possible. Press space to jump!

This game is officially finished for turning in, but there are a couple of
extra TODO's to make this game even better
TODO:
    menu system
    leaderboards
    networking
    sound toggle
    update graphics for text
"""

# Import needed modules
import pygame
from pygame.locals import *
import os
from os import chdir
from random import *
from os.path import dirname

class FloppyPaul:
    
    """ 
    This class handles all of the game modules and the actual game playing
    """
    
    def __init__(self):
        
        """ 
        Constructor to initialize the FloppyPaul class. This includes initializing
        all classes and variables and methods associated with this class.
        """
        
        # Initialize pygame
        pygame.init()
        
        # Set the width and height of the window relative to the screen resolution
        infoObject = pygame.display.Info()
        screenWidth,screenHeight = infoObject.current_w, infoObject.current_h
        height=int(screenHeight/2)
        width=int(height)
        self.screen = pygame.display.set_mode((width,height))
        
        # Set the title of the window
        pygame.display.set_caption('Floppy Paul')
        
        # Initialize pygame's clock
        self.clock=pygame.time.Clock()
        
        # Initialize Bird class, Background class, and Pipe array
        self.bird=Bird(self.screen) 
        self.bg = Background(self.screen)
        self.pipes = []
        
        # Initialize score variable
        self.score =0

        # Initialze game state variables
        self.soundPlayed=False
        self.startGame = False
        self.gameOn=True
        
        # Start playing the song
        self.song=pygame.mixer.music.load('Pirates of the caribbean 8-bit.mp3')        
        pygame.mixer.music.play()

        
    def explosion(self):
        
        """
        Play the explosion sound when the bird dies
        """
        
        # Load and play the explosion sound
        self.track = pygame.mixer.music.load('Explosion.wav')        
        pygame.mixer.music.play()
        
        # Indicate that the sound has been played so it doesn't play again
        self.soundPlayed=True
                            
    def display_score(self):
        
        """
        Display the score on the corner of the screen
        """
        
        # Set the message to be written and its font
        message = 'Score: ' + str(self.score)
        fontobject=pygame.font.SysFont('Courier', int(self.screen.get_height()*.055))
        
        # Write the message to the corner of the screen
        self.screen.blit(fontobject.render(message, 1, (0, 0, 0)),((self.screen.get_width()*0.65), 0))
        
    def display_instructions(self):
        
        """
        Display the instructions in the beginning of the game
        """
        
        # Set the message to be written and its font
        message = 'PRESS THE [SPACE] KEY TO START!'
        fontobject=pygame.font.SysFont('Courier', 20)
        
        # Write the message to the middle of the screen
        self.screen.blit(fontobject.render(message, 1, (0, 0,0)),(self.screen.get_width()*0.15,self.screen.get_height()*0.4))
        
        
    def display_loss(self):
        
        """
        If you lose, display a message indicating that user has lost and
        display the score
        """
        
        # Instantiate messages to post on screen
        message = 'YOU LOST'  
        message2 = 'Your score: '+ str(self.score)
        
        # Set font for messages
        fontobject=pygame.font.SysFont('Courier', int(self.screen.get_height()/9.0))
        fontobject2=pygame.font.SysFont('Courier', int(self.screen.get_height()/15.0))
        
        # Add message to screen
        self.screen.blit(fontobject2.render(message2, 1, (255, 255, 255)),(self.screen.get_width()/3.0,self.screen.get_height()/1.8))
        self.screen.blit(fontobject.render(message, 1, (255, 255, 255)),(self.screen.get_width()/4.0,self.screen.get_height()/2.5))
            
    def update_display_score(self):
        
        """
        Updates the score variable when bird passes through a pipe
        """
        
        # Increment score by 1
        self.score += 1
            
    def update_pipes(self):
        
        """
        Updates the pipes array to add more pipes in the end if more are needed 
        or delete pipes in the beginning if they are off the screen
        """
        
        # If there are no pipes currently, add a pipe
        if len(self.pipes)==0:
            self.pipes.append(Pipe(self.screen,self.bg.sky1Size[1]))
            
        # If the first pipe is off the screen, remove it from the array
        if self.pipes[0].x<=-1*self.pipes[0].pipeSize[0]:
            self.pipes.pop(0)
            
        # If the last pipe has gone down far enough, then add another pipe
        if self.pipes[-1].x<=self.screen.get_width()*0.5:
            self.pipes.append(Pipe(self.screen,self.bg.sky1Size[1]))
            
    def isGameOn(self):            
        
        """
        Changes the gameOn game state variable if the bird dies
        """
        
        # If the bird has hit the ground, end the game
        if self.bird.yposition>=self.screen.get_height()-self.bird.picture.get_height()-self.bg.groundSize[1]:
            self.gameOn=False
            
        # Check the bird's position relative to each pipe
        for pipe in self.pipes:
            
            # Read and cast bird position and size variables
            bird_x = int(self.bird.xposition)
            bird_y = int(self.bird.yposition)
            bird_width = int(self.bird.picture.get_width())
            bird_height = int(self.bird.picture.get_height())
            
            # For the left corners of the bird...
            if bird_x in range(int(pipe.x) , int(pipe.x+pipe.pipeSize[0])):
                
                # If the top-left corner of the bird is touching the top pipe, end the game
                if bird_y in range(0, int(pipe.topPipeHeight + pipe.pipeTopSize[1])):
                    self.gameOn=False
                
                # If the bottom-left corner of the bird is touching the top pipe, end the game
                elif bird_y +bird_height in range(int(pipe.topPipeHeight+ pipe.width), int(pipe.topPipeHeight+pipe.pipeTopSize[1]+ pipe.width+pipe.bottomPipeHeight+pipe.pipeTopSize[1])):
                    self.gameOn=False
            
            # For the right corners of the bird...
            if bird_x +bird_width in range(int(pipe.x) , int(pipe.x+pipe.pipeSize[0])):
                
                # If the top-right corner of the bird is touching the top pipe, end the game
                if bird_y in range(0, int(pipe.topPipeHeight+pipe.pipeTopSize[1])):
                    self.gameOn=False
                
                # If the bottom-right corner of the bird is touching the top pipe, end the game
                elif bird_y +bird_height in range(int(pipe.topPipeHeight+ pipe.width), int(pipe.topPipeHeight+pipe.pipeTopSize[1]+ pipe.width+pipe.bottomPipeHeight+pipe.pipeTopSize[1])):
                    self.gameOn=False  
            
    def update(self):
        
        """
        Update any variables that need to be changed and draw everything on the screen
        """
        
        # Set the FPS of the game
        self.clock.tick(60)
        
        # Clear the screen
        self.screen.fill(0)
        
        # For any user inputs given
        for event in pygame.event.get():
            
            # Quit the game if the exit buttom is pressed
            if event.type==QUIT:
                exit()
            
            # If a keyboard button is presseed
            if event.type == KEYDOWN:
                
                # Quit the game if the escape button is pressed
                if event.key == K_ESCAPE:
                    exit()
                    
                # Make the bird jump and start the game if not already started
                # if the space button is pressed
                if event.key == K_SPACE:
                    self.startGame=True
                    self.bird.jump()
         
        # If the game has started then...
        if self.startGame:
            
            # If the user is still alive then...
            if self.gameOn:
                
                # Test to see if the user is still alive
                self.isGameOn()
                
                # Update the background and its graphics and the pipes array
                self.bg.update()
                self.update_pipes()
                for pipe in self.pipes:
                    pipe.update()
                    
                    # Increment the score if the bird passes through the pipe
                    ## THIS NEEDS TO FIXED!!!!!
                    if self.bird.xposition == pipe.x:
                        self.update_display_score()
                        
                # Update the bird and its graphics and display the score
                self.bird.update()
                self.display_score()
            
            # If the user is dead then...
            else:
                
                # Play the explosion if it hasn't been played already
                if not self.soundPlayed:
                    self.explosion()
                    
                # Indicate the user that he has lost
                self.display_loss()
            
        # If the game hasn't started, then add static pictures of the bird,
        # background, and instructions
        else: 
            self.bg.update_static()
            self.bird.drawInit()
            self.display_instructions()

        # Pygame function to update graphics
        pygame.display.flip()
        
class Bird:
    
    """
    This class represents the bird (or Paul's head) and its characteristics
    """
    
    def __init__(self,screen):
        
        """
        Initialize the Bird class
        """
        
        # Make the screen of FloppyPaul accessible to Bird
        self.screen=screen
        
        # Load a picture of Paul as the main character of the game and scale
        # the picture to an appropriate size
        temppic=pygame.image.load(os.path.join('','paul.png'))
        factor=(self.screen.get_height()/11.0)/temppic.get_height()
        self.picture=pygame.transform.scale(temppic,(int(temppic.get_width()*factor),int(temppic.get_height()*factor)))
        
        # Set the initial (and possibly constant) position, y-velocity, and
        # acceleration
        self.xposition=self.screen.get_width()/5.0
        self.yposition=self.screen.get_height()/2.0
        self.yvelocity=0.0
        self.acceleration=self.screen.get_height()/1800.0
        

    def update_position(self):
        
        """
        Update the position of the bird
        """
        
        # Update the position and velocity based on previous velocity and
        # acceleration, respectively
        self.yposition +=self.yvelocity
        self.yvelocity += self.acceleration
        
        # If the bird is too low, then keep him on the bottom of the screen
        if self.yposition>self.screen.get_height()-self.picture.get_height():                
            self.yposition=self.screen.get_height()-self.picture.get_height()
            
        # If the bird is too high, then keep him on the top of the screen
        elif self.yposition<0:                
            self.yposition=0
            
    def jump(self):
        
        """
        Make the bird jump by changing it's velocity
        """
        
        # Set the velocity of the bird based on the screen size
        self.yvelocity=-1*self.screen.get_height()*.011
        
    def update(self):
        
        """
        Update the bird's position and graphics
        """
        
        # Update the position of the bird
        self.update_position()
        
        # Add the bird graphic to the screen
        self.screen.blit(self.picture,(self.xposition,self.yposition))
    
    def drawInit(self):
        
        """
        Static image of the bird to add in the beginning of the game
        """
        
        # Add the bird to the screen
        self.screen.blit(self.picture,(self.xposition,self.yposition))
        
class Pipe:
    
    """
    Class to represent each pair of pipes (lower and upper pipe) scrolling
    in the game
    """
    
    def __init__(self,screen,yPos):
        
        """
        Initialize the pipe array
        """
        
        # Make the screen of FloppyPaul accessible to Pipe
        self.screen=screen    
        
        # Make the pipe start at the end of the screen
        self.x = self.screen.get_width()
        
        # Load the images of the pipes 
        self.pipe = pygame.image.load(os.path.join('','pipe.png'))
        self.pipeTop = pygame.image.load(os.path.join('','pipetop.png'))
        
        # Resize the pipes to appropriately fit onto the screen and make
        # size variables
        self.pipeSize = self.pipe.get_size()
        self.pipeTopSize = self.pipeTop.get_size()
        factor = self.screen.get_width()/20.0/self.pipeTopSize[1]
        self.pipe=pygame.transform.scale(self.pipe,(int(factor*self.pipeSize[0]),int(self.pipeSize[1])))
        self.pipeTop=pygame.transform.scale(self.pipeTop,(int(factor*self.pipeTopSize[0]),int(factor*self.pipeTopSize[1])))
        self.pipeSize = self.pipe.get_size()
        self.pipeTopSize = self.pipeTop.get_size()
        
        # Calculate where each of the pair of pipes should start and end on
        # the screen
        minHeight = self.screen.get_height()/150.0 # Minimum length of the pipe
        minY = yPos-2*self.pipeTopSize[1]+2*minHeight
        maxY = 0
        minWidth = (minY-maxY)/2.5 
        maxWidth = (minY-maxY)/2
        self.width = int(random()*(maxWidth-minWidth)+minWidth) # Width between the pipes
        totHeight = yPos
        self.topPipeHeight = int(random()*(minY-maxY-self.width)+minHeight) # Length of top pipe
        self.bottomPipeHeight = totHeight-self.topPipeHeight-2*self.pipeTopSize[1]-self.width # Length of bottom pipe
        self.bottom=yPos
        self.top=0
        
    def update_position(self):
        
        """
        Change the x position of the pipe
        """
        
        # Update the x position of the pipe
        self.x -= self.screen.get_width()/225.0
        
    def update(self):
        
        """
        Update the properties of the pipe and update the graphics
        """
        
        # Update the position of the pipe
        self.update_position()
        
        # Add the shaft of the top pipe to the screen
        for i in range(self.topPipeHeight):
            self.screen.blit(self.pipe,(int(self.x),int(self.top+i)))
            
        # Add the pipe tops to the screen
        self.screen.blit(pygame.transform.flip(self.pipeTop,False,True),(int(self.x),int(self.topPipeHeight)))
        self.screen.blit(self.pipeTop,(int(self.x),int(self.topPipeHeight+self.width)))
        
        # Add the shaft of the bottom pipe to the screen
        for i in range(self.topPipeHeight+self.width+self.pipeTopSize[1],self.bottom):
            self.screen.blit(self.pipe,(int(self.x),int(self.top+i)))      
        
class Background:
    
    """
    This class represents the background of the game (the sky and ground)
    """
    
    def __init__(self,screen):
        
        """
        Initialize the Background class
        """
        
        # Make the screen of FloppyPaul accessible to Background
        self.screen=screen
        
        # Load the images for Background
        self.ground = pygame.image.load(os.path.join('','ground.png'))
        self.sky1 = pygame.image.load(os.path.join('','sky1.png'))
        self.sky2 = pygame.image.load(os.path.join('','sky2.png'))
        
        # Resize the background images to fit on the screen appropriately        
        self.groundSize = self.ground.get_size()
        self.sky1Size = self.sky1.get_size()
        self.sky2Size = self.sky2.get_size()        
        totalSize = self.sky1Size[1]+self.groundSize[1]
        factor = self.screen.get_height()*1.0/totalSize        
        self.sky1=pygame.transform.scale(self.sky1,(int(self.sky1Size[0]*factor),int(self.sky1Size[1]*factor)))
        self.sky2=pygame.transform.scale(self.sky2,(int(self.sky2Size[0]*factor),int(self.sky1Size[1]*factor)))
        self.ground=pygame.transform.scale(self.ground,(int(self.groundSize[0]*factor),self.screen.get_height()-int(self.sky2Size[1]*factor)))
        
        # Make accessible variables for the sizes of the background images
        self.groundSize = self.ground.get_size()
        self.sky1Size = self.sky1.get_size()
        self.sky2Size = self.sky2.get_size()
        
        # Set the initial (and possibly constant) positions of the background images
        self.groundXPos = 0
        self.groundYPos = self.screen.get_height()-self.groundSize[1]
        self.sky1XPos = 0
        self.sky1YPos = 0
        self.sky2XPos = self.sky1XPos + self.sky1Size[0]
        self.sky2YPos = 0
    
    def update_static(self):
        
        """
        Static background to add at the beginning of the game
        """
        
        # Add sky and ground images to screen
        self.screen.blit(self.sky1,(int(self.sky1XPos),int(self.sky1YPos)))
        self.screen.blit(self.sky2,(int(self.sky2XPos),int(self.sky2YPos)))
        for i in range(self.screen.get_width()/self.groundSize[0]+2):
            self.screen.blit(self.ground,(self.groundXPos+i*self.groundSize[0],self.groundYPos))
         
    def updateGround(self):
        
        """
        Move the ground along with the pipes
        """
        
        # Change the starting x position of the first ground image
        self.groundXPos-=self.screen.get_width()/225.0
        
        # If the first ground image goes off the screen, reset it to the
        # beginning of the screen
        if self.groundXPos+self.groundSize[0]<=0:
            self.groundXPos=0
    
    def updateSky(self):
        
        """
        Move the ground at a slower pace than the ground
        """
        
        # Change the position of the sky images
        self.sky1XPos-=self.screen.get_width()/900.0
        self.sky2XPos-=self.screen.get_width()/900.0
        
        # If the first sky image goes off the screen, put it after the
        # second sky image
        if self.sky1XPos+self.sky1Size[0]<=0:
            self.sky1XPos=self.sky2XPos+self.sky2Size[0]
        
        # If the second sky image goes off the screen, put it after the
        # first sky image
        if self.sky2XPos+self.sky2Size[0]<=0:
            self.sky2XPos=self.sky1XPos+self.sky1Size[0]    
        
    def update(self):
        
        """
        Update the background images graphics
        """
        
        # Move the ground and sky images
        self.updateGround()
        self.updateSky()
        
        # Add the ground graphics to the screen
        for i in range(self.screen.get_width()/self.groundSize[0]+2):
            self.screen.blit(self.ground,(self.groundXPos+i*self.groundSize[0],self.groundYPos))
        
        # Add the sky images to the screen
        self.screen.blit(self.sky1,(int(self.sky1XPos),int(self.sky1YPos)))
        self.screen.blit(self.sky2,(int(self.sky2XPos),int(self.sky2YPos)))
        
        
# Main function to run all the code
if __name__ =='__main__':
    
    # Initialize the Floppy Paul game
    game = FloppyPaul()
    
    # Keep updating the game variable    
    while 1:
        game.update()