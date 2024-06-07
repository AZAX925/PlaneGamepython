import pygame
import random
import time

from pygame.locals import (
    K_w,
    RLEACCEL,
    K_s,
    K_a,
    K_d,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()

time1c = time.time()
time2c = time.time()
clock = pygame.time.Clock()

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)
ADDFINISHLINE = pygame.USEREVENT + 1
pygame.time.set_timer(ADDCLOUD, 1000)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("Spaceship.png").convert()
        self.surf.set_colorkey((255, 255, 255))
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_w]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_s]:
            self.rect.move_ip(0, 15)
        if pressed_keys[K_a]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_d]:
            self.rect.move_ip(5, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("Bomb.png").convert()
        self.surf.set_colorkey((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )
        self.speed = random.randint(5, 10)
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class Clouds(pygame.sprite.Sprite):
    def __init__(self):
        super(Clouds, self).__init__()
        self.surf = pygame.image.load("clouds.png").convert()
        self.surf.set_colorkey((0, 0, 0))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )
        self.speed = random.randint(5, 20)
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


class finishline(pygame.sprite.Sprite):
    def __init__(self):
        super(finishline, self).__init__()
        self.surf = pygame.image.load("finishline.png").convert()
        self.surf.set_colorkey((0, 0, 0))
        self.rect = self.surf.get_rect(center=(4000, 400))
        self.speed = random.randint(1, 5)
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

Alexandros = Player()
f = finishline()
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
groupfinish = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(Alexandros)
all_sprites.add(f)
groupfinish.add(f)

h3 = pygame.image.load("lives3.png").convert_alpha()
h_rect = h3.get_rect()
l = 3

bg = pygame.image.load("stars.jpg")

running = True
flag1 = 1

while running:

    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_ESCAPE]:
        running = False

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False

        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        elif event.type == ADDCLOUD:
            new_clouds = Clouds()
            clouds.add(new_clouds)
            all_sprites.add(new_clouds)

    if flag1 == 1:
        screen.blit(bg, (0, 0))

        Alexandros.update(pressed_keys)
        enemies.update()
        clouds.update()
        groupfinish.update()

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        if pygame.sprite.spritecollideany(Alexandros, enemies):
            en = pygame.sprite.spritecollideany(Alexandros, enemies)
            en.kill()
            l = l - 1

        if pygame.sprite.spritecollideany(Alexandros, groupfinish):
            en = pygame.sprite.spritecollideany(Alexandros, groupfinish)
            en.kill()
            flag1 = 0



        if l == 3:
            h3 = pygame.image.load("lives3.png").convert_alpha()
            h3.set_colorkey((255, 255, 255), RLEACCEL)
            screen.blit(h3, (SCREEN_WIDTH-h_rect.width, -10))
        elif l == 2:
            h3 = pygame.image.load("lives2.png").convert_alpha()
            h3.set_colorkey((255, 255, 255), RLEACCEL)
            screen.blit(h3, (SCREEN_WIDTH-h_rect.width, -10))
        elif l == 1:
            h3 = pygame.image.load("lives1.png").convert_alpha()
            h3.set_colorkey((255, 255, 255), RLEACCEL)
            screen.blit(h3, (SCREEN_WIDTH-h_rect.width, -10))

        elif l == 0:
            flag1 = 0

    else:
        if pressed_keys[pygame.K_RETURN]:
            for s in all_sprites:
                s.kill()
            for e in enemies:
                e.kill()
            all_sprites.add(Alexandros)
            l = 3
            flag1 = 1
        else:
            screen.fill((0,0,0))
            go_font = pygame.font.SysFont("cosmicsansms", 80, True, True)
            go = go_font.render("GAME OVER", True, (255, 255, 255))
            text = pygame.font.SysFont("cosmicsansms", 50, True, True)
            txt = text.render("Press enter to play again", True, (255, 255, 255))
            screen.blit(go, (50, 100))
            screen.blit(txt, (50, 200))




    pygame.display.flip()

    clock.tick(40)

