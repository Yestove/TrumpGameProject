from random import randint
import pygame

WIDTH = 1200
HEIGHT = 800

walkRight = [pygame.image.load('right_1.png'), pygame.image.load('right_2.png'), pygame.image.load('right_3.png'),
             pygame.image.load('right_4.png'), pygame.image.load('right_5.png'), pygame.image.load('right_6.png')]

walkLeft = [pygame.image.load('left_1.png'), pygame.image.load('left_2.png'), pygame.image.load('left_3.png'),
            pygame.image.load('left_4.png'), pygame.image.load('left_5.png'), pygame.image.load('left_6.png')]

bg = pygame.image.load('bg.png')
playerStand = pygame.image.load('idle.png')


class Trump:
    def __init__(self, screen, x, y, animation_count):
        self.screen = screen
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.a = 1
        self.animation_count = animation_count
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


class Dollar:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.vy = 1

    def move(self):
        self.y += self.vy

    def draw(self):
        pygame.draw.circle(self.screen, (0, 0, 255), (self.x, self.y), 6)

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
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.vx = 1
        self.money_time = 0

    def move(self):
        if (self.x + self.vx >= WIDTH) or (self.x + self.vx <= 0):
            self.vx *= -1
        self.x += self.vx

    def draw(self):
        pygame.draw.rect(self.screen, (0, 0, 0), (self.x, self.y, 30, 30))

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


def draw_counters(counter1, counter2):
    fild = pygame.font.Font(None, 36)
    text1 = fild.render("Money: " + str(counter1) + " $", True, (0, 255, 0))
    text2 = fild.render("Lives: " + str(counter2), True, (255, 0, 0))
    screen.blit(text1, (50, 50))
    screen.blit(text2, (50, 80))


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

Player = Trump(screen, 50, HEIGHT - 75, 0)
bird1 = Bird(screen, 30, 30)

dollars = []

money_counter = 0
life_counter = 5

finished = False
while not finished:
    clock.tick(60)
    screen.blit(bg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

    keys = pygame.key.get_pressed()
    state(keys)
    Player.move()
    bird1.move()
    bird1.create_dollar()
    Player.draw()
    bird1.draw()
    mote_dollars()
    draw_counters(money_counter, life_counter)
    pygame.display.update()

pygame.quit()
