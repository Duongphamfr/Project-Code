import pygame
import pyautogui
import random
import json

# initialize the modules
pygame.init()
pygame.font.init()
pygame.mixer.init()

# set the screen system

width, height = pyautogui.size()
window = pygame.display.set_mode((width, height-80))
pygame.display.set_caption("BATAILLE NAVIRE")

bg_img = pygame.image.load("Assets/bg-accueil.jpg")
bg_img = pygame.transform.scale(bg_img, (width, height-80))

# set the color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
COLOR_INACTIVE_BOX = WHITE
COLOR_ACTIVE_BOX = RED

# set the size of grid
SIZE_GRID_SMALL = 7
SIZE_GRID_MEDIUM = 10


# create the textbox class
class Text_box:
    def __init__(self, text, pos, size, color):
        self.pos = pos
        font = pygame.font.Font(None, size)
        self.text = font.render(text, True, color)
    
    def draw(self):
        window.blit(self.text, self.pos)



# create the button class
class Button:
    def __init__(self, text, pos, size):
        self.size = size
        self.text = text
        self.x, self.y = pos
        self.font = pygame.font.SysFont("comicsans", self.size)
        self.change(WHITE, BLACK)
    
    def change(self, color, bg):
        self.bg = bg
        self.new_text = self.font.render(self.text, 1, pygame.Color(color))
        self.size = self.new_text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.new_text, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

    def draw(self):
        window.blit(self.surface, (self.x, self.y))
        self.hover()
    
    def click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    return True
                else:
                    return False

    def hover(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.change(RED, YELLOW)
            return True
        else:
            self.change(WHITE, BLACK)
            return False


# create the input box class
class Input_box:
    def __init__(self, size, pos):
        self.user_text = ""
        self.active = False
        self.color = COLOR_INACTIVE_BOX
        self.x, self.y = pos
        self.rect = pygame.Rect(self.x, self.y, size[0], size[1])
        self.font = pygame.font.Font(None, 60)
        self.text_surface = self.font.render(self.user_text, True, BLACK)
    
    def draw(self):
        pygame.draw.rect(window, self.color, self.rect)
        window.blit(self.text_surface, (self.rect.x+5, self.rect.y+5))
        self.rect.w = max(100, self.text_surface.get_width()+10)

    def handle_event(self, event):
        self.event = event
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.active = True
                else:
                    self.active = False
                self.color = COLOR_ACTIVE_BOX if self.active else COLOR_INACTIVE_BOX
        if (event.type == pygame.KEYDOWN) and (self.active):
            if event.key == pygame.K_BACKSPACE:
                self.user_text = self.user_text[:-1]
            elif (event.key != pygame.K_RETURN) and (len(self.user_text) < 15):
                self.user_text += event.unicode
            self.text_surface = self.font.render(self.user_text, True, BLACK)   


class Ship:
    def __init__(self, size, pos):
        self.draging = False
        self.size_x = size[0]
        self.size_y = size[1]
        self.x, self.y = pos
        self.color = GREEN
    
    def draw(self):
        self.rect = pygame.Rect(self.x, self.y, self.size_x, self.size_y)  
        pygame.draw.rect(window, self.color, self.rect)
    
    def handle_event(self, event):
        # drag and drop
        self.event = event
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(mouse_x, mouse_y):
                if event.button == 1:
                    self.draging = True
                    self.offset_x = self.x - mouse_x
                    self.offset_y = self.y - mouse_y
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.draging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.draging:
                mouse_x, mouse_y = event.pos
                self.x = mouse_x + self.offset_x
                self.y = mouse_y + self.offset_y
        # rotate
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(mouse_x, mouse_y):
                if event.button == 3:
                    a = self.size_x
                    self.size_x = self.size_y
                    self.size_y = a


# button Square

class Square(Ship):
    def __init__(self, size, pos, listShip, dataTarget):
        self.isChangeTurn = False
        self.listShip = listShip
        self.dataTarget = dataTarget
        # self.confirmed = False
        if dataTarget == 0:
            self.isTarget = False
        elif dataTarget == 1:
            self.isTarget = True
        self.hovered = False
        self.chose = False
        self.isAttacked = False
        self.color = BLACK
        self.x, self.y = pos
        self.size = size

        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
    
    def handle_event(self, event):
        self.event = event
        for ship in self.listShip:
            if self.rect.colliderect(ship.rect):
                self.hovered = True
                if (not ship.draging):
                    self.chose = True
                break
            else:
                self.hovered = False
                self.chose = False

        if self.chose:
            self.isTarget = True
            self.color = RED
        elif self.hovered:
            self.isTarget = False
            self.color = YELLOW
        else:
            self.isTarget = False
            self.color = BLACK

    def attacked(self, event):
        if self.isOnAttacked:
            self.event = event
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if self.rect.collidepoint(mouse_x, mouse_y):
                        if not self.isAttacked:
                            if not self.isTarget:
                                self.isChangeTurn = True
                            self.isAttacked = True
        if self.isAttacked:
            if self.isTarget:
                self.color = BLUE
            else:
                self.color = WHITE

    def isKilled(self):
        self.isAttacked = True
        if not self.isTarget:
            self.isChangeTurn = True

    def draw(self):
        pygame.draw.rect(window, self.color, self.rect)

# create the grid

class Grid:
    def __init__(self, size, pos, listShip=[], getData=False):
        self.turnAttacked = False
        self.listShip = listShip
        self.size = size
        self.getData = getData
        if self.getData == False:
            self.dataTarget = []
            for i in range(self.size * self.size):
                self.dataTarget.append(0)
        elif self.getData == "Random":
            self.dataTarget = gridDataRandom()
        elif self.getData == "Player1":
            with open("players_data.json", "r") as f:
                data = f.read()
                data = json.loads(data)
            self.dataTarget = data['grid1']
        elif self.getData == "Player2":
            with open("players_data.json", "r") as f:
                data = f.read()
                data = json.loads(data)
            self.dataTarget = data['grid2']

        self.x, self.y = pos
        self.blockSize = 35
        self.width = self.x + (self.blockSize*size) + (self.size-1)*5
        self.height = self.y + (self.blockSize*size) + (self.size-1)*5

        self.listSquare = []

        vertical = self.y
        i = 0
        self.indexDataTarget = 0
        while vertical < self.height:
            horizontal = self.x
            j = 0
            while horizontal < self.width:
                self.square = Square((self.blockSize, self.blockSize), (horizontal, vertical), self.listShip, self.dataTarget[self.indexDataTarget])
                self.listSquare.append(self.square)
                self.indexDataTarget += 1
                horizontal += (self.blockSize + 5)
                j += 1
            vertical += (self.blockSize + 5)
            i += 1

    def draw(self):
        for i in self.listSquare:
            i.draw()
    
    def handle_event(self, event):
        self.event = event
        for i in self.listSquare:
            i.handle_event(self.event)
    
    def attacked(self, event):
        self.event = event
        for i in self.listSquare:
            i.attacked(self.event)

    def save(self):
        dataGrid = []
        for i in self.listSquare:
            if i.isTarget:
                dataGrid.append(1)
            else:
                dataGrid.append(0)
        return dataGrid

    def onAttacked(self):
        for i in self.listSquare:
            i.isOnAttacked = True

    def offAttacked(self):
        for i in self.listSquare:
            i.isOnAttacked = False

    def randomAttacked(self):
        i = random.choice(self.listSquare)
        while i.isAttacked:
            i = random.choice(self.listSquare)
        i.isKilled()
    
    def countTarget(self):
        self.target = 0
        for i in self.listSquare:
            if i.isTarget:
                self.target += 1
        return self.target
    
    def countTargetAlive(self):
        self.targetAlive = 0
        for i in self.listSquare:
            if (i.isTarget) and (not i.isAttacked):
                self.targetAlive += 1
        return self.targetAlive

    def changeTurn(self):
        self.isChangeTurn = False
        for i in self.listSquare:
            if i.isChangeTurn:
                self.isChangeTurn = True
        return self.isChangeTurn
    
    def resetTurn(self):
        for i in self.listSquare:
            i.isChangeTurn = False

##################################################################################
shipL = 5
shipM = 3
shipS = 1


def gridDataRandom():
    global dataTarget, listTargetChose
    
    dataTarget = []
    listTargetChose = []

    with open("players_data.json", "r") as f:
        data = f.read()
        data = json.loads(data)

    if data['size'] == 'small':
        sizeGrid = 7
    elif data['size'] == 'medium':
        sizeGrid = 10

    for i in range(sizeGrid):
        line = []
        for j in range(sizeGrid):
            line.append(0)
        dataTarget.append(line)
    
    if data['size'] == 'small':
        # 1 shipM and 5 shipS
        shipDataRandom(shipM, 1, sizeGrid)
        shipDataRandom(shipS, 5, sizeGrid)
    if data['size'] == 'medium':
        # 1 shipL and 2 shipM and 5 shipS
        shipDataRandom(shipL, 1, sizeGrid)
        shipDataRandom(shipM, 2, sizeGrid)
        shipDataRandom(shipS, 5, sizeGrid)

    res = []
    for line in dataTarget:
        for data in line:
            res.append(data)

    return res

def shipDataRandom(sizeShip, amount, sizeGrid):
    global dataTarget, listTargetChose


    ship_Added = 0
    while ship_Added < amount:
        yShip = random.randint(0, sizeGrid-1)
        if yShip > (sizeGrid-sizeShip):
            xShip = random.randint(0, sizeGrid-sizeShip)
            horizontal = True
        else:
            horizontal = random.choice([True, False])
            if horizontal:
                xShip = random.randint(0, sizeGrid-sizeShip)
            else:
                xShip = random.randint(0, sizeGrid-1)
            
        if horizontal:
            canAdded = True
            for i in range(xShip, xShip+sizeShip):
                if (yShip, i) in listTargetChose:
                        canAdded = False
            if canAdded:
                for i in range(xShip, xShip+sizeShip):
                    dataTarget[yShip][i] = 1
                    listTargetChose.append((yShip, i))
                ship_Added += 1
        else:
            canAdded = True
            for i in range(yShip, yShip+sizeShip):
                if (i, xShip) in listTargetChose:
                    canAdded = False
            if canAdded:
                for i in range(yShip, yShip+sizeShip):
                    dataTarget[i][xShip] = 1
                    listTargetChose.append((i, xShip))
                ship_Added += 1




##########################################################################
class Game:
    def __init__(self):
        self.turn = 1
        self.bothConnected = False
        self.p1Ready, self.p2Ready = False, False
        self.name1, self.name2, self.size = "", "", ""
        self.grid1, self.grid2 = None, None 
        self.winner = None

    def reset(self):
        self.p1Ready, self.p2Ready = False, False
        self.grid1, self.grid2 = None, None 
        self.winner = None
