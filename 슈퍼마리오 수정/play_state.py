import Global
import constant
from Mario import *
from Block import *

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

score = 0

collisions_range = set()

def enter():
    global background_img, mario, blocks, items, enemies, attacks, effects
    background_img = load_image('ImageFolder/Title_Img.png')
    # 카메라 정보 가져오기
    Global.camera.load_window_max('DataFolder/stage' + str(Global.play_stage_number) + '_camera.txt')
    # 마리오
    mario = Mario(100.0, 100.0)
    # 블럭
    blocks = Load_blocks('DataFolder/stage' + str(Global.play_stage_number) + '_blocks.txt')
    # 아이템
    items = []
    # 적
    enemies = []

    # 그 외
    attacks = []
    effects = []


def exit():
    global background_img, mario, blocks, items, effects, enemies, attacks
    del background_img, mario, blocks, items, effects, enemies, attacks


def handle_events():
    global mario

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.pop_state()
                break
            elif event.key == SDLK_RIGHT:
                mario.add_dir(+1)
            elif event.key == SDLK_LEFT:
                mario.add_dir(-1)
            elif event.key == SDLK_UP:
                mario.jump_key = True
            elif event.key == SDLK_p:
                Global.show_collide_rec = not Global.show_collide_rec

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                mario.add_dir(-1)
            elif event.key == SDLK_LEFT:
                mario.add_dir(+1)
            elif event.key == SDLK_UP:
                mario.jump_key = False


def draw():
    global background_img, mario, blocks
    clear_canvas()
    # 배경 그리기
    background_img.draw(constant.screen_w // 2, constant.screen_h // 2, constant.screen_w, constant.screen_h)
    # 블럭 그리기
    for block in blocks:
        block.draw()
    # 적 그리기
    
    # 마리오 그리기
    mario.draw()
    # 아이템 그리기
    for item in items:
        item.draw()
    # 이펙트 그리기
    for effect in effects:
        effect.draw()
    # 공격 그리기
    
    # 충돌범위 그리기
    for collision in collisions_range:
        collision.draw_collision_rect()
    collisions_range.clear()

    update_canvas()


def update():
    mario.move()

    for item in items:
        item.update()

    for effect in effects:
        effect.update()

    # 카메라 위치 설정
    Global.camera.set_pos(mario.pos)

def pause():
    pass


def resume():
    pass


def get_check_blocks(pos):
    global blocks

    obj_left = pos.x - pos.w / 2
    obj_right = pos.x + pos.w / 2
    s = 0
    e = len(blocks) - 1
    while s != e:
        middle = (s + e) // 2
        if blocks[middle].pos.x + blocks[middle].pos.w / 2 < obj_left:
            s = middle + 1
        else:
            e = middle
    index_left = e

    s = 0
    e = len(blocks) - 1
    while s != e:
        middle = math.ceil((s + e) / 2)
        if blocks[middle].pos.x - blocks[middle].pos.w / 2 < obj_right:
            s = middle
        else:
            e = middle - 1
    index_right = e

    return blocks[index_left:index_right + 1]


def add_collision_range(pos):
    if Global.show_collide_rec:
        collisions_range.add(pos)


def add_score(value):
    global score
    score += value

