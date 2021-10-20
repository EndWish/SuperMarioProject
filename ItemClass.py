from AnimationClass import *
from PositionClass import *
import copy
import StageClass


class Item:
    image_sheet = load_image("ItemImg.png")
    item_images = [
        Ani(image_sheet, 1, 0, 0, 18, 18, 0, 50, 50),   # 0
        Ani(image_sheet, 1, 40, 0, 18, 18, 0, 50, 50),   # 1
        Ani(image_sheet, 1, 80, 0, 18, 18, 0, 50, 50),   # 2
        Ani(image_sheet, 4, 0, 20, 16, 20, 20, 50, 50),   # 3
        Ani(image_sheet, 4, 0, 40, 18, 18, 20, 50, 50),  # 4
    ]

    def __init__(self, kind, pos):
        self.kind = kind    # 0 == 슈퍼버섯, 1 == 1up 버섯, 2 == 독버섯,  3 == 슈퍼스타, 4 == 플라워
        self.pos = pos
        self.motion = 0

        self.dir = 1
        self.v_speed = 0
        self.landing = True

        # 아이템 종류에 따른 필요한 변수들 추가
        if self.kind == 0:
            self.rise_y = 0

    def draw(self):
        Item.item_images[self.kind].draw(self.pos.x, self.pos.y, '')

    def create_clone(self):
        return copy.deepcopy(self)

    def collide_with_block(self, block):
        # 오른쪽과 왼쪽 충돌확인
        middle_pos = Position(self.pos.x, self.pos.y, self.pos.w, self.pos.h / 2)

        draw_rectangle(middle_pos.x - middle_pos.w/2, middle_pos.y - middle_pos.h/2, middle_pos.x + middle_pos.w/2, middle_pos.y + middle_pos.h/2)
        col_xy1 = middle_pos.collide_pos(block.pos)
        if col_xy1 != (0, 0):
            self.pos.x = self.pos.x - col_xy1[0]
            self.dir *= - 1

        # 아래쪽 충돌확인
        under_pos = Position(self.pos.x, self.pos.y - self.pos.h/2 - 1, self.pos.w * 0.8, 1)

        draw_rectangle(under_pos.x - under_pos.w/2, under_pos.y - under_pos.h/2, under_pos.x + under_pos.w/2, under_pos.y + under_pos.h/2)
        col_xy = under_pos.collide_pos(block.pos)
        if col_xy != (0, 0):
            self.pos.y = int(self.pos.y - (col_xy[1] + 1))
            self.landing = True

    def collide_with_blocks(self):
        # 이진탐색으로 마리오 근처의 블럭으로 범위 좁히기
        index_left, index_right = StageClass.stage.can_crash_black_search(self.pos)

        # 좁힌 범위에서 충돌 체크하기
        self.landing = False  # 각각의 블록과 충돌하기전 landing 을 False 로 초기화, 마리오가 하나의 블록이라도 위에 있다면 landing = True
        for b in StageClass.stage.blocks[index_left:index_right + 1]:
            if b.active:
                draw_rectangle(b.pos.x - b.pos.w / 2, b.pos.y - b.pos.h / 2, b.pos.x + b.pos.w / 2,
                               b.pos.y + b.pos.h / 2)
                self.collide_with_block(b)

    def collide_with_mario(self):
        col_xy = self.pos.collide_pos(StageClass.stage.mario.pos)
        if col_xy != (0, 0):
            # 마리오와 출돌했을 경우
            if self.kind == 0:
                StageClass.stage.mario.change_mode = 1
                # 슈퍼버섯일때
                pass

            # 아이템 삭제를 위해 True 리턴
            return True

        return False

    def super_mushroom_running(self):
        # 아이템이 생성될때
        if self.motion == 0:
            if self.rise_y < 50:
                self.pos.y += 1
                self.rise_y += 1
            else:
                self.motion = 1
        # 좌우로 돌아다닐때
        elif self.motion == 1:
            # 움직이고
            self.pos.x += 2 * self.dir
            if self.landing:
                self.v_speed = 0
            else:
                self.v_speed -= 0.5
                if self.v_speed < -15:
                    self.v_speed = -15
                self.pos.y += self.v_speed

            # 충돌체크
            self.collide_with_blocks()

    def running_del(self):
        # 슈퍼 버섯
        if self.kind == 0:
            self.super_mushroom_running()

        return self.collide_with_mario()


