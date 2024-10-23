#settings
import pygame as pg
import math
vec = pg.math.Vector2

#colour bank
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

#game settings
WIDTH = 1800    # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 1000    # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Dungeon Crawler"
BGCOLOR = DARKGREY

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

#player setting
PLAYER_SPEED = 450
DASH_LEGTH = 200
DASH_INTERVAL = 1500
PLAYER_IMG = "player.png"
IDLE_PLAYER_DOWN_SPRITESHEET = "idle_player_down_spritesheet.png"
IDLE_PLAYER_RIGHT_SPRITESHEET = "idle_player_right_spritesheet.png"
IDLE_PLAYER_UP_SPRITESHEET = "idle_player_up_spritesheet.png"
IDLE_PLAYER_LEFT_SPRITESHEET = "idle_player_left_spritesheet.png"
LEFT_PLAYER_SPRITESHEET = "left_player_spritesheet.png"
RIGHT_PLAYER_SPRITESHEET = "right_player_spritesheet.png"
DOWN_PLAYER_SPRITESHEET = "down_player_spritesheet.png"
UP_PLAYER_SPRITESHEET = "up_player_spritesheet.png"
PLAYER_HIT_RECT = pg.Rect(0, 0, 50, 80)
PLAYER_LIVES = 6
HEART_IMG = "heart.png"
HALF_HEART_IMG = "half heart.png"
I_FRAMES = 300
PLAYER_CENTER = [WIDTH / 2, HEIGHT / 2]

#mob settings
MOB_IMG = "mob.png"
MOB_SPEEDS = [150, 100, 120, 175, 150]
MOB_HIT_RECT = pg.Rect(0, 0, 60, 110)
MOB_HEALTH = 100
MOB_DAMAGE = 5
AVOID_RADIUS = 50
DETECT_RADIUS = 600
SHOOT_RADIUS = 1000

#weapon settings
RELOADING_IMG = "reloading!.png"
PLAYER_WEAPON = "pistol"
MOB_WEAPON = ["shotgun", "pistol", "sniper", "uzi","shotgun", "pistol"]
WEAPONS = {}
WEAPONS['pistol'] = {'bullet_speed': 10,
                     'bullet_lifetime': 1000000,
                     'rate': 400,
                     'kickback': 0,
                     'spread': 5,
                     'damage': 20,
                     'bullet_size': 'pi',
                     'bullet_count': 1,
                     'gun_img': "pistol.png",
                     'bullet_img': "pistol_bullet.png",
                     "mag_size": 10,
                     "reload_speed": 2500}
WEAPONS['shotgun'] = {'bullet_speed': 4,
                      'bullet_lifetime': 100000,
                      'rate': 900,
                      'kickback': 0,
                      'spread': 20,
                      'damage': 10,
                      'bullet_size': 'sh',
                      'bullet_count': 5,
                      'gun_img': "shotgun.png",
                      'bullet_img': "shotgun_bullet.png",
                      "mag_size": 2,
                      "reload_speed": 4000}
WEAPONS['sniper'] = {'bullet_speed': 15,
                      'bullet_lifetime': 100000,
                      'rate': 1500,
                      'kickback': 0,
                      'spread': 5,
                      'damage': MOB_HEALTH,
                      'bullet_size': 'sn',
                      'bullet_count': 1,
                      'gun_img': "sniper.png",
                      'bullet_img': "sniper_bullet.png",
                      "mag_size": 1,
                      "reload_speed": 4000}
WEAPONS['uzi'] = {'bullet_speed': 10,
                      'bullet_lifetime': 100000,
                      'rate': 75,
                      'kickback': 0,
                      'spread': 5,
                      'damage': 10,
                      'bullet_size': 'uzi',
                      'bullet_count': 1,
                      'gun_img': "uzi.png",
                      'bullet_img': "pistol_bullet.png",
                      "mag_size": 20,
                      "reload_speed": 4000}

GUN_HIT_RECT = pg.Rect(0, 0, 0, 0)
HANDLE_OFFSET = vec(20, 20)
BARREL_OFFSET = vec(8000, 1000)

#effects
MUZZLE_FLASHES = ['whitePuff15.png', 'whitePuff16.png', 'whitePuff17.png',
                  'whitePuff18.png']
FLASH_DURATION = 40
DAMAGE_ALPHA = [i for i in range(0, 255, 10)]

# Layers
WALL_LAYER = 1
PLAYER_LAYER = 7
BULLET_LAYER = 4
MOB_LAYER = 3
EFFECTS_LAYER = 5
GUN_LAYER = 8
ITEMS_LAYER = 1

#items
ITEM_IMAGES = {'health': 'health_pack.png',
               'shotgun': 'shotgun.png',
               'pistol': 'pistol.png',
               'sniper': 'sniper.png',
               'uzi': 'uzi.png'}
PICKUP_DELAY = 300
HEALTH_PACK_AMOUNT = 1
BOB_RANGE = 15
BOB_SPEED = 0.4

# Sounds
BG_MUSIC = "doom bg music.ogg"
PLAYER_HIT_SOUNDS = ["player hit.wav"]
ZOMBIE_MOAN_SOUNDS = ["temp.wav"]
ZOMBIE_HIT_SOUNDS = ["temp.wav"]
WEAPON_SOUNDS = {"pistol": ["pistol_shot.wav"],
                     "shotgun": ["shotgun_shot.wav"],
                     "sniper": ["sniper_shot.wav"],
                     "uzi": ["pistol_shot.wav"]}
EFFECTS_SOUNDS = {'level_start': 'start up.wav',
                  'health_up': 'health up.wav', 
                  'gun_pickup': 'gun_pickup.wav'}

#buttons
BUTTON_WIDTH = 266
BUTTON_HEIGHT = 50
AUDIO_IMG = "button_audio.png"
BACK_IMG = "button_back.png"
KEYS_IMG = "button_keys.png"
OPTIONS_IMG = "button_options.png"
QUIT_IMG = "button_quit.png"
RESUME_IMG = "button_resume.png"
VIDEO_IMG = "button_video.png"

#crosshair
CROSSHAIR_IMG = "crosshair.png"
