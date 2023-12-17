import pygame
import math
import random

# Constants
WIDTH, HEIGHT = 1200, 800
BG_COLOR = (255, 255, 255)
BIRD_COLOR = (0, 0, 0)
NUM_BIRDS = 30
BL = 10  # Body length/diameter of each bird
DELTA_T = 0.1  # Time step for updating positions

ALPHA_0 = 20 # Acceleration coefficient for separation/cohesion
BETA_0 = 20 # Angular velocity coefficient for alignment
ALPHA_1 = 10 # Acceleration coefficient for adapting to spatial gradient velocity 
BETA_1 = 10 # Angular velocity coefficient for adapting to the angular gradient 
MAX_SPEED = 3


class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.v = 2 # Initial velocity
        self.angle = random.uniform(0, 2 * math.pi)
        self.bl = BL
        self.radius = BL / 2
        self.speed = 1 # Initial speed


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
        self.x %= WIDTH
        self.y %= HEIGHT

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

kkt = 125
# Create a set of birds
center_x, center_y = WIDTH // 2, HEIGHT // 2
birds = []
for _ in range(NUM_BIRDS):
    while True:
        new_x = center_x + random.uniform(-kkt, kkt)
        new_y = center_y + random.uniform(-kkt, kkt)
        
        # Check if the new position is not already taken
        if (new_x, new_y) not in [(b.x, b.y) for b in birds]:
            break

    birds.append(Bird(new_x, new_y))
# birds = [Bird(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(NUM_BIRDS)]

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