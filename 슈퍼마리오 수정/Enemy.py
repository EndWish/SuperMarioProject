import Global
import constant
from Animation import *
from Position import *

import play_state


class Enemy:
    def enemy_number(self):
        return 0

    def __init__(self):
        self.life = None
        self.animator = None
        self.pos = None
        self.dir = 0
        self.speed = 150
        self.v_speed = 0
        self.landing = False
        self.flip = ''

    def draw(self):
        self.animator.draw(self.pos.x, self.pos.y, self.flip)

    def draw_edit(self):
        self.animator.draw(self.pos.x, self.pos.y, '')

    def update(self):
        pass

    def save(self):
        txt = "%d %d %d\n" % (self.enemy_number(), self.pos.x, self.pos.y)
        return txt


class Goomba(Enemy):
    def enemy_number(self):
        return 1

    def __init__(self, pos):
        super().__init__()
        self.animator = OriginAnimation(Global.enemy_img, 0, 0, 18, 18, 50, 50, 2, 20, 0.5)
        self.pos = Position(float(pos.x), float(pos.y), 47, 47)
        self.dir = 0
        self.speed = 150
        self.v_speed = 0
        self.landing = False

    def update(self):
        pass

    def move(self):
        delta_time = Global.delta_time

        # 좌우 이동
        target_pos = Position(self.pos.x + self.speed * self.dir * delta_time, self.pos.y, self.pos.w, self.pos.h)
        check_blocks = play_state.get_check_blocks(target_pos)

        # target_pos 와 부딪히면 벽이 있는지 확인
        for block in check_blocks:
            play_state.add_collision_range(block.pos)
            col_xy = target_pos.collide_pos(block.pos)
            if col_xy != (0, 0) and not block.hidden:
                target_pos.x -= col_xy[0]
                self.dir *= -1

        self.pos.x = target_pos.x

        # 낙하&점프
        self.v_speed -= constant.mario_gravity * delta_time
        if self.v_speed < constant.mario_min_v_speed:  # 낙하 최대속도 조정
            self.v_speed = constant.mario_min_v_speed

        target_pos = Position(self.pos.x, self.pos.y + self.v_speed * delta_time, self.pos.w, self.pos.h + 2)
        check_blocks = play_state.get_check_blocks(target_pos)
        # target_pos 와 부딪히면 벽이 있는지 확인
        self.landing = False
        for block in check_blocks:
            play_state.add_collision_range(block.pos)
            col_xy = target_pos.collide_pos(block.pos)
            if col_xy != (0, 0):
                if self.v_speed:  # 아래쪽 충돌 확인
                    if block.hidden:
                        continue
                    target_pos.y -= col_xy[1] + 1
                    self.v_speed = 0
                    self.landing = True
                else:  # 위쪽 충돌 확인
                    target_pos.y -= col_xy[1] - 1
                    self.v_speed = 0

        self.pos.y = target_pos.y
        play_state.add_collision_range(target_pos)

        # 좌우반전
        if self.speed > 0 and self.flip == 'h':
            self.flip = ''
        elif self.speed < 0 and self.flip == '':
            self.flip = 'h'


def load_enemy(txt):
    txt = list(map(int, txt.split()))
    if txt[0] == 1:
        return Goomba(Position(txt[1], txt[2], 47, 47))


def Load_enemies(file_name):
    enemies = []
    f = open(file_name, 'r', encoding='UTF8')
    f.readline()  # 첫줄 (설명라인) 제거

    # 블럭리스트 생성
    while True:
        line = f.readline()
        if not line: break
        enemy = load_enemy(line)
        enemies.append(enemy)

    f.close()
    return enemies

