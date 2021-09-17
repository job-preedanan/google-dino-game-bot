import cv2
from PIL import ImageGrab
from object import Object
import numpy as np
import pyautogui as pag
import time


def grabScreen(bbox=None):
    img = ImageGrab.grab(bbox=bbox)
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return img


dino = Object('objects/dino.png')
restart = Object('objects/restart.png')
enemies = [Object('objects/plant1.png'), Object('objects/plant2.png'), Object('objects/plant3.png'),
           Object('objects/bird.png')]
distance_th = 80
start_time = time.time()
prev_time = time.time()
speed_increase = 2

# detecting dino to start the game.
while 1:
    # capture whole screen to find dino.
    screen = grabScreen()
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)

    if restart.matching(screen_gray):
        print('Restart !!')
        pag.press('space')

    if dino.matching(screen_gray):

        # cropping the screen based on dino's location
        start_point = (dino.location[0][0] - dino.width, dino.location[0][1] - 2*dino.height)
        end_point = (dino.location[1][0] + 8*dino.width, dino.location[1][1] + dino.height)

        print('Game Start !!')
        print(start_point[0], start_point[1], end_point[0], end_point[1])
        break

    cv2.imshow('screen', screen)

    if cv2.waitKey(1) == ord('q'):
        break

pag.press('space')

# playing the game
while 1:

    print_flag = False

    # screen = grabScreen(bbox=(600, 100, 1000, 300))
    screen = grabScreen(bbox=(start_point[0], start_point[1], end_point[0], end_point[1]))
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)

    # speed adjust (every 1 sec.)
    current_time = time.time() - start_time
    if time.time() - prev_time >= 1 and current_time < 180:
        # print('Time:' + str(int(current_time)) + ', distance_th = ' + str(distance_th))
        distance_th += speed_increase
        print_flag = True
        prev_time = time.time()

    if dino.matching(screen_gray):
        cv2.rectangle(screen, dino.location[0], dino.location[1], (0, 255, 0))

    for enemy in enemies:

        if enemy.matching(screen_gray):
            cv2.rectangle(screen, enemy.location[0], enemy.location[1], (0, 0, 255))

            # horizontal :enemy(start loc x) - player(end loc x)
            distance_x = enemy.location[0][0] - dino.location[1][0]

            # vertical : enemy(end loc y) - player(start loc y)
            distance_y = enemy.location[1][1] - dino.location[0][1]

            if print_flag:
                print('found ' + enemy.name + ' : (x,y)=(' + str(distance_x) + ',' + str(distance_y) + ')')

            # jump if the horizontal distance is less than threshold and don't jump if enemy is above dino.
            if distance_x < distance_th and distance_y > 5:
                pag.press('space')
                break

    cv2.imshow('screen', screen)

    if cv2.waitKey(1) == ord('q'):
        print('End !!')
        break
