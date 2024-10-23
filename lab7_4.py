import numpy as np
import matplotlib.pyplot as plt

# Initialize variables
n_arms = 10
n_steps = 10000
epsilon = 0.1
alpha = 0.1  # Forgetting factor

# Initialize rewards and estimates
true_rewards = np.zeros(n_arms)
estimated_rewards = np.zeros(n_arms)
action_counts = np.zeros(n_arms)
cumulative_rewards = []

# Simulate 10-armed bandit with non-stationary rewards
for step in range(n_steps):
    # Non-stationary reward evolution
    true_rewards += np.random.normal(0, 0.01, n_arms)
    
    # Epsilon-greedy action selection
    if np.random.rand() < epsilon:
        action = np.random.randint(n_arms)
    else:
        action = np.argmax(estimated_rewards)
    
    # Get reward from the selected arm
    reward = np.random.normal(true_rewards[action], 1)
    
    # Update estimated rewards with forgetting factor
    estimated_rewards[action] += alpha * (reward - estimated_rewards[action])
    
    # Track cumulative rewards
    if step == 0:
        cumulative_rewards.append(reward)
    else:
        cumulative_rewards.append(cumulative_rewards[-1] + reward)

# Plot the cumulative reward graph
plt.plot(cumulative_rewards)
plt.xlabel('Iterations')
plt.ylabel('Cumulative Reward')
plt.title('Modified Epsilon-Greedy Algorithm Performance')
plt.show()
