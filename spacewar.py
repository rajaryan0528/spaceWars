import pygame
import random
from pygame import mixer

pygame.init()

# background

screen = pygame.display.set_mode((800, 600))
bg_img = pygame.image.load("background.jpg")
background = pygame.transform.scale(bg_img, (800, 600))
start_pic = pygame.image.load("starting_image copy.jpg")

# background music
mixer.music.load("background.wav")
mixer.music.play(-1)

# font object
font = pygame.font.Font("freesansbold.ttf", 32)

# some colours
bright_green = (0, 255, 0)
green = (0, 175, 0)
bright_red = (255, 0, 0)
red = (175, 0, 0)
black = (0, 0, 0)

running = True

# title and icon
pygame.display.set_caption("Space Wars")
icon = pygame.image.load("project_icon.png")
pygame.display.set_icon(icon)

# Images:
player_img = pygame.image.load('rocket_1.png')
enemy1_img = pygame.image.load('alien_1.png')
enemy2_img = pygame.image.load('ufo.png')
player_bullet_img = pygame.image.load('user_bullet.png')
enemy1_bullet_img = pygame.transform.scale(pygame.image.load("alien_bullet_2.png"), (32, 32))
enemy2_bullet_img = pygame.transform.scale(pygame.image.load("alien_bullet_1.png"), (32, 32))
instructions_img = pygame.transform.scale(pygame.image.load("how_to_play.png"), (800, 600))
mini_ship = pygame.transform.scale(pygame.image.load("rocket_1.png"), (32, 32))

#-----------------------------------------------------------Classes-----------------------------------------------------------------------------


# Game control parameters
class Game():

    def __init__(self):
        self.num_of_enemies = 2
        self.level = 1
        self.score = 0
        self.high_score = ''
        self.color_list = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.user_shooting_lim =200
        self.user_health_del=4

    def level_update(self, alien_type_1_list, alien_type_2_list):
        if len(alien_type_1_list) == 0 and len(alien_type_2_list) == 0:
            self.score += 25
            self.level += 1
            self.num_of_enemies += 2
            self.user_shooting_lim-=2
            self.user_health_del+=4

    def read_highscore(self):
        with open("highscore.txt", "r") as f:
            self.high_score = f.read()

    def update_highscore(self):
        with open("highscore.txt", "w") as f:
            f.write(str(self.high_score))

    def show_score(self):
        score = font.render("Score :" + str(self.score), True, (255, 255, 255))
        screen.blit(score, (10, 10))

        hiscore = font.render("High Score :" + str(self.high_score), True, (18, 208, 18))
        screen.blit(hiscore, (540, 500))

        level = font.render("Level:" + str(self.level), True, (255, 1, 1))
        screen.blit(level, (40, 500))

    def game_over(self):
        if self.score > int(self.high_score):
            self.high_score = self.score
            self.update_highscore()
        alien.eliminate()
        ship.eliminate()
        ufo.eliminate()
        screen.fill((0, 0, 0))
        text_objects("GAME OVER", 200, 250, red)


game = Game()


# Player
class user:
    x_change: int

    def __init__(self):
        self.Img = player_img
        self.x = 370
        self.y = 480
        self.x_change = 0
        self.bullets = []
        self.cooldown_count = 0
        self.health = 240

    def movement(self, userInput):
        self.x_change = 0
        if userInput[pygame.K_LEFT]:
            self.x_change = -1
        if userInput[pygame.K_RIGHT]:
            self.x_change = 1
        # checking for boundaries while steering spaceship
        if self.x <= 0:
            self.x = 0
        if self.x >= 736:
            self.x = 736
        self.x += self.x_change

    def draw_player(self):
        #pygame.draw.rect(screen, black, (self.x, self.y, 64, 64), 3)
        screen.blit(self.Img, (self.x, self.y))

    def eliminate(self):
        self.x = 1000

    # so that ship does not fire infinte many bullets
    def cooldown(self):
        # greater the shooting_lim less bullets will be appended to the list
        if self.cooldown_count >= game.user_shooting_lim:
            self.cooldown_count = 0
        elif self.cooldown_count > 0:
            self.cooldown_count += 1

    def is_collision(self, aliens_list):
        for alien in aliens_list:
            for alien_bullet in alien.bullets:
                if (self.x < alien_bullet.x < self.x + 64) and (self.y < alien_bullet.y < self.y + 64):
                    # print("ship is shot")
                    alien.bullets.remove(alien_bullet)
                    return True
                else:
                    return False

    def shoot(self, userInput):
        self.cooldown()
        if userInput[pygame.K_SPACE] and (self.cooldown_count == 0):
            bullet = UserBullet(self.x, self.y)
            self.bullets.append(bullet)
            # print("bullets ready")
            bullet_sound = mixer.Sound("laser.wav")
            bullet_sound.play()
            self.cooldown_count = 1
        for bullet in self.bullets:
            # print("firing bullet")
            bullet.movement()
            if bullet.off_screen():
                # print("removing bullet")
                self.bullets.remove(bullet)

    def health_status(self):
        pygame.draw.rect(screen, bright_red, (500, 10, 240, 20))
        pygame.draw.rect(screen, bright_green, (500, 10, self.health, 20))
        screen.blit(mini_ship, (485 + self.health, 10))


# enemy 1

class Alien1():
    def __init__(self):
        self.Img = enemy1_img
        self.x = random.randint(0, 735)
        self.y = random.randint(50, 150)
        self.x_change = 1
        self.y_change = 10
        self.bullets = []
        self.max_bullets = 1
        self.fire_chance = random.random()
        self.prob_to_fire=0.4

    def movement(self):
        if self.x <= 0:
            self.x_change = 1.
            self.y += self.y_change
        elif self.x >= 736:
            self.x_change = -1.
            self.y += self.y_change
        self.x += self.x_change

    def draw_enemy(self):
        #pygame.draw.rect(screen, black, (self.x, self.y, 64, 64), 1)
        screen.blit(self.Img, (self.x, self.y))

    # blits the alien off the screen after the game is over
    def eliminate(self):
        for self in alien_type_1_list:
            self.y = 2000

    def shoot(self):
        if (self.fire_chance <= self.prob_to_fire) and len(self.bullets) <= self.max_bullets:
            alien_bullet = Alien1_Bullet(self.x, self.y)
            self.bullets.append(alien_bullet)
        for alien_bullet in self.bullets:
            alien_bullet.movement()
            if alien_bullet.off_screen():
                self.bullets.remove(alien_bullet)

    def is_collision(self):
        for bullet in ship.bullets:
            if (self.x < bullet.x < self.x + 64) and (self.y + 2 < bullet.y < self.y + 64):
                # print("alien is shot")
                ship.bullets.remove(bullet)
                return True
            else:
                return False


# Alien_1 Bullet
class Alien1_Bullet():

    def __init__(self, x, y):
        self.Img = enemy1_bullet_img
        self.x = x + 5
        self.y = y + 50
        self.x_change = 0
        self.y_change = 1

    def draw_bullet(self,x,y):
        screen.blit(self.Img, (self.x, self.y))

    def off_screen(self):
        if self.y >= 550:
            return True

    def movement(self):
        # pygame.draw.rect(screen, black, (self.x, self.y, 45, 40), 1)
        self.draw_bullet(self.x, self.y)
        self.y += self.y_change


# Enemy 2
class Alien2():
    def __init__(self):
        self.Img = enemy2_img
        self.x = random.randint(0, 735)
        self.y = random.randint(50, 150)
        self.x_change = 1
        self.y_change = 10
        self.bullets = []
        self.max_bullets = 1
        self.fire_chance = random.random()
        self.prob_to_fire=0.4

    def movement(self):
        if self.x <= 0:
            self.x_change = 2
            self.y += self.y_change
        elif self.x >= 736:
            self.x_change = -2
            self.y += self.y_change
        self.x += self.x_change

    def draw_enemy(self):
        #pygame.draw.rect(screen, black, (self.x, self.y, 64, 64), 1)
        screen.blit(self.Img, (self.x, self.y))

    # blits the alien off the screen after the game is over
    def eliminate(self):
        for self in alien_type_2_list:
            self.y = 2000

    def shoot(self):
        if (self.fire_chance <=self.prob_to_fire) and len(self.bullets) <= self.max_bullets:
            ufo_bullet = Alien2_Bullet(self.x, self.y)
            self.bullets.append(ufo_bullet)
        for ufo_bullet in self.bullets:
            ufo_bullet.movement()
            if ufo_bullet.off_screen():
                self.bullets.remove(ufo_bullet)

    def is_collision(self):
        for bullet in ship.bullets:
            if (self.x < bullet.x < self.x + 64) and (self.y + 2 < bullet.y < self.y + 64):
                ship.bullets.remove(bullet)
                return True
            else:
                return False


# Alien_2 bullet
class Alien2_Bullet():
    def __init__(self, x, y):
        self.Img = enemy2_bullet_img
        self.x = x + 5
        self.y = y + 50
        self.x_change = 0
        self.y_change = 1

    def off_screen(self):
        if (self.y >= 550):
            return True

    def draw_bullet(self, x, y):
        screen.blit(self.Img, (self.x, self.y))

    def movement(self):
        self.draw_bullet(self.x, self.y)
        # print(self.x,self.y,"bullet")
        self.y += self.y_change


# User Bullet
class UserBullet():

    def __init__(self, x, y):
        self.Img = player_bullet_img
        self.x = x + 16
        self.y = y + 10
        self.x_change = 0
        self.y_change = 3

    def draw_bullet(self, x, y):
        screen.blit(self.Img, (self.x, self.y))

    def off_screen(self):
        if not (self.y >= 0):
            return True

    def movement(self):
        self.draw_bullet(self.x, self.y)
        self.y -= self.y_change


def text_objects(text, x, y, colour):
    if text != "GAME OVER":
        text = font.render(text, True, colour)
        screen.blit(text, (x, y))
    else:
        over_font = pygame.font.Font("freesansbold.ttf", 75)
        text = over_font.render(text, True, colour)
        screen.blit(text, (200, 250))


def button(msg, x, y, active_colour, inactive_colour, length, height, action=None):
    text_call = True
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    # if the mouse is hovering over the button:
    if x + length > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, active_colour, (x, y, length, height))
        if click[2] == True and action != None:
            if action == "inst":
                text_call = False
                screen.fill((0, 0, 0))
                screen.blit(instructions_img, (0, 0))
            if action == "quit":
                print("quit")
                pygame.quit()
                quit()
    else:
        pygame.draw.rect(screen, inactive_colour, (x, y, length, height))

    if text_call:
        text_objects(msg, x + 25, y + 20, black)


def game_menu():
    screen.fill((0, 0, 0,))
    screen.blit(start_pic, (0, 0))
    font1 = pygame.font.Font("freesansbold.ttf", 34)
    text1 = font1.render("Right click anywhere on the screen to play", True, game.color_list)
    pygame.draw.rect(screen,red,(80,450,700,30),3)
    screen.blit(text1, (80, 450))
    pygame.draw.rect(screen, green, (480, 300, 150, 75))
    pygame.draw.rect(screen, red, (150, 300, 285, 75))
    button('QUIT', 480, 300, bright_green, green, 150, 75, "quit")
    button("INSTRUCTIONS", 150, 300, bright_red, red, 285, 75, "inst")
    pygame.display.update()


ship = user()
alien_type_1_list = []
alien_type_2_list = []

#-------------------------------------------------------------------main loop-----------------------------------------------------------------------------

menu = True
while running:

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    menu = False
        game_menu()

    screen.fill((0, 0, 0,))
    screen.blit(background, (0, 0))

    # Event Handlers:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                menu = True

    # Player:
    userInput = pygame.key.get_pressed()
    ship.movement(userInput)
    ship.shoot(userInput)
    ship.health_status()
    ship.draw_player()

    # creating enemies  object
    if len(alien_type_1_list) == 0 and len(alien_type_2_list) == 0:
        for i in range(game.num_of_enemies):
            alien = Alien1()
            ufo = Alien2()
            alien_type_1_list.append(alien)
            alien_type_2_list.append(ufo)

    # Enemy 1:
    for alien in alien_type_1_list:
        alien.draw_enemy()
        alien.shoot()
        alien.movement()
        if alien.y > 440 or ship.health < 0:
            game.game_over()
        # Collision check of user_bullet with enemy_1:
        collision = alien.is_collision()
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            game.score += 1
            alien_type_1_list.remove(alien)

    # Enemy 2:
    for ufo in alien_type_2_list:
        ufo.draw_enemy()
        ufo.shoot()
        ufo.movement()
        if ufo.y > 440 or ship.health < 0:
            game.game_over()
        # Collision check of user_bullet with enemy_2:
        ufo_collision = ufo.is_collision()
        if ufo_collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            game.score += 2
            alien_type_2_list.remove(ufo)

    # Collision of enemy_1_bullet with ship
    collision_1 = ship.is_collision(alien_type_1_list)
    if collision_1:
        ship.health -=game.user_health_del+2
    # Collision of enemy_2_bullet with ship
    collision_2 = ship.is_collision(alien_type_2_list)
    if collision_2:
        ship.health -=game.user_health_del
    game.show_score()
    game.read_highscore()
    game.level_update(alien_type_1_list, alien_type_2_list)
    pygame.display.update()
