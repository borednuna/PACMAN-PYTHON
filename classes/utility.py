import pygame
import math
from board import boards

WIDTH = 900
HEIGHT = 950

class Utility:
    def __init__(self):
        self.player_images = []
        pygame.font.init()
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        for i in range(1, 5):
            self.player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (45, 45)))

    def get_targets(self, blinky, inky, pinky, clyde, player, eaten_ghost):
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
                if 340 < blinky.x_pos < 560 and 340 < blinky.y_pos < 500:
                    blink_target = (400, 100)
                else:
                    blink_target = (player.x, player.y)
            else:
                blink_target = return_target
            if not inky.is_dead and not eaten_ghost[1]:
                ink_target = (runaway_x, player.y)
            elif not inky.is_dead and eaten_ghost[1]:
                if 340 < inky.x_pos < 560 and 340 < inky.y_pos < 500:
                    ink_target = (400, 100)
                else:
                    ink_target = (player.x, player.y)
            else:
                ink_target = return_target
            if not pinky.is_dead:
                pink_target = (player.x, runaway_y)
            elif not pinky.is_dead and eaten_ghost[2]:
                if 340 < pinky.x_pos < 560 and 340 < pinky.y_pos < 500:
                    pink_target = (400, 100)
                else:
                    pink_target = (player.x, player.y)
            else:
                pink_target = return_target
            if not clyde.is_dead and not eaten_ghost[3]:
                clyd_target = (450, 450)
            elif not clyde.is_dead and eaten_ghost[3]:
                if 340 < clyde.x_pos < 560 and 340 < clyde.y_pos < 500:
                    clyd_target = (400, 100)
                else:
                    clyd_target = (player.x, player.y)
            else:
                clyd_target = return_target
        else:
            if not blinky.is_dead:
                if 340 < blinky.x_pos < 560 and 340 < blinky.y_pos < 500:
                    blink_target = (400, 100)
                else:
                    blink_target = (player.x, player.y)
            else:
                blink_target = return_target
            if not inky.is_dead:
                if 340 < inky.x_pos < 560 and 340 < inky.y_pos < 500:
                    ink_target = (400, 100)
                else:
                    ink_target = (player.x, player.y)
            else:
                ink_target = return_target
            if not pinky.is_dead:
                if 340 < pinky.x_pos < 560 and 340 < pinky.y_pos < 500:
                    pink_target = (400, 100)
                else:
                    pink_target = (player.x, player.y)
            else:
                pink_target = return_target
            if not clyde.is_dead:
                if 340 < clyde.x_pos < 560 and 340 < clyde.y_pos < 500:
                    clyd_target = (400, 100)
                else:
                    clyd_target = (player.x, player.y)
            else:
                clyd_target = return_target
        return [blink_target, ink_target, pink_target, clyd_target]

    def draw_misc(self, screen, score, powerup, lives, game_over, game_won):
        score_text = self.font.render(f'Score: {score}', True, 'white')
        screen.blit(score_text, (10, 920))
        if powerup:
            pygame.draw.circle(screen, 'blue', (140, 930), 15)
        for i in range(lives):
            screen.blit(pygame.transform.scale(self.player_images[0], (30, 30)), (650 + i * 40, 915))
        if game_over:
            pygame.draw.rect(screen, 'white', [50, 200, 800, 300],0, 10)
            pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
            gameover_text = self.font.render('Game over! Space bar to restart!', True, 'red')
            screen.blit(gameover_text, (100, 300))
        if game_won:
            pygame.draw.rect(screen, 'white', [50, 200, 800, 300],0, 10)
            pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
            gameover_text = self.font.render('Victory! Space bar to next level!', True, 'green')
            screen.blit(gameover_text, (100, 300))

    def check_collisions(self, scor, power, power_count, eaten_ghosts, level, player_x, center_x, center_y):
        num1 = (HEIGHT - 50) // 32
        num2 = WIDTH // 30
        if 0 < player_x < 870:
            if level[center_y // num1][center_x // num2] == 1:
                level[center_y // num1][center_x // num2] = 0
                scor += 10
            if level[center_y // num1][center_x // num2] == 2:
                level[center_y // num1][center_x // num2] = 0
                scor += 50
                power = True
                power_count = 0
                eaten_ghosts = [False, False, False, False]
        return scor, power, power_count, eaten_ghosts
    
    def draw_board(self, screen, level, flicker):
        num1 = ((HEIGHT - 50) // 32)
        num2 = (WIDTH // 30)
        for i in range(len(level)):
            for j in range(len(level[i])):
                if level[i][j] == 1:
                    pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
                if level[i][j] == 2 and not flicker:
                    pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
                if level[i][j] == 3:
                    pygame.draw.line(screen, 'blue', (j * num2 + (0.5 * num2), i * num1),
                                     (j * num2 + (0.5 * num2), i * num1 + num1), 3)
                if level[i][j] == 4:
                    pygame.draw.line(screen, 'blue', (j * num2, i * num1 + (0.5 * num1)),
                                     (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
                if level[i][j] == 5:
                    pygame.draw.arc(screen, 'blue', [(j * num2 - (num2 * 0.4)) - 2, (i * num1 + (0.5 * num1)), num2, num1],
                                    0, math.pi / 2, 3)
                if level[i][j] == 6:
                    pygame.draw.arc(screen, 'blue',
                                    [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], math.pi / 2, math.pi, 3)
                if level[i][j] == 7:
                    pygame.draw.arc(screen, 'blue', [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], math.pi,
                                    3 * math.pi / 2, 3)
                if level[i][j] == 8:
                    pygame.draw.arc(screen, 'blue',
                                    [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * math.pi / 2,
                                    2 * math.pi, 3)
                if level[i][j] == 9:
                    pygame.draw.line(screen, 'white', (j * num2, i * num1 + (0.5 * num1)),
                                     (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
                    