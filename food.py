import pygame
import random
from setting import *
import setting

###########   VARIABLE   ####################################################################################
WIDTH = SETTING2['SCREEN']['WIDTH']
HEIGHT = SETTING2['SCREEN']['HEIGHT']
NUMBER_ROWS = SETTING2['SCREEN']['NUMBER_ROWS']
NUMBER_COLUMNS = SETTING2['SCREEN']['NUMBER_COLUMNS']
CELL_SIZE = SETTING2['SCREEN']['CELL_SIZE']
FOOD = SETTING2['FOOD']


###########   Load data of foods from json file   ###########################################################
def loadPreviousFoodManager(path='./data/player/onePlayer/food/food.json'):
    foodManagerDict = None

    with open(path, 'r') as file:
        foodManagerDict = json.load(file)
    file.close()
    
    foodDict = foodManagerDict['FOOD_MANAGER'][SETTING1['ACCOUNT']['INDEX_ACCOUNT']]
    
    listFood = []
    for food in foodDict['FOODS']:
        listFood.append(Food(x=food['x'], y=food['y'], indexFrame=food['indexFrame']))
        
    return FoodManager(listFood=listFood)

###########   Save data of current foods to json file   #####################################################
def saveFoodManager(foodManager, path='./data/player/onePlayer/food/food.json'):
    foodDict = {
        'FOODS' : [
           
        ]
    }
    for food in foodManager.listFood:
        foodDict['FOODS'].append(
            {
                'x' : food.x,
                'y' : food.y,
                'indexFrame' : food.indexFrame
            }
        )
    
    foodManagerDict = None
    with open(path, 'r') as file:
        foodManagerDict = json.load(file)
    file.close()
    
    for indexAccount in range(len(foodManagerDict['FOOD_MANAGER'])):
        if indexAccount == SETTING1['ACCOUNT']['INDEX_ACCOUNT']:
            foodManagerDict['FOOD_MANAGER'][indexAccount] = foodDict
    
    with open(path, 'w') as file:
        json.dump(foodManagerDict, file, indent=4)
    file.close()


def removeFoodManager(index=-1, path='./data/player/onePlayer/food/food.json',
                      path2='./data/player/twoPlayer/food/food.json'):
    if index >= 0:
        foodManagerDict = None
        with open(path, 'r') as file:
            foodManagerDict = json.load(file)
        file.close()
        foodManagerDict['FOOD_MANAGER'].pop(index)
        with open(path, 'w') as file:
            json.dump(foodManagerDict, file, indent=4)
        file.close()
        
        foodManagerDict = None
        with open(path2, 'r') as file:
            foodManagerDict = json.load(file)
        file.close()
        foodManagerDict['FOOD_MANAGER'].pop(index)
        with open(path2, 'w') as file:
            json.dump(foodManagerDict, file, indent=4)
        file.close()

def addNewFoodManager(path1='./data/player/onePlayer/food/food.json',
                      path2='./data/player/twoPlayer/food/food.json'):
    for i in range(2):
        path = ""
        if i == 0:
            path = path1
        elif i == 1:
            path = path2
        foodManagerDict = None
        with open(path, 'r') as file:
            foodManagerDict = json.load(file)
        file.close()
        foodManagerDict['FOOD_MANAGER'].append({
            "FOODS" : [
                
            ]
        })
        with open(path, 'w') as file:
            json.dump(foodManagerDict, file, indent=4)
        file.close()

###########  CLASS FOOD  ####################################################################################
class Food:
    ########### Constructor  ################################################################################
    def __init__(self, x, y, indexFrame=0):
        ###########  Create surface   #######################################################################
        self.surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
        self.surfaceRect = self.surface.get_rect()
        self.surfaceRect.topleft = (x, y)
        self.x = x
        self.y = y
        ###########  Default image food  ####################################################################
        self.surface.blit(FOOD[0], (0, 0))
        self.indexFrame = indexFrame
    
    ###########  Get coordinate of food  ####################################################################
    def coordinate(self):
        return [self.x, self.y]
    
    ###########  Update image of food  ######################################################################
    def update(self):
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
    def __init__(self, listFood=[]):
        ###########  Surface and coordinate #################################################################
        self.surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.surfaceRect = self.surface.get_rect()
        self.surfaceRect.topleft = (0, 0)
        ###########  List food anf  number of foods  ########################################################
        self.listFood = listFood
        self.maxFood = SETTING1['FOOD']['MAX_FOOD']
        self.animationSpeed = SETTING1['FOOD']['ANIMATION_SPEED']
    
    ###########  Get coordinate of all foods ################################################################
    def coordinateFoods(self):
        return [food.coordinate() for food in self.listFood]
    
    ###########  Create a random Food  ######################################################################
    def createRandomValidFood(self, coordinateSnakeBlockss=[], coordinateWalls=[]):
        listCoordinateCanChoose = []
        for row in range(NUMBER_ROWS):
            for column in range(NUMBER_COLUMNS):
                if [column*CELL_SIZE, row*CELL_SIZE] not in (coordinateSnakeBlockss + coordinateWalls):
                    listCoordinateCanChoose.append([column*CELL_SIZE, row*CELL_SIZE])
        if len(listCoordinateCanChoose) == 0:
            return None
        coordinate = random.choice(listCoordinateCanChoose)
        return Food(coordinate[0], coordinate[1])
    
    ###########  Update status food man #####################################################################
    def supplementFood(self, coordinateSnakeBlockss, coordinateWalls):
        ###########  Supplement the Food Manager  ###########################################################
        while len(self.listFood) < self.maxFood:
            randomValidFood = self.createRandomValidFood(coordinateSnakeBlockss, coordinateWalls)
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
            
    
    ###########  Remove all foos of Food Manager ############################################################
    def removeAllFoods(self):
        ###########  Remove all foods  ######################################################################
        self.listFood = []
        ###########  Remove old image foods  ################################################################
        self.surface.fill((0, 0, 0, 0))
        ###########  Draw all new image foods  ##############################################################
        for food in self.listFood:
            food.update()
            food.draw(self.surface)
        
    ###########   Update animation of foods   ###############################################################
    def updateAnimation(self):
        ###########   Remove old images   ###################################################################
        self.surface.fill((0, 0, 0, 0))
        ###########   Draw new images   #####################################################################
        for food in self.listFood:
            food.indexFrame = (food.indexFrame + 1) % 4
            food.update()
            food.draw(self.surface)
    
    ###########  Draw all foods on another surface  #########################################################
    def draw(self, parentSurface):
        parentSurface.blit(self.surface, self.surfaceRect) 