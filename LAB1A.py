import pygame
import sys
from collections import deque

# Grid dimensions
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 20, 20
CELL_SIZE = WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Gridworld Navigation")

# Define the environment grid and the obstacles
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
obstacles = [(5, 5), (6, 5), (7, 5), (8, 5), (9, 5)]
target_position = (15, 15)

# Place obstacles and target in the grid
for (x, y) in obstacles:
    grid[y][x] = 1
grid[target_position[1]][target_position[0]] = 2


# Define the agent's properties
class Agent:
    def __init__(self, start_position):
        self.position = start_position
        self.path = []

    def move(self, direction):
        x, y = self.position
        if direction == "up" and y > 0:
            self.position = (x, y - 1)
        elif direction == "down" and y < ROWS - 1:
            self.position = (x, y + 1)
        elif direction == "left" and x > 0:
            self.position = (x - 1, y)
        elif direction == "right" and x < COLS - 1:
            self.position = (x + 1, y)

    def sense_environment(self):
        x, y = self.position
        surroundings = []
        directions = ["up", "down", "left", "right"]
        for dx, dy, direction in [(-1, 0, "left"), (1, 0, "right"), (0, -1, "up"), (0, 1, "down")]:
            if 0 <= x + dx < COLS and 0 <= y + dy < ROWS:
                surroundings.append((grid[y + dy][x + dx], direction))
        return surroundings

    def bfs_pathfinding(self, target):
        queue = deque([(self.position, [])])
        visited = set()
        visited.add(self.position)
        while queue:
            current, path = queue.popleft()
            if current == target:
                self.path = path
                return path
            x, y = current
            for dx, dy, move in [(-1, 0, "left"), (1, 0, "right"), (0, -1, "up"), (0, 1, "down")]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < COLS and 0 <= ny < ROWS and (nx, ny) not in visited and grid[ny][nx] != 1:
                    queue.append(((nx, ny), path + [move]))
                    visited.add((nx, ny))
        return []


# Draw the grid and entities
def draw_grid():
    for y in range(ROWS):
        for x in range(COLS):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            color = WHITE
            if grid[y][x] == 1:
                color = BLACK  # Obstacle
            elif grid[y][x] == 2:
                color = RED  # Target
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLUE, rect, 1)  # Outline


# Main simulation loop
def main():
    agent = Agent(start_position=(0, 0))
    target = target_position
    agent.bfs_pathfinding(target)

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(WHITE)
        draw_grid()
        x, y = agent.position
        pygame.draw.rect(screen, GREEN, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Move agent along the found path
        if agent.path:
            next_move = agent.path.pop(0)
            agent.move(next_move)

        pygame.display.flip()
        clock.tick(5)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
LAB1A.py