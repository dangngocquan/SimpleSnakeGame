from codecs import ignore_errors
import sys
import pygame
from food import FoodManager

from menu import MainMenu, PlayGameMenu, GameOverMenu
from inGame import InGame
from snake import Snake

###########  SCREEN SETTING  ################################################################################
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_CAPTION = "Simple Snake Gameeee"
FPS = 60

###########  COLOR  #########################################################################################
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

###########   CLASS GAME   ##################################################################################
class Game:
    ###########   Constructor   #############################################################################
    def __init__(self):
        ###########   Create window game, caption, clock   ##################################################
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(SCREEN_CAPTION)
        self.clock = pygame.time.Clock()
        self.countTicks = 0
        
        ###########   Status in game   ######################################################################
        self.running = True
        self.runningMainMenu = True
        self.runningPlayGameMenu = False
        self.runningInGame = False
        self.runningContinueGameMenu = False
        self.runningOptionsMenu = False
        self.runningGameOverMenu = False
        
        ###########   Screens in game   #####################################################################
        self.mainMenu = MainMenu(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.playGameMenu = PlayGameMenu(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.inGame = InGame()
        self.gameOverMenu = GameOverMenu(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, SCREEN_WIDTH, SCREEN_HEIGHT, self.inGame.snake)
    
    ###########   Main loop in game   #######################################################################
    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.getEvents()
            for i in range(1000):
                self.countTicks = (self.countTicks + 1) % (FPS * 1000)
                self.update()
            self.display()
    
    ###########   Get events in current screen   ############################################################    
    def getEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running =False
                pygame.quit()
                sys.exit()
            ###########   Get events when current screen is Main Menu   #####################################
            if self.runningMainMenu:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.mainMenu.cursor += 1
                        self.mainMenu.cursor %= 2
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.mainMenu.cursor -= 1
                        self.mainMenu.cursor %= 2
                    elif event.key == pygame.K_RETURN:
                        if self.mainMenu.cursor == 0:
                            self.runningPlayGameMenu = True
                            self.playGameMenu.cursor = 0
                        elif self.mainMenu.cursor == 1:
                            self.runningOptionsMenu = True
                        self.runningMainMenu = False
            ###########   Get events when current screen is Play Game Menu  #################################
            elif self.runningPlayGameMenu:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.playGameMenu.cursor += 1
                        self.playGameMenu.cursor %= 3
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.playGameMenu.cursor -= 1
                        self.playGameMenu.cursor %= 3
                    if event.key == pygame.K_RETURN:
                        if self.playGameMenu.cursor == 0:
                            self.runningInGame = True
                            self.inGame.showingScreenStart = True
                        elif self.playGameMenu.cursor == 1:
                            self.runningContinueGameMenu = True
                        elif self.playGameMenu.cursor == 2:
                            self.runningMainMenu = True
                            self.mainMenu.cursor = 0
                        self.runningPlayGameMenu = False
            ###########   Get events when current screen is Options Menu   ##################################
            elif self.runningOptionsMenu:
                pass
            ###########   Get events when current screen is InGame (player controls snake)   ################
            elif self.runningInGame:
                ###########   Get events when current screen is Start InGame   ##############################
                if self.inGame.showingScreenStart:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.inGame.showingScreenStart = False
                            self.inGame.running = True
                ###########   Get events when snake moving   ################################################
                elif self.inGame.running:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                            pass
                        elif event.key == pygame.K_UP or event.key == pygame.K_w:
                            if self.inGame.snake.currentDirection != 'DD' and self.inGame.snake.checkSnakeCanMove('UU'):
                                self.inGame.snake.currentDirection = 'UU'
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            if self.inGame.snake.currentDirection != 'UU' and self.inGame.snake.checkSnakeCanMove('DD'):
                                self.inGame.snake.currentDirection = 'DD'
                        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            if self.inGame.snake.currentDirection != 'LL' and self.inGame.snake.checkSnakeCanMove('RR'):
                                self.inGame.snake.currentDirection = 'RR'
                        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            if self.inGame.snake.currentDirection != 'RR' and self.inGame.snake.checkSnakeCanMove('LL'):
                                self.inGame.snake.currentDirection = 'LL'
                ###########   Get events when game pause   ##################################################
                elif self.inGame.waiting:
                    pass
            elif self.runningGameOverMenu:
                 if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.gameOverMenu.cursor += 1
                        self.gameOverMenu.cursor %= 2
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.gameOverMenu.cursor -= 1
                        self.gameOverMenu.cursor %= 2
                    elif event.key == pygame.K_RETURN:
                        if self.gameOverMenu.cursor == 0:
                            self.runningInGame = True
                            self.inGame.showingScreenStart = True
                        elif self.gameOverMenu.cursor == 1:
                            self.runningMainMenu = True
                        self.inGame.snake = Snake()
                        self.inGame.foodManager = FoodManager()
                        self.inGame.showingScreenStart = True
                        self.runningGameOverMenu = False
                        
                
                    
            ###########   Get events when current screen is Continue Game Menu   ############################
            elif self.runningContinueGameMenu:
                pass
                        
    ###########   Update screen with current status   #######################################################       
    def update(self):
        if self.runningMainMenu:
            if self.countTicks % (FPS * 1000 // self.mainMenu.FPS) == 0:
                self.mainMenu.update()
        elif self.runningPlayGameMenu:
            if self.countTicks % (FPS * 1000 // self.mainMenu.FPS) == 0:
                self.playGameMenu.update()
        elif self.runningInGame:
            if self.inGame.snake.died():
                self.inGame.running = False
                self.runningInGame = False
                self.runningGameOverMenu = True
                self.gameOverMenu = GameOverMenu(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, SCREEN_WIDTH, SCREEN_HEIGHT, self.inGame.snake)
            if self.inGame.showingScreenStart:
                if self.countTicks % (FPS * 1000 // self.inGame.snake.frameTransitionSpeed) == 0:
                    self.inGame.update(type='UpdateSnakeFrame')
                if self.countTicks % (FPS * 1000 // self.mainMenu.FPS) == 0:
                    self.inGame.update()
            elif self.inGame.running:
                if self.countTicks % (FPS * 1000 // self.inGame.snake.frameTransitionSpeed) == 0:
                    self.inGame.update(type='UpdateSnakeFrame')
                if self.countTicks % (FPS * 1000 // self.inGame.foodManager.frameTransitionSpeed) == 0:
                    self.inGame.update(type='UpdateFoodFrame')
                if self.countTicks % (FPS * 1000 // self.inGame.snake.speed) == 0:
                    self.inGame.update()
            elif self.inGame.waiting:
                pass
        elif self.runningGameOverMenu:
            if self.countTicks % (FPS * 1000 // self.inGame.snake.dropSpeed) == 0:
                    self.gameOverMenu.update(type='UpdateSnakeFrameDrop')
            if self.countTicks % (FPS * 1000 // self.gameOverMenu.FPS) == 0:
                self.gameOverMenu.update()
            
        
    ###########   Draw screen with current status and show it   #############################################
    def display(self):
        self.screen.fill(BLACK)
        if self.runningInGame:
            self.inGame.draw(self.screen)
        elif self.runningMainMenu:
            self.mainMenu.draw(self.screen)
        elif self.runningPlayGameMenu:
            self.playGameMenu.draw(self.screen)
        elif self.runningGameOverMenu:
            self.gameOverMenu.draw(self.screen)
        pygame.display.flip()