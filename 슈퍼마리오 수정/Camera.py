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

    def set_pos(self, x, y):
        self.left = x - constant.screen_w / 2
        self.bottom = y - constant.screen_h / 2
        self.right = x + constant.screen_w / 2
        self.top = y + constant.screen_h / 2

        # 좌우 보정
        if self.left < self.left_min:
            self.right += self.left_min - self.left
            self.left = self.left_min
        elif self.right_max < self.right:
            self.left += self.right_max - self.right
            self.right = self.right_max




        pass
