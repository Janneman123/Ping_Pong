import pygame, sys
from pygame.locals import *
##from tkinter import messagebox

##Main Screen##
FPS=200

WINDOWWIDTH=400
WINDOWHEIGHT=300
INCREASESPEED=5



##Draw the Arena

BLACK=(0,0,0)
WHITE=(255,255,255)

LINETHICKNESS=10
PADDLESIZE=50
PADDLEOFFSET=20
BALLSIZE=10



def drawArena():
    DISPLAYSURF.fill((0,0,0))
    #Draw outline of arena
    pygame.draw.rect(DISPLAYSURF, WHITE, ((0,0),(WINDOWWIDTH,WINDOWHEIGHT)), LINETHICKNESS*2)
    #Draw centre line
    pygame.draw.line(DISPLAYSURF, WHITE, ((0,(WINDOWHEIGHT//2))),((WINDOWWIDTH,(WINDOWHEIGHT//2))), (LINETHICKNESS//4))

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

def checkPointScored(paddle1,ball,score):
    if ball.bottom==WINDOWHEIGHT-LINETHICKNESS:
        score+=1
    return score

def checkLives(paddle1,ball,lives):
    if ball.top==LINETHICKNESS:
        lives -=1
    return lives


def displayScore(score):
    resultSurf=BASICFONT.render('Score=%s' %(score),True,WHITE)
    resultRect=resultSurf.get_rect()
    resultRect.topleft=(WINDOWWIDTH -150,25)
    DISPLAYSURF.blit(resultSurf,resultRect)

def displayLives(lives):
    resultSurf=BASICFONT.render('Lives=%s' %(lives),True,WHITE)
    resultRect=resultSurf.get_rect()
    resultRect.topleft=(WINDOWWIDTH -150,50)
    DISPLAYSURF.blit(resultSurf,resultRect)

def AI(ball,ballDirY,paddle2):
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
    
def main():
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
    lives=3

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
    
    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type==MOUSEMOTION:
                mousex,mousey=event.pos
                paddle1.x=mousex

            elif lives < 0:
                pygame.quit()
                sys.exit()
        drawArena()
        drawPaddle(paddle1)
        drawPaddle(paddle2)
        drawBall(ball)
        score=checkPointScored(paddle1,ball,score)
        lives=checkLives(paddle1,ball,lives)

        ball=moveBall(ball,ballDirX,ballDirY)
        ballDirX,ballDirY=checkEdgeColission(ball,ballDirX,ballDirY)
        
        ballDirY=ballDirY*checkPaddleColission(ball,paddle1,paddle2,ballDirY)
        paddle2=AI(ball,ballDirY,paddle2)
        
        displayScore(score)
        displayLives(lives)

        if lives < 0:
            pygame.quit()
            sys.exit()

                

        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__=='__main__':
    main()
    
##messagebox.showinfo("Your Moves are Weak!"," Your Score is:%s" %score)
