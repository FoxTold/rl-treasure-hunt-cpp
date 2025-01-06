from argparse import Action

import numpy as np
import pygame
import random
import itertools

def hash_state(state):
    return tuple(map(tuple, state))

def primt(policy):
    for p in policy:
        print(p)
    env = TreasureHuntEnv(render_mode="none")
    state = env.reset()
    done = False
    action = None
    steps = 0
    moves = [3,1]
    while not done:
        hashed_state = hash_state(state)

        try:
            action = policy[hashed_state]
        except KeyError:
            action = moves[steps % 2]
            policy[hashed_state] = moves[steps % 2]
        state, reward, done, _ = env.step(action)
        if hashed_state[4][5] == 1.0:
            policy[hashed_state] = 1

        steps += 1
        env.render()

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
        if self.collected_treasures < 3:  # Ensure all treasures are collected before removing enemies
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

        if self.collected_treasures < 3:  # Ensure all treasures are collected before removing enemies
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
        reward = 0.0  # Start reward at 0

        if self.player_pos in self.treasures:
            self.treasures.remove(self.player_pos)
            self.collected_treasures += 1
            reward += 0.1  # Reward for collecting a treasure

        if self.player_pos == self.meta_flag and self.collected_treasures == 3:  # Total treasures is 3
            reward += 0.5  # Reward for reaching the meta flag
            self.done = True

        if self.collected_treasures < 3:  # Ensure enemies move only if treasures remain
            self._move_enemy()

        if self.collected_treasures < 3 and self.player_pos == self.enemy_pos:
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

    def get_possible_actions(self, state):
        px, py = self.player_pos
        possible_actions = []

        if px > 0:  # Can move up
            possible_actions.append(0)
        if px < self.grid_size - 1:  # Can move down
            possible_actions.append(1)
        if py > 0:  # Can move left
            possible_actions.append(2)
        if py < self.grid_size - 1:  # Can move right
            possible_actions.append(3)

        return possible_actions

    def get_next_states(self, state, action):
        """
        Get all possible next states from the given state by taking the specified action.
        For a deterministic environment, this will always return one state with probability 1.0.
        """
        state_array = np.array(state)
        player_positions = np.argwhere(state_array == 1.0)

        if len(player_positions) == 0:

            return None

        px, py = player_positions[0]

        if action == 0 and px > 0:  # Up
            px -= 1
        elif action == 1 and px < self.grid_size - 1:  # Down
            px += 1
        elif action == 2 and py > 0:  # Left
            py -= 1
        elif action == 3 and py < self.grid_size - 1:  # Right
            py += 1

        next_state = np.zeros((self.grid_size, self.grid_size), dtype=np.float32)
        next_state[px, py] = 1.0
        for tx, ty in self.treasures:
            next_state[tx, ty] = 2.0
        if self.collected_treasures < 3:
            ex, ey = self.enemy_pos
            next_state[ex, ey] = 3.0
        mx, my = self.meta_flag
        next_state[mx, my] = 4.0

        return {tuple(map(tuple, next_state)): 1.0}  # Deterministic: Only one next state with prob = 1.0

    def get_next_state(self, state, action):
        px, py = self.player_pos

        if action == 0 and px > 0:  # Up
            px -= 1
        elif action == 1 and px < self.grid_size - 1:  # Down
            px += 1
        elif action == 2 and py > 0:  # Left
            py -= 1
        elif action == 3 and py < self.grid_size - 1:  # Right
            py += 1

        next_state = np.zeros((self.grid_size, self.grid_size), dtype=np.float32)
        next_state[px, py] = 1.0
        for tx, ty in self.treasures:
            next_state[tx, ty] = 2.0
        if self.collected_treasures < 3:
            ex, ey = self.enemy_pos
            next_state[ex, ey] = 3.0
        mx, my = self.meta_flag
        next_state[mx, my] = 4.0
        return tuple(map(tuple, next_state))

    def get_all_states(self):
        treasure_combinations = list(itertools.product([0, 1], repeat=len(self.treasures)))
        all_states = []

        enemy_column = self.enemy_pos[1]
        enemy_positions = [(row, enemy_column) for row in range(self.grid_size)]

        for player_pos in itertools.product(range(self.grid_size), repeat=2):
            for enemy_pos in enemy_positions:
                for treasure_state in treasure_combinations:
                    self.player_pos = player_pos
                    self.enemy_pos = enemy_pos
                    self.collected_treasures = sum(treasure_state)
                    self.treasures = [self.treasures[i] for i in range(len(self.treasures)) if treasure_state[i] == 0]
                    state = self._get_state()
                    all_states.append(tuple(map(tuple, state)))

        return all_states

    def close(self):
        if self.pygame_initialized:
            pygame.quit()

    def get_reward(self, state, action, next_state):
        next_state_array = np.array(next_state)

        # Check if the player position exists in the next state
        player_positions = np.argwhere(next_state_array == 1.0)
        if len(player_positions) == 0:
            return 0.0
            raise ValueError(f"Invalid next_state: Player position not found. State:\n{next_state_array}")

        px, py = player_positions[0]

        # Check if player reached a treasure
        if (px, py) in self.treasures:
            return 0.1

        # Check if player reached the meta flag
        if (px, py) == self.meta_flag and self.collected_treasures == len(self.treasures):
            return 0.5

        # Check if player is caught by the enemy
        enemy_positions = np.argwhere(next_state_array == 3.0)
        if len(enemy_positions) > 0:
            ex, ey = enemy_positions[0]
            if (px, py) == (ex, ey):
                return -0.2

        # Default reward
        return 0.0


# Example usage
if __name__ == "__main__":
    env = TreasureHuntEnv(render_mode="pygame")
    state = env.reset()
    done = False

    while not done:
        action = np.random.choice(env.get_possible_actions(state))
        state, reward, done, _ = env.step(action)

        env.render()

    env.close()
