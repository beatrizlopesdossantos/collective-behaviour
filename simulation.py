import pygame
import math
import random

# Constants
WIDTH, HEIGHT = 800, 600
BG_COLOR = (255, 255, 255)
BIRD_COLOR = (0, 0, 0)
NUM_BIRDS = 50
BL = 10  # Body length/diameter of each bird
DELTA_T = 2.0  # Time step for updating positions
ALPHA_0 = 2 # Acceleration coefficient for separation/cohesion
BETA_0 = 0.01  # Angular velocity coefficient for alignment
ALPHA_1 = 0.2  # Acceleration coefficient for adapting to spatial gradient velocity 
BETA_1 = 0.2  # Angular velocity coefficient for adapting to the angular gradient 
MAX_SPEED = 5


class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.v = 20  # Initial velocity
        self.angle = random.uniform(0, 2 * math.pi)
        self.bl = BL
        self.radius = BL / 2
        self.speed = 2  # Initial speed


    def update(self, birds):
        # Initialize the change in speed and heading
        dspeed = 0
        dangle = 0
        
        # Distance and angle differences to other birds
        distances = [self.distance_to(other) for other in birds if other != self]
        angle_diffs = [(math.atan2(other.y - self.y, other.x - self.x) - self.angle) % (2*math.pi) for other in birds if other != self]
        
        for dist, angle_diff in zip(distances, angle_diffs):
            if angle_diff > math.pi:
                angle_diff -= 2 * math.pi  # Wrap the angle to [-pi, pi]

            # Separate from birds that are too close
            if dist < self.radius * 2:
                dspeed -= ALPHA_0 / dist
                dangle -= BETA_0 * angle_diff / dist
            
            # Cohere towards birds that are at an ideal distance
            elif dist < self.radius * 4:
                dspeed += ALPHA_0 / dist
                dangle += BETA_0 * angle_diff / dist
        
        # Compute spatial gradient based on the average speed.
        avg_speed = sum(other.speed for other in birds if other != self) / (len(birds) - 1)
        spatial_grad = avg_speed - self.speed
        
        # Compute angular gradient based on the average angle.
        avg_angle = sum(angle_diffs) / len(angle_diffs) if angle_diffs else 0
        angular_grad = avg_angle - self.angle
        
        # Apply the adaptive coefficients
        dspeed += ALPHA_1 * spatial_grad
        dangle += BETA_1 * angular_grad

        # Cap the speed to a maximum value to maintain control
        self.speed = min(self.speed + dspeed * DELTA_T, MAX_SPEED)
        self.angle += dangle * DELTA_T
        
        # Update position with the adjusted speed and angle
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        
        # Wrap-around the screen
        self.x %= (WIDTH - 10)
        self.y %= (HEIGHT - 10)

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx * dx + dy * dy)
    
    @staticmethod
    def normalize_angle(angle):
        # Normalize angle to be between -pi and pi
        while angle <= -math.pi:
            angle += 2 * math.pi
        while angle > math.pi:
            angle -= 2 * math.pi
        return angle
    
    def move(self):
        self.x += self.v * math.cos(self.angle) * DELTA_T
        self.y += self.v * math.sin(self.angle) * DELTA_T
        self.x %= WIDTH
        self.y %= HEIGHT

    def draw(self, screen):
        # Draw bird as a circle with radius = BL / 2
        pygame.draw.circle(screen, BIRD_COLOR, (int(self.x), int(self.y)), self.bl // 2)

# Set up the Pygame screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flocking Simulation")

# Create a set of birds
birds = [Bird(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(NUM_BIRDS)]

running = True
clock = pygame.time.Clock()

# Main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill(BG_COLOR)

    # Update and draw all birds
    for bird in birds:
        bird.update(birds)
        bird.draw(screen)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()