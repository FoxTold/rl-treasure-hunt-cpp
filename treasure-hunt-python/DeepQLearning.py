import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from collections import deque
import random

# Enhanced Neural Network for Q-Learning
class AdvancedDQNetwork(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(AdvancedDQNetwork, self).__init__()
        self.fc1 = nn.Linear(input_dim, 256)
        self.fc2 = nn.Linear(256, 256)
        self.fc3 = nn.Linear(256, 128)
        self.fc4 = nn.Linear(128, output_dim)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.relu(self.fc3(x))
        return self.fc4(x)

# Deep Q-Learning Agent
class DeepQLearningAgent:
    def __init__(self, env, state_dim, action_dim, learning_rate=0.001, discount_factor=0.99, exploration_rate=1.0, exploration_decay=0.995, min_exploration_rate=0.01, batch_size=64, memory_size=10000):
        self.env = env
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay
        self.min_exploration_rate = min_exploration_rate
        self.batch_size = batch_size

        # Replay memory
        self.memory = deque(maxlen=memory_size)

        # Device setup for GPU/CPU
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Q-network and optimizer
        self.q_network = AdvancedDQNetwork(state_dim, action_dim).to(self.device)
        self.target_network = AdvancedDQNetwork(state_dim, action_dim).to(self.device)
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=learning_rate)

        # Sync target network
        self.update_target_network()

    def update_target_network(self):
        self.target_network.load_state_dict(self.q_network.state_dict())

    def preprocess_state(self, state):
        return torch.tensor(state.flatten(), dtype=torch.float32).to(self.device)

    def choose_action(self, state):
        if random.uniform(0, 1) < self.exploration_rate:
            return random.randint(0, self.action_dim - 1)
        else:
            state_tensor = self.preprocess_state(state).unsqueeze(0)
            with torch.no_grad():
                q_values = self.q_network(state_tensor)
            return torch.argmax(q_values).item()

    def store_experience(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay(self):
        if len(self.memory) < self.batch_size:
            return

        batch = random.sample(self.memory, self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)

        states = torch.stack([self.preprocess_state(s) for s in states])
        next_states = torch.stack([self.preprocess_state(s) for s in next_states])
        actions = torch.tensor(actions, dtype=torch.int64).unsqueeze(1).to(self.device)
        rewards = torch.tensor(rewards, dtype=torch.float32).unsqueeze(1).to(self.device)
        dones = torch.tensor(dones, dtype=torch.float32).unsqueeze(1).to(self.device)

        q_values = self.q_network(states).gather(1, actions)
        with torch.no_grad():
            max_next_q_values = self.target_network(next_states).max(1, keepdim=True)[0]
            target_q_values = rewards + (1 - dones) * self.discount_factor * max_next_q_values

        loss = nn.MSELoss()(q_values, target_q_values)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def train(self, episodes=1000, target_update_frequency=10):
        self.rewards =[]
        for episode in range(episodes):
            state = self.env.reset()
            total_reward = 0
            done = False

            while not done:
                action = self.choose_action(state)
                next_state, reward, done, _ = self.env.step(action)
                self.store_experience(state, action, reward, next_state, done)
                self.replay()
                state = next_state
                total_reward += reward

            if episode % target_update_frequency == 0:
                self.update_target_network()

            self.exploration_rate = max(self.min_exploration_rate, self.exploration_rate * self.exploration_decay)
            print(f"Episode {episode + 1}/{episodes}, Total Reward: {total_reward:.2f}, Exploration Rate: {self.exploration_rate:.4f}")
            self.rewards.append(total_reward)

    def play(self, render_mode="pygame"):
        self.env.render_mode = render_mode
        state = self.env.reset()
        done = False

        while not done:
            state_tensor = self.preprocess_state(state).unsqueeze(0)
            with torch.no_grad():
                q_values = self.q_network(state_tensor)
            action = torch.argmax(q_values).item()
            state, reward, done, _ = self.env.step(action)
            self.env.render()


# Example usage
if __name__ == "__main__":
    from Environment import *
    import matplotlib.pyplot as plt

    env = TreasureHuntEnv(render_mode="none")
    state_dim = env.grid_size ** 2
    action_dim = env.action_space

    agent = DeepQLearningAgent(env, state_dim, action_dim)

    print("Training Deep Q-Learning Agent...")
    agent.train(episodes=5_000)
    plt.plot(agent.rewards)
    plt.show()
    print("Playing with the trained agent...")
    agent.play(render_mode="pygame")
