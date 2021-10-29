import Global
import constant
from Position import *
from Animation import *


class Mario:

    def __init__(self, x, y):
        self.life = 3
        self.pos = Position(x, y, 50, 50)
        self.mode = 0

        self.dir = 0  # 방향키를 눌렀는지 (1 = right 키, -1 = left 키)
        self.speed = 0
        self.v_speed = 0
        self.landing = True

        # 드로우 관련 변수
        self.draw_mode = 0
        self.change_mode = 0
        self.change_time = 100
        self.flip = ''
        self.motion = 0
        self.animator = [
            [
                SingleIndexAnimation(Global.player_img, 0, 0, 18, 18, 50, 50),  # idle : 0
                SingleIndexAnimation(Global.player_img, 20, 0, 18, 18, 50, 50),  # jump : 1
                OriginAnimation(Global.player_img, 4, 40, 0, 18, 18, 20, 50, 50, 0.05),  # run : 2
                SingleIndexAnimation(Global.player_img, 120, 0, 18, 18, 50, 50),  # turn : 3
            ],
            [
                SingleIndexAnimation(Global.player_img, 0, 20, 18, 36, 50, 100),  # idle : 0
                SingleIndexAnimation(Global.player_img, 20, 20, 18, 36, 50, 100),  # jump : 1
                OriginAnimation(Global.player_img, 4, 40, 20, 18, 36, 20, 50, 100, 0.05),  # run : 2
                SingleIndexAnimation(Global.player_img, 120, 20, 18, 36, 50, 100),  # turn : 3
            ],
        ]


    def move(self):
        # 움직일수 없는 조건을 함수로 제공하여 리턴

        delta_time = Global.delta_time
        print(delta_time)

        # 속도계산
        if self.dir == 1:  # 오른쪽키(+가속)
            self.speed += constant.mario_accel * delta_time
            if self.speed < 0:
                self.speed += constant.mario_retar * delta_time
        elif self.dir == -1:  # 왼쪽키(-가속)
            self.speed -= constant.mario_accel * delta_time
            if self.speed > 0:
                self.speed -= constant.mario_retar * delta_time
        else:  # 아무키도 안눌렀을 경우(0으로 감속)
            if self.speed >= constant.mario_retar * delta_time:
                self.speed -= constant.mario_retar * delta_time
            elif self.speed <= -constant.mario_retar * delta_time:
                self.speed += constant.mario_retar * delta_time
            else:
                self.speed = 0

        # 속도제한 하기
        if self.speed > constant.mario_max_speed:
            self.speed = constant.mario_max_speed
        elif self.speed < -constant.mario_max_speed:
            self.speed = -constant.mario_max_speed

        # 좌우반전
        if self.speed > 0 and self.flip == 'h':
            self.flip = ''
        elif self.speed < 0 and self.flip == '':
            self.flip = 'h'

        # 이동
        self.pos.x += self.speed * delta_time

        target_pos = Position(self.pos.x + self.speed * delta_time, self.pos.y, self.pos.w, self.pos.h )
        # target_pos 와 부딪히면 벽이 있는지 확인

    def draw(self):
        self.animator[self.draw_mode][self.motion].draw(self.pos.x, self.pos.y, self.flip)

    def add_dir(self, d):
        self.dir += d












