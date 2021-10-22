import math

import pico2d
import Global

import play_state
import game_framework


class Button:
    def __init__(self):
        self.pos = None
        self.w = None
        self.h = None
        pass

    def onClick(self, mx, my):
        if self.pos[0] - (self.w / 2) <= mx <= self.pos[0] + (self.w / 2) and self.pos[1] - (self.h / 2) <= my <= self.pos[1] + (self.h / 2):
            return True
        return False


    def draw(self):
        pass


class StageButton(Button):
    def __init__(self):
        self.w, self.h = 50, 50

        self.stageNumber = None
        self.clear = False
        self.canPlay = False
        self.next_node = ()
        pass

    def onClick(self, mx, my):
        if super().onClick(mx, my):
            if self.clear or self.canPlay:
                Global.play_stage_number = self.stageNumber
                game_framework.push_state(play_state)


    def setStageNumber(self, number):
        self.stageNumber = number

    def setClear(self, value=True):
        self.clear = value

    def setCanPlay(self, value=True):
        self.canPlay = value

    def setPos(self, pos):
        self.pos = pos

    def draw(self):
        if self.clear:  # 빨강체크
            Global.stageButton_img.clip_draw(400, 0, 195, 195, self.pos[0], self.pos[1], self.w, self.h)
        else:
            if self.canPlay:    # 빨강
                Global.stageButton_img.clip_draw(200, 0, 195, 195, self.pos[0], self.pos[1], self.w, self.h)
            else:   # 흑백
                Global.stageButton_img.clip_draw(0, 0, 195, 195, self.pos[0], self.pos[1], self.w, self.h)


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
            line_dx, line_dy = stageButtons[i].pos[0] - stageButton.pos[0], stageButtons[i].pos[1] - stageButton.pos[1]
            line_dir = math.atan2(line_dy, line_dx)
            line_x, line_y = (stageButtons[i].pos[0] + stageButton.pos[0]) / 2, (stageButtons[i].pos[1] + stageButton.pos[1]) / 2
            line_dis = math.sqrt(line_dx**2 + line_dy**2)

            stageNodeLines.append((line_dir, line_x, line_y, line_dis))

            # 재귀함수
            Init_stageButton_dfs(i, stageButtons, visit, stageNodeLines)


def Load_stageButtons():
    stageButtons = []
    stageNodeLines = []
    f = open('stage_buttons.txt', 'r', encoding='UTF8')
    f.readline()  # 첫줄 (설명라인) 제거
    while True:
        line = f.readline()
        if not line: break
        line = list(map(int, line.split()))
        # 버튼 생성
        pos = (line[0], line[1])
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


