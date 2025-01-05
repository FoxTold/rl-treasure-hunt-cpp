import numpy as np
import pygame

class TreasureHuntEnv:
    def __init__(self, render_mode=None):
        self.grid_size = 6
        self.action_space = 4  # Up, Down, Left, Right
        self.window_size = 600
        self.cell_size = self.window_size // self.grid_size

        self.render_mode = render_mode
        self.pygame_initialized = False
        if render_mode == "pygame":
            self._init_pygame()  # Initialize Pygame components

        self.reset()

    def _init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_size, self.window_size + 50))  # Extra space for score
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.player_image = pygame.image.load("resources/player.png")
        self.player_image = pygame.transform.scale(self.player_image, (self.cell_size, self.cell_size))
        self.enemy_image = pygame.image.load("resources/player.png").copy()
        self.enemy_image.fill((255, 0, 0), special_flags=pygame.BLEND_MULT)
        self.pygame_initialized = True

    def reset(self):
        self.player_pos = (0, 0)
        self.treasures = [(2, 2), (3, 3), (4, 4)]  # Fixed treasure positions
        self.meta_flag = (5, 5)  # Fixed meta flag position
        self.enemy_pos = (0, 5)  # Fixed enemy position
        self.enemy_direction = 1  # 1 for down, -1 for up
        self.collected_treasures = 0
        self.steps = 0
        self.done = False
        return self._get_state()

    def _get_state(self):
        grid = np.zeros((self.grid_size, self.grid_size), dtype=np.float32)
        px, py = self.player_pos
        grid[px, py] = 1.0
        for tx, ty in self.treasures:
            grid[tx, ty] = 2.0
        ex, ey = self.enemy_pos
        grid[ex, ey] = 3.0
        mx, my = self.meta_flag
        grid[mx, my] = 4.0
        return grid

    def render(self):
        if self.render_mode == "pygame":
            if not self.pygame_initialized:
                self._init_pygame()
            self._render_pygame()
        elif self.render_mode == "text":
            print(self._get_state())
        elif self.render_mode is None:
            pass

    def _render_pygame(self):
        self.screen.fill((255, 255, 255))
        score_text = self.font.render(f"Score: {self.collected_treasures}", True, (0, 0, 0))
        step_text = self.font.render(f"Step: {self.steps}", True, (0, 0, 0))
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(step_text, (self.window_size - 200, 10))

        for x in range(self.grid_size):
            for y in range(self.grid_size):
                rect = pygame.Rect(y * self.cell_size, x * self.cell_size + 50, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)

        for tx, ty in self.treasures:
            center = (ty * self.cell_size + self.cell_size // 2, tx * self.cell_size + 50 + self.cell_size // 2)
            pygame.draw.circle(self.screen, (255, 223, 0), center, self.cell_size // 4)

        mx, my = self.meta_flag
        for i in range(2):
            for j in range(2):
                color = (255, 255, 255) if (i + j) % 2 == 0 else (0, 0, 0)
                rect = pygame.Rect(my * self.cell_size + j * self.cell_size // 2, mx * self.cell_size + 50 + i * self.cell_size // 2, self.cell_size // 2, self.cell_size // 2)
                pygame.draw.rect(self.screen, color, rect)

        ex, ey = self.enemy_pos
        self.screen.blit(self.enemy_image, (ey * self.cell_size, ex * self.cell_size + 50))

        px, py = self.player_pos
        self.screen.blit(self.player_image, (py * self.cell_size, px * self.cell_size + 50))
        pygame.display.flip()
        self.clock.tick(1)

    def step(self, action):
        if self.done:
            raise ValueError("Game is over. Reset the environment to play again.")

        x, y = self.player_pos
        if action == 0:  # Up
            x = max(0, x - 1)
        elif action == 1:  # Down
            x = min(self.grid_size - 1, x + 1)
        elif action == 2:  # Left
            y = max(0, y - 1)
        elif action == 3:  # Right
            y = min(self.grid_size - 1, y + 1)

        self.player_pos = (x, y)
        self.steps += 1
        reward = -0.05  # Start reward at 0

        if self.player_pos in self.treasures:
            self.treasures.remove(self.player_pos)
            self.collected_treasures += 1
            reward += 0.1  # Reward for collecting a treasure

        if self.player_pos == self.meta_flag and self.collected_treasures == 3:  # Total treasures is 3
            reward += 0.5  # Reward for reaching the meta flag
            self.done = True

        self._move_enemy()

        if self.player_pos == self.enemy_pos:
            reward -= 0.2  # Penalty for being caught by the enemy
            self.done = True

        if self.steps >= 100:
            self.done = True

        return self._get_state(), reward, self.done, {}

    def _move_enemy(self):
        ex, ey = self.enemy_pos
        if self.enemy_direction == 1 and ex < self.grid_size - 1:
            ex += 1
        elif self.enemy_direction == -1 and ex > 0:
            ex -= 1
        else:
            self.enemy_direction *= -1
            ex += self.enemy_direction

        self.enemy_pos = (ex, ey)

    def close(self):
        if self.pygame_initialized:
            pygame.quit()

# Example usage
if __name__ == "__main__":
    env = TreasureHuntEnv(render_mode="pygame")
    state = env.reset()
    done = False

    while not done:
        action = np.random.randint(0, 4)
        state, reward, done, _ = env.step(action)
        env.render()

    env.close()
