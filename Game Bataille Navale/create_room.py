import sys
import pygame
import index
import json
import add_players
import set_grid
import network




# setting for the infinity loop
clock = pygame.time.Clock()
FPS = 60

#menu game
def main():
    n = network.Network()  # ket noi server

    # create the button
    backButton = index.Button("BACK", (0, 0), 80)
    text1 = index.Text_box(f"Your room ID: {n.ip_addr}", (300, 300), 50, index.BLACK)

    # hien thi nguoi 2 ket noi hay chua #################
    text2 = index.Text_box("Waiting for player 2...", (300, 500), 50, index.BLACK)


    with open("players_data.json", "r") as f:
        data = f.read()
        data = json.loads(data)

    running = True
    while running:
        try:
            # game = n.send("get")
            # n = network.Network()
            game = n.send("get")
            game.name1 = data["name1"]
            game.size = data["size"]
        except Exception as e:
            print(e)
            running = False
            print("Couldn't get game")
            break

        clock.tick(FPS)
        index.window.blit(index.bg_img, (0, 0))
        backButton.draw()
        text1.draw()
        if not game.bothConnected:
            text2.draw()
        else:
            set_grid.main()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if backButton.click(event):
                add_players.main()
        pygame.display.update()

