#  tutorial 2 - spaceship movement

import pygame
import random

pygame.init()

win_width, win_height = 1200, 900
win = pygame.display.set_mode((win_width, win_height))
win_caption = pygame.display.set_caption("space shooter game")

running = True

clock = pygame.time.Clock()

FPS = 60


class SpaceShip(object):
    def __init__(self):
        self.image = pygame.image.load("images/space_ship.png").convert_alpha()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = win_width // 2 - self.width
        self.y = win_height - self.height - 50
        self.rotation_angle = 0
        self.right = False
        self.left = False
        self.vel = 8
        self.health = 10
        self.hit_box = (self.x, self.y, self.width, self.height)

    def rotate(self, right: bool, left: bool):
        if right and self.rotation_angle > -3:
            self.rotation_angle -= 1

        elif left and self.rotation_angle < 3:
            self.rotation_angle += 1

    def move(self):
        if self.right:
            if self.x < win_width - self.width - 20:  # the ten is just that the space ship does not touch the edge
                self.x += self.vel
                self.rotate(True, False)
            win.blit(pygame.transform.rotate(self.image, self.rotation_angle), (self.x, self.y))

        elif self.left:
            if self.x > 10:  # the ten is just that the space ship does not touch the edge, it is just fo looks
                self.x -= self.vel
                self.rotate(False, True)
            win.blit(pygame.transform.rotate(self.image, self.rotation_angle), (self.x, self.y))

        else:
            if self.rotation_angle != 0:
                if self.rotation_angle < 0:
                    self.rotation_angle += 1
                elif self.rotation_angle > 0:
                    self.rotation_angle -= 1

            elif self.rotation_angle == 0:
                self.y = win_height - self.height - 50

            win.blit(pygame.transform.rotate(self.image, self.rotation_angle), (self.x, self.y))

    def health_bar(self):
        pygame.draw.rect(win, (255, 0, 0), (self.x, self.y + self.height + 20, self.width, 10))
        pygame.draw.rect(win, (0, 255, 0), (self.x, self.y + self.height + 20, self.width / 10 * self.health, 10))


class Missile(object):
    def __init__(self):
        self.image = pygame.image.load("images/missile.png").convert_alpha( )
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = space_ship.x + space_ship.width // 2
        self.y = space_ship.y
        self.vel = 5

    def move(self):
        win.blit(self.image, (self.x, self.y))

        self.y -= self.vel


class Meteor(object):
    def __init__(self):
        self.image = pygame.image.load("images/meteor.png").convert_alpha()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = random.randint(self.width, win_width - self.width)
        self.y = 0 - self.height
        self.hit_box = (self.x, self.y, self.width, self.height)
        self.vel = 7

    def move(self):
        win.blit(self.image, (self.x, self.y))

        self.y += self.vel


space_ship = SpaceShip()

bullets = []
bullet_count = 13

meteors = []
meteor_count = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if space_ship.health != 0:
        meteor_count += 1

        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            space_ship.right = True
            space_ship.left = False

        elif keys[pygame.K_a]:
            space_ship.right = False
            space_ship.left = True

        else:
            space_ship.right = False
            space_ship.left = False

        if keys[pygame.K_SPACE] and bullet_count == 13:
            bullets.append(Missile())
            bullet_count = 0

        win.fill((5, 0, 30))  # space color

        space_ship.move()
        space_ship.health_bar()

        # bullets
        for bullet in bullets:
            if bullet.y > 0 - bullet.height:
                bullet.move()
            else:
                bullets.remove(bullet)

        if bullet_count != 13:
            bullet_count += 1

        if meteor_count == 0:
            meteors.append(Meteor())

        for meteor in meteors:
            if meteor.y > meteor.y - meteor.height:
                meteor.move()
            else:
                meteors.remove(meteor)

        if meteor_count == 80:
            meteor_count = -1

        pygame.display.update()
        clock.tick(FPS)

pygame.quit()
quit()

