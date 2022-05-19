import sys
import pygame
import index
import accueil
import choose_size
import json
import create_room
import join_room
import add_players


backButton = index.Button("BACK",(0,0),80)
button1 = index.Button("Create a new Room", (300, 500), 100)
button2 = index.Button("Join a room", (300, 700), 100)

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
            if backButton.click(event):
                accueil.main()
            if button1.click(event):
                data["host"] = "True"
                with open("players_data.json", "w") as f:
                    f.write(str(data).replace("\'", "\""))
                # create_room.main()
                add_players.main()
            if button2.click(event):
                data["host"] = "False"
                with open("players_data.json", "w") as f:
                    f.write(str(data).replace("\'", "\""))
                join_room.main()

        pygame.display.update()
    

