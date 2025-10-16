import pygame
from game.game_engine import GameEngine

# Initialize pygame/Start application
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Game loop
engine = GameEngine(WIDTH, HEIGHT)

def main():
    running = True
    while running:
        SCREEN.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not engine.game_over:
            engine.handle_input()
            engine.update()
            engine.render(SCREEN)
        else:
            SCREEN.fill(BLACK)  # Clear the screen before showing game over
            winner = "Player Wins!" if engine.player_score == engine.target_score else "AI Wins!"
            engine.show_game_over(winner, SCREEN)
            pygame.display.flip()
            pygame.time.delay(1500)
            engine.replay_menu(SCREEN)
            # After replay_menu, game is reset, so continue

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()

