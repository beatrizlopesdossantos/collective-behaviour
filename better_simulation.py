import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1200, 800
BG_COLOR = (255, 255, 255)
BIRD_COLOR = (0, 0, 0)
VISION_COLOR = (200, 200, 200)
NUM_BIRDS = 50
VISION_ANGLE = 100
VISION_RADIUS = 50
TURN_SPEED = 0.1
SPEED = 2

# Bird class
class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = random.uniform(0, 2 * math.pi)

    def update(self, birds):
        # Check for nearby birds in vision
        nearby_birds = [b for b in birds if b != self and self.in_vision(b)]

        if len(nearby_birds) != 0:

            avg_position = (
                sum([bird.x for bird in nearby_birds]) / len(nearby_birds),
                sum([bird.y for bird in nearby_birds]) / len(nearby_birds),
            )

            vector_x = avg_position[0] - self.x
            vector_y = avg_position[1] - self.y
            direction_radians = math.atan2(vector_y, vector_x)
            self.angle = (direction_radians + 2 * math.pi) % (2 * math.pi)
        
        else:

            self.angle += random.uniform(-TURN_SPEED, TURN_SPEED)

        # Move forward
        self.x = (self.x + SPEED * math.cos(self.angle)) % WIDTH
        self.y = (self.y + SPEED * math.sin(self.angle)) % HEIGHT

    def in_vision(self, other_bird):
        angle_to_other = math.atan2(other_bird.y - self.y, other_bird.x - self.x)
        angle_diff = abs(angle_to_other - self.angle)

        # Check if the other bird is within vision angle and radius
        return angle_diff < math.radians(VISION_ANGLE / 2) and math.hypot(
            other_bird.x - self.x, other_bird.y - self.y
        ) < VISION_RADIUS

# Create birds
birds = [Bird(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(NUM_BIRDS)]

# Main loop
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flock of Birds")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update bird positions
    for bird in birds:
        bird.update(birds)

    # Draw background
    screen.fill(BG_COLOR)

    # Draw birds and their vision
    for bird in birds:
        pygame.draw.circle(screen, BIRD_COLOR, (int(bird.x), int(bird.y)), 5)
        vision_end_x = bird.x + VISION_RADIUS * math.cos(bird.angle + 0.75 * math.pi)
        vision_end_y = bird.y + VISION_RADIUS * math.sin(bird.angle + 0.75 * math.pi)
        pygame.draw.line(screen, VISION_COLOR, (bird.x, bird.y), (vision_end_x, vision_end_y))
        vision_end_x = bird.x + VISION_RADIUS * math.cos(bird.angle - 0.75 * math.pi)
        vision_end_y = bird.y + VISION_RADIUS * math.sin(bird.angle - 0.75 * math.pi)
        pygame.draw.line(screen, VISION_COLOR, (bird.x, bird.y), (vision_end_x, vision_end_y))
        pygame.draw.arc(screen, 
                        VISION_COLOR, 
                        pygame.Rect(bird.x - VISION_RADIUS, bird.y - VISION_RADIUS, VISION_RADIUS*2, VISION_RADIUS*2), 
                        bird.angle - 0.75 * math.pi, 
                        bird.angle + 0.75 * math.pi,
                        1)

    pygame.display.flip()
    pygame.time.Clock().tick(30)
