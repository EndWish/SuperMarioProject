import Global
import constant

import map_state
import game_framework
from pico2d import *


name = "TitleState"
image = None
image2 = None
image2_alpha = 1.0
image2_frame = 0


def enter():
    global image, image2
    image = load_image('ImageFolder/Title_Img.png')
    image2 = load_image('ImageFolder/TitleSentence_Img.png')


def exit():
    global image, image2
    del image, image2


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif event.type == SDL_KEYDOWN:
                game_framework.change_state(map_state)


def draw():
    global image
    clear_canvas()
    image.draw(constant.screen_w // 2, constant.screen_h // 2, constant.screen_w, constant.screen_h)
    image2.draw(constant.screen_w // 2, constant.screen_h // 6, constant.screen_w // 5, constant.screen_h // 21)
    update_canvas()


def update():
    global image2_frame, image2_alpha
    image2_frame += Global.delta_time
    image2_alpha = abs(math.sin(image2_frame))
    image2.opacify(image2_alpha)
    pass


def pause():
    pass


def resume():
    pass







