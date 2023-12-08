import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1200, 800
FPS = 60
NUM_BIRDS = 30
VISION_RADIUS = 20
SPEED = 2
BACKGROUND_COLOR = (173, 216, 230)
VISION_COLOR = (255, 255, 0, 90)

# Bird class
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 255, 255))
        self.image.set_colorkey((255, 255, 255))
        pygame.draw.circle(self.image, (255, 255, 255), (5, 5), 5)
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = random.uniform(0, 2 * math.pi)

    def update(self, birds):
        # Get flocking behaviors
        alignment = self.align(birds)
        cohesion = self.cohere(birds)
        separation = self.separate(birds)

        # Combine behaviors
        if alignment is not None and cohesion is not None and separation is not None:
            angle = alignment
        else:
            angle = random.uniform(-0.1, 0.1)  # Random direction if no birds in vision
            angle = self.direction + angle

        # Update position
        self.direction = angle
        self.rect.x += int(SPEED * math.cos(self.direction))
        self.rect.y += int(SPEED * math.sin(self.direction))

        # Wrap around screen
        self.rect.x %= WIDTH
        self.rect.y %= HEIGHT

    def align(self, birds):
        # Alignment: steer towards the average heading of neighbors
        neighbors = [bird for bird in birds if bird != self and self.in_vision(bird)]
        if neighbors:
            avg_direction = sum([bird.direction for bird in neighbors]) / len(neighbors)
            return avg_direction - self.direction
        return None

    def cohere(self, birds):
        # Cohesion: steer towards the average position of neighbors
        neighbors = [bird for bird in birds if bird != self and self.in_vision(bird)]
        if neighbors:
            avg_position = (
                sum([bird.rect.x for bird in neighbors]) / len(neighbors),
                sum([bird.rect.y for bird in neighbors]) / len(neighbors),
            )
            angle_to_avg = math.atan2(avg_position[1] - self.rect.y, avg_position[0] - self.rect.x)
            return angle_to_avg - self.direction
        return None

    def separate(self, birds):
        # Separation: avoid crowding neighbors
        neighbors = [bird for bird in birds if bird != self and self.in_vision(bird)]
        if neighbors:
            separation_vector = [0, 0]
            for bird in neighbors:
                distance = math.hypot(bird.rect.x - self.rect.x, bird.rect.y - self.rect.y)
                separation_vector[0] += (self.rect.x - bird.rect.x) / distance
                separation_vector[1] += (self.rect.y - bird.rect.y) / distance
            separation_angle = math.atan2(separation_vector[1], separation_vector[0])
            return separation_angle - self.direction
        return None

    def in_vision(self, other_bird):
        distance = math.hypot(other_bird.rect.x - self.rect.x, other_bird.rect.y - self.rect.y)
        angle_to_other = math.atan2(other_bird.rect.y - self.rect.y, other_bird.rect.x - self.rect.x)
        angle_difference = abs(angle_to_other - self.direction)
        return 0 < distance < VISION_RADIUS and angle_difference < math.radians(150)

# Initialize Pygame screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flock of Birds")
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

    screen.fill(BACKGROUND_COLOR)

    # Update and draw birds
    for bird in birds:
        bird.update(birds)
        # Draw vision area
        pygame.draw.circle(screen, VISION_COLOR, bird.rect.center, VISION_RADIUS, 1)
        # Draw bird
        screen.blit(bird.image, bird.rect.topleft)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
