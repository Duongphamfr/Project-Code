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
        button1 = index.Button("Confirm grid", (100, 300), 30)
        button3 = index.Button("WAR", (100, 300), 50)
        guide_1 = index.Text_box(" click RIGHT mouse to change the ships' direction", (650, 130), 50, index.BLACK)
        guide_2 = index.Text_box("1. Drag and drop the ships in the map,", (650,90), 50, index.BLACK)
        guide_3 = index.Text_box("2. Click confirm when ships are all set", (650,180), 50, index.BLACK)
        running = True
        chifoumi_single = index.chifoumi_game()

        while running:
            # get the number of target
            target = grid.countTarget()

            clock.tick(FPS)
            index.window.blit(index.bg_img, (0, 0))
            backButton.draw()
            grid.draw()
            index.window.blit(index.wood_img, (630,50))
            
            if ('grid1' not in data):
                button1.draw()
                guide_1.draw()
                guide_2.draw()
                guide_3.draw()
                chifoumi_single.draw()
            if ('grid1' in data):
                button3.draw()
                chifoumi_single.print_result_COM()
            for ship in listShip:
                ship.draw()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                grid.handle_event(event)
                if backButton.click(): 
                    choose_size.main()
                for ship in listShip:
                    ship.handle_event(event)
                if ('grid1' not in data) and (target == data_map.totalTarget) and chifoumi_single.choice_player != "null":
                    if button1.click():
                        data['grid1'] = grid.save()
                        with open("players_data.json", "w") as f:
                            f.write(str(data).replace("\'", "\""))
                        grid.__init__(data_map.gridSize, (200, 350), listShip)
                        data_map.reset_listShip()
                        print("Saved Player 1")
                if ('grid1' in data):
                    if button3.click():
                        battle.main()
                if chifoumi_single.choose(event) != 0:
                    chifoumi_single.play_COM()
            chifoumi_single.chifoumi(chifoumi_single.choice_player, chifoumi_single.choice_COM)
            

    elif data['mode'] == 'multi':
        button1 = index.Button("Confirm grid of player 1", (100, 300), 30)
        button2 = index.Button("Confirm grid of player 2", (500, 300), 30)
        button3 = index.Button("WAR", (100, 300), 50)
        guide_1 = index.Text_box(" click RIGHT mouse to change the ships' direction", (650, 130), 50, index.BLACK)
        guide_2 = index.Text_box("1. Drag and drop the ships in the map,", (650,90), 50, index.BLACK)
        guide_3 = index.Text_box("2. Click confirm when ships are all set", (650,180), 50, index.BLACK)
        
        running = True
        chifoumi_multi = index.chifoumi_game()
        while running:
            # get the number of target
            target = grid.countTarget()

            clock.tick(FPS)
            index.window.blit(index.bg_img, (0, 0))
            backButton.draw()
            grid.draw()
            index.window.blit(index.wood_img, (630,50))
            if ('grid1' not in data):
                button1.draw()
                guide_1.draw()
                guide_2.draw()
                guide_3.draw()
                chifoumi_multi.draw()
            if ('grid2' not in data):
                button2.draw()
                guide_1.draw()
                guide_2.draw()
                guide_3.draw()
                chifoumi_multi.draw()
            if ('grid1' in data) and ('grid2' in data):
                button3.draw()
                chifoumi_multi.print_result_player()
            for ship in listShip:
                ship.draw()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                grid.handle_event(event)
                if backButton.click():  
                    choose_size.main()
                for ship in listShip:
                    ship.handle_event(event)
                if ('grid1' not in data) and (target == data_map.totalTarget) and chifoumi_multi.choice_player_1 != "null":
                    if button1.click():    
                        data['grid1'] = grid.save()
                        with open("players_data.json", "w") as f:
                            f.write(str(data).replace("\'", "\""))
                        grid.__init__(data_map.gridSize, (200, 350), listShip)
                        data_map.reset_listShip()
                        chifoumi_multi.reset_choice()
                if ('grid2' not in data) and (target == data_map.totalTarget) and chifoumi_multi.choice_player_2 != "null":
                    if button2.click(): 
                        data['grid2'] = grid.save()
                        with open("players_data.json", "w") as f:
                            f.write(str(data).replace("\'", "\""))
                        grid.__init__(data_map.gridSize, (200, 350), listShip)
                        data_map.reset_listShip()
                        chifoumi_multi.reset_choice()
                if ('grid1' in data) and ('grid2' in data):
                    if button3.click(): 
                        battle.main()   
                if chifoumi_multi.choose(event) != 0 and ('grid1' not in data):
                    chifoumi_multi.play_1()
                if chifoumi_multi.choose(event) != 0 and ('grid2' not in data):
                    chifoumi_multi.play_2()
            chifoumi_multi.chifoumi(chifoumi_multi.choice_player_1,chifoumi_multi.choice_player_2)
            
############################ TWO PLAYERS ON TWO DIFFERENT COMPUTERS IN THE SAME LAN (LOCAL AREA NETWORK) ############################
    if data['mode'] == 'multi2':
        # get the connection created before
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
                if backButton.click():
                    choose_size.main()
                for ship in listShip:
                    ship.handle_event(event)
                if ('grid1' not in data) and (target == data_map.totalTarget):
                    if button1.click():
                        data['grid1'] = grid.save()
                        with open("players_data.json", "w") as f:
                            f.write(str(data).replace("\'", "\""))
                        grid.__init__(data_map.gridSize, (200, 350), listShip)
                        data_map.reset_listShip()
                        game = n.send("ready")
            if (game.p1Ready) and (game.p2Ready):
                battle.main()