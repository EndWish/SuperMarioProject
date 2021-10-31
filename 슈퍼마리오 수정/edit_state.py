import Global
import constant
from Mario import *
from Block import *

import game_framework
from pico2d import *

name = "Edit_State"
background_img = None

mario = None
blocks = []
enemies = []

mouse_on_block = None


def enter():
    global background_img, mario, blocks, enemies
    background_img = load_image('Title_Img.png')
    # 마리오
    mario = Mario(100.0, 100.0)
    # 블럭
    blocks = Load_blocks('stage' + str(Global.play_stage_number) + '_blocks.txt')
    # 적
    enemies = []


def exit():
    global background_img, mario, blocks, enemies
    # 파일에 저장하기
    del background_img, mario, blocks, enemies


def handle_events():
    global mario

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_MOUSEMOTION:
            search_mouse_on_block(event.x, constant.screen_h - event.y)
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.pop_state()


def draw():
    global background_img, mario, blocks
    clear_canvas()
    # 배경 그리기
    background_img.draw(constant.screen_w // 2, constant.screen_h // 2, constant.screen_w, constant.screen_h)
    # 블럭 그리기
    for block in blocks:
        block.draw_edit()
    # 적 그리기

    # 마리오 그리기
    mario.draw()
    # 아이템 그리기
    if mouse_on_block is not None:
        for i in range(len(mouse_on_block.item_queue)):
            mouse_on_block.item_queue[i].draw_edit(mouse_on_block.pos.x + i * 25, mouse_on_block.pos.y)

    # 이펙트 그리기

    # 공격 그리기

    # 충돌범위 그리기

    update_canvas()


def update():
    pass


def pause():
    pass


def resume():
    pass


def add_score(value):
    global score
    score += value


def search_mouse_on_block(mx, my):
    global mouse_on_block
    mouse_on_block = None

    check_blocks = get_check_blocks(mx, my)
    for block in check_blocks:
        if block.pos.y - block.pos.h / 2 <= my <= block.pos.y + block.pos.h / 2:
            mouse_on_block = block
            break


def get_check_blocks(mx, my):
    global blocks

    s = 0
    e = len(blocks) - 1
    while s != e:
        middle = (s + e) // 2
        if blocks[middle].pos.x + blocks[middle].pos.w / 2 < mx:
            s = middle + 1
        else:
            e = middle
    index_left = e

    s = 0
    e = len(blocks) - 1
    while s != e:
        middle = math.ceil((s + e) / 2)
        if blocks[middle].pos.x - blocks[middle].pos.w / 2 < mx:
            s = middle
        else:
            e = middle - 1
    index_right = e

    return blocks[index_left:index_right + 1]
