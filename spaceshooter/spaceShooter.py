#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: tasdik
# @Contributers : Branden (Github: @bardlean86)
# @Date:   2016-01-17
# @Email:  prodicus@outlook.com  Github: @tasdikrahman
# @Last Modified by:   tasdik
# @Last Modified by:   Branden
# @Last Modified by:   Dic3
# @Last Modified time: 2016-10-16
# MIT License. You can find a copy of the License @ http://prodicus.mit-license.org

## Game music Attribution
##Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3 <http://creativecommons.org/licenses/by/3.0/>

## Additional assets by: Branden M. Ardelean (Github: @bardlean86)

from __future__ import division
import pygame
import random
import time
import os
import sqlite3

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')
from os import path

## assets folder
img_dir = path.join(path.dirname(__file__), 'assets')
sound_folder = path.join(path.dirname(__file__), 'sounds')

###############################
## to be placed in "constant.py" later
WIDTH = 480
HEIGHT = 600
FPS = 60
POWERUP_TIME = 5000
BAR_LENGTH = 100
BAR_HEIGHT = 10

# Define Colors 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
###############################

###############################
## to placed in "__init__.py" later
## initialize pygame and create window
pygame.init()
pygame.mixer.init()  ## For sound
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()     ## For syncing the FPS
###############################

font_name = pygame.font.match_font('arial')

#wave(stage) 함수
def count_wave(wavecounter):
    if wavecounter >= 0 and wavecounter <=200:
        return 1
    elif wavecounter > 200 and wavecounter <=400:
        return 2
    elif wavecounter > 400 and wavecounter <= 600:
        return 3
    elif wavecounter > 600 :
        return 4

def main_menu():
    global screen

    menu_song = pygame.mixer.music.load(path.join(sound_folder, "menu.ogg"))
    pygame.mixer.music.play(-1)

    title = pygame.image.load(path.join(img_dir, "main.png")).convert()
    score_background = pygame.image.load(path.join(img_dir, "starfield1.png")).convert()
    showHiScores = False
    pygame.display.update()
    font = pygame.font.Font(None, 36)

    hiScores = Database.getScores()
    highScoreTexts = [
                        font.render("NAME", 1, WHITE),
                        font.render("SCORE", 1, WHITE)
                        ]
    highScorePos = [highScoreTexts[0].get_rect(
                    topleft=screen.get_rect().inflate(-100, -100).topleft),
                    highScoreTexts[1].get_rect(
                    topright=screen.get_rect().inflate(-100, -100).topright)]
    for hs in hiScores:
        highScoreTexts.extend([font.render(str(hs[x]), 1, BLUE)
                                for x in range(2)])
        highScorePos.extend([highScoreTexts[x].get_rect(
            topleft=highScorePos[x].bottomleft) for x in range(-2, 0)])

    while True:
        
        title = pygame.transform.scale(title, (WIDTH, HEIGHT), screen)
        pygame.display.update()
        for event in pygame.event.get():
            # if event.type == pygame.KEYDOWN:
            # showHiScores = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                #pygame.mixer.music.stop()
                ready = pygame.mixer.Sound(path.join(sound_folder, 'getready.ogg'))
                ready.play()
                screen.fill(BLACK)
                draw_text(screen, "GET READY!", 40, WIDTH/2, HEIGHT/2)
                pygame.display.update()
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                pygame.quit()
                quit()
            # 스코어 추가
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s: 
                showHiScores = True
            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and showHiScores == True):
                showHiScores = False
                screen.fill((0,0,0))
                continue
            elif event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

        if showHiScores:
            screen.blit(score_background, (0, 0))
            textOverlays = zip(highScoreTexts, highScorePos)
            for txt, pos in textOverlays:
                screen.blit(txt, pos)
        else:
            # TODO: 이상하게 스코어를 조회하고 다시 돌아오면 화면이 안돌아온다...
            screen.blit(title, (0, 0))
            draw_text(screen, "Press [ENTER] To Begin", 30, WIDTH/2, HEIGHT/2)
            draw_text(screen, "or [Q] To Quit", 30, WIDTH/2, (HEIGHT/2)+40)
            draw_text(screen, "or [S] To Score", 30, WIDTH/2, (HEIGHT/2)+80)
        pygame.display.flip()

class Keyboard(object):
    keys = {pygame.K_a: 'A', pygame.K_b: 'B', pygame.K_c: 'C', pygame.K_d: 'D',
            pygame.K_e: 'E', pygame.K_f: 'F', pygame.K_g: 'G', pygame.K_h: 'H',
            pygame.K_i: 'I', pygame.K_j: 'J', pygame.K_k: 'K', pygame.K_l: 'L',
            pygame.K_m: 'M', pygame.K_n: 'N', pygame.K_o: 'O', pygame.K_p: 'P',
            pygame.K_q: 'Q', pygame.K_r: 'R', pygame.K_s: 'S', pygame.K_t: 'T',
            pygame.K_u: 'U', pygame.K_v: 'V', pygame.K_w: 'W', pygame.K_x: 'X',
            pygame.K_y: 'Y', pygame.K_z: 'Z'}

def scoreBorder(highScore):
    font = pygame.font.Font(None, 36)
    hiScores = Database.getScores()
    isHiScore = len(hiScores) < Database.numScores or score > hiScores[-1][1]
    name = ''
    nameBuffer = []
    
    score_background = pygame.image.load(path.join(img_dir, "starfield1.png")).convert()
    while True:

    # Event Handling
        for event in pygame.event.get():
            if (event.type == pygame.QUIT
                or not isHiScore
                and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_ESCAPE):
                return False
            elif (event.type == pygame.KEYDOWN
                  and event.key == pygame.K_RETURN
                  and not isHiScore):
                return True
            elif (event.type == pygame.KEYDOWN
                  and event.key in Keyboard.keys.keys()
                  and len(nameBuffer) < 8):
                nameBuffer.append(Keyboard.keys[event.key])
                name = ''.join(nameBuffer)
            elif (event.type == pygame.KEYDOWN
                  and event.key == pygame.K_BACKSPACE
                  and len(nameBuffer) > 0):
                nameBuffer.pop()
                name = ''.join(nameBuffer)
            elif (event.type == pygame.KEYDOWN
                  and event.key == pygame.K_RETURN
                  and len(name) > 0):
                Database.setScore(hiScores, (name, score))
                return True

        if isHiScore:
            hiScoreText = font.render('HIGH SCORE!', 1, RED)
            hiScorePos = hiScoreText.get_rect(
                midbottom=screen.get_rect().center)
            scoreText = font.render(str(score), 1, BLUE)
            scorePos = scoreText.get_rect(midtop=hiScorePos.midbottom)
            enterNameText = font.render('ENTER YOUR NAME:', 1, RED)
            enterNamePos = enterNameText.get_rect(midtop=scorePos.midbottom)
            nameText = font.render(name, 1, BLUE)
            namePos = nameText.get_rect(midtop=enterNamePos.midbottom)
            textOverlay = zip([hiScoreText, scoreText,
                               enterNameText, nameText],
                              [hiScorePos, scorePos,
                               enterNamePos, namePos])
        else:
            gameOverText = font.render('GAME OVER', 1, BLUE)
            gameOverPos = gameOverText.get_rect(
                center=screen.get_rect().center)
            scoreText = font.render('SCORE: {}'.format(score), 1, BLUE)
            scorePos = scoreText.get_rect(midtop=gameOverPos.midbottom)
            textOverlay = zip([gameOverText, scoreText],
                              [gameOverPos, scorePos])
    
    # Update and draw all sprites
        screen.blit(score_background, (0, 0))
        for txt, pos in textOverlay:
            screen.blit(txt, pos)
        pygame.display.flip()

# 점수 저장하는 db 클래스
class Database(object):
    path = os.path.join(data_dir, 'score.db')
    numScores = 15

    @staticmethod
    def getScores():
        conn = sqlite3.connect(Database.path)
        c = conn.cursor()
        c.execute('''CREATE TABLE if not exists scores (name text, score integer)''')
        c.execute("SELECT * FROM scores ORDER BY score DESC")
        hiScores = c.fetchall()
        conn.close()
        return hiScores

    @staticmethod
    def setScore(hiScores, entry):
        conn = sqlite3.connect(Database.path)
        c = conn.cursor()
        if len(hiScores) == Database.numScores:
            lowScoreName = hiScores[-1][0]
            lowScore = hiScores[-1][1]
            c.execute("DELETE FROM scores WHERE (name = ? AND score = ?)", (lowScoreName, lowScore))
        c.execute("INSERT INTO scores VALUES (?,?)", entry)
        conn.commit()
        conn.close()

def draw_text(surf, text, size, x, y):
    ## selecting a cross platform font to display the score
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)       ## True denotes the font to be anti-aliased 
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_shield_bar(surf, x, y, pct):
    # if pct < 0:
    #     pct = 0
    pct = max(pct, 0) 
    ## moving them to top
    # BAR_LENGTH = 100
    # BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect= img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)



def newmob(wave):
    if wave == 1:
        mob_element = Mob()
        all_sprites.add(mob_element)
        mobs.add(mob_element)
        
    elif wave == 2:
        Mob.image_orig = random.choice(ghost_images)
        mob_element = Mob()
        mob_element.mobchange()        
        all_sprites.add(mob_element)
        mobs.add(mob_element)
        
    elif wave == 3:
        Mob.image_orig = random.choice(cockpit_images)
        mob_element = Mob()
        mob_element.mobchange2()
        all_sprites.add(mob_element)
        mobs.add(mob_element)
        
    elif wave == 4:
        Mob.image_orig = random.choice(cockpit2_images)
        mob_element = Mob()
        mob_element.mobchange3()        
        all_sprites.add(mob_element)
        mobs.add(mob_element)        


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0 
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        ## scale the player img down
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.invincibility = 2000   # 무적시간 2초
        self.power_count = 30
        self.power_count_text = "∞"
        self.bomb_count = 1

    def update(self):
        ## time out for powerups
#        if self.power >=2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
        if self.power >=2 and self.power_count == 0:
            self.power = 1
            self.power_count = 30
#            self.power_time = pygame.time.get_ticks()

        ## unhide 
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 30

        self.speedx = 0     ## makes the player static in the screen by default. 
        # then we have to check whether there is an event hanlding being done for the arrow keys being 
        ## pressed
        self.speedy = 0

        ## will give back a list of the keys which happen to be pressed down at that moment
        keystate = pygame.key.get_pressed()
        ## 대각선으로 이동 가능하게 하는 기능
        if (keystate[pygame.K_UP] and keystate[pygame.K_RIGHT]):
            self.speedx = 5
            self.speedy = -5
        elif (keystate[pygame.K_UP] and keystate[pygame.K_LEFT]):
            self.speedx = -5
            self.speedy = -5
        elif (keystate[pygame.K_DOWN] and keystate[pygame.K_RIGHT]):
            self.speedx = 5
            self.speedy = +5
        elif (keystate[pygame.K_DOWN] and keystate[pygame.K_LEFT]):
            self.speedx = -5
            self.speedy = +5
        elif keystate[pygame.K_LEFT]:
            self.speedx = -5
        elif keystate[pygame.K_RIGHT]:
            self.speedx = 5
        elif keystate[pygame.K_UP]: #화살표 위 클릭시 y 좌표 -5
            self.speedy = -5
        elif keystate[pygame.K_DOWN]: #화살표 아래 클릭시 y 좌표 5
            self.speedy = +5

        #Fire weapons by holding spacebar
        if keystate[pygame.K_SPACE]:
            self.shoot()
        if keystate[pygame.K_z]:
            self.bomb_shoot()
        #z누르면 폭탄나감

        ## check for the borders at the left and right
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
            
        if self.rect.bottom > HEIGHT-10: #바닥 제한 설정
            self.rect.bottom = HEIGHT-10

        self.rect.x += self.speedx
        self.rect.y += self.speedy

    #폭탄 발사 함수 생성
    def bomb_shoot(self):
        now = pygame.time.get_ticks()
        if self.bomb_count >= 1:
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                bomb1 = Bomb(self.rect.centerx-160, self.rect.centery+80)
                bomb2 = Bomb(self.rect.centerx-140, self.rect.centery+70)
                bomb3 = Bomb(self.rect.centerx-120, self.rect.centery+60)
                bomb4 = Bomb(self.rect.centerx-100, self.rect.centery+50)
                bomb5 = Bomb(self.rect.centerx-80, self.rect.centery+40)
                bomb6 = Bomb(self.rect.centerx-60, self.rect.centery+30)
                bomb7 = Bomb(self.rect.centerx-40, self.rect.centery+20)
                bomb8 = Bomb(self.rect.centerx-20, self.rect.centery+10)
                bomb9 = Bomb(self.rect.centerx, self.rect.top)#센터
                bomb10 = Bomb(self.rect.centerx+20, self.rect.centery+10)
                bomb11 = Bomb(self.rect.centerx+40, self.rect.centery+20)
                bomb12 = Bomb(self.rect.centerx+60, self.rect.centery+30)
                bomb13 = Bomb(self.rect.centerx+80, self.rect.centery+40)
                bomb14 = Bomb(self.rect.centerx+100, self.rect.centery+50)
                bomb15 = Bomb(self.rect.centerx+120, self.rect.centery+60)
                bomb16 = Bomb(self.rect.centerx+140, self.rect.centery+70)
                bomb17 = Bomb(self.rect.centerx+160, self.rect.centery+80)           
                all_sprites.add(bomb1)
                all_sprites.add(bomb2)
                all_sprites.add(bomb3)
                all_sprites.add(bomb4)
                all_sprites.add(bomb5)
                all_sprites.add(bomb6)
                all_sprites.add(bomb7)
                all_sprites.add(bomb8)
                all_sprites.add(bomb9)
                all_sprites.add(bomb10)
                all_sprites.add(bomb11)
                all_sprites.add(bomb12)
                all_sprites.add(bomb13)
                all_sprites.add(bomb14)
                all_sprites.add(bomb15)
                all_sprites.add(bomb16)
                all_sprites.add(bomb17)
                bombs.add(bomb1)
                bombs.add(bomb2)
                bombs.add(bomb3)
                bombs.add(bomb4)
                bombs.add(bomb5)
                bombs.add(bomb6)
                bombs.add(bomb7)
                bombs.add(bomb8)
                bombs.add(bomb9)
                bombs.add(bomb10)
                bombs.add(bomb11)
                bombs.add(bomb12)
                bombs.add(bomb13)
                bombs.add(bomb14)
                bombs.add(bomb15)
                bombs.add(bomb16)
                bombs.add(bomb17)
                shooting_sound.play()
                self.bomb_count -= 1
            
    def shoot(self):
        ## to tell the bullet where to spawn
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                self.power_count_text = "∞"
                shooting_sound.play()
            if self.power == 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                self.power_count_text = str(self.power_count)
                shooting_sound.play()
                self.power_count -= 1 #파워 2이상일때 총알 카운트

            """ MOAR POWAH """
            if self.power >= 3:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                missile1 = Missile(self.rect.centerx, self.rect.top) # Missile shoots from center of ship
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(missile1)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(missile1)
                self.power_count_text = str(self.power_count)
                shooting_sound.play()
                missile_sound.play()
                self.power_count -= 1 #파워 2이상일때 총알 카운트

    def powerup(self):
        self.power += 1
#        self.power_time = pygame.time.get_ticks()
        self.power_count = 30

    def hide(self):
        """죽었을 때"""
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)
        self.power = 1              #죽었을 때 파워 초기화
        self.power_count = 30       #죽었을 때 파워 카운트(총알 갯수) 초기화
        self.bomb_count = 1         #죽었을 때 폭탄 갯수 초기화

    
# defines the enemies
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width *.90 / 2)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(5, 20)        ## for randomizing the speed of the Mob

        ## randomize the movements a little more 
        self.speedx = random.randrange(-3, 3)

        ## adding rotation to the mob element
        self.rotation = 0
        self.rotation_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()  ## time when the rotation has to happen
        
    def rotate(self):
        time_now = pygame.time.get_ticks()
        if time_now - self.last_update > 50: # in milliseconds
            self.last_update = time_now
            self.rotation = (self.rotation + self.rotation_speed) % 360 
            new_image = pygame.transform.rotate(self.image_orig, self.rotation)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    #wave2 몹 change
    def mobchange(self):
        self.image_orig = random.choice(ghost_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width *.90 / 2)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(5, 20)        
    #wave3 몹 cahnge
    def mobchange2(self):
        self.image_orig = random.choice(cockpit_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width *.90 / 2)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(5, 20)
    #wave4 몹 change
    def mobchange3(self):
        self.image_orig = random.choice(cockpit2_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width *.90 / 2)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(5, 20)        
    def update(self):
        if self.image_orig == random.choice(meteor_images):
            self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        ## now what if the mob element goes out of the screen

        if (self.rect.top > HEIGHT + 10) or (self.rect.left < -25) or (self.rect.right > WIDTH + 20):
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)        ## for randomizing the speed of the Mob

## defines the sprite for Powerups
class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun', 'bomb', 'heart']) #폭탄, 목숨 아이템 추가
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        ## place the bullet according to the current position of the player
        self.rect.center = center
        self.speedy = 2

    def update(self):
        """should spawn right in front of the player"""
        self.rect.y += self.speedy
        ## kill the sprite after it moves over the top border
        if self.rect.top > HEIGHT:
            self.kill()

#폭탄을 위한 Bomb 클래스 생성
class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bomb_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):

        self.rect.y += self.speedy

        if self.rect.bottom < 0:
            self.kill()
            

## defines the sprite for bullets
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        ## place the bullet according to the current position of the player
        self.rect.bottom = y 
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        """should spawn right in front of the player"""
        self.rect.y += self.speedy
        ## kill the sprite after it moves over the top border
        if self.rect.bottom < 0:
            self.kill()

        ## now we need a way to shoot
        ## lets bind it to "spacebar".
        ## adding an event for it in Game loop

## FIRE ZE MISSILES
class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = missile_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        """should spawn right in front of the player"""
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


###################################################
## Load all game images
#배경화면 이미지 리스트로 저장
starfield=['starfield1.png', 'starfield2.png', 'starfield3.png', 'starfield4.png']
#스테이지 당 배경화면 설정
def setbackground(wave):
    if wave == 1:
        background = pygame.image.load(path.join(img_dir, starfield[0])).convert()
    elif wave == 2:
        background = pygame.image.load(path.join(img_dir, starfield[1])).convert()
    elif wave == 3:
        background = pygame.image.load(path.join(img_dir, starfield[2])).convert()
    elif wave == 4:
        background = pygame.image.load(path.join(img_dir, starfield[3])).convert()
    return background

player_img = pygame.image.load(path.join(img_dir, 'playerShip1_orange.png')).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
bullet_img = pygame.image.load(path.join(img_dir, 'laserRed16.png')).convert()
bomb_img = pygame.image.load(path.join(img_dir, 'spaceMissiles_006.png')).convert()
missile_img = pygame.image.load(path.join(img_dir, 'missile.png')).convert_alpha()
# meteor_img = pygame.image.load(path.join(img_dir, 'meteorBrown_med1.png')).convert()
meteor_images = []
meteor_list = [
    'meteorBrown_big1.png',
    'meteorBrown_big2.png', 
    'meteorBrown_med1.png', 
    'meteorBrown_med3.png',
    'meteorBrown_small1.png',
    'meteorBrown_small2.png',
    'meteorBrown_tiny1.png'
]

for image in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, image)).convert())

#외계인 이미지 추가 wave2 몹
ghost_images = []
ghost_list = [
    'ghost1.png',
    'ghost1b.png',
    'ghost2.png',
    'ghost2b.png',
    'ghost3.png',
    'ghost3b.png',
    'ghost4.png',
    'ghost4b.png'
]
for image in ghost_list:
    ghost_images.append(pygame.image.load(path.join(img_dir, image)).convert())

#우주선 이미지 추가 wave3 몹
cockpit_images = []
cockpit_list = [
    'cockpit1Green.png',
    'cockpit2Green.png',
    'cockpit3Green.png',
    'cockpit1Grey.png',
    'cockpit2Grey.png',
    'cockpit3Grey.png',
    'cockpit1Red.png',
    'cockpit2Red.png',
    'cockpit3Red.png',
    'cockpit1Yellow.png',
    'cockpit2Yellow.png',
    'cockpit3Yellow.png'   
]
for image in cockpit_list:
    cockpit_images.append(pygame.image.load(path.join(img_dir, image)).convert())

#우주선2 이미지 추가 wave4 몹
cockpit2_images = []
cockpit2_list = [
    'cockpit4Green.png',
    'cockpit5Green.png',
    'sampleShip1.png',
    'cockpit4Grey.png',
    'cockpit5Grey.png',
    'sampleShip2.png',
    'cockpit4Red.png',
    'cockpit5Red.png',
    'sampleShip3.png',
    'cockpit4Yellow.png',
    'cockpit5Yellow.png'
]
for image in cockpit2_list:
    cockpit2_images.append(pygame.image.load(path.join(img_dir, image)).convert())


## meteor explosion
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    ## resize the explosion
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)

    ## player explosion
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)

## load power ups
powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'shield_gold.png')).convert()
powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'bolt_gold.png')).convert()
powerup_images['bomb'] = pygame.image.load(path.join(img_dir, 'bomb_gold.png')).convert()
#bomb 이미지 설정
powerup_images['heart'] = pygame.image.load(path.join(img_dir, 'heart.png')).convert()
#heart(목숨) 아이템 이미지 설정

###################################################


###################################################
### Load all game sounds
shooting_sound = pygame.mixer.Sound(path.join(sound_folder, 'pew.wav'))
missile_sound = pygame.mixer.Sound(path.join(sound_folder, 'rocket.ogg'))
expl_sounds = []
for sound in ['expl3.wav', 'expl6.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(sound_folder, sound)))
## main background music
#pygame.mixer.music.load(path.join(sound_folder, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(0.2)      ## simmered the sound down a little

player_die_sound = pygame.mixer.Sound(path.join(sound_folder, 'rumble1.ogg'))
###################################################

## TODO: make the game music loop over again and again. play(loops=-1) is not working
# Error : 
# TypeError: play() takes no keyword arguments
#pygame.mixer.music.play()

#############################
## Game loop
running = True
menu_display = True
while running:
    if menu_display:
        main_menu()
        pygame.time.wait(3000)

        #Stop menu music
        pygame.mixer.music.stop()
        #Play the gameplay music
        pygame.mixer.music.load(path.join(sound_folder, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
        pygame.mixer.music.play(-1)     ## makes the gameplay sound in an endless loop
        
        menu_display = False

        bossStage = False
        wavecounter = 0 #처음에 몹 죽인 횟수 0으로 count
        wave = 1 #stage(wave) = 1
        background = setbackground(wave)
        background_rect = setbackground(wave).get_rect() 
        
        ## group all the sprites together for ease of update
        all_sprites = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)

        ## spawn a group of mob
        mobs = pygame.sprite.Group()
        for i in range(8):      ## 8 mobs
            # mob_element = Mob()
            # all_sprites.add(mob_element)
            # mobs.add(mob_element)
            newmob(wave)

        ## group for bullets
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        bombs = pygame.sprite.Group() #bombs 라는 그룹 생성

        #### Score board variable
        score = 0
        
    #1 Process input/events
    clock.tick(FPS)     ## will make the loop run at the same speed all the time
    for event in pygame.event.get():        # gets all the events which have occured till now and keeps tab of them.
        ## listening for the the X button at the top
        if event.type == pygame.QUIT:
            running = False

        ## Press ESC to exit game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        # ## event for shooting the bullets
        # elif event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_SPACE:
        #         player.shoot()      ## we have to define the shoot()  function

    #2 Update
    all_sprites.update()


    ## check if a bullet hit a mob
    ## now we have a group of bullets and a group of mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    ## now as we delete the mob element when we hit one with a bullet, we need to respawn them again
    ## as there will be no mob_elements left out 
    for hit in hits:
        wavecounter += 1
        wave = count_wave(wavecounter)
        if wavecounter %200 <=10:
            background = setbackground(wave)
            background_rect = setbackground(wave).get_rect() 
        score += 100 - hit.radius         ## give different scores for hitting big and small metoers
        random.choice(expl_sounds).play()
        # m = Mob()
        # all_sprites.add(m)
        # mobs.add(m)
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.95:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newmob(wave)        ## spawn a new mob

    ## ^^ the above loop will create the amount of mob objects which were killed spawn again
    #########################

#폭탄과 몬스터가 충돌 시 코드
    b_hits = pygame.sprite.groupcollide(mobs, bombs, True, True)
    for hit in b_hits:
        wavecounter += 1
        wave = count_wave(wavecounter)
        if wavecounter %200 <=10:
            background = setbackground(wave)
            background_rect = setbackground(wave).get_rect() 
        score += 100 - hit.radius         ## give different scores for hitting big and small metoers
        random.choice(expl_sounds).play()
        # m = Mob()
        # all_sprites.add(m)
        # mobs.add(m)
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.95:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newmob(wave)    

    ## check if the player collides with the mob
    # gives back a list, True makes the mob element disappear
    # 몬스터와 플레이어가 부딛혔을 시 코드
    hits = pygame.sprite.spritecollide(
        player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob(wave)
        if player.shield <= 0: 
            player_die_sound.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            # running = False     ## GAME OVER 3:D
            player.hide()
            player.lives -= 1
            player.shield = 100

    ## if the player hit a power up
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 30)
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            player.powerup()
        if hit.type == 'bomb':
            player.bomb_count += 1 #폭탄 먹었을 때 폭탄 갯수 +1
            if player.bomb_count >= 3:
                player.bomb_count = 3
        if hit.type == 'heart': #하트 추가, 갯수 제한
            player.lives += 1
            if player.lives >= 3:
                player.lives = 3
                
    ## if player died and the explosion has finished, end game
    if player.lives == 0 and not death_explosion.alive():
        scoreBorder(score)
        running = False
        # menu_display = True
        # pygame.display.update()

    #3 Draw/render
    screen.fill(BLACK)
    ## draw the stargaze.png image
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    # 15px down from the screen
    draw_text(screen, 'score: ' + str(score), 20, WIDTH / 10, 15)
    draw_text(screen, 'bullet: ' + str(player.power_count_text), 20, WIDTH / 10, 35)
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_text(screen, 'kill ' + str(wavecounter),18, WIDTH / 2,25)
    draw_text(screen, 'wave ' + str(wave), 18, WIDTH / 2, 40)
    # Draw lives
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)

    # Draw bombs 폭탄 갯수 화면에 표시
    draw_lives(screen, WIDTH - 100, 25, player.bomb_count, powerup_images['bomb'])
    
    ## Done after drawing everything to the screen
    pygame.display.flip()       

pygame.quit()
