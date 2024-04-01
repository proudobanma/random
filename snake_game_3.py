import pygame
import math
import sys
import random
import time

# constants
WIDTH = 640
HEIGHT = 640
PIXELS = 32
SQUARES = int(WIDTH // PIXELS)

# COLORS
BG1 = (156, 210, 54)
BG2 = (145, 203, 57)
RED = (255, 0, 0)
BLUE = (0, 0, 50)
BLACK = (0, 0, 0)

class Body:
    def __init__(self, color, posX, posY):
        self.color = color
        self.posX = posX
        self.posY = posY

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.posX, self.posY, PIXELS, PIXELS))

class Snake:
    def __init__(self):
        self.color = BLUE
        self.body_color = list(BLUE)
        self.headX = random.randrange(0, WIDTH, PIXELS)
        self.headY = random.randrange(0, HEIGHT, PIXELS)
        self.state = 'STOP'
        self.bodies = []

    def move(self):
        if self.state == 'UP':
            self.headY -= PIXELS
        elif self.state == 'DOWN':
            self.headY += PIXELS
        elif self.state == "RIGHT":
            self.headX += PIXELS
        elif self.state == 'LEFT':
            self.headX -= PIXELS

    def move_body(self):
        if len(self.bodies) > 0:
            for i in range(len(self.bodies) - 1, -1, -1):
                if i == 0:
                    self.bodies[0].posX = self.headX
                    self.bodies[0].posY = self.headY
                else:
                    self.bodies[i].posX = self.bodies[i - 1].posX
                    self.bodies[i].posY = self.bodies[i - 1].posY

    def add_body(self):
        self.body_color[2] += 1.5
        body = Body(tuple(self.body_color), self.headX, self.headY)
        self.bodies.append(body)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.headX, self.headY, PIXELS, PIXELS))
        for body in self.bodies:
            body.draw(surface)

    def die(self):
        self.headX = random.randrange(0, WIDTH, PIXELS)
        self.headY = random.randrange(0, HEIGHT, PIXELS)
        self.bodies = []
        self.body_color = list(BLUE)  # Resetting the body_color properly
        self.state = 'STOP'

class Apple:
    def __init__(self):
        self.color = RED
        self.spawn()

    def spawn(self):
        self.posX = random.randrange(0, WIDTH, PIXELS)
        self.posY = random.randrange(0, HEIGHT, PIXELS)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.posX, self.posY, PIXELS, PIXELS))

class Background:
    def draw(self, surface):
        surface.fill(BG1)
        counter = 0
        for row in range(SQUARES):
            for col in range(SQUARES):
                if counter % 2 == 0:
                    pygame.draw.rect(surface, BG2, (col * PIXELS, row * PIXELS, PIXELS, PIXELS))
                if col != SQUARES - 1:
                    counter += 1

class Collision:
    def between_snake_and_apple(self, snake, apple):
        distance = math.sqrt(math.pow((snake.headX - apple.posX), 2) + math.pow((snake.headY - apple.posY), 2))
        return distance < PIXELS

    def between_snake_and_walls(self, snake):
        if snake.headX < 0 or snake.headX > WIDTH - PIXELS or snake.headY < 0 or snake.headY > HEIGHT - PIXELS:
            return True
        return False
    
    def between_head_and_body(self, snake):
        for body in snake.bodies:
            distance = math.sqrt(math.pow((snake.headX - body.posX), 2) + math.pow((snake.headY - body.posY), 2))
            if distance < PIXELS:
                return True
        return False

class Score:

    def __init__(self):
        self.points = 0
        self.font = pygame.font.SysFont('monospace', 30, bold=True)
    
    def increase(self):
        self.points += 1
    
    def reset(self):
        self.points = 0

    def draw(self, surface):
        lbl = self.font.render("LOL, IMAGINE HAVING: " + str(self.points), 1, BLACK)
        surface.blit(lbl, ( 5, 5 ))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("snake")

    # object #class
    snake = Snake()
    apple = Apple()
    background = Background()
    collision = Collision()
    score = Score()

    # mainloop
    while True:
        background.draw(screen)
        snake.draw(screen)
        apple.draw(screen)
        score.draw( screen )
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP :
                    if snake.state != 'DOWN':
                        snake.state = 'UP'

                if event.key == pygame.K_DOWN:
                    if snake.state != 'UP':
                        snake.state = 'DOWN'

                if event.key == pygame.K_LEFT:
                    if snake.state != 'RIGHT':
                        snake.state = 'LEFT'

                if event.key == pygame.K_RIGHT:
                    if snake.state != 'LEFT':
                        snake.state = 'RIGHT'
                if event.key == pygame.K_p:
                    snake.state = 'STOP'

        if collision.between_snake_and_apple(snake, apple):
            apple.spawn()
            snake.add_body()
            score.increase()

        if snake.state != 'STOP':
            snake.move_body()
            snake.move()

        if collision.between_snake_and_walls(snake) or collision.between_head_and_body(snake):
            snake.die()
            apple.spawn()
            score.reset()

        pygame.display.update()
        pygame.time.delay(125)

main()