import copy

import Global
import constant
from Mario import *
from Block import *
from Button import *
from Item import *


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

pushing_mode = (lambda mx, my: 0)   # 0: nothing, 1: push_in_blocks, 2:push_in_block, 3: push_enemies
pushing_txt = "2 425 225 0 0"

edit_obj_kind = 0
edit_obj_buttons = [
    None,
    [  # 블럭 버튼들
        EditBlockButton(25, constant.screen_h - 25, 1, 0),
        EditBlockButton(75, constant.screen_h - 25, 1, 1),
        EditBlockButton(125, constant.screen_h - 25, 2, 0),
        EditBlockButton(175, constant.screen_h - 25, 2, 1),
    ],
    [
        EditItemButton(25, constant.screen_h - 25, 1),
    ],
]

def enter():
    global background_img, mario, blocks, enemies, window_points, camera_center, edit_obj_buttons
    background_img = load_image('ImageFolder/Title_Img.png')
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

    #



def exit():
    global background_img, mario, blocks, enemies, window_points, camera_center
    # 파일에 저장하기
    del background_img, mario, blocks, enemies, window_points, camera_center


def handle_events():
    global mario, camera_center, pushing_mode, edit_obj_kind

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()

        elif event.type == SDL_MOUSEMOTION:
            mouse_x = event.x + Global.camera.left
            mouse_y = constant.screen_h - event.y + Global.camera.bottom
            search_mouse_on_block(mouse_x, mouse_y)

        elif event.type == SDL_MOUSEBUTTONDOWN:
            mouse_x = event.x + Global.camera.left
            mouse_y = constant.screen_h - event.y + Global.camera.bottom
            if event.button == SDL_BUTTON_LEFT:
                is_click_button = False
                if edit_obj_kind != 0:
                    for edit_obj_button in edit_obj_buttons[edit_obj_kind]:
                        if edit_obj_button.onClick(mouse_x, mouse_y):
                            is_click_button = True

                if not is_click_button:  # 버튼 아이콘을 선택했을땐 오브젝트를 설치하지 않는다.
                    pushing_mode(mouse_x, mouse_y)
            elif event.button == SDL_BUTTON_RIGHT:
                pop_obj(mouse_x, mouse_y)

        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.pop_state()
                break
            elif event.key == SDLK_p:
                save_blocks('DataFolder/stage' + str(Global.play_stage_number) + '_blocks.txt')
            elif event.key == SDLK_w:
                move_camera_center(0, +100)
            elif event.key == SDLK_a:
                move_camera_center(-100, 0)
            elif event.key == SDLK_s:
                move_camera_center(0, -100)
            elif event.key == SDLK_d:
                move_camera_center(+100, 0)
            elif event.key == SDLK_BACKQUOTE:
                edit_obj_kind = 0
                pushing_mode = (lambda mx, my: 0)
            elif event.key == SDLK_1:
                edit_obj_kind = 1
            elif event.key == SDLK_2:
                edit_obj_kind = 2


def draw():
    global background_img, mario, blocks, edit_obj_buttons
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
    # 오브젝트 버튼 그리기
    if edit_obj_kind != 0:
        for edit_obj_button in edit_obj_buttons[edit_obj_kind]:
            edit_obj_button.draw_edit()

    update_canvas()


def update():
    global camera_center
    Global.camera.set_pos(camera_center)

    if edit_obj_kind != 0:
        for edit_obj_button in edit_obj_buttons[edit_obj_kind]:
            edit_obj_button.update()

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
        if block.pos.y - block.pos.h / 2 <= my <= block.pos.y + block.pos.h / 2 and block.pos.x - block.pos.w / 2 <= mx <= block.pos.x + block.pos.w / 2:
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


def move_camera_center(x, y):
    global camera_center
    if x != 0:
        camera_center.x += x
        if camera_center.x < Global.camera.left_min + constant.screen_w/2:
            camera_center.x = Global.camera.left_min + constant.screen_w/2
        elif camera_center.x > Global.camera.right_max - constant.screen_w/2:
            camera_center.x = Global.camera.right_max - constant.screen_w/2
    elif y != 0:
        camera_center.y += y
        if camera_center.y < Global.camera.bottom_min + constant.screen_h/2:
            camera_center.y = Global.camera.bottom_min + constant.screen_h/2
        elif camera_center.y > Global.camera.top_max - constant.screen_h/2:
            camera_center.y = Global.camera.top_max - constant.screen_h/2


def save_blocks(file_name):
    global blocks
    f = open(file_name, 'w', encoding='UTF8')
    f.write("(첫줄은 카메라 영역) 블럭(클래스)의 종류, x, y, hidden, item_num, 아이템들....저장\n")

    # 블럭리스트 정렬
    blocks.sort(key=lambda a: a.pos.x)

    # 블럭리스트 저장
    for block in blocks:
        f.write(block.save())

    # 블럭리스트 x 좌표로 정렬
    f.close()
    return blocks


def push_block(mx, my):
    global mouse_on_block, blocks

    new_block = load_block(pushing_txt)
    new_block.pos.x = (int(mx) // 50) * 50 + 25
    new_block.pos.y = (int(my) // 50) * 50 + 25

    # print('중복블럭 제거완료')
    if mouse_on_block is not None:
        blocks.remove(mouse_on_block)

    # print('블럭 삽입완료')
    blocks.append(new_block)
    blocks.sort(key=lambda a: a.pos.x)


def push_item(mx, my):
    global mouse_on_block

    if mouse_on_block is not None:
        mouse_on_block.item_queue.append(make_item_from_block(int(pushing_txt), mouse_on_block))


def pop_obj(mx, my):
    global mouse_on_block
    if mouse_on_block is not None:
        blocks.remove(mouse_on_block)
        mouse_on_block = None

