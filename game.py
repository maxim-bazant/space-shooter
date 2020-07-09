#  tutorial 2 - spaceship movement

import pygame

pygame.init()

win_width, win_height = 1000, 900
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
        self.x = 20
        self.y = win_height - self.height - 50
        self.rotation_angle = 0

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.x += 5
            win.blit(self.image, (self.x, self.y))

        elif keys[pygame.K_a]:
            self.x -= 5
            win.blit(self.image, (self.x, self.y))

        else:
            win.blit(self.image, (self.x, self.y))


space_ship = SpaceShip()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    win.fill((0, 0, 0))
    space_ship.move()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
quit()

