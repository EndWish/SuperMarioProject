from MarioClass import *
from StructureClass import *
from ItemClass import *
import math


class Stage:
    def __init__(self):
        self.mario = None
        self.blocks = []
        self.effects = []
        self.items = []

    def draw(self):
        # 마리오 그리기
        self.mario.draw()

        # 아이템 그리기
        count = 0
        for item in self.items:
            item.draw()
            count += 1
            print("# %d : item종류 : %d, x:%d, y:%d".format() % (count, item.kind, item.pos.x, item.pos.y))

        # 블럭 그리기
        for block in self.blocks:
            block.draw()

        # 이펙트 draw 및 삭제하기
        delete_list = []
        for i in range(len(self.effects)):
            if self.effects[i].draw_del():
                delete_list.append(i)

        for i in delete_list:
            self.effects.pop(i)
        pass

    def sort_blocks(self):
        self.blocks.sort(key=lambda a: a.pos.x)

    def can_crash_black_search(self, pos):
        obj_left = pos.x - pos.w / 2
        obj_right = pos.x + pos.w / 2
        s = 0
        e = len(self.blocks) - 1
        while s != e:
            middle = (s + e) // 2
            if self.blocks[middle].pos.x + self.blocks[middle].pos.w / 2 < obj_left:
                s = middle + 1
            else:
                e = middle
        index_left = e

        s = 0
        e = len(self.blocks) - 1
        while s != e:
            middle = math.ceil((s + e) / 2)
            if self.blocks[middle].pos.x - self.blocks[middle].pos.w / 2 < obj_right:
                s = middle
            else:
                e = middle - 1
        index_right = e
        return index_left, index_right

    def collision_check(self):
        # 이진탐색으로 마리오 근처의 블럭으로 범위 좁히기
        index_left, index_right = self.can_crash_black_search(self.mario.pos)

        # 좁힌 범위에서 충돌 체크하기
        self.mario.landing = False  # 각각의 블록과 충돌하기전 landing 을 False 로 초기화, 마리오가 하나의 블록이라도 위에 있다면 landing = True
        for b in self.blocks[index_left:index_right + 1]:
            if b.active:
                draw_rectangle(b.pos.x - b.pos.w / 2, b.pos.y - b.pos.h / 2, b.pos.x + b.pos.w / 2, b.pos.y + b.pos.h / 2)
                self.mario.collide_with_block(b)

    def item_running(self):
        delete_list = []
        for i in range(len(self.items)):
            if self.items[i].running_del():
                delete_list.append(i)

        for i in delete_list:
            self.items.pop(i)


stage = Stage()

stage1 = Stage()
stage1.mario = Mario(400, 300)
stage1.blocks = [
    Block(25, 25),
    Block(75, 25),
    Block(125, 25),
    Block(175, 25),
    Block(225, 25),
    Block(275, 25),
    Block(325, 25),
    Block(375, 25),
    Block(425, 25),
    Block(475, 25),
    Block(525, 25),
    Block(575, 25),

    Block(475, 75),
    Block(525, 75),
    Block(175, 75),

    Block(225, 275, 2, 0),
    Block(275, 275, 1, 1),
    Block(325, 275, 2, 0, False),
    Block(375, 275, 0, 2, False),
    Block(425, 275, 3, 3, True, 2, 0, Item(0, Position(425, 275, 50, 50)), 2)

]
