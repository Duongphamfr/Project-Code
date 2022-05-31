import sys
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

wood_img = pygame.image.load("assets/wood_background.jpg")
wood_img = pygame.transform.scale(wood_img, (850,200))

rock_img = pygame.image.load("assets/rock.png")
rock_img = pygame.transform.scale(rock_img, (180, 180))     #load the image of rock
paper_img = pygame.image.load("assets/paper.png")
paper_img = pygame.transform.scale(paper_img, (180, 180))   #load the image of paper
scissors_img = pygame.image.load("assets/scissors.png")
scissors_img = pygame.transform.scale(scissors_img, (180, 180))     #load the image of scissors

hollow_sound  = pygame.mixer.Sound("Assets/hollow.wav")
click_sound = pygame.mixer.Sound("Assets/clicked.wav")

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
        font = pygame.font.SysFont('Helvatica', size)
        self.text = font.render(text, True, color)
    
    def draw(self):
        window.blit(self.text, self.pos)



# create the button class
class Button:
    def __init__(self,text,pos,size):
        self.pressed = False
        self.hollowed = False
        self.elevation = 5
        self.dynamic_elecation = 5
        self.original_y_pos  = pos[1]
        self.font = pygame.font.SysFont('Helvatica', size)
        #text
        self.text = self.font.render(text, True, '#ffffff')
        
        #top rectangle
        self.top_rect = pygame.Rect(pos, (self.text.get_size()[0], self.text.get_size()[1] + 10))
        self.top_color = '#00008b'
        self.text_rect = self.text.get_rect(center = self.top_rect.center)
        
        #bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (self.text.get_size()[0],self.text.get_size()[1] + 10))
        self.bottom_color = '#98926A'
        
    def draw(self):
        #elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center
        
        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation
        
        pygame.draw.rect(window, self.bottom_color, self.bottom_rect, border_radius = 12)
        pygame.draw.rect(window, self.top_color, self.top_rect, border_radius = 12)
        window.blit(self.text, self.text_rect)
        self.hover()
    
    def click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            elif pygame.MOUSEBUTTONUP:
                if self.pressed == True:
                    pygame.mixer.Sound.play(click_sound)
                    self.pressed = False
                    return True
        
    def hover(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#000080'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0 
            else:
                self.dynamic_elecation = self.elevation
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = '#00008b' 
            

# create the input box class
class Input_box:
    def __init__(self, size, pos):
        self.user_text = ""
        self.active = False
        self.color = '#0014a8'
        self.x, self.y = pos
        self.rect = pygame.Rect(self.x, self.y, size[0], size[1])
        self.font = pygame.font.SysFont('Helvatica', 60)
        self.text_surface = self.font.render(self.user_text, True, BLACK)
    
    def draw(self):
        pygame.draw.rect(window, self.color, self.rect, border_radius = 10)         ###########################
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
                self.color = '#483d8b' if self.active else '#0014a8'
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
        elif isinstance(self.getData, list):
            self.dataTarget = self.getData

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

    def dataAttacked(self):
        dataAttacked = []
        for i in self.listSquare:
            if i.isAttacked:
                dataAttacked.append(1)
            else:
                dataAttacked.append(0)
        return dataAttacked
    
    def updateSquare(self, list):
        k = 0
        for i in self.listSquare:
            if list[k] == 1:
                i.isAttacked = True
                if i.isTarget:
                    i.color = BLUE
                else:
                    i.color = WHITE
            k += 1

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

shipL = 5
shipM = 3
shipS = 1

# create by random the grid of computer
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

# random the position of the ship on the grid (used in mode "mono" to set the computer's grid)
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

# class Game to handle data in mode MULTI2
class Game:
    def __init__(self):
        self.turn = 1
        self.bothConnected = False
        self.p1Ready, self.p2Ready = False, False
        self.toggleGrid = False
        self.p1PushGrid = False
        self.p2PushGrid = False
        self.updateGrid1, self.updateGrid2 = [], []
        self.winner = None
        self.reseted = False
    
    def setName(self, playerId, name):
        if playerId == 1:
            self.name1 = name
        elif playerId == 2:
            self.name2 = name
    
    def setSize(self, size):
        self.size = size
        if size == 'small':
            self.sizeGrid = 7
        elif size == 'medium':
            self.sizeGrid = 10
        for i in range(self.sizeGrid*self.sizeGrid):
            self.updateGrid1.append(0)
            self.updateGrid2.append(0)

    
    def setGrid(self, playerId, list):
        with open("players_data.json", "r") as f:
            data = f.read()
            data = json.loads(data)

        if data['size'] == 'small':
            gridSize = 7
        elif data['size'] == 'medium':
            gridSize = 10

        if playerId == 1:
            self.grid1 = Grid(gridSize, (200, 300), getData=list)
        elif playerId == 2:
            self.grid2 = Grid(gridSize, (1200, 300), getData=list)    
    
    def setReady(self, playerId):
        if playerId == 1:
            self.p1Ready = True
        else:
            self.p2Ready = True
    
    def setPushGrid(self, playerId):
        if playerId == 1:
            self.p1PushGrid = True
        else:
            self.p2PushGrid = True
    
    def setTurn(self, playerId):
        self.turn = playerId
    
    def setWinner(self, winner):
        if winner == 1:
            self.winner = self.name1
        else:
            self.winner = self.name2
        self.reseted = False
    
    def reset(self):
        if not self.reseted:
            self.p1Ready, self.p2Ready = False, False
            self.grid1, self.grid2 = None, None 
            self.winner = None
            self.turn = 1
            self.toggleGrid = False
            self.p1PushGrid = False
            self.p2PushGrid = False
            for i in self.updateGrid1:
                self.updateGrid1[i] = 0
                self.updateGrid2[i] = 0
            self.reseted = True
            
#create a button with image
class button_img():
    def __init__(self, img, pos):
        self.img = img 
        self.x , self.y = pos
        self.size= self.img.get_size()
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
        self.surface = pygame.Surface(self.size)
        self.hover_size = (self.size[0] + 5, self.size[1] + 5)
        self.clicked = False
        
    def change(self,new_size):
        self.new_size = new_size
        self.new_img = pygame.transform.scale(self.img, (self.new_size))

    def draw(self):
        self.hover()
        if not self.clicked:
            window.blit(self.new_img,(self.x, self.y))

    def click(self, event):  
        x,y = pygame.mouse.get_pos()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x,y):
                    return True
                else:
                    return False
                
    def hover(self):
        x, y = pygame.mouse.get_pos()
        if self.rect.collidepoint(x, y):
            self.change(self.hover_size)
        else:
            self.change(self.size)

#create rock, scissors, paper game to determine the player that will play frist
class chifoumi_game():
    def __init__(self):
        #define button
        self.rock_img_1 =button_img(rock_img, (650, 550))
        self.paper_img_1 = button_img(paper_img, (850, 550))
        self.scissors_img_1 = button_img(scissors_img, (1050, 550))
        
        self.list_choice = ["R","P","S"]
        self.choice_player = "null"
        self.choice_player_1 = "null"
        self.choice_player_2 = "null"
        self.choice = "null"
        self.winner = 3
        self.choice_COM = self.list_choice[random.randint(0,2)]
        
        self.font = pygame.font.SysFont('Helvatica',80)
        self.text = ""
                 
    def draw(self):
        self.rock_img_1.draw()
        self.paper_img_1.draw()
        self.scissors_img_1.draw()

    def choose(self,event): 
        if self.rock_img_1.click(event):
            self.choice = "R"
            self.rock_img_1.clicked = True
            self.paper_img_1.clicked = False
            self.scissors_img_1.clicked = False
        elif self.paper_img_1.click(event):
            self.choice = "P"
            self.rock_img_1.clicked = False
            self.paper_img_1.clicked = True
            self.scissors_img_1.clicked = False
        elif self.scissors_img_1.click(event):
            self.choice  = "S"
            self.rock_img_1.clicked = False
            self.paper_img_1.clicked = False
            self.scissors_img_1.clicked = True
            
    def play_COM(self):
        self.choice_player = self.choice
    
    def play_1(self):
        self.choice_player_1 = self.choice
    
    def play_2(self):
        self.choice_player_2 = self.choice
    
    def print_result_COM(self):     
        with open("players_data.json","r") as f:
            data = f.read()
            data = json.loads(data)
            
        if self.winner == 1:  
            self.text = "PLAYER play first"
            data["chifoumi"] = data["name1"]
        elif self.winner == 2: 
            self.text = "COMPUTER play first " 
            data["chifoumi"] = "Computer"  
        elif self.winner == 0:
            self.choice_COM = self.list_choice[random.randint(0,2)]
        
        with open("players_data.json","w") as f:
            f.write(str(data).replace("\'","\""))
        
        self.text_result = self.font.render(self.text, True, BLACK)
        window.blit(self.text_result, (870,100))
    
    def print_result_player(self):    
        with open("players_data.json","r") as f:
            data = f.read()
            data = json.loads(data)
            
        if self.winner == 1:
            self.text = "PLAYER 1 play first"
            data["chifoumi"] = data["name1"]
        elif self.winner == 2:
            self.text = "PLAYER 2 play first "
            data["chifoumi"] = data["name2"]
        elif self.winner == 0:  #if draw, random the result of the chifoumi game
            self.choice_player_1 = self.list_choice[random.randint(0,2)]
            self.choice_player_2 = self.list_choice[random.randint(0,2)] 

        with open("players_data.json","w") as f:
            f.write(str(data).replace("\'","\""))
            
        self.text_result = self.font.render(self.text, True, BLACK)
        window.blit(self.text_result, (870,100))
    
    def chifoumi(self, player_1, player_2):
        if (player_1 == "R" and player_2 == "P") or (player_1 == "P" and player_2 == "S") or (player_1 == "S" and player_2 == "R"):
            self.winner = 2
        if (player_1 == "P" and player_2 == "R") or (player_1 == "S" and player_2 == "P") or (player_1 == "R" and player_2 == "S"):
            self.winner = 1
        if player_1 == player_2:
            self.winner = 0
    
    def reset_choice(self):
        self.choice = "null"
        self.rock_img_1.clicked = False
        self.paper_img_1.clicked = False
        self.scissors_img_1.clicked = False