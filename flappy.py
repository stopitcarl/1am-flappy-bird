import pygame
import pygame.freetype
import random
import hashlib

WIDTH = 900
HEIGHT = 600

GRAVITY = 0.5
BIRD_INIT_X = WIDTH / 3 - 50
BIRD_INIT_Y = HEIGHT / 2
JUMP_VELOCITY = -9
MAX_VELOCITY = 30
PIPE_GAP = 170
SPACE_BETWEEN_PIPES = 300
PIPE_VEL = 3


pygame.init()
GAME_FONT = pygame.freetype.SysFont("Comic Sans MS", 40)
POINTS_FONT = pygame.freetype.SysFont("Comic Sans MS", 20)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flappy bird')
clock = pygame.time.Clock()

crashed = False
best_score = 0

black = (0, 0, 0)
white = (255, 255, 255)
orange = (255, 165, 0)
red = (255, 0, 0)
green = (0, 255, 0)


class Pipe:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 80
        self.alive = True
        self.color = green

    def draw(self):
        # Top pipe
        pygame.draw.rect(screen, green,
                         (self.x, 0,
                          self.width, self.y))
        # Bottom pipe
        pygame.draw.rect(screen, green,
                         (self.x, self.y + PIPE_GAP,
                          self.width, HEIGHT - (self.y + PIPE_GAP)))

    def step(self):
        self.x -= PIPE_VEL

    def to_delete(self):
        if self.x + self.width < 0:
            self.color = black
            return True
        return False

    # Detect collision with bird

    def collide(self, bird):
        if (bird.x + bird.width > self.x and
                bird.x < self.x + self.width):
            if (bird.y + bird.height > self.y + PIPE_GAP or
                    bird.y < self.y):
                return True
        return False


class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel_y = 0
        self.width = 40
        self.height = 40
        self.alive = True
        self.zombie = True
        self.points = 0
        self.color = orange

    def step(self):

        if self.zombie and self.y > BIRD_INIT_Y + 60:
            self.vel_y = JUMP_VELOCITY

        self.y += self.vel_y
        self.vel_y += GRAVITY

        if self.alive and self.y > (HEIGHT - self.height):
            self.y = HEIGHT - self.height
            self.vel_y = JUMP_VELOCITY * 1.4
            self.die()

        pygame.draw.rect(screen, self.color,
                         (self.x, self.y, self.width, self.height))

        return self.y > HEIGHT

    def die(self):
        self.alive = False
        self.color = red

    def jump(self):
        self.zombie = False
        self.vel_y = JUMP_VELOCITY


bird = None
pipes = None
move_pipes = True


def reset_game():
    global bird, pipes, move_pipes
    bird = Bird(BIRD_INIT_X, BIRD_INIT_Y)
    pipes = [Pipe(WIDTH + i * (SPACE_BETWEEN_PIPES), random.randint(20,
                                                                    HEIGHT - PIPE_GAP - 20)) for i in range(5)]
    move_pipes = True


reset_game()
move_pipes = True

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        # print(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if bird.alive:
                    bird.jump()
                else:
                    reset_game()

    screen.fill((255, 255, 255))

    if not bird.zombie:
        for i, pipe in enumerate(pipes):
            if move_pipes:
                pipe.step()
            pipe.draw()

            if pipe.collide(bird):
                bird.die()
                move_pipes = False
                continue

            elif pipe.x + pipe.width / 2 < bird.x and bird.alive and pipe.alive:
                bird.points += 1
                if bird.points > best_score:
                    best_score = bird.points
                pipe.alive = False

            elif not pipe.alive:
                pipes.append(Pipe(
                    pipes[-1].x + SPACE_BETWEEN_PIPES,
                    random.randint(20, HEIGHT - PIPE_GAP - 20)))

    pipes = [pipe for pipe in pipes if not pipe.to_delete()]

    if not bird.step():
        # crashed = True
        pass

    if bird.zombie:
        GAME_FONT.render_to(screen, (WIDTH / 3, 200),
                            "Flapppy Bird", black)

    if not bird.alive:
        GAME_FONT.render_to(screen, (WIDTH / 3, 200),
                            f"This run: {bird.points}", black)
        GAME_FONT.render_to(screen, (WIDTH / 3, 250),
                            f"Best: {best_score}", black)        
        POINTS_FONT.render_to(screen, (WIDTH / 3, 300),
                              f"Press space to restart", black)
        code = hashlib.md5(bytes(best_score))
        POINTS_FONT.render_to(screen, (WIDTH / 4, HEIGHT-100),
                              f"code that proves your best score: {code.hexdigest()[:6]}", black)
    else:
        POINTS_FONT.render_to(screen, (10, 10),
                              f"Score: {bird.points}", black)
        POINTS_FONT.render_to(screen, (WIDTH - 120, 10),
                              f"Best: {best_score}", black)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
