from pico2d import Image
import time


class Ani:
    def __init__(self, image, index_max, img_x, img_y, img_w, img_h, jump_x, draw_w, draw_h, time_slice=0.1):
        self.index = 0
        self.indexMax = index_max
        self.image = image
        self.img_x = img_x
        self.img_y = img_y
        self.img_w = img_w
        self.img_h = img_h
        self.jump_x = jump_x
        self.draw_w = draw_w
        self.draw_h = draw_h
        self.now_time = time.time()
        self.time_slice = time_slice
        self.time_slice_speed = 1.0

    def set_img(self, image):
        self.image = image

    def draw(self, x, y, flip):
        if self.indexMax > 1 and (time.time() - self.now_time) >= self.time_slice / self.time_slice_speed:
            self.now_time = time.time()
            self.index = (self.index + 1) % self.indexMax

        self.image.clip_composite_draw(self.img_x + self.index * self.jump_x, self.img_y, self.img_w, self.img_h,
                             0, flip, x, y, self.draw_w, self.draw_h)

    def draw_wreckage(self, points):
        divied_w = self.img_w // 2
        divied_h = self.img_h // 2
        divied_draw_h = self.draw_h // 2
        divied_draw_w = self.draw_w // 2
        if points[0][1] > -25:
            self.image.clip_composite_draw(self.img_x + divied_w, self.img_y + divied_h, divied_w, divied_h,
                                           points[0][2], '', points[0][0], points[0][1], divied_draw_h, divied_draw_w)
        if points[1][1] > -25:
            self.image.clip_composite_draw(self.img_x, self.img_y + divied_h, divied_w, divied_h,
                                           points[1][2], '', points[1][0], points[1][1], divied_draw_h, divied_draw_w)
        if points[2][1] > -25:
            self.image.clip_composite_draw(self.img_x, self.img_y, divied_w, divied_h,
                                           points[2][2], '', points[2][0], points[2][1], divied_draw_h, divied_draw_w)
        if points[3][1] > -25:
            self.image.clip_composite_draw(self.img_x + divied_w, self.img_y, divied_w, divied_h,
                                           points[3][2], '', points[3][0], points[3][1], divied_draw_h, divied_draw_w)

        pass

