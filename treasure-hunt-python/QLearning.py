import numpy as np
import random

class QLearningAgent:
    def __init__(self, env, learning_rate=0.1, discount_factor=0.99, exploration_rate=1.0, exploration_decay=0.995, min_exploration_rate=0.01):
        """
        Initialize the Q-Learning agent.
        """
        self.env = env
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay
        self.min_exploration_rate = min_exploration_rate

        self.q_table = {}

    def _get_state_key(self, state):
        """
        Convert the environment state to a hashable string key for Q-table lookup.
        """
        return str(state)

    def choose_action(self, state):
        """
        Choose an action using the epsilon-greedy strategy.
        """
        state_key = self._get_state_key(state)
        if state_key not in self.q_table:
            self.q_table[state_key] = np.zeros(self.env.action_space)

        if random.uniform(0, 1) < self.exploration_rate:
            return random.randint(0, self.env.action_space - 1)  # Explore: choose random action
        else:
            max_value = np.max(self.q_table[state_key])
            best_actions = [action for action, value in enumerate(self.q_table[state_key]) if value == max_value]
            return random.choice(best_actions)  # Randomly select among the best actions

    def update_q_table(self, state, action, reward, next_state, done):
        """
        Update the Q-table using the Q-learning formula.
        """
        state_key = self._get_state_key(state)
        next_state_key = self._get_state_key(next_state)

        if state_key not in self.q_table:
            self.q_table[state_key] = np.zeros(self.env.action_space)
        if next_state_key not in self.q_table:
            self.q_table[next_state_key] = np.zeros(self.env.action_space)

        # Update Q-value using the Bellman equation
        best_next_action = np.max(self.q_table[next_state_key]) if not done else 0
        self.q_table[state_key][action] += self.learning_rate * (
            reward + self.discount_factor * best_next_action - self.q_table[state_key][action]
        )

    def train(self, episodes=1000):
        """
        Train the Q-learning agent over a specified number of episodes.
        """
        random.seed(69)  # Set random seed for reproducibility
        np.random.seed(69)

        rewards = []
        for episode in range(episodes):
            state = self.env.reset()
            total_reward = 0
            done = False

            while not done:
                action = self.choose_action(state)
                next_state, reward, done, _ = self.env.step(action)
                self.update_q_table(state, action, reward, next_state, done)

                state = next_state
                total_reward += reward

            rewards.append(total_reward)
            self.exploration_rate = max(self.min_exploration_rate, self.exploration_rate * self.exploration_decay)
            print(f"Episode {episode + 1}/{episodes}, Total Reward: {total_reward:.2f}, Exploration Rate: {self.exploration_rate:.4f}")

        return rewards

    def play(self, render_mode="pygame"):
        """
        Play the environment using the trained Q-table.
        """
        self.env.render_mode = render_mode
        state = self.env.reset()
        done = False

        while not done:
            state_key = self._get_state_key(state)
            max_value = np.max(self.q_table.get(state_key, np.zeros(self.env.action_space)))
            best_actions = [action for action, value in enumerate(self.q_table.get(state_key, np.zeros(self.env.action_space))) if value == max_value]
            action = random.choice(best_actions)  # Randomly select among the best actions
            state, reward, done, _ = self.env.step(action)
            self.env.render()


# Example usage
if __name__ == "__main__":
    from Environment import *
    env = TreasureHuntEnv(render_mode="none")  # Disable rendering during training
    agent = QLearningAgent(env)

    print("Training Q-Learning Agent...")
    rewards = agent.train(episodes=1_000 )

    print("Playing with the trained agent...")
    agent.play(render_mode="pygame")  # Enable Pygame rendering for visualization
