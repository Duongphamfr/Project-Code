import sys
import pygame
import index
import accueil
import choose_size
import json

# setting for the infinity loop
clock = pygame.time.Clock()
FPS = 60

button1 = index.Button('MENU', (650, 300), 50)
button2 = index.Button('REPLAY', (650, 500), 50)
button3 = index.Button('QUIT',( 650, 700), 50)


def main():
    with open("players_data.json", "r") as f:
        data = f.read()
        data = json.loads(data)
    
    winner = index.Text_box('The winner is ' + str(data['winner']), (300, 100), 50, index.BLACK)


    running = True
    while running:
        clock.tick(FPS)
        index.window.blit(index.bg_img, (0, 0))
        button1.draw()
        button2.draw()
        button3.draw()
        winner.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or button3.click(event):
                pygame.quit()
                sys.exit()
            if button1.click(event):
                accueil.main()
            if button2.click(event):
                if data['mode'] == 'mono':
                    data.pop('winner')
                    data.pop('grid1')
                    data.pop('size')
                if data['mode'] == 'multi':
                    data.pop('winner')
                    data.pop('grid1')
                    data.pop('grid2')
                    data.pop('size')
                with open("players_data.json", "w") as f:
                    f.write(str(data).replace("\'", "\""))
                choose_size.main()
                    
        pygame.display.update()
