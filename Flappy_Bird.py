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

class ParallaxBackground:
    def __init__(self):
        self.img = pygame.image.load("images/bg.png").convert_alpha()
        self.img = pygame.transform.rotozoom(self.img, 0, 1.5)

        self.offset = 0
        self.speed = 0.1  # slow drifting background

        self.width = self.img.get_width()
        self.height = self.img.get_height()

    def update(self):
        self.offset -= self.speed
        if self.offset <= -self.width:
            self.offset = 0

    def render(self, screen, shake_offset=(0, 0)):
        ox, oy = shake_offset
        screen.blit(self.img, (self.offset + ox, oy))
        screen.blit(self.img, (self.offset + self.width + ox, oy))

class Cloud:
    def __init__(self):
        img_name = random.choice(["cloud1.png", "cloud2.png", "cloud3.png"])
        self.img = pygame.image.load(f"images/{img_name}").convert_alpha()

        scale = random.uniform(0.6, 1.3)
        self.img = pygame.transform.rotozoom(self.img, 0, scale)

        self.x = random.randint(0, 500)
        self.y = random.randint(20, 200)
        self.speed = random.uniform(0.2, 0.7)

    def update(self):
        self.x -= self.speed
        if self.x < -200:
            self.x = 600
            self.y = random.randint(20, 200)
            self.speed = random.uniform(0.2, 0.7)

    def render(self, screen, shake_offset=(0, 0)):
        ox, oy = shake_offset
        screen.blit(self.img, (self.x + ox, self.y + oy))


class RainParticle:
    def __init__(self, width, height):
        self.x = random.randint(0, width)
        self.y = random.randint(-200, -10)
        self.speed_y = random.uniform(4, 8)
        self.length = random.randint(8, 15)
        self.thickness = 1

    def update(self):
        self.y += self.speed_y
        if self.y > 800:
            self.y = random.randint(-200, -10)
            self.x = random.randint(0, 500)

    def render(self, screen, shake_offset=(0, 0)):
        ox, oy = shake_offset
        pygame.draw.line(
            screen,
            (180, 180, 255),
            (self.x + ox, self.y + oy),
            (self.x + ox, self.y + self.length + oy),
            self.thickness
        )


class RainSystem:
    def __init__(self, count=150, width=500, height=700):
        self.particles = [RainParticle(width, height) for _ in range(count)]

    def update(self):
        for p in self.particles:
            p.update()

    def render(self, screen, shake_offset=(0, 0)):
        for p in self.particles:
            p.render(screen, shake_offset)


class CameraShake:
    def __init__(self):
        self.duration = 0
        self.intensity = 0

    def trigger(self, intensity=5, duration=20):
        self.intensity = intensity
        self.duration = duration

    def update(self):
        if self.duration > 0:
            self.duration -= 1
            return (random.randint(-self.intensity, self.intensity),
                    random.randint(-self.intensity, self.intensity))
        return (0, 0)


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
        pygame.init()
        self.screen = pygame.display.set_mode((500, 700))
        pygame.display.set_caption("Flappy Bird")

        self.bird = Bird(75, 350)
        self.obstacle = Obstacle()

        self.bg = ParallaxBackground()
        self.clouds = [Cloud() for _ in range(4)]
        self.rain = RainSystem(count=150)

        self.shake = CameraShake()

        self.clock = pygame.time.Clock()
        self.running = True

    def update(self):
        self.events()

        self.bg.update()
        for c in self.clouds: c.update()
        self.rain.update()

        self.bird.update()
        self.obstacle.update()

        shake_offset = self.shake.update()
        self.shake_offset = shake_offset

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
        ox, oy = self.shake_offset

        self.bg.render(self.screen, self.shake_offset)
        for c in self.clouds:
            c.render(self.screen, self.shake_offset)
        self.rain.render(self.screen, self.shake_offset)

        self.bird.render(self.screen)  # you may also shake this
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
        self.shake.trigger(intensity=8, duration=25)
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
        self.bird = Bird(75, 350)
        self.obstacle = Obstacle()


if __name__ == "__main__":
    app = Run()
    app.run()
