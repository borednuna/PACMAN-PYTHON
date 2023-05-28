import pygame
import math
from classes.ghost import Ghost

# Inherit Clyde from Ghost
class Clyde(Ghost):
    img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/orange.png'), (45, 45))
    spooked_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/powerup.png'), (45, 45))
    dead_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/dead.png'), (45, 45))

    # constructor
    def __init__(self, target, id, speed_modifier):
        super().__init__(440, 438, target, 2, id, speed_modifier)
        self.rect = pygame.rect.Rect(0, 0, 0, 0)

    # draw ghost
    def draw(self, screen):
        if (not self.is_frightened and not self.is_dead) or (self.is_eaten and self.is_frightened and not self.is_dead):
            screen.blit(self.img, (self.x_pos, self.y_pos))
        elif self.is_frightened and not self.is_dead and not self.is_eaten:
            screen.blit(self.spooked_img, (self.x_pos, self.y_pos))
        else:
            screen.blit(self.dead_img, (self.x_pos, self.y_pos))
        ghost_rect = pygame.rect.Rect((self.center_x - 18, self.center_y - 18), (36, 36))
        return ghost_rect

    # check collisions
    def check_collisions(self, level, HEIGHT, WIDTH):
        # R, L, U, D
        num1 = ((HEIGHT - 50) // 32)
        num2 = (WIDTH // 30)
        num3 = 15
        self.turns = [False, False, False, False]
        if 0 < self.center_x // 30 < 29:
            if level[(self.center_y - num3) // num1][self.center_x // num2] == 9:
                self.turns[2] = True
            if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                    self.is_in_box or self.is_dead)):
                self.turns[1] = True
            if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                    self.is_in_box or self.is_dead)):
                self.turns[0] = True
            if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                    self.is_in_box or self.is_dead)):
                self.turns[3] = True
            if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                    self.is_in_box or self.is_dead)):
                self.turns[2] = True

            if self.direction == 2 or self.direction == 3:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.is_in_box or self.is_dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.is_in_box or self.is_dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num2) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x - num2) // num2] == 9 and (
                            self.is_in_box or self.is_dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num2) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x + num2) // num2] == 9 and (
                            self.is_in_box or self.is_dead)):
                        self.turns[0] = True

            if self.direction == 0 or self.direction == 1:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.is_in_box or self.is_dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.is_in_box or self.is_dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                            self.is_in_box or self.is_dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                            self.is_in_box or self.is_dead)):
                        self.turns[0] = True

        else:
            self.turns[0] = True
            self.turns[1] = True
        if 350 < self.x_pos < 550 and 330 < self.y_pos < 480: # cek box
            self.is_in_box = True
        else:
            self.is_in_box = False
        return self.turns, self.is_in_box

    # move ghost GBFS
    def move_gbfs(self, level, HEIGHT, WIDTH):
        self.turns, self.is_in_box = self.check_collisions(level, HEIGHT, WIDTH)
        minDistance = 1000000
        newpos = (self.x_pos, self.y_pos)
        fixdir = (self.x_pos, self.y_pos)
        newcenter = (self.center_x, self.center_y)
        fixcenter = (self.center_x, self.center_y)

        for i in range(len(self.turns)):
            if self.turns[i]:
                if i == 0:
                    newpos = (self.x_pos + self.speed, self.y_pos)
                    newcenter = (self.center_x + self.speed, self.center_y)
                elif i == 1:
                    newpos = (self.x_pos - self.speed, self.y_pos)
                    newcenter = (self.center_x - self.speed, self.center_y)
                elif i == 2:
                    newpos = (self.x_pos, self.y_pos - self.speed)
                    newcenter = (self.center_x, self.center_y - self.speed)
                elif i == 3:
                    newpos = (self.x_pos, self.y_pos + self.speed)
                    newcenter = (self.center_x, self.center_y + self.speed)
                distance = (newpos[0] - self.target[0]) ** 2 + (newpos[1] - self.target[1]) ** 2
                if distance < minDistance:
                    minDistance = distance
                    self.direction = i
                    fixdir = newpos
                    fixcenter = newcenter

        self.x_pos = fixdir[0]
        self.y_pos = fixdir[1]

        self.center_x = fixcenter[0]
        self.center_y = fixcenter[1]

        if self.x_pos < -30:
            self.x_pos = 900
            self.center_x = 922
        elif self.x_pos > 900:
            self.x_pos -= 30

        # print(self.target, self.x_pos, self.y_pos, self.turns)
        return self.x_pos, self.y_pos, self.direction

    # move ghost A*
    def move_astar(self, level, HEIGHT, WIDTH):
        frontier = PriorityQueue()
        frontier.put((0, (self.x_pos, self.y_pos)))
        came_from = {}
        cost_so_far = {}
        came_from[(self.x_pos, self.y_pos)] = None
        cost_so_far[(self.x_pos, self.y_pos)] = 0

        while not frontier.empty():
            current = frontier.get()[1]
            if current == self.target:
                break
            
            self.turns, self.is_in_box = self.check_collisions(level, HEIGHT, WIDTH)
            for i in range(len(self.turns)):
                if self.turns[i]:
                    if i == 0:
                        newpos = (current[0] + self.speed, current[1])
                    elif i == 1:
                        newpos = (current[0] - self.speed, current[1])
                    elif i == 2:
                        newpos = (current[0], current[1] - self.speed)
                    elif i == 3:
                        newpos = (current[0], current[1] + self.speed)
                    new_cost = cost_so_far[current] + 1
                    if newpos not in cost_so_far or new_cost < cost_so_far[newpos]:
                        cost_so_far[newpos] = new_cost
                        priority = new_cost + self.heuristic(self.target, newpos)
                        frontier.put((priority, newpos))
                        came_from[newpos] = current
        
        path =  self.reconstruct_path(came_from, self.target, (self.x_pos, self.y_pos))

        if len(path) > 1:
            if path[1][0] > self.x_pos:
                self.direction = 0
            elif path[1][0] < self.x_pos:
                self.direction = 1
            elif path[1][1] < self.y_pos:
                self.direction = 2
            elif path[1][1] > self.y_pos:
                self.direction = 3

        self.x_pos = path[1][0]
        self.y_pos = path[1][1]
        
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos -= 30

        return self.x_pos, self.y_pos, self.direction

    def reconstruct_path(self, came_from, goal, start):
        current = goal
        path = []
        while current != start:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path
        
    # # move ghost
    def move(self, level, HEIGHT, WIDTH):
        # r, l, u, d
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction