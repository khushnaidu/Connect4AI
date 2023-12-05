import re
import random
import copy


# First user input possible for selecting game mode. The function return 'P' or 'Any input'
def start_game():
    while True:
        user_choice = input('\n┌─----------------------Connect 4------------------------─┐'
                            '\n│ Versus AI     - One Player, Standard Board, AI          │'
                            '\n└─-------------------------------------------------------─┘\n'
                            ' Enter (Y) to continue or (N) to close: ')
        if user_choice.lower() == "y" or user_choice.lower() == "yes":
            return True
        elif user_choice.lower() == "n" or user_choice.lower() == "no":
            print('\n\nThank you for playing Connect-4 made by me! Goodbye!')
            exit()
        else:
            print('\n\n\n\n\n\n\n\n\n\n')
            print('Invalid input! Please enter (Y) or (N)!')
            continue

# Receiving matrix row and col and Creating empty board/matrix , also create columns indexes list and return them.
def board_creating(matrix_rows: int, matrix_cols: int):
    board_matrix = [[' ' for _ in range(matrix_cols)] for _ in range(matrix_rows)]
    columns_index_print = ['-' + str(x) + '-' if x < 10 else str(x) for x in range(1, number_of_cols + 1)]
    return board_matrix, columns_index_print


def check_free_columns(matrix_board: list, matrix_cols: int):
    free_cols = [(index_col + 1) for index_col in range(matrix_cols) if matrix_board[0][index_col] == ' ']
    return free_cols


# Take the user input and check it if is valid, return correct index for token place
def player_token_placement(p_symbol: str, player_name: str, free_columns_index: list, matrix):
    if player_name == "AI":
        return monte_carlo_ai_placement(matrix)

    while True:
        try:
            column_index_place = int(input(f'Choose a column to drop your token.\n => : '))

            # If index is incorrect raise error
            if column_index_place + 1 not in free_columns_index:
                raise ValueError

            # stop the loop and return correct index for placing the player symbol
            return column_index_place

        # if error occurred print error message and show the free columns for placement
        except ValueError:
            print(f'\nIncorrect input!'
                  f'\nChoose one of the free columns: {free_columns_index}')


#  Placing the token, checking from the lowest to the upper floor/level  for empty cell / box
def place_token(board_matrix: list, matrix_rows: int, col_to_place: int, p_symbol: str):
    # Starting form the bottom of the board/matrix
    for current_row in range(matrix_rows - 1, -1, -1):

        # There is no else case, there is at least one free space guaranteed from check_free_columns().
        if board_matrix[current_row][col_to_place] == ' ':
            board_matrix[current_row][col_to_place] = p_symbol

            # Creating variable for where was placed the last token.
            last_row_col_placement = (current_row, col_to_place)

            # Return updated matrix/board and the coordinates of the last token placed
            return board_matrix, last_row_col_placement


# Function to check if there is a winner after every placement on board
def winner_check(matrix_board: list, p_symbol: str, last_r_c_token_placed: tuple, matrix_rows: int, matrix_cols: int):
    row, col = last_r_c_token_placed

    # Win pattern, going in both direction in the matrix with positive or negative step( -1 , +1 ).
    directions = (
        # (R, C) # First direction | Second direction
        (1, 0),  # Bottom - Top
        (0, 1),  # Right - Left
        (1, 1),  # Prime Diagonal
        (1, -1)  # Secondary Diagonal
    )

    # Checking every possible direction for least 4 connected/same blocks
    for dir_r, dir_c in directions:

        # The last token itself is already 1 of 4 blocks , counter = 1
        counter = 1

        # Using positive or negative step to check in both direction of a row , column or diagonal
        for direction_step_pos_or_neg in [1, -1]:

            # Checking maximum tree blocks in direction is the limit for longest chain , or maximum 7 blocks connected.
            for dir_step in range(1, 4):

                #  Token index  row/col  + ( direction pattern * dir_step (1,2,3) * step (+1 , -1 )
                new_r = row + dir_r * dir_step * direction_step_pos_or_neg
                new_c = col + dir_c * dir_step * direction_step_pos_or_neg

                # check if the new created indexes are in range of the matrix/board
                if 0 <= new_r < matrix_rows and 0 <= new_c < matrix_cols:

                    # if there is the same symbol there as the current player  counter add 1
                    if matrix_board[new_r][new_c] == p_symbol:
                        counter += 1
                    # else stop checking in this direction
                    else:
                        break

        # if counter is at least 4 = four or more connected same elements , return True ( current player is Winner )
        if counter >= 4:
            return True
    # return False there is still no winner
    return False


# Taking input from user and return boolean statement for new_game_flag
def another_game():
    # The loop is repeated until correct input yes or no.
    while True:
        do_you_want_new_game = input('\n\nDo you want to play again [Y/N] ? \n => : ')
        if do_you_want_new_game.lower() == 'yes' or do_you_want_new_game.lower() == 'y':
            return True
        elif do_you_want_new_game.lower() == 'no' or do_you_want_new_game.lower() == 'n':
            return False
        else:
            print(f'\nIncorrect input!')


# Simple - MCTS - Model
def monte_carlo_ai_placement(matrix):
    player_token = '\033[1;31m██\033[0m'
    ai_token = '\033[1;34m██\033[0m'

    all_first_moves_dict = {}
    first_move_loc = int()

    # Number of random played games - simulation
    for game_number in range(100):
        mc_matrix = copy.deepcopy(matrix)
        for counter in range(0, 100):

            free_cols = check_free_columns(mc_matrix, number_of_cols)
            random_place = random.choice(free_cols) - 1

            if counter == 0:
                if random_place not in all_first_moves_dict:
                    all_first_moves_dict[random_place] = 0
                first_move_loc = random_place

            if counter % 2 == 0:
                player_symbol = ai_token
            else:
                player_symbol = player_token

            # AI Place random token
            mc_matrix, mc_r_c_last_token = place_token(mc_matrix, number_of_rows, random_place, player_symbol)

            # Flags for Winner or Draw Game
            mc_winner_flag = winner_check(mc_matrix, player_symbol, mc_r_c_last_token, number_of_rows, number_of_cols)
            mc_end_game_flag = False if len(check_free_columns(mc_matrix, number_of_cols)) > 0 else True

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

    sorted_all_moves = (sorted(all_first_moves_dict.items(), key=lambda k: (-k[1], k[0])))
    return sorted_all_moves[0][0]

# Print - GAME BOARD
def board_print(matrix_board: list, columns_print: list, matrix_cols: int):
    # Spacing from other prints
    print('\n\n\n\n\n\n\n')

    # Columns with numbers
    print('|' + '|'.join(columns_print) + '|')

    # Every mid row and matrix row.
    [print('|' + '---|' * (matrix_cols - 1) + '---|\n' + '|-' + '-|-'.join(x), end='-|\n') for x in matrix_board]

    # Bottom frame
    print('-' + '----' * (matrix_cols - 1) + '----\n')

def winner_print(p_symbol: str, player_name: str):
    print(
        f'\n┌─---------CONGRATULATION-----------┐'
        f'\n            {player_name}                 '
        f'\n└─-------------YOU-WIN--------------┘'
    )

def draw_print():
    print(
        f'\n┌─-----------GOOD-GAME-----------┐'
        f'\n           THIS ROUND IS          '
        f'\n└─-------------DRAW--------------┘'
    )

# Start game and initialize variables
gameplay_mode = start_game()
number_of_rows, number_of_cols = 6, 7
players_dict = {}
players_dict['You'] = "x" # Player
players_dict['AI'] = "o"  # AI
winner_flag = False # Either player wins
end_game_flag = False # Draw
new_game_flag = False # New game

# Create board
board, columns_print_for_representation = board_creating(number_of_rows, number_of_cols)

# While one of two condition is met [Winner] or [No more moves].
while not winner_flag and not end_game_flag:

    # Using for-loop to rotate players turns.
    for player_name, players_symbol in players_dict.items():

        board_print(board, columns_print_for_representation, number_of_cols)
        free_columns = check_free_columns(board, number_of_cols) # Check for free columns (cols w empty on top)
        column_to_place = player_token_placement(players_symbol, player_name, free_columns, board)

        # Placing the color token in the board
        board, r_c_last_token = place_token(board, number_of_rows, column_to_place, players_symbol)

        # Check if there is a winner ( based on last placed token )
        winner_flag = winner_check(board, players_symbol, r_c_last_token, number_of_rows, number_of_cols)

        # Check if there is more empty spaces
        end_game_flag = False if len(check_free_columns(board, number_of_cols)) > 0 else True

        # if any of the flag is raised stop the loop
        if winner_flag or end_game_flag:

            # Print the final state of the board
            board_print(board, columns_print_for_representation, number_of_cols)

            # Print Winner
            if winner_flag:
                winner_print(players_symbol, player_name)

            # Print Draw
            elif end_game_flag:
                draw_print()

            # Option for new round available only in the end of the game
            new_game_flag = another_game()
            break

    # If new round is selected the game continue after the players name and color selection.
    if new_game_flag:
        # Reset all flags and create new empty board.
        winner_flag = False
        end_game_flag = False
        new_game_flag = False
        board, columns_print_for_representation = board_creating(number_of_rows, number_of_cols)
        continue

print('\n\nThank you for playing Connect-4 made by me! Goodbye!')
