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
    global n
    n = network.Network()  # ket noi server

    # create the button
    backButton = index.Button("BACK", (0, 0), 80)
    text1 = index.Text_box(f"Your room ID: {n.ip_addr}", (300, 300), 50, index.BLACK)

    # hien thi nguoi 2 ket noi hay chua #################
    text2 = index.Text_box("Waiting for player 2...", (300, 500), 50, index.BLACK)


    with open("players_data.json", "r") as f:
        data = f.read()
        data = json.loads(data)
    
    game = n.send(data["size"])
    game = n.send(data["name1"])
    # print(game.name1)


    running = True
    while running:
        game = n.send("update")

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

