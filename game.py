#  tutorial 7 - sound effects + pixel perfect collision

import pygame
import random
import time

pygame.init()
pygame.font.init()
pygame.mixer.pre_init(44100, 16, 2, 4096)


font_size = 60
my_font = pygame.font.SysFont("Comic Sans", font_size)

win_width, win_height = 1000, 1000
win = pygame.display.set_mode((win_width, win_height))
win_caption = pygame.display.set_caption("space shooter game")

running = True

clock = pygame.time.Clock()

FPS = 60

score = 0

lost_start_new_game = False
start_new_game = True
all_explosions_done = False
space_ship_explosion = False

# sounds
explosion_sound = pygame.mixer.Sound("music/explosion1.wav")
space_ship_explosion_sound = pygame.mixer.Sound("music/explosion.wav")
space_ship_explosion_sound.set_volume(1)
explosion_sound.set_volume(0.3)
laser_shoot = pygame.mixer.Sound("music/laser_shoot.wav")
laser_shoot.set_volume(0.2)


class SpaceShip(object):
    def __init__(self):
        self.image = pygame.image.load("images/space_ship.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = win_width // 2 - self.width + 70  # 70 is for the space ship to be perfectly in middle
        self.space_between_the_Earth = 250  # 200 is so there is space between the Earth and the space ship
        self.y = win_height - self.height - self.space_between_the_Earth
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

    def show_me(self):
        win.blit(pygame.transform.rotate(self.image, self.rotation_angle), (self.x, self.y))

    def move(self):
        if self.right:
            if self.x < win_width - self.width - 20:  # the ten is just that the space ship does not touch the edge
                self.x += self.vel
                self.rotate(True, False)
            self.show_me()

        elif self.left:
            if self.x > 10:  # the ten is just that the space ship does not touch the edge, it is just fo looks
                self.x -= self.vel
                self.rotate(False, True)
            self.show_me()

        else:
            if self.rotation_angle != 0:
                if self.rotation_angle < 0:
                    self.rotation_angle += 1
                elif self.rotation_angle > 0:
                    self.rotation_angle -= 1

            elif self.rotation_angle == 0:
                self.y = win_height - self.height - self.space_between_the_Earth

            self.show_me()

    def health_bar(self):
        pygame.draw.rect(win, (255, 0, 0), (self.x, self.y + self.height + 20, self.width, 10))
        pygame.draw.rect(win, (0, 255, 0), (self.x, self.y + self.height + 20, self.width / 10 * self.health, 10))


class Missile(object):
    def __init__(self):
        self.image = pygame.image.load("images/missile.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = space_ship.x + space_ship.width // 2
        self.y = space_ship.y
        self.vel = 8
        self.hit_box = (self.x, self.y, self.width, self.height)

    def move(self):
        win.blit(self.image, (self.x, self.y))

        self.y -= self.vel


class Meteor(object):
    def __init__(self):
        self.image = pygame.image.load("images/meteor.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = random.randint(50 + self.width, win_width - self.width - 50)  # 50 are to keep meteor from edges
        self.y = 0 - self.height
        self.hit_box = (self.x, self.y, self.width, self.height)
        self.vel = 9

    def show_me(self):
        win.blit(self.image, (self.x, self.y))

    def move(self):
        self.show_me()

        self.y += self.vel


class Explosion(object):
    def __init__(self, x, y, explode_, zoom=False):
        self.x = x
        self.y = y
        self.images = list()
        self.explode_count = 0
        self.explode_ = explode_
        self.zoom = zoom

        if not zoom:
            for i in ["01", "02", "03", "04"]:
                self.images.append(pygame.image.load(f"images/explosion{i}.png").convert_alpha())
        else:
            for i in ["01", "02", "03", "04"]:
                self.images.append(pygame.transform.scale2x(
                     pygame.image.load(f"images/explosion{i}.png").convert_alpha()))

        self.images.extend([self.images[-1] for _ in range(2)])  # for longer explosion

    def explode(self):
        if self.explode_:
            if self.explode_count + 1 < 3 * len(self.images):
                self.explode_count += 1
            else:
                self.explode_count = 0
                self.explode_ = False

            win.blit(self.images[self.explode_count // 3], (self.x, self.y))


class Earth(object):
    def __init__(self):
        self.image = pygame.image.load("images/earth.png").convert_alpha()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = 0 - (self.width - win_width) // 2
        self.y = (win_height - self.height) + self.height // 7
        self.shake_count = 0
        self.shake_ = False

    def shake(self):
        if self.shake_:
            if self.shake_count < 6:
                if self.shake_count % 2 == 0:
                    self.x -= 7.5
                    self.y -= 7.5
                elif self.shake_count % 2 == 1:
                    self.x += 7.5
                    self.y += 7.5

                self.shake_count += 1
            else:
                self.shake_count = 0
                self.shake_ = False

    def show_me(self):
        win.blit(self.image, (self.x, self.y))


class Button(object):
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.interaction_image = pygame.image.load("button/start_button_brighter.png").convert_alpha()
        self.width = image.get_width()
        self.height = image.get_height()

    def show_me(self):
        win.blit(self.image, (self.x, self.y))

    def is_clicked(self):
        if (self.x < int(pygame.mouse.get_pos()[0]) < self.x + self.width
                and self.y < int(pygame.mouse.get_pos()[1]) < self.y + self.height):
            start_button_brighter.show_me()

            if pygame.mouse.get_pressed()[0]:
                return True

        else:
            start_button.show_me()


space_ship = SpaceShip()

explosions = []
explosions_sound = []

bullets = []
bullet_count = 20

meteors = []
meteor_count = 0

Earth = Earth()

game_over_button = Button(win_width // 2 - 180, win_height // 2 - 200,
                          pygame.image.load("button/game_over_button.png").convert_alpha())

start_button = Button(win_width // 2 - 230, win_height // 2 - 120,
                      pygame.image.load("button/start_button.png").convert_alpha())

start_button_brighter = Button(win_width // 2 - 230, win_height // 2 - 120,
                               pygame.image.load("button/start_button_brighter.png").convert_alpha())


def blit_some_things():
    win.fill((5, 0, 30))  # space color

    space_ship.move()
    space_ship.health_bar()

    Earth.show_me()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not (lost_start_new_game or start_new_game):
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

        if keys[pygame.K_SPACE] and bullet_count == 20:
            laser_shoot.play()
            bullets.append(Missile())
            bullet_count = 0

        win.fill((5, 0, 30))  # space color

        space_ship.move()
        space_ship.health_bar()

        Earth.show_me()
        Earth.shake()

        # bullets
        for bullet in bullets:
            if bullet.y > 0 - bullet.height:
                bullet.move()
            else:
                bullets.remove(bullet)

        if bullet_count != 20:
            bullet_count += 1

        if meteor_count == 0:
            meteors.append(Meteor())

        # meteors
        for meteor in meteors:
            if meteor.y < win_height + meteor.height:
                meteor.move()
            else:
                meteors.remove(meteor)

        if meteor_count == 80:
            meteor_count = -1

        if score == 5:
            FPS = 65

        if score == 15:
            FPS = 75

        # collision for meteor and spaceship
        for meteor in meteors:
            offset = (space_ship.x - meteor.x, space_ship.y - meteor.y)
            collision = meteor.mask.overlap(space_ship.mask, offset)
            if collision:
                space_ship.health -= 1
                explosions.append(Explosion(meteor.x, meteor.y + meteor.height // 2, True))
                explosions_sound.append(explosion_sound)
                meteors.remove(meteor)

        # collision for meteor and missile
        for meteor in meteors:
            for bullet in bullets:
                offset = (bullet.x - meteor.x, bullet.y - meteor.y)
                collision = meteor.mask.overlap(bullet.mask, offset)
                if collision:
                    score += 1
                    explosions.append(Explosion(meteor.x, meteor.y + meteor.height // 2, True))
                    explosions_sound.append(explosion_sound)
                    meteors.remove(meteor)
                    bullets.remove(bullet)

        # collision with Earth
        for meteor in meteors:
            if meteor.y > win_height - meteor.height - 40:
                meteors.remove(meteor)
                explosions.append(Explosion(meteor.x, meteor.y + meteor.height // 2, True))
                explosions_sound.append(explosion_sound)
                score -= 2
                Earth.shake_ = True

        for explosion in explosions:
            explosion.explode()

            if not explosion.explode_:
                explosions.remove(explosion)

        for explosion_sound_ in explosions_sound:
            explosion_sound.play()
            explosions_sound.remove(explosion_sound_)

        score_text = my_font.render(f"Your score: {score}", False, (255, 255, 255))
        win.blit(score_text, (20, 20))

        pygame.display.update()
        clock.tick(FPS)

        if space_ship.health == 0 or score < -5:
            lost_start_new_game = True

    elif space_ship.health == 0:
        explosion_x = space_ship.x
        explosion_y = space_ship.y
        explosion_of_space_ship = Explosion(explosion_x, explosion_y, True, True)
        space_ship_explosion_sound.play()

        meteors = []
        bullets = []
        explosions = []
        win.fill((5, 0, 30))  # space color
        Earth.show_me()
        score_text = my_font.render(f"Your score was: {score}", False, (255, 255, 255))
        win.blit(score_text, (20, 20))

        pygame.display.update()
        clock.tick(FPS)

        while explosion_of_space_ship.explode_:
            explosion_of_space_ship.explode()
            space_ship_explosion = True
            pygame.display.update()
            clock.tick(FPS)

        lost_start_new_game = True
        space_ship.health = 10

    elif lost_start_new_game and not space_ship.health == 0:
        if not space_ship_explosion:
            while not all_explosions_done:
                win.fill((5, 0, 30))
                Earth.show_me()
                space_ship.show_me()
                space_ship.health_bar()
                try:
                    meteors[0].show_me()
                except IndexError:
                    pass
                score_text = my_font.render(f"Your score was: {score}", False, (255, 255, 255))
                win.blit(score_text, (20, 20))
                for explosion in explosions:
                    explosion.explode()

                    if not explosion.explode_:
                        all_explosions_done = True
                    pygame.display.update()
                    clock.tick(60)

        space_ship.rotation_angle = 0
        space_ship.x = win_width // 2 - space_ship.width + 70  # 70 is for the space ship to be perfectly in middle
        meteors = []
        bullets = []
        explosions = []
        FPS = 60
        blit_some_things()
        game_over_button.show_me()
        pygame.display.update()
        clock.tick(FPS)
        time.sleep(2)
        lost_start_new_game = False
        start_new_game = True
        Earth.shake_count = 0
        Earth.shake_ = False
        time.sleep(1)

    elif start_new_game:
        win.fill((5, 0, 30))  # space color
        if not start_button.is_clicked():
            Earth.show_me()
            win.blit(space_ship.image, (space_ship.x, space_ship.y))
            pygame.display.update()
            clock.tick(FPS)
        else:
            start_new_game = False
            space_ship_explosion = False
            space_ship.x = win_width // 2 - space_ship.width + 70  # 70 is for the space ship to be perfectly in middle
            score = 0
            pygame.display.update()
            clock.tick(FPS)


pygame.quit()
quit()
