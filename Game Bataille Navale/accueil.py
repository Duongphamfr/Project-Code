import sys
import pygame
import index
import add_players

# create the button
button1 = index.Button("Mono-player", (300, 300), 100)
button2 = index.Button("Multi-player", (300, 500), 100)

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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if button1.click(event):
                data = {"mode": "mono"}
                with open("players_data.json", "w") as f:
                    f.write(str(data).replace("\'", "\""))
                add_players.main()
            if button2.click(event):
                data = {"mode": "multi"}
                with open("players_data.json", "w") as f:
                    f.write(str(data).replace("\'", "\""))
                add_players.main()
        pygame.display.update()


if __name__ == '__main__':
    main()