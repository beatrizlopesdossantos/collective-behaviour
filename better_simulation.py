import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BG_COLOR = (180, 230, 255)
BIRD_COLOR = (0, 0, 0)
VISION_COLOR = (255, 255, 255)
NUM_BIRDS = 10
VISION_ANGLE = 360
VISION_RADIUS = 30
VISION_ANGLE_RAD = VISION_ANGLE * math.pi / 180

# A higher ALPHA_0 will lead to a stronger acceleration effect from birds in a bird's field of vision.
ALPHA_0 = 1
# A BETA _0 value of -1 makes birds turn away from the side where more birds are present, potentially dispersing the flock.
BETA_0 = -1
# A GAMMA value of 1.5 can rapidly slow birds down to their preferred speed, possibly leading to a more 
# ordered and less erratic flock movement.
GAMMA = 0.05
# DELTA_T controls the granularity of time in the simulation; a value too high might 
# lead to instability or unrealistic behavior, while a value too low could lead to a very slow-running simulation. 
# 0.1 is typically a balanced choice to ensure smooth behavior in real time.
DELTA_T = 0.1
v0 = 2

# Bird class
class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.v = v0
        self.angle = random.uniform(0, 2 * math.pi)

    def update(self, birds):
        left_count = 0
        right_count = 0
        front_count = 0
        
        # Count birds in different vision areas
        for other in birds:
            if other != self and self.in_vision(other):
                angle_to_other = self.relative_angle(other)
                if -math.pi / 2 <= angle_to_other < math.pi / 2:
                    front_count += 1
                if angle_to_other < 0:
                    left_count += 1
                else:
                    right_count += 1
        
        # Equation for velocity (speed) change
        dv = ALPHA_0 * front_count - GAMMA * (self.v - v0)
        self.v += dv * DELTA_T

        # Equation for orientation (angle) change
        dpsi = BETA_0 * (right_count - left_count)
        self.angle += dpsi * DELTA_T
        self.angle = (self.angle + 2 * math.pi) % (2 * math.pi)  # Normalize the angle

        # Move forward based on the new speed and direction
        self.x = (self.x + self.v * math.cos(self.angle)) % WIDTH
        self.y = (self.y + self.v * math.sin(self.angle)) % HEIGHT

    def in_vision(self, other):
        distance = math.hypot(other.x - self.x, other.y - self.y)
        angle_to_other = self.relative_angle(other)
        return (distance <= VISION_RADIUS and
                -VISION_ANGLE_RAD / 2 <= angle_to_other <= 
                VISION_ANGLE_RAD / 2)

    def relative_angle(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        angle_to_other = math.atan2(dy, dx)
        return (angle_to_other - self.angle + math.pi) % (2 * math.pi) - math.pi
    
    def draw(self, screen):
        pygame.draw.circle(screen, BIRD_COLOR, (int(bird.x), int(bird.y)), 5)
        # Vision field
        # pygame.draw.circle(screen, BIRD_COLOR, (int(bird.x), int(bird.y)), VISION_RADIUS, 1)

# Create birds
birds = [Bird(random.randint(0, WIDTH), random.randint(0, HEIGHT))
         for _ in range(NUM_BIRDS)]

# Main simulation loop
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flocking Simulation")

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update bird positions
    for bird in birds:
        bird.update(birds)

    # Draw background
    screen.fill(BG_COLOR)

    # Draw birds and their fields of vision
    for bird in birds:
        bird.draw(screen)

    pygame.display.flip()
    pygame.time.Clock().tick(30)

pygame.quit()
sys.exit()