import math
import random
import numpy as np
import matplotlib.pyplot as plt
import csv

def nearest_neighbor_init(dist_matrix):
    n = len(dist_matrix)
    unvisited = set(range(n))
    current_city = random.choice(list(unvisited))
    tour = [current_city]
    unvisited.remove(current_city)

    while unvisited:
        next_city = min(unvisited, key=lambda city: dist_matrix[current_city][city])
        tour.append(next_city)
        unvisited.remove(next_city)
        current_city = next_city

    return tour

def exponential_cooling(temp, alpha=0.99):
    return temp * alpha

def two_opt_swap(tour):
    new_tour = tour[:]
    i, j = random.sample(range(len(tour)), 2)
    if i > j:
        i, j = j, i
    new_tour[i:j] = reversed(new_tour[i:j])
    return new_tour

def calculate_tour_length(tour, dist_matrix):
    length = sum(dist_matrix[tour[i]][tour[i + 1]] for i in range(len(tour) - 1))
    length += dist_matrix[tour[-1]][tour[0]]  # Complete the cycle
    return length

def create_distance_matrix(coords):
    n = len(coords)
    dist_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            dist_matrix[i][j] = np.sqrt((coords[i][0] - coords[j][0]) ** 2 + (coords[i][1] - coords[j][1]) ** 2)
    return dist_matrix

def simulated_annealing(dist_matrix, max_iter=10000, init_temp=1000, cooling_rate=0.99):
    n = len(dist_matrix)
    current_tour = nearest_neighbor_init(dist_matrix)
    current_cost = calculate_tour_length(current_tour, dist_matrix)
    
    best_tour = current_tour[:]
    best_cost = current_cost
    temperature = init_temp
    
    for iteration in range(max_iter):
        new_tour = two_opt_swap(current_tour)
        new_cost = calculate_tour_length(new_tour, dist_matrix)
        
        delta_cost = new_cost - current_cost
        
        if delta_cost < 0 or random.uniform(0, 1) < math.exp(-delta_cost / temperature):
            current_tour = new_tour
            current_cost = new_cost
            
            if current_cost < best_cost:
                best_tour = current_tour
                best_cost = current_cost
        
        temperature = exponential_cooling(temperature, cooling_rate)
        
        if temperature < 1e-5:
            break
    
    return best_tour, best_cost

def plot_tour(tour, coords):
    plt.figure(figsize=(10, 8))
    
    # Create the plot, adding the first city again to complete the cycle
    plt.plot([coords[tour[i % len(tour)]][0] for i in range(len(tour) + 1)],
             [coords[tour[i % len(tour)]][1] for i in range(len(tour) + 1)],
             'ro-')  # 'ro-' means red color, round points, and lines connecting them

    plt.title("Best TSP Tour using Simulated Annealing")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.grid(True)

    # Annotate the cities
    for i, (x, y) in enumerate(coords):
        plt.annotate(f'{i + 1}', (x, y), textcoords="offset points", xytext=(0, 10), ha='center')
    
    plt.show()

def read_coordinates_from_file(file_path):
    coords = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            coords.append((float(row[0]), float(row[1])))
    return coords

# Main execution
file_path = r'C:\Users\Ammu\OneDrive\Desktop\CS-307 AI\bcl380.csv'  # Raw string

coords = read_coordinates_from_file(file_path)

dist_matrix = create_distance_matrix(coords)

# Run the improved Simulated Annealing
best_tour, best_cost = simulated_annealing(dist_matrix)

# Display the results
print("Best tour:", best_tour)
print("Best cost:", best_cost)

# Plot the best tour
plot_tour(best_tour, coords)

