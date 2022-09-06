import pygame
from setting import *
import setting



WIDTH = SETTING2['SCREEN']['WIDTH']
HEIGHT = SETTING2['SCREEN']['HEIGHT']
NUMBER_ROWS = SETTING2['SCREEN']['NUMBER_ROWS']
NUMBER_COLUMNS = SETTING2['SCREEN']['NUMBER_COLUMNS']
CELL_SIZE = SETTING2['SCREEN']['CELL_SIZE']
SNAKE = SETTING2['SNAKE']
MOVE_SPEED = SETTING1['SNAKE']['MOVE_SPEED']
DROP_SPEED = SETTING1['SNAKE']['DROP_SPEED']
ANIMATION_SPEED = SETTING1['SNAKE']['ANIMATION_SPEED']


###########  CLASS SNAKE BLOCK  #############################################################################
class SnakeBlock:
    ###########   Constructor   #############################################################################
    def __init__(self, image, x=NUMBER_COLUMNS//2 * CELL_SIZE, y=NUMBER_ROWS//2 * CELL_SIZE, 
                 direction='UU', indexFrame=0):
        self.surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
        self.surfaceRect = self.surface.get_rect()
        self.surfaceRect.topleft = (x, y)
        self.surface.blit(image, (0, 0))
        self.x = x
        self.y = y
        self.direction = direction
        self.indexFrame = indexFrame
    
    ###########   Get coordinate of Snake Block with type List  #############################################
    def coordinate(self):
        return [self.x, self.y]
    
    ###########   Set up new coordinate for Snake Block   ###################################################
    def setCoordinate(self, x, y):
        self.x = x
        self.y = y
        self.surfaceRect.topleft = (x, y)
    
    ###########   Update new image for Snake Block   ########################################################
    def update(self, part):
        ###### Clear old image ##############################################################################
        self.surface.fill((0, 0, 0, 0))
        ###### Add new image ################################################################################
        img = SNAKE[part][self.direction][self.indexFrame]
        self.surface.blit(img, (0, 0))

    ###########   Draw SnakeBlock in another surface   ######################################################
    def draw(self, parentSurface):
        parentSurface.blit(self.surface, self.surfaceRect)
      
      
        
###########  CLASS SNAKE  ###################################################################################
class Snake:
    ###########   Constructor   #############################################################################
    def __init__(self, speed=MOVE_SPEED, currentDirection='UU', previousDirection='UU', score=0):
        ###########   Surface and coordinate   ##############################################################
        self.surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.surfaceRect = self.surface.get_rect()
        self.surfaceRect.topleft = (0, 0)
        
        ###########   Create first head, body anf tail for Snake   ##########################################
        self.head = [SnakeBlock(SNAKE['HEAD']['UU'][0], indexFrame=0)]
        self.body = [SnakeBlock(SNAKE['BODY']['UU'][0], NUMBER_COLUMNS//2*CELL_SIZE, 
                                NUMBER_ROWS//2*CELL_SIZE + CELL_SIZE, indexFrame=1)]
        self.tail = [SnakeBlock(SNAKE['TAIL']['UU'][0], NUMBER_COLUMNS//2*CELL_SIZE, 
                                NUMBER_ROWS//2*CELL_SIZE + 2*CELL_SIZE, indexFrame=2)]
        self.head[0].draw(self.surface)
        self.body[0].draw(self.surface)
        self.tail[0].draw(self.surface)
        
        ###########   Speed, Direction of Snake #############################################################
        self.moveSpeed = speed
        self.dropSpeed = DROP_SPEED
        self.animationSpeed = ANIMATION_SPEED
        self.currentDirection = currentDirection
        self.previousDirection = previousDirection
        self.score = score

    ###########  Get all coordinate of Snake Blocks #########################################################
    def coordinateSnakeBlocks(self):
        return [snakeBlock.coordinate() for snakeBlock in (self.head + self.body + self.tail)]
    
    ###########   Check if snake can move or not with next direction   ######################################
    def checkSnakeCanMove(self, aDirection):
        if aDirection == 'UU' and (self.head[0].y - CELL_SIZE) == self.body[0].y:
            return False
        elif aDirection == 'DD' and (self.head[0].y + CELL_SIZE) == self.body[0].y:
            return False
        elif aDirection == 'RR' and (self.head[0].x + CELL_SIZE) == self.body[0].x:
            return False
        elif aDirection == 'LL' and (self.head[0].x - CELL_SIZE) == self.body[0].x:
            return False
        return True
    
    ###########   Check if snake is eating food   ##########################################################
    def eatingFood(self, foodList):
        for food in foodList:
            if self.head[0].coordinate() == food.coordinate():
                foodList.remove(food)
                self.score += self.moveSpeed
                return True
        return False
    
    ##   Update Coordinate and Direction of head, body and tail when snake move with current direction   ####
    def onlyMove(self):
        if self.currentDirection == None:
            return
        
        ########  Correct direction for head, body and tail  ################################################
        self.head[0].direction = self.head[0].direction[1] + self.currentDirection[0]
        self.tail[0].direction = self.body[len(self.body) - 1].direction
        for index in range(len(self.body) - 1, 0, -1):
            self.body[index].direction = self.body[index-1].direction
        self.body[0].direction = self.head[0].direction
        
        #######  Update new image for head, body and tail  ##################################################
        self.head[0].update('HEAD')
        for snakeBlock in self.body:
            snakeBlock.update('BODY')
        self.tail[0].update('TAIL')
        
        ########  New Coordinate of snakeBlocks  ############################################################
        self.tail[0].setCoordinate(self.body[len(self.body)-1].x, self.body[len(self.body)-1].y)
        for index in range(len(self.body) - 1, 0, -1):
            self.body[index].setCoordinate(self.body[index-1].x, self.body[index-1].y)
        self.body[0].setCoordinate(self.head[0].x, self.head[0].y)
        if self.currentDirection == 'UU':
            self.head[0].setCoordinate(self.head[0].x, (self.head[0].y - CELL_SIZE) % HEIGHT)
        elif self.currentDirection == 'DD':
            self.head[0].setCoordinate(self.head[0].x, (self.head[0].y + CELL_SIZE) % HEIGHT)
        elif self.currentDirection == 'RR':
            self.head[0].setCoordinate((self.head[0].x + CELL_SIZE) % WIDTH, self.head[0].y)
        elif self.currentDirection == 'LL':
            self.head[0].setCoordinate((self.head[0].x - CELL_SIZE) % WIDTH, self.head[0].y)
            
    def moveAndGrowUp(self):
        if self.currentDirection == None:
            return
        
        ########  Correct direction for head, body and tail  ################################################
        self.head[0].direction = self.head[0].direction[1] + self.currentDirection[0]
        newSnakeBlockDirection = self.head[0].direction
        
        ########  New Coordinate of snakeBlocks  ############################################################
        newSnakeBlockCoordinate = [self.head[0].x, self.head[0].y]
        if self.currentDirection == 'UU':
            self.head[0].setCoordinate(self.head[0].x, (self.head[0].y - CELL_SIZE) % HEIGHT)
        elif self.currentDirection == 'DD':
            self.head[0].setCoordinate(self.head[0].x, (self.head[0].y + CELL_SIZE) % HEIGHT)
        elif self.currentDirection == 'RR':
            self.head[0].setCoordinate((self.head[0].x + CELL_SIZE) % WIDTH, self.head[0].y)
        elif self.currentDirection == 'LL':
            self.head[0].setCoordinate((self.head[0].x - CELL_SIZE) % WIDTH, self.head[0].y)
        
        #######  Update new image for head, body and tail  ##################################################
        newSnakeBlockIndexFrame = self.head[0].indexFrame
        self.head[0].indexFrame = (self.head[0].indexFrame -1) % 7
        self.head[0].update('HEAD')
        newSnakeBlock = SnakeBlock(SNAKE['BODY'][newSnakeBlockDirection][newSnakeBlockIndexFrame], x=newSnakeBlockCoordinate[0],
                                   y=newSnakeBlockCoordinate[1], direction=newSnakeBlockDirection, 
                                   indexFrame=self.head[0].indexFrame)
        self.body.insert(0, newSnakeBlock)
    
    
    def died(self):
        return self.head[0].coordinate() in [snakeBlock.coordinate() for snakeBlock in (self.body + self.tail)]
    
        
    ###########   Update snake displacement  ################################################################
    def updateLocation(self, foodList):
        if self.eatingFood(foodList):
            self.moveAndGrowUp()
        else:
            self.onlyMove()
        
        self.surface.fill((0, 0, 0, 0))
        self.tail[0].draw(self.surface)
        for index in range(len(self.body) - 1, -1, -1):
            self.body[index].draw(self.surface)
        self.head[0].draw(self.surface)
        
    
    def updateAnimation(self):
        self.head[0].indexFrame = (self.head[0].indexFrame - 1) % 7
        self.head[0].update('HEAD')
        for snakeBlock in self.body :
            snakeBlock.indexFrame = (snakeBlock.indexFrame - 1) % 7
            snakeBlock.update('BODY')
        self.tail[0].indexFrame = (self.tail[0].indexFrame - 1) % 7
        self.tail[0].update('TAIL')
        
        self.surface.fill((0, 0, 0, 0))
        self.tail[0].draw(self.surface)
        for index in range(len(self.body) - 1, -1, -1):
            self.body[index].draw(self.surface)
        self.head[0].draw(self.surface)
    
    def drop(self):
        for snakeBlock in (self.head + self.body + self.tail):
            if [snakeBlock.x, snakeBlock.y + CELL_SIZE] not in self.coordinateSnakeBlocks():
                if snakeBlock.y + CELL_SIZE < HEIGHT:
                    snakeBlock.setCoordinate(snakeBlock.x, snakeBlock.y + CELL_SIZE)
            else:
                if snakeBlock.x < WIDTH//2:
                    if [snakeBlock.x + CELL_SIZE, snakeBlock.y + CELL_SIZE] not in self.coordinateSnakeBlocks():
                        if snakeBlock.y + CELL_SIZE < HEIGHT:
                            snakeBlock.setCoordinate(snakeBlock.x + CELL_SIZE, snakeBlock.y + CELL_SIZE)
                    elif [snakeBlock.x - CELL_SIZE, snakeBlock.y + CELL_SIZE] not in self.coordinateSnakeBlocks():
                        if snakeBlock.y + CELL_SIZE < HEIGHT and snakeBlock.x - CELL_SIZE >= 0:
                            snakeBlock.setCoordinate(snakeBlock.x - CELL_SIZE, snakeBlock.y + CELL_SIZE)
                else:
                    if [snakeBlock.x - CELL_SIZE, snakeBlock.y + CELL_SIZE] not in self.coordinateSnakeBlocks():
                        if snakeBlock.y + CELL_SIZE < HEIGHT and snakeBlock.x - CELL_SIZE >= 0:
                            snakeBlock.setCoordinate(snakeBlock.x - CELL_SIZE, snakeBlock.y + CELL_SIZE)
                    elif [snakeBlock.x + CELL_SIZE, snakeBlock.y + CELL_SIZE] not in self.coordinateSnakeBlocks():
                        if snakeBlock.y + CELL_SIZE < HEIGHT:
                            snakeBlock.setCoordinate(snakeBlock.x + CELL_SIZE, snakeBlock.y + CELL_SIZE)
                    
        
        self.surface.fill((0, 0, 0, 0))
        self.tail[0].draw(self.surface)
        for index in range(len(self.body) - 1, -1, -1):
            self.body[index].draw(self.surface)
        self.head[0].draw(self.surface)
    
    ###########   Draw snake on another surface   ###########################################################
    def draw(self, parentSurface):
        parentSurface.blit(self.surface, self.surfaceRect)