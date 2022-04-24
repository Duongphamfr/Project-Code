import sys
import pygame
import index
import json
import result



# setting for the infinity loop
clock = pygame.time.Clock()
FPS = 60

def main():
    with open("players_data.json", "r") as f:
        data = f.read()
        data = json.loads(data)

    if data['mode'] == 'mono':
        grid1 = index.Grid(10, (200, 300), getData="Player1")
        gridAuto = index.Grid(10, (1200, 300), getData="Random Medium")

        name1 = index.Text_box(data['name1'], (200, 150), 50, index.BLACK)
        nameAuto = index.Text_box("Computer", (1200, 150), 50, index.BLACK)



        turn = "player1"
        
        running = True
        while running:
            clock.tick(FPS)
            index.window.blit(index.bg_img, (0, 0))
            grid1.draw()
            gridAuto.draw()
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
                if turn == "player1":
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
                        turn = "auto"
                if turn == "auto":
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
                        turn = "player1"

    elif data['mode'] == 'multi':

        grid1 = index.Grid(10, (200, 300), getData="Player1")
        grid2 = index.Grid(10, (1200, 300), getData="Player2")
        name1 = index.Text_box(data['name1'], (200, 150), 50, index.BLACK)
        name2 = index.Text_box(data['name2'], (1200, 150), 50, index.BLACK)




        turn = "player1"
        
        running = True
        while running:
            clock.tick(FPS)
            index.window.blit(index.bg_img, (0, 0))
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
                if turn == "player1":
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
                        turn = "player2"
                if turn == "player2":
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
                        turn = "player1"