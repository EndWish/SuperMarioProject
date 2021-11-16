import Global
import pico2d


class Position:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def collide_pos(self, other):
        self_right = self.x + self.w / 2
        self_left = self.x - self.w / 2
        self_top = self.y + self.h / 2
        self_bottom = self.y - self.h / 2

        other_right = other.x + other.w / 2
        other_left = other.x - other.w / 2
        other_top = other.y + other.h / 2
        other_bottom = other.y - other.h / 2

        if self_left <= other_right and self_right >= other_left and self_bottom <= other_top and self_top >= other_bottom:
            col_x = 0
            col_y = 0
            if self.x < other.x:
                col_x = self_right - other_left + 1
            else:
                col_x = self_left - other_right - 1

            if self.y < other.y:
                col_y = self_top - other_bottom + 1
            else:
                col_y = self_bottom - other_top - 1

            return col_x, col_y
        else:
            return 0, 0

    def draw_collision_rect(self):
        if Global.show_collide_rec:
            x = self.x - Global.camera.left
            y = self.y - Global.camera.bottom
            pico2d.draw_rectangle(x - self.w/2, y - self.h/2, x + self.w/2, y + self.h/2)
