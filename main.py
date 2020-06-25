import random
import pygame

FPS = 60
X = 600
Y = 400
pygame.init()
surface = pygame.display.set_mode((X, Y))
clock = pygame.time.Clock()


pygame.time.set_timer(pygame.USEREVENT, 2000)
pygame.time.set_timer(pygame.USEREVENT+1, 200)


class BaseSprite(pygame.sprite.Sprite):
    size = 10

    def __init__(self, x, y):
        super().__init__()
        self.image: pygame.Surface = pygame.Surface((self.size, self.size))
        self.rect: pygame.Rect = pygame.Rect((x, y, self.size, self.size))


class AppleSprite(BaseSprite):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image.fill((255, 0, 0))

    def update(self):
        part = SNAKE.sprites()[0]
        if part.rect.x == self.rect.x and part.rect.y == self.rect.y:
            print('Yam !')
            globals()['SCORE'] += 1  # very very bag code TODO Refactoring
            last_part = SNAKE.sprites()[-1]
            if last_part.direction[0] == 1:
                SnakePartSprite(last_part.rect.x - 10,
                                last_part.rect.y,
                                last_part.direction[0],
                                last_part.direction[1])
            elif last_part.direction[0] == -1:
                SnakePartSprite(last_part.rect.x + 10,
                                last_part.rect.y,
                                last_part.direction[0],
                                last_part.direction[1])
            elif last_part.direction[1] == 1:
                SnakePartSprite(last_part.rect.x,
                                last_part.rect.y-10,
                                last_part.direction[0],
                                last_part.direction[1])
            elif last_part.direction[0] == -1:
                SnakePartSprite(last_part.rect.x,
                                last_part.rect.y+10,
                                last_part.direction[0],
                                last_part.direction[1])
            self.kill()


class SnakePartSprite(BaseSprite):
    def __init__(self, x, y, x_dir, y_dir):
        super().__init__(x, y)
        self.direction = [x_dir, y_dir]
        self.image.fill((255, 255, 255))
        self.add(SNAKE)

    def update(self):
        for block in CHANGE_DIRECTION.sprites():
            if block.rect.x == self.rect.x and block.rect.y == self.rect.y:
                self.direction = block.direction
        if 0 <= self.rect.x <= X:
            self.rect.x += self.direction[0]*self.size
        if 0 <= self.rect.y <= Y:
            self.rect.y += self.direction[1]*self.size


class ChangeDirectionSprite(BaseSprite):
    def __init__(self, x, y, x_dir, y_dir):
        super().__init__(x, y)
        self.direction = [x_dir, y_dir]
        self.image.fill((0, 0, 0))
        self.add(CHANGE_DIRECTION)

    def update(self):
        a = True
        for part in SNAKE.sprites():
            if part.rect.x == self.rect.x and part.rect.y == self.rect.y:
                a = False

        if a:
            self.kill()


if __name__ == '__main__':
    APPLES = pygame.sprite.Group()
    SNAKE = pygame.sprite.Group()
    CHANGE_DIRECTION = pygame.sprite.Group()
    SnakePartSprite(X / 2, Y / 2, 0, 0)
    SCORE = 0
    while True:
        clock.tick(FPS)
        surface.fill((0, 0, 0))

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                print(SCORE)
                print(len(SNAKE.sprites()))
                exit()
            if i.type == pygame.USEREVENT:
                APPLES.add(AppleSprite(random.randint(0, X / 10) * 10, random.randint(0, Y / 10) * 10))
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_LEFT:
                    ChangeDirectionSprite(SNAKE.sprites()[0].rect.x, SNAKE.sprites()[0].rect.y, -1, 0)
                if i.key == pygame.K_RIGHT:
                    ChangeDirectionSprite(SNAKE.sprites()[0].rect.x, SNAKE.sprites()[0].rect.y, 1, 0)
                if i.key == pygame.K_UP:
                    ChangeDirectionSprite(SNAKE.sprites()[0].rect.x, SNAKE.sprites()[0].rect.y, 0, -1)
                if i.key == pygame.K_DOWN:
                    ChangeDirectionSprite(SNAKE.sprites()[0].rect.x, SNAKE.sprites()[0].rect.y, 0, 1)
            if i.type == pygame.USEREVENT+1:
                SNAKE.update()

        CHANGE_DIRECTION.draw(surface)
        APPLES.draw(surface)
        SNAKE.draw(surface)
        APPLES.update()
        CHANGE_DIRECTION.update()
        pygame.display.update()
