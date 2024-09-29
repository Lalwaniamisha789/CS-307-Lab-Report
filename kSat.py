import random

# Step 1: Random k-SAT Problem Generation
def generate_k_sat(k, m, n):
    clauses = []
    for _ in range(m):
        clause = random.sample(range(1, n + 1), k)  # Select k distinct variables
        clause = [var if random.choice([True, False]) else -var for var in clause]  # Randomly negate
        clauses.append(clause)
    return clauses

# Step 2: Implement Search Algorithms
def evaluate(solution, clauses):
    return sum(all(variable in solution or -variable not in solution for variable in clause) for clause in clauses)

def hill_climbing(clauses, n):
    solution = [random.choice([-1, 1]) * i for i in range(1, n + 1)]
    current_eval = evaluate(solution, clauses)

    while True:
        neighbors = []
        for i in range(n):
            neighbor = solution[:]
            neighbor[i] = -neighbor[i]  # Flip the variable
            neighbors.append(neighbor)
        
        next_solution = max(neighbors, key=lambda x: evaluate(x, clauses))
        next_eval = evaluate(next_solution, clauses)

        if next_eval <= current_eval:
            break
        solution, current_eval = next_solution, next_eval
    
    return solution, current_eval

def beam_search(clauses, n, beam_width):
    solutions = [[random.choice([-1, 1]) * i for i in range(1, n + 1)]]
    while True:
        new_solutions = []
        for sol in solutions:
            for i in range(n):
                neighbor = sol[:]
                neighbor[i] = -neighbor[i]  # Flip the variable
                new_solutions.append(neighbor)
        
        new_solutions.sort(key=lambda x: evaluate(x, clauses), reverse=True)
        solutions = new_solutions[:beam_width]
        
        if evaluate(solutions[0], clauses) == len(clauses):  # All clauses satisfied
            return solutions[0], evaluate(solutions[0], clauses)

def variable_neighborhood_descent(clauses, n):
    solution = [random.choice([-1, 1]) * i for i in range(1, n + 1)]
    current_eval = evaluate(solution, clauses)

    neighborhoods = [list(range(1, n + 1)) for _ in range(3)]  # Three neighborhoods

    while True:
        improved = False
        for neighborhood in neighborhoods:
            for var in neighborhood:
                neighbor = solution[:]
                neighbor[var - 1] = -neighbor[var - 1]  # Flip the variable
                next_eval = evaluate(neighbor, clauses)

                if next_eval > current_eval:
                    solution, current_eval = neighbor, next_eval
                    improved = True
                    break
            
            if improved:
                break

        if not improved:
            break

    return solution, current_eval

# Step 3: Heuristic Functions
def heuristic1(solution, clauses):
    return evaluate(solution, clauses)

def heuristic2(solution, clauses):
    return len(clauses) - evaluate(solution, clauses)

# Step 4: Performance Comparison
def run_experiment(k, m_values, n_values):
    results = {}
    for m in m_values:
        for n in n_values:
            clauses = generate_k_sat(k, m, n)
            results[(m, n)] = {}
            
            # Hill Climbing
            hc_solution, hc_eval = hill_climbing(clauses, n)
            results[(m, n)]['Hill Climbing'] = (hc_solution, hc_eval)
            
            # Beam Search with width 3
            bs_solution_3, bs_eval_3 = beam_search(clauses, n, 3)
            results[(m, n)]['Beam Search (width 3)'] = (bs_solution_3, bs_eval_3)
            
            # Beam Search with width 4
            bs_solution_4, bs_eval_4 = beam_search(clauses, n, 4)
            results[(m, n)]['Beam Search (width 4)'] = (bs_solution_4, bs_eval_4)
            
            # Variable Neighborhood Descent
            vnd_solution, vnd_eval = variable_neighborhood_descent(clauses, n)
            results[(m, n)]['Variable Neighborhood Descent'] = (vnd_solution, vnd_eval)
    
    return results

# Example usage
m_values = [5, 10, 15]  # Number of clauses
n_values = [4, 5, 6]    # Number of variables
performance_results = run_experiment(3, m_values, n_values)

# Display results
for key, value in performance_results.items():
    print(f"m={key[0]}, n={key[1]}:")
    for algorithm, (solution, eval_value) in value.items():
        print(f"  {algorithm}: Solution: {solution}, Satisfied Clauses: {eval_value}/{key[0]}")
