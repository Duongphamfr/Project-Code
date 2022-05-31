import sys
import pygame
import index
import battle
import json
import choose_size
from importlib import reload
import create_room
import join_room
import result

backButton = index.Button("BACK",(0,0),80)

# setting for the infinity loop
clock = pygame.time.Clock()
FPS = 60

def main():
    import data_map
    reload(data_map)

    listShip = data_map.listShip
    grid = index.Grid(data_map.gridSize, (200, 350), listShip)


    with open("players_data.json", "r") as f:
        data = f.read()
        data = json.loads(data)

    if data['mode'] == 'mono':
        button1 = index.Button("Confirm grid", (100, 150), 30)
        button3 = index.Button("WAR", (100, 700), 30)

        running = True

        while running:
            # get the number of target
            target = grid.countTarget()

            clock.tick(FPS)
            index.window.blit(index.bg_img, (0, 0))
            backButton.draw()
            grid.draw()
            if ('grid1' not in data):
                button1.draw()
            if ('grid1' in data):
                button3.draw()
            for ship in listShip:
                ship.draw()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                grid.handle_event(event)
                if backButton.click(event):
                    choose_size.main()
                for ship in listShip:
                    ship.handle_event(event)
                if ('grid1' not in data) and (target == data_map.totalTarget):
                    if button1.click(event):
                        data['grid1'] = grid.save()
                        with open("players_data.json", "w") as f:
                            f.write(str(data).replace("\'", "\""))
                        grid.__init__(data_map.gridSize, (200, 350), listShip)
                        data_map.reset_listShip()
                        print("Saved Player 1")
                if ('grid1' in data):
                    if button3.click(event):
                        battle.main()

    elif data['mode'] == 'multi1':
        button1 = index.Button("Confirm grid of player 1", (100, 150), 30)
        button2 = index.Button("Confirm grid of player 2", (500, 150), 30)
        button3 = index.Button("WAR", (100, 700), 30)

        running = True

        while running:
            # get the number of target
            target = grid.countTarget()

            clock.tick(FPS)
            index.window.blit(index.bg_img, (0, 0))
            backButton.draw()
            grid.draw()
            if ('grid1' not in data):
                button1.draw()
            if ('grid2' not in data):
                button2.draw()
            if ('grid1' in data) and ('grid2' in data):
                button3.draw()
            for ship in listShip:
                ship.draw()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                grid.handle_event(event)
                if backButton.click(event):
                    choose_size.main()
                for ship in listShip:
                    ship.handle_event(event)
                if ('grid1' not in data) and (target == data_map.totalTarget):
                    if button1.click(event):
                        data['grid1'] = grid.save()
                        with open("players_data.json", "w") as f:
                            f.write(str(data).replace("\'", "\""))
                        grid.__init__(data_map.gridSize, (200, 350), listShip)
                        data_map.reset_listShip()
                if ('grid2' not in data) and (target == data_map.totalTarget):
                    if button2.click(event):
                        data['grid2'] = grid.save()
                        with open("players_data.json", "w") as f:
                            f.write(str(data).replace("\'", "\""))
                        grid.__init__(data_map.gridSize, (200, 350), listShip)
                        data_map.reset_listShip()
                if ('grid1' in data) and ('grid2' in data):
                    if button3.click(event):
                        battle.main()

    if data['mode'] == 'multi2':
        global n
        if data['playerId'] == '1' and data["replay"] == "False":
            n = create_room.n
        elif data['playerId'] == '2' and data["replay"] == "False":
            n = join_room.n
        else:
            n = result.n

        button1 = index.Button("Confirm grid", (100, 150), 30)
        button2 = index.Button("Waiting for player 2", (100, 250), 30)

        running = True

        while running:
            try:
                game = n.send("update")
            except Exception as e:
                running = False
                print(e)
                print("Couldn't get game")
                break

            # get the number of target
            target = grid.countTarget()

            clock.tick(FPS)
            index.window.blit(index.bg_img, (0, 0))
            backButton.draw()
            grid.draw()
            if 'grid1' not in data:
                button1.draw()
            elif 'grid1' in data:
                button2.draw()

            for ship in listShip:
                ship.draw()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                grid.handle_event(event)
                if backButton.click(event):
                    choose_size.main()
                for ship in listShip:
                    ship.handle_event(event)
                if ('grid1' not in data) and (target == data_map.totalTarget):
                    if button1.click(event):
                        data['grid1'] = grid.save()
                        with open("players_data.json", "w") as f:
                            f.write(str(data).replace("\'", "\""))
                        grid.__init__(data_map.gridSize, (200, 350), listShip)
                        data_map.reset_listShip()
                        game = n.send("ready")
            if (game.p1Ready) and (game.p2Ready):
                battle.main()