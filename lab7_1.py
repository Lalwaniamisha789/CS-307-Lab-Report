import random

# MENACE class to implement Tic-Tac-Toe learning
class MENACE:
    def _init_(self):
        # Dictionary to store matchbox states and available moves (represented by beads)
        self.matchboxes = {}
        self.history = []  # Track moves made during the game

    def get_state(self, board):
        # Convert the board into a tuple representing the state
        return tuple(board)

    def choose_move(self, board):
        state = self.get_state(board)
        if state not in self.matchboxes:
            # Initialize the matchbox for the state with all possible moves (1 bead per valid move)
            moves = [i for i in range(9) if board[i] == 0]  # Valid moves (empty spots)
            self.matchboxes[state] = {move: 3 for move in moves}  # Start with 3 beads per move
        # Choose a move randomly based on bead counts (weighted random choice)
        moves = list(self.matchboxes[state].keys())
        weights = list(self.matchboxes[state].values())
        move = random.choices(moves, weights=weights)[0]
        self.history.append((state, move))  # Record move for learning
        return move

    def update_rewards(self, reward):
        # Update matchboxes based on the result of the game (reward)
        for state, move in self.history:
            if move in self.matchboxes[state]:
                self.matchboxes[state][move] = max(1, self.matchboxes[state][move] + reward)
        self.history.clear()  # Clear history after each game

    def print_board(self, board):
        symbols = [' ', 'X', 'O']
        print("\n".join(["|".join([symbols[board[i]] for i in range(j, j+3)]) for j in range(0, 9, 3)]))
        print("-----")

# Game of Tic-Tac-Toe
def check_winner(board):
    # Check all winning combinations
    wins = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    for a, b, c in wins:
        if board[a] == board[b] == board[c] != 0:
            return board[a]
    if all(x != 0 for x in board):
        return 0  # Draw
    return None  # Game ongoing

# Train MENACE
def play_game():
    menace = MENACE()
    for game in range(1000):  # Play 1000 games to train MENACE
        board = [0] * 9  # Initialize empty board
        turn = 1  # X always starts
        winner = None

        while winner is None:
            if turn == 1:
                move = menace.choose_move(board)
            else:
                # Random move for O (opponent)
                move = random.choice([i for i in range(9) if board[i] == 0])
            
            board[move] = turn
            winner = check_winner(board)
            turn = 3 - turn  # Switch turn

        if winner == 1:
            menace.update_rewards(1)  # MENACE wins
        elif winner == 2:
            menace.update_rewards(-1)  # MENACE loses
        else:
            menace.update_rewards(0)  # Draw

    return menace

# Play a game against the trained MENACE
def play_against_menace(menace):
    board = [0] * 9  # Empty board
    turn = 1  # Player 1 (X) starts
    winner = None

    while winner is None:
        if turn == 1:
            move = int(input("Enter your move (0-8): "))
        else:
            move = menace.choose_move(board)
            print(f"MENACE plays at position {move}")

        if board[move] != 0:
            print("Invalid move! Try again.")
            continue

        board[move] = turn
        menace.print_board(board)
        winner = check_winner(board)
        turn = 3 - turn  # Switch turn

    if winner == 1:
        print("You win!")
    elif winner == 2:
        print("MENACE wins!")
    else:
        print("It's a draw!")

# Train MENACE and play against it
if _name_ == "_main_":
    trained_menace = play_game()
    print("MENACE is trained. Let's play!")
    play_against_menace(trained_menace)
