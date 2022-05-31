import imp
import sys
import pygame
import index
import accueil
import json
import add_players


backButton = index.Button("BACK",(0,0),80)
button1 = index.Button("Create a new Room", (300, 500), 100)
button2 = index.Button("Join a room", (300, 700), 100)

# setting for the infinity loop
clock = pygame.time.Clock()
FPS = 60

# menu game
def main():
    # get data stocked in a json file
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
            if backButton.click():
                accueil.main()
            if button1.click():
                data["playerId"] = '1'
                with open("players_data.json", "w") as f:
                    f.write(str(data).replace("\'", "\""))
                add_players.main()
            if button2.click():
                data["playerId"] = '2'
                with open("players_data.json", "w") as f:
                    f.write(str(data).replace("\'", "\""))
                add_players.main()

        pygame.display.update()
    
