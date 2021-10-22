import time

import Global

class GameState:
    def __init__(self, state):
        self.enter = state.enter
        self.exit = state.exit
        self.pause = state.pause
        self.resume = state.resume
        self.handle_events = state.handle_events
        self.update = state.update
        self.draw = state.draw


running = None
stack = []  # stat 를 넣는 stack


def run(start_state):
    global running, stack
    running = True
    stack = [start_state]
    start_state.enter()

    Global.pre_time = time.time()
    Global.delta_time = 0.01
    Global.load_images()

    # 반복적으로 실행하기
    while running:
        stack[-1].handle_events()
        stack[-1].update()
        stack[-1].draw()

        Global.delta_time = time.time() - Global.pre_time
        Global.pre_time = time.time()
    # 종료되었을때 남은 스택 전부 해제
    while len(stack) > 0:
        stack[-1].exit()
        stack.pop()

    Global.del_images()


def quit():
    global running
    running = False


def push_state(state):
    global stack
    if len(stack) > 0:
        stack[-1].pause()
    stack.append(state)
    state.enter()


def pop_state():
    global stack
    # state 를 하나 제거하고
    if len(stack) > 0:
        stack[-1].exit()
        stack.pop()
    # 이전의 state 를 다시 실행
    if len(stack) > 0:
        stack[-1].resume()


def change_state(state):
    global stack
    if len(stack) > 0:
        stack[-1].exit()
        stack.pop()
    stack.append(state)
    state.enter()




