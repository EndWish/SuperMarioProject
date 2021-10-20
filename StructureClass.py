import random

from pico2d import *
import math
import StageClass
from AnimationClass import *
from PositionClass import *
from ItemClass import *

"""
블럭의 종류:
무적 블럭(2가지 이미지)  kind == 0
부서지는 블럭     kind == 1
박치기로 움직이는 블럭(아이템이 안나오는 블럭)    kind == 2
박치기로 움직이는 블럭(아이템이 나오는 블럭)    kind == 3


visible = True, False
"""


class Block:
    image_sheet = load_image("StructureImg.png")
    block_images = [
        Ani(image_sheet, 1, 0, 16, 16, 16, 0, 50, 50),  # 기본벽
        Ani(image_sheet, 1, 16, 16, 16, 16, 0, 50, 50),  # 벽돌
        Ani(image_sheet, 1, 48, 16, 16, 16, 0, 50, 50),  # 암석
        Ani(image_sheet, 1, 96, 0, 16, 16, 0, 50, 50),  # ?벽돌
    ]

    def __init__(self, x, y, kind=0, img_num=0, visible=True, change_kind=-1, change_img_num=-1, item=None, item_num=1):
        self.pos = Position(x, y, 50, 50)
        self.img_num = img_num
        self.kind = kind
        self.visible = visible

        self.change_kind = (self.kind if change_kind == -1 else change_kind)
        self.change_img_num = (self.img_num if change_img_num == -1 else change_img_num)

        self.bounce = 0  # 바운스하는 정도: 0 초과일겨우 바운스된 상태
        self.item = item
        self.item_num = item_num

        self.active = True

    def draw(self):
        if self.kind == 3:
            print(self.item.pos.x)

        if self.active and self.visible:
            if self.bounce <= 0:
                Block.block_images[self.img_num].draw(self.pos.x, self.pos.y, '')
            else:
                Block.block_images[self.img_num].draw(self.pos.x, self.pos.y + math.sin(self.bounce * math.pi / 15) * 25, '')
                self.bounce = (self.bounce + 1) % 15

    def crash(self):
        if self.active:
            #  부딪히면 가시화
            if not self.visible:
                self.visible = True

            # 부딪혔을때 상호작용
            if self.kind == 1:  # 부서지는 블럭
                self.active = False
                StageClass.stage.effects.append(Wreckage(self.pos.x, self.pos.y, self.img_num))
                # 부서지는 조각 생성
                pass
            elif self.kind == 2:  # 흔들리는 블럭(아이템 X)
                self.bounce = 1
            elif self.kind == 3:  # 흔들리는 블럭(아이템 O)
                self.bounce = 1
                if self.item_num > 0:
                    self.item_num -= 1
                    # 아이템 생성
                    StageClass.stage.items.append(self.item.create_clone())
                    if self.item_num <= 0:
                        self.kind = self.change_kind
                        self.img_num = self.change_img_num

            pass


class Wreckage:
    def __init__(self, x, y, img_num):
        self.img_num = img_num
        self.points = [     # x, y, r, moveX, moveY, rotateR
            [x + 12.5, y + 12.5, 0, random.uniform(-5, 5), random.uniform(2, 10), random.uniform(-3, 3)],
            [x - 12.5, y + 12.5, 0, random.uniform(-5, 5), random.uniform(2, 10), random.uniform(-3, 3)],
            [x - 12.5, y - 12.5, 0, random.uniform(-5, 5), random.uniform(2, 10), random.uniform(-3, 3)],
            [x + 12.5, y - 12.5, 0, random.uniform(-5, 5), random.uniform(2, 10), random.uniform(-3, 3)]
            ]

    def draw_del(self):
        delete = True
        Block.block_images[self.img_num].draw_wreckage(self.points)
        for point in self.points:
            if point[1] > -25:
                delete = False
                point[0] += point[3]
                point[1] += point[4]
                point[4] -= 0.5
                point[2] += point[5]

        return delete

