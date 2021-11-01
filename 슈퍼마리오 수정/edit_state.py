import Global
import constant
from Mario import *
from Block import *

import game_framework
from pico2d import *

name = "Edit_State"
background_img = None

mario = None
blocks = None
enemies = None

mouse_on_block = None
window_points = tuple()
camera_center = None

def enter():
    global background_img, mario, blocks, enemies, window_points, camera_center
    background_img = load_image('Title_Img.png')
    # 카메라 정보 가져오기
    camera_center = Position(constant.screen_w/2, constant.screen_h/2, 0, 0)
    Global.camera.load_window_max('DataFolder/stage' + str(Global.play_stage_number) + '_camera.txt')
    window_points = (Global.camera.left_min, Global.camera.bottom_min, Global.camera.right_max, Global.camera.top_max)
    Global.camera.window_expand(100)
    # 마리오
    mario = Mario(100.0, 100.0)
    # 블럭
    blocks = Load_blocks('DataFolder/stage' + str(Global.play_stage_number) + '_blocks.txt')
    # 적
    enemies = []


def exit():
    global background_img, mario, blocks, enemies, window_points, camera_center
    # 파일에 저장하기
    del background_img, mario, blocks, enemies, window_points, camera_center


def handle_events():
    global mario, camera_center

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_MOUSEMOTION:
            search_mouse_on_block(event.x + Global.camera.left, constant.screen_h - event.y + Global.camera.bottom)
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.pop_state()
            elif event.key == SDLK_w:
                camera_center.y += 100
            elif event.key == SDLK_a:
                camera_center.x -= 100
            elif event.key == SDLK_s:
                camera_center.y -= 100
            elif event.key == SDLK_d:
                camera_center.x += 100


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
    draw_rectangle(window_points[0] - Global.camera.left, window_points[1] - Global.camera.bottom, window_points[2] - Global.camera.left, window_points[3] - Global.camera.bottom)
    update_canvas()


def update():
    global camera_center
    Global.camera.set_pos(camera_center)
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
