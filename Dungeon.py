#Dungeon Crawler

import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *
from button import *
import pytmx
from random import random

# HUD functions
def draw_player_health(surf, x, y, pct): #draws the players health above them
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:    #bar changes colour as health decreases
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

class Game:
    def __init__(self): #creates screen
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
        self.menu()
        self.pickup = False
        self.last_restart = 0
        self.mob_counter = 0
        self.auto = False

    def load_data(self): #loads all images 
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        snd_folder = path.join(game_folder, 'snd')
        music_folder = path.join(game_folder, 'music')
        self.map_folder = path.join(game_folder, 'maps')
        self.player_img = pg.transform.rotozoom(pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha(), 0, 1.2)
        #reloading img
        self.reloading_img = pg.transform.rotozoom(pg.image.load(path.join(img_folder, RELOADING_IMG)).convert_alpha(), 0, 0.8)
        self.idle_player_down_spritesheet = pg.image.load(path.join(img_folder, IDLE_PLAYER_DOWN_SPRITESHEET)).convert_alpha()
        #idle images
        self.idle_down_frames = {}
        self.idle_down_frames[0] = self.get_image(0, 17, 22, 5, BLACK, self.idle_player_down_spritesheet, False)
        self.idle_down_frames[1] = self.get_image(1, 17, 22, 5, BLACK, self.idle_player_down_spritesheet, False)
        self.idle_down_frames[2] = self.get_image(2, 17, 22, 5, BLACK, self.idle_player_down_spritesheet, False)
        self.idle_down_frames[3] = self.get_image(3, 17, 22, 5, BLACK, self.idle_player_down_spritesheet, False)
        self.idle_down_frames[4] = self.get_image(4, 17, 22, 5, BLACK, self.idle_player_down_spritesheet, False)
        self.idle_down_frames[5] = self.get_image(5, 17, 22, 5, BLACK, self.idle_player_down_spritesheet, False)
        #player idle right up
        self.idle_player_right_up_spritesheet = pg.image.load(path.join(img_folder, IDLE_PLAYER_LEFT_SPRITESHEET)).convert_alpha()
        self.idle_right_up_frames = {}
        self.idle_right_up_frames[0] = self.get_image(0, 16, 22, 5, BLACK, self.idle_player_right_up_spritesheet, True)
        self.idle_right_up_frames[1] = self.get_image(1, 16, 22, 5, BLACK, self.idle_player_right_up_spritesheet, True)
        self.idle_right_up_frames[2] = self.get_image(2, 16, 22, 5, BLACK, self.idle_player_right_up_spritesheet, True)
        self.idle_right_up_frames[3] = self.get_image(3, 16, 22, 5, BLACK, self.idle_player_right_up_spritesheet, True)
        #player idle right down
        self.idle_player_right_down_spritesheet = pg.image.load(path.join(img_folder, IDLE_PLAYER_RIGHT_SPRITESHEET)).convert_alpha()
        self.idle_right_down_frames = {}
        self.idle_right_down_frames[0] = self.get_image(0, 16, 24, 5, BLACK, self.idle_player_right_down_spritesheet, False)
        self.idle_right_down_frames[1] = self.get_image(1, 16, 24, 5, BLACK, self.idle_player_right_down_spritesheet, False)
        self.idle_right_down_frames[2] = self.get_image(2, 16, 24, 5, BLACK, self.idle_player_right_down_spritesheet, False)
        self.idle_right_down_frames[3] = self.get_image(3, 16, 24, 5, BLACK, self.idle_player_right_down_spritesheet, False)
        #player idle up
        self.idle_player_up_spritesheet = pg.image.load(path.join(img_folder, IDLE_PLAYER_UP_SPRITESHEET)).convert_alpha()
        self.idle_up_frames = {}
        self.idle_up_frames[0] = self.get_image(0, 17, 22, 5, BLACK, self.idle_player_up_spritesheet, False)
        self.idle_up_frames[1] = self.get_image(1, 17, 22, 5, BLACK, self.idle_player_up_spritesheet, False)
        self.idle_up_frames[2] = self.get_image(2, 17, 22, 5, BLACK, self.idle_player_up_spritesheet, False)
        self.idle_up_frames[3] = self.get_image(3, 17, 22, 5, BLACK, self.idle_player_up_spritesheet, False)
        self.idle_up_frames[4] = self.get_image(4, 17, 22, 5, BLACK, self.idle_player_up_spritesheet, False)
        self.idle_up_frames[5] = self.get_image(5, 17, 22, 5, BLACK, self.idle_player_up_spritesheet, False)
        #player idle left up
        self.idle_player_left_spritesheet = pg.image.load(path.join(img_folder, IDLE_PLAYER_LEFT_SPRITESHEET)).convert_alpha()
        self.idle_left_frames = {}
        self.idle_left_frames[0] = self.get_image(0, 16, 22, 5, BLACK, self.idle_player_left_spritesheet, False)
        self.idle_left_frames[1] = self.get_image(1, 16, 22, 5, BLACK, self.idle_player_left_spritesheet, False)
        self.idle_left_frames[2] = self.get_image(2, 16, 22, 5, BLACK, self.idle_player_left_spritesheet, False)
        self.idle_left_frames[3] = self.get_image(3, 16, 22, 5, BLACK, self.idle_player_left_spritesheet, False)
        #player idle left down
        self.idle_player_left_down_spritesheet = pg.image.load(path.join(img_folder, IDLE_PLAYER_RIGHT_SPRITESHEET)).convert_alpha()
        self.idle_left_down_frames = {}
        self.idle_left_down_frames[0] = self.get_image(0, 16, 24, 5, BLACK, self.idle_player_left_down_spritesheet, True)
        self.idle_left_down_frames[1] = self.get_image(1, 16, 24, 5, BLACK, self.idle_player_left_down_spritesheet, True)
        self.idle_left_down_frames[2] = self.get_image(2, 16, 24, 5, BLACK, self.idle_player_left_down_spritesheet, True)
        self.idle_left_down_frames[3] = self.get_image(3, 16, 24, 5, BLACK, self.idle_player_left_down_spritesheet, True)
        #player left up
        self.left_player_spritesheet = pg.image.load(path.join(img_folder, LEFT_PLAYER_SPRITESHEET)).convert_alpha()
        self.left_frames = {}
        self.left_frames[0] = self.get_image(0, 17, 24, 5, BLACK, self.left_player_spritesheet, False)
        self.left_frames[1] = self.get_image(1, 17, 24, 5, BLACK, self.left_player_spritesheet, False)
        self.left_frames[2] = self.get_image(2, 17, 24, 5, BLACK, self.left_player_spritesheet, False)
        self.left_frames[3] = self.get_image(3, 17, 24, 5, BLACK, self.left_player_spritesheet, False)
        self.left_frames[4] = self.get_image(4, 17, 24, 5, BLACK, self.left_player_spritesheet, False)
        self.left_frames[5] = self.get_image(5, 17, 24, 5, BLACK, self.left_player_spritesheet, False)
        #player right down
        self.right_player_spritesheet = pg.image.load(path.join(img_folder, RIGHT_PLAYER_SPRITESHEET)).convert_alpha()
        self.right_frames = {}
        self.right_frames[0] = self.get_image(0, 17, 24, 5, BLACK, self.right_player_spritesheet, False)
        self.right_frames[1] = self.get_image(1, 17, 24, 5, BLACK, self.right_player_spritesheet, False)
        self.right_frames[2] = self.get_image(2, 17, 24, 5, BLACK, self.right_player_spritesheet, False)
        self.right_frames[3] = self.get_image(3, 17, 24, 5, BLACK, self.right_player_spritesheet, False)
        self.right_frames[4] = self.get_image(4, 17, 24, 5, BLACK, self.right_player_spritesheet, False)
        self.right_frames[5] = self.get_image(5, 17, 24, 5, BLACK, self.right_player_spritesheet, False)
        #player up
        self.up_player_spritesheet = pg.image.load(path.join(img_folder, UP_PLAYER_SPRITESHEET)).convert_alpha()
        self.up_frames = {}
        self.up_frames[0] = self.get_image(0, 17, 24, 5, BLACK, self.up_player_spritesheet, False)
        self.up_frames[1] = self.get_image(1, 17, 24, 5, BLACK, self.up_player_spritesheet, False)
        self.up_frames[2] = self.get_image(2, 17, 24, 5, BLACK, self.up_player_spritesheet, False)
        self.up_frames[3] = self.get_image(3, 17, 24, 5, BLACK, self.up_player_spritesheet, False)
        self.up_frames[4] = self.get_image(4, 17, 24, 5, BLACK, self.up_player_spritesheet, False)
        self.up_frames[5] = self.get_image(5, 17, 24, 5, BLACK, self.up_player_spritesheet, False)
        #player down
        self.down_player_spritesheet = pg.image.load(path.join(img_folder, DOWN_PLAYER_SPRITESHEET)).convert_alpha()
        self.down_frames = {}
        self.down_frames[0] = self.get_image(0, 17, 24, 5, BLACK, self.down_player_spritesheet, False)
        self.down_frames[1] = self.get_image(1, 17, 24, 5, BLACK, self.down_player_spritesheet, False)
        self.down_frames[2] = self.get_image(2, 17, 24, 5, BLACK, self.down_player_spritesheet, False)
        self.down_frames[3] = self.get_image(3, 17, 24, 5, BLACK, self.down_player_spritesheet, False)
        self.down_frames[4] = self.get_image(4, 17, 24, 5, BLACK, self.down_player_spritesheet, False)
        self.down_frames[5] = self.get_image(5, 17, 24, 5, BLACK, self.down_player_spritesheet, False)
        #crosshair image
        self.crosshair_img = pg.image.load(path.join(img_folder, CROSSHAIR_IMG)).convert_alpha()
        #gun images
        self.gun_images = {}
        self.gun_images['pi'] = pg.transform.rotozoom(pg.image.load(path.join(img_folder, 'pistol.png')).convert_alpha(), 0, 1.5)
        self.gun_images['sh'] = pg.transform.rotozoom(pg.image.load(path.join(img_folder, 'shotgun.png')).convert_alpha(), 0, 1.2)
        self.gun_images['sn'] = pg.transform.rotozoom(pg.image.load(path.join(img_folder, 'sniper.png')).convert_alpha(), 0, 1.5)
        self.gun_images['uzi'] = pg.transform.rotozoom(pg.image.load(path.join(img_folder, 'uzi.png')).convert_alpha(), 0, 1.5)
        #bullet images
        self.bullet_images = {}
        self.bullet_images["pi"] = pg.transform.rotozoom(pg.image.load(path.join(img_folder, "pistol_bullet.png")).convert_alpha(), 0 , 1)
        self.bullet_images["sh"] = pg.transform.rotozoom(pg.image.load(path.join(img_folder, "shotgun_bullet.png")).convert_alpha(), 0 , 0.2)
        self.bullet_images["sn"] = pg.transform.rotozoom(pg.image.load(path.join(img_folder, "sniper_bullet.png")).convert_alpha(), 0 , 0.55)
        self.bullet_images["uzi"] = pg.transform.rotozoom(pg.image.load(path.join(img_folder, "pistol_bullet.png")).convert_alpha(), 0 , 0.55)
        #mob images
        self.mob_img = pg.transform.rotozoom(pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha(), 0 , 5)
        #
        self.heart_img = pg.transform.rotozoom(pg.image.load(path.join(img_folder, HEART_IMG)).convert_alpha(), 0 , 1.3)
        self.half_heart_img = pg.transform.rotozoom(pg.image.load(path.join(img_folder, HALF_HEART_IMG)).convert_alpha(), 0 , 1.3)
        self.gun_flashes = []
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.transform.rotozoom(pg.image.load(path.join(img_folder, ITEM_IMAGES[item])).convert_alpha(), 0, 2)
         # Sound loading
        pg.mixer.music.load(path.join(music_folder, BG_MUSIC))
        pg.mixer.music.set_volume(2)
        self.effects_sounds = {}
        for type in EFFECTS_SOUNDS:
            self.effects_sounds[type] = pg.mixer.Sound(path.join(snd_folder, EFFECTS_SOUNDS[type]))
        self.weapon_sounds = {}
        for weapon in WEAPON_SOUNDS:
            self.weapon_sounds[weapon] = []
            for snd in WEAPON_SOUNDS[weapon]:
                s = pg.mixer.Sound(path.join(snd_folder, snd))
                s.set_volume(0.3)
                self.weapon_sounds[weapon].append(s)
        self.zombie_moan_sounds = []
        for snd in ZOMBIE_MOAN_SOUNDS:
            s = pg.mixer.Sound(path.join(snd_folder, snd))
            s.set_volume(0.2)
            self.zombie_moan_sounds.append(s)
        self.player_hit_sounds = []
        for snd in PLAYER_HIT_SOUNDS:
            self.player_hit_sounds.append(pg.mixer.Sound(path.join(snd_folder, snd)))
        self.zombie_hit_sounds = []
        for snd in ZOMBIE_HIT_SOUNDS:
            self.zombie_hit_sounds.append(pg.mixer.Sound(path.join(snd_folder, snd)))
        #text font
        self.text_font = pg.font.SysFont(None, 64)



    def get_image(self, frame, width, height, scale, colour, sheet, flipped): #adjusts the player images before animation
        scale = 4
        image = pg.Surface((width, height)).convert_alpha()
        image.blit(sheet, (0, 0), ((frame * width), 0, width, height))
        if flipped:
            image = pg.transform.flip(pg.transform.scale(image, (width * scale, height * scale)), True, False)
        else:
            image = pg.transform.flip(pg.transform.scale(image, (width * scale, height * scale)), False, False)
        image.set_colorkey(colour)
        return image

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.player_bullets = pg.sprite.Group()
        self.mob_bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.mob_guns = pg.sprite.Group()
        self.map = TiledMap(path.join(self.map_folder, 'map1.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2,
                             tile_object.y + tile_object.height / 2)
            if tile_object.name == "player":
                self.player = Player(self, obj_center.x, obj_center.y, "player")
                self.gun = Gun(self, obj_center.x, obj_center.y)
            if tile_object.name == "mob":
                i = randint(0, 5)
                self.mob = Mob(self, obj_center.x, obj_center.y, MOB_WEAPON[i], self.mob_counter)
                self.mob_gun = Mob_Gun(self,obj_center.x, obj_center.y, MOB_WEAPON[i], self.mob_counter)
                self.mob_counter += 1
            if tile_object.name == "wall":
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name in ['health', 'shotgun', 'pistol', 'sniper', 'uzi']:
                Item(self,obj_center, tile_object.name)
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        self.menu = False
        self.options = False
        self.video = False
        self.audio = False
        self.keys = False
        self.effects_sounds['level_start'].play()

    def menu(self):
        game_folder = path.dirname(__file__)
        menu_folder = path.join(game_folder, "menu")
        self.resume_img = pg.image.load(path.join(menu_folder, RESUME_IMG)).convert_alpha()
        self.options_img = pg.image.load(path.join(menu_folder, OPTIONS_IMG)).convert_alpha()
        self.quit_img = pg.image.load(path.join(menu_folder, QUIT_IMG)).convert_alpha()
        self.audio_img = pg.image.load(path.join(menu_folder, AUDIO_IMG)).convert_alpha()
        self.back_img = pg.image.load(path.join(menu_folder, BACK_IMG)).convert_alpha()
        self.keys_img = pg.image.load(path.join(menu_folder, KEYS_IMG)).convert_alpha()
        self.video_img = pg.image.load(path.join(menu_folder, VIDEO_IMG)).convert_alpha()
    

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        pg.mixer.music.play(loops=-1)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if self.menu == True or self.options == True:
                pass
            else:
                self.update()
            self.draw()


    def quit(self):
        pg.quit()  #enables you to close tab
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
        #player hits items
        hits = pg.sprite.spritecollide(self.player, self.items, False)
        if self.pickup:
            for hit in hits:
                if hit.type == 'health' and self.player.lives < PLAYER_LIVES:
                    hit.kill()
                    self.player.add_health(HEALTH_PACK_AMOUNT)
                    self.effects_sounds['health_up'].play()
                if hit.type in ["shotgun", "pistol", "sniper", "uzi"]:
                    now1 = pg.time.get_ticks()
                    if now1 - self.player.last_hit >= PICKUP_DELAY:
                        self.player.last_hit = now1
                        #Item(self, self.player.pos, self.player.weapon)
                        hit.kill()
                        self.item = Item(self, self.player.pos, self.player.weapon)
                        self.effects_sounds['gun_pickup'].play()
                        self.player.weapon = hit.type
                        self.gun.kill()
                        self.gun = Gun(self, self.player.pos.x, self.player.pos.y)
        self.pickup = False
               
        # mobs hit player
        now = pg.time.get_ticks()
        if self.player.damaged == False:
            hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
            for hit in hits:
                choice(self.player_hit_sounds).play()
                self.player.lives -= 1
                self.player.hit()
                if self.player.lives <= 0:
                    self.playing = False 
            #bullet hits player    
            hits = pg.sprite.spritecollide(self.player, self.mob_bullets, False, collide_hit_rect)
            for hit in hits:
                choice(self.player_hit_sounds).play()
                self.player.lives -= 1
                self.player.hit()
                if self.player.lives <= 0:
                    self.playing = False
                hit.kill()
         # player_bullets hit mobs
        hits = pg.sprite.groupcollide(self.mobs, self.player_bullets, False, True)
        for hit in hits:
            hit.health -= WEAPONS[self.player.weapon]['damage'] * len(hits[hit])
            hit.vel = vec(0,0)
        
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw_lives(self, surf, x, y, lives):
            for i in range(lives):
                if i % 2 == 0: #checks which heart image it is first half or full half
                    img = self.half_heart_img
                    img_rect = img.get_rect()
                    img_rect.x = x + 25 * i
                    img_rect.y = y
                    surf.blit(img, img_rect)
                else:
                    img = self.heart_img
                    img_rect = img.get_rect()
                    img_rect.x = x + 25 * (i-1)
                    img_rect.y = y
                    surf.blit(img, img_rect)

    def draw_menu(self, surf, x, y): #draws thepause menu on screen
        self.resume_button = Button(x, y - 150, self.resume_img, 1)
        self.resume_button.draw(self.screen)
        if self.menu == True:
            if self.resume_button.draw(self.screen):
                self.menu = False
        self.options_button = Button(x, y - 70, self.options_img, 1)
        self.options_button.draw(self.screen)
        if self.menu == True:
            if self.options_button.draw(self.screen):
                self.options = True
                self.menu = False
        self.quit_button = Button(x, y + 10, self.quit_img, 1)
        self.quit_button.draw(self.screen)
        if self.menu == True:
            if self.quit_button.draw(self.screen):
                pg.quit() #ends game
                sys.exit() 
    
    def draw_options(self, surf, x, y): #draws options menu
        offset = 200
        if self.options == True and self.menu == False:
            self.video_button = Button(x + offset, y - 150, self.video_img, 1)
            self.video_button.draw(self.screen)
            if self.video_button.draw(self.screen):
                self.options = False
                self.video = True
            self.audio_button = Button(x+ offset, y - 70, self.audio_img, 1)
            self.audio_button.draw(self.screen)
            if self.audio_button.draw(self.screen):
                self.options = False
                self.audio = True
            self.keys_button = Button(x+ offset, y + 10, self.keys_img, 1)
            self.keys_button.draw(self.screen)
            if self.keys_button.draw(self.screen):
                self.options = False
                self.keys = True

    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw_crosshair(self): #replaces cursor with crosshair image
        pg.mouse.set_visible(False)
        self.rect = self.crosshair_img.get_rect()
        #print(self.rect)
        self.screen.blit(self.crosshair_img, vec(pg.mouse.get_pos()) - vec(16, 16))

    def draw_reloading(self):
        #player reloading
        if self.gun.player_reloading:
            self.screen.blit(self.reloading_img, (5, 40))
        #mob reloading

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        #self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        # self.draw_grid()
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)

        # pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
        # HUD functions
        self.draw_lives(self.screen, WIDTH - 150, 5, self.player.lives)
        if self.menu == True:
            self.draw_menu(self.screen, WIDTH/2 - BUTTON_WIDTH/2, HEIGHT/2)
        if self.options == True:
            self.draw_options(self.screen, WIDTH/2 - BUTTON_WIDTH/2, HEIGHT/2)
        #print("m", self.menu, "o", self.options, "v", self.video, "a", self.audio, "k", self.keys)  
        self.draw_text("{}s".format(math.trunc((pg.time.get_ticks() - self.last_restart)/1300)), "freesansbold.ttf", 30, WHITE, 5, 5)
        self.draw_crosshair()
        self.draw_reloading()
        pg.display.flip()
    
    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                self.auto = True
            if event.type == pg.MOUSEBUTTONUP:  
                self.auto = False
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.menu = not self.menu #toggles pause
                    self.options = False
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug
                if event.key == pg.K_c:
                    self.pickup = True
                else:
                    self.pickup = False

    def show_start_screen(self):
        pass

    def show_go_screen(self): #game over screen
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", "freesansbold.ttf", 100, RED,
                       WIDTH / 2, HEIGHT / 2, align="center")
        self.draw_text("Press a key to start", "freesansbold.ttf", 75, WHITE,
                       WIDTH / 2, HEIGHT * 3 / 4, align="center")
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False
                    self.last_restart = pg.time.get_ticks()

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()