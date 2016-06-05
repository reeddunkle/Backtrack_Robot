import os
import time
from random import randint
os.system('cls' if os.name == 'nt' else 'clear')

DOWN = "Down"
RIGHT = "Right"
DESTINATION = "Destination!"
EMPTY_CHAR = "[ ]"
OBSTACLE_CHAR = "[X]"
HOME_CHAR = "[+]"
DOWN_CHAR = "[|]"
RIGHT_CHAR = "[-]"
DESTINATION_CHAR = "[*]"
DOWN_RIGHT_CHAR = "[{}]".format(chr(8735))
RIGHT_DOWN_CHAR = "[{}]".format(chr(119317))

def possible_directions(row, col, obstacles):
    """Returns the moves that are legal from the given coordinates."""

    dirs = []
    if row == 0 and col == 0:
        dirs.append((0, 0))
    if col > 0 and (row, col-1) not in obstacles:
        dirs.append((row, col-1))
    if row > 0 and (row-1, col) not in obstacles:
        dirs.append((row-1, col))
    return dirs


def find_path(row, col, destination_row, destination_column, obstacles):
    """The backtrack algorithm -- returns the robot's path."""

    if (destination_row == 0 and destination_column == 1) or (destination_row == 1 and destination_column == 0):
        return [(0, 0), (row, col)]
    else:
        for coordinance in possible_directions(row, col, obstacles):
            r, c = coordinance
            if r == 0 and c == 0:
                return [(0, 0)]

            solution = find_path(r, c, destination_row, destination_column, obstacles)
            if solution:
                final = solution + [(r, c)]
                if row == destination_row and col == destination_column:
                    final += [(row, col)]
                return final


def create_board(number_of_rows, number_of_columns, obstacles):
    '''Returns an array representation of the board.'''

    board = []
    for r in range(number_of_rows + 1):
        board.append([])
        for c in range(number_of_columns + 1):
            if (r, c) in obstacles:
                board[r].append(OBSTACLE_CHAR)
            else:
                board[r].append(EMPTY_CHAR)
    return board


def coords_to_english(path):
    """Writes the English directions of the robot's path."""

    path_english = []
    for i in range(0, -1 + len(path)):
        r, c = path[i]
        next_r, next_c = path[i+1]
        if c < next_c:
            path_english.append(RIGHT)
        elif r < next_r:
            path_english.append(DOWN)

    path_english.append(DESTINATION)
    return path_english


def draw_path_to_board(board, path, destination_row, destination_column):
    """Draws the robot's path to the board."""

    # Edge case where destination is the same as starting pos
    if destination_row == 0 and destination_column == 0:
        return [HOME_CHAR]

    if path:
        path_english = coords_to_english(path)

        board[0][0] = DOWN_CHAR if path_english[0] == DOWN else RIGHT_CHAR

        for i in range(1, len(path) - 1):
            prev_move = path_english[i-1]
            next_move = path_english[i+1]
            cur_move = path_english[i]
            r, c = path[i]

            if prev_move == RIGHT and cur_move == DOWN:
                move = RIGHT_DOWN_CHAR
            elif prev_move == DOWN and cur_move == RIGHT:
                move = DOWN_RIGHT_CHAR
            elif cur_move == RIGHT:
                move = RIGHT_CHAR
            elif cur_move == DOWN:
                move = DOWN_CHAR

            board[r][c] = move

        board[destination_row][destination_column] = DESTINATION_CHAR

    return board


def char_matrix_to_string(board_matrix):
    """Returns a string representation of the board."""

    board_string = ""
    for row in board_matrix:
        row_string = "".join(row)
        board_string += row_string + "\n"

    return board_string


def print_introduction():
    """Prints the game's introduction messages."""

    print("-" * 15)
    print("Welcome to the Robot Game!")
    print("Your robot starts in the upper left corner")
    print("of the game board, at coordinates (0,0)\n")
    print("She can only move to the RIGHT and DOWN.\n")


def get_destination():
    """Gets coordinates from the user for the robot's destination"""

    prompt = "What are the coordinates of your robot's destination?\nExample: 2,2\n> "
    error_msg = "Sorry. You must enter the destination in the form Row,Column."
    test = lambda s: len([c for c in s if c.isdigit()]) > 1

    user_input = validate_user_input(prompt, error_msg, test)
    r, c = [c for c in user_input if c.isdigit()][:2]
    r = int(r)
    c = int(c)

    return (r, c)


def play_game(path, board_string, board_path_string):
    """Displays the game's process to the user."""

    print("\nOkay. Right now there are some obstacles...")
    print("Those squares are marked with a {}.\n".format(OBSTACLE_CHAR))
    print(board_string)

    message = "Looking for a path..."
    print(message, end="\r")
    time.sleep(2.2)

    if path:
        message = "Looking for a path...Success!!!"
        message += "\nCheck it out:\n"
        print(message, end="\r")
        print(board_path_string)

    else:
        message = "Looking for a path...Darn!"
        message += "\nThere doesn't seem to be a path through the obstacles!\n"
        print(message, end="\r")
        print("Such ill-placed obstacles.")


def validate_user_input(prompt, error_msg, test):
    """
    Keeps prompting the user for a valid input. <test> is a function that returns
    a Boolean value, depending on whether or not the input is valid.
    """

    user_input = input(prompt)

    while not test(user_input):
        if not test(user_input):
            print(error_msg)

        user_input = input(prompt)

    return user_input


def generate_obstacles(destination_row, destination_column):
    """Prompts the user to decide how many obstacles to generate."""

    # destination_x are coordinates, not size, thus we need to +1
    # We subtract 2 because src and trg are not allowed to have obstacles.
    max_obstacles = (destination_row + 1) * (destination_column + 1) - 2

    prompt = "Please enter a number of random obstacles:\n> "
    error_msg = "Sorry, for a board of this size\nyou can only have {} obstacles.".format(max_obstacles)

    num_obstacles = validate_user_input(prompt, error_msg, lambda s: s.isdigit() and int(s) < max_obstacles)
    num_obstacles = int(num_obstacles)

    current_obstacles = 0
    obstacles = []
    while (current_obstacles < num_obstacles):
        r = randint(0, destination_row)
        c = randint(0, destination_column)

        # Avoid placing obstacles in src and trg
        if (r == 0 and c == 0) or (r == destination_row and c == destination_column):
            continue

        elif (r, c) in obstacles:
            continue

        else:
            obstacles.append((r, c))
            current_obstacles += 1

    return obstacles


if __name__ == '__main__':
    print_introduction()
    dest_row, dest_column = get_destination()
    obstacles = generate_obstacles(dest_row, dest_column)
    game_board = create_board(dest_row, dest_column, obstacles)
    backtrack_path = find_path(dest_row, dest_column, dest_row, dest_column, obstacles)
    board_string = char_matrix_to_string(game_board)
    board_with_path = draw_path_to_board(game_board, backtrack_path, dest_row, dest_column)
    board_path_string = char_matrix_to_string(board_with_path)
    play_game(backtrack_path, board_string, board_path_string)
