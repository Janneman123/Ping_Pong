import pygame, sys
from pygame.locals import *
from random import randint
import pandas as pd

FPS=200

WINDOWWIDTH=400
WINDOWHEIGHT=300
INCREASESPEED=5
MAXSCORE=10

BLACK=(0,0,0)
WHITE=(255,255,255)

LINETHICKNESS=10
PADDLESIZE=50
PADDLEOFFSET=20
BALLSIZE=10



def drawArena():
    DISPLAYSURF.fill((0,0,0))
  
    pygame.draw.rect(DISPLAYSURF, WHITE, ((0,0),(WINDOWWIDTH,WINDOWHEIGHT)), LINETHICKNESS*2)

def drawPaddle(paddle):
    if paddle.left <LINETHICKNESS:
        paddle.left=LINETHICKNESS
    elif paddle.right >WINDOWWIDTH-LINETHICKNESS:
        paddle.right=WINDOWWIDTH-LINETHICKNESS
    pygame.draw.rect(DISPLAYSURF, WHITE, paddle)

def drawBall(ball):
    pygame.draw.rect(DISPLAYSURF,WHITE,ball)

def moveBall(ball,ballDirX,ballDirY):
    ball.x +=(ballDirX*INCREASESPEED)
    ball.y +=(ballDirY*INCREASESPEED)
    return ball

def movePaddle(paddle,paddleDirX):
    paddle.x +=paddleDirX
  
    return paddle

def checkEdgeColission(ball,ballDirX,ballDirY):
    if ball.left==(LINETHICKNESS) or ball.right==(WINDOWWIDTH-LINETHICKNESS):
        ballDirX=(ballDirX*-1)
    if ball.top==(LINETHICKNESS) or ball.bottom==(WINDOWHEIGHT-LINETHICKNESS):
        ballDirY=(ballDirY*-1)

    return ballDirX,ballDirY

def checkPaddleColission(ball,paddle1,paddle2,ballDirY):
    if ballDirY==-1 and paddle1.bottom==ball.top and paddle1.right>ball.left and paddle1.left<ball.right:
        return -1
    elif ballDirY==1 and paddle2.top==ball.bottom and paddle2.right>ball.left and paddle2.left<ball.right:
        return -1
    else:
        return 1

def checkPlayer1PointScored(ball,Player1Score):
    if ball.bottom==WINDOWHEIGHT-LINETHICKNESS:
        Player1Score+=1
    return Player1Score

def checkPlayer2PointScored(ball,Player2Score):
    if ball.top==LINETHICKNESS:
        Player2Score+=1
    return Player2Score

def displayPlayer1Score(Player1Score):
    resultSurf1=BASICFONT.render('Player1Score=%s' %(Player1Score),True,WHITE)
    resultRect1=resultSurf1.get_rect()
    resultRect1.topleft=(WINDOWWIDTH -150,25)
    DISPLAYSURF.blit(resultSurf1,resultRect1)

    return Player1Score

def displayPlayer2Score(Player2Score):
    resultSurf2=BASICFONT.render('Player2Score=%s' %(Player2Score),True,WHITE)
    resultRect2=resultSurf2.get_rect()
    resultRect2.topleft=(WINDOWWIDTH -150,WINDOWHEIGHT-25)
    DISPLAYSURF.blit(resultSurf2,resultRect2)

    return Player2Score

def AIPlayer1(ball,ballDirY,paddle1,paddle2):

    if ballDirY==1:
        if paddle1.centerx > (WINDOWWIDTH//2):
            paddle1.x-=INCREASESPEED
        elif paddle1.centerx < (WINDOWWIDTH//2):
            paddle1.x+=INCREASESPEED
    elif ballDirY==-1:
        if paddle1.centerx < ball.centerx:
            paddle1.x+=INCREASESPEED
        elif paddle1.centerx > ball.centerx:
            paddle1.x-=INCREASESPEED
    return paddle1

def AIPlayer2(ball,ballDirY,paddle1,paddle2):
    if ballDirY==-1:
        if paddle2.centerx > (WINDOWWIDTH//2):
            paddle2.x-=INCREASESPEED
        elif paddle2.centerx < (WINDOWWIDTH//2):
            paddle2.x+=INCREASESPEED
    elif ballDirY==1:
        if paddle2.centerx < ball.centerx:
            paddle2.x+=INCREASESPEED
        elif paddle2.centerx > ball.centerx:
            paddle2.x-=INCREASESPEED
    return paddle2

def main(AI):
    pygame.init()
    global DISPLAYSURF

    global BASICFONT, BASICFONTSIZE
    BASICFONTSIZE=10
    BASICFONT=pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

    FPSCLOCK=pygame.time.Clock()
    DISPLAYSURF=pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    pygame.display.set_caption('Ping Pong by J.F Olivier')

    

    player1Position=(WINDOWWIDTH-PADDLESIZE)//2
    player2Position=(WINDOWWIDTH-PADDLESIZE)//2
    ballX=(WINDOWWIDTH//2)
    ballY=(WINDOWHEIGHT//2)-(LINETHICKNESS//2)
    score=0
    Player1Score=0
    Player2Score=0
##    lives=3

    paddle1 = pygame.Rect(player1Position,PADDLEOFFSET, PADDLESIZE,LINETHICKNESS)
    paddle2 = pygame.Rect(player2Position,WINDOWHEIGHT-PADDLEOFFSET-LINETHICKNESS, PADDLESIZE,LINETHICKNESS)
    ball=pygame.Rect(ballX,ballY,BALLSIZE,BALLSIZE)

    ballDirX=-1
    ballDirY=-1
    paddle1DirX=0
    paddle2DirX=0

    
    ball=moveBall(ball,ballDirX,ballDirY)
    paddle1=movePaddle(paddle1,paddle1DirX)
    paddle2=movePaddle(paddle2,paddle2DirX)

    pygame.mouse.set_visible(1)

    data=pd.DataFrame([])
    
    while True:

                
        row =pd.DataFrame({'Paddle1X': paddle1.x,\
                            'Paddle2X':paddle2.x,\
                            'BallX':ball.x,\
                            'Paddle1YDistanceFromBall':-paddle1.y+ball.y,\
                            'Paddle2YDistanceFromBall':-ball.y+paddle2.y,\
                           'Paddle1XDistanceFromBall':ball.x-paddle1.x,\
                           'Paddle2XDistanceFromBall':ball.x-paddle2.x,\
                            'Player1Score':Player1Score,\
                          'Player2Score':Player2Score},\
                            index=[0])
        data=data.append(row,ignore_index=True)

        

        for event in pygame.event.get():
            if event.type==QUIT:
                print(data)
                pygame.quit()
                sys.exit()
                

        drawArena()
        drawPaddle(paddle1)
        drawPaddle(paddle2)
        drawBall(ball)
        Player1Score=checkPlayer1PointScored(ball,Player1Score)
        Player2Score=checkPlayer2PointScored(ball,Player2Score)
        ball=moveBall(ball,ballDirX,ballDirY)
        ballDirX,ballDirY=checkEdgeColission(ball,ballDirX,ballDirY)
        ballDirY=ballDirY*checkPaddleColission(ball,paddle1,paddle2,ballDirY)

        if AI==1:
            paddle1=AIPlayer1(ball,ballDirY,paddle1,paddle2)
        elif AI==0 and event.type==MOUSEMOTION:
            mousex,mousey=event.pos
            paddle1.x=mousex
            
        paddle2=AIPlayer2(ball,ballDirY,paddle1,paddle2)
        
        displayPlayer1Score(Player1Score)
        displayPlayer2Score(Player2Score)
        

    
        
        
        
##        data=pd.DataFrame(data)
        
##        displayLives(lives)

##        if lives < 0:
##            pygame.quit()
##            sys.exit()
        if Player1Score==MAXSCORE or Player2Score==MAXSCORE:
               pygame.quit()
               sys.exit()

                

        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__=='__main__':
    main(1)
print(data)
    
##messagebox.showinfo("Your Moves are Weak!"," Your Score is:%s" %score)
