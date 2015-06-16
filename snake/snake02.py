import pygame
import os

# Special code to center window
os.environ['SDL_VIDEO_CENTERED'] = '1'


class Snake(object):
    def __init__(self):
        self.snake = [(World.GRID_W/2-1, World.GRID_H/2), (World.GRID_W/2, World.GRID_H/2)]

    def draw(self, screen):
        block_size = World.BLOCK_SIZE
        block_color = World.WHITE
        for x, y in self.snake:
            block_pos = (x * World.BLOCK_W, y * World.BLOCK_H)
            rect = pygame.Rect(block_pos, block_size)
            pygame.draw.rect(screen, block_color, rect)


class World(object):
    FRAMES_PER_SECOND = 30
    RESOLUTION = WIDTH, HEGIHT = 800, 600
    GRID_SIZE = GRID_W, GRID_H = (40, 40)
    BLOCK_SIZE = BLOCK_W, BLOCK_H = (WIDTH / GRID_W, HEGIHT / GRID_H)
    WINDOWS_TITLE = 'Snake v1.0 by raz'
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    def __init__(self):
        self.player = Snake()

    def draw(self, screen):
        screen.fill(self.BLACK)
        self.player.draw(screen)
        pygame.display.flip()


def main():
    # Initial Setup
    pygame.init()
    screen_surface = pygame.display.set_mode(World.RESOLUTION)
    pygame.display.set_caption(World.WINDOWS_TITLE)

    world = World()
    done = False
    clock = pygame.time.Clock()
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        world.draw(screen_surface)
        # Delays until next frame
        clock.tick(World.FRAMES_PER_SECOND)
    pygame.quit()

main()