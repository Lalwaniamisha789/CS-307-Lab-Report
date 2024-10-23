import numpy as np

class NonstationaryBandit:
    def _init_(self, k=10, mean=0, std_dev=0.01):
        self.k = k
        self.mean_rewards = np.full(k, mean)
        self.std_dev = std_dev

    def step(self):
        self.mean_rewards += np.random.normal(0, self.std_dev, self.k)

    def get_reward(self, action):
        reward = np.random.normal(self.mean_rewards[action], 1)
        return reward

def bandit_nonstat(action):
    # Initialize the bandit
    bandit = NonstationaryBandit()
    
    # Perform steps to simulate the random walk
    for _ in range(1000):  # Simulate 1000 time steps
        bandit.step()
    
    # Get the reward for the specified action
    reward = bandit.get_reward(action)
    return reward

# Example of using the bandit_nonstat function
action = np.random.randint(0, 10)  # Choose a random action
reward = bandit_nonstat(action)
print("Action:", action, "Reward:", reward)
