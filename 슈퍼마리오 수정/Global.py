import time
import pico2d

game_running = True

pre_time = time.time()
delta_time = 0.01

play_stage_number = None

player_img = None
structure_img = None
enemy_img = None
item_img = None
stageButton_img = None


def load_images():
    global player_img, structure_img, enemy_img, item_img, stageButton_img
    player_img = pico2d.load_image('Player_Img.png')
    structure_img = pico2d.load_image('Structure_Img.png')
    enemy_img = pico2d.load_image('EnemyImg.png')
    item_img = pico2d.load_image('Item_Img.png')
    stageButton_img = pico2d.load_image('StageButtons_Img.png')


def del_images():
    global player_img, structure_img, enemy_img, item_img, stageButton_img
    del player_img, structure_img, enemy_img, item_img, stageButton_img
