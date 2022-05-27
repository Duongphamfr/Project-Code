import sys
import pygame
import index
import json
import result
import accueil
import set_grid

quitButton = index.Button("QUIT", (1500, 0), 50)

# setting for the infinity loop
clock = pygame.time.Clock()
FPS = 60

def main():

    with open("players_data.json", "r") as f:
        data = f.read()
        data = json.loads(data)
    
    if data['size'] == 'small':
        gridSize = 7
    elif data['size'] == 'medium':
        gridSize = 10
    
    turn = data['name1']

    if data['mode'] == 'mono':
        grid1 = index.Grid(gridSize, (200, 300), getData="Player1")
        gridAuto = index.Grid(gridSize, (1200, 300), getData="Random")

        name1 = index.Text_box("Grid of " + data['name1'], (200, 150), 50, index.BLACK)
        nameAuto = index.Text_box("Grid of " + "Computer", (1200, 150), 50, index.BLACK)
        
        running = True
        while running:
            clock.tick(FPS)
            index.window.blit(index.bg_img, (0, 0))
            quitButton.draw()
            grid1.draw()
            gridAuto.draw()
            turnText = index.Text_box("Turn of: " + turn, (700, 100), 50, index.BLACK)
            turnText.draw()
            # draw text name player
            name1.draw()
            nameAuto.draw()
            # draw text the number target remain grid.countTargetAlive()
            target1 = index.Text_box("Target Alive: " + str(grid1.countTargetAlive()), (200, 800), 50, index.BLACK)
            targetAuto = index.Text_box("Target Alive: " + str(gridAuto.countTargetAlive()), (1200, 800), 50, index.BLACK)

            target1.draw()
            targetAuto.draw()

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if quitButton.click(event):
                    accueil.main()
                if turn == data['name1']:
                    # draw text turn
                    grid1.resetTurn()
                    grid1.offAttacked()
                    gridAuto.onAttacked()
                    gridAuto.attacked(event)
                    if gridAuto.countTargetAlive() == 0:
                        with open("players_data.json", "w") as f:
                            data['winner'] = data['name1']
                            f.write(str(data).replace("\'", "\""))
                        result.main()
                    if gridAuto.changeTurn():
                        turn = "Computer"
                if turn == "Computer":
                    # draw text turn
                    gridAuto.resetTurn()
                    gridAuto.offAttacked()
                    grid1.onAttacked()
                    grid1.randomAttacked()
                    grid1.attacked(event)
                    if grid1.countTargetAlive() == 0:
                        with open("players_data.json", "w") as f:
                            data['winner'] = 'Computer'
                            f.write(str(data).replace("\'", "\""))
                        result.main()
                    if grid1.changeTurn():
                        turn = data['name1']

    elif data['mode'] == 'multi1':

        grid1 = index.Grid(gridSize, (200, 300), getData="Player1")
        grid2 = index.Grid(gridSize, (1200, 300), getData="Player2")
        name1 = index.Text_box("Grid of " + data['name1'], (200, 150), 50, index.BLACK)
        name2 = index.Text_box("Grid of " + data['name2'], (1200, 150), 50, index.BLACK)



        running = True
        while running:
            clock.tick(FPS)
            index.window.blit(index.bg_img, (0, 0))
            quitButton.draw()
            turnText = index.Text_box("Turn of: " + turn, (700, 100), 50, index.BLACK)
            turnText.draw()
            grid1.draw()
            grid2.draw()
            # draw text name player
            name1.draw()
            name2.draw()
            # draw text the number target remain grid.countTargetAlive()
            target1 = index.Text_box("Target Alive: " + str(grid1.countTargetAlive()), (200, 800), 50, index.BLACK)
            target2 = index.Text_box("Target Alive: " + str(grid2.countTargetAlive()), (1200, 800), 50, index.BLACK)

            target1.draw()
            target2.draw()

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if quitButton.click(event):
                    accueil.main()
                if turn == data['name1']:
                    # draw text turn
                    grid1.resetTurn()
                    grid1.offAttacked()
                    grid2.onAttacked()
                    grid2.attacked(event)
                    if grid2.countTargetAlive() == 0:
                        with open("players_data.json", "w") as f:
                            data['winner'] = data['name1']
                            f.write(str(data).replace("\'", "\""))
                        result.main()
                    if grid2.changeTurn():
                        turn = data['name2']
                if turn == data['name2']:
                    # draw text turn
                    grid2.resetTurn()
                    grid2.offAttacked()
                    grid1.onAttacked()
                    grid1.attacked(event)
                    if grid1.countTargetAlive() == 0:
                        with open("players_data.json", "w") as f:
                            data['winner'] = data['name2']
                            f.write(str(data).replace("\'", "\""))
                        result.main()
                    if grid1.changeTurn():
                        turn = data['name1']




# part must finish ##################################################################################
    elif data['mode'] == 'multi2':
        running = True

        n = set_grid.n
        try:
            game = n.send("get")
            if data["playerId"] == "1":
                grid1 = index.Grid(gridSize, (200, 300), getData="Player1")
                game.grid1 = grid1
            else:
                grid2 = index.Grid(gridSize, (1200, 300), getData="Player1")
                game.grid2 = grid2
        except:
            running = False
            print("Couldn't get game")



        name1 = index.Text_box("Grid of " + game.name1, (200, 150), 50, index.BLACK)
        name2 = index.Text_box("Grid of " + game.name2, (1200, 150), 50, index.BLACK)


        while running:
            try:
                game = n.send("get")
                grid1 = game.grid1
                grid2 = game.grid2
            except:
                running = False
                print("Couldn't get game")
                break

            clock.tick(FPS)
            index.window.blit(index.bg_img, (0, 0))
            quitButton.draw()
            turnText = index.Text_box("Turn of: " + turn, (700, 100), 50, index.BLACK)
            turnText.draw()
            grid1.draw()
            grid2.draw()
            # draw text name player
            name1.draw()
            name2.draw()
            # draw text the number target remain grid.countTargetAlive()
            target1 = index.Text_box("Target Alive: " + str(grid1.countTargetAlive()), (200, 800), 50, index.BLACK)
            target2 = index.Text_box("Target Alive: " + str(grid2.countTargetAlive()), (1200, 800), 50, index.BLACK)

            target1.draw()
            target2.draw()

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if quitButton.click(event):
                    accueil.main()
                if game.turn == 1 and data['playerId'] == '1':
                    # draw text turn
                    grid1.resetTurn()
                    grid1.offAttacked()
                    grid2.onAttacked()
                    grid2.attacked(event)
                    if grid2.changeTurn():
                        game.turn = 2
                if game.turn == 2 and data['playerId'] == '2':
                    # draw text turn
                    grid2.resetTurn()
                    grid2.offAttacked()
                    grid1.onAttacked()
                    grid1.attacked(event)
                    if grid1.changeTurn():
                        game.turn = 1
            if grid2.countTargetAlive() == 0:
                game.winner = data['name1']
                game = n.send("get")
                result.main()
            if grid1.countTargetAlive() == 0:
                game.winner = data['name1']
                game = n.send("get")
                result.main()

