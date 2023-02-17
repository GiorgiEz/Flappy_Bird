import pygame, random

pause, score = False, 0

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speedY = 0

        self.img = pygame.image.load("images/bird1.png").convert_alpha()
        self.img = pygame.transform.rotozoom(self.img, 0, 2)

    def render(self, screen):
        screen.blit(self.img, (self.x, self.y))

    def update(self):
        self.y -= self.speedY
        # gravity
        self.speedY -= 0.011


class Obstacle:
    def __init__(self):
        self.color = (0, 253, 117)
        self.x = 500
        self.y = random.randint(80, 420)

        self.LowerPipe = pygame.image.load("images/pipe.png").convert_alpha()
        self.LowerPipe = pygame.transform.rotozoom(self.LowerPipe, 0, 4)

        self.upperPipe = pygame.transform.rotate(self.LowerPipe, 180.0)

    def display_obstacle(self, screen):
        screen.blit(self.upperPipe, (self.x - 50, self.y - 418))
        screen.blit(self.LowerPipe, (self.x - 50, self.y + 200))
        
    def move(self):
        self.x = 500
        self.y = random.randint(80, 420)

    def update(self):
        self.x -= 0.3

class Background:
    def __init__(self):
        self.img = pygame.image.load("images/bg.png").convert_alpha()
        self.img = pygame.transform.rotozoom(self.img, 0, 1.5)

    def render(self, screen):
        screen.blit(self.img, (0, 0))

class Run:
    def __init__(self):
        self.running = False
        self.clock = None
        self.screen = None
        self.bird = None
        self.obstacle = None
        self.bg = None

    def run(self):
        self.init()
        while self.running: self.checkForCollisions()

    def init(self):
        self.screen = pygame.display.set_mode((500, 700))
        pygame.display.set_caption("Flappy Bird")
        pygame.init()
        self.bird = Bird(75, 350)
        self.clock = pygame.time.Clock()
        self.running = True

        self.obstacle = Obstacle()
        self.bg = Background()

    def update(self):
        self.events()
        self.bird.update()
        self.obstacle.update()

    def events(self):
        global pause,score
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            keys = pygame.key.get_pressed()
            if not pause:
                if keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]:
                    # Jump height
                    self.bird.speedY = 1.6
            if keys[pygame.K_RETURN] or pygame.mouse.get_pressed()[0]:
                if pause: score = 0
                pause = False
            if keys[pygame.K_ESCAPE]:
                self.running = False

    def collisions(self):
        global score, pause
        if self.is_collision(): self.death()

        if self.obstacle.x <= -50:
            self.obstacle.move()
            score += 1

        if self.bird.y >= 660:
            self.bird.y = 660
        if self.bird.y <= 0:
            self.bird.y = 0

    def render(self):
        self.bg.render(self.screen)
        self.bird.render(self.screen)
        self.obstacle.display_obstacle(self.screen)
        self.scores()
        pygame.display.flip()

    def is_collision(self):
        if self.obstacle.x - 100 <= self.bird.x <= self.obstacle.x + 50:
            if self.obstacle.y >= self.bird.y or self.bird.y >= self.obstacle.y + 165:
                return True
        return False

    def checkForCollisions(self):
        global pause
        while self.running:
            self.update()
            if not pause:
                self.render()
                self.collisions()
            else: self.death()

    def death(self):
        global pause
        self.game_over()
        pause = True
        self.reset()

    def scores(self):
        font = pygame.font.SysFont('tah-oma', 35)
        scores = font.render(f"Score: {score}", True, 'black')
        self.screen.blit(scores, (10, 5))

    def game_over(self):
        font = pygame.font.SysFont('tah-oma', 25)
        text = font.render(f"Click to play again or press Esc", True, "Black")
        self.screen.blit(text, (80, 300))
        pygame.display.flip()

    def reset(self):
        #helloooo
        self.bird = Bird(75, 350)
        self.obstacle = Obstacle()


if __name__ == "__main__":
    app = Run()
    app.run()
