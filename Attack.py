from Position import *
from Animation import *

import constant
import play_state


class Attack:
    def __init__(self):
        self.pos = None
        self.animator = None

    def update(self):
        pass

    def crash_enemies(self):
        pass

    def draw(self):
        pass


class FireBall(Attack):
    def __init__(self, pos, dir):
        super().__init__()
        self.pos = Position(pos.x, pos.y, 25, 25)
        self.dir = dir
        self.animator = SingleIndexAnimation(Global.attack_img, 0, 0, 8, 8, 20, 20)
        self.life_time = 1

        self.rotate = 0
        self.spin_power = 30
        self.speed = 700
        self.v_speed = 500
        self.landing = False

    def update(self):
        delta_time = Global.delta_time

        self.rotate += self.spin_power * Global.delta_time * self.dir * -1
        self.move()
        if self.crash_enemies():
            return

        self.life_time -= delta_time
        if self.life_time <= 0:
            play_state.attacks.remove(self)
            return

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
                    self.v_speed = 500
                    self.landing = True
                else:  # 위쪽 충돌 확인
                    target_pos.y -= col_xy[1] - 1
                    self.v_speed = 0

        self.pos.y = target_pos.y
        play_state.add_collision_range(target_pos)

    def crash_enemies(self):
        for enemy in play_state.enemies:
            col_xy = self.pos.collide_pos(enemy.pos)
            if col_xy != (0, 0):    # 충돌 했을 경우
                enemy.attacked(1)
                play_state.attacks.remove(self)
                return True

        return False

    def draw(self):
        self.animator.draw(self.pos.x, self.pos.y, '', self.rotate)
