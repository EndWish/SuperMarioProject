import Global
import constant
import play_state

from Animation import print_numbers

import game_framework
from pico2d import *

import map_state

name = "ClearState"
image = None
image_alpha = 0


def enter():
    global image, image_alpha
    image = load_image('ImageFolder/Clear_Img.png')
    image_alpha = 0

def exit():
    global image
    del image


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()


def draw():
    global image
    clear_canvas()
    image.draw(constant.screen_w // 2, constant.screen_h // 2, constant.screen_w, constant.screen_h)

    print_numbers(play_state.score, constant.screen_w/2 - 100, constant.screen_h/2 - 100, 50)

    update_canvas()


def update():
    global image, image_alpha
    image_alpha += Global.delta_time
    image.opacify(min(image_alpha, 1.0))

    if image_alpha > 2.5:
        # 스테이지 클리어로 바꾸기
        map_state.stageButtons[Global.play_stage_number].clear_stage()
        game_framework.pop_state()
        game_framework.pop_state()
        return


def pause():
    pass


def resume():
    pass







