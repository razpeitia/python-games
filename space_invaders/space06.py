import pygame
import os
from pygame.locals import *
import random


# Special code to center window
os.environ['SDL_VIDEO_CENTERED'] = '1'


class Bullet(object):
    def __init__(self, pos, direction):
        self.size = self.size_w, self.size_h = (4, 10)
        self.pos = pos
        self.speed = 10
        self.direction = direction
        self.color = (255, 0, 0)
        self.is_dead = False

    def draw(self, screen):
        rect = pygame.Rect(self.pos, self.size)
        pygame.draw.rect(screen, self.color, rect)

    def update(self, world):
        x, y = self.pos
        if self.direction == 'UP':
            y -= self.speed
        elif self.direction == 'DOWN':
            y += self.speed
        self.pos = (x, y)
        if y < 0:
            self.is_dead = True
        elif y > (world.HEGIHT + self.size_h):
            self.is_dead = True

    def collide(self, obj):
        own_rect = pygame.Rect(self.pos, self.size)
        obj_rect = pygame.Rect(obj.pos, obj.size)
        return own_rect.colliderect(obj_rect)


class Enemy(object):
    def __init__(self, pos):
        self.size = self.size_w, self.size_h = (20, 20)
        self.color = (255, 255, 255)
        self.speed = 1
        self.pos = pos
        self.direction_table = {
            "RIGHT": ("DOWN",   5),
            "DOWN":  ("LEFT",  60),
            "LEFT":  ("RIGHT", 60),
        }
        self.direction = 'RIGHT'
        self.ticks = 60
        self.is_dead = False
        self.bullet_ticks = random.randrange(100, 200)

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

        if self.bullet_ticks == 0:
            self.bullet_ticks = random.randrange(100, 200)
            x, y = self.pos
            y += self.size_h + 1
            bullet = Bullet((x, y), 'DOWN')
            world.objects.append(bullet)
        self.bullet_ticks -= 1

        for obj in world.objects:
            if isinstance(obj, Bullet) and (not obj.is_dead) and obj.collide(self) and obj.direction == 'UP':
                self.is_dead = True
                obj.is_dead = True


class Player(object):
    def __init__(self):
        self.size = self.size_w, self.size_h = (20, 20)
        self.pos = ((World.WIDTH / 2) - (self.size_h / 2), World.HEGIHT - self.size_h)
        self.color = (255, 255, 255)
        self.speed = 10
        self.is_dead = False
        self.bullet_ticks = 10
        self.bullet_tick_counter = 0
        self.can_shoot = False

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

        if keys[K_SPACE] and self.can_shoot:
            self.can_shoot = False
            bullet = Bullet((x, y+1), 'UP')
            world.objects.append(bullet)
        if self.bullet_tick_counter == self.bullet_ticks:
            self.bullet_tick_counter = 0
            self.can_shoot = True
        self.bullet_tick_counter += 1

        for obj in world.objects:
            if isinstance(obj, Bullet) and (not obj.is_dead) and obj.collide(self) and obj.direction == 'DOWN':
                self.is_dead = True
                obj.is_dead = True


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
        live_object = []
        for obj in self.objects:
            obj.update(self)
            if not obj.is_dead:
                live_object.append(obj)
        self.objects = live_object

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
