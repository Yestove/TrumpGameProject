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


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

Player = Trump(screen, 50, HEIGHT - 75, 0)

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
    Player.draw()
    pygame.display.update()

pygame.quit()
