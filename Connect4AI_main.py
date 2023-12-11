import re
import random
import copy


# Confirm user choice to initiate game
def start_game():
    while True:
        user_choice = input(
            "\n┌─----------------------Connect 4------------------------─┐"
            "\n│ Versus AI     - One Player, Standard Board, AI          │"
            "\n└─-------------------------------------------------------─┘\n"
            " Enter (Y) to continue or (N) to close: "
        )
        if user_choice.lower() == "y" or user_choice.lower() == "yes":
            return True
        elif user_choice.lower() == "n" or user_choice.lower() == "no":
            print("\nThank you for playing Connect-4 made by me! Goodbye!")
            exit()
        else:
            print("\nInvalid input! Please enter (Y) or (N)!")
            continue

# Customize board size
def custom_board():
    while True:
        user_choice = input(
            "\n\n\n\nWhat size board would you like to play on? (Default is 6x7)"
            "\n\nPlay on a 6x7 board? (Y/N): "
        )
        if user_choice.lower() == "y" or user_choice.lower() == "yes":
            return 6, 7
        elif user_choice.lower() == "n" or user_choice.lower() == "no":
            try:
                num_rows = int(input("\n\n\n\nPlease enter the number of rows you would like to play on:\n => : "))
                num_cols = int(input("\n\n\n\nPlease enter the number of columns you would like to play on:\n => : "))
                break
            except ValueError:
                print("\nInvalid input! Please enter a valid integer.")
                continue
            
    return num_rows, num_cols        

# Generate new game board and return index list of columns
def generate_game_board(rows: int, cols: int):
    game_board = [[" " for _ in range(cols)] for _ in range(rows)]
    columns_list = [
        " " + str(x) + " " if x < 10 else str(x) for x in range(1, cols + 1)
    ]
    return game_board, columns_list


def check_free_columns(game_board: list, num_cols: int):
    return [
        (col + 1)
        for col in range(num_cols)
        if game_board[0][col] == " "
    ]


# Ask user for col choice and place token on board
def new_token_col(
    player_name: str, free_columns_index: list, matrix
):
    if player_name == "AI":
        return monte_carlo_ai_placement(matrix)

    while True:
        col_choice = int(
            input(f"Choose a column to drop your token.\n => : ")
        )
        if col_choice not in free_columns_index:
            print(
            f"\nIncorrect input!"
            f"\nChoose one of the free columns: {free_columns_index}"
            ) 
        else:
            return col_choice


def place_token(game_board: list, num_rows: int, num_cols: int, player_symbol: str):
    for current_row in range(num_rows - 1, -1, -1):
        if game_board[current_row][num_cols - 1] == " ":
            game_board[current_row][num_cols - 1] = player_symbol
            last_row_col_placement = (current_row, num_cols - 1)
            return game_board, last_row_col_placement
    
    # Return a default value if token placement is not successful
    return game_board, (0, 0)


def winner_check(
    game_board: list,
    player_symbol: str,
    last_token: tuple,
    num_rows: int,
    num_cols: int,
):
    row, col = last_token

    directions = ((1, 0),(0, 1),(1, 1),(1, -1),)

    # Checking every possible direction for blocks
    for x, y in directions:
        count = 1
        for dir in [1, -1]:
            for step in range(1, 4):
                x_new = row + x * step * dir
                y_new = col + y * step * dir
                if 0 <= x_new < num_rows and 0 <= y_new < num_cols:
                    if game_board[x_new][y_new] == player_symbol:
                        count += 1
                    else:
                        break
        if count >= 4:
            return True
    return False


def another_game_prompt():
    while True:
        is_play_again = input("\nDo you want to play again [Y/N] ? \n => : ")
        if is_play_again.lower() == "yes" or is_play_again.lower() == "y":
            return True
        elif (
            is_play_again.lower() == "no" or is_play_again.lower() == "n"
        ):
            return False
        else:
            print(f"\Invalid input!")


# Simple - MCTS - Model
def monte_carlo_ai_placement(matrix):
    first_move_scores = {}
    first_move_col = int()
    player_token = "x"
    ai_token = "o"

    # Number of random played games - simulation
    for game_number in range(100):
        mc_matrix = copy.deepcopy(matrix)
        for counter in range(0, 100):
            free_col = check_free_columns(mc_matrix, num_cols)
            random_col = random.choice(free_col) - 1

            if counter == 0:
                if random_col not in first_move_scores:
                    first_move_scores[random_col] = 0
                first_move_col = random_col

            if counter % 2 == 0:
                player_symbol = ai_token
            else:
                player_symbol = player_token

            # AI Place random token
            mc_matrix, last_token_position  = place_token(
                mc_matrix, num_rows, random_col, player_symbol
            )

            # Flags for Winner or Draw Game
            win_flag  = winner_check(
                mc_matrix,
                player_symbol,
                last_token_position ,
                num_rows,
                num_cols,
            )
            
            if len(check_free_columns(mc_matrix, num_cols)) > 0:
                end_game_flag = False
            else:
                end_game_flag = True
            
            if win_flag  or end_game_flag:
                # Winner
                if win_flag :
                    if player_symbol == ai_token:
                        first_move_scores[first_move_col] += 6
                    elif player_symbol == player_token:
                        first_move_scores[first_move_col] -= 4

                # Draw
                elif end_game_flag:
                    first_move_scores[first_move_col] -= 1

                break

    sorted_all_moves = sorted(first_move_scores.items(), key=lambda k: (-k[1], k[0]))
    return sorted_all_moves[0][0]


def print_game_board(game_board: list, cols_print: list, num_cols: int):
    print("\n\n\n\n\n\n\n")

    print("|" + "|".join(cols_print) + "|")
    [
        print(
            "|" + "---|" * (num_cols - 1) + "---|\n" + "|-" + "-|-".join(x),
            end="-|\n",
        )
        for x in game_board
    ]
    print("-" + "----" * (num_cols - 1) + "----\n")

# Start game and initialize variables
start_game()
num_rows, num_cols = custom_board()
players_dict = {}
players_dict["You"] = "x"  # Player
players_dict["AI"] = "o"  # AI
is_winner = False  # Either player wins
is_game_end = False  # Draw
is_play_again = False  # New game



# Create board
board, cols_print = generate_game_board(num_rows, num_cols)

# While one of two condition is met [Winner] or [No more moves].
while not is_winner and not is_game_end:
    # Using for-loop to rotate players turns.
    for player_name, players_symbol in players_dict.items():
        print_game_board(board, cols_print, num_cols)
        free_columns = check_free_columns(
            board, num_cols
        )
        column_to_place = new_token_col(
            player_name, free_columns, board
        )

        board, r_c_last_token = place_token(
            board, num_rows, column_to_place, players_symbol
        )

        # Check if there is a winner ( based on last placed token )
        is_winner = winner_check(
            board, players_symbol, r_c_last_token, num_rows, num_cols
        )

        # Check if there is more empty spaces
        is_game_end = (
            False if len(check_free_columns(board, num_cols)) > 0 else True
        )

        # exit on game end or start another
        if is_winner or is_game_end:
            print_game_board(board, cols_print, num_cols)

            if is_winner:
                print(f"{player_name} won this round!")
            elif is_game_end:
                print("\n┌-------------DRAW-------------")

            # Prompt user to play arouther round
            is_play_again = another_game_prompt()
            break

    # Reset game for another round
    if is_play_again:
        is_winner = False
        is_game_end = False
        is_play_again = False
        board, cols_print = generate_game_board(
            num_rows, num_cols
        )
        continue

print("\n\nThank you for playing")
