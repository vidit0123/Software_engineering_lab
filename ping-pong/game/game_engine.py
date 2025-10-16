import pygame
from .paddle import Paddle
from .ball import Ball
import sys

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.target_score = 5  # Default, can be changed in replay_menu
        self.game_over = False

        self.font = pygame.font.SysFont("Arial", 30)

        pygame.mixer.init()
        self.sound_paddle = pygame.mixer.Sound("paddle_hit.mp3")
        self.sound_score = pygame.mixer.Sound("score.mp3")
        self.sound_wall = pygame.mixer.Sound("bounce.mp3")

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        self.ball.move()
        self.ball.check_collision(self.player, self.ai)

        # Score logic
        if self.ball.x <= 0:
            self.ai_score += 1
            self.sound_score.play()
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.sound_score.play()
            self.ball.reset()

        self.ai.auto_track(self.ball, self.height)

        # Game over check
        if self.player_score == self.target_score or self.ai_score == self.target_score:
            self.game_over = True

    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))

    def reset_game(self):
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()
        self.game_over = False

    def show_game_over(self, winner):
        font = pygame.font.Font(None, 72)
        text = font.render(winner, True, WHITE)
        rect = text.get_rect(center=(self.width // 2, self.height // 2))
        # You must pass the screen to this function or store it as self.screen
        pygame.display.get_surface().blit(text, rect)

    def replay_menu(self, screen):
        font = pygame.font.Font(None, 48)
        options = [
            "Press 3 for Best of 3",
            "Press 5 for Best of 5",
            "Press 7 for Best of 7",
            "Press ESC to Exit"
        ]
        waiting = True
        while waiting:
            screen.fill((0, 0, 0))
            for i, opt in enumerate(options):
                text = font.render(opt, True, WHITE)
                screen.blit(text, (200, 200 + i * 60))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key in [pygame.K_3, pygame.K_5, pygame.K_7]:
                        self.target_score = int(event.unicode)
                        self.reset_game()
                        waiting = False
