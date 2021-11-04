import time
import pico2d


game_running = True
show_collide_rec = True
edit_mode = False

pre_time = time.time()
delta_time = 0.01

play_stage_number = None
camera = None

# 이미지
player_img = None
structure_img = None
enemy_img = None
item_img = None
stageButton_img = None
editButton_img = None


def load_images():
    global player_img, structure_img, enemy_img, item_img, stageButton_img, editButton_img
    player_img = pico2d.load_image('ImageFolder/Player_Img.png')
    structure_img = pico2d.load_image('ImageFolder/Structure_Img.png')
    enemy_img = pico2d.load_image('ImageFolder/Enemy_Img.png')
    item_img = pico2d.load_image('ImageFolder/Item_Img.png')
    stageButton_img = pico2d.load_image('ImageFolder/StageButtons_Img.png')
    editButton_img = pico2d.load_image('ImageFolder/EditButton_Img.png')



def del_images():
    global player_img, structure_img, enemy_img, item_img, stageButton_img, editButton_img
    del player_img, structure_img, enemy_img, item_img, stageButton_img, editButton_img
