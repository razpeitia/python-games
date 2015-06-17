import pygame
import os

# Special code to center window
os.environ['SDL_VIDEO_CENTERED'] = '1'


def main():
    # Settings
    FRAMES_PER_SECOND = 30
    RESOLUTION = WIDTH, HEGIHT = 800, 600
    WINDOWS_TITLE = 'Space Invaders v1.0 by raz'

    # Initial Setup
    pygame.init()
    screen_surface = pygame.display.set_mode(RESOLUTION)
    pygame.display.set_caption(WINDOWS_TITLE)

    done = False
    clock = pygame.time.Clock()
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # Delays until next frame
        clock.tick(FRAMES_PER_SECOND)
    pygame.quit()

main()
