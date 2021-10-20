from pico2d import *
open_canvas()
# open_canvas(1920, 1080, True, True)

from MarioClass import *
from AnimationClass import *
import StageClass


def handle_events():
    global gameRunning
    global right_key
    global left_key

    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                right_key = True
                StageClass.stage.mario.dir = 1
            elif event.key == SDLK_LEFT:
                left_key = True
                StageClass.stage.mario.dir = -1
            elif event.key == SDLK_UP and StageClass.stage.mario.landing:
                StageClass.stage.mario.v_speed = 15
                StageClass.stage.mario.landing = False
            elif event.key == SDLK_ESCAPE:
                gameRunning = False

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                right_key = False
                if left_key:
                    StageClass.stage.mario.dir = -1
                else:
                    StageClass.stage.mario.dir = 0
            elif event.key == SDLK_LEFT:
                left_key = False
                if right_key:
                    StageClass.stage.mario.dir = 1
                else:
                    StageClass.stage.mario.dir = 0

        elif event.type == SDL_QUIT:
            gameRunning = False


# 전역변수 생성
right_key = False
left_key = False

# 게임 옵션관련 변수
gameRunning = True
now_time = time.time()
deltaTime = 0.0
FPS = 100.0


StageClass.stage = StageClass.stage1
StageClass.stage.sort_blocks()

while gameRunning:
    deltaTime = time.time() - now_time
    now_time = time.time()
    handle_events()
    clear_canvas()
    StageClass.stage.mario.move()
    StageClass.stage.mario.change()
    StageClass.stage.draw()
    StageClass.stage.collision_check()
    StageClass.stage.item_running()



    # 프레임 고정
    if time.time() - now_time < (1.0/FPS):
        delay((1.0/FPS) - (time.time() - now_time))

    update_canvas()

close_canvas()
