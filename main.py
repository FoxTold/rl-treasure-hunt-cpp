import pygame
import random
import numpy as np

# Initialize pygame
pygame.init()

# Environment configuration
GRID_SIZE = 6  # 10x10 grid
CELL_SIZE = 40  # Each cell is 40x40 pixels
WIDTH, HEIGHT = GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE
FPS = 5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)

# Actions
ACTIONS = ['UP', 'DOWN', 'LEFT', 'RIGHT']

class TreasureHuntEnv:
    def __init__(self):
        self.agent_pos = [0, 0]
        self.treasure_pos = [GRID_SIZE - 1, GRID_SIZE - 1]
        self.enemy_pos = [GRID_SIZE // 2, GRID_SIZE // 2]
        self.obstacles = self.generate_obstacles(15)
        self.state_space = GRID_SIZE * GRID_SIZE
        self.action_space = len(ACTIONS)
        self.reset()

    def reset(self):
        self.agent_pos = [0, 0]
        self.enemy_pos = [GRID_SIZE // 2, GRID_SIZE // 2]
        self.obstacles = self.generate_obstacles(15)
        return self.agent_pos

    def generate_obstacles(self, count):
        obstacles = []
        while len(obstacles) < count:
            pos = [random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)]
            if pos != self.agent_pos and pos != self.treasure_pos and pos not in obstacles:
                obstacles.append(pos)
        return obstacles

    def move_enemy(self):
        possible_moves = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        random.shuffle(possible_moves)
        for move in possible_moves:
            x, y = self.enemy_pos
            if move == 'UP' and y > 0:
                y -= 1
            elif move == 'DOWN' and y < GRID_SIZE - 1:
                y += 1
            elif move == 'LEFT' and x > 0:
                x -= 1
            elif move == 'RIGHT' and x < GRID_SIZE - 1:
                x += 1
            
            # Ensure enemy doesn't move into obstacles
            if [x, y] not in self.obstacles:
                self.enemy_pos = [x, y]
                break

    def step(self, action):
        # Move agent
        x, y = self.agent_pos
        if action == 'UP' and y > 0:
            y -= 1
        elif action == 'DOWN' and y < GRID_SIZE - 1:
            y += 1
        elif action == 'LEFT' and x > 0:
            x -= 1
        elif action == 'RIGHT' and x < GRID_SIZE - 1:
            x += 1

        if [x, y] not in self.obstacles:
            self.agent_pos = [x, y]

        # Move enemy
        self.move_enemy()

        reward = -1  # Step penalty
        done = False

        # Check for collisions
        if self.agent_pos == self.treasure_pos:
            reward = 100  # Treasure found
            done = True
        elif self.agent_pos == self.enemy_pos:
            reward = -100  # Agent caught by enemy
            done = True

        return self.agent_pos, reward, done

    def render(self, screen):
        screen.fill(WHITE)
        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(screen, BLACK, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(screen, BLACK, (0, y), (WIDTH, y))

        # Draw agent, treasure, enemy, and obstacles
        pygame.draw.rect(screen, BLUE, (*[p * CELL_SIZE for p in self.agent_pos], CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, GREEN, (*[p * CELL_SIZE for p in self.treasure_pos], CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, PURPLE, (*[p * CELL_SIZE for p in self.enemy_pos], CELL_SIZE, CELL_SIZE))
        for obs in self.obstacles:
            pygame.draw.rect(screen, RED, (*[p * CELL_SIZE for p in obs], CELL_SIZE, CELL_SIZE))

        pygame.display.flip()

# Pygame main loop
def main():
    env = TreasureHuntEnv()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    running = True
    done = False

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not done:
            action = random.choice(ACTIONS)  # Replace with RL agent's action
            _, _, done = env.step(action)

        env.render(screen)

    pygame.quit()

if __name__ == "__main__":
    main()
