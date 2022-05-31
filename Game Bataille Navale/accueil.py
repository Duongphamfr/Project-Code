import sys
import pygame
import index
import add_players
import room_setting

button1 = index.Button("Mono-player", (300, 300), 100)
button2 = index.Button("Multi-player 1 PC", (300, 500), 100)
button3 = index.Button("Multi-player 2 PC", (300, 700), 100)

# setting for the infinity loop
clock = pygame.time.Clock()
FPS = 60

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
            if button1.click(event):
                data = {"mode": "mono", "playerId": 'None'}
                with open("players_data.json", "w") as f:
                    f.write(str(data).replace("\'", "\""))
                add_players.main()
            if button2.click(event):
                data = {"mode": "multi1", "playerId": 'None'}
                with open("players_data.json", "w") as f:
                    f.write(str(data).replace("\'", "\""))
                add_players.main()
            if button3.click(event):
                data = {"mode": "multi2", "replay": "False"}
                with open("players_data.json", "w") as f:
                    f.write(str(data).replace("\'", "\""))
                room_setting.main()
        pygame.display.update()


if __name__ == '__main__':
    main()