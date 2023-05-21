import pygame
from classes.ghost import Ghost

# Inherit Pinky from Ghost
class Pinky(Ghost):
    img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/pink.png'), (45, 45))
    spooked_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/powerup.png'), (45, 45))
    dead_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/dead.png'), (45, 45))

    # constructor
    def __init__(self, target, id):
        super().__init__(56, 58, target, 2, id)
        rect = pygame.rect.Rect(0, 0, 0, 0)

    # draw ghost
    def draw(self, screen):
        if (not self.is_frightened and not self.is_dead) or (self.is_eaten and self.is_frightened and not self.is_dead):
            screen.blit(self.img, (self.x_pos, self.y_pos))
        elif self.is_frightened and not self.is_dead and not self.is_eaten:
            screen.blit(self.spooked_img, (self.x_pos, self.y_pos))
        else:
            screen.blit(self.is_dead_img, (self.x_pos, self.y_pos))
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
        if 350 < self.x_pos < 550 and 370 < self.y_pos < 480:
            self.is_in_box = True
        else:
            self.is_in_box = False
        return self.turns, self.is_in_box
    
    # move ghost
    def move(self, level, HEIGHT, WIDTH):
        # r, l, u, d
        # inky is going to turn left or right whenever advantageous, but only up or down on collision
        self.turns, self.is_in_box = self.check_collisions(level, HEIGHT, WIDTH)
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
                self.center_x += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                    self.center_y += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                    self.center_y -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                    self.center_x -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                    self.center_y += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                    self.center_y -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                    self.center_x -= self.speed
            elif self.turns[0]:
                self.x_pos += self.speed
                self.center_x += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
                self.center_x -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                    self.center_y += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                    self.center_y -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                    self.center_x += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                    self.center_y += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                    self.center_y -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                    self.center_x += self.speed
            elif self.turns[1]:
                self.x_pos -= self.speed
                self.center_x -= self.speed
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
                self.center_x -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
                self.center_y -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                    self.center_x += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                    self.center_x -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                    self.center_y += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                    self.center_x -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                    self.center_y += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                    self.center_x += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                    self.center_x += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                    self.center_x -= self.speed
                else:
                    self.y_pos -= self.speed
                    self.center_y -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
                self.center_y += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                    self.center_x += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                    self.center_x -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                    self.center_y -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                    self.center_y -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                    self.center_x -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                    self.center_x += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                    self.center_x += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                    self.center_x -= self.speed
                else:
                    self.y_pos += self.speed
                    self.center_y += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
            self.center_x = 922
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction

