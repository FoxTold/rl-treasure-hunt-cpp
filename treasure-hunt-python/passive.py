import numpy as np

class PassiveLearningAgent:
    def __init__(self, env, gamma=0.99, theta=1e-4):
        """
        Initialize the Passive Learning Agent.

        Args:
            env: The environment the agent interacts with.
            gamma (float): Discount factor for future rewards.
            theta (float): Convergence threshold for value iteration and policy iteration.
        """
        self.env = env
        self.gamma = gamma
        self.theta = theta
        self.value_function = np.zeros((env.grid_size, env.grid_size))  # State values
        self.policy = np.zeros((env.grid_size, env.grid_size), dtype=int)  # Policy

    def policy_evaluation(self):
        """
        Perform policy evaluation to update the value function.
        """
        while True:
            delta = 0
            for x in range(self.env.grid_size):
                for y in range(self.env.grid_size):
                    old_value = self.value_function[x, y]

                    action = self.policy[x, y]
                    self.env.player_pos = (x, y)
                    self.env.done = False  # Reset the environment's 'done' flag
                    next_state, reward, done, _ = self.env.step(action)
                    nx, ny = self.env.player_pos

                    self.value_function[x, y] = reward + self.gamma * (0 if done else self.value_function[nx, ny])
                    delta = max(delta, abs(old_value - self.value_function[x, y]))

            if delta < self.theta:
                break

    def policy_improvement(self):
        """
        Perform policy improvement to update the policy based on the value function.
        """
        policy_stable = True
        for x in range(self.env.grid_size):
            for y in range(self.env.grid_size):
                old_action = self.policy[x, y]
                best_action = old_action
                best_value = float('-inf')

                for action in range(self.env.action_space):
                    self.env.player_pos = (x, y)
                    self.env.done = False  # Reset the environment's 'done' flag
                    next_state, reward, done, _ = self.env.step(action)
                    nx, ny = self.env.player_pos

                    value = reward + self.gamma * (0 if done else self.value_function[nx, ny])
                    if value > best_value:
                        best_value = value
                        best_action = action

                self.policy[x, y] = best_action
                if old_action != best_action:
                    policy_stable = False

        return policy_stable

    def policy_iteration(self):
        """
        Perform policy iteration to find the optimal policy.
        """
        while True:
            self.policy_evaluation()
            if self.policy_improvement():
                break

    def value_iteration(self):
        """
        Perform value iteration to directly find the optimal value function and policy.
        """
        while True:
            delta = 0
            for x in range(self.env.grid_size):
                for y in range(self.env.grid_size):
                    old_value = self.value_function[x, y]
                    best_value = float('-inf')

                    for action in range(self.env.action_space):
                        self.env.player_pos = (x, y)
                        self.env.done = False  # Reset the environment's 'done' flag
                        next_state, reward, done, _ = self.env.step(action)
                        nx, ny = self.env.player_pos

                        value = reward + self.gamma * (0 if done else self.value_function[nx, ny])
                        if value > best_value:
                            best_value = value
                            self.policy[x, y] = action

                    self.value_function[x, y] = best_value
                    delta = max(delta, abs(old_value - self.value_function[x, y]))

            if delta < self.theta:
                break

    def display_policy(self):
        """
        Display the policy as a grid.
        """
        print("Policy:")
        policy_symbols = ['^', 'v', '<', '>']  # Up, Down, Left, Right
        for x in range(self.env.grid_size):
            print(" ".join(policy_symbols[self.policy[x, y]] for y in range(self.env.grid_size)))

    def display_values(self):
        """
        Display the value function as a grid.
        """
        print("Value Function:")
        print(self.value_function)

    def simulate_policy(self):
        """
        Simulate the agent's learned policy in the environment and display its behavior.
        """
        state = self.env.reset()
        self.env.render_mode = "pygame"  # Use text rendering for simplicity
        done = False
        total_reward = 0

        print("Simulating policy:")
        while not done:
            x, y = self.env.player_pos
            action = self.policy[x, y]
            state, reward, done, _ = self.env.step(action)
            total_reward += reward
            self.env.render()

        print(f"Total Reward: {total_reward}")

# Example usage
if __name__ == "__main__":
    from Environment import *
    env = TreasureHuntEnv(render_mode="none")
    agent = PassiveLearningAgent(env)

    print("Running Value Iteration...")
    agent.value_iteration()
    agent.display_policy()
    agent.display_values()

    print("Simulating learned policy...")
    agent.simulate_policy()

    print("Running Policy Iteration...")
    agent.policy_iteration()
    agent.display_policy()
    agent.display_values()
