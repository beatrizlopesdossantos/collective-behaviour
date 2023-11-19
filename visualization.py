import matplotlib.pyplot as plt
from random import randint
from typing import List

class Animal:
    def __init__(self, x, y, velocity_x = 0, velocity_y = 0):
        self.position = (x, y)
        self.velocity = (velocity_x, velocity_y)

    def move(self):
        x, y = self.position
        vx, vy = self.velocity
        new_x = x + vx
        new_y = y + vy
        self.position = (new_x, new_y)

    def change_velocity(self, other, vision):
        #self.velocity = (self.velocity[0] + randint(-3, 3), self.velocity[1] + randint(-3, 3))
        distance = ((self.position[0] - other.position[0])**2 + (self.position[1] - other.position[1])**2)**0.5
        colision = 10
        if distance < colision:
            self.velocity = other.velocity
            
        elif distance >= colision and distance < vision:
            # Get closer, return a velocity vector towards point A
            dx = self.position[0] - other.position[0]
            dy = self.position[1] - other.position[1]
            magnitude = (dx**2 + dy**2)**0.5
            if magnitude == 0:
                self.velocity = (0, 0)
            else:
                self.velocity = (dx / magnitude * 2, dy / magnitude * 2)  # You can adjust the factor (2) for the desired speed.
        else:
            # Move randomly within a range of (-3, 3) units in both x and y directions
            self.velocity = (self.velocity[0] + randint(-4, 4), self.velocity[1] + randint(-4, 4))

    def __str__(self):
        return f"Animal at position {self.position} with velocity {self.velocity}"



def visualize(points):
    x = [point[0] for point in points]
    y = [point[1] for point in points]

    plt.scatter(x, y)
    plt.xlabel('South')
    plt.ylabel('West')
    plt.title('Birds with vision = 80')

if __name__ == "__main__":
    animals: List[Animal] = []
    r = 300
    vision = 80
    for _ in range(20):
        animals.append(Animal(randint(-r,r), randint(-r,r)))

    for _ in range(200):
        for i, animal in enumerate(animals):
            animal.move()
            for a in range(0, i):
                animal.change_velocity(animals[a], vision)

        plt.clf()
        visualize(list(map(lambda animal: animal.position, animals)))
        plt.pause(0.01) 

    plt.show() 
