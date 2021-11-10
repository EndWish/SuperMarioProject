import Global
import constant

import map_state
import game_framework
from pico2d import *


name = "GameoverState"
image = None
image_alpha = 0


def enter():
    global image, image_alpha
    image = load_image('ImageFolder/GameOver_Img.png')
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
            elif event.type == SDL_KEYDOWN:
                game_framework.change_state(map_state)


def draw():
    global image
    clear_canvas()
    # game_framework.stack[-2].draw()
    image.draw(constant.screen_w // 2, constant.screen_h // 2, constant.screen_w, constant.screen_h)
    update_canvas()


def update():
    global image, image_alpha
    image_alpha += Global.delta_time
    image.opacify(min(image_alpha, 1.0))

    if image_alpha > 3:
        game_framework.pop_state()
        game_framework.pop_state()
        return


def pause():
    pass


def resume():
    pass







