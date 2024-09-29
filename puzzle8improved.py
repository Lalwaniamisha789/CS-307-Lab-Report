from collections import deque
import random

class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent

def get_successors(node):
    successors = []
    index = node.state.index(0)
    # Define valid moves based on the current position (0 to 8)
    moves = []
    if index % 3 > 0:  # Can move left
        moves.append(-1)
    if index % 3 < 2:  # Can move right
        moves.append(1)
    if index // 3 > 0:  # Can move up
        moves.append(-3)
    if index // 3 < 2:  # Can move down
        moves.append(3)

    # Generate successor states by swapping the 0 with a valid move
    for move in moves:
        new_index = index + move
        new_state = list(node.state)
        new_state[index], new_state[new_index] = new_state[new_index], new_state[index]
        successors.append(Node(new_state, node))

    return successors

def is_solvable(state):
    # Check if a given Puzzle-8 configuration is solvable
    inversions = 0
    state_no_zero = [x for x in state if x != 0]  # Ignore the empty space (0)
    for i in range(len(state_no_zero)):
        for j in range(i + 1, len(state_no_zero)):
            if state_no_zero[i] > state_no_zero[j]:
                inversions += 1
    # If the number of inversions is even, the puzzle is solvable
    return inversions % 2 == 0

def bfs(start_state, goal_state):
    start_node = Node(start_state)
    queue = deque([start_node])
    visited = set()
    nodes_explored = 0

    while queue:
        node = queue.popleft()
        if tuple(node.state) in visited:
            continue
        visited.add(tuple(node.state))
        nodes_explored += 1

        if node.state == goal_state:
            path = []
            while node:
                path.append(node.state)
                node = node.parent
            print(f'Total nodes explored: {nodes_explored}')
            return path[::-1]

        for successor in get_successors(node):
            if tuple(successor.state) not in visited:
                queue.append(successor)

    return None  # No solution found

# Example to generate a solvable goal state at depth D
def generate_solvable_puzzle(start_state, D):
    s_node = Node(start_state)
    d = 0
    while d < D:
        successors = get_successors(s_node)
        goal_state = random.choice(successors).state
        if is_solvable(goal_state):  # Ensure the new state is solvable
            s_node = Node(goal_state)
            d += 1
    return goal_state

# Initial state (solved state)
start_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]  

# Specify the depth D to generate a goal state
D = 20
goal_state = generate_solvable_puzzle(start_state, D)

print("Start State:", start_state)
print("Generated Goal State at depth", D, ":", goal_state)

solution = bfs(start_state, goal_state)
if solution:
    print("Solution found:")
    for step in solution:
        print(step)
else:
    print("No solution found.")
