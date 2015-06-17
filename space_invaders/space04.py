import pygame
import os
from pygame.locals import *


# Special code to center window
os.environ['SDL_VIDEO_CENTERED'] = '1'


class Enemy(object):
    def __init__(self, pos):
        self.size = self.size_w, self.size_h = (20, 20)
        self.color = (255, 255, 255)
        self.speed = 1
        self.pos = pos
        self.direction_table = {
            "RIGHT": ("DOWN",   1),
            "DOWN":  ("LEFT",  60),
            "LEFT":  ("RIGHT", 60),
        }
        self.direction = 'RIGHT'
        self.ticks = 60

    def draw(self, screen):
        rect = pygame.Rect(self.pos, self.size)
        pygame.draw.rect(screen, self.color, rect)

    def update(self, world):
        if self.ticks == 0:
            self.direction, self.ticks = self.direction_table[self.direction]
        x, y = self.pos
        if self.direction == 'RIGHT':
            x += self.speed
        elif self.direction == 'LEFT':
            x -= self.speed
        elif self.direction == 'DOWN':
            y += self.speed
        self.pos = x, y
        self.ticks -= 1


class Player(object):
    def __init__(self):
        self.size = self.size_w, self.size_h = (20, 20)
        self.pos = ((World.WIDTH / 2) - (self.size_h / 2), World.HEGIHT - self.size_h)
        self.color = (255, 255, 255)
        self.speed = 10

    def draw(self, screen):
        rect = pygame.Rect(self.pos, self.size)
        pygame.draw.rect(screen, self.color, rect)

    def update(self, world):
        keys = pygame.key.get_pressed()
        x, y = self.pos
        if keys[K_LEFT]:
            x -= self.speed
        if keys[K_RIGHT]:
            x += self.speed
        if x < 0:
            x = 0
        elif x > (world.WIDTH - self.size_w):
            x = (world.WIDTH - self.size_w)
        self.pos = (x, y)


class World(object):
    FRAMES_PER_SECOND = 30
    RESOLUTION = WIDTH, HEGIHT = 800, 600
    WINDOWS_TITLE = 'Space Invaders v1.0 by raz'
    done = False

    def __init__(self):
        pygame.init()
        enemy_list = [Enemy((100 + 100*i, 100 + 50*j)) for i in range(6) for j in range(4)]
        self.objects = [Player()] + enemy_list
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
        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE] or keys[K_q]:
            self.done = True
            return
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
