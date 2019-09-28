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
    loops = 0
    command = ''
    walk = 'ad'

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

def verifyBattleStuck():
    sleep(0.5)
    img = imagesearch(Bot.imageFolder + 'fight.png', precision=0.8)
    if img is None:
        return

    #vish
    imgClick(Bot.imageFolder + 'pokemon.png', 1, 1)
    pyautogui.typewrite('23456',0.4)


def battle(verifySituationCommand):
    while True:
        if imgClick(Bot.imageFolder + 'fight.png', 1, 1):
            sleep(0.4)
            if '1' in verifySituationCommand:
                skill('1')
            verifyBattleStuck()
            sleep(2)
        img = imagesearch(Bot.imageFolder+'battleFound.png', precision=0.8)
        if img is None:
            Bot.battles = Bot.battles + 1
            print('battles: '+str(Bot.battles))
            Bot.thingsOK = True
            return

def verifyBattle():
    img = imagesearch(Bot.imageFolder+'battleFound.png', precision=0.8)
    if img is not None:
        print("battleFound!")
        sleep(1)
        img = imagesearch_numLoop(Bot.imageFolder + 'fight.png', 1, 2, precision=0.8)
        if img is not None:
            if 'fight' in Bot.command:
                battle(Bot.command)
            if 'catch' in Bot.command:
                catch()


def catch():
    img = imagesearch(Bot.imageFolder + 'abra.png', precision=0.9)
    if img is None:
        img = imagesearch(Bot.imageFolder + 'ditto.png', precision=0.9)
    if img is not None:
        print('POKEMON FOUND')
        sleep(9999)

    run()

def run():
    imgClick(Bot.imageFolder + 'run.png', 1, 5)
    Bot.thingsOK = True

def hunt():
    while(True):
        for dir in Bot.walk:
            walk(dir, 1)
            verifyBattle()
            verifySituation()
            verifyLearnMove()
            #verifyDeath(locaation)d
            print("hunting!")

def verifyLearnMove():
    img = imagesearch(Bot.imageFolder + 'doNotLearn.png', precision=0.8)
    if img is not None:
        imgClick(Bot.imageFolder + 'doNotLearn.png', 1, 3, precision=0.8)
        sleep(1)
        imgClick(Bot.imageFolder + 'yes.png', 1, 3, precision=0.8)

def verifySituation():
    if Bot.exiting:
        exit('verifySituation')
    if Bot.location == 'route_10':
        if Bot.battles > 5:
            print('HEALING!')
            moveTo('route_10_pokecenter')
            healPokecenter()
            moveTo('route_10')
            Bot.battles = 0
            Bot.loops = Bot.loops + 1
            print('Looping!!')
    elif Bot.location == 'pokemon_tower':
        if Bot.battles > 5:
            print('HEALING!')
            walk('d',4)
            nurseTalk(2)
            Bot.battles = 0
            Bot.loops = Bot.loops + 1
            print('Looping!!')
    if Bot.location == 'cinnabar':
        if Bot.battles > 5:
            print('HEALING!')
            moveTo('cinnabar_pokecenter')
            healPokecenter('cinnabar')
            moveTo('cinnabar_mansion')
            Bot.battles = 0
            Bot.loops = Bot.loops + 1
            print('Looping!!')


def nurseTalk(spaces):
    pyautogui.typewrite('       11111111', 0.3)
    sleep(2)
    for i in range(0, spaces):
        pyautogui.typewrite(' ')
        sleep(2)


def healPokecenter(pokecenter='default'):
    if pokecenter == 'cinnabar':
        sleep(3)
        walk('w', 4)
        walk('a', 4)
        walk('w', 3)
        nurseTalk(3)
        walk('s', 7)
        walk('d', 4)
        sleep(3)
    else:
        sleep(3)
        walk('w', 8)
        nurseTalk(3)
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
    elif m == 'cinnabar_pokecenter':
        walk("a", 3)
        walk("s", 1)
        walk("d", 3)
        sleep(2)
        walk("s", 2)
        walk("a", 2)
        walk("s", 5)
        walk("s", 6)
        walk("d", 4)
        walk("w", 3)
        sleep(2)
    elif m == 'cinnabar_mansion':
        walk("s", 1)
        walk("a", 4)
        walk("w", 8)
        walk("d", 3)
        walk("w", 6)
        walk("d", 3)
        walk("a", 1)
        walk("w", 2)



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
        sleep(300)
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
    Bot.walk = 'ad'
    Bot.command = 'fight_1'
    #Bot.command = 'catch'
    Bot.location = 'cinnabar'
    #Bot.location ='pokemon_tower'

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