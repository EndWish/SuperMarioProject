import Global
import constant
from Mario import *

import game_framework
from pico2d import *


name = "PlayState"
background_img = None


mario = None
blocks = []
items = []
effects = []
enemies = []
attacks = []


def enter():
    global background_img, mario
    background_img = load_image('Title_Img.png')
    # 마리오
    mario = Mario(100, 100)
    # 블럭

    # 아이템

    # 적



def exit():
    global background_img, mario
    del background_img, mario


def handle_events():
    global mario

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_RIGHT:
                mario.add_dir(+1)
            elif event.key == SDLK_LEFT:
                mario.add_dir(-1)

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                mario.add_dir(-1)
            elif event.key == SDLK_LEFT:
                mario.add_dir(+1)




def draw():
    global background_img
    clear_canvas()
    # 배경 그리기
    background_img.draw(constant.screen_w // 2, constant.screen_h // 2, constant.screen_w, constant.screen_h)
    # 블럭 그리기
    
    # 적 그리기
    
    # 마리오 그리기
    mario.draw()
    # 아이템 그리기
    
    # 이펙트 그리기

    # 공격 그리기

    update_canvas()


def update():
    mario.move()
    pass


def pause():
    pass


def resume():
    pass







