from time import sleep
from imagesearch import *
import threading
import pyautogui
from pynput import keyboard as keyboardL
import sys
from datetime import datetime
import os


class Bot:
    eventEmptyFlag = True
    pyautogui.FAILSAFE = False
    '''0,0       X increases -->
+---------------------------+
|                           | Y increases
|                           |     |
|   1920 x 1080 screen      |     |
|                           |     V
|                           |
|                           |
+---------------------------+ 1919, 1079'''
    mouseX = 0
    mouseY = 0
    skill_1_mouseX = 466
    skill_1_mouseY = 521
    imageFolder = os.getcwd()+r"\\imagens\\"
    thingsOK = True
    battles = 0
    location = None
    exiting = False

def eventEmpty():
    return Bot.eventEmptyFlag

def walk(key, times=1):
    if times == 1:
        pyautogui.typewrite(key)
    else:
        hold(key, times * 0.225)

def skill(key):
    pyautogui.press(str(key))

def hold(key, holdTime=0.25):
    pyautogui.keyDown(key)
    sleep(holdTime)
    pyautogui.keyUp(key)

def on_press(key):
    try:
        k = key.char
        print('alphanumeric key {0} pressed'.format(key.char))
    except:
        return

    if k == 'p':
        im = pyautogui.screenshot()
        im.save('exit.png')
        exit('on_press')
    if k =='m':
        getMousePosition()

def keyboardListener():
    # Collect events until released
    try:
        with keyboardL.Listener(on_press=on_press) as listener:
            listener.join()
            listener.start()
    except:
        exit('keyboardListener')


def exit(called):
    Bot.exiting = True
    print(called+' exiting!!!!!!!!!')
    sys.exit()


def getMousePosition():
    Bot.mouseX, Bot.mouseY = pyautogui.position()
    print("mouseX :"+str(Bot.mouseX))
    print("mouseY :"+str(Bot.mouseY))

# def isPokemonAlive():
#     img = imagesearch(Bot.imageFolder + 'battleFound.png', precision=0.95)
#     isAlive = img is not None
#     if not isAlive:
#         print('POKEMON MORREU')
#     else:
#         print('POKEMON VIVO')
#     return isAlive

def battle(verifySituationCommand):
    while True:
        if imgClick(Bot.imageFolder + 'fight.png', 1, 1):
            sleep(0.4)
            if '1' in verifySituationCommand:
                skill('1')
            sleep(2)
        img = imagesearch(Bot.imageFolder+'battleFound.png', precision=0.8)
        if img is None:
            Bot.battles = Bot.battles + 1
            print('battles: '+str(Bot.battles))
            return

def verifyBattle():
    img = imagesearch(Bot.imageFolder+'battleFound.png', precision=0.8)
    if img is not None:
        Bot.thingsOK = True
        print("battleFound!")
        sleep(1)
        img = imagesearch_numLoop(Bot.imageFolder + 'fight.png', 1, 5, precision=0.8)
        if img is not None:
            verifySituationCommand = verifyBattleSituation()
            if 'fight' in verifySituationCommand:
                battle(verifySituationCommand)

def verifyBattleSituation():
    # img = imagesearch(Bot.imageFolder + 'spearrow.png', precision=0.95)
    # if img is not None:
    #     return 'fight'
    # else:
    #     print('ACHEI ALGO')
    #     catchPokemon()
    return 'fight_1'

def run():
    imgClick(Bot.imageFolder + 'run.png', 1, 5)
    sleep(2)

def hunt():
    while(True):
        walk("a", 7)
        verifyBattle()
        verifySituation()
        #verifyDeath(locaation)d
        walk("d", 7)
        verifyBattle()
        verifySituation()
        #verifyDeath(location)
        print("hunting!")


def verifySituation():
    if Bot.exiting:
        exit('verifySituation')
    if Bot.location == 'route_10':
        if Bot.battles > 1:
            print('HEALING!')
            moveTo('route_10_pokecenter')
            healPokecenter()
            moveTo('route_10')
            Bot.battles = 0

def healPokecenter():
    sleep(3)
    walk('w', 8)
    pyautogui.typewrite('       11111111', 0.3)
    sleep(2)
    pyautogui.typewrite(' ', 0.5)
    sleep(1)
    pyautogui.typewrite('  ', 1)
    walk('s', 8)
    sleep(3)

def moveTo(m):
    if m == 'route_10':
        walk("s", 10)
    elif m == 'route_10_pokecenter':
        #tem q pensar em melhorar essa gambi
        walk("w", 4)
        walk("d", 15)
        walk("a", 6)
        walk("w", 4)



# def verifyDeath(moveToLocation):
#     img = imagesearch(Bot.imageFolder + 'nurse.png', precision=0.8)
#     if img is not None:
#         print("DEATH DETECTED")
#         moveTo(moveToLocation)

# def catchPokemon():
#     ret = imgClick(Bot.imageFolder + 'bag.png',1, 3, precision=0.8)
#     if not ret:
#         return False
#     ret = imgClick(Bot.imageFolder + 'ball.png', 1, 3, precision=0.8)
#     if not ret:
#         return False
#     ret = imgClick(Bot.imageFolder + 'useItem.png', 1, 3, precision=0.8)
#     if not ret:
#         return False

def exitOnError():
    while True:
        Bot.thingsOK = False
        sleep(120)
        if not Bot.thingsOK:
            print("EXITING BY INACTIVITY")
            exit('exitOnError')
        elif Bot.exiting:
            exit('exitOnError')

def timePrinter():
    while True:
        print(datetime.now())
        sleep(10)
        if Bot.exiting:
            exit('timePrinter')

# def fishing():
#     while True:
#         pos = imagesearch_numLoop(Bot.imageFolder + 'fishing.png', 0.01, 10, 0.91, False)
#         if pos is not None:
#             pyautogui.press("space")

def main():
    Bot.command = 'battle'
    Bot.location ='route_10'

    t = []
    t.append(threading.Thread(target=keyboardListener, args=()))
    t.append(threading.Thread(target=hunt, args=()))
    t.append(threading.Thread(target=exitOnError, args=()))
    t.append(threading.Thread(target=timePrinter, args=()))

    sleep(1)
    for oneT in t:
        oneT.start()

#MAIN
main()