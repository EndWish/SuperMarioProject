import Global
import constant
from Mario import *
from Block import *
from Enemy import *
from Structure import *

import game_framework
import gameover_state
import clear_state
from pico2d import *


name = "PlayState"
background_img = None
heart_img = None


mario = None
blocks = []
items = []
effects = []
enemies = []
attacks = []
structures = []
flag = None

score = int()

collisions_range = set()

def enter():
    global background_img, heart_img
    global mario, blocks, items, enemies, attacks, effects, structures, flag
    background_img = load_image('ImageFolder/Background1_1_Img.png')
    heart_img = load_image('ImageFolder/Heart_Img.png')
    # 카메라 정보 가져오기
    Global.camera.load_window_max('DataFolder/stage' + str(Global.play_stage_number) + '_camera.txt')
    # 마리오
    mario = Mario(100.0, 100.0)
    # 블럭
    blocks = Load_blocks('DataFolder/stage' + str(Global.play_stage_number) + '_blocks.txt')
    # 아이템
    items = []
    # 적
    enemies = Load_enemies('DataFolder/stage' + str(Global.play_stage_number) + '_enemies.txt')
    # 구조물
    structures = Load_structures('DataFolder/stage' + str(Global.play_stage_number) + '_structures.txt')
    # 깃발
    flag = structures[0]

    # 그 외
    attacks = []
    effects = []

    Global.bgm_mp3.repeat_play()


def exit():
    global background_img, heart_img
    global mario, blocks, items, effects, enemies, attacks, flag, score
    del background_img, heart_img
    del mario, blocks, items, effects, enemies, attacks, flag
    Global.bgm_mp3.stop()
    score = 0

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
            elif event.key == SDLK_z:
                mario.attack_fireball()
            elif event.key == SDLK_p:
                Global.show_collide_rec = not Global.show_collide_rec
            elif event.key == SDLK_o:
                if Global.game_fps == 30:
                    Global.game_fps = 100
                else:
                    Global.game_fps = 30

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
    bg_h = Global.camera.top_max - Global.camera.bottom_min
    bg_w = bg_h * 512 / 432

    draw_y = Global.camera.bottom_min
    draw_x = Global.camera.left_min

    while draw_x < Global.camera.right_max:
        if Global.camera.left <= draw_x + bg_w and draw_x <= Global.camera.right:
            background_img.draw_to_origin(draw_x - Global.camera.left, draw_y - Global.camera.bottom, bg_w, bg_h)
        draw_x += bg_w

    # 블럭 그리기
    for block in blocks:
        block.draw()
    # 적 그리기
    for enemy in enemies:
        enemy.draw()
    # 마리오 그리기
    mario.draw()
    # 아이템 그리기
    for item in items:
        item.draw()
    # 이펙트 그리기
    for effect in effects:
        effect.draw()
    # 공격 그리기
    for attack in attacks:
        attack.draw()
    # 구조물 그리기
    for structure in structures:
        structure.draw()
    
    # 충돌범위 그리기
    for collision in collisions_range:
        collision.draw_collision_rect()
    collisions_range.clear()

    # UI 그리기
    heart_img.draw(30, constant.screen_h - 30, 40, 40)  # 하트
    print_numbers(mario.life, 70, constant.screen_h - 30, 30)  # 목숨 수
    print_numbers(score, constant.screen_w - 150, constant.screen_h - 30, 30)   # 점수

    update_canvas()


def update():
    for enemy in enemies:
        enemy.update()

    mario.update()

    for item in items:
        item.update()

    for attack in attacks:
        attack.update()

    for effect in effects:
        effect.update()

    # 카메라 위치 설정
    Global.camera.set_pos(mario.pos)
    
    # 게임 오버
    if mario.death:
        game_framework.push_state(gameover_state)
        return

    # 게임 클리어
    if mario.clear:
        game_framework.push_state(clear_state)
        return

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

