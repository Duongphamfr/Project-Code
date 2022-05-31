import sys
import pygame
import index
import json
import add_players
import network
import set_grid


backButton = index.Button("BACK",(0,0),80)
textGuide = index.Text_box("Insert Room ID and press ENTER to join", (100, 600), 50, index.BLACK)
input1 = index.Input_box((600,100),(650,300))
text1 = index.Text_box("Room ID", (650, 250), 80, index.BLACK)

# setting for the infinity loop
clock = pygame.time.Clock()
FPS = 60

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
            input1.draw()
            text1.draw()
            textGuide.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if backButton.click(event):
                    add_players.main()
                input1.handle_event(event)
                if len(input1.user_text) != 0:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            data["roomID"] = input1.user_text
                            global n
                            n = network.Network(input1.user_text) # create a connection to server
                            try:
                                game = n.send(data["name2"])
                                data['name1'] = game.name1
                                data['size'] = game.size
                            except:
                                running = False
                                print("Couldn't get game")
                                break

                            with open("players_data.json", "w") as f:
                                f.write(str(data).replace("\'", "\""))
                            if game.bothConnected:
                                set_grid.main()
            pygame.display.update()