import constant
import Global
import random
from Position import *
from Animation import *
from Effect import *
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

    def draw_edit(self, x, y):
        self.animator.draw(x, y, self.flip)

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
            if self.rise == 0:
                Global.itemSprouting_wav.play(1)
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

    def crash_mario(self):
        col_xy = self.pos.collide_pos(play_state.mario.pos)
        if col_xy != (0, 0):
            play_state.mario.upgrade_change_mode(1)
            play_state.items.remove(self)


class LifeUpMushroom(Item):
    def item_number(self):
        return 2

    def __init__(self, pos):
        super().__init__()
        self.animator = SingleIndexAnimation(Global.item_img, 40, 0, 18, 18, 50, 50)
        self.pos = Position(float(pos.x), float(pos.y), 47, 47)
        self.mode = 0
        self.dir = 0
        self.speed = 200
        self.v_speed = 0
        self.landing = False

        self.rise = 0

    def update(self):
        delta_time = Global.delta_time

        if self.mode == 0:  # 블럭에서 생성되서 나타날때
            if self.rise == 0:
                Global.itemSprouting_wav.play(1)
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

    def crash_mario(self):
        col_xy = self.pos.collide_pos(play_state.mario.pos)
        if col_xy != (0, 0):
            play_state.mario.life += 1
            play_state.items.remove(self)
            Global.oneUp_wav.play(1)


class FireFlower(Item):
    def item_number(self):
        return 3

    def __init__(self, pos):
        super().__init__()
        self.animator = OriginAnimation(Global.item_img, 0, 40, 18, 18, 50, 50, 3, 20, 0.1)
        self.pos = Position(float(pos.x), float(pos.y), 47, 47)
        self.mode = 0
        self.v_speed = 0

        self.rise = 0

    def update(self):
        delta_time = Global.delta_time

        if self.mode == 0:  # 블럭에서 생성되서 나타날때
            if self.rise == 0:
                Global.itemSprouting_wav.play(1)
            self.v_speed = 100
            self.pos.y += self.v_speed * delta_time
            self.rise += self.v_speed * delta_time
            if self.rise >= 50:
                self.mode = 1

        elif self.mode == 1:    # 일반적인 상황
            self.base_move()
            self.crash_mario()

    def base_move(self):
        pass

    def crash_mario(self):
        col_xy = self.pos.collide_pos(play_state.mario.pos)
        if col_xy != (0, 0):
            play_state.mario.upgrade_change_mode(2)
            play_state.items.remove(self)


class Coin(Item):
    def item_number(self):
        return 4

    def __init__(self, pos):
        super().__init__()
        self.animator = OriginAnimation(Global.item_img, 0, 60, 11, 16, 33, 48, 6, 20, 0.05)
        self.pos = Position(float(pos.x), float(pos.y), 33, 48)
        self.mode = 0
        self.v_speed = 0
        self.life_time = 0.3

        self.rise = 0

    def update(self):
        delta_time = Global.delta_time

        if self.mode == 0:  # 블럭에서 생성되서 나타날때
            self.v_speed = 800
            self.pos.y += self.v_speed * delta_time
            self.rise += self.v_speed * delta_time
            if self.rise >= 50:
                self.mode = 1

        elif self.mode == 1:    # 일반적인 상황
            self.base_move()
            self.crash_mario()
            self.life_time -= delta_time
            if self.life_time <= 0:
                play_state.score += 100
                play_state.items.remove(self)
                Global.coin_wav.play(1)

    def base_move(self):
        delta_time = Global.delta_time

        # 낙하&점프
        self.v_speed -= constant.mario_gravity * delta_time
        if self.v_speed < constant.mario_min_v_speed:  # 낙하 최대속도 조정
            self.v_speed = constant.mario_min_v_speed

        self.pos.y += self.v_speed * delta_time

    def crash_mario(self):
        col_xy = self.pos.collide_pos(play_state.mario.pos)
        if col_xy != (0, 0):
            play_state.score += 100
            play_state.items.remove(self)
            Global.coin_wav.play(1)


class SuperStar(Item):
    def item_number(self):
        return 5

    def __init__(self, pos):
        super().__init__()
        self.animator = OriginAnimation(Global.item_img, 0, 20, 16, 18, 50, 50, 4, 20, 0.1)
        self.pos = Position(float(pos.x), float(pos.y), 47, 47)
        self.mode = 0
        self.v_speed = 0

        self.rise = 0

    def update(self):
        delta_time = Global.delta_time

        if self.mode == 0:  # 블럭에서 생성되서 나타날때
            if self.rise == 0:
                Global.itemSprouting_wav.play(1)
            self.v_speed = 100
            self.pos.y += self.v_speed * delta_time
            self.rise += self.v_speed * delta_time
            if self.rise >= 50:
                self.mode = 1

        elif self.mode == 1:    # 일반적인 상황
            self.base_move()
            self.crash_mario()

    def base_move(self):
        pass

    def crash_mario(self):
        col_xy = self.pos.collide_pos(play_state.mario.pos)
        if col_xy != (0, 0):
            play_state.mario.set_invincible(10)
            play_state.mario.super_invincible = 10
            play_state.effects.append(SuperStarLightEffect())
            play_state.items.remove(self)

def make_item_from_block(number, block):
    if number == 1:
        return SuperMushroom(block.pos)
    elif number == 2:
        return LifeUpMushroom(block.pos)
    elif number == 3:
        return FireFlower(block.pos)
    elif number == 4:
        return Coin(block.pos)
    elif number == 5:
        return SuperStar(block.pos)
