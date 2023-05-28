import pygame
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

WIDTH = 900
HEIGHT = 950

class Levels:
    def __init__(self, game_manager, screen, level_index):
        self.game_manager = game_manager
        self.screen = screen
        self.level_index = level_index
        self.level = copy.deepcopy(boards)
        self.is_running = False

    def initialize(self):
        # R, L, U, D
        self.turns_allowed = [False, False, False, False]
        self.direction_command = 0
        self.score = 0
        self.counter = 0
        self.power_counter = 0
        self.eaten_ghost = [False, False, False, False]
        self.moving = False
        self.startup_counter = 0
        self.game_over = False
        self.game_won = False

        # instatiate self.player
        self.player = Player(self.level_index)
        self.targets = [(self.player.x, self.player.y), (self.player.x, self.player.y), (self.player.x, self.player.y), (self.player.x, self.player.y)]
        self.center_x = self.player.x + 23
        self.center_y = self.player.y + 24
        self.player_circle = pygame.draw.circle(self.screen, 'black', (self.center_x, self.center_y), 20, 2)

        # instatiate ghosts
        self.blinky = Blinky((self.player.x, self.player.y), 0, self.level_index)
        self.inky = Inky((self.player.x, self.player.y), 1, self.level_index)
        self.pinky = Pinky((self.player.x, self.player.y), 2, self.level_index)
        self.clyde = Clyde((self.player.x, self.player.y), 3, self.level_index)

        # instantiate utility class
        self.utility = Utility()

    def handle_events(self):
        # Handle level-specific events here
        pygame.display.init()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.direction_command = 0
                if event.key == pygame.K_LEFT:
                    self.direction_command = 1
                if event.key == pygame.K_UP:
                    self.direction_command = 2
                if event.key == pygame.K_DOWN:
                    self.direction_command = 3
                if event.key == pygame.K_SPACE and (self.game_over or self.game_won):
                    self.player.is_powered_up = False
                    self.power_counter = 0
                    self.player.lives -= 1
                    self.startup_counter = 0
                    self.player.x = 450
                    self.player.y = 663
                    self.direction = 0
                    self.direction_command = 0
                    self.blinky.x_pos = 56
                    self.blinky.y_pos = 58
                    self.blinky.direction = 0
                    self.inky.x_pos = 440
                    self.inky.y_pos = 388
                    self.inky.direction = 2
                    self.pinky.x_pos = 440
                    self.pinky.y_pos = 438
                    self.pinky.direction = 2
                    self.clyde.x_pos = 440
                    self.clyde.y_pos = 438
                    self.clyde.direction = 2
                    self.eaten_ghost = [False, False, False, False]
                    self.blinky.is_dead = False
                    self.inky.is_dead = False
                    self.clyde.is_dead = False
                    self.pinky.is_dead = False
                    self.score = 0
                    self.player.lives = 3
                    self.level = copy.deepcopy(boards)
                    self.game_over = False
                    self.game_won = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT and self.direction_command == 0:
                    self.direction_command = self.player.direction
                if event.key == pygame.K_LEFT and self.direction_command == 1:
                    self.direction_command = self.player.direction
                if event.key == pygame.K_UP and self.direction_command == 2:
                    self.direction_command = self.player.direction
                if event.key == pygame.K_DOWN and self.direction_command == 3:
                    self.direction_command = self.player.direction

        if self.direction_command == 0 and self.turns_allowed[0]:
            self.player.direction = 0
            
        if self.direction_command == 1 and self.turns_allowed[1]:
            self.player.direction = 1
        if self.direction_command == 2 and self.turns_allowed[2]:
            self.player.direction = 2
        if self.direction_command == 3 and self.turns_allowed[3]:
            self.player.direction = 3

        if self.player.x > 900:
            self.player.x = -47
        elif self.player.x < -50:
            self.player.x = 897

        if self.blinky.is_in_box and self.blinky.is_dead:
            self.blinky.is_dead = False
        if self.inky.is_in_box and self.inky.is_dead:
            self.inky.is_dead = False
        if self.pinky.is_in_box and self.pinky.is_dead:
            self.pinky.is_dead = False
        if self.clyde.is_in_box and self.clyde.is_dead:
            self.clyde.is_dead = False

    def update(self):
        # Update level-specific logic here
        if self.game_manager.counter < 19:
            self.game_manager.counter += 1
            if self.game_manager.counter > 3:
                self.game_manager.flicker = False
        else:
            self.game_manager.counter = 0
            self.game_manager.flicker = True
        if self.player.is_powered_up and self.power_counter < 600:
            self.power_counter += 1
            self.blinky.is_frightened = True
            self.inky.is_frightened = True
            self.pinky.is_frightened = True
            self.clyde.is_frightened = True
        elif self.player.is_powered_up and self.power_counter >= 600:
            self.power_counter = 0
            self.player.is_powered_up = False
            self.blinky.is_frightened = False
            self.inky.is_frightened = False
            self.pinky.is_frightened = False
            self.clyde.is_frightened = False
            self.eaten_ghost = [False, False, False, False]
        if self.startup_counter < 180 and not self.game_over and not self.game_won:
            self.moving = False
            self.startup_counter += 1
        else:
            self.moving = True

        self.center_x = self.player.x + 23
        self.center_y = self.player.y + 24
        if self.player.is_powered_up:
            self.ghost_speeds = [1, 1, 1, 1]
            self.blinky.speed = 1
            self.inky.speed = 1
            self.pinky.speed = 1
            self.clyde.speed = 1
        else:
            self.ghost_speeds = [2, 2, 2, 2]
            self.blinky.speed = 2
            self.inky.speed = 2
            self.pinky.speed = 2
            self.clyde.speed = 2
        if self.blinky.is_eaten:
            self.ghost_speeds[0] = 2
            self.blinky.speed = 2
        if self.inky.is_eaten:
            self.ghost_speeds[1] = 2
            self.inky.speed = 2
        if self.pinky.is_eaten:
            self.ghost_speeds[2] = 2
            self.pinky.speed = 2
        if self.clyde.is_eaten:
            self.ghost_speeds[3] = 2
            self.clyde.speed = 2
        if self.blinky.is_dead:
            self.ghost_speeds[0] = 4
            self.blinky.speed = 4
        if self.inky.is_dead:
            self.ghost_speeds[1] = 4
            self.inky.speed = 4
        if self.pinky.is_dead:
            self.ghost_speeds[2] = 4
            self.pinky.speed = 4
        if self.clyde.is_dead:
            self.ghost_speeds[3] = 4
            self.clyde.speed = 4

        self.game_won = True
        for i in range(len(self.level)):
            if 1 in self.level[i] or 2 in self.level[i]:
                self.game_won = False

        self.targets = self.utility.get_targets(self.blinky, self.inky, self.pinky, self.clyde, self.player, self.eaten_ghost)
        self.blinky.target = self.targets[0]
        self.inky.target = self.targets[1]
        self.pinky.target = self.targets[2]
        self.clyde.target = self.targets[3]
        self.turns_allowed = self.player.check_position(self.center_x, self.center_y, self.level)

        if self.moving:
            self.player.move_player(self.turns_allowed)
            if not self.blinky.is_dead and not self.blinky.is_in_box:
                self.blinky.x_pos, self.blinky.y_pos, self.blinky.direction = self.blinky.move_gbfs(self.level, HEIGHT, WIDTH)
            else:
                self.blinky.x_pos, self.blinky.y_pos, self.blinky.direction = self.blinky.move_astar(self.level, HEIGHT, WIDTH)
            if not self.pinky.is_dead and not self.pinky.is_in_box:
                self.pinky.x_pos, self.pinky.y_pos, self.pinky.direction = self.pinky.move(self.level, HEIGHT, WIDTH)
            else:
                self.pinky.x_pos, self.pinky.y_pos, self.pinky.direction = self.pinky.move(self.level, HEIGHT, WIDTH)
            if not self.inky.is_dead and not self.inky.is_in_box:
                self.inky.x_pos, self.inky.y_pos, self.inky.direction = self.inky.move(self.level, HEIGHT, WIDTH)
            else:
                self.inky.x_pos, self.inky.y_pos, self.inky.direction = self.inky.move(self.level, HEIGHT, WIDTH)
            self.clyde.x_pos, self.clyde.x_pos, self.clyde.direction = self.clyde.move(self.level, HEIGHT, WIDTH)
        self.score, self.player.is_powered_up, self.power_counter, self.eaten_ghost = self.utility.check_collisions(self.score, self.player.is_powered_up, self.power_counter, self.eaten_ghost, self.level, self.player.x, self.center_x, self.center_y)
        # add to if not self.player.is_powered_up to check if eaten ghosts
        if not self.player.is_powered_up:
            if (self.player_circle.colliderect(self.blinky.rect) and not self.blinky.is_dead) or \
                    (self.player_circle.colliderect(self.inky.rect) and not self.inky.is_dead) or \
                    (self.player_circle.colliderect(self.pinky.rect) and not self.pinky.is_dead) or \
                    (self.player_circle.colliderect(self.clyde.rect) and not self.clyde.is_dead):
                if self.player.lives > 0:
                    self.player.lives -= 1
                    self.startup_counter = 0
                    self.player.is_powered_up = False
                    self.power_counter = 0
                    self.player.x = 450
                    self.player.y = 663
                    self.player.direction = 0
                    self.direction_command = 0
                    self.blinky.x_pos = 56
                    self.blinky.y_pos = 58
                    self.blinky.direction = 0
                    self.inky.x_pos = 440
                    self.inky.y_pos = 388
                    self.inky.direction = 2
                    self.pinky.x_pos = 440
                    self.pinky.y_pos = 438
                    self.pinky.direction = 2
                    self.clyde.x_pos = 56
                    self.clyde.y_pos = 58
                    self.clyde.direction = 2
                    self.eaten_ghost = [False, False, False, False]
                    self.blinky.is_dead = False
                    self.inky.is_dead = False
                    self.clyde.is_dead = False
                    self.pinky.is_dead = False
                else:
                    self.game_over = True
                    self.moving = False
                    self.startup_counter = 0
        if self.player.is_powered_up and self.player_circle.colliderect(self.blinky.rect) and self.eaten_ghost[0] and not self.blinky.is_dead:
            if self.player.lives > 0:
                self.player.is_powered_up = False
                self.power_counter = 0
                self.player.lives -= 1
                self.startup_counter = 0
                self.player.x = 450
                self.player.y = 663
                self.player.direction = 0
                self.direction_command = 0
                self.blinky.x_pos = 56
                self.blinky.y_pos = 58
                self.blinky.direction = 0
                self.inky.x_pos = 440
                self.inky.y_pos = 388
                self.inky.direction = 2
                self.pinky.x_pos = 440
                self.pinky.y_pos = 438
                self.pinky.direction = 2
                self.clyde.x_pos = 440
                self.clyde.y_pos = 438
                self.clyde.direction = 2
                self.eaten_ghost = [False, False, False, False]
                self.blinky.is_dead = False
                self.inky.is_dead = False
                self.clyde.is_dead = False
                self.pinky.is_dead = False
            else:
                self.game_over = True
                self.moving = False
                self.startup_counter = 0
        if self.player.is_powered_up and self.player_circle.colliderect(self.inky.rect) and self.eaten_ghost[1] and not self.inky.is_dead:
            if self.player.lives > 0:
                self.player.is_powered_up = False
                self.power_counter = 0
                self.player.lives -= 1
                self.startup_counter = 0
                self.player.x = 450
                self.player.y = 663
                self.player.direction = 0
                self.direction_command = 0
                self.blinky.x_pos = 56
                self.blinky.y_pos = 58
                self.blinky.direction = 0
                self.inky.x_pos = 440
                self.inky.y_pos = 388
                self.inky.direction = 2
                self.pinky.x_pos = 440
                self.pinky.y_pos = 438
                self.pinky.direction = 2
                self.clyde.x_pos = 440
                self.clyde.y_pos = 438
                self.clyde.direction = 2
                self.eaten_ghost = [False, False, False, False]
                self.blinky.is_dead = False
                self.inky.is_dead = False
                self.clyde.is_dead = False
                self.pinky.is_dead = False
            else:
                self.game_over = True
                self.moving = False
                self.startup_counter = 0
        if self.player.is_powered_up and self.player_circle.colliderect(self.pinky.rect) and self.eaten_ghost[2] and not self.pinky.is_dead:
            if self.player.lives > 0:
                self.player.is_powered_up = False
                self.power_counter = 0
                self.player.lives -= 1
                self.startup_counter = 0
                self.player.x = 450
                self.player.y = 663
                self.player.direction = 0
                self.direction_command = 0
                self.blinky.x_pos = 56
                self.blinky.y_pos = 58
                self.blinky.direction = 0
                self.inky.x_pos = 440
                self.inky.y_pos = 388
                self.inky.direction = 2
                self.pinky.x_pos = 440
                self.pinky.y_pos = 438
                self.pinky.direction = 2
                self.clyde.x_pos = 440
                self.clyde.y_pos = 438
                self.clyde.direction = 2
                self.eaten_ghost = [False, False, False, False]
                self.blinky.is_dead = False
                self.inky.is_dead = False
                self.clyde.is_dead = False
                self.pinky.is_dead = False
            else:
                self.game_over = True
                self.moving = False
                self.startup_counter = 0
        if self.player.is_powered_up and self.player_circle.colliderect(self.clyde.rect) and self.eaten_ghost[3] and not self.clyde.is_dead:
            if self.player.lives > 0:
                self.player.is_powered_up = False
                self.power_counter = 0
                self.player.lives -= 1
                self.startup_counter = 0
                self.player.x = 450
                self.player.y = 663
                self.player.direction = 0
                self.direction_command = 0
                self.blinky.x_pos = 56
                self.blinky.y_pos = 58
                self.blinky.direction = 0
                self.inky.x_pos = 440
                self.inky.y_pos = 388
                self.inky.direction = 2
                self.pinky.x_pos = 440
                self.pinky.y_pos = 438
                self.pinky.direction = 2
                self.clyde.x_pos = 440
                self.clyde.y_pos = 438
                self.clyde.direction = 2
                self.eaten_ghost = [False, False, False, False]
                self.blinky.is_dead = False
                self.inky.is_dead = False
                self.clyde.is_dead = False
                self.pinky.is_dead = False
            else:
                self.game_over = True
                self.moving = False
                self.startup_counter = 0
        if self.player.is_powered_up and self.player_circle.colliderect(self.blinky.rect) and not self.blinky.is_dead and not self.eaten_ghost[0]:
            self.blinky.is_dead = True
            self.eaten_ghost[0] = True
            self.blinky.is_dead = True
            self.blinky.is_eaten = True
            self.score += (2 ** self.eaten_ghost.count(True)) * 100
        if self.player.is_powered_up and self.player_circle.colliderect(self.inky.rect) and not self.inky.is_dead and not self.eaten_ghost[1]:
            self.inky.is_dead = True
            self.eaten_ghost[1] = True
            self.inky.is_dead = True
            self.inky.is_eaten = True
            self.score += (2 ** self.eaten_ghost.count(True)) * 100
        if self.player.is_powered_up and self.player_circle.colliderect(self.pinky.rect) and not self.pinky.is_dead and not self.eaten_ghost[2]:
            self.pinky.is_dead = True
            self.eaten_ghost[2] = True
            self.pinky.is_dead = True
            self.pinky.is_eaten = True
            self.score += (2 ** self.eaten_ghost.count(True)) * 100
        if self.player.is_powered_up and self.player_circle.colliderect(self.clyde.rect) and not self.clyde.is_dead and not self.eaten_ghost[3]:
            self.clyde.is_dead = True
            self.eaten_ghost[3] = True
            self.clyde.is_dead = True
            self.clyde.is_eaten = True
            self.score += (2 ** self.eaten_ghost.count(True)) * 100

    def render(self):
        # Render level-specific graphics here
        self.screen.fill('black')
        self.utility.draw_board(self.screen, self.level, self.game_manager.flicker)
        self.player_circle = pygame.draw.circle(self.screen, 'black', (self.center_x, self.center_y), 20, 2)
        self.player.draw_player(self.screen, self.counter)
        self.blinky.rect = self.blinky.draw(self.screen)
        self.inky.rect = self.inky.draw(self.screen)
        self.pinky.rect = self.pinky.draw(self.screen)
        self.clyde.rect = self.clyde.draw(self.screen)
        self.utility.draw_misc(self.screen, self.score, self.player.is_powered_up, self.player.lives, self.game_over, self.game_won)

    def start_level(self):
        self.initialize()
        self.level_running = True

        while self.level_running:
            self.handle_events()
            self.update()
            self.render()

            pygame.display.flip()
            self.game_manager.timer.tick(60)

    def stop_level(self):
        self.level_running = False

class GameManager:
    def __init__(self):
        pygame.init()
        
        self.running = False
        self.screen = None
        self.levels = []
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        self.counter = 0
        self.timer = pygame.time.Clock()
        self.running = True
        self.flicker = False
        self.fps = 60
        self.font = pygame.font.Font('freesansbold.ttf', 20)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self, level_index):
        # Update game logic here
        current_level = self.levels[level_index]
        if current_level.game_won:
            self.switch_level(level_index + 1)

    def quit(self):
        self.running = False

    def add_level(self, level):
        self.levels.append(level)

    def switch_level(self, level_index):
        current_level = self.levels[level_index]
        current_level.start_level()

    def run(self):
        self.initialize()

        while self.running:
            self.handle_events()
            self.update()

            pygame.display.flip()

        pygame.quit()

game_manager = GameManager()

level1 = Levels(game_manager, game_manager.screen, 1)
level2 = Levels(game_manager, game_manager.screen, 2)
level3 = Levels(game_manager, game_manager.screen, 3)
level4 = Levels(game_manager, game_manager.screen, 4)
level5 = Levels(game_manager, game_manager.screen, 5)
game_manager.add_level(level1)
game_manager.switch_level(0)