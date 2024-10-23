import numpy as np

class EpsilonGreedyBinaryBandit:
    def _init_(self, epsilon=0.1, num_actions=2):
        self.epsilon = epsilon
        self.num_actions = num_actions
        self.action_values = np.zeros(num_actions)  # Estimated reward for each action
        self.action_counts = np.zeros(num_actions)  # Number of times each action was chosen
    
    def select_action(self):
        """Selects an action using epsilon-greedy strategy."""
        if np.random.rand() < self.epsilon:
            return np.random.choice(self.num_actions)  # Explore: choose random action
        else:
            return np.argmax(self.action_values)  # Exploit: choose action with highest estimated reward
    
    def update_estimates(self, action, reward):
        """Updates the estimated reward for the chosen action."""
        self.action_counts[action] += 1
        n = self.action_counts[action]
        # Update action-value estimate using incremental formula
        self.action_values[action] += (1 / n) * (reward - self.action_values[action])

    def simulate(self, bandit, iterations=1000):
        """Simulates the bandit problem for a given number of iterations."""
        rewards = np.zeros(iterations)
        for i in range(iterations):
            action = self.select_action()
            reward = bandit(action)  # Get reward for the chosen action
            rewards[i] = reward
            self.update_estimates(action, reward)
        return rewards

# Define bandit functions for binaryBanditA and binaryBanditB
def binary_bandit_A(action):
    p = [0.1, 0.2]  # Probabilities for actions 1 and 2
    return 1 if np.random.rand() < p[action] else 0

def binary_bandit_B(action):
    p = [0.8, 0.9]  # Probabilities for actions 1 and 2
    return 1 if np.random.rand() < p[action] else 0

# Initialize the epsilon-greedy agent
epsilon_greedy_agent_A = EpsilonGreedyBinaryBandit(epsilon=0.1)
epsilon_greedy_agent_B = EpsilonGreedyBinaryBandit(epsilon=0.1)

# Simulate the binary bandit problem for Bandit A and Bandit B
rewards_A = epsilon_greedy_agent_A.simulate(binary_bandit_A, iterations=1000)
rewards_B = epsilon_greedy_agent_B.simulate(binary_bandit_B, iterations=1000)

# Output the results
print("Total rewards for Bandit A:", sum(rewards_A))
print("Total rewards for Bandit B:", sum(rewards_B))
