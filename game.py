#  tutorial 2 - spaceship movement

import pygame

pygame.init()

win_width, win_height = 1200, 900
win = pygame.display.set_mode((win_width, win_height))
win_caption = pygame.display.set_caption("space shooter game")

running = True

clock = pygame.time.Clock()

FPS = 30


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
        self.vel = 10
        self.health = 10
        self.hitbox = (self.x, self.y, self.width, self.height)

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

    def healt_bar(self):
        pygame.draw.rect(win, (255, 0, 0), (self.x, self.y + self.height + 20, self.width, 10))
        pygame.draw.rect(win, (0, 255, 0), (self.x, self.y + self.height + 20, self.width / 10 * self.health, 10))


class Missile(object):
    def __init__(self):
        self.image = pygame.image.load("images/missile.png")
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = space_ship.x + space_ship.width // 2
        self.y = space_ship.y
        self.vel = 10

    def move(self):
        win.blit(self.image, (self.x, self.y))

        self.y -= self.vel


space_ship = SpaceShip()
bullets = []
bullet_count = 15

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if space_ship.health != 0:
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

        if keys[pygame.K_SPACE] and bullet_count == 15:
            bullets.append(Missile())
            bullet_count = 0

        win.fill((5, 0, 30))  # space color
        space_ship.move()
        space_ship.healt_bar()

        for bullet in bullets:
            if bullet.y > 0 - bullet.height:
                bullet.move()
            else:
                bullets.pop(0)

        if bullet_count != 15:
            bullet_count += 1

        pygame.display.update()
        clock.tick(FPS)

pygame.quit()
quit()

