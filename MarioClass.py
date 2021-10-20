from pico2d import *
from AnimationClass import *
from PositionClass import *


class Mario:
    image_sheet = load_image('ObjectImg.png')

    def __init__(self, x=0, y=0):
        self.life = 3
        self.pos = Position(x, y, 50, 50)
        self.life = 5
        self.mode = 0
        self.current_mode = 0
        self.change_mode = 0
        self.change_time = 100
        self.landing = True

        self.motion = 0
        self.animator = [
            [
                Ani(Mario.image_sheet, 1, 0, 0, 18, 18, 20, 50, 50),  # idle : 0
                Ani(Mario.image_sheet, 1, 20, 0, 18, 18, 20, 50, 50),  # jump : 1
                Ani(Mario.image_sheet, 4, 40, 0, 18, 18, 20, 50, 50, 0.05),  # run : 2
                Ani(Mario.image_sheet, 1, 120, 0, 18, 18, 20, 50, 50),  # turn : 3
            ],
            [
                Ani(Mario.image_sheet, 1, 0, 20, 18, 36, 20, 50, 100),  # idle : 0
                Ani(Mario.image_sheet, 1, 20, 20, 18, 36, 20, 50, 100),  # jump : 1
                Ani(Mario.image_sheet, 4, 40, 20, 18, 36, 20, 50, 100, 0.05),  # run : 2
                Ani(Mario.image_sheet, 1, 120, 20, 18, 36, 20, 50, 100),  # turn : 3
            ]

        ]
        self.flip = ''

        self.dir = 0  # 방향키를 눌렀는지 (1 = right 키, -1 = left 키)
        self.speed = 0
        self.v_speed = 0

    def invincibility(self):
        if self.mode != self.change_mode:
            return True
        return False

    def change(self):
        if self.mode != self.change_mode:
            self.change_time -= 1
            if (self.change_time//20) % 2 == 0:
                self.current_mode = self.mode
            else:
                self.current_mode = self.change_mode

            if self.change_time <= 0:
                self.mode = self.change_mode
                self.current_mode = self.change_mode
                self.change_time = 100
                if self.change_mode == 1 or self.change_mode == 2:
                    self.pos.h = 100

    def draw(self):
        self.animator[self.current_mode][self.motion].draw(self.pos.x, self.pos.y, self.flip)

    def move(self):
        if self.mode != self.change_mode:
            return

        acceleration = 0.2  # 가속도
        retardation = 0.25  # 감속도
        max_speed = 8
        gravity = 0.5
        min_v_speed = -15

        # 이동
        if self.dir == 1:  # 오른쪽키(+가속)
            self.speed += acceleration
            if self.speed < 0:
                self.speed += retardation
        elif self.dir == -1:  # 왼쪽키(-가속)
            self.speed -= acceleration
            if self.speed > 0:
                self.speed -= retardation
        else:  # 아무키도 안눌렀을 경우(0으로 감속)
            if self.speed >= retardation:
                self.speed -= retardation
            elif self.speed <= -retardation:
                self.speed += retardation
            else:
                self.speed = 0

        # 속도제한 하기
        if self.speed > max_speed:
            self.speed = max_speed
        elif self.speed < -max_speed:
            self.speed = -max_speed

        # 좌우반전
        if self.speed > 0 and self.flip == 'h':
            self.flip = ''
        elif self.speed < 0 and self.flip == '':
            self.flip = 'h'

        # 모션 바꾸기
        if self.landing:
            if self.speed == 0:
                self.motion = 0
            else:   # speed != 0
                self.animator[self.mode][self.motion].time_slice_speed = abs(self.speed / max_speed) + 0.01
                if (self.speed > 0 and self.dir == -1) or (self.speed < 0 and self.dir == 1):
                    self.motion = 3
                else:
                    self.motion = 2
        else:
            self.motion = 1

        # 낙하
        if self.landing:
            self.v_speed = 0
        else:
            self.v_speed -= gravity
            if self.v_speed < min_v_speed:  # 낙하 최대속도 조정
                self.v_speed = min_v_speed
            self.pos.y += self.v_speed

        self.pos.x += self.speed

    def collide_with_block(self, block):
        if not block.active:
            return

        if self.v_speed > 0:
            # 위쪽 충돌 확인
            over_pos = Position(self.pos.x, self.pos.y + self.pos.h / 2 + 1, self.pos.w * 0.8, 1)

            draw_rectangle(over_pos.x - over_pos.w / 2, over_pos.y - over_pos.h / 2, over_pos.x + over_pos.w / 2,
                           over_pos.y + over_pos.h / 2)
            col_xy = over_pos.collide_pos(block.pos)
            if col_xy != (0, 0):
                self.pos.y = int(self.pos.y - (col_xy[1] + 1))
                # self.landing = True
                self.v_speed = 0
                block.crash()
                # 충돌한 블럭에 대한 이벤트 넣기

        if not block.visible:
            return

        # 오른쪽과 왼쪽 충돌확인
        middle_pos = Position(self.pos.x, self.pos.y, self.pos.w, self.pos.h / 2)

        draw_rectangle(middle_pos.x - middle_pos.w/2, middle_pos.y - middle_pos.h/2, middle_pos.x + middle_pos.w/2, middle_pos.y + middle_pos.h/2)
        col_xy1 = middle_pos.collide_pos(block.pos)
        if col_xy1 != (0, 0):
            self.pos.x = self.pos.x - col_xy1[0]
            self.speed = 0

        # 아래쪽 충돌확인
        under_pos = Position(self.pos.x, self.pos.y - self.pos.h/2 - 1, self.pos.w * 0.8, 1)

        draw_rectangle(under_pos.x - under_pos.w/2, under_pos.y - under_pos.h/2, under_pos.x + under_pos.w/2, under_pos.y + under_pos.h/2)
        col_xy = under_pos.collide_pos(block.pos)
        if col_xy != (0, 0):
            self.pos.y = int(self.pos.y - (col_xy[1] + 1))
            self.landing = True



