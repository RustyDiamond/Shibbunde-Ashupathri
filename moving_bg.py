import pygame
import time
import random
import math

pygame.init()

def game():
    screen=pygame.display.set_mode((800,400))

    card=pygame.image.load("delorean.png")
    card=pygame.transform.scale(card, (125,32+8))
    bg=pygame.image.load("ground.png")
    wall=pygame.image.load("wall.png")
    xcord=0

    y=316
    x=100
    start_time=time.monotonic()
    end_time=0
    obs_time=random.randint(1,2)

    rightcol=False
    leftcol=False
    upcol=False
    downcol=False
    

    obstacles=[]

    up=True

    while True:
        screen.fill((255,255,255))

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                exit()
            
                
        screen.blit(bg,(xcord,400-64))
        
        xcord-=0.5
        if xcord<-800:
            xcord=0
        keys=pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and rightcol==False:
            x+=0.5
        elif keys[pygame.K_LEFT] and leftcol==False:
            x-=0.7


        if keys[pygame.K_RIGHT] and keys[pygame.K_SPACE]:
            x+=1

            
        if keys[pygame.K_UP]:
            y-=0.3
        elif keys[pygame.K_DOWN]:
            y+=0.3

            
        if not keys[pygame.K_RIGHT] and rightcol==False:
            x-=0.1
        if x<0:
            x=0       
        if y<0:
            y=0
        elif y>316:
            y=316

        
            

        check_time=time.monotonic()

        end_time=(check_time-start_time)
        
        
        if int(end_time)==obs_time:
            obs_y=random.randint(5,306)
            obs_x=800
            obstacles.append([wall,obs_x,obs_y])
            
            start_time=time.monotonic()
            obs_time=random.randint(1,2)

        if xcord in [-40,-220,-460,-700]:
            up=True
            
        if xcord in [-75,-300,-500,-794]:
            up=False

        if up==True:
            screen.blit(card,(x,y+1))
            player_rect=pygame.Rect(x,y+1,125,32+8)
        elif up==False:
            screen.blit(card,(x,y-1))
            player_rect=pygame.Rect(x,y+1,125,32+8)

            
        for obj in obstacles:
            if obj[0]==wall:
                
                obj[1]-=0.3
                screen.blit(wall,(obj[1],obj[2]))
                obj_rect=pygame.Rect(obj[1],obj[2],120,40)
                ycheck=y
                xcheck=x
                if player_rect.colliderect(obj_rect):
                    rightcol=True
                    if x+120>obj[1]:
                    
                        x-=0.3

                else:
                    rightcol=False
                
                
                
                
                
                        
                  
                    
                    
                


        



        
        
        pygame.display.update()

while True:
    game()
        

        
