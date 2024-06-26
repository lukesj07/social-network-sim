import pygame
import sys
import random
import math

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
pygame.init()
display = pygame.display
surface = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
display.set_caption("Social Network Sim")

def main() -> None:
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if keys[pygame.K_q]:
            run = False

        surface.fill(BLACK)

        pygame.draw.arc(surface, WHITE, (200, 200, 100, 20), 0, math.pi, 1)
        pygame.draw.rect(surface, WHITE, (200, 200, 100, 20), 1)

        #pygame.draw.circle(surface, WHITE, (200, 215), 2)
        #pygame.draw.circle(surface, WHITE, (300, 215), 2)

        
        display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
