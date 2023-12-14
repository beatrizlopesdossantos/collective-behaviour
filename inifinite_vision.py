import matplotlib.pyplot as plt
import numpy as np
import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

def distance(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

# function to check if point is inside circle
def is_inside(circle, point):
    return distance(circle.center, point) <= circle.radius

def is_in_vision(circle1, circle2, circle3):
    """
    Check if one object is in vision of other.

    Parameters:
    - circle1 (Circle): Object with a vision.
    - circle2 (Circle): Target object.
    - circle3 (Circle): Obstacle.

    Returns:
    bool: True if circle2 is in vision of circle1.
    """

    points_on_circle2 = []
    for i in range(8):
        angle = (2 * math.pi / 8) * i
        x = circle2.center.x + circle2.radius * math.cos(angle)
        y = circle2.center.y + circle2.radius * math.sin(angle)
        points_on_circle2.append(Point(x, y))

    vectors = []
    for point in points_on_circle2:
            v = (point.x - circle1.center.x, point.y - circle1.center.y)
            v = (v[0] / math.sqrt(v[0]**2 + v[1]**2), v[1] / math.sqrt(v[0]**2 + v[1]**2))
            vectors.append(v)

    counter = 0
    for i, vec in enumerate(vectors):
        end = Point(circle1.center.x + vec[0], circle1.center.y + vec[1])
        if (abs(end.x - circle1.center.x) == abs(points_on_circle2[i].x - circle1.center.x) or
            abs(end.y - circle1.center.y) == abs(points_on_circle2[i].y - circle1.center.y)):
            counter += 1
            continue
        while (abs(end.x - circle1.center.x) < abs(points_on_circle2[i].x - circle1.center.x) and 
               abs(end.y - circle1.center.y) < abs(points_on_circle2[i].y - circle1.center.y)):
            if is_inside(circle3, end):
                counter += 1
                break
            end = Point(end.x + vec[0], end.y + vec[1])

    return counter != len(points_on_circle2)


def draw_circles_and_line(circle1, circle2, circle3):
    fig, ax = plt.subplots()

    # Draw circle1
    circle1_patch = plt.Circle((circle1.center.x, circle1.center.y), circle1.radius, color='blue', fill=False)
    ax.add_patch(circle1_patch)

    # Draw circle2
    circle2_patch = plt.Circle((circle2.center.x, circle2.center.y), circle2.radius, color='green', fill=False)
    ax.add_patch(circle2_patch)

    # Draw circle3
    circle3_patch = plt.Circle((circle3.center.x, circle3.center.y), circle3.radius, color='red', fill=False)
    ax.add_patch(circle3_patch)

    # Draw the line connecting circle1 center and four points on circle2
    points_on_circle2 = []
    for i in range(8):
        angle = (2 * math.pi / 8) * i
        x = circle2.center.x + circle2.radius * math.cos(angle)
        y = circle2.center.y + circle2.radius * math.sin(angle)
        points_on_circle2.append(Point(x, y))

    for point in points_on_circle2:
        line_x = [circle1.center.x, point.x]
        line_y = [circle1.center.y, point.y]
        ax.plot(line_x, line_y, linestyle='--', color='black', label=f'Line C1-{points_on_circle2.index(point) + 1}')

    # Mark the four points on circle2
    ax.scatter(*zip(*[(point.x, point.y) for point in points_on_circle2]), color='black', label='Points on C2')

    ax.set_aspect('equal', adjustable='datalim')
    ax.legend()
    plt.grid(True)
    plt.show()


def draw_flock(circles):
    _, ax = plt.subplots()

    circle = circles[0]

    circle_patch = plt.Circle((circle.center.x, circle.center.y), circle.radius, color="blue", fill=True)
    ax.add_patch(circle_patch)

    visible = False

    for j, other_circle in enumerate(circles[1:]):

        for k, obstacle in enumerate(circles[1:]):
            if j == k:
                continue
            if not is_in_vision(circle, other_circle, obstacle):
                print(f"Circle ({circle.center.x}, {circle.center.y}) does not see circle ({circles[j+1].center.x}, {circles[j+1].center.y}) because of ({circles[k+1].center.x}, {circles[k+1].center.y})")
                visible = False
                break
            visible = True

        color = 'green' if visible else 'red'
        circle_patch = plt.Circle((other_circle.center.x, other_circle.center.y), other_circle.radius, color=color, fill=True)
        ax.add_patch(circle_patch)

    ax.plot()

    ax.set_aspect('equal', adjustable='datalim')
    plt.grid(True)
    plt.show()


def main(num_of_units=10):
    
    circles = []
    i = 0
    while (i < num_of_units):
        center = Point(np.random.randint(0, 150), np.random.randint(0, 100))
        radius = np.random.randint(4, 8)
        acceptable = True
        for c in circles:
            dist = distance(c.center, center)
            if (dist < (c.radius + radius)):
                acceptable = False
                break
        if acceptable:    
            circles.append(Circle(center, radius))
            print("o", end="")
            i += 1

    # Check if any of the four points on circle2 intersects with circle3
    # result = is_in_vision(circle1, circle2, circle3)
    # print("Does it see the other disc?", result)

    for ci in circles:
        print(ci.center.x, ci.center.y, ci.radius)
    draw_flock(circles)

main(15)
