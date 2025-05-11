#створи гру "Лабіринт"!
from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_w, player_h, player_speed):
        super().__init__()
        self.width = player_w
        self.height = player_h
        self.image = transform.scale(image.load(player_image), (self.width, self.height))    
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y 
        
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        key_press = key.get_pressed()
        if key_press[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if key_press[K_RIGHT] and self.rect.x < 595:
            self.rect.x += self.speed
        if key_press[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if key_press[K_DOWN] and self.rect.y < 395:
            self.rect.y += self.speed

class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_w, player_h, player_speed, direction):
        super().__init__(player_image, player_x, player_y, player_w, player_h, player_speed)
        self.direction = direction
    def update(self):
        if self.rect.x <= 520:
            self.direction = "right"
        if self.rect.x >= 610:
            self.direction = "left"
        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Enemy2(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_w, player_h,player_speed, direction):
        super().__init__(player_image, player_x, player_y, player_w, player_h, player_speed)
        self.direction = direction

    def update(self):
        if self.rect.y <= 340:
            self.direction = "down"
        if self.rect.y >= 420:
            self.direction = "up"
        if self.direction == "up":
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed           

class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y,wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1 #color_2 та color_3 аналогічно   
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


window = display.set_mode((700, 500))
display.set_caption("Hakaton")
background = transform.scale(image.load("fon.png"), (700, 500))
mixer.init()
mixer.music.load("fon.mp3")
mixer.music.play()
kick = mixer.Sound('scream55.mp3')
money = mixer.Sound('kidcheer.mp3')

# написи
font.init()
font1 = font.Font(None, 70)
font2 = font.Font(None,30)

win = font1.render('OH! GOOD JOB!', True, (255, 215, 0))
lose = font1.render('LOSER.', True, (180, 0, 0))

level = 1

game = True
finish = False
clock = time.Clock()
FPS = 60
hero = Player("foxy.png",50,50,35,35,5)
cyborg = Enemy("foxy2.png", 500,180,35,35,1,"left")
cyborg2 = None
prize = GameSprite("piizza.png", 550,330,35,35,0)
door = GameSprite('door.png',10,10,65,75,0)

wall_p0 = Wall(0, 0, 0, 20, 140, 20, 310)
wall_p1 = Wall(0, 0, 0, 140, 40, 20, 200)
wall_p2 = Wall(0, 0, 0, 140, 40, 510, 20)
wall_p3 = Wall(0, 0, 0, 650, 40, 20, 430)
wall1 = Wall(0, 0, 0, 140, 350, 20, 100)
wall2 = Wall(0, 0, 0, 20, 450, 650, 20)
wall3 = Wall(0, 0, 0, 260, 40, 20, 100)
wall4 = Wall(0, 0, 0, 260, 250, 20, 200)
wall5 = Wall(0, 0, 0, 380, 40, 20, 330)
wall6 = Wall(0, 0, 0, 500, 140, 20, 330)


walls = [wall_p0, wall_p1, wall_p2, wall_p3, wall1, wall2, wall3, wall4, wall5, wall6]
iskey = False

while game:
    for e in event.get():
        if e.type == QUIT:
           game = False

    if finish != True:
        window.blit(background,(0, 0))
        door.reset()
        prize.reset()
        hero.update()
        hero.reset()
        level_text = font2.render(f"Level:{level}",True, (252,0,0))
        window.blit(level_text,(300,10))
        cyborg.update()
        cyborg.reset()
        

        for wall in walls:
            wall.draw_wall()
        
        if sprite.collide_rect(hero,prize):
            money.play()
            prize.rect.x = 800
            iskey = True
            
        if sprite.collide_rect(hero,door) and iskey==True:
            if level >= 3:
                window.blit(win, (200, 200))
                finish = True
            else:
                level += 1
                print(level)
                hero.rect.x = 50
                hero.rect.y = 50
                iskey = False
                prize.rect.x = 550
                prize.rect.y = 330
                finish = False
                time.delay(1000)  
        
        if level == 2 and cyborg2 is None:
            cyborg2 = Enemy2("bonnyy.png",340,420,35,35,1,"up")

        if cyborg2:
            cyborg2.update()
            cyborg2.reset()

        if level == 3:
            hero.image = transform.scale(image.load("foxy.png"), (45, 45)) 
            hero.rect = hero.image.get_rect(x=hero.rect.x, y=hero.rect.y) 
        
        for wall in walls:
            if sprite.collide_rect(hero, wall):
                kick.play()
                window.blit(lose,(200, 200))
                finish = True
        
        if sprite.collide_rect(hero,cyborg) or (cyborg2 and sprite.collide_rect(hero,cyborg2)):
            kick.play()
            window.blit(lose,(200, 200))
            finish = True

        display.update()
        
    else:
        finish = False
        iskey = False
        level = 1
        hero = Player("foxy.png",50,50,35,35,5)
        prize = GameSprite("piizza.png", 550,330,35,35,0)
        cyborg2 = None
        time.delay(3000)

    clock.tick(FPS)