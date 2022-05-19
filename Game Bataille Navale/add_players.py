import sys
import pygame
import index
import accueil
import choose_size
import json


backButton = index.Button("BACK",(0,0),80)
textGuide = index.Text_box("Fill your name and press Enter to continue", (100, 600), 50, index.BLACK)

# setting for the infinity loop
clock = pygame.time.Clock()
FPS = 60

def main():
    with open("players_data.json", "r") as f:
        data = f.read()
        data = json.loads(data)

    if data['mode'] == 'mono' or data['mode'] == 'multi2':
        input1 = index.Input_box((600,100),(650,300))
        text1 = index.Text_box("Player's Name", (650, 250), 80, index.BLACK)
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
                    accueil.main()
                input1.handle_event(event)
                if len(input1.user_text) != 0:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            if data['host'] == 'True' or data['mode'] == 'mono':
                                data["name1"] = input1.user_text
                                with open("players_data.json", "w") as f:
                                    f.write(str(data).replace("\'", "\""))
                                choose_size.main()
                            elif data['host'] == 'False':
                                data["name2"] = input1.user_text
                                with open("players_data.json", "w") as f:
                                    f.write(str(data).replace("\'", "\""))
                                join_room.main()


            pygame.display.update()
    
    elif data['mode'] == 'multi1':
        input1 = index.Input_box((600,100),(300,300))
        input2 = index.Input_box((600,100),(1000,300))
        text1 = index.Text_box("Name of Player 1", (300, 250), 80, index.BLACK)
        text2 = index.Text_box("Name of Player 2", (1000, 250), 80, index.BLACK)
        running = True
        while running:
            clock.tick(FPS)
            index.window.blit(index.bg_img, (0, 0))
            backButton.draw()
            input1.draw()
            input2.draw()
            text1.draw()
            text2.draw()
            textGuide.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if backButton.click(event):
                    accueil.main()
                input1.handle_event(event)
                input2.handle_event(event)
                if (len(input1.user_text) != 0) and (len(input2.user_text) != 0):
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            data["name1"] = input1.user_text
                            data["name2"] = input2.user_text
                            with open("players_data.json", "w") as f:
                                f.write(str(data).replace("\'", "\""))
                            choose_size.main()
            pygame.display.update()

