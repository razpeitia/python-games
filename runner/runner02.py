import pygame
import os
from pygame.locals import *

# Special code to center window
os.environ['SDL_VIDEO_CENTERED'] = '1'


class Player(object):
    def __init__(self):
        self.size = self.size_w, self.size_h = (20, 20)
        self.pos = ((World.WIDTH / 2) - (self.size_h / 2), World.HEGIHT - self.size_h)
        self.color = (255, 255, 255)
        self.speed = 5
        self.jumping_state = 'STANDING'
        self.jumping_ticks = 0
        self.speed_jump = 15

    def draw(self, screen):
        rect = pygame.Rect(self.pos, self.size)
        pygame.draw.rect(screen, self.color, rect)

    def update(self, world):
        keys = pygame.key.get_pressed()
        x, y = self.pos

        if keys[K_LEFT]:
            x -= self.speed
        elif keys[K_RIGHT]:
            x += self.speed
        if x < 0:
            x = 0
        elif x > (world.WIDTH - self.size_w):
            x = (world.WIDTH - self.size_w)

        if keys[K_UP] and self.jumping_state == 'STANDING':
            self.jumping_state = 'JUMPING'
            self.jumping_ticks = 0
        elif self.jumping_state == 'JUMPING':
            vy = self.speed_jump - world.GRAVITY * self.jumping_ticks
            y -= vy
            if y > (world.HEGIHT - self.size_h):
                y = world.HEGIHT - self.size_h
                self.jumping_state = 'STANDING'
            self.jumping_ticks += 1
        self.pos = (x, y)


class World(object):
    FRAMES_PER_SECOND = 30
    RESOLUTION = WIDTH, HEGIHT = 800, 600
    WINDOWS_TITLE = 'Runner v1.0 by raz'
    done = False
    GRAVITY = 1

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
        keys = pygame.key.get_pressed()
        if keys[K_q] or keys[K_ESCAPE]:
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
