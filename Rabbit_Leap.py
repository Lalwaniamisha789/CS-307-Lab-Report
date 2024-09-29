from collections import deque

def is_valid(state):
    # We don't need to check validity explicitly as all transitions will be valid
    return True

def get_successors(state):
    successors = []
    empty_index = state.index('-')
    
    # Define possible moves for the empty stone
    possible_moves = [
        (empty_index - 1, empty_index),   # Move left 1 step
        (empty_index - 2, empty_index),   # Move left 2 steps
        (empty_index + 1, empty_index),   # Move right 1 step
        (empty_index + 2, empty_index)    # Move right 2 steps
    ]
    
    for move_from, move_to in possible_moves:
        if 0 <= move_from < len(state):
            new_state = list(state)
            # Swap the empty stone with the rabbit
            new_state[move_to], new_state[move_from] = new_state[move_from], new_state[move_to]
            if is_valid(new_state):
                successors.append(tuple(new_state))
    
    return successors

def bfs(start_state, goal_state):
    queue = deque([(start_state, [])])
    visited = set()
    
    while queue:
        (state, path) = queue.popleft()
        if state in visited:
            continue
        visited.add(state)
        path = path + [state]
        
        if state == goal_state:
            return path
        
        for successor in get_successors(state):
            queue.append((successor, path))
    
    return None

def dfs(start_state, goal_state):
    stack = [(start_state, [])]  # Stack for DFS
    visited = set()
    
    while stack:
        state, path = stack.pop()  # Pop the top element from the stack
        if state in visited:
            continue
        visited.add(state)
        path = path + [state]
        
        if state == goal_state:
            return path
        
        for successor in get_successors(state):
            stack.append((successor, path))  # Push the successor states onto the stack
    
    return None

# Initial state: three east-bound rabbits on the left, three west-bound on the right, and one empty stone in the middle
start_state = ('E', 'E', 'E', '-', 'W', 'W', 'W')
goal_state = ('W', 'W', 'W', '-', 'E', 'E', 'E')

solution = bfs(start_state, goal_state)
if solution:
    print("Solution found:")
    for step in solution:
        print(step)
else:
    print("No solution found.")