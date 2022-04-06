from random import randrange
import pygame

WIDTH = 350
HEIGHT = 600
FPS = 60

BLACK = (13, 13, 13)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

pygame.init()
font = pygame.font.SysFont(None, 30)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Mario Jumper')
clock = pygame.time.Clock()
background = pygame.transform.scale(pygame.image.load('images/bg.png').convert_alpha(), (WIDTH, HEIGHT))
game_over = 0
victory = None
main_menu = True

music = pygame.mixer.Sound('sounds/music.wav')
music.set_volume(0.2)
music.play(loops=-1)

coin_fx = pygame.mixer.Sound('sounds/coin.wav')
coin_fx.set_volume(0.4)

damage_fx = pygame.mixer.Sound('sounds/damage.wav')
damage_fx.set_volume(0.2)

life_fx = pygame.mixer.Sound('sounds/life.wav')
life_fx.set_volume(0.25)

def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

class Mario(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.image.load('images/mario.png').convert_alpha()
        self.image = pygame.transform.scale(self.img, (int(self.img.get_width() * scale), int(self.img.get_height() * scale)))
        self.new_image = pygame.transform.scale(self.img, (int(self.img.get_width() * scale), int(self.img.get_height() * scale)))
        self.flipped = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.rect.x = x 
        self.rect.y = y
        self.is_jump = False
        self.jump_count = 10
        self.health = 5
        self.damage_cooldown = 0
        self.last_damage = pygame.time.get_ticks()
        self.score = 0
        self.moving_right = False
        self.moving_left = False

    def update(self):
        dx = 0 
        dy = 0

        key = pygame.key.get_pressed()

        if not self.is_jump:
            if key[pygame.K_SPACE]:
                self.is_jump = True
        else:
            if self.jump_count >= -10:
                self.rect.y -= (self.jump_count * abs(self.jump_count)) * 0.48
                self.jump_count -= 1
            else:
                self.jump_count = 10
                self.is_jump = False
                if self.rect.y < 450:
                    self.rect.y = 450

        if key[pygame.K_LEFT] and self.rect.left > 0:
            dx -= 6
            self.moving_left = True
            self.moving_right = False
            self.image = self.flipped

        if key[pygame.K_RIGHT] and self.rect.right < WIDTH:
            dx += 6
            self.moving_right = True
            self.moving_left = False
            self.image = self.new_image

        self.rect.x += dx 
        self.rect.y += dy

    def take_damage(self):
        now = pygame.time.get_ticks()
        if now - self.last_damage > self.damage_cooldown:
            self.last_damage = now
            damage_fx.play()
            self.health -= 1
            self.damage_cooldown = 500

    def is_mario_dead(self):
        return self.health <= 0

    def gain_life(self):
        self.health += 1
        if self.health >= 5:
            self.health = 5
    
    def gain_score(self):
        self.score += 1

    def reset(self, x, y):
        self.health = 5
        self.score = 0
        self.rect.x = x
        self.rect.y = y
        self.jump_count = 10
        self.image = self.new_image

class Thwomp(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/thwomp.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * scale), int(self.image.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.rect.x = x 
        self.rect.y = y
        self.move_direction = 1 
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 120:
            self.move_direction *= -1
            self.move_counter *= -1

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/coin.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * scale), int(self.image.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.rect.x = x 
        self.rect.y = y

    def update(self):
        new_x = randrange(20,WIDTH - 100)
        new_y = randrange(20,HEIGHT - 150)
        self.rect.x = new_x 
        self.rect.y = new_y

class Mushroom(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/mushroom.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * scale), int(self.image.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.rect.x = x 
        self.rect.y = y

    def update(self):
        new_x = randrange(20,WIDTH - 100)
        new_y = 380
        self.rect.x = new_x 
        self.rect.y = new_y

class Goomba(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/goomba.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * scale), int(self.image.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.rect.x = x 
        self.rect.y = y
        self.y_speed = 2

    def update(self):
        self.rect.x += 4
        self.rect.y += self.y_speed
        if self.rect.bottom > HEIGHT - 100:
            self.y_speed = -5
        if self.rect.top < 100:
            self.y_speed = 5
        if self.rect.left > WIDTH:
            self.rect.right = 0

class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x 
        self.y = y 
        self.health = health 
        self.max_health = max_health

    def draw(self, health):
        self.health = health 
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y 
        self.clicked = False

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, self.rect)
        return action

mario_group = pygame.sprite.GroupSingle()
mario = Mario(5, 450, 0.4)
mario_group.add(mario)

thwomp_group = pygame.sprite.GroupSingle()
thwomp = Thwomp(150, 450, 0.22)
thwomp_group.add(thwomp)

goomba_group = pygame.sprite.GroupSingle()
goomba = Goomba(150, 220, 0.20)
goomba_group.add(goomba)

coin_group = pygame.sprite.Group()
coin_timer = pygame.USEREVENT + 1
pygame.time.set_timer(coin_timer, 2500) 

mushroom_group = pygame.sprite.Group()
mushroom_timer = pygame.USEREVENT + 2
pygame.time.set_timer(mushroom_timer, 10_000) 

health_bar = HealthBar(10, 10, mario.health, mario.health)
restart_img = pygame.image.load('images/restart_btn.png').convert_alpha()
restart_button = Button(WIDTH // 2 - 60, HEIGHT // 2 - 50, restart_img)

start_img = pygame.image.load('images/start_btn.png').convert_alpha()
start_button = Button(WIDTH // 2 - 60, HEIGHT // 2 - 50, start_img)

exit_img = pygame.image.load('images/exit_btn.png').convert_alpha()
exit_button = Button(WIDTH // 2 - 60, HEIGHT // 2, exit_img)

running = True
while running:
    clock.tick(FPS)
    screen.blit(background,(0,0))

    if main_menu:
        if exit_button.draw():
            running = False
        if start_button.draw():
            main_menu = False

    elif not game_over:
        if pygame.sprite.spritecollide(mario, thwomp_group, False) or pygame.sprite.spritecollide(mario, goomba_group, False):
            mario.take_damage()

        if pygame.sprite.spritecollide(mario, coin_group, True):
            mario.gain_score()
            coin_fx.play()

        if pygame.sprite.spritecollide(mario, mushroom_group, True):
            mario.gain_life()
            life_fx.play()

        if mario.is_mario_dead():
            game_over = 1
            victory = False

        if mario.score == 20:
            game_over = 1
            victory = True

        mario_group.draw(screen)
        thwomp_group.draw(screen)
        health_bar.draw(mario.health)
        goomba_group.draw(screen)
        coin_group.draw(screen)
        mushroom_group.draw(screen)

        draw_text(f'Pontos: {mario.score}', font, BLACK, 240, 10)

        mario_group.update()
        thwomp_group.update()
        goomba_group.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == coin_timer:
            coin = Coin(randrange(20,WIDTH - 100), randrange(20,HEIGHT - 150), 0.13)
            coin_group.add(coin)
            coin_group.update()
        if event.type == mushroom_timer:
            mushroom = Mushroom(randrange(20,WIDTH - 100), 380, 0.13)
            mushroom_group.add(mushroom)
            mushroom_group.update()

    if game_over:
        if victory:
            draw_text('Você VENCEU!', font, BLACK, (WIDTH // 2) - 70, HEIGHT // 2)
        else:
            draw_text('Você PERDEU!', font, BLACK, (WIDTH // 2) - 70, HEIGHT // 2)
        if restart_button.draw():
            game_over = 0
            mario.reset(5, 450)
            mushroom_group.empty()
            coin_group.empty()

    pygame.display.update()

pygame.quit()