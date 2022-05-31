import sys
import pygame
import index
import add_players
import room_setting

# create the button
button1 = index.Button('Singleplayer',(300,300),100)               
button2 = index.Button('Multiplayer', (300, 500), 100)  
button3 = index.Button("Multi-player 2 PC", (300, 700), 100)
# setting for the infinity loop
clock = pygame.time.Clock()
FPS = 60

#menu game
def main():
    running = True
    while running:
        clock.tick(FPS)
        index.window.blit(index.bg_img, (0, 0))
        button1.draw()
        button2.draw()
        button3.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if button1.click():         
            data = {"mode": "mono", "playerId": 'None'}
            with open("players_data.json", "w") as f:
                f.write(str(data).replace("\'", "\""))
            add_players.main()
        if button2.click():         
            data = {"mode": "multi", "playerId": 'None'}
            with open("players_data.json", "w") as f:
                f.write(str(data).replace("\'", "\""))
            add_players.main()
        if button3.click():
            data = {"mode": "multi2", "replay": "False"}

            with open("players_data.json", "w") as f:
                f.write(str(data).replace("\'", "\""))
            room_setting.main()
        pygame.display.update()


if __name__ == '__main__':
    main()