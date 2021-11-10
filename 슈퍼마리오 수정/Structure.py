from Position import *
from Animation import *


class Structure:
    def structure_number(self):
        return 0

    def update(self):
        pass

    def draw(self):
        pass

    def draw_edit(self):
        self.draw()

    def save(self):
        pass


class Flag(Structure):
    def structure_number(self):
        return 1

    def __init__(self, pos):
        self.height = 6
        self.pos = Position(pos.x, pos.y, 50, 50)
        self.col_pos = Position(pos.x, pos.y - 25 + 50 * ((self.height - 1) / 2), 20, (self.height - 1) * 50)
        self.animator = [
            SingleIndexAnimation(Global.structure_img, 16 * 12, 0, 16, 16, 50, 50),   # 기둥
            SingleIndexAnimation(Global.structure_img, 16 * 12, 16, 16, 16, 50, 50),    # 기둥 꼭대기
        ]
        pass

    def draw(self):
        for i in range(self.height):
            if i == self.height - 1:
                self.animator[1].draw(self.pos.x, self.pos.y + (self.pos.h * i), '')
                break
            self.animator[0].draw(self.pos.x, self.pos.y + (self.pos.h * i), '')

    def save(self):
        txt = "%d %d %d\n" % (self.structure_number(), self.pos.x, self.pos.y)
        return txt


def load_structure(txt):
    txt = list(map(int, txt.split()))
    if txt[0] == 1:
        return Flag(Position(txt[1], txt[2], 50, 50))


def Load_structures(file_name):
    structures = []
    f = open(file_name, 'r', encoding='UTF8')
    f.readline()  # 첫줄 (설명라인) 제거

    # 블럭리스트 생성
    while True:
        line = f.readline()
        if not line: break
        structure = load_structure(line)
        structures.append(structure)

    f.close()
    return structures
