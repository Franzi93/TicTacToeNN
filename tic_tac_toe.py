import pygame, sys, random, copy
from pygame.locals import *
#from TicTacToeBot import TicTacToeBot

##CONSTANTS, yo##

WINDOWWIDTH = 640
WINDOWHEIGHT = 480
FPS = 30
BOXSIZE = 100
GAPSIZE = 10
BOARDWIDTH = 3
BOARDHEIGHT = 3
XMARK = 'X'
OMARK = 'O'
XMARGIN = int((WINDOWWIDTH -(BOARDWIDTH * (BOXSIZE + GAPSIZE)))/2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE)))/2)

#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)
BLACK    = (  0,   0,   0)
COMBLUE  = (233, 232, 255)

BGCOLOR = BLACK
BOXCOLOR = BGCOLOR
LINECOLOR = COMBLUE

def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    mainFont = pygame.font.SysFont('Arial', 90)
    smallFont = pygame.font.SysFont('Arial', 25)

    pygame.display.set_caption('Tic-Tac-Toe')

  #  bot1 = TicTacToeBot()
   # bot1.train(100)
    
    #bot1.evaluate_action(...)

    playerScore = 0
    computerScore = 0
    tieScore = 0
    playerWins = False
    computerWins = False
    mousex = None
    mainBoard = makeEachBoxFalse(False)
    usedBoxes = makeEachBoxFalse(False)

    player = XMARK

    DISPLAYSURF.fill(BGCOLOR)
    drawLines()
    

    while True:
        
        print(mainBoard)
        

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
        
         #   elif event.type == MOUSEMOTION:
       #         mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
        if mousex != None:
            boxx, boxy = getBoxAtPixel(mousex, mousey)
    
            player = makeMove(player,usedBoxes,mainBoard,mainFont,boxx,boxy)
        
        playerWins, computerWins = gameWon(mainBoard)

        if playerWins:
            pygame.time.wait(500)
            highlightWin(mainBoard)
           
            pygame.display.update()
            playerScore += 1
            player, usedBoxes, mainBoard,  playerWins, computerWins = boardReset(player, usedBoxes, mainBoard,  playerWins, computerWins)
            DISPLAYSURF.fill(BGCOLOR)
            drawLines()
            
        elif computerWins:
            pygame.time.wait(500)
            highlightWin(mainBoard)
            
            pygame.display.update()
            computerScore += 1
            player, usedBoxes, mainBoard,  playerWins, computerWins = boardReset(player, usedBoxes, mainBoard,  playerWins, computerWins)
            DISPLAYSURF.fill(BGCOLOR)
            drawLines()

        else:
            if gameOver(usedBoxes, mainBoard):
                tieScore += 1
                player,usedBoxes, mainBoard,  playerWins, computerWins = boardReset(player,usedBoxes, mainBoard,  playerWins, computerWins)
                DISPLAYSURF.fill(BGCOLOR)
                drawLines()

        
        

        drawScoreBoard(smallFont, playerScore, computerScore, tieScore)
        
                

        pygame.display.update()
        FPSCLOCK.tick(FPS)

       


###### Functions to set up the board  #########


def drawLines():

    #######VERTICAL LINES########
    
    left = XMARGIN + BOXSIZE
    top = YMARGIN
    width = GAPSIZE
    height = (BOXSIZE + GAPSIZE) * BOARDHEIGHT
    
    vertRect1 = pygame.Rect(left, top, width, height)
    pygame.draw.rect(DISPLAYSURF, WHITE, vertRect1)

    vertRect2 = pygame.Rect(left + BOXSIZE + GAPSIZE, top, width, height)
    pygame.draw.rect(DISPLAYSURF, WHITE, vertRect2)


    ########HORIZONTAL LINES ##########

    left = XMARGIN
    top = YMARGIN + BOXSIZE
    width = (BOXSIZE + GAPSIZE) * BOARDWIDTH
    height = GAPSIZE
    
    horizRect1 = pygame.Rect(left, top, width, height)
    pygame.draw.rect(DISPLAYSURF, WHITE, horizRect1)

    horizRect2 = pygame.Rect(left, top + BOXSIZE + GAPSIZE, width, height)
    pygame.draw.rect(DISPLAYSURF, WHITE, horizRect2)


def makeEachBoxFalse(val):
    usedBoxes = []
    for i in range(BOARDWIDTH):
        usedBoxes.append([val] * BOARDHEIGHT)
    return usedBoxes


def drawScoreBoard(smallFont, playerScore, computerScore, tieScore):
    scoreBoard = smallFont.render('Player: ' + str(playerScore) + '     ' + 'Computer: ' + str(computerScore) + '      ' + 'Tie: ' + str(tieScore), True, COMBLUE, BGCOLOR)
    scoreBoardRect = scoreBoard.get_rect()
    scoreBoardRect.x = 0
    scoreBoardRect.y = 0
    DISPLAYSURF.blit(scoreBoard, scoreBoardRect)







##### Coordinate Functions #####

def getBoxAtPixel(x, y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)


def leftTopCoordsOfBox(boxx, boxy):
    left = boxx *(BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return left, top


def centerxAndCenteryOfBox(boxx, boxy):
    centerx = boxx * (BOXSIZE + GAPSIZE) + XMARGIN + (BOXSIZE / 2)
    centery = boxy * (BOXSIZE + GAPSIZE) + YMARGIN + (BOXSIZE / 2) + 5
    return centerx, centery









##### Functions dealing with computer and player moves ######

def makeMove(player,usedBoxes,mainBoard, mainFont,boxx = None,boxy = None):
           
      #  if boxx == None and boxy == None:        
        if player == OMARK:
            spielfeld = [0]*9
            for y in range(3):
                for x in range(3):
                    if mainBoard[x][y] == MARKO:
                        spielfeld[x+3*y] = 1
                    if mainBoard[x][y] == MARKX:
                        spielfeld[x+3*y] = 2                
            
            (boxx, boxy) = bot.get_action(spielfeld)
            #boxx = random.randint(0,2)
            #boxy = random.randint(0,2)
            
        if boxx != None and boxy != None:

            if not usedBoxes[boxx][boxy]:
                markBox(player, boxx, boxy, mainFont)
                
                usedBoxes[boxx][boxy] = True
                mainBoard[boxx][boxy] = player
                if player == XMARK:
                    player = OMARK
                else: player = XMARK
                
                pygame.display.update()
                
                pygame.time.wait(500)
                
        return player



def markBox(player, boxx, boxy, mainFont):
    centerx, centery = centerxAndCenteryOfBox(boxx, boxy)
    mark = mainFont.render(player, True, GREEN)
    markRect = mark.get_rect()
    markRect.centerx = centerx
    markRect.centery = centery
    DISPLAYSURF.blit(mark, markRect)





def computerTurnWithAI(usedBoxes, mainBoard):
    
    """
    ## Step 1: Check to see if there is a winning move ##
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            mainBoardCopy = copy.deepcopy(mainBoard)
            if usedBoxes[boxx][boxy] == False:
                mainBoardCopy[boxx][boxy] = OMARK
                playerWins, computerWins = gameWon(mainBoardCopy)

                if computerWins == True:
                    return boxx, boxy




    ## Step 2: Check to see if there is a potential win that needs to be blocked ##
    
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDWIDTH):
            mainBoardCopy = copy.deepcopy(mainBoard)
            if usedBoxes[boxx][boxy] == False:
                mainBoardCopy[boxx][boxy] = XMARK
                playerWins, computerWins = gameWon(mainBoardCopy)

                if playerWins == True:
                    return boxx, boxy




    ## Step 3: Check if the center is empty ##

    mainBoardCopy = copy.deepcopy(mainBoard)

    if mainBoardCopy[1][1] == False:
        return 1, 1

    


    ## Step 4: Prevent a potential fork ##

    if ((mainBoardCopy[0][0] == mainBoardCopy[2][2] == XMARK) or
        (mainBoardCopy[0][2] == mainBoardCopy[2][0] == XMARK)):
        if mainBoardCopy[1][2] == False:
            return 1, 2

    if mainBoard[1][0] == XMARK:
        if mainBoard[0][1] == XMARK:
            if mainBoard[0][0] == False:
                return 0, 0

    if mainBoard[1][0] == XMARK:
        if mainBoard[2][1] == XMARK:
            if mainBoard[2][0] == False:
                return 2, 0

    if mainBoard[0][1] == XMARK:
        if mainBoard[1][2] == XMARK:
            if mainBoard[0][2] == False:
                return 0, 2

    if mainBoard[2][1] == XMARK:
        if mainBoard[1][2] == XMARK:
            if mainBoard[2][2] == False:
                return 2, 2
        

    if (mainBoard[0][2] == XMARK):
        if (mainBoard[2][1] == XMARK):
            if mainBoard[1][2] == False:
                return 1, 2
        elif (mainBoard[1][0]):
            if mainBoard[0][1] == False:
                return 0, 1

    if mainBoard[2][2] == XMARK:
        if mainBoard[0][1] == XMARK:
            if mainBoard[1][2] == False:
                return 1, 2
        elif mainBoard[1][0] == XMARK:
            if mainBoard[2][1] == False:
                return 2, 1

    if mainBoard[0][0] == XMARK:
        if mainBoard[2][1] == XMARK:
            if mainBoard[1][0] == False:
                return 1, 0
        elif mainBoard[1][2] == XMARK:
            if mainBoard[0][1] == False:
                return 0, 1

    if mainBoard[2][0] == XMARK:
        if mainBoard[1][2] == XMARK:
            if mainBoard[2][1] == False:
                return 2, 1
        elif mainBoard[0][1] == XMARK:
            if mainBoard[1][0] == False:
                return 1, 0

    

    

    
                            



    ## Step 5: Check if a corner is open ##
    
    xlist = [0, 2, 0, 2]
    ylist = [0, 2, 0, 2]

    random.shuffle(xlist)
    random.shuffle(ylist)

    for x in xlist:
        for y in ylist:
            if mainBoardCopy[x][y] == False:
                return x, y
    
    



    ## Step 6: Check if a side is open ##

    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            if mainBoardCopy[boxx][boxy] == False:
                return boxx, boxy

    """






##### Functions dealing with an end of game ########       

def gameWon(mainBoard):
    if ((mainBoard[0][0] == mainBoard[1][0] == mainBoard[2][0] == XMARK) or
        (mainBoard[0][1] == mainBoard[1][1] == mainBoard[2][1] == XMARK) or
        (mainBoard[0][2] == mainBoard[1][2] == mainBoard[2][2] == XMARK) or
        (mainBoard[0][0] == mainBoard[0][1] == mainBoard[0][2] == XMARK) or
        (mainBoard[1][0] == mainBoard[1][1] == mainBoard[1][2] == XMARK) or
        (mainBoard[2][0] == mainBoard[2][1] == mainBoard[2][2] == XMARK) or
        (mainBoard[0][0] == mainBoard[1][1] == mainBoard[2][2] == XMARK) or
        (mainBoard[0][2] == mainBoard[1][1] == mainBoard[2][0] == XMARK)):

        playerWins = True
        computerWins = False
        return playerWins, computerWins
    
    
    elif ((mainBoard[0][0] == mainBoard[1][0] == mainBoard[2][0] == OMARK) or
          (mainBoard[0][1] == mainBoard[1][1] == mainBoard[2][1] == OMARK) or
          (mainBoard[0][2] == mainBoard[1][2] == mainBoard[2][2] == OMARK) or
          (mainBoard[0][0] == mainBoard[0][1] == mainBoard[0][2] == OMARK) or
          (mainBoard[1][0] == mainBoard[1][1] == mainBoard[1][2] == OMARK) or
          (mainBoard[2][0] == mainBoard[2][1] == mainBoard[2][2] == OMARK) or
          (mainBoard[0][0] == mainBoard[1][1] == mainBoard[2][2] == OMARK) or
          (mainBoard[0][2] == mainBoard[1][1] == mainBoard[2][0] == OMARK)):

        playerWins = False
        computerWins = True
        return playerWins, computerWins

    
    else:
        playerWins = False
        computerWins = False
        return playerWins, computerWins


def gameOver(usedBoxes, mainBoard):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            if usedBoxes[boxx][boxy] == False:
                return False

    else:
        return True


def boardReset(player,usedBoxes, mainBoard,  playerWins, computerWins):
    pygame.time.wait(1000)
    usedBoxes = makeEachBoxFalse(False)
    mainBoard = makeEachBoxFalse(False)
    player = XMARK
    playerWins = computerWins = False

    return player,usedBoxes, mainBoard,  playerWins, computerWins


def highlightWin(mainBoard):

    scenario1 = 1
    scenario2 = 2
    scenario3 = 3
    scenario4 = 4
    scenario5 = 5
    scenario6 = 6
    scenario7 = 7
    scenario8 = 8
    
    if mainBoard[0][0] == mainBoard[1][0] == mainBoard[2][0]:
        highLightBoxes(mainBoard, scenario1)

    
    elif mainBoard[0][1] == mainBoard[1][1] == mainBoard[2][1]:
        highLightBoxes(mainBoard, scenario2)

    
    elif mainBoard[0][2] == mainBoard[1][2] == mainBoard[2][2]:
        highLightBoxes(mainBoard, scenario3)

    
    elif mainBoard[0][0] == mainBoard[0][1] == mainBoard[0][2]:
        highLightBoxes(mainBoard, scenario4)

    
    elif mainBoard[1][0] == mainBoard[1][1] == mainBoard[1][2]:
        highLightBoxes(mainBoard, scenario5)

    
    elif mainBoard[2][0] == mainBoard[2][1] == mainBoard[2][2]:
        highLightBoxes(mainBoard, scenario6)

    
    elif mainBoard[0][0] == mainBoard[1][1] == mainBoard[2][2]:
        highLightBoxes(mainBoard, scenario7)

    
    elif mainBoard[2][0] == mainBoard[1][1] == mainBoard[0][2]:
        highLightBoxes(mainBoard, scenario8)


def highLightBoxes(mainBoard, scenario):

    if scenario == 1:
        startPos = (XMARGIN + (BOXSIZE/2), YMARGIN + (BOXSIZE/2))
        endPos = (XMARGIN + BOXSIZE + GAPSIZE + BOXSIZE + GAPSIZE + (BOXSIZE/2), YMARGIN + (BOXSIZE/2))
        

        pygame.draw.line(DISPLAYSURF, LINECOLOR, startPos, endPos, 10)

    elif scenario == 2:
        startPos = (XMARGIN + (BOXSIZE/2), YMARGIN + BOXSIZE + GAPSIZE + (BOXSIZE/2))
        endPos = (XMARGIN + (BOXSIZE/2) + BOXSIZE + GAPSIZE + BOXSIZE + GAPSIZE, YMARGIN + BOXSIZE + GAPSIZE + (BOXSIZE/2))


        pygame.draw.line(DISPLAYSURF, LINECOLOR, startPos, endPos, 10)

    elif scenario == 3:
        startPos = (XMARGIN + (BOXSIZE/2), YMARGIN + BOXSIZE + GAPSIZE + BOXSIZE + GAPSIZE + (BOXSIZE/2))
        endPos = (XMARGIN + (BOXSIZE/2) + BOXSIZE + GAPSIZE + BOXSIZE + GAPSIZE, YMARGIN + BOXSIZE + GAPSIZE + BOXSIZE + GAPSIZE + (BOXSIZE/2))


        pygame.draw.line(DISPLAYSURF, LINECOLOR, startPos, endPos, 10)

    elif scenario == 4:
        startPos = (XMARGIN + (BOXSIZE/2), YMARGIN + (BOXSIZE/2))
        endPos = (XMARGIN + (BOXSIZE/2), YMARGIN + BOXSIZE + GAPSIZE + BOXSIZE + GAPSIZE + (BOXSIZE/2))
        

        pygame.draw.line(DISPLAYSURF, LINECOLOR, startPos, endPos, 10)

    elif scenario == 5:
        startPos = (XMARGIN + BOXSIZE + GAPSIZE + (BOXSIZE/2), YMARGIN + (BOXSIZE/2))
        endPos = (XMARGIN + BOXSIZE + GAPSIZE + (BOXSIZE/2), YMARGIN + BOXSIZE + GAPSIZE + BOXSIZE + GAPSIZE + (BOXSIZE/2))
        

        pygame.draw.line(DISPLAYSURF, LINECOLOR, startPos, endPos, 10)

    elif scenario == 6:
        startPos = (XMARGIN + BOXSIZE + GAPSIZE + BOXSIZE + GAPSIZE + (BOXSIZE/2), YMARGIN + (BOXSIZE/2))
        endPos = (XMARGIN + BOXSIZE + GAPSIZE + BOXSIZE + GAPSIZE + (BOXSIZE/2), YMARGIN + BOXSIZE + GAPSIZE + BOXSIZE + GAPSIZE + (BOXSIZE/2))
        

        pygame.draw.line(DISPLAYSURF, LINECOLOR, startPos, endPos, 10)

    elif scenario == 7:
        startPos = (XMARGIN + (BOXSIZE/2), YMARGIN + (BOXSIZE/2))
        endPos = (XMARGIN + BOXSIZE + GAPSIZE + BOXSIZE + GAPSIZE + (BOXSIZE/2), YMARGIN + BOXSIZE + GAPSIZE + BOXSIZE + GAPSIZE + (BOXSIZE/2))

        
        pygame.draw.line(DISPLAYSURF, LINECOLOR, startPos, endPos, 10)

    elif scenario == 8:
        startPos = (XMARGIN + BOXSIZE + GAPSIZE + BOXSIZE + GAPSIZE + (BOXSIZE/2), YMARGIN + (BOXSIZE/2))
        endPos = (XMARGIN + (BOXSIZE/2), YMARGIN + BOXSIZE + GAPSIZE + BOXSIZE + GAPSIZE + (BOXSIZE/2))
        

        pygame.draw.line(DISPLAYSURF, LINECOLOR, startPos, endPos, 10)
    
        
"""
def warGameEnding(smallFont, COMPUTERVOICE):

    surfRect = DISPLAYSURF.get_rect()
    DISPLAYSURF.fill(BGCOLOR)

    computerMessage1 = smallFont.render('A strange game...', True, COMBLUE, BGCOLOR)
    computerMessage1Rect = computerMessage1.get_rect()
    computerMessage1Rect.x = XMARGIN/3
    computerMessage1Rect.y = YMARGIN * 2

    uncoverWords(computerMessage1, computerMessage1Rect)
    pygame.time.wait(1000)
        

    computerMessage2 = smallFont.render('The only winning move is not to play.', True, COMBLUE, BGCOLOR)
    computerMessage2Rect = computerMessage2.get_rect()
    computerMessage2Rect.x = XMARGIN/3
    computerMessage2Rect.centery = (YMARGIN * 2) + 50

    uncoverWords(computerMessage2, computerMessage2Rect)
    pygame.time.wait(3000)




def uncoverWords(text, textRect):
    textRectCopy = copy.deepcopy(textRect)
    blackRect = textRectCopy
    textLength = textRect.width

    revealSpeed = 5
    

    for i in range((textLength / revealSpeed) + 1):
        DISPLAYSURF.blit(text, textRect)
        pygame.draw.rect(DISPLAYSURF, BLACK, blackRect)
        pygame.display.update()

        blackRect.x += revealSpeed
        blackRect.width -= revealSpeed

"""  
    

if __name__ == '__main__':
    main()




    
