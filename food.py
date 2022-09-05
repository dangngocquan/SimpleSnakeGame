import pygame
import random


###########  SETTING  #######################################################################################
CELL_SIZE = 25
INGAME_WIDTH = 1000
INGAME_HEIGHT = 600
NUMBER_ROWS = INGAME_HEIGHT // CELL_SIZE
NUMBER_COLUMNS = INGAME_WIDTH // CELL_SIZE
DEFAULT_MAX_FOOD = 7
DEFAULT_FOOD_TRANSITION_SPEED = 6

###########  IMAGES  ########################################################################################
FOOD = []
for i in range(4):
    img = pygame.image.load("./assets/images/food/food" + str(i) + ".png")
    img = pygame.transform.scale(img, (CELL_SIZE, CELL_SIZE))
    FOOD.append(img)

###########  CLASS FOOD  ####################################################################################
class Food:
    ########### Constructor  ################################################################################
    def __init__(self, x, y):
        ###########  Create surface   #######################################################################
        self.surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
        self.surfaceRect = self.surface.get_rect()
        self.surfaceRect.topleft = (x, y)
        self.x = x
        self.y = y
        
        ###########  Default image food  ####################################################################
        self.surface.blit(FOOD[0], (0, 0))
        self.indexFrame = 0
    
    ###########  Get coordinate of food  ####################################################################
    def coordinate(self):
        return [self.x, self.y]
    
    ###########  Update image of food  ######################################################################
    def update(self):
        # self.indexFrame = (self.indexFrame + 1) % 4
        ###########  Remove old image food  #################################################################
        self.surface.fill((0, 0, 0, 0))
        ###########  Draw new image food  ###################################################################
        self.surface.blit(FOOD[self.indexFrame], (0, 0))
    
    ###########  Draw Food on another surface  ##############################################################
    def draw(self, parentSurface):
        parentSurface.blit(self.surface, self.surfaceRect)


###########  CLASS FOOD MANAGER  ############################################################################
class FoodManager:
    ###########  Constructor  ###############################################################################
    def __init__(self):
        ###########  Surface and coordinate #################################################################
        self.surface = pygame.Surface((INGAME_WIDTH, INGAME_HEIGHT), pygame.SRCALPHA)
        self.surfaceRect = self.surface.get_rect()
        self.surfaceRect.topleft = (0, 0)
        ###########  List food anf  number of foods  ########################################################
        self.listFood = []
        self.maxFood = DEFAULT_MAX_FOOD
        self.frameTransitionSpeed = DEFAULT_FOOD_TRANSITION_SPEED
    
    ###########  Get coordinate of all foods ################################################################
    def coordinateFoods(self):
        return [food.coordinate() for food in self.listFood]
    
    ###########  Create a random Food  ######################################################################
    def createRandomValidFood(self, coordinateSnakeBlockss=[]):
        if len(self.listFood) + len(coordinateSnakeBlockss) >= NUMBER_ROWS * NUMBER_COLUMNS:
            return None
        randomX = random.randint(0, NUMBER_COLUMNS-1) * CELL_SIZE
        randomY = random.randint(0, NUMBER_ROWS-1) * CELL_SIZE
        while ([randomX, randomY] in (self.coordinateFoods() + coordinateSnakeBlockss)):
            randomX = random.randint(0, NUMBER_COLUMNS-1) * CELL_SIZE
            randomY = random.randint(0, NUMBER_ROWS-1) * CELL_SIZE
        return Food(randomX, randomY)
    
    ###########  Update status food man #####################################################################
    def supplementFood(self, coordinateSnakeBlockss):
        ###########  Supplement the Food Manager  ###########################################################
        while len(self.listFood) < self.maxFood:
            randomValidFood = self.createRandomValidFood(coordinateSnakeBlockss)
            if randomValidFood == None:
                break
            else:
                self.listFood.append(randomValidFood)
        ###########  Remove old image foods  ################################################################
        self.surface.fill((0, 0, 0, 0))
        ###########  Draw all new image foods  ##############################################################
        for food in self.listFood:
            food.update()
            food.draw(self.surface)
        
    
    def updateFrameFoods(self):
        self.surface.fill((0, 0, 0, 0))
        for food in self.listFood:
            food.indexFrame = (food.indexFrame + 1) % 4
            food.update()
            food.draw(self.surface)
    
    ###########  Draw all foods on another surface  #########################################################
    def draw(self, parentSurface):
        parentSurface.blit(self.surface, self.surfaceRect) 