import random
import sys
import pygame

pygame.init()

is_die = False


def draw_text(text, x, y):
    text_surf = test_font.render(f"{text}", True, (255, 255, 255))
    screen.blit(text_surf, (x, y))


def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = screen_height / 2
    score = 0
    return score


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            'flappy-bird-assets/sprites/pipe-green.png').convert_alpha()
        self.rect = self.image.get_rect()
        if pos == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - 120 / 2]
        elif pos == -1:
            self.rect.topleft = [x, y + 120 / 2]

    def update(self):
        self.rect.x -= 2
        if (self.rect.right < -20):
            self.kill()


class Bird(pygame.sprite.Sprite):
    global is_die

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.images = []
        self.sounds = ['die', 'wing', 'swoosh', 'hit']
        self.index = 0
        self.counter = 0
        for image in ['yellowbird-upflap', 'yellowbird-downflap', 'yellowbird-downflap']:
            img = pygame.image.load(
                f'flappy-bird-assets/sprites/{image}.png').convert_alpha()
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

        self.velacity = pygame.Vector2()
        self.velacity.xy = 0, 0
        self.acceleration = 0.53

        self.wing_sound = pygame.mixer.Sound(
            'flappy-bird-assets/audio/wing.ogg')
        self.wing_sound.set_volume(0.3)

        self.die_sound = pygame.mixer.Sound(
            f'flappy-bird-assets/audio/die.ogg')
        self.die_sound.set_volume(1)

        self.hit_sound = pygame.mixer.Sound(
            f'flappy-bird-assets/audio/hit.ogg')
        self.hit_sound.set_volume(1)

        self.is_die = True
        self.is_jump = False
        self.coldown = 20

    def update(self):

        if game_over == True:
            if self.rect.bottom <= screen_height-10:
                self.velacity.y = 7
                self.velacity.y += self.acceleration
                self.rect.y += self.velacity.y
        if is_flying:
            self.velacity.y += self.acceleration
            if keys[pygame.K_SPACE] and self.is_jump == False:
                self.velacity.y = -7
                self.wing_sound.play()
                self.is_jump = True
                print(self.rect.y)

            if self.counter <= 0:
                self.is_jump = False
                self.coldown = 10

            if self.rect.y <= 0:
                self.velacity.y = 7

            self.rect.y += self.velacity.y
            self.coldown -= 0.5

        if game_over and self.is_die:
            self.die_sound.play()
            self.hit_sound.play()
            self.is_die = False
        if game_over == False and self.is_die == False:
            self.is_die = True

        #! handel the animation
        self.counter += 1
        flap_cooldown = 5
        if self.counter > flap_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0

        self.image = self.images[self.index]


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self):
        action = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


screen_width, screen_height = 600, 400

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

test_font = pygame.font.Font('flappy-bird-assets/font/Always Lovely.ttf', 50)
button_image = pygame.image.load('flappy-bird-assets/sprites/restart.png')

pygame_icon = pygame.image.load('flappy-bird-assets/favicon.ico')
pygame.display.set_icon(pygame_icon)

clock = pygame.time.Clock()

bird_group = pygame.sprite.Group()
flappy = Bird(100, int(screen_height/2))
bird_group.add(flappy)

pipe_group = pygame.sprite.Group()

button = Button(screen_width / 2, screen_height / 2, button_image)

pipe_fer = 1500
last_pipe = pygame.time.get_ticks()
print(last_pipe)


bg_image = pygame.image.load('flappy-bird-assets/sprites/background-night.png')

game_over = False
is_flying = False
pass_pipe = False
score = 0


while True:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if keys[pygame.K_SPACE] and game_over == False and is_flying == False:
            is_flying = True

    screen.fill((255, 255, 220))
    screen.blit(bg_image, (0, 0))
    screen.blit(bg_image, (288, 0))
    screen.blit(bg_image, (288 + 288, 0))

    pipe_group.draw(screen)

    bird_group.draw(screen)
    bird_group.update()

    draw_text(score, screen_width / 2, 50)

    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right and pass_pipe == False:
            pass_pipe = True
        if pass_pipe:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                point_sound = pygame.mixer.Sound(
                    'flappy-bird-assets/audio/point.ogg')
                point_sound.set_volume(1)
                point_sound.play()
                pass_pipe = False

    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.bottom >= screen_height - 10:
        game_over = True
        is_flying = False
        id_die = True

    if game_over:
        if button.draw():
            game_over = False
            score = reset_game()

    if game_over == False and is_flying:
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_fer:
            pipe_heigh = random.randint(-100, 100)
            top_pipe = Pipe(screen_width, int(screen_height/2) + pipe_heigh, 1)
            btm_pipe = Pipe(screen_width, int(
                screen_height/2) + pipe_heigh, -1)
            pipe_group.add(top_pipe)
            pipe_group.add(btm_pipe)
            last_pipe = time_now
        pipe_group.update()

    pygame.display.flip()
    clock.tick(60)
