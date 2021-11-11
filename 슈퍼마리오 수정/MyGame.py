import constant
import game_framework
import pico2d

import title_state

pico2d.open_canvas(constant.screen_w, constant.screen_h, False, False)
game_framework.run(title_state)
pico2d.close_canvas()
