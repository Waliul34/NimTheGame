import pygame, sys

from button import Button1
from button import Button

import random
import numpy as np

from functools import cache
from itertools import combinations

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Nim The Game")
gui_font = pygame.font.Font("assets/final_font.ttf", 30)
BG = pygame.image.load("assets/final_final.jpg")
BG = pygame.transform.scale(BG, (1280, 720))
img = pygame.image.load("assets/dice1.png")
img = pygame.transform.scale(img, (80, 50))
img.convert()
# gobal variable
human_turn = 2

# Minimax - Start

choice_of_pile = 2


def possible_new_states(state):
    piles = []
    for i in range(len(state)):
        piles.append(i)
    possible_piles = list(combinations(piles, choice_of_pile))
    for pile in possible_piles:
        for remain in range(state[pile[0]]):
            yield state[: pile[0]] + (remain,) + state[pile[0] + 1:]

        for remain in range(state[pile[1]]):  # Needed for second choice
            yield state[: pile[1]] + (remain,) + state[pile[1] + 1:]

        for remain1 in range(state[pile[0]]):  # Needed for second choice
            for remain2 in range(state[pile[1]]):
                yield state[: pile[0]] + (remain1,) + state[pile[0] + 1: pile[1]] + (remain2,) + state[pile[1] + 1:]


def evaluate(state, is_maximizing):
    if all(counters == 0 for counters in state):
        return -1 if is_maximizing else 1


@cache
def minimax(state, is_maximizing, alpha=-1, beta=1):
    if (score := evaluate(state, is_maximizing)) is not None:
        return score

    scores = []
    for new_state in possible_new_states(state):
        scores.append(score := minimax(new_state, not is_maximizing, alpha, beta))
        if is_maximizing:
            alpha = max(alpha, score)
        else:
            beta = min(beta, score)
        if beta <= alpha:
            break

    return (max if is_maximizing else min)(scores)


def best_move(state):
    return max(
        (minimax(tuple(sorted(new_state)), is_maximizing=False), new_state) for new_state in possible_new_states(state))


## Minimax - End

##GUI
def dice(string, arr_x):
    for i in range(int(len(string))):
        r2 = int(string[i])
        for j in range(r2):
            rec = img.get_rect()
            pl = 620 - (50 * j)
            rec.center = arr_x[i], pl
            SCREEN.blit(img, rec)
    pygame.display.update()


def get_font(size):
    return pygame.font.Font("assets/final_font.ttf", size)


def cal_sum(ss):
    pp = 0
    for i in range(int(len(ss))):
        pp += int(ss[i])
    return pp


def decision(strr, arr_x, player):
    remain = -1
    global human_turn
    main_menu = Button1('Play', 250, 40, (500, 400), 5, get_font(30))
    quit_button = Button1('Quit', 250, 40, (500, 500), 5, get_font(30))

    while (True):

        SCREEN.blit(BG, (0, 0))
        ## If there is no dice
        if (cal_sum(strr) == 0):
            SCREEN.blit(BG, (0, 0))
            main_menu.draw(SCREEN)
            quit_button.draw(SCREEN)

            # Human 0
            # Computer 1
            if (player == 0):
                PLAY_TEXT = get_font(45).render("Human has no options. Computer wins!!", True, "#ffffff")
                PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 160))
                SCREEN.blit(PLAY_TEXT, PLAY_RECT)
            elif (player == 1):

                PLAY_TEXT = get_font(45).render("Computer has no options. Human wins!!", True, "#ffffff")
                PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 160))
                SCREEN.blit(PLAY_TEXT, PLAY_RECT)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if main_menu.check_click() == True:
                        play()

                    if quit_button.check_click() == True:
                        pygame.quit()
                        sys.exit()
            pygame.display.update()
        # Human's Turn
        elif (player == 0):

            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONDOWN:

                    for i in range(int(len(strr))):
                        r1 = int(strr[i])
                        for j in range(r1):
                            rect = img.get_rect()
                            rect.center = arr_x[i], 620 - (50 * j)
                            if rect.collidepoint(event.pos):
                                remain = j
                                i_p = i
                                break

                if event.type == pygame.MOUSEBUTTONUP:
                    if remain >= 0:

                        strr = strr[: i_p] + str(remain) + strr[i_p + 1:]
                        dice(strr, arr_x)
                        # If it is the first move of human
                        if human_turn == 2 and cal_sum(strr) != 0:

                            human_turn = 4
                            while True:
                                MENU_MOUSE_POS = pygame.mouse.get_pos()

                                MENU_TEXT = get_font(45).render("Do you want to remove from second one?", True,
                                                                "#ffffff")

                                MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

                                SCREEN.blit(MENU_TEXT, MENU_RECT)

                                YES_BUTTON = Button(
                                    image=pygame.transform.scale(pygame.image.load("assets/Play Rect.png"), (80, 50)),
                                    pos=(500, 200),
                                    text_input="YES", font=get_font(30), base_color="#d7fcd4", hovering_color="#1bf726")

                                NO_BUTTON = Button(
                                    image=pygame.transform.scale(pygame.image.load("assets/Quit Rect.png"), (80, 50)),
                                    pos=(700, 200),
                                    text_input="NO", font=get_font(30), base_color="#d7fcd4", hovering_color="#1bf726")

                                for button in [YES_BUTTON, NO_BUTTON]:
                                    button.changeColor(MENU_MOUSE_POS)
                                    button.update(SCREEN)

                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        pygame.quit()
                                        sys.exit()
                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        if YES_BUTTON.checkForInput(MENU_MOUSE_POS):
                                            SCREEN.blit(BG, (0, 0))
                                            dice(strr, arr_x)
                                            decision(strr, arr_x, player)
                                        if NO_BUTTON.checkForInput(MENU_MOUSE_POS):
                                            decision(strr, arr_x, 1)
                                            pygame.time.delay(700)

                                pygame.display.update()

                        player = 1 - player
                        remain = -1
                        break
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        # Computers Turn
        else:
            human_turn = 2
            tup = tuple(list(int(x) for x in strr))
            bst = best_move(tup)
            lst = list(bst[1])
            strr = "".join(str(x) for x in lst)
            pygame.time.delay(1500)
            dice(strr, arr_x)
            pygame.time.delay(700)
            player = 1 - player


def piles(turn):
    PLAY_TEXT = get_font(50).render("Choose pile number", True, "#660000")
    PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 160))
    PLAY_3 = Button(image=pygame.image.load("assets/Num Rect.png"), pos=(450, 350),
                    text_input="3", font=get_font(65), base_color="White", hovering_color='#59ff62')
    PLAY_4 = Button(image=pygame.image.load("assets/Num Rect.png"), pos=(650, 350),
                    text_input="4", font=get_font(65), base_color="White", hovering_color='#59ff62')
    PLAY_5 = Button(image=pygame.image.load("assets/Num Rect.png"), pos=(850, 350),
                    text_input="5", font=get_font(65), base_color="White", hovering_color='#59ff62')
    PLAY_BACK = Button1('BACK', 250, 40, (500, 550), 5, get_font(30), )

    while True:
        SCREEN.blit(BG, (0, 0))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        PLAY_BACK.draw(SCREEN)

        PLAY_3.changeColor(PLAY_MOUSE_POS)
        PLAY_4.changeColor(PLAY_MOUSE_POS)
        PLAY_5.changeColor(PLAY_MOUSE_POS)

        PLAY_3.update(SCREEN)
        PLAY_4.update(SCREEN)
        PLAY_5.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                sz = 0
                if PLAY_BACK.check_click() == True:
                    play()
                if PLAY_3.checkForInput(PLAY_MOUSE_POS):
                    sz = 3
                if PLAY_4.checkForInput(PLAY_MOUSE_POS):
                    sz = 4
                if PLAY_5.checkForInput(PLAY_MOUSE_POS):
                    sz = 5
                if (sz in range(2, 7)):
                    place(sz, turn)
        pygame.display.update()


def play():
    SCREEN.blit(BG, (0, 0))
    
    global human_turn
    human_turn = 2

    PLAY_TEXT = get_font(60).render("Choose Turn", True, "#660000")
    PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 160))
    SCREEN.blit(PLAY_TEXT, PLAY_RECT)

    PLAY_C = Button1('Computer', 250, 40, (300, 300), 5, get_font(30))

    PLAY_H = Button1('Human', 250, 40, (700, 300), 5, get_font(30))

    PLAY_BACK = Button1('Back', 250, 40, (500, 450), 5, get_font(30))
    while True:

        PLAY_C.draw(SCREEN)
        PLAY_H.draw(SCREEN)
        PLAY_BACK.draw(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.check_click() == True:
                    main_menu()
                if PLAY_C.check_click() == True:
                    piles(1)
                if PLAY_H.check_click() == True:
                    piles(0)

        pygame.display.update()


def place(n, turn):
    SCREEN.blit(BG, (0, 0))
    arr_x = np.zeros(7)
    c = 1280 / (n + 1)
    d = c
    for i in range(n + 1):
        arr_x[i] = c
        c += d
    string = ""
    for i in range(n):
        r = int(random.randint(1, 6))
        string += str(r)
    while (1):

        SCREEN.blit(BG, (0, 0))
        dice(string, arr_x)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            else:
                decision(string, arr_x, turn)

    pygame.display.update()


def main_menu():
    MENU_TEXT = get_font(80).render("Nim The Game", True, "#660000")
    MENU_RECT = MENU_TEXT.get_rect(center=(650, 200))
    button1 = Button1('Play', 250, 40, (350, 400), 5, get_font(30))
    button2 = Button1('Quit', 250, 40, (700, 400), 5, get_font(30))

    while True:
        SCREEN.blit(BG, (0, 0))
        SCREEN.blit(MENU_TEXT, MENU_RECT)
        button1.draw(SCREEN)
        button2.draw(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button1.check_click() == True:
                    play()

                if button2.check_click() == True:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()
