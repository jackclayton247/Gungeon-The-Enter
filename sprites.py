#sprites

import pygame as pg
from settings import *
from tilemap import *
import math
from os import path
vec = pg.math.Vector2
from random import uniform, choice, randint, random
import pytweening as tween
from itertools import chain

Mobs = {}
for x in range(100):
    Mobs[x] = {"pos": (0, 0),
                "angle": 0}

def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y
                

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y, sprite):    #sprite image
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.idle_down_frames[0]
        self.rect = self.image.get_rect()
        #hitbox
        self.rect.center = (x, y)
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)    #position
        self.last_shot = 0
        self.lives = PLAYER_LIVES
        self.last_hit = 0
        self.last_hit_hurt = 0
        self.last_pickup = 0
        self.weapon = PLAYER_WEAPON
        self.damaged = False
        self.animation_counter = 0 
        #player state
        self.gun_left = False
        self.running_left = False
        self.idle_left_up = False
        self.idle_left_down = False
        self.gun_right = False
        self.running_right = False
        self.idle_right_up = False
        self.idle_right_down = False
        self.gun_up = False
        self.running_up = False
        self.idle_up = False
        self.gun_down = False
        self.running_down = False
        self.idle_down = False
        self.dash_dir = vec(0, 0)

    def player_state(self):
        #gun direction
        if self.vel.x or self.vel.y != 0:
            if 90 <= self.game.gun.angle <= 180 or -180 <= self.game.gun.angle <= -90:
                self.gun_left = True 
            else:
                self.gun_left = False
            if -90 < self.game.gun.angle < 90:
                self.gun_right = True
            else:
                self.gun_right = False
            if -180 < self.game.gun.angle <= 0:
                self.gun_up = True
            else:
                self.gun_up = False
            if 0 < self.game.gun.angle < 180:
                self.gun_down = True
            else:
                self.gun_down = False
        else:
            self.gun_left = False
            self.gun_right = False
            self.gun_up = False
            self.gun_down = False
        #print("i = {}, l = {}, r - {}, u = {}, d = {}".format(self.idle, self.left, self.right, self.up, self.down))
        #movement direction
        if self.vel.x < 0: #left
            self.running_left = True
        else:
            self.running_left = False
        if self.vel.x > 0: #right
            self.running_right = True
        else:
            self.running_right = False
        if self.vel.y < 0: #up
            self.running_up = True
        else:
            self.running_up = False
        if self.vel.y > 0: #down
            self.running_down = True
        else:
            self.running_down = False
        #print("l = {}, r - {}, u = {}, d = {}".format(self.running_left, self.running_right, self.running_up, self.running_down))
        #idle direction
        if self.vel.x or self.vel.y == 0:
            if -180 < self.game.gun.angle <= -135:
                self.idle_left_up = True 
            else:
                self.idle_left_up = False
            if 135 < self.game.gun.angle <= 180:
                self.idle_left_down = True 
            else:
                self.idle_left_down = False
            if -45 < self.game.gun.angle <= 0:
                self.idle_right_up = True
            else:
                self.idle_right_up = False
            if 0 < self.game.gun.angle <= 45:
                self.idle_right_down = True
            else:
                self.idle_right_down = False
            if -135 < self.game.gun.angle <= -45:
                self.idle_up = True
            else:
                self.idle_up = False
            if 45 < self.game.gun.angle <= 135:
                self.idle_down = True
            else:
                self.idle_down = False
        else:
            self.idle_left_up = False
            self.idle_left_down = False
            self.idle_right_up = False
            self.idle_right_down = False
            self.idle_up = False
            self.idle_down = False
        
        #print("l = {}, r - {}, u = {}, d = {}".format(self.idle_left, self.idle_right, self.idle_up, self.idle_down))

    def get_keys(self):
        self.vel = vec(0, 0)   #catches movement events
        if self.game.gun.dashing == False:
            x = PLAYER_SPEED
            keys =pg.key.get_pressed()
            if keys[pg.K_LEFT] or keys[pg.K_a]:
                self.vel.x = -x
            if keys[pg.K_RIGHT] or keys[pg.K_d]:
                self.vel.x = x
            if keys[pg.K_UP] or keys[pg.K_w]:
                self.vel.y = -x
            if keys[pg.K_DOWN] or keys[pg.K_s]:
                self.vel.y = x
            if self.vel.x != 0 and self.vel.y != 0:
                self.vel *= 0.7071
        else:
            self.vel += 3 * self.dash_dir
        
    
    def hit(self):
        self.damaged = True
        self.damage_alpha = chain(DAMAGE_ALPHA * 4)
    
    def animate_player(self):
        #idle
        if self.idle_down:
            while self.animation_counter >= (len(self.game.idle_down_frames) * 9):
                self.animation_counter  = 0
            frame = math.trunc(self.animation_counter / 9)
            self.image = self.game.idle_down_frames[frame]
            self.animation_counter += 1
            self.game.screen.blit(self.image, (-1000,-10000))
            pg.display.flip()
        if self.idle_right_up:
            while self.animation_counter >= (len(self.game.idle_right_up_frames) * 13.5):
                self.animation_counter  = 0
            frame = math.trunc(self.animation_counter / 13.5)
            self.image = self.game.idle_right_up_frames[frame]
            self.animation_counter += 1
            self.game.screen.blit(self.image, (-1000,-10000))
            pg.display.flip()
        if self.idle_right_down:
            while self.animation_counter >= (len(self.game.idle_right_down_frames) * 13.5):
                self.animation_counter  = 0
            frame = math.trunc(self.animation_counter / 13.5)
            self.image = self.game.idle_right_down_frames[frame]
            self.animation_counter += 1
            self.game.screen.blit(self.image, (-1000,-10000))
            pg.display.flip()
        if self.idle_up:
            while self.animation_counter >= (len(self.game.idle_up_frames) * 9):
                self.animation_counter  = 0
            frame = math.trunc(self.animation_counter / 9)
            self.image = self.game.idle_up_frames[frame]
            self.animation_counter += 1
            self.game.screen.blit(self.image, (-1000,-10000))
            pg.display.flip()
        if self.idle_left_up:
            while self.animation_counter >= (len(self.game.idle_left_frames) * 13.5):
                self.animation_counter  = 0
            frame = math.trunc(self.animation_counter / 13.5)
            self.image = self.game.idle_left_frames[frame]
            self.animation_counter += 1
            self.game.screen.blit(self.image, (-1000,-10000))
            pg.display.flip()
        if self.idle_left_down:
            while self.animation_counter >= (len(self.game.idle_left_down_frames) * 13.5):
                self.animation_counter  = 0
            frame = math.trunc(self.animation_counter / 13.5)
            self.image = self.game.idle_left_down_frames[frame]
            self.animation_counter += 1
            self.game.screen.blit(self.image, (-1000,-10000))
            pg.display.flip()
        #running
        if self.running_left or self.running_right:
            if self.gun_left:
                while self.animation_counter >= (len(self.game.left_frames) * 9):
                    self.animation_counter  = 0
                frame = math.trunc(self.animation_counter / 9)
                self.image = self.game.left_frames[5 - frame]
                self.animation_counter += 1
                self.game.screen.blit(self.image, (-1000,-10000))
                pg.display.flip()
            if self.gun_right:
                while self.animation_counter >= (len(self.game.right_frames) * 9):
                    self.animation_counter  = 0
                frame = math.trunc(self.animation_counter / 9)
                self.image = self.game.right_frames[frame]
                self.animation_counter += 1
                self.game.screen.blit(self.image, (-1000,-10000))
                pg.display.flip()
        elif self.running_up or self.running_down:
            if self.gun_up:
                while self.animation_counter >= (len(self.game.up_frames) * 9):
                    self.animation_counter  = 0
                frame = math.trunc(self.animation_counter / 9)
                self.image = self.game.up_frames[frame]
                self.animation_counter += 1
                self.game.screen.blit(self.image, (-1000,-10000))
                pg.display.flip()
            if self.gun_down:
                while self.animation_counter >= (len(self.game.down_frames) * 9):
                    self.animation_counter  = 0
                frame = math.trunc(self.animation_counter / 9)
                self.image = self.game.down_frames[frame]
                self.animation_counter += 1
                self.game.screen.blit(self.image, (-1000,-10000))
                pg.display.flip()

    
    def update(self): #calls all the functions
        self.image = pg.transform.rotate(self.image.copy(), 0)
        if self.damaged:
            try:
                self.image.fill((255, 255, 255, next(self.damage_alpha)), special_flags=pg.BLEND_RGBA_MULT)
            except:
                self.damaged = False
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
        self.get_keys()
        self.animate_player()
        self.player_state()
    
    def add_health(self, amount):
        self.lives += amount
        if self.lives > PLAYER_LIVES:
            self.lives = PLAYER_LIVES

    

class Gun(pg.sprite.Sprite): #weapon image
    def __init__(self, game, x, y):
        self._layer = GUN_LAYER
        self.pos = vec(x+0.7, y+1.2) * TILESIZE
        self.groups = game.all_sprites,
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.gun_images[WEAPONS[game.player.weapon]["bullet_size"]]
        self.base_gun_image = self.image
        self.hitbox_rect = self.base_gun_image.get_rect(center = self.pos)
        self.rect = self.hitbox_rect.copy()
        self.hit_rect = GUN_HIT_RECT #hitbox
        self.vel = vec(0,0)
        self.offset = vec(10, 0)
        self.last_shot = 0
        self.rot = 0
        self.flipped = False  #tracks state
        tm = pytmx.load_pygame(path.join(path.join(path.dirname(__file__), 'maps'), 'map1.tmx'), pixelalpha=True) #map width/height
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.scroll_lim_x = False
        self.scroll_lim_y = False
        self.angle = 0
        self.shots_fired = 0
        self.player_reloading = False
        self.dashing = False
        self.last_dash = False

    def gun_rotation(self): #roates the gun sprite to point the cursor
        if self.scroll_lim_x == True and self.scroll_lim_y == True:
            if self.game.player.pos.x < WIDTH / 2 and self.game.player.pos.y < HEIGHT / 2:
                self.mouse_coords = pg.mouse.get_pos()
            elif self.width - WIDTH / 2 < self.game.player.pos.x and self.game.player.pos.y < HEIGHT / 2: #top right
                self.mouse_coords = vec((self.width - WIDTH),0) + pg.mouse.get_pos()
            elif self.game.player.pos.x < WIDTH / 2 and self.height - HEIGHT / 2 < self.game.player.pos.y: #top left
                self.mouse_coords = vec(0,(self.height - HEIGHT)) + pg.mouse.get_pos()
            else:
                self.mouse_coords = vec((self.width - WIDTH),(self.height - HEIGHT)) + pg.mouse.get_pos()
        elif self.scroll_lim_x == True:
            if self.game.player.pos.x < WIDTH / 2:
                self.mouse_coords = vec(0,self.pos.y) - vec(0,(HEIGHT/2)) + pg.mouse.get_pos()
            else:
                self.mouse_coords = vec((self.width - WIDTH), self.game.player.pos.y - HEIGHT / 2) + pg.mouse.get_pos()
        elif self.scroll_lim_y == True:
            if self.game.player.pos.y < HEIGHT / 2:
                self.mouse_coords = vec(self.pos.x, 0) - vec((WIDTH/2), 0) + pg.mouse.get_pos()
            else:
                self.mouse_coords = vec((self.game.player.pos.x - WIDTH / 2, self.height - HEIGHT)) + pg.mouse.get_pos()
        else:
            self.mouse_coords = self.pos - PLAYER_CENTER + pg.mouse.get_pos()
        self.x_change_mouse_gun = (self.mouse_coords[0] - self.hitbox_rect.centerx)
        self.y_change_mouse_gun = (self.mouse_coords[1] - self.hitbox_rect.centery)
        self.angle = math.degrees(math.atan2(self.y_change_mouse_gun, self.x_change_mouse_gun))
        self.image = pg.transform.rotate(self.base_gun_image, -self.angle)
        offset_rotated = self.offset.rotate(self.angle)
        self.rect = self.image.get_rect(center = self.pos + offset_rotated)
        if self.flipped:
            if -70 < self.angle < 70:
                self.flipped = False
                #self.pos = self.game.player.pos + HANDLE_OFFSET
                self.base_gun_image = pg.transform.flip(self.base_gun_image, False, True)
        else:
            if -180 < self.angle < -110 or 110 < self.angle <= 180:
                self.flipped = True
                #self.pos = vec(self.game.player.pos.x - HANDLE_OFFSET.x, self.game.player.pos.y + HANDLE_OFFSET.y)
                self.base_gun_image = pg.transform.flip(self.base_gun_image, False, True) 
        if self.flipped:
            self.pos = vec(self.game.player.pos.x - HANDLE_OFFSET.x, self.game.player.pos.y + HANDLE_OFFSET.y)
        else:
            self.pos = self.game.player.pos + HANDLE_OFFSET
                 

    def get_keys(self):
        self.vel = vec(0, 0)   #catches movement events
        keys =pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -PLAYER_SPEED
            self.hitbox_rect.center = self.pos
            self.rect.center = self.hitbox_rect.center
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = PLAYER_SPEED
            self.hitbox_rect.center = self.pos
            self.rect.center = self.hitbox_rect.center
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -PLAYER_SPEED
            self.hitbox_rect.center = self.pos
            self.rect.center = self.hitbox_rect.center
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = PLAYER_SPEED
            self.hitbox_rect.center = self.pos
            self.rect.center = self.hitbox_rect.center
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071
        if keys[pg.K_SPACE]:
            if self.game.player.vel != [0, 0] and self.dashing != True and pg.time.get_ticks() - self.last_dash > DASH_INTERVAL:
                self.dashing = True
                self.game.player.dash_dir = self.game.player.vel
                self.time_of_dash_start = pg.time.get_ticks()
        if self.shots_fired >= WEAPONS[self.game.player.weapon]["mag_size"]:
            self.player_reloading = True
            self.reload()
        if self.game.auto == True:
            if self.player_reloading == False:
                self.shoot()
                
            
        #print(self.shots_fired, WEAPONS[self.game.player.weapon]["mag_size"], self.reloading)
    def dash_timer(self):
        now = pg.time.get_ticks()
        if now - self.time_of_dash_start > DASH_LEGTH:
            self.dashing = False
            self.last_dash = pg.time.get_ticks()
                
            
    def shoot(self):
        now = pg.time.get_ticks()
        self.hitbox_rect.center = self.pos
        self.rect.center = self.hitbox_rect.center
        if now - self.last_shot > WEAPONS[self.game.player.weapon]["rate"]:
            snd = choice(self.game.weapon_sounds[self.game.player.weapon])
            if snd.get_num_channels() > 2:
                snd.stop()
            snd.play()
            self.last_shot = now
            dir = vec(1, 0).rotate(-self.rot)
            pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
            for i in range(1,WEAPONS[self.game.player.weapon]["bullet_count"] + 1, 1):
                num_bullets = WEAPONS[self.game.player.weapon]["bullet_count"]
                mid_bullet = ((num_bullets+ 1) / 2)
                if i < mid_bullet:
                    self.spread = (-10) * i 
                if i == mid_bullet:
                    self.spread = 0
                if i > mid_bullet and i < num_bullets + 1:
                    self.spread = 10 * (i - mid_bullet)
                Player_Bullet(self.game, pos, dir, self.spread)
            self.vel = vec(-WEAPONS[self.game.player.weapon]["kickback"], 0).rotate(-self.rot)
            magnitude_flash = math.sqrt(self.game.gun.x_change_mouse_gun **2 + self.game.gun.y_change_mouse_gun **2)
            MuzzleFlash(self.game, [self.game.gun.x_change_mouse_gun / magnitude_flash * 40, self.game.gun.y_change_mouse_gun / magnitude_flash * 40] + self.game.gun.pos)
            self.shots_fired = self.shots_fired + 1
            self.time_of_last_shot = pg.time.get_ticks()

    def reload(self):
        now = pg.time.get_ticks()
        if now - self.time_of_last_shot > WEAPONS[self.game.player.weapon]["reload_speed"]:
            self.shots_fired = 0
            self.player_reloading = False 

    def map_scrolling_limited(self):
        if self.width - WIDTH / 2 < self.game.player.pos.x or self.game.player.pos.x < WIDTH / 2:
            self.scroll_lim_x = True
        else:
            self.scroll_lim_x = False
        if self.height - HEIGHT / 2 < self.game.player.pos.y or self.game.player.pos.y < HEIGHT / 2:
            self.scroll_lim_y = True
        else:
            self.scroll_lim_y = False

    def update(self):  #calls all the functions
        self.get_keys()
        self.gun_rotation()
        self.map_scrolling_limited()
        if self.dashing:
            self.dash_timer()
    
class Player_Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, spread):
        self._layer = BULLET_LAYER
        self.groups = game.all_sprites, game.player_bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bullet_images[WEAPONS[game.player.weapon]["bullet_size"]] #sprite image
        self.rect = self.image.get_rect()
        magnitude_bullet = math.sqrt(self.game.gun.x_change_mouse_gun **2 + self.game.gun.y_change_mouse_gun **2)  #for unit vector calc
        self.pos = [self.game.gun.x_change_mouse_gun / magnitude_bullet * 40, self.game.gun.y_change_mouse_gun / magnitude_bullet * 40] + self.game.gun.pos  #spawn the bullet based on the gun pos and a factor of the unit vector
        self.rect.center = pos #center
        self.vel = vec(1, 0).rotate(self.game.gun.angle + spread)
        self.vel = vec(self.vel.x*WEAPONS[self.game.player.weapon]["bullet_speed"], self.vel.y*WEAPONS[self.game.player.weapon]["bullet_speed"])
        #self.vel = dir * WEAPONS[game.player.weapon]["bullet_speed"]
        self.spawn_time = pg.time.get_ticks()
        self.base_bullet_image = self.image
        if self.game.player.weapon == "pistol" or self.game.player.weapon == "sniper" or self.game.player.weapon == "uzi":
            self.image = pg.transform.rotate(self.base_bullet_image, -self.game.gun.angle)  #rotate based on function in gun class
        if self.game.player.weapon == "shotgun":
            self.image = pg.transform.rotate(self.base_bullet_image, -self.game.gun.angle - spread)
        self.rect = self.image.get_rect(center = self.pos)
        self.hit_rect = self.rect
        #print(spread)

    def update(self): #calls all funtions
        self.pos += (self.vel)
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > WEAPONS[self.game.player.weapon]["bullet_lifetime"]:
            self.kill()

class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y, weapon, mob_num):
        self._layer = WALL_LAYER
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob_img.copy() # sprite image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y) #hitbox
        self.hit_rect = MOB_HIT_RECT.copy() 
        self.hit_rect.center = self.rect.center
        offset = vec(30, 0)
        self.pos = vec(x, y)  #postion
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = MOB_HEALTH
        self.speed = choice(MOB_SPEEDS)
        self.target = game.player
        self.weapon = weapon
        self.last_shot = 0
        self.shots_fired_mob = 0
        self.mob_num = mob_num
        print(weapon)
        #print(mob_num)

    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < AVOID_RADIUS:
                    self.acc = dist.normalize()

    def angle_to_player(self):
        self.change = self.game.player.pos - self.pos
        self.angle = math.degrees(math.atan2(self.change.y, self.change.x))

    def shoot(self, weapon):
        now = pg.time.get_ticks()
        self.hit_rect.center = self.pos
        self.rect.center = self.hit_rect.center
        if now - self.last_shot > WEAPONS[weapon]["rate"]:
            snd = choice(self.game.weapon_sounds[weapon])
            if snd.get_num_channels() > 2:
                snd.stop()
            #snd.play()
            self.last_shot = now
            dir = vec(1, 0).rotate(-self.rot)
            pos = self.pos
            for i in range(1,WEAPONS[weapon]["bullet_count"] + 1, 1):
                num_bullets = WEAPONS[weapon]["bullet_count"]
                mid_bullet = ((num_bullets+ 1) / 2)
                if i < mid_bullet:
                    self.spread = (WEAPONS[weapon]["spread"]) * i 
                if i == mid_bullet:
                    self.spread = 0
                if i > mid_bullet and i < num_bullets + 1:
                    self.spread = -WEAPONS[weapon]["spread"] * (i - mid_bullet)
                self.mob_bullet = Mob_Bullet(self.game, self.pos, dir, self.spread, self.rot, weapon)
            self.time_of_last_shot_mob = pg.time.get_ticks()
            self.shots_fired_mob += 1

    def update(self): #calls funtion
        target_dist_squared =  (self.target.pos.x - self.pos.x)**2 + (self.target.pos.y - self.pos.y)**2
        if target_dist_squared < DETECT_RADIUS**2:
            self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
            self.image = self.game.mob_img
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.avoid_mobs()
            self.vel = vec(0, 1).rotate(-self.rot - 90) + self.acc
            self.pos += self.vel 
            self.hit_rect.centerx = self.pos.x              
            collide_with_walls(self, self.game.walls, 'x')
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')
            self.rect.center = self.hit_rect.center
            if target_dist_squared < SHOOT_RADIUS**2:
                if self.shots_fired_mob < WEAPONS[self.weapon]["mag_size"]:
                    self.shoot(self.weapon)
        if self.shots_fired_mob >= WEAPONS[self.weapon]["mag_size"]:       
            self.reload()#self.weapon
        if self.health <= 0:
            self.kill()
            self.pos = (-100000, -100000)
            print(Mobs[self.mob_num])
        self.angle_to_player()
        Mobs[self.mob_num]["pos"] = self.pos
        Mobs[self.mob_num]["angle"] = self.angle
        #print(self.shots_fired_mob)
    
    def reload(self):
        now = pg.time.get_ticks()
        if now - self.time_of_last_shot_mob > WEAPONS[self.weapon]["reload_speed"]:
            self.shots_fired_mob = 0

    def draw_health(self):
        health_surface = pg.Surface((self.rect.width, 7))  # Create a new surface for the health bar
        if self.health > 60:
            col = GREEN
        elif self.health > 30:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / MOB_HEALTH)
        health_bar = pg.Rect(0, 0, width, 7)
        empty_bar = pg.Rect(width, 0, self.rect.width - width, 7)
        pg.draw.rect(health_surface, col, health_bar)  # Draw the health bar on the health surface
        pg.draw.rect(health_surface, BLACK, empty_bar)
        self.image.blit(health_surface, (0, 0))  # Blit the health surface onto the sprite's image

class Mob_Gun(pg.sprite.Sprite):
    def __init__(self, game, x, y, weapon, num):
        self._layer = GUN_LAYER
        self.groups = game.all_sprites, game.mob_guns
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.gun_images[WEAPONS[weapon]["bullet_size"]]
        self.base_bullet_image = self.image
        self.pos = vec(x, y)
        self.rect = self.image.get_rect()
        self.num = num
        self.offset = vec(50, 0)
        self.hit_rect = self.image.get_rect()
    
    def rotate(self):
        self.image = pg.transform.rotate(self.base_bullet_image, -Mobs[self.num]["angle"])
        offset_rotated = self.offset.rotate(Mobs[self.num]["angle"])
        self.rect = self.image.get_rect(center = self.pos + offset_rotated)

    def update(self):
        #print(Mobs[self.num])
        if Mobs[self.num] == (-100000, -100000):
            self.kill()
        self.pos = Mobs[self.num]["pos"]
        self.rect.center = self.pos
        self.rotate()
        self.hit_rect = self.image.get_rect()


class Mob_Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, spread, angle, weapon):
        self._layer = EFFECTS_LAYER
        self.groups = game.all_sprites, game.mob_bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bullet_images[WEAPONS[weapon]["bullet_size"]] #sprite image
        self.rect = self.image.get_rect()
        self.vel = vec(0, 1).rotate(-angle - 90 + spread) * WEAPONS[weapon]["bullet_speed"]
        #self.vel = vec(self.vel.x*WEAPONS[self.game.mob.weapon]["bullet_speed"], self.vel.y*-WEAPONS[self.game.mob.weapon]["bullet_speed"])
        self.pos = pos + dir * 90  #spawn the bullet based on the gun pos and a factor of the unit vector
        self.rect.center = pos #center
        #self.vel = dir * WEAPONS[game.player.weapon]["bullet_speed"]
        self.spawn_time = pg.time.get_ticks()
        self.base_bullet_image = self.image
        if weapon != "shotgun":
            self.image = pg.transform.rotate(self.base_bullet_image, angle)  #rotate based on function in gun class
        if weapon == "shotgun":
            self.image = pg.transform.rotate(self.base_bullet_image, angle - spread)
        self.rect = self.image.get_rect(center = self.pos)
        self.hit_rect = self.rect
        #print(spread)

    def update(self): #calls all funtions
        self.pos += (self.vel)
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > WEAPONS[self.game.mob.weapon]["bullet_lifetime"]:
            self.kill()
          
        
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):   #sprite image
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class MuzzleFlash(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = EFFECTS_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        size = randint(20, 50)
        self.image = pg.transform.scale(choice(game.gun_flashes), (size, size))
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect.copy()
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > FLASH_DURATION:
            self.kill()

class Item(pg.sprite.Sprite):
    def __init__(self, game, pos, type):
        self._layer = ITEMS_LAYER
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.item_images[type]
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect.copy()
        self.type = type
        self.rect.center = pos
        self.pos = pos
        self.pos_y = self.pos.y
        self.tween = tween.easeInOutSine
        self.step = 0
        self.dir = 1
    
    def update(self):
        # bobbing motion
        offset = BOB_RANGE * (self.tween(self.step / BOB_RANGE) - 0.5)
        self.rect.centery = self.pos_y + offset * self.dir
        self.step += BOB_SPEED
        if self.step > BOB_RANGE:
            self.step = 0
            self.dir *= -1
