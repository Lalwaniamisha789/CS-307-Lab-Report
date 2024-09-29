import heapq
import time

class MarbleSolitaire:
    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.goal_state = self.generate_goal_state()

    def generate_goal_state(self):
        # The goal state where only one marble remains at the center
        goal = [[0, 0, 1, 1, 1, 0, 0],
                [0, 0, 1, 1, 1, 0, 0],
                [1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 0, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1],
                [0, 0, 1, 1, 1, 0, 0],
                [0, 0, 1, 1, 1, 0, 0]]
        return goal

    def get_possible_moves(self, state):
        moves = []
        for r in range(7):
            for c in range(7):
                if state[r][c] == 1:  # If there's a marble
                    # Check all possible jump moves (up, down, left, right)
                    if r >= 2 and state[r-1][c] == 1 and state[r-2][c] == 0:  # Up
                        moves.append(((r, c), (r-2, c)))
                    if r <= 4 and state[r+1][c] == 1 and state[r+2][c] == 0:  # Down
                        moves.append(((r, c), (r+2, c)))
                    if c >= 2 and state[r][c-1] == 1 and state[r][c-2] == 0:  # Left
                        moves.append(((r, c), (r, c-2)))
                    if c <= 4 and state[r][c+1] == 1 and state[r][c+2] == 0:  # Right
                        moves.append(((r, c), (r, c+2)))
        return moves

    def apply_move(self, state, move):
        (r1, c1), (r2, c2) = move
        new_state = [row[:] for row in state]  # Copy the state
        new_state[r1][c1] = 0  # The original marble is now empty
        new_state[r2][c2] = 1  # The new position has the marble
        # Remove the jumped marble
        new_state[(r1+r2)//2][(c1+c2)//2] = 0
        return new_state

    def priority_queue_search(self):
        # Priority queue search (uniform cost search)
        start_time = time.time()
        pq = []
        heapq.heappush(pq, (0, self.initial_state))  # (path cost, state)
        visited = set()
        nodes_expanded = 0

        while pq:
            path_cost, state = heapq.heappop(pq)
            if str(state) in visited:
                continue
            visited.add(str(state))
            nodes_expanded += 1

            if state == self.goal_state:
                end_time = time.time()
                return {
                    "solution": state,
                    "path_cost": path_cost,
                    "nodes_expanded": nodes_expanded,
                    "time": end_time - start_time
                }

            for move in self.get_possible_moves(state):
                new_state = self.apply_move(state, move)
                if str(new_state) not in visited:
                    heapq.heappush(pq, (path_cost + 1, new_state))  # Increment cost

        return None  # No solution found

    def best_first_search(self, heuristic):
        start_time = time.time()
        pq = []
        heapq.heappush(pq, (heuristic(self.initial_state), self.initial_state))  # (heuristic, state)
        visited = set()
        nodes_expanded = 0

        while pq:
            _, state = heapq.heappop(pq)
            if str(state) in visited:
                continue
            visited.add(str(state))
            nodes_expanded += 1

            if state == self.goal_state:
                end_time = time.time()
                return {
                    "solution": state,
                    "nodes_expanded": nodes_expanded,
                    "time": end_time - start_time
                }

            for move in self.get_possible_moves(state):
                new_state = self.apply_move(state, move)
                if str(new_state) not in visited:
                    heapq.heappush(pq, (heuristic(new_state), new_state))

        return None  # No solution found

    def a_star_search(self, heuristic):
        start_time = time.time()
        pq = []
        heapq.heappush(pq, (heuristic(self.initial_state), 0, self.initial_state))  # (f(n), g(n), state)
        visited = set()
        nodes_expanded = 0

        while pq:
            _, g_n, state = heapq.heappop(pq)
            if str(state) in visited:
                continue
            visited.add(str(state))
            nodes_expanded += 1

            if state == self.goal_state:
                end_time = time.time()
                return {
                    "solution": state,
                    "path_cost": g_n,
                    "nodes_expanded": nodes_expanded,
                    "time": end_time - start_time
                }

            for move in self.get_possible_moves(state):
                new_state = self.apply_move(state, move)
                if str(new_state) not in visited:
                    f_n = g_n + 1 + heuristic(new_state)  # f(n) = g(n) + h(n)
                    heapq.heappush(pq, (f_n, g_n + 1, new_state))

        return None  # No solution found

# Heuristics
def h1(state):
    # Heuristic 1: Number of remaining marbles
    return sum(sum(row) for row in state)

def h2(state):
    # Heuristic 2: Number of potential moves left
    potential_moves = 0
    for r in range(7):
        for c in range(7):
            if state[r][c] == 1:
                potential_moves += len([(r2, c2) for (r2, c2) in [
                    (r-2, c), (r+2, c), (r, c-2), (r, c+2)] if 
                    0 <= r2 < 7 and 0 <= c2 < 7 and
                    state[r2][c2] == 0 and 
                    state[(r+r2)//2][(c+c2)//2] == 1])
    return potential_moves

# Compare the performance of the algorithms
def compare_algorithms(solitaire_game):
    initial_state = solitaire_game.initial_state
    
    # Run the priority queue search
    priority_result = solitaire_game.priority_queue_search()

    # Run Best-First Search with h1 and h2
    bfs_result_h1 = solitaire_game.best_first_search(h1)
    bfs_result_h2 = solitaire_game.best_first_search(h2)

    # Run A* Search with h1 and h2
    a_star_result_h1 = solitaire_game.a_star_search(h1)
    a_star_result_h2 = solitaire_game.a_star_search(h2)

    # Print or return comparison results
    return {
        "Priority Queue Search": priority_result,
        "Best-First Search (h1)": bfs_result_h1,
        "Best-First Search (h2)": bfs_result_h2,
        "A* Search (h1)": a_star_result_h1,
        "A* Search (h2)": a_star_result_h2
    }

# Example of initializing the game and comparing algorithms
initial_board = [[0, 0, 1, 1, 1, 0, 0],
                 [0, 0, 1, 1, 1, 0, 0],
                 [1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 0, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1],
                 [0, 0, 1, 1, 1, 0, 0],
                 [0, 0, 1, 1, 1, 0, 0]]

solitaire_game = MarbleSolitaire(initial_board)
comparison_results = compare_algorithms(solitaire_game)

# Display results
for algorithm, result in comparison_results.items():
    print(f"{algorithm}: {result}")
