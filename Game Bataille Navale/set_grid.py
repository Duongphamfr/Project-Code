import sys
import pygame
from win32api import GetSystemMetrics
import random

# set the color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
COLOR_INACTIVE_BOX = WHITE
COLOR_ACTIVE_BOX = RED

# initialize the modules
pygame.init()
pygame.font.init()
pygame.mixer.init()

# set the screen system
width, height = GetSystemMetrics(0), GetSystemMetrics(1)
window = pygame.display.set_mode((width, height-80))
pygame.display.set_caption("BATAILLE NAVIRE")

bg_img = pygame.image.load("Assets/bg-accueil.jpg")
bg_img = pygame.transform.scale(bg_img, (width, height-80))



class Ship:
    def __init__(self, size, pos):
        self.draging = False
        self.size = size
        Ship.x, Ship.y = pos
        self.color = GREEN
        # self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])  
    
    def draw(self):
        Ship.rect = pygame.Rect(Ship.x, Ship.y, self.size[0], self.size[1])  
        pygame.draw.rect(window, self.color, Ship.rect)
    
    def drag_drop(self, event):
        self.event = event
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if Ship.rect.collidepoint(mouse_x, mouse_y):
                if event.button == 1:
                    self.draging = True
                    self.offset_x = Ship.x - mouse_x
                    self.offset_y = Ship.y - mouse_y
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.draging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.draging:
                mouse_x, mouse_y = event.pos
                Ship.x = mouse_x + self.offset_x
                Ship.y = mouse_y + self.offset_y


# button Square

class Square(Ship):
    def __init__(self, size, pos, target):
        self.target = target
        self.hovered = False
        self.clicked = False
        self.color = BLACK
        self.x, self.y = pos
        self.size = size

        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])  
    
    def handle_event(self, event):
        self.event = event
        # x, y = pygame.mouse.get_pos()
        if self.rect.colliderect(Ship.rect):
            self.hovered = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    self.clicked = True
        else:
            self.hovered = False
        if self.clicked:
            if self.target:
                self.color = RED
            else:
                self.color = WHITE
        elif self.hovered:
            self.color = YELLOW
        else:
            self.color = BLACK

    def draw(self):
        pygame.draw.rect(window, self.color, self.rect)

# create a list for grid

def listGrid(size, prop):
    grid = []
    for i in range(size):
        line = []
        for j in range(size):
            if random.random() < prop:
                k = 1
            else:
                k = 0
            line.append(k)
        grid.append(line)
    return grid

# create the grid

class Grid:
    def __init__(self, size, pos):
        self.size = size
        self.x, self.y = pos
        self.blockSize = 35
        self.width = self.x + (self.blockSize*size)
        self.height = self.y + (self.blockSize*size)

        self.grid = listGrid(self.size, 0.5)


        self.list = []

        vertical = self.y
        i = 0
        while vertical < self.height:
            horizontal = self.x
            j = 0
            while horizontal < self.width:
                if self.grid[i][j] == 1:
                    self.target = True
                else:
                    self.target = False
                self.square = Square((self.blockSize, self.blockSize), (horizontal, vertical), self.target)
                self.list.append(self.square)
                horizontal += (self.blockSize + 2)
                j += 1
            vertical += (self.blockSize + 12)
            i += 1

    def draw(self):
        for i in self.list:
            i.draw()
    
    def handle_event(self, event):
        self.event = event
        for i in self.list:
            i.handle_event(self.event)









ship1 = Ship((30, 120), (1500, 300))








                
grid1 = Grid(15, (200, 250))



# setting for the infinity loop
clock = pygame.time.Clock()
FPS = 60

# create the main function
def main():
    running = True
    while running:
        clock.tick(FPS)
        window.blit(bg_img, (0, 0))
        grid1.draw()
        ship1.draw()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            grid1.handle_event(event)
            ship1.drag_drop(event)

main()

