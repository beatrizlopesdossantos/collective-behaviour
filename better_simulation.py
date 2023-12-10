import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1500, 800
BG_COLOR = (180, 230, 255)
BIRD_COLOR = (0, 0, 0)
VISION_COLOR = (200, 200, 200)
NUM_BIRDS = 50
VISION_ANGLE = 100
VISION_RADIUS = 30
TURN_SPEED = 0.3
SPEED = 2

# Bird class
class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = random.uniform(0, 2 * math.pi)
        self.group_count = 0

    def update(self, birds):
        # Check for nearby birds in vision
        nearby_birds = [b for b in birds if b != self and self.in_vision(b)]
        if len(nearby_birds) == 1:
            self.group_count = 1
            nearby_birds[0].group_count = 1

        if len(nearby_birds) != 0:

            avg_angle = sum([b.angle for b in nearby_birds]) / len(nearby_birds)
            self.angle = (avg_angle + 2 * math.pi) % (2 * math.pi)
            self.neighbor_count = len(nearby_birds)
        
        else:

            self.angle += random.uniform(-TURN_SPEED, TURN_SPEED)

        if self.group_count == 0:
            self.angle += random.uniform(-TURN_SPEED, TURN_SPEED)

        # Move forward
        self.x = (self.x + SPEED * math.cos(self.angle)) % WIDTH
        self.y = (self.y + SPEED * math.sin(self.angle)) % HEIGHT

    def in_vision(self, other_bird):
        # Check if the other bird is within vision radius
        return math.hypot(other_bird.x - self.x, other_bird.y - self.y) < VISION_RADIUS


# Create birds
birds = [Bird(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(NUM_BIRDS)]

# Main loop
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Birds orientation based purely on their vision")

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
        tmp = -1 * bird.angle
        pygame.draw.arc(screen, 
                        VISION_COLOR, 
                        pygame.Rect(bird.x - VISION_RADIUS, bird.y - VISION_RADIUS, VISION_RADIUS*2, VISION_RADIUS*2), 
                        (tmp - 0.75 * math.pi + math.pi * 2 ) % (2 * math.pi),
                        (tmp + 0.75 * math.pi + math.pi * 2 ) % (2 * math.pi), 
                        1)



    pygame.display.flip()
    pygame.time.Clock().tick(30)
