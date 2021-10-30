import constant
import Global
import random
from Position import *
from Animation import *
import play_state


class Item:
    def item_number(self):
        return 0

    def __init__(self):
        self.animator = None
        self.flip = ''
        self.pos = None
        pass

    def draw(self):
        self.animator.draw(self.pos.x, self.pos.y, self.flip)

    def update(self):
        pass


class SuperMushroom(Item):
    def item_number(self):
        return 1

    def __init__(self, pos):
        super(SuperMushroom, self).__init__()
        self.animator = SingleIndexAnimation(Global.item_img, 0, 0, 18, 18, 50, 50)
        self.pos = Position(float(pos.x), float(pos.y), 47, 47)
        self.mode = 0
        self.dir = 0
        self.speed = 150
        self.v_speed = 0
        self.landing = False

        self.rise = 0

    def update(self):
        delta_time = Global.delta_time

        if self.mode == 0:  # 블럭에서 생성되서 나타날때
            self.v_speed = 500
            self.pos.y += self.v_speed * delta_time
            self.rise += self.v_speed * delta_time
            if self.rise > 50:
                self.mode = 1
                self.dir = (-1, 1)[random.randint(0, 1)]

        elif self.mode == 1:    # 일반적인 상황
            self.base_move()
            self.crash_mario()

    def base_move(self):
        delta_time = Global.delta_time

        # 좌우 이동
        target_pos = Position(self.pos.x + self.speed * self.dir * delta_time, self.pos.y, self.pos.w, self.pos.h)
        check_blocks = play_state.get_check_blocks(target_pos)

        # target_pos 와 부딪히면 벽이 있는지 확인
        for block in check_blocks:
            play_state.add_collision_range(block.pos)
            col_xy = target_pos.collide_pos(block.pos)
            if col_xy != (0, 0):
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
                if self.v_speed <= 0 and (not block.hidden):  # 아래쪽 충돌 확인
                    target_pos.y -= col_xy[1] + 1
                    self.v_speed = 0
                    self.landing = True
                else:  # 위쪽 충돌 확인
                    target_pos.y -= col_xy[1] - 1
                    self.v_speed = 0
                    block.heading()

        self.pos.y = target_pos.y
        play_state.add_collision_range(target_pos)

        # 좌우반전
        if self.speed > 0 and self.flip == 'h':
            self.flip = ''
        elif self.speed < 0 and self.flip == '':
            self.flip = 'h'

    def crash_mario(self):
        col_xy = self.pos.collide_pos(play_state.mario.pos)
        if col_xy != (0, 0):
            play_state.items.remove(self)
            print('eat!')


def make_item_from_block(number, block):
    if number == 1:
        return SuperMushroom(block.pos)
