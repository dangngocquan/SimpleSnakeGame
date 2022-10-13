import pygame
from setting import *
from grid import *
from button import Button
from menuGetInput import GetPasswordMenu

###########   VARIABLE   ####################################################################################
ANIMATION_SPEED = SETTING1['MENU']['ANIMATION_SPEED']
BIG_FONT = SETTING2['MENU']['BIG_FONT']
MEDIUM_FONT = SETTING2['MENU']['MEDIUM_FONT']
MEDIUM_FONT_HORVED = SETTING2['MENU']['MEDIUM_FONT_HORVED']
MEDIUM_FONT_2 = SETTING2['MENU']['MEDIUM_FONT_2']
SMALL_FONT = SETTING2['MENU']['SMALL_FONT']
DESCRIPTION_FONT = SETTING2['MENU']['DESCRIPTION_FONT']
WHITE = SETTING2['COLOR']['WHITE']


##########   Load data of Statistics from json file   ############################################################
def loadData(path='./data/history/history.json'):
    data = None
    with open(path, 'r') as file:
        data = json.load(file)
    file.close()
    return data

HISTORY = loadData()

###########   Save data of Account Manager to json file   ############################################################
def saveData(path='./data/history/history.json'):   
    with open(path, 'w') as file:
        json.dump(HISTORY, file, indent=4)
    file.close()


###########  CLASS HISTORY MENU  ##########################################################################
class HistoryMenu:
    ###########  Constructor  ###############################################################################
    def __init__(self, x, y, width, height):
        ###########  Surface, cursor and coordinate center  #################################################
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.surfaceRect = self.surface.get_rect()
        self.surfaceRect.center = (x, y)
        
        self.container0 = pygame.Surface((900, 420), pygame.SRCALPHA)
        self.container0Rect = self.container0.get_rect()
        self.container0Rect.center = (width//2, height//2)
        
        ##################   Surfaces in Container0   #######################################################
        self.container1 = pygame.Surface((self.container0Rect.width, 60), pygame.SRCALPHA)
        self.container1Rect = self.container1.get_rect()
        self.container1Rect.topleft = (0, 0)
        
        self.container2 = pygame.Surface(
            (self.container0Rect.width, self.container0Rect.height - self.container1Rect.height), pygame.SRCALPHA)
        self.container2Rect = self.container2.get_rect()
        self.container2Rect.topleft = (0 , self.container1Rect.height)
        
        ##################   Cells and text in Container1    #################################################
        self.columnAccount = pygame.Surface((self.container1Rect.width//8*2, 60), pygame.SRCALPHA)
        self.columnAccountRect = self.columnAccount.get_rect()
        self.columnAccountRect.topleft = (0, 0)
        self.titleAccount = Button("Account", DESCRIPTION_FONT_2, 10, 10, 'topLeft')
        
        self.columnTime = pygame.Surface((self.container1Rect.width//8*2, 60), pygame.SRCALPHA)
        self.columnTimeRect = self.columnTime.get_rect()
        self.columnTimeRect.topleft = (self.columnAccountRect.topright[0], 0)
        self.titleTime = Button("Time", DESCRIPTION_FONT_2, 10, 10, 'topLeft')
        
        self.columnScore = pygame.Surface((self.container1Rect.width//8*1, 60), pygame.SRCALPHA)
        self.columnScoreRect = self.columnScore.get_rect()
        self.columnScoreRect.topleft = (self.columnTimeRect.topright[0], 0)
        self.titleScore = Button("Score", DESCRIPTION_FONT_2, 10, 10, 'topLeft')
        
        self.columnResult = pygame.Surface((self.container1Rect.width//8*1, 60), pygame.SRCALPHA)
        self.columnResultRect = self.columnResult.get_rect()
        self.columnResultRect.topleft = (self.columnScoreRect.topright[0], 0)
        self.titleResult = Button("Result", DESCRIPTION_FONT_2, 10, 10, 'topLeft')
        
        self.columnTypeGame = pygame.Surface((self.container1Rect.width//8*2, 60), pygame.SRCALPHA)
        self.columnTypeGameRect = self.columnTypeGame.get_rect()
        self.columnTypeGameRect.topleft = (self.columnResultRect.topright[0], 0)
        self.titleTypeGame = Button("Type Game", DESCRIPTION_FONT_2, 10, 10, 'topLeft')
        
        
        
        self.FPS = ANIMATION_SPEED
        self.cursor = 0
        self.positionMouse = (-100, -100)
        self.positionLeftMouse = (-100, -100)
        ########### Buttons in Statistics Menu  ##############################################################
        self.title = Button("HISTORY", MEDIUM_FONT, width//2, height//24*2)
        self.titleBack = Button("BACK", MEDIUM_FONT, width//2, height*22//24)
    
    
    def updatePostionMouse(self, position):
        self.positionMouse = position
        
    def isPointedAt(self, positionMouse=(0, 0), parent3SurfaceRect=None, 
                    parent2SurfaceRect=None, parent1SurfaceRect=None, surfaceCheckRect=None):
        if surfaceCheckRect == None:
            return False
        x0 = positionMouse[0]
        y0 = positionMouse[1]
        x1 = 0
        y1 = 0
        if parent3SurfaceRect != None:
            x1 += parent3SurfaceRect.topleft[0]
            y1 += parent3SurfaceRect.topleft[1]
        if parent2SurfaceRect != None:
            x1 += parent2SurfaceRect.topleft[0]
            y1 += parent2SurfaceRect.topleft[1]
        if parent1SurfaceRect != None:
            x1 += parent1SurfaceRect.topleft[0]
            y1 += parent1SurfaceRect.topleft[1]
        x1 += surfaceCheckRect.topleft[0]
        y1 += surfaceCheckRect.topleft[1]
        x2 = x1 + surfaceCheckRect.width
        y2 = y1 + surfaceCheckRect.height
        
        return (x1 < x0 and x0 < x2 and y1 < y0 and y0 < y2)
        
    def updateMousePoitedAt(self):
        if self.isPointedAt(positionMouse=self.positionMouse,
                            surfaceCheckRect=self.titleBack.textRect):
            self.cursor = 0
        else:
            self.cursor = 1
    
    
    def updatePositionLeftMouse(self):
        self.positionLeftMouse = self.positionMouse
        if self.isPointedAt(positionMouse=self.positionLeftMouse,
                            surfaceCheckRect=self.titleBack.textRect):
            self.cursor = -1
    
    
    
    ###########   Update cursor and buttons status in Play Game Menu   ######################################
    def update(self):
        ###########   Update cursor and buttons   ###########################################################
        self.updateMousePoitedAt()
        if self.cursor == 0:
            self.titleBack.isChosen = True
            self.titleBack.update("BACK", MEDIUM_FONT_HORVED, 'G')
        else:
            self.titleBack.isChosen = False
            self.titleBack.update("BACK", MEDIUM_FONT, 'G')
        
        ###########   Remove old button display   ###########################################################
        self.surface.fill((0, 0, 0, 0))
        self.container0.fill((111, 111, 111))
        self.container1.fill((50, 50, 50))
        self.columnAccount.fill((50, 50, 50))
        self.columnTime.fill((50, 50, 50))
        self.columnScore.fill((50, 50, 50))
        self.columnResult.fill((50, 50, 50))
        self.columnTypeGame.fill((50, 50, 50))
        self.container2.fill((80, 80, 80))
        ###########   Draw new buttons   ####################################################################
        self.title.draw(self.surface)
        self.titleBack.draw(self.surface)
        
        self.titleAccount.draw(self.columnAccount)
        self.titleTime.draw(self.columnTime)
        self.titleScore.draw(self.columnScore)
        self.titleResult.draw(self.columnResult)
        self.titleTypeGame.draw(self.columnTypeGame)
        
        self.container1.blit(self.columnAccount, self.columnAccountRect)
        self.container1.blit(self.columnTime, self.columnTimeRect)
        self.container1.blit(self.columnScore, self.columnScoreRect)
        self.container1.blit(self.columnResult, self.columnResultRect)
        self.container1.blit(self.columnTypeGame, self.columnTypeGameRect)
        
        self.container0.blit(self.container1, self.container1Rect)
        self.container0.blit(self.container2, self.container2Rect)
        self.surface.blit(self.container0, self.container0Rect)

    
    ###########  Draw PlayGame Menu in another surface  #####################################################
    def draw(self, parentSurface):
        parentSurface.blit(self.surface, self.surfaceRect)