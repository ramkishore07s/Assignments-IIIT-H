import getch
import os
import time

def start(level):
    os.system('clear')
    time.sleep(0.5)
    print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
    print("                                                                                          BOMBERMAN")
    time.sleep(0.5)
    print("                                                                                           LEVEL  " + str(level))
    time.sleep(0.5)
    print("                                                                                   press any key to start")
    time.sleep(0.5)
    print("                                                                                     press 1 to quit")
    time.sleep(0.5)
    print("                                                                                     press 2 for info")
    print("\n"*8)
    print("                                                                                         move : WSAD")
    print("                                                                                         powerup : P")
    print("                                                                                          bomb: B")
    key = getch.getch()
    if key is '1':
        return 0
    if key is '2':
        os.system('clear')
        print("\n"*3)
        print("* Developed and Tested on Mac OS X v.10.12.6")
        print("* Not tested on Linux or Windows, this may not work on Windows")
        print("* Note:")
        print(" ~ Only one powerup per level")
        print(" ~ Only two types of powerups, one slows down enemies, one makes players life infinite")
        print(" ~ The game ends on level 4")
        print("\n"*12)
        print(" "*60 + "press any key to start")
        getch.getch()
        return 1
    else:
        return 1


def lose():
    os.system('clear')
    print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
    print("                                                                                           you lose :(")
    return 0


def win():
    os.system('clear')
    print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
    print("                                                                                           you win :)")
    return 0
