import pygame
import os

# Special code to center window
os.environ['SDL_VIDEO_CENTERED'] = '1'


class Player(object):
    def __init__(self):
        self.size = self.size_w, self.size_h = (20, 20)
        self.pos = ((World.WIDTH / 2) - (self.size_h / 2), World.HEGIHT - self.size_h)
        self.color = (255, 255, 255)

    def draw(self, screen):
        rect = pygame.Rect(self.pos, self.size)
        pygame.draw.rect(screen, self.color, rect)

    def update(self, world):
        pass


class World(object):
    FRAMES_PER_SECOND = 30
    RESOLUTION = WIDTH, HEGIHT = 800, 600
    WINDOWS_TITLE = 'Space Invaders v1.0 by raz'
    done = False

    def __init__(self):
        pygame.init()
        self.objects = [Player()]
        self.screen = None
        self.clock = None

    def start(self):
        self.screen = pygame.display.set_mode(self.RESOLUTION)
        pygame.display.set_caption(self.WINDOWS_TITLE)
        self.clock = pygame.time.Clock()

    def draw(self):
        self.screen.fill((0, 0, 0))
        for obj in self.objects:
            obj.draw(self.screen)
        pygame.display.flip()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
                return
        for obj in self.objects:
            obj.update(self)

    def wait(self):
        self.clock.tick(self.FRAMES_PER_SECOND)


def main():
    world = World()

    world.start()
    while not world.done:
        world.update()
        world.draw()
        world.wait()

main()
