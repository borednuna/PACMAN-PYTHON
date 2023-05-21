import copy
import pygame
import math
from board import boards
from classes.blinky import Blinky
from classes.pinky import Pinky
from classes.inky import Inky
from classes.clyde import Clyde
from classes.utility import Utility
from classes.player import Player

pygame.init()

WIDTH = 900
HEIGHT = 950
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)
level = copy.deepcopy(boards)
color = 'blue'
PI = math.pi
flicker = False
# R, L, U, D
turns_allowed = [False, False, False, False]
direction_command = 0
score = 0
counter = 0
power_counter = 0
eaten_ghost = [False, False, False, False]
moving = False
startup_counter = 0
game_over = False
game_won = False

# instatiate player
player = Player()
targets = [(player.x, player.y), (player.x, player.y), (player.x, player.y), (player.x, player.y)]

# instatiate ghosts
blinky = Blinky((player.x, player.y), 0)
inky = Inky((player.x, player.y), 1)
pinky = Pinky((player.x, player.y), 2)
clyde = Clyde((player.x, player.y), 3)

# instantiate utility class
utility = Utility()

def get_targets(blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y):
    if player.x < 450:
        runaway_x = 900
    else:
        runaway_x = 0
    if player.y < 450:
        runaway_y = 900
    else:
        runaway_y = 0
    return_target = (380, 400)
    if player.is_powered_up:
        if not blinky.is_dead and not eaten_ghost[0]:
            blink_target = (runaway_x, runaway_y)
        elif not blinky.is_dead and eaten_ghost[0]:
            if 340 < blink_x < 560 and 340 < blink_y < 500:
                blink_target = (400, 100)
            else:
                blink_target = (player.x, player.y)
        else:
            blink_target = return_target
        if not inky.is_dead and not eaten_ghost[1]:
            ink_target = (runaway_x, player.y)
        elif not inky.is_dead and eaten_ghost[1]:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (player.x, player.y)
        else:
            ink_target = return_target
        if not pinky.is_dead:
            pink_target = (player.x, runaway_y)
        elif not pinky.is_dead and eaten_ghost[2]:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (player.x, player.y)
        else:
            pink_target = return_target
        if not clyde.is_dead and not eaten_ghost[3]:
            clyd_target = (450, 450)
        elif not clyde.is_dead and eaten_ghost[3]:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyd_target = (400, 100)
            else:
                clyd_target = (player.x, player.y)
        else:
            clyd_target = return_target
    else:
        if not blinky.is_dead:
            if 340 < blink_x < 560 and 340 < blink_y < 500:
                blink_target = (400, 100)
            else:
                blink_target = (player.x, player.y)
        else:
            blink_target = return_target
        if not inky.is_dead:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (player.x, player.y)
        else:
            ink_target = return_target
        if not pinky.is_dead:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (player.x, player.y)
        else:
            pink_target = return_target
        if not clyde.is_dead:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyd_target = (400, 100)
            else:
                clyd_target = (player.x, player.y)
        else:
            clyd_target = return_target
    return [blink_target, ink_target, pink_target, clyd_target]

run = True
while run:
    timer.tick(fps)
    if counter < 19:
        counter += 1
        if counter > 3:
            flicker = False
    else:
        counter = 0
        flicker = True
    if player.is_powered_up and power_counter < 600:
        power_counter += 1
        blinky.is_frightened = True
        inky.is_frightened = True
        pinky.is_frightened = True
        clyde.is_frightened = True
    elif player.is_powered_up and power_counter >= 600:
        power_counter = 0
        player.is_powered_up = False
        blinky.is_frightened = False
        inky.is_frightened = False
        pinky.is_frightened = False
        clyde.is_frightened = False
        eaten_ghost = [False, False, False, False]
    if startup_counter < 180 and not game_over and not game_won:
        moving = False
        startup_counter += 1
    else:
        moving = True

    screen.fill('black')
    utility.draw_board(screen, level, flicker)
    center_x = player.x + 23
    center_y = player.y + 24
    if player.is_powered_up:
        ghost_speeds = [1, 1, 1, 1]
        blinky.speed = 1
        inky.speed = 1
        pinky.speed = 1
        clyde.speed = 1
    else:
        ghost_speeds = [2, 2, 2, 2]
        blinky.speed = 2
        inky.speed = 2
        pinky.speed = 2
        clyde.speed = 2
    if blinky.is_eaten:
        ghost_speeds[0] = 2
        blinky.speed = 2
    if inky.is_eaten:
        ghost_speeds[1] = 2
        inky.speed = 2
    if pinky.is_eaten:
        ghost_speeds[2] = 2
        pinky.speed = 2
    if clyde.is_eaten:
        ghost_speeds[3] = 2
        clyde.speed = 2
    if blinky.is_dead:
        ghost_speeds[0] = 4
        blinky.speed = 4
    if inky.is_dead:
        ghost_speeds[1] = 4
        inky.speed = 4
    if pinky.is_dead:
        ghost_speeds[2] = 4
        pinky.speed = 4
    if clyde.is_dead:
        ghost_speeds[3] = 4
        clyde.speed = 4

    game_won = True
    for i in range(len(level)):
        if 1 in level[i] or 2 in level[i]:
            game_won = False

    player_circle = pygame.draw.circle(screen, 'black', (center_x, center_y), 20, 2)
    player.draw_player(screen, counter)
    blinky.rect = blinky.draw(screen)
    inky.rect = inky.draw(screen)
    pinky.rect = pinky.draw(screen)
    clyde.rect = clyde.draw(screen)
    utility.draw_misc(screen, score, player.is_powered_up, player.lives, game_over, game_won)
    targets = get_targets(blinky.x_pos, blinky.y_pos, inky.x_pos, inky.x_pos, pinky.x_pos, pinky.y_pos, clyde.x_pos, clyde.y_pos)

    turns_allowed = player.check_position(center_x, center_y, level)
    if moving:
        player.move_player(turns_allowed)
        if not blinky.is_dead and not blinky.is_in_box:
            blinky.x_pos, blinky.y_pos, blinky.direction = blinky.move(level, HEIGHT, WIDTH)
        else:
            blinky.x_pos, blinky.y_pos, blinky.direction = blinky.move(level, HEIGHT, WIDTH)
        if not pinky.is_dead and not pinky.is_in_box:
            pinky.x_pos, pinky.y_pos, pinky.direction = pinky.move(level, HEIGHT, WIDTH)
        else:
            pinky.x_pos, pinky.y_pos, pinky.direction = pinky.move(level, HEIGHT, WIDTH)
        if not inky.is_dead and not inky.is_in_box:
            inky.x_pos, inky.y_pos, inky.direction = inky.move(level, HEIGHT, WIDTH)
        else:
            inky.x_pos, inky.y_pos, inky.direction = inky.move(level, HEIGHT, WIDTH)
        clyde.x_pos, clyde.x_pos, clyde.direction = clyde.move(level, HEIGHT, WIDTH)
    score, player.is_powered_up, power_counter, eaten_ghost = utility.check_collisions(score, player.is_powered_up, power_counter, eaten_ghost, level, player.x, center_x, center_y)
    # add to if not player.is_powered_up to check if eaten ghosts
    if not player.is_powered_up:
        if (player_circle.colliderect(blinky.rect) and not blinky.is_dead) or \
                (player_circle.colliderect(inky.rect) and not inky.is_dead) or \
                (player_circle.colliderect(pinky.rect) and not pinky.is_dead) or \
                (player_circle.colliderect(clyde.rect) and not clyde.is_dead):
            if player.player.lives > 0:
                player.player.lives -= 1
                startup_counter = 0
                player.is_powered_up = False
                power_counter = 0
                player.x = 450
                player.y = 663
                player.direction = 0
                direction_command = 0
                blinky.x_pos = 56
                blinky.y_pos = 58
                blinky.direction = 0
                inky.x_pos = 440
                inky.y_pos = 388
                inky.direction = 2
                pinky.x_pos = 440
                pinky.y_pos = 438
                pinky.direction = 2
                clyde.x_pos = 440
                clyde.y_pos = 438
                clyde.direction = 2
                eaten_ghost = [False, False, False, False]
                blinky.is_dead = False
                inky.is_dead = False
                clyde.is_dead = False
                pinky.is_dead = False
            else:
                game_over = True
                moving = False
                startup_counter = 0
    if player.is_powered_up and player_circle.colliderect(blinky.rect) and eaten_ghost[0] and not blinky.is_dead:
        if player.player.lives > 0:
            player.is_powered_up = False
            power_counter = 0
            player.player.lives -= 1
            startup_counter = 0
            player.x = 450
            player.y = 663
            player.direction = 0
            direction_command = 0
            blinky.x_pos = 56
            blinky.y_pos = 58
            blinky.direction = 0
            inky.x_pos = 440
            inky.y_pos = 388
            inky.direction = 2
            pinky.x_pos = 440
            pinky.y_pos = 438
            pinky.direction = 2
            clyde.x_pos = 440
            clyde.y_pos = 438
            clyde.direction = 2
            eaten_ghost = [False, False, False, False]
            blinky.is_dead = False
            inky.is_dead = False
            clyde.is_dead = False
            pinky.is_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if player.is_powered_up and player_circle.colliderect(inky.rect) and eaten_ghost[1] and not inky.is_dead:
        if player.player.lives > 0:
            player.is_powered_up = False
            power_counter = 0
            player.player.lives -= 1
            startup_counter = 0
            player.x = 450
            player.y = 663
            player.direction = 0
            direction_command = 0
            blinky.x_pos = 56
            blinky.y_pos = 58
            blinky.direction = 0
            inky.x_pos = 440
            inky.y_pos = 388
            inky.direction = 2
            pinky.x_pos = 440
            pinky.y_pos = 438
            pinky.direction = 2
            clyde.x_pos = 440
            clyde.y_pos = 438
            clyde.direction = 2
            eaten_ghost = [False, False, False, False]
            blinky.is_dead = False
            inky.is_dead = False
            clyde.is_dead = False
            pinky.is_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if player.is_powered_up and player_circle.colliderect(pinky.rect) and eaten_ghost[2] and not pinky.is_dead:
        if player.lives > 0:
            player.is_powered_up = False
            power_counter = 0
            player.lives -= 1
            startup_counter = 0
            player.x = 450
            player.y = 663
            player.direction = 0
            direction_command = 0
            blinky.x_pos = 56
            blinky.y_pos = 58
            blinky.direction = 0
            inky.x_pos = 440
            inky.y_pos = 388
            inky.direction = 2
            pinky.x_pos = 440
            pinky.y_pos = 438
            pinky.direction = 2
            clyde.x_pos = 440
            clyde.y_pos = 438
            clyde.direction = 2
            eaten_ghost = [False, False, False, False]
            blinky.is_dead = False
            inky.is_dead = False
            clyde.is_dead = False
            pinky.is_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if player.is_powered_up and player_circle.colliderect(clyde.rect) and eaten_ghost[3] and not clyde.is_dead:
        if player.lives > 0:
            player.is_powered_up = False
            power_counter = 0
            player.lives -= 1
            startup_counter = 0
            player.x = 450
            player.y = 663
            player.direction = 0
            direction_command = 0
            blinky.x_pos = 56
            blinky.y_pos = 58
            blinky.direction = 0
            inky.x_pos = 440
            inky.y_pos = 388
            inky.direction = 2
            pinky.x_pos = 440
            pinky.y_pos = 438
            pinky.direction = 2
            clyde.x_pos = 440
            clyde.y_pos = 438
            clyde.direction = 2
            eaten_ghost = [False, False, False, False]
            blinky.is_dead = False
            inky.is_dead = False
            clyde.is_dead = False
            pinky.is_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if player.is_powered_up and player_circle.colliderect(blinky.rect) and not blinky.is_dead and not eaten_ghost[0]:
        blinky.is_dead = True
        eaten_ghost[0] = True
        blinky.is_dead = True
        blinky.is_eaten = True
        score += (2 ** eaten_ghost.count(True)) * 100
    if player.is_powered_up and player_circle.colliderect(inky.rect) and not inky.is_dead and not eaten_ghost[1]:
        inky.is_dead = True
        eaten_ghost[1] = True
        inky.is_dead = True
        inky.is_eaten = True
        score += (2 ** eaten_ghost.count(True)) * 100
    if player.is_powered_up and player_circle.colliderect(pinky.rect) and not pinky.is_dead and not eaten_ghost[2]:
        pinky.is_dead = True
        eaten_ghost[2] = True
        pinky.is_dead = True
        pinky.is_eaten = True
        score += (2 ** eaten_ghost.count(True)) * 100
    if player.is_powered_up and player_circle.colliderect(clyde.rect) and not clyde.is_dead and not eaten_ghost[3]:
        clyde.is_dead = True
        eaten_ghost[3] = True
        clyde.is_dead = True
        clyde.is_eaten = True
        score += (2 ** eaten_ghost.count(True)) * 100

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction_command = 0
            if event.key == pygame.K_LEFT:
                direction_command = 1
            if event.key == pygame.K_UP:
                direction_command = 2
            if event.key == pygame.K_DOWN:
                direction_command = 3
            if event.key == pygame.K_SPACE and (game_over or game_won):
                player.is_powered_up = False
                power_counter = 0
                player.lives -= 1
                startup_counter = 0
                player.x = 450
                player.y = 663
                direction = 0
                direction_command = 0
                blinky.x_pos = 56
                blinky.y_pos = 58
                blinky.direction = 0
                inky.x_pos = 440
                inky.y_pos = 388
                inky.direction = 2
                pinky.x_pos = 440
                pinky.y_pos = 438
                pinky.direction = 2
                clyde.x_pos = 440
                clyde.y_pos = 438
                clyde.direction = 2
                eaten_ghost = [False, False, False, False]
                blinky.is_dead = False
                inky.is_dead = False
                clyde.is_dead = False
                pinky.is_dead = False
                score = 0
                player.lives = 3
                level = copy.deepcopy(boards)
                game_over = False
                game_won = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and direction_command == 0:
                direction_command = player.direction
            if event.key == pygame.K_LEFT and direction_command == 1:
                direction_command = player.direction
            if event.key == pygame.K_UP and direction_command == 2:
                direction_command = player.direction
            if event.key == pygame.K_DOWN and direction_command == 3:
                direction_command = player.direction

    if direction_command == 0 and turns_allowed[0]:
        player.direction = 0
    if direction_command == 1 and turns_allowed[1]:
        player.direction = 1
    if direction_command == 2 and turns_allowed[2]:
        player.direction = 2
    if direction_command == 3 and turns_allowed[3]:
        player.direction = 3

    if player.x > 900:
        player.x = -47
    elif player.x < -50:
        player.x = 897

    if blinky.is_in_box and blinky.is_dead:
        blinky.is_dead = False
    if inky.is_in_box and inky.is_dead:
        inky.is_dead = False
    if pinky.is_in_box and pinky.is_dead:
        pinky.is_dead = False
    if clyde.is_in_box and clyde.is_dead:
        clyde.is_dead = False

    pygame.display.flip()
pygame.quit()


# sound effects, restart and winning messages
