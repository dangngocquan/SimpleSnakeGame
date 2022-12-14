from cv2 import _InputArray_KIND_MASK
import pygame
from account import ACCOUNT_MANAGER
from setting import *
import setting
from grid import *
from button import Button

###########   VARIABLE   ####################################################################################
ANIMATION_SPEED = SETTING1['MENU']['ANIMATION_SPEED']
BIG_FONT = SETTING2['MENU']['BIG_FONT']
MEDIUM_FONT = SETTING2['MENU']['MEDIUM_FONT']
MEDIUM_FONT_HORVED = SETTING2['MENU']['MEDIUM_FONT_HORVED']
MEDIUM_FONT_2 = SETTING2['MENU']['MEDIUM_FONT_2']
SMALL_FONT = SETTING2['MENU']['SMALL_FONT']
DESCRIPTION_FONT = SETTING2['MENU']['DESCRIPTION_FONT']
WHITE = SETTING2['COLOR']['WHITE']


###########  CLASS GET PASSWORD MENU  ###############################################################################
class GetPasswordMenu:
    ###########  Constructor  ###############################################################################
    def __init__(self, x, y, width, height,
                 textWhenCorrect="Password is correct !!!",
                 textWhenIncorrect="Password is incorrect. Please try again.",
                 textHint="Do you know my birthday? Let's write it =))"):
        ###########  Surface, cursor   ######################################################################
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.surfaceRect = self.surface.get_rect()
        self.surfaceRect.center = (x, y)
        
        self.textWhenCorrect = textWhenCorrect
        self.textWhenIncorrect = textWhenIncorrect
        self.textHint = textHint
        
        self.container0 = pygame.Surface((width, height-40), pygame.SRCALPHA)
        self.container0Rect = self.container0.get_rect()
        self.container0Rect.topleft = (0, 20)
        
        self.container1 = pygame.Surface((width-12, (self.container0Rect.height-12-4)//2), pygame.SRCALPHA)
        self.container1Rect = self.container1.get_rect()
        self.container1Rect.topleft = (6, 6)
        
        self.cells = []
        self.titleDigits = []
        for i in range(6):
            cell = pygame.Surface(
                (self.container1Rect.width//6 - 20, self.container1Rect.height - 40), 
                pygame.SRCALPHA)
            cellRect = cell.get_rect()
            cellRect.topleft = (10 + self.container1Rect.width//6*i, 20)
            self.cells.append([cell, cellRect])
            
            titleDigit = Button("", MEDIUM_FONT, cellRect.width//2, cellRect.height//2)
            self.titleDigits.append(titleDigit)
        
        self.container2 = pygame.Surface((width-12, (self.container0Rect.height-12-4)//2), pygame.SRCALPHA)
        self.container2Rect = self.container2.get_rect()
        self.container2Rect.topleft = (6, 6+4+self.container1Rect.height)
        
        self.descriptionBox = pygame.Surface(
            (self.container2Rect.width-20, self.container2Rect.height-40), 
            pygame.SRCALPHA)
        self.descriptionBoxRect = self.descriptionBox.get_rect()
        self.descriptionBoxRect.topleft = (10, 20)
        
        self.titleDescription = Button(self.textHint, 
                                       DESCRIPTION_FONT_2, self.descriptionBoxRect.width//2, 
                                       self.descriptionBoxRect.height//2)
        
        self.inputDigits = []
        
        self.FPS = ANIMATION_SPEED
        self.cursor = 0
        ########### Buttons   ###############################################################################
        self.titlePassword = Button("PASSWORD", MEDIUM_FONT, width//2, 20)
        self.titlePassword.isChosen = True
        self.titleCancer = Button("CANCER", MEDIUM_FONT_2, width//4, height-20)
        self.titleEnter = Button("ENTER", MEDIUM_FONT_2, width//4*3, height-20)
        
    def addDigit(self, digit):
        length = len(self.inputDigits)
        if length < 6:
            self.inputDigits.append(digit)
            self.titleDigits[length].update(str(digit), MEDIUM_FONT)
            
    def removeDigit(self):
        length = len(self.inputDigits)
        if length > 0:
            self.inputDigits.pop(length-1)
            self.titleDigits[length-1].update("", MEDIUM_FONT)
            
    def removeAllDigits(self):
        length = len(self.inputDigits)
        while len(self.inputDigits) > 0:
            length = len(self.inputDigits)
            self.inputDigits.pop(length-1)
            self.titleDigits[length-1].update("", MEDIUM_FONT)
            
    def checkPassword(self):
        password = ['1', '0', '0', '4', '0', '3']
        if self.inputDigits == password :
            self.titleDescription.update(self.textWhenCorrect, DESCRIPTION_FONT_2)
            return True
        else:
            self.titleDescription.update(self.textWhenIncorrect, DESCRIPTION_FONT_2)
            return False
            
    def resetDefaultDescription(self):
        self.titleDescription.update(self.textHint, DESCRIPTION_FONT_2)
            
        
    ###########  Update cursor and button status in Get Password Menu #######################################
    def update(self):
        ###########  Update cursor and button of Get Password Menu  #########################################
        if self.cursor == 0:
            self.titleEnter.isChosen = True
            self.titleCancer.isChosen = False
            self.titleEnter.update('ENTER', MEDIUM_FONT_HORVED, 'G')
            self.titleCancer.update('CANCER', MEDIUM_FONT, 'G')
        elif self.cursor == 1:
            self.titleEnter.isChosen = False
            self.titleCancer.isChosen = True
            self.titleEnter.update('ENTER', MEDIUM_FONT, 'G')
            self.titleCancer.update('CANCER', MEDIUM_FONT_HORVED, 'G')
        self.titlePassword.update("PASSWORD", MEDIUM_FONT, 'ALL')
        ###########  Remove old button display  #############################################################
        self.surface.fill((0, 0, 0, 0))
        self.container0.fill((0, 0, 255))
        self.container1.fill((170, 200, 255))
        self.container2.fill((170, 200, 255))
        for i in range(6):
            self.cells[i][0].fill((100, 100, 100))
            self.cells[i][0].blit(self.titleDigits[i].text, self.titleDigits[i].textRect)
            self.container1.blit(self.cells[i][0], self.cells[i][1])    
        self.descriptionBox.fill((100, 100, 100))
        ###########  Draw new button   ######################################################################
        self.descriptionBox.blit(self.titleDescription.text, self.titleDescription.textRect)
        self.container2.blit(self.descriptionBox, self.descriptionBoxRect)
        self.container0.blit(self.container1, self.container1Rect)
        self.container0.blit(self.container2, self.container2Rect)
        self.surface.blit(self.container0, self.container0Rect)
        self.titlePassword.draw(self.surface)
        self.titleEnter.draw(self.surface)
        self.titleCancer.draw(self.surface)
        
    
    ###########  Draw Get Password Menu in another surface  #################################################
    def draw(self, parentSurface):
        parentSurface.blit(self.surface, self.surfaceRect)
        
        


###########  CLASS GET INPUT STRING MENU  ###################################################################
class GetInputStringMenu:
    ###########  Constructor  ###############################################################################
    def __init__(self, x, y, width, height, title = "", lengthMax = 18,
                 textWhenCorrect="Create new account succeeded.",
                 textWhenIncorrect="Your name is existing or invalid. Please try again.",
                 textHint="The name include character a-z, 0-9, max length is 18."):
        ###########  Surface, cursor   ######################################################################
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.surfaceRect = self.surface.get_rect()
        self.surfaceRect.center = (x, y)
        
        self.title = title
        self.textWhenCorrect = textWhenCorrect
        self.textWhenIncorrect = textWhenIncorrect
        self.textHint = textHint
        self.lengthMax = lengthMax
                
        self.FPS = ANIMATION_SPEED
        self.cursor = 0
        
        ######################   Surface in Main surface   ###################################################
        self.container0 = pygame.Surface((width, height-40), pygame.SRCALPHA)
        self.container0Rect = self.container0.get_rect()
        self.container0Rect.topleft = (0, 20)
        
        self.titleMain = Button(self.title, MEDIUM_FONT, width//2, 20)
        self.titleMain.isChosen = True
        self.titleCancer = Button("CANCER", MEDIUM_FONT_2, width//4, height-20)
        self.titleEnter = Button("ENTER", MEDIUM_FONT_2, width//4*3, height-20)
        ######################   Surface in Container0   #####################################################
        self.container1 = pygame.Surface((width-12, (self.container0Rect.height-12-4)//2), pygame.SRCALPHA)
        self.container1Rect = self.container1.get_rect()
        self.container1Rect.topleft = (6, 6)
        
        self.container2 = pygame.Surface((width-12, (self.container0Rect.height-12-4)//2), pygame.SRCALPHA)
        self.container2Rect = self.container2.get_rect()
        self.container2Rect.topleft = (6, 6+4+self.container1Rect.height)
        
        #####################   Surface, text and Button in Container1   #####################################
        self.inputCell = pygame.Surface(
            (self.container1Rect.width - 6, self.container1Rect.height - 40), pygame.SRCALPHA)
        self.inputCellRect = self.inputCell.get_rect()
        self.inputCellRect.topleft = (3, 20)
        
        self.inputString = ""
        self.titleInputString = Button(self.inputString, MEDIUM_FONT, 
                                       self.inputCellRect.width//2, self.inputCellRect.height//2)
        
        
        #####################   Surface, text and Button in Container2   #####################################
        self.descriptionBox = pygame.Surface(
            (self.container2Rect.width-20, self.container2Rect.height-40), 
            pygame.SRCALPHA)
        self.descriptionBoxRect = self.descriptionBox.get_rect()
        self.descriptionBoxRect.topleft = (10, 20)
        
        self.titleDescription = Button(self.textHint, 
                                       DESCRIPTION_FONT_2, self.descriptionBoxRect.width//2, 
                                       self.descriptionBoxRect.height//2)

        
        
    def addChar(self, char):
        if char in 'abcdefghijklmnopqrstuvwxyz0123456789':
            length = len(self.inputString)
            if length < self.lengthMax:
                self.inputString += char
            
    def removeChar(self):
        length = len(self.inputString)
        if length > 0:
            self.inputString = self.inputString[0:length-1]
     
    def removeAllChars(self):
        self.inputString = ""
            
    def resetDefaultDescription(self):
        self.titleDescription.update(self.textHint, DESCRIPTION_FONT_2)
    
    
        
    ###########  Update cursor and button status in Get Input String Menu ###################################
    def update(self):
        ###########  Update cursor and button of Get Input String menu  #####################################
        if self.cursor == 0:
            self.titleEnter.isChosen = True
            self.titleCancer.isChosen = False
            self.titleEnter.update('ENTER', MEDIUM_FONT_HORVED, 'G')
            self.titleCancer.update('CANCER', MEDIUM_FONT, 'G')
        elif self.cursor == 1:
            self.titleEnter.isChosen = False
            self.titleCancer.isChosen = True
            self.titleEnter.update('ENTER', MEDIUM_FONT, 'G')
            self.titleCancer.update('CANCER', MEDIUM_FONT_HORVED, 'G')
        else:
            self.titleEnter.isChosen = False
            self.titleCancer.isChosen = False
            self.titleEnter.update('ENTER', MEDIUM_FONT, 'G')
            self.titleCancer.update('CANCER', MEDIUM_FONT, 'G')
        self.titleMain.update(self.title, MEDIUM_FONT, 'ALL')
        self.titleInputString.update(self.inputString, MEDIUM_FONT, 'G')
        ###########  Remove old button display  #############################################################
        self.surface.fill((0, 0, 0, 0))
        self.container0.fill((0, 0, 255))
        self.container1.fill((170, 200, 255))
        self.container2.fill((170, 200, 255))
        self.inputCell.fill((100, 100, 100))
        self.descriptionBox.fill((100, 100, 100))
        ###########  Draw new button   ######################################################################
        self.descriptionBox.blit(self.titleDescription.text, self.titleDescription.textRect)
        self.inputCell.blit(self.titleInputString.text, self.titleInputString.textRect)
        self.container1.blit(self.inputCell, self.inputCellRect)
        self.container2.blit(self.descriptionBox, self.descriptionBoxRect)
        self.container0.blit(self.container1, self.container1Rect)
        self.container0.blit(self.container2, self.container2Rect)
        self.surface.blit(self.container0, self.container0Rect)
        self.titleMain.draw(self.surface)
        self.titleEnter.draw(self.surface)
        self.titleCancer.draw(self.surface)
        
    
    ###########  Draw Get Input String Menu in another surface  #############################################
    def draw(self, parentSurface):
        parentSurface.blit(self.surface, self.surfaceRect)