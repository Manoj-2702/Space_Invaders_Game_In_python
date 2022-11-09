import PySimpleGUI as sg
import json
import os
import pygame
import random
import time
from pygame import mixer
import json
import os.path
from datetime import datetime
def getHighScore():
    state = os.path.isfile('highscore.txt')
    if state == False:
        return 0
    with open("highscore.txt","r") as fp1:
        data = json.load(fp1)
        fp1.close()
        #print(max(data.values()))
        return(max(data.values()))

def Start_Menu():
    GUI = True
    sg.theme("Dark Blue")
    layout = [[sg.Text('Space Invaders')],
                     [sg.Button("Start Game")],
                        [sg.Text("Controls:\n A:LEFT\n D:RIGHT\n SPACE:SHOOT\n P:PAUSE\n")],
                     [sg.Button("View High Score")],
                     [sg.Button("Exit")]]

    window = sg.Window('Window Title', layout)

    while GUI:
        event, values = window.read()
        if event in (None, 'Exit'):
            break
        elif event == "Start Game":
            window.close()
            # *****ALL FUNCTIONS*******
            # functions to blit objects
            def player(x, y):
                screen.blit(playerimg, (x, y))

            def enemy(x, y, i):
                screen.blit(enemyimg[i], (x, y))

            def fire(bullet_state, x, y):
                bullet_state = True
                screen.blit(bulletimg, (x + 16, y + 10))
                return bullet_state

            def isColission(enemyx, enemyy, bulletx, bullety):
                dist = ((enemyx - bulletx) ** 2 + (bullety - enemyy) ** 2) ** 0.5
                if dist < (8 + 32):
                    return True
                else:
                    return False

            def isGameOver(enemyx, enemyy, playerx, playery):
                dist = ((enemyx - playerx) ** 2 + (enemyy - playery) ** 2) ** 0.5
                # print(dist)
                if dist < 50:
                    return True
                else:
                    return False

            def show_score(x, y, score):
                val = pygame.font.Font("jedi.ttf", 25).render("Score : " + str(score), True,
                                                              (0, 255, 255))  # rendering the text
                screen.blit(val, (x, y))  # blitting the text on (x,y) where tuple indicates pos

            def game_over_text(score):
                val = pygame.font.Font("jedi.ttf", 25).render("Your Final Score: " + str(score), True, (0, 255, 255))
                mess = pygame.font.Font("jedi.ttf", 25).render("Game Over", True, (0, 255, 255))
                screen.blit(val, (200, 250))
                screen.blit(mess, (200, 300))

            def isHighScore(myscore):
                choice = 0
                d = dict()

                # taking input score
                curr = datetime.now()

                # checking if file exists
                state = os.path.isfile('highscore.txt')
                if state == False:
                    # creating file
                    with open("highscore.txt", "a+") as f:
                        d.update({str(curr): myscore})
                        f.write(json.dumps(d))
                    f.close()
                else:
                    # comparing score
                    with open("highscore.txt", "r") as fp1:
                        data = json.load(fp1)
                        fp1.close()
                    if score > max(data.values()):
                        d.update({str(curr): score})
                        with open("highscore.txt", "w") as fp:
                            fp.write(json.dumps(d))
                            fp.close()

                # reading score
                with open("highscore.txt", "r") as fp1:
                    data = json.load(fp1)
                    high = max(data.values())
                fp1.close()
                return high

            # ****END OF HIGH SCORE****
            def EndHighScoreTxt(highscore):
                val = pygame.font.Font("jedi.ttf", 25).render("Your HighScore: " + str(highscore), True, (0, 255, 255))
                screen.blit(val, (200, 350))

            def PrevHighScoreTxt(x, y, highscore):
                val = pygame.font.Font("jedi.ttf", 25).render("Prev Highscore : " + str(highscore), True,
                                                              (0, 255, 255))  # rendering the text
                screen.blit(val, (x, y))

            def getPrevHighScore():
                state = os.path.isfile('highscore.txt')
                if state == True:
                    with open("highscore.txt", "r") as fp1:
                        data = json.load(fp1)
                        curr = max(data.values())
                        fp1.close()
                    return curr
                else:
                    return 0

            def QuitWindow():
                layout = [[sg.Text("Do you really want to quit")],
                          [sg.Button("Yes"), sg.Button("No")]]

                quit_window = sg.Window('Window Title', layout)
                extbutton = True
                while extbutton:
                    event, values = quit_window.read()
                    if event in (None, 'Exit'):
                        break
                    if event == "Yes":
                        extbutton = False
                        quit_window.close()
                        return [True, False]
                    elif event == "No":
                        quit_window.close()
                        return [False, True]  # pause,running
            def PauseWindow():
                layout = [[sg.Text("Game Paused")],[sg.Button("Resume")]]

                pause_window = sg.Window('Window Title', layout)
                pausebttn = True
                while pausebttn:
                    event, values = pause_window.read()
                    if event in (None, 'Exit'):
                        break
                    if event == "Resume":
                        pausebttn = False
                        pause_window.close()
                        return [False,True] #pause,running
                

                window.close()

            # *****ENDS HERE THE FUNCS********

            # *************************MAIN GAME FUNC*********************

            pygame.mixer.pre_init(44100, 16, 2, 4096)
            pygame.init()
            bg = pygame.image.load("space.jpg")
            mixer.music.load("bgm_16bit.wav")
            mixer.music.play(-1)  # to play on loop
            screen = pygame.display.set_mode((800, 600))

            pygame.display.set_caption("Space Invasion")
            ufo = pygame.image.load("ufo.jpg")
            pygame.display.set_icon(ufo)

            # game over
            flag = False

            # player
            playerimg = pygame.image.load('ship.png')
            playerh = playerw = 64
            playerx = 370
            playery = 480
            playerXchange = 0
            playerYchange = 0

            # multiple enemies
            enemyno = 6  # change based on difficulty
            enemyimg = []
            enemyx = []
            enemyy = []
            enemyh = []
            enemyw = []
            enemyXchange = []
            enemyYchange = []
            for i in range(enemyno):
                enemyimg.append(pygame.image.load('opp.png'))
                enemyh.append(64)
                enemyw.append(64)
                enemyx.append(random.randint(0, (800 - enemyw[i])))
                enemyy.append(random.randint(50, 150))
                enemyXchange.append(2)
                enemyYchange.append(0)

            # bullet
            bulletimg = pygame.image.load("bullet.png")
            bulleth = bulletw = 16
            bulletx = 0  # we are gonna change the value inside the while loop
            bullety = 480  # initial position of the battleship
            bulletchange = 6
            bullet_state = False  # Not yet shot the bullet

            # score:
            scorex = 10  # pos of score
            scorey = 10
            score = 0

            running = True
            # print(isHighScore(0))
            prev_high = getPrevHighScore()
            # print(prev_high)
            # event loop
            GAME = True
            while GAME:
                pause = False
            
                
                while pause == False:
                    while running:
                        screen.fill((0, 0, 0))  # screen shld be at the start
                        # add after black space
                        screen.blit(bg, (0, 0))  # this is a large file and hence it has to load everytime in while loop
                        presses = pygame.key.get_pressed()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False
                                GAME = False
                                pause = True
                                GUI = False
                            if event.type == pygame.KEYDOWN:  # pressed key
                                if event.key == pygame.K_a:
                                    playerXchange = -4
                                elif event.key == pygame.K_d:
                                    playerXchange = 4
                                elif event.key == pygame.K_SPACE:
                                    bulletx = playerx
                                    bullet_state = fire(bullet_state, bulletx, bullety)

                            if event.type == pygame.KEYUP:  # releasing the key
                                if event.key == pygame.K_a or event.key == pygame.K_a or event.key == pygame.K_d:
                                    playerXchange = 0
                                    playerYchange = 0
                        if presses[pygame.K_q]:
                            pause = True
                            pause, running = QuitWindow()
                            GAME = False
                            pause = True
                            GUI = False
                            window.close()
                        if presses[pygame.K_p]:
                            pause = True
                            pause, running = PauseWindow()
                        if presses[pygame.K_r]:
                            pause = False
                        # changing velocity of player ship
                        playerx = playerx + playerXchange
                        playery = playery + playerYchange

                        # boundary cond. forr player ship
                        if playerx > (800 - playerw):
                            playerx = (800 - playerw)
                        elif playerx < 0:
                            playerx = 0
                        elif playery < 400:
                            playery = 400
                        elif playery > (600 - playerh):
                            playery = (600 - playerh)

                        # boundary condition for enemy ship and Collission of enemy with ship
                        for i in range(enemyno):
                            gameover = isGameOver(enemyx[i], enemyy[i], playerx, 480)
                            if gameover == True:
                                for j in range(enemyno):  # moving all enemies out of the screen
                                    enemyy[j] = 2000
                                    end = mixer.Sound("gameover.wav")
                                    end.play()
                                # ************calling high score********
                                high = isHighScore(score)
                                flag = True
                                break

                            if enemyx[i] > (800 - enemyw[i]):
                                enemyXchange[i] = -2
                                enemyYchange[i] = enemyh[i] / 2
                                time.sleep(1 / 60)
                                enemyy[i] = enemyy[i] + enemyYchange[i]  # shld change only after it collides with wall

                            elif enemyx[i] < 0:
                                enemyXchange[i] = 2
                                enemyYchange[i] = enemyh[i]
                                time.sleep(1 / 60)
                                enemyy[i] = enemyy[i] + enemyYchange[i]  # shld change only after it collides with wall
                            enemyx[i] = enemyx[i] + enemyXchange[i]
                            # checking for collission for each enemy with bullet
                            # collission with bullet:
                            collission = isColission(enemyx[i], enemyy[i], bulletx, bullety)
                            if collission == True and bullet_state == True:
                                shoot = mixer.Sound("explosion.wav")
                                shoot.play()
                                bullety = 480
                                bullet_state = False
                                score = score + 1
                                # print(score)
                                # reset enemy to a random location
                                enemyx[i] = random.randint(0, (800 - enemyw[i]))
                                enemyy[i] = random.randint(50, 150)
                            # image blitting for each enemy
                            enemy(enemyx[i], enemyy[i], i)

                        # bullet trajectory
                        if bullet_state == True:
                            if bullety <= 0:  # once it crosses (0,0) it should reset to initial condition
                                bullety = 480
                                bullet_state = False
                            fire(bullet_state, bulletx, bullety)  # this is used to blit the bullet img every frame
                            # print(bullety)
                            bullety = bullety - bulletchange  # we want the bullet to travel in upward direction when we shoot

                        # enemy png and player png shld appear on top of screen n its inside while loop for continous blitting
                        player(playerx, playery)
                        show_score(scorex, scorey, score)
                        # FPreprint(prev_high)
                        PrevHighScoreTxt(scorex, scorey + 30, prev_high)
                        if flag == True:
                            game_over_text(score)
                            EndHighScoreTxt(prev_high)
                        pygame.display.update()


        elif event == "View High Score":
            Score = getHighScore()
            sg.popup('\nYour High Score\n', Score)
        elif event == "Exit":
            GUI = False
            window.close()
        pygame.quit()
Start_Menu()

