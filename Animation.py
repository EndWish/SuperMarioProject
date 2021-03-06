import time
import math

import pico2d

import Global


class Animation:
    def __init__(self):
        pass

    def draw(self, x, y, flip):
        pass


class SingleIndexAnimation(Animation):
    def __init__(self, image, img_x, img_y, img_w, img_h, draw_w, draw_h):
        super().__init__()
        self.image = image
        self.img_x = img_x
        self.img_y = img_y
        self.img_w = img_w
        self.img_h = img_h
        self.draw_w = draw_w
        self.draw_h = draw_h

    def draw(self, x, y, flip, r=0):
        x -= Global.camera.left
        y -= Global.camera.bottom

        self.image.clip_composite_draw(self.img_x, self.img_y, self.img_w, self.img_h,
                                       r, flip, x, y, self.draw_w, self.draw_h)


class OriginAnimation(Animation):
    def __init__(self, image, img_x, img_y, img_w, img_h, draw_w, draw_h, index_max, jump_x, time_slice=0.1):
        super().__init__()
        self.image = image
        self.img_x = img_x
        self.img_y = img_y
        self.img_w = img_w
        self.img_h = img_h
        self.draw_w = draw_w
        self.draw_h = draw_h

        self.index = 0
        self.indexMax = index_max
        self.jump_x = jump_x
        self.time_slice = time_slice
        self.now_time = time.time()
        self.time_slice_speed = 1.0

    def draw(self, x, y, flip):
        x -= Global.camera.left
        y -= Global.camera.bottom

        if (time.time() - self.now_time) >= self.time_slice / (self.time_slice_speed + 0.001):
            self.now_time = time.time()
            self.index = (self.index + 1) % self.indexMax

        self.image.clip_composite_draw(self.img_x + self.index * self.jump_x, self.img_y, self.img_w, self.img_h,
                                       0, flip, x, y, self.draw_w, self.draw_h)


def print_numbers(numbers, x, y, size):
    numbers = int(numbers)

    digit = 1
    if numbers > 0:
        digit = int(math.log10(numbers)) + 1

    for i in range(digit - 1, -1, -1):
        number = numbers % 10     # 그 자리의 숫자 구하고
        numbers //= 10     # 일의 자리 삭제
        Global.numbers_img.clip_draw(300 * number, 0, 300, 400, x + size * i, y, size, size * 4/3)

