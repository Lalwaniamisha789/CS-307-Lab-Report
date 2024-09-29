import numpy as np
import random
import math
import h5py

# Load the scrambled image from the MATLAB file
with h5py.File(r'C:\Users\Ammu\OneDrive\Desktop\CS-307 AI\scrambled_lena (1).mat', 'r') as mat_file:
    scrambled_image = np.array(mat_file['scrambled_lena'])  # Adjust the key according to your .mat file structure

# Flatten the scrambled image for processing
scrambled_image_flat = scrambled_image.flatten()

# Define the cost function
def calculate_cost(state, goal_state):
    # Calculate the cost as the number of mismatched pieces
    cost = sum(1 for i in range(len(state)) if state[i] != goal_state[i])
    return cost

# Function to swap two pieces
def swap(state, i, j):
    new_state = state[:]
    new_state[i], new_state[j] = new_state[j], new_state[i]
    return new_state

# Simulated annealing algorithm
def simulated_annealing(initial_state, goal_state, initial_temp, cooling_rate):
    current_state = initial_state
    current_cost = calculate_cost(current_state, goal_state)
    
    best_state = current_state
    best_cost = current_cost

    temp = initial_temp
    
    while temp > 1:
        # Select two random indices to swap
        i, j = random.sample(range(len(current_state)), 2)
        new_state = swap(current_state, i, j)
        new_cost = calculate_cost(new_state, goal_state)

        # Accept new state if it has a lower cost, or probabilistically accept a worse state
        if new_cost < current_cost or random.uniform(0, 1) < math.exp((current_cost - new_cost) / temp):
            current_state = new_state
            current_cost = new_cost
            
            # Update best state if necessary
            if current_cost < best_cost:
                best_state = current_state
                best_cost = current_cost

        # Decrease temperature
        temp *= cooling_rate

    return best_state, best_cost

# Assuming the goal state is the correct order of pieces
goal_state = np.arange(len(scrambled_image_flat))  # Correct order of the puzzle pieces

# Initialize parameters
initial_temp = 1000
cooling_rate = 0.95

# Run the simulated annealing algorithm
best_state, best_cost = simulated_annealing(scrambled_image_flat, goal_state, initial_temp, cooling_rate)

# Reshape the best_state back to the original image shape
best_image = np.array(best_state).reshape(scrambled_image.shape)

# Display the final result or save it for further analysis
print(f"Best cost (number of incorrect pieces): {best_cost}")

# Optionally save the result to a new MATLAB file
from scipy.io import savemat

# Save the reconstructed image
savemat(r'C:\Users\Ammu\OneDrive\Desktop\CS-307 AI\reconstructed_lena.mat', {'reconstructed_lena': best_image})
