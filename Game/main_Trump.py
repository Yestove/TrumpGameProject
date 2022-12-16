from random import randint
from random import choice
import pygame
import lib

pygame.init()
pygame.display.set_caption('Trump Game')
screen = pygame.display.set_mode((lib.WIDTH, lib.HEIGHT))
clock = pygame.time.Clock()

ch_finished = False
while not ch_finished:
    clock.tick(60)
    screen.blit(lib.bg_initial, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            level = lib.ch_level(mouse_x, mouse_y)
            ch_finished = True
    pygame.display.update()

lib.number_of_birds = int(level)
lib.life_counter = 2 * lib.number_of_birds
        
number_of_birds = lib.number_of_birds
life_counter = lib.life_counter

Player = lib.Player

birds = lib.birds
dollars = lib.dollars

money_counter = lib.money_counter

for i in range(number_of_birds):
    bird = lib.Bird(screen)
    birds.append(bird)

finished = False
while not finished:
    clock.tick(60)
    screen.blit(lib.bg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

    keys = pygame.key.get_pressed()
    lib.state(keys)
    Player.move()
    Player.draw()
    lib.mote_birds()
    lib.mote_dollars()
    lib.draw_counters(lib.money_counter, lib.life_counter)
    lib.level_up(lib.money_counter)
    lib.is_game_over(lib.life_counter, lib.money_counter)
    pygame.display.update()

pygame.quit()
