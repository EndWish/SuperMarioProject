import pico2d
import Global
import math
from Animation import *
from Position import *


class Block:
    def block_number(self):
        return 0

    def __init__(self, pos, hidden=False):
        self.pos = pos
        self.hidden = hidden
        self.animator = None
        self.item_queue = []

    def heading(self):
        if self.hidden:
            self.hidden = False

    def draw(self):
        if not self.hidden:
            self.animator.draw(self.pos.x, self.pos.y, '')

    def save(self):
        txt = "%d %d %d %d %d" % (self.block_number(), self.pos.x, self.pos.y, self.hidden, len(self.item_queue))
        return txt


class RigidBlock(Block):
    def block_number(self):
        return 1

    def __init__(self, pos, hidden=False):
        super().__init__(pos, hidden)
        self.animator = SingleIndexAnimation(Global.structure_img, 48, 16, 16, 16, 50, 50)


class BounceBlock(Block):
    def block_number(self):
        return 2

    def __init__(self, pos, hidden=False):
        super().__init__(pos, hidden)
        self.animator = SingleIndexAnimation(Global.structure_img, 0, 16, 16, 16, 50, 50)
        self.bounce = 0

    def draw(self):
        if not self.hidden:
            if self.bounce <= 0:
                self.animator.draw(self.pos.x, self.pos.y, '')
            else:
                self.animator.draw(self.pos.x, self.pos.y + math.sin(self.bounce * math.pi / 0.15) * 25, '')
                self.bounce -= Global.delta_time

    def heading(self):
        super(BounceBlock, self).heading()
        self.bounce = 0.15


def load(txt):
    txt = list(map(int, txt.split()))
    if txt[0] == 1:
        return RigidBlock(Position(txt[1], txt[2], 50, 50), bool(txt[3]))
    elif txt[0] == 2:
        block = BounceBlock(Position(txt[1], txt[2], 50, 50), bool(txt[3]))
        # block 에 아이템 넣기
        return block


def Load_blocks(file_name):
    blocks = []
    f = open(file_name, 'r', encoding='UTF8')
    f.readline()  # 첫줄 (설명라인) 제거

    # 블럭리스트 생성
    while True:
        line = f.readline()
        if not line: break
        block = load(line)
        blocks.append(block)

    # 블럭리스트 x 좌표로 정렬
    blocks.sort(key=lambda a: a.pos.x)

    f.close()
    return blocks





if __name__ == '__main__':
    blocks = Load_blocks('test_blocks.txt')
    for b in blocks:
        print(b.save())



