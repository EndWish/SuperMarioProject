import Global
import constant

import game_framework
from pico2d import *


name = "PlayState"
background_img = None


def enter():
    global background_img
    background_img = load_image('Title_Img.png')


def exit():
    global background_img
    del background_img


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()


def draw():
    global background_img
    clear_canvas()
    background_img.draw(constant.screen_w // 2, constant.screen_h // 2, constant.screen_w, constant.screen_h)
    update_canvas()


def update():
    pass


def pause():
    pass


def resume():
    pass







