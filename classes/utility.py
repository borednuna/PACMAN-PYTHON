import pygame
import math
from board import boards

WIDTH = 900
HEIGHT = 950

class Utility:
    def __init__(self):
        self.player_images = []
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        for i in range(1, 5):
            self.player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (45, 45)))

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
            gameover_text = self.font.render('Victory! Space bar to restart!', True, 'green')
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
                    