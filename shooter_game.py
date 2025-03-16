from pygame import *
from random import randint
from time import time as timer


#background music
mixer.init()
mixer.music.load('space.ogg')
mixer.music.set_volume(0.1)
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
fire_sound.set_volume(0.1)


#fonts and captions
font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
font2 = font.Font(None, 36)


#we need the following images:
img_back = "galaxy.jpg" #game background
img_hero = "rocket.png" #hero
img_bullet = "bullet.png" #bullet
img_enemy = "ufo.png" #enemy
img_aste = "asteroid.png"


score = 0 #ships destroyed
lost = 0 #ships missed
max_lost = 10 #lose if you miss that many
goal = 45
life = 3


#parent class for other sprites
class GameSprite(sprite.Sprite):
 #class constructor
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        #Call for the class (Sprite) constructor:
        sprite.Sprite.__init__(self)


        #every sprite must store the image property
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed


        #every sprite must have the rect property that represents the rectangle it is fitted in
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 #method drawing the character on the window
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


#main player class
class Player(GameSprite):
   #method to control the sprite with arrow keys
    def update(self):
        #Keyboard Ver
        '''keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed'''
        #Mouse Ver
        mouse_x, _ = mouse.get_pos()
        self.rect.x = mouse_x - self.rect.width//2
 #method to "shoot" (use the player position to create a bullet there)
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -30)
        bullets.add(bullet)


#enemy sprite class  
class Enemy(GameSprite):
   #enemy movement
    def update(self):
        self.rect.y += self.speed
        global lost
        #disappears upon reaching the screen edge
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1


#bullet sprite class  
class Bullet(GameSprite):
   #enemy movement
    def update(self):
        self.rect.y += self.speed
        #disappears upon reaching the screen edge
        if self.rect.y < 0:
            self.kill()


#Create a window
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))


#create sprites
ship = Player(img_hero, 5, win_height - 100, 80, 100, 20)


monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(3, 7))
    monsters.add(monster)
asteroids = sprite.Group()
for i in range(1,3):
    asteroid = Enemy(img_aste, randint(30,win_width - 30), -40, 80, 50, randint(3, 7))
    asteroids.add(asteroid)


bullets = sprite.Group()


#the "game is over" variable: as soon as True is there, sprites stop working in the main loop
finish = False
#Main game loop:
run = True #the flag is reset by the window close button
num_fire = 0
rel_time = False
while run:
   #"Close" button press event
    for e in event.get():
        if e.type == QUIT:
            run = False
        #event of pressing the spacebar - the sprite shoots
        #LMB ver
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire +1
                    fire_sound.play()
                    ship.fire()

            if num_fire >= 5 and rel_time == False:
                last_time = timer()
                rel_time = True
        #Space ver
        '''elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()'''


    if not finish:
        #update the background
        window.blit(background,(0,0))


        #write text on the screen
        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))


        text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))


        #launch sprite movements
        ship.update()
        monsters.update()
        bullets.update()
        asteroid.update()

        #update them in a new location in each loop iteration
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        
        if rel_time == True:
            now_time = timer()
            if now_time - last_time <1:
                reload = font2.render("Reloading",1,(200,0,0))
                window.blit(reload, (260,460))
            else:
                num_fire = 0
                rel_time = False


        collide = sprite.groupcollide(monsters,bullets, True, True)
        for c in collide:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(3,7))
            monsters.add(monster)

            if sprite.spritecollide(ship,monsters, False) or sprite.spritecollide(ship, asteroids, False):
                sprite.spritecollide(ship,monsters,True) 
                sprite.spritecollide(ship,asteroids,True)
                life = life - 1
        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200,200))

        if score > goal:
            finish = True
            window.blit(win,(200,200))
        if life == 3:
            life_color = (0,200,0)
        if life == 2:
            life_color = (150,150,0)
        if life == 1:
            life_color = (200,0,0)
        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650,10))


        display.update()
    #the loop is executed each 0.05 sec
    else:
        finish = False
        score = 0
        lost = 0
        num_fire = 0
        life = 3
        
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill() 
        for a in asteroids:
            a.kill()
        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(3, 7))
            monsters.add(monster)

        for i in range(1,3):
            asteroid = Enemy(img_aste, randint(30, win_width - 30), -40,80,50,randint(3,7))
            asteroids.add(asteroid)
    time.delay(50)