from random import randint
from random import choice
import pygame

WIDTH = 1200
HEIGHT = 800

walkRight = [pygame.image.load('right_1.png'), pygame.image.load('right_2.png'), pygame.image.load('right_3.png'),
             pygame.image.load('right_4.png'), pygame.image.load('right_5.png'), pygame.image.load('right_6.png')]

walkLeft = [pygame.image.load('left_1.png'), pygame.image.load('left_2.png'), pygame.image.load('left_3.png'),
            pygame.image.load('left_4.png'), pygame.image.load('left_5.png'), pygame.image.load('left_6.png')]

bg_initial = pygame.image.load('bg_initial.png')
bg = pygame.image.load('bg.png')

endgame = pygame.image.load('game_over.png')

playerStand = pygame.image.load('idle.png')

birdLeft = [pygame.image.load('bird_left_1.png'), pygame.image.load('bird_left_2.png')]

birdRight = [pygame.image.load('bird_right_1.png'), pygame.image.load('bird_right_2.png')]

moneybag = pygame.image.load('Money.png')

screen = pygame.display.set_mode((WIDTH, HEIGHT))

dollars = []
birds = []

money_counter = 0
level = 1

def ch_level(mouse_x, mouse_y):
    global num
    if mouse_y > 400 and mouse_y < 600:
        if mouse_x > 310 and mouse_x < 450:
            num = 1
        elif mouse_x > 540 and mouse_x < 670:
            num = 2
        elif mouse_x > 760 and mouse_x < 890:
            num = 3
        else:
            num = 1

    return(num)

number_of_birds = level
life_counter = 2 * number_of_birds

class Trump:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.a = 1
        self.animation_count = 0
        self.vector = 0
        self.is_jump = False

    def move(self):
        self.vx = 5 * self.vector
        if 0 < self.x + self.vx < WIDTH - 50:
            self.x += self.vx
        if self.is_jump:
            if self.y + self.vy < HEIGHT - 55:
                self.y += self.vy
                self.vy += self.a
            else:
                self.is_jump = False

    def draw(self):
        if self.animation_count + 1 >= 30:
            self.animation_count = 0

        if self.vector == -1:
            screen.blit(walkLeft[self.animation_count // 5], (self.x, self.y))
            self.animation_count += 1
        elif self.vector == 1:
            screen.blit(walkRight[self.animation_count // 5], (self.x, self.y))
            self.animation_count += 1
        else:
            screen.blit(playerStand, (self.x, self.y))

Player = Trump(screen, 50, 750) 

class Dollar:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.vy = 1

    def move(self):
        self.y += self.vy

    def draw(self):
        screen.blit(moneybag, (self.x, self.y))

    def hit(self, object):
        global money_counter, life_counter
        if self.y + self.vy >= HEIGHT:
            life_counter -= 1
            return True
        elif (abs(self.y - object.y) <= 50) and (abs(self.x - object.x) <= 50):
            money_counter += 25
            return True
        else:
            return False

class Bird:
    def __init__(self, screen):
        self.screen = screen
        self.x = randint(100, WIDTH-100)
        self.y = 70
        self.vx = choice([-1, 1])
        self.money_time = randint(0, 225)
        self.animation_count = randint(0, 30)

    def move(self):
        if (self.x + self.vx >= WIDTH) or (self.x + self.vx <= 0):
            self.vx *= -1
        self.x += self.vx

    def draw(self):
        if self.animation_count + 1 >= 30:
            self.animation_count = 0

        if self.vx == -1:
            screen.blit(birdLeft[self.animation_count // 15], (self.x, self.y))
            self.animation_count += 1
        elif self.vx == 1:
            screen.blit(birdRight[self.animation_count // 15], (self.x, self.y))
            self.animation_count += 1

    def create_dollar(self):
        global dollars
        if self.money_time == 300:
            money = Dollar(self.screen, self.x, self.y)
            dollars.append(money)
            self.money_time = randint(0, 299)
        else:
            self.money_time += 1


def state(keyboard_keys):
    global Player

    if keyboard_keys[pygame.K_SPACE]:
        if not Player.is_jump:
            Player.is_jump = True
            Player.vy = -20
    if keyboard_keys[pygame.K_LEFT]:
        Player.vector = -1
    elif keyboard_keys[pygame.K_RIGHT]:
        Player.vector = 1
    else:
        Player.vector = 0


def mote_dollars():
    global dollars, Player
    for dollar in dollars:
        if dollar.hit(Player):
            dollars.remove(dollar)
        else:
            dollar.move()
            dollar.draw()


def mote_birds():
    global birds
    for bird in birds:
        bird.move()
        bird.create_dollar()
        bird.draw()


def draw_counters(counter1, counter2):

    fild = pygame.font.SysFont('times new roman', 28)
    text1 = fild.render("Money: " + str(counter1) + " $", True, (0, 175, 0))
    text2 = fild.render("Lives: " + str(counter2), True, (240, 0, 0))
    screen.blit(text1, (20, 10))
    screen.blit(text2, (20, 40))


def is_game_over(number_of_lives, number_of_money):
    global birds, dollars
    if number_of_lives <= 0:
        birds.clear()
        dollars.clear()
        screen.blit(endgame, (0, 0))
        fild = pygame.font.SysFont('times new roman', 36)
        text1 = fild.render("You have just got " + str(number_of_money) + " $ of money. Congratulations !!!",
                            True, (255, 255, 255))
        screen.blit(text1, (270, 550))

def level_up(number_of_money):
    global birds, dollars, life_counter, level
    if number_of_money >= (level ** 1.5) * 75:
        bird = Bird(screen)
        birds.append(bird)

        life_counter += 2
        level += 1
