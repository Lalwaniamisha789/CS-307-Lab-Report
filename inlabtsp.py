import math
import random

# List of 20 tourist locations in Rajasthan
locations = [
    'Jaipur', 'Jaisalmer', 'Udaipur', 'Jodhpur', 'Mount Abu', 'Bikaner', 
    'Ajmer', 'Pushkar', 'Ranthambore', 'Alwar', 'Bundi', 'Chittorgarh', 
    'Bharatpur', 'Kota', 'Shekhawati', 'Kumbhalgarh', 'Jhalawar', 
    'Barmer', 'Sikar', 'Nathdwara'
]

# Dummy distance matrix (symmetric matrix)
distances = [
    [0, 540, 395, 345, 475, 335, 135, 150, 155, 150, 215, 310, 185, 250, 295, 320, 420, 290, 220, 295],
    [540, 0, 490, 290, 610, 160, 580, 595, 720, 660, 650, 790, 655, 740, 640, 795, 885, 150, 630, 800],
    [395, 490, 0, 260, 165, 495, 310, 325, 410, 420, 335, 115, 410, 295, 380, 85, 255, 470, 370, 45],
    [345, 290, 260, 0, 350, 195, 405, 410, 570, 500, 550, 670, 420, 480, 310, 500, 450, 480, 390, 320],
    [475, 610, 165, 350, 0, 420, 520, 400, 530, 620, 520, 300, 520, 350, 440, 330, 170, 620, 480, 590],
    [335, 160, 495, 195, 420, 0, 340, 400, 500, 450, 440, 640, 480, 540, 480, 600, 700, 350, 510, 700],
    [135, 580, 310, 405, 520, 340, 0, 130, 260, 250, 180, 310, 220, 280, 340, 350, 390, 150, 270, 360],
    [150, 595, 325, 410, 400, 400, 130, 0, 250, 300, 230, 350, 290, 300, 300, 450, 520, 160, 270, 390],
    [155, 720, 410, 570, 530, 500, 260, 250, 0, 400, 450, 510, 350, 520, 450, 520, 600, 300, 400, 510],
    [150, 660, 420, 500, 620, 450, 250, 300, 400, 0, 300, 350, 250, 350, 400, 450, 600, 320, 250, 370],
    [215, 650, 335, 550, 520, 440, 180, 230, 450, 300, 0, 380, 290, 320, 240, 300, 450, 180, 150, 300],
    [310, 790, 115, 670, 300, 640, 310, 350, 510, 350, 380, 0, 430, 490, 320, 400, 580, 230, 370, 470],
    [185, 655, 410, 420, 520, 480, 220, 290, 350, 250, 290, 430, 0, 340, 250, 250, 390, 290, 220, 380],
    [250, 740, 295, 480, 350, 540, 280, 300, 520, 350, 320, 490, 340, 0, 350, 450, 590, 270, 210, 470],
    [295, 640, 380, 310, 440, 480, 340, 300, 450, 400, 240, 320, 250, 350, 0, 400, 500, 320, 260, 370],
    [320, 795, 85, 500, 330, 600, 350, 450, 520, 450, 300, 400, 250, 450, 400, 0, 310, 360, 300, 450],
    [420, 885, 255, 450, 170, 700, 390, 520, 600, 600, 450, 580, 390, 590, 500, 310, 0, 490, 440, 540],
    [290, 150, 470, 480, 620, 350, 150, 160, 300, 320, 180, 230, 290, 270, 320, 360, 490, 0, 270, 360],
    [220, 630, 370, 390, 480, 510, 270, 270, 400, 250, 150, 370, 220, 210, 260, 300, 440, 270, 0, 300],
    [295, 800, 45, 320, 590, 700, 360, 390, 510, 370, 300, 470, 380, 470, 370, 450, 540, 360, 300, 0]
]

# Function to calculate the total cost (tour distance)
def calculate_cost(tour, distances):
    total_distance = 0
    for i in range(len(tour) - 1):
        total_distance += distances[tour[i]][tour[i + 1]]
    # Add the distance to return to the starting city
    total_distance += distances[tour[-1]][tour[0]]
    return total_distance

# Function to generate a random initial solution (random tour)
def random_tour(num_locations):
    return random.sample(range(num_locations), num_locations)

# Function to generate a neighboring solution by swapping two cities
def generate_neighbor(tour):
    new_tour = tour[:]
    i, j = random.sample(range(len(tour)), 2)
    new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
    return new_tour

# Simulated Annealing algorithm
def simulated_annealing(distances, initial_temp, cooling_rate, num_iterations):
    num_locations = len(distances)
    current_tour = random_tour(num_locations)
    current_cost = calculate_cost(current_tour, distances)
    best_tour = current_tour[:]
    best_cost = current_cost
    temperature = initial_temp
    
    for iteration in range(num_iterations):
        # Generate a neighboring solution
        new_tour = generate_neighbor(current_tour)
        new_cost = calculate_cost(new_tour, distances)

        # Calculate the change in cost
        delta_cost = new_cost - current_cost

        # Accept the new solution with a probability based on temperature
        if delta_cost < 0 or random.random() < math.exp(-delta_cost / temperature):
            current_tour = new_tour
            current_cost = new_cost

            # Update the best solution if the new one is better
            if new_cost < best_cost:
                best_tour = new_tour
                best_cost = new_cost

        # Cool down the temperature
        temperature *= cooling_rate

        # Optionally print progress every few iterations
        if iteration % 10 == 0:
            print(f"Iteration {iteration}, Best cost so far: {best_cost}")

    return best_tour, best_cost

# Example usage
initial_temperature = 500
cooling_rate = 0.995
num_iterations = 500

best_tour, best_cost = simulated_annealing(distances, initial_temperature, cooling_rate, num_iterations)
print("Best tour found:", best_tour)
print("Best tour cost:", best_cost)

# Output the best tour and its cost (interpreted in terms of locations)
best_tour_locations = [locations[i] for i in best_tour]
print("Best tour locations:", best_tour_locations)
