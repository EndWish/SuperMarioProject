import Global
import constant
from Button import *

import game_framework
from pico2d import *


name = "MapState"
background_img = None
nodeLine_img = None
stageButtons = []
stageNodeLines = []


def enter():
    global background_img, nodeLine_img, stageButtons, stageNodeLines
    background_img = load_image('BackgroundMap_Img.png')
    nodeLine_img = load_image('NodeLine_Img.png')

    stageButtons, stageNodeLines = Load_stageButtons()


def exit():
    global background_img, nodeLine_img
    del background_img, nodeLine_img


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.quit()
        elif (event.type, event.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT):
            # 왼쪽 마우스 클릭
            for stageButton in stageButtons:
                stageButton.onClick(event.x, constant.screen_h - event.y)



def draw():
    global background_img
    clear_canvas()

    # 배경그리기
    background_img.draw(constant.screen_w // 2, constant.screen_h // 2, constant.screen_w, constant.screen_h)

    # 간서 - 버튼 그리기
    for stageNodeLine in stageNodeLines:
        nodeLine_img.composite_draw(stageNodeLine[0], '', stageNodeLine[1], stageNodeLine[2], stageNodeLine[3], 5)
    for stageButton in stageButtons:
        stageButton.draw()


    update_canvas()


def update():

    pass


def pause():
    pass


def resume():
    pass







