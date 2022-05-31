import sys
import pygame
import index
import accueil
import choose_size
import json
import battle
import set_grid

# setting for the infinity loop
clock = pygame.time.Clock()
FPS = 60

button1 = index.Button('MENU', (650, 300), 100)
button2 = index.Button('REPLAY', (650, 400), 100)      
button3 = index.Button('QUIT',( 650, 500), 100)     


def main():
    running = True
    #get data stocked in a json file
    with open("players_data.json", "r") as f:
        data = f.read()
        data = json.loads(data)
    
    if data['mode'] == 'multi2':
        global n
        n = battle.n #get the connection created before
    
    if data['mode'] == 'multi2':
        try:
            game = n.send("update")
            data['winner'] = game.winner
        except Exception as e:
            print(e)
            print("Coudn't get game")
            running = False


    while running:
        
        winner = index.Text_box('The winner is ' + str(data['winner']), (300, 100), 50, index.BLACK)
        
        clock.tick(FPS)
        index.window.blit(index.bg_img, (0, 0))
        button1.draw()
        button2.draw()
        button3.draw()
        winner.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or button3.click():    
                pygame.quit()
                sys.exit()
            if button1.click(): 
                accueil.main()
            if button2.click():     
                if data['mode'] == 'mono':
                    data.pop('winner')
                    data.pop('grid1')
                    data.pop('size')
                    data.pop("chifoumi")
                if data['mode'] == 'multi':
                    data.pop('winner')
                    data.pop('grid1')
                    data.pop('grid2')
                    data.pop('size')
                    data.pop("chifoumi")
                if data['mode'] == 'multi2':
                    data.pop('winner')
                    data.pop('grid1')
                    data["replay"] = "True"
                    with open("players_data.json", "w") as f:
                        f.write(str(data).replace("\'", "\""))
                        game = n.send('reset')
                        set_grid.main()
                with open("players_data.json", "w") as f:
                    f.write(str(data).replace("\'", "\""))
                choose_size.main()
                    
        pygame.display.update()


if __name__ == '__main__':
    main()