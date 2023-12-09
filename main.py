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
        if col_choice + 1 not in free_columns_index:
            print(
            f"\nIncorrect input!"
            f"\nChoose one of the free columns: {free_columns_index}"
            ) 
        else:
            return col_choice - 1


# Place a token on the board
def place_token(game_board: list, num_rows: int, num_cols: int, player_symbol: str):
    for current_row in range(num_rows - 1, -1, -1):
        if game_board[current_row][num_cols] == " ":
            game_board[current_row][num_cols] = player_symbol
            last_row_col_placement = (current_row, num_cols)
            return game_board, last_row_col_placement


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
    player_token = "\033[1;31m██\033[0m"
    ai_token = "\033[1;34m██\033[0m"

    all_first_moves_dict = {}
    first_move_loc = int()

    # Number of random played games - simulation
    for game_number in range(100):
        mc_matrix = copy.deepcopy(matrix)
        for counter in range(0, 100):
            free_cols = check_free_columns(mc_matrix, num_cols)
            random_place = random.choice(free_cols) - 1

            if counter == 0:
                if random_place not in all_first_moves_dict:
                    all_first_moves_dict[random_place] = 0
                first_move_loc = random_place

            if counter % 2 == 0:
                player_symbol = "x"  # Player
            else:
                player_symbol = "o"  # AI

            # AI Place random token
            mc_matrix, mc_r_c_last_token = place_token(
                mc_matrix, num_rows, random_place, player_symbol
            )

            # Flags for Winner or Draw Game
            mc_winner_flag = winner_check(
                mc_matrix,
                player_symbol,
                mc_r_c_last_token,
                num_rows,
                num_cols,
            )
            mc_end_game_flag = (
                False
                if len(check_free_columns(mc_matrix, num_cols)) > 0
                else True
            )

            # if any of the flag is raised stop the loop
            if mc_winner_flag or mc_end_game_flag:
                # Rewarding system
                # State Winner
                if mc_winner_flag:
                    if player_symbol == ai_token:
                        all_first_moves_dict[first_move_loc] += 6
                    elif player_symbol == player_token:
                        all_first_moves_dict[first_move_loc] -= 4

                # State Draw
                elif mc_end_game_flag:
                    all_first_moves_dict[first_move_loc] -= 1

                break

    sorted_all_moves = sorted(all_first_moves_dict.items(), key=lambda k: (-k[1], k[0]))
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
gameplay_mode = start_game()
num_rows, num_cols = 6, 7
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
            players_symbol, player_name, free_columns, board
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
