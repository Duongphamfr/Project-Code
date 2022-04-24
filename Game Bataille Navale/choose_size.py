import sys
import pygame
import index
import json
import set_grid_medium



# create the button
backButton = index.Button("BACK", (0, 0), 80)
button1 = index.Button("Small Grid", (350, 300), 100)
button2 = index.Button("Medium Grid", (350, 450), 100)

# setting for the infinity loop
clock = pygame.time.Clock()
FPS = 60

#menu game
def main():
    with open("players_data.json", "r") as f:
        data = f.read()
        data = json.loads(data)

    running = True
    while running:
        clock.tick(FPS)
        index.window.blit(index.bg_img, (0, 0))
        backButton.draw()
        button1.draw()
        button2.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            """if button1.hover():
                # mo ta game
            if button2.hover():
                # mo ta game"""
            if backButton.click(event):
                accueil.main()
            """if button1.click(event):
                data["size"] = "small"
                with open("players_data.txt", "w") as f:
                    f.write(str(data))
                if data["mode"] == "mono":
                    # set_grid_small_1_player.main()
                elif data['mode'] == "multi":
                    # set_grid_small_2_players.main()"""
            if button2.click(event):
                data["size"] = "medium"
                with open("players_data.json", "w") as f:
                    f.write(str(data).replace("\'", "\""))
                if data['mode'] == "mono":
                    set_grid_medium.main()
                elif data['mode'] == "multi":
                    set_grid_medium.main()
        pygame.display.update()


if __name__ == '__main__':
    main()