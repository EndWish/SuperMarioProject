import time
import pico2d


game_running = True
show_collide_rec = True
edit_mode = False

game_fps = 100
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
attack_img = None
numbers_img = None

# 사운드
bgm_mp3 = None
oneUp_wav = None
powerUp_wav = None
powerDown_wav = None
getHit_wav = None
coin_wav = None
marioDies_wav = None
marioJump_wav = None
itemSprouting_wav = None
enemyGetHit_wav = None
blockHeading_wav = None
throwingFireball_wav = None


def load_images():
    global player_img, structure_img, enemy_img, item_img, stageButton_img, editButton_img, attack_img, numbers_img
    player_img = pico2d.load_image('ImageFolder/Player_Img.png')
    structure_img = pico2d.load_image('ImageFolder/Structure_Img.png')
    enemy_img = pico2d.load_image('ImageFolder/Enemy_Img.png')
    item_img = pico2d.load_image('ImageFolder/Item_Img.png')
    stageButton_img = pico2d.load_image('ImageFolder/StageButtons_Img.png')
    editButton_img = pico2d.load_image('ImageFolder/EditButton_Img.png')
    attack_img = pico2d.load_image('ImageFolder/Attack_Img.png')
    numbers_img = pico2d.load_image('ImageFolder/Numbers_Img.png')


def del_images():
    global player_img, structure_img, enemy_img, item_img, stageButton_img, editButton_img, attack_img, numbers_img
    del player_img, structure_img, enemy_img, item_img, stageButton_img, editButton_img, attack_img, numbers_img


def load_sound():
    global powerUp_wav, powerDown_wav, coin_wav, marioDies_wav, marioJump_wav, itemSprouting_wav, oneUp_wav
    global getHit_wav, enemyGetHit_wav, blockHeading_wav, throwingFireball_wav, bgm_mp3
    bgm_mp3 = pico2d.load_music('SoundFolder/BGM.mp3')
    oneUp_wav = pico2d.load_wav('SoundFolder/1-Up.wav')
    powerUp_wav = pico2d.load_wav('SoundFolder/Power up.wav')
    powerDown_wav = pico2d.load_wav('SoundFolder/Power down.wav')
    getHit_wav = pico2d.load_wav('SoundFolder/Get hit.wav')
    coin_wav = pico2d.load_wav('SoundFolder/Coin.wav')
    marioDies_wav = pico2d.load_wav('SoundFolder/Mario dies.wav')
    marioJump_wav = pico2d.load_wav('SoundFolder/Mario jump.wav')
    marioJump_wav.set_volume(50)
    itemSprouting_wav = pico2d.load_wav('SoundFolder/Item sprouting.wav')
    enemyGetHit_wav = pico2d.load_wav('SoundFolder/Enemy get hit.wav')
    blockHeading_wav = pico2d.load_wav('SoundFolder/Block heading.wav')
    throwingFireball_wav = pico2d.load_wav('SoundFolder/Throwing fireball.wav')


def del_sound():
    global powerUp_wav, powerDown_wav, coin_wav, marioDies_wav, marioJump_wav, itemSprouting_wav, oneUp_wav
    global getHit_wav, enemyGetHit_wav, blockHeading_wav, throwingFireball_wav, bgm_mp3
    del powerUp_wav, powerDown_wav, coin_wav, marioDies_wav, marioJump_wav, itemSprouting_wav, oneUp_wav
    del getHit_wav, enemyGetHit_wav, blockHeading_wav, throwingFireball_wav, bgm_mp3
