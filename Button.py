import math

import pico2d
import Global
import constant
import map_state
from Position import *
from Animation import *


import play_state
import game_framework


class Button:
    def __init__(self):
        self.pos = None
        pass

    def onClick(self, mx, my):
        if self.pos.x - (self.pos.w / 2) <= mx <= self.pos.x + (self.pos.w / 2) and self.pos.y - (self.pos.h / 2) <= my <= self.pos.y + (self.pos.h / 2):
            return True
        return False


    def draw(self):
        pass


class EditButton(Button):
    def __init__(self):
        super().__init__()
        self.pos = Position(60, constant.screen_h - 60, 50, 50)

    def onClick(self, mx, my):
        if super().onClick(mx, my):
            Global.edit_mode = not Global.edit_mode

    def draw(self):
        if Global.edit_mode:
            Global.editButton_img.clip_draw(600,0,600,600,self.pos.x, self.pos.y, self.pos.w, self.pos.h)
        else:
            Global.editButton_img.clip_draw(0, 0, 600, 600, self.pos.x, self.pos.y, self.pos.w, self.pos.h)


class StageButton(Button):
    def __init__(self):
        super().__init__()
        self.stageNumber = None
        self.clear = False
        self.canPlay = False
        self.next_node = ()
        pass

    def onClick(self, mx, my):
        import edit_state
        if super().onClick(mx, my):
            if Global.edit_mode:
                Global.play_stage_number = self.stageNumber
                game_framework.push_state(edit_state)
            elif self.clear or self.canPlay:
                Global.play_stage_number = self.stageNumber
                game_framework.push_state(play_state)


    def setStageNumber(self, number):
        self.stageNumber = number

    def setClear(self, value=True):
        self.clear = value

    def setCanPlay(self, value=True):
        self.canPlay = value

    def clear_stage(self):
        self.setClear()
        for next_node_num in self.next_node:
            map_state.stageButtons[next_node_num].setCanPlay()

    def setPos(self, pos):
        self.pos = pos

    def draw(self):
        if self.clear:  # 빨강체크
            Global.stageButton_img.clip_draw(400, 0, 195, 195, self.pos.x, self.pos.y, self.pos.w, self.pos.h)
        else:
            if self.canPlay:    # 빨강
                Global.stageButton_img.clip_draw(200, 0, 195, 195, self.pos.x, self.pos.y, self.pos.w, self.pos.h)
            else:   # 흑백
                Global.stageButton_img.clip_draw(0, 0, 195, 195, self.pos.x, self.pos.y, self.pos.w, self.pos.h)


class EditBlockButton(Button):
    def __init__(self, x, y, block_number, hidden):
        super(EditBlockButton, self).__init__()
        self.pos = Position(x, y, 50, 50)
        self.init_pos = Position(x, y, 50, 50)
        self.block_number = block_number
        self.hidden = hidden
        self.animator = [
            None,
            SingleIndexAnimation(Global.structure_img, 48, 16, 16, 16, 50, 50),  # 단단한 벽
            SingleIndexAnimation(Global.structure_img, 0, 16, 16, 16, 50, 50),  # 바운스 벽돌
            SingleIndexAnimation(Global.structure_img, 16, 16, 16, 16, 50, 50),  # 벽돌 블럭
        ]

    def onClick(self, mx, my):
        if super().onClick(mx, my):
            import edit_state
            edit_state.pushing_mode = edit_state.push_block  # 변수에 함수를 넣어준다.
            edit_state.pushing_txt = "%d 0 0 %d 0" % (self.block_number, self.hidden)
            return True
        return False

    def update(self):
        self.pos.x = self.init_pos.x + Global.camera.left
        self.pos.y = self.init_pos.y + Global.camera.bottom

    def draw_edit(self):
        if self.hidden:
            self.animator[self.block_number].image.opacify(0.5)
        else:
            self.animator[self.block_number].image.opacify(1)
        self.animator[self.block_number].draw(self.pos.x, self.pos.y, '')
        self.animator[self.block_number].image.opacify(1)


class EditItemButton(Button):
    def __init__(self, x, y, item_number):
        super(EditItemButton, self).__init__()
        self.pos = Position(x, y, 50, 50)
        self.init_pos = Position(x, y, 50, 50)
        self.item_number = item_number
        self.animator = [
            None,
            SingleIndexAnimation(Global.item_img, 0, 0, 18, 18, 50, 50),    # 슈퍼 머쉬룸
            SingleIndexAnimation(Global.item_img, 40, 0, 18, 18, 50, 50),   # 라이프 머쉬룸
            SingleIndexAnimation(Global.item_img, 0, 40, 18, 18, 50, 50),   # 파이어 플라워
            SingleIndexAnimation(Global.item_img, 0, 60, 11, 16, 22, 32),   # 코인
            SingleIndexAnimation(Global.item_img, 0, 20, 16, 18, 50, 50),   # 슈퍼스타
        ]

    def onClick(self, mx, my):
        if super().onClick(mx, my):
            import edit_state
            edit_state.pushing_mode = edit_state.push_item  # 변수에 함수를 넣어준다.
            edit_state.pushing_txt = "%d" % self.item_number
            return True
        return False

    def update(self):
        self.pos.x = self.init_pos.x + Global.camera.left
        self.pos.y = self.init_pos.y + Global.camera.bottom

    def draw_edit(self):
        self.animator[self.item_number].draw(self.pos.x, self.pos.y, '')


class EditEnemyButton(Button):
    def __init__(self, x, y, enemy_number):
        super(EditEnemyButton, self).__init__()
        self.pos = Position(x, y, 50, 50)
        self.init_pos = Position(x, y, 50, 50)
        self.enemy_number = enemy_number
        self.animator = [
            None,
            SingleIndexAnimation(Global.enemy_img, 0, 0, 18, 18, 50, 50),  # 굼바
            OriginAnimation(Global.enemy_img, 0, 20, 18, 27, 50, 50, 2, 20, 0.5),  # 트루파(엉금엉금)
        ]

    def onClick(self, mx, my):
        if super().onClick(mx, my):
            import edit_state
            edit_state.pushing_mode = edit_state.push_enemy  # 변수에 함수를 넣어준다.
            edit_state.pushing_txt = "%d 0 0" % self.enemy_number
            return True
        return False

    def update(self):
        self.pos.x = self.init_pos.x + Global.camera.left
        self.pos.y = self.init_pos.y + Global.camera.bottom

    def draw_edit(self):
        self.animator[self.enemy_number].draw(self.pos.x, self.pos.y, '')


class EditStructureButton(Button):
    def __init__(self, x, y, structure_number):
        super(EditStructureButton, self).__init__()
        self.pos = Position(x, y, 50, 50)
        self.init_pos = Position(x, y, 50, 50)
        self.structure_number = structure_number
        self.animator = [
            None,
            SingleIndexAnimation(Global.structure_img, 16 * 13, 16, 16, 16, 50, 50),    # 기둥 꼭대기
        ]

    def onClick(self, mx, my):
        if super().onClick(mx, my):
            import edit_state
            edit_state.pushing_mode = edit_state.push_structure  # 변수에 함수를 넣어준다.
            edit_state.pushing_txt = "%d 0 0" % self.structure_number
            return True
        return False

    def update(self):
        self.pos.x = self.init_pos.x + Global.camera.left
        self.pos.y = self.init_pos.y + Global.camera.bottom

    def draw_edit(self):
        self.animator[self.structure_number].draw(self.pos.x, self.pos.y, '')

def CreateStageButton(pos, stage_num, clear, next_node):
    button = StageButton()
    button.setStageNumber(stage_num)
    button.setPos(pos)
    button.setClear(clear)
    button.next_node = next_node
    return button


def Init_stageButton_dfs(index, stageButtons, visit, stageNodeLines):
    visit[index] = True
    stageButton = stageButtons[index]

    for i in stageButton.next_node:
        if not visit[i]:
            # 지금 노드가 클리어 되었으면 다음 노드들을 canPlay상태로 만든다.
            if stageButton.clear:
                stageButtons[i].setCanPlay()
            # stageNodeLine (각도, x, y, dis) 추가
            line_dx, line_dy = stageButtons[i].pos.x - stageButton.pos.x, stageButtons[i].pos.y - stageButton.pos.y
            line_dir = math.atan2(line_dy, line_dx)
            line_x, line_y = (stageButtons[i].pos.x + stageButton.pos.x) / 2, (stageButtons[i].pos.y + stageButton.pos.y) / 2
            line_dis = math.sqrt(line_dx**2 + line_dy**2)

            stageNodeLines.append((line_dir, line_x, line_y, line_dis))

            # 재귀함수
            Init_stageButton_dfs(i, stageButtons, visit, stageNodeLines)


def Load_stageButtons():
    stageButtons = []
    stageNodeLines = []
    f = open('DataFolder/stage_buttons.txt', 'r', encoding='UTF8')
    f.readline()  # 첫줄 (설명라인) 제거
    while True:
        line = f.readline()
        if not line: break
        line = list(map(int, line.split()))
        # 버튼 생성
        pos = Position(line[0], line[1], 50, 50)
        stage_num = line[2]
        clear = bool(line[3])
        next_node, pre_node = [], []
        if line[4] > 0:
            next_node = tuple(line[5: 5 + int(line[4])])
        pre_node_num_index = 5 + int(line[4])  # pre_node 개수가 들어있는 인덱스 )
        stageButton = CreateStageButton(pos, stage_num, clear, next_node)

        stageButtons.append(stageButton)

    # stage canPlay 초기화하기
    stageButtons[0].setCanPlay()
    visit = [False for i in range(len(stageButtons))]
    Init_stageButton_dfs(0, stageButtons, visit, stageNodeLines)

    f.close()
    return stageButtons, stageNodeLines





if __name__ == '__main__':
    pico2d.open_canvas()
    Global.load_images()

    button = StageButton()
    button.setPos((100, 100))
    button.draw()
    pico2d.update_canvas()

    pico2d.delay(1)

    Global.del_images()
    pico2d.close_canvas()


