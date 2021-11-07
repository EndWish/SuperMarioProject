import Global
import constant
import play_state
from Position import *
from Animation import *


class Mario:

    def __init__(self, x, y):
        self.life = 3
        self.death = False
        self.invincible = 0
        self.pos = Position(x, y, 46, 46)
        
        self.mode = 0

        self.dir = 0  # 방향키를 눌렀는지 (1 = right 키, -1 = left 키)
        self.speed = 0
        self.jump_key = False
        self.v_speed = 0
        self.landing = False

        # 드로우 관련 변수
        self.draw_mode = 0
        self.change_mode = 0
        self.change_time = 100
        self.flip = ''
        self.motion = 0
        self.animator = [
            [
                SingleIndexAnimation(Global.player_img, 0, 0, 18, 18, 50, 50),  # idle : 0
                SingleIndexAnimation(Global.player_img, 20, 0, 18, 18, 50, 50),  # jump : 1
                OriginAnimation(Global.player_img, 40, 0, 18, 18, 50, 50, 4, 20, 0.05),  # run : 2
                SingleIndexAnimation(Global.player_img, 120, 0, 18, 18, 50, 50),  # turn : 3
            ],
            [
                SingleIndexAnimation(Global.player_img, 0, 20, 18, 34, 50, 100),  # idle : 0
                SingleIndexAnimation(Global.player_img, 20, 20, 18, 34, 50, 100),  # jump : 1
                OriginAnimation(Global.player_img, 40, 20, 18, 34, 50, 100, 4, 20, 0.05),  # run : 2
                SingleIndexAnimation(Global.player_img, 120, 20, 18, 34, 50, 100),  # turn : 3
            ],
            [
                SingleIndexAnimation(Global.player_img, 0, 60, 18, 34, 50, 100),  # idle : 0
                SingleIndexAnimation(Global.player_img, 20, 60, 18, 34, 50, 100),  # jump : 1
                OriginAnimation(Global.player_img, 40, 60, 18, 34, 50, 100, 4, 20, 0.05),  # run : 2
                SingleIndexAnimation(Global.player_img, 120, 60, 18, 34, 50, 100),  # turn : 3
            ],
        ]

    def update(self):
        delta_time = Global.delta_time

        self.invincible -= delta_time

        if self.mode != self.change_mode:   # 변신중
            self.changing()
        else:
            self.move()

        self.crash_enemies()

    def changing(self):
        delta_time = Global.delta_time

        # 시작할때
        if self.change_time == 100:
            if self.change_mode == 1 or self.change_mode == 2:
                self.pos.h = 46 * 2
            else:
                self.pos.h = 46
            self.move()

        if self.mode < self.change_mode:  # 강화 변신
            self.change_time -= 100 * delta_time
            if (self.change_time // 20) % 2 == 0:
                self.draw_mode = self.mode
            else:
                self.draw_mode = self.change_mode
        else:  # 약화 변신
            self.change_time = 0

        # 변신이 끝나면
        if self.change_time <= 0:
            self.mode = self.change_mode
            self.draw_mode = self.change_mode
            self.change_time = 100

    def move(self):
        # 움직일수 없는 조건을 함수로 제공하여 리턴

        delta_time = Global.delta_time

        # 속도계산
        if self.dir == 1:  # 오른쪽키(+가속)
            self.speed += constant.mario_accel * delta_time
            if self.speed < 0:
                self.speed += constant.mario_retar * delta_time
        elif self.dir == -1:  # 왼쪽키(-가속)
            self.speed -= constant.mario_accel * delta_time
            if self.speed > 0:
                self.speed -= constant.mario_retar * delta_time
        else:  # 아무키도 안눌렀을 경우(0으로 감속)
            if self.speed >= constant.mario_retar * delta_time:
                self.speed -= constant.mario_retar * delta_time
            elif self.speed <= -constant.mario_retar * delta_time:
                self.speed += constant.mario_retar * delta_time
            else:
                self.speed = 0

        # 속도제한 하기
        if self.speed > constant.mario_max_speed:
            self.speed = constant.mario_max_speed
        elif self.speed < -constant.mario_max_speed:
            self.speed = -constant.mario_max_speed

        # 좌우 이동
        target_pos = Position(self.pos.x + self.speed * delta_time, self.pos.y, self.pos.w, self.pos.h)
        check_blocks = play_state.get_check_blocks(target_pos)

        # target_pos 와 부딪히면 벽이 있는지 확인
        for block in check_blocks:
            play_state.add_collision_range(block.pos)
            col_xy = target_pos.collide_pos(block.pos)
            if col_xy != (0, 0) and not block.hidden:
                target_pos.x -= col_xy[0]
                self.speed = 0
                break

        self.pos.x = target_pos.x

        # 낙하&점프
        self.v_speed -= constant.mario_gravity * delta_time
        if self.v_speed < constant.mario_min_v_speed:  # 낙하 최대속도 조정
            self.v_speed = constant.mario_min_v_speed
        elif self.v_speed > -constant.mario_min_v_speed:  # 점프 최대속도 조정
            self.v_speed = -constant.mario_min_v_speed

        target_pos = Position(self.pos.x, self.pos.y + self.v_speed * delta_time, self.pos.w, self.pos.h + 2)
        check_blocks = play_state.get_check_blocks(target_pos)
        # target_pos 와 부딪히면 벽이 있는지 확인
        self.landing = False
        for block in check_blocks:
            play_state.add_collision_range(block.pos)
            col_xy = target_pos.collide_pos(block.pos)
            if col_xy != (0, 0):
                if self.v_speed <= 0:   # 아래쪽 충돌 확인
                    if block.hidden:
                        continue
                    target_pos.y -= col_xy[1] + 1
                    self.v_speed = 0
                    self.landing = True
                else:   # 위쪽 충돌 확인
                    target_pos.y -= col_xy[1] - 1
                    self.v_speed = 0
                    block.heading()
                break

        self.pos.y = target_pos.y

        if self.jump_key:
            self.jump()

        play_state.add_collision_range(target_pos)

        # 모션

        # 좌우반전
        if self.speed > 0 and self.flip == 'h':
            self.flip = ''
        elif self.speed < 0 and self.flip == '':
            self.flip = 'h'

        # 모션 바꾸기
        if self.landing:
            if self.speed == 0:
                self.motion = 0
            else:  # speed != 0
                self.animator[self.mode][self.motion].time_slice_speed = abs(self.speed / constant.mario_max_speed) + 0.01
                if (self.speed > 0 and self.dir == -1) or (self.speed < 0 and self.dir == 1):
                    self.motion = 3
                else:
                    self.motion = 2
        else:
            self.motion = 1

    def crash_enemies(self):
        for enemy in play_state.enemies:
            col_xy = self.pos.collide_pos(enemy.pos)
            if col_xy != (0, 0):    # 충돌 했을 경우
                if -20 < col_xy[1] < 0:
                    if self.v_speed < 0:
                        # 위에서 밟았을 경우
                        self.v_speed = 1000
                        enemy.attacked(1)
                        pass
                else:
                    # 적에게 맞을 경우
                    self.speed, self.v_speed = col_xy[0] * -250, col_xy[1] * -20
                    if self.is_invincible():
                        # 무적인 경우
                        pass
                    else:
                        # 무적이 아닌데, 적에게 맞을경우
                        self.downgrage_change_mode()
                        pass
                break


    def jump(self):
        if self.landing:
            self.v_speed = 1500

    def draw(self):
        # 변신 상태일때
        if self.mode != self.change_mode:
            self.motion = 1
        # 무적 상태일때
        if self.is_invincible():
            if self.invincible // 0.1 % 2 == 0:
                self.animator[self.draw_mode][self.motion].image.opacify(0.5)

        self.animator[self.draw_mode][self.motion].draw(self.pos.x, self.pos.y, self.flip)
        self.animator[self.draw_mode][self.motion].image.opacify(1)

    def add_dir(self, d):
        self.dir += d

    def upgrade_change_mode(self, mode):
        # 이미 업그래이드 되어 있을 경우
        if mode <= self.change_mode:
            if mode == 1:
                # 추가 점수+
                play_state.score += 500
            elif mode == 2:
                # 추가 점수+
                play_state.score += 1000
        # 업그래이드 될 수 있을경우
        else:
            self.change_mode = mode
            self.set_invincible(1)

    def downgrage_change_mode(self):
        if self.is_invincible():    # 무적일경우 아무것도 하지 않는다.
            return
        else:                       # 무적이 아닐경우
            self.set_invincible(0.4)

        # 진화 상태가 아닐때
        if self.mode == 0:
            if self.life <= 0:
                self.death = True
            else:
                self.life -= 1
        # 진화 상태 일때
        else:
            self.change_mode = self.mode - 1

    def is_invincible(self):
        if self.invincible > 0:
            return True
        return False

    def set_invincible(self, set_time):
        if self.invincible < set_time:
            self.invincible = set_time
