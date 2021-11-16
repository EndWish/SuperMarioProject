import constant


class Camera:
    def __init__(self):
        self.left = None
        self.bottom = None
        self.right = None
        self.top = None

        self.left_min = None
        self.bottom_min = None
        self.right_max = None
        self.top_max = None

    def set_window_max(self, left_min, bottom_min, right_max, top_max):
        self.left_min = left_min
        self.bottom_min = bottom_min
        self.right_max = right_max
        self.top_max = top_max

    def load_window_max(self, file_name):
        f = open(file_name, 'r', encoding='UTF8')
        txt = list(map(int, f.readline().split()))
        self.set_window_max(txt[0], txt[1], txt[2], txt[3])

    def set_pos(self, pos):
        self.left = pos.x - constant.screen_w / 2
        self.bottom = pos.y - constant.screen_h / 2
        self.right = pos.x + constant.screen_w / 2
        self.top = pos.y + constant.screen_h / 2

        # 좌우 보정
        if self.left < self.left_min:
            self.right += self.left_min - self.left
            self.left = self.left_min
        elif self.right_max < self.right:
            self.left += self.right_max - self.right
            self.right = self.right_max
        
        # 상하 보정
        if self.bottom < self.bottom_min:
            self.top += self.bottom_min - self.bottom
            self.bottom = self.bottom_min
        elif self.top_max < self.top:
            self.bottom += self.top_max - self.top
            self.top = self.top_max

    def window_expand(self, margin):
        self.left_min -= margin
        self.right_max += margin
        self.bottom_min -= margin
        self.top_max += margin
