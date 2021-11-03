import random

import Global
import play_state
from Position import *
from Animation import *


class WreckageEffect:
    def __init__(self, pos):
        self.poses = [
            Position(pos.x + pos.w / 4, pos.y + pos.h / 4, pos.w, pos.h),
            Position(pos.x - pos.w / 4, pos.y + pos.h / 4, pos.w, pos.h),
            Position(pos.x - pos.w / 4, pos.y - pos.h / 4, pos.w, pos.h),
            Position(pos.x + pos.w / 4, pos.y - pos.h / 4, pos.w, pos.h),
        ]
        self.rotations = [0, 0, 0, 0]
        self.move_info = [  # x이동, y이동, 회전력
            [random.uniform(-500, 500), random.uniform(200, 1000), random.uniform(-300, 300)],
            [random.uniform(-500, 500), random.uniform(200, 1000), random.uniform(-300, 300)],
            [random.uniform(-500, 500), random.uniform(200, 1000), random.uniform(-300, 300)],
            [random.uniform(-500, 500), random.uniform(200, 1000), random.uniform(-300, 300)],
        ]
        self.animators = [
            SingleIndexAnimation(Global.structure_img, 24, 24, 8, 8, 25, 25),  # 벽돌 블럭
            SingleIndexAnimation(Global.structure_img, 16, 24, 8, 8, 25, 25),  # 벽돌 블럭
            SingleIndexAnimation(Global.structure_img, 16, 16, 8, 8, 25, 25),  # 벽돌 블럭
            SingleIndexAnimation(Global.structure_img, 24, 16, 8, 8, 25, 25),  # 벽돌 블럭
        ]

    def update(self):
        delta_time = Global.delta_time
        all_fell = True
        for i in range(4):
            if self.poses[i].y <= -50:
                continue
            self.move_info[i][1] -= 5000 * delta_time   # 중력가속도
            self.poses[i].x += self.move_info[i][0] * delta_time   # x이동
            self.poses[i].y += self.move_info[i][1] * delta_time   # y이동
            self.rotations[i] += self.move_info[i][2] * delta_time   # 회전
            all_fell = False

        if all_fell:
            play_state.effects.remove(self)

    def draw(self):
        for i in range(4):
            if self.poses[i].y <= -50:
                continue
            self.animators[i].draw(self.poses[i].x, self.poses[i].y, '', self.rotations[i])

