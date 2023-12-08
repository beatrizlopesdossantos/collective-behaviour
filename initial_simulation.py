import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1200, 800
FPS = 60
NUM_BIRDS = 40
VISION_RADIUS = 30
SPEED = 2

# Colors
WHITE = (255, 255, 255)
BACKGROUND = (150, 200, 255)

# Bird class
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = random.uniform(0, 2 * math.pi)

    def update(self, birds):
        # Get flocking behaviors
        alignment = self.align(birds)
        cohesion = self.cohere(birds)
        separation = self.separate(birds)

        # Combine behaviors
        angle = 0.5 * alignment + 0.5 * cohesion + 1.5 * separation
        if angle == 0:
            angle = self.direction

        # Update position
        self.direction += 0.15 * angle
        self.rect.x += int(SPEED * math.cos(self.direction))
        self.rect.y += int(SPEED * math.sin(self.direction))

        # Wrap around screen
        self.rect.x %= WIDTH
        self.rect.y %= HEIGHT

    def align(self, birds):
        # Alignment: steer towards the average heading of neighbors
        avg_direction = sum([bird.direction for bird in birds]) / len(birds)
        return avg_direction - self.direction

    def cohere(self, birds):
        # Cohesion: steer towards the average position of neighbors
        avg_position = (
            sum([bird.rect.x for bird in birds]) / len(birds),
            sum([bird.rect.y for bird in birds]) / len(birds),
        )
        angle_to_avg = math.atan2(avg_position[1] - self.rect.y, avg_position[0] - self.rect.x)
        return angle_to_avg - self.direction

    def separate(self, birds):
        # Separation: avoid crowding neighbors
        separation_vector = [0, 0]
        for bird in birds:
            if bird != self:
                distance = math.hypot(bird.rect.x - self.rect.x, bird.rect.y - self.rect.y)
                if 0 < distance < VISION_RADIUS:
                    separation_vector[0] += (self.rect.x - bird.rect.x) / distance
                    separation_vector[1] += (self.rect.y - bird.rect.y) / distance
        separation_angle = math.atan2(separation_vector[1], separation_vector[0])
        return separation_angle - self.direction

# Initialize Pygame screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flock of birds moving based on their vision")
clock = pygame.time.Clock()

# Create birds
birds = pygame.sprite.Group()
for _ in range(NUM_BIRDS):
    bird = Bird(random.randint(0, WIDTH), random.randint(0, HEIGHT))
    birds.add(bird)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BACKGROUND)

    # Update and draw birds
    for bird in birds:
        bird.update(birds)
        pygame.draw.circle(screen, WHITE, bird.rect.center, 4, 0)
        pygame.draw.circle(screen, WHITE, bird.rect.center, VISION_RADIUS, 1)
        pygame.draw.line(
            screen,
            WHITE,
            bird.rect.center,
            (
                bird.rect.center[0] + int(VISION_RADIUS * math.cos(bird.direction)),
                bird.rect.center[1] + int(VISION_RADIUS * math.sin(bird.direction)),
            ),
        )

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
