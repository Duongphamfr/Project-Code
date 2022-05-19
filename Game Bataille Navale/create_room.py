import sys
import pygame
import index
import json
import add_players
import set_grid
from network import Network

n = network.Network()

# create the button
backButton = index.Button("BACK", (0, 0), 80)
text1 = index.Text_box(f"Your room ID: {n.ip_addr}", (300, 300), 50, index.BLACK)

# hien thi nguoi 2 ket noi hay chua #################

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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if backButton.click(event):
                add_players.main()
        pygame.display.update()

