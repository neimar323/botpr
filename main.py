from time import sleep
from imagesearch import *
import threading
import pyautogui
from pynput import keyboard as keyboardL
import sys
from datetime import datetime
import os


class Bot:
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
    battlesBeforePokecenter = 1
    state = {
        'inBattle': False,
        'evolving': False,
        'learnMove': False,
        'fightAvaliable': False
    }



def walk(key, times=1):
    if times == 1:
        hold(key, times * 0.01)
    else:
        hold(key, times * 0.215)

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

def  verifyBattleStuck():
    if not Bot.state['inBattle']:
        return
    if not Bot.state['fightAvaliable']:
        return

    #vish
    imgClick(Bot.imageFolder + 'pokemon.png', 1, 1)
    pyautogui.typewrite('23456', 0.4)

def waitBattleMoves():
    i = 0
    while i < 6:
        if Bot.exiting:
            exit('waitBattleMoves')
        if Bot.state['fightAvaliable']:
            return
        sleep(1)
        i = i + 1

def battle():
    while True:
        if Bot.exiting:
            exit('battle')
            return
        x = 1
        while True:
            if Bot.exiting:
                exit('battle')
                return
            trySkill = False
            if not Bot.state['inBattle']:
                break
            if Bot.state['fightAvaliable']:
                if imgClick(Bot.imageFolder + 'fight.png', 1, 1):
                    sleep(0.6)
                    skill(x)
                    trySkill = True
            if not Bot.state['inBattle']:
                break
            if trySkill:
                 verifyBattleStuck()

        if not Bot.state['inBattle']:
            Bot.battles = Bot.battles + 1
            print('battles: '+str(Bot.battles))
            Bot.thingsOK = True
            return

def verifyBattle():
    if Bot.state['inBattle']:
        print("battleFound!")
        i = 0
        while i < 3:
            sleep(1)
            if Bot.state['fightAvaliable']:
                if 'fight' in Bot.command:
                     battle()
                if 'catch' in Bot.command:
                    catch()
                return
            else:
                i = i + 1

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
            verifyLearnMove()
            verifyEvolving()
            verifySituation()
            print("hunting!")

def verifyEvolving():
    if Bot.state['evolving']:
        imgClick(Bot.imageFolder + 'no.png', 1, 3, precision=0.8)

def verifyLearnMove():
    if Bot.state['learnMove']:
        imgClick(Bot.imageFolder + 'doNotLearn.png', 1, 3, precision=0.8)
        sleep(1)
        imgClick(Bot.imageFolder + 'yes.png', 1, 3, precision=0.8)


def bicycleClick():
    sleep(1)
    imgClick(Bot.imageFolder + 'bicycle.png', 1, 3, precision=0.8)
    sleep(1)

def huntLoop(pokecenterRoute, pokecenterAlgoritm, hunterRoute, bycicle=True):
    if Bot.battles > Bot.battlesBeforePokecenter:
        print('HEALING!')
        if bycicle:
            bicycleClick()
        moveTo(pokecenterRoute)
        healPokecenter(pokecenterAlgoritm)
        moveTo(hunterRoute)
        Bot.battles = 0
        Bot.loops = Bot.loops + 1
        print('Looping!!')
        if bycicle:
            bicycleClick()

def verifySituation():
    if Bot.exiting:
        exit('verifySituation')
    if Bot.battles <= Bot.battlesBeforePokecenter:
        return
    print('STARTING LOOPING!')
    i = 0
    while i < 4:
        if Bot.state['inBattle'] or Bot.state['learnMove'] or Bot.state['evolving']:
            print('LOOPING ABORTED')
            return
        sleep(1)
        i = i + 1

    if Bot.location == 'route_10':
        huntLoop('route_10_pokecenter', 'default', 'route_10')
    elif Bot.location == 'pokemon_tower':
        #i need to refactor thisss
            print('HEALING!')
            walk('d',2)
            walk('d', 2)
            nurseTalk(2)
            Bot.battles = 0
            Bot.loops = Bot.loops + 1
            print('Looping!!')
    if Bot.location == 'cinnabar':
        huntLoop('cinnabar_pokecenter', 'cinnabar_pokecenter', 'cinnabar_mansion')
    if Bot.location == 'victory_r':
        huntLoop('indigo_pokecenter', 'indigo_pokecenter', 'victory_r')


def nurseTalk():
    i = 0
    while not imgClick(Bot.imageFolder + 'yesPlease.png', 1, 1):
        i = i + 1
        pyautogui.typewrite(' ')
        sleep(0.5)
        if i > 5:
            return
    sleep(2)
    for i in range(0, 3):
        pyautogui.typewrite(' ')
        sleep(2)
        messageWindow = imagesearch(Bot.imageFolder + 'messageWindow.png', precision=0.8)
        if messageWindow is None:
            return

def healPokecenter(pokecenter='default'):
    if pokecenter == 'cinnabar_pokecenter':
        sleep(3)
        walk('w', 4)
        walk('a', 4)
        walk('w', 3)
        nurseTalk()
        walk('s', 7)
        walk('d', 4)
        sleep(3)
    elif pokecenter == 'indigo_pokecenter':
        sleep(3)
        walk('a', 6)
        walk('w', 5)
        nurseTalk()
        walk('d', 6)
        walk('s', 6)
        sleep(3)
    else:
        sleep(3)
        walk('w', 8)
        nurseTalk()
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
    elif m == 'victory_r':
        walk("s", 4)
        walk("a", 11)
        walk("s", 10)
        walk("d", 4)
        walk("s", 6)
        walk("a", 1)
        walk("s", 1)
        sleep(2)
        walk("a", 1)
        walk("s", 1)

    elif m == 'indigo_pokecenter':
        walk("d", 3)
        walk("a", 1)
        walk("w", 2)
        sleep(2)
        walk("w", 16)
        walk("d", 12)
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
        sleep(300)
        if not Bot.thingsOK:
            print("EXITING BY INACTIVITY")
            exit('exitOnError')
        elif Bot.exiting:
            exit('exitOnError')

def timePrinter():
    while True:
        print(datetime.now())
        sleep(1)
        if Bot.exiting:
            exit('timePrinter')

# def fishing():
#     while True:
#         pos = imagesearch_numLoop(Bot.imageFolder + 'fishing.png', 0.01, 10, 0.91, False)
#         if pos is not None:
#             pyautogui.press("space")

def state():
    while True:
        if Bot.exiting:
            exit('state')

        battleFound = imagesearch(Bot.imageFolder + 'battleFound.png', precision=0.8)
        Bot.state['inBattle'] = (battleFound is not None)
        if Bot.state['inBattle']:
            Bot.state['evolving'] = False
            fight = imagesearch(Bot.imageFolder + 'fight.png', precision=0.8)
            Bot.state['fightAvaliable'] = (fight is not None)
            Bot.state['learnMove'] = False

        else:
            evolving = imagesearch(Bot.imageFolder + 'evolving.png', precision=0.8)
            Bot.state['evolving'] = (evolving is not None)
            doNotLearn = imagesearch(Bot.imageFolder + 'doNotLearn.png', precision=0.8)
            Bot.state['learnMove'] = (doNotLearn is not None)
            Bot.state['fightAvaliable'] = False

        print(Bot.state)
        sleep(0.3)

def main():
    Bot.walk = 'ad'
    Bot.command = 'fight'
    #Bot.command = 'catch'
    #Bot.location ='route_10'
    #adadadBot.location ='pokemon_tower'
    #Bot.location = 'cinnabar'
    Bot.location = 'victory_r'
    Bot.battlesBeforePokecenter = 3

    t = []
    t.append(threading.Thread(target=keyboardListener, args=()))
    t.append(threading.Thread(target=hunt, args=()))
    t.append(threading.Thread(target=exitOnError, args=()))
    t.append(threading.Thread(target=timePrinter, args=()))
    t.append(threading.Thread(target=state, args=()))

    sleep(1)


    for oneT in t:
        oneT.start()

#MAIN
main()