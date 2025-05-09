#frimpot
from random import randint

import mixer
from pygame import *
#object
mixer.init()

mixer.music.load("blue.mp3")
mixer.music.play()

img_back = "phone.png"
img_back2 = "phone2.png"
img_back3 = "phone3.png"
img_player = "player.png"
img_enemy = "zombie.png"
img_bullet = "bullet.png"
img_bullet2 = "bullet2.png"
fire_snd = mixer.Sound("fire.ogg")
fire_snd2 = mixer.Sound("fire.ogg")
img_meteor = "meteor.png"
img_player2 = "player2.png"
img_zoklama = "zombiklama.png"
#winlose
font.init()
font2 = font.SysFont(None, 36)
font1 = font.SysFont(None, 80)
win = font1.render('Ти виграв!', True, (0,255,0))
lose = font1.render('Ти програв :(', True, (200,0,0))
#score
lost = 0
score = 0
goal = 15
max_lost = 3
#window
win_width = 900
win_height = 600
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
background2 = transform.scale(image.load(img_back2), (win_width, win_height))
display.set_caption("Shooter")

#programmer
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 70:
            self.rect.x += self.speed



    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Player2(GameSprite):
    def update(self):
        keys = key.get_pressed()


        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 70:
            self.rect.x += self.speed



    def fire(self):
        bullet2 = Bullet(img_bullet2, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets2.add(bullet2)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_width:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


#dange!
def level():
    level = font2.render("Рівень 2 ", 1, (255, 255, 0))
    window.blit(level, (10, 20))
    player = Player(img_player, 5, win_height - 100, 80, 100, 10)
    player2 = Player2(img_player2, 5, win_height - 100, 150, 120, 10)
    monsters = sprite.Group()
    bullets = sprite.Group()
    bullets2 = sprite.Group()


for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), 0, 60, 70, randint(2, 6))
    monsters.add(monster)



finish = False
run = True

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_snd.play()
                player.fire()
            if e.key == K_v:
                fire_snd2.play()
                player2.fire()



    if not finish:
        window.blit(background, (0, 0))

        text_score = font2.render("Скількі збив: " + str(score), 1, (0, 0, 255))
        window.blit(text_score, (10, 20))


        text_lose = font2.render("Пропустив: " + str(lost), 1, (255, 255, 0))
        window.blit(text_lose, (10, 50))

        player.update()
        player2.update()
        monsters.update()
        bullets.update()
        bullets2.update()

        player.reset()
        player2.reset()
        monsters.draw(window)
        bullets.draw(window)
        bullets2.draw(window)



        collides = sprite.groupcollide(monsters, bullets, True, True)
        collides2 = sprite.groupcollide(monsters, bullets2, True, True)
        for c in collides:
            score += 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), 0, 60, 70, randint(1, 6))
            monsters.add(monster)
        for c in collides2:
            score += 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), 0, 60, 70, randint(1, 6))
            monsters.add(monster)

        if sprite.spritecollide(player, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))
        if sprite.spritecollide(player2, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))


        if score >= goal:
            finish = False
            window.blit(level, (200, 200))



        display.update()

    time.delay(50)


